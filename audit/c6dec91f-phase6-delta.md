# Phase 6 delta ledger — libcna.com → CNA `c6dec91f`

Record of the pin move from CNA `c1c316b9` to `c6dec91f` (update and cleanup, not a redesign).
Nothing in this file is served as site content (`_config.yml` excludes `audit/`); the site's pages never link to it.
This file and the fact sheets in `audit/data/facts/c6dec91f/` name the retired renderer identities; public pages
must not (section 4).

## 1. Source boundary

| Item | Value |
|---|---|
| libcna.com HEAD at session start | `bca024b` "site: Museum Simulator is playable on play.libcna.com", branch `develop`; the Phase 6 presentation baseline was inventoried from that commit (`audit/data/phase6-baseline-inventory.json`, 782 pages) |
| Old `cnahead` | `c1c316b9c7a846ce8002809c151fcd1af14942c9` (2026-10-09, then the tip of `apple/m4-stabilization`) |
| New `cnahead` | `c6dec91fbf3ef5440f60e5329e4a4758b2d80c22` + one newline — commit date 2026-10-24, on `next` (`origin/next` contains it; `origin/main` is the `v0.1.0` release) |
| Release between the two | `v0.1.0`, tagged 2026-10-10 on commit `10a4ef1cb4cd832f761536d77588000104947f8d`. `c1c316b9` is an ancestor of `v0.1.0` (22 commits before the tag); `v0.1.0` is an ancestor of `c6dec91f` |
| Ancestry and distance | `git rev-list --count c1c316b9..c6dec91f` = **834** (678 first-parent, 4 merges); `v0.1.0..c6dec91f` = **812** (656 first-parent, 4 merges); `v0.1.0-alpha.1..c6dec91f` = 4,521 (1,977 first-parent, 69 merges); `git describe` = `v0.1.0-812-gc6dec91fb` |
| Product version string | `0.1.0` (unchanged since the release) |
| How CNA was read | Git objects of the local clone (`../cna`) and the tree extracted by `scripts/extract_cna_trees.sh` into `~/.cache/libcna-com/cna-target` (stamp = `c6dec91f`). Nothing in CNA or any sibling repository was modified, built or run |
| Sibling versions at T | `cmake/DependencyVersions.cmake`: sharp-runtime 0.1.x (this snapshot needs its `next` branch; `v0.1.0` pairs with CNA 0.1.0), easy-gl `v0.1.1` (0.1.x ≥ 0.1.1), meta-gl `v0.4.1` (0.4.x ≥ 0.4.1); configure checks them (`CNA_CHECK_DEPENDENCY_VERSIONS`) |
| CNA.NET | admits exactly C ABI 0.47.0 (admitted at cna-dotnet `f1f88e1`, 2026-10-13); its CI pins CNA `next` `fbd8e64a3` (ABI 0.47.0, verified in `../cna`); it refuses 0.46.0 (the release) and 0.50.0 (this snapshot) |

## 2. Before → after

Recomputed at `c6dec91f` with the Phase 5 methods; `scripts/check_facts.py derive_from_cna` reproduces each
(details and commands: `audit/data/facts/c6dec91f/R1-renderers-platforms-numbers.md` §1).

