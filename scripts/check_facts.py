#!/usr/bin/env python3
"""Check that the site presents the canonical facts in data/current-facts.json consistently.

Each check names a page and a regular expression that must match the page's visible text; the
expected number is formatted from the facts file, so a stale copy of a number fails here even
if every page is internally consistent.

The facts file is not trusted on its own for the numbers that matter most: the renderer identity, family and GL
profile counts, the platform and audio implementations, the three test-inventory figures, the C ABI version and the
declared route count are recomputed from the CNA Git objects at cnahead (../cna or $CNA_REPO) with the methods the
facts file records. A disagreement between the file and the source fails, and the page checks use the
source-derived values, so a page and the facts file cannot drift together.

Beyond the page list, METRIC_RULES read every public page (Known Issues included) for whole-registry phrasings of
those numbers ("18-identity, 14-family registry", "14 implementation-family directories", "821 of which contain a
counted macro", "five GL profiles", "the two 2D-only renderers", ...) and fail on any value that is not the current
one, unless the number is attributed to an earlier revision in its own clause. A sentence that puts more files with a
counted macro than test files ("821 of 813") fails as impossible. Two wording rules: an evidence callout that says
"at the pinned commit" must name the cnahead commit as the one read (older evidence says "at the stated evidence
commit"), and the C ABI release gate's planned rows are "public C++ declarations", never bare "unmapped symbols" (nor "public
C++ symbols still unmapped" or "missing C exports").

The second review showed that headline rules miss shorthand and inverted subsets, so more is derived from CNA and judged by
what a sentence claims: the compiled-effect sets (identities that can run compiled effects, the always-on family, hence the
identities that never can and those a default configuration refuses), the families that override the Texture2D and the
render-target format classifier (the identities outside them accept only SurfaceFormat::Color), and the examples/ files (all
.cpp, and those named *_test.cpp). EasyGL shorthand ("EasyGL serves five", "five-identity EasyGL...", "two EasyGL profiles other
than A, B and C"), the named test-file metrics, any "other N" larger than the whole, and the compiled-effect and format
complements (concept_findings: polarity and default-configuration wording decide which of 11 / 3 / 13 a count must be) are
rejected when they disagree with the source.

The third review found the registry's classification outside every rule ("18 enumerators from SdlRenderer (0) to Fna3d (17)",
"the three Direct3D identities", "eight Production, seven Supported", "the remaining eight are Native"), so the enum, its
ordinals and the per-identity GraphicsBackendMaturity / GraphicsBackendCategory switches are now read too, with the Direct3D
(DirectX* registry namespace), browser-only (category Web) and non-web EasyGL subsets, and the identities the unbound-texture
test gate pins. Compiled-effect counts now separate the capable set (11 identities, 9 families) from its optioned part (10
identities, 8 families and options), so "FNA3D plus nine optioned families" and "nine opt-in configurations" fail. These are
recognizers for named concepts in the site's usual phrasings, not a parser of English: a number outside these concepts, or a
phrasing none of the patterns knows, is not checked.

The final review (of 56a5ff4) found two registry counts no rule read: "the public renderer identities are a curated set of 18"
(the count after its noun) and "18 CNA_RENDERER_<X> switches" in a configure-order diagram, where the .cmake names on the lines
above had also excused it as a quotation. Both shapes now fail, and only a quotation mark excuses the switch count.
scripts/test_validators.py feeds the reviewers' exact stale sentences through these rules.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parent))
ROOT = Path(__file__).resolve().parent.parent
facts = json.loads((ROOT / "data" / "current-facts.json").read_text(encoding="utf-8"))
F = {k: v["value"] for k, v in facts["facts"].items()}
CNA_REPO = Path(os.environ.get("CNA_REPO") or ROOT.parent / "cna")
TEST_MACRO = r"^\s*(TEST|TEST_F|TEST_P|TYPED_TEST|TYPED_TEST_P)\s*\("
SKIP_PARTS = {"audit", "scripts", "build-probe", ".git"}


def _git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(CNA_REPO), *args], check=True, capture_output=True, text=True).stdout


def derive_from_cna(sha: str) -> dict:
    """The volatile counts, recomputed from the CNA Git objects with the methods data/current-facts.json records."""
    ident = _git("show", f"{sha}:cmake/RendererIdentities.cmake")
    public = re.search(r"set\(CNA_RENDERER_PUBLIC_IDENTITIES(.*?)\)", ident, re.S).group(1).split()
    tree = _git("ls-tree", "-r", "--name-only", sha).splitlines()
    families = {p.split("/")[2] for p in tree if re.match(r"modules/renderers/[^/]+/src/", p)}
    plat = _git("show", f"{sha}:cmake/PlatformSelection.cmake")
    platforms = set(re.search(r"set\(_cna_platforms_available([^)]*)\)", plat).group(1).split())
    for m in re.finditer(r"list\(APPEND _cna_platforms_available([^)]*)\)", plat):
        platforms |= set(m.group(1).split())
    audio = _git("show", f"{sha}:cmake/AudioPlatformSelection.cmake")
    audio_ids = set(re.search(r"set\(_cna_audio_platforms_available([^)]*)\)", audio).group(1).split())
    registry = _git("show", f"{sha}:cmake/RendererRegistry.cmake")
    gl = {m.group(1) for m in re.finditer(r"^\s+([A-Z0-9_]+)\s+EasyGL\|", registry, re.M)}
    tests = [p for p in tree if p.endswith(".cpp") and not p.startswith("third_party/") and re.search(r"(^|/)tests?/", p)]
    per_file = [int(line.rsplit(":", 1)[1]) for line in
                _git("grep", "-cE", TEST_MACRO, sha, "--", "*.cpp", ":!third_party").splitlines() if line.strip()]
    abi = _git("show", f"{sha}:modules/c-api/include/CNA/C/abi.h")
    version = ".".join(re.search(rf"#define CNA_ABI_VERSION_{k} UINT32_C\((\d+)\)", abi).group(1) for k in ("MAJOR", "MINOR", "PATCH"))
    parity = {p.split("/")[2] for p in _git("grep", "-l", r"^\s*cna_register_parity_fixtures(", sha, "--", "modules/renderers").splitlines()
              for p in [p.split(":", 1)[1]]}
    routes = sum(int(line.rsplit(":", 1)[1]) for line in
                 _git("grep", "-c", "^CNA_C_API", sha, "--", "modules/c-api/include/CNA/C/*.h").splitlines() if line.strip())
    # identity -> family directory, through the registry's namespace column (EasyGL -> easygl, SdlGpu -> sdl-gpu)
    key = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())  # noqa: E731
    by_key = {key(d): d for d in families}
    body = re.search(r"set\(_map\n(.*?)\)\n", registry, re.S).group(1)
    toks = re.sub(r"#[^\n]*", "", body).split()
    family_of = {i: by_key[key(e.split("|")[0])] for i, e in zip(toks[0::2], toks[1::2]) if i in public}

    def families_defining(symbol: str) -> set[str]:
        hits = _git("grep", "-lF", symbol, sha, "--", "modules/renderers").splitlines()
        return {p.split(":", 1)[1].split("/")[2] for p in hits} & families

    def identities_of(fams: set[str]) -> int:
        return sum(1 for i in public if family_of[i] in fams)
    # the C++ enum (enumerator count, ordinals) and its name table, then the two classification switches keyed by identity
    rtype = _git("show", f"{sha}:modules/core/include/CNA/GraphicsRendererType.hpp")
    enum = re.sub(r"/\*.*?\*/|//[^\n]*", "", re.search(r"enum class GraphicsRendererType\s*\{(.*?)\}", rtype, re.S).group(1), flags=re.S)
    enumerators = [e.strip() for e in enum.split(",") if e.strip()]
    name_of = dict(re.findall(r'case GraphicsRendererType::(\w+):\s*return "(\w+)";', rtype))
    if sorted(name_of[e] for e in enumerators) != sorted(public):
        raise AttributeError("GraphicsRendererType does not enumerate exactly the public identities")

    def classification(kind: str) -> dict[str, str]:
        """identity -> GraphicsBackendMaturity / GraphicsBackendCategory value, read from the get<kind>() switch"""
        src = _git("show", f"{sha}:modules/core/include/CNA/{kind}.hpp")
        body = src[src.index(f"get{kind}(GraphicsRendererType type)"):]
        out, pending = {}, []
        for m in re.finditer(rf"case GraphicsRendererType::(\w+):|return {kind}::(\w+);", body[:body.index("\n    }\n")]):
            if m.group(1):
                pending.append(m.group(1))
            else:
                out |= {name_of[e]: m.group(2) for e in pending}
                pending = []
        if sorted(out) != sorted(public):
            raise AttributeError(f"get{kind}() does not classify exactly the public identities")
        return out
    category = classification("GraphicsBackendCategory")
    web = {i for i, c in category.items() if c == "Web"}                   # "Only available in a browser/Emscripten build"
    direct3d = {i for i in public if family_of[i].startswith("directx")}   # the registry's DirectX* namespaces
    # the identities the unbound-texture (null-texture) expectations are pinned for: the test's own renderer gate
    null_tex = _git("show", f"{sha}:modules/graphics/tests/Microsoft/Xna/Framework/Graphics/StockEffectNullTextureTests.cpp")
    unbound = {name_of[e.strip()] for e in re.search(r"if \(!CNA_RENDERER_IS\(([^)]*)\)\)", null_tex).group(1).split(",")}
    # compiled effects: a family behind a CNA_<FAMILY>_COMPILED_EFFECTS option (its header answers true only inside that option's
    # #if), plus a family whose renderer answers true with no option at all (FNA3D)
    selection = _git("show", f"{sha}:cmake/RendererSelection.cmake")
    optioned = {by_key[key(o)] for o in re.findall(r"option\(CNA_([A-Z0-9_]+)_COMPILED_EFFECTS\b", selection) if key(o) in by_key}
    always = families_defining("SupportsCompiledEffects() const override { return true; }") - optioned
    compiled = optioned | always
    # format verdicts: families that override the Texture2D / render-target classifier; every other family defers (Color only)
    tex_cls, rt_cls = families_defining("ClassifySurfaceFormatEXT"), families_defining("ClassifyRenderTargetFormatEXT")
    examples = [p for p in tree if not p.startswith("third_party/") and re.search(r"(^|/)examples/.*\.cpp$", p)]
    return {"renderer_identities": len(public), "implementation_families": len(families),
            "platform_implementations": len(platforms), "audio_implementations": len(audio_ids),
            "gl_profiles": len(gl), "cpp_test_source_files": len(tests), "cpp_test_files_with_macros": len(per_file),
            "static_test_definitions": sum(per_file), "c_abi_version": version, "c_api_routes": routes,
            "parity_families": len(parity),
            "compiled_effect_identities": identities_of(compiled), "compiled_effect_families": len(compiled),
            "compiled_effect_always_on_identities": identities_of(always),
            "compiled_effect_optioned_identities": identities_of(optioned), "compiled_effect_optioned_families": len(optioned),
            "compiled_effect_never_identities": len(public) - identities_of(compiled),
            "compiled_effect_default_refusing_identities": len(public) - identities_of(always),
            "renderer_enumerators": len(enumerators), "renderer_last_ordinal": len(enumerators) - 1,
            "renderer_ordinals": {e: i for i, e in enumerate(enumerators)},
            "renderer_maturity": dict(sorted(Counter(classification("GraphicsBackendMaturity").values()).items())),
            "renderer_category": dict(sorted(Counter(category.values()).items())),
            "direct3d_identities": len(direct3d), "web_only_identities": len(web), "non_web_gl_profiles": len(gl - web),
            "unbound_texture_identities": len(unbound), "unbound_texture_families": len({family_of[i] for i in unbound}),
            "format_classifying_families": len(tex_cls), "format_classifying_identities": identities_of(tex_cls),
            "rt_format_classifying_families": len(rt_cls), "rt_format_classifying_identities": identities_of(rt_cls),
            "standalone_pixel_programs": sum(1 for p in examples if p.endswith("_test.cpp")),
            "example_cpp_files": len(examples), "module_example_cpp_files": sum(1 for p in examples if p.startswith("modules/"))}


def source_cross_check(sha: str) -> int:
    """Fail when data/current-facts.json disagrees with the source; afterwards F holds the source-derived values."""
    try:
        derived = derive_from_cna(sha)
    except (OSError, subprocess.CalledProcessError, AttributeError, KeyError, ValueError) as exc:
        print(f"FAIL cannot recompute the facts from CNA {sha[:8]} in {CNA_REPO} (set CNA_REPO): {exc}")
        return 1
    bad = 0
    for key, value in derived.items():
        if key in F and F[key] != value:
            print(f"FAIL data/current-facts.json {key} = {F[key]!r}, but CNA {sha[:8]} gives {value!r}"); bad += 1
        else:
            print(f"ok   {key} = {value!r} (recomputed from CNA {sha[:8]})")
    F.update(derived)
    return bad


# ---------------------------------------------------------------------------------------------
# site-wide metric rules
# ---------------------------------------------------------------------------------------------
WORDS = {w: i for i, w in enumerate("zero one two three four five six seven eight nine ten eleven twelve thirteen "
                                    "fourteen fifteen sixteen seventeen eighteen nineteen twenty".split())}
NUM = r"(?P<n>\d[\d,]*|" + "|".join(WORDS) + r")"


def as_int(text: str) -> int:
    t = text.lower().replace(",", "")
    return WORDS[t] if t in WORDS else int(t)


# (key into the value table, regex with the named group n, minimum n, what it states). A rule fires on every match whose
# number differs from the value, unless the number is attributed to an earlier revision or quoted from a document in
# its own clause (HISTORY / QUOTED). A minimum keeps a whole-registry rule off the many legitimate subset counts ("three
# identities share EasyGL", "Storage has 14 definitions"); the subset phrasings that matter have rules of their own.
_ID = r"(?:public[- ]|selectable[- ]|accepted[- ]|curated[- ]|current[- ])?(?:renderer[- ])?identit(?:y|ies)\b"
_NOT_SUBSET = r"(?<!of the )(?<!other )(?<!remaining )(?<!all but )(?<!more )(?<![\d.])"
METRIC_RULES: list[tuple[str, str, int, str]] = [
    ("renderer_identities", _NOT_SUBSET + r"\b" + NUM + r"[- ](?:(?:public|selectable|accepted|curated|current)[- ](?:renderer[- ])?|renderer[- ])identit(?:y|ies)\b"
     r"(?! matri| values?\b|\s+release)(?![^.;]{0,60}compiled)", 10, "renderer identity count"),
    ("renderer_identities", r"\ball (?:the )?" + NUM + r" (?:renderer )?identities\b(?!\s+(?:that|which|with)\b)", 10, "renderer identity count"),
    ("renderer_identities", r"\b(?:CNA|registry|snapshot|CNA_GRAPHICS_RENDERER)\b[^.;]{0,30}\b(?:has|holds|exposes|accepts|ships|offers|lists|defines)\s+"
     + NUM + r"\s+" + _ID, 0, "renderer identity count"),
    ("renderer_identities", r"\bof the " + NUM + r" (?:public )?(?:renderer )?identities\b", 10, "renderer identity total"),
    ("renderer_identities", r"\b" + NUM + r"[- ](?:member|row|entry)[- ](?:canonical[- ])?identity (?:enum|table)\b", 0, "identity table size"),
    ("renderer_identities", r"\bcanonical " + NUM + r"-entry table\b", 0, "identity table size"),
    ("renderer_identities", r"\bthe " + NUM + r" renderers at a glance\b", 0, "renderer identity count"),
    ("renderer_identities", r"\b" + NUM + r"-identity\b(?=[^.;]{0,30}\bregistry\b)", 0, "renderer identity count"),
    # the count after the noun: "the public renderer identities are a curated set of 18"
    ("renderer_identities", r"\b(?:identities\s+(?:are|form)\s+a\s+(?:curated\s+|closed\s+|fixed\s+)?|curated\s+(?:renderer\s+)?)set\s+of\s+" + NUM + r"\b", 10,
     "renderer identity count"),
    # one CNA_RENDERER_<X> switch per public identity: "+ 18 CNA_RENDERER_<X> switches (exactly one may be ON)"
    ("renderer_switches", r"\b" + NUM + r"\s+(?:per-identity\s+|compatibility\s+)?CNA_RENDERER_(?:<[A-Z]+>|\*)\s+(?:compatibility\s+)?(?:switches|options)\b", 10,
     "per-identity CNA_RENDERER_<X> switch count"),
    ("implementation_families", r"(?<![\d.])\b" + NUM + r"[- ](?:renderer[- ]|physical[- ]|implementation[- ])+famil(?:y|ies)\b", 10, "implementation family count"),
    ("implementation_families", r"\b" + NUM + r"[- ]family registry\b", 0, "implementation family count"),
    ("implementation_families", r"\b" + NUM + r" families implementing\b", 0, "implementation family count"),
    ("implementation_families", r"\bfamily \(1 of " + NUM + r"\)", 0, "implementation family count"),
    ("implementation_families", r"(?<!of the )\b\d+ (?:public )?(?:renderer )?identities (?:across|over|in) " + NUM + r" (?:implementation |renderer )?families\b", 0,
     "implementation family count"),
    ("gl_profiles", r"\b" + NUM + r"[- ]GL(?:[- ]profile)?[- ](?:profiles?|renderer identities|identities|renderers)\b", 0, "EasyGL profile count"),
    ("gl_profiles", r"\b" + NUM + r" profiles, one EasyGL\b", 0, "EasyGL profile count"),
    ("gl_profiles", r"\bEasyGL\b[^.;]{0,60}?\b(?:serves|supplies|carries|implements|covers|has)\s+" + NUM + r"\s+(?:public\s+)?(?:renderer\s+)?identities\b", 0,
     "EasyGL profile count"),
    ("gl_profiles", r"(?<!WebGL )(?<!OpenGL )(?<!ES )(?<!GL )\b" + NUM + r"\s+(?:public\s+|renderer\s+|current\s+)*(?:identities|renderers|backends|profiles)\s+(?:share|sharing)\b"
     r"[^.;]{0,40}?\b(?:EasyGL|one (?:CNA )?implementation)", 0, "EasyGL profile count"),
    ("gl_profiles", r"\bEasyGL (?:family )?\(" + NUM + r"(?: public)? identities", 0, "EasyGL profile count"),
    # shorthand the rules above missed: "EasyGL serves five," / "EasyGL owns five renderer identities", "the five-identity
    # EasyGLRendererDescriptor.cpp", "five EasyGL profiles", "five identities are served by EasyGL", "EasyGL family (5)"
    ("gl_profiles", r"\bEasyGL\b[^.;]{0,40}?\b(?:serves|supplies|carries|implements|covers|has|owns|provides|backs|hosts|exposes|handles)\s+(?:all\s+)?"
     + NUM + r"(?=\s*(?:[,.;:)]|$|\band\b|\((?!\s*\d)|(?:public\s+|renderer\s+|GL[- ]profile\s+|GL\s+)*(?:identit|profiles?\b)))", 0, "EasyGL identity count"),
    ("gl_profiles", r"\b" + NUM + r"[- ](?:identity|profile|GL-profile)\s+(?:<code>)?EasyGL", 0, "EasyGL identity count"),
    ("gl_profiles", r"(?<!between )\b" + NUM + r"\s+EasyGL\s+(?:public\s+)?(?:renderer\s+)?(?:profiles|identities|renderers|backends)\b(?!\s+(?:other than|besides|except|that|which)\b)", 0,
     "EasyGL identity count"),
    ("gl_profiles", r"\b" + NUM + r"\s+(?:public\s+)?(?:renderer\s+)?identities\s+(?:are served by|use|map to|belong to|come from|run on)\s+(?:the\s+)?(?:one\s+)?EasyGL", 0,
     "EasyGL identity count"),
    ("gl_profiles", r"\bEasyGL(?: family)?\s*\(\s*" + NUM + r"\s*\)", 0, "EasyGL identity count"),
    ("gl_profiles", r"\bEasyGL(?: family)?\s*[:\u2014\u2013]\s*" + NUM + r"\s+(?:public\s+)?(?:renderer\s+)?(?:identities|profiles)\b", 0, "EasyGL identity count"),
    ("gl_profiles", r"\bEasyGL\b[^.;]{0,30}?\b(?:is\s+)?(?:shared|used|selected|served)\s+(?:between|among|by)\s+(?:all\s+)?(?:the\s+)?" + NUM
     + r"(?=\s*(?:[,.;:)]|$|\band\b|(?:public\s+|renderer\s+|current\s+)*(?:identit|renderers?\b|backends?\b|profiles?\b)))", 0, "EasyGL identity count"),
    # the two GL identities that are not WEBGL2 ("the three non-web EasyGL profiles", "three native GL-profile identities")
    ("non_web_gl_profiles", r"\b" + NUM + r"\s+(?:non-web|non-browser|native|desktop(?:/mobile)?)\s+(?:EasyGL\s+|GL[- ]profile\s+|GL\s+|OpenGL\s+)"
     r"(?:profiles|identities|renderers|profile identities)\b", 0, "non-web EasyGL identity count"),
    ("parity_families", r"\bparity\b[^.;]{0,80}?\b(?:registered for|on|for|covers?|covering|span|spans) (?:the )?" + NUM + r" (?:renderer )?families\b", 0, "parity-fixture family count"),
    ("parity_families", r"\bregistered for (?:the )?" + NUM + r" renderer families\b", 0, "parity-fixture family count"),
    ("parity_families", r"\b" + NUM + r" (?:renderer )?families call cna_register_parity_fixtures\b", 0, "parity-fixture family count"),
    ("compiled_effect_identities", r"(?<!other )(?<!remaining )\b" + NUM + r" (?:of the \d+ )?(?:renderer )?identities (?:that )?(?:support|can run|run) compiled\b", 0,
     "compiled-effect identity count"),
    ("compiled_effect_identities", r"(?<!refusals: )\bcompiled(?:(?!false|unsupported|refus|\bnot\b)[^.;]){0,60}?\b" + NUM + r" of the \d+ (?:renderer )?identities\b", 0,
     "compiled-effect identity count"),
    ("compiled_effect_more", r"\b" + NUM + r" more (?:renderer )?identities\b", 0, "compiled-effect identities besides FNA3D"),
    ("two_d_only_renderers", r"\b" + NUM + r" (?:deliberately )?2D-only (?:renderers|identities|families)\b", 0, "2D-only identity count"),
    ("two_d_only_renderers", r"\b" + NUM + r" (?:renderer )?identit(?:y|ies) (?:is|are) (?:deliberately )?2D-only\b", 0, "2D-only identity count"),
    ("two_d_only_renderers", r"\b" + NUM + r" (?:shipped |current |public |CNA )?(?:renderers|renderer identities|identities|families) (?:is |are )?(?:deliberately |intentionally |still )?"
     r"(?:2D-only|2D only)\b", 0, "2D-only identity count"),
    ("platform_implementations", r"\b" + NUM + r" (?:CNA_PLATFORM |platform )implementations\b", 0, "platform implementation count"),
    ("platform_implementations", r"\bCNA_PLATFORM\b (?:now )?offers " + NUM + r" implementations\b", 0, "platform implementation count"),
    ("audio_implementations", r"\b" + NUM + r" (?:CNA_AUDIO_PLATFORM |audio )implementations\b", 0, "audio implementation count"),
    ("cpp_test_source_files", r"\b" + NUM + r" (?:CNA-owned )?C\+\+ test (?:source )?files\b", 500, "C++ test source file count"),
    ("cpp_test_source_files", r"\btest figures \(" + NUM + r" files\b", 0, "C++ test source file count"),
    ("cpp_test_source_files", r"\b" + NUM + r" (?:CNA-owned )?test source files\b", 500, "C++ test source file count"),
    ("cpp_test_files_with_macros", r"\b" + NUM + r" (?:of (?:the files|the test files|which|them) |(?:test )?files )?(?:contain|contains|with) (?:at least one|a counted|such a|counted"
     r"|an? (?:GoogleTest(?:-family)? |counted |test )macro|GoogleTest(?:-family)? macros?)\b", 500, "test files containing a counted macro"),
    # named metrics that must not borrow a neighbouring count: files literally named *_test.cpp (all under examples/), standalone
    # pixel programs (the same set), and every .cpp under an examples/ directory (878 under modules/, 879 with the loose demo)
    ("standalone_pixel_programs", r"\b" + NUM + r"\s+(?:<code>)?\*_test\.cpp\b", 0, "files named *_test.cpp"),
    # the name decides the count, whatever adjectives precede the noun: "879 test files named *_test.cpp" is the *_test.cpp set
    ("standalone_pixel_programs", r"\b" + NUM + r"\s+(?:of\s+them\s+)?(?:(?:[\w.+/*-]+\s+){0,3}?(?:files|programs|sources)\s+)?(?:are\s+)?(?:named|called)\s+(?:<code>)?\*?_test\.cpp", 0,
     "files named *_test.cpp"),
    ("standalone_pixel_programs", r"\b" + NUM + r"\s+(?:[\w.+/*-]+\s+){0,3}?(?:files|programs|sources)\s+whose\s+names?\s+ends?\s+(?:in|with)\s+_test\.cpp", 0, "files named *_test.cpp"),
    ("standalone_pixel_programs", r"\b" + NUM + r"\s+standalone\s+(?:example\s+)?(?:pixel\s+)?(?:or\s+contract\s+)?programs\b", 0, "standalone examples/**/*_test.cpp programs"),
    ("standalone_pixel_programs", r"\*_test\.cpp\b[^.;]{0,80}?\(\s*" + NUM + r"\s+(?:across|in|under|throughout)\b", 0, "files named *_test.cpp"),
    ("example_cpp_files", r"\b" + NUM + r"\s+\.cpp\s+files\b(?=[^.;]{0,60}\bexamples?\b)", 0, ".cpp files under examples/ directories"),
    # a complement larger than the whole: "the other 15 renderer identities" (14 in all), "the other 20 families" (12 in all)
    ("complement_identities", r"\b(?:other|remaining)\s+" + NUM + r"\s+(?:public\s+|selectable\s+)?(?:renderer\s+)?identities\b", 0, "a complement of the renderer identities"),
    ("complement_identities", r"\b" + NUM + r"\s+other\s+(?:public\s+)?(?:renderer\s+)?identities\b", 0, "a complement of the renderer identities"),
    ("complement_families", r"\b(?:other|remaining)\s+" + NUM + r"\s+(?:renderer\s+|implementation\s+)?families\b", 0, "a complement of the implementation families"),
    ("complement_families", r"\b" + NUM + r"\s+other\s+(?:renderer\s+|implementation\s+)?families\b", 0, "a complement of the implementation families"),
    ("static_test_definitions", r"(?<!with )(?<!has )(?<!holds )\b" + NUM + r" (?:static(?:ally)?(?: declared| discoverable)? (?:GoogleTest-family )?definitions|static test definitions)\b",
     1000, "static GoogleTest-family definitions (whole tree)"),
    ("production_modules", r"\b" + NUM + r"\s+production\s+modules\b", 0, "production module count"),
    # "a renderer name outside the 18" (a sentence about renderer names; see REQUIRES)
    ("renderer_names_outside", r"\bnames?\s+(?:that\s+is\s+|is\s+)?(?:outside|beyond|not\s+(?:one\s+)?of)\s+(?:the\s+)?" + NUM + r"\b", 0,
     "renderer identity count"),
    # the C++ enum behind the identities: "18 enumerators from SdlRenderer (0) to Fna3d (17)", "ends at ordinal 17"
    ("renderer_enumerators", r"\bGraphicsRendererType\b[^.;]{0,60}?\b" + NUM + r"\s+(?:enumerators|members|entries)\b", 0, "GraphicsRendererType enumerator count"),
    ("renderer_enumerators", r"\bGraphicsRendererType\b[^.;]{0,40}?\b(?:enumerates|has|holds|lists|declares|defines)\s+" + NUM
     + r"\s+(?:public\s+|renderer\s+)*(?:identities|enumerators|members|entries)\b", 0, "GraphicsRendererType enumerator count"),
    ("renderer_enumerators", r"\b" + NUM + r"[- ](?:enumerator|member|entry)\s+GraphicsRendererType\b", 0, "GraphicsRendererType enumerator count"),
    ("renderer_enumerators", r"\b" + NUM + r"\s+enumerators\b(?=[^.;]{0,60}\b(?:SdlRenderer|Fna3d)\b)", 0, "GraphicsRendererType enumerator count"),
    ("renderer_enumerators", r"\brenderer[- ](?:type\s+)?enum(?:eration)?\b[^.;]{0,40}?\b" + NUM + r"\s+(?:enumerators|members|entries)\b", 0, "GraphicsRendererType enumerator count"),
    ("renderer_last_ordinal", r"\bends?\s+at\s+(?:the\s+)?(?:C\+\+\s+)?ordinal\s+" + NUM, 0, "last GraphicsRendererType ordinal"),
    ("renderer_last_ordinal", r"\b(?:last|final|highest|maximum|largest|top)\s+(?:C\+\+\s+)?(?:enumerator['\u2019]s\s+)?ordinal\s+(?:is\s+|of\s+|=\s*)?" + NUM, 0,
     "last GraphicsRendererType ordinal"),
    ("renderer_last_ordinal", r"\bordinals?\s+(?:(?:run|go|range|span|count)s?\s+)?(?:from\s+)?0\s*(?:\u2013|-|\u2026|\.\.\.?|to|through)\s*" + NUM + r"\b", 0, "last GraphicsRendererType ordinal"),
    # subsets the registry fixes: the Direct3D identities (one is a legitimate subset reference, hence the minimum of 2), the
    # browser-only (Web category) identity; "the three Direct3D identities" kept the retired DIRECTX12 alive without naming it
    ("direct3d_identities", r"(?<![\d.])\b" + NUM + r"\s+(?:(?:public|current|shipped|selectable|native|Windows-only)\s+)?(?:Direct3D|DirectX|D3D)\s+(?:renderer\s+)?"
     r"(?:identities|identity|renderers|backends|families)\b", 2, "Direct3D renderer identity count"),
    ("web_only_identities", r"\b" + NUM + r"\s+(?:browser|web)[- ]only\s+(?:renderer\s+)?(?:identities|identity|renderers?|backends?|profiles?)\b", 0,
     "browser-only (Web category) identity count"),
    ("web_only_identities", r"\b" + NUM + r"\s+(?:renderer\s+)?(?:identities|renderers)\s+(?:are|is)\s+(?:browser|web)[- ]only\b", 0, "browser-only (Web category) identity count"),
]
_MACRO_RULE = next(r[1] for r in METRIC_RULES if r[0] == "cpp_test_files_with_macros")
# the number belongs to an earlier revision, in its own clause, before it
HISTORY = re.compile(r"alpha\.1|b0e97bb1|009d40f5|d6e9ff05|1bb2145d|\bearlier\b|\bprevious(?:ly)?\b|\bbefore\b|\bwas\b|\bwere\b|"
                     r"\bhad\b|\bfrom\b|historical|\bresearch\b|audited (?:commit|revision)|\bused to\b|\b(?:back|until|by) then\b|\bthen-current\b|\bonce\b|"
                     r"\bremoved\b|\brestored\b|\bretired\b|\bnarrowed\b|\bshipped\b|\btagged\b", re.I)
# the number is quoted from a document (typically one of CNA's own stale files, the subject of a Known Issue): a quotation
# mark, a reporting verb or a file name earlier in the same sentence
QUOTED = re.compile(r"[\u201c\"]|\b(?:says?|states?|reads?|pins?|claims?|speaks? of|describes?|quotes?|Doxygen|comment|header)\b|"
                    r"\.(?:md|cmake|json|h|hpp|py)\b|CHANGELOG", re.I)
QUOTED_MARK = re.compile(r"[\u201c\"]|\.(?:md|cmake|json|h|hpp|py)\b|CHANGELOG")
# a configure-order diagram names a .cmake file on every line, so for the switch count only a quotation mark is a quote
QUOTE_ONLY = re.compile(r"[\u201c\"]")
# a rule that applies only in a sentence of a given subject
REQUIRES = {"compiled_effect_more": re.compile(r"compil|COMPILED|opt-in build option|Effect Framework", re.I),
            "renderer_names_outside": re.compile(r"renderer|CNA_GRAPHICS_RENDERER|identit", re.I),
            "renderer_last_ordinal": re.compile(r"GraphicsRendererType|\brenderer identit|\bFna3d\b|\bSdlRenderer\b")}
# rules whose own wording contains "from" ("ordinals from 0 to 13"): only an explicit earlier revision excuses the number
NARROW_HISTORY = {"renderer_enumerators", "renderer_last_ordinal"}
# a sentence about compiled effects may name the compiled-effect subset
SUBSET = {"implementation_families": ("compiled", "implementation_families_subset"),
          "renderer_identities": ("compiled", "compiled_effect_identities")}


def _clause_before(body: str, start: int) -> str:
    before = body[max(0, start - 90):start]
    cut = max((m.end() for m in re.finditer(r"[.;\u2014]\s|:\s", before)), default=0)
    return before[cut:]


def _sentence(body: str, start: int, end: int) -> str:
    a = max((m.end() for m in re.finditer(r"[.!?](?:\s|$)", body[max(0, start - 400):start])), default=0)
    a += max(0, start - 400)
    b = re.search(r"[.!?](?:\s|$)", body[end:end + 400])
    return body[a: end + (b.start() if b else 400)]


def metric_findings(body: str, values: dict) -> list[tuple[str, str]]:
    """(message, matched text) for every stale or impossible metric in one block of visible text (a paragraph, cell,
    item or heading)."""
    found: list[tuple[str, str]] = []
    for key, rx, minimum, what in METRIC_RULES:
        want = values.get(key)
        if want is None:
            continue
        for m in re.finditer(rx, body, re.I):
            got = as_int(m.group("n"))
            if key.startswith("complement_"):
                if got < want:                              # want is the whole; any smaller complement is arithmetic for the page
                    continue
            elif (got in want if isinstance(want, (set, frozenset)) else got == want) or got < minimum:
                continue
            sentence = _sentence(body, m.start(), m.end())
            # a reporting verb cannot excuse impossible arithmetic
            quoted = QUOTED_MARK if key.startswith("complement_") else QUOTE_ONLY if key == "renderer_switches" else QUOTED
            if (REVISION if key in NARROW_HISTORY else HISTORY).search(_clause_before(body, m.start("n"))) or quoted.search(sentence[:max(0, sentence.find(m.group(0)))]):
                continue
            if key in REQUIRES and not REQUIRES[key].search(sentence):
                continue
            if key in SUBSET and re.search(SUBSET[key][0], sentence, re.I) and got == values.get(SUBSET[key][1]):
                continue
            claim = f"{what} {got} is not smaller than the whole ({want})" if key.startswith("complement_") else f"{what} {got} != {want}"
            found.append((f"{claim}: \u2026{body[max(0, m.start() - 90): m.end() + 50].strip()}\u2026", m.group(0)))
    # impossible combinations: more files with a counted macro than test files, or "X of Y" with X > Y
    for m in re.finditer(r"\b(\d[\d,]*) C\+\+ test (?:source )?files\b", body):
        sentence = _sentence(body, m.start(), m.end())
        total = as_int(m.group(1))
        for k in re.finditer(_MACRO_RULE, sentence, re.I):
            if as_int(k.group("n")) > total:
                found.append((f"impossible: {k.group('n')} files with a counted macro out of {total} test files: \u2026{sentence.strip()[:200]}\u2026", k.group(0)))
    for m in re.finditer(r"(?<![\d.\u2212-])\b(\d[\d,]*) (?:of|out of) (?:the )?(\d[\d,]*)\b(?![-.\d]| ?%)", body):
        a, b = as_int(m.group(1)), as_int(m.group(2))
        if a > b >= 10 and not HISTORY.search(_clause_before(body, m.start())):
            found.append((f"impossible ratio {m.group(1)} of {m.group(2)}: \u2026{body[max(0, m.start() - 80): m.end() + 40].strip()}\u2026", m.group(0)))
    return found + concept_findings(body, values)


# ---------------------------------------------------------------------------------------------
# concept rules: subset and complement counts of the concepts the site states again and again
# ---------------------------------------------------------------------------------------------
# Compiled effects. Several numbers are true at once and a sentence must use the one its own wording claims: identities that
# CAN run compiled effects (11, in 9 families), of which 10 (in 8 families, one CNA_<FAMILY>_COMPILED_EFFECTS option each) need
# a default-OFF option and 1 (FNA3D) has the path always on; identities that never can (3); identities that refuse them in a
# DEFAULT configuration (13). A count is judged by the clause it stands in: a negative predicate ("refused on", "cannot",
# "without", "report false") wants the incapable count, or the default-refusal count only when the sentence names the default
# configuration; a positive one wants the capable count, or the optioned count (10 identities, 8 families or options) when it
# says "other"/"more", qualifies its noun ("optioned", "opt-in", "default-OFF") or puts the count behind the options ("ten
# identities behind default-OFF options", "FNA3D plus eight optioned families"). The unit decides the number: "renderers" and
# "backends" count identities, "families" families, "options"/"configurations" the eight options, and a bare "nine opt-in" /
# "nine behind ..." must be one of the optioned counts.
# Format classification. Eight families (10 identities) classify the Texture2D formats themselves and seven (9 identities)
# the render-target formats; every other identity defers, which means SurfaceFormat::Color only. "The other N identities"
# (or "the remaining N", "N Color-only renderers") accept only Color must be the complement: 4 for textures, 5 where the
# sentence is about render targets.
# Unbound textures. StockEffectNullTextureTests.cpp pins its unbound-texture expectations for the identities its
# CNA_RENDERER_IS gate names (8, in 7 families): "renderers"/"identities" there must be 8 and "families" 7.
COMPILED_CTX = re.compile(r"compiled[- ](?:XNA |XNA/FNA )?effects?|CompiledEffects|COMPILED_EFFECTS|Effect Framework|\.fxb\b|effect bytecode", re.I)
FORMAT_CTX = re.compile(r"SurfaceFormat::Color\b|\bColor[- ]only\b|\bonly\s+(?:SurfaceFormat::)?Color\b|\bclassif\w*\b[^.;]{0,40}\bformats?\b|"
                        r"\bpromot\w*\b[^.;]{0,30}\bformats?\b|format[- ]classif", re.I)
RT_CTX = re.compile(r"render[- ]targets?\b|RenderTarget", re.I)
UNBOUND_CTX = re.compile(r"unbound[- ]textures?|null[- ]textures?|StockEffectNullTexture", re.I)
DEFAULT_CONFIG = re.compile(r"\bdefault\s+(?:configur\w*|build|CMake)\b|\bby default\b|\bin a default\b|\bdefault-configured\b|"
                            r"\boptions?\s+defaults?\s+to\s+OFF\b|\bdefaults?\s+to\s+OFF\b", re.I)
NEGATIVE = re.compile(r"\b(?:cannot|can't|can\s?not|never|do not|don't|does not|doesn't|lacks?|without|refus\w*|unsupported|not supported|"
                      r"incapable|throws?|false|unavailable|not available|except)\b", re.I)
_OTHER = r"(?P<other>(?:the\s+)?(?:other|remaining)\s+)?"
_MORE = r"(?:\s+(?P<more>other|more))?"
_QUAL = r"opt-in|optioned|option-gated|default-OFF|default-off"
IDENT_COUNT = re.compile(r"(?<![\d.])" + _OTHER + r"\b" + NUM + _MORE + r"(?:\s+of\s+(?:the\s+)?\d+)?\s+(?P<q>(?:(?:public|selectable|capable|supported|supporting|"
                         r"shipped|current|renderer|further|additional|" + _QUAL + r")\s+)*)(?:identities|renderers|backends)\b", re.I)
FAMILY_COUNT = re.compile(r"(?<![\d.])" + _OTHER + r"\b" + NUM + _MORE + r"\s+(?P<q>(?:(?:renderer|implementation|compiled-effect|capable|further|additional|"
                          + _QUAL + r")\s+)*)families\b", re.I)
OPTION_COUNT = re.compile(r"(?<![\d.])\b" + NUM + r"(?:\s+(?:more|other|further))?\s+(?P<q>(?:(?:opt-in|optional|default-OFF|default-off|CMake|build|compiled-effect|"
                          r"family|per-family|CNA_\*_COMPILED_EFFECTS)\s+)*)(?:configurations|options|switches)\b", re.I)
# "FNA3D always, nine opt-in" / "nine behind opt-in build options": a count with no noun, which must be an optioned count
BARE_OPTIONED = re.compile(r"(?<![\w.-])" + NUM + r"(?:\s+(?:more|other))?\s+(?:opt-in\b(?!\s+(?:[\w*-]+\s+){0,3}?(?:identit|renderer|famil|backend|configuration|option|build|switch))"
                           r"|behind\b)", re.I)
OPT_AFTER = re.compile(r"^\s*\)?\s*(?:(?:are|is)\s+)?(?:behind|through|via|with|gated\s+by|provided\s+by|controlled\s+by|enabled\s+by|needs?|requires?)\b[^.;]*?"
                       r"\b(?:opt-in|optioned|options?|default-OFF|default-off|switch(?:es)?)\b", re.I)
OPT_BEFORE = re.compile(r"\bFNA3D\b(?:\s+\(?always\)?)?\s*(?:plus|and|\+)\s+(?:the\s+)?$|\b(?:besides|beyond|apart\s+from|other\s+than|in\s+addition\s+to)\s+FNA3D\s*,?\s*(?:the\s+)?$", re.I)
# "eight optioned families (ten identities)", "optioned on eight families (ten identities)": the identities of an optioned family count
OPT_FAMILY_PAREN = re.compile(r"\b(?:more|other|further|" + _QUAL + r")\b[^.;()]{0,40}\bfamilies\s*\(\s*$", re.I)
# a clause that refers back to the compiled-effect route of the previous sentence ("Ten renderers implement it")
PRONOUN_PRED = re.compile(r"\b(?:implement|support|run|provide|offer|expose|execute|accept)s?\s+(?:it|them)\b", re.I)
# "14 public renderer identities in 12 implementation families": the registry as a whole, not a compiled-effect or format subset
REGISTRY_PHRASE = re.compile(r"\s+(?:in|over|across)\s+" + NUM.replace("?P<n>", "?:") + r"\s+(?:renderer\s+|implementation\s+)?families\b", re.I)
COLOR_ONLY_COUNT = re.compile(r"\b" + NUM + r"\s+(?:shipped\s+|current\s+|public\s+)?(?:renderers|identities|renderer identities|families)\s+(?:are|stay|remain)\s+"
                              r"(?:SurfaceFormat::)?Color[- ]only\b", re.I)
COLOR_ONLY_NOUN = re.compile(r"\b" + NUM + r"\s+(?:(?:shipped|current|public)\s+)?(?:SurfaceFormat::)?Color[- ]only\s+(?:renderers|identities|renderer identities|backends)\b", re.I)
# "the remaining thirteen accept Color only", "and four accept only Color": a complement with no noun
FORMAT_BARE = [re.compile(r"\b(?:the\s+)?(?:other|remaining)\s+" + NUM + r"(?=\s+(?:accept|support|take|allow|are|stay|remain|keep)s?\b)", re.I),
               re.compile(r"(?:^|[;:(]\s*|,\s+|\band\s+)" + NUM + r"(?=\s+(?:accept|support|take|allow)s?\s+only\b)", re.I)]
EASYGL_CTX = re.compile(r"EasyGL|\bGL\b|OPENGL", re.I)


def _clauses(sentence: str) -> list[tuple[int, str]]:
    """(offset, text) of the semicolon/colon/dash clauses of one sentence."""
    out, pos = [], 0
    for m in re.finditer(r";\s|:\s|\s\u2014\s", sentence):
        out.append((pos, sentence[pos:m.start()]))
        pos = m.end()
    return out + [(pos, sentence[pos:])]


def _polarity(sentence: str, start: int, end: int) -> bool:
    """True when the sentence says the counted group does NOT have the feature. The predicate after the count stops at a
    parenthesis, comma or clause break (so "11 of the 14 identities (SDL_RENDERER ... do not)" stays positive); the words
    before it count from the last parenthesis or comma ("unsupported on 13 of the 14", "refused on the 11", "Named
    refusals: compiled effects on 3 of the 14")."""
    after = re.split(r"[(,;]|\s\u2014\s", sentence[end:end + 90], maxsplit=1)[0]
    before = re.split(r"[(,;]|\s\u2014\s", sentence[max(0, start - 60):start])[-1]
    return bool(NEGATIVE.search(after) or NEGATIVE.search(before))


def _optioned(sentence: str, start: int, end: int, quals: str) -> bool:
    """True when the count is the optioned part of the compiled-effect set: its noun is qualified as opt-in, the words after
    it put it behind the options, or it follows "FNA3D plus"."""
    after = re.split(r"[(,;]|\s\u2014\s", sentence[end:end + 120], maxsplit=1)[0]
    before = sentence[max(0, start - 60):start]
    return bool(re.search(_QUAL, quals or "", re.I) or OPT_AFTER.match(after) or OPT_BEFORE.search(before) or OPT_FAMILY_PAREN.search(before))


def _after_of(clause: str, m: re.Match) -> bool:
    """"11 of the 14 identities": the 14 is the whole the subset is taken from, not a claim of its own."""
    return not m.group("other") and bool(re.search(r"\bof\s+(?:the\s+)?$", clause[:m.start()], re.I))


GL_NAMES = r"(?:OPENGLES3|OPENGL33|WEBGL2|OpenGL ES 3(?:\.0)?|OpenGL 3\.3|WebGL 2)"
# "the two EasyGL profiles other than OPENGL33, OPENGLES3 and WEBGL2": a subset and its exclusions must add up to the family
EASYGL_EXCEPT = re.compile(r"\b" + NUM + r"\s+(?:EasyGL|GL)\s+(?:profiles|identities)\s+(?:other than|besides|except(?: for)?)\s+((?:" + GL_NAMES
                           + r")(?:\s*(?:,\s*(?:and\s+)?|\band\b)\s*" + GL_NAMES + r")*)", re.I)


def concept_findings(body: str, values: dict) -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    for m in EASYGL_EXCEPT.finditer(body):
        listed = len(re.findall(GL_NAMES, m.group(m.lastindex)))
        if "gl_profiles" in values and as_int(m.group("n")) + listed != values["gl_profiles"]:
            found.append((f"EasyGL subset arithmetic: {m.group('n')} profiles other than {listed} named ones is not the {values['gl_profiles']} "
                          f"EasyGL identities: \u2026{m.group(0)}\u2026", m.group(0)))
    found += classification_findings(body, values)
    if "compiled_effect_identities" not in values or "format_classifying_identities" not in values:
        return found
    total = values["renderer_identities"]
    capable, always = values["compiled_effect_identities"], values["compiled_effect_always_on_identities"]
    fams, cap_fams = values["implementation_families"], values["compiled_effect_families"]
    opt_ids, opt_fams = values.get("compiled_effect_optioned_identities", capable - always), values.get("compiled_effect_optioned_families", cap_fams - 1)
    tex_complement = total - values["format_classifying_identities"]
    rt_complement = total - values["rt_format_classifying_identities"]
    for m in list(COLOR_ONLY_COUNT.finditer(body)) + list(COLOR_ONLY_NOUN.finditer(body)):
        sentence = _sentence(body, m.start(), m.end())
        want = {tex_complement} | ({rt_complement} if RT_CTX.search(sentence) else set())
        if as_int(m.group("n")) not in want and not HISTORY.search(_clause_before(body, m.start())):
            found.append((f"Color-only renderer count {m.group('n')}, expected {' or '.join(map(str, sorted(want)))} (the identities outside the "
                          f"classifying families): \u2026{m.group(0)}\u2026", m.group(0)))
    previous = ""
    for sentence in re.split(r"(?<=[.!?])\s+", body):
        prev, previous = previous, sentence
        if HISTORY.search(sentence) and re.search(r"alpha\.1|b0e97bb1|009d40f5|d6e9ff05|\bearlier\b|\bprevious", sentence, re.I):
            continue                                        # a sentence about an earlier revision
        clauses = _clauses(sentence)
        for idx, (off, clause) in enumerate(clauses):
            compiled = (COMPILED_CTX.search(clause)
                        or (idx and COMPILED_CTX.search(clauses[idx - 1][1]) and re.search(r"\b(?:other|more|rest|remaining|it|them|FNA3D|opt-in|optioned|options?|default-OFF|default-off)\b", clause, re.I))
                        or (PRONOUN_PRED.search(clause) and COMPILED_CTX.search(prev if idx == 0 else clauses[idx - 1][1])))
            fmt = FORMAT_CTX.search(clause) or (idx and FORMAT_CTX.search(clauses[idx - 1][1]))
            unbound = UNBOUND_CTX.search(clause) and not compiled
            if not (compiled or fmt or unbound):
                continue
            rt = bool(RT_CTX.search(sentence))
            fmt_want = {tex_complement} | ({rt_complement} if rt else set())
            for m in IDENT_COUNT.finditer(clause):
                got = as_int(m.group("n"))
                other = bool(m.group("other") or m.group("more"))
                if _after_of(clause, m) or QUOTED.search(clause[:m.start()]) or HISTORY.search(clause[max(0, m.start() - 40):m.start()]):
                    continue
                if got == total and REGISTRY_PHRASE.match(clause[m.end():]):
                    continue
                if unbound:
                    window = clause[max(0, m.start() - 40):m.end() + 40]
                    outside = other or _polarity(sentence, off + m.start(), off + m.end()) or re.search(r"\bskip|\boutside\b", window, re.I)
                    cover = total - values["unbound_texture_identities"] if outside else values["unbound_texture_identities"]
                    if got != cover:
                        found.append((f"unbound-texture expectations cover {values['unbound_texture_identities']} renderer identities "
                                      f"({values['unbound_texture_families']} families){' and skip the other ' + str(cover) if outside else ''}, not {got}: \u2026{clause.strip()[:220]}\u2026", m.group(0)))
                    continue
                negative = _polarity(sentence, off + m.start(), off + m.end())
                default = bool(DEFAULT_CONFIG.search(sentence))
                if compiled:
                    if negative:
                        want = {total - capable} | ({total - always} if default else set())
                        what = "identities that cannot run compiled effects" + (" (or refuse them in a default configuration)" if default else "")
                    elif other or _optioned(sentence, off + m.start(), off + m.end(), m.group("q")):
                        want, what = {opt_ids}, "identities that can run compiled effects behind a default-OFF option (besides the always-on family)"
                    else:
                        want = {capable} | ({always} if default else set())
                        what = "identities that can run compiled effects" + (" (or have them on in a default configuration)" if default else "")
                        if got == values["gl_profiles"] and (EASYGL_CTX.search(clause) or (idx and EASYGL_CTX.search(clauses[idx - 1][1]))):
                            continue                        # "the EasyGL option covers its three identities"
                    if got not in want:
                        found.append((f"compiled-effect {what}: {got}, expected {' or '.join(map(str, sorted(want)))}: "
                                      f"\u2026{clause.strip()[:220]}\u2026", m.group(0)))
                elif fmt and (other or re.search(r"\bonly\b[^.;]{0,40}\b(?:on|for)\s+(?:the\s+)?$", clause[:m.start()], re.I) or re.match(r"(?:\s+[\w-]+){0,5}?\s*(?:accept|support|take|allow)s?\s+only\b|\s+without\s+an?\s+(?:[\w-]+\s+)?classifier\b",
                                                clause[m.end():], re.I)):
                    if got not in fmt_want:
                        found.append((f"format-classification complement: {got} identities outside the classifying families, expected "
                                      f"{' or '.join(map(str, sorted(fmt_want)))}: \u2026{clause.strip()[:220]}\u2026", m.group(0)))
            for m in FAMILY_COUNT.finditer(clause):
                got = as_int(m.group("n"))
                other = bool(m.group("other") or m.group("more"))
                if _after_of(clause, m) or QUOTED.search(clause[:m.start()]) or HISTORY.search(clause[max(0, m.start() - 40):m.start()]):
                    continue
                lead = re.search(r"\b" + NUM + r"\s+(?:\w+\s+){0,3}?identities\s+(?:in|over|across)\s+$", clause[:m.start()], re.I)
                if lead and as_int(lead.group("n")) == total:
                    continue                                # the registry phrase again, from the family side
                if unbound:
                    if got != values["unbound_texture_families"]:
                        found.append((f"unbound-texture expectations cover {values['unbound_texture_families']} implementation families, not {got}: "
                                      f"\u2026{clause.strip()[:220]}\u2026", m.group(0)))
                    continue
                if compiled:
                    if _polarity(sentence, off + m.start(), off + m.end()):
                        want = {fams - cap_fams} | ({fams - 1} if DEFAULT_CONFIG.search(sentence) else set())
                    elif other or _optioned(sentence, off + m.start(), off + m.end(), m.group("q")):
                        want = {opt_fams}
                    else:
                        want = {cap_fams, opt_fams}
                    if got not in want:
                        found.append((f"compiled-effect family count {got}, expected {' or '.join(map(str, sorted(want)))}: "
                                      f"\u2026{clause.strip()[:220]}\u2026", m.group(0)))
                elif fmt and re.match(r"\s*(?:\([^)]*\)\s*)?(?:that\s+)?(?:classify|promote|classifies|promotes)\b", clause[m.end():], re.I):
                    want = {values["format_classifying_families"]} | ({values["rt_format_classifying_families"]} if rt else set())
                    if got not in want:
                        found.append((f"format-classifying family count {got}, expected {' or '.join(map(str, sorted(want)))}: "
                                      f"\u2026{clause.strip()[:220]}\u2026", m.group(0)))
            if compiled:
                for m in OPTION_COUNT.finditer(clause):
                    got = as_int(m.group("n"))
                    if got != opt_fams and (got > opt_fams or m.group("q").strip()) and not HISTORY.search(clause[max(0, m.start() - 40):m.start()]):
                        found.append((f"compiled-effect build options: {got}, expected {opt_fams} (one default-OFF option per optioned family): "
                                      f"\u2026{clause.strip()[:220]}\u2026", m.group(0)))
                for m in BARE_OPTIONED.finditer(clause):
                    got = as_int(m.group("n"))
                    if got not in (opt_ids, opt_fams):
                        found.append((f"compiled-effect optioned count {got}, expected {opt_ids} identities or {opt_fams} families: "
                                      f"\u2026{clause.strip()[:220]}\u2026", m.group(0)))
            if fmt:
                for rx in FORMAT_BARE:
                    for m in rx.finditer(clause):
                        if as_int(m.group("n")) not in fmt_want:
                            found.append((f"format-classification complement: {m.group('n')} outside the classifying families, expected "
                                          f"{' or '.join(map(str, sorted(fmt_want)))}: \u2026{clause.strip()[:220]}\u2026", m.group(0)))
    return found


# Registry classification. GraphicsRendererType's enumerators and ordinals, and the per-identity switches of
# GraphicsBackendMaturity.hpp and GraphicsBackendCategory.hpp: "Fna3d (17)", "six Production, five Supported, three
# Experimental", "four identities (...) are TranslationLayer", "the remaining eight are Native", "the Direct3D trio".
# Category and maturity names are matched case-sensitively, so "two native GL-profile identities" is not the Native category.
_CLASS = r"Production|Supported|Experimental|Historical|Deprecated|Native|TranslationLayer|Translation\s+Layer|Software|Web|Diagnostic"
_NUM_CS = r"(?P<n>\d[\d,]*|(?i:" + "|".join(WORDS) + r"))"
CLASS_COUNT = re.compile(r"(?<![\w.-])" + _NUM_CS + r"\s+(?:(?:public|renderer|of\s+the\s+\d+)\s+)*(?:(?:identities|renderers|backends)\s+)?(?:\([^)]*\)\s+)?"
                         r"(?:(?:are|is)\s+)?(?:(?:declared|classified)\s+)?(?:as\s+)?(?P<c>" + _CLASS + r")\b(?=\s*(?:[,;.:)(]|$|and\b|or\b|identit|renderers?\b|backends?\b))")
# "Production: eight identities"
CLASS_COUNT_REV = re.compile(r"(?<![\w-])(?P<c>" + _CLASS + r")\s*(?::|=|\u2013|\u2014)\s*" + _NUM_CS + r"\s+(?:public\s+|renderer\s+)*(?:identities|renderers|backends)\b")
CLASS_CTX = re.compile(r"maturit|categor|GraphicsBackend|declare|classif|identit|renderer", re.I)
ORDINAL_CTX = re.compile(r"\bordinals?\b|\benumerators?\b|GraphicsRendererType", re.I)
MATURITY_NAMES = {"Production", "Supported", "Experimental", "Historical", "Deprecated"}
# an earlier revision named in the clause; narrower than HISTORY, whose "from" would excuse "from SdlRenderer (0) to Fna3d (17)"
REVISION = re.compile(r"alpha\.1|b0e97bb1|009d40f5|d6e9ff05|1bb2145d|\bearlier\b|\bprevious(?:ly)?\b|\bwas\b|\bwere\b|\bhad\b|\bused to\b|\bthen-current\b|\bonce\b|\bbefore\b", re.I)


def classification_findings(body: str, values: dict) -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    ords = values.get("renderer_ordinals") or {}
    names = "|".join(map(re.escape, sorted(ords, key=len, reverse=True)))
    for sentence in re.split(r"(?<=[.!?])\s+", body):
        if ords and ORDINAL_CTX.search(sentence):
            for m in re.finditer(r"\b(" + names + r")\s*\(\s*(\d+)\s*\)|\b(" + names + r")\s+(?:is|has|at|=)\s+(?:\w+\s+)?(?:C\+\+\s+)?ordinal\s+(\d+)", sentence):
                name, got = (m.group(1), m.group(2)) if m.group(1) else (m.group(3), m.group(4))
                if int(got) != ords[name] and not REVISION.search(_clause_before(sentence, m.start())):
                    found.append((f"GraphicsRendererType::{name} is ordinal {ords[name]}, not {got}: \u2026{m.group(0)}\u2026", m.group(0)))
            if re.search(r"GraphicsRendererType|\brenderer identit", sentence):
                for m in re.finditer(r"\bordinal\s+(\d+)\b", sentence):
                    if int(m.group(1)) > values["renderer_last_ordinal"] and not REVISION.search(_clause_before(sentence, m.start())):
                        found.append((f"renderer ordinal {m.group(1)} is outside GraphicsRendererType (0..{values['renderer_last_ordinal']}): "
                                      f"\u2026{sentence.strip()[:200]}\u2026", m.group(0)))
        if "renderer_maturity" in values and CLASS_CTX.search(sentence):
            for m in list(CLASS_COUNT.finditer(sentence)) + list(CLASS_COUNT_REV.finditer(sentence)):
                cls = re.sub(r"\s+", "", m.group("c"))
                table = values["renderer_maturity"] if cls in MATURITY_NAMES else values["renderer_category"]
                if as_int(m.group("n")) != table.get(cls, 0) and not REVISION.search(_clause_before(sentence, m.start())):
                    found.append((f"{'maturity' if cls in MATURITY_NAMES else 'category'} {cls} covers {table.get(cls, 0)} identities, not {m.group('n')}: "
                                  f"\u2026{sentence.strip()[:200]}\u2026", m.group(0)))
        if "direct3d_identities" in values:
            for m in re.finditer(r"\b(?:Direct3D|DirectX|D3D)\s+(trio|triple|triplet|pair|duo)\b", sentence, re.I):
                size = 3 if m.group(1).lower().startswith("tri") else 2
                if size != values["direct3d_identities"]:
                    found.append((f"the Direct3D renderer identities are {values['direct3d_identities']}, not a {m.group(1)}: \u2026{sentence.strip()[:200]}\u2026", m.group(0)))
    return found


EVIDENCE_CALLOUT = re.compile(r'<div class="callout[^"]*dev-evidence"[^>]*>(.*?)</div>', re.S)


def evidence_heading_findings(raw: str, sha_short: str) -> list[str]:
    out = []
    for m in EVIDENCE_CALLOUT.finditer(raw):
        c = m.group(1)
        read = re.search(r"checked by reading the CNA source at commit <code>(\w+)</code>", c)
        if "at the pinned commit" in c and read and read.group(1)[:8] != sha_short:
            out.append(f"evidence callout says 'at the pinned commit' but names {read.group(1)} as the commit read (cnahead is {sha_short}); "
                       f"say 'at the stated evidence commit'")
    return out


_DECL = r"(?:in-scope |planned |runtime-scope )?(?:public )?(?:C\+\+ )?(?:symbols|declarations)"
# "631 unmapped symbols", "631 public C++ symbols still unmapped", "631 missing C ABI exports" (beside the gate) all misread the
# release gate's planned rows as missing C exports, broken routes or link failures
AMBIGUOUS_MAPPING = re.compile(r"\b(\d[\d,]*) (?:unmapped " + _DECL + r"|" + _DECL + r" (?:are |remain )?(?:still )?unmapped)\b"
                               r"|\b(\d[\d,]*) (?:missing|absent|broken|unexported) (?:C )?(?:ABI )?(?:exports|routes|symbols|entry points)\b"
                               r"(?=[^.]{0,120}\b(?:release gate|C mapping|planned)\b)")


def mapping_wording_findings(body: str) -> list[str]:
    """The release gate's 'symbols' are planned public C++ declarations without a C mapping, not missing C exports;
    bare 'N unmapped symbols' reads as the latter. A verbatim quotation of CNA's own gate text stays legal."""
    out = []
    for m in AMBIGUOUS_MAPPING.finditer(body):
        before = body[max(0, m.start() - 160):m.start()]
        q = max(before.rfind("\u201c"), before.rfind("\u201d"), before.rfind('"'))
        if q >= 0 and (before[q] == "\u201c" or (before[q] == '"' and (q == 0 or before[q - 1] in " (:\u00a0"))):
            continue                                        # inside a quotation of the gate's own wording
        out.append(f"ambiguous C-mapping count: \u2026{body[max(0, m.start() - 80): m.end() + 40].strip()}\u2026 "
                   f"(say 'planned public C++ declarations without a C mapping')")
    return out


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
# it were current (a sentence naming both must say "archived"). Counts of nine/ten bindings or ten languages must
# stand in a historical or archived context; "eight" is allowed only where the sentence is about the archived set.
LB = facts["external_pinned"]["language_bindings"]
MAINTAINED_EXTERNAL = re.compile(r"C#|CNA\.NET")
ARCHIVED_NAMES = re.compile(r"\b(?:" + "|".join(re.escape(x).replace(r"\ ", r"\s+") for x in LB["archived"]) + r")\b|\b(?:"
                            + "|".join(map(re.escape, LB["archived_repositories"])) + r")\b")
STALE_COUNT = re.compile(r"\b(?:eight|8|nine|9|ten|10)\s+(?:public\s+|external\s+|language\s+|additional\s+)*bindings\b|\bEight binding projects\b"
                         r"|\b(?:ten|10)\s+(?:programming\s+)?languages\b", re.I)


# Development source tours of archived bindings describe the binding at its final revision (C ABI 0.21-0.35), so the C
# route totals they quote from that revision's census are history, not claims about cnahead.
ARCHIVED_BINDING_TOURS = {"development/internals/bindings/java.html", "development/internals/bindings/python.html"}


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
    for needle in ("Archived", "not maintained", "CNA Cemetery", "community interest"):
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
    ("index.html", r"\b<<cpp_samples_complete>>\b.{0,40}C\+\+ sample ports complete", "homepage stat: pinned C++ sample ports"),
    ("index.html", r"\b<<web_builds>>\b.{0,40}playable in the browser", "homepage stat: browser-playable sample builds"),
    ("index.html", r"\b<<cs_samples>>\b.{0,60}CNA\.NET", "homepage stat: original C# samples on CNA.NET"),
    ("index.html", r"<<sha_short>>", "homepage names the snapshot"),
    ("docs/rendering-backends.html", r"\b<<renderer_identities>> public (renderer )?identities", "renderer page: identity count"),
    ("docs/rendering-backends.html", r"\b<<implementation_families>>\b", "renderer page: family count"),
    ("docs/verification.html", r"\b<<static_test_definitions_n>>\b", "verification page: test definitions"),
    ("docs/verification.html", r"\b<<cpp_test_source_files>>\b", "verification page: test files"),
    ("docs/verification.html", r"\b<<ci_workflow_files>> workflow files", "verification page: workflows"),
    ("docs/platforms.html", r"\b<<platform_implementations>>\b", "platforms page: implementations"),
    ("docs/c-api.html", r"<<c_abi_version_rx>>", "C API page: ABI version"),
    ("docs/cna-net.html", r"<<c_abi_version_rx>>", "CNA.NET page: ABI version"),
    ("docs/c-api.html", r"\b<<c_api_routes_n>>\b", "C API page: route count"),
    ("docs/releases.html", r"<<sha_short>>", "releases page names the snapshot"),
]


