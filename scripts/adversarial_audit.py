#!/usr/bin/env python3
"""Independent adversarial checks for the Phase-3 result (written without reusing bible_inventory.py / bible_ledger.py).

    adversarial_audit.py graph      # re-derive the Bible LaTeX inclusion graph from main.tex and compare it with audit/data/bible/units.json
    adversarial_audit.py anchors [--strict|--repair]   # ledger destinations: page + fragment exist, tokens occur at page level (error) and inside the cited anchor section (counted); --repair re-points imprecise anchors
    adversarial_audit.py issues     # data/known-issues.json <-> detail pages <-> hubs: counts, orphans, facts, evidence flags, unreviewed duplicate candidates
    adversarial_audit.py counts [--write]   # the published quantities between <!-- counts:begin/end --> in audit/phase3-adversarial-audit.md: --write regenerates, default checks
    adversarial_audit.py all        # graph + anchors + issues + counts (what scripts/validate_all.sh runs)

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
SOURCE_GRAPH = ROOT / "audit" / "data" / "adversarial" / "source-graph.json"
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
    # every other Bible document must be an auxiliary unit or carry an explicit non-canonical disposition
    import fnmatch
    aux = {a["path"] for a in json.loads(UNITS.read_text(encoding="utf-8"))["aux"]}
    dispositioned = [d["path"] for d in json.loads(SOURCE_GRAPH.read_text(encoding="utf-8"))["non_canonical"]] if SOURCE_GRAPH.exists() else []
    stray = []
    for p in sorted(list(BIBLE.glob("*")) + list((BIBLE / "audit").glob("*")) + list((BIBLE / "latex").glob("*")) + list((BIBLE / "latex" / "book").glob("*"))):
        rel = p.relative_to(BIBLE).as_posix()
        if p.is_dir() and rel not in ("audit", "latex", "docs", "tools", "build"):
            continue
        if p.is_dir() or rel.startswith(".") or rel in aux or rel in mine or ("latex/book/" + Path(rel).name) in mine:
            continue
        if rel in ("latex/common", "latex/book/chapters", "latex/book/figures", "latex/book/front", "latex/book/images", "latex/book/common"):
            continue
        if not any(fnmatch.fnmatch(rel, d) or rel == d for d in dispositioned):
            stray.append(rel)
    for rel in stray:
        errs.append(f"Bible file is neither an audited unit nor dispositioned as non-canonical: {rel} (add it to audit/data/adversarial/source-graph.json with a reason)")
    for e in errs:
        print("ERROR", e)
    print(f"graph: {len(mine)} reachable TeX files = {len(mine & theirs)} units + {len(mine & structural)} structural (main.tex, preamble); "
          f"{len(aux)} aux units; {len(dispositioned)} dispositioned non-canonical entries; errors {len(errs)}")
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


def _best_anchor(base: str, tokens: list[str]) -> str | None:
    """The id on a page whose own section holds every token, preferring the smallest such section."""
    section(base, "")
    t = _trees.get(base)
    if t is None:
        return None
    best: tuple[int, str] | None = None
    whole = len(section(base, "") or "")
    for frag, node in t.ids.items():
        if node.tag in ("main", "article", "body", "html", "nav", "header", "footer"):
            continue                       # a container holds every token and says nothing about where the concept lives
        sec = section(base, frag)
        if sec and whole and len(sec) > 0.6 * whole:
            continue
        if sec and all(_norm(x) in sec for x in tokens) and (best is None or len(sec) < best[0]):
            best = (len(sec), frag)
    return best[1] if best else None


def repair_anchors() -> int:
    """Precision repair of ledger destinations whose tokens sit on the page but outside the cited anchor. Single destination: re-point it to the smallest
    anchor section that holds all tokens. Several destinations: add that anchor (nothing is removed). Concepts with no such anchor are left alone."""
    changed = left = 0
    for p in sorted(RECORDS.glob("*.json")):
        rec = json.loads(p.read_text(encoding="utf-8"))
        dirty = False
        for c in rec.get("concepts") or []:
            dests, toks = c.get("destinations") or [], c.get("tokens") or []
            if not dests or not toks:
                continue
            blobs = []
            for d in dests:
                base, _, frag = d.partition("#")
                blobs.append(section(base, frag) if frag else section(base, ""))
            if any(b is None for b in blobs):
                continue
            ab = " ".join(blobs)
            missing = [t for t in toks if _norm(t) not in ab]
            if not missing:
                continue
            fixed = None
            for d in dests:
                base = d.partition("#")[0]
                frag = _best_anchor(base, toks)
                if frag:
                    fixed = f"{base}#{frag}"
                    break
            if not fixed:
                left += 1
                continue
            if len(dests) == 1:
                c["destinations"] = [fixed]
            elif fixed not in dests:
                c["destinations"] = dests + [fixed]
            dirty = True
            changed += 1
        if dirty:
            p.write_text(json.dumps(rec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"anchors --repair: {changed} concept destination(s) made precise; {left} left (no single anchor section holds every token)")
    return 0


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

# ---------------------------------------------------------------------------------------------
# issues: the canonical JSON, the generated pages and the hubs must agree; summary numbers are derived, never typed
# ---------------------------------------------------------------------------------------------
PUBLIC = ROOT / "data" / "known-issues.json"
DUP_REVIEW = ROOT / "audit" / "data" / "adversarial" / "duplicate-review.json"
_LABEL = {"bug": "Bug", "functional-gap": "Functional gap", "platform-limitation": "Platform limitation", "verification-gap": "Verification gap"}
_GROUP = {"bug": "bugs", "functional-gap": "gaps", "platform-limitation": "limitations", "verification-gap": "verification-gaps"}


def issue_counts(issues: list[dict]) -> dict:
    """Every published quantity, recomputed from the entries."""
    sev = Counter(i["severity"] for i in issues if i["class"] == "bug")
    return {"total": len(issues), "by_class": dict(Counter(i["class"] for i in issues)), "bug_severity": {k: sev.get(k, 0) for k in ("high", "medium", "low")},
            "status": dict(Counter(i["status"] for i in issues)), "tests_present": sum(1 for i in issues if i.get("tests_present"))}


def _facts(page_html: str) -> dict[str, str]:
    m = re.search(r'<dl class="issue-facts">(.*?)</dl>', page_html, re.S)
    out = {}
    for k, v in re.findall(r"<div><dt>(.*?)</dt><dd>(.*?)</dd></div>", m.group(1) if m else "", re.S):
        out[k] = html.unescape(re.sub(r"<[^>]+>", "", v)).strip()
    return out


def _similarity_pairs(issues: list[dict]) -> list[tuple[float, str, str]]:
    """TF-IDF cosine over title + summary + contract, restricted to entries sharing a source path; the generator never sees this, a future duplicate would."""
    import math
    stop = set("the a an of to in on for and or is are was be by with as at it its this that from not no does do when which than then into if can may must should would could has have had but only also any all each".split())
    docs = {i["id"]: [w for w in re.findall(r"[a-z_][a-z0-9_:]{2,}", (i["title"] + " " + i["summary"] + " " + i["public_contract"]).lower()) if w not in stop] for i in issues}
    df = Counter(w for d in docs.values() for w in set(d))
    n = len(docs)
    vec = {k: {w: (1 + math.log(c)) * math.log(n / df[w]) for w, c in Counter(d).items()} for k, d in docs.items()}
    norm = {k: math.sqrt(sum(x * x for x in v.values())) or 1.0 for k, v in vec.items()}
    srcs = {i["id"]: set(i["sources"]) for i in issues}
    out = []
    ids = sorted(docs)
    for a_i, a in enumerate(ids):
        for b in ids[a_i + 1:]:
            if not srcs[a] & srcs[b]:
                continue
            c = sum(x * vec[b].get(w, 0) for w, x in vec[a].items()) / (norm[a] * norm[b])
            if c >= 0.5:
                out.append((round(c, 2), a, b))
    return sorted(out, reverse=True)


def cmd_issues() -> int:
    errs: list[str] = []
    pub = json.loads(PUBLIC.read_text(encoding="utf-8"))
    issues = pub["issues"]
    cnt = issue_counts(issues)
    if pub.get("counts") != cnt["by_class"]:
        errs.append(f"index counts {pub.get('counts')} != recomputed {cnt['by_class']}")
    ids = Counter(i["id"] for i in issues)
    errs += [f"duplicate id {k}" for k, m in ids.items() if m > 1]
    on_disk = {p.relative_to(ROOT).as_posix() for g in _GROUP.values() for p in (ROOT / "known-issues" / g).glob("*.html") if p.name != "index.html"}
    want = {i["detail"] for i in issues}
    errs += [f"missing detail page {p}" for p in sorted(want - on_disk)]
    errs += [f"orphan detail page (no JSON entry) {p}" for p in sorted(on_disk - want)]
    for i in issues:
        pg = ROOT / i["detail"]
        if not pg.is_file():
            continue
        f = _facts(pg.read_text(encoding="utf-8"))
        if f.get("Identifier") != i["id"]:
            errs.append(f"{i['id']}: page identifier {f.get('Identifier')!r}")
        if f.get("Category") != _LABEL[i["class"]]:
            errs.append(f"{i['id']}: page category {f.get('Category')!r} != {_LABEL[i['class']]!r}")
        if not f.get("Status", "").lower().startswith(i["status"]):
            errs.append(f"{i['id']}: page status {f.get('Status')!r} != {i['status']}")
        want_sev = i["severity"].capitalize() if i["severity"] != "n/a" else None
        got_sev = f.get("Severity", "").split(" ")[0] or None
        if want_sev != got_sev:
            errs.append(f"{i['id']}: page severity {got_sev!r} != {want_sev!r}")
        want_tests = "Yes" if i.get("tests_present") else "None"
        if not f.get("Tests touching this area", "").startswith(want_tests):
            errs.append(f"{i['id']}: page test flag {f.get('Tests touching this area')!r} != {want_tests}")
        body = pg.read_text(encoding="utf-8")
        target = (ROOT / "cnahead").read_text(encoding="utf-8").strip()
        if target not in f.get("Verified against", "") or i.get("verified_against") != target:
            errs.append(f"{i['id']}: page or index does not name the TARGET commit {target[:8]}")
        for sp in i["sources"]:
            if f"/{target}/{sp}" not in body:
                errs.append(f"{i['id']}: source path {sp} is not linked to the TARGET commit on the page")
        if ("tests exist" in body) != bool(i.get("tests_present")):
            errs.append(f"{i['id']}: the evidence callout says {'tests exist' if 'tests exist' in body else 'no tests'} but tests_present is {i.get('tests_present')}")
        if i["confidence"] == "verified-by-reading" and re.search(r"Reproduced: executed", body):
            errs.append(f"{i['id']}: source-verified entry shows an executed-evidence label")
    for cls, g in _GROUP.items():
        hub = (ROOT / "known-issues" / g / "index.html").read_text(encoding="utf-8")
        listed = re.findall(r'<td><a href="[^"]+"><code>(CNA-[A-Z]+-\d{3})</code></a></td>', hub)
        want_ids = sorted(i["id"] for i in issues if i["class"] == cls)
        if sorted(listed) != want_ids:
            errs.append(f"hub {g}: lists {len(listed)} entries, JSON has {len(want_ids)} (or the ids differ)")
        m = re.search(r'<h2 id="entries">(\d+) entries</h2>', hub)
        if want_ids and (not m or int(m.group(1)) != len(want_ids)):
            errs.append(f"hub {g}: heading says {m.group(1) if m else '?'} entries, JSON has {len(want_ids)}")
    ov = (ROOT / "known-issues" / "index.html").read_text(encoding="utf-8")
    for cls, label in _LABEL.items():
        m = re.search(r'<a href="[^"]*/index.html">' + re.escape(label) + r"</a></td><td>(\d+)</td>", ov)
        if not m or int(m.group(1)) != cnt["by_class"].get(cls, 0):
            errs.append(f"overview: {label} count {m.group(1) if m else '?'} != {cnt['by_class'].get(cls, 0)}")
    reviewed = set()
    if DUP_REVIEW.exists():
        for rec in json.loads(DUP_REVIEW.read_text(encoding="utf-8")).get("pairs", []):
            reviewed.add(tuple(sorted(rec["ids"])))
    unreviewed = [(c, a, b) for c, a, b in _similarity_pairs(issues) if (a, b) not in reviewed]
    for c, a, b in unreviewed:
        errs.append(f"duplicate candidate not reviewed (cosine {c}, shared source path): {a} ~ {b} - decide it in audit/data/adversarial/duplicate-review.json")
    for e in errs:
        print("ERROR", e)
    print(f"issues: {cnt['total']} entries {cnt['by_class']}, bug severity {cnt['bug_severity']}, status {cnt['status']}, with tests {cnt['tests_present']}; errors {len(errs)}")
    return 1 if errs else 0


# ---------------------------------------------------------------------------------------------
# counts: the numbers a report quotes are generated from the canonical data, never typed
# ---------------------------------------------------------------------------------------------
LEDGER = ROOT / "audit" / "phase3-adversarial-audit.md"
COUNTS_BEGIN, COUNTS_END = "<!-- counts:begin -->", "<!-- counts:end -->"


def counts_block() -> str:
    pub = json.loads(PUBLIC.read_text(encoding="utf-8"))
    issues = pub["issues"]
    c = issue_counts(issues)
    conf = Counter(i["confidence"] for i in issues)
    sub = Counter(i["subsystem"] for i in issues)
    disp = json.loads((ROOT / "audit" / "data" / "bible" / "issues" / "dispositions.json").read_text(encoding="utf-8"))
    trail = disp.get("adversarial_audit", {})
    rev_dir = ROOT / "audit" / "data" / "adversarial" / "issue-reviews"
    reviewed = 0
    verdicts: Counter = Counter()
    if rev_dir.exists():
        for f in sorted(rev_dir.glob("*.jsonl")):
            for line in f.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    reviewed += 1
                    verdicts[json.loads(line)["verdict"]] += 1
    dis_dir = ROOT / "audit" / "data" / "adversarial" / "dismissal-reviews"
    dreviewed = 0
    dverdicts: Counter = Counter()
    if dis_dir.exists():
        for f in sorted(dis_dir.glob("*.jsonl")):
            for line in f.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    dreviewed += 1
                    dverdicts[json.loads(line)["verdict"]] += 1
    ur_dir = ROOT / "audit" / "data" / "adversarial" / "unit-reviews"
    status: Counter = Counter()
    ftypes: Counter = Counter()
    tot: Counter = Counter()
    seen_units: list[str] = []
    if ur_dir.exists():
        for f in sorted(ur_dir.glob("*.json")):
            for u in json.loads(f.read_text(encoding="utf-8")).get("units", []):
                seen_units.append(u["unit"])
                status[u["status"]] += 1
                for fd in u.get("findings", []):
                    ftypes[fd["type"]] += 1
                for k, sub in (("residuals", ("reviewed", "lost")), ("dropped", ("reviewed", "false_drop", "restore_issue")), ("corrections", ("verified", "disagree"))):
                    for fld in sub:
                        tot[f"{k}.{fld}"] += (u.get(k) or {}).get(fld, 0)
    bc = c["by_class"]
    lines = [COUNTS_BEGIN, "",
             f"Generated by `python3 scripts/adversarial_audit.py counts --write` from `data/known-issues.json` and `audit/data/adversarial/`; `validate_all.sh` fails when it is stale.", "",
             "| Quantity | Value |", "|---|---|",
             f"| Published entries | **{c['total']}** = {bc.get('bug', 0)} bugs · {bc.get('functional-gap', 0)} functional gaps · {bc.get('platform-limitation', 0)} platform limitations · {bc.get('verification-gap', 0)} verification gaps |",
             f"| Bug severity | **{c['bug_severity']['high']} high · {c['bug_severity']['medium']} medium · {c['bug_severity']['low']} low** |",
             f"| Status | {c['status'].get('open', 0)} open · {c['status'].get('narrowed', 0)} narrowed |",
             f"| Evidence basis | " + " · ".join(f"{k} {v}" for k, v in sorted(conf.items())) + " |",
             f"| Entries with a test touching the area | {c['tests_present']} of {c['total']} |",
             f"| Subsystems | " + " · ".join(f"{k} {v}" for k, v in sorted(sub.items(), key=lambda kv: -kv[1])) + " |",
             f"| Audit operations recorded in `dispositions.json` | folded {len(trail.get('folded', {}))} · retired {len(trail.get('retired', {}))} · reclassified {len(trail.get('reclassified', {}))} · added {len(trail.get('added', {}))} |",
             f"| Independent issue reviews ingested | {reviewed} of {c['total']} entries; " + (", ".join(f"{k} {v}" for k, v in sorted(verdicts.items())) or "none") + " |",
             f"| Independent dismissal reviews ingested | {dreviewed} of 121; " + (", ".join(f"{k} {v}" for k, v in sorted(dverdicts.items())) or "none") + " |",
             f"| Independent Bible-unit reviews ingested | {len(seen_units)} of 98 canonical text units; " + (", ".join(f"{k} {v}" for k, v in sorted(status.items())) or "none")
             + f"; findings {sum(ftypes.values())} (" + (", ".join(f"{k} {v}" for k, v in sorted(ftypes.items())) or "none") + ") |",
             f"| Unit-review evidence | residual paragraphs/identifiers reviewed {tot['residuals.reviewed']} (lost-useful {tot['residuals.lost']}); dropped dispositions reviewed {tot['dropped.reviewed']} "
             f"(false drops {tot['dropped.false_drop']}, restore-issue {tot['dropped.restore_issue']}); ledger TARGET corrections re-derived {tot['corrections.verified']} (disagreements {tot['corrections.disagree']}) |", "",
             COUNTS_END]
    return "\n".join(lines)


def cmd_counts(write: bool) -> int:
    text = LEDGER.read_text(encoding="utf-8")
    if COUNTS_BEGIN not in text or COUNTS_END not in text:
        print(f"counts: markers missing in {LEDGER.relative_to(ROOT)}")
        return 1
    head, rest = text.split(COUNTS_BEGIN, 1)
    _old, tail = rest.split(COUNTS_END, 1)
    new = head + counts_block() + tail
    if write:
        LEDGER.write_text(new, encoding="utf-8")
        print("counts: wrote", LEDGER.relative_to(ROOT))
        return 0
    if new != text:
        print("ERROR counts: the generated block in audit/phase3-adversarial-audit.md is stale; run scripts/adversarial_audit.py counts --write")
        return 1
    print("counts: ledger block is current")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("graph")
    a = sub.add_parser("anchors")
    a.add_argument("--strict", action="store_true", help="treat anchor-precision misses as errors")
    a.add_argument("--repair", action="store_true", help="re-point imprecise ledger anchors (rewrites audit/data/bible/records)")
    sub.add_parser("issues")
    cn = sub.add_parser("counts")
    cn.add_argument("--write", action="store_true")
    sub.add_parser("all")
    args = ap.parse_args()
    if args.cmd == "graph":
        return cmd_graph()
    if args.cmd == "anchors":
        return repair_anchors() | cmd_anchors(args.strict) if args.repair else cmd_anchors(args.strict)
    if args.cmd == "issues":
        return cmd_issues()
    if args.cmd == "counts":
        return cmd_counts(args.write)
    return cmd_graph() | cmd_anchors() | cmd_issues() | cmd_counts(False)


if __name__ == "__main__":
    sys.exit(main())
