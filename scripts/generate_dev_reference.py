#!/usr/bin/env python3
"""Generate the factual inventories under development/reference/ from the CNA TARGET Git objects.

    generate_dev_reference.py            # write the five generated pages

Read-only against CNA: everything is read with `git ls-tree` / `git show <TARGET>:path` (TARGET = cnahead);
no checkout, branch, index or working tree of the CNA repository is touched.  Ported from the generator of the
developer.libcna.com working tree (scripts/generate_reference.py), with three changes: pages are rendered with the
libcna.com chrome through scripts/site_dev.py, module rows link to the Development pages, and a fifth inventory
(selection axes: platforms, audio implementations and renderer identities -> families) is derived from the CMake
registries so the counts on the site have one mechanical source.

The inventories are *syntactic* (declarations, file shapes).  They locate things; they do not establish behaviour,
build status or test results.
"""

from __future__ import annotations

import html
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dev_manifest as M  # noqa: E402
import site_dev  # noqa: E402

ROOT = site_dev.ROOT
CNA = site_dev.CNA_REPO
TARGET = site_dev.TARGET
FACTS = json.loads((ROOT / "data" / "current-facts.json").read_text(encoding="utf-8"))["facts"]


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(CNA), *args], check=True, capture_output=True, text=True).stdout


FILES = git("ls-tree", "-r", "--name-only", TARGET).splitlines()
FILESET = set(FILES)
_show_cache: dict[str, str] = {}


def show(path: str) -> str:
    if path not in _show_cache:
        _show_cache[path] = git("show", f"{TARGET}:{path}")
    return _show_cache[path]


def esc(s: str) -> str:
    return html.escape(s)


def src(path: str, label: str | None = None) -> str:
    assert path in FILESET, path
    return f'<a class="src-link" href="{esc(site_dev.src_url(path))}"><code>{esc(label or path)}</code></a>'


def tree(path: str, label: str | None = None) -> str:
    return f'<a class="src-link" href="{esc(site_dev.src_url(path, "tree"))}"><code>{esc(label or path + "/")}</code></a>'


META_STRIP = '<div class="meta-strip">{}</div>'


def strip(*items: tuple[str, str]) -> str:
    return META_STRIP.format("".join(f"<span><strong>{v}</strong> {esc(l)}</span>" for v, l in items))


def gen_note(script_hint: str = "python3 scripts/generate_dev_reference.py") -> str:
    return ('<div class="callout callout--info"><span class="callout-icon">&#8505;</span><p><strong>Generated page.</strong> '
            f'Produced by <code>{script_hint}</code> from the Git objects of CNA commit <code>{site_dev.TARGET_SHORT}</code>; '
            'do not edit it by hand. It is a syntactic inventory: it locates declarations and files, and does not establish '
            'behaviour, build success or test results.</p></div>')


# ---------------------------------------------------------------------------------------------
# 1. modules
# ---------------------------------------------------------------------------------------------
GUIDES = {
    "runtime": "development/internals/runtime/module.html",
    "graphics": "development/internals/graphics/device.html",
    "content": "development/internals/content/runtime.html",
    "content-pipeline": "development/internals/content/pipeline.html",
    "input": "development/internals/input/events.html",
    "audio": "development/internals/audio/engine.html",
    "c-api": "development/internals/bindings/c-api-internals.html",
    "platform": "development/internals/platforms/index.html",
    "renderers": "development/internals/graphics/backends.html",
    "core": "development/internals/modules/core.html",
    "math": "development/internals/modules/math.html",
    "design": "development/internals/modules/design.html",
    "devices": "development/internals/modules/devices.html",
    "devices-ext": "development/internals/modules/devices-ext.html",
    "diagnostics": "development/internals/modules/diagnostics.html",
    "inspector": "development/internals/modules/inspector.html",
    "phone": "development/internals/modules/phone.html",
    "storage": "development/internals/modules/storage.html",
    "media": "development/internals/modules/media.html",
    "video-ffmpeg": "development/internals/modules/video-ffmpeg.html",
    "gamer-services": "development/internals/modules/gamer-services.html",
    "graphics-ext": "development/internals/modules/graphics-ext.html",
    "net": "development/internals/modules/net.html",
}
FAMILY_GUIDES = {
    "easygl": "development/internals/graphics/easygl.html",
    "vulkan": "development/internals/graphics/vulkan.html",
    "sdl-gpu": "development/internals/graphics/sdl-gpu.html",
    "software": "development/internals/graphics/software.html",
    "headless": "development/internals/graphics/headless.html",
    "stub": "development/internals/graphics/stub.html",
    "opengl4": "development/internals/graphics/opengl4.html",
}
PAGE = "development/reference/{}.html"


