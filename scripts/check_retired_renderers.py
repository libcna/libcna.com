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

The line patterns above see a name and its immediate neighbour only, so a prose name inside a longer list slipped
through ("DirectX 9, DirectX 11 and DirectX 12 report loss", "(EasyGL, WebGPU, SDL_GPU, DirectX 11 and DirectX 12)",
"the Direct3D 12 and SDL GPU renderers", a table row whose Family cell is "Direct3D 12"). The semantic pass reads the
visible text of every HTML page block by block, takes the whole list a retired prose name stands in, and decides
by what the list is about:
  * allowed when the list's head noun is a driver, API, device, debug layer, library or other non-renderer noun,
    when the name is possessed ("Direct3D 12's upload path"), or when SDL owns it ("SDL's Direct3D 12 driver");
  * flagged when the head noun is renderer/backend/identity/family/profile/implementation, when the list also names a
    current CNA renderer that is not also an API name (EasyGL, SDL_GPU, FNA3D, Software, Headless, Stub, or any
    identity in CMake spelling), when the clause before it is about renderers, families, identities or
    registrations, or when CNA itself is said to accept/support/offer it;
  * flagged when a table cell holds nothing but the retired name in a column headed Family/Renderer/Identity/Backend
    (or, without such a header, in a column whose other cells are current renderers).
scripts/test_validators.py feeds the exact bypasses and the legitimate SDL-driver sentences through it.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tombstones import TOMBSTONES  # noqa: E402

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


# ---------------------------------------------------------------------------------------------
# semantic pass over the visible text of HTML pages (see the module docstring)
# ---------------------------------------------------------------------------------------------
BLOCK = "¶"
BLOCK_TAGS = ["p", "li", "td", "th", "dd", "dt", "h1", "h2", "h3", "h4", "h5", "h6", "caption", "figcaption", "pre",
              "tr", "br", "div", "section", "article", "blockquote", "summary", "title", "option", "label"]
# current CNA renderers whose names are not also the name of a graphics API another project implements
CURRENT_CNA_ONLY = (r"EasyGL|SDL[_ ]GPU|SDL[_ ]Renderer|FNA3D|Software|Headless|Stub|OPENGLES3|OPENGL33|WEBGL2|VULKAN|WEBGPU|"
                    r"METAL|SDL_RENDERER|DIRECTX9|DIRECTX11|HEADLESS|SOFTWARE|STUB")
# names that can be a CNA renderer or a graphics API (or another project's driver), so they only extend a list
API_LIKE = (r"(?:Direct3D|DirectX|D3D)[ -]?\d+(?:\s*/\s*\d+)*|DX\d+|Vulkan|Metal|WebGPU|WebGL[ -]?\d(?:\.\d)?|WebGL|"
            r"OpenGL(?:[ -]?ES)?[ -]?\d(?:\.\d)?|OpenGL(?:[ -]?ES)?|GLES[ -]?\d(?:\.\d)?|Canvas(?:2D)?")
LIST_SEP = r"\s*(?:,\s*(?:and|or)\s+|,|/|&|\band\b|\bor\b|\bplus\b)\s*(?:the\s+)?"
NON_RENDERER_HEADS = {
    "driver", "drivers", "api", "apis", "device", "devices", "debug-layer", "debug", "runtime", "runtimes", "adapter",
    "adapters", "sdk", "sdks", "header", "headers", "library", "libraries", "dll", "dlls", "feature", "features",
    "context", "contexts", "entry", "extension", "extensions", "function", "functions", "specification", "spec",
    "conformance", "swap", "swapchain", "swapchains", "queue", "queues", "shader", "shaders", "bytecode", "blobs",
    "upload", "element", "elements", "surface", "surfaces", "canvas", "texture", "textures", "format", "formats",
    "hardware", "gpu", "gpus", "translation", "layer", "layers", "route", "routes", "path", "paths", "probe", "probes",
    "flag", "flags", "version", "versions",
}
ROLE_HEADS = {"renderer", "renderers", "backend", "backends", "identity", "identities", "family", "families",
              "profile", "profiles", "implementation", "implementations"}
ROLE_CONTEXT = re.compile(r"\b(?:renderers?|backends?|identit(?:y|ies)|famil(?:y|ies)|registers?|registered|registrations?)\b", re.I)
CNA_CLAIM = re.compile(r"\bCNA(?:['\u2019]s)?\b[^.;]{0,60}\b(?:accepts?|supports?|offers?|exposes?|ships?|includes?|provides?)\b")
SDL_OWNED = re.compile(r"\bSDL(?:3|_gpu|_GPU)?\s*['\u2019]s\s+(?:own\s+)?(?:GPU\s+API\s*['\u2019]s\s+)?$")
CELL_ROLE_HEADER = re.compile(r"\b(?:famil(?:y|ies)|renderers?|identit(?:y|ies)|backends?)\b", re.I)
CELL_NON_RENDERER_HEADER = re.compile(r"\b(?:drivers?|API|devices?|librar(?:y|ies)|hosts?|platforms?|SDKs?)\b", re.I)


