#!/usr/bin/env python3
"""Presentation-preservation checks for owner-designated content.

These are deliberately structural, not prose-exact: they protect the parts of the
known-good site that the owner explicitly asked to keep, without freezing every byte.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from inventory_presentation import ROOT, extract_page  # noqa: E402

CNA_TARGET = "009d40f5dd085c4e674d3479675fac84b12b3e0a"
SPEEDY_BLUPI_URL = "https://speedyblupi.com/SpeedyBlupi2013/"
BASELINE = ROOT / "audit" / "data" / "phase1-baseline-inventory.json"


def page(rel: str) -> dict:
    return extract_page((ROOT / rel).read_text(encoding="utf-8"), rel)


def main() -> int:
    errors: list[str] = []
    ok: list[str] = []

    # --- cnahead -------------------------------------------------------------------
    raw = (ROOT / "cnahead").read_bytes() if (ROOT / "cnahead").exists() else b""
    if raw != (CNA_TARGET + "\n").encode():
        errors.append(f"cnahead must be exactly {CNA_TARGET} + one newline (got {raw!r})")
    else:
        ok.append("cnahead == TARGET + newline")

    # --- homepage Quick Stats -----------------------------------------------------
    home = page("index.html")
    big = [s for s in home["stats"] if s["kind"] == "big-number" and s["value"] and s["label"]]
    if len(big) < 6:
        errors.append(f"index.html Quick Stats: expected >= 6 stats with value+label, found {len(big)}")
    else:
        ok.append(f"index.html Quick Stats present ({len(big)} stats)")

    # --- showcase: real-XNA verification -------------------------------------------
    show = page("showcase.html")
    block = next((b for b in show["blocks"] if re.search(r"verification against the real xna", b["heading"], re.I)), None)
    if block is None:
        errors.append("showcase.html: section 'Verification against the real XNA runtime' missing")
    else:
        if block["words"] < 250:
            errors.append(f"showcase.html real-XNA verification section too thin ({block['words']} words < 250)")
        if block["cards"] < 3:
            errors.append(f"showcase.html real-XNA verification section has {block['cards']} cards (< 3)")
        if block["images"] < 4:
            errors.append(f"showcase.html real-XNA verification section shows {block['images']} oracle images (< 4)")
        if not errors or all("showcase" not in e for e in errors):
            ok.append(f"showcase.html real-XNA verification present ({block['words']} words, "
                      f"{block['cards']} cards, {block['images']} images)")

    # --- demos: Speedy Blupi ------------------------------------------------------------
    demos = page("demos.html")
    sb = next((b for b in demos["blocks"] if "speedy blupi" in b["heading"].lower()), None)
    if sb is None:
        errors.append("demos.html: Speedy Blupi section missing")
    else:
        if sb["words"] < 120:
            errors.append(f"demos.html Speedy Blupi section too thin ({sb['words']} words < 120)")
        if sb["cards"] < 3:
            errors.append(f"demos.html Speedy Blupi section has {sb['cards']} items (< 3)")
        ok.append(f"demos.html Speedy Blupi section present ({sb['words']} words, {sb['cards']} items)")
    play = [c for c in demos["ctas"] if c["href"] == SPEEDY_BLUPI_URL]
    if not play:
        errors.append(f"demos.html: no CTA to {SPEEDY_BLUPI_URL}")
    else:
        c = play[0]
        if c["role"] != "primary":
            errors.append(f"demos.html Speedy Blupi CTA is '{c['role']}', must stay primary (btn-primary)")
        if not re.search(r"play in browser", c["label"], re.I):
            errors.append(f"demos.html Speedy Blupi CTA label is '{c['label']}', must read 'Play in Browser'")
        if c["role"] == "primary" and re.search(r"play in browser", c["label"], re.I):
            ok.append("demos.html Speedy Blupi 'Play in Browser' is a primary CTA -> " + c["href"])

    # --- baseline primary CTAs: no silent downgrade or loss ---------------------------
    if BASELINE.exists():
        base = json.loads(BASELINE.read_text(encoding="utf-8"))["pages"]
        disp_path = ROOT / "audit" / "data" / "phase1-dispositions.json"
        disp = json.loads(disp_path.read_text(encoding="utf-8"))["dispositions"] if disp_path.exists() else []
        problems = 0
        total = 0
        for rel, p in base.items():
            cur = page(rel) if (ROOT / rel).exists() else None
            for c in p["ctas"]:
                if c["role"] != "primary":
                    continue
                total += 1
                same = [x for x in (cur["ctas"] if cur else []) if x["href"] == c["href"]]
                if same and any(x["role"] == "primary" for x in same):
                    continue
                if any(d.get("page") == rel and d.get("kind") in ("cta", "cta-downgrade")
                       and d.get("match", "").lower() in c["href"].lower() for d in disp):
                    continue
                problems += 1
                errors.append(f"{rel}: baseline primary CTA lost/downgraded without disposition: "
                              f"{c['label']} -> {c['href']}")
        if not problems:
            ok.append(f"all {total} baseline primary CTAs preserved (or dispositioned)")

    for line in ok:
        print("ok   ", line)
    for line in errors:
        print("FAIL ", line)
    print(f"presentation checks: {len(ok)} ok, {len(errors)} failed")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