def guide_link(page: str, target: str | None) -> str:
    if not target:
        return "no dedicated internals page"
    return f'<a href="{esc(site_dev.rel_href(page, target))}">Internals page</a>'


def shape(prefix: str) -> tuple[list[str], list[str], list[str], list[str]]:
    owned = [p for p in FILES if p.startswith(prefix)]
    headers = [p for p in owned if "/include/" in p and p.endswith((".hpp", ".h"))]
    sources = [p for p in owned if "/src/" in p and p.endswith((".cpp", ".c", ".mm", ".m"))]
    tests = [p for p in owned if "/tests/" in p]
    return owned, headers, sources, tests


def gen_modules() -> tuple[dict, str]:
    page = PAGE.format("modules")
    modules = sorted({p.split("/")[1] for p in FILES if p.startswith("modules/") and len(p.split("/")) > 2 and
                      p.split("/")[1] != "CMakeLists.txt"})
    rows = []
    for m in modules:
        prefix = f"modules/{m}/"
        owned, headers, sources, tests = shape(prefix)
        entries = []
        cm = prefix + "CMakeLists.txt"
        if cm in FILESET:
            entries.append(src(cm, "CMakeLists.txt"))
        for cand in headers[:2]:
            entries.append(src(cand, Path(cand).name))
        rows.append(f"<tr><td><code>{esc(m)}</code></td><td>{len(headers)}</td><td>{len(sources)}</td><td>{len(tests)}</td>"
                    f"<td>{' &middot; '.join(entries)}</td><td>{guide_link(page, GUIDES.get(m))}</td></tr>")
    fam_dirs = sorted({p.split("/")[2] for p in FILES if p.startswith("modules/renderers/") and len(p.split("/")) > 3})
    fam_rows = []
    for f in fam_dirs:
        prefix = f"modules/renderers/{f}/"
        owned, headers, sources, tests = shape(prefix)
        owns_src = any(p.startswith(prefix + "src/") for p in FILES)
        entries = []
        cm = prefix + "CMakeLists.txt"
        if cm in FILESET:
            entries.append(src(cm, "CMakeLists.txt"))
        role = "implementation family" if owns_src else "shared helper (no <code>src/</code> of its own)"
        fam_rows.append(f"<tr><td><code>{esc(f)}</code></td><td>{role}</td><td>{len(headers)}</td><td>{len(sources)}</td>"
                        f"<td>{len(tests)}</td><td>{' &middot; '.join(entries)}</td><td>{guide_link(page, FAMILY_GUIDES.get(f))}</td></tr>")
    n_fam = sum(1 for f in fam_dirs if any(p.startswith(f"modules/renderers/{f}/src/") for p in FILES))
    total_files = sum(1 for p in FILES if p.startswith("modules/"))
    body = (gen_note() + strip((str(len(modules)), "physical production modules"), (f"{total_files:,}", "files under modules/"),
                                (str(n_fam), "renderer implementation families")) +
            '<h2 id="inventory">Modules</h2><p>Every directory under <code>modules/</code> at the snapshot. Counts describe tree shape, not '
            'architectural importance: a module with few headers can own a great deal of behaviour, and header counts include '
            '<code>Internal/</code> headers.</p>'
            '<table><thead><tr><th scope="col">Module</th><th scope="col">Headers</th><th scope="col">Sources</th><th scope="col">Test files</th>'
            '<th scope="col">Entry points</th><th scope="col">Maintainer page</th></tr></thead><tbody>' + "".join(rows) + "</tbody></table>"
            '<h2 id="renderer-families">Renderer directories under <code>modules/renderers/</code></h2>'
            '<p>A directory that owns a <code>src/</code> is an <em>implementation family</em>; one family can serve several public identities '
            '(EasyGL serves five). <code>common/</code> holds shared helpers. The identity-to-family map is in the '
            f'<a href="{esc(site_dev.rel_href(page, PAGE.format("selection-axes")))}">selection axes index</a>.</p>'
            '<table><thead><tr><th scope="col">Directory</th><th scope="col">Role</th><th scope="col">Headers</th><th scope="col">Sources</th>'
            '<th scope="col">Test files</th><th scope="col">Entry point</th><th scope="col">Maintainer page</th></tr></thead><tbody>'
            + "".join(fam_rows) + "</tbody></table>"
            '<p>A module without a dedicated internals page has not been given a deep maintainer tour on this site; that says nothing about '
            'the module itself.</p>')
    meta = {"title": "Module index",
            "description": f"Generated inventory of the {len(modules)} production modules and the renderer families at CNA snapshot {site_dev.TARGET_SHORT}: header, source and test counts with source-pinned entry points.",
            "keywords": ["modules", "inventory", "source ownership", "generated", "renderers", "families", "headers", "tests"],
            "evidence": {"levels": ["source-verified"], "note": "Counts are computed from the Git tree of the pinned commit."},
            "layers": {"maintainer": [["development/repository/source-ownership.html", "Source ownership"],
                                      ["development/repository/index.html", "Repository map"]],
                       "architecture": [["development/repository/module-graph.html", "Physical module graph"]],
                       "reference": [["development/reference/public-headers.html", "Public header index"],
                                     ["development/reference/selection-axes.html", "Selection axes index"]]}}
    return meta, body


