#!/usr/bin/env python3
"""Check that the site presents the canonical facts in data/current-facts.json consistently.

Each check names a page and a regular expression that must match the page's visible text; the
expected number is formatted from the facts file, so a stale copy of a number fails here even
if every page is internally consistent.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
facts = json.loads((ROOT / "data" / "current-facts.json").read_text(encoding="utf-8"))
F = {k: v["value"] for k, v in facts["facts"].items()}


def n(v) -> str:
    return f"{v:,}" if isinstance(v, int) and v >= 1000 else str(v)


def text(rel: str) -> str:
    soup = BeautifulSoup((ROOT / rel).read_text(encoding="utf-8"), "html.parser")
    for t in soup.find_all(["script", "style"]):
        t.decompose()
    parts = [soup.get_text(" ")]
    # hover titles carry evidence strings
    parts += [t.get("title", "") for t in soup.find_all(True) if t.get("title")]
    return re.sub(r"\s+", " ", " ".join(parts))


def content_text(rel: str, anchor: str | None = None) -> str:
    """Visible page content without navigation chrome; with `anchor`, only that heading's section."""
    soup = BeautifulSoup((ROOT / rel).read_text(encoding="utf-8"), "html.parser")
    main = soup.find("main") or soup.body or soup
    for t in main.find_all(["script", "style", "nav", "aside", "footer"]):
        t.decompose()
    if anchor:
        head = main.find(id=anchor)
        if head is None:
            return ""
        parts = [head.get_text(" ")]
        for sib in head.find_next_siblings():
            if sib.name in ("h1", "h2") or (sib.name == head.name):
                break
            parts.append(sib.get_text(" "))
        return re.sub(r"\s+", " ", " ".join(parts))
    return re.sub(r"\s+", " ", main.get_text(" "))


# Language-binding policy (external_pinned.language_bindings). The canonical section states both sets, the homepage
# leads with the maintained set, and no sentence anywhere presents an archived binding beside a maintained one as if
# it were current (a sentence naming both must say "archived"). Counts of eight/nine bindings or ten languages must
# stand in a historical or archived context.
LB = facts["external_pinned"]["language_bindings"]
MAINTAINED_EXTERNAL = re.compile(r"C#|\bJava\b|\bTypeScript\b")
ARCHIVED_NAMES = re.compile(r"\b(?:" + "|".join(map(re.escape, LB["archived"])) + r")\b|cna-(?:"
                            + "|".join(x.lower() for x in LB["archived"]) + r")\b")
STALE_COUNT = re.compile(r"\b(?:eight|8|nine|9)\s+(?:public\s+|external\s+|language\s+)*bindings\b|\bEight binding projects\b"
                         r"|\b(?:ten|10)\s+(?:programming\s+)?languages\b", re.I)


def binding_policy(pages: list[str]) -> int:
    bad = 0
    page, _ = LB["canonical_page"].split("#")
    maintained = content_text(page, "maintained-bindings")
    archived = content_text(page, "archived-bindings")
    for lang in LB["maintained"]:
        if not re.search(rf"(?<![\w#]){re.escape(lang)}(?![\w#])", maintained):
            print(f"FAIL binding policy: {page}#maintained-bindings does not name {lang}"); bad += 1
    for lang in LB["archived"]:
        if not re.search(rf"\b{re.escape(lang)}\b", archived):
            print(f"FAIL binding policy: {page}#archived-bindings does not name {lang}"); bad += 1
    for needle in ("Archived", "not maintained", "no forward compatibility guarantee", "CNA Lab"):
        if needle not in archived:
            print(f"FAIL binding policy: {page}#archived-bindings lacks '{needle}'"); bad += 1
    lead = "actively maintains " + ", ".join(LB["maintained"][:-1]) + " and " + LB["maintained"][-1] + " bindings"
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    if lead not in content_text("index.html") or 'href="docs/c-api.html#archived-bindings"' not in home:
        print(f"FAIL binding policy: index.html must lead with '{lead}' and link the archived bindings"); bad += 1
    for rel in pages:
        body = content_text(rel)
        for sentence in re.split(r"(?<=[.!?;])\s+", body):
            if MAINTAINED_EXTERNAL.search(sentence) and ARCHIVED_NAMES.search(sentence) and not re.search(r"archiv", sentence, re.I):
                print(f"BINDING? {rel}: archived binding named beside maintained ones without 'archived': {sentence[:160]}"); bad += 1
        for m in STALE_COUNT.finditer(body):
            ctx = body[max(0, m.start() - 160): m.end() + 160]
            if not re.search(r"archiv|during its development|historic", ctx, re.I):
                print(f"BINDING? {rel}: '{m.group(0)}' outside a historical or archived context: {ctx.strip()[:160]}"); bad += 1
    return bad


