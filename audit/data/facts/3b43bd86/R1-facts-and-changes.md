# R1 — Facts and changes, CNA B=`c6dec91f` → T=`3b43bd86`

INTERNAL AUDIT RECORD (not served). Written by the coordinator from the CNA Git objects (`git show`, `git diff`,
`git ls-tree`, `git log`) of the local clone `../cna`, the tree extracted by `scripts/extract_cna_trees.sh`
(`~/.cache/libcna-com/cna-target`, stamp = T), and read-only looks at the sibling clones `../FNA3D`, `../mojoshader`,
`../cna-avatar-assets` and `../cna-dotnet`. Nothing in CNA or any sibling repository was modified, built or run.
The local CNA checkout is on `next` at `421a38e4f`, one commit past T; nothing after T is documented.

## 0. Identity and ancestry

| Item | Value | Command |
|---|---|---|
| B | `c6dec91fbf3ef5440f60e5329e4a4758b2d80c22`, 2026-10-24 10:23:27 +0200 | `git log -1 B` |
| T | `3b43bd8687ed46523d873f9bec4b32bd8481dcb5`, 2026-10-27 17:18:11 +0100, "test(RTS-001): measure EasyGL custom 3D render-target sampling"; on `origin/next` | `git branch -r --contains T` |
| Ancestry | B is an ancestor of T | `git merge-base --is-ancestor B T` → 0 |
| Interval | **136** commits, all first-parent, 0 merges | `git rev-list --count [--first-parent|--merges] B..T` |
| Diff | **1,052** files, +17,805 / −55,092 | `git diff --shortstat B T` |
| Largest areas (files) | `modules/gamer-services` 374 (355 are the avatar catalog leaving the tree), `cmake/patches` 147, `modules/graphics` 99, `modules/renderers` 98, `tools/avatar_builder` 44, `modules/c-api` 24, `third_party/enet` 22, `modules/content` 22, `modules/content-pipeline` 20 | `git diff --name-only B T \| awk -F/ '{print $1"/"$2}' \| sort \| uniq -c` |
| Distance to the release | **948** commits after `v0.1.0` (792 first-parent, 4 merges); `git describe` = `v0.1.0-948-g3b43bd868` (B: 812) | `git rev-list --count v0.1.0..T` |
| Distance to alpha.1 | 4,657 (2,113 first-parent, 69 merges); `git diff --shortstat v0.1.0-alpha.1 T` prints 10,273 files (+1,379,094 / −1,201,657; name-status 3,058 A / 4,823 D / 2,359 M / 33 R; `--no-renames` 10,306 records; Git warns about diff.renameLimit) | |
| Distance to the release (paths) | `git diff --shortstat v0.1.0 T`: 6,383 files, +237,668 / −966,681 (587 A / 4,083 D / 1,700 M / 13 R; `--no-renames` 6,396 records); B: 6,302 | |
| Version string | `0.1.0` (`project(CNA VERSION 0.1.0)`, `CNA_VERSION_PRERELEASE ""`) | `CMakeLists.txt:3,12` |
| C ABI | **0.50.0** (`abi.h`) — unchanged | `modules/c-api/include/CNA/C/abi.h` |

What the deletions are: 355 avatar asset files (moved to a submodule, §4), 147 `cmake/patches` files (133 MojoShader +
4 FNA3D patches and two apply scripts now live as commits on the forks; two SDL Vulkan patches are upstream in the new SDL
pin; three SDL patches renamed for the new base), retired notes (`misc/`, 12 files; `plans/`, 9 files; three root campaign
handoffs) and ENet's patched 1.3.17 replaced by upstream master. None of it removed a feature.

## 1. Canonical numbers

