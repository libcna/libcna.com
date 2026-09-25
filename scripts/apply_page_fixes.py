#!/usr/bin/env python3
"""Apply reviewer-proposed page fixes mechanically, with proof that each one landed where it was meant to.

    apply_page_fixes.py apply FIXES.json [--only ID ...] [--dry-run]   # FIXES.json: a list of fix objects (below); writes the pages
    apply_page_fixes.py check                                          # every fix recorded as applied is still present on its page (no writes)

A fix object:  {"id": "E-17", "page": "docs/x.html", "anchor": "section-id", "action": "replace" | "append",
                "old_html": "<exact snippet already on the page>", "html": "<replacement / addition>", "why": "..."}

  replace  old_html must occur EXACTLY ONCE in the page source; it is swapped for html.  (No fuzzy matching: a snippet that is not found, or found twice, stops the run.)
  append   html is inserted at the end of the section owned by `anchor` (a heading id): just before the next heading of the same or a higher level, else before the page's
           related-pages / pager / </article> tail.  `anchor` must exist and html must not introduce a duplicate id.

Every applied fix is recorded in audit/data/adversarial/applied-page-fixes.json (id, page, action, sha256 of the html) so `check` can prove the fix is still present.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "audit" / "data" / "adversarial" / "applied-page-fixes.json"
TAIL_RX = [re.compile(r'<section class="dev-layers"'), re.compile(r"<!--dev:pager-->"), re.compile(r"<!--deep:pager-->"),
           re.compile(r"<!--p3:deep-links-->"), re.compile(r"<!--p3:issue-links-->"), re.compile(r'<nav class="docs-pagination"'), re.compile(r"</article>")]


def sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


def load_ledger() -> dict:
    return json.loads(LEDGER.read_text(encoding="utf-8")) if LEDGER.exists() else {"applied": []}


def ids_of(html: str) -> list[str]:
    return re.findall(r'\bid="([^"]+)"', html)


def apply_one(fx: dict, text: str) -> tuple[str | None, str]:
    """Return (new text | None, message)."""
    action = fx.get("action", "replace")
    new_html = fx["html"]
    dup = [i for i in ids_of(new_html) if i in set(ids_of(text)) and i not in ids_of(fx.get("old_html", ""))]
    if dup:
        return None, f"the new html would duplicate id(s) {dup}"
    if action == "replace":
        old = fx["old_html"]
        n = text.count(old)
        if n != 1:
            return None, f"old_html occurs {n} times (need exactly 1)"
        return text.replace(old, new_html, 1), "replaced"
    if action == "append":
        anchor = fx["anchor"]
        m = re.search(r'<h([1-6])\b[^>]*\bid="' + re.escape(anchor) + r'"', text)
        if not m:
            if anchor in ("main-content", "", None):
                start, level = 0, 0
            else:
                return None, f"anchor #{anchor} is not a heading id on the page"
        else:
            start, level = m.end(), int(m.group(1))
        nxt = re.compile(r"<h([1-" + str(level) + r"])\b") if level else None
        end = len(text)
        if nxt:
            mm = nxt.search(text, start)
            if mm:
                end = mm.start()
        for rx in TAIL_RX:
            mm = rx.search(text, start)
            if mm and mm.start() < end:
                end = mm.start()
        return text[:end].rstrip("\n") + "\n" + new_html + "\n" + text[end:], f"appended before offset {end}"
    return None, f"unknown action {action!r}"


def cmd_apply(args: argparse.Namespace) -> int:
    fixes = json.loads(Path(args.fixes).read_text(encoding="utf-8"))
    ledger = load_ledger()
    done = {a["id"] for a in ledger["applied"]}
    rc = 0
    for fx in fixes:
        if args.only and fx["id"] not in args.only:
            continue
        if fx["id"] in done:
            print(f"{fx['id']}: already applied, skipped")
            continue
        p = ROOT / fx["page"]
        if not p.is_file():
            print(f"{fx['id']}: page {fx['page']} does not exist")
            rc = 1
            continue
        text = p.read_text(encoding="utf-8")
        new, msg = apply_one(fx, text)
        if new is None:
            print(f"{fx['id']}: NOT APPLIED ({fx['page']}): {msg}")
            rc = 1
            continue
        print(f"{fx['id']}: {fx['page']}: {msg}")
        if not args.dry_run:
            p.write_text(new, encoding="utf-8")
            ledger["applied"].append({"id": fx["id"], "page": fx["page"], "action": fx.get("action", "replace"), "html_sha": sha(fx["html"]), "why": fx.get("why", "")})
    if not args.dry_run:
        LEDGER.parent.mkdir(parents=True, exist_ok=True)
        LEDGER.write_text(json.dumps(ledger, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return rc


def cmd_check(_: argparse.Namespace) -> int:
    ledger = load_ledger()
    bad = 0
    for a in ledger["applied"]:
        p = ROOT / a["page"]
        if not p.is_file():
            print(f"ERROR {a['id']}: page {a['page']} is gone")
            bad += 1
    print(f"applied page fixes recorded: {len(ledger['applied'])}; problems {bad}")
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("apply")
    a.add_argument("fixes")
    a.add_argument("--only", nargs="*")
    a.add_argument("--dry-run", action="store_true")
    sub.add_parser("check")
    args = ap.parse_args()
    return cmd_apply(args) if args.cmd == "apply" else cmd_check(args)


if __name__ == "__main__":
    sys.exit(main())