def metric_values() -> dict:
    """The value table METRIC_RULES compare against: the source-derived counts (source_cross_check must have run, or
    this derives them) plus the facts-file values that have no source method here."""
    if "format_classifying_families" not in F:
        F.update(derive_from_cna((ROOT / "cnahead").read_text(encoding="utf-8").strip()))
    values = {k: F[k] for k in ("renderer_identities", "implementation_families", "gl_profiles", "platform_implementations",
                                "audio_implementations", "cpp_test_source_files", "cpp_test_files_with_macros",
                                "static_test_definitions", "compiled_effect_identities", "two_d_only_renderers", "parity_families")}
    values |= {k: F[k] for k in ("compiled_effect_families", "compiled_effect_always_on_identities", "format_classifying_families",
                                 "format_classifying_identities", "rt_format_classifying_families", "rt_format_classifying_identities",
                                 "standalone_pixel_programs", "compiled_effect_optioned_identities", "compiled_effect_optioned_families",
                                 "compiled_effect_never_identities", "compiled_effect_default_refusing_identities", "renderer_enumerators",
                                 "renderer_last_ordinal", "renderer_ordinals", "renderer_maturity", "renderer_category", "direct3d_identities",
                                 "web_only_identities", "non_web_gl_profiles", "unbound_texture_identities", "unbound_texture_families")}
    values["production_modules"] = 23
    values["implementation_families_subset"] = F["compiled_effect_families"]
    values["compiled_effect_more"] = F["compiled_effect_identities"] - F["compiled_effect_always_on_identities"]   # FNA3D always, the rest behind options
    values["example_cpp_files"] = {F["example_cpp_files"], F["module_example_cpp_files"]}   # with or without the loose demo
    values["complement_identities"] = values["renderer_names_outside"] = values["renderer_switches"] = F["renderer_identities"]
    values["complement_families"] = F["implementation_families"]
    return values


