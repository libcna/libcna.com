#!/usr/bin/env python3
"""Scaffold syntax check of every C++ block on the Deep Dive and Development pages against the pinned CNA TARGET headers.

    scripts/check_cpp_blocks.py [--jobs N] [--all]     report-only; nothing is built (g++ -fsyntax-only), sources go to build-probe/cpp-blocks/ and are deleted

Most blocks are fragments (they use variables declared elsewhere), so each one is compiled inside a function whose parameters declare the usual context
(device, spriteBatch, content, game, texture, font ...); a block that starts with a declaration (class, struct, template, a function definition) is compiled at namespace
scope instead, and a block with #include and main() as it stands.  A kitchen-sink header includes every public Microsoft/* header of CNA and every System/* header of the
local sharp-runtime checkout.  Only diagnostics that point at a wrong API are kept (no such member, type or overload, wrong arity or conversion); "not declared" is
expected for a fragment and is dropped.  What survives is a lead, not a verdict: a fragment whose context is unknown to the scaffold reports its own missing context.

Environment: CNA_TARGET_TREE (default /rv/tmp/libcna-v2/cna-target), SHARP_RUNTIME (default ../sharp-runtime), EASY_GL (../easy-gl), META_GL (../meta-gl).
Limits: sibling checkouts are the local ones, not a pinned revision; a block that uses a member of a variable whose type the scaffold does not know is not checked.
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import glob
import html
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = Path(os.environ.get("CNA_TARGET_TREE", "/rv/tmp/libcna-v2/cna-target"))
SHARP = Path(os.environ.get("SHARP_RUNTIME", ROOT.parent / "sharp-runtime"))
EASY = Path(os.environ.get("EASY_GL", ROOT.parent / "easy-gl"))
META = Path(os.environ.get("META_GL", ROOT.parent / "meta-gl"))
WORK = ROOT / "build-probe" / "cpp-blocks"

USINGS = ["Microsoft::Xna::Framework", "Microsoft::Xna::Framework::Graphics", "Microsoft::Xna::Framework::Input", "Microsoft::Xna::Framework::Content",
          "Microsoft::Xna::Framework::Media", "Microsoft::Xna::Framework::Audio", "Microsoft::Xna::Framework::GamerServices", "Microsoft::Xna::Framework::Net",
          "Microsoft::Xna::Framework::Storage", "Microsoft::Xna::Framework::Input::Touch"]
CTX = """void snippet_fn(GraphicsDevice& device, GraphicsDevice& graphicsDevice, SpriteBatch* spriteBatch, SpriteBatch* spriteBatch_, ContentManager& content,
  Game* game, GraphicsDeviceManager& graphics, GraphicsDeviceManager& graphics_, Texture2D& texture, SpriteFont& font, GameTime& gameTime, Vector2& position,
  Vector3& v, Matrix& world, Matrix& view, Matrix& projection, BasicEffect& effect, Model& model, Color& tint, RenderTarget2D* renderTarget)
{"""
KEEP = re.compile(r"(is not a member of|has no member named|no matching function|cannot convert|no type named|too (few|many) arguments|does not name a type|invalid (use|conversion)|is private|is protected|deleted function|no match for|could not convert|expected primary|call of overloaded|no declaration matches|has not been declared)")
DROP = re.compile(r"(was not declared in this scope|use of undeclared|unable to deduce|has incomplete type|redefinition|conflicts with|previous declaration|ambiguous)")
DECL = re.compile(r"^\s*(class|struct|template|namespace|enum|using|static\s|inline\s|extern\s|typedef|#include|[A-Za-z_][\w:<>,\s\*&]*\s+[\w:~]+\([^;]*\)\s*(const)?\s*(noexcept)?\s*\{?\s*$)")
VAR_DECL = re.compile(r"^\s*(const\s+)?[\w:<>]+\s+\w+\s*(=|\(|\{)[^;]*;")


def headers(base: Path, pattern: str, skip: tuple[str, ...] = ()) -> list[str]:
    out = set()
    for p in base.glob(pattern):
        rel = p.as_posix().split("/include/", 1)[-1]
        if not any(s in rel for s in skip):
            out.add(rel)
    return sorted(out)


def kitchen() -> str:
    lines = ["// generated kitchen sink"]
    for rel in headers(TARGET, "modules/**/include/Microsoft/**/*.hpp") + headers(SHARP, "modules/**/include/System/**/*.hpp", ("/detail/", "/Detail/", "Internal")):
        lines += [f'#if __has_include("{rel}")', f'#include "{rel}"', "#endif"]
    return "\n".join(lines) + "\n"


def include_flags() -> list[str]:
    dirs = sorted(glob.glob(str(TARGET / "modules/*/include"))) + sorted(glob.glob(str(TARGET / "modules/renderers/*/include"))) + sorted(glob.glob(str(SHARP / "modules/*/include")))
    dirs += [str(SHARP / "include"), str(EASY / "include"), str(META / "include"), str(SHARP / "vendor")]
    return [f"-I{d}" for d in dirs if os.path.isdir(d)]


def blocks() -> list[tuple[str, str]]:
    out = []
    for f in sorted(glob.glob(str(ROOT / "deep-dives/**/*.html"), recursive=True) + glob.glob(str(ROOT / "development/**/*.html"), recursive=True)):
        text = Path(f).read_text(encoding="utf-8")
        for m in re.finditer(r'<pre\b[^>]*><code class="language-cpp">(.*?)</code></pre>', text, re.S):
            out.append((os.path.relpath(f, ROOT), html.unescape(re.sub(r"<[^>]+>", "", m.group(1)))))
    return out


def compile_one(i: int, code: str, variant: str, flags: list[str]) -> list[str]:
    hoist = [l for l in code.splitlines() if l.startswith("#include")]
    body = "\n".join(l for l in code.splitlines() if not l.startswith("#include"))
    pre = '#include "kitchen.hpp"\n#include <string>\n#include <vector>\n#include <memory>\n#include <cmath>\n#include <cstdint>\n#include <functional>\n#include <optional>\n#include <array>\n'
    pre += "".join(f"using namespace {u};\n" for u in USINGS)
    if variant == "complete":
        src = "\n".join(hoist) + "\n" + pre + "\n" + body
    elif variant == "fn":
        src = "\n".join(hoist) + "\n" + pre + "\n" + CTX + "\n{\n" + body + "\n}}\n"
    else:
        src = "\n".join(hoist) + "\n" + pre + "\n" + body + "\n"
    path = WORK / f"s{i:03d}{variant}.cpp"
    path.write_text(src, encoding="utf-8")
    try:
        r = subprocess.run(["g++", "-std=c++23", "-fsyntax-only", "-fmax-errors=60", "-w", "-fdiagnostics-color=never", *flags, "-DCNA_RENDERER_HEADLESS", "-DSOUND_ENABLED", f"-I{WORK}", str(path)],
                           capture_output=True, text=True)
    finally:
        path.unlink(missing_ok=True)
    return [l for l in r.stderr.splitlines() if " error: " in l]


def job(args: tuple[int, str, str, list[str]]) -> tuple[int, str, list[str]]:
    i, page, code, flags = args
    lines = [l for l in code.splitlines() if l.strip() and not l.strip().startswith("//")]
    first = lines[0] if lines else ""
    if re.search(r"\bint\s+main\s*\(", code) and "#include" in code:
        return i, "complete", compile_one(i, code, "complete", flags)
    if DECL.match(first) and not VAR_DECL.match(first):
        return i, "ns", compile_one(i, code, "ns", flags)
    return i, "fn", compile_one(i, code, "fn", flags)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--all", action="store_true", help="also list blocks with no API-level diagnostic")
    args = ap.parse_args()
    if not (TARGET / "modules").is_dir():
        print(f"TARGET tree not found: {TARGET}", file=sys.stderr)
        return 2
    WORK.mkdir(parents=True, exist_ok=True)
    (WORK / "kitchen.hpp").write_text(kitchen(), encoding="utf-8")
    flags = include_flags()
    bl = blocks()
    flagged = 0
    with cf.ThreadPoolExecutor(max_workers=args.jobs) as ex:
        for i, variant, errs in ex.map(job, [(i, p, c, flags) for i, (p, c) in enumerate(bl)]):
            kept = [e for e in errs if KEEP.search(e) and not DROP.search(e)]
            if kept:
                flagged += 1
            if kept or args.all:
                first = (bl[i][1].strip().splitlines() or [""])[0][:90]
                print(f"#{i} {bl[i][0]} [{variant}] {'FLAGGED' if kept else 'clean'}: {first}")
                for e in kept[:3]:
                    print("     " + re.sub(r"^.*?/s\d+\w+\.cpp", "", e)[:220])
    shutil.rmtree(WORK, ignore_errors=True)
    print(f"check_cpp_blocks: {len(bl)} C++ blocks; {flagged} with an API-level diagnostic (leads to read, not verdicts)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