| Fact | B `c6dec91f` | T `3b43bd86` | Method |
|---|---|---|---|
| Renderer identities / families | 10 / 8 | **10 / 8** | `check_facts.py derive_from_cna` |
| Maturity P/S/E; category N/TL/S/W/D | 3/5/2; 3/3/1/1/2 | **same** | idem |
| Compiled-effect identities / families | 8 / 6 | **8 / 6** | idem |
| Format classifiers (Texture2D; RT) | 6 fam / 8 id; 4 / 6 | **same** | idem |
| `GraphicsCapability` members | 17 | **17** | header unchanged |
| `RendererFeature` / `RendererLimit` ids | 31 / 8 | **33 / 8** (+`MultiSampleMask` 35, `RenderTargetReadback` 36; `Count` = 37) | `RendererCapabilityProfile.hpp` |
| Platform capability flags | 31 | **31** | `PlatformCapabilities.hpp` |
| Platform / audio implementations | 3 / 3 | **3 / 3** | derived |
| C++ test source files / with macros / definitions | 898 / 855 / 11,898 | **900 / 857 / 11,927** | derived |
| Standalone `examples/**/*_test.cpp` | 598 | **599** (`texture_setdata_after_draw_test.cpp` new) | derived |
| `examples/` `.cpp` (all / under `modules/`) | 694 / 693 | **695 / 694** | derived |
| CI workflow files / jobs (automatic) | 18 / 25 (16 / 22) | **unchanged** (`.github` not touched) | `git diff --stat B T -- .github` empty |
| XNA census types / members | 331 / 3,627 | **331 / 3,627** (report unchanged) | `docs/xna-4-runtime-member-coverage.md` |
| XNA oracle scenes | 39 | **39** | `tools/xna-oracle/scenes/*.scene` |
| XNB built-in readers | 61 (60) | **61 (60)**; `modules/content/src/Xnb` unchanged | |
| C ABI / headers / declared routes | 0.50.0 / 60 / 3,212 | **0.50.0 / 60 / 3,212** | derived |
| ABI baseline structs / integer / float constants | 196 / 1,476 / 11 | **196 / 1,478 / 11** | `tools/c-api/abi_baseline.json` |
| C ABI release gate (public C++ declarations) | Not ready: 8,125 = 7,032 impl / 15 partial / 625 planned / 453 n/a; 466 headers, 406 excluded | **Not ready: 8,134 = 7,033 / 15 / 633 / 453**; 466 / 406 | `docs/c-api/COVERAGE.md`, `RELEASE_GATE.md` (graphics +3 symbols, math +6: the XmlSerializer hooks and the new features, planned under CBIND-127) |
| Avatar catalog | v3 **revision 4**, 359 files, in-tree | v3 **revision 5**, 359 files, 45,960,930 bytes, submodule `cna-avatar-assets` `4617a1e7503f` | `catalog.json` |
| CNA.NET consumer ABI | exactly 0.47.0 | **exactly 0.47.0** (local `develop` still `90b11a2`) — does not consume T | `eng/cna-native-abi-policy.json` |

## 2. Third-party dependencies

### 2.1 FNA3D and MojoShader: CNA's forks (`81ab03e72`, `8b5564f1e`, `13d0ed91a`, then the audit pins)

* `cmake/ThirdPartyFNA3D.cmake`: `cna_fna3d_select_source_pin(DEFAULT_REPOSITORY "https://github.com/libcna/FNA3D.git"
  DEFAULT_TAG "10f650b9d0f6bb0e6f3f9378833fbd807dfe8cde")`; FetchContent `GIT_SUBMODULES_RECURSE TRUE`, `EXCLUDE_FROM_ALL`,
  `GIT_SHALLOW FALSE`; cache variables `CNA_FNA3D_GIT_REPOSITORY`, `CNA_FNA3D_GIT_TAG`. `RendererSelection.cmake` status line
  "libcna/FNA3D + MojoShader forks".
* Verified in `../FNA3D` (remotes: origin libcna/FNA3D, upstream FNA-XNA/FNA3D): `10f650b9d0f6` = 2026-10-26 "D3D11: a Depth
  vertex element is the input-layout semantic DEPTH", on `origin/cna`; upstream release tags `26.08` (`32401479a3ab`) and
  `26.10` (`62a41708e975`) are ancestors; 53 non-merge commits after 26.10 on the fork. Its `MojoShader` gitlink =
  `03b686fe1a33863a61fa153d6d33c3b6eafa514d`.
* Verified in `../mojoshader` (origin libcna/mojoshader, upstream icculus/mojoshader): `03b686fe1a33` = 2026-10-26
  "hlsl: a DEPTH vertex input is the input-layout semantic DEPTH<n>", on `origin/cna`; upstream `6333f74` and `ad5dff8` (the
  revision FNA3D 26.10 pins) are ancestors.
* Why forks (`docs/fna3d-renderer.md` "The two forks"): to carry CNA's fixes as ordinary commits on a `cna` branch; the
  default branches mirror upstream; upstream accepts no AI-written code, so the fixes are not offered there. Both are linked
  **statically only**: they add entry points (`FNA3D_SetXnaPixelCenterEXT`, `FNA3D_SetLegacyBumpMapEnvEXT`,
  `MOJOSHADER_glProgram*Info`, `MOJOSHADER_sdl*` hooks), render-state values and struct fields, so neither is ABI-compatible with
  an upstream shared library. Before the upstream merges, every source file is identical to what the former patch series
  (137 files under `cmake/patches/`) produced from FNA3D `3240147` and MojoShader `6333f74`. MojoShader `cna`: 133 commits, each
  naming its former patch in a `CNA-Patch:` trailer; audit fixes carry `CNA-Audit-Finding:` trailers; regression suites in
  `tests/cna` (`-DMOJOSHADER_CNA_TESTS=ON` / `-DFNA3D_CNA_TESTS=ON`).
