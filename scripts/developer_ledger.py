#!/usr/bin/env python3
"""Phase-2 absorption ledger: enumerate, collect, check and render.

    developer_ledger.py enumerate               # mechanically list every Developer unit (N of them)
    developer_ledger.py collect --src DIR       # merge DIR/**/*.ledger.json (page units) + audit/data/developer-absorption-nonpage.json
                                                # into audit/data/developer-absorption-units.json
    developer_ledger.py check [--strict]        # conservation checks against the built pages; exit 1 on any ERROR
    developer_ledger.py render                  # write audit/developer-absorption-phase2.md from the units file

Units are FILES of the developer.libcna.com working tree (read, not the Git HEAD): every page, generated reference,
process document, tool and asset.  A unit is *done* when it has a final action and (for page units) its destination page exists and every Developer
heading is mapped.  The conservation invariant is: pending == 0 and no unaccounted heading / cited source path.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import subprocess
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dev_manifest as M  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DEV = Path(os.environ.get("DEVELOPER_REPO", ROOT.parent / "developer.libcna.com"))
CNA = Path(os.environ.get("CNA_REPO", ROOT.parent / "cna"))
UNITS = ROOT / "audit" / "data" / "developer-absorption-units.json"
NONPAGE = ROOT / "audit" / "data" / "developer-absorption-nonpage.json"
REPORT = ROOT / "audit" / "developer-absorption-phase2.md"
TARGET = (ROOT / "cnahead").read_text().strip()
DEV_PIN = (DEV / "cnahead").read_text().strip()

GENERATED = {"reference/modules.html", "reference/cmake-options.html", "reference/test-targets.html",
             "reference/public-headers.html"}
ACTIONS = {"MERGE", "EXPAND", "NEW PAGE", "GENERATED REFERENCE", "CROSS-LINK", "SUPERSEDED", "DUPLICATE",
           "OBSOLETE", "TARGET-CONTRADICTED", "NOT CURRENT"}
PAGE_ACTIONS = {"MERGE", "EXPAND", "NEW PAGE", "GENERATED REFERENCE"}


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", html.unescape(re.sub(r"<[^>]+>", "", s)).lower()).strip()


class Headings(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.items: list[dict] = []
        self._cur: dict | None = None
        self.in_article = False
        self.ids: set[str] = set()
        self.text: list[str] = []
        self.links: list[str] = []
        self.codes: list[str] = []
        self._code = False
        self._buf = ""
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        v = {k: (x or "") for k, x in attrs}
        if v.get("id"):
            self.ids.add(v["id"])
        if tag == "article":
            self.in_article = True
        if not self.in_article:
            return
        if tag in ("script", "style"):
            self._skip += 1
        if tag in ("h2", "h3"):
            self._cur = {"level": int(tag[1]), "id": v.get("id", ""), "text": ""}
        if tag == "a" and v.get("href"):
            self.links.append(v["href"])
        if tag == "code":
            self._code, self._buf = True, ""

    def handle_endtag(self, tag):
        if tag == "article":
            self.in_article = False
        if tag in ("script", "style") and self._skip:
            self._skip -= 1
        if tag in ("h2", "h3") and self._cur is not None:
            self._cur["text"] = re.sub(r"\s+", " ", self._cur["text"]).strip()
            self.items.append(self._cur)
            self._cur = None
        if tag == "code" and self._code:
            self.codes.append(self._buf.strip())
            self._code = False

    def handle_data(self, data):
        if not self.in_article or self._skip:
            return
        self.text.append(data)
        if self._cur is not None:
            self._cur["text"] += data
        if self._code:
            self._buf += data


def parse(path: Path) -> Headings:
    p = Headings()
    p.feed(path.read_text(encoding="utf-8"))
    return p


def words(p: Headings) -> int:
    return len(" ".join(p.text).split())


def cited_paths(p: Headings, rev_any: bool = True) -> set[str]:
    out = set()
    for href in p.links:
        m = re.match(r"https://github\.com/libcna/cna/(?:blob|tree)/[0-9a-f]{40}/([^#]+)", href)
        if m:
            out.add(re.sub(r"%([0-9A-Fa-f]{2})", lambda x: chr(int(x.group(1), 16)), m.group(1)).rstrip("/"))
    return out


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout


def target_files() -> set[str]:
    return set(git(CNA, "ls-tree", "-r", "--name-only", TARGET).splitlines())


def dev_files() -> list[str]:
    out = []
    for dirpath, dirs, files in os.walk(DEV):
        dirs[:] = [d for d in dirs if d != ".git"]
        for f in files:
            out.append((Path(dirpath) / f).relative_to(DEV).as_posix())
    return sorted(out)


def source_type(rel: str) -> str:
    if rel in GENERATED:
        return "generated-reference"
    if rel.endswith(".html"):
        return "authored-page"
    if rel == "docs/COVERAGE.md":
        return "process-document"
    if rel.startswith("scripts/") or rel in ("Makefile",):
        return "tooling"
    if rel.startswith("assets/"):
        return "presentation-asset"
    return "repository-metadata"


def dev_state(rel: str) -> str:
    st = subprocess.run(["git", "-C", str(DEV), "status", "--short", "--", rel], capture_output=True,
                        text=True).stdout.strip()
    if not st:
        return "committed"
    code = st.split()[0]
    return {"M": "modified (uncommitted)", "??": "untracked (uncommitted)"}.get(code, st)


COVERAGE_STATE: dict[str, str] = {}  # developer page -> its state in docs/COVERAGE.md (filled lazily)


def coverage_note(rel: str) -> str:
    """What Developer's own coverage ledger says about this page (its audit state, NOT CNA product status)."""
    cov = (DEV / "docs/COVERAGE.md").read_text(encoding="utf-8")
    hits = []
    for line in cov.splitlines():
        if line.startswith("|") and f"`{rel}`" in line:
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) >= 2:
                hits.append(cells[1])
    if hits:
        return "; ".join(sorted(set(hits))) + " (Developer coverage state, not CNA product status)"
    return "not tracked in Developer's coverage ledger"


