# Phase 4 delta ledger — libcna.com → CNA `b0e97bb1`

Record of the pin move from CNA `009d40f5` to `b0e97bb1` (update and expansion, not a redesign).
Nothing in this file is served as site content (`_config.yml` excludes `audit/`); the site's pages never link to it.
The per-area fact sheets this ledger cites are in `audit/data/facts/b0e97bb1/` (R1–R10 and the editorial guide used
for this update).

## 1. Source boundary

| Item | Value |
|---|---|
| libcna.com HEAD at session start | `df85d05` "docs(GS-AUDIT-P4): correct verified GamerServices networking and avatar capability claims", branch `develop` |
| libcna.com working tree at start | clean (no tracked or untracked changes recorded before work began) |
| Old `cnahead` | `009d40f5dd085c4e674d3479675fac84b12b3e0a` (CNA `next`, 2026-09-24) |
| New `cnahead` | `b0e97bb1bb876f9b3edd6f4ff1ef3067908ae8ac` + one newline — "CHANGELOG link refs openeggbert/cna → libcna/cna", 2026-10-04 13:20 +0200, on `next` (and `samples`) |
| Ancestry | `git merge-base --is-ancestor 009d40f5 b0e97bb1` → true |
| Commits traversed `009d40f5..b0e97bb1` | **456** (232 first-parent, 18 merges); 2,402 changed paths |
| Distance from the release | `v0.1.0-alpha.1..b0e97bb1` = 3,333 commits (945 first-parent, 65 merges), 7,436 changed paths; `git describe` = `v0.1.0-alpha.1-3333-gb0e97bb1b` |
| Product version string | still `0.1.0-alpha.1` (`CMakeLists.txt`); no tag after `v0.1.0-alpha.1` |
| How CNA was read | Git objects only (`git show`, `git ls-tree`, `git grep`, `git diff`, `git cat-file`); nothing in CNA or any sibling repository was checked out, built or modified |
| Pinned external revisions | `data/current-facts.json` → `external_pinned` (cna-samples `5db32e6`, samples.libcna.com `b3939de`, cna-cs `860f92c`, cna-cs-samples `1e6d763`, cna-cs-template `008c3b1`, cna-multi-language-3d-demo `16bde3c`, cna-lab `d292e40b` and the final binding revisions) |

## 2. Before → after

