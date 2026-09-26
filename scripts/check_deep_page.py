#!/usr/bin/env python3
"""Per-page checks for Deep Dives and Known Issues pages while they are being written.

    check_deep_page.py deep-dives/graphics/spritebatch-sorting.html [more pages ...]
    check_deep_page.py --all                       # every declared page that exists on disk

Same checks as scripts/check_dev_page.py (strict HTML5, duplicate ids, JSON-LD, local links and #fragments, TARGET-pinned CNA source
links that exist at TARGET, retired renderer identities, alpha.1 only as history, first-person voice) plus the Phase-3 rules:

  * no book vocabulary: the pages are a knowledge graph, not a converted book ("Chapter 12", "the Bible", "this book", "Part IV",
    "\\S3.2" section marks, LaTeX macros, the Bible's file names, the Bible's pin d6e9ff05, "cnabugs");
  * exactly one <h1>; every <h2>/<h3> in the article has an id; heading levels never skip; every <table> has <th scope>;
    every <img> has non-empty alt; every <pre><code> block declares a language class or is a plain diagram;
  * the evidence callout exists and names the basis; meta description present and single-sentence sized.
Exit status 1 when any page has an ERROR.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_dev_page as CD  # noqa: E402
import check_retired_renderers as R  # noqa: E402
import deep_manifest as DM  # noqa: E402
import site_dev  # noqa: E402

ROOT = CD.ROOT

BOOK_VOCAB = re.compile(
    r"(\bthe (?:CNA )?Bible\b|\bthis book\b|\bthe book\b|\bChapters? \d+\b|\bCh\. ?\d+\b|\bPart [IVX]+\b|\\S ?\d|§ ?\d|\\(?:cnaclass|texttt|ref|cite)\b|"
    r"bible\.libcna|cnabugs|\bd6e9ff05\b|\blatex/book\b|ch\d\d-[a-z-]+\.tex|\bthe manuscript\b|\bthis edition\b|\bsealed edition\b)", re.I)
# check_dev_page.DEV_VOCAB minus the false positive on CNA's own file names that end in "coverage.md"
DEV_VOCAB = re.compile(r"(developer\.libcna\.com|(?<![\w/-])COVERAGE\.md|this manual\b|this handbook\b|this website's pin|"
                       r"Phase 0 overview)", re.I)
HEADING = re.compile(r"<h([1-6])\b([^>]*)>", re.I)


def article(raw: str) -> str:
    m = re.search(r"<article\b.*?</article>", raw, re.S)
    return m.group(0) if m else raw


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2
    if args == ["--all"]:
        args = [p["path"] for p in DM.all_pages() if (ROOT / p["path"]).exists()]
    retired = R.derive(R.BASE_TREE, R.TARGET_TREE)
    strong = sorted(i for i in retired if i not in R.WORDS)
    strong_rx = re.compile(r"(?<![A-Za-z0-9_])(" + "|".join(map(re.escape, strong)) + r")(?![A-Za-z0-9_])", re.I)
    files, dirs = site_dev.target_tree()
    idcache: dict[Path, set[str]] = {}
    declared = {p["path"] for p in DM.all_pages()}
    rc = 0
    for rel in args:
        path = ROOT / rel
        errors: list[str] = []
        warns: list[str] = []
        if not path.exists():
            print(f"{rel}: ERROR page does not exist")
            rc = 1
            continue
        raw = path.read_text(encoding="utf-8")
        p = CD.P()
        p.feed(raw)
        art_raw = article(raw)
        pa = CD.P()
        pa.feed(art_raw)
        try:
            import html5lib
            parser = html5lib.HTMLParser(strict=False, namespaceHTMLElements=False)
            parser.parse(raw)
            for pos, code, det in parser.errors:
                errors.append(f"HTML5 {pos[0]}:{pos[1]} {code} {det}")
        except ImportError:
            warns.append("html5lib unavailable; strict parse skipped")
        dups = sorted({i for i in p.ids if p.ids.count(i) > 1})
        if dups:
            errors.append("duplicate ids: " + ", ".join(dups))
        for i, blob in enumerate(p.ld):
            try:
                json.loads(blob)
            except Exception as exc:  # noqa: BLE001
                errors.append(f"JSON-LD block {i}: {exc}")
        for href in pa.links:
            u = urlparse(href)
            if u.scheme in ("http", "https"):
                m = re.match(r"https://github\.com/libcna/cna/(blob|tree)/([^/]+)/(.+)", href)
                if m:
                    rev, sp = m.group(2), unquote(m.group(3).split("#", 1)[0]).rstrip("/")
                    if rev != site_dev.TARGET:
                        errors.append(f"CNA link not pinned to TARGET: {href}")
                    elif sp not in files and sp not in dirs:
                        errors.append(f"CNA source path absent at TARGET: {sp}")
                continue
            if href.startswith(("mailto:", "tel:", "javascript:")):
                continue
            tgt_rel = unquote(u.path)
            tgt = (path.parent / tgt_rel).resolve() if tgt_rel else path.resolve()
            if not tgt.exists():
                try:
                    site_rel = tgt.relative_to(ROOT.resolve()).as_posix()
                except ValueError:
                    site_rel = ""
                if site_rel in declared or site_rel in DM.page_index():
                    warns.append(f"PENDING (declared, not built yet): {href}")
                else:
                    errors.append(f"broken local link: {href}")
                continue
            if u.fragment and tgt.suffix == ".html" and unquote(u.fragment) not in CD.ids_of(tgt, idcache):
                errors.append(f"missing fragment: {href}")
        text = " ".join(pa.text)
        for m in strong_rx.finditer(text):
            errors.append(f"retired renderer identity in text: {m.group(0)}")
        for m in re.finditer(r"alpha\.1", text):
            ctx = text[max(0, m.start() - 60): m.end() + 40].replace("\n", " ")
            warns.append(f"mentions alpha.1 (must be historical context only): ...{ctx}...")
        for m in CD.FIRST_PERSON.finditer(text):
            errors.append(f"first-person voice: {m.group(0)}")
        is_issue = rel.startswith("known-issues/")  # issue pages quote CNA's own documents (COVERAGE.md, "NOT STARTED", "§3") legitimately
        for m in list(DEV_VOCAB.finditer(text)) + ([] if is_issue else list(CD.DEV_STATUS.finditer(text))):
            if is_issue and "COVERAGE" in m.group(0).upper():
                continue
            errors.append(f"Developer-site vocabulary left in text: {m.group(0)}")
        for m in BOOK_VOCAB.finditer(text):
            if is_issue and m.group(0).startswith(("§", "\\S")):
                continue
            errors.append(f"book vocabulary: {m.group(0)!r} (pages are a knowledge graph, not a converted book)")
        # structure
        heads = [(int(m.group(1)), m.group(2)) for m in HEADING.finditer(art_raw) if "toc-title" not in m.group(2)]
        h1s = [h for h in heads if h[0] == 1]
        if len(h1s) != 1:
            errors.append(f"expected exactly one <h1>, found {len(h1s)}")
        last = 1
        for level, attrs in heads:
            if level > last + 1:
                errors.append(f"heading level jumps from h{last} to h{level}")
            last = level
            if level in (2, 3) and "id=" not in attrs:
                errors.append(f"<h{level}> without an id")
        if re.search(r"<table\b", art_raw) and not re.search(r"<th\b[^>]*scope=", art_raw):
            errors.append("table without <th scope=...>")
        for m in re.finditer(r"<img\b[^>]*>", art_raw):
            if not re.search(r'alt="[^"]+"', m.group(0)):
                errors.append("<img> without alt text")
        for m in re.finditer(r"<pre><code(?![^>]*class=)", art_raw):
            warns.append("code block without a language class (use language-cpp|bash|cmake|json|glsl or a plain <pre class=\"diagram\">)")
            break
        for m in re.finditer(r'<pre class="diagram"', art_raw):
            before = art_raw[:m.start()]
            fig_open = before.rfind("<figure")
            fig_close = before.rfind("</figure>")
            if fig_open < 0 or fig_close > fig_open:
                errors.append('<pre class="diagram"> must sit inside <figure class="diagram-figure"> with a <figcaption> (text alternative)')
                break
            cap = re.search(r"<figcaption[^>]*>(.*?)</figcaption>", art_raw[fig_open:], re.S)
            if not cap or len(re.sub(r"<[^>]+>", "", cap.group(1)).strip()) < 40:
                errors.append("diagram figcaption missing or shorter than 40 characters (it is the text alternative)")
                break
        if "dev-evidence" not in art_raw:
            errors.append("missing evidence callout")
        if not re.search(r'<meta name="description" content="[^"]{30,}"', raw):
            errors.append("missing/short meta description")
        status = "ERROR" if errors else "ok"
        print(f"{rel}: {status} ({len(pa.ids)} ids, {len(pa.links)} links, {len(text.split())} words)")
        for e in errors:
            print("   ERROR", e)
            rc = 1
        for w in warns[:40]:
            print("   warn ", w)
    return rc


if __name__ == "__main__":
    sys.exit(main())
