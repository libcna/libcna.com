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
  * a "Wayland backend" / "X11 platform" / "Win32 implementation" that SDL does not own ("SDL's Wayland backend" stays legal);
  * a sentence about CNA's platform implementations that names a retired backend as one of them, even outside a list:
    "Some implementations are host-conditional (Terminal is POSIX-only, Win32 Windows-only, X11 and Wayland need their
    development packages)" -- the sentence the generator wrote at f412fa0. Legal when the sentence says SDL reaches the
    window system ("through SDL's own video drivers", "SDL3 on X11"), names it as a host/window-system environment beside
    Windows/macOS/..., denies it is an implementation, frames it as retired/refused, or uses it as the modifier of a
    non-CNA noun ("an X11 or Wayland surface", "the X11 native handle");
  * a table cell holding only a retired name in a column of platform implementations (by caption, header or nearest
    heading, or because the column's other cells are SDL3 / HEADLESS / TERMINAL), unless its row says it is retired;
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
                 "compositor", "compositors", "host", "hosts", "environment", "environments", "values", "value",
                 "surface", "surfaces", "socket", "sockets", "event", "events", "atom", "atoms", "visual", "visuals",
                 "keysym", "keysyms", "scancode", "scancodes", "native", "client", "clients", "extension", "extensions",
                 "development", "headers", "header", "libraries", "library", "dependencies", "dependency", "support"}
IMPL_NOUN = re.compile(r"\b(?:platform\s+)?implementations?\b|\bplatform\s+(?:layer|backend|module|integration)s?\b|\bbackends?\b|"
                       r"\bhost-conditional\b", re.I)
NEGATED_IMPL = re.compile(r"\b(?:not|no longer|never)\b[^.;]{0,40}\b(?:an?\s+)?(?:CNA\s+)?(?:platform\s+)?(?:implementations?|backends?)\b", re.I)
RETIRED_FRAME = re.compile(r"\b(?:retired|refused|refuses|rejected|no longer|removed)\b", re.I)
SDL_OWNS = re.compile(r"\bSDL(?:3)?\s*['\u2019]s\s+(?:own\s+)?$")


def semantic_findings(html_text: str, retired: list[str], ci_systems: set[str]) -> list[tuple[str, str, str]]:
    """(reason, excerpt, core) for every retired backend the visible text presents as CNA's; core is the matched text."""
    if not retired:
        return []
    names = sorted({PRETTY.get(r, r.title()) for r in retired} | set(retired) | {"Xlib"}, key=len, reverse=True)
    ret = "|".join(map(re.escape, names))
    item = r"(?:" + "|".join((ret, CURRENT_IMPL, WINDOW_SYSTEM_ONLY, OTHER_ITEMS)) + r")"
    sep = r"(?:\s*(?:,\s*(?:and|or)\s+|,|/|\u00b7|\||\band\b|\bor\b)\s*|\s+)"
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
        out += _ownership_findings(block, ret)
        for system in sorted(ci_systems):
            claim = re.compile(r"\bno (?:CI |automatic |automated )?(?:workflow|job|lane)s?\b(?:(?!workflow|\bjob|\blane)[^.;]){0,90}?\b(?:a |any |native )?"
                               + system + r"\b", re.I)  # stops where another workflow is named
            for m in claim.finditer(block):
                out.append((f"says no workflow covers {system}, but platform-ci.yml at cnahead runs SDL3 on {system}",
                            block[max(0, m.start() - 40): m.end() + 40], m.group(0)))
    return out + platform_cells(html_text, retired) + _item_list_findings(visible_blocks(html_text), ret)


