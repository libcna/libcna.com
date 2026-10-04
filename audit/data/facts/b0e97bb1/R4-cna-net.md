# R4 — CNA.NET (C# binding of CNA): evidence-classified facts

## Executive summary (15 lines)

1. CNA.NET = repo `libcna/cna-cs` (public, default branch `develop`); C#/.NET binding over CNA's C ABI; Ms-PL. Status in its own words: "exact public metadata for the selected XNA 4.0 Windows runtime profile; not yet behaviorally complete or release-ready" and "beta, source-first".
2. Layers: game → `CNA.XnaCompat` (namespace `Microsoft.Xna.Framework.*`) → `CNA.Framework` (namespace `CNA.*`) → `CNA.Interop` (internal `LibraryImport` P/Invoke, 1419 imports) → CNA C ABI (`libcna_c_api`) → CNA C++.
3. Source compatibility is the goal; strong-named Microsoft binary identity is explicitly NOT taken. Pure-IL prebuilt XNA libraries can run via XNA-named, key-less type-forwarding assemblies; a game's own `.exe` is not run as a binary.
4. ABI pairing: CNA.NET admits exactly C ABI **0.44.0** (point matrix, not a range). CNA at T (`b0e97bb`) exports 0.44.0 and differs from the tested CNA commit (`8a7e13ff5`) only by 4 docs commits → **CNA@T and cna-cs@860f92c are a matched pair**. libcna.com still says "pinned to 0.21.x / pre-alpha / CNA exports 0.29.0" — stale.
5. Requirements: .NET 8+ SDK (desktop libs target `net8.0`; generators need Roslyn 4.11 = SDK 8.0.4xx); browser/Android heads need .NET 11 (RC1 used) + `wasm-tools`/`android` workload. Native lib located via `CNA_NATIVE_LIBRARY` (abs path) > `CNA_NATIVE_DIR` > beside app / `runtimes/<rid>/native`.
6. No published NuGet packages and no official native binaries; local package acceptance only (linux-x64, `0.1.0-local.1`).
7. Metadata: strict XNA 4.0 Windows runtime profile 256/256 types, 0 diagnostics; GamerServices/Avatar/Net profile 75/75 (measured locally against legally supplied XNA reference assemblies, 2026-10-04).
8. Local test matrix 2026-10-04 (Linux x64, OPENGLES3 + compiled effects): 1,261 managed/native tests per configuration (653+319+5+260+24), Debug and Release.
9. Linux x86_64 is the only broadly runtime-qualified platform — but runs were on *private* displays (Xvfb/llvmpipe or headless Weston+Xwayland on the real GPU), never the owner's interactive desktop.
10. Browser: plain `Microsoft.NET.Sdk.WebAssembly` (not Blazor) + static CNA WebGL2 archive; qualified ONLY in **headless Chromium + SwiftShader**; optional threaded build works but WebGL is proxied (slow). No interactive browser / hardware GPU / audio / video qualification.
11. Android: SDL activity host; qualified ONLY on **x86_64 emulator, API 35, headless, `-no-audio`, swiftshader GPU**; arm64-v8a packaging builds but nothing ran on it; no physical device.
12. Windows/macOS/iOS: not runtime-qualified ("nothing was run on them"); Windows build steps are documented but unverified.
13. Campaign (CSX-001..155, 2026-10-01..04, closed, saturation B): 82/84 Microsoft gallery rows run on Linux unchanged; 84-row manifest runs in headless Chromium and the emulator; 95 external project investigations; final 10-project sweep found 0 new general defects.
14. Template `cna-game` (local `dotnet new install <path>`): one shared source set + desktop (`net8.0`), `Platforms/Browser` (`net11.0`) and `Platforms/Android` (`net11.0-android`) heads. Multi-language demo: C++, C, C# — one unchanged `StarfieldGame.cs` builds and runs on CNA.NET and FNA.
15. GitHub CI is NOT green evidence: latest completed runs (2026-10-02/03) failed 4 jobs; runs for the final commits are queued; native/strict-API jobs skip without secrets. All headline numbers are local measurements recorded in docs.

---

## 0. Repository state (read-only; facts are from committed content)

| Repo | Branch | HEAD (full) | Commit date | Tree | origin/develop |
| --- | --- | --- | --- | --- | --- |
| cna-cs | develop | `860f92cca30f0862f6eabf7970269ce49af90536` | 2026-10-04 13:20:39 +0200 ("docs: point CNA links at libcna") | clean | = HEAD |
| cna-cs-template | develop | `008c3b1e720b74ac2b411c9f411f372e0a4c2f56` | 2026-10-04 11:47:05 +0200 ("docs(CSX-154)…") | clean | = HEAD |
| cna-multi-language-3d-demo | develop | `16bde3c20fd6e3f4539e1e6ed8a2869c65e002dd` | 2026-10-04 12:09:44 +0200 ("feat(CSX-155)…") | clean | = HEAD |
| cna (read via git objects only) | — | T = `b0e97bb1bb876f9b3edd6f4ff1ef3067908ae8ac` | 2026-10-04 13:20:39 +0200 ("docs: point release links at libcna") | n/a (working tree is on `samples` @1f2ada05, dirty — NOT used) | — |

- GitHub (queried read-only via `gh repo view`, 2026-10-04): all three sibling repos are PUBLIC with default branch `develop`. `origin/main` is stale in each (cna-cs main = 7f73954, 2026-08-15, 437 commits behind, lacks the migration guide; demo main still lists Java/TS/Python/Rust/... ports that were removed). → Site links must point at `develop` (or pinned SHAs), never `main`.
- cna-cs `5e94c82` (campaign closure HEAD named in CNA handoff) is an ancestor of `860f92c`; the only later commit edits 10 doc/link files (18+/18−). Evidence: `git log 5e94c82..HEAD`.
- CNA commits cited by cna-cs docs (`ed885a8ae` ABI 0.44.0 baseline, `21dc29101` audit, `8a7e13ff5` measured state, `28f8312f0`, `16dce8d5a`) are all ancestors of T. `git log 8a7e13ff5..T` = 4 docs-only commits, 2 files, no `modules/c-api` change; `git diff ed885a8ae T -- modules/c-api/include` is empty. [source fact]
- CNA@T `modules/c-api/include/CNA/C/abi.h:34-40`: MAJOR 0, MINOR 44, PATCH 0. [source fact]