# ---------------------------------------------------------------------------------------------
# 2. CMake options
# ---------------------------------------------------------------------------------------------
OPTION_RE = re.compile(r"(?ims)\b(option|cmake_dependent_option)\s*\(\s*([A-Za-z0-9_]+)\s+(?:\"([^\"]*)\"|([^\s\)]+))\s+([^\s\)]+)")
CACHE_RE = re.compile(r"(?ims)\bset\s*\(\s*([A-Za-z0-9_]+)\s+([^\s\)]+).*?\bCACHE\s+(BOOL|STRING|PATH|FILEPATH)\s+(?:\"([^\"]*)\"|([^\)]*))\)")


def gen_options() -> tuple[dict, str]:
    cmake_files = [p for p in FILES if p.endswith(("CMakeLists.txt", ".cmake"))]
    options: dict[str, tuple[str, str, str, str]] = {}
    for path in cmake_files:
        text = show(path)
        for m in OPTION_RE.finditer(text):
            options.setdefault(m.group(2), ("option" if m.group(1).lower() == "option" else "dependent option",
                                            m.group(5), (m.group(3) or m.group(4) or "").strip(), path))
        for m in CACHE_RE.finditer(text):
            options.setdefault(m.group(1), (f"cache {m.group(3).lower()}", (m.group(2) or "").strip(),
                                            (m.group(4) or m.group(5) or "").strip(), path))
    cna = {k: v for k, v in options.items() if k.startswith(("CNA_", "SHARP_"))}
    rows = "".join(f"<tr><td><code>{esc(n)}</code></td><td>{esc(kind)}</td><td><code>{esc(d)}</code></td><td>{esc(desc)}</td><td>{src(p, p)}</td></tr>"
                   for n, (kind, d, desc, p) in sorted(options.items()))
    body = (gen_note() + strip((str(len(options)), "cache options / variables found"), (str(len(cna)), "with a CNA_ or SHARP_ prefix"),
                               (str(len(cmake_files)), "CMake files scanned")) +
            '<h2 id="options">Options</h2><p>Every <code>option()</code>, <code>cmake_dependent_option()</code> and <code>set(… CACHE …)</code> declaration found by '
            'a syntactic scan of the CMake files. Read the linked CMake logic before relying on a value: conditional defaults can depend on host or toolchain and can be '
            'rewritten after declaration, and a declaration says nothing about which combinations are valid (see '
            f'<a href="{esc(site_dev.rel_href(PAGE.format("cmake-options"), PAGE.format("selection-axes")))}">selection axes</a> and the '
            f'<a href="{esc(site_dev.rel_href(PAGE.format("cmake-options"), "development/build/architecture.html"))}">CMake architecture</a> page).</p>'
            '<table><thead><tr><th scope="col">Name</th><th scope="col">Kind</th><th scope="col">Default / value</th><th scope="col">Description</th>'
            '<th scope="col">Declared in</th></tr></thead><tbody>' + rows + "</tbody></table>")
    meta = {"title": "CMake option index",
            "description": f"Generated index of the {len(options)} CMake options and cache variables declared at CNA snapshot {site_dev.TARGET_SHORT}, with defaults, descriptions and source-pinned declarations.",
            "keywords": ["cmake", "options", "cache", "cna_platform", "cna_graphics_renderer", "cna_audio_platform", "build", "generated"],
            "evidence": {"levels": ["source-verified"], "note": "A syntactic scan; conditional defaults are not evaluated."},
            "layers": {"guide": [["docs/building.html", "Building CNA"]],
                       "internals": [["development/build/architecture.html", "CMake architecture"]],
                       "maintainer": [["development/handbook/change-build-configuration.html", "Change build configuration"]],
                       "reference": [["development/reference/selection-axes.html", "Selection axes index"]]}}
    return meta, body


