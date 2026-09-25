#!/usr/bin/env python3
"""Find where the site already says something — page and nearest heading anchor — before deciding a concept's disposition.

    site_grep.py TOKEN [TOKEN ...]               # case-sensitive substring, all tokens must occur in the same page
    site_grep.py --any TOKEN [TOKEN ...]         # pages containing at least one token; per-token hit counts
    site_grep.py --re 'Exit\\(\\).{0,40}Exiting'  # regular expression over article text (whitespace-collapsed)
    site_grep.py --page docs/game-loop.html --context 200 TOKEN   # show text around the hits on one page
    site_grep.py --area docs|development|deep-dives|known-issues|tutorials TOKEN   # restrict to an area

Only <article> text is searched (site chrome excluded), code blocks included.  For every matching page it prints the word count, the
number of hits and the nearest preceding <h2>/<h3> id for each of the first hits, so a concept can be pointed at page#anchor.
A page that merely *mentions* a token is not coverage: read the hit's context (--context) before marking a concept PRESERVED.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP = {"audit", "scripts", ".git"}


def area_of(rel: str) -> str:
    if rel.startswith("docs/tutorials/"):
        return "tutorials"
    top = rel.split("/")[0]
    return top if "/" in rel else "root"


def load(area: str | None) -> dict[str, tuple[str, list[tuple[int, str]]]]:
    pages: dict[str, tuple[str, list[tuple[int, str]]]] = {}
    for p in sorted(ROOT.rglob("*.html")):
        rel = p.relative_to(ROOT).as_posix()
        if set(rel.split("/")) & SKIP:
            continue
        if area and area_of(rel) != area:
            continue
        raw = p.read_text(encoding="utf-8")
        m = re.search(r"<article\b.*?</article>", raw, re.S) or re.search(r"<main\b.*?</main>", raw, re.S)
        if not m:
            continue
        body = re.sub(r"<(script|style)\b.*?</\1>", " ", m.group(0), flags=re.S)
        # remember heading positions in the *text* stream
        anchors: list[tuple[int, str]] = []
        out: list[str] = []
        pos = 0
        for tok in re.finditer(r"<[^>]+>|[^<]+", body):
            t = tok.group(0)
            if t.startswith("<"):
                hm = re.match(r'<h[23]\b[^>]*\bid="([^"]+)"', t)
                if hm:
                    anchors.append((pos, hm.group(1)))
                if re.match(r"</?(p|li|div|tr|br|h\d|pre|table|section|ul|ol|dt|dd)\b", t):
                    out.append(" ")
                    pos += 1
            else:
                s = html.unescape(t)
                out.append(s)
                pos += len(s)
        text = "".join(out)
        text = re.sub(r"[ \t\r\n]+", " ", text)
        # positions drifted by whitespace collapsing; recompute anchors proportionally (good enough for navigation)
        if anchors and pos:
            scale = len(text) / max(pos, 1)
            anchors = [(int(a * scale), i) for a, i in anchors]
        pages[rel] = (text, anchors)
    return pages


def nearest(anchors: list[tuple[int, str]], at: int) -> str:
    cur = ""
    for a, i in anchors:
        if a <= at:
            cur = i
        else:
            break
    return cur


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("tokens", nargs="*")
    ap.add_argument("--any", action="store_true")
    ap.add_argument("--re", dest="regex")
    ap.add_argument("--page")
    ap.add_argument("--context", type=int, default=0)
    ap.add_argument("--area")
    ap.add_argument("--limit", type=int, default=25)
    args = ap.parse_args()
    pages = load(args.area)
    if args.page:
        pages = {k: v for k, v in pages.items() if k == args.page}
    rows = []
    for rel, (text, anchors) in pages.items():
        if args.regex:
            hits = [m.start() for m in re.finditer(args.regex, text)]
            counts = {args.regex: len(hits)}
            ok = bool(hits)
        else:
            counts = {t: text.count(t) for t in args.tokens}
            ok = any(counts.values()) if args.any else all(counts.values()) and bool(args.tokens)
            hits = sorted(m.start() for t in args.tokens for m in re.finditer(re.escape(t), text))
        if ok:
            rows.append((rel, len(text.split()), counts, hits, anchors, text))
    rows.sort(key=lambda r: -sum(r[2].values()))
    for rel, words, counts, hits, anchors, text in rows[: args.limit]:
        anc = []
        for h in hits[:6]:
            a = nearest(anchors, h)
            if a and a not in anc:
                anc.append(a)
        print(f"{rel}  ({words}w)  " + " ".join(f"{t}×{n}" for t, n in counts.items()) + ("  #" + ", #".join(anc) if anc else ""))
        if args.context:
            for h in hits[:4]:
                s = text[max(0, h - args.context): h + args.context]
                print("    …" + s + "…")
    print(f"{len(rows)} page(s) match" + (f" (showing {args.limit})" if len(rows) > args.limit else ""))
    return 0 if rows else 1


if __name__ == "__main__":
    sys.exit(main())