| Fact | `009d40f5` | `b0e97bb1` | Method |
|---|---|---|---|
| Renderer identities | 25 | **18** | `cmake/RendererIdentities.cmake`, cross-checked with the C++ enum, registry map and C ABI table |
| Implementation families | 21 | **14** | directories under `modules/renderers` that own a `src/` (canvas, directx9, directx11, directx12, easygl, fna3d, headless, metal, sdl-gpu, sdl-renderer, software, stub, vulkan, webgpu) |
| Deliberately 2D-only identities | 7 | **2** (SDL_RENDERER, CANVAS) | ThreeD capability in code |
| Compiled-effect identities | 14 (10 families, 9 options) | **13** (9 families, 8 options) | `*_COMPILED_EFFECTS` options + FNA3D |
| Platform implementations | 7 | **6** (SDL3, X11, WAYLAND, WIN32, HEADLESS, TERMINAL) | `cmake/PlatformSelection.cmake` |
| Audio implementations | 4 | **3** (SDL3, NULL, ALSA) | `cmake/AudioPlatformSelection.cmake` |
| C ABI | 0.29.0 (`0x00001D00`), 61 headers, 4,055 routes | **0.44.0** (`0x00002C00`), 60 headers, 3,210 routes, 197 struct layouts | `modules/c-api/include/CNA/C/abi.h`; `tools/c-api/abi_baseline.json` |
| C ABI release gate | Not ready, 468 unmapped | Not ready, **656** unmapped (coverage 469 headers / 8,142 symbols / 7,030 implemented / 15 partial / 656 planned / 441 n/a) | committed `RELEASE_GATE.md`, `COVERAGE.md` (not re-run) |
| `CNA_GRAPHICS_RENDERER_MAXIMUM` | 46 | **43** | `abi.h` |
| C++ test source files | 904 (871 with macros) | **852** (821 with macros) | `git ls-tree` / `git grep -c` (same method reproduces the old values exactly) |
| Static GoogleTest-family definitions | 12,610 | **12,021** (TEST 9,002, TEST_F 2,900, TEST_P 119; 85 INSTANTIATE) | `git grep -cE '^\s*(TEST|TEST_F|TEST_P|TYPED_TEST|TYPED_TEST_P)\s*\('` |
| Standalone pixel programs | 879 | **779** | `examples/**/*_test.cpp` |
| CI workflow files | 20 (28 jobs; 17 automatic / 24 jobs by the site's method) | **18** (26 jobs; 16 automatic / 23 jobs) | `.github/workflows` (`gdi-windows-ci.yml` and `htmldom-ci.yml` deleted) |
| XNA 4.0 runtime representation | 331/331 types, 3,627/3,627 members | unchanged in the committed report (not re-run); representation, not behavioural parity | `docs/xna-4-runtime-member-coverage.md` |
| XNA C++ sample completion (cna-samples) | 87 of 153 (`4da98a0`) | **91** complete (`5db32e6`): 153 is the SAMPLE-001…153 audit universe; 8 relevant targets remain; 54 entries are not port targets; Racing Game Kit is a separate plan, not counted in the 91 | cna-samples `plan.md` |
| samples.libcna.com | 40 published builds | **90** playable C++ WebAssembly builds (`b3939de`; one, PerformanceUtility, marked partial) | gallery manifest |
| Language bindings | maintained C, C#, Java, TypeScript; archived 5 | maintained **C and C#**; archived **8** (Common Lisp, Go, Java, Python, Ruby, Rust, Swift, TypeScript) in `libcna/cna-lab` | cna-lab `d292e40b`, binding final revisions |

## 3. Owner decisions applied

1. **The seven removed renderers leave no public trace.** DIRECT2D, FREEDIRECT, PORTABLEGL, GDI, HTML_DOM, SVG_DOM and
   OPENGL4 are not mentioned anywhere in public content, neither as current features nor as history; the site presents
   CNA as having the 18 identities and 14 families it has. The removal trail stays only in `audit/` (this file, the fact
   sheets, the Known Issues retirement records). `scripts/check_retired_renderers.py` enforces it (section 9).
2. **Racing Game is not hosted.** The completed C++ port is described with its existing screenshot and video, worded
   "not hosted because its original content is not treated as redistributable by the CNA sample gallery"; no Racing
   asset, binary or bundle is published.

## 4. Removed public renderer pages and content

Deleted pages (inbound links repointed in 124 files, duplicate hub cards removed):

| Page | Inbound links now go to |
|---|---|
| `deep-dives/renderers/windows-2d-renderers.html` | `deep-dives/renderers/direct3d-evidence-and-wine.html` |
| `deep-dives/siblings/freedirect-and-freeapi.html` | `deep-dives/siblings/index.html` |
| `development/internals/graphics/opengl4.html` | `development/internals/graphics/easygl.html` |
| `development/internals/platforms/sdl2.html` | `development/internals/platforms/index.html` |
| `docs/tutorials/130-opengl4-desktop.html` | `docs/tutorials/102-opengl-family.html` |
| `docs/tutorials/153-image-based-lighting.html` | `docs/tutorials/114-pbr-materials.html` (IBL generation left CNA with the engine layer) |
| `docs/tutorials/154-cascaded-shadows.html` | `docs/tutorials/59-shadow-mapping.html` |

Renamed: `deep-dives/renderers/browser-dom-renderers.html` → `canvas-renderer.html` (now the CANVAS page only);
`docs/cnaext-engine.html` → `docs/cnaext-extensions.html`. Removed elsewhere: the seven renderer cards and their rows on
`features.html`, the OPENGL4 section and rows on `docs/rendering-backends.html`, the SDL2 platform/audio columns and rows
(the SDL2 platform and audio implementations were also retired in this range), the FreeDirect roadmap item, the
"free-direct & free-api" and "FreeDirect game consumers" related-project cards, and every renderer-specific sentence in
the user guide, tutorials, deep dives and Development pages. Generators and manifests were updated so the content cannot
return: `dev_manifest.py` (opengl4, sdl2 entries), `generate_dev_reference.py` (OPENGL4 family guide),
`audit/data/deep-pages/WP11.json`/`WP17.json` (windows-2d, freedirect, browser-dom entries), `make_architecture_diagram.py`.
The expansion `WPB6/wpb6-freedirect-translation-unit-surface` (target page deleted) was removed.

## 5. CNAEXT graphics-engine disposition

CNA retired the CNAEXT graphics engine layer (render pipeline, post-process chain, shadow/IBL generation, clustered
lighting, compute/storage resources, `engine_layer.h`; MOD-RETIRE-1 `5572f3ca1`). The site now presents it as
non-existent: `docs/cnaext-engine.html` became `docs/cnaext-extensions.html`, which documents only what survives —
`CRTEffect`, `DepthEffect` (colour-depth/palette reduction), `AsciiPostProcessEffect`, `DebugDraw`,
`ShaderCodeEXT`/`ShaderPackageEXT`, `CNAEXT.hpp` and the C header `graphics_ext.h` (44 routes); `CNA_CNAEXT` still
defaults to OFF. "CNAEXT" as the marker for non-XNA API (`CNA_STRICT_XNA_API`) is kept everywhere it is still true, and the
core `PbrEffect`/`SkinnedPbrEffect` (CNAEXT-annotated, in `modules/graphics`) are documented as surviving receivers; the
application renders shadow maps and environment textures itself.

## 6. CNA.NET additions

New pages: `docs/cna-net.html` (architecture C# game → CNA.XnaCompat → CNA.Framework → CNA.Interop → C ABI → C++;
source compatibility, not binary; status and evidence table; original samples; routes; limits),
`docs/migrating-to-cna-net.html` (XNA/MonoGame/FNA → CNA.NET), `docs/tutorials/170-run-xna-csharp-game-on-cna-net.html`,
`docs/tutorials/171-cna-net-template.html`. Homepage card "C# through CNA.NET", documentation cards, showcase C# samples
card and platform table, tutorial hub section "C# with CNA.NET", sidebar entries, a pointer callout on
`docs/migration-from-monogame.html`, and the C API page's maintained-bindings section. Evidence strengths as recorded
(R4/R5): Linux x86_64, headless Chromium (WebAssembly) and the x86_64 Android emulator; Windows and macOS not run; iOS
planned. 84 original Microsoft sample executables run from byte-identical upstream C# source (84/84 Linux, 84/84
single-threaded Chromium, 84/84 Android emulator; 26 pixel-equal to their C++ port), recorded in the campaign ledgers,
not CI. CNA.NET is presented as a migration route alongside MonoGame and FNA, with no claims about those projects
beyond their public positioning.

