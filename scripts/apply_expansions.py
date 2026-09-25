#!/usr/bin/env python3
"""Apply additive Bible-derived expansions to existing Phase-1/Phase-2 pages (idempotent).

    apply_expansions.py apply [--only KEY ...]     # insert / refresh every expansion under audit/data/bible/expansions/
    apply_expansions.py check                      # every expansion is applied and its marker region is intact (no writes)
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

Only pages under docs/ and development/ may be targeted (root pages are protected and are edited by hand).  Sections must use ids that
do not exist on the target page; new <h2> entries are added to the page's "On this page" list when it has one; the JSON-LD
dateModified is refreshed.  KEY must be globally unique.  Nothing already on the page is ever removed or altered.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import site_dev as SD  # noqa: E402
import site_deep  # noqa: E402,F401  (side effect: {{page:}} tokens may target Deep Dives / Known Issues pages)

ROOT = SD.ROOT
EXP = ROOT / "audit" / "data" / "bible" / "expansions"
ALLOWED = ("docs/", "development/")
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


TAIL_RX = [re.compile(r'<section class="dev-layers"'), re.compile(r"<!--dev:pager-->"), re.compile(r"<!--deep:pager-->"),
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


def cmd_apply(args: argparse.Namespace) -> int:
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
    sub.add_parser("list")
    args = ap.parse_args()
    return {"apply": cmd_apply, "check": cmd_check, "list": cmd_list}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
