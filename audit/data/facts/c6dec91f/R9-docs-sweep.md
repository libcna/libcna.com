# R9 — Docs sweep (hand-written `docs/*.html` and the top-level features, roadmap and about pages), CNA B=c1c316b9 → T=c6dec91f

INTERNAL AUDIT RECORD (not served).

Scope: every hand-written `docs/*.html` page (not `docs/tutorials/`), plus the subsystem statements of `features.html`,
`roadmap.html` and `about.html`. The coordinator had already applied renderers, numbers, versions, branches, the C ABI and the
link-size facts to these pages; this sweep covers the remaining behavioural changes B..T (CNA-DEMOS repair campaign, museum
fixes, XNA-parity fixes, exception types, content, storage, audio, media, input, net, gamer services, avatars, math).

## 1. Method

* CNA was read, never built or run: `git log/diff/show/grep` at B and T in `/rv/data/development/github.com/libcna/cna`, the
  extracted tree `~/.cache/libcna-com/cna-target` (stamp = T), `CNA_DEMOS_REPAIR_MATRIX.json` at T for issue status, and
  `docs/gamer-services-known-limitations.md` / `docs/avatars.md` at T. sharp-runtime read with `git show` only (local clone,
  `next` 4e146b90; `v0.1.0` tag c20373ba; 41b918c9). XNA 4.0 decompiled `Game.cs` read for the component-initialisation rule.
* The docs pages cite almost no CNA source links (only `storage.html` → `StorageContainer.cpp`, `inspector.html` →
  `docs/inspector.md`/`modules/inspector`, plus LICENSE in footers), so per page the subsystem prose was read and every
  behavioural statement checked against the T source of the subsystem it describes, with `git log B..T` of that module.
* Unclosed demos fixes (005, 006, 007, 008, 022, 023, 031, 066, 067) are never called fixed: where a page describes one
  (006, 007, 022, 023, 031) it says "a change committed at this snapshot that CNA has not yet validated" or equivalent;
  FIXED_PLATFORM_VALIDATION_PENDING items (003, 101, 152) say the platform validation is pending.
* Test counts were recomputed with the site's method (files with a `test`/`tests` path segment under the module; `TEST`,
  `TEST_F`, `TEST_P`, `TYPED_TEST`, `TYPED_TEST_P`). Where the page's old figure could not be reproduced at B by that method,
  this is noted.
* Evidence callouts: no page in scope has a `dev-evidence` callout; doc-meta lines already name c6dec91f (coordinator). The
  statements changed below are source-verified at c6dec91f. One doc-meta date was wrong and fixed (`docs/roadmap.html`).
* No commit, push, `regenerate_site.sh`, `apply_expansions.py fold`; no `<!--p3:deep-links-->`/`<!--p3:issue-links-->`
  block, sidebar, breadcrumb, pager, hub list or `<!--issue:KEY-->` text edited; nothing in `development/`, `deep-dives/`,
  `known-issues/` or `docs/tutorials/` edited.

## 2. Per-page record

Format: changed in B..T (basis) / re-read / page changes / evidence / ids / p3.

### docs/storage.html
- B..T: `modules/storage` 14 commits (a24c75b2e, 162e07b8a, c30925496, 4dba781c3, 9c068f632, 4d384865c, 21b4cd64c,
  ac6be8f03, 17c66a9d3, fffa552ad, 3798787bb, 5865ae938, cd211420e, 657eff838); cited `StorageContainer.cpp` +181/−72.
  Matrix: 010 FIXED_VALIDATED, 151 FIXED_VALIDATED, 152 FIXED_PLATFORM_VALIDATION_PENDING (Windows runtime pending).
- Re-read at T: `StorageDevice.cpp`, `StorageContainer.cpp`, both headers (diff B..T), the seven test files (70 definitions;
  B: one file, 14), sharp-runtime `FileStream.hpp` (4-argument constructor added in c6984ece, absent at 41b918c9 and at the
  `v0.1.0` tag), `modules/storage/CMakeLists.txt` (IDBFS/WasmFS rule unchanged).
