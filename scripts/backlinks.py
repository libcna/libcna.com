#!/usr/bin/env python3
"""Two-way discoverability for the Deep Dives and Known Issues areas (idempotent).

    backlinks.py apply     # (re)write the marked backlink blocks on existing docs/ and development/ pages
    backlinks.py check     # verify blocks are current (no writes); exit 1 if any page would change
    backlinks.py report    # print the target-page -> deep pages / issues mapping

A deep-dive page names its neighbouring guide / architecture / internals / maintainer / tests / reference pages in its "Related pages" block.
This script reads those blocks from the *built* pages and, on every such existing page, maintains

    <!--p3:deep-links-->  ... "Deep dives on this topic" ...  <!--/p3:deep-links-->

Likewise a Known Issues detail page's related links produce, on the linked pages,

    <!--p3:issue-links--> ... "Known issues in this area" ... <!--/p3:issue-links-->

The blocks are inserted before the page's related-pages / pager / pagination tail and are regenerated from scratch each run, so a page that
gains or loses a deep dive stays correct.  Nothing else on the target page is touched.  Protected root pages are never written (they are
linked by hand); tutorials are eligible only when a deep page explicitly names them.
"""

from __future__ import annotations

import argparse
import html
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import deep_manifest as DM  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PROTECTED = {"index.html", "demos.html", "showcase.html", "videos.html", "features.html", "about.html", "documentation.html", "tutorials.html",
             "architecture.html", "roadmap.html", "network.html", "contact.html"}
TAIL_RX = [re.compile(r'<section class="dev-layers"'), re.compile(r"<!--dev:pager-->"), re.compile(r"<!--deep:pager-->"),
           re.compile(r'<nav class="docs-pagination"'), re.compile(r"</article>")]
DEEP = ("<!--p3:deep-links-->", "<!--/p3:deep-links-->")
ISSUE = ("<!--p3:issue-links-->", "<!--/p3:issue-links-->")


def rel(from_page: str, to: str) -> str:
    return os.path.relpath(to, os.path.dirname(from_page) or ".").replace(os.sep, "/")


def meta_of(path: str) -> tuple[str, str]:
    raw = (ROOT / path).read_text(encoding="utf-8")
    t = re.search(r"<h1>(.*?)</h1>", raw, re.S)
    d = re.search(r'<meta name="description" content="([^"]*)"', raw)
    title = html.unescape(re.sub(r"<[^>]+>", "", t.group(1))).strip() if t else path
    return title, html.unescape(d.group(1)) if d else ""


def related_targets(page: str) -> set[str]:
    """Existing (non-deep, non-issue) site pages this deep page links from its Related pages block."""
    raw = (ROOT / page).read_text(encoding="utf-8")
    m = re.search(r'<section class="dev-layers".*?</section>', raw, re.S)
    if not m:
        return set()
    out = set()
    for href in re.findall(r'href="([^"#]+)', m.group(0)):
        if href.startswith("http"):
            continue
        tgt = os.path.normpath(os.path.join(os.path.dirname(page), href)).replace(os.sep, "/")
        if (ROOT / tgt).is_file() and not tgt.startswith(("deep-dives/", "known-issues/")):
            out.add(tgt)
    return out


def collect() -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    deep: dict[str, list[str]] = {}
    issues: dict[str, list[str]] = {}
    for p in DM.all_pages():
        if p.get("kind") == "hub" or not (ROOT / p["path"]).is_file():
            continue
        target = deep if p["area"] == "deep-dives" else issues
        for t in related_targets(p["path"]):
            target.setdefault(t, []).append(p["path"])
    return deep, issues


def block(page: str, kind: str, sources: list[str]) -> str:
    begin, end = DEEP if kind == "deep" else ISSUE
    items = []
    for s in sorted(sources, key=lambda x: (meta_of(x)[0].lower())):
        title, desc = meta_of(s)
        title = re.sub(r"\s*-\s*CNA (Deep Dives|Known Issues)$", "", title)
        items.append(f'<li><a href="{rel(page, s)}">{html.escape(title)}</a>' + (f" &mdash; {html.escape(desc)}" if desc else "") + "</li>")
    if kind == "deep":
        h, ident, lead = ("Deep dives on this topic", "deep-dives-here",
                          "Long-form pages that explain the exact semantics, invariants and evidence behind this subject.")
    else:
        h, ident, lead = ("Known issues in this area", "known-issues-here",
                          "Current defects, gaps and limitations at this snapshot that touch this subject.")
    return (f'{begin}\n<section class="deep-links" aria-labelledby="{ident}">\n<h2 id="{ident}">{h}</h2>\n<p>{lead}</p>\n'
            f'<ul>\n' + "\n".join(items) + f'\n</ul>\n</section>\n{end}\n')


def strip_block(text: str, marks: tuple[str, str]) -> str:
    return re.sub(re.escape(marks[0]) + r".*?" + re.escape(marks[1]) + r"\n?", "", text, flags=re.S)


def insert_block(text: str, blk: str) -> str:
    art = text.find("<article")
    cands = [m.start() for rx in TAIL_RX if (m := rx.search(text, art))]
    at = min(cands) if cands else text.find("</article>")
    return text[:at] + blk + text[at:]


def process(check_only: bool) -> tuple[int, int]:
    deep, issues = collect()
    pages = set(deep) | set(issues)
    # pages that carry a block but no longer qualify must lose it
    for p in list(ROOT.glob("docs/**/*.html")) + list(ROOT.glob("development/**/*.html")):
        r = p.relative_to(ROOT).as_posix()
        t = p.read_text(encoding="utf-8")
        if (DEEP[0] in t or ISSUE[0] in t) and r not in pages:
            pages.add(r)
    changed = 0
    for r in sorted(pages):
        if r in PROTECTED or not r.startswith(("docs/", "development/")):
            continue
        p = ROOT / r
        old = p.read_text(encoding="utf-8")
        new = strip_block(strip_block(old, DEEP), ISSUE)
        ins = ""
        if r in deep:
            ins += block(r, "deep", deep[r])
        if r in issues:
            ins += block(r, "issues", issues[r])
        if ins:
            new = insert_block(new, ins)
        if new != old:
            changed += 1
            if not check_only:
                p.write_text(new, encoding="utf-8")
    return len(pages), changed


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["apply", "check", "report"])
    args = ap.parse_args()
    if args.cmd == "report":
        deep, issues = collect()
        for t, ps in sorted(deep.items()):
            print(f"{t}: deep <- {', '.join(ps)}")
        for t, ps in sorted(issues.items()):
            print(f"{t}: issues <- {', '.join(ps)}")
        return 0
    n, changed = process(args.cmd == "check")
    print(f"backlink targets: {n}; pages {'that would change' if args.cmd == 'check' else 'rewritten'}: {changed}")
    return 1 if (args.cmd == "check" and changed) else 0


if __name__ == "__main__":
    sys.exit(main())
