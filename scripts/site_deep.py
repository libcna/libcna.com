#!/usr/bin/env python3
"""Build and maintain the Deep Dives (deep-dives/**) and Known Issues (known-issues/**) areas of libcna.com.

    site_deep.py build  --src DIR [PATH ...]   # write authored pages from DIR/<path minus .html>.body.html + .meta.json
    site_deep.py hubs                          # (re)generate the area hubs and every group hub from the built pages
    site_deep.py sync                          # rewrite sidebar / breadcrumb / pager on every page of both areas
    site_deep.py check                         # manifest vs disk (no writes)

Page fragments use the same three tokens as the Development area ({{src:...}}, {{tree:...}}, {{page:...}}), expanded and validated
by scripts/site_dev.py against the TARGET Git objects.  Fragment meta is the Development meta plus two extra `layers` rows:
    deep    other deep-dive pages, e.g. [["deep-dives/graphics/spritebatch-sorting.html", "SpriteBatch sorting"]]
    issues  known-issues pages, e.g. [["known-issues/bugs/cna-bug-019.html", "CNA-BUG-019"]]
The page set comes from audit/data/deep-pages/*.json (see scripts/deep_manifest.py).
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import deep_manifest as DM  # noqa: E402
import dev_manifest as _DEVM  # noqa: E402
import site_dev as SD  # noqa: E402
import site_nav  # noqa: E402

ROOT = SD.ROOT
TARGET_SHORT = SD.TARGET_SHORT
TODAY = SD.TODAY
SITE = SD.SITE
esc = SD.esc
rel_href = SD.rel_href

# {{page:...}} tokens and layer links may point at Deep Dives / Known Issues pages, built or planned
_orig_page_index = _DEVM.page_index


def _combined_index():
    d = dict(_orig_page_index())
    d.update(DM.page_index())
    return d


_DEVM.page_index = _combined_index

LAYER_TITLES = {
    "guide": "User guide", "architecture": "Architecture", "internals": "Internals", "maintainer": "Maintainer workflow",
    "tests": "Tests and validation", "reference": "Reference", "deep": "Deep dives", "issues": "Known issues",
}


def area_cfg(page: str) -> dict:
    name = DM.area_of(page)
    if name is None:
        raise SystemExit(f"{page} is outside the deep-dives / known-issues areas")
    return DM.AREAS[name] | {"name": name}


# ---------------------------------------------------------------------------------------------
# furniture
# ---------------------------------------------------------------------------------------------
def sidebar_html(page: str) -> str:
    a = area_cfg(page)
    idx = DM.page_index()
    cur_group = idx[page][0]["key"] if page in idx else None
    hub = a["hub"]
    out = ['<details class="dev-nav" open>', f'  <summary class="docs-sidebar-title">{esc(a["title"])}</summary>',
           '  <ul class="dev-nav-list">']
    cls = "docs-nav-link active" if page == hub else "docs-nav-link"
    hub_attr = ' aria-current="page"' if page == hub else ""
    out.append(f'    <li class="dev-nav-item"><a href="{rel_href(page, hub)}" class="{cls}"{hub_attr}>{esc(a["title"])} home</a></li>')
    for g in a["groups"]:
        landing = DM.group_landing(a["name"], g["key"])
        pages = DM.group_pages(a["name"], g["key"])
        is_cur = g["key"] == cur_group
        link_cls = "docs-nav-link active" if page == landing else ("docs-nav-link is-group-active" if is_cur else "docs-nav-link")
        cur_attr = ' aria-current="page"' if page == landing else ""
        count = f' <span class="dev-nav-count">{len(pages)}</span>' if pages else ""
        out.append(f'    <li class="dev-nav-item{" is-open" if is_cur else ""}">'
                   f'<a href="{rel_href(page, landing)}" class="{link_cls}"{cur_attr}>{esc(g["label"])}{count}</a>')
        if is_cur and pages and a["name"] != "known-issues":  # hundreds of issue pages: the category hub lists them
            out.append('      <ul class="dev-nav-sub">')
            for p in pages:
                c = "docs-nav-link active" if p["path"] == page else "docs-nav-link"
                at = ' aria-current="page"' if p["path"] == page else ""
                out.append(f'        <li><a href="{rel_href(page, p["path"])}" class="{c}"{at}>{esc(p["label"])}</a></li>')
            out.append("      </ul>")
        out.append("    </li>")
    out += ["  </ul>", "</details>"]
    return "\n".join(out)


def breadcrumb_html(page: str) -> str:
    a = area_cfg(page)
    idx = DM.page_index()
    group, entry = idx[page]
    items = [f'<li><a href="{rel_href(page, "index.html")}">Home</a></li>']
    if page == a["hub"]:
        items.append(f'<li aria-current="page">{esc(a["title"])}</li>')
    else:
        items.append(f'<li><a href="{rel_href(page, a["hub"])}">{esc(a["title"])}</a></li>')
        landing = DM.group_landing(a["name"], group["key"])
        if page == landing:
            items.append(f'<li aria-current="page">{esc(group["label"])}</li>')
        else:
            items.append(f'<li><a href="{rel_href(page, landing)}">{esc(group["label"])}</a></li>')
            items.append(f'<li aria-current="page">{esc(entry["label"])}</li>')
    return ('<nav class="breadcrumb" aria-label="Breadcrumb">\n      <ol>\n        '
            + "\n        ".join(items) + "\n      </ol>\n    </nav>")


def pager_html(page: str) -> str:
    a = area_cfg(page)
    group, entry = DM.page_index()[page]
    if entry.get("kind") == "hub" or not group.get("key") or group["key"] == "home":
        return ""
    pages = DM.group_pages(a["name"], group["key"])
    paths = [p["path"] for p in pages]
    if page not in paths or len(pages) < 2:
        return ""
    i = paths.index(page)
    prev = pages[i - 1] if i > 0 else None
    nxt = pages[i + 1] if i + 1 < len(pages) else None
    parts = []
    if prev:
        parts.append(f'<a class="dev-pager-prev" href="{rel_href(page, prev["path"])}" rel="prev">'
                     f'<span>Previous</span>{esc(prev["title"])}</a>')
    if nxt:
        parts.append(f'<a class="dev-pager-next" href="{rel_href(page, nxt["path"])}" rel="next">'
                     f'<span>Next</span>{esc(nxt["title"])}</a>')
    return '<nav class="dev-pager" aria-label="Pages in this section">' + "".join(parts) + "</nav>" if parts else ""


def layers_html(page: str, layers: dict, errors: list[str]) -> str:
    rows = []
    for key in DM.SEE_ALSO_LAYERS:
        links = layers.get(key) or []
        if not links:
            continue
        anchors = []
        for target, label in links:
            if re.match(r"https?://", target):
                anchors.append(f'<a href="{esc(target)}" target="_blank" rel="noopener">{label}</a>')
            else:
                base = target.split("#", 1)[0]
                if not SD.known_page(base):
                    errors.append(f"{page}: layers link target does not exist: {target}")
                frag = "#" + target.split("#", 1)[1] if "#" in target else ""
                anchors.append(f'<a href="{esc(rel_href(page, base) + frag)}">{label}</a>')
        rows.append(f'<div class="dev-layers-row"><dt>{LAYER_TITLES[key]}</dt><dd>{" &middot; ".join(anchors)}</dd></div>')
    if not rows:
        return ""
    return ('<section class="dev-layers" aria-labelledby="related-layers">\n'
            '<h2 id="related-layers">Related pages</h2>\n'
            '<p>The same subject is explained at several altitudes. These are the neighbouring pages at each one.</p>\n'
            f'<dl>{"".join(rows)}</dl>\n</section>')


def head_html(page: str, meta: dict) -> str:
    a = area_cfg(page)
    title = f'{meta["title"]} - CNA {a["title"]}'
    desc = meta["description"]
    url = f"{SITE}/{page}"
    kws = meta.get("keywords") or []
    kw = f'  <meta name="keywords" content="{esc(", ".join(kws))}">\n' if kws else ""
    ld = json.dumps({
        "@context": "https://schema.org", "@type": "TechArticle", "headline": meta["title"], "description": desc,
        "url": url, "datePublished": TODAY, "dateModified": TODAY,
        "isPartOf": {"@type": "CreativeWorkSeries", "name": a["part_of"], "url": f"{SITE}/{a['hub']}"},
        "author": {"@type": "Organization", "name": "libcna", "url": "https://github.com/libcna"},
        "technicalAudience": "Software Developer", "proficiencyLevel": "Expert",
    }, ensure_ascii=False, separators=(",", ":"))
    prefix = rel_href(page, "css/style.css")[: -len("css/style.css")]
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}">
{kw}  <meta property="og:type" content="website">
  <meta property="og:site_name" content="CNA">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(desc)}">
  <link rel="stylesheet" href="{prefix}css/style.css">
  <link rel="icon" href="{prefix}favicon.svg" type="image/svg+xml">
  <link rel="canonical" href="{url}">
  <link rel="stylesheet" href="{prefix}css/prism-tomorrow.min.css">
  <script type="application/ld+json">
  {ld}
  </script>
  <script>(function(){{try{{var t=localStorage.getItem("cna-theme");if(t==="light"||t==="dark")document.documentElement.setAttribute("data-theme",t);}}catch(e){{}}}})();</script>
</head>
<body>
'''


def page_shell(page: str, meta: dict, body: str, evidence: str, toc: str, layers: str, group_label: str) -> str:
    a = area_cfg(page)
    prefix = rel_href(page, "index.html")[: -len("index.html")]
    docs_prefix = prefix + "docs/"
    text = head_html(page, meta)
    text += site_nav.nav_block(prefix, a["hub"])
    text += f'''
<main id="main-content">
  <div class="docs-layout">

    <aside class="docs-sidebar">
<!--deep:sidebar-->
{sidebar_html(page)}
<!--/deep:sidebar-->
    </aside>

<!--deep:breadcrumb-->
    {breadcrumb_html(page)}
<!--/deep:breadcrumb-->
    <article class="docs-content dev-content">
      <h1>{esc(meta["title"])}</h1>
{toc}      <p class="doc-meta">CNA snapshot {TARGET_SHORT} &nbsp;&middot;&nbsp; {esc(a["title"])} &rsaquo; {esc(group_label)} &nbsp;&middot;&nbsp; source links pinned to <code>{TARGET_SHORT}</code></p>
{evidence}

{body.strip()}

{layers}
<!--deep:pager-->
{pager_html(page)}
<!--/deep:pager-->
    </article>
  </div>
</main>

'''
    text += site_nav.footer_block(prefix, docs_prefix, False)
    return text


def render_page(page: str, meta: dict, body: str, errors: list[str]) -> str:
    idx = DM.page_index()
    if page not in idx:
        raise SystemExit(f"{page} is not declared in audit/data/deep-pages/*.json")
    group, entry = idx[page]
    body = SD.expand_tokens(body, page, errors)
    body = re.sub(r"<table\b", '<div class="table-wrap"><table', body)
    body = body.replace("</table>", "</table></div>")
    layers = layers_html(page, meta.get("layers") or {}, errors)
    toc = SD.auto_toc(body, bool(layers))
    if body.count('id="related-layers"'):
        errors.append(f"{page}: body must not define id=related-layers")
    return page_shell(page, meta, body, SD.evidence_html(meta), toc, layers, group["label"])


# ---------------------------------------------------------------------------------------------
# generated hubs
# ---------------------------------------------------------------------------------------------
def built_description(path: str) -> str:
    p = ROOT / path
    if not p.exists():
        return ""
    m = re.search(r'<meta name="description" content="([^"]*)"', p.read_text(encoding="utf-8"))
    return html.unescape(m.group(1)) if m else ""


def hub_body(page: str) -> tuple[dict, str]:
    a = area_cfg(page)
    idx = DM.page_index()
    group, entry = idx[page]
    if a["name"] == "known-issues":
        import known_issues as KI
        res = KI.hub_body(page, a["hub"], None if page == a["hub"] else group["key"])
        if res:
            return res
    if page == a["hub"]:
        cards = []
        for g in a["groups"]:
            pages = DM.group_pages(a["name"], g["key"])
            landing = DM.group_landing(a["name"], g["key"])
            n = f' <span class="dev-nav-count">{len(pages)} pages</span>' if pages else ""
            cards.append(f'  <div class="card"><h3 id="group-{g["key"]}"><a href="{rel_href(page, landing)}">{esc(g["label"])}</a>{n}</h3><p>{esc(g["intro"])}</p></div>')
        if a["name"] == "deep-dives":
            meta = {"title": "Deep Dives",
                    "description": "Long-form technical knowledge about CNA: lifecycle, math, graphics, renderers, content, 3D, services, platforms and evidence, "
                                   "each explained with its exact semantics and pinned to one source snapshot.",
                    "keywords": ["deep dive", "internals", "semantics", "architecture", "cna", "xna"],
                    "evidence": {"levels": ["source-verified", "test-present"]}}
            lede = ('<p class="lede">The Deep Dives are the long-form layer of libcna.com. Where a guide tells you how to use a feature and the '
                    '<a href="../development/index.html">Development area</a> tells a maintainer how to change it, a deep dive explains what the feature '
                    '<em>means</em>: its exact semantics, the invariants behind it, why CNA behaves this way, what evidence supports each claim and where the '
                    'edges are. They are written for advanced CNA users and for anyone who needs the precise answer.</p>')
            extra = ('<h2 id="how">How to use these pages</h2>\n'
                     '<ul>\n<li><strong>Start from a subject, not a chapter.</strong> Each group below is a subject area; each page inside is one concept.</li>\n'
                     '<li><strong>Pages link outward.</strong> Every deep dive lists its neighbouring user guide, architecture map, internals tour, maintainer recipe, tests '
                     'and known issues in a <em>Related pages</em> block.</li>\n'
                     '<li><strong>Evidence is graded.</strong> Each page states its basis (source-verified, tests present, and so on). &ldquo;The implementation exists&rdquo; '
                     'is never presented as &ldquo;the behaviour is proven correct everywhere&rdquo;, and representation coverage is never presented as behavioural parity.</li>\n'
                     '<li><strong>One snapshot.</strong> Everything is pinned to CNA commit <code>' + TARGET_SHORT + '</code>. '
                     'Current defects are listed on <a href="../known-issues/index.html">Known Issues</a>, not repeated here.</li>\n</ul>')
        else:
            meta = {"title": "Known Issues",
                    "description": "Current bugs, functional gaps, platform limitations and verification gaps in CNA at the pinned snapshot, each with its evidence and a stable identifier.",
                    "keywords": ["known issues", "bugs", "gaps", "limitations", "cna-bug", "verification gaps"],
                    "evidence": {"levels": ["source-verified"]}}
            lede = ('<p class="lede">This area answers one question: <em>what is wrong with, or missing from, CNA right now?</em> It lists only what exists at CNA commit '
                    f'<code>{TARGET_SHORT}</code>. A defect that was fixed is not listed; a limitation that is a deliberate design choice is not called a bug.</p>')
            extra = ""
        body = lede + "\n" + f'<h2 id="areas">{"Subjects" if a["name"] == "deep-dives" else "Categories"}</h2>\n<div class="cards cards--2">\n' + "\n".join(cards) + "\n</div>\n" + extra
        return meta, body
    pages = DM.group_pages(a["name"], group["key"])
    meta = {"title": group["label"],
            "description": group["intro"][:215].rstrip(),
            "keywords": [group["key"], a["title"].lower(), "cna"],
            "evidence": {"levels": ["source-verified"]}}
    items = []
    for p in pages:
        d = built_description(p["path"])
        items.append(f'<li><a href="{rel_href(page, p["path"])}"><strong>{esc(p["title"])}</strong></a>'
                     f'{" &mdash; " + esc(d) if d else ""}</li>')
    listing = ('<ul class="deep-list">\n' + "\n".join(items) + "\n</ul>") if items else "<p>No pages in this group yet.</p>"
    body = f'<p class="lede">{esc(group["intro"])}</p>\n<h2 id="pages">Pages in this group</h2>\n{listing}'
    return meta, body


def render_hub(page: str) -> str:
    meta, body = hub_body(page)
    group, entry = DM.page_index()[page]
    toc = ""
    return page_shell(page, meta, body, SD.evidence_html(meta), toc, "", group["label"])


def cmd_hubs(_: argparse.Namespace) -> int:
    n = 0
    for p in DM.all_pages():
        if p.get("kind") != "hub":
            continue
        out = ROOT / p["path"]
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_hub(p["path"]), encoding="utf-8")
        n += 1
    print(f"generated {n} hub page(s)")
    return 0


# ---------------------------------------------------------------------------------------------
# build / sync / check
# ---------------------------------------------------------------------------------------------
def cmd_build(args: argparse.Namespace) -> int:
    src_dir = Path(args.src)
    authored = [p for p in DM.all_pages() if p.get("kind") != "hub"]
    wanted = args.paths or [p["path"] for p in authored if (src_dir / (p["path"][:-5] + ".body.html")).exists()]
    # manifest problems only block a build when they concern a page being built (other packages may be mid-edit)
    errors: list[str] = [e for e in DM.problems() if any(w in e for w in wanted)]
    built = 0
    for page in wanted:
        meta, body = SD.read_src(src_dir, page)
        text = render_page(page, meta, body, errors)
        if errors:
            continue
        out = ROOT / page
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        built += 1
    if errors:
        print(f"FAILED ({len(errors)} error(s)); nothing written for pages with errors:")
        for e in errors:
            print(" -", e)
        return 1
    print(f"built {built} page(s)")
    return 0


REGION = {
    "sidebar": re.compile(r"<!--deep:sidebar-->\n.*?\n<!--/deep:sidebar-->", re.S),
    "breadcrumb": re.compile(r"<!--deep:breadcrumb-->\n.*?\n<!--/deep:breadcrumb-->", re.S),
    "pager": re.compile(r"<!--deep:pager-->\n.*?\n<!--/deep:pager-->", re.S),
}


def region_text(name: str, page: str) -> str:
    if name == "sidebar":
        return f"<!--deep:sidebar-->\n{sidebar_html(page)}\n<!--/deep:sidebar-->"
    if name == "breadcrumb":
        return f"<!--deep:breadcrumb-->\n    {breadcrumb_html(page)}\n<!--/deep:breadcrumb-->"
    return f"<!--deep:pager-->\n{pager_html(page)}\n<!--/deep:pager-->"


def cmd_sync(_: argparse.Namespace) -> int:
    changed = 0
    for entry in DM.all_pages():
        path = ROOT / entry["path"]
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        new = text
        for name, rx in REGION.items():
            if not rx.search(new):
                print(f"warning: {entry['path']} has no {name} region")
                continue
            new = rx.sub(lambda _m, n=name, p=entry["path"]: region_text(n, p), new, count=1)
        if new != text:
            path.write_text(new, encoding="utf-8")
            changed += 1
    print(f"regions rewritten in {changed} page(s)")
    return 0


def cmd_check(_: argparse.Namespace) -> int:
    rc = 0
    for e in DM.problems():
        print("PROBLEM", e)
        rc = 1
    declared = {p["path"] for p in DM.all_pages()}
    on_disk: set[str] = set()
    for a in DM.AREAS.values():
        d = ROOT / a["root"]
        if d.is_dir():
            on_disk |= {p.relative_to(ROOT).as_posix() for p in d.rglob("*.html")}
    for p in sorted(declared - on_disk):
        print("declared but not built:", p)
        rc = 1
    for p in sorted(on_disk - declared):
        print("page not declared in audit/data/deep-pages:", p)
        rc = 1
    print(f"deep/known-issues pages declared {len(declared)}, on disk {len(on_disk)}")
    return rc


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--src", required=True)
    b.add_argument("paths", nargs="*")
    sub.add_parser("hubs")
    sub.add_parser("sync")
    sub.add_parser("check")
    args = ap.parse_args()
    return {"build": cmd_build, "hubs": cmd_hubs, "sync": cmd_sync, "check": cmd_check}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
