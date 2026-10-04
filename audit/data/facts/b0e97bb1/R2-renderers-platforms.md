# R2: Renderers, platforms and audio, CNA O=009d40f5 → T=b0e97bb1

INTERNAL NOTES. This file names the removed identities. The public site must not.
Pins: O=`009d40f5dd085c4e674d3479675fac84b12b3e0a` (2026-09-24, "merge(OpenGL4ModernGraphics)"), T=`b0e97bb1bb876f9b3edd6f4ff1ef3067908ae8ac` (2026-10-04). `git log O..T` contains 456 commits.
CNA was read only through git objects. The site was read in its working tree, which already holds another agent's footer/snapshot edits to 808 files. Grep counts are identical at HEAD and in the working tree.

## Executive summary (canonical numbers at T)

1. **18 public renderer identities over 14 implementation families** (O: 25/21). EasyGL implements 5 of them: OPENGLES2, OPENGLES3, OPENGL33, WEBGL1, WEBGL2. Sources: `cmake/RendererIdentities.cmake` L25-28, `cmake/RendererRegistry.cmake` L28-48, `docs/renderer-registry.md`.
2. Removed between O and T: DIRECT2D, FREEDIRECT, PORTABLEGL (`0f96ea703`, RRC-012, 2026-09-27) and GDI, HTML_DOM, SVG_DOM, OPENGL4 (`261cb5f7f`, RRC-015, 2026-09-28). `200d08fb6` (RRC-014) moved the GDI-only Software contracts first, `590ac27c8` (RRC-016) removed CNA_SOFTWARE_2D_ONLY, and `3b9982646` (RRC-017) wrote the docs record. Merge `38e2209fb` (2026-09-29) brought RRC-014..017 into `next`; RRC-012 was already there. **None is replaced.** All 7 names are refused by name at configure time, and their C ABI values 16/21/46/18/40/44/33 stay reserved.
3. **Default renderer, unchanged from O:** WEBGL2 under Emscripten, OPENGLES3 on Linux, SDL_RENDERER everywhere else (Windows, macOS, Android, iOS). Source: `cmake/RendererIdentityDefault.cmake`.
4. **Deliberately 2D-only (ThreeD = false): 2, SDL_RENDERER and CANVAS** (O: 7). STUB answers false to every capability (a no-op renderer, not a 2D one). HEADLESS reports ThreeD = true.
5. **GraphicsCapability has 19 members**, unchanged; only doc comments changed.
6. **Compiled XNA effects (.fxb / XNB Effect): 13 identities in 9 families** (O: 14 in 10). FNA3D is always on. Eight options default to OFF: CNA_{EASYGL,VULKAN,WEBGPU,SOFTWARE,DIRECTX11,DIRECTX12,DIRECTX9,SDL_GPU}_COMPILED_EFFECTS. CNA_OPENGL4_COMPILED_EFFECTS is gone. MojoShader fixes FX-140..146 (2026-10-01..04) landed for the GLSL/GLSL ES routes.
7. **Compute shaders and indirect draws:** EasyGL (only on a runtime context of desktop GL ≥4.3 for compute / ≥4.0 for indirect, or ES ≥3.1; never WebGL), SDL_GPU, VULKAN, WEBGPU, and now **DIRECTX11 and DIRECTX12** (feature level ≥11_0; WIN11 merge `7301f386a`). OPENGL4's own implementation was deleted, not moved. EasyGL already had compute and indirect at O.
8. **Platforms (CNA_PLATFORM): 6**, O had 7 including SDL2. SDL3 (default) and HEADLESS everywhere. WIN32 on Windows targets only. TERMINAL on POSIX only. X11 and WAYLAND where their dev libraries exist.
9. **Audio (CNA_AUDIO_PLATFORM): 3**, O had 4. SDL3 (default), NULL, ALSA (Linux only). SDL2 was retired in `76c9bda29`, with its contract locked in `6ee00e35d`. `-DCNA_PLATFORM=SDL2` and `-DCNA_AUDIO_PLATFORM=SDL2` now fail with "not a known (audio) platform". There is no alias.
10. **Renderer combination rules: 1, the platform partition** (O: 3). Windows-only {DX9, DX11, DX12}, Emscripten-only {WEBGL1, WEBGL2, CANVAS}, macOS-only {METAL}. The rules "SDL_RENDERER/SDL_GPU/FNA3D need SDL" (3 renderers, O: 4) and "TERMINAL accepts only SOFTWARE/HEADLESS/STUB" still apply.
11. **CI: 18 workflow files, 26 jobs** (O: 20/28). Deleted: `gdi-windows-ci.yml`, `htmldom-ci.yml`. The DIRECT2D leg left `d3d-windows-ci`, the SDL2 row left `platform-ci`, and the Emscripten multi job is now WEBGL2+WEBGL1+CANVAS. **CMakePresets.json is byte-identical between O and T** (18 configure, 17 build presets).
12. Windows 2D now: SDL_RENDERER (default, 2D-only), SOFTWARE presented through the Win32 platform's surface presenter (gdi32 StretchDIBits), or DIRECTX9/11/12, SDL_GPU, FNA3D. Browser: WEBGL2 (default), WEBGL1, CANVAS (2D-only), WEBGPU (experimental, emdawnwebgpu).
13. Notable at T: WebGPU per-draw binding work (street frame 91-95 → 26-29 ms). STREETPERF: Vulkan 120 → 27-28 ms, SDL_GPU and WebGPU no longer copy geometry per draw. DirectX9 fullscreen/motion fixes. DX11/DX12 validated on one physical Intel Iris Xe laptop running Windows 11 (WIN11). EasyGL threading and offscreen back buffer (KF-*).
14. **Site impact:** the site's own gate `scripts/check_retired_renderers.py` (read-only run) flags **2079 lines in 330 files**: 1471 lines in 234 authored files, 389 in 88 known-issues pages, and 219 in generated files. The gate does **not** catch "OpenGL 4" (29 files), "free-direct"/"free-api" (45 files), "DirectDraw" (45 files), CNA's SDL2 (110 pages, 587 hits) or stale counts.
15. **8 dedicated pages:** delete 5 (windows-2d-renderers, freedirect-and-freeapi, internals/graphics/opengl4, internals/platforms/sdl2, tutorial 130). Rewrite 3 (browser-dom-renderers → CANVAS-only, tutorial 105 → CANVAS, tutorial 107 → drop PortableGL). free-direct and free-api still exist as independent openeggbert repos, but CNA at T has no build reference to them.

---

## 1. Identity → family ownership, defaults, selection

### 1.1 Map at T (`cmake/RendererRegistry.cmake` `_cna_renderer_identity_map`, L28-48; `docs/renderer-registry.md`)

| C ABI | Identity | Family dir (`modules/renderers/`) | Namespace / accessor | Platform gate (configure) | 2D-only | Compiled FX option | Compute / indirect |
|---:|---|---|---|---|---|---|---|
| 1 | SDL_RENDERER | sdl-renderer | SdlRenderer | none (needs SDL3) | **yes** | — | no |
| 2 | OPENGLES2 | easygl | EasyGL\|GetDescriptorOpenGLES2 | non-Emscripten | no | CNA_EASYGL_COMPILED_EFFECTS | runtime: ES ≥3.1 |
| 3 | OPENGLES3 | easygl | EasyGL\|GetDescriptorOpenGLES3 | non-Emscripten (Linux default) | no | same | runtime: ES ≥3.1 |
| 4 | OPENGL33 | easygl | EasyGL\|GetDescriptorOpenGL33 | non-Emscripten | no | same | runtime: GL ≥4.3 / ≥4.0 |
| 5 | WEBGL1 | easygl | EasyGL\|GetDescriptorWebGL1 | Emscripten only | no | same | never (WebGL) |
| 6 | WEBGL2 | easygl | EasyGL\|GetDescriptorWebGL2 | Emscripten only (default there) | no | same | never (WebGL) |
| 8 | VULKAN | vulkan | Vulkan | Vulkan SDK/runtime | no | CNA_VULKAN_COMPILED_EFFECTS | yes |
| 9 | WEBGPU | webgpu | WebGPU | wgpu-native; emdawnwebgpu port under Emscripten | no | CNA_WEBGPU_COMPILED_EFFECTS | yes (device present) |
| 11 | HEADLESS | headless | Headless | none | no (ThreeD true, no pixels) | — | no |
| 12 | SOFTWARE | software | Software | none | no | CNA_SOFTWARE_COMPILED_EFFECTS | no |
| 13 | STUB | stub | Stub | none | (all capabilities false) | — | no |
| 14 | DIRECTX11 | directx11 | DirectX11 | Windows only | no | CNA_DIRECTX11_COMPILED_EFFECTS | yes (FL ≥11_0), **new since O** |
| 15 | DIRECTX12 | directx12 | DirectX12 | Windows only | no | CNA_DIRECTX12_COMPILED_EFFECTS | yes (FL ≥11_0), **new since O** |
| 17 | CANVAS | canvas | Canvas | Emscripten only | **yes** | — | no |
| 22 | DIRECTX9 | directx9 | DirectX9 | Windows only | no | CNA_DIRECTX9_COMPILED_EFFECTS | no |
| 31 | SDL_GPU | sdl-gpu | SdlGpu | needs SDL3 (SDL GPU) | no | CNA_SDL_GPU_COMPILED_EFFECTS | yes |
| 42 | METAL | metal | Metal | macOS only (iOS refused unless CNA_APPLE_ALLOW_UNVALIDATED_RENDERER) | no | — | no |
| 43 | FNA3D | fna3d | Fna3d | FNA3D dependency, needs SDL3 | no | always on | no |

Evidence:
- The 14 family directories with `src/` at T are canvas, directx11, directx12, directx9, easygl, fna3d, headless, metal, sdl-gpu, sdl-renderer, software, stub, vulkan and webgpu (`git ls-tree T modules/renderers/`). `common/` has no src.
- O also had direct2d, freedirect, gdi, html-dom, opengl4, portablegl and svg-dom, for 21.
- The registry map at O had 25 rows: + PORTABLEGL, DIRECT2D, HTML_DOM, SVG_DOM, FREEDIRECT, OPENGL4, GDI.
- `CNA_GRAPHICS_RENDERER_MAXIMUM` is FNA3D (43) at T (`modules/c-api/include/CNA/C/graphics.h` L72). The next new value is 52.
- The C ABI moved 0.29.0 → **0.44.0** between O and T (`abi.h`). That number is outside R2. Per `docs/removed-renderers.md`, the retirements contributed bumps to 0.31.0 and 0.33.0.

### 1.2 Defaults (build-time, `cmake/RendererIdentityDefault.cmake`, unchanged O→T)
`if(EMSCRIPTEN) WEBGL2 elseif(CMAKE_SYSTEM_NAME STREQUAL "Linux") OPENGLES3 else() SDL_RENDERER`. That gives Windows, macOS, Android, iOS and tvOS SDL_RENDERER. The iOS allow-list is SDL_RENDERER only (`cmake/ApplePlatform.cmake` L246-248); `docs/renderer-registry.md` restates the same rule.

### 1.3 Selection rules at T (unchanged in behaviour O→T except the removals)

**Single-renderer build (default and recommended)**
- `-DCNA_GRAPHICS_RENDERER=<X>` selects one renderer per build.
- An empty value means the per-host default.

**Multi-renderer build**
- `CNA_GRAPHICS_RENDERERS="A;B;..."` is the opt-in list.
- `CNA_GRAPHICS_RENDERER` must be a member of the list, or configure fails with FATAL_ERROR (`cmake/RendererDefaultSelection.cmake` L34-67). It is not silently substituted.
- The default is reordered to the front of the list.

**Configure-time refusal of retired and unknown names**
- `cna_validate_renderer_identity_selection()` checks every route: CNA_GRAPHICS_RENDERER, each member of CNA_GRAPHICS_RENDERERS, and any `CNA_RENDERER_<RETIRED>=ON` (`cmake/RendererIdentities.cmake` L87-105).
- A retired name gets "has been retired ... not replaced ... C ABI value N stays reserved".
- An unknown name gets "unknown graphics renderer".

**Runtime selection** (`docs/runtime-renderer-selection.md`), in precedence order:
1. `GraphicsRendererSelection::SetPreferred()`.
2. The `CNA_GRAPHICS_RENDERER` environment variable.
3. The compile-time default.
- A name that is not compiled in throws.
- Emscripten pages can set `Module.cnaPreferredRenderer` or call `ccall("cna_set_preferred_renderer")`.
- RRC-015 added a runtime test that SetPreferred refuses retired names in any spelling.

**Fallback**
- Default policy is a hard failure.
- Opt-in with `SetFallbackChain()` or `EnableAutomaticFallback(true)`. Each step is logged and recorded in `GetFallbackHistory()`.
- `GetSelected()` and `GetActive()` may differ.
- Test seams: `CNA_DEBUG_UNAVAILABLE_RENDERERS` and `CNA_DEBUG_FAIL_RENDERER_INIT`.
- The latch: the selection is frozen after the first GraphicsDevice.

**What changed O→T in selection (from `git diff O T` of cmake/Renderer*.cmake, SdlAvailability, PlatformSelection, AudioPlatformSelection and CMakeLists)**
- 7 `option(CNA_RENDERER_*)` switches and their dispatch arms were removed.
- The Windows-only gate is now DX9/11/12 (DIRECT2D and GDI dropped).
- The HTML_DOM and SVG_DOM Emscripten gates were removed.
- The TERMINAL renderer list is now `SOFTWARE HEADLESS STUB` (PORTABLEGL dropped).
- The SDL-requiring renderer list is now `SDL_RENDERER SDL_GPU FNA3D` (FREEDIRECT dropped).
- The `../free-direct` sibling `add_subdirectory` was removed, so **easy-gl is the only renderer sibling left**. It gained a `CNA_EASYGL_ROOT` cache path, default `../easy-gl`.
- Combination rules went from 3 to 1: the PORTABLEGL-vs-real-GL and GDI+SOFTWARE rules were removed (`cmake/RendererCombinations.cmake`).
- The verified multi-renderer sets now listed in the CNA doc:
  - `HEADLESS;SOFTWARE;STUB`
  - `WEBGL2;WEBGL1;CANVAS` (headless Chrome, 2026-09-28, not in CI)
  - `SDL_RENDERER;OPENGLES3;SOFTWARE;HEADLESS;STUB`
  - `OPENGLES3;OPENGLES2;OPENGL33;SOFTWARE;HEADLESS` (6385/0)
  - `OPENGLES3;VULKAN;SOFTWARE;HEADLESS;STUB` (6385/0)
- The defaults did not change.

## 2. 2D-only identities and GraphicsCapability

| Identity | Evidence at T | Claim class |
|---|---|---|
| SDL_RENDERER | `SdlRenderer.hpp` L196-201: `SupportsCapability(c) { return c == AdditiveBlending; }` ("The renderer is 2D-only") | source |
| CANVAS | `CanvasRenderer.hpp` L114-119: same pattern ("Canvas is 2D-only") | source |
| (STUB) | `StubRenderer.hpp` L175-178 `return false;` for all; registry calls it "No renderer" | source |

- Every other family answers ThreeD true: through explicit cases (DX11 L1434, DX12 L3130, SDL_GPU L2682, Vulkan L3163, MetalPolicy L175) or through `default: return true` / the base default in `IGraphicsRenderer.hpp` L3760-3784 (DirectX9, EasyGL, FNA3D, Headless, Software, WebGPU).
- `docs/renderer-registry.md` capability classes:
  - "2D-oriented: SDL_RENDERER and CANVAS"
  - "CPU bounded 3D: SOFTWARE"
  - "No renderer: STUB, HEADLESS"
  - "Abstraction layer: FNA3D"
- At O the 2D-only list in code was SDL_RENDERER, CANVAS, FREEDIRECT, DIRECT2D, GDI, HTML_DOM and SVG_DOM (7). The site's `data/current-facts.json` matches that.
- 2D-only renderers still throw on 3D calls by default, or warn and stub under `Unsupported3DGraphicsCallBehavior::WarnAndStub` (`CNA/Unsupported3DGraphicsCallBehavior.hpp`). Source-verified.
- **GraphicsCapability has 19 members** at both O and T, verified by parsing `modules/graphics/include/CNA/GraphicsCapability.hpp`: ThreeD, DepthStencilBuffer, MultiSampleAntiAliasing, MultipleRenderTargets, AnisotropicFiltering, WireFrame, OcclusionQuery, CustomEffects, Texture3D, MultiStreamVertexInput, Instancing, StencilBuffer, AdditiveBlending, CompiledEffects, FloatRenderTargets, HalfFloatRenderTargets, HalfFloatTextureLinearFiltering, ComputeShaders, IndirectDraw.
  - The O→T diff touches comments only. The GDI, HTML_DOM and CNAEXT-engine HDR/Bloom wording was removed.
  - `CNA_GRAPHICS_CAPABILITY_MAXIMUM` = INDIRECT_DRAW.

