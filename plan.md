# libcna.com — CNA accuracy audit and website refresh

## Current authoritative audit: CNA v0.1.0-alpha.1

**Audit date:** 2026-08-20 (Europe/Prague)
**Detailed delta ledger:** `audit/alpha1-delta.md`

The 2026-08-11 audit below is retained as historical context only. Its renderer, test,
CI, effects, build and limitation claims are superseded by this section and the delta
ledger.

### Immutable source boundary

| Ref | Resolved commit | Result |
|---|---|---|
| BASE | `ae0be4b5211957efaef60f2f23627ae5a9ddda23` | Confirmed commit and ancestor of target |
| Tag | `v0.1.0-alpha.1` | `1bb2145d99ed572dd4eb15009c34e2e5f410fcf0` |
| Exact range | `ae0be4b5211957efaef60f2f23627ae5a9ddda23..1bb2145d99ed572dd4eb15009c34e2e5f410fcf0` | 1,445 commits; 6,803 changed paths |
| Tag date | 2026-08-20 19:06:23 +0200 | Annotated tag metadata |
| CNA HEAD at audit start | `1bb2145d99ed572dd4eb15009c34e2e5f410fcf0` | Equal to tag; zero post-tag commits |

Both revisions were inspected through temporary detached worktrees. The user's CNA
checkout was not switched, edited, reset or cleaned. Because its HEAD was exactly the
tag, it was also used read-only as the source for an out-of-source C API build whose
entire build tree lived under `/tmp`.

### Canonical alpha.1 facts

- Product version: `0.1.0-alpha.1`; Git tag: `v0.1.0-alpha.1`. The first tagged CNA
  release is an alpha prerelease, and pre-1.0 C++ APIs may change.
- Generated `CNA/Version.hpp` exposes `CNA_VERSION_*`, `CNA::getVersionMajor()`,
  `getVersionMinor()`, `getVersionPatch()`, `getVersionPreRelease()`,
  `getVersionString()` and `isPreReleaseVersion()`.
- Graphics: 50 public renderer identities, 46 implementation families, no aliases.
  EasyGL owns five identities. Thirteen identities are deliberately 2D-only; NanoVG
  and PixiJS are part of that final set. `GraphicsCapability` has 14 members, but its
  inherited defaults remain permissive enough that a positive answer is only a hint.
- The default remains a single renderer. `CNA_GRAPHICS_RENDERERS` opts into compatible
  multi-renderer builds; API choice beats `CNA_GRAPHICS_RENDERER` environment choice,
  which beats the compiled default. Selection latches on first device creation and
  fallback is opt-in.
- Host platform, audio-device selection, graphics renderer and target OS are separate axes.
  `CNA_PLATFORM` implements SDL3, SDL2, Headless and POSIX Terminal;
  `CNA_AUDIO_PLATFORM` selects SDL3, SDL2 or Null low-level device code. Only SDL3 defines
  `SOUND_ENABLED` and links the SDL3_mixer-backed XNA playback/decoding engine; SDL2 and
  Null are not high-level feature-equivalent. Reserved identifiers fail rather than falling back.
- Compiled XNA/FNA D3D9 Effect Framework bytecode (`.fxb`, XNA wrapper, XNB Effect)
  works on FNA3D by default and on explicitly enabled EasyGL, SDL_GPU and Vulkan builds.
  HLSL `.fx` source, DXBC and MGFX are different unsupported formats.
- The experimental C layer is opt-in with `CNA_BUILD_C_API=ON`; its intended targets use
  C17 while public headers are checked for C99 consumers, and it declares independent ABI
  0.7.0. The tag has 59 public C headers, 2,861 declared routes and a checked-in 6,712-row
  semantic inventory. However, its final implementation cannot compile: a 49-entry C
  renderer map is asserted against CNA's 50 canonical identities, with NanoVG missing.
  A Headless/Null-audio GCC 14.2 build with networking enabled reproduced `(49 == 50)`;
  disabling networking instead fails earlier on an unconditional GamerServices include.
  Alpha.1 therefore has a broad C source contract but no consumable native C library.
- Source inventory: 568 C++ test files and 8,263 statically discoverable
  GoogleTest-family definitions. Executed/CTest totals are configuration-specific.
