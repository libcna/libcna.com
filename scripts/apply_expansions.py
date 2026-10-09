#!/usr/bin/env python3
"""Apply additive Bible-derived expansions to existing Phase-1/Phase-2 pages (idempotent).

    apply_expansions.py apply [--only KEY ...]     # insert / refresh every expansion under audit/data/bible/expansions/
    apply_expansions.py check                      # every expansion is applied, its marker region is intact and still
                                                   # equals what its source renders to (no writes)
    apply_expansions.py fold [--only KEY ...]      # write each drifted marker region back into its source fragment
    apply_expansions.py list

An expansion is a pair of files authored by a work package, never a direct edit of the target page:

    audit/data/bible/expansions/<WP>/<key>.json    {"target": "docs/game-loop.html", "mode": "append|before_id|after_id",
                                                    "id": "existing-heading-id (before_id / after_id)", "note": "why"}
    audit/data/bible/expansions/<WP>/<key>.html    body fragment: one or more <h2 id="...">/<h3 id="..."> sections, same
                                                    tokens as Development pages ({{src:..}}, {{tree:..}}, {{page:..}})

The block is written between <!--p3:begin KEY--> and <!--p3:end KEY--> so re-running replaces it in place.  Modes:

    append      end of the article content, before the related-pages / pager / pagination block
    before_id   immediately before the element whose id is `id`
    after_id    at the end of the <h2> section whose heading id is `id` (i.e. before the next <h2>)

Only pages under docs/, development/ and deep-dives/ may be targeted (root pages are protected and are edited by hand).  Sections must use ids that
do not exist on the target page; new <h2> entries are added to the page's "On this page" list when it has one; the JSON-LD
dateModified is refreshed.  KEY must be globally unique.  Nothing already on the page is ever removed or altered.
"""

from __future__ import annotations

import argparse
import fcntl
import html
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parent))
import site_dev as SD  # noqa: E402
import site_deep  # noqa: E402,F401  (side effect: {{page:}} tokens may target Deep Dives / Known Issues pages)

ROOT = SD.ROOT
EXP = ROOT / "audit" / "data" / "bible" / "expansions"
ALLOWED = ("docs/", "development/", "deep-dives/")
KEY_RX = re.compile(r"^[a-z0-9][a-z0-9-]{3,60}$")


def load_all() -> list[dict]:
    out = []
    if not EXP.is_dir():
        return out
    for meta in sorted(EXP.glob("*/*.json")):
        body = meta.with_suffix(".html")
        d = json.loads(meta.read_text(encoding="utf-8"))
        d["key"] = meta.stem
        d["wp"] = meta.parent.name
        d["body_path"] = body
        out.append(d)
    return out


def marker(key: str) -> tuple[str, str]:
    return f"<!--p3:begin {key}-->", f"<!--p3:end {key}-->"


TAIL_RX = [re.compile(r"<!--p3:deep-links-->"), re.compile(r"<!--p3:issue-links-->"), re.compile(r'<section class="dev-layers"'), re.compile(r"<!--dev:pager-->"), re.compile(r"<!--deep:pager-->"),
           re.compile(r'<nav class="docs-pagination"'), re.compile(r'<div class="docs-pagination"'), re.compile(r"</article>")]


def insert_index(text: str, mode: str, ident: str | None, errors: list[str], where: str) -> int:
    art = text.find("<article")
    if art < 0:
        errors.append(f"{where}: no <article>")
        return -1
    if mode == "append":
        cands = []
        for rx in TAIL_RX:
            m = rx.search(text, art)
            if m:
                cands.append(m.start())
        # the earliest tail marker that follows all article prose
        return min(cands) if cands else -1
    m = re.search(r'<(h[1-6]|section|div|table|figure|pre|nav)\b[^>]*\bid="' + re.escape(ident or "") + r'"', text[art:])
    if not m:
        errors.append(f"{where}: id {ident!r} not found in the target page")
        return -1
    start = art + m.start()
    if mode == "before_id":
        return start
    # after_id: end of the <h2> section starting at this heading
    nxt = re.search(r"<h2\b", text[start + 4:])
    tail = min([c for c in (TAIL_RX_pos(text, start) or [])] or [len(text)])
    if nxt:
        return min(start + 4 + nxt.start(), tail)
    return tail


def TAIL_RX_pos(text: str, start: int) -> list[int]:
    return [m.start() for rx in TAIL_RX if (m := rx.search(text, start))]


