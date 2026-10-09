#!/usr/bin/env python3
"""Fail if public site content still names a renderer identity that CNA has retired.

The retired set is DERIVED from the CNA registries at check time and is never stored in this
repository (the site does not publish a retired-renderer catalogue):

    retired = (identities in BASE cmake/RendererSelection.cmake STRINGS list)
              - (identities in TARGET cmake/RendererIdentities.cmake public list)
              + (TARGET's own retired list)

Usage:
    check_retired_renderers.py [--base DIR] [--target DIR]

Sources, in order: --base/--target (or $CNA_BASE_TREE / $CNA_TARGET_TREE) when given and present;
otherwise the Git objects of the CNA clone (../cna or $CNA_REPO) at the alpha.1 baseline and at the
commit in cnahead, which need no extracted tree; otherwise ~/.cache/libcna-com/cna-base and cna-target
(created by scripts/extract_cna_trees.sh). The scan therefore runs wherever the CNA clone is present.

Public content = every tracked/untracked file outside audit/, scripts/ and plan.md.
Ordinary English words that double as identities (Magnum, Wicked, Glide, Sokol, Diligent, Canvas) are only
flagged in identity-like spellings (all caps, CMake option form, or module-directory form); the HTML <canvas>
element a browser build draws into is not an identity.

Retired identities also have prose names that the identity spelling does not cover ("the Canvas renderer",
"Direct3D 12 backend", "WebGL 1", "OpenGL ES 2", "Direct3D 9/11/12"). Those are flagged when they are presented as a
CNA renderer: followed by renderer/backend/identity/family, listed as a sibling of current renderers, or joined to
Direct3D 11 as one renderer list. SDL_GPU's Direct3D 12 *driver*, meta-gl's GLES 2.0 entry points and WebGL 1/2
context flags are other projects' facts and stay legal.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_CACHE = Path(os.environ.get("XDG_CACHE_HOME") or Path.home() / ".cache") / "libcna-com"
BASE_TREE = Path(os.environ.get("CNA_BASE_TREE") or _CACHE / "cna-base")      # CNA at the v0.1.0-alpha.1 baseline
TARGET_TREE = Path(os.environ.get("CNA_TARGET_TREE") or _CACHE / "cna-target")  # CNA at the commit in cnahead
CNA_REPO = Path(os.environ.get("CNA_REPO") or ROOT.parent / "cna")
BASE_SHA = "1bb2145d99ed572dd4eb15009c34e2e5f410fcf0"  # tag v0.1.0-alpha.1 (same constant as extract_cna_trees.sh)
WORDS = {"MAGNUM", "WICKED", "SOKOL", "DILIGENT", "GLIDE", "IGL", "CANVAS"}
# prose names of retired identities whose CMake spelling the strong pattern cannot see; each is checked only if the
# identity is in the derived retired set, so a name that is (re)admitted stops being flagged without editing this file
PROSE = {
    "CANVAS": r"Canvas(?:2D)?",
    "DIRECTX12": r"(?:Direct3D|DirectX|D3D)[ -]?12|DX12",
    "WEBGL1": r"WebGL[ -]?1(?:\.0)?",
    "OPENGLES2": r"OpenGL[ -]?ES[ -]?2(?:\.0)?|GLES[ -]?2(?:\.0)?",
}
_GAP = r"(?:\s|&nbsp;|<[^>]+>|\))*"
_CURRENT = r"(?:WebGL[ -]?2|WebGPU|SDL_Renderer|SDL_GPU|Software|Headless|Stub|Metal|Vulkan|EasyGL|FNA3D|OpenGL[ -]?ES[ -]?3|OpenGL[ -]?3\.?3)"
SKIP_DIRS = {"audit", "scripts", ".git", ".idea"}
SKIP_FILES = {"plan.md"}
TEXT_SUFFIX = {".html", ".json", ".xml", ".js", ".css", ".txt", ".md", ".svg", ""}


def quoted_list(text: str, marker: str) -> list[str]:
    i = text.index(marker)
    j = text.index(")", i)
    return re.findall(r"[A-Z][A-Z0-9_]+", text[i + len(marker): j])


def git_show(rev: str, path: str) -> str | None:
    try:
        return subprocess.run(["git", "-C", str(CNA_REPO), "show", f"{rev}:{path}"], check=True,
                              capture_output=True, text=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return None


def sources(base: Path | None, target: Path | None) -> tuple[str, str, str] | None:
    """(base RendererSelection.cmake, target RendererIdentities.cmake, where they came from)."""
    if base and target and (base / "cmake").is_dir() and (target / "cmake").is_dir():
        return ((base / "cmake/RendererSelection.cmake").read_text(encoding="utf-8"),
                (target / "cmake/RendererIdentities.cmake").read_text(encoding="utf-8"), f"trees {base} and {target}")
    head = (ROOT / "cnahead").read_text(encoding="utf-8").strip()
    b, t = git_show(BASE_SHA, "cmake/RendererSelection.cmake"), git_show(head, "cmake/RendererIdentities.cmake")
    if b and t:
        return b, t, f"Git objects of {CNA_REPO} at {BASE_SHA[:8]} and {head[:8]}"
    return None


def derive_text(base_sel: str, ident: str) -> set[str]:
    strings = re.search(r'set_property\(CACHE CNA_GRAPHICS_RENDERER PROPERTY STRINGS ([^)]*)\)', base_sel).group(1)
    base_ids = set(re.findall(r'"([A-Z0-9_]+)"', strings))
    public = set(quoted_list(ident, "set(CNA_RENDERER_PUBLIC_IDENTITIES"))
    retired_decl = re.search(r"set\(CNA_RENDERER_RETIRED_IDENTITIES(.*?)\)", ident, re.S).group(1)
    retired = {m.group(1) for m in re.finditer(r"([A-Z][A-Z0-9_]+)=\d+", retired_decl)}
    return (base_ids - public) | retired


def derive(base: Path | None = None, target: Path | None = None) -> set[str]:
    """The retired set. Callers pass the extracted trees (kept for compatibility); when those are absent or stale the
    CNA Git objects at the alpha.1 baseline and at cnahead are read instead."""
    src = sources(base, target) if base and target and _tree_current(target) else None
    src = src or sources(None, None) or sources(BASE_TREE, TARGET_TREE)
    if src is None:
        raise SystemExit(f"cannot derive the retired renderer set: no CNA clone at {CNA_REPO} (set CNA_REPO) and no extracted trees")
    return derive_text(src[0], src[1])


def _tree_current(target: Path) -> bool:
    stamp = target / ".extracted-from"
    head = (ROOT / "cnahead").read_text(encoding="utf-8").strip()
    return not stamp.exists() or stamp.read_text(encoding="utf-8").strip() == head


def strong_pattern(strong: list[str]) -> re.Pattern[str]:
    """Every spelling of a retired identity: the CMake name, its module-directory and prose forms (HTML_DOM, html-dom,
    HTML DOM, HtmlDom) and a CamelCase prefix such as Direct2DRenderer or OpenGL4Modern. Matching ignores case except
    for the character after the name, which may only be an upper-case letter (a CamelCase continuation) or a non-word
    character, so gdi32 or OpenGL4x are not spellings of an identity."""
    forms = set()
    for ident in strong:
        forms |= {ident, ident.replace("_", "-"), ident.replace("_", " "), ident.replace("_", "")}
    alt = "|".join(sorted((re.escape(f) for f in forms), key=len, reverse=True))
    return re.compile(r"(?<![A-Za-z0-9_])(?i:(" + alt + r"))(?![a-z0-9_])")


def prose_pattern(retired: set[str]) -> re.Pattern[str] | None:
    names = [PROSE[i] for i in sorted(retired) if i in PROSE]
    if not names:
        return None
    nm = "(?:" + "|".join(names) + ")"
    role = r"(?:renderers?|backends?|identit(?:y|ies)|famil(?:y|ies)|profiles?)\b"
    return re.compile(
        r"(?<![A-Za-z0-9_])" + nm + r"(?![A-Za-z0-9_])" + _GAP + r"(?:/" + _GAP + r"(?:WebGL[ -]?2|2)" + _GAP + r")?" + role  # "Canvas renderer", "WebGL 1/2 profiles"
        + r"|(?:Direct3D|DirectX|D3D|DIRECTX)[ -]?(?:9[ ,/]+)?11" + _GAP + r"(?:/|,|and|&amp;)" + _GAP + r"12\b"               # "Direct3D 9/11/12", "Direct3D 11 and 12"
        + r"|\b" + _CURRENT + r"(?:</code>)?" + _GAP + r"(?:,|and|or)" + _GAP + r"(?:<code>)?" + nm + r"(?![A-Za-z0-9_])(?!" + _GAP + r"(?:element|API|context|surface|canvas|drivers?|devices?))"
        + r"|(?<![A-Za-z0-9_])" + nm + r"(?:</code>)?" + _GAP + r"(?:,|and|or)" + _GAP + r"(?:<code>)?" + _CURRENT + r"\b(?!" + _GAP + r"(?:drivers?|devices?|context))")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=os.environ.get("CNA_BASE_TREE"))
    ap.add_argument("--target", default=os.environ.get("CNA_TARGET_TREE"))
    args = ap.parse_args()
    src = (sources(Path(args.base) if args.base else None, Path(args.target) if args.target else None)
           or sources(None, None) or sources(BASE_TREE, TARGET_TREE))
    if src is None:
        print(f"cannot derive the retired set: no CNA clone at {CNA_REPO} (set CNA_REPO) and no extracted trees")
        return 2
    retired = derive_text(src[0], src[1])
    head = (ROOT / "cnahead").read_text(encoding="utf-8").strip()
    if "trees" in src[2]:
        stamp = Path(args.target or TARGET_TREE) / ".extracted-from"
        if stamp.exists() and stamp.read_text().strip() != head:
            print(f"extracted target tree is {stamp.read_text().strip()[:8]}, cnahead is {head[:8]}: re-run scripts/extract_cna_trees.sh")
            return 2
    strong = sorted(i for i in retired if i not in WORDS)
    weak = sorted(i for i in retired if i in WORDS)
    strong_rx = strong_pattern(strong)
    # also the CamelCase enum spellings of the strong set, e.g. OpenGLES1 / DirectX7 / Blend2D / NanoVg
    weak_rx = re.compile(r"(?<![A-Za-z0-9_])(" + "|".join(map(re.escape, weak)) + r")(?![A-Za-z0-9_])") if weak else None
    prose_rx = prose_pattern(retired)
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
            if m is None and prose_rx is not None:
                m = prose_rx.search(line)
            if m:
                hits.append((rel.as_posix(), number, line.strip()[:140]))
    for rel, number, line in hits:
        print(f"{rel}:{number}: {line}")
    print(f"retired-renderer references in public content: {len(hits)} "
          f"({len(retired)} retired identities derived from the CNA registries, read from {src[2]})")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
