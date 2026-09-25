#!/usr/bin/env python3
"""Phase-3 Bible absorption ledger: check, progress and render.

    bible_ledger.py progress [--units ID ...]   # one-screen state (units audited, concepts by disposition, bugs)
    bible_ledger.py check [--units ID ...] [--final]
                                                # conservation checks; exit 1 on any ERROR.  --final also requires
                                                # pending == 0 and MISSING == 0
    bible_ledger.py render                      # write audit/bible-absorption-phase3.md (+ ...-concepts.md)

Inputs
  audit/data/bible/units.json           the mechanically enumerated Bible source graph (scripts/bible_inventory.py)
  audit/data/bible/records/<id>.json    one authored record per unit (see audit/data/bible/README.md)
  audit/data/bible/bugs-*.json          bug / gap verification records are checked by scripts/known_issues.py

A unit is *audited* when its record exists, is marked done, and passes every check below.  The conservation invariant is
pending == 0, no MISSING concept, and no unaccounted Bible heading.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "audit" / "data" / "bible"
UNITS = DATA / "units.json"
RECORDS = DATA / "records"
REPORT = ROOT / "audit" / "bible-absorption-phase3.md"
CONCEPTS = ROOT / "audit" / "bible-absorption-phase3-concepts.md"

DISPOSITIONS = ["PRESERVED", "SUPERSEDED", "EXPANDED", "MOVED", "NEW PAGE", "OBSOLETE", "HISTORICAL ONLY", "FIXED BUG",
                "REMOVED FUNCTIONALITY", "DUPLICATE", "TARGET CONTRADICTED", "MISSING"]
NEEDS_DEST = {"PRESERVED", "SUPERSEDED", "EXPANDED", "MOVED", "NEW PAGE", "DUPLICATE"}
NEEDS_NOTE = {"OBSOLETE", "HISTORICAL ONLY", "FIXED BUG", "REMOVED FUNCTIONALITY", "TARGET CONTRADICTED", "MISSING"}
ACTIONS = {"MERGE", "EXPAND", "NEW PAGE", "DEEP DIVE", "REFERENCE", "TUTORIAL", "MAINTAINER", "TESTING/EVIDENCE", "BUG", "GAP",
           "HISTORY", "SUPERSEDED", "DUPLICATE", "OBSOLETE", "TARGET-CONTRADICTED", "REMOVED FUNCTIONALITY"}
FIG_DISPOSITIONS = {"PRESERVED", "RECREATED", "SUPERSEDED", "OBSOLETE", "MISSING"}
EX_DISPOSITIONS = {"PRESERVED", "RECREATED", "SUPERSEDED", "REJECTED", "OBSOLETE", "NOT PORTED", "MISSING"}
TARGET_RESULTS = {"confirmed", "corrected", "contradicted", "obsolete", "not-applicable", "unverifiable-hedged"}
RELEVANCE = {"current", "partly-stale", "stale", "historical"}
ISSUE_KINDS = {"bug-candidate", "functional-gap", "platform-limitation", "verification-gap", "not-an-issue"}


def norm(s: str) -> str:
    s = html.unescape(s)
    s = re.sub(r"\\[a-zA-Z]+\*?", " ", s)
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


BLOCK_TAGS = {"p", "li", "div", "tr", "td", "th", "br", "h1", "h2", "h3", "h4", "h5", "h6", "pre", "table", "section", "ul", "ol", "dt", "dd",
              "figure", "figcaption", "blockquote", "dl", "thead", "tbody", "nav", "aside", "article", "main", "summary", "details"}


class Page(HTMLParser):
    """Collects ids and the text of <article> (or <main> when a page has no article, e.g. the protected root pages).
    Inline tags add nothing, block tags add a space, so a token that runs across <code>…</code> before punctuation still matches."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.text: list[str] = []
        self._art = 0
        self._main = 0
        self._skip = 0
        self.has_article = False

    @property
    def _in(self) -> bool:
        return bool(self._art or (self._main and not self.has_article))

    def handle_starttag(self, tag, attrs):
        v = {k: (x or "") for k, x in attrs}
        if v.get("id"):
            self.ids.add(v["id"])
        if tag == "article":
            self._art += 1
            self.has_article = True
        if tag == "main":
            self._main += 1
        if tag in ("script", "style"):
            self._skip += 1
        if tag in BLOCK_TAGS and self._in:
            self.text.append(" ")

    def handle_endtag(self, tag):
        if tag == "article" and self._art:
            self._art -= 1
        if tag == "main" and self._main:
            self._main -= 1
        if tag in ("script", "style") and self._skip:
            self._skip -= 1
        if tag in BLOCK_TAGS and self._in:
            self.text.append(" ")

    def handle_data(self, data):
        if self._in and not self._skip:
            self.text.append(data)


