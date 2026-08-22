#!/usr/bin/env python3
"""Rebuild search-index.json and sitemap.xml from public HTML metadata."""

from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parent.parent
SITE = "https://libcna.com"
UPDATED = "2026-08-20"
EXCLUDED = {
    "404.html",
    "search.html",
}

# A global release footer changed every page. Only pages whose substantive content was
# audited or rewritten get a new sitemap date.
MATERIALLY_UPDATED = {
    "about.html", "architecture.html", "contribute.html", "documentation.html",
    "features.html", "index.html", "roadmap.html", "showcase.html", "tutorials.html",
    "docs/3d-rendering.html", "docs/audio.html", "docs/building.html", "docs/c-api.html",
    "docs/content-manager.html", "docs/content-pipeline-xnb.html", "docs/effects.html",
    "docs/faq.html", "docs/getting-started.html", "docs/graphics-state.html", "docs/migration-from-monogame.html",
    "docs/math-types.html", "docs/model-loading.html", "docs/packed-vector.html", "docs/platforms.html",
    "docs/releases.html", "docs/render-targets.html", "docs/rendering-backends.html",
    "docs/roadmap.html", "docs/runtime-renderer-selection.html", "docs/shader-effects.html",
    "docs/storage.html", "docs/verification.html", "docs/xna-compatibility.html",
    "docs/tutorials/01-introduction.html", "docs/tutorials/02-setup.html",
    "docs/tutorials/03-first-window.html", "docs/tutorials/20-build-run.html",
    "docs/tutorials/14-sound-effects.html", "docs/tutorials/15-background-music.html",
    "docs/tutorials/21-spritebatch.html", "docs/tutorials/31-first-3d-triangle.html",
    "docs/tutorials/32-basiceffect.html", "docs/tutorials/33-matrices.html",
    "docs/tutorials/34-camera-3d.html", "docs/tutorials/35-model-loading.html",
    "docs/tutorials/36-model-texturing.html", "docs/tutorials/37-multiple-lights.html",
    "docs/tutorials/38-vertex-buffers.html", "docs/tutorials/39-depth-buffer.html",
    "docs/tutorials/40-primitive-types.html", "docs/tutorials/51-custom-vertex.html",
    "docs/tutorials/52-custom-shaders.html", "docs/tutorials/53-effect-parameter.html",
    "docs/tutorials/54-alpha-test.html", "docs/tutorials/55-dual-texture.html",
    "docs/tutorials/56-environment-map.html", "docs/tutorials/57-skinned-effect.html",
    "docs/tutorials/58-normal-mapping.html",
    "docs/tutorials/59-shadow-mapping.html", "docs/tutorials/60-instancing.html",
    "docs/tutorials/61-occlusion-query.html", "docs/tutorials/62-mrt.html",
    "docs/tutorials/65-msaa.html",
    "docs/tutorials/63-stencil-buffer.html", "docs/tutorials/64-cubemaps.html",
    "docs/tutorials/66-bloom.html", "docs/tutorials/67-deferred-rendering.html",
    "docs/tutorials/68-terrain.html", "docs/tutorials/69-water.html",
    "docs/tutorials/70-procedural-geometry.html",
    "docs/tutorials/72-backend-selection.html", "docs/tutorials/80-cross-platform.html",
    "docs/tutorials/73-profiling.html", "docs/tutorials/74-frustum-culling.html",
    "docs/tutorials/75-lod.html", "docs/tutorials/81-emscripten.html",
    "docs/tutorials/82-android.html", "docs/tutorials/83-migrate-monogame.html",
    "docs/tutorials/84-migrate-xna.html", "docs/tutorials/85-vulkan-backend.html",
    "docs/tutorials/86-bgfx-backend.html", "docs/tutorials/87-custom-backend.html",
    "docs/tutorials/93-fps-game.html", "docs/tutorials/95-speedy-blupi.html",
    "docs/tutorials/99-unit-testing.html",
    "docs/tutorials/100-shipping.html",
    "docs/tutorials/101-renderer-capabilities.html",
    "docs/tutorials/102-opengl-family.html", "docs/tutorials/103-direct3d-windows.html",
    "docs/tutorials/104-directx-ladder.html", "docs/tutorials/105-browser-renderers.html",
    "docs/tutorials/106-vector-renderers.html", "docs/tutorials/107-cpu-renderers.html",
    "docs/tutorials/108-fna3d.html", "docs/tutorials/109-metal-macos.html",
    "docs/tutorials/110-gltf-models.html", "docs/tutorials/111-cnj-pipeline.html",
    "docs/tutorials/112-gltf-animation.html", "docs/tutorials/114-pbr-materials.html",
    "docs/tutorials/118-dynamic-audio.html", "docs/tutorials/119-3d-audio.html",
    "docs/tutorials/120-xact.html", "docs/tutorials/122-media-library.html",
    "docs/tutorials/117-devices-layer.html",
    "docs/tutorials/125-pixel-testing.html", "docs/tutorials/126-multi-renderer-build.html",
    "docs/tutorials/127-platform-audio-selection.html",
    "docs/tutorials/128-compiled-xna-effects.html",
    "docs/tutorials/129-c-api-first-program.html",
}

