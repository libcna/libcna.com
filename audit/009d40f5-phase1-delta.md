# Phase 1 delta ledger — libcna.com → CNA `009d40f5`

Living record of the Phase-1 update (preservation-first). Updated at every checkpoint.
Nothing in this file is served as site content; the site's pages never link to it.

## 1. Source boundary

| Item | Value |
|---|---|
| `LIBCNA_PRESENTATION_BASE` (libcna.com HEAD at session start, branch `docs/unified-v2`, == `develop`) | `be359024e3012653fa1e4963eb3ef86d9c16a5b7` — "index.html was updated", 2026-09-19 |
| libcna.com working tree at start | clean (only untracked `scripts/__pycache__/`) |
| `cnahead` at `LIBCNA_PRESENTATION_BASE` | **absent** — the deployed baseline has no `cnahead` file, so `CNA_DOCUMENTATION_BASE` was derived from release evidence (below) |
| `CNA_DOCUMENTATION_BASE` | `1bb2145d99ed572dd4eb15009c34e2e5f410fcf0` (CNA tag `v0.1.0-alpha.1`, 2026-08-20 19:04:19 +0200) |
| Evidence for the BASE | libcna tag `v0.1.0-alpha.1` → `c0ba893` "Update documentation for CNA v0.1.0-alpha.1"; `plan.md` and `audit/alpha1-delta.md` (both record `1bb2145d…` as the audited tag commit); `docs/releases.html` and `docs/roadmap.html`/`roadmap.html` cite it. Every commit after `c0ba893` in the deployed history is a presentation/ecosystem edit (web demos, blog callouts, network directory, org-link migration), not a CNA re-audit. |
| `CNA TARGET` | `009d40f5dd085c4e674d3479675fac84b12b3e0a` — "merge(OpenGL4ModernGraphics): integrate opengl4-modern-graphics into next", 2026-09-24 17:08:57 +0200 |
| Ancestry | `git merge-base --is-ancestor 1bb2145d… 009d40f5…` → **true** |
| `cnahead` (new) | `009d40f5dd085c4e674d3479675fac84b12b3e0a` + one newline (41 bytes) |
| CNA product version string at TARGET | `0.1.0-alpha.1` (`CMakeLists.txt`: `project(CNA VERSION 0.1.0)` + `CNA_VERSION_PRERELEASE "alpha.1"`) — TARGET is a **post-alpha.1 development snapshot on `next`**, not a tagged release |
| Immutable source worktrees | `/rv/tmp/libcna-v2/cna-base` (BASE) and `/rv/tmp/libcna-v2/cna-target` (TARGET), detached. Placed under `/rv/tmp` rather than `/tmp` because the shared build rules forbid clones/checkouts under `/tmp`. Removed at the end. |
| CNA branch checked out by the owner during the session | `street-perf` (other agents keep committing there; the TARGET is on `next` and is an ancestor-independent snapshot) |

## 2. Mechanical delta BASE → TARGET

| Metric | Value |
|---|---|
| Commits `BASE..TARGET` | **2,877** |
| First-parent commits | **713** |
| Merge commits | **47** |
| Changed paths (`git diff --name-status`) | **7,027** files: 3,430 added, 1,170 deleted, 2,499 modified (no-renames view) |
| Insertions / deletions | **+1,541,855 / −401,051** |
| Public-ish header files (`modules/**/include/**`, `Internal/` excluded) | 521 → **808** (287 added, 218 modified, 0 removed); +75,503 / −1,322 lines |
| All header files under `modules/**/include/**` | 823 → 1,081 |
| Tree size | 8,854 files / 132 MB → 11,114 files / 174 MB |

Commit types: fix 1,105 · feat 693 · docs 538 · test 331+33 · merge 29 · refactor 26 · perf 21 · chore 20 · build 15 · revert 11 · ci 10 · plan 8 · spike 7 · tools 4.

Largest changed areas by path: `modules/renderers` 2,001 · `tests/reference` 566 · `modules/graphics-ext` 564 · `modules/graphics` 516 · `tests/assets` 354 · `modules/content` 344 · `modules/content-pipeline` 243 · `modules/platform` 241 · `modules/c-api` 147 · `cmake/patches` 130 · `tools/xna-pipeline-oracle` 113 · `modules/media` 81 · `modules/audio` 80 · `tools/platform` 62 · `tools/xna-oracle` 59 · `modules/gamer-services` 53 · `modules/math` 43 · `modules/devices` 42 · `modules/input` 34 · `modules/runtime` 30 · `modules/net` 30.

