# Fact sheet 06 - C API, bindings boundary, Diagnostics, Inspector, other new modules/tools, project statistics

Phase 1 research (read-only). Author: research agent 06. Date: 2026-09-24.

- TARGET: CNA commit `009d40f5dd085c4e674d3479675fac84b12b3e0a` (2026-09-24 17:08:57 +0200, `merge(OpenGL4ModernGraphics)`), read from the immutable worktree `/rv/tmp/libcna-v2/cna-target`. All `path:line` citations below are TARGET-relative unless prefixed `BASE:`.
- BASE: `1bb2145d99ed572dd4eb15009c34e2e5f410fcf0` (`v0.1.0-alpha.1`, 2026-08-20), worktree `/rv/tmp/libcna-v2/cna-base`.
- Range: `git rev-list --count BASE..TARGET` = **2,877 commits**; `git describe --tags TARGET` = `v0.1.0-alpha.1-2877-g009d40f5d`.
- Evidence tags: **[SRC]** implementation / build config / header read directly; **[GEN]** checked-in generated report or baseline (`tools/c-api/*.json`, `docs/c-api/COVERAGE.md`, `RELEASE_GATE.md`); **[CALC]** computed by me from TARGET/BASE files (method stated); **[DOC]** CNA Markdown (untrusted, used only for orientation or explicitly marked as CNA's own claim).
- Nothing was built or run. No CNA worktree was modified. Only file written: this one. The counting scripts I used lived in the session scratchpad only; their logic is reproduced in section "Project statistics".

---

## Verified facts

Headline table (TARGET vs the alpha.1 site baseline).

| Topic | Alpha.1 (BASE / site) | TARGET | Tag / evidence |
|---|---|---|---|
| C ABI version | 0.7.0 | **0.29.0** (encoded `0x00001D00` = 7424) | [SRC] `modules/c-api/include/CNA/C/abi.h:34-44`; [GEN] `tools/c-api/abi_baseline.json` `abi_version` |
| Public C headers | 59 | **61** (adds `cnb.h`, `engine_layer.h`) | [CALC] `ls modules/c-api/include/CNA/C` |
| Declared `CNA_C_API` routes | 2,861 | **4,055** (declared name set == exported-symbol baseline set, empty difference both ways) | [CALC] regex of `tools/c-api/check_declared_exports.py:36` over headers vs `abi_baseline.json` `exports` |
| Recorded ABI baseline | not stated | 221 struct layouts, 350 scalar types, 1,558 integer constants, 14 string constants, 141 colour constants, 4,055 exports | [GEN] `tools/c-api/abi_baseline.json` |
| Semantic inventory | 6,712 rows: 6,317 impl / 15 partial / 380 N/A; 421 headers | **9,355 symbols: 8,363 impl / 15 partial / 468 planned / 509 N/A**; 556 headers in scope, 425 headers excluded | [GEN] `docs/c-api/COVERAGE.md:15` |
| C renderer map vs canonical | 49 rows vs 50 -> `static_assert` fails, library cannot compile | **25 rows vs 25 canonical; `MAXIMUM` = 46 = highest published value: both asserts hold by inspection** | [SRC] `modules/c-api/src/CnaCApiCoreExt.cpp:195-244`, `modules/core/include/CNA/GraphicsRendererType.hpp:16-`, `modules/c-api/include/CNA/C/graphics.h:16-85` |
| `CNA_BUILD_C_API=ON` with `CNA_ENABLE_NET=OFF` | fails late on a missing GamerServices include | **configure-time `FATAL_ERROR` naming the option** | [SRC] `CMakeLists.txt:185-190` |
| Release gate | site: checked-in report "Ready" vs workflow "NOT READY" dispute | **both agree: "Not ready. 1 criteria are unmet" (468 unmapped public symbols)** | [GEN] `docs/c-api/RELEASE_GATE.md:11-16`; `.github/workflows/c-api-release-gate.yml` header |
| Does any CI job build the C API? | (site: "five declared gates") | **No.** The five `c-api-*.yml` workflows are build-free (headers/JSON/Doxygen only). `CNA_BUILD_C_API` appears in no workflow and is `OFF` in all three `CMakePresets.json` presets. Build + `CApi_*` CTest run only where a developer configures `-DCNA_BUILD_C_API=ON`. | [SRC] `.github/workflows/c-api-*.yml`; `CMakePresets.json:29,56,93` |
| New top-level modules | - | `content-pipeline`, `design`, `diagnostics`, `inspector`, `phone`, `video-ffmpeg` (6; `modules/` directories 17 -> 23 incl. `renderers`) | [CALC] `ls modules` diff |
| Diagnostics / Inspector build options | absent | `CNA_DIAGNOSTICS=OFF\|STATS\|FULL` (default OFF), `CNA_BUILD_INSPECTOR` (default OFF) | [SRC] `CMakeLists.txt:149-171` |
| C++ test files (site method) | 568 | **903** | [CALC] method in S1 |
| GoogleTest-family definitions (site method) | 8,263 | **12,610** | [CALC] method in S1 |
| CI workflow files | 21 | **20** (removed `[retired]-ci.yml`, `[retired]-cross-platform-ci.yml`; added `content-pipeline-windows-ci.yml`) | [CALC] `ls .github/workflows` diff |
| Invalid `EASYGL` workflow values | present in `general-tests-ci.yml` and two `input-ci.yml` rows | **gone** (`OPENGLES3`; input rows `OPENGLES3`, `OPENGLES3`+ASan/UBSan, `SDL_RENDERER`, `VULKAN`) | [SRC] `.github/workflows/general-tests-ci.yml:139`, `input-ci.yml:35-56` |
| Product version string | `0.1.0-alpha.1` | **still `0.1.0-alpha.1`**; no newer tag (tags: `v0.1.0-alpha.1`, `audit-2026-07-complete`) | [SRC] `CMakeLists.txt:3,12-14`; `Doxyfile:51` |
| License | MS-PL | **unchanged** (`LICENSE`, `NOTICE.md` byte-identical); `THIRD_PARTY_NOTICES.md` gains a DirectXMesh (MIT) adaptation and loses retired-renderer notices | [CALC] `cmp` / `diff` |
| Public renderer identities | 50 in 46 families | **25 in 21 families** (25 retired; owned by another agent, but it is why the C blocker vanished) | [SRC] `GraphicsRendererType.hpp`; `docs/c-api/ABI_VERSIONING.md:31-54` |
| `Microsoft.Xna.Framework.Design` | "the only XNA 4.0 namespace CNA does not cover" | **implemented**, opt-in module `CNA::Design`, 13 converter classes | [SRC] `modules/design/include/Microsoft/Xna/Framework/Design/*.hpp`, `modules/CMakeLists.txt:338` |
| XNB authoring | "CNA does not author XNB" | **`cna-content build --format xnb` writes XNB (incl. LZX)** | [SRC] `tools/content/content.cpp:283-333` |
| "28 demo programs under `examples/`" | 28 | The same 28 `cna_demo_*` targets still exist, but **none lives under top-level `examples/`** (it holds one file + `golden/`, at BASE too); they are in `modules/*/examples/`. New: `cna_inspector_demo`. | [CALC] see O3 |

---

## C API

### C1. Identity, versioning and change policy

- ABI is **0.29.0**: `CNA_ABI_VERSION_MAJOR 0`, `MINOR 29`, `PATCH 0` (`modules/c-api/include/CNA/C/abi.h:34,37,40`); `CNA_ABI_VERSION_ENCODE` packs `major<<16 | minor<<8 | patch` (`abi.h:28-31`); runtime query `cna_get_abi_version()` (`abi.h:114`, implemented `modules/c-api/src/CnaCApi.cpp:19`). Baseline records `encoded: 7424` and `runtime: 7424` (`tools/c-api/abi_baseline.json`, `abi_version`).
- The ABI version is independent of the CNA product version and of Sharp Runtime's (`docs/c-api/ABI_VERSIONING.md` "API evolution" section [DOC]; verified by construction: `CMakeLists.txt:12` says `alpha.1`, `abi.h:37` says `29`).
- ELF symbol-version node is `CNA_C_API_0.1` and is deliberately never bumped with minors; only `cna_*` is global, everything else local (`modules/c-api/cmake/CnaCApiExports.map:1-17`), applied via `--version-script` and `--exclude-libs,ALL` when `UNIX AND NOT APPLE AND NOT EMSCRIPTEN` (`modules/c-api/CMakeLists.txt:103-108`).
- Change policy [DOC, corroborated by the gates below]: while `0.x`, an incompatible change requires a minor increment, release notes and a regenerated baseline; `1.x` and later permit only additive change within a major. Package compatibility is `SameMajorVersion` (`modules/c-api/CMakeLists.txt:475-479`), so `find_package(CNA 0.1 CONFIG)` accepts 0.1 and everything additive after it and rejects 1.x (`docs/c-api/ABI_VERSIONING.md:296-299`). The package version is read out of `abi.h` at configure time (`modules/c-api/CMakeLists.txt:452-466`).
- Version history at TARGET (`docs/c-api/ABI_VERSIONING.md` [DOC]; spot-checked against `abi_baseline.json` and headers):

| ABI | What changed (CNA's own summary) |
|---|---|
| 0.1.0 | initial |
| 0.2.0 | additive routes (CBIND-054..058) |
| 0.3.0 | **not additive**: all 94 `CNA_Bool`-taking routes refuse a byte outside {0,1} (CBIND-067) |
| 0.4.0 | `cna_content_manager_register_cnj_loader_ext` |
| 0.5.0 | portable native-window handle routes |
| 0.6.0 | empty shader-source refusal standardized |
| **0.7.0** | six PBR / morph-target routes - **the alpha.1 value** |
| 0.8.0 | [retired] renderer identity + 5 engine-layer capability identities (moved both `MAXIMUM` sentinels) |
| 0.9.0 | owned-`GraphicsDevice` create/destroy, render-target ContentLost subscription, `cna_video_player_get_frame_ext`; **seven documented contracts changed** (e.g. `Apply3D` on an unpositioned playing instance now `CNA_RESULT_INVALID_STATE`) |
| 0.10-0.17 | `.cnb` container, document, texture / model / sprite-font / sound / song / video / curve / clip schemas, loader registry + `.cnj`/source compile front ends, reflective content readers (eight additive generations) |
| 0.18.0 | `Dictionary<string,object>` object-dictionary handle + reference-shaped reflective reader |
| 0.19.0 | `Load<Model>` and the `Tag` a content processor wrote |
| 0.20.0 | removed 11 renderer identities (incompatible) |
| 0.21.0 | `cna_environment_get_device_type`, object-dictionary type-name pair |
| 0.22.0 | restored 10 identities, `MAXIMUM` back to 50 |
| 0.23.0 | `cna_decal_pass_is_supported` |
| 0.24.0 | `CNA_RENDERER_FEATURE_TEXTURE_3D_SAMPLING` (30) |
| 0.25.0 | `CNA_SHADER_DIALECT_SPIRV` (7) |
| 0.26.0 | `CNA_RENDERER_FEATURE_BASE_INSTANCE_DRAWING` (31) |
| 0.27.0 | `CNA_GRAPHICS_RENDERER_[retired]` = 51 (later retired) |
| 0.28.0 | **retired 25 renderer identities**; `MAXIMUM` 51 -> 46; retired values `7,10,19,20,23-30,32,34-39,41,45,47-51` permanently reserved; next new identity takes **52** |
| **0.29.0** | removed `cna_sprite_batch_draw_mesh_ext` + `CNA_SpriteMeshEXT`; exports 4,056 -> 4,055; struct layouts 222 -> 221 |

  CHANGELOG cross-check: `CHANGELOG.md` `[Unreleased]` records 0.26.0, 0.27.0 (later retired), 0.28.0 and 0.29.0 in prose (`CHANGELOG.md:10-69`) but has **no entries** for Diagnostics, Inspector, Design, Content Pipeline, Phone or the 0.8-0.25 C ABI growth.
- Recorded-baseline enforcement [SRC]: `tools/c-api/generate_abi_baseline.py` compares header-measured struct sizes/offsets/constants (and, with `--library`, the real `.so`'s exports and runtime ABI version) with `tools/c-api/abi_baseline.json`; registered as `CApiAbiHeaderBaseline` (ordinary build, no C API needed) and `CApiAbiBaseline` (only `if(TARGET cna_c_api AND UNIX AND NOT APPLE)`) in `cmake/Tests/ModuleProbes.cmake:525-546`. CI: `.github/workflows/c-api-abi-baseline.yml` (header half plus a self-test that swaps two `CNA_Point` fields and requires rejection).

### C2. Public headers and routes

- 61 headers in `modules/c-api/include/CNA/C/` [CALC]. Umbrella `CNA/C/cna.h` includes 59 of the other 60 directly (`named_colors.h` is reached indirectly) (`cna.h:8-70`). Headers carry `extern "C"` guards (e.g. `abi.h:8-10`).
- Route count per header, top: `engine_layer.h` 858, `effects.h` 290, `cnb.h` 272, `gamer_services.h` 250, `models.h` 216, `media_library.h` 148, `sensors.h` 144, `vectors.h` 137 [CALC, lines starting `CNA_C_API`]. Total 4,055.
- Route counting method (matches BASE 2,861): number of lines starting with `CNA_C_API` in `modules/c-api/include/CNA/C/*.h`; BASE gives 2,861, TARGET 4,055. The stricter regex in `tools/c-api/check_declared_exports.py:36` also yields 4,055 unique names at TARGET (2,861 at BASE).
- Library outputs: shared `libcna_c_api.so` (`add_library(cna_c_api SHARED ...)` `modules/c-api/CMakeLists.txt:23`, `OUTPUT_NAME cna_c_api` `:88`; 59 source files listed `:24-82` (73 files in `src/` incl. private headers)); under Emscripten it is `STATIC` (`:17-21`).
- Coverage contract [GEN/SRC]: `tools/c-api/generate_coverage_inventory.py` derives the inventory from `modules/*/include/{Microsoft,CNA}/**/*.hpp` (Doxygen XML) and maps each symbol through `tools/c-api/coverage_mappings.json`; `MODULE_SCOPE` is total over modules. Out of runtime C API scope by owner decision: `content-pipeline` (107 headers), `phone` (9), `platform` (27), `renderers/**` (138) and Internal/Detail path segments (`docs/c-api/COVERAGE.md:17-38`). Summary line `COVERAGE.md:15`; per-module table `COVERAGE.md:59-74`.
- `tools/c-api/` (20 files): `generate_abi_baseline.py`, `generate_compatibility_matrix.py`, `generate_coverage_inventory.py`, `generate_limitations.py`, `check_release_gate.py`, `check_declared_exports.py`, `check_doc_export_counts.py`, `check_route_test_coverage.py` (budget file `route_test_coverage_budget.json`: `uncovered_route_budget: 0`, so every exported route is named by at least one test/example source), `generate_bool_contract_test.py`, `generate_static_archive.py`, `generate_wasm_exports.py`, `generate_artifact_manifest.py`, `audit_coverage_backlog.py`, `test_coverage_scope.py`, plus the JSON data files.

### C3. Language / toolchain requirements

- CNA itself: C++23 (`CMakeLists.txt:21-22`); with `CNA_BUILD_C_API=ON` the root enables C, `CMAKE_C_STANDARD 17`, required (`CMakeLists.txt:79-82`), `CMAKE_C_EXTENSIONS ON` directory-wide for vendored POSIX C but **every `modules/c-api` target sets `C_EXTENSIONS OFF`** (`CMakeLists.txt:83-88` comment) and PIC is forced (`:89`). c-api targets compile with `-Wall -Wextra -Wpedantic -Werror` (`/W4 /WX` on MSVC) (`modules/c-api/CMakeLists.txt:5-11`).
- Consumer floor: **C99** (not C17). Public headers are compiled on their own and via the umbrella in every declared mode: `cc` c99/c11/c17 (required), `c++` c++11/14/17 (required), optional gcc c99-c23, g++ c++17/20/23, clang c99-c23, clang++ c++17/20/23, `x86_64-w64-mingw32-gcc` c99-c17 headers-only (`docs/c-api/COMPATIBILITY.md:25-31` [GEN], from `tools/c-api/compatibility_matrix.json`; gates `CApiCompatibilityMatrix` / `CApiHeaderCompatibility`, `.github/workflows/c-api-compat-matrix.yml`, build-free). The shipped example is compiled at exactly C99 with `-Wall -Wextra -Wpedantic -Werror` (`modules/c-api/examples/c/CMakeLists.txt:28-38`). Note `docs/c-api/README.md` still says "public C17 headers" - stale relative to the matrix.
- Run configurations recorded in the matrix: `headless`, `sdlrenderer`, `software`, `asan` (`COMPATIBILITY.md:41-44`). Not covered: running any Windows binary, macOS/iOS/Android/web targets, C89 (`COMPATIBILITY.md:51-54`).

### C4. CMake option, targets, install, export names

- Option: `CNA_BUILD_C_API` (default `OFF`) `CMakeLists.txt:78`. Prerequisite: `CNA_ENABLE_NET=ON` (default ON), else `FATAL_ERROR` (`CMakeLists.txt:185-190`) - the C API links `CNA_GamerServices` unconditionally.
- Targets: `cna_c_api` (alias `CNA::CApi`, `EXPORT_NAME CApi`) `modules/c-api/CMakeLists.txt:84,86-87`; optional static archive `CNA::CApiStatic` produced by `tools/c-api/generate_static_archive.py` (whole closure partially linked into one relocatable object, non-`cna_*` symbols localized, build fails if any survive except `STB_GNU_UNIQUE`); option `CNA_C_API_BUILD_STATIC` default ON, `UNIX AND NOT APPLE` + Python3 only (`modules/c-api/CMakeLists.txt:343-370`); its imported target defines `CNA_C_API_STATIC` (`tools/c-api/generate_static_archive.py:194-199`). Windows export macro: `__declspec(dllexport)` when `CNA_C_API_BUILD`, else `dllimport`; `CNA_C_API_STATIC` empties it (`abi.h:13-25`).
- Install component `CNACApi`: library (`install(TARGETS cna_c_api EXPORT CNACTargets ...)` `:373-378`), `include/` tree (`:381-384`), CNA-built SDL3 libs (`libSDL3*.so*`, `SDL3*.dll`) into the same directory (`:398-419`), `INSTALL_RPATH "$ORIGIN"` (`:96`), `CNACTargets.cmake` with `NAMESPACE CNA::` under `lib/cmake/CNA` (`:427-433`), `CNAConfig.cmake` + `CNAConfigVersion.cmake` (`:468-484`, template `modules/c-api/cmake/CNAConfig.cmake.in`). FFmpeg is never shipped; it is a system dependency only when `CNA_ENABLE_VIDEO` selected it ([DOC] `docs/c-api/CONSUMING.md:121-132`). `cmake --install <build> --component CNACApi --prefix <p>` installs only the C ABI (`CONSUMING.md:29-35` [DOC]; component mechanism [SRC] above).
- The C++ framework still has **no** `install()` rules (grep of root/module CMake outside `modules/c-api` finds none) - consistent with the site.
- WebAssembly artifact (new since BASE): under Emscripten, target `cna_c_api_wasm` (`add_executable ... wasm/module_entry.c`) emits `cna_c_api.mjs` + `.wasm` (`MODULARIZE=1`, `EXPORT_ES6=1`, `EXPORT_NAME=createCnaCApi`, `ALLOW_MEMORY_GROWTH=1`, `ASYNCIFY=0`), export list generated from the headers by `tools/c-api/generate_wasm_exports.py` (`modules/c-api/CMakeLists.txt:110-160`); tests `CApi_WasmLinkContract`, `CApi_WasmModuleSmoke`, `CApi_WasmBrowserProbe`.

### C5. How it is built and tested; CI gate

- Tests: 85 pure-C programs in `modules/c-api/tests/pure_c/*.c` (+1 header), 5 C++ tests (`tests/cpp/`: `AbiHeaderCpp`, `BoundaryDetailTest`, `CubeLutOracleTest`, `HandleRegistryTest`, `Utf8OracleTest`), 2 libFuzzer sources compiled as an object library only (`tests/fuzz/StringViewFuzz.cpp`, `CubeLutFuzz.cpp`; `modules/c-api/CMakeLists.txt:2139-`). They are **not GoogleTest**: `modules/c-api/tests` contributes 0 GoogleTest definitions and is filtered out of `CnaTests` (`cmake/UnitTests.cmake:55-60`).
- CTest registrations: 98 `add_test(NAME ...)` in `modules/c-api/CMakeLists.txt` (some conditional, some in loops) plus 12 header/JSON gate tests in `cmake/Tests/ModuleProbes.cmake` (`CApiCoverageMatrix`, `CApiCoverageScopeModel`, `CApiCompatibilityMatrix`, `CApiHeaderCompatibility`, `CApiLimitations`, `CApiDocExportCounts`, `CApiRouteTestCoverage`, `CApiBoolContractCurrent`, `CApiReleaseGate`, `CApiAbiHeaderBaseline`, `CApiAbiBaseline`, `CApiDeclaredExports`). The header-only ones are deliberately **not** inside `if(CNA_BUILD_C_API)` so the ordinary build runs them (`ModuleProbes.cmake:397-403`). CNA's own plan records `ctest -R '^CApi'` = 111 tests, 108 pass, 3 fail (the three generator gates) in a Debug HEADLESS tree on 2026-09-18 [DOC `plans/plan_capi_smoke_stability.md:285-295`]; I could not reproduce it.
- `CApi_InstalledConsumer` (Linux/ELF only, `UNIX AND NOT APPLE`, timeout 900 s, `RUN_SERIAL`): installs `CNACApi` to a staging prefix, configures `modules/c-api/examples/c` as a standalone project against `CMAKE_PREFIX_PATH`, builds `hello_cna` shared and static, runs both with no `LD_LIBRARY_PATH` / `-rpath-link` (`modules/c-api/CMakeLists.txt:2105-2132`; driver `modules/c-api/cmake/RunInstalledConsumer.cmake`).
- CI: five workflows, all `ubuntu-24.04`, all build-free: `c-api-abi-baseline.yml`, `c-api-compat-matrix.yml`, `c-api-coverage-gate.yml`, `c-api-limitations.yml`, `c-api-release-gate.yml`; triggers push/PR on `next, develop, main` plus `workflow_dispatch`, path-filtered. The coverage/limitations/release jobs clone the `sharp-runtime` sibling (`scripts/ci/clone_siblings.sh`) and install Doxygen only for the header inventory. None compiles `cna_c_api`.
- Release gate at TARGET [GEN] (`docs/c-api/RELEASE_GATE.md`): "Release: CNA C ABI 0.29.0, experimental"; **"Not ready. 1 criteria are unmet"** = "No public C++ symbol is unaccounted for - 468 public symbols are still unmapped". The nine other criteria are marked met, incl. "A real C application, built the way a consumer builds one - hello_cna is built from an installed prefix and run by CApi_InstalledConsumer", "package installable and findable", "221 struct layouts and 4055 exported symbols recorded", "23 declared cells across 7 toolchains", "13 documents present", "A static configuration that keeps the same ABI promise". Generated by `tools/c-api/check_release_gate.py` from `release_gate.json`. The gate explicitly says ABI 1.0 is a separate decision (`RELEASE_GATE.md:7`).
- Coverage backlog in CNA's own words [DOC `docs/c-api/COVERAGE_AUDIT.md` header, marked superseded]: the earlier "~3,000 planned" figure was mostly mis-modelled evidence; genuine missing runtime bindings measured 259 logical APIs; the coverage scanner was repaired (CTC-2..CTC-9) and the 468 now-planned rows are the live backlog (`CBIND-127`).

### C6. Does the final library now compile and link?

Confidence statement: **High that the two documented alpha.1 blockers are fixed in source; medium-high (about 85-90 percent) that the shared library compiles and links at exactly `009d40f5d`. I did not, and by rule could not, build it, and no CI job builds it.**

Evidence for "compiles":
1. Renderer map/asserts [SRC]: `CnaCApiCoreExt.cpp:195-220` holds 25 `{C identity, native}` pairs; `CanonicalRendererCount()` (`:181-189`) counts `CNA::getGraphicsRendererName` results until `"UNKNOWN"`; the C++ enum `GraphicsRendererType` has exactly 25 enumerators (`GraphicsRendererType.hpp:16-` through `PortableGL`) and `getGraphicsRendererName` has 25 `case` arms (`:182-`), so `static_assert(RendererIdentities.size() == CanonicalRendererCount())` (`:241`) is 25 == 25. `HighestPublishedIdentity()` (`:226-236`) is 46 = `CNA_GRAPHICS_RENDERER_PORTABLEGL` (`graphics.h:66`), equal to `CNA_GRAPHICS_RENDERER_MAXIMUM` (`graphics.h:85`), so `static_assert(CNA_GRAPHICS_RENDERER_MAXIMUM == HighestPublishedIdentity())` (`:243`) holds. [retired] (the missing row at BASE) no longer exists as an identity. Nothing under `modules/c-api` names a retired renderer or `DrawMeshEXT` except the reserved-values comment in `graphics.h:77-81` [CALC grep].
2. The networking prerequisite is refused at configure time (`CMakeLists.txt:185-190`), not discovered per translation unit.
3. Include closure [CALC]: all 1,855 `#include` directives in `modules/c-api/src/` and `modules/c-api/tests/` resolve to files present in the TARGET tree, to standard headers, or to `System/...` (sibling sharp-runtime); none point at a removed header.
4. Declared == exported [CALC]: the 4,055 header-declared route names equal the 4,055 names in `abi_baseline.json` `exports` (empty set difference both ways), and that baseline carries a `runtime` ABI field that only a real library can supply. The commit that recorded it says it was measured from a real library (`4a1dbb4ea`, 2026-09-18: "`generate_abi_baseline.py --check --library`, the normal supported path, ran for the first time since the C API build broke ... 221 structs ... 4055 exports ... the entire file diff is `"runtime": 7424`") [git history, orientation only].
5. Post-fix history: only four commits touched `modules/c-api` after that measurement (`75097d5ed`, `40c48cdbb` on 2026-09-18, smoke repairs; `9a42a7e82`, `6a3ba555e` on 2026-09-20, `GraphicsState` and `AvatarDescription` changes; the latter states "The exported symbol set is unchanged").
6. Build failures CNA repaired on the same branch [DOC `CHANGELOG.md:100-108`, `plans/plan_terminal_capi_repair.md`]: effect collections return `T*` not `T&` (`CnaCApiEffects.cpp`), NET=OFF include failure (now refused), ABI walls asserted `0.27.0` vs `0.29.0`.

Not verified (would need a build): that nothing in the 2026-09-19..24 graphics/renderer merges broke a C-API translation unit; that `libcna_c_api.so` links with `CNA_SHARED_LIBRARY` at its default on a given toolchain; Windows/macOS shared-library builds (package machinery, RPATH, version script and consumer test are ELF/Linux only).

Corrected alpha.1 statement: "alpha.1 has no consumable native C library" was true of the tag. At TARGET the package is designed, gated and (per CNA's own consumer test) consumable **from a source build on Linux**, but it is still not a release, not built by CI, and the gate says "Not ready".

### C7. Conventions (handles, errors, ownership, strings, threading)

- Result codes: `CNA_Result` = `uint32_t`; 0 success, 1 invalid argument, 2 invalid handle, 3 invalid state, 4 out of memory, 5 I/O, 6 not supported, 7 platform, 8 thread, 9 callback, 10 overflow, 11 encoding, 12 internal, 13 shutting down, 14 buffer too small (`abi.h:47-92` [SRC]). No C++ exception crosses the ABI ([DOC] `docs/c-api/ERRORS.md`). Per-thread last error: `cna_error_get_last_info`, `cna_error_get_last_message_size`, `cna_error_copy_last_message` (`modules/c-api/include/CNA/C/core.h:154`; struct `CNA_ErrorInfo` `core.h:60-75`); the query routes do not overwrite it.
- Handles: `CNA_Handle` = `uint64_t`, `CNA_INVALID_HANDLE` = 0 (`abi.h:104,107`); slot in the low 32 bits, generation in the high 32; the registry checks runtime, kind, generation ([DOC] `HANDLES.md:3-17`). Zero, stale, wrong-kind or foreign handle -> `CNA_RESULT_INVALID_HANDLE`; a second release of an owned handle -> `CNA_RESULT_INVALID_HANDLE` (idempotence-detecting).
- One active runtime/game per process: creating a second returns `CNA_RESULT_INVALID_STATE` (`modules/c-api/src/CnaCApiRuntime.cpp:43,643,664,821` [SRC]; `HANDLES.md:55` [DOC]).
- Booleans: `CNA_Bool` = `uint8_t`, only 0/1 valid; every route taking one refuses other bytes with `CNA_RESULT_INVALID_ARGUMENT` (0.3.0 behaviour; generated test `CApi_BoolContractSmoke`).
- Strings/buffers: `CNA_StringView { const char* data; uint64_t byte_length; }` UTF-8 (`core.h:80-86`); output strings use count-then-copy, the count excludes any terminator, and a too-small buffer is refused with no partial write (`examples/c/hello_cna.c:67-74`, `:116-123`).
- Versioned structs start with `struct_size` and `struct_version`; the caller sets `sizeof` and the documented version; extra trailing fields are additive ([DOC] `ABI_VERSIONING.md:354-372`; used at `hello_cna.c:61-62,109-110`).
- Ownership categories (owned / borrowed / retained / transferred / callback context / caller buffer) and child-before-parent destruction: `cna_game_destroy` returns `CNA_RESULT_INVALID_STATE` while an owned graphics child is live ([DOC] `OWNERSHIP.md`); the graphics-device handle is borrowed and valid only inside a lifecycle callback (`hello_cna.c:79-106`).
- Threading: lifecycle, game, graphics, content, input, media, device and resource-destruction calls belong to the runtime's creation thread; a wrong-thread call returns `CNA_RESULT_THREAD` (`modules/c-api/src/CnaCApiDetail.cpp:45,304,321,338` [SRC]; `CALLBACKS_AND_THREADING.md` [DOC]). Lifecycle callbacks run synchronously on that thread; they may call `cna_game_request_exit`, `cna_game_clear`, `cna_game_set_window_title`, not `cna_game_run` / `_run_one_frame` / `_destroy` (`CNA_RESULT_INVALID_STATE`).
- Capability discipline: branch on `cna_graphics_device_supports_capability` and renderer feature queries, never on the renderer name (`hello_cna.c:125-132`).
- The exported surface does not vary with configuration: all four measured configurations export the same 4,055 names; a route whose backend is compiled out exists and answers `CNA_RESULT_NOT_SUPPORTED` ([DOC] `ABI_VERSIONING.md:428-436`, `COMPATIBILITY.md:34-48`).

### C8. Examples / first program

- One shipped C program: `modules/c-api/examples/c/hello_cna.c` (354 lines), built by `modules/c-api/examples/c/CMakeLists.txt` as a standalone project: `cmake_minimum_required(VERSION 3.20)`, `project(cna_c_examples LANGUAGES C)`, `find_package(CNA 0.1 CONFIG REQUIRED)`, `target_link_libraries(hello_cna PRIVATE CNA::CApi)` and, if present, `hello_cna_static` linked to `CNA::CApiStatic` (`CMakeLists.txt:15-57`). It demonstrates: ABI check first, `cna_game_create` with C callbacks, borrowing the graphics device in a callback, capability queries, count-then-copy, reading the error diagnostic after deliberate failures, creating/uploading/drawing a texture, and teardown children-then-game (`hello_cna.c:17-26`). It is guarded so it exits cleanly headless (`hello_cna.c:13-15`).
- Non-CMake consumption: `cc -std=c99 -I<prefix>/include main.c -L<prefix>/lib -lcna_c_api` ([DOC] `CONSUMING.md:66-73`; consistent with the install layout above).
- Alpha.1 tutorial 129 snippet API names still exist: `cna_get_abi_version`, `CNA_GameCreateInfo` (`runtime.h:177-198`; fields `is_fixed_time_step` `:185`, `target_elapsed_time_ticks` `:191`, `window_title` `:194`), `cna_game_create` (`:207`), `cna_game_run` (`:227`), `cna_game_request_exit` (`:235`), `cna_game_destroy` (`:266`). Its `find_package(CNA 0.7 ...)` would still be accepted by the 0.29.0 package (same major, minor >= requested) but the shipped example requests `0.1`.

### C9. ABI-checking tooling (summary)

`generate_abi_baseline.py` (layouts, offsets, widths, constants, exports, runtime version; `abi_baseline.json`), `check_declared_exports.py` (header-declared vs library-exported set difference in both directions; docstring says it originated from a report by the C# binding), `check_doc_export_counts.py` (prose counts must match the exported count), `check_release_gate.py` + `release_gate.json`, `generate_compatibility_matrix.py`, `generate_coverage_inventory.py`, `generate_limitations.py`, `check_route_test_coverage.py` (ratchet, budget 0), `generate_bool_contract_test.py`, `generate_artifact_manifest.py` (JSON schema `cna-c-abi-artifact/1`: file name/size/sha256/build-id/exported route count, source HEAD + dirty flag, ABI version, target OS/arch, selected renderer/platform/audio/CNAEXT/video from `CMakeCache.txt`; `status` is `BUILT` and nothing more), `generate_wasm_exports.py`, `generate_static_archive.py`.

---

## Bindings boundary

What CNA itself says and publishes (the binding repos were not analyzed).

- Scope rule [DOC `plans/plan_binding.md:21,59,176`]: the C ABI plan is "intentionally not a plan for C#, .NET, JavaScript/TypeScript, Rust, Python, Java, Zig, Go, Swift, or any other language-specific binding"; "a language-specific binding, wrapper, package, generator or sample for any language other than C" is a non-goal inside the CNA repository. `CLAUDE.md:33-35` (TARGET) points at `plans/plan_bindings_upstream.md` for divergences "the language bindings measured".
- Binding repos named in CNA: `plans/plan_bindings_upstream.md:3-4` says "Ten language bindings live in `../_bindings`: `cna-cs`, `cna-common-lisp`, `cna-go`, `cna-java`, `cna-python`, `cna-ruby`, `cna-rust`, `cna-swift`, `cna-ts`, and their templates" (nine named plus templates; CNA says ten). Other names appear only in design notes (`misc/analysis_binding*.md`: `cna-dotnet`, `cna-js`, `cna-rs`, `cna-sys`, `cna-zig`) and in code comments: `cna-ts` (`modules/c-api/CMakeLists.txt:138`, `modules/c-api/wasm/module_smoke.mjs:6`), `cna-cs` (`modules/c-api/tests/pure_c/OwnedGraphicsDeviceSmoke.c:6`, `docs/c-api/CABI_BLOCKER_HANDOFF.md:4,164`). The site's related-project card for `cna-cs` ("CNA.NET") is the only binding it links today.
- Expected ABI markers CNA publishes: `cna_get_abi_version()` -> encoded `0x00001D00` for 0.29.0 (`abi.h:34-44,114`); the `CNA_ABI_VERSION` macro; CMake package version == ABI version with `SameMajorVersion` (`modules/c-api/CMakeLists.txt:452-479`); ELF symbol-version node `CNA_C_API_0.1` (never bumped for minors); `tools/c-api/abi_baseline.json` as the machine-readable contract (all struct layouts, constants, exports); per-artifact `generate_artifact_manifest.py` JSON for "which file is this".
- Historical pins recorded by CNA [DOC, not current]: bindings measured ABI 0.7.0-0.21.0 (`plans/plan_bindings_upstream.md:10-13`); `cna-cs` policy named 0.6.0-0.8.0 and would refuse 0.9.0 until extended; `cna-rust` pinned `CNA_ABI_VERSION = 0x0000_0700` with exact equality (`plans/plan_cabi.md:1182-1189`). CNA does not state which ABI each binding expects today.
- What CNA generates or validates for bindings: the wasm export list (`generate_wasm_exports.py`, a build dependency of `cna_c_api_wasm`, `modules/c-api/CMakeLists.txt:113-136`); the export/declaration set-difference gate (`CApiDeclaredExports`); the WebAssembly ABI contract note `docs/c-api/WASM_ARTIFACT.md` (BigInt for by-value `uint64_t`, no NUL on copied strings, `_malloc`/`_free`/`addFunction` exported) [DOC]. CNA generates **no** language bindings itself.

---

## Diagnostics

**What it is.** `modules/diagnostics`, namespace `CNA::Diagnostics`: a renderer-independent, in-process observation layer (counters, gauges, per-frame counters, frame history, resource metadata, optional CPU zones/markers/event history, bounded recording and trace export). Only the C++ standard library; **no thread, no socket, no renderer dependency** (`modules/diagnostics/CMakeLists.txt:1-10`, `modules/diagnostics/include/CNA/Diagnostics/Diagnostics.hpp:1-11`). It has no XNA counterpart and **no C ABI routes** (grep of `modules/c-api` finds no `Diagnostics`/`Inspector` reference).

**How to enable.**
- CMake: `-DCNA_DIAGNOSTICS=OFF|STATS|FULL` (cache string, default `OFF`, case-normalized, an invalid value is a `FATAL_ERROR`; maps to `CNA_DIAGNOSTICS_LEVEL` 0/1/2) `CMakeLists.txt:153-171`. `CNA_DIAGNOSTICS_LEVEL=${...}` is a **public compile definition** of `cna_build_config`, so engine and application share it (`modules/CMakeLists.txt:243`). `cna_diagnostics` is always part of the `CNA` umbrella (`modules/CMakeLists.txt:395`); with `OFF` it links but does nothing. Header fallback: `CNA_DIAGNOSTICS_LEVEL` defaults to 0 and values outside 0-2 are a `#error` (`Diagnostics.hpp:13-19`).
- Runtime: `GetBuildMode()` (constexpr = compile level, `Diagnostics.hpp:627-630`), `GetRuntimeMode()` (`:636`; returns `Off` in OFF builds, `Diagnostics.cpp:1323-1329`), `SetRuntimeMode(Mode)` (`:643`, `Diagnostics.cpp:1332-1345`): rejects a mode above the build mode; a mode change bumps a generation counter so open zones are invalidated. The initial runtime mode equals the build mode (`Diagnostics.cpp:248`).
- **No environment variables** in Diagnostics or the Inspector agent (`grep getenv` over both modules finds only `CNA_INSPECTOR_TOKEN` in `modules/inspector/src/InspectorMain.cpp:149`, the separate bridge process).

**Public headers / API** (`modules/diagnostics/include/CNA/Diagnostics/`).
- `Instrumentation.hpp` macros: STATS and FULL (`CNA_DIAGNOSTICS_LEVEL >= 1`, `:19-68`): `CNA_DIAGNOSTICS_COUNTER_ADD(name,delta)`, `CNA_DIAGNOSTICS_GAUGE_SET`, `CNA_DIAGNOSTICS_GAUGE_ADD`, `CNA_DIAGNOSTICS_FRAME_COUNTER_ADD`, `CNA_DIAGNOSTICS_FRAME_SCOPE()`. FULL only (`>= 2`, `:70-100`): `CNA_PROFILE_SCOPE(name)`, `CNA_PROFILE_SCOPE_CATEGORY(name,cat)`, `CNA_DIAGNOSTICS_EVENT(name)`, `CNA_DIAGNOSTICS_EVENT_CATEGORY(name,cat)`. In lower modes every macro expands to `do { (void) sizeof((args)); } while(false)` (`:17,62-67,95-99`): arguments are type-checked but **never evaluated**; a test asserts this (`modules/diagnostics/tests/CNA/Diagnostics/DiagnosticsTests.cpp:107`, `DisabledMacrosDoNotEvaluateArguments`). Names at macro sites register once through function-local statics.
- `Diagnostics.hpp`: enums `Mode{Off,Stats,Full}`, `MetricUnit{Count,Bytes,Nanoseconds,PerSecond,BasisPoints}`, `MetricKind{Counter,Gauge,FrameCounter}`, `Accuracy{Exact,Estimated,Unavailable}`, `Category{Core,Update,Draw,Graphics,Audio,Content,Application,Gpu}`, `EventKind{Zone,Marker,Frame,ResourceCreated,ResourceDestroyed,Malformed}`, `ResourceKind{Unknown,Texture2D,Texture3D,TextureCube,VertexBuffer,IndexBuffer,RenderTarget2D,RenderTargetCube,AudioVoice,Custom}` (`:24-132`); handles `NameHandle`, `CounterHandle`, `GaugeHandle`, `FrameCounterHandle` (registering constructors, `:148-261`); `IDiagnosticsSource` + `FrameStatisticsSink` + `SourceRegistration` / `RegisterSource` (`:263-354`); `ResourceDescriptor` / `ResourceRecord` / `ResourceHandle` RAII (`:403-482`); `BeginZone` / `EndZone` / `ZoneScope` / `MarkEvent` (`:484-541`); `BeginFrame` / `EndFrame` / `FrameScope` (`:543-564`); `Snapshot` and `IDiagnosticsProvider` (`InterfaceVersion = 1`, `:589`; `CaptureSnapshot`, `ReadEvents(afterSequence, maxEvents)`, `ResolveName`; `:585-615`), `GetProvider()` (`:621`); `Trace` (`FormatVersion = 1`, `WriteBinary`, `ReadBinary`, `WriteChromeTrace`, `:646-703`), `RecordingSession`, `StartRecording(maxEvents)`, `StopRecording(session)` (`:705-756`).

**Built-in engine instrumentation** [SRC].
- Frames: `Game::Tick` and the Emscripten main-loop callback each open `CNA_DIAGNOSTICS_FRAME_SCOPE()` plus `CNA_PROFILE_SCOPE_CATEGORY("Game/Tick", Core)` (`modules/runtime/src/Game.cpp:615-616`, `:1081-1082`); zones `Game/Update` (`:663,712`) and `Game/Draw` (`:732`); frame counters `Runtime/UpdateCount` (`:666,715`) and `Runtime/DrawCount` (`:736`).
- Graphics (common `GraphicsDevice`, not per renderer): frame counters `Graphics/DrawCalls`, `Graphics/IndexedDrawCalls`, `Graphics/NonIndexedDrawCalls`, `Graphics/SubmittedPrimitives`, `Graphics/IndirectDrawCalls` (`modules/graphics/src/Xna/GraphicsDevice.cpp:68-84`), `Graphics/EffectChanges` (`:3827`), `Graphics/RenderTargetChanges` (`:5397,5504`); `Graphics/TextureBindingChanges` (`modules/graphics/src/Xna/TextureCollection.cpp:94`); `Graphics/SpriteSubmissions` (`modules/graphics/src/Xna/SpriteBatch.cpp:491`). Resource metadata is registered by Texture2D/3D/Cube, RenderTarget2D/Cube, VertexBuffer and IndexBuffer (`modules/graphics/src/Xna/*.cpp`, helper `modules/graphics/include/CNA/Internal/Graphics/DiagnosticResource.hpp`, compiled only when `CNA_DIAGNOSTICS_LEVEL >= 1`).
- Audio: gauge `Audio/AllocatedVoices`, counter `Audio/VoiceCreations` in both mixer engines (`modules/audio/src/Backend/CnaMixer/MixerEngine.cpp:235,380-396`, `.../Sdl3Mixer/MixerEngine.cpp:328,449-459`).
- Not published anywhere in the tree: GPU timings, input metrics, total process/driver memory. No production code registers an `IDiagnosticsSource` or an Inspector preview provider (grep of `modules/` for `RegisterSource(` / `IResourcePreviewProvider`: hits only in `modules/inspector` and tests). Texture format metadata is the numeric `SurfaceFormat` value. (CHANGELOG mentions Vulkan GPU timing query pools, but they are not wired to Diagnostics.)

**Limits (compile-time constants).** `MaximumZoneDepth = 64`, `ThreadEventCapacity = 1024` (per-thread ring), `EventHistoryCapacity = 32768` (process ring), `FrameHistoryCapacity = 240` (`Diagnostics.hpp:139-145`); `MaximumMetrics = 512`, `MaximumFrameMetrics = 64` (frame counters copied per historical frame), `MaximumTraceNames = 65,536`, `MaximumTraceNameBytes = 1 MiB`, `MaximumTraceTotalNameBytes = 16 MiB` (`Diagnostics.cpp:23-27`). Registrations beyond 512 return an inert handle; a conflicting re-registration (kind/unit/accuracy) returns an inert handle; a full producer ring drops **new** events and counts them; the process ring overwrites the **oldest** and counts overwrites.

**Overhead facts derivable from code.** OFF: macros compile out and evaluate nothing; no state object, thread or lock is reachable from them (CNA's benchmark note says an `nm -u` check of `Game.cpp`, `GraphicsDevice.cpp`, `SpriteBatch.cpp`, `TextureCollection.cpp` objects shows no `CNA::Diagnostics` reference [DOC]). STATS: `AddMetric` / `SetMetric` are one relaxed atomic RMW/store after a relaxed runtime-mode load (`Diagnostics.cpp:344-362`); frame end iterates only registered metrics (`:700-782`) and invokes registered sources synchronously (`CollectDiagnosticsSources`, from `EndFrame` only; never a background thread). FULL: zones/markers write into a thread-local ring; the first event on a thread allocates its context; merging into the process ring happens at frame boundaries or explicit provider reads. A microbenchmark exists (`modules/diagnostics/benchmarks/DiagnosticsBenchmark.cpp`: 5,000,000 iterations, 512-op batches for zones; built with `-DCNA_BUILD_BENCHMARKS=ON` as `cna_diagnostics_benchmark`, `modules/diagnostics/CMakeLists.txt:6-10`). CNA's recorded numbers [DOC `docs/diagnostics-benchmark.md`; AMD Ryzen 7 PRO 7840U, GCC 14.2, Release, median of 7, pinned to one CPU]: OFF within noise of the empty loop; STATS frame-counter update about 1.6 ns; FULL completed scoped zone about 64 ns. **I did not reproduce these**; publish only with the machine qualifier, or omit.

**Trace formats.** `Trace::WriteBinary`: magic bytes `CNATRACE`, u16 version 1, u16 reserved, u32 name count, u64 event count, u64 dropped, names then events, little-endian; the reader rejects bad magic/version, truncation, invalid enums, more than 65,536 names, a name over 1 MiB, more than 16 MiB of names, more than 32,768 events (`Diagnostics.cpp:1356,1389-1415`). `WriteChromeTrace` streams Chrome Trace Event JSON without building a whole document. `StartRecording` returns an active session only in FULL and clamps `maximumEvents` to the history size (`Diagnostics.cpp:1486-1492`); `StopRecording` copies at most that many newest events.

**Tests.** `modules/diagnostics/tests/CNA/Diagnostics/DiagnosticsTests.cpp`: 40 `TEST` definitions [CALC]; plus `modules/graphics/tests/Microsoft/Xna/Framework/Graphics/GraphicsDiagnosticsTests.cpp` (6) and `modules/audio/tests/CNA/AudioDiagnosticsTests.cpp` (1). They are part of the ordinary `CnaTests` glob; focused target `CnaDiagnosticsTests` (`cmake/UnitTests.cmake:444`). **No CI workflow configures `CNA_DIAGNOSTICS` other than OFF or `CNA_BUILD_INSPECTOR=ON`** (grep of `.github/workflows` finds only the unrelated `CNA_DIRECT2D_DIAGNOSTICS`).

**Minimal verified recipe (Diagnostics only).**
```sh
cmake -S . -B build -DCNA_DIAGNOSTICS=FULL          # or STATS
```
```cpp
#include "CNA/Diagnostics/Instrumentation.hpp"
#include <fstream>
void Simulate() {
    CNA_PROFILE_SCOPE_CATEGORY("Physics/Simulate", CNA::Diagnostics::Category::Update);   // FULL
    CNA_DIAGNOSTICS_FRAME_COUNTER_ADD("Physics/Contacts", 12);                            // STATS and FULL
    CNA_DIAGNOSTICS_GAUGE_SET("Physics/ActiveBodies", 340);
}
// after some frames have run:
auto snap = CNA::Diagnostics::GetProvider().CaptureSnapshot();      // metrics, recentFrames, resources
auto rec  = CNA::Diagnostics::StartRecording(4096);                  // FULL only, otherwise inactive
/* ... run frames ... */
auto trace = CNA::Diagnostics::StopRecording(rec);
std::ofstream out("trace.json"); (void) trace.WriteChromeTrace(out);  // Chrome/Perfetto-loadable
```
(Every call above exists as cited; the game links `CNA`, which carries `CNA_DIAGNOSTICS_LEVEL`.)

---

## Inspector

**What it is.** An optional development tool that observes a running CNA app through the version-1 diagnostics provider. Two parts: (a) an in-process **agent** (`CNA::Inspector::Agent`, one background thread, authenticated TCP, compact binary protocol) and (b) a separate **`cna-inspector` bridge process** that serves an offline browser UI at `http://127.0.0.1:<port>/` and talks to the agent. The agent never embeds a web server or builds JSON. It is **view-only**: the protocol has only the messages listed below (no editing, scripting, input injection, arbitrary memory or method access).

**How to enable.**
- CMake: `-DCNA_BUILD_INSPECTOR=ON` (default `OFF`) `CMakeLists.txt:151`; `modules/inspector/CMakeLists.txt:5-41` builds static library `cna_inspector` (`CNA::Inspector`; public deps `cna_diagnostics`, `cna_core_headers`; private `Threads`, and `ws2_32` + `bcrypt` on Windows), executable **`cna-inspector`** (`src/InspectorMain.cpp`), and, with `CNA_BUILD_EXAMPLES` (default ON), the demo **`cna_inspector_demo`** (output in the build root, `:29-34`); benchmarks with `CNA_BUILD_BENCHMARKS`. The module is **not** in the `CNA` umbrella: a game links `CNA CNA::Inspector` explicitly.
- Combine with `-DCNA_DIAGNOSTICS=STATS|FULL`: provider `buildMode >= Stats` yields snapshot/resource capabilities; `>= Full` adds `Events` and `CpuZones`; `ResourcePreviews` only if the application supplies a preview provider (`modules/inspector/src/Agent.cpp:313-324`). With `OFF` a session negotiates but shows nothing useful.
- Application activation is explicit code, not a flag: `CNA::Inspector::Agent::Start(AgentConfiguration, error)` returns `std::unique_ptr<Agent>` or null with `error` (`Agent.hpp:88-102`). There is **no static initializer, no environment hook, no automatic Game change**; without the call no listener or thread exists.
- **Platform / renderer requirements**: desktop Windows, Linux, macOS/POSIX only; `CNA_BUILD_INSPECTOR=ON` is a configure `FATAL_ERROR` on Emscripten, Android and iOS (`modules/inspector/CMakeLists.txt:6-10`). Uses only std plus OS sockets/RNG (POSIX sockets + `/dev/urandom`; Winsock2 + `BCryptGenRandom`, `InternalSocket.cpp:188,196`). No renderer requirement: the demo says it "runs under any platform, including HEADLESS" (`examples/inspector_demo.cpp:6`). CNA claims native-MSVC and Linux+Chrome end-to-end validation and macOS "implemented, runtime validation pending" [DOC `docs/inspector.md:280-289`]; no CI workflow covers any of it.

**Public headers** (`modules/inspector/include/CNA/Inspector/`): `Agent.hpp` (`AgentConfiguration`, `IResourcePreviewProvider`, `Agent`), `Client.hpp` (`ClientConfiguration`, `Client`: `Connect`, `CaptureSnapshot`, `ReadEvents`, `RequestPreview`, `PollPreview`, `Ping`), `Protocol.hpp` (wire types).

`AgentConfiguration` defaults (`Agent.hpp:41-55`): `bindAddress "127.0.0.1"`, `port 0` (ephemeral; read back with `GetPort()`), `allowRemote false`, empty `authenticationToken` (then a 256-bit token is generated from the OS secure RNG, `Agent.cpp:57-62,140`; read with `GetAuthenticationToken()`), `applicationName "CNA application"`, `platformBackend` / `buildConfiguration` auto-filled if empty (`Agent.cpp:150-156`), `metadata` (max 64 entries, key <= 128 bytes, value <= 1024 bytes: `Agent.cpp:129`, `Protocol.cpp:688`), `previewProvider` null, `maximumRequestsPerSecond 64` (clamped to 1..1024, `Agent.cpp:144-145`), `maximumPendingPreviews 4`, `previewCooldownMilliseconds 250`. Session identity (`cnaVersion`, `targetPlatform`, `graphicsRenderer`) is filled from `CNA::getVersionString()`, `CNA::getCurrentPlatformName()`, `CNA::getCurrentGraphicsRendererName()` (`Agent.cpp:339-343`).

**Transport, protocol, security** [SRC].
- Agent <-> bridge: TCP, plaintext, little-endian, fixed **24-byte header** with magic `CNAI` (`0x49414E43`), major 1, minor 0, message type, flags 0, payload length (max **8 MiB**), request id (`Protocol.cpp:14-15`, `Protocol.hpp:16-24,117-126`). Messages: `ClientHello`=1 `ServerHello`=2 `Error`=3 `SnapshotRequest`=10 `SnapshotResponse`=11 `EventsRequest`=12 `EventsResponse`=13 `PreviewRequest`=14 `PreviewPollRequest`=15 `PreviewResponse`=16 `Ping`=17 `Pong`=18 (`Protocol.hpp:27-53`); capability bits `Snapshots, Events, ResourceMetadata, CpuZones, Accuracy, Discontinuities, ResourcePreviews` (`:56-72`); error codes `InvalidRequest, UnsupportedVersion, Unauthorized, Unavailable, LimitExceeded, Busy, InternalError` (`:86-102`). At most 4,096 events per response, preview at most 4 MiB (`:22,24`); preview request bounds default 1024x1024, protocol maximum 4096x4096 (`Protocol.hpp:217-218`, `Protocol.cpp:849-850`).
- Agent limits: handshake timeout 3 s, socket timeout 30 s (`Agent.cpp:24-25`); listen backlog **4** (`InternalSocket.cpp:264`); one authenticated client and one request at a time; a non-loopback bind is rejected unless `allowRemote` (`Agent.cpp:123-127`, "non-loopback Inspector binding requires allowRemote=true"); authentication happens before the provider is queried (test `RejectsBadAuthenticationWithoutProviderAccess`).
- Bridge (`cna-inspector`, `src/InspectorMain.cpp`): options `--agent-host` (default 127.0.0.1), `--agent-port` (required), `--token`, `--token-file` (<= 256 bytes, trailing CR/LF stripped), `--http-port` (default ephemeral), `--allow-remote-agent`, `--help` (`InspectorMain.cpp:16-31,80-139`); the token may come from **`CNA_INSPECTOR_TOKEN`** (`:149`); a non-loopback agent host requires `--allow-remote-agent` (`:160-165`); it prints `CNA Inspector is available at http://127.0.0.1:<port>/` (`:176-178`). HTTP server: always binds `127.0.0.1`, up to **32** concurrent connections (excess refused), 16 KiB request cap, 12 MiB response cap, 5 s I/O timeout, **1 s header timeout** (`WebBridge.cpp:26-37`), requires `Host == 127.0.0.1:<port>` (`:642-648`), serves `/`, `/style.css`, `/app.js`, injects a per-process UI token into the page and requires header `x-cna-inspector-ui-token` on every `/api/` request (`:650-671`); API routes `GET /api/session`, `GET /api/snapshot`, `GET /api/events`, `POST /api/preview`, `GET /api/preview` (`:682-743`); responses carry `Cache-Control: no-store`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: no-referrer` and a CSP `default-src 'self'; ... frame-ancestors 'none'` (`:788-792`); no CORS header. 64-bit integers are JSON strings for JavaScript safety.

**What the UI displays** (embedded assets, no CDN; `modules/inspector/src/WebAssets.cpp:25-32,37-82,97-124`): eight views - **Session** (CNA version, target, platform backend, renderer, build, protocol and provider versions, exposure local/remote, metadata, negotiated capabilities), **Performance** (FPS, frame time, frame graph from the 240-frame history, frame number, metric and resource counts, profiler memory lower bound, metrics table with unit/kind/accuracy), **CPU profiler** (hot zones aggregated over the latest 1,000 retained events, recent timeline), **Graphics** (draw calls, primitives, texture-binding changes, resource count, declared resource bytes; states there is no shader reflection), **Resources** (sortable/filterable, fetched only on open/Refresh; id, kind, label, dimensions, format, mips, bytes, accuracy, per-row Preview button enabled only for texture/render-target kinds when the capability exists), **Audio** (`Audio/AllocatedVoices`, `Audio/VoiceCreations`, audio resources; "not necessarily audible"), **Input** (explicit unavailable state), **Events** (filterable log: sequence, frame, thread, kind, category, name, duration, value). It polls every 500 ms, pulls up to 512 events per round (up to 4 rounds), retains 1,000 locally, shows `—` for unpublished metrics, and its discontinuity banner reports only losses since it connected. **It controls nothing in the game** apart from user-initiated resource preview requests (`POST /api/preview`) and metadata refresh.
- Previews: `IResourcePreviewProvider` (`RequestPreview`, `PollPreview`) must return promptly; only registered texture/render-target ids; bounded; **no renderer installs one at TARGET**, so preview is unavailable in real sessions (verified by grep, above).

**Overhead / limits provable from code.** Without a call to `Agent::Start()` there is no listener, thread or work; a started agent with no client blocks in the OS (test `EnabledWithoutClientDoesNotPollProvider`, `InspectorTests.cpp:467`). Provider v1 returns an owned complete snapshot, so an overview request copies the resource registry internally even when the protocol omits it (consistent with the `CaptureSnapshot()` signature, `Diagnostics.hpp:598`). CNA's recorded numbers [DOC `docs/inspector-benchmark.md`, same machine as above]: linked-but-not-started and idle-agent loops within noise of the compiled-out control (+0.02 ns/iteration), zero idle provider calls; live snapshot about 71 us/request and a 512-zone profiling response about 121 us/request on the agent thread; a 1 MiB preview transport about 1.4 ms excluding GPU readback. Benchmarks: `cna_inspector_benchmark`, `cna_inspector_compiled_out_benchmark` (`modules/inspector/CMakeLists.txt:36-49`, built with `-DCNA_BUILD_BENCHMARKS=ON`).

**Tests.** `modules/inspector/tests/CNA/Inspector/InspectorTests.cpp`: 27 `TEST` definitions [CALC] (protocol round-trips/mutation/truncation, frontend asset assertions, real-loopback agent tests incl. reconnect, rate backpressure, preview bounds, descriptor-limit case, non-loopback authorization); compiled only when `CNA_BUILD_INSPECTOR=ON` (`cmake/UnitTests.cmake:62-66`); focused target `CnaInspectorTests` (`:451`).

**Minimal verified end-to-end recipe (Linux; headless is fine).**
```sh
cmake -S . -B build -DCNA_DIAGNOSTICS=FULL -DCNA_BUILD_INSPECTOR=ON   # CNA_BUILD_EXAMPLES is ON by default
cmake --build build --target cna_inspector_demo cna-inspector
build/cna_inspector_demo --port 47001 --seconds 60     # prints "Inspector port: N" and "Inspector token: T" (examples/inspector_demo.cpp:211-212)
CNA_INSPECTOR_TOKEN='<T>' build/modules/inspector/cna-inspector --agent-port 47001
# open the printed http://127.0.0.1:<port>/
```
Output locations verified: demo -> `${CMAKE_BINARY_DIR}` (`modules/inspector/CMakeLists.txt:33`); bridge -> `<build>/modules/inspector/` (no output-directory override anywhere in root/module CMake). Demo flags `--seconds N`, `--port P` (`inspector_demo.cpp:8,183-192`). The demo starts the agent before `Game::Run` and prints the token to stdout - **the token is a secret; do not paste it into shared logs**. In your own game (all calls verified in `Agent.hpp`):
```cmake
target_link_libraries(my_game PRIVATE CNA CNA::Inspector)
```
```cpp
#include "CNA/Inspector/Agent.hpp"
CNA::Inspector::AgentConfiguration cfg;
cfg.applicationName = "My game";
cfg.metadata = {{"Resolution", "1920x1080"}};
std::string err;
auto inspector = CNA::Inspector::Agent::Start(cfg, err);   // keep the unique_ptr alive for the app lifetime
if (inspector) { /* hand GetPort() and GetAuthenticationToken() to the developer over a local channel */ }
```

---

## Other new modules/tools

### O1. Modules (TARGET vs BASE; "site" = any published HTML page mentions it, by grep)

Counts are files under `include/`, `src/`, `tests/` [CALC].

| Module | BASE -> TARGET files (hdr / src / tests) | Verified description | On the site today? |
|---|---|---|---|
| `diagnostics` | 0 -> 2 / 1 / 1 | Renderer-independent metrics/profiler foundation (section Diagnostics). | No |
| `inspector` | 0 -> 3 / 10 / 1 | Optional agent + bridge + browser UI (section Inspector). | No |
| `content-pipeline` | 0 -> 107 / 86 / 48 | Build-time XNA-shaped Content Pipeline (`Microsoft::Xna::Framework::Content::Pipeline`, incl. `Serialization/Compiler/ContentWriter`, `ContentCompiler`) plus a FreeType `.spritefont` route (`CNA_ENABLE_FONT_PIPELINE` OFF/AUTO/ON, default AUTO) and FFmpeg-based MP3/WMA/WMV importers (`CNA_ENABLE_MEDIA_PIPELINE` OFF/AUTO/ON, default AUTO). Only `cna_content_compiler` links it, so FreeType/FFmpeg never enter a runtime game (`modules/content-pipeline/CMakeLists.txt:1-13,19-22,35-60`). Excluded from the C API (`COVERAGE.md:22`). | No (site documents only read-side XNB) |
| `design` | 0 -> 16 / 3 / 2 | `CNA::Design`: XNA 4.0 `Microsoft::Xna::Framework::Design` - `MathTypeConverter` (derives `System::ComponentModel::ExpandableObjectConverter`) plus 12 concrete converters (Point, Rectangle, Vector2/3/4, Quaternion, Matrix, Color, BoundingBox, BoundingSphere, Plane, Ray); registered by `EnsureFrameworkDesignConvertersRegistered()` through `TypeDescriptor::RegisterType`; links sharp-runtime `ComponentModel`; **opt-in, not in the `CNA` umbrella** (`modules/design/CMakeLists.txt`, `modules/design/src/Registration.cpp:26-40`, `modules/CMakeLists.txt:338,378-380`). 25 test definitions. | No; the site says the opposite ("except Framework.Design") |
| `phone` | 0 -> 9 / 3 / 2 | `Microsoft::Phone::Shell` (`PhoneApplicationService`: Launching / Activated / Deactivated / Closing events driven from `Game`'s platform lifecycle after an `AttachEXT` call) and `Microsoft::Phone::Notification` (`HttpNotificationChannel` with a local HTTP listener thread, `PushNotificationSender`, `RawPushNotificationMessage`): the Windows Phone 7 lifecycle/push API, not XNA 4.0. Depends on `runtime`. 18 test definitions. Out of C API scope (`COVERAGE.md:23`). | No |
| `video-ffmpeg` | 0 -> 0 / 2 / 0 | FFmpeg decoding split out of `media` into an optional STATIC archive `cna_video_ffmpeg` (`CNA::VideoFfmpeg`; `VideoDecoder.cpp`, `AudioDurationProbe.cpp`), selected by the new switch **`CNA_ENABLE_VIDEO` = OFF / AUTO (default) / ON** (`CMakeLists.txt:192-200`, `modules/CMakeLists.txt:9-57`); OFF or absent => file-backed `Video` throws `NotSupportedException`, while headers, readers and the metadata constructor stay ([DOC] `docs/video-backend.md`). | Partly (`docs/video-playback.html` describes auto-detected FFmpeg; the switch is missing) |
| `graphics-ext` (existing) | 14 -> 100 / 7 -> 265 / 3 -> 152 | Grew from a thin shim into the CNAEXT engine layer (`CNA::Graphics`: HDR pipeline, post-process passes, shadows, IBL, instancing/LOD, compute), with the implementation moved here; opt-in `CNA_CNAEXT` (default OFF). Its C surface is `engine_layer.h` (858 routes). | Partly (features.html mentions CNAEXT) |
| `platform` (existing) | src 77 -> 214, tests 49 -> 103 | Substantially expanded (CHANGELOG: native Win32 backend `CNA_PLATFORM=WIN32`, `CHANGELOG.md:33-42`; docs list `platform-x11.md`, `platform-wayland.md`, `platform-win32.md`). Owned by another agent. | Partly |
| `content` (existing) | hdr 38 -> 99, src 24 -> 78, tests 116 -> 174 | Large growth (CNB format, Model schema, XNB writer front ends). Owned by another agent. | Partly |
| `audio` 26->31 / 27->49 / 37->45; `graphics` 154->181 / 71->85 / 109->166; `runtime` 20->23 / 15->18 / 25->29; `core` 15->22 / 6->8 / 5->9; `input` 54->55 / 28 / 45->49; `math` 23->24 / 17 / 22->27; `devices` 31->33 / 23->24 / 27->28; `media` 36 / 32 / 32->33; `storage` 3 / 3 / 1 | moderate growth (hdr / src / tests). `devices-ext` (18/10/10), `gamer-services` (55/36/16), `net` (29/25/18) are unchanged in file counts. | Existing modules; not new. | Already covered |
| renderers | 47 directories -> 22 | 25 retired identities removed together with their implementations. Owned by another agent. | - |

Root/module build-flag additions worth a Building mention [CALC diff of `option(CNA_*)` and `set(CNA_* ... CACHE ...)`]: `CNA_BUILD_INSPECTOR`, `CNA_DIAGNOSTICS`, `CNA_BUILD_BENCHMARKS`, `CNA_ENABLE_VIDEO`, `CNA_ENABLE_FONT_PIPELINE`, `CNA_ENABLE_MEDIA_PIPELINE`, `CNA_ENABLE_SDL`, `CNA_SHARED_LIBRARY`, `CNA_ENABLE_EMSCRIPTEN_THREADS`, `CNA_ENABLE_IPO`, `CNA_ENABLE_PCH`, `CNA_ENABLE_UNITY_BUILD`, `CNA_DEBUG_INFO`, `CNA_LINKER`, `CNA_C_API_BUILD_STATIC`, `CNA_[retired renderers]_COMPILED_EFFECTS`, `CNA_OPENGL4/SOFTWARE/WEBGPU_COMPILED_EFFECTS`, `CNA_SDL_GPU_SHADERCROSS`, `CNA_CNB_ZSTD`, `CNA_FXC_EXECUTABLE` / `CNA_FXC_LAUNCHER`. **`CNA_SHARED_LIBRARY` defaults ON on native ELF GNU/Clang builds with CMake >= 3.27** (`CMakeLists.txt:43-66`): executables link one `libcna.so` instead of carrying a static engine copy each - a behaviour change for `add_subdirectory` consumers on Linux, absent at BASE.

### O2. CLI tools (new since BASE unless noted) [SRC]

- **`cna-content`** (target `cna_content_tool`, `OUTPUT_NAME "cna-content"`, `cmake/ToolContentPipeline.cmake:17-22`; sources `tools/content/content.cpp`, `content_main.cpp`): `cna-content build <source|dir|.contentproj> -o <out> [--format cnb|xnb] [--config] [--workers 1..64] [--xnb-platform] [--xnb-version 4|5] [--xnb-profile reach|hidef] [--xnb-compress none|lzx|lz4] [--xnb-reader-names xna40|portable] [--fx-compiler] [--xma-encoder] [--font-directory] [--explain] [--quiet] [--xna-compatible] [--only-configured-assets]` and `cna-content clean <dir>` (`tools/content/content.cpp:283-345`). Importer -> Processor -> Writer; CNB is the default output; **XNB is written with real LZX compression**; `.fx` needs an external fxc-compatible compiler (option, then `CNA_FXC` env, then the CMake-baked path, then `fxc` on PATH); `.contentproj` builds are supported; the `xbox360` platform is refused unless `--xnb-allow-unverified-xbox`. CMake function `cna_add_content(TARGET ... SOURCE_DIR ... OUTPUT_DIR ... FORMAT ...)` (`cmake/ToolContentPipeline.cmake`). Examples: `cna_custom_content_compiler_example`, `cna_xna_custom_pipeline_example`.
- **`cna_tool_cnb_info`** (`cmake/ToolCnbInfo.cmake`, `tools/cnb_info/cnb_info.cpp`): offline `.cnb` inspector/validator; needs no device.
- **`cna_tool_source_to_cnb`** (`tools/source_to_cnb/`): direct source (image/DDS/WAV/...) -> `.cnb`.
- **`cna_tool_cnj_to_cnb`** (`tools/cnj_to_cnb/`): `.cnj` -> `.cnb`.
- **`cna_tool_gltf_to_cnb`** (`tools/gltf_to_cnb/`): glTF -> `.cnb` (shares the `CNA::Content` implementation with `cna-content`).
- **`cna_tool_xnb_interop_fixtures`** (`tools/xnb/generate_interop_fixtures.cpp`): writes the committed CNA-generated XNB corpus and expected-value manifests.
- **`cna-inspector`** (Inspector bridge; section Inspector).
- Existing at BASE: `cna_tool_gltf_to_cnj` (`cmake/ToolGltfToCnj.cmake`).
- Other new `tools/` directories: `build/` (build-performance and clang time-trace analysis), `provenance/` (`provenance_gate.py`, `third-party.json`, `derived-sources.json`, `license-baseline.json`: gate that no proprietary binary or font is tracked, every C++ source under `modules/ tools/ spikes/` declares `SPDX-License-Identifier: MS-PL`, vendored and adapted third-party code is declared; registered in `cmake/XnaPipelineParityGates.cmake:133-146`), `shader_package/`, `tests/run_gtest_bounded.sh` (bounded-memory GoogleTest runner), `xna-pipeline-oracle/` (113 files), `xna-sample-sweep/`, `xnb/`, `vulkan/`, `opengl4/`, `common/` (atomic-write and numeric-argument helpers). Removed: `tools/[retired]`.
- Scripts: 73 -> 65 in `scripts/`; new `check_cnaext_*.{py,sh}`, `check_removed_renderer_api.py`, `check_test_display_isolation.py`, `check_renderer_configure_sweep.sh`, `run-parity-*.sh`, `run-webgpu-*.sh`, `scripts/ci/clone_siblings.sh`; removed the [retired]-10, Open[retired] and [retired] scripts. `programs.md` (Debian package requirements) changed only by dropping [retired]-specific text.

### O3. Examples

- Top-level `examples/` contains exactly `xvfb_screenshot_demo.cpp` and `golden/` at both BASE and TARGET. The published "28 demo programs under `examples/`" is therefore **misplaced**: the 28 `cna_demo_*` `add_executable` targets (identical name set at BASE and TARGET [CALC]) live in module example trees (`modules/graphics/examples`, `audio`, `input`, `devices`, `gamer-services`, `net`, ...), per `docs/physical-modules.md` [DOC] and the CMake registrations. Names: `cna_demo_2d`, `_achievement_showcase`, `_avatar`, `_avatar_animation_gallery`, `_avatar_appearance_tint_studio`, `_avatar_bone_state_boundary`, `_avatar_dual_compare`, `_avatar_multi_attach_stress`, `_avatar_wardrobe_hotswap`, `_devices`, `_friends_and_gamercard`, `_gamer_profile_privileges`, `_gamer_roster_hud`, `_gamerservices_dispatcher_watchdog`, `_gamerservices_signin_presence`, `_guide_overlay_console`, `_input`, `_leaderboard_viewer`, `_net_avatar_sync`, `_net_client_server_arena`, `_packet_roundtrip`, `_qos_probe`, `_renderer_selection`, `_session_browser`, `_session_lifecycle_events`, `_simulated_network_conditions`, `_sound`, `_xact`. New: `cna_inspector_demo`, `cna_custom_content_compiler_example`, `cna_xna_custom_pipeline_example`, and the C example `hello_cna`.
- Total example/probe source files under `modules/*/examples` (`.cpp/.c/.mm`): BASE 1,298 -> TARGET 986 (many are renderer-specific contract tests and parity fixtures, not demos; the drop is renderer retirement). This is not a "demo" count and should not be published as one.

---

## Project statistics (method + numbers)

### S1. Test files and GoogleTest-family definitions (site method reproduced exactly)

Method that reproduces the BASE figures **exactly** (568 files, 539 with macros, 8,263 definitions; matches `index.html:139` title text and `docs/verification.html:138`):
1. Candidate files = every `*.cpp`, `*.cc`, `*.cxx` under `modules/` or `tests/` whose path contains a directory component named `tests` (vendored `third_party/` and `vendor/` are outside those roots). BASE: 552 under `modules/**/tests/` + 16 in top-level `tests/` = 568.
2. Definition = a line matching `^\s*(TEST|TEST_F|TEST_P|TYPED_TEST|TYPED_TEST_P)\s*\(` (multiline regex; all five counted together, not deduplicated, no preprocessing; `INSTANTIATE_*` and `GTEST_TEST` not counted). BASE: TEST 6,299 + TEST_F 1,925 + TEST_P 39 = 8,263; TYPED_* 0; `INSTANTIATE_TEST_SUITE_P` 9 not counted.
3. "Files with macros" = files with at least one match.

| | BASE | TARGET |
|---|---:|---:|
| C++ test files (step 1) | 568 | **903** |
| of which contain a counted macro | 539 | **871** |
| `TEST` | 6,299 | 9,718 |
| `TEST_F` | 1,925 | 2,778 |
| `TEST_P` | 39 | 114 |
| `TYPED_TEST` / `TYPED_TEST_P` | 0 / 0 | 0 / 0 |
| **Definitions (site method)** | **8,263** | **12,610** |
| `INSTANTIATE_TEST_SUITE_P` (not counted by the site) | 9 | 84 |
| all-macro total incl. INSTANTIATE | 8,272 | 12,694 |

No file outside those paths contains the macros (checked over `*.cpp, *.cc, *.cxx, *.mm` excluding `third_party`/`vendor`). Reproduce (Python 3, from a CNA checkout root):
```python
import os, re
pat = re.compile(r'^\s*(TEST|TEST_F|TEST_P|TYPED_TEST|TYPED_TEST_P)\s*\(', re.M)
files = [os.path.join(dp, f) for top in ('modules', 'tests')
         for dp, _, fs in os.walk(top) if 'tests' in dp.split(os.sep)
         for f in fs if f.endswith(('.cpp', '.cc', '.cxx'))]
defs = sum(len(pat.findall(open(f, errors='replace').read())) for f in files)   # 12,610 at TARGET
```
Per-module definitions at TARGET (files/definitions): audio 38/765, c-api 7/0 (C smoke programs, not GoogleTest), content 170/1,871, content-pipeline 47/487, core 9/106, design 2/25, devices 27/474, devices-ext 10/56, diagnostics 1/40, gamer-services 14/382, graphics 161/2,906, graphics-ext 92/967, input 47/523, inspector 1/27, math 27/873, media 30/304, net 18/316, phone 2/18, platform 85/1,208, runtime 27/185, **storage 1/14**, top-level `tests/` 18/13; renderers: canvas 1/17, direct2d 1/25, directx11 1/18, directx12 2/28, directx9 1/21, easygl 4/234, fna3d 9/99, html-dom 1/60, metal 26/206, opengl4 9/98, sdl-gpu 3/54, software 2/12, svg-dom 1/100, vulkan 1/26, webgpu 2/40, common 5/12. Cross-check against BASE per-area facts the site publishes (`contribute.html:241`): the same script gives BASE storage 5, media 286, canvas 17 (reproduced); TARGET storage 14, media 304, canvas 17. Any published number must carry the caveat: static macro counts, not instantiated cases, not CTest registrations, not pass results.

### S2. Other statistics

- CI workflow files: **20** `*.yml` in `.github/workflows/` (no `*.yaml`). Versus BASE: removed `[retired]-ci.yml`, `[retired]-cross-platform-ci.yml`; added `content-pipeline-windows-ci.yml` (push to branch `content-pipeline-final` plus `workflow_dispatch`, native MSVC). Manual-only: `d3d-windows-ci.yml`, `gdi-windows-ci.yml`. The invalid `EASYGL` identity is gone from `general-tests-ci.yml` and `input-ci.yml` (repairs in the `GLTF-420` series, 2026-08-21; `RRC-004` on 2026-09-17 dropped retired-renderer jobs).
- Public C++ headers (`modules/**/include/**/*.hpp|h`): BASE 823 -> TARGET 1,081 (excluding `Internal`/`Detail` path components: 507 -> 790); production TUs (`modules/**/src/**/*.cpp|mm|c`): 696 -> 954; test-tree sources including `.c` / `.mm`: 642 -> 988 [CALC; not currently published by the site].
- Commits since alpha.1: 2,877 (2026-08-20 to 2026-09-24); first commit in repository history 2025-02-22.
- Version / CHANGELOG / tags: product `0.1.0` + prerelease `alpha.1` -> `0.1.0-alpha.1` (`CMakeLists.txt:3,12-14`, `Doxyfile:51`); `CHANGELOG.md` has an `[Unreleased]` section (Added: [retired] - later retired; native Win32 platform backend. Removed: 25 renderer identities and `SpriteBatch::DrawMeshEXT`. Changed: SDL3 not built when unused, base-instance drawing, Vulkan indirect drawing, Vulkan GPU timing. Fixed: TERMINAL+SOFTWARE presenter, `CNA_BUILD_C_API=ON` builds again) above `[0.1.0-alpha.1] - 2026-08-20`. Tags in the repo: `v0.1.0-alpha.1` (annotated, 2026-08-20) and `audit-2026-07-complete`. `docs/releasing.md` still says "Current as of 0.1.0-alpha.1" and describes only the tag + CHANGELOG process. **There is no release after alpha.1**; TARGET is an unreleased development snapshot.
- License: `LICENSE` = Microsoft Public License (Ms-PL), unchanged; `NOTICE.md` identical; `THIRD_PARTY_NOTICES.md` adds DirectXMesh (MIT; adapted file `modules/content-pipeline/src/Internal/DirectXMeshOptimizeFaces.cpp`, revision `bd17eb215d46...`, tag `oct2025`, used only by `cna_content_pipeline`) and drops the [retired]/... sections for retired renderers. Every source under `modules/ tools/ spikes/` must carry `SPDX-License-Identifier: MS-PL` unless declared in `tools/provenance/derived-sources.json` (enforced by `tools/provenance/provenance_gate.py`).

---

## Corrections to existing site claims

"Also" lists other pages carrying the same stale claim so the editor can sweep with one search.

| # | Page (line) | Old claim (short quote) | TARGET truth | Evidence |
|---|---|---|---|---|
| 1 | `docs/c-api.html` (6, 20, 26, 46) | "ABI 0.7.0"; "59 public C headers and 2,861 declared cna_* routes" | ABI **0.29.0**; **61** headers; **4,055** routes | `abi.h:34-44`; header count; declared set == `abi_baseline.json` exports |
| 2 | `docs/c-api.html` (14, 28-33, 63) | "not consumable ... 49 entries while CNA has 50 ... [retired] missing ... static_assert ... false" | The map has 25 rows == 25 canonical identities; `MAXIMUM` = 46 = highest; [retired] no longer exists as an identity (retired in ABI 0.28.0). Rewrite the blocker section as history ("alpha.1 defect, resolved after the tag"). | `CnaCApiCoreExt.cpp:195-244`; `graphics.h:16-85`; `ABI_VERSIONING.md:31-54` |
| 3 | `docs/c-api.html` (63) | "CNA_BUILD_C_API=ON with CNA_ENABLE_NET=OFF is also broken ... unconditionally includes GamerServices" | Now a deliberate configure-time `FATAL_ERROR`: "requires CNA_ENABLE_NET=ON" | `CMakeLists.txt:185-190` |
| 4 | `docs/c-api.html` (59) | "421 public C++ headers and 6,712 symbol rows: 6,317 implemented, 15 partial, 380 not applicable" | 556 headers in scope (425 excluded), **9,355** symbols: **8,363** implemented, 15 partial, **468 planned**, 509 N/A. The scope model changed (content-pipeline, phone, platform, renderers explicitly out of scope), so the numbers are not directly comparable; cite as a generated snapshot. | `COVERAGE.md:15,17-38` |
| 5 | `docs/c-api.html` (35, 43, install section) | package "intended ... not successfully consumable" | Package rules exist and are exercised by `CApi_InstalledConsumer` (Linux/ELF, local CTest only); component `CNACApi`; targets `CNA::CApi`, `CNA::CApiStatic`; RPATH `$ORIGIN`; SDL3 shipped beside the library; **not built by any CI workflow; not a release** | `modules/c-api/CMakeLists.txt:343-484,2105-2132`; workflows |
| 6 | `docs/c-api.html` (find_package snippet) | `find_package(CNA 0.7 CONFIG REQUIRED)` | The shipped example requests `0.1`; package version == ABI version, `SameMajorVersion`; request the version you wrote against | `examples/c/CMakeLists.txt:24`; `modules/c-api/CMakeLists.txt:475-479` |
| 7 | `docs/c-api.html` (release-gate paragraph) | "checked-in generated release report says ready while a workflow label says not ready" | Both say not ready: **1 unmet criterion (468 unmapped public symbols)**; nine other criteria met | `RELEASE_GATE.md:11-16,22-31` |
| 8 | `docs/c-api.html` (Important limitations) | "The declared ABI 0.7.0 is experimental" | ABI **0.29.0**, still experimental `0.x`; ABI 1.0 is a separate future decision; add the version-history table (0.8 -> 0.29) and the 0.28.0 / 0.29.0 removals | `ABI_VERSIONING.md`; `RELEASE_GATE.md:7` |
| 9 | `docs/tutorials/129-c-api-first-program.html` (meta, callout, line 142) | "Inspect ... ABI 0.7.0 ... reproduce its renderer-map compile blocker ... Do not attempt to ship the alpha.1 C library"; "59 headers / 2,861 routes / 6,317 ..." | Turn it into a real first-program tutorial around `hello_cna.c`: install `CNACApi`, `find_package(CNA 0.1 CONFIG REQUIRED)`, `target_link_libraries(... CNA::CApi)`, C99, count-then-copy, error info, children before game. Keep an "at the alpha.1 tag this did not build" note. Snippet API names verified. | `examples/c/hello_cna.c`, `examples/c/CMakeLists.txt`, `runtime.h:177-266` |
| 10 | `docs/releases.html` (131, 141) | "ABI identity: 0.7.0 at this tag ... cannot produce the final C library ... 49 vs 50"; "This edition audits changes from ae0be4b... through the resolved tag" | Add a post-alpha.1 section: product still `0.1.0-alpha.1`, **no newer tag**, TARGET is +2,877 commits; ABI 0.29.0; blocker resolved in source | `CMakeLists.txt:12`; `git describe`; `abi.h` |
| 11 | `docs/roadmap.html` (119, 223), `roadmap.html` (74, 186) | "568 C++ test sources with 8,263 ... definitions"; "21 workflow files"; "C API implementation is still compile-blocked"; "intended unfiltered general job and two Input rows still select the removed EASYGL value and fail"; "50 renderer identities across 46 families"; "covers ... except Framework.Design" | **903** files / **12,610** defs; **20** workflows; C API blocker resolved (still not CI-built); EASYGL rows fixed; 25 identities / 21 families (renderers agent); Framework.Design now implemented (opt-in) | S1, S2, C6; `.github/workflows/*.yml`; `modules/design` |
| 12 | `docs/roadmap.html` / `roadmap.html` ("The .xnb content pipeline Shipped", `roadmap.html:134`) | read-side only | Also now a **build-time Content Pipeline** (`cna-content`, XNB writer with LZX, `.contentproj`); the read-side statements stay | `tools/content/content.cpp:283-345` |
| 13 | `docs/getting-started.html` (124, 241) | "experimental C API source layer, but its final library target is compile-blocked and is not a usable getting-started path"; "568 ... 8,263" | A C path now exists (Linux, source build): point to the updated C API page and tutorial 129; counts 903 / 12,610 | C6, S1 |
| 14 | `index.html` (139, 141, 151, 399) | stats "8,263 ... 568 (539 contain macros)"; "21 CI workflow files"; "C ABI 0.7.0 ... compile-blocked by a missing [retired] identity mapping"; "exact CNA alpha.1 C library cannot be built without correcting its missing [retired] C identity" | 12,610 / 903 (871 contain macros); 20 workflows (workflow files, not passing lanes); ABI 0.29.0, blocker fixed after alpha.1; the hover-title text must change; the binding paragraph should say bindings pin ABI minors independently | S1, S2, C1, C6 |
| 15 | `features.html` (7, 12, 68, 151, 492, 499) | meta "compile-blocked C API source surface"; "CNA does not author XNB files"; "568 ... 8,263"; "21 workflow files ... EASYGL ... C API final implementation blocked" | ABI 0.29.0 source layer with consumer package; **`cna-content` authors CNB and XNB**; 903 / 12,610; 20 workflows, EASYGL fixed, C API gates build-free; new sections: Diagnostics, Inspector | O2, S1, S2 |
| 16 | `about.html` (68, 73, 136) | "21 workflow files ... final C API target is compile-blocked"; "568 C++ test files and 8,263"; "Storage ... one source and five definitions" | 20 workflows; 903 / 12,610; storage 1 source / **14** definitions; CNAEXT/DEVICES statements unchanged | S1, S2 |
| 17 | `architecture.html` (111, tree at 296-340) | "50 public identities ... newer [retired] and [retired]"; tree omits `c-api`, `content-pipeline`, `design`, `diagnostics`, `inspector`, `phone`, `video-ffmpeg`; `tools/ gltf_to_cnj, xna-oracle`; `renderers/ 46 families, 50 public identities` with [retired]..12 / [retired] | 25 identities / 21 families; add the six new modules plus `c-api`; the tools list gains `content`, `cnb_info`, `source_to_cnb`, `cnj_to_cnb`, `gltf_to_cnb`, `provenance`; `cmake/` gains tool/gate files | O1, O2, `docs/physical-modules.md` |
| 18 | `documentation.html` (94, 118-119, card list) | card: "ABI 0.7.0 source surface, ... 49-versus-50 renderer-map compile blocker"; no Diagnostics / Inspector / Tools / Content Pipeline cards | Update the C API card; add cards for the new pages (section "Proposed new pages") | C1, C6 |
| 19 | `docs/verification.html` (138, 174-175, 270-281) | "568 ... 8,263"; "21 workflow files ... intended unfiltered general job and two Input matrix rows ... EASYGL"; Native C API row: "An isolated tag build reproduced the final implementation failure ... With networking off it fails earlier" | 903 / 871 / 12,610 with the same method wording; 20 workflows; EASYGL rows fixed; Native C API row: five build-free gates, no CI build, local `CApi_*` CTest, release gate "Not ready (468 unmapped)" | S1, S2, C5 |
| 20 | `contribute.html` (96, 124, 211, 241) | "568 ... 8,263"; "21 workflow files ... C API's final target ... compile-blocked"; "Storage has only five ... Media 286, Canvas 17" | 903 / 12,610; 20 workflows; storage 14, media 304, canvas 17; new contributor entry points: Diagnostics/Inspector, the C API backlog (468 planned rows), `cna-content` | S1, S2 |
| 21 | `docs/building.html` (332, 389) | `CNA_BUILD_C_API`: "compile-blocked by a 49-entry C renderer map ... NET=OFF instead fails earlier"; "cannot compile the final implementation" | Requires `CNA_ENABLE_NET=ON` (configure error otherwise), C17 implementation / C99 consumer; static archive option `CNA_C_API_BUILD_STATIC`; add rows for `CNA_DIAGNOSTICS`, `CNA_BUILD_INSPECTOR`, `CNA_BUILD_BENCHMARKS`, `CNA_ENABLE_VIDEO`, `CNA_ENABLE_FONT_PIPELINE`, `CNA_ENABLE_MEDIA_PIPELINE`, `CNA_SHARED_LIBRARY`; the C++ framework still has no install rules (unchanged) | C4, O1 |
| 22 | `showcase.html` (104, 143), `docs/faq.html` (277), `docs/tutorials/72-backend-selection.html` (340), `100-shipping.html` (150), `85-vulkan-backend.html` (149), `02-setup.html` (283), `80-cross-platform.html` (161), `125-pixel-testing.html` (297), `docs/vs-alternatives.html` (104, 174, 216) | "C API final target is compile-blocked" / "21 workflow files" / "568 ... 8,263" / "28 demo programs under examples/" / "except Framework.Design" | Same fixes as rows 11-16; "28 demo programs" -> the 28 `cna_demo_*` still exist but live in module example trees, not `examples/`; Framework.Design implemented | O3, C6 |
| 23 | `docs/xna-compatibility.html` (142, 395, 429), `docs/faq.html` (137), `tutorials/01-introduction.html` (112), `84-migrate-xna.html` (112) | "the only XNA 4.0 namespace CNA does not cover: Framework.Design ... no C++ equivalent" | `Microsoft::Xna::Framework::Design` is implemented as opt-in `CNA::Design` (13 `TypeConverter`s over the sharp-runtime ComponentModel). The Windows Forms designer host itself is still absent; only the converter surface exists. | `modules/design/include/.../Design/*.hpp`; `docs/framework-design.md:1-30` [DOC] |
| 24 | `docs/content-pipeline-xnb.html` (134), `features.html` (151), `index.html` / `about.html` ("real .xnb content pipeline"), tutorials 35 / 110 / 111 etc. | "CNA does not author XNB" / read-side only | `cna-content --format xnb` writes XNB; `--xnb-compress lzx` matches XNA 4.0's compression; only the read-side statements about the runtime `ContentManager` remain true | `tools/content/content.cpp:283-333` |
| 25 | `docs/video-playback.html` (FFmpeg section, about line 315) | FFmpeg "located through pkg-config at configure time"; no switch | New tri-state `CNA_ENABLE_VIDEO` (OFF/AUTO/ON); the backend is module `video-ffmpeg`; OFF builds have no FFmpeg link edge and file-backed video throws `NotSupportedException` | `CMakeLists.txt:192-200`; `modules/video-ffmpeg/CMakeLists.txt` |

---

## Proposed new pages with outlines

(Every bullet has a verified source above; where a claim is CNA-documented only it is marked.)

### P1. `docs/diagnostics.html` - Diagnostics and Profiler (new)
1. What it is / is not: in-process, std-only, no thread, no C ABI, not the Inspector (`Diagnostics.hpp:1-11`).
2. Modes table (OFF / STATS / FULL): what each retains, cost model, the `CNA_DIAGNOSTICS` option, the public `CNA_DIAGNOSTICS_LEVEL` define, runtime lowering with `SetRuntimeMode`, generation invalidation of open zones (`CMakeLists.txt:153-171`, `Diagnostics.cpp:1323-1345`).
3. Instrumentation macros and handles; the "arguments are not evaluated when compiled out" callout; naming convention (stable slash-separated literals) (`Instrumentation.hpp`).
4. Built-in metrics table (12 counters/gauges plus 3 zones) with kind and accuracy caveats (SpriteBatch does not go through draw calls; indirect draws contribute 0 primitives) (`Game.cpp`, `GraphicsDevice.cpp:68-84`).
5. Resource metadata and memory scope: kinds, exact vs estimated bytes, `registeredResourceBytes` is a mixed aggregate, no GPU readback (`DiagnosticResource.hpp`, `Diagnostics.hpp:403-430`).
6. Pull provider and sources: `IDiagnosticsProvider` v1, cursor reads, drops/overwrites, `IDiagnosticsSource` contract (never wait on the GPU); note nothing in the tree registers a source yet.
7. Recording and export: `StartRecording` / `StopRecording`, CNATRACE v1 layout, Chrome trace export; reader safety limits.
8. Limits table (512 metrics, 64 frame metrics, zone depth 64, 1,024 per-thread events, 32,768 history, 240 frames).
9. Overhead: code-derived facts plus CNA's benchmark record labelled as measured by CNA on one machine; how to run `cna_diagnostics_benchmark` (`-DCNA_BUILD_BENCHMARKS=ON`).
10. Recipe (configure, instrument, read, record, export) and known limitations (no GPU timers, no input metrics, no process-memory measurement, no C ABI, not covered by CI).
Cross-links: Inspector, Building (options), Verification (tests: 40 + 6 + 1 definitions).

### P2. `docs/inspector.html` - CNA Inspector (new)
1. Purpose and non-goals (view-only; not an editor, debugger or remote administration tool).
2. Architecture diagram: game process (`IDiagnosticsProvider` -> `Agent` thread) <-> authenticated TCP <-> `cna-inspector` bridge (127.0.0.1 HTTP) <-> browser. Why the split (a browser refresh or crash never touches the game).
3. Build and activation: `CNA_BUILD_INSPECTOR`, required `CNA_DIAGNOSTICS`, link line, `Agent::Start`, `AgentConfiguration` table with defaults, no env/auto-start. Platform matrix (desktop only; configure error on Web/Android/iOS).
4. Run it: the demo (`cna_inspector_demo --port/--seconds`), bridge flags table, `CNA_INSPECTOR_TOKEN` / `--token-file`, the printed URL.
5. Security model: loopback default, `allowRemote`, 256-bit token, UI-token header, Host check, CSP, plaintext-protocol warning, request-rate cap, backlog 4, timeouts, 32-connection cap; what it does NOT expose.
6. UI tour: the eight views and what each reads; discontinuity banner semantics; `—` for unpublished metrics.
7. Wire protocol v1 reference (header, message types, capability bits, limits) for tool authors; the `Client` API for custom front ends.
8. Previews: seam only, off by default, no renderer installs a provider yet; bounds.
9. Performance record (CNA-measured, labelled) and how to reproduce (`cna_inspector_benchmark`).
10. Troubleshooting table (target missing, no events in STATS, connection refused, authentication failed, reconnecting).
11. Status: 27 tests; no CI lane; native Windows validated per CNA notes, macOS not.

### P3. `docs/tools.html` - Command-line tools reference (new; no home today)
`cna-content` (build/clean, options, `--format cnb|xnb`, `.contentproj`, `cna_add_content()`), `cna_tool_cnb_info`, `cna_tool_source_to_cnb`, `cna_tool_cnj_to_cnb`, `cna_tool_gltf_to_cnb`, `cna_tool_gltf_to_cnj`, `cna_tool_xnb_interop_fixtures`, `cna-inspector`, plus the developer gates (`scripts/check_*`, `tools/c-api/*`, `tools/provenance/provenance_gate.py`). Each row: purpose, target name, build condition, example.

### P4. `docs/content-pipeline.html` - Build-time Content Pipeline (new; complements the read-side `docs/content-pipeline-xnb.html`)
Importer -> Processor -> Writer; `cna-content`; CNB vs XNB outputs; LZX; `.contentproj`; incremental manifest; `CNA_ENABLE_FONT_PIPELINE` / `CNA_ENABLE_MEDIA_PIPELINE`; module boundary (`content-pipeline` is never linked into games); custom-compiler examples; Windows CI lane. The owner of this page should be the content agent; details from `docs/content-pipeline.md` are [DOC].

### P5. Rewrite `docs/c-api.html` and tutorial 129; add `docs/c-api-versioning.html` (or a section)
- Status banner: experimental, ABI 0.29.0, not a release, no CI build, gate "Not ready".
- Build/consume: options, the `CNACApi` install component, `find_package(CNA 0.1 CONFIG)`, `CNA::CApi` / `CNA::CApiStatic`, non-CMake command line, Linux-only verification, SDL3 shipped, FFmpeg optional.
- Conventions: results, handles, ownership, threading, strings, structs (with verified `hello_cna` excerpts).
- ABI policy and version-history table (0.7 -> 0.29), reserved renderer values, symbol version node, baseline/gates.
- Coverage snapshot and limitations (9,355 / 8,363 / 15 / 468 / 509) with the "generated snapshot, scope model changed" caveat.
- WebAssembly artifact section (target, files, BigInt rule).
- Bindings boundary (CNA publishes the ABI only; named consumers).

### P6. Smaller additions (no new page needed)
- `docs/xna-compatibility.html`: replace the Framework.Design exclusion by an "Opt-in Design module" section (13 converters, registration, link `CNA::Design`); add a `Microsoft.Phone` note (a lifecycle/push module `CNA::Phone` outside XNA 4.0).
- `docs/building.html`: the option rows listed in correction 21.
- `docs/video-playback.html`: a `CNA_ENABLE_VIDEO` section.
- Tutorials (optional): "Profile a frame with Diagnostics", "Watch a running game in the Inspector", "Compile content with cna-content".

---

## Open questions

1. **Framing of the target**: TARGET is +2,877 commits after `v0.1.0-alpha.1`, still stamped `0.1.0-alpha.1`, with no new tag. The site claims to document "the immutable v0.1.0-alpha.1 tag" (`index.html:151`, `docs/releases.html:141`). The owner must decide how to label a development snapshot (for example "development snapshot `009d40f`") without inventing a release.
2. **Compile status is inferred, not measured**: confidence and gaps are in section C6. The definitive check, if the owner permits it, is one out-of-source build of `-DCNA_BUILD_C_API=ON` in the shared `build/` directory plus `ctest -R '^CApi'`; I was forbidden to run it.
3. **CNA documentation inconsistencies to avoid propagating**: `docs/c-api/README.md` says "public C17 headers" (the matrix says C99 floor); `RELEASE_GATE.md` prose still cites 654 Content Pipeline declarations under open `CBIND-117` while `COVERAGE.md` treats that scope as excluded by owner decision; `ABI_VERSIONING.md` 0.9.0 text names [retired] among ContentLost renderers although [retired] is retired; `CHANGELOG.md` `[Unreleased]` omits Diagnostics / Inspector / Design / Content Pipeline / Phone and the ABI 0.8-0.25 growth; `plans/plan_bindings_upstream.md` says "ten bindings" but names nine plus templates; `docs/inspector.md` uses a non-standard `build-inspector` directory in its examples (use `build`).
4. **Performance numbers** (Diagnostics about 1.6 ns / 64 ns; Inspector about 71 / 121 us) come from CNA's Markdown for one Ryzen machine and are not reproducible here. Publish only with the machine qualifier, or not at all.
5. **Inspector validation claims** (native MSVC run, Chrome end-to-end on Linux) are recorded in `docs/inspector.md` and `plans/plan_diagnostics_inspector_audit.md`, but no CI workflow covers Diagnostics/Inspector; macOS is documented as untested.
6. **Which ABI version each binding expects today** is not published by CNA (only historical pins 0.6-0.9 in plans). The site should not state a binding/ABI pairing.
7. **Phone module**: `HttpNotificationChannel` runs a local listener thread (`modules/phone/src/HttpNotificationChannel.cpp`); I did not audit its platform coverage (Windows / Linux / macOS / Emscripten). Describe it conservatively.
8. **Design module completeness**: `docs/framework-design.md` claims the complete public namespace; I verified the 13 class declarations, the registration code and 25 tests exist, but did not audit converter behaviour against XNA.
9. **Renderer counts** (25 identities / 21 families) and all renderer/capability claims belong to another agent; I rely on them only for the C-map consistency argument.
10. **`CNA_SHARED_LIBRARY` default ON** (Linux) is a consumer-visible change (`libcna.so`); the Building/Platforms owner should confirm the wording.
