# Phase 7 delta ledger — libcna.com → CNA `3b43bd86`

Record of the pin move from CNA `c6dec91f` to `3b43bd86`: an incremental update, not a re-audit of Phase 6.
Nothing in this file is served as site content (`_config.yml` excludes `audit/`). The detailed records are in
`audit/data/facts/3b43bd86/`: `00-editorial-guide.md` (rules for this phase), `R1-facts-and-changes.md` (every fact and change
of the interval, with commits and evidence), `R2-deep-dives.md`, `R4-development.md`, `R5-known-issues.md` (per-area reviews),
`worklist.json` and `topics.txt` (the evidence intersection, section 3).

## 1. Source boundary

| Item | Value |
|---|---|
| libcna.com HEAD at session start | `9c6d76e` "site: load prism-c before the Prism components that extend it" (the Prism fix after Phase 6), branch `develop`, clean; the Phase 7 presentation baseline was inventoried from it before any edit (`audit/data/phase7-baseline-inventory.json`, 721 pages) |
| Old `cnahead` | `c6dec91fbf3ef5440f60e5329e4a4758b2d80c22` (2026-10-24 10:23 +0200) |
| New `cnahead` | `3b43bd8687ed46523d873f9bec4b32bd8481dcb5` + newline — 2026-10-27 17:18 +0100, "test(RTS-001): measure EasyGL custom 3D render-target sampling", on `origin/next` |
| Ancestry | `git merge-base --is-ancestor c6dec91f 3b43bd86` → true; `git rev-list --count c6dec91f..3b43bd86` = **136** (136 first-parent, 0 merges) |
| Diff | `git diff --shortstat c6dec91f 3b43bd86`: **1,052 files, +17,805 / −55,092** (deletions: 355 avatar catalog files that moved to a submodule, 147 `cmake/patches` files — the FNA3D/MojoShader series now commits on CNA's forks, two SDL patches now upstream, three renamed —, the retired `misc/` and `plans/` documents, three root campaign handoffs, ENet's patched copy replaced by upstream) |
| Distance to the release | **948** after `v0.1.0` (792 first-parent, 4 merges; `git describe` = `v0.1.0-948-g3b43bd868`); 4,657 after `v0.1.0-alpha.1`; `git diff --shortstat v0.1.0 3b43bd86` = 6,383 paths (alpha.1: 10,273) |
| Product version / C ABI | `0.1.0` (`CMakeLists.txt`, empty pre-release) / `0.50.0` (`abi.h`) — both unchanged; no 0.1.1, no 0.51.0 |
| How CNA was read | Git objects of `../cna` (its working tree is one commit past T, `421a38e4f`, and was never read) and `~/.cache/libcna-com/cna-target` (`extract_cna_trees.sh`, stamp T). Read-only clones consulted: `../FNA3D`, `../mojoshader` (the forks), `../cna-avatar-assets` (the catalog), `../cna-dotnet` (`develop` `90b11a2`), `../sharp-runtime` (`next` `4e146b90`), `../cna-gamer-services-server`. Nothing in CNA or any sibling repository was modified, built or run |
| CNA.NET | still admits exactly C ABI 0.47.0 (`eng/cna-native-abi-policy.json` at `90b11a2`); refuses 0.46.0 and 0.50.0, so it does not consume this snapshot either |

## 2. Before → after (canonical facts)

Recomputed at `3b43bd86`; `scripts/check_facts.py derive_from_cna` reproduces every value it derives (method per value in
`data/current-facts.json`, detail in R1 §1).

