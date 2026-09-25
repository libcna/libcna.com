#!/usr/bin/env python3
"""Keep the global header entries for the Development, Deep Dives and Known Issues areas in sync (idempotent).

Phase 2 added exactly one header entry ("Development") after "Documentation"; Phase 3 adds one entry each for the Deep Dives and
Known Issues areas directly after it.  The areas' own pages are reached through their hubs and local sidebars, never through the
global header.  Re-running this script adds whatever is missing and changes nothing else.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENTRIES = [("development/index.html", "Development", r'documentation\.html" class="nav-link(?: active)?">Documentation</a>'),
           ("deep-dives/index.html", "Deep Dives", r'development/index\.html" class="nav-link(?: active)?">Development</a>')]


FOOT = re.compile(r'<li><a href="(?P<x>(?:\.\./)*(?:docs/)?)faq\.html">FAQ</a></li></ul>')


ML_FOOT = re.compile(r'(?P<ind>[ \t]*)<li><a href="(?P<x>(?:\.\./)*(?:docs/)?)faq\.html">FAQ</a></li>\n')


def patch_footer(text: str) -> str:
    """Add Deep Dives and Known Issues to the footer's Docs column (idempotent)."""
    if "known-issues/index.html" in text.split("<footer", 1)[-1]:
        return text

    def repl(m: re.Match) -> str:
        x = m.group("x")
        root = x[:-5] if x.endswith("docs/") else x + "../"
        return (m.group(0)[:-len("</ul>")] + f'<li><a href="{root}deep-dives/index.html">Deep Dives</a></li>'
                f'<li><a href="{root}known-issues/index.html">Known Issues</a></li></ul>')
    if FOOT.search(text):
        return FOOT.sub(repl, text, count=1)
    # multi-line footers of docs/ and tutorial pages
    head, sep, foot = text.rpartition("<footer")
    m = ML_FOOT.search(foot)
    if not sep or not m:
        return text
    x = m.group("x")
    root = x[:-5] if x.endswith("docs/") else x + "../"
    ind = m.group("ind")
    add = (f'{ind}<li><a href="{root}deep-dives/index.html">Deep Dives</a></li>\n'
           f'{ind}<li><a href="{root}known-issues/index.html">Known Issues</a></li>\n')
    foot = foot[:m.end()] + add + foot[m.end():]
    return head + sep + foot


def patch(text: str) -> str:
    for target, label, anchor in ENTRIES:
        if f'{target}" class="nav-link' in text:
            continue
        pat = re.compile(r'(?P<indent>^[ \t]*)?<a href="(?P<pre>(?:\.\./)*)' + anchor + r'(?P<nl>\n)?', re.M)

        def repl(m: re.Match, target=target, label=label) -> str:
            indent = m.group("indent") or ""
            link = f'<a href="{m.group("pre")}{target}" class="nav-link">{label}</a>'
            original = m.group(0)
            if m.group("nl") and indent:
                return original + indent + link + "\n"
            return original + link

        text, _n = pat.subn(repl, text, count=1)
    return patch_footer(text)


def main() -> int:
    changed = missing = 0
    for path in sorted(ROOT.rglob("*.html")):
        if {"audit", "scripts", "build-probe", ".git"} & set(path.relative_to(ROOT).parts):
            continue
        text = path.read_text(encoding="utf-8")
        new = patch(text)
        if new == text:
            if 'development/index.html" class="nav-link' not in text:
                missing += 1
                print("no Documentation nav link:", path.relative_to(ROOT))
            continue
        path.write_text(new, encoding="utf-8")
        changed += 1
    print(f"nav patched on {changed} page(s); {missing} without a Documentation nav link")
    return 0


if __name__ == "__main__":
    sys.exit(main())
