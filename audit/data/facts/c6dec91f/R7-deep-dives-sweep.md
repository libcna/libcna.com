# R7 — Deep Dives sweep (pages not re-verified at T), CNA B=c1c316b9 → T=c6dec91f

INTERNAL AUDIT RECORD (not served).

Scope: the 56 Deep Dives listed in section 2 of `R2-deep-dives.md` other than the five math pages owned by R6 and the
tombstones. Some services pages were last verified at `b0e97bb1`, not at B; their diffs were read from that base.

## 1. Method

* CNA was read, never built or run: `git log/diff/show/grep` at B (or `b0e97bb1`) and at T in
  `/rv/data/development/github.com/libcna/cna`. `~/.cache/libcna-com/cna-base` is alpha.1, not B, so every B reading used
  `git show c1c316b9:` or `git grep … c1c316b9`.
* Per page: cited CNA paths collected from the page's source links; `git diff --stat B..T` on them; `git log` of the changed
  files; the changed functions re-read at T, plus any uncited file a statement depended on (e.g. `ContentModelLoaders.cpp`,
  which received the loose readers that `ContentManager.cpp` lost in LINK-004/005).
* CNA-DEMOS repair status taken from `CNA_DEMOS_REPAIR_MATRIX.json` at T. The nine unclosed fixes (005, 006, 007, 008, 022,
  023, 031, 066, 067) are never called fixed: where a page describes one (005, 007, 008, 023, 031, 066) it says "a change
  committed at this snapshot that CNA has not yet validated" or equivalent.
* sharp-runtime: the local clone (`next` 4e146b90) was read only with `git ls-tree/show` to resolve CNA's sharp-runtime
  includes at 41b918c9 and at `next`; sharp-runtime statements on the four sharp-runtime pages stay attributed to 41b918c9.
* Every page whose CNA claims were re-checked had its evidence callout switched to "source-verified at the pinned commit …
  checked by reading the CNA source at commit c6dec91f". All 56 pages were re-checked; none kept "at the stated evidence
  commit". Historical mentions of c1c316b9 that remain are dated provenance (records read at B and removed since).
* No commit, push, `regenerate_site.sh`, `apply_expansions.py fold`; no `<!--p3:deep-links-->`/`<!--p3:issue-links-->` block,
  sidebar, breadcrumb, pager or hub list edited; nothing in `development/`, `docs/`, `known-issues/` or top-level pages edited.

## 2. Per-page record

Each entry: cited paths changed B..T and what was re-read ("changed cited"), what the page now says ("page changes"),
evidence status (all: pinned commit c6dec91f), ids removed (none unless stated) and p3 regions touched.