- Changes: status callout (XNA exception types); test callout rewritten (7 sources / 70; single-byte read-backs; no
  realistic save round trip; sharing matrix not built for the browser); `BeginShowSelector` validation
  (`ArgumentOutOfRangeException` for player, then negative size); `EndShowSelector` (`ArgumentNullException`,
  `InvalidOperationException` on second End); `BeginOpenContainer` (no validation); `EndOpenContainer` (whole chain created,
  result consumed on failure, ArgumentNull/Argument/IOException/UnauthorizedAccess, device must outlive container);
  `IsConnected` (creates root; false on failure); `DeleteContainer` now XNA's scope (the B-era "CNA also deletes the other
  players' folders" comparison removed; escape refusal kept as the one deliberate deviation); `SetAppNameEXT` creates
  nothing; `GetStorageRootEXT` throws; root paragraph (lazy, failure not cached — the B text "latched empty … resolves
  against the working directory" removed; how each access reports failure); path containment (`System::ArgumentException`,
  dangling final links, `ArgumentNullException` with parameter names, uninspectable components fail with the FS error);
  container disposal (`ObjectDisposedException` before validation; streams kept); `CreateFile` exclusive; `OpenFile` sharing
  (XNA defaults; native share masks / POSIX advisory locks / best-effort browser VFS; Linux validated, Windows pending;
  needs sharp-runtime c6984ece, which shares version 0.1.0 with older checkouts); `FileExists`/`DirectoryExists` false on any
  failure; `DeleteFile` (`File.Delete` semantics); `GetFileNames` vanished root → `DirectoryNotFoundException`; empty
  patterns → no names; `CreateDirectory` file in the way; `DeleteDirectory` exception set; `StorageDeviceNotConnectedException`
  cases rewritten; catch sample (System types); `End*` exception paragraph; dispose callout.
- p3 `wp15-storage-container-details` touched: wildcard paragraph (empty pattern; what the tests match), "Disposal and
  concurrent writers" paragraph rewritten (ODE; sharing defaults; native share modes; Linux/Windows validation), syntax-check
  provenance sentence ("an earlier snapshot's headers; the calls it uses are unchanged at c6dec91f").
- Ids: none changed (`#storage-root`, `#path-containment`, `#container-details`, `#disposal-and-sharing` kept).

### docs/content-manager.html
- B..T: `ContentManager.hpp/.cpp` (583af2a5e root guard, d7ce398d8/c1006b03e OpenStream, 39ef8ea2f Unload,
  cd211420e ODE, bbe2bda7b root discovery + manifest bookkeeping, dcb9e0978/2a5100d72 declared readers), new
  `ContentSoundEffectLoaders.cpp`. Matrix 011, 012, 013, 014, 039, 043, 045, 087 FIXED_VALIDATED.
- Re-read: `Load<T>` template, `Load<SoundEffect>` specialisation, `Unload`/`Dispose(bool)`, `setRootDirectoryProperty` doc,
  `TitleRootedDirectory`, manifest scan.
- Changes: RootDirectory row (assignment while cached → `InvalidOperationException`, even same root); manifest row
  (`cna-content` bookkeeping excluded); seam paragraph in `#caching-and-lifetime` rewritten (Load reads the `.xnb` through
  virtual `OpenStream`; base missing-XNB fallback only; `RouteLoadsThroughOpenStreamEXT`; `ResourceContentManager`;
  ODE after `Dispose`). The coordinator's Unload row was checked and holds.
- Ids: none changed.

### docs/migration-from-monogame.html
- Changes: `shared_ptr` bullet, `Unload()` bullet and side-by-side comment (Unload disposes; held copies share the disposed
  resources; one manager per lifetime); "Web builds" bullet (saves persist through IDBFS; threaded WasmFS refusal) — the old
  "no save persistence … in-memory file system" was already wrong at B.
- Checked, holds: XACT caveats (`WaveBank.cpp` XMA/WMA → null, first PlayWave), `TouchCollection` advisory `IsReadOnly`,
  video `NotSupportedException`.