## 7. Sample and gallery additions

Homepage, showcase, demos and videos pages: 91 complete C++ ports (153 = audit universe; the categories of the 54
non-targets named), 90 playable builds at samples.libcna.com ("playable in the browser" only for runtime-qualified
builds), Racing Game Kit as a completed port that is not hosted (screenshot and YouTube video only), and the C# samples
on CNA.NET. Racing is not among cna-samples' 91 ✅ rows; it is worded as a separately planned completed port.

## 8. Gamer Services and tutorial additions

`docs/gamer-services.html` (offline by default, server-backed when configured, trust boundaries, avatars,
qualification) and tutorials 162–168 (setup and local profiles; the Guide; connecting to the CNA Gamer Services server;
friends and presence; online sessions; avatars; operating the server), each separating offline behaviour, server-backed
behaviour, security and qualification. Tutorials 97 (networking) and 123 (achievements) were rewritten for the
server-backed `PlayerMatch`/`Ranked`, relay, invitations, host migration and voice. `docs/xna-compatibility.html`'s
GamerServices section and Net rows were rewritten. Qualification wording: Linux-only (CNA's recorded runs: 649
GamerServices and 524 Net tests), no public service instance, browser builds without service, relay or voice.

## 9. Archived binding policy update

Maintained: C and C# (CNA.NET). Archived (eight, from the cna-lab evidence, not from the request text): Common Lisp, Go,
Java, Python, Ruby, Rust, Swift, TypeScript — kept in `libcna/cna-lab` under `bindings/`; the standalone repositories no
longer exist. Seven were requalified on Linux against C ABI 0.35.0 on 2026-09-30 before archiving; Common Lisp's final
revision targets 0.21–0.23. Kotlin and VB.NET were considered and excluded (no evidence of a binding). `docs/c-api.html`
`#maintained-bindings` and `#archived-bindings`, the homepage callout ("actively maintains C and C# bindings"), the
Development binding pages (now titled "(archived)") and `scripts/check_facts.py`'s binding policy (MAINTAINED_EXTERNAL
`C#|CNA.NET`, archived names and repositories from `current-facts.json`) were updated.