- CI: 21 workflow files. Linux, Apple, Emscripten, multi-renderer, platform and declared
  C API gates have distinct scopes; native Windows D3D/GDI and Wine paths are manual. The
  intended unfiltered job and two Input rows use the invalid `EASYGL` identity and fail
  configuration at the tag; the C API final target separately fails its renderer-count
  assertion.
- XNB: 50 built-in readers with FFmpeg, 49 without it. `EffectReader` is real. CNA loads
  but does not author XNB. Runtime glTF and Media catalogue behavior remain real.
- Apple floors are macOS 13.3 and iOS 16.3. iOS is experimental and only
  `SDL_RENDERER` is allow-listed; CI final-links a device app and launches a simulator
  frame, with no physical-device or pixel claim.

### Website work

- 166 existing HTML pages changed; 102 received substantive alpha.1 content updates and
  the remainder received the release-aware global footer and/or metadata/HTML cleanup.
  The two checked-in Emscripten-generated demo shells were preserved.
- Seven public pages were added: Releases & Versioning, Runtime Renderer Selection,
  Experimental Native C API, and tutorials 126–129.
- Tutorial count grew from 125 to 129. All 125 existing tutorial pages were searched;
  72 received substantive release corrections, while every tutorial now carries the
  release snapshot footer.
- The homepage exposes the release, 50/46 renderer inventory, 568-source/8,263-definition
  test scope, 63/86 ported XNA samples and 21 workflows. The user confirmed the
  `cna-samples` repository had not changed since the prior audit.
- “Related projects & references” was expanded with public OpenEggbert ecosystem
  projects including sharp-runtime, easy-gl/meta-gl, free-direct/free-api, Easy3D,
  CNA glTF Viewer, CNA.NET, Galaxy Eggbert, Mobile Eggbert, MeshCraft, archived CNA
  Editor, FreeDirect game consumers and the public ecosystem map. Private repositories
  were not exposed, and a release-boundary warning explains independent repository cadence.
- Search and sitemap are generated from canonical HTML metadata by
  `scripts/build_site_indexes.py`. A reusable structural/link/index validator lives at
  `scripts/validate_site.py`.

### Validation record

- 175 HTML files parsed; 173 authored pages pass the HTML5 parser with zero errors. The
  two preserved Emscripten-generated shells are parsed by the tolerant pass and are an
  explicit strict-parser exemption.
- 10,083 link/resource references and 486 local fragments inspected; zero missing local
  targets or fragments.
- Zero duplicate IDs; 140 JSON-LD blocks parse structurally.
- `search-index.json`: 171 unique public pages, exactly one entry per intended page.
- `sitemap.xml`: 171 unique canonical URLs, exactly one entry per intended page.
- Metadata and canonical coverage is complete for authored site pages.

Final stale-fact and post-tag sweeps found no unintended public claim. Firefox visual QA
covered the homepage in both themes, the open mobile navigation, the expanded Related
projects section, the main renderer/platform/effects/build pages, both new reference pages,
the tutorial index, a new tutorial and the long verification page. `git diff --check` passes,
the complete 169-file tracked diff plus 10 new files was reviewed, and both temporary CNA
worktrees and the out-of-source C API build were removed. Nothing was pushed.

---

**Audit date:** 2026-08-11
**Previous audit record:** 2026-07-09 (superseded — that document's counts, feature
statuses, bugs, platform statuses, test counts, coverage estimates, sample counts and
renderer statuses are all obsolete and were NOT carried forward).

---

## 1. Source of truth

| Ref | SHA | Notes |
|---|---|---|
| CNA local `develop` | `7a64362efef4119bf880459ef1704fb2c52199e2` | working tree clean |
| CNA `origin/develop` | `7a64362efef4119bf880459ef1704fb2c52199e2` | **identical** — nothing unpushed |
| CNA `HEAD` | `7a64362efef4119bf880459ef1704fb2c52199e2` | on branch `develop` |
| CNA `master` / `origin/master` | `b080a705e34262ec4525cb3cd3096dcb5884b2fa` | behind `develop`; not used |

Commit: `integration: reconcile parallel feature lanes`, 2026-08-11 18:33:25 +0200.

Local and origin `develop` were identical, so no choice between them was required.
Analysis was performed **read-only, in place** in the existing clean checkout at
`/rv/data/development/github.com/libcna/cna`. No worktree was created, nothing was
written to CNA, no CNA branch was merged, reset or cleaned, and **no build was run**
(the environment has strict SSD-wear and RAM limits).

