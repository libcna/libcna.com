# 00 — Editorial guide for Phase-1 page edits (read this first, then your fact sheets)

Authoritative for every agent editing libcna.com pages in Phase 1. If a fact sheet and this guide disagree, this guide wins
(the orchestrator has cross-checked the numbers below); if you find a *fact-sheet* error while editing, say so in your report.

## 0. The job in one paragraph

The deployed libcna.com (baseline `be35902`) documented CNA `v0.1.0-alpha.1` (`1bb2145d`). Update it **in place** so that it accurately
documents CNA snapshot **`009d40f5dd085c4e674d3479675fac84b12b3e0a`** (24 Sep 2026, branch `next`, 2,877 commits after the tag;
CNA's product version string is *still* `0.1.0-alpha.1`). The owner likes this site. **Preserve human value** — sections, cards,
buttons, CTAs, images, statistics, stories, examples, explanatory depth, visual hierarchy — and correct/extend the facts *inside* them.
"Old valuable section + TARGET truth = updated valuable section", never "stale facts → delete section".

## 1. Hard preservation rules (protected pages are: index, demos, showcase, videos, features, about, documentation, tutorials,
architecture, roadmap, network, contact — all at repo root)

* Do **not** remove a substantial section, collapse cards into a paragraph, remove a useful image/screenshot/video, remove a useful direct
  external link, downgrade a primary CTA (e.g. `btn btn-primary` "Play in Browser" → generic secondary), replace a specific playable/demo URL by a
  homepage, or shrink a substantial section by more than 50 % for concision. Do not turn a rich page into a directory of links.
* If something is stale: update the number, narrow the overstated claim, correct the status, correct the description around a still-valid link.
  Delete only genuinely dead / false / unsupported / removed-functionality material, and record why (see §8 "dispositions").
* Preserve visual language, class names, page structure, `id` anchors (other pages and outside links deep-link to them). Additive expansion is welcome
  (new sections, cards, tables, pages) — the site may grow substantially.
* After editing a protected page run `python3 scripts/compare_presentation.py --page <page>`; it must report **0 unexplained losses**.
  It compares against the baseline inventory (`audit/data/phase1-baseline-inventory.json`). Anything it flags you either restore or list under
  "Requested dispositions" in your report (with the reason). Never silence it by editing scripts or the baseline.
