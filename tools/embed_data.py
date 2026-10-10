#!/usr/bin/env python3
"""
Incorpora in index.html le cartelle di data/ che l'app legge dall'oggetto DATA ma che non
richiedono il generatore completo: oggi data/recommendations/ e data/rules/ (Mappa terapeutica) e data/infusions/ (UTIC).

Riscrive solo le chiavi DATA.recommendations, DATA.rules e DATA.infusions; il resto di DATA resta identico.

Uso:
    python3 tools/embed_data.py          # aggiorna index.html
    python3 tools/embed_data.py --check  # verifica soltanto (esce con 1 se servirebbe aggiornare)
"""
from __future__ import annotations
import json, re, sys, argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "index.html"
DATA = ROOT / "data"
PATTERN = re.compile(r"(const DATA = )(\{.*?\})(;\nlet query)", re.S)


def carica(cartella: str) -> dict:
    d = DATA / cartella
    return {f.stem: json.loads(f.read_text(encoding="utf-8")) for f in sorted(d.glob("*.json"))}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    h = HTML.read_text(encoding="utf-8")
    m = PATTERN.search(h)
    if not m:
        sys.exit("ERRORE: blocco DATA non trovato in index.html")
    d = json.loads(m.group(2))

    recs, rules, inf = carica("recommendations"), carica("rules"), carica("infusions")
    slugs = {p["slug"] for p in d.get("pathologies", [])}
    ignote = sorted(set(recs) - slugs)
    if ignote:
        sys.exit("ERRORE: raccomandazioni per patologie inesistenti nell'app: " + ", ".join(ignote))

    if d.get("recommendations") == recs and d.get("rules") == rules and d.get("infusions") == inf:
        print("DATA già allineato con data/recommendations, data/rules e data/infusions")
        return 0
    if args.check:
        print("DATA non allineato: eseguire python3 tools/embed_data.py")
        return 1

    d["recommendations"], d["rules"], d["infusions"] = recs, rules, inf
    nuovo = json.dumps(d, ensure_ascii=False)
    HTML.write_text(h[:m.start(2)] + nuovo + h[m.end(2):], encoding="utf-8")
    print(f"index.html aggiornato: {len(recs)} patologie con classi, "
          f"{sum(len(o.get('rules', [])) for o in rules.values())} regole, {len(inf)} infusioni")
    return 0


if __name__ == "__main__":
    sys.exit(main())