The "≈11 merged branches" signal corresponds to ten lane merges plus one reconciliation
commit:

```
7a64362ef integration: reconcile parallel feature lanes
b4cbb688a Merge lane 10/10: feature/portablegl        (913d39e66)
43d589e0d Merge lane  9/10: feature/openvg            (7de755c84)
fcc0df60e Merge lane  8/10: feature/svgdom            (b39037f87)
0597cd7af Merge lane  7/10: feature/fna3d             (a8cd3032a)
43966a13b Merge lane  6/10: feature/blend2d           (9709d0336)
763795ef6 Merge lane  5/10: feature/opengles2         (9faa2c6e3)
0db2347b9 Merge lane  4/10: feature/asciieffect       (70be5f515)
6acadb24a Merge lane  3/10: feature/direct2dcomplete  (53abe801d)
264be1270 Merge lane  2/10: feature/gltf              (e9336a107)
f8d9fd374 Merge lane  1/10: feature/bigcommit         (d61be1020)
```

**930** first-parent commits landed on `develop` between the previous site sync
(2026-07-09) and this SHA.

---

## 2. Method

Six parallel read-only subagent audits of the pinned CNA tree, each required to cite
`file:line` evidence and to classify confidence (Verified / Strong / Probable /
Uncertain):

1. renderers and capabilities
2. XNA API surface, content pipeline / XNB, models and glTF
3. effects, shaders and advanced graphics features
4. audio, input, devices, sensors, networking, GamerServices, storage, media, video
5. build system, platforms, tests, CI
6. known bugs, the eleven merged lanes, roadmap, sibling ecosystem

The audits were instructed to treat **CNA's own Markdown as untrusted**. That mattered:
CNA's README, `docs/coverage.md`, `known_bugs.md`, `TODO.md` and several plan files are
stale in **both** directions. Their findings were reconciled into a single canonical fact
sheet, which was the sole authority for every website edit.

Evidence order used: implementation → build configuration/headers → tests and test
registration → current generated reports → corroborated CNA docs → historical CNA docs →
the old website.

---

## 3. Headline facts established

| Fact | Old site | Current truth |
|---|---|---|
| Renderer identities | 14 "backends" | **46 renderers** (in 42 implementation families) |
| CMake option | `CNA_GRAPHICS_BACKEND` | **`CNA_GRAPHICS_RENDERER`** |
| Renderer interface | `IGraphicsBackend` | **`IGraphicsRenderer`** |
| Extension marker | `NOXNA` | **`CNAEXT`** |
| Unit tests | "4,845" | **6,818 GoogleTest case definitions** in 433 test files |
| Renderer pixel tests | "648" | **1,624** registered CTest entries tree-wide; ≤293 per build |
| Type coverage | "~99% / ~75%" | **not reproducible — removed**; 357 public types instead |
| XNB readers | 49 | **50** (49 without FFmpeg) |
| XNA oracle corpus | 39 scenes, "pixel-exact" | 39 scenes ✅ — but pixel-exact **only on `DIRECTX9`** |
| XNA samples | 63/86 | 63/86 ✅ — reworded: "ported and building", of 153 upstream |
| CI | "one auto-triggered workflow" | 8 workflows, 6 auto — but still **thin** |

**Terminology migration** (all verified against CNA source, not docs):

* `EASYGL` is no longer a public renderer name. Five public GL profiles share the
  internal EasyGL implementation: `OPENGLES2`, `OPENGLES3`, `OPENGL33`, `WEBGL1`,
  `WEBGL2`. They are not cosmetic — `OPENGLES2` and `WEBGL1` genuinely lose MRT,
  occlusion queries, `Texture3D`, instancing and multi-stream vertex input.
* `D3D9`/`D3D11`/`D3D12` → `DIRECTX9`/`DIRECTX11`/`DIRECTX12`.
* The old site's `DX3` → `FREEDIRECT`. **Trap:** a renderer named `DIRECTX3` exists
  today and is a *different* renderer (real DirectX 3, formerly staged as `DX30`).
* `ASCII` was a real renderer for 27 days and was **deliberately deleted** on
  2026-08-11. Its logic became the CNAEXT `CNA::Graphics::AsciiPostProcessEffect`,
  which is strictly better: it works through public `Texture2D::GetData()` and
  `SpriteBatch`, so it now applies on *any* renderer and to 3D-rendered sources.
