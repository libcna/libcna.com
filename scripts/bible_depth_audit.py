#!/usr/bin/env python3
"""Depth audit of the large Bible units (Phase 3, requirement 17): source words vs the substance that now exists on the site.

    bible_depth_audit.py            # write audit/bible-depth-audit-phase3.md

For every canonical LaTeX unit with >= 2,500 prose words: concepts recorded, disposition mix, the distinct destination pages (deep dives, guides,
internals, known issues) with their words, and a ratio flag.  A low ratio is a warning signal, not proof of loss: the record's dispositions
(PRESERVED / HISTORICAL ONLY / TARGET CONTRADICTED ...) must explain it.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bible_ledger as L  # noqa: E402

ROOT = L.ROOT


def main() -> int:
    doc = L.load_units()
    recs = L.load_records()
    rows = []
    for u in doc["units"]:
        if u["kind"] == "figure" or u["prose_words"] < 2500:
            continue
        r = recs.get(u["id"])
        if not r:
            continue
        cs = r.get("concepts") or []
        disp = Counter(c["disposition"] for c in cs)
        pages = []
        for c in cs:
            for d in c.get("destinations") or []:
                b = L.split_dest(d)[0]
                if b not in pages:
                    pages.append(b)
        dest_words = sum(L.page_words(p) for p in pages if p.startswith("deep-dives/") or p.startswith("known-issues/"))
        all_words = sum(L.page_words(p) for p in pages)
        ratio = dest_words / u["prose_words"]
        rows.append((u["id"], u["prose_words"], len(cs), disp, len(pages), dest_words, all_words, ratio))
    L_ = ["# Phase-3 depth audit — large Bible units", "",
          "Units with >= 2,500 prose words. *Deep-dive words* = article words of the distinct `deep-dives/**` and `known-issues/**` destination pages of the unit's concepts "
          "(pages are shared between units, so the column is an upper bound of what a unit alone contributes); *all destination words* also counts guide and Development pages. "
          "A ratio below 0.8 is a warning that must be explained by the dispositions (PRESERVED on existing pages, HISTORICAL ONLY, TARGET CONTRADICTED …).", "",
          "| Unit | Bible words | Concepts | NEW PAGE | PRESERVED | HISTORICAL / OBSOLETE / REMOVED | Fixed / contradicted | Destination pages | Deep-dive words | All destination words | Ratio | Flag |",
          "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|"]
    for uid, bw, n, disp, npg, dw, aw, ratio in sorted(rows, key=lambda r: -r[1]):
        hist = disp.get("HISTORICAL ONLY", 0) + disp.get("OBSOLETE", 0) + disp.get("REMOVED FUNCTIONALITY", 0)
        fx = disp.get("FIXED BUG", 0) + disp.get("TARGET CONTRADICTED", 0)
        flag = "" if ratio >= 0.8 else ("explained: mostly PRESERVED elsewhere" if disp.get("PRESERVED", 0) + disp.get("DUPLICATE", 0) >= n * 0.5 else "REVIEW")
        L_.append(f"| `{uid}` | {bw} | {n} | {disp.get('NEW PAGE', 0)} | {disp.get('PRESERVED', 0)} | {hist} | {fx} | {npg} | {dw} | {aw} | {ratio:.2f} | {flag} |")
    (ROOT / "audit" / "bible-depth-audit-phase3.md").write_text("\n".join(L_) + "\n", encoding="utf-8")
    review = [r for r in rows if r[7] < 0.8]
    print(f"{len(rows)} large units; ratio < 0.8: {len(review)}")
    for r in review:
        print("  ", r[0], f"{r[7]:.2f}", dict(r[3]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