### docs/audio.html
- B..T: `modules/audio` (6102058bb ISSUE-114, 5d66bb795 ISSUE-029, 514a6a8c2 ISSUE-073, 85a23569c ISSUE-038,
  783fe5739/3c67874ba ISSUE-028, c02d59409 AM4-321, 39ef8ea2f, 7d8eba687 LINK-006, 844e3ce41/594d7d328 museum).
- Re-read: `SoundEffect.hpp` (two `FromStream` overloads) and the XNA wave parser, `SoundEffectInstance::setIsLooped`,
  `setPan`, `Stop(bool)`, `WaveBank.cpp`, `Cue.cpp`.
- Changes: test count 38/765 → 41/793 (same method gives 37/762 at B, so the old figure used another base); NULL row and
  `Duration` row (XNA `FromStream(Stream&)` reports a duration on every implementation); `FromStream` row (two overloads, XNA
  exceptions, stream closed on success); `IsLooped` → `InvalidOperationException`; `Stop(immediate)` row (`Stop(false)` plays
  the loop tail; the commit tested SDL3_mixer, ALSA syntax-checked only); sample comment; refused `setPanProperty` keeps the
  value.

### docs/video-playback.html
- B..T: `VideoPlayer.cpp/.hpp`, `Video.cpp/.hpp` (abbd8a4ea ISSUE-099/100 FIXED_VALIDATED, 101
  FIXED_PLATFORM_VALIDATION_PENDING; 45f704c04; 0562550c3).
- Changes: warn callout (constructor `FileNotFoundException` first); tests 30/304 → 40/362 (method reproduces 30/304 at B;
  alpha.1 parenthesis dropped); Video paragraph (constructor exception, `FromUriEXT` title-relative with platform validation
  pending, per-Video track selection, destruction detaches players); `Play` exceptions; `Stop` keeps video and frame;
  `GetTexture` (`InvalidOperationException` before any open; last frame when paused/stopped; nullptr cases); `Volume` range;
  `getVideoProperty` retention, `SetVideoTrackEXT`, which members throw ODE; texture pointer stability.

### docs/input.html
- B..T: `modules/input` (cd211420e, 974c1ac08 only; public headers unchanged except `HapticDevice.hpp`);
  `Sdl3InputServices.cpp` (0c230d2e9 AM4-320, 90ae88759).
- Re-read: `Mouse::SetPosition` (relative mode no-op holds), `NeedsVirtualMouseWarp` (Emscripten and SDL's `wayland`
  driver), `TouchCollection` (advisory `IsReadOnly` holds); test count 50/540 verified at T.
- Change: Wayland virtual-warp anchoring sentence.

### docs/sensors.html
- B..T: `modules/devices` (a83673fc5 `Dispose(bool)` protected, ec2d8b692 ISSUE-008 [unclosed] macro hygiene, 66918da04
  docs); 8842b9a50 (ISSUE-062) is C ABI only.
- Change: test count 37/530 (alpha.1 36/525) → 39/535 (same method gives 38/534 at B).

### docs/gamer-services.html
- Basis: `CMakeLists.txt` (`CNA_ENABLE_GAMER_SERVICES` default = `CNA_ENABLE_NET`; NET requires it), `CMakePresets.json`
  ios presets, `docs/avatars.md` (1,021-byte description holds), `docs/gamer-services-known-limitations.md` §33 (avatar
  review of 2026-10-15), 26b0167f0 (`SendDataOptions` flags), 420a4572a/8a5e5d8aa (ISSUE-085/025 offline leaderboard
  columns).
- Changes: build-option sentence; iOS sentence; avatar evidence (2026-10-15 review on OPENGL33, OPENGLES3, SOFTWARE, SDL_GPU
  on Vulkan, WEBGPU, FNA3D, and DIRECTX9 / SDL_GPU on SDL's Direct3D 12 driver under Wine; worst mean difference 0.09/255,
  worst silhouette 0.9988; native Windows drivers and Metal not measured) replacing "not measured on Direct3D 9 or FNA3D";
  not-qualified list; known-gaps line (stream columns and combined `SendDataOptions` no longer gaps; guests remain,
  CNA-GAP-074). Dated 2 Oct / 7 Oct qualification runs kept as dated history.

