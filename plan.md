# libcna.com update plan — 2026-07-09

Source of truth: `/rv/data/development/github.com/openeggbert/cna` (real project state, verified
directly: `README.md`, `NEXT.md`, `docs/xna-4-api-coverage.md`, `known_bugs.md`, git log, direct
header count, `.github/workflows/`). Previous sync was 2026-07-02 (`6b4be1a`); since then CNA has
had **~1,494 more commits** (2,038 total, HEAD `c77cc0a9`, 2026-07-09) — roughly 73% of the
project's entire git history landed in the last week. This is a much bigger delta than a routine
sync; several headline stats and feature claims are now substantially out of date.

Never fabricate URLs/links/IDs/percentages — where the CNA project itself no longer publishes a
number (e.g. per-backend completion %), use its own qualitative framing instead of inventing one.

## Ground truth (verified 2026-07-09, HEAD `c77cc0a9`)

- **Public headers:** `include/` now has **440** (`.hpp`/`.h`, direct count). Was 280 (279 confirmed
  at the 07-02 baseline commit). Breakdown: 346 under `Microsoft/` (317 `Xna/Framework/`, of which
  119 are Graphics: 100 top-level + 19 PackedVector) + 94 under `CNA/` (internal backend contracts).
- **Tests:** full `ctest` (EasyGL backend): **4,522/4,525 passing (99%)**, verified fresh today
  (Task 493, commit `2233de15`). 3 known pre-existing failures, all in GPU/pixel integration tests,
  none in the pure unit suite: `EasyGL_MRT_TwoAttachments`, `EasyGL_GraphicsDevice_ReferenceStencil`
  (Task 872, open), `easy-gl-resource-smoke-tests` (vendored `easy-gl` Mesa/llvmpipe env quirk, not
  a CNA bug). Breakdown confirmed via Task 494 (`2fe45b55`): **~4,357 pure GoogleTest unit tests**
  (`tests/`, `CnaTests` target, **0 known failures**) + **388 GPU/pixel integration tests**
  (`examples/`, individually registered via `add_test()`), of which **168 are EasyGL-specific**
  (166/168 passing — the 2 EasyGL failures above). Was 1,813/1,813, 0 known failures.
- **API coverage:** headline **~85%** (EasyGL backend, 2D+3D game) is unchanged and still accurate
  (`docs/xna-4-api-coverage.md`, touched today, Task 483/490). What *did* change: the gap list.
  Touch input and XACT audio — previously cited on the site as open gaps — are now closed:
  - `Input::Touch`: **~98% behavior**, byte-faithful FNA gesture-pipeline port, fully wired
    (`feature/input` Phase I2/I9). Site currently says "GetState() returns an empty collection on
    all platforms" — **false**, fix everywhere.
  - `Audio (XACT)` — AudioEngine/SoundBank/WaveBank/Cue: **~97%**, real `.xgs`/`.xsb`/`.xwb` parser +
    SDL3_mixer playback, category/lifecycle/3D/instance-limit/fade/RPC curves all real. Site
    currently says "stub only, ~0% functional" in ~15 places — **false**, fix everywhere.
  - Remaining main gap, sitewide: **XNB content pipeline / binary content compatibility**
    (`ContentManager` ~65%, no `.xnb` parsing, custom `.model.json` instead). This should replace
    "XACT audio, .xnb content pipeline, touch input backend, GamerServices" as the single honest
    headline gap.
  - `docs/xna-4-api-coverage.md` itself still lists `GamerServices ~5%`/`Framework.Net 0%
    (intentionally excluded)` — **this specific row is stale**, contradicted directly by
    `README.md` §7 and by real files on disk (see next point). Treat the coverage-table row as an
    oversight, not ground truth, for GamerServices/Net specifically.
