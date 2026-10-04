# R9: Known Issues dispositions for the pin move O → T

- **O** (old pin) = `009d40f5dd085c4e674d3479675fac84b12b3e0a`
- **T** (new pin) = `b0e97bb1bb876f9b3edd6f4ff1ef3067908ae8ac`
- **Commits in O..T:** 456

**Method.** All 370 published entries (`data/known-issues.json`, which equals `audit/data/bible/issues/issues-source.json`) were checked at T with read-only git objects.
- **Mechanical pass:** each entry's source paths were checked for existence at T and for O..T changes. Its text was scanned for retired-renderer spellings using the site's own `check_retired_renderers.strong_pattern` over the identities newly retired at T. Its `{{src:}}`/`{{tree:}}` tokens were checked against the T tree.
- **Verification pass:** nine parallel verifier batches reviewed every entry against the code, tests and docs at T. Each FIXED claim names a commit plus code or a test at T.
- **Spot checks:** I re-checked a sample at T. The tests for BUG-077, 167, 171/174, 172, 255, 265, 268, VGAP-009, 040 and 055 exist; ContentLoadException derives from System::Exception; the unguarded setenv (NEW-1) is present.

## Executive summary

**Removed subjects at T**

| Removed | Commit |
|---|---|
| DIRECT2D, FREEDIRECT, PORTABLEGL | 0f96ea703 (RRC-012) |
| GDI, HTML_DOM, SVG_DOM, OPENGL4 | 261cb5f7f (RRC-015) |
| CNA_SOFTWARE_2D_ONLY | 590ac27c8 (RRC-016) |
| Graphics engine layer (RenderPipeline, post-process, bloom/SSAO/fog, clustered lighting, shadow maps, GPU timers, engine compute, PbrMaterial, `engine_layer.h`) | 5572f3ca1 (MOD-RETIRE-1) |
| SDL2 platform and audio | 76c9bda29 (locked by test 6ee00e35d) |

CNAEXT itself survives (ASCII/CRT/Depth effects, DebugDraw, ShaderPackageEXT, `CNA_CNAEXT`), so a passing "CNAEXT" mention is not stale by itself.

**Dispositions of the 370 entries.** 128 need action; 242 are still valid.

| Disposition | Count | Effect |
|---|---|---|
| RETIRE-OBSOLETE (subject removed) | 23 | unpublished |
| RETIRE-FIXED (`PROVEN FIXED`) | 24 | unpublished |
| NARROWED (`status` → `narrowed`, with new text) | 11 | published |
| CHANGED (facts or numbers moved) | 31 | published |
| EDIT (wording, dead paths or removed-subject mentions only) | 39 | published |
| STILL VALID | 242 | published |
| **Total** | **370** | **323 stay published** |

**KF-* and KILLER-1 fixes.** These are cna-killer findings; most were never Known Issues. The ones that map to entries:

| Fix | Entry | Outcome |
|---|---|---|
| KF-13 | CNA-GAP-001 | fixed |
| KF-9 | CNA-BUG-122 | narrowed |
| KF-12 | CNA-BUG-148 | narrowed |
| KF-15 | CNA-BUG-081 | changed; the loop still never sleeps |
| KF-1, KF-1a, KF-16 | CNA-GAP-071 | narrowed |

KF-2, 4, 5, 6, 7, 8, 11, 14, 17 and KILLER-1 match no published entry.

**Other fixes that close entries**
- **GS-*/GSX/GSP/GSH (GamerServices/Net rework):** 14 retirements and 5 changes.
- **BINDFIX:** BINDFIX-038 fixes BUG-077; BINDFIX-041 fixes VGAP-055.
- **CBIND:** CBIND-138 fixes VGAP-009; CBIND-140 narrows BUG-041.
- **FULLSCREEN-001/002** fix GAP-017.
- **CCS-1** fixes BUG-255.
- **MOD-RETIRE-1** also fixed BUG-062 by adding MODULE_SCOPE entries.
- **SDL2 retirement doc edits** fixed BUG-233 and BUG-236.

**Blocking findings for the regeneration**

1. **The retired-renderer check fails.** With `cnahead` = T, `check_retired_renderers.py` flags 175 hits in `data/known-issues.json`, plus the generated pages. They are spread over 54 entries and every one is covered below; each retirement or edit removes them.
2. **The source check fails.** `known_issues.py validate` fails on 49 entries whose `sources` paths are missing at T, and the token expansion fails on 33 entries with dead `{{src:}}`/`{{tree:}}` tokens. All are covered by a retirement or an edit.
3. **Seven of the 24 entries to retire cannot be retired with the current script without renumbering other ids.** They are the audit-added entries CNA-BUG-255, 257, 258, 265, 266, 268 and 270 (keys NEW-AUDIT-07/09/10/21/23/25/27):
   - The `"retired"` pass runs before `"added"`, so it fails with "unknown entry".
   - Deleting the entries from `"added"` renumbers every later added bug id: CNA-BUG-256…274 would shift.
   - A small script change is needed; see §4.
4. **Edits to six added entries go inside their `added[]` element.** These are CNA-GAP-071, CNA-BUG-253, CNA-BUG-264, CNA-GAP-070, CNA-VGAP-056 and CNA-VGAP-059.
5. **Edits to reclassified entries use the pre-reclassification key in `"entries"`.** CNA-GAP-064 uses CNA-BUG-100, CNA-GAP-065 uses CNA-BUG-108, and CNA-BUG-250 uses CNA-GAP-050.
6. **Folded duplicates re-inject stale text.** The fold copies the folded entry's `summary` into the survivor's `evidence` and merges its `sources`. Patch these folded ids in `"entries"` as well: CNA-BUG-187 (into 190), CNA-VGAP-043 (into 026), VGAP-045 (into 023) and VGAP-048 (into 025).
7. **367 of the 370 entries say "at 009d40f5" in their text.** Examples: "Checked by reading at 009d40f5" (212), "the named sources at 009d40f5" (106). The page header will say "Verified against b0e97bb1".
   - Recommend one global decision: either a `patches.json` `global_replace` adding "re-checked at b0e97bb1 (not executed)", or an `append` of a re-verification note.
   - Per-entry substitutions below do not cover this.

**Six new issues have evidence at T** (§6):
- **NEW-1:** an unguarded POSIX `setenv` in the globbed CnaTests sources, and the guard test is gone.
- **NEW-2:** XNA's `SoundEffect.Play(volume,pitch,pan)` throws on out-of-range or disposed input; CNA clamps or returns false.
- **NEW-3 to NEW-6:** four GamerServices/Net gaps that CNA records itself.

## 1. Every entry that needs action

The `key` column is the stable key used in `patches-adversarial.json`:
- For an original entry it is the published id.
- `NEW-AUDIT-nn` marks an added entry.
- A different `CNA-` id marks a reclassified entry.

The **exact replacement text** for every EDIT, CHANGED and NARROWED row is in the batch appendix named in the `batch` column. It is given as `field: 'old verbatim substring' -> 'new'` against `issues-source.json` field values, with replacement `sources` and `related`.


### RETIRE-OBSOLETE (23)

| published id | key | class | title (short) | disposition | evidence at T | batch |
|---|---|---|---|---|---|---|
| CNA-BUG-097 | CNA-BUG-097 | bug | RenderPipeline::releaseDeviceResourcesEXT() keeps the Bloom, SSAO and volumetric-fog target pools, and the ... | RETIRE-OBSOLETE | 5572f3ca1 (MOD-RETIRE-1) deleted RenderPipeline, BloomPass, SsaoPass, VolumetricFogPass, DeviceLifecycleTests | G1 |
| CNA-BUG-098 | CNA-BUG-098 | bug | A throwing shadow-caster or transparent-phase callback leaves RenderPipeline and its ShadowMap in an unreco... | RETIRE-OBSOLETE | 5572f3ca1 deleted RenderPipeline.cpp, ShadowMap.cpp, PipelineDiagnosticsTests.cpp | G1 |
| CNA-BUG-109 | CNA-BUG-109 | bug | The engine layer's capability-name table has no IndirectDraw entry, although its comment says a missing cap... | RETIRE-OBSOLETE | 5572f3ca1 deleted graphics-ext/src/RequireCapability.cpp (nameOfCapability gone) | G1 |
| CNA-BUG-175 | CNA-BUG-175 | bug | The bundled procedural avatar's garment shells interpenetrate its body, leaving the collar and cuffs visibl... | RETIRE-OBSOLETE | 3f4518e69 (GS-009b..d) replaced the procedural avatar by a 71-bone catalog; 13dfe0499 (GS-009f) removed both cited Blender .py scripts; garment fit test AvatarCatalogTest.ItemsAreFittedToTheirBody (75a390447) | NET |
| CNA-BUG-178 | CNA-BUG-178 | bug | The SDL2 backend negates a flipped mouse wheel while SDL3 passes SDL's adjusted value through, so the two r... | RETIRE-OBSOLETE | 76c9bda29 deleted modules/platform/src/Sdl2/*; 6ee00e35d CnaPlatformSelection_SDL2 + PlatformFactoryTests.RetiredSdl2ImplementationIsNeitherAdvertisedNorCreatable | BUILD |
| CNA-BUG-189 | CNA-BUG-189 | bug | The GDI renderer's configure message hard-codes '3 GDI-owned units' while modules/renderers/gdi/src compile... | RETIRE-OBSOLETE | 261cb5f7f (RRC-015) deleted modules/renderers/gdi (GDI=40 retired) | BUILD |
| CNA-BUG-194 | CNA-BUG-194 | bug | The SDL2-only configuration guard recommends VULKAN, which the SDL2 platform cannot run | RETIRE-OBSOLETE | 76c9bda29 deleted cmake/Sdl2OnlyConfiguration.cmake, Sdl2OnlyRendererGate.cmake, Sdl2Platform.cpp | BUILD |
| CNA-BUG-195 | CNA-BUG-195 | bug | The SDL2-only guard inspects only CNA_GRAPHICS_RENDERER, so a multi-renderer list containing an SDL3-linked... | RETIRE-OBSOLETE | 76c9bda29 (same); SdlAvailability.cmake has no SDL2 branch | BUILD |
| CNA-BUG-200 | CNA-BUG-200 | bug | The registered CTest CNAEXT_NoPosixSetenv fails at this snapshot: twelve Wayland setenv/unsetenv call lines... | RETIRE-OBSOLETE | 5572f3ca1 deleted the add_test(CNAEXT_NoPosixSetenv) block; no CMake registers check_no_posix_setenv.py at T (see NEW-1) | BUILD |
| CNA-BUG-249 | CNA-BUG-249 | bug | misc/CNAEXT.md's 'Renderer shader coverage for PBR' table omits OPENGL4 and METAL and still says WebGPU has... | RETIRE-OBSOLETE | 5572f3ca1 marks misc/CNAEXT.md "Historical record"; OPENGL4 (261cb5f7f) and PORTABLEGL (0f96ea703) gone; 2 cited sources missing | DOC |
| CNA-BUG-257 | NEW-AUDIT-09 | bug | PORTABLEGL depth clears force glDepthMask(GL_TRUE) and never restore it, although their own comment says bo... | RETIRE-OBSOLETE | 0f96ea703 (RRC-012) removed PORTABLEGL (PORTABLEGL=46 retired); added entry -> needs retired_added | G1 |
| CNA-BUG-270 | NEW-AUDIT-27 | bug | The @param lines of cna_post_process_chain_add_owned_pass and cna_skybox_set_owned_environment say the cons... | RETIRE-OBSOLETE | 5572f3ca1 deleted engine_layer.h (12,039 lines) and CnaCApiEngineLayer.cpp; route names absent at T; added entry -> needs retired_added | MISC |
| CNA-GAP-025 | CNA-GAP-025 | functional-gap | DIRECT2D refuses additive blending (SourceAlpha/One and One/One) and other asymmetric or non-Add blend stat... | RETIRE-OBSOLETE | 0f96ea703 removed modules/renderers/direct2d | G2 |
| CNA-GAP-027 | CNA-GAP-027 | functional-gap | HTML_DOM and SVG_DOM refuse back-buffer readback | RETIRE-OBSOLETE | 261cb5f7f removed HTML_DOM and SVG_DOM | G2 |
| CNA-GAP-029 | CNA-GAP-029 | functional-gap | EasyGL GPU timers read 32-bit nanosecond results and cannot detect GL disjoint events | RETIRE-OBSOLETE | 5572f3ca1 removed CNA::Graphics::GpuTimer, pass timings, graphics-ext/src/GpuTimer.cpp (EasyGLGpuTimerRenderer survives only behind internal CreateGpuTimerEXT) | G2 |
| CNA-GAP-030 | CNA-GAP-030 | functional-gap | FREEDIRECT keeps presenting at the old physical scale after a virtual-resolution change once the first Pres... | RETIRE-OBSOLETE | 0f96ea703 removed freedirect and docs/freedirect-renderer.md | G2 |
| CNA-GAP-031 | CNA-GAP-031 | functional-gap | ClusteredForwardEffect binds no material textures: many punctual lights cannot be combined with a texture set | RETIRE-OBSOLETE | 5572f3ca1; git grep ClusteredForwardEffect at T finds nothing; graphics-ext-scope-reduction.md section B | G2 |
| CNA-PLAT-006 | CNA-PLAT-006 | platform-limitation | Under Wine or Proton, Direct2D lacks the ColorMatrix effect and ignores bounded-copy and Porter-Duff compos... | RETIRE-OBSOLETE | 0f96ea703 (Direct2D removed) | G2 |
| CNA-PLAT-007 | CNA-PLAT-007 | platform-limitation | On browsers without mix-blend-mode: plus-lighter, HTML_DOM and SVG_DOM draw BlendState.Additive as ordinary... | RETIRE-OBSOLETE | 261cb5f7f (HTML_DOM/SVG_DOM removed) | G2 |
| CNA-VGAP-010 | CNA-VGAP-010 | verification-gap | No CI workflow builds or tests the OPENGL4 renderer | RETIRE-OBSOLETE | 261cb5f7f removed modules/renderers/opengl4, docs/opengl4-renderer.md, OpenGL4 plan (OPENGL4=33 retired) | BUILD |
| CNA-VGAP-017 | CNA-VGAP-017 | verification-gap | graphics-ext shader-package drift guards have holes: no reproducibility check for shadow_caster, none run i... | RETIRE-OBSOLETE | 5572f3ca1 deleted shadow_caster, modern_resource_interop, clustered_forward packages + ClusteredForwardEffectTests.cpp (residue moved into CNA-VGAP-056) | TEST |
| CNA-VGAP-018 | CNA-VGAP-018 | verification-gap | No test asserts RenderPipeline's fixed post-process order; the order-named tests only count passes | RETIRE-OBSOLETE | 5572f3ca1 removed RenderPipeline.cpp, RenderPipelineTests.cpp, PassTimingTests.cpp | TEST |
| CNA-VGAP-042 | CNA-VGAP-042 | verification-gap | FREEDIRECT is built and tested by no workflow, has been verified on Linux only, and its free-direct and fre... | RETIRE-OBSOLETE | 0f96ea703 removed modules/renderers/freedirect + docs (FREEDIRECT=21 retired) | TEST |

### RETIRE-FIXED (24)

