#!/usr/bin/env python3
"""Compare the current site's presentation inventory with the Phase-1 baseline.

Every baseline item (heading, CTA, significant link, card, image, video, stat, table,
major block, page) must still exist in the working tree -- or be covered by an explicit,
justified entry in audit/data/phase1-dispositions.json.  Differences that are *not*
losses (an updated statistic value, a renamed-but-matching heading) are reported as
"updated", not as losses.

Exit status: 0 = no unexplained loss; 1 = unexplained loss(es).

Usage:
    compare_presentation.py                       # whole site
    compare_presentation.py --page demos.html     # one page (use after each protected-page edit)
    compare_presentation.py --report audit/phase1-presentation-comparison.md

Phase 2 uses the same engine against the PHASE1_BASE inventory with a stricter size guard:
    compare_presentation.py --phase2 [--report audit/phase2-presentation-comparison.md]
        baseline    audit/data/phase2-baseline-inventory.json   (inventory of 94d758a)
        dispositions audit/data/phase2-dispositions.json
        page-shrink / block-shrink fire on a >10% reduction (Phase 1: 40% / 50%)
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from inventory_presentation import ROOT, extract_page  # noqa: E402

BASELINE = ROOT / "audit" / "data" / "phase1-baseline-inventory.json"
DISPOSITIONS = ROOT / "audit" / "data" / "phase1-dispositions.json"
PHASE2_BASELINE = ROOT / "audit" / "data" / "phase2-baseline-inventory.json"
PHASE2_DISPOSITIONS = ROOT / "audit" / "data" / "phase2-dispositions.json"
# fraction of the baseline size below which a block / page counts as shrunk
BLOCK_KEEP = 0.5
PAGE_KEEP = 0.6
ROLE_RANK = {"primary": 3, "secondary": 2, "outline": 1, "plain": 0}
FUZZY = 0.82


def norm(text: str) -> str:
    text = re.sub(r"[^\w\s]", " ", (text or "").lower())
    return re.sub(r"\s+", " ", text).strip()


def similar(a: str, b: str) -> float:
    a, b = norm(a), norm(b)
    if not a or not b:
        return 1.0 if a == b else 0.0
    if a == b:
        return 1.0
    return difflib.SequenceMatcher(None, a, b).ratio()


def best(text: str, candidates: list[str]) -> float:
    return max((similar(text, c) for c in candidates), default=0.0)


class Loss:
    def __init__(self, page: str, kind: str, key: str, detail: str = "") -> None:
        self.page, self.kind, self.key, self.detail = page, kind, key, detail
        self.disposition: dict | None = None

    def matches(self, entry: dict) -> bool:
        if entry.get("page") not in (self.page, "*"):
            return False
        if entry.get("kind") not in (self.kind, "*"):
            return False
        needle = entry.get("match", "")
        return bool(needle) and needle.lower() in self.key.lower()


def compare_page(rel: str, base: dict, cur: dict | None) -> tuple[list[Loss], list[str]]:
    losses: list[Loss] = []
    notes: list[str] = []
    if cur is None:
        losses.append(Loss(rel, "page", rel, "page no longer exists"))
        return losses, notes

    # headings
    cur_heads = [h["text"] for h in cur["headings"]]
    cur_ids = {h["id"] for h in cur["headings"] if h["id"]} | set(cur["section_ids"])
    for h in base["headings"]:
        if h["level"] > 3 and rel.startswith("docs/tutorials/"):
            continue  # deep tutorial sub-headings are content, covered by word-count check
        if best(h["text"], cur_heads) >= FUZZY:
            continue
        if h["id"] and h["id"] in cur_ids:
            notes.append(f"{rel}: heading `{h['text']}` retitled (id #{h['id']} kept)")
            continue
        losses.append(Loss(rel, "heading", h["text"], f"h{h['level']}"))

    # section ids (deep-link anchors)
    for sid in base["section_ids"]:
        if sid not in cur["section_ids"]:
            losses.append(Loss(rel, "anchor", sid, "id no longer exists (deep links break)"))

    # CTAs: same href must survive; prominence must not drop
    cur_ctas = cur["ctas"]
    for c in base["ctas"]:
        same = [x for x in cur_ctas if x["href"] == c["href"]]
        if not same:
            near = [x for x in cur_ctas if similar(x["label"], c["label"]) >= 0.9]
            losses.append(Loss(rel, "cta", f"{c['label']} -> {c['href']}",
                               "href gone" + (f"; similar label now -> {near[0]['href']}" if near else "")))
            continue
        if max(ROLE_RANK.get(x["role"], 0) for x in same) < ROLE_RANK.get(c["role"], 0):
            losses.append(Loss(rel, "cta-downgrade", f"{c['label']} -> {c['href']}",
                               f"was {c['role']}, now {same[0]['role']}"))
    base_primary = sum(1 for c in base["ctas"] if c["role"] == "primary")
    cur_primary = sum(1 for c in cur_ctas if c["role"] == "primary")
    if cur_primary < base_primary:
        notes.append(f"{rel}: primary CTA count {base_primary} -> {cur_primary}")

    # significant external links
    sig = {"external-deep", "external-root", "github-repo", "github-deep", "github-org"}
    cur_hrefs = {l["href"] for l in cur["links"]} | {c["href"] for c in cur["ctas"]}
    for l in base["links"]:
        if l["kind"] in sig and l["href"] not in cur_hrefs:
            losses.append(Loss(rel, "link", f"{l['label']} -> {l['href']}", l["kind"]))

    # cards
    cur_titles = [c["title"] for c in cur["cards"]]
    seen = set()
    for c in base["cards"]:
        if not c["title"] or (c["kind"], c["title"]) in seen:
            continue
        seen.add((c["kind"], c["title"]))
        if best(c["title"], cur_titles) < FUZZY:
            losses.append(Loss(rel, "card", c["title"], c["kind"]))

    # images
    cur_src = {i["src"] for i in cur["images"]}
    for i in base["images"]:
        if i["src"] not in cur_src:
            losses.append(Loss(rel, "image", i["src"], i["alt"][:80]))

    # videos
    cur_v = {v.get("id") or v.get("src", "") for v in cur["videos"]}
    cur_vt = [v["title"] for v in cur["videos"]]
    for v in base["videos"]:
        key = v.get("id") or v.get("src", "")
        if key and key in cur_v:
            continue
        if v["title"] and best(v["title"], cur_vt) >= FUZZY:
            continue
        losses.append(Loss(rel, "video", key or v["title"], v["title"]))

    # stats
    cur_labels = [s["label"] for s in cur["stats"]]
    for s in base["stats"]:
        if best(s["label"], cur_labels) < 0.6:
            losses.append(Loss(rel, "stat", f"{s['value']} {s['label']}"))
        else:
            match = max(cur["stats"], key=lambda x: similar(s["label"], x["label"]))
            if match["value"] != s["value"]:
                notes.append(f"{rel}: stat `{s['label']}` {s['value']} -> {match['value']} (updated)")
    if base["stats"] and len(cur["stats"]) < len(base["stats"]):
        notes.append(f"{rel}: stat count {len(base['stats'])} -> {len(cur['stats'])}")

    # tables
    cur_tables = [t["purpose"] + " " + " ".join(t["headers"]) for t in cur["tables"]]
    for t in base["tables"]:
        key = t["purpose"] + " " + " ".join(t["headers"])
        if best(key, cur_tables) < 0.55 and not any(
                set(map(norm, t["headers"])) & set(map(norm, x["headers"])) for x in cur["tables"]):
            losses.append(Loss(rel, "table", key[:100], f"{t['rows']} rows"))
    if len(cur["tables"]) < len(base["tables"]):
        notes.append(f"{rel}: table count {len(base['tables'])} -> {len(cur['tables'])}")

    # major blocks: heading must exist and must not shrink by more than 50%
    cur_blocks = cur["blocks"]
    for b in base["blocks"]:
        if not b["heading"]:
            continue
        cand = [x for x in cur_blocks if similar(x["heading"], b["heading"]) >= FUZZY]
        if not cand:
            # block may have been split/merged: fall back to a heading anywhere
            if best(b["heading"], cur_heads) < FUZZY:
                losses.append(Loss(rel, "block", b["heading"], f"{b['words']} words"))
            continue
        w = max(x["words"] for x in cand)
        if b["words"] >= 60 and w < BLOCK_KEEP * b["words"]:
            losses.append(Loss(rel, "block-shrink", b["heading"], f"{b['words']} -> {w} words"))

    # whole-page size guard
    if base["words"] >= 400 and cur["words"] < PAGE_KEEP * base["words"]:
        losses.append(Loss(rel, "page-shrink", rel, f"{base['words']} -> {cur['words']} words"))
    return losses, notes


def main() -> int:
    global BLOCK_KEEP, PAGE_KEEP
    ap = argparse.ArgumentParser()
    ap.add_argument("--page", action="append", help="limit to page(s)")
    ap.add_argument("--report")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--phase2", action="store_true",
                    help="compare against the PHASE1_BASE inventory with the strict 10%% shrink guard")
    args = ap.parse_args()

    baseline_path, disp_path = (PHASE2_BASELINE, PHASE2_DISPOSITIONS) if args.phase2 else (BASELINE, DISPOSITIONS)
    if args.phase2:
        BLOCK_KEEP = PAGE_KEEP = 0.9
    baseline_doc = json.loads(baseline_path.read_text(encoding="utf-8"))
    base = baseline_doc["pages"]
    baseline_label = baseline_doc.get("meta", {}).get("sha", "")[:7] or "baseline"
    dispositions = []
    if disp_path.exists():
        dispositions = json.loads(disp_path.read_text(encoding="utf-8"))["dispositions"]

    all_losses: list[Loss] = []
    all_notes: list[str] = []
    for rel, page in sorted(base.items()):
        if args.page and rel not in args.page:
            continue
        path = ROOT / rel
        cur = extract_page(path.read_text(encoding="utf-8"), rel) if path.exists() else None
        losses, notes = compare_page(rel, page, cur)
        all_losses += losses
        all_notes += notes

    unexplained, explained = [], []
    for loss in all_losses:
        for entry in dispositions:
            if loss.matches(entry):
                loss.disposition = entry
                break
        (explained if loss.disposition else unexplained).append(loss)

    phase = "Phase-2" if args.phase2 else "Phase-1"
    if not args.phase2:
        baseline_label = "be35902"
    lines = [f"# {phase} presentation comparison (baseline `{baseline_label}` vs working tree)", "",
             f"- baseline pages compared: {len(base) if not args.page else len(args.page)}",
             f"- unexplained losses: **{len(unexplained)}**",
             f"- dispositioned differences: **{len(explained)}**",
             f"- notes (updates/adjustments that are not losses): {len(all_notes)}", ""]
    if unexplained:
        lines += ["## Unexplained losses", ""]
        for l in unexplained:
            lines.append(f"- `{l.page}` [{l.kind}] {l.key}" + (f" — {l.detail}" if l.detail else ""))
        lines.append("")
    if explained:
        lines += ["## Dispositioned differences", "", "| Page | Kind | Item | Disposition | Reason |", "|---|---|---|---|---|"]
        for l in explained:
            d = l.disposition
            lines.append(f"| `{l.page}` | {l.kind} | {l.key[:90].replace('|', '/')} | {d.get('disposition', '')} | "
                         f"{d.get('reason', '').replace('|', '/')} |")
        lines.append("")
    if all_notes:
        lines += ["## Notes", ""] + [f"- {n}" for n in all_notes] + [""]
    text = "\n".join(lines) + "\n"
    if args.report:
        Path(args.report).write_text(text, encoding="utf-8")
    if not args.quiet:
        print(text if len(text) < 20000 else text[:20000] + "\n… (truncated; see --report)")
    else:
        print(f"unexplained losses: {len(unexplained)}; dispositioned: {len(explained)}; notes: {len(all_notes)}")
    return 1 if unexplained else 0


if __name__ == "__main__":
    sys.exit(main())