* Defaults: Emscripten → `WEBGL2`, Linux → `OPENGLES3`, otherwise → `SDL_RENDERER`.

---

## 4. Status changes the refresh had to correct

### Stale NEGATIVE claims — the site said broken, the code works
1. **`Media` catalogue types are not no-ops.** `MediaLibrary` resolves real Music/Pictures
   folders, scans them, parses ID3v2/Vorbis/Opus/FLAC tags, probes durations, finds album
   art, reads playlists and saves pictures.
2. **GamerServices genuinely persists.** Achievements and leaderboard entries are written
   as JSON under `SDL_GetPrefPath()` and reload in a later process.
   `LeaderboardWriter`/`LeaderboardReader` implement real sorting, ranking and paging.
3. **`Guide::BeginShowMessageBox`/`EndShowMessageBox` and the keyboard-input pair are
   real**, with overlay rendering, password masking and mouse hit-testing. (FNA's are
   permanent stubs; CNA's are not.) Fifteen other `Guide::Show*` entry points remain
   documented no-ops.
4. **Sensors are not Android-only.** `Accelerometer` and `Gyroscope` reach real SDL3
   hardware on desktop. (`Compass`/`Motion` genuinely are Android-only.)
5. **Avatars really render** via the CNAEXT `AvatarRenderer::DrawRealEXT` path (19-bone
   rig, real GPU skinning, pixel-readback tests).
6. **`SimulatedLatency`/`SimulatedPacketLoss` are implemented** (real deferred-delivery
   queue and seeded-RNG drop) — tutorial 97 claimed they did nothing.
7. Unmentioned but real: `MediaPlayer::GetVisualizationData` (FFT spectrum + waveform),
   `VideoPlayer` audio-track playback and multi-track selection, `Microphone` capture.

### Stale POSITIVE claims — the site said fine, reality is weaker
1. **FFmpeg is a hard requirement on Linux/macOS.** Configuration fails without it. The
   old build instructions never mentioned it.
2. **Video is absent on Windows/Emscripten/Android** — the TUs are excluded, so calling
   code compiles and then fails to *link*.
3. **On the web there is no save persistence at all.** `SDL_GetPrefPath` resolves into
   volatile MEMFS; CNA mounts no IDBFS and never calls `FS.syncfs`. Saves are silently
   discarded on reload. This was documented **nowhere** — on the site or in CNA.
4. **`CNA_CNAEXT` and `CNA_DEVICES` are OFF by default.**
5. Storage/GamerServices `Begin*`/`End*` are synchronous (faithful to XNA's fake async).
6. XACT XMA/WMA does not throw — it logs and yields a null sound (silently missing audio).
7. `StorageContainer` has zero tests.
8. `Texture2D` is still `SurfaceFormat::Color`-only — **except on `SKIA`**, which has
   passed a promotion gate for the packed, float, normalized and DXT/BC7 formats.
   (The old blanket claim was checked in code rather than assumed.)

### Genuinely new capability
**Runtime glTF 2.0 loading.** Drop a `.gltf`/`.glb` into the content root and call
`Content.Load<Model>()` — no tooling step, no CMake option, vendored cgltf 1.15, with
skeletal animation, morph targets and CUBICSPLINE interpolation. The site previously
documented only the offline `gltf_to_cnj` conversion and called it "CNA's primary model
path", which is no longer true. Known limits published: runtime imports only the first
mesh group, hardcodes unit scale 1.0, silently drops rigid (unskinned) node animation,
loses factor-only PBR material properties, and performs no `extensionsRequired` check.

**PBR is real, not aspirational** — `PbrEffect` and `SkinnedPbrEffect`, consumed by 16
renderers, with per-renderer pixel tests.

### Still true, and kept
Compiled `.fx` shader bytecode remains unsupported and is the single largest XNA gap:
`Effect(GraphicsDevice&, bytecode)` throws unconditionally and `EffectReader` throws a
`ContentLoadException` before reading a byte. No HLSL/DXBC translator exists. The five
stock effects are a separate, working path. This was the old site's most load-bearing
true statement and it survives verification.

---

## 5. Deliberate editorial decisions

* **Per-renderer LOC, CTest counts and maturity badges were removed, not updated.**
  CNA has **no machine-readable maturity registry**; the two Markdown matrices that
  exist are incomplete and stale. Per-renderer CTest counts cannot be established
  without configuring 46 separate builds. Publishing them would have meant inventing
  authority the project does not have.
* **The `~99%` / `~75%` percentages were deleted rather than re-derived.** Neither is
  reproducible: CNA's own framework-wide figure is 92.7% (227/245), a one-off manual
  count from 2026-07-11 whose stated justification is now false, and the only "~99%" in
  the repo is scoped to the Input namespace alone. They were replaced with a countable
  fact (357 public types) plus the mechanism CNA actually relies on — compile-time
  signature-freeze tests and the `CNA_STRICT_XNA_API` purity mode.
* **"XNB content pipeline" → "XNB loader".** CNA only ever *reads* `.xnb` produced by
  XNA/MonoGame/FNA; producing them is explicitly and permanently out of scope.
* **File names and URLs were preserved.** `docs/rendering-backends.html` keeps its URL
  despite the terminology change, as do `docs/tutorials/72-backend-selection.html`,
  `85-vulkan-backend.html`, `86-bgfx-backend.html` and `87-custom-backend.html`. Only
  the visible titles and content changed. This is a static site with no redirect
  mechanism, so renaming would have broken every inbound link for no user benefit.
* **`known_bugs.md` is not linked and was not used as a source.** Every heading still
  marked `OPEN` there is superseded by the file's own 2026-08-09 disposition block,
  narrowed into a declared capability boundary, or moot. There are **zero genuinely open
  user-facing bugs** in it. The published limitations list was derived from the
  per-renderer capability tables and the glTF defect ledger instead.

---

## 6. Work completed

**Every one of the 141 pre-existing pages was modified — zero were left untouched.**
The site grew from 141 to 166 pages.

| Area | Pages | What happened |
|---|---|---|
| Global scripted passes | all 141 | terminology renames, footer sentence, headline numbers, 2D-only renderer lists, capability wording, `Rendering Backends` → `Renderers` link label, dead `--target CNA` command |
| Hand-rewritten in depth | 19 | `index`, `features`, `about`, `architecture`, `roadmap`, `docs/roadmap`, `contribute`, `documentation`, `docs/getting-started`, `docs/rendering-backends`, `docs/building`, `docs/platforms`, `docs/verification`, `docs/xna-compatibility`, `docs/faq`, `docs/model-loading`, `docs/storage`, `docs/sensors`, `docs/video-playback` |
| Tutorials audited file-by-file | 100 | stale renderer names, counts, build commands, platform claims, API names; Discord nav added; `dateModified` stamped |
| Tutorials created | 25 | numbered 101–125, see below |
| Index/metadata | 3 | `tutorials.html`, `search-index.json`, `sitemap.xml` |

### Renderer page restructured
`docs/rendering-backends.html` (URL preserved) now covers all 46 identities grouped into
eight families — GL profiles, standalone GL, modern GPU APIs, portable 2D/vector
rasterizers, the Windows Direct3D ladder, browser/Emscripten, portable middleware, and
CPU/no-GPU — with columns **Renderer | What it is | Scope | Platform | Dependency**.
The LOC, CTest and maturity columns were removed rather than refreshed (see §5).

### 25 new tutorials
Output of a gap analysis, not a target. Each covers a capability CNA genuinely has that
the previous set taught nowhere.

* **Renderers (101–109)** — capability querying and the fail-open trap; the five GL
  profiles; Direct3D 11/12 via MinGW + Wine/DXVK; the historical DIRECTX1–DIRECTX10
  ladder; browser-native Canvas/HTML DOM/SVG DOM; Skia/Blend2D/OpenVG; the CPU-only
  Software/PortableGL/Headless/Stub set; FNA3D; Metal on macOS.
* **3D content and extensions (110–117)** — runtime glTF 2.0 loading; the CNJ format and
  `gltf_to_cnj`; skeletal animation; morph targets; PBR materials; the CNAEXT policy and
  `CNA_STRICT_XNA_API`; CNAEXT post-process effects; the `CNA::Devices` layer.
* **Audio, media, services, verification (118–125)** — `DynamicSoundEffectInstance`;
  3D positional audio; XACT; video playback; `MediaLibrary` and FFT visualization;
  locally-persisted achievements and leaderboards; **WebAssembly gotchas**; headless and
  pixel testing with the XNA oracle corpus.

Three new sections were added to `tutorials.html` with matching jump-nav entries, and the
JSON-LD `ItemList` was rebuilt from the pages' real `<h1>` values (125 entries,
`numberOfItems` corrected from a stale 99).

### Corrections found by reading code, not documentation
* Two genuine **code bugs in tutorial examples**: `SoundEffect::CreateInstance()` and
  `ContentManager::Load<T>()` both return by value, not by pointer.
* A **renamed class the site was still teaching**: `ContentTypeReader<T>` is now
  `LooseFileContentTypeReader<T>`, with a different `Read` signature. Tutorial 46 was
  rewritten against the real class and retitled.
* Two **invalid build commands**: tutorials 20 and 100 told readers to build for the web
  with `-DCNA_GRAPHICS_RENDERER=OPENGLES3`, which is gated *off* Emscripten and fails
  configure. Both now use `WEBGL2`.
* Several **stale renderer defects** were removed after checking the code rather than
  trusting the old page: bgfx's 32-bit index-buffer corruption (`CreateIndexBuffer32` is
  overridden today) and its "only unpinned dependency" claim (now a pinned SHA).

