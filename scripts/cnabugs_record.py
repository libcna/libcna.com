#!/usr/bin/env python3
"""Write the ledger record of the Bible's defect ledger (aux-cnabugs) from the verified Known Issues dispositions.

    cnabugs_record.py            # audit/data/bible/records/aux-cnabugs.json

Every ### CNA-BUG-NNN heading of cnabugs.md gets one concept whose disposition follows the TARGET verification of that candidate
(audit/data/bible/issues/dispositions.json, written by known_issues.py merge):

    STILL EXISTS / PARTIALLY FIXED -> NEW PAGE     (destination: the published Known Issues page)
    PROVEN FIXED                   -> FIXED BUG    (never published; positive evidence in the note)
    OBSOLETE                       -> OBSOLETE
    NOT A BUG                      -> TARGET CONTRADICTED (the Bible's claim of a defect is not carried over)
    INSUFFICIENT EVIDENCE          -> HISTORICAL ONLY (not asserted; note says why)

The ## headings are method / summary sections: containers are listed under empty_sections, the rest get a disposition.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ISS = ROOT / "audit" / "data" / "bible" / "issues"
UNITS = ROOT / "audit" / "data" / "bible" / "units.json"
OUT = ROOT / "audit" / "data" / "bible" / "records" / "aux-cnabugs.json"
DISPO_MAP = {"PROVEN FIXED": "FIXED BUG", "OBSOLETE": "OBSOLETE", "NOT A BUG": "TARGET CONTRADICTED", "INSUFFICIENT EVIDENCE": "HISTORICAL ONLY"}


def main() -> int:
    units = json.loads(UNITS.read_text(encoding="utf-8"))
    heads = next(a for a in units["aux"] if a["id"] == "aux-cnabugs")["headings"]
    dispo = {d["cand"]: d for d in json.loads((ISS / "dispositions.json").read_text(encoding="utf-8"))["dispositions"]}
    issues = {i["id"]: i for i in json.loads((ROOT / "data" / "known-issues.json").read_text(encoding="utf-8"))["issues"]}
    concepts: list[dict] = []
    empty: list[dict] = []
    n = 0

    def cid() -> str:
        nonlocal n
        n += 1
        return f"CNABUGS-{n:03d}"

    for h in heads:
        title = h["title"]
        m = re.match(r"CNA-BUG-(\d{3}) — (.*)", title)
        if m:
            key = f"CNA-BUG-{m.group(1)}"
            d = dispo.get(key)
            if d is None:
                raise SystemExit(f"no verified disposition for {key}")
            cl = d["classification"]
            ev = d.get("evidence", "")
            base = {"id": cid(), "section": title, "kind": "defect-ledger-entry"}
            if cl in ("STILL EXISTS", "PARTIALLY FIXED"):
                pub = d.get("published_as")
                it = issues[pub]
                concepts.append({**base, "text": f"Bible ledger entry {key} ({m.group(2)}) re-verified at TARGET; it survives as {pub} ({it['class']}, {it['status']}).",
                                 "disposition": "NEW PAGE", "destinations": [it["detail"]], "tokens": [pub],
                                 "target": {"result": "corrected" if cl == "PARTIALLY FIXED" else "confirmed", "evidence": ev[:300]},
                                 "note": f"published as {pub}; classification {cl}"})
            else:
                disp = DISPO_MAP[cl]
                concepts.append({**base, "text": f"Bible ledger entry {key} ({m.group(2)}) re-verified at TARGET: {cl.lower()}; not published as a current defect.",
                                 "disposition": disp, "destinations": [],
                                 "target": {"result": "contradicted" if disp == "TARGET CONTRADICTED" else "corrected", "evidence": ev[:300]},
                                 "note": (ev or cl)[:400] if len(ev) >= 20 else f"{cl}: {ev} (see dispositions.json)"})
            continue
        low = title.lower()
        if re.match(r"\d+\. ", title):
            if title.startswith("8. Documentation defects"):
                for k in ("BIBLE-DOC-1", "BIBLE-DOC-2", "BIBLE-DOC-3", "BIBLE-DOC-4"):
                    d = dispo[k]
                    cl = d["classification"]
                    ev = d.get("evidence", "")
                    base = {"id": cid(), "section": title, "kind": "documentation-defect"}
                    if cl in ("STILL EXISTS", "PARTIALLY FIXED"):
                        it = issues[d["published_as"]]
                        concepts.append({**base, "text": f"Bible 'documentation defects' item {k} re-verified at TARGET; survives as {d['published_as']}.",
                                         "disposition": "NEW PAGE", "destinations": [it["detail"]], "tokens": [d["published_as"]],
                                         "target": {"result": "corrected" if cl == "PARTIALLY FIXED" else "confirmed", "evidence": ev[:300]}, "note": cl})
                    else:
                        concepts.append({**base, "text": f"Bible 'documentation defects' item {k} re-verified at TARGET: {cl.lower()}; not published.",
                                         "disposition": DISPO_MAP[cl], "destinations": [],
                                         "target": {"result": "contradicted" if cl == "NOT A BUG" else "corrected", "evidence": ev[:300]},
                                         "note": (ev or cl)[:400] if len(ev) >= 20 else f"{cl}: {ev}"})
            else:
                empty.append({"heading": title, "reason": "group heading; its entries are recorded individually as CNA-BUG-nnn concepts"})
            continue
        if low.startswith("target active backlog"):
            concepts.append({"id": cid(), "section": title, "kind": "ledger-summary", "text": "The Bible's TARGET-era disposition table (31 active backlog items at its own pin d6e9ff05) is superseded by the re-verification at CNA TARGET recorded per entry in this ledger.",
                             "disposition": "HISTORICAL ONLY", "destinations": [], "target": {"result": "not-applicable", "evidence": ""},
                             "note": "Superseded: every entry was re-verified at TARGET (audit/data/bible/issues/verified-B*.json); the Bible's table was used as a hint only."})
        elif low.startswith("alpha.1 re-triage"):
            concepts.append({"id": cid(), "section": title, "kind": "ledger-summary", "text": "The Bible's alpha.1 re-triage table records each defect's disposition at the alpha.1 tag, a release older than TARGET.",
                             "disposition": "HISTORICAL ONLY", "destinations": [], "target": {"result": "not-applicable", "evidence": ""},
                             "note": "Historical: alpha.1-tag dispositions; the current state of every entry is the TARGET verification above."})
        elif low.startswith("how to read this"):
            concepts.append({"id": cid(), "section": title, "kind": "method", "text": "Findings carry a confidence grade (reproduced / verified by reading / strong / probable) and a severity that is a triage suggestion, not a project priority.",
                             "disposition": "PRESERVED", "destinations": ["known-issues/index.html#method"], "tokens": ["Evidence is stated per entry"],
                             "target": {"result": "not-applicable", "evidence": ""}, "note": ""})
        elif low.startswith("what this list does not cover"):
            concepts.append({"id": cid(), "section": title, "kind": "method", "text": "The original defect findings were derived by reading and were not individually executed; severity judgements would benefit from reproduction.",
                             "disposition": "PRESERVED", "destinations": ["known-issues/index.html#method"], "tokens": ["Evidence is stated per entry"],
                             "target": {"result": "not-applicable", "evidence": ""}, "note": ""})
            concepts.append({"id": cid(), "section": title, "kind": "evidence-scope", "text": "Pixel verification against the XNA oracle exists only for a small subset of renderers, and for most the reference is the renderer's own output.",
                             "disposition": "SUPERSEDED", "destinations": ["deep-dives/verification/oracles-and-engagement.html"], "tokens": ["oracle"],
                             "target": {"result": "corrected", "evidence": "current oracle coverage by renderer is stated on deep-dives/verification/oracles-and-engagement.html"},
                             "note": "the numbers in the Bible are alpha.1-era"})
        else:
            empty.append({"heading": title, "reason": "container heading without a claim of its own"})

    rec = {"unit": "aux-cnabugs", "author": "orchestrator", "done": True, "target_relevance": "partly-stale",
           "actions": ["BUG", "GAP", "HISTORY", "TARGET-CONTRADICTED"],
           "summary": "The Bible's defect ledger (62 CNA-BUG entries plus four documentation-defect items) was re-verified at TARGET by the Known Issues packages B1-B12: survivors are published under their stable ids in known-issues/, fixed or obsolete items are not published, and claims that turned out to be XNA-faithful behaviour are recorded as contradicted.",
           "concepts": concepts, "empty_sections": empty}
    OUT.write_text(json.dumps(rec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"aux-cnabugs: {len(concepts)} concepts, {len(empty)} empty sections -> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
