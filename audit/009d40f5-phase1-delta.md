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

## 3. Workstream → affected existing pages → new documentation

*(filled in per campaign as each checkpoint completes; see §5)*

## 4. Presentation baseline

- `audit/phase1-presentation-baseline.md` (human-readable) and `audit/data/phase1-baseline-inventory.json` (machine-readable) are generated from git revision `be35902…` **before any site edit** by `scripts/inventory_presentation.py` + `scripts/inventory_report.py`.
- 174 HTML pages · 2,113 headings · 79 CTAs (22 primary) · 2,542 significant links · 681 cards/callouts · 52 images · 13 video entries · 8 homepage Quick Stats · 297 tables · 52 major blocks.
- Owner-designated protected content (must survive): homepage Quick Stats (8 stats); Showcase "Verification against the real XNA runtime"; Demos → Speedy Blupi section incl. primary `Play in Browser` → `https://speedyblupi.com/SpeedyBlupi2013/`.
- Baseline validator result (before edits): `scripts/validate_site.py` → 174 HTML files, 172 search entries, 172 sitemap URLs, 0 problems (strict html5lib pass skipped: `html5lib` not installed).

## 5. Checkpoints

| # | Checkpoint | Status |
|---|---|---|
| 1 | Pin TARGET, record baseline, ledger skeleton | done |
| 2 | Per-area fact sheets (`audit/data/facts/01…08`) | in progress |

