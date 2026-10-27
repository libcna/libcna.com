# R4 — Development area review, CNA `c6dec91f` → `3b43bd86`

INTERNAL AUDIT RECORD (not served). Written by the Development reviewer of Phase 7. Scope: every `development/` row of
`worklist.json` with `status: "review"` except the five generated reference pages and the two pages the coordinator had
already reviewed (`development/maintenance.html`, `development/handbook/update-libcna-com.html`): **85 pages**. Nothing in
CNA or any sibling repository was modified, built or run; no generator or sync script was run; nothing was committed.

## 1. Method

* **Reading CNA.** Git objects only: `git -C ../cna show|diff|log|grep|ls-tree|rev-list|cat-file` at `c6dec91f` (B) and
  `3b43bd86` (T). The working tree of `../cna` (one commit past T) was never read.
* **Per page.** The diff of every file in the row's `changed_files` was read (diffs saved per file) and mapped to the
  sentences that cite the file; every `topics` hit was read in context; in addition every scoped page was scanned for the
  interval topics of the editorial guide §3 (PresentationParameters/800×480/`GraphicsDevice()`, `RendererFeature` counts,
  `MultiSampleMask`, readback, upload ordering/Immediate, cube faces in MRT sets, pixel centres, VFACE, bump environment,
  struct defaults, `MouseState`/`GamePadState` text, `cna_shader_effect_create`, 0.x consumer rule, release-gate figures,
  nested names, `BuildAndLoadAsset`, Workshop semantics, forks/patches/ENet/SDL pin/submodules/avatars, deleted `misc/` and
  `plans/` files, handoff/repair files, test counts). Sentences were corrected only where T contradicts them or the interval
  made them misleading; a few pre-existing errors found while verifying (not interval changes) were corrected too and are
  marked as such below.
* **Counts.** Every figure a page states as computed from the tree or history was recomputed at T with the method the page
  states; in each case the same script reproduced the page's c6dec91f figure exactly before it was run at T (exceptions:
  none). Methods used: `git ls-tree -r --name-only <rev> <dir> | wc -l` (directory counts); `.cpp` under `tests/` or
  `test/`, vendored excluded (test-source distribution); line-anchored `^\s*(TEST|TEST_F|TEST_P)\(` scans (module test
  definitions); lines of `include/` + `src/` (module sizes); `git rev-list --count`, `--first-parent`, `--merges`;
  `git cat-file --batch` for `gpgsig` headers (and `-----BEGIN SSH SIGNATURE`); subject regexes
  `^[a-z]+(\([^)]*\))?!?:` (type(scope), reproduces 4,134), `\(Tasks? ` (reproduces 895), `\b[A-Z][A-Z0-9]*-[0-9]+`
  (reproduces 3,622); `git grep -o 'plans/plan_[A-Za-z0-9_]+\.md'` over modules/cmake/scripts/tools/tests/examples
  (reproduces 1,651 / 4,736 / 70 / 412 / 29); the generator's own `TARGET_RE` scan (generated test-target count, reproduces
  238); `tools/count_webgpu_plan_status.sh` (plan_webgpu rows).
* **Snapshot labels.** On a page whose review was finished, the dev-evidence callout SHA (wording unchanged), the doc-meta
  line, meta descriptions and every inline label of the documented snapshot moved to `3b43bd86`; statements of what was done
  at an earlier commit ("re-read at c6dec91f", "re-read at c1c316b9") were kept as history. Dates next to a moved label
  became 27 October 2026.