| Fact | `c6dec91f` | `3b43bd86` |
|---|---|---|
| Renderer identities / families; maturity; category | 10 / 8; 3/5/2; 3/3/1/1/2 | **unchanged** |
| Compiled-effect identities / families; format classifiers | 8 / 6; 6/8 and 4/6 | **unchanged** |
| `GraphicsCapability` members / platform capability flags | 17 / 31 | **unchanged** |
| `RendererFeature` / `RendererLimit` ids | 31 / 8 | **33** / 8 (MultiSampleMask 35, RenderTargetReadback 36) — newly derived |
| C++ test files / with a counted macro / definitions | 898 / 855 / 11,898 | **900 / 857 / 11,927** |
| Standalone `examples/**/*_test.cpp` | 598 | **599** |
| CI workflow files / jobs | 18 / 25 (16 / 22 automatic) | **unchanged** (`.github` untouched) |
| XNA census; oracle scenes; XNB readers | 331 / 3,627; 39; 61 (60) | **unchanged** |
| C ABI; headers; routes; structs | 0.50.0; 60; 3,212; 196 | **unchanged** |
| ABI baseline integer constants | 1,476 | **1,478** (two feature constants added *at the same version*) — newly derived |
| C ABI release gate (public C++ declarations, not routes) | 8,125 = 7,032 / 15 / 625 / 453 | **8,134 = 7,033 / 15 / 633 / 453**, still Not ready — newly derived |
| Avatar catalog | v3 revision 4, in-tree | **v3 revision 5**, submodule `cna-avatar-assets` `4617a1e7503f` — revision newly derived |
| Known Issues | 248 (147 / 45 / 12 / 44; 197 open, 51 narrowed) | **249** (145 / 47 / 13 / 44; 195 open, 54 narrowed) |
| Homepage stats | 812 commits since 0.1.0, 11,898 definitions | **948, 11,927** |

## 3. Method: an incremental update with an evidence intersection

The pin-move procedure (`development/handbook/update-libcna-com.html`) asks for the intersection of the CNA paths each page cites
with `git diff --name-only OLD NEW`. It was scripted for this move and is now `scripts/evidence_worklist.py`:

* every page with a `dev-evidence` callout gets the cited CNA files that changed in a way that can matter (code, Markdown/JSON,
  public-header doc comments), the cited files whose change only reworded a comment (most `.cmake`/`.cpp` edits of the interval
  removed `plans/plan_vulkan_parity.md` references), and the interval topics found in its text (`topics.txt`);
* **carry** (nothing cited changed, no topic): 28 pages; 24 moved their callout mechanically, `development/maintenance.html` was
  rewritten for this phase and reviewed in full, and 3 `c1c316b9`-labelled pages kept their label (only their doc-meta line, which
  names where links are pinned, moved); **review**: 182 non-Known-Issues pages, all read against the diff (91 Deep Dives by the Deep
  Dives agent, 85 Development pages by the Development agent, `development/handbook/update-libcna-com.html` by the coordinator, and the
  five generated reference pages regenerated by `generate_dev_reference.py`);
* pages without callouts (`docs/`, tutorials, top-level) were swept by targeted searches for every stale claim the interval could
  have produced (R1 topics, the c6dec91f values, deleted paths) and corrected; their "snapshot c6dec91f" labels then moved, while
  statements of what was done at `c6dec91f` ("re-checked at", "unchanged at", "syntax-checked at an earlier snapshot") stay as
  history (several gained "and at 3b43bd86" where the cited module is byte-identical in the interval).

Result: every reviewed page says "source-verified at the pinned commit … `3b43bd86`" (112 Deep Dives, 79 Development, all
Known Issues pages); the 19 Development pages already labelled "at the stated evidence commit … `c1c316b9`" keep that label,
with any sentence the interval made wrong corrected (R4). No page was left on `c6dec91f`.

Mechanical steps: `cnahead`; 5,645 CNA source links re-pinned where the path exists at T (9 links to vanished files repointed by
hand to their successors, R1 §9); the footer sentence on all 688 pages (the hand-written pages carry their footer, so it was
replaced with `site_nav.FOOTER_SNAPSHOT` verbatim); `img/architecture-diagram.svg` and `mermaid-diagram.png` regenerated
(`make_architecture_diagram.py --png`: 33 features, snapshot 3b43bd86).

## 4. What changed on the site, by area (R1 holds the CNA evidence)

