# R3 — C ABI 0.44.0 → 0.46.0, the C API on macOS, and CNA.NET (cna-dotnet) on macOS, at CNA `c1c316b9`

Internal audit record (not served). Research only; nothing was built or run for this sheet.
TARGET = CNA `c1c316b9c7a846ce8002809c151fcd1af14942c9` (2026-10-09). BASE = `b0e97bb1bb876f9b3edd6f4ff1ef3067908ae8ac` (2026-10-04).
Evidence tags as in `R2-apple-m4.md` (M4-LOCAL, M4-LOCKED, SIM, BUILD-ONLY, CI-HOSTED, TEST-SUITE, SOURCE, DOC).

> **Public-content warning.** §1 names the four renderer constants retired in 0.45.0 because this is an internal audit record. Those
> names must never appear on a public page, not even as "removed". Public wording: "0.45.0 retired four renderer identity constants;
> their integer values stay permanently reserved" — or simply describe 0.46.0 as current.

---

## 1. C ABI version history in the delta (SOURCE)

`git log b0e97bb1..c1c316b9 -- modules/c-api/include/CNA/C/abi.h tools/c-api/abi_baseline.json`:

| Version | Commit | Date | Change | Compatibility |
|---|---|---|---|---|
| **0.44.0** (BASE) | `ed885a8ae` (CBIND-155) | 2026-10-03 | Activation/deactivation handlers run inside a callback scope and may borrow the device. No route/constant/struct change. | — |
| **0.45.0** | `1cac65958` (RRC-018) | 2026-10-07 | Retires four public renderer identities with their four `CNA_GRAPHICS_RENDERER_*` constants (internal: `OPENGLES2`=2, `WEBGL1`=5, `DIRECTX12`=15, `CANVAS`=17). Values permanently reserved; `CNA_GRAPHICS_RENDERER_MAXIMUM` stays 43 (`FNA3D`); next new value stays 52; **3,210 exports unchanged**; no route, structure, field, capability bit or exported symbol changes; no surviving identity renumbered. | **Source-breaking for a binding that names one of the four constants** (no longer compiles) and **behaviour-breaking for one that passes their integers** (every route refuses with `CNA_RESULT_INVALID_ARGUMENT`) — `docs/c-api/ABI_VERSIONING.md` "Previous ABI 0.45.0". Pre-1.0 experimental ABI: minor bumps may break. |
| **0.46.0** (TARGET) | `b0390cbbc` (AM4-037) | 2026-10-07 | Appends `CNA_NATIVE_WINDOW_SYSTEM_UIKIT` = **9** (`runtime_window.h`); on iOS/iPadOS `cna_game_window_get_native_window_ext` reports SDL's `uikit` window with `CNA_NativeWindowHandle::window` = `UIWindow*` (previously `CNA_NATIVE_WINDOW_SYSTEM_HEADLESS` with null pointers). `CNA_NATIVE_WINDOW_SYSTEM_MAXIMUM` 8 → 9. "every existing value keeps its number and no route, structure or exported symbol changes. The minor increments because the closed enumerable range changed, so a binding can require the first ABI that can report a UIKit window." (`ABI_VERSIONING.md` "ABI identity") | **Additive** (new constant; widened closed range). A binding that validates the native-window-system enum against a hard-coded maximum must accept 9. |

Measured baseline (`tools/c-api/abi_baseline.json`, counted at both revisions):

| Key | BASE `b0e97bb1` | TARGET `c1c316b9` |
|---|---|---|
| `abi_version.minor` / encoded | 44 / 11264 | **46 / 11776** |
| exports | 3,210 | **3,210** |
| integer constants | 1,466 | **1,463** (−4 renderer constants, +1 UIKit) |
| structs | 197 | 197 |
| scalars | 295 | 295 |
| strings / colors | 14 / 141 | 14 / 141 |

`abi.h` at TARGET: `CNA_ABI_VERSION_MAJOR 0`, `MINOR 46`, `PATCH 0`, comment "experimental" (`modules/c-api/include/CNA/C/abi.h:34-44`).