- **NEW major feature area — GamerServices / Net / Avatar** (not on the site at all today; kicked
  off 2026-06-30, largely landed by 2026-07-07, hardening pass ongoing per `plan_net.md`):
  - `GamerServices`: complete XNA-shaped API port (`Gamer`, `SignedInGamer`, `GamerProfile`,
    `FriendGamer`/`FriendCollection`, leaderboards, `Guide`, achievements). Local/synthetic
    semantics, not Xbox-Live-binary-compatible — same approach FNA itself uses for this namespace.
  - `Net` (`NetworkSession`): complete API surface (5 enums + 18 classes). **Real networking** for
    `SystemLink`, backed by ENet (reliable UDP, vendored) — hosting, joining, LAN discovery,
    `AppData` relay, disconnect handling, `StartGame`/`EndGame` broadcast all run over a genuine
    transport. Verified across **4 platforms**: Linux (native, 2-process loopback), Windows (WinSock2
    under Wine), Web/Emscripten (real ENet-over-WebSocket, client-only per browser sandbox), Android
    NDK (native ENet/UDP, real x86_64 emulator).
  - `Avatar` (within `GamerServices`): `AvatarAnimation`/`AvatarDescription`/`AvatarRenderer` ported
    from a decompiled real Microsoft XNA 4.0 reference assembly — FNA never implemented this at all.
  - Confirmed via real files (`include/Microsoft/Xna/Framework/Net/NetworkSession.hpp` + `.cpp` +
    tests) and `plan_net.md` (132/132 tasks closed, second hardening pass in progress).
