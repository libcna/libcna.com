# R3 — CNA C ABI: O `009d40f5` (0.29.0) → T `b0e97bb1` (0.44.0)

Evidence classes used below: **[S]** source (git objects at a pin) · **[B]** build claim · **[R]** runtime-qualified (a commit message or sibling README reports a local run; not CI, not reproduced here) · **[P]** platform-qualified · **[C]** compatibility result · **[F]** future plan. Nothing was built or run for this report.

## Executive summary (15 lines)

1. [S] `abi.h`: 0.29.0 (`0x00001D00`) at O → **0.44.0** (`0x00002C00`) at T. 15 minors (0.30–0.44) in 456 commits, 2026-09-27 … 2026-10-03.
2. [S] Exports 4,055 → **3,210** = −842 (MOD-RETIRE-1: `engine_layer.h` −858, `graphics_ext.h` +16) −11 (avatar EXT) −2 (Guide setters) +10 new routes. Strict `check_declared_exports.py` regex: declared = baseline set, empty diff both ways, at O (4,055) and T (3,210).
3. [S] Baseline at T: 3,210 exports · 197 structs (−24) · 295 scalars (−55) · 1,466 integer constants (−92) · 14 strings · 141 colours. Headers 61 → **60**.
4. [S] 0.30–0.35 are **breaking** (engine-layer deletion; renderer constants retired twice; Guide/Dispatcher rule changes; avatar EXT and two Guide setters removed; a two-line 0.33 collision merged as 0.35). 0.36–0.39 and 0.41 are **purely additive** (+1/+4/+1/+1/+1 routes). 0.40, 0.42, 0.43, 0.44 are **rule-only** (export set unchanged; a previously refused call is now accepted).
5. [S] Threading model is no longer strictly "creation thread only": opt-in foreign-thread call queue (0.39) and a way to drain it while the game thread waits (0.41); `cna_sound_effect_play*` on any thread (0.43); device borrowable before the run (0.42) and in Activated/Deactivated handlers (0.44); adapters answer the game handle (0.40).
6. [S] New host-driven loop `cna_game_run_frame_ext` (0.38) delivers begin_run/end_run/exiting (the old `cna_game_run_one_frame` never did). New canonical-exception queries (0.37), `cna_packet_reader_copy_data_ext` (0.36).
7. [S/R] Platforms: Android NDK configure/build without libcurl (CBIND-136; service/relay then refuse); Emscripten static C archive (CBIND-135, linked by cna-cs into `dotnet.native.wasm`); threaded browser builds where the game thread is a worker (CBIND-151; 64 MB initial memory, SDL patch 0004). Runtime evidence is commit-message / cna-cs reports only.
8. [S] CNA CI still builds **no** C library: 5 `c-api-*.yml` workflows remain build-free; no workflow sets `CNA_BUILD_C_API=ON` (18 workflow files at T, 20 at O).
9. [S] Release gate at T: "CNA C ABI 0.44.0, experimental", **Not ready**, 9/10 met, unmet = **656** unmapped public symbols (O: 468). Coverage: 469 headers, 8,142 symbols, 7,030 impl, 15 partial, 656 planned, 441 n/a (O: 556 / 9,355 / 8,363 / 15 / 468 / 509).
10. [S] The scope-table defect the site describes (design/diagnostics/inspector unclassified; CNA-BUG-062) is **fixed in source** at `5572f3ca1`; gate `--check` not re-run here.
11. [S] Consumer story unchanged: `-DCNA_BUILD_C_API=ON` (requires `CNA_ENABLE_NET=ON`), `cmake --install … --component CNACApi`, `find_package(CNA 0.1 CONFIG REQUIRED)`, `CNA::CApi` / `CNA::CApiStatic`, `modules/c-api/examples/c/hello_cna.c` (354 lines). Matrix: 23 cells / 7 toolchains, 61 TUs per cell.
12. [C] cna-cs `develop@860f92c` (2026-10-04): exact-match policy, accepts **only 0.44.0**; CI pins CNA `ed885a8ae`; headers + baseline at T are byte-identical to `ed885a8ae` ⇒ T's version would be admitted (inference, not run). README: 1,419 imports, measured against CNA `8a7e13ff5` (ancestor of T).
13. [S] cna-c-template `develop@024c1f7` (2026-08-22) pins CNA `6bba5562` = **ABI 0.8.0** (2,862 exports) via `add_subdirectory`, no runtime ABI check, still pins retired FREE_DIRECT; not updated for 0.44.
14. Site: 227 grep lines in 60 files (incl. 4 in `data/current-facts.json`, 5 in `data/known-issues.json`; minus ~6 false positives: luminance `0.2126`), plus separately 23 lines/8 files under `known-issues/` and 14 in `search-index.json`. Every "0.29.0 / 61 headers / 4,055 / 221 / 1,558 / 350 / 468 / 9,355 / bindings pinned to 0.21.x / 0x00001D00 / engine_layer.h 858" statement is stale.
15. Needed new site content: threading section (foreign-thread queue + the four rule relaxations), host-driven run, exception-name queries, ABI history rows 0.30–0.44, Android/Emscripten-threads notes, cna-cs now at 0.44.0. Several CNA docs at T are themselves stale (CALLBACKS_AND_THREADING, CONSUMING "every minor additive", WASM_ARTIFACT loop/0.21.0, COMPATIBILITY "25 identities / no Android or web") — do not copy those.

---

## 0. Pins and method

