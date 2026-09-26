#!/usr/bin/env python3
"""Known Issues pipeline (Phase 3): validate, merge, generate.

    known_issues.py check [--pkg B1 ...]     # validate verified-<pkg>.json against its candidates and TARGET (agents run this)
    known_issues.py merge                    # merge every verified-*.json, allocate stable ids -> issues-source.json + dispositions.json
    known_issues.py build                    # generate data/known-issues.json and every known-issues/** page from issues-source.json
    known_issues.py validate                 # whole-system validation of data/known-issues.json against pages, sources and rules (no writes)

Files
  audit/data/bible/issues/candidates-<pkg>.json   candidates assigned to a verification package (scripts/issues_candidates.py)
  audit/data/bible/issues/verified-<pkg>.json     authored: dispositions of EVERY candidate + public entries (see audit/data/phase3-issues-guide.md)
  audit/data/bible/issues/issues-source.json      merged public entries with final stable ids (narrative HTML lives here)
  audit/data/bible/issues/dispositions.json       merged non-public audit trail (fixed / obsolete / not-a-bug / insufficient, with evidence)
  data/known-issues.json                          the public machine-readable current issue index (generated)
  known-issues/**                                 detail pages, category hubs and the overview (generated)

Only issues that EXIST at TARGET are ever published: the index has no `fixed` status and the validator refuses one.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

ROOT = Path(__file__).resolve().parent.parent
ISS = ROOT / "audit" / "data" / "bible" / "issues"
SOURCE = ISS / "issues-source.json"
DISPO = ISS / "dispositions.json"
PUBLIC = ROOT / "data" / "known-issues.json"
TARGET = (ROOT / "cnahead").read_text(encoding="utf-8").strip()
TARGET_SHORT = TARGET[:8]
TODAY = "2026-09-25"

CLASSES = {
    "bug": {"group": "bugs", "prefix": "CNA-BUG", "label": "Bug"},
    "functional-gap": {"group": "gaps", "prefix": "CNA-GAP", "label": "Functional gap"},
    "platform-limitation": {"group": "limitations", "prefix": "CNA-PLAT", "label": "Platform limitation"},
    "verification-gap": {"group": "verification-gaps", "prefix": "CNA-VGAP", "label": "Verification gap"},
}
CLASS_DEF = {
    "bug": "Existing behaviour violates an intended or documented contract.",
    "functional-gap": "Functionality is intentionally or currently incomplete or unsupported; nothing violates a contract, the contract is narrower than one might expect.",
    "platform-limitation": "A host, platform or toolchain constraint makes behaviour differ or be unavailable.",
    "verification-gap": "An implementation exists, but the evidence that it behaves correctly is insufficient.",
}
CLASSIFICATIONS = {"STILL EXISTS", "PARTIALLY FIXED", "PROVEN FIXED", "OBSOLETE", "NOT A BUG", "INSUFFICIENT EVIDENCE"}
PUBLISHED = {"STILL EXISTS", "PARTIALLY FIXED"}
SUBSYSTEMS = ["Math & geometry", "Core & runtime", "Graphics & renderers", "Content & XNB/CNB/CNJ", "Models & glTF", "Input", "Audio & media", "Storage",
              "Networking & gamer services", "Platforms", "Build & CI", "Testing & evidence", "Diagnostics & Inspector", "C API & bindings",
              "Documentation & release tooling"]
STATUSES = {"open", "narrowed"}
SEVERITIES = {"high", "medium", "low", "n/a"}
CONFIDENCES = {"reproduced", "recorded-by-cna", "verified-by-reading", "strong", "probable"}
# What each confidence value claims, in the words the pages use.  Source-verified is never allowed to imply an execution.
CONFIDENCE_LABEL = {
    "verified-by-reading": "Source-verified: read at TARGET, not executed",
    "reproduced": "Reproduced: executed for this entry (the Evidence section names exactly what was run)",
    "recorded-by-cna": "Recorded by CNA: CNA's own recorded run, not repeated here",
    "strong": "Inferred (strong): follows from the code, but the behaviour was not run",
    "probable": "Inferred (probable): depends on a platform or toolchain step nobody executed",
}
CONFIDENCE_SHORT = {"verified-by-reading": "source-verified", "reproduced": "reproduced", "recorded-by-cna": "recorded by CNA",
                    "strong": "inferred (strong)", "probable": "inferred (probable)"}
EVIDENCE_LEVELS = {"verified-by-reading": ["source-verified"], "reproduced": ["source-verified", "executed"],
                   "recorded-by-cna": ["source-verified", "recorded-by-cna"], "strong": ["source-verified", "inferred"],
                   "probable": ["source-verified", "inferred"]}
# An entry's tests_current text always exists; whether a test *touches the affected area* is a separate fact.  An explicit
# `tests_present` (set from the independent review) wins; the fallback reads the opening of the text.
_NO_TEST_RX = re.compile(r"^\s*(?:<[^>]+>\s*)*(?:none\b|no (?:test|tests|unit test|regression test|existing test|gate|check|coverage)\b|nothing (?:covers|tests|asserts|exercises|checks)\b|not covered\b|untested\b)", re.I)


def has_tests(it: dict) -> bool:
    if isinstance(it.get("tests_present"), bool):
        return it["tests_present"]
    text = it.get("tests_current") or ""
    return bool(text) and not _NO_TEST_RX.match(text)
REQUIRED = ["cand_ids", "id", "class", "title", "summary", "subsystem", "status", "severity", "confidence", "public_contract", "expected", "actual",
            "sources", "evidence", "tests_current", "regression_test", "blast_radius", "related", "origin"]
HTML_FIELDS = ["expected", "actual", "evidence", "reproduction", "tests_current", "regression_test", "blast_radius", "workaround"]
LAYER_KEYS = {"guide", "architecture", "internals", "maintainer", "tests", "reference", "deep", "issues"}
ID_RX = re.compile(r"^CNA-(BUG|GAP|PLAT|VGAP)-(\d{3})$")


def detail_path(issue_id: str, cls: str) -> str:
    return f"known-issues/{CLASSES[cls]['group']}/{issue_id.lower()}.html"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def retired_rx():
    import check_retired_renderers as R
    retired = R.derive(R.BASE_TREE, R.TARGET_TREE)
    strong = sorted(i for i in retired if i not in R.WORDS)
    return re.compile(r"(?<![A-Za-z0-9_])(" + "|".join(map(re.escape, strong)) + r")(?![A-Za-z0-9_])", re.I)


# ---------------------------------------------------------------------------------------------
# validation of one verified file
# ---------------------------------------------------------------------------------------------
def check_issue(it: dict, files: set[str], errs: list[str], where: str, known_page, expand) -> None:
    for f in REQUIRED:
        if f == "cand_ids" and it.get("cand_ids") == [] and str(it.get("origin", "")).lower().startswith("new finding"):
            continue  # a defect found while verifying, with no earlier candidate
        if f not in it or it[f] in (None, "", []):
            if f in ("related",) and it.get(f) == {}:
                errs.append(f"{where}: related must link at least one page")
            elif f not in ("origin",) or f not in it:
                errs.append(f"{where}: missing required field {f}")
    cls = it.get("class")
    if cls not in CLASSES:
        errs.append(f"{where}: class {cls!r} not in {sorted(CLASSES)}")
    if it.get("subsystem") not in SUBSYSTEMS:
        errs.append(f"{where}: subsystem {it.get('subsystem')!r} not in the fixed list")
    if it.get("status") not in STATUSES:
        errs.append(f"{where}: status {it.get('status')!r} not in {sorted(STATUSES)} (fixed items are never published)")
    if it.get("severity") not in SEVERITIES:
        errs.append(f"{where}: severity must be one of {sorted(SEVERITIES)}")
    if cls == "bug" and it.get("severity") == "n/a":
        errs.append(f"{where}: a bug needs a severity judgement")
    if it.get("confidence") not in CONFIDENCES:
        errs.append(f"{where}: confidence must be one of {sorted(CONFIDENCES)}")
    if _MARKUP_RX.search(it.get("public_contract") or ""):
        errs.append(f"{where}: public_contract is a plain-text field; markup or entities found (it is escaped on the page and would show literally)")
    for s in it.get("sources") or []:
        p = s.get("path", "") if isinstance(s, dict) else ""
        if p not in files:
            errs.append(f"{where}: source path absent at TARGET: {p!r}")
        if isinstance(s, dict) and re.search(r"[:#]L?\d+", s.get("note", "") + p):
            errs.append(f"{where}: no line numbers in sources (name the function): {s}")
    for k, links in (it.get("related") or {}).items():
        if k not in LAYER_KEYS:
            errs.append(f"{where}: related key {k!r} invalid")
        for link in links:
            base = link[0].split("#", 1)[0]
            if not (base.startswith("http") or known_page(base)):
                errs.append(f"{where}: related page does not exist: {link[0]}")
    for f in HTML_FIELDS:
        v = it.get(f)
        if v:
            expand(v, where + "/" + f, errs)
    if it.get("id") and not (ID_RX.match(it["id"]) or it["id"].startswith("NEW-")):
        errs.append(f"{where}: id must be CNA-(BUG|GAP|PLAT|VGAP)-nnn or a temporary NEW-<pkg>-<nn>")
    if ID_RX.match(it.get("id", "")):
        want = {"BUG": "bug", "GAP": "functional-gap", "PLAT": "platform-limitation", "VGAP": "verification-gap"}[ID_RX.match(it["id"]).group(1)]
        if want != cls:
            errs.append(f"{where}: id prefix implies class {want}, entry says {cls}")
    if len(it.get("summary", "")) > 260:
        errs.append(f"{where}: summary must be one sentence (<= 260 chars)")


def cmd_check(args: argparse.Namespace) -> int:
    import site_dev as SD
    import site_deep  # noqa: F401  (page index incl. deep/known-issue pages)
    files, _dirs = SD.target_tree()
    rx = retired_rx()
    pkgs = args.pkg or sorted(p.stem.split("-")[1] for p in ISS.glob("verified-*.json"))
    rc = 0
    for pkg in pkgs:
        vf = ISS / f"verified-{pkg}.json"
        cf = ISS / f"candidates-{pkg}.json"
        errs: list[str] = []
        if not vf.exists():
            print(f"{pkg}: no verified-{pkg}.json yet")
            rc = 1
            continue
        v, c = load(vf), load(cf)
        cands = {x["cand"]: x for x in c["candidates"]}
        disp = v.get("dispositions") or []
        seen = Counter(d.get("cand") for d in disp)
        for k in cands:
            if seen[k] != 1:
                errs.append(f"{pkg}: candidate {k} has {seen[k]} dispositions (need exactly 1)")
        for k in seen:
            if k not in cands:
                errs.append(f"{pkg}: disposition for unknown candidate {k}")
        issue_ids = {i.get("id") for i in v.get("issues") or []}
        if len(issue_ids) != len(v.get("issues") or []):
            errs.append(f"{pkg}: duplicate issue ids")
        resolved: Counter = Counter()
        for d in disp:
            k = d.get("cand")
            cl = d.get("classification")
            if cl not in CLASSIFICATIONS:
                errs.append(f"{pkg}/{k}: classification {cl!r} invalid")
                continue
            if len(d.get("evidence", "")) < 30:
                errs.append(f"{pkg}/{k}: evidence must be substantive (>= 30 chars)")
            if cl in PUBLISHED:
                if d.get("published_as") not in issue_ids:
                    errs.append(f"{pkg}/{k}: {cl} needs published_as pointing at an entry of issues[]")
            elif d.get("published_as") and d["published_as"] not in issue_ids:
                errs.append(f"{pkg}/{k}: published_as {d['published_as']} not in issues[]")
        for it in v.get("issues") or []:
            w = f"{pkg}/{it.get('id')}"
            check_issue(it, files, errs, w, lambda p: SD.known_page(p) or p in site_deep.DM.page_index(),
                        lambda text, where, e: SD.expand_tokens(text, "known-issues/bugs/x.html", e))
            for cid in it.get("cand_ids") or []:
                if cid not in cands:
                    errs.append(f"{w}: cand_ids has unknown candidate {cid}")
                else:
                    resolved[cid] += 1
                    dd = next((d for d in disp if d.get("cand") == cid), None)
                    if dd is None or dd.get("classification") not in PUBLISHED or dd.get("published_as") != it.get("id"):
                        errs.append(f"{w}: candidate {cid} is not dispositioned STILL EXISTS/PARTIALLY FIXED with published_as {it.get('id')}")
                    elif dd["classification"] == "PARTIALLY FIXED" and it.get("status") != "narrowed":
                        errs.append(f"{w}: candidate {cid} is PARTIALLY FIXED, so the entry status must be narrowed")
        for d in disp:
            if d.get("classification") in PUBLISHED and d.get("published_as") and resolved[d["cand"]] == 0:
                errs.append(f"{pkg}/{d['cand']}: published_as {d['published_as']} does not list this candidate in cand_ids")
        blob = json.dumps(v, ensure_ascii=False)
        for m in rx.finditer(blob):
            errs.append(f"{pkg}: retired renderer identity in output: {m.group(0)}")
        counts = Counter(d.get("classification") for d in disp)
        print(f"{pkg}: {len(cands)} candidates, {len(disp)} dispositions {dict(counts)}; published {len(v.get('issues') or [])}; errors {len(errs)}")
        for e in errs:
            print("  ERROR", e)
            rc = 1
    return rc


# ---------------------------------------------------------------------------------------------
# independent adversarial audit: audit/data/bible/issues/patches-adversarial.json
#   {"entries":      {"CNA-BUG-nnn": {"set": {"field": value}, "append": {"field": "<p>..</p>"}}},   field corrections (HTML fields hold HTML); set first, then append
#    "folded":       {"CNA-BUG-226": "CNA-BUG-215"},                                  duplicate folded into its survivor (the survivor keeps its id)
#    "retired":      {"CNA-BUG-nnn": {"classification": "NOT A BUG|PROVEN FIXED|OBSOLETE|INSUFFICIENT EVIDENCE|DUPLICATE", "evidence": "..."}},
#    "reclassified": {"CNA-BUG-nnn": {"class": "functional-gap", "set": {...}}},       a new id in the target class is allocated after every existing one
#    "added":        [{... a full entry with a temporary id NEW-AUDIT-nn and cand_ids of the restored candidates ...}]}
# Every operation runs AFTER the stable ids were allocated, so no surviving entry is ever renumbered and a retired id is never reused.
# ---------------------------------------------------------------------------------------------
def apply_adversarial(issues: list[dict], disp: list[dict], counters: dict[str, int]) -> tuple[list[dict], list[dict], dict, int]:
    path = ISS / "patches-adversarial.json"
    if not path.exists():
        return issues, disp, {}, 0
    adv = load(path)
    trail: dict = {"folded": {}, "retired": {}, "reclassified": {}, "added": {}}
    by = {i["id"]: i for i in issues}

    def need(iid: str, what: str) -> bool:
        if iid not in by:
            print(f"patches-adversarial.json: {what}: unknown entry {iid}")
            return False
        return True

    for iid, spec in (adv.get("entries") or {}).items():
        if not need(iid, "entries"):
            return issues, disp, trail, 1
        by[iid].update(spec.get("set", {}))
        for fld, add in (spec.get("append") or {}).items():
            by[iid][fld] = (by[iid].get(fld) or "") + add
    for src, dst in (adv.get("folded") or {}).items():
        if not (need(src, "folded") and need(dst, "folded")):
            return issues, disp, trail, 1
        s_, d_ = by[src], by[dst]
        d_["cand_ids"] = sorted(set(d_.get("cand_ids") or []) | set(s_.get("cand_ids") or []))
        d_["origin"] = f"{d_.get('origin', '')}; folded with {src} by the adversarial audit"
        d_["evidence"] = (d_.get("evidence") or "") + (f"<p><em>Independently reported as {html.escape(src)} (folded into this entry by the adversarial audit):</em> "
                                                       + html.escape(s_.get("summary", "")) + "</p>")
        have = {x["path"] for x in d_["sources"]}
        d_["sources"] = d_["sources"] + [x for x in s_["sources"] if x["path"] not in have]
        for d in disp:
            if d.get("published_as") == src:
                d["published_as"] = dst
        trail["folded"][src] = dst
        del by[src]
    for iid, spec in (adv.get("retired") or {}).items():
        if not need(iid, "retired"):
            return issues, disp, trail, 1
        if spec["classification"] not in CLASSIFICATIONS - PUBLISHED:
            print(f"patches-adversarial.json: retired {iid}: classification {spec['classification']!r} is not a non-published one")
            return issues, disp, trail, 1
        for d in disp:
            if d.get("published_as") == iid:
                d["classification"] = spec["classification"]
                d["evidence"] = "Retired by the independent adversarial audit: " + spec["evidence"]
                d["adversarial_retired_entry"] = iid
                d["published_as"] = None
        trail["retired"][iid] = {"classification": spec["classification"], "evidence": spec["evidence"]}
        del by[iid]
    for iid, spec in sorted((adv.get("reclassified") or {}).items()):
        if not need(iid, "reclassified"):
            return issues, disp, trail, 1
        e = by.pop(iid)
        cls = spec["class"]
        counters[cls] += 1
        new = f"{CLASSES[cls]['prefix']}-{counters[cls]:03d}"
        e.update(spec.get("set", {}))
        e["class"], e["id"] = cls, new
        e["origin"] = f"{e.get('origin', '')}; reclassified from {iid} by the adversarial audit"
        if cls != "bug":
            e["severity"] = "n/a"
        for d in disp:
            if d.get("published_as") == iid:
                d["published_as"] = new
        by[new] = e
        trail["reclassified"][iid] = new
    for k, e in enumerate(adv.get("added") or []):
        e = dict(e)
        cls = e["class"]
        counters[cls] += 1
        new = f"{CLASSES[cls]['prefix']}-{counters[cls]:03d}"
        tmp = e["id"]
        e["temp_id"], e["id"] = tmp, new
        for cid in e.get("cand_ids") or []:
            for d in disp:
                if d["cand"] == cid:
                    d["classification"] = "PARTIALLY FIXED" if e.get("status") == "narrowed" else "STILL EXISTS"
                    d["published_as"] = new
                    d["evidence"] = "Restored by the independent adversarial audit (earlier dismissal: " + d.get("evidence", "")[:200] + ")"
        by[new] = e
        trail["added"][tmp] = new
    # text written before the final ids were known refers to entries as {{issue:NEW-AUDIT-nn}} (an added entry) or {{issue:CNA-XXX-nnn}} (an id that was folded or reclassified);
    # the reference is resolved here, after allocation, so no later operation can leave a wrong id in the published text
    resolve = {**trail["added"], **trail["reclassified"], **trail["folded"]}
    rx = re.compile(r"\{\{issue:([A-Z0-9-]+)\}\}")

    def sub(x):
        if isinstance(x, str):
            def one(m):
                if m.group(1) not in resolve:
                    raise SystemExit(f"patches-adversarial.json: {{{{issue:{m.group(1)}}}}} does not name an added, reclassified or folded entry")
                return resolve[m.group(1)]
            return rx.sub(one, x)
        if isinstance(x, list):
            return [sub(v) for v in x]
        if isinstance(x, dict):
            return {k: sub(v) for k, v in x.items()}
        return x
    for iid in list(by):
        by[iid] = sub(by[iid])
    return list(by.values()), disp, {k: v for k, v in trail.items() if v}, 0


# ---------------------------------------------------------------------------------------------
# merge
# ---------------------------------------------------------------------------------------------
def build_entries(with_adversarial: bool) -> tuple[list[dict], list[dict], dict, dict, dict] | int:
    """Merge every verified-*.json into public entries with stable ids (merge-map folds, allocation, patches.json), optionally followed by the
    adversarial-audit operations.  Returns (issues, dispositions, remap, counters, audit_trail) or a non-zero exit code.  Pure: writes nothing."""
    packs = sorted(ISS.glob("verified-*.json"))
    if not packs:
        print("no verified-*.json files")
        return 1
    issues: list[dict] = []
    disp: list[dict] = []
    for p in packs:
        v = load(p)
        pkg = v["pkg"]
        for d in v.get("dispositions") or []:
            d = dict(d)
            d["pkg"] = pkg
            disp.append(d)
        for it in v.get("issues") or []:
            it = dict(it)
            it["pkg"] = pkg
            issues.append(it)
    # a candidate must be dispositioned once across packages
    dup = [k for k, n in Counter(d["cand"] for d in disp).items() if n > 1]
    if dup:
        print("duplicate dispositions across packages:", dup)
        return 1
    # cross-package duplicates: audit/data/bible/issues/merge-map.json = {"<folded id>": "<surviving id>", ...}
    mm_path = ISS / "merge-map.json"
    merged: dict[str, str] = load(mm_path) if mm_path.exists() else {}
    if merged:
        by_id = {i["id"]: i for i in issues}
        for src, dst in merged.items():
            if src not in by_id or dst not in by_id:
                print(f"merge-map: unknown id {src!r} or {dst!r}")
                return 1
            s, d_ = by_id[src], by_id[dst]
            d_["cand_ids"] = sorted(set(d_.get("cand_ids") or []) | set(s.get("cand_ids") or []))
            d_["origin"] = f"{d_.get('origin', '')}; merged with {src}"
            have = {x["path"] for x in d_["sources"]}
            d_["sources"] = d_["sources"] + [x for x in s["sources"] if x["path"] not in have]
            d_["evidence"] = (d_.get("evidence") or "") + ("<p><em>Independently observed as a separate finding (merged):</em> "
                              + esc(s["summary"]) + "</p>")
        issues = [i for i in issues if i["id"] not in merged]
        for d in disp:
            if d.get("published_as") in merged:
                d["published_as"] = merged[d["published_as"]]
    used = {i["id"] for i in issues if ID_RX.match(i["id"])}
    counters: dict[str, int] = {}
    for cls, spec in CLASSES.items():
        nums = [int(ID_RX.match(i).group(2)) for i in used if i.startswith(spec["prefix"])]
        counters[cls] = max(nums + [62 if cls == "bug" else 0])
    remap: dict[str, str] = {}

    def order_key(it: dict) -> tuple:
        mm2 = re.match(r"NEW-B(\d+)-(\d+)", it["id"])
        return (SUBSYSTEMS.index(it["subsystem"]), int(mm2.group(1)) if mm2 else 0, int(mm2.group(2)) if mm2 else 0)

    # final ids are allocated in subsystem order (then package, then sequence) so related entries get neighbouring numbers
    for it in sorted((i for i in issues if i["id"].startswith("NEW-")), key=order_key):
        cls = it["class"]
        counters[cls] += 1
        new = f"{CLASSES[cls]['prefix']}-{counters[cls]:03d}"
        remap[it["id"]] = new
        it["temp_id"] = it["id"]
        it["id"] = new
    # folded entries point at their survivor's final id
    for src, dst in merged.items():
        remap[src] = remap.get(dst, dst)
    for d in disp:
        if d.get("published_as") in remap:
            d["published_as"] = remap[d["published_as"]]

    tmp_rx = re.compile(r"NEW-B\d+-\d+")

    def fix(v):
        if isinstance(v, str):
            return tmp_rx.sub(lambda m_: remap.get(m_.group(0), m_.group(0)), v)
        if isinstance(v, list):
            return [fix(x) for x in v]
        if isinstance(v, dict):
            return {k: fix(x) for k, x in v.items()}
        return v
    issues = [fix(i) for i in issues]
    # orchestrator patches (QA corrections and wording fixes): audit/data/bible/issues/patches.json
    #   {"global_replace": [["old", "new"], ...], "entries": {"CNA-BUG-nnn": {"set": {"field": "text"}}}}
    pp = ISS / "patches.json"
    if pp.exists():
        patches = load(pp)
        by = {i["id"]: i for i in issues}
        for old_s, new_s in patches.get("global_replace", []):
            issues = [json.loads(json.dumps(i).replace(json.dumps(old_s)[1:-1], json.dumps(new_s)[1:-1])) for i in issues]
        by = {i["id"]: i for i in issues}
        for iid, spec in (patches.get("entries") or {}).items():
            if iid not in by:
                print(f"patches.json: unknown entry {iid}")
                return 1
            by[iid].update(spec.get("set", {}))
        # entries refuted by the adversarial QA review: unpublished; their candidates become NOT A BUG with the QA evidence
        refuted = patches.get("refuted", {})
        if refuted:
            issues = [i for i in issues if i["id"] not in refuted]
            for d in disp:
                if d.get("published_as") in refuted:
                    d["classification"] = "NOT A BUG"
                    d["evidence"] = "Refuted by the independent QA review: " + refuted[d["published_as"]]
                    d["qa_refuted_entry"] = d["published_as"]
                    d["published_as"] = None
    audit_trail: dict = {}
    if with_adversarial:
        issues, disp, audit_trail, rc = apply_adversarial(issues, disp, counters)
        if rc:
            return rc
    for i in issues:                                   # public_contract is a plain-text field (the page escapes it); 36 Phase-3 entries carried <code> markup that rendered literally
        i["public_contract"] = plain_text(i.get("public_contract"))
    return issues, disp, remap, counters, audit_trail


def cmd_merge(_: argparse.Namespace) -> int:
    built = build_entries(True)
    if isinstance(built, int):
        return built
    issues, disp, remap, _counters, audit_trail = built
    ids = Counter(i["id"] for i in issues)
    bad = [k for k, n in ids.items() if n > 1]
    if bad:
        print("duplicate public ids:", bad)
        return 1
    issues.sort(key=lambda i: (list(CLASSES).index(i["class"]), i["id"]))
    SOURCE.write_text(json.dumps({"target": TARGET, "issues": issues}, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    out = {"target": TARGET, "dispositions": disp, "remapped_temp_ids": remap}
    if audit_trail:
        out["adversarial_audit"] = audit_trail
    DISPO.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"merged {len(issues)} public issue(s) and {len(disp)} disposition(s); {len(remap)} temp ids remapped")
    return 0


# ---------------------------------------------------------------------------------------------
# generation
# ---------------------------------------------------------------------------------------------
def esc(s: str) -> str:
    return html.escape(s, quote=True)


_MARKUP_RX = re.compile(r"</?(?:code|em|strong|a|p|ul|li|br)\b[^>]*>|&(?:lt|gt|amp|quot|#\d+);|\{\{src")


def plain_text(s: str | None) -> str:
    """Markup-free text for the plain-text fields (public_contract): tags removed, entities decoded."""
    return html.unescape(re.sub(r"</?(?:code|em|strong|a|p|ul|li|br)\b[^>]*>", "", s or "")).strip()


def issue_pages(issues: list[dict] | None = None) -> list[dict]:
    """Manifest records for the detail pages (consumed by deep_manifest.all_pages)."""
    if issues is None:
        if not PUBLIC.exists():
            return []
        issues = load(PUBLIC)["issues"]
    out = []
    for it in issues:
        g = CLASSES[it["class"]]["group"]
        n = int(it["id"].rsplit("-", 1)[1])
        out.append({"path": it["detail"], "title": f"{it['id']}: {it['title']}", "label": it["id"], "group": g, "order": n, "kind": "issue"})
    return out


def public_entry(it: dict) -> dict:
    return {
        "id": it["id"], "class": it["class"], "title": it["title"], "summary": it["summary"], "subsystem": it["subsystem"],
        "status": it["status"], "severity": it["severity"], "confidence": it["confidence"], "tests_present": has_tests(it), "public_contract": it["public_contract"],
        "verified_against": TARGET, "detail": detail_path(it["id"], it["class"]),
        "sources": [s["path"] for s in it["sources"]],
        "related": sorted({l[0].split("#")[0] for ls in it["related"].values() for l in ls}),
    }


def page_fragment(it: dict) -> tuple[dict, str]:
    def block(title: str, ident: str, content: str | None) -> str:
        return f'<h2 id="{ident}">{title}</h2>\n{content}\n' if content else ""

    def para(text: str | None) -> str | None:
        if not text:
            return None
        return text if re.match(r"\s*<", text) else f"<p>{text}</p>"

    cls = CLASSES[it["class"]]
    status_txt = {"open": "Open", "narrowed": "Narrowed (partially fixed; describes only what survives)"}[it["status"]]
    facts = [("Identifier", f"<code>{it['id']}</code>"), ("Category", cls["label"]), ("Subsystem", esc(it["subsystem"])),
             ("Status", f'<span class="issue-status issue-status--{it["status"]}">{esc(status_txt)}</span>'),
             ("Verified against", f"CNA <code>{TARGET_SHORT}</code> (<code>{TARGET}</code>)")]
    if it["severity"] != "n/a":
        facts.append(("Severity", f"{esc(it['severity'].capitalize())} <span class=\"issue-note\">(a triage suggestion, not a project priority)</span>"))
    facts += [("Evidence basis", esc(CONFIDENCE_LABEL[it["confidence"]])), ("Tests touching this area", "Yes: see Current tests" if has_tests(it) else "None"),
              ("Affected contract", esc(it["public_contract"]))]
    dl = '<dl class="issue-facts">' + "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in facts) + "</dl>"
    src_items = "".join(f"<li>{{{{src:{s['path']}}}}}" + (f" &mdash; {esc(s['note'])}" if s.get("note") else "") + "</li>" for s in it["sources"])
    body = f'<p class="lede">{esc(it["summary"])}</p>\n{dl}\n'
    body += block("Expected behaviour", "expected", para(it["expected"]))
    body += block("Actual behaviour at TARGET", "actual", para(it["actual"]))
    body += block("Source locations", "sources", f'<ul class="source-list">{src_items}</ul>')
    body += block("Evidence", "evidence", para(it["evidence"]))
    body += block("Focused reproduction", "reproduction",
                  para(it.get("reproduction")) or "<p>No focused reproduction is known. Nothing has been invented here; the evidence above is what exists.</p>")
    body += block("Current tests", "tests", para(it["tests_current"]))
    body += block("Regression test", "regression-test", para(it["regression_test"]))
    body += block("Blast radius", "blast-radius", para(it["blast_radius"]))
    body += block("Workaround", "workaround", para(it.get("workaround")) or "<p>No workaround is known.</p>")
    def label(s: str) -> str:
        return s if re.search(r"&(#\d+|\w+);", s) else html.escape(s, quote=False)
    layers = {k: [[u, label(lb)] for u, lb in v] for k, v in it["related"].items() if v}
    layers.setdefault("issues", [["known-issues/" + cls["group"] + "/index.html", cls["label"] + " index"]])
    meta = {"title": f"{it['id']}: {it['title']}", "description": it["summary"][:220],
            "keywords": [it["id"].lower(), it["class"], it["subsystem"].lower(), "known issue", "cna"],
            "evidence": {"levels": EVIDENCE_LEVELS[it["confidence"]] + (["test-present"] if has_tests(it) else []),
                         "note": "Nothing on this page was executed unless the Evidence section says so."},
            "layers": layers}
    return meta, body


def cmd_build(_: argparse.Namespace) -> int:
    import deep_manifest as DM
    import site_dev as SD
    import site_deep
    src = load(SOURCE)
    issues = src["issues"]
    for it in issues:
        it["detail"] = detail_path(it["id"], it["class"])
    pub = {"schema": 1, "target": TARGET, "target_short": TARGET_SHORT, "generated": TODAY,
           "note": "Current defects only: this index lists what exists at `target`. Fixed defects are never listed. Generated by scripts/known_issues.py from the verified findings; do not edit by hand.",
           "classes": {k: {"label": v["label"], "id_prefix": v["prefix"], "definition": CLASS_DEF[k]} for k, v in CLASSES.items()},
           "counts": dict(Counter(i["class"] for i in issues)),
           "issues": [public_entry(i) | {"detail": i["detail"]} for i in issues]}
    PUBLIC.parent.mkdir(exist_ok=True)
    PUBLIC.write_text(json.dumps(pub, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    errors: list[str] = []
    for it in issues:
        meta, body = page_fragment(it)
        page = it["detail"]
        text = site_deep.render_page(page, meta, body, errors)
        if errors:
            continue
        out = ROOT / page
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
    if errors:
        print("FAILED:")
        for e in errors[:40]:
            print(" -", e)
        return 1
    keep = {ROOT / it["detail"] for it in issues}
    stale = [p for grp in CLASSES.values() for p in sorted((ROOT / "known-issues" / grp["group"]).glob("*.html"))
             if p.name != "index.html" and p not in keep]
    for p in stale:
        p.unlink()
    if stale:
        print(f"removed {len(stale)} detail page(s) of entries that no longer exist")
    site_deep.cmd_hubs(argparse.Namespace())
    print(f"built {len(issues)} issue page(s), data/known-issues.json, and the hubs")
    return 0


# ---------------------------------------------------------------------------------------------
# hubs (called by site_deep.hub_body for the known-issues area)
# ---------------------------------------------------------------------------------------------
def hub_body(page: str, area_hub: str, group_key: str | None) -> tuple[dict, str] | None:
    if not PUBLIC.exists():
        return None
    pub = load(PUBLIC)
    issues = pub["issues"]
    from site_dev import rel_href
    if group_key is None:
        counts = Counter(i["class"] for i in issues)
        rows = "".join(
            f'<tr><td><a href="{rel_href(page, "known-issues/" + v["group"] + "/index.html")}">{v["label"]}</a></td><td>{counts.get(k, 0)}</td>'
            f'<td>{esc(CLASS_DEF[k])}</td></tr>' for k, v in CLASSES.items())
        subs = Counter((i["subsystem"], i["class"]) for i in issues)
        srows = ""
        for s in SUBSYSTEMS:
            tot = sum(subs.get((s, k), 0) for k in CLASSES)
            if tot:
                srows += f'<tr><td>{esc(s)}</td>' + "".join(f"<td>{subs.get((s, k), 0)}</td>" for k in CLASSES) + f"<td>{tot}</td></tr>"
        meta = {"title": "Known Issues",
                "description": f"What is wrong with, or missing from, CNA at snapshot {TARGET_SHORT}: {counts.get('bug', 0)} current bugs, {counts.get('functional-gap', 0)} functional gaps, "
                               f"{counts.get('platform-limitation', 0)} platform limitations and {counts.get('verification-gap', 0)} verification gaps, each with its evidence.",
                "keywords": ["known issues", "bugs", "gaps", "limitations", "cna-bug", "verification gaps", "cna"],
                "evidence": {"levels": ["source-verified"], "note": "Each entry states exactly what was read and what, if anything, was executed."}}
        body = (f'<p class="lede">This area answers one question: <em>what is wrong with, or missing from, CNA right now?</em> It lists only what exists at CNA commit '
                f'<code>{TARGET_SHORT}</code>. A defect that has been fixed is not listed; a deliberate design choice is not called a bug; and a shortfall of this website\'s documentation is not a CNA defect.</p>\n'
                f'<h2 id="categories">Four kinds of issue</h2>\n<div class="table-wrap"><table><thead><tr><th scope="col">Category</th><th scope="col">Entries</th><th scope="col">Definition</th></tr></thead><tbody>{rows}</tbody></table></div>\n'
                f'<h2 id="subsystems">By subsystem</h2>\n<div class="table-wrap"><table><thead><tr><th scope="col">Subsystem</th><th scope="col">Bugs</th><th scope="col">Gaps</th><th scope="col">Platform limits</th><th scope="col">Verification gaps</th><th scope="col">Total</th></tr></thead><tbody>{srows}</tbody></table></div>\n'
                f'<h2 id="method">How an entry gets here</h2>\n<ul>\n'
                f'<li><strong>Every entry was re-verified at the pinned commit.</strong> An earlier audit finding is a <em>candidate</em>, not a fact: it was checked against the source, headers, build files and tests at <code>{TARGET_SHORT}</code>.</li>\n'
                f'<li><strong>Every entry was then read a second time by a reviewer whose brief was to refute it.</strong> A reviewer could confirm, correct, narrow, reclassify, fold or remove an entry; the candidates that were dismissed earlier were re-read by reviewers told to prove the dismissal wrong, and a sample of entries was also checked by running small probes built from the pinned sources.</li>\n'
                f'<li><strong>A finding is removed only on positive evidence</strong>: the fixing code and, where one exists, the test that pins it; the renderer registry that retires the affected family (its identity is refused at configure time); or the source and the XNA 4.0 or FNA reference showing that the behaviour is the documented contract. It is not removed because a TODO vanished or a subsystem was rewritten.</li>\n'
                f'<li><strong>Evidence is stated per entry.</strong> <em>Source-verified</em> means the failure follows from code that was read at the pinned commit; it is not a run. '
                f'<em>Reproduced</em> means something was executed for the entry and the Evidence section names exactly what. <em>Recorded by CNA</em> means CNA&rsquo;s own recorded run says so and it was not repeated here. '
                f'<em>Inferred</em> means it follows from the code but depends on a platform or toolchain step nobody executed. Each entry also says whether any test touches the affected area.</li>\n'
                f'<li><strong>Documentation bugs are CNA&rsquo;s.</strong> A comment, header or document <em>inside the CNA repository</em> that contradicts the code at that commit is recorded as a bug in the <em>Documentation &amp; release tooling</em> subsystem; it says the text is stale, not that the code is wrong. A gap in this website is never listed.</li>\n'
                f'<li><strong>Stable identifiers.</strong> <code>CNA-BUG-###</code> identifiers are kept from the earlier audits; new ones continue the sequence.</li>\n</ul>\n'
                f'<h2 id="data">Machine-readable index</h2>\n<p>The same list is published as <a href="{rel_href(page, "data/known-issues.json")}"><code>data/known-issues.json</code></a> '
                f'(identifier, category, subsystem, status, severity, evidence basis, source paths, detail page), pinned to <code>{TARGET_SHORT}</code>.</p>\n'
                f'<h2 id="related">Related</h2>\n<p>What each subsystem is <em>supposed</em> to do is on the <a href="{rel_href(page, "deep-dives/index.html")}">Deep Dives</a> and the '
                f'<a href="{rel_href(page, "docs/verification.html")}">Verification &amp; Known Issues</a> guide page; how to change it safely is in the '
                f'<a href="{rel_href(page, "development/index.html")}">Development area</a>.</p>')
        return meta, body
    cls = next(k for k, v in CLASSES.items() if v["group"] == group_key)
    items = [i for i in issues if i["class"] == cls]
    label = CLASSES[cls]["label"] + "s" if not CLASSES[cls]["label"].endswith("s") else CLASSES[cls]["label"]
    meta = {"title": {"bug": "Current bugs", "functional-gap": "Functional gaps", "platform-limitation": "Platform limitations",
                      "verification-gap": "Verification gaps"}[cls],
            "description": f"{len(items)} {label.lower()} that exist in CNA at snapshot {TARGET_SHORT}: {CLASS_DEF[cls]}"[:220],
            "keywords": [group_key, "known issues", "cna"], "evidence": {"levels": ["source-verified"]}}
    if not items:
        body = f'<p class="lede">{esc(CLASS_DEF[cls])}</p>\n<p>No entries at this snapshot.</p>'
        return meta, body
    trs = ""
    for i in items:
        trs += (f'<tr><td><a href="{rel_href(page, i["detail"])}"><code>{i["id"]}</code></a></td><td>{esc(i["title"])}</td><td>{esc(i["subsystem"])}</td>'
                f'<td><span class="issue-status issue-status--{i["status"]}">{i["status"]}</span></td><td>{esc(i["severity"])}</td><td>{esc(CONFIDENCE_SHORT[i["confidence"]])}</td></tr>')
    body = (f'<p class="lede">{esc(CLASS_DEF[cls])} Every entry below exists at CNA <code>{TARGET_SHORT}</code>; open an entry for its expected and actual behaviour, source locations, evidence and blast radius.</p>\n'
            f'<h2 id="entries">{len(items)} entries</h2>\n<div class="table-wrap"><table><thead><tr><th scope="col">ID</th><th scope="col">Title</th><th scope="col">Subsystem</th>'
            f'<th scope="col">Status</th><th scope="col">Severity</th><th scope="col">Evidence basis</th></tr></thead><tbody>{trs}</tbody></table></div>')
    return meta, body


# ---------------------------------------------------------------------------------------------
# whole-system validation
# ---------------------------------------------------------------------------------------------
def cmd_qa(_: argparse.Namespace) -> int:
    """Fold the adversarial QA verdicts (qa-Q*.json) into patches.json: CORRECTED -> field replacements, REFUTED -> unpublished."""
    pp = ISS / "patches.json"
    patches = load(pp) if pp.exists() else {"global_replace": [], "entries": {}, "refuted": {}}
    patches.setdefault("entries", {})
    patches.setdefault("refuted", {})
    counts: Counter = Counter()
    for f in sorted(ISS.glob("qa-Q*.json")):
        if f.name.endswith("-list.json"):
            continue
        for v in load(f).get("verdicts", []):
            counts[v["verdict"]] += 1
            if v["verdict"] == "CORRECTED":
                patches["entries"].setdefault(v["id"], {"set": {}})["set"].update(v.get("corrections") or {})
            elif v["verdict"] == "REFUTED":
                patches["refuted"][v["id"]] = v.get("evidence", "")
    pp.write_text(json.dumps(patches, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("qa verdicts folded:", dict(counts), "| corrected entries:", len(patches["entries"]), "| refuted:", len(patches["refuted"]))
    return 0


def cmd_validate(_: argparse.Namespace) -> int:
    if not PUBLIC.exists():
        print("data/known-issues.json not built yet")
        return 1
    import site_dev as SD
    pub = load(PUBLIC)
    files, _d = SD.target_tree()
    errs: list[str] = []
    if pub.get("target") != TARGET:
        errs.append(f"index target {pub.get('target')} != cnahead {TARGET}")
    ids = Counter(i["id"] for i in pub["issues"])
    for k, n in ids.items():
        if n > 1:
            errs.append(f"duplicate id {k}")
    titles = Counter((i["class"], re.sub(r"\W+", " ", i["title"].lower())) for i in pub["issues"])
    for k, n in titles.items():
        if n > 1:
            errs.append(f"duplicate title in class {k[0]}: {k[1]}")
    for i in pub["issues"]:
        if not ID_RX.match(i["id"]):
            errs.append(f"{i['id']}: bad id")
        if i["status"] not in STATUSES:
            errs.append(f"{i['id']}: status {i['status']} (fixed/other statuses are never published)")
        if i["verified_against"] != TARGET:
            errs.append(f"{i['id']}: verified_against is not TARGET")
        if not (ROOT / i["detail"]).is_file():
            errs.append(f"{i['id']}: detail page missing: {i['detail']}")
        for s in i["sources"]:
            if s not in files:
                errs.append(f"{i['id']}: source path absent at TARGET: {s}")
    if DISPO.exists():
        d = load(DISPO)
        pub_ids = set(ids)
        for x in d["dispositions"]:
            if x["classification"] in PUBLISHED and x.get("published_as") not in pub_ids:
                errs.append(f"disposition {x['cand']} says {x['classification']} but {x.get('published_as')} is not published")
            if x["classification"] not in PUBLISHED and x.get("published_as") in pub_ids:
                errs.append(f"disposition {x['cand']} is {x['classification']} yet published as {x['published_as']}")
    for e in errs:
        print("ERROR", e)
    print(f"known issues: {len(pub['issues'])} entries {dict(pub['counts'])}; errors {len(errs)}")
    return 1 if errs else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("--pkg", nargs="*")
    sub.add_parser("merge")
    sub.add_parser("build")
    sub.add_parser("validate")
    sub.add_parser("qa")
    args = ap.parse_args()
    return {"check": cmd_check, "merge": cmd_merge, "build": cmd_build, "validate": cmd_validate, "qa": cmd_qa}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