Documentation state at TARGET:
- `docs/c-api/ABI_VERSIONING.md` describes 0.46.0 as current, 0.45.0 and 0.44.0 as previous (DOC, consistent with SOURCE).
- `docs/c-api/RELEASE_GATE.md`: "CNA C ABI 0.46.0, experimental"; verdict **Not ready**, 1 criterion unmet ("631 public symbols are still unmapped"); "197 struct layouts and 3210 exported symbols recorded"; packaging criterion names `libcna_c_api.dylib` with `LC_RPATH @loader_path` (DOC; regenerated with Doxygen 1.9.8, AM4-160/AM4-210).
- `docs/c-api/COVERAGE.md`: 469 headers, 8,142 symbols, 7,053 implemented, 15 partial, 631 planned, 443 N/A; 451 excluded headers (DOC).
- **Gate numbers moved in the delta** (BASE → TARGET, `RELEASE_GATE.md`/`COVERAGE.md`): unmapped ("planned") public symbols **656 → 631**; implemented 7,030 → 7,053;
  not applicable 441 → 443; explicitly excluded headers 471 → 451; partial 15 → 15; LIMITATIONS "15 partially mapped symbols in 9 groups, 443 unmapped in 86 groups"
  (BASE: 441 in 86 groups); "23 declared cells across 7 toolchains" and "197 struct layouts and 3210 exported symbols" unchanged. Touching commits: `1cac65958`
  (RRC-018), `bf410474b` (RRC-024), `0fc33dac1` (RRC-028), `64c5e28f0` (AM4-160), `46538cc17` (AM4-210), `a3da0a5bb` (AM4-214). Site pages quoting "656 unmapped"
  / "441 no C form" / "0.44.0" are therefore stale.
- **`CHANGELOG.md` has a 0.45.0 entry (renderer retirement) but no 0.46.0/UIKit entry** — CNA-internal omission; do not infer anything from it.
- Site wording should therefore be: "C ABI 0.46.0 (experimental)"; "3,210 exported `cna_*` routes".

---

## 2. The C API on macOS (Phase 5, AM4-072..075, 122, 160, 164, 197, 198, 206, 209..214)

Host: physical Mac mini M4 (see R2 §1). All rows **M4-LOCAL, TEST-SUITE** unless stated. CNA commits verified in the CNA clone.

