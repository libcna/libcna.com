#!/usr/bin/env python3
"""Extract a presentation inventory (sections, CTAs, cards, images, videos, stats, tables).

The inventory is a preservation contract: it is generated from the known-good
libcna.com revision before Phase-1 edits and compared with the updated site at the end
(see compare_presentation.py).  It intentionally records *presentation* (what a visitor
sees and can click), not byte-exact markup.

Usage:
    inventory_presentation.py --rev <git-rev> --out audit/data/baseline.json
    inventory_presentation.py --out /tmp/current.json          # working tree
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup, Tag

ROOT = Path(__file__).resolve().parent.parent

CARD_CLASSES = {"card", "demo-item", "video-card", "callout"}
BLOCK_CLASSES = {"demo-platform", "hero", "page-header"}
CTA_ROLE_CLASSES = ("btn-primary", "btn-secondary", "btn-outline")
CHROME_CLASSES = {"nav", "nav-container", "nav-menu", "footer-inner", "skip-link"}


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def classes(tag: Tag) -> list[str]:
    value = tag.get("class") or []
    return value if isinstance(value, list) else str(value).split()


def in_chrome(tag: Tag) -> bool:
    """True when the element is inside the site-wide nav or footer."""
    for parent in tag.parents:
        if not isinstance(parent, Tag):
            continue
        if parent.name in {"nav", "footer"}:
            return True
    return False


def link_kind(href: str) -> str:
    if not href:
        return "empty"
    if href.startswith("#"):
        return "fragment"
    parsed = urlparse(href)
    if parsed.scheme in {"mailto", "tel", "javascript"}:
        return parsed.scheme
    if not parsed.scheme and not parsed.netloc:
        return "internal"
    path = parsed.path.strip("/")
    if parsed.netloc.endswith("github.com"):
        depth = len([p for p in path.split("/") if p])
        return "github-org" if depth <= 1 else ("github-repo" if depth == 2 else "github-deep")
    if not path and not parsed.query and not parsed.fragment:
        return "external-root"
    return "external-deep"


def cta_role(tag: Tag) -> str | None:
    cls = classes(tag)
    if "btn" not in cls and not any(c.startswith("btn-") for c in cls):
        return None
    for name in CTA_ROLE_CLASSES:
        if name in cls:
            return name.split("-", 1)[1]
    return "plain"


def container_label(tag: Tag) -> str:
    """Describe the card/section that contains an element."""
    for parent in tag.parents:
        if not isinstance(parent, Tag):
            continue
        pc = set(classes(parent))
        if pc & (CARD_CLASSES | BLOCK_CLASSES) or parent.name in {"section", "figure", "article"}:
            heading = parent.find(["h1", "h2", "h3", "h4"])
            name = norm(heading.get_text(" ")) if heading else ""
            kind = next(iter(pc & (CARD_CLASSES | BLOCK_CLASSES)), parent.name)
            return f"{kind}: {name}" if name else kind
    return ""


def section_key(tag: Tag) -> str:
    """Nearest heading-bearing block for a section-level label."""
    return container_label(tag)


def first_title(tag: Tag) -> str:
    heading = tag.find(["h1", "h2", "h3", "h4", "h5"])
    if heading:
        return norm(heading.get_text(" "))
    strong = tag.find(["strong", "b"])
    if strong:
        return norm(strong.get_text(" "))
    return ""


def extract_stats(soup: BeautifulSoup) -> list[dict]:
    """Quick-stat style blocks: a large value with a small label beneath it."""
    stats: list[dict] = []
    seen: set[int] = set()
    # inline-styled big numbers (homepage quick stats) or any element whose class mentions stat
    for tag in soup.find_all(True):
        style = (tag.get("style") or "").replace(" ", "").lower()
        cls = " ".join(classes(tag)).lower()
        is_value = bool(re.search(r"font-size:(2|2\.\d+|3|4)rem", style)) and bool(
            re.search(r"font-weight:(700|800|bold)", style)
        )
        if not is_value and "stat" not in cls.replace("status", ""):
            continue
        if "stat" in cls.replace("status", "") and not is_value:
            # stat container: record its text once
            if id(tag) in seen:
                continue
            seen.add(id(tag))
            stats.append({"value": "", "label": norm(tag.get_text(" ")), "title": tag.get("title", ""),
                          "kind": "stat-class", "section": section_key(tag)})
            continue
        value = norm(tag.get_text(" "))
        label_el = tag.find_next_sibling()
        label = norm(label_el.get_text(" ")) if label_el else ""
        title = ""
        for parent in [tag.parent, tag.parent.parent if tag.parent else None]:
            if parent is not None and parent.get("title"):
                title = parent.get("title")
                break
        stats.append({"value": value, "label": label, "title": title, "kind": "big-number",
                      "section": section_key(tag)})
    return stats


def extract_page(html: str, rel: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    title = norm(soup.title.get_text()) if soup.title else ""
    desc_tag = soup.find("meta", attrs={"name": "description"})
    page: dict = {
        "path": rel,
        "title": title,
        "description": desc_tag.get("content", "").strip() if desc_tag else "",
    }

    main = soup.find("main") or soup.body or soup
    page["headings"] = [
        {"level": int(h.name[1]), "text": norm(h.get_text(" ")), "id": h.get("id", "")}
        for h in main.find_all(["h1", "h2", "h3", "h4"])
    ]

    # ids on structural elements = anchors/sections a visitor may deep-link to
    page["section_ids"] = sorted(
        {t.get("id") for t in main.find_all(True) if t.get("id")}
    )

    # major blocks with size (for the >50% reduction check)
    blocks = []
    for tag in main.find_all(["section", "div"]):
        cls = set(classes(tag))
        is_block = tag.name == "section" or bool(cls & BLOCK_CLASSES)
        if not is_block:
            continue
        heading = tag.find(["h1", "h2", "h3"])
        text = norm(tag.get_text(" "))
        blocks.append({
            "kind": ("section" if tag.name == "section" else sorted(cls & BLOCK_CLASSES)[0]),
            "id": tag.get("id", ""),
            "heading": norm(heading.get_text(" ")) if heading else "",
            "words": len(text.split()),
            "links": len(tag.find_all("a", href=True)),
            "images": len(tag.find_all("img")),
            "cards": len([c for c in tag.find_all(True) if set(classes(c)) & {"card", "demo-item", "video-card"}]),
            "ctas": len([a for a in tag.find_all("a", href=True) if cta_role(a)]),
        })
    page["blocks"] = blocks

    ctas = []
    for a in main.find_all("a", href=True):
        role = cta_role(a)
        if not role:
            continue
        ctas.append({
            "label": norm(a.get_text(" ")),
            "href": a["href"],
            "kind": link_kind(a["href"]),
            "role": role,
            "classes": classes(a),
            "target": a.get("target", ""),
            "rel": a.get("rel", "") if isinstance(a.get("rel", ""), str) else " ".join(a.get("rel", [])),
            "in": container_label(a),
        })
    page["ctas"] = ctas

    links = []
    for a in main.find_all("a", href=True):
        if cta_role(a):
            continue
        label = norm(a.get_text(" "))
        links.append({"label": label, "href": a["href"], "kind": link_kind(a["href"]), "in": container_label(a)})
    page["links"] = links

    cards = []
    for tag in main.find_all(True):
        cls = set(classes(tag))
        hit = cls & CARD_CLASSES
        if not hit:
            continue
        kind = sorted(hit)[0]
        text = norm(tag.get_text(" "))
        cards.append({
            "kind": kind,
            "title": first_title(tag),
            "words": len(text.split()),
            "excerpt": text[:220],
            "ctas": [{"label": norm(a.get_text(" ")), "href": a["href"], "role": cta_role(a)}
                     for a in tag.find_all("a", href=True) if cta_role(a)],
            "images": [i.get("src", "") for i in tag.find_all("img")],
            "in": "",
        })
    page["cards"] = cards

    images = []
    for img in main.find_all("img"):
        parent_a = img.find_parent("a")
        fig = img.find_parent("figure")
        caption = ""
        if fig and fig.find("figcaption"):
            caption = norm(fig.find("figcaption").get_text(" "))
        elif fig:
            p = fig.find("p")
            caption = norm(p.get_text(" ")) if p else ""
        images.append({
            "src": img.get("src", ""),
            "alt": img.get("alt", ""),
            "caption": caption,
            "clickable": bool(parent_a),
            "target": parent_a["href"] if parent_a else "",
            "in": container_label(img),
        })
    page["images"] = images

    videos = []
    for card in main.find_all(True, class_="video-card"):
        vid = ""
        for el in card.find_all(True):
            for attr in ("data-video-id", "data-id", "data-src", "src", "href"):
                val = el.get(attr, "")
                m = re.search(r"(?:embed/|v=|youtu\.be/|/vi/)([A-Za-z0-9_-]{11})", val) or (
                    re.fullmatch(r"[A-Za-z0-9_-]{11}", val) if attr.startswith("data-video") or attr == "data-id" else None
                )
                if m:
                    vid = m.group(1) if m.groups() else val
                    break
            if vid:
                break
        thumb = card.find("img")
        videos.append({
            "id": vid,
            "title": first_title(card),
            "thumbnail": thumb.get("src", "") if thumb else "",
            "words": len(norm(card.get_text(" ")).split()),
            "ctas": [{"label": norm(a.get_text(" ")), "href": a["href"]} for a in card.find_all("a", href=True)],
            "html_hint": str(card)[:400].replace("\n", " "),
        })
    for frame in main.find_all(["iframe", "video", "embed"]):
        videos.append({"id": "", "title": frame.get("title", ""), "src": frame.get("src", ""),
                       "kind": frame.name, "words": 0, "ctas": [], "thumbnail": ""})
    page["videos"] = videos

    page["stats"] = extract_stats(main)

    tables = []
    for table in main.find_all("table"):
        heads = [norm(th.get_text(" ")) for th in table.find_all("th")]
        rows = table.find_all("tr")
        prev = table.find_previous(["h2", "h3", "h4"])
        tables.append({
            "purpose": norm(prev.get_text(" ")) if prev else "",
            "headers": heads[:14],
            "rows": max(len(rows) - 1, 0),
        })
    page["tables"] = tables

    callouts = []
    for c in main.find_all(True, class_="callout"):
        callouts.append({"kind": [x for x in classes(c) if x.startswith("callout--")],
                         "title": first_title(c), "words": len(norm(c.get_text(" ")).split()),
                         "excerpt": norm(c.get_text(" "))[:200]})
    page["callouts"] = callouts

    code = main.find_all("pre")
    page["code_blocks"] = len(code)
    page["words"] = len(norm(main.get_text(" ")).split())
    return page


def git_files(rev: str) -> list[str]:
    out = subprocess.run(["git", "-C", str(ROOT), "ls-tree", "-r", "--name-only", rev],
                         check=True, capture_output=True, text=True).stdout
    return [p for p in out.splitlines() if p.endswith(".html")]


def git_show(rev: str, path: str) -> str:
    return subprocess.run(["git", "-C", str(ROOT), "show", f"{rev}:{path}"],
                          check=True, capture_output=True).stdout.decode("utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", help="git revision to read (default: working tree)")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    pages = {}
    if args.rev:
        rels = sorted(git_files(args.rev))
        loader = lambda rel: git_show(args.rev, rel)  # noqa: E731
    else:
        rels = sorted(p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*.html"))
        loader = lambda rel: (ROOT / rel).read_text(encoding="utf-8")  # noqa: E731
    for rel in rels:
        pages[rel] = extract_page(loader(rel), rel)

    meta = {"rev": args.rev or "working-tree"}
    if args.rev:
        meta["sha"] = subprocess.run(["git", "-C", str(ROOT), "rev-parse", args.rev], check=True,
                                     capture_output=True, text=True).stdout.strip()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"meta": meta, "pages": pages}, indent=1, ensure_ascii=False) + "\n",
                   encoding="utf-8")
    print(f"{len(pages)} pages -> {out} ({out.stat().st_size // 1024} KiB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
