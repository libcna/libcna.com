# R1 — Renderers, platforms and the canonical numbers, CNA B=b0e97bb1 → T=c1c316b9

INTERNAL AUDIT RECORD (not served). This file names retired renderer identities and retired platform backends;
the public site must not — not even as "removed" notices, in metadata, search data or diagrams
(`scripts/check_retired_renderers.py` and `scripts/check_retired_platforms.py` enforce that).

Pins: B=`b0e97bb1bb876f9b3edd6f4ff1ef3067908ae8ac` (2026-10-04, branch `next`),
T=`c1c316b9c7a846ce8002809c151fcd1af14942c9` (2026-10-09 17:22 +0200, tip of `apple/m4-stabilization` when read;
the remote branch has since moved to `63ef2e62`). `git rev-list --count b0e97bb1..c1c316b9` = **354**.
CNA was read through Git objects of the local clone (`git show`, `git ls-tree`, `git grep`, `git rev-list`) and the
tree extracted by `scripts/extract_cna_trees.sh` (stamp = T). Nothing in CNA or a sibling repository was modified,
built or run for this record.

## 1. Canonical numbers (recomputed at T; every method reproduces the B value exactly)

| Fact | B `b0e97bb1` | T `c1c316b9` | Method |
|---|---|---|---|
| Commits since `v0.1.0-alpha.1` | 3,333 | **3,687** | `git rev-list --count v0.1.0-alpha.1..T` |
| First-parent / merges | 945 / 65 | **1,299 / 65** | `--first-parent` / `--merges` |
| `git describe` | `…-3333-gb0e97bb1b` | **`v0.1.0-alpha.1-3687-gc1c316b9c`** | `git describe --tags --abbrev=9` |
| Changed paths since alpha.1 | 7,436 | **7,463** (A 3,212 · D 1,483 · M 2,704 · R 64); `--no-renames`: 7,527 (3,276 / 1,547 / 2,704) | `git diff --shortstat` / `--name-status` |
| Lines since alpha.1 | +1.48 M / −0.47 M | **+1,395,726 / −489,780** | `git diff --shortstat` |
| Public renderer identities | 18 | **14** | `CNA_RENDERER_PUBLIC_IDENTITIES`, `cmake/RendererIdentities.cmake:26-28` |
| Implementation families | 14 | **12** | `git ls-tree T modules/renderers/` (directories with `src/`, `common/` excluded) |
| Retired identities (derived) | 33 | **37** | `CNA_RENDERER_RETIRED_IDENTITIES`, `RendererIdentities.cmake:33-38`; `check_retired_renderers.py` derives the same 37 |
| 2D-only identities | 2 | **1** (`SDL_RENDERER`) | code-declared `ThreeD` |
| Compiled-effect identities | 13 in 9 families | **11 in 9 families** | FNA3D always + 8 `option(CNA_*_COMPILED_EFFECTS)` (EASYGL ×3 identities, VULKAN, WEBGPU, SOFTWARE, DIRECTX9, DIRECTX11, SDL_GPU, **METAL**); default configure: true on FNA3D only (13 of 14 false) |
| `CNA_GRAPHICS_RENDERER_MAXIMUM` | 43 | **43** (`FNA3D`; next new value 52) | `modules/c-api/include/CNA/C/graphics.h` |
| Platform implementations | 6 | **3** (`SDL3`, `HEADLESS`, `TERMINAL`; TERMINAL not on Windows) | `_cna_platforms_available`, `cmake/PlatformSelection.cmake:30-33` |
| Retired platforms | — | `WIN32`, `X11`, `WAYLAND` (refused by name, pointing at SDL3) | `_cna_platforms_retired`, `PlatformSelection.cmake:52` |
| Audio implementations | 3 | **3** (`SDL3`, `NULL`, `ALSA`) | `cmake/AudioPlatformSelection.cmake:17` |
| C++ test source files | 852 | **813** | `git ls-tree -r --name-only T`, `*.cpp` outside `third_party/` with a `test`/`tests` path segment |
| Files with a counted macro | 821 | **781** | `git grep -cE '^\s*(TEST\|TEST_F\|TEST_P\|TYPED_TEST\|TYPED_TEST_P)\s*\(' T -- '*.cpp' '*.mm' '*.cc'` |
| Static GoogleTest-family definitions | 12,021 | **11,380** (TEST 8,785 · TEST_F 2,476 · TEST_P 119) | same `git grep`, summed |
| Standalone `examples/**/*_test.cpp` pixel programs | 779 | **781** | `git ls-tree -r --name-only T \| grep -E '(^\|/)examples/.*_test\.cpp$'` (not part of the test counts) |
| CI workflow files / jobs | 18 / 26 | **18 / 24** | `.github/workflows/*.yml`, `jobs:` keys |
| Automatic files / jobs | 16 / 23 | **16 / 21** | files triggered by push + pull_request; jobs minus manual-only (`d3d-windows-ci` 1 job, `content-pipeline-windows-ci` 1 job on its own branch, `platform-ci`'s `sdl3-windows`, whose `if:` requires `workflow_dispatch`) |
| C ABI | 0.44.0 | **0.46.0** | `modules/c-api/include/CNA/C/abi.h:34-44` (see R3) |
| `GraphicsCapability` members / profile | 19 / 32 features, 22 limits | unchanged | `GraphicsCapability.hpp`, `RendererCapabilityProfile` |

## 2. Renderer identities at T

| C ABI | Identity | Family (`modules/renderers/`) | Platform gate | Declared maturity | Compiled-effect option |
|---:|---|---|---|---|---|
| 1 | SDL_RENDERER | sdl-renderer | needs SDL3 | Production (2D-only) | — |
| 3 | OPENGLES3 | easygl | non-Emscripten; Linux default | Production | CNA_EASYGL_COMPILED_EFFECTS |
| 4 | OPENGL33 | easygl | non-Emscripten | Production | same |
| 6 | WEBGL2 | easygl | Emscripten only (default there) | Supported | same |
| 8 | VULKAN | vulkan | Vulkan SDK/runtime | Production | CNA_VULKAN_COMPILED_EFFECTS |
| 9 | WEBGPU | webgpu | wgpu-native; emdawnwebgpu under Emscripten | Experimental | CNA_WEBGPU_COMPILED_EFFECTS |
| 11 | HEADLESS | headless | none | Supported | — |
| 12 | SOFTWARE | software | none | Experimental | CNA_SOFTWARE_COMPILED_EFFECTS |
| 13 | STUB | stub | none | Supported | — |
| 14 | DIRECTX11 | directx11 | Windows only | Production | CNA_DIRECTX11_COMPILED_EFFECTS |
| 22 | DIRECTX9 | directx9 | Windows only | Production | CNA_DIRECTX9_COMPILED_EFFECTS |
| 31 | SDL_GPU | sdl-gpu | needs SDL3 | Supported | CNA_SDL_GPU_COMPILED_EFFECTS |
| 42 | METAL | metal | macOS and iOS | Supported (not primary-production, AM4-159) | CNA_METAL_COMPILED_EFFECTS (default OFF) |
| 43 | FNA3D | fna3d | FNA3D dependency, needs SDL3 | Experimental | always on |

* Defaults (`cmake/RendererIdentityDefault.cmake`, unchanged): `WEBGL2` under Emscripten, `OPENGLES3` on Linux,
  `SDL_RENDERER` everywhere else.
* iOS allow-list (`cmake/ApplePlatform.cmake:246-249`): `SDL_RENDERER` and **`METAL`** (B: `SDL_RENDERER` only);
  anything else needs `CNA_APPLE_ALLOW_UNVALIDATED_RENDERER=ON` and is "experimentation only".
* Browser renderers at T: `WEBGL2` (default) and `WEBGPU`. Windows renderers: `DIRECTX9`, `DIRECTX11` (plus the
  cross-platform `SDL_GPU`, `VULKAN`, `SOFTWARE`, `FNA3D`).
* Workflows that name each identity: SDL_RENDERER (input, apple), OPENGLES3 (input, gltf-stride, platform,
  devices, general), WEBGL2 and WEBGPU (emscripten-multi-renderer only: a browser bundle built and inspected, not
  run), VULKAN (input, gltf-stride, platform), HEADLESS, SOFTWARE, STUB (multi-renderer, gltf, platform,
  content-pipeline), DIRECTX11 (d3d-windows, manual), METAL (metal-macos, apple). **No workflow names SDL_GPU,
  OPENGL33, DIRECTX9 or FNA3D.**
* `SupportsCapability()` overrides: every renderer family except DIRECTX9 (`git grep -l SupportsCapability T --
  modules/renderers`).
* Parity fixtures: 32, registered for EasyGL, WEBGPU, SDL_GPU and DIRECTX11 (four families).

## 3. What changed B → T (internal history; never public)

| Commit | Date | Task | Change |
|---|---|---|---|
| `39e84add7` | 2026-10-06 | PLAT-142 | Retired the direct Win32, X11 and Wayland platform backends (`modules/platform/src/{Win32,X11,Wayland}` and the helpers only they used: `Xkb/`, `Freedesktop/`, `Linux/`, `Posix/`, `Common/SurfaceFrameFitting`; 52 test files; `cmake/PlatformX11.cmake`, `cmake/PlatformWayland.cmake`; four CI jobs). `PlatformFactory` knows SDL3, Headless and Terminal only. **Kept:** `NativeWindowSystem::Win32/X11/Wayland`, `NativeWindowHandle`, `TryGetWin32/X11/Wayland`, `CNA_NATIVE_WINDOW_SYSTEM_*`, `Sdl3Window::GetNativeHandle()` (filled from SDL's window properties), `GameWindow::GetNativeWindowHandleEXT()`; `CNA_ENABLE_SDL=OFF` remains the windowless configuration. New `CnaPlatformSdl3X11Tests` / `CnaPlatformSdl3WaylandTests` run SDL3 on a private Xvfb / headless Weston (`plans/plan_platform.md` §11c). |
| `1cac65958` | 2026-10-07 | RRC-018 | Retired `DIRECTX12`(15), `CANVAS`(17), `OPENGLES2`(2), `WEBGL1`(5); values reserved; C ABI 0.45.0 (see R3). |
| `b0390cbbc` | 2026-10-07 | AM4-037 | `METAL` on iOS (UIKit view path); C ABI 0.46.0 adds `CNA_NATIVE_WINDOW_SYSTEM_UIKIT`=9. |
| AM4-* | 2026-10-04…09 | Apple campaign | Metal MSAA/MRT/queries/instancing/formats/PBR/MSL custom effects/compiled effects; macOS and iOS evidence (see R2). |

PLAT-142 evidence recorded by CNA (DOC/plan, not re-run here): CnaPlatformSdl3X11Tests 38 passed, CnaPlatformSdl3WaylandTests
30 passed; seven renderers' demos ran on both SDL drivers; a mingw cross-build under Wine passed 30 tests.
`platform-ci.yml` at T has four jobs: `platform-contract` (SDL3 on x11 under Xvfb and on wayland under headless
Weston), `sdl-free` (Headless + ALSA), `sdl-enable-matrix`, `sdl3-windows` (native MSVC, manual dispatch).

## 4. Site impact and the public wording rule

* Pages deleted: `deep-dives/renderers/canvas-renderer.html`,
  `development/internals/platforms/{x11,wayland,win32}.html` (inbound links repointed to
  `deep-dives/platforms/web-build-and-main-loop.html` and `development/internals/platforms/sdl3.html`).
* `docs/native-platforms.html` keeps its URL and became "Windows, X11 and Wayland" (through SDL3's video drivers,
  native handles, the windowless SDL-free configuration). Tutorials 135/136 became "Running on X11/Wayland through
  SDL3"; the tutorial hub section is "Window Systems and Builds".
* Public wording: describe the current product only. Windows, X11 and Wayland are environments reached through
  SDL's `windows`, `x11` and `wayland` video drivers; native handles remain available; Xvfb and Weston are test
  servers. Never "native X11 platform", "Win32 backend", `CNA_PLATFORM=X11`, never a retired renderer name or
  prose alias (Canvas renderer, Direct3D 12 renderer, WebGL 1, OpenGL ES 2) except SDL_GPU's Direct3D 12 *driver*,
  meta-gl's GLES 2.0 entry points and WebGL 1/2 context flags, which are other projects' facts.
* Guards: `scripts/check_retired_renderers.py` (derived set + `CANVAS` as a weak word + prose aliases) and
  `scripts/check_retired_platforms.py` (derived from `_cna_platforms_retired`; distinguishes `CNA_PLATFORM=X11`
  from SDL's `x11` driver), both wired into `scripts/validate_all.sh`.