Task-ID campaigns discovered from commit subjects (commit count): MOD 401 · SOFTWARE 389 · VULKAN 258 · XNASWEEP 185 · WEBGPU 133 · SAMPLE 110 · XNAPP 101 · SDLGPU 83 · WINNATIVE 75 · CBIND 75 · RLGL 56 · WINCLOSE 49 · CABI 49 · NPV 43 · XNAP 40 · WMG 38 · CNBF 38 · DX12 37 · WINPORT 32 · BINDFIX 32 · X11 31 · SMG 30 · GL4 25 · VKPAR 24 · GLTF 20 · XNA-MISSING 19 · REMED-GFX 18 · NPI 17 · WAYLAND 16 · VMG 16 · COMP 13 · RRC 12 · GTI 10 · STREET(S/W) 23 · PSG 6 · DIAG/INSP 4+7.

Top-level integration merges (first-parent, newest first): OpenGL4ModernGraphics · SdlGpuModernGraphics · WebGPUModernGraphics · VulkanModernGraphics · VulkanClassicCloseout · GpuTestIsolation · VulkanParity · `work` · DIAG-0001/INSP-0001 (Diagnostics and Inspector) · CApiCoverageToolingCleanup · CApiSmokeStability · TerminalCApiRepair · RendererCleanup (renderer-set curation) · GraphicsSharedCleanup · DirectX12 parity · X11 native backend (phases M, N) · RLGL · software renderer · sdlgpu · xnapipeline · vulkan · dx · webgpu · Three.js analysis · "restore the ten removed renderer identities" · CNB source mipmaps · csl · `pipeline` · content-pipeline (several) · bindings · CNB content format · modern.

Structural observations that shape the work (details in the per-area fact sheets under `audit/data/facts/`):

- The renderer module set shrank from 46 module directories to 21 (`modules/renderers/`) and gained `opengl4`; TARGET renderer truth is derived from the registry, not from history (the history contains removal, restoration and a final curation).
- New top-level modules: `content`, `content-pipeline`, `design`, `diagnostics`, `inspector`, `phone`, `runtime`, `graphics-ext`, `devices-ext`, `video-ffmpeg`, `c-api` (grown), plus `tools/xna-pipeline-oracle`, `tools/xna-oracle` (extended), `tools/xna-sample-sweep`.
- Native X11/Wayland/Windows platform work (`X11`, `WAYLAND`, `WINNATIVE`, `WINCLOSE`, `WINPORT`).
- XNA API-representation closure campaigns (`XNA-ENUM`, `XNA-MEMBER`, `XNA-MISSING`).

## 3. Workstreams → affected existing pages → new documentation