## 3. Compiled XNA effects

**Options at T** (`cmake/RendererSelection.cmake`), all `OFF` by default:

| Line | Option | Plan reference |
|---:|---|---|
| L251 | CNA_EASYGL_COMPILED_EFFECTS | FX-062 |
| L272 | CNA_VULKAN_COMPILED_EFFECTS | FX-065 |
| L293 | CNA_WEBGPU_COMPILED_EFFECTS | WEBGPU-167 |
| L321 | CNA_SOFTWARE_COMPILED_EFFECTS | — |
| L342 | CNA_DIRECTX11_COMPILED_EFFECTS | FX-063 |
| L357 | CNA_DIRECTX12_COMPILED_EFFECTS | FX-134 |
| L378 | CNA_DIRECTX9_COMPILED_EFFECTS | FX-070 |
| L418 | CNA_SDL_GPU_COMPILED_EFFECTS | FX-061 |

O additionally had `CNA_OPENGL4_COMPILED_EFFECTS` (GL4-0020), also OFF.

**Support in code**
- `SupportsCompiledEffects() override { return true; }` sits under `#if defined(CNA_<X>_COMPILED_EFFECTS)` in the EasyGL, Vulkan, WebGPU, DX9, DX11, DX12 and SDL_GPU headers.
- Software returns true or false under `#if` (`SoftwareRenderer2DState.cpp` L420-427).
- FNA3D returns true unconditionally (`Fna3dRenderer.hpp` L1394).
- METAL, SDL_RENDERER, CANVAS, HEADLESS and STUB have no override, so they report false.

**Count at T: 13 identities in 9 families**
- 13 identities: EasyGL ×5, VULKAN, WEBGPU, SOFTWARE, DX9, DX11, DX12, SDL_GPU, FNA3D.
- 9 families: easygl, vulkan, webgpu, software, directx9, directx11, directx12, sdl-gpu, fna3d.
- Only FNA3D has the path on by default.
- **O: 14 identities in 10 families** (+OPENGL4). This confirms the site's current fact.

**Caveat: stale CNA doc.** `docs/fx-compiled-effects.md` §10 "Renderer support matrix" (unchanged O→T) lists only FNA3D, SDL_GPU, the EasyGL family, VULKAN, DX11 and DX12, and says "every other renderer identity false". That disagrees with the code and options for WEBGPU, SOFTWARE and DIRECTX9, each of which has a compiled-effect implementation and tests:
- `WebGPUCompiledEffect.cpp` + `WebGPUCompiledEffectTests.cpp` + `webgpu_browser_compiled_effect_test.cpp`
- `SoftwareCompiledEffect.cpp` + `SoftwareCompiledEffectConformanceTests.cpp`
- `D3D9CompiledEffect.cpp` + `DirectX9CompiledEffectTests.cpp`

Use the code-derived 13/9 and classify it as source + tests exist. Do not claim CI execution.

**FX-140..146 (all O..T; MojoShader patches pinned in `cmake/ThirdPartyFNA3D.cmake`):**

