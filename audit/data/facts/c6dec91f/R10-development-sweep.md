# R10 — Development sweep (pages not re-verified at T), CNA B=c1c316b9 → T=c6dec91f

INTERNAL AUDIT RECORD (not served).

Scope: the 67 `development/` pages listed in sections 3 ("delta-edited only", 48) and 4 ("only evidence-wording
changes", 19) of `R4-development.md`. R4 had applied renderer, number, ABI and content-reader facts to them; this pass
swept them for every other behavioural change between B and T.

## 1. Method

* CNA was read, never built or run: `git log/diff/show/grep` between B and T in
  `/rv/data/development/github.com/libcna/cna`, B readings with `git show c1c316b9:…`, T readings in the extracted tree
  `~/.cache/libcna-com/cna-target`. Commit ancestry was checked with `git merge-base --is-ancestor` before attributing a
  change to B..T.
* Per page: the cited CNA paths (source links and paths named in prose) were collected and diffed B..T
  (`scratchpad/r10/paths.py`); for every changed path the commits were read and the touched functions re-read at T; pages
  were also scanned for the topics of the B..T behaviour commits even where the changed file was not cited (content
  ownership/Unload, OpenStream, RootDirectory guard, System exceptions, storage, ResetElapsedTime, browser variable step,
  fullscreen events, lazy capabilities/`Supports()`, `PlatformFactoryDefault.cpp`, LINK-006 dispatcher slots, mixer
  `atexit`, MUSEUM-AUDIO/PHONE/NET repairs, C API ISSUE-050/051 and exit destruction, component lifecycle 031693a9f,
  pipeline ISSUE-047/048, renderer behaviour on HEADLESS/STUB/SOFTWARE). Every test name or identifier a page cites was
  checked to exist at T.
* CNA-DEMOS status from `CNA_DEMOS_REPAIR_MATRIX.json` at T: the nine unclosed fixes (005, 006, 007, 008, 022, 023, 031,
  066, 067) are never called fixed. Where a page touches one (008 on devices, 066 SetBlendEnabled on stub) it says
  "committed at this snapshot, not yet validated by CNA" or describes T without claiming a fix.
* Evidence callouts: a page whose CNA claims were re-checked as a whole was switched to "source-verified at the pinned
  commit … checked by reading the CNA source at commit c6dec91f" (and any "re-read at c6dec91f" partial note was dropped
  or reduced). Pages edited only in part keep the c1c316b9 callout ("at the stated evidence commit"), some with an added
  note naming what was re-read.
* No commit, push, `regenerate_site.sh`, `apply_expansions.py fold`. No `<!--p3:deep-links-->`/`<!--p3:issue-links-->`
  block, sidebar, breadcrumb, pager, dev-layers row or generated hub list was edited; no `<!--p3:begin … end-->` region
  was edited. Nothing in `docs/`, `deep-dives/`, `known-issues/`, `docs/tutorials/`, `development/maintenance.html`,
  `development/handbook/update-libcna-com.html` or the five generated `development/reference/*` pages was touched.
  JSON-LD `dateModified` was set to 2026-10-26 on every page edited in this pass (`build_site_indexes.py` restamps it at
  regeneration anyway).

## 2. Outcome by page

Edited and pinned to c6dec91f after a full re-check (48): internals/modules/{storage,media,devices,devices-ext,net,
gamer-services,core,math,phone,diagnostics,video-ffmpeg,design}, takeover/{case-study-storage,ownership,threading,
case-study-components}, internals/content/{runtime,pipeline}, internals/audio/engine, internals/input/events,
internals/runtime/{frame,shutdown,startup,module}, handbook/{modify-contentmanager,debug-shutdown-and-lifetime,change-map,
add-a-regression-test,change-public-xna-behavior,conventions,investigate-a-sample-failure,modify-the-content-pipeline,
modify-a-platform-backend}, invariants, internals/bindings/c-api-internals,
architecture/{content,runtime,overview,audio-input,platform,bindings}, debugging,
internals/graphics/{headless,stub,software}, internals/platforms/{headless,terminal,index}.

Edited in part, callout kept at c1c316b9 "at the stated evidence commit" (4): internals/platforms/sdl3 (callout note
extended to name the re-read paragraphs), takeover/validation, repository/source-ownership, takeover/mental-model.

Unchanged (15): internals/graphics/easygl, internals/modules/{graphics-ext,inspector},
internals/bindings/{csharp,java,python}, handbook/index, internals/index, reference/index, takeover/index, testing/index,
takeover/{curriculum,investigation,xna-oracle}, workflows. Their claims were checked against the B..T commits and none is
contradicted at T; their callouts keep c1c316b9.

## 3. Per-page record

Format per page: changed cited paths and the commits behind them; what was re-read; page changes; ids; p3 regions.
"ids: none changed" means no `id` attribute was added, removed or renamed. No p3 region was touched anywhere.