The CNA delta was audited hierarchically: `git log --first-parent` and the Task-ID campaign histogram located the change campaigns; the TARGET source
(read-only worktree) decided every fact; CNA's own Markdown was treated as untrusted. Eight read-only research agents produced cited fact sheets
(`audit/data/facts/01…08`, committed scrubbed of retired-renderer names) and a shared editorial guide with the cross-checked canonical numbers (`00-editorial-guide.md`).
The orchestrator independently recomputed the test inventory (904 files / 871 with macros / 12,610 definitions, same method reproduces BASE's 568 / 8,263 exactly)
and spot-verified removed-card premises and the homepage code example (syntax-only compile against the pinned headers).

| Workstream (campaigns) | What changed in CNA | Existing pages updated | New documentation |
|---|---|---|---|
| Renderer curation + modern graphics (RRC, RendererCleanup, VULKAN/VKPAR, SDLGPU, WEBGPU/WGF, GL4/STREETGL, DX12, SOFTWARE, WMG/SMG/VMG) | 50 → 25 public identities, 46 → 21 families; capability model 14 → 19 members + `RendererCapabilityProfile`; compiled effects on 14 identities; modern Vulkan/SDL_GPU/WebGPU/OpenGL4 surfaces | rendering-backends, runtime-renderer-selection, 3d-rendering, graphics-state, render-targets, tutorials 72, 85, 87, 101–103, 105, 107–109, 126 | tutorials 130–133; 3 tutorials removed (retired subject) |
| Platforms + audio + build (WINNATIVE/WINCLOSE/WINPORT, X11, WAYLAND, MOD, AUD-*) | native X11/Wayland/Win32 platforms, ALSA + CNA mixer, `CNA_ENABLE_SDL`, optional FFmpeg, `CNA_SHARED_LIBRARY`, 17+1 presets, 22 focused test targets, sharp-runtime `next` requirement | platforms, building, getting-started, audio, tutorials 01–03, 14, 15, 20, 80–82, 100, 118–120, 124, 127 | `docs/native-platforms.html`; tutorials 135–139 |
| Content (CNBF, XNAPP/XNAP, XNB, GLTF) | build-time Content Pipeline writing XNB and CNB, 61 XNB readers, `.xnb → .cnb → loose` ladder, `ResourceContentManager`, glTF limits re-verified | content-manager, content-pipeline-xnb (retitled XNB Loading & Interoperability), model-loading, tutorials 35, 36, 45, 46, 110–113 | `docs/content-pipeline.html`, `docs/cnb-format.html`; tutorials 145–148 |
| XNA representation (XNA-ENUM/MEMBER/MISSING, Framework.Design, Phone) | 3,627/3,627 members and 331/331 types represented; Framework.Design converters; storage/GamerServices/net behaviors | xna-compatibility, input, storage, sensors, video-playback, math-types, packed-vector, game-loop, spritebatch, migration-from-monogame, vs-alternatives, faq, tutorials 04–13, 16–19, 21, 22, 25–30, 41–44, 47–50, 71, 73, 76–79, 83, 84, 89–92, 94–98, 121–123 | `docs/design-converters.html`; tutorials 140, 141 |
| Effects, shaders, CNAEXT engine layer (FX, GSC, REMED-GFX) | compiled XNA effects on 14 identities, build-time `.fx` via external fxc, Reach profile enforced, engine layer 12 → 98 headers | effects, shader-effects, tutorials 23, 24, 31–34, 37–40, 51–70, 74, 75, 93, 114–117, 88, 128 | `docs/cnaext-engine.html`; tutorials 150–154 |
| C API, Diagnostics, Inspector, tools (CBIND, CABI, BINDFIX, DIAG, INSP) | C ABI 0.7.0 → 0.29.0 (61 headers, 4,055 routes); Diagnostics and Inspector modules; CLI tools | c-api, releases, docs/roadmap, tutorial 129 | `docs/diagnostics.html`, `docs/inspector.html`, `docs/tools.html`; tutorials 155–157 |
| Verification (XNASWEEP, SAMPLE, GTI, PSG) | 904 test files / 12,610 definitions, 20 workflows, oracle corpus facts, parity fixtures, content-pipeline oracle, bounded runner | verification, contribute, tutorials 99, 125 | tutorials 160, 161 |
| Ecosystem / front pages | cna-samples 87/153 (pinned), 14 web demos, new public projects, bindings pinned to ABI 0.21.x, dead links | index, demos, showcase, videos, features, about, documentation, tutorials hub, architecture, roadmap, network, contact | architecture diagram redrawn; 10 homepage stats; 6 new project cards |

Public-facing decisions recorded in the editorial guide: TARGET is described as a **development snapshot** (not a release; `CNA_VERSION_STRING` is still `0.1.0-alpha.1`); clone instructions use `next`
(GitHub's default branch is still the alpha.1 commit); consumer-project numbers are pinned to a repository revision; Speedy Blupi's live web build is described as an external, earlier CNA build.

## 4. Presentation baseline

- `audit/phase1-presentation-baseline.md` and `audit/data/phase1-baseline-inventory.json` were generated from git revision `be35902…` **before any site edit** by `scripts/inventory_presentation.py` + `scripts/inventory_report.py`.
- 174 HTML pages · 2,113 headings · 79 CTAs (22 primary) · 2,542 significant links · 681 cards/callouts · 52 images · 13 video entries · 8 homepage Quick Stats · 297 tables · 52 major blocks.
- Owner-designated protected content: homepage Quick Stats; Showcase "Verification against the real XNA runtime"; Demos → Speedy Blupi incl. the primary `Play in Browser` → `https://speedyblupi.com/SpeedyBlupi2013/`.
- Final result: `audit/phase1-presentation-comparison.md` — **0 unexplained losses**, 98 dispositioned differences recorded in `audit/data/phase1-dispositions.json`.

## 5. Checkpoints (commits on `docs/unified-v2`, nothing pushed)

| # | Checkpoint | Status |
|---|---|---|
| 1 | Pin TARGET (`cnahead`), record baseline, ledger | done |
| 2 | Preservation tooling, snippet checker, docs sidebar/new-page generator, facts file | done |
| 3 | Homepage, demos, showcase, videos | done |
| 4 | Renderer surface (reference, selection, tutorials, 130–133) | done |
| 5 | Content pipeline / CNB / XNB / glTF (+145–148) | done |
| 6 | C API, releases, roadmap, Diagnostics, Inspector, tools (+155–157) | done |
| 7 | Verification evidence (+160, 161) | done |
| 8 | About, roadmap, documentation hub, contact, network | done |
| 9 | Platform, audio, build (+135–139) | done |
| 10 | CNAEXT engine layer (+153, 154) | done |
| 11 | Features, architecture (+ redrawn diagram) | done |
| 12 | 3D rendering and 3D tutorials (+152) | done |
| 13 | XNA reference pages (+140, 141), foundation tutorials 04–30 | done |
| 14 | Effects (+150, 151), advanced 3D tutorials, intermediate tutorials 41–98 | done |
| 15 | Tutorial hub, three tutorials removed, site-wide consistency, indexes, responsive CSS, final audit | done |

## 6. Validation evidence (final run)

| Check | Result |
|---|---|
| `scripts/validate_site.py` | 204 HTML files parsed; strict HTML5 (html5lib) 204/204 authored pages with no errors; 14,081 references and 924 local fragments inspected, 0 broken; 0 duplicate IDs; 188 JSON-LD blocks parse; 202 search entries and 202 sitemap URLs, unique and complete; metadata/canonical complete |
| `scripts/compare_presentation.py` | 0 unexplained losses (98 dispositioned) |
| `scripts/validate_presentation.py` | 6/6 (cnahead, Quick Stats, real-XNA verification, Speedy Blupi section, Speedy Blupi primary CTA, all 22 baseline primary CTAs) |
| `scripts/check_retired_renderers.py` | 0 references to any of the 26 retired identities in public content (set derived from the CNA registries at run time; nothing stored in the repository) |
| `scripts/check_facts.py` | 0 problems (canonical numbers in `data/current-facts.json` present on the pages that must carry them; no stale alpha.1 count presented as current) |
| External links | 133 distinct external URLs checked; all answer 2xx (two VS Code Marketplace URLs answer 404 to scripts but 200 to a browser user agent) |
| Code snippets | every C++ example written or repaired in Phase 1 was syntax-checked with `g++ -std=c++23 -fsyntax-only` against the pinned TARGET headers (`scripts/check_snippet.sh`); nothing was built or run, and the pages that depend on unbuilt configurations say so |
| `git diff --check` | clean |
| Mobile/tablet layout | headless-Chrome scan of all 203 public pages at 390 px and 768 px: 0 pages with horizontal page overflow (baseline: **103 of 173** pages overflowed at 390 px, e.g. docs/vs-alternatives at 1,067 px, because docs grids used `1fr` columns; fixed with `minmax(0,1fr)` grid columns and long-identifier wrapping) |
| Visual QA | headless Chrome 1360 px, light and dark: index, demos, showcase, videos, features, documentation, tutorials, renderers, platforms, content pipeline, verification inspected; 390 px screenshots of index (light/dark), demos, showcase, renderers, platforms. No browser extension was connected, so screenshots were taken from the command line |

## 7. Post-TARGET contamination check

CNA HEAD at completion: `9bb6dc0a7e03ddcca60f5d496f23b302d332dcf8` (branch `street-perf`, the owner's working branch). `git log 009d40f5..HEAD` = **7 commits**
(STREETGL4-0001/0002 and STREETPERF-0001…0004: renderer performance work, plus two plans and docs); `git diff --name-status 009d40f5..HEAD` touches renderer sources/tests and the
engine-layer version header only. **None of it is documented** (site grep for those task ids and features: no hit). The TARGET SHA in `cnahead` and on every page is unchanged.

## 8. Known limits (stated on the pages where they matter)

- Nothing was built or run: C++ claims come from source, CMake logic and CI YAML; the C API library, Wayland, Windows-native, Android, Metal-on-macOS and browser results are not verified by us.
- CI status: workflow files are configuration, not results; static reading suggests several Apple/Emscripten/Windows workflows pin an older sharp-runtime revision than the snapshot needs.
- Consumer-project numbers (cna-samples 87/153, cna-examples 249, cna-extended lines, demos) are pinned to a named external revision and are not TARGET results.
- Speedy Blupi: the hosted web build is an external build with an embedded May-2026 CNA revision (static inspection of the committed wasm; not run in a browser); no Android APK exists.
- The oracle corpus references were captured under Wine + DXVK on Linux; DIRECTX9's 39/39 has no committed 39-scene run log (the last dated report covers 31); none of it is in CI.