| Item | Value |
|---|---|
| CNA O | `009d40f5dd085c4e674d3479675fac84b12b3e0a` (ABI 0.29.0) |
| CNA T | `b0e97bb1bb876f9b3edd6f4ff1ef3067908ae8ac` (ABI 0.44.0); `git rev-list --count O..T` = 456 |
| Route count method A | lines beginning `CNA_C_API` in `modules/c-api/include/CNA/C/*.h` (`git grep -c '^CNA_C_API' <rev> -- 'modules/c-api/include/CNA/C/*.h'`) |
| Route count method B | `DECLARATION = re.compile(r"CNA_C_API\s+[A-Za-z_][\w\s*]*?\b(cna_\w+)\s*\(", re.M)` from `tools/c-api/check_declared_exports.py`, run over `git show` blobs; compared with `abi_baseline.json["exports"]` |
| Results | O: A=4,055, B=4,055, baseline 4,055, B−baseline=0, baseline−B=0. T: A=3,210, B=3,210, baseline 3,210, both diffs 0. (Header-vs-baseline only; the tool's `nm -D` library half was not run.) |
| cna-cs | `develop` `860f92cca30f0862f6eabf7970269ce49af90536` (2026-10-04, "docs: point CNA links at libcna") |
| cna-c-template | `develop` `024c1f7aad2092c9ec8dc4862bd201c43a4ae3cc` (2026-08-22, "fix: harden CTest configuration contracts") |
| libcna.com | `develop` `df85d05d82abf8ffa39c5a02661eb2abb85946e3` |

## 1. ABI version history 0.30.0 → 0.44.0

Source: `docs/c-api/ABI_VERSIONING.md` at T (637 lines) + commit subjects/bodies; minor read from `abi.h`, counts from `tools/c-api/abi_baseline.json` at each commit.

| ABI | Commit (date) | Task | One-line meaning | Class | Exports | Other baseline deltas |
|---|---|---|---|---|---|---|
| 0.30.0 | `5572f3ca1` (09-27) | MOD-RETIRE-1 | `engine_layer.h` deleted (pipeline, post-process, clustered lighting, shadows, probes, optional PBR material routes, their handles/enums/layouts); ASCII, CRT, colour-depth, DebugDraw kept/moved into `graphics_ext.h` (28→44) | **Breaking** | 4,055→3,213 | structs 221→198, ints 1,558→1,473, scalars 350→295 |
| 0.31.0 | `0f96ea703` (09-27) | RRC-012 | retire renderer constants DIRECT2D 16, FREEDIRECT 21, PORTABLEGL 46; `CNA_GRAPHICS_RENDERER_MAXIMUM` 46→44; 25→22 identities | **Breaking** (constants) | 3,213 | ints →1,470 |
| 0.32.0 | `32c0002ff` (09-28) | GS-005b | +2 caller-buffer picture copies (`cna_achievement_copy_picture`, `cna_gamer_profile_copy_picture`); Guide/Dispatcher reflect configured service availability; unconfigured social/sign-in refuse; duplicate init → INVALID_STATE | **Breaking** (error/behaviour rules) + additive | 3,215 | — |
| 0.33.0 (`next`) | `261cb5f7f` (09-28) | RRC-015 | retire HTML_DOM 18, OPENGL4 33, GDI 40, SVG_DOM 44; MAXIMUM 44→43 (FNA3D); 18 identities; next new value still 52 | **Breaking** (constants) | 3,215 | ints →1,466 |
| 0.33.0 (`feature/gamer-services-server`) | `13dfe0499` (09-28) | GS-009f | Avatar real-rendering EXT removed: 11 routes + `CNA_AvatarAppearanceEXT`; `is_real_rendering_enabled` folded into `reserved[3]` (size/offsets kept) | **Breaking** | 3,204 | structs →197 |
| 0.34.0 (same line) | `39b037130` (09-29) | GS-011b | removed `cna_guide_set_is_visible`, `cna_guide_set_is_trial_mode` | **Breaking** | 3,202 | — |
| 0.35.0 | `df4c7a25d` (09-29) | merge | both lines used 0.33.0; merged ABI takes an unused number; holds all three changes; "a binding built against either earlier 0.33.0 or 0.34.0 must rebuild" | Breaking vs 0.32 | 3,202 | ints 1,466, structs 197 |
| 0.35.0 (correction) | `424c09f5c`, `39cbe801e` (09-30) | BINDFIX-048 | `CNA_CNB_SOUND_EFFECT_SCHEMA_VERSION` 1→2 with no version move (owner-approved 2026-09-30) | constant correction | 3,202 | 1 changed constant |
| 0.36.0 | `402c1aaa9` (10-01) | CBIND-130 | +`cna_packet_reader_copy_data_ext` (read a received packet's bytes) | **Additive** | 3,203 | — |
| 0.37.0 | `e9dd5d879` (10-01) | CBIND-132 | +4 routes: canonical .NET exception type name + ArgumentException param name of the last failure | **Additive** | 3,207 | — |
| 0.38.0 | `f445fef8c` (10-01) | CBIND-134 | +`cna_game_run_frame_ext`: host drives a run one frame per call | **Additive** | 3,208 | — |
| 0.39.0 | `0a57ccad2` (10-01) | CBIND-141 | +`cna_game_set_foreign_thread_calls_ext` (off by default): other threads' calls on game-thread handles queued to the game thread | **Additive** | 3,209 | — |
| 0.40.0 | `22b30b30e` (10-02) | CBIND-145 | rule: 12 `cna_graphics_adapter_*` routes accept the active game's own handle on its thread (refresh still refuses) | Rule change (widens) | 3,209 | none |
| 0.41.0 | `c77f983b1` (10-02) | CBIND-152 | +`cna_game_run_foreign_thread_calls_ext`: drain the queue now, while the game thread waits | **Additive** | 3,210 | — |
| 0.42.0 | `938a22069` (10-02) | CBIND-153 | rule: `cna_game_get_graphics_device` lends the device before the run begins, on the creating thread, until the first callback returns | Rule change (widens) | 3,210 | none |
| 0.43.0 | `23d7bad1e` (10-03) | CBIND-154 | rule: `cna_sound_effect_play` / `_play_with_settings` answer on any thread; every other sound-effect route keeps the creating-thread rule | Rule change (widens) | 3,210 | none |
| 0.44.0 | `ed885a8ae` (10-03) | CBIND-155 | rule: Activated/Deactivated handlers (`cna_game_subscribe`) run inside a callback scope (device borrowable); run-start activation holds the game thread's context | Rule change (widens) | 3,210 | none |

T (`b0e97bb1`) is 34 commits after `ed885a8ae`; `git diff ed885a8ae T -- tools/c-api/abi_baseline.json modules/c-api/include/` is empty [S].

**4,055 → 3,210 accounting** [S] (set diff of baseline `exports` O vs T: 855 removed, 10 added):

| Header | O | T | Δ | Cause |
|---|---:|---:|---:|---|
| `engine_layer.h` | 858 | — (deleted) | −858 | MOD-RETIRE-1 (0.30) |
| `graphics_ext.h` | 28 | 44 | +16 | retained retro effects moved in (ascii_post 8, crt_effect 11, debug_draw 15, depth_effect 5, image_based 2, indirect_draw 2, graphics_ext 1) |
| `gamer_services.h` | 250 | 239 | −11 | −11 avatar EXT (0.33 GS), −2 Guide setters (0.34), +2 picture copies (0.32) |
| `core.h` | 3 | 7 | +4 | exception queries (0.37) |
| `runtime.h` | 42 | 45 | +3 | run_frame (0.38), set/run foreign-thread calls (0.39, 0.41) |
| `net.h` | 50 | 51 | +1 | packet reader copy (0.36) |
| **Total** | **4,055** | **3,210** | **−845** | −858+16 = −842 (0.30); −13+2 (GS); +8 (CBIND) |

Removed by family prefix (top): clustered 102, pbr 67, light 55, render 44, depth 37, cube 28, cascaded 24, particle 24, post 23, gpu 22, shadow 21, … avatar 11. 24 struct layouts removed (23 engine-layer incl. `CNA_PbrMaterial`, `CNA_RenderPipelineSettings*`, `CNA_Particle*`, lights; + `CNA_AvatarAppearanceEXT`); 0 added. 92 integer constants removed (85 + 3 + 4), 0 added. Routes the site still cites that no longer exist at T: `cna_compute_shader_copy_compile_error`, `cna_post_process_chain_add_pass`, `cna_post_process_chain_add_owned_pass`, `cna_post_process_effect_pass_create_owning`, `cna_skybox_set_environment`, `cna_skybox_set_owned_environment`, `cna_decal_pass_is_supported`.

Policy text unchanged [S]: 0.x incompatible change ⇒ minor + notes + regenerated baseline; 1.x additive only; `find_package` version file `SameMajorVersion`; ABI 1.0 is a separate decision. CNA increments the minor for additive generations too.

## 2. What changed for C users and binding authors

| Area | ABI | What a C program / binding can now do | Limits stated in source | Evidence |
|---|---|---|---|---|
| Packet reader | 0.36 | Copy the bytes a native packet reader holds (inverse of `set_data_ext`); BUFFER_TOO_SMALL reports size, writes nothing; position untouched | — | [S] `net.h`; [R] NetSmoke.c, `^CApi 117/117` (commit) |
| Canonical exception | 0.37 | `cna_error_get_last_exception_type_size_ext`/`_copy_…_type_ext` → e.g. `System.ArgumentOutOfRangeException`, `Microsoft.Xna.Framework.GamerServices.GamerPrivilegeException`; `_param_name_*` for ArgumentException | A failure the C layer raises itself names none (sizes 0). Documented in `ERRORS.md` (+20 lines) | [S]; [R] NetSmoke.c |
| Host-driven run | 0.38 | `cna_game_run_frame_ext(game, &running)`: 1st call initializes + `begin_run`; each call one frame (Emscripten frame body on web); exit ends run with `exiting` then `end_run`; later calls report false. Also C++ `Game::RunFrameEXT()` (CNAEXT) | A failed callback ends the run in that call and returns CALLBACK. `cna_game_run_one_frame` unchanged (never begins/ends a run) | [S] `runtime.h:220-235`; [R] HostDrivenRunSmoke.c |
| Foreign-thread calls | 0.39 | `cna_game_set_foreign_thread_calls_ext(game, CNA_TRUE)` on the game thread: a call refused *only* because another thread created the handle is queued; caller blocks; game thread runs it at start of next update/draw inside callback scope (≤8 ms per step while calls arrive); caller gets result + error record | Off by default (CNA_RESULT_THREAD stays default); driving/destroying the game still refused; pending calls fail INVALID_STATE when disabled/destroyed; game thread waiting on such a thread deadlocks | [S] `runtime.h:237-259`; [R] ForeignThreadCallsSmoke.c, `^CApi|^Game|Lifecycle 437/437` |
| Adapters early | 0.40 | Pass the active game handle as `graphics_device` to the 12 `cna_graphics_adapter_*` routes, on its thread, before any callback (constructor-time `GraphicsAdapter.DefaultAdapter`) | `cna_graphics_adapters_refresh` still refuses | [S]; [R] GraphicsSurfaceSmoke |
| Drain queue while waiting | 0.41 | `cna_game_run_foreign_thread_calls_ext(game)` from the game thread while it joins a worker (XNA loading-screen pattern) | Returns at once if empty; runs calls arriving within 8 ms; no-op when feature off | [S] `runtime.h:261-276`; [R] smoke fails without the route body |
| Device before run | 0.42 | `cna_game_get_graphics_device` succeeds right after `cna_game_create` on the creating thread (constructor `ApplyChanges` pattern); handle lasts until first callback returns | Between frames after the run began: still INVALID_STATE | [S]; [R] LifecycleSmoke |
| Sound from any thread | 0.43 | `cna_sound_effect_play`, `cna_sound_effect_play_with_settings` on any thread (HandleRegistry `GetFromAnyThread`) | All other sound-effect routes keep creating-thread rule; `cna_dynamic_sound_effect_instance_submit_buffer` still thread-checked (BorrowDynamicInstance → registry Get) | [S] `audio.h:482-483`; [R] AudioSoundEffectSmoke |
| Activation handlers | 0.44 | Activated/Deactivated handlers can borrow the device (`OnActivated` pattern) | — | [S]; [R] LifecycleSmoke check 14 |
| Component handlers (no bump) | 0.35→ | CBIND-128: component C handlers run inside the lifecycle callback scope (can borrow device; cannot drive game). CBIND-129: component initialize handler runs before base LoadContent | "No export, layout or constant changed" | [S] `CALLBACKS_AND_THREADING.md` +4 lines; [R] RuntimeComponentDeviceBorrow.c |
| Concurrency/exit fixes (no bump) | — | BINDFIX-050: standalone devices created/destroyed on several threads at once; BINDFIX-041: process exit with a live game created on an ended thread no longer aborts | — | [S] ConcurrentDeviceCreationSmoke.c, ExitWithForeignThreadGameSmoke.c (registered tests) |
| Android NDK | CBIND-136 (`552a0d8cb`) | `cna_c_api` configures/builds for Android with the NDK alone: libcurl optional on Android → `CNA_SERVICE_TLS_TRANSPORT` undefined, service/relay refuse (`SERVICE_/RELAY_TRANSPORT_UNAVAILABLE`); JSON headers from host; opus probe skipped | Desktop still requires libcurl. Further Android runtime fixes CBIND-137/138/139, BL-13/19/21 found via downstream apps | [S]; [B][P] commit message only, no ctest numbers |
| Emscripten static archive | CBIND-135 (`1e7c4d323`) | `cna_c_api_static` (in ALL) now builds under Emscripten: closure from the wasm module's link line, archives merged by MRI script, no partial link/localization | "The cna-cs browser route links the resulting archive into dotnet.native.wasm as its only native file" | [S] `generate_static_archive.py`; [B] |
| Browser worker game thread | CBIND-151 (`cde2251fa`) | Threaded builds (`CNA_ENABLE_EMSCRIPTEN_THREADS=ON`, option pre-existing) run a game whose thread is a worker: 64 MB `-sINITIAL_MEMORY`, SDL patch 0004 commits proxied frames (`OFFSCREEN_FRAMEBUFFER`), WEBGL_polygon_mode probe tolerant, IDBFS ready flag read on page thread | Single-threaded builds unchanged | [S]; [R][P] headless Chromium: Enceladus, Missile Command, Racing Game Kit; "84-row single-threaded browser requalification passes" |
| Other wasm | BINDFIX-039/052/053, CBIND-143 | WASM C ABI builds again (libc++ ADL/override/link fixes); Game outlives a standalone device on WebAssembly (SDL patch 0003); MRT on WebGL 2; avatars load in single-threaded browser build | — | [S]; [R] BINDFIX-039: `CApi_WasmLinkContract`, `CApi_WasmModuleSmoke`, browser probe 11/11 (Chromium 151) |

**CNA documents at T that lag these changes (do not copy them onto the site):** `CALLBACKS_AND_THREADING.md` still states only the creation-thread baseline and "any later … main-thread-dispatch facility must state …" (no mention of 0.39/0.41/0.42/0.43/0.44); `CONSUMING.md` step 3 "borrow the graphics device, which is legal only inside a callback" and line 63 "every minor within a major is additive" (contradicted by 0.30–0.35); `hello_cna.c` comment same; `WASM_ARTIFACT.md` §7 names `run_one_frame` as the browser loop and §10 "qualified artifact answered 0.21.0" (file unchanged O..T); `COMPATIBILITY.md`/`LIMITATIONS.md` "CNA has 25 renderer identities", "Four of the 49 renderers", "macOS, iOS, Android and the web targets: no toolchain … no cell"; `README.md`/`FEATURE_MATRIX.md` still "0.1.0" (CNA-BUG-056); `audio.h:668` still calls submit_buffer producer-thread safe (CNA-BUG-213).

## 3. Consumer documentation at T

`docs/c-api/` — 40 files, list unchanged O→T [S]: ABI_VERSIONING, AUDIO, CABI_BLOCKER_HANDOFF, CALLBACKS_AND_THREADING, CNB, COMPATIBILITY, CONSUMING, CONTENT, CORE, COVERAGE, COVERAGE_AUDIT, DEVICES, EFFECTS, ERRORS, FEATURE_MATRIX, FUZZING, GAMER_SERVICES, GAME_COMPONENTS, GRAPHICS_DEVICE, GRAPHICS_EXT, GRAPHICS_RESOURCES, HANDLES, INDEX_BUFFERS, INPUT_SNAPSHOTS, LIMITATIONS, MATH_AND_3D_VALUES, MEDIA, MODELS, NET, OWNERSHIP, README, RELEASE_GATE, RENDERERS_AND_CAPABILITIES, SHARP_RUNTIME_BOUNDARY, STORAGE, STRINGS_AND_BUFFERS, TEXTURES, TEXTURE_VOLUMES, VERTEX_BUFFERS, WASM_ARTIFACT (.md). Changed O..T: ABI_VERSIONING (+204), GAMER_SERVICES, NET, COVERAGE, ERRORS (+20, exception queries), FEATURE_MATRIX, GRAPHICS_EXT (−58 net), LIMITATIONS, RELEASE_GATE, CALLBACKS_AND_THREADING (+4), README, CONSUMING (4,055→3,210), COMPATIBILITY, CABI_BLOCKER_HANDOFF.

| Topic | Fact at T | Source |
|---|---|---|
| Configure option | `option(CNA_BUILD_C_API "Build the experimental native CNA C API shared library" OFF)`; `CNA_BUILD_C_API=ON requires CNA_ENABLE_NET=ON` (FATAL_ERROR) | `CMakeLists.txt:80,187-189` |
| Static archive | `option(CNA_C_API_BUILD_STATIC "Build and install the static C API archive" ON)`; `CNA_ENABLE_IPO` cannot package it | `modules/c-api/CMakeLists.txt:350`; `cmake/BuildPerformance.cmake:439` |
| Presets | all three `CMakePresets.json` presets set `CNA_BUILD_C_API` OFF (lines 29, 56, 93) | [S] |
| Install | `cmake --install <cna-build-dir> --component CNACApi --prefix /opt/cna` (component = one shared lib, headers, CMake package, SDL3 libs beside it; RPATH `$ORIGIN`) | `CONSUMING.md` |
| Consume | `find_package(CNA 0.1 CONFIG REQUIRED)` + `target_link_libraries(my_game PRIVATE CNA::CApi)`; `CNA::CApiStatic` defines `CNA_C_API_STATIC`; no-CMake: `cc -std=c99 -I/opt/cna/include main.c -L/opt/cna/lib -lcna_c_api` | `CONSUMING.md` |
| Package version | = C ABI version read from `abi.h` at configure; `SameMajorVersion` | `CONSUMING.md`, `ABI_VERSIONING.md` |
| Example | `modules/c-api/examples/c/hello_cna.c` (354 lines, unchanged), built by `CApi_InstalledConsumer` from an installed prefix, shared and static | [S] |
| Release gate | "CNA C ABI 0.44.0, experimental"; **Not ready**, 1 of 10 unmet: "656 public symbols are still unmapped"; met rows: 23 cells / 7 toolchains; 197 struct layouts + 3210 exports; limitations "15 partially mapped symbols in 9 groups, 441 unmapped in 86 groups"; hello_cna consumer; package; 13 docs present; stress/oracle/fuzz present; SDL3 ships; static archive. Still says "654 … CBIND-117" (CNA-BUG-058) | `RELEASE_GATE.md` |
| Compatibility matrix | 7 toolchains: `cc` c99/c11/c17 (req), `c++` c++11/14/17 (req), `gcc` c99–c23, `g++` c++17/20/23, `clang` c99–c23, `clang++` c++17/20/23, `x86_64-w64-mingw32-gcc` c99/c11/c17 (headers only) = 23 cells; 61 TUs per cell (O: 62); run configs headless / sdlrenderer / software / asan (SOFTWARE+ASan/UBSan) | `COMPATIBILITY.md` |
| Limitations | 8,142 declarations: fully 7,030, partial 15, no C form 441 (17 themes); non-symbol: FFmpeg system dep, static archive keeps STB_GNU_UNIQUE statics, one runtime per process, thread-affine handles, ABI 0.x experimental, compiled effects never accepted in the 4 trees | `LIMITATIONS.md` |
| Coverage | 469 headers, 8,142 symbols, 7,030 impl, 15 partial, **656 planned**, 441 n/a, 471 excluded. Planned by module: graphics 275, content 206, graphics-ext 40, input 30, gamer-services 29, math 27, runtime 19, net 15, audio 10, devices 2, storage 2, media 1. `coverage_mappings.json` 628 rules (O 693) | `COVERAGE.md` |
| Tests | 93 pure-C sources (O 85; +AvatarExitWhileLoading, ConcurrentDeviceCreation, ContentModelEffect, ExitWithForeignThreadGame, ForeignThreadCalls, HostDrivenRun, RendererEnvironment, RuntimeComponentDeviceBorrow, ServiceClient; −EngineLayerSmoke); 4 C++ (−CubeLutOracleTest); 1 fuzz source (StringViewFuzz; −CubeLutFuzz); 104 `add_test` in `modules/c-api/CMakeLists.txt` (O 98); 12 `CApi*` probes in `ModuleProbes.cmake` (unchanged); 59 `CnaCApi*.cpp` units (EngineLayer→DebugDraw); include+src 144,896 lines (O 178,863) | [S] |
| CI | 5 `c-api-*.yml` (abi-baseline, compat-matrix, coverage-gate, limitations, release-gate), build-free; no workflow references `cna_c_api`/`CNA_BUILD_C_API=ON`; `general-tests-ci.yml` only installs gcc-14 for `CApiHeaderCompatibility` | [S] |
| Local run claims | commits CBIND-145/152/153/154/155: `^CApi 119/119`, "C API gates 9/9"; df4c7a25d: `ctest -R '^CApi' 107/110` | [R] |
| Renderer identities | `CNA_GRAPHICS_RENDERER_MAXIMUM` = `FNA3D` (43); 18 public identities; reserved `7, 10, 16, 18–21, 23–30, 32–41, 44–51`; next 52. `CNA_RENDERER_FEATURE_MAXIMUM` unchanged (31) | `graphics.h`, `ABI_VERSIONING.md` |
| cnb.h | 272 routes (unchanged) | [S] |

## 4. Downstream pins

| Repo (branch@HEAD) | ABI it requires/admits | Mechanism | Notes |
|---|---|---|---|
| cna-cs `develop@860f92c` (2026-10-04) | **exactly 0.44.0** (`ConsumerVersion = (0<<16)|(44<<8)|0`); every other 0.x and any 1.x rejected | `src/CNA.Interop/CnaNativeAbiPolicy.cs` (policy `cna-cs-native-abi/1`, point matrix, never a range), `NativeLibraryResolver.cs` calls `cna_get_abi_version` then verifies all imports + 3 runtime canaries; `eng/cna-native-abi-policy.json` `consumerAbi: "0.44.0"` | Retired: 0.6, 0.7, 0.8, 0.19, 0.20, 0.21, 0.35–0.43. Evidence row: CNA `next` `ed885a8ae`; baselinediff 0.43→0.44: 1,416 consumed, 0 absent/changed; 3210→3210. `docs/native-abi-compatibility.md`: consumed 1,419; abi-verify 1,137 layout values, 0 mismatches, 23 callbacks, 604 constants; fixtures 2 accepted / 10 rejected. CI `.github/workflows/build.yml:18` `CNA_UPSTREAM_COMMIT: ed885a8ae…` and runs native tests against a **prebuilt** `libcna_c_api.so` from a secret (line 313), not a source build. README: "targets CNA C ABI 0.44.0", measured 2026-10-04 against CNA `8a7e13ff5`, Linux x64 OPENGLES3: native integration 260/260, framework 653/653, XNA-compat 319/319 [C][R][P]. Stale comment: `src/CNA.Framework/CnaAbi.cs:18` still says "= 0.6.0" (constant itself = ConsumerVersion). |
| cna-c-template `develop@024c1f7` (2026-08-22) | CNA `6bba5562d66b2005057569373843be6c843ec8f1` (2026-08-22) ⇒ **ABI 0.8.0**, 2,862 exports | `dependencies.lock` + `cmake/CnaDependencyPin.cmake` (HEAD/worktree checked; `CNA_ALLOW_UNPINNED=ON` to override); consumes CNA via `add_subdirectory`, links shared `CNA::CApi`, forces `CNA_C_API_BUILD_STATIC=OFF`; **no `cna_get_abi_version` check** in game code | Lock still names `openeggbert/*` repos and pins FREE_DIRECT (renderer retired in 0.31.0); `docs/compatibility.md` records an NDK 29 blocker at the pinned CNA (`AudioCategory` mismatched tags). Not updated since 2026-08-22; 2,614 commits behind O. Site does not mention cna-c-template. |

## 5. libcna.com impact

Grep `0\.29\.0|0\.21|4,055|4055|61 public|61 headers|engine_layer|ABI 0\.` (excl. audit/ scripts/ .git known-issues/ build-probe/ search-index.json sitemap.xml): **227 lines / 60 files**; false positives: `docs/tutorials/24-post-processing.html:169,304`, `66-bloom.html:225`, `151-one-shader-several-renderers.html:111,150` (GLSL `0.2126`), `historical/index.html:58` (historical PDF note, correct as is). Supplementary grep for `221 struct|1,558|350 scalar|9,355|8,363|468|509|0x00001D00|83 groups|85 pure-C|CUBE-LUT|2 libFuzzer|858` adds the rows marked †.

Corrected values to use everywhere: ABI **0.44.0** (`0x00002C00`); **60** headers; **3,210** routes/exports; baseline **197 / 295 / 1,466 / 14 / 141 / 3,210**; coverage **469 / 8,142 / 7,030 / 15 / 656 / 441** (471 excluded); gate Not ready, **656** unmapped; renderer MAXIMUM **43**, 18 identities; tests **93 / 4 / 1**; cna-cs **0.44.0 exact**.

### 5a. Key pages

| File:line | Current claim | Correct at T | New content needed |
|---|---|---|---|
| docs/c-api.html:6,7,9 | meta: "ABI 0.29.0 with 61 headers and 4,055 routes"; bindings incl. 0.21 | 0.44.0 / 60 / 3,210 | — |
| docs/c-api.html:59 | "declared C ABI 0.29.0 · … not built by any CI workflow" | 0.44.0; CI claim still true | — |
| docs/c-api.html:61 | callout: 468 unmapped | 656 | — |
| docs/c-api.html:66–71 | 0.29.0 `0x00001D00`; 61 headers "(adds cnb.h and engine_layer.h)"; 4,055 routes; baseline 221/350/1,558/14/141/4,055; inventory 9,355 in 556; gate 1 unmet (468), re-run 2 unmet | 0.44.0 `0x00002C00`; 60 (alpha.1 59 + `cnb.h`; `engine_layer.h` added after alpha.1, deleted in 0.30.0); 3,210 (set-equal to baseline); 197/295/1,466/14/141/3,210; 8,142 in 469; committed 1 unmet (656); scope defect fixed at `5572f3ca1` (re-run not done) | — |
| docs/c-api.html:76–85 | "table has 25 rows against 25 canonical identities"; 85–90% build estimate; 4,055 names match | 18 identities (MAXIMUM FNA3D 43); estimate/numbers stale; CNA commits now report local `^CApi 119/119` [R] | rewrite as historical |
| docs/c-api.html:87–110 | build/package table and commands | still valid (option names, `CNACApi`, `CNA::CApi`, `CNA::CApiStatic`, `CNA_C_API_BUILD_STATIC`, `find_package(CNA 0.1 CONFIG REQUIRED)`) | add Emscripten static archive (CBIND-135), Android NDK build (CBIND-136, service/relay refuse) |
| docs/c-api.html:111 | WebAssembly artifact paragraph | still valid for single-threaded | add threaded/worker builds (CBIND-151), `cna_game_run_frame_ext` for rAF hosts |
| docs/c-api.html:115,124 | identity table 0.29.0; "two minor steps since alpha.1 (0.28.0 and 0.29.0) were incompatible" | 0.44.0; incompatible since alpha.1: 0.28, 0.29, 0.30, 0.31, 0.32 (rules), 0.33 ×2, 0.34, 0.35; rule-only 0.40/0.42/0.43/0.44 | — |
| docs/c-api.html:126–134 | history table ends at 0.29.0; link to ABI_VERSIONING at 009d40f5 | add rows 0.30–0.44 (table §1); link to T | **new rows** |
| docs/c-api.html:136–138 | MAXIMUM "currently 46", 25 identities, `PORTABLEGL` 46 example | 43 (FNA3D), 18; PORTABLEGL retired/reserved | — |
| docs/c-api.html:146–148 | Callbacks row: device only in callback; Threading row: creation thread only, wrong thread → THREAD; Failures row | add 0.39/0.41 opt-in queue, 0.42 device before run, 0.43 sound play any thread, 0.44 activation handlers, CBIND-128 component handlers; failures: + exception type/param queries (0.37) | **new threading subsection** |
| docs/c-api.html:154–158 | 61 headers; largest: engine_layer.h 858, gamer_services.h 250 | 60; top 8 at T: effects 290, cnb 272, gamer_services 239, models 216, media_library 148, sensors 144, vectors 137, net_sessions 104 | — |
| docs/c-api.html:168,214 | Tutorial 129 "against ABI 0.29.0" | 0.44.0 | — |
| docs/c-api.html:171–173† | 556/9,355/8,363/15/468/509; 425 excluded; "re-running … fails earlier" | 469/8,142/7,030/15/656/441; 471 excluded | — |
| docs/c-api.html:178–182† | "85 pure-C programs, 5 C++ tests, 2 libFuzzer … CUBE-LUT oracles"; plan ctest 111 tests 2026-09-18 | 93 / 4 / 1 (no CUBE-LUT); latest commit-reported `^CApi 119/119` [R] | — |
| docs/c-api.html:189–197 | all bindings target 0.21.x; cna-cs `e223909` 0.21.0 "refuses" 0.29.0 | cna-cs `860f92c` (2026-10-04) exact 0.44.0; CI pin `ed885a8ae`; T headers/baseline identical ⇒ admitted by version (inference). cna-java/cna-ts not re-checked here | update table |
| docs/c-api.html:203–210 | column "with a 0.29.0 library"; `0x00001D00 for 0.29.0` | "with a 0.44.0 library"; `0x00002C00`; cna-rust still declares a route absent at T | — |
| docs/c-api.html:213 | 468 unmapped, 509 no-C-form "in 83 groups"; "two incompatible minor steps"; Android not verified | 656; 441 (gate: 86 groups; LIMITATIONS: 17 themes); many; Android build claimed by CBIND-136 [B], runtime only via downstream [R]; CNA's COMPATIBILITY.md still has no Android/web cell | — |
| docs/c-api.html:220,222,233,234,241,242 | related-link blurbs 0.29.0; CNA-BUG-056/058/270, GAP-062 | 0.44.0; BUG-270 obsolete (routes deleted); 468→656 | — |
| docs/releases.html:210,235,243 | "0.29.0: 61 headers, 4,055 routes"; "0.29.0 at snapshot 009d40f5"; incompatible 0.28/0.29; bindings "pin … 0.21.x" | 0.44.0 / 60 / 3,210 at T; incompatible list as above; cna-cs pins 0.44.0 | — |
| docs/roadmap.html:178,256,289† | 0.29.0/61/4,055; gate 468 + 509, re-run 2 unmet (scope table, CNA-BUG-062); bindings 0.21.x; "burning down its 468" | 0.44.0/60/3,210; 656 + 441; scope fixed in source; cna-cs 0.44.0; 656 | [F] items stay future |
| roadmap.html:248† | 0.29.0, 61, 4,055, 221 layouts, 468/9,355/8,363/15/468/509, re-run 2 unmet, 0.28/0.29 incompatible, bindings 0.21.x | 0.44.0, 60, 3,210, 197, 656 / 8,142 / 7,030 / 15 / 656 / 441; incompatible steps 0.30–0.35 too | — |
| features.html:880–883† | "ABI 0.29.0"; 61 headers, 4,055 routes "(engine layer alone is 858)"; baseline 221/4,055; inventory 9,355…; scope-check note | 0.44.0; 60, 3,210; engine layer gone; 197/3,210; 8,142/7,030/15/656/441; scope fixed | add frame stepping / foreign-thread line |
| index.html:108,111,412 | "C ABI (0.29.0…)", bindings "currently 0.21.x"; CNA.NET "pinned to ABI 0.21.x … this snapshot exports 0.29.0" | 0.44.0; cna-cs 0.44.0 exact (matches T) | — |
| about.html:120 | 0.29.0, 61 headers, 4,055 routes | 0.44.0, 60, 3,210 | — |
| architecture.html:243,531 | "C ABI 0.29.0" | 0.44.0 | — |
| documentation.html:96,128 | 0.29.0; 61 headers, 4,055 routes | 0.44.0; 60; 3,210 | — |
| docs/building.html:459,546† | "(ABI 0.29.0 …)"; 468 unmapped; "bindings pin an exact ABI" | 0.44.0; 656 | — |
| docs/verification.html:192,213,420,521† | baseline 221/4,055; "9,355 C API symbols"; 468; 556/9,355/…; re-run 8/10 | 197/3,210; 8,142; 656; 469/8,142/7,030/15/656/441; committed 9/10 | — |
| docs/faq.html:181 | bindings "pinned to … (0.21.x) than this snapshot exports (0.29.0)" | cna-cs 0.44.0 | — |
| docs/cnaext-engine.html:237,498 | "`engine_layer.h` declares its routes in every build … NOT_SUPPORTED"; ABI 0.29.0 | `engine_layer.h` deleted in 0.30.0 (MOD-RETIRE-1); only retro routes remain in `graphics_ext.h` (44) | coordinate with engine-layer agent |
| docs/runtime-renderer-selection.html:138,153 | ABI 0.29.0; MAXIMUM 46; "outside the 25" | 0.44.0; 43; 18 | — |
| docs/rendering-backends.html:661 | "(ABI 0.29.0 …)" | 0.44.0 | — |
| docs/cnb-format.html:512 | "0.29.0 … 272 `cna_cnb_*` routes" | 0.44.0; 272 still correct | — |
| docs/tutorials/129-c-api-first-program.html:7,12,18,55,59,61,257,262,272,290,293 | ABI 0.29.0; "two minor steps (0.28.0, 0.29.0)"; run vs run_one_frame only; sample output "CNA C ABI 0.29.0"; 61/4,055; 9,355/8,363/468/509 | 0.44.0; incompatible list; mention `cna_game_run_frame_ext`; output 0.44.0; 60/3,210; 8,142/7,030/656/441. Code itself uses no removed route | small "threads" note |
| docs/tutorials/133-renderer-capability-profile.html:444 | C ABI 0.29.0 | 0.44.0 | — |
| docs/tutorials/146-cnb-packs.html:429 | 0.29.0, 272 routes | 0.44.0, 272 | — |
| docs/tutorials/81-emscripten.html:198 | "`Game::RunOneFrame()` … as the experimental C API's WebAssembly build does" | also `Game::RunFrameEXT()` / `cna_game_run_frame_ext` (0.38) for host-driven runs with begin/end | — |
| tutorials 155/156/157 (`155-diagnostics-stats.html`, `156-inspector-live.html`, `157-cna-tools-tour.html`) | no C ABI claims (only snapshot 009d40f5 references) | — | — |
| tutorials.html:1395 | title "Inspect the Experimental C API Boundary" | page's own title is "Your First C Program Against the Experimental C API" (pre-existing mismatch) | — |
| development/architecture/bindings.html:7,8,13,19,146,149,153,165,172–188,195,205,207 | 0.29.0; 61 headers; "85 pure-C programs, five C++ tests … two libFuzzer"; all bindings 0.21.x; "five of the eight refuse a 0.29.0"; "Removing a route (as 0.29.0 did for one)" | 0.44.0; 60; 93/4/1; cna-cs 0.44.0; 0.30–0.35 removed many | add foreign-thread rule to boundary checklist |
| development/internals/bindings/c-api-internals.html:7,13,19,147,218,227,280,288,308,309,318 | 0.29.0; run_one_frame/run/tick only; "outside a callback that route answers INVALID_STATE"; 85 pure-C | 0.44.0; + `run_frame_ext`; device also before run (0.42) and in activation handlers (0.44); 93; 59 units still correct | queue mechanism (CallWithExceptionBarrier queues refused foreign-thread calls) |
| development/internals/bindings/csharp.html:7,13,19,148,176,178,180–181,237 | cna-cs `e223909`, ConsumerVersion 0.21.0, 1,002 imports, README says 0.20.0/861 | `860f92c`: 0.44.0 exact, 1,419 imports, README says 0.44.0 | rewrite against new HEAD |
| development/internals/bindings/java.html:7,13,19,170,220; python.html:150,232–240 | "TARGET's ABI 0.29.0" | 0.44.0 (binding facts are per their own pins; not re-checked) | — |
| development/handbook/update-the-c-api.html:169,172,176,180,186,198,214–215,228,233–236,284,312–326 | 61 headers; baseline 221/350/1,558/4,055; "84 *Smoke.c … LUT oracles"; 509; (0, 29, 0); `0x00001D00`; history examples end 0.29; coverage 556/9,355/…; planned by module (content 188 …); 693 rules; re-run fails at scope check; bindings 0.21.x | 60; 197/295/1,466/3,210; 93 pure-C, 4 C++ (no LUT); 441; (0, 44, 0); `0x00002C00`; add 0.30–0.44 examples (incl. rule-only bumps); 469/8,142/7,030/15/656/441; planned by module per §3; 628 rules; scope fixed; cna-cs 0.44.0 | rule-only version bumps as a category |
| development/handbook/make-a-release.html:176 | "0.29.0, experimental" | 0.44.0 | — |
| development/handbook/update-libcna-com.html:216–217 | facts row "C ABI (0.29.0), headers (61), routes (4,055)"; bindings 0.21.x | 0.44.0 / 60 / 3,210; cna-cs 0.44.0 | — |
| development/handbook/change-public-xna-behavior.html:232; change-map.html:217; workflows.html:166 | bindings 0.21.x vs 0.29.0 | 0.44.0 | — |
| development/debugging.html:207,262 | cites `cna_compute_shader_copy_compile_error`; 0.29.0 `0x00001D00` | route removed in 0.30.0; `cna_shader_effect_copy_compile_error_ext` still exported at T; 0.44.0 `0x00002C00` | — |
| development/repository/index.html:224,241; source-ownership.html:366; internals/modules/storage.html:225 | 0.29.0; 61 headers | 0.44.0; 60 | — |
| development/takeover/{uncertainty:164–165,179; blast-radius:169; investigation:188; inherited:155; index:195; mental-model:194; worked-changes:199; own-a-subsystem:206} | 0.29.0, 61 headers, 4,055; "c-api has 178,863 lines"; bindings 0.21.x; cna-cs e2239099 0.21.0 | 0.44.0, 60, 3,210; 144,896 lines (same method); cna-cs 0.44.0 | — |
| development/reference/public-headers.html:162,176 | generated from 009d40f5 | regenerate at T | — |
| deep-dives/reference/native-c-api.html:7,13,19,128,135,140,142,152 | 0.29.0, `0x00001D00`, "all 61 headers"; admission table columns "Headers 0.21.0, library 0.29.0 / Headers 0.29.0, library 0.28.0"; 0.29.0 removal example | 0.44.0, `0x00002C00`, 60; columns re-based (e.g. 0.36→0.44, 0.44→0.43); removal examples 0.30/0.33/0.34; note rule-only bumps pass link check but change accepted calls | — |
| deep-dives/reference/native-c-api.html:211 | "No route at 009d40f5 provides a deferred-release or main-thread dispatch queue … must hand the work to the creation thread itself" | **False at T**: opt-in queue `cna_game_set_foreign_thread_calls_ext` (0.39) + `cna_game_run_foreign_thread_calls_ext` (0.41); sound play any-thread (0.43). submit_buffer still thread-checked by default | **new section** |
| deep-dives/reference/native-c-api.html:223 | three engine-layer ownership-transfer routes | all three deleted in 0.30.0 | rewrite/remove |
| deep-dives/reference/native-c-api.html:248–260 | "The 4,055 routes by family"; Core 61, Runtime 139, CNAEXT engine layer 886, Services 486 | 3,210; Core 65 (core.h 7), Runtime 142 (runtime.h 45), "Graphics extensions" 44 (`graphics_ext.h` only), Services 476 (gamer_services 239, net 51); others unchanged (Math 444, Graphics 267, Effects+models 506, Content 366, Audio 136, Media 270, Input 288, Devices+sensors 206) | — |
| deep-dives/reference/c-api-evidence-and-gates.html:7,13,19,144,148,150,211,215,247,253,265,269,270† | 0.29.0; 61 headers, 4,055 routes, 59 units; 85/5/2; bindings 0.21.x; scope check stops gate; totals 556/9,355/…; "say ABI 0.29.0 …" | 0.44.0; 60, 3,210, 59 ✓; 93/4/1; cna-cs 0.44.0; scope fixed in `5572f3ca1`; 469/8,142/7,030/15/656/441 | — |
| deep-dives/reference/{glossary:142; index:130–131; ecosystem-quick-reference:8,198}; foundations/cna-and-xna:203,208; practice/project-records-and-evidence:152,177,193†; reference/verification-tiers:240† | 0.29.0; "every one targets the 0.21 ABI generation"; "468 unmapped" | 0.44.0; cna-cs 0.44.0; 656 | — |
| development/testing/architecture.html:345,380; reference/test-targets.html:142 | link blurbs "C ABI 0.29.0" | 0.44.0 | — |
| data/current-facts.json:109,115–121,151–152 | `c_abi_version` "0.29.0", `c_api_headers` 61, `c_api_routes` 4055, `bindings_expected_abi` "0.21.x"; `bindings_pins.cna-cs` e223909 | "0.44.0", 60, 3210; cna-cs 0.44.0 @ 860f92c | — |
| img/architecture-diagram.svg:171 | "Inspector · experimental C ABI 0.29.0" | 0.44.0 | — |
| search-index.json | 14 matching strings | regenerate | — |
| contribute.html:258 | "20 workflow files … five C API header gates" | 18 files at T; still 5 C API gates | — |

### 5b. Known-issues (counted separately)

`known-issues/**`: **23 lines in 8 files** (incl. pager/index links; CNA-BUG-269/271 hits are only neighbour-page links); `data/known-issues.json`: 5 lines (counted in the main 227).

| Issue | Site status | State at T |
|---|---|---|
| CNA-BUG-056 (FEATURE_MATRIX/README say 0.1.0 vs abi.h 0.29.0) | narrowed | still present; title should say 0.44.0 [S] |
| CNA-BUG-058 (LIMITATIONS omits 468 planned; RELEASE_GATE "654 … CBIND-117") | narrowed | still present; 656 planned [S] |
| CNA-BUG-062 (MODULE_SCOPE leaves design/diagnostics/inspector unclassified) | open | **fixed in source** `5572f3ca1` (generate_coverage_inventory.py:91–93; COVERAGE.md lists them out of scope) |
| CNA-BUG-213 (submit_buffer "producer thread safe" but THREAD) | open | still present by default (`audio.h:668`, BorrowDynamicInstance thread-checked); with 0.39 opt-in the call is queued rather than refused |
| CNA-BUG-214 (SHUTTING_DOWN never returned) | open | unchanged (only in category switch `CnaCApiDetail.cpp:132`) |
| CNA-BUG-270 (engine_layer.h @param lines) | open | **obsolete**: header and both routes deleted in 0.30.0 |
| CNA-GAP-062 (468 planned) | open | 656 planned |
| CNA-VGAP-053 (no CI builds C API) | open | still true |
| CNA-VGAP-055 (exit with live resources, creating thread ended, untested) | open | `CApi_ExitWithForeignThreadGameSmoke` registered (BINDFIX-041, `0f7166cd8`) — likely addressed; re-verify |

### 5c. Language-binding policy statements on the site (listed only)

index.html:108–113 ("actively maintains C, C#, Java and TypeScript bindings"; archived Rust/Python/Ruby/Swift/Go in CNA Lab); index.html:412 (CNA.NET); docs/faq.html:181; docs/c-api.html:187–210 (nine bindings; four maintained; five archived; tables); development/architecture/bindings.html:146,170–188,195; deep-dives/reference/ecosystem-quick-reference.html:198; features.html:883; docs/roadmap.html:256; roadmap.html:248; development/workflows.html:166; development/handbook/update-the-c-api.html:284; development/takeover/{investigation:188, blast-radius:169, mental-model:194, worked-changes:199, uncertainty:165}; data/current-facts.json:151–160 (`bindings_expected_abi`, `bindings_pins`).

## 6. Not verified / open

- No CNA build, `ctest`, `check_release_gate.py --check` or `check_declared_exports.py --library` run; all counts are from git objects.
- cna-java, cna-ts not present locally; their ABI pins were not re-read.
- Android/web runtime claims come from CNA commit messages and cna-cs reports (headless Chromium, Android emulator); CNA's own COMPATIBILITY.md at T has no Android/web cell.
- Whether T's library passes cna-cs's symbol/canary checks is inferred (identical headers/baseline to `ed885a8ae`), not executed.