* **c1c316b9 pages.** The 16 stated-evidence pages in scope keep `c1c316b9` in their callout (none was re-verified in full).
  Their doc-meta line ("CNA snapshot … · source links pinned to …") was moved to `3b43bd86`, because their source links are
  pinned to `3b43bd86` (coordinator's repin) and Phase 6 likewise gave c1c316b9 pages the then-current pin in that line;
  pin references in instructions (investigation.html's "The Development pages are pinned to …" and its `git` examples,
  workflows.html's `git grep` example) were moved for the same reason. Interval-contradicted sentences on them were fixed.

## 2. Per page

- development/architecture/bindings.html: no prose change. ABI_VERSIONING.md (0.x consumer rule, two constants added at 0.50.0), COVERAGE.md (8,134/633), OWNERSHIP.md (callback registration detach), abi_baseline.json (+2 constants) read; no sentence contradicted (page says 'exact, not stable', 'new constants', no counts). MOVED.
- development/architecture/content.html: no prose change; Game.cpp diff is only CreateGameGraphicsDevice (not described here); content-pipeline interval changes (nested names, BuildAndLoadAsset, Workshop) do not touch the map's statements. MOVED.
- development/architecture/graphics.html: #construction: Game's device is built from `PresentationParameters::CreateWindowedEXT(DefaultBackBufferWidth, DefaultBackBufferHeight)` + Depth24 (Game.cpp CreateGameGraphicsDevice, e460e0ed6), not 'default PresentationParameters' (now XNA's 0x0 full-screen). Rest unchanged (device-loss callback users unchanged in modules/renderers diff). MOVED.
- development/architecture/overview.html: no prose change (RendererSelection.cmake: FNA3D status line only; IPlatform.hpp: comment now cites docs/platform-abstraction.md). MOVED.
- development/architecture/platform.html: '31 flags at c6dec91f' recomputed at 3b43bd86 (PlatformCapabilities.hpp byte-identical) and relabelled; docs/platform-abstraction.md gained a 'contract describes what CNA needs' rule, plan_platform.md/sdl_classify.py comment-only; nothing contradicted. MOVED.
- development/architecture/runtime.html: construction tree: device parameters are `PresentationParameters::CreateWindowedEXT(800, 480)` with Depth24 (Game.cpp CreateGameGraphicsDevice at 3b43bd86), not 'default PresentationParameters'. MOVED.
- development/build/architecture.html: coordinator's dependency corrections (forks, SDL 86296ac8 + five patches, ENet, source checks, toolchain-aware manifest, mechanisms callout) checked against cmake/ThirdPartyFNA3D.cmake, Fna3dSourcePin/Check.cmake, ThirdPartySDL.cmake, SdlPrebuiltFingerprint.cmake, VendoredSourceCheck.cmake at 3b43bd86 and kept. Added: a "Dependency source checks" row in the configure-gate table (VendoredSourceCheck.cmake / Fna3dSourceCheck.cmake, CNA_VENDORED_SOURCE_CHECK, CNA_FNA3D_ALLOW_SOURCE_DRIFT); the CnaSdlPrebuiltFingerprint description now includes the native-manifest and stamp-watch cases (cmake/Tests/SdlPrebuiltFingerprint.cmake cases 17, 18 at 3b43bd86); generated test-target count 238 -> 248 (same TARGET_RE scan as generate_dev_reference.py over the 3b43bd86 tree: +CnaENetFragmentTests exe/test, CnaFna3dSourcePin, CnaFna3dSourceCheck, CnaFna3dDependencyShape, CnaCxxSdkDependencies, CnaVendoredSourceCheck, CnaSdlShadercrossPatch, CnaSdlAndroidAssetEnumeration, GamerServices_AvatarAcceptanceStatic). MOVED.
- development/build/index.html: prerequisites "Submodules" now lists the avatar-catalog submodule modules/gamer-services/assets/avatars (FATAL_ERROR in modules/gamer-services/CMakeLists.txt at 3b43bd86 when empty; not needed with CNA_ENABLE_GAMER_SERVICES=OFF; source archives carry no submodules) and the stale-submodule refusal (cmake/VendoredSourceCheck.cmake, CNA_VENDORED_SOURCE_CHECK default ON). Rebuild table: compiled-effects toggle fetches CNA's FNA3D/MojoShader forks at the pin; a drifted fetched checkout stops unless CNA_FNA3D_ALLOW_SOURCE_DRIFT=ON (cmake/ThirdPartyFNA3D.cmake, Fna3dSourceCheck.cmake). build-performance.md diff (8-job guidance, ccache/benchmark rules) touches nothing the page states. MOVED.
- development/debugging.html: no prose change (GraphicsDevice.cpp: GraphicsDevice() default + two feature rows, not described here; RendererSelection.cmake status line; profile_dead_tests.py comment; ENet now upstream but still vendored and outside CNA_SANITIZE, as stated). MOVED.
- development/getting-started.html: snapshot paragraph now names 3b43bd8687ed… (27 October 2026; 948 already set by the coordinator), the ancestry commands use the new full SHA; no other change (unit preset has CNA_ENABLE_NET=OFF so Gamer Services and the avatar submodule are not needed for the first loop; handoff.md/removed-renderers.md statements still hold). MOVED.
- development/handbook/add-a-regression-test.html: no prose change (ParityFixtures.cmake gained texture_setdata_after_draw; registering families still EasyGL, SDL_GPU, WebGPU; UnitTests.cmake additions — renderer-suite discovery in multi trees, new configuration tests, input filter's -MediaPlayerTest.* — do not contradict the recipe). MOVED.
- development/handbook/change-build-configuration.html: coordinator's dependency table/pin procedure kept (verified against ThirdPartyFNA3D.cmake header, VendoredSourceCheck.cmake, SdlPrebuiltFingerprint.cmake at 3b43bd86). 'Where to change' row for a pinned dependency now names VendoredSources.cmake, Fna3dSourcePin/Check.cmake and the configuration tests registered in cmake/UnitTests.cmake at 3b43bd86 (CnaVendoredSourceCheck, CnaFna3dSourcePin, CnaFna3dSourceCheck, CnaFna3dDependencyShape, CnaCxxSdkDependencies, CnaSdlShadercrossPatch, CnaSdlAndroidAssetEnumeration on POSIX hosts). MOVED.
- development/handbook/change-map.html: no prose change (cited files changed narrowly: GraphicsDevice()/CreateGameGraphicsDevice parameters, two IGraphicsRenderer virtuals, content.cpp nested names, UnitTests.cmake registrations; no row states any of them). MOVED.
- development/handbook/change-public-xna-behavior.html: no prose change (plan_bindings_upstream.md gained four XNA-over-FNA rows — struct defaults, MSAA pixel centres, MouseState/GamePadState text, PresentationParameters defaults — consistent with the page's recording rule; fna-reference-harness.md, compare-fna-reference.py, xna-oracle README (private-display command), audit_xna_runtime_surface.py note, ABI_VERSIONING.md 0.x consumer rule: nothing the page states changed). MOVED.
- development/handbook/conventions.html: no prose change (AGENTS.md now points binding design at docs/binding.md instead of the read-only misc/analysis_binding*.md — the page never cited those; CHECKLIST.md comment rewording; plan_bindings_upstream.md rows added). MOVED.
- development/handbook/debug-shutdown-and-lifetime.html: no prose change; the 'Status at' column relabelled 3b43bd86 after checking that modules/phone, audio, media, storage, devices (only a compass comment), CnaCApiDetail.cpp and CurrentPlatform.cpp are unchanged in the interval; TeardownLifetimeSmoke.c only sets is_full_screen = CNA_FALSE (XNA PresentationParameters defaults); build-performance.md still says vendored SDL and ENet stay uninstrumented. MOVED.
- development/handbook/fix-a-renderer-bug.html: no prose change. '32 parity fixtures' recounted at 3b43bd86 = 32 (texture_setdata_after_draw went into CNA_CONFORMANCE_FIXTURES, not CNA_PARITY_FIXTURES); registering families unchanged; xna-oracle README now runs Wine under run_gpu_tests_private.sh (page names no command); HEADLESS readback refusal matches RenderTargetReadback Unsupported. MOVED.
- development/handbook/investigate-a-sample-failure.html: coordinator's vertex-colour-clamp correction kept (docs/fx-compiled-effects.md §10.4 at 3b43bd86: fork commit vertex-color-clamp, every GLSL profile). Error-guide sentences unchanged in the doc. MOVED.
- development/handbook/make-a-release.html: no prose change (CHANGELOG.md diff only adds the avatar-submodule note under [Unreleased]; 0.1.0 entry unchanged, so 'read from CHANGELOG.md at' relabelled; version 0.1.0 and ABI 0.50.0 unchanged; RELEASE_GATE still Not ready). MOVED.
- development/handbook/modify-a-platform-backend.html: '31 flags at c6dec91f' recomputed (PlatformCapabilities.hpp unchanged) and relabelled 3b43bd86; PlatformEvent.hpp change is a comment; platform-abstraction.md still has the twelve-step 'Adding an implementation' list (plus a new 'contract describes what CNA needs' rule). MOVED.
- development/handbook/modify-contentmanager.html: no prose change (ContentManager.hpp and LooseFileContentTypeReader.hpp changed only comments: cnj.md -> docs/cnj-format.md). MOVED.
- development/handbook/modify-the-content-pipeline.html: 'Child assets' rule extended: an unnamed nested build gets <derived>_<index> (smallest index no build item holds; XnaPipelineBridge.cpp ~L858-890), as XNA BuildCoordinator.ChooseOutputFilename, settled in node order independent of worker count (tools/content/content.cpp reservation loop, ContentPipeline.hpp NestedBuildNames/reservedNestedNames at 3b43bd86; 98aa655f2, 419723275); 'one name' -> 'one explicit name' for the collision rule. XnaPipelineBridge.cpp changes (AddDependency as PipelineException, XNA-typed texture BuildAndLoadAsset) contradict nothing on the page. MOVED.
- development/handbook/update-the-c-api.html: planned rows by module recomputed from docs/c-api/COVERAGE.md at 3b43bd86 (graphics 252, math 32; others unchanged; sum 633); "the generated 625" -> 633 (plan_binding.md still says 320 for CBIND-127; RELEASE_GATE.md still records 654); 0.50.0 "three renderer features" -> five (ABI_VERSIONING.md: 32–36, the last two added at the same ABI version); binding consequence (a) rewritten: CONSUMING.md and ABI_VERSIONING.md at 3b43bd86 no longer suggest every 0.x minor is additive — they tell a 0.x consumer to refuse an unknown minor via cna_get_abi_version() (hello_cna.c step 1); find_package still accepts any later 0.x. 628 mapping rules unchanged. MOVED.
- development/index.html: snapshot sentence -> 3b43bd86 (27 October 2026, 948 commits after 0.1.0), 'These pages describe CNA at' -> 3b43bd86; hub counts (23 modules, 10/8, 3/3) unchanged at 3b43bd86 (R1 §1). MOVED.
- development/internals/audio/engine.html: no prose change (modules/audio byte-identical in the interval; UnitTests.cmake audio filters unchanged; modules/CMakeLists.txt comment only). MOVED.
- development/internals/bindings/c-api-internals.html: Strings paragraph gains the one exception: cna_shader_effect_create copies a whole SPIR-V module view byte for byte (whole 32-bit words, >= 5-word header, SPIR-V magic) and validates other views as text (modules/c-api/src/CnaCApiEffects.cpp IsSpirvModuleView/ReadShaderSource at 3b43bd86, 9ef292993, DC-R3). 59 CnaCApi*.cpp unchanged; ABI 0.50.0, 60 headers unchanged. MOVED.
- development/internals/bindings/csharp.html (c1c316b9 label KEPT): the README run 'against CNA 8a7e13ff5 (an ancestor of this snapshot whose C headers are the same)' was wrong — git diff 8a7e13ff5 c1c316b9/c6dec91f/3b43bd86 -- modules/c-api/include differs (abi.h minor 44 vs 46/50, graphics.h, effects.h, runtime_window.h; 3b43bd86 adds two RendererFeature constants and doc changes) — reworded to 'whose C headers declare ABI 0.44.0; the headers have changed since'. Name-level import comparison (#snapshot section) still holds at 3b43bd86: no C route declaration removed in the interval (3,212 routes, 60 headers). CNA.NET still exactly 0.47.0. Callout and inline 'c6dec91f declares 0.50.0' left as history; doc-meta untouched. NOT MOVED (c1c316b9).
- development/internals/bindings/java.html, python.html (c1c316b9 labels KEPT): nothing the interval contradicts — no C route declaration added or removed (3,212 routes, 60 headers), ABI 0.50.0, identity set unchanged (graphics.h only gained two feature constants). No edit. NOT MOVED (c1c316b9).
- development/internals/content/pipeline.html: coordinator's nested-name and BuildAndLoadAsset corrections verified against XnaPipelineBridge.cpp (~L858-890 <derived>_<index>, NestedBuildNames) and tools/content/content.cpp at 3b43bd86 and kept; no further change (889a31be4 Workshop items — AddDependency as PipelineException, Convert argument checks — are not described here in a contradicting way). MOVED.
- development/internals/content/runtime.html: no prose change (ContentManager.hpp, LooseFileContentTypeReader.hpp, CnjResolverOrderTests.cpp: comment/message rewording to docs/cnj-format.md; Game.cpp change is the device parameters; model-content-pipeline-support.md rewrite not cited for a contradicted claim; the Avatar/ENet/misc topic hits and CNA-BUG-245/256/272 are only in the generated issue block). MOVED.
- development/internals/graphics/backends.html: CNA-DEMOS-ISSUE-066 (SetBlendEnabled) no longer "committed but not yet validated": CNA_DEMOS_REPAIR_MATRIX.json at 3b43bd86 = FIXED_VALIDATED (closed on a complete checkpoint, 6c8b042c4). Stale-comment notes re-checked at 3b43bd86 and still true (DirectX9Renderer.hpp "un-overridden here on purpose" while overriding; IGraphicsRenderer.hpp depth/stencil split comment; RendererSelection.cmake FNA3D effect-blob comment vs single FetchContent_Declare), so "read at" relabelled. MOVED.
- development/internals/modules/devices.html (partial, see below): ISSUE-008 sentence "committed at this snapshot but not yet validated by CNA" -> "recorded by CNA as validated on a complete checkpoint (6c8b042c4)" (matrix FIXED_VALIDATED).
- development/internals/graphics/device.html: default constructor now CreateWindowedEXT(800, 480) (GraphicsDevice.cpp ~L424 at 3b43bd86; XNA's PresentationParameters() is 0x0 full screen, e460e0ed6); capability profile '31 features' -> 33 (RendererCapabilityProfile.hpp: MultiSampleMask = 35, RenderTargetReadback = 36, Count = 37; GraphicsDevice.cpp rows from MultiSampleMaskSupportEXT()/ReadsBackRenderTargetsEXT()). Test-file diffs (renderer identity test asks the selected renderer; capability tests for the new rows) consistent with the table. MOVED.
- development/internals/graphics/draw-call.html: SDL_GPU snapshot step adds that PushDrawOrder applies MultiSampleMask all-or-none on a multisampled target (keep-all draws, keep-none drops, partial throws NotSupportedException; SdlGpuRenderer.cpp PushDrawOrder at 3b43bd86, c7f6c68e5 DC-R2). Software trace still accurate at its level (pixel-centre move now in clip space before clipping, also on MSAA targets; not detailed here). MOVED.
- development/internals/graphics/easygl.html (c1c316b9 label KEPT): EasyGLRenderer.cpp/EasyGLCompiledEffect.cpp diffs (pixel-centre correction now also on multisampled targets; absent vertex colour reads white; new MultiSampleMaskSupportEXT/ReadsBackRenderTargetsEXT overrides) contradict no sentence — the page states no MSAA exception, no sample-mask answer and no absent-attribute rule. CNA-BUG-282 (EasyGL Unsupported without glSampleMaski) not stated in prose. No edit. NOT MOVED.
- development/internals/graphics/headless.html: no prose change (modules/renderers/headless: only an examples/CMakeLists.txt comment; render-target readback refusal matches the new RendererFeature::RenderTargetReadback = Unsupported answer for HEADLESS). MOVED.
- development/internals/graphics/resources.html: coordinator's DC-R1 cube-face-in-MRT text kept (SdlGpuRenderer::SetRenderTargets at 3b43bd86); Texture2DTests/RenderTargetSemanticsTests diffs only switch to CreateWindowedEXT and add readback cases; no other change. MOVED.
- development/internals/graphics/sdl-gpu.html: coordinator's DC-R1/DC-R2/upload-ordering corrections verified against SdlGpuRenderer.cpp at 3b43bd86 (PushDrawOrder mask block, FillCubeFaceColorTargetInfo, SubmitQueuedSamplersEXT) and kept; the flush list now also names an upload to a texture a queued command samples (SubmitQueuedSamplersEXT calls EnsureFrameRendered when framePending_ and the state is shared). Pixel-centre (now also on MSAA targets), EmissiveColor and non-Color cube readback changes contradict no sentence. MOVED.
- development/internals/graphics/selection.html: the environment-selection route is now also exercised by the CTest discovery of the SDL_GPU/FNA3D compiled-effect suites in trees where they are compiled in but not the default (cmake/UnitTests.cmake _cna_unit_tests_renderer_suites, ENVIRONMENT CNA_GRAPHICS_RENDERER=<renderer>, 47c3c4405 AVH-07). FNA3D status line/ThirdPartyFNA3D changes do not touch the page's claims (cna_configure_mojoshader/cna_configure_fna3d unchanged). MOVED.
- development/internals/graphics/software.html: no prose change (SoftwareRenderer.cpp: pixel-centre correction moved into clip space and now applied on 4x targets too; MultiSampleMaskSupportEXT Supported / ReadsBackRenderTargetsEXT true added; the page states neither the old MSAA exception nor a mask answer). MOVED.
- development/internals/graphics/stub.html: no prose change (modules/renderers/stub and CMakePresets.json unchanged; STUB inherits the two new IGraphicsRenderer defaults, Unsupported/false, as the page's 'inherited defaults' rule says). MOVED.
- development/internals/index.html (c1c316b9 label KEPT): hub only; the FNA3D mention ('no dedicated page yet') still true. No edit.
- development/internals/input/events.html: MouseInputTests.cpp '(43 cases)' -> 44 (TEST/TEST_F count at 3b43bd86; 0ef875619 added the XNA ToString case). Other counted files unchanged in the interval. MouseState/GamePadState ToString now XNA's text — the page does not describe it; CnaCApiInput.cpp gamepad text route change not described either. MOVED.
- development/internals/modules/core.html: no prose change (modules/core byte-identical; avatar catalog library still links cna_core_headers only; graphics.h gained feature constants, identity values unchanged; c-api CMakeLists/CoreExt unchanged). Kept 're-read at c6dec91f' in the callout as Phase 6 history. MOVED.
- development/internals/modules/design.html: no prose change (modules/design unchanged; UnitTests.cmake/modules/CMakeLists.txt changes do not touch its registration; 'enet' topic hit was a substring). MOVED.
- development/internals/modules/devices-ext.html: no prose change (devices.h: doc comment of cna_environment_get_device_type corrected in CNA, not described here; Sdl3SystemServices.cpp: Android 'assets://' base path -> './', not the dialog/tray code described). MOVED.
- development/internals/modules/devices.html: ISSUE-008 status corrected (above); modules/devices changed only a compass comment; DeviceType 'Device on mobile, Emulator elsewhere' matches the corrected devices.h doc. MOVED.
- development/internals/modules/diagnostics.html: no prose change (modules/diagnostics unchanged; Game.cpp/GraphicsDevice.cpp changes are the device parameters and two feature rows, not the diagnostic sites). MOVED.
- development/internals/modules/gamer-services.html: coordinator's avatar-submodule/revision-5 text verified (modules/gamer-services/CMakeLists.txt FATAL_ERROR, docs/gamer-services-known-limitations.md item at 3b43bd86) and kept. Test-macro count recomputed with the page's line-anchored TEST/TEST_F/TEST_P method: 701 -> 708 at 3b43bd86 (39 files; GuideAvatarEditorTests.cpp, CredentialStoreTests.cpp grew); 82 src TUs and GamerServicesServiceTests 58 unchanged. 'avatar record re-read at' relabelled 3b43bd86. MOVED.
- development/internals/modules/graphics-ext.html (c1c316b9 label KEPT): removed the sentence that GraphicsDevice declares DrawPrimitivesIndirectEXT/DrawIndexedPrimitivesIndirectEXT — no such declaration exists at c6dec91f or 3b43bd86 (git grep IndirectEXT in modules/graphics/include: none; the indirect path was retired with the modern GPU layer); removed the stale "rerun the HLSL script"/"The HLSL script has no --check mode" (no HLSL script in modules/graphics-ext or tools/shader_package at 3b43bd86, and the page itself says the HLSL route is gone). Test macros 73 unchanged at 3b43bd86; modules/graphics-ext changed by one line. NOT MOVED.
- development/internals/modules/inspector.html (c1c316b9 label KEPT): modules/inspector unchanged in the interval; cited CMake files changed only comments/test registrations elsewhere. No edit.
- development/internals/modules/math.html: coordinator's XmlSerializer Color/Rectangle/Point paragraph verified (XmlSerializationEXT.hpp at 3b43bd86) and kept. Counts recomputed: math test definitions 957 -> 959 (42 files), XmlSerializationEXTTests 4 -> 6. modules/math otherwise unchanged (only XmlSerializationEXT.hpp + its test), so the 'read at' table headers and statements were relabelled 3b43bd86; 'Re-read at c6dec91f' (Decompose note) kept as Phase 6 history. MOVED.
- development/internals/modules/media.html: no prose change (modules/media unchanged; ThirdPartySDL.cmake still SDLMIXER_OPUS=OFF; Sdl3SystemServices.cpp change is the Android base path, not the user folders described; UnitTests.cmake keeps MediaPlayerTest out of the input gate, not stated here). MOVED.
- development/internals/modules/net.html: ENet build paragraph now says third_party/enet is upstream master 5a9c537f unmodified, a committed directory (not a submodule), linked statically (cmake/ThirdPartyENet.cmake header and BUILD_SHARED_LIBS OFF at 3b43bd86; c59a91c00). Test paragraph: 'CnaENetUnsequencedTests separately pins the vendored ENet patch' was wrong at 3b43bd86 (no patch; CNA_PATCHES.md gone) -> two UBSan C programs CnaENetUnsequencedTests and CnaENetFragmentTests (new, cmake/UnitTests.cmake) compile ENet's protocol.c and check unsigned shifts that upstream release tags still do signed. 35 test files / 563 macros unchanged. MOVED.
- development/internals/modules/phone.html, storage.html, video-ffmpeg.html: no prose change (modules/phone, modules/storage, modules/video-ffmpeg byte-identical in the interval; the cited Game.cpp/UnitTests.cmake/modules/CMakeLists.txt/root CMakeLists.txt changes do not touch their statements; storage "ABI 0.50.0 at" relabelled — still 0.50.0). MOVED (3 pages).
- development/internals/platforms/headless.html: no prose change (Headless/Terminal platform sources unchanged; platform CTest routes unchanged — the UnitTests.cmake changes are the renderer-suite discovery, ENet test, media filter and configuration tests). MOVED.
- development/internals/platforms/index.html: no prose change (platform-abstraction.md still has the twelve-step list; IPlatform.hpp comment only; FNA3D hit is the SDL-linking family list). MOVED.
- development/internals/platforms/sdl3.html (c1c316b9 label KEPT): nothing contradicted (Sdl3 platform sources changed only in Sdl3SystemServices.cpp — Android base path 'assets://' -> './' — and a header comment; the page states nothing about the base path). No edit.
- development/internals/platforms/terminal.html: 'Game's constructor reads the capability set once' was wrong (since 1741edc5c, 2026-10-12, Game reads it lazily in GetPlatformCapabilitiesEXT via std::call_once); reworded: the probe still runs during Game construction because GraphicsDevice asks Supports(SurfacePresentation), which IPlatform's default answers through GetCapabilities (TerminalPlatform does not override Supports). Pre-existing error, not an interval change. 800x480 text is about a requested size, still correct. MOVED.
- development/internals/runtime/frame.html, module.html, shutdown.html: no prose change (Game.cpp diff is CreateGameGraphicsDevice only; GraphicsDeviceManager defaults 800x480/Depth24 unchanged; PlatformEvent.hpp/GraphicsDevice.hpp changes are comments). MOVED (3 pages).
- development/internals/runtime/startup.html: Game's device parameters are windowed 800x480 from PresentationParameters::CreateWindowedEXT + Depth24 (Game.cpp CreateGameGraphicsDevice at 3b43bd86), not 'default PresentationParameters (800x480)'; the construction diagram already said '800x480 parameters with Depth24'. Descriptor header unchanged, so 'at 3b43bd86 no descriptor asks for a high-density window' relabelled. MOVED.
- development/invariants.html: no prose change (Game.cpp, GraphicsDevice.cpp, IGraphicsRenderer.hpp, RendererSelection.cmake diffs do not touch the rules; no test registration removed in UnitTests.cmake; content-pipeline.md change is component versions). Kept 'evidence was re-read at c6dec91f' as history. MOVED.
- development/repository/index.html: coordinator's submodule/fork/ENet/misc corrections kept. Top-level counts recomputed from git ls-tree -r 3b43bd86 with the page's method: modules/ 4,256 -> 3,902 (avatar catalog now a gitlink), cmake/ 254 -> 133 and patches/ 146 -> 7 (five SDL patches, the shadercross patch and its apply script), tests/ 2,063 -> 2,067 (assets 1,140 -> 1,141, reference/xna40 567 -> 570: effect-struct-defaults), tools/ 454 -> 496 (avatar_builder 27 -> 67), scripts/ 50 -> 49, docs/ 188 -> 192, spikes/ 74 -> 78 and 20 -> 21 probe directories (xna-msaa-pixel-center-spike); plans/ 66 already right. Test-source distribution: graphics 196 -> 198 (RenderTargetReadbackLayoutTests.cpp, XnaMultisamplePixelCenterTests.cpp), so the table sums to the stated 900 again. MOVED.
- development/repository/module-graph.html: no prose change (module CMake edges unchanged; modules/renderers/CMakeLists.txt and renderer_sdl_audit.py unchanged; content.cpp change is the nested-name reservation, not an edge). MOVED.
- development/repository/source-ownership.html (c1c316b9 label KEPT): coordinator's dependency rows kept (verified: SDL 86296ac8, avatars 4617a1e7 + FATAL_ERROR, ENet 5a9c537f unmodified, FNA3D 10f650b9d0f6 fork). Generated-files row was wrong: '*ShaderPackage.generated.hpp (20 headers) ... 18 *ShaderPackageReproducibility tests; ShadowCaster and ModernResourceInterop packages have no registration' -> 3 headers and 3 registrations, one per package (git ls-tree; cmake/Tests/ModuleProbes.cmake L272-303 at 3b43bd86; the same 3 at c6dec91f — a pre-existing error). NOT MOVED.
- development/takeover/case-study-components.html: no prose change (Game.cpp component code untouched by the interval; 3faa1930aa and 43748c883 are ancestors of 3b43bd86, re-checked with merge-base --is-ancestor). Meta descriptions and ancestry command relabelled. MOVED.
- development/takeover/curriculum.html (c1c316b9 label KEPT): nothing contradicted (presets, filters and named symbols unchanged; the 'changed recently in UnitTests.cmake' note predates the 3b43bd86 additions but states nothing false). No edit.
- development/takeover/inherited.html: planning-material list no longer names misc/ (retired 2026-10-25) or 'repair handoffs' generically; it now names handoff.md, CHECKLIST.md, CNA_ENGINE_REPAIR_HANDOFF.md and CNA_DEMOS_REPAIR_MATRIX.json (root of 3b43bd86) and says misc/ and the closed handoffs survive in Git history. 'At snapshot … the tree has 23 directories' relabelled (counts 900/11,927 already set by the coordinator, so the sentence now names the commit they were counted at). MOVED.
- development/takeover/investigation.html (c1c316b9 evidence label KEPT): only the pin references were moved — doc-meta, 'The Development pages are pinned to …' and its git show/grep/diff examples, and the record template's 'CNA commit (vs …)' — to 3b43bd86, because the area's links and pin are now 3b43bd86; the traces themselves keep their c1c316b9 evidence statement. Nothing in the traces contradicted (GraphicsDevice::Reset path unchanged; ABI 0.50.0; CNA.NET exactly 0.47.0).
- Doc-meta lines ('CNA snapshot … · source links pinned to …') on the reviewed c1c316b9-labelled pages (csharp, java, python, easygl, internals/index, graphics-ext, inspector, sdl3, source-ownership, curriculum, investigation) moved to 3b43bd86: their source links are pinned to 3b43bd86 (coordinator's repin), and Phase 6 gave c1c316b9 pages the then-current pin in this line too. Their evidence callouts stay c1c316b9.
- development/takeover/mental-model.html (c1c316b9 label KEPT): nothing contradicted (resolveRenderer, IPlatform event order, link multiplicity unchanged). Doc-meta pin line moved. No other edit.
- development/takeover/own-a-subsystem.html: size figures recomputed at 3b43bd86 with the page's stated method (lines in include/+src/, line-start TEST/TEST_F/TEST_P scan of tests/; the same script reproduces every c6dec91f figure exactly): math 14,208 -> 14,266 lines, 951 -> 953 definitions (and 'about 14,200' -> 14,300); c-api 152,519 -> 152,629; content 64,929 -> 65,001 lines (2,082 unchanged); graphics 62,179 -> 62,306 lines, 3,100 -> 3,111; platform 21,026 -> 21,036. storage, design, phone, diagnostics, audio, Terminal/Headless and STUB/HEADLESS renderer figures unchanged. MOVED.
- development/takeover/ownership.html: no prose change (ownership paths in Game.cpp/GraphicsDevice.cpp unchanged; only the device parameters changed). MOVED.
- development/takeover/review-ai-generated-code.html: every Git/tree statistic recomputed at 3b43bd86 with the method that reproduces the c6dec91f figures exactly (scripts in the R4 record): reachable commits 10,543 -> 10,679 (one author); since v0.1.0-alpha.1 4,521 -> 4,657, no Co-authored-by, signed 4,018 -> 4,154 (SSH 212); type(scope): subjects 4,134 -> 4,242 (regex ^[a-z]+(\([^)]*\))?!?:); (Task …) 895 -> 916; PREFIX-number ~3,620 (80 %) -> ~3,670 (79 %); ranges 30 and widest unchanged; first-parent 1,977 -> 2,113 (2,061 direct + 52 merges; 69 merges, 31 merge(<Campaign>); 2,544 inside branches unchanged); plans 68 -> 62 (+ index; 63 .md); handoff.md 353 -> 524 lines, last changed by the target commit 3b43bd868 itself, §5.1 none open (reconciled 2026-10-24); CNA_*_REPAIR_HANDOFF.md files -> only CNA_ENGINE_REPAIR_HANDOFF.md remains (demos/museum handoffs and inherited review removed 2026-10-25); spikes 20 -> 21, xna-* probes six -> seven; docs/ top-level .md 138 -> 142 (all 177 -> 181); AGENTS.md 503 -> 498 lines; plan citations 1,651 files / 4,736 cites / 70 plans -> 1,613 / 4,616 / 70, missing-plan cites 412/29 -> 413/30; plan_webgpu 201 done + 1 partial unchanged. Drift table re-checked (cited files unchanged except a TestDisplayPolicy comment); labels moved. MOVED.
- development/takeover/threading.html: no prose change (thread-construction file list identical at both commits by the page's search; no lock added or removed in the SdlGpuRenderer.cpp, EasyGLRenderer.cpp or AvatarModel.cpp diffs; lease paths unchanged). MOVED.
- development/takeover/uncertainty.html: no prose change (cited history commits remain ancestors of 3b43bd86; ABI 0.50.0, 60 headers, 3,212 routes, C ABI renderer MAXIMUM 43 unchanged; handoff.md §5 still the register; graphics.h gained only feature constants). Meta description relabelled with the callout. MOVED.
- development/takeover/validation.html (c1c316b9 label KEPT): the gtest_discover_tests paragraph now adds that in a tree where SDL_GPU or FNA3D is compiled in but not the default, their compiled-effect suites are discovered by a separate call with CNA_GRAPHICS_RENDERER set and excluded from the default discovery (cmake/UnitTests.cmake at 3b43bd86, AVH-07). apple-platforms.md (patch rename), input-build-and-test.md (SDL revision), ABI_VERSIONING.md: nothing the page states changed. Doc-meta pin line moved.
- development/takeover/worked-changes.html: C ABI rehearsal now notes that CNA appended CNA_RENDERER_FEATURE_MULTI_SAMPLE_MASK (35) and _RENDER_TARGET_READBACK (36), moving CNA_RENDERER_FEATURE_MAXIMUM to 36, inside the existing 0.50.0 notes (@since ABI 0.50.0, c7f6c68e5/e357bc4c4, 2026-10-24) although ABI_VERSIONING.md says an append that moves a MAXIMUM takes a minor — so 0.50.0 alone does not tell a consumer whether a library knows them (CNA-side inconsistency, reported). GraphicsCapability 17 members / 0–16 unchanged. MOVED.
- development/takeover/xna-oracle.html (c1c316b9 label KEPT): coordinator's 'seven probes' edits kept (spikes/xna-msaa-pixel-center-spike at 3b43bd86). FNA-executed fixtures row now notes that Fna3dEffectPixelOracleTests overrides one pass (CnaConformanceEffect FirstTechnique/P0) with genuine XNA 4.0's value because FNA's MojoShader read the structure defaults wrongly (c71eeb6e8; tests/reference/xna40/effect-struct-defaults). 'Re-read at c6dec91f' kept as history. Doc-meta pin line moved. README now runs Wine under run_gpu_tests_private.sh; the page quotes no command.
- development/testing/architecture.html: coordinator's SDL defragmenter correction kept. Discovery paragraph: SDL_GPU/FNA3D compiled-effect suites are discovered by their own call with CNA_GRAPHICS_RENDERER (and FNA3D_FORCE_DRIVER from CNA_FNA3D_TEST_DRIVER) in trees where they are compiled in but not the default, and excluded from the default discovery (cmake/UnitTests.cmake _cna_unit_tests_renderer_suites, 47c3c4405). Input label: CNA_INPUT_TEST_FILTER now ends in -MediaPlayerTest.* (b747faca2). CnaSdlPrebuiltFingerprint: 'fourteen cases' -> eighteen numbered cases (cmake/Tests/SdlPrebuiltFingerprint.cmake). Configuration-test table: new rows for CnaVendoredSourceCheck, CnaFna3dSourcePin, CnaFna3dSourceCheck, CnaFna3dDependencyShape, CnaCxxSdkDependencies, CnaSdlShadercrossPatch, CnaSdlAndroidAssetEnumeration (POSIX only), and CnaENetUnsequencedTests/CnaENetFragmentTests (UBSan C programs, native Linux GCC/Clang) and GamerServices_AvatarAcceptanceStatic. Meta descriptions relabelled with the callout. MOVED.
- development/testing/index.html (c1c316b9 label KEPT): generated test-target count 238 -> 248 (recomputed, see build/architecture); '-L configuration' row names the new dependency source/pin checks. Coordinator's 900/857/11,927/599 counts kept. Doc-meta pin line moved.
- development/workflows.html (c1c316b9 label KEPT): nothing contradicted (AGENTS.md change is the bindings section; plan_bindings_upstream.md rows added; plan_gpu_test_isolation.md comment rewording; ABI 0.50.0). Moved only pin references: doc-meta and the git grep example SHA (full 3b43bd86); the callout's 're-read at c6dec91f' kept as history.
- Wording (Phase 6 guard): "SDL's Vulkan backend" -> "SDL's Vulkan GPU driver" in the SDL patch 0005 descriptions on development/build/architecture.html, handbook/change-build-configuration.html and repository/source-ownership.html (check_retired_renderers.py flagged the coordinator-written phrase).
- development/internals/bindings/csharp.html: the corrected 8a7e13ff5 sentence says "an earlier commit than this snapshot" (keeps check_facts.py's ABI 0.44.0 needle satisfied; the binding run is attributed to that commit).

## 3. Pages moved to `3b43bd86` (69)

- development/architecture/bindings.html
- development/architecture/content.html
- development/architecture/graphics.html
- development/architecture/overview.html
- development/architecture/platform.html
- development/architecture/runtime.html
- development/build/architecture.html
- development/build/index.html
- development/debugging.html
- development/getting-started.html
- development/handbook/add-a-regression-test.html
- development/handbook/change-build-configuration.html
- development/handbook/change-map.html
- development/handbook/change-public-xna-behavior.html
- development/handbook/conventions.html
- development/handbook/debug-shutdown-and-lifetime.html
- development/handbook/fix-a-renderer-bug.html
- development/handbook/investigate-a-sample-failure.html
- development/handbook/make-a-release.html
- development/handbook/modify-a-platform-backend.html
- development/handbook/modify-contentmanager.html
- development/handbook/modify-the-content-pipeline.html
- development/handbook/update-the-c-api.html
- development/index.html
- development/internals/audio/engine.html
- development/internals/bindings/c-api-internals.html
- development/internals/content/pipeline.html
- development/internals/content/runtime.html
- development/internals/graphics/backends.html
- development/internals/graphics/device.html
- development/internals/graphics/draw-call.html
- development/internals/graphics/headless.html
- development/internals/graphics/resources.html
- development/internals/graphics/sdl-gpu.html
- development/internals/graphics/selection.html
- development/internals/graphics/software.html
- development/internals/graphics/stub.html
- development/internals/input/events.html
- development/internals/modules/core.html
- development/internals/modules/design.html
- development/internals/modules/devices-ext.html
- development/internals/modules/devices.html
- development/internals/modules/diagnostics.html
- development/internals/modules/gamer-services.html
- development/internals/modules/math.html
- development/internals/modules/media.html
- development/internals/modules/net.html
- development/internals/modules/phone.html
- development/internals/modules/storage.html
- development/internals/modules/video-ffmpeg.html
- development/internals/platforms/headless.html
- development/internals/platforms/index.html
- development/internals/platforms/terminal.html
- development/internals/runtime/frame.html
- development/internals/runtime/module.html
- development/internals/runtime/shutdown.html
- development/internals/runtime/startup.html
- development/invariants.html
- development/repository/index.html
- development/repository/module-graph.html
- development/takeover/case-study-components.html
- development/takeover/inherited.html
- development/takeover/own-a-subsystem.html
- development/takeover/ownership.html
- development/takeover/review-ai-generated-code.html
- development/takeover/threading.html
- development/takeover/uncertainty.html
- development/takeover/worked-changes.html
- development/testing/architecture.html

## 4. Pages left on `c1c316b9` (16; label "at the stated evidence commit" kept, doc-meta moved)

- development/internals/bindings/csharp.html
- development/internals/bindings/java.html
- development/internals/bindings/python.html
- development/internals/graphics/easygl.html
- development/internals/index.html
- development/internals/modules/graphics-ext.html
- development/internals/modules/inspector.html
- development/internals/platforms/sdl3.html
- development/repository/source-ownership.html
- development/takeover/curriculum.html
- development/takeover/investigation.html
- development/takeover/mental-model.html
- development/takeover/validation.html
- development/takeover/xna-oracle.html
- development/testing/index.html
- development/workflows.html

No page in scope was left on `c6dec91f`.

## 5. Issue references, generated regions

* No hand-written prose on a scoped page relied on CNA-BUG-191, -245, -256, -272 or the old meaning of CNA-BUG-280; every
  reference to them is inside a generated `<!--p3:issue-links-->` block. Those blocks now link retired pages
  (`check_dev_page.py`/`validate_site.py` report broken links: build/architecture.html → cna-bug-191,
  internals/content/runtime.html → cna-bug-245/256/272, internals/modules/net.html → cna-bug-191); they are the
  coordinator's to regenerate. No prose states the EasyGL or WEBGPU `MultiSampleMask` answer (CNA-BUG-282), so nothing was
  reworded for it. Stale figures left inside generated regions (625 in deep-link descriptions; 625/8,125 in issue blocks on
  update-the-c-api.html) were not touched.
* Two CNA-DEMOS findings described on Development pages as "committed but not yet validated" are FIXED_VALIDATED at T
  (`CNA_DEMOS_REPAIR_MATRIX.json`, closed by `6c8b042c4`): ISSUE-066 (internals/graphics/backends.html) and ISSUE-008
  (internals/modules/devices.html). ISSUE-101 and ISSUE-152 remain FIXED_PLATFORM_VALIDATION_PENDING, as the media and
  storage pages say.
* The generated test-target index will list **248** declarations at T (the pages that quote it now say 248); the generated
  references themselves were not edited.

## 6. CNA-side inconsistencies found (reported, not fixed)

1. `CNA_RENDERER_FEATURE_MULTI_SAMPLE_MASK` (35) and `_RENDER_TARGET_READBACK` (36), which move
   `CNA_RENDERER_FEATURE_MAXIMUM` to 36, were added on 2026-10-24 (`c7f6c68e5`, `e357bc4c4`) inside the existing 0.50.0
   notes with `@since ABI 0.50.0`, while `docs/c-api/ABI_VERSIONING.md` itself says an append that moves a `_MAXIMUM` takes
   a minor increment (its 0.25.0/0.26.0 entries). A library reporting 0.50.0 may or may not know the two constants.
2. Generated nested names: `tools/content/content.cpp` and `ContentPipeline.hpp` comments call XNA's generated names
   `stub_N`, while `XnaPipelineBridge.cpp` generates `<derived>_<index>` (`surface_0`) and its own comment says so; R1 and R5
   repeat the `stub_N` wording. The pages follow the code.
3. `docs/c-api/CONSUMING.md` and `ABI_VERSIONING.md` now tell a 0.x consumer to refuse an unknown minor, but the installed
   package's `SameMajorVersion` still accepts every later 0.x (both documents say so; the pages state both).
4. Pre-existing and still present at T (already stated on pages): `plans/plan_binding.md` keeps 320 open rows for CBIND-127
   against the generated 633; `RELEASE_GATE.md` still records 654 content-pipeline declarations under an open task;
   `scripts/check_renderer_identities.py` still lists the deleted `docs/renderer-expansion-candidates.md`;
   `modules/renderers/CMakeLists.txt` still says three SDL families; `CHECKLIST.md` says FNA is authoritative for behaviour
   against CLAUDE.md's XNA tie-break.
5. `handoff.md` was last changed by the target commit itself (`3b43bd868`), while its campaign section and §5.1 ("None
   open") are dated 2026-10-24.

## 7. Pre-existing errors corrected (not interval changes)

* internals/platforms/terminal.html: Game no longer reads platform capabilities in its constructor (lazy since
  `1741edc5c`, 2026-10-12); the probe still runs during construction through `GraphicsDevice`'s `Supports` query.
* internals/modules/graphics-ext.html: `DrawPrimitivesIndirectEXT`/`DrawIndexedPrimitivesIndirectEXT` are not declared at
  c6dec91f or T (sentence removed); no HLSL script exists (two stale references removed).
* repository/source-ownership.html: 3 generated shader-package headers and 3 reproducibility tests (not 20 and 18).
* internals/bindings/csharp.html: 8a7e13ff5's C headers were never "the same" as the snapshot's (ABI 0.44.0 there).

## 8. Uncertainties and notes for the coordinator

* The carry pages `development/handbook/index.html`, `development/reference/index.html`, `development/takeover/index.html`
  (c1c316b9) still carry `CNA snapshot c6dec91f · source links pinned to c6dec91f` in their doc-meta line; the reviewed
  c1c316b9 pages now say `3b43bd86` there (see §1). Apply the same or revert mine, but keep them consistent.
* The "about 3,670 (79 %)" PREFIX-number figure: two regexes that both give 3,622 at c6dec91f give 3,669 and 3,656 at T; the
  page keeps "about".
* Not executed here: every test, workflow or acceptance result quoted is CNA's record ("recorded by CNA").
* Checks run: `check_dev_page.py` on all 85 pages (only the generated issue-link breakages above), `check_dev_claims.py`
  (no error on scoped pages; the one error is `audit/3b43bd86-phase7-delta.md` on handbook/update-libcna-com.html, out of
  scope), `check_source_links.py` (ok), `check_retired_renderers.py` (no development hit after the "Vulkan GPU driver"
  rewording), `check_facts.py` (development hits are footer text, generated regions, generated reference pages and their
  callouts only), `validate_site.py` (Known Issues regeneration items and the generated issue-link breakages only).
