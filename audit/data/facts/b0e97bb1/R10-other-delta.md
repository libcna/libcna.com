# R10 — "Everything else" in CNA O..T, mapped to libcna.com

Pins: **O** = `009d40f5` (2026-09-24), **T** = `b0e97bb1` (2026-10-04, branch `next`). O..T = 456 commits, 232 first-parent.
I read the CNA repo only through git objects (`git show/grep/diff/log` at O and T) and did not build or run anything.
Classes used: **[src]** source fact · **[build]** build-system fact · **[rt]** runtime result as a commit message or doc in the repo records it (I did not re-run it) · **[plat]** platform-qualified · **[compat]** compatibility result against XNA or FNA · **[plan]** future or open item.
Out of scope here because other agents cover them: renderer removals, SDL2, platform lists, CNAEXT retirement, C ABI versions, CNA.NET, samples, bindings, GamerServices/avatars/networking, known-issue dispositions. I mention them only where they change a number I own (tests and CI).

---

## Executive summary

1. **GL context and threading changed in substance (EasyGL only).** The game thread now holds the GL context for all of Initialize, BeginRun, every Tick (Update and Draw) and EndRun (KF-16/KF-2, `a033a9184`). Before, it held it only for BeginDraw..EndDraw. Texture, buffer and render-target constructors, `SetData`, `GetData` and `Dispose` now take the context lease on **any** thread (KF-1, `00b9c9898`). The device resource registry is now mutex-guarded (KF-1a). A known **deadlock** is documented: the game thread waiting inside LoadContent/Update/Draw for a worker that creates GPU resources. libcna.com tutorials 77 and 78 ("never call any CNA rendering API from a worker", "ContentManager::Load: do not call from background threads") are now stale or over-strict for EasyGL.
2. **Several devices on several threads** (BINDFIX-050, `5b4edd6cc`): creating and destroying devices concurrently from different threads is now safe and documented in `graphics_device.h` [src, rt 240/240 reproducer runs].
3. **New opt-in keyboard emulation, three switches, all off by default:** `GamePad::setKeyboardEmulationEnabledEXT(true)` (INPUT-EMU-002, `df2deb690`) gives player one a software pad (WASD, arrows, TFGH, KLJI, Q/E, Z/C, Shift, Enter/Escape). INPUT-EMU-001 (`31a560af9`) adds `Accelerometer::setKeyboardEmulationEnabledEXT` and `GameWindow::setKeyboardOrientationEmulationEnabledEXT`. **None of the three appears anywhere on libcna.com.**
4. **A relative content root is now resolved under `TitleLocation.Path`** (or the platform base path), falling back to the working directory (CBIND-140, `9976f4909`). About 20 site statements say "relative to the working directory" and are now stale. Android is unchanged.
5. **Browser saves now persist** (SAMPLE-070 `8a67da536`, SAMPLE-071 `c5986156d`). The storage module links IDBFS and mounts `/cna-storage` (StorageDevice) and `/save` (IsolatedStorage) with `autoPersist`, restoring both before `main()`. Threaded builds keep WasmFS by default, so persistence there needs the **new option `CNA_EMSCRIPTEN_USE_WASMFS=OFF`**. Without it StorageDevice throws `StorageDeviceNotConnectedException` ("Persistent browser storage is unavailable."). About 18 site statements say "no IDBFS / saves lost on reload" and are now **false**.
6. **Android runtime fixes, recorded on the emulator:** lifecycle events are now actually delivered (BL-20; before this they were mapped but never produced). On Android `IsActive` follows the lifecycle instead of focus (BL-21). `.cnb` loads from inside the APK (BL-19). Back is seen as Escape and as player one's Back (CBIND-137). Portrait games run in portrait (CBIND-138). Models draw whole on the emulator (CBIND-139). `CNA_PLATFORM_<X>` is exported so SDL_main is found (BL-13). The C API builds with the NDK alone (CBIND-136). There is still **no Android workflow and no retained artifact**.
7. **Compiled effects on GLES/WebGL:** 7 new pinned MojoShader patches (117 → 124 files). The patches cover SM3 point-size scalar writes (FX-140), mixed abs/plain constants (FX-141), SM1 colour input not centroid (FX-142), `sampler3D` precision on ES 3 (FX-143), highp float sampling on ES 3 (FX-145), emulated vertex `TEXLDL` LOD bias on ES 3 (FX-146), plus one D3D11 lifetime patch. The record is 686/686 `EasyGLCompiledEffect*` on Mesa GLES 3.2 [rt]. Two stock-effect behaviour changes also landed: CBIND-156 (a draw samples the device's texture slot) and Task 1120 (a stock effect passed to `SpriteBatch.Begin` places sprites by its own matrices).
8. **XNA-fidelity exceptions and game-loop fixes:**
   - Game loop: `Tick` runs no Update after `Exit()` (KILLER-1). Timing setters throw `ArgumentOutOfRangeException` (KF-15). `GameComponentCollection` throws XNA's exception types (KF-14). Device-creation failure in `Game`'s constructor becomes `NoSuitableGraphicsDeviceException` (CBIND-144).
   - Content: `ContentLoadException` now derives from `System::Exception` (KF-13), and a wrong-type XNB is a `ContentLoadException`, not `std::bad_any_cast` (KF-9).
   - Audio: arguments are validated as in XNA (KF-12). Sample size and duration follow XNA's arithmetic (KF-7/8). A zero-channel WAVE no longer kills the process (KF-17). XNA-built sounds with content rates such as 48,056 Hz now load (CBIND-146).
   - Many site pages still describe the FNA-style or `std::` behaviour.
9. **Input fidelity:**
   - Mouse: the SDL3 mouse reads the desktop pointer minus the window position on x11, windows and cocoa (CBIND-148). The browser emulates `Mouse.SetPosition` virtually (CSX-145).
   - Window: `ClientBounds` now carries the desktop position (CBIND-147) and, when fullscreen, the back-buffer size (CBIND-157).
   - Touch: touch-synthesised mouse events no longer re-enter the mouse→touch emulation (SAMPLE-046), and the emulated touch is clamped to the display (SAMPLE-067).
10. **XACT build:** `BuildXact` now drives Microsoft's real `XactBld3` with `/WINDOWS` or `/XBOX360` and Wine path mapping (XACTBUILD-001/SAMPLE-122, `db68149e3`). It is configured by `CNA_XACTBLD`, `CNA_XACTBLD_LAUNCHER` or `SetXactCompilerEXT`, and was qualified against XactBld3 9.28.1886.0 under Wine on two projects [rt]. The Xbox 360 switch is argument-tested only. libcna.com says only "BuildXact is declared".
11. **Tests and CI:**
    - Static GTest definitions fell 12,610 → 12,021 (−589). That is **−1,190 definitions in 105 deleted files**: 874 in `modules/graphics-ext/tests` (86 files, the engine layer), 100 svg-dom, 98 opengl4 (9 files), 60 html-dom, 25 direct2d, 17 gamer-services, 15 other. It is offset by **+468 in 55 new files** (248 gamer-services, 160 net, …) and +133 in existing files.
    - Workflows fell 20 → 18 (`gdi-windows-ci.yml` and `htmldom-ci.yml` deleted) and jobs 28 → 26. Standalone `examples/**/*_test.cpp` pixel programs fell 879 → **779**.
    - Unchanged: oracle scenes (39), XNB built-in readers (61; `XnbBuiltInReaders.cpp` untouched), and the committed XNA surface report (331/331 types, 3,627/3,627 members).
12. **Version:** still `0.1.0` plus `alpha.1` (`CMakeLists.txt:3,12`). There is no new tag (`git tag --contains O` is empty). T is **3,333 commits after alpha.1** (945 first-parent, 65 merges); `git describe` gives `v0.1.0-alpha.1-3333-gb0e97bb1b`. `b0e97bb1b` only repoints two `CHANGELOG.md` release links from `openeggbert/cna` to `libcna/cna`.
13. **CMake options:**
    - Added: `CNA_EMSCRIPTEN_USE_WASMFS` (ON), plus cache variables `CNA_ENABLE_VOICE` (AUTO/ON/OFF), `CNA_EASYGL_ROOT` and `CNA_GAMER_SERVICES_SERVER_ROOT`.
    - Removed: `CNA_RENDERER_{DIRECT2D,FREEDIRECT,GDI,HTML_DOM,OPENGL4,PORTABLEGL,SVG_DOM}`, `CNA_OPENGL4_COMPILED_EFFECTS`, `CNA_BUILD_{HTML,SVG}_DOM_HOST_TESTS`, `CNA_SDL2_{ROOT,GIT_REPOSITORY,GIT_TAG}` and `CNA_DIRECT2D_TEST_RUNTIME`.
    - Compiled-effect options went from nine to **eight**.
    - `CMakePresets.json` is unchanged.

---

## A. Delta facts (with evidence)

### A1. Threading / GL context

| ID / commit | Fact at T | Class | Evidence |
|---|---|---|---|
| KF-16, KF-2 `a033a9184` | The game thread holds the EasyGL context for **Initialize, BeginRun, every Tick (Update + Draw) and EndRun**, and releases it between frames after Tick's wait. Before, the lease covered only BeginDraw..EndDraw, so `SetRenderTarget`/`Clear` issued from Update were silently lost and a minimized `ApplyChanges` built an incomplete MSAA back buffer. | src + rt | `modules/runtime/src/Game.cpp:777-892` (`AcquireGameThreadContextLease` at 687,696,731,767,811,1160,1355; definition 1143-1148); tests `easygl_update_time_gl_work`, `easygl_msaa_backbuffer_minimized_resize` |
| KF-1, KF-1a `00b9c9898` | Constructors, `SetData`, `GetData` and `Dispose` of Texture2D, Texture3D, TextureCube, render targets, VertexBuffer and IndexBuffer take the lease on **any thread**. On the game thread inside a frame the lease is nested; on another thread it is a real lease that waits for the gap between frames. `GraphicsDevice::resources_` is now mutex-guarded (`GraphicsDevice.hpp:1488,1969` `resourcesMutex_`). **Deadlock:** a game thread that waits inside LoadContent/Update/Draw for a worker creating GPU resources (FNA and MonoGame do the same; XNA allows it). | src + rt (worker test 10/10) | `docs/opengl33-renderer.md:82-94` (T); commit body |
| Lease scope | Only EasyGL implements `AcquireThreadContextLeaseEXT`; the base returns `nullptr` (`IGraphicsRenderer.hpp:2403-2410`). OPENGL4, which libcna.com says has one, was retired (renderer agent). | src, platform-qualified | `git grep AcquireThreadContextLeaseEXT T -- modules/renderers` → easygl only (plus a vulkan test file) |
| CBIND-133 `e77ae09ed`, CBIND-131 `abd005ab8` | The lease type moved to `RendererThreadContextLease.hpp` (libc++/Emscripten compile). The lease state now lives on the lease control, so it survives exit-time static destruction. | src | commits |
| BINDFIX-050 `5b4edd6cc` | Several threads may create and destroy devices at once. Five process-wide paths were guarded: shared sampler identities, SDL window/context teardown, adapter cache, display-mode queries, and serialised device construction. | src + rt (240/240 reproducer; `CApi_ConcurrentDeviceCreationSmoke`) | `modules/c-api/include/CNA/C/graphics_device.h` (T) |
| BINDFIX-041 `0f7166cd8` | At process exit, objects created by another, already-ended thread are left to the OS instead of aborting (JVM-host case). | src | commit |
| KF-6 `10daf178a`, `64b02d468`, `1dbc94f28` | The EasyGL back buffer is now an **offscreen FBO** wherever the profile can blit: GL 3.3, GLES 3, and WebGL 2 off the web. `GetBackBufferData` reads it at the logical size. ES 2 and the web canvas still use framebuffer 0. `GraphicsDevice::Reset` takes the lease. | src | `docs/opengl33-renderer.md:95-105` (T) |
| Web, threaded (SAMPLE-071, CBIND-151 `cde2251fa`) | Threaded builds: WasmFS by default, `-sOFFSCREEN_FRAMEBUFFER`, and the lease excludes loads and frames. CBIND-151 (C ABI/.NET route): SDL patch `0004` commits proxied frames from a worker, the threaded `cna_c_api_wasm` links 64 MB initial memory, the `WEBGL_polygon_mode` probe is tolerated on a worker, and StorageDevice asks the page thread. **No CNA ctest drives a threaded browser build**; the evidence is headless-Chromium runs. | src + rt (Chromium, commit-recorded) | `docs/web-emscripten-graphics-limitations.md:35-75` (T); `plans/plan_binding.md` CBIND-151 row |

### A2. Input

| ID / commit | Fact at T | Class | Evidence |
|---|---|---|---|
| INPUT-EMU-002 `df2deb690` (2026-10-03) | **`GamePad::setKeyboardEmulationEnabledEXT(bool)` / `getKeyboardEmulationEnabledEXT()`** (CNAEXT; process-wide; off by default). It adds a connected software pad to **PlayerIndex.One only**, with or without a physical pad. Layout: left stick WASD; right stick arrows; D-pad T/F/G/H; A/B/X/Y = K/L/J/I; LB/RB = Q/E; LT/RT = Z/C (0 or 1); stick clicks = Left/Right Shift; Start/Back = Enter/Escape. Buttons are OR'd with the physical pad's, and a nonzero keyboard axis wins. Dead zones still apply. Capabilities report the mapped controls. Not emulated: BigButton, vibration, sensors, identity. Keys are **not consumed** from `Keyboard.GetState`. Unfocused input is neutral, and Guide interplay is handled. There is no C ABI or Sharp Runtime change. | src + rt (Input 560/560, runtime 33/33, SAMPLE-085 native + WEBGL2 gates) | `modules/input/include/Microsoft/Xna/Framework/Input/GamePad.hpp:44,50`; `docs/keyboard-device-emulation.md:60-101`; AUDIT.md head |
| INPUT-EMU-001 `31a560af9` (2026-09-28; merged via `9373ca58b`) | `Accelerometer::setKeyboardEmulationEnabledEXT(true)` (process-wide; arrows tilt ±1 g; `IsSupported` becomes true on **desktop and Browser** without hardware). `getWindowProperty().setKeyboardOrientationEmulationEnabledEXT(true)` (per window; Up=Portrait, Left=LandscapeLeft, Right=LandscapeRight; honours `SupportedOrientations`). Both off by default. | src + rt (runtime 43/43, sensors 91 + 4 skips, input 83/83; OPENGLES3/WEBGL2 sample) | `docs/keyboard-device-emulation.md:7-58`; `Accelerometer.hpp:168,175` |
| GamePad EXT count | GamePad CNAEXT static **functions**: 19 at O → **21** at T. My count excludes the 3 constexpr constants. | src | `git show {O,T}:…/GamePad.hpp` |
| CBIND-148 `6e273cd89` | The SDL3 `Mouse.GetState` reads `SDL_GetGlobalMouseState` minus the window position on the **x11, windows and cocoa** video drivers. This matches XNA's `GetCursorPos` and FNA, and the result is not clamped to the window edge. Other drivers keep the window-relative state. | src [plat] | `modules/platform/src/Sdl3/Sdl3InputServices.cpp` (`ReportsTheDesktopPointer`) |
| CSX-145 `d80111333` | Under Emscripten, `Mouse.SetPosition` is emulated: the requested position is anchored virtually and later physical deltas are applied (`BrowserMouseWarp`). This fixes mouse-look games such as TerrainDemo. | src + rt (headless Chromium) | `modules/platform/src/Sdl3/BrowserMouseWarp.hpp`; `handoff.md` §19 |
| CBIND-147 `e6f9d5384` | `GameWindow.ClientBounds` X/Y = the client area's **desktop position**. A platform without desktop placement (e.g. Wayland) still answers 0. | src [compat XNA+FNA] | `modules/runtime/src/GameWindow.cpp`; `runtime_window.h` |
| CBIND-157 `75b55659c` | A **fullscreen** window's `ClientBounds` size = the back buffer's logical size (XNA's mode switch), keeping the platform position. | src + rt (Speedy Blupi on Xvfb) | `GameWindowTest.FullscreenClientBoundsAreTheBackBuffersModeAsXnaSetsIt` |
| SAMPLE-046 `c74569ae5` | Mouse events that SDL synthesised from touch no longer feed CNA's mouse→touch emulation, which preserves real pinch input (`PlatformEvent::synthesizedFromTouch`). | src | `SdlInputBridge.cpp`, `PlatformEvent.hpp` |
| SAMPLE-067 `8c917a6d7` | The emulated touch position is clamped to the display; `Mouse.GetState` is unchanged. | src | `SdlInputBridge.cpp:432-460` |
| CBIND-137 `747b02493` | Android Back is latched: the next keyboard update shows Escape once, and for a game that asked for pads the next gamepad update shows player one's Back once (MonoGame-like). | src [plat Android] + host tests | `docs/input-fna-fidelity.md` (T) |

### A3. Content

| ID / commit | Fact at T | Class | Evidence |
|---|---|---|---|
| CBIND-140 `9976f4909` | On non-Android targets a relative `RootDirectory` resolves to `<TitleLocation.Path>/<root>` **if that directory exists**. When TitleLocation is undecided the platform base path is used instead. Otherwise it falls back to the path as given (the working directory). Android keeps packaged-asset paths. | src [compat XNA] | `ContentManager.cpp:507-523` (`TitleRootedDirectory`), `modules/content/src/Internal/ContentRoot.cpp`, `modules/core/src/TitlePath.cpp` |
| BL-19 `5d275f556` | Both `.cnb` tiers (by name and by literal name, in `Load<T>` and SoundEffect) read through `TryReadAssetBytes`, so Android finds `.cnb` inside the APK. The loose tier was not covered by BL-19 (I did not check it). | src + rt (House Simulator APK, emulator) | `ContentManager.hpp:503-548` |
| KF-13 `2d85a276f` | `ContentLoadException` derives from **`System::Exception`**, as in XNA and FNA. Its hiding `InnerException` field/accessor was removed. | src [compat] | `ContentLoadException.hpp` (T) |
| KF-9 `0af45cbd4` | A reader producing the wrong type, or asking for the wrong `T`, throws `ContentLoadException` naming the asset and the produced type. **No more `std::bad_any_cast`**. | src [compat XNA `BadXnbWrongType`] | `ContentReader.hpp` (`CastReadResult`) |
| CBIND-146 `51d9c84cc` | The XNB SoundEffect reader accepts XNA's content rate range (XAudio2 1,000–200,000 Hz, e.g. 48,056 Hz ADPCM). The public constructors keep 8,000–48,000 Hz. | src [compat] | `SoundEffect.hpp` private ctor; `SoundEffectContentTypeReader.cpp` |
| LRS-R28 `78b708bcb` (docs) | `.cnb` XREF names are logical names relative to the **compile-time content root**, unlike `.xnb`, whose references resolve against the referring asset. | src (doc) | `docs/cnb-format.md` XREF |
| CNA-F20 `e45faa1d7`, LRS-R29 `87db4ddc7` | `.cnj` and `.cnb` (V1 and V2) model parts that name one image share **one `Texture2D` object** (XNA-like identity). | src | `ModelResources`; `CnjModelTests.PartsNamingOneTextureShareOneTexture2D` |
| CNASTREET-SKINMETA `1d1992823` | Compiled `.cnj`/`.cnb` skinned models now fill `Model::SkinsEXT` (one skin); before, only `Tag` was set. | src | `SetCompiledModelSkinEXT` |
| CNASTREET-SKINDRAW `e9e2b5d2e` | Skinned glTF: the mesh node's transform is **ignored** (glTF 2.0 §3.7.3.2). The root prefix is now scene ancestry alone; `inverse(meshNodeWorld)` was dropped. | src [compat glTF spec] | commit; `BuildSkeleton` |
| LRS-R1 `8e2096c64` | The fallback tangent is always perpendicular to the normal. | src | commit |
| XACTBUILD-001 / SAMPLE-122 `db68149e3` | `BuildXact` invokes the real `XactBld3` with `/WINDOWS` or `/XBOX360` (an unsupported platform is refused before launch). Under Wine, paths are mapped with `winepath -w`, shared with the effect compiler (`CNA::Internal::HostProcess`). Configuration: `CNA_XACTBLD`, `CNA_XACTBLD_LAUNCHER`, `BuildXact::SetXactCompilerEXT`. Qualified: 45/45 focused cases; 2/2 genuine-SDK gates (ShipGame XACT3, Catapult XACT2 auto-imported to version 46) with **XactBld3 9.28.1886.0 under Wine/Xvfb**. **Not qualified:** authentic XACT2 binaries, XNA2 runtime, cue-exact playback, Xbox 360 output (argument contract only). | src + rt [plat Linux+Wine] | `modules/content-pipeline/src/Xna/Tasks/BuildXact.cpp:23-44,144`; `plans/plan_xact_build_invocation.md` |
| BL-17 `6824a036f` | The MojoShader patch script hashes the series in memory. An already-patched read-only FNA3D checkout (`~/deps`) now configures without writes. | build | `cmake/patches/apply-fna3d-mojoshader-patch.cmake` |

### A4. Effects / shaders

| ID / commit | Fact at T | Class | Evidence |
|---|---|---|---|
| FX-140 `1c2923efd` | SM3 point-size/fog output takes scalar writes in GLSL (resonance-game). | src + rt | patch `mojoshader-6333f74-glsl-sm3-scalar-outputs.patch` |
| FX-141 `46231e857` | SM3 programs may mix `abs` and plain constant reads (SOFTWARE-410 rule removed). | src | `…-shader-model-three-mixed-constant-absolute.patch` |
| FX-142 `fb5cb3ba2` | An SM1 pixel shader's COLOR input stays a plain varying at link time (Racing Game Kit, GLES). | src + rt | `…-glsl-sm1-color-input-not-centroid.patch` |
| FX-143 `d9d599263` | GLSL ES 3 declares `precision highp sampler3D`, so compiled effects with volume samplers build on OPENGLES3 and WEBGL2. | src + rt | `…-glsles3-sampler3d-precision.patch` |
| FX-145 `26b477686` | GLSL ES 3 `sampler2D`/`samplerCube` are highp, so float textures are sampled at 32-bit (LiSPSM shadow). | src + rt | `…-glsles3-sampler-precision.patch`; fixture `tests/fixtures/compiled-effects/variance-moments-xna4.*` |
| FX-146 `1e12bd3a0` | GLSL ES 3 **compiled vertex `TEXLDL`** adds the live vertex-sampler `MipMapLevelOfDetailBias` in generated code. Desktop keeps `GL_TEXTURE_LOD_BIAS`. Implicit, pixel and stock sampling on ES is **still not representable**. | src + rt (686/686 `EasyGLCompiledEffect*`, Mesa GLES 3.2) | `docs/sampler-state-support.md:121,131-139` (T) |
| Patch count | MojoShader patch files: 117 (O) → 124 (T). The 7th new patch is `d3d11-bound-shader-lifetime` (WIN11). | src | `git ls-tree cmake/patches` |
| CBIND-156 `6c278b21d` | Stock-effect `Apply` binds the effect's texture (null too) to the device sampler slot. A draw samples `GraphicsDevice.Textures[n]` as it is then, so a texture set **after** `Apply` is drawn (XNA). This covers BasicEffect (textured shaders), AlphaTest, DualTexture (slots 0 and 1), EnvironmentMap (0 and cube 1) and Skinned. | src [compat] + rt (LilyPath) | `Effect.hpp` `BindStockTextureInternal` |
| Task 1120 `7661f6981` | `SpriteBatch.Begin(..., stockEffect, ...)` draws through the stock effect's vertex shader as indexed quads per pass, so the effect's matrices place the sprites (XNA). | src [compat] | `SpriteBatch.cpp` |
| CBIND-149/150 `d459f42aa` `3c72165e6` | EasyGL applies the sample mask only on desktop GL ≥ 3.2 or GLES ≥ 3.1 (never WebGL 2). Texture swizzle for 1- and 2-channel render targets is applied only on GL 3.3 and GLES 3. **On WebGL the unstored channels read 0, a recorded divergence from D3D's 1.** | src [plat] | `GlProfile.hpp` `HasTextureSwizzle` |
| BINDFIX-053 `7dae9216f` | MRT draws on WebGL 2 reach both targets (EasyGL narrows the draw buffers). | src + rt | commit |
| GLES wireframe: SAMPLE-048 `251bf6c98`, SAMPLE-055 `cefe6c83b`, `96b5038de` | Without a polygon-mode API (GLES and WebGL without `WEBGL_polygon_mode`), EasyGL emulates `FillMode::WireFrame` for **two bounded stock routes**: (a) non-indexed single-stream PositionColor TriangleList, clipped, with no culling, depth, stencil, scissor, bias, MSAA or render target; (b) indexed PositionNormal (24-byte) with clipping, culling and depth test. Everything else still refuses, and **`GraphicsCapability::WireFrame` stays false**. | src + rt (sample frames vs XNA ±8 levels) | NEXT.md entries (T); `EasyGLUnsupportedWireFrameTest` |
| CCS-2 `6bd1387bf` | `DrawUserPrimitives`/`DrawUserIndexedPrimitives` with a pointer to a non-stock struct and **no declaration no longer compiles** (deleted, constrained templates). An explicit `const void*` still takes the VertexPositionColor path. | src | commit |
| CCS-1 `731120eb9` | `Clear(Target\|Stencil)` restores the stencil write mask on EasyGL. | src | commit |
| GSC-0009/0010 `6924ca040` `a1414a1b0` | EasyGL PBR: a zero normal or tangent no longer produces NaN. A double-sided back face is lit from the visible side (`uDoubleSided`). | src + rt | commits |
| LRS-R23 `39daf1ab7` | SpriteBatch draws into a bound RenderTargetCube face on EasyGL. | src + rt | commit |

### A5. Browser / WebAssembly

| ID / commit | Fact at T | Class | Evidence |
|---|---|---|---|
| SAMPLE-070 `8a67da536` | Any Emscripten build that uses the legacy FS links `-lidbfs.js` plus pre-js `WebStoragePre.js`, which mounts IDBFS at `/cna-storage` **and** `/save` (`autoPersist`) and runs `FS.syncfs(true)` before `main()`. StorageDevice root = `/cna-storage/<app>`. If the mount or restore failed, it throws `StorageDeviceNotConnectedException("Persistent browser storage is unavailable.")` instead of saving to memory. A Node runner without IndexedDB keeps process-local storage. | src + rt (Chrome reload; Firefox 600 frames; `CnaStorageTests` 14/14) | `modules/storage/CMakeLists.txt:9-18`; `modules/storage/src/WebStoragePre.js`; `StorageDevice.cpp:15-24,128-137`; NEXT.md SAMPLE-070 |
| SAMPLE-071 `c5986156d` | **New option `CNA_EMSCRIPTEN_USE_WASMFS` (default ON).** In a threaded build, WasmFS cannot link IDBFS, so persistence needs `-DCNA_EMSCRIPTEN_USE_WASMFS=OFF`. The docs warn that the legacy FS can wait on the browser main thread during background content loads (Firefox), so WasmFS stays recommended for games that load on workers. | build + src | `CMakeLists.txt:27-28`; `modules/CMakeLists.txt:266`; `docs/web-emscripten-graphics-limitations.md:46-52` |
| GamerServices local store on web | `LocalProfiles.cpp:204-209` resolves `XDG_DATA_HOME`/`HOME` paths, which are not under `/cna-storage` or `/save`, so by source reading GS local profiles still do not persist in a browser. **Not run.** Flag for the GS agent. | src (inference) | `modules/gamer-services/src/Internal/LocalProfiles.cpp:204` |
| BINDFIX-052 `17281e841` | SDL patch `0003` guards the Emscripten filedrop rmdir, so a Game outlives a standalone device on WASM. | src + rt (browser_probe 12/12) | `cmake/patches/sdl-cbe3fbe9-0003-…` |
| BINDFIX-039 `3e5d8b967`, CBIND-135 `1e7c4d323` | `cna_c_api_wasm` builds again (libc++/ADL, `override`, ENet filter link). The static C API archive builds under Emscripten using an MRI-script merge. | build | commits (bindings/C-ABI agents own these) |
| CBIND-143 `ffb82bc0d` | In single-threaded browser builds, avatar loader jobs run inline (no `std::thread`). | src | commit |
| CSX-145 | See A2 (virtual mouse warp). | | |

### A6. Android

| ID / commit | Fact at T | Class | Evidence |
|---|---|---|---|
| BL-20 `9408eba8e` | SDL3 lifecycle events (WillEnterBackground, DidEnterForeground, LowMemory, Terminating) are **now delivered** through an event watch. At O they were mapped but never produced, because `SDL_SendAppEvent` does not queue them. | src + host tests | `Sdl3Platform.cpp` |
| BL-21 `016c588bf` | On Android, `FocusLost`/`FocusGained` no longer change `IsActive`; the application lifecycle does (XNA phone behaviour). Desktop is unchanged. | src + rt (House Simulator, emulator) | `Game.cpp` |
| BL-13 `f6c4df279` | `CNA::BuildConfig` exports `CNA_PLATFORM_<X>`, so a game's `main()` built beside CNA via `add_subdirectory` gets `SDL_main` on Android. | build | `cmake/PlatformSelection.cmake` |
| CBIND-136 `552a0d8cb` | The C API configures with the NDK alone: libcurl is optional on Android (no service TLS transport, so service/relay refuse as in a browser), JSON headers come from the host, and the opus probe is skipped. | build [plat] | commit (GS/bindings agents may cite) |
| CBIND-138 `80572aa00` | A portrait game runs in portrait on Android: `SupportedOrientations` Default is resolved from the preferred back buffer, and SDL re-reads the orientation hint. | src + host tests | `GraphicsDeviceManager.cpp`, `GameWindow::resolveSupportedOrientations` |
| CBIND-139 `1dc4ce06a` | On the Android emulator (`ro.boot.qemu`), EasyGL rebases base-vertex indices on the CPU. `CNA_EASYGL_CPU_BASE_VERTEX=1` forces this anywhere. | src + rt (emulator) | `EasyGLRenderer.cpp` |
| Evidence level | There is still **no Android workflow and no Android preset**, and no APK or logcat is committed (no `.apk`, `.aab` or logcat file in the O..T diff). The runtime claims are emulator runs recorded in commit messages and plans. | — | `git diff --name-status O T` |

### A7. Audio

| ID / commit | Fact at T | Class | Evidence |
|---|---|---|---|
| KF-12 `49119a34c`, `27538ade1` | XNA validation replaces FNA's: the SoundEffect/DynamicSoundEffectInstance rate (8,000–48,000) and channels give `ArgumentOutOfRange`. A buffer, offset, count or loop region not in whole 16-bit frames (including an empty buffer) gives `ArgumentException`, for `SoundEffect` and `SubmitBuffer`. Instance `Volume`/`Pitch`/`Pan`, `MasterVolume` (0..1, NaN refused), `SpeedOfSound` (>0) and `DopplerScale` (≥0, NaN refused) give `ArgumentOutOfRange`. `IsLooped=true` on a dynamic instance gives `InvalidOperation`. Volume, Pitch and CreateInstance after Dispose give `ObjectDisposed`. **`DistanceScale` 0 becomes the smallest positive float** (it was refused); a negative value throws. `SoundEffect.Play(v,p,pan)` **still clamps pitch** and range-checks pan. | src [compat XNA IL] | `SoundEffect.cpp:470-567`; `DynamicSoundEffectInstance.cpp:91-98,384-388` |
| KF-7/8 `4874c521d` | `GetSampleDuration` and `GetSampleSizeInBytes` use XNA's arithmetic: whole frames, rounded ms, and the float factor quirk (1 s mono 44.1 kHz = **88,198 bytes / 23 ms**, where FNA gives 88,200 / 22). Dynamic instances and Microphone delegate to it. | src [compat] | commit |
| KF-17 `c63056ea4` | A RIFF WAVE with zero channels, rate or block size is refused (`NotSupportedException` from `FromStream`) instead of SIGFPE. | src | `MixerEngine.cpp` |
| CBIND-154 `23d7bad1e` | Fire-and-forget playback answers on any thread (ABI 0.43.0; C ABI agent). | src | — |
| BINDFIX-051 `9d04c6702` | Audio and shader diagnostics go through the logger sink (no direct `std::cerr`). | src | — |
| Unchanged | Microphone `GetData` still has no frame-alignment check (not touched by KF-12). | src | KF-12 file list |

### A8. Game loop / exceptions

| ID / commit | Fact at T | Class | Evidence |
|---|---|---|---|
| KILLER-1 `8dc7a7b99` | `Tick` returns at once after `Exit()`. The catch-up loop stops at the step that exited, and a quit handled in `PollEvents` prevents that frame's Update, in both fixed and variable step. The Emscripten frame loop behaves the same. This is XNA IL (FNA differs). | src [compat XNA] | `Game.cpp:777,824,892` |
| KF-15 `16a1b67d9` | `TargetElapsedTime <= 0` and `InactiveSleepTime < 0` throw `ArgumentOutOfRangeException("value")` (was `std::out_of_range`). Zero sleep is valid. | src [compat] | commit |
| KF-14 `d82c81a4e` | A duplicate component gives **ArgumentException**. A bad index to the indexer, Insert or RemoveAt gives **ArgumentOutOfRangeException**. SetItem gives **NotSupportedException**. The shared_ptr Add/Insert ownership leak on failure was fixed. | src [compat] | commit |
| CBIND-144 `a71cc2415` | A device-creation failure in `Game`'s constructor is wrapped as `NoSuitableGraphicsDeviceException`, with the cause inside (XNA `CreateDevice` IL). A directly constructed `GraphicsDevice` keeps its own refusals. | src [compat] | `Game.cpp:259,372` |
| CBIND-158 `42181a9bb` | After a failed C callback, only the **UnloadContent** cleanup still runs, after `Content.Unload`. This was measured on real XNA 4.0 under Wine/DXVK with the new `tools/xna-oracle/LifecycleFailureOracle.cs`: `UNLOAD_CONTENT_CALLS=1`, `ORDER=Content.Unload,Game.UnloadContent`. Frame and event callbacks stay suppressed. No ABI change. | src + compat (oracle) | `tools/xna-oracle/README.md` "Lifecycle failure oracle" |
| CBIND-128/129 `bdf239360` `6e0de68e8` | Component C handlers run inside the game's callback scope (they can borrow the device). The initialize handler now runs before base LoadContent. | src | C-ABI agent |

### A9. Build

| Item | Fact | Class | Evidence |
|---|---|---|---|
| Options diff (`option(CNA_…)`) | Counting only `*.cmake` and `CMakeLists.txt`: O 71 → T 62 distinct options (a whole-repo grep, including docs, gives 78 → 69). **Added:** `CNA_EMSCRIPTEN_USE_WASMFS` (ON). **Removed:** `CNA_RENDERER_{DIRECT2D,FREEDIRECT,GDI,HTML_DOM,OPENGL4,PORTABLEGL,SVG_DOM}`, `CNA_OPENGL4_COMPILED_EFFECTS`, `CNA_BUILD_HTML_DOM_HOST_TESTS`, `CNA_BUILD_SVG_DOM_HOST_TESTS`. The T grep's `option(CNA_RENDERER_` match is a doc string in `docs/removed-renderers.md:124`. | build | `git grep -oE 'option\(CNA_…'` O vs T |
| Cache variables | **Added:** `CNA_ENABLE_VOICE` ("AUTO"; `modules/net/CMakeLists.txt:30`), `CNA_EASYGL_ROOT` (`cmake/RendererSelection.cmake:202`), `CNA_GAMER_SERVICES_SERVER_ROOT` (`cmake/Harnesses.cmake:626`). **Removed:** `CNA_SDL2_ROOT`, `CNA_SDL2_GIT_REPOSITORY`, `CNA_SDL2_GIT_TAG`, `CNA_DIRECT2D_TEST_RUNTIME`. | build | same |
| Compiled-effect options | 9 → **8**: EASYGL, VULKAN, WEBGPU, SOFTWARE, DIRECTX9, DIRECTX11, DIRECTX12, SDL_GPU. | build | grep `_COMPILED_EFFECTS` |
| `CNA_CNAEXT` help text | Now "standalone ASCII, CRT, colour-depth and DebugDraw graphics extensions" (CNAEXT agent). | build | `CMakeLists.txt` diff |
| Presets | `CMakePresets.json` is byte-identical between O and T. | build | `git diff --stat` empty |
| CNA-F3 `e2a5b5a46` | A read-only CNA checkout fails with a message naming `-DCNA_SDL_PREBUILT_ROOT` (the shared `.sdl-prebuilt-<key>` cache default is unchanged). | build | `cmake/ThirdPartySDL.cmake` |
| CNA-F4 `b8d3660e2` | README: the vendored SDL still needs X11, OpenGL and audio dev headers (programs.md §2). `libxtst-dev` was added as required (SDL's X11 configure stops without XTest). A Wayland pointer goes to `docs/platform-wayland.md`. | build/doc | README.md, programs.md |
| `1ca684199` | Renderers link Sharp Runtime **without** Xml/tinyxml2 (`CNA_SHARP_RUNTIME_RENDERER_COMPONENTS`); the `CNA` umbrella still provides them. This fixed tinyxml2 version clashes (MeshCraft). | build | `cmake/SharpRuntimeConsumption.cmake` |
| BL-17 | See A3. | build | |
| README/getting-started | `README.md` diff is mostly renderer, CNAEXT and GS (other agents) plus CNA-F4. There is **no** `docs/getting-started*` change in O..T. | doc | `git diff --stat O T -- README.md docs/getting-started*` |
| `b0e97bb1b` | `CHANGELOG.md` link refs `openeggbert/cna` → `libcna/cna` (2 lines). No content change. | doc | commit |

### A10. Tests / CI / verification assets

| Item | O → T | Explanation / evidence |
|---|---|---|
| Static GTest-family defs | 12,610 → 12,021 (my regex: 12,613 → 12,024, the same −589) | **Deleted files: 105 files / 1,190 defs:** `modules/graphics-ext/tests` 86/874 (MOD-RETIRE-1, `5572f3ca1`), `renderers/svg-dom` 1/100, `renderers/opengl4` 9/98, `renderers/html-dom` 1/60, `renderers/direct2d` 1/25, `gamer-services/tests` 3/17, graphics 1/6, platform 1/5, content 1/4, audio 1/1. **New files: 55 / +468:** gamer-services 25/248, net 15/160, renderers/software 2/25, input 2/12, runtime 4/8, graphics 3/5, devices 1/4, content 1/4, vulkan 1/1, sdl-gpu 1/1. **Existing files: +133 net** (net +53, graphics +29, GS +21, runtime +15, platform +13, …, graphics-ext −17). |
| Test files | 904 / 871 with macros → 852 / 821 | as above |
| All deleted test-path files (incl. non-gtest) | 303 of 900 deleted paths match `test` | top dirs: graphics-ext/tests 146, renderers/opengl4 37, graphics-ext/examples 24, gdi 17, portablegl 13, freedirect 10, vulkan 8, tests/fixtures/direct2d 7, html-dom 6, direct2d 6, svg-dom 4, GS tests 4, sdl-gpu 3, c-api tests 3, … plus 6 htmldom/svgdom scripts and `cmake/Tests/Sdl2OnlyRendererGate.cmake` |
| `examples/**/*_test.cpp` pixel programs | 879 → **779** | `git ls-tree -r` count |
| Workflows | 20 → **18** files; 28 → **26** jobs | deleted `gdi-windows-ci.yml` (workflow_dispatch, 1 job) and `htmldom-ci.yml` (push + PR, 1 job). My push/PR-key count gives O 18/26 → T 17/25 automatic files/jobs. The site's O figure is 17/24 by its own method, so apply −1 file/−1 job (→ 16/23) or recount. Modified: 32bit-arithmetic, d3d-windows (−158 lines, Direct2D leg gone), emscripten-multi-renderer, platform-ci. |
| XNA oracle scenes | 39 → 39 `.scene` | `tools/xna-oracle/scenes`. Newly added: a **non-rendering** `LifecycleFailureOracle.cs` (CBIND-158); the GDI arm was removed from `CnaOracleRender.cpp`. |
| XNB built-in readers | 61 (60 without int128) → **unchanged** | `modules/content/src/Xnb/XnbBuiltInReaders.cpp` has no diff. The registration test changed only in its cube-storage renderer list. |
| XNA runtime surface census | 331/331 types, 3,627/3,627 members → **unchanged in the committed report** | `docs/xna-4-runtime-member-coverage.md:7,20-21` at T. The JSON was regenerated once in O..T (GS-011b `39b037130`), changing only 2 `cna_symbol` strings (Guide `IsTrialMode`/`IsVisible` setters dropped). Microsoft-header deletions in O..T are all EXT (`AvatarAnimationPresetNamesEXT`, `AvatarAppearanceEXT`, `AvatarBodyTypeNamesEXT`, `AreaLightEXT`), plus 68 modified Microsoft headers. I did **not** re-run `tools/audit_xna_runtime_surface.py` (it needs Microsoft inputs outside the repo). Wording: "committed report at T: 331/331, 3,627/3,627". |
| New C test isolation | CSX-153 `8a7e13ff5` isolates the C API audio smokes | `modules/c-api/CMakeLists.txt` |

### A11. Version / release

- `CMakeLists.txt:3` `project(CNA VERSION 0.1.0)`; `:12` `set(CNA_VERSION_PRERELEASE "alpha.1")`, so `CNA_VERSION_STRING = 0.1.0-alpha.1` [src].
- Tags: `git tag -l` gives `audit-2026-07-complete` and `v0.1.0-alpha.1`. `git tag --contains O` is empty, so **no release after alpha.1**.
- Distance: `v0.1.0-alpha.1..T` = 3,333 commits, 945 first-parent, 65 merges. O..T adds 456 commits, 232 first-parent and 18 merges. T date 2026-10-04; T is on `next` (and `samples`).
- `CHANGELOG.md [Unreleased]` gained GS, RLGL and related Added entries (O..T +28 lines). Stale internal line still present: "`Content` has no general `.xnb` reader by design" (CHANGELOG at T, older section; not a site concern).

### A12. Other O..T items, noted for completeness (another agent owns each)

- Renderer agent: WIN11-0003..0103 (`7301f386a` merge). Physical Windows 11 and Intel GPU validation of classic DX11 and DX12, and DX12 swap-chain first-frame fix WIN11-0091. `plans/plan_windows11_directx.md` (T) says a "native MSVC and physical Intel GPU baseline established on 2026-09-25", yet README at T still says "real-Windows hardware verification … still open". Also FULLSCREEN-001/002 (DirectX9, Vulkan and Canvas letterbox/scale recovery), STREETPERF/WEBGPUPERF/STREETGL4 (performance), DX-271, GDI-079/080 (later retired), SOFTWARE-485, VULKAN-154/159.
- C-ABI agent: CBIND-130/132/134/141/145/152..155 (ABI 0.36–0.44); BINDFIX-037/038/040/042..049.
- GS agent: all `GS-*`, `GSX`, `GSP`, `GSH`, `SAMPLE-100/104`; CBIND-136's libcurl-optional rule.

---

## B. libcna.com mapping (stale claims and missing new capability)

I grepped the whole site excluding `audit/`, `scripts/`, `known-issues/`, `search-index.json` and `sitemap.xml`. Line numbers are from the current working tree (HEAD `df85d05`).

### B1. Threading / GL context

| file:line | Current text (short) | Corrected / new text (short) |
|---|---|---|
| docs/tutorials/78-multithreading.html:110 | "`SpriteBatch`, `Texture2D`, buffers, render targets — No — GPU-facing use and disposal are serialized on the device's thread" | "Not concurrently thread-safe. On the GL renderers (EasyGL), constructing, `SetData`, `GetData` and `Dispose` may run on a loading thread: each takes the GL-context lease and waits for the gap between frames (KF-1). Drawing stays on the game thread." |
| …/78-multithreading.html:112 | "`Texture2D::GetData` … main thread only" | "Game thread, or a loading thread on EasyGL (it takes the lease and runs between frames)." |
| …/78-multithreading.html:113 | "`ContentManager::Load` — No — Creates GPU resources; the asset cache has no lock" | "Usable from **one** loading thread at a time (XNA's loading-screen pattern). On EasyGL `ContentReader` holds the lease for the whole asset. The manager's cache is still unlocked: never load through one manager from two threads." |
| …/78-multithreading.html:124 | "Never call any CNA rendering API from a worker thread." | "Never draw from a worker. On EasyGL, resource creation, upload and readback from a loading thread are supported. **Do not wait** inside LoadContent/Update/Draw for a worker that creates graphics resources: the game thread holds the context for the whole frame, so that deadlocks (FNA and MonoGame do the same)." Cite CNA `docs/opengl33-renderer.md` §"Graphics resources on other threads". |
| …/78-multithreading.html:7,12 (meta) | "GPU, input and audio calls on the main thread" | Soften to "draw, input and audio on the game thread; GPU uploads may run on a loading thread (GL renderers)". |
| docs/tutorials/77-async-loading.html:105 | "graphics API is owner-thread only … textures, buffers … must be used and disposed on the thread that owns the device" | Keep the decode/upload pattern as one option, and add that on EasyGL a loading thread may construct and upload (`Content.Load`, `new Texture2D`, `SetData`) between frames. |
| …/77-async-loading.html:272-273 | "`ContentManager::Load<T>()` is **not thread-safe** … Do not call it from background threads … The actual `Load` calls must happen on the main thread." | "A single `ContentManager` is not safe for concurrent use, but a loading thread may own it: on EasyGL each load leases the context for the whole asset, and the frame waits until that asset is done. Use one manager per loading thread, and never wait for it from Update/Draw/LoadContent." Note that CNA-BUG-119 (reader registry) still applies to two concurrent loaders. |
| development/takeover/threading.html:174 | "a constructed `ContentReader` holds a renderer context lease …" | Add: "and since KF-1, every texture, buffer or render-target constructor, `SetData`, `GetData` and `Dispose`". |
| …/threading.html:187 | "`BeginDraw`…`EndDraw` holds one for the frame … absent: Any lock in `GraphicsDevice` itself" | "`Game` holds it for Initialize, BeginRun, each Tick (Update+Draw) and EndRun (KF-16). `GraphicsDevice::resources_` is now mutex-guarded (KF-1a). Only EasyGL leases (OPENGL4 was retired)." |
| …/threading.html:227 | "only the EasyGL and OpenGL4 renderers override it" | "only EasyGL". |
| …/threading.html:228 ("Who takes it") | "`GraphicsDeviceManager::BeginDraw` stores … `EndDraw` … releases it" | Add: `Game::AcquireGameThreadContextLease` wraps Initialize, BeginRun, Tick and EndRun. The manager's frame lease still exists, nested inside that. |
| development/internals/graphics/device.html:224 | "only the EasyGL and OpenGL4 families return one … the resource registry and bindings are mutated without any lock" | "only EasyGL … the resource registry is mutex-guarded (KF-1a); state and bindings are not". Add the BINDFIX-050 rule: several devices may be created and destroyed concurrently on different threads. |
| development/internals/graphics/easygl.html:223 | "serialises a background content upload against a frame" | "…against a frame. Since KF-1 all resource constructors, SetData, GetData and Dispose take it, and since KF-16 the game thread holds it for whole frames, including Update." |
| deep-dives/content/contentmanager-resolution-rules.html:278 | "perform every load … from one owner" | Still valid. Add the lease and deadlock rule, and the fact that the owner may be a loading thread. |
| deep-dives/siblings/easygl-and-metagl.html:248 | "no multi-threaded run was made for this page" | Optional: CNA now has `easygl_worker_thread_resources` (10/10, commit-recorded) and `CApi_ConcurrentDeviceCreationSmoke`. |
| development/internals/graphics/easygl.html:190; deep-dives/renderers/presentation-and-backbuffer-readback.html:227 | The EasyGL back buffer is the window surface; only the MSAA FBO is offscreen | "EasyGL draws into an offscreen FBO and blits at Present on GL 3.3, GLES 3 and WebGL 2 off the web (KF-6). `GetBackBufferData` reads that FBO at the logical size. ES 2 and the web canvas still use framebuffer 0." |

### B2. Input (new capability; no current mention anywhere)

| file:line | Current | New / corrected |
|---|---|---|
| docs/input.html:317-330 (GamePad) | No keyboard emulation | Add callout: "**Keyboard GamePad emulation (CNAEXT, off by default):** `GamePad::setKeyboardEmulationEnabledEXT(true)` makes player one a connected pad driven by the keyboard (WASD left stick, arrows right stick, TFGH D-pad, K/L/J/I = A/B/X/Y, Q/E shoulders, Z/C triggers, Shift stick clicks, Enter/Escape Start/Back). It merges with a real pad, keys stay visible to `Keyboard`, and players 2–4 are unchanged. No vibration or BigButton. [CNA `docs/keyboard-device-emulation.md`]" |
| docs/input.html:436-437 | "CNA adds 19 `CNAEXT`-tagged static functions" | "21" (+ `set/getKeyboardEmulationEnabledEXT`) |
| docs/input.html:617 (GamePad status row) | "19 CNAEXT extension functions" | "21 …; opt-in keyboard emulation for player one" |
| docs/input.html:572-575, docs/sensors.html:209, docs/tutorials/50-accelerometer.html:105,171 | `IsSupported` true only where a platform reports a sensor; "a browser build is excluded" | Add: "With `Accelerometer::setKeyboardEmulationEnabledEXT(true)` (off by default) the arrow keys drive a software primary accelerometer, and `IsSupported` is true on desktop **and Browser** without hardware." Tutorial 50 line 262 "Keyboard fallback" could mention the built-in switch. |
| docs/tutorials/30-gamepad.html | — | Add a short "no pad? test with the keyboard" box (same API). |
| docs/input.html (orientation) or docs/game-loop.html (GameWindow) | — | `getWindowProperty().setKeyboardOrientationEmulationEnabledEXT(true)`: Up/Left/Right request Portrait/LandscapeLeft/LandscapeRight within `SupportedOrientations` (INPUT-EMU-001). |
| docs/input.html:519-520 | Mouse→touch emulation described | Add: "touch-synthesised mouse events do not feed the emulation, so pinch stays two real fingers (SAMPLE-046); the emulated touch is clamped to the display (SAMPLE-067)." |
| docs/input.html:229 / development/internals/platforms/sdl3.html:208 | "`Sdl3Mouse::Update` reads `SDL_GetMouseState`" | "On the x11, windows and cocoa SDL video drivers it reads `SDL_GetGlobalMouseState` minus the window position, so the position is current and unclamped, as XNA's `GetCursorPos` (CBIND-148). Other drivers are window-relative." |
| docs/tutorials/11-mouse.html:229 (SetPosition) | "moves the OS cursor" | Add: "In a browser the OS cursor cannot move; CNA emulates the warp virtually (later physical deltas are applied to the requested point), so recentring mouse-look works (CSX-145)." |
| docs/game-loop.html:401 | "`getClientBoundsProperty()` … (X, Y always 0 …)" | "X, Y = the client area's desktop position where the platform reports one (0 on Wayland). Fullscreen size = the back buffer's size, as after XNA's mode switch (CBIND-147, CBIND-157)." |
| deep-dives/framework/window-and-device-manager.html:140 | "`ClientBounds` (client-local, so the desktop position never leaks into it)" | Same correction as above. |
| docs/tutorials/82-android.html (input section) | — | Add: "Android Back reaches the game once as `Keys::Escape` and, for a game that polls pads, as `GamePad.GetState(PlayerIndex::One).Buttons.Back` (CBIND-137)." |

### B3. Content root, exceptions, `.cnb` on Android, XACT build

| file:line | Current | Corrected |
|---|---|---|
| docs/tutorials/45-content-manager.html:124, :166 | "relative to the working directory" | "relative to the title folder (`TitleLocation.Path`) when `<title>/Content` exists, else the working directory (CBIND-140; Android: packaged assets)". |
| docs/tutorials/145-content-pipeline-build.html:213, :279, :321, :354 | "The working directory decides …" | Same rule. Running from another directory now works when `Content/` sits beside the executable. Downgrade the troubleshooting row to "content is neither beside the executable nor in the working directory". |
| docs/tutorials/147-xnb-interop.html:129, :321 | "The root directory is relative to the working directory" | Same. |
| docs/tutorials/148-custom-content-type.html:317, :630-631 | same | Same. |
| docs/tutorials/137-alsa-audio.html:332 | "resolved against the working directory, which is why you run from the directory that holds it" | "resolved under the executable's folder first". The `cd build-alsa` advice is optional. |
| docs/tutorials/04-game-lifecycle.html:223 | "(a `Content` folder relative to the process's working directory …)" | "relative to the game's title folder (falls back to the working directory)". |
| docs/tutorials/08-textures.html:128; 13-sprite-sheets.html:304; 12-moving-sprites.html:296 | code comments "relative to the working directory" | "relative to the title folder (falls back to the working directory)". |
| docs/content-pipeline.html:495, :581 | same | same |
| deep-dives/content/contentmanager-resolution-rules.html:196 | `root "" … (relative to the working directory)` | An empty root never resolves under the title (`ResolveContentRoot` returns empty), so the line stays. Add a row for a non-empty relative root resolved under the title. |
| deep-dives/platforms/android-and-apple-platforms.html:162 | "On the desktop … a relative content root is resolved against the process working directory first …; no test … loads content … inside an APK" | Desktop: title-first rule. APK: BL-19 records House Simulator loading all `.cnb` from the APK on the emulator (commit-recorded; still no CNA test or artifact). |
| docs/tutorials/147-xnb-interop.html:118, :128, :322; docs/content-pipeline-xnb.html:371; deep-dives/content/contentmanager-resolution-rules.html:257; deep-dives/content/content-robustness.html:198; docs/tutorials/148-custom-content-type.html:634 | "wrong `T` raises `std::bad_any_cast`"; "`ContentLoadException` (a `std::runtime_error`)" | "A wrong `T` throws `ContentLoadException` naming the asset and the produced type (KF-9). `ContentLoadException` derives from `System::Exception` (KF-13), so `catch (const System::Exception&)` now sees content failures." The robustness page (fuzzer) should say `bad_any_cast` is no longer an accepted rejection. |
| deep-dives/framework/game-class-and-lifecycle.html:260 | "One derives from `std::runtime_error`: … `ContentLoadException` …" | Move `ContentLoadException` to the `System::Exception` family. |
| deep-dives/reference/verification-tiers.html:292 | "surviving item is that `ContentLoadException` derives from `std::runtime_error` by design" | Resolved by KF-13 at T (the known-issues agent should close CNA-GAP-001; the reference page needs the same edit). |
| docs/content-pipeline.html:529 | "`BuildXact` is declared" | "`BuildXact` runs Microsoft's `XactBld3` (path via `CNA_XACTBLD`, launcher such as `wine` via `CNA_XACTBLD_LAUNCHER`, or `SetXactCompilerEXT`) with `/WINDOWS` or `/XBOX360` and Wine path mapping. Qualified with XactBld3 9.28.1886.0 under Wine on two unchanged projects. The Xbox 360 target is argument-tested only." |
| docs/tutorials/120-xact.html:128 | "CNA cannot author these files — it only reads them. They come from Microsoft's XACT3 authoring tool." | Keep "cannot author", and add: "CNA's content pipeline can **build** them from a `.xap` by driving Microsoft's `XactBld3` (also under Wine on Linux) — see Content Pipeline." Do not claim XACT2/XNA2 runtime parity. |
| docs/cnb-format.html:257 | XREF "by the exact name you would pass to `Load<T>()`" | Add: "relative to the content root the file was compiled against (unlike `.xnb`, which resolves against the referring asset)" (LRS-R28). |
| docs/model-loading.html:447; docs/tutorials/112-gltf-animation.html:128 | (claims `.cnj`/`.cnb` list skins in `SkinsEXT`) | Now true at T (CNASTREET-SKINMETA, one skin per compiled model). Wording is fine; optionally drop "Multi-skin models loaded from `.cnb` were not verified" → "a compiled model lists its one skin in `SkinsEXT`". |
| docs/tutorials/112-gltf-animation.html:141; deep-dives/models/skinning-and-animation.html:213-215 | "`P_root = W_ancestor * inverse(W_meshNode)` … the cancellation of the skinned mesh node's own transform" | "`P_root = W_ancestor`: the skinned mesh node's transform is ignored, as glTF 2.0 §3.7.3.2 requires (CNASTREET-SKINDRAW, `e9e2b5d2e`)." |
| deep-dives/graphics/graphicsdevice-contract.html:251 | "declaration-less `DrawUserPrimitives(type, const void*, …)` reads its array as VertexPositionColor" | Add: "a pointer to any other non-stock struct without a declaration no longer compiles (CCS-2)". |

### B4. Effects / compiled effects

| file:line | Current | Corrected |
|---|---|---|
| docs/graphics-state.html:446 | "`MipMapLevelOfDetailBias` … Not representable on GL ES" | "Not representable as GL ES sampler state; EasyGL emulates it for compiled vertex `TEXLDL` on ES 3 (FX-146). Stock and pixel sampling on ES still ignore it." |
| docs/building.html:353; docs/tutorials/128-compiled-xna-effects.html:75 | "nine options" (lists `CNA_OPENGL4_COMPILED_EFFECTS`) | "eight" (OPENGL4 retired; renderer agent may also edit). |
| docs/tutorials/128-compiled-xna-effects.html (renderer table ~63) | — | Add a GLES/WebGL note: compiled effects with volume samplers, SM3 point-size, SM1 COLOR inputs and float textures now work on OPENGLES3/WEBGL2 (FX-140..145; 686/686 compiled-effect tests on Mesa GLES 3.2, commit-recorded). |
| deep-dives/graphics/compiled-effects-semantics.html:201-211 | EasyGL profile table / refusals | Add the ES 3 preamble facts (`highp sampler2D/samplerCube/sampler3D`), the vertex LOD-bias uniform, and the patch count 124 (all pinned to MojoShader `6333f74`). |
| deep-dives/graphics/stock-effects-semantics.html (BasicEffect section ~161) | — | Add: "`Apply` binds the effect's texture (null too) to the device's sampler slot; a draw samples `GraphicsDevice.Textures` as it stands, so a texture set after `Apply` is drawn, as in XNA (CBIND-156)." |
| deep-dives/graphics/spritebatch-semantics.html:157 | "`Effect*` — the renderer's built-in sprite shader" | Add: "a stock effect passed here (BasicEffect …) transforms the sprites by its own matrices, drawn as indexed quads per pass (Task 1120)". |
| docs/3d-rendering.html:948, :969 | "`FillMode::WireFrame` is **not available** on … OPENGLES2, OPENGLES3, WEBGL1, WEBGL2" | "`GraphicsCapability::WireFrame` stays false there. EasyGL still emulates two bounded stock routes without a polygon-mode API: non-indexed PositionColor triangles, and indexed PositionNormal with clipping, culling and depth (SAMPLE-048/055). Other wireframe draws refuse." |
| docs/tutorials/65-msaa.html / docs/render-targets (WebGL) | — | Optional: WebGL never applies the sample mask (an all-ones mask is fine); 1- and 2-channel render targets read 0 in the unstored channels on WebGL (CBIND-149/150). |

### B5. Browser storage (the largest stale cluster)

Canonical replacement text:
> "Since SAMPLE-070, CNA's storage module mounts IndexedDB-backed IDBFS at `/cna-storage` (StorageDevice) and `/save` (IsolatedStorage) and restores both before `main()`; writes persist automatically. `StorageDevice` throws `StorageDeviceNotConnectedException` if browser storage cannot be mounted. **Threaded builds** use WasmFS by default, which cannot host IDBFS. Configure `-DCNA_EMSCRIPTEN_USE_WASMFS=OFF` to get persistence there. Keep WasmFS if the game loads content on worker threads. GamerServices' local profile store is not under these mounts."

Classes: src plus rt (Chrome reload and Firefox, SAMPLE-070, commit-recorded). The GS sentence is a source inference only, not run.

| file:line | Current |
|---|---|
| docs/storage.html:148 | "On the web, saves do not persist … finds no IDBFS, no FS.syncfs, no FS.mount" |
| roadmap.html:304 | "CNA mounts no persistent file system … documented gap" |
| docs/faq.html:284 | "There is no save persistence at all …" |
| docs/xna-compatibility.html:388 | "On the Web there is no save persistence at all" |
| docs/verification.html:564 | "Web has no save persistence at all" |
| docs/platforms.html:562 | same |
| docs/rendering-backends.html:434 | "CNA itself provides **no save persistence** on the web" |
| docs/tutorials/81-emscripten.html:110 | "2. There is no save persistence at all" |
| docs/tutorials/100-shipping.html:115, :338 | "every save is silently discarded on reload"; checklist "confirm you are not relying on saves that do not persist" → change to "confirm saves survive a reload" |
| docs/tutorials/105-browser-renderers.html:212 | "no built-in save persistence" |
| docs/tutorials/80-cross-platform.html:222 | code comment "CNA mounts no IDBFS" |
| docs/tutorials/19-save-load.html:104, :158, :405-406 | three places, including "do the persistence yourself … localStorage" |
| docs/tutorials/124-web-gotchas.html:157-162 | whole gotcha ("do not route it through StorageDevice") |
| docs/tutorials/83-migrate-monogame.html:242 | "is lost when the page reloads" |
| deep-dives/platforms/web-build-and-main-loop.html:151-153 | §"Saves live in memory unless the page adds persistence". Rewrite it: `/save` is now mounted by CNA for IsolatedStorage too. |
| deep-dives/platforms/web-build-and-main-loop.html:146 | "…and on the final link `-sOFFSCREEN_FRAMEBUFFER=1` and `-sWASMFS=1`" → "`-sWASMFS=1` unless `CNA_EMSCRIPTEN_USE_WASMFS=OFF`" |
| features.html:282 | "no read/write round-trip test" — still true for native; the browser round trip was runtime-observed in SAMPLE-070 (not a ctest) |
| docs/building.html:491 (options table) | add a row: `CNA_EMSCRIPTEN_USE_WASMFS` ON/OFF, default ON: "threaded Emscripten builds use WasmFS; OFF selects the legacy FS, required for IDBFS persistence" |
| docs/platforms.html:479 | "Threads option `CNA_ENABLE_EMSCRIPTEN_THREADS`" → add `CNA_EMSCRIPTEN_USE_WASMFS` |
| docs/tutorials/78-multithreading.html:127, docs/tutorials/77-async-loading.html:277 | threaded-web callouts: add the WasmFS/persistence trade-off |

### B6. Android

| file:line | Current | Corrected |
|---|---|---|
| deep-dives/platforms/android-and-apple-platforms.html:147-158 ("Mobile lifecycle: explicit, and tested only in portable form") | Table implies the lifecycle events arrive | "At the previous snapshot the SDL3 lifecycle events were mapped but never delivered (`SDL_SendAppEvent` does not queue). Since BL-20 an event watch delivers them, and on Android `IsActive` follows WillEnterBackground/DidEnterForeground, not window focus (BL-21). Host tests plus a House Simulator emulator run (commit-recorded)." |
| …android-and-apple-platforms.html:165-166 | "no CNA binary has a record of running …; no Android APK of any CNA application" | Soften: commit messages in this range record emulator runs of House Simulator (lifecycle, `.cnb` from the APK) and of cna-cs games (CBIND-137..139). There is still no Android workflow or preset and no retained APK or logcat in the repo. |
| …android-and-apple-platforms.html:137 (Entrypoint) | — | Add: `CNA_PLATFORM_<X>` now reaches consumers via `CNA::BuildConfig`, so a game built beside CNA with `add_subdirectory` gets `SDL_main` (BL-13). |
| docs/tutorials/82-android.html:107 | "Everything on this page is a documented route, not a machine-verified one" | Keep "no CI", and add the emulator observations above as commit-recorded. |
| deep-dives/framework/window-and-device-manager.html:167, :205-207 | "a phone game that asks for 480×800 gets an 800×480 back buffer unless it also asks for Portrait" | CBIND-138: `SupportedOrientations::Default` is resolved from the preferred back buffer, so 480×800 now runs in portrait on Android (host-tested with a reported-Android platform). Re-check the wording. |
| docs/tutorials/82-android.html (renderer/3D) | — | Note: on the Android emulator EasyGL rebases base-vertex draws on the CPU; `CNA_EASYGL_CPU_BASE_VERTEX=1` forces it (CBIND-139). |

### B7. Audio

| file:line | Current | Corrected |
|---|---|---|
| deep-dives/services/sound-effects-and-streaming.html:148 | "`DistanceScale` (… 0 or less throws …), `DopplerScale` (… negative throws) and `SpeedOfSound` (default 343.5, **not validated**)" | "`MasterVolume` outside 0..1 or NaN throws. `DistanceScale` negative throws, 0 becomes the smallest positive float. `DopplerScale` negative or NaN throws. `SpeedOfSound` ≤ 0 or NaN throws (KF-12, XNA's IL)." |
| …sound-effects-and-streaming.html:185 | "Submissions are range-checked but not checked for frame alignment … accepted, where XNA throws" | "`SubmitBuffer` refuses an empty buffer, or an offset or count not in whole frames, with `ArgumentException`, as in XNA (KF-12). A looped dynamic instance throws `InvalidOperationException`." (I did not check float submissions.) |
| …sound-effects-and-streaming.html:195 | Microphone `GetData` no alignment check | **Still true** at T. |
| docs/tutorials/118-dynamic-audio.html:200-205 | sizing helpers | Add: "computed as XNA computes them (whole frames, XNA's float rounding: 1 s of 44.1 kHz mono = 88,198 bytes), not FNA's 88,200 (KF-7/8)". |
| docs/tutorials/14-sound-effects.html:153 | "A pan outside −1…1 throws …; pitch is clamped." | **Still true for `SoundEffect::Play(v,p,pan)`.** Add: "`SoundEffectInstance::setPitchProperty`/`setVolumeProperty`/`setPanProperty` outside range or NaN throw `ArgumentOutOfRangeException` (KF-12)." |
| known-issues vgap-035 and dev bindings pages citing "8,000–48,000" | — | Public constructors: unchanged. Add: XNB-built sounds accept 1,000–200,000 Hz (CBIND-146). |
| docs/audio.html (codecs / robustness) | — | Optional: a malformed WAVE (0 channels, rate or block size) is refused with `NotSupportedException` (KF-17). |

### B8. Game loop / exceptions

| file:line | Current | Corrected |
|---|---|---|
| deep-dives/framework/exit-and-shutdown-semantics.html:144 | "An `Exit()` from `Update` does not stop the current tick. The remaining catch-up updates of that tick still run" | "`Exit()` stops the tick: no further catch-up Update runs, and a quit event handled in `PollEvents` prevents that frame's Update (XNA IL; FNA differs) (KILLER-1)." |
| development/internals/runtime/frame.html:172 | "a fixed-step tick that already entered its update loop runs its remaining catch-up updates" | same correction |
| deep-dives/framework/game-class-and-lifecycle.html:159, :164 | `InactiveSleepTime` / `TargetElapsedTime` throw `std::out_of_range` | `System::ArgumentOutOfRangeException("value")` (KF-15) |
| deep-dives/framework/game-class-and-lifecycle.html:259 | "21 explicit throw sites … all standard types: `std::out_of_range` … `std::invalid_argument` (… duplicate component …) … `std::logic_error` (SetItem)" | The property guards and collection now throw XNA types (`ArgumentOutOfRangeException`, `ArgumentException`, `NotSupportedException`). Recount the throw sites before restating "21". |
| deep-dives/framework/game-class-and-lifecycle.html:264 (code comment) | "renderer or platform failures surface here" | "a device that cannot be created surfaces as `NoSuitableGraphicsDeviceException` with the cause inside (CBIND-144)". |
| deep-dives/framework/services-and-components.html:162, :163, :166 | duplicate gives `std::invalid_argument`; indices give `std::out_of_range`; `SetItem` gives `std::logic_error` | `ArgumentException` (CannotAddSameComponentMultipleTimes); `ArgumentOutOfRangeException("index")`; `NotSupportedException` (KF-14). Add: a rejected Add no longer drops a shared_ptr reference. |
| development/internals/bindings/c-api-internals.html:226 | "once latched, later callbacks … are skipped" | "…except the UnloadContent cleanup, which still runs after `Content.Unload`, as measured on real XNA (CBIND-158; `tools/xna-oracle/LifecycleFailureOracle.cs`)". |

### B9. Build, tests, version (numbers)

| file:line | Current | Corrected (T) |
|---|---|---|
| index.html:128-129,134,147; about.html:70,166; features.html:80; docs/faq.html:147,299; docs/releases.html:112,134,159-160; docs/vs-alternatives.html:133,245; docs/verification.html:154; docs/building.html:133; docs/tutorials/01-introduction.html:116; roadmap.html:76; docs/roadmap.html:131; deep-dives/reference/glossary.html:140; contribute.html:123,162,288 | snapshot `009d40f5`, 24 Sep 2026, 2,877 commits (713 first-parent, 47 merges); 904 test files / 12,610 defs / 871; 879 pixel programs | `b0e97bb1`, 4 Oct 2026, **3,333 commits (945 first-parent, 65 merges)**, `git describe` `v0.1.0-alpha.1-3333-gb0e97bb1b`. Version string still `0.1.0-alpha.1`, no newer tag. **852 test files / 12,021 defs / 821 with macros. 779 standalone pixel programs.** |
| contribute.html:133,258; roadmap.html:236; docs/roadmap.html:246; about.html:75; docs/faq.html:249,301; showcase.html:106; docs/vs-alternatives.html:252 | "20 workflow files (28 jobs; 17 auto / 24 jobs)"; "the D3D and GDI Windows lanes are manual"; "HTML DOM browser" workflow | **18 files / 26 jobs.** The auto-triggered count drops by 1 file and 1 job (`htmldom-ci` deleted), giving 16/23 by the site's method; recount. The GDI lane and HTML DOM workflow are gone. |
| index.html:134 tooltip; about.html:166; docs/faq.html:299 | "879 standalone renderer pixel programs" | **779** |
| roadmap.html:155; index.html:217; about.html:173; docs/faq.html:300; docs/roadmap.html:183 | 39-scene oracle | unchanged (39). Optional: "plus a lifecycle-failure oracle (non-rendering)". |
| about.html:116; roadmap.html:137,274; contribute.html:276; docs/vs-alternatives.html:217; docs/roadmap.html:165; docs/verification.html:630; features.html:165; docs/faq.html:367 | 61 XNB readers | unchanged |
| index.html:135,169; documentation.html:134; docs/faq.html:148; docs/migration-from-monogame.html:147; roadmap.html:166; docs/verification.html:213,511-512 | 331/331, 3,627/3,627 | unchanged in the committed report at T (not re-run) |
| docs/building.html:491 options table | — | add `CNA_EMSCRIPTEN_USE_WASMFS`, and `CNA_ENABLE_VOICE` (AUTO/ON/OFF, libopus network voice; GS agent may own it). Remove rows for retired options if any are present (renderer agent). |
| docs/tutorials/02-setup.html, docs/building.html:140-141 | already list `libxtst-dev` | OK. docs/native-platforms.html:383 and docs/tutorials/135-native-x11-build.html:81 omit `libxtst-dev`. Those recipes target `CNA_PLATFORM=X11`; whether the vendored SDL3 is still built there is unclear, so recheck rather than edit blind. |
| docs/building.html troubleshooting | — | Optional: a read-only CNA checkout fails with an error naming `-DCNA_SDL_PREBUILT_ROOT` (CNA-F3), and an already-patched shared FNA3D in `~/deps` no longer needs to be writable (BL-17). |

---

## C. Caveats

- Every "rt" entry relies on commit messages, NEXT.md, AUDIT.md, `plans/` or `handoff.md` at T. None was reproduced here.
- Android and browser runs are emulator and headless-Chromium observations. **There is no Android CI, and no CNA ctest drives a threaded browser build.**
- My static gtest regex (`^\s*(TEST|TEST_F|TEST_P|TYPED_TEST|TYPED_TEST_P)\(`) gives 12,613/874 at O and 12,024/824 at T. The deltas match the orchestrator's 12,610 → 12,021 exactly (−589).
- My workflow auto-trigger counting (`push`/`pull_request` keys) differs from the site's for O (18/26 vs 17/24). Report only the delta, or recount with the site's method.
- The context lease applies to EasyGL only. Do not generalise the new threading rules to Vulkan, SDL_GPU, WebGPU, DirectX or Metal.
- The claim that the GamerServices local store does not persist in the browser is a source reading of `LocalProfiles.cpp`, not a run.