def visible_blocks(html_text: str, cell_headers: bool = False) -> list[str]:
    """The visible text of a page split into blocks (paragraph, list item, table cell, heading, ...), whitespace
    collapsed. Hover titles and the meta description are blocks of their own. With `cell_headers`, a data cell is
    prefixed with its column header in double brackets ("[[Alpha.1]] 50 public identities ..."), so a cell keeps
    the context its column gives it."""
    from bs4 import BeautifulSoup  # imported here so the line scan needs nothing beyond the standard library
    soup = BeautifulSoup(html_text, "html.parser")
    extra = [t.get("title", "") for t in soup.find_all(True) if t.get("title")]
    extra += [m.get("content", "") for m in soup.find_all("meta") if m.get("name") == "description" or m.get("property") == "og:description"]
    for t in soup.find_all(["script", "style"]):
        t.decompose()
    if cell_headers:
        for table in soup.find_all("table"):
            first = table.find("tr")
            headers = [c.get_text(" ", strip=True) for c in first.find_all(["th", "td"])] if first and first.find("th") else []
            for tr in table.find_all("tr")[1:] if headers else []:
                for col, cell in enumerate(tr.find_all(["td", "th"], recursive=False)):
                    if col < len(headers) and headers[col]:
                        cell.insert(0, f"[[{headers[col]}]] ")
    for t in soup.find_all(BLOCK_TAGS):
        t.append(f" {BLOCK} ")
    text = soup.get_text(" ")
    blocks = [re.sub(r"\s+", " ", b).strip() for b in text.split(BLOCK)] + [re.sub(r"\s+", " ", e).strip() for e in extra]
    return [b for b in blocks if b]


def retired_prose_rx(retired: set[str]) -> re.Pattern[str] | None:
    names = [PROSE[i] for i in sorted(retired) if i in PROSE]
    if not names:
        return None
    return re.compile(r"(?<![A-Za-z0-9_])(?:" + "|".join(names) + r")(?![A-Za-z0-9_])")


def _clause_before(block: str, start: int) -> str:
    before = block[max(0, start - 160):start]
    cut = max((m.end() for m in re.finditer(r"[.;!?](?:\s|$)", before)), default=0)
    return before[cut:]


def judge_list(block: str, retired_rx: re.Pattern[str], weak: bool = False) -> list[tuple[str, str, str]]:
    """Findings for one block: (reason, excerpt, the list itself) for every list in which a retired prose name is presented as a
    current CNA renderer. `weak` names (Canvas) are judged only by list membership and head noun."""
    item = r"(?:" + CURRENT_CNA_ONLY + r"|" + API_LIKE + r"|" + retired_rx.pattern + r")"
    run_rx = re.compile(r"(?<![\w-])" + item + r"(?:" + LIST_SEP + item + r")*(?![\w])")
    out: list[tuple[str, str, str]] = []
    for run in run_rx.finditer(block):
        text = run.group(0)
        if not retired_rx.search(text):
            continue
        excerpt = block[max(0, run.start() - 70): run.end() + 50]
        rest = re.sub(r"^\s*/\s*\d+(?:\.\d+)?", "", block[run.end():])   # "WebGL 1/2 flags": the version pair ends the name
        if re.match(r"\s*['\u2019]s\b", rest):
            continue                                        # "Direct3D 12's upload path" -- the API's property
        head_m = re.match(r"\s*\)?\s*([A-Za-z][\w-]*)", rest)
        head = head_m.group(1).lower() if head_m and not rest.lstrip().startswith(")") else ""
        if head in NON_RENDERER_HEADS:
            continue
        before = _clause_before(block, run.start())
        if SDL_OWNED.search(before):
            continue
        if head in ROLE_HEADS:
            out.append((f"retired renderer named with the role noun '{head}'", excerpt, text))
            continue
        current = [m.group(0) for m in re.finditer(r"(?<![\w-])(?:" + CURRENT_CNA_ONLY + r")(?![\w])", text)]
        if current:
            out.append((f"retired renderer listed beside current CNA renderer(s) {', '.join(current[:3])}", excerpt, text))
            continue
        if weak:
            continue
        if ROLE_CONTEXT.search(before):
            out.append(("retired renderer listed in a renderer/family/identity context", excerpt, text))
            continue
        if CNA_CLAIM.search(before):
            out.append(("retired renderer presented as something CNA accepts/supports/offers", excerpt, text))
    return out


