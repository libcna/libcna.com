#!/usr/bin/env python3
"""Prism syntax-highlighting scripts: dependency order on every page.

    prism_scripts.py check        # every page: each Prism component after the scripts it extends, and a component
                                  # for every language its code blocks name (no writes)
    prism_scripts.py fix          # insert missing components and restore the order in place; idempotent

A Prism language component extends another language at load time (prism-cpp.min.js calls
Prism.languages.extend("c", ...)), so the component that defines it must have run first; otherwise the
component throws "Cannot set properties of undefined" and its blocks stay unhighlighted. The dependencies are
read from the component files in js/prism/ themselves (their extend("...") calls), so adding a component needs
no edit here. Languages defined by the core bundle (prism.min.js: clike, markup, css, javascript, ...) need no
extra script.

Pages written whole by a generator take the order from scripts/site_nav.py footer_block(); every other page
carries its scripts in its own HTML, which is why `fix` edits pages and validate_site.py runs the check.
"""

from __future__ import annotations

import re
import sys
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRISM_DIR = ROOT / "js" / "prism"
CORE = "prism"
SKIP_PARTS = {"audit", "scripts", "build-probe", ".git"}

TAG_RX = re.compile(r'<script\b[^>]*\bsrc="(?P<src>[^"]*?js/prism/(?P<name>prism(?:-[a-z0-9]+)?)\.min\.js)"[^>]*>\s*</script>')
EXTEND_RX = re.compile(r'\bextend\("([A-Za-z0-9_-]+)"')
CORE_LANG_RX = re.compile(r'\blanguages\.([A-Za-z0-9_]+)=')
LANG_CLASS_RX = re.compile(r'<(?:code|pre)\b[^>]*\bclass="[^"]*\blanguage-([A-Za-z0-9_-]+)')


@lru_cache(maxsize=None)
def core_languages() -> frozenset[str]:
    return frozenset(CORE_LANG_RX.findall((PRISM_DIR / f"{CORE}.min.js").read_text(encoding="utf-8")))


@lru_cache(maxsize=None)
def requires() -> dict[str, tuple[str, ...]]:
    """Component name (e.g. "prism-cpp") -> the component scripts it needs loaded before it."""
    core_langs = core_languages()
    out: dict[str, tuple[str, ...]] = {CORE: ()}
    for path in sorted(PRISM_DIR.glob("prism-*.min.js")):
        name = path.name[: -len(".min.js")]
        lang = name[len("prism-"):]
        deps: list[str] = []
        for target in EXTEND_RX.findall(path.read_text(encoding="utf-8")):
            if target == lang or target in core_langs:
                continue
            dep = f"prism-{target}"
            if not (PRISM_DIR / f"{dep}.min.js").exists():
                raise SystemExit(f"{path.name} extends {target!r}, which neither the core bundle nor a component in js/prism/ defines")
            if dep not in deps:
                deps.append(dep)
        out[name] = tuple(deps)
    return out


def needed(text: str, req: dict[str, tuple[str, ...]]) -> list[str]:
    """Components for the languages the page's code blocks name (language-cpp -> prism-cpp), where js/prism/ has one."""
    langs = dict.fromkeys(LANG_CLASS_RX.findall(text))
    return [f"prism-{lang}" for lang in langs if lang not in core_languages() and f"prism-{lang}" in req]


def problems(text: str, req: dict[str, tuple[str, ...]] | None = None) -> list[str]:
    """Problems of the Prism scripts in one page's HTML: order, and a component missing for a language its code
    blocks name (empty when the page has neither Prism scripts nor such blocks)."""
    req = requires() if req is None else req
    tags = list(TAG_RX.finditer(text))
    names = [m.group("name") for m in tags]
    out: list[str] = [f"a code block names language-{n[len('prism-'):]}, but {n}.min.js is not loaded"
                      for n in needed(text, req) if n not in names]
    if not tags:
        return out
    for name in sorted({n for n in names if names.count(n) > 1}):
        out.append(f"{name}.min.js is loaded {names.count(name)} times")
    if names[0] != CORE:
        out.append(f"{names[0]}.min.js is loaded before the Prism core ({CORE}.min.js)" if CORE in names
                   else f"Prism components are loaded without the Prism core ({CORE}.min.js)")
    modes = {("defer" in m.group(0).split(), "async" in m.group(0).split()) for m in tags}
    if len(modes) > 1:
        out.append("the Prism scripts mix loading modes (defer/async), so they do not run in document order")
    seen: set[str] = set()
    for name in names:
        if name not in req:
            out.append(f"{name}.min.js is not a component in js/prism/")
        for dep in req.get(name, ()):
            if dep not in seen:
                where = "after it" if dep in names else "not at all"
                out.append(f"{name}.min.js needs {dep}.min.js loaded before it ({dep}.min.js is loaded {where})")
        seen.add(name)
    return out


def ordered(names: list[str], req: dict[str, tuple[str, ...]]) -> list[str]:
    """The page's components with missing dependencies added, core first, each dependency right before its first
    dependent, otherwise in the page's own order."""
    out: list[str] = []

    def place(name: str) -> None:
        if name in out:
            return
        for dep in req.get(name, ()):
            place(dep)
        out.append(name)

    place(CORE)
    for name in names:
        place(name)
    return out


def repair(text: str, req: dict[str, tuple[str, ...]] | None = None) -> tuple[str, str | None]:
    """(new text, error). The Prism tags must form one run separated only by whitespace; the run is rebuilt with
    the same tag form, path prefix and separator, so a correct page comes back unchanged."""
    req = requires() if req is None else req
    tags = list(TAG_RX.finditer(text))
    if not problems(text, req):
        return text, None
    if not tags:
        return text, "the page loads no Prism scripts to extend; add them by hand"
    seps = [text[a.end():b.start()] for a, b in zip(tags, tags[1:])]
    if any(s.strip() for s in seps):
        return text, "the Prism scripts are not one contiguous run; fix by hand"
    if len({m.group(0).replace(m.group("src"), "") for m in tags}) > 1:
        return text, "the Prism script tags differ in form; fix by hand"
    if len({m.group("src")[: -len(m.group("name") + ".min.js")] for m in tags}) > 1:
        return text, "the Prism scripts use different path prefixes; fix by hand"
    first = tags[0]
    prefix = first.group("src")[: -len(first.group("name") + ".min.js")]
    form = first.group(0).replace(first.group("src"), "{src}")
    sep = max(set(seps), key=seps.count) if seps else "\n"
    names = list(dict.fromkeys([m.group("name") for m in tags] + needed(text, req)))
    run = sep.join(form.replace("{src}", f"{prefix}{n}.min.js") for n in ordered(names, req))
    return text[: first.start()] + run + text[tags[-1].end():], None


def pages() -> list[Path]:
    return sorted(p for p in ROOT.rglob("*.html") if not (SKIP_PARTS & set(p.relative_to(ROOT).parts)))


def main() -> int:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    if cmd not in ("check", "fix"):
        print(__doc__)
        return 2
    rc = changed = bad = 0
    for path in pages():
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        if cmd == "fix":
            new, err = repair(text)
            if err:
                print(f"ERROR {rel}: {err}")
                rc = 1
            elif new != text:
                path.write_text(new, encoding="utf-8")
                changed += 1
            text = new
        for p in problems(text):
            print(f"ERROR {rel}: {p}")
            bad += 1
            rc = 1
    if cmd == "fix":
        print(f"prism scripts: pages rewritten {changed}; problems left {bad}")
    else:
        print(f"prism scripts: {len(pages())} pages checked; problems {bad}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
