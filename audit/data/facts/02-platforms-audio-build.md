# Fact sheet 02 - platforms, audio, build system, CI, dependencies

- TARGET: CNA commit `009d40f5dd085c4e674d3479675fac84b12b3e0a` (read through the immutable worktree `/rv/tmp/libcna-v2/cna-target`).
- BASE: `1bb2145d99ed572dd4eb15009c34e2e5f410fcf0` (v0.1.0-alpha.1; worktree `/rv/tmp/libcna-v2/cna-base`).
- Range BASE..TARGET: 2,877 commits (`git rev-list --count`), 7,027 changed paths.
- Method: implementation, then CMake/headers, then test registration, then CI YAML. CNA's own Markdown was used only as a pointer and every claim below was re-checked in code. No configure/build/compile was run (rules of this task), so statements about what "configures" or "fails" are **static readings of the CMake logic**, and are marked accordingly.
- All paths are TARGET-worktree-relative unless prefixed `SITE:` (the libcna.com repository) or `BASE:`.
- Confidence: **H** = read directly in code/CMake/YAML; **M** = inferred from code plus one documented statement; **L** = weak or indirect.

Cross-reference numbering used inside this file (subsection numbers are kept): 1 = Verified facts (1.1 release/build baseline, 1.2 platform P#, 1.3 audio A#, 1.4 build B#, 1.5 CI C#), 2 = Platform matrix, 3 = Audio matrix, 4 = CMake options table (4.7 presets), 5 = Build/quickstart corrections, 6 = CI inventory, 7 = Corrections to existing site claims, 8 = New pages/sections warranted, 9 = Open questions.

## Headline findings (read first)

1. **TARGET is not a release.** `009d40f` is the tip of the `next` branch. `main` and `develop` of `libcna/cna` (and `openeggbert/cna`) still point at the alpha.1 commit `1bb2145`; the repository's default branch is `develop` (= alpha.1). TARGET still reports itself as `0.1.0-alpha.1` (`CMakeLists.txt:3,12`). Verified with `git ls-remote --symref` on 2026-09-24. Any quickstart that says `git clone https://github.com/libcna/cna.git` therefore gets alpha.1, not TARGET.
2. **TARGET needs sharp-runtime `next`, not its default branch.** `cmake/SharpRuntimeConsumption.cmake:33-38,60` adds the components `Resources` and `Xml.Serialization` (plus `Xml`, `ComponentModel`). sharp-runtime `main` (default branch, `54578590`) and `develop` (`df1b42ab`) contain no `modules/resources` and no `modules/xml-serialization`; only `next` (`41b918c9`) has them. `scripts/ci/clone_siblings.sh:5-9` records the same fact ("`next` asks for sharp-runtime components that exist only on sharp-runtime's own `next`"). H.
3. **Three native platform backends are new and real**: `CNA_PLATFORM=X11`, `WAYLAND`, `WIN32` (none is SDL). Two more selections became independent: `CNA_ENABLE_SDL=AUTO|ON|OFF` (SDL-free builds exist) and `CNA_AUDIO_PLATFORM=ALSA` (native Linux audio with CNA's own mixer). "SDL3 is the only real platform and SDL2/Headless/Terminal are the alternatives" is stale.
4. **`SOUND_ENABLED` is now defined for SDL3 *and* ALSA** (`modules/CMakeLists.txt:270-276`). SDL2 and NULL still have no mixer. H.
5. **FFmpeg is now optional** (`CNA_ENABLE_VIDEO=AUTO|ON|OFF`, default AUTO; `modules/CMakeLists.txt:8-58`). `Video`/`VideoPlayer` and the XNB `VideoReader` exist in every build; with no backend they throw `System::NotSupportedException` at run time instead of failing to link (`modules/media/src/Internal/VideoDecoderUnavailable.cpp:9-24`). H.
6. **Renderer set shrank from 50 to 25 public identities** (`cmake/RendererIdentities.cmake:25-38`), 21 families (`modules/CMakeLists.txt:441-444` list). Retired names are refused by name at configure time. This is outside this sheet's scope but it changes every build-option, platform-gate and CI statement on the site. H.
7. **Workflow files: 20 at TARGET vs 21 at BASE.** `[retired]-ci.yml` and `[retired]-cross-platform-ci.yml` deleted (their renderers were retired); `content-pipeline-windows-ci.yml` added. The alpha.1 "EASYGL" broken lanes are fixed (no invalid renderer identity remains in any workflow). **No workflow builds `CNA_PLATFORM=WAYLAND`**, and **no workflow builds with `CNA_BUILD_C_API=ON`**. H.
   **New defect class (static reading): nine jobs in eight workflows check out sharp-runtime at a stale pinned commit or at its default branch**, none of which contains the `Resources`/`Xml.Serialization` components TARGET requests (see C6). Only the lanes that use `scripts/ci/clone_siblings.sh` (which picks `next`) can satisfy the closure. M (not run).
8. **CMake presets: 17 visible configure presets + 1 hidden (18) and 17 build presets**, not "five". H.
9. **A build-layout default changed**: on native ELF GNU/Clang builds with CMake >= 3.27, `CNA_SHARED_LIBRARY` defaults ON and every executable links one `libcna.so` (`CMakeLists.txt:43-73`). H.

## Verified facts

### 1.1 Release, branch and build-baseline facts

| # | Claim | Evidence | Conf |
|---|---|---|---|
| F1 | Minimum CMake is 3.20; C++ standard is 23 with extensions off. No compiler-version check exists anywhere in CMake (`grep COMPILER_VERSION` finds only an unrelated Apple deployment check). | `CMakeLists.txt:1,21-23`; `modules/CMakeLists.txt:234` (`cxx_std_23`); `cmake/ApplePlatform.cmake:97` | H |
| F2 | The code base uses `<format>` unconditionally in the always-built content-pipeline module, which needs libstdc++ 13 / a current libc++ / MSVC 2022. So the "GCC 12+" minimum repeated on the site is not supported by the code. CI proves GCC 14 (Linux), AppleClang on macos-14, MSVC on windows-latest, mingw-w64 GCC, emsdk 6.0.3. | `modules/content-pipeline/include/Microsoft/Xna/Framework/Content/Pipeline/PipelineException.hpp:5`, `.../ContentBuildLogger.hpp:4`, `modules/content-pipeline/src/Xna/Serialization/Intermediate/IntermediateSerializer.cpp:10`; `.github/workflows/platform-ci.yml:74-75`; `.github/workflows/emscripten-multi-renderer-ci.yml:45`; `.github/workflows/apple-ci.yml:88,200` | H (usage) / M (exact floor) |
| F3 | Product version is still `0.1.0-alpha.1` at TARGET. | `CMakeLists.txt:3,12-18` | H |
| F4 | `cmake --build build --target CNA` still does not work: `CNA` is `add_library(CNA INTERFACE)`. Real targets: `CnaTests` (aggregate) plus 22 focused test targets, `cna_demo_2d`, `cna_house3d_demo`, `cna_content_tool` (output name `cna-content`), `cna_tool_*`. | `modules/CMakeLists.txt:382`; `cmake/UnitTests.cmake:439-460,478`; `modules/graphics/examples/CMakeLists.txt:52,153`; `cmake/ToolContentPipeline.cmake:17-20` | H |
| F5 | There is no target named `hello-triangle-sdl` anywhere in CMake (BASE either). Only README text and historical target listings mention it. | `grep -rn hello-triangle` over both worktrees: `README.md`, `modularization/**/targets-opengles.txt` only | H |
| F6 | The 22 focused test targets: `CnaAudioTests CnaContentTests CnaContentPipelineTests CnaCoreTests CnaDesignTests CnaDiagnosticsTests CnaDevicesTests CnaDevicesExtTests CnaGamerServicesTests CnaGraphicsTests CnaGraphicsExtTests CnaInputModuleTests CnaInspectorTests CnaIntegrationTests CnaMathTests CnaMediaTests CnaNetTests CnaPhoneTests CnaPlatformModuleTests CnaRendererTests CnaRuntimeTests CnaStorageTests`. BASE had none of them (`grep` count 0). | `cmake/UnitTests.cmake:439-460` | H |
| F7 | `CNA_TEST_DISPLAY` defaults to **empty** (tests inherit the caller's `DISPLAY`), not `:0`. `:0` is honoured only with `CNA_TEST_ALLOW_LIVE_DISPLAY=ON`; a Wayland guard stops tests connecting to a live compositor. | `cmake/TestDisplayPolicy.cmake:33-46,10-23` | H |
| F8 | The registered CTest inventory includes many separately registered example/smoke executables that `--target CnaTests` does not build; the project's own unfiltered CI job therefore does a full default build. | `.github/workflows/general-tests-ci.yml:145-150` | H |
| F9 | No install/export/CPack rules exist for the C++ framework; only the optional C API installs a `CNA` CMake package (`CNACTargets.cmake`, `CNAConfig.cmake`, `CNAConfigVersion.cmake`, component `CNACApi`; static archive gated by `CNA_C_API_BUILD_STATIC=ON`). | `grep install(` over TARGET: only `modules/c-api/CMakeLists.txt:364-480`; `modules/c-api/CMakeLists.txt:343` | H |
| F10 | `CNA_BUILD_C_API=ON` now **requires** `CNA_ENABLE_NET=ON` and fails at configure with a named `FATAL_ERROR` (alpha.1 failed later on a missing include). C ABI is `0.29.0`, C17 with `CMAKE_C_EXTENSIONS ON` for vendored C. `docs/c-api/RELEASE_GATE.md` (untrusted) reports "Not ready, 1 criterion unmet (468 unmapped public symbols)". The `static_assert` on renderer-map size still exists (`modules/c-api/src/CnaCApiCoreExt.cpp:241`); I did not compile it. | `CMakeLists.txt:78-90,185-191`; `modules/c-api/include/CNA/C/abi.h:34-40`; `docs/c-api/RELEASE_GATE.md:9-20` | H (option/abi) / M (buildability) |

### 1.2 Platform layer (`CNA_PLATFORM`)

| # | Claim | Evidence | Conf |
|---|---|---|---|
| P1 | `CNA_PLATFORM` cache default is **`SDL3` on every OS** (no per-OS default). The per-OS default exists only for the *renderer*: Emscripten `WEBGL2`, Linux `OPENGLES3`, everything else `SDL_RENDERER`. Audio default is also `SDL3` on every OS. | `cmake/PlatformSelection.cmake:15-16`; `cmake/RendererIdentityDefault.cmake:26-32`; `cmake/AudioPlatformSelection.cmake:13` | H |
| P2 | Implemented, offered values: `SDL3`, `SDL2`, `HEADLESS` always; `WIN32` where the target is Windows (native or mingw-w64 cross); `TERMINAL` where the target is not Windows (POSIX/termios); `X11` where `find_package(X11)` finds libX11, libXext and `X11/XKBlib.h` and the target is not Windows/Emscripten/Android/iOS; `WAYLAND` where pkg-config finds wayland-client >= 1.18, xkbcommon >= 0.5, wayland-protocols with `stable/xdg-shell`, and wayland-scanner, on a target that is not Windows/Emscripten/Android/Apple. | `cmake/PlatformSelection.cmake:27-32,40-44,61-65`; `cmake/PlatformX11.cmake:37-68`; `cmake/PlatformWayland.cmake:52,69,78,86,97-120` | H |
| P3 | Reserved values that **fail configure** with "reserved identifier that is NOT implemented": `SDL12`, `EMSCRIPTEN`, plus `TERMINAL` on Windows and `WIN32` off Windows. Unknown values fail with "not a known platform". `X11`/`WAYLAND` requested but not buildable fail with a message naming the packages to install and explicitly refuse to fall back to SDL3. Values are case-sensitive (`IN_LIST`). | `cmake/PlatformSelection.cmake:46-54,67-75,85-114` | H |
| P4 | Exactly one implementation is compiled as the default (`CNA_PLATFORM_<NAME>` define); `Headless` is **always** compiled, `Terminal` is always compiled on non-Windows. `PlatformFactory::GetAvailable()`/`Create(name)` therefore expose several names at run time; there is no `CNA_PLATFORM` environment variable. | `modules/platform/CMakeLists.txt:14-110`; `modules/platform/src/PlatformFactory.cpp:37-50,124-150`; `cmake/PlatformSelection.cmake:130` | H |
| P5 | Native backends use no SDL: `src/X11` (43 files, ~11.8k lines), `src/Wayland` (34 files, ~8.8k lines), `src/Win32` (31 files, ~4.5k lines); SDL3 backend 28 files (~5.5k), SDL2 6 files (~0.9k), Terminal 22 files (~3.2k), Headless 2 files. X11/Wayland share `src/Xkb`, `src/Freedesktop` (D-Bus portal, loaded at run time), `src/Posix`, `src/Linux` (evdev gamepads/haptics/power via kernel `<linux/input.h>`, no libudev). | `modules/platform/src/*` line counts; `modules/platform/CMakeLists.txt:59-88` | H |
| P6 | Capability contract grew from 29 to **32** flags: `dragAndDrop`, `primarySelection`, `clipboardData` were appended. Every flag defaults to false and "false" means the call refuses deterministically. | `modules/platform/include/CNA/Platform/PlatformCapabilities.hpp:26-92`; `PlatformCapability.hpp:21-126`; BASE diff | H |
| P7 | Per-backend capability sets are in the Platform matrix below; sources: SDL3 `modules/platform/src/Sdl3/Sdl3Platform.cpp:278-333`, SDL2 `.../Sdl2/Sdl2Platform.cpp:220-236` (no mouse/gamepad/clipboard service: `:419-426`), X11 `.../X11/X11Platform.cpp:215-289`, Wayland `.../Wayland/WaylandPlatform.cpp:487-545`, Win32 `.../Win32/Win32Platform.cpp:80-111`, Terminal `.../Terminal/TerminalPlatform.cpp:178-190`, Headless `.../Headless/HeadlessPlatform.cpp:142-147` (all false). | | H |
| P8 | TERMINAL at configure accepts only CPU renderers: `SOFTWARE PORTABLEGL HEADLESS STUB` (site's "[retired]" are gone). | `cmake/RendererSelection.cmake:139-147` | H |
| P9 | **SDL2/SDL3 mixing is now a hard configure error** in three cases: platform SDL2 + audio SDL3 (i.e. `-DCNA_PLATFORM=SDL2` alone, because audio defaults to SDL3), platform SDL3 + audio SDL2, and platform SDL2 + audio SDL2 with a renderer among `SDL_RENDERER SDL_GPU FNA3D FREEDIRECT`. | `cmake/Sdl2OnlyConfiguration.cmake:19-46` | H |
| P10 | `CNA_ENABLE_SDL` (`AUTO` default, `ON`, `OFF`) decides whether the vendored SDL3 sub-build runs at all. With `OFF`, any selection that needs SDL is refused with "genuinely requires SDL: <reasons>": platform SDL3/SDL2, audio SDL3/SDL2, and renderers `SDL_RENDERER SDL_GPU FNA3D FREEDIRECT` (also when they appear in `CNA_GRAPHICS_RENDERERS`). With `OFF`, `find_package(SDL*)` is blocked for every subproject. | `cmake/SdlAvailability.cmake:27-32,61-86,88-101`; `CMakeLists.txt:245-249` | H |
| P11 | SDL2 platform is fetched with `FetchContent` (not a submodule): pinned commit `fa24d868ac2f8fd558e4e914c9863411245db8fd` ("SDL 2.30.11"), override `CNA_SDL2_ROOT`. SDL3/SDL3_image/SDL3_mixer are git submodules built at configure time into `<source>/.sdl-prebuilt-<os>-<arch>[-min<deploy>][-wayland]/` (persistent across clean builds). SDL3 is built **shared** on Linux/macOS/Windows/Android and **static** on Emscripten and iOS. | `cmake/ThirdPartySDL2.cmake:12-18`; `cmake/ThirdPartySDL.cmake:56-125,262-305` | H |
| P12 | Vendored SDL3 video drivers depend on which development packages exist when SDL is first built; CNA reports the resulting driver list and warns if Wayland was requested but absent. Installing packages later does not change an existing prebuilt cache. | `cmake/ThirdPartySDL.cmake:141-216` | H |
| P13 | Target-OS axis is separate: `CNA::TargetPlatform` has `Desktop, Android, iOS, Web`; macros `CNA_TARGET_APPLE/IOS/MACOS`; a comment states `CNA_PLATFORM_<NAME>` names the *implementation* axis. | `modules/core/include/CNA/TargetPlatform.hpp:1-19,45-55` | H |
| P14 | Win32 backend declares API level `_WIN32_WINNT/WINVER = 0x0603` (Windows 8.1) as a floor; links only OS libraries `user32 gdi32 opengl32 ole32 shell32 uuid`; Vulkan loaded at run time. No XInput/gamepad, no IME, no drag-and-drop, no tray in Win32. | `modules/platform/src/Win32/Win32Common.hpp:37-43`; `modules/platform/CMakeLists.txt:162-164`; `Win32Platform.cpp:105-110` | H |
| P15 | Wayland is **not exercised by any GitHub workflow**: no workflow selects `CNA_PLATFORM=WAYLAND`. Tests exist and are registered (`CnaWaylandMappingTests`, `...ProtocolTests`, `...PortalTests`, `...WestonTests`, `...WestonGpuTests`, `...MutterTests`, `...MutterCzechTests`, `...IbusTests`, `...LinkClosure`, `...WestonScaledTests`, `CnaWaylandPlatformSelection`) but are launched locally through `tools/platform/wayland_test_server.sh`. CNA's own docs claim Weston and GNOME Mutter validation; that is local evidence only. | `grep -rn WAYLAND .github/workflows` (no selection); `cmake/UnitTests.cmake:1557-1563,1712-1782`; `docs/platform-wayland.md:368-388` (untrusted) | H (absence) / M (local validation) |
| P16 | X11 and Win32 *are* in CI: `platform-ci.yml` jobs `x11-sdl-free` (X11 + HEADLESS + NULL, `CNA_ENABLE_SDL=OFF`, Xvfb+openbox, uinput/D-Bus suites must not skip) and `x11-sdl-free-gpu` (X11 + OPENGL33/VULKAN/SOFTWARE/HEADLESS runtime-selectable + ALSA, no SDL, two real games run); `win32-cross` (mingw-w64 cross-built **standalone platform harness**, run under Wine on push/PR) and `win32-native` (MSVC, **manual dispatch only**). The Win32 jobs build `tools/platform/standalone_tests`, not the full CNA. | `.github/workflows/platform-ci.yml:378-650,245-311,323-363` | H |

### 1.3 Audio (`CNA_AUDIO_PLATFORM`)

| # | Claim | Evidence | Conf |
|---|---|---|---|
| A1 | Implemented values: `SDL3` (default), `SDL2`, `NULL`, `ALSA` (Linux only). Reserved and refused: `OPENAL`, `WASAPI` (alpha.1 also reserved ALSA; that changed). Unknown values fail. `ALSA` on a non-Linux target fails. | `cmake/AudioPlatformSelection.cmake:13,17,21,25-48` | H |
| A2 | `SOUND_ENABLED` (a mixer exists behind `MixerEngine.hpp`) is defined for **SDL3 and ALSA** only. | `modules/CMakeLists.txt:270-276` | H |
| A3 | Source selection: `Platform/Sdl3` + `Backend/Sdl3Mixer` only for SDL3; `Platform/Sdl2` only for SDL2; `Platform/Alsa` + `Backend/CnaMixer` only for ALSA; `Platform/Null` is always compiled. Link rules: SDL3 -> `SDL3::SDL3` + `SDL3_mixer::SDL3_mixer`; SDL2 -> `SDL2::SDL2`; ALSA -> headers + `${CMAKE_DL_LIBS}` + vendored `stb`/`dr_libs` include dirs; NULL -> nothing. | `modules/audio/CMakeLists.txt:9-31,39-54` | H |
| A4 | ALSA: `libasound.so.2` is `dlopen`ed at run time (never linked; CI asserts no `NEEDED asound`), device from `CNA_AUDIO_DEVICE` (`null` = silent), capture from `CNA_AUDIO_RECORDING_DEVICE`; configure needs ALSA **headers** (`libasound2-dev`) and fails with a named message otherwise. | `modules/audio/src/Platform/Alsa/AlsaLibrary.cpp:25`; `AlsaAudioDevice.cpp:35`; `AlsaAudioRecordingDevice.cpp:34`; `modules/audio/CMakeLists.txt:22-31`; `.github/workflows/platform-ci.yml:614-628` | H |
| A5 | CNA's own mixer (`Backend/CnaMixer`): linear-interpolation resampler, per-track mix callback, post-mix callback, loops, streams; decoders vendored: WAV PCM8/16/24/32 + IEEE float + MS-ADPCM + IMA-ADPCM (`WavDecoder.cpp`), Ogg Vorbis (`stb_vorbis` 1.22), MP3 (`dr_mp3` 0.7.3), FLAC (`dr_flac` 0.13.3). Opus, WMA/xWMA, XMA are not decoded. | `modules/audio/src/Backend/CnaMixer/CnaMixer.hpp:1-60`; `CnaMixerDecoders.cpp:301,348,400`; `StbVorbis.cpp:3`; `DrLibs.cpp:3`; `third_party/{stb,dr_libs}` | H |
| A6 | SDL3 path: `SDL3_mixer` (vendored, `MIX_Track` model) with codec dependencies mostly disabled: `SDLMIXER_GME/MOD_XMP/MP3_MPG123/MIDI_FLUIDSYNTH/OPUS/VORBIS_VORBISFILE/VORBIS_TREMOR/WAVPACK/FLAC_LIBFLAC=OFF`. | `modules/audio/src/Backend/Sdl3Mixer/MixerEngine.cpp:39-63`; `cmake/ThirdPartySDL.cmake:363-376` | H |
| A7 | Capture: SDL3 (`Sdl3AudioRecordingDevice`), ALSA (`AlsaAudioRecordingDeviceProvider`), **none** for SDL2 (`nullptr`) and NULL (`nullptr`). | `modules/audio/src/Platform/AudioDeviceFactory.cpp:34-52` | H |
| A8 | `WavDecoder.cpp` (SDL-free WAV decode) is compiled regardless of audio platform, so `cna_content` links without SDL. | `docs/platform-abstraction.md:~60-75` (untrusted) confirmed by `modules/audio/CMakeLists.txt:4-21` (no filter on `src/Internal`) | H |
| A9 | XNA-level behaviour changes since BASE: `Apply3D(const AudioListener*, int, const AudioEmitter&)` and the collection overload accept **any positive listener count** (dominant = nearest listener decides); zero/negative count and null array still throw. `Microphone.All` is the machine's devices; MS-ADPCM encoder for `ConvertFormat`; Doppler scaling matches XNA. Unchanged: WaveBank XMA/WMA entry logs to stderr and returns `nullptr`; reverb send is a no-op (`SoundEffectInstance::INTERNAL_applyReverb`); only the first `PlayWave` per track; `.m4a/.aac` unsupported. | `modules/audio/include/Microsoft/Xna/Framework/Audio/SoundEffectInstance.hpp:363-392`; `modules/audio/src/Xna/WaveBank.cpp:358-373`; `SoundEffectInstance.cpp:689`; `Cue.cpp:93-98`; `modules/media/src/Internal/MediaLibraryIndex.cpp:38` | H |
| A10 | Under SDL2 and NULL the XNA facade (`SoundEffect`, `SoundEffectInstance`, `DynamicSoundEffectInstance`, `MediaPlayer`, `Microphone`) compiles without a mixer: `SOUND_ENABLED` blocks are absent; mixer-dependent test files are excluded from the build. | `modules/audio/src/Xna/*.cpp` (`#ifdef SOUND_ENABLED` counts: SoundEffect 12, SoundEffectInstance 25, DynamicSoundEffectInstance 13, Microphone 1); `modules/media/src/Xna/MediaPlayer.cpp` (12); `cmake/UnitTests.cmake:130-165` | H |

### 1.4 Build system, dependencies, packaging

| # | Claim | Evidence | Conf |
|---|---|---|---|
| B1 | Required sibling checkouts: `../sharp-runtime` always (configure `FATAL_ERROR` otherwise; override `CNA_SHARP_RUNTIME_ROOT`); `../easy-gl` (which needs `../meta-gl`) for `OPENGLES2 OPENGLES3 OPENGL33 WEBGL1 WEBGL2` only; `../free-direct` (which pulls `../free-api`) for `FREEDIRECT` only. Nothing else is a sibling. The FATAL message cites `https://github.com/openeggbert/sharp-runtime.git`; `libcna/*` and `openeggbert/*` resolve to identical repositories (same SHAs). `free-direct`/`free-api` exist only under `openeggbert/` (not `libcna/`). | `CMakeLists.txt:286-304`; `cmake/RendererSelection.cmake:207-262`; `git ls-remote` on both orgs | H |
| B2 | Branches to clone for TARGET: CNA `next`; sharp-runtime `next`; easy-gl `develop`; meta-gl `develop` (`clone_siblings.sh` picks the first candidate branch that exists, then `next`, then `develop`). Default HEADs: cna=`develop`(alpha.1), sharp-runtime=`main`, easy-gl=`develop`, meta-gl=`develop`, free-direct=`develop`, free-api=`develop`. | `scripts/ci/clone_siblings.sh:1-32`; `git ls-remote --symref` | H |
| B3 | Git submodules: **five** gitlinks, not four: `third_party/SDL` (`cbe3fbe9...` + two Vulkan patches applied to a staged copy), `third_party/SDL_image` (`fcb9d0b1...`), `third_party/SDL_mixer` (`3075d3ed...`), `third_party/draco` (`8786740...`, needed unless `CNA_ENABLE_DRACO=OFF`, default ON except under Emscripten), `vendor/googletest` (`7e2c425d...`, needed while `CNA_BUILD_TESTS=ON`). Non-recursive `git submodule update --init` is correct (recursion only pulls unused codec submodules). Vendored in-tree (no fetch): `third_party/{enet,stb,dr_libs,cgltf}`. | `.gitmodules`; `git ls-tree HEAD`; `cmake/ThirdPartySDL.cmake:219-243`; `modules/CMakeLists.txt:77-82,131-150`; `cmake/UnitTests.cmake:22-33` | H |
| B4 | Fetched at configure time when the matching renderer/option is selected: FNA3D `3240147` (+ MojoShader patch series) for `FNA3D` and every `*_COMPILED_EFFECTS` option; wgpu-native `v29.0.1.1` for `WEBGPU` (`CNA_WEBGPU_AUTO_DOWNLOAD=ON`); PortableGL `63a55db7` for `PORTABLEGL`; SDL_shadercross `1ff05bec` + SPIRV-Cross `vulkan-sdk-1.4.350.0` for `SDL_GPU` when `CNA_SDL_GPU_SHADERCROSS` (default ON on Windows/Apple, OFF elsewhere). `VULKAN` needs `find_package(Vulkan REQUIRED)`; `OPENGL4` needs `find_package(OpenGL REQUIRED)`. | `cmake/ThirdPartyFNA3D.cmake:19-31`; `cmake/ThirdPartyWebGPU.cmake:12-14`; `cmake/ThirdPartyPortableGL.cmake:18-20`; `cmake/ThirdPartySDLShaderCross.cmake:7-13`; `cmake/RendererSelection.cmake:323,484-490,511` | H |
| B5 | FFmpeg: `CNA_ENABLE_VIDEO` `AUTO` (default; enabled only if libavcodec/libavformat/libavutil/libswresample are found via pkg-config), `ON` (requires them; FATAL if the target cannot support FFmpeg), `OFF`. Never available on `MINGW`/`WIN32`/`EMSCRIPTEN`/`ANDROID`/iOS (AUTO silently falls back, ON fails). macOS keeps FFmpeg support. | `CMakeLists.txt:192-202`; `modules/CMakeLists.txt:8-58` | H |
| B6 | Sharp Runtime component closure requested by CNA: `Core.Base IO Collections.Core Collections.ObjectModel Runtime Threading Text Globalization ComponentModel Storage Security.Cryptography Xml Resources` plus `Xml.Serialization` on non-Windows targets. | `cmake/SharpRuntimeConsumption.cmake:20-62` | H |
| B7 | Optional-library switches with `AUTO` semantics: `CNA_ENABLE_FONT_PIPELINE` (FreeType), `CNA_ENABLE_MEDIA_PIPELINE`, `CNA_CNB_ZSTD` (libzstd). `CNA_ENABLE_NET=ON` builds vendored ENet. | `CMakeLists.txt:105-107,178`; `modules/content-pipeline/CMakeLists.txt:58-60`; `modules/CMakeLists.txt:92-129` | H |
| B8 | Apple: hard floors macOS **13.3** and iOS **16.3** (below is a `FATAL_ERROR`; caused by floating-point `std::to_chars`); iOS renderer allow-list is `SDL_RENDERER` only (others need `CNA_APPLE_ALLOW_UNVALIDATED_RENDERER=ON`); `CNA_BUILD_APPLE_SMOKE_APP` defaults to ON for iOS; iOS toolchain `cmake/toolchains/ios.cmake` (`CNA_IOS_SIMULATOR`). SDL is static on iOS. | `cmake/ApplePlatform.cmake:74-104,246-292`; `cmake/AppleSmoke.cmake:3-5`; `cmake/toolchains/ios.cmake:29` | H |
| B9 | Emscripten: `emcmake` (or the Emscripten toolchain file) is required; `CNA_ENABLE_EMSCRIPTEN_THREADS` (OFF) is Emscripten-only; JS-lowered exceptions (`-fexceptions`), `-sSTACK_SIZE=1048576`; Asyncify only for application targets; Draco defaults OFF (pinned Draco 1.5.7 does not link under Emscripten); no sanitizers. The `web` preset has **no toolchain file**, so `cmake --preset web` alone configures natively; its own description says `emcmake cmake --preset web`. CI pins emsdk `6.0.3`. | `CMakeLists.txt:25-41`; `cmake/BuildPerformance.cmake:110-118,146-148`; `modules/CMakeLists.txt:66-81,246-270`; `CMakePresets.json` preset `web`; `.github/workflows/emscripten-multi-renderer-ci.yml:45` | H |
| B10 | Android: no preset, no workflow, no CMake minimum-API check. The only Android build project is the Devices demo (Gradle: `minSdkVersion 24`, `targetSdkVersion 35`, `compileSdkVersion 35`, `ndkVersion 30.0.14904198`, `abiFilters 'arm64-v8a'`, `-DANDROID_PLATFORM=android-24`). SDL3 is built as a shared library with `ANDROID_ABI/PLATFORM/STL` forwarded. | `modules/devices/examples/demo_devices/android/com.openeggbert.cna.demodevices/app/build.gradle:9-28`; `cmake/ThirdPartySDL.cmake:267-271,433-446` | H |
| B11 | Windows: MinGW-w64 toolchain file `cmake/toolchains/mingw-w64.cmake` (x86_64, falls back to i686); native MSVC builds work only in manual CI; `/utf-8`, `/bigobj`, `NOMINMAX` are applied. There is **no** `mingw-w64-i686.cmake` ([retired] is gone). | `cmake/toolchains/`; `modules/CMakeLists.txt:283-311` | H |
| B12 | `CNA_SHARED_LIBRARY` defaults ON for native (non-cross) ELF Linux/BSD builds with GNU/Clang and CMake >= 3.27; forced OFF elsewhere; `ON` where unsupported is a `FATAL_ERROR`. Effect: executables link `libcna.so` (WHOLE_ARCHIVE of the CNA modules) instead of static archives. | `CMakeLists.txt:43-73`; `cmake/SharedRuntimeLibrary.cmake:1-40` | H |
| B13 | Build-quality gates that run at configure time and can fail a configure: platform ratchet (`CNA_PLATFORM_RATCHET`, strict by default, needs Python 3, skipped without it), hot-path lint (`CNA_PLATFORM_HOT_PATH_LINT`), renderer descriptor gate (`CNA_BUILD_RENDERER_DESCRIPTOR_GATE`), source-partition validator, legacy-tree guard, retired-renderer refusal. | `cmake/PlatformRatchet.cmake:19-34`; `cmake/PlatformHotPathLint.cmake:15`; `cmake/RendererDescriptorGate.cmake:24`; `modules/CMakeLists.txt:432-474`; `cmake/RendererIdentities.cmake:88-106` | H |
| B14 | Renderer combination rules at TARGET (three families, [retired] gone): PORTABLEGL + any real-GL family (`OPENGLES2 OPENGLES3 OPENGL33 WEBGL1 WEBGL2 OPENGL4`), GDI + SOFTWARE, and cross-OS partitions (Windows-only `DIRECTX9 DIRECTX11 DIRECTX12 DIRECT2D GDI`; Emscripten-only `WEBGL1 WEBGL2 CANVAS HTML_DOM SVG_DOM`; macOS-only `METAL`). Windows-only gate: 5 renderers (not 14). | `cmake/RendererCombinations.cmake:14-32,89-135`; `cmake/RendererSelection.cmake:149-160` | H |
| B15 | Sanitizers via `CNA_SANITIZE` (comma list; ASan+TSan and TSan+MSan rejected; not on MSVC or Emscripten), `CNA_SANITIZE_OPTIMIZATION` (`DEFAULT O0 O1 O2 O3`), `CNA_DEBUG_INFO` (`FULL LINE_TABLES SPLIT`), `CNA_LINKER` (`AUTO DEFAULT LLD MOLD`, native ELF only), `CNA_ENABLE_IPO`, `CNA_ENABLE_UNITY_BUILD`, `CNA_ENABLE_PCH`, `CNA_DIAGNOSTICS` (`OFF STATS FULL`). ccache: `CNA_USE_CCACHE` (ON) with `CNA_CCACHE_BASEDIR`. | `cmake/BuildPerformance.cmake:9,19,131-138,338-341`; `cmake/UnitTests.cmake:11`; `CMakeLists.txt:100,113-147,153-171` | H |

### 1.5 CI (see the CI inventory for the per-file table)

| # | Claim | Evidence | Conf |
|---|---|---|---|
| C1 | 20 workflow files; 17 trigger automatically on push to `next`/`develop`/`main` and PRs targeting them (several path-filtered), 3 are manual-only or branch-specific: `d3d-windows-ci.yml` and `gdi-windows-ci.yml` (`workflow_dispatch` only), `content-pipeline-windows-ci.yml` (push to branch `content-pipeline-final` + dispatch). Inside `platform-ci.yml` one job (`win32-native`) is dispatch-only. | `.github/workflows/*.yml` `on:` blocks; `platform-ci.yml:327` | H |
| C2 | No workflow selects an invalid renderer identity at TARGET (script check of every `CNA_GRAPHICS_RENDERER(S)=` value and matrix `renderer:` list against the 25 public identities). alpha.1's `EASYGL` lanes were corrected: `general-tests-ci.yml` now uses `OPENGLES3`; `input-ci.yml` matrix uses `OPENGLES3`, `SDL_RENDERER`, `VULKAN`. | scripted check + `general-tests-ci.yml:134-141`, `input-ci.yml` matrix | H |
| C3 | Known static defects: `metal-macos-ci.yml` push `paths:` filter lists three files that no longer exist (`cmake/BackendLibraries.cmake`, `cmake/Examples.cmake`, `cmake/Tests/MetalTests.cmake`); it still triggers on PRs and on the paths that do exist. `general-tests-ci.yml` runs `ctest` with `continue-on-error: true` and then classifies failures against a one-name allowlist (`EasyGL_GraphicsDevice_ReferenceStencil`). | `.github/workflows/metal-macos-ci.yml` `paths:`; `general-tests-ci.yml:176,192-194` | H |
| C4 | Runner OS/compilers: ubuntu-24.04 with `gcc-14/g++-14` for all Linux workflows except `devices-tests.yml` (`ubuntu-latest`, `build-essential` default compiler); `macos-14` (Apple); `windows-latest` (MSVC via `ilammy/msvc-dev-cmd`); emsdk `6.0.3`; Playwright+Chromium for HTML_DOM; mingw-w64 + Wine for Win32 cross. | workflow YAML | H |
| C5 | Configure-time gate scripts run in CI: `tools/platform/{sdl_inventory,sdl_classify,renderer_sdl_audit,sdl_ratchet --strict,hot_path_lint,nonproduction_sdl_audit,check_contract}.py` (HEADLESS cell of platform-ci), `tools/build/check_build_performance_policy.py` (general-tests), `scripts/check_renderer_identities.py` and friends (multi-renderer "Registry gates"), `tools/c-api/*` (5 workflows). | `platform-ci.yml:216-225,534-540`; `general-tests-ci.yml:73-76`; `multi-renderer-ci.yml` "Registry gates" | H |
| C6 | **sharp-runtime revision per workflow.** Lanes using `clone_siblings.sh` (branch match, else `next`, else `develop`): `platform-ci` (all jobs), `general-tests-ci`, `input-ci`, `multi-renderer-ci`, `gltf-renderer-stride-ci` (2 jobs), `gltf-sanitizers-ci`, `c-api-coverage-gate`, `c-api-limitations`, `c-api-release-gate`. Lanes with a **hard pin or default branch**: `emscripten-multi-renderer-ci`, `htmldom-ci`, `devices-tests` pin `bc8dbf41` (2026-08-15); `apple-ci` (macOS job and iOS job) and `metal-macos-ci` pin `f23ded28` (2026-08-15); `content-pipeline-windows-ci` pins `df1b42ab` (sharp-runtime `develop` tip, 2026-08-28); `d3d-windows-ci` and `gdi-windows-ci` take the default branch (`main`, `54578590`). `Resources` (`modules/resources`) and `Xml.Serialization` (`modules/xml-serialization`) are registered only on sharp-runtime `next`, and CNA's default closure links `SharpRuntime::Resources` (and `Xml.Serialization` off Windows), so these lanes should fail at configure or generate time. CNA grew the closure after those pins were written: `Xml.Serialization` on 2026-09-06 (`0794128b6`, SAMPLE-066) and `Resources` on 2026-09-20 (`8c1c8b412`, XNA-MISSING-013); the `bc8dbf41` pin was last touched by `eaf455a94` (2026-08-21). Not run; static reading. | `.github/workflows/{emscripten-multi-renderer-ci,htmldom-ci,devices-tests}.yml` (`ref: bc8dbf41...`), `apple-ci.yml:101-102,224-225` and `metal-macos-ci.yml:51-52` (`ref: f23ded28...`), `content-pipeline-windows-ci.yml:42-43` (`ref: df1b42ab...`), `d3d-windows-ci.yml:57-59`, `gdi-windows-ci.yml:36-38` (no `ref:`); `cmake/SharpRuntimeConsumption.cmake:20-62,73-79`; `git ls-tree`/`git grep` on sharp-runtime refs | M |

## Platform matrix

### 2.1 The four axes (plus one switch), exactly as at TARGET

| Axis | Question | Selected by | Compile-time marker | Values at TARGET | Evidence |
|---|---|---|---|---|---|
| 1. Target operating system | What ABI/toolchain is this binary for? | CMake toolchain / host (`CMAKE_SYSTEM_NAME`, `EMSCRIPTEN`, `ANDROID`, `CNA_APPLE_IOS`) | `CNA_TARGET_APPLE/IOS/MACOS`; `CNA::TargetPlatform` = `Desktop, Android, iOS, Web`; `getCurrentPlatformName()` = `Web Android iOS macOS Windows Linux Desktop` | Linux, Windows (MSVC, MinGW), macOS, iOS, Android, Emscripten | `modules/core/include/CNA/TargetPlatform.hpp:1-19,45-140` |
| 2. Platform implementation | Who owns windows, events, input, timing, host services? | `CNA_PLATFORM` (default `SDL3`) | `CNA_PLATFORM_<NAME>` | `SDL3 SDL2 X11 WAYLAND WIN32 HEADLESS TERMINAL` (reserved: `SDL12 EMSCRIPTEN`) | `cmake/PlatformSelection.cmake` |
| 3. Graphics renderer | Who turns draw calls into pixels? | `CNA_GRAPHICS_RENDERER` (default per OS) and optional `CNA_GRAPHICS_RENDERERS` | `CNA_RENDERER_<X>` (default identity only), `CNA_MULTI_RENDERER` | 25 public identities | `cmake/RendererSelection.cmake`, `RendererIdentities.cmake` |
| 4. Audio implementation | Who opens playback/capture and (for two values) mixes? | `CNA_AUDIO_PLATFORM` (default `SDL3`) | `CNA_AUDIO_PLATFORM_<NAME>`; `SOUND_ENABLED` for SDL3, ALSA | `SDL3 SDL2 NULL ALSA` (reserved: `OPENAL WASAPI`) | `cmake/AudioPlatformSelection.cmake`, `modules/CMakeLists.txt:270-276` |
| (switch) SDL availability | Is SDL configured at all? | `CNA_ENABLE_SDL` `AUTO`(default)/`ON`/`OFF` | `CNA_SDL2_ONLY_CONFIGURATION` (internal) | `OFF` refuses SDL3/SDL2 platform, SDL3/SDL2 audio, and renderers `SDL_RENDERER SDL_GPU FNA3D FREEDIRECT` | `cmake/SdlAvailability.cmake` |

Axes are independent **with hard exclusions**: SDL2 and SDL3 may not share a process (P9); TERMINAL only with CPU renderers (P8); `WIN32` only on Windows targets, `TERMINAL` only off Windows, `X11`/`WAYLAND` only where their dev packages exist; `ALSA` only on Linux; the four SDL3-direct renderers need SDL. Reserved values never fall back.

### 2.2 Implementation status

| `CNA_PLATFORM` | Status at TARGET | Third-party inputs | Offered when | Default renderer note | Automatic CI evidence | Other evidence |
|---|---|---|---|---|---|---|
| `SDL3` | Implemented, **default**, most complete; the only implementation exercised on macOS, iOS, Android (code only) and Emscripten | vendored SDL3 (shared; static on iOS/Emscripten) | always | OS default renderer applies | Many workflows (platform-ci matrix, input-ci, general-tests, apple-ci, emscripten, htmldom, ...) | SDL pinned `cbe3fbe9` |
| `SDL2` | Implemented, deliberately narrow (real SDL 2.30, no `sdl2-compat`) | SDL2 via FetchContent (`fa24d868`) | always | Needs audio SDL2 (P9) | `platform-ci.yml` cell "SDL2 + OpenGLES3" with audio SDL2, plus targets `cna_platform_sdl2_tests`, `cna_audio_sdl2_tests` | `docs/platform-sdl2.md` (untrusted; matches code) |
| `X11` | **Implemented, native (Xlib, XKB, XInput2, XRandR, Xcursor, MIT-SHM, GLX, D-Bus portal), no SDL anywhere** | libX11+libXext+XKBlib.h mandatory; Xi, Xrandr, Xcursor, Xfixes, Xau, Xss, XShm, GLX, Vulkan headers, D-Bus headers optional (each gates one capability) | Unix-like host with X dev packages | Works with `CNA_ENABLE_SDL=OFF`; renderer needs a non-SDL family | `x11-sdl-free`, `x11-sdl-free-gpu` (push/PR) | `docs/testing-x11-desktop.md`, `tools/platform/x11_desktop_validation` |
| `WAYLAND` | **Implemented, native Wayland client (xdg-shell, xkbcommon, EGL/Vulkan/wl_shm, text-input-v3, fractional-scale, ...), no SDL/X11/Xwayland** | wayland-client >= 1.18, xkbcommon >= 0.5, wayland-scanner, wayland-protocols (build); EGL, wayland-egl, wayland-cursor, libdbus loaded at run time | Unix host (not Apple/Android/Windows/Emscripten) with the packages | same | **none** (P15) | In-process test compositor + Weston/Mutter suites, run locally |
| `WIN32` | **Implemented, native user32/gdi32/WGL/COM backend, no SDL** | OS libraries only | Windows targets, including mingw-w64 cross | e.g. `DIRECTX11` (registered in `modules/renderers/directx11/examples`) | `win32-cross` (standalone platform harness, mingw-w64 + Wine, push/PR); `win32-native` manual | `docs/testing-win32-native.md`; `tools/platform/validate_win32_native.ps1` |
| `HEADLESS` | Implemented, one window object, no services, all capabilities false; **always compiled** | none | always | `HEADLESS`/`STUB`/`SOFTWARE` | platform-ci "Headless + Headless + Null audio", multi-renderer-ci | |
| `TERMINAL` | Implemented, POSIX-only (termios/poll); Kitty keyboard protocol probe; presents finished CPU frames; one window | none | non-Windows targets | Renderers limited to `SOFTWARE PORTABLEGL HEADLESS STUB` | platform-ci cell "Terminal + Software + Null audio" + `TerminalSoftwareDemoIntegration` pseudo-TTY test | `docs/platform-terminal-analysis.md` |
| `SDL12`, `EMSCRIPTEN` | Reserved, configure `FATAL_ERROR` | | never | | | `cmake/PlatformSelection.cmake:85-107` |

How they fail when reserved or unavailable (all `FATAL_ERROR`, no fallback): see P3. Emscripten is a *target OS* served by the `SDL3` implementation; `CNA_PLATFORM=EMSCRIPTEN` is reserved.

### 2.3 Capability matrix (`PlatformCapabilities`, 32 flags)

Legend: **Y** always true; **cond** true only when the stated runtime/build condition holds; **-** false (call refuses with `PlatformNotSupportedException`). Sources: P7.

| Capability | SDL3 | SDL2 | X11 | Wayland | Win32 | Terminal | Headless |
|---|---|---|---|---|---|---|---|
| multipleWindows | Y | Y | Y | Y | Y | - (one) | - (one) |
| highDpi | Y | Y | **-** (one coordinate space, by design) | Y (fractional/integer) | Y | - | - |
| multipleDisplays | Y | Y | cond (RandR) | cond (wl_output) | Y | - | - |
| borderlessFullscreen | Y | Y | cond (EWMH fullscreen hint); exclusive fullscreen through XRandR exists | Y | Y | - | - |
| nativeWindowHandle | Y | - | Y (Display*+XID) | Y (wl_display*+wl_surface*) | Y (HWND) | - | - |
| surfacePresentation (CPU frame) | Y | - | Y (XPutImage, MIT-SHM optional) | cond (wl_shm XRGB8888) | Y | cond (stdout is a TTY) | - |
| openGlContext | Y | Y | cond (GLX, loaded at run time) | cond (EGL, run time) | Y (WGL) | - | - |
| vulkanSurface | cond (`HasVulkanSupport`) | - | cond (Vulkan headers at build) | cond | cond (vulkan-1.dll present) | - | - |
| clipboard / clipboardData | Y / Y | - / - | Y / Y (ICCCM+INCR, MIME targets) | cond / cond (data device) | Y / - | - | - |
| dragAndDrop | Y | - | Y (XDND 5, target side) | cond | - | - | - |
| primarySelection | Y (unix, not Android/Emscripten) | - | Y | cond | - | - | - |
| textInput | Y | -* | Y | Y | Y | - | - |
| ime | Y | - | cond (XIM composition) | cond (text-input-v3) | - | - | - |
| exactKeyboardState | Y | Y | Y | Y | Y | cond (Kitty keyboard protocol) | - |
| pixelAccurateMouse | Y | - | Y | Y | Y | - (cells) | - |
| relativeMouse | Y | - | cond (XI2 raw motion) | cond (relative-pointer) | Y | - | - |
| cursorShapes | Y | - | Y | cond | Y | - | - |
| globalPointer | Y | - | Y | **-** (Wayland gives no desktop coordinates) | Y | - | - |
| inputDeviceEnumeration | Y | - | cond (XI2) | cond | Y | - | - |
| gamepad / joystick | Y / Y | - | Y / Y via kernel evdev (Linux with `linux/input.h`) | same as X11 | **-** / **-** (no XInput) | - | - |
| gamepadRumble / gamepadSensors | Y / Y | - | Y / Y (evdev) | Y / Y | - | - | - |
| haptics | Y | - | Y (evdev force feedback) | Y | - | - | - |
| sensors (accelerometer etc.) | Y | - | - | - | - | - | - |
| powerInfo | Y | - | Y on Linux (evdev/sysfs; needs `<linux/input.h>`) | same as X11 | Y | - | - |
| messageBox | Y | - | Y (Xlib-drawn window) | cond | Y | - | - |
| nativeFileDialog | Y | - | cond (D-Bus desktop portal) | cond (portal) | Y | - | - |
| tray | cond | - | cond (a system tray must exist) | - | - | - | - |
| camera | cond | - | - | - | - | - | - |
| managedEntrypoint | Y (Android/iOS `main` handling) | - | - | - | - | - | - |
| Touch/pen **events** (`TouchEvent`) | Y | - | Y (XInput 2.2 touchscreen + pen) | Y (wl_touch, tablet) | - | - | - |

`-*`: SDL2 translates text-input *events* (`docs/platform-sdl2.md` "Events", untrusted) but reports `textInput=false` (`Sdl2Platform.cpp:220-236`).
Sources for the conditional cells: X11 `X11Platform.cpp:215-289`; Wayland `WaylandPlatform.cpp:487-545`; Win32 `Win32Platform.cpp:80-111`.

Cross-checks that matter for documentation: SDL2 has **no** mouse snapshot, gamepad, clipboard, safe-area or surface-presenter service (`Sdl2Platform.cpp:419-426`); Win32 has **no** gamepads (the site must not imply XInput); Wayland has no `globalPointer`, no tray.

### 2.4 Renderer-versus-platform facts that follow from code (not from the docs)

| Fact | Evidence | Conf |
|---|---|---|
| `SDL_RENDERER SDL_GPU FNA3D FREEDIRECT` link SDL3 by identity; they are refused by `CNA_ENABLE_SDL=OFF` and, with SDL2 platform+audio, by `Sdl2OnlyConfiguration`. | `cmake/SdlAvailability.cmake:68-72`; `cmake/Sdl2OnlyConfiguration.cmake:37-46` | H |
| SDL2 platform can back GL-context renderers (`OPENGLES2/3`, `OPENGL33`, `OPENGL4`) and windowless CPU renderers, not `VULKAN` (no `vulkanSurface`), not native-handle renderers (DirectX, GDI, METAL). Unavailable combinations refuse at run time, not configure time. | `docs/platform-sdl2.md:121-140` (untrusted) + `Sdl2Platform.cpp:220-236` | M |
| X11 in CI runs `OPENGL33`, `VULKAN`, `SOFTWARE`, `HEADLESS` (runtime-selectable) with ALSA audio and no SDL. | `platform-ci.yml:549-650` | H |
| Native Win32 + DirectX has a registered test target, but the automatic Win32 CI job exercises only the platform module (standalone harness), not a full CNA + DirectX build. | `modules/renderers/directx11/examples/CMakeLists.txt:19`; `platform-ci.yml:245-311`; `tools/platform/standalone_tests/CMakeLists.txt:1-40` | H |
| `TERMINAL` is refused (configure) for every GPU renderer. | `cmake/RendererSelection.cmake:139-147` | H |

### 2.5 Operating-system status matrix for the website (claim only what code/CI proves)

Levels: **CI** = an automatic workflow (push/PR to `next|develop|main`) builds or tests it; **Manual CI** = a workflow exists but only `workflow_dispatch`; **Code** = sources and CMake wiring, no workflow; **Local** = only in-tree docs/scripts claim validation.

| Target | Platform implementations available | Real / tested | Experimental | Unsupported / not proven | Evidence |
|---|---|---|---|---|---|
| **Linux, X11 desktop (Xorg)** | `SDL3` (default), `X11` (native), `SDL2`, `HEADLESS`, `TERMINAL` | CI: SDL3 x {OPENGLES3, VULKAN, SOFTWARE, SDL_RENDERER}, SDL2+OPENGLES3, native X11+HEADLESS+NULL, native X11 + OPENGL33/VULKAN/SOFTWARE/HEADLESS + ALSA; runs under Xvfb, not real desktops | | GPU pixel/oracle matrix is not a CI gate | `platform-ci.yml`, `input-ci.yml`, `general-tests-ci.yml` |
| **Linux, Wayland session** | `SDL3` (its Wayland driver is built only if dev packages existed when SDL was built), native `WAYLAND`, or X11 through Xwayland | Code + test suites for native Wayland; **no CI**; local Weston/Mutter validation is claimed only in CNA docs | native Wayland backend (no automatic evidence) | SDL3-on-Wayland: no test runs a Wayland session in CI (all tests use Xvfb) | P15; `platform-ci.yml:121-135`; `cmake/ThirdPartySDL.cmake:141-216` |
| **Windows** | `SDL3` (default), `WIN32` (native), `SDL2`, `HEADLESS` | Manual CI: MSVC builds of `DIRECTX11`, `DIRECTX12`, `DIRECT2D` (`d3d-windows-ci.yml`), `GDI` (`gdi-windows-ci.yml`), HEADLESS content pipeline (`content-pipeline-windows-ci.yml`, branch `content-pipeline-final`), Win32 backend standalone harness (`win32-native`). CI: mingw-w64 cross-build + Wine of the Win32 platform module only. | Native `WIN32` backend (no gamepad, IME, drag-and-drop) | FFmpeg video (never built for Windows); WASAPI audio (reserved); XInput | `platform-ci.yml:245-363`; Windows workflows |
| **macOS** | `SDL3` | CI (macos-14): configure+build `CnaTests` on `SDL_RENDERER`, portable suites, self-contained `.app` bundle launch; `metal-macos-ci.yml` builds `METAL` and runs `^Metal` tests. Floor macOS 13.3. | `METAL` contract is narrower than "it builds" | Anything else not in these lanes | `apple-ci.yml`, `metal-macos-ci.yml`, `cmake/ApplePlatform.cmake:74-104` |
| **iOS** | `SDL3` | CI: device final-link of `cna_ios_smoke.app`, simulator install + launch of a one-frame smoke app; `SDL_RENDERER` only; floor iOS 16.3; net disabled in CI | Whole target is experimental | Physical device, pixels, input, audio, storage; tvOS | `apple-ci.yml:198-340`; `cmake/ApplePlatform.cmake:246-292` |
| **Android** | `SDL3` | Code only (NDK sensors, SDL entrypoint, demo Gradle project with minSdk 24 / NDK 30 / arm64-v8a). **No workflow, no preset.** | | Everything at run time | B10 |
| **WebAssembly (Emscripten)** | `SDL3` | CI: `emscripten-multi-renderer-ci.yml` builds/links one bundle with `WEBGL2;CANVAS;HTML_DOM;SVG_DOM` and asserts the JS selection surface; `htmldom-ci.yml` runs the HTML_DOM browser suite in Chromium (Playwright); emsdk 6.0.3; Draco off | Threads option `CNA_ENABLE_EMSCRIPTEN_THREADS` | Video (no FFmpeg build), sanitizers, `CNA_PLATFORM` other than SDL3 | workflow files; B9 |
| **Terminal (POSIX)** | `TERMINAL` | CI: `CnaPlatformTests` (TerminalPlatform unit tests) plus the `TerminalSoftwareDemoIntegration` pseudo-TTY test of `cna_demo_2d` | | Windows console | `platform-ci.yml:66-72,204-206` |
| **Headless (any host)** | `HEADLESS` | CI | | | `platform-ci.yml:59-65` |

### 2.6 Default selection per OS (exact)

| Target | `CNA_PLATFORM` | `CNA_AUDIO_PLATFORM` | `CNA_GRAPHICS_RENDERER` | `CNA_ENABLE_VIDEO` (AUTO resolves to) |
|---|---|---|---|---|
| Linux | SDL3 | SDL3 | `OPENGLES3` (needs easy-gl + meta-gl siblings) | on if the four FFmpeg pkg-config modules are found |
| Windows (MSVC/MinGW) | SDL3 | SDL3 | `SDL_RENDERER` | off (unsupported) |
| macOS | SDL3 | SDL3 | `SDL_RENDERER` | on if Homebrew FFmpeg found |
| iOS | SDL3 | SDL3 | `SDL_RENDERER` (only allowed) | off |
| Android | SDL3 | SDL3 | `SDL_RENDERER` | off |
| Emscripten | SDL3 | SDL3 | `WEBGL2` | off |

Evidence: P1, B5.

## Audio matrix

Everything is selected by `CNA_AUDIO_PLATFORM` and is independent of `CNA_PLATFORM` (SDL2/SDL3 cross-pairings excepted, P9). Sources: A1-A10.

| | `SDL3` (default) | `SDL2` | `NULL` | `ALSA` |
|---|---|---|---|---|
| Status | Implemented, default | Implemented as a **transport only** | Implemented, deterministic silent transport | **New**: implemented, native, no SDL |
| OS | Every target CNA supports (Linux, Windows, macOS, iOS, Android, Emscripten) | Whatever SDL 2.30 supports; only proven in the Linux `SDL2 + OpenGLES3` CI cell | All | **Linux only** (configure fails elsewhere) |
| Device class (`IAudioDevice`) | `Sdl3AudioDevice` | `Sdl2AudioDevice` (callback device) | `NullAudioDevice` (paced thread, discards samples) | `AlsaAudioDevice` (`libasound.so.2` loaded at run time; ~10 ms periods x 4) |
| Capture (`Microphone`) | Yes (`Sdl3AudioRecordingDevice`) | **No** (`nullptr` provider) | **No** | Yes (`AlsaAudioRecordingDeviceProvider`, `CNA_AUDIO_RECORDING_DEVICE`) |
| Defines `SOUND_ENABLED` | **Yes** | No | No | **Yes** |
| Mixer engine behind `MixerEngine.hpp` | SDL3_mixer (`MIX_Track`) | none | none | CNA's own `CnaMixer` (linear-interpolation resampler, same track/callback semantics) |
| Decoders on the play path | SDL3_mixer's vendored codecs; Opus/WavPack/mpg123/libvorbisfile/libFLAC/FluidSynth/GME/xmp switched off at build (`ThirdPartySDL.cmake:363-376`); no AAC | none | none | WAV PCM/float/MS-ADPCM/IMA-ADPCM (CNA), Ogg Vorbis (`stb_vorbis`), MP3 (`dr_mp3`), FLAC (`dr_flac`); no Opus, WMA/xWMA, XMA |
| CNA-owned WAV decode for content (`DecodeWavToPcm16`) | Yes | Yes | Yes | Yes |
| Extra link inputs | SDL3, SDL3_mixer | SDL2 | none | ALSA headers at build, `dl` |
| `SoundEffect` construction / `Duration` | Yes | Constructible, but the file-name constructor loads nothing without a mixer (`SoundEffect.cpp:275-292`); `Duration` is reported from decoded WAV data on every platform (commit `6c4a97fff`, NPV-0105) | same as SDL2 | Yes |
| `SoundEffect.Play()` / `SoundEffectInstance` (volume, pitch, pan, loop, pause) | Yes | `Play()` returns false; no mixing | same as SDL2 | Yes |
| `DynamicSoundEffectInstance` | Yes | Compiles; no playback engine | same | Yes |
| `MediaPlayer` / `Song` | Yes | Compiles; no playback | same | Yes (Songs decoded as they play) |
| XACT `AudioEngine`/`SoundBank`/`WaveBank`/`Cue` | Parse + play | Classes compile; no audible engine (mixer-dependent XACT tests are excluded) | same | Parse + play (`AudioCategoryTests` runs on ALSA; tests that read SDL3_mixer track handles stay SDL3-only) |
| 3D audio `Apply3D` (distance/pan approximation, Doppler factor, multi-listener dominant-listener rule) | Applied to mixer track | Math present, nothing audible | same | Applied to CnaMixer track |
| Microphone as XNA `Microphone.All/Start/Stop/BufferReady` | Real SDL3 capture | Unsupported | Unsupported | Real ALSA capture |
| Env knobs | `SDL_AUDIODRIVER` (SDL) | `SDL_AUDIODRIVER` | none | `CNA_AUDIO_DEVICE`, `CNA_AUDIO_RECORDING_DEVICE` |
| CI evidence | platform-ci SDL3 cells (`SDL_AUDIODRIVER=dummy`), apple-ci | platform-ci SDL2 cell (`CnaSdl2AudioDeviceTests`) | platform-ci Headless/Terminal/X11 cells (`WavDecoderTest`, content tests) | `x11-sdl-free-gpu`: `CnaMixer.*`, `AlsaAudioDevice.*`, `AlsaAudioRecordingDevice.*`, `Microphone*`, `AudioCategory*`, `AudioEngine*` on ALSA's `null` device |

Not offered anywhere: OpenAL, WASAPI, CoreAudio, PulseAudio, PipeWire, Web-Audio-specific backends (`OPENAL`, `WASAPI` reserved and refused; the others do not exist). Windows and macOS therefore have **no SDL-free audio path**: SDL-free WIN32 builds must use `NULL` audio (`docs/platform-win32.md:187-196`, untrusted, consistent with `AudioPlatformSelection.cmake`). PipeWire/PulseAudio desktops are reached through ALSA's `default` device plugins (`docs/audio-alsa.md`, untrusted).

Evidence for the XNA-level rows: `#ifdef SOUND_ENABLED` structure of `modules/audio/src/Xna/*.cpp` and `modules/media/src/Xna/MediaPlayer.cpp`; `SoundEffect::Play` returns false without the mixer (`modules/audio/src/Xna/SoundEffect.cpp:~607-610`); the test-exclusion list `cmake/UnitTests.cmake:130-165`; `modules/audio/src/Platform/AudioDeviceFactory.cpp:34-52`.

XNA-level parity notes that apply to every mixer-backed choice (unchanged from alpha.1 unless marked NEW): only the first `PlayWave` per track is honoured; XMA/WMA wave-bank entries log to stderr and return `nullptr`; reverb send is a documented no-op; `.m4a/.aac` unsupported; **NEW** multi-listener `Apply3D` (no longer throws); **NEW** `SoundEffect` MS-ADPCM re-encode via `ConvertFormat`.

## CMake options table

Values are case-normalised where noted. "Ren" = only meaningful when that renderer is selected. All paths are TARGET-relative.

### 4.1 Selection

| Option | Values | Default | Effect | Evidence |
|---|---|---|---|---|
| `CNA_PLATFORM` | `SDL3 SDL2 X11 WAYLAND WIN32 HEADLESS TERMINAL` (list depends on host/packages) | `SDL3` | Platform implementation; reserved `SDL12 EMSCRIPTEN` fail | `cmake/PlatformSelection.cmake:15-114` |
| `CNA_AUDIO_PLATFORM` | `SDL3 SDL2 NULL ALSA` | `SDL3` | Audio implementation; reserved `OPENAL WASAPI` fail; `ALSA` Linux-only | `cmake/AudioPlatformSelection.cmake` |
| `CNA_ENABLE_SDL` | `AUTO ON OFF` (also `TRUE/1`, `FALSE/0/NO`) | `AUTO` | `OFF` = no SDL fetched/built/found; refuses selections needing SDL | `cmake/SdlAvailability.cmake:27-101` |
| `CNA_GRAPHICS_RENDERER` | one of 25 identities: `SDL_RENDERER OPENGLES2 OPENGLES3 OPENGL33 WEBGL1 WEBGL2 VULKAN WEBGPU HEADLESS SOFTWARE STUB DIRECTX11 DIRECTX12 DIRECT2D CANVAS HTML_DOM FREEDIRECT DIRECTX9 SDL_GPU OPENGL4 GDI METAL FNA3D SVG_DOM PORTABLEGL` | Emscripten `WEBGL2`; Linux `OPENGLES3`; else `SDL_RENDERER` | Single/default renderer; retired or unknown names fail by name | `cmake/RendererIdentities.cmake:25-38`; `RendererIdentityDefault.cmake:26-32`; `RendererSelection.cmake:13` |
| `CNA_GRAPHICS_RENDERERS` | `;`-list of compatible identities | empty (= single mode) | Opt-in multi-renderer build; singular option must be a member | `cmake/RendererDefaultSelection.cmake:30-32` |
| `CNA_RENDERER_<NAME>` (25 switches) | `ON/OFF` | `OFF` | Alternative to `CNA_GRAPHICS_RENDERER`; exactly one may be ON; retired `CNA_RENDERER_<RETIRED>=ON` fails by name | `cmake/RendererSelection.cmake:17-73,111-126` |
| Retired renderer names (refused) | `[retired] [retired] [retired] [retired] [retired] [retired] [retired] [retired] [retired] [retired] [retired] [retired] OPEN[retired] [retired] [retired] [retired] [retired] [retired] [retired] [retired] [retired] [retired] [retired] [retired] [retired] [retired]` (C ABI values reserved) | - | Configure `FATAL_ERROR` | `cmake/RendererIdentities.cmake:34-38` |

### 4.2 Feature layers

| Option | Values | Default | Effect | Evidence |
|---|---|---|---|---|
| `CNA_CNAEXT` | ON/OFF | OFF | CNAEXT extended graphics layer | `CMakeLists.txt:176` |
| `CNA_DEVICES` | ON/OFF | OFF | Device/sensor extensions beyond XNA | `CMakeLists.txt:177` |
| `CNA_ENABLE_NET` | ON/OFF | ON | GamerServices + Net (vendored ENet); required by C API | `CMakeLists.txt:178-191,254-257` |
| `CNA_ENABLE_VIDEO` | `OFF AUTO ON` | AUTO | FFmpeg video backend; never on Windows/MinGW/Emscripten/Android/iOS | `CMakeLists.txt:192-202`; `modules/CMakeLists.txt:8-58` |
| `CNA_ENABLE_DRACO` | ON/OFF | ON (OFF under Emscripten) | `KHR_draco_mesh_compression` decoding; ON needs `third_party/draco` submodule | `modules/CMakeLists.txt:77-82` |
| `CNA_USE_SYSTEM_DRACO` | ON/OFF | OFF | Use a system Draco package | `modules/CMakeLists.txt:82` |
| `CNA_CNB_ZSTD` | `AUTO ON OFF` | AUTO | libzstd for `.cnb` chunk compression | `modules/CMakeLists.txt:92-129` |
| `CNA_ENABLE_FONT_PIPELINE` | `OFF AUTO ON` | AUTO | `.spritefont` source route (FreeType, build-time only) | `CMakeLists.txt:105-107` |
| `CNA_ENABLE_MEDIA_PIPELINE` | `OFF AUTO ON` | AUTO | Build-time MP3/WMA/WMV importers | `modules/content-pipeline/CMakeLists.txt:58-60` |
| `CNA_BUILD_INSPECTOR` | ON/OFF | OFF | Inspector agent, bridge, local browser UI; `FATAL_ERROR` on Emscripten/Android/iOS | `CMakeLists.txt:151`; `modules/inspector/CMakeLists.txt:6` |
| `CNA_DIAGNOSTICS` | `OFF STATS FULL` | OFF | Profiler/diagnostics level (`CNA_DIAGNOSTICS_LEVEL=0/1/2`) | `CMakeLists.txt:153-171` |
| `CNA_BUILD_C_API` | ON/OFF | OFF | Experimental native C API; needs `CNA_ENABLE_NET=ON`; C17 | `CMakeLists.txt:78-90,185-191` |
| `CNA_C_API_BUILD_STATIC` | ON/OFF | ON | Static C API archive (Linux, needs Python 3) | `modules/c-api/CMakeLists.txt:343` |
| `CNA_SHARED_LIBRARY` | ON/OFF | ON iff native ELF GNU/Clang and CMake >= 3.27, else OFF (ON elsewhere is fatal) | Link runtime into one `libcna.so` | `CMakeLists.txt:43-73` |

### 4.3 Renderer-specific and effect/bytecode options

| Option | Default | Ren | Effect | Evidence |
|---|---|---|---|---|
| `CNA_EASYGL_COMPILED_EFFECTS` | OFF | GL family | D3D9 Effect Framework bytecode via MojoShader GL adapter | `cmake/RendererSelection.cmake:310` |
| `CNA_VULKAN_COMPILED_EFFECTS` | OFF | VULKAN | same (SPIR-V) | `:331` |
| `CNA_WEBGPU_COMPILED_EFFECTS` | OFF | WEBGPU | same (SPIR-V -> WGSL in browser) | `:352` |
| `CNA_SOFTWARE_COMPILED_EFFECTS` | OFF | SOFTWARE | same | `:380` |
| `CNA_DIRECTX9_COMPILED_EFFECTS` / `CNA_DIRECTX11_...` / `CNA_DIRECTX12_...` | OFF | [retired renderers] | same | `:455`, `:401`, `:416` |
| `CNA_SDL_GPU_COMPILED_EFFECTS` | OFF | SDL_GPU | same | `:495` |
| `CNA_OPENGL4_COMPILED_EFFECTS` | OFF | OPENGL4 | same | `:519` |
| (no option) FNA3D | always on | FNA3D | compiled effects always supported | `cmake/RendererSelection.cmake:538-539` |
| `CNA_SDL_GPU_SHADERCROSS` | ON on Windows/Apple, OFF elsewhere | SDL_GPU | SPIR-V stock shaders through SDL_shadercross | `:477-490` |
| `CNA_WEBGPU_AUTO_DOWNLOAD` / `CNA_WEBGPU_ROOT` / `CNA_WEBGPU_VERSION` | ON / empty / `v29.0.1.1` | WEBGPU | wgpu-native binary release | `cmake/ThirdPartyWebGPU.cmake:12-14` |
| `CNA_FXC_EXECUTABLE` / `CNA_FXC_LAUNCHER` | empty | content tool | Path to an fxc-compatible effect compiler (and e.g. `wine`) | `modules/content-pipeline/CMakeLists.txt:110-113` |
| `CNA_DIRECT2D_TEST_RUNTIME` | `WINE` (or `PROTON`) | DIRECT2D | Cross-compiled Direct2D test runtime | `CMakeLists.txt:206` |
| `CNA_BUILD_CANVAS_HOST_TESTS` / `..._HTML_DOM_HOST_TESTS` / `..._SVG_DOM_HOST_TESTS` | OFF | DOM/Canvas | Native host-side contract tests | `modules/renderers/CMakeLists.txt:203,223,244` |
| `CNA_BUILD_RENDERER_DESCRIPTOR_GATE` | ON | all | Compile every registered family's descriptor | `cmake/RendererDescriptorGate.cmake:24` |

### 4.4 Dependencies, SDL and third-party controls

| Option | Default | Effect | Evidence |
|---|---|---|---|
| `CNA_USE_SYSTEM_SDL` | OFF | Use installed SDL3/SDL3_image/SDL3_mixer instead of submodules | `cmake/ThirdPartySDL.cmake:3,219-225` |
| `CNA_SDL_PREBUILT_ROOT` | `<src>/.sdl-prebuilt-<key>` | Persistent SDL install (survives clean) | `cmake/ThirdPartySDL.cmake:120-129` |
| `CNA_MAX_VENDORED_BUILD_JOBS` | `2` | Parallel jobs for configure-time SDL builds | `cmake/ThirdPartySDL.cmake:8-13,533` |
| `CNA_SDL2_ROOT`, `CNA_SDL2_GIT_REPOSITORY`, `CNA_SDL2_GIT_TAG` | empty, SDL upstream, `fa24d868` | SDL2 source for `CNA_PLATFORM=SDL2` | `cmake/ThirdPartySDL2.cmake:12-18` |
| `CNA_SHARP_RUNTIME_ROOT` | `../sharp-runtime` | sharp-runtime checkout (must be `next`-era) | `CMakeLists.txt:293-304` |
| `SHARP_RUNTIME_COMPONENTS` | CNA closure (B6) | Merged, forced to include the closure | `CMakeLists.txt:264-285` |
| `FETCHCONTENT_SOURCE_DIR_FNA3D` (CMake built-in), `CNA_FNA3D_GIT_REPOSITORY/TAG`, `CNA_PORTABLEGL_GIT_*`, `CNA_SDL_SHADERCROSS_GIT_*` | pinned | Offline/air-gapped or re-pinned third-party fetches | `cmake/ThirdPartyFNA3D.cmake:14-31`, `ThirdPartyPortableGL.cmake:18-20`, `ThirdPartySDLShaderCross.cmake:7-13` |
| `CNA_USE_CCACHE` / `CNA_CCACHE_BASEDIR` | ON / `$CCACHE_BASEDIR` or `<src>/..` | ccache launcher with stable base dir | `CMakeLists.txt:100-147` |

### 4.5 Build quality, tests, tools, examples

| Option | Values | Default | Effect | Evidence |
|---|---|---|---|---|
| `CNA_BUILD_TESTS` | ON/OFF | ON | GoogleTest suites (needs `vendor/googletest`) | `CMakeLists.txt:149`; `cmake/UnitTests.cmake:22-33` |
| `CNA_BUILD_EXAMPLES` | ON/OFF | ON | Demos and module examples | `CMakeLists.txt:175` |
| `CNA_BUILD_BENCHMARKS` | ON/OFF | OFF | Microbenchmarks | `CMakeLists.txt:150` |
| `CNA_TEST_DISPLAY` / `CNA_TEST_ALLOW_LIVE_DISPLAY` | string / ON,OFF | empty / OFF | Display for GPU tests; `:0` needs the second option | `cmake/TestDisplayPolicy.cmake:33-36` |
| `CNA_PLATFORM_CTEST_BINARY` | `CnaTests`, `CnaPlatformModuleTests` | `CnaTests` | Binary the `CnaPlatform*/CnaX11*/CnaWayland*` ctest entries run | `cmake/UnitTests.cmake:1589-1595` |
| `CNA_SANITIZE` | comma list, e.g. `address,undefined`, `thread` | empty | Sanitizers on CNA + sharp-runtime + tests (not vendored SDL/ENet; not MSVC/Emscripten) | `cmake/BuildPerformance.cmake:135-206` |
| `CNA_SANITIZE_OPTIMIZATION` | `DEFAULT O0 O1 O2 O3` | DEFAULT | Optimization override for sanitizer builds | `:137` |
| `CNA_DEBUG_INFO` | `FULL LINE_TABLES SPLIT` | FULL | Debug-info level (not with sanitizers; native GNU/Clang Debug only) | `:131,199-236` |
| `CNA_LINKER` | `AUTO DEFAULT LLD MOLD` | AUTO | Fast linker (native ELF GNU/Clang only) | `:19-100` |
| `CNA_ENABLE_IPO` / `CNA_ENABLE_UNITY_BUILD` / `CNA_ENABLE_PCH` | ON/OFF | OFF / OFF / OFF | LTO, unity pilot (core+math), PCH pilot (content tests) | `:338-341`; `cmake/UnitTests.cmake:11` |
| `CNA_EXPORT_COMPILE_COMMANDS` | ON/OFF | ON | `compile_commands.json` (Ninja/Makefiles) | `:9` |
| `CNA_PLATFORM_RATCHET` / `_STRICT` / `CNA_PLATFORM_HOT_PATH_LINT` | ON/OFF | ON / ON / ON | Configure-time SDL-coupling ratchet (hard error) and hot-path lint (need Python 3; skipped without it) | `cmake/PlatformRatchet.cmake:19-20`; `cmake/PlatformHotPathLint.cmake:15` |
| `CNA_CONFIGURE_AUDIT_CACHE` | ON/OFF | ON | Cache successful configure-time audits by input fingerprint | `cmake/ConfigureAuditCache.cmake:4` |
| `CNA_FX_FUZZER_ENTRY_POINT`, `CNA_XNA_MODEL_FUZZER_ENTRY_POINT`, `CNA_XNA_INTERMEDIATE_FUZZER_ENTRY_POINT` | ON/OFF | OFF | libFuzzer/AFL++ entry points | `cmake/Harnesses.cmake:311,344,366` |

Offline tools built by default when their inputs exist: `cna_content_tool` (executable `cna-content`), `cna_tool_gltf_to_cnj`, `cna_tool_cnj_to_cnb`, `cna_tool_gltf_to_cnb`, `cna_tool_source_to_cnb`, `cna_tool_cnb_info`, `cna_tool_xnb_interop_fixtures` (`cmake/Tool*.cmake`).

### 4.6 Apple, Emscripten, Android

| Option | Default | Effect | Evidence |
|---|---|---|---|
| `CNA_MACOS_DEPLOYMENT_TARGET` / `CNA_IOS_DEPLOYMENT_TARGET` | `13.3` / `16.3` | Deployment floors; lowering is a `FATAL_ERROR` | `cmake/ApplePlatform.cmake:74-104` |
| `CNA_IOS_SIMULATOR` | OFF | With `cmake/toolchains/ios.cmake`: simulator SDK | `cmake/toolchains/ios.cmake:29` |
| `CNA_APPLE_BUNDLE_IDENTIFIER_PREFIX` / `CNA_APPLE_BUNDLE_VERSION` / `CNA_APPLE_DEVELOPMENT_TEAM` | `com.openeggbert.cna` / project numeric version `0.1.0` / empty | Bundle identity, version (no prerelease suffix), signing team | `cmake/ApplePlatform.cmake:109-116` |
| `CNA_APPLE_BUNDLE_MACOS_EXECUTABLES` | OFF | macOS executables as `.app` bundles | `:118` |
| `CNA_BUILD_APPLE_SMOKE_APP` | ON for iOS, OFF otherwise | `cna_ios_smoke` / `cna_macos_smoke` | `cmake/AppleSmoke.cmake:3-5` |
| `CNA_APPLE_ALLOW_UNVALIDATED_RENDERER` | OFF | Experiment outside the iOS allow-list (only `SDL_RENDERER` is on it) | `cmake/ApplePlatform.cmake:250-253` |
| `CNA_ENABLE_EMSCRIPTEN_THREADS` | OFF | Shared-memory pthread ABI; Emscripten-only | `CMakeLists.txt:25-41` |
| (Android) none | - | Standard NDK toolchain variables (`ANDROID_ABI`, `ANDROID_PLATFORM`) are forwarded to the SDL sub-builds | `cmake/ThirdPartySDL.cmake:433-446` |

### 4.7 CMake presets (`CMakePresets.json`, version 3, min CMake 3.20)

18 configure presets (17 visible; hidden `base-ninja` = Ninja + `CNA_EXPORT_COMPILE_COMMANDS=ON` + `CNA_USE_CCACHE=ON`), 17 build presets, **no** test/workflow/package presets. Build directories are `${sourceDir}/cmake-build-<preset>`.

| Configure preset | Renderer | Key settings | Build preset -> target |
|---|---|---|---|
| `dev` | STUB | Debug, tests/examples/C API/net/video/Draco OFF | `dev` -> `cna_tool_cnb_info` |
| `dev-fast-debug` | STUB | `dev` + `CNA_DEBUG_INFO=LINE_TABLES` | `dev-fast-debug` -> `cna_tool_cnb_info` |
| `unit` | STUB | Debug, tests ON, examples/net/video/Draco OFF | `unit` -> `CnaTests`; `unit-core` -> `CnaCoreTests`; `unit-math` -> `CnaMathTests`; `unit-content` -> `CnaContentTests`; `unit-graphics` -> `CnaGraphicsTests` |
| `unit-pch` | STUB | `unit` + PCH | `unit-content-pch` -> `CnaContentTests` |
| `unit-unity` | STUB | `unit` + unity build | `unit-core-math-unity` -> `CnaCoreTests`,`CnaMathTests` |
| `release-modules` | STUB | Release, tests/examples off | `release-modules` -> `cna_tool_cnb_info` |
| `release-ipo` | STUB | `release-modules` + IPO | `release-ipo` -> `cna_tool_cnb_info` |
| `web` | WEBGL2 | Release, examples ON, tests OFF, `EASYGL_BUILD_*` OFF; **no toolchain file: run as `emcmake cmake --preset web`** | `web` -> `cna_house3d_demo` |
| `devices-asan` / `devices-tsan` / `devices-ubsan` | OPENGLES3 | Debug, `CNA_DEVICES=ON`, `CNA_SANITIZE=address` / `thread` / `undefined` respectively | same names -> `CnaTests` |
| `macos` | SDL_RENDERER | Release, tests+examples ON | (none) |
| `ios` / `ios-simulator` | SDL_RENDERER | Release, `ios.cmake` toolchain, tests/examples/net OFF | (none) |
| `tests` | OPENGLES3 | Debug, tests+examples ON | `tests` -> `CnaTests` |
| `multi-renderer` | HEADLESS | `CNA_GRAPHICS_RENDERERS=HEADLESS;SOFTWARE;STUB` | (none) |
| `cnaext` | OPENGLES3 | Debug, `CNA_CNAEXT=ON`, tests ON, examples OFF | `cnaext` -> `CnaTests` |

BASE had 9 configure presets (`web devices-asan devices-tsan devices-ubsan macos ios ios-simulator tests multi-renderer`); the site's "five presets" was already stale at BASE.

## Build/quickstart corrections

Commands currently published on the site, checked against TARGET (static reading; nothing was configured or built). "OK" = valid syntax and target/option exists at TARGET; "WRONG" = would fail, or is materially misleading.

### 5.1 `SITE:index.html` quickstart (lines 116-131)

| Command / statement | Verdict | TARGET truth | Evidence |
|---|---|---|---|
| `git clone https://github.com/libcna/cna.git` | WRONG for TARGET | Default branch is `develop` = alpha.1 commit `1bb2145`. TARGET is branch `next`. Use `git clone -b next` (or wait for a tag). | `git ls-remote --symref` (2026-09-24) |
| `git clone .../libcna/sharp-runtime.git` | WRONG for TARGET | Default `main` (`54578590`, "prepare v0.1.0-beta.1") lacks the `Resources` and `Xml.Serialization` components CNA now requests; use `-b next` (`41b918c9`). | `cmake/SharpRuntimeConsumption.cmake:33-38,60`; `scripts/ci/clone_siblings.sh:5-9` |
| `git clone .../easy-gl.git`, `.../meta-gl.git` | OK | Needed by the default Linux renderer; default branch `develop` matches what CI clones. | `cmake/RendererSelection.cmake:207-235`; `clone_siblings.sh:29-32` |
| `git submodule update --init          # non-recursive is correct` | OK | Confirmed by CMake itself; it fetches five submodules (SDL, SDL_image, SDL_mixer, draco, googletest). | `cmake/ThirdPartySDL.cmake:224-243`; `.gitmodules` |
| `# FFmpeg is required on Linux/macOS, not optional` + `libavcodec-dev ...` | WRONG | Optional. `CNA_ENABLE_VIDEO=AUTO`; video reports `NotSupportedException` when absent. | B5; `VideoDecoderUnavailable.cpp:9-24` |
| `sudo apt install cmake g++ ninja-build pkg-config ...` | Incomplete | CI's Linux jobs also install X11/GL/Vulkan/ALSA/D-Bus/Wayland development packages so the vendored SDL3 gets real video drivers and the GL/Vulkan renderers configure: `libx11-dev libxext-dev libxrandr-dev libxi-dev libxcursor-dev libxfixes-dev libxss-dev libxtst-dev libxkbcommon-dev libgl1-mesa-dev libegl1-mesa-dev libgles2-mesa-dev libvulkan-dev libasound2-dev libudev-dev libdbus-1-dev` (+ `libwayland-dev wayland-protocols`), and use `g++-14`. Minimal sufficient set not measured. `ninja-build` is optional (Makefile default generator). | `.github/workflows/platform-ci.yml:89-101`; `cmake/ThirdPartySDL.cmake:141-186` |
| `cmake -S . -B build -DCNA_GRAPHICS_RENDERER=OPENGLES3` | OK | Valid identity and the Linux default; needs easy-gl+meta-gl. On CMake >= 3.27 the default also enables `CNA_SHARED_LIBRARY` (one `libcna.so`). | `RendererIdentityDefault.cmake:26-32`; `CMakeLists.txt:56-73` |
| `cmake --build build --target CnaTests` | OK | Target exists (aggregate of 22 module test object sets). | `cmake/UnitTests.cmake:478` |
| `ctest --test-dir build --output-on-failure` | Misleading | (a) tests run against the caller's `DISPLAY` (default `CNA_TEST_DISPLAY` empty) and ~a thousand renderer tests open windows; (b) many CTest entries are separate executables that `--target CnaTests` does not build, so an unfiltered run after building only `CnaTests` reports missing binaries (the project's own unfiltered CI does a full `cmake --build`). Use a label/regex, e.g. CI's `xvfb-run -a ctest --test-dir build -L input --output-on-failure`, or `tools/platform/run_gpu_tests_private.sh`. | `cmake/TestDisplayPolicy.cmake:10-23,33`; `general-tests-ci.yml:145-150`; `input-ci.yml` |
| "Get running in 5 minutes" | Unsupported | First configure builds SDL3, SDL3_image and SDL3_mixer from source (persistent `.sdl-prebuilt-*`), and `macos` preset text says "several minutes". No timing was measured. | `cmake/ThirdPartySDL.cmake:14-18`; `CMakePresets.json` preset `macos` description |

### 5.2 `SITE:docs/getting-started.html`

| Statement | Verdict | TARGET truth / evidence |
|---|---|---|
| "C++23-capable compiler: GCC 12+ or Clang 15+ / MSVC 2022 v17.8+" | Unsupported | No version check in CMake (F1); `<format>` used in always-built content-pipeline (F2) so GCC 12 cannot be assumed; CI proves GCC 14, AppleClang (macos-14), MSVC (windows-latest), emsdk 6.0.3, mingw-w64. Clang on Linux and clang-cl are not exercised by any build workflow. |
| "`../easy-gl` directory - only needed for the OPENGLES3 renderer" | WRONG | Needed for all five GL identities (`OPENGLES2 OPENGLES3 OPENGL33 WEBGL1 WEBGL2`) and it requires `../meta-gl` (`RendererSelection.cmake:207-235`). |
| "SDL3, SDL3_image, and SDL3_mixer are built from vendored submodules - no system packages required" | Half true | No SDL packages, but X11/Wayland/GL/audio development headers must exist when SDL is first built or the vendored SDL has no window driver (`ThirdPartySDL.cmake:141-186`). |
| "Disk space ~500 MB (source + build artifacts)" | WRONG for default (tests+examples ON) | `CMakeLists.txt:43-55` records ~104 MB per statically linked test/example executable across 798 executables (~83 GB Debug) before `libcna.so` existed. Only a `CnaTests`-only or preset `dev` build is small. |
| "RAM 4 GB minimum" | Unverified | No source. |
| `git submodule update --init --recursive` (twice) | WRONG | CMake says non-recursive; recursion only pulls unused codec submodules (`ThirdPartySDL.cmake:224-243`). CNA's README still says `--recursive`; the code disagrees. |
| `cmake --build build --target hello-triangle-sdl` | WRONG | No such target at TARGET or BASE (F5). |
| "Only CNA_AUDIO_PLATFORM=SDL3 enables the tag's real XNA mixer" | WRONG | SDL3 **and ALSA** (A2). |
| "SDL2/Headless/Terminal ... opt-in topics" | Incomplete | Also X11, WAYLAND, WIN32, `CNA_ENABLE_SDL`, ALSA. |
| Windows prerequisites "SDL3 built from vendored submodules" | OK | SDL3 shared DLL built at configure (`ThirdPartySDL.cmake:276-281`); native MSVC is only in manual CI. |

### 5.3 `SITE:docs/building.html` (statement -> verdict)

| Statement | Verdict | TARGET truth / evidence |
|---|---|---|
| "FFmpeg is a hard requirement on Linux and macOS... No CMake switch disables it" (callout, Troubleshooting, options) | WRONG | `CNA_ENABLE_VIDEO` (B5). |
| "On Windows, Emscripten and Android FFmpeg is not used... video translation units excluded... compiles and then fails to link" | WRONG | Video/VideoPlayer/VideoReader link everywhere; without FFmpeg they throw `NotSupportedException` at run time. Also excluded: iOS. |
| Sibling table (sharp-runtime, easy-gl+meta-gl, free-direct+free-api) | OK, plus branch note | Add: sharp-runtime `next`; `free-direct`/`free-api` live under `openeggbert/`. |
| "it fetches exactly the four submodules CNA builds" | WRONG | Five (adds `third_party/draco`, needed unless `CNA_ENABLE_DRACO=OFF`); googletest only while tests ON. |
| "50 public renderer identities" | WRONG | 25 (`RendererIdentities.cmake:25-29`). |
| "dead values ... EASYGL, D3D9, D3D11, D3D12, DX3, ASCII" | OK but incomplete | Still unknown values; plus 25 named retired identities (P-table 4.1). "a renderer called [retired] does exist" is WRONG: retired. |
| Combination rules "PortableGL+real OpenGL, GDI+Software, [retired]+any, cross-platform" | Partly wrong | [retired] removed; three rule families; `OPENGL4` counts as real GL (B14). |
| "CNA_PLATFORM accepts SDL3, SDL2, HEADLESS and POSIX-only TERMINAL. CNA_AUDIO_PLATFORM accepts SDL3, SDL2 and NULL" | WRONG | Platform adds `X11 WAYLAND WIN32`; audio adds `ALSA` (P2, A1). |
| "Only the SDL3 audio value defines SOUND_ENABLED" | WRONG | SDL3 and ALSA (A2). |
| "Choose platform and audio independently" (implied free combination) | Incomplete | Hard exclusions P9, P8, P10. `-DCNA_PLATFORM=SDL2` alone now fails (default audio SDL3). |
| "14 are Windows-only ([retired]-12 ladder plus DIRECT2D, [retired], GDI)... METAL macOS-only, WEBGL1/2/CANVAS/HTML_DOM/SVG_DOM/[retired] Emscripten-only, and OPENGLES2/3/OPENGL33/[retired] cannot be selected under Emscripten" | WRONG | Windows-only: `DIRECTX9 DIRECTX11 DIRECTX12 DIRECT2D GDI` (5). Emscripten-only: `WEBGL1 WEBGL2 CANVAS HTML_DOM SVG_DOM` (5). `OPENGLES2/3/OPENGL33` cannot target Emscripten. `RendererCombinations.cmake:27-32`; `RendererSelection.cmake:149-159` |
| "Five presets ship" (web, tests, devices-*) | WRONG | 17 visible configure presets + 17 build presets (section 4.7). |
| Windows cross: `-DCNA_GRAPHICS_RENDERER=DIRECTX9` with mingw toolchain; "[retired] ... `mingw-w64-i686.cmake`" | Command OK; [retired] text WRONG | Toolchain dir has only `mingw-w64.cmake` and `ios.cmake`. |
| "alpha.1 has no automatic MinGW/Wine workflow" | Partly wrong at TARGET | `platform-ci.yml` job `win32-cross` cross-builds the Win32 **platform module** with mingw-w64 and runs it under Wine on every push/PR. Full CNA/DirectX builds are still manual. |
| Web: `cmake --preset web` / `cmake --build --preset web` | Configure command WRONG | Preset has no toolchain file; use `emcmake cmake --preset web` (the preset's own description). Build preset target is `cna_house3d_demo`. |
| "no video" on web | Reworded | Video links but throws at run time. |
| Android command | OK shape | No preset, no CI; demo project pins NDK 30, minSdk 24, arm64-v8a only (B10). |
| Option table: `CNA_GRAPHICS_RENDERER` "Any one of the 50" | WRONG | 25. |
| `CNA_BUILD_C_API` "compile-blocked by a 49-entry C renderer map... NET=OFF fails earlier on GamerServices include" | Stale | NET=OFF is now an explicit configure `FATAL_ERROR`; ABI 0.29.0; buildability at TARGET not verified by me (F10). |
| `CNA_TEST_DISPLAY` default "X display :0" | WRONG | Empty (F7). |
| `[retired]`, `[retired]` | WRONG | Options removed with retired renderers. |
| Options missing from the table | Incomplete | `CNA_ENABLE_SDL`, `CNA_ENABLE_VIDEO`, `CNA_ENABLE_DRACO`, `CNA_SHARED_LIBRARY`, `CNA_ENABLE_NET` (present), 6 more `*_COMPILED_EFFECTS` (9 total), `CNA_DIAGNOSTICS`, `CNA_BUILD_INSPECTOR`, `CNA_DEBUG_INFO`, `CNA_LINKER`, `CNA_ENABLE_IPO/UNITY_BUILD/PCH`, `CNA_MAX_VENDORED_BUILD_JOBS`, `CNA_SDL2_ROOT`, etc. (section 4). |
| "Test labels follow the current renderer names" | OK | Labels unchanged in kind. |
| "CI ... alpha.1 does not have an effective full-suite gate: general-tests-ci.yml still configures the removed EASYGL identity" | WRONG at TARGET | Now `OPENGLES3`; a known-failure allowlist of one test (C2, C3). |
| "C++ framework has no general install()/export()/CPack" | OK | Still true (F9). |
| Troubleshooting: FFmpeg configure failure; "[retired] missing [retired]"; "[retired] ... refuse to configure"; "14 Windows-gated" | WRONG | See above rows. |
| "cmake --build build --target CNA no longer works" | OK | Still true (F4). |

### 5.4 Other command-level facts to publish

- Correct TARGET quickstart requires: `git clone -b next` for `cna` and `sharp-runtime`; `easy-gl` and `meta-gl` default branch; `git submodule update --init`; X11/GL dev packages; `cmake -S . -B build`; `cmake --build build --target cna_demo_2d` (or `CnaTests`); labelled/filtered `ctest` under `xvfb-run -a`.
- SDL-free X11 recipe proven by CI: `cmake -S . -B build -DCNA_ENABLE_SDL=OFF -DCNA_PLATFORM=X11 -DCNA_AUDIO_PLATFORM=NULL -DCNA_GRAPHICS_RENDERER=HEADLESS` (or `ALSA` + `OPENGL33` with `CNA_GRAPHICS_RENDERERS="OPENGL33;VULKAN;SOFTWARE;HEADLESS"`) (`platform-ci.yml:451-465,590-602`).
- Native Wayland recipe (documented, not CI-proven): `-DCNA_PLATFORM=WAYLAND -DCNA_GRAPHICS_RENDERER=HEADLESS` (`docs/platform-wayland.md:20-33`, untrusted; selection logic verified in `PlatformSelection.cmake:61-75`).
- Native Win32 (mingw cross): `-DCMAKE_TOOLCHAIN_FILE=cmake/toolchains/mingw-w64.cmake -DCNA_PLATFORM=WIN32 -DCNA_AUDIO_PLATFORM=NULL -DCNA_GRAPHICS_RENDERER=DIRECTX11 -DCNA_ENABLE_SDL=OFF` (`docs/platform-abstraction.md:31-34`, untrusted; consistent with `PlatformSelection.cmake:27-32`).
- Consuming CNA: `add_subdirectory(<cna>)` and `target_link_libraries(game PRIVATE CNA)`; consumers should set `CNA_BUILD_TESTS=OFF CNA_BUILD_EXAMPLES=OFF` (the Android demo does, `modules/devices/examples/demo_devices/android/.../app/jni/CMakeLists.txt:10-11`); the mobile-eggbert case is cited in `modules/CMakeLists.txt:463-468`.

### 5.5 Toolchain and package facts (what the code names and what CI installs)

| Topic | Fact | Evidence |
|---|---|---|
| CMake | Minimum 3.20 (`cmake_minimum_required`); 3.27+ only matters for the automatic `CNA_SHARED_LIBRARY`; Apple CI passes `CMAKE_POLICY_VERSION_MINIMUM=3.5` for vendored SDL sub-builds under new CMake | `CMakeLists.txt:1,56-60`; `apple-ci.yml:119,159,250` |
| C++ | C++23, no extensions (`CMAKE_CXX_STANDARD 23`, `cxx_std_23`); C17 only for the optional C API | F1, F10 |
| Compilers proven by CI | GCC 14 (Ubuntu 24.04), AppleClang (macos-14), MSVC (windows-latest), mingw-w64 GCC (Win32 cross), Emscripten emsdk 6.0.3 (clang). Clang on Linux appears only in the C header compatibility matrix; clang-cl is not tested | C4, F2 |
| Debian/Ubuntu, Linux windowed build (from the platform/general/input workflows) | `g++-14 cmake ninja-build ccache pkg-config xvfb x11-utils libavcodec-dev libavformat-dev libavutil-dev libswresample-dev libvulkan-dev mesa-vulkan-drivers libgl1-mesa-dev libegl1-mesa-dev libgles2-mesa-dev libx11-dev libxext-dev libxrandr-dev libxi-dev libxcursor-dev libxfixes-dev libxss-dev libxtst-dev libwayland-dev wayland-protocols libxkbcommon-dev libasound2-dev libpulse-dev libudev-dev libdbus-1-dev` (FFmpeg lines are optional for CNA itself) | `.github/workflows/platform-ci.yml:93-101` |
| Native X11 platform | mandatory: `libx11-dev`, `libxext-dev`, `XKBlib.h`; optional (each gates one capability): Xi, Xrandr, Xcursor, Xfixes, Xss, XShm, GLX (`libgl1-mesa-dev`/`libglx-dev`), Vulkan headers, D-Bus headers (`libdbus-1-dev`) | `cmake/PlatformX11.cmake:44-157`; `platform-ci.yml:403-407,573-578` |
| Native Wayland platform | mandatory: `libwayland-dev` (>= 1.18), `libxkbcommon-dev` (>= 0.5), `wayland-protocols` (with `stable/xdg-shell`), `libwayland-bin` (wayland-scanner), `pkg-config`; optional: EGL/wayland-egl/wayland-cursor headers, Vulkan headers, D-Bus headers | `cmake/PlatformWayland.cmake:58-120` |
| ALSA audio | `libasound2-dev` (headers only at build; `libasound.so.2` at run time) | `modules/audio/CMakeLists.txt:22-31` |
| Optional libs | FFmpeg (`libavcodec libavformat libavutil libswresample`), `libzstd` (`CNA_CNB_ZSTD`), FreeType (`CNA_ENABLE_FONT_PIPELINE`), Vulkan SDK (`VULKAN`), OpenGL (`OPENGL4`) | `modules/CMakeLists.txt`; `cmake/RendererSelection.cmake:323,511` |
| macOS | Homebrew `ccache ffmpeg` (CI); floor 13.3; deployment target below floor is fatal | `apple-ci.yml:106,229`; B8 |
| Windows | MSVC (developer environment) + Ninja in CI; no FFmpeg; SDL3 built as DLL at configure; `CNA_SDL_GPU_SHADERCROSS` defaults ON | `d3d-windows-ci.yml:76-81`; B4 |
| Windows cross | `g++-mingw-w64-x86-64` (+ `wine`, `xvfb` to run) | `platform-ci.yml:265-266` |
| Emscripten | emsdk `6.0.3` (pinned), `python3`, `ccache`; Playwright + Chromium for the browser suite | `emscripten-multi-renderer-ci.yml:45,107`; `htmldom-ci.yml:91-97` |
| Android | NDK via toolchain file; demo pins NDK 30.0.14904198, API 24, arm64-v8a; no CI | B10 |
| Python 3 | Needed for configure-time gates (skipped if absent) and the static C API archive; required by many CI gates | B13, F9 |
| Persistent build output | `<source>/.sdl-prebuilt-*` (SDL3 install), never removed by a clean build | P11 |

## CI inventory

Counts: **20 workflow files at TARGET, 21 at BASE**; 28 jobs at TARGET (not counting matrix legs). BASE-only: `[retired]-ci.yml`, `[retired]-cross-platform-ci.yml` (deleted with the retired renderers). TARGET-only: `content-pipeline-windows-ci.yml`. All 18 remaining files were modified. "Auto" = push to `next|develop|main` and PRs targeting them (unless noted); every workflow also has `workflow_dispatch`. All `paths:` filters are as written in the files. All but the two manual-only Windows workflows define a concurrency group that cancels superseded runs.

| # | File (workflow `name:`) | Trigger | Runner | What it builds / runs | What it gates | Notes, known limits |
|---|---|---|---|---|---|---|
| 1 | `32bit-arithmetic-ci.yml` (32-bit Arithmetic Coverage) | Auto, path-filtered (audio tag parser, content exception, software allocation sources, `tools/media/**`, 2 tools) | ubuntu-latest | `tools/media/arithmetic32bit` with `-m32`; runs as a genuine 32-bit binary | 32-bit overflow arithmetic in media/software allocation code | Not a CNA configure |
| 2 | `apple-ci.yml` (Apple platforms) | push path-filtered, PR **unfiltered** | ubuntu-24.04 + macos-14 | Job `apple-cmake-check` (`scripts/check-apple-platform-cmake.sh`); `macos-build` (`SDL_RENDERER`, tests ON, Draco OFF, portable suites, then a self-contained `.app` bundle verified and launched); `ios-build` matrix device/simulator (`cna_ios_smoke`, net OFF, archive/bundle verified, simulator: install + launch, one frame) | macOS build + portable suites; iOS final link + simulator frame | Homebrew `ccache ffmpeg`; `CMAKE_POLICY_VERSION_MINIMUM=3.5`; no physical device |
| 3 | `c-api-abi-baseline.yml` (C API ABI baseline) | Auto, path-filtered (`modules/c-api/include/**`, baseline tool/JSON) | ubuntu-24.04 | `tools/c-api/generate_abi_baseline.py --check`; proves the gate rejects a moved field | Header struct layouts/widths/constants | Does not build the library |
| 4 | `c-api-compat-matrix.yml` (C API compatibility matrix) | Auto, path-filtered | ubuntu-24.04 | Compiles every public C header in each declared language mode of gcc-14, clang, mingw gcc (`gcc-mingw-w64-x86-64`) | Header compatibility matrix | No library build |
| 5 | `c-api-coverage-gate.yml` (C API coverage gate) | Auto, path-filtered (`modules/**/include/**`, mappings) | ubuntu-24.04 | `generate_coverage_inventory.py` vs `docs/c-api/COVERAGE.md` | Public C++ headers mapped to C routes | Needs Doxygen |
| 6 | `c-api-limitations.yml` (C API limitations matrix) | Auto, path-filtered | ubuntu-24.04 | `generate_limitations.py` | Limitations doc freshness | |
| 7 | `c-api-release-gate.yml` (C API release gate) | Auto, path-filtered | ubuntu-24.04 | `tools/c-api/check_release_gate.py --check/--run` plus negative test | Record-vs-measurement of the release criteria. The gate currently says **not ready** and the job passes "while the verdict stands". | No workflow builds `cna_c_api` (`CNA_BUILD_C_API` appears in no workflow) |
| 8 | `content-pipeline-windows-ci.yml` (Content Pipeline Windows CI, MSVC) | **push to branch `content-pipeline-final` only + dispatch** | windows-latest | `CNA_PLATFORM=HEADLESS`, renderer HEADLESS, audio SDL3, net/video/Draco OFF; builds `cna_content_tool`, `CnaContentTests`; CPU pipeline/codec/manifest tests; Unicode CLI + deterministic rebuild hash check | Content pipeline on MSVC | **New at TARGET.** Effectively manual for normal branches |
| 9 | `d3d-windows-ci.yml` (Windows graphics CI: D3D11/D3D12/Direct2D, MSVC) | **`workflow_dispatch` only** | windows-latest | Matrix `DIRECTX11`, `DIRECTX12`, `DIRECT2D`; RelWithDebInfo, tests ON, net OFF; `ctest -L <renderer>`; Direct2D adds debug-layer, WARP, lifetime audits and plan/mutation validators | Native D3D on real Windows | Manual; runner has no GPU display session |
| 10 | `devices-tests.yml` (Devices and Sensors Tests) | Auto, path-filtered (devices sources, `CMakeLists.txt`, `CMakePresets.json`, `cmake/**`) | ubuntu-latest | `cmake --preset devices-ubsan`; Devices/Sensors + CNA::Devices suites; `cna_strict_xna_api_check` | `CNA_DEVICES=ON` under UBSan | Uses default compiler (not gcc-14) |
| 11 | `emscripten-multi-renderer-ci.yml` (Emscripten multi-renderer CI) | Auto (paths-ignore `**.md`, `docs/**`) | ubuntu-24.04 | emsdk `6.0.3`; `emcmake` with `CNA_GRAPHICS_RENDERERS="WEBGL2;CANVAS;HTML_DOM;SVG_DOM"`, Draco OFF; asserts every renderer and the JS selection surface are in the bundle | Web build/link + selection surface | Build/link only; runtime is `htmldom-ci` |
| 12 | `gdi-windows-ci.yml` (GDI Windows CI, MSVC) | **`workflow_dispatch` only** | windows-latest | GDI renderer, focused targets, `ctest -L GDI` | Native GDI | Manual |
| 13 | `general-tests-ci.yml` (general-tests-ci) | Auto (`**` minus `**.md`, `docs/**`, plus `docs/c-api/COVERAGE.md`) | ubuntu-24.04, gcc-14 | Xvfb `:99`; **`OPENGLES3`**, Debug, tests+examples ON; full default build; **unfiltered** `ctest`; build-performance report artifact; `tools/build/check_build_performance_policy.py` | The whole default suite on the EasyGL family | ctest step is `continue-on-error`; a classification step fails the job on any failure except `EasyGL_GraphicsDevice_ReferenceStencil` (1 known). alpha.1's `EASYGL` defect is gone. 90-min timeout |
| 14 | `gltf-renderer-stride-ci.yml` (glTF renderer conformance) | Auto | ubuntu-24.04, gcc-14 | Matrix `STUB HEADLESS OPENGLES3 VULKAN SOFTWARE`: `ctest -L gltf-conformance` + stride tests; job `l7-corpus` (OPENGLES3) against a pinned cna-gltf-viewer | glTF conformance/stride | |
| 15 | `gltf-sanitizers-ci.yml` (glTF sanitizers) | Auto (paths-ignore docs) | ubuntu-24.04, gcc-14 | STUB, ASan+UBSan, Draco ON/OFF; validator fetch, golden regeneration checks, provenance check, `*Gltf*` tests | glTF import memory/UB safety | |
| 16 | `htmldom-ci.yml` (htmldom-ci) | Auto (paths-ignore docs) | ubuntu-24.04 | emsdk `6.0.3`; `HTML_DOM`; Playwright + Chromium under Xvfb; smoke/pixel/stress/dispose suite | HTML_DOM runtime in a real browser | The only browser runtime gate |
| 17 | `input-ci.yml` (input-ci) | Auto (paths-ignore docs) | ubuntu-24.04, gcc-14 | Matrix: `OPENGLES3`, `OPENGLES3` + ASan+UBSan, `SDL_RENDERER`, `VULKAN`; `xvfb-run -a ctest -L input` | Input suite | BASE had 5 rows incl. two `EASYGL` and `[retired]`; all fixed/removed |
| 18 | `metal-macos-ci.yml` (Native Metal renderer, macOS) | push path-filtered, PR unfiltered | macos-14 | `METAL`, tests ON, Draco OFF; `ctest -R '^Metal'` with Metal validation env; compile-definition control test | METAL contract | **Stale push filter**: lists three files that no longer exist (C3) |
| 19 | `multi-renderer-ci.yml` (Multi-renderer CI) | Auto (paths-ignore docs) | ubuntu-24.04, gcc-14 | Registry gates (`scripts/check_renderer_identities.py`, `check_renderer_combinations.py`, `check_runtime_renderer_discipline.py`, `check_renderer_target_discipline.py`); `HEADLESS;SOFTWARE;STUB` build, every renderer reachable at run time, default-in-set check, tests; single-renderer control | Runtime selection + identity registry | |
| 20 | `platform-ci.yml` (Platform implementation matrix) | Auto (paths-ignore docs); job `win32-native` dispatch-only | ubuntu-24.04 (+ windows-latest for one job) | 6 jobs: `platform-contract` (6 legs: SDL3+OPENGLES3, SDL2+OPENGLES3 [audio SDL2], SDL3+VULKAN, SDL3+SOFTWARE, HEADLESS+HEADLESS+NULL, TERMINAL+SOFTWARE+NULL; `CnaPlatformTests`, window tests, cross-implementation event oracle, 2D demo, terminal pseudo-TTY test, 7 source gates); `win32-cross`; `win32-native` (manual); `x11-sdl-free`; `x11-sdl-free-gpu`; `sdl-enable-matrix` (AUTO/ON/OFF x platform; the OFF+SDL3 leg must *fail* with "genuinely requires SDL") | Platform axis, SDL containment, SDL-free X11 (with ALSA) | BASE had only `platform-contract`. **No Wayland job.** Wayland dev packages are installed but tests run under Xvfb |

### 6.1 Coverage observations the site can safely state

- Automatic on every push/PR: Linux (GCC 14) suites for input, glTF, general default suite, platform matrix, multi-renderer selection, devices (UBSan), native X11 SDL-free with and without GPU; macOS and iOS (build/simulator) lanes; HTML_DOM in Chromium; Emscripten multi-renderer build.
- Manual only: native MSVC D3D11/D3D12/Direct2D, GDI, Win32 backend on MSVC, content pipeline on MSVC (branch trigger).
- Not exercised by any workflow: native Wayland, SDL2 outside Linux, Android, tvOS, `CNA_BUILD_C_API=ON` builds, Clang on Linux (except C header compat), `CNA_ENABLE_VIDEO=OFF` on Linux, full CNA + DirectX under Wine/MinGW (only the platform module), GPU pixel/oracle corpus.
- Not one workflow provides a physical-GPU or real-desktop run: Linux GPU tests use Mesa software drivers on Xvfb.
- Runner images: `ubuntu-24.04`, `ubuntu-latest`, `macos-14`, `windows-latest`.
- Eight workflows are configured against a sharp-runtime revision that predates CNA's current component closure (C6); treat them as *configured*, not *passing*.

### 6.2 sharp-runtime revision used by each workflow (see C6)

| Workflow | How sharp-runtime is obtained | Contains `Resources` / `Xml.Serialization`? |
|---|---|---|
| platform-ci, general-tests-ci, input-ci, multi-renderer-ci, gltf-renderer-stride-ci, gltf-sanitizers-ci, c-api-coverage-gate, c-api-limitations, c-api-release-gate | `scripts/ci/clone_siblings.sh`: first existing branch among head/base/ref names, else `next`, else `develop` | Yes when it lands on `next` (a push to `next` does) |
| emscripten-multi-renderer-ci, htmldom-ci, devices-tests | `actions/checkout` pinned `bc8dbf41...` (2026-08-15) | No |
| apple-ci (macOS, iOS), metal-macos-ci | pinned `f23ded28...` (2026-08-15) | No |
| content-pipeline-windows-ci | pinned `df1b42ab...` (sharp-runtime `develop` tip) | No |
| d3d-windows-ci, gdi-windows-ci | default branch (`main`) | No |
| 32bit-arithmetic-ci, c-api-abi-baseline, c-api-compat-matrix | not needed | n/a |

Consequence for the site: do not claim the Emscripten, HTML_DOM, Apple, Metal, Devices or Windows lanes as *currently passing* at TARGET without a recorded run; say what each lane is configured to do.

### 6.3 Scripts that act as gates

| Gate | Where it runs | What it enforces |
|---|---|---|
| `tools/platform/sdl_inventory.py`, `sdl_classify.py`, `renderer_sdl_audit.py`, `sdl_ratchet.py --strict`, `nonproduction_sdl_audit.py`, `check_contract.py`, `hot_path_lint.py` | platform-ci HEADLESS leg; ratchet/lint also at configure (`PlatformRatchet.cmake`, `PlatformHotPathLint.cmake`) | SDL stays confined to `modules/platform`; renderer SDL allow-list; no platform calls in hot loops; contract shape |
| `scripts/check_renderer_identities.py`, `check_renderer_combinations.py`, `check_runtime_renderer_discipline.py`, `check_renderer_target_discipline.py`, `check_renderer_descriptors.py`, `check_removed_renderer_api.py` | multi-renderer-ci and configure (`RendererDescriptorGate.cmake`) | One canonical identity table across CMake/C++/C ABI; combination rules mirrored in docs; retired renderer names/API stay gone |
| `tools/build/check_build_performance_policy.py` | general-tests-ci | Build-speed policy |
| `scripts/check-apple-platform-cmake.sh` | apple-ci | Apple CMake layer without a Mac |
| `scripts/check_test_display_isolation.py`, `cmake/TestDisplayPolicy*.cmake` tests | ctest (`CnaTestDisplayIsolation`, `CnaTestDisplayPolicy_*`) | No test opens windows on the owner's live display |
| `tools/c-api/*` (5 workflows) | c-api-*.yml | ABI baseline, header matrix, coverage, limitations, release gate |
| `scripts/check_module_link_closure.py`, `cmake/Tests/*.cmake` script-mode tests (e.g. `WaylandPlatformSelection.cmake`, `Sdl2OnlyRendererGate.cmake`, `SdlOffFindPackage.cmake`, `RendererRetiredIdentityCase.cmake`) | ctest | Selection contracts fail loudly, not silently |

## Corrections to existing site claims

Each row: page and HTML line where the old claim (or its nearest text) lives at the time of this audit, the claim, what is true at TARGET, and the evidence. Fact ids (F, P, A, B, C, Headline) refer to sections 0-1 of this file. Renderer-count corrections (50/46 -> 25/21) are recorded here only where they appear beside platform/build/CI text; the renderer sheet owns the renderer detail.

| Page:line | Old claim (short quote) | TARGET truth | Evidence |
|---|---|---|---|
| `SITE:index.html:137` | stat "4 Platform implementations" | 7: SDL3, SDL2, X11, WAYLAND, WIN32, HEADLESS, TERMINAL (X11/WAYLAND/WIN32 new; TERMINAL POSIX-only, WIN32 Windows-only, X11/WAYLAND need dev packages) | P2, `cmake/PlatformSelection.cmake:27-65` |
| `SITE:index.html:138` | stat "3 Audio platform choices"; tooltip "only SDL3 enables the alpha.1 XNA playback/mixer path" | 4: SDL3, SDL2, NULL, ALSA. `SOUND_ENABLED` for SDL3 and ALSA | A1, A2, `cmake/AudioPlatformSelection.cmake:17`, `modules/CMakeLists.txt:270-276` |
| `SITE:index.html:141` | stat "21 CI workflow files"; tooltip about stale EASYGL rows | 20 files; no invalid renderer identity remains in any workflow | C1, C2, section 6 |
| `SITE:index.html:135` | stat "50 Renderer identities" | 25 public identities (renderer sheet owns the detail) | `cmake/RendererIdentities.cmake:25-29` |
| `SITE:index.html:136` | stat "46 Implementation families" | 21 families under `modules/renderers` | `modules/CMakeLists.txt:441-444` |
| `SITE:index.html:134` | stat "0.1.0 alpha.1 release" and hero "tag v0.1.0-alpha.1" | TARGET is the tip of `next` (not tagged) and still reports 0.1.0-alpha.1; `main`/`develop` = alpha.1. Decide what revision the site documents | Headline 1, F3 |
| `SITE:index.html:179` | "CNA_PLATFORM selects SDL3, real SDL2, Headless or POSIX Terminal ... CNA_AUDIO_PLATFORM ... SDL3, SDL2 or Null. At alpha.1 only SDL3 enables SOUND_ENABLED" | CNA_PLATFORM also X11, WAYLAND, WIN32; CNA_AUDIO_PLATFORM also ALSA; SOUND_ENABLED for SDL3 and ALSA; add CNA_ENABLE_SDL and hard SDL2/SDL3 exclusions | P2, A1, A2, P9, P10 |
| `SITE:index.html:299` | quickstart clone of `cna` (default branch) | Default branch is alpha.1; TARGET needs `-b next` | Headline 1 |
| `SITE:index.html:300` | quickstart clone of `sharp-runtime` (default branch) | TARGET needs sharp-runtime `next` (components `Resources`, `Xml.Serialization`) | Headline 2, B1, B2 |
| `SITE:index.html:306` | "# 2. System packages (FFmpeg is required on Linux/macOS, not optional)" | FFmpeg optional (`CNA_ENABLE_VIDEO=AUTO`); missing: X11/GL/audio dev packages | B5, section 5.1 |
| `SITE:index.html:315` | "# 4. Run the tests ctest --test-dir build --output-on-failure" | Needs a DISPLAY and a full build; filter with `-L`/`-R` under `xvfb-run -a` | F7, F8 |
| `SITE:index.html:297` | "Get running in 5 minutes" | First configure builds SDL3/SDL3_image/SDL3_mixer; unmeasured | `cmake/ThirdPartySDL.cmake:14-18` |
| `SITE:docs/platforms.html:139` | CNA_PLATFORM row: implemented `SDL3, SDL2, HEADLESS, TERMINAL`; "SDL12, WIN32 and EMSCRIPTEN are reserved" | Implemented: SDL3 SDL2 X11 WAYLAND WIN32 HEADLESS TERMINAL; reserved: SDL12, EMSCRIPTEN (WIN32 is reserved only off Windows, TERMINAL only on Windows) | P2, P3, `cmake/PlatformSelection.cmake:85-107` |
| `SITE:docs/platforms.html:140` | CNA_AUDIO_PLATFORM row: `SDL3, SDL2, NULL`; "Only SDL3 defines SOUND_ENABLED"; "OPENAL, WASAPI and ALSA are reserved and rejected" | Implemented: SDL3 SDL2 NULL ALSA; reserved: OPENAL WASAPI; SOUND_ENABLED for SDL3 and ALSA | A1, A2, `cmake/AudioPlatformSelection.cmake:17,21` |
| `SITE:docs/platforms.html:162` | warning "SOUND_ENABLED is defined only for CNA_AUDIO_PLATFORM=SDL3... Null is therefore useful for deterministic configuration" | Still true for SDL2/NULL; ALSA now has a real mixer (CnaMixer) and SOUND_ENABLED | A2, A5, `modules/CMakeLists.txt:270-276` |
| `SITE:docs/platforms.html:184` | "the tag has no automatic MinGW/Wine workflow" | `platform-ci.yml` job `win32-cross` cross-builds the Win32 platform module with mingw-w64 and runs it under Wine on push/PR (not the full engine) | P16, `platform-ci.yml:245-311` |
| `SITE:docs/platforms.html:196` | Linux row: "the large majority of the 50" renderers | 25 identities; Linux-selectable = everything except Windows-only (5), macOS-only (1), Emscripten-only (5) | B14 |
| `SITE:docs/platforms.html:202` | Windows row: "The 14 Windows-only renderers" | 5: DIRECTX9 DIRECTX11 DIRECTX12 DIRECT2D GDI | `cmake/RendererCombinations.cmake:27` |
| `SITE:docs/platforms.html:208` | Web row: "WEBGL1, WEBGL2, CANVAS, HTML_DOM, SVG_DOM, [retired]" | 5 identities ([retired] retired) | `cmake/RendererCombinations.cmake:31` |
| `SITE:docs/platforms.html:242` | Linux: "the FFmpeg development packages, which are mandatory here" | Optional (AUTO) | B5 |
| `SITE:docs/platforms.html:245` | Windows: "14 renderers refuse to configure anywhere else - the [retired] to DIRECTX12 ladder plus DIRECT2D, [retired] and GDI. [retired] additionally needs a 32-bit i686 toolchain" | 5 renderers; no [retired], no i686 toolchain file | B11, B14 |
| `SITE:docs/platforms.html:254` | "There is no video on Windows... Video and VideoPlayer are missing symbols. Calling code compiles and then fails to link" | They link; without FFmpeg they throw `NotSupportedException` at run time. FFmpeg is still never built for Windows | B5, `VideoDecoderUnavailable.cpp:9-24` |
| `SITE:docs/platforms.html:255` | "The MinGW cross-build itself is not covered by CI. No workflow builds a MinGW target or runs anything under Wine" | Partly wrong: `win32-cross` (platform module only) and `c-api-compat-matrix.yml` (mingw gcc header check) do | P16, section 6 rows 4 and 20 |
| `SITE:docs/platforms.html:259` | "Six renderers are Emscripten-only - WEBGL1, WEBGL2, CANVAS, HTML_DOM, SVG_DOM and [retired]" | Five (no [retired]) | `cmake/RendererCombinations.cmake:31` |
| `SITE:docs/platforms.html:271` | Web: "the video translation units are excluded from Emscripten builds... fail to link" | Links; throws at run time | B5 |
| `SITE:docs/platforms.html:275` | macOS: "the one automatic non-Linux native CI job in the project"; "FFmpeg is a hard requirement on macOS" | macOS is one of several automatic non-Linux lanes (apple-ci macOS build+bundle launch, iOS device+simulator, metal-macos-ci); FFmpeg optional (AUTO; CI installs it via Homebrew) | section 6 rows 2, 18 |
| `SITE:docs/platforms.html:276` | (same sentence) | FFmpeg optional | B5 |
| `SITE:docs/platforms.html:290` | "The tag contains 21 GitHub Actions workflow files... intended unfiltered general job and two Input matrix rows pass the removed EASYGL value and fail" | 20 files; EASYGL rows fixed; C API workflows do not build the library | C1, C2, section 6 |
| `SITE:docs/platforms.html:300` | CI table row for platform-ci.yml: "Platform abstraction and SDL2/SDL3/Headless/Terminal combinations" | Also native X11 SDL-free (no GPU and with GPU+ALSA), Win32 cross under Wine, `CNA_ENABLE_SDL` matrix; no Wayland | section 6 row 20 |
| `SITE:docs/platforms.html:322` | "Where video is available: exist on Linux and macOS only... link error" | Present in every build; functional only when FFmpeg is found (never on Windows/Emscripten/Android/iOS) | B5 |
| `SITE:docs/audio.html:119` | Overview: "SDL3 is the default and the only choice that defines SOUND_ENABLED and links the SDL3_mixer engine" | SDL3 (SDL3_mixer) and ALSA (CnaMixer) both define it | A2, A3 |
| `SITE:docs/audio.html:119` | "real playback likewise requires the SDL3 choice" (XACT) | Requires a mixer: SDL3 or ALSA | A10, `cmake/UnitTests.cmake:130-165` |
| `SITE:docs/audio.html:104` | Section title "Tier 1 - Implemented playback (SDL3_mixer)"; "SDL3_mixer decodes the audio file progressively" | Backend is SDL3_mixer or CNA's own mixer; under ALSA Songs decode as they play via stb_vorbis/dr_mp3/dr_flac | A5 |
| `SITE:docs/audio.html:287` | XACT note: "Cue plays the result back through SDL3_mixer" | SDL3_mixer or CnaMixer | A3 |
| `SITE:docs/audio.html:323` | Cue table row: "Real playback through SDL3_mixer" | SDL3_mixer or CnaMixer | A3 |
| `SITE:docs/audio.html:340` | "Microphone is implemented using real SDL3 capture devices" | SDL3 capture and ALSA capture (`CNA_AUDIO_RECORDING_DEVICE`); none on SDL2/NULL | A7 |
| `SITE:docs/audio.html:115` | "31 audio test sources with 689 statically discoverable definitions" | Counts changed (ALSA/CnaMixer/WavDecoder suites added); recompute in the test-count sheet | `modules/audio/tests` |
| `SITE:docs/faq.html:209` | "Fourteen renderers are Windows-only... [retired] to DIRECTX12, plus DIRECT2D, [retired] and GDI... WEBGL1, WEBGL2, CANVAS, HTML_DOM, SVG_DOM and [retired] are Emscripten-only" | Windows-only 5; Emscripten-only 5; macOS-only METAL | B14 |
| `SITE:docs/faq.html:226` | "CNA's 21 workflows still do not cover every identity" | 20 workflows | C1 |
| `SITE:docs/faq.html:237` | "video is absent from Windows builds entirely... fail to link" | Links; run-time `NotSupportedException` without FFmpeg | B5 |
| `SITE:docs/faq.html:247` | macOS answer: "FFmpeg is a hard build requirement on macOS as it is on Linux" | Optional | B5 |
| `SITE:docs/faq.html:259` | Browser answer: "six identities: WEBGL2, WEBGL1, CANVAS, HTML_DOM, SVG_DOM and [retired]"; "There is no video... fail to link" | Five identities; video throws at run time | B14, B5 |
| `SITE:docs/faq.html:277` | CI answer: "21 workflow files... The C API final target is compile-blocked" | 20 files; C API library not built in CI | C1, section 6 |
| `SITE:docs/faq.html:323` | "On Linux and macOS you also need the FFmpeg development packages... configure fails without them" | Optional; missing X11/GL/audio dev packages instead | B5 |
| `SITE:docs/faq.html:329` | "CNA_PLATFORM selects SDL3, real SDL 2.30, Headless or POSIX Terminal; CNA_AUDIO_PLATFORM independently accepts SDL3, SDL2 or Null. only SDL3 audio defines SOUND_ENABLED" | Native X11, Wayland and Win32 platforms need no SDL (`CNA_ENABLE_SDL=OFF`); audio adds ALSA (SDL-free, has a mixer); SOUND_ENABLED for SDL3 and ALSA | P2, P10, A1, A2 |
| `SITE:docs/faq.html:343` | "50 built-in type readers (49 in a build without FFmpeg, which drops VideoReader)" | VideoReader is registered in every build (no FFmpeg gate); reader total to be re-counted by the XNB sheet | `modules/content/src/Xnb/XnbBuiltInReaders.cpp:19`; `cmake/UnitTests.cmake:219` |
| `SITE:docs/faq.html:371` | XACT answer: "with the default CNA_AUDIO_PLATFORM=SDL3... SDL2/Null audio selections omit that mixer-dependent engine" | SDL3 or ALSA | A2 |
| `SITE:docs/faq.html:372` | "3D audio supports exactly one AudioListener and a second one throws" | Any positive listener count is accepted (dominant nearest listener decides) | A9, `SoundEffectInstance.hpp:363-392` |
| `SITE:docs/faq.html:383` | custom-shader answer lists `[retired]`, `[retired]`, `[retired]`, `[retired]`, `[retired]` | Retired renderers (renderer sheet) | `cmake/RendererIdentities.cmake:34-38` |
| `SITE:docs/faq.html:307` | sibling-repo answers (sharp-runtime, easy-gl) | Add branch requirement (sharp-runtime `next`), `free-direct`/`free-api` under `openeggbert/` | B1, B2 |
| `SITE:docs/releases.html:101` | "Current documented release: 0.1.0-alpha.1 - tagged 20 August 2026" | Still the last tag; TARGET is untagged `next` reporting the same version string | Headline 1, F3 |
| `SITE:docs/releases.html:149` | "declares its own ABI identity: 0.7.0 at this tag... 49 entries against the canonical 50, with [retired] missing" | C ABI is 0.29.0 at TARGET; [retired] is retired (value 50 reserved); C renderer maximum 46; release gate says not ready (1 criterion unmet). Buildability not verified | F10, `modules/c-api/include/CNA/C/abi.h:34-40`, `docs/c-api/RELEASE_GATE.md:9-20` |
| `SITE:docs/releases.html:159` | "Exact source boundary: ae0be4b... through 1bb2145" | New boundary: 1bb2145 .. 009d40f | Header of this sheet |
| `SITE:docs/runtime-renderer-selection.html:105` | "[retired] cannot be combined with another renderer because it pins the build to the 32-bit [retired] ABI" | [retired] retired; rule gone. Remaining rules: PORTABLEGL + real GL (now includes OPENGL4), GDI + SOFTWARE, cross-OS partitions | B14, `cmake/RendererCombinations.cmake` |
| `SITE:docs/runtime-renderer-selection.html:105` | "PORTABLEGL + a real-OpenGL family is rejected" | Still true; real-GL set is `OPENGLES2 OPENGLES3 OPENGL33 WEBGL1 WEBGL2 OPENGL4` | `cmake/RendererCombinations.cmake:16-19` |
| `SITE:docs/runtime-renderer-selection.html:105` | partition sentence | Windows-only: 5; Emscripten-only: 5; macOS-only: METAL | B14 |
| `SITE:features.html:68` | intro: "adds 50 renderer identities in 46 families, ... independent platform/audio implementations" | 25 identities / 21 families; platform axis now includes three native backends and SDL-free builds | P2, `modules/CMakeLists.txt:441-444` |
| `SITE:features.html:125` | Input: "GamePad is a real SDL3 bridge with rumble..." | SDL3 bridge on the SDL3 platform; native X11/Wayland read gamepads through kernel evdev (Linux); Win32 and SDL2 platforms expose no gamepad | P7, section 2.3 |
| `SITE:features.html:227` | Media: "MediaPlayer genuinely plays songs through SDL3_mixer... VideoPlayer genuinely decodes video through FFmpeg" | Songs through SDL3_mixer or CnaMixer (ALSA); video only when FFmpeg is found | A3, B5 |
| `SITE:features.html:151` | XNB: "50 built-in readers with FFmpeg and 49 without video... VideoReader follows FFmpeg availability" | VideoReader registered regardless; re-count in XNB sheet | see faq.html row |
| `SITE:features.html:228` | "the three video translation units are excluded from the build entirely on Windows, Emscripten and Android... fails to link... FFmpeg is a hard requirement on Linux and macOS" | Optional AUTO; unavailable-backend fallback links everywhere; iOS also excluded | B5 |
| `SITE:features.html:270` | "The IPlatform layer also has real SDL2, Headless and POSIX Terminal implementations" | Also native X11, Wayland, Win32 | P2 |
| `SITE:features.html:277` | "CNA_AUDIO_PLATFORM independently selects SDL3, SDL2 or Null... Only SDL3 defines SOUND_ENABLED" | SDL3, SDL2, NULL, ALSA; SOUND_ENABLED: SDL3 and ALSA | A1, A2 |
| `SITE:features.html:443` | Linux: "FFmpeg video decoding is available on Linux and macOS, but not on Windows, Emscripten or Android" | Reword: FFmpeg-backed video is optional and only built for Linux/macOS when found | B5 |
| `SITE:features.html:464` | (Emscripten) "A real path with six identities: WEBGL1/2, Canvas, HTML DOM, SVG DOM and [retired]" | Five identities | B14 |
| `SITE:features.html:482` | "CNA targets C++23 throughout. Requires GCC 12+, Clang 15+, or MSVC 2022 v17.8+" | No enforced or CI-proven minimum below GCC 14 / current AppleClang / MSVC (windows-latest) / emsdk 6.0.3; `<format>` is used | F1, F2 |
| `SITE:features.html:499` | "21 GitHub Actions workflow files... EASYGL... C API final implementation independently blocked" | 20 files; EASYGL fixed | C1, C2 |
| `SITE:about.html:73` | "Its 21 workflow files cover important Linux, Apple/Metal, Emscripten..." | 20 files | C1 |
| `SITE:about.html:140` | "Language: C++23 - requires GCC 12+, Clang 15+, or MSVC 2022 v17.8+" | see features.html row | F1, F2 |
| `SITE:about.html:141` | "Platform implementations: SDL3 by default, real SDL 2.30, Headless, or POSIX Terminal through CNA_PLATFORM" | Also X11, WAYLAND, WIN32 | P2 |
| `SITE:about.html:143` | "Audio-device selection: SDL3, SDL2 or Null... only SDL3 enables alpha.1's high-level XNA playback/decoding engine" | Also ALSA; SDL3 and ALSA enable the mixer | A1, A2 |
| `SITE:about.html:147` | "Video translation units are present for Linux and macOS and excluded on Emscripten, Android and Windows in alpha.1" | FFmpeg optional; API always linked | B5 |
| `SITE:about.html:91` | "Alpha.1 contains Linux, Windows, macOS, Emscripten and Android paths, plus narrow experimental iOS" | Still accurate; add native X11/Wayland/Win32 and SDL-free builds | section 2.5 |
| `SITE:architecture.html:106` | ASCII diagram: "CNA_PLATFORM: SDL3 . SDL2 . HEADLESS . TERMINAL" / "CNA_AUDIO_PLATFORM: SDL3 . SDL2 . NULL" | Add X11, WAYLAND, WIN32 / ALSA | P2, A1 |
| `SITE:architecture.html:145` | "46 implementation families carrying 50 identities" | 21 families / 25 identities | `modules/CMakeLists.txt:441-444` |
| `SITE:architecture.html:147` | "Audio-device code may independently be SDL3, SDL2 or Null; only SDL3 defines SOUND_ENABLED" | Add ALSA; SOUND_ENABLED SDL3+ALSA; native backends contain no SDL | A2, P5 |
| `SITE:architecture.html:158` | Platform service contract list includes "Audio initialisation - SDL3_mixer setup" | Audio is a separate axis (`cna_audio`), not part of `IPlatform` | `modules/audio/CMakeLists.txt`; `modules/platform/include/CNA/Platform/IPlatform.hpp` |
| `SITE:architecture.html:171` | "CNA depends on two sibling C++ libraries" (sharp-runtime + easy-gl); "easy-gl ... required only for the OPENGLES3 renderer" | sharp-runtime always; easy-gl (+meta-gl) for five GL identities; free-direct(+free-api) for FREEDIRECT; FNA3D/wgpu-native/PortableGL/SDL2 fetched when selected | B1, B4 |
| `SITE:architecture.html:258` | "[retired] is fetched via CMake FetchContent" | [retired] retired | `cmake/RendererIdentities.cmake:34` |
| `SITE:roadmap.html:74` | "exposes 50 renderer identities across 46 implementation families" | 25 / 21 | `modules/CMakeLists.txt:441-444` |
| `SITE:roadmap.html:186` | "21 workflow files... the C API final target separately fails its 49-versus-50 renderer-map assertion" | 20 files; C API not built in CI; renderer-map claim to be re-verified | C1, F10 |
| `SITE:roadmap.html:135` | "50 built-in readers with FFmpeg, 49 without it" | VideoReader always registered | see faq.html row |
| `SITE:roadmap.html:230` | "video is not compiled into every target" | Video API compiled into every target; decoding needs FFmpeg | B5 |
| `SITE:docs/roadmap.html:223` | "Alpha.1 has 21 workflow files... Expanding automatic Windows and platform-combination coverage" | 20 files; platform-combination coverage now exists (platform-ci); automatic native Windows still absent | C1, section 6.1 |
| `SITE:docs/roadmap.html:124` | "Renderers - 50 identities, 46 families" | 25 / 21 | `modules/CMakeLists.txt:441-444` |
| `SITE:documentation.html:101` | "Platforms: ... SDL3/SDL2/Headless/Terminal host-platform and SDL3/SDL2/Null audio selections" | Add X11/Wayland/Win32, ALSA, SDL-free builds | P2, A1 |
| `SITE:documentation.html:107` | "all 50 selectable renderers" | 25 | `cmake/RendererIdentities.cmake:25-29` |
| `SITE:documentation.html:119` | "ABI 0.7.0 source surface... alpha.1's 49-versus-50 renderer-map compile blocker" | ABI 0.29.0; gate "not ready" | F10 |
| `SITE:documentation.html:246` | "VideoPlayer and Song. FFmpeg-backed, desktop only." | Linux/macOS when FFmpeg found; API linked everywhere | B5 |
| `SITE:documentation.html:289` | "SDL3 is CNA's platform foundation" | SDL3 is the default platform and the only one on macOS/iOS/Android/Emscripten; Linux/Windows can run without SDL | P2, P10 |
| `SITE:docs/tutorials/01-introduction.html:110` | "runs on Linux, Windows, Android, and the web through SDL3" | Add macOS/iOS; SDL3 is default, not the only route (native X11/Wayland/Win32) | P2 |
| `SITE:docs/tutorials/01-introduction.html:113` | "50 built-in type readers (49 without FFmpeg, which drops the video reader)" | VideoReader always present | see faq row |
| `SITE:docs/tutorials/01-introduction.html:121` | "50 renderer identities across 46 implementation families"; "one of the 50" | 25 / 21 | `cmake/RendererIdentities.cmake:25-29` |
| `SITE:docs/tutorials/02-setup.html:114` | Prerequisites table: "GCC 12+ or Clang 15+; MSVC 2022 v17.8+"; "If GCC 12 is not the default ... CNA_GRAPHICS_RENDERER"; "select your kit (GCC 12 or Clang 15)" | Unsupported minimum (F1, F2); CI uses GCC 14 | F1, F2 |
| `SITE:docs/tutorials/02-setup.html:119` | "OS: Linux (Ubuntu 22.04+, Fedora 36+, Arch), Windows 10+, macOS 12+ (experimental)" | macOS floor is 13.3 (hard error below); Ubuntu 22.04 ships GCC 11 (needs a newer compiler); Windows floor not enforced (Win32 backend API level 0x0603) | B8, P14 |
| `SITE:docs/tutorials/02-setup.html:127` | "FFmpeg is a hard requirement... configure fails outright" | Optional | B5 |
| `SITE:docs/tutorials/02-setup.html:282` | "CMake presets - web, tests, devices-asan, devices-tsan and devices-ubsan" | 17 visible presets (section 4.7) | section 4.7 |
| `SITE:docs/tutorials/02-setup.html:134` | apt/dnf package lists | Add X11/GL/Vulkan/ALSA/D-Bus dev packages for a windowed build; FFmpeg optional | section 5.1 |
| `SITE:docs/tutorials/03-first-window.html:250` | "SDL3, SDL3_image, and SDL3_mixer are linked as static libraries built from submodules" | Shared on Linux/macOS/Windows/Android; static only on Emscripten and iOS | P11, `cmake/ThirdPartySDL.cmake:262-305` |
| `SITE:docs/tutorials/03-first-window.html:160` | "in this default SDL3 platform/audio configuration, links SDL3 transitively" | Additionally, with CMake >= 3.27 on native Linux, `CNA` resolves to `libcna.so` (`CNA_SHARED_LIBRARY`) | B12 |
| `SITE:docs/tutorials/03-first-window.html:275` | troubleshooting row "Configure fails on libavcodec ... required with no opt-out" | Delete; optional | B5 |
| `SITE:docs/tutorials/14-sound-effects.html:99` | "requires CNA_AUDIO_PLATFORM=SDL3, the only alpha.1 selection that defines SOUND_ENABLED" | SDL3 or ALSA | A2 |
| `SITE:docs/tutorials/14-sound-effects.html:218` | "passing more than one listener throws NotSupportedException" | Accepted; dominant (nearest) listener decides | A9 |
| `SITE:docs/tutorials/15-background-music.html:99` | same | SDL3 or ALSA | A2 |
| `SITE:docs/tutorials/15-background-music.html:317` | MediaLibrary "probes track durations through FFmpeg" | Only when FFmpeg is found (`AudioDurationProbeUnavailable.cpp` otherwise) | `modules/media/CMakeLists.txt:7-13` |
| `SITE:docs/tutorials/20-build-run.html:145` | "fourteen renderers are gated to a Windows configure" | 5 | B14 |
| `SITE:docs/tutorials/20-build-run.html:167` | "CNA supports Emscripten 3.1+" | Only emsdk 6.0.3 is exercised (CI); older versions unproven | B9 |
| `SITE:docs/tutorials/20-build-run.html:218` | "No video playback. The video translation units are excluded... fail at link time" | Links; throws at run time | B5 |
| `SITE:docs/tutorials/20-build-run.html:225` | "Install Android NDK r25+ and Android SDK with API level 24+" | API 24 confirmed by the demo; the demo pins NDK 30.0.14904198; r25+ unproven | B10 |
| `SITE:docs/tutorials/80-cross-platform.html:131` | macOS row: METAL "has an automatically triggered macos-14 CI job - the only renderer that does" | apple-ci also builds SDL_RENDERER on macOS and iOS automatically | section 6 row 2 |
| `SITE:docs/tutorials/80-cross-platform.html:149` | iOS row: "No toolchain file exists" | `cmake/toolchains/ios.cmake` exists; iOS is experimental with CI final-link + simulator launch (`SDL_RENDERER` only, floor 16.3) | B8 |
| `SITE:docs/tutorials/80-cross-platform.html:123` | "14 Windows-only renderers, plus the portable ones" | 5 | B14 |
| `SITE:docs/tutorials/80-cross-platform.html:158` | "FFmpeg is a hard requirement... Video is absent entirely on Windows, Web and Android... fails to link" | Optional; links everywhere | B5 |
| `SITE:docs/tutorials/80-cross-platform.html:247` | platform/audio paragraph ("CNA_PLATFORM can select SDL2, HEADLESS or POSIX-only TERMINAL ... CNA_AUDIO_PLATFORM can select SDL2 or NULL") | Add X11/WAYLAND/WIN32 and ALSA | P2, A1 |
| `SITE:docs/tutorials/81-emscripten.html:131` | "CNA ships a web CMake preset that configures exactly this: cmake --preset web" | `emcmake cmake --preset web`; the preset has no toolchain file | B9 |
| `SITE:docs/tutorials/81-emscripten.html:151` | "Five of CNA's 50 renderer identities are gated to Emscripten" | Five of 25 ([retired] gone) | B14 |
| `SITE:docs/tutorials/81-emscripten.html:108` | "3. There is no video... missing symbols... fails to link" | Links; throws at run time | B5 |
| `SITE:docs/tutorials/82-android.html:105` | "Video is absent entirely on Android... missing symbols" | Links; throws at run time | B5 |
| `SITE:docs/tutorials/82-android.html:110` | "NDK 29/30-era toolchains" | Demo pins NDK 30.0.14904198, minSdk 24, arm64-v8a | B10 |
| `SITE:docs/tutorials/100-shipping.html:120` | "FFmpeg is a hard requirement... Linux and macOS builds... Your shipped Linux binary therefore links FFmpeg runtime libraries" | Only when FFmpeg was found at configure (`AUTO`) or forced (`ON`) | B5 |
| `SITE:docs/tutorials/100-shipping.html:117` | "Windows, Web and Android... compiles and then fails to link" | Links; throws at run time | B5 |
| `SITE:docs/tutorials/100-shipping.html:314` | "21 workflow files... intended unfiltered general job and two Input rows..." | 20 files; EASYGL fixed | C1, C2 |
| `SITE:docs/tutorials/118-dynamic-audio.html:101` | "real dynamic playback in alpha.1 requires CNA_AUDIO_PLATFORM=SDL3" | SDL3 or ALSA | A2 |
| `SITE:docs/tutorials/119-3d-audio.html:101` | same | SDL3 or ALSA | A2 |
| `SITE:docs/tutorials/119-3d-audio.html:151` | "Exactly one listener is supported... for any other count it throws NotSupportedException"; page summary "The one-listener limit"; also "One listener." and Cue note "same single-listener restriction" | Multi-listener overloads accepted (count >= 1); dominant listener evaluated; zero/negative count and null array throw | A9, `SoundEffectInstance.hpp:363-392` |
| `SITE:docs/tutorials/120-xact.html:101` | "XACT playback... requires CNA_AUDIO_PLATFORM=SDL3" | SDL3 or ALSA | A2, A10 |
| `SITE:docs/tutorials/120-xact.html:287` | "Cue::Apply3D ... with the same single-listener restriction" | No such restriction | A9 |
| `SITE:docs/tutorials/126-multi-renderer-build.html:67` | "CMake rejects ... PortableGL with a real-GL family, GDI with Software, [retired] with anything else, and combinations that span mutually exclusive OS partitions" | [retired] retired; three rule families remain | B14 |
| `SITE:docs/tutorials/127-platform-audio-selection.html:58` | table rows: CNA_PLATFORM `SDL3, SDL2, HEADLESS, TERMINAL`; CNA_GRAPHICS_RENDERER "One of 50"; CNA_AUDIO_PLATFORM `SDL3, SDL2, NULL` | Platform adds X11 WAYLAND WIN32; renderer 25; audio adds ALSA | P2, A1 |
| `SITE:docs/tutorials/127-platform-audio-selection.html:63` | "The three audio choices... Alpha.1 defines SOUND_ENABLED only for SDL3" | Four choices; SDL3 and ALSA have the mixer | A2 |
| `SITE:docs/tutorials/127-platform-audio-selection.html:91` | "accepts CPU/no-output renderers: Software, [retired], PortableGL, Headless or Stub" | `SOFTWARE PORTABLEGL HEADLESS STUB` | P8 |
| `SITE:docs/tutorials/127-platform-audio-selection.html:94` | "SDL12, WIN32 and EMSCRIPTEN are reserved platform identifiers; OPENAL, WASAPI and ALSA are reserved audio identifiers" | WIN32 implemented (Windows only); ALSA implemented (Linux only); reserved: SDL12, EMSCRIPTEN, OPENAL, WASAPI | P3, A1 |
| `SITE:docs/tutorials/127-platform-audio-selection.html:77` | SDL2 recipe (both SDL2) presented as one option among free combinations | Also: platform SDL2 with default audio SDL3, and SDL3 with SDL2 audio, are configure errors | P9 |

### 7.1 Tutorials: rewrite versus small fix

| Tutorial | Verdict | Why (main items) |
|---|---|---|
| 127 Choose Platform, Renderer, and Audio Independently | **Rewrite** | Entire premise (three platform values, three audio values, reserved list, TERMINAL renderer list) changed; needs X11/WAYLAND/WIN32, ALSA, `CNA_ENABLE_SDL`, SDL2/SDL3 exclusions, SDL-free recipes |
| 80 Cross-Platform Build Guide | **Rewrite** | Status table (iOS "no toolchain", METAL "only renderer with CI", 14 Windows renderers), FFmpeg statements, platform/audio paragraph, sibling/branch guidance |
| 119 3D Positional Audio | **Rewrite the listener sections** (rest keeps) | "One-listener limit" is gone; multi-listener dominant-listener rule; build requirement SDL3 or ALSA; Cue restriction sentence |
| 02 Setting Up Your Dev Environment | **Substantial fix** (near-rewrite of prerequisites) | Compiler minimums, OS floors, FFmpeg optional, package lists (X11/GL/etc.), presets, clone branches (`next`), SDL not static |
| 20 Building and Running Your Game | Small/medium fix | "fourteen renderers", Emscripten "3.1+", video statement, Android NDK claim, web preset (already `emcmake` there) |
| 81 Emscripten | Small fix | `cmake --preset web` -> `emcmake cmake --preset web`; "five of 50"; video statement |
| 82 Android | Small fix | Video statement; NDK/minSdk facts from demo; otherwise still accurate (no CI, no preset) |
| 100 Shipping Your CNA Game | Small fix | FFmpeg "hard requirement" bundling advice becomes conditional; video link-failure statement; workflow count; renderer counts |
| 03 Your First CNA Window | Small fix | "static libraries" -> shared/static per OS; `libcna.so` note; drop FFmpeg troubleshooting row; add branch/sibling note |
| 01 Introduction | Small fix | Counts (25/21), readers (VideoReader always), platforms sentence |
| 14 Sound Effects | Small fix | Build requirement SDL3 or ALSA; delete "exactly one listener" paragraph |
| 15 Background Music | Small fix | Build requirement; FFmpeg-conditional duration probing |
| 118 Procedural Audio | Small fix | Build requirement SDL3 or ALSA |
| 120 XACT | Small fix | Build requirement; single-listener sentence in the 3D section |
| 126 Multi-renderer build | Small fix | Rule list ([retired] gone; OPENGL4 in real-GL set) |

## New pages/sections warranted

Only where TARGET code proves the content. "Page" = new file under `docs/`; "section" = new heading in an existing page.

| # | Proposed | Why / content it must carry | Key evidence |
|---|---|---|---|
| 1 | Page **Native X11 platform** (`docs/platform-x11.html`) | New SDL-free backend; dependency table (mandatory vs optional per capability), capability boundary incl. no HiDPI by design, exclusive fullscreen, XI2 touch/pen, XIM IME, XDND, ICCCM clipboard/primary, D-Bus portal dialogs, system-tray icons, evdev gamepads; CI evidence (two jobs, Xvfb) and its limits (no real desktop in CI) | P2, P7, P16; `docs/platform-x11.md` |
| 2 | Page **Native Wayland platform** (`docs/platform-wayland.html`) | Native client; packages; protocol/capability table; run-time-loaded EGL/Vulkan/D-Bus; **must state no CI**; local validation is a claim by the project | P15, `cmake/PlatformWayland.cmake`, `WaylandPlatform.cpp:487-545` |
| 3 | Page **Native Win32 platform** (`docs/platform-win32.html`) | user32/gdi32/WGL/COM backend, no SDL; what it lacks (gamepad, IME, drag-drop, tray, camera); SDL-free Windows means silent (NULL) audio; CI = mingw+Wine platform module, manual MSVC | P14, P16, A-notes |
| 4 | Page **SDL2 platform and audio** (`docs/platform-sdl2.html`) | Real SDL 2.30 backend, its narrow capability profile, exact renderer compatibility table, the three configure-time exclusions with SDL3 | P9, `Sdl2Platform.cpp:220-236` |
| 5 | Page **Terminal and Headless platforms** | POSIX-only terminal backend (Kitty keyboard probe, CPU frame presenter, one window), Headless (all capabilities false, always compiled), allowed renderers | P4, P8, `TerminalPlatform.cpp:178-190` |
| 6 | Page **Building without SDL** (`CNA_ENABLE_SDL=OFF`) | The three-way switch; which selections need SDL; working recipes (X11 + NULL/ALSA + HEADLESS/OpenGL/Vulkan/Software; WIN32 + NULL + DirectX); how CI proves it; what still needs SDL | P10, `platform-ci.yml:378-650` |
| 7 | Page or section **ALSA audio and CNA's own mixer** | New audio backend: run-time `libasound`, env vars, formats (Vorbis/MP3/FLAC/WAV family), no Opus/WMA/XMA, capture, PipeWire/PulseAudio via ALSA `default` | A1-A7 |
| 8 | Section in Audio page: **Backend feature matrix** | Table from section 3 (SDL3/SDL2/NULL/ALSA x playback, Dynamic, MediaPlayer, XACT, Microphone, 3D) | Section 3 |
| 9 | Page **Apple platforms** (macOS/iOS) | Floors 13.3/16.3, iOS allow-list (`SDL_RENDERER`), smoke app, bundle options, what CI does and does not prove | B8, `apple-ci.yml` |
| 10 | Section in Building: **Release boundary and branches** | Which branch/tag each sibling needs (`next` vs default), `main` = alpha.1, TARGET unreleased; `libcna/*` and `openeggbert/*` aliases | Headlines 1-2, B1, B2 |
| 11 | Section in Building: **Build performance and layout** | `CNA_SHARED_LIBRARY`/`libcna.so`, ccache, linker, IPO/unity/PCH, sanitizers, presets (17), `.sdl-prebuilt-*` persistence, `CNA_MAX_VENDORED_BUILD_JOBS`, vendored SDL builds at configure | B12, B15, section 4 |
| 12 | Section in Building: **Optional FFmpeg / video** | `CNA_ENABLE_VIDEO` semantics, per-OS availability, run-time failure mode | B5 |
| 13 | Section in Verification/Platforms: **CI inventory (20 workflows)** | Section 6 table condensed; automatic vs manual; what is not covered (Wayland, Android, C API build, GPU pixel matrix) | Section 6 |
| 14 | Tutorials (new) | "Build an SDL-free X11 game with ALSA audio" and "Choose an audio backend" (would replace part of 127) | P10, A1-A7 |

## Open questions

1. **Documented revision.** TARGET is the tip of `next` and still says `0.1.0-alpha.1`; `main`/`develop` = alpha.1. Should the site describe an unreleased revision, wait for a tag, or carry a "development (`next`)" banner? This decides whether `git clone -b next` and sharp-runtime `next` belong in the quickstart. (Headlines 1-2.)
2. **sharp-runtime dependency branch and stale CI pins.** I proved the requested components (`Resources`, `Xml.Serialization`) exist only on sharp-runtime `next`, and that eight workflows (nine jobs) pin older sharp-runtime commits or use `main` (C6). I did not configure to observe the failure text. Is there a sharp-runtime commit CNA `next` is meant to pin, and were those lanes red at TARGET? Only a recorded GitHub Actions history can answer; I had no access.
3. **Wayland evidence.** Only in-tree docs claim Weston/GNOME Mutter validation; no workflow, no recorded run. Publish as "implemented, tested locally, not in CI" or ask the owner for a recorded result?
4. **Compiler and OS minimums.** No CMake check exists. Owner decision needed: GCC 13 vs 14, Clang version, MSVC version, Windows floor (Win32 header level 0x0603 = 8.1), Emscripten minimum (only 6.0.3 exercised), NDK/API (demo: NDK 30 / API 24). I can state only what CI proves.
5. **C API buildability at TARGET.** The renderer set shrank, so the alpha.1 49-vs-50 defect may be gone, but a `static_assert` still exists (`CnaCApiCoreExt.cpp:241`) and no workflow builds the library. Not verified (no compile allowed). `docs/c-api/RELEASE_GATE.md` claims a consumer build/run test exists (`CApi_InstalledConsumer`) - untrusted.
6. **FFmpeg-off on Linux.** No Linux workflow runs `CNA_ENABLE_VIDEO=OFF`; the unavailable-backend fallback is exercised only by Windows/Emscripten/iOS-style exclusions. Is it safe to publish "optional" for Linux? (Code path is clear: B5; runtime evidence is indirect.)
7. **SDL2 beyond Linux.** SDL2 is fetched with `FetchContent` and CI covers only Linux; no CMake gate prevents `CNA_PLATFORM=SDL2` on Windows/macOS/Android/iOS/Emscripten. Unproven there.
8. **X11 on macOS.** `PlatformX11.cmake` excludes Windows/Emscripten/Android/iOS but not macOS, so `CNA_PLATFORM=X11` can be offered on a Mac with XQuartz dev files. Untested; do not document.
9. **Test/inventory numbers.** This sheet does not recount test files, GoogleTest macros or per-module counts (site currently quotes 568 / 8,263 / 31 audio / 29 media); another sheet should.
10. **Organisation names.** `libcna/*` and `openeggbert/*` resolve to identical repositories for cna, sharp-runtime, easy-gl, meta-gl; `free-direct`/`free-api` exist only under `openeggbert/`. CI and CMake messages use `openeggbert/`, the site uses `libcna/`. Pick one canonical spelling for commands.
11. **Win32 gamepad/IME roadmap.** `Win32Platform.cpp:105-110` says the remaining work is recorded in `plans/plan_win32.md` section 15 (not read). Should the site mention a roadmap?
12. **Presets on the site.** With 17 presets, decide which are user-facing (`tests`, `web`, `multi-renderer`, `macos`, `ios*`, `cnaext`, `unit*`) versus maintainer tooling (`dev*`, `release-*`, `devices-*`).
13. **Sanity of quickstart timing and disk.** "5 minutes", "~500 MB", "4 GB RAM" have no source; the repository itself records ~104 MB per statically linked test executable (`CMakeLists.txt:43-55`) and a 30 GB shared build machine.

## Method notes and limits

- Nothing was configured, compiled or run; every "would fail" is read from `message(FATAL_ERROR ...)` logic and guard conditions. Where a statement rests on `git ls-remote` or the sharp-runtime local clone (read-only `git ls-tree`/`git ls-remote`), it is marked in the fact rows.
- I accidentally created three temporary files outside the one permitted output file: an empty `audit/data/facts/.notpage` (a mistaken `cat >`), an empty `/rv/data/development/github.com/libcna/.scan_tmp_unused` (same mistake), and a generator script `audit/data/facts/.rows_tmp.py` used to compute HTML line numbers for section 7; all three were deleted before finishing. No other file in either repository was written. The CNA worktrees were not modified.
- CNA's own Markdown (`docs/platform-*.md`, `docs/audio-alsa.md`, `README.md`, `CHANGELOG.md`) was used only as pointers; the rows that cite it say "(untrusted)" and were cross-checked in code, except where explicitly marked M.