## 10. Known Issues

Through the existing process (`audit/data/bible/issues/patches-adversarial.json`, `known_issues.py merge/build`):
47 retired with evidence (23 obsolete because the code they describe was removed, 24 proven fixed), 11 narrowed,
31 changed, 39 edited, 5 added (CNA-BUG-275 unguarded `setenv` in tests, CNA-BUG-276 `SoundEffect.Play` validation,
CNA-GAP-072 combined Chat send flags, CNA-GAP-073 offline leaderboard Stream columns, CNA-GAP-074 online sessions refuse
guests). Published: 328 entries (205 bugs, 64 functional gaps, 10 platform limitations, 49 verification gaps; 303 open,
25 narrowed). `known_issues.py` gained `retired_added` and `repin` (both documented in the patch file). The page marker
`<!--issue:NEW-AUDIT-25-->` on `deep-dives/services/network-sessions.html` (retired CNA-BUG-268) was replaced by the fix
reference. Executed probes stay attributed to `009d40f5` in the issue text.

## 11. Re-pin method and evidence levels

* **Links.** 5,612 CNA blob/tree links pinned to `009d40f5` were re-pinned; every linked path exists at `b0e97bb1`
  except 110 paths of retired code, which were linked only from the five generated `development/reference/` pages and
  disappeared when those were regenerated. No pinned link carries a line anchor. `check_source_links.py`: ok.
* **Labels.** 1,054 textual mentions (meta lines, "source links pinned to", evidence boxes, "read at …") were moved to
  `b0e97bb1`. Sentences that report something executed or observed at `009d40f5`, and ledger filenames
  (`009d40f5-phase1-delta.md`), were kept. The one executed C-API gate verdict now names the previous snapshot.
* **Why "read at b0e97bb1" is justified.** (a) The 456-commit delta was studied by area (R1–R10) and every affected
  page in the user guide, tutorials, deep dives and Development section was revised from those reports; (b) for every
  page, the code identifiers and repository paths it cites were checked mechanically against both trees (`git cat-file`
  over all blobs): only identifiers that existed at `009d40f5` and are absent at `b0e97bb1` can make a pinned claim
  stale, and every such hit was resolved or confirmed as a false positive (XNA property names, sibling-library tokens);
  (c) pages whose cited files did not change carry over exactly.
* **Not re-read.** sharp-runtime (CNA does not pin it): its pages still describe `next @ 41b918c9` and now say it was
  not re-read for this move. External projects (MonoGame, FNA) were not re-examined.

## 12. Evidence conflicts resolved (Git evidence over the request, except the two owner decisions)

* Racing Game Kit is not one of cna-samples' 91 ✅ rows (separate `plan_racing.md`); the site says 91 complete plus
  Racing ported separately.
* C# sample executables: 84/84 (CAMPAIGN.md) rather than an unsourced 82/84.
* The archived bindings are the eight above (Kotlin and VB.NET excluded for lack of evidence).
* Automatic workflow counts use the site's existing method (16 files / 23 jobs).
* Direct3D 11/12 compute, indirect draws and GPU timers are verified in source but are renderer-internal (no public API).

## 13. CNA defects observed (reported, not fixed — CNA was not modified)

Recorded as new Known Issues where they affect users (section 10). Also noted, internal only: unguarded `setenv`/`unsetenv`
calls in tests (counted in CNA-BUG-275) and `scripts/check_no_posix_setenv.py` registered nowhere; `CHANGELOG.md` lacks
entries for ABI 0.30, 0.32 and 0.34–0.44; `CNA_GAMER_SERVICES_SERVER_ROOT` defaults two directories up; README still
says real-Windows hardware verification is open while `plans/plan_windows11_directx.md` records a 2026-09-25 baseline;
`CMakePresets.json`'s `cnaext` preset display name still says "engine layer"; `demo_avatar` probably shows the avatar's
back; by source reading, GamerServices local profiles do not persist in a browser (outside the IDBFS mounts).

