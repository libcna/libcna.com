# Phase-2 editorial guide — absorbing developer.libcna.com into libcna.com/development

Authoritative for every agent writing Development pages. Read it completely, then read the Phase-1 editorial guide's
§2–§5 (`audit/data/facts/00-editorial-guide.md`: snapshot framing, canonical numbers, retired-renderer rule, truthfulness
rules), which still apply unchanged. If the two guides disagree, this one wins for Development pages.

## 0. The job in one paragraph

libcna.com (Phase 1, accepted) documents CNA snapshot **`009d40f5dd085c4e674d3479675fac84b12b3e0a`** (call it TARGET).
`developer.libcna.com` is a separate, frozen maintainer field manual, written against an **older** CNA commit
(`d6e9ff050e32bcfe5e7fd640006619a90b92298c`, the "Developer pin", an ancestor of TARGET, 55 commits earlier). Your job is to
**absorb every piece of useful current knowledge in your assigned Developer pages into libcna.com/development/**, additively and
without loss, after **re-verifying it against TARGET**. Developer is a *knowledge source*, never a factual authority: where it
disagrees with TARGET, TARGET wins and you write the TARGET-correct statement.

```
developer page  ->  candidate knowledge  ->  verify against TARGET source  ->  publish as a libcna.com page
```

The result should read as a natural part of libcna.com (same site chrome, same voice as the Phase-1 docs), be at least as deep as the
Developer page it absorbs, and be **more** useful: cross-linked to the user guide, architecture and neighbouring pages.

## 1. Hard boundaries

* **Read-only sources:** the Developer working tree (`/rv/data/development/github.com/libcna/developer.libcna.com`), the CNA repository
  (`/rv/data/development/github.com/libcna/cna`, Git objects only; never check out, reset, clean, fetch or write there) and the extracted
  TARGET tree **`/rv/tmp/libcna-v2/cna-target`** (read-only; `third_party/` and `vendor/` are not extracted: use
  `git -C /rv/data/development/github.com/libcna/cna show 009d40f5dd085c4e674d3479675fac84b12b3e0a:<path>` for those).
* **Never document post-TARGET facts.** The CNA checkout's HEAD is 7 commits *past* TARGET; ignore it. Always read TARGET
  (`/rv/tmp/libcna-v2/cna-target`, or `git show 009d40f5…:path`). Never use `git grep` without naming the TARGET revision.
* Do **not** read or use: the CNA Bible (`bible.libcna.com`), any earlier "unified documentation" attempt, other libcna.com branches or worktrees.
  Your inputs are exactly: the accepted Phase-1 working tree, the original Developer pages, and TARGET.
* No builds, no cmake/make/compilers, nothing under `/tmp` except the scratchpad given in your brief. No `git add/commit/push`.
* Write **only** (a) fragment files under the scratchpad `dev-src/` tree for your assigned pages and (b) the built pages for those pages
  (`python3 scripts/site_dev.py build …`). Do not edit any other repository file (not the manifest, CSS, scripts, protected pages).
  If you believe the manifest, tooling or another page needs a change, say so in your report.
* Do not import Developer's *coverage status* as product status. In Developer, "NOT STARTED" means "its documentation audit has not
  covered this", not "CNA lacks it"; "SOURCE VERIFIED" means "cross-checked against a Git tree by Developer's authors", not "runtime-proven".
  None of those labels appears on the published pages.

## 2. Tools

```bash
cd /rv/data/development/github.com/libcna/libcna.com
python3 scripts/dev_pack.py <developer-page>          # e.g. platforms/wayland.html — verification pack (do this first)
python3 scripts/dev_manifest.py --list                # the whole planned page set (paths you may link with {{page:}})
python3 scripts/site_dev.py build --src <SRC> <page>  # write one page from <SRC>/<path minus .html>.body.html + .meta.json
python3 scripts/check_dev_page.py <page> [...]        # per-page validator; must print "ok" for your pages
git -C /rv/data/development/github.com/libcna/cna diff d6e9ff05 009d40f5 -- <path>   # what changed after the Developer pin
```

`dev_pack.py` prints: every CNA path the Developer page cites (exists at TARGET? changed since the Developer pin? renamed?),
`<code>` tokens whose identifiers do not occur anywhere in TARGET, cited commits, external repository pins, and the page text.
**A "changed since Developer pin" path is a mandatory re-verification target**: read its diff and the current file, and rewrite every
claim that depended on it. But an *unchanged* path only proves the file is identical; the claim about it may still have been wrong,
so spot-check the load-bearing claims there too (symbols, ordering, ownership, test names, CMake options).

CNA changed after the Developer pin mostly in: `modules/renderers/opengl4/`, `modules/renderers/sdl-gpu/` (modern compute, SPIR-V shader
intake, indirect draw, shadow/IBL, storage buffers/images), `modules/renderers/easygl/` (5 files), `modules/graphics/` (tests, examples, 3 headers:
`GlPresentationSurfaceState.hpp`, `GlStockShaderSources.hpp`, `PlatformGlRendererState.hpp`), `modules/graphics-ext/` (clustered forward desktop GLSL),
`cmake/` (RendererSelection, TestHelpers, UnitTests, Harnesses, SDL prebuilt fingerprint/patches, FNA3D, SDL), `docs/opengl4-renderer.md`,
`docs/cnaext-engine-layer.md`, `tools/opengl4/`, `tools/platform/`. Everything else is byte-identical to the Developer pin.

## 3. Method for each Developer page you own

1. `python3 scripts/dev_pack.py <page>`; read the whole pack and the Developer page carefully. Note the page's own section list.
2. Read the Phase-1 libcna pages that cover the same subsystem (`docs/*.html`, `architecture.html`; the destination's neighbours in the manifest)
   so that you complement rather than duplicate or contradict them. The Phase-1 site is the trusted foundation; if you find a genuine
   Phase-1 factual error, record it in your report (do not edit protected pages yourself).
3. **Verify every technical claim against TARGET**: paths, symbols (types, methods, enumerators), CMake targets/options/defaults, test names
   and registration, ordering and ownership statements, behaviours, counts. Read the source, do not rely on grep hits alone for behaviour.
   Classify each claim: *confirmed*, *corrected* (TARGET differs), *dropped* (no longer true / not verifiable — say why in the ledger),
   *extended* (you learned something more from TARGET that belongs on the page).
4. Write the page (§4–§6). Keep **all** of the Developer page's unique knowledge that is still true — the reasoning, the worked
   examples, the caveats, the "read in this order" lists, the tests named, the failure modes. Do not summarize a 1,500-word page into 600 words.
   You may reorganize for reading flow, but not thin out. You *may* add value: more precise TARGET facts, TARGET-pinned links, cross-links,
   a short "what changed for a maintainer" note where TARGET moved past Developer.
5. Write the ledger record (§7), build the page, run `check_dev_page.py`, fix all ERRORs. Keep the `PENDING` warnings that point to
   manifest pages that other agents are still writing.

## 4. Quality bar

* Concrete CNA content only: source paths, types, functions, registries, CMake targets/options, tests, invariants, call flow, ownership,
  failure modes. No generic software-engineering advice, no filler, no motivational prose.
* Preserve evidence semantics exactly. Distinguish *source verified*, *build verified*, *test covered/present*, *runtime observed*,
  *oracle compared*, *hardware observed*. "The implementation exists" is not "the behaviour is proven correct everywhere". A test being
  named/registered is not the test having passed. You did not run tests or builds: say "not executed" wherever the distinction matters,
  and keep Developer's own carve-outs ("real-host validation remains", "not exercised on native Windows", …) when they still hold.
* Do not over-claim beyond Developer either: if TARGET evidence for a sentence is thin, hedge or drop it and log it.
* Use TARGET numbers from the Phase-1 canon (25 renderer identities / 21 families, 7 platforms, 4 audio implementations, C ABI 0.29.0, …).
  Where Developer quotes a count, recompute or replace it with the canonical fact; do not copy a stale number.
* Never name a retired renderer identity (see Phase-1 guide §4). `check_dev_page.py` and the site validators scan for them. When a Developer
  page discusses renderer history, describe it without naming retired identities (e.g. "an earlier, much larger renderer set was curated
  down to the current 25 identities") and say in the ledger that names were withheld by policy.
* `alpha.1` appears only as historical context ("since v0.1.0-alpha.1"); TARGET is a post-alpha.1 development snapshot on `next`.
* Bugs and gaps: if the Developer page records a *current* defect or gap, keep it on the page only as a scoped, evidenced maintainer note
  and list it in the ledger `current_bugs_or_gaps`. Do not import fixed historical defects as if current. (A page's *worked historical
  case study* of a fixed defect is legitimate teaching material; it must say it is historical and what the current code does.)
* Voice: neutral third person, present tense for TARGET facts. Never "I verified…"; write "checked by reading … at 009d40f5; not executed".
  No references to "this manual", "this handbook", "the coverage ledger", "Phase 0", Developer's site/nav/generator, or its pin.
  Refer to "these pages", "the TARGET snapshot", "the Development area".

## 5. Fragment format (what you write)

Body fragment `<SRC>/<page path minus .html>.body.html` — the inside of the article, **without** `<h1>` (generated from meta.title), without
TOC, evidence box, related-pages block, breadcrumb, sidebar, pager (all generated).

* Start with `<p class="lede">…</p>` (2–4 sentences: what this page is for and who needs it), then `<h2 id="kebab-id">` sections; `<h3>` inside.
  Keep Developer's h2 ids where a section survives, so the ledger can map section→section mechanically.
* Links to CNA source — **only via tokens** (validated against the TARGET tree at build time):
  `{{src:modules/runtime/src/Game.cpp}}` · `{{src:modules/runtime/src/Game.cpp|Game.cpp}}` (label) · `{{tree:modules/platform/src|platform sources}}` (directory).
  No line-number anchors (they rot); name the function instead. Every source path you mention in prose should be a token link the first
  time it appears in a section (a path that is a plain `<code>` cannot be validated). Symbols: plain `<code>Game::Tick</code>`.
* Links to other site pages — **only via** `{{page:development/internals/runtime/startup.html|label}}` or with a fragment
  `{{page:docs/platforms.html#sdl3|Platforms guide}}`. Any manifest page is a valid target even if unbuilt yet. Verify a fragment you link exists.
* External binding repositories (cna-cs, cna-java, cna-python) may be linked as
  `https://github.com/libcna/<repo>/blob/<40-hex commit>/<path>` at the commit the Developer page cites, **after** you verify the path exists there
  (`git -C /rv/data/development/github.com/libcna/<repo> cat-file -e <commit>:<path>`). They are evidence for *that revision*, not for TARGET.
* Elements: `<div class="callout callout--info|warn|note"><span class="callout-icon">&#8505;</span><p>…</p></div>`;
  `<table><thead><tr><th scope="col">…</th></tr></thead><tbody>…</tbody></table>` (do **not** wrap tables; the generator does);
  code `<pre><code class="language-cpp|bash|cmake|json">…</code></pre>` (escape `<`, `&`); ASCII diagrams `<pre class="diagram">…</pre>` (no `<code>` inside);
  lists `<ul>`/`<ol>`; "Read in this order" as `<ol class="source-list">`. No inline styles, scripts, images, or custom classes.
* Prose can name `Game::Tick` etc. in `<code>`; never put `{{…}}` inside `<code>`.

Meta `<SRC>/<page path minus .html>.meta.json`:

```json
{
  "title": "Wayland platform internals",
  "description": "One sentence (<= 220 chars, no HTML) that matches the page.",
  "keywords": ["wayland", "xdg-shell", "…6-12 lowercase search terms: option names, key types, subsystem words"],
  "evidence": {"levels": ["source-verified", "test-present"],
               "note": "Optional extra sentence, e.g. what remains unverified (real compositor matrix)."},
  "layers": {
    "guide":        [["docs/native-platforms.html#wayland", "Native platforms guide"]],
    "architecture": [["development/architecture/platform.html", "Platform architecture"]],
    "internals":    [["development/internals/platforms/x11.html", "X11 (sibling backend)"]],
    "maintainer":   [["development/handbook/modify-a-platform-backend.html", "Modify a platform backend"]],
    "tests":        [["development/testing/architecture.html", "Test architecture"]],
    "reference":    [["development/reference/test-targets.html", "Test target index"]]
  },
  "developer_sources": ["platforms/wayland.html"]
}
```

`evidence.levels` ⊆ {source-verified, test-present, build-verified, runtime-observed, oracle-compared, hardware-observed}. For pages you wrote
from reading source: `source-verified`, plus `test-present` when the page names tests that exist. Use the other levels only when TARGET's own records
say so *and* you attribute them to CNA ("CNA's records report …") — the site never claims it ran anything.
`layers` targets: at least `guide` (a Phase-1 docs/ page — verify it exists and the anchor exists) and `architecture`/`internals`/`maintainer` where they
apply; every link must resolve.

## 6. Section-preservation rule

Every Developer h2/h3 of your page must end up either (a) as a section in the destination (same or retitled), (b) merged into another section
of the destination, or (c) dropped with a stated reason (stale / contradicted by TARGET / process content about Developer's own site). The ledger records the mapping;
a checker compares it against Developer's headings, so **do not leave a Developer heading unaccounted for**.

## 7. Ledger record (what you write, one per Developer page)

`<SRC>/<destination path minus .html>.ledger.json`:

```json
{
  "developer_source": "platforms/wayland.html",
  "destination": "development/internals/platforms/wayland.html",
  "action": "MERGE | EXPAND | NEW PAGE | CROSS-LINK | SUPERSEDED | DUPLICATE | OBSOLETE | TARGET-CONTRADICTED | NOT CURRENT",
  "developer_status": "as stated in Developer docs/COVERAGE.md (Developer's own audit state, NOT CNA product status)",
  "unique_knowledge": "2-4 sentences: what this unit contributes that no Phase-1 page has",
  "phase1_overlap": [{"page": "docs/native-platforms.html", "relation": "complements | duplicates | contradicts", "note": ""}],
  "target_verification": {
    "cited_paths": 12, "missing_at_target": [], "changed_since_developer_pin": [],
    "claims_checked": 60,
    "contradictions": [{"developer_claim": "…", "target_fact": "…", "evidence": "path (function/symbol)", "resolution": "corrected on the page"}],
    "dropped": [{"claim": "…", "reason": "…"}],
    "extended": ["one line per notable TARGET fact added beyond Developer"]
  },
  "sections": [
    {"developer_heading": "Where platform, renderer and native driver meet", "developer_id": "selection",
     "disposition": "MERGED | EXPANDED | CORRECTED | SPLIT | DROPPED",
     "destination": "development/internals/graphics/sdl-gpu.html#selection", "note": ""}
  ],
  "current_bugs_or_gaps": [{"summary": "…", "evidence": "path", "note": "recorded for the later bug catalogue; not published as a catalogue"}],
  "phase1_errors_found": [{"page": "docs/x.html", "issue": "…", "evidence": "…"}]
}
```

`action` is normally `MERGE` (Developer knowledge re-hosted and merged into the Development area), `EXPAND` (you substantially extended it),
`NEW PAGE` (no Developer counterpart); use the others only with a clear reason. `sections` must list **every** Developer `<h2>` and `<h3>` of the source page.

## 8. Report (≤ 350 words, your final message)

(1) pages built (paths) and word counts vs the Developer source; (2) contradictions corrected (Developer vs TARGET) — the most important ones;
(3) claims dropped and why; (4) Phase-1 errors found; (5) current bugs/gaps recorded; (6) anything unverifiable that you hedged;
(7) manifest/tooling changes you need; (8) `check_dev_page.py` result.
