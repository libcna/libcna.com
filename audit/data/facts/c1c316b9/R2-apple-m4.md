# R2 — Apple / macOS / iOS / Metal at CNA `c1c316b9` (fact sheet)

Internal audit record (not served). Research only; no CNA build or run was performed for this sheet.

- **TARGET**: CNA `c1c316b9c7a846ce8002809c151fcd1af14942c9` (branch `apple/m4-stabilization`, 2026-10-09 17:22 +0200,
  "docs(Task AM4-306): name the run the earlier GPU hang came from").
- **BASE**: CNA `b0e97bb1bb876f9b3edd6f4ff1ef3067908ae8ac` (2026-10-04). `b0e97bb1` is an ancestor of TARGET;
  `git rev-list --count b0e97bb1..c1c316b9` = **354** commits (≈290 carry an `AM4-*` task id; the rest are `RRC-018..029`,
  `PLAT-142`, `MSR-*`, `FNA3D-53`, `SMG-0043`).
- **Primary source**: `plans/plan_apple_m4.md` at TARGET (340 lines, 249,697 bytes, read in full). Cited as `plan AM4-nnn`.
  Secondary: `docs/apple-platforms.md` (cited `apple-platforms.md:<line>`), `docs/metal-renderer.md`,
  `docs/metal-shader-effect-contract.md`, `docs/c-api/CONSUMING.md`, `.github/workflows/apple-ci.yml`,
  `.github/workflows/metal-macos-ci.yml`, `cmake/ApplePlatform.cmake`, `cmake/RendererSelection.cmake`.
- Every CNA SHA quoted below was checked with `git cat-file` in the CNA clone. **Sibling-repository SHAs are quoted from the plan only**:
  none of them exists in the local sibling clones (all are pre-campaign), so they are "as recorded by `plan_apple_m4.md`", not verified objects.

## Evidence-type legend (used in every row)

| Tag | Meaning |
|---|---|
| **M4-LOCAL** | Local manual campaign on the physical Mac mini M4 (real Apple hardware, real GPU). Not CI. |
| **M4-LOCKED** | As M4-LOCAL, but measured while the console session was locked (macOS reports every window occluded); on-screen presentation was therefore *not observed*. Applies to the Phase 4 full-tree run (`apple-platforms.md:191-193`) and to the WebGPU runs from AM4-088 on. |
| **SIM** | iOS Simulator (iOS 27 Simulator, iPhone 17 profile) on the M4 host. Simulator only, not a device. |
| **BUILD-ONLY** | Compiled/linked, not executed. |
| **CI-HOSTED** | GitHub-hosted runner (macos-26, "Apple Paravirtual device" GPU for Metal). Configured in the workflow; a *green* result after the last change is **not recorded** in the plan unless stated. |
| **TEST-SUITE** | ctest/gtest suite counts. |
| **PIXEL** | Readback / pixel comparison evidence. |
| **SOURCE** | Implementation/CMake/header fact at TARGET. |
| **DOC** | CNA documentation statement at TARGET (lower priority than plan records). |

---

## 1. Hardware and toolchain of the physical Mac mini M4 campaign

