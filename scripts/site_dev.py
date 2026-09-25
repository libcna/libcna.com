#!/usr/bin/env python3
"""Build and maintain the Development area (development/**) of libcna.com.

    site_dev.py build  --src DIR [PATH ...]   # write pages from DIR/<path minus .html>.body.html + .meta.json
    site_dev.py sync                          # rewrite sidebar / breadcrumb / pager on every development page
    site_dev.py check                         # manifest vs disk, marker and token sanity (no writes)

The page set, order and sidebar come from scripts/dev_manifest.py.  Body fragments are authored HTML for the
inside of <article class="docs-content"> and may use three tokens, expanded (and validated) here:

    {{src:modules/runtime/src/Game.cpp}}            link to that file at the TARGET commit, label = the path
    {{src:modules/runtime/src/Game.cpp#L40-L60|Game::Tick}}   optional line range and label
    {{tree:modules/platform/src|platform sources}}  link to a directory at the TARGET commit
    {{page:development/internals/runtime/startup.html#ctor|startup trace}}   link to another site page

A {{src:...}} or {{tree:...}} whose path does not exist in the TARGET tree is a build error: source
links on these pages are pinned to the exact snapshot and are checked at generation time.

Fragment meta (.meta.json):
    title, description (required); keywords (list); evidence {levels:[...], note:"..."};
    layers {guide|architecture|internals|maintainer|tests|reference: [[site-path-or-url, label], ...]};
    developer_sources [..]  (informational)
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dev_manifest as M  # noqa: E402
import site_nav  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://libcna.com"
TARGET = (ROOT / "cnahead").read_text(encoding="utf-8").strip()
TARGET_SHORT = TARGET[:8]
TODAY = "2026-09-25"
CNA_REPO = Path(os.environ.get("CNA_REPO", ROOT.parent / "cna"))

EVIDENCE_LABELS = {
    "source-verified": "source-verified at the pinned commit",
    "test-present": "tests exist (not executed for this page)",
    "executed": "executed for this entry (the Evidence section names exactly what was run)",
    "recorded-by-cna": "recorded by CNA's own run (not repeated here)",
    "inferred": "inferred from the source (the behaviour was not run)",
    "build-verified": "build-verified (recorded by CNA, not re-run here)",
    "runtime-observed": "runtime-observed (recorded by CNA, not re-run here)",
    "oracle-compared": "oracle-compared (recorded by CNA, not re-run here)",
    "hardware-observed": "hardware-observed (recorded by CNA, not re-run here)",
}

_tree_cache: tuple[set[str], set[str]] | None = None


def target_tree() -> tuple[set[str], set[str]]:
    """(files, directories) of the TARGET commit, read from Git objects (no checkout)."""
    global _tree_cache
    if _tree_cache is None:
        out = subprocess.run(["git", "-C", str(CNA_REPO), "ls-tree", "-r", "--name-only", TARGET],
                             check=True, capture_output=True, text=True).stdout.splitlines()
        files = set(out)
        dirs: set[str] = set()
        for f in files:
            parts = f.split("/")
            for i in range(1, len(parts)):
                dirs.add("/".join(parts[:i]))
        _tree_cache = (files, dirs)
    return _tree_cache


def src_url(path: str, kind: str = "blob", frag: str = "") -> str:
    return f"https://github.com/libcna/cna/{kind}/{TARGET}/{quote(path)}{frag}"


# ---------------------------------------------------------------------------------------------
# token expansion
# ---------------------------------------------------------------------------------------------
SRC_RE = re.compile(r"\{\{src:([^|}#]+)(#L\d+(?:-L\d+)?)?(?:\|([^}]*))?\}\}")
TREE_RE = re.compile(r"\{\{tree:([^|}]+)(?:\|([^}]*))?\}\}")
PAGE_RE = re.compile(r"\{\{page:([^|}#]+)(#[^|}]+)?(?:\|([^}]*))?\}\}")
RAW_GH_RE = re.compile(r'https://github\.com/libcna/cna/(blob|tree)/([^/"\s]+)/([^"#\s]*)')


def rel_href(from_page: str, to_path: str) -> str:
    """Relative URL from one site page to another site path."""
    return os.path.relpath(to_path, os.path.dirname(from_page) or ".").replace(os.sep, "/")


def known_page(path: str) -> bool:
    return path in M.page_index() or (ROOT / path).exists()


def expand_tokens(text: str, page: str, errors: list[str]) -> str:
    files, dirs = target_tree()
    # hand-written links to the CNA repository must already be pinned to TARGET and exist there
    for kind, rev, path in RAW_GH_RE.findall(text):
        clean = path.rstrip("/")
        if rev != TARGET:
            errors.append(f"{page}: raw CNA link is not pinned to TARGET ({rev}/{clean})")
        elif clean not in files and clean not in dirs:
            errors.append(f"{page}: raw CNA link path absent at TARGET: {clean}")

    def src(m: re.Match) -> str:
        path, frag, label = m.group(1).strip(), m.group(2) or "", m.group(3)
        if path not in files:
            errors.append(f"{page}: source path absent at TARGET: {path}")
        return (f'<a class="src-link" href="{html.escape(src_url(path, "blob", frag))}">'
                f'<code>{html.escape(label if label else path)}</code></a>')

    def tree(m: re.Match) -> str:
        path, label = m.group(1).strip().rstrip("/"), m.group(2)
        if path not in dirs:
            errors.append(f"{page}: source directory absent at TARGET: {path}")
        return (f'<a class="src-link" href="{html.escape(src_url(path, "tree"))}">'
                f'<code>{html.escape(label if label else path + "/")}</code></a>')

    def pg(m: re.Match) -> str:
        path, frag, label = m.group(1).strip(), m.group(2) or "", m.group(3)
        if not known_page(path):
            errors.append(f"{page}: {{page:}} target does not exist: {path}")
        if not label:
            entry = M.page_index().get(path)
            label = entry[1]["title"] if entry else path
        return f'<a href="{html.escape(rel_href(page, path) + frag)}">{label}</a>'

    text = SRC_RE.sub(src, text)
    text = TREE_RE.sub(tree, text)
    text = PAGE_RE.sub(pg, text)
    leftover = re.findall(r"\{\{[a-z]+:[^}]*\}\}", text)
    for tok in leftover:
        errors.append(f"{page}: unexpanded token {tok}")
    return text


# ---------------------------------------------------------------------------------------------
# page furniture
# ---------------------------------------------------------------------------------------------
GROUP_HEADINGS = {
    "handbook": "Do the work",
    "architecture": "How CNA is built",
    "reference": "Look things up",
}


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def sidebar_html(page: str) -> str:
    idx = M.page_index()
    cur_group = idx[page][0]["key"] if page in idx else None
    out = ['<details class="dev-nav" open>',
           '  <summary class="docs-sidebar-title">Development</summary>',
           '  <ul class="dev-nav-list">']
    for g in M.GROUPS:
        heading = GROUP_HEADINGS.get(g["key"])
        if heading:
            out.append(f'    <li class="dev-nav-heading" role="presentation">{esc(heading)}</li>')
        landing = g["pages"][0]["path"]
        is_cur = g["key"] == cur_group
        link_cls = "docs-nav-link active" if page == landing else ("docs-nav-link is-group-active" if is_cur else "docs-nav-link")
        cur_attr = ' aria-current="page"' if page == landing else ""
        out.append(f'    <li class="dev-nav-item{" is-open" if is_cur else ""}">'
                   f'<a href="{rel_href(page, landing)}" class="{link_cls}"{cur_attr}>{esc(g["label"])}</a>')
        if is_cur and len(g["pages"]) > 1:
            out.append('      <ul class="dev-nav-sub">')
            for p in g["pages"][1:]:  # the group link above already is the landing page
                cls = "docs-nav-link active" if p["path"] == page else "docs-nav-link"
                attr = ' aria-current="page"' if p["path"] == page else ""
                out.append(f'        <li><a href="{rel_href(page, p["path"])}" class="{cls}"{attr}>{esc(p["label"])}</a></li>')
            out.append("      </ul>")
        out.append("    </li>")
    out += ["  </ul>", "</details>"]
    return "\n".join(out)


def breadcrumb_html(page: str) -> str:
    idx = M.page_index()
    group, entry = idx[page]
    crumbs: list[tuple[str, str]] = [("Home", "index.html")]
    if page != "development/index.html":
        crumbs.append(("Development", "development/index.html"))
    items = []
    for label, path in crumbs:
        items.append(f'<li><a href="{rel_href(page, path)}">{esc(label)}</a></li>')
    if page == "development/index.html":
        items = [f'<li><a href="{rel_href(page, "index.html")}">Home</a></li>',
                 '<li aria-current="page">Development</li>']
    else:
        seg = list(group["crumbs"])
        crumb_paths = [p for _, p in seg]
        if page in crumb_paths:
            seg = seg[:crumb_paths.index(page)]
            tail_label = dict((p, l) for l, p in group["crumbs"])[page]
            for label, path in seg:
                items.append(f'<li><a href="{rel_href(page, path)}">{esc(label)}</a></li>')
            items.append(f'<li aria-current="page">{esc(tail_label)}</li>')
        else:
            for label, path in seg:
                items.append(f'<li><a href="{rel_href(page, path)}">{esc(label)}</a></li>')
            items.append(f'<li aria-current="page">{esc(entry["label"])}</li>')
    return ('<nav class="breadcrumb" aria-label="Breadcrumb">\n      <ol>\n        '
            + "\n        ".join(items) + "\n      </ol>\n    </nav>")


def pager_html(page: str) -> str:
    group, _ = M.page_index()[page]
    pages = group["pages"]
    if len(pages) < 2:
        return ""
    i = [p["path"] for p in pages].index(page)
    prev = pages[i - 1] if i > 0 else None
    nxt = pages[i + 1] if i + 1 < len(pages) else None
    if not prev and not nxt:
        return ""
    parts = []
    if prev:
        parts.append(f'<a class="dev-pager-prev" href="{rel_href(page, prev["path"])}" rel="prev">'
                     f'<span>Previous</span>{esc(prev["title"])}</a>')
    if nxt:
        parts.append(f'<a class="dev-pager-next" href="{rel_href(page, nxt["path"])}" rel="next">'
                     f'<span>Next</span>{esc(nxt["title"])}</a>')
    return '<nav class="dev-pager" aria-label="Pages in this section">' + "".join(parts) + "</nav>"


LAYER_TITLES = {
    "guide": "User guide", "architecture": "Architecture", "internals": "Internals",
    "maintainer": "Maintainer workflow", "tests": "Tests and validation", "reference": "Reference",
}


def layers_html(page: str, layers: dict, errors: list[str]) -> str:
    rows = []
    for key in M.SEE_ALSO_LAYERS:
        links = layers.get(key) or []
        if not links:
            continue
        anchors = []
        for target, label in links:
            if re.match(r"https?://", target):
                anchors.append(f'<a href="{esc(target)}" target="_blank" rel="noopener">{label}</a>')
            else:
                base = target.split("#", 1)[0]
                if not known_page(base):
                    errors.append(f"{page}: layers link target does not exist: {target}")
                frag = "#" + target.split("#", 1)[1] if "#" in target else ""
                anchors.append(f'<a href="{esc(rel_href(page, base) + frag)}">{label}</a>')
        rows.append(f'<div class="dev-layers-row"><dt>{LAYER_TITLES[key]}</dt><dd>{" &middot; ".join(anchors)}</dd></div>')
    if not rows:
        return ""
    return ('<section class="dev-layers" aria-labelledby="related-layers">\n'
            '<h2 id="related-layers">Related pages</h2>\n'
            '<p>The same subsystem is explained at four altitudes. These are the neighbouring pages at each one.</p>\n'
            f'<dl>{"".join(rows)}</dl>\n</section>')


def evidence_html(meta: dict) -> str:
    ev = meta.get("evidence") or {}
    levels = ev.get("levels") or ["source-verified"]
    labels = "; ".join(EVIDENCE_LABELS.get(l, l) for l in levels)
    note = ev.get("note", "")
    text = (f'<strong>Evidence basis:</strong> {esc(labels)}. Claims on this page were checked by reading the CNA source '
            f'at commit <code>{TARGET_SHORT}</code>; unless a sentence says otherwise, nothing here was built or executed.')
    if note:
        text += f' {note}'
    return (f'<div class="callout callout--note dev-evidence"><span class="callout-icon">&#10003;</span>'
            f'<p>{text}</p></div>')


def auto_toc(body: str, has_layers: bool) -> str:
    entries = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body, re.S)
    if has_layers:
        entries.append(("related-layers", "Related pages"))
    if len(entries) < 3:
        return ""
    lis = "\n".join(f'          <li><a href="#{i}">{t}</a></li>' for i, t in entries)
    return (f'      <nav class="toc" aria-label="Table of contents">\n        <h2 class="toc-title">On this page</h2>\n'
            f'        <ul class="toc-list">\n{lis}\n        </ul>\n      </nav>\n')


def head_html(page: str, meta: dict) -> str:
    title = f'{meta["title"]} - CNA Development'
    desc = meta["description"]
    url = f"{SITE}/{page}"
    kws = meta.get("keywords") or []
    kw = f'  <meta name="keywords" content="{esc(", ".join(kws))}">\n' if kws else ""
    ld = json.dumps({
        "@context": "https://schema.org", "@type": "TechArticle", "headline": meta["title"], "description": desc,
        "url": url, "datePublished": TODAY, "dateModified": TODAY,
        "isPartOf": {"@type": "CreativeWorkSeries", "name": "CNA Development", "url": f"{SITE}/development/index.html"},
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


def render_page(page: str, meta: dict, body: str, errors: list[str]) -> str:
    idx = M.page_index()
    if page not in idx:
        raise SystemExit(f"{page} is not in scripts/dev_manifest.py")
    group, entry = idx[page]
    prefix = rel_href(page, "index.html")[: -len("index.html")]
    docs_prefix = prefix + "docs/"
    body = expand_tokens(body, page, errors)
    # wide tables scroll inside their own box (fragments must not wrap tables themselves)
    body = re.sub(r"<table\b", '<div class="table-wrap"><table', body)
    body = body.replace("</table>", "</table></div>")
    layers = layers_html(page, meta.get("layers") or {}, errors)
    toc = auto_toc(body, bool(layers))
    if body.count('id="related-layers"'):
        errors.append(f"{page}: body must not define id=related-layers")
    text = head_html(page, meta)
    text += site_nav.nav_block(prefix, "development/index.html")
    text += f'''
<main id="main-content">
  <div class="docs-layout">

    <aside class="docs-sidebar">
<!--dev:sidebar-->
{sidebar_html(page)}
<!--/dev:sidebar-->
    </aside>

<!--dev:breadcrumb-->
    {breadcrumb_html(page)}
<!--/dev:breadcrumb-->
    <article class="docs-content dev-content">
      <h1>{esc(meta["title"])}</h1>
{toc}      <p class="doc-meta">CNA snapshot {TARGET_SHORT} &nbsp;&middot;&nbsp; Development &rsaquo; {esc(group["label"])} &nbsp;&middot;&nbsp; source links pinned to <code>{TARGET_SHORT}</code></p>
      {evidence_html(meta)}

{body.strip()}

{layers}
<!--dev:pager-->
{pager_html(page)}
<!--/dev:pager-->
    </article>
  </div>
</main>

'''
    text += site_nav.footer_block(prefix, docs_prefix, False)
    return text


def read_src(src_dir: Path, page: str) -> tuple[dict, str]:
    stem = src_dir / page[: -len(".html")]
    meta_path, body_path = Path(str(stem) + ".meta.json"), Path(str(stem) + ".body.html")
    if not meta_path.exists() or not body_path.exists():
        raise SystemExit(f"missing fragment for {page}: {body_path} / {meta_path}")
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    for key in ("title", "description"):
        if not meta.get(key):
            raise SystemExit(f"{meta_path}: missing {key}")
    return meta, body_path.read_text(encoding="utf-8")


def cmd_build(args: argparse.Namespace) -> int:
    src_dir = Path(args.src)
    wanted = args.paths or [p["path"] for p in M.all_pages()
                            if (src_dir / (p["path"][:-5] + ".body.html")).exists()]
    errors: list[str] = []
    built = 0
    for page in wanted:
        meta, body = read_src(src_dir, page)
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
    "sidebar": (re.compile(r"<!--dev:sidebar-->\n.*?\n<!--/dev:sidebar-->", re.S), sidebar_html),
    "breadcrumb": (re.compile(r"<!--dev:breadcrumb-->\n.*?\n<!--/dev:breadcrumb-->", re.S), None),
    "pager": (re.compile(r"<!--dev:pager-->\n.*?\n<!--/dev:pager-->", re.S), pager_html),
}


def region_text(name: str, page: str) -> str:
    if name == "sidebar":
        return f"<!--dev:sidebar-->\n{sidebar_html(page)}\n<!--/dev:sidebar-->"
    if name == "breadcrumb":
        return f"<!--dev:breadcrumb-->\n    {breadcrumb_html(page)}\n<!--/dev:breadcrumb-->"
    return f"<!--dev:pager-->\n{pager_html(page)}\n<!--/dev:pager-->"


def cmd_sync(_: argparse.Namespace) -> int:
    changed = 0
    for entry in M.all_pages():
        path = ROOT / entry["path"]
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        new = text
        for name in ("sidebar", "breadcrumb", "pager"):
            rx = REGION[name][0]
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
    idx = M.page_index()
    on_disk = {p.relative_to(ROOT).as_posix() for p in (ROOT / "development").rglob("*.html")}
    missing = sorted(set(idx) - on_disk)
    extra = sorted(on_disk - set(idx))
    for p in missing:
        print("missing page:", p)
    for p in extra:
        print("page not in manifest:", p)
    return 1 if missing or extra else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--src", required=True)
    b.add_argument("paths", nargs="*")
    sub.add_parser("sync")
    sub.add_parser("check")
    args = ap.parse_args()
    return {"build": cmd_build, "sync": cmd_sync, "check": cmd_check}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