## 14. Presentation-loss audit

Baseline `audit/data/phase4-baseline-inventory.json`, taken from `df85d05` (838 pages) before any edit; compared by
`compare_presentation.py --phase4` with the strict 10 % shrink guard. The earlier baselines (Phase 1 `be35902`,
Phase 2 `94d758a`, Phase 3 `2c4970c`) were compared too. A CNA source link re-pinned from `009d40f5` to the current
`cnahead` counts as the same link (`PIN_MAP` in the comparator); everything else that changed is dispositioned item by item.

| Comparison | Unexplained | Dispositioned (new in Phase 4) |
|---|---|---|
| Phase 1 | 0 | 184 (57) |
| Phase 2 | 0 | 151 (104) |
| Phase 3 | 0 | 464 (375) |
| Phase 4 | 0 | 725 (682) |

Phase 4 dispositions by reason: CNA files linked from pages that no longer exist at `b0e97bb1` (129); generated reference
pages regenerated (137); generated Known Issues pages rebuilt or retired (91 + 47); retired-renderer, SDL2, engine-layer or
web-save-gap content (67 + 2 links); deleted or renamed pages (9); external links re-pinned or archived (77); source links
dropped with rewritten sentences (21); and 139 items reviewed by hand. The reviewed items are the removed free-direct
call-site audits on `porting-case-studies.html`, the rewritten tutorials 97, 105 and 123, the removed engine-layer
sections of tutorials 37, 59, 64–67, 115 and 116, the retitled EasyGL and avatars deep dives, callouts superseded by CNA
fixes (gamer copy semantics, the storage-root latch, web saves, content-root resolution, exact ABI admission), and
generated backlink blocks that lost retired entries. No item was a loss of current content.

Owner-designated content (`validate_presentation.py`): `cnahead` constant; homepage Quick Stats present (12 stats,
recomputed); the showcase's real-XNA verification section (876 words, 8 cards, 4 images); the Speedy Blupi section on
`demos.html` and its primary "Play in Browser" CTA to speedyblupi.com; all 22 baseline primary CTAs preserved. Removed
on purpose: the homepage cards "free-direct & free-api" and "FreeDirect game consumers" (their only link to CNA was the
FREEDIRECT renderer; owner decision).

## 15. Stale-pattern classification (request §21)

A census over every tracked and new file; "public" means served HTML/SVG, "data" `data/*.json`.

| Pattern | Public | Classification of the public occurrences | Elsewhere |
|---|---|---|---|
| `25 renderer` | 4 | VALID SOURCE EXAMPLE — CNA-BUG-055 quotes CNA's own stale `LIMITATIONS.md`/`COMPATIBILITY.md` text, which is the defect | audit 166, `check_facts.py` needle 1 |
| `21 implementation` | 0 | — | audit 72, needle 1 |
| `7 platform` | 0 | — | audit 11, needle 1 |
| `4 audio` | 0 | — | audit 10 |
| `12,610` | 0 (data 1) | HISTORICAL AUDIT — the method note in `current-facts.json` that the same count reproduces the previous value | audit 74, needle 1 |
| `2,877` | 0 | — | audit 87, needle 1 |
| `87 / 153` | 0 | — | audit 25, needles 2 |
| `0.29.0` | 7 | VALID SOURCE EXAMPLE — ABI history (`docs/c-api.html` ×2, `update-the-c-api.html` ×2, `takeover/uncertainty.html`, the archived Python binding tour) and Tutorial 129's note that its program was first checked against the 0.29.0 headers | audit 388, needles 2 |
| `009d40f5` | 27 (data 5) | HISTORICAL AUDIT — Known Issues text attributing executed probes to the previous snapshot (20), the C-API gate verdict executed there (1), the sharp-runtime revision note (2), the ledger filename and previous pin on the maintenance pages (4); data: `previous_snapshot` and method notes | audit ~19,150, scripts 22 (constants, `PIN_MAP`) |
| `DIRECT2D`, `FREEDIRECT`, `PORTABLEGL`, `HTML_DOM`, `SVG_DOM`, `OPENGL4`, `GDI` (all spellings) | 0 | — | audit (history), scripts (checker patterns, superseded-tag filter) |

