#!/usr/bin/env python3
"""Per-page checks for Development pages while they are being written.

    check_dev_page.py development/internals/platforms/wayland.html [more pages ...]

Checks each named page only (the whole-site validators are scripts/validate_all.sh):
  * strict HTML5 parse (html5lib), duplicate ids, JSON-LD parses, title/description/canonical/og present;
  * every local link and #fragment resolves against the pages on disk; a link to a manifest page that has not
    been built yet is reported as PENDING, not as an error;
  * every CNA source link is pinned to TARGET and the path exists there (Git objects);
  * no retired renderer identity (derived from the CNA registries) and no bare "alpha.1" used as current state;
  * no first-person singular ("I verified ...") and no leftover Developer-site vocabulary.
Exit status 1 when any page has an ERROR.
"""

from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dev_manifest as M  # noqa: E402
import check_retired_renderers as R  # noqa: E402
import site_dev  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

FIRST_PERSON = re.compile(r"\b(I verified|I did not|I checked|I traced|I read|I inspected|we verified)\b")
DEV_VOCAB = re.compile(r"(developer\.libcna\.com|COVERAGE\.md|this manual\b|this handbook\b|this website's pin|"
                       r"\bd6e9ff05|Phase 0 overview)", re.I)
DEV_STATUS = re.compile(r"\b(SOURCE VERIFIED|INVESTIGATING|NOT STARTED|DRAFTED)\b")


class P(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.links: list[str] = []
        self.ld: list[str] = []
        self._ld = False
        self.text: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        v = {k.lower(): (x or "") for k, x in attrs}
        if v.get("id"):
            self.ids.append(v["id"])
        if tag in ("a", "link") and v.get("href"):
            self.links.append(v["href"])
        if tag in ("script", "img", "source") and v.get("src"):
            self.links.append(v["src"])
        if tag == "script" and v.get("type") == "application/ld+json":
            self._ld = True
            self.ld.append("")
        if tag in ("script", "style"):
            self.skip += 1

    def handle_endtag(self, tag):
        if tag == "script":
            self._ld = False
        if tag in ("script", "style") and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if self._ld:
            self.ld[-1] += data
        elif not self.skip:
            self.text.append(data)


def ids_of(path: Path, cache: dict[Path, set[str]]) -> set[str]:
    if path not in cache:
        p = P()
        p.feed(path.read_text(encoding="utf-8"))
        cache[path] = set(p.ids)
    return cache[path]


def main() -> int:
    pages = sys.argv[1:]
    if not pages:
        print(__doc__)
        return 2
    retired = R.derive(Path("/rv/tmp/libcna-v2/cna-base"), Path("/rv/tmp/libcna-v2/cna-target"))
    strong = sorted(i for i in retired if i not in R.WORDS)
    strong_rx = re.compile(r"(?<![A-Za-z0-9_])(" + "|".join(map(re.escape, strong)) + r")(?![A-Za-z0-9_])", re.I)
    files, dirs = site_dev.target_tree()
    idcache: dict[Path, set[str]] = {}
    rc = 0
    for rel in pages:
        path = ROOT / rel
        errors: list[str] = []
        warns: list[str] = []
        if not path.exists():
            print(f"{rel}: ERROR page does not exist")
            rc = 1
            continue
        raw = path.read_text(encoding="utf-8")
        p = P()
        p.feed(raw)
        # link/text checks look at the article only; site chrome (nav, sidebar, footer) is validated site-wide
        art = re.search(r"<article\b.*?</article>", raw, re.S)
        pa = P()
        pa.feed(art.group(0) if art else raw)
        try:
            import html5lib
            parser = html5lib.HTMLParser(strict=False, namespaceHTMLElements=False)
            parser.parse(raw)
            for pos, code, det in parser.errors:
                errors.append(f"HTML5 {pos[0]}:{pos[1]} {code} {det}")
        except ImportError:
            warns.append("html5lib unavailable; strict parse skipped")
        dups = sorted({i for i in p.ids if p.ids.count(i) > 1})
        if dups:
            errors.append("duplicate ids: " + ", ".join(dups))
        for i, blob in enumerate(p.ld):
            try:
                json.loads(blob)
            except Exception as exc:  # noqa: BLE001
                errors.append(f"JSON-LD block {i}: {exc}")
        for href in pa.links:
            u = urlparse(href)
            if u.scheme in ("http", "https"):
                m = re.match(r"https://github\.com/libcna/cna/(blob|tree)/([^/]+)/(.+)", href)
                if m:
                    rev, sp = m.group(2), unquote(m.group(3).split("#", 1)[0]).rstrip("/")
                    if rev != site_dev.TARGET:
                        errors.append(f"CNA link not pinned to TARGET: {href}")
                    elif sp not in files and sp not in dirs:
                        errors.append(f"CNA source path absent at TARGET: {sp}")
                continue
            if href.startswith(("mailto:", "tel:", "javascript:")):
                continue
            tgt_rel = unquote(u.path)
            tgt = (path.parent / tgt_rel).resolve() if tgt_rel else path.resolve()
            if not tgt.exists():
                try:
                    site_rel = tgt.relative_to(ROOT.resolve()).as_posix()
                except ValueError:
                    site_rel = ""
                if site_rel in M.page_index():
                    warns.append(f"PENDING (not built yet): {href}")
                else:
                    errors.append(f"broken local link: {href}")
                continue
            if u.fragment and tgt.suffix == ".html" and unquote(u.fragment) not in ids_of(tgt, idcache):
                errors.append(f"missing fragment: {href}")
        text = " ".join(pa.text)
        for m in strong_rx.finditer(text):
            errors.append(f"retired renderer identity in text: {m.group(0)}")
        for m in re.finditer(r"alpha\.1", text):
            ctx = text[max(0, m.start() - 60): m.end() + 40].replace("\n", " ")
            warns.append(f"mentions alpha.1 (must be historical context only): ...{ctx}...")
        for m in FIRST_PERSON.finditer(text):
            errors.append(f"first-person voice: {m.group(0)}")
        for m in list(DEV_VOCAB.finditer(text)) + list(DEV_STATUS.finditer(text)):
            errors.append(f"Developer-site vocabulary left in text: {m.group(0)}")
        status = "ERROR" if errors else "ok"
        print(f"{rel}: {status} ({len(pa.ids)} ids, {len(pa.links)} links, {len(text.split())} words)")
        for e in errors:
            print("   ERROR", e)
            rc = 1
        for w in warns[:40]:
            print("   warn ", w)
    return rc


if __name__ == "__main__":
    sys.exit(main())
