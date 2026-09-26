#!/usr/bin/env python3
"""Hand-written references to Known Issues that the audit created or renumbered stay correct (idempotent).

    issue_refs.py apply     # rewrite every <!--issue:KEY-->...<!--/issue-->  in the public pages to the entry's current id and link
    issue_refs.py check     # no writes; exit 1 if a marker is stale or unresolvable, or a page cites such an entry without a marker

The stable ids of the earlier audits (CNA-BUG-001 ... 249, CNA-GAP-001 ... 062, ...) never change.  The ids the independent audit allocated afterwards
(the entries it added, and the new ids of the entries it reclassified into another class) are assigned in order, so a later reclassification can shift them.
A page that names one of those entries by its number would then point at a different defect without any validator noticing.  The reference is therefore written

    <!--issue:KEY--><a href="../../known-issues/bugs/cna-bug-nnn.html">CNA-BUG-nnn</a><!--/issue-->

where KEY is the entry's identity that does not move: the temporary id NEW-AUDIT-nn of an entry the audit added, or the earlier id of an entry it reclassified or
folded (CNA-BUG-100 for what is now a functional gap).  KEY is resolved from audit/data/bible/issues/dispositions.json; the text between the markers is regenerated
from scratch on every run (the id and a link relative to the page), exactly like the marked backlink blocks of backlinks.py.  A link or a plain mention of such an
entry outside a marker is an error, so an unprotected reference cannot be added by accident.  Known Issues pages are generated and resolve the same kind of
reference from {{issue:KEY}} in the entry text (scripts/known_issues.py), so they are not scanned here.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DISP = ROOT / "audit" / "data" / "bible" / "issues" / "dispositions.json"
PUBLIC = ROOT / "data" / "known-issues.json"
MARK = re.compile(r"<!--issue:([A-Za-z0-9-]+)-->(.*?)<!--/issue-->", re.S)
ID = r"CNA-(?:BUG|GAP|PLAT|VGAP)-\d{3}"
LINK = re.compile(r'<a\b[^>]*href="[^"]*known-issues/(?:bugs|gaps|limitations|verification-gaps)/(cna-[a-z]+-\d{3})\.html[^"]*"[^>]*>.*?</a>', re.S)
SKIP_DIRS = ("audit/", "build-probe/", "known-issues/", ".git/")


def load() -> tuple[dict, dict[str, str], set[str]]:
    trail = json.loads(DISP.read_text(encoding="utf-8")).get("adversarial_audit", {})
    detail = {i["id"]: i["detail"] for i in json.loads(PUBLIC.read_text(encoding="utf-8"))["issues"]}
    shifting = set(trail.get("added", {}).values()) | set(trail.get("reclassified", {}).values())
    return trail, detail, shifting


def resolve(key: str, trail: dict, detail: dict[str, str]) -> str | None:
    for group in ("added", "reclassified", "folded"):
        if key in trail.get(group, {}):
            return trail[group][key]
    return key if key in detail else None


def pages() -> list[Path]:
    out = []
    for p in sorted(ROOT.glob("**/*.html")):
        r = p.relative_to(ROOT).as_posix()
        if not r.startswith(SKIP_DIRS):
            out.append(p)
    return out


def rel(from_page: str, to: str) -> str:
    return os.path.relpath(to, os.path.dirname(from_page) or ".").replace(os.sep, "/")


def process(write: bool) -> tuple[int, list[str], list[str]]:
    trail, detail, shifting = load()
    refs = 0
    changed: list[str] = []
    errors: list[str] = []
    for p in pages():
        r = p.relative_to(ROOT).as_posix()
        old = p.read_text(encoding="utf-8")

        def fix(m: re.Match) -> str:
            nonlocal refs
            refs += 1
            final = resolve(m.group(1), trail, detail)
            if final is None or final not in detail:
                errors.append(f"{r}: <!--issue:{m.group(1)}--> names no published entry (retired, or a typo)")
                return m.group(0)
            return f'<!--issue:{m.group(1)}--><a href="{rel(r, detail[final])}">{final}</a><!--/issue-->'

        new = MARK.sub(fix, old)
        # outside a marker, and outside the generated blocks and pagers: no link to and no mention of an entry the audit created or renumbered
        rest = MARK.sub(" ", new)
        rest = re.sub(r"<!--p3:(?:issue|deep)-links-->.*?<!--/p3:(?:issue|deep)-links-->", " ", rest, flags=re.S)
        rest = re.sub(r'<nav class="docs-pagination".*?</nav>|<a class="(?:dev|deep)-pager-(?:next|prev)".*?</a>', " ", rest, flags=re.S)
        for m in LINK.finditer(rest):
            if m.group(1).upper() in shifting:
                errors.append(f"{r}: a link to {m.group(1).upper()} is not wrapped in <!--issue:KEY-->...<!--/issue-->; that id was allocated by the audit and can be renumbered")
        text = re.sub(r"<[^>]+>", " ", LINK.sub(" ", rest))
        for m in re.finditer(ID, text):
            if m.group(0) in shifting:
                errors.append(f"{r}: the mention of {m.group(0)} is not wrapped in <!--issue:KEY-->...<!--/issue-->; that id was allocated by the audit and can be renumbered")
        if new != old:
            changed.append(r)
            if write:
                p.write_text(new, encoding="utf-8")
    return refs, changed, sorted(set(errors))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["apply", "check"])
    args = ap.parse_args()
    refs, changed, errors = process(args.cmd == "apply")
    for e in errors:
        print("ERROR", e)
    if args.cmd == "check":
        for r in changed:
            print(f"ERROR {r}: an issue reference is stale (an id the audit allocated moved); run scripts/issue_refs.py apply")
    print(f"issue references: {refs} marked; pages {'that would change' if args.cmd == 'check' else 'rewritten'}: {len(changed)}; errors {len(errors)}")
    return 1 if errors or (args.cmd == "check" and changed) else 0


if __name__ == "__main__":
    sys.exit(main())