def add_toc(text: str, block: str) -> str:
    m = re.search(r'<ul class="toc-list">(.*?)</ul>', text, re.S)
    if not m:
        return text
    have = set(re.findall(r'href="#([^"]+)"', m.group(1)))
    add = []
    for i, t in re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', block, re.S):
        if i not in have:
            add.append(f'          <li><a href="#{i}">{t}</a></li>\n')
    if not add:
        return text
    pos = m.end(1)
    # keep a trailing "Related pages" entry last
    inner = m.group(1)
    rel = re.search(r'\s*<li><a href="#related-layers">.*?</a></li>\s*$', inner, re.S)
    if rel:
        pos = m.start(1) + rel.start()
    return text[:pos] + "\n" + "".join(add).rstrip("\n") + text[pos:]


def apply_one(exp: dict, errors: list[str]) -> bool:
    key, target = exp["key"], exp.get("target", "")
    where = f"{exp['wp']}/{key}"
    if not KEY_RX.match(key):
        errors.append(f"{where}: key must match {KEY_RX.pattern}")
        return False
    if not target.startswith(ALLOWED):
        errors.append(f"{where}: target {target} is not under {ALLOWED}")
        return False
    path = ROOT / target
    if not path.is_file():
        errors.append(f"{where}: target page missing: {target}")
        return False
    if not exp["body_path"].is_file():
        errors.append(f"{where}: missing fragment {exp['body_path'].relative_to(ROOT)}")
        return False
    mode = exp.get("mode", "append")
    if mode not in ("append", "before_id", "after_id"):
        errors.append(f"{where}: bad mode {mode}")
        return False
    frag = SD.expand_tokens(exp["body_path"].read_text(encoding="utf-8"), target, errors)
    frag = re.sub(r"<table\b", '<div class="table-wrap"><table', frag)
    frag = frag.replace("</table>", "</table></div>")
    text = path.read_text(encoding="utf-8")
    begin, end = marker(key)
    block = f"{begin}\n{frag.strip()}\n{end}\n"
    if begin in text:
        rx = re.compile(re.escape(begin) + r".*?" + re.escape(end) + r"\n?", re.S)
        new = rx.sub(lambda _m: block, text, count=1)
    else:
        # ids the block defines must be new to the page
        existing = set(re.findall(r'\bid="([^"]+)"', text))
        clash = sorted(set(re.findall(r'\bid="([^"]+)"', frag)) & existing)
        if clash:
            errors.append(f"{where}: ids already on {target}: {clash[:6]}")
            return False
        idx = insert_index(text, mode, exp.get("id"), errors, where)
        if idx < 0:
            return False
        new = text[:idx] + block + text[idx:]
        new = add_toc(new, frag)
    new = re.sub(r'("dateModified"\s*:\s*")[^"]+(")', r"\g<1>" + SD.TODAY + r"\g<2>", new)
    if errors:
        return False
    if new != text:
        path.write_text(new, encoding="utf-8")
    return True


def render(exp: dict, errors: list[str]) -> str:
    frag = SD.expand_tokens(exp["body_path"].read_text(encoding="utf-8"), exp.get("target", ""), errors)
    frag = re.sub(r"<table\b", '<div class="table-wrap"><table', frag)
    return frag.replace("</table>", "</table></div>").strip()


def region(exp: dict) -> str | None:
    t = ROOT / exp.get("target", "")
    if not t.is_file():
        return None
    begin, end = marker(exp["key"])
    m = re.search(re.escape(begin) + r"\n?(.*?)\n?" + re.escape(end), t.read_text(encoding="utf-8"), re.S)
    return m.group(1).strip() if m else None


SRC_LINK_RX = re.compile(r'<a class="src-link" href="https://github\.com/libcna/cna/(blob|tree)/([0-9a-f]{40})/([^"#]*)(#L\d+(?:-L\d+)?)?">'
                         r'<code>([^<|}]*)</code></a>')


PAGE_LINK_RX = re.compile(r'<a href="([^":#/?][^"#?]*\.html)(#[^"|}]+)?">([^<|}]*)</a>')