_page_cache: dict[str, Page | None] = {}


def load_page(rel: str) -> Page | None:
    if rel not in _page_cache:
        p = ROOT / rel
        if not p.is_file() or p.suffix != ".html":
            _page_cache[rel] = None
        else:
            pg = Page()
            pg.feed(p.read_text(encoding="utf-8"))
            _page_cache[rel] = pg
    return _page_cache[rel]


def page_text(rel: str) -> str:
    pg = load_page(rel)
    return re.sub(r"\s+", " ", "".join(pg.text)) if pg else ""


def split_dest(d: str) -> tuple[str, str]:
    base, _, frag = d.partition("#")
    return base, frag


def load_units() -> dict:
    return json.loads(UNITS.read_text(encoding="utf-8"))


def record_units(doc: dict) -> list[dict]:
    """Units that carry their own record file: every tex unit except figures (those are recorded by their including chapter), plus aux documents."""
    return [u for u in doc["units"] if u["kind"] != "figure"] + doc["aux"]


def load_records() -> dict[str, dict]:
    out = {}
    if RECORDS.is_dir():
        for p in sorted(RECORDS.glob("*.json")):
            try:
                out[p.stem] = json.loads(p.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                out[p.stem] = {"_error": f"invalid JSON: {exc}"}
    return out


# ---------------------------------------------------------------------------------------------
# checks
# ---------------------------------------------------------------------------------------------
def check_dest(dest: str, where: str, errs: list[str]) -> bool:
    base, frag = split_dest(dest)
    pg = load_page(base)
    if pg is None:
        errs.append(f"{where}: destination page does not exist: {base}")
        return False
    if frag and frag not in pg.ids:
        errs.append(f"{where}: destination fragment missing: {dest}")
        return False
    return True


def check_record(uid: str, rec: dict, unit: dict, final: bool) -> tuple[list[str], list[str]]:
    errs: list[str] = []
    warns: list[str] = []
    if "_error" in rec:
        return [f"{uid}: {rec['_error']}"], warns
    if rec.get("unit") != uid:
        errs.append(f"{uid}: record 'unit' is {rec.get('unit')!r}")
    if not rec.get("done"):
        errs.append(f"{uid}: record is not marked done")
    if rec.get("target_relevance") not in RELEVANCE:
        errs.append(f"{uid}: target_relevance must be one of {sorted(RELEVANCE)}")
    if len(rec.get("summary", "")) < 60:
        errs.append(f"{uid}: summary missing or too short")
    acts = rec.get("actions") or []
    if not acts or any(a not in ACTIONS for a in acts):
        errs.append(f"{uid}: actions must be a non-empty subset of {sorted(ACTIONS)} (got {acts})")

    kind = unit["kind"]
    concepts = rec.get("concepts") or []
    if kind in ("chapter", "front", "appendix", "fragment") or kind == "aux":
        if not concepts:
            errs.append(f"{uid}: no concepts recorded")
    ids = [c.get("id") for c in concepts]
    dup = [k for k, n in Counter(ids).items() if n > 1]
    if dup:
        errs.append(f"{uid}: duplicate concept ids {dup[:5]}")

    heads = unit.get("headings") or []
    head_norm = {norm(h["title"]): h for h in heads}
    covered: set[str] = set()
    for c in concepts:
        cid = c.get("id", "?")
        where = f"{uid}/{cid}"
        d = c.get("disposition")
        if d not in DISPOSITIONS:
            errs.append(f"{where}: invalid disposition {d!r}")
            continue
        if len(c.get("text", "")) < 25:
            errs.append(f"{where}: concept text missing or too short")
        sec = c.get("section", "")
        if sec:
            covered.add(norm(sec))
        if d == "MISSING":
            (errs if final else warns).append(f"{where}: still MISSING — {c.get('text', '')[:80]}")
        dests = c.get("destinations") or []
        if d in NEEDS_DEST and not dests:
            errs.append(f"{where}: {d} requires at least one destination")
        if d in NEEDS_NOTE and d != "MISSING" and len(c.get("note", "")) < 20:
            errs.append(f"{where}: {d} requires a note (>=20 chars) explaining why")
        ok_dest = True
        for dest in dests:
            ok_dest &= check_dest(dest, where, errs)
        tr = (c.get("target") or {}).get("result")
        if d not in ("OBSOLETE", "HISTORICAL ONLY", "REMOVED FUNCTIONALITY") and tr not in TARGET_RESULTS:
            errs.append(f"{where}: target.result must be one of {sorted(TARGET_RESULTS)}")
        if d in NEEDS_DEST and dests and ok_dest:
            toks = c.get("tokens") or []
            if not toks and not c.get("no_tokens_reason"):
                errs.append(f"{where}: {d} needs 'tokens' (identifiers/phrases that must occur in the destination) "
                            f"or a 'no_tokens_reason'")
            blob = " ".join(page_text(split_dest(x)[0]) for x in dests)
            missing = [t for t in toks if t not in blob]
            if missing:
                errs.append(f"{where}: token(s) not found in destination page text: {missing[:6]}")
        if d == "TARGET CONTRADICTED" and (c.get("target") or {}).get("result") not in ("contradicted", "corrected"):
            errs.append(f"{where}: TARGET CONTRADICTED needs target.result contradicted|corrected with evidence")

    empties = {norm(e.get("heading", "")): e for e in (rec.get("empty_sections") or [])}
    for e in empties.values():
        if len(e.get("reason", "")) < 12:
            errs.append(f"{uid}: empty_sections entry needs a reason: {e.get('heading')}")
    unaccounted = [h["title"] for k, h in head_norm.items() if k not in covered and k not in empties]
    if unaccounted:
        errs.append(f"{uid}: {len(unaccounted)} Bible heading(s) with no concept and not listed in empty_sections: "
                    f"{unaccounted[:6]}")

    words = unit.get("prose_words", 0)
    if concepts and words >= 400:
        per_k = len(concepts) / (words / 1000)
        if per_k < 6:
            warns.append(f"{uid}: sparse concept extraction ({len(concepts)} concepts / {words} words = {per_k:.1f} per 1000)")

    for f in rec.get("figures") or []:
        if f.get("disposition") not in FIG_DISPOSITIONS:
            errs.append(f"{uid}: figure {f.get('unit')} has invalid disposition {f.get('disposition')!r}")
        if f.get("disposition") in ("PRESERVED", "RECREATED", "SUPERSEDED"):
            if not f.get("destinations"):
                errs.append(f"{uid}: figure {f.get('unit')} needs destinations")
            for dest in f.get("destinations") or []:
                check_dest(dest, f"{uid}/figure {f.get('unit')}", errs)
        elif f.get("disposition") == "OBSOLETE" and len(f.get("note", "")) < 20:
            errs.append(f"{uid}: obsolete figure {f.get('unit')} needs a note")
        elif f.get("disposition") == "MISSING":
            (errs if final else warns).append(f"{uid}: figure {f.get('unit')} still MISSING")
    for ex in rec.get("examples") or []:
        if ex.get("disposition") not in EX_DISPOSITIONS:
            errs.append(f"{uid}: example {ex.get('id')} has invalid disposition {ex.get('disposition')!r}")
        if ex.get("disposition") in ("PRESERVED", "RECREATED", "SUPERSEDED"):
            for dest in ex.get("destinations") or []:
                check_dest(dest, f"{uid}/example {ex.get('id')}", errs)
            if not ex.get("destinations"):
                errs.append(f"{uid}: example {ex.get('id')} needs destinations")
        if ex.get("disposition") == "MISSING":
            (errs if final else warns).append(f"{uid}: example {ex.get('id')} still MISSING")
    for iss in rec.get("issues") or []:
        if iss.get("kind") not in ISSUE_KINDS:
            errs.append(f"{uid}: issue kind {iss.get('kind')!r} invalid (want one of {sorted(ISSUE_KINDS)})")
    return errs, warns


def run_check(only: list[str] | None, final: bool, quiet: bool = False) -> int:
    doc = load_units()
    recs = load_records()
    units = {u["id"]: u for u in record_units(doc)}
    errs: list[str] = []
    warns: list[str] = []
    audited = 0
    for uid, unit in units.items():
        if only and uid not in only:
            continue
        rec = recs.get(uid)
        if rec is None:
            if final:
                errs.append(f"{uid}: no record (pending)")
            continue
        e, w = check_record(uid, rec, unit, final)
        errs += e
        warns += w
        if not e:
            audited += 1
    extra = sorted(set(recs) - set(units))
    for x in extra:
        errs.append(f"record without a unit: {x}")
    # figures / assets must each be covered exactly once
    fig_cover: Counter = Counter()
    for rec in recs.values():
        for f in rec.get("figures") or []:
            fig_cover[f.get("unit")] += 1
    for u in doc["units"]:
        if u["kind"] == "figure" and final and not only and fig_cover[u["id"]] != 1:
            errs.append(f"figure {u['id']} covered {fig_cover[u['id']]} times (need exactly 1)")
    for a in doc["assets"]:
        key = "asset:" + a["id"]
        if final and not only and fig_cover[key] != 1:
            errs.append(f"asset {a['id']} covered {fig_cover[key]} times (need exactly 1)")
    # stable global concept ids
    seen: dict[str, str] = {}
    for uid, rec in recs.items():
        for c in rec.get("concepts") or []:
            cid = c.get("id")
            if cid in seen and seen[cid] != uid:
                errs.append(f"concept id {cid} used in both {seen[cid]} and {uid}")
            seen[cid] = uid
    for e in errs:
        print("ERROR", e)
    if not quiet:
        for w in warns[:80]:
            print("warn ", w)
    total = len([u for k, u in units.items() if not only or k in only])
    pend = total - audited
    print(f"units: {audited}/{total} audited, pending {pend} | errors {len(errs)} | warnings {len(warns)}")
    return 1 if errs else 0


# ---------------------------------------------------------------------------------------------
# progress / render
# ---------------------------------------------------------------------------------------------
def tally(recs: dict[str, dict]) -> tuple[Counter, Counter, list]:
    disp: Counter = Counter()
    tgt: Counter = Counter()
    issues: list = []
    for uid, rec in recs.items():
        for c in rec.get("concepts") or []:
            disp[c.get("disposition")] += 1
            tgt[(c.get("target") or {}).get("result", "-")] += 1
        for i in rec.get("issues") or []:
            issues.append((uid, i))
    return disp, tgt, issues


def cmd_progress(args: argparse.Namespace) -> int:
    doc = load_units()
    recs = load_records()
    units = record_units(doc)
    done = [u for u in units if u["id"] in recs and recs[u["id"]].get("done")]
    disp, tgt, issues = tally(recs)
    print(f"Bible units (tex graph): {len(doc['units'])} (record units {len(units) - len(doc['aux'])} + {sum(1 for u in doc['units'] if u['kind'] == 'figure')} figures)  "
          f"assets: {len(doc['assets'])}  aux: {len(doc['aux'])}")
    print(f"records done: {len(done)}/{len(units)}   pending: {len(units) - len(done)}")
    print("concepts:", sum(disp.values()), dict(disp.most_common()))
    print("target verification:", dict(tgt.most_common()))
    print("issue candidates:", Counter(i.get("kind") for _, i in issues))
    return 0


def dest_summary(rec: dict) -> list[str]:
    seen: list[str] = []
    for c in rec.get("concepts") or []:
        for d in c.get("destinations") or []:
            b = split_dest(d)[0]
            if b not in seen:
                seen.append(b)
    for f in (rec.get("figures") or []) + (rec.get("examples") or []):
        for d in f.get("destinations") or []:
            b = split_dest(d)[0]
            if b not in seen:
                seen.append(b)
    return seen


def page_words(rel: str) -> int:
    pg = load_page(rel)
    return len("".join(pg.text).split()) if pg else 0


def cmd_render(_: argparse.Namespace) -> int:
    doc = load_units()
    recs = load_records()
    meta = doc["meta"]
    units = record_units(doc)
    total = len(units)
    done = [u for u in units if u["id"] in recs and recs[u["id"]].get("done")]
    disp, tgt, issues = tally(recs)
    L: list[str] = []
    L += ["# Phase-3 absorption ledger — the CNA Bible → libcna.com", "",
          "Durable record of the additive absorption of the CNA Bible's current technical knowledge into libcna.com. Generated by "
          "`scripts/bible_ledger.py render` from `audit/data/bible/units.json` (mechanical source graph) and "
          "`audit/data/bible/records/*.json` (one authored record per unit). Nothing here is served as site content. "
          "Full concept-level tables: `audit/bible-absorption-phase3-concepts.md`.", ""]
    L += ["## 1. Source boundary", "", "| Item | Value |", "|---|---|",
          f"| `PHASE2_BASE` (accepted Phase-2 HEAD, branch `docs/unified-v2`) | `2c4970c131eac9b69a9bbfb3c30eee080cbc1469` — “docs: add the Living Room Simulator web build to the demos” |",
          f"| CNA `TARGET` (= `cnahead`) | `{(ROOT / 'cnahead').read_text().strip()}` |",
          f"| Bible repository HEAD | `{meta['bible_head']}` (branch `{meta['bible_branch']}`); its **working tree** was read: {meta['bible_dirty_paths']} paths modified or untracked (uncommitted synchronisation work included) |",
          f"| Bible `cnahead` (the CNA commit it documents) | `{meta['bible_cnahead']}` — an ancestor of TARGET, 55 commits earlier; chapters not touched by that synchronisation still describe the alpha.1 baseline |",
          f"| Source graph | {meta['graph_files']} LaTeX files reached from `latex/book/main.tex` ({meta['main_tex_inputs']} direct inputs + nested fragments and figures); read from the working tree, not HEAD or the generated HTML/PDF |", ""]
    nfig = sum(1 for u in doc["units"] if u["kind"] == "figure")
    ntex = len(doc["units"]) - nfig
    L += ["## 2. Progress", "", f"- Bible source units audited: **{len(done)}/{total}** = {ntex} canonical LaTeX units (front matter, chapters, appendices, nested fragments) + {len(doc['aux'])} auxiliary evidence/planning documents "
          f"(canonical LaTeX units audited: **{sum(1 for u in units if u['kind'] != 'aux' and u['id'] in recs and recs[u['id']].get('done'))}/{ntex}**)",
          f"- Figures (TikZ sources) and raster images, recorded inside their including chapter: {nfig} figures + {len(doc['assets'])} images",
          f"- Pending source units: **{total - len(done)}**",
          f"- Technical concepts classified: **{sum(disp.values())}**",
          f"- Useful current concepts still MISSING: **{disp.get('MISSING', 0)}**", ""]
    L += ["| Disposition | Concepts |", "|---|---:|"] + [f"| {d} | {disp.get(d, 0)} |" for d in DISPOSITIONS] + [""]
    L += ["| TARGET verification result | Concepts |", "|---|---:|"] + [f"| {k} | {v} |" for k, v in sorted(tgt.items())] + [""]
    L += ["## 3. Units", "",
          "| # | Source unit | Part / chapter | Scope | TARGET relevance | Concepts | Destinations | Action | Verification | Done |",
          "|---:|---|---|---|---|---:|---|---|---|---|"]
    for u in units:
        rec = recs.get(u["id"])
        part = u.get("part") or u.get("category", "")
        if u["kind"] == "chapter" and u.get("chapter_number"):
            part += f" · ch{u['chapter_number']}"
        scope = f"{u.get('prose_words', 0)} words · {len(u.get('headings') or [])} headings" if u["kind"] != "aux" else f"{u.get('bytes', 0) // 1024} KiB"
        if not rec:
            L.append(f"| {u.get('order', '')} | `{u['id']}` ({u['kind']}) | {part} | {scope} | – | – | – | – | – | ☐ |")
            continue
        cs = rec.get("concepts") or []
        dests = dest_summary(rec)
        dtxt = ", ".join(f"`{d}`" for d in dests[:4]) + (f" (+{len(dests) - 4})" if len(dests) > 4 else "")
        vc = Counter((c.get("target") or {}).get("result", "-") for c in cs)
        vtxt = ", ".join(f"{k} {v}" for k, v in vc.most_common(4))
        L.append(f"| {u.get('order', '')} | `{u['id']}` ({u['kind']}) | {part} | {scope} | {rec.get('target_relevance', '')} | "
                 f"{len(cs)} | {dtxt} | {', '.join(rec.get('actions') or [])} | {vtxt} | {'☑' if rec.get('done') else '☐'} |")
    L.append("")
    fig_rows = []
    for uid, rec in recs.items():
        for f in rec.get("figures") or []:
            fig_rows.append((f.get("unit"), uid, f))
    if fig_rows:
        L += ["## 4. Figures, diagrams and images", "", "| Figure / asset | Recorded in | Disposition | Destination | Note |", "|---|---|---|---|---|"]
        for unit, uid, f in sorted(fig_rows, key=lambda r: str(r[0])):
            L.append(f"| `{unit}` | `{uid}` | {f.get('disposition')} | {', '.join(f'`{d}`' for d in f.get('destinations') or [])} | {f.get('note', '')[:160].replace('|', '/')} |")
        L.append("")
    ex_rows = [(uid, e) for uid, rec in recs.items() for e in rec.get("examples") or []]
    if ex_rows:
        L += ["## 5. Code examples", "", "| Unit | Example | Disposition | Verification | Destination | Note |", "|---|---|---|---|---|---|"]
        for uid, e in ex_rows:
            L.append(f"| `{uid}` | {e.get('id')}: {e.get('text', '')[:80].replace('|', '/')} | {e.get('disposition')} | {e.get('verified', '')} | "
                     f"{', '.join(f'`{d}`' for d in e.get('destinations') or [])} | {e.get('note', '')[:120].replace('|', '/')} |")
        L.append("")
    REPORT.write_text("\n".join(L) + "\n", encoding="utf-8")

    C: list[str] = ["# Phase-3 absorption ledger — concept level", "",
                    "Every meaningful current technical concept of every Bible unit, with its disposition, destination and the TARGET check "
                    "that decided it. Generated from `audit/data/bible/records/*.json`.", ""]
    for u in units:
        rec = recs.get(u["id"])
        if not rec:
            continue
        C += [f"## {u['id']} ({u['kind']})", "", rec.get("summary", ""), ""]
        C += ["| Concept | Section | Disposition | Destination | TARGET check | Evidence |", "|---|---|---|---|---|---|"]
        for c in rec.get("concepts") or []:
            t = c.get("target") or {}
            C.append(f"| {c.get('id')}: {c.get('text', '')[:170].replace('|', '/')} | {c.get('section', '')[:40].replace('|', '/')} | "
                     f"{c.get('disposition')} | {', '.join(f'`{d}`' for d in (c.get('destinations') or [])[:3])} | "
                     f"{t.get('result', '')} | {t.get('evidence', c.get('note', ''))[:110].replace('|', '/')} |")
        C.append("")
    CONCEPTS.write_text("\n".join(C) + "\n", encoding="utf-8")
    print(f"wrote {REPORT.relative_to(ROOT)} ({REPORT.stat().st_size // 1024} KiB) and {CONCEPTS.relative_to(ROOT)} "
          f"({CONCEPTS.stat().st_size // 1024} KiB); {len(done)}/{total} units done")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("--units", nargs="*")
    c.add_argument("--final", action="store_true")
    c.add_argument("--quiet", action="store_true")
    p = sub.add_parser("progress")
    p.add_argument("--units", nargs="*")
    sub.add_parser("render")
    args = ap.parse_args()
    if args.cmd == "check":
        return run_check(args.units, args.final, args.quiet)
    if args.cmd == "progress":
        return cmd_progress(args)
    return cmd_render(args)


if __name__ == "__main__":
    sys.exit(main())
