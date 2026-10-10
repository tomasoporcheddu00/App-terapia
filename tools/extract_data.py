#!/usr/bin/env python3
"""
Estrae l'oggetto DATA incorporato in index.html e ne verifica l'allineamento con data/.

Serve finché il generatore non viene ricostruito: i contenuti esistono in due forme (i JSON
revisionabili in data/ e l'oggetto DATA dentro l'applicazione) e devono restare identici.

Uso:
    python3 tools/extract_data.py            # confronta e segnala le divergenze
    python3 tools/extract_data.py --dump DIR # scrive i JSON estratti dall'HTML in DIR
"""
from __future__ import annotations
import json, re, sys, argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "index.html"
DATA = ROOT / "data"


def estrai() -> dict:
    h = HTML.read_text(encoding="utf-8")
    m = re.search(r"const DATA = (\{.*?\});\nlet query", h, re.S)
    if not m:
        sys.exit("ERRORE: blocco DATA non trovato in index.html")
    return json.loads(m.group(1))


def carica(cartella: str) -> dict[str, dict]:
    d = DATA / cartella
    return {f.stem: json.loads(f.read_text(encoding="utf-8")) for f in sorted(d.glob("*.json"))} if d.is_dir() else {}


def confronta(nome: str, da_html: dict, da_file: dict, chiavi: list[str]) -> list[str]:
    """Confronta solo i campi clinicamente rilevanti: l'HTML può contenere campi derivati."""
    diff = []
    soli_html = set(da_html) - set(da_file)
    soli_file = set(da_file) - set(da_html)
    for k in sorted(soli_html):
        diff.append(f"{nome}: '{k}' presente nell'app ma non in data/")
    for k in sorted(soli_file):
        diff.append(f"{nome}: '{k}' presente in data/ ma non nell'app")
    for k in sorted(set(da_html) & set(da_file)):
        a, b = da_html[k], da_file[k]
        for c in chiavi:
            va = a.get(c) if isinstance(a, dict) else None
            vb = b.get(c) if isinstance(b, dict) else None
            if json.dumps(va, sort_keys=True, ensure_ascii=False) != json.dumps(vb, sort_keys=True, ensure_ascii=False):
                diff.append(f"{nome}/{k}: campo '{c}' diverso fra app e data/")
    return diff


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dump", metavar="DIR", help="scrive in DIR i JSON estratti dall'HTML")
    args = ap.parse_args()

    d = estrai()
    drugs_html = {x["meta"]["id"]: x for x in d.get("drugs", [])}
    classes_html = d.get("classes", {}) or {}
    ix_html = d.get("interactions", {}) or {}
    reg_html = d.get("regulatory", {}) or {}

    if args.dump:
        out = Path(args.dump)
        for sub, obj in (("drugs", drugs_html), ("classes", classes_html),
                         ("interactions", ix_html), ("regulatory", reg_html)):
            (out / sub).mkdir(parents=True, exist_ok=True)
            for k, v in obj.items():
                (out / sub / f"{k}.json").write_text(
                    json.dumps(v, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"estratti in {out}: {len(drugs_html)} farmaci, {len(classes_html)} classi, "
              f"{len(ix_html)} interazioni, {len(reg_html)} record regolatori")
        return 0

    diff: list[str] = []
    diff += confronta("drugs", drugs_html, carica("drugs"), ["clinical", "name", "identity", "deep"])
    diff += confronta("classes", classes_html, carica("classes"), ["name", "memberDrugIds", "mechanismSummary"])
    diff += confronta("interactions", ix_html, carica("interactions"), ["items"])
    diff += confronta("regulatory", reg_html, carica("regulatory"), ["reimbursementClass", "supplyRegime", "marketed"])
    diff += confronta("recommendations", d.get("recommendations", {}) or {}, carica("recommendations"), ["meta", "groups"])
    diff += confronta("rules", d.get("rules", {}) or {}, carica("rules"), ["rules"])

    print(f"App: {len(drugs_html)} farmaci · {len(classes_html)} classi · "
          f"{len(d.get('pathologies', []))} patologie")
    if not diff:
        print("Allineamento app ↔ data/: OK")
        return 0
    print(f"\nDIVERGENZE ({len(diff)}):")
    for x in diff[:60]:
        print("  ✗ " + x)
    if len(diff) > 60:
        print(f"  … e altre {len(diff) - 60}")
    print("\nRicorda: una modifica ai contenuti va riportata sia in data/ sia nell'oggetto DATA "
          "dentro index.html (per recommendations/ e rules/: python3 tools/embed_data.py).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