# ---------------------------------------------------------------------------------------------
# 3. test targets
# ---------------------------------------------------------------------------------------------
TARGET_RE = re.compile(r"(?im)\b(add_executable|add_test)\s*\(\s*(?:NAME\s+)?([A-Za-z0-9_.:+${}-]+)")


def gen_tests() -> tuple[dict, str]:
    cmake_files = [p for p in FILES if p.endswith(("CMakeLists.txt", ".cmake"))]
    targets: dict[tuple[str, str], str] = {}
    for path in cmake_files:
        for kind, name in TARGET_RE.findall(show(path)):
            if kind == "add_test" or "test" in name.lower() or "/tests/" in path or path.startswith("tests/"):
                targets.setdefault((kind, name), path)
    rows = "".join(f"<tr><td><code>{esc(name)}</code></td><td>{esc(kind)}</td><td>{src(path, path)}</td></tr>"
                   for (kind, name), path in sorted(targets.items(), key=lambda x: (x[0][1].lower(), x[0][0])))
    n_files = sum(1 for p in FILES if re.search(r"(^|/)(test|tests)/", p) and p.endswith(".cpp") and not p.startswith("third_party/"))
    body = (gen_note() + strip((str(len(targets)), "test-related declarations"), (f"{n_files:,}", "C++ test source files (tests/ or test/ directories)")) +
            '<h2 id="targets">Targets and registrations</h2><p>Declarations found by a syntactic scan of <code>add_executable</code> and <code>add_test</code>. '
            'Generator expressions and helper functions create further tests at configure time, and one configured build contains only a subset of these: '
            'confirm a configuration with <code>ctest --test-dir &lt;build&gt; -N</code>. A declaration in this table is a registration, not a test result.</p>'
            '<table><thead><tr><th scope="col">Name</th><th scope="col">Declaration</th><th scope="col">Source</th></tr></thead><tbody>' + rows + "</tbody></table>")
    meta = {"title": "Test target index",
            "description": f"Generated index of the {len(targets)} test-related executable and CTest declarations at CNA snapshot {site_dev.TARGET_SHORT}, each with its source-pinned CMake declaration.",
            "keywords": ["tests", "ctest", "gtest", "targets", "test registration", "generated", "unit tests", "examples"],
            "evidence": {"levels": ["source-verified"], "note": "Declarations only: none of the listed targets was built or run to produce this page."},
            "layers": {"guide": [["docs/verification.html", "Verification &amp; known issues"]],
                       "internals": [["development/testing/architecture.html", "Test architecture and change recipes"]],
                       "maintainer": [["development/takeover/validation.html", "What to test after changing X"],
                                      ["development/handbook/add-a-regression-test.html", "Add a regression test"]]}}
    return meta, body


