# Phase-4 editorial guide — libcna.com update to CNA snapshot b0e97bb1

Repository: /rv/data/development/github.com/libcna/libcna.com (static HTML site; branch develop; DO NOT commit, DO NOT push).
CNA: /rv/data/development/github.com/libcna/cna — read ONLY via git objects (`git -C ../cna show T:path`, `git -C ../cna ls-tree -r T`, `git -C ../cna grep -n PAT T -- paths`, `git -C ../cna diff O T -- path`). Never check out / reset / build.
T = b0e97bb1bb876f9b3edd6f4ff1ef3067908ae8ac (new pin, 2026-10-04, branch next). O = 009d40f5dd085c4e674d3479675fac84b12b3e0a (old pin).
Scratchpad (facts, worklists): <scratch>/
Fact sheets with evidence: scratchpad/facts/R1-cnaext.md, R2-renderers-platforms.md (§8.5 has a per-page table of renderer/SDL2 hits), R3-c-abi.md (§5 per-page C ABI fixes), R4-cna-net.md, R5-cs-samples.md, R6-cpp-samples-gallery.md, R7-bindings.md, R8-gamer-services.md, R10-other-delta.md (per-topic site mapping), R9-known-issues.md (when present).
Per-page mechanical worklist: scratchpad/page-worklist.txt (missing cited paths at T, identifiers that no longer exist anywhere in CNA, identifiers that left a cited changed file, count of removed-renderer lines).

## 0. What NOT to do
- No redesign; keep CSS classes, page structure, headings, callouts, tables, tone. Minimal, precise edits. Do not shorten a page by more than needed (a Phase-4 presentation check fails on >10% shrink of a page or block without a recorded reason — removing a whole section about a removed subject is fine, report it).
- Do not edit generated regions: anything between `<!--dev:...-->` markers (sidebar, breadcrumb, pager), `<!--p3:deep-links-->…<!--/p3:deep-links-->`, `<!--p3:issue-links-->…`, text inside `<!--issue:KEY-->…<!--/issue-->` markers, the footer, `development/reference/*.html`, `known-issues/**`, `data/known-issues.json`, `search-index.json`, `sitemap.xml`. Do not edit files outside your assignment.
- No first-person voice, no marketing hyperbole, no claims stronger than the evidence (source-verified ≠ built ≠ run ≠ platform-qualified).
- Do not change `009d40f5` → `b0e97bb1` in links or snapshot labels yourself; the orchestrator re-pins mechanically after your pass. DO fix every cited path that no longer exists at T (see §9).

## 1. The seven removed renderers — owner decision
CNA's public site presents EXACTLY 18 renderer identities, as if CNA had always had only these. The seven removed identities are DIRECT2D, FREEDIRECT, PORTABLEGL, GDI, HTML_DOM, SVG_DOM, OPENGL4 (also the other 26 older retired ones). They must not appear on any public page in ANY spelling: `DIRECT2D/Direct2D/direct2d`, `FREEDIRECT/FreeDirect/free-direct`, `free-api`, `PORTABLEGL/PortableGL/pgl*`, `GDI` as a renderer (Win32 API prose must say `gdi32` or "Win32 surface presenter"), `HTML_DOM/HTML DOM/html-dom/HtmlDom`, `SVG_DOM/SVG DOM/svg-dom/SvgDom`, `OPENGL4/OpenGL4/opengl4/"OpenGL 4" as a renderer name`, `DirectDraw` (FreeDirect context). Also no "formerly supported", "retired", "removed renderers", "used to have 25", "down from", "no longer". No tombstones. Just describe the 18.
- Removing a renderer from a list: rewrite the sentence naturally; remove table rows; delete sections dedicated to them; recount.
- Gate: `python3 scripts/check_retired_renderers.py` must report 0 lines for your files (it scans all public files; filter its output to your files).

