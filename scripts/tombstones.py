#!/usr/bin/env python3
"""Tombstones: short transition pages kept at the URLs of retired pages, so inbound links do not end in a 404.

The site is served by GitHub Pages through Jekyll with no redirect plugin, and its pages carry no front matter, so it
has no server-side redirect (plan.md, "File names and URLs were preserved"). A page that had to go therefore leaves a
tombstone at its URL: one notice that points to where the subject lives now. A tombstone does not describe the
retired component and never presents it as a current feature. It is marked noindex, kept out of the sitemap and the
search index (scripts/build_site_indexes.py, scripts/validate_site.py), and no other page may link to it; the
retired-renderer and retired-platform scans skip it because this script checks it instead.

    tombstones.py build    # (re)write every tombstone in TOMBSTONES
    tombstones.py check    # each tombstone is exactly what build writes, and no page links to one
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

ROOT = Path(__file__).resolve().parent.parent
MARKER = '<meta name="cna-page-kind" content="tombstone">'

# retired page -> where its subject lives now. "message" is HTML: the current state only, no account of the removal.
TOMBSTONES: dict[str, dict] = {
    "deep-dives/renderers/canvas-renderer.html": {
        "title": "Browser rendering",
        "message": "The page that used to be at this address is no longer part of the documentation. In current CNA a "
                   "browser build renders through the <code>WEBGL2</code> or <code>WEBGPU</code> renderer.",
        "links": [("docs/rendering-backends.html", "Graphics renderers: every current renderer"),
                  ("deep-dives/platforms/web-build-and-main-loop.html", "Web builds and the browser main loop")],
    },
    "deep-dives/renderers/direct3d11-and-12-resources.html": {
        "title": "Direct3D on Windows",
        "message": "The page that used to be at this address is no longer part of the documentation. In current CNA a "
                   "Windows build renders through <code>DIRECTX9</code>, or through <code>SDL_GPU</code> on SDL&rsquo;s "
                   "Direct3D 12 GPU driver.",
        "links": [("deep-dives/renderers/direct3d-presentation-and-state.html", "Direct3D 9 presentation and state"),
                  ("docs/rendering-backends.html#windows-directx", "Graphics renderers: Windows")],
    },
    "deep-dives/renderers/sdl-renderer-2d-contract.html": {
        "title": "2D rendering",
        "message": "The page that used to be at this address is no longer part of the documentation. In current CNA every "
                   "renderer that produces pixels draws 2D through <code>SpriteBatch</code>.",
        "links": [("docs/spritebatch.html", "SpriteBatch"),
                  ("deep-dives/graphics/spritebatch-sorting-and-batching.html", "SpriteBatch sorting and batching")],
    },
    "deep-dives/renderers/vulkan-deferred-state-and-descriptors.html": {
        "title": "Native GPU rendering",
        "message": "The page that used to be at this address is no longer part of the documentation. In current CNA native "
                   "GPU rendering goes through the <code>SDL_GPU</code> renderer, on SDL&rsquo;s Vulkan, Direct3D 12 or "
                   "Metal GPU driver.",
        "links": [("deep-dives/renderers/sdl-gpu-pipeline-state-and-draw-order.html", "SDL_GPU shader intake, pipeline keys and draw order"),
                  ("docs/rendering-backends.html", "Graphics renderers: every current renderer")],
    },
    "deep-dives/renderers/vulkan-presentation-and-readback.html": {
        "title": "Presentation and back-buffer readback",
        "message": "The page that used to be at this address is no longer part of the documentation. Presentation and "
                   "back-buffer readback for the current renderers are described on the pages below.",
        "links": [("deep-dives/renderers/presentation-and-backbuffer-readback.html", "Presentation and back-buffer readback"),
                  ("deep-dives/renderers/sdl-gpu-resources-and-frame-recovery.html", "SDL_GPU resources and frame recovery")],
    },
    "development/internals/graphics/vulkan.html": {
        "title": "SDL_GPU renderer internals",
        "message": "The page that used to be at this address is no longer part of the documentation. In current CNA native "
                   "GPU rendering goes through the <code>SDL_GPU</code> renderer, on SDL&rsquo;s Vulkan, Direct3D 12 or "
                   "Metal GPU driver.",
        "links": [("development/internals/graphics/sdl-gpu.html", "SDL_GPU renderer internals"),
                  ("development/internals/graphics/backends.html", "Graphics backends: the renderer family map")],
    },
    "docs/tutorials/85-vulkan-backend.html": {
        "title": "Choosing a renderer",
        "message": "The tutorial that used to be at this address is no longer part of the series. In current CNA native GPU "
                   "rendering goes through the <code>SDL_GPU</code> renderer, on SDL&rsquo;s Vulkan, Direct3D 12 or Metal "
                   "GPU driver.",
        "links": [("docs/tutorials/72-backend-selection.html", "Tutorial 72: Choosing a Renderer"),
                  ("docs/rendering-backends.html", "Graphics renderers: every current renderer")],
    },
    "development/internals/platforms/x11.html": {
        "title": "X11 through SDL3",
        "message": "The page that used to be at this address is no longer part of the documentation. CNA reaches X11 "
                   "through its SDL3 platform implementation and SDL's <code>x11</code> video driver.",
        "links": [("development/internals/platforms/sdl3.html", "SDL3 platform internals"),
                  ("docs/native-platforms.html#x11", "Windows, X11 and Wayland: X11")],
    },
    "development/internals/platforms/wayland.html": {
        "title": "Wayland through SDL3",
        "message": "The page that used to be at this address is no longer part of the documentation. CNA reaches "
                   "Wayland through its SDL3 platform implementation and SDL's <code>wayland</code> video driver.",
        "links": [("development/internals/platforms/sdl3.html", "SDL3 platform internals"),
                  ("docs/native-platforms.html#wayland", "Windows, X11 and Wayland: Wayland")],
    },
    "development/internals/platforms/win32.html": {
        "title": "Windows through SDL3",
        "message": "The page that used to be at this address is no longer part of the documentation. CNA reaches "
                   "Windows through its SDL3 platform implementation and SDL's <code>windows</code> video driver.",
        "links": [("development/internals/platforms/sdl3.html", "SDL3 platform internals"),
                  ("docs/native-platforms.html#overview", "Windows, X11 and Wayland: one windowing implementation")],
    },
}


def is_tombstone(rel: str) -> bool:
    return rel in TOMBSTONES


def render(rel: str) -> str:
    import site_nav  # noqa: E402  (only build/check need the page chrome)
    t = TOMBSTONES[rel]
    prefix = "../" * rel.count("/")
    title = f"{t['title']} - CNA"
    plain = re.sub(r"<[^>]+>", "", t["message"])
    head = site_nav.head_block(rel, title, plain, prefix, "tombstone", t["title"], False)
    head = head.replace('  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n',
                        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
                        '  <meta name="robots" content="noindex">\n  ' + MARKER + '\n', 1)
    links = "\n".join(f'      <li><a href="{prefix}{href}">{site_nav.esc(label)}</a></li>' for href, label in t["links"])
    body = f'''<main id="main-content" class="docs-main">
  <article class="docs-content">
    <h1>{site_nav.esc(t["title"])}</h1>
    <p>{t["message"]}</p>
    <p>Continue with:</p>
    <ul>
{links}
    </ul>
  </article>
</main>
'''
    return head + site_nav.nav_block(prefix, "") + body + site_nav.footer_block(prefix, prefix + "docs/", False)


def cmd_build() -> int:
    for rel in TOMBSTONES:
        path = ROOT / rel
        text = render(rel)
        if not path.exists() or path.read_text(encoding="utf-8") != text:
            path.write_text(text, encoding="utf-8")
            print("wrote", rel)
    return 0


def cmd_check() -> int:
    bad = 0
    for rel, t in TOMBSTONES.items():
        path = ROOT / rel
        if not path.exists():
            print(f"ERROR {rel}: tombstone missing (scripts/tombstones.py build)"); bad += 1; continue
        if path.read_text(encoding="utf-8") != render(rel):
            print(f"ERROR {rel}: differs from what scripts/tombstones.py build writes"); bad += 1
        for href, _label in t["links"]:
            base = href.split("#", 1)[0]
            if not (ROOT / base).exists() or base in TOMBSTONES:
                print(f"ERROR {rel}: points to {href}, which is not a current page"); bad += 1
    # nothing may link to a tombstone: it is for inbound links from outside the site only
    names = "|".join(re.escape(Path(r).name) for r in TOMBSTONES)
    link_rx = re.compile(r'href="([^"#]*(?:' + names + r'))(?:#[^"]*)?"')
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT).as_posix()
        if rel in TOMBSTONES or {"audit", "scripts", "build-probe", ".git"} & set(path.relative_to(ROOT).parts):
            continue
        for m in link_rx.finditer(path.read_text(encoding="utf-8")):
            target = (path.parent / m.group(1)).resolve()
            if target.is_relative_to(ROOT) and target.relative_to(ROOT).as_posix() in TOMBSTONES:
                print(f"ERROR {rel}: links to the tombstone {m.group(1)}"); bad += 1
    for index in ("sitemap.xml", "search-index.json"):
        text = (ROOT / index).read_text(encoding="utf-8")
        for rel in TOMBSTONES:
            if rel in text:
                print(f"ERROR {index} lists the tombstone {rel}"); bad += 1
    print(f"tombstones: {len(TOMBSTONES)} checked; problems {bad}")
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["build", "check"])
    args = ap.parse_args()
    return cmd_build() if args.cmd == "build" else cmd_check()


if __name__ == "__main__":
    sys.exit(main())