* **FNA3D and MojoShader are CNA's forks** (libcna/FNA3D `10f650b9d0f6`, libcna/mojoshader `03b686fe1a33`; upstream FNA-XNA/FNA3D and
  icculus/mojoshader are ancestors; verified in the local fork clones). Every "patch series applied at configure time" statement
  rewritten (build architecture, repository map, source ownership, build-configuration handbook, Building, renderers page,
  tutorials 108 and 128, deep dives); the pin-pair logic (`Fna3dSourcePin.cmake`), the read-only source check and
  `CNA_FNA3D_ALLOW_SOURCE_DRIFT`, old `_deps/fna3d-src` trees, static linking, `BUILD_SHARED_LIBS` restore, the C++ SDK bundling FNA3D
  only with the FNA3D renderer, and how the forks follow upstream (merge, never rebase). The forks are never called upstream.
* **SDL `86296ac8`** with five platform-specific patches (the two Vulkan patches are upstream; macOS unpatched), the Android
  asset-enumeration patch (not yet run on Android), the Vulkan mip-extent patch; **SDL_shadercross** keeps one build-integration patch
  applied only to the build tree's clone or a staged copy; **`CNA_VENDORED_SOURCE_CHECK`**; the SDL prebuilt manifest now covers the
  toolchain, and build trees watch the shared install (a running build is still unprotected: `CNA_SDL_PREBUILT_ROOT`).
* **ENet** is unmodified upstream master `5a9c537f`, vendored (never a submodule); its configure message was fixed (CNA-BUG-191 retired).
* **Avatars**: catalog v3 **revision 5**; the `cna-avatar-assets` submodule, required at configure time while Gamer Services is on
  (not in a source archive); five submodules in every clone instruction (Building, Getting Started, tutorials 02, 80, 131, 160,
  contribute, releases); the current evidence record (revision 4 review 982 frames; revision 5 acceptance on eight renderers,
  36-view regression on six; Windows only through translation layers, not for revision 5); link-size 22.3 MB deflated (the
  site's "13 MB" was CNA's own stale figure); tutorial 168 imports only `v3` (its v1/v2 loop was wrong since 2026-10-15).
* **Renderers**: SDL_GPU and WEBGPU order an upload after the queued draws that sample it, so `SpriteSortMode::Immediate` is
  per-draw there (the "one open defect" removed from features, roadmaps, verification, renderers, tutorials 103, 131, 132,
  contribute); SDL_GPU binds cube faces in any MRT slot (only WEBGPU and DIRECTX9 refuse); SDL_GPU MultiSampleMask is all-or-none
  with partial masks refused; XNA integer pixel centres on multisampled targets (seventh real-XNA probe); `RendererFeature` 33
  (tutorials 101, 133 and nine other pages); FNA3D VFACE sign, bump environment, effect struct defaults; SDL_GPU emissive × vertex
  colour; `new PresentationParameters()` is XNA's 0x0 full-screen default with CNAEXT `CreateWindowedEXT` (tutorial 131's sample
  updated and syntax-checked; Game/`GraphicsDevice()` internals corrected).
* **C API**: SPIR-V modules accepted byte for byte by `cna_shader_effect_create`; the 0.x consumer rule (`hello_cna.c` now refuses
  another 0.x minor); `cna_presentation_parameters_init` XNA defaults; the two feature constants added under 0.50.0; release-gate
  inventory 8,134 / 7,033 / 15 / 633 / 453.
* **Content pipeline**: `XmlSerializer` for Color/Rectangle/Point (needs sharp-runtime `next` ≥ `f990d074`), build-wide generated
  nested names, the XNA-typed `BuildAndLoadAsset<TextureContent, TextureContent>`, Pipeline Workshop exception semantics;
  content-pipeline test definitions 534 → 541.
* **Documentation relocation**: links and mentions of `misc/*.md`, the seven deleted plans and the three removed handoffs repointed
  to their successors (`docs/cnj-format.md`, `docs/binding.md`, `docs/consoles.md`, `docs/location-proposal.md`,
  `docs/build-performance.md`, …); `docs/consoles.md` and `docs/location-proposal.md` are not presented as platform or device support.
