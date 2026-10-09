# Phase 5 delta ledger — libcna.com → CNA `c1c316b9`

Record of the pin move from CNA `b0e97bb1` to `c1c316b9` (update and cleanup, not a redesign).
Nothing in this file is served as site content (`_config.yml` excludes `audit/`); the site's pages never link to it.
This file and the fact sheets in `audit/data/facts/c1c316b9/` name the retired renderer identities and platform
backends; public pages must not (sections 4 and 5).

## 1. Source boundary

| Item | Value |
|---|---|
| libcna.com HEAD at session start | `7f0dbaa` "audit(PIN-b0e97bb1): record the Phase 4 pin move ledger, plan and handoff notes", branch `develop`; the Phase 5 presentation baseline was inventoried from that commit (`audit/data/phase5-baseline-inventory.json`, 800 pages) |
| Old `cnahead` | `b0e97bb1bb876f9b3edd6f4ff1ef3067908ae8ac` (CNA `next`, 2026-10-04) |
| New `cnahead` | `c1c316b9c7a846ce8002809c151fcd1af14942c9` + one newline — 2026-10-09 17:22 +0200, tip of `apple/m4-stabilization` when fetched (`git fetch origin apple/m4-stabilization`; the remote branch has since moved on to `63ef2e62`) |
| Ancestry | `b0e97bb1` is an ancestor of `c1c316b9`; `git rev-list --count b0e97bb1..c1c316b9` = **354** (all first-parent); 1,227 changed paths (R5) |
| Distance from the release | `v0.1.0-alpha.1..c1c316b9` = **3,687** commits (1,299 first-parent, 65 merges), 7,463 changed paths; `git describe` = `v0.1.0-alpha.1-3687-gc1c316b9c` |
| Product version string | still `0.1.0-alpha.1`; no tag after `v0.1.0-alpha.1`; `CHANGELOG.md` has only `[Unreleased]` above it |
| How CNA was read | Git objects of the local clone and the tree extracted by `scripts/extract_cna_trees.sh` (stamp = `c1c316b9`); nothing in CNA, cna-gamer-services-server or any sibling repository was modified, built or run |
| Gamer Services server | two archives without `.git` (`…-next.zip` = local clone `4ab12fd`; `…-apple-m4-stabilization.zip` = `4ab12fd` plus the four macOS portability files of AM4-071/AM4-178). No SHA is claimed for the second archive (R4 §1) |
| Sibling SHAs of the Apple campaign | quoted from CNA's `plans/plan_apple_m4.md` at `c1c316b9` and marked as such; most are not present in the local clones (R2 §5, R3 §3.2) |
| Pinned external revisions | `data/current-facts.json` → `external_pinned` (cna-samples `5db32e6` — the local `02511f3` changes no count; samples.libcna.com `b3939de`; cna-dotnet `860f92c` as the last locally verified pin with the 0.46.0 admission `8219a6c` quoted from the plan; cna-dotnet-samples `1e6d763`; cna-dotnet-template `008c3b1`) |

## 2. Before → after

Recomputed at `c1c316b9` with the Phase 4 methods (each reproduces the `b0e97bb1` value exactly); details and
commands in `audit/data/facts/c1c316b9/R1-renderers-platforms-numbers.md` §1.

