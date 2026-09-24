# 07 - Verification, oracle and testing evidence at CNA TARGET

- TARGET: `009d40f5dd085c4e674d3479675fac84b12b3e0a` (2026-09-24 17:08 +0200, `merge(OpenGL4ModernGraphics)`), worktree `/rv/tmp/libcna-v2/cna-target`.
- BASE: `1bb2145d99ed572dd4eb15009c34e2e5f410fcf0` (tag `v0.1.0-alpha.1`, 2026-08-20), worktree `/rv/tmp/libcna-v2/cna-base`.
- Range `BASE..TARGET`: 2,877 commits; `git diff --shortstat`: 7,027 files changed, +1,541,855 / -401,051.
- All paths below are TARGET-relative unless prefixed `BASE:`. Nothing was built or run; every number is either recomputed statically from source/CMake/committed data (tag **[V]**) or quoted from a CNA-committed report/plan (tag **[R]**, UNTRUSTED, with its own date). **[STALE]** marks a CNA document that contradicts newer CNA evidence.
- Labels used deliberately: *reference corpus size* (what exists) vs *campaign denominator* (what a given command/CTest actually iterates) vs *renderer* vs *host* vs *tolerance* vs *independent FNA evidence* vs *representation* (a symbol exists) vs *behavior* (output compared).

---

## Verified facts

### F1. The headline change since BASE: the renderer set shrank, so every per-renderer verification number from alpha.1 is void
- `cmake/RendererIdentities.cmake:20-23` lists **25 public renderer identities**; `:29-33` lists 26 retired identities ([retired], [retired renderers], OPEN[retired]). Commit `1321ca346` (2026-09-17, RRC-005) says "25 public renderer identities over 21 implementation families".
- `modules/renderers/` holds 23 entries at TARGET vs 48 at BASE (`ls`). `docs/removed-renderers.md` tombstones the rest. The C-API renderer map (`modules/c-api/src/CnaCApiCoreExt.cpp:195-220`) has 25 rows against the canonical 25 (static read only; C API buildability was NOT verified by me).
- Consequence for verification claims: `OPEN[retired]` (the site's "11 / 39" row) no longer exists; `scripts/run-oracle-corpus-diff-open[retired].sh` is gone; `docs/fna3d-parity-report.md:3-5,28` keeps the row but tags it "retired 2026-09-17". (Renderer inventory itself is another agent's fact sheet; I only use it as a denominator context.)

### F2. The 39-scene oracle corpus is unchanged in content; the tree around it grew
- 39 top-level `tools/xna-oracle/scenes/*.scene` + 39 `tools/xna-oracle/reference/*.png` at both BASE and TARGET. The 39 scene files differ only in header comments (`plan_dx9.md` -> `plans/plan_dx9.md`); I compared non-comment lines of all 39: **0 content changes**. All 39 reference PNGs are byte-identical BASE vs TARGET (sha256), and the site's `img/oracle/*.png` (39 files) are byte-identical to the TARGET references.
- All 39 scenes are 256x256 (65,536 pixels each), `profile=HiDef`; 9 are `spritebatchmode=true`; effects declared: AlphaTestEffect 8, BasicEffect 2 (others default to BasicEffect), DualTextureEffect 1, EnvironmentMapEffect 3, SkinnedEffect 6 (`grep` over `scenes/*.scene`).
- NEW since BASE (all commit `ea0656ca1`, 2026-09-17, GSC-0004, plus `38a375fbf` VKPAR-0014): 7 scenes + 7 PNGs under `scenes/null-texture/` and `reference/null-texture/` (64x64, measure what a stock effect samples from an unbound texture: opaque black); `FormatExpansionOracle.cs` + `reference/format-expansion/xna-format-expansion.txt` (17 SurfaceFormat channel-expansion measurements, comment header lines 1-4). Total `tools/xna-oracle` files: 97 (46 scene files, 46 PNGs, 1 text table, README, Oracle.cs, CnaOracleRender.cpp, FormatExpansionOracle.cs).
- The 7 null-texture scenes are **deliberately outside every script's `scenes/*.scene` glob** (`tools/xna-oracle/scenes/null-texture/*.scene:5-6`). They are not part of any pixel-diff denominator; unit tests hard-code their centre-pixel values (`modules/graphics/tests/Microsoft/Xna/Framework/Graphics/StockEffectNullTextureTests.cpp:3-12`, active for Software, OpenGL33, OpenGL4, OpenGLES3, DirectX11, DirectX12, Vulkan, WebGPU at `:71-78`).
- `BASE:tools/xna-oracle/[retired]-2d-policy.tsv` is gone ([retired] retired).

### F3. Who produced the reference images: real Microsoft XNA 4.0, on Wine + DXVK, on Linux - not on Windows
- `tools/xna-oracle/README.md:83-104`: `Oracle.cs` is compiled by the real `csc.exe` inside Wine prefix `~/.wine-cna-xna40` (WINEARCH=win32) against the GAC `Microsoft.Xna.Framework*.dll`, with DXVK installed into that same prefix ("otherwise real XNA runs on WineD3D while CNA/D3D9 runs on DXVK, and any diff would silently measure a driver difference").
- `docs/d3d9-divergence-report.md:135-147` **[R]**: every comparison ran under Wine+DXVK on an AMD Radeon 780M (RADV); `D3DCAPS9` is synthesized by DXVK; "not yet validated against a real Windows box" (task `D9-140`, still `needs_human` and open: `plans/plan_dx9.md:993`).
- `spikes/xna-*-spike/README.md` (6 probes) confirm the same host: `~/.wine-cna-xna40`, "D3D9 through DXVK", DXVK 2.6, AMD Radeon 780M.
- Real Windows is used elsewhere only for the Content Pipeline: `README.md:55` [R] says disputed behavior was "settled against genuine XNA 4.0 on a Windows 7 VM"; `plans/plan_xna_sample_xnb_sweep.md:34-46` [R] lists `win7-export/`, `win7-build/` as genuine-reference directories. `docs/testing-win32-native.md:3-4` [R] states everything known about `CNA_PLATFORM=WIN32` came from MinGW cross-builds run under Wine, not native Windows.
- `scripts/xna-diff.py` (whole file): default `--tolerance 0`, every RGBA channel of every pixel; optional extended-policy flags (`--rgb-tolerance`, `--alpha-tolerance`, `--max-raw-differing-pixels`, `--allowed-raw-diff-rect`, `:25-60`) exist but **no script at TARGET uses them** (grep). Every runner passes `--tolerance 0` (`run-oracle-corpus-diff.sh:59`, `run-oracle-corpus-multi.sh:92`, `run-oracle-corpus-diff-easygl.sh:84`) or defaults to 0 (`-fna3d`, `-software`).

### F4. What CNA's tooling actually gates, per renderer (campaign denominators)
| Command / CTest | Registered at | Scenes iterated | Tolerance | Fails on | Renderer / host |
|---|---|---|---|---|---|
| `D3D9_XNA_Diff` -> `scripts/run-oracle-corpus-diff.sh` | `modules/renderers/directx9/examples/CMakeLists.txt:254` (block starts `:17`: only when `CNA_BUILD_TESTS` and `CNA_GRAPHICS_RENDERER=DIRECTX9`) | **39** (`for scene in "$SCENES_DIR"/*.scene`, `run-oracle-corpus-diff.sh:39`, non-recursive) | 0 | any scene that fails to render or differs by 1 channel value in 1 pixel | DIRECTX9, MinGW cross-build run through `scripts/run-wine-dxvk9.sh` (Wine+DXVK) |
| `Fna3d_XNA_Oracle` -> `run-oracle-corpus-diff-fna3d.sh` | `modules/renderers/fna3d/examples/CMakeLists.txt:92-95` | 39 (`:63`) | 0 (arg 2, default 0) | **only** a scene that fails to render (or missing reference); pixel differences are reported, not failed (`:101-104`, header `:14-24`) | FNA3D, `FNA3D_FORCE_DRIVER=OpenGL`, X display |
| `EasyGL_XnaLineCoverage` | `modules/renderers/easygl/examples/CMakeLists.txt:157-161` | **2** (`colored_linelist_quad colored_linestrip_quad` passed as args) | 0 | either scene differs | EasyGL default-profile build (`CNA_BUILD_EXAMPLES` and `CNA_BUILD_TESTS` on, not Windows, not Emscripten; block at `easygl/examples/CMakeLists.txt:48-49`), X display |
| `Software_XnaLineCoverage` | `modules/renderers/software/examples/CMakeLists.txt:1154-1157` | **2** (same two) | 0 | either scene differs | single-renderer SOFTWARE build (`software/examples/CMakeLists.txt:30`), display-free (`SDL_VIDEODRIVER=dummy`) |
| `scripts/run-oracle-corpus-diff-software.sh` (whole corpus) | not registered (header `:1-7`: "a measurement, not an exact-image gate") | 39 (`:48`) | arg, default 0 | only render failure | SOFTWARE |
| `scripts/run-oracle-corpus-diff-easygl.sh` (whole corpus) | not registered when run without scene args | 39 (`:58`) | 0 | any difference (exit 1) | EasyGL |
| `scripts/run-oracle-corpus-multi.sh` | not registered (`rg` finds no CMake/workflow reference) | 39 x N renderers (`:73`) | 0 | any difference for any listed renderer; a renderer not compiled in is reported SKIPPED | one multi-renderer binary, renderer chosen per run via `CNA_GRAPHICS_RENDERER` |
- **No GitHub workflow runs any of these** (`rg -i "oracle|XNA_Diff|xna-diff" .github/workflows` finds nothing relevant; `general-tests-ci.yml` does not install Pillow, which `xna-diff.py` imports; `gltf-renderer-stride-ci.yml:144` does). The only gated whole-corpus check (`D3D9_XNA_Diff`) exists only in a DIRECTX9 cross-build tree and needs Wine+DXVK.
- The 7 null-texture scenes and the 17-row format table are **not iterated by any script**; they exist as recorded measurements consumed by unit-test expectations.

