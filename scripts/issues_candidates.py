#!/usr/bin/env python3
"""Assemble the candidate findings for the Known Issues pipeline (Phase 3).

    issues_candidates.py build        # write audit/data/bible/issues/candidates-B1..B6.json (idempotent)
    issues_candidates.py summary      # counts per package and source

Sources, all *candidates* (never confirmed bugs):
  * the Bible defect ledger, cnabugs.md of the Bible working tree (62 stable ids CNA-BUG-001..062) plus its "Documentation defects" items,
  * the 222 bug-like findings the Phase-2 Development pages recorded (audit/data/developer-absorption-units.json -> current_bugs_or_gaps),
  * issue candidates recorded by the chapter work packages (audit/data/bible/issues/WP*.json), mapped to a package by the Bible unit they came from.

Package areas: B1 math/core types · B2 runtime, takeover maps, invariants · B3 content, models, glTF · B4 audio, input, media, video · B5 graphics & renderers
· B6 build, CI, testing, tooling, repository docs · B7 platforms & phone · B8 devices, gamer services, storage, networking · B9 C API, bindings, diagnostics, inspector.
"""

from __future__ import annotations

import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BIBLE = Path(os.environ.get("BIBLE_REPO", ROOT.parent / "bible.libcna.com"))
OUT = ROOT / "audit" / "data" / "bible" / "issues"
UNITS = ROOT / "audit" / "data" / "developer-absorption-units.json"

BIBLE_PKG = {}
for pkg, ids in {
    "B1": [1, 2, 3, 4, 24, 25, 26, 27, 28, 42, 43],
    "B2": [19, 20, 29],
    "B3": [5, 7, 8, 9, 10, 16, 17, 18, 21, 22, 23, 41, 44, 45, 57],
    "B4": [51, 52],
    "B8": [46, 47, 48, 49, 50],
    "B5": [6, 11, 12, 13, 14, 15, 37, 38, 53, 54],
    "B6": [30, 31, 32, 33, 34, 35, 36, 39, 40, 55, 56],
    "B9": [58, 59, 60, 61, 62],
}.items():
    for i in ids:
        BIBLE_PKG[i] = pkg

DOC_ITEMS = [
    ("BIBLE-DOC-1", "CNA `xnb.md` contradicts its own banner",
     "The line 'Status: planning document only. Nothing described here is implemented yet.' sits directly beneath a revision note recording the XNB phases complete (Bible ledger section 8, item 1)."),
    ("BIBLE-DOC-2", "CNA documents still assert that CNA cannot read .xnb",
     "docs/migration-guide.md, docs/xna-4-api-coverage.md, docs/coverage.md ('Content pipeline (.xnb) — 0 %'), docs/README.md and CNA's AUDIT.md were reported still to claim CNA cannot read .xnb (Bible ledger section 8, item 2)."),
    ("BIBLE-DOC-3", "CNA renderer feature matrix self-labels 'Master, up-to-date' while stale",
     "docs/graphics-renderer-feature-matrix.md was reported to self-label 'Master, up-to-date' while carrying rows refuted by the code and covering only a few renderers (Bible ledger section 8, item 3)."),
    ("BIBLE-DOC-4", "CNA's per-file audit tree is keyed on the pre-modularization layout",
     "The audit/ tree of .audit.md files was reported to be keyed on the pre-modularization layout and to list an already-fixed HIGH finding as open (Bible ledger section 8, closing paragraph)."),
]

# Phase-2 destination page -> package
def p2_pkg(dest: str) -> str:
    d = dest
    if any(x in d for x in ("internals/modules/core", "internals/modules/math", "internals/modules/design")):
        return "B1"
    if any(x in d for x in ("internals/platforms/", "internals/modules/phone")):
        return "B7"
    if any(x in d for x in ("internals/runtime/", "architecture/runtime", "takeover/", "invariants", "debugging")):
        return "B2"
    if "internals/content/" in d:
        return "B3"
    if any(x in d for x in ("modules/devices", "modules/gamer-services", "modules/net", "modules/storage")):
        return "B8"
    if any(x in d for x in ("internals/audio/", "internals/input/", "modules/media", "modules/video-ffmpeg")):
        return "B4"
    if "internals/graphics/" in d or "modules/graphics-ext" in d:
        return "B5"
    if any(x in d for x in ("internals/bindings/", "modules/diagnostics", "modules/inspector")):
        return "B9"
    return "B6"


# Bible unit -> package (for candidates recorded by chapter work packages)
def unit_pkg(unit: str) -> str:
    u = unit.lower()
    m = re.match(r"ch(\d+)", u)
    if m:
        n = int(m.group(1))
        if n in (7, 8):
            return "B1"
        if n in (5, 6):
            return "B2"
        if 12 <= n <= 32:
            return "B5"
        if 33 <= n <= 43 and "content-pipeline" in u or 33 <= n <= 37:
            return "B3"
        if 38 <= n <= 43:
            return "B3"
        if 44 <= n <= 46:
            return "B4"
        if 47 <= n <= 52:
            return "B8"
        if 53 <= n <= 60:
            return "B6" if n >= 59 else "B2"
        if 61 <= n <= 67:
            return "B7"
        if n >= 68:
            return "B6"
        return "B6"
    if u.startswith("appendix-"):
        return {"a": "B5", "h": "B3", "i": "B6"}.get(u[9], "B6")
    return "B6"