### docs/model-loading.html
- Basis: `GltfImportCore` (5f136988a ISSUE-092, eb9653bf2 ISSUE-093 FIXED_VALIDATED; a9d378c06 ISSUE-031 unclosed),
  1beef880d ISSUE-023 unclosed (cameras in `.cnj` and a non-mandatory `MCAM` chunk), cd1f5ef0a ISSUE-022 unclosed (texture
  children by default), `Model.cpp` (cd211420e). Published CNA-GAP-035 is already "narrowed" to match.
- Changes: Scene row (empty selected scene → `ContentLoadException`); sampler sentence (undefined interpolation refused;
  STEP/CUBICSPLINE resampling committed, not validated) replacing the flat "supports"; cameras row; `.cnb` route (texture
  children and cameras, both committed-not-validated); `.xnb` route (cameras dropped, textures as XNB children, Model/clip
  children refused); `CopyAbsoluteBoneTransformsTo` → `ArgumentOutOfRangeException`.

### docs/game-loop.html
- Basis: `runtime/src/Game.cpp` (f9747ea49 ISSUE-019, 90ae88759, 031693a9f, 96522bf34, dcb9e0978/2a5100d72, cd211420e),
  `GraphicsDeviceManager.cpp` (DeviceDisposing raised unguarded), XNA decomp `Game.cs` (`notYetInitialized`, `inRun`).
- Changes: fixed-vs-variable paragraph (`ResetElapsedTime()` works in both modes — the old "does nothing under the fixed
  step" removed); Emscripten caveat rewritten (variable step honoured; `IsRunningSlowly` false; `SuppressDraw`/
  `ResetElapsedTime` ignored); `IsRunningSlowly` sentence; component-added rule corrected (was imprecise at B too: a component
  added later from Update/Draw is initialised); readers sentence (declared, installed per type); `UnloadContent` warnings
  (`Content.Unload()`/`Load()` there throw ODE out of `Dispose()`); `Dispose(true)` paragraph (snapshot of components;
  content disposes its assets); `IsFullScreen` row (follows window-system toggles; windowed re-centre).
- p3 touched: `wp03-game-loop-dispose-false-path` (Dispose paragraph), `wp03-game-loop-isrunningslowly` (one sentence).

### docs/content-pipeline-xnb.html
- Changes: Content-namespace note (`Load<T>` reads through `OpenStream`; `Unload()` disposes incl. shared resources —
  3d254dfa7 ISSUE-087, 39ef8ea2f) replacing "the public ladder still searches files … a copy stays valid"; test counts
  170/1,872 → 189/2,082 and pipeline 47/487 → 55/534 (the figures the coordinator already used on `content-pipeline.html`;
  the method gives 170/1,877 and 47/492 at B).

### docs/content-pipeline.html (coordinator re-verified it; delta only)
- Changes: `generateChildAssets` bullet (texture children whatever the setting; ISSUE-022 committed-not-validated);
  glTF→XNB paragraph (cameras dropped, XNB texture children, Model/clip children refused); limits row (cameras in an
  optional chunk, ISSUE-023 committed-not-validated).

### docs/cnb-format.html (coordinator re-verified it)
- Change: `MCAM` sentence marked as a change committed at this snapshot that CNA has not yet validated. `CnbLoaderRegistry`'s
  `std::invalid_argument`/`std::logic_error` hold at T.

### docs/spritebatch.html
- Basis: `SpriteBatch.cpp` (3b6a2eaf3 ISSUE-003 FIXED_PLATFORM_VALIDATION_PENDING; 9359a26b6 ISSUE-004), R7's
  `spritebatch-semantics`.
- Changes: Immediate row (each draw takes the live `SamplerStates[0]`); device-state paragraph (last texture left in
  `Textures[0]`, platform validation pending).
- p3 touched: `wp05-spritebatch-device-state`.

### docs/effects.html, docs/cnaext-extensions.html, docs/shader-effects.html
- Basis: 8f08a82cc ISSUE-007 unclosed (`SpriteBatch::Begin` refuses `ColorMatrixEffect` with `NotSupportedException` where
  the renderer does not apply it); d650554a8 ISSUE-034/035 (stock getter contract, Bones element views).