### F5. Recorded results (all [R], dated, NOT re-run by me)
- DIRECTX9, tolerance 0: `docs/d3d9-divergence-report.md:3-4,31` says **0/31 scenes diverge** (2026-07-15; that report was never updated after the corpus grew). `tools/xna-oracle/README.md:175` says "Thirty-nine scenes so far, all pixel-perfect on the original D3D9 oracle path". `NEXT.md:6556-6558` (2026-07-16): "36 scenes deep, all pixel-perfect (5 new since the 31-scene count)" and `NEXT.md:6609`: the 3 cull-mode scenes brought the corpus to 39 (each `0/65536`). There is **no committed dated run log for 39/39**; the 39/39 figure is the sum of per-scene notes plus the README status. `README.md:47,591` [STALE] still says "31-scene corpus, 0/31".
- FNA3D: `docs/fna3d-parity-report.md:3-16` (2026-08-11, Mesa 25.2.8 llvmpipe, GL driver only): **10/39 exact, 29 differing, 0 failed to render**; same report lists EasyGL 10/39 and OPEN[retired] 11/39 (retired). These figures **predate** EasyGL fixes (`76f1f6ebe` 2026-08-22 "restore XNA pixel-center coverage in EasyGL" which targets the very edge-only divergence class the report attributes 17 of 21 EasyGL differences to; `SOFTWARE-336` clip-depth fix 2026-09-11) and no later committed EasyGL whole-corpus count exists. Treat 10/39 as dated and possibly understated, not as current.
- SOFTWARE: `plans/plan_software.md:675,677` and `docs/software-renderer.md:897-917` (2026-09-11): 39/39 render; after `SOFTWARE-345` **18/39 byte-exact, 30/39 within 1 channel value**, same nine point-texture-boundary scenes outside 1; the two line scenes are exact after `SOFTWARE-344` and are the `Software_XnaLineCoverage` gate.
- EasyGL line scenes: `docs/software-renderer.md:905-907` "the same seven references match current Mesa EasyGL" (7 = the isolated line probes + the two corpus scenes).
- Cross-renderer whole-corpus multi-run: `plans/plan_runtimerenderer.md:825` (RTR-P9-24) records that the script was verified on `OPENGLES3;OPENGL33`; no committed per-renderer totals.

