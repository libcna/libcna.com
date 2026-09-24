#!/usr/bin/env python3
"""Canonical docs sidebar, shared by every docs/*.html page, and a new-page generator.

    site_nav.py sync                 # rewrite <ul class="docs-nav-list"> in every docs/*.html
    site_nav.py new-docs  --slug content-pipeline --title "Content Pipeline" \
        --description "..." --body body.html [--toc] [--after xna-compatibility] [--label "Sidebar label"]
    site_nav.py new-tutorial --number 130 --slug opengl4-desktop --title "..." \
        --description "..." --body body.html [--learn "..."]

The sidebar order lives in SIDEBAR below; entries whose file does not exist are skipped, so the
list can name pages that other work packages are still writing.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SITE = "https://libcna.com"
TODAY = "2026-09-24"

# (file, sidebar label) in display order
SIDEBAR: list[tuple[str, str]] = [
    ("getting-started.html", "Getting Started"),
    ("building.html", "Building"),
    ("releases.html", "Releases &amp; Versioning"),
    ("platforms.html", "Platforms"),
    ("native-platforms.html", "Native Platforms (X11, Wayland, Win32)"),
    ("rendering-backends.html", "Renderers"),
    ("runtime-renderer-selection.html", "Runtime Renderer Selection"),
    ("xna-compatibility.html", "XNA Compatibility"),
    ("verification.html", "Verification &amp; Known Issues"),
    ("c-api.html", "Experimental C API"),
    ("effects.html", "Effects System"),
    ("shader-effects.html", "Shader Effects"),
    ("cnaext-engine.html", "CNAEXT Engine Layer"),
    ("render-targets.html", "Render Targets"),
    ("spritebatch.html", "SpriteBatch"),
    ("audio.html", "Audio System"),
    ("input.html", "Input System"),
    ("math-types.html", "Math Types"),
    ("content-manager.html", "ContentManager"),
    ("content-pipeline-xnb.html", "XNB Loading"),
    ("content-pipeline.html", "Content Pipeline"),
    ("cnb-format.html", "CNB Format"),
    ("tools.html", "Command-Line Tools"),
    ("3d-rendering.html", "3D Rendering"),
    ("packed-vector.html", "PackedVector Types"),
    ("vs-alternatives.html", "CNA vs Alternatives"),
    ("migration-from-monogame.html", "Migration from MonoGame"),
    ("game-loop.html", "Game Loop"),
    ("graphics-state.html", "Graphics State"),
    ("model-loading.html", "Model Loading"),
    ("video-playback.html", "Video Playback"),
    ("storage.html", "Storage"),
    ("sensors.html", "Sensors"),
    ("design-converters.html", "Framework.Design"),
    ("diagnostics.html", "Diagnostics"),
    ("inspector.html", "Inspector"),
    ("../roadmap.html", "Roadmap"),
    ("faq.html", "FAQ"),
]

SIDEBAR_RE = re.compile(r'(<ul class="docs-nav-list">)(.*?)(</ul>)', re.S)


def sidebar_html(active: str, indent: str = "") -> str:
    items = []
    for target, label in SIDEBAR:
        if not (DOCS / target).exists():
            continue
        cls = "docs-nav-link active" if target == active else "docs-nav-link"
        items.append(f'{indent}<li><a href="{target}" class="{cls}">{label}</a></li>')
    return "\n".join(items)


def sync_sidebars() -> int:
    changed = 0
    for path in sorted(DOCS.glob("*.html")):
        text = path.read_text(encoding="utf-8")
        if 'class="docs-nav-list"' not in text:
            continue
        active = path.name
        new = SIDEBAR_RE.sub(
            lambda m: m.group(1) + "\n" + sidebar_html(active, "        ") + "\n      " + m.group(3),
            text, count=1)
        if new != text:
            path.write_text(new, encoding="utf-8")
            changed += 1
    return changed


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def head_block(rel: str, title: str, description: str, root_prefix: str, kind: str, headline: str,
               tutorial: bool) -> str:
    url = f"{SITE}/{rel}"
    ld_extra = ('"isPartOf":{"@type":"CreativeWorkSeries","name":"CNA Tutorial Series",'
                '"url":"https://libcna.com/tutorials.html"},') if tutorial else ""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="CNA">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <link rel="stylesheet" href="{root_prefix}css/style.css">
  <link rel="icon" href="{root_prefix}favicon.svg" type="image/svg+xml">
  <link rel="canonical" href="{url}">
  <link rel="stylesheet" href="{root_prefix}css/prism-tomorrow.min.css">
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"TechArticle","headline":"{esc(headline)}","description":"{esc(description)}","url":"{url}","datePublished":"{TODAY}","dateModified":"{TODAY}",{ld_extra}"author":{{"@type":"Organization","name":"libcna","url":"https://github.com/libcna"}},"technicalAudience":"Software Developer","proficiencyLevel":"Advanced"}}
  </script>
  <script>(function(){{try{{var t=localStorage.getItem("cna-theme");if(t==="light"||t==="dark")document.documentElement.setAttribute("data-theme",t);}}catch(e){{}}}})();</script>
</head>
<body>
'''


def nav_block(root_prefix: str, active: str) -> str:
    items = [("index.html", "Home"), ("about.html", "About"), ("features.html", "Features"),
             ("architecture.html", "Architecture"), ("documentation.html", "Documentation"),
             ("tutorials.html", "Tutorials"), ("demos.html", "Demos"), ("showcase.html", "Showcase"),
             ("videos.html", "Videos"), ("roadmap.html", "Roadmap"), ("contact.html", "Contact"),
             ("network.html", "Network"), ("search.html", "Search")]
    links = "\n".join(
        f'    <a href="{root_prefix}{f}" class="nav-link{" active" if f == active else ""}">{l}</a>'
        for f, l in items)
    return f'''<a class="skip-link" href="#main-content">Skip to content</a>
<nav class="nav"><div class="nav-container">
  <a href="{root_prefix}index.html" class="nav-brand">CNA</a>
  <button class="nav-toggle" aria-label="Toggle navigation" aria-expanded="false"><span></span><span></span><span></span></button>
  <div class="nav-menu">
{links}
    <a href="https://github.com/libcna/cna" class="nav-link nav-link--github" target="_blank" rel="noopener">GitHub</a>
    <a href="https://blog.libcna.com/" class="nav-link nav-link--blog" target="_blank" rel="noopener">Blog</a>
    <a href="https://www.youtube.com/@libcna" class="nav-link nav-link--youtube" target="_blank" rel="noopener">YouTube</a>
    <a href="https://discord.gg/vrnc4n6DaE" class="nav-link nav-link--discord" target="_blank" rel="noopener">Discord</a>
  </div>
  <button class="theme-toggle" type="button" aria-label="Switch to light theme" title="Switch to light theme">
    <svg class="theme-icon-light" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M12 17a5 5 0 1 1 0-10 5 5 0 0 1 0 10zm0-2a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM11 1h2v3h-2V1zm0 19h2v3h-2v-3zM3.5 4.9l1.4-1.4 2.1 2.1-1.4 1.4L3.5 4.9zm13.5 13.5l1.4-1.4 2.1 2.1-1.4 1.4-2.1-2.1zM19.1 3.5l1.4 1.4-2.1 2.1-1.4-1.4 2.1-2.1zM5.6 17l1.4 1.4-2.1 2.1-1.4-1.4L5.6 17zM23 11v2h-3v-2h3zM4 11v2H1v-2h3z"/></svg>
    <svg class="theme-icon-dark" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M12.3 22a10 10 0 0 1-1.6-19.9c.6-.1 1 .5.8 1a7.9 7.9 0 0 0 9.7 10.6c.5-.2 1 .3.9.8A10 10 0 0 1 12.3 22z"/></svg>
  </button>
</div></nav>
'''


def footer_block(root_prefix: str, docs_prefix: str, tutorial: bool) -> str:
    scripts = ["js/main.js"]
    tail = "".join(f'<script src="{root_prefix}{s}"></script>\n' for s in scripts)
    for s in ("prism.min", "prism-cpp.min", "prism-glsl.min", "prism-json.min", "prism-bash.min", "prism-cmake.min"):
        tail += f'<script src="{root_prefix}js/prism/{s}.js" defer></script>\n'
    if tutorial:
        tail += f'<script src="{root_prefix}js/tutorial-progress.js"></script>\n'
    return f'''<footer><div class="footer-inner">
  <div class="footer-top">
    <div class="footer-brand"><div class="footer-brand-name">CNA</div><p>Documentation snapshot for CNA commit 009d40f5 (24 September 2026), a post-alpha.1 development snapshot. CNA exposes 25 renderer identities across 21 implementation families; APIs may change before 1.0.</p></div>
    <div class="footer-col"><h4>Project</h4><ul><li><a href="{root_prefix}about.html">About</a></li><li><a href="{root_prefix}features.html">Features</a></li><li><a href="{root_prefix}architecture.html">Architecture</a></li><li><a href="{root_prefix}roadmap.html">Roadmap</a></li></ul></div>
    <div class="footer-col"><h4>Docs</h4><ul><li><a href="{docs_prefix}getting-started.html">Getting Started</a></li><li><a href="{docs_prefix}building.html">Building</a></li><li><a href="{docs_prefix}platforms.html">Platforms</a></li><li><a href="{docs_prefix}rendering-backends.html">Renderers</a></li><li><a href="{docs_prefix}faq.html">FAQ</a></li></ul></div>
    <div class="footer-col"><h4>Community</h4><ul><li><a href="https://github.com/libcna/cna" target="_blank" rel="noopener">GitHub</a></li><li><a href="https://discord.gg/vrnc4n6DaE" target="_blank" rel="noopener">Discord</a></li><li><a href="{root_prefix}demos.html">Demos</a></li><li><a href="{root_prefix}videos.html">Videos</a></li><li><a href="{root_prefix}contact.html">Contact</a></li></ul></div>
  </div>
  <div class="footer-bottom"><p>CNA is not affiliated with or endorsed by Microsoft Corporation. XNA is a trademark of Microsoft. Licensed under the Microsoft Public License (Ms-PL).</p><div class="footer-links"><a href="https://github.com/libcna/cna/blob/master/LICENSE" target="_blank" rel="noopener">License</a><a href="{root_prefix}contact.html">Contact</a></div></div>
</div></footer>
{tail}</body>
</html>
'''


def auto_toc(body: str) -> str:
    entries = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body, re.S)
    if len(entries) < 3:
        return ""
    lis = "\n".join(f'          <li><a href="#{i}">{t}</a></li>' for i, t in entries)
    return f'''      <nav class="toc" aria-label="Table of contents">
        <h2 class="toc-title">On this page</h2>
        <ul class="toc-list">
{lis}
        </ul>
      </nav>
'''


def new_docs(slug: str, title: str, description: str, body: str, label: str | None, meta_line: str) -> Path:
    rel = f"docs/{slug}.html"
    out = ROOT / rel
    if out.exists():
        raise SystemExit(f"{rel} already exists")
    page_title = f"{title} - CNA Documentation"
    text = head_block(rel, page_title, description, "../", "docs", title, False)
    text += nav_block("../", "documentation.html")
    text += f'''
<main id="main-content">
  <div class="docs-layout">

    <aside class="docs-sidebar">
      <div class="docs-sidebar-title">Documentation</div>
      <ul class="docs-nav-list">
      </ul>
    </aside>

    <nav class="breadcrumb" aria-label="Breadcrumb">
      <ol>
        <li><a href="../index.html">Home</a></li>
        <li><a href="../documentation.html">Docs</a></li>
        <li aria-current="page">{html.escape(title)}</li>
      </ol>
    </nav>
    <article class="docs-content">
      <h1>{html.escape(title)}</h1>
{auto_toc(body)}      <p class="doc-meta">{meta_line}</p>

{body}
    </article>
  </div>
</main>

'''
    text += footer_block("../", "", False)
    out.write_text(text, encoding="utf-8")
    if label:
        print(f"note: add ('{slug}.html', '{label}') to SIDEBAR in scripts/site_nav.py if it is not there yet")
    return out


def new_tutorial(number: int, slug: str, title: str, description: str, body: str, learn: str | None) -> Path:
    rel = f"docs/tutorials/{number:02d}-{slug}.html"
    out = ROOT / rel
    if out.exists():
        raise SystemExit(f"{rel} already exists")
    full_title = f"Tutorial {number}: {title}"
    text = head_block(rel, f"{full_title} - CNA Tutorials", description, "../../", "tutorial", full_title, True)
    text += nav_block("../../", "tutorials.html")
    learn_html = (f'\n  <div class="callout callout--info"><span class="callout-icon">&#8505;</span>'
                  f'<p><strong>What you&rsquo;ll learn:</strong> {learn}</p></div>\n') if learn else ""
    text += f'''<main id="main-content"><div class="tutorial-layout"><div class="docs-main"><article class="docs-content">
  <nav class="breadcrumb" aria-label="Breadcrumb"><ol><li><a href="../../index.html">Home</a></li><li><a href="../../tutorials.html">Tutorials</a></li><li aria-current="page">Tutorial {number}</li></ol></nav>
  <h1>{html.escape(full_title)}</h1>
  <p class="doc-meta">CNA Tutorials &nbsp;&middot;&nbsp; CNA snapshot 009d40f5</p>
{learn_html}
{body}

</article></div></div></main>
'''
    text += footer_block("../../", "../", True)
    out.write_text(text, encoding="utf-8")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("sync")
    d = sub.add_parser("new-docs")
    d.add_argument("--slug", required=True)
    d.add_argument("--title", required=True)
    d.add_argument("--description", required=True)
    d.add_argument("--body", required=True, help="file with the article body HTML (h2 sections with ids)")
    d.add_argument("--label")
    d.add_argument("--meta-line", default="CNA snapshot 009d40f5")
    t = sub.add_parser("new-tutorial")
    t.add_argument("--number", type=int, required=True)
    t.add_argument("--slug", required=True)
    t.add_argument("--title", required=True)
    t.add_argument("--description", required=True)
    t.add_argument("--body", required=True)
    t.add_argument("--learn")
    args = ap.parse_args()

    if args.cmd == "sync":
        print(f"docs sidebars rewritten in {sync_sidebars()} pages")
        return 0
    body = Path(args.body).read_text(encoding="utf-8")
    if args.cmd == "new-docs":
        out = new_docs(args.slug, args.title, args.description, body, args.label, args.meta_line)
        sync_sidebars()
    else:
        out = new_tutorial(args.number, args.slug, args.title, args.description, body, args.learn)
    print(f"created {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