- **Windows: now a real supported platform**, not "Planned". Via `SDL_RENDERER` backend (MSVC 2022,
  clang-cl, or MinGW-w64) — cross-compiled with MinGW-w64 from Linux and **verified running under
  Wine** (i.e. verified-but-not-on-native-hardware, same honesty tier as the site's existing
  Android "verified on emulator" framing — don't overclaim native Windows CI). Site currently shows
  "Windows: Planned" in ~7 places — fix everywhere, with the precise cross-compiled/Wine caveat.
- **Vulkan SpriteBatch multi-Begin/End bug: FIXED.** Commit `b90940090`, Task 664, **2026-07-07**.
  Root cause: `Begin()` destructively cleared vectors `End()` had just populated, plus a hardcoded
  offset-0 harvest bug. Fixed via a per-cycle `BatchSnapshot` + real running cursor; regression test
  added (`examples/vulkan_spritebatch_multi_begin_end_test.cpp`). CNA's own `known_bugs.md` **still
  lists this as open — that file is stale**, same pattern as last sync's `known_bugs.md` discovery.
  Site currently discloses this as an open "known issue" on `features.html`'s Vulkan card and
  `docs/roadmap.html` — update to "fixed 2026-07-07".
- **New Vulkan known issue to disclose** (replaces the fixed SpriteBatch one, same honesty-first
  precedent as last sync): `BlendState` is "almost entirely fake — hardcodes one blend equation
  regardless of request", confirmed 5× via pixel tests (Task 868, **open**). Also `OcclusionQuery`
  is **architecturally blocked** on Vulkan (Task 447 — deferred-draw recording can't correlate a
  query's Begin/End span to a specific deferred draw). Positive: `DepthStencilState` compare-op +
  stencil ops are now real (Task 870, 2026-07-08, previously a gap).
- **Bgfx reached full 2D+3D pixel-verified parity with EasyGL/Vulkan as of Phase 72.** Was "~82%, in
  progress". Remaining named gaps: custom `ShaderEffect` (GLSL/SPIR-V) source compilation
  unsupported (`CreateEffectBackend` returns `nullptr`); `OcclusionQuery` Begin/End wiring is real
  but pixel-verified correctness can't be confirmed in this project's sandbox (software GL 2.1
  driver, no dedicated-view architecture yet — Task 917, open). 1 known pre-existing test failure:
  `Bgfx_RenderTarget2D_MsaaResolve` (Xvfb has no DRI3 support — documented sandbox limitation, not a
  code bug).
- **No more round completion percentages per backend in CNA's own docs.** The project deliberately
  moved from "~93%"/"~82%"-style badges to a qualitative maturity ranking + named-gap list (EasyGL
  most mature → Vulkan second-most → Bgfx third-but-at-parity → SDL_RENDERER 2D-only-by-design).
  Do not invent new percentages for Vulkan/Bgfx; replace `~93%`/`~82%` UI badges with short
  maturity-rank labels sourced from the above, keeping visual structure (table cells, card badges)
  intact.
- **CI now partially exists.** Two GitHub Actions workflows added 2026-07-07:
  `.github/workflows/input-ci.yml` (matrix: EasyGL/SDL_RENDERER/Vulkan/bgfx + ASan/UBSan, runs the
  Input test suite only, triggered on `feature/input`/`develop`/`master`) and
  `devices-tests.yml` (Devices/Sensors gtest suite). **Graphics, Audio, and Net are still verified
  manually, not gated by CI.** Site's `showcase.html` says "CNA does not currently run automated
  CI" — this is now **partially false**; fix to something like "CI covers the Input and
  Devices/Sensors subsystems (GitHub Actions); Graphics/Audio/Net are still verified via manual
  local `ctest` runs, not yet gated by CI" — do not overclaim full-repo CI, it doesn't exist yet.
- **cna-samples: 48 done (was 31), out of 153 total catalogued** (source: `cna-samples/PLAN.md`
  "Sample Count Summary" table, repo HEAD 2026-07-06). Breakdown: 48 ✅ Done, 10 🔓 Unblocked
  (ready, no remaining engine gap), 28 🚧 Placeholder (blocked on a real CNA gap), 67 Ignored (never
  gets a directory — out of scope). Addressable set is 153−67=86; 48+10=58 of that 86 are done or
  ready. The site's "31 of 83 targeted" framing is superseded by this table — no historical "31"
  figure exists in `cna-samples`' own tracked history, so the old figure was likely already stale
  before 07-02. Use "48 samples ported and building, out of 153 cataloged original XNA 4.0 Game
  Studio samples (86 addressable after excluding 67 out-of-scope)."
- **Pre-existing site contradictions (independent of new CNA drift) now resolve themselves the
  right way:** root `roadmap.html` line ~177 already claims XACT audio is "Complete" — this
  contradicted `features.html`/`docs/faq.html` before, but is **now actually true** (XACT ~97%).
  Fix by updating the *other* pages to match, not by walking back `roadmap.html`. Root
  `roadmap.html` line ~286's stale "Vulkan 3D textured pipeline is the remaining gap" phrase is
  still wrong (was already stale in 07-02, missed by the last sync) — fix to reflect the real
  current Vulkan gaps (BlendState, OcclusionQuery).
- `docs/xna-compatibility.html` is the most granular page (~30 subsystem rows, a bar chart, and a
  separate "~80% functionally usable" overall estimate) — needs the most careful line-by-line pass.

## Execution approach (all complete)

1. [x] **P0a — sitewide mechanical stat sweep** (scripted, done centrally to avoid conflicting
   edits): `280`→`440` headers, `1,813`/`1813`→`4,357` unit tests across 18 files + `search-index.json`.
   Verified zero stray old figures remained afterward (one legitimate coordinate false positive,
   `280.0f`/`280, 100` in tutorial code samples, correctly left alone).
2. [x] **P0b — qualitative accuracy fixes**, split by file group and executed in parallel (6 forked
   agents with full research context): landing pages (index/about/features), architecture+roadmap
   pages, `docs/xna-compatibility.html`, showcase+FAQ+contribute, subsystem docs pages
   (audio/platforms/building/input/migration/documentation), tutorial pages with stale XACT/stub
   claims + `vs-alternatives.html`. All landed cleanly (0 HTML tag-balance issues across 142 pages).
   - [x] Removed XACT "stub/~0%" claims (15+ files) → real, ~97%, SDL3_mixer-backed.
   - [x] Removed Touch "empty collection/partial" claims → ~98%, wired gesture pipeline.
   - [x] Windows "Planned" → supported via SDL_RENDERER, MinGW-w64 cross-compiled, Wine-verified
     (only the specifically-confirmed cross-compile+Wine row was upgraded on `docs/building.html`/
     `docs/platforms.html`; native MSVC/native-Windows-MinGW rows correctly left "Planned" — not
     specifically confirmed by source facts).
   - [x] Vulkan SpriteBatch bug → fixed 2026-07-07 disclosed; replaced with real BlendState/
     OcclusionQuery gap disclosure everywhere (features.html, roadmap.html, docs/roadmap.html,
     docs/rendering-backends.html, docs/building.html, docs/tutorials/72/85/86, docs/3d-rendering.html).
   - [x] Bgfx "~82%, in progress" → full 2D+3D pixel-verified parity (Phase 72), named remaining
     gaps (ShaderEffect source compilation, OcclusionQuery sandbox-verification) — same file set.
   - [x] Added new GamerServices/Net/Avatar feature content: new features.html card, about.html
     "what problem does CNA solve" bullets + portability line, index.html status callout, root
     roadmap.html + docs/roadmap.html "what's new"/milestone entries, docs/xna-compatibility.html
     new `Microsoft.Xna.Framework.Net` section + GamerServices/Avatar row rewrite.
   - [x] cna-samples 31/83 → 48/153 (86 addressable) — showcase.html, root roadmap.html, index.html.
   - [x] CI disclosure fixed to partial (Input + Devices CI exists via GitHub Actions;
     Graphics/Audio/Net still manual) — showcase.html, docs/faq.html.
   - [x] Fixed root `roadmap.html`'s stale Vulkan "remaining gap" phrase and stale bug-name known-
     failures paragraph; left its (now-true) XACT "Complete" claim alone.
3. [x] **P1 — verification pass:** re-grepped for every old figure/claim sitewide; found and fixed
   6 files the fork file-groups had missed (`docs/rendering-backends.html`, `docs/3d-rendering.html`,
   `docs/building.html`, `docs/tutorials/72-backend-selection.html`, `docs/tutorials/85-vulkan-backend.html`,
   `docs/tutorials/86-bgfx-backend.html`) plus 2 small ones (`docs/tutorials/95-speedy-blupi.html`'s
   stale "replace XACT" instruction, `docs/audio.html`'s stale `#tier-2-stub-only-xact` anchor id).
   Also caught and fixed 2 **internal contradictions introduced by the forks themselves**:
   `features.html`'s Vulkan card listed "occlusion queries" as supported one paragraph above a
   "OcclusionQuery is architecturally blocked" known-gap note; a separate `features.html`
   OcclusionQuery feature card claimed it was "implemented... on Vulkan" outright — both fixed to
   consistently say Vulkan's `OcclusionQuery` is blocked. Also fixed
   `docs/tutorials/86-bgfx-backend.html`'s "What's limited" list, which still said `OcclusionQuery`
   was "stubbed... returns 0 always" one paragraph below text I'd already corrected to say the
   Begin/End wiring is real. Fixed a genuinely pre-existing (not CNA-sync-related) dead link in
   `docs/vs-alternatives.html`: it said a MonoGame/FNA migration guide was "planned" via a
   commented-out link, when `docs/migration-from-monogame.html` already exists — linked it.
   Also fixed 2 stale `search-index.json` description fields the file-level sweep didn't reach
   because they aren't sourced from any single page's own meta tags. Final re-sweep: zero stray
   instances of `280`/`1,813`/`93%`/`82%`/`31 of 83` anywhere in the repo; 0/142 pages have
   unbalanced HTML tags; `search-index.json` parses as valid JSON.
4. **P2 — carry forward from last sync, still open, not touched, do not guess:**
   - `cna.openeggbert.com` vs `libcna.com` relationship — no response received last time either.
   - TODO placeholders needing real values: `videos.html` YouTube IDs/channel, `contact.html`
     Android/Play Store + author contact + cna-demo link, `demos.html` APK download links.
5. Commit only after user confirms (per this session's git safety rules) — do not push without
   explicit request.

## Out of scope but flagged once

- `known_bugs.md` in the `cna` repo is stale (still lists the fixed SpriteBatch bug) — not a
  website task, flag to Robert.
- `docs/xna-4-api-coverage.md`'s `GamerServices ~5%` / `Framework.Net 0%` row in the `cna` repo
  itself contradicts `README.md` §7 and real files — likely an oversight from a doc pass that
  didn't touch the Net-track rows. Not a website task, flag to Robert.
- `README.md` §6 (Backend System) still calls Vulkan "incomplete, TODO/stub areas", contradicting
  its own §1 Project Status ("real, working 3D rendering... second-most mature"). Not a website
  task, flag to Robert.
- `sitemap.xml` (138 URLs) has drifted from the actual 142-page site (gap predates this sync too,
  not touched by 07-02 sync either) — low priority, not attempted this round unless time remains.