**STALE / MUST FIX: 0.** `check_retired_renderers.py` reports 0 references in public content (33 retired spellings
derived from the CNA registries); `check_facts.py` reports 0 problems.

## 16. Validation results

| Command | Result |
|---|---|
| `./scripts/regenerate_site.sh` | exit 0; a second run leaves the tree unchanged (idempotent) |
| `./scripts/validate_all.sh` | **overall: PASS** (`validate_site`, `validate_presentation` 6/6, `compare_presentation` phases 1–4 with 0 unexplained, `check_facts` 0, `check_source_links` ok, `site_dev check`, `check_retired_renderers` 0, `site_deep check`, `check_deep_page --all`, `apply_expansions check`, `backlinks check`, `known_issues validate` 328, `issue_refs check`, `adversarial_audit all` (anchors 0 errors, lost concepts 0), `apply_page_fixes check` 0, `git diff --check`) |
| `git diff --check` | clean |
| Engine-layer leak grep (public HTML) | only CNA's own doc filename `cnaext-engine-layer.md` in source links and the archived Python binding's docstring term |
| Browser QA (`browser_qa.py sweep`, Chrome headless, 1400/390 px × dark/light) | homepage, renderers, platforms, C API, CNA.NET, migration guide, tutorials hub, Gamer Services, Tutorial 167, showcase, selection axes, Known Issues index, demos: no horizontal overflow, no console errors, no failed images, global header intact; the only flags are the known inherited low-contrast elements (muted pager text, prism green, hub level badge, "No APK published yet" badge) |

Tooling changed to match the new target: `check_retired_renderers.py` (Git-object derivation, all spellings, always run),
`check_facts.py` (binding policy, new stats, stale needles, archived binding tours), `compare_presentation.py` (`--phase4`,
pin normalisation), `build_site_indexes.py` (superseded-tag filter, new tags), `apply_page_fixes.py` (`superseded_by`),
`update_tutorial_hub.py` (pager re-chaining, new sections), `known_issues.py` (`retired_added`, `repin`), `site_nav.py`,
`site_dev.py`, `dev_manifest.py`, `generate_dev_reference.py`, `make_architecture_diagram.py`, `validate_presentation.py`,
`validate_all.sh`. The Bible absorption records were reconciled: 164 concepts whose subject CNA removed are now
`REMOVED FUNCTIONALITY` (old tokens and destinations kept under `*_009d40f5`), 2 point at retired Known Issues (`OBSOLETE`),
269 dropped stale tokens (kept under `tokens_superseded_b0e97bb1`), 49 had destinations repointed; 79 applied page fixes
are marked `superseded_by` this ledger.

## 17. Known unresolved documentation questions

1. sharp-runtime was not re-read: its pages describe `next @ 41b918c9` and now say so.
2. GamerServices local profiles in a browser: by source reading they live outside the IDBFS mounts and do not persist; not run.
3. Tutorial 129's C program was checked against the 0.29.0 headers; every identifier is still declared at `b0e97bb1`, but it was not recompiled.
4. The HLSL variants of the CNAEXT CRT and colour-depth shaders (DIRECTX11/12) have no recorded run.
5. CNA.NET, sample and Android/browser results are CNA's and the sibling projects' recorded runs (Xvfb, headless Chromium, the x86_64 emulator), not CI and not re-run here.
6. The five new Known Issues have had no adversarial review; 242 entries judged still valid rely on the R9 reading.
7. Low-contrast inherited elements remain known presentation debt (unchanged).
8. Whether libcna.com should disclose AI assistance remains an owner decision (unchanged; no wording added).
9. CNA's own documents still carry stale statements (README's open real-Windows verification, the `cnaext` preset label "engine layer", `CHANGELOG.md` without ABI 0.30–0.44 entries); the site reports CNA as it is and leaves CNA unmodified.

## 18. Commits (local, on `develop`; nothing pushed)

Two local commits on `develop`, nothing pushed: the atomic pin move (prose, generated pages, indexes, tooling, Known
Issues, dispositions and fact sheets together, as `development/maintenance.html` requires) and this audit record with
`plan.md` and the maintenance handoff. Hashes: `git log --oneline df85d05..develop`.