* Following upstream: merge (never rebase) upstream's default branch or a release tag into `cna`; push MojoShader first,
  commit its gitlink in FNA3D, push FNA3D, then move `CNA_FNA3D_GIT_TAG`; a pin is always a full SHA.
* Pin selection (`cmake/Fna3dSourcePin.cmake`): repository and tag move as one pair; a tree's CNA defaults follow the current
  pin, a developer's own value is never replaced (provenance recorded in `_CNA_FNA3D_GIT_*_ORIGIN`); a developer value next to
  an obsolete CNA default is refused; upstream FNA-XNA/FNA3D with CNA's default commit is refused (the commit exists only in
  the fork); any non-default pair is warned about on every configure; no network access.
* Source check (`cmake/Fna3dSourceCheck.cmake`), every configure, read-only: FNA3D HEAD vs the pin, MojoShader HEAD vs FNA3D's
  gitlink, local changes in either. FetchContent-populated checkout: mismatch = **error** unless
  `CNA_FNA3D_ALLOW_SOURCE_DRIFT=ON` (warning). `FETCHCONTENT_SOURCE_DIR_FNA3D` checkout: findings are warnings (built as it is;
  that is how a fork change is tried before the pin moves). Missing MojoShader submodule: error in both.
* `BUILD_SHARED_LIBS`: FNA3D is forced static during the fetch and the caller's variable/cache entry restored exactly (C-07).
  FNA3D's directory is `EXCLUDE_FROM_ALL` on every supported CMake (C-06; CMake 3.20 minimum).
* Installed C++ SDK (`cmake/InstallCxxDependencies.cmake`, C-02): `cna_cpp_sdk` bundles FNA3D only when the FNA3D renderer
  links it (or `cna_mojoshader` links FNA3D); an SDL-free compiled-effect configuration no longer compiles FNA3D.
* Old trees: one whose `_deps/fna3d-src` still holds the former configure-time patches stops; delete `_deps/fna3d-*`.
* Offline: `-DFETCHCONTENT_SOURCE_DIR_FNA3D=<clone of the fork at the pin, MojoShader submodule initialized>`.

### 2.2 SDL, SDL_shadercross, vendored-source check

* `third_party/SDL` gitlink `cbe3fbe9` → **`86296ac8f01597076979630667472a846b04ce46`** (SDL main 2026-05-15): the first
  upstream commit with both Vulkan GPU fixes CNA carried as patches (`f286e420` defrag barriers, `86296ac8` swapchain fields).