* `python3 scripts/validate_site.py` must stay clean for your pages (it validates *all* pages; ignore problems in files you don't own but report them).

## 2. Framing: snapshot vs release

* Say **"this snapshot"**, "CNA snapshot `009d40f5`", "current development snapshot" for anything true at TARGET. Use **alpha.1** / `v0.1.0-alpha.1` only for
  historical statements ("alpha.1 shipped X; this snapshot has Y") and on `docs/releases.html`.
* CNA's `CNA_VERSION_STRING` is still `0.1.0-alpha.1` — it is *not* a new release. Never write "alpha.2", "0.2", "beta".
* `git clone https://github.com/libcna/cna.git` yields **alpha.1** (GitHub default branch `develop` = the tag commit). TARGET is branch **`next`**
  (`git clone -b next …`, or check out `009d40f5dd085c4e674d3479675fac84b12b3e0a`). **sharp-runtime must also be its `next` branch** (`main`/`develop` lack the
  `Resources` and `Xml.Serialization` components CNA now requires). easy-gl / meta-gl / free-direct use their default `develop`. Any quickstart must say so.
* Links to CNA files: prefer `https://github.com/libcna/cna/blob/009d40f5dd085c4e674d3479675fac84b12b3e0a/<path>` (or `/tree/next/…`) over `master`/`develop`
  (`master` does not exist; `develop` = alpha.1). Link to the tag only when you mean the tag.
* Do not present moving external numbers (samples, lines of code, binding versions, demo counts) as TARGET facts. If needed, pin `repo @ sha (date)`.

## 3. Canonical numbers (cross-checked; use exactly these)

| Fact | Value | Note |
|---|---|---|
| Snapshot | `009d40f5` = `009d40f5dd085c4e674d3479675fac84b12b3e0a`, 2026-09-24 17:08 +0200, branch `next` | |
| Release history | tag `v0.1.0-alpha.1` = `1bb2145d99ed572dd4eb15009c34e2e5f410fcf0`, 2026-08-20 | +2,877 commits (713 first-parent, 47 merges), 7,027 changed paths, +1.54 M / −0.40 M lines |
| **Renderers** | **25 public identities over 21 implementation families**; 5 GL identities share EasyGL | was 50/46 |
| 2D-only renderers | 7 (`SDL_RENDERER DIRECT2D CANVAS HTML_DOM SVG_DOM FREEDIRECT GDI`); `STUB` also reports 3D false (no-op) | was 13 |
| Windows-only / Emscripten-only / macOS-only | 5 (`[retired renderers] DIRECT2D GDI`) / 5 (`WEBGL1/2 CANVAS HTML_DOM SVG_DOM`) / 1 (`METAL`) | |
| Default renderer | Emscripten `WEBGL2`; Linux `OPENGLES3`; everything else `SDL_RENDERER` | unchanged |
| GraphicsCapability | **19** members (was 14) + new `RendererCapabilityProfile` API (32 features, 22 limits, per-format usage, report) | |
| Compiled XNA effects | Supported by **14 of 25 identities** in **10 families**: FNA3D always on; 9 default-OFF build options (`CNA_EASYGL_/VULKAN_/WEBGPU_/SOFTWARE_/DIRECTX9_/DIRECTX11_/DIRECTX12_/SDL_GPU_/OPENGL4_COMPILED_EFFECTS`; EasyGL's option enables all five GL identities). A default configure reports `CompiledEffects` true on FNA3D only (24 of 25 false). `Effect(GraphicsDevice&, bytes)` is real, not a throwing stub. No runtime HLSL `.fx`/DXBC/MGFX. `cna-content` compiles `.fx` at build time through an external legacy fxc (unverified against genuine fxc). | fact sheet 05 |
| Default GraphicsProfile | **Reach**, now enforced on every renderer: MRT, OcclusionQuery, 32-bit indices, float targets, large cubes throw unless `HiDef` is requested — many alpha.1-era tutorials omit this | fact sheet 05 §H |
| **Platform implementations** (`CNA_PLATFORM`) | **7**: `SDL3` (default) `SDL2` `X11` `WAYLAND` `WIN32` `HEADLESS` `TERMINAL`; reserved & refused: `SDL12`, `EMSCRIPTEN` | native X11/Wayland/Win32 use no SDL; `CNA_ENABLE_SDL=AUTO|ON|OFF` |
| **Audio implementations** (`CNA_AUDIO_PLATFORM`) | **4**: `SDL3` (default) `SDL2` `NULL` `ALSA`; reserved & refused: `OPENAL`, `WASAPI` | `SOUND_ENABLED` (a mixer) for **SDL3 and ALSA** only |
| FFmpeg | now optional (`CNA_ENABLE_VIDEO=AUTO|ON|OFF`); Video types exist everywhere, throw `NotSupportedException` without a backend | never built on Windows/Emscripten/Android/iOS |
| Toolchain | CMake ≥ 3.20, C++23; `CNA_SHARED_LIBRARY` defaults ON on native ELF (GNU/Clang, CMake ≥ 3.27) | see fact sheet 02 for presets (17 visible + 1 hidden configure presets) |
| Tests (site method, recomputed at both revisions) | **904** C++ test source files (871 contain a counted macro), **12,610** static GoogleTest-family definitions (BASE 568 / 539 / 8,263) | plus 879 standalone `examples/**/*_test.cpp` pixel programs not in those figures; no CTest total is derivable — publish none |
| CI | **20** workflow files, 28 jobs (BASE 21 files); 17 automatic; D3D/GDI Windows lanes manual; no Android, no Wayland, no C-API-build, no oracle-corpus workflow | `EASYGL` config bug fixed |
| XNA API representation | **331/331** public types, **3,627/3,627** documented runtime members represented (`tools/audit_xna_runtime_surface.py`, census from Microsoft XML + DLL metadata) | *representation only, not behavior* |
| Content Pipeline API representation | 128/128 types, 705/705 members, 10 importers, 12 processors | representation; build-time tool |
| Oracle corpus | **39** scenes (256×256, HiDef) with real-XNA-4.0 reference PNGs (captured under **Wine + DXVK on Linux**), plus 7 null-texture scenes and a 17-format expansion table (outside any diff denominator) | DIRECTX9 recorded 0-diff at tolerance 0 on all 39 (Wine+DXVK; last dated report covers 31; not in CI). EasyGL & Software gated on 2 line scenes only; Software measured 18/39 byte-exact; FNA3D gates only that scenes render. See fact sheet 07 |
| Cross-renderer parity fixtures | 32 fixtures × 4 renderers (EasyGL, WebGPU, SDL_GPU, OpenGL4); oracle = the fixtures' own assertions, not real XNA | |
| glTF conformance corpus | 148 assets = 140 captured + 8 rejected safely; renderer-owned goldens (not a reference-renderer comparison); Khronos comparison subset 13 | |
| XNB built-in readers | **61** (60 without native int128); load ladder `.xnb` → `.cnb` → loose files; **CNA now also writes XNB and CNB** via `cna-content` (build-time content pipeline) | fact sheet 04 |
| C ABI | **0.29.0** (experimental; was 0.7.0); 61 headers; 4,055 routes; inventory 9,355 symbols (8,363 implemented / 15 partial / 468 planned / 509 N/A); release gate "Not ready" (468 unmapped); no CI job builds it; the alpha.1 compile blocker (renderer-map count) is gone in source but a build was **not** verified by us | say "source-level, not build-verified" where it matters |
| Product version | `0.1.0-alpha.1` (unchanged) | |
| New modules | `content`, `content-pipeline`, `design` (Framework.Design converters), `diagnostics`, `inspector`, `phone`, `video-ffmpeg`, `graphics-ext` (CNAEXT engine layer: 12 → 98 public headers), `devices-ext`, `runtime` | fact sheets 04/05/06 |
| cna-samples (external, **pinned**) | `libcna/cna-samples @ 4da98a0` (2026-09-20): plan inventories **153** upstream sample directories; **87** marked complete; 40 published playable at samples.libcna.com; 49 await owner decisions; 14 documented non-ports; Racing Game tracked separately | the alpha.1-era "63 of 86 / 23 blocked by .fx" is **false** now; results are for CNA `next` at that date, not for TARGET |
| Language bindings (external) | cna-cs, cna-java, cna-ts, cna-python, cna-rust, cna-swift are public pre-alpha projects; each targets ABI **0.21.x**; CNA TARGET exports **0.29.0** (alpha.1: 0.7.0). Five refuse 0.29.0 by exact-version rule. **Never** imply "latest binding + latest CNA works". cna-go / cna-ruby are listed at the owner's request (2026-09-25) as in development, in repositories that are not public yet — never link them (GitHub returns 404). | fact sheet 08 |

## 4. Retired renderers — hard rule

25 renderer identities that existed in alpha.1 were retired (a 26th was added and retired in between). Their names and dependencies are in the **private**
file a private scratch file that is deliberately not part of the repository
(read it for scrubbing only). **Never write a retired identity, alias, module name, or a dependency used only by a retired renderer into any page**
(not even "removed: X"), except: `docs/releases.html` may say generically that alpha.1 had a much broader renderer surface that was later curated to 25.
There is no "retired renderers" catalogue. A retired name in CMake is a configure error; you may say *that* ("a name outside the 25 is a configure-time
error") without naming names. Old spellings that are **not** retired identities but old names of current ones (`D3D9`→`DIRECTX9`, `DX3`→`FREEDIRECT`,
`CNA_GRAPHICS_BACKEND`→`CNA_GRAPHICS_RENDERER`, `EASYGL`→five GL profiles) may remain in "names that changed" tables.
Pages whose *whole purpose* is retired functionality (tutorials 86, 104, 106) are deleted by the orchestrator, not by you — but you must remove
links to them from your pages when the orchestrator tells you, and keep your prose valid without them. Preserve the PRESENTATION VALUE:
an old rich 50-renderer section becomes an equally rich, current 25-renderer section (tables, callouts, per-family cards), not a short list.

## 5. Truthfulness rules that have bitten before

* Distinguish **representation** (a symbol/type/member exists; 3,627/3,627) from **behavior** (output compared with real XNA). Never imply the denominator is larger than the executed evidence.
* Distinguish reference corpus size, campaign denominator, renderer, host (Wine+DXVK on Linux, not Windows), tolerance, independent FNA evidence.
* "Builds" ≠ "passes" ≠ "verified". State CI scope (what a workflow actually gates). Whether the C API library builds at TARGET was **not** verified by us.
* Consumer projects (samples, Speedy Blupi, demos, showcase games, bindings) are evidence for *their own pinned revision*, not for TARGET.
* Speedy Blupi: the live `https://speedyblupi.com/SpeedyBlupi2013/` is a stock-Emscripten WebAssembly build of the OpenEggbert C++ port of the *2013 Windows Phone* game;
  it embeds an early (May 2026, pre-modularization) CNA + sharp-runtime + SDL3 revision using the `SDL_RENDERER` backend, i.e. neither alpha.1 nor TARGET.
  No Android APK is published anywhere. Desktop builds from source (`openeggbert/mobile-eggbert`). The game was decompiled from the 2013 release — do not call it "open-source".
  Do not claim a CNA Desktop/WebAssembly/Android *release* of it.
* Where the web has no persistence claim you are unsure of, check fact sheet 03/04 before repeating alpha.1's "no web save persistence" (it may have changed).

## 6. HTML/site conventions

* Every page: `<title>`, `<meta name="description">` (keep it a single sentence that matches the page), og:title/og:description equal to title/description, canonical, JSON-LD
  (`dateModified` → `2026-09-24` for pages you substantively edit). `scripts/build_site_indexes.py` regenerates `search-index.json` and `sitemap.xml` from these — **do not edit those two files**.
* Keep the existing component classes: `callout callout--info|warn|note`, `cards`/`cards--2`/`card`, `table-wrap`, `demo-platform`/`demo-item`, `video-card`, `btn btn-primary|secondary|outline [btn-sm]`,
  `status-badge status-done|wip|planned|partial`, `doc-meta`, `toc`, `docs-pagination`. Code blocks: `<pre><code class="language-cpp|bash|cmake|json">` with HTML-escaped `<`, `&`.
* Accessibility: semantic headings in order, alt text on images, `<th scope>`/headers in tables, meaningful link text, no color-only meaning, tables wrapped in `.table-wrap`.
* No duplicate `id`s; every `#fragment` you link must exist; no broken relative links. New docs pages use `python3 scripts/site_nav.py new-docs …`; new tutorials
  `python3 scripts/site_nav.py new-tutorial …` (they generate the shared nav/footer/JSON-LD; the sidebar is synchronized centrally — tell the orchestrator the sidebar label you want).
  New pages **must be linked** from at least one hub (`documentation.html`, `tutorials.html`, a docs pagination or an existing docs page) — leave hub links to the orchestrator unless the hub is in your page list; list them in your report.
* Footer text and the global snapshot footer were already updated on all 174 pages — leave it.
* Code shown must be true at TARGET: verify class/method names and signatures against `/rv/tmp/libcna-v2/cna-target` headers (`modules/*/include`). The real call style is
  `getContentProperty().Load<T>("name")` returning by value (older pages that show `Content->Load`/`Content.Load` do not compile) — check fact sheet 04.
* Never run cmake/make/compilers and never write under `/tmp`. You may run `g++ -fsyntax-only` only if you know the include set works without generated headers; otherwise read headers.
* Do not `git add`/`git commit`. The orchestrator commits by workstream.

## 7. Tutorials

Audit every tutorial in your range for TARGET correctness: stale APIs, build flags, renderer/platform/audio assumptions, content workflow, effect workflow, counts, sample references,
"Before you start" boilerplate lines (e.g. "thirteen 2D-only renderers…" → 7), `dateModified`. Do not rewrite mature tutorials for style; do not delete a tutorial because part is stale — correct it.
Replace the CMake command line `-DCNA_GRAPHICS_RENDERER=` values only with the 25 valid names. Real end-to-end tasks, not link cards. Keep pagination/next-links valid.
New tutorials: numbers by work package (see your brief); file name `NNN-slug.html`; they are real end-to-end tasks with commands/APIs verified against TARGET.

## 8. Your report (what the orchestrator needs)

Reply with ≤ 500 words: (1) files changed / created / deleted (paths); (2) each significant fact you changed and any *fact-sheet* disagreements you found;
(3) **Requested dispositions** — every protected-page item you removed/downgraded with reason + evidence (only where truly justified);
(4) sidebar labels / hub links you need added; (5) anything you could not verify and left hedged; (6) validator results for your files.

## 9. Fact sheets (read the ones for your area; they cite TARGET file:line)

`audit/data/facts/01-renderers.md` · `02-platforms-audio-build.md` · `03-xna-api-runtime.md` · `04-content-pipeline.md` · `05-effects-cnaext.md` ·
`06-capi-diagnostics-inspector.md` · `07-verification.md` · `08-ecosystem-external.md`. TARGET tree: `/rv/tmp/libcna-v2/cna-target`, BASE tree: `/rv/tmp/libcna-v2/cna-base` (read-only).
Baseline inventory of the deployed site: `audit/phase1-presentation-baseline.md`.