NEW_TAGS = {
    "/docs/releases.html": ["release", "version", "semver", "alpha", "prerelease", "abi"],
    "/docs/runtime-renderer-selection.html": ["renderer", "runtime", "selection", "fallback", "multi-renderer"],
    "/docs/c-api.html": ["c", "api", "abi", "native", "experimental", "c17"],
    "/docs/tutorials/126-multi-renderer-build.html": ["tutorial", "renderer", "runtime", "cmake", "fallback"],
    "/docs/tutorials/127-platform-audio-selection.html": ["tutorial", "platform", "audio", "sdl2", "headless"],
    "/docs/tutorials/128-compiled-xna-effects.html": ["tutorial", "effects", "fxb", "xnb", "fna3d"],
    "/docs/tutorials/129-c-api-first-program.html": ["tutorial", "c", "api", "abi", "cmake"],
}


class MetadataParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: list[str] = []
        self.in_title = False
        self.description = ""
        self.canonical = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): value or "" for key, value in attrs}
        if tag.lower() == "title":
            self.in_title = True
        elif tag.lower() == "meta" and values.get("name", "").lower() == "description":
            self.description = values.get("content", "").strip()
        elif tag.lower() == "link" and "canonical" in values.get("rel", "").lower().split():
            self.canonical = values.get("href", "").strip()

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)

    @property
    def title(self) -> str:
        return re.sub(r"\s+", " ", "".join(self.title_parts)).strip()


def public_pages() -> list[Path]:
    return [
        path for path in sorted(ROOT.rglob("*.html"))
        if path.relative_to(ROOT).as_posix() not in EXCLUDED
    ]


def load_old_search() -> dict[str, dict]:
    path = ROOT / "search-index.json"
    if not path.exists():
        return {}
    return {item["url"]: item for item in json.loads(path.read_text(encoding="utf-8"))}


def load_old_sitemap() -> dict[str, tuple[str, str]]:
    path = ROOT / "sitemap.xml"
    if not path.exists():
        return {}
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    result: dict[str, tuple[str, str]] = {}
    for node in ET.parse(path).getroot().findall("s:url", ns):
        loc = node.findtext("s:loc", "", ns)
        result[loc] = (
            node.findtext("s:lastmod", "2026-08-11", ns),
            node.findtext("s:priority", "0.6", ns),
        )
    return result


def fallback_tags(url: str, title: str) -> list[str]:
    words = re.findall(r"[a-z0-9]+", f"{url} {title}".lower())
    ignored = {"html", "docs", "tutorials", "cna", "documentation", "the", "and", "for"}
    return list(dict.fromkeys(word for word in words if word not in ignored))[:8]


def update_material_dates() -> None:
    """Stamp JSON-LD only on pages whose release content materially changed."""
    pattern = re.compile(r'("dateModified"\s*:\s*")\d{4}-\d{2}-\d{2}("\s*)')
    for rel in sorted(MATERIALLY_UPDATED):
        path = ROOT / rel
        if not path.exists():
            raise SystemExit(f"Materially updated page does not exist: {rel}")
        source = path.read_text(encoding="utf-8")
        updated = pattern.sub(rf'\g<1>{UPDATED}\g<2>', source)
        if updated != source:
            path.write_text(updated, encoding="utf-8")


def main() -> None:
    update_material_dates()
    old_search = load_old_search()
    old_sitemap = load_old_sitemap()
    search: list[dict] = []
    sitemap_rows: list[tuple[str, str, str]] = []

    for path in public_pages():
        rel = path.relative_to(ROOT).as_posix()
        parser = MetadataParser()
        parser.feed(path.read_text(encoding="utf-8"))
        if not (parser.title and parser.description and parser.canonical):
            raise SystemExit(f"Missing title, description or canonical metadata: {rel}")

        parsed = urlparse(parser.canonical)
        url = parsed.path or "/"
        search_url = "/index.html" if rel == "index.html" else "/" + rel
        tags = NEW_TAGS.get(search_url, old_search.get(search_url, {}).get("tags"))
        if not tags:
            tags = fallback_tags(search_url, parser.title)
        search.append({
            "url": search_url,
            "title": parser.title,
            "description": parser.description,
            "tags": tags,
        })

        old_date, old_priority = old_sitemap.get(parser.canonical, (UPDATED, "0.6"))
        date = UPDATED if rel in MATERIALLY_UPDATED else old_date
        priority = "1.0" if rel == "index.html" else old_priority
        if rel in {"docs/releases.html", "docs/runtime-renderer-selection.html", "docs/c-api.html"}:
            priority = "0.8"
        sitemap_rows.append((parser.canonical, date, priority))

    search.sort(key=lambda item: item["url"])
    (ROOT / "search-index.json").write_text(
        json.dumps(search, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, lastmod, priority in sorted(sitemap_rows):
        lines.extend([
            "  <url>", f"    <loc>{loc}</loc>", f"    <lastmod>{lastmod}</lastmod>",
            f"    <priority>{priority}</priority>", "  </url>",
        ])
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"search-index.json: {len(search)} public pages")
    print(f"sitemap.xml: {len(sitemap_rows)} public URLs")


if __name__ == "__main__":
    main()