* **Releases page**: the snapshot block, distances and path counts (with the method), a third-party-sources row and a
  `PresentationParameters` row in the 0.1.0 → snapshot table.

## 5. Known Issues (R5)

248 → **249**. Retired 4: CNA-BUG-191 (PROVEN FIXED, `c59a91c00`), CNA-BUG-245 (OBSOLETE: `misc/` removed), CNA-BUG-256 and
CNA-BUG-272 (PROVEN FIXED by the rewritten docs). Added 5: CNA-PLAT-019 (FNA3D refuses tangent-free PBR on its SDL_GPU/D3D11
drivers), CNA-GAP-075 (MojoShader SPIR-V refuses eight SM1.x instructions), CNA-GAP-076 (WEBGPU and DIRECTX9 refuse a cube face in an
MRT set), CNA-BUG-281 (MojoShader's Direct3D 11 glue: packed ps_3_0 inputs, substring semantic match; R9-01/R9-03), CNA-BUG-282
(`RendererFeature::MultiSampleMask` misreports EasyGL without `glSampleMaski` and WEBGPU on Metal). Narrowed 6, among them
**CNA-BUG-280**: fixed for SDL_GPU and WEBGPU (`d9b513ee0`, `96577db26`), it now describes only FNA3D's SDL_GPU driver (a TextureCube,
Texture3D or mipmapped Texture2D changed between two draws shows its new contents in the earlier draw), so one defect keeps one id.
Edited 15 (incl. CNA-BUG-279, now also needing sharp-runtime `f990d074`; CNA-BUG-058/GAP-062 counts; the four CNA-DEMOS entries whose
issues CNA closed on `6c8b042c4` but whose published scope lies outside the fix). Carried unchanged after re-reading: 223, incl.
CNA-BUG-278 and CNA-VGAP-061 (SDL_GPU still unqualified on native Windows, macOS and iOS). No reclassification; **no published id
moved** (checked by merging before and after each addition). The repin step `c6dec91f → 3b43bd86` was appended after every entry was
re-checked.

## 6. Tooling changed

| File | Change |
|---|---|
| `cnahead`, `data/current-facts.json` | pin; snapshot block; recomputed facts; new `renderer_feature_ids`, `c_api_integer_constants`, `c_api_coverage`, `avatar_catalog`, `avatar_catalog_revision`; changed-path counts with method; CNA.NET pairing re-read |
| `scripts/check_facts.py` | derives RendererFeature ids, ABI integer constants, the release-gate inventory (COVERAGE.md) and the avatar catalog revision (`CATALOG_REVISION`, since the catalog is a submodule); six page checks for them; `c6dec91f` stale needles; the Phase-1 `BASE` excuse matched in capitals only (it excused any sentence with "baseline") |
| `scripts/known_issues.py` | `"after_added"` anchors a late reclassification after a named added entry (CNA-GAP-010 → CNA-BUG-280 after `NEW-PIN3-03`), so new bugs no longer renumber it; `TODAY` |
| `scripts/check_source_links.py` | validates pinned links into libcna/FNA3D and libcna/mojoshader against the local clones |
| `scripts/evidence_worklist.py` | new: the per-page evidence intersection (section 3) |
| `scripts/test_validators.py` | five fixtures rebased to T; `METRIC_REJECT_PHASE7` (13) / `METRIC_ALLOW_PHASE7` (5); the anchored-reclassification fixture (3 cases) — 363 fixtures |
| `scripts/compare_presentation.py`, `scripts/validate_all.sh` | `--phase7` (baseline `9c6d76e`); `c6dec91f` links re-pinned like older pins |
| `scripts/validate_presentation.py`, `site_nav.py`, `build_site_indexes.py`, `make_architecture_diagram.py` | `CNA_TARGET`; `TODAY`/`UPDATED` 2026-10-27; diagram labels |
| `audit/data/bible/issues/patches-adversarial.json` | section 5 (the only hand-edited Known Issues file) |
| `audit/data/phase{1..7}-dispositions.json` | section 8 |

