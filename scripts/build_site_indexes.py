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
UPDATED = "2026-09-25"  # Phase 3: Deep Dives and Known Issues added; every page gained the header entries
EXCLUDED = {
    "404.html",
    "search.html",
}

# Phase 1 audited every public page against CNA snapshot 009d40f5 (facts, footer, metadata), so every
# page carries the snapshot date. A page that is regenerated later without a content audit should be
# removed from this rule deliberately, not implicitly.
MATERIALLY_UPDATED: set[str] = set()  # filled from the file system in main(); see all_public_pages()

NEW_TAGS = {
    "/docs/rendering-backends.html": ["rendering", "renderers", "sdl_renderer", "opengl", "easygl", "vulkan", "webgpu", "d3d11", "d3d12", "direct3d", "headless", "software"],
    "/features.html": ["features", "renderers", "cross-platform", "opengl", "sdl3", "webgpu", "direct3d"],
    "/docs/content-pipeline.html": ["content", "pipeline", "cna-content", "xnb", "cnb", "importer", "processor"],
    "/docs/cnb-format.html": ["cnb", "format", "content", "binary", "zstd"],
    "/docs/diagnostics.html": ["diagnostics", "statistics", "profiling", "trace", "metrics"],
    "/docs/inspector.html": ["inspector", "debugging", "browser", "agent", "diagnostics"],
    "/docs/tools.html": ["tools", "cli", "cna-content", "gltf", "cnb"],
    "/docs/native-platforms.html": ["platform", "x11", "wayland", "win32", "sdl-free"],
    "/docs/cnaext-engine.html": ["cnaext", "engine", "pbr", "shadows", "ibl", "extensions"],
    "/docs/design-converters.html": ["design", "converters", "typeconverter", "framework.design"],
    "/network.html": ["network", "sites", "links", "bible", "demos", "metagl", "meshcraft", "easygl"],
    "/docs/releases.html": ["release", "version", "semver", "alpha", "prerelease", "abi"],
    "/docs/runtime-renderer-selection.html": ["renderer", "runtime", "selection", "fallback", "multi-renderer"],
    "/docs/c-api.html": ["c", "api", "abi", "native", "experimental", "c17"],
    "/docs/tutorials/126-multi-renderer-build.html": ["tutorial", "renderer", "runtime", "cmake", "fallback"],
    "/docs/tutorials/127-platform-audio-selection.html": ["tutorial", "platform", "audio", "sdl2", "headless"],
    "/docs/tutorials/128-compiled-xna-effects.html": ["tutorial", "effects", "fxb", "xnb", "fna3d"],
    "/docs/tutorials/129-c-api-first-program.html": ["tutorial", "c", "api", "abi", "cmake"],
}


DEV_HUBS = {"development/index.html", "development/handbook/index.html", "development/takeover/index.html",
            "development/internals/index.html", "development/repository/index.html",
            "deep-dives/index.html", "known-issues/index.html"}


class MetadataParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: list[str] = []
        self.in_title = False
        self.description = ""
        self.canonical = ""
        self.keywords: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): value or "" for key, value in attrs}
        if tag.lower() == "title":
            self.in_title = True
        elif tag.lower() == "meta" and values.get("name", "").lower() == "description":
            self.description = values.get("content", "").strip()
        elif tag.lower() == "meta" and values.get("name", "").lower() == "keywords":
            self.keywords = [k.strip().lower() for k in values.get("content", "").split(",") if k.strip()]
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


NON_SITE_DIRS = {"audit", "scripts", "build-probe", ".git"}  # repository content, not published pages (see _config.yml)


def public_pages() -> list[Path]:
    return [
        path for path in sorted(ROOT.rglob("*.html"))
        if path.relative_to(ROOT).as_posix() not in EXCLUDED and not (NON_SITE_DIRS & set(path.relative_to(ROOT).parts))
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


def all_public_pages() -> set[str]:
    return {path.relative_to(ROOT).as_posix() for path in public_pages()}


def update_material_dates() -> None:
    """Stamp JSON-LD dateModified on every audited public page."""
    MATERIALLY_UPDATED.update(all_public_pages())
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
        if not tags and parser.keywords:
            # Development pages carry their own search terms in <meta name="keywords">
            area_tag = ("development" if rel.startswith("development/") else "deep dive" if rel.startswith("deep-dives/")
                        else "known issue" if rel.startswith("known-issues/") else None)
            tags = list(dict.fromkeys(parser.keywords + ([area_tag] if area_tag else [])))[:16]
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
        if rel in DEV_HUBS or (rel.startswith(("deep-dives/", "known-issues/")) and rel.endswith("/index.html")):
            priority = "0.8"
        if rel in {"docs/releases.html", "docs/runtime-renderer-selection.html", "docs/c-api.html",
                   "docs/content-pipeline.html", "docs/cnb-format.html", "docs/diagnostics.html",
                   "docs/inspector.html", "docs/native-platforms.html", "docs/cnaext-engine.html"}:
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
