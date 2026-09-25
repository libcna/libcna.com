#!/usr/bin/env python3
"""Independent adversarial checks for the Phase-3 result (written without reusing bible_inventory.py / bible_ledger.py).

    adversarial_audit.py graph      # re-derive the Bible LaTeX inclusion graph from main.tex and compare it with audit/data/bible/units.json
    adversarial_audit.py anchors    # ledger destinations: page + fragment exist, tokens occur at page level (error) and inside the cited anchor section (counted)
    adversarial_audit.py all        # both (what scripts/validate_all.sh runs)

The Bible repository (default ../bible.libcna.com, override with BIBLE_REPO) is read-only; when it is absent `graph` is skipped, like the other Bible-dependent gates.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BIBLE = Path(os.environ.get("BIBLE_REPO", ROOT.parent / "bible.libcna.com"))
BOOK = BIBLE / "latex" / "book"
UNITS = ROOT / "audit" / "data" / "bible" / "units.json"
RECORDS = ROOT / "audit" / "data" / "bible" / "records"

# ---------------------------------------------------------------------------------------------
# graph
# ---------------------------------------------------------------------------------------------
INCLUDE_KINDS = [
    ("input", re.compile(r"\\input\s*\{([^}]+)\}")),
    ("input-bare", re.compile(r"\\input\s+([A-Za-z0-9_./-]+)")),
    ("include", re.compile(r"\\include\s*\{([^}]+)\}")),
    ("subfile", re.compile(r"\\subfile\s*\{([^}]+)\}")),
    ("import", re.compile(r"\\(?:sub)?import\*?\s*\{([^}]+)\}\s*\{([^}]+)\}")),
    ("iife", re.compile(r"\\InputIfFileExists\s*\{([^}]+)\}")),
]
OTHER_KINDS = [
    ("lstinput", re.compile(r"\\lstinputlisting\s*(?:\[[^\]]*\])?\s*\{([^}]+)\}")),
    ("verbatiminput", re.compile(r"\\verbatiminput\s*\{([^}]+)\}")),
    ("graphics", re.compile(r"\\includegraphics\s*(?:\[[^\]]*\])?\s*\{([^}]+)\}")),
    ("standalone", re.compile(r"\\includestandalone\s*(?:\[[^\]]*\])?\s*\{([^}]+)\}")),
    ("bibliography", re.compile(r"\\(?:bibliography|addbibresource)\s*(?:\[[^\]]*\])?\s*\{([^}]+)\}")),
]


def _strip_comments(text: str) -> str:
    return re.sub(r"(?<!\\)%.*", "", text)


def _resolve(base: str, ref: str) -> Path | None:
    for cand in (BOOK / ref, BOOK / (ref + ".tex"), (BOOK / base).parent / ref, (BOOK / base).parent / (ref + ".tex")):
        cand = cand.resolve()
        if cand.is_file():
            return cand
    return None


def reconstruct() -> tuple[list[str], list[tuple[str, str, str]], list[tuple[str, str]]]:
    """Return (reachable files relative to latex/book, unresolved inclusions, commented-out inclusions)."""
    seen: list[str] = []
    unresolved: list[tuple[str, str, str]] = []
    commented: list[tuple[str, str]] = []
    queue = ["main.tex"]
    while queue:
        rel = queue.pop(0)
        if rel in seen:
            continue
        seen.append(rel)
        raw = (BOOK / rel).read_text(encoding="utf-8")
        active = _strip_comments(raw)
        dead = "\n".join(re.findall(r"(?<!\\)%(.*)", raw))
        for kind, rx in INCLUDE_KINDS:
            for m in rx.finditer(active):
                ref = "/".join(m.groups())
                target = _resolve(rel, ref)
                if target is None:
                    unresolved.append((rel, kind, ref))
                    continue
                queue.append(os.path.relpath(target, BOOK))
        for kind, rx in INCLUDE_KINDS + OTHER_KINDS:
            for m in rx.finditer(dead):
                commented.append((rel, "/".join(m.groups())))
    return seen, unresolved, commented


def cmd_graph() -> int:
    if not BOOK.joinpath("main.tex").is_file():
        print("graph: Bible repository not present (BIBLE_REPO); skipped")
        return 0
    seen, unresolved, commented = reconstruct()
    mine = {("latex/book/" + s) if not s.startswith("..") else "latex/" + s[3:] for s in seen}
    theirs = {u["path"] for u in json.loads(UNITS.read_text(encoding="utf-8"))["units"]}
    structural = {"latex/book/main.tex", "latex/common/preamble.tex"}
    errs = []
    if unresolved:
        errs.append(f"unresolved inclusions: {unresolved[:5]}")
    if commented:
        errs.append(f"commented-out inclusions (decide whether they are canonical): {commented[:5]}")
    if theirs - mine:
        errs.append(f"units.json lists files that main.tex does not reach: {sorted(theirs - mine)[:5]}")
    if mine - theirs - structural:
        errs.append(f"main.tex reaches files that units.json lacks: {sorted(mine - theirs - structural)}")
    for e in errs:
        print("ERROR", e)
    print(f"graph: {len(mine)} reachable TeX files = {len(mine & theirs)} units + {len(mine & structural)} structural (main.tex, preamble); errors {len(errs)}")
    return 1 if errs else 0


# ---------------------------------------------------------------------------------------------
# anchors
# ---------------------------------------------------------------------------------------------
VOID = {"br", "hr", "img", "meta", "link", "input", "area", "base", "col", "embed", "source", "track", "wbr"}
BLOCK = {"p", "li", "div", "tr", "td", "th", "br", "h1", "h2", "h3", "h4", "h5", "h6", "pre", "table", "section", "ul", "ol", "dt", "dd", "figure",
         "figcaption", "blockquote", "dl", "thead", "tbody", "nav", "aside", "article", "main", "summary", "details"}
HEAD = re.compile(r"^h([1-6])$")


class Node:
    __slots__ = ("tag", "attrs", "kids", "parent")

    def __init__(self, tag: str, attrs: dict, parent: "Node | None") -> None:
        self.tag, self.attrs, self.kids, self.parent = tag, attrs, [], parent


class Tree(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = Node("root", {}, None)
        self.cur = self.root
        self.ids: dict[str, Node] = {}

    def handle_starttag(self, tag, attrs):
        n = Node(tag, dict(attrs), self.cur)
        self.cur.kids.append(n)
        if n.attrs.get("id"):
            self.ids.setdefault(n.attrs["id"], n)
        if tag not in VOID:
            self.cur = n

    def handle_endtag(self, tag):
        c = self.cur
        while c is not None and c.tag != tag:
            c = c.parent
        if c is not None and c.parent is not None:
            self.cur = c.parent

    def handle_data(self, data):
        self.cur.kids.append(data)


def node_text(n) -> str:
    if isinstance(n, str):
        return n
    if n.tag in ("script", "style"):
        return ""
    inner = "".join(node_text(k) for k in n.kids)
    return f" {inner} " if n.tag in BLOCK else inner


def section_text(n: Node) -> str:
    """Text an anchor 'owns': a heading owns everything up to the next heading of the same or a higher level, a <dt> its <dd>s, anything else its own subtree."""
    if n.tag == "dt":
        out, sib = [node_text(n)], n.parent.kids
        for x in sib[sib.index(n) + 1:]:
            if not isinstance(x, str) and x.tag == "dt":
                break
            out.append(node_text(x))
        return " ".join(out)
    m = HEAD.match(n.tag)
    if not m:
        return node_text(n)
    level, out, sib = int(m.group(1)), [node_text(n)], n.parent.kids
    for s in sib[sib.index(n) + 1:]:
        if not isinstance(s, str):
            hm = HEAD.match(s.tag)
            if hm and int(hm.group(1)) <= level:
                break
            inner = [x for x in s.kids if not isinstance(x, str) and HEAD.match(x.tag)]
            if inner and int(HEAD.match(inner[0].tag).group(1)) <= level:
                break
        out.append(node_text(s))
    return " ".join(out)


_trees: dict[str, Tree | None] = {}
_sections: dict[tuple[str, str], str | None] = {}


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(s))


def section(rel: str, frag: str) -> str | None:
    key = (rel, frag)
    if key not in _sections:
        if rel not in _trees:
            p = ROOT / rel
            if p.is_file() and p.suffix == ".html":
                t = Tree()
                t.feed(p.read_text(encoding="utf-8"))
                _trees[rel] = t
            else:
                _trees[rel] = None
        t = _trees[rel]
        if t is None:
            _sections[key] = None
        elif not frag:
            _sections[key] = _norm(node_text(t.root))
        else:
            _sections[key] = _norm(section_text(t.ids[frag])) if frag in t.ids else None
    return _sections[key]


def cmd_anchors(strict: bool = False) -> int:
    errs: list[str] = []
    anchor_only: list[str] = []
    stats: Counter = Counter()
    for p in sorted(RECORDS.glob("*.json")):
        rec = json.loads(p.read_text(encoding="utf-8"))
        uid = p.stem
        items = [(c.get("id", "?"), c.get("destinations") or [], c.get("tokens") or [], True) for c in rec.get("concepts") or []]
        items += [(f"figure {f.get('unit')}", f.get("destinations") or [], [], False) for f in rec.get("figures") or []]
        items += [(f"example {e.get('id')}", e.get("destinations") or [], [], False) for e in rec.get("examples") or []]
        for cid, dests, toks, is_concept in items:
            page_blob: list[str] = []
            anchor_blob: list[str] = []
            broken = False
            for d in dests:
                base, _, frag = d.partition("#")
                pg = section(base, "")
                if pg is None:
                    errs.append(f"{uid}/{cid}: destination page does not exist: {base}")
                    broken = True
                    continue
                page_blob.append(pg)
                if frag:
                    sec = section(base, frag)
                    if sec is None:
                        errs.append(f"{uid}/{cid}: destination anchor does not exist: {d}")
                        broken = True
                        continue
                    anchor_blob.append(sec)
                else:
                    anchor_blob.append(pg)
            stats["destinations"] += len(dests)
            if broken or not toks or not is_concept:
                continue
            pb, ab = " ".join(page_blob), " ".join(anchor_blob)
            miss_page = [t for t in toks if _norm(t) not in pb]
            miss_anchor = [t for t in toks if _norm(t) not in ab]
            if miss_page:
                errs.append(f"{uid}/{cid}: token(s) absent from the destination page(s): {miss_page[:4]}")
            elif miss_anchor:
                anchor_only.append(f"{uid}/{cid}: {miss_anchor[:3]} not inside {dests[0]}")
            else:
                stats["ok"] += 1
    for e in errs:
        print("ERROR", e)
    if strict:
        for a in anchor_only:
            print("ERROR (anchor precision)", a)
    print(f"anchors: {stats['destinations']} destinations checked; {stats['ok']} concepts fully anchored; "
          f"tokens on the page but outside the cited anchor: {len(anchor_only)}; errors {len(errs) + (len(anchor_only) if strict else 0)}")
    return 1 if errs or (strict and anchor_only) else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("graph")
    a = sub.add_parser("anchors")
    a.add_argument("--strict", action="store_true", help="treat anchor-precision misses as errors")
    sub.add_parser("all")
    args = ap.parse_args()
    if args.cmd == "graph":
        return cmd_graph()
    if args.cmd == "anchors":
        return cmd_anchors(args.strict)
    return cmd_graph() | cmd_anchors()


if __name__ == "__main__":
    sys.exit(main())