def judge_cells(html_text: str, retired_rx: re.Pattern[str]) -> list[tuple[str, str, str]]:
    """A table cell holding nothing but a retired name, in a column about renderers (by header or by its neighbours)."""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_text, "html.parser")
    out: list[tuple[str, str, str]] = []
    whole = re.compile(r"^\s*(?:" + retired_rx.pattern + r")\s*$")
    current = re.compile(r"(?<![\w-])(?:" + CURRENT_CNA_ONLY + r")(?![\w])")
    for table in soup.find_all("table"):
        header_row = table.find("tr")
        headers = [c.get_text(" ", strip=True) for c in header_row.find_all(["th", "td"])] if header_row and header_row.find("th") else []
        rows = [[c.get_text(" ", strip=True) for c in tr.find_all(["th", "td"])] for tr in table.find_all("tr")]
        for row in rows:
            for col, cell in enumerate(row):
                if not whole.match(cell):
                    continue
                head = headers[col] if col < len(headers) else ""
                if head and CELL_NON_RENDERER_HEADER.search(head) and not CELL_ROLE_HEADER.search(head):
                    continue
                neighbours = [r[col] for r in rows if r is not row and col < len(r)]
                if CELL_ROLE_HEADER.search(head) or any(current.search(n) for n in neighbours):
                    out.append((f"table cell '{cell}' in a renderer column ({head or 'no header'})", " | ".join(row)[:160], " ".join(row)[:80]))
    return out


def semantic_findings(html_text: str, retired: set[str]) -> list[tuple[str, str, str]]:
    """(reason, excerpt, core) for every retired renderer the visible text presents as a current CNA renderer; core is
    the list or table row itself, which scripts/adversarial_audit.py locates inside a ledger anchor section."""
    strong_prose = retired_prose_rx({r for r in retired if r not in WORDS})
    weak_prose = retired_prose_rx({r for r in retired if r in WORDS})
    found: list[tuple[str, str, str]] = []
    blocks = visible_blocks(html_text)
    for rx, weak in ((strong_prose, False), (weak_prose, True)):
        if rx is None:
            continue
        for block in blocks:
            if rx.search(block):
                found += judge_list(block, rx, weak)
        found += judge_cells(html_text, rx)
    seen, unique = set(), []
    for f in found:
        if f[1] not in seen:
            seen.add(f[1])
            unique.append(f)
    return unique


def line_hits(text: str, retired: set[str]) -> list[tuple[int, str]]:
    """(line number, line) for every line that spells a retired identity (strong, weak or prose form)."""
    strong = sorted(i for i in retired if i not in WORDS)
    weak = sorted(i for i in retired if i in WORDS)
    strong_rx = strong_pattern(strong)
    # also the CamelCase enum spellings of the strong set, e.g. OpenGLES1 / DirectX7 / Blend2D / NanoVg
    weak_rx = re.compile(r"(?<![A-Za-z0-9_])(" + "|".join(map(re.escape, weak)) + r")(?![A-Za-z0-9_])") if weak else None
    prose_rx = prose_pattern(retired)
    weak_form = re.compile(r"CNA_RENDERER_(" + "|".join(map(re.escape, weak)) + r")\b|renderers/(" + "|".join(x.lower() for x in weak) + r")\b") if weak else None
    out = []
    for number, line in enumerate(text.splitlines(), 1):
        m = strong_rx.search(line)
        if m is None and weak_rx is not None:
            m = weak_rx.search(line) if re.search(r"[A-Z]{4,}", line) else None
            if m is None and weak_form:
                m = weak_form.search(line)
        if m is None and prose_rx is not None:
            m = prose_rx.search(line)
        if m:
            out.append((number, line.strip()[:140]))
    return out


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
    hits: list[tuple[str, int, str]] = []
    semantic: list[tuple[str, str, str]] = []
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
            semantic += [(rel.as_posix(), why, excerpt) for why, excerpt, _core in semantic_findings(text, retired)]
        hits += [(rel.as_posix(), number, line) for number, line in line_hits(text, retired)]
    for rel, number, line in hits:
        print(f"{rel}:{number}: {line}")
    for rel, why, excerpt in semantic:
        print(f"{rel}: {why}: \u2026{excerpt}\u2026")
    print(f"retired-renderer references in public content: {len(hits)} by spelling, {len(semantic)} by list semantics "
          f"({len(retired)} retired identities derived from the CNA registries, read from {src[2]})")
    return 1 if hits or semantic else 0


if __name__ == "__main__":
    sys.exit(main())