## services/touch-and-gestures (base b0e97bb1)
- changed: TouchCollection.cpp, TouchPanel.cpp, TouchEdgeCaseTests.cpp (cd211420e only); headers unchanged; FrameworkDispatcher rewritten LINK-006 (touch update unchanged)
- re-read: TouchPanel/TouchCollection/GestureDetector/FrameworkDispatcher/Game.cpp:448, GraphicsDevice display size, GuideDialogs suppress, test names
- changed: operator[] exception std::out_of_range -> System::ArgumentOutOfRangeException (+RemoveAt/Insert/CopyTo); callout -> c6dec91f
## services/input-model (base b0e97bb1)
- changed: MouseCursor.cpp (cd211420e), Game.cpp (PollEvents fullscreen events, F9/F10 same), Sdl3InputServices.cpp (MSR-040 Wayland virtual warp, AM4-320 warp hint, 90ae88759 fractional relative delta), tests
- changed on page: FromTexture2D both ArgumentException; SetPosition row (Wayland anchor, warp-emulation hint); 49/538 -> 50/540; fragment provenance; callout -> c6dec91f
## services/gamepads-and-haptics (base b0e97bb1)
- changed cited: docs/platform-input-notes.md (Wayland warp wording), Sdl3InputServices.cpp (mouse/haptic enumeration only), Sdl3EventMapperTests.cpp (+fullscreen test), SdlHapticBackendTests (comment); HapticDevice ctor out of line (974c1ac08)
- re-read gamepad slot/normalization/deadzone/ext/haptics/power/sensors code at T; CNA_DEVICES default OFF; CnaInputSensorsTest
- no factual change; callout -> c6dec91f; fragment provenance b0e97bb1; p3 wpb5-evdev-controller-mappings "Checked by reading at c1c316b9" -> c6dec91f
## services/host-devices (base b0e97bb1)
- changed cited: CMakeLists.txt (option unchanged), Camera.cpp (+CameraSupport.cpp), MessageBox.cpp (Supports()), Sdl3Camera.cpp (EnsureCameraSubsystem moved to Sdl3ServiceSupport.cpp, LINK-023/029/037), Sdl3SystemServices.cpp (aff773b3b Return/Escape defaults), Sdl3Tray.cpp (MUSEUM-TRAY-001 labels), SystemTray.hpp doc (d7ed7592d)
- page changes: 10 -> 12 sources; SDL3 message box marks first Return/last Escape default (Zenity may ignore); SystemTray PlatformException even when supported (Linux session bus/StatusNotifier); camera subsystem paragraph re-pointed to Sdl3ServiceSupport.cpp, service created on GetCamera(), Sdl3PlatformTests now pin; callout -> c6dec91f
## services/media-contract (base b0e97bb1)
- changed cited: ContentManager.cpp (Song reader moved to ContentMediaLoaders.cpp), Song.cpp (963970799 title-relative FromUri, 45f704c04 disposal guards, ownership 39ef8ea2f), MediaLibrary (a83673fc5 SavePicture loop, 098), VideoPlayer/Video (abbd8a4ea 099/100/101, 0562550c3), VideoDecoder (mid-stream resolution refusal)
- page changes: FromUri relative->title dir; ToString source comment; new Disposal bullet; fragment comment; Song reader link -> ContentMediaLoaders.cpp; SavePicture stream loop; Video: null/missing-file/resolution refusals, disposal guard list incl getters/setters, Volume range, Stop keeps frame, GetTexture InvalidOperation, Video destruction, per-Video track override; callout -> c6dec91f
- note: matrix 101 RESOLVED_PENDING_PLATFORM_VALIDATION (URI resolution) - page states code only
## services/sensors-and-vibration (base b0e97bb1)
- changed: Accelerometer/Gyroscope/Compass/Motion.hpp Dispose(bool) protected (a83673fc5; CNA-BUG-049 retired); reading headers drop Prop.hpp (ec2d8b692, ISSUE-008 unclosed); comments only elsewhere
- page changes: meta description (meta/og/JSON-LD) "the open Dispose(bool) defect" -> "disposal"; lede; h2 #lifetime text + TOC "Lifetime, concurrency and disposal" (id kept); warn callout rewritten; fragment provenance; callout -> c6dec91f
- generated copies of old description now stale: deep-dives/services/index.html hub, docs/sensors.html, docs/tutorials/50-accelerometer.html, development/testing/architecture.html, development/internals/modules/devices.html, development/architecture/platform.html, search-index.json
## services/sound-effects-and-streaming (base b0e97bb1)
- changed cited: SoundEffect.cpp/.hpp (5d66bb795 FromStream(Stream), ownership), SoundEffectInstance.cpp (514a6a8c2 pan order, 6102058bb loop tail), DynamicSoundEffectInstance.cpp (85a23569c disposed guards, LINK-006 install), Microphone.cpp (install), XnbCanonicalData.cpp (LINK-005 split -> XnbCanonicalSound.cpp), ThirdPartySDL.cmake (SDL3_image removed; mixer options same)
- page changes: construction "five sources" with XNA FromStream(Stream) + CNAEXT istream; XNB decode link -> XnbCanonicalSound.cpp; TARGET wording; p3 wpb5-microphone-device-order "Checked by reading at" -> c6dec91f; callout -> c6dec91f
## services/text-input-and-ime (base b0e97bb1)
- changed cited: TextInputEXT.hpp (CNAEXT position only); TextInputEXT.cpp, Clipboard.cpp, bridge unchanged; SDL3 text input/primary selection read at T
- page changes: callout -> c6dec91f; TARGET provenance wording (3 places)
## services/xact-runtime (base c1c316b9)
- changed cited: WaveBank.cpp (3c67874ba, 783fe5739 ISSUE-028), XactParser.cpp (stream overload); TitleContentBytes.cpp (c02d59409 AM4-321 title lookup); AudioEngine/SoundBank/Cue/AudioCategory unchanged
- page changes: loading paragraph (title lookup for xgs/xsb, WaveBank cwd absolute + header check); failure table WaveBank rows (FileNotFound both; ArgumentException header; InvalidOperationException metadata); streaming retained file; "at c1c316b9" -> c6dec91f; callout -> c6dec91f
## services/network-sessions (base c1c316b9)
- changed cited: ENetBackend.cpp (a83673fc5 client refuses hello; f59336878 SessionNotJoinable; 04fb4978a welcome state; cd9868526 migration excludes departed machine; 01534c2e7 simulator moved), NetPacketCodec (26b0167f0 flags), ENetDiscoveryService.cpp (5c60a2028 private reply socket all platforms; 494e24d09 NetworkNotAvailableException), NetworkSession.cpp, harness
- page changes: join errors (SessionNotJoinable produced), ServerWelcome row (+Playing state suffix), discovery (private search socket everywhere, Apple per-interface; NetworkNotAvailableException), discovery-hardening (property index 0-7, max 8, no dup -- was stale 256 even at B), trust (+client refuses hello), delivery table rewritten for flags (Chat alone best effort; undefined bits ArgumentOutOfRange), PacketWriter doc still says floats (Reader fixed), migration successor excludes departed machine; retry rationale; conditions rewritten (sender side, Reliable exempt, normal latency, queues, setter refusals); evidence 524 record now history + 526/526 (a83673fc5); callout -> c6dec91f
- KI: CNA-BUG-267 still holds at T (HandleClientHello sends welcome before AddRemoteGamer)
## services/gamer-services-contract (base c1c316b9)
- changed cited: LocalGamerServicesStore.cpp + LeaderboardWriter.cpp (420a4572a ISSUE-085 stream columns; 8a5e5d8aa ISSUE-025 EndGame flush), docs/gamer-services-known-limitations.md, GamerServicesDispatcher/Guide (LINK-003/012, AM4-323, messages 32), CMakeLists (CNA_ENABLE_GAMER_SERVICES); achievements collection read-only/KeyNotFound (4a756413f), EarnedOnline (2ac45d2f0) not stated on page
- page changes: build option paragraph (CNA_ENABLE_GAMER_SERVICES default=NET, NET requires it), iOS presets; status table leaderboards; offline stream columns kept (256 B hex); EndGame flush; callout -> c6dec91f (audit record still "at c1c316b9")
## services/avatars (base c1c316b9)
- changed cited: docs/avatars.md (format 3, catalog v3 only rev 4), known-limitations (§33 review 2026-10-15, §40-42), AvatarDescriptionCodec.cpp (format 3), AvatarRenderer.cpp (device resources AV3X-18, per-material highlight), SkinnedModelEXT.hpp (+DiffuseColor UB-002), ContentManager.cpp -> ContentModelLoaders.cpp (reader; stride must be 52 af11b2ce5; diffuseColor), convert_avatar.py (UB-001/002/003), GlStockShaderSources.hpp, examples CMake
- page changes: two-systems table rows; description encoding (formats 1-3, catalog >=3); non-CNA buffer list; CreateRandom; Device resources; Versions rewritten (v3 only, rev 4 counts); later-catalog packs; editor build gating; lighting highlight; PartEXT DiffuseColor; reader link + manifest table + validation; converter; visual limits; evidence review record 2026-10-15 (8 identities incl. DIRECTX9/D3D12 under Wine); demos vs review/editor gating; p3 wpb6-avatar-regression-floor (date 2026-10-15, Read at c6dec91f); callout -> c6dec91f
## framework/game-class-and-lifecycle (base c1c316b9)
- changed cited: Game.cpp/.hpp (b3e15f645 Depth24, dcb9e0978/2a5100d72 declared readers, 547c3092a lazy capabilities, 96522bf34 fullscreen, 90ae88759 browser variable step, 031693a9f component dispose, f9747ea49 ResetElapsedTime, cd211420e exceptions), GameTests.cpp; renderers (F9/F10 overrides still EasyGL/DIRECTX9/WEBGPU; WebGPU refusal holds, CNA-BUG-078)
- page changes: constructor paragraph (Depth24; readers declared); GetPlatformCapabilitiesEXT lazy; null platform ArgumentNullException; disposed -> ObjectDisposedException (2 places); exceptions paragraph recount 23 -> 31 with types (method reproduces 23 at B); browser variable step; porting list (ResetElapsedTime and component-removal items removed); main() sample provenance "headers at c1c316b9"; callout -> c6dec91f
## framework/services-and-components (base c1c316b9)
- changed cited: GameComponent.hpp/.cpp, DrawableGameComponent.cpp, GameComponentCollection.cpp, Game.cpp (031693a9f component lifecycle), GameServiceContainer.hpp/.cpp (cd211420e), GameComponentCollectionTests (25->34), new ComponentLifecycleCompatibilityTests.cpp (9)
- page changes: setter/hook order now XNA (override can suppress); drawable UnloadContent on every explicit Dispose(true), flag not reset; #disposed-components rewritten (heading "Disposal unregisters", id kept); service exceptions ArgumentNull/Argument; second manager ArgumentException; evidence counts; callout -> c6dec91f
- game-class page link re-pointed #disposed-components -> #drawable-content
## framework/exit-and-shutdown-semantics (base c1c316b9)
- changed cited: Game.cpp (031693a9f snapshot dispose), GameComponent.cpp/DrawableGameComponent.cpp/GameComponentCollection.cpp (031693a9f), ContentManager.cpp (39ef8ea2f Unload disposes assets, throws ObjectDisposed when disposed; cd211420e), GraphicsDeviceManager.cpp (exceptions only), GameTests
- page changes: Dispose steps (snapshot; content disposes assets); game UnloadContent note (Content.Unload/Load throw ObjectDisposedException); XNA comparison rows (iteration, content, component own Dispose); consequences rewritten (Content.Unload in UnloadContent throws; no index shift); throwing paragraph; test statement; components-at-shutdown fact 1; main() provenance; callout -> c6dec91f
- CANDIDATE KI: Content.Unload() called from UnloadContent() during Game::Dispose() throws System::ObjectDisposedException (Game.cpp:1167 disposes Content_ before the device service whose DeviceDisposing calls UnloadContent; ContentManager.cpp:364-367 Unload refuses a disposed manager). XNA's DeviceDisposing handler unloads Content itself and Game.Dispose does not dispose Content, so the common XNA idiom works there. Result in CNA: exception out of Dispose(), game never marked disposed, Disposed never raised; repeated Dispose() rethrows.
## framework/game-time-and-timestep (base c1c316b9)
- changed cited: Game.cpp (f9747ea49 ResetElapsedTime both modes, consumes stale time, clears slow history; 90ae88759 browser variable step), new ResetElapsedTimeTests.cpp (7 cases, XNA oracle recorded by CNA); GraphicsDevice/GDM swap interval unchanged in substance
- page changes: TOC + h2 #reset-elapsed-time text ("discards the stale time", id kept); section rewritten (old decompile-based XNA deferral analysis removed); lede; variable-step IsRunningSlowly; hysteresis code block; xna-slowly test sentence; browser bullets (variable step honoured); evidence; fragment provenance; callout -> c6dec91f
## framework/window-and-device-manager (base c1c316b9)
- changed cited: GraphicsDeviceManager.cpp (cd211420e exceptions), GameWindow.cpp/Sdl3Window.cpp (96522bf34 re-centre, fullscreen follow), LaunchParameters (b086814f9 XNA parsing, duplicate Add throws; tests 12->15), TitleContainer.cpp (5ccb70808, cbb77e3c8 XNA failures), FrameworkDispatcher.cpp (LINK-006 installed slots), GraphicsDevice.cpp (TryBeginDrawEXT gate, DIRECTX9 d0cea7036)
- page changes: BeginDraw gate; GDM exceptions; IsFullScreen follows window-system toggles; LaunchParameters rules; TitleContainer failures; FrameworkDispatcher; fragment provenance; p3 wpb5-mobile-backbuffer-orientation "Checked by reading at" -> c6dec91f; callout -> c6dec91f
## framework/first-game-walkthrough (base c1c316b9)
- changed cited: SpriteBatch.hpp (docs/binding), Texture2D.hpp (copy/ownership), Rectangle.cpp (hash/union), Game.cpp; used ctors/overloads unchanged (Texture2D(path, device) CNAEXT, Draw(tex,float,float) CNAEXT); IntersectsAdjacentRectanglesReturnsFalse present; .xnb > .cnb > loose order holds
- page changes: callout -> c6dec91f with sample provenance; evidence wording (no TARGET)
## framework/math-coordinate-conventions (base c1c316b9)
- changed cited: Quaternion.cpp (hash/Length/Normalize precision/NotFiniteNumber; Lerp/Slerp structure same), Matrix.cpp, Vector3.cpp, BoundingFrustum.cpp (R6: conventions hold), GlStockShaderSources.hpp, EasyGLRenderer.cpp, SoftwareRenderer.cpp (depth remap, ToColumnMajor uploads, ClipPlaneDistance, BuildPositionColorClipVertex, SDL_GPU sprite y-negation verified); tests named all present; quaternion order still unpinned
- page changes: TARGET wording (lede, depth, example provenance, evidence); callout -> c6dec91f
## content/contentmanager-resolution-rules (base c1c316b9)
- changed cited: ContentManager.hpp/.cpp (583af2a5e root guard + IO wrap; d7ce398d8/c1006b03e OpenStream routing; 39ef8ea2f disposal list/Unload; cd211420e ObjectDisposed; bbe2bda7b root discovery), ContentTypeReaderManager.cpp (dcb9e0978 locks; 252e9bca1 target lookup), ContentReader.cpp (3d254dfa7 dispatch, IO wrap), Game.cpp, TitleContainer.cpp (cbb77e3c8)
- page changes: SoundEffect specialisation location; XNB tier via OpenStream; cache identity root rule (setter refuses while cached); disposal list; Unload/Dispose rewritten (disposes, ownership copies, exceptions); setContentProperty copies disposal list; seams paragraph rewritten (Load uses OpenStream, RouteLoadsThroughOpenStreamEXT, ResourceContentManager); TitleContainer refusals; failure table rows (disposed, EOF wrapped, Song companion wrapped); threads (registries locked); porting bullets; sample comment; evidence test list; callout -> c6dec91f
- retired KIs reflected: CNA-BUG-021, CNA-BUG-119, CNA-BUG-121
## content/xnb-container-and-object-graph (base c1c316b9)
- changed cited: ContentReader.hpp/.cpp (3d254dfa7 XNA dispatch, existing-instance identity, recording; 583af2a5e IO wrap), ContentTypeReader.hpp, ContentTypeReaderManager.cpp (dcb9e0978 locks, 252e9bca1 target lookup), XnbCanonicalData.cpp -> XnbCanonicalAsset.cpp (LINK-005), ContentManager.cpp/Untyped (shared header validation), tests
- page changes: total-length (shared 14-byte guard; importer link), null index = default(T), explicit-reader overloads, existing-instance identity rule, ReadExternalReference template, disposal recording rewritten (h3 text "Disposal recording", id kept), registry locking, p3 wpb4-xnb-extension-proof (Game declares; "Checked by reading at" -> c6dec91f), evidence; callout -> c6dec91f
## content/xnb-type-readers (base c1c316b9; R6 edited sphere sentence)
- changed cited: XnbCanonicalData.cpp split into XnbCanonical{Textures,Sound,Model,Asset}.cpp (b328826af LINK-005); readers themselves unchanged except one line; Song wrap (583af2a5e); VideoPlayer::Play missing file ArgumentException (abbd8a4ea); ReadBoundingSphere still constructor-validated (R6 candidate KI holds; 1ec77a734 test-only)
- page changes: shared-decoders paragraph (per-family decoders links), DecodeXnbCanonicalAsset location, Song missing companion wrapped, Video Play failures, evidence wording; callout -> c6dec91f
## content/cnj-documents (base c1c316b9)
- changed cited: ContentManager.cpp (loose readers moved to per-family ContentXxxLoaders.cpp, LINK-004/005); CnjEnvelope/SourceFile/CanonicalRead/Json.hpp unchanged; colorKey/copy semantics hold; RegisterCnjLoader exceptions unchanged (std::invalid_argument/logic_error)
- page changes: loose-reader location (2 links -> modules/content/src/Xna); callout -> c6dec91f
## content/content-robustness (base c1c316b9)
- changed cited: Texture2DContentTypeReader.cpp/PathContainment.hpp (comments only); related: XnbContainerFuzzTests (EndOfStream no longer accepted, 583af2a5e wraps), CNB 2386155f2 (stored chunk exact size), untyped decoder shares 14-byte guard; integration/ removed (96c6e77be)
- page changes: CNB limits row + decompression para; normalization table (EndOfStream row folded into ContentLoadException); crash wording (Vulkan driver path / wgpu-native, no renderer trace); asymmetry bullet; integration record now Git history; callout -> c6dec91f
## graphics/texture-data-transfer (base c1c316b9)
- changed cited: Texture2D.hpp/.cpp (39ef8ea2f copy/ownership; cd211420e System exceptions; compressed no shadow; REMED ids removed from comments), ShaderEffect.cpp (+4)
- page changes: copy semantics + content ownership; REMED-GFX ids removed (3); shadow failure exceptions NotSupportedException; RETIRED-RENDERER trace removed (Vulkan_* / Direct3D 11 parity registrations, missed by check_retired_renderers) -> SDL_GPU oracles + cross-family parity programs; evidence; callout -> c6dec91f
## graphics/resource-lifetime (base c1c316b9)
- changed cited: GraphicsResource.cpp/.hpp (39ef8ea2f: IsDisposed published before Disposing, no repeat, shared content metadata), Texture.cpp (exceptions); Texture2D/TextureCube copy ctors custom; SDL_GPU f0caebc0d live texture list
- page changes: Dispose(bool) event order; copy metadata sharing; by-type table (no longer defaulted; Unload disposes content copies); RETIRED-RENDERER trace ("Vulkan keeps a list of live textures") replaced with SDL_GPU live texture states (missed by guard); callout -> c6dec91f
## graphics/effect-object-model (base c1c316b9)
- changed cited: BasicEffect/AlphaTest/DualTexture/EnvironmentMap/SkinnedEffect.cpp, Effect.cpp/.hpp, EffectParameter.cpp (d650554a8 ISSUE-034/035 stock getter contract, Bones 72x(4x3) element views, EnvMap Texture/EnvironmentMap records), SpriteEffect unchanged (MatrixTransform still missing), draw packet facts hold
- page changes: EnvMap row 12->14 and XNA-extra column; Bones shape now XNA's; parameter-storage header + new paragraph (stock strict getters, StockParameterContractTests); evidence; callout -> c6dec91f
## graphics/spritebatch-semantics (base c1c316b9)
- changed cited: SpriteBatch.cpp/.hpp (3b6a2eaf3 ISSUE-003 Textures[0] binding + Immediate flush hook; 9359a26b6 ISSUE-004 live sampler; 65e69cc5e ISSUE-082 disposal sequencing; 8f08a82cc ISSUE-007 ColorMatrixEffect refusal [unclosed]; a07b9e5be IsStockEffectEXT), SpriteBatchTests (lifecycle tests), IGraphicsRenderer (float dest overrides still EasyGL+SOFTWARE)
- page changes: Immediate live sampler; Textures[0] left behind; disposed-batch row rewritten; ColorMatrixEffect row (marked not yet validated by CNA); Dispose sentence; Immediate retention + CNA-BUG-278 link + Textures[0] disposal behaviour; evidence; callout -> c6dec91f
## graphics/stock-effects-semantics (base c1c316b9)
- changed cited: BasicEffect.hpp (IsStockEffectEXT; SetShadowCascadesEXT ArgumentOutOfRange), AlphaTestEffect.cpp / SkinnedEffect.cpp (AddStockParameterInternal; Bones 4x3 views; REMED comments removed), GlStockShaderSources.hpp (cube-dir flip helper for rendered cubes; REMED comments); verified at T: DualTexture TextureCoordinate1 refusal (GraphicsDevice.cpp ValidateStockVertexInputs), SkinnedEffect throws, EnvMap NotSupported, CNA-BUG-261 still open (comment unchanged), per-pixel switches in DIRECTX9/EasyGL/WEBGPU/SDL_GPU/SOFTWARE/FNA3D, shadow forcing EasyGL/WEBGPU/SDL_GPU
- page changes: example provenance "TARGET headers" -> headers at c6dec91f; callout -> c6dec91f
## graphics/spritefont-text-layout (base c1c316b9)
- changed cited: SpriteBatch.cpp (DrawString: throwIfDisposed removed per ISSUE-082, layout loop unchanged), easygl_spritefont_multiglyph_spacing_test.cpp (2 lines, comment); SpriteFont.cpp/.hpp, Utf8Decode.hpp, SpriteEffects.hpp, SpriteFontTests unchanged; registrations (EasyGL 7, SDL_GPU cross-family, parity sprite_font, Software 6) hold; docs/spritefont-support.md still says combined flip unrepresentable
- page changes: callout -> c6dec91f (incl. "Checked by reading ... at c6dec91f")
## graphics/surface-formats (base c1c316b9)
- changed cited: Texture.cpp (cd211420e: GetBlockSizeSquaredEXT/GetFormatSizeEXT ArgumentOutOfRange, ValidateGetDataFormat ArgumentException, ValidateFormat InvalidOperation), Texture2D.cpp (renderer verdict InvalidOperation; order profile size -> renderer dim -> profile format -> shape -> renderer verdict, same at B but page said four checks), TextureCube/Texture3D (System exceptions; zero-size ArgumentOutOfRange; WarnAndStub exemption present since B), RendererCapabilityProfile.hpp (StorageRead/Write/Atomic usage bits removed with the retired modern GPU layer), IGraphicsRenderer.hpp (16384 comment unchanged), GraphicsDevice.cpp (draw-time checks unchanged), Fna3dRenderer.cpp (override still), Texture2DContentTypeReader (comment)
- page changes: helper exceptions (2 rows); Texture2D admission five checks incl. ArgumentOutOfRange and dimension NotSupported; verdict exceptions (Unsupported/Defer InvalidOperationException); WEBGPU-163 location; cube/volume zero-size + WarnAndStub; usage bits list; p3 wpb2-renderer-texture-maximum: header-comment sentence rewritten (no longer says CNA targets Direct3D 11; rationale vs GLES 3.0/WebGL 2 minimum 2048); callout -> c6dec91f
## graphics/vertex-and-index-buffers (base c1c316b9)
- changed cited: none (VertexBuffer.cpp, IndexBuffer.cpp unchanged B..T); related: D3D9Buffers.cpp (b5d187960: plain uploads D3DPOOL_MANAGED, options uploads DYNAMIC|DEFAULT, resize Reset reports content-lost); other families' option handling unchanged (comment-only diffs); EasyGL tests present; GFX-043/FX-131 labels still in source
- page changes: Direct3D 9 row rewritten; storage paragraph sentence; evidence; callout -> c6dec91f
## graphics/vertex-streams-and-declarations (base c1c316b9)
- changed cited: GraphicsDevice.cpp (stock-input checks e7bd98e46/31fe7917f incl. DrawUser*; draw order otherwise same; SetVertexBuffers unchanged); VertexDeclaration/VertexElement/VertexBufferBinding/BuiltInVertexStreams unchanged; related: WebGPU GetMaxVertexStreams (device max, no reserved slot; already so at B — page was wrong), D3D9 StateInvalidated content-lost on resize Reset (b5d187960)
- page changes: WEBGPU max-stream sentence; content-lost sentence (DIRECTX9 resize Reset); user-array draws refuse missing stock inputs; evidence; callout -> c6dec91f
## graphics/graphicsdevice-contract (base c1c316b9)
- changed cited: GraphicsDevice.cpp/.hpp (34be9272b ISSUE-066 SetBlendEnabled [unclosed]; 2df868a13 ISSUE-005 deleted raw user-draw templates [unclosed]; stock inputs; System exceptions; context ownership 9e4d0279a; constructor sequence unchanged), Effect.cpp (stock parameter helpers), PresentationParameters.hpp (D3D11 mention removed from comment), Game.hpp, tests (renderer gates drop retired identities), DirectX9Renderer.cpp (recovery; SetContextRecoveryEnabled still no-op), software readback test (comments)
- page changes: texture-slot paragraph rewritten (stock effects bind their texture to the device slot on Apply and sample the slot while applied — stale even at B); clear-test gating (SingleArgumentClear… also SDL_GPU); SetBlendEnabled behaviour (marked not yet validated); raw user draws refuse non-trivially-copyable vertex at compile time (marked not yet validated); evidence; callout -> c6dec91f
## graphics/device-reset-and-lifetime (base c1c316b9)
- changed cited: GraphicsDevice.cpp (d0cea7036: Reset returns before viewport/DeviceReset when CanBeginDrawEXT false; dirty states; disposal order unchanged), GraphicsResource.cpp (39ef8ea2f: IsDisposed published first, unregisters even when handler throws), GraphicsAdapter.cpp (System exceptions), GraphicsDeviceManager.cpp (System exceptions, comments), tests (+PresentationLifecycle, +DisposalHook); related: D3D9 StateInvalidated (b5d187960), RendererAdapterQueries: back-buffer hook only DIRECTX9, depth-selection hook unused (DIRECTX11 retired); stale DeviceLost header comments fixed by 66918da04
- page changes: Reset steps 7-8 (early return; dirty states); rollback paragraph; status (StateInvalidated; removed stale-header sentence); resource Dispose(bool) ordering; content copy disposed by Unload; QueryBackBufferFormat row (no "Direct3D families"); evidence; callout -> c6dec91f
- also touched: graphics/resource-lifetime #content-lost (StateInvalidated), graphics/vertex-streams WEBGPU phrase corrected
- device-reset: QueryRenderTargetFormat MSAA clamp corrected (EasyGL 2/4 since 714bfd9bc; FNA3D 2/4)
## renderers/easygl-state-and-resource-semantics (base c1c316b9)
- changed cited: EasyGLRenderer.cpp (retired modern GPU layer removed; rendered-cube orientation a6e8104d2/c8722e283; 4x MSAA promise 714bfd9bc; live limits b1ec33424; GLES float readback 53292f147; PBR colours; SpriteBatch ISSUE-003; SetBlendEnabled removed from renderer ISSUE-066), GlProfile.hpp (kMaxMultiSampleCount=4, ClampMultiSampleCount), GlStockShaderSources.hpp (cnaCubeDir), docs/easygl_bugs.md (banner unchanged), docs/rendertarget-support.md (Vulkan/Metal history removed, orientation audit added), backbuffer_pass_order_test (C5 kept; registrations EasyGL/SDL_GPU/WEBGPU/DIRECTX9/SOFTWARE/HEADLESS hold), easygl tests (registered); page sections otherwise hold
- page changes: rendered-cube orientation sentence; lede/evidence snapshot -> c6dec91f; callout -> c6dec91f
## build/module-architecture (base c1c316b9)
- changed cited: modules/CMakeLists.txt (cna_add_module now cna_module_include_root + cna_register_cxx_target from cmake/InstallCxx.cmake [CNA_INSTALL_CXX SDK]; cna_build_config adds C++-runtime-first link option [CNA_CXX_RUNTIME_LINKAGE] and size GC link option [CNA_OPTIMIZE_FOR_SIZE]; gamer-services under CNA_ENABLE_GAMER_SERVICES), modules/renderers (retired families removed; SDL interop include for sdl-gpu+fna3d only), cmake/Tests/ModuleProbes.cmake (identity-count comment fixed), cmake/RendererSelection.cmake, CrossFamilyPrograms.cmake; shared libcna.so needs CMake>=3.30 (cmake/SharedRuntimePolicy.cmake); modularization/RECONCILIATION.md removed (ce74063e6)
- page changes: cna_add_module code + helper paragraph; build_config facts + link options; networking row (gamer services option); two SDL-backed families; figure Net/GamerServices gating line + caption (shared lib conditions, gamer services option, snapshot); stale-comment examples (identity count removed); reconciliation record location (callout + evidence); lede/evidence snapshot; callout -> c6dec91f
## build/tools-and-scripts (base c1c316b9)
- changed cited: CMakePresets.json (retired renderers out of macOS/iOS presets; tests description now non-recursive, names SDL/SDL_mixer/googletest; counts 17/17 unchanged), cmake/UnitTests.cmake (22 focused targets unchanged), ModuleProbes.cmake (C++ runtime linkage probes), check_renderer_identities.py, run-all-renderer-smoke-tests.sh (tiers now OPENGLES3/SDL_GPU/WEBGPU; p3 region already at c6dec91f, not edited), check_build_performance_policy.py (stale-exception rule), tools/platform (tray/message-box harnesses); counts 898/11,898/598/17 hold; tools named all exist
- page changes: preset-lag sentence; lede/evidence snapshot; callout -> c6dec91f
## reference/native-c-api (base c1c316b9; body already refreshed to c6dec91f by an earlier pass)
- changed cited: abi.h (0.46 -> 0.50), headers (route count 3,212 / 60 headers verified by recount), route wrappers moved to modules/c-api/src/generated/*.inc included by the cited .cpp files (helpers unchanged in substance), CnaCApiContent.cpp (C load detaches content ownership), ContentManager.cpp (Unload disposes recorded objects, 39ef8ea2f)
- page changes: content-handles sentence (Unload disposes; C copy detached); callout -> c6dec91f (incl. snippet note)
## reference/ecosystem-quick-reference (base c1c316b9; cites modules/ tree)
- changed: storage module (ISSUE-010 [FIXED_VALIDATED] XNA exception types; ISSUE-152 sharing [platform validation pending]; lazy root; dangling-symlink refusal; tests 14 -> 70 in 7 files); DynamicSoundEffectInstance 16-bit frame check (present already at B; row was wrong); input EXT members, video NotSupported, 71-bone rig, sharp-runtime 0.1.0 gate, 331/3,627 hold
- page changes: StorageDevice row, StorageContainer row, storage caution sentence; DynamicSoundEffectInstance row; snapshot mentions (callout, lede, applications); callout -> c6dec91f
- generated/other-area copy to report: development/internals/modules/storage.html#tests likely still says 14 storage tests (not edited: development/ out of scope)
## platforms/web-build-and-main-loop (base c1c316b9)
- changed cited: Game.cpp (90ae88759 browser variable step: IsFixedTimeStep=false runs one Update with real elapsed time + one Draw; BeginDraw gate), StorageDevice.cpp (lazy root; web mount refusal unchanged), ENetBackend.cpp (comments; web port/outbound client unchanged; discovery compile-out is in ENetDiscoveryService.cpp), RendererSelection.cmake (retired identities removed; WEBGL2 rules hold; default in RendererIdentityDefault.cmake), BuildPerformance.cmake (size options added; exception ABI/Asyncify unchanged), CMakeLists.txt (threads/WasmFS unchanged), c-api CMake (ASYNCIFY=0, CheckWasmLinkContract, --check-playwright hold), workflow (submodules non-recursive; emsdk 6.0.3); NEXT.md renamed handoff.md (bb6607d34) with SAMPLE-070 record; run_browser_tests.mjs unchanged
- page changes: #loop browser frame-body bullets (variable step honoured); SAMPLE-070 record location; discovery source file; p3 wpb6-playwright-resolution "Checked by reading at" -> c6dec91f; callout -> c6dec91f
## practice/porting-case-studies (base c1c316b9)
- changed cited: ContentManager.cpp (loose loaders split out: ApplyColorKey now in BuiltinContentLoaders.cpp, called from ContentTexture2DLoaders.cpp; exact-match logic unchanged), docs/webgpu-renderer.md & headless-renderer.md (records of the Blupi runs still present), CnjCanonicalRead/SongContentPipeline/SongContentTypeReader/MediaLibraryIndex/ThirdPartySDL unchanged; SDL_mixer submodule same commit; default timestep 166,667 ticks
- page changes: ApplyColorKey link; "TARGET" wording in info box -> c6dec91f; snapshot mentions; callout -> c6dec91f
## practice/migrating-an-xna-game (base c1c316b9)
- changed cited: RendererSelection.cmake (retired identities removed; DIRECTX9 Windows gate, TERMINAL CPU-only, OPENGLES3 refused under Emscripten hold), Harnesses.cmake (strict-API harness still wired), Game.cpp (timestep default/setter/500 ms clamp hold), xna-oracle (39 non-recursive scenes hold), XnbDecompression/Effect readers unchanged; untyped LZ4 refusal holds (ContentManagerUntyped.cpp); facts 61 readers / 8-of-10 compiled effect identities hold
- page changes: "the Direct3D identities" -> DIRECTX9 (retired-renderer trace); TARGET wording x3; snapshot mentions; callout -> c6dec91f
## practice/xna-api-surface-auditing (base c1c316b9)
- changed cited: Viewport.hpp/.cpp (ec2d8b692 ISSUE-008 [unclosed]: DEF_PROP replaced by explicit accessors; behaviour unchanged), ViewportTests (+65; TitleSafeAreaEqualsBounds present), Ray.cpp (e1377c437 ray-box boundaries; Equals(any)/GetHashCode ^ unchanged), census JSON (3 cna_symbol strings; all counts unchanged), CHECKLIST.md (quoted rules present), test_audit script (+44)
- page changes: Viewport accessor sentence (DEF_PROP history; ISSUE-008 phrased as committed, not validated); snapshot mentions x3; callout -> c6dec91f
## models/gltf-conformance (base c1c316b9)
- changed cited: corpus (counts 148/148/148/744 and 140 goldens unchanged; tex-dual-texture-stride now stride 28, 9cff1501c), manifest (that fixture only; ledger 9 records unchanged), UnitTests ladder rungs (L0-L6, Perf, Ledger, Tool hold), workflows (stride CI renderers STUB/HEADLESS/OPENGLES3/SDL_GPU/WEBGPU/SOFTWARE; non-recursive submodules), plan_gltf.md (GLTF ROBUST 9 of 12 holds), test suites named in p3 present
- page changes: p3 wpb4-gltf-suite-guards "Checked by reading ... at" -> c6dec91f; evidence (TARGET wording, snapshot); callout -> c6dec91f
## models/vertex-packing-and-strides (base c1c316b9)
- changed cited: GltfImportCore.cpp (9cff1501c: dual-texture layout stride 20 -> 28 with TextureCoordinate1), VertexDeclarationFidelity.hpp (kStride28 row; table now 12 entries; preamble now records the no-translation finding as a past measurement), ContentManager.cpp (raw upload moved to ContentModelLoaders.cpp; 28 via SetDataRaw), l5.py (stride 28), CI stride conformance on 6 identities (WEBGPU joined 2026-10-17)
- page changes: stride table (20 -> non-glTF VertexPositionTexture; new 28 row); count sentence + reason for 28; selection sentence; lossy-row sentence; raw upload list + file link; canonical-table measurement tense; callout identities 5 -> 6; TARGET wording; callout -> c6dec91f
## models/gltf-import (base c1c316b9)
- changed cited: GltfImportCore.cpp (5f136988a ISSUE-092 [FIXED_VALIDATED] empty selected scene imports nothing; eb9653bf2 ISSUE-093 [FIXED_VALIDATED] undefined interpolation refused; ab0ab883c 094/095 reporting; 9cff1501c stride 28; size ~5,600 lines), cgltf now compiled in CgltfImplementation.cpp (bf9089edc LINK-002) with CgltfInternals.hpp exports, ReadGltfModel moved to ContentModelLoaders.cpp (stale first-group comment still present there), registry 21 records, Load wrapper message holds
- page changes: build-invariant paragraph (cgltf TU, stb users); ReadGltfModel links (2, one inside p3 wpb4-gltf-cgltf-faults); scene fallback sentence; interpolation refusal bullet; size; evidence/TARGET; p3 wpb4-gltf-cgltf-faults "Checked by reading ... at" -> c6dec91f; callout -> c6dec91f
## models/model-mesh-runtime (base c1c316b9)
- changed cited: Model.cpp (cd211420e: rootBoneIndex/meshParentBones/materialVariant -> ArgumentOutOfRangeException), ModelMesh.cpp (da6c5c120 ISSUE-081 [FIXED_VALIDATED] constructor seeds Effects from parts), ContentManager.cpp (39ef8ea2f ISSUE-011 [FIXED_VALIDATED]: Unload disposes model buffers/effects/textures on all four routes; readers moved to ContentModelLoaders.cpp; CNB decoders in Cnb/CnbModel*Decode.cpp), 1beef880d ISSUE-023 [unclosed] cameras in .cnj/.cnb schema 1; ModelTests 24 holds; collection exceptions unchanged
- page changes: hand-built exception; code snippet exception (old wrong example replaced); material variant exception; part-effects paragraph (constructor seeding); routes table (decoder/reader locations; cameras); route-choice cameras; getCamerasEXTProperty; Unload code comment + paragraph (disposal); TARGET wording; callout -> c6dec91f
## models/cnj-toolchain (base c1c316b9)
- changed cited: gltf_to_cnj.cpp (1beef880d ISSUE-023 [unclosed]: cameras array), ContentManager.cpp (Model .cnj reader moved to ContentModelLoaders.cpp; stride/skip/default rules unchanged), GltfToCnjToolTests (+68); skeleton sidecar reading unchanged (096 concerns AnimationPlayer)
- page changes: cameras sentence (marked not yet validated); outputs table; reader link; TARGET wording; callout -> c6dec91f
## models/skinning-and-animation (base c1c316b9)
- changed cited: AnimationPlayer.cpp/.hpp (b98629c89 ISSUE-096 [FIXED_VALIDATED] partial prefix -> ArgumentException at construction and recompute; cd211420e ApplyClipToBonesEXT ArgumentException), MorphTargetEXT.cpp (ArgumentException / InvalidOperationException; unbind/rebind already at B), GltfImportCore.cpp (a9d378c06 ISSUE-031 [unclosed] STEP hold keys + cubic sampling), AnimationPlayerTests (+40)
- page changes: Recompute check (prefix); prefix paragraph; clip resampling paragraph (marked not yet validated); ApplyClipToBonesEXT/BlendMorphTargetsEXT/SetMorphWeightsEXT exception types + unbind note; TARGET wording; callout -> c6dec91f
## siblings/easygl-and-metagl (base c1c316b9)
- changed cited: EasyGLRenderer.cpp/.hpp (3e1a154f4 modern GPU layer dropped: GPU timer and query/compute meta-gl calls gone; direct meta-gl wrappers 44 -> 32 by distinct-name count; RecoverableResource adopters 10 -> 9), RendererSelection.cmake (CNA_EASYGL_ROOT, JS exception model hold), d3d-windows-ci.yml (now clone_siblings.sh), CMakePresets (EASYGL_BUILD_* OFF in web preset holds), SdlAvailability (NPV-0114 holds), UnitTests (cna_test_build_config holds); integration records removed (96c6e77be) — dated evidence kept with Git-history note
- page changes: wrapper count (figure caption + body); nine RecoverableResource classes; GPU-timer limitation paragraph replaced; reading-order item; CI sibling sentence; integration-record note; snapshot mentions; callout -> c6dec91f
## sharp-runtime/components-and-consumption (base c1c316b9; sharp-runtime facts at 41b918c9 unchanged)
- changed CNA-side: ec2d8b692 ISSUE-008 [unclosed]: Prop.hpp no longer included by CNA production sources (Viewport, ContentManager, 7 sensor headers spelled out); include census 84/92 -> 93/101 (recounted; all resolve at 41b918c9, 15 module dirs); Xml.Serialization now on every platform (Windows exclusion removed); shared lib CMake >= 3.30; runtime private Uri
- page changes: meta description (commit removed: generated copies stale — hub deep-dives/sharp-runtime/index.html, search-index.json); lede; closure Windows note; header census; Prop.hpp consumer paragraph (marked not yet validated); Viewport macro sentence; CMake 3.30; runtime row; Windows paragraph; advice bullet; figure caption; callout -> c6dec91f
## sharp-runtime/object-model-and-core-types (base c1c316b9; sharp-runtime facts at 41b918c9 unchanged)
- CNA-side re-checked at T: nine exception headers with the serialization constructor (four write/restore via ExceptionSerialization.hpp), NetworkSession.cpp GamerJoined SetReplayHook, TextInputEXT MulticastAction, NetworkSessionProperties MutationCounter — all hold (NetworkSession.cpp diff concerns other behaviour)
- page changes: lede snapshot; callout -> c6dec91f
## sharp-runtime/parity-and-verification (base c1c316b9; sharp-runtime facts at 41b918c9 unchanged)
- CNA-side: plan_apple_m4.md (62952ef5 18,084/18,059/0/25 record present), sibling tests forced off; Windows Xml.Serialization exclusion and Prop.hpp inheritance changed (see components page)
- page changes: for-CNA sentence; lede snapshot; callout -> c6dec91f
## sharp-runtime/streams-text-and-tasks (base c1c316b9; sharp-runtime facts at 41b918c9 unchanged)
- CNA-side re-checked at T: ContentManager::OpenStream (read-only MemoryStream; INT32_MAX refusal; resolution through TryReadAssetBytes incl. packaged assets), ResourceContentManager MemoryStream, BinaryReader::ReadChar users, Threading.Tasks not in closure — hold
- page changes: lede snapshot; callout -> c6dec91f
## foundations/language-conventions (base c1c316b9; R6 had kept c1c316b9 — now re-verified)
- changed cited: Color.cpp (CornflowerBlue unchanged), SkinnedEffect.cpp (setter unchanged), Game.hpp (Exiting unchanged), SpriteBatch.cpp (still throws ODE), Texture3D/TextureCube.hpp (concepts unchanged), IGraphicsRenderer.hpp; error model recounted: runtime_error production sites 1,646 -> 1,078 with renderers 741 (~7/10, was ~4/5); ODE throw sites ~120 across graphics, audio, net, gamer-services, content, storage, media, devices, runtime (Game now ODE, cd211420e), none in renderers; graphics/src/Xna 50 ODE throws; CLAUDE.md still prescribes std::runtime_error; dialect claims hold (no C++23-only facilities; Doxyfile settings)
- page changes: ODE count sentence; p3 wpb1-cpp-dialect-error-model error-model sentences (renderer share; ODE sites; Game); lede snapshot; callout -> c6dec91f
- language-conventions p3: VideoPlayer idempotence reason updated (CHECKLIST row now cites genuine XNA IL)

## 3. Ids and p3 regions

* No element id was removed or renamed on any page. Headings whose text changed keep their id:
  `services/sensors-and-vibration#lifetime`, `framework/services-and-components#disposed-components`,
  `framework/game-time-and-timestep#reset-elapsed-time`, `content/xnb-container-and-object-graph#disposal-recording`.
  One internal link was re-pointed: `framework/game-class-and-lifecycle` → `services-and-components.html#drawable-content`.
* p3 regions touched (inside `<!--p3:begin X-->…<!--p3:end X-->` only):
  - `deep-dives/services/gamepads-and-haptics.html` — `wpb5-evdev-controller-mappings`
  - `deep-dives/services/sound-effects-and-streaming.html` — `wpb5-microphone-device-order`
  - `deep-dives/services/avatars.html` — `wpb6-avatar-regression-floor`
  - `deep-dives/framework/window-and-device-manager.html` — `wpb5-mobile-backbuffer-orientation`
  - `deep-dives/content/xnb-container-and-object-graph.html` — `wpb4-xnb-extension-proof`
  - `deep-dives/graphics/surface-formats.html` — `wpb2-renderer-texture-maximum`
  - `deep-dives/platforms/web-build-and-main-loop.html` — `wpb6-playwright-resolution`
  - `deep-dives/models/gltf-conformance.html` — `wpb4-gltf-suite-guards`
  - `deep-dives/models/gltf-import.html` — `wpb4-gltf-cgltf-faults`
  - `deep-dives/foundations/language-conventions.html` — `wpb1-cpp-dialect-error-model`
  (`deep-dives/build/tools-and-scripts.html` `wpb6-smoke-orchestrator` was checked and already correct at T; not edited.)
* Known Issues links added: one, `CNA-BUG-278` on `graphics/spritebatch-semantics`, wrapped as
  `<!--issue:NEW-PIN3-02-->…<!--/issue-->`. No link to a retired entry was added.

## 4. Candidate new Known Issues (not filed; for R5's owner)

1. **Content.Unload() in UnloadContent() during Game::Dispose() throws ObjectDisposedException.** `Game.cpp` (Dispose,
   ~line 1167 at T) disposes `Content_` before the graphics-device service whose `DeviceDisposing` handler calls
   `UnloadContent()`; `ContentManager::Unload()` (ContentManager.cpp:364–367) refuses a disposed manager. XNA's handler
   unloads Content itself and `Game.Dispose` does not dispose Content, so the common XNA idiom works there. In CNA the
   exception leaves `Dispose()`, the game is never marked disposed and a repeated `Dispose()` rethrows. Class: bug.
2. **GL/GLES/WebGL families report a 16,384 maximum texture dimension without querying the device.**
   `IGraphicsRenderer::GetMaxTextureDimension()` (IGraphicsRenderer.hpp ~3196) returns 16384; no EasyGL identity overrides it,
   while GLES 3.0 / WebGL 2 guarantee only 2048. A Texture2D or an XNB texture larger than the device's
   `GL_MAX_TEXTURE_SIZE` passes CNA's size checks and fails in the driver; the capability profile marks the value "known".
   The header comment justifying 16384 still cites Direct3D 11 and "every native API this project targets". Class:
   verification gap or bug (low).
3. **Stale code comments that contradict the code** (documentation class, low): `modules/renderers/CMakeLists.txt` speaks of
   "three PLAT-76 allowlisted SDL-backed families" (two remain: sdl-gpu, fna3d); `ContentModelLoaders.cpp` (~1680) says a
   runtime glTF load imports only the first mesh group (it imports every group); `cmake/Tests/ModuleProbes.cmake` (~113)
   says SDL3 is a private detail of core's Logger (core no longer includes SDL); `CLAUDE.md` (~180) and the coding rules
   prescribe `std::runtime_error` for use after disposal while every XNA-facing site, Game included, throws
   `System::ObjectDisposedException`; `PacketWriter.hpp` still documents float colour reads (from the network pass).
4. Still holding from earlier passes: R6's negative XNB bounding-sphere radius refusal (ContentReader.cpp:174–179; 1ec77a734
   is test-only); `CNA-BUG-267` (HandleClientHello sends the welcome before `AddRemoteGamer`) holds at T.

## 5. Changes needed outside this sweep's scope (report only; not edited)

* Generated copies of edited descriptions are stale until the next `scripts/regenerate_site.sh`:
  `services/sensors-and-vibration` (hub `deep-dives/services/index.html`, `docs/sensors.html`,
  `docs/tutorials/50-accelerometer.html`, `development/testing/architecture.html`,
  `development/internals/modules/devices.html`, `development/architecture/platform.html`, `search-index.json`) and
  `sharp-runtime/components-and-consumption` (hub `deep-dives/sharp-runtime/index.html`, `search-index.json`, any
  related-page lists that quote it).
* `check_facts.py` flags copies of older deep-dive descriptions in `docs/` and `development/` ("C ABI 0.46.0",
  "14 public renderer identities", "12 renderer families"): `docs/runtime-renderer-selection.html`, `docs/verification.html`,
  `docs/c-api.html`, `development/handbook/update-the-c-api.html`, `development/repository/index.html`,
  `development/architecture/bindings.html`, `development/testing/architecture.html`,
  `development/internals/modules/core.html`, `development/internals/bindings/c-api-internals.html`,
  `development/build/architecture.html`, `development/repository/module-graph.html`,
  `development/repository/source-ownership.html`. The deep pages themselves are current; regeneration should clear these.
* `docs/migration-from-monogame.html` says loaded copies "stay valid" after `Unload()`; at T `Unload()` disposes every
  recorded object, content-owned copies included (39ef8ea2f).
* `development/internals/modules/storage.html#tests` (linked from the ecosystem quick reference) likely still says 14
  storage tests; T has 70 definitions in seven files.
* `development/internals/content/runtime.html` (linked from model-mesh-runtime) should state that `Unload()` disposes model
  buffers, effects and textures on every Model route.
* Generated sidebars of all `deep-dives/renderers/*` pages still list the tombstoned renderer pages
  (`check_retired_renderers.py` hits on `docs-nav-link`/`dev-pager` lines) — a site_deep.py regeneration matter.

## 6. Open doubts

* `reference/native-c-api`: the body had already been refreshed to c6dec91f by an earlier pass; I verified the route count
  (3,212 over 60 headers), the generated route wrappers (`modules/c-api/src/generated/*.inc`, included by the cited `.cpp`
  files) and the content-handle detachment, not every ABI-history sentence.
* `siblings/easygl-and-metagl`: the direct meta-gl wrapper count (32 at T) uses distinct `metagl::gl*` names outside comments;
  the same method gives 44 at B where the page said 43, so the old figure used a slightly different method.
* `sharp-runtime/components-and-consumption`: the include census (93 production, 101 overall) uses
  `#include <System/…>|<SharpRuntime/…>` in `modules/*/{include,src}`; at B the same method gives 86 where the page said 84.
  The per-module-directory breakdown replaced the per-component one, which needs the registry and was not recomputed.
* `graphics/vertex-and-index-buffers` and `models/vertex-packing-and-strides` describe DIRECTX9 storage and the
  declaration-fidelity measurement from source; no renderer test was run.
* `platforms/web-build-and-main-loop`: the browser variable-step path was read, not run; CNA-BUG-080 (status "narrowed")
  remains linked.
* `graphics/graphicsdevice-contract` texture-slot paragraph was wrong already at B (stock effects bound the slot at B too).

## 7. Validators (after the sweep)

* `check_deep_page.py`: all 56 pages ok (7 pages carry the pre-existing "mentions alpha.1 (historical)" warning).
* `check_facts.py | grep deep-dives/`: no finding (baseline: none); remaining findings are in `docs/`/`development/`.
* `check_retired_renderers.py | grep deep-dives/`: only generated sidebar/pager lines of `deep-dives/renderers/*`; one
  body finding on `services/avatars` ("Direct3D 12" beside DIRECTX9) fixed to "SDL_GPU on SDL's Direct3D 12 driver".
* `check_source_links.py`: ok.
* `validate_site.py`: no finding in `deep-dives/`; one baseline broken link elsewhere disappeared (another agent's fix).
* `issue_refs.py check`: 0 errors (the CNA-BUG-278 link was wrapped).