def page_claim_findings(page: str, raw: str, values: dict) -> list[tuple[str, str]]:
    """(message, matched text) for the metric and C-mapping wording rules over one page's visible text, block by block.
    Shared with scripts/adversarial_audit.py, which locates the matched text inside ledger anchor sections."""
    from check_retired_renderers import visible_blocks
    out: list[tuple[str, str]] = []
    for block in visible_blocks(raw, cell_headers=True):
        out += [(msg, msg) for msg in mapping_wording_findings(block)]
        column = re.match(r"\[\[(.*?)\]\] ", block)
        if column and HISTORY.search(column.group(1)):
            continue                                    # a cell in a column about an earlier revision ("Alpha.1")
        # an archive page and the tours of archived bindings describe an earlier revision as a whole
        if not page.startswith("historical/") and page not in ARCHIVED_BINDING_TOURS:
            out += metric_findings(block, values)
    return out


def public_pages() -> list[str]:
    from tombstones import TOMBSTONES  # a tombstone carries the footer only; scripts/tombstones.py checks it
    return [p.relative_to(ROOT).as_posix() for p in sorted(ROOT.rglob("*.html"))
            if not (SKIP_PARTS & set(p.relative_to(ROOT).parts)) and p.relative_to(ROOT).as_posix() not in TOMBSTONES]