# (page, regex, description) -- <<name>> placeholders are filled from F
CHECKS = [
    ("index.html", r"\b<<renderer_identities>>\b.{0,40}Renderer identities", "homepage stat: renderer identities"),
    ("index.html", r"\b<<implementation_families>>\b.{0,20}Implementation families", "homepage stat: families"),
    ("index.html", r"\b<<platform_implementations>>\b.{0,20}Platform implementations", "homepage stat: platforms"),
    ("index.html", r"\b<<audio_implementations>>\b.{0,20}Audio platform choices", "homepage stat: audio"),
    ("index.html", r"\b<<static_test_definitions_n>>\b.{0,20}Static test definitions", "homepage stat: test definitions"),
    ("index.html", r"\b<<ci_workflow_files>>\b.{0,20}CI workflow files", "homepage stat: workflows"),
    ("index.html", r"\b<<xna_runtime_members_n>> / <<xna_runtime_members_n>>\b", "homepage stat: XNA members"),
    ("index.html", r"87 / 153", "homepage stat: pinned samples"),
    ("index.html", r"009d40f5", "homepage names the snapshot"),
    ("docs/rendering-backends.html", r"\b<<renderer_identities>> public (renderer )?identities", "renderer page: identity count"),
    ("docs/rendering-backends.html", r"\b<<implementation_families>>\b", "renderer page: family count"),
    ("docs/verification.html", r"\b<<static_test_definitions_n>>\b", "verification page: test definitions"),
    ("docs/verification.html", r"\b<<cpp_test_source_files>>\b", "verification page: test files"),
    ("docs/verification.html", r"\b<<ci_workflow_files>> workflow files", "verification page: workflows"),
    ("docs/platforms.html", r"\b<<platform_implementations>>\b", "platforms page: implementations"),
    ("docs/c-api.html", r"0\.29\.0", "C API page: ABI version"),
    ("docs/c-api.html", r"\b<<c_api_routes_n>>\b", "C API page: route count"),
    ("docs/releases.html", r"009d40f5", "releases page names the snapshot"),
]


def main() -> int:
    F["static_test_definitions_n"] = n(F["static_test_definitions"])
    F["xna_runtime_members_n"] = n(F["xna_runtime_members"])
    F["c_api_routes_n"] = n(F["c_api_routes"])
    bad = 0
    cache: dict[str, str] = {}
    for page, pattern, what in CHECKS:
        if not (ROOT / page).exists():
            print(f"FAIL {what}: {page} missing"); bad += 1; continue
        cache.setdefault(page, text(page))
        rx = re.sub(r"<<([a-z_0-9]+)>>", lambda m: re.escape(str(F[m.group(1)])), pattern)
        if re.search(rx, cache[page], re.S):
            print(f"ok   {what}")
        else:
            print(f"FAIL {what}: /{rx}/ not found in {page}"); bad += 1
    # stale numbers from the alpha.1 audit must not appear as current claims
    stale = [("50 renderer identities", "alpha.1 renderer count"), ("46 implementation families", "alpha.1 family count"),
             ("8,263 static", "alpha.1 test definitions"), ("21 workflow files", "alpha.1 workflow count")]
    for page in [p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*.html") if not ({"audit", "scripts", "build-probe", ".git", "known-issues"} & set(p.relative_to(ROOT).parts))]:  # known-issues pages quote stale numbers of CNA's own documents on purpose
        if page == "docs/releases.html":
            continue  # release history compares alpha.1 with the snapshot on purpose
        body = cache.get(page) or text(page)
        for needle, what in stale:
            for m in re.finditer(re.escape(needle), body):
                ctx = body[max(0, m.start() - 90): m.end() + 60]
                if re.search(r"alpha\.1|earlier|previous|BASE|was |had |historical|\(BASE", ctx, re.I):
                    continue
                print(f"STALE? {page}: '{needle}' ({what}) … {ctx.strip()[:150]}"); bad += 1
    # Phase 2: a whole-registry count written on any page (Development pages included) must equal the canonical fact
    drift = [
        (r"\b(\d+)\s+public\s+(?:renderer\s+)?identities", F["renderer_identities"], "renderer identity count"),
        (r"\b(\d+)\s+(?:renderer\s+)?implementation\s+families", F["implementation_families"], "implementation family count"),
        (r"\b(\d+)\s+(?:CNA_PLATFORM|platform)\s+implementations", F["platform_implementations"], "platform implementation count"),
        (r"\b(\d+)\s+(?:CNA_AUDIO_PLATFORM|audio)\s+implementations", F["audio_implementations"], "audio implementation count"),
        (r"\b(\d+)\s+production\s+modules", 23, "production module count"),
    ]
    for page in [p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*.html") if not ({"audit", "scripts", "build-probe", ".git", "known-issues"} & set(p.relative_to(ROOT).parts))]:  # known-issues pages quote stale numbers of CNA's own documents on purpose
        if page == "docs/releases.html":
            continue
        body = cache.get(page) or text(page)
        for rx, want, what in drift:
            for m in re.finditer(rx, body, re.I):
                if int(m.group(1)) == want:
                    continue
                ctx = body[max(0, m.start() - 90): m.end() + 60]
                if re.search(r"alpha\.1|earlier|previous|BASE|was |had |historical|Developer|compiled|of the 25|spread over", ctx, re.I):
                    continue
                print(f"DRIFT {page}: {what} {m.group(1)} != {want} ... {ctx.strip()[:150]}"); bad += 1
    bad += binding_policy([p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*.html")
                           if not ({"audit", "scripts", "build-probe", ".git", "known-issues"} & set(p.relative_to(ROOT).parts))])
    print(f"fact checks: {bad} problem(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