---

## 7. Validation performed

A purpose-built validator (`validate_site.py`) checks every page for: local link
resolution, `#fragment` resolution against real `id`/`name` attributes, HTML structural
nesting, duplicate `id`s, JSON-LD parseability, search-index coverage, and sitemap
coverage.

| Check | Result |
|---|---|
| Site validator, all pages | **166 pages checked, TOTAL PROBLEMS: 0** |
| Broken local links | 0 |
| Broken local fragments | 0 |
| Duplicate IDs / malformed nesting | 0 |
| JSON-LD blocks parse | all |
| `search-index.json` parses | 164 entries |
| `sitemap.xml` parses | 164 URLs |
| Index coverage | every indexable page exactly once; `404.html` and `search.html` still excluded |
| Sitemap coverage | same set; home page still represented as `/`, not `/index.html` |
| **Description consistency** | **164 / 164** search-index descriptions byte-identical to their page's `<meta name="description">` |
| `git diff --check` | clean, no whitespace errors |
| Files changed | 144 modified + 25 new; **all `.html`/`.json`/`.xml`/`.md`** |
| `demos/` modified | **0 files** |
| Binary files modified | **0** |
| Discord nav link | 166 / 166 pages |
| CNA repository | HEAD still `7a64362e`, branch `develop`, **0 dirty files** |

