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
commit"), and the C ABI release gate's planned rows are "public C++ declarations", never bare "unmapped symbols".
scripts/test_validators.py feeds the reviewer's exact stale sentences through METRIC_RULES.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
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
    return {"renderer_identities": len(public), "implementation_families": len(families),
            "platform_implementations": len(platforms), "audio_implementations": len(audio_ids),
            "gl_profiles": len(gl), "cpp_test_source_files": len(tests), "cpp_test_files_with_macros": len(per_file),
            "static_test_definitions": sum(per_file), "c_abi_version": version, "c_api_routes": routes,
            "parity_families": len(parity)}


def source_cross_check(sha: str) -> int:
    """Fail when data/current-facts.json disagrees with the source; afterwards F holds the source-derived values."""
    try:
        derived = derive_from_cna(sha)
    except (OSError, subprocess.CalledProcessError, AttributeError) as exc:
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
    ("gl_profiles", r"(?<!WebGL )(?<!OpenGL )(?<!ES )(?<!GL )\b" + NUM + r"\s+(?:public\s+)?(?:renderer\s+)?identities\s+(?:share|sharing)\b[^.;]{0,40}?\b(?:EasyGL|one (?:CNA )?implementation)", 0,
     "EasyGL profile count"),
    ("gl_profiles", r"\bEasyGL (?:family )?\(" + NUM + r"(?: public)? identities", 0, "EasyGL profile count"),
    ("parity_families", r"\bparity\b[^.;]{0,80}?\b(?:registered for|on|for) (?:the )?" + NUM + r" (?:renderer )?families\b", 0, "parity-fixture family count"),
    ("parity_families", r"\bregistered for (?:the )?" + NUM + r" renderer families\b", 0, "parity-fixture family count"),
    ("parity_families", r"\b" + NUM + r" (?:renderer )?families call cna_register_parity_fixtures\b", 0, "parity-fixture family count"),
    ("compiled_effect_identities", r"\b" + NUM + r" (?:of the \d+ )?(?:renderer )?identities (?:that )?(?:support|can run|run) compiled\b", 0, "compiled-effect identity count"),
    ("compiled_effect_identities", r"(?<!refusals: )\bcompiled(?:(?!false|unsupported|refus|\bnot\b)[^.;]){0,60}?\b" + NUM + r" of the \d+ (?:renderer )?identities\b", 0,
     "compiled-effect identity count"),
    ("compiled_effect_more", r"\b" + NUM + r" more (?:renderer )?identities\b", 0, "compiled-effect identities besides FNA3D"),
    ("two_d_only_renderers", r"\b" + NUM + r" (?:deliberately )?2D-only (?:renderers|identities|families)\b", 0, "2D-only identity count"),
    ("two_d_only_renderers", r"\b" + NUM + r" (?:renderer )?identit(?:y|ies) (?:is|are) (?:deliberately )?2D-only\b", 0, "2D-only identity count"),
    ("platform_implementations", r"\b" + NUM + r" (?:CNA_PLATFORM |platform )implementations\b", 0, "platform implementation count"),
    ("platform_implementations", r"\bCNA_PLATFORM\b (?:now )?offers " + NUM + r" implementations\b", 0, "platform implementation count"),
    ("audio_implementations", r"\b" + NUM + r" (?:CNA_AUDIO_PLATFORM |audio )implementations\b", 0, "audio implementation count"),
    ("cpp_test_source_files", r"\b" + NUM + r" (?:CNA-owned )?C\+\+ test (?:source )?files\b", 500, "C++ test source file count"),
    ("cpp_test_source_files", r"\btest figures \(" + NUM + r" files\b", 0, "C++ test source file count"),
    ("cpp_test_files_with_macros", r"\b" + NUM + r" (?:of (?:the files|the test files|which|them) |(?:test )?files )?(?:contain|contains|with) (?:at least one|a counted|such a|counted)\b",
     500, "test files containing a counted macro"),
    ("static_test_definitions", r"(?<!with )(?<!has )(?<!holds )\b" + NUM + r" (?:static(?:ally)?(?: declared| discoverable)? (?:GoogleTest-family )?definitions|static test definitions)\b",
     1000, "static GoogleTest-family definitions (whole tree)"),
    ("production_modules", r"\b" + NUM + r"\s+production\s+modules\b", 0, "production module count"),
]
_MACRO_RULE = next(r[1] for r in METRIC_RULES if r[0] == "cpp_test_files_with_macros")
# the number belongs to an earlier revision, in its own clause, before it
HISTORY = re.compile(r"alpha\.1|b0e97bb1|009d40f5|d6e9ff05|1bb2145d|\bearlier\b|\bprevious(?:ly)?\b|\bbefore\b|\bwas\b|\bwere\b|"
                     r"\bhad\b|\bfrom\b|historical|\bresearch\b|audited (?:commit|revision)|\bused to\b|\bthen\b|\bonce\b|"
                     r"\bremoved\b|\brestored\b|\bretired\b|\bnarrowed\b|\bshipped\b|\btagged\b", re.I)
# the number is quoted from a document (typically one of CNA's own stale files, the subject of a Known Issue): a quotation
# mark, a reporting verb or a file name earlier in the same sentence
QUOTED = re.compile(r"[\u201c\"]|\b(?:says?|states?|reads?|pins?|claims?|speaks? of|describes?|quotes?|Doxygen|comment|header)\b|"
                    r"\.(?:md|cmake|json|h|hpp|py)\b|CHANGELOG", re.I)
# a rule that applies only in a sentence of a given subject
REQUIRES = {"compiled_effect_more": re.compile(r"compil|COMPILED|opt-in build option|Effect Framework", re.I)}
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
            if got == want or got < minimum:
                continue
            sentence = _sentence(body, m.start(), m.end())
            if HISTORY.search(_clause_before(body, m.start("n"))) or QUOTED.search(sentence[:max(0, sentence.find(m.group(0)))]):
                continue
            if key in REQUIRES and not REQUIRES[key].search(sentence):
                continue
            if key in SUBSET and re.search(SUBSET[key][0], sentence, re.I) and got == values.get(SUBSET[key][1]):
                continue
            found.append((f"{what} {got} != {want}: \u2026{body[max(0, m.start() - 90): m.end() + 50].strip()}\u2026", m.group(0)))
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


AMBIGUOUS_MAPPING = re.compile(r"\b(\d[\d,]*) (?:unmapped (?:public )?symbols|(?:public )?symbols (?:are )?(?:still )?unmapped)\b")


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
    for needle in ("Archived", "not maintained", "CNA Lab", "community interest"):
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
    if "gl_profiles" not in F:
        F.update(derive_from_cna((ROOT / "cnahead").read_text(encoding="utf-8").strip()))
    values = {k: F[k] for k in ("renderer_identities", "implementation_families", "gl_profiles", "platform_implementations",
                                "audio_implementations", "cpp_test_source_files", "cpp_test_files_with_macros",
                                "static_test_definitions", "compiled_effect_identities", "two_d_only_renderers", "parity_families")}
    values["production_modules"] = 23
    values["implementation_families_subset"] = int(re.search(r"\((\d+) families\)", facts["facts"]["compiled_effect_identities"]["label"]).group(1))
    values["compiled_effect_more"] = F["compiled_effect_identities"] - 1   # FNA3D always, the rest behind options
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