# ---------------------------------------------------------------------------------------------
# 4. public headers
# ---------------------------------------------------------------------------------------------
def gen_headers() -> tuple[dict, str]:
    headers = [p for p in FILES if p.startswith("modules/") and ("/include/CNA/" in p or "/include/Microsoft/" in p)
               and "/Internal/" not in p and p.endswith((".hpp", ".h"))]
    groups: dict[str, list[str]] = {}
    for p in headers:
        groups.setdefault(p.split("/")[1], []).append(p)
    sections = []
    for module, paths in sorted(groups.items()):
        sections.append(f'<h2 id="module-{esc(module)}">{esc(module)} <small>({len(paths)})</small></h2><ul class="source-list">'
                        + "".join(f"<li>{src(p)}</li>" for p in paths) + "</ul>")
    body = (gen_note() + strip((f"{len(headers):,}", "non-Internal CNA/Microsoft headers"), (str(len(groups)), "modules")) +
            '<div class="callout callout--warn"><span class="callout-icon">&#9888;</span><p><strong>“Public” is a tree-shape term here.</strong> The lists below are headers under '
            '<code>include/CNA</code> or <code>include/Microsoft</code>, outside <code>Internal</code>. That includes the XNA-shaped surface. Export macros and target install rules '
            'remain authoritative for what a shipped binary actually exposes, and the experimental C ABI (<code>modules/c-api/include/CNA/C</code>, ABI '
            f'{esc(str(FACTS["c_abi_version"]["value"]))}) is separately versioned.</p></div>' + "".join(sections))
    meta = {"title": "Public header index",
            "description": f"Generated index of the {len(headers):,} non-Internal CNA and Microsoft headers across {len(groups)} modules at CNA snapshot {site_dev.TARGET_SHORT}, with source-pinned links.",
            "keywords": ["headers", "public api", "include", "xna", "microsoft.xna.framework", "inventory", "generated", "c api"],
            "evidence": {"levels": ["source-verified"], "note": "A tree-shape inventory; it does not distinguish supported API from headers that merely sit under include/."},
            "layers": {"guide": [["docs/xna-compatibility.html", "XNA compatibility"], ["docs/c-api.html", "Experimental C API"]],
                       "maintainer": [["development/handbook/change-public-xna-behavior.html", "Change public XNA behavior"],
                                      ["development/handbook/update-the-c-api.html", "Update the C API"]],
                       "reference": [["development/reference/modules.html", "Module index"]]}}
    return meta, body