- Changes: `ColorMatrixEffect` rows on all three pages (committed-not-validated refusal); `effects.html` EffectParameter
  scalar bullet (strict stock getters, `Bones` elements). Checked: compiled-effect runtime internals still throw
  `std::runtime_error` (Fna3d/EasyGL compiled-effect sources), so the exceptions table holds.

### docs/xna-compatibility.html
- Changes: Storage table row (the "lightly tested" badge removed; XNA error types, DeleteContainer scope, sharing defaults,
  70 tests in 7 files); Net row (reliable packets exempt from simulated loss — `NetworkSimulator.cpp:54`; flags);
  `ResourceContentManager` gap rewritten (stream-only `Load`, `ResourceContentManager.cpp:18,27`; every manager honours an
  `OpenStream` override); runtime glTF samplers; `Song::FromUri` relative URIs below the title folder (963970799 ISSUE-015);
  GamerServices qualification dated and avatar wording (DIRECTX9 only under Wine); Storage bullet rewritten.

### docs/faq.html
- Changes: storage test bullet (70, mostly error/path/sharing contracts); storage sentence (XNA exception types).

### features.html
- Changes: SpriteBatch card "all 12 identities that produce pixels" → 8 (a stale renderer count the earlier pass missed) and
  the `Textures[0]` note; Storage card (System exception types instead of `std::invalid_argument`; "New:" dropped);
  capability-profile card (LOD-bias/PBR-shading features from c6dec91fb, ISSUE-006, marked committed-not-validated).

### docs/roadmap.html
- Change: doc-meta "audited against CNA snapshot c6dec91f (9 October 2026)" → 24 October 2026 (c6dec91f's date). Body
  re-read: already current (Storage 70, Media 362, gaps).

### Checked, no change
- `roadmap.html`, `about.html`: subsystem statements hold (e.g. the GamerServices local profile store is outside the IDBFS
  mounts: `LocalProfiles.cpp:205-208` uses its own path; achievements/leaderboards follow `GetStorageRootEXT()`).
- `docs/math-types.html` (already rewritten by the math pass; body holds), `docs/packed-vector.html`,
  `docs/diagnostics.html` / `docs/inspector.html` (module change e541a636f already stated; `docs/inspector.md` and
  `modules/inspector` unchanged B..T), `docs/verification.html` (storage/media counts and repair-campaign wording already
  current), `docs/c-api.html`, `docs/cna-net.html`, `docs/migrating-to-cna-net.html`, `docs/tools.html`,
  `docs/platforms.html`, `docs/3d-rendering.html` (32-bit index default still `std::runtime_error`,
  `IGraphicsRenderer.hpp:2939-2943`), `docs/graphics-state.html`, `docs/render-targets.html`, `docs/getting-started.html`,
  `docs/design-converters.html`; renderer/number pages (`building`, `native-platforms`, `link-size`, `releases`,
  `rendering-backends`, `runtime-renderer-selection`, `vs-alternatives`) scanned for subsystem statements only.

## 3. Ids and p3 regions

* No element id removed, renamed or added on any page (checked with `git diff -U0 | grep id=`). One new internal link:
  `docs/content-pipeline-xnb.html` → `content-manager.html#caching-and-lifetime` (exists).
* p3 regions touched (inside `<!--p3:begin X-->…<!--p3:end X-->` only):
  - `docs/storage.html` — `wp15-storage-container-details`
  - `docs/game-loop.html` — `wp03-game-loop-dispose-false-path`, `wp03-game-loop-isrunningslowly`
  - `docs/spritebatch.html` — `wp05-spritebatch-device-state`
* No Known Issues link added; no prose in scope names a retired KI (script check against `data/known-issues.json`).

## 4. Candidate new Known Issues (not filed)

1. **Content.Unload() in UnloadContent() during Game::Dispose() throws ObjectDisposedException** (R7 §4.1, re-confirmed):
   `modules/runtime/src/Game.cpp:1146-1176` disposes `Content_` (line 1167) before the device service, whose
   `DeviceDisposing` (raised unguarded, `GraphicsDeviceManager.cpp:447`) calls `UnloadContent()`;
   `ContentManager.cpp:364-367` refuses a disposed manager. XNA's own idiom works there. Class: bug. (Now stated on
   `docs/game-loop.html`.)