| Task / commit | Fact | Evidence |
|---|---|---|
| AM4-072 | "The C API had never been built on macOS." Library and headers compiled; 41 pure-C smoke suites needed C11 `<threads.h>`, absent from Apple's C library → `tests/pure_c/CnaTestThreads.h` maps the used subset onto POSIX threads. First macOS `ctest -R ^CApi`: 102/115. | M4-LOCAL |
| AM4-073 | Teardown at process exit crashed (destroyed function-local statics; Darwin `EINVAL`); three statics made immortal; all 7 teardown modes pass. | M4-LOCAL |
| AM4-074, AM4-122 | Apple main-thread rule: a windowed renderer created off the main thread is refused with a message naming the main thread; SOFTWARE runs on SDL's offscreen driver without a window; exit from another thread with the game alive still supported. | M4-LOCAL |
| AM4-075, 164, 197, 198, 206 | C smokes made portable (libc++ type-name length, `CFFIXED_USER_HOME` for media folders, capability-aware clears/cubes, SDL backend blend refusal → `NOT_SUPPORTED`). | M4-LOCAL |
| AM4-160 | `CApiCoverageMatrix`/`CApiLimitations`/`CApiReleaseGate` pin Doxygen 1.9.x; with Homebrew's 1.18 they now **skip** (exit 77, named `UnpinnedDoxygen`); with `CNA_C_API_DOXYGEN` = 1.9.8 they pass. `COVERAGE.md`/`RELEASE_GATE.md` regenerated (ABI 0.46.0). | M4-LOCAL |
| **AM4-209** `96d25fe65` | Before: `libcna_c_api.dylib` exported **21,904** symbols, 3,210 of them `_cna_*`. Now ld64 `-exported_symbols_list cmake/CnaCApiExports.darwin.txt` (`_cna_*`), `LINK_DEPENDS`, `CApi_Exports` registered on Apple via `cmake/CheckMachOExports.cmake` (`nm -gU`). Result: **exactly 3,210 symbols, all `_cna_*`** (the count `abi_baseline.json` pins); every C API test 116/116 in SOFTWARE and SDL_RENDERER trees. | M4-LOCAL |
| **AM4-210** `46538cc17` | Installed library: `INSTALL_RPATH "@loader_path"` (was ELF `$ORIGIN`, written literally by ld64), install name `@rpath/libcna_c_api.dylib`, **Mach-O compatibility version `MAJOR.MINOR.0` and current version `MAJOR.MINOR.PATCH` = 0.46.0** (dyld refuses an older minor than linked), `CNACApi` component installs `libSDL3`, `libSDL3_image`, `libSDL3_mixer` dylibs beside it. `check_release_gate.py` requires the dylib pattern + `@loader_path`. Example built against the prefix with `find_package(CNA)` runs with **no `DYLD_*` variable**. Homebrew FFmpeg/curl/opus/zstd stay system dependencies. | M4-LOCAL |
| **AM4-211** `784a2dae5` | `CApi_InstalledConsumer` (install `CNACApi` into a stage, configure `modules/c-api/examples/c` with only `CMAKE_PREFIX_PATH`, build, run) now registered on Darwin; asserts `LC_RPATH @loader_path` and `libSDL3.0.dylib` in the stage via `otool -l`. Passes in the SOFTWARE tree (runs `hello_cna`). | M4-LOCAL |
| **AM4-212** `25338a450` | `generate_abi_baseline.py`, `check_declared_exports.py`, `generate_artifact_manifest.py` decide by file magic; Mach-O exports via `nm -gU` (underscore dropped), build ID = `LC_UUID`. "declared and exported agree exactly: **3210 routes**"; baseline current on arm64 macOS (**197 structs, 295 scalar types, 1,463 constants, 3,210 exports**: "the layouts pinned on Linux hold here"). `CApiAbiBaseline`, `CApiDeclaredExports`, `CApiAbiHeaderBaseline`, `CApi_Exports`, `CApiReleaseGate` pass (SOFTWARE); first two also in SDL_RENDERER. | M4-LOCAL |
| **AM4-213** `97bf4540c` | Static `CNA::CApiStatic` on macOS: `ld -r -all_load` (with the dylib's `-arch`) + **`nmedit -s`** localization; survivors must be exactly `_cna_*` (Mach-O has no `STB_GNU_UNIQUE`); frameworks/dylibs/SDK text stubs become the imported target's interface (`libcurl.tbd` → `curl`; C++ runtime `c++`). `libcna_c_api_static.a` (162 MB Debug): "3210 exported cna_* symbols, 32 archives combined". `CApi_InstalledConsumer` builds and runs `hello_cna` **and** `hello_cna_static` from the installed package in both trees; every C API test **119/119** in SOFTWARE and in SDL_RENDERER. | M4-LOCAL |
| **AM4-214** `a3da0a5bb` | Docs: `CONSUMING.md` gains a macOS section (install name, ABI-derived dylib versions, exported-symbols list, `@loader_path`, ld64/`nmedit` static archive, external libs: libcurl/FFmpeg/Opus/zstd with `brew install curl ffmpeg opus zstd`, deployment-target caveat, main-thread rule, `SDL_VIDEODRIVER=dummy` headless, no EGL `offscreen`); `compatibility_matrix.json` → `COMPATIBILITY.md`/`LIMITATIONS.md`: the old "macOS, iOS, Android and the web targets. **No toolchain for any of them is present**" is replaced by a macOS entry ("not a cell of this matrix ... measured separately on Apple silicon (AM4-209..213): every C API test passes in the SOFTWARE and SDL_RENDERER configurations ... CApi_InstalledConsumer builds and runs the installed package, shared and static") and an "iOS, Android and the web targets" entry that keeps "No toolchain ... iOS builds of CNA itself exist; the C ABI is not exercised on them"; `CALLBACKS_AND_THREADING.md` states the Apple main-thread rule; `apple-platforms.md` C API row → PASS. | DOC |

Matrix row (`docs/apple-platforms.md:218`): **C API — PASS** — "every C API test, 119/119, in the SOFTWARE and `SDL_RENDERER` trees, the documentation gates
with Doxygen 1.9.8 through `CNA_C_API_DOXYGEN`; `CApi_InstalledConsumer` installs the package and builds and runs `hello_cna` against it, shared and static
... **No CI job builds the C API on macOS yet**".

Boundaries of the C API macOS claim:
- Configurations measured: **SOFTWARE and SDL_RENDERER** trees only (the C API under METAL was exercised indirectly by the CNA.NET work, which linked a METAL Release C API, AM4-215/228/229).
- arm64 only (Apple silicon); no Intel run. No CI. Not exercised on iOS.
- System libraries: libcurl (SDK libcurl → relay refused by name), FFmpeg (raises the deployment floor if Homebrew's), Opus, zstd are not packaged.
- The C ABI release gate is still "Not ready" (unmapped C++ symbols) — unrelated to macOS.

---

## 3. CNA.NET (repository `libcna/cna-dotnet`) on macOS

### 3.1 The rename (SOURCE, local clone)

- The C#/.NET binding repositories are now **`libcna/cna-dotnet`**, **`libcna/cna-dotnet-template`**, **`libcna/cna-dotnet-samples`** (local clones' `origin` remotes:
  `git@github-libcna:libcna/cna-dotnet`, `.../cna-dotnet-template`, `.../cna-dotnet-samples`).
- Local cna-dotnet `develop` head `8947b91` (2026-10-06) "chore: complete cna-dotnet rename" rewrote `cna-cs-template` → `cna-dotnet-template`,
  `CnaCsRoot`/`CNA_CS_ROOT` → `CnaDotnetRoot`/`CNA_DOTNET_ROOT` (docs/packaging.md), workflow and test references. The product name stays **CNA.NET**.
- The libcna.com baseline facts (`audit/data/facts/b0e97bb1/R4-cna-net.md`) still call the repos `cna-cs`, `cna-cs-template`, `cna-cs-samples`; the public site
  has **98** such occurrences (62 `cna-cs`, 23 `cna-cs-samples`, 12 `cna-cs-template`, 1 `cna-cs-native-abi`) and **0** `cna-dotnet` (see worklist §W-NET).
  Note: the binding's ABI policy identifier was `cna-cs-native-abi/1` pre-rename (local README); whether it was renamed is **not established** (post-campaign
  cna-dotnet commits are not present locally) — do not invent a new identifier.
