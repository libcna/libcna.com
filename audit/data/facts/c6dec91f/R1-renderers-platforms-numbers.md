# R1 — Renderers, platforms, release and the canonical numbers, CNA B=c1c316b9 → T=c6dec91f

INTERNAL AUDIT RECORD (not served). This file names retired renderer identities and retired platform backends;
the public site must not — not even as "removed" notices, in metadata, search data or diagrams
(`scripts/check_retired_renderers.py` and `scripts/check_retired_platforms.py` enforce that).

Pins: B=`c1c316b9c7a846ce8002809c151fcd1af14942c9` (2026-10-09, tip of `apple/m4-stabilization` when Phase 5 read it),
T=`c6dec91fbf3ef5440f60e5329e4a4758b2d80c22` (2026-10-24 10:23:27 +0200, branch `next`; "Report sampler LOD bias and PBR
shading per renderer (CNA-DEMOS-ISSUE-006)"). `B` is an ancestor of `T`; `git rev-list --count B..T` = **834**
(678 first-parent, 4 merges); `git diff --shortstat B T`: 6,310 files, +242,902 / −934,124 lines.
CNA was read through the Git objects of the local clone (`git show`, `git ls-tree`, `git grep`, `git rev-list`) and the
tree extracted by `scripts/extract_cna_trees.sh` (stamp = T). Nothing in CNA or a sibling repository was modified,
built or run for this record. The local CNA checkout itself is on `next` at `f3e999a59`, 22+ commits past T; nothing
after T is documented.

## 0. Release identity

| Item | Value | Evidence |
|---|---|---|
| Released version | **0.1.0**, tag `v0.1.0` (annotated, "CNA 0.1.0", tagger date 2026-10-10 16:34 +0200) on commit `10a4ef1cb4cd832f761536d77588000104947f8d` "chore(release): prepare v0.1.0" | `git cat-file -t v0.1.0`; `CHANGELOG.md` "[0.1.0] — 2026-10-10" |
| B relative to the release | B is 22 commits **before** `v0.1.0` (`git rev-list --count B..v0.1.0` = 22); Phase 5 documented a pre-release snapshot whose version string was `0.1.0-alpha.1` | `git tag --contains B` = `v0.1.0` |
| T relative to the release | **812 commits after `v0.1.0`** (`git describe --tags` = `v0.1.0-812-gc6dec91fb`; 656 first-parent, 4 merges); `CHANGELOG.md` has a non-empty `[Unreleased]` section above `[0.1.0]` | `git rev-list --count v0.1.0..T` |
| Product version string at T | **`0.1.0`** (`project(CNA VERSION 0.1.0)`, `CNA_VERSION_PRERELEASE ""`), the same string as the release: the snapshot is unreleased development on top of 0.1.0, not 0.1.0 itself | `CMakeLists.txt:3,12` |
| Earlier release | `v0.1.0-alpha.1` (2026-08-20, `1bb2145d`); T is 4,521 commits after it (1,977 first-parent, 69 merges); 10,670 changed paths, +1,402,659 / −1,187,935 lines | `git rev-list`, `git diff --shortstat` |
| Sibling versions required at 0.1.0 and T | sharp-runtime **0.1.0**, easy-gl **0.1.1**, meta-gl **0.4.1**, enforced at configure time by `cmake/DependencyVersions.cmake` (`-DCNA_CHECK_DEPENDENCY_VERSIONS=OFF` downgrades to a warning) | `cmake/DependencyVersions.cmake:20-24`; CHANGELOG 0.1.0 "Dependencies" |
| 0.1.0 release verification (CNA's own record) | `cmake-build-multi`, Debian 13, GCC 14.2.0: 11,509 tests, 11,310 passed, 192 skipped, 7 failed (3 pre-existing, 3 Wine display limitation, 1 timing-sensitive) | CHANGELOG 0.1.0 "Verification" (RECORDED BY CNA, not re-run) |

The 0.1.0 release itself still had 14 renderer identities (B's set; `RRC-031..035` came after the tag) and C ABI 0.46.0
(handoff.md §2: "CNA `main`/`develop` are the v0.1.0 release (ABI 0.46.0)").

## 1. Canonical numbers (recomputed at T with the Phase 5 methods; `scripts/check_facts.py derive_from_cna` reproduces each)

| Fact | B `c1c316b9` | T `c6dec91f` | Method |
|---|---|---|---|
| Public renderer identities | 14 | **10** | `CNA_RENDERER_PUBLIC_IDENTITIES`, `cmake/RendererIdentities.cmake:27-29` |
| Implementation families | 12 | **8** (`directx9 easygl fna3d headless sdl-gpu software stub webgpu`) | directories under `modules/renderers/` with `src/` (`common/` excluded) |
| Retired identities | 37 | **41** (+`VULKAN`=8, `DIRECTX11`=14, `METAL`=42, `SDL_RENDERER`=1) | `CNA_RENDERER_RETIRED_IDENTITIES`, `RendererIdentities.cmake:34-39`; `docs/removed-renderers.md` |
| `GraphicsRendererType` enumerators / last ordinal | 14 / 13 | **10 / 9** (`OpenGLES3`=0 … `Fna3d`=9; dense) | `modules/core/include/CNA/GraphicsRendererType.hpp` |
| C ABI identity values | sparse, max 43 | **sparse**: 3, 4, 6, 9, 11, 12, 13, 22, 31, 43; reserved gaps 1, 2, 5, 7, 8, 10, 14–21, 23–30, 32–42, 44–51; `CNA_GRAPHICS_RENDERER_MAXIMUM` = 43 (FNA3D); next new value 52 | `modules/c-api/include/CNA/C/graphics.h:16-58`; `docs/renderer-registry.md` |
| Maturity (`GraphicsRendererMaturity`) | Production 6, Supported 5, Experimental 3 | **Production 3** (OPENGLES3, OPENGL33, DIRECTX9), **Supported 5** (WEBGL2, WEBGPU, HEADLESS, STUB, SDL_GPU), **Experimental 2** (SOFTWARE, FNA3D). WEBGPU moved Experimental → Supported (`f2f5a04aa`, 2026-10-17) | `modules/core/include/CNA/GraphicsRendererMaturity.hpp:66-89` |
| Category (`GraphicsRendererCategory`) | Native 6, TranslationLayer 4, Software 1, Web 1, Diagnostic 2 | **Native 3** (OPENGLES3, OPENGL33, DIRECTX9), **TranslationLayer 3** (WEBGPU, SDL_GPU, FNA3D), **Software 1**, **Web 1** (WEBGL2), **Diagnostic 2** (HEADLESS, STUB) | `GraphicsRendererCategory.hpp:64-91` |
| Classification names | `GraphicsBackendCategory`/`GraphicsBackendMaturity`, `getGraphicsBackend*()` | **`GraphicsRendererCategory`/`GraphicsRendererMaturity`**, `get[Current]GraphicsRenderer{Category,Maturity}()`; C: `CNA_GraphicsRenderer*`, `CNA_GRAPHICS_RENDERER_CATEGORY_*`/`_MATURITY_*`, `cna_graphics_renderer_*`; no alias of the old names (`91408ad08`, `34e86e430`, ABI 0.49.0) | CHANGELOG [Unreleased] "Changed" |
| Direct3D identities | 2 | **1** (`DIRECTX9`) | registry `DirectX*` namespaces |
| Browser-only identities | 1 | **1** (`WEBGL2`) | category Web |
| EasyGL identities / non-web | 3 / 2 | **3 / 2** (`OPENGLES3`, `OPENGL33`, `WEBGL2`) | `cmake/RendererRegistry.cmake` |
| Deliberately 2D-only identities | 1 | **0** (the only one was retired) | no surviving renderer is a 2D-only renderer; every pixel-producing renderer answers `GraphicsCapability::ThreeD` true, while STUB answers false for every capability, ThreeD included (`StubRenderer.hpp:180`; corrected after the deep-dives review) |
| `GraphicsCapability` members | 19 | **17** (`ComputeShaders`, `IndirectDraw` removed by MRT-007) | `modules/graphics/include/CNA/GraphicsCapability.hpp` |
| Compiled-effect identities / families | 11 / 9 | **8 / 6**: FNA3D always; five default-OFF options `CNA_{EASYGL,WEBGPU,SOFTWARE,DIRECTX9,SDL_GPU}_COMPILED_EFFECTS` (EasyGL covers 3 identities → 7 optioned identities); never: HEADLESS, STUB (2); refuse in a default configure: 9 of 10 | `cmake/RendererSelection.cmake:207,228,256,277,310` |
| Format-classifying families (Texture2D / render target) | 8 / 10; 7 / 9 | **Texture2D: 6 families / 8 identities** (`directx9 easygl fna3d sdl-gpu software webgpu`; HEADLESS and STUB accept only `Color`); **render target: 4 families / 6 identities** (`easygl sdl-gpu software webgpu`; HEADLESS, STUB, FNA3D and DIRECTX9 accept only `Color` render targets) | overrides of `ClassifySurfaceFormatEXT` / `ClassifyRenderTargetFormatEXT` outside examples/tests (`check_facts.py families_overriding`; the earlier text search also counted a DIRECTX9 comment) |
| Unbound-texture gate | 8 identities / 7 families | **5 / 4** (`Software, OpenGL33, OpenGLES3, WebGPU, SdlGpu`) | `StockEffectNullTextureTests.cpp:75` |
| Parity-fixture families | — | 3 | `cna_register_parity_fixtures(` under `modules/renderers` |
| Default renderer per host | Linux `OPENGLES3`, Emscripten `WEBGL2`, everything else the 2D renderer | **Emscripten `WEBGL2`; Windows, macOS (`Darwin`) and iOS `SDL_GPU`; every other system (Linux, Android, BSDs) `OPENGLES3`** | `cmake/RendererIdentityDefault.cmake` |
| iOS renderer allow-list | the 2D renderer and the Apple-native one | **`SOFTWARE`, `SDL_GPU`** ("SDL's GPU API on its Metal backend; not yet built or qualified for iOS") | `cmake/ApplePlatform.cmake:246-249` |
| Platform implementations | 3 | **3** (`SDL3`, `HEADLESS`, `TERMINAL`; TERMINAL POSIX-only) | `cmake/PlatformSelection.cmake` |
| Audio implementations | 3 | **3** (`SDL3`, `NULL`, `ALSA`) | `cmake/AudioPlatformSelection.cmake` |
| C++ test source files | 813 | **898** | `*.cpp` outside `third_party/` with a `test`/`tests` path segment |
| Files with a counted macro | 781 | **855** | `git grep -cE '^\s*(TEST\|TEST_F\|TEST_P\|TYPED_TEST\|TYPED_TEST_P)\s*\(' T -- '*.cpp' ':!third_party'` |
| Static GoogleTest-family definitions | 11,380 | **11,898** (TEST 8,859 · TEST_F 2,859 · TEST_P 161 · TYPED_TEST 19); 106 `INSTANTIATE_TEST_SUITE_P` | same grep, summed |
| Standalone `examples/**/*_test.cpp` programs | 781 | **598** (694 `.cpp` under `examples/`, 693 under `modules/`) | `git ls-tree -r --name-only T` |
| CI workflow files / jobs | 18 / 24 | **18 / 25** (`metal-macos-ci.yml` gone, `c-api-generated-routes.yml` new; `apple-ci.yml` 4 jobs incl. `macos-sdlgpu`) | `.github/workflows/*.yml`, `jobs:` keys |
| Automatic files / jobs | 16 / 21 | **16 / 22** (manual-only: `d3d-windows-ci` 1 job; `content-pipeline-windows-ci` 1 job on its own branch; `platform-ci`'s `sdl3-windows`, `if: workflow_dispatch`) | triggers |
| XNA 4.0 runtime types / members represented | 331 / 3,627 | **331 / 3,627** (`docs/xna-4-runtime-member-coverage.md` unchanged in B..T) | generated census, not re-run |
| XNA oracle scenes | 39 | **39** | `tools/xna-oracle/scenes/*.scene` |
| Built-in XNB readers | 61 (60 without native int128) | **61 (60)** — same canonical names; since LINK-004/021/053 they are *declared* registered by every `Game`/`ContentManager` and *installed* per family on first `Load<T>` | `AddTypeCreator("…")` names under `modules/content/src/Xnb` |
| C ABI version | 0.46.0 | **0.50.0** (0.47.0 MRT-008; 0.48.0 RRC-031..035; 0.49.0 classification rename; 0.50.0 UB-002 skinned-model part diffuse colour routes) | `modules/c-api/include/CNA/C/abi.h:34-40`; `docs/c-api/ABI_VERSIONING.md` |
| Public C headers | 60 | **60** | `ls modules/c-api/include/CNA/C` |
| Declared C routes (lines beginning `CNA_C_API`) | 3,210 | **3,212** (= 3,212 exports in `tools/c-api/abi_baseline.json`; 196 struct layouts, 1,476 integer constants) | `git grep -c '^CNA_C_API'` |
| Generated routes | none | **3,202 of 3,210** at the generation change were one spec line in `modules/c-api/spec/*.toml` (2,252 whole, 950 boundary + named helper); only the seven `cna_error_*` queries and `cna_get_abi_version` hand-written (CHANGELOG; `docs/c-api/GENERATED_ROUTES.md`). The two 0.50.0 routes came after that count | CHANGELOG [Unreleased] |
| C ABI release gate | Not ready, 631 planned (7,053 / 15 / 631 / 443 of 8,142) | **Not ready, 625 planned** (466 headers, 8,125 symbols: 7,032 implemented / 15 partial / 625 planned / 453 not applicable; 406 excluded headers); LIMITATIONS "15 partially mapped symbols in 9 groups, 453 unmapped in 89 groups" | `docs/c-api/RELEASE_GATE.md`, `docs/c-api/COVERAGE.md` |

## 2. What the four renderer retirements of 2026-10-13/14 mean for current guidance (RRC-031..054)

* The surviving native paths: **`SDL_GPU` is CNA's modern native path** (SDL owns its Vulkan, Direct3D 12 and Metal
  backends; FNA3D selects SDL_GPU, Direct3D 11 or OpenGL internally). Neither internal choice is a CNA identity
  (`docs/renderer-registry.md`). On Windows `DIRECTX9` remains; `OPENGLES3` is the default outside the browser on
  Linux/Android/BSD.
* `SDL_GPU` gaps carried over (CHANGELOG [Unreleased] "Removed"; handoff §5.2): `ShaderEffect` (`CustomEffects`) is
  compiled out on Windows, Apple and Emscripten (no runtime GLSL→SPIR-V→DXIL/MSL path); no occlusion queries (SDL_gpu
  3.5 has none); `BlendState.MultiSampleMask` ignored (pinned SDL 3.4.0 headers reserve the mask). `SDL_GPU` implements
  `RendererFeature::BaseInstanceDrawing` since RRC-043 (host-side expansion from the first instance); no other survivor.
* `SDL_GPU` is **the default on Windows, macOS and iOS but is not qualified there** (handoff §5.2): evidence = Linux
  (Vulkan) and Direct3D 12 under Wine (vkd3d-proton); no native Windows run; no re-run on Apple hardware after the
  retirement; `SDL_GPU` has never been built for iOS (CI tries it as a non-gating leg).
* Retired run-time behaviour: a retired name is refused at configure time and at run time (`CNA_GRAPHICS_RENDERER`
  environment variable, `GraphicsRendererSelection::SetPreferred`, the C by-name route), with its reserved C ABI value
  (`RRC-040`, `6549c623e`).
* Removed with them: `SetSamplerAddressModeWEXT` (RRC-041), `GraphicsRendererDescriptor::wantsHighDpi` (RRC-042),
  `IPlatformVulkanSurface` (platform header deleted).
* Automatic fallback now tries `HEADLESS` after the renderers that show a picture (`af83a91a6`).

## 3. The retired modern GPU layer (MRT-001..012, 2026-10-13)

Removed end to end: compute dispatch, storage buffers/images, the texture-array facade, `GraphicsMemoryBarrier`,
`GraphicsImageAccess`, `IndirectDrawArguments`, indirect drawing, the GPU-timer abstraction; `GraphicsCapability::
ComputeShaders`/`IndirectDraw`; the related `RendererFeature`/`RendererLimit`/`RendererFormatUsage` identities (ordinals
reserved); `ShaderStageEXT::Compute`; C routes and structs (ABI 0.47.0: 3,210 → 3,205 exports, two structs removed).
Kept: ordinary graphics — glTF/PBR/IBL/shadows, `ShaderEffect`, vertex/fragment `ShaderPackageEXT`, float render
targets, instancing, compiled effects, uniform blocks (`plans/plan_modern_retirement.md`; handoff §2 "Graphics layer").
The public `ComputeShader`/`StorageBuffer`/`StorageTexture2D`/`Texture2DArray`/`GpuTimer` classes had already gone in the
2026-09 scope reduction.

## 4. Link boundaries and size (LINK-001..054, merged `78298853f` 2026-10-13)

`docs/link-size-architecture.md`. A program links only the CNA subsystems it uses; nothing was disabled. Measured by CNA
on Mobile Eggbert (Linux x86-64 Debug, OPENGLES3, 2026-10-12): 208 MB → 62.4 MB Debug, 44.6 MB → 6.2 MB stripped, 3.0 MB as
a Release build with `CNA_OPTIMIZE_FOR_SIZE` (one game, one toolchain: RECORDED BY CNA, not a guarantee). Gates:
`LinkFootprint_2DGame`, `LinkFootprint_GamerServicesGame`, `LinkFootprint_FullFeatures`, `LinkFootprint_CapabilityQuery`,
`LinkFootprint_CameraOnly/_TrayOnly`, `ModuleLinkClosure_*` (`cmake/Tests/LinkFootprint.cmake`,
`scripts/check_link_footprint.py`); tools `tools/link_audit/why_linked.py`, `link_closure.py`.
New/changed options: `CNA_ENABLE_GAMER_SERVICES` (default = `CNA_ENABLE_NET`; `CNA_ENABLE_NET=ON` requires it),
`CNA_OPTIMIZE_FOR_SIZE` (OFF; `-ffunction-sections -fdata-sections` + `--gc-sections`/`-dead_strip`),
`CNA_CXX_RUNTIME_LINKAGE` (AUTO/STATIC/SHARED), `CNA_SHARED_LIBRARY` (ON on native Linux). SDL3_image and its submodule
removed (nothing used it). C++ ABI break: rebuild C++ consumers (`IPlatform::Supports()`, protected
`GetCameraService()`/`GetTrayService()`, `Effect::IsStockEffectEXT()`, `Texture::AsTextureCubeEXT()/AsTexture3DEXT()`,
`IRenderTargetBindingSource`, `Game` members); source compatibility kept except `IPlatform` implementations. mold now
links the same members as GNU ld and lld with a shared C++ runtime (`CNA::BuildConfig` names the runtime first).
CMake 3.30 is required for the shared-runtime linking mode (`b35fbc933`; root minimum stays 3.20).
`GraphicsDevice::GetShaderDialectEXT()` now returns the public `CNA::ShaderDialectEXT` (`CNA/ShaderDialectEXT.hpp`).

## 5. Platform evidence at T (handoff.md §2, §5.2)

| Target | What is verified |
|---|---|
| Linux x86_64 | everything; the suites run here |
| Windows | MinGW-w64 cross builds under Wine: `DIRECTX9` through DXVK, `SDL_GPU`'s Direct3D 12 backend through vkd3d-proton, `SOFTWARE`; manual MSVC workflow builds/runs the `DIRECTX9` suite and (since RRC-051) an `SDL_GPU` Direct3D 12 smoke leg, not yet run. No real-Windows hardware validation is current. C API pure-C suites run under Wine from MinGW-w64 |
| Web | `WEBGL2`, `WEBGPU` in Chrome |
| Android | `OPENGLES3` (default) on an x86_64 emulator; `SDL_GPU` on Android not qualified |
| macOS / iOS | macOS CI: `SOFTWARE`, portable platform suites, bundle smoke app; gating `macos-sdlgpu` leg (SDL_GPU on Metal smoke) since RRC-051, not run yet. iOS: `SOFTWARE` simulator smoke app; `SDL_GPU` legs non-gating. `SDL_GPU` is the default on both but not re-qualified |

The Phase 5 Mac mini M4 campaign (AM4, before T's retirements) remains history: it qualified renderer trees that included
two identities now retired; its evidence for `SOFTWARE`, `OPENGL33`, `SDL_GPU`, `WEBGPU`, `FNA3D` trees on that Mac predates
the 2026-10-13 retirement and was not re-run (handoff §5.2 "a re-run on Apple hardware" is listed as not done).

## 6. Test evidence at T (RECORDED BY CNA; nothing re-run here)

* Latest full Debug runs, 2026-10-17 (branch `stabilization`, private runner, RADV): `cmake-build-multi` (OPENGLES3 default +
  OPENGL33, WEBGPU, SDL_GPU, FNA3D, SOFTWARE, HEADLESS, STUB; C API) 11,433 tests, 1 failed, 195 skipped; `cmake-build-sdlgpu`
  11,284 / 0 failed / 256 skipped; `cmake-build-webgpu` 10,964 / 0 / 256; `cmake-build-software` 10,982 / 0 / 101;
  `cmake-build-fna3d` 10,806 / 2 failed (pass alone) / 400 skipped. Wine: `cmake-build-mingw` DIRECTX9 suite 59/59 without
  `DirectX9_CompiledEffects` (DXVK 2.6.0), 60/60 twice with DXVK 3.1.1. `cmake-build-headless` not re-run (handoff §2).
* CNA/cna-demos repair checkpoint, 2026-10-24 (batch 8, demos tree from CNA `da6c5c120`): SOFTWARE 664 PASS / 4 FAIL / 48 SKIP /
  3 NOTRUN of 719 IDs; OPENGLES3 706 / 3 / 7 / 3; serial CTest 684 PASS / 48 SKIP / 0 FAIL / 3 disabled (handoff §0).
* Stabilization pass 2026-10-16/17 "fixed or removed every reproduced CNA defect that was on" handoff §5; §5.1 now lists one
  defect (`SpriteSortMode::Immediate` batched on `SDL_GPU` and `WEBGPU`).

## 7. CNA/cna-demos repair campaign (`CNA_DEMOS_REPAIR_MATRIX.json` at T)

156 historical IDs. Matrix `status`: 137 RESOLVED, 8 PENDING_VERIFICATION, 7 ALREADY_FIXED, 2 RESOLVED_PENDING_PLATFORM_VALIDATION,
1 CONFIRMED_OPEN (066), 1 DEMO_EXPECTATION_BUG. `final_disposition`: 110 FIXED_VALIDATED, 23 DOCUMENTATION_CORRECTED,
8 ALREADY_FIXED, 3 FIXED_PLATFORM_VALIDATION_PENDING, 1 DEMO_EXPECTATION_BUG, 1 DUPLICATE_ROOT_CAUSE, 1 UNSUPPORTED_CONTRACT_CORRECTED,
9 none (005, 006, 007, 008, 022, 023, 031, 066, 067). Commits for all nine land **inside** B..T after the matrix and handoff
were last reconciled (`2df868a13` 005, `c6dec91fb` 006, `8f08a82cc` 007, `ec2d8b692` 008, `cd1f5ef0a` 022, `1beef880d` 023,
`a9d378c06` 031, `34be9272b` 066, `f1f1edae9` 067), but none is closed on a complete checkpoint at T: the site may say "a fix
is committed at the snapshot; CNA has not yet validated its closure", never "fixed". Two further findings outside the 156:
DC-R1 (SDL_GPU mixed cube/2D MRT, a documented boundary) and DC-R2 (SDL_GPU multisample mask ignored), both CONFIRMED_OPEN.

## 8. External repositories touched by T's facts

* CNA.NET (`libcna/cna-dotnet`, local `develop` `90b11a2`, 2026-10-25): consumer ABI **exactly 0.47.0** (`f1f88e1`,
  MRT-012, 2026-10-13; `eng/cna-native-abi-policy.json`); CI pins CNA `next` `fbd8e64a3` (`CNA_UPSTREAM_COMMIT`); it refuses
  0.46.0 (the v0.1.0 release) and has not admitted 0.48.0–0.50.0, so it does **not** consume the documented snapshot
  (handoff §2 "must admit 0.50.0 before it moves its pin").
* Archived bindings: in `cna-cemetery` (the handoff's "cna-lab" wording is stale; the site already says cna-cemetery).
