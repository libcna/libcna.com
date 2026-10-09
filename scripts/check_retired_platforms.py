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

A second, semantic pass reads the visible text of every HTML page block by block and catches the shapes the line
patterns missed:
  * a list (comma, "and"/"or", slash or bare whitespace, as in a compact source tree "src/ Sdl3 X11 Wayland Win32
    Terminal Headless") that puts a retired backend name beside a current CNA implementation (SDL3, HEADLESS,
    TERMINAL) -- unless the list is about window systems (it also names Cocoa, UIKit, Android, the web, macOS or iOS),
    its head noun is a driver/handle/pointer/session/server/suite, or the clause frames the names as retired/refused;
  * "X11 (native sibling)", "Win32 native sibling";
  * a "Wayland backend" / "X11 platform" that SDL does not own ("SDL's Wayland backend" stays legal);
  * a CI statement that contradicts the workflows at cnahead: "no workflow runs a Wayland session" while
    .github/workflows/platform-ci.yml runs the SDL3 window suites under a private headless Weston (and the same for
    X11 under Xvfb). The workflow facts are read from the CNA clone, not stored here.
scripts/test_validators.py feeds the exact bypasses and the allowed SDL-driver / host / handle sentences through it.

Usage: check_retired_platforms.py            (CNA clone: ../cna or $CNA_REPO)
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_retired_renderers import visible_blocks  # noqa: E402
from tombstones import TOMBSTONES  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CNA_REPO = Path(os.environ.get("CNA_REPO") or ROOT.parent / "cna")
SKIP_DIRS = {"audit", "scripts", ".git", ".idea"}
SKIP_FILES = {"plan.md"}
TEXT_SUFFIX = {".html", ".json", ".xml", ".js", ".css", ".txt", ".md", ".svg", ""}
# the helper directories that only the retired backends used (removed together with them)
HELPER_DIRS = ("Xkb", "Freedesktop", "Linux", "Posix")
PRETTY = {"WIN32": "Win32", "X11": "X11", "WAYLAND": "Wayland"}


def cna_file(path: str) -> str:
    head = (ROOT / "cnahead").read_text(encoding="utf-8").strip()
    try:
        return subprocess.run(["git", "-C", str(CNA_REPO), "show", f"{head}:{path}"],
                              check=True, capture_output=True, text=True).stdout
    except (OSError, subprocess.CalledProcessError):
        raise SystemExit(f"cannot read {path} at {head[:8]} from {CNA_REPO} (set CNA_REPO)")


def retired_platforms() -> list[str]:
    text = cna_file("cmake/PlatformSelection.cmake")
    m = re.search(r"set\(_cna_platforms_retired\s+([^)]*)\)", text)
    return sorted(set(re.findall(r"[A-Z][A-Z0-9_]+", m.group(1)))) if m else []


def ci_window_systems() -> set[str]:
    """The window systems platform-ci.yml at cnahead really runs SDL3 on, each under its private server."""
    wf = cna_file(".github/workflows/platform-ci.yml")
    found = set()
    if re.search(r"Sdl3X11", wf) and re.search(r"\bxvfb\b", wf, re.I):
        found.add("X11")
    if re.search(r"Sdl3Wayland", wf) and re.search(r"\bweston\b", wf, re.I):
        found.add("Wayland")
    return found


# ---------------------------------------------------------------------------------------------
# semantic pass over visible text (see the module docstring)
# ---------------------------------------------------------------------------------------------
CURRENT_IMPL = r"SDL3|Sdl3|HEADLESS|Headless|TERMINAL|Terminal"
WINDOW_SYSTEM_ONLY = r"Windows|Cocoa|UIKit|Android|Web|macOS|iOS|Emscripten|browser"  # host OS / window-system names
OTHER_ITEMS = r"SDL12|EMSCRIPTEN|SDL2|SDL|Common|CNA"
NOT_CNA_HEADS = {"driver", "drivers", "video", "pointer", "pointers", "handle", "handles", "window", "windows",
                 "display", "displays", "session", "sessions", "server", "servers", "suite", "suites", "desktop",
                 "desktops", "selection", "selections", "connection", "connections", "packages", "package", "protocol",
                 "compositor", "compositors", "host", "hosts", "environment", "environments", "values", "value"}
RETIRED_FRAME = re.compile(r"\b(?:retired|refused|refuses|rejected|no longer|removed)\b", re.I)
SDL_OWNS = re.compile(r"\bSDL(?:3)?\s*['\u2019]s\s+(?:own\s+)?$")


