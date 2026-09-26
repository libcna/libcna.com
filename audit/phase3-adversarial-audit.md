# Phase 3 — independent adversarial audit (2026-09-25 / 26)

Reviewer stance: an independent skeptic who tries to *disprove* the Phase-3 result. Phase 3 is not implementation authority; neither is this document. Truth is the CNA TARGET
(`009d40f5dd085c4e674d3479675fac84b12b3e0a`). The historical Phase-3 records (`audit/phase3-completion.md`, `audit/bible-absorption-phase3*.md`) are kept; where this audit corrects a
figure or a statement in them, the correction is appended there as *Post-Phase-3 adversarial audit correction* and the original wording is not erased.

## 1. Source boundary and baseline

| Item | Value |
|---|---|
| `PHASE3_BASE` (clean HEAD when the audit began; branch `docs/unified-v2`) | `33fd57023a16168bc3d354c8907df2db83ca42f6` — “audit: correct the severity summary in the Phase 3 completion record (2 high, 46 medium, 170 low)” |
| CNA TARGET | `009d40f5dd085c4e674d3479675fac84b12b3e0a` |
| `cnahead` | exactly the TARGET SHA + one newline (41 bytes) |
| CNA HEAD (not used) | `5229c992ebc795b63a2c1d6469a6190ada0e5fb9`, **11** commits after TARGET; only an untracked `startup-metrics.log` |
| Bible HEAD | `4df1475c00ec241f126bca20b065eb465917adaa` (`develop`), **86** modified/untracked paths (working tree is the read source, as in Phase 3) |
| Developer HEAD | `9f07046d91ad01e835274b8027f8e30298193d01`, **7** modified/untracked paths (pre-existing) |
| Pinned TARGET snapshot | `/rv/tmp/libcna-v2/cna-target` — re-verified against git: 11,064 extracted files, **0 hash mismatches** with the TARGET blobs |

CNA, Bible and Developer repositories are read-only for this audit; their `git status` digests were recorded at the start and are compared again at the end (§9).

## 2. Method

Two directions, both required:

* **Source → destination.** Independent of the Phase-3 concept ledger: (a) the Bible source graph is re-derived from `latex/book/main.tex`; (b) every Bible paragraph and every technical identifier is
  tested against the *whole published site* (`scripts/adversarial_audit.py recall`); the residuals are reviewed by reading; (c) every ledger destination anchor is re-checked at *anchor-section* level,
  not just page level; (d) every disposition that *drops* knowledge (FIXED BUG, REMOVED FUNCTIONALITY, OBSOLETE, HISTORICAL ONLY, TARGET CONTRADICTED, SUPERSEDED, DUPLICATE) is challenged against TARGET.
* **Destination → TARGET.** Every one of the 350 Known Issues is re-read against TARGET by a reviewer whose brief is to *refute* it (verdicts CONFIRMED / CORRECTED / NARROWED / RECLASSIFIED / DUPLICATE /
  FIXED AT TARGET / NOT A BUG / INSUFFICIENT EVIDENCE); Deep-Dive identifiers are checked for existence at TARGET; TARGET corrections made in Phase 3 are re-derived on a risk-weighted sample.

Subagent discipline: at most five (default three) concurrent leaf reviewers, no nesting, read-only, TARGET tree only.

## 3. Source-graph reconstruction (independent)

`latex/book/main.tex` was re-parsed for every inclusion macro (`\input`, bare `\input`, `\include`, `\subfile`, `\import`, `\InputIfFileExists`, `\lstinputlisting`, `\verbatiminput`, `\includegraphics`,
`\includestandalone`, `\bibliography`), including commented-out inclusions, without using `scripts/bible_inventory.py`.

