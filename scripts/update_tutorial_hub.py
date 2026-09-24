#!/usr/bin/env python3
"""Synchronise tutorials.html (the tutorial hub) with docs/tutorials/*.html.

* removes hub entries whose page no longer exists;
* adds entries for tutorials missing from the hub, into the section named by SECTION_OF;
* creates the new sections listed in NEW_SECTIONS (same markup as the existing ones);
* recounts each section, the page totals and rebuilds the JSON-LD ItemList;
* fixes js/tutorial-progress.js so its total is counted from the page instead of hard-coded.

Idempotent: running it twice changes nothing.
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TUT = ROOT / "docs" / "tutorials"
HUB = ROOT / "tutorials.html"

# tutorial number -> section id (existing sections or NEW_SECTIONS ids)
SECTION_OF = {}
for n in range(130, 134): SECTION_OF[n] = "renderers"
for n in range(135, 140): SECTION_OF[n] = "native"
for n in (140, 141): SECTION_OF[n] = "subsystems"
for n in range(145, 149): SECTION_OF[n] = "content-pipeline"
for n in range(150, 155): SECTION_OF[n] = "modern-graphics"
for n in range(155, 158): SECTION_OF[n] = "tooling"
for n in (160, 161): SECTION_OF[n] = "subsystems"

# id, colour, icon, badge, title, description, jump-nav label
NEW_SECTIONS = [
    ("native", "red", "&#128421;", "Expert", "Native Platforms and Builds",
     "Build and run CNA without SDL on native X11, Wayland or Win32, use ALSA audio and CNA's own mixer, configure SDL-free builds, and run CNA in a terminal.",
     "Native Platforms and Builds"),
    ("content-pipeline", "orange", "&#128230;", "Advanced", "Content Pipeline and CNB",
     "Author content with the build-time Content Pipeline, pack it as CNB, interoperate with XNB produced by XNA and MonoGame, and write your own content types.",
     "Content Pipeline and CNB"),
    ("modern-graphics", "orange", "&#10024;", "Advanced", "Modern Graphics",
     "Graphics profiles, build-time shader compilation, image-based lighting and cascaded shadow maps on the renderers that support them.",
     "Modern Graphics"),
    ("tooling", "red", "&#128200;", "Expert", "Diagnostics, Inspector and Tools",
     "Turn on Diagnostics statistics and traces, connect the Inspector to a running game, and use the command-line content and asset tools.",
     "Diagnostics, Inspector and Tools"),
]


def title_of(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    m = re.search(r"<h1>\s*Tutorial\s+\d+\s*:\s*(.*?)</h1>", text, re.S)
    return html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else path.stem


def collect() -> dict[int, tuple[str, str]]:
    out = {}
    for p in sorted(TUT.glob("*.html")):
        m = re.match(r"(\d+)-", p.name)
        if m:
            out[int(m.group(1))] = (p.name, title_of(p))
    return out


def item_html(number: int, file: str, title: str, color: str, indent: str = "        ") -> str:
    return (f'{indent}<a href="docs/tutorials/{file}" class="tut-item tut-item--{color} tut-item--available">\n'
            f'{indent}  <span class="tut-num">{number}</span>\n'
            f'{indent}  <span class="tut-title">{html.escape(title, quote=False)}</span>\n'
            f'{indent}  <span class="tut-time">20 min</span>\n{indent}</a>\n')


def section_bounds(text: str, sid: str) -> tuple[int, int]:
    m = re.search(rf'<section class="section(?: section--alt)?" id="{re.escape(sid)}">', text)
    if m is None:
        raise ValueError(sid)
    i = m.start()
    j = text.index("</section>", i) + len("</section>")
    return i, j


def main() -> int:
    text = HUB.read_text(encoding="utf-8")
    tutorials = collect()

    # 1. drop entries whose page is gone
    def drop(m: re.Match) -> str:
        return m.group(0) if (TUT / m.group(1)).exists() else ""
    text = re.sub(r'[ \t]*<a href="docs/tutorials/([^"]+)" class="tut-item[^"]*">.*?</a>\n(?:\n)?', drop, text, flags=re.S)

    # 2. create new sections after #subsystems
    have = set(re.findall(r'<section class="section(?: section--alt)?" id="([^"]+)"', text))
    _, end_subsystems = section_bounds(text, "subsystems")
    blocks = []
    for idx, (sid, color, icon, badge, title, desc, _) in enumerate(NEW_SECTIONS):
        if sid in have:
            continue
        alt = " section--alt" if idx % 2 == 0 else ""
        blocks.append(f'''

  <!-- ================================================================
       {title}
       ================================================================ -->
  <section class="section{alt}" id="{sid}">
    <div class="container">

      <div class="tut-section-card tut-section-card--{color}">
        <div class="tut-section-icon">{icon}</div>
        <div>
          <span class="diff-badge diff-badge--{color}">{badge}</span>
          <h2>{title}</h2>
          <p>{desc}</p>
          <div class="tut-meta">
            <span class="tut-meta-item">0 tutorials</span>
            <span class="tut-meta-item">&bull;</span>
            <span class="tut-meta-item">&#9200; 20&ndash;30 min each</span>
            <span class="tut-meta-item">&bull;</span>
            <span class="tut-meta-item status-badge status-done">Available now</span>
          </div>
        </div>
      </div>

      <div class="tut-grid">
      </div>

    </div>
  </section>''')
    if blocks:
        text = text[:end_subsystems] + "".join(blocks) + text[end_subsystems:]

    # 3. add missing entries
    present = set(re.findall(r'href="docs/tutorials/([^"]+)"', text))
    for number, (file, title) in sorted(tutorials.items()):
        if file in present or number not in SECTION_OF:
            continue
        sid = SECTION_OF[number]
        i, j = section_bounds(text, sid)
        sec = text[i:j]
        color = re.search(r"tut-item--(\w+)", sec)
        color = color.group(1) if color else next(c for s, c, *_ in NEW_SECTIONS if s == sid)
        k = sec.rindex("      </div>\n\n    </div>\n  </section>") if "      </div>\n\n    </div>\n  </section>" in sec else sec.rindex("</div>")
        # the grid's closing tag is the last "</div>" that closes .tut-grid; find it structurally
        g = sec.index('<div class="tut-grid">')
        gend = sec.index("</div>", sec.rindex("</a>", g) if "</a>" in sec[g:] else g)
        sec = sec[:gend].rstrip(" ") + item_html(number, file, title, color, "        ") + "      " + sec[gend:]
        text = text[:i] + sec + text[j:]
        present.add(file)

    # 4. recount sections
    def recount(m: re.Match) -> str:
        sec = m.group(0)
        n = len(re.findall(r'class="tut-item ', sec))
        return re.sub(r'<span class="tut-meta-item">\d+ tutorials</span>', f'<span class="tut-meta-item">{n} tutorials</span>', sec)
    text = re.sub(r'<section class="section(?: section--alt)?" id="(?:beginner|intermediate|advanced|expert|renderers|content-ext|subsystems|native|content-pipeline|modern-graphics|tooling)">.*?</section>',
                  recount, text, flags=re.S)
    total = len(re.findall(r'class="tut-item ', text))

    # 5. jump nav: extend ranges and add the new sections
    def range_of(sid: str) -> str:
        i, j = section_bounds(text, sid)
        nums = sorted(int(x) for x in re.findall(r'<span class="tut-num">(\d+)</span>', text[i:j]))
        # compress into ranges
        parts, start, prev = [], nums[0], nums[0]
        for n in nums[1:] + [None]:
            if n is None or n != prev + 1:
                parts.append(f"{start:02d}&ndash;{prev:02d}" if start != prev else f"{start:02d}")
                start = n
            prev = n if n is not None else prev
        return ", ".join(parts)
    nav_labels = {"renderers": "Renderers in Depth", "content-ext": "3D Content and CNA Extensions", "subsystems": "Audio, Media, Services and Verification"}
    for sid, label in nav_labels.items():
        text = re.sub(rf'(<a href="#{sid}" class="tut-jump-link tut-jump-link--\w+">&#x2713; {re.escape(label)} &mdash; )[^<]*(</a>)',
                      lambda m: m.group(1) + range_of(sid) + m.group(2), text)
    nav_end = text.index("</nav>", text.index('class="tut-jump-nav"'))
    for sid, color, _i, _b, _t, _d, label in NEW_SECTIONS:
        if f'href="#{sid}"' in text[:nav_end]:
            text = re.sub(rf'(<a href="#{sid}" class="tut-jump-link tut-jump-link--\w+">&#x2713; {re.escape(label)} &mdash; )[^<]*(</a>)',
                          lambda m: m.group(1) + range_of(sid) + m.group(2), text)
            continue
        link = f'\n        <a href="#{sid}" class="tut-jump-link tut-jump-link--{color}">&#x2713; {label} &mdash; {range_of(sid)}</a>'
        nav_end = text.index("</nav>", text.index('class="tut-jump-nav"'))
        text = text[:nav_end].rstrip() + link + text[nav_end:]

    # 6. totals and JSON-LD
    text = re.sub(r"\b\d+ step-by-step CNA tutorials covering everything from your first window to [^\"]*?workflows\.",
                  f"{total} step-by-step CNA tutorials covering everything from your first window to renderer, platform, content pipeline, effects, diagnostics and C API workflows.", text)
    text = re.sub(r"\d+ step-by-step tutorials for C\+\+ game development with CNA", f"{total} step-by-step tutorials for C++ game development with CNA", text)
    text = re.sub(r'"numberOfItems": \d+', f'"numberOfItems": {total}', text)
    text = re.sub(r"From zero to shipping &mdash; \d+ step-by-step guides for C\+\+ game development with CNA[^<]*\.",
                  f"From zero to shipping &mdash; {total} step-by-step guides for C++ game development with CNA, including guides for the native platforms, the Content Pipeline, Diagnostics and the Inspector added since the first tagged pre-release.", text)
    text = re.sub(r"All \d+ tutorials available", f"All {total} tutorials available", text)
    items = []
    for pos, (number, (file, title)) in enumerate(sorted(tutorials.items()), 1):
        items.append(f'    {{ "@type": "ListItem", "position": {pos}, "name": {json.dumps(title, ensure_ascii=False)}, "url": "https://libcna.com/docs/tutorials/{file}" }}')
    ld_i = text.index('"itemListElement": [')
    ld_j = text.index("]", ld_i)
    text = text[:ld_i] + '"itemListElement": [\n' + ",\n".join(items) + "\n  " + text[ld_j:]
    HUB.write_text(text, encoding="utf-8")

    js = ROOT / "js" / "tutorial-progress.js"
    src = js.read_text(encoding="utf-8")
    new = src.replace("const total = 99;", "const total = document.querySelectorAll('.tut-item').length;")
    if new != src:
        js.write_text(new, encoding="utf-8")
    on_disk = len(tutorials)
    print(f"hub entries: {total}; tutorial pages on disk: {on_disk}")
    return 0 if total == on_disk else 1


if __name__ == "__main__":
    sys.exit(main())