## 7. Evidence conflicts and decisions

* **CNA-BUG-280: retire or narrow?** CNA's handoff §5.1 lists no open defect, and the Deep Dives agent suggested closing the entry.
  The same defect class survives on FNA3D's SDL_GPU driver (handoff §5.3, `texture_setdata_after_draw` leg B fails there), so the
  entry was narrowed to that case instead of retired plus re-added.
* **Feature constants inside 0.50.0.** `c6dec91f` already reported ABI 0.50.0 without `CNA_RENDERER_FEATURE_MULTI_SAMPLE_MASK`/`_RENDER_TARGET_READBACK`;
  CNA added them later without a version change and `ABI_VERSIONING.md` lists them under 0.50.0. Whether `c6dec91f` was ever the
  public tip without them could not be established, so no Known Issue was published; `docs/c-api.html` says plainly that they came
  later under the same version.
* **Generated nested names.** XNA's `BuildCoordinator` term is `stub_N`; CNA generates `<derived>_<index>` (CNA's own comments say
  `stub_N`). Pages use CNA's form and name XNA's rule.
* **Pre-existing errors found and corrected** (wrong before this interval): `docs/xna-compatibility.html` called Alpha8 render targets
  refused (they fall back to Color); `docs/render-targets.html` said HEADLESS refuses a cube face in an MRT set (it accepts it);
  `contribute.html` listed SDL3_image as a submodule, 781 pixel programs, and `known_bugs.md`/`TODO.md`; the build-configuration
  handbook said the C++ framework has no install rules (`CNA_INSTALL_CXX` exists); the update-libcna-com facts table held
  `c1c316b9` values (14 / 12 / 1 / 19); tutorial 168 imported catalogs v1 and v2 that CNA stopped shipping on 2026-10-15; the
  Development agent's list in R4 (terminal capabilities, a non-existent `DrawPrimitivesIndirectEXT`, shader-package counts).

* **Final adversarial sweep** (after validation passed): every remaining `c6dec91f` on a public page was read in context. Three were
  wrong rather than historical and were corrected: `development/takeover/index.html` said the Development links target `c6dec91f`
  (beside "948 commits"), and the C# and Java binding tours named `c6dec91f` as the snapshot declaring ABI 0.50.0. The rest are dated
  measurements or statements of what was read at that commit. Searches for ABI 0.51/0.1.1, upstream-fork confusion, ENet as a
  submodule, revision 4 as current, removed avatars, Immediate batching, SDL_GPU ignoring the mask or refusing cube faces, and
  hardware-qualification claims found nothing current. The generated CMake option index quotes CNA's own docstring for
  `CNA_RENDERER_FNA3D` ("FNA-XNA/FNA3D + MojoShader"), which CNA did not update with the forks (section 11).

## 8. Presentation-loss audit

`compare_presentation.py --phase7` (baseline `9c6d76e`, 721 pages): **0 unexplained losses, 51 dispositioned**
(`audit/data/phase7-dispositions.json`, 48 entries; report `audit/phase7-presentation-comparison.md`). By cause:

| Cause | Items |
|---|---|
| Link to a CNA path gone at `3b43bd86`, or a source no longer supporting a narrowed entry (the old SDL patch names, `cmake/patches` as the home of a MojoShader patch, `avatar_visual_regression_check.py`, deleted plans, `misc/`, the EasyGL/DIRECTX9 sources of CNA-BUG-280, the SDL_GPU example list of CNA-PLAT-002) | 22 |
| Tombstone pages (retired in Phases 5/6) that the `9c6d76e` inventory recorded as pages | 10 |
| Known Issues entry re-verified and edited or narrowed (title changed) | 6 |
| Known Issues entry retired (CNA-BUG-191, 245, 256, 272) | 4 |
| Generated "Known issues in this area" blocks listing the retired entries | 4 |
| Individually justified: the contribute card and its heading on Immediate sprites (fixed; replaced by the remaining FNA3D upload-ordering item), a Building heading extended for the avatar submodule, the release-gate figure 625 → 633, a link that went with a pre-existing false sentence about indirect-draw declarations | 5 |