* Reachable TeX files: **120** = `main.tex` + `common/preamble.tex` + **118** book files. The 118 are *identical* to the 118 units of `audit/data/bible/units.json` (98 text units + 20 figure sources).
* No unresolved inclusion; no commented-out inclusion; 5 `\includegraphics` = the 5 raster assets Phase 3 recorded.
* `main.tex` (part structure) and `common/preamble.tex` (macros; *and* the Bible's own volatile counts `RendererIdentityCount=25`, `RendererFamilyCount=21`, `XnaOracleSceneCount=46`) carry no prose to conserve.
  The counts are examined in §7.
* The other **136** `.tex` files on disk are `build/html-src/**` and `build/figures/**` — gitignored generated snapshots (dated 2026-08-12 / 2026-09-02) of an *older* chapter arrangement
  (e.g. an old `ch24` about retired renderers); they are not canonical and were correctly excluded.
* Auxiliary set: Phase 3 audited 21 aux documents (8 top-level + 13 `audit/*.md`). **Not dispositioned by Phase 3:** `NEXT-ARCHIVE-2026-07-26.md`, `PLAN-ARCHIVE-2026-07-26.md` (dated snapshots, pre-alpha.1
  restructuring) and `tools/*.sh` (`verify-book.sh`, `verify-edition-facts.sh`, …). See §5.4 for their disposition.

## 4. Baseline recomputation (nothing copied from Phase 3)

Recomputed from `data/known-issues.json` and the file system at `PHASE3_BASE`:

* 350 entries = **218 bugs · 62 functional gaps · 15 platform limitations · 55 verification gaps**; 336 open, 14 narrowed; bugs: **2 high · 46 medium · 170 low** (the figure the last Phase-3 commit already corrected);
  confidence: 330 verified-by-reading, 9 reproduced, 9 strong, 2 probable.
* 350 detail pages = 350 JSON entries; 5 hubs; 0 orphan pages; 0 duplicate IDs; `CNA-BUG` ids 1–249 with exactly the 31 non-surviving Bible ids missing (1–62) and 063–249 contiguous.
* `scripts/validate_all.sh` with `PHASE3_FINAL=1` → overall PASS at `PHASE3_BASE`.
* 783 public HTML pages on disk; sitemap 781 and search index 781 = every page except the two intentional utility pages (`404.html`, `search.html`); no duplicates; `audit/`, `scripts/`, `plan.md`, `build-probe/`
  are excluded from publication by `_config.yml`.
* Reachability: every Deep Dive page has ≥ 2 in-body inbound links; no orphan page in `deep-dives/`, `development/`, `docs/`, `known-issues/`; Known Issues is linked from the footer of all 783 pages and in-body from the
  homepage, Documentation hub and Deep Dives hub — global navigation is left unchanged.

### 4.1 Current published quantities (generated; the recomputation above is the state at `PHASE3_BASE`)

<!-- counts:begin -->

Generated by `python3 scripts/adversarial_audit.py counts --write` from `data/known-issues.json` and `audit/data/adversarial/`; `validate_all.sh` fails when it is stale.

| Quantity | Value |
|---|---|
| Published entries | **370** = 232 bugs · 70 functional gaps · 12 platform limitations · 56 verification gaps |
| Bug severity | **2 high · 47 medium · 183 low** |
| Status | 353 open · 17 narrowed |
| Evidence basis | probable 2 · recorded-by-cna 13 · reproduced 17 · strong 13 · verified-by-reading 325 |
| Entries with a test touching the area | 325 of 370 |
| Subsystems | Graphics & renderers 68 · Documentation & release tooling 48 · Testing & evidence 43 · Networking & gamer services 32 · Math & geometry 26 · Build & CI 25 · Core & runtime 22 · Audio & media 20 · Platforms 20 · Content & XNB/CNB/CNJ 16 · Models & glTF 14 · Storage 10 · Input 9 · Diagnostics & Inspector 9 · C API & bindings 8 |
| Audit operations recorded in `dispositions.json` | folded 8 · retired 3 · reclassified 8 · added 31 |
| Independent issue reviews ingested | 344 of the 350 Phase-3 entries re-read individually (CONFIRMED 224, CORRECTED 95, DUPLICATE 2, NARROWED 12, NOT A BUG 3, RECLASSIFIED 8), plus 6 more folded as identical-source duplicates into a re-read survivor (BUG-187, BUG-188, BUG-219, BUG-226, VGAP-043, VGAP-045); entries added by the audit that a separate reviewer then tried to refute: 31 of 31 |
| Extra-deep second look at a stratified sample (source re-derivation and, where feasible, an executed probe) | 34 entries; HOLDS 16, HOLDS WITH NOTES 11, NEEDS CORRECTION 7; a probe was executed for 24 of them |
| Independent dismissal reviews ingested | 121 of 121; ALREADY-PUBLISHED 2, DISMISSAL CONFIRMED 105, NARROW-RESTORE 6, RESTORE-BUG 1, RESTORE-GAP 1, RESTORE-VERIFICATION-GAP 5, UNRESOLVED 1 |
| Independent site-errata verifications ingested | 76 of 76 Phase-3 errata; CORRECT 36, INCOMPLETE 28, NUANCE-LOST 10, OVERSTATED 2 |
| Independent Bible-unit reviews ingested | 98 of 98 canonical text units; PASS 17, PASS WITH FIXES 81; findings 223 (FALSE-DROP 4, LOST 25, OVERSTATED 100, RESTORE-ISSUE 1, SHALLOW 45, WRONG-CORRECTION 47, WRONG-DESTINATION 1) |
| Independent auxiliary-document reviews ingested | 21 of 21 auxiliary documents; PASS 8, PASS WITH FIXES 13; findings 31 (FALSE-DROP 1, LOST 5, OVERSTATED 8, RESTORE-ISSUE 2, SHALLOW 11, WRONG-CORRECTION 3, WRONG-DESTINATION 1) |
| Unit-review evidence (canonical units and auxiliary documents together) | residual paragraphs/identifiers reviewed 894 (lost-useful 24); dropped dispositions reviewed 753 (false drops 5, restore-issue 1); ledger TARGET corrections re-derived 1118 (disagreements 29) |
| Unit-review findings and their outcome | 254 = fixed 250 · owner-decision 1 · restored 3 |

Per-unit review results (dropped dispositions: reviewed / false drops; ledger TARGET corrections: re-derived / agreeing):

| Unit | Status | Large | Findings | Dropped | Corrections |
|---|---|---|---|---:|---:|
| `titlepage` | PASS |  | none | 1 / 0 | 0 / 0 |
| `preface` | PASS |  | none | 4 / 0 | 0 / 0 |
| `reading-paths` | PASS |  | none | 1 / 0 | 0 / 0 |
| `production-method` | PASS WITH FIXES |  | LOST 1 | 4 / 0 | 0 / 0 |
| `ch01-cna-and-xna` | PASS WITH FIXES | yes | OVERSTATED 1, WRONG-DESTINATION 1 | 5 / 0 | 5 / 5 |
| `ch02-ecosystem-vocabulary` | PASS WITH FIXES |  | OVERSTATED 3, SHALLOW 1, WRONG-CORRECTION 1 | 3 / 0 | 6 / 6 |
| `ch03-language-conventions-cnaext` | PASS |  | none | 3 / 0 | 7 / 7 |
| `ch04-configuring-building` | PASS WITH FIXES |  | OVERSTATED 1, SHALLOW 2, WRONG-CORRECTION 1 | 4 / 0 | 22 / 22 |
| `ch05-first-game` | PASS |  | none | 0 / 0 | 4 / 4 |
| `ch06-game-lifecycle` | PASS WITH FIXES | yes | OVERSTATED 5, SHALLOW 1, WRONG-CORRECTION 1 | 9 / 0 | 26 / 25 |
| `ch07-math-conventions` | PASS WITH FIXES |  | FALSE-DROP 1, OVERSTATED 2, WRONG-CORRECTION 1 | 2 / 1 | 11 / 11 |
| `ch08-geometry-color-layout` | PASS WITH FIXES |  | SHALLOW 1 | 3 / 0 | 12 / 12 |
| `ch09-module-monorepo` | PASS WITH FIXES |  | OVERSTATED 1, WRONG-CORRECTION 1 | 2 / 0 | 17 / 16 |
| `ch10-boundaries-enforcement` | PASS WITH FIXES |  | OVERSTATED 1 | 0 / 0 | 13 / 13 |
| `ch11-dependencies-tools` | PASS |  | none | 2 / 0 | 16 / 16 |
| `ch12-graphicsdevice` | PASS WITH FIXES | yes | OVERSTATED 4, SHALLOW 1 | 7 / 0 | 46 / 45 |
| `ch13-spritebatch` | PASS WITH FIXES | yes | LOST 1, OVERSTATED 1, SHALLOW 1, WRONG-CORRECTION 2 | 6 / 0 | 34 / 33 |
| `ch14-textures-rendertargets` | PASS WITH FIXES | yes | LOST 1, OVERSTATED 1, WRONG-CORRECTION 1 | 6 / 0 | 38 / 38 |
| `ch15-stock-effects` | PASS WITH FIXES | yes | OVERSTATED 5, SHALLOW 1 | 13 / 0 | 18 / 18 |
| `ch16-state-objects` | PASS WITH FIXES | yes | OVERSTATED 1, SHALLOW 2, WRONG-CORRECTION 2 | 12 / 0 | 30 / 30 |
| `ch17-shaders-four-answers` | PASS WITH FIXES | yes | LOST 1, OVERSTATED 2, SHALLOW 1 | 0 / 0 | 12 / 12 |
| `ch18-vertex-streams-capabilities` | PASS WITH FIXES |  | OVERSTATED 2, SHALLOW 1 | 1 / 0 | 11 / 11 |
| `ch19-renderer-contract` | PASS WITH FIXES | yes | LOST 2, OVERSTATED 1, SHALLOW 1 | 9 / 0 | 38 / 35 |
| `ch20-selection-identity` | PASS |  | none | 0 / 0 | 2 / 2 |
| `ch21-opengl-fixed-profiles` | PASS |  | none | 0 / 0 | 2 / 2 |
| `ch22-opengl-programmable` | PASS WITH FIXES | yes | LOST 3, OVERSTATED 1, SHALLOW 1 | 5 / 0 | 20 / 19 |
| `ch23-native-modern-gpu` | PASS WITH FIXES | yes | OVERSTATED 1, RESTORE-ISSUE 1 | 11 / 0 | 6 / 5 |
| `legacy-webgpu` | PASS WITH FIXES | yes | LOST 1, OVERSTATED 2, SHALLOW 1 | 14 / 0 | 9 / 8 |
| `legacy-sdlgpu` | PASS WITH FIXES | yes | LOST 1, OVERSTATED 2, WRONG-CORRECTION 2 | 7 / 0 | 8 / 8 |
| `ch24-abstraction-layers-one` | PASS |  | none | 0 / 0 | 0 / 0 |
| `ch25-abstraction-layers-two` | PASS WITH FIXES |  | WRONG-CORRECTION 3 | 1 / 0 | 0 / 0 |
| `ch26-directx-time-machine` | PASS |  | none | 0 / 0 | 1 / 1 |
| `ch27-retro-ladder` | PASS WITH FIXES |  | OVERSTATED 2, SHALLOW 1, WRONG-CORRECTION 1 | 0 / 0 | 0 / 0 |
| `ch29-windows-2d` | PASS |  | none | 0 / 0 | 7 / 7 |
| `ch31-web-dom-renderers` | PASS |  | none | 0 / 0 | 7 / 7 |
| `ch32-diagnostic-renderers` | PASS WITH FIXES |  | WRONG-CORRECTION 1 | 8 / 0 | 8 / 8 |
| `ch28-modern-direct3d` | PASS WITH FIXES | yes | LOST 1, OVERSTATED 4, SHALLOW 1, WRONG-CORRECTION 2 | 17 / 0 | 39 / 37 |
| `ch30-vector-rasterizers` | PASS WITH FIXES | yes | OVERSTATED 1, SHALLOW 1, WRONG-CORRECTION 2 | 7 / 0 | 8 / 7 |
| `ch33-contentmanager-resolution` | PASS |  | none | 0 / 0 | 4 / 4 |
| `ch34-xnb-container` | PASS WITH FIXES |  | FALSE-DROP 1 | 1 / 1 | 2 / 2 |
| `ch35-xnb-type-readers` | PASS WITH FIXES |  | OVERSTATED 1, WRONG-CORRECTION 2 | 0 / 0 | 20 / 20 |
| `ch36-cnj-format` | PASS WITH FIXES |  | LOST 1, SHALLOW 2 | 0 / 0 | 5 / 5 |
| `ch37-content-pipeline-architecture` | PASS WITH FIXES |  | SHALLOW 1 | 0 / 0 | 0 / 0 |
| `ch38-content-pipeline-build` | PASS WITH FIXES |  | LOST 1, OVERSTATED 1 | 0 / 0 | 1 / 1 |
| `ch37-content-robustness` | PASS WITH FIXES |  | WRONG-CORRECTION 1 | 0 / 0 | 6 / 5 |
| `ch38-models-meshes` | PASS WITH FIXES | yes | OVERSTATED 1, SHALLOW 1, WRONG-CORRECTION 5 | 3 / 0 | 27 / 26 |
| `ch39-gltf-import-core` | PASS WITH FIXES |  | OVERSTATED 1, WRONG-CORRECTION 1 | 0 / 0 | 10 / 9 |
| `ch40-gpu-packing` | PASS WITH FIXES |  | OVERSTATED 1, WRONG-CORRECTION 1 | 1 / 0 | 14 / 13 |
| `ch41-skinning-animation` | PASS WITH FIXES |  | SHALLOW 1, WRONG-CORRECTION 1 | 1 / 0 | 6 / 6 |
| `ch42-cnj-model-toolchain` | PASS WITH FIXES |  | OVERSTATED 1 | 0 / 0 | 9 / 9 |
| `ch43-gltf-conformance` | PASS |  | none | 0 / 0 | 6 / 6 |
| `ch44-input-system` | PASS WITH FIXES | yes | LOST 2, OVERSTATED 2, SHALLOW 2, WRONG-CORRECTION 1 | 13 / 0 | 34 / 34 |
| `ch45-audio-system` | PASS WITH FIXES |  | LOST 1, OVERSTATED 1, WRONG-CORRECTION 1 | 1 / 0 | 17 / 17 |
| `ch46-media-system` | PASS WITH FIXES |  | SHALLOW 2 | 3 / 0 | 15 / 15 |
| `ch47-sensors` | PASS WITH FIXES |  | OVERSTATED 1, WRONG-CORRECTION 1 | 1 / 0 | 7 / 7 |
| `ch48-host-devices` | PASS WITH FIXES |  | SHALLOW 1 | 1 / 0 | 12 / 12 |
| `ch49-gamerservices` | PASS WITH FIXES |  | OVERSTATED 2, SHALLOW 1 | 2 / 0 | 4 / 4 |
| `ch50-storage` | PASS WITH FIXES |  | OVERSTATED 1, SHALLOW 1 | 3 / 0 | 1 / 1 |
| `ch51-networking` | PASS WITH FIXES |  | OVERSTATED 3 | 11 / 0 | 8 / 8 |
| `ch52-avatar` | PASS WITH FIXES |  | SHALLOW 1, WRONG-CORRECTION 1 | 2 / 0 | 7 / 6 |
| `ch53-sharp-runtime-overview` | PASS WITH FIXES | yes | WRONG-CORRECTION 1 | 0 / 0 | 17 / 16 |
| `ch54-components-consumption` | PASS |  | none | 0 / 0 | 11 / 11 |
| `ch55-object-model` | PASS WITH FIXES |  | SHALLOW 1 | 0 / 0 | 4 / 4 |
| `ch56-sharp-runtime-namespaces` | PASS WITH FIXES |  | WRONG-CORRECTION 1 | 0 / 0 | 6 / 6 |
| `ch57-parity-philosophy` | PASS WITH FIXES |  | LOST 1, OVERSTATED 2 | 0 / 0 | 3 / 3 |
| `ch58-verification-audit` | PASS WITH FIXES |  | SHALLOW 1, WRONG-CORRECTION 1 | 1 / 0 | 9 / 9 |
| `ch59-easygl-metagl` | PASS WITH FIXES | yes | LOST 1, OVERSTATED 2 | 1 / 0 | 12 / 12 |
| `ch60-freedirect-freeapi` | PASS WITH FIXES |  | OVERSTATED 3 | 0 / 0 | 2 / 1 |
| `ch61-cross-platform-contract` | PASS WITH FIXES |  | OVERSTATED 2, WRONG-CORRECTION 1 | 0 / 0 | 4 / 3 |
| `ch62-windows-cross-compiling` | PASS WITH FIXES |  | LOST 1, OVERSTATED 2, WRONG-CORRECTION 1 | 1 / 0 | 2 / 2 |
| `ch63-wine-engagement` | PASS WITH FIXES |  | FALSE-DROP 1, SHALLOW 1 | 1 / 1 | 0 / 0 |
| `ch64-web-compiling` | PASS WITH FIXES |  | WRONG-CORRECTION 2 | 0 / 0 | 6 / 5 |
| `ch65-web-main-loop` | PASS WITH FIXES |  | OVERSTATED 3 | 3 / 0 | 4 / 4 |
| `ch66-web-renderer-evidence` | PASS WITH FIXES |  | OVERSTATED 1 | 0 / 0 | 2 / 2 |
| `ch67-android-macos` | PASS WITH FIXES |  | FALSE-DROP 1, LOST 1, OVERSTATED 2 | 3 / 1 | 6 / 5 |
| `ch68-diagnostics` | PASS |  | none | 0 / 0 | 2 / 2 |
| `ch69-inspector` | PASS WITH FIXES |  | LOST 1 | 0 / 0 | 6 / 6 |
| `ch68-cnatests-architecture` | PASS WITH FIXES |  | OVERSTATED 2 | 0 / 0 | 2 / 2 |
| `ch69-counting-discipline` | PASS |  | none | 0 / 0 | 6 / 6 |
| `ch70-oracles` | PASS WITH FIXES |  | LOST 1, OVERSTATED 1, WRONG-CORRECTION 2 | 1 / 0 | 5 / 3 |
| `ch71-hostile-environments` | PASS WITH FIXES |  | LOST 1, OVERSTATED 3 | 1 / 0 | 2 / 2 |
| `ch72-discipline-as-test` | PASS WITH FIXES |  | SHALLOW 1 | 0 / 0 | 0 / 0 |
| `ch73-ci-reality` | PASS WITH FIXES |  | OVERSTATED 1, SHALLOW 1 | 0 / 0 | 4 / 4 |
| `ch74-migration-guide` | PASS WITH FIXES |  | OVERSTATED 1, SHALLOW 1 | 0 / 0 | 6 / 6 |
| `ch75-blupi-case-study` | PASS WITH FIXES |  | OVERSTATED 1, SHALLOW 1 | 0 / 0 | 4 / 4 |
| `ch76-xna4-spec-auditing` | PASS WITH FIXES |  | LOST 1 | 0 / 0 | 4 / 4 |
| `ch77-samples-and-examples` | PASS WITH FIXES |  | SHALLOW 1 | 0 / 0 | 6 / 6 |
| `ch78-project-practice` | PASS WITH FIXES |  | OVERSTATED 2, SHALLOW 1 | 1 / 0 | 3 / 3 |
| `ch79-roadmap` | PASS WITH FIXES |  | OVERSTATED 1, SHALLOW 2 | 1 / 0 | 1 / 1 |
| `appendix-a-core-graphics-quick-reference` | PASS WITH FIXES |  | OVERSTATED 1, SHALLOW 1 | 3 / 0 | 7 / 7 |
| `appendix-b-feature-matrix` | PASS WITH FIXES |  | OVERSTATED 3 | 2 / 0 | 0 / 0 |
| `appendix-c-glossary` | PASS WITH FIXES |  | OVERSTATED 4 | 2 / 0 | 11 / 11 |
| `appendix-d-repo-map` | PASS WITH FIXES |  | OVERSTATED 1 | 5 / 0 | 2 / 2 |
| `appendix-e-cnaext-catalog` | PASS WITH FIXES |  | OVERSTATED 1, WRONG-CORRECTION 1 | 1 / 0 | 5 / 4 |
| `appendix-f-ecosystem-quick-reference` | PASS WITH FIXES |  | OVERSTATED 1 | 0 / 0 | 8 / 8 |
| `appendix-g-verification-tiers` | PASS WITH FIXES | yes | SHALLOW 1 | 6 / 0 | 4 / 4 |
| `appendix-h-gltf-evidence-matrix` | PASS WITH FIXES |  | WRONG-CORRECTION 1 | 0 / 0 | 11 / 10 |
| `appendix-i-native-c-api` | PASS WITH FIXES |  | SHALLOW 1 | 1 / 0 | 10 / 10 |
| `aux-plan` | PASS WITH FIXES | yes | OVERSTATED 1, SHALLOW 1 | 34 / 0 | 2 / 2 |
| `aux-next` | PASS WITH FIXES | yes | LOST 1 | 17 / 0 | 1 / 1 |
| `aux-progress` | PASS |  | none | 9 / 0 | 3 / 3 |
| `aux-readme` | PASS |  | none | 5 / 0 | 2 / 2 |
| `aux-claude` | PASS |  | none | 7 / 0 | 0 / 0 |
| `aux-audit-alpha1-delta` | PASS WITH FIXES |  | OVERSTATED 1, SHALLOW 1 | 20 / 0 | 13 / 13 |
| `aux-audit-d6e9ff05-delta` | PASS WITH FIXES | yes | LOST 1 | 13 / 0 | 14 / 14 |
| `aux-cnabugs` | PASS WITH FIXES | yes | OVERSTATED 1 | 33 / 0 | 14 / 14 |
| `aux-audit` | PASS WITH FIXES | yes | OVERSTATED 1, RESTORE-ISSUE 1 | 23 / 0 | 15 / 15 |
| `aux-editorial-audit` | PASS | yes | none | 20 / 0 | 5 / 5 |
| `aux-audit-3d-gltf-cnj` | PASS | yes | none | 18 / 0 | 21 / 21 |
| `aux-audit-content-xnb-cnj` | PASS WITH FIXES | yes | RESTORE-ISSUE 1 | 17 / 0 | 12 / 12 |
| `aux-audit-renderer-draw-path-matrix` | PASS |  | none | 6 / 0 | 7 / 7 |
| `aux-audit-platforms` | PASS | yes | none | 39 / 0 | 12 / 12 |
| `aux-audit-architecture-build` | PASS WITH FIXES | yes | OVERSTATED 2, SHALLOW 2, WRONG-CORRECTION 2, WRONG-DESTINATION 1 | 43 / 0 | 20 / 19 |
| `aux-audit-framework-core-math` | PASS WITH FIXES | yes | FALSE-DROP 1, LOST 1, OVERSTATED 1, WRONG-CORRECTION 1 | 16 / 1 | 14 / 13 |
| `aux-audit-graphics-core-effects` | PASS WITH FIXES | yes | SHALLOW 1 | 67 / 0 | 22 / 22 |
| `aux-audit-input-audio-net-services` | PASS WITH FIXES | yes | LOST 1, OVERSTATED 1, SHALLOW 4 | 27 / 0 | 18 / 18 |
| `aux-audit-renderer-catalog` | PASS | yes | none | 27 / 0 | 11 / 11 |
| `aux-audit-sibling-libraries` | PASS WITH FIXES | yes | SHALLOW 1 | 38 / 0 | 10 / 10 |
| `aux-audit-testing-verification` | PASS WITH FIXES | yes | LOST 1, SHALLOW 1 | 30 / 0 | 7 / 7 |

<!-- counts:end -->

## 5. Findings (append-only; status is updated in place)

| ID | Area | Finding | Status |
|---|---|---|---|
| AF-001 | Known Issues pages | The generator (`scripts/known_issues.py page_fragment`) marked **every** page `test-present` because `tests_current` is never empty; entries whose own text says "None"/"No test…" rendered “tests exist (not executed for this page)”. | **fixed** (commit `2a20e08`): an explicit per-entry `tests_present` (from the review), evidence basis spelled out (source-verified / reproduced / recorded by CNA / inferred) |
| AF-002 | Known Issues evidence | `confidence: reproduced` was applied to entries whose text says CNA's *own* recorded run was used and "not executed for this entry" (CNA-BUG-099, -175, -203). | **fixed**: the three entries became `recorded-by-cna`; `reproduced` is now used only where something was executed and the Evidence section names it (17 entries at the end, ten of them after an executed probe) |
| AF-003 | Known Issues duplicates | Mechanical pre-pass: CNA-BUG-215 / -219 / -226 (same `IsLatched()` defect, identical sources), -185 / -188, and several weaker pairs. | **fixed**: eight entries folded into their survivors; six further candidate pairs decided as distinct (`duplicate-review.json`); the scan is a gate of `adversarial_audit.py issues` |
| AF-004 | Ledger precision | 93 of 5,494 ledger concepts (1.7 %) cite a destination *anchor* whose section does not contain the concept's own tokens (they are elsewhere on the same page). Page-level: 0 misses. | **reduced** to 46 of 6,549 destinations (a mechanical repair and the page fixes); each remaining anchor cites a section that lacks one token of the concept, which sits elsewhere on the same page |
| AF-005 | Source graph | `NEXT-ARCHIVE-2026-07-26.md`, `PLAN-ARCHIVE-2026-07-26.md` never dispositioned. | **fixed** (commit `6dccabe`): historical snapshots, identifiers unique to them are stale backend/test/plan names; `audit/data/adversarial/source-graph.json` + a gate in `adversarial_audit.py graph` |
| AF-006 | Known Issues evidence boundary | CNA-BUG-181 and -182 cite SDL source read "at c74569ae, not the submodule revision cbe3fbe9 that TARGET pins". | **fixed** (commit `726c69f`): the supporting claims were re-read in a sibling SDL checkout at exactly cbe3fbe9 and hold; the evidence now says so |
| AF-007 | Audit tooling | A first version of the planner read the post-merge `issues-source.json`, so re-planning silently dropped an applied reclassification. | **fixed** (commit `9b5bbf7`): `known_issues.build_entries()` is pure; plans are computed against the pre-audit entries |
| AF-008 | Known Issues coverage | Four defects nobody listed, found by reviewers and re-verified by the orchestrator: BoundingSphere(Vector3, float) accepts a negative radius (XNA throws); four `GetHashCode` sums overflow `int` (UB); the SDL_GPU constructor-failure test aborts with a double free that CNA's own record calls real and unfixed; `docs/directx9-renderer.md` says custom ShaderEffect (D9-11) is not started while the plan records it closed. | **added** as CNA-BUG-250 … CNA-BUG-253 |
| AF-009 | Known Issues duplicates | CNA-BUG-215 / -219 / -226 are one root defect (the `IsLatched()` comment; CNA-BUG-219's own origin note says "cross-package duplicate"): the Phase-3 merge map missed them. | **fixed**: -219 and -226 folded into -215 |
| AF-011 | Known Issues premise | CNA-BUG-084 (`ResetElapsedTime` does nothing under the fixed step, "XNA honours it in both modes") rested on a false XNA premise: XNA's flagged fixed-step tick returns before `GameClock.AdvanceFrameTime()`, so the load's elapsed time reappears one tick later and XNA runs the same catch-up burst. The Deep Dive `game-time-and-timestep.html` repeated the premise. | **fixed**: entry retired (NOT A BUG), Deep Dive corrected |
| AF-012 | Existing pages | "Six XNA stock effects" / "SpriteEffect is XNA's 2D sprite effect class" on six Phase-1/2 pages incl. two protected ones: XNA 4.0 has five public stock effects, SpriteEffect is internal to SpriteBatch; the Phase-3 Deep Dive already said so (an internal inconsistency of the site). | **fixed** (errata 79) |
| AF-010 | Existing pages | `roadmap.html` said the C ABI release gate "has one unmet criterion" and `features.html` that it reads "Not ready because of those 468"; running `check_release_gate.py --run` in the read-only TARGET tree measures two unmet (coverage-closed, limitations-matrix); Phase-3 errata 51/63 fixed `docs/c-api.html` and two others but missed these two. | **fixed** (errata 77–78) |
| AF-013 | Known Issues pages | `public_contract` is a plain-text field that the generator escapes, but 36 detail pages carried `<code>` markup in it, so the “Affected contract” fact showed literal tags (present at `PHASE3_BASE`). | **fixed**: `known_issues.py` normalises the field and `validate` rejects markup in it |
| AF-014 | Existing pages | Double-escaped entities printed literally on two Phase-1/2 pages: a code sample in `docs/tutorials/26-tilemaps.html` (`std::vector&lt;int&gt;`) and a placeholder in `development/workflows.html` (identical at `PHASE2_BASE`). | **fixed** (errata 81) |
| AF-015 | Existing pages | The Phase-3 errata corrected a statement on one page and left the same claim on sibling pages (E1: 22 of 38 rows incomplete; ten tutorials still called `Present()` inside `Draw`, thirteen pages said the profile must be chosen “before the device exists”). | **fixed** (errata 80) |
| AF-016 | Math semantics | The math internals page said a mirrored matrix decomposes “with the reflection folded into the quaternion”; the quaternion is not a rotation, and CNA follows FNA, not the XNA IL, for mirrored and sheared inputs (found by re-reading a dismissed candidate). | **added** as CNA-BUG-259; page corrected (errata 82) |
| AF-017 | Known Issues pipeline | Three accepted severity downgrades (CNA-BUG-206, -035, -049) were recorded as `accept` decisions without the `severity` key, so the change silently did not land while this ledger said it had; found when the start-versus-final transition table was recomputed. | **fixed**: applied (2 high · 47 medium · 183 low); the planner now reports an accepted reviewer severity proposal without a `severity` key as pending |
| AF-018 | Known Issues text | Hand-written references from one entry to another by final id went wrong when a later reclassification shifted the id allocation: CNA-BUG-268 cited CNA-GAP-068 (the video gap) for the network-session gap; a reviewer's text cited a reclassified entry by number. | **fixed**: `{{issue:ID}}` placeholders resolved after allocation; all 14 remaining prose references to audit-numbered ids were read against the entry they name |
| AF-019 | Source coverage | The 21 auxiliary documents (1,502 of the ledger's concepts: the fact stores the chapters were written from) had been dispositioned but not independently reviewed. | **done** (§6): 21/21 reviewed, 31 findings, four new Known Issues (CNA-BUG-271 … 274) and two corrected ones (CNA-BUG-228, -235) |
| AF-020 | Known Issues links | 24 entries were linked from a page's own prose while that page was missing from the entry's related documentation. | **fixed**: reciprocal (0 missing; checked by script) |
| AF-021 | Existing pages | `docs/tutorials/02-setup.html`, `118-dynamic-audio.html` and `docs/building.html` presented `CNA_STRICT_XNA_API` as a CMake option that gives a compile error (it is a compile definition on two harness targets that yields a deprecation warning); `contribute.html` presented two fixed `known_bugs.md` entries as open work; `docs/tutorials/109-metal-macos.html` called a run-time answer a compile-time constant. | **fixed** (aux reviews X1–X3); the `contribute.html` card retitle is recorded as a disposition |
| AF-022 | Audit tooling | A re-render of the Phase-3 ledger (`bible_ledger.py render`) would overwrite the original Phase-3 wording of `audit/bible-absorption-phase3.md`. | **fixed**: a correction note appended below the marker `post-phase3-correction` survives a re-render; the originals are otherwise untouched |
| AF-023 | Audit tooling | The applied-fix ledger only proved that a page still existed. A fix applied to a *generated* page (the Known Issues overview) was silently overwritten by the next regeneration, and three later edits had reworded text that earlier fixes added. | **fixed**: every recorded fix carries a probe (a run of the added text) and `apply_page_fixes.py check` fails when it is no longer on the page; the overview wording now lives in its generator |

## 6. Bible knowledge-conservation review (independent, complete)

### 6.1 Scope and method

Every source unit of the frozen book received an independent review status. Nothing was taken from the Phase-3 ledger without being opened.

| Set | Units | Reviewed by | Result |
|---|---:|---|---|
| Canonical text units (front matter 4, chapters 83, appendices 9, nested fragments 2) | **98** | 13 reviewer groups (C01–C13), each told to *prove the absorption wrong* | PASS 17 · PASS WITH FIXES 81 · FAIL 0 (98/98) |
| … of which large units (≥ 2,500 source words), reviewed section by section | 20 | the same reviewers, all sections, destination sections opened | all 20 PASS WITH FIXES |
| Figure sources | 20 | the orchestrator, node by node and edge by edge against the destination diagram (§6.4) | 20/20 conserved |
| Raster images | 5 | ledger disposition SUPERSEDED (Software screenshots of older revisions) re-read | 5/5 correct |
| Auxiliary documents (`NEXT.md`, `PLAN.md`, `PROGRESS.md`, `README.md`, `CLAUDE.md`, `AUDIT.md`, `EDITORIAL-AUDIT.md`, `cnabugs.md`, 13 subsystem audits) | **21** | 4 reviewer groups (X1–X4), same brief, adapted to fact stores | PASS 8 · PASS WITH FIXES 13 · FAIL 0 (21/21) |
| Dated archive snapshots, book tooling, build output | 13 entries | dispositioned with a reason in `audit/data/adversarial/source-graph.json`; a gate fails when a Bible top-level or `audit/` markdown file is in none of the three sets | — |

Each reviewer received, per unit: the source path; a **section map** (Bible section → source words → words of the destination sections the ledger cites); the **residual paragraphs** (source paragraphs whose distinctive vocabulary is not covered by any single site page — computed against the whole published site, independently of the ledger); the **absent identifiers** (present in the unit and at TARGET, on no page); every **dropped disposition** (HISTORICAL ONLY, REMOVED FUNCTIONALITY, OBSOLETE, SUPERSEDED, DUPLICATE, TARGET CONTRADICTED, FIXED BUG) with the ledger's evidence; and the **TARGET corrections** the ledger recorded. The procedure required reading the whole source, grading every section of a large unit (full / partial / thin / absent) against the destination section it cites, resolving every residual (covered / stale at TARGET / lost-useful / narrative), verifying every dropped disposition at TARGET (a FIXED BUG needs *positive* evidence — the fixing code and the test that pins it), re-deriving at least fifteen TARGET corrections by consequence, and flagging every sentence that claims more than the evidence supports. The reviewers wrote their findings with a ready-to-apply fix; the orchestrator re-verified the consequential ones at TARGET, applied each fix mechanically with a proof that it landed (`scripts/apply_page_fixes.py`: exact-once replace or append at an existing heading, recorded in `audit/data/adversarial/applied-page-fixes.json`) and repointed the ledger.

### 6.2 Results

The counts below are generated (§4.1); this section explains them.

* **Canonical units: 223 findings** — OVERSTATED 100, WRONG-CORRECTION 47, SHALLOW 45, LOST 25, FALSE-DROP 4, RESTORE-ISSUE 1, WRONG-DESTINATION 1; 72 medium, 151 low. **221 fixed** on the site or in the ledger, **1 restored** as a Known Issue (Vulkan passes XNA's normalised `DepthBias` unscaled: CNA-BUG-264) and **1 owner decision** (§6.5).
* **Auxiliary documents: 31 findings** — OVERSTATED 8, SHALLOW 11, LOST 5, WRONG-CORRECTION 3, RESTORE-ISSUE 2, FALSE-DROP 1, WRONG-DESTINATION 1; 28 low and 3 medium. All applied; the two RESTORE-ISSUE findings became CNA-BUG-272 to CNA-BUG-274, and the stale `known_bugs.md` entries that the same review found behind a wrong Contribute-page card became CNA-BUG-271.
* **Evidence examined:** 894 residual paragraphs and absent-identifier clusters (24 *lost-useful*), 753 dropped dispositions (**5 false drops**, 1 restore-issue), **1,118 ledger TARGET corrections re-derived from source (29 disagreements, 2.6 %)**.
* **475 recorded page fixes on 195 pages**, plus direct corrections of Known Issues text and 83 ledger records changed or added.

What the reviewers found is more instructive than the totals. The *absorption* itself held: the reviewers did not find a large body of missing knowledge, and the two directions of the review agree on that (the independent recall analysis of §2(b) and the section-by-section reading). What did not hold was **strength and correction**:

* **OVERSTATED (108).** Site statements stronger than TARGET supports, mostly inherited from the source or from a ledger "correction": `CNA_STRICT_XNA_API=ON` "turns a call into a compile error" (it is a compile definition on two harness targets and yields a deprecation warning); the Emscripten multi-renderer lane described in terms that read as renderer evidence although it establishes configure, build and link only; `Immediate` described as one GPU draw per `Draw()` although grouping happens below the renderer seam; "device loss is reported by" family lists that still disagreed with TARGET; unqualified "byte-exact" on an oracle tier row; "verified" for statements that rest on reading.
* **WRONG-CORRECTION (50).** A Phase-3 *TARGET correction* recorded as "confirmed" that was itself wrong or incomplete, so the page repeated a wrong "fix": a WebAssembly link-flag claim (JSPI against Asyncify, which CNA's own link line silently overrides: CNA-BUG-262), the renderer families that keep the logical-coordinate contract (Metal was grouped wrongly), how a redundant render-target bind behaves on Direct3D 11/12, whether CNA's oracle chain references the XNA decompilation, the `Model::Tag` contract of skinned models. Twenty-seven of the 895 corrections re-derived for the canonical units disagreed with TARGET.
* **SHALLOW (56) and LOST (30).** Detail that survived as one clause or not at all: the compass azimuth formulas and the landscape axis remap, the XACT magic numbers and byte-swap rule, the direction-button dead-zone threshold, `NetworkSessionJoinError` producers, the HTML_DOM atlas-edge bleed and browser tolerances, the `Prop.hpp` macro shape, the Vulkan 32-byte vertex / 128-byte push-constant contract, the default-backbuffer stencil rule of EasyGL, the `Game::Update` member-vector re-entrancy hazard.
* **FALSE-DROP (5).** Items dispositioned as fixed, history or superseded that are current at TARGET: the Proton "fabricated Steam tree" result (still how the Direct2D lane is qualified), the macOS 143-test / 136-pass record, the LZX cross-implementation fuzz oracle, an executable demo comparison, and the orientation-from-window-bounds rule of `GameWindow` (the ledger had called it alpha.1).
* **RESTORE-ISSUE (3).** A "test defect" closure that hid a real Vulkan defect (CNA-BUG-264) and CNA documents that still contradict the code (README.md and CLAUDE.md/AGENTS.md: CNA-BUG-273, CNA-BUG-274; misc/cnj.md: CNA-BUG-272).

### 6.3 Ledger delta

`audit/data/bible/records/` after the audit, compared with `PHASE3_BASE`: concepts **6,019 → 6,049** (+30: 29 NEW PAGE and one HISTORICAL ONLY provenance concept). NEW PAGE 3,493 → 3,530; HISTORICAL ONLY 345 → 342; SUPERSEDED 145 → 144; FIXED BUG 121 → 120; TARGET CONTRADICTED 54 → 53; OBSOLETE 18 → 17; every other disposition unchanged. Eight dispositions that *dropped* knowledge were reversed to NEW PAGE after review (four HISTORICAL ONLY, one each of OBSOLETE, TARGET CONTRADICTED, FIXED BUG and SUPERSEDED); 83 records changed in destinations, tokens, notes or TARGET result, and the recorded TARGET result of 14 concepts moved from *confirmed* to *corrected* or *contradicted*. The original Phase-3 records are otherwise untouched, and each edited record carries a "post-Phase-3 adversarial audit" note.

### 6.4 Figures, code examples, spot reconstruction

* **Figures.** All 20 figure sources (`fig-*.tex`) were extracted (alt text, nodes, edges, caption) and compared with the redrawn diagram at the destination the ledger cites, node by node and edge by edge, then read for semantic correctness at TARGET. Every diagram conserves the source topology and is *richer* than the source; the TARGET corrections the ledger claimed (nine option-gated effect families rather than eight; 44 sharp-runtime modules and 47 names; Asyncify suspension instead of a registered callback; a literal-`.cnb` tier in `ContentManager` resolution; LZ4 in the XNB container; 25 identities mapped to 21 families) were re-derived. Of 190 node and edge labels in the sources, 45 contain a word that the destination page does not use; each was read, and all are rewording or belong to a retired renderer (`D8VK`). The five rasters are Software screenshots from older revisions, not reproduced, correctly SUPERSEDED.
* **Code examples.** The 126 C++ blocks of the Deep Dive and Development pages were compiled as fragments against the TARGET headers by `scripts/check_cpp_blocks.py` (kitchen-sink include of all 494 public XNA-namespace headers and 1,043 Sharp Runtime `System` headers; each block inside a function with typed context parameters, or at namespace scope when it starts with a declaration): 23 blocks report an API-level diagnostic, and every one is missing context or an omitted namespace of a symbol that exists at TARGET (`CNA::Input::Haptics`, `Power`, `Microsoft::Devices::Sensors::SensorReadingEventArgs`, sibling-library namespaces); none names a member, type or overload that does not exist. The two complete programs of `first-game-walkthrough.html` compile syntax-clean.
* **Known Issues links.** The 1,419 pinned source links on the Known Issues detail pages resolve (`check_source_links.py`). For the 1,184 that carry a symbol in their note, the named symbol (or its last scope segment) occurs in the linked file in all but 24 cases, and each of those 24 is a note that states an *absence* ("no IDBFS mount", "no `SetSamplerAddressMode` override", "none for `SetPosition`"), which was read. Of the 912 links from entries to documentation pages, 11 share no identifier with their entry; all 11 were read and all are relevant. 24 entries whose own prose cited a page that was not in their related list were made reciprocal (AF-020), and the 14 prose references from pages to audit-numbered entries were each checked against the entry they name.
* **Independent spot reconstruction (without the ledger's destination mapping).** For the runtime (ch06), math (ch07), GraphicsDevice/resources (ch12, ch14), renderer (ch19, ch22, ch28), Content (ch33–ch36), model (ch38, ch39, ch41), input/audio (ch44, ch45), platform (ch61–ch67) and C API/verification (appendix G, appendix I, ch70) chapters the reviewers located each important idea on the site by their own search, then compared with the ledger. Ideas the ledger missed are exactly the LOST findings above (a ledger concept `…-advNN` now exists for each).

### 6.5 The one owner decision

`production-method-F1` (LOST, low): the book states how it was produced (a sentence on AI-agent assistance and maintainer responsibility). The site has no equivalent statement about *its own* production. Adding one would state a policy on the owner's behalf, so nothing was added; the statement is recorded as a HISTORICAL ONLY concept (`WPB…-adv01` of that unit) with the reason, and is listed in the final report.

### 6.6 Independent recomputations that agreed with Phase 3

Bible graph (118 book files); the 350 = 218 + 62 + 15 + 55 arithmetic and the 2/46/170 severities; 350 pages = 350 entries; sitemap and search 781 = every page except `404.html` and `search.html`; 62 Bible bug ids = 31 survive + 3 reclassified + 16 proven fixed + 5 obsolete + 7 not a bug; 566 candidates = 566 dispositions; presentation against `PHASE2_BASE`; volatile facts recomputed from TARGET (25 renderer identities, 20 workflows, 39 top-level oracle scenes + 7 null-texture = 46 files, 61 C API headers, ABI 0.29.0); the oracle scene denominators; no post-TARGET identifier on the site; every Deep Dive page has ≥ 2 in-body inbound links and ≥ 1,391 words; 8,767 pinned source links resolve.

## 7. Known Issues — independent adversarial review

### 7.1 Coverage

| Population | Entries | Reviewed by | Result |
|---|---:|---|---|
| The 350 entries Phase 3 published | 350 | 17 reviewer batches (R01–R15, HM1, HM2; 7–30 entries each), each entry read against TARGET by a reviewer whose brief was to *refute* it (verdicts CONFIRMED · CORRECTED · NARROWED · RECLASSIFIED · DUPLICATE · FIXED AT TARGET · NOT A BUG · INSUFFICIENT EVIDENCE) | 344 individually re-read; the other 6 were folded before review as identical-source duplicates of an entry that was re-read |
| … all 2 high, all 46 medium and all 170 low bugs, all 62 functional gaps, all 15 platform limitations, all 55 verification gaps | 350 | the same batches (the medium bugs outside a subsystem batch, 15 of them, form HM1 and HM2) | see 7.2 |
| The 121 candidates Phase 3 *dismissed* (fixed, obsolete, not a bug, insufficient evidence) | 121 | 4 reverse-review batches (D1–D4) told to prove each dismissal wrong | 105 dismissals confirmed; 13 restored (1 bug, 6 narrowed entries, 1 gap, 5 verification gaps), 2 already published, 1 unresolved candidate settled by a probe and restored — see 7.5 |
| The 39 entries this audit created or reclassified | 39 | 27 re-read by an independent batch (R16) that had not seen them; the 4 documentation-drift entries added last by another (R18); 8 reclassified entries by their original batch | every one has an independent verdict |
| A stratified sample: both high bugs, medium / low, old and new ids, every evidence basis, every class, every subsystem | 34 | an extra-deep second look (R17) allowed to *execute* probes built from the TARGET sources | HOLDS 16 · HOLDS WITH NOTES 11 · NEEDS CORRECTION 7 · **REFUTED 0**; a probe was executed for 24, compile-and-run probes for 12 |

A reviewer's verdict was a *proposal*. Text corrections and evidence flags were applied by `scripts/audit_issue_review.py plan` as data; class changes, folds, retirements and severity changes were listed as pending until the orchestrator adjudicated each in `audit/data/adversarial/decisions.json` (with the reason), re-reading the TARGET source for every one that was contestable. The generated numbers are in §4.1.

### 7.2 Result on the 350 Phase-3 entries

Verdicts (344 individually re-read): **CONFIRMED 224 · CORRECTED 95 · NARROWED 12 · RECLASSIFIED 8 · DUPLICATE 2 · NOT A BUG 3.** About a third of the entries (107) therefore needed a correction of text, scope, evidence basis or test claim; 13 of 344 (4 %) were wrong enough to change whether the defect exists or what kind of entry it is (3 retired, 8 reclassified, 2 folded). One statement was wrong on every page: **the footer "tests exist" was false for 39 of the surviving entries** (AF-001).

| | Phase 3 | Final |
|---|---|---|
| Entries | 350 = 218 bugs · 62 functional gaps · 15 platform limitations · 55 verification gaps | **370 = 232 bugs · 70 functional gaps · 12 platform limitations · 56 verification gaps** |
| Bug severity | 2 high · 46 medium · 170 low | **2 high · 47 medium · 183 low** |
| Status | 336 open · 14 narrowed | 353 open · 17 narrowed |
| Evidence basis | verified-by-reading 330 · reproduced 9 · strong 9 · probable 2 | verified-by-reading 325 · **reproduced 17** · recorded-by-cna 13 · strong 13 · probable 2 |
| Entries whose page says a test touches the area | 350 of 350 (every page carried the label) | **325 of 370** |

Operations (every id is stable; none is renumbered, and a retired or folded id is never reused):

* **Retired, 3 (NOT A BUG):** CNA-BUG-084 (the XNA IL shows a flagged fixed-step tick returns before `AdvanceFrameTime()`, so `ResetElapsedTime` behaves as in CNA; the page premise was false and the Deep Dive was corrected), CNA-BUG-089 (XNA's `GraphicsDeviceManager.Dispose(bool)` has no re-entrancy guard either), CNA-BUG-136 (dropping the two ISO-layout scancodes is an accepted, tested decision matching FNA, already stated in the input-model Deep Dive).
* **Folded, 8:** CNA-BUG-187 → 190, 188 → 185, 219 and 226 → 215 (one `IsLatched()` comment defect reported under three ids), CNA-VGAP-043 → 026, 045 → 023, 048 → 025, 050 → CNA-GAP-013 (each survivor keeps the folded entry's summary and sources).
* **Reclassified, 8:** CNA-BUG-079, -100, -108, -127 → functional gaps (CNA-GAP-063 … 066: the behaviour is a documented or inherited limit, not a contract violation), CNA-PLAT-008, -010, -015 → functional gaps (CNA-GAP-067 … 069: no host constraint forces the behaviour), and CNA-GAP-050 → bug CNA-BUG-250 (`LocalNetworkGamer::SendData` in a Local session silently drops every packet, which violates the API contract).
* **Added, 31** (CNA-BUG-251 … 274, CNA-VGAP-056 … 060, CNA-GAP-070 … 071): 27 found while re-reading something else or restored from a dismissal, then 4 CNA documentation-drift entries from the auxiliary review. Five are medium bugs: CNA-BUG-253 (SDL_GPU constructor-failure double free that CNA's own record calls real), -259 (`Matrix::Decompose` follows FNA, not XNA 4.0), -264 (Vulkan passes XNA's normalised depth bias unscaled), -267 (a join beyond `MaxGamers` is welcomed and never rostered) and -268 (a `NetworkSession` callback that calls `End*` frees the closure it is running in).
* **Broadened, 3:** CNA-VGAP-020 (the hand-written platform test filter misses a suite, recomputed at *case* level after a first count that matched suite names only: eight further suites, not nine), CNA-BUG-235 (four stale Sharp Runtime rows of one CNA document), CNA-VGAP-025 (absorbs the OPENGLES2/FNA3D observation of the folded umbrella).
* **Severity, 4 changes:** CNA-BUG-206, -035 and -049 medium → low (tooling or CI-evidence only, or a memory-safety exposure that needs a deliberate call on a method XNA hides); CNA-BUG-146 low → medium (the video converter is hard-wired full-range BT.601, so most real limited-range video shows lifted blacks). Both HIGH bugs were re-derived by the orchestrator and then *reproduced by execution* (R17): CNA-BUG-001 (`Plane::Transform` through an aliased `Matrix::Transpose` returns a normal of (1, 1, 0) where XNA gives (0, 1, 0)) and CNA-BUG-137 (`MediaPlayer::Play(Song*)` clears the queue that owns the song before copying it: an AddressSanitizer heap-use-after-free).

### 7.3 Corrections that mattered

* **False test claims (AF-001).** The generator stamped every page "tests exist" because a text field is never empty; entries that said "None" rendered the opposite. Each entry now carries an explicit flag from its reviewer; the callout names the evidence basis (source-verified · reproduced · recorded by CNA · inferred).
* **Overstated evidence (AF-002).** `reproduced` had been applied to entries whose text says CNA's *own recorded* run was used and "not executed for this entry": three became *recorded by CNA*. Conversely, ten entries became `reproduced` only after a probe built from the TARGET sources actually showed the failure (R17).
* **Wrong premises.** CNA-BUG-084 (a false XNA premise), CNA-BUG-101 (the Direct2D refusal cannot fire in `Reset` because the formats are normalised first), CNA-BUG-215 ("a failed construction leaves the choice open": only a failed *resolution* does), CNA-BUG-224 (five families raise `DeviceLost` from real error paths, not six), CNA-BUG-190 (`DIRECTX11;DIRECTX12` is *not* hit), CNA-BUG-045 (the contract is the vendoring convention, not `docs/xnb-interoperability.md`), CNA-BUG-001 (FNA makes the same aliased call; what is safe there is FNA's alias-safe `Matrix.Transpose`).
* **Unpublished defects.** 31 entries the pipeline had not published were added: among them the `BoundingSphere` constructor that accepts a negative radius, the overflowing `GetHashCode` sums, the SDL_GPU constructor-failure double free, a stale renderer status document, the restored dismissals, and four CNA documents that contradict their own code.
* **Evidence-boundary repairs.** CNA-BUG-181/182 cited SDL read at a revision the snapshot does not pin; the claims were re-read at the pinned revision. PLAT-015/GAP-069 states plainly which facts come from an unpinned sibling checkout.

### 7.4 Old identifiers CNA-BUG-001 … 062 (the Bible's own ledger)

All 62 are reconciled with a recorded reason (`audit/data/bible/issues/dispositions.json`, and `aux-cnabugs` in the ledger): **32 survive as bugs** (31 with their own id, and CNA-BUG-043 as CNA-BUG-260), **2 as functional gaps** (024 → CNA-GAP-001, 046 → CNA-GAP-048), **2 as verification gaps** (032 → CNA-VGAP-019, 038 → CNA-VGAP-056), **16 are proven fixed** (each with the fixing code and a test), **4 are obsolete** (their renderer families are retired), **6 are not bugs** (019, 020, 023, 033, 034, 042: XNA/FNA-faithful or unreachable). Phase 3 had 31 + 3 survivors, 16 proven fixed, 5 obsolete and 7 not a bug; the audit moved one entry out of "not a bug" (BUG-043 became a bug) and one out of "obsolete" (BUG-038 became a verification gap for the current renderer families).

### 7.5 Dismissals and FIXED BUG claims challenged

The 121 dismissed candidates were re-read by reviewers told to prove each dismissal wrong: **105 dismissals confirmed**. The others: 1 restored bug (`Matrix::Decompose` against the decompiled XNA IL — re-derived by the orchestrator by porting both algorithms to a float32 model), 6 narrow restores, 1 restored gap and 5 restored verification gaps, 2 already published and 1 unresolved candidate settled by an emscripten probe. In the conservation review, of the 244 dropped dispositions of the canonical units reviewed (FIXED BUG among them) 4 were false drops, and of the 509 in the auxiliary documents 1: a FIXED BUG needs positive evidence at TARGET (the fixing code and the test that pins it), and where a defect survived (a Vulkan depth bias closed as "a test defect") it was restored as CNA-BUG-264.

### 7.6 Classification, duplicates and severity

* **Boundaries.** The class definitions of the overview page were applied literally: a *bug* violates an intended or documented contract; a *functional gap* is a narrower contract that nothing violates; a *platform limitation* needs a host or toolchain constraint that CNA cannot lift; a *verification gap* has an implementation but insufficient evidence. Eight entries moved. Where a class question remained open the entry says why it stays (CNA-GAP-008, CNA-PLAT-011).
* **Duplicates.** A mechanical similarity scan (title, summary, contract, shared source path; cosine ≥ 0.5) flags candidate pairs; each pair that survives is decided in `audit/data/adversarial/duplicate-review.json` (six recorded as distinct, with the reason) and `adversarial_audit.py issues` fails on an undecided pair. Eight entries were folded as true duplicates (7.2).
* **Severity.** The categorical scheme (high · medium · low; a triage suggestion) was kept and applied by the rubric of the review brief (high: crash, memory-safety violation, data loss or silently wrong results on a widely used public path; medium: wrong or missing behaviour on a supported path a typical user or maintainer will plausibly hit; low: narrow edge cases, tooling, documentation drift). Every high and medium bug was re-read by this audit's reviewers, both high bugs and the contested mediums a second time by the orchestrator.

### 7.7 What this review does not establish

Nothing was built as a whole and no CI result was read; entries are *source-verified* unless they say otherwise. Twelve probes compiled TARGET sources against a sibling Sharp Runtime checkout that TARGET does not pin (each says so). CNA-BUG-137 and CNA-BUG-001 are reproduced on the code paths described, not in a full engine run. The extra-deep sample found no refutation in 34 entries (95 % upper bound on the share of refutable entries: about 9 %), but 7 of the 34 still needed a correction of detail: the list is accurate about what is wrong and occasionally imprecise about the details.

## 8. Evidence, terminology, count and rendering audits (complete)

* **Evidence vocabulary (Known Issues).** Phase 3 stamped every detail page “tests exist” (`tests_current` is never empty) and used `reproduced` for entries whose text says CNA's own recorded run was used (AF-001, AF-002). Now: an explicit per-entry `tests_present`; the page callout names the basis (source-verified · reproduced · recorded by CNA · inferred); the overview lists the vocabulary. Distribution in §4.1. Entries labelled `reproduced` are those for which something was executed and the Evidence section names it (for example the header-only `Json.hpp` depth probe, `check_no_posix_setenv.py`, the software diff script with `/usr/bin/cp` as the renderer, `test_coverage_scope.py`, the devices-tests filter scan).
* **Strong-claim terms on the new Deep Dive and Development pages** (“verified”, “proven”, “identical”, “byte-exact”, “bit-exact”, “pixel-exact”, “matches XNA”, “all/every renderer”): every occurrence of “matches XNA”, “pixel-exact”, “bit-exact” and “all renderers” (16) was read in context and “byte-exact” (14), “guaranteed” (10) and “proven/proved” (58) were sampled. None asserts a run that was not made: the oracle statements are attributed to CNA's recorded corpus (“recorded pixel-exact on all 39 through Wine and DXVK”, “an empirical match, not a proof”), the XNA-parity statements name the IL or the test they rest on, and the unqualified “byte-exact” of the oracle tier row was corrected by the ch28 review (`direct3d-evidence-and-wine.html#evidence-ladder`).
* **XNA-oracle denominators.** 39 committed scenes / 31 in the last dated report / 46 scene files (39 top-level + 7 null-texture) / 18 of 39 byte-exact for SOFTWARE trace to CNA text at TARGET; no page divides by a different total.
* **Volatile counts.** 25 renderer identities, 21 implementation families, 20 workflows, 61 C API headers, ABI 0.29.0 recomputed from TARGET; the Known Issues totals on every hub, on the overview and in `data/known-issues.json` are generated from one list and checked by `validate_all.sh` (`adversarial_audit.py issues`), so no page carries a typed count that can go stale. A text search for “350”, “218” and “62 functional” finds only entry identifiers.
* **Post-TARGET contamination.** CNA's live checkout is now 12 commits past TARGET (other sessions kept committing during this audit; the audit never read them). Every identifier those commits add (138 that do not exist in the TARGET tree) was searched on the final site: only `GpuTimerTests` appears, and it is a TARGET file name, not a symbol.
* **Rendering leakage (visible markup, double-escaped entities, template braces, temporary ids, unresolved `{{issue:…}}` placeholders)** was scanned statically over all 803 public pages and dynamically by the QA harness (`MARKUP-LEAK`): AF-013 (36 Known Issues pages) and AF-014 (two earlier pages) were fixed; the remaining hits are code samples (C++ initializer braces, an Emscripten shell template, a GitHub Actions expression) and prose about `<div>` elements and XML escaping.
* **Code examples.** The two complete programs in `deep-dives/framework/first-game-walkthrough.html` compile syntax-clean against the TARGET headers (`scripts/check_snippet.sh`, g++ 14, C++23). All 126 C++ blocks of the Deep Dive and Development pages were then compiled as fragments (`scripts/check_cpp_blocks.py`, report-only, nothing built): a kitchen-sink include of every public XNA-namespace header of CNA (494) and every Sharp Runtime `System` header of the local checkout (1,043), each block inside a function with typed context parameters (or at namespace scope when it starts with a declaration). 23 blocks report an API-level diagnostic; each was read, and all are missing context (a variable or type the fragment does not declare, a sibling-library namespace) or an omitted `using` for a symbol that exists at TARGET (`CNA::Input::Haptics`, `Power`, `Microsoft::Devices::Sensors::SensorReadingEventArgs`); none names a member, type or overload that does not exist.

## 9. Preservation, validation and browser QA

* **Protected Phase-1/2 content** is unchanged except where the audit corrected a statement or a rendering defect (errata 77–82 and the aux-review corrections of `contribute.html`, `docs/building.html` and tutorials 02, 109 and 118): `compare_presentation.py` against `PHASE2_BASE` reports 0 unexplained losses (11 dispositioned: the retired book sites, the documented `architecture.html` retitle and the two retitled parts of `docs/model-loading.html` and `contribute.html`, each with its reason); Homepage Quick Stats, the Showcase, the Speedy Blupi section and its Play in Browser call to action, Development / Human Takeover / Maintainer Handbook, the tutorials and the demos/media are intact.
* **Browser QA** (headless Chrome via CDP, `scripts/browser_qa.py`), final content: **352 pages × {1400 px, 390 px} × {light, dark} = 1,408 renders** — all 231 non-Known-Issues pages changed by the audit, and 121 Known Issues pages (the 5 hubs, the overview, all 39 created or reclassified entries, the 34 sampled entries and 45 random others). **0 horizontal overflow, 0 broken images, 0 console errors**; the global header is on two rows at 1400 px and collapsed at 390 px on every page. 164 renders were flagged, all in three classes: **116 × the pre-existing pager-label contrast of 4.12 in dark mode** (`--text-muted` on the dark background), **24 × a contrast of 2.68 for Prism's green class-name token inside CMake code blocks** (`CNA::CApi`, `CNA::Design`, …; identical on a copy of the `PHASE2_BASE` page, so it is not introduced by Phase 3 or by this audit), and **24 × `MARKUP-LEAK`**, each of which is legitimate prose about `<div>` elements or about the escaped forms `&amp;` `&lt;` `&gt;`. **The site is not visually perfect:** the two contrast items remain and were left alone because `css/style.css` is a Phase-1/2 asset that this audit was not asked to redesign.
* **Validation.** `scripts/validate_all.sh` (`PHASE3_FINAL=1`) is overall PASS: site and presentation validators, `compare_presentation` for the three phases, fact checks, source-link resolution (all pinned links), retired-renderer scan, Deep-Dive page checks, the Bible ledger (`--final`: 119/119, 0 errors, 0 warnings), the source-graph, anchor, Known-Issues and duplicate gates, the generated counts block (a stale block fails the run), the recorded page fixes, and `git diff --check`. The final gate also fails unless every canonical unit (98), auxiliary document (21), Phase-3 entry (350) and audit-added entry (31) has an independent review.
* **Sibling repositories** were not modified by this audit: the Bible (`4df1475c`, 86 modified or untracked paths) and the Developer repository (`9f07046d`, 7 paths) have the same HEAD and status counts as at the start; CNA's HEAD moved from `5229c992` (11 commits after TARGET) to `cefe6c83` (12) through a commit by another session, and its working tree still shows only the untracked `startup-metrics.log`. `cnahead` is exactly the TARGET SHA and one newline (41 bytes). Nothing was pushed.
