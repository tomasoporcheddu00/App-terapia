#!/usr/bin/env python3
"""
Validazione dei contenuti clinici in data/.

Controlla che i JSON siano ben formati, che i riferimenti incrociati puntino a entità esistenti,
che gli stati editoriali siano coerenti e che ogni scheda popolata dichiari almeno una fonte.

Uso:
    python3 tools/validate_data.py            # riepilogo + errori
    python3 tools/validate_data.py --verbose  # elenca anche gli avvisi
    python3 tools/validate_data.py --json     # esito in JSON (per la CI)

Esce con codice 1 se trova errori (gli avvisi non fanno fallire la validazione).
"""
from __future__ import annotations
import json, sys, argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
STATI = {"placeholder", "source-review", "clinician-approved", "regulatory-review"}
SEVERITA = {"contraindicated", "major", "moderate", "minor"}
CLASSI_RACC = {"I", "IIa", "IIb", "III", None}
LIVELLI = {"A", "B", "C", None}

errori: list[str] = []
avvisi: list[str] = []


def err(msg: str) -> None:
    errori.append(msg)


def avv(msg: str) -> None:
    avvisi.append(msg)


def carica(cartella: str) -> dict[str, dict]:
    out: dict[str, dict] = {}
    d = DATA / cartella
    if not d.is_dir():
        err(f"cartella mancante: data/{cartella}")
        return out
    for f in sorted(d.glob("*.json")):
        try:
            out[f.stem] = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            err(f"data/{cartella}/{f.name}: JSON non valido — {e}")
    return out


