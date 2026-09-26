#!/usr/bin/env python3
"""Fail if public site content still names a renderer identity that CNA has retired.

The retired set is DERIVED from the CNA registries at check time and is never stored in this
repository (the site does not publish a retired-renderer catalogue):

    retired = (identities in BASE cmake/RendererSelection.cmake STRINGS list)
              - (identities in TARGET cmake/RendererIdentities.cmake public list)
              + (TARGET's own retired list)

Usage:
    check_retired_renderers.py [--base DIR] [--target DIR]

Defaults: $CNA_BASE_TREE and $CNA_TARGET_TREE, else ~/.cache/libcna-com/cna-base and cna-target
(create them with scripts/extract_cna_trees.sh).

Public content = every tracked/untracked file outside audit/, scripts/ and plan.md.
Ordinary English words that double as identities (Magnum, Wicked, Glide, Sokol, Diligent) are only
flagged in identity-like spellings (all caps, CMake option form, or module-directory form).
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_CACHE = Path(os.environ.get("XDG_CACHE_HOME") or Path.home() / ".cache") / "libcna-com"
BASE_TREE = Path(os.environ.get("CNA_BASE_TREE") or _CACHE / "cna-base")      # CNA at the v0.1.0-alpha.1 baseline
TARGET_TREE = Path(os.environ.get("CNA_TARGET_TREE") or _CACHE / "cna-target")  # CNA at the commit in cnahead
WORDS = {"MAGNUM", "WICKED", "SOKOL", "DILIGENT", "GLIDE", "IGL"}
SKIP_DIRS = {"audit", "scripts", ".git", ".idea"}
SKIP_FILES = {"plan.md"}
TEXT_SUFFIX = {".html", ".json", ".xml", ".js", ".css", ".txt", ".md", ".svg", ""}


def quoted_list(text: str, marker: str) -> list[str]:
    i = text.index(marker)
    j = text.index(")", i)
    return re.findall(r"[A-Z][A-Z0-9_]+", text[i + len(marker): j])


def derive(base: Path, target: Path) -> set[str]:
    base_sel = (base / "cmake/RendererSelection.cmake").read_text(encoding="utf-8")
    strings = re.search(r'set_property\(CACHE CNA_GRAPHICS_RENDERER PROPERTY STRINGS ([^)]*)\)', base_sel).group(1)
    base_ids = set(re.findall(r'"([A-Z0-9_]+)"', strings))
    ident = (target / "cmake/RendererIdentities.cmake").read_text(encoding="utf-8")
    public = set(quoted_list(ident, "set(CNA_RENDERER_PUBLIC_IDENTITIES"))
    retired_decl = re.search(r"set\(CNA_RENDERER_RETIRED_IDENTITIES(.*?)\)", ident, re.S).group(1)
    retired = {m.group(1) for m in re.finditer(r"([A-Z][A-Z0-9_]+)=\d+", retired_decl)}
    return (base_ids - public) | retired


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=str(BASE_TREE))
    ap.add_argument("--target", default=str(TARGET_TREE))
    args = ap.parse_args()
    retired = derive(Path(args.base), Path(args.target))
    strong = sorted(i for i in retired if i not in WORDS)
    weak = sorted(i for i in retired if i in WORDS)
    strong_rx = re.compile(r"(?<![A-Za-z0-9_])(" + "|".join(map(re.escape, strong)) + r")(?![A-Za-z0-9_])", re.I)
    # also the CamelCase enum spellings of the strong set, e.g. OpenGLES1 / DirectX7 / Blend2D / NanoVg
    weak_rx = re.compile(r"(?<![A-Za-z0-9_])(" + "|".join(map(re.escape, weak)) + r")(?![A-Za-z0-9_])") if weak else None
    weak_form = re.compile(r"CNA_RENDERER_(" + "|".join(map(re.escape, weak)) + r")\b|renderers/(" + "|".join(x.lower() for x in weak) + r")\b") if weak else None

    hits: list[tuple[str, int, str]] = []
    for path in sorted(ROOT.rglob("*")):
        rel = path.relative_to(ROOT)
        if not path.is_file() or set(rel.parts) & SKIP_DIRS or rel.as_posix() in SKIP_FILES:
            continue
        if path.suffix.lower() not in TEXT_SUFFIX:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for number, line in enumerate(text.splitlines(), 1):
            m = strong_rx.search(line)
            if m is None and weak_rx is not None:
                m = weak_rx.search(line) if re.search(r"[A-Z]{4,}", line) else None
                if m is None and weak_form:
                    m = weak_form.search(line)
            if m:
                hits.append((rel.as_posix(), number, line.strip()[:140]))
    for rel, number, line in hits:
        print(f"{rel}:{number}: {line}")
    print(f"retired-renderer references in public content: {len(hits)} "
          f"({len(retired)} retired identities derived from the CNA registries)")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
