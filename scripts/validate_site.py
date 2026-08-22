#!/usr/bin/env python3
"""Validate libcna.com's static HTML, links, metadata, JSON-LD and indexes."""

from __future__ import annotations

import json
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parent.parent
SITE = "https://libcna.com"
INDEX_EXCLUDED = {
    "404.html", "search.html",
}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.links: list[str] = []
        self.title = False
        self.title_text: list[str] = []
        self.description = ""
        self.canonical = ""
        self.og: dict[str, str] = {}
        self.json_ld: list[str] = []
        self.in_json_ld = False
        self.json_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): value or "" for key, value in attrs}
        if values.get("id"):
            self.ids.append(values["id"])
        if tag.lower() in {"a", "link", "script", "img", "source"}:
            key = "href" if tag.lower() in {"a", "link"} else "src"
            if values.get(key):
                self.links.append(values[key])
        if tag.lower() == "title":
            self.title = True
        elif tag.lower() == "meta":
            if values.get("name", "").lower() == "description":
                self.description = values.get("content", "").strip()
            prop = values.get("property", "").lower()
            if prop.startswith("og:"):
                self.og[prop] = values.get("content", "").strip()
        elif tag.lower() == "link" and "canonical" in values.get("rel", "").lower().split():
            self.canonical = values.get("href", "").strip()
        elif tag.lower() == "script" and values.get("type", "").lower() == "application/ld+json":
            self.in_json_ld = True
            self.json_parts = []

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self.title = False
        elif tag.lower() == "script" and self.in_json_ld:
            self.json_ld.append("".join(self.json_parts))
            self.in_json_ld = False

    def handle_data(self, data: str) -> None:
        if self.title:
            self.title_text.append(data)
        if self.in_json_ld:
            self.json_parts.append(data)


def resolve_local(source: Path, href: str) -> tuple[Path, str] | None:
    parsed = urlparse(href)
    if parsed.scheme or parsed.netloc or href.startswith(("mailto:", "tel:", "javascript:")):
        return None
    raw_path = unquote(parsed.path)
    if not raw_path:
        target = source
    elif raw_path.startswith("/"):
        target = ROOT / raw_path.lstrip("/")
    else:
        target = source.parent / raw_path
    if raw_path.endswith("/"):
        target /= "index.html"
    try:
        target = target.resolve()
        target.relative_to(ROOT.resolve())
    except (ValueError, OSError):
        return target, parsed.fragment
    return target, unquote(parsed.fragment)


def expected_canonical(rel: str) -> str:
    return SITE + ("/" if rel == "index.html" else "/" + rel)