def _ownership_findings(block: str, ret: str) -> list[tuple[str, str, str]]:
    """A retired backend named inside a sentence about CNA's platform implementations (see the module docstring). The
    exemptions must hold for the name itself: SDL framing or a denial in the name's own clause, an environment name
    (Windows, macOS, ...) in the name's own list, a non-CNA head noun right after the name's list."""
    name_rx = re.compile(r"(?<![\w-])(?:" + ret + r")(?![\w-])")
    sdl_reached = re.compile(r"\bSDL3?(?:['\u2019]s)?\b(?:(?!\bCNA\b)[^.;]){0,80}?\bdrivers?\b|\bvideo drivers?\b|\b(?:through|via)\s+SDL|"
                             r"\bSDL3?\s+(?:on|over|under|through|via)\s+(?:the\s+|an?\s+)?(?:" + ret + r")\b", re.I)
    sep = r"(?:\s*(?:,\s*(?:and|or)\s+|,|/|\u00b7|\||\band\b|\bor\b)\s*(?:on\s+)?)"
    item = r"(?:" + "|".join((ret, CURRENT_IMPL, WINDOW_SYSTEM_ONLY, OTHER_ITEMS, r"Cocoa|UIKit|Linux")) + r")"
    list_rx = re.compile(r"(?<![\w-])" + item + r"(?:" + sep + item + r")*(?![\w-])")
    environment = re.compile(r"(?<![\w-])(?:" + WINDOW_SYSTEM_ONLY + r"|Cocoa|UIKit|Linux)(?![\w-])")
    out = []
    sentences = re.split(r"(?<=[.!?])\s+", block)
    for k, sentence in enumerate(sentences):
        # the implementation noun may stand in the sentence before ("Compare implementations of one contract. For the
        # platform, compare SDL3 with Win32 or X11, and contrast Headless.")
        if not name_rx.search(sentence) or not (IMPL_NOUN.search(sentence) or (k and IMPL_NOUN.search(sentences[k - 1]))):
            continue
        for m in name_rx.finditer(sentence):
            delim = r"[;:()\u2014]|,\s+(?=(?:unlike|while|whereas|but|which|although)\b)"
            a = max((x.end() for x in re.finditer(delim, sentence[:m.start()])), default=0)
            b = re.search(delim, sentence[m.end():])
            clause = sentence[a: m.end() + (b.start() if b else len(sentence))]
            run = next((r for r in list_rx.finditer(sentence) if r.start() <= m.start() < r.end()), None)
            # the head noun after the whole list the name stands in ("the X11, GL, Vulkan, ALSA and D-Bus development packages")
            tail = re.match(r"(?:\s*(?:,\s*(?:and|or)\s+|,|/|\band\b|\bor\b)\s*[A-Z][\w-]*(?:\s+\d+(?:\.\d+)?)?)*\s*([A-Za-z][\w-]*)?",
                            sentence[run.end() if run else m.end():])
            head = (tail.group(1) or "").lower()
            if re.match(r"\s*(?:wl_\w+|xcb_\w+|Display\b|XID\b|Window\b|HWND\b)", sentence[m.end():]):
                continue                                    # "an X11 Display* and window", "a Wayland wl_display*": native handles
            before_all = sentence[:m.start()]
            if before_all.count("\u201c") > before_all.count("\u201d") or before_all.count('"') % 2:
                continue                                    # inside a quoted message ("this session is not running X11/Wayland")
            if sdl_reached.search(clause) or NEGATED_IMPL.search(clause) or (run and environment.search(run.group(0))):
                continue
            if head in NOT_CNA_HEADS or RETIRED_FRAME.search(sentence[a:m.start()]) or SDL_OWNS.search(sentence[:m.start()]):
                continue
            if re.match(r"\s*(?:are\s+|is\s+|stay\s+|remain\s+)?(?:still\s+)?(?:refused|rejected|fail|fails|retired|removed|no longer)\b",
                        sentence[run.end() if run else m.end():]):
                continue                                    # "WIN32, X11 and WAYLAND fail with a message that says to configure SDL3"
            if re.search(r"(?:\b(?:OR|AND|NOT)|\bif\s*\()\s*$", sentence[:m.start()]) or re.match(r"\s*(?:OR|AND)\b", sentence[m.end():]):
                continue                                    # CMake's WIN32 host variable in a condition ("MINGW OR WIN32")
            out.append(("names a retired backend in a sentence about CNA's platform implementations", sentence[:240], sentence))
            break
    return out