# ---------------------------------------------------------------------------------------------
def cmd_enumerate(_: argparse.Namespace) -> int:
    files = dev_files()
    c = Counter(source_type(f) for f in files)
    print(f"Developer files (working tree): {len(files)}")
    for k, v in sorted(c.items()):
        print(f"  {k}: {v}")
    dirty = [(f, dev_state(f)) for f in files if dev_state(f) != "committed"]
    print("uncommitted:", dirty)
    return 0


def cmd_collect(args: argparse.Namespace) -> int:
    src = Path(args.src)
    files = dev_files()
    page_ledgers: dict[str, dict] = {}
    for p in sorted(src.rglob("*.ledger.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        page_ledgers[d["developer_source"]] = d
    nonpage = json.loads(NONPAGE.read_text(encoding="utf-8")) if NONPAGE.exists() else {}
    units = []
    for i, rel in enumerate(files, 1):
        st = source_type(rel)
        unit = {"id": f"D-{i:03d}", "developer_source": rel, "source_type": st,
                "developer_state": dev_state(rel), "developer_status": coverage_note(rel) if st == "authored-page" else "",
                "action": "", "destination": "", "unique_knowledge": "", "target_verification_needed": st in
                ("authored-page", "generated-reference", "process-document"), "done": False}
        if rel in page_ledgers:
            d = page_ledgers[rel]
            for k in ("action", "destination", "unique_knowledge", "phase1_overlap", "target_verification", "sections",
                      "current_bugs_or_gaps", "phase1_errors_found", "paths_not_carried", "developer_status"):
                if k in d:
                    unit[k] = d[k]
            unit["developer_status"] = d.get("developer_status") or unit["developer_status"]
            unit["done"] = bool(d.get("action")) and bool(d.get("destination"))
        elif rel in nonpage:
            for k, v in nonpage[rel].items():
                unit[k] = v
            unit["done"] = bool(unit.get("action"))
        units.append(unit)
    new_pages = []
    for entry in M.all_pages():
        if entry["dev"]:
            continue
        meta_path = src / (entry["path"][:-5] + ".meta.json")
        meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
        new_pages.append({"path": entry["path"], "title": entry["title"], "kind": entry["kind"],
                          "exists": (ROOT / entry["path"]).exists(),
                          "draws_on": meta.get("developer_sources", []),
                          "purpose": meta.get("description", "")})
    doc = {"meta": {"developer_head": git(DEV, "rev-parse", "HEAD").strip(), "developer_cnahead": DEV_PIN,
                    "target": TARGET, "units": len(units)},
           "units": units, "new_pages": new_pages}
    UNITS.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    done = sum(1 for u in units if u["done"])
    print(f"{len(units)} units; {done} done; {len(units) - done} pending -> {UNITS.relative_to(ROOT)}")
    return 0


def load_units() -> dict:
    return json.loads(UNITS.read_text(encoding="utf-8"))


def cmd_check(args: argparse.Namespace) -> int:
    doc = load_units()
    units = doc["units"]
    errors: list[str] = []
    flags: list[str] = []
    files = dev_files()
    listed = {u["developer_source"] for u in units}
    for f in files:
        if f not in listed:
            errors.append(f"Developer file has no unit: {f}")
    for f in listed - set(files):
        errors.append(f"unit for a file that is not in the Developer tree: {f}")
    tfiles = target_files()
    dmap = M.developer_map()
    pending = 0
    for u in units:
        rel = u["developer_source"]
        act = u.get("action", "")
        if not act or act not in ACTIONS:
            errors.append(f"{rel}: missing/invalid action {act!r}")
            pending += 1
            continue
        if not u.get("done"):
            pending += 1
        if u["source_type"] in ("authored-page", "generated-reference"):
            exp = dmap.get(rel)
            dest = u.get("destination", "")
            if act in PAGE_ACTIONS or act == "GENERATED REFERENCE":
                if not dest:
                    errors.append(f"{rel}: no destination")
                    continue
                if exp and dest.split("#")[0] != exp:
                    errors.append(f"{rel}: destination {dest} differs from manifest {exp}")
                if not (ROOT / dest.split("#")[0]).exists():
                    errors.append(f"{rel}: destination page does not exist: {dest}")
                    continue
        if u["source_type"] != "authored-page":
            continue
        dest = u.get("destination", "").split("#")[0]
        dpage_path = ROOT / dest
        if not dest or not dpage_path.exists():
            continue
        dp, sp = parse(dpage_path), parse(DEV / rel)
        # 1. every Developer h2/h3 must be mapped
        mapped_ids = {s.get("developer_id") for s in u.get("sections", []) if s.get("developer_id")}
        mapped_heads = {norm(s.get("developer_heading", "")) for s in u.get("sections", [])}
        for h in sp.items:
            if h["id"] and h["id"] in mapped_ids:
                continue
            if norm(h["text"]) in mapped_heads:
                continue
            errors.append(f"{rel}: Developer heading not mapped in ledger: <h{h['level']}> {h['text']!r} #{h['id']}")
        for s in u.get("sections", []):
            d = s.get("destination", "")
            if s.get("disposition") == "DROPPED":
                if not s.get("note"):
                    errors.append(f"{rel}: DROPPED section without a reason: {s.get('developer_heading')}")
                continue
            if "#" in d:
                page, frag = d.split("#", 1)
                pp = ROOT / page
                if not pp.exists():
                    errors.append(f"{rel}: section destination page missing: {d}")
                elif frag not in parse(pp).ids:
                    errors.append(f"{rel}: section destination anchor missing: {d}")
            elif not d:
                errors.append(f"{rel}: section without destination: {s.get('developer_heading')}")
        # 2. cited source paths carried over (or explained)
        dev_paths = {p for p in cited_paths(sp) if p in tfiles or any(f.startswith(p + "/") for f in tfiles)}
        gone = {p for p in cited_paths(sp) if p not in tfiles and not any(f.startswith(p + "/") for f in tfiles)}
        carried = cited_paths(dp)
        explained = {x["path"] for x in u.get("paths_not_carried", [])}
        tv = u.get("target_verification", {})
        explained |= set(tv.get("missing_at_target", []))
        lost = sorted(p for p in dev_paths if p not in carried and p not in explained)
        if lost:
            flags.append(f"{rel}: {len(lost)} cited source path(s) not carried to {dest}: " + ", ".join(lost[:6]) +
                         (" …" if len(lost) > 6 else ""))
        if gone and not tv.get("missing_at_target"):
            flags.append(f"{rel}: Developer cites {len(gone)} path(s) absent at TARGET, ledger lists none: " +
                         ", ".join(sorted(gone)[:4]))
        # 3. size and code-token conservation
        ws, wd = words(sp), words(dp)
        if wd < 0.85 * ws:
            flags.append(f"{rel}: destination has {wd} words vs Developer {ws} ({wd / ws:.0%})")
        dtext = " ".join(dp.text)
        toks = [t for t in dict.fromkeys(sp.codes) if len(t) >= 4 and re.search(r"[A-Za-z]", t)]
        missing_tokens = [t for t in toks if t not in dtext and t not in " ".join(dp.codes)]
        if toks and len(missing_tokens) / len(toks) > 0.35:
            flags.append(f"{rel}: {len(missing_tokens)}/{len(toks)} Developer code tokens absent from destination")
    for u in units:
        if u.get("action") == "TARGET-CONTRADICTED" and not u.get("note") and not u.get("unique_knowledge"):
            errors.append(f"{u['developer_source']}: TARGET-CONTRADICTED without explanation")
    for n in doc.get("new_pages", []):
        if not (ROOT / n["path"]).exists():
            errors.append(f"planned new page not built: {n['path']}")
    audited = sum(1 for u in units if u.get("action"))
    print(f"Developer units audited: {audited}/{len(units)}   pending: {pending}")
    print(f"errors: {len(errors)}   review flags: {len(flags)}")
    for e in errors:
        print("  ERROR", e)
    for f in flags:
        print("  flag ", f)
    if args.strict and flags:
        return 1
    return 1 if errors or pending else 0


def cmd_render(_: argparse.Namespace) -> int:
    doc = load_units()
    units = doc["units"]
    meta = doc["meta"]
    c_action = Counter(u.get("action") or "PENDING" for u in units)
    pages = [u for u in units if u["source_type"] == "authored-page"]
    contradictions = [(u, x) for u in units for x in (u.get("target_verification") or {}).get("contradictions", [])]
    dropped = [(u, x) for u in units for x in (u.get("target_verification") or {}).get("dropped", [])]
    bugs = [(u, x) for u in units for x in u.get("current_bugs_or_gaps", [])]
    p1err = [(u, x) for u in units for x in u.get("phase1_errors_found", [])]
    pending = [u for u in units if not u.get("done")]
    L: list[str] = []
    L += ["# Phase-2 absorption ledger — developer.libcna.com → libcna.com/development", "",
          "Durable record of the additive absorption of every Developer knowledge unit into libcna.com. Generated by",
          "`scripts/developer_ledger.py render` from `audit/data/developer-absorption-units.json` (page units are written by the",
          "authors of each page; non-page units in `audit/data/developer-absorption-nonpage.json`). Nothing here is served as site content.", ""]
    L += ["## 1. Source boundary", "", "| Item | Value |", "|---|---|",
          f"| `PHASE1_BASE` (libcna.com accepted Phase-1 HEAD, branch `docs/unified-v2`) | `94d758ae85d3209eee8f613d31fd9f7097c24dc6` — “docs: link the now-public Go and Ruby bindings on the homepage and the C API page” |",
          f"| CNA `TARGET` (= `cnahead`) | `{TARGET}` (branch `next`, 2026-09-24) |",
          f"| Developer repository HEAD | `{meta['developer_head']}` (its **working tree** was read, not only HEAD) |",
          f"| Developer `cnahead` (the CNA commit it documents) | `{meta['developer_cnahead']}` — an ancestor of TARGET, 55 commits earlier (224 files changed between them, concentrated in OpenGL4, SDL_gpu, EasyGL, graphics tests/examples, `cmake/`) |",
          "| Developer uncommitted work absorbed | " + "; ".join(f"`{u['developer_source']}` ({u['developer_state']})" for u in units if u["developer_state"] != "committed") + " |",
          "| Developer status vocabulary | `NOT STARTED / INVESTIGATING / DRAFTED / SOURCE VERIFIED / COMPLETE` describe **Developer's own documentation audit**, never CNA product status; none appears on published pages |",
          "| TARGET access | read-only `git archive` extraction at `/rv/tmp/libcna-v2/cna-target` (no CNA checkout, branch or working tree touched) |", ""]
    L += ["## 2. Progress", "", f"```text",
          f"Developer units (files): {len(units)}   authored pages: {len(pages)}   generated reference classes: {sum(1 for u in units if u['source_type'] == 'generated-reference')}",
          f"Audited: {sum(1 for u in units if u.get('action'))}/{len(units)}   Pending: {len(pending)}",
          "Actions: " + ", ".join(f"{k} {v}" for k, v in sorted(c_action.items())),
          f"TARGET contradictions corrected: {len(contradictions)}   claims dropped with reason: {len(dropped)}",
          f"Phase-1 errors found: {len(p1err)}   current bugs/gaps recorded for Phase 3: {len(bugs)}", "```", ""]
    L += ["## 3. Ledger (one row per Developer file)", "",
          "Columns: Developer source · source type · Developer's own status (its audit state) · unique knowledge · TARGET verification needed? · libcna destination · action · done.", "",
          "| Developer source | Type | Developer status | Unique knowledge | TARGET check | libcna destination | Action | Done |",
          "|---|---|---|---|---|---|---|---|"]
    for u in units:
        def cell(s: str) -> str:
            return (s or "").replace("|", "/").replace("\n", " ")
        dest = u.get("destination", "")
        dest_cell = f"`{dest}`" if dest else "—"
        L.append(f"| `{u['developer_source']}`{' *(' + u['developer_state'] + ')*' if u['developer_state'] != 'committed' else ''} | {u['source_type']} | "
                 f"{cell(u.get('developer_status', ''))} | {cell(u.get('unique_knowledge', ''))} | "
                 f"{'yes' if u['target_verification_needed'] else 'no'} | {dest_cell} | {u.get('action') or 'PENDING'} | {'yes' if u.get('done') else 'NO'} |")
    L.append("")
    if contradictions:
        L += ["## 4. TARGET contradictions corrected (Developer text vs CNA `009d40f5`)", "",
              "| Developer page | Developer claim | TARGET fact | Evidence | Resolution |", "|---|---|---|---|---|"]
        for u, x in contradictions:
            L.append(f"| `{u['developer_source']}` | {x.get('developer_claim', '').replace('|', '/')} | {x.get('target_fact', '').replace('|', '/')} | "
                     f"{x.get('evidence', '').replace('|', '/')} | {x.get('resolution', '').replace('|', '/')} |")
        L.append("")
    if dropped:
        L += ["## 5. Developer claims not carried over", "", "| Developer page | Claim | Reason |", "|---|---|---|"]
        for u, x in dropped:
            L.append(f"| `{u['developer_source']}` | {x.get('claim', '').replace('|', '/')} | {x.get('reason', '').replace('|', '/')} |")
        L.append("")
    if p1err:
        L += ["## 6. Phase-1 factual errors found during Phase 2", "", "| Page | Issue | Evidence |", "|---|---|---|"]
        for u, x in p1err:
            L.append(f"| `{x.get('page', '')}` | {x.get('issue', '').replace('|', '/')} | {x.get('evidence', '').replace('|', '/')} |")
        L.append("")
    if bugs:
        L += ["## 7. Current bugs / gaps noted while absorbing (for the Phase-3 catalogue; not published as a catalogue)", "",
              "| Source unit | Summary | Evidence |", "|---|---|---|"]
        for u, x in bugs:
            L.append(f"| `{u['developer_source']}` | {x.get('summary', '').replace('|', '/')} | {x.get('evidence', '').replace('|', '/')} |")
        L.append("")
    newp = doc.get("new_pages", [])
    if newp:
        L += ["## 8. Pages with no single Developer counterpart (new material written from TARGET, drawing on the listed Developer units)", "",
              "| Page | Kind | Built | Draws on (Developer units) | Purpose |", "|---|---|---|---|---|"]
        for n in newp:
            L.append(f"| `{n['path']}` | {n['kind']} | {'yes' if n['exists'] else 'NO'} | {', '.join('`' + d + '`' for d in n['draws_on']) or '—'} | {n['purpose'].replace('|', '/')} |")
        L.append("")
    if pending:
        L += ["## 9. Pending units", ""] + [f"- `{u['developer_source']}`" for u in pending] + [""]
    REPORT.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"wrote {REPORT.relative_to(ROOT)} ({len(units)} units, {len(pending)} pending)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("enumerate")
    c = sub.add_parser("collect")
    c.add_argument("--src", required=True)
    k = sub.add_parser("check")
    k.add_argument("--strict", action="store_true")
    sub.add_parser("render")
    args = ap.parse_args()
    return {"enumerate": cmd_enumerate, "collect": cmd_collect, "check": cmd_check, "render": cmd_render}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