| published id | key | class | title (short) | disposition | evidence at T | batch |
|---|---|---|---|---|---|---|
| CNA-BUG-062 | CNA-BUG-062 | bug | MODULE_SCOPE in generate_coverage_inventory.py leaves design, diagnostics and inspector unclassified, so ev... | RETIRE-FIXED | 5572f3ca1 adds design/diagnostics/inspector as OUT_OF_SCOPE to MODULE_SCOPE (generate_coverage_inventory.py); COVERAGE.md regenerated (469 headers/8142 symbols); test_coverage_scope.py; 8b55f7f4d records CApiCoverageMatrix passing | DOC |
| CNA-BUG-077 | CNA-BUG-077 | bug | An invalid CNA_GRAPHICS_RENDERER value (or Module.cnaPreferredRenderer) terminates the process during stati... | RETIRE-FIXED | f1593227d (BINDFIX-038) GraphicsRendererSelection.cpp no longer rebuilds attempt order in static init; error kept and rethrown as InvalidOperationException; tests GraphicsRendererSelectionTest.ARefusedEnvironmentVariableKeepsRefusingUntilARendererIsSet, CApi_RendererEnvironment_unknown/_absent | CORE |
| CNA-BUG-151 | CNA-BUG-151 | bug | StorageDevice::EnsureStorageRoot latches an empty root after a failed resolution, and storage then operates... | RETIRE-FIXED | 8a67da536 (SAMPLE-070): flag set only after storageRoot_ assigned; failed create_directories throws StorageDeviceNotConnectedException and is retried (code evidence, no test) | NET |
| CNA-BUG-165 | CNA-BUG-165 | bug | LeaderboardReader::Read, PageDown and PageUp never delete the LeaderboardAction their Begin call allocates | RETIRE-FIXED | 9473f5c89 (GS-006a): all synchronous wrappers own the Begin result in std::unique_ptr (code evidence) | NET |
| CNA-BUG-166 | CNA-BUG-166 | bug | GamerServicesDispatcher::Initialize deletes every SignedInGamer in the installed collection, including game... | RETIRE-FIXED | 0ab6cc3fe (GS-003b/004a): Initialize creates/deletes no gamers; harness mode initialize-leak-check asserts 0 freed; test InitializeWithoutAServiceSignsInNobody | NET |
| CNA-BUG-167 | CNA-BUG-167 | bug | LocalGamerServicesStore rounds 64-bit values through double and renames an unchecked temporary write over t... | RETIRE-FIXED | 38287637d (GS-AUDIT-005) integers stored exactly (LeaderboardWriterTest.OfflineIntegerBoundariesRoundTripExactly); 33e08899f (GS-AUDIT-001) checked write+rename (OfflineWriteFailurePreservesPreviousRecord) | NET |
| CNA-BUG-171 | CNA-BUG-171 | bug | LocalNetworkGamer::ReceiveData(PacketReader&, NetworkGamer*&) does not resize the reader, so a reused reade... | RETIRE-FIXED | 35ce1f3e8 (GS-007m): ReceiveData(PacketReader) resizes the reader; LocalNetworkGamerTest.ReceiveDataReturnsThePacketSizeAndRefusesWithoutDequeuing | NET |
| CNA-BUG-172 | CNA-BUG-172 | bug | A joined SystemLink session reports MaxGamers 31 and PrivateGamerSlots 4 instead of the host's values | RETIRE-FIXED | 4a1121e03 (GS-007n): host sends CurrentSettings after welcome; ENetBackendTest.AClientReportsTheHostsSettingsAndMachines | NET |
| CNA-BUG-173 | CNA-BUG-173 | bug | GamerPresence maps a presence mode to its display string through an alphabetically ordered table indexed by... | RETIRE-FIXED | ac56c4f50 (GS-005a): presenceModeStrings_ in enum order; ServiceReadLifetimeTest.PresenceChangedWhilePendingPublishesTheNewRevisionOnFollowingUpdate | NET |
| CNA-BUG-174 | CNA-BUG-174 | bug | LocalNetworkGamer::ReceiveData(PacketReader&, NetworkGamer*&) always returns 0 instead of the packet size | RETIRE-FIXED | 35ce1f3e8: ReceiveData returns size; same LocalNetworkGamerTest case | NET |
| CNA-BUG-233 | CNA-BUG-233 | bug | CLAUDE.md's Platform Boundary lists WIN32 as a reserved identifier that fails configuration, but cmake/Plat... | RETIRE-FIXED | 76c9bda29 rewrote CLAUDE.md platform list ("host-conditional WIN32"), matching PlatformSelection.cmake | DOC |
| CNA-BUG-236 | CNA-BUG-236 | bug | docs/platform-abstraction.md's Implementations table lists five backends and omits X11 and Wayland | RETIRE-FIXED | 76c9bda29: docs/platform-abstraction.md table now has X11 and WAYLAND rows | DOC |
| CNA-BUG-255 | NEW-AUDIT-07 | bug | EasyGL family: ClearColorAndStencil leaves the stencil write mask forced to all ones, so a later draw ignor... | RETIRE-FIXED | 731120eb9 (CCS-1): EasyGLRenderer::ClearColorAndStencil calls RestoreWriteMasksAfterClear(false,true); test EasyGL_Clear_RestoresStencilWriteMask (easygl_clear_restores_stencil_write_mask_test.cpp); OpenGL4 half gone (261cb5f7f); added entry -> needs retired_added | G1 |
| CNA-BUG-258 | NEW-AUDIT-10 | bug | LocalNetworkGamer::ReceiveData(byte buffer, offset) dequeues and silently truncates a packet larger than th... | RETIRE-FIXED | 35ce1f3e8: oversized packet -> ArgumentException, packet stays queued; same test; added entry -> needs retired_added | NET |
| CNA-BUG-265 | NEW-AUDIT-21 | bug | SignedInGamer::SignedIn does not replay already signed-in gamers to a late subscriber, unlike XNA 4.0 | RETIRE-FIXED | 6f61c5cb9 (GS-004n): SignedIn replay hook; SystemGuideTest.SignedInReplaysOnSubscribeAndSigningOutDisposesTheGamer; added entry -> needs retired_added | NET |
| CNA-BUG-266 | NEW-AUDIT-23 | bug | GamerServicesDispatcher::Initialize re-initialises silently when gamer services are already initialised, wh... | RETIRE-FIXED | 0ab6cc3fe: Initialize throws InvalidOperationException when already initialized; harness initialize-leak-check; added entry -> needs retired_added | NET |
| CNA-BUG-268 | NEW-AUDIT-25 | bug | A NetworkSession BeginCreate, BeginFind or BeginJoin callback that calls the matching End* frees the action... | RETIRE-FIXED | b7754e45f (GS-007e2b): InvokeActiveActionCallback keeps ownership until Begin returns; NetworkSessionTest.BeginCreateCallbackCanReentrantlyCallEndCreate; added entry -> needs retired_added | NET |
| CNA-GAP-001 | CNA-GAP-001 | functional-gap | ContentLoadException derives from std::runtime_error, not System::Exception, so no Sharp Runtime catch clau... | RETIRE-FIXED | 2d85a276f (KF-13): class ContentLoadException : public System::Exception (ContentLoadException.hpp:15); ContentRuntimeContractTests pin System::Exception | CORE |
| CNA-GAP-017 | CNA-GAP-017 | functional-gap | PresentationMode is stored but not honoured by FREEDIRECT (always letterbox), CANVAS (only FixedHeightDynam... | RETIRE-FIXED | CANVAS honours PresentationMode since 6f6100cd3 (FULLSCREEN-001; tests CanvasPresentation.*), DIRECTX9 since 9bbba48d8 (FULLSCREEN-002; CTests DirectX9_SpriteBatchPresentation, DirectX9_ResizeStateAndMotion); FREEDIRECT removed (0f96ea703) | G2 |
| CNA-GAP-051 | CNA-GAP-051 | functional-gap | Guide's fourteen Show* shell entry points and DelayNotifications are empty no-ops | RETIRE-FIXED | ac56c4f50, a482999e5, 45c23451b, 8abd5e029, 8559d5bd3: every Guide Show* opens a Guide screen, DelayNotifications defers; GuideSocialPaneTests/GuideUiTests/GuidePartyTests/GamerServicesServiceTests | NET |
| CNA-GAP-052 | CNA-GAP-052 | functional-gap | Local gamer services have no catalogue, presence or profile data: achievement metadata is empty, Achievemen... | RETIRE-FIXED | 529f22e45, 32c0002ff, ac56c4f50, 148d9db35, 4f7796e46: offline catalog, GetPicture, presence, privileges; SignedInGamerTest.AnOfflineCatalogListsEveryDefinedAchievementWithItsEarnedState, GuidePrivilegeTest.TheAccountsPolicyBecomesItsGamerPrivileges | NET |
| CNA-VGAP-009 | CNA-VGAP-009 | verification-gap | GraphicsDeviceManager's iOS/Android back-buffer orientation branch has no test | RETIRE-FIXED | 80572aa00 (CBIND-138) added GraphicsDeviceManagerOrientationTests.cpp (3 Android orientation/back-buffer tests) | BUILD |
| CNA-VGAP-040 | CNA-VGAP-040 | verification-gap | Avatar rendering evidence uses a synthetic one-bone quad; no renderer test draws the bundled 19-bone avatar... | RETIRE-FIXED | 3f4518e69 added avatar_standard_render_test.cpp (EasyGL_/Vulkan_AvatarRenderer_Standard: real catalog avatar drawn and read back); 13dfe0499 removed the EnableRealRenderingEXT surface | TEST |
| CNA-VGAP-055 | CNA-VGAP-055 | verification-gap | Process exit with live EasyGL-family resources whose creating thread has already ended is untested; a bindi... | RETIRE-FIXED | 0f7166cd8 (BINDFIX-041): HandleRegistry::~HandleRegistry leaves foreign-thread objects to the OS; test CApi_ExitWithForeignThreadGameSmoke (ExitWithForeignThreadGameSmoke.c); see also 00b9c9898, abd005ab8 | MISC |

### NARROWED (11)

| published id | key | class | title (short) | disposition | evidence at T | batch |
|---|---|---|---|---|---|---|
| CNA-BUG-041 | CNA-BUG-041 | bug | ContentManager resolves a relative RootDirectory against the working directory, not TitleLocation, and its ... | NARROWED | (already narrowed) 9976f4909 (CBIND-140) ResolveContentRoot under title path (ContentRootTests.cpp); 5d275f556 (BL-19) .cnb via TryReadAssetBytes; residue: StandardFileSystem::GetBasePath = current_path() on non-SDL3 platforms, std::filesystem::exists in ResolveAssetPath, ImageLoader ifstream on Android | MEDIA |
| CNA-BUG-122 | CNA-BUG-122 | bug | ContentManager::Load<T> leaks non-XNA exception types: std::bad_any_cast for a wrong .xnb type, unwrapped L... | NARROWED | 0af45cbd4 (KF-9) CastReadResult -> ContentLoadException (LoadingAsAnotherTypeThrowsContentLoadExceptionNotBadAnyCast); residue: Load<SoundEffect> unwrapped NotSupportedException, disposed manager std::runtime_error | MEDIA |
| CNA-BUG-148 | CNA-BUG-148 | bug | DynamicSoundEffectInstance::SubmitBuffer accepts empty and non-frame-aligned buffers that XNA rejects | NARROWED | 49119a34c (KF-12) SubmitBuffer refuses empty/partial frames (SubmitBufferRefusesPartialFrames*); residue: SubmitFloatBufferEXT (pinned by SubmitFloatBufferWithSampleCountNotDivisibleByChannelCountDoesNotThrow, AUD-07-006 open) | MEDIA |
| CNA-GAP-014 | CNA-GAP-014 | functional-gap | CANVAS and FREEDIRECT ignore GraphicsDevice.Viewport and ScissorRectangle, and SDL_RENDERER ignores Viewport | NARROWED | FREEDIRECT removed; CANVAS SetViewport since 6f6100cd3; CANVAS still no SetScissorRect; SDL_RENDERER still ignores Viewport | G2 |
| CNA-GAP-032 | CNA-GAP-032 | functional-gap | Engine-layer PBR limits: one punctual light per PbrEffect draw, 8-bit environment cubes, no back-face norma... | NARROWED | 5572f3ca1 removed EnvironmentProcessor/shadow_caster; a1414a1b0 (GSC-0010) back-face flip on EasyGL only (easygl_pbr_double_sided_test); one PunctualLightEXT unchanged | G2 |
| CNA-GAP-053 | CNA-GAP-053 | functional-gap | Voice chat, party invites, NetworkMachine::RemoveFromSession, arbitration/TrueSkill events and QualityOfSer... | NARROWED | voice b1d44dc94; party invites 8559d5bd3/35ce1f3e8; RemoveFromSession ea10f1f5c; events 062cbe193/db71f60b4; SystemLink QoS b4a378b90/122922f52; residue: PlayerMatch/Ranked listing QoS never measured (limitations section 17) | NET |
| CNA-GAP-071 | NEW-AUDIT-17 | functional-gap | GraphicsDevice is single-threaded: its resource registry has no lock and only EasyGL and OpenGL4 lease a co... | NARROWED | 00b9c9898 (KF-1/1a) resourcesMutex_ + LeaseRendererContext; a033a9184 (KF-16); 5b4edd6cc (BINDFIX-050); only EasyGL implements AcquireThreadContextLeaseEXT; added entry (NEW-AUDIT-17) -> edit inside added[] | G2 |
| CNA-PLAT-003 | CNA-PLAT-003 | platform-limitation | EasyGL on GLES/WebGL contexts without GL_NV_polygon_mode or WEBGL_polygon_mode refuses wireframe triangle d... | NARROWED | 251bf6c98, 96b5038de (SAMPLE-048), cefe6c83b (SAMPLE-055) add two line-loop wireframe routes (EasyGLUnsupportedWireFrameTest.*); all other WireFrame triangle draws still throw | G2 |
| CNA-PLAT-011 | CNA-PLAT-011 | platform-limitation | Under Emscripten nothing mounts a persistent file system, so saves and the local gamer-services store are l... | NARROWED | 8a67da536 + c5986156d: IDBFS mounted at /cna-storage and /save before main(); residue: threaded WasmFS builds (default) have no persistence and StorageDevice refuses | NET |
| CNA-VGAP-011 | CNA-VGAP-011 | verification-gap | No test exercises PlatformSelection.cmake's reserved-identifier and unknown-name refusal paths | NARROWED | 6ee00e35d CnaPlatformSelection_SDL2 covers the unknown-name refusal; reserved-identifier branch (SDL12, EMSCRIPTEN, WIN32 off Windows, TERMINAL on Windows) still untested | BUILD |
| CNA-VGAP-041 | CNA-VGAP-041 | verification-gap | The CNA_STRICT_XNA_API purity check compiles only the Microsoft::Devices sensor surface | NARROWED | 577fb0674 (BL-16), 2c70eaf0f (BL-18) widen StrictXnaApiSurfaceCheck.cpp (CNAEXT using-line placement + SamplerStates setter compile); leak twin still Accelerometer only | TEST |

### CHANGED (31)

| published id | key | class | title (short) | disposition | evidence at T | batch |
|---|---|---|---|---|---|---|
| CNA-BUG-016 | CNA-BUG-016 | bug | The .cnj JSON parser (CNA::Internal::ParseJson) recurses without a nesting limit, so a small crafted docume... | CHANGED | 38287637d (GS-AUDIT-005) moved store files to nlohmann::json; ParseJson now reached only by ParseOfflineCatalog (529f22e45); Json.hpp unchanged | MEDIA |
| CNA-BUG-035 | CNA-BUG-035 | bug | devices-tests.yml's exact-name gtest filters skip seven Microsoft::Devices suites and never match the FileD... | CHANGED | 31a560af9 (INPUT-EMU-001) added KeyboardAccelerometerTest (4) not in the filter: 33 of 478 missed, eight suites | BUILD |
| CNA-BUG-050 | CNA-BUG-050 | bug | Guide message-box and keyboard-input results cannot be waited on: GamerServicesDispatcher::Update pumps not... | CHANGED | Update now pumps service (0ab6cc3fe, 73011288e); End* waits via modal frames (70d6f109e); GuideAction wait handle still constructed signalled | NET |
| CNA-BUG-055 | CNA-BUG-055 | bug | Stale whole-registry renderer counts survive outside check_renderer_identities.py's list: the C API's CORE.... | CHANGED | 18 public identities / 14 families at T; CNA_GRAPHICS_RENDERER_MAXIMUM = FNA3D 43; stale counts (50, 46, 42, 49) still present; the "25" now stale too | DOC |
| CNA-BUG-056 | CNA-BUG-056 | bug | docs/c-api/FEATURE_MATRIX.md and docs/c-api/README.md still present the C ABI as version 0.1.0 while abi.h ... | CHANGED | abi.h declares 0.44.0 (was 0.29.0); FEATURE_MATRIX.md/README.md still 0.1.0 | DOC |
| CNA-BUG-058 | CNA-BUG-058 | bug | LIMITATIONS.md omits the 468 planned C API symbols and RELEASE_GATE.md still attributes 654 declarations to... | CHANGED | LIMITATIONS.md: 8,142 declared, 7,030+15+441=7,486; COVERAGE 656 planned; release_gate.json still says 654 under CBIND-117 | DOC |
| CNA-BUG-081 | CNA-BUG-081 | bug | Game::InactiveSleepTime is stored and validated but the loop never sleeps while the game is inactive | CHANGED | 16a1b67d9 (KF-15): setter throws ArgumentOutOfRangeException with XNA text and has a test; loop still never sleeps while inactive | CORE |
| CNA-BUG-094 | CNA-BUG-094 | bug | SDL_GPU claims compute and SPIR-V shader intake on every device, including Direct3D 12 and Metal drivers th... | CHANGED | SDL_GPU still claims compute/SPIR-V on D3D12/Metal; public ComputeShader removed by 5572f3ca1 -> rewrite contract/blast radius around ShaderEffect SPIR-V payloads | G1 |
| CNA-BUG-099 | CNA-BUG-099 | bug | 24 classic SDL_GPU CTests still fail in CNA's latest recorded run; CNA's records name a cause for only thre... | CHANGED | d111906f7 (STREETPERF-0002) plan_street_perf.md: 25 of 238 ^SdlGpu failing, unnamed; cause for two SdlGpuIndexedDrawRangeTest cases | G1 |
| CNA-BUG-115 | CNA-BUG-115 | bug | DIRECTX9 requests D3DPRESENT_INTERVAL_TWO without checking device support, and a failing Reset is then retr... | CHANGED | 6f6100cd3 (FULLSCREEN-001): TryBeginDrawEXT runs EnsureDeviceSize and refuses frames while presentationDirty_ -> Draw and Present skipped every frame | G1 |
| CNA-BUG-118 | CNA-BUG-118 | bug | GraphicsDevice::GetMaxTextureDimension() is documented as the renderer's real maximum, but most renderers r... | CHANGED | only VULKAN reports a real limit at T (Direct2D/GDI gone); StorageTexture2D/Texture2DArray removed by 5572f3ca1; C API texture route checks the value | G1 |
| CNA-BUG-133 | CNA-BUG-133 | bug | DIRECTX11, DIRECTX12, FREEDIRECT and METAL implement the window-to-logical transform but never register for... | CHANGED | FREEDIRECT removed (0f96ea703); 9bbba48d8 (FULLSCREEN-002) added DirectX9 TransformWindowToLogical without RegisterForWindow -> list becomes DIRECTX9, DIRECTX11, DIRECTX12, METAL | MISC |
| CNA-BUG-150 | CNA-BUG-150 | bug | StorageDevice::EnsureStorageRoot publishes its initialised flag before the root, without synchronisation | CHANGED | 8a67da536 fixed store order; statics still unsynchronised (StorageDevice.hpp 178-180) | NET |
| CNA-BUG-190 | CNA-BUG-190 | bug | modules/renderers/CMakeLists.txt enters common/d3d, the GDI software sources and the Metal renderer target ... | CHANGED | GDI half gone (261cb5f7f, 590ac27c8; PORTABLEGL/GDI combination rules removed); common/d3d and METAL conditions unchanged; folded CNA-BUG-187 must be patched too | BUILD |
| CNA-BUG-192 | CNA-BUG-192 | bug | metal-macos-ci.yml's push path filter names three CMake files that no longer exist and omits the files that... | CHANGED | workflow count 20 -> 18; three dead cmake paths still in metal-macos-ci.yml filter | BUILD |
| CNA-BUG-199 | CNA-BUG-199 | bug | Six CI workflows pin August 2026 sharp-runtime commits that lack components CNA's default closure requests ... | CHANGED | htmldom-ci.yml and gdi-windows-ci.yml deleted (261cb5f7f): five workflows with stale pins | BUILD |
| CNA-BUG-213 | CNA-BUG-213 | bug | audio.h and AUDIO.md call cna_dynamic_sound_effect_instance_submit_buffer safe from a producer thread, but ... | CHANGED | default unchanged (CNA_RESULT_THREAD); new opt-in cna_game_set_foreign_thread_calls_ext (0a57ccad2, CBIND-141, ABI 0.39.0); CBIND-154 lifts thread rule only for cna_sound_effect_play* | MISC |
| CNA-GAP-004 | CNA-GAP-004 | functional-gap | Game::ShowMissingRequirementMessage is a virtual hook that nothing in CNA calls | CHANGED | a71cc2415 (CBIND-144) CreateGameGraphicsDevice converts device-creation failures to NoSuitableGraphicsDeviceException in the constructor; hook still never called | CORE |
| CNA-GAP-008 | CNA-GAP-008 | functional-gap | SDL_GPU ShaderEffect draws bind only the first vertex stream, and the limitation report misstates ShaderEff... | CHANGED | SDL_GPU custom-effect draw still binds slot 0 only; StorageBuffer/ParticleSystem public API gone (5572f3ca1) | G1 |
| CNA-GAP-009 | CNA-GAP-009 | functional-gap | Sub-pixel SpriteBatch destinations reach only EasyGL, OPENGL4 and SOFTWARE; every other renderer truncates ... | CHANGED | float-destination Draw overridden only by EasyGL and SOFTWARE at T (OPENGL4 gone); sources: drop OpenGL4SpriteBatch.cpp | G1 |
| CNA-GAP-047 | CNA-GAP-047 | functional-gap | XACT wave-bank entries compressed as XMA/XMA2 or WMA produce no sound | CHANGED | 9d04c6702 (BINDFIX-051): warning now via LogAudio at WARN, not std::cerr; still returns nullptr | MEDIA |
| CNA-GAP-062 | CNA-GAP-062 | functional-gap | The C ABI has no route for 468 public C++ declarations that the coverage inventory records as planned | CHANGED | COVERAGE.md at T: 656 planned (was 468); RELEASE_GATE "CNA C ABI 0.44.0 ... 656 public symbols are still unmapped"; module breakdown graphics 275, content 206, graphics-ext 40 ... | MISC |
| CNA-GAP-070 | NEW-AUDIT-14 | functional-gap | NetworkSession's Begin/End pairs are synchronous: the result is complete and the callback has run when Begi... | CHANGED | b7754e45f made service PlayerMatch/Ranked and JoinInvited genuinely pending; Local/SystemLink still synchronous; added entry (NEW-AUDIT-14) -> edit inside added[] | NET |
| CNA-PLAT-014 | CNA-PLAT-014 | platform-limitation | Compass and Motion work only on Android; desktop sensors come only through the SDL3 platform, and web targe... | CHANGED | 31a560af9 (INPUT-EMU-001) opt-in keyboard Accelerometer emulation: IsSupported true everywhere while on | BUILD |
| CNA-VGAP-008 | CNA-VGAP-008 | verification-gap | Android and iOS have no device evidence at this snapshot: no Android workflow, one iOS simulator frame, and... | CHANGED | commit records of manual Android-emulator runs (BL-19 5d275f556, BL-21 016c588bf, CBIND-139 1dc4ce06a); CBIND-140 relative root resolution | BUILD |
| CNA-VGAP-021 | CNA-VGAP-021 | verification-gap | No SpriteFont/DrawString pixel test exists for DIRECTX9, DIRECT2D, GDI, METAL, CANVAS, SVG_DOM, PORTABLEGL ... | CHANGED | seven renderers retired; DIRECTX11/12 now register sprite_font parity fixture; residue DIRECTX9, METAL, CANVAS, FNA3D | TEST |
| CNA-VGAP-023 | CNA-VGAP-023 | verification-gap | Most browser renderer paths are never executed automatically: WEBGL1/WEBGL2 have no test registrations, CAN... | CHANGED | 261cb5f7f removed htmldom-ci.yml and browser scripts; emscripten bundle WEBGL2+WEBGL1+CANVAS linked, never run; folded CNA-VGAP-045 must be patched | TEST |
| CNA-VGAP-026 | CNA-VGAP-026 | verification-gap | The Windows renderer families have no automatic native Windows execution: DIRECTX9 has no CI job, the DIREC... | CHANGED | d3d-windows-ci.yml: workflow_dispatch only, [DIRECTX11, DIRECTX12]; GDI/D2D lanes removed; folded CNA-VGAP-043 must be patched | TEST |
| CNA-VGAP-039 | CNA-VGAP-039 | verification-gap | The process-spawning networking tests are compiled out on Windows, Emscripten, Android and iOS, and multi-m... | CHANGED | TwoProcessLoopbackTest.cpp has 8 TESTs (was 3); exclusions unchanged | TEST |
| CNA-VGAP-044 | CNA-VGAP-044 | verification-gap | Wine test routes and the DIRECTX12 Proton route do not prove which Direct3D or Direct2D implementation serv... | CHANGED | direct2d examples/scripts/pin removed (0f96ea703); D3D Wine/Proton gate skips unchanged | TEST |
| CNA-VGAP-047 | CNA-VGAP-047 | verification-gap | Test strength is never measured automatically: no coverage build, no scheduled fuzzing campaign, and the Di... | CHANGED | direct2d_mutation_check.py gone; cnaext-coverage.md marked historical (5572f3ca1); fuzz harnesses unchanged | TEST |

### EDIT (39)

| published id | key | class | title (short) | disposition | evidence at T | batch |
|---|---|---|---|---|---|---|
| CNA-BUG-002 | CNA-BUG-002 | bug | BoundingSphere::Contains(const BoundingFrustum&) never returns Disjoint | EDIT | blast_radius names removed FrustumCullerEXT/ClusteredShadowPolicyEXT (5572f3ca1); field comes from patches.json | CORE |
| CNA-BUG-003 | CNA-BUG-003 | bug | BoundingBox::Contains(const BoundingFrustum&) never returns Disjoint and answers Contains when only the fir... | EDIT | blast_radius "culling helpers" (5572f3ca1) | CORE |
| CNA-BUG-004 | CNA-BUG-004 | bug | BoundingFrustum::Intersects(Ray) never computes an entry distance: rays starting outside always miss, and a... | EDIT | blast_radius "culling helpers in graphics-ext" (GpuInstanceCuller removed, 5572f3ca1) | CORE |
| CNA-BUG-012 | CNA-BUG-012 | bug | Two tests still encode the wrong occlusion-query expectation for SDL_GPU after the renderer was made truthful | EDIT | drop PORTABLEGL arm | TEST |
| CNA-BUG-071 | CNA-BUG-071 | bug | BoundingFrustum::Intersects differs from XNA 4.0: box and sphere overloads use a conservative plane test, a... | EDIT | drop missing source graphics-ext/src/FrustumCullerEXT.cpp and its mention | CORE |
| CNA-BUG-078 | CNA-BUG-078 | bug | Game::PollEvents fires the renderer's test-only context-loss hooks on F9/F10 in every build | EDIT | drop Direct2D/GDI hook overrides (renderers removed); evidence part lives in an adversarial append | CORE |
| CNA-BUG-090 | CNA-BUG-090 | bug | GraphicsDeviceInformation accepts a null Adapter, and GraphicsDeviceManager then binds a reference through ... | EDIT | variable name "gdi" trips check_retired_renderers -> reword summary/actual | CORE |
| CNA-BUG-101 | CNA-BUG-101 | bug | GraphicsDevice::Reset rolls back only the window and virtual-resolution stage; a later renderer failure lea... | EDIT | example renderer Direct2D removed -> use DirectX11Renderer::ApplyMultiSampleCount | G1 |
| CNA-BUG-107 | CNA-BUG-107 | bug | DIRECTX9 draws a 3D ShaderEffect with the stock BasicEffect shader (16-byte vertices) or fails with a Basic... | EDIT | PostProcessPass removed (5572f3ca1) -> neutral wording | G1 |
| CNA-BUG-111 | CNA-BUG-111 | bug | ShaderEffect::SetTexture(int, Texture2D&), SetTexture(int, TextureCube&) and SetTexture(int, Texture3D&) ev... | EDIT | drop OpenGL4 mention | G1 |
| CNA-BUG-113 | CNA-BUG-113 | bug | An enabled zero-area ScissorRectangle draws unclipped on VULKAN and SDL_GPU, while WEBGPU clips everything ... | EDIT | drop OPENGL4 from fixture list (2 occurrences) | G1 |
| CNA-BUG-134 | CNA-BUG-134 | bug | Inside a letterbox bar, Mouse::GetState reports the raw window coordinate on renderers whose transform decl... | EDIT | GlPresentationSurfaceState.hpp moved to modules/renderers/easygl/include/CNA/Internal/Renderers/EasyGL/ (261cb5f7f); drop OPENGL4/SVG_DOM/HTML_DOM/GDI/Direct2D/FREEDIRECT | MISC |
| CNA-BUG-140 | CNA-BUG-140 | bug | MediaPlayer::Play reports no error when a song cannot be played and can leave the player Playing with no track | EDIT | "SDL2 or NULL audio" -> "NULL audio" (76c9bda29) | MEDIA |
| CNA-BUG-142 | CNA-BUG-142 | bug | Without a mixer (SDL2 or NULL audio) songs never end: queued copies carry no Duration, so the elapsed-time ... | EDIT | title/contract/actual/blast/workaround drop SDL2 audio (76c9bda29) | MEDIA |
| CNA-BUG-168 | CNA-BUG-168 | bug | LocalGamerServicesStore maps distinct gamertags to one achievements file when they differ only in character... | EDIT | ac961f433 isValidLocalGamertag limits Guide profiles; blast radius narrower | NET |
| CNA-BUG-177 | CNA-BUG-177 | bug | The Headless and Terminal window constructors accept BorderlessFullscreen although their own SetFullscreenM... | EDIT | drop SDL2 platform from CreateWindow list | BUILD |
| CNA-BUG-180 | CNA-BUG-180 | bug | Win32GlContext ignores multisample and per-channel format requests and reports the requested description as... | EDIT | drop OpenGL4 RequestedContext | BUILD |
| CNA-BUG-202 | CNA-BUG-202 | bug | In a multi-renderer build, non-default renderers' example CTests are registered but run under the default r... | EDIT | drop OpenGL4 precedent and opengl4_smoke_test.cpp source | TEST |
| CNA-BUG-224 | CNA-BUG-224 | bug | GraphicsDevice's DeviceLost documentation and device-status comments still say only Direct3D 9 reports devi... | EDIT | Direct2D raise site removed -> four families; source Direct2DRenderer.cpp -> DirectX9Renderer.cpp | DOC |
| CNA-BUG-250 | CNA-GAP-050 | bug | LocalNetworkGamer::SendData in a Local or LocalWithLeaderboards session silently drops every packet, so nei... | EDIT | service-backed PlayerMatch/Ranked also deliver; known_gaps.md rewritten -> drop that source; patch under stable key CNA-GAP-050 | NET |
| CNA-BUG-253 | NEW-AUDIT-03 | bug | SdlGpu_ConstructorExceptionSafety aborts with a double free, a defect CNA's own record calls real and leave... | EDIT | STREETPERF-0002 unnamed 25 failures; added entry (NEW-AUDIT-03) -> edit inside added[] | G1 |
| CNA-BUG-264 | NEW-AUDIT-20 | bug | Vulkan passes XNA's normalised RasterizerState.DepthBias to vkCmdSetDepthBias unscaled, so a realistic bias... | EDIT | OpenGL4/PortableGL removed; scale reference -> EasyGLDepthBiasToPolygonOffsetUnits; misc/known_bugs.md now lists directx11+vulkan; added entry (NEW-AUDIT-20) -> edit inside added[] | G1 |
| CNA-GAP-006 | CNA-GAP-006 | functional-gap | GraphicsDeviceManager never calls its FindBestDevice, RankDevices or CanResetDevice virtuals | EDIT | "default GDI" (GraphicsDeviceInformation) trips the checker -> reword | CORE |
| CNA-GAP-010 | CNA-GAP-010 | functional-gap | SpriteSortMode::Immediate does not submit each sprite as it is drawn on VULKAN, SDL_GPU, the Direct3D famil... | EDIT | drop OPENGL4 (EasyGL, FNA3D, SOFTWARE submit per Draw); drop OpenGL4SpriteBatch.cpp source | G1 |
| CNA-GAP-012 | CNA-GAP-012 | functional-gap | On HEADLESS, TextureCube::SetData throws NotSupportedException because the headless cube renderer stores no... | EDIT | test gate now CubeStorageSupported(): SdlRenderer, Canvas, Headless | G2 |
| CNA-GAP-021 | CNA-GAP-021 | functional-gap | DIRECTX9 BasicEffect reaches only 12 of its 32 shader variants; other combinations throw 'no matching CNA v... | EDIT | d3d-windows-ci matrix [DIRECTX11, DIRECTX12] (no DIRECT2D) | G2 |
| CNA-GAP-023 | CNA-GAP-023 | functional-gap | On DIRECTX9 a Texture2D can only be created with SurfaceFormat::Color | EDIT | drop OPENGL4 | G2 |
| CNA-GAP-028 | CNA-GAP-028 | functional-gap | The METAL renderer applies KHR_materials_specular factors only and samples neither specular texture | EDIT | drop OpenGL4 (RRC-017 3b9982646 dropped it from gltf-limitations.md) | G2 |
| CNA-GAP-033 | CNA-GAP-033 | functional-gap | CNA has no counterpart of XNA's MissingVertexShaderInput draw check, and renderers resolve a stock-effect d... | EDIT | drop OPENGL4 text and OpenGL4StockDraw.cpp source | G2 |
| CNA-GAP-059 | CNA-GAP-059 | functional-gap | In a MinGW-w64 cross tree CnaTests gets a Wine CROSSCOMPILING_EMULATOR only when the default renderer is DI... | EDIT | DIRECT2D emulator branch removed (0f96ea703) | BUILD |
| CNA-GAP-064 | CNA-BUG-100 | functional-gap | WEBGPU does not propagate a real device loss: OnDeviceLost only logs, so DeviceLost, the device status and ... | EDIT | drop Direct2D from DeviceLost raisers; patch under stable key CNA-BUG-100 | G2 |
| CNA-GAP-065 | CNA-BUG-108 | functional-gap | The renderer capability profile has no feature for pre-compiled SPIR-V payloads, so SDL_GPU and VULKAN repo... | EDIT | (optional) engine-layer wording; patch under stable key CNA-BUG-108 | G2 |
| CNA-PLAT-001 | CNA-PLAT-001 | platform-limitation | CANVAS, FREEDIRECT, SDL_RENDERER, HTML_DOM and SVG_DOM throw for any Texture2D mip level above 0, so mipmap... | EDIT | only CANVAS and SDL_RENDERER remain (FREEDIRECT/HTML_DOM/SVG_DOM removed); source freedirect -> SdlRenderer.cpp; test SDL_Renderer_Texture2D_MipLevelThrows | G2 |
| CNA-VGAP-012 | CNA-VGAP-012 | verification-gap | No CI workflow selects CNA_PLATFORM=WAYLAND, so the native Wayland backend's suites run only on a developer... | EDIT | platform-ci matrix lost SDL2 cell (76c9bda29) | BUILD |
| CNA-VGAP-022 | CNA-VGAP-022 | verification-gap | No test measures presentation cadence: PresentInterval::Two against ordinary vsync, or Vulkan's FIFO_RELAXE... | EDIT | drop OPENGL4 registrations | TEST |
| CNA-VGAP-025 | CNA-VGAP-025 | verification-gap | No CI workflow selects WEBGPU or SDL_GPU; WebGPU evidence is local Linux and scripted headless Chrome, and ... | EDIT | drop OPENGL4/FREEDIRECT paragraph and opengl4 source; folded CNA-VGAP-048 must be patched | TEST |
| CNA-VGAP-030 | CNA-VGAP-030 | verification-gap | Model drawing on VULKAN, SOFTWARE and the Direct3D renderers is checked in CI only at the stride draw bound... | EDIT | drop OPENGL4 and dead EasyGLParityCorpus.cmake token | TEST |
| CNA-VGAP-056 | NEW-AUDIT-05 | verification-gap | The checked-in shader bytecode headers of VULKAN, SDL_GPU and the Direct3D renderers come from generators t... | EDIT | tests_current cited retiring CNA-VGAP-017; related links to engine pages; added entry (NEW-AUDIT-05) -> edit inside added[] | TEST |
| CNA-VGAP-059 | NEW-AUDIT-19 | verification-gap | The VibrateController shutdown-ordering tests never open a haptic device or destroy a Game-owned SDL3 platf... | EDIT | SDL2-only exclusion gone (76c9bda29); added entry (NEW-AUDIT-19) -> edit inside added[] | TEST |

## 2. STILL VALID (242): defect unchanged at T; no text change required

Each batch appendix records what was re-checked at T for every one of these entries. Optional notes: CNA-BUG-181 and CNA-BUG-274 link `docs/cnaext-engine.html`, labelled "CNAEXT engine layer", so relabel or retarget the link if that page changes. CNA-VGAP-054 and CNA-BUG-267 have optional one-sentence appends; see the MISC and NET appendices.

- **bug** (161): CNA-BUG-001, CNA-BUG-006, CNA-BUG-008, CNA-BUG-017, CNA-BUG-021, CNA-BUG-022, CNA-BUG-025, CNA-BUG-026, CNA-BUG-027, CNA-BUG-028, CNA-BUG-029, CNA-BUG-036, CNA-BUG-045, CNA-BUG-047, CNA-BUG-049, CNA-BUG-052, CNA-BUG-054, CNA-BUG-057, CNA-BUG-061, CNA-BUG-063, CNA-BUG-064, CNA-BUG-065, CNA-BUG-066, CNA-BUG-067, CNA-BUG-068, CNA-BUG-069, CNA-BUG-070, CNA-BUG-072, CNA-BUG-073, CNA-BUG-074, CNA-BUG-075, CNA-BUG-076, CNA-BUG-080, CNA-BUG-082, CNA-BUG-083, CNA-BUG-085, CNA-BUG-086, CNA-BUG-087, CNA-BUG-088, CNA-BUG-091, CNA-BUG-092, CNA-BUG-093, CNA-BUG-095, CNA-BUG-096, CNA-BUG-102, CNA-BUG-103, CNA-BUG-104, CNA-BUG-105, CNA-BUG-106, CNA-BUG-110, CNA-BUG-112, CNA-BUG-114, CNA-BUG-116, CNA-BUG-117, CNA-BUG-119, CNA-BUG-120, CNA-BUG-121, CNA-BUG-123, CNA-BUG-124, CNA-BUG-125, CNA-BUG-126, CNA-BUG-128, CNA-BUG-129, CNA-BUG-130, CNA-BUG-131, CNA-BUG-132, CNA-BUG-135, CNA-BUG-137, CNA-BUG-138, CNA-BUG-139, CNA-BUG-141, CNA-BUG-143, CNA-BUG-144, CNA-BUG-145, CNA-BUG-146, CNA-BUG-147, CNA-BUG-149, CNA-BUG-152, CNA-BUG-153, CNA-BUG-154, CNA-BUG-155, CNA-BUG-156, CNA-BUG-157, CNA-BUG-158, CNA-BUG-159, CNA-BUG-160, CNA-BUG-161, CNA-BUG-162, CNA-BUG-163, CNA-BUG-164, CNA-BUG-169, CNA-BUG-170, CNA-BUG-176, CNA-BUG-179, CNA-BUG-181, CNA-BUG-182, CNA-BUG-183, CNA-BUG-184, CNA-BUG-185, CNA-BUG-186, CNA-BUG-191, CNA-BUG-193, CNA-BUG-196, CNA-BUG-197, CNA-BUG-198, CNA-BUG-201, CNA-BUG-203, CNA-BUG-204, CNA-BUG-205, CNA-BUG-206, CNA-BUG-207, CNA-BUG-208, CNA-BUG-209, CNA-BUG-210, CNA-BUG-211, CNA-BUG-212, CNA-BUG-214, CNA-BUG-215, CNA-BUG-216, CNA-BUG-217, CNA-BUG-218, CNA-BUG-220, CNA-BUG-221, CNA-BUG-222, CNA-BUG-223, CNA-BUG-225, CNA-BUG-227, CNA-BUG-228, CNA-BUG-229, CNA-BUG-230, CNA-BUG-231, CNA-BUG-232, CNA-BUG-234, CNA-BUG-235, CNA-BUG-237, CNA-BUG-238, CNA-BUG-239, CNA-BUG-240, CNA-BUG-241, CNA-BUG-242, CNA-BUG-243, CNA-BUG-244, CNA-BUG-245, CNA-BUG-246, CNA-BUG-247, CNA-BUG-248, CNA-BUG-251, CNA-BUG-252, CNA-BUG-254, CNA-BUG-256, CNA-BUG-259, CNA-BUG-260, CNA-BUG-261, CNA-BUG-262, CNA-BUG-263, CNA-BUG-267, CNA-BUG-269, CNA-BUG-271, CNA-BUG-272, CNA-BUG-273, CNA-BUG-274
- **functional-gap** (41): CNA-GAP-002, CNA-GAP-003, CNA-GAP-005, CNA-GAP-007, CNA-GAP-011, CNA-GAP-013, CNA-GAP-015, CNA-GAP-016, CNA-GAP-018, CNA-GAP-019, CNA-GAP-020, CNA-GAP-022, CNA-GAP-024, CNA-GAP-026, CNA-GAP-034, CNA-GAP-035, CNA-GAP-036, CNA-GAP-037, CNA-GAP-038, CNA-GAP-039, CNA-GAP-040, CNA-GAP-041, CNA-GAP-042, CNA-GAP-043, CNA-GAP-044, CNA-GAP-045, CNA-GAP-046, CNA-GAP-048, CNA-GAP-049, CNA-GAP-054, CNA-GAP-055, CNA-GAP-056, CNA-GAP-057, CNA-GAP-058, CNA-GAP-060, CNA-GAP-061, CNA-GAP-063, CNA-GAP-066, CNA-GAP-067, CNA-GAP-068, CNA-GAP-069
- **platform-limitation** (6): CNA-PLAT-002, CNA-PLAT-004, CNA-PLAT-005, CNA-PLAT-009, CNA-PLAT-012, CNA-PLAT-013
- **verification-gap** (34): CNA-VGAP-001, CNA-VGAP-002, CNA-VGAP-003, CNA-VGAP-004, CNA-VGAP-005, CNA-VGAP-006, CNA-VGAP-007, CNA-VGAP-013, CNA-VGAP-014, CNA-VGAP-015, CNA-VGAP-016, CNA-VGAP-019, CNA-VGAP-020, CNA-VGAP-024, CNA-VGAP-027, CNA-VGAP-028, CNA-VGAP-029, CNA-VGAP-031, CNA-VGAP-032, CNA-VGAP-033, CNA-VGAP-034, CNA-VGAP-035, CNA-VGAP-036, CNA-VGAP-037, CNA-VGAP-038, CNA-VGAP-046, CNA-VGAP-049, CNA-VGAP-051, CNA-VGAP-052, CNA-VGAP-053, CNA-VGAP-054, CNA-VGAP-057, CNA-VGAP-058, CNA-VGAP-060

**Check:** 128 action + 242 still valid = 370 entries; per disposition {'RETIRE-OBSOLETE': 23, 'RETIRE-FIXED': 24, 'NARROWED': 11, 'CHANGED': 31, 'EDIT': 39}.

## 3. Cross-cutting checks to run after patching

- **Retired-renderer spellings.** These are DIRECT2D, FREEDIRECT, GDI, HTML_DOM, OPENGL4, PORTABLEGL and SVG_DOM, in any spelling: `gdi`, `Gdi`, `OpenGL4…`, `html-dom`, `HtmlDom`, `portablegl/…`.
  - 54 entries carry them; per-field hits are in `r9work/rrhits.json`. Every one is retired or edited in §1.
  - Four are hidden traps:
    - CNA-BUG-090 and CNA-GAP-006 use `gdi` or "GDI" for GraphicsDeviceInformation.
    - CNA-BUG-012 has a PORTABLEGL arm.
    - CNA-GAP-012 has a test-gate list.
  - Re-run `check_retired_renderers.py` after `known_issues.py merge && build`.
- **Source paths missing at T: 49 entries.** All are handled by a retirement or a replacement `sources` list in §1.
  - CNA-BUG-134's file moved to `modules/renderers/easygl/include/CNA/Internal/Renderers/EasyGL/GlPresentationSurfaceState.hpp`, renamed in 261cb5f7f.
- **Dead `{{src:}}`/`{{tree:}}` tokens in HTML fields: 33 entries** (`r9work/deadtokens.json`). All are retired, or their batch appendix replaces the token.
- **`related` links to site pages about removed subjects.** These stay valid only while the pages exist. Check them if the documentation update deletes or retargets the pages:
  - `docs/cnaext-engine.html` is linked from CNA-BUG-181 and CNA-BUG-274 (both still valid), and from CNA-BUG-094 and CNA-GAP-032 (that link is dropped in their edits).
  - `deep-dives/reference/cnaext-catalog.html` is linked from CNA-BUG-075, CNA-BUG-092 and CNA-VGAP-041.
  - `development/internals/modules/graphics-ext.html` is linked from CNA-VGAP-056 (dropped in its edit).
  - `docs/tutorials/105-browser-renderers.html` is linked from CNA-BUG-199.
  - `deep-dives/renderers/browser-dom-renderers.html` is linked from CNA-VGAP-023 (drop it).
  - `deep-dives/renderers/windows-2d-renderers.html#d2d-tests` is linked from CNA-VGAP-026 (drop it).
  - `development/internals/platforms/sdl2.html` is linked only from entries that are being retired (BUG-178, 194, 195).
  - `development/internals/audio/engine.html` is the audio engine and is unaffected.
- **Hand-written site references to the 47 retiring entries.** These pages are outside `known-issues/` and were scanned in the current working tree. `issue_refs.py check` and link validation will fail until they are edited:
  - CNA-BUG-062: development/handbook/update-the-c-api.html, development/internals/bindings/c-api-internals.html, development/testing/architecture.html, docs/c-api.html, docs/roadmap.html
  - CNA-BUG-077: development/internals/graphics/selection.html, development/internals/modules/core.html, docs/runtime-renderer-selection.html
  - CNA-BUG-097: development/architecture/graphics.html, development/internals/modules/graphics-ext.html, docs/cnaext-extensions.html
  - CNA-BUG-098: development/handbook/debug-shutdown-and-lifetime.html, development/internals/modules/graphics-ext.html, docs/cnaext-extensions.html
  - CNA-BUG-109: development/internals/modules/graphics-ext.html
  - CNA-BUG-151: development/internals/modules/storage.html, development/takeover/case-study-storage.html, docs/storage.html
  - CNA-BUG-165: development/internals/modules/gamer-services.html, docs/tutorials/123-achievements.html
  - CNA-BUG-166: development/internals/modules/gamer-services.html, development/takeover/ownership.html
  - CNA-BUG-167: development/internals/modules/gamer-services.html, docs/tutorials/123-achievements.html
  - CNA-BUG-171: development/internals/modules/net.html
  - CNA-BUG-172: development/internals/modules/net.html, docs/tutorials/97-networking.html
  - CNA-BUG-173: deep-dives/services/gamer-services-contract.html, development/internals/modules/gamer-services.html
  - CNA-BUG-174: development/internals/modules/net.html
  - CNA-BUG-178: development/internals/input/events.html, docs/input.html
  - CNA-BUG-189: development/build/architecture.html, development/repository/module-graph.html
  - CNA-BUG-194 and CNA-BUG-195: development/handbook/change-build-configuration.html, docs/platforms.html
  - CNA-BUG-200: development/internals/platforms/wayland.html, development/testing/index.html
  - CNA-BUG-233: development/build/index.html, development/internals/platforms/win32.html, docs/native-platforms.html
  - CNA-BUG-236: development/architecture/platform.html, development/internals/platforms/index.html, docs/native-platforms.html
  - CNA-BUG-249: development/internals/graphics/backends.html, development/maintenance.html, docs/effects.html, docs/tutorials/114-pbr-materials.html
  - CNA-BUG-255: development/internals/graphics/easygl.html, docs/graphics-state.html
  - CNA-BUG-257: development/internals/graphics/backends.html, docs/graphics-state.html
  - CNA-BUG-258: development/internals/modules/net.html, docs/xna-compatibility.html
  - CNA-BUG-265: docs/xna-compatibility.html
  - CNA-BUG-268: deep-dives/services/network-sessions.html (including marker `<!--issue:NEW-AUDIT-25-->`)
  - CNA-BUG-270: deep-dives/reference/native-c-api.html (including marker `<!--issue:NEW-AUDIT-27-->`), docs/c-api.html
  - CNA-GAP-001: deep-dives/reference/verification-tiers.html, development/internals/content/runtime.html, development/internals/modules/core.html, development/maintenance.html, docs/content-manager.html
  - CNA-GAP-029: development/internals/graphics/easygl.html
  - CNA-GAP-031: development/internals/modules/graphics-ext.html, docs/cnaext-extensions.html
  - CNA-GAP-052: development/internals/modules/gamer-services.html
  - CNA-VGAP-010: development/testing/architecture.html, docs/verification.html
  - CNA-VGAP-017 and CNA-VGAP-018: development/internals/modules/graphics-ext.html, development/testing/architecture.html, docs/cnaext-extensions.html
  - CNA-VGAP-042: docs/rendering-backends.html
  - CNA-VGAP-055: development/internals/bindings/java.html, development/internals/graphics/easygl.html, development/internals/runtime/shutdown.html
  - No hand-written reference found for CNA-BUG-175, BUG-266, GAP-017, GAP-025, GAP-027, GAP-030, GAP-051, PLAT-006, PLAT-007, VGAP-009 or VGAP-040.
- **Cross-references inside entries that point at retiring ids:**
  - CNA-GAP-062 cites CNA-BUG-062 in `actual` and `tests_current`. Its replacement text (Appendix MISC) drops the citation.
  - CNA-BUG-058's evidence cites BUG-062 (Appendix DOC replaces it).
  - CNA-VGAP-056 cites VGAP-017 (Appendix TEST).
  - CNA-VGAP-025 cites VGAP-010 and VGAP-042 (Appendix TEST).
  - CNA-VGAP-008's evidence calls the Android packaged-content half "the defect CNA-BUG-041"; that still holds, since BUG-041 stays narrowed.
  - CNA-VGAP-024 cites CNA-VGAP-050, which was already folded into GAP-013. That dangling reference predates this pin move.

## 4. Expressing each action in `patches-adversarial.json`

This is the format as implemented by `scripts/known_issues.py` `apply_adversarial`.

**Order of operations:** `entries` (set, then append) → `folded` → `retired` → `reclassified` (new ids allocated) → `added` (new ids allocated) → `{{issue:KEY}}` resolution. Two consequences:
- `entries` and `retired` can only name ids that exist before reclassification and addition: original ids, folded ids, and the pre-reclassification ids.
- `retired.classification` must be one of `PROVEN FIXED`, `OBSOLETE`, `NOT A BUG` or `INSUFFICIENT EVIDENCE`. The header comment also lists `DUPLICATE`, but it is not in `CLASSIFICATIONS` and would be rejected. There is no `fixed` status.

**Existing retire, copied from the file**, the template for the 40 retirements of original ids:
```json
"retired": {
 "CNA-BUG-084": {
  "classification": "NOT A BUG",
  "evidence": "XNA 4.0's fixed-step Tick applies forceElapsedTimeToZero to the measured elapsed time, but the flagged tick then finds num == 0 whole steps ... Deep Dive game-time-and-timestep.html#reset-elapsed-time corrected accordingly."
 }
}
```
New examples:
```json
"CNA-GAP-025": {"classification": "OBSOLETE", "evidence": "The DIRECT2D renderer was removed by 0f96ea703 (RRC-012); DIRECT2D=16 is in CNA_RENDERER_RETIRED_IDENTITIES at b0e97bb1 and modules/renderers/direct2d no longer exists."}
"CNA-GAP-001": {"classification": "PROVEN FIXED", "evidence": "2d85a276f (KF-13): ContentLoadException derives from System::Exception (ContentLoadException.hpp); ContentRuntimeContractTests pin the base."}
```
The earlier audit's wording for a retired renderer (dispositions.json, CNA-BUG-014) is "Concerns a retired renderer family: the identity is listed in CNA_RENDERER_RETIRED_IDENTITIES of cmake/RendererIdentities.cmake …"; reuse it.

**Existing edits, copied from the file.** `set` replaces whole field values; `append` concatenates after `set`.
```json
"entries": {
 "CNA-BUG-052": {"set": {"tests_present": true, "confidence": "strong"}},
 "CNA-BUG-220": {"set": {"sources": [{"path": "modules/c-api/src/CnaCApiRuntime.cpp", "note": "cna_game_destroy comment after the Shutdown call; CGame::Shutdown"}, "..."]}},
 "CNA-BUG-001": {"set": {"tests_present": true, "confidence": "reproduced", "expected": "<p>...</p>", "evidence": "<p>...</p>", "reproduction": "<p>...</p>"},
                 "append": {"evidence": "<p><em>Independent re-verification:</em> ...</p>"}}
}
```
Rules for the 81 edited, changed or narrowed entries:
- **Build each new value from the current final value.** Take the final value in `issues-source.json`, apply the substitutions from the appendix, and write the full result as `entries.<key>.set.<field>`. Where an `entries.<key>` record already exists (344 do), merge into it.
- **Watch fields with an existing `append`.** 112 entries have one, all on `evidence`, plus one on `actual`. The final value already contains the appended text, so a new `set` built from it would duplicate it. Either edit the `append` text itself, or set the base without the appended part. CORE notes that CNA-BUG-078's second evidence string sits in its `append`.
- **Watch fields that come from `patches.json`.** Example: CNA-BUG-002's `blast_radius`. A later adversarial `set` overrides them, so setting there is fine.
- **NARROWED:** add `"status": "narrowed"` to `set`. CNA-BUG-041 is already narrowed.
- **Reclassified entries:** CNA-GAP-064 → `entries["CNA-BUG-100"]`, CNA-GAP-065 → `entries["CNA-BUG-108"]`, CNA-BUG-250 → `entries["CNA-GAP-050"]`. The alternative is the `reclassified.<old>.set` block.
- **Added entries:** CNA-BUG-253 (NEW-AUDIT-03), CNA-BUG-264 (NEW-AUDIT-20), CNA-GAP-070 (NEW-AUDIT-14), CNA-GAP-071 (NEW-AUDIT-17, also `status: narrowed`), CNA-VGAP-056 (NEW-AUDIT-05) and CNA-VGAP-059 (NEW-AUDIT-19). Edit the fields directly inside the element of `"added"` whose `"id"` is the NEW-AUDIT key. The element has the full field set: actual, blast_radius, cand_ids, class, confidence, evidence, expected, id, origin, public_contract, regression_test, related, reproduction, severity, sources, status, subsystem, summary, tests_current, tests_present, title, workaround.
- **Folded duplicates:** set `summary` and `sources` on `entries["CNA-BUG-187"]`, `["CNA-VGAP-043"]`, `["CNA-VGAP-045"]` and `["CNA-VGAP-048"]`. The values are in Appendices BUILD and TEST.

**Retiring the seven added entries needs a script change.** The entries are NEW-AUDIT-07, 09, 10, 21, 23, 25 and 27, published as CNA-BUG-255, 257, 258, 265, 266, 268 and 270.
- **Why the current mechanisms fail:** `"retired"` cannot see them, and deleting them from `"added"` renumbers CNA-BUG-256…274, breaking stable public URLs.
- **Proposed minimal change:** a new top-level key, processed inside the `added` loop *after* the id is allocated. The number is consumed and never reused, and later ids do not move:
```json
"retired_added": {
  "NEW-AUDIT-07": {"classification": "PROVEN FIXED", "evidence": "731120eb9 (CCS-1) makes EasyGLRenderer::ClearColorAndStencil restore the stencil write mask (RestoreWriteMasksAfterClear); EasyGL_Clear_RestoresStencilWriteMask covers all four stencil clears; the OpenGL4 half went with 261cb5f7f."},
  "NEW-AUDIT-09": {"classification": "OBSOLETE", "evidence": "PORTABLEGL was removed by 0f96ea703 (RRC-012); PORTABLEGL=46 is retired."},
  "NEW-AUDIT-27": {"classification": "OBSOLETE", "evidence": "engine_layer.h and CnaCApiEngineLayer.cpp were removed by 5572f3ca1 (MOD-RETIRE-1)."}
}
```
```python
# in apply_adversarial, inside `for k, e in enumerate(adv.get("added") or []):` right after `new` is computed:
spec = (adv.get("retired_added") or {}).get(e["id"])
if spec:
    if spec["classification"] not in CLASSIFICATIONS - PUBLISHED: ...error...
    for cid in e.get("cand_ids") or []:
        for d in disp:
            if d["cand"] == cid:
                d.update(classification=spec["classification"], published_as=None,
                         evidence="Retired by the independent adversarial audit: " + spec["evidence"], adversarial_retired_entry=new)
    trail["retired"][new] = {"key": e["id"], **spec}
    continue        # id consumed, entry not published
```
Two of these entries carry restored candidates: NEW-AUDIT-07 has `cand_ids: ["WP05-i011"]`, and others may too. The loop above re-dispositions them. `issue_refs.py` then correctly reports the `NEW-AUDIT-25` and `NEW-AUDIT-27` markers as unresolvable until the pages are edited.

**Other script constants.** `TODAY` is already `2026-10-04` in the working tree. `TARGET` comes from `cnahead`, which is already T in the working tree.

## 5. Exact sources at T for the new text

Each appendix gives verbatim `old -> new` substitutions and replacement `sources`, `related`, `status` and `title` values. The batch verifiers confirmed that every quoted `old` substring occurs in `issues-source.json`; G1 verified uniqueness with a script.

## 6. New issues at T worth recording (with evidence)

| # | Proposed class / subsystem | Title | Evidence at T |
|---|---|---|---|
| NEW-1 | bug, Build & CI (sev. medium) | CnaTests sources call POSIX `setenv`/`unsetenv` unguarded on every target, and the CTest that guarded against this (`CNAEXT_NoPosixSetenv`) is gone | `modules/graphics/tests/Microsoft/Xna/Framework/Graphics/IndexedDrawDeferredTests.cpp:571-572`, `struct CpuBaseVertexSwitch { ::setenv("CNA_EASYGL_CPU_BASE_VERTEX","1",1); ... ::unsetenv(...) }`, outside any `#if`. Added by 1dc4ce06a (CBIND-139). The file is compiled into CnaTests by `file(GLOB_RECURSE CNA_TEST_SOURCES ...)` (cmake/UnitTests.cmake:39), and the tree has no setenv shim. 5572f3ca1 removed the `CNAEXT_NoPosixSetenv` registration. Repeating `scripts/check_no_posix_setenv.py`'s scan finds 12 lines in 5 files at O and 53 lines in 18 files at T. MSVC and MinGW have no `setenv` (CNA's own `docs/cnatests-mingw-setenv-proposal.md`), so a Windows CnaTests build should fail to compile. Inferred (strong); nothing was built. CNA-BUG-200 retires and this supersedes it. |
| NEW-2 | bug, Audio & media (sev. low) | `SoundEffect::Play(volume, pitch, pan)` clamps pitch, does not range-check volume, and returns false when disposed, where XNA 4.0 throws ArgumentOutOfRangeException / ObjectDisposedException | CNA `modules/audio/src/Xna/SoundEffect.cpp` at T, `SoundEffect::Play`: `if (isDisposed_) return false;`; comment "Pitch is clamped rather than validated"; only `pan` throws; no volume check. XNA 4.0 (`xna4-decomp/.../Microsoft.Xna.Framework.Audio/SoundEffect.cs` `Play(float,float,float)`) throws ObjectDisposedException when disposed and assigns `Volume`/`Pitch`/`Pan` through the SoundEffectInstance setters, which throw ArgumentOutOfRangeException outside [0,1] / [-1,1] / [-1,1]. Since KF-12 (49119a34c) CNA's `SoundEffectInstance` setters throw, so the two paths now disagree. `audio.h` `cna_sound_effect_play_with_settings` documents "pitch is clamped". Verified by reading. |
| NEW-3 | functional-gap, Networking | `SendDataOptions` cannot express XNA's combined flags (values 5–7); Chat and unknown values fall back to reliable delivery | `SendDataOptions.hpp` is a plain enum 0–4 with no bitwise operators. `NetPacketCodec.cpp` maps Chat and any unknown value to reliable (around lines 570–575). CNA records this itself as GS-AUDIT-016 in `audit/gamer-services/gamer-services-issues.md`. |
| NEW-4 | functional-gap, Networking & gamer services | Offline leaderboards drop Stream columns, and a column-only change is not saved offline | `ColumnsToJson` skips Stream values; `LeaderboardWriter.cpp` saves offline only when the rating changes. CNA's GS-AUDIT-006 and `docs/gamer-services-known-limitations.md` §22. |
| NEW-5 | functional-gap, Networking & gamer services | PlayerMatch/Ranked sessions refuse guests, which XNA allows | `docs/gamer-services-known-limitations.md` §16 ("Guests: partially implemented"). |
| NEW-6 | functional-gap (or fold into CNA-GAP-071) | On EasyGL a game thread that waits inside LoadContent/Update/Draw for a worker creating graphics resources deadlocks; XNA allows it | KF-1 00b9c9898 and KF-16 a033a9184 commit messages; `docs/opengl33-renderer.md` "Graphics resources on other threads". The G2 batch text folds this into the narrowed CNA-GAP-071. |