# ---------------------------------------------------------------------------------------------
# 5. selection axes
# ---------------------------------------------------------------------------------------------
def gen_axes() -> tuple[dict, str]:
    page = PAGE.format("selection-axes")
    ident_cmake = show("cmake/RendererIdentities.cmake")
    public = re.findall(r"[A-Z][A-Z0-9_]+", re.search(r"set\(CNA_RENDERER_PUBLIC_IDENTITIES\s(.*?)\)", ident_cmake, re.S).group(1))
    check = show("scripts/check_renderer_identities.py")
    table = re.findall(r'\("([A-Z0-9_]+)",\s*"([A-Za-z0-9]+)",\s*(\d+)\)', re.search(r"IDENTITIES = \[(.*?)\n\]", check, re.S).group(1))
    abi = {n: (enum, int(v)) for n, enum, v in table}
    reg_text = show("cmake/RendererRegistry.cmake")
    body_map = re.search(r"set\(_map\n(.*?)\)\n", reg_text, re.S).group(1)
    toks = re.sub(r"#[^\n]*", "", body_map).split()
    fmap = dict(zip(toks[0::2], toks[1::2]))
    if set(public) != set(abi) or set(public) != set(fmap):
        raise SystemExit(f"identity sets disagree: cmake={len(public)} table={len(abi)} registry={len(fmap)}")
    fam_dir_by_ns = {}
    for d in {p.split("/")[2] for p in FILES if p.startswith("modules/renderers/") and len(p.split("/")) > 3}:
        fam_dir_by_ns[re.sub(r"[^a-z0-9]", "", d.lower())] = d
    fam_of = {}
    for ident in public:
        ns = fmap[ident].split("|")[0]
        d = fam_dir_by_ns.get(re.sub(r"[^a-z0-9]", "", ns.lower()))
        if d is None:
            raise SystemExit(f"cannot map family namespace {ns} to a modules/renderers directory")
        fam_of[ident] = (ns, d, fmap[ident].split("|")[1] if "|" in fmap[ident] else "GetDescriptor")
    families = sorted({d for _, d, _ in fam_of.values()})
    if len(public) != FACTS["renderer_identities"]["value"] or len(families) != FACTS["implementation_families"]["value"]:
        raise SystemExit(f"counts drifted from data/current-facts.json: {len(public)} identities, {len(families)} families")
    id_rows = []
    for ident in sorted(public, key=lambda i: abi[i][1]):
        ns, d, acc = fam_of[ident]
        family_cell = tree(f"modules/renderers/{d}", d + "/")
        guide = FAMILY_GUIDES.get(d)
        gl = f' &middot; <a href="{esc(site_dev.rel_href(page, guide))}">internals</a>' if guide else ""
        id_rows.append(f"<tr><td><code>{ident}</code></td><td>{abi[ident][1]}</td><td><code>{esc(abi[ident][0])}</code></td>"
                       f"<td>{family_cell}{gl}</td><td><code>{esc(acc)}</code></td></tr>")
    plat = show("cmake/PlatformSelection.cmake")
    plat_str = re.search(r'set\(CNA_PLATFORM "SDL3" CACHE STRING\s+"Platform implementation \(([^)]*)\)"', plat).group(1)
    platforms = [x.strip() for x in plat_str.split("|")]
    if "SDL12" not in plat or "EMSCRIPTEN" not in plat:
        raise SystemExit("PlatformSelection.cmake no longer mentions the reserved SDL12/EMSCRIPTEN identifiers")
    audio = show("cmake/AudioPlatformSelection.cmake")
    audio_avail = re.search(r"set\(_cna_audio_platforms_available\s+([A-Z0-9_ ]+)\)", audio).group(1).split()
    audio_res = re.search(r"set\(_cna_audio_platforms_reserved\s+([A-Z0-9_ ]+)\)", audio).group(1).split()
    if len(platforms) != FACTS["platform_implementations"]["value"] or len(audio_avail) != FACTS["audio_implementations"]["value"]:
        raise SystemExit(f"platform/audio counts drifted: {len(platforms)} / {len(audio_avail)}")
    plat_notes = {
        "SDL3": "default; SDL3 windowing, events and input", "SDL2": "SDL2 windowing, events and input (partial services)",
        "X11": "native Xlib backend, no SDL; offered only where the X development environment exists",
        "WAYLAND": "native Wayland client, no SDL and no X11 library; offered only where the Wayland development environment exists",
        "WIN32": "native user32/gdi32 backend; offered when the target is Windows",
        "HEADLESS": "no window; injected events; conformance and CI role", "TERMINAL": "POSIX terminal session (termios); CPU-frame presentation",
    }
    audio_notes = {
        "SDL3": "default; SDL3 device transport with the SDL3_mixer-backed XNA playback engine (defines <code>SOUND_ENABLED</code>)",
        "SDL2": "SDL2 device transport; no XNA mixer", "NULL": "deterministic paced callback transport; no XNA mixer",
        "ALSA": "native Linux backend: libasound loaded at run time, CNA's own mixer (defines <code>SOUND_ENABLED</code>)",
    }
    prow = "".join(f"<tr><td><code>{p}</code></td><td>{plat_notes.get(p, '')}</td></tr>" for p in platforms)
    arow = "".join(f"<tr><td><code>{p}</code></td><td>{audio_notes.get(p, '')}</td></tr>" for p in audio_avail)
    body = (gen_note() + strip((str(len(public)), "public renderer identities"), (str(len(families)), "implementation families"),
                               (str(len(platforms)), "platform implementations"), (str(len(audio_avail)), "audio implementations")) +
            '<p class="lede">CNA composes a build from independent axes: which <em>platform</em> owns the window and events, which <em>audio platform</em> owns the device, '
            'and which <em>renderer identity</em> produces pixels. This page lists each axis from the registries that define it, so the counts used across the site have one mechanical source.</p>'
            '<h2 id="renderers">Renderer identities and their families</h2>'
            f'<p>Identities come from {src("cmake/RendererIdentities.cmake")} (<code>CNA_RENDERER_PUBLIC_IDENTITIES</code>); the C ABI value and C++ enumerator from the canonical table in '
            f'{src("scripts/check_renderer_identities.py")}; the identity-to-family map from {src("cmake/RendererRegistry.cmake")}. The three sources agree (checked at generation time: '
            'the generator refuses to write this page if they disagree with each other or with the site\'s canonical counts). A name outside this set is a configure-time error.</p>'
            '<table><thead><tr><th scope="col">Identity (<code>CNA_GRAPHICS_RENDERER</code>)</th><th scope="col">C ABI value</th><th scope="col">C++ enumerator</th>'
            '<th scope="col">Implementation family</th><th scope="col">Descriptor accessor</th></tr></thead><tbody>' + "".join(id_rows) + "</tbody></table>"
            '<h2 id="platforms">Platform implementations (<code>CNA_PLATFORM</code>)</h2>'
            f'<p>From {src("cmake/PlatformSelection.cmake")}. <code>SDL12</code> and <code>EMSCRIPTEN</code> are reserved identifiers that are refused rather than aliased. '
            'Some implementations are host-conditional (Terminal is POSIX-only, Win32 Windows-only, X11 and Wayland need their development packages) and are refused with an explanation rather than replaced by SDL3.</p>'
            '<table><thead><tr><th scope="col">Value</th><th scope="col">Role</th></tr></thead><tbody>' + prow + "</tbody></table>"
            '<h2 id="audio">Audio implementations (<code>CNA_AUDIO_PLATFORM</code>)</h2>'
            f'<p>From {src("cmake/AudioPlatformSelection.cmake")}. Reserved and refused: {", ".join(f"<code>{r}</code>" for r in audio_res)}. '
            'Audio selection is independent of the platform: a headless application may use SDL3 audio, and a graphical one may choose deterministic <code>NULL</code> audio.</p>'
            '<table><thead><tr><th scope="col">Value</th><th scope="col">Role</th></tr></thead><tbody>' + arow + "</tbody></table>"
            '<h2 id="rules">How the axes combine</h2><p>The axes are validated separately and then together (see '
            f'{src("cmake/RendererCombinations.cmake")} and {src("cmake/RendererSelection.cmake")}); not every combination is valid, and a GPU renderer needs a native window handle that the Headless and Terminal '
            'platforms do not provide. Multiple renderer identities can be compiled into one binary through <code>CNA_GRAPHICS_RENDERERS</code>; an API choice beats the <code>CNA_GRAPHICS_RENDERER</code> environment variable, '
            'which beats the compiled default. See the '
            f'<a href="{esc(site_dev.rel_href(page, "development/internals/graphics/selection.html"))}">renderer selection internals</a> and '
            f'<a href="{esc(site_dev.rel_href(page, "development/internals/platforms/index.html"))}">platform backends</a>.</p>')
    meta = {"title": "Selection axes index",
            "description": f"Generated index of CNA's three build axes at snapshot {site_dev.TARGET_SHORT}: {len(public)} renderer identities mapped to {len(families)} implementation families, {len(platforms)} platform implementations and {len(audio_avail)} audio implementations.",
            "keywords": ["renderer identities", "families", "cna_platform", "cna_audio_platform", "cna_graphics_renderer", "abi values", "selection", "generated"],
            "evidence": {"levels": ["source-verified"], "note": "Derived from the CMake registries; whether a given combination builds or runs on a host is not established here."},
            "layers": {"guide": [["docs/rendering-backends.html", "Renderers"], ["docs/platforms.html", "Platforms"], ["docs/audio.html", "Audio system"]],
                       "internals": [["development/internals/graphics/selection.html", "Renderer selection internals"],
                                     ["development/internals/platforms/index.html", "Platform backends"]],
                       "maintainer": [["development/repository/source-ownership.html", "Source ownership"]],
                       "reference": [["development/reference/modules.html", "Module index"], ["development/reference/cmake-options.html", "CMake option index"]]}}
    return meta, body


def main() -> int:
    errors: list[str] = []
    outputs = {"modules": gen_modules, "cmake-options": gen_options, "test-targets": gen_tests,
               "public-headers": gen_headers, "selection-axes": gen_axes}
    for slug, fn in outputs.items():
        page = PAGE.format(slug)
        meta, body = fn()
        text = site_dev.render_page(page, meta, body, errors)
        if errors:
            continue
        out = ROOT / page
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(f"{page}: {len(text) // 1024} KiB")
    if errors:
        print("FAILED:")
        for e in errors:
            print(" -", e)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
