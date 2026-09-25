#!/usr/bin/env python3
"""Turn the independent reviewers' verdicts on the published Known Issues into patches-adversarial.json.

    audit_issue_review.py ingest SRC_DIR [--kind issues|dismissals]   # copy reviewer JSONL into audit/data/adversarial/ after schema checks
    audit_issue_review.py summary                                    # verdict table over everything ingested
    audit_issue_review.py show ID                                    # old -> new field text for one entry (what `plan` would write)
    audit_issue_review.py plan [--write]                             # build audit/data/bible/issues/patches-adversarial.json

Inputs (all under audit/data/adversarial/):
  issue-reviews/*.jsonl        one verdict per published entry (CONFIRMED / CORRECTED / NARROWED / RECLASSIFIED / DUPLICATE / FIXED AT TARGET / NOT A BUG / INSUFFICIENT EVIDENCE)
  dismissal-reviews/*.jsonl    one verdict per dismissed candidate (DISMISSAL CONFIRMED / RESTORE-* / ALREADY-PUBLISHED / NARROW-RESTORE / UNRESOLVED)
  decisions.json               the orchestrator's adjudication; a reviewer's verdict is a proposal, not a fact.

Automatic (no decision needed): the `tests_present` flag, text corrections of CORRECTED / NARROWED entries and the evidence-basis label.
Needs an explicit decision (listed by `plan`, applied only when decisions.json says so): a severity change, RECLASSIFIED, DUPLICATE, FIXED AT TARGET / NOT A BUG / INSUFFICIENT EVIDENCE (retirement),
and every restored dismissal.  decisions.json:
  {"issues": {"CNA-BUG-nnn": {"action": "accept" | "reject" | "override", "note": "...", "set": {...}, "severity": "...", "class": "...", "duplicate_of": "...", "retire": "NOT A BUG|...", "evidence": "...",
                             "fold_into": "CNA-BUG-mmm", "retire_as": "NOT A BUG|PROVEN FIXED|OBSOLETE|INSUFFICIENT EVIDENCE", "reclassify_to": "functional-gap"}},
   "dismissals": {"CNA-BUG-0nn": {"action": "accept" | "reject", "entry": {... complete entry with temp id NEW-AUDIT-nn ...}}},
   "new_findings": [{... complete entry, temp id NEW-AUDIT-nn, cand_ids [] and an origin starting "new finding" ...}]}
  reject = keep the entry exactly as published (the reviewer's proposal is dropped); accept = apply the proposal; override = apply `set` / `severity` / ... as written here instead.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ADV = ROOT / "audit" / "data" / "adversarial"
ISS = ROOT / "audit" / "data" / "bible" / "issues"
SOURCE = ISS / "issues-source.json"
PATCHES = ISS / "patches-adversarial.json"
BASIS_TO_CONFIDENCE = {"source-verified": "verified-by-reading", "reproduced": "reproduced", "recorded-by-cna": "recorded-by-cna",
                       "inferred-strong": "strong", "inferred-probable": "probable"}
VERDICTS = {"CONFIRMED", "CORRECTED", "NARROWED", "RECLASSIFIED", "DUPLICATE", "FIXED AT TARGET", "NOT A BUG", "INSUFFICIENT EVIDENCE"}
DISMISSAL_VERDICTS = {"DISMISSAL CONFIRMED", "RESTORE-BUG", "RESTORE-GAP", "RESTORE-PLATFORM-LIMITATION", "RESTORE-VERIFICATION-GAP", "ALREADY-PUBLISHED",
                      "NARROW-RESTORE", "UNRESOLVED"}
RETIRE_CLASSIFICATION = {"FIXED AT TARGET": "PROVEN FIXED", "NOT A BUG": "NOT A BUG", "INSUFFICIENT EVIDENCE": "INSUFFICIENT EVIDENCE", "DUPLICATE": "DUPLICATE"}
PATH_RX = re.compile(r"(?<![\w/.\-])((?:modules|cmake|tools|docs|scripts|tests|plans|examples|third_party|integration|misc|\.github|include)/[\w./+@\-]*[\w])")
IDENT_RX = re.compile(
    r"(?<![\w>`.])("
    r"(?:[A-Za-z_]\w*::)*[A-Za-z_]\w*(?:&lt;[\w:, *&;]+?&gt;)+(?:::\w+)*(?:\([^()\n]{0,40}\))?"   # templates and casts: static_cast<int>(x), std::vector<T>
    r"|(?:[A-Za-z_]\w*::)+[A-Za-z_]\w*(?:\([^()\n]{0,40}\))?"                # qualified names, optionally with a short argument list
    r"|(?:[A-Z][A-Za-z0-9]*\.)+[A-Z][A-Za-z0-9]*(?:\([^()\n]{0,40}\))?"       # dotted managed names: CurveKeyCollection.ComputeCacheValues, Microsoft.Xna.Framework
    r"|[A-Za-z_]\w*\([^()\n]{0,40}\)"                                       # function calls
    r"|[a-z]+[A-Z]\w*|[A-Z][a-z0-9]+[A-Z]\w*|[A-Za-z]+_\w+"                    # camelCase, PascalCase, snake_case
    r")(?![\w<])")


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def target_files() -> set[str]:
    sys.path.insert(0, str(ROOT / "scripts"))
    import site_dev as SD
    files, _dirs = SD.target_tree()
    return files


def plain_to_html(text: str, files: set[str]) -> str:
    """Reviewer plain text -> the entry's HTML conventions: escaped, TARGET paths as {{src:...}} tokens, identifiers in <code>; several lines become a list."""
    def one(block: str) -> str:
        block = html.escape(block.strip(), quote=False)
        parts: list[str] = []
        pos = 0
        for m in PATH_RX.finditer(block):
            parts.append(("txt", block[pos:m.start()]))
            path = m.group(1).rstrip(".,;:)")
            tail = m.group(1)[len(path):]
            parts.append(("src", path) if path in files else ("code", path))
            parts.append(("txt", tail))
            pos = m.end()
        parts.append(("txt", block[pos:]))
        out = []
        for kind, val in parts:
            if kind == "src":
                out.append("{{src:" + val + "|" + val.rsplit("/", 1)[-1] + "}}")
            elif kind == "code":
                out.append("<code>" + val + "</code>")
            else:
                out.append(IDENT_RX.sub(lambda m: "<code>" + m.group(1) + "</code>", val))
        return "".join(out)

    lines = [l for l in text.split("\n") if l.strip()]
    if len(lines) > 1:
        return "<ul>" + "".join(f"<li>{one(l)}</li>" for l in lines) + "</ul>"
    return f"<p>{one(lines[0])}</p>" if lines else ""