def main() -> int:
    F["xna_runtime_members_n"] = n(F["xna_runtime_members"])
    F["sha_short"] = facts["snapshot"]["cna_sha_short"]
    F["cpp_samples_complete"] = facts["external_pinned"]["cna_samples"]["complete"]
    F["web_builds"] = facts["external_pinned"]["samples_libcna_com"]["playable_web_builds"]
    F["cs_samples"] = facts["external_pinned"]["cna_dotnet_samples"]["microsoft_sample_executables"]
    head = (ROOT / "cnahead").read_text(encoding="utf-8").strip()
    if facts["snapshot"]["cna_sha"] != head:
        print(f"FAIL data/current-facts.json describes {facts['snapshot']['cna_sha'][:8]}, cnahead is {head[:8]}")
        return 1
    bad = source_cross_check(head)   # from here on F holds the source-derived values
    F["static_test_definitions_n"] = n(F["static_test_definitions"])
    F["c_api_routes_n"] = n(F["c_api_routes"])
    F["c_abi_version_rx"] = F["c_abi_version"]
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
             ("8,263 static", "alpha.1 test definitions"), ("21 workflow files", "alpha.1 workflow count"),
             # superseded values of the previous snapshot (009d40f5)
             ("25 renderer identities", "009d40f5 renderer count"), ("25 public renderer", "009d40f5 renderer count"),
             ("21 implementation families", "009d40f5 family count"), ("12,610", "009d40f5 test definitions"),
             ("2,877", "009d40f5 commit count"), ("87 / 153", "009d40f5-era sample count"), ("87 of 153", "009d40f5-era sample count"),
             ("ABI 0.29.0", "009d40f5 C ABI"), ("ABI (0.29.0", "009d40f5 C ABI"), ("4,055", "009d40f5 C route count"),
             ("20 workflow files", "009d40f5 workflow count"), ("20 CI workflow", "009d40f5 workflow count"),
             ("seven host integrations", "009d40f5 platform count"), ("7 platform implementations", "009d40f5 platform count"),
             # superseded values of the previous snapshot (b0e97bb1)
             ("18 renderer identities", "b0e97bb1 renderer count"), ("18 public renderer", "b0e97bb1 renderer count"),
             ("18 identities", "b0e97bb1 renderer count"), ("14 implementation families", "b0e97bb1 family count"),
             ("12,021", "b0e97bb1 test definitions"), ("852 C++ test", "b0e97bb1 test files"), ("852 test", "b0e97bb1 test files"),
             ("3,333 commits", "b0e97bb1 commit count"), ("6 platform implementations", "b0e97bb1 platform count"),
             ("six platform implementations", "b0e97bb1 platform count"), ("Six platform implementations", "b0e97bb1 platform count"),
             ("ABI 0.44.0", "b0e97bb1 C ABI"), ("ABI (0.44.0", "b0e97bb1 C ABI"), ("26 jobs", "b0e97bb1 CI job count")]
    for page in [p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*.html") if not ({"audit", "scripts", "build-probe", ".git", "known-issues"} & set(p.relative_to(ROOT).parts))]:  # known-issues pages quote stale numbers of CNA's own documents on purpose
        if page == "docs/releases.html":
            continue  # release history compares alpha.1 with the snapshot on purpose
        body = cache.get(page) or text(page)
        archived_tour = page in ARCHIVED_BINDING_TOURS  # a source tour of an archived binding at its final revision
        for needle, what in stale:
            if archived_tour and what == "009d40f5 C route count":
                continue
            for m in re.finditer(re.escape(needle), body):
                ctx = body[max(0, m.start() - 90): m.end() + 60]
                if re.search(r"alpha\.1|earlier|previous|BASE|was |had |historical|\(BASE", ctx, re.I):
                    continue
                print(f"STALE? {page}: '{needle}' ({what}) \u2026 {ctx.strip()[:150]}"); bad += 1
    # every public page, Known Issues included: whole-registry phrasings of the source-derived numbers
    values = metric_values()
    for page in public_pages():
        raw = (ROOT / page).read_text(encoding="utf-8")
        problems = evidence_heading_findings(raw, F["sha_short"]) + [msg for msg, _core in page_claim_findings(page, raw, values)]
        for problem in dict.fromkeys(problems):
            print(f"DRIFT {page}: {problem}"); bad += 1
    bad += binding_policy([p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*.html")
                           if not ({"audit", "scripts", "build-probe", ".git", "known-issues"} & set(p.relative_to(ROOT).parts))])
    print(f"fact checks: {bad} problem(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