Optional or lower-confidence leads, not proposed as entries:
- OPENGLES2, WEBGL1 and the web still draw into framebuffer 0, so the Wayland one-frame size lag that KF-6 fixed elsewhere remains there (`docs/opengl33-renderer.md`).
- `RuntimePlatformTestSupport.hpp:14` declares `namespace CNA::Runtime::Testing`, which clashes with `class CNA::Runtime` in `CNA/Misc.hpp`. It is test-only and nothing includes `Misc.hpp`, so it could be one sentence in CNA-GAP-003.
- GS-AUDIT-012: signed-out gamer objects are kept for the whole process lifetime. CNA calls this accepted design.
- misc/FUTURE.md:30 ("15 of 17 PBR renderers") and misc/CNAEXT.md:165 probably still count OPENGL4 and PORTABLEGL. Not recounted.
- **The C ABI release gate.** At T, RELEASE_GATE.md reads "CNA C ABI 0.44.0 … Not ready … 656 public symbols are still unmapped" (468 at O). This is already covered by CNA-GAP-062, CNA-BUG-058 and CNA-BUG-056, all marked CHANGED.
- **The SDL2 retirement** is cleanly locked:
  - `CnaPlatformSelection_SDL2` asserts "CNA_PLATFORM=SDL2 is not a known platform".
  - The audio selection test refuses SDL2.
  - docs/platform-abstraction.md:38 says SDL2 was retired 2026-10-04.
  - The only remaining SDL2 mention in docs is `misc/cnaplatform.md`, a design note.
  - No new defect was found. Its effects on the index are the 4 SDL2 retirements (BUG-178, 194, 195, plus BUG-233/236 fixed by the same commit's doc edits) and the SDL2 text edits (BUG-140, 142, 177, VGAP-012, 059, BUG-041).

## 7. Work files (scratchpad, not part of any repo)

These are in `<scratch>/r9work/`:
- `scan.json`: per-entry source existence and change data.
- `rrhits.json`: retired-renderer hits per field.
- `deadtokens.json`: dead `{{src:}}`/`{{tree:}}` tokens.
- `actions.tsv`: the 128 actions.
- `res-*.md`: the full batch reports, which are also appended below.

---

# Appendices: full batch reports, with exact substitutions per entry



---

## Appendix G1: Graphics & renderers, part 1


I've classified all 34 Graphics & renderers entries in batch G1 against the new pin: 5 should be retired, 6 have changed facts, 7 need text edits and 16 are still valid. The handback call was refused, so the report is here as plain text. I wrote nothing outside the scratch folder (`r9work/g1subs.py` checks that every quoted "old" text occurs exactly once in issues-source.json, except the BUG-113 string, which occurs twice and is replaced at both; `r9work/g1show.py` prints an entry).

**Retiring or editing four of these needs a different route.** BUG-253 (NEW-AUDIT-03), BUG-255 (NEW-AUDIT-07), BUG-257 (NEW-AUDIT-09) and BUG-264 (NEW-AUDIT-20) were added by the earlier adversarial audit. In `apply_adversarial`, `entries` and `retired` run before `added`, so they cannot name these ids and would fail with "unknown entry". Edits have to go into the entry's own record in the `added` list. Retiring one means deleting that record, which renumbers every later NEW-AUDIT id. The alternative is a new script operation that retires by final id after allocation.

#### 1. Entries needing action

**Retire: subject removed (OBSOLETE)**

| id | key | evidence at T |
|---|---|---|
| CNA-BUG-097 RenderPipeline release keeps the Bloom/SSAO/fog pools | CNA-BUG-097 | 5572f3ca1 (MOD-RETIRE-1) deleted RenderPipeline, BloomPass, SsaoPass, VolumetricFogPass and DeviceLifecycleTests. `modules/graphics-ext` at T holds only the ASCII/CRT/Depth effects, DebugDraw and ShaderCode/PackageEXT. |
| CNA-BUG-098 throwing callback breaks RenderPipeline/ShadowMap | CNA-BUG-098 | 5572f3ca1 deleted RenderPipeline.cpp, ShadowMap.cpp and PipelineDiagnosticsTests.cpp. |
| CNA-BUG-109 engine-layer capability table lacks IndirectDraw | CNA-BUG-109 | 5572f3ca1 deleted `graphics-ext/src/RequireCapability.cpp`; `nameOfCapability` no longer exists. |
| CNA-BUG-257 PORTABLEGL depth clears never restore glDepthMask | NEW-AUDIT-09 | 0f96ea703 (RRC-012); PORTABLEGL=46 is in the retired identity list. Remove from `added`. |

Proposed retire record, same wording pattern for 098 and 109:
`"retired": {"CNA-BUG-097": {"classification": "OBSOLETE", "evidence": "The graphics engine layer (RenderPipeline, BloomPass, SsaoPass, VolumetricFogPass) was removed by 5572f3ca1 (MOD-RETIRE-1); none of the cited files exists at b0e97bb1."}}`

**Retire: fixed (PROVEN FIXED)**

- **CNA-BUG-255 (key NEW-AUDIT-07), EasyGL ClearColorAndStencil leaves the stencil write mask open.**
  - Commit 731120eb9 (CCS-1) makes `EasyGLRenderer::ClearColorAndStencil` call `RestoreWriteMasksAfterClear(false, true)`.
  - New test `EasyGL_Clear_RestoresStencilWriteMask` (`easygl_clear_restores_stencil_write_mask_test.cpp`) fails before the fix; after it, all four stencil-clear variants pass.
  - The entry's OpenGL4 half is gone with 261cb5f7f.
  - Remove from `added`. Evidence text: "731120eb9 (CCS-1) makes ClearColorAndStencil restore the stencil write mask; EasyGL_Clear_RestoresStencilWriteMask covers all four stencil clears."

**CHANGED: still exists, facts differ**

- **CNA-BUG-094, SDL_GPU claims compute and SPIR-V intake on Direct3D 12/Metal.**
  - Still true at T:
    - `SupportsComputeShadersEXT` returns `device_ != nullptr`.
    - `SupportsShaderLanguageEXT` accepts SpirV.
    - `CreateShaderFromRemappedSpirvEXT` passes `SDL_GPU_SHADERFORMAT_SPIRV`.
    - Shadercross still defaults ON for Windows and Apple.
  - What changed: the public `CNA::Graphics::ComputeShader` was removed by 5572f3ca1, and nothing outside the renderers creates compute shaders.
  - Edits:
    - public_contract: `GraphicsDevice::SupportsShaderLanguageEXT and CNA::Graphics::ComputeShader on SDL_GPU` → `GraphicsDevice::SupportsShaderLanguageEXT and ShaderEffect SPIR-V payloads on SDL_GPU`
    - actual: replace `there the capability is true and creation fails, so <code>CNA::Graphics::ComputeShader</code> throws <code>ShaderCompilationExceptionEXT</code> carrying SDL's error instead of the <code>NotSupportedException</code> a false capability would give, and a shader package` → `there both answers are true while a raw SPIR-V ShaderEffect cannot be created (SDL reports the failure instead of the NotSupportedException a false answer would lead to; no public CNA API creates compute pipelines since 5572f3ca1), and a shader package`
    - evidence: delete the sentence starting `Engine-layer consumers mostly survive the claim:` through `… Windows and Apple builds.`
    - blast_radius: `CNAEXT <code>ComputeShader</code>, storage-buffer compute work and shader packages that select a SPIR-V variant` → `ShaderEffect SPIR-V payloads, shader packages that select a SPIR-V variant, and callers that trust SupportsCapability(ComputeShaders)`
    - workaround: `on macOS, use another renderer for CNAEXT compute.` → `on macOS, use another renderer for SPIR-V ShaderEffects.`
    - sources: drop `modules/graphics-ext/src/ComputeShader.cpp`.
    - related: drop `docs/cnaext-engine.html#renderers`.

- **CNA-BUG-099, 24 classic SDL_GPU CTests still fail.**
  - Commit d111906f7 (STREETPERF-0002) added `plans/plan_street_perf.md`, which did not exist at O. It records:
    - 213 passing / 25 failing of 238 `^SdlGpu` tests, "the same 25 as the unmodified renderer", unnamed.
    - A cause for the two `SdlGpuIndexedDrawRangeTest` cases: they rewrite a still-bound buffer, which the device now refuses as XNA does.
  - All the named tests are still registered at T.
  - Edits:
    - title: `24 classic SDL_GPU CTests still fail in CNA's latest recorded run` → `Classic SDL_GPU CTests still fail in CNA's latest recorded runs (25 of 238)`
    - summary: "CNA's last named SDL_GPU record (STREETS-0008) lists 26 failing classic ^SdlGpu CTests and the later STREETPERF-0002 run 25 of 238, unnamed; two are separate entries, and of the other 24 the records give a cause for four, a guess for a fifth, and nothing for 19."
    - actual: after `… is 26 failures, "none new".` append "The later STREETPERF-0002 record ({{src:plans/plan_street_perf.md|plan_street_perf.md}}) reports 25 of 238 failing, the same 25 as the unmodified renderer, without naming them, and attributes the two SdlGpuIndexedDrawRangeTest cases to tests that rewrite a buffer still bound to a queued draw, which the device now refuses as XNA does."
    - actual, cause paragraph: "only three of the 24" → "four of the 24 (plus the guess)"; "The other 21" → "The other 19".
    - sources: add `{"path": "plans/plan_street_perf.md", "note": "STREETPERF-0002: 25 of 238 ^SdlGpu ctests failing; cause of the two SdlGpuIndexedDrawRangeTest cases"}`.

- **CNA-BUG-115, DIRECTX9 PresentInterval Two is unchecked and a failing Reset is retried.** The consequence is now worse.
  - `BuildPresentParameters` still maps 2 to `D3DPRESENT_INTERVAL_TWO` with no caps check.
  - A failed `EnsureDeviceSize` still leaves `presentationDirty_` set.
  - New since 6f6100cd3 (FULLSCREEN-001): `GraphicsDeviceManager::BeginDraw` calls `DirectX9Renderer::TryBeginDrawEXT`. That runs `EnsureDeviceSize()` and returns false while `presentationDirty_` is set, so `Game` skips both Draw and EndDraw/Present.
  - Edits:
    - actual, after `… with <code>PresentationParameters</code> still claiming Two.` append: "Since FULLSCREEN-001 the retry also runs from the draw gate: <code>GraphicsDeviceManager::BeginDraw</code> calls <code>DirectX9Renderer::TryBeginDrawEXT</code>, which runs <code>EnsureDeviceSize</code> and refuses the frame while <code>presentationDirty_</code> is set, so every Draw and Present is skipped while Update keeps running."
    - summary: "retries on every Present while still reporting Two" → "retries every frame from the draw gate, skipping Draw and Present, while still reporting Two".

- **CNA-BUG-118, GetMaxTextureDimension returns an unqueried 16384.**
  - At T only `VulkanRenderer` returns a real limit; FNA3D returns the default.
  - The Direct2D and GDI overrides are gone.
  - The public StorageTexture2D, Texture2DArray and the engine render-target size scope were removed by 5572f3ca1.
  - The C API texture-create route in `CnaCApiGraphics.cpp` checks sizes against this value.
  - Edits:
    - summary: `Only VULKAN, DIRECT2D and GDI report a real or bounded limit;` → `Only VULKAN reports a real limit;` (rest unchanged).
    - actual: `(VULKAN, DIRECT2D and GDI override)` → `(VULKAN overrides)`
    - actual: `VULKAN (<code>maxImageDimension2D</code>), DIRECT2D (<code>GetMaximumBitmapSize</code>) and GDI (a fixed software-framebuffer ceiling) override;` → `VULKAN (<code>maxImageDimension2D</code>) overrides;`
    - actual: `<code>EasyGL</code>, OPENGL4, <code>SDL_GPU</code>, WEBGPU` → `<code>EasyGL</code>, <code>SDL_GPU</code>, WEBGPU`
    - actual: the clause from `<code>StorageTexture2D</code> and <code>Texture2DArray</code> preparation` to `any application that reads the reported value.` → `the C API's texture creation and renderer information routes, and any application or binding that reads the reported value.`
    - evidence: `the exposure is EXT texture types, engine-layer allocations and callers` → `the exposure is the C API texture route and callers`
    - sources: drop the direct2d and gdi paths. Add `{"path": "modules/renderers/fna3d/src/Fna3dRenderer.cpp", "note": "GetMaxTextureDimension returns the default (no FNA3D query)"}` and `{"path": "modules/c-api/src/CnaCApiGraphics.cpp", "note": "texture creation checks width/height against GetMaxTextureDimension"}`.

- **CNA-GAP-008, SDL_GPU ShaderEffect draws bind only vertex stream 0.**
  - Unchanged at T:
    - `QueueCustomEffect3DDrawEXT` still sets `buffer_slot = 0`.
    - `IssueCustomEffect3DDrawEXT` still binds a single vertex buffer.
    - The limitation text is unchanged.
  - What changed: the public StorageBuffer and ParticleSystem left with 5572f3ca1. The storage-buffer instancing route can no longer be reached publicly, so the "instancing not implemented" sentence is now effectively accurate.
  - Edits:
    - title: "SDL_GPU ShaderEffect draws bind only the first vertex stream, while the limitation report claims all sixteen stream bindings".
    - summary: "SDL_GPU's custom-effect draw takes its attributes from the first vertex buffer and binds slot 0 only, so other streams (including per-instance streams) are never consumed, and its limitation text does not mention the restriction."
    - actual: replace the two sentences from `Instanced ShaderEffect draws do work …` to `… silent about the stream restriction.` with `The limitation text claims all sixteen XNA vertex-stream bindings and says nothing about this ShaderEffect restriction (its instancing sentence is accurate since the storage-buffer API left with the engine layer in 5572f3ca1).`
    - tests_current: delete the sentence `The storage-buffer instancing route is exercised through the particle system in <code>CnaGraphicsExtTests</code> (CNA records SDL_GPU at 931/0/31 of 962, SMG-0042).` together with the space after it.
    - blast_radius: `Stock-effect draws and storage-buffer instancing are unaffected;` → `Stock-effect draws are unaffected;`
    - workaround: `give a ShaderEffect its per-instance data through a storage buffer indexed by <code>gl_InstanceIndex</code>, or interleave` → `interleave`

- **CNA-GAP-009, sub-pixel SpriteBatch destinations reach only a few renderers.**
  - At T the float-destination `Draw` is overridden only by `EasyGLSpriteBatchRenderer` and `SoftwareSpriteBatchRenderer`; Canvas overrides only the integer overloads.
  - The sub-pixel contract test is registered only for EasyGL and Software.
  - Edits:
    - title: `reach only EasyGL, OPENGL4 and SOFTWARE` → `reach only EasyGL and SOFTWARE`
    - summary: `only the EasyGL, OPENGL4 and SOFTWARE sprite renderers override it.` → `only the EasyGL and SOFTWARE sprite renderers override it.`
    - actual: `Only <code>EasyGLRenderer</code>, <code>OpenGL4SpriteBatchRenderer</code> and the SOFTWARE sprite renderer override it; VULKAN, SDL_GPU, WEBGPU, the Direct3D renderers, DIRECT2D, GDI, SDL_RENDERER, the browser renderers, METAL, FNA3D and the rest` → `Only <code>EasyGLSpriteBatchRenderer</code> and the SOFTWARE sprite renderer override it; VULKAN, SDL_GPU, WEBGPU, the Direct3D renderers, SDL_RENDERER, CANVAS, METAL, FNA3D and the rest`
    - evidence: `(<code>EasyGL</code>, OPENGL4, SOFTWARE); GDI's sprite batch wraps the Software 2D core but forwards only the three integer overloads, so it inherits the truncating default too.` → `(<code>EasyGL</code>, SOFTWARE).`
    - evidence: `registered only for <code>EasyGL</code>, OPENGL4 (parity corpus) and SOFTWARE;` → `registered only for <code>EasyGL</code> and SOFTWARE;`
    - workaround: `or use one of the three renderers.` → `or use an EasyGL identity or SOFTWARE.`
    - sources: drop `modules/renderers/opengl4/src/OpenGL4SpriteBatch.cpp`. Add `{"path": "modules/renderers/easygl/src/EasyGLRenderer.cpp", "note": "EasyGLSpriteBatchRenderer::Draw float override"}` and `{"path": "modules/renderers/software/src/SoftwareSpriteBatch.cpp", "note": "SoftwareSpriteBatchRenderer::Draw float override"}`.

**EDIT: defect unchanged, text must change**

- **CNA-BUG-101, Reset rolls back only the window stage.** The renderer calls still run after the rollback block. The Direct2D example is gone, but `DirectX11Renderer::ApplyMultiSampleCount` → `RecreateDefaultRenderSurfaces` throws `std::runtime_error` when the native allocation fails.
  - actual: replace the parenthetical starting `(<code>Direct2D</code>'s <code>ApplyMultiSampleCount</code>, for example,` and ending `… through the renderer's applied-format hooks)` with `(<code>DirectX11Renderer::ApplyMultiSampleCount</code>, for example, recreates the default render surfaces and throws <code>std::runtime_error</code> when that native allocation fails)`.
- **CNA-BUG-107, DIRECTX9 draws a 3D ShaderEffect as BasicEffect.** The DX9 code is untouched; PostProcessPass was removed by 5572f3ca1.
  - actual: `because the query is renderer-wide and engine-layer passes such as <code>PostProcessPass</code> draw their <code>ShaderEffect</code> as 3D, where a true answer would over-promise.` → `because the query is renderer-wide and a caller may draw a <code>ShaderEffect</code> as 3D geometry, where a true answer would over-promise.`
  - blast_radius: `<p>Engine or game code that uses ShaderEffect` → `<p>Game code that uses ShaderEffect`
- **CNA-BUG-111, ShaderEffect::SetTexture forwards null for a disposed texture.** Code unchanged.
  - actual: `<code>EasyGL</code> and <code>OpenGL4</code> return early` → `<code>EasyGL</code> returns early`
- **CNA-BUG-113, a zero-area scissor is unclipped on VULKAN and SDL_GPU.** Code unchanged; the test fixture only lost its OPENGL4 row.
  - evidence (two occurrences): `(WEBGPU, EASYGL, OPENGL4, SOFTWARE, HEADLESS, DIRECTX9, DIRECTX11, DIRECTX12)` → `(WEBGPU, EASYGL, SOFTWARE, HEADLESS, DIRECTX9, DIRECTX11, DIRECTX12)`
- **CNA-BUG-253 (key NEW-AUDIT-03), SdlGpu_ConstructorExceptionSafety double free.** No fix commit; the test is still registered. Edit inside its `added` record.
  - actual: `The last record before TARGET (STREETS-0008) still counts it among the failing classic tests.` → `The last record that names the failing classic tests (STREETS-0008) still counts it among them; the later STREETPERF-0002 run reports 25 failures without names.`
  - "cluster of 24" in summary and tests_current stays correct.
- **CNA-BUG-264 (key NEW-AUDIT-20), Vulkan passes DepthBias unscaled.** Still `vkCmdSetDepthBias(cb, draw.depthBias, 0.0f, draw.slopeScaleDepthBias)` (VulkanRenderer.cpp line 15115). `docs/easygl_bugs.md` at T lists only directx11 and vulkan as unscaled. Edit inside its `added` record.
  - summary: `EasyGL, OpenGL4, SDL_GPU and Direct3D 11/12 scale` → `EasyGL, SDL_GPU and Direct3D 11/12 scale`
  - expected: `CNA's EasyGL, OpenGL4, SDL_GPU and Direct3D 11/12 renderers convert it as well` → `CNA's EasyGL, SDL_GPU and Direct3D 11/12 renderers convert it as well`
  - actual: replace the final OpenGL4Renderer::ApplyCurrentDepthBias sentence with `EasyGL's {{src:modules/renderers/easygl/include/CNA/Internal/Renderers/EasyGL/EasyGLRenderer.hpp|EasyGLDepthBiasToPolygonOffsetUnits}} carries the 16/24-bit scale Vulkan lacks.`
  - evidence: `against the Vulkan and OpenGL4 sources` → `against the Vulkan and EasyGL sources`; delete the sentence beginning `The same note lists PortableGL, …`
  - sources: replace the opengl4 entry with `{"path": "modules/renderers/easygl/include/CNA/Internal/Renderers/EasyGL/EasyGLRenderer.hpp", "note": "EasyGLDepthBiasToPolygonOffsetUnits: the depth-format scale Vulkan lacks"}`. Change the `docs/easygl_bugs.md` note to "CNA's own record (2026-09-08): Vulkan and DirectX 11 still carry the unscaled premise".
- **CNA-GAP-010, Immediate sort mode batches below the seam on several renderers.** Still unhonoured on Vulkan, SDL_GPU, Direct3D and WebGPU; the immediate-submission contract test is registered for EasyGL and Software only.
  - summary: `while EasyGL, OPENGL4, FNA3D and SOFTWARE submit per Draw.` → `while EasyGL, FNA3D and SOFTWARE submit per Draw.`
  - actual: `EasyGL, <code>OPENGL4</code> and <code>FNA3D</code> flush the sprite before <code>Draw</code> returns while immediate mode is set (EasyGL and OpenGL 4 end their sprite <code>Draw</code> with` → `EasyGL and <code>FNA3D</code> flush the sprite before <code>Draw</code> returns while immediate mode is set (EasyGL ends its sprite <code>Draw</code> with`
  - evidence: `which made EasyGL, OpenGL 4 and FNA3D honour immediate submission;` → `which made EasyGL honour immediate submission (FNA3D already did);`
  - evidence: `<code>EasyGL</code> honour immediate submission; OPENGL4 gained the same flush in its 2026-09-24 rebuild and FNA3D had it from its introduction.` → `<code>EasyGL</code> honour immediate submission; FNA3D had it from its introduction.`
  - evidence: `is registered for <code>EasyGL</code>, OPENGL4 and SOFTWARE only.` → `is registered for <code>EasyGL</code> and SOFTWARE only.`
  - sources: drop `modules/renderers/opengl4/src/OpenGL4SpriteBatch.cpp`.

#### 2. Still valid (what I checked at T)

- **CNA-BUG-006:** SpriteEffect still looks up the "MatrixTransform" parameter. The only Effect.cpp change is `BindStockTextureInternal`.
- **CNA-BUG-029:** the GraphicsResource copy constructor still never calls `AddResourceReference`; KF-1 only added a mutex. Texture2D and TextureCube copies are still defaulted.
- **CNA-BUG-054:** headless occlusion query still reports `PixelCount()` as 1.
- **CNA-BUG-093:** all cited sources unchanged.
- **CNA-BUG-095:** a failed GraphicsDevice constructor still rethrows without unlatching. The latch still happens at the end of `resolveRenderer`; BINDFIX-038 only changed the environment-variable handling.
- **CNA-BUG-096:** the Vulkan constructor region has no changes.
- **CNA-BUG-102:** DX9 recovery and string-marker calls are still "not yet implemented", and GraphicsDevice still sets its flag first.
- **CNA-BUG-103:** the Vulkan MRT render pass still clears every attachment, unchanged since O.
- **CNA-BUG-104:** DX9 still writes MaxAnisotropy without clamping and has no capability override.
- **CNA-BUG-105:** SDL_Renderer code unchanged; scissor rectangles are still forwarded regardless of the enable flag.
- **CNA-BUG-106:** ShaderEffect, PbrEffect, SkinnedPbrEffect and ColorMatrixEffect clones still skip the disposed check.
- **CNA-BUG-110:** stock-effect parameters are still read at draw time. CBIND-156 (6c278b21d) only changed how stock-effect textures are sampled after Apply.
- **CNA-BUG-112:** Vulkan still tags only 3D draws with the active occlusion query.
- **CNA-BUG-114:** WebGPU still always creates a Depth24PlusStencil8 attachment with no applied-format override.
- **CNA-BUG-116:** the DX9 MRT branch is untouched.
- **CNA-BUG-117:** the SDL_Renderer constructor still maps any positive interval to 1.

#### 3. Outside this batch

- FULLSCREEN-001 (6f6100cd3) added window-to-logical transforms for DIRECTX9, and letterboxing plus input transforms for Canvas. This likely changes CNA-BUG-133 and CNA-BUG-134, which are in the MISC batch.

#### 4. Counts

| Disposition | Count | Entries |
|---|---|---|
| Retire, subject removed | 4 | BUG-097, BUG-098, BUG-109, BUG-257 |
| Retire, fixed | 1 | BUG-255 |
| Narrowed | 0 | |
| Changed | 6 | BUG-094, BUG-099, BUG-115, BUG-118, GAP-008, GAP-009 |
| Edit | 7 | BUG-101, BUG-107, BUG-111, BUG-113, BUG-253, BUG-264, GAP-010 |
| Still valid | 16 | listed in section 2 |
| **Total** | **34** | |


---

## Appendix G2: Graphics & renderers, part 2


Batch G2 (34 graphics entries, CNA-GAP-011..033, GAP-064/065/071, PLAT-001..007, VGAP-003): disposition of each at T=b0e97bb1, with evidence and the text changes needed.

#### R9 batch G2: known-issue dispositions at T=b0e97bb1

**Summary:** 34 entries.
- **RETIRE: 8**
  - 7 are obsolete because their subject was removed (GAP-025, 027, 029, 030, 031, PLAT-006, 007).
  - 1 is proven fixed (GAP-017).
- **NARROWED: 4** (GAP-014, 032, 071, PLAT-003).
- **EDIT: 8** (GAP-012, 021, 023, 028, 033, 064, 065, PLAT-001).
- **STILL VALID: 14.**

**How each entry is patched in `patches-adversarial.json`:**
- **GAP-064:** edits use `"CNA-BUG-100"` under `entries`. That phase runs before reclassification.
- **GAP-065:** edits use `"CNA-BUG-108"`.
- **GAP-071:** its key is NEW-AUDIT-17. Edit that object in `added[]` directly (set `status: "narrowed"` and the replacement fields there).
- **Every other entry:** patch it under its own id.

**What fails the checks today:**
- `check_retired_renderers` flags any spelling of a removed renderer. That includes source paths and `related` links. Every EDIT below removes those mentions.
- `validate` rejects any source path that does not exist at T. Each dead path below has a replacement or removal.

#### 1. Entries needing action

| published id | stable key | short title | disposition | evidence at T | proposed change |
|---|---|---|---|---|---|
| CNA-GAP-025 | CNA-GAP-025 | DIRECT2D refuses additive blending | RETIRE `OBSOLETE` | 0f96ea703 (RRC-012) removed `modules/renderers/direct2d`. DIRECT2D=16 is in `CNA_RENDERER_RETIRED_IDENTITIES`. | `retired` |
| CNA-GAP-027 | CNA-GAP-027 | HTML_DOM/SVG_DOM refuse back-buffer readback | RETIRE `OBSOLETE` | 261cb5f7f (RRC-015) removed html-dom and svg-dom. | `retired` |
| CNA-GAP-030 | CNA-GAP-030 | FREEDIRECT keeps the old physical scale after a virtual-resolution change | RETIRE `OBSOLETE` | 0f96ea703 removed freedirect and `docs/freedirect-renderer.md`. | `retired` |
| CNA-GAP-031 | CNA-GAP-031 | ClusteredForwardEffect binds no material textures | RETIRE `OBSOLETE` | 5572f3ca1 (MOD-RETIRE-1). `git grep ClusteredForwardEffect T -- modules` finds nothing; `docs/graphics-ext-scope-reduction.md` §B lists clustered lighting as removed. | `retired` |
| CNA-GAP-029 | CNA-GAP-029 | EasyGL GPU timers read 32-bit results, no disjoint detection | RETIRE `OBSOLETE` | 5572f3ca1 removed the public contract the entry names (`CNA::Graphics::GpuTimer` and RenderPipeline pass timings) and `modules/graphics-ext/src/GpuTimer.cpp`. The internal `EasyGLGpuTimerRenderer` still reads 32-bit results, but only the internal `IGraphicsRenderer::CreateGpuTimerEXT` reaches it; the only public trace left is the `RendererFeature::GpuTimers` flag. | `retired` (keeping it as an internal-only entry is an alternative) |
| CNA-PLAT-006 | CNA-PLAT-006 | Direct2D under Wine/Proton lacks ColorMatrix | RETIRE `OBSOLETE` | 0f96ea703. | `retired` |
| CNA-PLAT-007 | CNA-PLAT-007 | HTML_DOM/SVG_DOM additive blending without plus-lighter | RETIRE `OBSOLETE` | 261cb5f7f. | `retired` |
| CNA-GAP-017 | CNA-GAP-017 | PresentationMode not honoured by FREEDIRECT, CANVAS and DIRECTX9 | RETIRE `PROVEN FIXED` | **CANVAS:** 6f6100cd3 (FULLSCREEN-001). `CanvasRenderer::getLogicalSize` and `getPresentedRect` now read `presentationMode_` and the virtual size for all modes. Tests: `CanvasPresentation.LetterboxUsesPhysicalBoundsAndInputOffset` and `StretchAndHiDpiInputUseIndependentAxisScales` (CanvasRendererTests.cpp), plus `cna_test_canvas_spritebatch_presentation`. **DIRECTX9:** 9bbba48d8 (FULLSCREEN-002). `DirectX9Renderer::GetLogicalSizeEXT`, `GetPresentedRectEXT` and `RestorePresentationViewportEXT` read `presentationMode_`, `virtualWidth_` and `virtualHeight_`. New CTests `DirectX9_SpriteBatchPresentation` and `DirectX9_ResizeStateAndMotion`. **FREEDIRECT:** removed by 0f96ea703. | `retired`. Evidence text should name all three. |
| CNA-GAP-014 | CNA-GAP-014 | CANVAS/FREEDIRECT ignore Viewport+Scissor; SDL_RENDERER ignores Viewport | NARROWED | FREEDIRECT removed by 0f96ea703. CANVAS gained a `SetViewport` override in 6f6100cd3: `state_->viewport` offsets, scales and clips sprite batches, and `GraphicsDevice::setViewportProperty` maps the viewport and forwards it. CANVAS still has no `SetScissorRect`. SdlRenderer.hpp is unchanged: it overrides `SetScissorRect` only and has no `GetApplied*FormatEXT`. | Set `status: "narrowed"`. **title:** "CANVAS ignores GraphicsDevice.ScissorRectangle, and SDL_RENDERER ignores Viewport". **summary:** "CANVAS leaves the no-op IGraphicsRenderer::SetScissorRect in place and SDL_RENDERER the no-op SetViewport, so a scissor rectangle never clips on CANVAS and a custom viewport never offsets drawing on SDL_RENDERER." **public_contract:** "GraphicsDevice.ScissorRectangle (with RasterizerState.ScissorTestEnable) on CANVAS; GraphicsDevice.Viewport on SDL_RENDERER". **actual**, replace `'CANVAS ({{src:modules/renderers/canvas/src/CanvasRenderer.cpp\|CanvasRenderer.cpp}}) and FREEDIRECT ({{src:modules/renderers/freedirect/src/FreeDirectRenderer.cpp\|FreeDirectRenderer.cpp}}) override neither, and SDL_RENDERER'` → `'CANVAS ({{src:modules/renderers/canvas/src/CanvasRenderer.cpp\|CanvasRenderer.cpp}}) overrides SetViewport (its sprite batches are offset, scaled and clipped to the viewport since FULLSCREEN-001) but not <code>SetScissorRect</code>, and SDL_RENDERER'`. **sources:** drop the freedirect path. Change the CanvasRenderer.cpp note to "SetViewport override; no SetScissorRect override". **tests_current:** "No scissor pixel fixture is registered for CANVAS, and none checks a custom viewport on SDL_RENDERER." **blast_radius:** "Clipped scroll panels on CANVAS; split-screen and offset viewports on SDL_RENDERER." **evidence**, append: "Re-read at b0e97bb1: FREEDIRECT retired (0f96ea703); CANVAS honours the viewport since 6f6100cd3." |
| CNA-GAP-032 | CNA-GAP-032 | Engine-layer PBR limits (1 light, 8-bit cubes, no back-face flip, no alpha-tested casters) | NARROWED | **Removed (5572f3ca1):** EnvironmentProcessor and the shadow_caster shaders. **Partly fixed (a1414a1b0, GSC-0010):** the back-face flip now exists on EasyGL only. `GpuDrawParams::pbrDoubleSided` and `uDoubleSided` flip N, T and B; test `easygl_pbr_double_sided_test`. `pbrDoubleSided` is read only in easygl. VULKAN, SDL_GPU, WEBGPU, DX9/11/12 and METAL all bind PBR maps but ignore it. **Unchanged:** PbrEffect.hpp still holds one `PunctualLightEXT`. | Set `status: "narrowed"`. **title:** "PbrEffect limits: one punctual light per draw, and no back-face normal flip for double-sided materials outside EasyGL". **summary:** "PbrEffect takes one punctual light, and only EasyGL's PBR programs reverse the normal of a double-sided material's back face (GSC-0010); every other PBR renderer lights the back face with the front normal." **public_contract:** "PbrEffect::setPunctualLightEXT; PbrEffect/SkinnedPbrEffect doubleSided on renderers other than EasyGL". **expected:** "&lt;p&gt;glTF 2.0 reverses the normal of a back face of a double-sided material before lighting.&lt;/p&gt;". **actual:** "{{src:…PbrEffect.hpp\|PbrEffect.hpp}} holds a single <code>PunctualLightEXT</code> ('Supplies one punctual light and its shadow'). The doubleSided mapping in {{src:docs/gltf-limitations.md\|gltf-limitations.md}} selects <code>CullNone</code>; PbrEffect and SkinnedPbrEffect pass it as <code>GpuDrawParams::pbrDoubleSided</code>, which only EasyGL reads (it flips N, T and B on the back face); VULKAN, SDL_GPU, WEBGPU, DIRECTX9/11/12 and METAL ignore it, so their back faces are lit with the front normal." **sources:** drop `docs/cnaext-engine-layer.md`, `EnvironmentProcessor.cpp` and `shadow_caster/directional.desktop.frag.glsl`. Add `modules/graphics/include/CNA/Internal/Renderers/Common/IGraphicsRenderer.hpp` (note: "GpuDrawParams::pbrDoubleSided") and `modules/renderers/easygl/examples/easygl_pbr_double_sided_test.cpp` (note: "EasyGL only"). **tests_current:** "easygl_pbr_double_sided_test lights a double-sided back face on EasyGL; no other renderer has one, and no test draws two punctual lights." **regression_test:** "A back-face lighting pixel test per PBR renderer; a two-punctual-light draw once lifted." **blast_radius:** "glTF scenes with double-sided foliage or cloth on non-EasyGL renderers, or several punctual lights per object." **related:** drop `docs/cnaext-engine.html#limits`. |
| CNA-GAP-071 | NEW-AUDIT-17 | GraphicsDevice single-threaded: registry unlocked, only EasyGL/OpenGL4 lease | NARROWED | **Registry locked:** 00b9c9898 (KF-1/KF-1a) added `resourcesMutex_` in Add-, Remove- and TransferResourceReference (GraphicsDevice.hpp names KF-1a). It also added `GraphicsResource::LeaseRendererContext`, taken in the ctor, SetData, GetData and Dispose of Texture2D/3D, TextureCube, the RTs, and VertexBuffer/IndexBuffer. **Whole-frame lease:** a033a9184 (KF-16): `Game::AcquireGameThreadContextLease`. **Device lifecycle serialized:** 5b4edd6cc (BINDFIX-050) added `NativeDeviceLifecycleMutex`. **Test:** `easygl_worker_thread_resources_test.cpp`. **Unchanged:** only `EasyGLRenderer` implements `AcquireThreadContextLeaseEXT`; OpenGL4 is gone (261cb5f7f); the Vulkan lease test header still says "no synchronization at all". | Edit the `added[]` object. Set `status: "narrowed"`. **title:** "Only EasyGL leases its context to other threads: on every other renderer, graphics resources created on a loading thread have no CNA-level exclusion against the frame". **summary** (235 chars): "GraphicsDevice's resource registry is now locked and EasyGL leases its context to resource creation on any thread, but every other renderer returns no lease and has no synchronization of its own, while XNA 4.0 creates its device D3DCREATE_MULTITHREADED." **actual:** state the registry lock (KF-1a), the EasyGL lease on resource construction, data transfer and Dispose (KF-1), and the whole-frame lease (KF-16). Then: "only EasyGLRenderer implements AcquireThreadContextLeaseEXT; VULKAN, the Direct3D renderers, SDL_GPU, WEBGPU, SDL_RENDERER and SOFTWARE return no lease", plus the Vulkan quote. Also: "RendererThreadContextLease.hpp still claims lease-less renderers 'support concurrent resource creation directly or own a different synchronization boundary'". Also: on EasyGL, a game thread that waits inside LoadContent, Update or Draw for a resource-creating worker deadlocks (docs/opengl33-renderer.md; XNA allows it). **sources:** replace the opengl4 path with `modules/graphics/include/CNA/Internal/Renderers/Common/RendererThreadContextLease.hpp` (lease contract) and `modules/renderers/easygl/examples/easygl_worker_thread_resources_test.cpp`. Optionally add `modules/runtime/src/Game.cpp` (AcquireGameThreadContextLease). Update the GraphicsDevice.cpp and GraphicsResource.cpp notes (resourcesMutex_; LeaseRendererContext). **tests_current:** "easygl_worker_thread_resources creates textures, vertex buffers and render targets on two workers while the game runs frames (EasyGL only); the Vulkan lease test asserts a null lease; nothing creates resources off the game thread on other renderers." **regression_test:** "Create and dispose resources on a worker while the game draws on each non-EasyGL renderer under ThreadSanitizer, or document that this is supported only on EasyGL." **blast_radius:** "Games that create resources or load content on a loading thread on renderers other than EasyGL." **workaround:** "&lt;p&gt;On renderers other than the EasyGL family, create graphics resources on the game thread or marshal loads to it.&lt;/p&gt;" |
| CNA-PLAT-003 | CNA-PLAT-003 | EasyGL GLES/WebGL without polygon mode refuses wireframe triangles | NARROWED | 251bf6c98 and 96b5038de (SAMPLE-048) added `CanDrawStockWireframeAsLineLoops`: single-stream stock non-indexed PositionColor TriangleList, clipped in homogeneous space, with no cull, depth, stencil, scissor, bias, MSAA or RT. cefe6c83b (SAMPLE-055) added `CanDrawStockIndexedWireframeAsLineLoops`: indexed 24-byte PositionNormal with the stock lit program, face culling and depth test. Tests: `EasyGLUnsupportedWireFrameTest.*` in EasyGLWireFrameContractTests.cpp. `RequireSupportedFillModeEXT` still throws for everything else, and the capability stays false. | Set `status: "narrowed"`. **title:** "EasyGL on GLES/WebGL contexts without GL_NV_polygon_mode or WEBGL_polygon_mode refuses most wireframe triangle draws". **summary** (≤253 chars): "Without a polygon-mode extension EasyGL draws only two bounded stock routes as line loops (non-indexed PositionColor and indexed PositionNormal TriangleLists); every other FillMode::WireFrame triangle draw throws NotSupportedException." **actual:** describe the two routes and their conditions (see the evidence column), then: "TriangleStrip, other layouts, custom or compiled effects, render targets, MSAA, scissor, stencil and bias still throw; GraphicsCapability::WireFrame remains false". **tests_current:** "EasyGLUnsupportedWireFrameTest covers both line-loop routes and the refusals (multi-stream, instanced, SpriteBatch, cull/bias/clipping/MSAA/two-sided stencil)". **evidence**, append the three commits. |
| CNA-PLAT-001 | CNA-PLAT-001 | CANVAS/FREEDIRECT/SDL_RENDERER/HTML_DOM/SVG_DOM throw for mip level > 0 | EDIT | Defect unchanged on the two surviving renderers: CanvasTextureRenderer.cpp `UpdatePixelsLevel` and SdlRenderer.cpp `SdlTextureRenderer::UpdatePixelsLevel` still throw std::runtime_error. CTest `SDL_Renderer_Texture2D_MipLevelThrows` (sdlrenderer_texture2d_miplevel_throws_test.cpp) pins it. The other three renderers were removed (0f96ea703, 261cb5f7f). | **title:** "CANVAS and SDL_RENDERER throw for any Texture2D mip level above 0, so mipmapped textures (including XNB textures with mip chains) cannot be uploaded there". **summary** (228 chars): "The texture renderers of CANVAS and SDL_RENDERER throw std::runtime_error from UpdatePixelsLevel for level > 0 because Canvas 2D and SDL_Renderer textures have no mip chain; the XNB Texture2D reader uploads every level it reads." **public_contract:** "… on CANVAS and SDL_RENDERER". **actual**, replace `'({{src:modules/renderers/canvas/src/CanvasTextureRenderer.cpp\|CanvasTextureRenderer.cpp}}), the <code>FreeDirect</code> texture and render-target renderers (<code>ThrowMipLevelUnsupported</code> in {{src:modules/renderers/freedirect/src/FreeDirectRenderer.cpp\|FreeDirectRenderer.cpp}}), <code>SdlTextureRenderer::UpdatePixelsLevel</code> ({{src:modules/renderers/sdl-renderer/src/SdlRenderer.cpp\|SdlRenderer.cpp}}), <code>HtmlDomTextureRenderer::UpdatePixelsLevel</code> and <code>SvgDomTextureRenderer::UpdatePixelsLevel</code> throw'` → `'({{src:modules/renderers/canvas/src/CanvasTextureRenderer.cpp\|CanvasTextureRenderer.cpp}}) and <code>SdlTextureRenderer::UpdatePixelsLevel</code> ({{src:modules/renderers/sdl-renderer/src/SdlRenderer.cpp\|SdlRenderer.cpp}}) throw'`. **sources:** replace the freedirect path with `modules/renderers/sdl-renderer/src/SdlRenderer.cpp` (note: "SdlTextureRenderer::UpdatePixelsLevel"). **evidence**, replace `'Check C of {{src:modules/renderers/freedirect/examples/freedirect_texture_rendertarget_test.cpp\|freedirect_texture_rendertarget_test.cpp}} pins the <code>FreeDirect</code> throw'` → `'SDL_Renderer_Texture2D_MipLevelThrows ({{src:modules/renderers/sdl-renderer/examples/sdlrenderer_texture2d_miplevel_throws_test.cpp\|sdlrenderer_texture2d_miplevel_throws_test.cpp}}) pins the SDL_RENDERER throw'`. **tests_current:** "No CANVAS or SDL_RENDERER test loads a mipmapped texture." **blast_radius:** "… that target CANVAS or SDL_RENDERER". |
| CNA-GAP-012 | CNA-GAP-012 | HEADLESS TextureCube::SetData throws | EDIT | Defect unchanged: HeadlessRenderer.hpp still says "Always false", and the TextureCube.cpp diff only adds the lease. The test gate is now `CubeStorageSupported(){ return !CNA_RENDERER_IS(SdlRenderer, Canvas, Headless); }`. | **evidence:** `'(its gate lists <code>SDL_RENDERER</code>, CANVAS, <code>HTML_DOM</code>, FREEDIRECT, HEADLESS, GDI and PORTABLEGL)'` → `'(its gate, <code>CubeStorageSupported</code>, lists <code>SDL_RENDERER</code>, CANVAS and HEADLESS)'` |
| CNA-GAP-021 | CNA-GAP-021 | DIRECTX9 BasicEffect reaches 12 of 32 variants | EDIT | D3D9EffectDraw.cpp is unchanged. `d3d-windows-ci.yml` matrix at T is `[DIRECTX11, DIRECTX12]`. | **evidence:** `'the Windows <code>D3D</code> CI matrix builds DIRECTX11, DIRECTX12 and DIRECT2D only'` → `'the Windows <code>D3D</code> CI matrix builds DIRECTX11 and DIRECTX12 only'` |
| CNA-GAP-023 | CNA-GAP-023 | DIRECTX9 Texture2D Color-only | EDIT | DX9 still has no `ClassifySurfaceFormatEXT` override. Overriders at T: DX11, DX12, EasyGL, SDL_GPU, Software, Vulkan, WebGPU. | **actual:** `'<code>EasyGL</code>, OPENGL4, <code>SDL_GPU</code>'` → `'<code>EasyGL</code>, <code>SDL_GPU</code>'` |
| CNA-GAP-028 | CNA-GAP-028 | METAL specular factor-only | EDIT | The test still has `factorOnly{{"metal"}}`. RRC-017 3b9982646 dropped OpenGL4 from gltf-limitations.md. | **actual:** `'names EasyGL, OpenGL4, DirectX9/11/12'` → `'names EasyGL, DirectX9/11/12'` |
| CNA-GAP-033 | CNA-GAP-033 | No MissingVertexShaderInput check | EDIT | No `MissingVertexShaderInput` anywhere in modules. WebGPU `SelectStockVertexShapeEXT` and Vulkan `BuildDualTextureVertexLayoutEXT` are unchanged. OpenGL4 was removed by 261cb5f7f. | **summary:** `'so EasyGL/OPENGL4 feed neutral values'` → `'so EasyGL feeds neutral values'`. **actual:** `'EasyGL and OPENGL4 leave a missing attribute disabled'` → `'EasyGL leaves a missing attribute disabled'`. **sources:** remove `modules/renderers/opengl4/src/OpenGL4StockDraw.cpp`. |
| CNA-GAP-064 | CNA-BUG-100 | WEBGPU OnDeviceLost only logs | EDIT | `OnDeviceLost` (WebGPURenderer.cpp:371) still only writes to std::cerr. `deviceLost_` is set only in `DebugSimulateContextLoss`. | Patch via key CNA-BUG-100. **expected:** `'<code>DirectX</code> 9, 11 and 12, <code>Direct2D</code> and Vulkan raise it'` → `'<code>DirectX</code> 9, 11 and 12 and Vulkan raise it'`. **blast_radius:** `'DirectX 9, 11 and 12, Direct2D and Vulkan raise'` → `'DirectX 9, 11 and 12 and Vulkan raise'`. |
| CNA-GAP-065 | CNA-BUG-108 | No capability feature for SPIR-V payloads | EDIT (optional: mentions the retired engine layer in passing) | Dialect mapping in GraphicsDevice.cpp:3608 is unchanged. SdlGpuRenderer.hpp:2993 still gives "the engine layer's GLSL ES 3.00" as the reason, which is stale. | Patch via key CNA-BUG-108. **actual:** `"because that route compiles Vulkan-rule GLSL where the engine layer's GLSL ES is not a legal input"` → `"because that route compiles Vulkan-rule GLSL, where GLSL ES 3.00 is not a legal input (the header still names the retired engine layer's shaders as the reason)"` |

**Note on evidence wording:** every kept entry says "Checked by reading at 009d40f5". A global `verified_against` and wording update belongs to the parent pass.

#### 2. STILL VALID (14)

- **CNA-GAP-011:** the only `getRenderTargetUsageProperty` read is still the bound target's (GraphicsDevice.cpp:5573).
- **CNA-GAP-013:** the metal tree changed only in an examples CMake glob. The CI still uses macos-14 and `-R '^Metal'`.
- **CNA-GAP-015:** the CBIND-156 diffs only add `BindStockTextureInternal`; there are still no Texture or DirLight parameters.
- **CNA-GAP-016:** `RegisterForWindow` and `UnregisterForWindow` are unchanged: no lock, no owner check, and the TextInputEXT slot handling is the same.
  - Optional note: device construction and teardown are now serialized by BINDFIX-050's `NativeDeviceLifecycleMutex`. `GetForWindow` readers are still unsynchronised.
- **CNA-GAP-018:** `EasyGLTexture3DRenderer` still derives only from `ITexture3DRenderer` (EasyGLRenderer.hpp:514).
- **CNA-GAP-019:** the Vulkan "reject additional spans" comment and logic are unchanged (VulkanRenderer.cpp:14887-14894).
- **CNA-GAP-020:** SDL_GPU still declares SpirV and the libshaderc route. `CnjEffectTests` is still `#version 300 es`.
- **CNA-GAP-022:** DX9 `CreateRenderTarget2D(... bool /*mipMap*/ ...)`. The cube target still ignores `mipMap` and `multiSampleCount`.
- **CNA-GAP-024:** no `SetFullscreenState` in modules. `exclusiveFullscreen_` is still only read.
- **CNA-GAP-026:** sources unchanged. The doc still marks Wrap/Mirror BLOCKED.
- **CNA-PLAT-002:** the REMED-GFX-086 comment is still there (SdlGpuRenderer.cpp:4673), as is the CMake "MultiSampleMask is NOT compiled in" comment.
- **CNA-PLAT-004:** no change to `ResolvePreciseTarget` or `PixelCountIsPreciseEXT` in the EasyGL diff.
- **CNA-PLAT-005:** `CreateOcclusionQuery` still throws with the same message (SdlGpuRenderer.cpp:4642).
- **CNA-VGAP-003:** EffectParameter sources and tests are unchanged O..T.

#### 3. New issues and cross-checks noticed

- **Possible new functional gap (or fold it into GAP-071's narrowed text as proposed):** on every GL profile, a game thread that waits inside LoadContent, Update or Draw for a worker creating graphics resources deadlocks, while XNA allows it. This is a consequence of KF-1/KF-16 and is stated in `docs/opengl33-renderer.md` §"Graphics resources on other threads".
- **Possible platform limitation:** on the ES 2.0 profiles (OPENGLES2, WEBGL1) and the web, the back buffer is still the window surface. So the Wayland surface lag that KF-6 fixed elsewhere remains there (same doc section).
- **Doc drift in CNA (low, optional):** SdlGpuRenderer.hpp lines 212, 2993, 3128 and 4247 still describe engine-layer passes and clustered lighting that 5572f3ca1 removed.
- **Cross-references to retiring entries:**
  - CNA-GAP-030 cites GAP-017; both retire.
  - Hand-written pages cite retiring or narrowed entries:
    - `development/internals/graphics/easygl.html` (GAP-029)
    - `development/internals/modules/graphics-ext.html` (GAP-031)
    - `docs/cnaext-engine.html` (GAP-031, GAP-032)
    - `development/takeover/threading.html` (GAP-071, now narrowed)
  - GAP-033 cross-references (`docs/effects.html`, `graphics-state.html`, `stock-effects-semantics.html`) stay valid.

#### 4. Counts

| disposition | count |
|---|---|
| RETIRE-OBSOLETE | 7 (GAP-025, 027, 029, 030, 031, PLAT-006, PLAT-007) |
| RETIRE-FIXED | 1 (GAP-017) |
| NARROWED | 4 (GAP-014, 032, 071, PLAT-003) |
| EDIT | 8 (GAP-012, 021, 023, 028, 033, 064, 065, PLAT-001) |
| STILL VALID | 14 |
| **Total** | **34** |

I wrote only scratch helpers (`r9work/g2_show.py`); no repository was modified.


---

## Appendix CORE: Math & geometry + Core & runtime


Task: batch-CORE, 48 Math & geometry and Core & runtime entries; disposition of each at T=b0e97bb1 against O=009d40f5.

Math needs almost nothing. Between O and T the math module changed only in `Matrix.hpp` (a Doxygen fix for `ToColumnMajor`), `CurveKeyCollection.hpp` (where the `CNAEXT` marker sits, BL-18) and one new `ToColumnMajor` test in `MatrixTests.cpp`. No math source file changed. Every inline `{{src:}}` and `{{tree:}}` token in the batch still resolves at T. No `related` link points at a missing page.

#### 1. Entries needing action

| published id | stable key | short title | disposition | evidence | proposed change |
|---|---|---|---|---|---|
| CNA-BUG-077 | CNA-BUG-077 | Invalid CNA_GRAPHICS_RENDERER terminates the process during static init | RETIRE-FIXED (PROVEN FIXED) | f1593227d (BINDFIX-038), `modules/core/src/GraphicsRendererSelection.cpp`: `PublishAvailable` and `ResetForTestingEXT` now only clear `attemptOrder` (it is rebuilt on first use) instead of calling `RebuildAttemptOrder` from the static initialiser. `ConsultEnvironmentOnce`/`ReadEnvironment` store `environmentError` and rethrow `InvalidOperationException` on every query, so a refusal is an ordinary exception (C API `CNA_RESULT_INVALID_STATE`). The Emscripten page property goes through the same `ReadEnvironment`. Tests at T: `GraphicsRendererSelectionTest.ARefusedEnvironmentVariableKeepsRefusingUntilARendererIsSet` (`modules/graphics/tests/CNA/GraphicsRendererSelectionTests.cpp:109`) and `CApi_RendererEnvironment_unknown`/`_absent` (`modules/c-api/tests/pure_c/RendererEnvironmentSmoke.c`, `modules/c-api/CMakeLists.txt:580-601`). | `"retired": {"CNA-BUG-077": {"classification": "PROVEN FIXED", "evidence": "<the evidence above>"}}` |
| CNA-GAP-001 | CNA-GAP-001 | ContentLoadException derives from std::runtime_error (status narrowed) | RETIRE-FIXED (PROVEN FIXED) | 2d85a276f (KF-13): `ContentLoadException.hpp` at T has `class ContentLoadException : public System::Exception`. `ContentRuntimeContractTests.cpp` now asserts `EXPECT_THROW(..., System::Exception)` in `TheParameterlessConstructorNamesItsOwnType` and `TheRestoredExceptionIsStillCatchableAsBefore`. Every XNA-named exception is now a `System::Exception`. What still derives from std types at T is CNA-internal only (`PlatformException`, `JsonParseException`, `XnbWriteException`, `ShaderCompilationExceptionEXT`, `HeadlessValidationException` and similar). | Retire as PROVEN FIXED. |
| CNA-BUG-078 | CNA-BUG-078 | F9/F10 fire the test-only context-loss hooks | EDIT (defect unchanged; Direct2D and GDI must go) | `Game.cpp:1479-1484` at T still calls `DebugSimulateContextLoss`/`DebugRestoreContext` with no guard. Overrides at T exist only for easygl, directx9/11/12 and webgpu. Direct2D removed by 0f96ea703, GDI by 261cb5f7f. | **actual**: delete `<li><code>Direct2D</code>: F9 recreates the complete device-resource domain.</li>`. Replace `<li>GDI overrides both hooks with empty bodies; the remaining renderers use the no-op defaults.</li>` with `<li>The remaining renderers use the no-op defaults.</li>`. Replace `(read at 009d40f5)` with `(read at b0e97bb1)`. **evidence**: `(EasyGL, DirectX 9/11/12, Direct2D, WebGPU, GDI)` becomes `(EasyGL, DirectX 9/11/12, WebGPU)`. `(<code>EasyGL</code>, <code>DirectX</code> 9/11/12, <code>Direct2D</code>, <code>WebGPU</code>, GDI)` becomes `(<code>EasyGL</code>, <code>DirectX</code> 9/11/12, <code>WebGPU</code>)`; this second string lives in patches-adversarial `entries.CNA-BUG-078.append.evidence`. **blast_radius**: `on the EasyGL, DirectX 9/11/12, Direct2D and WebGPU renderer families` becomes `on the EasyGL, DirectX 9/11/12 and WebGPU renderer families`. |
| CNA-BUG-090 | CNA-BUG-090 | GraphicsDeviceInformation accepts a null Adapter | EDIT (still valid; the variable name `gdi` trips check_retired_renderers) | `GraphicsDeviceInformation::setAdapterProperty` still stores any pointer. `GraphicsDeviceManager.cpp:727` still reads `graphicsDevice_->Reset(pp, *gdi.getAdapterProperty());`. The pointer overload of `Reset` still keeps the old adapter when given null. | **summary**: `passes *gdi.getAdapterProperty() to GraphicsDevice::Reset` becomes `dereferences its GraphicsDeviceInformation's getAdapterProperty() when it calls GraphicsDevice::Reset`. **actual**: `then calls <code>graphicsDevice_</code>-&gt;Reset(pp, *gdi.getAdapterProperty()), forming` becomes `then passes the dereferenced <code>getAdapterProperty()</code> of its <code>GraphicsDeviceInformation</code> argument to <code>graphicsDevice_-&gt;Reset</code>, forming`. Both fields come from patches-adversarial `set`. |
| CNA-GAP-006 | CNA-GAP-006 | GraphicsDeviceManager never calls FindBestDevice, RankDevices or CanResetDevice | EDIT (still valid; "GDI" in summary) | The three virtuals are defined at `GraphicsDeviceManager.cpp:528-547` and nothing in `modules/runtime/src` calls them. | **summary**: `(as a default GDI, a no-op and 'device exists')` becomes `(as a default GraphicsDeviceInformation, a no-op and 'device exists')`. |
| CNA-BUG-071 | CNA-BUG-071 | BoundingFrustum::Intersects differs from XNA 4.0 | EDIT (still valid; a source file was removed) | `BoundingFrustum.cpp` is unchanged. `modules/graphics-ext/src/FrustumCullerEXT.cpp` was deleted by 5572f3ca1 (MOD-RETIRE-1). | **sources**: drop `{"path":"modules/graphics-ext/src/FrustumCullerEXT.cpp",...}`. **actual**: `<code>BoundingBox::Intersects(BoundingFrustum)</code>, <code>BoundingSphere::Intersects(BoundingFrustum)</code> and graphics-ext's <code>FrustumCullerEXT</code> forward to these.` becomes `<code>BoundingBox::Intersects(BoundingFrustum)</code> and <code>BoundingSphere::Intersects(BoundingFrustum)</code> forward to these.`. **blast_radius**: `<p>Culling (extra draws, not missing ones),` becomes `<p>Game-side culling (extra draws, not missing ones),`. |
| CNA-BUG-002 | CNA-BUG-002 | BoundingSphere::Contains(BoundingFrustum) never returns Disjoint | EDIT (defect valid; text names removed engine classes) | `FrustumCullerEXT` and `ClusteredShadowPolicyEXT` were removed by 5572f3ca1; there are no BoundingFrustum consumers in graphics-ext at T except `DebugDraw`. | **blast_radius** (set via patches.json): delete ` (used by <code>FrustumCullerEXT</code> and <code>ClusteredShadowPolicyEXT</code>)`. |
| CNA-BUG-003 | CNA-BUG-003 | BoundingBox::Contains(BoundingFrustum) never returns Disjoint | EDIT (same reason) | 5572f3ca1 | **blast_radius**: `which classify the box against the frustum planes and are what the culling helpers use,` becomes `which classify the box against the frustum planes,`. |
| CNA-BUG-004 | CNA-BUG-004 | BoundingFrustum::Intersects(Ray) never computes an entry distance | EDIT (same reason) | 5572f3ca1 (removed `GpuInstanceCuller` and `FrustumCullerEXT`) | **blast_radius**: `Not affected: frustum tests against boxes, spheres, planes and other frustums, and the culling helpers in graphics-ext, which use box and sphere tests.` becomes `Not affected: frustum tests against boxes, spheres, planes and other frustums.`. |
| CNA-BUG-081 | CNA-BUG-081 | InactiveSleepTime is never honoured by the loop | CHANGED (defect unchanged, details outdated) | Still no reader of `InactiveSleepTime_` at T (only accessors, `Game.cpp:377/509-523`, and the C API). 16a1b67d9 (KF-15) changed the setter to throw `System::ArgumentOutOfRangeException("value", "...greater than or equal to zero...")` and added a test. | **actual**: `rejected when negative (the message says “must be positive” although zero is accepted)` becomes `rejected when negative with System::ArgumentOutOfRangeException and XNA's message (zero is accepted)`. **tests_current**: `No test in {{tree:modules/runtime/tests\|modules/runtime/tests}} reads or sets <code>InactiveSleepTime</code>.` becomes `{{src:modules/runtime/tests/Microsoft/Xna/Framework/GamePlatformTimingTests.cpp\|GamePlatformTimingTests.cpp}} (<code>InactiveSleepTimeRefusesNegativeButAcceptsZeroAsXnaDoes</code>) checks only the setter; no test checks that the loop sleeps while inactive.` (`tests_present` is already true.) |
| CNA-GAP-004 | CNA-GAP-004 | ShowMissingRequirementMessage is never called | CHANGED (minor) | `Game::Run` at T still logs and rethrows without consulting the hook; the hook still returns false (`Game.cpp:1093`). New since O: a71cc2415 (CBIND-144) adds `CreateGameGraphicsDevice` in Game's constructor, which wraps every device-creation failure in `NoSuitableGraphicsDeviceException`, still before Run. | **actual**: `throw sites read at 009d40f5` becomes `throw sites read at b0e97bb1`. Before `a hook wired into Run alone would not see those.` insert: `Since a71cc2415 Game's constructor also converts every other failure to create its device into a <code>NoSuitableGraphicsDeviceException</code> (<code>CreateGameGraphicsDevice</code>), likewise before Run;`. |

`patches-adversarial.json` holder for each target field:

- **CNA-BUG-078:**
  - `actual` comes from adversarial `set`.
  - `evidence` is the base text plus an adversarial `append`.
- **CNA-BUG-090:** `summary` and `actual` come from adversarial `set`.
- **CNA-BUG-002:** `blast_radius` comes from `patches.json`.
- **All other edited fields** are base verified text, so they need a new `entries.<id>.set`.

All 11 actioned entries keep their original stable key, so a plain `retired` or `entries` operation works for each.

#### 2. STILL VALID (37)

- **No source changed, re-checked at T:**
  - CNA-BUG-001 (aliased `Matrix::Transpose` in `Plane.cpp`)
  - CNA-BUG-026 (3.141593f guard; the `MatrixTests.cpp` change is only the new `ToColumnMajor` test)
  - CNA-BUG-027, -028, -063, -064, -065, -066, -068, -069, -070, -072, -073, -074, -076
  - CNA-BUG-251 (key NEW-AUDIT-01) and CNA-BUG-252 (NEW-AUDIT-02)
  - CNA-VGAP-002
- **CNA-BUG-067:** math throw sites unchanged. The `CnaCApiDetail.hpp:332-335` barrier still maps `out_of_range` to INVALID_ARGUMENT/RANGE and `invalid_argument` to INVALID_ARGUMENT/ARGUMENT. CHECKLIST.md:203 still records the mixed precedent.
- **CNA-BUG-075:** `Point` operators are still unmarked. `CNAEXT` itself survives, so that mention is fine.
- **CNA-BUG-259 (NEW-AUDIT-11):** `Decompose` unchanged. `DecomposeReportsPositiveScaleForAMirroredAffineTransform` is at `MatrixTests.cpp:826`. The CLAUDE.md "XNA wins" rule is at line 20.
- **CNA-VGAP-001:** builder tests unchanged. The retained graphics-ext `DebugDrawTests` and the ascii example still use `CreateLookAt` and `CreatePerspectiveFieldOfView`, so "graphics-ext consumers" is still true.
- **CNA-BUG-080:** `EmscriptenMainLoopCallback` (`Game.cpp:1268-1349`) still caps the delta at 250 ms, ignores `IsFixedTimeStep`, `suppressDraw_` and `forceElapsedTimeToZero_`, forces `IsRunningSlowly=false`, and its catch clears the slot without raising Exiting. KILLER-1 only added a `RunApplication` guard.
- **CNA-BUG-082:** `registerServices` still adds the `ClientSizeChanged` lambda without a token, Game still caches the raw pointers, and the C API `RetiredManagers` workaround remains. The new `keyboardOrientationChanged_` callback is cleared in Dispose.
- **CNA-BUG-083:** `modules/phone` unchanged.
- **CNA-BUG-085:** the `updateFrameLag_` logic (`Game.cpp:854-871`) is unchanged.
- **CNA-BUG-086:** `GameComponent::Dispose(bool)` still only raises Disposed. KF-14 changed only exception types and ownership in `GameComponentCollection`.
- **CNA-BUG-087:** the `Game::Dispose(bool)` live-index loop (`Game.cpp:1108`) is unchanged.
- **CNA-BUG-088:** the variable-step branch (`Game.cpp:879-907`) still passes the whole accumulator.
- **CNA-BUG-091:** `GameWindow::window_` is set only in `setWindowInternal` and never cleared; `destroyNativeResources` still resets `platformWindow_` (`GraphicsDevice.cpp:4547`).
- **CNA-BUG-092:** the four `Texture` helpers and the `IsBorderlessEXT` accessors are still unmarked. The strict-mode tests are still at `Harnesses.cmake:222/240`.
- **CNA-BUG-260 (NEW-AUDIT-12):** `ExitingEventArgs.hpp` is unchanged, unmarked and never raised.
- **CNA-GAP-002:** `Logger.cpp` unchanged; `minimumLevel_` is still unsynchronised.
- **CNA-GAP-003:** `Misc.hpp` unchanged, still defined nowhere; the `CApi_UnimplementedRuntimeFacade` test (`modules/c-api/CMakeLists.txt:530`) and the `cna-runtime-facade` coverage rule are still present.
- **CNA-GAP-005:** `DrawableGameComponent.cpp:63` still has the "Until that service exists" comment and `OnDeviceCreated` is still unsubscribed.
- **CNA-GAP-007:** 99 public headers still include `Prop.hpp` or `SharpRuntimeHelper.hpp` (the same count at O and at T).
- **CNA-GAP-063 (key CNA-BUG-079):** the `MaxElapsedTime` clamp (`Game.cpp:815`) is still before the fixed-step loop, and the `Game.hpp` doc still says only "positive and non-zero".

#### 3. New issue noticed at T (low; optional)

New at T, `modules/runtime/tests/Microsoft/Xna/Framework/RuntimePlatformTestSupport.hpp:14` declares `namespace CNA::Runtime::Testing`. That clashes with `class CNA::Runtime` in `modules/runtime/include/CNA/Misc.hpp`, so any translation unit including both fails to compile. It is test-only and latent, since nothing includes `Misc.hpp`; it could be added as a sentence to CNA-GAP-003.

#### 4. Counts (48)

| Disposition | Count |
|---|---|
| RETIRE-FIXED | 2 (BUG-077, GAP-001) |
| RETIRE-OBSOLETE | 0 |
| NARROWED | 0 |
| EDIT | 7 (BUG-002, -003, -004, -071, -078, -090, GAP-006) |
| CHANGED | 2 (BUG-081, GAP-004) |
| STILL VALID | 37 |

Of the EDITs, BUG-078, BUG-090 and GAP-006 are required, because check_retired_renderers fails on "Direct2D", "GDI" and "gdi". The other four remove mentions of removed engine-layer helpers or the dead `FrustumCullerEXT.cpp` source path.

All 48 entries say "checked/read at 009d40f5" in their evidence or actual text. Moving the pin needs a global wording change; the per-entry substitutions above don't cover it.


---

## Appendix MEDIA: Audio & media + Content + Models & glTF


MEDIA batch (50 entries: audio, media, content, models): disposition of every entry at T=b0e97bb1 against O=009d40f5.

**Result.** No entry in this batch is about a removed renderer or the removed engine layer, so nothing is retired as OBSOLETE. No entry is fully fixed. 7 entries need action and 43 are still valid.
- **3 narrowed (partly fixed):** BUG-041 (fixed in part by CBIND-140 and BL-19), BUG-122 (KF-9), BUG-148 (KF-12).
- **2 changed:** BUG-016 and GAP-047.
- **2 edits for the SDL2 removal:** BUG-140 and BUG-142.
- None of the 50 entries has a dead source path at T, a dead inline `{{src:}}` or `{{tree:}}` token, or a retired-renderer spelling in its text.
- Every actionable entry's stable key equals its published id. GAP-066 (key CNA-BUG-127) and GAP-068 (key CNA-PLAT-010) are still valid, so their reclassification lines need no change.

#### (1) Entries needing action

| published id | stable key | short title | disposition | evidence at T | proposed change |
|---|---|---|---|---|---|
| CNA-BUG-041 | CNA-BUG-041 | ContentManager relative root vs TitleLocation; Android tiers | NARROWED further (already `narrowed`) | **9976f4909 (CBIND-140):** `ContentManager::TitleRootedDirectory()` resolves the root through `CNA::Internal::ResolveContentRoot(rootDirectory_, title)`. `TitleLocation::setPathProperty` and `Initialize` now call `CNA::Internal::SetTitlePath`. Pinned by `modules/content/tests/CNA/Internal/ContentRootTests.cpp` (`ARelativeRootThatExistsUnderTheTitleIsReadFromThere` plus 3 others).<br>**5d275f556 (BL-19):** both `.cnb` tiers (generic and `SoundEffect`) read through `TryReadAssetBytes` and parse with `CnbDocument::Parse`.<br>**What survives:** `ResolveAssetPath` (ContentManager.hpp) still gates the literal, `.cnj` and reader-extension probes on `std::filesystem::exists`. `ImageLoader::Load` still opens with `std::ifstream`. On Android `TitleRootedDirectory` returns `rootDirectory_` unchanged. `StandardFileSystem::GetBasePath` still returns `current_path()`, and `TitleLocation::DetectBasePath` uses it. So X11, Wayland, native Win32, headless and terminal still root content in the working directory. | Text below (block A). Sources unchanged; optionally add `modules/content/src/Internal/ContentRoot.cpp` (note "ResolveContentRoot: under the title when that directory exists, else the working directory"). |
| CNA-BUG-122 | CNA-BUG-122 | Load<T> leaks non-XNA exception types | NARROWED (set `status: narrowed`) | **Wrong-type case fixed by 0af45cbd4 (KF-9):** every `any_cast` in ContentReader.hpp goes through `CastReadResult<T>`, which throws ContentLoadException. Test: `CustomContentTypeReaderTest.LoadingAsAnotherTypeThrowsContentLoadExceptionNotBadAnyCast`. XnbContainerFuzzTests no longer accepts `std::bad_any_cast`.<br>**Still present:** `Load<Audio::SoundEffect>` ends in an unwrapped `return reader.Read(resolvedPath, *this);`. `SoundEffect(const std::string&)` throws `System::NotSupportedException`. `throw std::runtime_error("ContentManager has been disposed.")` remains at ContentManager.hpp `Load` and at ContentManager.cpp lines 256 and 6486.<br>**Context:** since 2d85a276f (KF-13) ContentLoadException derives from System::Exception. | Text below (block B). |
| CNA-BUG-148 | CNA-BUG-148 | SubmitBuffer accepts empty and partial-frame buffers | NARROWED: XNA-contract part fixed, float extension remains. Alternative: RETIRE PROVEN FIXED, if the FNA-only extension is judged contract-free. | **Fixed by 49119a34c (KF-12):** `SubmitBuffer` throws `ArgumentException` for an empty buffer, a size not a whole number of frames, and an offset or count off a frame boundary or out of range (64-bit sum). Test: `DynamicSoundEffectInstanceTest.SubmitBufferRefusesPartialFrames` and `...WhilePlaying`.<br>**Still present:** `SubmitFloatBufferEXT(buffer, offset, count)` checks only the range. The test `SubmitFloatBufferWithSampleCountNotDivisibleByChannelCountDoesNotThrow` pins the acceptance, and plans/plan_audio.md AUD-07-006 is still open. | Text below (block C). |
| CNA-BUG-016 | CNA-BUG-016 | `ParseJson` recursion without a depth limit | CHANGED (reach list) | `Json.hpp` is unchanged, so the defect stands.<br>38287637d (GS-AUDIT-005) moved `LocalGamerServicesStore::TryReadJsonFile` to `nlohmann::json` (`StoreJson::parse`, catches `StoreJson::exception`). Within that file `ParseJson` is now reached only by `ParseOfflineCatalog` (the title's offline achievement catalog, 529f22e45 GS-004p). | Text below (block D). |
| CNA-GAP-047 | CNA-GAP-047 | XMA/WMA wave-bank entries silent | CHANGED (diagnostic channel) | 9d04c6702 (BINDFIX-051): `WaveBank::GetSoundEffect` now calls `CNA::Internal::Audio::LogAudio(CNA::LogLevel::WARN, "... sound will be missing")` instead of `std::cerr`, then still returns `nullptr`. | Text below (block E). |
| CNA-BUG-140 | CNA-BUG-140 | MediaPlayer::Play reports no error on failure | EDIT (SDL2) | 76c9bda29 removed SDL2 audio. `cmake/AudioPlatformSelection.cmake` now allows `SDL3 \| NULL \| ALSA`. The defect itself is unchanged: MediaPlayer.cpp is identical at O and T. | blast_radius: `'In builds without a mixer (SDL2 or NULL audio)'` -> `'In builds without a mixer (NULL audio)'` |
| CNA-BUG-142 | CNA-BUG-142 | Without a mixer songs never end | EDIT (SDL2) | 76c9bda29 as above. `SOUND_ENABLED` is still defined only for SDL3 and ALSA (modules/CMakeLists.txt). `LoadSong` is unchanged. | Exact substitutions below this table. |

**CNA-BUG-142 substitutions:**
- title: `'Without a mixer (SDL2 or NULL audio) songs never end'` -> `'Without a mixer (NULL audio) songs never end'`
- public_contract: `'under CNA_AUDIO_PLATFORM=SDL2 or NULL'` -> `'under CNA_AUDIO_PLATFORM=NULL'`
- actual: `'In the other builds <code>Update</code>'` -> `'In the NULL audio build, the only other selection since SDL2 audio was retired (76c9bda29), <code>Update</code>'`
- blast_radius: `'SDL2 and NULL audio selections only, where'` -> `'The NULL audio selection only, where'`
- workaround: `'in these profiles'` -> `'in this profile'`

##### Block A: CNA-BUG-041 (set)

**title:**
"A relative ContentManager root still follows the working directory on the non-SDL3 platforms, and the loose tier cannot see Android packaged assets"

**summary (237 characters):**
"ContentManager now roots a relative RootDirectory under TitleLocation and reads .cnb through the platform on Android, but TitleLocation is the working directory on the non-SDL3 platforms and the loose tier still gates on std::filesystem::exists."

**actual:**
"<p><code>BuildAssetPath</code> joins <code>TitleRootedDirectory()</code> and the asset name. Off Android, that function passes the root through <code>CNA::Internal::ResolveContentRoot</code> ({{src:modules/content/src/Internal/ContentRoot.cpp|ContentRoot.cpp}}): a relative root is used under the title path (<code>TitleLocation</code>'s path, else the platform's <code>GetBasePath()</code>) when that directory exists, and is otherwise left relative to the working directory. On the SDL3 platform the title path is the executable directory. On the X11, Wayland, native Win32, headless and terminal platforms it is the working directory, because <code>StandardFileSystem::GetBasePath</code> ({{src:modules/platform/src/Common/StandardFileSystem.cpp|StandardFileSystem.cpp}}) returns <code>current_path()</code>. A game started from another directory therefore still misses its default <code>Content</code> root there.</p><p>On Android the root is used as given, and <code>TryReadAssetBytes</code> forwards a relative path to the platform file system. That reaches packaged assets for the <code>.xnb</code> tier and, since BL-19, for both <code>.cnb</code> tiers. <code>ResolveAssetPath</code> ({{src:modules/content/include/Microsoft/Xna/Framework/Content/ContentManager.hpp|ContentManager.hpp}}) still tests the literal path, the <code>.cnj</code> candidate and every reader extension with <code>std::filesystem::exists</code>, which cannot see APK assets, and the built-in <code>Texture2D</code> loose reader opens through <code>ImageLoader::Load</code>'s <code>std::ifstream</code>.</p><p><strong>Fixed since first recorded:</strong> a relative root resolves under the title (CBIND-140, 9976f4909) and the <code>.cnb</code> tiers read through <code>TryReadAssetBytes</code> (BL-19, 5d275f556). Earlier fixes: <code>TitleContainer</code> and <code>TitleLocation</code> have in-tree consumers ({{src:modules/c-api/src/CnaCApiGameProperties.cpp|CnaCApiGameProperties.cpp}}), and the <code>.xnb</code> tier's Android route goes through <code>Sdl3FileSystem::TryLoadFileIgnoringCase</code>.</p>"

**tests_current:**
"<p>{{src:modules/content/tests/CNA/Internal/ContentRootTests.cpp|ContentRootTests.cpp}} pins <code>ResolveContentRoot</code> (a root under the title, a missing title directory, an absolute root, no title). {{src:modules/content/tests/Microsoft/Xna/Framework/Content/UnicodeContentRootTests.cpp|UnicodeContentRootTests.cpp}} and {{src:modules/content/tests/Microsoft/Xna/Framework/Content/ContentPathContainmentTests.cpp|ContentPathContainmentTests.cpp}} use absolute roots. No Android content-path test runs in <code>CnaTests</code>, and no test loads through a non-SDL3 platform from another working directory.</p>"

**regression_test:**
"<p>On Android, one device test per tier (<code>.cnj</code>, a loose PNG, a loose WAV) loaded from the APK with the relative root <code>\"Content\"</code>. On a platform backed by <code>StandardFileSystem</code>, a <code>Load&lt;T&gt;</code> with the working directory changed away from the executable's directory.</p>"

**blast_radius:**
"<p>Games on the X11, Wayland, native Win32, headless or terminal platforms launched from another directory with a relative root. On Android, every <code>.cnj</code> and loose (non-compiled) asset shipped inside the APK. The SDL3 platform on desktop, absolute roots, and <code>.xnb</code> and <code>.cnb</code> content on Android are unaffected.</p>"

**workaround:**
"<p>On the platforms whose base path is the working directory, build an absolute root from the executable's own directory by host means, or start the game from its directory. On Android, ship run-time content as <code>.xnb</code> or <code>.cnb</code>.</p>"

**Also:**
- evidence: drop or rewrite the two sentences "The disagreement with <code>TitleContainer</code> exists only on the SDL3 platform: the SDL2, X11, ..." (they name SDL2 and describe pre-CBIND-140 code).
- evidence (append): "<p>Re-checked by reading at b0e97bb1: TitleRootedDirectory, ResolveContentRoot, ResolveAssetPath, ImageLoader::Load and StandardFileSystem::GetBasePath; not executed.</p>"

##### Block B: CNA-BUG-122 (set status `narrowed`)

**title:**
"ContentManager::Load<T> leaks non-XNA exception types: unwrapped Load<SoundEffect> errors and std::runtime_error when disposed"

**summary (256 characters):**
"ContentManager::Load wraps loose-reader failures in ContentLoadException, but the SoundEffect specialization lets System::NotSupportedException escape from its loose tier, and a disposed manager throws std::runtime_error instead of ObjectDisposedException."

**actual:** delete the first `<li>` (the one beginning `<li><strong>Wrong type on the <code>.xnb</code> tier.</strong>` and ending `throws <code>std::bad_any_cast</code>.</li>`).
- Replace `'therefore miss all three.</p>'` with `'therefore miss both. Since KF-13 (2d85a276f) <code>ContentLoadException</code> derives from <code>System::Exception</code>, so a <code>catch (System::Exception)</code> now covers the <code>SoundEffect</code> case; only the disposed manager's <code>std::runtime_error</code> escapes it.</p><p><strong>Fixed since first recorded:</strong> a reader that produces another type than requested is a <code>ContentLoadException</code> naming both types (<code>CastReadResult</code> in {{src:modules/content/include/Microsoft/Xna/Framework/Content/ContentReader.hpp|ContentReader.hpp}}, KF-9, 0af45cbd4).</p>'`.

**reproduction:** delete the first try/catch (the `Load<Graphics::Texture2D>("click")` lines and the `// Content/click.xnb holds a SoundEffect` comment).

**tests_current:** replace with
"<p>{{src:modules/content/tests/Microsoft/Xna/Framework/Content/CustomContentTypeReaderTests.cpp|CustomContentTypeReaderTests.cpp}} pins the fixed wrong-type case (<code>LoadingAsAnotherTypeThrowsContentLoadExceptionNotBadAnyCast</code>). {{src:modules/content/tests/Microsoft/Xna/Framework/Content/ContentRuntimeContractTests.cpp|ContentRuntimeContractTests.cpp}} checks <code>ObjectDisposedException</code> for <code>ReadAsset&lt;T&gt;</code> only. No test calls <code>Load&lt;SoundEffect&gt;</code> on a missing file or <code>Load&lt;T&gt;</code> after <code>Dispose()</code>.</p>"

**regression_test:** drop the `Load<Texture2D>` of `tone_mono_44khz_16bit.xnb` clause and the fuzz-narrowing sentence.

**evidence:** drop `std::bad_any_cast` from the list of escaping types in the XnbContainerFuzzTests sentence.

##### Block C: CNA-BUG-148 (set status `narrowed`)

**title:**
"DynamicSoundEffectInstance::SubmitFloatBufferEXT accepts empty and non-frame-aligned float buffers"

**summary (234 characters):**
"SubmitBuffer now refuses partial frames as XNA does, but SubmitFloatBufferEXT still queues an empty buffer or a sample count that is not a whole number of channel frames, which SDL3 audio then drops and CNA's ALSA mixer plays shifted."

**public_contract:**
"DynamicSoundEffectInstance::SubmitFloatBufferEXT(const std::vector<float>&[, int offset, int count])"

**actual:**
"<p><code>SubmitFloatBufferEXT</code> in {{src:modules/audio/src/Xna/DynamicSoundEffectInstance.cpp|DynamicSoundEffectInstance.cpp}} throws only for a disposed instance, a negative or overrunning offset or count, and the int/float mode guard. An empty buffer, a zero count and a sample count that is not a multiple of the channel count are queued. SDL3 audio refuses the resulting partial frame (<code>SDL_PutAudioStreamData</code>); CNA logs \"stream submit failed (N bytes dropped)\" and the chunk is lost. CNA's ALSA mixer appends it, shifting every later sample.</p><p><strong>Fixed since first recorded:</strong> <code>SubmitBuffer</code> refuses an empty buffer, a partial frame and an off-frame offset or count with <code>ArgumentException</code> (KF-12, 49119a34c).</p>"

**tests_current:**
"<p><code>SubmitBufferRefusesPartialFrames</code> and <code>SubmitBufferRefusesPartialFramesWhilePlaying</code> pin the fixed integer path. <code>SubmitFloatBufferWithSampleCountNotDivisibleByChannelCountDoesNotThrow</code> pins the float path's acceptance (P9-DYNAMIC-009).</p>"

**Also:** in the expected and regression_test fields, keep only the float-path sentences; the related plan item is AUD-07-006 (open).

##### Block D: CNA-BUG-016 (set)

**public_contract:**
"CNA::Internal::ParseJson - documented to throw JsonParseException for malformed input; reached by every .cnj load, the .cnj compilers and the gamer-services offline achievement catalog"

**actual:**
- `'no <code>catch</code> in <code>ContentManager</code>, the build tools or <code>TryReadJsonFile</code> can intercept it'` -> `'no <code>catch</code> in <code>ContentManager</code>, the build tools or the gamer-services catalog reader can intercept it'`
- `'and {{src:modules/gamer-services/src/Internal/LocalGamerServicesStore.cpp|LocalGamerServicesStore.cpp}}.'` -> `'and <code>ParseOfflineCatalog</code> in {{src:modules/gamer-services/src/Internal/LocalGamerServicesStore.cpp|LocalGamerServicesStore.cpp}} (the title's offline achievement catalog). The store's own persisted files are parsed with nlohmann::json since GS-AUDIT-005 (38287637d) and no longer reach this parser.'`

**expected:** drop the sentence `'<code>LocalGamerServicesStore</code> promises that a corrupt store file "starts empty rather than throwing".'`

**blast_radius:**
`'and the gamer-services store at start-up (where a corrupted store file should degrade to empty but can crash instead).'` -> `'and the gamer-services offline achievement catalog (a title-shipped file).'`

**sources:** change the LocalGamerServicesStore.cpp note to "ParseOfflineCatalog - the offline achievement catalog is parsed with ParseJson; persisted store files use nlohmann::json (GS-AUDIT-005)".

**related:** check that `development/internals/modules/gamer-services.html#store-failure` still fits.

##### Block E: CNA-GAP-047 (set)

**summary:**
"WaveBank::GetSoundEffect returns null for XMA and WMA entries after logging a warning through CNA's logger, so cues using them are silent."

**actual:**
`'after writing &#8220;sound will be missing&#8221; to <code>std::cerr</code>'` -> `'after logging &#8220;sound will be missing&#8221; at WARN through CNA's logger (<code>LogAudio</code>, BINDFIX-051)'`

**blast_radius:**
`'with only a stderr line'` -> `'with only a logged warning'`

#### (2) Still valid (verified at T)

**Content (XNB/CNB/CNJ)**
- **BUG-008:** `ResolveAssetPath` still tries literal, then `.cnj`, then extensions; `SongTypeReader` and `VideoTypeReader::Read` have no `.cnj` branch (ContentManager.cpp lines 6106-6135). Song.cpp and Video.cpp are unchanged.
- **BUG-017:** `TryReadAssetBytes` still checks only `INT32_MAX`; `ScanXnbReaderNames` reads the whole file. Optional: since BL-19, `.cnb` is read whole through the same function.
- **BUG-021:** `Unload()` is still `loadedAssets_.clear()`; `RecordDisposable`'s "XNB-17B" deferral comment is still in ContentReader.hpp (line 595).
- **BUG-022:** ContentReader.cpp, ContentTypeReader.hpp and ReflectiveTypeReader.hpp are unchanged.
- **BUG-119:** ContentTypeReaderManager.cpp, ContentTypeReader.hpp and ContentReader.cpp are unchanged.
- **BUG-120:** `LoadXnbAssetUntyped` still reads 4 bytes at offset 10 with only the `[10, size]` check, and its LZ4 branch still throws "does not yet support".
- **BUG-121:** `Load<T>` still reads the `.xnb` tier through `TryReadAssetBytes`; `OpenStream` is called only from `ReadAsset`. ResourceContentManager is unchanged.
- **BUG-123:** the cache is still filled only after a successful load; ContentReader.cpp is unchanged.
- **BUG-124:** `LooseFileContentTypeReader<T>& reader = **readerPtr;` (ContentManager.hpp line 572); `RegisterTypeReader` still replaces the `shared_ptr` (line 301).
- **BUG-125:** XnbDecompression.cpp and LzxDecoder.cpp are unchanged.
- **BUG-126:** `InnerReadObjectAny` in ContentReader.cpp is unchanged; KF-9 touched only the casts.
- **GAP-034:** DecimalDateTimeContentTypeReaders.hpp is unchanged.
- **GAP-066:** `ApplyColorKey` still writes `Color(keyR, keyG, keyB, 0)` (ContentManager.cpp line 766).

**Models and glTF**
- **BUG-128:** `Model::Draw` still grows `sharedDrawBoneMatrices_` only to the bone count and reads `[boneIdx]` unchecked (lines 436-457); the Model.cpp diff touches only the bounding-sphere comment.
- **BUG-129:** `BlendMorphTargetsEXT` is unchanged; b2fd47a45 only adds unbind/rebind around `SetDataRaw`.
- **BUG-130 and BUG-131:** the ContentManager.cpp diff does not touch the `.cnj` Model mesh loop, `BuildModelMeshPartGeometryEXT` or `ParseCnjBoneArrayEXT`.
- **GAP-035:** `setCamerasEXTProperty` in content is still only in the glTF path (line 4339). The C API setter already existed at O. gltf_to_cnj still only reports `cameraNodeCount`.
- **GAP-036:** the "unitScale is always 1.0" comment is still there (line 2896); the converter options are unchanged.
- **GAP-037:** the `gpu-instancing-dropped` diagnostic and gltf-limitations.md (UNSUPPORTED, §4.1) are unchanged.
- **GAP-038:** the `mirrored-winding-unapplied` diagnostic is still present; mirroring is not handled.
- **GAP-039:** the `uv-set-mismatch`, `influence-sets-dropped` and `color-sets-dropped` diagnostics are still present.
- **GAP-040:** the `rigid-animation-dropped-on-skinned-model` diagnostic is still present.
- **GAP-041:** `ExtractMorphWeightTrack` is unchanged; the CNASTREET-SKINDRAW diff touches `BuildSkeleton` only.
- **GAP-042:** `BuildTrack` and AnimationPlayer are unchanged.
- **GAP-043:** `kMaxPaletteBones = 72` (GltfImportCore.cpp line 1644).
- **GAP-044:** `ExtractPunctualLightsEXT` and the docs row are unchanged.

**Audio**
- **BUG-052:** `SDLMIXER_OPUS=OFF` is still set (ThirdPartySDL.cmake line 396); `SongTypeReader` still lists `.opus`, `.aac` and `.wma`; MediaLibraryIndex still indexes `.opus`.
- **BUG-147:** `kFireAndForgetSafetyNet{5}` minutes and the sweep at line 150 are still there; BINDFIX-051 changed only logging.
- **BUG-149:** `Microphone::Start` still has `catch (...)` (line 218) and an unconditional `Started` (line 226).
- **GAP-045:** `INTERNAL_applyReverb` is still a no-op; the limits, filter decode and RPC code changed only in logging.
- **GAP-046:** there is no `throw InstancePlayLimitException` in modules/ outside the tests.

**Media and video**
- **BUG-137, BUG-138, BUG-139:** MediaPlayer.cpp and MediaQueue.cpp are identical at O and T.
- **BUG-141:** MediaPlayer.hpp/.cpp and CnaCApiMediaPlayer.cpp are unchanged.
- **BUG-143, BUG-144, BUG-145:** the VideoPlayer.cpp diff is a comment-only SDL2 cleanup; VideoDecoder.cpp and Video.cpp are unchanged.
- **BUG-146:** VideoDecoder.cpp is unchanged.
- **GAP-068:** `_cna_ffmpeg_platform_supported` is still OFF for MINGW, WIN32, EMSCRIPTEN, ANDROID and CNA_APPLE_IOS; video-backend.md still lists MEDIA-192 to MEDIA-195.

**Verification gaps**
- **VGAP-005:** UnitTests.cmake still filters the same 8 suites for non-SDL3 audio, now 440 TEST definitions (442 at O), so "about 440" stands. CnaMixerXnaTests still has 7 cases; the platform-ci.yml ALSA cell and its filter are unchanged.
- **VGAP-006:** every cited file is unchanged.

#### (3) New issues noticed at T
None that warrant a new entry. Two observations:
- The BUG-148 residual (float path) is pinned by a deliberate CNA test and by the still-open plan_audio.md item AUD-07-006. That is CNA's own record that the gap is still open.
- KF-7/KF-8 (duration/size conversions), KF-17 (WAVE with zero channels), CBIND-146 (content sample rate) and CNA-F20/LRS-R29 (shared model textures) fix defects that no MEDIA entry describes, so none of them retires anything here.

#### (4) Counts
| Disposition | Count | Entries |
|---|---|---|
| RETIRE-OBSOLETE | 0 | — |
| RETIRE-FIXED | 0 | BUG-148 could be retired instead; see its row |
| NARROWED | 3 | BUG-041, BUG-122, BUG-148 |
| CHANGED | 2 | BUG-016, GAP-047 |
| EDIT (SDL2) | 2 | BUG-140, BUG-142 |
| STILL VALID | 43 | |
| **Total** | **50** | |

Helper scripts are in the work folder r9work/ (`media_show.py`, `media_full.py`, `media-cm.diff`). No repository files were modified.


---

## Appendix DOC: Documentation & release tooling


Task: classify the 48 entries in batch-DOC (Documentation & release tooling) at T=b0e97bb1 against O=009d40f5.

#### R9 batch DOC: 48 entries

**Counts:** RETIRE-FIXED 3 (BUG-062, 233, 236) · RETIRE-OBSOLETE 1 (BUG-249) · CHANGED 3 (BUG-055, 056, 058) · EDIT 1 (BUG-224) · STILL VALID 40 (BUG-274 has one conditional `related` fix).

All entries in this batch have stable key equal to published id, except BUG-254/256/261/271/272/273/274 (keys NEW-AUDIT-04/08/13/28/29/30/31). Those are all STILL VALID, so the added/reclassified renumbering problem does not come up here.

#### (1) Entries needing action

| id | key | short title | disposition | evidence at T | proposed change |
|---|---|---|---|---|---|
| CNA-BUG-062 | CNA-BUG-062 | MODULE_SCOPE leaves design/diagnostics/inspector unclassified, every C API inventory gate stops | **RETIRE-FIXED** (`PROVEN FIXED`) | 5572f3ca1 (MOD-RETIRE-1) adds `"design"`, `"diagnostics"`, `"inspector"` as `Scope.OUT_OF_SCOPE` to `MODULE_SCOPE` in `tools/c-api/generate_coverage_inventory.py`. At T, `docs/c-api/COVERAGE.md` is regenerated: the excluded-module table lists `modules/design` (16), `modules/diagnostics` (2) and `modules/inspector` (3); snapshot is 469 headers / 8142 symbols. `tools/c-api/test_coverage_scope.py::test_the_repository_classifies_every_publishing_module` exists. Recorded by CNA in merge 8b55f7f4d (2026-10-01): "CApi: 113/116, CApiAbiBaseline and CApiCoverageMatrix pass; the three failures are the audio smokes". | `retired` with classification `PROVEN FIXED`. **Also needed:** CNA-GAP-062 `actual` and `tests_current` cite "(CNA-BUG-062)" as the reason the backlog cannot be regenerated or its gates fail; edit both (GAP-062 is in another batch). Hand-written site links to cna-bug-062 must go: `docs/roadmap.html` lines 256 and 309, `docs/c-api.html` line 235. |
| CNA-BUG-233 | CNA-BUG-233 | CLAUDE.md lists WIN32 as a reserved identifier | **RETIRE-FIXED** | 76c9bda29 rewrote CLAUDE.md lines 501–502: "`SDL3`, `X11`, `WAYLAND`, `HEADLESS`, `TERMINAL`, or host-conditional `WIN32`". The "SDL12/WIN32/EMSCRIPTEN are reserved" sentence is gone. It agrees with `cmake/PlatformSelection.cmake` (WIN32 available on Windows; SDL12 and EMSCRIPTEN reserved). | `retired` `PROVEN FIXED`. Small leftover, too minor for an entry: CLAUDE.md does not say TERMINAL is reserved on Windows (PlatformSelection.cmake lines 89–93). Remove the link at `docs/native-platforms.html` line 519. |
| CNA-BUG-236 | CNA-BUG-236 | platform-abstraction.md Implementations table omits X11 and Wayland | **RETIRE-FIXED** | 76c9bda29: at T the `docs/platform-abstraction.md` table has rows `SDL3`, `WIN32`, `X11` (`CNA::Platform::X11`, links platform-x11.md), `WAYLAND` (`CNA::Platform::Wayland`, links platform-wayland.md), `HEADLESS`, `TERMINAL`. The SDL2 row is gone. | `retired` `PROVEN FIXED`. The entry's minor side note still holds: the compile-scope paragraph mentions only HEADLESS, TERMINAL and WIN32. Remove the link at `docs/native-platforms.html` line 520. |
| CNA-BUG-249 | CNA-BUG-249 | misc/CNAEXT.md PBR coverage table omits OPENGL4/METAL; says WebGPU has no skinned PBR | **RETIRE-OBSOLETE** | 5572f3ca1 put a banner at the top of `misc/CNAEXT.md`: "Historical record: The modern graphics-engine layer described below was removed in the 2026-09 scope reduction … Do not use the old code examples or capability claims as current documentation." The entry's premise ("maintained as current support rather than a dated snapshot") no longer holds. Two of its contradictions concern removed renderers: OPENGL4 (261cb5f7f) and PORTABLEGL (0f96ea703). Both cited sources are gone: `OpenGL4StockDraw.cpp` and `PortableGLRenderer.cpp`. The entry carries retired-identity spellings in nearly every field. | `retired` `OBSOLETE`. Remove the links at `docs/effects.html` line 662 and `docs/tutorials/114-pbr-materials.html` line 351. |
| CNA-BUG-055 | CNA-BUG-055 | stale whole-registry renderer counts | **CHANGED** | At T the registry has 18 public identities over 14 families: the `cmake/RendererIdentities.cmake` public list; `docs/runtime-renderer-selection.md` line 28 says "14 implementation families / 18 public renderer identities"; `CNA_GRAPHICS_RENDERER_MAXIMUM` is `CNA_GRAPHICS_RENDERER_FNA3D` (graphics.h line 72; was 46). The C API has no DIRECT2D/OPENGL4 constants. The old stale counts are all still present: CORE.md line 60 "50 public renderer identities"; FEATURE_MATRIX.md line 30 "50"; core_ext.h line 621 "the 46 identities"; ModuleProbes.cmake line 6 "the 42 public renderer identities"; CHANGELOG.md line 146 "49 renderer identities"; LIMITATIONS.md line 133 "Four of the 49 renderers". The "25" the entry cited as correct is now stale too: LIMITATIONS.md line 143, COMPATIBILITY.md line 54, `tools/c-api/compatibility_matrix.json` line 99 and `tools/c-api/coverage_mappings.json` lines 7454/7487/7517/7550 ("any of the 25 public renderer identities"). | **title** → "Stale whole-registry renderer counts survive outside check_renderer_identities.py's list: CORE.md and FEATURE_MATRIX.md say 50, core_ext.h 46, ModuleProbes.cmake 42, the C API limitation and mapping records 25, and CHANGELOG 49 for a 50-identity release". **summary** → "CNA has 18 public renderer identities, yet the C API's backend-classification contract and mapping records, a public C header's Doxygen, a CMake test header and the alpha.1 release notes still state obsolete totals that no count gate reads." (240 chars). **actual:** 'The routes accept the 25 and refuse everything else, as `<code>tools/c-api/coverage_mappings.json</code>`, the C API\'s own mapping record for the same routes, says.' → 'The routes accept the 18 identities of `<code>cmake/RendererIdentities.cmake</code>` and refuse everything else (`<code>MapRendererType</code>` in `<code>CnaCApiCoreExt.cpp</code>`); `<code>tools/c-api/coverage_mappings.json</code>`, the C API\'s own mapping record for the same routes, still says 25, as do the generated `<code>docs/c-api/LIMITATIONS.md</code>` and `<code>COMPATIBILITY.md</code>` bullet "CNA has 25 renderer identities; four are built and run here. The other 21 …" (from `<code>tools/c-api/compatibility_matrix.json</code>`).' **evidence:** 'now states 21 families / 25 identities' → 'now states 14 families / 18 identities'; 'while a later bullet in the same file says CNA has 25 renderer identities' → '… says CNA has 25 renderer identities (both figures are stale at TARGET, which has 18)'. **blast_radius:** '(46, with retired values reserved)' → '(43, `<code>FNA3D</code>`, with retired values reserved)'. **sources notes:** cmake/RendererIdentities.cmake → "18 public renderer identities at this snapshot"; tools/c-api/compatibility_matrix.json → "source of the stale 'CNA has 25 renderer identities' note"; docs/c-api/LIMITATIONS.md → "the 'Four of the 49 renderers' row and the '25 renderer identities' bullet, both stale". **Add source** `tools/c-api/coverage_mappings.json` — "backend-classification mapping and test rows: 'any of the 25 public renderer identities'". |
| CNA-BUG-056 | CNA-BUG-056 | FEATURE_MATRIX/README say ABI 0.1.0 | **CHANGED** (only the version moved) | `abi.h` lines 34–40 declare 0.44.0. RELEASE_GATE.md reads "CNA C ABI 0.44.0, experimental". FEATURE_MATRIX.md lines 1, 5, 17 and 277 and README.md line 5 still say 0.1.0 / "0.1". | Replace "0.29.0" with "0.44.0" in **title**, **actual** ("finds 0.29.0 against 0.1.0"), **evidence** ('"CNA C ABI 0.29.0, experimental"') and **blast_radius** ("The library reports 0.29.0"). |
| CNA-BUG-058 | CNA-BUG-058 | LIMITATIONS omits planned rows; RELEASE_GATE attributes 654 to CBIND-117 | **CHANGED** | At T, LIMITATIONS.md says "records all 8,142", then lists Fully mapped 7,030, Partially mapped 15 and No C form 441 (sum 7,486). The word "planned" does not appear. `generate_limitations.py` `read_rows()` is unchanged (keeps only partial and not-applicable). COVERAGE.md line 15: 656 planned. RELEASE_GATE.md: "656 public symbols are still unmapped" and "441 unmapped in 86 groups". The release note (`release_gate.json` line 5 and RELEASE_GATE.md line 7) still says 654 under CBIND-117. In `plans/plan_binding.md`, CBIND-117 still owns 134 rows; the CBIND-117/120/121/122/125/127 rows are 134/3/1/5/5/320. | **title:** "468 planned" → "656 planned". **summary** → "The generated C API limitations document partitions 7,486 of the 8,142 declarations it counts and never mentions the 656 planned ones, and the release-gate note still says the Content Pipeline task owns 654 declarations where the plan records 134." (247 chars). **actual:** "records 9,355 declarations, then partitions Fully mapped 8,363, Partially mapped 15 and No C form 509: 8,887. The 468" → "records 8,142 declarations, then partitions Fully mapped 7,030, Partially mapped 15 and No C form 441: 7,486. The 656"; "“468 public symbols are still unmapped” (planned) and “509 unmapped in 83 groups”" → "“656 public symbols are still unmapped” (planned) and “441 unmapped in 86 groups”"; "and the planned backlog as 134 + 3 + 1 + 5 + 5 (CBIND-125) + 320 (CBIND-127) = 468;" → "and its open rows as 134 + 3 + 1 + 5 + 5 (CBIND-125) + 320 (CBIND-127) = 468, while COVERAGE.md now counts 656 planned rows;"; "now state the same 9,355." → "now state the same 8,142." **evidence:** "Not executed: the generators cannot run at this snapshot (CNA-BUG-062), so the arithmetic is taken from the committed documents." → "Not executed; the arithmetic is taken from the committed generated documents (COVERAGE.md snapshot: 469 headers, 8142 symbols, 7030 implemented, 15 partial, 656 planned, 441 not applicable)." This removes the reference to the retired BUG-062. |
| CNA-BUG-224 | CNA-BUG-224 | DeviceLost docs say only D3D9 reports loss | **EDIT** (Direct2D removed by 0f96ea703; the defect is unchanged) | GraphicsDevice.hpp lines 118 and 1931 and GraphicsDevice.cpp lines 4449 and 4914 are unchanged. `RendererDeviceEvent::Lost` is raised in DirectX9Renderer.cpp (Lost at lines 228, 784, 1699; Resetting 576; Reset 627), DirectX11Renderer.cpp, DirectX12Renderer.cpp, VulkanRenderer.cpp and WebGPURenderer.cpp. | **summary:** "five renderer families" → "four renderer families"; "a sixth, WebGPU" → "a fifth, WebGPU". **actual:** "by five families: `<code>DirectX</code>` 9, `<code>DirectX</code>` 11 (`<code>DirectX11Renderer::CheckDeviceRemoved</code>`), `<code>DirectX</code>` 12 (`<code>DirectX12Renderer::CheckDeviceRemovedEXT</code>`), `<code>Direct2D</code>` (`<code>Direct2DRenderer::RecreateDeviceResourcesForRecovery</code>`) and Vulkan" → same text with "four families" and without the Direct2D clause ("… 12 (`<code>DirectX12Renderer::CheckDeviceRemovedEXT</code>`) and Vulkan"); "raised around real recovery by `<code>DirectX</code>` 9 and `<code>Direct2D</code>`;" → "raised around real recovery by `<code>DirectX</code>` 9 only;". **evidence:** "The six raise sites" → "The five raise sites". **sources:** drop `modules/renderers/direct2d/src/Direct2DRenderer.cpp`; add `modules/renderers/directx9/src/DirectX9Renderer.cpp` — "DirectX9Renderer raises Lost, Resetting and Reset through deviceEventCallback_ around its real device-reset recovery". |
| CNA-BUG-274 | NEW-AUDIT-31 | README calls CNA_STRICT_XNA_API a CMake option | STILL VALID, conditional `related` fix | README.md line 51 still says "a dedicated CMake build option". `cmake/Harnesses.cmake` lines 191/232 only use `target_compile_definitions`. | `related.guide` links `docs/cnaext-engine.html` with label "CNAEXT engine layer". The engine layer is retired at T; if the site update renames or retargets that page, update the link or label (e.g. "CNAEXT graphics extensions"). |

#### (2) STILL VALID: what was checked at T

- BUG-025: PlaneIntersectionType.hpp lines 10/13 still say negative/positive half-space; all sources unchanged.
- BUG-045 (narrowed): THIRD_PARTY_NOTICES still has no cgltf, stb_image, ENet or dr_libs section. The only diff O..T swaps the avatar section. The vendored files and CGLTF_/STB_IMAGE_ implementation defines are present.
- BUG-057: XnbBuiltInReaders.hpp line 24 still says "known-unsupported placeholder".
- BUG-061: README line 34 and docs/coverage.md / xna-4-api-coverage.md still say 3,467/3,627 and 160 gaps; the generated report says 3627/3627, MISSING 0.
- BUG-215: IsLatched @brief and "Becomes true when the first GraphicsDevice begins construction" unchanged. Latch is only at GraphicsDevice.cpp line 4385, after successful resolution.
- BUG-216: MathTypeConverter.hpp line 99 comment unchanged; 6× `supportStringConvert = false` in Converters.cpp.
- BUG-217: framework-design.md line 61 "descriptor collections" unchanged.
- BUG-218: `cna_get_last_error_message` still at content_readers.h line 1139; the real accessors are the cna_error_* functions in core.h.
- BUG-220: CnaCApiRuntime.cpp line 936 and CnaCApiRuntimeDetail.hpp line 95 comments unchanged. Game::Dispose(bool) still never disposes GraphicsDevice_.
- BUG-221: ContentCompiler.hpp line 162 unchanged; content.cpp line 2733 still registers "whatever --format says".
- BUG-222: SoundEffect.hpp lines 269/279 "instance limit"; SoundEffect.cpp line 89 "freed in"; is3D_ comment line 108 "Never reset back to false"; setPanProperty still clears or throws (CABI-25); SoundEffectReader still uses ConvertXnbSoundToImportedSound.
- BUG-223: input-backend.md lines 50–55, 77 and 319 still describe the raw ProcessEvent and src/Input paths; SdlInputBridge.hpp has no ProcessEvent.
- BUG-225: EasyGLRendererDescriptor.cpp line 7 and RendererCombinations.cmake lines 14–15 vs line 72 unchanged.
- BUG-227: StubRenderer.hpp line 64 unchanged; ITextureRenderer::GetData defaults still return false.
- BUG-228: xnb.md line 41 "planning document only" and line 25 "nothing there is started".
- BUG-229 (narrowed): feature matrix line 230 vs lines 288 and 355–356 still contradict; plan_graphics Task 872 still ⬜; easygl examples CMakeLists line 1975 "documented known failure".
- BUG-230: SharedRuntimeLibrary.cmake line 145 comment unchanged; modules/CMakeLists.txt lines 361–362 and both module files still create the targets unconditionally.
- BUG-231: CHECKLIST.md line 61 vs CLAUDE.md line 20.
- BUG-232: "platform" absent from physical-modules.md; line 121 "holds exactly one thing"; xvfb demo still compiled; audio still links diagnostics and platform.
- BUG-234: CLAUDE.md line 643 "current baseline implements…" vs line 576.
- BUG-235: module table rows for input, media, content and phone unchanged vs their cna_link_sharp_runtime calls.
- BUG-237: Sdl3Platform.cpp line 643 and X11Platform.cpp line 1517 still name Game::UpdateInput().
- BUG-238: kOwnedWindowProperty is set and removed and never read; the comment at Win32Window.cpp line 117 is unchanged.
- BUG-239: win32-directx-spike comment and "Windows 10 1703" next to 0x0603 unchanged.
- BUG-240: X11Display.hpp line 109; X11Platform.hpp lines 49, 98 and 156–211 unchanged; only PolicyMutex exists.
- BUG-241: devices-event-contract.md line 211 and devices-thread-safety.md lines 39/71 unchanged.
- BUG-242: GetPreferencesPath doc "Backs StorageDevice" and the CApi_StorageSmoke comment unchanged; StorageDevice.cpp line 124 still resolves its root independently of the platform.
- BUG-243: gltf-limitations.md line 98 "CNA reverses it" vs ContentManager.cpp line 3591.
- BUG-244: README lines 591/623/629 unchanged; EndDraw still presents; Present has no per-frame guard.
- BUG-245: cnj.md line 220 and xnb.md line 406 unchanged; ContentManager.hpp lines 835–856 still call std::filesystem::exists.
- BUG-246: graphics-resource-lifetime.md line 16 still says `ITexture2DRenderer`; Texture2D, Texture3D and TextureCube still hold shared_ptr renderers.
- BUG-247: easygl-policy.json and report still say "137" next to 148/140/8; FUTURE.md line 30 still "137 … plus 8".
- BUG-248: PacketReader.hpp lines 85–87 and PacketWriter.hpp line 98, the test comment at line 144 and the demo Main.cpp lines 171–175 are unchanged. Only the C API net.h was corrected (c323ef242, BINDFIX-049).
- BUG-254: directx9-renderer.md line 192 "has not been started" vs plan_dx9.md line 956.
- BUG-256 (narrowed): model-content-pipeline-support.md lines 59/71; xna-4-api-coverage.md line 133 still lists the loader gaps.
- BUG-261: IGraphicsRenderer.hpp line 1796; D3D9ShaderDispatch.hpp lines 16–17; DirectX9Renderer.hpp lines 608/618; docs line 82 — vs D3D9EffectDraw.cpp line 951 and Fna3dDraw.cpp line 355, which read specularEnabled.
- BUG-271: known_bugs.md still "Status: OPEN" (line 11) and the line 47 entry; Vulkan_SpriteBatch_MultiBeginEnd still registered.
- BUG-272: cnj.md lines 593–595 "no JSON object type"; the native table still has no glTF; ContentManager.cpp line 4354 returns .cnj, .gltf and .glb.
- BUG-273: CLAUDE.md line 182 and AGENTS.md line 179 rule unchanged; still 51 ObjectDisposedException sites in modules/graphics/src.
- BUG-274: see the table above.

#### (3) New issues and side effects noticed

- **Stale "25 renderer identities"** in docs/c-api LIMITATIONS.md, COMPATIBILITY.md, compatibility_matrix.json and coverage_mappings.json at T (CNA has 18). Folded into the BUG-055 CHANGED text rather than a new entry.
- **CNA-GAP-062** (other batch) cites the retiring CNA-BUG-062 in `actual` and `tests_current`. It must be edited, and its planned-row figures (468) likely need the new value 656.
- **Hand-written site references to retiring entries:**
  - `docs/roadmap.html` lines 256 and 309, `docs/c-api.html` line 235 → BUG-062
  - `docs/native-platforms.html` lines 519–520 → BUG-233 / BUG-236
  - `docs/effects.html` line 662, `docs/tutorials/114-pbr-materials.html` line 351 → BUG-249
- **Low confidence, not recommended without a recount:** misc/FUTURE.md line 30 ("15 of 17 PBR renderers apply COLOR_0 … other 2 refuse") and misc/CNAEXT.md line 165 ("all 15 PBR renderers") probably still count the retired OPENGL4 and PORTABLEGL. FUTURE.md's row is labelled CURRENT. I did not establish the current PBR-renderer count.

#### patches-adversarial.json shape for this batch

All keys here equal the published ids, so plain `retired` and `entries.set` work with no renumbering.

```json
"retired": {
  "CNA-BUG-062": {"classification": "PROVEN FIXED", "evidence": "…5572f3ca1 MODULE_SCOPE…; COVERAGE.md exclusions; 8b55f7f4d CApi 113/116…"},
  "CNA-BUG-233": {"classification": "PROVEN FIXED", "evidence": "…76c9bda29 CLAUDE.md…"},
  "CNA-BUG-236": {"classification": "PROVEN FIXED", "evidence": "…76c9bda29 platform-abstraction.md table…"},
  "CNA-BUG-249": {"classification": "OBSOLETE", "evidence": "…5572f3ca1 historical banner; 261cb5f7f/0f96ea703…"}
},
"entries": {
  "CNA-BUG-055": {"set": {"title": "…", "summary": "…", "actual": "…", "evidence": "…", "blast_radius": "…", "sources": [ … ]}},
  "CNA-BUG-056": {"set": {"title": "…", "actual": "…", "evidence": "…", "blast_radius": "…"}},
  "CNA-BUG-058": {"set": {"title": "…", "summary": "…", "actual": "…", "evidence": "…"}},
  "CNA-BUG-224": {"set": {"summary": "…", "actual": "…", "evidence": "…", "sources": [ … ]}}
}
```

`set` replaces a whole field, so apply each substitution above to the full current value from issues-source.json before writing it. BUG-055, 056, 058 and 224 already have `entries` records in patches-adversarial.json (it holds 344), so merge into those records rather than adding new keys.


---

## Appendix TEST: Testing & evidence


I checked all 43 entries in batch-TEST at T=b0e97bb1 against O=009d40f5. 18 need action and 25 are still valid. Nothing in any repo was modified.

##### How these patches have to be expressed in patches-adversarial.json
- **Original ids** (stable key equals the published id) are retired through `"retired"` and edited through `"entries"`. That covers VGAP-017, 018, 040 and 042, and every other entry in this batch except the four NEW-AUDIT ones below.
- **NEW-AUDIT entries cannot go through `"entries"`.** The `"entries"` step runs before `"added"`, so `need()` would fail on them. CNA-VGAP-056 (NEW-AUDIT-05) and CNA-VGAP-059 (NEW-AUDIT-19) must be edited inside their element of the `"added"` list. The same applies to CNA-VGAP-057 and -058, which need no change.
- **Folded entries leak dead text and paths into their survivors.** VGAP-043→026, VGAP-045→023 and VGAP-048→025 each bring their `summary` (pasted into the survivor's `evidence`) and their `sources` (merged into the survivor's). Both must be fixed with `"entries": {"CNA-VGAP-04x": {"set": {"summary": …, "sources": […]}}}`. Those ids still exist when `"entries"` runs.

##### 1. Entries needing action

| published id | stable key | short title | disposition | evidence at T | proposed change |
|---|---|---|---|---|---|
| CNA-VGAP-017 | CNA-VGAP-017 | graphics-ext shader-package drift guards | RETIRE-OBSOLETE | 5572f3ca1 (MOD-RETIRE-1) deleted the shadow_caster, modern_resource_interop and clustered_forward packages and ClusteredForwardEffectTests.cpp. ModuleProbes.cmake at T keeps only ShaderPackageReproducibility (portable_tint) and PostProcessShaderPackageReproducibility (post_process). | Retire as OBSOLETE. The leftover point (no workflow installs shaderc, so both surviving checks skip with code 77) moves into VGAP-056, see below. |
| CNA-VGAP-018 | CNA-VGAP-018 | No test asserts RenderPipeline's post-process order | RETIRE-OBSOLETE | 5572f3ca1 removed RenderPipeline.cpp, RenderPipelineTests.cpp and PassTimingTests.cpp, i.e. the render pipeline itself. | Retire as OBSOLETE. |
| CNA-VGAP-042 | CNA-VGAP-042 | FREEDIRECT built and tested by no workflow | RETIRE-OBSOLETE | 0f96ea703 (RRC-012) removed modules/renderers/freedirect and docs/freedirect-renderer.md. FREEDIRECT=21 is in CNA_RENDERER_RETIRED_IDENTITIES. | Retire as OBSOLETE. |
| CNA-VGAP-040 | CNA-VGAP-040 | Avatar rendering evidence is a synthetic one-bone quad | RETIRE-FIXED | 3f4518e69 (GS-009b..d) added modules/gamer-services/examples/avatar_standard_render_test.cpp. It draws an avatar from the embedded CNA catalog through the standard AvatarRenderer into a 256×256 RenderTarget2D and reads pixels back (GetData). It checks shirt/trouser/skin colours, that an expression changes only the face, and that Wave raises the arm. It is registered as EasyGL_AvatarRenderer_Standard (easygl/examples/CMakeLists.txt) and Vulkan_AvatarRenderer_Standard. 13dfe0499 (GS-009f) retired the EnableRealRenderingEXT/DrawRealEXT surface named in the contract and deleted avatar_real_render_integration_test.cpp. | Retire as PROVEN FIXED. The EXT subject is also gone. |
| CNA-VGAP-041 | CNA-VGAP-041 | Strict-API purity check covers only the Devices sensor surface | NARROWED (status → narrowed) | 577fb0674 (BL-16) and 2c70eaf0f (BL-18) changed tools/devices/StrictXnaApiSurfaceCheck.cpp. It now includes ContentManager, CurveKeyCollection, GameComponentCollection, GameWindow and AnimationPlayer with -Wdeprecated-declarations silenced, which only checks where CNAEXT sits on `using` lines. It also compiles, but never runs, the SamplerStates[i] = state setter. The leak twin still includes only Accelerometer.hpp. | See text (a) below. |
| CNA-VGAP-021 | CNA-VGAP-021 | No SpriteFont pixel test for … | CHANGED | DIRECT2D, GDI, SVG_DOM, PORTABLEGL, OPENGL4, FREEDIRECT and HTML_DOM are retired (0f96ea703, 261cb5f7f). At T the directx11 and directx12 example trees also call cna_register_parity_fixtures, whose list (modules/graphics/examples/parity/ParityFixtures.cmake) includes sprite_font. No DrawString/SpriteFont registration exists for directx9, metal, canvas or fna3d. | See text (b) below. |
| CNA-VGAP-023 | CNA-VGAP-023 | Most browser renderer paths never executed automatically | CHANGED | 261cb5f7f removed htmldom-ci.yml, run-svgdom-browser-test.sh and run-htmldom-test-suite.sh. The emscripten-multi-renderer-ci.yml bundle is now WEBGL2+WEBGL1+CANVAS and its header says "does NOT run the bundle in a browser". No workflow mentions chrom*, playwright or puppeteer. The canvas examples are add_executable only. CanvasHostContracts sits behind the off-by-default CNA_BUILD_CANVAS_HOST_TESTS. | See text (c) below. CNA-VGAP-045's old claim "WEBGL1 is built by no workflow" is now false. |
| CNA-VGAP-026 | CNA-VGAP-026 | Windows renderer families have no automatic native run | CHANGED | d3d-windows-ci.yml at T: `on: workflow_dispatch` only, matrix [DIRECTX11, DIRECTX12]. gdi-windows-ci.yml, gdi/examples and docs/direct2d-release-gate.md were removed (0f96ea703, 261cb5f7f). platform-ci.yml: win32-cross runs only the platform harness; win32-native is dispatch-only. No workflow selects DIRECTX9. | See text (d) below. |
| CNA-VGAP-039 | CNA-VGAP-039 | Process-spawning net tests compiled out off POSIX | CHANGED | TwoProcessLoopbackTest.cpp at T has 8 TESTs, not 3 (added by GSX-E1, GS-007p, GS-007o, GSH-02). The WIN32/EMSCRIPTEN/ANDROID/iOS exclusion is unchanged (UnitTests.cmake). The ENetDiscoveryService.cpp comment still says Windows SO_REUSEADDR was "not independently verified". | `actual`: replace "holds three loopback cases: one host and one client exchanging app data, a rollback when discovery registration fails, and a three-process host migration in which one survivor is promoted and the other reconnects" with "holds eight loopback cases: one host and one client exchanging app data, voice both ways, two Find/Join cases, a client AddLocalGamer, SystemLink guests seen as guests on every machine, a rollback when discovery registration fails, and a three-process host migration in which one survivor is promoted and the other reconnects". |
| CNA-VGAP-044 | CNA-VGAP-044 | Wine and Proton routes don't prove which D3D/D2D implementation ran | CHANGED | direct2d/examples, run-wine-direct2d.sh, run-proton-direct2d.sh and direct2d-proton-pin.txt are absent at T (0f96ea703). Still true: UnitTests.cmake sets CROSSCOMPILING_EMULATOR with CNA_D3D9/11_SKIP_DXVK_GATE and CNA_D3D12_SKIP_VKD3D_GATE; run-proton-vkd3d.sh defaults to "Proton - Experimental" and `exec python3 "${PROTON_DIR}/proton" run`; there are still 3 DIRECTX12_PROTON fixtures. | See text (e) below. |
| CNA-VGAP-047 | CNA-VGAP-047 | Test strength never measured automatically | CHANGED | scripts/direct2d_mutation_check.py is gone and d3d-windows-ci.yml no longer mentions mutation (0f96ea703); no other mutation checker exists. docs/cnaext-coverage.md now carries a "Historical record" banner: it measured the removed engine layer (5572f3ca1). The fuzz harnesses and the cna_c_api_fuzz_targets OBJECT library are unchanged. | See text (f) below. |
| CNA-BUG-012 | CNA-BUG-012 | Two tests encode the wrong SDL_GPU occlusion expectation | EDIT | The defect is unchanged: the `default: return {true,true,true}` arm is still there. The sdlgpu limitation test is unchanged and still compares error.what() to the renderer's message, and the OcclusionQuery.cpp refusal is unchanged. Only the PortableGL arm was deleted (0f96ea703). | `actual`: replace "explicit arms only for OPENGLES2/WEBGL1, PORTABLEGL, FNA3D and SOFTWARE" with "explicit arms only for OPENGLES2/WEBGL1, FNA3D and SOFTWARE". |
| CNA-BUG-202 | CNA-BUG-202 | Multi-renderer example CTests run under the default renderer | EDIT | The guards are unchanged at T: sdl-gpu/stub/software/vulkan examples still guard only on `CNA_GRAPHICS_RENDERER STREQUAL …`, and modules/renderers/CMakeLists.txt still re-points the variable. OpenGL4 is gone (261cb5f7f). | `expected`: replace from "CNA already enforces this for three families: … crashed in a multi-renderer tree." with "CNA already enforces this for two families: the HEADLESS and EasyGL example blocks are entered only when that family is the build default (`_cna_default_renderer_identity`, VKPAR-0003)." `evidence`: delete the sentence " The GL4-0035 change records the analogous OpenGL4 failure: … and crashed." `sources`: remove modules/renderers/opengl4/examples/opengl4_smoke_test.cpp. |
| CNA-VGAP-022 | CNA-VGAP-022 | No test measures presentation cadence | EDIT | Registrations at T: easygl_present_interval_test in easygl, software, vulkan and DirectXParityTests; the swap-interval contract in easygl and DirectXParityTests. The VulkanRenderer.hpp `@param interval … 2 = half-rate` and the FIFO_RELAXED mapping are unchanged. | `actual`: "(also registered for VULKAN, SOFTWARE, OPENGL4 and, through" becomes "(also registered for VULKAN, SOFTWARE and, through"; "(also registered for DIRECTX11/12 and OPENGL4)" becomes "(also registered for DIRECTX11/12)". |
| CNA-VGAP-025 | CNA-VGAP-025 | No CI workflow selects WEBGPU or SDL_GPU | EDIT | Still no WEBGPU, SDL_GPU, OPENGLES2, FNA3D or DIRECTX9 in .github/workflows. Parity fixtures are registered by directx11, directx12, easygl, sdl-gpu and webgpu. opengl4 is gone (261cb5f7f). | `actual`: replace the 2nd paragraph with "<p>The same search finds no workflow that selects OPENGLES2 or FNA3D either, so the parity fixtures that the WEBGPU and SDL_GPU example trees register through <code>cna_register_parity_fixtures</code> are local evidence; the browser renderers (CNA-VGAP-023), the Windows identities (CNA-VGAP-026) and the recorded glTF golden sets (CNA-VGAP-030) have entries of their own.</p>" This drops the references to the retired CNA-VGAP-010 and -042. `sources`: remove modules/renderers/opengl4/examples/CMakeLists.txt. Folded **CNA-VGAP-048**: set `summary` to "Only the OPENGLES3 whole-corpus L7 rung runs in CI; WEBGPU, SDL_GPU, OPENGLES2, FNA3D and DIRECTX9 are selected by no workflow at all (WEBGL1 is only linked into a bundle that is never run), so their registered parity fixtures are local evidence." and set its `sources` to gltf-renderer-stride-ci.yml, webgpu/examples/CMakeLists.txt and sdl-gpu/examples/CMakeLists.txt (no opengl4). |
| CNA-VGAP-030 | CNA-VGAP-030 | Model drawing in CI only at the stride boundary | EDIT | The easygl_model_* programs are registered in software, vulkan, sdl-gpu (SdlGpu_EasyGLOracle_model_*) and DirectXParityTests. The L7 reports at T are still captured 2026-08-18 at b6c180fd; only corpusManifestSha256 changed. platform-ci still filters ctest. | `summary`: "SOFTWARE, VULKAN, SDL_GPU, OPENGL4 and the DirectX parity set" becomes "SOFTWARE, VULKAN, SDL_GPU and the DirectX parity set". `actual`: ", {{src:modules/renderers/opengl4/examples/EasyGLParityCorpus.cmake\|EasyGLParityCorpus.cmake}} and {{src:cmake/DirectXParityTests.cmake\|DirectXParityTests.cmake}}" becomes " and {{src:cmake/DirectXParityTests.cmake\|DirectXParityTests.cmake}}". That `{{src:}}` token currently points at a dead path. |
| CNA-VGAP-056 | NEW-AUDIT-05 (edit inside `added`) | Shader bytecode headers have no `--check` | EDIT | The generators are unchanged: only `--output`, no CTest or workflow, shadow_sampling.glsl still shared. Its tests_current cites CNA-VGAP-017, which is being retired. Its `related` links point at the removed engine layer. No workflow installs shaderc. | `tests_current`: replace "the graphics-ext shader packages are guarded separately (CNA-VGAP-017)." with "the two remaining shader-package reproducibility CTests (<code>ShaderPackageReproducibility</code> for the portable_tint example package and <code>PostProcessShaderPackageReproducibility</code> for the retained post_process package) exit 77 and skip wherever libshaderc is absent, which includes every CI workflow: none installs shaderc." `related`: drop `development/internals/modules/graphics-ext.html#shaders-clustered` and `docs/cnaext-engine.html#evidence` (engine-layer pages), or repoint them to whatever pages replace them. |
| CNA-VGAP-059 | NEW-AUDIT-19 (edit inside `added`) | VibrateController shutdown-ordering tests | EDIT | 76c9bda29 removed CNA_SDL2_ONLY_CONFIGURATION from the exclusion. At T: `if(WIN32 OR EMSCRIPTEN OR ANDROID OR CNA_APPLE_IOS)`. SDLCORE-011 is still OPEN in plan_devices.md, and ~Sdl3Platform still calls haptics_.Deactivate(). | `actual`: "excluded on Windows, Emscripten, Android, <code>iOS</code> and SDL2-only builds." becomes "excluded on Windows, Emscripten, Android and <code>iOS</code>." `tests_current`: "excluded on Windows, Emscripten, Android, iOS and SDL2-only builds." becomes "excluded on Windows, Emscripten, Android and iOS." |

**Replacement text for the CHANGED and NARROWED entries**

(a) **CNA-VGAP-041** (status `narrowed`)
- `title`: "The CNA_STRICT_XNA_API purity check calls only the Microsoft::Devices sensor surface and one SamplerStateCollection indexer"
- `summary`: "cna_strict_xna_api_check calls only Devices/Sensors members and one SamplerStateCollection indexer, and its must-fail twin includes only Accelerometer.hpp, so no automated check covers strict-mode purity or marker completeness of the other XNA surfaces." (253 characters)
- `actual`:
  - Replace "which includes VibrateController and the Sensors headers (plus three math value types) and calls only their members." with "which includes VibrateController and the Sensors headers (plus three math value types) and calls their members; since BL-16 and BL-18 it also parses ContentManager.hpp, CurveKeyCollection.hpp, GameComponentCollection.hpp, GameWindow.hpp and AnimationPlayer.hpp with deprecation warnings silenced (a check of CNAEXT placement on using lines, not of purity) and compiles, without calling, one use of XNA's <code>SamplerStates[i] = state</code> indexer setter."
  - Replace "No test compiles graphics, content, input, audio, media or runtime calls under the strict macro" with "Apart from that indexer, no test compiles graphics, content, input, audio, media or runtime calls under the strict macro".
- `tests_current`: replace "both Microsoft::Devices only" with "Microsoft::Devices calls plus the SamplerStates indexer setter; the twin is Accelerometer only".

(b) **CNA-VGAP-021**
- `title`: "No SpriteFont/DrawString pixel test exists for DIRECTX9, METAL, CANVAS or FNA3D"
- `summary`: "SpriteFont/DrawString reach pixels in registered tests on EasyGL, SOFTWARE, SDL_RENDERER, VULKAN, SDL_GPU, WEBGPU and DIRECTX11/12 (the shared sprite_font parity fixture and the DirectX SpriteFont fixtures); four families have no text pixel test."
- `actual`: "<p>A count of <code>SpriteFont</code>/<code>DrawString</code> registrations in each renderer's <code>examples/CMakeLists.txt</code> and in the shared corpora finds them for <code>EasyGL</code>, SOFTWARE, <code>SDL_RENDERER</code> and VULKAN, plus the DIRECTX11/12 fixtures in {{src:cmake/DirectXParityTests.cmake\|DirectXParityTests.cmake}}. The shared parity fixture <code>sprite_font</code> (WEBGPU-179) in {{src:modules/graphics/examples/parity/ParityFixtures.cmake\|ParityFixtures.cmake}} is registered by <code>cna_register_parity_fixtures</code> for <code>SDL_GPU</code>, WEBGPU, <code>EasyGL</code>, DIRECTX11 and DIRECTX12. None is registered for DIRECTX9, METAL, CANVAS or FNA3D; HEADLESS and STUB rasterise nothing.</p>"
- `sources`: replace the opengl4 path with `modules/graphics/examples/parity/ParityFixtures.cmake`, note "sprite_font in the shared parity list".
- `evidence`: "The blast radius is text output on the eight listed renderers" becomes "the four listed renderers".

(c) **CNA-VGAP-023**
- `title`: "No browser renderer path is executed automatically: WEBGL1/WEBGL2 have no test registrations and CANVAS has no registered browser run"
- `summary`: "WebGL identities have no test registrations and CI only links a WEBGL2+WEBGL1+CANVAS bundle without running it, CANVAS test programs are not registered, and CanvasHostContracts is opt-in with no workflow; no workflow runs any renderer in a browser."
- `public_contract`: "WEBGL1, WEBGL2 and CANVAS renderer identities (and the CANVAS host contracts)"
- `actual`: keep the easygl and canvas sentences, then: "{{src:modules/renderers/CMakeLists.txt\|CMakeLists.txt}} gates CanvasHostContracts behind the off-by-default CNA_BUILD_CANVAS_HOST_TESTS option, which no workflow sets. {{src:.github/workflows/emscripten-multi-renderer-ci.yml\|emscripten-multi-renderer-ci.yml}} links WEBGL2, WEBGL1 and CANVAS into one bundle and, per its header, does not run it in a browser; no workflow drives a browser."
- `sources`: drop the three missing paths.
- `tests_current`: "Build only: one Emscripten bundle linked, never run; any browser runs are manual."
- `regression_test`: "A headless-browser CI step per identity and a CI configuration that enables CNA_BUILD_CANVAS_HOST_TESTS."
- `blast_radius`: "All WebGL and Canvas rendering, context loss and host-owned loop behaviour."
- Folded **CNA-VGAP-045**: set `summary` to "No workflow runs a renderer in a browser: CANVAS, WEBGL1 and WEBGL2 have no browser harness, and the Emscripten multi-renderer job only links a WEBGL2+WEBGL1+CANVAS bundle." and set its `sources` to just .github/workflows/emscripten-multi-renderer-ci.yml.
- `related`: deep-dives/renderers/browser-dom-renderers.html is about the retired DOM renderers; drop it or repoint it.

(d) **CNA-VGAP-026**
- `title`: "The Windows renderer families have no automatic native Windows execution: DIRECTX9 has no CI job and the DIRECTX11/12 lane is manual"
- `summary`: "The Direct3D Windows workflow (DIRECTX11 and DIRECTX12) runs only on manual dispatch, no workflow selects DIRECTX9, the automatic win32-cross job runs only the platform harness, and DXGI device removal is only simulated."
- `public_contract`: "DIRECTX9, DIRECTX11 and DIRECTX12 renderer identities on native Windows"
- `actual`: "<p>{{src:.github/workflows/d3d-windows-ci.yml\|d3d-windows-ci.yml}} (matrix DIRECTX11, DIRECTX12) triggers only on <code>workflow_dispatch</code>; no workflow selects DIRECTX9. {{src:.github/workflows/platform-ci.yml\|platform-ci.yml}}'s automatic win32-cross job builds and runs only the standalone Win32 platform harness under Wine, and its win32-native job is manual. Device removal on the DXGI renderers is exercised only through debug simulation hooks. The Wine/DXVK/vkd3d cross-build lanes are local evidence, not native Windows.</p>"
- `sources`: d3d-windows-ci.yml and platform-ci.yml only.
- `regression_test`: "Push or scheduled triggers for the Windows lane and a DIRECTX9 job."
- `related`: drop deep-dives/renderers/windows-2d-renderers.html#d2d-tests.
- Folded **CNA-VGAP-043**: set `summary` to "The automatic win32-cross job builds and runs only the standalone Win32 platform harness under Wine; every engine-level Windows workflow is manual." and set its `sources` to platform-ci.yml and d3d-windows-ci.yml.

(e) **CNA-VGAP-044**
- `title`: "Wine test routes and the DIRECTX12 Proton route do not prove which Direct3D implementation served a run"
- `summary`: "CnaTests' Wine emulator skips the DXVK/vkd3d-proton engagement gate for every discovered case, and the DIRECTX12 Proton route uses a moving Proton build with no pin, identity record or log gate."
- `public_contract`: "CTest routes for DIRECTX9, DIRECTX11 and DIRECTX12 in MinGW cross trees"
- `expected`: "Direct3D or Direct2D" becomes "Direct3D".
- `actual`: keep the first sentence. Delete "In the Wine-runtime branch … d2d1 marker." Keep the run-proton-vkd3d.sh sentence. Replace the "By contrast …" sentence with "Nothing in the tree pins the Proton build or records which one served a run."
- `sources`: drop direct2d/examples/CMakeLists.txt and scripts/run-wine-direct2d.sh.
- `evidence`: drop the d2d1 clauses and "the Direct2D Proton wrapper's pin and identity record already model".
- `tests_current`: "CnaTests cases and the Proton fixtures do not."
- `regression_test`: drop "add a d2d1 engagement marker to the Direct2D wrapper".
- `blast_radius`: "How much Direct3D evidence obtained under Wine or Proton can be trusted; native Windows runs are unaffected."

(f) **CNA-VGAP-047**
- `title`: "Test strength is never measured automatically: no coverage build, no scheduled fuzzing campaign and no mutation checking"
- `summary`: "No workflow or CMake option enables coverage instrumentation, the libFuzzer-capable harnesses are not CTests and no job or schedule runs them (their recorded campaigns were manual, one-time runs), and no mutation checker exists."
- `actual`:
  - Replace "{{src:docs/cnaext-coverage.md\|cnaext-coverage.md}} records one --coverage build of 2026-08-18, for the graphics-ext layer only." with "the only recorded --coverage build, {{src:docs/cnaext-coverage.md\|cnaext-coverage.md}} (2026-08-18), measured the graphics engine layer that has since been removed, and the document is marked historical."
  - Replace the final d3d-windows-ci / direct2d_mutation_check sentence with "No mutation-testing tool exists in the tree."
- `sources`: drop scripts/direct2d_mutation_check.py and .github/workflows/d3d-windows-ci.yml.
- `regression_test`: "a scheduled --run of the mutation checker" becomes "a mutation-testing pass".

##### 2. STILL VALID (25 entries; cited code re-read at T)
- CNA-BUG-036: `cmake --build "${dir}" -j4 -- -k` at run-all-renderer-smoke-tests.sh lines 86 and 155; multi-renderer preset binaryDir is cmake-build-multi.
- CNA-BUG-201: StorageDeviceTests.cpp unchanged. EnsureStorageRoot still reads XDG_DATA_HOME/LOCALAPPDATA; the CBIND-151/SAMPLE-070 changes only add an Emscripten branch and move the init flag. UnitTests.cmake sets no storage env.
- CNA-BUG-203: CNA_SDLGPU_TEST_VIDEO_DRIVER still defaults to x11; non-Windows HEADLESS env equals the test env; SdlGpu_2D_HeadlessDriver still appends FORCE_HEADLESS=1; the refusal text is still at SdlGpuRenderer.cpp:2407.
- CNA-BUG-204: ExpectedGlslEffectValidity is unchanged in CnjEffectTests and CnjStockEffectTests; SDL_GPU still returns ShaderDialectEXT::SpirV.
- CNA-BUG-205: the test still catches `std::runtime_error` and asserts `!ClearThrows(Stencil)`. GraphicsDevice::Clear still throws System::InvalidOperationException for a missing depth or stencil.
- CNA-BUG-206: run-oracle-corpus-diff-software.sh and the Software CMakeLists are unchanged.
- CNA-VGAP-016: tests preset description unchanged; cna_cue_test fixed fixture names remain; general-tests-ci still runs a plain `ctest --output-on-failure`.
- CNA-VGAP-019: check_module_link_closure.py unchanged; all ModuleLinkClosure_* tests (CnaExtComposition, NetHasENet and the rest) still get SKIP_RETURN_CODE 77; no workflow changed generator.
- CNA-VGAP-020: CnaPlatformTests filter still has `TerminalPresenter.*`; none of the eight named suites appears in UnitTests.cmake.
- CNA-VGAP-024: Metal examples still register only PortableHelpers/Smoke/Capabilities; metal_spritebatch_customeffect_test.cpp is still unregistered; metal-macos-ci.yml unchanged.
- CNA-VGAP-027: sdl-renderer examples, input-ci.yml and apple-ci.yml unchanged.
- CNA-VGAP-028: no changes under tests/assets/xnb or tests/reference; only the pipeline test XnaXmlSourceRouteTests uses xml_framework_curve.
- CNA-VGAP-029: ReadTextFile is still a whole-file ifstream with no limit; no .cnj or JSON fuzz target. Json.hpp is unchanged, so CNA-BUG-016 still stands.
- CNA-VGAP-031: plan_gltf.md row 12 still reads "3 of 4" (the CNASTREET-SKINDRAW edits are elsewhere in the file).
- CNA-VGAP-032, -033, -034, -036: all sources unchanged.
- CNA-VGAP-035: every named DynamicSoundEffectInstance in the tests is still 44,100 Hz; other rates appear only in constructor-range checks after KF-12. Update still uses GetMixerStreamQueuedBytes.
- CNA-VGAP-037: `option(CNA_DEVICES … OFF)`; devices-ext tests unchanged.
- CNA-VGAP-038: storage tests and StorageSmoke.c unchanged; CNA_BUILD_C_API is OFF in the presets and absent from workflows.
- CNA-VGAP-046: D3D9_XNA_Diff still registered; no Pillow in general-tests-ci; cna_reference_dump still has no add_test.
- CNA-VGAP-049: all 3,627 rows still `behavior_assessed: false`; census numbers identical (GS-011b's edit didn't change them); no workflow runs audit_xna_runtime_surface.py.
- CNA-VGAP-057: migration-guide.md:119 still lists Task 933 as open; plan_graphics row 933 still "remains open".
- CNA-VGAP-058: DestroyMixer has no caller in src; g_audioDevice static unchanged; AUD-15-016 still unchecked.

##### 3. New issues and notes at T
- **CNA-VGAP-024 cites a dangling id.** It refers to CNA-VGAP-050, which the adversarial audit folded into CNA-GAP-013. This predates the pin change.
- **No browser CI at all.** With htmldom-ci.yml removed, no workflow runs any renderer in a browser. This is captured in the CNA-VGAP-023 rewrite.
- **Both surviving shader-package checks skip in CI.** No workflow installs shaderc, so both reproducibility CTests always skip there. This is captured in the CNA-VGAP-056 edit.
- **Dates in evidence text.** Every edited entry's `evidence` says "at 009d40f5"; that wording has to move to the new pin for all entries.

##### 4. Counts (43 entries)
| Disposition | Count | Entries |
|---|---|---|
| RETIRE-OBSOLETE | 3 | VGAP-017, VGAP-018, VGAP-042 |
| RETIRE-FIXED | 1 | VGAP-040 |
| NARROWED | 1 | VGAP-041 |
| CHANGED | 6 | VGAP-021, 023, 026, 039, 044, 047 |
| EDIT | 7 | BUG-012, BUG-202, VGAP-022, 025, 030, 056, 059 |
| STILL VALID | 25 | listed in section 2 |

Another fork overwrote the shared helper `r9work/show.py` while I was working. My own helper is in `r9work/test-fork/`, and I wrote nothing else.


---

## Appendix BUILD: Build & CI + Platforms


Task: decide each batch-BUILD.txt entry's disposition at T=b0e97bb1 (45 entries: Build & CI and Platforms). The repos were only read; I wrote no files.

#### (1) Entries that need action

Field substitutions are written as `field: 'old verbatim' -> 'new'` against issues-source.json.

| published id | stable key | short title | disposition | evidence at T | proposed change |
|---|---|---|---|---|---|
| CNA-BUG-178 | CNA-BUG-178 | SDL2 negates flipped wheel, SDL3 does not | RETIRE (OBSOLETE) | 76c9bda29 deleted modules/platform/src/Sdl2/* (Sdl2Platform.cpp etc.). SDL3 is now the only SDL backend, so the two backends can no longer disagree. 6ee00e35d adds CnaPlatformSelection_SDL2 and PlatformFactoryTests.RetiredSdl2ImplementationIsNeitherAdvertisedNorCreatable. | retire |
| CNA-BUG-189 | CNA-BUG-189 | GDI configure message "3 GDI-owned units" | RETIRE (OBSOLETE) | 261cb5f7f (RRC-015) deleted modules/renderers/gdi/ (CMakeLists.txt, GdiRendererDescriptor.cpp). GDI=40 is in CNA_RENDERER_RETIRED_IDENTITIES. | retire |
| CNA-BUG-194 | CNA-BUG-194 | SDL2-only guard recommends VULKAN | RETIRE (OBSOLETE) | 76c9bda29 deleted cmake/Sdl2OnlyConfiguration.cmake, cmake/Tests/Sdl2OnlyRendererGate.cmake and Sdl2Platform.cpp. | retire |
| CNA-BUG-195 | CNA-BUG-195 | SDL2-only guard ignores CNA_GRAPHICS_RENDERERS | RETIRE (OBSOLETE) | 76c9bda29, as for BUG-194. SdlAvailability.cmake no longer has any SDL2 branch. | retire |
| CNA-BUG-200 | CNA-BUG-200 | Registered CTest CNAEXT_NoPosixSetenv is red | RETIRE (OBSOLETE) | 5572f3ca1 (MOD-RETIRE-1) deleted the `add_test(NAME CNAEXT_NoPosixSetenv ...)` block from modules/graphics-ext/examples/CMakeLists.txt. `git grep NoPosixSetenv\|check_no_posix_setenv` at T finds no CMake registration (only plan text, one test comment and the script itself). The registered red gate no longer exists. See NEW-1 for what this leaves behind. | retire |
| CNA-VGAP-010 | CNA-VGAP-010 | No CI builds or tests OPENGL4 | RETIRE (OBSOLETE) | 261cb5f7f removed modules/renderers/opengl4, docs/opengl4-renderer.md and plans/plan_opengl4_modern_graphics.md. OPENGL4=33 is retired. | retire |
| CNA-VGAP-009 | CNA-VGAP-009 | GDM iOS/Android orientation branch has no test | RETIRE (PROVEN FIXED) | 80572aa00 (CBIND-138) added modules/runtime/tests/Microsoft/Xna/Framework/GraphicsDeviceManagerOrientationTests.cpp. A PlatformTestDecorator reports GetPlatformName()=="Android" and drives GraphicsDeviceManager::ApplyChanges. It asserts the PresentationParameters orientation and size for three cases: Default 480x800 gives Portrait 480x800 (ADefaultPortraitGameGetsAPortraitBackBuffer); Default 853x480 gives LandscapeLeft (ADefaultLandscapeGameKeepsItsLandscapeBackBuffer); Portrait with an 800x480 preference is swapped to 480x800 (AnExplicitPortraitSetSwapsALandscapePreference). Forwarding to the platform window is covered by GameWindowTests SetSupportedOrientations_ForwardsTheRequestedSetToThePlatformWindow. The suite skips where the build's platform cannot create a window. | retire |
| CNA-VGAP-011 | CNA-VGAP-011 | PlatformSelection refusal paths untested | NARROWED | 6ee00e35d adds CTest CnaPlatformSelection_SDL2 (cmake/Tests/RetiredSdl2PlatformSelection.cmake). It runs PlatformSelection.cmake in script mode with CNA_PLATFORM=SDL2 and asserts "is not a known platform", so the unknown-name branch is now covered. The reserved branch (SDL12, EMSCRIPTEN, WIN32 off Windows, TERMINAL on Windows) is still untested. cmake/Tests/Sdl2OnlyRendererGate.cmake was deleted by 76c9bda29. | status→"narrowed"; title→"No test exercises PlatformSelection.cmake's reserved-identifier refusal paths"; summary→"PlatformSelection.cmake fails configure for SDL12, EMSCRIPTEN, WIN32 off Windows and TERMINAL on Windows, but no test asserts those refusals; the only platform-selection configure tests cover Wayland and the retired SDL2 value (an unknown name)."; public_contract→"cmake/PlatformSelection.cmake configure-time refusals for reserved CNA_PLATFORM values"; actual: after 'changes no default.' insert ' Since 6ee00e35d, <code>CnaPlatformSelection_SDL2</code> ({{src:cmake/Tests/RetiredSdl2PlatformSelection.cmake\|RetiredSdl2PlatformSelection.cmake}}) runs the selection file in script mode with <code>CNA_PLATFORM=SDL2</code> and asserts the unknown-name refusal.'; actual: ', <code>TERMINAL</code> on Windows, or an unknown name and asserts the <code>FATAL_ERROR</code>.' -> ' or <code>TERMINAL</code> on Windows and asserts the reserved-identifier <code>FATAL_ERROR</code>.'; actual: 'The <code>Sdl2OnlyRendererGate</code>, <code>RendererDefaultCase</code> and <code>RendererRetiredIdentityCase</code> tests cover renderer selection, not the four platform refusal branches.' -> 'The <code>RendererDefaultCase</code> and <code>RendererRetiredIdentityCase</code> tests cover renderer selection, not the reserved-identifier platform branch.'; tests_current: '(Wayland only), and the renderer-selection fixtures. None configures a reserved or unknown' -> '(Wayland only), <code>CnaPlatformSelection_SDL2</code> (unknown-name refusal via the retired SDL2 value) and the renderer-selection fixtures. None configures a reserved'; regression_test: 'each reserved value, an unknown value, and a host-wrong value' -> 'each reserved value and a host-wrong value'; sources: add {path: cmake/Tests/RetiredSdl2PlatformSelection.cmake, note: "CnaPlatformSelection_SDL2: covers only the unknown-name refusal"}; UnitTests.cmake note -> "CnaWaylandPlatformSelection and CnaPlatformSelection_SDL2 are the only platform-selection configure tests" |
| CNA-BUG-035 | CNA-BUG-035 | devices-tests.yml filters skip suites | CHANGED (counts) | INPUT-EMU-001 (31a560af9) added modules/devices/tests/Microsoft/Devices/Sensors/KeyboardAccelerometerTests.cpp (KeyboardAccelerometerTest, 4 TEST_F), which DEVICES_GTEST_FILTER does not name. TEST/TEST_F definitions went from 474 at O to 478 at T. Workflow and fixtures are otherwise unchanged. | title: 'skip seven Microsoft::Devices suites' -> 'skip eight Microsoft::Devices suites'; summary: 'misses 29 of 474 TEST definitions' -> 'misses 33 of 478 TEST definitions'; actual: 'selects 445 of the 474 definitions' -> 'selects 445 of the 478 definitions'; actual: 'Seven suites are missing:' -> 'Eight suites are missing:'; actual: insert '<code>KeyboardAccelerometerTest</code> (4, added by INPUT-EMU-001), ' before '<code>NativeDia'; evidence (merged paragraph): '445 of the 474 TEST definitions' -> '445 of the 478 TEST definitions'; tests_current: 'the seven <code>Microsoft::Devices</code> suites' -> 'the eight <code>Microsoft::Devices</code> suites'; source notes: 'one of the seven unfiltered suites' -> 'one of the eight unfiltered suites' (2 notes) |
| CNA-BUG-190 | CNA-BUG-190 (survivor of fold CNA-BUG-187) | Pre-loop helper dirs keyed to default identity | CHANGED (GDI half gone) | 261cb5f7f removed the `if(CNA_GRAPHICS_RENDERER STREQUAL "GDI") add_subdirectory(software)` block from modules/renderers/CMakeLists.txt. 590ac27c8 removed the software GDI branch. RendererCombinations.cmake lost its PORTABLEGL and GDI rules (0f96ea703, 261cb5f7f). The common/d3d condition (`if(CNA_GRAPHICS_RENDERER STREQUAL "DIRECTX11" OR ... "DIRECTX12")`) and metal (`if(CNA_GRAPHICS_RENDERER STREQUAL "METAL")` in metal/CMakeLists.txt) are unchanged. The Windows partition is now DIRECTX9 DIRECTX11 DIRECTX12. | title -> "modules/renderers/CMakeLists.txt enters common/d3d and the Metal renderer target only when the default identity matches, so a multi-renderer set that lists DIRECTX11, DIRECTX12 or METAL without the matching default passes the combination rules and then cannot build"; summary: 'Three helper directories' -> 'Two helper directories'; actual: 'makes three decisions' -> 'makes two decisions'; actual: '(HEADLESS, DIRECTX9, GDI, ...)' -> '(HEADLESS, DIRECTX9, ...)'; actual: delete the whole `<li>software is entered for GDI only when GDI is the default; ... an undefined header target.</li>`; actual: 'refuses only PORTABLEGL with a real-GL renderer, GDI with SOFTWARE, and pairs from two different platform partitions' -> 'refuses only pairs from two different platform partitions'; actual: 'avoid all three conditions' -> 'avoid both conditions'; actual: '(for example DIRECTX11;DIRECTX12, or DIRECTX9;DIRECT2D)' -> '(for example DIRECTX11;DIRECTX12)'; regression_test: 'for the three helpers' -> 'for the two helpers'; blast_radius: 'DIRECTX11, DIRECTX12, GDI or METAL' -> 'DIRECTX11, DIRECTX12 or METAL'; sources: drop modules/renderers/gdi/CMakeLists.txt and modules/renderers/software/CMakeLists.txt; first note -> "the pre-loop add_subdirectory conditions for metal and common/d3d, and the family loop". **Also patch folded CNA-BUG-187** in "entries", because the fold runs after "entries" and re-appends its summary into BUG-190's evidence plus its missing sources: summary -> "Before its per-family loop the file adds common/d3d only when the default renderer is DIRECTX11 or DIRECTX12, so a Windows multi-renderer build with DIRECTX11 or DIRECTX12 as a non-default member lacks the target it links."; sources = BUG-187's list minus gdi/CMakeLists.txt and software/CMakeLists.txt |
| CNA-BUG-192 | CNA-BUG-192 | metal-macos-ci push filter names dead files | CHANGED (count) | The three cmake files are still absent and the filter is unchanged. Workflows went from 20 to 18 (gdi-windows-ci.yml and htmldom-ci.yml deleted by 261cb5f7f). A scan finds no other dead workflow path filters and no workflow names a removed renderer, SDL2 or graphics-ext. | actual: 'any of the 20 workflow files' -> 'any of the 18 workflow files' |
| CNA-BUG-199 | CNA-BUG-199 | CI workflows pin old sharp-runtime | CHANGED (6 -> 5 workflows) | htmldom-ci.yml and gdi-windows-ci.yml deleted (261cb5f7f). Pins at T: devices-tests.yml and emscripten-multi-renderer-ci.yml at bc8dbf41; apple-ci.yml (2 jobs) and metal-macos-ci.yml at f23ded28; content-pipeline-windows-ci.yml at df1b42ab. The default closure still adds Resources and, off Windows, Xml.Serialization; the root CMakeLists still merges it. The emscripten bundle is now WEBGL2;WEBGL1;CANVAS. | title: 'Six CI workflows' -> 'Five CI workflows'; summary: 'The five non-Windows lanes' -> 'The four non-Windows lanes'; public_contract -> "devices-tests.yml, emscripten-multi-renderer-ci.yml, apple-ci.yml, metal-macos-ci.yml and content-pipeline-windows-ci.yml; SHARP_RUNTIME_COMPONENTS"; actual: '{{src:.github/workflows/htmldom-ci.yml\|htmldom-ci.yml}}, {{src:.github/workflows/devices-tests.yml\|devices-tests.yml}} and' -> '{{src:.github/workflows/devices-tests.yml\|devices-tests.yml}} and'; actual: 'and {{src:.github/workflows/gdi-windows-ci.yml\|gdi-windows-ci.yml}} (manual dispatch only) check out' -> '(manual dispatch only) checks out'; actual: 'Apart from the six pins' -> 'Apart from the five pins'; regression_test: 'bumping the six refs' -> 'bumping the five refs'; blast_radius: 'the HTML_DOM browser suite, the Microsoft::Devices suites' -> 'the Microsoft::Devices suites'; blast_radius: 'the two manual-dispatch Windows lanes that check out sharp-runtime's default branch depend' -> 'the manual-dispatch Windows D3D lane that checks out sharp-runtime's default branch depends'; evidence: 'when the two manual Windows lanes would be dispatched' -> 'when the manual Windows lane would be dispatched'; sources: drop .github/workflows/htmldom-ci.yml; related: re-check guide link docs/tutorials/105-browser-renderers.html if that tutorial is retired |
| CNA-PLAT-014 | CNA-PLAT-014 | Compass/Motion Android-only; no browser sensors | CHANGED | 31a560af9 (INPUT-EMU-001) adds Accelerometer::set/getKeyboardEmulationEnabledEXT. getIsSupportedProperty now returns true first when emulation is on, on any target including the browser (CNA::Platform::KeyboardAccelerometer, platform-independent). Compass.cpp, Motion.cpp and the other sensors are unchanged. | summary -> "Compass::IsSupported and Motion::IsSupported are false everywhere except Android, as SDL3 exposes no magnetometer or fused-orientation API; Accelerometer and Gyroscope read real sensors on Android, iOS and desktop, never in a browser."; actual: append '<p>Since INPUT-EMU-001 (31a560af9) <code>Accelerometer</code> has an opt-in keyboard emulation (<code>setKeyboardEmulationEnabledEXT</code>): while it is on, <code>IsSupported</code> is true on every target, browser included, but readings come from the keyboard, not a sensor.</p>' |
| CNA-VGAP-008 | CNA-VGAP-008 | Android/iOS have no device evidence | CHANGED | Still no Android workflow or preset (`git grep -il android` matches only devices-tests.yml, host suites). apple-ci.yml and apple_smoke.cpp are unchanged. New, non-CI, manual Android-emulator records exist in commit messages: BL-19 5d275f556 (2026-09-29, House APK loads all .cnb from the APK), BL-21 016c588bf (2026-09-29, activate and deactivate across Home), CBIND-139 1dc4ce06a (2026-10-01). ContentManager now resolves a relative root under TitleLocation's path (CBIND-140 9976f4909, ContentRoot.cpp ResolveContentRoot). | actual: '<p>No workflow or preset targets Android; {{src:docs/devices-build.md\|devices-build.md}} records the APK and emulator runs of July 2026, with no retained artifacts.' -> '<p>No workflow or preset targets Android. Besides the July 2026 APK and emulator runs in {{src:docs/devices-build.md\|devices-build.md}}, CNA's commit records describe manual Android-emulator runs with the House Simulator APK on 2026-09-29 and 2026-10-01 (BL-19: .cnb content loaded from the APK; BL-21: activation across Home and return; CBIND-139: models drawn whole), at revisions before b0e97bb1 and with no retained artifacts.'; actual: "which ContentManager does not consult (CNA-BUG-041).</p>" -> "which ContentManager consults for a relative root since CBIND-140 (9976f4909); no device or simulator run loads content through it.</p>"; evidence: the 'packaged-content half is the defect CNA-BUG-041' sentences need syncing with whatever the MEDIA batch decides for BUG-041 |
| CNA-BUG-177 | CNA-BUG-177 | Headless/Terminal ctor accepts BorderlessFullscreen | EDIT (drop SDL2) | Headless and Terminal sources are unchanged, so the defect stands. SDL2 removed by 76c9bda29. | expected: 'functions of the X11, SDL2 and SDL3 platforms ({{src:modules/platform/src/X11/X11Platform.cpp\|X11Platform.cpp}}, <code>Sdl2Platform</code>.cpp, <code>Sdl3Platform</code>.cpp)' -> 'functions of the X11 and SDL3 platforms ({{src:modules/platform/src/X11/X11Platform.cpp\|X11Platform.cpp}}, <code>Sdl3Platform</code>.cpp)'; evidence: 'the X11, SDL2 and SDL3 <code>CreateWindow</code> functions' -> 'the X11 and SDL3 <code>CreateWindow</code> functions'; blast_radius: '(SDL3, SDL2, X11, Wayland, Win32)' -> '(SDL3, X11, Wayland, Win32)' |
| CNA-BUG-180 | CNA-BUG-180 | Win32GlContext reports request as granted | EDIT (drop OpenGL4) | Win32GraphicsServices.cpp and Win32Window.cpp are unchanged. EasyGLRenderer.cpp RequestedGlContext still requests no multisample. | blast_radius: "EasyGL's <code>RequestedGlContext</code> and OpenGL4's <code>RequestedContext</code> ask only for" -> "EasyGL's <code>RequestedGlContext</code> asks only for"; blast_radius: 'an EasyGL or OpenGL4 renderer that asked' -> 'an EasyGL renderer that asked' |
| CNA-GAP-059 | CNA-GAP-059 | MinGW CnaTests Wine emulator only for D3D defaults | EDIT (drop DIRECT2D) | At T, UnitTests.cmake (lines ~1198-1210) sets CROSSCOMPILING_EMULATOR only for DIRECTX9, DIRECTX11 and DIRECTX12 defaults. 0f96ea703 removed the DIRECT2D branch. The mingw toolchain usage example is unchanged (SDL_RENDERER). | title -> "In a MinGW-w64 cross tree CnaTests gets a Wine CROSSCOMPILING_EMULATOR only when the default renderer is DIRECTX9, DIRECTX11 or DIRECTX12"; actual: 'DIRECTX12 default, or when DIRECT2D is in <code>CNA_RENDERER_IDENTITIES</code>.' -> 'DIRECTX12 default.'; blast_radius: 'Direct3D and Direct2D cross trees, and native builds, are unaffected.' -> 'Direct3D cross trees and native builds are unaffected.' |
| CNA-VGAP-012 | CNA-VGAP-012 | No CI selects CNA_PLATFORM=WAYLAND | EDIT (drop SDL2) | 76c9bda29 removed the "SDL2 + OpenGLES3" matrix cell from platform-ci.yml. The matrix is now SDL3 (3 cells), HEADLESS and TERMINAL; still no WAYLAND job, and wayland_test_server.sh is unchanged. | actual: "matrix is SDL3, SDL2, HEADLESS and TERMINAL" -> "matrix is SDL3, HEADLESS and TERMINAL" |
| CNA-BUG-181 | CNA-BUG-181 | SDL3 reports nativeFileDialog on iOS/web | STILL VALID, plus a related-link edit if that page goes | Sdl3Platform.cpp:339 still has `capabilities.nativeFileDialog = true;` with no guard. | related.guide ["docs/cnaext-engine.html","CNAEXT engine layer"]: replace or drop if the site retires or renames the engine-layer page (the engine layer was retired by 5572f3ca1) |

Retirement mechanics: all seven retired entries keep their original ids as stable keys (none was added or reclassified), so plain `"retired": {"<id>": {"classification": "OBSOLETE" | "PROVEN FIXED", "evidence": ...}}` works for each of them.

#### (2) STILL VALID (cited code or CI re-read at T)

- **CNA-BUG-176:** Game.cpp setIsMouseVisibleProperty still calls `mouse->SetCursorVisible` uncaught. TerminalMouse::SetCursorVisible still throws. The test still covers only the no-pointer case.
- **CNA-BUG-179:** Win32Window.cpp unchanged.
- **CNA-BUG-182:** Win32SystemServices.cpp and the contract headers unchanged.
- **CNA-BUG-183:** ResultTrampoline (Sdl3SystemServices.cpp:738) and EntryClickTrampoline (Sdl3Tray.cpp:119) still have no try/catch.
- **CNA-BUG-184:** `-lembind` is still in modules/core/CMakeLists.txt with its emscripten::val comment. No emscripten/val.h or bind.h include anywhere. The stale comment in GraphicsRendererSelection.cpp:25 remains. probe_core's pattern still lacks libSDL3 and keeps the "SDL3 ... PRIVATE detail" comment.
- **CNA-BUG-185:** stub/examples/CMakeLists.txt still links SDL3::SDL3 unguarded. CNA_ENABLE_SDL=OFF is still supported; SdlAvailability.cmake lost only its SDL2 and FREEDIRECT items.
- **CNA-BUG-186:** pkg_check_modules is still unversioned (modules/CMakeLists.txt:31-42). VideoDecoder.cpp still uses ch_layout and swr_alloc_set_opts2.
- **CNA-BUG-191:** ThirdPartyENet.cmake and .gitmodules unchanged.
- **CNA-BUG-193:** KNOWN_FAILURES is still ("EasyGL_GraphicsDevice_ReferenceStencil"). EasyGLRenderer::SetReferenceStencil is present. REMEDIATION_PROGRESS.md unchanged.
- **CNA-BUG-196:** PlatformX11.cmake and the X11 sources unchanged.
- **CNA-BUG-197:** mingw-w64.cmake unchanged (x86_64 processor, i686 fallback, PREFIX_PATH comment). ThirdPartySDL.cmake still keys on CMAKE_SYSTEM_PROCESSOR.
- **CNA-BUG-198:** every ModuleLinkClosure_* add_test still passes `--build-dir "${CMAKE_BINARY_DIR}"`; the new ModuleLinkClosure_XmlFree_* set from 1ca684199 does the same.
- **CNA-BUG-262:** CnaTests still gets `-sJSPI=1` (UnitTests.cmake:603) and `cna_emscripten_asyncify` (`-sASYNCIFY=1`); there is no CNA_EMSCRIPTEN_ASYNCIFY OFF for CnaTests.
- **CNA-BUG-269:** cna_validate_renderer_identity_selection still checks CNA_RENDERER_<X> only for retired names.
- **CNA-GAP-054, GAP-055, GAP-056, GAP-058:** sources unchanged.
- **CNA-GAP-057:** Sdl3SystemServices.cpp:667 still has `button.flags = 0`. Other sources unchanged.
- **CNA-GAP-069:** SharpRuntimeConsumption.cmake still sets the Windows HAS_XML_SERIALIZATION OFF branch with the DX-250 comment. Its "CNAEXT" wording is fine, because CNAEXT survives.
- **CNA-PLAT-013:** WaylandMouse.cpp and platform-input-notes.md unchanged.
- **CNA-VGAP-007:** no test at T names Sdl3Camera, Sdl3CameraProvider, Sdl3Tray or ResultTrampoline.
- **CNA-VGAP-013:** neither script is invoked by cmake, workflows or scripts; mentions are only in docs, plans and NEXT.md.
- **CNA-VGAP-014:** the validator is still GLOB_RECURSE "*.cpp" "*.mm" with a prefix match (modules/CMakeLists.txt:452), cna_add_renderer still uses non-recursive `src/*.cpp`, and the directx9 and common/d3d shader subdirectories still exist.
- **CNA-VGAP-015:** Rgba16 is still used (EasyGLRenderer.cpp:1525,1540) and EASYGL_EMSCRIPTEN_EXCEPTION_MODEL is still forced. No sibling pin or check was added. I could not tell from CNA alone whether the required minimum revisions have risen.
- **CNA-VGAP-060:** InjectEvent still has no caller (only its declaration, definition and the plan row). The `HeadlessPlatform*` filter token is still in UnitTests.cmake:1569 and matches no suite.

#### (3) New issues at T

**NEW-1 (bug, Build & CI, low–medium): the setenv/unsetenv gate is gone and the calls it guarded against have spread.**
- MOD-RETIRE-1 (5572f3ca1) deleted the CTest that ran scripts/check_no_posix_setenv.py. The script still exists but nothing runs it.
- Replicating the script's scan (modules/tools/tests, *.cpp/*.hpp, comment lines skipped): 12 lines in 5 files at O, 53 lines in 18 files at T.
- The clearest case is modules/graphics/tests/Microsoft/Xna/Framework/Graphics/IndexedDrawDeferredTests.cpp, struct CpuBaseVertexSwitch. It calls `::setenv`/`::unsetenv("CNA_EASYGL_CPU_BASE_VERTEX")` outside any `#if`, was added by 1dc4ce06a (CBIND-139, 2026-10-01), and is pulled into CnaTests on every target by UnitTests.cmake's `GLOB_RECURSE "modules/*/tests/*.cpp"`.
- Most of the new gamer-services test hits are also unguarded. Some are under `#if defined(__unix__) || defined(__APPLE__)` (ServiceRequestRetryTests, the LocalProfileTests includes); not checked one by one.
- Consequence, inferred and not built: MinGW-w64 and MSVC have no POSIX setenv (CNA's own docs/cnatests-mingw-setenv-proposal.md), so Windows CnaTests builds would fail to compile.
- Also stale: modules/content-pipeline/tests/CNA/Content/Pipeline/EffectSourceCommandLineTests.cpp:177 still says ctest `CNAEXT_NoPosixSetenv` refuses setenv.
- Confidence: source-verified for the scan; probable for the compile failure.

**General note:** most entries' evidence says "Checked by reading at 009d40f5". Once verified_against moves to T this needs a global decision (re-verification note or global_replace); not handled per entry here.

#### (4) Counts (45 entries)

| Disposition | Count | Entries |
|---|---|---|
| RETIRE (OBSOLETE) | 6 | BUG-178, BUG-189, BUG-194, BUG-195, BUG-200, VGAP-010 |
| RETIRE (PROVEN FIXED) | 1 | VGAP-009 |
| NARROWED | 1 | VGAP-011 |
| CHANGED | 6 | BUG-035, BUG-190 (+ folded BUG-187 patch), BUG-192, BUG-199, PLAT-014, VGAP-008 |
| EDIT | 4 | BUG-177, BUG-180, GAP-059, VGAP-012 |
| STILL VALID | 27 | BUG-181 included (related link conditional) |

After these edits no entry in this batch has a source path missing at T or a mention of a retired renderer (BUG-190 and BUG-199 drop their dead paths; the rest are retired).



---

## Appendix NET: Networking & gamer services + Storage


Task: classify every entry in batch-NET (42 GamerServices, Net, Storage and Phone entries) at T=b0e97bb1 against O=009d40f5. This was read-only: no repository was changed and nothing was written.

#### Counts
- **RETIRE-FIXED:** 14.
- **RETIRE-OBSOLETE:** 1.
- **NARROWED:** 2.
- **CHANGED:** 3.
- **EDIT:** 2.
- **STILL VALID:** 20.
- **Total:** 42.

None of these 42 entries appears in rrhits.json, so no retired renderer name needs removing. No SDL2 or engine-layer mentions. Only one dead source path: BUG-175.

#### Patch-mechanism caveats
- **Pass order matters.** patches-adversarial is applied in this order: entries → folded → retired → reclassified → added.
- **Reclassified entries are edited by their old id.** BUG-250 has stable key CNA-GAP-050, so its edit goes in `entries["CNA-GAP-050"]`.
- **Added entries cannot be retired by the current script.** Four entries came from the `added` list: BUG-258 (NEW-AUDIT-10), BUG-265 (NEW-AUDIT-21), BUG-266 (NEW-AUDIT-23) and BUG-268 (NEW-AUDIT-25).
  - A `retired` key for them fails with "unknown entry", because `retired` runs before `added`.
  - Deleting them from `added` renumbers every later added bug, e.g. CNA-BUG-259 would become CNA-BUG-258.
  - The fix needs a script change: either a skip or retired flag on an added item, or a retire pass that runs after `added`.
- **Edits to added entries go in the `added` item itself.** GAP-070 is NEW-AUDIT-14, so its edit goes into that `added` array element.
- **Stale "009d40f5" phrases.** Every entry's evidence says "Checked by reading at 009d40f5". That needs a global re-wording or a re-verification statement.

#### (1) Entries needing action

| Published id | Stable key | Short title | Disposition | Evidence at T | Proposed change |
|---|---|---|---|---|---|
| CNA-BUG-151 | CNA-BUG-151 | EnsureStorageRoot latches an empty root after a failed resolution | RETIRE-FIXED (PROVEN FIXED) | 8a67da536 (SAMPLE-070). In `modules/storage/src/StorageDevice.cpp`, `EnsureStorageRoot` now sets `storageRootInitialized_ = true` only after `storageRoot_` is assigned. A failed `create_directories` throws `StorageDeviceNotConnectedException` and the next call retries. Code evidence only; no test. | retire: "Fixed by 8a67da536: the flag is published after storageRoot_ is assigned; a failed creation throws and is retried, so no empty root is latched." |
| CNA-BUG-150 | CNA-BUG-150 | Flag published before the root, unsynchronised | CHANGED | Same commit fixed the order, but the three statics are still plain and unsynchronised (StorageDevice.hpp lines 178–180). | See CHANGED texts below. |
| CNA-BUG-165 | CNA-BUG-165 | LeaderboardReader Read/PageDown/PageUp leak LeaderboardAction | RETIRE-FIXED | 9473f5c89 (GS-006a). Every synchronous wrapper in `LeaderboardReader.cpp` (three `Read` overloads, `PageDown`, `PageUp`) wraps the Begin result in `std::unique_ptr<System::IAsyncResult> owned(result)`. Code evidence only. | retire |
| CNA-BUG-166 | CNA-BUG-166 | Dispatcher Initialize deletes app-created SignedInGamers | RETIRE-FIXED | 0ab6cc3fe (GS-003b/004a). `Initialize` no longer creates or deletes gamers; it fills the list from internal slots via `publish()`. Covered by the harness in `tools/net/gamerservices_dispatcher_harness.cpp`: mode `initialize-leak-check` asserts `GetFreedGamerCountForTesting()==0`, and `GamerServicesDispatcherHangRegressionTest.InitializeWithoutAServiceSignsInNobody` checks the empty case. | retire. Residual note: `publish()` empties a collection the app installed via `setSignedInGamersProperty` but frees nothing. This is XNA-consistent, since that setter is internal in XNA. |
| CNA-BUG-266 | NEW-AUDIT-23 | Initialize silently re-initialises | RETIRE-FIXED (needs script support, see caveats) | 0ab6cc3fe: `if(isInitialized_) throw InvalidOperationException("Gamer services are already initialized.")`. The harness `initialize-leak-check` asserts the refusal. | retire |
| CNA-BUG-265 | NEW-AUDIT-21 | SignedIn not replayed to late subscribers | RETIRE-FIXED (needs script support) | 6f61c5cb9 (GS-004n). `SignedInGamer.cpp` installs `SignedIn.SetReplayHook`; SignedIn is now raised at Update, not inside Initialize. Test: `SystemGuideTest.SignedInReplaysOnSubscribeAndSigningOutDisposesTheGamer`. | retire |
| CNA-BUG-167 | CNA-BUG-167 | Store rounds 64-bit through double; unchecked temp-file rename | RETIRE-FIXED | 38287637d (GS-AUDIT-005): nlohmann integer storage plus legacy-safe `Integer()`; test `LeaderboardWriterTest.OfflineIntegerBoundariesRoundTripExactly`. 33e08899f (GS-AUDIT-001): `WriteJsonFile` uses stream exceptions and renames only after success, and the fallback is gone; tests `OfflineWriteFailurePreservesPreviousRecord` and `OfflineSaveRefusesAnUncreatableParentDirectory`. | retire. Note: history already rounded before the fix cannot be recovered. |
| CNA-BUG-171 | CNA-BUG-171 | ReceiveData(PacketReader) does not resize the reader | RETIRE-FIXED | 35ce1f3e8 (GS-007m). `data.ResizeInternal(size)`, which calls `SetLength`; an empty queue resizes to 0. Test: `LocalNetworkGamerTest.ReceiveDataReturnsThePacketSizeAndRefusesWithoutDequeuing` (checks reader length 6, then 0). | retire |
| CNA-BUG-174 | CNA-BUG-174 | ReceiveData(PacketReader) always returns 0 | RETIRE-FIXED | 35ce1f3e8: returns `size`. Same test (`EXPECT_EQ(6, ReceiveData(reader, sender))`). | retire |
| CNA-BUG-258 | NEW-AUDIT-10 | ReceiveData(byte[]) dequeues and truncates an oversized packet | RETIRE-FIXED (needs script support) | 35ce1f3e8: checks the size against the front packet first, throws `ArgumentException`, and leaves the packet queued. Same test asserts the throw and that `IsDataAvailable` is still true. | retire |
| CNA-BUG-172 | CNA-BUG-172 | Joined SystemLink session reports MaxGamers 31 / PrivateGamerSlots 4 | RETIRE-FIXED | 4a1121e03 (GS-007n). In `ENetBackend.cpp`, `HandleClientHello` sends `CurrentSettings(session)` right after the welcome; clients apply it in `HandleSessionSettings`, and the host republishes on change. Tests: `ENetBackendTest.AClientReportsTheHostsSettingsAndMachines` (client reads 12/2) and `HostSendsItsSettingsAndMachineGroupingAndRepublishesChanges`. | retire. Caveat: EndJoin still constructs the session with 31/4; the real values arrive in the settings packet right behind the welcome. |
| CNA-BUG-173 | CNA-BUG-173 | Presence table alphabetical, indexed by ordinal | RETIRE-FIXED | ac56c4f50 (GS-005a). `presenceModeStrings_` is now in `GamerPresenceMode` declaration order (index 0 is "", ends "Found Secret", "Cornflower Blue"). Test: `ServiceReadLifetimeTest.PresenceChangedWhilePendingPublishesTheNewRevisionOnFollowingUpdate` asserts Level gives "Level 1". | retire |
| CNA-BUG-268 | NEW-AUDIT-25 | Begin* callback calling End* frees the running closure and the returned pointer | RETIRE-FIXED (needs script support) | b7754e45f (GS-007e2b, caller-owned Net async results). `InvokeActiveActionCallback` keeps ownership across the callback (copies the callback, `unique_ptr`, `release`), and End* no longer deletes the action. Test: `NetworkSessionTest.BeginCreateCallbackCanReentrantlyCallEndCreate` now uses the returned result after a reentrant `EndCreate` (`IsCompleted`, `WaitOne(0)`, second End throws). | retire |
| CNA-GAP-051 | CNA-GAP-051 | Guide's 14 Show* and DelayNotifications are no-ops | RETIRE-FIXED | Commits: ac56c4f50, a482999e5 (GS-005c), 45c23451b (GS-005d), 8abd5e029 (GSX-U1), 8559d5bd3 (parties).<br>In `Guide.cpp` every Show* runs XNA's checks and opens a GuideUi screen; `DelayNotifications` calls `delayNotifications()`; `ShowGameInvite(sessionId)` throws `NotSupportedException` as XNA does on Windows.<br>Tests: `GuideSocialPaneTests.cpp`, `GuideUiTests.cpp`, `GuidePartyTests.cpp`, `GamerServicesServiceTests.cpp`. | retire |
| CNA-GAP-052 | CNA-GAP-052 | Local gamer services have no catalogue, presence or profile data; permissive privileges | RETIRE-FIXED | Commits: 529f22e45 (offline achievement catalog, honest profile fields), 32c0002ff (GetPicture), ac56c4f50 (presence), 148d9db35 (privileges), 4f7796e46 (GamerZone and Reputation).<br>At T: `Achievement::GetPicture` returns a title-file or service-asset stream; `SetPresenceModeStringEXT` sets and publishes; privileges come from account policy.<br>Tests: `SignedInGamerTest.AnOfflineCatalogListsEveryDefinedAchievementWithItsEarnedState` (names, descriptions, GetPicture), `GuidePrivilegeTest.TheAccountsPolicyBecomesItsGamerPrivileges`. | retire. Remaining offline-profile permissiveness is documented as intentional in docs/gamer-services-known-limitations.md §20 and §23. |
| CNA-GAP-053 | CNA-GAP-053 | Voice, party invites, RemoveFromSession, arbitration/TrueSkill events, QoS bandwidth missing | NARROWED | Commits: b1d44dc94 (voice), 8559d5bd3 and 35ce1f3e8 (party invites and checks), ea10f1f5c (`RemoveFromSession`), 062cbe193 and db71f60b4 (events raised at NetworkSession.cpp lines 941–943 and 1038–1039), b4a378b90 and 122922f52 (SystemLink QoS bandwidth).<br>Tests: `ENetBackendTest.VoiceFromTheMicrophoneOwnerReachesTheRemoteMachine`, `NetworkMachineTest.RemoveFromSessionFollowsTheReferenceChecks`, `OnlineLeaderboardTest.RankedMachinesReportArbitratedAndTrueSkillForEveryGamerAndAgreementCommits`, `ENetDiscoveryServiceTest.UpstreamInvitationsAndReportsRoundTripAndRefuseNegativeRates`.<br>What survives: QoS of PlayerMatch/Ranked search results (CNA limitations §17). | See NARROWED texts below. |
| CNA-PLAT-011 | CNA-PLAT-011 | Emscripten saves lost on page reload | NARROWED | 8a67da536 and c5986156d (SAMPLE-071). `modules/storage/src/WebStoragePre.js` mounts IDBFS over /cna-storage and /save (autoPersist) and runs syncfs before main; StorageDevice roots storage there. `modules/storage/CMakeLists.txt` links it only when `NOT CNA_ENABLE_EMSCRIPTEN_THREADS OR NOT CNA_EMSCRIPTEN_USE_WASMFS`; otherwise `cnaStorageReady` is never set and StorageDevice throws. The browser save/reload run is recorded by CNA in NEXT.md (SAMPLE-070); there is no automated browser test. | See NARROWED texts below. |
| CNA-BUG-050 | CNA-BUG-050 | Guide results cannot be waited on | CHANGED (status stays narrowed) | Dispatcher Update now pumps the service backend (0ab6cc3fe, 73011288e). End* waits by running the game's modal frames (70d6f109e, `PrepareForEnd`) and throws only when no running game presents the Guide. Still true: `GuideAction` constructs `asyncWaitHandle_(true, ManualReset)` (Guide.cpp lines 58–92); it is never reset, and `GuideMessageBoxAction` and `GuideKeyboardInputAction` derive from it. | See CHANGED texts below. |
| CNA-GAP-070 | NEW-AUDIT-14 | NetworkSession Begin/End are synchronous | CHANGED (edit in the `added` item) | PlayerMatch/Ranked Create/Find/Join and JoinInvited are now genuinely pending (`QueueOnlineSession`, `QueueServiceSearch`, `Queue`; End pumps up to 30 s). For Local, LocalWithLeaderboards and SystemLink, Begin still completes and runs the callback inline. `completedSynchronously_` now defaults to true (NetworkSession.hpp line 1006). `kSearchWindowMs=150` and the 5 s EndJoin wait still exist. | See CHANGED texts below. |
| CNA-BUG-250 | CNA-GAP-050 | SendData in Local/LocalWithLeaderboards drops packets | EDIT (defect unchanged) | NetworkSession.cpp `Update`: `if (RealNetworkingEnabled(sessionType_) \|\| online_)`; `RealNetworkingEnabled` is still SystemLink-only (ENetBackend.cpp line 1561). misc/known_gaps.md §4 was rewritten and no longer says "nothing is missing about Local sessions". Test names unchanged. | See EDIT texts below. |
| CNA-BUG-168 | CNA-BUG-168 | Sanitiser maps distinct gamertags to one achievements file | EDIT (narrower blast radius) | `SanitizeStoreFileNameComponent` is unchanged. Since ac961f433, local profiles must pass `isValidLocalGamertag` (ASCII alphanumerics and single spaces, ≤15 characters, case-folded), so Guide-created profiles cannot collide. Arbitrary names still arrive through `SignedInGamer::CreateInternal` and `cna_signed_in_gamer_create_ext`. Service accounts award on the service. | See EDIT texts below. |
| CNA-BUG-175 | CNA-BUG-175 | Procedural avatar garment shells interpenetrate the body | RETIRE-OBSOLETE | The subject is gone. 3f4518e69 (GS-009b..d) replaced the procedural avatar with the generated 71-slot catalog. 13dfe0499 (GS-009f) removed the Blender scripts, including both cited `tools/avatar_builder/*.py` files, which are missing at T. NEXTnet.md is now marked HISTORICAL CHECKPOINT. Garment fit for catalog v2 was reworked in 75a390447; test `AvatarCatalogTest.ItemsAreFittedToTheirBody`. | retire, classification OBSOLETE |

##### CHANGED and NARROWED texts

**CNA-BUG-050**
- **title:** "Guide message-box and keyboard-input results expose an AsyncWaitHandle that is already signalled while the answer is pending"
- **summary** (255 characters): "Guide's message-box and keyboard-input results construct their AsyncWaitHandle already signalled, so WaitOne returns while IsCompleted is still false; End* now waits by running the game's modal frames and refuses only when no running game shows the Guide."
- **public_contract:** "getAsyncWaitHandleProperty() and getIsCompletedProperty() of the IAsyncResult returned by Guide::BeginShowMessageBox and Guide::BeginShowKeyboardInput; EndShowMessageBox and EndShowKeyboardInput"
- **actual (replace):** "<p>{{src:modules/gamer-services/src/Xna/Guide.cpp|Guide.cpp}}'s <code>GuideAction</code>, the base of the message-box and keyboard-input results, constructs its <code>EventWaitHandle</code> signalled (<code>asyncWaitHandle_(true, ManualReset)</code>), and nothing resets it, so <code>WaitOne()</code> returns at once while <code>IsCompleted</code> is still false. End* no longer throws while the answer is pending: since 70d6f109e it claims the result and runs the game's modal frames until the Guide is answered, and it throws <code>InvalidOperationException</code> only when no running game presents the Guide. <code>GamerServicesDispatcher::Update</code> now pumps service work, but the answer comes only from the Guide drawn in the game's frames, so a thread that waits on the handle and then calls End* still blocks in End*, or gets the exception.</p>"
- **sources notes:**
  - GamerServicesDispatcher.cpp → "Update pumps service work; it does not answer a pending Guide result"
  - Guide.cpp → "GuideAction constructs its wait handle signalled; PrepareForEnd runs modal frames"
  - Guide.hpp → "BeginShowMessageBox completes when the user answers"
  - Drop the GamerServicesComponent.cpp note "forwards to the empty dispatcher Update", or re-note it.

**CNA-BUG-150**
- **title:** "StorageDevice::EnsureStorageRoot caches the process-wide storage root in unsynchronised statics"
- **summary** (253 characters): "The storage root is cached in a plain static bool and std::string with no lock or atomic, so two threads touching storage for the first time both resolve it and write the string concurrently, a data race, and a reader may see the flag before the string."
- **actual:** "<p><code>EnsureStorageRoot</code> in {{src:modules/storage/src/StorageDevice.cpp|StorageDevice.cpp}} tests <code>storageRootInitialized_</code>, resolves the path, assigns <code>storageRoot_</code> and sets the flag last. That order was corrected by 8a67da536, which removed the single-threaded empty-root latch. <code>storageRoot_</code>, <code>appName_</code> and <code>storageRootInitialized_</code> are still plain statics with no lock or atomic. Two threads that arrive before the first resolution finishes both resolve the root and both assign the <code>std::string</code>, a data race (undefined behaviour). Nothing orders the plain <code>bool</code> store after the string store, so another core may see the flag set while the string is still being written.</p>"
- **sources[0].note:** "StorageDevice::EnsureStorageRoot (flag set after storageRoot_, no lock), SetAppNameEXT, GetStorageRootEXT"
- **evidence:** drop "The same flag-first order is why a failed resolution latches an empty root..." from `actual`. The regression test text may stay.

**CNA-GAP-070** (edit inside the `added` item NEW-AUDIT-14)
- **title:** "NetworkSession's Local, LocalWithLeaderboards and SystemLink Begin/End pairs are synchronous: Begin runs the callback and returns a completed result, and End does the work on the caller's thread"
- **summary** (230 characters): "For Local, LocalWithLeaderboards and SystemLink sessions, BeginCreate, BeginFind and BeginJoin run the callback inline and return a completed result; End* then blocks: 150 ms for a SystemLink Find, up to 5 s for a SystemLink Join."
- **actual:** "<p>In {{src:modules/net/src/Xna/NetworkSession.cpp|NetworkSession.cpp}} a <code>NetworkSessionAction</code> starts complete (<code>IsCompleted</code> true, wait handle signalled, <code>CompletedSynchronously</code> true). For every session type except <code>PlayerMatch</code> and <code>Ranked</code>, <code>BeginCreate</code>, <code>BeginFind</code> and <code>BeginJoin</code> invoke the <code>AsyncCallback</code> inline (<code>InvokeActiveActionCallback</code>) before returning. The work then runs in End* on the caller's thread. On native builds, <code>EndFind</code> waits the fixed 150 ms SystemLink discovery window, and <code>EndJoin</code> pumps the joined session for up to 5 s until the host's welcome arrives. A game that polls <code>IsCompleted</code> every frame and calls End* when it turns true therefore stalls there. Service-backed <code>PlayerMatch</code>/<code>Ranked</code> Create, Find and Join, and <code>BeginJoinInvited</code>, are genuinely pending (<code>QueueOnlineSession</code>, <code>QueueServiceSearch</code>): <code>IsCompleted</code> stays false until the CNA service answers, so they are not part of this entry.</p>"
- **public_contract:** drop BeginJoinInvited.
- **sources note:** NetworkSession.hpp → "NetworkSessionAction::completedSynchronously_ defaults to true".

**CNA-GAP-053** (status narrowed)
- **title:** "QualityOfService of PlayerMatch and Ranked search results is never measured"
- **summary** (210 characters): "QualityOfService of a PlayerMatch or Ranked search result is never measured: IsAvailable stays false and the round-trip and bandwidth fields stay 0, so online lobbies cannot sort sessions by connection quality."
- **actual:** "<p><code>EndFind</code> in {{src:modules/net/src/Xna/NetworkSession.cpp|NetworkSession.cpp}} builds each service listing with <code>QualityOfService::CreateInternal()</code>, which ({{src:modules/net/src/Xna/QualityOfService.cpp|QualityOfService.cpp}}) sets <code>IsAvailable</code> false and leaves both round trips and both bandwidths at 0. SystemLink results measure the round trip and both bandwidths. CNA's own limitations register (§17) records the missing pre-join relay probe. Voice, party invites, <code>RemoveFromSession</code>, the arbitrated, unarbitrated and TrueSkill write events, and SystemLink bandwidth are implemented since the commits named in the evidence.</p>"
- **public_contract:** "AvailableNetworkSession::getQualityOfServiceProperty() for PlayerMatch/Ranked listings; QualityOfService"
- **sources:** NetworkSession.cpp ("EndFind: service listings get an unmeasured QualityOfService"), QualityOfService.cpp ("default constructor: IsAvailable false"), docs/gamer-services-known-limitations.md ("§17").

**CNA-PLAT-011** (status narrowed)
- **title:** "Threaded Emscripten builds on the default WasmFS have no persistent storage, so StorageDevice refuses rather than saving"
- **summary** (229 characters): "Threaded Emscripten builds default to WasmFS, which cannot link IDBFS, so StorageDevice there reports StorageDeviceNotConnectedException instead of persisting saves unless the application configures CNA_EMSCRIPTEN_USE_WASMFS=OFF."
- **actual:** "<p>Since 8a67da536 and c5986156d the storage module links IDBFS. A pre-js hook ({{src:modules/storage/src/WebStoragePre.js|WebStoragePre.js}}) mounts <code>/cna-storage</code> and <code>/save</code> over IndexedDB with autoPersist and restores them before <code>main()</code>, and {{src:modules/storage/src/StorageDevice.cpp|StorageDevice.cpp}} roots storage, and so the gamer-services store, there. {{src:modules/storage/CMakeLists.txt|CMakeLists.txt}} adds these link options only when <code>NOT CNA_ENABLE_EMSCRIPTEN_THREADS OR NOT CNA_EMSCRIPTEN_USE_WASMFS</code>. A threaded build on its default WasmFS therefore never sets <code>Module.cnaStorageReady</code>, and <code>EnsureStorageRoot</code> throws <code>StorageDeviceNotConnectedException</code>. A failed IndexedDB restore has the same result. Turning WasmFS off restores persistence, but {{src:docs/web-emscripten-graphics-limitations.md|the web limitations page}} warns that worker file access then waits on the browser thread.</p>"
- **tests_current:** "No automated browser storage test; CNA records a Chrome save/reload run of SAMPLE-070 in NEXT.md."
- **workaround:** "Configure -DCNA_EMSCRIPTEN_USE_WASMFS=OFF in threaded builds that need saves."
- **sources:** add WebStoragePre.js, modules/storage/CMakeLists.txt and docs/web-emscripten-graphics-limitations.md. StorageContainer.cpp ("no Emscripten persistence branch") is now irrelevant; drop it.

##### EDIT texts

**CNA-BUG-250** (`entries["CNA-GAP-050"]`)
- **summary:** "(SystemLink)" → "(SystemLink, or a service-backed PlayerMatch/Ranked session)".
- **actual:**
  - "delivers it only inside if (<code>ENetBackend::RealNetworkingEnabled(sessionType_)</code>), which is true for <code>SystemLink</code> alone ({{src:…ENetBackend.cpp}}), so" → "delivers it only when <code>ENetBackend::RealNetworkingEnabled(sessionType_)</code> (true for <code>SystemLink</code> alone, {{src:modules/net/src/Internal/ENetBackend.cpp|ENetBackend.cpp}}) or the session is a service-backed <code>PlayerMatch</code>/<code>Ranked</code> session, so"
  - "but no CNA header documents it and {{src:misc/known_gaps.md|known_gaps.md}} says the opposite." → "a comment in <code>Update</code> now records the no-op on the premise that these sessions \"have no remote gamers\", which overlooks delivery between local gamers, and no CNA header documents it."
- **sources:** remove the misc/known_gaps.md item (its §4 no longer makes that claim).

**CNA-BUG-168**
- **blast_radius:** "<p>Gamers created with arbitrary gamertags through <code>SignedInGamer::CreateInternal</code> or the C route <code>cna_signed_in_gamer_create_ext</code> while no service is configured: two names that sanitise alike share one achievements list. Local profiles from the Guide's sign-in are limited to ASCII letters, digits and single spaces and matched case-insensitively ({{src:modules/gamer-services/src/Internal/LocalProfiles.cpp|LocalProfiles.cpp}}, <code>isValidLocalGamertag</code>), so two of them cannot collide, and service accounts keep their achievements on the service. Leaderboards are unaffected.</p>"
- This removes the phrase "the four stub gamers".
- **sources:** optionally add LocalProfiles.cpp ("isValidLocalGamertag").

#### (2) STILL VALID (checked at T)
- **BUG-047:** `StorageContainer.cpp`, its header, `CnaCApiStorage.cpp` and both tests are byte-identical at T (`GlobMatch` unchanged).
- **BUG-152:** the space and connected properties still pass the `std::string` root to `fs::exists`, `fs::space` and `fs::path` (StorageDevice.cpp at T).
- **BUG-153 / BUG-155:** `StorageContainer.cpp` and its header are unchanged.
- **BUG-154:** `StoreRoot()` is still `GetStorageRootEXT()/"GamerServices"` and `DeleteContainer` still does `remove_all`.
- **BUG-156, 157, 158, 159, 160, 161, 163, 164:** `modules/phone` has zero diff from O to T; `inspector/InternalSocket.cpp` is unchanged.
- **BUG-162:** phone unchanged; no WSAStartup; `cmake/UnitTests.cmake` still excludes `HttpNotificationChannelTests.cpp` on WIN32 (WINNATIVE-0014).
- **BUG-169:** `AddLocalGamer` still inserts into `allGamers_` immediately and queues a GamerJoin; the constructor's replay hook walks `allGamers_`. All three cited tests exist.
- **BUG-170:** the NetworkSession constructor still calls `StartHosting` for every SystemLink session (`ConnectToHost` also calls it natively), which calls `RegisterHost`. `ReplyToQuery` has no IsHost check, and `HandleClientHello` has no host check. Cited tests exist.
- **BUG-267:** `HandleClientHello` sends `ServerWelcome` and registers wire ids before `AddRemoteGamer` throws "Session is full!". The receive switch catches `std::exception`. `SessionFull` appears only in `OnlineSessionBinding.cpp` (online path). Optional appended note: Find now filters out sessions without open public slots (`ENetDiscoveryService::Matching`), which reduces but does not remove exposure.
- **GAP-048:** `StorageContainer.cpp` is unchanged.
- **GAP-049:** `DeviceChanged` has no Raise anywhere (only Add/Remove in the C API).
- **PLAT-012:** the Emscripten branch of `ENetDiscoveryService` is still empty stubs; `kEmscriptenHostPort=61191`; the `EndJoin` welcome wait is still inside `#ifndef __EMSCRIPTEN__`; the examples and the TwoProcess and dispatcher tests are still excluded. It is consistent with CNA limitations §26.

#### (3) NEW issues found at T (with evidence)
1. **SendDataOptions cannot express XNA's combined Chat flags** (functional-gap, or bug).
   - `modules/net/include/Microsoft/Xna/Framework/Net/SendDataOptions.hpp` declares a plain `enum class` with values 0–4 and no bitwise operators.
   - `NetPacketCodec.cpp` (lines 570–575) maps Chat and any unknown value to `ENET_PACKET_FLAG_RELIABLE`.
   - XNA's `[Flags]` allows Chat combined with Reliable or InOrder (values 5–7) and chat-ordered traffic.
   - CNA records this itself as GS-AUDIT-016 in `audit/gamer-services/gamer-services-issues.md` ("XNA COMPATIBILITY LIMITATION").
2. **Offline leaderboards drop Stream columns, and column-only edits are not persisted offline** (functional-gap).
   - CNA's own GS-AUDIT-006 and limitations §22 ("offline local boards (no service) do not keep Stream columns").
   - `LocalGamerServicesStore.cpp` `ColumnsToJson` skips Stream values.
   - `LeaderboardWriter.cpp` saves offline only through the rating hook.
3. **Online guests are refused** (functional-gap). CNA limitations §16: PlayerMatch and Ranked refuse guests with `GamerServicesNotAvailableException` or `GamerPrivilegeException`. XNA allows guests of a LIVE profile.
4. **Optional, LOW:** signed-out SignedInGamer objects are kept for the whole process lifetime (`ownedGamers` vector in `GamerServicesDispatcher.cpp`). CNA marks it accepted design (GS-AUDIT-012). Publish only if accepted-design memory growth counts as a known issue.

Outside my scope, for the website team: GS-AUDIT-013 in the same CNA audit file says libcna.com features claims were obsolete. Its status is FIXED by website commit df85d05.


---

## Appendix MISC: Input + Diagnostics & Inspector + C API & bindings


#### R9 batch MISC: dispositions at T (Input, Diagnostics and Inspector, C API and bindings; 26 entries)

All checks were read-only, using git objects at T=b0e97bb1 against O=009d40f5. Nothing was written to any repository.

##### Executive summary
Of the 26 entries, 6 need action and 20 are still valid.
- **Retire, subject removed:** CNA-BUG-270. The engine layer's C API was deleted.
- **Retire, fixed:** CNA-VGAP-055. BINDFIX-041 fixed the defect and added a CNA test for exactly this case.
- **Changed:** CNA-BUG-133, CNA-BUG-213 and CNA-GAP-062.
- **Edit:** CNA-BUG-134. It drops the retired renderers and needs one moved source path.

**Mechanism caveat for BUG-270.** Its stable key is NEW-AUDIT-27, so it comes from the `added` list. `apply_adversarial` applies `retired` before `added`, so `"retired": {"CNA-BUG-270": ...}` fails with "unknown entry". To retire it, NEW-AUDIT-27 has to be deleted from `added`. That renumbers NEW-AUDIT-28..31, which are now CNA-BUG-271..274, down by one. The other way out is to add an op to the script that runs after allocation.

##### (1) Entries needing action

| published id | stable key | short title | disposition | evidence at T | proposed change |
|---|---|---|---|---|---|
| CNA-BUG-270 | NEW-AUDIT-27 | `@param` lines of `cna_post_process_chain_add_owned_pass` / `cna_skybox_set_owned_environment` | **RETIRE-OBSOLETE** | 5572f3ca1 (MOD-RETIRE-1) deleted `modules/c-api/include/CNA/C/engine_layer.h` (12,039 lines) and `src/CnaCApiEngineLayer.cpp`. `git grep` at T finds neither route name nor the phrase "whether or not the call succeeded" in modules/ or tools/. | Retire as OBSOLETE, giving 5572f3ca1 as the evidence. Because it is an `added` entry, remove NEW-AUDIT-27 from `added` (see the caveat above). |
| CNA-VGAP-055 | CNA-VGAP-055 | Process exit with live EasyGL resources whose creating thread has ended is untested | **RETIRE-FIXED** (PROVEN FIXED) | 0f7166cd8, fix(BINDFIX-041), reproduced the cna-java JAVA-UPSTREAM-014 probe on OPENGLES3 and fixed it. `HandleRegistry::~HandleRegistry()` (modules/c-api/src/CnaCApiDetail.cpp:454 at T) leaves objects that another thread created to the OS. The new test `CApi_ExitWithForeignThreadGameSmoke` (modules/c-api/tests/pure_c/ExitWithForeignThreadGameSmoke.c, registered in modules/c-api/CMakeLists.txt) creates a game and a never-destroyed dynamic vertex buffer on a thread that ends, then exits. The commit records exit 134 before the fix and 0 after on OPENGLES3. Related: 00b9c9898 (KF-1) makes `VertexBuffer::Dispose`/`~VertexBuffer` take `TryLeaseRendererContext()`, and abd005ab8 (CBIND-131) keeps EasyGL's lease state valid during exit-time static destruction. | `"retired": {"CNA-VGAP-055": {"classification": "PROVEN FIXED", "evidence": "BINDFIX-041 (0f7166cd8) reproduced cna-java's exit_with_live_graph case on OPENGLES3 and fixed it: HandleRegistry::~HandleRegistry leaves objects created by another thread to the operating system. CNA now tests it: CApi_ExitWithForeignThreadGameSmoke (ExitWithForeignThreadGameSmoke.c) creates a game and a live dynamic vertex buffer on a thread that ends, then exits; exit 134 before, 0 after (CNA's recorded run). The test is not pinned to a GL renderer and C tests are not run in CI (CNA-VGAP-053)."}}` |
| CNA-BUG-133 | CNA-BUG-133 | Renderers implement the window-to-logical transform but never call `RegisterForWindow` | **CHANGED** | FREEDIRECT was removed by 0f96ea703. 9bbba48d8 (FULLSCREEN-002) added `DirectX9Renderer::TransformWindowToLogical`/`TransformLogicalToWindow` (directx9/src/DirectX9Renderer.cpp:721) without registering. `git grep RegisterForWindow` at T finds no call in directx9, directx11, directx12 or metal. The registrants are Canvas, EasyGL, FNA3D, SDL_GPU, SdlRenderer, Vulkan and WebGPU. The registry comment is still at IGraphicsRenderer.hpp:3866. | **title:** 'DIRECTX11, DIRECTX12, FREEDIRECT and METAL implement' -> 'DIRECTX9, DIRECTX11, DIRECTX12 and METAL implement'. **public_contract:** 'on the DIRECTX11, DIRECTX12, FREEDIRECT and METAL renderers' -> 'on the DIRECTX9, DIRECTX11, DIRECTX12 and METAL renderers'. **expected:** 'Vulkan, EasyGL, OpenGL4, SDL_GPU, WebGPU, FNA3D, the SDL renderer, GDI, Direct2D, Canvas and the DOM renderers call' -> 'Vulkan, EasyGL, SDL_GPU, WebGPU, FNA3D, the SDL renderer and Canvas call'. **actual:** '{{src:modules/renderers/freedirect/src/FreeDirectRenderer.cpp\|FreeDirectRenderer.cpp}}' -> '{{src:modules/renderers/directx9/src/DirectX9Renderer.cpp\|DirectX9Renderer.cpp}} (whose transform FULLSCREEN-002 added)'. **evidence:** '(the Direct3D and FreeDirect renderers are Windows-only, METAL is Apple-only)' -> '(the Direct3D renderers are Windows-only, METAL is Apple-only)'. **blast_radius:** 'Games on DIRECTX11, DIRECTX12, FREEDIRECT or METAL' -> 'Games on DIRECTX9, DIRECTX11, DIRECTX12 or METAL'. **sources:** replace the freedirect row with `{"path":"modules/renderers/directx9/src/DirectX9Renderer.cpp","note":"TransformWindowToLogical / TransformLogicalToWindow (added by FULLSCREEN-002); no RegisterForWindow"}`. |
| CNA-BUG-134 | CNA-BUG-134 | Mouse::GetState reports the raw window coordinate inside a letterbox bar | **EDIT** (defect unchanged) | GlPresentationSurfaceState.hpp moved to modules/renderers/easygl/include/CNA/Internal/Renderers/EasyGL/GlPresentationSurfaceState.hpp (261cb5f7f). `WindowToLogical` there still returns the in-rectangle test (lines 175-211). `SdlGpuRenderer::TransformWindowToLogical` (:4364) and `WebGPURenderer::TransformWindowToLogical` (:12912) still decline. Mouse.cpp `window_to_logical` and SdlInputBridge.cpp `to_logical_position` (:372) still fall back to the raw coordinate. Vulkan (:16487) still returns true with no range check. | **summary:** 'EasyGL (every GL-family identity), OPENGL4, SDL_GPU, WEBGPU, SVG_DOM, HTML_DOM and GDI decline' -> 'EasyGL (every GL-family identity), SDL_GPU and WEBGPU decline'. **expected:** 'Vulkan, Canvas and Direct2D return' -> 'Vulkan and Canvas return'. **actual:** 'modules/graphics/include/CNA/Internal/Renderers/Common/GlPresentationSurfaceState.hpp' -> 'modules/renderers/easygl/include/CNA/Internal/Renderers/EasyGL/GlPresentationSurfaceState.hpp'; '(<code>EasyGL</code>, OPENGL4)' -> '(<code>EasyGL</code>)'; '<code>SDL_GPU</code>, <code>WebGPU</code>, <code>SVG_DOM</code>, <code>HTML_DOM</code> and GDI (<code>MapGdiWindowToLogical</code>) do the same' -> '<code>SDL_GPU</code> and <code>WebGPU</code> do the same'. **evidence:** 'VULKAN, Canvas, <code>Direct2D</code>, FNA3D, the SDL renderer and FREEDIRECT return true without a range check.' -> 'VULKAN, Canvas, FNA3D and the SDL renderer return true without a range check; DIRECTX9's transform (added by FULLSCREEN-002) has no range check either, but DIRECTX9 never registers (CNA-BUG-133).' **blast_radius:** 'on the six renderers named' -> 'on the renderers named (every EasyGL identity, SDL_GPU and WEBGPU)'. **sources:** set path to `modules/renderers/easygl/include/CNA/Internal/Renderers/EasyGL/GlPresentationSurfaceState.hpp` (same note). |
| CNA-BUG-213 | CNA-BUG-213 | `submit_buffer` is documented as safe from a producer thread, but returns `CNA_RESULT_THREAD` | **CHANGED** (default behaviour unchanged; new opt-in) | `BorrowDynamicInstance` still goes through `GetSoundEffectInstance` and `HandleRegistry::Get`, which returns `CNA_RESULT_THREAD` (CnaCApiDetail.hpp:549-550). The audio.h `submit_buffer` Doxygen still makes the producer-thread claim (lines 667-669). AUDIO.md is unchanged. 0a57ccad2 (CBIND-141, ABI 0.39.0) added `cna_game_set_foreign_thread_calls_ext`, off by default, which queues refused calls for the game thread. 23d7bad1e (CBIND-154, ABI 0.43.0) lifted the thread rule only for `cna_sound_effect_play` and `cna_sound_effect_play_with_settings`. | **append to actual:** '<p>Since C ABI 0.39.0 (CBIND-141) a game can opt in with <code>cna_game_set_foreign_thread_calls_ext(game, CNA_TRUE)</code>: a call another thread\'s handle refused is then queued for the game thread, and the producer blocks until <code>Update</code>/<code>Draw</code> or <code>cna_game_run_foreign_thread_calls_ext</code> serves it. The switch is off by default, so the documented producer-thread call still returns <code>CNA_RESULT_THREAD</code>; with it on, submission is serialized through the game thread rather than made concurrently with playback. CBIND-154 (ABI 0.43.0) lifted the creating-thread rule only for <code>cna_sound_effect_play</code> and <code>cna_sound_effect_play_with_settings</code>; the submission routes keep it.</p>'. **append to workaround:** ' Alternatively enable <code>cna_game_set_foreign_thread_calls_ext</code> and accept that each submission waits for the game thread.' |
| CNA-GAP-062 | CNA-GAP-062 | C ABI has no route for N planned public declarations | **CHANGED** | At T, COVERAGE.md shows 469 headers, 8,142 symbols, 7,030 implemented, 15 partial, **656 planned** and 441 N/A. Planned rows by module: graphics 275, content 206, graphics-ext 40, input 30, gamer-services 29, math 27, runtime 19, net 15, audio 10, devices 2, storage 2, media 1. RELEASE_GATE.md: "CNA C ABI 0.44.0", "Not ready", "656 public symbols are still unmapped". In generate_coverage_inventory.py, `owner_task` defaults to CBIND-127 (`UNMAPPED_RUNTIME_SURFACE_TASK`). The CBIND-127/117/120/121/122/125 counts in plans/plan_binding.md are unchanged (320/134/3/1/5/5) and no longer sum to 656. `MODULE_SCOPE` now classifies design, diagnostics and inspector (5572f3ca1), so the generator runs (CNA-BUG-062 looks fixed; that entry belongs to another batch). The StorageTexture2D/Texture2DArray public classes are gone; ShaderPackageEXT and ShaderCodeEXT remain. | **title:** '468 public C++ declarations' -> '656 public C++ declarations'. **summary:** -> 'COVERAGE.md records 656 in-scope public C++ declarations without a C mapping (graphics 275, content 206, graphics-ext 40 and smaller tails in nine other modules), which is why the C ABI release gate reads Not ready.' **public_contract:** 'CNA C ABI 0.29.0' -> 'CNA C ABI 0.44.0'. **actual (full replacement):** '<p><code>COVERAGE.md</code> (469 headers, 8,142 symbols: 7,030 implemented, 15 partial, 441 not applicable) records 656 planned rows: graphics 275, content 206, graphics-ext 40, input 30, gamer-services 29, math 27, runtime 19, net 15, audio 10, devices 2, storage 2, media 1. <code>owner_task</code> in <code>generate_coverage_inventory.py</code> names an open task for every row: CBIND-127 (runtime surface that grew after the binding campaign closed) by default, and CBIND-117, CBIND-120, CBIND-121, CBIND-122 and CBIND-125 for the slices and symbols they own. The per-task counts in <code>plans/plan_binding.md</code> predate the engine-layer retirement and the GamerServices/Net work and no longer sum to the measured figure. A C caller cannot reach these declarations through the ABI; the C++ API provides them.</p>'. **evidence:** 'at 009d40f5; the plan\'s row counts sum to the inventory\'s 468. The per-symbol matrix is generated on demand and could not be generated at this commit, so individual symbols were not listed.' -> 'at b0e97bb1; the module summary sums to 656, as RELEASE_GATE.md reports. The per-symbol matrix is generated on demand and was not generated here, so individual symbols were not listed.'; in the merged paragraph '468 public symbols still unmapped, so the 0.29.0 C ABI' -> '656 public symbols still unmapped, so the 0.44.0 C ABI'. **tests_current:** -> '<p><code>CApiCoverageMatrix</code> and <code>CApiReleaseGate</code> measure the backlog; <code>.github/workflows/c-api-coverage-gate.yml</code> runs the coverage <code>--check</code>.</p>'. **blast_radius:** 'that need the engine-layer storage/array textures, shader packages, CNB Model-v2 decoding or the smaller seams listed' -> 'that need any unbound declaration (for example ShaderPackageEXT/ShaderCodeEXT, CNB Model-v2 decoding or the smaller seams)'. **workaround:** 'in a tree where the generator runs' -> 'with <code>generate_coverage_inventory.py --write</code>'. Sources: all exist at T, no change. |

##### (2) Still valid (20)
- **CNA-BUG-049:** all four sensor headers still declare `Dispose(bool) override` public. `Accelerometer::Dispose(false)` still just forwards to `SensorBase`. The INPUT-EMU-001 diff only adds keyboard-emulation members. `AvatarRenderer::Dispose(bool)` is still protected.
- **CNA-BUG-132:** `use_scancode_mode` is still consulted only at SdlInputBridge.cpp:472 and :646. `Sdl3Keyboard::Update` still calls `SDL_GetKeyFromScancode(..., SDL_KMOD_NONE, false)` at :119. The Keyboard.cpp diff is a Guide filter only. input-fna-fidelity.md:523 still makes the promise.
- **CNA-BUG-135:** the `SetCaptureEXT`, `GetGlobalPositionEXT` and `WarpGlobalEXT` wrappers still have no guard. WaylandMouse (:950/958/966) and TerminalMouse still throw `PlatformNotSupportedException(GlobalPointer)`.
- **CNA-BUG-207:** both MixerEngines still `GAUGE_ADD +1/-1`. Only shutdown sets the gauge to 0, and the `Mode::Off` early returns are unchanged.
- **CNA-BUG-208:** `CNA_DIAGNOSTICS_FRAME_SCOPE` is still inside `EmscriptenMainLoopCallback` (:1277), and `RunLoop` still calls `CNA_WaitForAnimationFrame()` outside it (:1375-1377).
- **CNA-BUG-209:** Agent.cpp:340 still uses `getCurrentGraphicsRendererName()`. The Agent.cpp diff only removes the SDL2 platform-name branch.
- **CNA-BUG-210:** Diagnostics.cpp and Protocol.cpp are unchanged; Agent.cpp changed only for SDL2.
- **CNA-BUG-211:** the Agent `Stop`/`Run`/`HandleClient` code is unchanged apart from the SDL2 lines; InternalSocket.cpp is unchanged.
- **CNA-BUG-212:** the route still calls `BorrowGameGraphicsDevice(parentGame)`, then `GetGame`. `cna_graphics_device_create` still makes the device's own handle the owner token (CnaCApiDisplay.cpp around :861).
- **CNA-BUG-214:** `CNA_RESULT_SHUTTING_DOWN` still appears only in abi.h, `ErrorCategoryForResult`, ERRORS.md, HANDLES.md and the ABI baseline.
- **CNA-BUG-263:** `TerminalMouse::SetPosition` still throws `PlatformException` (:32). `Mouse::SetPosition` still forwards to it unguarded. TerminalMouseTests.cpp still has no `SetPosition` case.
- **CNA-GAP-060:** `IDiagnosticsSource`/`RegisterSource` are used only in the diagnostics module and its tests. `AudioVoice` appears only in Diagnostics.hpp and WebBridge.cpp.
- **CNA-GAP-061:** `IResourcePreviewProvider` appears only in the inspector header, tests and benchmark. The Agent.cpp diff is SDL2 only.
- **CNA-GAP-067:** `AccumulateWheel` still casts to int before multiplying by 120 (Sdl3InputServices.cpp:70-78). The test `WheelEventsAccumulateInXnaUnitsAndTruncateBeforeScaling` is still present.
- **CNA-PLAT-009:** all sources are unchanged between O and T.
- **CNA-VGAP-004:** `CNA_TEST_GAMECONTROLLERDB` is set by no workflow; the only references are the test and plan_x11.md.
- **CNA-VGAP-051:** no workflow or CMakePresets entry sets `CNA_DIAGNOSTICS` or `CNA_BUILD_INSPECTOR`. DiagnosticsTests.cpp and InspectorTests.cpp are unchanged.
- **CNA-VGAP-052:** InspectorTests.cpp and WebBridge.cpp are unchanged; Agent.cpp changed only for SDL2.
- **CNA-VGAP-053:** the c-api-*.yml workflows (abi-baseline, compat-matrix, coverage-gate, limitations, release-gate) still configure no `CNA_BUILD_C_API`. CMakePresets still has it OFF.
- **CNA-VGAP-054:** `cna_graphics_device_destroy` still counts no children. The new ConcurrentDeviceCreationSmoke.c (BINDFIX-050) creates and destroys devices with no resources on them, so the gap stands. Optional append to actual: 'ConcurrentDeviceCreationSmoke.c (BINDFIX-050) creates and destroys devices on several threads but leaves no resource on them.'

##### (3) New issues and leads (outside this batch's entries)
- **CNA-BUG-062 (DOC batch) looks fixed.** At T, `MODULE_SCOPE` in tools/c-api/generate_coverage_inventory.py (lines 91-93) classifies design, diagnostics and inspector as out of scope; this came in with 5572f3ca1. The committed COVERAGE.md lists them, and RELEASE_GATE.md shows only the coverage criterion unmet.
- **Lead for the MEDIA batch; not checked against XNA.** After KF-12 (49119a34c), `SoundEffectInstance` Pitch 2 throws (CApi_AudioSmoke expects `INVALID_ARGUMENT`). But `SoundEffect::Play(volume, pitch, pan)` still clamps pitch (SoundEffect.cpp:560-567, with the comment "Pitch is clamped rather than validated"), and audio.h `cna_sound_effect_play_with_settings` still documents "pitch is clamped". The two paths are inconsistent; whether XNA's `Play` throws was not checked here.

##### (4) Counts
| Disposition | Count |
|---|---|
| RETIRE-OBSOLETE | 1 (CNA-BUG-270) |
| RETIRE-FIXED | 1 (CNA-VGAP-055) |
| CHANGED | 3 (CNA-BUG-133, CNA-BUG-213, CNA-GAP-062) |
| EDIT | 1 (CNA-BUG-134) |
| NARROWED | 0 |
| STILL VALID | 20 |
| **Total** | **26** |

None of the related links in this batch name a removed subject.