| Fact | `b0e97bb1` | `c1c316b9` |
|---|---|---|
| Commits since alpha.1 (first-parent / merges) | 3,333 (945 / 65) | **3,687 (1,299 / 65)** |
| Renderer identities / families | 18 / 14 | **14 / 12** |
| Retired identities (derived) | 33 | **37** |
| Deliberately 2D-only identities | 2 | **1** (`SDL_RENDERER`) |
| Compiled-effect identities | 13 in 9 families | **11 in 9 families** (METAL gained an opt-in route) |
| Platform implementations | 6 | **3** (`SDL3`, `HEADLESS`, `TERMINAL`) |
| Audio implementations | 3 | 3 (`SDL3`, `NULL`, `ALSA`) |
| C ABI | 0.44.0 | **0.46.0** (3,210 exports and 197 structs unchanged; 1,463 integer constants) |
| C ABI release gate | Not ready, 656 unmapped (7,030 / 15 / 656 / 441) | Not ready, **631** unmapped (7,053 / 15 / 631 / 443) |
| C++ test sources / files with macros / definitions | 852 / 821 / 12,021 | **813 / 781 / 11,380** |
| Standalone pixel programs | 779 | **781** |
| CI workflow files / jobs (automatic files / jobs) | 18 / 26 (16 / 23) | **18 / 24 (16 / 21)** |
| iOS renderer allow-list | `SDL_RENDERER` | **`SDL_RENDERER`, `METAL`** |
| Known Issues published | 328 | **310** (22 retired, 4 new) |
| Homepage stats | 18 identities, 14 families, 6 platforms, 12,021 definitions, 3,333 commits | **14, 12, 3, 11,380, 3,687**, plus "7 renderer test trees passing on a physical Mac mini M4" |

## 3. Decisions applied

1. **Retired renderers leave no public trace.** OPENGLES2, WEBGL1, DIRECTX12 and CANVAS (RRC-018, `1cac65958`) join the
   earlier retirements: not on any public page, in metadata, search data, the sitemap or the architecture diagram,
   not even as a "removed" notice. The C ABI 0.45.0 step is described publicly only as "retired four renderer identity
   constants; their values stay reserved".
2. **The retired platform backends leave no public trace, but Windows, X11 and Wayland stay.** PLAT-142
   (`39e84add7`) removed `CNA_PLATFORM=WIN32/X11/WAYLAND`. The site now says SDL3 is the one windowing platform and
   reaches Windows, X11 and Wayland through SDL's video drivers; native handles (`HWND`, `Display*` + XID,
   `wl_display*` + `wl_surface*`) remain available through `GameWindow::GetNativeWindowHandleEXT()`; Xvfb and
   headless Weston are CI test servers; `CNA_ENABLE_SDL=OFF` is the windowless configuration. The removal is not
   narrated.
3. **Evidence boundaries are kept apart.** Physical Mac mini M4 runs (console locked: presentation not observed),
   iOS Simulator runs, hosted CI, build-only artefacts and CNA's own documents are never merged into one claim; no
   physical iPhone, Intel Mac, soak run or post-campaign green Apple/Metal CI run is claimed.
4. **No Xbox LIVE claim** for the Gamer Services server; its limits (single process and machine, SQLite, loopback
   qualification) stay next to every capability statement.

## 4. Renderer cleanup

* Deleted page: `deep-dives/renderers/canvas-renderer.html` (inbound links → `deep-dives/platforms/web-build-and-main-loop.html`).
* Rewritten: the renderer reference, features matrix, architecture diagram (`img/architecture-diagram.svg`,
  `mermaid-diagram.png`, regenerated by `scripts/make_architecture_diagram.py`), FAQ, roadmaps, verification,
  building, releases, every tutorial and deep dive that counted identities, listed EasyGL's profiles, the browser
  renderers or the Windows Direct3D set (EasyGL is now `OPENGLES3`, `OPENGL33`, `WEBGL2`; the browser has `WEBGL2`
  and `WEBGPU`; Windows Direct3D is `DIRECTX9` and `DIRECTX11`).
* Guard: `scripts/check_retired_renderers.py` keeps deriving the set from CNA and now (a) treats `CANVAS` as a weak
  word (the HTML canvas element stays legal) and (b) flags the prose aliases of a retired identity when presented as
  a CNA renderer ("Canvas renderer", "Direct3D 12 backend", "Direct3D 9/11/12", "Direct3D 11 and 12", "WebGL 1" or
  "OpenGL ES 2" listed with current renderers). SDL_GPU's Direct3D 12 driver, meta-gl's GLES 2.0 entry points and
  WebGL 1/2 context flags are other projects' facts and stay legal.