def tokenize(body: str, page: str) -> str:
    """Turn rendered links back into tokens: CNA source links pinned to the current TARGET into {{src:}} / {{tree:}}, and
    relative links to existing site pages into {{page:}}, so a folded source re-pins and re-validates itself on the next
    pin move like an authored one (anything else stays literal HTML; `fold` verifies the round trip)."""
    target = (ROOT / "cnahead").read_text(encoding="utf-8").strip()

    def page_back(m: re.Match) -> str:
        href, frag, label = m.group(1), m.group(2) or "", m.group(3)
        path = os.path.normpath(os.path.join(os.path.dirname(page), href)).replace(os.sep, "/")
        if path.startswith("..") or not SD.known_page(path) or SD.rel_href(page, path) != href:
            return m.group(0)
        return "{{page:" + path + frag + "|" + label + "}}"

    def back(m: re.Match) -> str:
        kind, rev, path, frag, label = m.groups()
        if rev != target:
            return m.group(0)
        path, label = unquote(path), html.unescape(label)
        if kind == "tree":
            path = path.rstrip("/")
            return "{{tree:" + path + ("" if label == path + "/" else "|" + label) + "}}"
        return "{{src:" + path + (frag or "") + ("" if label == path else "|" + label) + "}}"
    return PAGE_LINK_RX.sub(page_back, SRC_LINK_RX.sub(back, body))


def cmd_fold(args: argparse.Namespace) -> int:
    """A page is edited in place when the facts it states change (a pin move rewrites every page, including the regions
    an expansion once inserted). Re-applying the original fragment would then put the stale text back, so the edited
    region is folded back into the source fragment: afterwards `apply` is a no-op and `check` passes. Token-free HTML is
    a valid fragment; table wrappers that `apply` adds are removed so that they are not doubled."""
    rc = 0
    for e in load_all():
        if args.only and e["key"] not in args.only:
            continue
        cur = region(e)
        if cur is None:
            print(f"not applied (nothing to fold): {e['wp']}/{e['key']} -> {e.get('target')}")
            rc = 1
            continue
        errors: list[str] = []
        if render(e, errors) == cur:
            continue
        body = cur.replace('<div class="table-wrap"><table', "<table").replace("</table></div>", "</table>")
        e["body_path"].write_text(tokenize(body, e["target"]) + "\n", encoding="utf-8")
        errors = []
        if render(e, errors) != cur or errors:
            print(f"fold did not round-trip: {e['wp']}/{e['key']} {errors[:2]}")
            rc = 1
        else:
            print(f"folded {e['wp']}/{e['key']} <- {e['target']}")
    return rc


def cmd_apply(args: argparse.Namespace) -> int:
    # several work packages may apply expansions at the same time: serialise read-modify-write of the target pages
    EXP.mkdir(parents=True, exist_ok=True)
    lock = open(EXP / ".lock", "w")
    fcntl.flock(lock, fcntl.LOCK_EX)
    exps = load_all()
    if args.only:
        exps = [e for e in exps if e["key"] in args.only]
    errors: list[str] = []
    n = 0
    seen: dict[str, str] = {}
    for e in exps:
        if e["key"] in seen:
            errors.append(f"duplicate expansion key {e['key']} ({seen[e['key']]} and {e['wp']})")
            continue
        seen[e["key"]] = e["wp"]
        if apply_one(e, errors):
            n += 1
    for msg in errors:
        print("ERROR", msg)
    print(f"applied {n} of {len(exps)} expansion(s); errors {len(errors)}")
    return 1 if errors else 0


def cmd_check(_: argparse.Namespace) -> int:
    rc = 0
    for e in load_all():
        t = ROOT / e.get("target", "")
        begin, end = marker(e["key"])
        if not t.is_file() or begin not in t.read_text(encoding="utf-8") or end not in t.read_text(encoding="utf-8"):
            print(f"not applied: {e['wp']}/{e['key']} -> {e.get('target')}")
            rc = 1
            continue
        errors: list[str] = []
        if render(e, errors) != region(e):
            # `apply` would overwrite the page's current text with the source's older text
            print(f"drift: {e['wp']}/{e['key']} -> {e.get('target')} differs from its source (run `fold` after a deliberate page edit)")
            rc = 1
    print("expansions ok" if rc == 0 else "expansions pending")
    return rc


def cmd_list(_: argparse.Namespace) -> int:
    for e in load_all():
        print(f"{e['wp']:8s} {e['key']:40s} {e.get('mode', 'append'):9s} {e.get('target')}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("apply")
    a.add_argument("--only", nargs="*")
    sub.add_parser("check")
    f = sub.add_parser("fold")
    f.add_argument("--only", nargs="*")
    sub.add_parser("list")
    args = ap.parse_args()
    return {"apply": cmd_apply, "check": cmd_check, "fold": cmd_fold, "list": cmd_list}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