## 2. Canonical numbers at T (data/current-facts.json)
| Fact | Value at T |
|---|---|
| Public renderer identities | 18: SDL_RENDERER OPENGLES2 OPENGLES3 OPENGL33 WEBGL1 WEBGL2 VULKAN WEBGPU HEADLESS SOFTWARE STUB DIRECTX11 DIRECTX12 CANVAS DIRECTX9 SDL_GPU METAL FNA3D |
| Implementation families | 14 (EasyGL implements OPENGLES2, OPENGLES3, OPENGL33, WEBGL1, WEBGL2; every other identity has its own family): canvas directx9 directx11 directx12 easygl fna3d headless metal sdl-gpu sdl-renderer software stub vulkan webgpu |
| Deliberately 2D-only | 2: SDL_RENDERER and CANVAS (STUB reports no 3D capability at all; HEADLESS reports ThreeD) |
| GraphicsCapability members | 19 (unchanged) |
| Compiled XNA effects | 13 identities in 9 families: FNA3D always on, plus eight default-OFF options `CNA_{DIRECTX9,DIRECTX11,DIRECTX12,EASYGL,SDL_GPU,SOFTWARE,VULKAN,WEBGPU}_COMPILED_EFFECTS` (EASYGL covers its 5 identities) |
| Platform implementations (CNA_PLATFORM) | 6: SDL3 (default), X11 and WAYLAND (native, where their development packages exist), WIN32 (Windows targets), HEADLESS, TERMINAL (POSIX) |
| Audio implementations (CNA_AUDIO_PLATFORM) | 3: SDL3 (default; SDL3_mixer-backed XNA playback engine, SOUND_ENABLED), ALSA (native Linux, CNA's own mixer, SOUND_ENABLED), NULL (deterministic, no mixer) |
| SDL-linking renderers | 3: SDL_RENDERER, SDL_GPU, FNA3D. `CNA_ENABLE_SDL=OFF` refuses the SDL3 platform, SDL3 audio and these three renderers |
| Combination rules | one: the platform partition (GPU renderers need a native window; HEADLESS/TERMINAL platforms don't provide one), plus TERMINAL's renderer restriction |
| Defaults | WEBGL2 under Emscripten, OPENGLES3 on Linux, SDL_RENDERER elsewhere (Windows, macOS, Android, iOS) |
| Static GoogleTest-family definitions | 12,021 in 852 C++ test files (821 contain a counted macro) |
| CI workflow files | 18 (26 jobs) |
| Commits since v0.1.0-alpha.1 | 3,333 (945 first-parent, 65 merges); version string still 0.1.0-alpha.1 |
| XNA runtime surface | 331/331 types, 3,627/3,627 members REPRESENTED (declaration census; not behavioural parity) |
| Oracle scenes | 39 (unchanged); XNB built-in readers 61 (unchanged) |
| C ABI | 0.44.0 (encoded 0x00002C00), 60 public C headers, 3,210 declared routes/exports, 197 struct layouts; release gate "Not ready", 656 public symbols unmapped |
| Modern features | compute + indirect draw: EasyGL (desktop GL 4.3+/4.0+ or GLES 3.1+ contexts, never WebGL), SDL_GPU, VULKAN, WEBGPU, DIRECTX11, DIRECTX12. OPENGL33 keeps a 3.3 contract; there is no OpenGL 4 renderer profile |
| Windows 2D | SDL_RENDERER (default) or Direct3D 9/11/12. SOFTWARE stays off-screen on every windowing platform (SDL3, X11, Wayland, Win32); only TERMINAL on a TTY displays its frames |
| Browser renderers | WEBGL2 (default), WEBGL1, CANVAS (2D only), WEBGPU (experimental) |
Old values that must NOT appear as current: 25 identities, 21 families, 7 2D-only, 14 compiled-effect identities in 10 families / "nine default-OFF", 7 platforms, 4 audio, 12,610, 904 test files, 871, 20 workflows, 28 jobs, 2,877 commits, C ABI 0.29.0 / 0x00001D00 / 61 headers / 4,055 routes / 221 layouts / 468 unmapped, "three combination rules", "four SDL-based renderers".
Exact repeated phrase to replace: "the seven 2D-only renderers (SDL_RENDERER, DIRECT2D, CANVAS, HTML_DOM, FREEDIRECT, GDI, SVG_DOM)" → "the two 2D-only renderers (SDL_RENDERER and CANVAS)".

## 3. SDL2
SDL2 platform and SDL2 audio no longer exist in CNA (T). Remove CNA SDL2 from lists, tables, options (`CNA_SDL2_*`), the "platform SDL2 + audio SDL2" refusal rule, "SDL2 and NULL audio have no mixer" → "the NULL audio platform has no mixer". Keep only mentions of FNA's own SDL2 backend (third-party). Don't write SDL2 history.

## 4. CNAEXT — the retired graphics engine layer (MOD-RETIRE-1, 5572f3ca1)
Gone (must not be presented as existing): the engine layer's RenderPipeline, render passes, post-processing chain/PostProcessEffect passes, bloom/HDR/tonemapping engine (`setHDREnabled`, `setTonemappingMode`, `setBloomIntensity`), ShadowMap/CascadedShadowMap generation, clustered lighting (`ClusteredLightType`), EnvironmentProcessor/IBL texture generation, skybox, decals, volumetric fog, SSAO/contact shadows, GPU particles/compute classes, storage buffers, texture arrays, GPU timers (public classes), `AreaLightEXT`, engine_layer.h C routes (858), the 98-header layer (now 11 headers), 32 CNAEXT ctests. Nothing moved to a new public API.
Survives at T: `modules/graphics-ext` with the opt-in `CNA_CNAEXT=ON` (default OFF; no CI builds it): retro effects in `CNA::Graphics` — `AsciiPostProcessEffect` (+`AsciiQuantizeMode`), `CRTEffect` (+`CRTMaskType`), `DepthEffect` (+`DepthEffectMode`, `DitherMode`; it is colour-depth/palette reduction, NOT depth visualisation); `DebugDraw` (gizmo methods removed); `ShaderCodeEXT`/`ShaderPackageEXT`; master include `CNAEXT.hpp`; C header `graphics_ext.h` (44 routes). Core (not engine layer, unchanged): `PbrEffect`, `SkinnedPbrEffect`, `IShadowReceiverEXT`, `ShadowCascadeStateEXT`, `PunctualLightEXT`, `ImageBasedLightEXT`, morph targets (`MorphTargetEXT`, `SetMorphWeightsEXT`), glTF runtime loading, `SkinningData`/`AnimationPlayer`, the `CNAEXT` marker macro and the `EXT` naming convention for non-XNA API. CNA no longer GENERATES shadow maps or IBL textures: an application that wants them renders/supplies them itself (e.g. its own depth pass into a RenderTarget2D) and hands them to the PbrEffect receivers. `DrawPrimitivesIndirectEXT` exists in a header but no public class can create its argument buffer — do not present it as usable.
Wording: say "CNAEXT extensions" (the opt-in extension module), never "the CNAEXT engine layer" or "graphics engine". The docs page is now `docs/cnaext-extensions.html` (orchestrator rewrites it). Tutorials 153/154 were deleted (links now point to 114/59 — fix any anchor text that still says "Tutorial 153/154", "Image-based lighting tutorial", "Cascaded shadow maps").

## 5. C ABI (details: R3-c-abi.md)
0.44.0. Since 0.29.0: 0.30 deleted engine_layer.h (breaking); 0.31/0.33 retired renderer constants; 0.32/0.34 Guide/avatar rule and route changes; 0.35 merge; additive 0.36 `cna_packet_reader_copy_data_ext`, 0.37 canonical exception type/param name queries, 0.38 `cna_game_run_frame_ext` (host-driven run, also C++ `Game::RunFrameEXT`), 0.39 `cna_game_set_foreign_thread_calls_ext` (opt-in queue running other threads' calls on the game thread), 0.41 `cna_game_run_foreign_thread_calls_ext`; rule-only 0.40 (adapters before first callback), 0.42 (device lent before the run), 0.43 (`cna_sound_effect_play`/`_play_with_settings` on any thread), 0.44 (Activated/Deactivated handlers may use the device). Minor versions below 1.0 can break compatibility. The C ABI builds for Android with the NDK alone and as a static archive under Emscripten; a threaded browser build can run the game thread as a worker. CNA's own CI still builds no C library (header/JSON gates only). Routes that no longer exist: `cna_compute_shader_copy_compile_error` (use `cna_shader_effect_copy_compile_error_ext`), `cna_post_process_*`, `cna_skybox_*`, `cna_decal_pass_is_supported`.

## 6. Bindings (details: R7-bindings.md)
Maintained: C (the ABI) and C# (CNA.NET, `libcna/cna-cs`, beta, admits exactly C ABI 0.44.0). Archived (8): Common Lisp, Go, Java, Python, Ruby, Rust, Swift, TypeScript (incl. JavaScript) — kept with history in CNA Lab (`libcna/cna-lab`, `bindings/`); standalone repos no longer exist (links to github.com/libcna/cna-java etc. are dead → `https://github.com/libcna/cna-lab/tree/develop/bindings/cna-<x>`). Seven were requalified against C ABI 0.35.0 on 2026-09-30 before archiving; Common Lisp froze at 0.21–0.23. Never say Java/TypeScript are maintained.

## 7. Other CNA changes O→T to reflect where pages discuss them (details: R10-other-delta.md)
- Browser saves now persist: the storage module mounts IDBFS (`/cna-storage` for StorageDevice, `/save` for IsolatedStorage) with auto-persist, restored before `main()`; threaded builds need `CNA_EMSCRIPTEN_USE_WASMFS=OFF` for persistence.
- A relative content root resolves under `TitleLocation.Path` first, then the working directory (CBIND-140); Android unchanged.
- EasyGL threading: the game thread holds the GL context for Initialize/BeginRun/each Tick/EndRun; texture/buffer/render-target constructors, SetData/GetData/Dispose take a context lease on any thread (EasyGL only — do not generalise); a game thread that waits inside LoadContent/Update/Draw for a worker creating GPU resources deadlocks. Several threads may create/destroy devices at once.
- Input: `GamePad::setKeyboardEmulationEnabledEXT(true)` (player one, off by default); `Accelerometer::setKeyboardEmulationEnabledEXT`; ClientBounds X/Y is the desktop position and a fullscreen window reports the back-buffer size; the browser emulates `Mouse::SetPosition`; Android Back arrives as Escape and as player one's Back.
- XNA-fidelity exceptions: `ContentLoadException` derives from `System::Exception`; a wrong-type XNB is a ContentLoadException; Game timing setters throw `ArgumentOutOfRangeException`; GameComponentCollection throws XNA's exceptions; no Update runs after `Exit()`; a device failure in Game's constructor is `NoSuitableGraphicsDeviceException`; audio argument validation follows XNA.
- Android (emulator evidence only): lifecycle events delivered, IsActive follows lifecycle, .cnb loads from the APK, portrait games run in portrait.
- Compiled effects: FX-140..146 GLSL/GLSL ES fixes (686/686 compiled-effect tests on Mesa GLES 3.2, recorded in CNA); GLES vertex-sampler LOD bias emulated.
- XACT: `BuildXact` drives the real XactBld3 (`/WINDOWS` or `/XBOX360`) through Wine path mapping (`CNA_XACTBLD`, `CNA_XACTBLD_LAUNCHER`).
- glTF skinning: a skinned mesh ignores its node transform, as the glTF spec says.

## 8. Ecosystem numbers
C++ samples (cna-samples 5db32e6, 2026-10-03): 153 is the SAMPLE-001..153 audit universe, not 153 games; 91 complete, 8 relevant XNA 4.0 C# programs remain, 54 are not port targets (XNA 3.x or older, Silverlight, WinForms tools, VB.NET, C++, asset packs, platform services, duplicates). Racing Game Kit: separate plan, not counted in the 91, C++ port feature-complete on Linux, not hosted. samples.libcna.com (b3939de): 90 playable C++ browser builds. CNA.NET samples (cna-cs-samples 1e6d763): 83 Microsoft XNA 4.0 sample projects (84 programs) from byte-identical upstream C# run on Linux, in headless Chromium and on the x86_64 Android emulator; 83 of the 91 C++ ports also run as unchanged C#.

## 9. Pinned CNA source links
Links look like `https://github.com/libcna/cna/blob/009d40f5dd085c4e674d3479675fac84b12b3e0a/<path>` (or `/tree/`). For every link whose <path> does not exist at T (listed in page-worklist.txt under "missing paths at T"; verify with `git -C ../cna cat-file -e T:<path>`): find where it went (`git -C ../cna log --oneline --diff-filter=DR -1 O..T -- <path>`, renames via `git -C ../cna diff --find-renames --name-status O T -- <dir>`), then either point the link at the current path (keep the old SHA in the URL; the orchestrator swaps it) or, when the subject is gone, remove the link and the claim. For identifiers listed as gone/moved, check the claim against T and correct it. Don't re-pin.

## 10. Verification per page
After editing a page: it must still parse (`python3 -c "import html5lib,sys;html5lib.HTMLParser(strict=False).parse(open(sys.argv[1]).read())" PAGE` or the per-area checker: `python3 scripts/check_dev_page.py PAGE` for development pages — ignore its pinned-link/snapshot complaints until re-pin; `python3 scripts/check_deep_page.py PAGE` for deep-dives), and `python3 scripts/check_retired_renderers.py | grep '^PAGE:'` must be empty.