def stato(o: dict) -> str:
    return ((o or {}).get("meta") or {}).get("editorialStatus", "")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", action="store_true", dest="as_json")
    args = ap.parse_args()

    drugs = carica("drugs")
    classes = carica("classes")
    dosing = carica("dosing")
    interactions = carica("interactions")
    regulatory = carica("regulatory")
    recommendations = carica("recommendations")
    rules = carica("rules")

    if not drugs:
        err("nessuna scheda-farmaco trovata")
        print("\n".join(errori))
        return 1

    # ---- schede-farmaco ----
    for did, d in drugs.items():
        p = f"drugs/{did}"
        meta = d.get("meta") or {}
        if meta.get("id") != did:
            err(f"{p}: meta.id ('{meta.get('id')}') diverso dal nome del file")
        st = stato(d)
        if st not in STATI:
            err(f"{p}: stato editoriale sconosciuto '{st}'")
        if st == "placeholder":
            continue

        # una scheda popolata deve dichiarare le fonti
        if not (meta.get("sources") or []):
            err(f"{p}: scheda popolata senza fonti in meta.sources")
        for s in meta.get("sources") or []:
            if not (s or {}).get("citation"):
                avv(f"{p}: una fonte non ha il campo 'citation'")

        cl = d.get("clinical") or {}
        if not (cl.get("authorisedIndications") or cl.get("guidelineIndications")):
            avv(f"{p}: nessuna indicazione (né autorizzata né da linee guida)")
        if not cl.get("absoluteContraindications"):
            avv(f"{p}: nessuna controindicazione assoluta registrata")

        # riferimenti incrociati
        for cid in d.get("classIds") or []:
            if cid not in classes:
                err(f"{p}: classId '{cid}' non corrisponde ad alcuna classe")
        for k in ("antidoteDrugIds", "alternativeDrugIds"):
            for rid in cl.get(k) or []:
                if rid not in drugs:
                    err(f"{p}: {k} rimanda a '{rid}', che non esiste")

        # farmacocinetica: l'emivita è stata completata su tutte le schede popolate
        pk = ((d.get("deep") or {}).get("pharmacokinetics") or {})
        if not pk.get("halfLife"):
            avv(f"{p}: emivita (halfLife) non compilata")

    # ---- classi ----
    for cid, c in classes.items():
        if stato(c) == "placeholder":
            continue
        for m in c.get("memberDrugIds") or []:
            if m not in drugs:
                err(f"classes/{cid}: memberDrugIds rimanda a '{m}', che non esiste")

    # ---- posologie ----
    for key, o in dosing.items():
        p = f"dosing/{key}"
        did = o.get("drugId")
        if did not in drugs:
            err(f"{p}: drugId '{did}' non esiste")
        if not o.get("dose"):
            err(f"{p}: campo 'dose' vuoto")
        ev = o.get("approvalEvidence") or {}
        if ev.get("smpcVerified") and not ev.get("clinicalReviewDone"):
            avv(f"{p}: marcato come verificato su RCP ma senza revisione clinica")

    # ---- interazioni ----
    for did, o in interactions.items():
        p = f"interactions/{did}"
        if o.get("drugId") not in drugs:
            err(f"{p}: drugId '{o.get('drugId')}' non esiste")
        for it in o.get("items") or []:
            if it.get("severity") not in SEVERITA:
                err(f"{p}: gravità sconosciuta '{it.get('severity')}'")
            if not it.get("agent"):
                err(f"{p}: una voce non ha il campo 'agent' (non verrebbe mai rilevata)")
            elif len(it["agent"]) < 4:
                avv(f"{p}: campo 'agent' molto corto ('{it['agent']}'): rischio di falsi positivi")
            if not it.get("effect"):
                avv(f"{p}: voce '{it.get('agent')}' senza descrizione dell'effetto")

    # ---- regolatorio ----
    for did, o in regulatory.items():
        if o.get("drugId") not in drugs:
            err(f"regulatory/{did}: drugId '{o.get('drugId')}' non esiste")

    # ---- raccomandazioni della Mappa terapeutica ----
    n_racc = 0
    for slug, o in recommendations.items():
        p = f"recommendations/{slug}"
        meta = o.get("meta") or {}
        if meta.get("id") != slug or o.get("pathology") != slug:
            err(f"{p}: meta.id e pathology devono coincidere con il nome del file")
        if stato(o) not in STATI:
            err(f"{p}: stato editoriale sconosciuto '{stato(o)}'")
        if not (meta.get("sources") or []):
            err(f"{p}: nessuna fonte in meta.sources")
        visti = set()
        for g in o.get("groups") or []:
            if not g.get("id") or not g.get("label"):
                err(f"{p}: gruppo senza id o etichetta")
            if g.get("id") in visti:
                err(f"{p}: id di gruppo duplicato '{g.get('id')}'")
            visti.add(g.get("id"))
            ids = set()
            for it in g.get("items") or []:
                n_racc += 1
                q = f"{p}/{g.get('id')}/{it.get('id')}"
                if not it.get("id") or it["id"] in ids:
                    err(f"{q}: id mancante o duplicato nel gruppo")
                ids.add(it.get("id"))
                if not it.get("text"):
                    err(f"{q}: testo mancante")
                if it.get("cor") not in CLASSI_RACC:
                    err(f"{q}: classe di raccomandazione sconosciuta '{it.get('cor')}'")
                if it.get("loe") not in LIVELLI:
                    err(f"{q}: livello di evidenza sconosciuto '{it.get('loe')}'")
                if it.get("loe") and not it.get("cor"):
                    err(f"{q}: livello di evidenza senza classe")
                for did in it.get("drugIds") or []:
                    if did not in drugs:
                        err(f"{q}: drugId '{did}' non esiste")
                if it.get("cor") is None:
                    avv(f"{q}: classe di raccomandazione non indicata")

    for key, o in rules.items():
        for r in o.get("rules") or []:
            q = f"rules/{key}/{r.get('id')}"
            if r.get("severity") not in SEVERITA:
                err(f"{q}: gravità sconosciuta '{r.get('severity')}'")
            if not r.get("message") or not r.get("source"):
                err(f"{q}: messaggio o fonte mancante")
            if len(r.get("all") or []) < 2:
                err(f"{q}: una regola richiede almeno due condizioni")
            for m in r.get("all") or []:
                for cid in m.get("classes") or []:
                    if cid not in classes:
                        err(f"{q}: classe '{cid}' non esiste")
                for did in m.get("drugs") or []:
                    if did not in drugs:
                        err(f"{q}: farmaco '{did}' non esiste")

    # ---- copertura ----
    popolati = [k for k, v in drugs.items() if stato(v) != "placeholder"]
    for did in popolati:
        if did not in interactions:
            avv(f"drugs/{did}: scheda popolata senza file di interazioni")
        if did not in regulatory:
            avv(f"drugs/{did}: scheda popolata senza record regolatorio")

    conteggi = {
        "farmaci": len(drugs),
        "farmaci_popolati": len(popolati),
        "approvati": sum(1 for v in drugs.values() if stato(v) == "clinician-approved"),
        "placeholder": sum(1 for v in drugs.values() if stato(v) == "placeholder"),
        "classi": len(classes),
        "classi_popolate": sum(1 for v in classes.values() if stato(v) != "placeholder"),
        "posologie": len(dosing),
        "interazioni": len(interactions),
        "regolatorio": len(regulatory),
        "patologie con classi": len(recommendations),
        "raccomandazioni": n_racc,
        "regole associazioni": sum(len(o.get("rules") or []) for o in rules.values()),
        "errori": len(errori),
        "avvisi": len(avvisi),
    }

    if args.as_json:
        print(json.dumps({"conteggi": conteggi, "errori": errori, "avvisi": avvisi},
                         ensure_ascii=False, indent=2))
        return 1 if errori else 0

    print("CardioTherapy Atlas — validazione dei contenuti\n")
    for k, v in conteggi.items():
        if k not in ("errori", "avvisi"):
            print(f"  {k.replace('_', ' '):<20} {v}")
    print()
    if errori:
        print(f"ERRORI ({len(errori)}):")
        for e in errori:
            print("  ✗ " + e)
        print()
    if avvisi:
        if args.verbose:
            print(f"AVVISI ({len(avvisi)}):")
            for a in avvisi:
                print("  · " + a)
        else:
            print(f"AVVISI: {len(avvisi)} (usa --verbose per l'elenco)")
        print()
    print("Esito: " + ("FALLITA" if errori else "OK"))
    return 1 if errori else 0


if __name__ == "__main__":
    sys.exit(main())