The baseline before this refresh was also zero problems across 141 pages, so the
invariant was preserved rather than merely restored.

### Stale-fact sweep
Every retired value was swept site-wide and confirmed absent as a *live* claim:
`4,845`, `648`, `14 backends`, `~99%`, `~75%`, `49 readers`, `1,624`, `CNA_GRAPHICS_BACKEND`,
`IGraphicsBackend`, `NOXNA`, and the stale project statistics (`236,708 lines`,
`908 source files`, `2,738 commits`, `135,204 LOC`, `12,375 test cases`, `419 suites`,
`5,089 CTest entries`, `1,115-line parser`, `2,071-line bridge`).

Surviving occurrences of `EASYGL`, `D3D9/11/12`, `DX3`, `ASCII` and `--target CNA` were
each inspected in context and are **deliberate "this name is dead" notes** — the site now
teaches the migration explicitly, because readers arriving with stale muscle memory are
the ones most likely to hit a `FATAL_ERROR`.

Two misses were caught only because the sweep used more than one spelling: the deleted
coverage percentages had survived in a spelled-out form ("type presence is about 99%",
"functional coverage is about 75%") on three pages, and the GamerServices
"no backend of any kind / nothing is saved / leaderboard I/O throws" claim survived on
four. Both were corrected.

Two self-inflicted errors are worth recording, because both were caught only by sweeping
rather than by trusting the pipeline:

1. The renderer CTest figure was corrected from 1,624 to **1,621** on the site but *not*
   in the canonical fact sheet, so later work re-introduced the old number.
2. The canonical fact sheet listed **`SOFTWARE` among the renderers that execute a custom
   `ShaderEffect`. That is wrong.** `SoftwareEffectRenderer::CompileProgram`
   (`modules/renderers/software/include/CNA/Internal/Renderers/Software/SoftwareRenderer.hpp:509-514`)
   accepts any GLSL/HLSL/WGSL source, reports success **without compiling it**, and has
   empty `SetUniform*` bodies — the renderer's own fixed CPU shading path produces the
   pixels. `SOFTWARE` belongs with `BGFX` in the accepts-and-silently-ignores group. The
   claim had reached six pages (`docs/rendering-backends.html`, `docs/xna-compatibility.html`,
   `docs/faq.html`, tutorials 52, 72 and 116) and was corrected on all of them.

