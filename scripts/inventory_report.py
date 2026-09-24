#!/usr/bin/env python3
"""Render a presentation inventory JSON (from inventory_presentation.py) as Markdown."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

PROTECTED = [
    "index.html", "demos.html", "showcase.html", "videos.html", "features.html", "about.html",
    "documentation.html", "tutorials.html", "architecture.html", "roadmap.html", "network.html",
    "contact.html",
]


def cell(text: str, limit: int = 110) -> str:
    text = " ".join((text or "").split()).replace("|", "\\|")
    return text if len(text) <= limit else text[: limit - 1] + "…"


def render(data: dict, title: str) -> str:
    pages = data["pages"]
    meta = data["meta"]
    out: list[str] = [f"# {title}", ""]
    out += [
        f"Source revision: `{meta.get('sha', meta['rev'])}`", "",
        "Generated mechanically by `scripts/inventory_presentation.py` + "
        "`scripts/inventory_report.py`. Machine-readable data: "
        "`audit/data/phase1-baseline-inventory.json`. This document is the Phase-1 preservation "
        "contract: every significant item below must still be present, updated, or explicitly "
        "dispositioned in `audit/phase1-presentation-comparison.md`.", "",
    ]

    total = {k: sum(len(p[k]) for p in pages.values()) for k in
             ("headings", "ctas", "links", "cards", "images", "videos", "stats", "tables", "blocks")}
    primary = sum(1 for p in pages.values() for c in p["ctas"] if c["role"] == "primary")
    out += ["## Totals (all HTML pages)", "", f"- HTML pages: **{len(pages)}**"]
    for key, value in total.items():
        out.append(f"- {key}: **{value}**")
    out += [f"- primary CTAs (`btn-primary`): **{primary}**", ""]

    out += ["## Presentation-protected pages", ""]
    out += ["| Page | Headings | Blocks | CTAs (primary) | Links | Cards | Images | Videos | Stats | Tables | Words |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for rel in PROTECTED:
        p = pages[rel]
        prim = sum(1 for c in p["ctas"] if c["role"] == "primary")
        out.append(f"| `{rel}` | {len(p['headings'])} | {len(p['blocks'])} | {len(p['ctas'])} ({prim}) | "
                   f"{len(p['links'])} | {len(p['cards'])} | {len(p['images'])} | {len(p['videos'])} | "
                   f"{len(p['stats'])} | {len(p['tables'])} | {p['words']} |")
    out.append("")

    for rel in PROTECTED:
        p = pages[rel]
        out += [f"## `{rel}`", "", f"**Title:** {p['title']}", ""]
        out += ["### Headings / sections", ""]
        for h in p["headings"]:
            out.append(f"- {'  ' * (h['level'] - 1)}h{h['level']} {cell(h['text'], 140)}"
                       + (f" `#{h['id']}`" if h["id"] else ""))
        out.append("")
        if p["blocks"]:
            out += ["### Major blocks", "", "| Kind | id | Heading | Words | Cards | CTAs | Images |", "|---|---|---|---:|---:|---:|---:|"]
            for b in p["blocks"]:
                out.append(f"| {b['kind']} | {b['id'] or ''} | {cell(b['heading'], 70)} | {b['words']} | "
                           f"{b['cards']} | {b['ctas']} | {b['images']} |")
            out.append("")
        if p["stats"]:
            out += ["### Statistics", "", "| Value | Label | Hover title |", "|---|---|---|"]
            for s in p["stats"]:
                out.append(f"| {cell(s['value'], 30)} | {cell(s['label'], 60)} | {cell(s['title'], 90)} |")
            out.append("")
        if p["ctas"]:
            out += ["### CTAs / buttons", "", "| Label | href | Role | target | Kind | Context |", "|---|---|---|---|---|---|"]
            for c in p["ctas"]:
                out.append(f"| {cell(c['label'], 50)} | `{cell(c['href'], 90)}` | {c['role']} | {c['target']} | "
                           f"{c['kind']} | {cell(c['in'], 60)} |")
            out.append("")
        if p["cards"]:
            out += ["### Cards / callouts", "", "| Kind | Title | Words | CTAs |", "|---|---|---:|---|"]
            for c in p["cards"]:
                out.append(f"| {c['kind']} | {cell(c['title'], 70)} | {c['words']} | "
                           f"{cell('; '.join(x['label'] for x in c['ctas']), 60)} |")
            out.append("")
        if p["images"]:
            out += ["### Images", "", "| src | alt | clickable | caption |", "|---|---|---|---|"]
            for i in p["images"]:
                out.append(f"| `{i['src']}` | {cell(i['alt'], 60)} | {i['clickable']} {i['target']} | {cell(i['caption'], 60)} |")
            out.append("")
        if p["videos"]:
            out += ["### Videos / media", "", "| id | title | thumbnail | CTA hrefs |", "|---|---|---|---|"]
            for v in p["videos"]:
                out.append(f"| {v['id'] or v.get('src', '')} | {cell(v['title'], 70)} | {v.get('thumbnail', '')} | "
                           f"{cell(', '.join(c['href'] for c in v['ctas']), 90)} |")
            out.append("")
        if p["tables"]:
            out += ["### Tables", "", "| Purpose | Headers | Data rows |", "|---|---|---:|"]
            for t in p["tables"]:
                out.append(f"| {cell(t['purpose'], 60)} | {cell(' / '.join(t['headers']), 100)} | {t['rows']} |")
            out.append("")
        sig = [l for l in p["links"] if l["kind"] in {"external-deep", "external-root", "github-repo",
                                                       "github-deep", "github-org"}]
        if sig:
            out += ["### Significant external links", "", "| Label | href | Kind |", "|---|---|---|"]
            seen = set()
            for l in sig:
                key = (l["label"], l["href"])
                if key in seen:
                    continue
                seen.add(key)
                out.append(f"| {cell(l['label'], 60)} | `{cell(l['href'], 100)}` | {l['kind']} |")
            out.append("")

    out += ["## All other pages (summary)", "",
            "| Page | H | CTAs (primary) | Cards | Images | Tables | Code blocks | Words |",
            "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for rel, p in pages.items():
        if rel in PROTECTED:
            continue
        prim = sum(1 for c in p["ctas"] if c["role"] == "primary")
        out.append(f"| `{rel}` | {len(p['headings'])} | {len(p['ctas'])} ({prim}) | {len(p['cards'])} | "
                   f"{len(p['images'])} | {len(p['tables'])} | {p['code_blocks']} | {p['words']} |")
    out.append("")
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("inventory")
    ap.add_argument("--out", required=True)
    ap.add_argument("--title", default="Phase-1 presentation baseline")
    args = ap.parse_args()
    data = json.loads(Path(args.inventory).read_text(encoding="utf-8"))
    Path(args.out).write_text(render(data, args.title), encoding="utf-8")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