* `scripts/build_site_indexes.py` drops retired-renderer and retired-backend tags from the search index wherever they
  come from (`RETIRED_TAG`).

## 5. Platform cleanup

* Deleted pages: `development/internals/platforms/{x11,wayland,win32}.html` (inbound links →
  `development/internals/platforms/sdl3.html`; `scripts/dev_manifest.py` entries removed).
* Renamed in place (same URL): `docs/native-platforms.html` → "Windows, X11 and Wayland" (SDL's video drivers,
  choosing a driver, native handles, renderers per window system, the windowless SDL-free build, CI evidence,
  limits); sidebar label in `scripts/site_nav.py`. Tutorials 135/136 → "Running on X11/Wayland through SDL3"; 137
  (ALSA) and 138 (SDL-free) reframed; hub section "Window Systems and Builds" (`scripts/update_tutorial_hub.py`).
* Guard: new `scripts/check_retired_platforms.py`, wired into `validate_all.sh`. It derives the retired set from
  `_cna_platforms_retired` in `cmake/PlatformSelection.cmake` at `cnahead` and flags `CNA_PLATFORM=X11` (and every
  spelling of a selection), `CNA_PLATFORM_X11`, "native/direct/SDL-free X11/Wayland/Win32" unless followed by
  window/handle/display/surface/session/video/driver/server/…, "X11 platform/backend", the backend classes and
  their source directories, and links to the deleted internals pages — while SDL's `x11` driver, `NativeWindowSystem::X11`,
  `TryGetX11`, Xvfb and Weston stay legal (`sep` requires a separator, so `DIRECTX11` is not "direct X11").

## 6. Apple, Mac mini M4 and iOS

Facts in `audit/data/facts/c1c316b9/R2-apple-m4.md` and `worklist-apple.md`. Public statements now carry:
hardware (Mac mini M4, arm64, 16 GB, macOS 27.0.1, Xcode 27, Apple clang 21); the seven full renderer trees
(METAL 11,015 passed / 114 skipped, SOFTWARE 11,084 / 133, OPENGL33 with compiled effects 11,916 / 128, SDL_GPU
10,962 / 295, WEBGPU 10,968 / 279, FNA3D 10,875 / 433, SDL_RENDERER 10,940 / 966); the 261 `-L Metal` tests under
the validation layers in Debug and Release; cna-samples 91/91 and cna-examples 248/248 on Metal; the AM4-159 verdict
(supported, not primary-production) with its limits; iOS (`SDL_RENDERER` and `METAL`, device build final-linked and
never run, Simulator pixel probe 29/31 and 8/8 after AM4-120, `CNA_ENABLE_NET=OFF`, no C API for iOS); the C API on
macOS (R3 §2); CNA.NET on osx-arm64 as local evidence (R3 §3); sharp-runtime's macOS run 18,084 / 18,059 / 0 / 25;
apple-ci and metal-macos-ci on `macos-26` without a recorded post-campaign green run; every workflow now choosing the
matching sharp-runtime branch (AM4-234), which retired the stale-pin caveat.

## 7. C API 0.46.0 and CNA.NET

R3. ABI 0.44.0 → 0.45.0 (RRC-018, four renderer constants retired, values reserved) → 0.46.0 (AM4-037,
`CNA_NATIVE_WINDOW_SYSTEM_UIKIT` = 9). Gate figures 631 / 7,053 / 15 / 443 of 8,142. The C# repositories were renamed
`cna-cs*` → `cna-dotnet*` (rename commit `8947b91`); every public link and name was changed; CNA.NET admits exactly
0.46.0 (cna-dotnet `8219a6c`, AM4-217; 0.45.0 was never admitted).

## 8. Gamer Services server