### internals/modules/storage
- changed cited: StorageDevice.cpp/.hpp, StorageContainer.cpp/.hpp (5865ae938, 3798787bb, fffa552ad, 17c66a9d3, ac6be8f03, 9c068f632, 4d384865c, c30925496, 162e07b8a, 4dba781c3, 21b4cd64c, a24c75b2e, cd211420e, 657eff838), StorageDeviceTests.cpp (+6 new test sources; 14 -> 70 defs), CnaCApiStorage.cpp/storage.h (generated routes; share forwarded; sharing docs), StorageSmoke.c (+sharing, delete-file, create-dir checks), PathContainment.hpp (comment only), ModuleProbes.cmake/UnitTests.cmake (registrations hold; XmlFree probe added), LocalGamerServicesStore.cpp (leaderboard columns only; root use holds)
- re-read: both storage sources and headers at T, all 7 test sources (names/counts/fixtures), C adapter OpenFileHandle/ShowSelector/DeleteContainer/Destroy, storage.h sharing doc, sharp-runtime 530e217f StoragePaths (resolver, default root) and handoff.md (Sharp Runtime next 530e217f needed; v0.1.0 tag lacks SetIsolatedStorageRootResolver/FileShare)
- page changes: callout -> pinned c6dec91f (Sharp Runtime 530e217f); fake-async diagram; selector validation (player then size, ArgumentOutOfRange; directoryCount unchecked; sentinel 255); End contract (ArgumentNull/InvalidOperation one-shot/Argument owner/ArgumentNull empty name; root resolved not created); root section (ResolveStorageRoot vs EnsureStorageRoot; cwd failure -> StorageDeviceNotConnected; Android GetDefaultIsolatedStorageRootPath; creation only in EnsureStorageRoot); SetAppNameEXT (lazy Sharp Runtime resolver, creates nothing, cannot fail; static unregisters; callers incl. one example); retry callout (tests now pin it; stale "failed SetAppNameEXT override" rule removed); constructor (ArgumentNull/Argument; Directory::CreateDirectory whole chain; IOException/UnauthorizedAccess); authority table rewritten (System exceptions, empty/. DeleteContainer accepted, dangling symlinks, uninspectable components); ResolveNativePath steps (+disposed/empty order, DanglingLinkStaysBelow, lexical fallback); method bullets (System.IO parity; delete type checks; enumeration DirectoryNotFound; empty pattern -> no matches; FileShare honoured, ISSUE-152 platform validation pending); UTF-8 tests note; #deletion rewritten (per-player XNA deletion, nothing created, error mapping, containment the one deviation); GamerServices collision narrowed; ownership table (owner/consumed flag); disposal paragraph (ObjectDisposedException on 15 access paths); C ABI bullets (selector, empty delete title, sharing honoured, CNA_RESULT_IO); #tests rewritten (7 sources/70 defs, per-file content); fixture callout (4 of 7 use real root; TearDown no longer creates game dir); "does not establish" list; change routes (Begin/End, new method); gaps list (3 items rewritten, c1c316b9 -> c6dec91f); IPlatformFileSystem -> IPlatformSystemServices (was wrong already at B); reading route items 2,3,6
- ids: none changed. p3: none.
### takeover/case-study-storage
- changed cited: StorageDevice.cpp, StorageContainer.cpp, StorageDeviceTests.cpp (+6 sources), PathContainment.hpp (comment), PathContainmentTests.cpp (comment), ContentManager.cpp (manifest sidecar resolution moved to BuiltinContentLoaders.cpp, LINK-004/005), PlaylistParser/MediaLibraryIndex/ContentReader (no containment change)
- re-read: helper call sites at T (git grep), DeleteContainer path at T, tests, unit presets, win32_unicode_paths.ps1 exists
- page changes: meta/og/JSON-LD description snapshot c1c316b9 -> c6dec91f (generated copy in search-index.json stale); callout -> pinned c6dec91f; lede; history ancestor + 4 rows for the Oct 2026 repairs; invariant (player folder); review questions; diagram rewritten (ResolveStorageRoot, StorageContainer::DeleteContainer, ResolveBelow, dangling link, not-a-directory return, error mapping); XNA as reference since 162e07b8a; root/latch paragraph; historical test paragraph (exception now ArgumentException; empty/. now XNA deletions); test table (27+4, new names, residual tests, dangling); fixture callout (TearDown creates nothing now); call-site table (ResolveContainedUtf8Path rows, BuiltinContentLoaders link, pipeline bridge); out-of-scope paragraph; limits; route steps (ranges c6dec91f, functions, filters)
- ids: none changed (#test, #limits linked from elsewhere, kept). p3: none.
### internals/content/runtime
- changed cited: ContentManager.hpp/.cpp (cd211420e ObjectDisposed; d7ce398d8/c1006b03e OpenStream routing + RouteLoadsThroughOpenStreamEXT; 583af2a5e root guard + shared ReadXnbHeader + IO wrap; 39ef8ea2f Unload disposal list; bbe2bda7b root discovery + manifest bookkeeping exclusion; dcb9e0978/2a5100d72 declared readers), ContentReader.cpp/.hpp (3d254dfa7 dispatch + shared-resource recording; ResolveRelativeAssetPath renamed detail::ResolveExternalReferencePath), ContentTypeReaderManager.cpp (shared_mutex locks, provisional/withdrawn names, 252e9bca1 target lookup), ContentManagerUntyped.cpp (shares ReadXnbHeader 14-byte guard; LZ4 still refused), ResourceContentManager.cpp (stream-only), CnbLoaderRegistry.cpp (LINK-041 removals; rules hold), CMakeLists (CNA::Zstd), XnbCanonicalData.cpp split (DecodeXnbCanonicalAsset now XnbCanonicalAsset.cpp), ContentSoundEffectLoaders.cpp (loose tier still unwrapped), tests (+stream routing, manifest, dispatch, ownership suites)
- page changes: callout -> pinned c6dec91f (untyped-guard caveat removed); lede (OpenStream, snapshot); Load<T> diagram rewritten (ObjectDisposed, strict option, BuiltinContent install, TryOpenCompiledStream/OpenStream, recording); cache-key paragraph (RootDirectory setter InvalidOperation while cached); XNB-tier paragraph (OpenStream seam, base-miss fallback only, strict mode, tests); path services (platform base path asked regardless of Game; OpenStream); manifest bookkeeping exclusion; header checks shared (ReadXnbHeader); untyped decoder shares guards; canonical decoder link -> XnbCanonicalAsset.cpp; registries table (locks, provisional/withdrawn, target lookup; "TARGET" header); lifetime paragraph (recording on all tiers, shared resources, InvalidOperation on mutation, Model routes, Dispose(bool) clears on throw, derived recorder); tests list (+11 suites); known gaps: OpenStream bullet rewritten, untyped-guard bullet removed, disposal bullet -> Game::Dispose/UnloadContent ordering; reading route item 2
- ids: none changed. p3: none.
### internals/audio/engine
- changed cited: AudioDeviceFactory.cpp (capture provider moved to new AudioRecordingDeviceFactory.cpp, LINK), FrameworkDispatcher.cpp (7d8eba687 LINK-006 installed slots; FrameworkUpdates.hpp new), SoundEffect.cpp/.hpp (5d66bb795 XNA FromStream(Stream) + CNAEXT istream; 39ef8ea2f content ownership; f46e29005 pan-state drain after MixerLock), SoundEffectInstance.cpp/.hpp (6102058bb Stop(false) ExitMixerTrackLoop/ISSUE-114; 514a6a8c2 pan refusal order/ISSUE-073), DynamicSoundEffectInstance.cpp/.hpp (85a23569c disposed guards/ISSUE-038; slot install), Sdl3Mixer AudioMixer.cpp (594d7d328 atexit(DestroyMixer)), Sdl3Mixer MixerEngine.cpp (844e3ce41 mixer-lock publication; loop exit resume), CnaMixer MixerEngine.cpp (ExitMixerTrackLoop), AudioMixer.hpp (comment), TitleContentBytes.cpp (c02d59409 title lookup), platform-ci.yml (4 SDL3-audio cells), tests (+4 files; counts 63->64, 133->135)
- page changes: callout -> pinned c6dec91f; selection paragraph (capture factory file); link-edge paragraph (title lookup, LINK-006 slots); Play/Stop(false) loop exit; Pan order + refusal keeps value; fire-and-forget drain behind MixerLock + exit ordering; dynamic disposed guards + slot install; decode section (XNA FromStream(Stream) vs CNAEXT istream); content route ownership; failure table (FromStream exceptions, IsLooped true only, Pan 3D, disposed rows); no-mixer section; capture factory/slot; DestroyMixer atexit + callout rewritten ("No production caller" -> exit handler; header comment stale); deferred-destruction paragraph (+MUSEUM-AUDIO-001 lock order); dispatcher paragraph (slots); tests table (counts + new row); CMake/CI paragraph (135; four SDL3 cells + Windows job); reading route item 7
- ids: none changed. p3: none.
- CNA doc drift: AudioMixer.hpp:46 says DestroyMixer has no production caller (atexit registration since 594d7d328); FireAndForgetPanState comment says freed in stopped callback (pre-existing).
### internals/modules/media
- changed cited: MediaPlayer.cpp (7d8eba687 media update slot via NotifyDispatcher; 380c32153 ISSUE-058 retained queue; disposed Song -> InvalidOperation), MediaLibrary.cpp (45f704c04 ISSUE-098 disposal guards; a83673fc5 SavePicture read loop), Song.cpp (963970799 ISSUE-015 title-relative FromUri; 45f704c04; 39ef8ea2f content ownership), Album/Artist/Genre/Picture/PictureAlbum/Playlist/collections (ISSUE-098), MediaObjectDisposal.hpp (new), Video.cpp (0562550c3 destruction stops player; File::Exists; FromUriEXT URI/title), VideoPlayer.cpp (abbd8a4ea ISSUE-099/100/101: ArgumentNull/ArgumentException/GetTexture InvalidOperation/Volume range/disposed setters/Stop keeps frame/per-Video track override/association list), PlaylistParser.cpp (comment), StandardFileSystem.cpp (directories not files), UnitTests.cmake (new video suites gated), tests (+MediaDisposalTests, MediaQueueReplayTests, 8 video suites)
- page changes: callout -> pinned c6dec91f; composition paragraph + diagram (media slot); lifecycle table VideoPlayer row; roots "read at c1c316b9" -> c6dec91f; graph paragraph (+ISSUE-098 disposal refusals, Song equality); SavePicture read loop; queue paragraph (disposed Song refusal, retained queue ISSUE-058); dispatcher paragraph (slots); sharp edges (first bullet removed as fixed; partial-fill bullet updated; c1c316b9 -> c6dec91f); Video construction (File::Exists, FromUriEXT URI rules, ISSUE-101 pending platform validation); VideoPlayer Play/OpenDecoder (XNA validation, track override, disposed guards, Volume); GetTexture (InvalidOperation before Play; decoder lives until Play/Dispose/Video destruction); Stop vs CloseDecoder paragraph; ownership paragraph (Video destruction detaches; copies start detached); tests intro/table/config paragraph; unverified callout c6dec91f
- ids: none changed. p3: none.
### internals/modules/devices
- changed cited: sensor headers only (a83673fc5 Dispose(bool) protected on Accelerometer/Gyroscope/Compass/Motion; ec2d8b692 ISSUE-008 [unclosed] Prop.hpp out of reading/event-args headers; 66918da04 AccelerometerReadingEventArgs doc), tests (+SensorHeaderMacroHygieneTests.cpp; static_assert in four sensor tests); Accelerometer.cpp/Gyroscope.cpp/Compass.cpp/Motion.cpp/SensorBase/PlatformSensorSubsystem/VibrateController/DevicesShutdownCoordinator/AndroidSensorBridge unchanged; CMake devices unconditional, presets unchanged, devices-tests.yml filter unchanged (suite census 30 at T)
- page changes: callout -> pinned c6dec91f; boundary paragraph (+Prop.hpp/ISSUE-008 committed, not validated); platform table read-at -> c6dec91f; disposal paragraph (+protected Dispose(bool)); tests intro -> c6dec91f; workflow filter census 7/28 -> 9/30 (+KeyboardAccelerometerTest, SensorHeaderMacroHygiene); unverified callout -> c6dec91f
- ids: none changed. p3: none.
### internals/modules/devices-ext
- changed cited: Camera.cpp (+CameraSupport.cpp), SystemTray.cpp (+SystemTraySupport.cpp), FileDialog.cpp/MessageBox.cpp (Supports(PlatformCapability), LINK-023/029/037), MessageBox.hpp (aff773b3b Return/Escape defaults; Supports doc), SystemTray.hpp (d7ed7592d construction can fail on Linux), IPlatform.hpp (Supports, non-virtual GetCamera/GetTray creating services), Sdl3Camera.cpp/Sdl3ServiceSupport.cpp (subsystem helper moved), Sdl3Tray.cpp (93baa9363 labels), Sdl3SystemServices.cpp (button defaults); tests: suites/counts unchanged (12 suites, workflow filter matches 8)
- page changes: callout -> pinned c6dec91f; diagram line (Supports); wrapper paragraph (Supports, lazily created camera/tray services, *Support.cpp link split); platform table read-at -> c6dec91f; Camera support query; SystemTray (capability vs running host; Linux construction failure); tray label storage; message-box keyboard defaults; unverified callout -> c6dec91f
- ids: none changed. p3: none.
### internals/modules/net
- changed cited: ENetBackend.cpp (a83673fc5 client-role session refuses ClientHello; f59336878 ISSUE-032 SessionNotJoinable reason; 04fb4978a ISSUE-033/MUSEUM-NET-002 welcome state; cd9868526 MUSEUM-NET-001 departed machine excluded; 01534c2e7 simulator moved out), NetworkSimulator.hpp/.cpp (new, sender-side loss/latency), NetPacketCodec.cpp (26b0167f0 flags mapping; welcome state suffix; undefined bits refused), SendDataOptions.hpp (flags enum), LocalNetworkGamer.cpp (option validation; SendDataInternal), NetworkSession.cpp (simulator; due packets first; LocalWithLeaderboards offline flush 8a5e5d8aa; join failure reason), ENetDiscoveryService.cpp (5c60a2028 ISSUE-026 private search socket on all platforms; 494e24d09 ISSUE-018 NetworkNotAvailableException), ENetHostHandle/ENetLibrary (NetworkNotAvailableException), ServiceENetSession/ServiceGamePacketPolicy (flags), third_party/enet protocol.c (5b6aab981 MUSEUM-NET-003), tests (33->35 files, 530->563 defs; +NetworkSimulatorTests, OfflineLeaderboardCommitTests, enet_unsequenced_window_test.c)
- page changes: callout -> pinned c6dec91f (35/563); client-role host comment + ClientHello refusal; Join failure reasons; welcome state/GameStarted replay; receive rules; pump (delayed deliveries removed); SendData (option validation, simulator); delivery-option mapping (flags); migration (departing machine); simulated conditions rewritten (sending side, rules, setter refusals, tests); discovery (private search socket everywhere, NetworkNotAvailableException); error families; leaderboard offline flush; tests list counts and new suites; recipes (simulator test hooks); evidence line -> c6dec91f
- ids: none changed (internal link to #pump-conditions added). p3: none.
- net (later): build paragraph CNA_ENABLE_GAMER_SERVICES (LINK-009), 39 -> 40 sources (NetworkSimulator.cpp), test filtering per option.
### internals/modules/gamer-services
- changed cited: CMakeLists.txt root (CNA_ENABLE_GAMER_SERVICES, 89083f101 LINK-009), modules/CMakeLists.txt, gamer-services/CMakeLists.txt (catalog v3 only, separate deflated catalog library 2487e9062/LINK), LocalGamerServicesStore.cpp (420a4572a ISSUE-085 stream columns), LeaderboardWriter.cpp (8a5e5d8aa ISSUE-025 FlushOfflineWrites), AchievementCollection.cpp (4a756413f ISSUE-077/078 read-only/KeyNotFound), Achievement.cpp + SignedInGamerRequests.cpp (2ac45d2f0 ISSUE-017 EarnedOnline), file splits (LINK-003/012: Guide*, SignedInGamer*, Gamer*, backends), Guide Messages 32 (f3abbd02b), museum profile/auth (ca8633622, 3cd6028b7: not on page), avatars (format 3, catalog v3; page only orients); tests 36->39 files, 637->701 defs; GamerServicesGamerTests 99->106, ServiceTests 57->58; src TUs 65->82; presets unchanged
- page changes: callout -> pinned c6dec91f (39/701); composition paragraph (new option, presets wording); TU count + split note; catalog v3 library; store column types (stream) and failure; LeaderboardWriter persistence (EndGame flush); achievements (read-only, KeyNotFound, EarnedOnline); storage-root link text (GetStorageRootEXT); test counts; Guide sibling files; tour item; avatar orientation (catalog v3); evidence line -> c6dec91f
- ids: none changed. p3: none.
### internals/modules/core
- changed cited: root CMakeLists.txt (CNA_VERSION_PRERELEASE "" since release; page still said alpha pre-release: stale since 10a4ef1cb), core src (+ContentOwnership.cpp: 9 -> 10 TUs; 39ef8ea2f), core tests (+ContentOwnershipTests.cpp: 9 -> 10 files, 106 -> 119 defs), PathContainment.hpp (comment), storage call sites moved to ResolveContainedUtf8Path/ValidateContainedNativePath, content sidecar cache-key in BuiltinContentLoaders.cpp, C API core routes now generated from spec/CoreExt.toml; BuildPerformance unity comment still "eight"; -lembind leftover holds; CnaCApiDetail barrier order holds
- page changes: callout -> pinned c6dec91f; TARGET wording (6 places); headers-only row (+avatar catalog library); version paragraph (empty pre-release, same string as v0.1.0); TU counts 9 -> 10; header table (+Internal/ContentOwnership.hpp); storage exception System::ArgumentException; containment callers table (3 rows); tests 9/106 -> 10/119 + ContentOwnership row; renderer-env note and C ABI paragraph read-at -> c6dec91f; C routes generated from CoreExt.toml
- ids: none changed. p3: none.
### internals/input/events
- changed cited: Game.cpp (96522bf34 fullscreen toggles followed; F9/F10 unchanged), Sdl3InputServices.cpp (0c230d2e9 AM4-320 real warps; 90ae88759 fractional relative delta), MouseCursor (cd211420e exceptions; not on page), HapticDevice (974c1ac08 ctor out of line; not on page), PlatformEvent.hpp (16 alternatives hold; fullscreen WindowEventKind), tests (Sdl3InputServicesTests 41 -> 42; others unchanged)
- page changes: callout -> pinned c6dec91f; WindowEvent row (fullscreen -> IsFullScreen); SDL3 mouse (warp hint; fractional delta); TARGET wording; test count
- ids: none changed. p3: none.
### internals/runtime/frame
- changed cited: Game.cpp (f9747ea49 ISSUE-019 ResetElapsedTime both modes; 90ae88759 browser variable step; 96522bf34 fullscreen toggles; LINK-006 dispatcher slots), GraphicsDeviceManager.cpp (exceptions; BeginDraw gate unchanged), renderers (CanBeginDrawEXT overrides: EasyGL, WEBGPU, DIRECTX9; D3D9 TryBeginDrawEXT), tests (+ResetElapsedTimeTests.cpp 7; GamePlatformTimingTests 11, golden 26 hold)
- page changes: callout -> pinned c6dec91f; tick diagram (wait skipped after reset); ResetElapsedTime paragraph (new); correction callout (second exception); FullscreenEntered/Left row; dispatcher sentence (slots); BeginDraw families (retired "Direct3D families" trace -> WEBGPU and DIRECTX9); Emscripten table (step mode, clock, first update); localizing-frame hint; test table (+ResetElapsedTimeTests)
- ids: none changed. p3: none.
### internals/runtime/shutdown
- changed cited: Game.cpp/.hpp (031693a9f component snapshot; cd211420e ObjectDisposedException; 547c3092a lazy capabilities), ContentManager.cpp (39ef8ea2f Unload disposes recorded objects; refuses disposed manager), GraphicsDeviceManager.cpp (exceptions only; Dispose order unchanged), GraphicsResource.cpp (39ef8ea2f IsDisposed before Disposing, shared content metadata; not on page), GraphicsDevice.cpp (disposal order holds), tests (GamePlatformOwnershipTests 13 -> 15)
- page changes: callout -> pinned c6dec91f; ownership tree capabilities line; Game::Dispose row (snapshot, content disposal, ObjectDisposedException); UnloadContent paragraph (+Content.Unload in UnloadContent throws out of Game::Dispose; repeated Dispose rethrows); explicit teardown diagram lines 1-2; tests row 13 -> 15 + capability tests
- ids: none changed. p3: none.
### internals/runtime/startup
- changed cited: Game.cpp/.hpp (b3e15f645 Depth24 default; 547c3092a lazy capabilities; cd211420e ArgumentNullException in InstallPlatform), GraphicsDeviceManager.cpp (ArgumentNull/Argument), tests (MultiRendererFallbackTests 12 -> 13; others hold)
- page changes: callout -> pinned c6dec91f; construction diagram (capabilities lazy; Depth24); device paragraph (Depth24, lazy capabilities); InstallPlatform exception (2 places); GDM constructor exceptions; fallback test count
- ids: none changed. p3: none.
### internals/runtime/module
- changed cited: Game.cpp/.hpp (lazy capabilities; ObjectDisposedException; ArgumentNullException; ResetElapsedTime both modes; 031693a9f component hooks/snapshot), GameServiceContainer.cpp (ArgumentNull/Argument), GraphicsDeviceManager.cpp (ArgumentNull/Argument), GameComponentCollection.cpp (031693a9f; page statements hold), FrameworkDispatcher (LINK-006), tests (GameTests 18 [page said 9, wrong at B too: 17], GamePlatformTimingTests 11 [page said 9, B had 11], GamePlatformOwnershipTests 15, +ComponentLifecycleCompatibilityTests 9, ResetElapsedTimeTests 7, GameExceptionCompatibilityTests 2)
- page changes: callout -> pinned c6dec91f; dispatcher sentence; ownership tree capabilities; service container and manager exception types; state table ResetElapsedTime; failure model (ObjectDisposedException, ArgumentNullException); extension points (lazy capabilities; component hooks); test table counts + new row
- ids: none changed. p3: none.
### internals/modules/math
- changed cited: all math sources (R6 commit list: 9a5e5d896, 1ad0a3916, 5ab1c7729, e1377c437, bd46b6ffe, 0e7be08e0, e4ddea6e0, 0b03b7b21, 5a44d2c50, 9786d4c93, eef23e6f8, bf209dcbe, 705ea2324, df9234202, 2a245b91f, d753d0997, cd211420e, a83673fc5), tests 27 -> 42 files, 873 -> 957 defs; unity groups unchanged (17 .cpp + 3 internal headers); C barrier arms; geometry.h frustum-ray doc (stale)
- re-read at T: vector magnitudes/Dot/Cross, Matrix hash/ToString/perspective/CheckForNaNs, Color Lerp/Multiply, Vector3 array range checks, frustum Contains/Intersects(Ray)/hash, Curve Evaluate/GetCurvePosition/ComputeTangent, CurveKeyCollection, BoundingSphere helpers, exception throws in all sources, BuildPerformance unity groups, UnitTests (no Xml exclusion)
- page changes: callout -> pinned c6dec91f; lede (snapshot; links to the two deep dives); family table counts + 15 new compatibility suites; test-dir count; Xml.Serialization now everywhere (Windows exclusion removed); perspective rows (ArgumentOutOfRange, order, pi, NaN, aspect 0); wide table header + vector magnitude row; not-wide paragraph; epsilons (users, geometry literals, exact setItem); hashes (XNA integers for value types; geometry still differ); CheckForNaNs NotFiniteNumberException; Color Lerp/Multiply fixed point (NaN keeps first colour; 109 example); failure map (5 rows); C barrier paragraph (+stale geometry.h doc); frustum Contains/Intersects(Ray); curve collection/evaluate/caveats (2 remain: CNA-BUG-028, 065 linked with issue markers); change route; evidence section; TARGET wording
- ids: none changed. p3: none. KI links added: CNA-BUG-028, CNA-BUG-065 (marked).
- CNA doc drift: modules/c-api/include/CNA/C/geometry.h (~731) says cna_bounding_frustum_intersects_ray reports no hit for outside origins / "does not provide full ray clipping" — false since 9a5e5d896.
### handbook/modify-contentmanager
- changed cited: ContentManager.hpp/.cpp (OpenStream routing, ObjectDisposed, root guard, disposal list, header EOF wrap), ContentManagerUntyped.cpp (shared header checks), ResourceContentManager.cpp, content tests (+ContentStreamRoutingTest, ownership suites); test suite names in the owner table verified at T
- page changes: callout -> pinned c6dec91f (registration note folded in); intro snapshot; ladder sentence (ObjectDisposed, strict mode, BuiltinContent install, OpenStream); owner table rows (ownership, OpenStream seam + tests); invariants (OpenStream; root guard; Unload disposes recorded objects); error table (disposed: ObjectDisposedException x3; root change; override refusal; EOF wrap); gaps paragraph (untyped guard fixed); review checklist
- ids: none changed. p3: none.
### takeover/ownership
- changed cited: ContentManager.cpp/ContentReader.hpp (39ef8ea2f disposal list; RecordDisposable defaults to the manager), ContentOwnership.hpp (new), AudioMixer.cpp (594d7d328 atexit DestroyMixer), Game.cpp (031693a9f snapshot), ContentManagerTexture2DXnbTests (assertion holds; first copy now disposed)
- page changes: meta/og/JSON-LD description snapshot c1c316b9 -> c6dec91f (search-index.json copy stale); callout -> pinned c6dec91f; vocabulary table (cache + disposal list row; content-ownership groups); content paragraph rewritten (copies disposed by Unload); mixer generation (atexit); teardown diagram lines 1-2
- ids: none changed. p3: none.
### handbook/debug-shutdown-and-lifetime
- changed cited: Game.cpp (dispose order; ObjectDisposed), ContentManager.cpp (39ef8ea2f), Video.cpp/VideoPlayer.cpp (0562550c3, abbd8a4ea), AudioMixer.cpp (594d7d328), MediaPlayer.cpp (380c32153), StorageContainer.cpp (5865ae938), BuildPerformance.cmake (7a8511d39 float-cast-overflow), ExitWithForeignThreadGameSmoke.c and lsan supp (one-line changes); phone singleton and cna_game_destroy comment unchanged (rows hold)
- page changes: callout -> pinned c6dec91f; intro snapshot; Game::Dispose bullet (+Content.Unload in UnloadContent throws); pointer table (ContentManager row; VideoPlayer/Video row); catalogue rows: mixer (fixed; header comment stale), queue-owned Song (fixed), StorageContainer after Dispose (fixed); sanitizer flags (GCC float-cast-overflow); TARGET wording (TOC entry + h2 text for #tooling, id kept; table header; Valgrind line)
- ids: none changed (#tooling heading text changed, id kept). p3: none.
### invariants
- changed cited: Game.cpp (InstallPlatform ArgumentNullException), XnbCanonicalData.cpp split (float/ADPCM decode now XnbCanonicalSound.cpp, LINK-005), AudioMixer.cpp (atexit DestroyMixer), SoundEffect.cpp (drain after MixerLock); other rules (selection, high-DPI, capabilities, SDL boundary) were re-read at c6dec91f by R4; Dispose order, Present guard, PollEvents order hold
- page changes: callout -> pinned c6dec91f; c1c316b9 mentions (2); InstallPlatform exception; content-pipeline qualification file name; mixer barrier (atexit; MixerLock drain)
- ids: none changed. p3: none.
### handbook/change-map
- changed cited: Game.cpp (ResetElapsedTime, browser variable step, component hooks), ContentManager (Unload, OpenStream), storage sources (DeleteContainer per-player, System exceptions), CMakeLists (CNA_ENABLE_GAMER_SERVICES); all 60 test-suite names on the page verified present at T
- page changes: callout -> pinned c6dec91f; read-at mentions (2); game-loop row (+ResetElapsedTimeTest, reset both modes, browser variable step); component row (+ComponentLifecycleCompatibilityTest, hooks); content row (Unload disposes; OpenStream); storage row (per-player delete, empty/dot, exceptions, more suites); networking row (gamer-services option)
- ids: none changed. p3: none.
### takeover/threading
- changed cited: ContentTypeReaderManager.cpp (shared mutexes + InstallMutex since dcb9e0978/d7ce398d8: XNB registries were unlocked at B), Game.cpp (DeclareBuiltinXnbReaders at construction; Exit bools, component snapshot hold; 031693a9f does not touch the lock path), Sdl3Mixer AudioMixer.cpp (atexit DestroyMixer 594d7d328), Sdl3Mixer MixerEngine.cpp (844e3ce41 callback publication under mixer lock), SoundEffect.cpp (f46e29005 drain after MixerLock), HttpNotificationChannel.cpp (20fe6efd2 listener cancellation; creation-site claim holds), gamer-services job worker moved to QueuedBackend.hpp (creation-site list otherwise unchanged B->T; GamerServicesBackend.cpp still owns event worker), CnaCApiDetail (8 ms, NoteForeignThreadRefusal, GetFromAnyThread hold; ABI 0.50.0 holds)
- page changes: callout -> pinned c6dec91f (2 places), dateModified; map table rows "Mixer teardown" (atexit, publication) and "CNB loader registry" -> "Content registries" (XNB tables locked); SDL3 mixer bullet (atexit, MUSEUM-AUDIO-001 lock order); per-track bullet (drain after MixerLock, exit order); content bullet rewritten (locked registries, declared vs installed, ContentManager unlocked)
- ids: none changed. p3: none. Generated issue-links block still lists retired CNA-BUG-119 (fixed per R5) and CNA-BUG-163 (fixed) -> regenerate.
### internals/bindings/c-api-internals
- changed cited: CnaCApiDetail.cpp/.hpp (0b1eebdb1 DestroyAll at exit, df24c26b3 Windows abandonment; arms table verified unchanged in order at T), CnaCApiRuntime.cpp (9b0f481f5 ISSUE-051 completion hooks after failure + first diagnostic retained; GameDestroy order holds incl. inaccurate comment), spec/Runtime.toml + generated Runtime.inc (128379554 ISSUE-050 dispatch=false owner-only groups), tests/pure_c (93 -> 97 .c: +ContentExceptionSmoke, GameDefaultDepthBufferSmoke, GeneratedRoutesSmoke, MathValueHashSmoke), tests/cpp/OwnerThreadRuntimeTest.cpp (CApi_OwnerThreadRuntime); CnaCApiAudio.cpp (generated boundary refactors; pcm16 route semantics hold); ObjectKind 139 kinds 1..181 hold; 59 TUs / 60 headers / 12 adapter routes / 7 error queries hold; 031693a9f component dispose and 124281bff content root do not touch page claims
- page changes: both evidence callouts -> pinned c6dec91f, dateModified; handles paragraph (+atexit DestroyAll / Windows abandonment); foreign-thread paragraph (+owner-only dispatch=false routes, ISSUE-050); callback-failure paragraph (completion hooks exiting/end_run still run; first diagnostic retained, ISSUE-051); tests table 93 -> 97 pure-C programs
- ids: none changed. p3: none. Generated issue-links block links retired CNA-BUG-067.
### architecture/content
- changed cited: modules/content (ContentManager.hpp/.cpp: OpenStream seam d7ce398d8, RootDirectory guard 583af2a5e, Unload disposal 39ef8ea2f, lazy loose-reader install LINK-004), Game.cpp (DeclareBuiltinXnbReaders holds), modules/content-pipeline (XNB compilation of more types; page's module split and options hold); all 11 named tests present at T
- page changes: callout -> pinned c6dec91f (inline "re-read at c6dec91f" dropped), dateModified; XNB tier (OpenStream); loose readers installed on first load (constructor no longer registers them); RootDirectory setter guard; Unload paragraph rewritten (disposes recorded objects, Dispose(false), ObjectDisposed, new ownership tests)
- ids: none changed. p3: none. Generated issue-links block still lists retired CNA-BUG-021 (Unload fixed) and CNA-BUG-119.
### architecture/runtime
- changed cited: Game.cpp/.hpp (Depth24 b3e15f645; lazy capabilities 547c3092a; ResetElapsedTime f9747ea49; browser variable step 90ae88759; fullscreen 96522bf34; component snapshot 031693a9f; ObjectDisposedException cd211420e), GraphicsDeviceManager.cpp (exceptions only), GraphicsDevice.cpp (Present refusal holds), present_lifecycle_contract_test.cpp (holds); all 10 named tests present
- page changes: callout -> pinned c6dec91f, dateModified; construction diagram (capabilities on first request; Depth24); event reactions (+fullscreen); clock paragraph (+ResetElapsedTime); Dispose paragraph (snapshot, Unload disposes, UnloadContent idiom throws, ObjectDisposed after dispose, repeated-dispose wording); browser bullet (variable step honoured)
- ids: none changed. p3: none. Generated issue-links block links retired CNA-GAP-003.
### architecture/overview
- changed cited: IPlatform.hpp (Supports(), lazy GetTray/GetCamera non-virtual, Vulkan surface service removed; page's service list holds), Game.hpp (holds), cmake selection files (re-read earlier at T), tools/platform (audits hold); ContentManager Unload (39ef8ea2f)
- page changes: callout -> pinned c6dec91f (partial re-read note dropped), dateModified; ownership bullet: Unload disposes recorded objects, kept copies share disposed resources
- ids: none changed. p3: none.
### architecture/audio-input
- changed cited: MixerEngine.hpp (+ExitMixerTrackLoop only), FrameworkDispatcher.cpp (LINK-006 slots; touch direct), Sdl3Mixer AudioMixer.cpp (594d7d328 atexit), AudioPlatformSelection.cmake (doc commits only; NULL/SOUND_ENABLED rule holds), CreateSelectedAudioDevice callers (both mixers) hold, modules/input/tests (counts not on page; InputResetTests.cpp present), docs/input-backend.md (wording)
- page changes: callout -> pinned c6dec91f, dateModified; dispatcher sentence (installed slots, touch direct); lifetime paragraph (+atexit mixer teardown)
- ids: none changed. p3: none.
### architecture/platform
- changed cited: IPlatform.hpp (Supports(), GetCamera/GetTray non-virtual over protected Get*Service, Vulkan service gone — LINK-023/029/035/037), PlatformFactory.cpp (+PlatformFactoryDefault.cpp, LINK-007: Create() constructs the selection directly), PlatformEvent.hpp (16 alternatives hold; fullscreen window event types PLAT-33), docs/platform-abstraction.md (matches), platform-ci.yml (renderer cells/submodules; the 7 gates and the x11-sdl-free subset hold), PlatformRatchet/HotPathLint options hold, tools/platform (budget updates)
- page changes: callout -> pinned c6dec91f (partial re-read note dropped), dateModified; factory paragraph (+PlatformFactoryDefault.cpp, a game calling Create() links only the selection); capability bullet (+Supports(), lazy Game read, lazily created camera/tray). Also overview.html: same factory nuance in the axes paragraph.
- ids: none changed. p3: none.
### architecture/bindings
- changed cited: modules/c-api (see c-api-internals: ISSUE-050 owner-only routes, ISSUE-051 completion hooks + first diagnostic, exit DestroyAll, shared runtime 89fb1493f), tests (93 -> 97 pure-C; 4 -> 5 C++ incl. OwnerThreadRuntimeTest.cpp), CMakeLists (C API still requires CNA_ENABLE_NET; NET now requires CNA_ENABLE_GAMER_SERVICES), docs/c-api/* (CALLBACKS_AND_THREADING +completion rule), abi.h 0.50.0 holds
- page changes: callout -> pinned c6dec91f (re-read note reduced to the cna-dotnet checkout), dateModified; callback-failure sentence (+completion hooks, first message); thread bullet (owner-only routes never queued, ISSUE-050); tests sentence (97 pure-C, five C++ tests incl. CApi_OwnerThreadRuntime)
- ids: none changed. p3: none.
- also c-api-internals: shared-library row +CNA_SHARED_LIBRARY shared runtime (89fb1493f; CApi_SharedRuntime* tests)
### debugging
- changed cited: CMakePresets.json (descriptions/Apple presets only; devices-* sanitizer presets hold), SharedRuntimePolicy.cmake (rule as stated holds), BuildPerformance.cmake (7a8511d39 float-cast-overflow appended to undefined on GCC), AudioDeviceFactory.cpp (capture factory split out; playback factory holds), Sdl3Mixer AudioMixer.cpp (atexit teardown), PlatformFactory.cpp (Create(name) refusal text holds), GraphicsDevice.cpp/Texture2D.cpp (Present refusal, CNA_TEXTURE_TRANSFER_TRACE, CNA_BACKBUFFER_READ_TRACE hold), renderer cmake (messages hold), tools (runner/profile script holds); all 30 identifiers, 7 named tests and parity fixtures present
- page changes: callout -> pinned c6dec91f (partial re-read note dropped), dateModified; lede snapshot c1c316b9 -> c6dec91f; immortal-registries sentence (CnaMixer engine + SDL3 callback holders immortal; SDL3 mixer atexit teardown); sanitizer sentence (+float-cast-overflow on GCC)
- ids: none changed. p3: none.
### handbook/add-a-regression-test
- changed cited: UnitTests.cmake (glob, group dependency tables incl. audio = cna_audio cna_input cna_media, umbrella groups, input filter, glTF rungs hold), TestHelpers.cmake (Vulkan output gate removed — page already says the helper adds none), PixelTestGame.hpp (API names hold), ParityFixtures.cmake (3 registering families hold), CMakePresets.json (unit presets hold), Rectangle.cpp (5a44d2c50 Union aliasing; worked example unaffected), storage tests (fixture still deletes its app-named root; the link target validation#storage holds); 27 identifiers checked present
- page changes: callout -> pinned c6dec91f, lede snapshot -> c6dec91f, dateModified
- ids: none changed. p3: none.
### handbook/change-public-xna-behavior
- changed cited: CLAUDE.md (FNA location, renderer list, coverage rule now names docs/xna-4-runtime-member-coverage.md and handoff.md; XNA-wins tie-break and naming rules hold), CnaCApiColor.cpp (route now generated from spec/Color.toml), Color.cpp (1ad0a3916 lerp/multiply fixed point; float packing rule on page holds), GraphicsAdapter.cpp (widescreen rule/test hold), Harnesses.cmake (strict-API gates hold), census 331/331 and 3627/3627 hold
- page changes: callout -> pinned c6dec91f, lede snapshot -> c6dec91f, dateModified; C ABI ripple row (generated route); coverage-records row (CLAUDE.md rule, generated coverage report, handoff.md)
- ids: none changed. p3: none.
### handbook/conventions
- changed cited: CLAUDE.md (see change-public), CHECKLIST.md ("FNA still wins on semantics" line still there), IAudioDevice.hpp (std exceptions hold), IPlatform.hpp (Supports()), Doxyfile settings hold, DependencyVersions.cmake (sharp-runtime 0.1.0 declared holds), all 12 gates named present; no CTest registers check_cnaext_naming.py or a CNAEXT guard check (holds)
- page changes: callout -> pinned c6dec91f (3 snapshot mentions), dateModified; errors row (+System argument and I/O exceptions); capability recommendation (+Supports())
- ids: none changed. p3: none.
### handbook/investigate-a-sample-failure
- changed cited: StorageDevice.cpp (root chain, lazy creation, browser unavailability: page's storage paragraph holds at T), SoundEffect.cpp (NoAudioHardwareException translation holds), graphics profile messages (IndexBuffer/Texture3D/OcclusionQuery/GraphicsDevice hold), GraphicsRendererSelection (env/fault-injection names hold), fx-compiled-effects.md (renderer-retirement/doc commits; error guide unchanged); external sample pins unchanged
- page changes: callout -> pinned c6dec91f, dateModified (no factual change needed)
- ids: none changed. p3: none.
### handbook/modify-the-content-pipeline
- changed cited: ContentBuildManifest.hpp/.cpp (version 9 -> 10, generatedOutput provenance, a56383319 ISSUE-047), ContentPipeline.hpp/.cpp (3a1437725 ISSUE-048 effective vs requested parameters; 1721b4182 named-only exclusion — page already says so; Freeze/logic_error, MaxContentBuildOutputs 256, XnbWriteLimits hold), XnaPipelineBridge.cpp (AddOutputFile generated outputs), content.cpp (2ce326907 option messages), content-pipeline facade (ContentCompiler writes XNB for more types — not contradicted), glTF children by default (cd1f5ef0a ISSUE-022, unclosed) and cameras (1beef880d ISSUE-023, unclosed) not on this page; all named suites/files present
- page changes: callout -> pinned c6dec91f, lede snapshot -> c6dec91f, dateModified; manifest version 9 -> 10 with meaning; strictness bullet (+ISSUE-048 effective/requested parameters); containment bullet (+AddOutputFile generated outputs, ISSUE-047)
- ids: none changed. p3: none.
### internals/content/pipeline
- changed cited: ContentCompiler.cpp (built-in facade writers for processed Texture2D/Cube/3D, SoundEffect, Song, Video, SpriteFont, CompiledEffect — c17178806, 3453776b7, 230291e6a, c168e141b, 142351dad, 133417b03; AddWriter validate around Initialize — 7864dd5b1), XnaPipelineBridge.cpp (6823af99a XNB writer honours build environment target; identity "2;"), BuildContent.cpp (23a34f986 unreadable previous manifest -> warning, rebuilt), ContentBuildManifest (v10 generatedOutput, requested parameters recorded — a56383319/3a1437725), ContentPipeline.cpp (ISSUE-048 effective vs requested; 1721b4182 named-only exclusion already described), XnbOutputContentPipeline.cpp (cd1f5ef0a ISSUE-022 / 1beef880d ISSUE-023 — both unclosed; not described on this page), CnaContentStaging.hpp (83e611fe1 cross-process coordination; claim holds), CnaToolAtomicWrite.hpp (32cb1a4ed Windows self-copy), content.cpp (2ce326907 message; page's option list holds), intermediate-serializer commits (not on this page)
- page changes: callout -> pinned c6dec91f, dateModified; XnaCompatible bullet (+ISSUE-048); ContentCompiler paragraph (built-in processed-content writers; AddWriter around Initialize); XnaObject XNB writer (build environment target, identity bump); BuildContent (+unreadable previous manifest, ISSUE-047); manifest v9 -> v10, generatedOutput flag, requested parameters
- ids: none changed. p3: region wp12-pipeline-fingerprint-hash not touched.
### handbook/modify-a-platform-backend
- changed cited: IPlatform.hpp (Supports(); non-virtual GetCamera/GetTray over protected Get*Service; LINK-023/029/035/037), Sdl3Platform.cpp (Supports(Camera) starts camera subsystem only when asked; CapabilitiesExceptCamera), PlatformFactory.cpp (+PlatformFactoryDefault.cpp LINK-007), Game.cpp (capabilities lazily read 547c3092a); all 13 conformance cases/variables present
- page changes: callout -> pinned c6dec91f (partial re-read note reduced), lede snapshot -> c6dec91f, dateModified; contract row (+non-virtual camera/tray accessors); selection row (+PlatformFactoryDefault.cpp); stability rule row and its failure note (+Supports(), camera subsystem cost); platform-object row (read once on first request)
- ids: none changed. p3: none.
### internals/graphics/headless
- changed cited: HeadlessRenderer.cpp/.hpp (9b277d451 cube faces bind in multi-target sets, no throw; d73f1aeab TextureCube stores and returns face data + ClassifyTextureCubeFormatEXT; c72fa6b05 MultiSampleAntiAliasing false, 0 samples everywhere, reset applies selected format; 718e428fe WarnAndStub NoOpTexture3DRenderer, ISSUE-104; 4dd8129c2 instanced draws count primitives per instance; 34be9272b SetBlendEnabled override removed — not on page), examples (49 Headless_* holds; resource test now asserts stored cube faces)
- page changes: callout -> pinned c6dec91f, dateModified; plain-throw list (cube-face throw removed); resource paragraph (cube store/readback, cube formats, 3D WarnAndStub null object, RT cube default GetData); SetRenderTargets (cube face takes a slot); SupportsCapability (+MultiSampleAntiAliasing false, 0 samples, reset format); instanced counting; test coverage wording (stored cube faces)
- ids: none changed. p3: none. Generated issue-links block still lists CNA-GAP-012 (PROVEN FIXED per R5).
- OUT OF SCOPE: internals/graphics/backends.html (section 2 page) says SetBlendEnabled is a pure virtual every family defines; at T the renderer interface has no SetBlendEnabled (34be9272b, ISSUE-066 unclosed) — GraphicsDevice::SetBlendEnabled is a CNAEXT device method.
### internals/graphics/stub
- changed cited: StubRenderer.hpp/.cpp (718e428fe WarnAndStub CreateTexture3D -> NoOpTexture3DRenderer; 34be9272b no renderer blend toggle), IGraphicsRenderer.hpp (ReadBackbuffer and DrawInstancedPrimitivesEx defaults hold)
- page changes: callout -> pinned c6dec91f, dateModified; implementation-location sentence (+StubRenderer.cpp CreateTexture3D); frame-call toggles (blend toggle removed from the list); capabilities bullet (+WarnAndStub null volume, ISSUE-104)
- ids: none changed. p3: none.
### internals/graphics/software
- changed cited: SoftwareRenderer.cpp (60019d629 PBR material; 375c8927e shadow reception; f74e0a8f7 IBL; 53aba6ef1 punctual lights; 766d62fbd ISSUE-027 blend ranges; c303d3ad9 ISSUE-113 occlusion; 144d9f909 shadow rows; 8f08a82cc ISSUE-007 and c6dec91fb ISSUE-006 — unclosed, not described on the page), SoftwareSpriteBatch.cpp (3b6a2eaf3 ISSUE-003), examples (154 -> 159 Software_* registrations: +PunctualLight, ImageBasedLighting, Pbr_DegenerateBasis, Pbr_DoubleSided, ShadowSampling)
- page changes: callout -> pinned c6dec91f, dateModified; capability paragraph: "There is no shadow or image-based-lighting reception here" (false since 375c8927e/f74e0a8f7) replaced by the PBR/shadow/IBL/punctual description and the pinning programs
- ids: none changed. p3: none.
### internals/graphics/easygl
- changed cited: EasyGLRenderer.cpp (714bfd9bc MSAA <= 4 promise applied on every surface; b1ec33424 live limits; a6e8104d2/c8722e283/313cd8ae6 cube orientation; 53292f147 float-target readback on GLES; bb6a2f44e PBR declared colours; 3b6a2eaf3 ISSUE-003; 34be9272b ISSUE-066 unclosed), GlProfile.hpp, descriptor; EasyGLTextureRenderer::GetData still DXT-only
- page changes: none — no sentence on the page is contradicted at T (its MSAA, limits, readback and render-target statements are at a level these commits do not change). Callout kept at c1c316b9 ("at the stated evidence commit"); the whole page was not re-verified.
- ids: none. p3: none.
### handbook/index
- hub only; no behavioural claims. Unchanged.
### internals/bindings/{csharp,java,python}
- binding facts are for the bindings' own pinned revisions; the CNA-side route names they cite all exist at T (cna_sprite_batch_draw_mesh_ext is cited as removed in 0.29.0 — correct history). No CNA behaviour change contradicts them. Unchanged; callouts kept.
### internals/modules/phone
- changed cited: HttpNotificationChannel.cpp/.hpp (20fe6efd2 MUSEUM-PHONE-001 Close shuts down the active connection, Windows stop/accept events, listener fd kept until join, INVALID_SOCKET compare, MSG_NOSIGNAL/SO_NOSIGPIPE; ReadRequestBody truncated body / >1 MiB headers -> 400, nothing queued; 3c61c30ef ErrorOccurred ChannelOpenFailed queued for socket/bind/listen/getsockname failures, raised first by DispatchPendingNotificationsEXT), PushNotificationSender.cpp (3078bb41e full send loop, require final 2xx response headers, 1xx skipped, 101/overlong/malformed false), new ChannelErrorType.hpp / NotificationChannelErrorEventArgs, UnitTests.cmake (CnaNotificationLifecycle_* 5, CnaNotificationOpenFailure_* 4, CnaNotificationSender_* 15), phone CMakeLists (Emscripten cna_notification_browser_probe); GoogleTest counts 9+9 hold
- page changes: callout -> pinned c6dec91f (unverified list reduced to the Windows host), dateModified, evidence-level sentence; Open failure bullet (ErrorOccurred); parser callout (400 for truncated body/oversized headers); listener paragraph rewritten (Close cancels incomplete request, Windows events, lifecycle programs, SIGPIPE handling); Close paragraph (wake, shut active connection, join, then close fd, events); dispatch (errors first); sender bullet (acknowledgement rule); Windows bullets (INVALID_SOCKET compare; WSAStartup locations; Windows coverage sentence); tests intro (+3 CTest programs, browser probe)
- ids: none changed. p3: none. Generated issue-links block still lists CNA-BUG-157, 158, 163 (all PROVEN FIXED per R5).
### internals/modules/diagnostics
- changed cited: Diagnostics.cpp (e541a636f thread-context release flag; late event -> producer drop), DiagnosticsTests.cpp (40 -> 41 FULL definitions: +death test); only commit touching the module B..T
- page changes: callout -> pinned c6dec91f, dateModified; thread-exit sentence (+release flag, exit() ordering, test); test table FULL column 40 -> 41
- ids: none changed. p3: none.
### internals/modules/video-ffmpeg
- changed cited: video-ffmpeg VideoDecoder.cpp (a83673fc5 mid-stream resolution change refused), media VideoPlayer/Video (abbd8a4ea ISSUE-099/100/101: missing file ArgumentException before decoder, GetTexture InvalidOperationException when nothing plays, volume refusal; 0562550c3 Video destruction stops player), tests (VideoDecoderTests 21 -> 22, VideoPlayerTests 29 -> 30; seven new video suites excluded with FFmpeg off; disabled-build test now asserts GetTexture throws)
- page changes: callout -> pinned c6dec91f, closing evidence sentence, dateModified; converter paragraph (+size mismatch refusal); failure table (mid-stream size row; missing-file note); disabled-build test sentence (+GetTexture); test counts and coverage sentence
- ids: none changed. p3: none.
### internals/modules/design
- changed cited: MathTypeConverter.hpp (66918da04: doc comments only — supportStringConvert comment now lists Rectangle, Matrix, Plane, BoundingBox, BoundingSphere, Ray as clearing it; CanConvertTo comment), no source or test change in modules/design B..T
- page changes: callout -> pinned c6dec91f, dateModified; "A stale comment" callout rewritten (comment now agrees with constructors/tests since 66918da04)
- ids: none changed. p3: none.
### internals/modules/inspector
- no inspector commits B..T; changed cited files are renderer/build files (renderer facts applied earlier) and Diagnostics.cpp (e541a636f, not described here). Unchanged.
### internals/modules/graphics-ext
- commits B..T are renderer retirements (Vulkan, DirectX 11, modern GPU layer; renderer facts already applied) and 4985e26e7 (GetShaderDialectEXT public enum; not described on the page); selectFor preference order verified at T. Unchanged; callout kept.
### internals/platforms/sdl3
- changed cited: Sdl3EventMapper.cpp (13 -> 15 window event types: FullscreenEntered/Left, 96522bf34/0bf951764), Sdl3InputServices.cpp (0c230d2e9 AM4-320 warp hint; 90ae88759 fractional relative delta), Sdl3Platform.cpp/.hpp (272696e8b haptic discovery lease; Supports()/lazy camera already on page), Sdl3Tray.cpp (93baa9363 label retention — covered on devices-ext page), Sdl3SystemServices.cpp (aff773b3b message-box keyboard defaults — devices-ext page)
- page changes: callout note extended (subsystem, event-mapping and mouse paragraphs re-read at c6dec91f; base kept c1c316b9), dateModified; mouse paragraph (+warp hint, fractional remainder); event mapper (15 window events incl. fullscreen toggles); subsystem paragraph (+haptic discovery lease)
- ids: none changed. p3: none.
### internals/platforms/{headless,terminal,index}
- changed cited: PlatformFactory.cpp (+PlatformFactoryDefault.cpp, LINK-007: Create()/GetDefaultName() construct the selection directly), Headless/Terminal sources (only GetTrayService/GetCameraService renames and the Vulkan accessor removal B..T; null tray/camera hold), Game.cpp (capabilities read on first GetPlatformCapabilitiesEXT), platform-ci.yml (cells OPENGLES3/SDL_GPU/WEBGPU/SOFTWARE hold on index)
- page changes: all three callouts -> pinned c6dec91f, dateModified; headless and terminal selection sentences (default name vs Create() in PlatformFactoryDefault.cpp); index diagram (PlatformFactoryDefault.cpp; capabilities on first request) and new-backend step (+PlatformFactoryDefault.cpp arms)
- ids: none changed. p3: none.
### takeover/case-study-components
- changed cited: GameComponentCollection.cpp/.hpp (031693a9f: try_emplace without replacing, argument retained through ComponentAdded, RemoveItem extracts and holds ownership through ComponentRemoved, Clear live index loop with keepAlive, index validated before duplicate), GameComponent/DrawableGameComponent.cpp (RetainCollectionOwnership in hooks and Dispose; Dispose removes before every Disposed event; Drawable unloads on every explicit disposal), Game.cpp (Dispose owning snapshot), tests (GameComponentCollectionTests +7 cases; new ComponentLifecycleCompatibilityTests.cpp, 9 cases; GameComponentTests/DrawableGameComponentTests still empty); lock table and regression tests hold
- page changes: callout -> pinned c6dec91f, meta/og/JSON-LD description snapshot -> c6dec91f (search-index.json copy now stale), history row and confirm-step command -> c6dec91f, dateModified; ownership paragraph rewritten for T ordering; test sentence (+7 callback-order cases, component side, ComponentLifecycleCompatibilityTests); merge checklist (+ComponentLifecycleCompatibilityTest.*)
- ids: none changed. p3: none.
### takeover/validation
- changed cited: storage tests (7 sources; random containers under the current root in three suites; three suites set XDG_DATA_HOME themselves), UnitTests.cmake (+CnaMixerCallbackPublication_{mix,stopped,stress,reentrant}), Harnesses.cmake (mixer-destroy harnesses hold), FileDialog.cpp (Supports() instead of GetCapabilities(); the page's continuation claims hold), presets (descriptions only), BuildPerformance (float-cast-overflow; page's sanitizer rule holds)
- page changes: dateModified; audio row (+CnaMixerCallbackPublication_*); storage section (whole suite, fixtures' reach, XDG_DATA_HOME for the run). Callout kept at c1c316b9 (page not fully re-verified).
- ids: none changed. p3: none.
### repository/source-ownership
- changed cited: PlatformFactory.cpp/+PlatformFactoryDefault.cpp (LINK-007). Page change: platform-backend row (named construction vs default in PlatformFactoryDefault.cpp), dateModified. Callout kept at c1c316b9 (only this row re-read). ids: none. p3: none.
### takeover/mental-model
- changed cited: Game.cpp (DeclareBuiltinXnbReaders: declared, installed on first load). Page change: control-path diagram line, dateModified. Callout kept at c1c316b9. ids: none. p3: none.
### internals/index, reference/index, takeover/index, testing/index (hubs)
- navigation and summary pages; no claim touched by a B..T behaviour change (reference/index's 10/8/3/3 axis counts hold). Unchanged; callouts kept.
### takeover/{curriculum,investigation,xna-oracle}, workflows
- method pages; the concrete traces (GraphicsDeviceManager::ApplyChanges, Terminal keyboard, C API SoundEffect handle) and oracle facts were checked against B..T commits (GraphicsDeviceManager: exception types only; Terminal keyboard sources unchanged; HandleRegistry lookup order holds; oracle tool changes are a frustum-separation record and comment edits). All named tests present at T. Unchanged; callouts kept.
### Follow-ups made after the validator run
- internals/runtime/startup: factory sentence named kDefaultName (gone at T; LINK-007) -> PlatformFactoryDefault.cpp GetDefaultName()/Create().
- internals/platforms/sdl3: "BrowserMouseWarp" (no such class at B or T) -> VirtualMouseWarp, used under Emscripten and on the wayland driver (pre-existing error).
- handbook/change-public-xna-behavior: coverage file name tripped the vocabulary rule (COVERAGE.md, case-insensitive) -> reworded to "the member report that tools/audit_xna_runtime_surface.py generates under docs/".
- internals/audio/engine (later): atexit sentence +CnaMixerExitOrder_{active,recreate,explicit-close} (594d7d328 added tools/audio/mixer_exit_order_test.cpp); exit callout's caller list (four tools/audio programs). takeover/validation audio row likewise.

## 4. Ids, links and p3 regions

* No `id` was added, removed or renamed on any page. handbook/debug-shutdown-and-lifetime: the visible text of the
  `#tooling` heading (and its TOC entry) changed from "TARGET" wording; the id is unchanged.
* One internal link added: internals/modules/net → `#pump-conditions` (same page).
* No `<!--p3:begin X-->…<!--p3:end X-->` region was edited (internals/content/pipeline's `wp12-pipeline-fingerprint-hash`
  was read and left as it is; it still holds at T).
* Known-issue links added in body text, with markers: internals/modules/math →
  `<!--issue:CNA-BUG-028-->…<!--/issue-->` and `<!--issue:CNA-BUG-065-->…<!--/issue-->` (both open at T).
  `issue_refs.py check`: 11 marked references site-wide, 0 errors.
* No body-text link to a retired known issue was added. The generated issue-links blocks of the edited pages still list
  35 retired entries (for example CNA-BUG-021, 119, 157, 158, 163, 216, CNA-GAP-003, 012); they are what
  `check_dev_page.py` and `validate_site.py` report as broken links on these pages and disappear at regeneration.

## 5. Candidate known issues found (source reading only; nothing executed)

1. **Content.Unload()/Load() in an overridden UnloadContent throws out of Game::Dispose.** `Game::Dispose(bool)`
   (modules/runtime/src/Game.cpp, `void Game::Dispose(bool disposing)`, ~line 1146) disposes `Content_` before the
   graphics-device service; `GraphicsDeviceManager::Dispose(bool)` (GraphicsDeviceManager.cpp ~422–460) raises
   `DeviceDisposing`, whose handler runs `UnloadContent`; `ContentManager::Unload()` (ContentManager.cpp ~364) and `Load`
   now refuse a disposed manager with `ObjectDisposedException` (cd211420e/39ef8ea2f). The common XNA idiom therefore
   throws from `Game::Dispose()`: `isDisposed_` stays false, `Disposed` is not raised, and because the manager sets
   `disposed_` only after raising `DeviceDisposing`, a repeated `Dispose()` raises it again and throws again. Whether real
   XNA orders these differently was not measured. (Documented on internals/runtime/shutdown, architecture/runtime,
   internals/content/runtime, handbook/debug-shutdown-and-lifetime.)
2. **Storage test fixtures reach the real per-user data root.** `StorageDeviceDeleteContainerTest` (StorageDeviceTests.cpp)
   sets the app name `CnaTestsContent002StorageDevice` under the real data root and `remove_all`s it in TearDown; the
   asynchronous-contract, lifetime and path-error suites create random containers under `<data root>/game`. Only three of
   the seven storage sources set `XDG_DATA_HOME` to a temporary directory, and the `CnaTests` registration sets no storage
   environment.
3. **CNA comments contradicting T behaviour** (doc drift; candidates for a comment-accuracy KI or for CNA-BUG-222's family):
   * modules/audio/include/CNA/Internal/Audio/AudioMixer.hpp (~line 46): says nothing calls `DestroyMixer` in production;
     since 594d7d328 the first mixer creation registers it with `std::atexit`.
   * modules/audio/src/Xna/SoundEffect.cpp: a `FireAndForgetPanState` comment still says the state is freed in the stopped
     callback; it is queued and drained after `MixerLock` (f46e29005).
   * modules/c-api/include/CNA/C/geometry.h (~line 731): says `cna_bounding_frustum_intersects_ray` reports no hit for an
     outside origin / does no full ray clipping; false since 9a5e5d896.
   * modules/c-api/src/CnaCApiRuntime.cpp `GameDestroy` (~line 840): the comment after `game->Shutdown()` says the canonical
     graphics device was disposed; `Game::Dispose(true)` never disposes it (the device raises `Disposing` from its
     destructor).
   * cmake/BuildPerformance.cmake: the unity-build comment still says "eight core sources" (core has ten at T).
   * The `CApi_StorageSmoke` registration comment ("derived from platform preference path"), in the CNA-BUG-242 family.
4. Still open at T and already recorded elsewhere (no new KI): CNA-BUG-164 (notification listener spins without backoff on
   a persistent accept error) — the loop is unchanged at T; CNA-BUG-028 and CNA-BUG-065 (curve caveats, linked on the
   math page).

Possible status changes for the known-issues owner (not edited here): CNA-VGAP-058 ("no dedicated test drives the
production audio shutdown path") — 594d7d328 added `tools/audio/mixer_exit_order_test.cpp` registered as
`CnaMixerExitOrder_{active,recreate,explicit-close}`; CNA-GAP-012 (HEADLESS TextureCube) and CNA-BUG-157/158/163 (phone) are
already PROVEN FIXED in R5.

## 6. Out-of-scope findings (not edited)

* internals/graphics/backends.html (R4 section 2, re-verified page): says `SetDepthTestEnabled` is pure virtual "like
  SetBlendEnabled", with Headless counting and tracing it. At T the renderer interface has no `SetBlendEnabled`
  (34be9272b, CNA-DEMOS-ISSUE-066, unclosed); `GraphicsDevice::SetBlendEnabled` is a CNAEXT device method.
* search-index.json: the descriptions of takeover/case-study-storage, takeover/ownership and takeover/case-study-components
  still say "c1c316b9"; their meta/og/JSON-LD descriptions now say c6dec91f. Regeneration fixes the index.
* development/testing/index.html: its generated dev-layers row links `../internals/graphics/vulkan.html#validation`
  (retired page; `validate_site.py` reports the fragment). Regeneration.
* Generated issue-links/deep-links blocks on the edited pages: retired KI entries (section 4) and deep-dive descriptions
  that still quote "ABI 0.46.0", "14 public renderer identities" or "12 renderer families" (flagged by `check_facts.py`
  and `check_retired_renderers.py`; all inside generated blocks).

## 7. Open doubts

* The B..T storage behaviour depends on Sharp Runtime `next` ≥ 530e217f (`SetIsolatedStorageRootResolver`, `FileShare`);
  the v0.1.0 Sharp Runtime tag lacks them. The storage page says so; whether the site's build instructions pin the right
  Sharp Runtime revision was not checked.
* CNA-DEMOS-ISSUE-152 (`FileShare` on Windows/non-locking filesystems) and ISSUE-101 (video) are closed in the matrix but
  record pending platform validation; the pages say "platform validation pending" rather than "verified".
* internals/graphics/easygl was not fully re-verified; it was checked only against the B..T EasyGL commit list
  (MSAA ≤ 4 promise, live limits, cube orientation, float-target readback on GLES, PBR colours), none of which contradicts
  its text. Its callout stays at c1c316b9.
* Thread and phone shutdown behaviour against a stalled peer on native Windows is covered only by the MinGW-w64 build of
  the lifecycle program (CNA's record says Wine); the phone page keeps "native Windows unverified".

## 8. Validators (run 2026-10-26 on the working tree; filtered to the 52 edited pages)

* `check_dev_page.py` on all 52: no error other than the generated-block broken KI links listed in section 4 (55 link
  occurrences, 35 distinct targets, every one verified to sit inside a `p3:issue-links` or `p3:deep-links` block); warnings
  only for historical "alpha.1" mentions (case-study-storage, case-study-components, investigate-a-sample-failure).
  One vocabulary error introduced in this pass (a file name containing "coverage.md" on handbook/change-public-xna-behavior)
  was fixed.
* `check_dev_claims.py`: 96 pages, 0 errors, 59 warnings site-wide (it ran; R4's dead-SNAP note no longer applies). On the
  edited pages the warnings are wildcard or abbreviated tokens (`Headless_*`, `_run_one_frame`, `CNA_CURVE_*`, the refused
  `CNA_PLATFORM_SDL12/EMSCRIPTEN`), one hypothetical test name in a worked example, and two real stale names that were then
  fixed: `kDefaultName` (internals/runtime/startup, gone with LINK-007) and `BrowserMouseWarp` (internals/platforms/sdl3; the
  class is `VirtualMouseWarp` at B and T, used under Emscripten and on the wayland driver).
* `check_facts.py`: 20 problems site-wide; on the edited pages only generated-block deep-dive descriptions
  (`ABI 0.46.0`, `14 public renderer`, `12 renderer families`).
* `check_retired_renderers.py`: hits on the edited pages are all inside generated blocks (verified by line).
* `check_retired_platforms.py`: 0. `check_source_links.py`: ok (2549 TARGET-pinned CNA links).
* `validate_site.py`: on the edited pages only the generated-block KI links above; site-wide also the search/sitemap
  coverage mismatches and the testing/index dev-layers fragment (regeneration).
* `issue_refs.py check`: 11 marked, 0 errors.
