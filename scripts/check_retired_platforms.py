#!/usr/bin/env python3
"""Fail if public site content presents a retired CNA platform implementation as part of CNA.

CNA's direct Win32, X11 and Wayland platform implementations were retired (PLAT-142); SDL3 is the one windowing
implementation and reaches Windows, X11 and Wayland through SDL's own video drivers. The site describes the
current product only, so a public page may talk about Windows, X11 and Wayland as environments, about SDL's x11 /
wayland / windows video drivers, about native window handles (HWND, Display* + XID, wl_display* + wl_surface*,
NativeWindowSystem::X11, TryGetWayland, ...) and about Xvfb / Weston test servers -- but never about a CNA platform
backend of that name.

The retired set is DERIVED from the CNA registry at check time (cmake/PlatformSelection.cmake, the
_cna_platforms_retired list at the commit in cnahead), so a later retirement is picked up without editing this file.

Flagged in public content (every tracked/untracked file outside audit/, scripts/ and plan.md):
  * a selection of a retired value: CNA_PLATFORM=X11, -DCNA_PLATFORM=WAYLAND, set(CNA_PLATFORM WIN32 ...),
    CNA_PLATFORM_X11 (the compile definition), CNA_PLATFORM&nbsp;...;
  * the backend presented as CNA's: "native X11 platform/backend", "X11 platform implementation", "Win32 backend",
    "SDL-free X11", the backend classes (X11Platform, WaylandPlatform, Win32Platform) and their source directories
    (modules/platform/src/X11, .../Wayland, .../Win32 and the helpers only they used).

Usage: check_retired_platforms.py            (CNA clone: ../cna or $CNA_REPO)
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CNA_REPO = Path(os.environ.get("CNA_REPO") or ROOT.parent / "cna")
SKIP_DIRS = {"audit", "scripts", ".git", ".idea"}
SKIP_FILES = {"plan.md"}
TEXT_SUFFIX = {".html", ".json", ".xml", ".js", ".css", ".txt", ".md", ".svg", ""}
# the helper directories that only the retired backends used (removed together with them)
HELPER_DIRS = ("Xkb", "Freedesktop", "Linux", "Posix")
PRETTY = {"WIN32": "Win32", "X11": "X11", "WAYLAND": "Wayland"}


def retired_platforms() -> list[str]:
    head = (ROOT / "cnahead").read_text(encoding="utf-8").strip()
    try:
        text = subprocess.run(["git", "-C", str(CNA_REPO), "show", f"{head}:cmake/PlatformSelection.cmake"],
                              check=True, capture_output=True, text=True).stdout
    except (OSError, subprocess.CalledProcessError):
        raise SystemExit(f"cannot read cmake/PlatformSelection.cmake at {head[:8]} from {CNA_REPO} (set CNA_REPO)")
    m = re.search(r"set\(_cna_platforms_retired\s+([^)]*)\)", text)
    return sorted(set(re.findall(r"[A-Z][A-Z0-9_]+", m.group(1)))) if m else []


def patterns(retired: list[str]) -> list[tuple[re.Pattern[str], str]]:
    if not retired:
        return []
    up = "|".join(map(re.escape, retired))
    names = sorted({PRETTY.get(r, r.title()) for r in retired} | set(retired), key=len, reverse=True)
    nm = "|".join(map(re.escape, names))
    cls = "|".join(re.escape(PRETTY.get(r, r.title())) for r in retired)
    dirs = "|".join(re.escape(PRETTY.get(r, r.title())) for r in retired) + "|" + "|".join(HELPER_DIRS)
    gap = r"(?:\s|&nbsp;|<[^>]+>)*"     # whitespace and inline markup such as <code>...</code>
    sep = r"(?:\s|&nbsp;|<[^>]+>)+"     # the same, at least one (so DIRECTX11 is not "direct X11")
    return [
        (re.compile(r"CNA_PLATFORM" + gap + r"(?:=|:STRING=|" + gap + r")" + gap + r"[\"']?(?:" + up + r")\b"), "selects a retired CNA_PLATFORM value"),
        (re.compile(r"\bCNA_PLATFORM_(?:" + up + r")\b"), "names a retired platform compile definition"),
        (re.compile(r"\bset\(\s*CNA_PLATFORM\s+(?:" + up + r")\b"), "selects a retired CNA_PLATFORM value"),
        (re.compile(r"\b(?:native|direct|SDL-free)" + sep + r"(?:" + nm + r")\b(?!" + gap + r"(?:window|handle|display|surface|session|video|driver|server|event|key|desktop|environment|HWND))", re.I),
         "presents a native/direct/SDL-free Win32, X11 or Wayland CNA backend"),
        (re.compile(r"\b(?:" + nm + r")" + sep + r"(?:platform|backend)s?" + gap + r"(?:implementation|backend|module|harness|layer)?\b(?!" + gap + r"(?:driver|video))", re.I),
         "presents Win32, X11 or Wayland as a CNA platform/backend"),
        (re.compile(r"\b(?:" + cls + r")Platform\b"), "names a retired backend class"),
        (re.compile(r"modules/platform/src/(?:" + dirs + r")\b"), "links or names a retired backend source directory"),
        (re.compile(r"internals/platforms/(?:x11|wayland|win32)\.html"), "links a deleted platform internals page"),
    ]


def main() -> int:
    retired = retired_platforms()
    pats = patterns(retired)
    hits: list[str] = []
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
            for rx, why in pats:
                m = rx.search(line)
                if m:
                    hits.append(f"{rel.as_posix()}:{number}: {why}: …{line[max(0, m.start() - 60): m.end() + 60].strip()}…")
                    break
    for h in hits:
        print(h)
    print(f"retired-platform references in public content: {len(hits)} "
          f"(retired platform implementations derived from CNA: {', '.join(retired) or 'none'})")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