R4 and `worklist-gamer-services.md`. Public pages describe the full contract (37 advertised capabilities, 59 public
operations, schema 23) and the operator infrastructure, the Linux handoff qualification of 2026-10-07 (46 configured,
29 passed, 17 CNA-harness tests skipped, 0 failed; ASan/UBSan 19/19; TSan 3/3; conformance 20 + 1 cases covering 59
operations), the macOS result (37 passed, 9 skipped, 0 failed with Homebrew curl 8.22; the SDK's libcurl 8.7.1 has no
WebSockets, so the relay refuses by name and events fall back to polling; AM4-071 nuance), the fact that the
2026-10-07 Linux run exercised no CNA processes (the last CNA-harness Linux run: 2026-10-02, 40 tests, 33 passed, 7
skipped), and the limits (single process and machine, SQLite, loopback qualification, no public instance, not
Xbox LIVE).

## 9. Known Issues

R5. 328 → **310** published: 22 retired (11 OBSOLETE — mostly the retired Win32/X11/Wayland code —, 10 PROVEN FIXED,
1 INSUFFICIENT EVIDENCE), 4 new (CNA-PLAT-016/017/018, CNA-BUG-277), 13 newly narrowed, 59 edited, 234 carried.
`scripts/known_issues.py` gained the repin-step list and `retired_reclassified`. Two KI texts that the strengthened
renderer guard flagged were corrected in `patches-adversarial.json` (CNA-BUG-094 now names "SDL_gpu's Direct3D 12
driver"; CNA-GAP-064 named a Direct3D 12 renderer that no longer exists — at `c1c316b9` DIRECTX9, DIRECTX11 and
VULKAN raise `Lost`), and CNA-VGAP-008 no longer says "one iOS simulator frame": `apple-ci.yml` at `c1c316b9` also
runs a METAL pixel probe in the Simulator that checks read-back pixels.

## 10. Tooling changed

| File | Change |
|---|---|
| `scripts/site_nav.py` | footer and doc-meta snapshot text derived from `cnahead` + `data/current-facts.json` (`_snapshot_constants()`), so a pin move no longer needs a hand edit; sidebar label |
| `scripts/check_facts.py` | `b0e97bb1` stale needles (18 identities, 14 families, 12,021, 852, 3,333 commits, 6 platforms, ABI 0.44.0, 26 jobs); `cna_dotnet_samples` key |
| `scripts/check_retired_renderers.py` | `CANVAS` weak; prose aliases (section 4) |
| `scripts/check_retired_platforms.py` | new (section 5) |
| `scripts/validate_presentation.py` | `CNA_TARGET` = `c1c316b9` |
| `scripts/compare_presentation.py` | `--phase5` (baseline `7f0dbaa`); `b0e97bb1` source links re-pinned like `009d40f5` ones |
| `scripts/build_site_indexes.py` | `UPDATED` 2026-10-09; `RETIRED_TAG` (retired renderer and backend tags dropped wherever they come from); `RENAMED_TAG` (`cna-cs*` → `cna-dotnet*` for tags carried over from the previous index); renderer and window-system tags |
| `scripts/make_architecture_diagram.py` | 14/12, three platforms, ABI 0.46.0, snapshot `c1c316b9` |
| `scripts/apply_expansions.py` | `check` now fails on drift between an expansion source and its page region (re-applying a stale source would have put retired content back); new `fold` writes edited regions back into their sources, turning pinned CNA source links and relative site links back into `{{src:}}` / `{{tree:}}` / `{{page:}}` tokens and verifying the round trip |
| `scripts/known_issues.py` | repin-step list, `retired_reclassified`, `TODAY` |
| `scripts/validate_all.sh` | runs `check_retired_platforms.py` and `compare_presentation.py --phase5` |

## 11. Evidence conflicts and how they were resolved

* The request named `c1c316b9` as the target; the commit was not in the local clone until `git fetch origin
  apple/m4-stabilization`. It is the tip of `apple/m4-stabilization`, not of `next`; every clone instruction on the
  site now uses that branch for CNA, sharp-runtime and meta-gl (easy-gl: `develop`).