def _item_list_findings(blocks: list[str], ret: str) -> list[tuple[str, str, str]]:
    """Consecutive blocks that are each nothing but one name (<li>SDL3</li><li>X11</li><li>Headless</li>): the same list
    test as the inline pass, across blocks, unless the introducing block frames the names as retired or as handles/drivers."""
    item = re.compile(r"^\s*(?:" + ret + r"|" + CURRENT_IMPL + r"|" + WINDOW_SYSTEM_ONLY + r"|Cocoa|UIKit)\s*[,.;]?\s*$")
    out, i = [], 0
    while i < len(blocks):
        if not item.match(blocks[i]):
            i += 1
            continue
        j = i
        while j < len(blocks) and item.match(blocks[j]):
            j += 1
        group, intro = " ".join(blocks[i:j]), blocks[i - 1] if i else ""
        has_retired = re.search(r"(?<![\w-])(?:" + ret + r")(?![\w-])", group)
        has_current = re.search(r"(?<![\w-])(?:" + CURRENT_IMPL + r")(?![\w-])", group)
        environment = re.search(r"(?<![\w-])(?:" + WINDOW_SYSTEM_ONLY + r"|Cocoa|UIKit)(?![\w-])", group)
        framed = RETIRED_FRAME.search(intro) or re.search(r"\b(?:drivers?|handles?|NativeWindowSystem|window systems?|sessions?)\b", intro, re.I)
        if j - i > 1 and has_retired and has_current and not environment and not framed:
            out.append(("lists a retired CNA platform backend beside the current implementations (one name per item)", f"{intro[:60]} \u2026 {group}", group))
        i = j
    return out


def platform_cells(html_text: str, retired: list[str]) -> list[tuple[str, str, str]]:
    """A table cell holding only a retired backend name in a column of CNA platform implementations."""
    from bs4 import BeautifulSoup
    names = sorted({PRETTY.get(r, r.title()) for r in retired} | set(retired), key=len, reverse=True)
    whole = re.compile(r"^\s*(?:" + "|".join(map(re.escape, names)) + r")\s*$")
    current = re.compile(r"^\s*(?:" + CURRENT_IMPL + r")\s*$")
    environment = re.compile(r"^\s*(?:" + WINDOW_SYSTEM_ONLY + r"|Cocoa|UIKit|Linux)\b")
    impl_context = re.compile(r"\bimplementations?\b|\bCNA_PLATFORM\b|\bplatform\s+(?:backends?|layers?|values?)\b", re.I)
    not_impl_header = re.compile(r"\b(?:drivers?|handles?|window\s+systems?|systems?|sessions?|hosts?|servers?|OS|environments?)\b", re.I)
    out = []
    soup = BeautifulSoup(html_text, "html.parser")
    for table in soup.find_all("table"):
        first = table.find("tr")
        headers = [c.get_text(" ", strip=True) for c in first.find_all(["th", "td"])] if first and first.find("th") else []
        heading = table.find_previous(["h1", "h2", "h3", "h4"])
        caption = table.find("caption")
        context = " ".join([heading.get_text(" ") if heading else "", caption.get_text(" ") if caption else ""])
        rows = [[c.get_text(" ", strip=True) for c in tr.find_all(["th", "td"])] for tr in table.find_all("tr")]
        for row in rows:
            for col, cell in enumerate(row):
                if not whole.match(cell) or RETIRED_FRAME.search(" ".join(row)) or re.search(r"\buse SDL3\b", " ".join(row)):
                    continue
                head = headers[col] if col < len(headers) else ""
                column = [r[col] for r in rows if r is not row and col < len(r)]
                if not_impl_header.search(head) or any(environment.match(c) for c in column):
                    continue                                # a column of window systems, hosts or drivers
                if impl_context.search(head) or (not head and impl_context.search(context)) or any(current.match(c) for c in column):
                    out.append((f"table cell '{cell}' in a column of CNA platform implementations", " | ".join(row)[:160], " ".join(row)[:80]))
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
        (re.compile(r"(?<!SDL's )(?<!SDL\u2019s )(?<!SDL3's )(?<!SDL3\u2019s )\b(?:" + nm + r")" + sep + r"(?:platform|backend|implementation)s?" + gap + r"(?:implementation|backend|module|harness|layer)?\b(?!" + gap + r"(?:driver|video))", re.I),
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
