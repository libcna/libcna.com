#!/usr/bin/env python3
"""List, for a pin move, which pages with an evidence callout must be re-read and which can carry their evidence forward.

    evidence_worklist.py --old <old cnahead> [--new <sha>] [--out FILE] [--topics REGEX-FILE]

The update procedure (development/handbook/update-libcna-com.html, step 3) says: intersect the CNA paths each page cites with
`git diff --name-only OLD NEW`; a file that is byte-identical between the two revisions cannot invalidate a claim that rests on it
alone. This script does that intersection for every page that carries a `dev-evidence` callout (Deep Dives, Development and the
generated Known Issues pages; the latter move only through scripts/known_issues.py) and adds two refinements used for the
3b43bd86 update:

  * a changed file whose diff touches only comment lines is reported apart (`comment_only_changed`): `//`, `/* */` and doc-comment
    lines in C and C++, `#` lines in CMake, Python, shell, YAML and TOML. A public header's doc comment is its documented contract,
    so a `.h`/`.hpp` change counts as a real change even when only comments moved. Markdown and JSON changes always count.
  * the page text is searched for the interval's topics (an optional file with one regular expression per line; without it no
    topic is searched), because a page can describe a changed subject without linking the file that changed.

A row is `carry` when nothing it cites changed (comment-only changes outside headers excepted) and no topic matched, otherwise
`review`. `carry` is a mechanical judgement about the cited evidence, not a re-verification of the page. Reads CNA Git objects only
(`../cna` or $CNA_REPO); writes only --out (default: standard output).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
CNA = Path(os.environ.get("CNA_REPO") or ROOT.parent / "cna")
SKIP = {"audit", "scripts", "build-probe", ".git"}
CALLOUT = re.compile(r'<div class="callout[^"]*dev-evidence"[^>]*>(.*?)</div>', re.S)
READ_AT = re.compile(r"checked by reading the CNA source at commit <code>(\w+)</code>")
LINK = re.compile(r'github\.com/libcna/cna/blob/[0-9a-f]{40}/([^"#?\s<]*)')
PROSE_PATH = re.compile(r"\b((?:modules|cmake|docs|tools|scripts|plans|tests|third_party|misc)/[A-Za-z0-9_./-]+\.[A-Za-z0-9]+)")
HASH_COMMENT = (".cmake", ".py", ".sh", "CMakeLists.txt", ".yml", ".yaml", ".toml")


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(CNA), *args], check=True, capture_output=True, text=True).stdout


def change_kind(old: str, new: str, path: str) -> str:
    """code, doc, comment-only or mode-only, from the -U0 diff of one path."""
    diff = git("diff", "-U0", old, new, "--", path)
    lines = [ln[1:] for ln in diff.splitlines() if ln[:1] in "+-" and not ln.startswith(("+++", "---"))]
    if not lines:
        return "mode-only"
    if path.endswith((".md", ".txt", ".json")) or path.endswith((".h", ".hpp")):
        return "doc" if path.endswith((".md", ".txt", ".json")) else (
            "code" if not all(re.match(r"^\s*(//|\*|/\*|\*/|$)", ln) for ln in lines) else "doc")
    comment = r"^\s*(//|\*|/\*|\*/|$)" + (r"|^\s*#" if path.endswith(HASH_COMMENT) else "")
    return "comment-only" if all(re.match(comment, ln) for ln in lines) else "code"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--old", required=True, help="the previous cnahead commit")
    ap.add_argument("--new", default=(ROOT / "cnahead").read_text(encoding="utf-8").strip())
    ap.add_argument("--out")
    ap.add_argument("--topics", help="file with one regular expression per line (blank lines and # comments ignored)")
    args = ap.parse_args()
    changed = set(git("diff", "--name-only", args.old, args.new).splitlines())
    topic_rx = None
    if args.topics:
        pats = [ln.strip() for ln in Path(args.topics).read_text(encoding="utf-8").splitlines()
                if ln.strip() and not ln.lstrip().startswith("#")]
        topic_rx = re.compile("|".join(f"(?:{p})" for p in pats)) if pats else None
    kinds: dict[str, str] = {}
    rows = []
    for page in sorted(ROOT.rglob("*.html")):
        rel = page.relative_to(ROOT)
        if SKIP & set(rel.parts):
            continue
        raw = page.read_text(encoding="utf-8")
        m = CALLOUT.search(raw)
        if not m:
            continue
        read = READ_AT.search(m.group(1))
        cited = {unquote(x).rstrip("/") for x in LINK.findall(raw)}
        cited |= set(PROSE_PATH.findall(re.sub(r'href="[^"]*"', "", raw)))
        hits = sorted(cited & changed)
        for f in hits:
            kinds.setdefault(f, change_kind(args.old, args.new, f))
        real = [f for f in hits if kinds[f] in ("code", "doc")]
        text = re.sub(r"<[^>]+>", " ", re.sub(r"<footer.*?</footer>", "", raw, flags=re.S))
        topics = sorted({t.group(0) for t in topic_rx.finditer(text)}) if topic_rx else []
        rows.append({"page": rel.as_posix(),
                     "kind": "pinned" if "at the pinned commit" in m.group(1) else "stated",
                     "evidence_sha": read.group(1) if read else None,
                     "status": "carry" if not real and not topics else "review",
                     "changed_files": real,
                     "comment_only_changed": [f for f in hits if kinds[f] not in ("code", "doc")],
                     "topics": topics})
    out = json.dumps(rows, indent=1) + "\n"
    if args.out:
        Path(args.out).write_text(out, encoding="utf-8")
    else:
        sys.stdout.write(out)
    carry = sum(1 for r in rows if r["status"] == "carry")
    print(f"evidence worklist: {len(rows)} pages with an evidence callout, {carry} carry, {len(rows) - carry} review "
          f"({len(changed)} paths changed {args.old[:8]}..{args.new[:8]})", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