| Item | Value (verbatim from `plan_apple_m4.md` "Host" table, lines 16-21) | Evidence |
|---|---|---|
| Machine | **Mac mini M4, arm64, 16 GB** | plan "Host" |
| OS / SDK | **macOS 27.0.1 (26A434)**; SDKs MacOSX27.0, iPhoneOS27.0, iPhoneSimulator27.0 | plan "Host" (build string `26A434` recorded verbatim) |
| Toolchain | **Xcode 27.0 (27A266a), Apple clang 21.0.0**, CMake 4.4.4, Ninja 1.13.2 | plan "Host" |
| Homebrew deps | ffmpeg 9.0.2, zstd 1.5.7, curl, nlohmann-json 3.12, opus 1.6.1 | plan "Host" |
| Platform layer | `CNA_PLATFORM=SDL3` (SDL's Cocoa and UIKit video drivers); **no** COCOA/APPKIT/UIKIT backend of CNA's own | plan "Ground rules"; `apple-platforms.md:186-187` |
| Out of scope | Vulkan/MoltenVK on Apple; DirectX renderers not applicable | plan "Ground rules" |
| Dates | Mac mini M4 qualification 2026-10-07/08 (`apple-platforms.md:183`); Phase 4 close-out at `fdd33d2c6` (2026-10-09 04:03), Phase 5 (C API) and 6 (.NET) 2026-10-09, Phase 7 (CI) to TARGET | SOURCE (commit dates) |
| Other tools user-local on the M4 | Doxygen 1.9.8 built from source (AM4-160); Blender 4.3.2 (AM4-204); .NET SDK 8.0.425 osx-arm64 (AM4-215); emsdk 6.0.3 (AM4-282/298) | plan |

The site may say: "tested on a physical Mac mini M4 (Apple M4, 16 GB, macOS 27.0.1, Xcode 27, Apple clang 21)".

---

## 2. macOS evidence boundary, per area

### 2.1 Core CNA build/test portability (M4-LOCAL / M4-LOCKED, TEST-SUITE)

- Phase 1-2 portability fixes found by Apple clang/libc++ and Darwin (all "Done"): `std::from_chars` float availability under Xcode 26+ libc++ (AM4-002), `CNAEXT` attribute placement for Clang strict-API mode (AM4-003), FFmpeg 8 `sample_fmts` (AM4-004), libzstd by absolute path (AM4-005), missing includes (AM4-006), test video-driver adaptation x11→cocoa (AM4-007), immortal mutexes for Darwin's EINVAL-on-destroyed-mutex (AM4-022, AM4-073), APFS normalization (AM4-024, AM4-111), arm64 FMA contraction off for XNA bit fidelity (`-ffp-contract=off` on `cna_math`, `AvatarModel.cpp`, SOFTWARE renderer; AM4-046, AM4-053), FBX −1 material index UB (AM4-047), test portability (AM4-048), Mach-O `nm` in tooling (AM4-049), Release-only `bad any cast` from incomplete-type `typeid` on Apple arm64 (AM4-161), test user-data isolation (AM4-162), socket-suite `RESOURCE_LOCK` (AM4-163), C API media smokes `CFFIXED_USER_HOME` (AM4-164), Draco-aware XNB corpus sweep (AM4-165), avatar catalog v3 check on non-glibc (AM4-166), `ModuleLinkClosure_*` under Ninja (AM4-167).
- **Phase 4 full-tree result at `fdd33d2c6`**, `ctest -j3`, console locked (`apple-platforms.md:191-224`; plan AM4-208):

| Renderer tree (macOS, SDL3 platform) | Result | Skips |
|---|---|---|
| METAL | 11,015 / 11,015 | 114 |
| SOFTWARE | 11,084 / 11,084 | 133 |
| OPENGL33 (EasyGL, compiled effects ON) | 11,916 / 11,916 | 128 |
| SDL_GPU (SDL's Metal driver) | 10,962 / 10,962 | 295 |
| WEBGPU (wgpu-native v29.0.1.1, Metal backend) | 10,968 / 10,968 | 279 |
| FNA3D (FNA3D's Metal driver = its SDL_GPU driver on Metal) | 10,875 / 10,875 | 433 |
| SDL_RENDERER | 10,940 / 10,940 | 966 (2D-only refusals) |

  "Skip counts are tests that decline by name ... never failures" (`apple-platforms.md:196-197`). The pre-fix baseline was 422 failing cases, every one classified before patching (plan AM4-208; report `zero-failure-macos-report.md` is in campaign cold storage, **not in the CNA tree**).
  Evidence type: **M4-LOCKED, TEST-SUITE**, Debug trees except where a Release tree is named.
- Release tree: METAL Release `cna-macos-sdl3-metal-release` built without errors; `ctest -L Metal`/`MetalOracle` 261/261; full suite 11,015 tests in 435 s (AM4-156). Residual Release-only failure fixed by AM4-161.
- Not covered on macOS: `.fx` compilation by the external fxc (`XnaDifferentialBuildTest` skips `.fx` cases without fxc, AM4-048); shaderc-dependent shader-package reproducibility tests skip (no shaderc on the host, AM4-168); `CnaXnbDependencyBoundary` needs FreeType (AM4-049); `EasyGL_XnaLineCoverage` needs Pillow (AM4-059, owner decision).

### 2.2 SDL3 platform on macOS (M4-LOCKED, TEST-SUITE)

- SDL3 is the only graphical platform (`apple-platforms.md:186-187`, `:240-242`: `CNA_PLATFORM_<NAME>` = `SDL3`, `HEADLESS`, `TERMINAL`).
- Fixes: test video-driver adaptation (AM4-007), haptics enumeration crash (AM4-045, AM4-117; `Sdl3InputDevicesTest` 10/10), Cocoa/UIKit main-thread requirement surfaced with a named refusal (AM4-074), Headless-window test integrity (AM4-119), platform refusal reported as `NoSuitableGraphicsDeviceException` for SDL_GPU/FNA3D/SDL_RENDERER without SDL video (AM4-176, AM4-188, AM4-207).
- Baseline: SDL_RENDERER full tree 10,940/10,940, 966 skip (`apple-platforms.md:204`), "PASS WITH KNOWN LIMITATION" (2D-only by design).
- Main-thread rule: SDL's Cocoa video driver initializes only on the process's main thread (AM4-074; `docs/c-api/CONSUMING.md` "macOS").

### 2.3 OpenGL / `OPENGL33` (EasyGL on Apple's OpenGL 4.1 core "4.1 Metal")

- Before: 55 of 400 EasyGL tests failed on macOS (AM4-040). Fixes: ES→desktop GLSL header rewrite where `GL_ARB_ES3_compatibility` is missing (AM4-040, AM4-055, AM4-116), lit BasicEffect without Normal (AM4-056), fallback-texture unit (AM4-057), occlusion-query dispose (AM4-058, AM4-115), line pixel centre with 4 subpixel bits (AM4-059), PBR singular World (AM4-060, AM4-125), **compiled effects on macOS's 4.1 core context via MojoShader's GLSL ES 3.00 route chosen by a probe compile** (AM4-062: 1,875/1,875 compiled-effect/effect tests; house-simulator Tier E renders), `texture3DProj` patch (AM4-063).
- Result: full tree **11,916/11,916, 128 skip, with `CNA_EASYGL_COMPILED_EFFECTS=ON`; cna-samples 91/91** — "PASS WITH KNOWN LIMITATION" (`apple-platforms.md:206`). **M4-LOCKED, TEST-SUITE.**
- Limitations still recorded: Apple's GL stores 24-bit depth as float32, so the normalized `DepthBias` contract case is skipped on OPENGL33 (AM4-171); over-cap anisotropy kept/clamped at filter time (AM4-172, expectation relaxed, not a CNA limit).
- `OPENGLES3`: **NOT APPLICABLE** on macOS (no native OpenGL ES) (`apple-platforms.md:211`).

### 2.4 Native `METAL` renderer

**What exists (SOURCE + M4-LOCAL):** direct `MTLDevice`/`MTLCommandQueue`/`MTLRenderCommandEncoder`/`CAMetalLayer` renderer on the SDL3 window
(`NSWindow*` macOS, `UIWindow*` iOS); not routed through SDL_Renderer/SDL_GPU (`metal-renderer.md:5-10`). Supported targets: macOS and,
since AM4-037, iOS/iPadOS; CMake rejects METAL elsewhere (`metal-renderer.md:12-13`).

**Feature list made native in the campaign** (each "Done" in the plan; capability table `metal-renderer.md:111-126`):

| Feature | Task(s) | Key evidence (M4, Metal validation layers on unless noted) |
|---|---|---|
| Backbuffer readback (`GetBackBufferData`) in logical backbuffer coordinates, Retina/letterbox aware | AM4-025 | `metal_capabilities_test`, shared pixel tests |
| 3D geometry (WVP transpose bug) and D3D9 pixel-centre convention | AM4-028, AM4-029, AM4-149 (lines) | `xna_pixel_center_contract_test`, `draw_line_topology_test` |
| Declaration-driven vertex input; integer/BLENDINDICES formats | AM4-035, AM4-152, AM4-155 | 12 portable tests; `software_vertex_declaration` 20/20 |
| Sampler `MaxMipLevel`, LOD bias (macOS/iOS 26 SDK+OS) | AM4-034, AM4-099, AM4-296 | `texture_filter_mip_contract_test` |
| Occlusion queries (one open at a time) | AM4-038, AM4-108 | `occlusion_query_test`, `OcclusionQueryLifecycleTest` |
| SpriteBatch-scoped MSL custom effects | AM4-077, AM4-121 | `Metal_SpriteBatch_CustomEffect` 10/10 |
| `ColorWriteChannels` (target 0; 1..3 for compiled MRT) | AM4-079, AM4-146 | `gfx077_colorwritechannels_3d_test` 8/8 |
| MRT up to 8 targets | AM4-097 | `Metal_MRT_StockEffectContract` 19/19 (22/22 with MSAA scenarios after AM4-141) |
| Autorelease pools (per-frame leak fixed) | AM4-102 | 6,000-frame loop: no growth after; `Metal_Smoke_AutoreleasePools` |
| DepthBias in normalized depth (Direct3D 9 semantics) | AM4-134, AM4-151 | `depth_bias_magnitude_contract_test`, `RasterizerDepthBiasContractTest` |
| **MSAA** (backbuffer, RT2D, RTCube, MRT; M4 supports 2x and 4x, not 8x) | AM4-141 | `msaa_fragment_contract_test` 29/29, `Metal_PresentationMsaaContract` |
| **Float / wide / packed surface formats** (RT2D, RTCube, Texture2D) | AM4-142 | `RenderTargetFormatAgreement`, `rendertarget_surface_format_contract_test` 10/10 |
| **Instancing and multi-stream vertex input** (and base-instance) | AM4-143, AM4-154 | 103 shared CnaTests + `instanced_textured_draw_test` 37/37 |
| **Compiled XNA effects** via MojoShader SPIR-V → SPIRV-Cross → MSL, opt-in **`CNA_METAL_COMPILED_EFFECTS` (default OFF)** | AM4-144 | 43 Metal tests + 1,237 effect/SpriteBatch tests in the FX tree (`cna-macos-sdl3-metal-fx-debug`) |
| Skinned normal in world space | AM4-145 | `Metal_SkinnedEffect_WorldNormal` 12/12 |
| **Cube and volume** textures in every uncompressed format; RenderTargetCube `SetData` | AM4-147 | cube/volume transfer tests |
| **DXT1/3/5** Texture2D and TextureCube (BC on every Mac; decoded RGBA8 fallback where no BC, e.g. iPhone GPUs) | AM4-148 | `Metal_Shared_dxt_texturecube_test` 11/11, `Metal_DxtDecodedFallback_SharedTests` 27/27 |
| Shared fixtures / oracle corpus coverage | AM4-026, AM4-149, AM4-150, AM4-154, AM4-155, AM4-158 | `ctest -L Metal`/`MetalOracle` **261/261** (101 shared pixel fixtures, 146 renderer-neutral oracles, 14 native) |
| Backbuffer `DepthStencilFormat`, Depth16 native | AM4-151 | 14 `BackBufferDepthStencilContractTest` cases |
| SpriteBatch whole transform (layerDepth, W, near clip); sub-pixel float positions; sprite batching | AM4-153, AM4-136, AM4-157 | 8 depth cases; `spritebatch_subpixel_contract_test`; bench 1.26 → 0.91 ms/frame (500 sprites) |
| Fog on unlit/alpha-test/dual-texture | AM4-137 | `stock_effect_fog_contract_test` |
| Command-buffer failure reporting | AM4-138 | unit test |
| Managed-storage sync before CPU writes (Intel/AMD/paravirtual) | AM4-289 | measured on the CI paravirtual device (probe); M4 unaffected |

**Verdict (AM4-159, commit `d8fb6e8ee`):** "Phase 3 closes at **SUPPORTED**." Inventory baseline at `48236696f`: 133 rows (74 FULL, 30 PARTIAL,
26 NOT IMPLEMENTED, 3 UNKNOWN). New verdict evidence: cna-samples Release multi-renderer tree with `CNA_METAL_COMPILED_EFFECTS=ON`
90/91 `AUTOMATED_PASS` (Yacht failed on every renderer; fixed by AM4-169, after which the matrix row reads **91/91**, `apple-platforms.md:205`);
16 compiled-effect CnaTests pass in the FX tree; iOS device apps compile and link at `a1c46e534`.
**"Not primary-production, because compiled effects are off in a default build, on-screen presentation was never observed (locked console),
no physical iOS device ran it, and no soak run bounded the caches."** (plan AM4-159; `metal-renderer.md:71-74`). Release qualification: AM4-156.

**Matrix row** (`apple-platforms.md:205`): METAL **PASS WITH KNOWN LIMITATION** — full tree 11,015/11,015 (114 skip); `-L Metal` 261/261;
Release 261/261; compiled effects 43 + 1,237; cna-samples 91/91; iOS device build links; cna-examples 248/248.

**Limitations still recorded for METAL** (AM4-159; `apple-platforms.md:205`; `metal-renderer.md`):
- compiled XNA effects are opt-in (`CNA_METAL_COMPILED_EFFECTS`, default OFF — `cmake/RendererSelection.cmake:347-348`);
- custom `ShaderEffect`s are SpriteBatch-scoped MSL only; a 3D draw with a custom effect throws; `[[color(1..)]]` outputs discarded under MRT (`metal-shader-effect-contract.md`);
- `PresentInterval.Two` presents as `One` (AM4-139 parked: needs an unlocked console);
- backbuffer always BGRA8 (reported as `Color`);
- sampler LOD bias needs macOS/iOS 26 (SDK and OS; AM4-099), and is refused on a device measured to ignore it (AM4-296);
- a multisampled RenderTarget2D loses a `SetData` under `PreserveContents`; a multisampled RenderTargetCube refuses `SetData` (AM4-147);
- shared-layer gaps: vertex textures (FX-109), Texture2D `GetData` without the CPU shadow, `LightingEnabled` without NORMAL0, backbuffer `PreserveContents`;
- CNAEXT scope not provided: custom MSL beyond SpriteBatch, compute, indirect draws, array slices;
- unbounded caches (no soak run);
- packed Bgr565/Bgra5551/Bgra4444 only on Apple-family GPUs; an Intel Mac GPU refuses them by name (AM4-142) — and **no Intel Mac was run**;
- DXT volume textures unsupported (as XNA keeps DXT out of Texture3D: AM4-147/148).
- Internal CNA doc inconsistency to *not* copy: `metal-renderer.md:83` (METAL-259 row) still says "MSAA capability is false"; superseded by AM4-141 (`metal-renderer.md:115`).

### 2.5 `WEBGPU` on macOS (wgpu-native v29.0.1.1 on its Metal backend)

- **Correction recorded by the plan:** before AM4-088 the WebGPU GPU tests had **never** run on macOS — the launcher returned the skip code (no X11/Wayland socket) and ctest counted 148 skips as passes (AM4-052 correction, AM4-088).
- Fixes: occluded-surface frames (AM4-052, AM4-078, AM4-089, AM4-109, AM4-118), occlusion counts boolean on Metal adapters (AM4-091), `RenderTarget2D.SetData` (AM4-094), instanced World (AM4-095), COLOR0 saturation (AM4-096, AM4-106), occlusion lifecycle (AM4-108), partial `MultiSampleMask` refused on Metal adapters (AM4-131, AM4-132), 16 vertex bindings (AM4-185), partial compressed cube writes (AM4-186), HdrBlendable/HalfVector4 Texture2D (AM4-187).
- Result: `WebGPU_*` 150/150 (AM4-131); full tree **10,968/10,968, 279 skip; cna-samples 91/91** — PASS WITH KNOWN LIMITATION (`apple-platforms.md:208`). **M4-LOCKED** (WebGPU renders offscreen when occluded since AM4-089).
- Limitations: wgpu-native's Metal backend ignores `MultiSampleMask` (partial mask refused by name on a Metal adapter) and counts occlusion as a boolean (`PixelCountIsPreciseEXT()` false) (AM4-091, AM4-131).

### 2.6 `SDL_GPU` on macOS (SDL3 GPU API on its Metal driver)

- Did not configure before AM4-039 (CMake `LINK_GROUP:RESCAN` unsupported by ld64). Fixes: AM4-064..070, AM4-107, AM4-124, AM4-174, AM4-175, AM4-176, AM4-181 (point lists), AM4-183 (forwarded draw ranges), AM4-184 (float/wide Texture2D formats).
- Result: full tree **10,962/10,962, 295 skip; cna-samples 90/91** (LensFlare `RENDERER_UNSUPPORTED`: SDL3's GPU API has no occlusion queries) (`apple-platforms.md:207`). **M4-LOCKED.**
- Limitations: no occlusion queries; SDL's Metal backend ignores `mip_lod_bias`; the GLSL/SPIR-V `ShaderEffect` capability is off on Apple (`modules/renderers/sdl-gpu/CMakeLists.txt:59-64`, AM4-175). Compiled XNA effects use a separate route (not re-stated here).

### 2.7 `FNA3D` on Apple

- **Default FNA3D driver on Apple is now `Metal`** (FNA3D's SDL_GPU driver on Metal) for the registered tests; Linux keeps OpenGL (AM4-051). The legacy macOS OpenGL path is a GL 2.1 compatibility context, where `Fna3d_RenderTarget_Advanced` leaks a draw into an unbound cube face (AM4-042/051, not root-caused).
- Fixes: MojoShader Metal profile `TEXCRD` + D3D9 vertex-colour clamp (AM4-192), missing stock input refused by name instead of crashing (AM4-190), NormalizedByte2 channel fill (AM4-193), platform refusal without SDL windows (AM4-188), expectations (AM4-189), LOD bias declared unsupported on Apple (AM4-191).
- Result: full tree **10,875/10,875, 433 skip; cna-samples 90/91** (LensFlare `RENDERER_UNSUPPORTED`) (`apple-platforms.md:210`). **M4-LOCKED.**
- Limitations: no occlusion queries on FNA3D's Metal driver; float render-target formats not promoted (Metal asserts on Bgra4444; cube/partial-transfer/swizzle paths break, AM4-189); LOD bias ignored on Apple except with the OpenGL driver (AM4-191); MojoShader does not saturate oD0/oD1 on non-Metal profiles (AM4-106 records FNA divergence; Metal profile patched by AM4-192).

### 2.8 `SOFTWARE`, `SDL_RENDERER`, others on macOS

- SOFTWARE: **PASS**, full tree 11,084/11,084, 133 skip (`apple-platforms.md:209`); arm64 FMA fix (AM4-053).
- SDL_RENDERER: PASS WITH KNOWN LIMITATION, 10,940/10,940, 966 skip (2D-only) (`:204`).
- WEBGL2: **NOT TESTED** (no emsdk on the host for that matrix; `:212`) — note: an Emscripten WEBGL2;WEBGPU bundle was later *built* on the M4 for CI reproduction (AM4-282, AM4-298), not run as a macOS renderer.
- HEADLESS, STUB: NOT TESTED in the matrix (`:213`) (HEADLESS-default multi tree used for some test fixes, AM4-268/269).
- VULKAN (MoltenVK): **OUT OF SCOPE** (`:214`). DIRECTX9/DIRECTX11: NOT APPLICABLE (`:215`).

### 2.9 Compiled XNA effects on macOS (summary)

- METAL: opt-in `CNA_METAL_COMPILED_EFFECTS` (AM4-144), default OFF.
- OPENGL33: `CNA_EASYGL_COMPILED_EFFECTS=ON` works on macOS's 4.1 core context through MojoShader's GLSL ES 3.00 route (AM4-062).
- FNA3D: always compiled effects (through MojoShader's Metal profile on Apple; AM4-192 patches).
- Two MojoShader patches added in this delta: `mojoshader-6333f74-glsles3-texture3d-proj.patch` (AM4-063), `mojoshader-6333f74-spirv-predicated-texkill.patch` (AM4-144), and the two FNA3D Metal-profile patches (AM4-192; 128 patches in series).
- `.fx` *compilation* (content build through the external fxc) was **not** exercised on macOS (AM4-048).

### 2.10 Content on macOS

- `cna-content` CLI Unicode-path exercise reproduced on the M4 SOFTWARE tree (AM4-278). XNB model corpus sweep passes with Draco linked (148 fixtures, AM4-165). FbxImporter −1 material index (AM4-047). WMA encoder on FFmpeg 8+ (AM4-004). Content parity report regeneration (AM4-050).
- house-simulator's content pipeline (non-Blender stages) and, with a user-local Blender 4.3.2, its world content were built on the Mac (AM4-199, AM4-204).
- FFmpeg: Homebrew FFmpeg dylibs are built for the host macOS (27.0), so `CNA_ENABLE_VIDEO=AUTO` binaries linked against them do not start below that macOS whatever the 13.3 deployment target says; keep the floor with `CNA_ENABLE_VIDEO=OFF` or an FFmpeg built for the floor (AM4-130; `apple-platforms.md:73-77`). **DOC + M4-LOCAL (linker warning).**

### 2.11 Avatars / Gamer Services on macOS

- Guide/gamer-services UI tests on Metal: 130/130 (AM4-086, AM4-090); Guide input fixes are platform-independent (AM4-086, AM4-090, AM4-111).
- Avatar fixes: AvatarRenderer partial upload crash on 2D renderers (AM4-008), standard avatar `World` in `EasyGL_AvatarRenderer_Standard` (AM4-082, passes on macOS OPENGL33), `-ffp-contract=off` on `AvatarModel.cpp` (AM4-046), catalog v3 frozen-bytes check on non-glibc C libraries (AM4-166: 137 of 94,555 words differ in six `FemaleShocked` rotations; check passes on the M4 with the documented relaxation).
- Online: reliable data after host migration fixed (AM4-200; 30/30 repeats, 304 networking cases on the Metal Debug tree).
- cna-gamer-services-server: see §5.

### 2.12 SystemLink discovery on macOS (AM4-043)

`ENetDiscoveryService.cpp`, Apple-guarded: `SO_REUSEPORT` for a second UDP socket on the discovery port; broadcast also to every up interface's
broadcast address (255.255.255.255 → EHOSTUNREACH on macOS); search sends from its own ephemeral socket. **`TwoProcessLoopbackTest` 8/8, ENet suites
81/81** on the M4; Linux path byte-identical. **M4-LOCAL, TEST-SUITE (loopback/two-process on one machine; no multi-machine evidence).**
Socket suites later run under a `RESOURCE_LOCK cna-network` (AM4-163).

### 2.13 Relay with libcurl without WebSockets (AM4-044, AM4-123)

- Apple's system libcurl **8.7.1 has no WebSocket support**; the relay URL path now refuses with `RELAY_SECURE_WEBSOCKET_UNAVAILABLE` (not `RELAY_CONFIGURATION`) (AM4-044). **Owner decision recorded: with the system libcurl the relay cannot work on macOS; Homebrew curl 8.22 has ws/wss.**
- AM4-123: capability rule is a pure function `relayTransportRefusalFor(version, protocols, tls)`, tested on synthetic data (8.11 and 7.86.0 with ws/wss+TLS accepted; 7.85, Apple 8.7.1, ws-without-wss, no TLS, no protocol list refused). `RelayTransportTest` 5/5.
- C API doc: "The SDK's own libcurl works for TLS but has no WebSocket support, and a build that found it refuses the online relay transport by name" (`docs/c-api/CONSUMING.md`, macOS section).
- iOS: networking needs `CNA_ENABLE_NET=OFF` (the iOS SDK ships no libcurl) (AM4-105; `apple-platforms.md:117-119`).

### 2.14 Homebrew FFmpeg raises the deployment floor (AM4-130)

See §2.10. Defaults: `CNA_MACOS_DEPLOYMENT_TARGET=13.3` (floor; float `std::to_chars`), `CNA_IOS_DEPLOYMENT_TARGET=16.3` (`apple-platforms.md:65`, `:132`).

### 2.15 Remaining macOS skips / known failures / open items at TARGET

- No failing case in any of the seven Phase 4 trees (all skips by name). Skip counts per tree in §2.1.
- Open items recorded (not failures): AM4-139 `PresentInterval.Two` (needs unlocked console); AM4-059 Pillow (owner); AM4-049/160 Doxygen version (C API coverage gates skip unless `CNA_C_API_DOXYGEN` points at 1.9.x); AM4-076/170 resolved; AM4-092 open WebGPU/SDL_GPU items listed there were later fixed by AM4-094..096, AM4-131, AM4-177, AM4-181, AM4-183..187; AM4-189 FNA3D float targets open; house-simulator two upstream questions (§5); `Unsupported3DBehavior`/`CubeVolume_*` resolved by AM4-196.
- Phase 4 run conditions: console locked; one tree re-run after a display-sleep stall (`caffeinate -d -i -m` advice) (`apple-platforms.md:191-196`).

### 2.16 macOS CI (CI-HOSTED) vs real M4

| Workflow | What it runs at TARGET | Recorded outcome |
|---|---|---|
| `metal-macos-ci.yml` | `runs-on: macos-26`; configure `-DCNA_GRAPHICS_RENDERER=METAL -DCNA_BUILD_TESTS=ON`; `ctest -R '^Metal'` (518 tests per AM4-279/289) with `MTL_DEBUG_LAYER=1`; shader validation and parallelism chosen per device (paravirtual: shader validation off, `--parallel 1`) | Hosted GPU is an **"Apple Paravirtual device"** (Apple1-5 + Mac2). Runs recorded: 154/518 failed before AM4-279; 29 after AM4-279 (run 37925410941); 516/518 (37939872061); 517/518 (37946285992, GPU hang). AM4-306 serialised the run. **No green run after AM4-306 is recorded in the plan.** The 518/518 figure is the M4's (AM4-289). |
| `apple-ci.yml` | `apple-cmake-check` (ubuntu-24.04); `macos-build` (macos-26, SDL_RENDERER, `CnaTests` filtered to TargetPlatform/GameWindow/lifecycle/Storage/DesktopOS, plus `cna_macos_smoke.app` bundle); `ios` matrix of 4 legs: SDL_RENDERER device/simulator and **METAL device/simulator**; simulator legs launch `cna_ios_smoke` and, for METAL, `cna_ios_pixel_probe` | Runners moved from macos-14 to macos-26 (AM4-255); nlohmann-json added (AM4-247); sharp-runtime branch (AM4-234). **No green run on macos-26 is recorded in the plan.** The last recorded green Apple-workflow run in CNA docs is still run 31736845749 for `be4ea08bc` on macOS 14 (`apple-platforms.md:28-30`, `:323-325`) — pre-campaign evidence. |

- Hosted-runner findings that changed product code: Managed-storage sync (AM4-289), LOD-bias probe (AM4-296), shader-validation incompatibility of the paravirtual device (AM4-279, AM4-283).
- **Internal CNA doc staleness (do not copy):** `apple-platforms.md:314` still says "macOS 14 runner" and `README.md:50` "A dedicated macOS 14 workflow"; the workflows run on `macos-26` (AM4-255). `README.md:48`/`:238` still call METAL "macOS only, experimental ... iOS ... not claimed" and `README.md:428-438`'s iOS configure lacks `-DCNA_ENABLE_NET=OFF` — README was not updated by the campaign (last touched by RRC-019 in the delta).

---

## 3. iOS

| Claim | Exact record | Evidence type |
|---|---|---|
| Native METAL on iOS/iPadOS | AM4-037 (commit `b0390cbbc`): new `NativeWindowSystem::UIKit` (`UIWindow*`, `TryGetUIKit`; C API `CNA_NATIVE_WINDOW_SYSTEM_UIKIT`=9, ABI 0.46.0); renderer adds a touch-transparent `CAMetalLayer`-backed UIView to SDL's root view; links UIKit on iOS; METAL joins the iOS allow-list and the iOS CI matrix (device + simulator). | SOURCE |
| First simulator result (verbatim) | "Evidence (iOS 27 Simulator, iPhone 17): smoke OK; probe exact on 29 of 31 launches -- the two all-zero runs were the first two after first install and did not reproduce; device build links (Mach-O platform 2, system Metal/UIKit only), not run (no device/signing)." (plan AM4-037). `apple-platforms.md:39-42` words it: "exact on 29 of 31 simulator launches (two all-zero runs right after first install did not reproduce)". | SIM, PIXEL |
| **Root cause later found** | AM4-120 (commit `f27d59bf9`): the stricter probe (first frame on macOS; up to 120-frame warm-up on iOS; then 10 more correct frames) failed 3 of 4 iOS Simulator launches; root cause SDL's `UIKit_ComputeViewFrame` swapping portrait bounds for a landscape-only orientation set before UIKit rotated the window → a 1346x0 root view (drawable 4038x1). "**This is also what the two unexplained all-zero launches at AM4-037 were.**" CNA carries `cmake/patches/sdl-cbe3fbe9-0005-uikit-scene-window-frame.patch` (iOS builds only). After the fix: instrumented probe 61/61 frames correct in 4 of 4 launches; **committed probe 8 of 8 launches (first good frame 1, 10 confirmed)**; `cna_ios_smoke` OK; device build links. | SIM, PIXEL |
| Matrix row | "iOS Simulator, SDL3 + `METAL` — **PASS** — `cna_ios_pixel_probe` (iOS 27 Simulator, iPhone 17 profile) exact on frame 1 and on the 10 frames after it in 8 of 8 launches at `AM4-120`, `cna_ios_smoke` OK" (`apple-platforms.md:216`). | SIM, PIXEL |
| Other simulator re-checks | AM4-105: head-of-branch rebuild, "simulator probe 16/16 exact on frame 1"; AM4-141..158: "iOS Simulator probe 3/3" after each Metal Phase 3 change; AM4-148: iOS sim build free of availability warnings at the 16.3 target. | SIM |
| iOS device | "**BUILD ONLY** — Final-linked `.app` for `iphoneos` (rebuilt at `49bdf63b8`: Mach-O arm64, platform 2, minos 16.3, system frameworks only) — No physical iPhone, signing identity or Apple account available" (`apple-platforms.md:217`); AM4-159: iOS device apps compile and link at `a1c46e534`. | BUILD-ONLY |
| Physical device | **None.** No physical iPhone/iPad run, no device pixels, real touch, audio, storage, background/resume or performance (`apple-platforms.md:45-48`, `:333-334`; `metal-renderer.md:14`). | — |
| Renderers allowed on iOS | `CNA_APPLE_IOS_RENDERERS` = **`SDL_RENDERER`, `METAL`** (`cmake/ApplePlatform.cmake:247-248`); SDL_GPU, OPENGLES3, HEADLESS/SOFTWARE/STUB refused by default; everything else refused; `CNA_APPLE_ALLOW_UNVALIDATED_RENDERER=ON` downgrades to a warning (`apple-platforms.md:169-181`). | SOURCE |
| Documented iOS configure | `-DCMAKE_TOOLCHAIN_FILE=cmake/toolchains/ios.cmake -DCNA_GRAPHICS_RENDERER=SDL_RENDERER|METAL -DCNA_ENABLE_NET=OFF -DCNA_BUILD_TESTS=OFF -DCNA_BUILD_EXAMPLES=OFF` (+ `-DCNA_IOS_SIMULATOR=ON` for the simulator) — `CNA_ENABLE_NET=OFF` is required (no libcurl in the iOS SDK) (AM4-105; `apple-platforms.md:99-120`). Relative toolchain-file re-configure fixed (AM4-105). | DOC + M4-LOCAL (reproduced) |
| Known iOS issue found, not fixed | With `PresentationMode::NativeBackBuffer` on iOS the device viewport is the native surface (2622x1206) while PresentationParameters stays 800x480, and readback later reads zeros (AM4-037). | SIM |
| SDL_RENDERER on iOS | Allowed; pixel probe is METAL-only because SDL_RENDERER refuses exact readback through the letterbox scaling a phone needs (`apple-platforms.md:42-43`; apple-ci.yml comment). | DOC |
| CI | `apple-ci.yml` iOS matrix has 4 legs (SDL_RENDERER/METAL × device/simulator); METAL simulator leg runs the pixel probe. Green hosted result after the campaign: **not recorded**. | CI-HOSTED (configured) |
| C ABI on iOS | Not exercised (`docs/c-api/COMPATIBILITY.md`, AM4-214). | DOC |
| Internal doc staleness | `apple-platforms.md:9-10` top table still says "iOS simulator — Experimental; one-frame app smoke run" and `:171` says SDL_RENDERER "is the only renderer built and final-linked by Apple CI" — both superseded by `:175`, `:216` and AM4-037/120. | — |

---

## 4. C API on macOS — see R3 (`R3-c-api-cna-net.md`). Summary: real Mach-O `libcna_c_api.dylib` exporting exactly the 3,210 `_cna_*` names (AM4-209), `@loader_path` rpath + ABI-derived Mach-O versions + SDL3 dylibs installed (AM4-210), `CApi_InstalledConsumer` on macOS (AM4-211), Mach-O ABI tooling (AM4-212), static archive via `ld -r -all_load` + `nmedit -s` (AM4-213), docs retire "no macOS toolchain" (AM4-214). C API 119/119 in SOFTWARE and SDL_RENDERER trees. **No CI job builds the C API on macOS** (`apple-platforms.md:218`).

## 5. Ecosystem projects in the campaign (sibling SHAs as recorded by the plan; not present locally)

| Project | Tasks | What was done / measured | Evidence type & boundary | Recorded sibling SHA(s) |
|---|---|---|---|---|
| **sharp-runtime** | AM4-001, AM4-009..021 (its own sequence; see `docs/Platform-macOS.md` in sharp-runtime), AM4-100/101/103/104, AM4-112..114, AM4-126..129, AM4-245, AM4-253 | Apple CSPRNG (`arc4random_buf`), `from_chars` shim, Clang header conformance, libc++ Regex, Darwin `ProcessPath`, pre-1900 zones, `Ping`, `NetworkInterface`, **kqueue `FileSystemWatcher` for Darwin** (labelled "AM4-055" in sharp-runtime — collides with CNA's AM4-055), hardening after the audit. **"Suite on M4 at `62952ef5`: 18,084 run, 18,059 passed, 0 failed, 25 skipped (independent rerun, 2026-10-08)."** Later (Phase 4 head): **18,127/18,127, 25 skip** (native float `from_chars` absent below macOS 26 x17, `/rv` XNA sample fixtures x3, live SOAP x2, x86-64 layout pin, ...) — PASS WITH KNOWN LIMITATION (`apple-platforms.md:203`; AM4-208). AM4-253: macOS Core_Base 6220 passed. | M4-LOCAL, TEST-SUITE (standalone sharp-runtime suite). The two figures are different measurements: 18,084 at `62952ef5`, 18,127 at the Phase 4 head. | `62952ef5` (kqueue watcher, last of AM4-009..021 series), `3b27f13b` (AM4-245), `59454257` (AM4-253); cna-template CI pins sharp-runtime `59454257e` (AM4-291) |
| **house-simulator** | AM4-054, 199, 201..204, 232, 233, 235..237, 243, 246, 258, 265..267, 276, 277, **301..303** | macOS port fixes (from_chars, FMA, EGL-free perf tests, content tool lookup, Blender lookup); Phase 4: **1,830/1,832, 22 skip** with world content built on the Mac (OPENGL33 tree; two open upstream questions) (`apple-platforms.md:221`). **AM4-303 (CNA commit `bccf1528c`): METAL identity added to `CNAHOUSE_RENDERER`, Tier E mapped to `CNA_METAL_COMPILED_EFFECTS` (forced on), `metal` preset; Mac mini M4 Release: walk scene at the 66.7 fps cap with Tier S+E, matches the OPENGL33 frame (0.9 % of pixels differ by >16, all at the ceiling lamp z-fight); suite 1,822/1,832 before AM4-301/302.** No CNA change was needed. AM4-301/302: Release-only test fixes. | M4-LOCAL (OPENGL33 suite; METAL Release run + frame comparison, PIXEL); M4-LOCKED for Phase 4. CI fixes (AM4-232..277) are CI-HOSTED config. | `c21f3273` (199), `0dd0aba3` (201), `3a32efd5` (202), `668ae237` (203), `fc3618c9` (204), `3b181823` (301), `b79ae985` (302), `d24265ab` (303); CI: `a9c91288`, `94a5ee84`, `319350de`, `3cb34045`, `1d9c9dbb`, `f224641f`, `210633be`, `ae6d9f26`, `78ce1153`, `ecb8d250`, `dfac7a8a`, `107b5bdb`, `2bcfb639`, `22ee2a0e`, `35b7db7b` |
| **cna-gamer-services-server** | AM4-071, AM4-178 | Boost 1.92 from Homebrew; Clang `-Werror` and Linux-only `prlimit(1)` fixes; with Homebrew curl 8.22: 37/46 pass, 7 skip (Linux namespaces/slirp4netns), 2 fail on 127/8 aliases (AM4-071) → AM4-178: those two skip (exit 77) where 127.0.0.2 is not routed. Phase 4: **46/46, 9 skip** with CNA client harnesses from a Homebrew-curl tree (`apple-platforms.md:223`). Against system libcurl 8.7.1 the relay/event channel refuse by name and 10 CNA-driven tests fail. | M4-LOCAL, TEST-SUITE; harness-driven, loopback only | `develop` fast-forwarded to `4ab12fd` first (present locally); `f74f42e` (AM4-178) |
| **cna-car-simulator** | AM4-076, AM4-170 | Builds and runs on macOS/Metal (chase view, night cockpit, rain, headlights, instrument-cluster and mirror render targets; screenshots on the campaign HDD); cockpit self-sampling bug fixed with a regression smoke; seeded traffic made portable across libc++/libstdc++ (`CarSim::Core::Random`); unit suite timeout 900 s; Phase 4: **7/7** CTest entries (Metal, Debug). | M4-LOCAL (visual run on Metal; TEST-SUITE) | `523b93b` (AM4-170); AM4-076 records no SHA |
| **cna-samples** | AM4-078, 079, 080, 081 (samples as fixtures), AM4-169, AM4-182 | Yacht adds `GamerServicesComponent` (passes on METAL, OPENGL33, SDL_GPU, WEBGPU, FNA3D); LensFlare on SDL_GPU/FNA3D classified `RENDERER_UNSUPPORTED (refused=OcclusionQuery)`. Phase 4 matrix: **453 automated passes** over METAL, OPENGL33, SDL_GPU, WEBGPU, FNA3D (Release multi-renderer tree); METAL 91/91, OPENGL33 91/91, WEBGPU 91/91, SDL_GPU 90/91, FNA3D 90/91. | M4-LOCKED, automated renderer matrix (per-sample `AUTOMATED_PASS`) | `d21c9ff` (169), `65fa2cd` (182) |
| **cna-examples** | (matrix row) | ctest 3/3; **248/248 demos render on Metal**; Net demos fixed in cna-examples `ede3473` (`apple-platforms.md:219`). | M4-LOCAL | `ede3473` |
| **cna-template** | AM4-249, 250, 251, 261, 274, **291**, 294, 297 (CNA fix), **298**, 299 (CNA fix) | CI repair: X11/Wayland dev headers on Linux jobs (249); Windows job blocked on old CNA pin (250, owner); setup-android v4 (251); AGP 8.7 GString args (261); release-signing refusal on tasks (274); **AM4-291 (owner decision 2026-10-09): `renderers.json` keeps exactly CNA's 14 public renderer identities, read from `cmake/RendererIdentities.cmake`; CI pins CNA `88abe456e`, sharp-runtime `59454257e`, easy-gl `1edf4c1a`, meta-gl `3f08607a` from `libcna`; web matrix `[WEBGL2]`**; deps (294); Emscripten exception ABI and `CNA::EmscriptenAsyncify` (298). Linux x5 green (run 37944973581); structure gate green (37943767525); Android/Windows needed CNA fixes AM4-297/299/304/305. | CI-HOSTED (template repo CI) + local Emscripten build on the M4 (AM4-298); **not a macOS build of the template** | `be51492` (249), `795314c`/`10c16b4` (250; `ad66016` reverted by `a69e038`), `0e6f800` (251), `729f518` (261), `9d0e86e` (274), `132bc33` (291), `8db770c` (294), `731b2d3` (298) |
| **meta-gl** | AM4-248, AM4-252 | `METAGL_API` removed from 49 inline call expressions (shared build); installed-package test PATH on Windows; all four meta-gl jobs pass. | CI-HOSTED | `37bc02a` (248, new branch `apple/m4-stabilization`), `02bdad8`, `3f08607` (252) |
| **cna-gltf-viewer** | AM4-242 | `--capture` asks for HiDef; CNA's `gltf-renderer-stride-ci` pins it. | CI-HOSTED; syntax-checked on the M4 | `6061bff` |
| **cna-dotnet / cna-dotnet-template / cna-dotnet-samples** | AM4-215..231, 256, 257, 262, 288 | See R3. | M4-LOCAL (osx-arm64) + CI-HOSTED fixes | see R3 |
| **easy-gl** | AM4-291 pin only | cna-template CI pins `1edf4c1a` | — | `1edf4c1a` |

---

## 6. Previously true caveats that are STALE at `c1c316b9`

| Caveat (as found on the site or in older CNA docs) | Status at TARGET | Citation |
|---|---|---|
| "macOS is configured/built in CI but not run" / "no native macOS test run" | **Stale.** Every renderer tree ran in full on a physical Mac mini M4 (7 trees, 10,875–11,916 tests each, 0 failures). CI on macOS is a separate, narrower matter. | AM4-208; `apple-platforms.md:201-224` |
| "METAL is only configured / compile-only / not verified / no representative 3D pixels" | **Stale.** METAL full tree 11,015/11,015; `-L Metal` 261/261 with validation layers incl. 101 shared pixel fixtures and 146 oracles; Release 261/261; cna-samples 91/91; 248 cna-examples demos. Verdict SUPPORTED (not primary-production). | AM4-159, AM4-156; `apple-platforms.md:205` |
| "METAL refuses MRT / custom effects / occlusion queries / instancing / multi-stream / backbuffer readback / MSAA / DXT / float formats / compiled effects" | **Stale.** All implemented (table §2.4). Compiled effects need `CNA_METAL_COMPILED_EFFECTS=ON`. | AM4-025, 038, 077, 097, 141..148 |
| "METAL samples KHR_materials_specular factors only" | **Stale** (both specular textures sampled). | AM4-085 |
| "METAL is macOS-only" | **Stale.** iOS/iPadOS added (Simulator-evidenced; device build-only). | AM4-037; `metal-renderer.md:12-14` |
| "iOS has only a one-frame smoke / link with no pixel evidence" | **Stale for the Simulator.** `cna_ios_pixel_probe` exact on frame 1 + 10 frames in 8 of 8 launches (iPhone 17 Simulator). Still **no physical device**. | AM4-120; `apple-platforms.md:216-217` |
| "Only SDL_RENDERER is allowed on iOS" | **Stale.** `SDL_RENDERER` and `METAL`. | `cmake/ApplePlatform.cmake:247-248` |
| "The C API has no macOS toolchain / untried on macOS / ELF-only package" | **Stale.** Mach-O dylib + static archive, installed-consumer test on macOS; 119/119 C API tests. | AM4-209..214 |
| "CNA.NET has not run on macOS / osx-arm64 pending" | **Stale.** osx-arm64 local evidence: builds, managed suites, package acceptance, template, 84 samples smoke-run on SOFTWARE and METAL. Still local evidence, not a shipping claim; no CI leg, signing or notarization. | AM4-215..231 |
| "C ABI 0.44.0" / "CNA.NET targets 0.44.0" | **Stale.** C ABI 0.46.0; cna-dotnet admitted 0.46.0 (0.45.0 never admitted). | `abi.h`; AM4-217 |
| "WebGPU on macOS: 148/148" or any pre-AM4-088 WebGPU macOS claim | **Was never true as a GPU run** (skips counted as passes). Current: full tree 10,968/10,968. | AM4-052 correction, AM4-088 |
| "SDL_GPU's Metal driver route has no native execution evidence" | **Stale** (local M4: 10,962/10,962). Still no CI job selects SDL_GPU on macOS. | AM4-208 |
| "Five CI workflows pin stale sharp-runtime commits" | **Stale (fixed)**. | AM4-234 |
| "ModuleLinkClosure_* gates skip under Ninja" | **Stale (fixed)**. | AM4-167 |
| "Metal CI on macos-14 / Xcode 15.4" | **Stale.** macos-26 (Xcode 26). | AM4-255; `metal-macos-ci.yml` |
| "sharp-runtime FileSystemWatcher has no macOS backend" / "uses FSEvents" | **Stale/wrong.** kqueue backend. | plan "sharp-runtime" section; AM4-105, AM4-110 |
| "FNA3D on macOS uses OpenGL" | **Stale for the tested default**: Metal driver on Apple; legacy GL 2.1 still selectable. | AM4-051 |

## 7. Limitations still recorded at `c1c316b9`

1. **No physical iPhone/iPad** ran anything; iOS device = final-linked build only (no signing identity/Apple account). No device pixels, real touch, audio, storage, background/resume, performance (`apple-platforms.md:45-48`, `:217`, `:333-334`).
2. **On-screen presentation never observed** on the M4 (console locked; windows occluded); `PresentInterval` pacing unmeasured; `PresentInterval.Two` presents as `One` on METAL (AM4-139 parked) (AM4-159; `metal-renderer.md:71-74`).
3. **No soak run** bounding Metal caches (AM4-159).
4. **METAL compiled effects default OFF** (`CNA_METAL_COMPILED_EFFECTS`).
5. METAL custom effects are SpriteBatch-scoped MSL only; backbuffer BGRA8; LOD bias needs macOS/iOS 26; MSAA RT2D `PreserveContents` `SetData` loss; shared-layer gaps; CNAEXT compute/indirect/array slices absent (§2.4).
6. **No Intel Mac run** (x86_64/universal configured, unverified; `apple-platforms.md:8`, `:335`); packed 16-bit formats refused on non-Apple GPUs.
7. **Hosted CI**: no green macOS run recorded after the campaign's last CI changes; hosted Metal GPU is a paravirtual device that cannot run Metal shader validation (AM4-279); the last documented green Apple workflow run is pre-campaign (macOS 14, `be4ea08bc`). **No CI job builds the C API on macOS** (`apple-platforms.md:218`); **CNA.NET has no macOS CI leg** apart from the osx-x64 ABI-header job (AM4-229, AM4-288).
8. System libcurl 8.7.1 → relay refused; Homebrew curl needed for online play on macOS (AM4-044, AM4-071, AM4-123).
9. Homebrew FFmpeg raises the effective deployment floor (AM4-130).
10. SDL_GPU and FNA3D (Metal drivers): no occlusion queries; LOD bias ignored; FNA3D float render targets not promoted (AM4-182, AM4-189, AM4-191).
11. WEBGPU on Metal: partial `MultiSampleMask` refused; occlusion boolean (AM4-091, AM4-131).
12. OPENGL33 on Apple GL: normalized DepthBias case skipped (float32 depth) (AM4-171).
13. iOS: `CNA_ENABLE_NET=OFF` required; FFmpeg disabled; no safe-area insets; no `.ipa`/App Store packaging; no Mac Catalyst/tvOS/watchOS/visionOS (`apple-platforms.md:117-119`, `:155-159`, `:336-339`); `NativeBackBuffer` viewport/readback mismatch on iOS (AM4-037).
14. house-simulator: two open tests needing a Linux reference run (`apple-platforms.md:221`).
15. Environment-dependent skips on macOS: Doxygen 1.9.x needed for C API coverage gates (AM4-160), shaderc absent (AM4-168), Pillow (AM4-059), fxc absent (AM4-048).
16. CNA.NET: SDL_RENDERER Integration suite still fails 239/261 (AM4-231 "Open"); the binding qualifies on SOFTWARE and METAL only; full graphics capture probe stops on a Reach refusal (AM4-225, not macOS-specific).

## 8. Claims that must NOT be made

- "Validated on iPhone/iPad", "runs on iPhone", "iOS device support", "tested on iOS hardware" — there was **no physical device**. Say "iOS Simulator (iPhone 17 profile) pixel probe; device build final-linked, not run".
- "iOS is only configured" / "iOS has no pixel evidence" — also wrong: Simulator execution with pixel readback exists.
- "CNA fully supports every Mac" / "Intel Macs supported" / "production-ready on macOS" / "METAL is production-grade" — the verdict is SUPPORTED, explicitly *not primary-production*; no Intel Mac was run.
- "Compiled XNA effects work on METAL out of the box" — they need `CNA_METAL_COMPILED_EFFECTS=ON`.
- "Metal custom shaders for 3D" — custom MSL effects are SpriteBatch-only.
- "macOS CI is green" / "CI verifies Metal pixels on every push" — no post-campaign green hosted run is recorded; the 518/518 and full-tree numbers are the **local M4** runs.
- "Online multiplayer works on macOS out of the box" — needs a libcurl with WebSockets (Homebrew curl); the SDK libcurl refuses the relay by name.
- "WebGPU passed 148/148 on macOS" (that was skips) or any pre-AM4-088 WebGPU macOS number.
- "On-screen presentation / vsync pacing verified on macOS" — never observed (locked console).
- "CNA.NET ships for macOS" / "signed/notarized" / "CNA.NET macOS CI" — local evidence only; no CI leg, signing or notarization (AM4-229).
- "CNA.NET runs on Windows" (no Windows run in this campaign; pre-campaign matrix lists win-x64 pending).
- "The C API is built on macOS in CI" — "No CI job builds the C API on macOS yet" (`apple-platforms.md:218`).
- "Vulkan/MoltenVK on macOS" — out of scope, not tested.
- "CNA has a Cocoa/AppKit/UIKit platform backend" — Apple is reached through SDL3 (`CNA_PLATFORM=SDL3`).
- Do not cite the two all-zero iOS launches as "unexplained" or "flaky" — AM4-120 found and fixed the cause (SDL UIKit view-frame swap); cite the 8 of 8 result.
- Do not mention retired renderer identities, retired direct platforms, or that they were removed (public-content policy).

## 9. Additional facts verified during the page survey (CNA `c1c316b9`)

| Fact | Citation |
|---|---|
| METAL capability policy: `MetalSupportsCapability` returns true for ThreeD, DepthStencilBuffer, MultipleRenderTargets (AM4-097), AnisotropicFiltering, WireFrame, OcclusionQuery (AM4-038), CustomEffects (AM4-077, SpriteBatch-scoped MSL), Texture3D, MultiStreamVertexInput and Instancing (AM4-143), StencilBuffer, AdditiveBlending; MultiSampleAntiAliasing is answered per device by `MetalRenderer::SupportsCapability` (AM4-141); CompiledEffects true only with `CNA_METAL_COMPILED_EFFECTS=ON`; ComputeShaders and IndirectDraw false. | `modules/renderers/metal/include/CNA/Internal/Renderers/Metal/MetalPolicy.hpp:165-184`; `metal-renderer.md:111-126` |
| The Metal renderer adds its own `CAMetalLayer`-backed view to the native window (no `SDL_Metal_CreateView` call in `modules/renderers/metal`). | `metal-renderer.md:5-10`; `git grep SDL_Metal_CreateView c1c316b9 -- modules/renderers/metal` = no hit |
| `CNA_BUILD_APPLE_SMOKE_APP` also builds `cna_ios_pixel_probe` / `cna_macos_pixel_probe`. | `cmake/AppleSmoke.cmake:25-35` (survey agent) |
| **The C API cannot be configured for iOS today**: `CNA_BUILD_C_API=ON` requires `CNA_ENABLE_NET=ON` (FATAL_ERROR), and iOS requires `CNA_ENABLE_NET=OFF`. | `CMakeLists.txt:187-192`; `apple-platforms.md:117-119` |
| macOS build prerequisites at TARGET: nlohmann_json ≥ 3.11 is required for gamer services (`cmake/HeaderOnlyJson.cmake`); libcurl ≥ 7.85 on desktop (GS-003a); Xcode 15.4 (Apple clang 15) is too old (no `std::jthread`/`std::stop_token`), CI uses Xcode 26 (`macos-26`), the campaign Xcode 27. | AM4-238, AM4-247, AM4-255 |
| Compiled-effect options at TARGET: 8 default-OFF options (`CNA_EASYGL_`, `_VULKAN_`, `_WEBGPU_`, `_SOFTWARE_`, `_DIRECTX11_`, `_DIRECTX9_`, `_METAL_`, `_SDL_GPU_COMPILED_EFFECTS`) + FNA3D always → 9 families, 11 of the 14 identities. | `cmake/RendererSelection.cmake:222-382` |
| CNA-internal stale wording not to copy: `cmake/RendererSelection.cmake:35` option docstring "Enable native Apple Metal graphics renderer (macOS only)" (the host gate at `:136-144` admits macOS and iOS); `cmake/RendererCombinations.cmake:25,50-51` partition still named/labelled "macOS"; `docs/gamer-services-known-limitations.md:80` (row 28 "Windows and macOS clients and server hosts not run"), `:581-583` ("no macOS host exists"), `:662` — superseded by the plan: on the M4 the full trees (incl. GamerServices/Net suites), Guide/gamer-services UI tests on Metal 130/130 (AM4-086/090), 304 networking cases (AM4-200) and the server suite with CNA's macOS client harnesses 46/46 (AM4-208) ran. | `git show c1c316b9:<path>` |
| `plans/plan_gltf.md:140` records the METAL specular-texture blocker closed (2026-10-08, AM4-085) while the GLTF robustness tally at `:142` still reads "9 of 12" (not re-assessed). | survey agent B; `plan_gltf.md` |
| `RRC-027` (`71a0e7313`): `modules/renderers/CMakeLists.txt:137-151` enters `common/d3d` and builds METAL on renderer-set membership, not only as the default (fixes the old CNA-BUG-190). | survey agent B; commit message |