def semantic_findings(html_text: str, retired: list[str], ci_systems: set[str]) -> list[tuple[str, str, str]]:
    """(reason, excerpt, core) for every retired backend the visible text presents as CNA's; core is the matched text."""
    if not retired:
        return []
    names = sorted({PRETTY.get(r, r.title()) for r in retired} | set(retired) | {"Xlib"}, key=len, reverse=True)
    ret = "|".join(map(re.escape, names))
    item = r"(?:" + "|".join((ret, CURRENT_IMPL, WINDOW_SYSTEM_ONLY, OTHER_ITEMS)) + r")"
    sep = r"(?:\s*(?:,\s*(?:and|or)\s+|,|/|\band\b|\bor\b)\s*|\s+)"
    run_rx = re.compile(r"(?<![\w/.-])" + item + r"(?:" + sep + item + r")+(?![\w])")
    out: list[tuple[str, str, str]] = []
    for block in visible_blocks(html_text):
        for run in run_rx.finditer(block):
            text = run.group(0)
            excerpt = block[max(0, run.start() - 70): run.end() + 50]
            has_retired = re.search(r"(?<![\w-])(?:" + ret + r")(?![\w-])", text)
            has_current = re.search(r"(?<![\w-])(?:" + CURRENT_IMPL + r")(?![\w-])", text)
            if not (has_retired and has_current) or re.search(r"(?<![\w-])(?:" + WINDOW_SYSTEM_ONLY + r")(?![\w-])", text):
                continue
            head_m = re.match(r"\s*([A-Za-z][\w-]*)", block[run.end():])
            if head_m and head_m.group(1).lower() in NOT_CNA_HEADS:
                continue
            before = block[max(0, run.start() - 120): run.start()]
            before = before[max((m.end() for m in re.finditer(r"[.;!?](?:\s|$)", before)), default=0):]
            if RETIRED_FRAME.search(before) or SDL_OWNS.search(before):
                continue
            out.append(("lists a retired CNA platform backend beside the current implementations", excerpt, text))
        for m in re.finditer(r"\b(?:" + ret + r")\b\W{0,4}(?:\(\s*)?native sibling|native sibling\W{0,4}(?:\(\s*)?\b(?:" + ret + r")\b", block):
            out.append(("presents a retired backend as a native sibling of SDL3", block[max(0, m.start() - 60): m.end() + 40], m.group(0)))
        for m in re.finditer(r"\b(?:" + ret + r")\s+(?:platform\s+)?(?:backend|lane|job|cell|leg|tuple)s?\b", block):
            if SDL_OWNS.search(block[max(0, m.start() - 30): m.start()]):
                continue                                    # SDL's Wayland backend is SDL's
            out.append(("presents a retired backend, or a CI lane of one, as CNA's", block[max(0, m.start() - 60): m.end() + 40], m.group(0)))
        for system in sorted(ci_systems):
            claim = re.compile(r"\bno (?:CI |automatic |automated )?(?:workflow|job|lane)s?\b(?:(?!workflow|\bjob|\blane)[^.;]){0,90}?\b(?:a |any |native )?"
                               + system + r"\b", re.I)  # stops where another workflow is named
            for m in claim.finditer(block):
                out.append((f"says no workflow covers {system}, but platform-ci.yml at cnahead runs SDL3 on {system}",
                            block[max(0, m.start() - 40): m.end() + 40], m.group(0)))
    return out


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
        (re.compile(r"(?<!SDL's )(?<!SDL\u2019s )(?<!SDL3's )(?<!SDL3\u2019s )\b(?:" + nm + r")" + sep + r"(?:platform|backend)s?" + gap + r"(?:implementation|backend|module|harness|layer)?\b(?!" + gap + r"(?:driver|video))", re.I),
         "presents Win32, X11 or Wayland as a CNA platform/backend"),
        (re.compile(r"\b(?:" + cls + r")Platform\b"), "names a retired backend class"),
        (re.compile(r"modules/platform/src/(?:" + dirs + r")\b"), "links or names a retired backend source directory"),
        (re.compile(r"(?<![\w-])src/(?:Platform/)?(?:" + "|".join(re.escape(PRETTY.get(r, r.title())) for r in retired) + r")/?(?![\w-])"),
         "names a retired backend source directory"),
        (re.compile(r"internals/platforms/(?:x11|wayland|win32)\.html"), "links a retired platform internals page (its URL holds only a tombstone)"),
    ]


def main() -> int:
    retired = retired_platforms()
    ci_systems = ci_window_systems()
    pats = patterns(retired)
    hits: list[str] = []
    for path in sorted(ROOT.rglob("*")):
        rel = path.relative_to(ROOT)
        if not path.is_file() or set(rel.parts) & SKIP_DIRS or rel.as_posix() in SKIP_FILES:
            continue
        if path.suffix.lower() not in TEXT_SUFFIX or rel.as_posix() in TOMBSTONES:
            continue  # a tombstone names its retired subject on purpose; scripts/tombstones.py checks it instead
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if path.suffix.lower() == ".html":
            hits += [f"{rel.as_posix()}: {why}: \u2026{excerpt.strip()}\u2026" for why, excerpt, _core in semantic_findings(text, retired, ci_systems)]
        for number, line in enumerate(text.splitlines(), 1):
            for rx, why in pats:
                m = rx.search(line)
                if m:
                    hits.append(f"{rel.as_posix()}:{number}: {why}: …{line[max(0, m.start() - 60): m.end() + 60].strip()}…")
                    break
    for h in hits:
        print(h)
    print(f"retired-platform references in public content: {len(hits)} "
          f"(retired platform implementations derived from CNA: {', '.join(retired) or 'none'}; "
          f"window systems platform-ci.yml runs SDL3 on: {', '.join(sorted(ci_systems)) or 'none'})")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