The earlier comparisons still run in `validate_all.sh`; elements this update removed that an older baseline also held were
dispositioned there with the same reasons: phase 2 +1, phase 3 +4, phase 4 +18, phase 5 +24, phase 6 +24 entries (all phases report 0
unexplained losses). The Bible absorption ledger: 11 concept records had their tokens or replacement tokens moved to the rewritten
text (FNA3D forks, Immediate per draw, SDL_GPU mask, 33 features, test counts, gate figures, plans count, handoff date,
`gtest_discover_tests` calls) and CNABUGS-050 became FIXED BUG with CNA-BUG-256; `adversarial_audit.py anchors` 15 → 0 errors.
20 expansion regions edited in place were folded back (`apply_expansions.py fold`, then `check`: ok).

## 9. Process: subagents

At most two concurrent subagents, each told not to spawn subagents or forks, commit, regenerate or edit generated regions. Wave 1:
Known Issues (R5) and Deep Dives (R2); wave 2, when the Known Issues slot freed: Development (R4). The coordinator wrote R1, the
editorial guide and the worklist, edited `docs/`, tutorials, top-level and the dependency-architecture Development pages, carried the
28 carry pages, added CNA-BUG-281/282 and the `after_added` option, and checked each agent's report against the source before folding
it in (spot checks: the narrowed CNA-BUG-280, the agents' recounts of `plans/`, `add_test(`, `gtest_discover_tests(` calls and
metagl wrappers, the two MultiSampleMask misreports).

## 10. Validation results

`./scripts/validate_all.sh` on the final working tree: **overall: PASS WITH OPTIONAL EXTERNAL CHECKS SKIPPED**. The two skipped stages
are optional by design and their inputs are absent on this machine: `developer_ledger.py check` (no `../developer.libcna.com`) and the
Bible inclusion graph of `adversarial_audit.py` (no `../bible.libcna.com`). No repository was created to satisfy them.

| Stage | Result |
|---|---|
| `test_validators.py` | 363 fixtures, 0 failed (344 before Phase 7) |
| `validate_site.py` | 688 HTML files, strict HTML5 parse of 688 authored pages, 68,008 references and 7,910 fragments resolved, 0 duplicate ids, 672 JSON-LD blocks, search index and sitemap 676 entries each, unique and complete, metadata complete; Prism dependency order checked on every page |
| `validate_presentation.py` | 6 ok, 0 failed |
| `compare_presentation.py` phases 1–7 | 0 unexplained losses each (233 / 319 / 870 / 1,684 / 1,135 / 667 / 51 dispositioned) |
| `check_facts.py` | 0 problems (every derived value recomputed from CNA `3b43bd86`) |
| `check_source_links.py` | ok (CNA links pinned to `3b43bd86` or a stated revision; 60 binding and fork links checked against local clones) |
| `check_retired_renderers.py` / `check_retired_platforms.py` | 0 / 0 |
| `site_dev.py check`, `site_deep.py check`, `tombstones.py check` (10) | ok |
| `check_deep_page.py --all` | every deep and Known Issues page ok (the warnings are the reviewed historical mentions of alpha.1) |
| `apply_expansions.py check`, `backlinks.py check`, `issue_refs.py check` | ok; 0 pages would change; 11 issue references, 0 errors |
| `known_issues.py validate` | 249 entries, 0 errors |
| `adversarial_audit.py all` | anchors 0 errors (4,865 concepts fully anchored), issues 249, lost concepts 0, counts current |
| `apply_page_fixes.py check` | 474 recorded (158 superseded), 0 problems |
| `git diff --check` | clean |