* `docs/releases.html` claimed a 2026-10-04 commit date and 945 first-parent commits for the snapshot (left over
  from `b0e97bb1`); recomputed.
* CNA.NET: the site's "pairs with exactly 0.44.0" was correct for the locally verified `860f92c` but superseded by
  AM4-217; the site states 0.46.0 and records where that comes from (`current-facts.json`).
* Contribute page: cube faces in MRT sets — `DIRECTX9` and `SDL_GPU` still refuse (`not implemented by this CNA
  renderer`), Metal attaches them (`MetalRenderer.mm` `currentMRT[0].cube`).
* Numbers that the agents' rewrites had not reached were recomputed with the Phase 4 methods, each method first
  reproducing its `b0e97bb1` value: the test-population table (`deep-dives/verification/test-populations-and-gates.html`:
  813 (812 by the CnaTests globs), 11,380 = 8,785 + 2,476 + 119, 1,375 (1,391) renderer-registration call sites, 186
  `add_test`, now **4** `gtest_discover_tests` sites because the networking suites are discovered separately under one
  `RESOURCE_LOCK`, 878 / 781 example files), the per-owner test-source table (graphics 168, platform 37, renderers 62),
  the authorship figures (9,709 reachable commits, one author, no `Co-authored-by`, 3,205 of the 3,687 commits since
  the tag with a signature header, 212 of them SSH), the C ABI gate figures on the C API handbook page and 24 CI jobs on
  the Development testing pages.
* Pages whose source links still pointed at `b0e97bb1` (Gamer Services, services deep dives and their internals) were
  re-pinned only after checking every linked file: all exist at `c1c316b9`; the changed ones changed by AM4 fixes,
  comment-only edits and the two retirements, none of which contradicts the pages. Their evidence callouts keep
  "checked by reading at `b0e97bb1`", which is what happened.
* `development/debugging.html` quoted CNA's refusal message for a retired `CNA_PLATFORM` value with its removal date;
  the row now explains the current message ("configure with -DCNA_PLATFORM=SDL3") without naming retired values.

## 12. Process note: subagents

The owner allowed at most three subagents, later lowered to two with the instruction to let the running ones finish.
Three were used (Gamer Services, Known Issues, Apple/C API/CNA.NET). Each of them additionally spawned forks of its
own, which exceeded the owner's cap; they were told to stop, and no further agent was started after the cap was
lowered. The Known Issues agent's final `known_issues.py merge/build` was blocked by the permission classifier; the
coordinator reviewed its proposed four-line `patches-adversarial.json` change and ran the Known Issues pipeline as part
of the regeneration this task requires.

## 13. Presentation-loss audit

Baseline `audit/data/phase5-baseline-inventory.json` (800 pages, inventoried from `7f0dbaa` before any edit) compared
with the final tree by `compare_presentation.py --phase5`: **472** differences, every one dispositioned in
`audit/data/phase5-dispositions.json` (one entry per item, exact key):

| Disposition | Items |
|---|---:|
| regenerated (Known Issues pages, generated reference pages, generated issue/deep-link and Known-issues blocks) | 133 |
| removed (retired subject) — RRC-018 renderers or PLAT-142 platform backends | 124 |
| removed (file gone at c1c316b9) — CNA source links whose file no longer exists | 94 |
| re-pinned or archived — `cna-cs*` → `cna-dotnet*` | 38 |
| rewritten (reviewed) | 34 |
| retired with evidence — the 22 retired Known Issues (R5) | 22 |
| not public — audit expansion sources folded back | 17 |
| removed with rewritten text — page shrinks on the Direct3D, gamepad, platform-backend and browser-renderer pages | 10 |

