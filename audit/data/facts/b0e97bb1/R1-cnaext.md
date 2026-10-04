# R1 — Retirement of the CNAEXT graphics "engine layer" (O=009d40f5 → T=b0e97bb1)

CNA repo read only via git objects. `O=009d40f5dd085c4e674d3479675fac84b12b3e0a`, `T=b0e97bb1bb876f9b3edd6f4ff1ef3067908ae8ac`.
Site = `/rv/data/development/github.com/libcna/libcna.com` (HEAD df85d05). Line numbers are physical lines of the HTML file (`grep -n`).
Claim classes: **SRC** source fact · **BLD** build fact (CMake/registration) · **RT** runtime-qualified · **PLAT** platform-qualified · **CNA-REC** CNA's own recorded result, not reproduced here · **PLAN** future plan.

## 0. Summary (for editors)

**Public-prose paragraph (truthful at T):**
> In late September 2026 (commit `5572f3ca1`, MOD-RETIRE-1) CNA retired its experimental `CNA::Graphics` "engine layer". The render pipeline, post-process chain and passes (bloom, tonemapping, FXAA, SSAO, SSR, fog, …), shadow-map generation, clustered/area lighting, light probes, sky, environment (IBL) preprocessing, PBR material abstraction, instancing/LOD/culling helpers, particles, and the public compute/storage-buffer/texture-array/GPU-timer classes were deleted, together with the C header `engine_layer.h` (858 routes). What remains of the opt-in `CNA_CNAEXT` option (still OFF by default, still built by no CI workflow) is a small `modules/graphics-ext` module: three standalone retro post-process effects — `AsciiPostProcessEffect`, `CRTEffect` and `DepthEffect` — plus the `DebugDraw` wireframe helper and the portable shader-package types `ShaderCodeEXT`/`ShaderPackageEXT` that those effects and `ShaderEffect`'s package constructors use. Everything XNA-shaped that the old pages called "always compiled" — `PbrEffect`, `SkinnedPbrEffect`, `ShaderEffect`, `ColorMatrixEffect`, glTF import, morph targets, skinning, shadow-*receiving* (`IShadowReceiverEXT`, `ShadowCascadeStateEXT`, `PunctualLightEXT`) and IBL-*receiving* (`ImageBasedLightEXT`) — is unaffected, but CNA no longer generates shadow maps or IBL textures for you: an application must produce them itself. The `CNAEXT` marker macro and the `…EXT` naming convention are unchanged.

**Exact surviving retro-effect names (all `namespace CNA::Graphics`, headers `modules/graphics-ext/include/CNA/Graphics/*.hpp`, every one wrapped in `#ifdef CNA_CNAEXT`):**
`AsciiPostProcessEffect` + enum `AsciiQuantizeMode {BlackWhite, Color}`; `CRTEffect` (derives `ShaderEffect`) + enum `CRTMaskType {None, ApertureGrille, ShadowMask}`; `DepthEffect` (derives `ShaderEffect`, colour-depth/palette reduction — *not* depth visualisation) + enums `DepthEffectMode {Color16Bit, Color8Bit, Grayscale4Bit, Grayscale2Bit, Grayscale1Bit, Palette256, Palette16}` and `DitherMode {None, Bayer4x4, Bayer8x8}`. Also retained in the same module: `DebugDraw`, `ShaderCodeEXT`, `ShaderPackageEXT` (+ `ShaderPackageSelectionEXT`, `ShaderBindingTypeEXT`, `ShaderBindingRequirementEXT` declared in that header), master include `CNAEXT.hpp`. C routes for all of these live in `CNA/C/graphics_ext.h`.

**Headline recommendation:** keep the URL `docs/cnaext-engine.html` (90 inbound files) but REWRITE it as "CNAEXT: extensions and retro effects"; DELETE tutorials 153 and 154; REWRITE 115, 116, `development/internals/modules/graphics-ext.html`; retire known issues CNA-BUG-097/098/109/270, CNA-GAP-031, CNA-VGAP-017/018 (subject deleted), rewrite CNA-GAP-032, CNA-BUG-094, CNA-BUG-200, CNA-GAP-029.

---

## 1. Commits in O..T (456 commits total)

`git log --oneline O..T | grep -iE 'MOD-RETIRE|cnaext|engine layer|graphics-ext|retro'`:

| Commit | Date | Subject | Relevance |
|---|---|---|---|
| `5572f3ca1` | 2026-09-27 | refactor(MOD-RETIRE-1): retire graphics engine layer and keep retro effects | **The retirement.** 685 files, +3,337 / −180,609 (`git show --stat 5572f3ca1`). Message body = `docs/graphics-ext-scope-reduction.md` (SRC). |
| `b6309c0a8` | 2026-09-28 | chore(c-api): regenerate COMPATIBILITY.md and BoolContractSmoke.c left stale by MOD-RETIRE-1 | C headers 61 (60 + umbrella); `CNA_Bool` routes 114 → 100. |
| `2c70eaf0f` | 2026-09-29 | fix(BL-18): put CNAEXT where C++ accepts it on using lines | Marker-macro fix (strict mode), unrelated to the engine layer; confirms marker convention lives on. |
| `b1e785273`, `6e27d7b14` | before 5572f3ca1 | DX12/DX11 CNAEXT compute/examples | Engine work added in O..T then deleted by 5572f3ca1. Many WIN11-00xx commits (e.g. `e876c8632` GPU particles on DX11, `4dec8dccd` DX11 clustered forward) likewise added engine features that no longer exist at T. |
| `774678acb` | 2026-09-26 | feat(WIN11-0033): enable DX11 postprocess and prepass HLSL packages | Added `modules/graphics-ext/src/shaders/post_process/PostProcessHlsl.generated.hpp`; **survives** — CRT/Depth now carry an HLSL variant (see §3). |

Out of my topic but affects the same pages: `261cb5f7f` (2026-09-28, RRC-015) retired GDI, HTML_DOM, SVG_DOM and **OPENGL4**; `0f96ea703` (RRC-012) removed FreeDirect, Direct2D, PortableGL. Renderer lists on engine pages are therefore doubly stale.

---

## 2. What was REMOVED

### 2.1 Module size (`git ls-tree -r --name-only <rev> modules/graphics-ext/...`)