2. **The sibling version gate accepts a sharp-runtime that cannot build this snapshot's storage module.**
   `cmake/DependencyVersions.cmake:20` requires sharp-runtime "0.1.0", which the sharp-runtime `v0.1.0` tag (c20373ba) and
   41b918c9 declare, but `modules/storage/src/StorageContainer.cpp:287,337,344,355` call
   `FileStream(path, mode, access, share)`, added only in sharp-runtime c6984ece (23 October 2026, not in the tag). A
   checkout that passes the gate fails to compile the storage module with no configure-time diagnostic. Class: build
   (low; `about.html` already says the snapshot needs sharp-runtime `next`).
3. **`StorageDevice::getIsConnectedProperty()` creates the storage root as a side effect** (`StorageDevice.cpp`
   `getIsConnectedProperty` → `EnsureStorageRoot()` → `create_directories`), while fffa552ad's stated intent is that only a
   storage access creates the root. Not compared against XNA's Windows `IsConnected`; low; record as a doubt unless the
   owner confirms.

## 5. Changes needed outside this sweep's scope / generated regions (report only; not edited)

* Generated `<!--p3:issue-links-->` blocks still list retired entries (broken links found by `validate_site.py`):
  `c-api` (CNA-BUG-004), `content-manager` (021, 121), `content-pipeline-xnb` (121), `design-converters` (216), `effects`
  and `graphics-state` (GAP-033), `game-loop` and `getting-started` (244), `math-types` (001–004, 026, 027, 063, 064, 066, 251,
  252, 259), `platforms` (192), `rendering-backends` (094, 234, 271), `runtime-renderer-selection` (096), `sensors` (049),
  `shader-effects` (GAP-008), `storage` (153, 155, GAP-048, VGAP-038), `verification` (061, 063, 193, 253), `video-playback`
  (143), `xna-compatibility` (061, 157, 158, 163, 259, 264). Regeneration will clear them.
* `check_retired_renderers.py` hits on scope pages are all in generated deep-links/issue-links blocks (`cnaext-extensions`,
  `effects`, `graphics-state`, `input`, `platforms`, `render-targets`, `rendering-backends`, `runtime-renderer-selection`).
* `check_facts.py` STALE hits on scope pages are generated deep-link descriptions ("ABI 0.46.0", "14 public renderer") on
  `runtime-renderer-selection`, `verification`, `c-api`.
* `docs/sensors.html` deep-link description still says "the open Dispose(bool) defect" (R7 §5).
* `search-index.json` / `sitemap.xml` lack `docs/link-size.html` (validate_site coverage mismatch).

## 6. Open doubts

* Audio, sensors and content test figures on the pages could not be reproduced at B with the site's method (37/762 vs
  38/765; 38/534 vs 37/530; 170/1,877 vs 170/1,872); the new T figures use that method throughout.
* `docs/storage.html` describes Windows share-mask enforcement from the header and the sharp-runtime commit; CNA lists the
  Windows runtime as not yet validated, and the page says so.
* `docs/audio.html` `Stop(false)`: CNA's own test ran on SDL3_mixer; the ALSA path was syntax-checked only by its author.
* `features.html` capability-profile "31 RendererFeature ids" was left as the coordinator wrote it (c6dec91fb added ordinals
  32–34); not recounted here.

## 7. Validators (after the sweep)

* `check_retired_platforms.py`: 0. `check_source_links.py`: ok. `issue_refs.py check`: 0 errors.
* `check_retired_renderers.py`: scope hits only in generated regions (§5).
* `check_facts.py`: scope hits only in generated deep-link descriptions (§5); none from edited prose.
* `validate_site.py`: scope findings only the generated broken KI links and the search/sitemap coverage (§5); no structural
  finding on edited pages.