* Five CNA patches (`cmake/ThirdPartySDL.cmake`), applied in order to a staged copy, never to `third_party/SDL`, each only where
  needed: `sdl-86296ac8-0001-emscripten-filedrop-rmdir`, `-0002-emscripten-commit-proxied-frame` (Emscripten),
  `-0003-uikit-scene-window-frame` (iOS), `-0004-android-relative-asset-enumeration` (Android; C-05: a relative directory that
  exists only in the APK's assets enumerates again — "an Android build has not been run with it yet", `8cef3c2d0`),
  `-0005-vulkan-mipmap-level-extent` (where the Vulkan backend is built: Linux, Windows, Android; clamps each mip level's blit
  extent to one texel, `32db01834`). macOS: SDL exactly as upstream ships it.
* SDL_shadercross: one build-integration patch (`sdl-shadercross-1ff05bec-disable-unused-export.patch`, guards an export with
  `SDLSHADERCROSS_INSTALL`), applied only to the clone FetchContent made for the build tree or to a staged copy of a
  `FETCHCONTENT_SOURCE_DIR_CNA_SDL_SHADERCROSS_SOURCE` checkout; success verified from the post-image (C-04).
* `CNA_VENDORED_SOURCE_CHECK` (ON default / WARN / OFF; `cmake/VendoredSourceCheck.cmake`, `cmake/VendoredSources.cmake`):
  `third_party/SDL` and `third_party/SDL_mixer` must be the pinned revisions; a stale submodule stops configure with the repair;
  a source archive is checked by tree id; on Windows a mode-only mismatch is a warning; without git only a STATUS line (C-03).
* Persistent SDL prebuilt: the manifest now records the toolchain file and the settings it decides (evaluated in `cmake -P`);
  an edited toolchain rebuilds SDL (`55ed86cf0`); each build tree watches the install record and reconfigures when another tree
  rebuilt it (C-08, `ef6cc0f2e`). Limitation (handoff §5.2): a shared prebuilt can still change under a **running** build when a
  tree with another manifest rebuilds it — give such a tree its own `CNA_SDL_PREBUILT_ROOT`.

### 2.3 ENet (`c59a91c00`)

`third_party/enet` (a committed directory, not a submodule, before and after) = upstream `lsalzman/enet` master
`5a9c537fd464b3c6d3c55e1d3bd47588faf71b42` (2026-06-23; ENet 1.3.18 and later fixes), unmodified except that upstream's
`.github/` and `.gitignore` are left out. Release tags still shift a signed 1 into bit 31 (UB); master shifts unsigned, checked
under UBSan by `modules/net/tests/enet_*_test.c` (`enet_fragment_bitmap_test.c` new). B had a patched tree with
`CNA_PATCHES.md`; gone. CNA links ENet statically (`BUILD_SHARED_LIBS OFF` in `cna_configure_vendored_enet`).

### 2.4 Clone instructions (`docs/development-environment.md` at T)

`git clone --recurse-submodules https://github.com/libcna/cna.git`; an existing clone, and after a pull that moves a submodule:
`git submodule update --init` (the doc adds `--recursive` as an alternative but says plain `--init` is enough and much faster:
the recursive form also clones SDL_mixer's codec submodules and Draco's test dependencies, which CNA builds none of). Submodules:
`third_party/SDL`, `third_party/SDL_mixer`, `third_party/draco`, `vendor/googletest`, and now
`modules/gamer-services/assets/avatars`. ENet, cgltf, stb, dr_libs are committed.

## 3. Graphics and renderers

| Change | Commit(s) | Scope and evidence (recorded by CNA) | Limits that remain |
|---|---|---|---|
| Texture upload after queued draws that sample it; `SpriteSortMode::Immediate` per-call | `d9b513ee0`, `96577db26` | SDL_GPU submits queued work first (Texture2D/Cube/3D); WEBGPU writes a fresh texture (2D, Cube, 3D). `spritebatch_sort_mode_semantics` leg B asserts XNA's red/blue on SDL_GPU, WEBGPU, OPENGLES3, OPENGL33, SOFTWARE, FNA3D; new conformance `texture_setdata_after_draw` (2D via BasicEffect, Cube via EnvironmentMapEffect) passes both legs on SDL_GPU, WEBGPU, OPENGLES3, OPENGL33, SOFTWARE | FNA3D fails leg B of `texture_setdata_after_draw`: its SDL_GPU driver uploads ahead of the frame's draws and cycles only a whole single-level 2D texture (TextureCube; by source also Texture3D and mipmapped Texture2D). handoff §5.3, `docs/fna3d-renderer.md` "Texture upload ordering" |
| Cube faces in MRT sets on SDL_GPU (DC-R1) | `51fb39d5a` | binds a `RenderTargetCube` face in any slot; `cube_mrt_binding` M1–M4 pass on SDL_GPU | WEBGPU and DIRECTX9 refuse cube faces in an MRT set (`NotSupportedException`) while `MultipleRenderTargets` is true; HEADLESS accepts |
| `MultiSampleMask` on SDL_GPU (DC-R2) | `c7f6c68e5` | all-or-none: keeping every sample draws, none drops the draw, partial throws `NotSupportedException`; single-sample targets ignore the mask (XNA). `RendererFeature::MultiSampleMask`: Restricted SDL_GPU; Supported EasyGL (where the context has `glSampleMaski`), WEBGPU, SOFTWARE, DIRECTX9; FNA3D Supported on its OpenGL driver only; Unsupported default (HEADLESS, STUB) | pinned SDL reserves `sample_mask` |
| `RendererFeature::RenderTargetReadback` (36) | `e357bc4c4` | `ReadsBackRenderTargetsEXT`: Supported SOFTWARE, EasyGL, WEBGPU, SDL_GPU, FNA3D, DIRECTX9; Unsupported HEADLESS, STUB (GetData on a render target throws `NotSupportedException`) | |
| Non-Color `RenderTargetCube` readback | `87449873e` | SDL_GPU and WEBGPU read float/other formats back; WEBGPU refuses when the cube fell back to the swap-chain format | |
| XNA integer pixel centres on multisampled targets | `baf453c9c` (+fork `74698f7`) | measured on XNA 4.0 via DXVK (`spikes/xna-msaa-pixel-center-spike`); all renderers incl. FNA3D drivers; `XnaMultisamplePixelCenterTest` | bias is 63/128 px (handoff §5.2); lines/points keep host centres, XNA's MSAA behaviour for them unmeasured |
| SDL_GPU per-pixel lit vertex colour × `EmissiveColor` | `129398956` | XNA formula `vc * (light * Diffuse + Emissive)`; parity columns on EasyGL, WEBGPU, SDL_GPU | |
| EasyGL absent vertex colour = white | `17cd5d3c3` | fixes a PbrEffect stride-48 draw with `VertexColorEnabledEXT` on and no colour element that came out black since `bb6a2f44e` (2026-10-22, before B — so B had this regression; the fix is in the interval) | |
| FNA3D double-sided PBR VFACE sign | `9852ba0b6` | every FNA3D driver hands Direct3D 9's clockwise-positive VFACE | |
| FNA3D bump environment | `725481a1e` | `BUMPENVMAT/LSCALE/LOFFSET` forwarded via `FNA3D_SetLegacyBumpMapEnvEXT`; contract passes on OpenGL driver incl. BEM; SDL_GPU driver TEXBEM/TEXBEML | MojoShader SPIR-V refuses ps_1_4 `BEM` and `TEXDEPTH` by name (FNA3D's SDL_GPU driver, CNA's SDL_GPU and WEBGPU compiled effects); GLSL implements both |
| Effect struct defaults = XNA 4.0 | `c71eeb6e8` | measured with XNA's own pipeline (`tests/reference/xna40/effect-struct-defaults/`) | |
| Tests that ask the selected renderer (T01–T32, AVH-07) | several | test-harness changes; no renderer behaviour | |
| `PresentationParameters` defaults = XNA | `e460e0ed6` | `new PresentationParameters()`: 0x0 back buffer, `IsFullScreen = true`; CNAEXT `CreateWindowedEXT(w, h)`; `GraphicsDevice()`, a `Game` without a device service (every C API game) and `GraphicsDeviceManager` unchanged in effect (800x480 windowed) | consumers building a device from the default must state a size |
| Readable refused vertex type | `a80534927` | error message names the type | |

handoff §5.2 limitations at T that are new or changed since B (all **recorded by CNA**): SDL_GPU MultiSampleMask all-or-none;
native `SurfaceFormat::Alpha8` render-target storage unavailable on every renderer (falls back to Color); FNA3D refuses a
`PbrEffect`/`SkinnedPbrEffect` draw without `TANGENT0` on its SDL_GPU and Direct3D 11 drivers (`FNA3D-MISSING-STOCK-INPUT`;
OpenGL driver and every other renderer supply a neutral tangent; measured 2026-10-25); pixel-centre bias 63/128; lines/points
pixel centres; MojoShader SPIR-V gaps (BEM, TEXDEPTH); MojoShader FOG lanes (GLSL ES/Metal place FOG positionally; vs_3_0 PSIZE
narrowed to x; HLSL refuses FOG/SAMPLE/TESSFACTOR vertex inputs; ARB1 FOG/PSIZE names; Vulkan pipeline creation and GL link of FOG
pairs not run); FNA3D OpenGL ES 3 readback (RGBA8, ColorSrgbEXT, float formats, others only where the implementation's read
layout is the format's; Mesa 25.0.7 radeonsi reads Rgba1010102, Rgba64, ByteEXT, UShortEXT; refuses Rg32 and ColorBgraEXT);
FNA3D pixel-store save/restore (six `glGetIntegerv` per upload, sync points under glthread); FNA3D tracing with several devices;
MojoShader's D3D11 glue (ps_3_0 register packing to separate VS registers fails to compile, R9-01; integer input-layout rewrite
matches semantics by substring, `DEPTH1` vs `DEPTH10`, R9-03; CNA's committed effects contain neither); SDL_shadercross
initialization is the application's in a standalone FNA3D build (CNA's SDL_GPU renderer does it); shared SDL prebuilt under a
running build. §5.3: FNA3D TextureCube upload ordering; WEBGPU and DIRECTX9 cube faces in MRT; SDL LeakSanitizer leaks (~50 KB);
the fork leaks measured on 2026-10-22/23 are fixed on the forks; DIRECTX9/DXVK 2.6.0 teardown (unchanged).

Unchanged and still stated by CNA: SDL_GPU is the Windows/macOS/iOS default but **not qualified** there (Linux/Vulkan and
Direct3D 12 under Wine only; never built for iOS; `ShaderEffect` compiled out on Windows, Apple and the browser; no occlusion
queries); WEBGPU verified on Linux x86_64 and headless Chrome only; iOS simulator smoke with SOFTWARE only; DIRECTX9 under
Wine+DXVK only.

## 4. Avatars (AVA-01..10, AVH-01..08, `56d5d8202`)

* Catalog v3 **revision 5** (`87466fb53`): ear shapes name their `lobes`, so earrings hang from the lobe of the shape worn
  (they keep the first shape's tilt on the others); trousers and skirts stay under the top in the deepest crouch (residual:
  at most 16 vertices of a top's covered waist over jeans/shorts/joggers and 21 over a skirt, pinned by
  `TheTrousersStayUnderTheTopInTheDeepestCrouch`); hair any hat passes through or over is hidden, not stretched (`60a06d039`;
  residual ragged edge under a brim from behind, e.g. afro under a bucket hat); planted-foot drift measured and pinned
  (`PlantedFeetDriftOnlyAsFarAsTheRootMotionAllows`): exact only on the body a preset was solved on; up to 7 mm on the other
  body at its authored height, up to 3 cm at the extremes in FemaleIdleFixShoe, Celebrate, MaleSurprised.
* Packaging: submodule `modules/gamer-services/assets/avatars` → `https://github.com/libcna/cna-avatar-assets`, CNA records
  `4617a1e7503ffc243fb898683c1dc22ae8163459` ("Import avatar catalog v3 revision 5 from CNA", 2026-10-25). Verified locally:
  its `v3/` tree is byte-identical to CNA `bdaeaff01`'s in-tree `v3/`; `catalog.json`: catalogVersion 3, revision 5, reader 2,
  rig `cna-avatar-71`, 358 listed assets + catalog.json = 359 files, 45,960,930 bytes. Licence: Ms-PL, CNA's own; original CNA
  content generated by `tools/avatar_builder/generate_avatar_catalog.py`. CHANGELOG [Unreleased]: "Catalog v3 revision 5 is byte
  for byte the same, and so is everything built from it" (no runtime/serialization change from the move).
* Build: `modules/gamer-services/CMakeLists.txt` **FATAL_ERROR** when the submodule directory is empty ("Run: git submodule update
  --init modules/gamer-services/assets/avatars"; "A source archive (git archive, a GitHub ZIP) contains no submodules: clone with
  Git instead. A build without GamerServices (CNA_ENABLE_GAMER_SERVICES=OFF) does not need the catalogs."); a submodule off its
  recorded commit without `v3/catalog.json` also fails. New CTest `GamerServices_AvatarAcceptanceStatic` (labels avatar,
  configuration).
* Footprint and timing (docs/avatars.md, recorded by CNA, Debug): library `cna_gamerservices_avatar_catalog` 22.3 MB deflated
  (46.0 MB of files), linked only by programs that use avatars; first avatar of a process ~370–410 ms, next ~140–210 ms, an
  avatar still drawn reused in ~0.3 ms; caches release an avatar and its textures once nothing draws it; parsed catalog models
  kept for reuse, at most 96. Revision 5's service manifest is 191 KB (message limit 64 KiB, so it is read by hash from the file
  route).
* Tests: checked-in visual regression `tools/avatar_builder/regression/` (36 views of nine described avatars and three
  `CreateRandom` avatars, goldens on SOFTWARE; `GamerServices_AvatarVisualRegression`); `scripts/avatar_visual_regression_check.py`
  removed; one acceptance command `tools/avatar_builder/avatar_acceptance.py <tree> [--all-renderers] [--service …]`.
  Recorded by CNA: at revision 5, 2026-10-25 at `ac20344ef` (AVH-08), acceptance passed on all eight renderers compiled in (233
  avatar tests each; one skip by design, three on STUB) and the 36-view regression on the six that draw. Not repeated for
  revision 5 on Windows translation layers; no native Windows/macOS evidence.
* Guide on a renderer with no render targets draws no avatar picture instead of throwing (`7f599008e`).

## 5. Content pipeline and formats

* `XmlSerializationEXT.hpp`: `XmlSerializer<Color>` (R, G, B, A, PackedValue), `<Rectangle>` (X, Y, Width, Height, then Location as
  a nested Point), `<Point>` (X, Y); reading follows document order (a later PackedValue/Location overrides), measured against
  genuine XNA 4.0 under Wine (`bbed8c61e`; needs sharp-runtime `f990d074`, property members).
* Generated nested names (`98aa655f2`, `419723275`): XNA's `stub_N` smallest free index across the whole build in node order,
  any worker count, incremental builds; explicit-name and path clashes still refused.
* `BuildAndLoadAsset<TextureContent, TextureContent>(…, "TextureProcessor")` answered by CNA's XNA-shaped TextureImporter and
  TextureProcessor in process (`671d8478e`); other requests keep the canonical route; `BuildAsset` unchanged.
* `889a31be4`: `ContentProcessorContext.Convert` (ArgumentNullException / InvalidOperationException before the processor runs),
  `AddDependency` refusal as PipelineException, `MaterialProcessor` InvalidContentException for a material without Effect,
  `BoneWeightCollection.NormalizeWeights` drops weights ≤ 0 and scales by one reciprocal, plus items 11 and 12 (read the commit).
  `48a5c75eb` TaskItem equality callable; `626de40e6` content tasks name the library they need.
* `30afa280b` bumps the glTF Model pipeline component versions (existing content builds recompile).
* `ContentTypeSerializerAttribute.hpp` (new header), `PipelineComponentScanner` changes, `VertexCollections` — read diffs.
* Formats: XNB, CNB, CNJ unchanged in behaviour. New/consolidated documents: `docs/cnj-format.md` (the .cnj specification,
  from `misc/cnj.md`), `docs/model-content-pipeline-support.md` (today's Model loaders), `docs/content-pipeline.md`,
  `docs/xnb-content-pipeline-support.md` (minor edits).

## 6. C API (ABI 0.50.0 unchanged)

* `cna_shader_effect_create` (`9ef292993`, DC-R3): a view of whole 32-bit words, ≥ 5-word header, starting with the SPIR-V magic
  is copied byte for byte; others validated as UTF-8 text (refused with `CNA_RESULT_ENCODING`). Getters copy bytes.
* `effects.h` (`f31dbf4e6`): the three texture-binding routes document WEBGPU's refusal of a cube sampler on its WGSL contract
  (`CNA_RESULT_NOT_SUPPORTED`).
* `graphics.h`: `CNA_RENDERER_FEATURE_MULTI_SAMPLE_MASK` 35, `_RENDER_TARGET_READBACK` 36, `_MAXIMUM` 36 (`@since ABI 0.50.0`);
  `graphics_state.h`: comment that C `MAX`/`MIN` keep 3/4 while C++ uses XNA's Min = 3, Max = 4, converted by name.
* `cna_presentation_parameters_init`: XNA's values (0x0, full screen); C smokes set `is_full_screen`.
* Input text routes: XNA's MouseState/GamePadState text; the generated gamepad text route now formats the caller's snapshot.
* `docs/c-api/ABI_VERSIONING.md`: a `0.x` consumer must also reject a minor it was not written against (any 0.x minor may
  break); the installed package's `SameMajorVersion` accepts every later `0.x`; `hello_cna.c` shows the runtime check.
* Release gate figures in §1. `docs/binding.md` (new): one C ABI for every language, boundary rules, Sharp Runtime's place, how
  to design/package/test a binding, when a binding counts as maintained, what CNA.NET may claim; distinguishes a game's
  GraphicsDevice from a standalone one.

## 7. Other

* Input: `MouseState.ToString()` `{X:10 Y:20 Buttons:Left Wheel:120}` (buttons in Left, Right, Middle, XButton1, XButton2 order or
  `None`), `GamePadState.ToString()` `{IsConnected:True|False}` (`0ef875619`).
* Net: unsigned ENet fragment bitmap masks (`03b92269c`), now upstream.
* Android: relative APK-only directory enumeration restored by SDL patch 0004 (not run on Android).
* `docs/consoles.md` (new): human rewrite of the console feasibility analysis — **not** console support. `docs/location-proposal.md`
  (new): a proposal for `System.Device.Location`-style location with the owner's six decisions of 2026-10-25 — **not implemented**.

## 8. Recorded evidence at T (handoff; nothing re-run here)

* Latest complete cross-subsystem checkpoint 2026-10-24 at `96577db26`: `cmake-build-multi` full CTest 12,553 of 12,569 passed;
  the 16 others pass with their renderer selected / without the dummy audio driver. cna-demos 719-ID sweeps SOFTWARE 671/0/45/3,
  OPENGLES3 709/0/7/3; serial CTest 732 enabled, 687 PASS/45 SKIP/0 FAIL/3 disabled.
* At the FNA3D pin `10f650b9d0f6` (2026-10-26): `CnaTests` with the audit's graphics filter 1,683 tests, no failure on each of
  OPENGLES3, OPENGL33, WEBGPU, SOFTWARE, SDL_GPU (Vulkan) and FNA3D (OpenGL and SDL_GPU drivers); network 574/574; platform
  1,553 on X11 and on Wayland. Fork suites: MojoShader `tests/cna` 16/16 (also ASan+UBSan+LSan); FNA3D `tests/cna` 21 (27 with
  tracing) under ASan+UBSan on OpenGL, GLES3, SDL_GPU, and eight executables on D3D11 under Wine/DXVK 3.1.1. MinGW under Wine:
  `DirectX9CompiledEffect*` 31/32 (one declared skip), pixel-centre/readback 5/6. Emscripten `cna_webgpu_compiled_effect_page`
  21/21 headless Chrome. Android not rebuilt at this pin.
* CNA-DEMOS campaign (`CNA_DEMOS_REPAIR_MATRIX.json`): 156 historical IDs, 156 final dispositions: 119 FIXED_VALIDATED, 23
  DOCUMENTATION_CORRECTED, 8 ALREADY_FIXED, 3 FIXED_PLATFORM_VALIDATION_PENDING (003, 101, 152: need native Windows/XNA), 1
  DEMO_EXPECTATION_BUG, 1 DUPLICATE_ROOT_CAUSE, 1 UNSUPPORTED_CONTRACT_CORRECTED; DC-R1 FIXED_VALIDATED, DC-R2
  UNSUPPORTED_CONTRACT_CORRECTED, DC-R3 FIXED_VALIDATED. The nine findings that Phase 6 described as "fix committed, closure not
  validated" (005, 006, 007, 008, 022, 023, 031, 066, 067) were **closed on a complete checkpoint** (`6c8b042c4`, batch 9,
  2026-10-24).

## 9. Deleted or moved CNA documents and files → current successor at T

| Gone at T | Successor (exists at T) | Note |
|---|---|---|
| `misc/cnj.md` | `docs/cnj-format.md` | the .cnj specification (`738b6240f`, `bf6928e68`) |
| `misc/cnb.md` | `docs/cnb-format.md` (goals/non-goals), `plans/plan_cnb.md` | retired (`fcd640e20`) |
| `misc/xnb.md` | `plans/plan_xnb.md`, `docs/xnb-content-pipeline-support.md` | retired: its plan was carried out (`cc8a9d84a`) |
| `misc/cnaplatform.md` | `docs/platform-abstraction.md`, `plans/plan_platform.md` | retired (`6993c3127`) |
| `misc/cnaconsoles.md` | `docs/consoles.md` | rewritten; not console support (`bd35db7ba`) |
| `misc/location_sensor.md` | `docs/location-proposal.md` | proposal, not implemented (`e27534501`, `f0aa07e12`) |
| `misc/analysis_binding*.md` (3) | `docs/binding.md` | (`6c59a47c4`, `c47fde6e4`, `0e737cf3b`) |
| `misc/cnacomp.md`, `plans/plan_compilation.md` | `docs/build-performance.md` | (`4b298db69`, `78afd08ab`) |
| `misc/gltfissues.md` | `docs/gltf-limitations.md`, `plans/plan_gltf.md` | findings closed (GLTF-450) |
| `misc/000036_*` | — | done backlog task |
| `plans/plan.md` | — | three tasks done (`91ea1d315`) |
| `plans/plan_graphics.md` | — (rows done/withdrawn/superseded; shared contracts in `plans/plan_graphics_shared_cleanup.md`) | `f279a845e` |
| `plans/plan_missing.md` | `docs/xna-4-runtime-member-coverage.md` | XNA-MISSING closed 3,627/3,627 |
| `plans/plan_xna_runtime_surface.md` | `docs/xna-4-enumerator-reference.md`, `docs/xna-4-runtime-member-coverage-baseline.md` | |
| `plans/plan_modern_retirement.md` | `docs/c-api/ABI_VERSIONING.md`, `docs/renderer-capability-profiles.md` | MRT-001..012 done |
| `plans/plan_vulkan_parity.md` | `plans/plan_graphics_shared_cleanup.md`, `plans/plan_gpu_test_isolation.md`, `docs/build-performance.md` | |
| `plans/plan_sdl3free.md` | `docs/platform-abstraction.md` | superseded |
| `CNA_DEMOS_REPAIR_HANDOFF.md`, `CNA_INHERITED_REVIEW.md`, `CNA_MUSEUM_REPAIR_HANDOFF.md` | `handoff.md` §0, `CNA_DEMOS_REPAIR_MATRIX.json`; Git history | removed |
| `scripts/avatar_visual_regression_check.py` | `tools/avatar_builder/avatar_visual_regression.py` | |
| `third_party/enet/CNA_PATCHES.md` | `cmake/ThirdPartyENet.cmake` header | ENet now unmodified upstream |
| `cmake/patches/fna3d-*`, `mojoshader-*`, `apply-fna3d-*.cmake` | commits on libcna/FNA3D and libcna/mojoshader `cna` | |
| `cmake/patches/sdl-cbe3fbe9-000{1,2}-vulkan-*` | upstream in SDL `86296ac8` | |
| `cmake/patches/sdl-cbe3fbe9-000{3,4,5}-*` | `cmake/patches/sdl-86296ac8-000{1,2,3}-*` | renamed for the new base |

A historical citation of a deleted file stays legal when it is pinned to a commit where the file exists and the sentence says so
(e.g. "`misc/cnj.md` at `c6dec91f`").