def read_jsonl(paths) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for p in sorted(paths):
        for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            if line.strip():
                d = json.loads(line)
                out[d.get("id") or d.get("cand")] = d
    return out


def cmd_ingest(args: argparse.Namespace) -> int:
    dest = ADV / ("issue-reviews" if args.kind == "issues" else "dismissal-reviews")
    dest.mkdir(parents=True, exist_ok=True)
    pub = {i["id"] for i in load(SOURCE)["issues"]}
    rc = 0
    for f in sorted(Path(args.src).glob("out-*.jsonl")):
        rows = [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
        keys = [r.get("id") or r.get("cand") for r in rows]
        bad = [k for k in keys if args.kind == "issues" and k not in pub]
        dups = [k for k, n in Counter(keys).items() if n > 1]
        allowed = VERDICTS if args.kind == "issues" else DISMISSAL_VERDICTS
        badv = [r for r in rows if r.get("verdict") not in allowed]
        if bad or dups or badv:
            print(f"{f.name}: unknown ids {bad[:3]}, duplicates {dups[:3]}, invalid verdicts {[r.get('verdict') for r in badv[:3]]}")
            rc = 1
            continue
        shutil.copyfile(f, dest / f.name.replace("out-", "").replace(".jsonl", ".jsonl"))
        print(f"{f.name}: {len(rows)} verdicts ingested -> {dest.relative_to(ROOT)}")
    return rc


def reviews(kind: str) -> dict[str, dict]:
    d = ADV / ("issue-reviews" if kind == "issues" else "dismissal-reviews")
    return read_jsonl(d.glob("*.jsonl")) if d.exists() else {}


def cmd_summary(_: argparse.Namespace) -> int:
    rv = reviews("issues")
    pub = load(SOURCE)["issues"]
    print(f"issue verdicts ingested: {len(rv)} of {len(pub)} published entries; missing {len(pub) - len(rv)}")
    print("  ", dict(Counter(r["verdict"] for r in rv.values())))
    byid = {i["id"]: i for i in pub}
    sev = [(k, byid[k]["severity"], r.get("severity_after")) for k, r in rv.items() if k in byid and byid[k]["class"] == "bug" and r.get("severity_after") not in (None, byid[k]["severity"])]
    print("   severity changes proposed:", len(sev), sev[:12])
    print("   tests_present false:", sum(1 for r in rv.values() if r.get("tests_present") is False), "| evidence basis:", dict(Counter(r.get("evidence_basis_after") for r in rv.values())))
    dv = reviews("dismissals")
    if dv:
        print(f"dismissal verdicts ingested: {len(dv)}", dict(Counter(r["verdict"] for r in dv.values())))
    return 0


def base_entries() -> dict[str, dict]:
    """The published entries as they stand BEFORE any adversarial operation, so a plan never depends on its own earlier output."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import known_issues as KI
    built = KI.build_entries(False)
    if isinstance(built, int):
        raise SystemExit("cannot rebuild the base entries")
    return {i["id"]: i for i in built[0]}


def build(rv: dict[str, dict], dec: dict, files: set[str]) -> tuple[dict, list[str]]:
    """A pure function of (reviews, decisions): re-running it never accumulates anything, because the merge applies the result to freshly rebuilt entries.
    Reviewer values are always emitted (never compared with the already patched issues-source.json), so a re-plan reproduces the same file."""
    byid = base_entries()
    patch: dict = {"entries": {}, "folded": {}, "retired": {}, "reclassified": {}, "added": []}
    pending: list[str] = []
    ids = sorted(set(rv) | set(dec.get("issues", {})))
    for iid in ids:
        if iid not in byid:
            continue
        cur = byid[iid]
        r = rv.get(iid) or {"verdict": "CONFIRMED"}
        d = dec.get("issues", {}).get(iid, {})
        act = d.get("action", "auto")
        verdict = "CONFIRMED" if act == "reject" else r["verdict"]
        sets: dict = {}
        appends: dict = {}
        if act != "reject":
            if isinstance(r.get("tests_present"), bool):
                sets["tests_present"] = r["tests_present"]
            conf = BASIS_TO_CONFIDENCE.get(r.get("evidence_basis_after") or "")
            if conf:
                downgrade = conf == "verified-by-reading" and cur["confidence"] in ("reproduced", "recorded-by-cna")
                if downgrade and act not in ("accept", "override"):
                    pending.append(f"{iid}: reviewer would downgrade the evidence basis {cur['confidence']} -> {conf}; needs an explicit decision")
                else:
                    sets["confidence"] = conf
            if verdict in ("CORRECTED", "NARROWED", "RECLASSIFIED"):
                corr = r.get("correction") or {}
                for f in ("title", "summary"):
                    if corr.get(f):
                        sets[f] = corr[f].strip()
                for f in ("expected", "actual"):
                    if corr.get(f):
                        sets[f] = plain_to_html(corr[f], files)
                if corr.get("evidence_note"):
                    appends["evidence"] = "<p><em>Independent re-verification:</em> " + html.escape(corr["evidence_note"].strip(), quote=False) + "</p>"
        if act in ("accept", "override"):
            if d.get("severity"):
                sets["severity"] = d["severity"]
            sets.update(d.get("set", {}))
            # manual outcomes, independent of any reviewer verdict
            if d.get("fold_into"):
                patch["folded"][iid] = d["fold_into"]
            if d.get("retire_as"):
                patch["retired"][iid] = {"classification": d["retire_as"], "evidence": d.get("evidence") or d.get("note", "")}
            if d.get("reclassify_to"):
                patch["reclassified"][iid] = {"class": d["reclassify_to"], "set": {}}
            if verdict == "RECLASSIFIED" and (d.get("class") or r.get("class_after")):
                patch["reclassified"][iid] = {"class": d.get("class") or r["class_after"], "set": {}}
            elif verdict == "DUPLICATE" and (d.get("duplicate_of") or r.get("duplicate_of")):
                patch["folded"][iid] = d.get("duplicate_of") or r["duplicate_of"]
            elif verdict in RETIRE_CLASSIFICATION:
                patch["retired"][iid] = {"classification": RETIRE_CLASSIFICATION[verdict], "evidence": d.get("evidence") or r.get("reason", "")}
        elif act != "reject":
            if verdict in ("RECLASSIFIED", "DUPLICATE", "FIXED AT TARGET", "NOT A BUG", "INSUFFICIENT EVIDENCE"):
                pending.append(f"{iid}: reviewer proposes {verdict}"
                               + (f" -> {r.get('class_after')}" if verdict == "RECLASSIFIED" else f" of {r.get('duplicate_of')}" if verdict == "DUPLICATE" else "")
                               + f": {r.get('reason', '')[:140]}")
            if cur["class"] == "bug" and r.get("severity_after") not in (None, cur["severity"]):
                pending.append(f"{iid}: reviewer proposes severity {cur['severity']} -> {r['severity_after']}: {r.get('reason', '')[:120]}")
        if sets or appends:
            spec = {}
            if sets:
                spec["set"] = sets
            if appends:
                spec["append"] = appends
            patch["entries"][iid] = spec
    for cand, d in dec.get("dismissals", {}).items():
        if d.get("action") == "accept" and d.get("entry"):
            patch["added"].append(d["entry"])
    for e in dec.get("new_findings", []):        # defects the audit itself found while re-reading (no earlier candidate)
        patch["added"].append(e)
    patch["added"].sort(key=lambda e: e["id"])           # allocation order = temporary id, so earlier ids never shift when entries are added
    return {k: v for k, v in patch.items() if v}, pending


def cmd_plan(args: argparse.Namespace) -> int:
    rv = reviews("issues")
    dec = load(ADV / "decisions.json") if (ADV / "decisions.json").exists() else {}
    patch, pending = build(rv, dec, target_files())
    print(f"plan: {len(patch.get('entries', {}))} field patches, {len(patch.get('folded', {}))} folds, {len(patch.get('retired', {}))} retirements, "
          f"{len(patch.get('reclassified', {}))} reclassifications, {len(patch.get('added', []))} restored entries; {len(pending)} proposals awaiting a decision")
    for p in pending:
        print("  PENDING", p)
    if args.write:
        PATCHES.write_text(json.dumps(patch, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print("wrote", PATCHES.relative_to(ROOT))
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    rv = reviews("issues")
    dec = load(ADV / "decisions.json") if (ADV / "decisions.json").exists() else {}
    patch, _ = build({args.id: rv[args.id]}, dec, target_files())
    cur = base_entries()[args.id]
    spec = patch.get("entries", {}).get(args.id) or {}
    sets = dict(spec.get("set", {}))
    for f, add in (spec.get("append") or {}).items():
        sets[f + " (appended)"] = add
    print(f"{args.id}: verdict {rv[args.id]['verdict']}; reason: {rv[args.id].get('reason')}")
    for f, new in sets.items():
        print(f"--- {f} (old)\n{str(cur.get(f))[:1500]}\n+++ {f} (new)\n{str(new)[:1800]}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("ingest")
    i.add_argument("src")
    i.add_argument("--kind", choices=["issues", "dismissals"], default="issues")
    sub.add_parser("summary")
    s = sub.add_parser("show")
    s.add_argument("id")
    p = sub.add_parser("plan")
    p.add_argument("--write", action="store_true")
    args = ap.parse_args()
    return {"ingest": cmd_ingest, "summary": cmd_summary, "show": cmd_show, "plan": cmd_plan}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