def main() -> int:
    errors: list[str] = []
    pages: dict[Path, PageParser] = {}
    html_files = sorted(ROOT.rglob("*.html"))

    for path in html_files:
        rel = path.relative_to(ROOT).as_posix()
        parser = PageParser()
        try:
            parser.feed(path.read_text(encoding="utf-8"))
            parser.close()
        except Exception as exc:
            errors.append(f"HTML parse {rel}: {exc}")
            continue
        pages[path.resolve()] = parser
        duplicates = [value for value, count in Counter(parser.ids).items() if count > 1]
        if duplicates:
            errors.append(f"Duplicate IDs {rel}: {', '.join(duplicates)}")
        for number, payload in enumerate(parser.json_ld, 1):
            try:
                value = json.loads(payload)
                if not isinstance(value, (dict, list)):
                    raise ValueError("top level must be an object or array")
            except Exception as exc:
                errors.append(f"JSON-LD {rel} block {number}: {exc}")

        if not "".join(parser.title_text).strip():
            errors.append(f"Missing title: {rel}")
        if not parser.description:
            errors.append(f"Missing meta description: {rel}")
        if not parser.canonical:
            errors.append(f"Missing canonical: {rel}")
        elif parser.canonical != expected_canonical(rel):
            errors.append(f"Wrong canonical {rel}: {parser.canonical}")
        for prop in ("og:title", "og:description"):
            if not parser.og.get(prop):
                errors.append(f"Missing {prop}: {rel}")

    try:
        import html5lib
        strict_count = 0
        for path in html_files:
            html5_parser = html5lib.HTMLParser(strict=False, namespaceHTMLElements=False)
            html5_parser.parse(path.read_text(encoding="utf-8"))
            strict_count += 1
            for position, code, details in html5_parser.errors:
                errors.append(f"HTML5 parse {rel}:{position[0]}:{position[1]}: {code} {details}")
    except ImportError:
        strict_count = 0

    for source, parser in pages.items():
        rel = source.relative_to(ROOT.resolve()).as_posix()
        for href in parser.links:
            resolved = resolve_local(source, href)
            if resolved is None:
                continue
            target, fragment = resolved
            if not target.exists():
                errors.append(f"Broken local link {rel}: {href}")
                continue
            if fragment and target.suffix.lower() == ".html":
                target_parser = pages.get(target.resolve())
                if target_parser is None or fragment not in target_parser.ids:
                    errors.append(f"Broken fragment {rel}: {href}")

    expected_rels = sorted(
        path.relative_to(ROOT).as_posix() for path in html_files
        if path.relative_to(ROOT).as_posix() not in INDEX_EXCLUDED
    )
    expected_search = {"/index.html" if rel == "index.html" else "/" + rel for rel in expected_rels}
    expected_sitemap = {expected_canonical(rel) for rel in expected_rels}

    try:
        search = json.loads((ROOT / "search-index.json").read_text(encoding="utf-8"))
        urls = [item["url"] for item in search]
        duplicates = [url for url, count in Counter(urls).items() if count > 1]
        if duplicates:
            errors.append("Duplicate search URLs: " + ", ".join(duplicates))
        if set(urls) != expected_search:
            errors.append(
                f"Search coverage mismatch: missing={sorted(expected_search-set(urls))}, "
                f"extra={sorted(set(urls)-expected_search)}"
            )
        for item in search:
            if not all(item.get(key) for key in ("url", "title", "description", "tags")):
                errors.append(f"Incomplete search entry: {item.get('url', '<missing>')}")
    except Exception as exc:
        errors.append(f"search-index.json: {exc}")
        search = []

    try:
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        sitemap_root = ET.parse(ROOT / "sitemap.xml").getroot()
        locs = [node.text or "" for node in sitemap_root.findall("s:url/s:loc", ns)]
        duplicates = [loc for loc, count in Counter(locs).items() if count > 1]
        if duplicates:
            errors.append("Duplicate sitemap URLs: " + ", ".join(duplicates))
        if set(locs) != expected_sitemap:
            errors.append(
                f"Sitemap coverage mismatch: missing={sorted(expected_sitemap-set(locs))}, "
                f"extra={sorted(set(locs)-expected_sitemap)}"
            )
    except Exception as exc:
        errors.append(f"sitemap.xml: {exc}")
        locs = []

    if errors:
        print(f"FAILED: {len(errors)} issue(s)")
        for error in errors:
            print(f"- {error}")
        return 1

    json_ld_count = sum(len(parser.json_ld) for parser in pages.values())
    link_count = sum(len(parser.links) for parser in pages.values())
    fragment_count = sum(
        1 for parser in pages.values() for href in parser.links
        if not urlparse(href).scheme and bool(urlparse(href).fragment)
    )
    print(f"HTML parsed: {len(html_files)}")
    if strict_count:
        print(f"Strict HTML5 parse: {strict_count} authored pages")
    print(f"Local/external references inspected: {link_count}")
    print(f"Local fragments inspected: {fragment_count}")
    print("Duplicate IDs: 0")
    print(f"JSON-LD blocks parsed: {json_ld_count}")
    print(f"Search entries: {len(search)} (unique and complete)")
    print(f"Sitemap URLs: {len(locs)} (unique and complete)")
    print("Metadata/canonical coverage: complete for site pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
