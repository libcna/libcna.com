#!/usr/bin/env python3
"""Insert the "Development" link after "Documentation" in the global header of every page (idempotent).

Phase 2 adds exactly one header entry for the whole Development area; the area's own pages are reached
through its hubs and local sidebar, never through the global header.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAT = re.compile(
    r'(?P<indent>^[ \t]*)?<a href="(?P<pre>(?:\.\./)*)documentation\.html" class="nav-link(?P<act> active)?">'
    r'Documentation</a>(?P<nl>\n)?', re.M)


def patch(text: str) -> str:
    if 'development/index.html" class="nav-link' in text:
        return text

    def repl(m: re.Match) -> str:
        indent = m.group("indent") or ""
        link = f'<a href="{m.group("pre")}development/index.html" class="nav-link">Development</a>'
        original = m.group(0)
        if m.group("nl") and indent:
            return original + indent + link + "\n"
        return original + link

    new, n = PAT.subn(repl, text, count=1)
    return new if n else text


def main() -> int:
    changed = missing = 0
    for path in sorted(ROOT.rglob("*.html")):
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