| Fact | `c1c316b9` | `c6dec91f` |
|---|---|---|
| Commits since alpha.1 | 3,687 | **4,521** (812 after `v0.1.0`) |
| Renderer identities / families | 14 / 12 | **10 / 8** |
| Retired identities (derived) | 37 | **41** (VULKAN, DIRECTX11, METAL, SDL_RENDERER added) |
| Deliberately 2D-only identities | 1 | **0** |
| Maturity (Production / Supported / Experimental) | 6 / 5 / 3 | **3 / 5 / 2** (WEBGPU Experimental → Supported) |
| Category (Native / TranslationLayer / Software / Web / Diagnostic) | 6 / 4 / 1 / 1 / 2 | **3 / 3 / 1 / 1 / 2** |
| Per-host default | Emscripten WEBGL2, Linux OPENGLES3, else SDL_RENDERER | **Emscripten WEBGL2; Windows, macOS, iOS SDL_GPU; else OPENGLES3** |
| iOS renderer allow-list | SDL_RENDERER, METAL | **SOFTWARE, SDL_GPU** |
| Compiled-effect identities / families | 11 / 9 | **8 / 6** (FNA3D always; 5 options) |
| Texture2D / render-target format classifiers (families / identities) | 8 / 10 and 7 / 9 | **6 / 8 and 4 / 6** (derived from overriding code; section 11) |
| `GraphicsCapability` members | 19 | **17** (ComputeShaders, IndirectDraw retired) |
| `RendererFeature` / `RendererLimit` ids | 32 / 22 | **31 / 8** |
| Platform capability flags | 32 | **31** (`vulkanSurface` retired) |
| C ABI | 0.46.0 (3,210 exports, 197 structs, 1,463 integer constants) | **0.50.0** (3,212 exports, 196 structs, 1,476 integer and 11 float constants); routes generated from `modules/c-api/spec/*.toml` (56 families) |
| C ABI release gate | Not ready, 631 planned (7,053 / 15 / 631 / 443) | Not ready, **625** planned (7,032 / 15 / 625 / 453 of 8,125; 466 headers, 406 excluded) |
| C++ test files / files with macros / definitions | 813 / 781 / 11,380 | **898 / 855 / 11,898** |
| Standalone pixel programs (`examples/**/*_test.cpp`) | 781 | **598** (the retired renderers' example programs went with them) |
| CI workflow files / jobs (automatic files / jobs) | 18 / 24 (16 / 21) | **18 / 25 (16 / 22)** |
| Storage / Media test definitions | 14 / 304 | **70 / 362** |
| XNB built-in readers; XNA census | 61; 331 / 3,627 | 61; 331 / 3,627 |
| Known Issues published | 310 (191 / 60 / 13 / 46; 275 open, 35 narrowed) | **248** (147 bugs / 45 functional gaps / 12 platform limitations / 44 verification gaps; 197 open, 51 narrowed) |
| Homepage stats | 14 identities, 12 families, ABI shown via Mac stat, 11,380, 3,687 | **10, 8, C ABI 0.50.0, 11,898, 4,521** |

## 3. Decisions applied

1. **The snapshot is framed after the 0.1.0 release.** Every page that dated the snapshot "after alpha.1" now says
   "a development snapshot 812 commits after the 0.1.0 release" (footer from `scripts/site_nav.py`); the release
   history (`docs/releases.html`) separates alpha.1 → 0.1.0 from 0.1.0 → this snapshot. Values the 0.1.0 release
   still had (14 identities, C ABI 0.46.0, 24 jobs) appear only in clauses attributed to the release.
2. **Retired renderers leave no public trace** (Phase 5 rule, now for VULKAN, DIRECTX11, METAL and SDL_RENDERER):
   no "removed" notices and no history of them on public pages. The API names Vulkan, Metal and Direct3D 11 stay legal
   as other projects' drivers ("SDL's Vulkan, Direct3D 12 or Metal GPU driver", "FNA3D chooses its SDL_GPU, Direct3D
   11 or OpenGL driver", "wgpu-native drives Metal there"); "driver" is preferred to "backend" for them.
3. **The retired modern GPU layer** (compute, storage buffers/images, texture arrays, barriers, indirect draws, GPU
   timers; MRT-001..012, ABI 0.47.0) is stated once where it matters ("CNA has no compute, storage-buffer,
   indirect-draw or GPU-timer API"); it was never a renderer, so its removal may be said plainly.
4. **Evidence boundaries.** The Apple campaign of early October (physical Mac mini M4) is presented as earlier
   evidence about the CNA of that time; the macOS/iOS default (`SDL_GPU`) is described as not re-qualified on Apple
   hardware, as CNA's handoff says. Wine runs are not native-Windows evidence. CNA.NET evidence is labelled as made
   with an earlier CNA.
5. **Evidence callouts.** Pages re-verified at `c6dec91f` say "source-verified at the pinned commit" and name it;
   pages not re-verified keep `c1c316b9` and say "at the stated evidence commit" (check_facts enforces the wording).

## 4. Renderer retirement (VULKAN, DIRECTX11, METAL, SDL_RENDERER)

CNA retired four identities after the release (RRC-031..036, 13 October 2026; ABI 0.48.0 retired their constants,
values reserved; `MAXIMUM` stays 43, the next new identity takes 52).

* Tombstones (`scripts/tombstones.py`): `deep-dives/renderers/{direct3d11-and-12-resources,sdl-renderer-2d-contract,
  vulkan-deferred-state-and-descriptors,vulkan-presentation-and-readback}.html`, `development/internals/graphics/vulkan.html`,
  `docs/tutorials/85-vulkan-backend.html`. Manifest entries removed (`audit/data/deep-pages/WP09/WP10/WP11.json`,
  `scripts/dev_manifest.py`, `scripts/generate_dev_reference.py` `FAMILY_GUIDES`); every inbound link repointed.
* Rewritten in place (URL kept): `docs/tutorials/103-direct3d-windows.html` (DIRECTX9 and SDL_GPU on Windows),
  `docs/tutorials/109-metal-macos.html` (macOS on Apple silicon), the Direct3D deep dives (DIRECTX9 only), the
  native-GPU evidence tiers, the renderer reference, features, architecture (diagram regenerated by
  `scripts/make_architecture_diagram.py`), FAQ, both roadmaps, 3D rendering, effects, shader effects, render targets,
  graphics state, SpriteBatch, native platforms, runtime selection, platforms, building, verification.
* `docs/rendering-backends.html#portable-2d` became "2D games" (no identity is 2D-only).
* Guard (`scripts/check_retired_renderers.py`): VULKAN and METAL are weak words (identity-like spellings only, plus
  CamelCase class prefixes `Vulkan…`/`Metal…` except MetalKit/MetalFX); prose aliases "Vulkan renderer", "Metal
  backend", "Direct3D 11 renderer", "SDL Renderer" are flagged when presented as CNA renderers; lists owned by SDL,
  FNA3D, wgpu-native, Dawn, DXVK, vkd3d, MoltenVK, ANGLE, Mesa, Godot or bgfx, and lists that say which driver an
  abstraction selects, stay legal; the CMake option forms of the strong set (`CNA_DIRECTX11_COMPILED_EFFECTS`,
  `CNA_RENDERER_SDL_RENDERER`) and a `-D` prefix are now caught.

## 5. Other CNA changes reflected

* **SDL_GPU is the modern native path** and the Windows/macOS/iOS default; qualified on Linux and under Wine only.
  Gaps carried everywhere: `ShaderEffect` compiled out on Windows, Apple and Emscripten; no occlusion queries;
  `MultiSampleMask` ignored; a cube face in an MRT set refused (also DIRECTX9; WEBGPU refuses too); never built for
  iOS.
* **PBR everywhere:** every pixel-producing renderer reports `PbrEffectShading` and `SkinnedPbrEffectShading`
  (FNA3D through CNA's compiled PBR effects; SOFTWARE on the CPU; DIRECTX9 with SM3 shaders and shadow sampling, no
  IBL).
* **Link size and installed SDK** (LINK-001..054; `docs/link-size-architecture.md`): new page `docs/link-size.html`
  (sidebar "Link Boundaries & Size"); options `CNA_ENABLE_GAMER_SERVICES`, `CNA_OPTIMIZE_FOR_SIZE`,
  `CNA_CXX_RUNTIME_LINKAGE`; `CNA_SHARED_LIBRARY` needs CMake ≥ 3.30; SDL3_image removed (four submodules); per-type
  content loaders and XNB readers (`Load<T>()` installs what `T` needs; `RegisterAllBuiltInXnbReaders()` is no longer
  required anywhere); `docs/building.html#installed-sdk` (`CNA_INSTALL_CXX`, `cna_cpp_sdk`, components).
* **C ABI 0.47 → 0.50** (`docs/c-api.html` history rows and the new `#generated-routes` section), CNA.NET pairing
  (section 1).
* **Content:** the XNA-shaped `ContentCompiler` writes textures (incl. cube/volume), fonts, sounds, songs, effects
  and videos as `.xnb`; the CNB Model schema gained an optional `MCAM` cameras chunk (277 `cna_cnb_*` routes); compiled
  references resolve beside a relocated build; registry-configuring CLI options are refused with a pre-built registry.
* **Immediate SpriteBatch:** at `c6dec91f` EasyGL, DIRECTX9 (since `3b6a2eaf3`), FNA3D and SOFTWARE submit per `Draw`;
  SDL_GPU and WEBGPU still batch ordinary sprites (CNA-BUG-280; section 8).
* **Math:** the 2026-10-19..22 math repairs (ray–frustum clipping, frustum containment, `Matrix::Decompose` with XNA's
  algorithm, alias-safe `Transpose` and so `Plane::Transform`, wide vector lengths, XNA 16.16 `Color::Lerp`/`Multiply`,
  hashes, curves) are reflected on `docs/math-types.html`, `docs/xna-compatibility.html`, `features.html`,
  `docs/verification.html`; the framework math deep dives were re-verified separately (section 9).

## 6. Known Issues

`audit/data/facts/c6dec91f/R5-known-issues.md`. All 310 published entries were re-read at `c6dec91f` and changed only
through `patches-adversarial.json` (new repin step `c1c316b9 → c6dec91f`): **64 retired** (47 PROVEN FIXED, each with
the fixing commit, the code at T and the pinning test where one exists; 17 OBSOLETE — 14 for the renderer retirement,
CNA-BUG-094 for the modern GPU layer, CNA-GAP-003 for the removed runtime facade, CNA-BUG-271 for the deleted
`known_bugs.md`), **1 new** (CNA-VGAP-061: `SDL_GPU` is the Windows/macOS/iOS default but not qualified there),
**1 reclassified** (CNA-GAP-010 → CNA-BUG-280, a `late` reclassification so CNA-BUG-251..277 keep their numbers;
`scripts/known_issues.py` gained `"late": true`), 31 narrowed, 84 edited, 131 carried → **247 published**. Four entries
describe code whose CNA-DEMOS fix is committed but not closed (CNA-GAP-007, 035, 042, CNA-PLAT-016) and say so.
Hand-written references to retired entries on other pages were removed or reworded (`issue_refs.py check`). After the agent's pass the coordinator added **CNA-BUG-278** (NEW-PIN3-02, found by the framework-math
re-verification): since `e1377c437` an XNB `BoundingSphere`, or a Model mesh sphere, with a negative radius fails to load
because `ContentReader::ReadBoundingSphere` goes through the validating constructor, while XNA's reader and CNA's own XNB
writer accept it; and **CNA-BUG-279** (NEW-PIN3-03, found by the docs sweep): `cmake/DependencyVersions.cmake` accepts
sharp-runtime's `v0.1.0` tag, but `StorageContainer.cpp` calls the four-argument `FileStream` constructor sharp-runtime
added afterwards in `c6984ece`, so such a build passes configuration and fails to compile. Added bugs are numbered before
the late reclassification, which is therefore published as **CNA-BUG-280** (R5 says 278). The Development sweep then
showed that CNA-VGAP-058 (NEW-AUDIT-18, no test of the production audio shutdown path) no longer holds: `594d7d328`
registers `DestroyMixer` with `atexit` and adds the `CnaMixerExitOrder_*` tests; it was retired as PROVEN FIXED
(`retired_added`). Final count **248** (147 bugs / 45 functional gaps / 12 platform limitations / 44 verification gaps;
197 open, 51 narrowed); no published number moved. One further candidate was confirmed in CNA's code but not published, because XNA's own
behaviour could not be checked here: `Content.Unload()` from `UnloadContent()` during `Game::Dispose()` throws
`ObjectDisposedException` (Game.cpp disposes `Content` before the device service; `ContentManager::Unload` refuses a
disposed manager). `docs/game-loop.html` states the CNA behaviour.

## 7. Tooling changed

| File | Change |
|---|---|
| `cnahead` | `c6dec91f…` |
| `data/current-facts.json` | snapshot block (release fields, distances), every fact, `external_pinned.cna_net`, `bindings_pins` |
| `scripts/check_facts.py` | maturity/category read from `GraphicsRenderer{Maturity,Category}.hpp` (fallback to the old names); format-classifier families derived from overriding code (`families_overriding`); `c1c316b9` stale needles with a narrow 0.1.0-release excuse (`RELEASE_010`); stale needles moved to module level (`STALE_NEEDLES`, `stale_needle_findings`) so tests can feed them; a table column headed "0.1.0" / "0.1.0 release" is treated like an "Alpha.1" column |
| `scripts/check_retired_renderers.py` | section 4 |
| `scripts/test_validators.py` | current-value fixtures rebased to `c6dec91f`; the `c1c316b9` sentences became rejects (`METRIC_REJECT_PHASE6`); new `RENDERER_REJECT_PHASE6` / `RENDERER_ALLOW_PHASE6`; `stale_problems()`; ledger fixtures without DirectX 11; one Known Issues fixture for `"late": true`; three Bible-ledger fixtures for `replacement_tokens` (328 fixtures, all passing) |
| `scripts/site_nav.py` | footer text "a development snapshot N commits after the X release"; `TODAY` 2026-10-25; sidebar entry for `docs/link-size.html` |
| `scripts/validate_presentation.py` | `CNA_TARGET` = `c6dec91f` |
| `scripts/compare_presentation.py` | `--phase6` (baseline `bca024b`); `c1c316b9` source links re-pinned like older pins |
| `scripts/validate_all.sh` | runs `compare_presentation.py --phase6` |
| `scripts/build_site_indexes.py` | `UPDATED` 2026-10-25; `RETIRED_TAG` also drops search tags naming the four retired renderers (`vulkan`, `metal`, `d3d11`, `directx11`, `sdl_renderer`, …), whatever their source |
| `scripts/make_architecture_diagram.py` | 10/8, two renderer groups, 17 capabilities / 31 features / 8 limits, ABI 0.50.0, snapshot `c6dec91f` |
| `scripts/tombstones.py` | six new tombstones (section 4) |
| `scripts/deep_manifest.py`, `audit/data/deep-pages/WP09–11.json` | retired pages dropped; renderers group intro; `direct3d-shadereffect-contract` retitled "Custom HLSL ShaderEffect on DIRECTX9" |
| `scripts/dev_manifest.py`, `scripts/generate_dev_reference.py` | Vulkan internals page dropped |
| `scripts/update_tutorial_hub.py` | skips tombstoned tutorials (tutorial 85), so the hub (156 entries) and the Prev/Next chain no longer include it |
| `scripts/known_issues.py` | `"late": true` reclassifications (Known Issues agent); `TODAY` 2026-10-25 |
| `scripts/bible_ledger.py` | a SUPERSEDED concept without `tokens` is anchored by its `replacement_tokens`, checked against the destination page like tokens (before, such concepts needed a `no_tokens_reason`, which is meant for concepts that cannot be anchored lexically) |
| `audit/data/bible/records/*.json` | 79 records changed (the 154 concepts retired with the tombstoned pages, then R8) with the rewritten pages (R8): new tokens or anchors, SUPERSEDED with replacement tokens, REMOVED FUNCTIONALITY for the retired renderers and modern GPU layer, FIXED BUG / OBSOLETE where the subject is gone; `adversarial_audit.py anchors` 338 → 0 errors, `bible_ledger.py check` 0 errors, 119/119 units |
| `audit/data/phase{1..5}-dispositions.json`, `audit/data/adversarial/applied-page-fixes.json` | section 10 |
| `audit/phase3-adversarial-audit.md` | generated counts block refreshed (`adversarial_audit.py counts --write`). The historical renders `audit/bible-absorption-phase3*.md` and `audit/phase{1,2,3}-presentation-comparison.md` were deliberately not re-rendered: they record the state at the end of their phase, and `bible_ledger.py render` would stamp the current pin into the Phase 3 record |
| `scripts/check_dev_claims.py`, `scripts/check_cpp_blocks.py`, `scripts/dev_pack.py` | default target tree is `~/.cache/libcna-com/cna-target` (made by `extract_cna_trees.sh`) instead of `/rv/tmp/libcna-v2/cna-target`, an extraction of the Phase 1 pin `009d40f5`; `check_dev_claims.py` rebuilds its word list when the tree's `.extracted-from` stamp changes, and no longer flags a path the page itself says left the tree |

## 8. Evidence conflicts and how they were resolved

* **Render-target classifier count.** The Phase 5 text search counted a family whose code only mentioned
  `ClassifyRenderTargetFormatEXT` in a comment (DIRECTX9), giving 5 families at `c6dec91f`; `families_overriding`
  counts overriding definitions outside examples/tests and gives 4 (EasyGL, SDL_GPU, WEBGPU, SOFTWARE). At `c1c316b9`
  the new method reproduces the published 8/10 and 7/9.
* **Immediate SpriteBatch.** CNA's handoff §5.1 (reproduced 2026-10-17) lists SDL_GPU and WEBGPU as batching
  Immediate sprites; commit `3b6a2eaf3` (2026-10-22) says it honours Immediate on WebGPU and D3D9. In the source,
  DIRECTX9 flushes per `Draw` (`D3D9SpriteBatch.cpp:552`), but WEBGPU's `FlushPendingSpritesEXT` flushes only the
  compiled-effect batch (`WebGPURenderer.cpp:3630`), so ordinary sprites are still batched. The coordinator first read
  the WEBGPU branch as a full fix; the Known Issues agent's reading was confirmed and the pages corrected: SDL_GPU and
  WEBGPU batch (CNA-BUG-280), DIRECTX9 does not.
* **STUB and `ThreeD`.** The first draft of R1 said every surviving renderer answers `ThreeD` true; STUB answers false
  for every capability (`StubRenderer.hpp:180`). R1 corrected.
* **FNA3D Texture2D formats.** FNA3D classifies Color, NormalizedByte2/4, Single and Vector4 as supported and defers
  everything else, so DXT `Texture2D`s fall to the framework's Color-only rule (`Fna3dRenderer.cpp:402`).
* **CMake version for `libcna.so`.** Several pages said CMake 3.27; `SharedRuntimePolicy.cmake` requires 3.30.
* **CNA.NET and this snapshot.** Pages said CNA.NET admits "the version this snapshot exports"; at `c6dec91f` it
  does not (0.47.0 vs 0.50.0). `docs/migrating-to-cna-net.html` now builds the C ABI at CNA.NET's pinned `fbd8e64a3`.
* **MojoShader patches.** The site said 124; there were 128 at `c1c316b9` and 133 at `c6dec91f` (deep-dives record R2).
* **Late corrections from the ledger and page-fix reviews.** Re-reading the earlier fixes and Bible concepts against
  the rewritten pages found three statements the rewrite had missed, each corrected from the source at `c6dec91f`: the
  EasyGL diagram still said 43 direct meta-gl wrappers (32 in `EasyGLRenderer.cpp`);
  `development/internals/content/runtime.html` called the XNB reader registry unlocked (since the per-type readers it
  sits behind shared mutexes, `ContentTypeReaderManager.cpp:26-40`; the manager's own caches are still unlocked);
  `development/internals/modules/storage.html` said no test uses a non-empty glob pattern
  (`EnumerationPreservesUnicodeNamesAndReturnsOnlyLeafNames` checks `*` patterns; `?` and case are still untested).
* **Storage tests.** "One source, 14 definitions" was right at `c1c316b9` (same method); at `c6dec91f` storage has 7
  sources / 70 definitions, so the "thin area" wording was retired. Input: 50 / 540 (the page had kept a Phase 4
  figure, 47 / 523).

## 9. Process note: subagents

The owner allowed at most two concurrent subagents. Wave 1: Known Issues (R5) and Deep Dives (R2). Wave 2, as slots
freed: Tutorials (R3) and Development (R4). Each was told not to spawn subagents or forks, not to commit, regenerate
or fold, and not to edit generated regions; the coordinator applied tombstones, manifests, folds, regeneration and
validation. Agents, in order (each left a record in `audit/data/facts/c6dec91f/`):

| Record | Scope |
|---|---|
| R5 | Known Issues: all 310 entries re-read at `c6dec91f`, changed only through `patches-adversarial.json` |
| R2 | Deep Dives: renderers, graphics, build, C API, platforms (tombstones and repointed links proposed) |
| R3 | Tutorials: the 157 tutorials and the hub |
| R4 | Development: about 94 hand-written pages |
| R6 | Framework-math Deep Dives (`deep-dives/framework/`), after the math repairs of 2026-10-14..22 |
| R7 | Deep Dives sweep: every deep dive not re-verified by R2/R6 |
| R9 | Docs sweep: `docs/*.html` not edited by the coordinator |
| R10 | Development sweep: the pages R4 had delta-edited only |
| R8 | Bible absorption ledger (`audit/data/bible/records/*.json`): tokens, anchors and dispositions after the rewrite |

R1 (facts sheet) and the top-level and reference `docs/` pages were written by the coordinator. The coordinator
checked each agent's report against the source before folding it in (section 8 lists the disagreements).

## 10. Presentation-loss audit

`compare_presentation.py --phase6` (baseline `bca024b`, 782 pages): **0 unexplained losses, 654 dispositioned**
(`audit/data/phase6-dispositions.json`; report `audit/phase6-presentation-comparison.md`). By cause:

| Cause | Items |
|---|---|
| Link to a CNA path that does not exist at `c6dec91f` (mostly the retired renderers' sources, examples and CMake files; `GraphicsBackend*` headers renamed to `GraphicsRenderer*`; deleted plans and notes such as `NEXT.md`, `known_bugs.md`) | 233 |
| Known Issues entry re-verified and edited or narrowed (R5) | 138 |
| Generated backlink blocks that list fewer (retired) entries or deep dives | 74 |
| Known Issues entry retired (64 by R5, CNA-VGAP-058 by the coordinator) | 65 |
| Content about a retired renderer, including the six tombstoned pages | 38 |
| Statement rewritten because the fact changed between `c1c316b9` and `c6dec91f` | 38 |
| Source link repointed to the file that holds the code at `c6dec91f` | 35 |
| Individually justified (callouts retitled for the 0.1.0 release, superseded stats, sections renamed) | 26 |
| Audit source file, not a public page | 4 |
| Retired modern GPU layer | 2 |
| Known Issues entry reclassified (CNA-GAP-010 → CNA-BUG-280) | 1 |

The earlier comparisons still run in `validate_all.sh`, so every element this update removed that an older baseline
also held was dispositioned there too, with the same reason: phase 1 +24, phase 2 +37, phase 3 +162, phase 4 +565,
phase 5 +594 entries (all phases now report 0 unexplained losses). The adversarial page-fix ledger
(`audit/data/adversarial/applied-page-fixes.json`) records 46 earlier fixes whose text this update rewrote, each with
`superseded_by` naming this ledger and the reason (retired renderer, tombstoned page, or the fact that changed);
checking them turned up one stale number the rewrite had missed (the EasyGL diagram's 43 direct meta-gl wrappers, 32
at `c6dec91f`), now corrected.

## 11. Validation results

`./scripts/validate_all.sh` on the working tree that became `3beac92`: **overall: PASS WITH OPTIONAL EXTERNAL CHECKS
SKIPPED**. The skipped stages are `developer_ledger.py check` (no `../developer.libcna.com`) and the Bible inclusion
graph of `adversarial_audit.py` (no `../bible.libcna.com`); both are optional by design.

| Stage | Result |
|---|---|
| `test_validators.py` | 328 fixtures, 0 failed |
| `validate_site.py` | 0 issues (links, fragments, sitemap 675 URLs, metadata) |
| `validate_presentation.py` | 6 ok, 0 failed |
| `compare_presentation.py` phases 1–6 | 0 unexplained losses each (233 / 318 / 866 / 1,676 / 1,122 / 654 dispositioned) |
| `check_facts.py` | 0 problems (10 identities, 8 families recomputed from CNA `c6dec91f`) |
| `check_source_links.py` | ok (every CNA source link pinned to `c6dec91f` or on a stated moving ref) |
| `check_retired_renderers.py` / `check_retired_platforms.py` | 0 / 0 references in public content |
| `site_deep.py check`, `site_dev.py check`, `tombstones.py check` (10 tombstones) | ok |
| `check_deep_page.py --all` | every deep and Known Issues page ok; 33 warnings, each a mention of alpha.1 that was reviewed and is historical (its release notes, its tag, "alpha.1-era" behaviour) |
| `apply_expansions.py check`, `backlinks.py check`, `issue_refs.py check` | ok, 0 pages would change, 0 errors |
| `known_issues.py validate` | 248 entries, 0 errors |
| `adversarial_audit.py all` | anchors 0 errors (4,866 concepts fully anchored); issues 248; lost concepts 0 |
| `apply_page_fixes.py check` | 474 recorded (158 superseded), 0 problems |
| `git diff --check` | clean |

Also run: `bible_ledger.py check --final` (119/119 units, 0 errors, 0 warnings);
`TMPDIR=~/.cache/libcna-com/tmp ./scripts/regenerate_site.sh --check` on `3beac92` ("regeneration leaves the committed
tree unchanged"; the temporary worktree was removed).

**Browser review.** A headless Chrome driven over the DevTools protocol loaded every changed page from a local server:
753 pages at 390 × 844 (mobile) and 1400 × 900 (desktop), light scheme. The 687 live pages showed no horizontal page
overflow, no element overflowing outside a scroll container, no broken image and no console error apart from the
pre-existing Prism one (section 12); the 66 deleted Known Issues pages answered 404 as intended. Twelve key pages
(homepage, features, architecture, renderers, link size, releases, Known Issues hub and CNA-BUG-280, native-GPU
evidence tiers, tutorial 103, SDL_GPU internals, easy-gl/meta-gl) were also checked in the dark scheme at both widths
and screenshot-reviewed.

## 12. Limitations and uncertainties

* **Nothing was built or run.** Every statement was checked by reading CNA's source, CMake and Git history at
  `c6dec91f`; no CNA test, sample or renderer was executed for this update. Recorded runs the site cites are CNA's own
  records, labelled with their date and commit.
* **Platform evidence is older than the snapshot.** The Mac mini M4 campaign of early October predates the renderer
  retirement; `SDL_GPU`, now the Windows, macOS and iOS default, is qualified on Linux and under Wine only (CNA-VGAP-061).
  Windows statements rest on Wine runs, not native Windows.
* **Pages that keep `c1c316b9` evidence.** 19 Development pages were delta-edited only (stale numbers, retired
  renderers, links) and say "at the stated evidence commit": `development/handbook/index.html`,
  `development/internals/bindings/{csharp,java,python}.html`, `development/internals/graphics/easygl.html`,
  `development/internals/index.html`, `development/internals/modules/{graphics-ext,inspector}.html`,
  `development/internals/platforms/sdl3.html`, `development/reference/index.html`,
  `development/repository/source-ownership.html`, `development/takeover/{curriculum,index,investigation,mental-model,
  validation,xna-oracle}.html`, `development/testing/index.html`, `development/workflows.html`. 447 pages say
  "source-verified at the pinned commit".
* **Unpublished candidate defect.** `Content.Unload()` called from `UnloadContent()` during `Game::Dispose()` throws
  `ObjectDisposedException` in CNA (section 6). It was not published because XNA 4.0's behaviour for that order could
  not be checked here.
* **CNA-side inconsistencies found and not fixed (CNA is read-only for this update).** Commit `3b6a2eaf3` says it
  honours Immediate on WebGPU, but ordinary sprites are still batched there (CNA-BUG-280); `cmake/DependencyVersions.cmake`
  accepts sharp-runtime `v0.1.0`, which cannot compile this snapshot (CNA-BUG-279); in the sibling easy-gl, the README still says
  C++20 while its CMake requires C++23; the agents' records list smaller documentation drifts (R2, R4, R7, R9, R10).
* **Optional external checks skipped.** `developer_ledger.py check` (no `../developer.libcna.com`) and the Bible
  inclusion graph of `adversarial_audit.py` (no `../bible.libcna.com`); both are optional stages of `validate_all.sh`.
* **Pre-existing, unrelated:** the Prism script order bug recorded in `audit/maintenance-handoff.md` (C++ and GLSL
  blocks are not highlighted; it predates this update and was left for the owner).

## 13. Commits (local, on `develop`; nothing pushed)

| Commit | Content |
|---|---|
| `3beac92` docs(PIN-c6dec91f): move the documented CNA snapshot to c6dec91f | every site page, generated file, script, record and data file of this update |
| the next commit, audit(PIN-c6dec91f) | this ledger, `plan.md` and `audit/maintenance-handoff.md` |

Nothing was pushed or deployed, and no branch was reset.