### F6. Independent FNA evidence (real FNA executed, values recorded)
- Harness `tools/fna-reference/` (C#, runs real `FNA.dll` under mono), `tools/cna-reference/CnaReferenceDump.cpp` (target `cna_reference_dump`, `cmake/Harnesses.cmake:169-183`), `scripts/compare-fna-reference.py` (default categories `NonRenderingApis`, `PackedVector`, `Viewport`, `:26`). `docs/fna-reference-harness.md:67-76`: **not registered as a CTest, manual developer workflow**; covers 21 enums, 16 state presets, 17 PackedVector types, Viewport project/unproject; Effect-device categories were "DEFERRED" in that doc.
- NEW since BASE (commit `a62c8458d`, 2026-09-10, FX-005): `tools/fna-reference/EffectPixelReference.cs` + checked-in FNA-produced JSON `tests/fixtures/compiled-effects/fna-effect-pixels.json` (generator string "FnaReference --effect-pixels", FNA assembly 26.5.0.0, FNA3D linked 260500, 7 effects), `fna-effect-reflection.json` (7 effects), `fna-effect-states.json` (7 `.fxb`). Consumed by CTest-registered gtests `Fna3dEffectPixelOracleTests.cpp:1-8`, `Fna3dEffectStateOracleTests.cpp`, `Fna3dCompiledEffectTests.cpp:362`, and referenced by the EasyGL/SDL_GPU/OpenGL4 compiled-effect tests. Pixel comparison uses a +/-3 channel tolerance (`modules/renderers/fna3d/tests/CNA/Internal/Renderers/Fna3d/Fna3dEffectPixelOracleTests.cpp:46`). This is the only committed *FNA-executed rendering* evidence; it is compiled-effect (`.fxb`) only, 8x8 flat-input pixels, not sprites/3D scenes.
- So the honest statement is: "value diffs (enums, state presets, packed vectors, viewport) against a running FNA build - manual; plus FNA-recorded compiled-effect reflection/state/pixel fixtures replayed by CNA tests". It is not an automated regression gate and not scene rendering.

### F7. New verification infrastructure since BASE (all [V] unless tagged)
1. **XNA Content Pipeline oracle** (`tools/xna-pipeline-oracle/`, 113 files; `tests/reference/xna40/`, 566 files, 7.0 MB): genuine XNA GS 4.0 Refresh assemblies run under Wine .NET 4.0 dump the pipeline API (`content-pipeline-api.json`, counts: 128 public types, 708 public/protected members, 10 importers, 12 processors, 47 processor properties, 18 extensions) and behavior oracles (graphics, framework packing, intermediate XML, model, media, audio, optimize, differential). `tests/reference/xna40/differential/differential-oracle.json` holds **152** recorded cases (`plans/plan_xnapipeline_parity.md:1058` [R] quotes an earlier 112). Gates in `cmake/XnaPipelineParityGates.cmake` (14 `add_test`), driven by `parity_report.py --check` and `inputs_matrix.py check`. Report `docs/xna-content-pipeline-parity-report.md` (see Coverage reports).
2. **XNA sample-asset sweep** (`tools/xna-sample-sweep/`, `plans/plan_xna_sample_xnb_sweep.md`) [R]: real Microsoft-pipeline `.xnb` files from public XNA samples vs CNA's pipeline output. Numbers in "Samples evidence" below. The corpus lives outside the repo (`/rv/tmp/samples`).
3. **Six real-XNA behaviour probes** (`spikes/xna-{diffuse-color-clamp,envmap-amount-clamp,multisample-antialias,pixel-center,spritebatch-sampler0,vertex-color-specular}-spike/`, C# under Wine): none existed at BASE (`BASE:spikes/` does not exist; BASE had `dx*-spike` dirs).
4. **Shared cross-renderer parity fixtures** (`modules/graphics/examples/parity/`, `docs/cross-renderer-parity-fixtures.md`): **32 renderer-neutral fixtures** (`ParityFixtures.cmake` list, `parity_*.cpp` count 32; BASE: 0). Each fixture states its expected result itself (`Expect*` assertions) and is registered as `<Renderer>_Parity_<fixture>` for every renderer that calls `cna_register_parity_fixtures()`: **EasyGL** (`easygl/examples/CMakeLists.txt:2738`), **WebGPU** (`:1081`), **SDL_GPU** (`sdl-gpu/examples/CMakeLists.txt:93`) and **OpenGL4** (`opengl4/examples/CMakeLists.txt:216`) - the doc at `docs/cross-renderer-parity-fixtures.md:32-34` lists only three and its "Current fixtures" table lists 13 of the 32 [STALE]. Oracle = the fixture's own assertions, not real XNA (the doc says so, `:60-66`); the whole-frame `cna_diag_compare` cross-check needs two builds (`scripts/run-parity-fixture.sh`, `run-parity-corpus.sh`).
5. **GPU test isolation** (`plans/plan_gpu_test_isolation.md`, GTI-0001..0010 all done): `cmake/TestDisplayPolicy.cmake:1-30` (CNA_TEST_DISPLAY empty by default; live desktop `:0` opt-in only; Wayland guard), `scripts/check_test_display_isolation.py` (checks `ctest --show-only=json-v1` of a configured tree; registered as CTest `CnaTestDisplayIsolation`, `cmake/Tests/ModuleProbes.cmake:711`), `tools/platform/run_gpu_tests_private.sh` (private Weston + rootful Xwayland with DRI3), `tools/platform/profile_dead_tests.py`. Doc comment: "~990 registrations" carried `DISPLAY=`.
6. **Bounded-memory GoogleTest runner** `tools/tests/run_gtest_bounded.sh` (PSG-0002, commit `5404e22eb`, 2026-09-23): shards a gtest binary (default 200 tests/shard, `--max-parallel`), reports a signal-killed shard as KILLED and fails; header `:10-15` [R] says CnaTests had 10,564 tests on WEBGPU and could not run in one process (peak RSS 1,115 MB per 200 tests on WEBGPU vs 167 MB on Vulkan).
7. **Focused per-module test executables**: `cmake/UnitTests.cmake:439-460` names 22 focused targets (`CnaAudioTests`, `CnaContentTests`, `CnaContentPipelineTests`, `CnaCoreTests`, `CnaDesignTests`, `CnaDiagnosticsTests`, `CnaDevicesTests`, `CnaDevicesExtTests`, `CnaGamerServicesTests`, `CnaGraphicsTests`, `CnaGraphicsExtTests`, `CnaInputModuleTests`, `CnaInspectorTests`, `CnaIntegrationTests`, `CnaMathTests`, `CnaMediaTests`, `CnaNetTests`, `CnaPhoneTests`, `CnaPlatformModuleTests`, `CnaRendererTests`, `CnaRuntimeTests`, `CnaStorageTests`) plus the aggregate `CnaTests` (`:478`). At BASE there was only `CnaTests`. Sources are collected by `file(GLOB_RECURSE)` (`UnitTests.cmake:39-46`) then filtered by platform/renderer/option conditionals (`:60-140`), which is why static counts cannot equal a CTest count.
8. **Static policy gates registered as CTests**: 50 `add_test` in `cmake/Tests/ModuleProbes.cmake` (module link-closure, renderer identity registry, retired-renderer refusal, runtime-renderer discipline, renderer combinations, shader-package reproducibility, C-API gates, display isolation ...), CNAEXT guard/matrix/naming/nodiscard/doxygen checks (`modules/graphics-ext/examples/CMakeLists.txt:249-329`), provenance gate (`cmake/XnaPipelineParityGates.cmake:136-147`; `tools/provenance/`). Python unit tests: 55 `def test_`/`class Test` in 4 files (BASE: 4 in 1 file) - `tools/c-api/test_coverage_scope.py` 29, `tools/test_audit_xna_runtime_surface.py` 21, `tools/gltf_fixtures/test_validator.py` 4, `tools/xna-pipeline-oracle/final_audit.py` 1.
9. **Native desktop validation harnesses** (standalone programs, not gtest): `tools/platform/x11_desktop_validation/`, `wayland_desktop_validation/`, `win32_*.ps1`, `windows_vm_*.sh`; `docs/testing-x11-desktop.md`, `docs/testing-win32-native.md`.
10. **glTF conformance corpora - unchanged since BASE** (reports and goldens byte-identical apart from one wording change in `docs/gltf-l7-corpus-report.json`): see below.

### F8. glTF conformance corpora (unchanged BASE -> TARGET) [V on files, R on outcomes]
- `tests/assets/gltf/manifest.json`: `distinctAssetCount` 148 (15 owning groups: container 8, accessors 13, component-types 8, topology 8, normals 8, transforms 17, materials 14, textures 10, skinning 17, animation 23, cameras 5, lights 2, scenes 3, draco 4, robustness 8). Same at BASE.
- L7 (rendered pixels) reports, each `assets` = 148 = **140 `capture` + 8 `reject`** (safe rejections): `docs/gltf-l7-corpus-report.json` (OPENGLES3/EasyGL on Mesa llvmpipe), `docs/gltf-l7-vulkan-corpus-report.json` (VULKAN on lavapipe), `docs/gltf-l7-software-corpus-report.json` (SOFTWARE), `docs/gltf-l7-directx11-report.json` (DIRECTX11 via DXVK 2.6.0 under Wine); each has **140 PNG goldens** in `tests/gltf-l7/{easygl,vulkan,software,directx11}/`. `capture.processesPerAsset` = 2, resolution 512x512, RGB and alpha tolerance 0, **renderer-owned goldens** ("no EasyGL image ... is reused", Vulkan/Software/DirectX11 `goldenComparison.justification`). This proves determinism/regression of each renderer against its own past output; it is **not** a comparison against a reference renderer.
- The independent reference comparison is separate and small: `docs/gltf-reference-comparison.json` (KhronosGroup/glTF-Sample-Renderer commit `863b981fb755359063e370ff7b6e956bda0716e2`, **13 assets**, mask-IoU / coverage / RGB-MAE thresholds, not exact) and `docs/gltf-viewer-retake-report.json` (14 gate rows, 15 capture cases, result "pass", 2026-08-14). `docs/gltf-l7-vulkan-materials-report.json` (14 `mat-*` fixtures) is explicitly "not a claim of whole-corpus Vulkan L7".
- CI: only the EasyGL/OPENGLES3 L7 job runs (`gltf-renderer-stride-ci.yml`, job `l7-corpus`) plus L0-L6 + stride conformance on STUB, HEADLESS, OPENGLES3, VULKAN, SOFTWARE (matrix `renderer`, `gltf-renderer-stride-ci.yml:34`; `l7-corpus` job `:115`). The `l7-corpus` job builds a pinned external viewer (`openeggbert/cna-gltf-viewer` at `f32d1f136c74ed1508d4887952bf5a7a3d3b8b40`, `gltf-renderer-stride-ci.yml:135-137`) with `-DCNA_GRAPHICS_RENDERER=OPENGLES3` and runs ctest `CnaGltfConformanceL7` under Xvfb (`:166-168`); the L7 harness therefore lives partly outside this repository. Vulkan, Software and DirectX11 L7 sets are recorded, not CI-run.
- `docs/gltf-conformance.md:924-936` and `:1099-1112` say "146 canonical assets" in the Vulkan section and "148" elsewhere [STALE internal inconsistency]; the JSON says 148.

---

## Oracle & reference corpus (with denominators)

**What exists (reference corpus size)**
- `tools/xna-oracle/`: **46 scene files / 46 real-XNA PNGs** = 39 diff-corpus scenes + 7 null-texture measurement scenes; plus a **17-row** SurfaceFormat channel-expansion text table (`reference/format-expansion/xna-format-expansion.txt`).
- FNA-executed fixtures: 3 JSON files x 7 compiled effects (`tests/fixtures/compiled-effects/`).
- Content Pipeline: XNA-produced inventory of 128 types / 708 members and a 152-case differential JSON (`tests/reference/xna40/`); [R] 7,726 genuine XNA-pipeline `.xnb` references outside the repo.

**Campaign denominators (what a run actually compares)**
- Whole diff corpus: **39** scenes x 65,536 px, tolerance 0 (D3D9 gate `D3D9_XNA_Diff`; measurement scripts for FNA3D, Software, EasyGL, multi-renderer).
- Cross-renderer *gated* subset: **2** scenes (`colored_linelist_quad`, `colored_linestrip_quad`) on EasyGL and on Software.
- Null-texture: 7 scenes, consumed as hard-coded centre-pixel expectations on 8 renderers.
- glTF L7: 148 assets = 140 captured + 8 refused, per renderer, self-golden. Khronos reference subset: 13.

**Renderer vs host vs tolerance (do not merge)**
- Reference images: genuine Microsoft XNA 4.0 runtime, Wine + DXVK 2.6 (D3D9 -> Vulkan), AMD Radeon 780M / RADV, Linux; not real Windows.
- "Pixel-exact" (tolerance 0, all RGBA channels, all 65,536 px, all 39 scenes) is recorded for **DIRECTX9 only**, executed through the same Wine+DXVK stack. It is a statement about DIRECTX9-over-DXVK, not about D3D9 on native Windows hardware/drivers.
- No other renderer is held to that bar. EasyGL and SOFTWARE have a 2-scene exact gate; FNA3D's CTest gates only that scenes render.
- Recorded whole-corpus tolerance-0 results (measurements, dated): SOFTWARE 18/39 (2026-09-11), FNA3D 10/39 and EasyGL 10/39 (2026-08-11, pre-fix), OPEN[retired] 11/39 (retired).

**Honest current sentence for the website (drop-in)**
> CNA keeps 39 renderer-neutral test scenes (256x256, HiDef) with reference images captured by running the genuine Microsoft XNA 4.0 runtime under Wine with DXVK on Linux; a further 7 unbound-texture scenes and a 17-format channel-expansion table were measured the same way. CNA's `DIRECTX9` renderer, run through the same Wine+DXVK stack, is recorded as matching all 39 at zero tolerance (CTest `D3D9_XNA_Diff`; the last dated report, `docs/d3d9-divergence-report.md`, covers the first 31 scenes, and the run has not been repeated on native Windows). No other renderer is held to pixel-exactness: `EasyGL` and `Software` are gated only on two line scenes, and whole-corpus results for the others are measurements (Software: 18 of 39 byte-exact, 30 within one channel value). None of this runs in CI.

**Cross-renderer parity fixtures** (F7.4): 32 fixtures, 4 registering renderers, oracle = fixture assertions; up to 32 CTests per registering renderer (`<Renderer>_Parity_<name>`), subject to that renderer's build. Tolerance convention `docs/cross-renderer-parity-fixtures.md:67-95` (interior sampling, 0-2 for flat colour, `kShadingTolerance` for shaded).

**D3D9 divergence report / FNA3D parity report**: both are dated measurements; the D3D9 report is at 31 scenes and lists six project-wide XNA divergences (`PreferPerPixelLighting` etc.) whose later fixes (`NEXT.md:6560+`, plan rows D9-81) are not reflected in it; do not quote its "Not yet measured" table as current.

---

## Test inventory (BASE vs TARGET, same method)

**Method** - the BASE figures (568 / 8,263 / 539) come from the site's own published commands (`docs/verification.html:401-410`, "Reproducing these numbers yourself"), run from the exact checkout with ripgrep:
```bash
# files: CNA-owned .cpp under a test/ or tests/ path component, third_party excluded
rg --files -g '*.cpp' -g '!third_party/**' | awk '$0 ~ /(^|\/)(test|tests)(\/|$)/' | wc -l
# static definitions: TEST, TEST_F, TEST_P, TYPED_TEST, TYPED_TEST_P at line start, all .cpp, third_party excluded
rg -n '^\s*(TEST|TEST_F|TEST_P|TYPED_TEST|TYPED_TEST_P)\s*\(' -g '*.cpp' -g '!third_party/**' | wc -l
# files containing at least one such macro
rg -l '^\s*(TEST|TEST_F|TEST_P|TYPED_TEST|TYPED_TEST_P)\s*\(' -g '*.cpp' -g '!third_party/**' | wc -l
```
I recomputed BASE with these exact commands: **568 / 8,263 / 539 - exact reproduction** of the alpha.1 site figures. Results are identical with `--no-ignore --hidden`. Every one of the definitions lies inside a test-path file (0 definitions outside), so the two commands are consistent. `TYPED_TEST*` matches: 0 in both trees. The vendored `vendor/googletest` submodule is empty in these worktrees; its own tests are `.cc`, which the `*.cpp` glob would not count in any case.

| Quantity | BASE (`1bb2145d9`) | TARGET (`009d40f5d`) | Delta |
|---|---:|---:|---:|
| C++ test source files (`*.cpp` in `test(s)/` paths) | **568** | **904** | +336 (+59%) |
| ...of which contain >=1 counted macro | 539 | **871** | +332 |
| Static GoogleTest-family definitions | **8,263** | **12,610** | +4,347 (+52.6%) |
| `TEST` / `TEST_F` / `TEST_P` | 6,299 / 1,925 / 39 | 9,718 / 2,778 / 114 | |
| All non-vendored `.cpp` files (context) | 2,557 | 2,878 | |
| `INSTANTIATE_*_P` lines (parameterisation exists; instantiated cases > static defs) | - | 84 | |
| Python unit-test defs (`def test_`/`class Test`) | 4 (1 file) | 55 (4 files) | |
| `cmake -P` script cases under `cmake/Tests/` | 5 entries | 11 entries | |
| `.c` files under `tests/` (C-API consumer tests, not counted above) | 74 | 85 | |

Blind spots of the method (state them, do not hide them):
- **Standalone example/pixel test programs are not counted.** Files named `*_test.cpp` under `examples/`: BASE 1,232 -> TARGET **879** (renderer readback/pixel programs with their own `main()`, registered through `cna_register_renderer_test`; the drop reflects the 25 retired renderers). They are the bulk of "GPU pixel-readback tests" and are absent from 568/904.
- Files under `modules/c-api/tests` (BASE 79 C/C++ files, TARGET 92) have their own `main()` and are excluded from `CnaTests` (`cmake/UnitTests.cmake:60`).
- Static definitions are not executed cases: conditionals, `INSTANTIATE_*`, renderer/platform filters and CMake source filters (`UnitTests.cmake:60-140`) change the instantiated set.

**Per-module split (test-path files / static definitions), top 10 by TARGET definitions**
| Module | BASE files | BASE defs | TARGET files | TARGET defs | Delta defs |
|---|---:|---:|---:|---:|---:|
| `modules/graphics` | 105 | 2,278 | 161 | 2,906 | +628 |
| `modules/content` | 112 | 977 | 170 | 1,871 | +894 |
| `modules/platform` | 36 | 443 | 85 | 1,208 | +765 |
| `modules/renderers` (all families) | 69 | 883 | 69 | 1,050 | +167 |
| `modules/graphics-ext` | 3 | 24 | 92 | 967 | +943 |
| `modules/math` | 22 | 820 | 27 | 873 | +53 |
| `modules/audio` | 31 | 666 | 38 | 765 | +99 |
| `modules/input` | 43 | 490 | 47 | 523 | +33 |
| `modules/content-pipeline` (new module) | 0 | 0 | 47 | 487 | +487 |
| `modules/devices` | 26 | 468 | 27 | 474 | +6 |
Next: gamer-services 382, net 316, media 304 (BASE 286), runtime 185, core 106, devices-ext 56, diagnostics 40, inspector 27, design 25, phone 18, storage 14 (BASE 5), canvas renderer 17 (unchanged), top-level `tests/` 13. Sum check: 12,610. (Some tests moved between `graphics` and `graphics-ext`; compare their sum, 2,302 -> 3,873.) The site's BASE-cited spot figures (Media 286, Storage 5, Canvas 17) reproduce exactly, which independently confirms the method.

**CTest registrations - not derivable statically; do not publish a total.** Reasons: `gtest_discover_tests(... PRE_TEST)` at build time (`cmake/UnitTests.cmake:1340-1346`); renderer-selected conditionals; `foreach` registration (32 parity fixtures x renderer via `cna_register_parity_fixtures`); option-gated example targets. Static call-site counts, for orientation only: `cna_register_renderer_test(` call lines BASE 1,731 -> TARGET 1,492 (easygl 307 -> 356, vulkan 214 -> 385, software 60 -> 154, sdl-gpu 85 -> 135, webgpu 82 -> 115; the total falls because [retired] etc. were removed); plain `add_test(` BASE 139 -> TARGET 203. Not a CTest count.

**CNA-recorded executed results (all [R], dated, cannot be reproduced here)**
- `docs/cnaext-coverage.md:15-21` (2026-08-18): whole `CnaTests` on OPENGLES3 + CNAEXT, Xvfb+llvmpipe: **7,940 ran, 7,876 pass, 64 skip, 0 fail**.
- `docs/software-easygl-parity-ledger.md:20-30` (2026-09-13): Software `CnaGraphicsTests` **2,640/2,688** (48 classified skips), Software label **160/160**; EasyGL `CnaGraphicsTests` 2,635/2,688 (53 skips), EasyGL compiled-effect family 679/679; five known non-renderer `CnaTests` failures stated.
- `plans/plan_vulkan.md:636-645` (2026-09-06, VULKAN campaign): full ctest in a Vulkan configuration **9,101/9,117** (`VULKAN-407`), 9,093/9,117 (`VULKAN-408`), of which `^Vulkan_` 256/256; 16 named standing failures, several audio-timing flakes that pass alone.
- `plans/plan_xna_sample_xnb_sweep.md:679-694` (2026-09-11): `CnaContentPipelineTests` 481/481; `CnaContentTests` 1,806 run, 1,792 pass, 9 skip, 5 fail (HEADLESS cube/3D texture); `CnaMathTests` 850/850; `CnaGraphicsTests` 2,345 run, 2,101 pass, 243 skip, 1 fail (HEADLESS readback).
- `plans/baselines/easygl-ctests-2026-09-06.txt`: a recorded `ctest -N -R '^EasyGL_'` list, **322** test names at that date.
- These are per-configuration and per-date; there is still no universal pass count. The site's "no pass rate" rule stands; if any is shown it must carry configuration, date and "CNA-recorded".

---

## CI as verification evidence

**Count**: TARGET `.github/workflows/` = **20** files, **28** jobs (BASE: 21 files, 24 jobs). Removed: `[retired]-ci.yml`, `[retired]-cross-platform-ci.yml` (renderers retired). Added: `content-pipeline-windows-ci.yml` (`git diff --name-status`). 17 of 20 trigger automatically on `push`/`pull_request` to `next, develop, main`; `d3d-windows-ci.yml` and `gdi-windows-ci.yml` are `workflow_dispatch` only; `content-pipeline-windows-ci.yml` triggers on push to branch `content-pipeline-final` + dispatch (so not on main lines). No Android workflow. No workflow runs the XNA oracle corpus, the FNA harness, the parity-fixture CTests for WebGPU/SDL_GPU/OpenGL4, or the Vulkan/Software/DirectX11 glTF L7 sets.

| Workflow | Trigger | What it establishes |
|---|---|---|
| `32bit-arithmetic-ci.yml` | push/PR (path-filtered) + dispatch | i386 build+run of width-dependent bounds checks (AudioTagParser, SoftwareFramebuffer/Texture); `tools/media/arithmetic32bit/` only |
| `apple-ci.yml` | push/PR + dispatch | Apple CMake layer check (Linux), macOS-14 build + portable tests, iOS device final-link, iOS simulator launch of one frame; no physical device |
| `c-api-abi-baseline.yml` | push/PR (path-filtered) | header half of ABI layout/export baseline (build-free) |
| `c-api-compat-matrix.yml` | same | every public C header through each installed C toolchain (build-free) |
| `c-api-coverage-gate.yml` | same | C API coverage inventory current (build-free) |
| `c-api-limitations.yml` | same | limitations matrix consistency (build-free) |
| `c-api-release-gate.yml` | same | release-gate declaration vs measurement; header comment: gate "currently reports NOT READY"; `docs/c-api/RELEASE_GATE.md:11` "Not ready. 1 criteria are unmet" (468 unmapped symbols) |
| `content-pipeline-windows-ci.yml` | push on `content-pipeline-final` + dispatch | native MSVC build and CPU/CLI gate of the build-time content pipeline (HEADLESS, no device tests) |
| `d3d-windows-ci.yml` | dispatch only | native MSVC, matrix `renderer` = DIRECTX11, DIRECTX12, DIRECT2D (no DIRECTX9) |
| `devices-tests.yml` | push/PR + dispatch | Devices/Sensors gtest suite + `cna_strict_xna_api_check` (UBSan preset) |
| `emscripten-multi-renderer-ci.yml` | push/PR | WEBGL2+CANVAS+HTML_DOM+SVG_DOM link into one wasm bundle; no browser run |
| `gdi-windows-ci.yml` | dispatch only | native MSVC GDI renderer correctness gate (hidden window) |
| `general-tests-ci.yml` | push/PR (4 path filters) | unfiltered `ctest` on OPENGLES3 under Xvfb `:99`; configure line now `-DCNA_GRAPHICS_RENDERER=OPENGLES3` (`:139`), so the alpha.1 `EASYGL` defect is fixed; `KNOWN_FAILURES` allowlist has **1** entry (`EasyGL_GraphicsDevice_ReferenceStencil`) |
| `gltf-renderer-stride-ci.yml` | push/PR | L0-L6 + stride conformance on STUB/HEADLESS/OPENGLES3/VULKAN/SOFTWARE; job `l7-corpus` runs EasyGL L7 goldens (installs `python3-pil`) |
| `gltf-sanitizers-ci.yml` | push/PR | glTF import under ASan+UBSan, matrix `draco` on/off, STUB renderer |
| `htmldom-ci.yml` | push/PR | HTML_DOM browser suite in headless Chromium |
| `input-ci.yml` | push/PR | input suite, matrix of 4: OPENGLES3, ASan+UBSan on OPENGLES3, SDL_RENDERER, VULKAN (`EASYGL` rows gone) |
| `metal-macos-ci.yml` | push/PR | native Metal renderer, macOS-14, supported contract tests |
| `multi-renderer-ci.yml` | push/PR | HEADLESS;SOFTWARE;STUB multi-renderer set + single HEADLESS control build |
| `platform-ci.yml` | push/PR | **6 jobs** (BASE: 1): contract matrix of 6 (SDL3/SDL2/Vulkan/Software/Headless/Terminal), `win32-cross` (MinGW cross-build **executed under Wine**, automatic), `win32-native` (dispatch-only), `x11-sdl-free`, `x11-sdl-free-gpu`, `sdl-enable-matrix` |

Notes: `platform-ci.yml` `win32-cross` is an automatic Wine-executed lane for the platform harness (not renderers) - this contradicts the site's "no automatic MinGW/Wine lane". The `-Werror` "CNAEXT purity" check is run in `devices-tests.yml` for Devices/Sensors only (see Corrections). CI does not establish a pass count for anything by itself; whether the current jobs are green was not verified.

---

## Coverage reports

| Report | Measures | Denominator / result | Caveat |
|---|---|---|---|
| `docs/xna-4-runtime-member-coverage.md` (+`.json`, baseline `.md/.json`) generated by `python3 tools/audit_xna_runtime_surface.py --write-reports` | **Representation** (declaration present in CNA public headers per Clang AST) of the **XNA 4.0 runtime documented API**. Census = Microsoft's runtime XML docs (10 XML files, listed `tools/audit_xna_runtime_surface.py:29-40`) + matching Microsoft DLL metadata; Content Pipeline XML excluded. | Types **331/331** (13 in `Design`, 331 = 329 + 2 because generic and non-generic `ContentTypeReader`/`IPackedVector` count separately). **3,627/3,627** = 253 constructors + 1,518 methods + 1,040 properties + 753 fields + 63 events (operators 145, indexers 29, enum values 661 are subsets inside those). Classification: EXACT_EQUIVALENT 1,746, SEMANTIC_EQUIVALENT 1,823, HOST_LANGUAGE_SUBSTITUTION 58, MISSING 0, NOT_APPLICABLE 0, NEEDS_REVIEW 0. Pre-fix baseline 3,463/3,627 (95.48%). Closure commit `391279c50` 2026-09-21. | "API representation does not establish behavior" (`:5`). Inputs (`/rv/data/.../xna4-decomp/dlls`) are outside the repo, so the number is reproducible only with the Microsoft files (SHA-256s recorded in the JSON). 1,039/1,040 properties are SEMANTIC because C++ spells them `getXProperty()`. |
| `docs/coverage.md:1-9`, `docs/xna-4-api-coverage.md:1-12` | historical snapshots | still print **3,467/3,627 (95.59%)** and "160 gaps" | **[STALE]**: contradict the generated report above; never quote them. `docs/coverage.md` itself says "not a current API census". |
| `docs/xna-content-pipeline-parity-report.md:9-27` (generated by `tools/xna-pipeline-oracle/parity_report.py` from `tests/reference/xna40/content-pipeline-api.json` + `content-pipeline-parity-map.json`) | Representation of the **XNA GS 4.0 Content Pipeline API** (build-time) | types **128/128**, members **705/705** (708 inventoried minus 3 delegate-plumbing members not counted), enum values 27/27, importers 10/10, processors 12/12, processor properties 47/47, source extensions IMPLEMENTED+TESTED 18/18. Type status: EXACT 44, SEMANTIC 79, HOST_SUBSTITUTION 5; member status: EXACT 457, SEMANTIC 237, HOST_SUBSTITUTION 11 | Many notes cite oracle measurements (`tests/reference/xna40/...`), but the percentage itself is representation. CNA loads XNB at runtime; this pipeline is a build-time tool ("CNA loads but does not author XNB" needs rewording: CNA now has a build-time content pipeline, `modules/content-pipeline`, not in the runtime link closure). |
| `docs/c-api/COVERAGE.md:15` (generated by `tools/c-api/generate_coverage_inventory.py`, gate `CApiCoverageMatrix` + `c-api-coverage-gate.yml`) | Mapping of **CNA's own** public C++ declarations to C ABI rows | 556 headers, **9,355 symbols: 8,363 implemented, 15 partial, 468 planned, 509 not applicable**; 425 headers excluded (Internal/Detail); out-of-scope modules: content-pipeline 107 headers, phone 9, platform 27, renderers 138. Release gate `docs/c-api/RELEASE_GATE.md:5-11`: ABI **0.29.0** experimental, "Not ready", 9 of 10 criteria met (only "No public C++ symbol is unaccounted for" unmet: 468). ABI baseline: 221 struct layouts, 4,055 exported symbols; compatibility matrix 23 cells / 7 toolchains | A symbol counted "implemented" is a mapped route, not a behavior test. BASE figures were 59 headers/2,861 routes/6,712 rows/ABI 0.7.0 - not comparable. |
| `docs/cnaext-coverage.md:11-21` (2026-08-18, hand-recorded from a `--coverage` GCC 13 build) | **Line/function/branch coverage** of `modules/graphics-ext` only | lines 94.2% (2,822/2,997), functions 97.8% (523/535), branches 57.5% (2,218/3,859) under 7,940 ran/7,876 pass/64 skip | Single module, dated snapshot, "not regenerated automatically". |
| `docs/gdm-coverage.md` (last updated 2026-06-27, Task 230) | one class, `GraphicsDeviceManager`, vs FNA | crude grep of status marks: 29 supported / 7 partial / 1 missing / 1 CNAEXT (includes legend lines) | Qualitative per-member table; not a percentage of anything; do not publish these counts. |
| `docs/devices-api-coverage.md` (re-verified 2026-07-06) | `Microsoft::Devices` + `Sensors` per-member table vs MSDN pages | crude grep: 72 table rows beginning with a backticked member, 30 of them marked Real; the file itself states "zero Missing and zero Extra-unmarked" at that date | one namespace, dated; the row counts are my line greps, not a published denominator. |
| `docs/graphics-compatibility-report.md:1-12` | 2026-07-09 milestone pass-rates | - | **[STALE]** by its own banner ("Do not treat the percentages ... as current"). |
| `docs/gltf-conformance.md` layers L1-L7 | see F8 | - | - |

### Samples evidence recorded inside CNA (all UNTRUSTED; the authoritative source is the external cna-samples repository)
- CNA records **no** "N of M XNA samples ported/verified" number at TARGET (`rg` across `README.md`, `docs/`, `plans/`, `CHANGELOG.md`). The only historical sample count is `plans/plan_graphics.md:787` "88 samples ported, 24 still placeholder" (2026-07-10, quoting `../cna-samples/DEFERRED.md`), which does not match the site's "63 of 86" either. So 63/86 cannot be confirmed or refuted from CNA; another fact sheet owns it.
- What CNA does record (different subject: content pipeline vs real sample assets), `plans/plan_xna_sample_xnb_sweep.md`: `/rv/tmp/samples` holds 157 per-sample artefact roots (`:31-32`); **7,726** genuine Microsoft-pipeline reference `.xnb` in **129 samples** across **433 build units**, 5,277 distinct contents (`:391-405`); run 66 (2026-09-11): **4,337 byte-identical, 747 semantically identical, 815 accepted differences (each proved by `accepted_audit.py`), 1,797 need a sample-defined pipeline component, 9 environment gaps, 21 references no longer present, 0 unexplained** (`:588-606`, `:889-905`); 4,337/7,726 = 56.1% byte-for-byte. Only 260 of 433 build units finished in the earlier table (`:427-435`). The corpus is outside the repo and not reproducible from a clone.
- `git log` shows 52 distinct `SAMPLE-###` task ids (up to SAMPLE-152) in commit subjects, **all after BASE** (0 before); 110 commits mention them. They are framework fixes found by porting, not a ported-sample count.

---

## Corrections to existing site claims

Legend: page -> old claim -> TARGET truth -> evidence.

**docs/verification.html**
1. Table row "XNA 4.0 oracle corpus ... **39 scenes** under tools/xna-oracle/, with reference PNGs captured from real XNA" (`:146-149`) -> keep "39 scenes" and add: 39 diff-corpus scenes/PNGs + 7 null-texture scenes/PNGs + 17-format table; all references from the real XNA 4.0 runtime under Wine+DXVK on Linux (not Windows). (F2, F3.)
2. `:206` "39 reference PNGs captured from real XNA 4.0 running under Wine + DXVK. CNA renders the same scenes and the images are diffed byte for byte." -> correct for DIRECTX9; say "recorded as matching all 39 at tolerance 0 through the same Wine+DXVK stack; no committed dated 39-scene report (last report covers 31); not run in CI". (F4, F5.)
3. `:211-218` renderer table "DIRECTX9 39/39; OPEN[retired] 11/39; EasyGL 10/39; FNA3D 10/39" -> **delete the OPEN[retired] row (renderer retired 2026-09-17)**; label the EasyGL/FNA3D rows "measurement, 2026-08-11, tolerance 0, Mesa llvmpipe, before later EasyGL pixel-center/clip-depth fixes"; add SOFTWARE **18/39 byte-exact, 30/39 within one channel value** (2026-09-11) and state that EasyGL and SOFTWARE are exact-gated on 2 line scenes only. Alternative: drop per-renderer numbers except DIRECTX9 and describe the others qualitatively. (F5.)
4. `:224` "Every other renderer is held to a 'looks right' bar" -> true in effect; more precisely "measured against the corpus, not gated (except two line scenes on EasyGL and Software; FNA3D gates only that scenes render)". (F4.)
5. `:227` "The corpus covers 39 scenes, not the API" -> keep.
6. `:299` "the project's most rigorous check is not automated" -> still true: `D3D9_XNA_Diff` is a CTest but only in a DIRECTX9+Wine cross-build tree and in no workflow. (F4.)
7. `:138`, `:175` "568 CNA-owned C++ files ... 539 ... **8,263**" -> **904 / 871 / 12,610** (same commands, TARGET). Add the blind spot: 879 standalone `examples/**/*_test.cpp` pixel programs are not counted. (Test inventory.)
8. `:152-153` "A harness links a *real, running* FNA build ..." -> keep, add "manual, not a CTest, not in CI; covers enums, state presets, PackedVector, Viewport"; add FNA-recorded compiled-effect fixtures (reflection/state/pixels, 7 effects, replayed by CTest gtests). (F6.)
9. `:157-158` "compile-time signature-freeze tests pin the public API" and `tools/devices/StrictXnaApiSurfaceCheck.cpp` -> **overstated**: there is exactly **one** signature-freeze test file (`modules/input/tests/.../PublicApiInputSignatureFreezeTests.cpp`, 56 `static_assert`s); the strict-mode compile check covers **only** `Microsoft::Devices`/`Sensors` (`tools/devices/StrictXnaApiSurfaceCheck.cpp:32-...`, `cmake/Harnesses.cmake:186-238`, run by `devices-tests.yml`). `CNA_STRICT_XNA_API` turns `CNAEXT` into `[[deprecated]]` library-wide (`modules/core/include/CNA/CNAHelper.hpp:14-25`), but no target compiles the whole XNA surface under it. The C API has its own ABI baseline (221 layouts, 4,055 exports). (F7.)
10. `:270` "**21 workflow files**" -> **20 workflow files, 28 jobs**; `:270-291` the EASYGL breakage and "C API final target is compile-blocked" text is alpha.1-specific: `general-tests-ci.yml:139` and `input-ci.yml` no longer use `EASYGL`; C API status must be re-read from the C-API fact sheet (static: the 25-row renderer map now equals the 25 canonical identities). Add: `platform-ci.yml` runs an automatic Wine-executed Win32 lane; remove "no automatic MinGW/Wine lane". (CI section.)
11. `:296` "Storage ... five test macros, and StorageContainer has none" -> Storage module has **14** macros; four tests exercise `StorageContainer` path containment (`modules/storage/tests/Microsoft/Xna/Framework/Storage/StorageDeviceTests.cpp:125-185`), `StorageSmoke.c` covers it from C. Still no save/load round-trip semantics test in the module; say "path-safety tested, not read/write semantics". (Test inventory.)
12. `:191` "50 renderer identities across 46 implementation families" -> **25 identities / 21 families** (F1; owned by the renderer fact sheet).
13. `:442` configure presets list -> TARGET has 18 configure presets (`CMakePresets.json`); owned by the build fact sheet.
14. Add a subsection or table row for: content-pipeline oracle, sample-asset sweep [R], parity fixtures, glTF corpora, GPU-test isolation and bounded runner, coverage generators. (F7, F8.)

**showcase.html - "Verification against the real XNA runtime" (MUST be preserved; corrected claims)**
- "39 scenes under tools/xna-oracle/, rendered by a real C#/XNA reference renderer and diffed against CNA's DIRECTX9 output at --tolerance 0" -> "**39 scenes** (256x256), reference images from the **genuine Microsoft XNA 4.0 runtime under Wine + DXVK** (`Oracle.cs`), compared with CNA's `DIRECTX9` renderer output at `--tolerance 0` (every RGBA channel of every one of 65,536 pixels per scene); recorded as matching all 39 through the same Wine+DXVK path; not run in CI; not yet repeated on native Windows".
- "This is the strongest correctness claim on the site: ... byte-identical to what the original runtime produced" -> qualify: "byte-identical to the original runtime as executed under Wine+DXVK on the reference machine, for these 39 scenes only".
- "The DIRECTX9 renderer exists largely to make this comparison possible - it uniquely targets pixel-exact XNA 4.0 authenticity" -> keep "targets", but note the EasyGL/Software 2-scene exact gate and Software's 18/39 measurement.
- "A real running FNA build lives under tools/fna-reference/ and dumps its observable behaviour as JSON ... diffs the two" -> accurate; add "manual; value-level (enums, presets, packed vectors, viewport) plus recorded compiled-effect fixtures".
- "Four of the 39 scenes" (images) -> images are current (byte-identical to TARGET references). Optionally add: 7 unbound-texture scenes exist at `tools/xna-oracle/reference/null-texture/`.
- `:104` note "alpha.1 contains 21 workflow files ... C API final target is compile-blocked ... Windows D3D/GDI lanes remain manual" -> 20 workflows; D3D/GDI still manual; re-check C API wording; Wine-executed Win32 platform lane is automatic.

**index.html**
- Card "Verified Against Real XNA" (`:220-221`): "39-scene oracle corpus ... diffed pixel-exactly against CNA's DIRECTX9 output at zero tolerance, alongside differential testing against a running FNA build" -> keep with the qualifiers above (Wine+DXVK, DIRECTX9 only, manual FNA harness); "63 of the 86 official XNA samples build" -> not verifiable in CNA (external repo; CNA's own note says "88 ported / 24 placeholder" at 2026-07-10).
- Quick Stats (`:139-141`): "8,263 Static test definitions / 568 sources / 539" -> **12,610 / 904 / 871**; "63 / 86 XNA samples ported" -> (external); "21 CI workflow files" -> **20**; the hover text "the intended full-suite job and two Input rows have a stale EASYGL configuration" is now false (fixed in `general-tests-ci.yml:139`, `input-ci.yml`).

**features.html**: "568 C++ test source files and 8,263 ..." -> 904 / 12,610; "21 GitHub Actions workflow files" and the EASYGL-broken sentence -> 20; remove EASYGL/C-API-blocked wording unless re-verified; "Windows-only; target of the pixel-exact XNA oracle corpus" (DIRECTX9) and "the 39-scene XNA oracle comparison at zero tolerance" -> add Wine+DXVK qualifier; "Renderer pixel programs, the XNA oracle and FNA differential checks cover separate compatibility questions" -> keep.

**about.html**: "568 C++ test files and 8,263 ..." (2 places) -> 904 / 12,610 (871 with macros); "21 workflow files" -> 20; "A real XNA reference renderer. ... genuine C#/XNA reference renderer" -> "genuine XNA 4.0 runtime under Wine+DXVK"; "A running FNA build ... Ground truth comes from executing the reference implementation" -> keep, add "manual".

**architecture.html**: tree shows `tests/` and `examples/` under each module - still true; no numeric verification claim found. Add the focused-target structure only if a build section wants it (22 focused test executables + `CnaTests`).

**roadmap.html / docs/roadmap.html**: "568 C++ test sources with 8,263" -> 904 / 12,610; "Pixel-exact verification against the real XNA runtime **Shipped** - 39 scenes ... alongside differential testing ... and a compile-time CNAEXT purity check that turns all **1,289** non-XNA declarations into [[deprecated]] warnings under -Werror" -> **remove "1,289"**: the number is not in CNA docs at BASE or TARGET and cannot be reproduced (a static count of `CNAEXT` tokens in public headers is 2,244 at BASE and 3,079 at TARGET, which counts markers, not distinct declarations); the `-Werror` compile check covers `Microsoft::Devices`/`Sensors` only (correction 9). "21 workflow files ... EASYGL ... 49-versus-50" -> 20 / fixed. "CNA covers the public XNA namespace surface except Framework.Design" -> `modules/design` now implements 13 Design types (`docs/xna-4-runtime-member-coverage.json`: Design 13; 25 static tests): all 331 documented runtime types are represented.

**docs/xna-compatibility.html**: "The whole module carries five test macros and StorageContainer has none, so treat its behaviour as read-not-run" (2 places) -> 14 macros, StorageContainer path-safety tests exist; "XNA namespace surface complete but for Framework.Design" -> complete including Design at the representation level (331/331 types, 3,627/3,627 members; representation, not behavior); "63 of 86 in-scope samples ported and building" -> external; "byte-exact verification of the DIRECTX9 renderer against the real XNA runtime" -> add Wine+DXVK qualifier.

**docs/faq.html**: "568 ... 8,263" -> 904 / 12,610; "The most rigorous check is the 39-scene XNA oracle corpus: ... DIRECTX9 matches all 39 at tolerance 0 ... other renderers match far fewer" -> keep with qualifiers (recorded, Wine+DXVK, not CI; other renderers are measured not gated; Software 18/39); "CNA's 21 workflows" (2 places) -> 20; "no automatic Wine workflow" -> `platform-ci.yml` has an automatic Wine-executed Win32 platform lane; renderer/D3D Wine validation is still manual; "Tests for the thin spots, above all Storage, whose module carries five test macros and whose StorageContainer has none" -> 14 macros / path-containment tests exist.

**contribute.html**: "568 / 8,263" (3 places) -> 904 / 12,610; "Alpha.1 has 21 workflow files" (2 places) -> 20; "Storage has only five ... Media has 286 and the Canvas renderer has 17" -> Storage 14, Media 304, Canvas 17.

**docs/tutorials/99-unit-testing.html**: "568 C++ test source files containing 8,263 ..." -> 904 / 12,610; the general-tests-ci paragraph ("distinguish four named known failures ... configure command still selects the removed EASYGL identity, so it fails before that suite runs. Two EasyGL rows in input-ci.yml have the same defect") -> the configure command now selects OPENGLES3 (`general-tests-ci.yml:139`); the allowlist has **1** named known failure (`:` `KNOWN_FAILURES=("EasyGL_GraphicsDevice_ReferenceStencil")`); input-ci rows are OPENGLES3, ASan+UBSan/OPENGLES3, SDL_RENDERER, VULKAN. Whether the job is green at TARGET was not verified.

**docs/tutorials/125-pixel-testing.html**: "39-scene XNA oracle corpus, captured from real XNA 4.0" -> keep (+ "under Wine+DXVK"); the renderer table (DIRECTX9 / OPEN[retired] / EasyGL / FNA3D) -> remove OPEN[retired], mark others as dated measurements, add SOFTWARE 18/39; "17 golden images" -> still **17** (`examples/golden/*.png`, unchanged); "568 ... 8,263 ... 21 workflow files" -> 904 / 12,610 / 20; "Oracle.cs, compiled against the genuine XNA 4.0 assemblies and run under Wine" -> correct; the tolerance/mutation-tested `xna-diff.py` paragraph -> still correct (`scripts/xna-diff.py`; README `:537-540`).

Also (not in your list but found): `docs/vs-alternatives.html`, `docs/building.html`, `docs/roadmap.html` carry 8,263/568 too (`rg -l 8,263`).

---

## Proposed current-facts values

(name -> value -> derivation -> evidence)

| Name | Value | Derivation | Evidence |
|---|---|---|---|
| `cna_test_source_files` | **904** | site command 1 (Test inventory) at TARGET | F-inventory; BASE 568 reproduced |
| `cna_test_sources_with_macros` | **871** | command 3 | BASE 539 |
| `cna_static_test_definitions` | **12,610** | command 2 | BASE 8,263 |
| `cna_static_defs_by_macro` | TEST 9,718; TEST_F 2,778; TEST_P 114 | per-macro tally | - |
| `cna_test_files_note` | "CNA-owned `*.cpp` under test/tests paths, vendored `third_party` excluded; static macro count, not executed cases; standalone `examples/**/*_test.cpp` pixel programs (879) are not included" | - | - |
| `cna_standalone_example_test_programs` | 879 (`*_test.cpp` under `examples/`; BASE 1,232) | `rg --files -g '*_test.cpp' -g '!third_party/**' \| rg '/examples/' \| wc -l` | file count, not CTest count |
| `cna_python_test_defs` | 55 in 4 files | `rg -c '^\s*(def test_\|class Test)' -g '*.py'` | - |
| `cna_focused_test_executables` | 22 + `CnaTests` aggregate | `cmake/UnitTests.cmake:439-460,478` | - |
| `cna_ctest_total` | **do not publish** | not statically derivable (`ctest --test-dir <build> -N` per configuration) | Test inventory |
| `cna_workflow_files` | **20** (28 jobs; 17 automatic on next/develop/main, 2 dispatch-only, 1 branch+dispatch) | `ls .github/workflows/*.yml \| wc -l`; job count from YAML | CI section |
| `cna_oracle_diff_scenes` | **39** (256x256, HiDef, 65,536 px each) | `ls tools/xna-oracle/scenes/*.scene \| wc -l` | F2 |
| `cna_oracle_reference_pngs_diff_corpus` | 39 | `ls tools/xna-oracle/reference/*.png \| wc -l` | F2 |
| `cna_oracle_null_texture_scenes` | 7 scenes + 7 PNGs (not in any diff denominator) | `ls tools/xna-oracle/scenes/null-texture/` | F2 |
| `cna_oracle_format_table_rows` | 17 SurfaceFormats | `grep -vc '^#' tools/xna-oracle/reference/format-expansion/xna-format-expansion.txt` | F2 |
| `cna_oracle_reference_host` | genuine Microsoft XNA 4.0 runtime, Wine (`~/.wine-cna-xna40`, win32) + DXVK 2.6, AMD Radeon 780M RADV, Linux; not Windows | `tools/xna-oracle/README.md:83-104`, `docs/d3d9-divergence-report.md:135-147` | F3 |
| `cna_oracle_tolerance` | 0 (all RGBA channels); FNA compiled-effect pixel fixtures +/-3 | `scripts/xna-diff.py`; `Fna3dEffectPixelOracleTests.cpp:43` | F3, F6 |
| `cna_oracle_directx9_result` | 39/39 recorded (gate `D3D9_XNA_Diff`); last dated report covers 31; native Windows re-run open (`D9-140`) | see F5 | F5 |
| `cna_oracle_exact_gated_scenes_easygl_software` | 2 each (`colored_linelist_quad`, `colored_linestrip_quad`) | CMake `EasyGL_XnaLineCoverage`, `Software_XnaLineCoverage` | F4 |
| `cna_oracle_software_result` | 18/39 byte-exact, 30/39 within 1 channel value (2026-09-11) | `plans/plan_software.md:677` | F5 [R] |
| `cna_oracle_fna3d_result` | 10/39 exact, 0 failed to render (2026-08-11, llvmpipe, GL driver); EasyGL 10/39 same date (pre-fix) | `docs/fna3d-parity-report.md:3-16` | F5 [R] |
| `cna_oracle_ci` | none of the oracle scripts/CTests runs in a workflow | `rg` over `.github/workflows` | F4 |
| `cna_parity_fixtures` | 32 fixtures; registering renderers EasyGL, WebGPU, SDL_GPU, OpenGL4 | `ParityFixtures.cmake`; 4 `cna_register_parity_fixtures(` sites | F7.4 |
| `cna_gltf_l7_assets` | 148 = 140 captured + 8 safe rejections; 4 renderer-owned golden sets (140 PNG each: EasyGL/OPENGLES3, Vulkan, Software, DirectX11) at tolerance 0, 2 processes; CI runs EasyGL only | JSON reports | F8 |
| `cna_gltf_reference_subset` | 13 assets vs Khronos glTF-Sample-Renderer `863b981` (thresholded) | `docs/gltf-reference-comparison.json` | F8 |
| `cna_xna_runtime_types_represented` | 331/331 | `docs/xna-4-runtime-member-coverage.md:7` | Coverage |
| `cna_xna_runtime_members_represented` | 3,627/3,627 (representation only; census = Microsoft runtime XML + DLL metadata) | `docs/xna-4-runtime-member-coverage.md:20-21` | Coverage |
| `cna_xna_runtime_member_kinds` | ctor 253, methods 1,518, properties 1,040, fields 753, events 63 | same | Coverage |
| `cna_xna_runtime_member_classes` | EXACT 1,746; SEMANTIC 1,823; HOST_LANGUAGE_SUBSTITUTION 58 | same | Coverage |
| `cna_pipeline_api_represented` | types 128/128; members 705/705; importers 10/10; processors 12/12; processor properties 47/47; source extensions 18/18 | `docs/xna-content-pipeline-parity-report.md:13-19` | Coverage |
| `cna_capi_symbols` | 9,355 symbols: 8,363 implemented / 15 partial / 468 planned / 509 N/A; 556 headers; ABI 0.29.0 experimental; release gate "Not ready" (1 unmet criterion) | `docs/c-api/COVERAGE.md:15`, `RELEASE_GATE.md:5-11` | Coverage |
| `cna_graphics_ext_line_coverage` | 94.2% lines (2,822/2,997), 97.8% functions, 57.5% branches; single module; dated 2026-08-18 | `docs/cnaext-coverage.md:15-17` | Coverage |
| `cna_samples_ported` | not derivable from CNA; external repo | - | Samples subsection |
| `cna_xnb_sweep` | 7,726 genuine reference .xnb, 4,337 byte-identical (56.1%), 747 semantically identical, 815 accepted, 1,797 need sample-defined components, 21 removed, 9 environment, 0 unexplained; corpus outside repo [R] | `plans/plan_xna_sample_xnb_sweep.md:889-905` | Samples subsection |
| `cna_signature_freeze_tests` | 1 file (Input), 56 `static_assert`s | `PublicApiInputSignatureFreezeTests.cpp` | Corrections 9 |
| `cna_strict_xna_check_scope` | `Microsoft::Devices` + `Sensors` only | `tools/devices/StrictXnaApiSurfaceCheck.cpp`, `cmake/Harnesses.cmake:186-238` | Corrections 9 |
| `cna_golden_images` | 17 (`examples/golden/*.png`, unchanged) | `ls examples/golden \| wc -l` | tutorial 125 |
| Storage / Media / Canvas defs | 14 / 304 / 17 | per-module tally | Test inventory |

---

## Open questions

1. **39/39 on DIRECTX9 has no committed dated run at TARGET.** The gate exists and the README/NEXT.md record it (2026-07-16), but `docs/d3d9-divergence-report.md` still says 31. Decide whether the site keeps "matches all 39" (recorded) with the date/host caveat, or "31 documented, 39 recorded".
2. **EasyGL/FNA3D whole-corpus numbers are stale (2026-08-11, pre-fix).** No committed re-measurement. Recommendation: drop per-renderer counts other than DIRECTX9 and SOFTWARE, or label them dated. A human/agent with the reference machine could re-run `scripts/run-oracle-corpus-multi.sh` (not allowed here).
3. **C API buildability** (alpha.1's compile blockers: 49-vs-50 map, unconditional GamerServices include with networking off) was not re-verified; statically the renderer map is now 25 = 25, but I did not check the GamerServices include or build anything. The C-API fact sheet must own this. Same for whether `general-tests-ci.yml` is actually green (and whether `EasyGL_XnaLineCoverage`, which imports Pillow via `xna-diff.py`, can run there since the workflow installs no `python3-pil`).
4. **"63 / 86 samples" cannot be sourced from CNA.** CNA's own (July) note says 88 ported/24 placeholder. Needs the cna-samples fact sheet.
5. **`1,289` non-XNA declarations** appears only on the site roadmap pages and not in any CNA file at either revision; recommend removal rather than replacement.
6. **CNA-side inconsistencies to mention to the maintainer, not to the public:** `README.md:47,591` still "31-scene, 0/31" and `:56` "~4,370-test"; `docs/coverage.md` and `docs/xna-4-api-coverage.md` still 3,467/3,627; `docs/cross-renderer-parity-fixtures.md` lists three renderers and 13 of 32 fixtures; `docs/gltf-conformance.md` says 146 vs 148 assets; `scripts/run-oracle-corpus-diff-*.sh` headers still say the EasyGL script "is NOT registered as a CTest" (it now is, for 2 scenes) and cite `open[retired]` twins.
7. **Whether to show the new Content-Pipeline oracle and sample-asset sweep on the verification page** and how: they are the largest real-XNA evidence added since alpha.1, but the sweep corpus (7,726 refs) and the XNA installer inputs are not in the repository, so readers cannot reproduce them from a clone. Suggested wording: "recorded by the project on its reference machine; inputs not redistributable".
8. The site's reproduce command could also print `git rev-parse HEAD` and add `-g '!vendor/**'` for safety; result unchanged in a clean worktree.
