#!/usr/bin/env python3
"""Mechanical TARGET cross-check of technical claims on Development pages (a safety net, not a proof).

    check_dev_claims.py [PAGE ...]        # default: every page under development/

For each page it extracts, from <code> text and prose:
  * repository paths (modules/..., cmake/..., tests/..., tools/..., scripts/..., docs/..., .github/...) that must exist at TARGET;
  * CMake preset names in `cmake --preset X`, `--build --preset X`, `ctest --preset X`, checked against CMakePresets.json;
  * CNA_* / SHARP_* build options that occur nowhere in the TARGET CMake files or sources;
  * <code> identifiers whose identifier parts are all unknown to the TARGET source index (renamed/removed/invented symbols).
ERRORs (exit 1): a repository path or a preset that does not exist at TARGET.  WARNs: unknown options / identifiers (review them:
vendored third-party symbols, external repositories and Developer-site tokens are legitimate exceptions).
"""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import site_dev  # noqa: E402

ROOT = site_dev.ROOT
SNAP = Path("/rv/tmp/libcna-v2/cna-target")
WORDS = set((SNAP.parent / "target-words.txt").read_text(encoding="utf-8").split("\n"))
FILES, DIRS = site_dev.target_tree()
PRESETS = json.loads((SNAP / "CMakePresets.json").read_text(encoding="utf-8"))
PRESET_NAMES = {p["name"] for k in ("configurePresets", "buildPresets", "testPresets", "workflowPresets") for p in PRESETS.get(k, [])}
PATH_RE = re.compile(r"^(?:modules|cmake|tests|tools|scripts|docs|\.github|examples|integration|plans|misc|spikes|remediation|modularization|audit)/[A-Za-z0-9_./+\-*]+$")
IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
EXTERNAL_HINTS = ("cna-cs", "cna-java", "cna-python", "cna-ts", "cna-rust", "cna-swift", "cna-go", "cna-ruby", "sharp-runtime",
                  "easy-gl", "meta-gl", "cna-samples", "cna-examples", "xna4-spec")

_cmake_text: str | None = None


def cmake_corpus() -> str:
    global _cmake_text
    if _cmake_text is None:
        parts = []
        for p in list(SNAP.rglob("CMakeLists.txt")) + list((SNAP / "cmake").rglob("*.cmake")) + [SNAP / "CMakePresets.json"]:
            try:
                parts.append(p.read_text(encoding="utf-8", errors="ignore"))
            except OSError:
                pass
        _cmake_text = "\n".join(parts)
    return _cmake_text


def article(text: str) -> str:
    m = re.search(r"<article\b.*?</article>", text, re.S)
    return m.group(0) if m else text


def check(rel: str) -> tuple[list[str], list[str]]:
    raw = (ROOT / rel).read_text(encoding="utf-8")
    art = article(raw)
    codes = [html.unescape(re.sub(r"<[^>]+>", "", c)).strip() for c in re.findall(r"<code[^>]*>(.*?)</code>", art, re.S)]
    prose = html.unescape(re.sub(r"<[^>]+>", " ", art))
    errors: list[str] = []
    warns: list[str] = []
    seen: set[str] = set()
    for c in codes:
        for tok in re.findall(r"[A-Za-z0-9_./+\-*]+", c):
            if PATH_RE.match(tok) and tok not in seen:
                seen.add(tok)
                base = tok.rstrip(".").rstrip("/")
                if rel.startswith("development/internals/bindings/") and rel.endswith(("csharp.html", "java.html", "python.html")) and not base.startswith("modules/"):
                    continue  # paths inside the external binding repositories
                if base in FILES or base in DIRS:
                    continue
                if base.startswith(("scripts/", "audit/", "data/", "css/", "js/")) and (ROOT / base).exists():
                    continue  # a path of this website's own repository (maintenance pages)
                if any(f.endswith("/" + base) or f.startswith(base + "/") or ("/" + base + "/") in f for f in FILES):
                    continue  # module-relative shorthand (e.g. examples/CMakeLists.txt inside a family)
                if "*" in base:
                    pat = re.compile("^" + re.escape(base).replace(r"\*", ".*") + "(/|$)")
                    if not any(pat.match(f) for f in FILES):
                        errors.append(f"path pattern matches nothing at TARGET: {tok}")
                elif base not in FILES and base not in DIRS:
                    errors.append(f"path absent at TARGET: {tok}")
    for m in re.finditer(r"(?:cmake\s+--preset|--build\s+--preset|ctest\s+--preset|--workflow\s+--preset)\s+([A-Za-z0-9_.-]+)", prose):
        if m.group(1) not in PRESET_NAMES:
            errors.append(f"preset does not exist at TARGET: {m.group(1)}")
    corpus = cmake_corpus()
    opts = sorted(set(re.findall(r"\b((?:CNA|SHARP)_[A-Z0-9_]{3,})\b", " ".join(codes) + " " + prose)))
    for o in opts:
        if o not in corpus and o not in WORDS:
            warns.append(f"option-like name not found in CMake or source at TARGET: {o}")
    unseen = []
    for c in dict.fromkeys(codes):
        if len(c) < 4 or " " in c and len(c.split()) > 4:
            continue
        if any(h in c for h in EXTERNAL_HINTS) or c.startswith(("http", "-", "$", "/", "…")) or re.fullmatch(r"[0-9a-fx]{6,40}", c, re.I):
            continue
        parts = [p for p in IDENT.findall(c) if len(p) >= 4 and not p.isdigit()]
        miss = [p for p in parts if p not in WORDS]
        if parts and len(miss) == len(parts):
            unseen.append(c)
    if unseen:
        warns.append(f"{len(unseen)} code token(s) unknown to the TARGET index: " + ", ".join(f"`{u}`" for u in unseen[:14]) + (" …" if len(unseen) > 14 else ""))
    return errors, warns


def main() -> int:
    pages = sys.argv[1:] or sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / "development").rglob("*.html")
                                    if "/reference/" not in p.as_posix())
    rc = 0
    tot_e = tot_w = 0
    for rel in pages:
        e, w = check(rel)
        tot_e += len(e)
        tot_w += len(w)
        if e or w:
            print(f"{rel}: {len(e)} error(s), {len(w)} warning(s)")
            for x in e:
                print("   ERROR", x)
            for x in w:
                print("   warn ", x)
        rc |= 1 if e else 0
    print(f"claims check: {len(pages)} pages, {tot_e} error(s), {tot_w} warning(s)")
    return rc


if __name__ == "__main__":
    sys.exit(main())