Categories were drafted by rule and every non-mechanical item (headings, cards, tables, CTAs, blocks and page shrinks
on authored pages) was reviewed by hand; the review moved 93 of the 137 items first drafted as "rewritten" or "removed with
rewritten text" into the retired-subject or regenerated categories and found no unintended loss (for example the tutorial 124 renderer table became one paragraph because only one
identity is Emscripten-only now; the Speedy Blupi section and every primary CTA are intact, `validate_presentation.py`
6/6). The earlier phases' baselines see the same changes; the same classification appended 22 / 111 / 220 / 423
entries to `phase1`–`phase4-dispositions.json`, so all five comparisons report 0 unexplained.

Related audit trails brought in line with the rewritten pages (no public effect):

* **Expansion sources:** 23 of the 34 `audit/data/bible/expansions/` regions had been edited in place; they were folded
  back (`apply_expansions.py fold`, source and page tokens reconstructed), and `check` now fails on any future drift.
* **Bible ledger** (`audit/data/bible/records/`): 122 concepts whose destination anchor or tokens disappeared — 81 set
  to REMOVED FUNCTIONALITY (subject retired by RRC-018 or PLAT-142), 41 to SUPERSEDED (destination rewritten; 26 of them
  reviewed by hand because their subject still exists). `adversarial_audit.py anchors` 0 errors, lost concepts 0;
  `counts --write` regenerated the counts block in `audit/phase3-adversarial-audit.md`.
* **Applied page fixes** (`audit/data/adversarial/applied-page-fixes.json`): 30 records whose text was rewritten carry
  `superseded_by` this ledger; for the 15 that are not about retired subjects the overstatement each fix had removed
  was re-checked on the rewritten page and is not reintroduced (for example device loss is now "five families").

## 14. Validation results

| Command | Result |
|---|---|
| `bash scripts/validate_all.sh` | **overall: PASS** |
| `validate_site.py` | 744 pages parsed (strict HTML5), 0 duplicate ids, 742 search entries and 742 sitemap URLs, unique and complete |
| `validate_presentation.py` | 6 ok, 0 failed (`cnahead` == `c1c316b9` + newline, homepage stats, showcase, Speedy Blupi, 22 primary CTAs) |
| `compare_presentation.py` phases 1–5 | 0 unexplained each (206 / 262 / 684 / 1,131 / 472 dispositioned) |
| `check_facts.py` | 0 problems (incl. the new `b0e97bb1` stale needles) |
| `check_source_links.py` | ok (3,285 deep-page and 2,931 other CNA links pinned to `c1c316b9`) |
| `check_retired_renderers.py` | 0 (37 retired identities derived from CNA, prose aliases included) |
| `check_retired_platforms.py` | 0 (WAYLAND, WIN32, X11 derived from CNA) |
| `site_deep.py check`, `check_deep_page.py --all`, `site_dev.py check` | pass (431 deep/Known Issues pages declared and on disk) |
| `apply_expansions.py check` | expansions ok (no drift) |
| `backlinks.py check`, `issue_refs.py check` | 0 pages would change, 0 errors |
| `known_issues.py validate` | 310 entries, 0 errors |
| `adversarial_audit.py all` | anchors 0 errors, issues 0 errors, lost concepts 0, counts current (Bible graph skipped: Bible repository not present) |
| `apply_page_fixes.py check` | 474 recorded (109 superseded), 0 problems |
| `git diff --check` | clean (new untracked files checked separately: no trailing whitespace) |
| `scripts/regenerate_site.sh --check` | after `c522acb`: "regeneration leaves the committed tree unchanged" (worktree under `~/.cache/libcna-com`, not `/tmp`; `CNA_REPO` must be absolute in check mode) |

## 15. Commits (local, on `develop`; nothing pushed)

| Commit | Content |
|---|---|
| `45b9b7a` docs(PIN-c1c316b9) | the site, `cnahead`, `data/`, `scripts/`, regenerated pages, search index and sitemap |
| the following `audit(PIN-c1c316b9)` commit | this ledger, the fact sheets in `audit/data/facts/c1c316b9/`, the Phase 5 baseline and dispositions, the appended Phase 1–4 dispositions, the Bible-ledger, page-fix and expansion reconciliation, `plan.md` and the handoff notes |