| Commit | Ticket | Fix |
|---|---|---|
| `1c2923efd` | FX-140 | vs_3_0 point-size/fog output is a scalar write on GLSL (a resonance-game effect failed on EasyGL/Mesa) |
| `46231e857` | FX-141 | ps_3_0 may mix abs and ordinary constant reads (escape-from-enceladus); the SOFTWARE-410 refusal was lifted |
| `fb5cb3ba2` | FX-142 | an SM1 pixel shader's colour input is not centroid at link time on GLSL ES (Racing Game Kit) |
| `d9d599263` | FX-143 | GLSL ES 3 `precision highp sampler3D`, so volume samplers compile on OPENGLES3/WEBGL2 (684/686) |
| `47b5f7665` | FX-144 | test-only, meta-gl init |
| `26b477686` | FX-145 | GLSL ES 3 samples sampler2D/samplerCube at highp (variance shadow maps; regression fixture built with XNA's EffectProcessor) |
| `1e12bd3a0` | FX-146 | emulates the GLES vertex-sampler LOD bias (`docs/sampler-state-support.md` updated) |

Class: source plus focused tests on Linux/Mesa. They mostly affect the EasyGL GLSL/GLSL ES routes, and therefore WebGL too.

## 4. OPENGL4's "modern graphics"; Windows 2D and browser options

**What OPENGL4 had at O** (`docs/opengl4-renderer.md` at O):
- A desktop GL 4.1 core context with native X11/Wayland/SDL3 and its own gl4 loader.
- The full classic XNA surface, plus compiled effects through GLSL 1.20.
- A CNAEXT "modern" surface: compute (GLSL 4.30 on 4.3+), storage and constant buffers, storage textures, indirect draws, GPU timers.

**Was any of it moved?**
- **No.** RRC-015: "OPENGL33 stays CNA's desktop OpenGL identity with its 3.3 contract (there is no EasyGL OpenGL 4 profile)". Modern-GPU work is covered by VULKAN, DIRECTX12, METAL, WEBGPU and SDL_GPU (`docs/removed-renderers.md`, 2026-09-28 table).
- The only thing moved is two headers, `GlStockShaderSources.hpp` and `GlPresentationSurfaceState.hpp`, back from Common/ into `modules/renderers/easygl`.

**What exists at T for compute and indirect** (`Supports{ComputeShaders,IndirectDraw}EXT` overrides; base default false at `IGraphicsRenderer.hpp` L3115/3122):
- **EasyGL already had** compute and indirect at O (`EasyGLRenderer::DispatchCompute` exists at O L6981 and T L7304). It answers from the runtime context:
  - ES ≥3.1, or desktop ≥4.3 for compute and ≥4.0 for indirect.
  - Never on WebGL (`EasyGLRenderer.cpp` L7122-7147).
  - So an OPENGL33 build on a 4.6 driver does report compute. That is runtime-qualified and driver-dependent.
- SDL_GPU: device present.
- VULKAN.
- WEBGPU: device present.
- **DIRECTX11** (WIN11-0029 `02f2c5e99` indirect, WIN11-0030..0032 `6e27d7b14` compute/images) and **DIRECTX12** (WIN11-0064 `cfe31a083` compute, WIN11-0065 `d58dbadac` indirect), both FL ≥11_0. These are **new since O** via merge `7301f386a`.
- METAL and FNA3D: false.

**Caveat:** MOD-RETIRE-1 (`5572f3ca1`, 2026-09-27, −180,609 lines, mostly `modules/graphics-ext`) retired the CNAEXT graphics engine layer: shadows, IBL, clustered lighting and similar. WIN11 "engine" features such as DX11 stock shadows, IBL, clustered forward and GPU particles may not survive at T. `plan_windows11_directx.md` notes the owner removed graphics CNAEXT from WIN11 scope on 2026-09-27. Another agent should own CNAEXT claims. Only the compute/indirect capability overrides above are verified at T.

**Windows 2D at T.** None of the removed renderers is replaced. What remains:
- SDL_RENDERER: the Windows default and 2D-only.
- SOFTWARE: CPU. Its descriptor sets `needsSurfacePresenter = true` (`SoftwareRendererDescriptor.cpp` L47), and on `CNA_PLATFORM=WIN32` it presents through `Win32GraphicsServices.cpp` StretchDIBits (L534). Source-verified; no CI job runs SOFTWARE+WIN32. The `win32-*` CI jobs build the standalone platform harness.
- DIRECTX9, DIRECTX11 and DIRECTX12, which handle SpriteBatch 2D fine.
- SDL_GPU, FNA3D, and the GL/Vulkan/WebGPU identities.
- Avoid the word "GDI" on the site (the gate flags it). Say "Win32 surface presenter (gdi32 StretchDIBits)" if needed.

**Browser at T:**
- WEBGL2 (default) and WEBGL1, both EasyGL profiles. In a bundle that contains WEBGL2, WEBGL1 runs on a WebGL 2 context.
- CANVAS: Canvas 2D, 2D-only.
- WEBGPU: through Emscripten's emdawnwebgpu port (`cmake/ThirdPartyWebGPU.cmake` L21-35). Experimental per the registry doc.
- The Emscripten multi-renderer CI bundle is `WEBGL2;WEBGL1;CANVAS`, workflow name "One wasm bundle, three renderers".
- `docs/runtime-renderer-selection.md`: in headless Chrome on 2026-09-28 the benchmark ran under each of the three. That run is "Not automated in CI" (the CI job builds and asserts the archive and registry).

## 5. SDL2 retirement (`76c9bda29` refactor, `6ee00e35d` contract test, `2707098fa` docs-only NEXT_platform.md; all 2026-10-04)

**Removed** (`git show --stat 76c9bda29`, 70 files, −2838):
- The platform: `modules/platform/src/Sdl2/{Sdl2Platform,Sdl2SystemServices,Sdl2Window}.{cpp,hpp}`.
- Audio: `modules/audio/src/Platform/Sdl2/Sdl2AudioDevice.{cpp,hpp}`.
- CMake: `cmake/ThirdPartySDL2.cmake`, `cmake/Sdl2OnlyConfiguration.cmake`, `cmake/Tests/Sdl2OnlyRendererGate.cmake`.
- Docs: `docs/platform-sdl2.md`.
- Tests: Sdl2PlatformTests and Sdl2AudioDeviceTests.
- CI: the `platform-ci.yml` "SDL2 + OpenGLES3" matrix row (platform-contract rows 6 → 5).
- Cache vars: `CNA_SDL2_ROOT`, `CNA_SDL2_GIT_TAG`, `CNA_SDL2_GIT_REPOSITORY`.
- `SDL2*` packages dropped from the CNA_ENABLE_SDL=OFF disable list.
- No CMake preset referenced SDL2, and the presets are unchanged.

**What a user gets now:**
- `-DCNA_PLATFORM=SDL2` → FATAL_ERROR "CNA_PLATFORM=SDL2 is not a known platform. Available: … Reserved but unimplemented: SDL12 EMSCRIPTEN (+TERMINAL on Windows / WIN32 elsewhere)" (`cmake/PlatformSelection.cmake` L112-117). Locked by `cmake/Tests/RetiredSdl2PlatformSelection.cmake` and `UnitTests.cmake` L1384.
- `-DCNA_AUDIO_PLATFORM=SDL2` → "is not a known audio platform. Available: SDL3 NULL ALSA. Reserved: OPENAL WASAPI".
- At runtime, `PlatformFactory::Create("SDL2")` throws PlatformException, and `GetAvailable()` never lists it (`IPlatformTests.cpp` RetiredSdl2ImplementationIsNeitherAdvertisedNorCreatable).
- `docs/platform-abstraction.md` L38: "It is not a selectable implementation, and CNA provides no compatibility alias or forwarding backend."
- `plans/plan_sdl3free.md` is marked superseded.

**Rules that disappear with SDL2** and appear on many site pages:
- "platform SDL2 + audio SDL2 refuses SDL_RENDERER/SDL_GPU/FNA3D/FREEDIRECT".
- "SDL3 platform with SDL2 audio" and "SDL2+SDL3 in one process" errors.
- "the SDL2 and NULL audio selections have no mixer". At T: only NULL has no mixer; SOUND_ENABLED holds for SDL3 and ALSA.

**Keep** the site's statements about **FNA's** SDL2 backend (`deep-dives/foundations/cna-and-xna.html` L177, `deep-dives/reference/glossary.html` L150). They describe FNA, not CNA.

## 6. Presets, options, CI

**CMakePresets.json:** `git diff O T -- CMakePresets.json` is empty.
- 18 configure presets: base-ninja, dev, dev-fast-debug, unit, unit-pch, unit-unity, release-modules, release-ipo, web, devices-asan, devices-tsan, devices-ubsan, macos, ios, ios-simulator, tests, multi-renderer, cnaext.
- 17 build presets.
- Renderer cache vars:

| Preset | Renderer |
|---|---|
| dev, unit, release-modules | STUB |
| web | WEBGL2 |
| devices-* | OPENGLES3 |
| tests | OPENGLES3 |
| macos, ios, ios-simulator | SDL_RENDERER |
| multi-renderer | HEADLESS;SOFTWARE;STUB |
| cnaext | OPENGLES3 + CNA_CNAEXT=ON |

**Options diff** (every `option(CNA_*)` / `cmake_dependent_option` and every `set(CNA_* … CACHE)` in *.cmake and CMakeLists, O vs T):

| Kind | Removed | Added |
|---|---|---|
| option() | CNA_RENDERER_{DIRECT2D,FREEDIRECT,GDI,HTML_DOM,OPENGL4,PORTABLEGL,SVG_DOM}, CNA_OPENGL4_COMPILED_EFFECTS, CNA_BUILD_HTML_DOM_HOST_TESTS, CNA_BUILD_SVG_DOM_HOST_TESTS | CNA_EMSCRIPTEN_USE_WASMFS (default ON; "legacy FS is required for IDBFS persistence") |
| cache var | CNA_DIRECT2D_TEST_RUNTIME, CNA_SDL2_ROOT, CNA_SDL2_GIT_TAG, CNA_SDL2_GIT_REPOSITORY | CNA_EASYGL_ROOT, CNA_ENABLE_VOICE, CNA_GAMER_SERVICES_SERVER_ROOT (the last two are networking and outside R2) |

Other changes:
- `CNA_PLATFORM` STRINGS are `SDL3 | X11 | WAYLAND | HEADLESS | TERMINAL | WIN32`.
- `CNA_AUDIO_PLATFORM` STRINGS are `SDL3 | NULL | ALSA`.
- `CNA_CNAEXT`'s description is now "Enable standalone ASCII, CRT, colour-depth and DebugDraw graphics extensions" (CNAEXT agent).

**CI workflows** (`git diff --name-status O T -- .github/workflows`):
- Deleted (D): `gdi-windows-ci.yml`, `htmldom-ci.yml`.
- Modified (M): `32bit-arithmetic-ci.yml` (comment only), `d3d-windows-ci.yml` (matrix `[DIRECTX11, DIRECTX12]`; O had `+DIRECT2D`), `emscripten-multi-renderer-ci.yml` (WEBGL2+WEBGL1+CANVAS; O: WEBGL2+CANVAS+HTML_DOM+SVG_DOM), `platform-ci.yml` (SDL2 row removed).
- No workflow was added.
- Counts: **O 20 files / 28 jobs → T 18 files / 26 jobs** (jobs counted by parsing YAML `jobs:`).
- Jobs per file at T: 32bit 1, apple 3, c-api-abi-baseline 1, c-api-compat-matrix 1, c-api-coverage-gate 1, c-api-limitations 1, c-api-release-gate 1, content-pipeline-windows 1, d3d-windows 1, devices-tests 1, emscripten-multi-renderer 1, general-tests 1, gltf-renderer-stride 2, gltf-sanitizers 1, input 1, metal-macos 1, multi-renderer 1, platform-ci 6.
- `platform-ci` jobs: platform-contract (5 rows), win32-cross, win32-native, x11-sdl-free, x11-sdl-free-gpu (OPENGL33;VULKAN;SOFTWARE;HEADLESS + ALSA), sdl-enable-matrix (4 rows).

## 7. Per-renderer notes at T (only what pages need)

| Renderer | Evidence (commit) | Class |
|---|---|---|
| WEBGPU | WEBGPUPERF-0001..0008 (`85c3baa09`, `976f2b75d`, `196b14bd0`, `a2cbe1e31`, `2d6c006eb`; merge `0f690d7d5`): uniform/vertex arenas, binding cache, one encoder per frame. cna-street WebGPU frame 91-95 → 26-29 ms (Vulkan 36-39); RT switch ~57 → ~16 µs; `ctest -L WebGPU` 147/147 | runtime, Linux dev host, wgpu-native; one app |
| VULKAN, SDL_GPU, WEBGPU | STREETPERF-0001..0004 (`a98496b06`, `d111906f7`, `5c392fe0e`, `f18076dba`): draws bind the buffers' own storage instead of per-draw copies. Vulkan 120 → 27-28 ms CPU (8 → 36 fps); SDL_GPU had copied ~430 MB/frame; WebGPU 316-367 → 107-113 ms (before WEBGPUPERF). The 18 captures are bit-identical | runtime, cna-street, Linux |
| VULKAN | VULKAN-154 `6d1a76886` (X error handler installed in the libX11 SDL loaded); VULKAN-159 `37ff144a3` (death tests) | test infrastructure |
| DIRECTX9 | FULLSCREEN-001 `6f6100cd3` (fullscreen scaling, DX9 device recovery; also Vulkan/Canvas logical vs physical projection, Canvas letterboxing), FULLSCREEN-002 `9bbba48d8` (DX9 presentation during motion/resize, letterbox input transform; 110 assertions in 5 private-Wine probes + Mobile Eggbert) | runtime under Wine (not native Windows) |
| DIRECTX11/12 | WIN11 merge `7301f386a` (76 commits WIN11-0003..0103): native MSVC on one HP EliteBook 840 G9, Intel Iris Xe, Windows 11 Pro 22631; DX11/DX12 classic Intel parity; compiled effects pass DX11/DX12 suites on Intel (WIN11-0066); cna-street, cna-car-simulator and cna-gltf-viewer physical runs; DX12 swap-chain first-frame fix (WIN11-0091); one open high-cardinality GBV+DRED descriptor fault exception. DX-271 `d5cf85221` restored MinGW consumer builds | runtime, one physical Intel machine (platform-qualified) |
| EasyGL (OPENGLES3/OPENGL33/WEBGL*) | KF-1/1a/2/16 (`00b9c9898`, `a033a9184`): the GL context is leased on any thread and the game thread holds it for whole frames. KF-6 (`1dbc94f28`, `64b02d468`): the back buffer is an offscreen FBO resolved at Present where the profile can blit. CCS-1..3, LRS-R*, GSC-0009/0010 PBR fixes. BINDFIX-053 `7dae9216f` (WebGL 2 MRT). CBIND-139 `1dc4ce06a` (Android emulator CPU base-vertex; `CNA_EASYGL_CPU_BASE_VERTEX=1`) | source + tests; findings from consumer apps |
| METAL | METAL-282 `c40d00823`: an **open** row; DualTextureEffect samples Texture2 with the first UV set (XNA uses TEXCOORD1). Not verifiable on Linux | documented gap |
| SOFTWARE | SOFTWARE-485 `629554a95` (BlendFunction Min/Max ordinals); RRC-014/016: Software contracts moved from the GDI suite; one full implementation | source + tests |
| METAL / WEBGPU status words | `docs/renderer-registry.md`: "WEBGPU remains experimental. Metal's adapted native macOS validation remains an external gate"; README: METAL "macOS only, experimental" | doc |

Stale CNA docs at T: do **not** copy their numbers.
- `docs/migration-guide.md` L54 says "25 … over 21".
- `docs/c-api/COMPATIBILITY.md` L54 and `LIMITATIONS.md` L143 say "25".
- `docs/c-api/COVERAGE_AUDIT.md` L63 and L402 say "25/21".
- `docs/RendererNamingMigration.md` L8 and L170 say 22/18 and 25/21.
- `docs/c-api/CORE.md` and `FEATURE_MATRIX.md` say "50 public renderer identities".
- `docs/directx-legacy-renderers-analysis.md` still describes FreeDirect as shipping.
- The authoritative sources are `cmake/RendererIdentities.cmake`, `docs/renderer-registry.md` and `docs/removed-renderers.md`.

---

## 8. libcna.com impact

### 8.1 Method and totals
- **Site gate.** I ran the site's own gate read-only: `python3 -B scripts/check_retired_renderers.py`. It derives the retired set from CNA git objects at alpha.1 and at `cnahead`, which is b0e97bb1 in the working tree.
  - Result: rc=1, **2079 flagged lines in 330 files** (33 retired identities derived).
  - Split: 1471 lines in 234 authored files; 389 lines in 88 `known-issues/**` pages; 219 lines in generated files.
  - Generated: search-index.json 87, data/known-issues.json 115, img/architecture-diagram.svg 7, sitemap.xml 3, development/reference/* 7.
  - Of the older retired names, only one stray `DIRECTX1…` line matched (development/workflows.html L259, a truncated `DIRECTX11`). Effectively only the 7 newly retired names occur.
- **Gate blind spots** (spellings the gate does not flag; my own scan):
  - "OpenGL 4" with a space, meaning the renderer: 29 files.
  - "free-direct"/"free-api": 45 files.
  - "DirectDraw": 45 files (mostly FREEDIRECT descriptions).
  - CNA's SDL2: 110 pages, 587 hits outside known-issues, of which 216 are platform-selection context and 51 audio.
  - Stale counts: see 8.4.
  - The gate *does* flag every bare "GDI", so Win32-platform prose about the GDI presenter must be reworded (e.g. "gdi32 StretchDIBits"). It does not flag `gdi32`.
- **My regex totals** across all non-audit/scripts files: DIRECT2D 683, FREEDIRECT(+free-direct) 831, free-api 157, PORTABLEGL 412, GDI 678, HTML_DOM 478, SVG_DOM 378, OPENGL4 1339, SDL2 716. These include generated files.

### 8.2 Generated artefacts: count only, fix the generator or input, then regenerate

| Artefact | Hits | Generator / source of truth | Note |
|---|---|---|---|
| `known-issues/**` | 389 gate lines in 88 pages (103 pages with my broader regex incl. SDL2) | `data/known-issues.json` + `scripts/known_issues.py` | 27 issue pages are *about* removed renderers or SDL2 by title (8.9) |
| `data/known-issues.json` | 115 gate lines (175 identity + 16 SDL2 hits) | hand-curated source (development/maintenance.html says do not hand-edit known-issues/**; edit this JSON) | resolve or retire issues whose subject no longer exists |
| `search-index.json` | 87 gate lines, 16 SDL2 | `scripts/build_site_indexes.py` | regenerate after the page edits |
| `sitemap.xml` | 9 URLs of dedicated pages: browser-dom-renderers L404, windows-2d-renderers L499, freedirect-and-freeapi L599, internals/graphics/opengl4 L824, internals/platforms/sdl2 L949, tut 105 L1389, tut 107 L1394, tut 130 L1524 | `scripts/build_site_indexes.py` | regenerate after deletions |
| `img/architecture-diagram.svg` | 7 labels | `scripts/make_architecture_diagram.py` L148 (`("OPENGL4","desktop GL 4.1+ core")`), L157 (`[["SDL_RENDERER","FREEDIRECT"],["DIRECT2D","GDI"],["CANVAS","HTML_DOM"],["SVG_DOM"]]`), L163 (`("PORTABLEGL","CPU OpenGL 3.x")`) | edit the script, regenerate; architecture.html L149 caption says "25 renderer identities" |
| `development/reference/{cmake-options,modules,selection-axes,test-targets}.html` | 3/1/1/2 gate lines (long lines) | `scripts/generate_dev_reference.py` (reads TARGET git objects; L114 maps `"opengl4"` to the deleted internals page; L416 says it refuses to write if counts disagree with the canonical counts) | regenerate at T after updating facts and removing the opengl4 mapping |
| Sidebars, breadcrumbs, pagers, `p3:deep-links` / `p3:issue-links` blocks | e.g. 19 deep-dives/renderers pages each link the two deleted renderer deep dives via the generated sidebar ("Windows 2D: DIRECT2D and GDI") | `scripts/site_deep.py`/`deep_manifest.py` (siblings intro L55-56 names "FreeDirect and FreeAPI"), `scripts/dev_manifest.py` (L212 opengl4 page, L233-234 sdl2 page), `scripts/site_nav.py`, `scripts/update_tutorial_hub.py` | regenerate after deleting the pages |

### 8.3 Pages dedicated to removed renderers or SDL2, and their inbound links (non-generated referrers; known-issues links counted separately)

| Page | Status | Recommended action | Inbound links (authored pages) |
|---|---|---|---|
| `deep-dives/renderers/windows-2d-renderers.html` ("DIRECT2D and GDI: two Windows 2D delivery stacks") | 100% removed | **Delete** | docs/rendering-backends, docs/tutorials/72, docs/tutorials/103, development/internals/graphics/backends, development/internals/graphics/software, development/handbook/fix-a-renderer-bug, development/testing/architecture, development/architecture/graphics, deep-dives/renderers/browser-dom-renderers; plus the generated deep-dive sidebar on all deep-dives/renderers/* pages, development/reference/test-targets (generated), data/known-issues.json (3 issue pages) |
| `deep-dives/renderers/browser-dom-renderers.html` ("CANVAS, HTML_DOM and SVG_DOM …") | mixed; it is the only CANVAS deep dive | **Rewrite as a CANVAS-only page** (rename, e.g. `canvas-renderer.html`, and leave a redirect stub or fix links) | docs/rendering-backends, docs/tutorials/72, docs/tutorials/81, docs/tutorials/105, deep-dives/platforms/web-build-and-main-loop, development/internals/graphics/backends, development/handbook/fix-a-renderer-bug, development/testing/architecture, development/architecture/graphics, deep-dives/renderers/windows-2d-renderers; generated sidebar on all renderer deep dives; development/reference/cmake-options (generated); known-issues (4) |
| `deep-dives/siblings/freedirect-and-freeapi.html` ("free-direct and free-api beneath the FREEDIRECT renderer") | 100% about the removed renderer's dependency chain | **Delete** | deep-dives/siblings/index, deep-dives/siblings/easygl-and-metagl (sidebar + pager next), docs/rendering-backends, docs/tutorials/72, development/internals/graphics/backends, development/handbook/fix-a-renderer-bug, development/repository/source-ownership, development/testing/architecture; development/reference/cmake-options (generated); known-issues (2) |
| `development/internals/graphics/opengl4.html` ("OpenGL4 renderer internals") | 100% removed | **Delete**; drop `dev_manifest.py` L212 and `generate_dev_reference.py` L114 | deep-dives/renderers/easygl-gl-profiles, deep-dives/renderers/presentation-and-backbuffer-readback, deep-dives/siblings/easygl-and-metagl, development/handbook/fix-a-renderer-bug, development/internals/index, development/internals/modules/graphics-ext, development/internals/platforms/wayland, development/internals/platforms/x11, development/takeover/blast-radius, development/takeover/review-ai-generated-code; development/reference/{modules,selection-axes} (generated); known-issues (1) |
| `development/internals/platforms/sdl2.html` ("SDL2 platform internals") | 100% removed (SDL2) | **Delete**; drop `dev_manifest.py` L233-234 | development/internals/index, development/internals/input/events; known-issues (3) |
| `docs/tutorials/130-opengl4-desktop.html` ("Run CNA on Desktop OpenGL 4 (OPENGL4)") | 100% removed | **Delete**; remove the hub card and JSON-LD item (position 127) in tutorials.html; fix the prev/next of neighbours | tutorials.html, docs/rendering-backends, docs/tutorials/{72,102,131,132,133}, deep-dives/renderers/easygl-gl-profiles, development/internals/graphics/opengl4 (also deleted). Suggested retarget: tutorial 102 (OpenGL family / OPENGL33) |
| `docs/tutorials/105-browser-renderers.html` ("Browser-Native Renderers") | mostly HTML_DOM/SVG_DOM (49 hits) | **Rewrite** around CANVAS (+ pointers to WEBGL1/2 and WEBGPU); delete "Where SVG_DOM differs", the readback/compositor comparisons and 3-way tables | tutorials.html, docs/rendering-backends, docs/tutorials/{72,101,102,132}, deep-dives/platforms/web-build-and-main-loop, deep-dives/renderers/browser-dom-renderers, deep-dives/verification/oracles-and-engagement; known-issues (1) |
| `docs/tutorials/107-cpu-renderers.html` ("CPU-Only Renderers: Software, PortableGL, Headless and Stub") | one section removed | **Rewrite** to Software/Headless/Stub (three); delete the "PORTABLEGL" section | tutorials.html, docs/rendering-backends, docs/tutorials/{72,101,103,105,109}, deep-dives/renderers/presentation-and-backbuffer-readback, development/internals/graphics/{headless,software,stub} |

Pages with a **dedicated section** to delete. They keep their other content.
- docs/rendering-backends.html: "Desktop OpenGL 4: the OPENGL4 renderer"; "Windows renderers: … Direct2D and GDI" → retitle.
- features.html: 7 renderer subsections (OpenGL 4, FreeDirect, Direct2D, GDI, HTML DOM, SVG DOM, PortableGL).
- development/internals/graphics/backends.html: "OPENGL4 and EasyGL: separate families…"; "SDL_RENDERER, DIRECT2D, GDI and FREEDIRECT".
- deep-dives/renderers/easygl-gl-profiles.html: "OPENGL4 and PORTABLEGL are not EasyGL".
- docs/tutorials/102-opengl-family.html: "Not in this family: OPENGL4".
- deep-dives/platforms/web-build-and-main-loop.html: "HTML_DOM: automated browser and compositor evidence"; "SVG_DOM: a real browser harness without a caller".
- deep-dives/verification/oracles-and-engagement.html: "Direct2D: prefixes, a virtual display and a pinned Proton".
- deep-dives/build/tools-and-scripts.html: "A gate over command text: the Direct2D parallelism cap".
- development/testing/architecture.html: "Output gates: Vulkan and OpenGL4".
- development/internals/graphics/software.html: "Identity, build target and unusual GDI reuse".
- development/internals/graphics/easygl.html: "Stock shader corpus shared with OpenGL4".
- docs/building.html: troubleshooting "CANVAS, HTML_DOM, SVG_DOM or WEBGL1/WEBGL2 refuse to configure" and '"puts SDL2 and SDL3 in one process"'.
- index.html: cards "free-direct & free-api" and "FreeDirect game consumers".
- roadmap.html: "FreeDirect renderer — the best 2D fidelity in the project Shipped".
- docs/platforms.html: "The seven platform implementations" and "The four audio implementations at a glance" (recount).

### 8.4 Recurring stale phrases (authored pages only; `git grep -c -i -F`, line counts)

| Phrase on site | Lines / files | Replace with (T) |
|---|---:|---|
| "seven 2D-only renderers (SDL_RENDERER, DIRECT2D, CANVAS, HTML_DOM, FREEDIRECT, GDI, SVG_DOM)" (3 variants; e.g. "Before you start … Requires a 3D-capable renderer such as OPENGLES3 or VULKAN; the seven 2D-only renderers (…) throw on 3D calls by default, and STUB reports no 3D capability at all.") | 62 / 50 (+1 "7 2D-only") | "the two 2D-only renderers (SDL_RENDERER and CANVAS) throw on 3D calls by default, and STUB reports no 3D capability at all" |
| "25 renderer identities" / "25 public renderer" / "25 identit" | 80 / 52; 24 / 19; 80 / 46 | 18 |
| "21 implementation famil…" / "21 famil…" | 49 / 35; 32 / 20 | 14 |
| "14 of the 25" (compiled effects) / "14 identities" / "10 families" / "nine default-OFF" | 26 / 21; 5 / 3; 7 / 7; 4 / 4 | "13 of the 18 identities in 9 families"; "eight default-OFF options plus FNA3D always on" |
| "Seven platform implementations (SDL3, SDL2, …)" / "7 platform" | 21 / 17; 10 / 8 | six (SDL3, X11, WAYLAND, WIN32, HEADLESS, TERMINAL) |
| "four audio" / "4 audio" | 8 / 5; 10 / 8 | three (SDL3, NULL, ALSA) |
| "SDL3, SDL2, …" lists | 45 / 31 | drop SDL2 |
| "CNA_ENABLE_SDL=OFF refuses … SDL3/SDL2 platform, SDL3/SDL2 audio and the SDL_RENDERER, SDL_GPU, FNA3D and FREEDIRECT renderers" / "four SDL-based renderers" | ~15 pages; 8 / 8 | "the SDL3 platform, SDL3 audio, and the three SDL-linking renderers SDL_RENDERER, SDL_GPU and FNA3D" (`cmake/SdlAvailability.cmake` at T) |
| "platform SDL2 + audio SDL2 refuses SDL_RENDERER/SDL_GPU/FNA3D/FREEDIRECT" | docs/platforms (2), docs/audio, docs/building, tut 127, dev/build/architecture, internals/platforms/index | delete (rule gone with Sdl2OnlyConfiguration.cmake) |
| "the SDL2 and NULL audio platforms have no mixer" | tutorials 14/78, takeover/mental-model, migration-from-monogame, media-contract … | "the NULL audio platform has no mixer" |
| "Three combination rules" | 6 / 5 | one rule: platform partition (+ the separate TERMINAL renderer restriction) |
| "20 workflow files" / "28 jobs" | 25 / 20; 19 / 18 | 18 files / 26 jobs |
| "OpenGL 4" as a renderer name (not a GL version) | 29 files (state-objects 8, features 9, …) | drop; keep "OpenGL 4.6 (Core Profile)" only where it describes the context an OPENGL33 build gets |
| "desktop OpenGL 3.3 and 4" (index hero) | index.html | "desktop OpenGL 3.3" |

### 8.5 Per-page table (authored and generated pages; known-issues/**, search-index.json and sitemap.xml are counted in 8.2)
"id-lines (gate)" is the number of lines `check_retired_renderers.py` flags. "SDL2" is the number of hits for CNA's SDL2 (FNA's SDL2 is kept, see §5). "Nature" counts hits per context: table rows, prose, list items, headings, code, nav or sidebar, and the shared 2D-only boilerplate sentence. "'OpenGL 4'" and "free-direct/api" are the forms the gate misses.

#### (root pages) (10 pages)

| Page | id-lines (gate) | SDL2 | Nature | Names | Action |
|---|---:|---:|---|---|---|
| `features.html` | 50 | 17 | 2D-only boilerplate; table rows(31); section heading; prose(40); SDL2(17); 'OpenGL 4'(9); free-direct/api(6) | GDI,PORTABLEGL,HTML_DOM,DIRECT2D,OPENGL4,SVG_DOM,FREEDIRECT | Delete the subsections "OpenGL 4 Renderer", "FreeDirect (DirectDraw) Renderer", "Direct2D Renderer", "GDI Renderer", "HTML DOM Renderer", "SVG DOM Renderer" and "PortableGL Renderer". Fix the 2D-only sentence and the 25/7-platform/4-audio counts, and remove SDL2 from the platform and audio lists. |
| `architecture.html` | 26 | 22 | table rows(8); code; prose(9); SDL2(22); 'OpenGL 4'(1); free-direct/api(9) | PORTABLEGL,FREEDIRECT,OPENGL4,GDI,DIRECT2D,HTML_DOM,SVG_DOM | Change "One list of 25" to 18 and "Three combination rules" to one (platform partition). Drop free-direct from "Required sibling repositories". In the text-alternative diagram code block, drop the 7 names. Remove SDL2 from the platform and audio axes. Line 220: "EasyGL and OpenGL 4 renderers" becomes EasyGL only. |
| `about.html` | 8 | 6 | list(9); prose(1); SDL2(6); free-direct/api(1) | GDI,OPENGL4,PORTABLEGL,DIRECT2D,FREEDIRECT | Remove the free-direct sibling bullet and the removed renderer names. Remove the SDL2 platform/audio mentions. |
| `index.html` | 7 | 5 | section heading; prose(12); SDL2(5); 'OpenGL 4'(1); free-direct/api(10) | GDI,FREEDIRECT,DIRECT2D,PORTABLEGL | Hero renderer sentence: drop "and 4", Direct2D, GDI, the DirectDraw-shaped FreeDirect, SVG/DOM and PortableGL. Delete the "free-direct & free-api" ecosystem card and the "FreeDirect game consumers" card. Remove SDL2. |
| `contribute.html` | 11 | 0 | code; list(1); prose(12); free-direct/api(9) | FREEDIRECT,GDI,OPENGL4,PORTABLEGL,DIRECT2D | Remove the free-direct/free-api clone commands and tree lines, "fetched ... PortableGL", and OPENGL4/PORTABLEGL/FREEDIRECT from the "no workflow names" list. |
| `roadmap.html` | 7 | 1 | section heading; prose(6); SDL2(1); free-direct/api(1) | OPENGL4,FREEDIRECT,PORTABLEGL,GDI | Delete the milestone "FreeDirect renderer ... Shipped". Retitle "Modern-graphics campaigns: OpenGL4, SDL_GPU, WebGPU and Vulkan" without OpenGL4. |
| `tutorials.html` | 5 | 0 | prose(6); 'OpenGL 4'(3) | OPENGL4,PORTABLEGL | Tutorial hub: delete card 130 and its JSON-LD ListItem, retitle card 107 (JSON-LD ListItem as well), and check card 105. Generated in part by update_tutorial_hub.py. |
| `showcase.html` | 5 | 1 | table rows(9); prose(2); SDL2(1); 'OpenGL 4'(1) | HTML_DOM,GDI,SVG_DOM,DIRECT2D | Line 106: "20 workflow files (28 jobs) ... HTML DOM" becomes 18 files (26 jobs). Browser row: WEBGL2, CANVAS and WEBGPU (plus WEBGL1). Windows row: SDL_RENDERER and DIRECTX9/11/12. Remove SDL2. |
| `documentation.html` | 1 | 3 | prose(4); SDL2(3); 'OpenGL 4'(1) | DIRECT2D,GDI,FREEDIRECT,PORTABLEGL | "all 25 selectable renderers ... OpenGL 4 ..." becomes 18 without the removed names. Remove SDL2. |
| `demos.html` | 1 | 0 | prose(2) | HTML_DOM,SVG_DOM | Browser renderer sentence: drop HTML_DOM/SVG_DOM. |

#### docs (25 pages)

| Page | id-lines (gate) | SDL2 | Nature | Names | Action |
|---|---:|---:|---|---|---|
| `docs/rendering-backends.html` | 91 | 9 | table rows(82); section heading; list(30); prose(55); nav/sidebar; SDL2(9); 'OpenGL 4'(3); free-direct/api(16) | OPENGL4,PORTABLEGL,FREEDIRECT,GDI,HTML_DOM,DIRECT2D,SVG_DOM | MAJOR REWRITE (main renderer guide). "The 25 renderers at a glance": 18 rows. Delete "Desktop OpenGL 4: the OPENGL4 renderer". Retitle "Windows renderers: Direct3D 9/11/12, Direct2D and GDI" to "Direct3D 9/11/12". "2D-only renderers": SDL_RENDERER and CANVAS. "Browser renderers": CANVAS + WEBGL1/2 (+WEBGPU). "CPU and no-GPU": drop PORTABLEGL. "Combination rules": 3 to 1. "Sibling repositories": drop free-direct/free-api and the PortableGL fetch. "Compiled XNA effects": 13 identities/9 families. "Modern features by renderer": drop OPENGL4, add DX11/DX12 compute and indirect draws. Fix the capability-matrix rows. |
| `docs/platforms.html` | 23 | 51 | table rows(24); list(6); prose(11); SDL2(51) | GDI,HTML_DOM,DIRECT2D,FREEDIRECT,PORTABLEGL,SVG_DOM,OPENGL4 | Change "The seven platform implementations" to six and "The four audio implementations" to three. Remove the SDL2 rows and code (51). Renderer-availability-by-OS table: drop the DIRECT2D/GDI, HTML_DOM/SVG_DOM, FREEDIRECT/PORTABLEGL/OPENGL4 entries. |
| `docs/building.html` | 18 | 18 | table rows(3); section heading; code; prose(17); SDL2(18); free-direct/api(3) | OPENGL4,FREEDIRECT,PORTABLEGL,HTML_DOM,GDI,DIRECT2D,SVG_DOM | Step 2: drop the free-direct/free-api clones. Troubleshooting: "CANVAS, HTML_DOM, SVG_DOM or WEBGL1/WEBGL2 refuse to configure" becomes "CANVAS or WEBGL1/WEBGL2". Delete the "puts SDL2 and SDL3 in one process" entry. Compiled-effects options: drop CNA_OPENGL4_COMPILED_EFFECTS. Remove SDL2 option rows. |
| `docs/audio.html` | 1 | 27 | prose(1); SDL2(27) | FREEDIRECT | Remove the SDL2 audio implementation (27 mentions). Audio is SDL3/NULL/ALSA. |
| `docs/verification.html` | 19 | 1 | table rows(14); list(24); prose(4); SDL2(1) | OPENGL4,GDI,DIRECT2D,HTML_DOM,FREEDIRECT,SVG_DOM,PORTABLEGL | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality; remove the CNA SDL2 platform/audio mentions |
| `docs/faq.html` | 11 | 6 | list(11); prose(14); SDL2(6); free-direct/api(2) | GDI,SVG_DOM,DIRECT2D,HTML_DOM,FREEDIRECT,PORTABLEGL,OPENGL4 | rewrite the sentence(s) to the 18-renderer reality; remove the CNA SDL2 platform/audio mentions |
| `docs/3d-rendering.html` | 16 | 0 | 2D-only boilerplate; table rows(14); list(1); prose(21) | OPENGL4,GDI,PORTABLEGL,DIRECT2D,HTML_DOM,FREEDIRECT,SVG_DOM | replace the "seven 2D-only renderers (...)" sentence with "the two 2D-only renderers, SDL_RENDERER and CANVAS"; delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality |
| `docs/native-platforms.html` | 9 | 6 | table rows(7); list(1); prose(4); SDL2(6) | FREEDIRECT,OPENGL4,PORTABLEGL,GDI,DIRECT2D,HTML_DOM,SVG_DOM | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality; remove the CNA SDL2 platform/audio mentions |
| `docs/effects.html` | 14 | 0 | 2D-only boilerplate; table rows(14); list(3); prose(3) | OPENGL4,PORTABLEGL,GDI,DIRECT2D,HTML_DOM,SVG_DOM,FREEDIRECT | replace the "seven 2D-only renderers (...)" sentence with "the two 2D-only renderers, SDL_RENDERER and CANVAS"; delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality |
| `docs/roadmap.html` | 8 | 2 | table rows(11); list(1); SDL2(2); 'OpenGL 4'(2); free-direct/api(1) | OPENGL4,FREEDIRECT,DIRECT2D,GDI,HTML_DOM,SVG_DOM,PORTABLEGL | Remove the removed-renderer rows from the roadmap tables. Line 286 "OpenGL 4 renderers" automatic-coverage gap: drop it. |
| `docs/render-targets.html` | 11 | 0 | table rows(7); prose(23) | OPENGL4,PORTABLEGL,GDI,DIRECT2D,HTML_DOM,SVG_DOM,FREEDIRECT | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality |
| `docs/shader-effects.html` | 9 | 0 | table rows(10); prose(5) | OPENGL4,GDI,HTML_DOM,SVG_DOM,PORTABLEGL,DIRECT2D,FREEDIRECT | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality |
| `docs/cnaext-engine.html` | 7 | 0 | 2D-only boilerplate; table rows(8); list(2) | OPENGL4,GDI,PORTABLEGL,DIRECT2D,HTML_DOM,SVG_DOM,FREEDIRECT | replace the "seven 2D-only renderers (...)" sentence with "the two 2D-only renderers, SDL_RENDERER and CANVAS"; delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality |
| `docs/runtime-renderer-selection.html` | 6 | 0 | list(6); prose(8) | GDI,HTML_DOM,SVG_DOM,PORTABLEGL,OPENGL4,FREEDIRECT | rewrite the sentence(s) to the 18-renderer reality |
| `docs/graphics-state.html` | 4 | 0 | list(2); prose(9) | OPENGL4,PORTABLEGL,GDI | rewrite the sentence(s) to the 18-renderer reality |
| `docs/xna-compatibility.html` | 3 | 1 | table rows(2); list(3); SDL2(1) | OPENGL4,PORTABLEGL | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality; remove the CNA SDL2 platform/audio mentions |
| `docs/input.html` | 2 | 1 | list(5); SDL2(1) | FREEDIRECT,OPENGL4,SVG_DOM,HTML_DOM,GDI | rewrite the sentence(s) to the 18-renderer reality; remove the CNA SDL2 platform/audio mentions |
| `docs/spritebatch.html` | 3 | 0 | 2D-only boilerplate; table rows(1); prose(1) | FREEDIRECT,SVG_DOM,DIRECT2D,HTML_DOM,GDI,PORTABLEGL,OPENGL4 | replace the "seven 2D-only renderers (...)" sentence with "the two 2D-only renderers, SDL_RENDERER and CANVAS"; delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality |
| `docs/getting-started.html` | 2 | 0 | list(2); prose(1) | DIRECT2D,GDI,OPENGL4 | rewrite the sentence(s) to the 18-renderer reality |
| `docs/releases.html` | 0 | 2 | SDL2(2); free-direct/api(1) |  | remove the CNA SDL2 platform/audio mentions; free-direct/free-api: drop it as a CNA dependency |
| `docs/vs-alternatives.html` | 1 | 1 | table rows(1); SDL2(1) | GDI | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; remove the CNA SDL2 platform/audio mentions |
| `docs/content-pipeline.html` | 1 | 0 | list(1) | GDI | rewrite the sentence(s) to the 18-renderer reality |
| `docs/math-types.html` | 1 | 0 | prose(1) | OPENGL4 | rewrite the sentence(s) to the 18-renderer reality |
| `docs/migration-from-monogame.html` | 0 | 1 | SDL2(1); free-direct/api(1) |  | remove the CNA SDL2 platform/audio mentions; free-direct/free-api: drop it as a CNA dependency |
| `docs/packed-vector.html` | 1 | 0 | prose(1) | OPENGL4 | rewrite the sentence(s) to the 18-renderer reality |

#### docs/tutorials (91 pages)

| Page | id-lines (gate) | SDL2 | Nature | Names | Action |
|---|---:|---:|---|---|---|
| `docs/tutorials/130-opengl4-desktop.html` | 46 | 5 | table rows(8); section heading; code; list(10); prose(33); SDL2(5); 'OpenGL 4'(5); free-direct/api(1) | OPENGL4,PORTABLEGL | DEDICATED. Delete the tutorial. Remove its tutorials.html hub card (update_tutorial_hub.py) and the prev/next links in 129/131. Retarget inbound links (102, 131, 132, 133, 72, rendering-backends, easygl-gl-profiles) to 102-opengl-family (OPENGL33). |
| `docs/tutorials/72-backend-selection.html` | 28 | 3 | table rows(19); list(11); prose(35); SDL2(3); 'OpenGL 4'(1); free-direct/api(8) | FREEDIRECT,OPENGL4,GDI,DIRECT2D,HTML_DOM,SVG_DOM,PORTABLEGL | Recount the groups: G1 GL family 6 to 5; G4 Windows 5 to 3 (DX9/11/12); G5 browser 3 to 1 (CANVAS, plus the WebGL profiles and WebGPU); G6 portable 2D 2 to 1 (SDL_RENDERER); G7 CPU/no-output 4 to 3. Fix the "refuse 3D", "custom shaders" and decision tables. |
| `docs/tutorials/105-browser-renderers.html` | 29 | 0 | table rows(14); section heading; code; list(4); prose(19) | HTML_DOM,SVG_DOM | DEDICATED in part. Rewrite as a CANVAS tutorial that points to WEBGL1/WEBGL2/WEBGPU for GPU paths. Delete "Where SVG_DOM differs", the DOM readback and compositor material, and the 3-way comparison tables and code. |
| `docs/tutorials/107-cpu-renderers.html` | 27 | 1 | table rows(6); section heading; code; list(3); prose(19); SDL2(1) | PORTABLEGL,GDI,OPENGL4 | Retitle "CPU-Only Renderers: Software, Headless and Stub". Delete the "PORTABLEGL: a real GL pipeline on the CPU" section. Change "four" to "three" in "at a glance" and "Choosing between the four". |
| `docs/tutorials/127-platform-audio-selection.html` | 5 | 22 | table rows(3); prose(2); SDL2(22) | FREEDIRECT,PORTABLEGL | Remove the SDL2 platform/audio rows and examples (22). Renderer table: drop FREEDIRECT/PORTABLEGL. |
| `docs/tutorials/80-cross-platform.html` | 7 | 8 | table rows(9); list(1); prose(4); SDL2(8); free-direct/api(2) | HTML_DOM,SVG_DOM,DIRECT2D,GDI,FREEDIRECT,PORTABLEGL | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality; remove the CNA SDL2 platform/audio mentions |
| `docs/tutorials/62-mrt.html` | 11 | 0 | 2D-only boilerplate; table rows(7); code; prose(6) | OPENGL4,PORTABLEGL,DIRECT2D,HTML_DOM,FREEDIRECT,GDI,SVG_DOM | replace the "seven 2D-only renderers (...)" sentence with "the two 2D-only renderers, SDL_RENDERER and CANVAS"; delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; fix the code/config example; rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/131-sdl-gpu.html` | 5 | 3 | list(4); nav/sidebar; SDL2(3); 'OpenGL 4'(2) | OPENGL4,FREEDIRECT | regenerate the sidebar; rewrite the sentence(s) to the 18-renderer reality; remove the CNA SDL2 platform/audio mentions |
| `docs/tutorials/151-one-shader-several-renderers.html` | 10 | 0 | table rows(11); code; prose(3) | OPENGL4,GDI,HTML_DOM,SVG_DOM,PORTABLEGL,DIRECT2D,FREEDIRECT | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; fix the code/config example; rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/102-opengl-family.html` | 8 | 1 | table rows(2); section heading; list(5); prose(6); SDL2(1) | OPENGL4,PORTABLEGL | Delete the section "Not in this family: OPENGL4". |
| `docs/tutorials/52-custom-shaders.html` | 9 | 0 | 2D-only boilerplate; table rows(1); list(12); prose(3) | OPENGL4,HTML_DOM,GDI,SVG_DOM,DIRECT2D,FREEDIRECT,PORTABLEGL | replace the "seven 2D-only renderers (...)" sentence with "the two 2D-only renderers, SDL_RENDERER and CANVAS"; delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/138-sdl-free-build.html` | 4 | 4 | table rows(9); SDL2(4) | GDI,PORTABLEGL,DIRECT2D,FREEDIRECT,OPENGL4 | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; remove the CNA SDL2 platform/audio mentions |
| `docs/tutorials/152-graphics-profiles.html` | 8 | 0 | table rows(7); code; prose(7) | OPENGL4,PORTABLEGL,GDI,DIRECT2D,FREEDIRECT,HTML_DOM,SVG_DOM | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; fix the code/config example; rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/60-instancing.html` | 8 | 0 | 2D-only boilerplate; table rows(7); code; prose(2) | OPENGL4,DIRECT2D,HTML_DOM,FREEDIRECT,GDI,SVG_DOM,PORTABLEGL | replace the "seven 2D-only renderers (...)" sentence with "the two 2D-only renderers, SDL_RENDERER and CANVAS"; delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; fix the code/config example; rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/65-msaa.html` | 7 | 1 | table rows(7); list(1); prose(2); SDL2(1) | PORTABLEGL,OPENGL4,GDI,DIRECT2D,HTML_DOM,FREEDIRECT,SVG_DOM | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality; remove the CNA SDL2 platform/audio mentions |
| `docs/tutorials/59-shadow-mapping.html` | 7 | 0 | 2D-only boilerplate; table rows(7); prose(3) | OPENGL4,DIRECT2D,HTML_DOM,FREEDIRECT,GDI,SVG_DOM,PORTABLEGL | replace the "seven 2D-only renderers (...)" sentence with "the two 2D-only renderers, SDL_RENDERER and CANVAS"; delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/61-occlusion-query.html` | 7 | 0 | 2D-only boilerplate; table rows(7); code; prose(1) | PORTABLEGL,DIRECT2D,HTML_DOM,FREEDIRECT,GDI,SVG_DOM,OPENGL4 | replace the "seven 2D-only renderers (...)" sentence with "the two 2D-only renderers, SDL_RENDERER and CANVAS"; delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; fix the code/config example; rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/67-deferred-rendering.html` | 7 | 0 | 2D-only boilerplate; table rows(7); prose(2) | OPENGL4,DIRECT2D,HTML_DOM,FREEDIRECT,GDI,SVG_DOM,PORTABLEGL | replace the "seven 2D-only renderers (...)" sentence with "the two 2D-only renderers, SDL_RENDERER and CANVAS"; delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/02-setup.html` | 4 | 2 | table rows(2); prose(3); SDL2(2); free-direct/api(2) | GDI,FREEDIRECT,DIRECT2D,OPENGL4 | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality; remove the CNA SDL2 platform/audio mentions |
| `docs/tutorials/103-direct3d-windows.html` | 6 | 0 | table rows(4); list(4); prose(12) | DIRECT2D,GDI,FREEDIRECT | Rewrite the Direct2D/GDI comparisons. Windows 2D now means SDL_RENDERER (default), SOFTWARE over the Win32 surface presenter, or DX9/11/12. |
| `docs/tutorials/63-stencil-buffer.html` | 6 | 0 | 2D-only boilerplate; table rows(7); prose(2) | DIRECT2D,HTML_DOM,FREEDIRECT,GDI,SVG_DOM,OPENGL4,PORTABLEGL | replace the "seven 2D-only renderers (...)" sentence with "the two 2D-only renderers, SDL_RENDERER and CANVAS"; delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/64-cubemaps.html` | 6 | 0 | 2D-only boilerplate; table rows(7); prose(2) | DIRECT2D,HTML_DOM,FREEDIRECT,GDI,SVG_DOM,OPENGL4,PORTABLEGL | replace the "seven 2D-only renderers (...)" sentence with "the two 2D-only renderers, SDL_RENDERER and CANVAS"; delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/66-bloom.html` | 6 | 0 | 2D-only boilerplate; table rows(7); prose(3) | PORTABLEGL,OPENGL4,DIRECT2D,HTML_DOM,FREEDIRECT,GDI,SVG_DOM | replace the "seven 2D-only renderers (...)" sentence with "the two 2D-only renderers, SDL_RENDERER and CANVAS"; delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/87-custom-backend.html` | 6 | 0 | table rows(1); prose(9) | OPENGL4,GDI,DIRECT2D,PORTABLEGL,HTML_DOM,SVG_DOM | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/100-shipping.html` | 3 | 2 | code; prose(2); SDL2(2) | OPENGL4,HTML_DOM,SVG_DOM,GDI | fix the code/config example; rewrite the sentence(s) to the 18-renderer reality; remove the CNA SDL2 platform/audio mentions |
| `docs/tutorials/101-renderer-capabilities.html` | 5 | 0 | table rows(6); prose(5) | GDI,DIRECT2D,FREEDIRECT,HTML_DOM,SVG_DOM | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/108-fna3d.html` | 3 | 2 | prose(3); SDL2(2) | OPENGL4,FREEDIRECT | rewrite the sentence(s) to the 18-renderer reality; remove the CNA SDL2 platform/audio mentions |
| `docs/tutorials/116-post-process-effects.html` | 5 | 0 | 2D-only boilerplate; table rows(1); prose(3) | OPENGL4,PORTABLEGL,GDI | replace the "seven 2D-only renderers (...)" sentence with "the two 2D-only renderers, SDL_RENDERER and CANVAS"; delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/135-native-x11-build.html` | 4 | 1 | table rows(3); prose(1); SDL2(1) | FREEDIRECT,PORTABLEGL,OPENGL4 | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality; remove the CNA SDL2 platform/audio mentions |
| `docs/tutorials/137-alsa-audio.html` | 1 | 4 | table rows(1); SDL2(4) | FREEDIRECT | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; remove the CNA SDL2 platform/audio mentions |
| `docs/tutorials/01-introduction.html` | 4 | 0 | table rows(4); prose(3); free-direct/api(1) | OPENGL4,FREEDIRECT,DIRECT2D,GDI | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/132-webgpu.html` | 3 | 0 | list(2); prose(3); 'OpenGL 4'(1) | OPENGL4,HTML_DOM,SVG_DOM | rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/160-run-parity-fixtures-and-bounded-tests.html` | 4 | 0 | table rows(3); list(2); prose(1) | OPENGL4 | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/53-effect-parameter.html` | 4 | 0 | 2D-only boilerplate; prose(7) | OPENGL4,HTML_DOM,GDI,SVG_DOM,DIRECT2D,FREEDIRECT,PORTABLEGL | replace the "seven 2D-only renderers (...)" sentence with "the two 2D-only renderers, SDL_RENDERER and CANVAS"; rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/58-normal-mapping.html` | 4 | 0 | 2D-only boilerplate; code; prose(3) | OPENGL4,DIRECT2D,HTML_DOM,FREEDIRECT,GDI,SVG_DOM,PORTABLEGL | replace the "seven 2D-only renderers (...)" sentence with "the two 2D-only renderers, SDL_RENDERER and CANVAS"; fix the code/config example; rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/69-water.html` | 4 | 0 | 2D-only boilerplate; table rows(7) | DIRECT2D,HTML_DOM,FREEDIRECT,GDI,SVG_DOM,OPENGL4,PORTABLEGL | replace the "seven 2D-only renderers (...)" sentence with "the two 2D-only renderers, SDL_RENDERER and CANVAS"; delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows |
| `docs/tutorials/79-debugging.html` | 4 | 0 | prose(6) | PORTABLEGL,OPENGL4,GDI,HTML_DOM,SVG_DOM | rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/81-emscripten.html` | 4 | 0 | list(2); prose(5) | HTML_DOM,SVG_DOM | rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/88-device-layer.html` | 0 | 4 | SDL2(4) |  | remove the CNA SDL2 platform/audio mentions |
| `docs/tutorials/114-pbr-materials.html` | 3 | 0 | table rows(3); list(2) | OPENGL4,PORTABLEGL | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/117-devices-layer.html` | 0 | 3 | SDL2(3) |  | remove the CNA SDL2 platform/audio mentions |
| `docs/tutorials/124-web-gotchas.html` | 3 | 0 | table rows(2); list(3) | HTML_DOM,SVG_DOM | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/126-multi-renderer-build.html` | 3 | 0 | table rows(2); prose(11) | GDI,HTML_DOM,SVG_DOM,PORTABLEGL,OPENGL4,DIRECT2D | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/128-compiled-xna-effects.html` | 3 | 0 | table rows(8) | GDI,OPENGL4,PORTABLEGL,DIRECT2D,HTML_DOM,SVG_DOM,FREEDIRECT | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows |
| `docs/tutorials/133-renderer-capability-profile.html` | 2 | 0 | list(1); prose(1); 'OpenGL 4'(1) | OPENGL4 | rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/139-terminal-platform.html` | 3 | 0 | table rows(1); code; prose(1) | PORTABLEGL | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; fix the code/config example; rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/37-multiple-lights.html` | 3 | 0 | 2D-only boilerplate; prose(2) | OPENGL4,DIRECT2D,HTML_DOM,FREEDIRECT,GDI,SVG_DOM | replace the "seven 2D-only renderers (...)" sentence with "the two 2D-only renderers, SDL_RENDERER and CANVAS"; rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/51-custom-vertex.html` | 3 | 0 | 2D-only boilerplate; prose(2) | OPENGL4,DIRECT2D,HTML_DOM,FREEDIRECT,GDI,SVG_DOM | replace the "seven 2D-only renderers (...)" sentence with "the two 2D-only renderers, SDL_RENDERER and CANVAS"; rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/57-skinned-effect.html` | 3 | 0 | 2D-only boilerplate; prose(1) | OPENGL4,DIRECT2D,HTML_DOM,FREEDIRECT,GDI,SVG_DOM,PORTABLEGL | replace the "seven 2D-only renderers (...)" sentence with "the two 2D-only renderers, SDL_RENDERER and CANVAS"; rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/68-terrain.html` | 3 | 0 | 2D-only boilerplate; list(1); prose(2) | OPENGL4,DIRECT2D,HTML_DOM,FREEDIRECT,GDI,SVG_DOM,PORTABLEGL | replace the "seven 2D-only renderers (...)" sentence with "the two 2D-only renderers, SDL_RENDERER and CANVAS"; rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/75-lod.html` | 3 | 0 | 2D-only boilerplate; list(1) | DIRECT2D,HTML_DOM,FREEDIRECT,GDI,SVG_DOM,PORTABLEGL,OPENGL4 | replace the "seven 2D-only renderers (...)" sentence with "the two 2D-only renderers, SDL_RENDERER and CANVAS"; rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/125-pixel-testing.html` | 2 | 0 | prose(2) | PORTABLEGL | rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/153-image-based-lighting.html` | 2 | 0 | table rows(2) | OPENGL4,PORTABLEGL | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows |
| `docs/tutorials/154-cascaded-shadows.html` | 2 | 0 | 2D-only boilerplate; list(1) | OPENGL4,PORTABLEGL | replace the "seven 2D-only renderers (...)" sentence with "the two 2D-only renderers, SDL_RENDERER and CANVAS"; rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/20-build-run.html` | 2 | 0 | prose(6) | DIRECT2D,GDI,HTML_DOM,SVG_DOM | rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/24-post-processing.html` | 2 | 0 | prose(3) | OPENGL4,PORTABLEGL | rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/34-camera-3d.html` | 1 | 1 | 2D-only boilerplate; SDL2(1) | DIRECT2D,HTML_DOM,FREEDIRECT,GDI,SVG_DOM | replace the "seven 2D-only renderers (...)" sentence with "the two 2D-only renderers, SDL_RENDERER and CANVAS"; remove the CNA SDL2 platform/audio mentions |
| `docs/tutorials/38-vertex-buffers.html` | 2 | 0 | 2D-only boilerplate; prose(1) | GDI,DIRECT2D,HTML_DOM,FREEDIRECT,SVG_DOM | replace the "seven 2D-only renderers (...)" sentence with "the two 2D-only renderers, SDL_RENDERER and CANVAS"; rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/55-dual-texture.html` | 2 | 0 | 2D-only boilerplate; prose(1) | DIRECT2D,HTML_DOM,FREEDIRECT,GDI,SVG_DOM,PORTABLEGL,OPENGL4 | replace the "seven 2D-only renderers (...)" sentence with "the two 2D-only renderers, SDL_RENDERER and CANVAS"; rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/70-procedural-geometry.html` | 2 | 0 | 2D-only boilerplate; prose(3) | GDI,DIRECT2D,HTML_DOM,FREEDIRECT,SVG_DOM,OPENGL4,PORTABLEGL | replace the "seven 2D-only renderers (...)" sentence with "the two 2D-only renderers, SDL_RENDERER and CANVAS"; rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/83-migrate-monogame.html` | 1 | 1 | prose(1); SDL2(1) | OPENGL4 | rewrite the sentence(s) to the 18-renderer reality; remove the CNA SDL2 platform/audio mentions |
| `docs/tutorials/84-migrate-xna.html` | 2 | 0 | prose(2) | OPENGL4 | rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/85-vulkan-backend.html` | 1 | 1 | prose(1); SDL2(1) | OPENGL4 | rewrite the sentence(s) to the 18-renderer reality; remove the CNA SDL2 platform/audio mentions |
| `docs/tutorials/96-physics.html` | 2 | 0 | 2D-only boilerplate; prose(2) | DIRECT2D,HTML_DOM,SVG_DOM,FREEDIRECT,GDI | replace the "seven 2D-only renderers (...)" sentence with "the two 2D-only renderers, SDL_RENDERER and CANVAS"; rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/109-metal-macos.html` | 1 | 0 | prose(4) | OPENGL4,PORTABLEGL,FREEDIRECT,GDI | rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/115-cnaext-overview.html` | 1 | 0 | prose(1) | OPENGL4 | rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/118-dynamic-audio.html` | 0 | 1 | SDL2(1) |  | remove the CNA SDL2 platform/audio mentions |
| `docs/tutorials/119-3d-audio.html` | 0 | 1 | SDL2(1) |  | remove the CNA SDL2 platform/audio mentions |
| `docs/tutorials/120-xact.html` | 0 | 1 | SDL2(1) |  | remove the CNA SDL2 platform/audio mentions |
| `docs/tutorials/122-media-library.html` | 0 | 1 | SDL2(1) |  | remove the CNA SDL2 platform/audio mentions |
| `docs/tutorials/136-native-wayland-build.html` | 1 | 0 | table rows(1) | PORTABLEGL | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows |
| `docs/tutorials/14-sound-effects.html` | 0 | 1 | SDL2(1) |  | remove the CNA SDL2 platform/audio mentions |
| `docs/tutorials/145-content-pipeline-build.html` | 1 | 0 | 2D-only boilerplate | DIRECT2D,HTML_DOM,SVG_DOM,FREEDIRECT,GDI | replace the "seven 2D-only renderers (...)" sentence with "the two 2D-only renderers, SDL_RENDERER and CANVAS" |
| `docs/tutorials/15-background-music.html` | 0 | 1 | SDL2(1) |  | remove the CNA SDL2 platform/audio mentions |
| `docs/tutorials/23-render-targets.html` | 1 | 0 | prose(1) | PORTABLEGL | rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/25-sprite-sort-mode.html` | 1 | 0 | prose(1) | OPENGL4 | rewrite the sentence(s) to the 18-renderer reality |
| `docs/tutorials/30-gamepad.html` | 0 | 1 | SDL2(1) |  | remove the CNA SDL2 platform/audio mentions |
| `docs/tutorials/31-first-3d-triangle.html` | 1 | 0 | 2D-only boilerplate | DIRECT2D,HTML_DOM,FREEDIRECT,GDI,SVG_DOM | replace the "seven 2D-only renderers (...)" sentence with "the two 2D-only renderers, SDL_RENDERER and CANVAS" |
| `docs/tutorials/32-basiceffect.html` | 1 | 0 | 2D-only boilerplate | DIRECT2D,HTML_DOM,FREEDIRECT,GDI,SVG_DOM | replace the "seven 2D-only renderers (...)" sentence with "the two 2D-only renderers, SDL_RENDERER and CANVAS" |
| `docs/tutorials/33-matrices.html` | 1 | 0 | 2D-only boilerplate | DIRECT2D,HTML_DOM,FREEDIRECT,GDI,SVG_DOM | replace the "seven 2D-only renderers (...)" sentence with "the two 2D-only renderers, SDL_RENDERER and CANVAS" |
| `docs/tutorials/35-model-loading.html` | 1 | 0 | 2D-only boilerplate | DIRECT2D,HTML_DOM,SVG_DOM,FREEDIRECT,GDI | replace the "seven 2D-only renderers (...)" sentence with "the two 2D-only renderers, SDL_RENDERER and CANVAS" |
| `docs/tutorials/36-model-texturing.html` | 1 | 0 | 2D-only boilerplate | DIRECT2D,HTML_DOM,SVG_DOM,FREEDIRECT,GDI | replace the "seven 2D-only renderers (...)" sentence with "the two 2D-only renderers, SDL_RENDERER and CANVAS" |
| `docs/tutorials/39-depth-buffer.html` | 1 | 0 | 2D-only boilerplate | DIRECT2D,HTML_DOM,FREEDIRECT,GDI,SVG_DOM | replace the "seven 2D-only renderers (...)" sentence with "the two 2D-only renderers, SDL_RENDERER and CANVAS" |
| `docs/tutorials/40-primitive-types.html` | 1 | 0 | 2D-only boilerplate | DIRECT2D,HTML_DOM,FREEDIRECT,GDI,SVG_DOM | replace the "seven 2D-only renderers (...)" sentence with "the two 2D-only renderers, SDL_RENDERER and CANVAS" |
| `docs/tutorials/49-touch-input.html` | 0 | 1 | SDL2(1) |  | remove the CNA SDL2 platform/audio mentions |
| `docs/tutorials/50-accelerometer.html` | 0 | 1 | SDL2(1) |  | remove the CNA SDL2 platform/audio mentions |
| `docs/tutorials/54-alpha-test.html` | 1 | 0 | 2D-only boilerplate | DIRECT2D,HTML_DOM,FREEDIRECT,GDI,SVG_DOM,PORTABLEGL | replace the "seven 2D-only renderers (...)" sentence with "the two 2D-only renderers, SDL_RENDERER and CANVAS" |
| `docs/tutorials/56-environment-map.html` | 1 | 0 | 2D-only boilerplate | DIRECT2D,HTML_DOM,FREEDIRECT,GDI,SVG_DOM,PORTABLEGL | replace the "seven 2D-only renderers (...)" sentence with "the two 2D-only renderers, SDL_RENDERER and CANVAS" |
| `docs/tutorials/74-frustum-culling.html` | 1 | 0 | 2D-only boilerplate | DIRECT2D,HTML_DOM,FREEDIRECT,GDI,SVG_DOM | replace the "seven 2D-only renderers (...)" sentence with "the two 2D-only renderers, SDL_RENDERER and CANVAS" |
| `docs/tutorials/78-multithreading.html` | 0 | 1 | SDL2(1) |  | remove the CNA SDL2 platform/audio mentions |
| `docs/tutorials/93-fps-game.html` | 1 | 0 | 2D-only boilerplate | DIRECT2D,HTML_DOM,FREEDIRECT,GDI,SVG_DOM,PORTABLEGL | replace the "seven 2D-only renderers (...)" sentence with "the two 2D-only renderers, SDL_RENDERER and CANVAS" |

#### deep-dives/renderers (20 pages)

| Page | id-lines (gate) | SDL2 | Nature | Names | Action |
|---|---:|---:|---|---|---|
| `deep-dives/renderers/windows-2d-renderers.html` | 46 | 0 | table rows(5); section heading; prose(91); nav/sidebar | GDI,DIRECT2D,FREEDIRECT | DEDICATED (DIRECT2D+GDI). Delete page. No Windows 2D-only renderer survives. Remove its sidebar entry (generated deep-dive nav on ~19 renderer pages) and the inbound prose links listed in section 8.3. |
| `deep-dives/renderers/browser-dom-renderers.html` | 28 | 0 | table rows(11); section heading; list(4); prose(28); nav/sidebar | HTML_DOM,SVG_DOM,DIRECT2D,GDI | DEDICATED in part (CANVAS+HTML_DOM+SVG_DOM). It is the only CANVAS deep dive, so rewrite it as a CANVAS-only page (rename, e.g. canvas-renderer.html). Delete the HTML_DOM and SVG_DOM sections and the three-model comparison. Fix inbound links. |
| `deep-dives/renderers/easygl-gl-profiles.html` | 18 | 0 | table rows(4); section heading; prose(30); nav/sidebar; 'OpenGL 4'(1) | OPENGL4,PORTABLEGL,DIRECT2D,GDI | Delete the section "OPENGL4 and PORTABLEGL are not EasyGL". State that there is deliberately no EasyGL OpenGL 4 profile. |
| `deep-dives/renderers/presentation-and-backbuffer-readback.html` | 14 | 0 | table rows(22); list(3); prose(12); nav/sidebar; free-direct/api(1) | OPENGL4,DIRECT2D,GDI,PORTABLEGL,HTML_DOM,SVG_DOM,FREEDIRECT | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; regenerate the sidebar; rewrite the sentence(s) to the 18-renderer reality |
| `deep-dives/renderers/renderer-contract.html` | 12 | 0 | table rows(2); prose(20); nav/sidebar | OPENGL4,GDI,DIRECT2D,PORTABLEGL,FREEDIRECT | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; regenerate the sidebar; rewrite the sentence(s) to the 18-renderer reality |
| `deep-dives/renderers/render-targets-clears-and-viewports.html` | 7 | 0 | table rows(11); prose(3); nav/sidebar | GDI,DIRECT2D,PORTABLEGL,OPENGL4,FREEDIRECT,HTML_DOM,SVG_DOM | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; regenerate the sidebar; rewrite the sentence(s) to the 18-renderer reality |
| `deep-dives/renderers/index.html` | 4 | 0 | list(8); nav/sidebar | DIRECT2D,GDI,OPENGL4,PORTABLEGL,HTML_DOM,SVG_DOM | regenerate the sidebar; rewrite the sentence(s) to the 18-renderer reality |
| `deep-dives/renderers/sdl-renderer-2d-contract.html` | 3 | 1 | prose(5); nav/sidebar; SDL2(1) | DIRECT2D,GDI,FREEDIRECT,HTML_DOM,SVG_DOM | Comparisons with DIRECT2D/GDI/FREEDIRECT/DOM: rewrite against CANVAS only. Fix the sidebar. |
| `deep-dives/renderers/easygl-state-and-resource-semantics.html` | 3 | 0 | prose(2); nav/sidebar | OPENGL4,DIRECT2D,GDI | regenerate the sidebar; rewrite the sentence(s) to the 18-renderer reality |
| `deep-dives/renderers/direct3d-evidence-and-wine.html` | 2 | 0 | prose(1); nav/sidebar | DIRECT2D,GDI | regenerate the sidebar; rewrite the sentence(s) to the 18-renderer reality |
| `deep-dives/renderers/direct3d-shadereffect-contract.html` | 2 | 0 | nav/sidebar | DIRECT2D,GDI | nav only: regenerate the sidebar after the page deletions |
| `deep-dives/renderers/native-gpu-evidence-tiers.html` | 2 | 0 | prose(1); nav/sidebar | DIRECT2D,GDI,OPENGL4 | regenerate the sidebar; rewrite the sentence(s) to the 18-renderer reality |
| `deep-dives/renderers/vulkan-deferred-state-and-descriptors.html` | 2 | 0 | prose(1); nav/sidebar | DIRECT2D,GDI,OPENGL4 | regenerate the sidebar; rewrite the sentence(s) to the 18-renderer reality |
| `deep-dives/renderers/direct3d-presentation-and-state.html` | 1 | 0 | nav/sidebar | DIRECT2D,GDI | nav only: regenerate the sidebar after the page deletions |
| `deep-dives/renderers/direct3d11-and-12-resources.html` | 1 | 0 | nav/sidebar | DIRECT2D,GDI | nav only: regenerate the sidebar after the page deletions |
| `deep-dives/renderers/direct3d9-xna-fidelity.html` | 1 | 0 | nav/sidebar | DIRECT2D,GDI | nav only: regenerate the sidebar after the page deletions |
| `deep-dives/renderers/sdl-gpu-pipeline-state-and-draw-order.html` | 1 | 0 | nav/sidebar | DIRECT2D,GDI | nav only: regenerate the sidebar after the page deletions |
| `deep-dives/renderers/sdl-gpu-resources-and-frame-recovery.html` | 1 | 0 | nav/sidebar | DIRECT2D,GDI | nav only: regenerate the sidebar after the page deletions |
| `deep-dives/renderers/vulkan-presentation-and-readback.html` | 1 | 0 | nav/sidebar | DIRECT2D,GDI | nav only: regenerate the sidebar after the page deletions |
| `deep-dives/renderers/webgpu-renderer-semantics.html` | 1 | 0 | nav/sidebar | DIRECT2D,GDI | nav only: regenerate the sidebar after the page deletions |

#### deep-dives/platforms (3 pages)

| Page | id-lines (gate) | SDL2 | Nature | Names | Action |
|---|---:|---:|---|---|---|
| `deep-dives/platforms/cross-platform-contract.html` | 4 | 15 | table rows(2); list(2); prose(1); SDL2(15) | HTML_DOM,FREEDIRECT,PORTABLEGL,SVG_DOM | Remove the SDL2 platform/audio route (15) and the DOM/FREEDIRECT/PORTABLEGL mentions. |
| `deep-dives/platforms/windows-cross-compiling-and-wine.html` | 19 | 0 | table rows(6); list(20); prose(21) | DIRECT2D,GDI | Remove the Direct2D Wine-prefix/Proton and GDI test-lane material (35 DIRECT2D + 12 GDI). Keep the DX9/11/12 Wine content. |
| `deep-dives/platforms/web-build-and-main-loop.html` | 15 | 0 | table rows(3); section heading; code; list(4); prose(34) | HTML_DOM,SVG_DOM | Delete the sections "HTML_DOM: automated browser and compositor evidence" and "SVG_DOM: a real browser harness without a caller". The Emscripten multi-renderer CI bundle is now WEBGL2+WEBGL1+CANVAS. |

#### deep-dives/siblings (3 pages)

| Page | id-lines (gate) | SDL2 | Nature | Names | Action |
|---|---:|---:|---|---|---|
| `deep-dives/siblings/freedirect-and-freeapi.html` | 35 | 0 | table rows(1); section heading; code; list(13); prose(62); nav/sidebar; free-direct/api(120) | FREEDIRECT,GDI,DIRECT2D | DEDICATED. Delete. CNA at T has no build reference to free-direct or free-api. Drop the siblings index count from 2 to 1, the deep_manifest.py siblings intro, and the easygl-and-metagl pager "next" link. |
| `deep-dives/siblings/index.html` | 6 | 0 | list(3); prose(4); nav/sidebar; free-direct/api(6) | FREEDIRECT | Change "2 pages" to 1 (easy-gl/meta-gl only) and drop the FreeDirect/FreeAPI intro. |
| `deep-dives/siblings/easygl-and-metagl.html` | 3 | 2 | prose(4); nav/sidebar; SDL2(2); free-direct/api(4) | FREEDIRECT,OPENGL4 | Drop the sidebar entry and pager-next link to the deleted page, and the FREEDIRECT comparisons. |

#### deep-dives/graphics (15 pages)

| Page | id-lines (gate) | SDL2 | Nature | Names | Action |
|---|---:|---:|---|---|---|
| `deep-dives/graphics/state-objects.html` | 5 | 0 | table rows(2); list(3); prose(2); 'OpenGL 4'(12) | PORTABLEGL,OPENGL4,GDI,DIRECT2D,FREEDIRECT | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality |
| `deep-dives/graphics/spritebatch-sorting-and-batching.html` | 7 | 0 | table rows(3); list(1); prose(6); 'OpenGL 4'(1) | OPENGL4,GDI,PORTABLEGL | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality |
| `deep-dives/graphics/texture-data-transfer.html` | 3 | 0 | list(1); prose(2); 'OpenGL 4'(4) | DIRECT2D,FREEDIRECT,PORTABLEGL | rewrite the sentence(s) to the 18-renderer reality |
| `deep-dives/graphics/shader-routes-four-answers.html` | 6 | 0 | table rows(8); prose(2) | OPENGL4,PORTABLEGL,GDI,FREEDIRECT,HTML_DOM,SVG_DOM,DIRECT2D | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality |
| `deep-dives/graphics/capability-model-and-evidence.html` | 5 | 0 | list(4); prose(13) | HTML_DOM,DIRECT2D,SVG_DOM,GDI,FREEDIRECT,OPENGL4,PORTABLEGL | rewrite the sentence(s) to the 18-renderer reality |
| `deep-dives/graphics/compiled-effects-semantics.html` | 4 | 0 | table rows(2); prose(2) | OPENGL4,GDI | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality |
| `deep-dives/graphics/graphicsdevice-contract.html` | 4 | 0 | prose(4) | OPENGL4,PORTABLEGL | rewrite the sentence(s) to the 18-renderer reality |
| `deep-dives/graphics/surface-formats.html` | 3 | 0 | table rows(5); prose(2); 'OpenGL 4'(1) | DIRECT2D,GDI,OPENGL4,PORTABLEGL | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality |
| `deep-dives/graphics/render-target-semantics.html` | 1 | 0 | prose(1); 'OpenGL 4'(2) | FREEDIRECT | rewrite the sentence(s) to the 18-renderer reality |
| `deep-dives/graphics/stock-effects-semantics.html` | 3 | 0 | prose(3) | OPENGL4,PORTABLEGL | rewrite the sentence(s) to the 18-renderer reality |
| `deep-dives/graphics/vertex-and-index-buffers.html` | 1 | 0 | prose(1); 'OpenGL 4'(2) | PORTABLEGL | rewrite the sentence(s) to the 18-renderer reality |
| `deep-dives/graphics/spritebatch-semantics.html` | 2 | 0 | prose(2) | OPENGL4 | rewrite the sentence(s) to the 18-renderer reality |
| `deep-dives/graphics/spritefont-text-layout.html` | 2 | 0 | table rows(3) | OPENGL4,FREEDIRECT | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows |
| `deep-dives/graphics/vertex-streams-and-declarations.html` | 2 | 0 | prose(2) | DIRECT2D,OPENGL4 | rewrite the sentence(s) to the 18-renderer reality |
| `deep-dives/graphics/device-reset-and-lifetime.html` | 1 | 0 | prose(1) | DIRECT2D | rewrite the sentence(s) to the 18-renderer reality |

#### deep-dives/foundations (3 pages)

| Page | id-lines (gate) | SDL2 | Nature | Names | Action |
|---|---:|---:|---|---|---|
| `deep-dives/foundations/ecosystem.html` | 6 | 1 | table rows(1); code; prose(5); SDL2(1); free-direct/api(27) | FREEDIRECT | Remove the free-direct/free-api rows, the diagram arrow and the paragraphs. They are no longer CNA build dependencies at T. |
| `deep-dives/foundations/cna-and-xna.html` | 1 | 3 | table rows(1); SDL2(3); free-direct/api(2) | FREEDIRECT | KEEP the FNA SDL2 remarks (they describe FNA, not CNA). Remove the "FREEDIRECT renderer fronts free-direct" bullet. |
| `deep-dives/foundations/compatibility-and-evidence.html` | 4 | 0 | table rows(9); list(4) | HTML_DOM,SVG_DOM,GDI,OPENGL4,PORTABLEGL,DIRECT2D,FREEDIRECT | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality |

#### deep-dives/practice (2 pages)

| Page | id-lines (gate) | SDL2 | Nature | Names | Action |
|---|---:|---:|---|---|---|
| `deep-dives/practice/porting-case-studies.html` | 6 | 0 | table rows(1); prose(6); free-direct/api(31) | FREEDIRECT,GDI | Remove the FREEDIRECT "migration bridge" recommendation. The free-direct audits concern non-CNA ports (owner decision: drop, or keep without any CNA-renderer link). |
| `deep-dives/practice/migrating-an-xna-game.html` | 1 | 1 | list(1); SDL2(1); 'OpenGL 4'(1); free-direct/api(1) | PORTABLEGL | rewrite the sentence(s) to the 18-renderer reality; remove the CNA SDL2 platform/audio mentions |

#### deep-dives/verification (2 pages)

| Page | id-lines (gate) | SDL2 | Nature | Names | Action |
|---|---:|---:|---|---|---|
| `deep-dives/verification/oracles-and-engagement.html` | 11 | 0 | table rows(1); section heading; list(3); prose(32) | DIRECT2D,HTML_DOM,SVG_DOM | Delete the section "Direct2D: prefixes, a virtual display and a pinned Proton". Drop the DOM evidence mentions. |
| `deep-dives/verification/test-populations-and-gates.html` | 4 | 0 | list(5); prose(3) | DIRECT2D,GDI | Remove the Direct2D/GDI test-population lines. |

#### deep-dives/build (5 pages)

| Page | id-lines (gate) | SDL2 | Nature | Names | Action |
|---|---:|---:|---|---|---|
| `deep-dives/build/third-party-dependencies.html` | 9 | 1 | table rows(7); section heading; prose(2); SDL2(1); free-direct/api(8) | FREEDIRECT,PORTABLEGL,OPENGL4,DIRECT2D,GDI | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality; remove the CNA SDL2 platform/audio mentions |
| `deep-dives/build/module-architecture.html` | 6 | 1 | table rows(8); list(3); prose(1); SDL2(1) | GDI,FREEDIRECT,OPENGL4,PORTABLEGL,DIRECT2D,HTML_DOM,SVG_DOM | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality; remove the CNA SDL2 platform/audio mentions |
| `deep-dives/build/configuring-cna.html` | 4 | 0 | prose(9) | DIRECT2D,HTML_DOM,SVG_DOM,GDI | rewrite the sentence(s) to the 18-renderer reality |
| `deep-dives/build/dependency-boundaries.html` | 1 | 2 | table rows(1); SDL2(2) | FREEDIRECT | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; remove the CNA SDL2 platform/audio mentions |
| `deep-dives/build/tools-and-scripts.html` | 3 | 0 | table rows(1); section heading; prose(7) | DIRECT2D,HTML_DOM | Delete the section "A gate over command text: the Direct2D parallelism cap". |

#### deep-dives/reference (3 pages)

| Page | id-lines (gate) | SDL2 | Nature | Names | Action |
|---|---:|---:|---|---|---|
| `deep-dives/reference/glossary.html` | 9 | 4 | prose(18); SDL2(4); free-direct/api(7) | FREEDIRECT,DIRECT2D,GDI,PORTABLEGL,HTML_DOM,SVG_DOM,OPENGL4 | rewrite the sentence(s) to the 18-renderer reality; remove the CNA SDL2 platform/audio mentions |
| `deep-dives/reference/verification-tiers.html` | 8 | 1 | table rows(4); list(6); prose(1); SDL2(1) | DIRECT2D,HTML_DOM,OPENGL4,GDI | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality; remove the CNA SDL2 platform/audio mentions |
| `deep-dives/reference/graphics-quick-reference.html` | 1 | 1 | table rows(1); SDL2(1) | PORTABLEGL | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; remove the CNA SDL2 platform/audio mentions |

#### deep-dives/services (9 pages)

| Page | id-lines (gate) | SDL2 | Nature | Names | Action |
|---|---:|---:|---|---|---|
| `deep-dives/services/input-model.html` | 6 | 0 | table rows(7); prose(3) | FREEDIRECT,OPENGL4,SVG_DOM,HTML_DOM,GDI,DIRECT2D,PORTABLEGL | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality |
| `deep-dives/services/sound-effects-and-streaming.html` | 0 | 4 | SDL2(4) |  | remove the CNA SDL2 platform/audio mentions |
| `deep-dives/services/avatars.html` | 3 | 0 | table rows(1); prose(4) | OPENGL4 | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality |
| `deep-dives/services/gamepads-and-haptics.html` | 0 | 1 | SDL2(1) |  | remove the CNA SDL2 platform/audio mentions |
| `deep-dives/services/media-contract.html` | 0 | 1 | SDL2(1) |  | remove the CNA SDL2 platform/audio mentions |
| `deep-dives/services/sensors-and-vibration.html` | 0 | 1 | SDL2(1) |  | remove the CNA SDL2 platform/audio mentions |
| `deep-dives/services/text-input-and-ime.html` | 0 | 1 | SDL2(1) |  | remove the CNA SDL2 platform/audio mentions |
| `deep-dives/services/touch-and-gestures.html` | 0 | 1 | SDL2(1) |  | remove the CNA SDL2 platform/audio mentions |
| `deep-dives/services/xact-runtime.html` | 0 | 1 | SDL2(1) |  | remove the CNA SDL2 platform/audio mentions |

#### deep-dives/framework (3 pages)

| Page | id-lines (gate) | SDL2 | Nature | Names | Action |
|---|---:|---:|---|---|---|
| `deep-dives/framework/math-coordinate-conventions.html` | 2 | 0 | prose(4) | PORTABLEGL,OPENGL4 | rewrite the sentence(s) to the 18-renderer reality |
| `deep-dives/framework/window-and-device-manager.html` | 1 | 0 | list(2); 'OpenGL 4'(1) | DIRECT2D,GDI | rewrite the sentence(s) to the 18-renderer reality |
| `deep-dives/framework/game-class-and-lifecycle.html` | 1 | 0 | prose(2) | DIRECT2D,GDI | rewrite the sentence(s) to the 18-renderer reality |

#### deep-dives/models (1 pages)

| Page | id-lines (gate) | SDL2 | Nature | Names | Action |
|---|---:|---:|---|---|---|
| `deep-dives/models/model-mesh-runtime.html` | 1 | 0 | prose(3); 'OpenGL 4'(1) | DIRECT2D,HTML_DOM,SVG_DOM | rewrite the sentence(s) to the 18-renderer reality |

#### deep-dives (top-level pages) (1 pages)

| Page | id-lines (gate) | SDL2 | Nature | Names | Action |
|---|---:|---:|---|---|---|
| `deep-dives/index.html` | 1 | 0 | section heading | FREEDIRECT | rewrite the sentence(s) to the 18-renderer reality |

#### development (top-level pages) (4 pages)

| Page | id-lines (gate) | SDL2 | Nature | Names | Action |
|---|---:|---:|---|---|---|
| `development/debugging.html` | 5 | 2 | table rows(2); list(8); SDL2(2) | OPENGL4,GDI,PORTABLEGL,DIRECT2D | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality; remove the CNA SDL2 platform/audio mentions |
| `development/invariants.html` | 2 | 4 | prose(3); SDL2(4) | FREEDIRECT,PORTABLEGL | rewrite the sentence(s) to the 18-renderer reality; remove the CNA SDL2 platform/audio mentions |
| `development/workflows.html` | 6 | 0 | table rows(5); list(4); prose(3) | OPENGL4,HTML_DOM,GDI,PORTABLEGL,FREEDIRECT,DIRECT2D | Workflow table: drop gdi-windows-ci and htmldom-ci (18 workflows, 26 jobs). Drop the DIRECT2D matrix leg. |
| `development/index.html` | 2 | 0 | list(5) | OPENGL4,DIRECT2D,PORTABLEGL,GDI,FREEDIRECT | rewrite the sentence(s) to the 18-renderer reality |

#### development/internals (30 pages)

| Page | id-lines (gate) | SDL2 | Nature | Names | Action |
|---|---:|---:|---|---|---|
| `development/internals/platforms/sdl2.html` | 2 | 68 | prose(2); SDL2(68) | FREEDIRECT,OPENGL4 | DEDICATED (SDL2 platform). Delete. Remove the dev_manifest.py entry (lines 233-234). Fix inbound links from internals/index and input/events. |
| `development/internals/graphics/opengl4.html` | 58 | 1 | table rows(8); section heading; code; list(48); prose(85); nav/sidebar; SDL2(1); 'OpenGL 4'(2) | OPENGL4,PORTABLEGL | DEDICATED. Delete. Also remove the dev_manifest.py entry (line 212) and the generate_dev_reference.py "opengl4" mapping (line 114). Fix inbound links from about 12 dev pages. |
| `development/internals/graphics/backends.html` | 38 | 0 | table rows(30); section heading; list(43); prose(27); nav/sidebar; 'OpenGL 4'(1); free-direct/api(7) | OPENGL4,GDI,FREEDIRECT,DIRECT2D,PORTABLEGL,HTML_DOM,SVG_DOM | Delete "OPENGL4 and EasyGL: separate families, shared GL semantics". Rewrite "SDL_RENDERER, DIRECT2D, GDI and FREEDIRECT" as the SDL_RENDERER and CANVAS 2D families. Family tables: 21 to 14. |
| `development/internals/platforms/index.html` | 5 | 30 | table rows(2); list(1); prose(2); SDL2(30) | PORTABLEGL,FREEDIRECT,GDI | Remove the SDL2 backend rows and prose (30). Platforms 7 to 6. |
| `development/internals/audio/engine.html` | 0 | 29 | SDL2(29) |  | Remove the SDL2 audio backend (Sdl2AudioDevice deleted in 76c9bda29). Audio implementations 4 to 3. |
| `development/internals/graphics/easygl.html` | 14 | 0 | section heading; list(3); prose(13); nav/sidebar | OPENGL4,PORTABLEGL | Rewrite "Stock shader corpus shared with OpenGL4". GlStockShaderSources.hpp and GlPresentationSurfaceState.hpp moved back under modules/renderers/easygl. |
| `development/internals/graphics/software.html` | 13 | 0 | section heading; list(5); prose(12); nav/sidebar | GDI,OPENGL4,DIRECT2D | Rewrite "Identity, build target and unusual GDI reuse". RRC-016 removed CNA_SOFTWARE_2D_ONLY, and SOFTWARE now compiles one full implementation. |
| `development/internals/platforms/sdl3.html` | 1 | 9 | prose(1); SDL2(9) | OPENGL4 | rewrite the sentence(s) to the 18-renderer reality; remove the CNA SDL2 platform/audio mentions |
| `development/internals/platforms/win32.html` | 7 | 3 | list(1); prose(8); SDL2(3) | GDI,DIRECT2D,OPENGL4,PORTABLEGL | rewrite the sentence(s) to the 18-renderer reality; remove the CNA SDL2 platform/audio mentions |
| `development/internals/input/events.html` | 2 | 7 | list(5); SDL2(7) | FREEDIRECT,OPENGL4,SVG_DOM,HTML_DOM,GDI | rewrite the sentence(s) to the 18-renderer reality; remove the CNA SDL2 platform/audio mentions |
| `development/internals/graphics/selection.html` | 8 | 0 | table rows(3); list(2); prose(7); nav/sidebar | OPENGL4,GDI,PORTABLEGL,DIRECT2D | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; regenerate the sidebar; rewrite the sentence(s) to the 18-renderer reality |
| `development/internals/graphics/device.html` | 6 | 0 | list(3); prose(4); nav/sidebar | OPENGL4,DIRECT2D,GDI | regenerate the sidebar; rewrite the sentence(s) to the 18-renderer reality |
| `development/internals/graphics/draw-call.html` | 6 | 0 | table rows(15); prose(1); nav/sidebar | OPENGL4,PORTABLEGL,GDI,HTML_DOM,SVG_DOM,DIRECT2D | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; regenerate the sidebar; rewrite the sentence(s) to the 18-renderer reality |
| `development/internals/platforms/x11.html` | 2 | 4 | prose(3); SDL2(4) | OPENGL4,PORTABLEGL | rewrite the sentence(s) to the 18-renderer reality; remove the CNA SDL2 platform/audio mentions |
| `development/internals/platforms/wayland.html` | 3 | 2 | prose(4); SDL2(2) | OPENGL4 | rewrite the sentence(s) to the 18-renderer reality; remove the CNA SDL2 platform/audio mentions |
| `development/internals/index.html` | 1 | 3 | table rows(2); SDL2(3) | OPENGL4 | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; remove the CNA SDL2 platform/audio mentions |
| `development/internals/modules/core.html` | 4 | 0 | prose(9) | PORTABLEGL,FREEDIRECT,SVG_DOM,OPENGL4 | rewrite the sentence(s) to the 18-renderer reality |
| `development/internals/modules/devices-ext.html` | 0 | 4 | SDL2(4) |  | remove the CNA SDL2 platform/audio mentions |
| `development/internals/modules/graphics-ext.html` | 4 | 0 | prose(13) | OPENGL4 | Drop the OPENGL4 mentions. The page is also affected by MOD-RETIRE-1 (graphics engine layer retired), which is outside R2. |
| `development/internals/platforms/terminal.html` | 2 | 2 | prose(2); SDL2(2) | PORTABLEGL | rewrite the sentence(s) to the 18-renderer reality; remove the CNA SDL2 platform/audio mentions |
| `development/internals/graphics/sdl-gpu.html` | 2 | 1 | nav/sidebar; SDL2(1) | OPENGL4 | nav only: regenerate the sidebar after the page deletions; remove the CNA SDL2 platform/audio mentions |
| `development/internals/graphics/vulkan.html` | 3 | 0 | list(1); nav/sidebar | OPENGL4 | regenerate the sidebar; rewrite the sentence(s) to the 18-renderer reality |
| `development/internals/modules/media.html` | 0 | 3 | SDL2(3) |  | remove the CNA SDL2 platform/audio mentions |
| `development/internals/platforms/headless.html` | 1 | 2 | prose(1); SDL2(2) | PORTABLEGL | rewrite the sentence(s) to the 18-renderer reality; remove the CNA SDL2 platform/audio mentions |
| `development/internals/graphics/resources.html` | 2 | 0 | prose(1); nav/sidebar | OPENGL4 | regenerate the sidebar; rewrite the sentence(s) to the 18-renderer reality |
| `development/internals/content/pipeline.html` | 1 | 0 | prose(2) | GDI | rewrite the sentence(s) to the 18-renderer reality |
| `development/internals/content/runtime.html` | 1 | 0 | prose(2) | OPENGL4 | rewrite the sentence(s) to the 18-renderer reality |
| `development/internals/graphics/headless.html` | 1 | 0 | nav/sidebar | OPENGL4 | nav only: regenerate the sidebar after the page deletions |
| `development/internals/graphics/stub.html` | 1 | 0 | nav/sidebar | OPENGL4 | nav only: regenerate the sidebar after the page deletions |
| `development/internals/modules/devices.html` | 0 | 1 | SDL2(1) |  | remove the CNA SDL2 platform/audio mentions |

#### development/reference (4 pages)

| Page | id-lines (gate) | SDL2 | Nature | Names | Action |
|---|---:|---:|---|---|---|
| `development/reference/cmake-options.html` | 3 | 6 | table rows(17); list(5); SDL2(6); free-direct/api(5) | PORTABLEGL,FREEDIRECT,HTML_DOM,SVG_DOM,DIRECT2D,OPENGL4,GDI | GENERATED (generate_dev_reference.py from TARGET). Regenerate at T. Removed: CNA_RENDERER_{DIRECT2D,FREEDIRECT,GDI,HTML_DOM,OPENGL4,PORTABLEGL,SVG_DOM}, CNA_OPENGL4_COMPILED_EFFECTS, CNA_BUILD_{HTML,SVG}_DOM_HOST_TESTS, CNA_DIRECT2D_TEST_RUNTIME, CNA_SDL2_*. |
| `development/reference/selection-axes.html` | 1 | 4 | table rows(29); SDL2(4) | OPENGL4,DIRECT2D,HTML_DOM,FREEDIRECT,GDI,SVG_DOM,PORTABLEGL | GENERATED. Regenerate at T (the generator cross-checks canonical counts, so update the facts first). |
| `development/reference/test-targets.html` | 2 | 0 | table rows(18); list(4) | HTML_DOM,SVG_DOM,DIRECT2D,GDI | GENERATED. Regenerate at T. |
| `development/reference/modules.html` | 1 | 0 | table rows(15) | OPENGL4,DIRECT2D,FREEDIRECT,GDI,HTML_DOM,PORTABLEGL,SVG_DOM | GENERATED. Regenerate at T. |

#### development/testing (2 pages)

| Page | id-lines (gate) | SDL2 | Nature | Names | Action |
|---|---:|---:|---|---|---|
| `development/testing/architecture.html` | 18 | 7 | table rows(11); section heading; list(15); prose(10); SDL2(7); free-direct/api(4) | OPENGL4,GDI,DIRECT2D,HTML_DOM,FREEDIRECT,SVG_DOM,PORTABLEGL | "Output gates: Vulkan and OpenGL4" becomes Vulkan only (the OpenGL4 GL-error ctest gate was removed). Drop gdi-windows-ci/htmldom-ci, the DIRECT2D leg and the SDL2 lanes. |
| `development/testing/index.html` | 4 | 0 | table rows(2); prose(8) | DIRECT2D,OPENGL4,GDI | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality |

#### development/handbook (9 pages)

| Page | id-lines (gate) | SDL2 | Nature | Names | Action |
|---|---:|---:|---|---|---|
| `development/handbook/change-build-configuration.html` | 4 | 13 | table rows(2); list(2); prose(1); SDL2(13); free-direct/api(1) | PORTABLEGL,FREEDIRECT,GDI,OPENGL4 | Remove the SDL2 recipes (13): CNA_PLATFORM=SDL2, CNA_SDL2_ROOT/GIT_TAG/GIT_REPOSITORY and the Sdl2OnlyConfiguration guard. |
| `development/handbook/fix-a-renderer-bug.html` | 17 | 0 | table rows(17); list(12); prose(4); free-direct/api(4) | OPENGL4,GDI,DIRECT2D,FREEDIRECT,PORTABLEGL,HTML_DOM,SVG_DOM | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality |
| `development/handbook/change-map.html` | 4 | 1 | table rows(8); SDL2(1) | PORTABLEGL,OPENGL4,GDI,FREEDIRECT,DIRECT2D | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; remove the CNA SDL2 platform/audio mentions |
| `development/handbook/modify-a-platform-backend.html` | 0 | 4 | SDL2(4) |  | remove the CNA SDL2 platform/audio mentions |
| `development/handbook/add-a-regression-test.html` | 2 | 0 | table rows(1); list(1) | OPENGL4 | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality |
| `development/handbook/conventions.html` | 2 | 0 | table rows(1); prose(1) | GDI,OPENGL4 | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality |
| `development/handbook/debug-shutdown-and-lifetime.html` | 1 | 1 | list(2); SDL2(1) | OPENGL4 | rewrite the sentence(s) to the 18-renderer reality; remove the CNA SDL2 platform/audio mentions |
| `development/handbook/make-a-release.html` | 2 | 0 | table rows(2); free-direct/api(1) | OPENGL4,GDI | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows |
| `development/handbook/update-libcna-com.html` | 1 | 0 | list(1) | OPENGL4 | rewrite the sentence(s) to the 18-renderer reality |

#### development/architecture (5 pages)

| Page | id-lines (gate) | SDL2 | Nature | Names | Action |
|---|---:|---:|---|---|---|
| `development/architecture/graphics.html` | 8 | 0 | list(11); prose(5) | OPENGL4,PORTABLEGL,DIRECT2D,GDI,HTML_DOM,SVG_DOM | rewrite the sentence(s) to the 18-renderer reality |
| `development/architecture/platform.html` | 2 | 5 | list(1); prose(1); SDL2(5) | FREEDIRECT,OPENGL4 | rewrite the sentence(s) to the 18-renderer reality; remove the CNA SDL2 platform/audio mentions |
| `development/architecture/overview.html` | 2 | 4 | prose(2); SDL2(4); free-direct/api(1) | OPENGL4,FREEDIRECT | rewrite the sentence(s) to the 18-renderer reality; remove the CNA SDL2 platform/audio mentions |
| `development/architecture/audio-input.html` | 0 | 5 | SDL2(5) |  | remove the CNA SDL2 platform/audio mentions |
| `development/architecture/runtime.html` | 1 | 0 | prose(1) | OPENGL4 | rewrite the sentence(s) to the 18-renderer reality |

#### development/repository (3 pages)

| Page | id-lines (gate) | SDL2 | Nature | Names | Action |
|---|---:|---:|---|---|---|
| `development/repository/source-ownership.html` | 7 | 3 | table rows(11); list(3); SDL2(3); free-direct/api(8) | OPENGL4,FREEDIRECT,GDI,PORTABLEGL | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality; remove the CNA SDL2 platform/audio mentions |
| `development/repository/index.html` | 5 | 3 | table rows(3); list(4); SDL2(3); free-direct/api(2) | GDI,FREEDIRECT,PORTABLEGL,DIRECT2D | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality; remove the CNA SDL2 platform/audio mentions |
| `development/repository/module-graph.html` | 6 | 1 | list(16); prose(8); SDL2(1) | GDI,FREEDIRECT,DIRECT2D,HTML_DOM,OPENGL4,PORTABLEGL,SVG_DOM | Drop the gdi/direct2d/freedirect/portablegl/html-dom/svg-dom/opengl4 module nodes (14 renderer families). |

#### development/build (2 pages)

| Page | id-lines (gate) | SDL2 | Nature | Names | Action |
|---|---:|---:|---|---|---|
| `development/build/architecture.html` | 6 | 10 | table rows(1); list(6); prose(6); SDL2(10); free-direct/api(1) | GDI,OPENGL4,FREEDIRECT,PORTABLEGL | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality; remove the CNA SDL2 platform/audio mentions |
| `development/build/index.html` | 6 | 5 | table rows(4); list(2); prose(1); SDL2(5); free-direct/api(1) | FREEDIRECT,OPENGL4,PORTABLEGL,GDI | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality; remove the CNA SDL2 platform/audio mentions |

#### development/takeover (10 pages)

| Page | id-lines (gate) | SDL2 | Nature | Names | Action |
|---|---:|---:|---|---|---|
| `development/takeover/review-ai-generated-code.html` | 11 | 0 | table rows(7); list(6); prose(6) | OPENGL4,DIRECT2D | The case study uses the OPENGL4 modern-graphics campaign. Replace it with a surviving renderer example (e.g. the WebGPU or STREETPERF work). |
| `development/takeover/threading.html` | 3 | 7 | table rows(1); list(6); SDL2(7) | OPENGL4 | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality; remove the CNA SDL2 platform/audio mentions |
| `development/takeover/validation.html` | 1 | 4 | table rows(3); SDL2(4) | OPENGL4 | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; remove the CNA SDL2 platform/audio mentions |
| `development/takeover/blast-radius.html` | 3 | 1 | table rows(1); list(3); SDL2(1) | OPENGL4 | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; rewrite the sentence(s) to the 18-renderer reality; remove the CNA SDL2 platform/audio mentions |
| `development/takeover/inherited.html` | 2 | 2 | prose(3); SDL2(2) | GDI,PORTABLEGL,OPENGL4 | rewrite the sentence(s) to the 18-renderer reality; remove the CNA SDL2 platform/audio mentions |
| `development/takeover/curriculum.html` | 2 | 0 | list(1); prose(2) | OPENGL4,PORTABLEGL | rewrite the sentence(s) to the 18-renderer reality |
| `development/takeover/mental-model.html` | 0 | 2 | SDL2(2) |  | remove the CNA SDL2 platform/audio mentions |
| `development/takeover/uncertainty.html` | 1 | 1 | table rows(1); SDL2(1) | OPENGL4 | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows; remove the CNA SDL2 platform/audio mentions |
| `development/takeover/xna-oracle.html` | 2 | 0 | table rows(2) | OPENGL4 | delete the OPENGL4/PORTABLEGL rows and drop the removed names from grouped rows |
| `development/takeover/investigation.html` | 1 | 0 | prose(1) | DIRECT2D | rewrite the sentence(s) to the 18-renderer reality |

#### data (2 pages)

| Page | id-lines (gate) | SDL2 | Nature | Names | Action |
|---|---:|---:|---|---|---|
| `data/known-issues.json` | 115 | 16 | prose(175); SDL2(16); free-direct/api(4) | OPENGL4,FREEDIRECT,DIRECT2D,GDI,HTML_DOM,SVG_DOM,PORTABLEGL | GENERATED SOURCE for known-issues/** (scripts/known_issues.py). 175 identity + 16 SDL2 hits. Retire or resolve the issues about removed renderers (27 dedicated pages), then regenerate. |
| `data/current-facts.json` | 1 | 2 | prose(5); SDL2(2) | DIRECT2D,HTML_DOM,SVG_DOM,FREEDIRECT,GDI | Update the facts (section 8.6): 25 to 18, 21 to 14, 7 to 2 (2D-only), 14 to 13 (10 to 9 families), 7 to 6 platforms, 4 to 3 audio, 20 to 18 CI files (28 to 26 jobs). The C ABI value is outside R2. |

#### img (1 pages)

| Page | id-lines (gate) | SDL2 | Nature | Names | Action |
|---|---:|---:|---|---|---|
| `img/architecture-diagram.svg` | 7 | 2 | prose(7); SDL2(2) | OPENGL4,FREEDIRECT,DIRECT2D,GDI,HTML_DOM,SVG_DOM,PORTABLEGL | GENERATED by scripts/make_architecture_diagram.py (lines 148-163 hard-code OPENGL4, FREEDIRECT, DIRECT2D, GDI, HTML_DOM, SVG_DOM and PORTABLEGL). Edit the script and regenerate. Also check any PNG export and the architecture.html caption "25 renderer identities". |
### 8.6 `data/current-facts.json` (feeds check_facts.py and generator count checks): values to change

| key | O value (site now) | T value | Evidence |
|---|---|---|---|
| renderer_identities | 25 | **18** | `cmake/RendererIdentities.cmake` L25-28 |
| implementation_families | 21 | **14** | `git ls-tree T modules/renderers/` dirs with src/ |
| two_d_only_renderers | 7 (method lists SDL_RENDERER, DIRECT2D, CANVAS, HTML_DOM, SVG_DOM, FREEDIRECT, GDI) | **2** (SDL_RENDERER, CANVAS) | §2 |
| graphics_capability_members | 19 | 19 (unchanged) | §2 |
| compiled_effect_identities | 14 ("10 families"; "nine default-OFF options") | **13** (9 families; FNA3D + eight default-OFF options) | §3 |
| platform_implementations | 7 (method "SDL3 SDL2 X11 WAYLAND WIN32 HEADLESS TERMINAL") | **6** (SDL3 X11 WAYLAND WIN32 HEADLESS TERMINAL) | `cmake/PlatformSelection.cmake` |
| audio_implementations | 4 ("SDL3 SDL2 NULL ALSA") | **3** (SDL3 NULL ALSA; SOUND_ENABLED for SDL3 and ALSA) | `cmake/AudioPlatformSelection.cmake` |
| ci_workflow_files | 20 ("28 jobs") | **18** (26 jobs) | §6 |
| c_abi_version | 0.29.0 | 0.44.0 (outside R2; verify with the C-API agent) | `abi.h` |

### 8.7 SDL2 on the site
- **Dedicated:** `development/internals/platforms/sdl2.html` (68 hits). Delete.
- **Heavy rewrite:**

| Page | SDL2 hits |
|---|---:|
| docs/platforms.html | 51 |
| development/internals/platforms/index.html | 30 |
| development/internals/audio/engine.html | 29 |
| docs/audio.html | 27 |
| architecture.html | 22 |
| docs/tutorials/127-platform-audio-selection.html | 22 |
| docs/building.html | 18 |
| features.html | 17 |
| deep-dives/platforms/cross-platform-contract.html | 15 |
| development/handbook/change-build-configuration.html | 13 |
| development/build/architecture.html | 10 |
| development/internals/platforms/sdl3.html (SDL2 comparisons) | 9 |

- **One-line mentions** in about 80 pages, mostly the audio-mixer sentence and platform lists in tutorials 14, 15, 30, 49, 50, 78, 88, 117-122 and in deep-dives/services/*.
- **Keep** FNA-SDL2 statements: `deep-dives/foundations/cna-and-xna.html` L177 and `deep-dives/reference/glossary.html` L150.
- Optionally add one neutral sentence where platforms are listed: "SDL2 platform and audio support was retired on 2026-10-04; CNA_PLATFORM=SDL2 and CNA_AUDIO_PLATFORM=SDL2 are rejected at configure time." This is allowed, because SDL2 is not a renderer identity. Owner's call.

### 8.8 free-direct and free-api: sibling projects, or only a CNA renderer?
- **They still exist independently** as openeggbert repositories:
  - `/rv/data/development/github.com/openeggbert/free-direct`: develop @ `9e1acd1`, 2026-09-30. README: "reimplements a narrow, game-driven subset of DirectX 3 (2D) using SDL3", MIT.
  - `/rv/data/development/github.com/openeggbert/free-api`: develop @ `8337b24`, 2026-09-30. A "minimal subset of the Windows API (WinAPI)" over SDL3, MIT.
  - Consumers outside CNA: free-eggbert and planetblupi.
- **CNA at T has no build reference to either.** `git grep -i 'free-direct\|free-api' T -- '*.cmake' '*CMakeLists.txt' modules` is empty, and the "Missing sibling repository 'free-direct'" check is gone. Only `easy-gl` is checked at T. Remaining mentions live in plans/, modularization/, integration/ and audit/ history plus `docs/removed-renderers.md`.
- **Recommendation:**
  - Remove free-direct/free-api from every CNA build or dependency statement: contribute.html clone list, docs/building Step 2, docs/faq, docs/releases ("easy-gl, meta-gl and free-direct use their default develop branch"), architecture "Required sibling repositories", about, index cards, ecosystem, third-party-dependencies, source-ownership, repository/index, development/build/*.
  - Delete the sibling deep dive.
  - The site gate does not flag the hyphenated name, but every existing site sentence ties it to the FREEDIRECT renderer.
  - If the owner wants the openeggbert Blupi ports mentioned at all (porting-case-studies, tutorial 95), describe them as non-CNA projects with no renderer link. Default recommendation: drop them, because CNA no longer consumes them.

### 8.9 Known-issues pages whose subject is a removed renderer or SDL2 (by title/h1; 27 of 103 pages with hits)
- **bugs:** cna-bug-133 (DX11/DX12/FREEDIRECT/METAL window transform; partially still relevant), 142 (SDL2/NULL songs never end; NULL part may still apply), 178 (SDL2 wheel), 189 (GDI), 190 (GDI software sources), 194 and 195 (SDL2-only guard), 249 (CNAEXT table omits OPENGL4/METAL), 257 (PORTABLEGL).
- **gaps:** cna-gap-009 (sub-pixel: EasyGL, OPENGL4, SOFTWARE), 014 (CANVAS+FREEDIRECT viewport; CANVAS part remains), 017 (FREEDIRECT/CANVAS PresentationMode; CANVAS part remains), 025 (DIRECT2D), 027 (HTML_DOM/SVG_DOM), 030 (FREEDIRECT), 059 (MinGW Wine emulator), 071 (EasyGL+OpenGL4 locking).
- **limitations:** cna-plat-001 (CANVAS/FREEDIRECT/SDL_RENDERER/DOM mips; partially remains), 006 (Direct2D under Wine), 007 (DOM plus-lighter).
- **verification-gaps:** cna-vgap-010 (no CI for OPENGL4), 021 (SpriteFont pixel tests list), 023 (browser paths), 026 (Windows families), 042 (FREEDIRECT), 044 (Wine D3D/D2D), 047 (test strength; mentions SDL2/others).
- **Action:** edit `data/known-issues.json`: retire issues whose only subject is removed, and strip removed names from mixed ones. Then regenerate.

## 9. Verification commands used (all read-only)
- Registries:
  - `git -C cna show T:cmake/RendererIdentities.cmake`, `…:cmake/RendererRegistry.cmake`, `…:cmake/RendererIdentityDefault.cmake`, `…:cmake/RendererDefaultSelection.cmake`.
  - `git diff O T -- cmake/Renderer*.cmake cmake/PlatformSelection.cmake cmake/AudioPlatformSelection.cmake cmake/SdlAvailability.cmake CMakeLists.txt CMakePresets.json`
- Families: `git ls-tree --name-only {O,T} modules/renderers/`
- Capabilities:
  - `git grep -n 'SupportsCapability\|SupportsCompiledEffects\|Supports(ComputeShaders|IndirectDraw)EXT' T -- modules/renderers`
  - The GraphicsCapability member count was parsed from the header at O and at T.
- Options: `git grep -o 'option(CNA_…' {O,T}` and `set(CNA_… CACHE` diffed with `comm`.
- CI: `git diff --name-status O T -- .github/workflows`; YAML `jobs:` counted with PyYAML for every workflow at O and T.
- Commits: `git log O..T --grep …` and `git show --stat` for 0f96ea703, 261cb5f7f, 590ac27c8, 3b9982646, 38e2209fb, 76c9bda29, 6ee00e35d, 2707098fa, 7301f386a, 5572f3ca1, FX-140..146, WEBGPUPERF, STREETPERF, FULLSCREEN, KF, VULKAN-154/159, METAL-282, DX-271.
- Site:
  - `python3 -B scripts/check_retired_renderers.py`: output saved to scratchpad `retired_check.txt`.
  - My classifier is `scratchpad/classify.py`, with per-page rows in `rows.json` and the table in `table.md`.
  - `git grep` phrase counts.
  - Sibling repo check: `git -C ~/…/openeggbert/free-{direct,api} log -1`.