def parse_bible() -> list[dict]:
    text = (BIBLE / "cnabugs.md").read_text(encoding="utf-8")
    # the TARGET disposition table
    rows = {}
    for m in re.finditer(r"^\| (\d{3}) \| ([^|]*) \| ([^|]*) \| ([^|]*) \| ([^|]*) \|$", text, re.M):
        rows[int(m.group(1))] = {"previous_status": m.group(2).strip(), "bible_target_status": m.group(3).strip("* ").strip(),
                                 "bible_target_evidence": m.group(4).strip(), "bible_action": m.group(5).strip()}
    items = []
    parts = re.split(r"^(?=### CNA-BUG-\d{3} — )", text, flags=re.M)
    for part in parts[1:]:
        head = part.splitlines()[0]
        m = re.match(r"### CNA-BUG-(\d{3}) — (.*)", head)
        n = int(m.group(1))
        body = re.split(r"^## ", part, maxsplit=1, flags=re.M)[0]
        items.append({"cand": f"CNA-BUG-{n:03d}", "source": "bible-cnabugs", "title": m.group(2).strip(), "bible_body": body.strip()[:12000],
                      **rows.get(n, {})})
    return items


def main() -> int:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "build"
    OUT.mkdir(parents=True, exist_ok=True)
    pk: dict[str, list[dict]] = {f"B{i}": [] for i in range(1, 14)}  # B10-B12 = candidates recorded by the chapter/aux packages (never mixed into B1-B9)
    bible = parse_bible()
    for it in bible:
        n = int(it["cand"][-3:])
        pk[BIBLE_PKG[n]].append(it)
    for cid, title, text in DOC_ITEMS:
        pk["B6"].append({"cand": cid, "source": "bible-cnabugs", "title": title, "bible_body": text})
    d = json.loads(UNITS.read_text(encoding="utf-8"))
    n = 0
    for u in d["units"]:
        for b in u.get("current_bugs_or_gaps") or []:
            n += 1
            dest = u.get("destination") or u.get("developer_source") or ""
            pk[p2_pkg(dest)].append({"cand": f"P2-{n:03d}", "source": "phase2", "dest_page": dest, "summary": b.get("summary", ""),
                                     "evidence": b.get("evidence", ""), "note": b.get("note", "")})
    ledger_ids = {c["cand"] for k, v in pk.items() if k != "B10" for c in v if c["cand"].startswith("CNA-BUG-")}
    skipped: list[dict] = []
    for f in sorted(OUT.glob("WP*.json")):
        doc = json.loads(f.read_text(encoding="utf-8"))
        for it in doc.get("items", []):
            it = dict(it)
            it["cand"] = it.pop("id", None) or f"{doc.get('wp', f.stem)}-i???"
            it["source"] = "wp"
            reading = (it.get("target_reading") or "").strip().lower()
            ids = set(re.findall(r"CNA-BUG-\d{3}", f"{it.get('bible_ref', '')} {it.get('ref', '')} {it.get('text', '')}"))
            reason = None
            if it.get("kind") == "not-an-issue":
                reason = "chapter package classified it not-an-issue (documentation gap or architecture decision)"
            elif reading.startswith("absent"):
                reason = "chapter package read it as absent at TARGET (not a current issue; no publication)"
            elif ids and ids <= ledger_ids:
                reason = "covered by the Bible-ledger verification of " + ", ".join(sorted(ids))
            if reason:
                skipped.append({"cand": it["cand"], "kind": it.get("kind"), "reading": reading[:40], "reason": reason, "text": it.get("text", "")[:160]})
            else:
                wp = str(doc.get("wp", f.stem))
                grp = "B10" if wp in {"WP02", "WP03", "WP04", "WP05", "WP06", "WP07", "WP08", "WP09", "WP10", "WP11"} else \
                      "B11" if wp in {"WP12", "WP13", "WP14", "WP15"} else "B13" if wp == "WPB7" else "B12"
                pk[grp].append(it)
    (OUT / "triage-B10.json").write_text(json.dumps({"skipped": skipped}, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    if cmd == "summary":
        for k, v in pk.items():
            print(k, len(v), dict(Counter(x["source"] for x in v)))
        return 0
    for k, v in pk.items():
        (OUT / f"candidates-{k}.json").write_text(json.dumps({"pkg": k, "candidates": v}, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print({k: len(v) for k, v in pk.items()}, "total", sum(len(v) for v in pk.values()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