Both originated the same way: an audit classified renderers by whether
`CreateEffectRenderer` returns non-null, rather than by whether the returned object
actually compiles anything. It is a good illustration of why "the implementation is the
authority" has to mean reading the implementation, not reading a summary of it.

### Internal consistency sweep
Canonical numbers were counted across all pages and every variant inspected:
46 renderers (231 uses), 6,818 GoogleTest cases (187), 39 oracle scenes (196),
1,621 CTest registrations, 50 XNB readers, 357 public types, 433 test files — with **no
contradicting variant**. The apparent outliers (42, 14, 16, 36) are all legitimate
qualifiers: 42 implementation *families*, 14 Windows-only renderers, 16 renderers
consuming PBR, ~36 renderers with no CI coverage.

A semantic contradiction sweep confirmed no page asserts both sides of: compiled `.fx`
support, web save persistence, iOS support, `EASYGL` validity, ASCII-as-a-renderer, or
runtime renderer switching.

### Representative source inspection
Relative-path depths were verified at all three levels after the mechanical edits —
`index.html` (`css/`), `docs/effects.html` (`../css/`), `docs/tutorials/110-gltf-models.html`
(`../../css/`) — for stylesheet, nav-brand and script references.

### Not verified
**No CNA build or test run was performed**, so nothing on the site claims any suite
*passes* — only that tests exist and how many are defined. Establishing pass/fail would
require a separate configure/build/test cycle per renderer, which the environment's
SSD-wear and RAM constraints rule out.

---

## 8. CNA-side inconsistencies found (reported, NOT fixed — CNA was not modified)

These are defects in the CNA repository itself, discovered while verifying website
claims. They are recorded here for the CNA maintainer; **no CNA file was changed**.

**Blocking / high severity**

1. **CI is broken by the renderer rename.** `general-tests-ci.yml:133`, `input-ci.yml:38`
   and `input-ci.yml:43` still pass `-DCNA_GRAPHICS_RENDERER=EASYGL`. `EASYGL` is not one
   of the 46 accepted values and has no alias, so those jobs hit
   `FATAL_ERROR "CNA: Unknown graphics renderer"` at configure time. This kills the only
   full-suite job and the only ASan+UBSan leg.
2. **`cmake --build ... --target CNA` no longer works.** `CNA` became an
   `add_library(CNA INTERFACE)` umbrella in the 2026-08-10 modularization, so it is not a
   buildable target. The README prints this command **eight times**, plus six more places
   in `docs/`.
3. **README build examples use dead renderer names** — `-DCNA_GRAPHICS_RENDERER=D3D9`,
   `D3D11`, `D3D12`. Likewise `ctest -L D3D9` / `-R D3D11` / `-R D3D12` match zero tests;
   the labels are `DIRECTX9`/`DIRECTX11`/`DIRECTX12`.
4. **README's Linux prerequisites omit the hard FFmpeg requirement**, without which
   configuration fails.
5. **`tools/gltf_fixtures/builder.py` was never committed** — `.gitignore`'s `build*`
   pattern (no slash) matches the file itself. The entire fixture regenerate/verify
   workflow is inoperable. Confirmed with `git check-ignore -v`.

**Documentation vs implementation**

6. `scripts/check_renderer_identities.py:4,19` says "exactly 42 public renderer
   identities"; its own table holds 46 and it prints `OK: 46`. (42 is the *module* count.)
7. `docs/svg-dom-renderer.md:233` records a **fabricated command output**:
   "✅ `OK: 42 public renderer identities preserved`". Running it prints 46.
8. **"FreeDirect, formerly DIRECTX3"** appears at seven sites and is both historically
   false and actively confusing, since `DIRECTX3` today is a different renderer. The repo
   fixed this once (`5a6a83de0`) and the current tree has it re-broken.
9. **"No `.xnb` support"** appears in at least eleven places (`README.md:26,27,628`,
   `docs/coverage.md`, `docs/xna-4-api-coverage.md:57,288`, …) and is false everywhere —
   a complete, tested XNB loader with a hand-written LZX decompressor exists. This is the
   single most damaging stale claim in the project.