- `CNA_CS_ROOT` / `CnaCsRoot` on site pages → `CNA_DOTNET_ROOT` / `CnaDotnetRoot` (per `8947b91`'s docs/packaging.md diff).

### 3.2 macOS campaign tasks (sibling SHAs as recorded by `plan_apple_m4.md`; **not present in the local clones**)

| Task | Repo / recorded SHA | Fact | Evidence |
|---|---|---|---|
| AM4-215 | (environment) | .NET SDK **8.0.425 osx-arm64**, user-local, SHA-512 checked. Native libraries: CNA `a3da0a5bb` **Release C API with `CNA_DEVICES=ON`** in three trees — SOFTWARE (`CNA_SOFTWARE_COMPILED_EFFECTS=ON`), **METAL (`CNA_METAL_COMPILED_EFFECTS=ON`)**, SDL_RENDERER — each installed with `--component CNACApi`. Side effect left for the owner: an ASP.NET Core HTTPS dev certificate in the login keychain. | M4-LOCAL |
| AM4-216 | cna-dotnet `4867008` | Native ABI fixture gate runs on macOS (`.dylib` fixtures); fixture inventory regenerated (three `cna_message_box_*_ext` imports). 1,419 required symbols. | M4-LOCAL |
| **AM4-217** | cna-dotnet `8219a6c` | **Admits C ABI 0.46.0.** `baselinediff.py` 0.44.0 (`ed885a8ae`) → 0.46.0 (`a3da0a5bb`): **1,419 consumed exports, 0 absent, 0 changed prototypes, no struct/scalar/string difference; five integer-constant differences reviewed** in `eng/cna-upstream-abi-allowlist.txt` (four retired renderer constants, `CNA_NATIVE_WINDOW_SYSTEM_MAXIMUM` 8 → 9). Policy, consumer constant, ABI tests, fixtures (13), CI pins and docs moved to 0.46.0; **0.45.0 never admitted**. Fixture gate 2 accepted / 11 rejected; the macOS dylib passes the runtime contract. | M4-LOCAL (compatibility review + gate) |
| AM4-218 | `ef4b7fc` | Case-insensitive APFS: content-path tests measure the filesystem; Framework **652 pass, 3 skip, 0 fail**. | M4-LOCAL |
| AM4-219 | `45a2d31` | Isolated-storage tests isolated with `CFFIXED_USER_HOME` via `setenv`; BrowserCompat 5/5. | M4-LOCAL |
| AM4-220 | `8ecd284` | ARM64 NaN sign accepted in the math corpus; XnaCompat **319/319**. | M4-LOCAL |
| AM4-221 | `bdbd49f` | Mach-O in resolver diagnostics, coverage sweep (3,210 exports, 0 absent), Interop acceptance pack globs `libSDL3*.0.dylib`. | M4-LOCAL |
| AM4-222 | `2dfa388`, `114f974` | Effect tests: SOFTWARE/HEADLESS do not inspect shader source. | M4-LOCAL |
| AM4-223 | `a85b02f` | Windows Forms handle test windowless branch (dummy driver → handle 0). | M4-LOCAL |
| AM4-224 | `8fe5a14` | No-display test: CPU renderers may construct; Integration 260/260 at the time. | M4-LOCAL |
| AM4-225 | `f99f4db` | Snapshot capture portable to bash 3.2/BSD; open (not macOS-specific): full graphics capture stops on a Reach refusal (SOFTWARE-212). | M4-LOCAL |
| **AM4-226** | cna-dotnet-template `8f439e0`, `e489f2a` | `verify-template.sh` portable (grep, dummy driver on Darwin); **development and package modes pass; the smoke test draws 60 frames**. | M4-LOCAL |
| **AM4-227** | cna-dotnet `80082b3` | `Package-Acceptance.sh` per-host (RID, suffix, SDL names, `otool` `LC_RPATH @loader_path`, dummy driver, `-arch x86_64` wrong-arch fixture). **`PACKAGE_ACCEPTANCE_STATUS=passed`** — three packages with `runtimes/osx-arm64/native`, isolated restore/build, **60 and 600 frames from the packaged native with no environment**, every diagnostic case, template development and package modes. | M4-LOCAL |
| **AM4-228** | cna-dotnet-samples `eadd50a`, `1dc7283`, `f3c2b0a` | Scripts portable to Darwin (`.dylib`, BSD `stat`, default SOFTWARE, `CNA_BUILD_ROOT`, dummy driver unless `SDL_VIDEODRIVER` asks; METAL needs `cocoa`). **Solution builds (122 projects, 0 errors); all 84 samples with a project start, load content and are running at a 15 s alarm on SOFTWARE with compiled effects (dummy driver) and on METAL with compiled effects (Cocoa windows, locked console); no log carries an exception or refusal. Yacht has no project.** | M4-LOCKED (smoke-run: start/load/run-to-alarm; not a per-sample pixel check) |
| **AM4-229** | cna-dotnet `f1429db`, `1931560` | README, `docs/packaging.md`, `eng/platform-matrix.json` now record the measured **osx-arm64** state "as **local evidence, not a shipping claim (no CI leg, signing or notarization)**": Debug and Release builds; Framework 652+3 skip, XnaCompat 319, BrowserCompat 5, Integration, GamerServices/Avatar/Net 24, ownership stress 100 cycles; `tools/abi-verify` 0 mismatches (1,137 layout values, 1,419 prototypes, 23 callbacks, 604 constants, 12/12 negative controls rejected); fixture gate 2/11; package acceptance; **on METAL a main-thread C# game with exact pixel readback**, the template and the 84 samples. | M4-LOCAL (+ PIXEL for the one main-thread METAL game) |
| AM4-230 | cna-dotnet-template `ec446e7` | `#if ENGINE_CNA` stripped by `dotnet new` (platform-independent PRODUCT bug) — fixed; a fresh `dotnet new cna-game` reports `METAL`, 3D and depth on the METAL library and draws 60/600 frames; SDL_RENDERER reports "2D only". | M4-LOCAL |
| AM4-231 | cna-dotnet `bd0c28f` | `Clear(Color)` on a back buffer without a depth plane (platform-independent PRODUCT) — fixed; Integration **261/261 on SOFTWARE**, Debug and Release, and under `DOTNET_GCgen0size=0x10000`. **Open: the SDL_RENDERER Integration suite still fails 239/261**; "the binding qualifies on SOFTWARE and METAL". | M4-LOCAL |
| AM4-256 | cna-dotnet `88d0c48` | Behaviour-corpus document regenerated (CI drift). | CI-HOSTED |
| AM4-257 | cna-dotnet `f58c1d0` | Leak-only verifier restores `CNA.XnaCompat` first (CI). | CI-HOSTED |
| AM4-262 | cna-dotnet `d6cd724` | CI checks out the same-named cna-dotnet-template branch when present. | CI-HOSTED |
| **AM4-288** | cna-dotnet `68e7c9c` | In run 37919294778 every job was green except `portable-abi-header (macos-13, osx-x64)`, queued forever (macos-13 image retired 2025-12-04); the **osx-x64 row moves to `macos-15-intel`**. CNA commit title (`dd6e52f05`): "record cna-dotnet's osx-x64 ABI header built on the Intel image that still exists". This is an **ABI-header** CI job, not an osx-x64 runtime run. | CI-HOSTED |

### 3.3 What ran, what did not

- **Ran (local, physical Mac mini M4, osx-arm64):** builds (Debug/Release); managed suites (Framework, XnaCompat, BrowserCompat, Integration on SOFTWARE, GamerServices/Avatar/Net 24, ownership stress); ABI verification against the 0.46.0 dylib; package acceptance; template (development + package mode; METAL game 60/600 frames); 84 samples smoke-run on SOFTWARE and on METAL; one main-thread C# game with exact pixel readback on METAL.
- **Renderers the binding is said to qualify on (macOS):** SOFTWARE and METAL (AM4-231). SDL_RENDERER: Integration 239/261, open.
- **Did not run / not claimed:** any CI runtime leg on macOS (only the osx-x64 ABI-header job); signing or notarization; osx-x64 runtime (no Intel Mac); **Windows** (no CNA.NET Windows run is recorded in this campaign; the pre-campaign local `eng/platform-matrix.json` lists `win-x64`/`win-arm64` as "pending ... runner", and the campaign only changed the osx-arm64 row per AM4-229 — post-campaign file not present locally); iOS (not part of the binding work); per-sample pixel verification of the 84 samples.
- **ABI:** CNA.NET's reviewed matrix admits **0.46.0** (0.44.0 → 0.46.0, 0.45.0 skipped). A site statement "CNA.NET targets C ABI 0.44.0" is stale.

---

## 4. Claims that must NOT be made (C API / CNA.NET)

- "The C API ships for macOS" in a release/CI sense — it is a local, measured package build; **no CI job builds it on macOS**.
- "C API tested under every renderer on macOS" — SOFTWARE and SDL_RENDERER trees (plus the METAL Release C API used by CNA.NET).
- "C ABI 0.46.0 is stable/1.0" — experimental; release gate "Not ready".
- "0.45.0/0.46.0 are fully backward compatible" — 0.45.0 removed four constants (source-breaking for bindings naming them); 0.46.0 is additive.
- Naming the four retired renderer constants on a public page.
- "CNA.NET supports macOS" as a shipping/product claim — say "measured locally on a physical Mac mini M4 (osx-arm64); not a shipping claim: no CI leg, signing or notarization".
- "CNA.NET runs on Windows/Intel Mac/iOS" — not established by this campaign.
- "All 84 C# samples verified pixel-exact on macOS" — they were smoke-run (start, load content, run to a 15 s alarm, no exception/refusal in logs).
- "cna-cs" as the current repository name — renamed to cna-dotnet (keep the product name CNA.NET).