Also run: `bible_ledger.py check` (119/119 units, 0 errors, 0 warnings); `check_dev_claims.py` (0 errors on every Development page;
the warnings are names outside CNA's index, such as this repository's own script names); `check_snippet.sh` on tutorial 131's
changed sample (syntax-only, against the target headers and sharp-runtime `next`: clean); `regenerate_site.sh` ran in place and was
re-run for the Known Issues additions (see section 12 for the reproducibility check on the committed tree).

## 11. Limitations and uncertainties

* **Nothing was built or run in CNA.** Every statement was checked by reading CNA's source, CMake and Git history at `3b43bd86`; test
  results on the site are CNA's records with their dates and commits. One code sample (tutorial 131) was syntax-checked against the
  target headers (`check_snippet.sh`, g++ `-fsyntax-only`).
* **Platform evidence is unchanged in kind:** SDL_GPU remains unqualified on native Windows, macOS and iOS (CNA-VGAP-061); Windows
  evidence is Wine; Android was not rebuilt at the FNA3D pin and the Android SDL patch has not run on Android; the avatar review on
  Windows translation layers predates revision 5.
* **Avatar catalog** values were checked twice: against CNA's committed documents and generator (`CATALOG_REVISION = 5`) and against
  the submodule commit in the local `../cna-avatar-assets` clone (catalog.json revision 5; tree byte-identical to CNA `bdaeaff01`'s
  in-tree v3). The local clones of the forks and the asset repository were not fetched; their commits were present.
* **Optional external checks** (`developer.libcna.com`, `bible.libcna.com`) are absent; see section 10.
* **Browser review.** Headless Chrome (`scripts/browser_qa.py`, profile in the session scratchpad) loaded all 678 changed pages from a
  local server at 1400 and 390 px, light scheme: no horizontal page overflow, no broken image and no console error on any of the
  1,356 loads; the flags are pre-existing presentation debt (Prism's green CMake tokens and the 404 home link at low contrast, and two
  intended literal angle-bracket texts). On the 335 changed pages with code blocks every C++ (1,072), GLSL (49), C (7), CMake (39) and
  JSON (25) block was highlighted; the unhighlighted blocks are languages those pages load no Prism component for (YAML, INI, Python,
  Groovy, plain text) or bash one-liners with nothing to tokenize, none changed here. Thirteen key pages were also checked in the
  dark scheme at both widths (no overflow, no console error) and two were screenshot-reviewed.
* **CNA-side drift noticed, not fixed (CNA is read-only):** CNA's README lists four submodules; `DependencyVersions.cmake` accepts
  sharp-runtime 0.1.0 though this snapshot needs `f990d074` (CNA-BUG-279); `plans/plan_xnb.md` banner vs body (CNA-BUG-228); the two
  feature constants under 0.50.0 (section 7); `StockVertexSemantics.hpp` still documents absent inputs as (0,0,0,1) although EasyGL
  reads an absent colour as white since `17cd5d3c3`; CNA's comments say `stub_N`; `RELEASE_GATE.md` and `plan_binding.md` counts
  disagree with the generated 633 (CNA-BUG-058); `modules/renderers/CMakeLists.txt` still says three SDL families; the `CNA_RENDERER_FNA3D` option's docstring still names
  FNA-XNA/FNA3D; the agents' records list smaller drifts.

## 12. Commits (local, on `develop`; nothing pushed or deployed)

| Commit | Content |
|---|---|
| `9a6867e` docs(PIN-3b43bd86): move the documented CNA snapshot to 3b43bd86 | every site page, generated file, script, record, fact file and presentation baseline of this update (759 files) |
| the next commit, audit(PIN-3b43bd86) | this ledger, `plan.md` and `audit/maintenance-handoff.md` |

`TMPDIR=~/.cache/libcna-com/tmp ./scripts/regenerate_site.sh --check` on `9a6867e`: "regeneration leaves the committed tree
unchanged" (exit 0; the throwaway copy was removed by the script). `./scripts/validate_all.sh` immediately before the commit:
"overall: PASS WITH OPTIONAL EXTERNAL CHECKS SKIPPED".

Nothing was pushed or deployed, no branch was reset, and the CNA repository and the fork and asset clones were only read.