10. **"`Media` types are shells/pure stubs"** (`README.md:26`, `docs/coverage.md:56`) —
    `MediaLibrary.cpp` is 604 lines backed by real tag-parsing, indexing and FFT internals.
11. `README.md:41` and `docs/d3d9-divergence-report.md` say "31-scene corpus"; it is 39.
12. `README.md:59` says "~4,370-test unit suite"; the computed figure is 6,818.
13. `README.md:58` calls FNA differential testing "against a real, running `FNA.dll`"; it
    is a JSON value diff with no checked-in reference data and no CTest wiring.
14. `README.md:550` claims Android is "verified building **and running**" on an emulator;
    `docs/devices-build.md:245-248` says the library build is compile-only.
15. `Effect.hpp:40` says CNA "has no MojoShader-equivalent" — MojoShader is now vendored
    in-tree via the FNA3D lane (though unreachable from `Effect`).
16. `RendererSelection.cmake:122,341` reference `cmake/BackendLibraries.cmake`, deleted.
17. `docs/renderer-registry.md:70-86` omits FNA3D, SVG_DOM, OPENVG and PORTABLEGL.
18. `scripts/run-all-renderer-smoke-tests.sh` claims to cover "every renderer available"
    but hardcodes four, and builds `-j4` (above this environment's 3-job ceiling).
19. **141 occurrences of the retired macro `CNA_NOXNA`** across 20+ Markdown files; no
    such macro exists in any `.cpp`/`.hpp`/`.cmake`. The real names are `CNA_CNAEXT` (the
    CMake option) and `CNAEXT` (the always-compiled marker) — two different things the
    docs conflate.
20. `noxna_devices.md:3-5` says "Analysis only. No implementation" — all ten proposed
    `CNA::Devices` classes are fully implemented.
21. `docs/avatar-real-rendering-ext.md:41-42` describes a "~50-65 bone Mixamo-style rig";
    the shipped rig is 19 bones.
22. `TODO.md` is dead (last touched 2026-04-11) and lists as unbuilt six sensor types
    that all exist at HEAD.
23. `known_bugs.md` — three headings still marked `OPEN` are wrong or superseded (#13,
    #23, #27); the most alarming-looking entry (#1, multi-`SpriteBatch` Begin/End) is
    fixed and carries no status marker at all.
24. `modules/graphics-ext/include/CNA/Graphics/AsciiPostProcessEffect.hpp` — the doxygen
    usage example calls `device.SetRenderTarget2D(...)`, which is an **internal**
    `IGraphicsRenderer` method. The public API is
    `GraphicsDevice::SetRenderTarget(RenderTarget2D*)` (`GraphicsDevice.hpp:298`), as the
    effect's own compiled pixel test
    (`modules/graphics-ext/examples/ascii_posteffect_pixel_test.cpp`) uses. Copying the
    header's example into game code would not compile.
25. `docs/ascii-post-process-effect.md` groups `SOFTWARE` with the non-shader renderers
    where `CRTEffect`/`DepthEffect` no-op, but `SOFTWARE` does execute `ShaderEffect`.

---

## 9. Unresolved / intentionally untouched

* **External TODOs were not guessed.** Placeholder YouTube video IDs, channel details,
  APK download URLs and contact details were left exactly as they were. No IDs or URLs
  were invented.
* **Generated demo assets were not touched** — no `.wasm`, `.data`, generated demo JS or
  Emscripten shell was modified. Rebuilding the demos is outside the scope of a
  documentation refresh, so demo *descriptions* were updated but the binaries were not.
* **Sibling-project figures that cannot be defended were left qualitative.**
  `cna-bible`'s "49 chapters", `cna-examples`' "249 demos" (tool-enforced but not
  grep-reproducible), and assertion counts for `easy-gl`/`meta-gl`/`free-direct`/
  `cna-craft` (which have no test framework) are not published as test counts.
* **Nothing was run.** No CNA build or test execution was performed, so no statement on
  the site claims that any suite *passes* — only that the tests exist and how many are
  defined. Establishing pass/fail would require 46 configure/build/test cycles, which the
  environment's SSD-wear and RAM constraints rule out.
* The `SKIA` `SurfaceFormat` promotion gate is documented as a per-renderer exception;
  whether every promoted format is pixel-correct on SKIA was not independently verified.