Citation shorthand: `cs@860f92c` = cna-cs, `tpl@008c3b1` = cna-cs-template, `demo@16bde3c` = cna-multi-language-3d-demo, `cna@T` = cna @ b0e97bb.

---

## 1. Architecture

| Layer | Project / assembly | Namespace(s) | Responsibility | Evidence |
| --- | --- | --- | --- | --- |
| Game | user code | `Microsoft.Xna.Framework.*` | unchanged XNA 4.0 source | cs@860f92c:README.md:10-20 |
| XNA facade | `CNA.XnaCompat` (`CNA.XnaCompat.dll`) | `Microsoft.Xna.Framework`, `.Graphics`, `.Graphics.PackedVector`, `.Audio`, `.Content`, `.Input`, `.Input.Touch`, `.Media`, `.Storage`, `.GamerServices`, `.Net`, `.Design`; plus `CNA.XnaCompat.Extensions` (renderer diagnostics, outside strict profile) | Reproduces XNA public type system via composition/internal adapters delegating to CNA.Framework; one owner per native handle; no public `CNA.*` leaks | cs@860f92c:docs/architecture.md:75-97; docs/xna-compatibility.md:72; `grep ^namespace src/CNA.XnaCompat` |
| Idiomatic API | `CNA.Framework` (`CNA.Framework.dll`) | bare `CNA`, `CNA.Graphics`, `CNA.Input`, `CNA.Content(.Xnb/.Cnb)`, `CNA.Audio`, `CNA.Media` (project name ≠ namespace, deliberately) | Managed value types in pure C#; native resources wrapped in `SafeHandle`; `CnaResult` → `CnaException`; `Game` lifecycle via `[UnmanagedCallersOnly]` callbacks | docs/architecture.md:27-73 |
| Interop | `CNA.Interop` (`CNA.Interop.dll`) | `CNA.Interop` | All-internal `LibraryImport` (source-generated) P/Invoke + ABI structs; native loader/ABI admission. `InternalsVisibleTo` CNA.Framework, CNA.XnaCompat, CNA.PhoneCompat (+tests/tools) | docs/architecture.md:46-53; src/CNA.Interop/AssemblyInfo.cs; 1419 `[LibraryImport(` declarations in src/CNA.Interop/Native*.cs (counted) |
| Native | CNA C ABI `libcna_c_api.so` / `cna_c_api.dll` (`.dylib` recognized) | C (`cna_*`) | Owned by libcna/cna `modules/c-api`; CNA.NET only consumes it | docs/architecture.md:136-143 |
| Engine | CNA C++ (+ Sharp Runtime internally, never exposed to C#) | `CNA::` | — | docs/architecture.md:154-190; NOTICE.md:22-31 |

Documented exceptions/extras (source facts):
- GamerServices, Avatar, Net call `CNA.Interop` directly from the facade (no CNA.* layer) — docs/architecture.md:107-121.
- Opt-in assemblies: `CNA.PhoneCompat` (`Microsoft.Devices`, `Microsoft.Devices.Sensors`; Windows Phone, not XNA), `CNA.WindowsFormsCompat` (tiny `System.Windows.Forms` subset: window lookup, border style, MessageBox), `CNA.BrowserCompat` (`System.IO.IsolatedStorage` for the browser runtime), `CNA.XnaCompat.Generators` (Roslyn source generators, netstandard2.0) — docs/architecture.md:99-105; src/*/ *.csproj descriptions; docs/migrating-xna-games.md:446-456.
- `src/XnaAssemblies/*`: ten assemblies named `Microsoft.Xna.Framework`, `.Avatar`, `.Game`, `.GamerServices`, `.Graphics`, `.Input.Touch`, `.Net`, `.Storage`, `.Video`, `.Xact`, version 4.0.0.0, containing only type forwards to CNA.XnaCompat, **carrying no public key** — src/XnaAssemblies/Directory.Build.props:3-21; docs/xna-compatibility.md:285-307.

Binary-compatibility claim (exact wording to respect):
- "Binary compatibility with Microsoft's strong-named assemblies is not the primary goal." — cs@860f92c:README.md:22-24. [source fact]
- Compatibility ladder: source → exact public metadata → behavior → selected FNA/MonoGame/Kni portability → "binary compatibility, which is not a primary goal." — docs/xna-compatibility.md:6-12.
- "They carry no public key: CNA.NET does not take Microsoft's identity." Prebuilt pure-IL libraries compiled against XNA run unchanged via forwarders + `CnaRetargetXnaReferences`; "An XNA game's own `.exe` is not run as a binary." — docs/xna-compatibility.md:291-307. Evidence for library path: `XnaBinaryLibraryTests` + Resonance with prebuilt BEPUphysics (same lines). [source fact + runtime-qualified fact, Linux]
- NOTICE: not produced/endorsed by Microsoft; does not include/redistribute/link Microsoft XNA binaries — NOTICE.md:8-20.

---

## 2. Requirements and native-library configuration

| Item | Fact | Class | Evidence |
| --- | --- | --- | --- |
| .NET SDK (desktop) | ".NET 8 or later"; all libs `TargetFramework net8.0`; CI uses `8.0.x` | source/build | README.md:51; Directory.Build.props:4; .github/workflows/build.yml:31 |
| Roslyn floor | generators target Roslyn 4.11 = ".NET SDK 8.0.4xx" | source | src/CNA.XnaCompat.Generators/CNA.XnaCompat.Generators.csproj:6-7,19 |
| .NET 9+ | XNA-era `BinaryFormatter` re-enabled through OOB package 10.0.12 for net9+ apps; opt-out `<CnaBinaryFormatter>false</CnaBinaryFormatter>` | source | CAMPAIGN.md:171; docs/migrating-xna-games.md:453-456 |
| Browser/Android | ".NET 11 and the corresponding workload" (`wasm-tools` / `android`); campaign used .NET 11 RC1; .NET 8/10 pin Emscripten 3.1.x whose libc++ cannot compile CNA; .NET 11 pins Emscripten 6.0.x | source/build | docs/migrating-xna-games.md:57-59; scripts/Build-BrowserNative.sh:5-7; CAMPAIGN.md:92,1246-1247 |
| Native toolchain | C++23 compiler, CMake ≥3.20, sibling checkouts `cna`, `sharp-runtime`, `easy-gl`, `meta-gl`; `git submodule update --init --recursive` in cna | source | docs/migrating-xna-games.md:36-59 |
| RIDs | `linux-x64`: "measured-local-evidence; not an official shipping claim". `linux-arm64`, `win-x64`, `win-arm64`, `osx-x64`, `osx-arm64`: pending, nativeEvidence none. Browser: static link into `dotnet.native.wasm`. Android: `android-x64` default, `android-arm64` via `-p:RuntimeIdentifier`. iOS: "planned as static `__Internal`" | source/future plan | eng/platform-matrix.json:15-52; eng/browser/CNA.Browser.targets:7-10; tpl@008c3b1:Platforms/Android/CnaCsTemplate.Android.csproj:19; docs/migrating-xna-games.md:430-440; CAMPAIGN.md:184-187 |
| Native lookup | 1) absolute `CNA_NATIVE_LIBRARY` (fail-fast, no fallback) 2) absolute `CNA_NATIVE_DIR` with exactly one recognized library (fail-fast) 3) beside the app incl. `runtimes/<rid>/native`. No source-tree, bare system-name, or process loader-path search. `CNA_NATIVE_DIAGNOSTICS=1` adds low-level loader details. Logical import name `cna-native`, candidates `cna-native`, `cna_c_api`. Android loads by bare name. | source | src/CNA.Interop/NativeLibraryResolver.cs:8-25; docs/packaging.md:105-119; README.md:61-75; CAMPAIGN.md:1260-1262 |
| MSBuild properties | `CnaCsRoot` / env `CNA_CS_ROOT` (dev mode source checkout); `XnaProfile` (Reach/HiDef → embedded `Microsoft.Xna.Framework.RuntimeProfile` resource), `XnaPlatform`; opt-outs `CnaBinaryFormatter`, `CnaNetFx40ListForEach`, `CnaNetFxAssemblyLoadFile`, `CnaNetFxTypeNames`, `CnaNetFxNumberSymbols`, `CnaSixtyFourBitLayouts`; browser `WasmEnableThreads`, `CnaBrowserNativeArchive`, `CnaGameContentDirectory`; Android `CnaAndroidNativeDirectory` | source | docs/migrating-xna-games.md:175-218; docs/xna-compatibility.md:140-160,243-249; src/CNA.XnaCompat/build/CNA.XnaCompat.targets (grep); eng/browser/CNA.Browser.targets:12-33,74-93; eng/android/CNA.Android.targets:12-13 |

C ABI admission (`cna-cs-native-abi/1`) — cs@860f92c:docs/native-abi-compatibility.md, eng/cna-native-abi-policy.json, src/CNA.Interop/CnaNativeAbiPolicy.cs:13-27:
- `ConsumerVersion = (0<<16)|(44<<8)|0` → exactly **0.44.0** accepted; any other 0.x rejected; any 1.x+ rejected (native-abi-compatibility.md:23-32). Point list, "There is no `>= 0.44` rule". [source fact]
- Rationale: under major 0, each minor is a reviewed generation that may be incompatible; patch also needs a matrix entry because native metadata has no shape fingerprint (lines 8-21).
- Load-time proof before returning a handle: readable `cna_get_abi_version` + exact matrix entry; every `LibraryImport` symbol present; `cna_error_get_last_message_size` signature canary; guarded `cna_touch_capabilities_init` 16-byte v1 shape canary (lines 295-303; policy json `validation`). Extra exports allowed.
- Browser: CNA is statically linked; only the version is checked at startup (missing symbols fail the link) — NativeLibraryResolver.cs:52-70.
- Build-time evidence: `tools/abi-verify` (1137 native/managed layout values, 0 mismatches; 1419 prototypes compiled; 23 callbacks; 604 constants), upstream `baselinediff.py` 0.43.0→0.44.0: 0 breaking (lines 67-79; README.md:40-44).
- Fixtures: 12 isolated (2 accepted, 10 rejected incl. `retired-0.43.0`, `unreviewed-0.45.0`) via `scripts/Verify-NativeAbiCompatibility.sh` (lines 314-336). [runtime-qualified fact, Linux, local]
- Retired: 0.6.0…0.43.0 (15 generations) — lines 45-58.
- Note doc drift: native-abi-compatibility.md:248 says "1409 names", :300 says "1416", README and actual source = **1419** imports. packaging.md:90-116 still describes the old 861-import / 0.6.0-era fixture matrix (historic). Quote 1419 / 0.44.0 only.

---

## 3. Build steps (copied from docs; not re-run by this research)

CNA C API, Linux (qualified configuration) — cs@860f92c:docs/migrating-xna-games.md:67-91 [source fact; runtime-qualified on Linux x64]:
```bash
cmake -S "$CNA_ROOT" -B "$CNA_ROOT/build" -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DCNA_GRAPHICS_RENDERER=OPENGLES3 \
  -DCNA_BUILD_C_API=ON \
  -DCNA_EASYGL_COMPILED_EFFECTS=ON
cmake --build "$CNA_ROOT/build" --target cna_c_api --parallel
export CNA_NATIVE_LIBRARY="$CNA_ROOT/build/modules/c-api/libcna_c_api.so"
```
- Verified at cna@T: `option(CNA_BUILD_C_API … OFF)` CMakeLists.txt:80; target `cna_c_api` modules/c-api/CMakeLists.txt:23,88; `CNA_EASYGL_COMPILED_EFFECTS` default OFF, pulls MojoShader via `cmake/ThirdPartyFNA3D.cmake` (cmake/RendererSelection.cmake:245-256) — needed for compiled XNA `.xnb` effects. [source fact]
- Installed (packaging) variant: `cmake --install <build> --component CNACApi --prefix …` — cna@T:docs/c-api/CONSUMING.md:30-35; cs@860f92c:docs/packaging.md:26-31.

CNA C API, Windows (documented, NOT runtime-qualified) — docs/migrating-xna-games.md:98-122: VS 2022 generator, `-DCNA_GRAPHICS_RENDERER=SDL_RENDERER -DCNA_BUILD_C_API=ON`, `--target cna_c_api`; set `$env:CNA_NATIVE_LIBRARY` to `cna_c_api.dll`. Doc itself: "treat this as a source-build workflow rather than a final platform-support promise." Note SDL_RENDERER has no 3D pipeline (tpl@008c3b1:README.md:159-170).

CNA.NET build + tests — cs@860f92c:README.md:53-66 [build fact]:
```bash
dotnet restore CNA.sln
dotnet build CNA.sln -c Release --no-restore
dotnet test tests/CNA.Framework.Tests/CNA.Framework.Tests.csproj
dotnet test tests/CNA.XnaCompat.Tests/CNA.XnaCompat.Tests.csproj
CNA_NATIVE_LIBRARY=/path/to/libcna_c_api.so \
  xvfb-run -a dotnet test tests/CNA.Integration.Tests/CNA.Integration.Tests.csproj
```
Strict API check (needs legally obtained XNA 4.0 reference assemblies, not in repo): `XNA_REFERENCE_PATH=… dotnet run --project tools/api-compat -c Release --no-build -- --format text` — README.md:77-89.

Run a sample — use the template (the in-repo `samples/HelloGame/README.md` is stale: still says "No content pipeline exists yet"):
```bash
dotnet new install /path/to/workspace/cna-cs-template
dotnet new cna-game --name MyGame
cd MyGame
CNA_CS_ROOT=/path/to/workspace/cna-cs dotnet build
CNA_CS_ROOT=/path/to/workspace/cna-cs \
CNA_NATIVE_LIBRARY=/path/to/workspace/cna/build/modules/c-api/libcna_c_api.so \
dotnet run            # add: -- --smoke-test (60 frames) / --stability-test (600 frames)
```
docs/migrating-xna-games.md:126-137; tpl@008c3b1:README.md:85-90.

Browser (Linux-only workflow; WSL 2 on Windows) — docs/migrating-xna-games.md:367-404:
```bash
"$DOTNET_ROOT_BROWSER/dotnet" workload install wasm-tools
./scripts/Build-BrowserNative.sh --dotnet-root "$DOTNET_ROOT_BROWSER" --configure   # in cna-cs
CNA_CS_ROOT=/path/to/cna-cs "$DOTNET_ROOT_BROWSER/dotnet" publish Platforms/Browser -c Release
cd Platforms/Browser/bin/Release/net11.0/publish/wwwroot && python3 -m http.server 8080
```
Threaded: `Build-BrowserNative.sh … --threads --configure`, `<WasmEnableThreads>true</WasmEnableThreads>`, serve with COOP/COEP.

Android — docs/migrating-xna-games.md:406-444:
```bash
"$DOTNET_ROOT_ANDROID/dotnet" workload install android
./scripts/Build-AndroidNative.sh --abi x86_64 --ndk "$ANDROID_NDK_ROOT" --configure   # in cna-cs
CNA_CS_ROOT=/path/to/cna-cs "$DOTNET_ROOT_ANDROID/dotnet" build Platforms/Android -c Release -t:Install
```
ARM64: `--abi arm64-v8a` + `-p:RuntimeIdentifier=android-arm64` (packaging only; not run). Native min platform `android-24` (scripts/Build-AndroidNative.sh:31,38; template `SupportedOSPlatformVersion 24`); Android native build has `CNA_ENABLE_VIDEO=OFF` (script :40); browser build also `CNA_ENABLE_VIDEO=OFF`, renderer `WEBGL2` (Build-BrowserNative.sh:69-76).

---

## 4. Migration recipe (XNA 4.0 / FNA / MonoGame) — cs@860f92c:docs/migrating-xna-games.md

XNA 4.0, no `.cs` changes (lines 155-265):
1. Keep the original `.csproj`, content project, sources and built output read-only; record Windows/Windows Phone, Reach/HiDef, Debug/Release, conditional symbols, exact `Compile` list. Don't glob every `.cs`. (157-169)
2. Add an SDK-style wrapper (`net8.0`, `WinExe`, `EnableDefaultCompileItems=false`, `XnaProfile`, `XnaPlatform`, original `DefineConstants` e.g. `WINDOWS`, explicit `<Compile Include="../OriginalGame/…">`, `ProjectReference` to `CNA.XnaCompat`, import `build/CNA.XnaCompat.targets`, copy original `Content/**`). (171-218) `XnaProfile` matters: `GraphicsDeviceManager` picks Reach/HiDef from the embedded RuntimeProfile resource, as XNA did (docs/xna-compatibility.md:243-249).
3. Content: prefer the original XNA 4.0 `.xnb/.xgs/.xwb/.xsb`; otherwise build the original `.contentproj` with XNA 4.0 BuildContent (Linux/Wine script in cna-cs-samples). Keep paths under `Content/`. Watch case sensitivity, backslashes in raw `System.IO`, custom reader assemblies, compiled effects + profile, WMA songs (provide `.ogg/.oga/.qoa` beside the unchanged song `.xnb`). Don't swap content to get green. (220-236)
4. Prebuilt XNA libraries: rebuild from source if possible; pure-IL ones can reference the XNA-named forwarding projects; native/mixed-mode/x86-only/Windows-specific ones need their own build. (238-254)
5. Build/run: `CNA_CS_ROOT=… dotnet build OriginalGame.CNA.csproj -c Release`; `CNA_NATIVE_LIBRARY=… dotnet run …`; run from the original working directory (XACT). (256-265)
- Compile-time .NET-vs-.NET-Framework-4.0 repairs applied automatically (opt-out properties): `List<T>.ForEach` mutation semantics, `Assembly.LoadFile` reuse, `Range`/`Index`/`PriorityQueue` name shadowing, `System.Runtime.Remoting.Messaging` using, 32-bit explicit layouts, and runtime ASCII `Infinity`/`-` number symbols — docs/xna-compatibility.md:140-160.

FNA (267-281): remove `FNA.dll` ref → add CNA.XnaCompat + targets → keep `Microsoft.Xna.Framework.*` source → original content → run against `cna_c_api`. Audit every FNA extension (`*EXT`, FNA env vars, raw FNA3D, custom audio/video); isolate, fix generally, or record as outside strict XNA.

MonoGame (283-306): remove `MonoGame.Framework.*` + platform bootstrap; ordinary `Program.Main` + `Game.Run`; keep profile/symbols; use XNA-built content, not MGCB-only types; audit MonoGame-only APIs, shader dialects, content processors, window hooks, platform services. "CNA.NET does not implement MonoGame extensions merely to increase the number of projects that compile… keep MonoGame as that project's backend." Template adapter example: `-p:Engine=MonoGame|FNA|CNA`.

Not supported / outside scope: FNA/MonoGame engine-specific extensions (docs/xna-compatibility.md:214-222); content pipeline/build-time assemblies (separate future profile, docs/xna-compatibility.md:280; final-compatibility-audit.md:55); Win32 P/Invoke, WPF, full WinForms, Silverlight, dead network services, commercial fonts, proprietary middleware (migrating:479-483); Xbox-only APIs; Phone Shell/Notification (final audit:54-55).

Debugging / which layer is at fault (what the docs actually provide):
- Editors: VS 2022 (open wrapper/generated project; set `CNA_CS_ROOT`/`CNA_NATIVE_LIBRARY` as debug env; VS does not build CNA) and VS Code (`coreclr` launch.json with env) — migrating:308-363.
- Loader problems: absolute `CNA_NATIVE_LIBRARY`, check architecture + ABI version; diagnostics name attempted config, consumer/detected ABI, RID and remediation; `CNA_NATIVE_DIAGNOSTICS=1` for low-level detail — README.md:68-75; migrating:460-464. `NativeLibraryResolver.LoadedLibraryPath / ResolutionSource / DetectedAbiVersion` are public — NativeLibraryResolver.cs:31-38.
- Native refusals: native exceptions never cross the ABI; they become `CNA_Result` + error info → `CnaException`, carrying `CanonicalExceptionType`/`CanonicalParamName` (C ABI ≥0.37). The facade re-raises XNA exception types at key boundaries; elsewhere a native refusal surfaces as `CNA.CnaException` — so a `CnaException` in a stack trace marks a native-side refusal reaching managed code — docs/architecture.md:180-181; docs/xna-compatibility.md:228-241.
- Known native gaps vs facade behavior are tabulated (affected XNA API → native route → observable CNA.NET behavior → required upstream change) in docs/native-behavior-blockers.md (re-audited at 0.44.0, `scripts/Verify-BlockerTable.sh`).
- Report: CNA + CNA.NET commit IDs, C ABI version, OS/arch, renderer, full exception + native log, original project/profile, content provenance, smallest unchanged repro, and whether it runs on real XNA/FNA/MonoGame — migrating:495-500.
- Project rule: "A defect is fixed in the layer it lives in, with a regression test at the lowest layer that can see it plus the C# consumer that exposed it" — CAMPAIGN.md:16-18.
- No explicit "reproduce in C to separate binding vs native bug" recipe exists in the docs; a site could suggest it only as advice (CNA ships a C example `modules/c-api/examples/c/hello_cna.c`, cna@T:docs/c-api/CONSUMING.md:9-24), not as documented procedure.

---

## 5. Platforms — exact evidence level

| Platform | Level | What exactly was run | Not covered | Evidence |
| --- | --- | --- | --- | --- |
| Linux x86_64 | runtime-qualified (primary) — **private displays, not the interactive desktop** | Managed + native suites (1,261 tests/config, OPENGLES3 + compiled effects); 82/84 Microsoft gallery rows unchanged; 95 external project investigations incl. commercial/indie games; ownership 100 cycles. Displays: `xvfb-run` / private Xvfb (llvmpipe) for many captures; CNA's `run_gpu_tests_private.sh` = headless Weston + rootful Xwayland **on the real GPU** (Mesa GLES 3.2) for native suites & demo. Campaign rule: "never `:0`/`wayland-0`". | renderer claims limited to tested matrices; OPENGL33 repeated `Game` construction not requalified (segfault on 2nd cycle historically) | cs@860f92c:README.md:28-44; CAMPAIGN.md:26-27,180; docs/final-compatibility-audit.md:89; docs/native-behavior-blockers.md (OPENGL33 row); cna@T:tools/platform/run_gpu_tests_private.sh:3-24; cna@T:handoff.md:404,699-707,743 |
| Browser / WebAssembly | runtime-qualified **headless Chromium + SwiftShader WebGL2 only** | Host = `Microsoft.NET.Sdk.WebAssembly` project (NOT Blazor) + `wasm-tools` native relink with static `cna-native.a` (WebGL2, JS-lowered exceptions, 64 MB heap); `Game.Run` driven by `requestAnimationFrame` via host-driven run (ABI ≥0.38). All 84 manifest rows run (2026-10-02, CNA ffb82bc0d); 21/25 then-tested games; threaded bundles (`WasmEnableThreads`, Emscripten 6.0.3 shared-memory archive, WebGL proxied via `OFFSCREEN_FRAMEBUFFER`) run Enceladus, Missile Command, Racing Game Kit (attract), Resonance (2026-10-04 requal CSX-150). Driven by Playwright `scripts/Run-BrowserPage.mjs` with scripted input. | interactive Chrome, hardware GPU, other browsers, audio, video (no backend), UDP; threaded perf ~0.65 fps Racing Game Kit; .NET 11 RC1 `Thread.Start` fault for workers created after `Main` | eng/browser/CNA.Browser.targets:1-33; scripts/Run-BrowserPage.mjs:1-8; CAMPAIGN.md:92-95,143-144,175,177; docs/final-compatibility-audit.md:90; docs/migrating-xna-games.md:394-404; cna@T:handoff.md:451-476,744 |
| Android | runtime-qualified **x86_64 emulator only** | AVD `Medium_Phone`, API 35 x86_64 Google APIs image, emulator 36.5.11.0, `-no-window -no-audio -gpu swiftshader_indirect`, NDK 29.0.14206865, .NET 11 RC1 `android` workload. Host: SDL's `SDLActivity` + `CnaGameApplication`; `Main` runs on SDL's thread. 84/84 gallery rows draw, 78 end on one Back press; pause/resume, relaunch, touch; 24/25 games (2026-10-02). | physical device, ARM/arm64-v8a runtime (packaging builds, "nothing ran"), audible audio, GL context loss, full lifecycle/input | CAMPAIGN.md:101-102,1130-1160,1244-1275; eng/android/CNA.Android.targets:1-35; docs/final-compatibility-audit.md:91; cna@T:handoff.md:481-488,745 |
| Windows | build architecture only; **not runtime-qualified**, "nothing was run on them" | Documented build steps (unverified). CI `portable-abi-header` on `windows-latest` (clang header/layout check) succeeded in run of 994327d (2026-10-03) = compile-time ABI evidence only. Wine runs of real XNA are oracles, not CNA-on-Windows. | everything at runtime | docs/migrating-xna-games.md:96-122; docs/final-compatibility-audit.md:92; cna@T:handoff.md:492-493; `gh run view 37125269028` |
| macOS | not runtime-qualified | resolver recognizes `.dylib`; CI ABI header check on macos-14 (arm64) succeeded, macos-13 cancelled (same run) | everything at runtime | docs/final-compatibility-audit.md:93; src/CNA.Interop/CNA.Interop.csproj:20 |
| iOS | future plan | "planned as static `__Internal`"; `Game.Run` skips `PosixSignalRegistration` on Android/iOS | everything | CAMPAIGN.md:184-187,1262-1263; docs/final-compatibility-audit.md:94 |

Dates: final audit 2026-10-04 (docs/final-compatibility-audit.md:3); migration guide platform statement 2026-10-04 (CAMPAIGN.md:213-232).

---

## 6. cna-cs-template (tpl@008c3b1)

- Install (local path; no published template package): `dotnet new install /path/to/cna-cs-template` then `dotnet new cna-game --name MyGame` — README.md:96-102; cs docs/migrating-xna-games.md:126-131.
- template.json: identity `OpenEggbert.CNA.Game.CSharp`, name "CNA C# XNA-style game", **shortName `cna-game`**, tags language C#, type project, classifications Games/CNA/XNA; parameters `consumerMode` = `Development` (default; references a CNA.NET source checkout) | `Package` (references `CNA.XnaCompat` from a NuGet feed; excludes `Platforms/**`), `cnaPackageVersion` (default `0.1.0-local.1`); excludes `Directory.Build.props`, `scripts/**` — .template.config/template.json:9-72.
- Generated structure (sourceName `CnaCsTemplate` → your name): `<Name>.csproj` (desktop, `net8.0`, `WinExe`, `Engine` default CNA; alternative `-p:Engine=MonoGame|FNA|Kni`), `HelloGame.cs`, `Program.cs`, `EngineDiagnostics.cs` (only engine-specific query), `Content/logo.png` (loaded raw via `Texture2D.FromStream`), `Platforms/Browser/<Name>.Browser.csproj` (`Microsoft.NET.Sdk.WebAssembly`, `net11.0`, compiles `../../*.cs`, imports cna-cs `eng/browser/CNA.Browser.targets`), `Platforms/Android/<Name>.Android.csproj` (`net11.0-android`, `SupportedOSPlatformVersion 24`, default RID `android-x64`, `AndroidManifest.xml`, `GameApplication.cs`, Content as Android assets) — CnaCsTemplate.csproj:1-106; Platforms/*/…csproj; `git ls-files`.
- Game content: lifecycle, device management, resize, keyboard/mouse/gamepad, PNG decode, Texture2D, SpriteBatch, rotating BasicEffect cube; 2D fallback when renderer lacks 3D — README.md:14-16.
- Run each head: desktop `CNA_CS_ROOT=… dotnet build` + `CNA_NATIVE_LIBRARY=…/libcna_c_api.so dotnet run` (or `CNA_NATIVE_DIR`); browser `dotnet publish Platforms/Browser -c Release` then serve `bin/Release/net11.0/publish/wwwroot` over HTTP; Android `dotnet build Platforms/Android -c Release -t:Install` — README.md:25-41,63-81. Template browser head is single-threaded by default ("a game that starts threads of its own is not for this head") — README.md:80-81; threaded path documented in cna-cs guide.
- Measured (Linux x64): CNA 60/600 frames on OPENGLES3, SOFTWARE, SDL_RENDERER (2D fallback), HEADLESS; FNA 600 frames (Vulkan, AMD Radeon 780M) from same source — README.md:156-165 [runtime-qualified, Linux; display type not stated for CNA rows]. Package-mode consumer: 60/600 frames OPENGLES3 from packaged RID asset with no env overrides — cs docs/packaging.md:78-83.
- `scripts/verify-template.sh --mode development|package` installs, generates into cna-cs `build-consumer/template-<mode>`, builds; smoke runs via CNA's private display runner — README.md:104-113. Last recorded dev-mode verification: 0 warnings/0 errors (CAMPAIGN.md:181, CSX-154) [build fact].
- License MIT (template) vs Ms-PL (cna-cs).

---

## 7. cna-multi-language-3d-demo (demo@16bde3c)

"CNA Starfield Courier", a small third-person 3D game (3 sectors, energy cells, hazards, extraction gate, chase camera, procedural `BasicEffect` geometry, HUD, sound) implemented in exactly three languages, all DONE: **C++** (CNA's XNA-style C++ API; reference), **C** (C99 on the public CNA C ABI: lifecycle, input, BasicEffect, audio/media), **C#** (one `cs/StarfieldGame.cs`, no CNA/FNA conditionals; MSBuild `-p:Engine=CNA` → `ProjectReference` to `CNA.XnaCompat` via `CNA_CS_ROOT`, or `-p:Engine=FNA` → `FNA.dll` via `FNA_FRAMEWORK_PATH`; `net8.0`) — README.md:3-67; cs/StarfieldCourier.csproj:1-31; cs/Directory.Build.props. Earlier plan for Java/TS/Python/Rust/etc. ports was removed ("No additional language ports are planned here", README.md:12-14). Evidence 2026-10-04: native suite 11/11 (7 C++ incl. OpenGL 3.3 + OpenGL ES 3, 4 C); both C# builds 0 warnings/errors; gameplay executables pass and `frame_valid=true` for all 3 sectors on **CNA's private real-GPU Weston/Xwayland runner** — CNA.NET on CNA's OpenGL 3.3 renderer, FNA on its Vulkan backend — BUILDING.md:62-70,153-158; cs CAMPAIGN.md:182,193-211. [runtime-qualified, Linux, private headless compositor with real GPU] MIT license.

---

## 8. Final compatibility audit and the CSX campaign

- Campaign: CSX-001..155 (106 task rows incl. range row `CSX-053..`), started 2026-10-01, **closed 2026-10-04**, "saturation condition B"; now maintenance/stabilization mode — cs@860f92c:CAMPAIGN.md:1-8. Goal statement: "existing XNA 4.0 C# source runs on CNA with no `.cs` changes -- same product category as MonoGame/FNA" (CAMPAIGN.md:9-10) [goal, not evidence].
- Final audit (cs docs/final-compatibility-audit.md, audited 2026-10-04 vs CNA `21dc29101`, ABI 0.44.0, CNA.NET `7db0863`): metadata 256/256 (Windows runtime) and 75/75 (GamerServices/Avatar/Net), 0 unallowlisted diagnostics; **zero** executable `throw new NotImplementedException` in `src/`; strict facade has no TODO/FIXME; 24 static `NotSupportedException` sites reviewed (lines 3-32). Remainder classified future work / platform limitation / intentionally unsupported (lines 34-56).
- Regression matrix CSX-153 (2026-10-04): Debug+Release each 653 Framework, 319 XnaCompat, 5 BrowserCompat, 260 native Integration, 24 GamerServices = 1,261/config, 2,522 total; native C API 107/107, compiled effects 710/710, Runtime/Game 208 + 2 expected skips; ownership 100/100 recreations, 3,000/3,000 releases (CAMPAIGN.md:180,234-258; docs/xna-compatibility.md:164-174). [runtime-qualified, Linux x64, local]
- Application corpus (CNA handoff at T, cna@T:handoff.md:699-707): **82 of 84** Microsoft XNA gallery rows run on Linux from unchanged Microsoft C# source (Yacht excluded by owner decision; PerformanceUtility has no C++ reference); the **84-row runnable manifest** passes in headless Chromium/SwiftShader and on the x86_64 Android emulator; **95 documented external project investigations** (85 rows + 10-project final sweep; some rows cover several apps). Final sweep: 2 ran unchanged, 8 stopped on non-XNA/external causes, 0 new general defects (CAMPAIGN.md:178). Notable unchanged games: Speedy Blupi, Rookie Drivers, TIE Fighter Forever, Resonance, Escape From Enceladus, Microsoft's Racing Game Kit (races) etc. (CAMPAIGN.md:86). Handoff caveat: "This is not a claim of 100% compatibility with every game." (handoff.md:768)
- Behavior corpus: prose says 470 observations, CNA runs all 470 (docs/xna-compatibility.md:100-114); generated manifest now totals **483** (docs/generated/behavior-corpus.md) — inconsistency; avoid quoting a number or say "~470+".
- CNA side at T: `git log --oneline 009d40f5..b0e97bb1 | grep -c CSX` = **24** (of 456 commits in range); CBIND-tagged = 40. Native fixes driven by C# are tracked as CBIND-128…158 (plans/plan_binding.md) and FX-*. Files at T mentioning "CNA.NET": `handoff.md` (campaign handoff + closure, 15 hits), `misc/analysis_binding.md`, `misc/analysis_binding_sharp_runtime.md` (design analyses), `plans/plan_binding.md`, `plans/plan_cabi.md`, `plans/plan_fx.md`, `docs/c-api/CABI_BLOCKER_HANDOFF.md`. CNA README at T does not mention CNA.NET.

---

## 9. Known limitations (from cna-cs docs; top 10+)

1. **Not released**: beta, source-first; no official native binaries, no published NuGet packages or public feed; production projects `IsPackable=false`; January 2027 stabilization start is "a roadmap expectation, not a binary-release date or support guarantee" — docs/migrating-xna-games.md:9-12,151-153; docs/packaging.md:3-6. [future plan for the date]
2. **Exact ABI pairing**: accepts only C ABI 0.44.0; any other CNA build is refused at load — README.md:68-72.
3. **Platform qualification**: Linux x86_64 only broadly; browser = headless Chromium/SwiftShader; Android = x86_64 emulator; Windows/macOS/iOS unqualified — final-compatibility-audit.md:85-94; migrating:18-21.
4. **Browser gaps**: no video backend, no UDP networking, audio/hardware-GPU/interactive not qualified; threaded WebGL proxied and slow (~0.65 fps worst case); single game per page — migrating:401-404; CAMPAIGN.md:175, 1320-1336.
5. **Toolchain friction**: browser/Android heads need .NET 11 (RC) + workloads + Linux-only staging scripts (WSL 2 on Windows); Visual Studio does not build CNA — migrating:57-59,367-368,321-323.
6. **Behavior not complete** ("not yet behaviorally complete", README.md:3-5). Specific: `GraphicsDevice.Present` with non-default args throws `NotSupportedException`; `ResourceCreated/Destroyed` never raised; `VideoPlayer.GetTexture` one borrowed transient texture; `AudioEngine` renderer/look-ahead ignored; non-empty `PropertyDictionary` streams refused; `LeaderboardWriter` unsupported; some native refusals arrive as `CNA.CnaException` rather than the XNA exception type — final-compatibility-audit.md:38-53.
7. **Content**: XNA songs are WMA, which CNA does not decode — needs `.ogg/.oga/.qoa` beside the `.xnb`; no content pipeline (XNA 4.0 BuildContent, e.g. under Wine, is required to (re)build content) — xna-compatibility.md:192-195; migrating:220-236.
8. **Scope**: XNA 4.0 only; no FNA/MonoGame extension subset; Xbox-only APIs and Content Pipeline assemblies are separate future profiles; Phone Shell/Notification intentionally unsupported — xna-compatibility.md:214-226,279-280; final audit:54-55.
9. **Host APIs not supplied**: Win32 P/Invoke, WPF, full WinForms (only a small subset; `Form.Opacity` stored but not applied), Silverlight, dead online services, commercial fonts, proprietary middleware — migrating:446-452,479-483; final audit:50.
10. **Binary limits**: game `.exe` never run as binary; native/mixed-mode/32-bit-by-construction libraries need their own build — xna-compatibility.md:302-307; migrating:253-254,472-477.
11. **Security caveat**: XNA-era `BinaryFormatter` enabled by default for compatible apps (trusted legacy data only; opt out) — migrating:453-456.
12. **Native stability follow-ups**: OPENGL33 repeated-construction not requalified; SDL_RENDERER + `SDL_VIDEODRIVER=offscreen` aborts; abrupt-signal native teardown; C smoke timing flakes under high parallelism — final audit:71-83; packaging.md:128-140.
13. **CI**: GitHub Actions `release-qualification` — last completed runs (2026-10-02/03, e.g. 994327d) concluded failure (failed: behavior-pure-corpus, template-development, leak-only-verifier, package-consumer-managed; builds/managed tests/ABI jobs passed); runs for 5e94c82/860f92c queued; `native-qualified-linux-x64` and `strict-api` skipped (need secrets) — external observation via `gh run list/view`, 2026-10-04.

---

## 10. Comparison vs MonoGame/FNA (only what cna-cs docs state, with evidence)

- Same compile-probe source passes against Microsoft XNA reference assemblies, CNA.XnaCompat, FNA and MonoGame; fails on Kni at one hierarchy assertion — docs/xna-compatibility.md:116-120. [compatibility result]
- Template source table: CNA pass 60/600 frames (OPENGLES3); FNA compile pass, runtime "Unavailable" in that audit; MonoGame DesktopGL 3.8.1.303 pass 60 frames (llvmpipe); Kni 4.2.9001 pass 60 frames — xna-compatibility.md:122-132 (later template README measured FNA 600 frames on Vulkan, tpl README.md:156-157; demo shows both CNA.NET and FNA pass). [compatibility result, Linux]
- Behavior corpus: CNA runs all observations; FNA emits the 199 pure ones then aborts in its own `SoundEffect` finalizer; MonoGame emits 106 pure ones then aborts in audio init and lacks Storage/XACT runtime surface — xna-compatibility.md:84-89,109-111; generated/behavior-corpus.md comparator table. [compatibility result, measured Linux environment]
- XNA-IL-verified value where FNA and MonoGame differ: `Color(0.5f, NaN, +∞, −∞)` → `00FF0080` — xna-compatibility.md:202-206.
- Shared design precedent: XNA-named forwarders "as FNA's `abi/` assemblies are for FNA"; WMA→ogg song substitution "as in CNA and FNA" — xna-compatibility.md:192-195,291-294.
- Performance, platform breadth, maturity, ecosystem: **no evidence** in cna-cs docs. Do not compare.

---

## 11. Suggested evidence-safe public wording (homepage / feature overview)

> CNA.NET is the C#/.NET binding for CNA. It provides the `Microsoft.Xna.Framework` API as a source-compatible facade (`CNA.XnaCompat`) over an idiomatic `CNA.*` layer and an internal P/Invoke layer that talks only to CNA's C ABI. Its public metadata exactly matches the selected XNA 4.0 Windows runtime profile (256 of 256 types, plus 75 of 75 GamerServices/Avatar/Net types); it does not take Microsoft's assembly identity. Existing XNA 4.0 games are rebuilt from their original, unchanged `.cs` files and original `.xnb` content through a small SDK-style wrapper project. On Linux x86_64, 82 of 84 Microsoft XNA samples and many real XNA games run this way. The same C# code has also run in headless Chromium (WebAssembly) and on an x86_64 Android emulator, but interactive browsers, physical Android devices, Windows, macOS and iOS are not yet qualified. CNA.NET is beta and source-first: there are no published packages or prebuilt binaries yet, and each CNA.NET revision accepts exactly one reviewed CNA C ABI version (currently 0.44.0). A `dotnet new cna-game` template and a step-by-step migration guide for XNA, FNA and MonoGame projects are available in the repositories.

Wording rules: say "source-compatible", never "binary-compatible" or "drop-in for XNA binaries"; say "headless Chromium" not "runs in your browser"; say "Android emulator (x86_64)" not "Android"; never say "100% compatible"; do not claim CI-verified; avoid "pre-alpha" (docs now say beta) and avoid "release-ready".

---

## 12. Stale libcna.com content found (for the updater)

- index.html:411-412 CNA.NET card: "pre-alpha … pinned to ABI 0.21.x … this CNA snapshot exports ABI 0.29.0 … not paired" → at T both are 0.44.0 and paired.
- data/current-facts.json:150-155 (`bindings_expected_abi` 0.21.x; `cna-cs` pin e223909 2026-09-03).
- docs/c-api.html:195 (cna-cs e223909, ABI 0.21.0, "Refuses it").
- development/architecture/bindings.html:172 (C#/.NET 0.21.x).
- development/internals/bindings/csharp.html (whole page pinned to e223909 / ABI 0.21.0; links to `blob/e223909…` paths).
- Also in cna-cs itself: Directory.Build.props:14-15 `PackageProjectUrl`/`RepositoryUrl` = `github.com/openeggbert/cna-dotnet` and NOTICE.md:1 "(`cna-dotnet`)" — stale identifiers; the real repo is `github.com/libcna/cna-cs`.

## 13. Doc inconsistencies inside cna-cs (do not propagate)

- Import count: 1419 (README, actual source) vs 1416 (native-abi-compatibility.md:300) vs 1409 (:248); packaging.md "861" (historic).
- Behavior corpus: 470 (xna-compatibility.md) vs 483 (generated manifest).
- FNA template runtime: "Unavailable" (xna-compatibility.md:127) vs FNA 600 frames (template README) and demo pass.
- CNA commit cited for "measured state" varies (8a7e13ff5 / 21dc29101 / ed885a8ae) — all ABI 0.44.0 and ancestors of T.
- samples/HelloGame/README.md is pre-content-pipeline-era (stale).
- csproj description of CNA.XnaCompat says it "never references CNA.Interop directly", but InternalsVisibleTo + architecture.md document the GamerServices/Net exception.