| Metric | O | T | Evidence |
|---|---:|---:|---|
| Public headers `include/CNA/Graphics/*.hpp` | 98 | 11 | `git ls-tree --name-only <rev> modules/graphics-ext/include/CNA/Graphics/ \| wc -l` |
| + internal ASCII headers (`include/CNA/Internal/Graphics/Ascii/`) | 2 | 2 | AsciiFontAtlas.hpp, AsciiQuantizer.hpp |
| `src/*.cpp` | 83 | 9 | |
| test `.cpp` files | 92 | 6 | |
| TEST/TEST_F/TEST_P/TYPED_TEST macros (static count) | 967 | 76 | `git grep -h -E '^\s*(TEST\|TEST_F\|TEST_P\|TYPED_TEST)\(' <rev> -- modules/graphics-ext/tests \| wc -l` |
| example `.cpp` | 32 | 6 | T: ascii_fontatlas, ascii_posteffect_3d_source, ascii_posteffect_pixel, ascii_quantizer, crt_effect_demo, depth_effect_demo |
| shader package dirs in graphics-ext | 11 | 1 (`post_process`) | `package.json` count; tree-wide 20 → 2 (other = `modules/graphics/examples/common/shaders/portable_tint`) |
| `*ShaderPackageReproducibility` ctests | 17 | 1 (`PostProcessShaderPackageReproducibility`) | `git grep -o '[A-Za-z]+ShaderPackageReproducibility' <rev> -- 'cmake/*' '*CMakeLists.txt'` (BLD) |
| `CNAEXT_*` ctests | 32 | 0 | `git show 5572f3ca1 -- modules/graphics-ext/examples/CMakeLists.txt` (BLD) |
| Line count, all categories (CNA's figure) | 125,949 | 8,728 | `docs/graphics-ext-scope-reduction.md` at T (CNA-REC) |

### 2.2 The 87 removed public headers (all `CNA::Graphics`, from `comm -23` of O vs T header lists)
AerialPerspectivePass, AreaLightBrdfTable, AreaLightShading, AsciiPass, AtmosphericSky, AutoExposureEXT, BlitPass, BloomPass, CascadedShadowMap, ChromaticAberrationPass, ClusteredForwardEffect, ClusteredLightAssignment, ClusteredLightBuffer, ClusteredLightCompute, ClusteredLightEXT, ClusteredLightGrid, ClusteredLightSetEXT, ClusteredLightType, ClusteredShadowPolicyEXT, ColorGradePass, ComputeShader, ConstantBuffer, ContactShadowPass, CubeLut, CubeShadowMap, DebugGizmos, DecalPass, DepthEncoding, DepthNormalPrepass, DepthOfFieldPass, DirectionalLightEXT, EffectPass (the CNA one, not XNA's), EngineException, EngineLayerVersion, EnvironmentProcessor, FilmGrainPass, FrustumCullerEXT, FullscreenPass, FxaaPass, GltfMaterialBridge, GpuInstanceCuller, GpuTimer, HdrDisplayOutput, HeightFogPass, InstancedRendererEXT, LensFlarePass, LightProbeBaker, LightProbeEXT, LightProbeVolumeEXT, LightShaftPass, LodGroupEXT, LutInterpolation, MaterialBinding, MotionBlurPass, ParticleSystem, PbrMaterial, PbrMaterialExtensions, PointLightEXT, PostProcessChain, PostProcessContext, PostProcessPass, RenderPipeline, RenderPipelineSettings, RenderQuality, RenderTargetPool, RequireCapability, ScopedRenderTarget, ShaderDiagnostics, ShaderEffectFactory, ShadowMap, ShadowQuality, Skybox, SpatialUpscalePass, SpotLightEXT, SpotShadowMap, SsaoPass, SsrPass, StorageBuffer, StorageTexture2D, Texture2DArray, ThinFilmIridescence, TonemapPass, TonemappingMode, TransparencyMode, TransparentDrawList, VolumetricFogPass, WeightedBlendedTransparency.
Also gone: `CNA_CNAEXT_ENGINE_VERSION`, `getEngineLayerVersion()`/`…String()` (no match in `modules/` at T), `StorageBufferT<T>`, `ConstantBufferT<T>`, `detail::requireCapability`.

### 2.3 Removed outside graphics-ext (SRC, `git show --stat 5572f3ca1`)
- **Core graphics:** `Microsoft/Xna/Framework/Graphics/AreaLightEXT.hpp` + `src/Xna/AreaLightEXT.cpp` + its test. `ShaderEffect` lost `SetTextureArrayEXT`, `ClearTextureArrayEXT`, `SetStorageTextureEXT`, `ClearStorageTextureEXT` (were `#ifdef CNA_CNAEXT`). `GraphicsDevice` lost the two engine exemptions `EngineLayerFloatFilteringScope` (float-filter bypass, VMG-0006) and `EngineLayerTextureSizeScope` (oversized RT ceiling) plus `include/CNA/Internal/Graphics/EngineLayer*.hpp` — "XNA profile rules now apply uniformly" (scope doc).
- **C API:** `modules/c-api/include/CNA/C/engine_layer.h` (12,039 lines; 858 `CNA_C_API` lines at O), `CnaCApiEngineLayer.cpp` (22,591 lines), `CnaCApiGraphicsExt.cpp` engine parts, tests `EngineLayerSmoke.c` (8,635 lines), `CubeLutOracleTest.cpp`, `CubeLutFuzz.cpp`. Exports in `tools/c-api/abi_baseline.json`: **4,055 (ABI 0.29.0) → 3,213 (ABI 0.30.0)** at 5572f3ca1, −842, 0 added. Removed families (export prefixes): pbr_material 65, clustered_light 60, light_probe 46, render_pipeline 38, clustered_forward 29, depth_normal 27, cascaded_shadow 24, post_process 23, particle_system 22, shadow_map 20, …, plus `cna_engine_layer_get_version`/`copy_version_string`, 6 DebugDraw gizmo routes, **13 effect shadow/IBL/punctual routes** (`cna_effect_set_shadow_map_ext`, `…_punctual_light_ext`, `…_image_based_light_ext`, …), `cna_graphics_device_draw_[indexed_]primitives_indirect_ext`, `cna_graphics_device_supports_shadow_sampling_ext`, `cna_pbr_effect_apply/extract_material`, `cna_skinned_pbr_effect_apply/extract_material`. C headers 61 → 60 (`git ls-tree --name-only <rev> modules/c-api/include/CNA/C/`).
  - At T (after later commits): ABI **0.44.0** (`abi.h` lines 34–40), **3,210** exports — later changes are out of R1 scope.
- **Renderer examples/tests removed** (engine consumers): `opengl4_gl41_floor_test`, `opengl4_modern_stress_test`, `OpenGL4StorageTextureTests`, `OpenGL4TextureArrayTests`, 3 `sdlgpu_*` (halffloat filtering, modern stress, storage-buffer lifetime), 8 `vulkan_*` (compute storage buffer, effect bound texture, engine matrix arena, format limit queries, gpu timer debug, indirect draw, shadow caster winding, texture2d array), `webgpu_debug_marker_test`, `webgpu_modern_stress_test`.
- **Content tests:** `GltfMaterialToPbrMaterialTests.cpp` removed; content test group no longer links `cna_graphics_ext` (`cmake/UnitTests.cmake` diff).
- **Tools:** 7 shader generators `tools/shader_package/generate_{clustered_forward,culler,depth_normal_prepass,particle,post_process,scene,transparency_test}_hlsl.py`.
- **Docs in CNA:** `docs/cnaext-nova3d.md`, `docs/cnaext-showcase.md` and 6 showcase PNGs deleted; `docs/cnaext-engine-layer.md` rewritten to 23 lines ("Standalone CNA graphics extensions"); `docs/cnaext-getting-started.md` rewritten to 11 lines; `docs/cnaext-coverage.md`, `cnaext-engine-changelog.md`, `cnaext-ownership.md`, `cnaext-perf.md`, `misc/CNAEXT.md` now carry a "Historical record … removed in the 2026-09 scope reduction" banner. New: `docs/graphics-ext-scope-reduction.md`.
- **ctests removed (all 32):** CNAEXT_Settings_Compile_Run, _ShadowMap, _CascadedShadowMap, _PointShadow, _Skybox, _ImageBasedLighting, _ShadowReceiver, _InstancingAndLod, _ComputeParticles, _ClusteredLights, _BloomInTenLines, _LeakLoop, _RenderPipeline, _Fxaa, _Showcase, _GltfPbr, _GpuDriven, _Transparency, _ContactShadow, _Grading, _GpuTiming, _Ssao, _Tonemap, _PostProcessChain, _HdrRenderTarget, **_GuardDiscipline, _MatrixCompleteness, _AccessorConventions, _NamingRule, _RendererDescriptorsParse, _NoPosixSetenv, _DoxygenGroup**. The scripts `scripts/check_no_posix_setenv.py` and `scripts/check_cnaext_guards.sh` still exist at T but **no CMake file at T references them** (`git grep -E 'check_no_posix_setenv|check_renderer_descriptors|check_cnaext' T -- 'cmake/*' 'CMakeLists.txt' 'modules/*'` → empty) (BLD).

### 2.4 What did NOT change
- `modules/devices-ext` (`CNA::Devices`): `git diff --stat O T -- modules/devices-ext` is empty. Its files are gated by **`CNA_DEVICES`**, not `CNA_CNAEXT` (`Clipboard.hpp` line 4 `#ifdef CNA_DEVICES`). 17 public headers + 1 `Detail/` header.
- Renderer-internal implementations of compute, storage buffers/textures, texture arrays, GPU timers, indirect draw: kept (`IGraphicsRenderer.hpp` at T: `IGpuTimerRenderer` l.208, `IStorageBufferRenderer` l.253, `IComputeShaderRenderer` l.353, `ITexture2DArrayRenderer` l.804, `IStorageTexture2DRenderer` l.844, `CreateComputeShader` l.3048, `CreateGpuTimerEXT` l.3191). Scope doc: "Renderer production implementations were left intact". **But no public class outside `modules/renderers` consumes them at T** (`git grep 'CreateGpuTimerEXT()\|CreateStorageBufferEXT\|…' T` outside renderers → only declarations) (SRC).

---

## 3. What SURVIVES at T with the CNAEXT name or EXT suffix

| Item | Where at T | Gate | Class |
|---|---|---|---|
| `CNA_CNAEXT` CMake option | `CMakeLists.txt:178` — text now "Enable standalone ASCII, CRT, colour-depth and DebugDraw graphics extensions", default OFF (was "Enable CNA CNAEXT extended graphics layer (beyond XNA 4.0)", O line 176) | — | BLD |
| `CNA_CNAEXT` compile definition | `modules/CMakeLists.txt:239` on `cna_build_config` | — | BLD |
| `cna_graphics_ext` / `CNA::GraphicsExt` target | `modules/graphics-ext/CMakeLists.txt` (comment: "Standalone retro effects, DebugDraw, and their portable shader packages"); always added (`modules/CMakeLists.txt:362`) | sources guarded | BLD |
| `cna_cnaext` / `CNA::CnaExt` INTERFACE umbrella | `modules/CMakeLists.txt:369-377` = `cna_graphics_ext` + `cna_devices_ext` | — | BLD |
| `cnaext` configure/build preset | `CMakePresets.json:234` (displayName still "CNAEXT engine layer (OpenGL ES renderer, Debug)", description still lists RenderPipelineSettings/PbrMaterial — **stale in CNA**) | — | BLD |
| Master include `CNA/Graphics/CNAEXT.hpp` | includes exactly the 10 retained public headers (`@file … Standalone CNA graphics utilities and retro effects`) | `CNA_CNAEXT` | SRC |
| Retro effects + enums | see §0 | `CNA_CNAEXT` | SRC |
| `DebugDraw` | `CNA::Graphics::DebugDraw`: begin(view,projection)/end/clear, addLine/addBox/addSphere(×2)/addFrustum/addCross, setDepthTested; uses core `BasicEffect` | `CNA_CNAEXT` | SRC |
| `ShaderCodeEXT`, `ShaderPackageEXT` (+`ShaderPackageSelectionEXT::isUsable`, `selectFor(...)`, `ShaderBindingTypeEXT`, `ShaderBindingRequirementEXT`) | graphics-ext headers | `CNA_CNAEXT` | SRC |
| `ShaderEffect(device, ShaderCodeEXT, ShaderCodeEXT)` / `ShaderEffect(device, ShaderPackageEXT[, …])` | `ShaderEffect.hpp` lines 48–72, 296–313, 336–356 | `#ifdef CNA_CNAEXT` | SRC |
| Retro shader package languages | `post_process/package.json`: glsl-es, glsl, spirv, wgsl; plus HLSL vertex+fragment added in code from `PostProcessHlsl.generated.hpp` (`PostProcessShaderPackages.cpp` ~l.92–103; HLSL fragments for `crt` and `depth_effect` at generated header l.383–384) | — | SRC. DirectX11 renderer returns true for `Hlsl` when a device exists (`DirectX11Renderer.cpp:1512-1513`) → CRT/Depth *should* be selectable on DIRECTX11: **RT/PLAT, not verified**. |
| C API `graphics_ext.h` | 44 declarations at T (28 at O): `cna_graphics_ext_is_available`; `cna_image_based_light_ext_init/_is_valid`; `cna_indirect_draw_[indexed_]arguments_init`; 11 `cna_crt_effect_*`; 5 `cna_depth_effect_*`; 8 `cna_ascii_post_process_effect_*`; 15 `cna_debug_draw_*`. Removed from it: `cna_pbr_material_init`, `cna_pbr_material_ext_init`, `cna_render_pipeline_settings_init`. Routes return `CNA_RESULT_NOT_SUPPORTED` with the option off (`docs/c-api/GRAPHICS_EXT.md` at T) | ABI-stable regardless of option | SRC |
| `CNAEXT` marker macro | `modules/core/include/CNA/CNAHelper.hpp:23/25` (deprecated under `CNA_STRICT_XNA_API`, else empty). Marker lines in `modules/*/include/Microsoft/*` (naive: `git grep -h -w CNAEXT <rev> … \| grep -vE '^\s*(#\|\*\|//\|/\*)' \| wc -l`): O 1,731, T 1,744 | always | SRC |
| Core EXT surface (always compiled, unaffected) | `PbrEffect`, `SkinnedPbrEffect` (same 18 EXT members O and T: set/getImageBasedLightEXT, set/getPunctualLightEXT, set/getShadowMapEXT, …CascadesEXT, …DepthBiasEXT, …FilterRadiusEXT, …LightViewProjectionEXT, setShadowsEnabledEXT, SetOwnedSpecular[Color]MapEXT); `IShadowReceiverEXT`, `ShadowCascadeStateEXT`, `PunctualLightEXT`, `ImageBasedLightEXT`, `AlphaModeEXT`, `TextureTransformEXT`, `GltfImportReportEXT`, `MorphTargetEXT` (`SetMorphWeightsEXT` l.157, `EvaluateMorphWeightsEXT` l.169), `SkinnedModelEXT`; `ColorMatrixEffect`; `CNA::Graphics::VertexTypeRegistryEXT` (in `modules/graphics`, ungated) | none | SRC |
| GraphicsDevice EXT members | identical set O and T: `DrawInstancedPrimitivesBaseInstanceEXT`, `DrawPrimitivesIndirectEXT`, `DrawIndexedPrimitivesIndirectEXT`, `GetMaxComputeWorkGroup{Count,Invocations,Size}EXT`, `SupportsShadowSamplingEXT`, `SupportsImageBasedLightingEXT`, `SupportsShaderLanguageEXT`, `GetRendererCapabilityProfileEXT`, … (27 names) | none | SRC. **Caveat:** the indirect draws take `const CNA::Internal::Renderers::IStorageBufferRenderer&` (`GraphicsDevice.hpp:637-658`); with `StorageBuffer` deleted no public class produces one → effectively unusable from game code at T. |
| `GraphicsCapability` | 19 members incl. `ComputeShaders`, `IndirectDraw`, `FloatRenderTargets`, `HalfFloatRenderTargets`, `HalfFloatTextureLinearFiltering` (doc comments rewritten to drop engine references) | none | SRC — capability *queries* survive; public compute *API* does not. |
| `SupportsComputeShadersEXT` | **renderer-internal** `IGraphicsRenderer::SupportsComputeShadersEXT()` (`IGraphicsRenderer.hpp:3115`), not a public GraphicsDevice member (also true at O) | — | SRC |
| CI | No `.github/workflows/*` at T mentions `CNA_CNAEXT` or the `cnaext` preset (18 workflow files) | — | BLD |
| CNA's own validation of the retained set | `CNA_CNAEXT=ON`, OPENGLES3: 78/78 retained-effect + graphics-profile tests, 4/4 ASCII examples, 17/17 focused C API tests; `CNA_CNAEXT=OFF` also built; Vulkan target compiled (2026-09-27) | — | CNA-REC (`docs/graphics-ext-scope-reduction.md`) |
| DebugGizmos | removed; "may be reimplemented in the future … built on top of DebugDraw … generic geometric data" | — | **PLAN** (scope doc §"DebugGizmos future intent") |

---

## 4. Feature disposition (everything libcna.com attributes to the engine layer)

| Feature as presented on site | Status at T | Where / what to say |
|---|---|---|
| RenderPipeline, RenderPipelineSettings, HDR scene target, statistics, user passes | **GONE** | — |
| Post-process chain & passes (Bloom, Tonemap+TonemappingMode, FXAA, SSAO, SSR, DoF, MotionBlur, ColorGrade/CubeLut/LutInterpolation, ChromaticAberration, FilmGrain, LensFlare, LightShaft, HeightFog, VolumetricFog, AerialPerspective, Decal, SpatialUpscale, HdrDisplayOutput, AutoExposureEXT, Blit, Fullscreen, CNA `EffectPass`, RenderTargetPool, ScopedRenderTarget) | **GONE** | Hand-written render-target post-processing (tutorials 24/66) still applies. |
| AsciiPass (ASCII wrapper for the chain) | **GONE** | `AsciiPostProcessEffect` itself SURVIVES. |
| AsciiPostProcessEffect, CRTEffect, DepthEffect, enums | **SURVIVE** | graphics-ext, `CNA::Graphics`, `CNA_CNAEXT=ON`. |
| DepthNormalPrepass, transparency (TransparencyMode, TransparentDrawList, WeightedBlendedTransparency) | **GONE** | — |
| Shadow *generation* (ShadowMap, CascadedShadowMap, SpotShadowMap, CubeShadowMap, ContactShadowPass, ClusteredShadowPolicyEXT, ShadowQuality) | **GONE** | App must render its own map. |
| Shadow *receiving* (IShadowReceiverEXT, ShadowCascadeStateEXT, PunctualLightEXT) | **SURVIVES** (C++ core) | C routes for effect shadow state **removed** (13 `cna_effect_*_ext`). |
| IBL *generation* (EnvironmentProcessor) | **GONE** | — |
| IBL *receiving* (ImageBasedLightEXT, setImageBasedLightEXT) | **SURVIVES** (C++ core) | C: `cna_image_based_light_ext_init/_is_valid` survive; effect set/get IBL routes removed; `cna_graphics_device_supports_image_based_lighting_ext` survives. |
| Engine lights DirectionalLightEXT/PointLightEXT/SpotLightEXT; clustered forward lighting (ClusteredForwardEffect, ClusteredLight*); light probes (LightProbe*); AreaLightShading/AreaLightBrdfTable; ThinFilmIridescence | **GONE** | — |
| `AreaLightEXT` (core, always compiled per site) | **GONE** (removed from `modules/graphics`) | Remove from every "always compiled" list. |
| Skybox, AtmosphericSky | **GONE** | Hand-written skybox (tutorial 64) still valid. |
| PbrMaterial, PbrMaterialExtensions, MaterialBinding, GltfMaterialBridge | **GONE** | glTF import builds `PbrEffect`/`SkinnedPbrEffect` directly (scope doc; content group no longer links graphics-ext). |
| PbrEffect / SkinnedPbrEffect | **SURVIVE** (core, not gated) | — |
| InstancedRendererEXT, LodGroupEXT, FrustumCullerEXT, GpuInstanceCuller, ParticleSystem | **GONE** | `DrawInstancedPrimitivesBaseInstanceEXT` survives on GraphicsDevice. |
| ComputeShader, StorageBuffer(T), ConstantBuffer(T), StorageTexture2D, Texture2DArray, GpuTimer | **GONE (public API)** | Renderer-internal implementations remain; capability queries remain. Do not claim apps can dispatch compute. |
| Indirect draw | **SURVIVES in header only** | Needs renderer-internal argument buffer; no public producer; C routes removed. |
| DebugDraw | **SURVIVES** (gizmo methods removed) | graphics-ext, `CNA_CNAEXT=ON`; C routes in graphics_ext.h. |
| DebugGizmos | **GONE** | PLAN: possible DebugDraw-based replacement. |
| ShaderCodeEXT, ShaderPackageEXT, typed ShaderEffect constructors | **SURVIVE** | graphics-ext (`CNA_CNAEXT=ON`). |
| ShaderEffectFactory, ShaderDiagnostics (CNA::Graphics) | **GONE** | Core `CNA::ShaderDiagnosticEXT` and `ShaderEffect::GetShaderDiagnosticsEXT()` survive. |
| ShaderEffect texture-array / storage-texture bindings | **GONE** | — |
| EngineException, EngineLayerVersion, RequireCapability, engine revision 18 | **GONE** | — |
| engine float-filtering & RT-size exemptions in GraphicsDevice | **GONE** | XNA profile rules apply to all draws/targets. |
| `engine_layer.h` (858 routes) | **GONE** | `graphics_ext.h` survives (44). |
| CNAEXT_* lint/ctests, 11 engine shader packages | **GONE** | 1 package + 1 reproducibility test remain. |
| `CNA::Devices` / devices-ext | **UNCHANGED** | gated by `CNA_DEVICES`. |
| Nothing **MOVED** | — | The only "move" is C DebugDraw routes now declared in `graphics_ext.h` (engine_layer.h gone) and the glTF→PBR path no longer touching graphics-ext. |

---

## 5. Site inventory (excluding `audit/`, which holds hundreds of historical references and should be left as records)

Disposition codes: **DELETE PAGE**, **REWRITE PAGE**, **REWRITE SECTION**, **REMOVE SENTENCE**, **EDIT** (number/word fix), **KEEP**, **FP** (false positive: user code / unrelated).

### 5.1 Primary pages

**`docs/cnaext-engine.html` (593 lines) → REWRITE PAGE in place (keep URL; 90 inbound files).** Retitle e.g. "CNAEXT: extensions and retro effects".
| Lines | Heading / content | Disposition |
|---|---|---|
| 6, 18 (JSON-LD), 105, 109 | title "CNAEXT Engine Layer", description "98 public headers" | REWRITE (title/description) |
| 111–123 | on-page TOC | REWRITE to match new sections |
| 126–133 | snapshot banner; "Experimental, opt-in and moving … CNA_CNAEXT_ENGINE_VERSION 18"; intro listing PBR, shadow generation, IBL, post-processing pipeline, compute | REWRITE (§0 paragraph) |
| 135–166 | "What CNAEXT is": 4-column table (l.142–148: CNA_CNAEXT "Compiles the CNA::Graphics engine layer (… 98 public headers)"); marker code l.153–159; EXT-suffix note l.164–165 | KEEP structure; EDIT l.147 → "compiles the standalone retro effects, DebugDraw and shader-package types (11 public headers) and ShaderEffect's package constructors"; devices-ext "17 public headers" still true |
| 168–182 | "Where extensions live": l.174 "CNA::Graphics (module graphics-ext) … The engine layer described on this page" | EDIT l.174; KEEP l.175–182 (VertexTypeRegistryEXT verified ungated) |
| 184–200 | "The always-compiled extension surface" | KEEP with edits: l.193 remove `AreaLightEXT`; replace "Generating shadow maps and IBL products needs the engine layer" with "CNA no longer generates them; supply your own maps/cubes"; l.194 remove "texture-array / storage-texture bindings"; l.196 indirect draws: add internal-argument caveat |
| 203–239 | "Building it, and how the gate works": l.209 row CNA_CNAEXT; l.216; preset l.218–219; l.226 cache comment "Build the CNA::Graphics engine layer"; l.233 `CNAEXT.hpp // every engine-layer type`; l.235 tests/examples; l.237 C API "engine_layer.h declares its routes…"; l.238 "11 packaged shader directories, 156 GLSL, 208 payloads" | REWRITE SECTION (1 package; C API = graphics_ext.h; examples = 4 ASCII + CRT/Depth demos) |
| 241–260 | "From 12 to 98 headers" table | DELETE SECTION (or replace with a short "History: 12 → 98 → 11" note citing 5572f3ca1) |
| 262–315 | "What the engine layer contains" (Frame pipeline, Post-processing passes, Prepass and transparency, Shadows, Lights and IBL, Sky, Materials, Geometry throughput, Compute and GPU resources, Shader authoring, Post-process effects that predate the layer, Foundation) | DELETE SECTION; keep only rewritten "Shader authoring" (ShaderCodeEXT/ShaderPackageEXT) and "retro effects" + DebugDraw |
| 317–362 | "Which renderers can run it" + 25-identity table | REWRITE for CRT/Depth package languages (GLSL ES, desktop GLSL, SPIR-V, WGSL, HLSL) — DirectX row now wrong (HLSL exists); renderer list also stale (OPENGL4, PORTABLEGL, GDI, DIRECT2D, FREEDIRECT, HTML_DOM, SVG_DOM retired) |
| 364–396 | "Requirements per feature" table | DELETE all rows except AsciiPostProcessEffect (l.392) and CRTEffect/DepthEffect (l.393; "four languages" → five incl. HLSL) |
| 398–401 | "How a renderer's 'no' is handled" (EngineException, requireCapability) | DELETE SECTION |
| 403–483 | "A minimal example" (RenderPipeline GlowGame; BloomPass/ShadowMap isSupported; getEngineLayerVersionString) | DELETE; replace with CRTEffect/DepthEffect via SpriteBatch + ASCII Draw example (pattern per `docs/cnaext-getting-started.md` at T) |
| 485–489 | "API style and ownership" | REWRITE (lowerCamelCase still used by retained classes e.g. `setCellSize`, `setMode`; ownership notes about pipeline/passes go) |
| 491–499 | "Stability" (revision 18, changelog, C ABI 0.29.0) | REWRITE (no revision counter; ABI 0.30.0 removed engine routes) |
| 501–521 | "Test evidence and what is CI'd" (92 files/967 tests, 24 CNAEXT_* programs, seven lint ctests) | REWRITE: 6 test files / 76 TEST macros, 4 ASCII ctests (Ascii_Quantizer, Ascii_FontAtlas, AsciiPostProcessEffect_Pixel, AsciiPostProcessEffect_3DSource), 1 package reproducibility test, 0 CNAEXT_* ctests; still no CI. KEEP l.516 (devices-ext tests) |
| 523–533 | "Limits and open questions" (IBL 8-bit, HDR, SSAO, cascades, …) | DELETE all but a rewritten "no CI / no Windows evidence" item |
| 535–542 | "Where to go next" (Tutorials 153/154, cnaext_showcase_test.cpp) | REWRITE (drop 153/154/showcase) |
| 547–568 | Deep-dive box + known-issues box (BUG-094/097/098/181/274, GAP-031/032, VGAP-017/018/056) | Regenerate from `data/known-issues.json` after §5.7 changes |

**`docs/tutorials/115-cnaext-overview.html` → REWRITE SECTION(s); KEEP page.**
| Lines | Content | Disposition |
|---|---|---|
| 108–125 | "Three things called CNAEXT": l.119 "Compiles in the whole CNA::Graphics engine layer"; l.125 mentions "engine-layer reference" | EDIT l.119 → "Compiles the standalone retro effects, DebugDraw and shader-package types" |
| 166–184 | "Where extensions live": l.175 "CNA::Graphics (the engine layer)"; l.182 "Scene- and frame-level orchestration … goes into CNA::Graphics"; l.184 engine style example `pipeline.getSettings().setBloomThreshold(0.5f)` | EDIT l.175; REMOVE orchestration sentence; replace l.184 example with `crt.setScanlineIntensity(…)`/`ascii.setCellSize(…)` |
| 232–276 | "CNA_CNAEXT: the engine layer": commands (l.236–242), empty-header trap (l.245–250, still true), l.254 "98 public headers … revision 18", gated/not-gated table l.261–269, l.274, l.276 renderer sentence | REWRITE SECTION: keep commands + trap; replace l.254 and table (gated column = AsciiPostProcessEffect, CRTEffect, DepthEffect + enums, DebugDraw, ShaderCodeEXT/ShaderPackageEXT + ShaderEffect package ctors; not-gated column KEEP but drop `AreaLightEXT` (l.266) and qualify "indirect draws" (l.267)); delete l.276 |
| 278–296 | "Staying XNA-pure on purpose" | KEEP |
| 298–302 | "A note on the old name" (NOXNA→CNAEXT, CNA_NOXNA→CNA_CNAEXT) | KEEP (historical, accurate) |
| 304–310 | "Where to go next": l.306 "engine-layer reference — what the layer contains …"; l.308 Tutorials 153/154 | EDIT l.306; REMOVE l.308 |

**`docs/tutorials/116-post-process-effects.html` → REWRITE SECTIONS; KEEP page (its subject survives).**
| Lines | Content | Disposition |
|---|---|---|
| 100 | "How these four relate to the much larger engine-layer RenderPipeline…" (what-you'll-learn) | REMOVE |
| 105 | "They were the whole of the CNAEXT engine layer at alpha.1; … grown to 98 headers, RenderPipeline and nineteen pass classes …" | REWRITE: "The engine layer that grew around them was retired in Sept 2026; these effects remain" |
| 111–113 | effect table (renderer lists name OPENGL4; CRT/Depth row lacks HLSL) | EDIT (renderers; HLSL variant at T) |
| 119–131 | "First: three of them are not in your build" | KEEP; l.129 "engine-layer reference has the status" → reword |
| 192–202 | CRT/Depth "real ShaderEffects": l.194/196 "four fragment variants … GLSL ES, desktop GLSL, SPIR-V and WGSL"; l.197 "DIRECTX9/11/12 … no HLSL variant exists" | EDIT: package now also carries HLSL (774678acb); DIRECTX11 accepts Hlsl (RT unverified); D3D9/12 not checked |
| 299–328 | "These four and the RenderPipeline" (RenderPipeline, `CNA::Graphics::EffectPass`, addUserPass) | DELETE SECTION |
| 330–345 | "Choosing between them": l.340 "Bloom, tonemapping, FXAA, SSAO … RenderPipeline passes" | REMOVE row l.340 |
| 347–355 | "Where to go next": l.350 engine reference + Tutorials 153/154 | EDIT/REMOVE |

**`docs/tutorials/117-devices-layer.html` → KEEP.** No engine-layer claims (only l.378 link to Tutorial 115). devices-ext unchanged O→T.

**`docs/tutorials/150-build-time-fx-compilation.html` → KEEP** (no hits). **`152-graphics-profiles.html` → KEEP** (l.63 "Nothing here needs CNA_CNAEXT" still true). **`151-one-shader-several-renderers.html` → REWRITE SECTION l.302–357** "Optional: a shader package (CNA_CNAEXT=ON)": types survive; l.349 "their constructors live in the engine layer, so you must link the CNAEXT library" → "in the graphics-ext module (`CNA::GraphicsExt`, part of the `CNA` umbrella)"; l.357 "typed CNA_CNAEXT constructors" KEEP.

**`docs/tutorials/153-image-based-lighting.html` (585 lines) → DELETE PAGE.** Entire tutorial is built on `CNA::Graphics::EnvironmentProcessor` (l.58, 63, 93, 137, 143, 149, 178, 216, 331, 360, 457), engine Skybox/RenderPipeline (l.545), "revision (18)" (l.552), `cnaext_ibl_test`/`cnaext_showcase_test` (l.554). Only the receiving half (`ImageBasedLightEXT`, `PbrEffect::setImageBasedLightEXT`) survives; a replacement would need app-supplied pre-baked irradiance/prefiltered/BRDF textures and would be new, unverified content.

**`docs/tutorials/154-cascaded-shadows.html` (510 lines) → DELETE PAGE.** Built on `CascadedShadowMap`, `DirectionalLightEXT` (engine), `ShadowQuality` (l.58–486 throughout: 75, 81, 95, 116, 122, 162–194, 256–286, 350, 427–428, 459–479). Only receiving (`ShadowCascadeStateEXT`, `setShadowCascadesEXT`) survives.

**`development/internals/modules/graphics-ext.html` → REWRITE PAGE in place** (URL is wired into `scripts/dev_manifest.py:298-299`, `scripts/generate_dev_reference.py:104`, dev sidebar on every internals page, prev/next from gamer-services.html:302 and net.html:269). Title "Graphics extension pipeline internals" → e.g. "Graphics extension internals".
| Lines | Content | Disposition |
|---|---|---|
| 19, 140 | JSON-LD/title "pipeline internals … orders a frame" | REWRITE |
| 155 | evidence banner (92 test files/967 macros) | REWRITE (6/76) |
| 157 | intro "frame pipeline … compute … shadows …" | REWRITE |
| 159–172 | "The physical and compile-time boundary": l.160 "83 translation units", "98 headers"; l.161 CNAEXT_GuardDiscipline ctest; l.162 CnaExt umbrella (KEEP), "AsciiPass" | EDIT counts (9 TUs, 11 headers); guard rule still holds by inspection but **no ctest enforces it at T**; drop AsciiPass |
| 164–177 | ownership diagram, RenderPipelineSettings | DELETE |
| 175–211 | "Why the pipeline settings…", "A frame through RenderPipeline…", "end and the fixed pass order", "PostProcessChain::apply", "Resource lifetime, reset and exception edges" | DELETE SECTIONS |
| 213–224 | "Shader packages: from manifest to the selected variant": "Eleven package directories"; "The clustered forward package at this snapshot" (l.221–224) | KEEP "authoring chain" + "How a package is selected" (re-verify selectFor order at T); EDIT eleven → one (`post_process`, + HLSL generated header); DELETE clustered-forward subsection |
| 225–227 | "Other test-tree changes" (texture_array, modern_conformance packages) | DELETE |
| 228–245 | "The other families: a source and test map" table | REPLACE with 6-file table (AsciiPostProcessEffectTests, CRTEffectTests, DepthEffectTests, DebugDrawTests, ShaderInfrastructureTests, CnaExtMasterIncludeTests) |
| 246–262 | "Human route…", "Curated source route…" | REWRITE (no RenderPipeline) |
| 264–288 | deep-dive / known-issues / related boxes (BUG-097/098/109, GAP-031, VGAP-017/018) | Regenerate |

### 5.2 Top-level pages
| File:line | Claim | Disposition |
|---|---|---|
| `index.html:205` | "the CNAEXT engine layer has grown to 98 public headers (cascaded shadows, image-based lighting, post-processing, compute passes)… See the engine layer." | REWRITE SENTENCE → opt-in retro effects (ASCII/CRT/colour-depth) + DebugDraw; keep PbrEffect/skinning/morph part |
| `features.html:24` (meta), `:80` | "the CNAEXT engine layer" / "a far larger opt-in CNAEXT engine layer" | EDIT |
| `features.html:235` | "punctual and area lights" sit on the effects | REMOVE "and area lights" (AreaLightEXT gone) |
| `features.html:237` | build boundary: CNA_CNAEXT gates "the separate CNA::Graphics engine layer (next card), including … PbrMaterial, TonemappingMode and ShadowQuality" | REWRITE |
| `features.html:242–245` | card "Opt-in engine layer — still moving" / "CNAEXT engine layer (CNA::Graphics)" / 98 headers list / requirements | REPLACE card with "Opt-in retro effects (CNA_CNAEXT)" |
| `features.html:736–737` | ASCII card: l.736 "A companion AsciiPass plugs it into the post-process chain" | REMOVE that sentence; rest KEEP |
| `features.html:882` | C ABI "61 public headers and 4,055 exported routes (the engine layer alone is 858) … 0.29.0 … 4,055 exports" | REWRITE (defer exact T numbers to C-API researcher: retirement → 60 / 3,213 / 0.30.0; T → 60 / 3,210 / 0.44.0) |
| `features.html:317, 656, 664, 688` | renderer cards list compute, GPU timers, indirect draw | KEEP as renderer capabilities but add caveat: no public compute/timer API at T (OPENGL4 card l.656 also retired — other researcher) |
| `about.html:70` | "an expanded CNAEXT engine layer" | EDIT |
| `about.html:119` | "An engine layer: … grew from 12 to 98 public headers" | REWRITE (grew, then retired in 5572f3ca1) |
| `about.html:150` | "the CNA::Graphics engine layer with its render-pipeline settings (PbrMaterial, TonemappingMode, ShadowQuality)" | REWRITE |
| `about.html:152` | "engine layer grew from 12 to 98 … revision 18" | REWRITE |
| `documentation.html:276–279` | card "CNAEXT Engine Layer — 98 headers: render pipeline, post-process passes, shadows, lighting, IBL, compute, particles …" | REWRITE card text (same URL) |
| `architecture.html:24` (meta), `:96` (ASCII diagram "Opt-in: CNAEXT engine layer"), `:194`, `:253` (module table "The CNAEXT engine layer (CNA::Graphics, 98 public headers)"), `:446`, `:528` (tree "graphics-ext/ ← CNAEXT engine layer") | EDIT each → "CNAEXT graphics extensions (retro effects, DebugDraw)" / 11 headers |
| `roadmap.html:125` | ASCII "with a companion AsciiPass for the engine layer's post-process chain" | REMOVE clause |
| `roadmap.html:149` | "plus RenderPipelineSettings, PbrMaterial, TonemappingMode and ShadowQuality, now inside a much larger engine layer" | REMOVE clause |
| `roadmap.html:196–197` | row "CNAEXT engine layer — Opt-in, not in CI … 12 to 98" | REWRITE → "Engine layer retired (MOD-RETIRE-1, 2026-09-27); retro effects remain opt-in, not in CI" |
| `roadmap.html:236` | "nothing builds the CNAEXT engine layer, Diagnostics or the Inspector" | EDIT "CNAEXT extensions" |
| `roadmap.html:310` | "the engine layer says it is still moving" | REMOVE clause |
| `docs/roadmap.html:168` | "PBR effects and the CNAEXT engine layer … grew from 12 to 98 (post-processing, shadows, IBL, instancing/LOD, compute)" | REWRITE |

### 5.3 Other `docs/` pages
| File:line | Claim | Disposition |
|---|---|---|
| every `docs/*.html` sidebar | link "CNAEXT Engine Layer" (generated from `scripts/site_nav.py:41`) | EDIT label in script, regenerate |
| `docs/building.html:380` | preset `cnaext` | KEEP (exists) |
| `docs/building.html:464` | CNA_CNAEXT "The CNAEXT engine layer, beyond XNA 4.0" | EDIT → CMake's own text at T |
| `docs/tutorials/02-setup.html:288` | CNA_CNAEXT gates "AsciiPostProcessEffect, CRTEffect, DepthEffect, PbrMaterial, CNA::Graphics" | EDIT: drop PbrMaterial; add DebugDraw |
| `docs/c-api.html:67` | "Public C headers 59→61 (adds cnb.h and engine_layer.h)" | EDIT (60 at T; engine_layer.h removed in 0.30.0) |
| `docs/c-api.html:128` | 0.8–0.9 history: "five engine-layer capability identities" | KEEP (history) |
| `docs/c-api.html:156` | header table row "engine_layer.h new 858 …" | REWRITE → removed in ABI 0.30.0 |
| `docs/c-api.html:241` | CNA-BUG-270 box | remove after issue retired |
| `docs/effects.html:135` | "in the optional CNA_CNAEXT engine layer, a handful more" | EDIT |
| `docs/effects.html:179–180` | table row "Shader package / engine layer — ShaderEffect(device, ShaderPackageEXT), CNA::Graphics::*" | EDIT ("graphics-ext") |
| `docs/effects.html:334` | ShaderCodeEXT/ShaderPackageEXT ctors need CNA_CNAEXT | KEEP |
| `docs/effects.html:344` | "For image-based lighting and cascaded shadows … see Tutorial 153 and Tutorial 154" | REMOVE sentence (rest KEEP; renderer list also stale) |
| `docs/effects.html:346–356` | section "Engine-layer effects (CNA_CNAEXT=ON)": "about 98 public headers"; rows CRTEffect/DepthEffect ("depth visualisation" — **wrong at O and T**: it is colour-depth reduction), ClusteredForwardEffect, CNA::Graphics::EffectPass, AsciiPostProcessEffect | REWRITE SECTION → "Retro effects (CNA_CNAEXT=ON)"; delete ClusteredForwardEffect and EffectPass rows; fix DepthEffect description |
| `docs/shader-effects.html:139` | "texture-array / storage-texture binding need CNA_CNAEXT=ON" | REMOVE that clause (bindings removed); rest KEEP |
| `docs/shader-effects.html:526` | "they live in the engine layer … The engine's own packages ship GLSL desktop, GLSL ES, SPIR-V and WGSL; no HLSL … package ships, and no renderer answers true for Hlsl" | REWRITE: graphics-ext module; retained CRT/Depth package carries HLSL; DirectX11 answers Hlsl with a device (`DirectX11Renderer.cpp:1512-1513`) — flag for the shader researcher to re-verify |
| `docs/faq.html:440` | "The CNA::Graphics engine layer and the other CNA:: namespaces … gated by CNA_CNAEXT" | EDIT |
| `docs/xna-compatibility.html:392, 426, 434, 490` | engine layer gated by CNA_CNAEXT; "render-pipeline settings including PbrMaterial (98 public headers … up from 12)"; "gates … PbrMaterial and the CNA::Graphics surface" | EDIT each (drop PbrMaterial / 98) |
| `docs/verification.html:261` | 2026-08-18 CnaTests run "with the CNAEXT engine layer" | KEEP as dated history, add "(layer since retired)" |
| `docs/verification.html:525` | "CNAEXT engine-layer line coverage docs/cnaext-coverage.md" | EDIT (now a historical record in CNA) |
| `docs/verification.html:539` | optional layers default OFF | KEEP |
| `docs/verification.html:589` | CNA_CNAEXT "including … PbrMaterial … now 98 public headers" | EDIT |
| `docs/rendering-backends.html:252` | ASCII "is now AsciiPostProcessEffect, a CNAEXT effect" | KEEP |
| `docs/rendering-backends.html:672, 678, 679, 680` | evidence cells cite `CNAEXT_ImageBasedLighting`, "CNAEXT compute-particle test", `cnaext_gpu_driven_test`, `cnaext_gpu_timing_test`, `vulkan_indirect_draw_test`, `OpenGL4_ModernStress` — **all removed at T** | REWRITE evidence cells |
| `docs/rendering-backends.html:684` | "The CNAEXT engine layer (CNA::Graphics, 98 public headers: PBR materials, cascaded … decals) … requireCapability" | DELETE paragraph |
| `docs/render-targets.html:528` | "CNA's own engine-layer ShadowMap (CNA_CNAEXT=ON) makes exactly this choice" | REMOVE sentence |
| `docs/3d-rendering.html:761–764`, `docs/graphics-state.html:565,612` | user `skybox` variable / user `ParticleSystem` class | FP — KEEP |

### 5.4 Other tutorials
| File:line | Claim | Disposition |
|---|---|---|
| `37-multiple-lights.html:170–171` | PunctualLightEXT always compiled | KEEP (shadow maps now app-supplied) |
| `37-multiple-lights.html:183–220` | section "Many Lights: ClusteredForwardEffect (CNAEXT engine layer)" + code | DELETE SECTION |
| `37-multiple-lights.html:374` | summary "… and, with CNA_CNAEXT=ON, ClusteredForwardEffect for up to 128 lights" | REMOVE clause |
| `59-shadow-mapping.html:98` | learn-list "the ready-made ShadowMap engine-layer route" | REMOVE |
| `59-shadow-mapping.html:105–106, 111, 129` | "Two routes to shadows"; "CNA's own ShadowMap uses SurfaceFormat::Single…"; "engine layer's ShadowQuality::Ultra"; "engine layer's CubeShadowMap implements the six-face version" | REMOVE engine sentences/clauses |
| `59-shadow-mapping.html:259` | table header "Engine-layer ShadowMap can generate" (renderer table column) | DELETE column |
| `59-shadow-mapping.html:285–340` | section "The engine-layer route: ShadowMap and shadow receivers" (ShadowMap, CascadedShadowMap, CubeShadowMap, SpotShadowMap, Tutorial 154) | REWRITE SECTION → "Feeding your map to the built-in receivers" (IShadowReceiverEXT: setShadowMapEXT, setLightViewProjectionEXT, …; survives) |
| `59-shadow-mapping.html:211–570` other `u_shadowMap` hits | user GLSL | FP |
| `64-cubemaps.html:429–430` | "The engine-layer skybox — CNA::Graphics::Skybox" | DELETE SECTION (rest of page is hand-written skybox: KEEP) |
| `65-msaa.html:100, 107` | "the engine-layer route need[s]…"; "The engine-layer RenderPipeline route needs -DCNA_CNAEXT=ON" | REMOVE clauses |
| `65-msaa.html:447–452+` | section "The engine-layer alternative: FxaaPass and RenderPipeline" | DELETE SECTION |
| `66-bloom.html:98` | learn-list "the ready-made engine-layer BloomPass" | REMOVE |
| `66-bloom.html:382–402` | section "The engine-layer route: RenderPipeline and BloomPass" | DELETE SECTION |
| `67-deferred-rendering.html:404` | "the CNAEXT engine layer … offers CNA::Graphics::ClusteredForwardEffect" | REMOVE paragraph |
| `85-vulkan-backend.html:148` | "Compute shaders … are exposed through the CNAEXT engine layer (CNA::Graphics::ComputeShader, storage buffers and storage textures)" | REWRITE: no public compute API at T; only capability query |
| `130-opengl4-desktop.html:302, 335` | OpenGL4_Gl41Floor test "built when CNA_CNAEXT is on" | test removed (and OPENGL4 retired) — other researcher; REMOVE |
| `131-sdl-gpu.html:331` | "CNA's own CNAEXT shadow-map and IBL tests … engine layer's passes degrade…" | REWRITE (tests gone) |
| `131-sdl-gpu.html:332` | "CNAEXT ShaderEffect instancing is not implemented" | KEEP (marker usage, not engine) — verify separately |
| `131-sdl-gpu.html:334` | "compute and indirect drawing are CNAEXT-level features (Tutorial 115)" | REWRITE: no public compute/indirect API at T |
| `132-webgpu.html:271–276` | "modern graphics campaign … adds, for the CNAEXT engine layer …: compute shaders, storage buffers, Texture2DArray, storage textures and GPU timers … WGSL shader-package variants for the stock engine passes" | REWRITE: renderer-internal support remains; public classes and engine passes gone |
| `84-migrate-xna.html:153` | "the larger CNA:: engine layer is instead gated by CNA_CNAEXT and named with an EXT suffix" | EDIT |
| `114-pbr-materials.html:101` | "only the environment generator … needs -DCNA_CNAEXT=ON" | REMOVE clause |
| `114-pbr-materials.html:227` | "The three textures come from CNA::Graphics::EnvironmentProcessor … Tutorial 153" | REWRITE: app must supply the three textures |
| `114-pbr-materials.html:236` | "The maps come from the engine layer's ShadowMap, CascadedShadowMap, CubeShadowMap and SpotShadowMap … Tutorial 154" | REWRITE: "from a pass you write yourself (Tutorial 59)" |
| `114-pbr-materials.html:339–340, 344` | links to 153/154; "CNAEXT engine-layer reference" | REMOVE / repoint |
| `52-custom-shaders.html:353–354` | typed ctors need CNA_CNAEXT | KEEP |
| `53-effect-parameter.html:161` | typed ShaderCodeEXT/ShaderPackageEXT | KEEP |
| `160-run-parity-fixtures-and-bounded-tests.html:103` | `graphics-ext` → `CnaGraphicsExtTests` | KEEP (`cmake/UnitTests.cmake:417` at T) |
| `28-particles-2d`, `47-game-component`, `39-depth-buffer`, `56-environment-map`, `90-easy-gl:174` | user classes / easygl enum | FP |

### 5.5 Deep dives
| File:line | Claim | Disposition |
|---|---|---|
| `deep-dives/reference/cnaext-catalog.html:128` (TOC), `:144`, `:145`, `:148` | engine-layer types in CNA::*; CNA_CNAEXT "compiles the CNA::Graphics engine layer"; CnaExt umbrella | EDIT; KEEP umbrella fact |
| `…/cnaext-catalog.html:166–181` | "Graphics and model extensions" table: l.179 last row "Engine layer (CNA_CNAEXT=ON only) … render pipeline …"; "Extra draws" row (indirect) | EDIT l.179 → retro effects/DebugDraw/shader packages; add indirect-draw caveat |
| `…/cnaext-catalog.html:209–211` | section "The engine layer at a glance" (98 headers, 92 tests, six groups …) | REWRITE SECTION |
| `…/cnaext-catalog.html:231` | related links | EDIT |
| `deep-dives/reference/glossary.html:171–172` | "CNA_CNAEXT is the CMake option … that compiles the CNA::Graphics engine layer" | EDIT |
| `deep-dives/reference/glossary.html:301` | "the engine layer uses getX()/setX()" | EDIT ("graphics-ext classes") |
| `deep-dives/reference/native-c-api.html:223` | three ownership-taking routes "all in the CNAEXT engine layer" (`cna_post_process_effect_pass_create_owning`, `cna_post_process_chain_add_owned_pass`, `cna_skybox_set_owned_environment`) | DELETE paragraph (routes removed) |
| `deep-dives/reference/native-c-api.html:258` | table "CNAEXT engine layer — engine_layer.h (858), graphics_ext.h (28) — 886" | REWRITE → graphics_ext.h (44) |
| `deep-dives/reference/c-api-evidence-and-gates.html:222, 240, 257` | coverage rows graphics-ext 1,549/1,335/133; CBIND-127 "mostly the CNAEXT engine layer … StorageTexture2D, Texture2DArray …" | REWRITE (numbers changed; regenerate from CNA at T — `tools/c-api/coverage_mappings.json` changed −2,714 lines in 5572f3ca1) |
| `deep-dives/reference/ecosystem-quick-reference.html:204` | cna-city "CNAEXT at scale: cascaded shadow maps, the HDR render pipeline …" | KEEP as pinned external fact (cna-city 267b79b9) but add "uses APIs since removed from CNA" |
| `deep-dives/foundations/cna-and-xna.html:197` | "The opt-in CNA::Graphics engine layer is a set of renderer-side services over GraphicsDevice" | REMOVE sentence |
| `deep-dives/foundations/compatibility-and-evidence.html:156` | default-OFF option CNA_CNAEXT | KEEP |
| `deep-dives/platforms/cross-platform-contract.html:143` | "optional CNAEXT (CNA_CNAEXT)" | KEEP |
| `deep-dives/models/gltf-import.html:243` | factor values copied "so the engine layer's glTF material bridge can use them" | REMOVE clause (bridge gone; no public consumer of clearcoat/sheen/volume at T — SRC-qualified) |
| `deep-dives/graphics/capability-model-and-evidence.html:190` | "engine layer's capability-name table … 18 of the 19 members" | REMOVE sentence (RequireCapability gone) |
| `deep-dives/graphics/surface-formats.html:193` | "Engine-layer targets. Inside an EngineLayerTextureSizeScope…" | REMOVE item |
| `deep-dives/graphics/surface-formats.html:237` | "The one exception is a draw issued by the CNAEXT engine layer inside its float-filtering scope (VMG-0006)" | REMOVE sentence (exemption removed; rule now uniform) |
| `deep-dives/graphics/render-target-semantics.html:154` | "Inside the CNAEXT engine layer an internal EngineLayerTextureSizeScope raises the edge limit…" | REMOVE sentence |
| `deep-dives/graphics/shader-routes-four-answers.html:163–169` | figure row "CNA::Graphics engine layer shader packages (GLSL ES, GLSL 330, SPIR-V, WGSL) (CNA_CNAEXT=ON)"; caption "plus the engine layer" | EDIT → "graphics-ext packages (CRT/Depth) and ShaderEffect package ctors"; add HLSL |
| `deep-dives/renderers/renderer-contract.html:166` | "IGpuTimerRenderer, IStorageBufferRenderer, IComputeShaderRenderer, ITexture2DArrayRenderer, IStorageTexture2DRenderer — The CNAEXT modern surface used by the engine layer" | EDIT: interfaces still exist (SRC) but have no public consumer |
| `deep-dives/build/module-architecture.html:157, 222, 254` | "the CNAEXT engine layer compiles only with CNA_CNAEXT"; CNAEXT examples under graphics-ext; "groups diagnostics with the CNAEXT engine layer" | EDIT wording |
| `deep-dives/build/dependency-boundaries.html:164–165, 201–204` | CnaExt umbrella; link-closure tests | KEEP (umbrella unchanged) |
| `deep-dives/framework/game-class-and-lifecycle.html:260` | "engine-layer and pipeline exceptions" | REMOVE "engine-layer" (EngineException gone) |
| `deep-dives/framework/bounding-volumes-and-intersections.html:220` | "…and so do the frustum-culling helpers of the engine layer" | REMOVE clause (FrustumCullerEXT/ClusteredShadowPolicyEXT gone) |
| `deep-dives/sharp-runtime/components-and-consumption.html:189` | graphics-ext links Core.Base | KEEP (still true) |
| `deep-dives/graphics/texture-data-transfer.html`, `stock-effects-semantics.html:242`, `siblings/easygl-and-metagl.html:202`, `renderers/direct3d-evidence-and-wine.html:209-210`, `foundations/language-conventions.html` | FP / unrelated (`skybox` var, easygl ComputeShader feature, setenv gate history) | KEEP; but `direct3d-evidence-and-wine.html:209-210` describe `check_no_posix_setenv.py` "registered" — ctest no longer registered at T (EDIT) |

### 5.6 `development/`
| File:line | Claim | Disposition |
|---|---|---|
| dev sidebar on all internals pages | "Graphics extensions" → graphics-ext.html | KEEP link (page rewritten) |
| `development/internals/index.html:165` | module list | KEEP |
| `development/internals/modules/devices-ext.html:156, 160` | devices-ext gated by CNA_DEVICES | KEEP |
| `development/internals/modules/devices-ext.html:280` | related link "CNAEXT engine layer" | EDIT label |
| `development/internals/graphics/draw-call.html:188` | "(except inside the CNAEXT engine layer's float-filtering scope…)" | REMOVE clause |
| `development/internals/graphics/sdl-gpu.html:235` | "SdlGpuModern … hold the CNAEXT engine layer's resources" | EDIT: renderer-internal; no public consumer |
| `development/internals/graphics/sdl-gpu.html:295` | modern tests incl. `SdlGpu_StorageBufferLifetime` | sdlgpu_storage_buffer_lifetime_test removed in 5572f3ca1 — EDIT |
| `development/internals/graphics/opengl4.html:227, 274, 280, 315` | CNAEXT ComputeShader, StorageTexture2D wrapper, engine-layer side, OpenGL4_ModernStress | page subject (OPENGL4) itself retired by RRC-015 — defer to renderer researcher |
| `development/internals/bindings/c-api-internals.html:175` | "CNA::Graphics::EngineException (CNAEXT builds only) → NOT_SUPPORTED" | REMOVE row |
| `development/internals/bindings/python.html:158` | `cna.extensions.engine` "the engine layer" | flag: archived binding at its pin — KEEP as pinned fact |
| `development/internals/platforms/terminal.html:259` | "graphics-ext's kAsciiGlyphRamp" | KEEP (`kAsciiGlyphRamp` present at T in `include/CNA/Internal/Graphics/Ascii/AsciiFontAtlas.hpp`) |
| `development/architecture/graphics.html:269` | CNA-BUG-097 box | remove with issue |
| `development/handbook/change-map.html:188` | row "The CNAEXT engine layer — modules/graphics-ext … shader packages …" | EDIT |
| `development/handbook/conventions.html:165` | "engine-layer names carry the EXT suffix" | EDIT |
| `development/handbook/conventions.html:197` | row "Engine layer … check_cnaext_naming.py and check_cnaext_nodiscard.py are registered as CTest entries" | REWRITE: no longer registered at T |
| `development/handbook/conventions.html:201` | "CNAEXT_GuardDiscipline test … fails if a file is not wrapped" | EDIT: guard still followed, test unregistered |
| `development/handbook/debug-shutdown-and-lifetime.html:254` | `cnaext_leak_loop_test.cpp` row | REMOVE (file removed) |
| `development/handbook/debug-shutdown-and-lifetime.html:303` | CNA-BUG-098 box | remove with issue |
| `development/handbook/change-public-xna-behavior.html:192` | CNAEXT marker rule | KEEP |
| `development/handbook/update-the-c-api.html:233` | coverage inventory method | KEEP (generic) |
| `development/handbook/add-a-regression-test.html:188` | "add the implementation to the group's dependency list, as the content group does for cna_graphics_ext" | EDIT: content group no longer links cna_graphics_ext at T (`cmake/UnitTests.cmake` diff in 5572f3ca1); pick another example. "graphics_ext … groups link the whole umbrella" KEEP |
| `development/workflows.html:158` | "New shader-based engine-layer code … CNAEXT_GuardDiscipline test enforces" | REWRITE (test gone) |
| `development/workflows.html:163` | "the engine layer has a test for it [Doxygen]" | REMOVE clause (CNAEXT_DoxygenGroup gone) |
| `development/takeover/validation.html:177` | `cnaext` preset "The engine-layer (CNAEXT) suites" | EDIT → retro-effect suites |
| `development/takeover/review-ai-generated-code.html:211, 216` | "CTest CNAEXT_RendererDescriptorsParse"; "CTest CNAEXT_NoPosixSetenv whenever tests are built" | EDIT: both ctests unregistered at T (BLD) |
| `development/takeover/review-ai-generated-code.html:240, 245` | stats of commit 009d40f5 (CnaGraphicsExtTests 960) | KEEP (historical, about O) |
| `development/takeover/inherited.html:164` | "CNAEXT seams beyond XNA (the engine layer, device extensions)" | EDIT |
| `development/repository/index.html:219, 238, 256, 289, 332` | module row "The CNAEXT engine layer"; "the engine layer under graphics-ext"; "*ShaderPackage.generated.hpp (engine layer and examples) … 20 shader packages"; graphics-ext "92" test files | EDIT (2 packages tree-wide, 6 test files) |
| `development/repository/module-graph.html:161–267` | targets/umbrella; l.185 "always built; the extension code inside is compiled under CNA_CNAEXT"; l.267 CNA-BUG-230 | KEEP (still true) |
| `development/repository/source-ownership.html:190` | Doxyfile.cnaext "CNAEXT_DoxygenGroup (exit 77)" | EDIT (Doxyfile exists at T; ctest gone) |
| `development/repository/source-ownership.html:292` | row "CNAEXT engine layer (post-process, clustered lights, sky) … BloomPass.cpp" | REWRITE row (e.g. CRTEffect.cpp) |
| `development/build/index.html:185, 253` | cnaext preset; shader regen "engine layer" | EDIT wording |
| `development/build/architecture.html:208, 214, 356` | cna_build_config, umbrella, BUG-230 | KEEP |
| `development/testing/architecture.html:179` | content group links "cna_content, cna_graphics_ext" | EDIT → cna_content only (UnitTests.cmake diff in 5572f3ca1) |
| `development/testing/architecture.html:187` | "graphics_ext CnaGraphicsExtTests 92" | EDIT → 6 |
| `development/testing/architecture.html:256` | "CNAEXT_* … naming, guard, matrix, accessor and Doxygen rules" | REMOVE (0 CNAEXT_* ctests) |
| `development/testing/architecture.html:450–451` | VGAP-017/018 boxes | remove with issues |
| `development/testing/index.html:162` | graphics-ext group | KEEP; `:277` BUG-200 box — update with issue |
| `development/debugging.html:203–204` | "the engine layer writes GLSL ES 3.00 (compute GLSL ES 3.10)…" | EDIT ("retained graphics-ext shaders") |
| `development/reference/public-headers.html:146` "graphics-ext (98)"; `modules.html`, `cmake-options.html`, `test-targets.html` | **generated** from O by `scripts/generate_dev_reference.py` | REGENERATE at T (graphics-ext 11 + 2 internal) |

### 5.7 Known issues (`data/known-issues.json`; HTML under `known-issues/` is generated from it)

Engine-subject or engine-touching ids (Python scan of each issue's JSON for the engine regex):

| ID | Subject | Status at T | Disposition |
|---|---|---|---|
| CNA-BUG-097 | RenderPipeline::releaseDeviceResourcesEXT keeps pass pools | RenderPipeline/BloomPass/SsaoPass/VolumetricFogPass deleted | **RETIRE** (resolved by removal in 5572f3ca1) |
| CNA-BUG-098 | throwing shadow/transparent callback leaves RenderPipeline/ShadowMap unrecoverable | deleted | **RETIRE** |
| CNA-BUG-109 | engine capability-name table lacks IndirectDraw | RequireCapability.hpp/.cpp deleted | **RETIRE** |
| CNA-BUG-270 | @param of `cna_post_process_chain_add_owned_pass`, `cna_skybox_set_owned_environment` | routes and engine_layer.h deleted (ABI 0.30.0) | **RETIRE** |
| CNA-GAP-031 | ClusteredForwardEffect binds no material textures | deleted | **RETIRE** |
| CNA-VGAP-017 | graphics-ext shader-package drift guards (shadow_caster, clustered-forward) | those packages deleted; only `post_process` + its reproducibility ctest remain | **RETIRE** (or rewrite as "remaining package covered; still no CI") |
| CNA-VGAP-018 | no test asserts RenderPipeline pass order | deleted | **RETIRE** |
| CNA-GAP-032 | "Engine-layer PBR limits": one punctual light per PbrEffect draw (still true, `PbrEffect.hpp`), 8-bit EnvironmentProcessor cubes (gone), no back-face normal flip (PbrEffect—re-verify), no alpha-tested shadow casters (engine shadow_caster shaders gone) | partly obsolete | **REWRITE** as PbrEffect limits only; drop engine items and `modules/graphics-ext/...` sources |
| CNA-BUG-094 | SDL_GPU claims compute/SPIR-V on D3D12/Metal | renderer claim may persist (`SupportsComputeShadersEXT` still renderer-internal); public `ComputeShader` example (detail l.123, l.131) gone | **REWRITE** detail/impact: SPIR-V package selection (CRT/Depth, ShaderEffect) is the remaining public exposure; re-verify at T |
| CNA-BUG-200 | registered CTest `CNAEXT_NoPosixSetenv` fails | ctest **unregistered** at T (registration lived in graphics-ext examples CMake, deleted in 5572f3ca1); script remains | **REWRITE/CLOSE**: the failing gate no longer exists; whether Wayland setenv calls remain is a separate question |
| CNA-GAP-029 | EasyGL GPU timers 32-bit | `EasyGLGpuTimerRenderer` still in `EasyGLRenderer.cpp` (14 matches); public consumer `GpuTimer` deleted | **REWRITE**: renderer-internal only, no public API exposes it; drop `GpuTimer.cpp` source and GpuTimerTests/PassTimingTests evidence |
| CNA-BUG-071 | BoundingFrustum::Intersects | math bug, unaffected | KEEP; remove `modules/graphics-ext/src/FrustumCullerEXT.cpp` from sources |
| CNA-BUG-230 | SharedRuntimeLibrary.cmake comment "exist only with CNA_CNAEXT" | comment still present at T (`cmake/SharedRuntimeLibrary.cmake:145`); both modules still always added | **KEEP** (still valid) |
| CNA-BUG-274 | README calls purity check "a dedicated CMake build option" | still at T (`README.md:51`) | KEEP (repoint its `docs/cnaext-engine.html` related link — URL kept) |
| CNA-BUG-181 | Sdl3Platform nativeFileDialog | unrelated | KEEP (related link only) |
| CNA-VGAP-056 | renderer shader generators lack --check | unrelated; text cites "graphics-ext shader packages set the standard … one reproducibility CTest per package" (l.110, 120, 122) | KEEP; EDIT those sentences (now 1 package) |
| CNA-GAP-062 (l.112, 124) | C coverage rows "graphics-ext 133", CBIND-127 "predominantly the CNAEXT engine layer" | counts changed | REWRITE numbers (C-API researcher) |
| CNA-BUG-111 (l.110) | cites `ShaderEffect::SetTextureArrayEXT` as the ObjectDisposed precedent | method removed | EDIT example |
| CNA-BUG-246 (l.112) | graphics-resource-lifetime.md mentions Texture2DArray | re-verify CNA doc at T | flag |
| CNA-BUG-002 (l.128), CNA-BUG-004 | "used by FrustumCullerEXT and ClusteredShadowPolicyEXT" | consumers gone | EDIT clause |
| CNA-VGAP-047 (l.112) | cnaext-coverage.md "for the graphics-ext layer only" | still a (historical) file | KEEP/EDIT |
| CNA-GAP-065 (l.112) | ShaderDialect profile | unrelated | KEEP |
| Prev/next-only mentions: CNA-BUG-096, 099, 107, 110, 199, 201, 229, 231; CNA-GAP-030, 033; CNA-VGAP-016, 019; index pages | regenerate after retirements | — |

### 5.8 Data, scripts, generated artefacts
| File:line | Content | Disposition |
|---|---|---|
| `data/current-facts.json` `facts.c_abi_version` (0.29.0), `c_api_headers` (61), `c_api_routes` (4055) ~l.108–124; `external_pinned.bindings_expected_abi.note` "TARGET exports 0.29.0" | all changed by retirement (0.30.0 / 60 / 3,213) and later commits (T: 0.44.0 / 60 / 3,210) | UPDATE (C-API researcher owns final values). No other engine-specific fact keys found. |
| `scripts/site_nav.py:41` | `("cnaext-engine.html", "CNAEXT Engine Layer")` | EDIT label |
| `scripts/build_site_indexes.py:36` | keywords `["cnaext","engine","pbr","shadows","ibl","extensions"]` | EDIT (e.g. "retro","crt","ascii","debugdraw") |
| `scripts/build_site_indexes.py:183` | sitemap priority set incl. cnaext-engine | KEEP (URL kept) |
| `scripts/dev_manifest.py:298–299` | title "Graphics extension pipeline internals" | EDIT title |
| `scripts/generate_dev_reference.py:104` | module → page map | KEEP |
| `scripts/make_architecture_diagram.py:174` → `img/architecture-diagram.svg:170` (and l.171 "C ABI 0.29.0") | box text "CNAEXT engine layer · Diagnostics" | EDIT script → e.g. "CNAEXT retro effects · Diagnostics", regenerate SVG |
| `scripts/issues_candidates.py:70` | internal triage heuristic | KEEP |
| `sitemap.xml:899, 1169` (keep), `1624, 1629` (153/154), `2419, 2424, 2469, 2904, 3244, 3424, 3779, 3784` (retired issues) | | regenerate |
| `search-index.json` (801 entries) | generated | regenerate |
| `tutorials.html:366–367` (JSON-LD ListItems 145/146), `:1562–1571` (cards 153/154), `:428` "All 151 tutorials available" | | REMOVE entries; count → 149 |
| `tutorials.html:333–334, 1294–1303` (115/116 cards) | | KEEP (titles fine; 116 title still accurate) |

---

## 6. Inbound links for pages to delete (excluding `audit/`), with suggested targets

| Deleted page | Inbound files (non-audit) | Suggested replacement target |
|---|---|---|
| `docs/tutorials/153-image-based-lighting.html` | `tutorials.html` (l.366, 1562), `docs/cnaext-engine.html` (l.538), `docs/effects.html` (l.344), `docs/tutorials/114-pbr-materials.html` (l.227, 339), `docs/tutorials/115-cnaext-overview.html` (l.308), `docs/tutorials/116-post-process-effects.html` (l.350), `docs/tutorials/154-cascaded-shadows.html`, `sitemap.xml:1624`, `search-index.json` | `docs/tutorials/114-pbr-materials.html` (IBL-receiving section) |
| `docs/tutorials/154-cascaded-shadows.html` | `tutorials.html` (l.367, 1567), `docs/cnaext-engine.html` (l.539), `docs/effects.html` (l.344), `docs/tutorials/59-shadow-mapping.html` (l.328), `docs/tutorials/114-pbr-materials.html` (l.236, 340), `115-cnaext-overview.html` (l.308), `116-post-process-effects.html` (l.350), `153-image-based-lighting.html`, `sitemap.xml:1629`, `search-index.json` | `docs/tutorials/59-shadow-mapping.html` (hand-written shadows + receivers) |
| Known-issue pages CNA-BUG-097 / 098 | `docs/cnaext-engine.html`, `development/internals/modules/graphics-ext.html`, `development/architecture/graphics.html:269` (097), `development/handbook/debug-shutdown-and-lifetime.html:303` (098), prev/next neighbours 096/098/099, bugs index | remove boxes; neighbours regenerate |
| CNA-BUG-109 | graphics-ext internals, neighbours 107/110, index | remove |
| CNA-BUG-270 | `docs/c-api.html:241`, `deep-dives/reference/native-c-api.html` (l.223 area), neighbours 269/271, index | remove (paragraph deleted anyway) |
| CNA-GAP-031 | `docs/cnaext-engine.html`, graphics-ext internals, neighbours 030/032, index | remove |
| CNA-VGAP-017 / 018 | `docs/cnaext-engine.html`, graphics-ext internals, `development/testing/architecture.html:450-451`, neighbours 016/018/019, index | remove |
| If editors instead delete `docs/cnaext-engine.html` (not recommended: 90 inbound files incl. every docs sidebar) | best target `docs/tutorials/116-post-process-effects.html` (retro effects) or `deep-dives/reference/cnaext-catalog.html` (marker) | — |
| If editors delete `development/internals/modules/graphics-ext.html` (38 inbound incl. `dev_manifest.py`, `generate_dev_reference.py`, `change-map.html:188`, `conventions.html`, `source-ownership.html`, `opengl4.html:280`, `shader-routes-four-answers.html`, `cnaext-catalog.html`) | best target `development/internals/modules/core.html` or the rewritten docs page | — |

---

## 7. Caveats and things not verified
- Nothing was built or run. All T facts are SRC/BLD from git objects; CNA's validation numbers (78/78, 17/17, 3,213 exports) are CNA-REC.
- Whether CRT/Depth actually render on DIRECTX11/12/9 at T is RT/PLAT-unverified (HLSL variant exists; DX11 accepts `Hlsl` in source).
- ShaderPackageEXT language preference order quoted on the internals page was not re-verified at T.
- OPENGL4, GDI, HTML_DOM, SVG_DOM, FreeDirect, Direct2D, PortableGL retirements (RRC-012/015) make renderer tables on these pages stale independently; another researcher should own those.
- ABI/route totals at T (0.44.0 / 3,210) include later, non-engine changes; quote them only with that qualification.
- `CMakePresets.json` `cnaext` preset description and `cmake/SharedRuntimeLibrary.cmake:145` comment are stale inside CNA itself (do not repeat them as facts).
