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
| Evidence basis | probable 2 · recorded-by-cna 13 · reproduced 7 · strong 13 · verified-by-reading 335 |
| Entries with a test touching the area | 325 of 370 |
| Subsystems | Graphics & renderers 68 · Documentation & release tooling 48 · Testing & evidence 43 · Networking & gamer services 32 · Math & geometry 26 · Build & CI 25 · Core & runtime 22 · Audio & media 20 · Platforms 20 · Content & XNB/CNB/CNJ 16 · Models & glTF 14 · Storage 10 · Input 9 · Diagnostics & Inspector 9 · C API & bindings 8 |
| Audit operations recorded in `dispositions.json` | folded 8 · retired 3 · reclassified 8 · added 31 |
| Independent issue reviews ingested | 344 of the 350 Phase-3 entries re-read individually (CONFIRMED 224, CORRECTED 95, DUPLICATE 2, NARROWED 12, NOT A BUG 3, RECLASSIFIED 8), plus 6 more folded as identical-source duplicates into a re-read survivor (BUG-187, BUG-188, BUG-219, BUG-226, VGAP-043, VGAP-045); entries added by the audit that a separate reviewer then tried to refute: 31 of 31 |
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
| AF-002 | Known Issues evidence | `confidence: reproduced` was applied to entries whose text says CNA's *own* recorded run was used and "not executed for this entry" (CNA-BUG-099, -175, -203). | open — the reviewers propose `recorded-by-cna`; applied at adjudication of the affected batches |
| AF-003 | Known Issues duplicates | Mechanical pre-pass: CNA-BUG-215 / -219 / -226 (same `IsLatched()` defect, identical sources), -185 / -188, and several weaker pairs. | open |
| AF-004 | Ledger precision | 93 of 5,494 ledger concepts (1.7 %) cite a destination *anchor* whose section does not contain the concept's own tokens (they are elsewhere on the same page). Page-level: 0 misses. | open |
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

## 6. Progress log (updated at each checkpoint; the final sections replace this one)

### 6.1 Known Issues — independent re-review (reviewers told to refute; verdicts stored in `audit/data/adversarial/issue-reviews/`)
Batches by subsystem; a verdict is a *proposal*: `audit_issue_review.py plan` applies text corrections and evidence flags automatically and lists severity changes, reclassifications, duplicates and retirements as *pending* until `decisions.json` adjudicates them.

| Batch | Scope | Reviewed | Confirmed | Corrected | Reclassified | Removed |
|---|---|---:|---:|---:|---:|---:|
| R10 | Math & geometry | 23 | 18 | 5 | 0 | 0 |
| R14 | Content & Models | 30 | 26 | 3 | 1 (CNA-BUG-127 → functional gap) | 0 |
| R01 | Graphics & renderers, part 1 (16 low + 5 high/medium bugs) | 21 | 12 | 6 (+1 narrowed) | 2 (CNA-BUG-100, -108 → functional gaps) | 0 |
| R08 | Networking, gamer services, storage | 26 | 22 | 2 | 1 (CNA-GAP-050 → low bug) | 2 (CNA-BUG-084, -089 NOT A BUG); 4 folds |
| R11, R12 | Platforms, Testing & CI, Build (part) | 43 | (see `audit/data/adversarial/issue-reviews/`) | | | |
| HM1, HM2 | All remaining medium bugs (15) | 15 | 10 | 5 (CNA-BUG-199, -200, -176, -112, -113) | 0 | 0; severity CNA-BUG-206, -035, -049 medium → low |

Independently re-verified by the orchestrator (not delegated): **both HIGH bugs** — CNA-BUG-001 (aliased `Matrix::Transpose` in `Plane::Transform`) and CNA-BUG-137 (`MediaPlayer::Play(Song*)` clears the queue that owns the song before copying it) — confirmed by reading; CNA-BUG-121 (spot check of a contestable medium; reviewer right); two reviewer *corrections* (CNA-GAP-034 `DateTime(ticks, kind)` exists in sharp-runtime; CNA-GAP-036 `gltf_to_cnj` takes a positional `unitScale`) — both true.
Re-executed by the orchestrator: CNA-BUG-062 (`generate_coverage_inventory.py --check` and `generate_limitations.py --check` exit 2, naming `modules/design|diagnostics|inspector/include`), CNA-BUG-200 (`check_no_posix_setenv.py` exit 1, twelve lines), CNA-BUG-016 (header-only `Json.hpp` probe: 1,000 and 10,000 levels parse; 50,000 and 100,000 levels SIGSEGV with the default 8 MiB stack, g++ 14.2 -O0 and -O2; probe removed from `build-probe/`).

### 6.2 Independent recomputations that agreed with Phase 3
Bible graph (118 book files); 350 = 218 + 62 + 15 + 55 entries and 2/46/170 severities; 350 pages = 350 entries, 0 orphans; sitemap and search 781 = every page except `404.html`/`search.html`; 62 Bible bug ids = 31 survive + 3 reclassified to gap/verification gap + 16 proven fixed + 5 obsolete + 7 not a bug; 566 candidates = 566 dispositions, 345 published entries with origins + 5 new findings; presentation against `PHASE2_BASE` (all 308 pages: only the 5 hrefs and 3 headings tied to the retired book sites and the documented `architecture.html` retitle are gone; 0 lost images/videos/ids, 0 shrunk pages); Deep Dives hub page counts (14 groups, 104 pages); volatile facts recomputed from TARGET (25 renderer identities, 20 workflows, 39 top-level oracle scenes + 7 null-texture = 46 files, 61 C API headers, ABI 0.29.0, SOFTWARE "10 → 18 of 39 byte-exact"); oracle scene denominators on the site (39 / 31 / 46 / 7 / 18 of 39 / 10 of 39) trace to TARGET text; no post-TARGET identifier from CNA's 11 later commits appears on the site; every Deep Dive page has ≥ 2 in-body inbound links and ≥ 1,391 words; near-duplicate prose paragraphs between pages: 13 benign pairs; the closest Deep-Dive/Development page pair (TF-IDF 0.57, network sessions) is layered by audience and cross-linked; inline-code identifiers of the new pages that do not exist at TARGET are XNA IL names, disclosed sibling-library reads (free-direct `934f72ff`, free-api `53d7a312`) or test-name fragments; 8,767 pinned source links resolve (43 symbol-label "mismatches" were path segments).

### 6.3 Site errata (Phase 3 corrected 76 statements on earlier pages) — independent verification
Rows 1–38 (batch E1) re-derived from TARGET by a reviewer told to refute: **15 CORRECT, 17 INCOMPLETE, 5 NUANCE-LOST, 1 OVERSTATED, 0 WRONG-FIX/OLD-WAS-RIGHT.** Every *original* correction was right; the defect was propagation — the same stale claim survived on sibling pages. Applied: 23 reviewer fixes plus 47 follow-ups found by searching the site (explicit `Present()` in ten tutorials' `Draw`, "before the device exists" for the HiDef request on 13 pages, "first Update is zero" for variable steps, descriptor-relative shader paths on four pages, SpriteEffect status on `effects.html`, Opus on `features.html`, one-named-hole wording). Facts re-checked by the orchestrator at TARGET or in the XNA IL before applying: `SendDataOptions` values (`[Flags]`, ReliableInOrder 3, Chat 4), Curve tangent/loop/segment guards, root-relative effect sidecars, profile propagation in `applyToExistingRenderer`. Rows 39–76 (batch E2): pending.

### 6.4 Dismissed candidates — reverse review (121 candidates the pipeline dismissed)
D1 + D2 (61 of 121): 52 dismissals confirmed; **6 narrow restores** (EasyGL `ClearColorAndStencil` stencil mask, `docs/model-content-pipeline-support.md`, `Matrix::Decompose` vs XNA 4.0, `ExitingEventArgs`, stale `specularEnabled` comments, `NetworkSession` Begin/End), **2 restored verification gaps**, 1 unresolved candidate settled by the orchestrator (CnaTests linked with both `-sJSPI=1` and `-sASYNCIFY=1`: probe with the local emsdk 6.0.9 shows the later flag wins; restored as a low bug, evidence "strong"). The Decompose finding was re-derived independently by porting both algorithms (XNA IL and CNA) to a float32 model; both the IL and the model agree with the reviewer: mirrored → positive scales + norm-0.707 quaternion; shear → `true`. D3, D4: pending.

## 8. Evidence, terminology, count and rendering audits (complete)

* **Evidence vocabulary (Known Issues).** Phase 3 stamped every detail page “tests exist” (`tests_current` is never empty) and used `reproduced` for entries whose text says CNA's own recorded run was used (AF-001, AF-002). Now: an explicit per-entry `tests_present`; the page callout names the basis (source-verified · reproduced · recorded by CNA · inferred); the overview lists the vocabulary. Distribution in §4.1. Entries labelled `reproduced` are those for which something was executed and the Evidence section names it (for example the header-only `Json.hpp` depth probe, `check_no_posix_setenv.py`, the software diff script with `/usr/bin/cp` as the renderer, `test_coverage_scope.py`, the devices-tests filter scan).
* **Strong-claim terms on the new Deep Dive and Development pages** (“verified”, “proven”, “identical”, “byte-exact”, “bit-exact”, “pixel-exact”, “matches XNA”, “all/every renderer”): every occurrence of “matches XNA”, “pixel-exact”, “bit-exact” and “all renderers” (16) was read in context and “byte-exact” (14), “guaranteed” (10) and “proven/proved” (58) were sampled. None asserts a run that was not made: the oracle statements are attributed to CNA's recorded corpus (“recorded pixel-exact on all 39 through Wine and DXVK”, “an empirical match, not a proof”), the XNA-parity statements name the IL or the test they rest on, and the unqualified “byte-exact” of the oracle tier row was corrected by the ch28 review (`direct3d-evidence-and-wine.html#evidence-ladder`).
* **XNA-oracle denominators.** 39 committed scenes / 31 in the last dated report / 46 scene files (39 top-level + 7 null-texture) / 18 of 39 byte-exact for SOFTWARE trace to CNA text at TARGET; no page divides by a different total.
* **Volatile counts.** 25 renderer identities, 21 implementation families, 20 workflows, 61 C API headers, ABI 0.29.0 recomputed from TARGET; the Known Issues totals on every hub, on the overview and in `data/known-issues.json` are generated from one list and checked by `validate_all.sh` (`adversarial_audit.py issues`), so no page carries a typed count that can go stale. A text search for “350”, “218” and “62 functional” finds only entry identifiers.
* **Post-TARGET contamination.** CNA's live checkout is now 12 commits past TARGET (another session committed one more during this audit). Every identifier added after TARGET (703 candidates, 133 absent from the TARGET tree) was searched on the site: none appears (`GpuTimerTests` is a TARGET file name, not a symbol).
* **Rendering leakage (visible markup, double-escaped entities, template braces, temporary ids)** was scanned statically over all 789 public pages and dynamically by the QA harness (new check `MARKUP-LEAK`): AF-013 (36 Known Issues pages), AF-014 (two earlier pages) fixed; the remaining hits are prose about `<div>` elements and XML escaping.
* **Code examples.** The two complete programs in `deep-dives/framework/first-game-walkthrough.html` compile syntax-clean against the TARGET headers (`scripts/check_snippet.sh`, g++ 14, C++23); the other 124 C++ blocks in the Deep Dives and Development pages are fragments without includes, so their identifiers were checked for existence at TARGET instead (only XNA IL names, disclosed sibling-library reads and test-name fragments are absent).

## 9. Preservation, validation and browser QA

* **Protected Phase-1/2 content** is unchanged except where the audit corrected a statement or a rendering defect (errata 77–82): `compare_presentation.py` against `PHASE2_BASE` reports 0 unexplained losses (8 dispositioned, all tied to the retired book sites and the documented `architecture.html` retitle); Homepage Quick Stats, the Showcase, the Speedy Blupi section and its Play in Browser call to action, Development / Human Takeover / Maintainer Handbook, the tutorials and the demos/media are intact.
* **Browser QA** (headless Chrome via CDP, `scripts/browser_qa.py`): 120 pages (all 102 non-Known-Issues pages changed by the audit + 13 Known Issues detail pages, the new entries among them, and the 5 hubs) × {1400 px, 390 px} × {light, dark} = 480 renders: **0 horizontal overflow, 0 broken images, 0 console errors**, the global header on two rows at 1400 px and collapsed at 390 px on every page; 96 flagged renders = 90 × the pre-existing pager label contrast of 4.12 in dark mode (`--text-muted` on the dark background, present in `PHASE2_BASE`; `css/style.css` is unchanged since the audit began) and 8 × the legitimate `<div>` mention. The earlier 64-URL sweep of the Deep Dive, Development and Known Issues areas found the same pre-existing contrast items only.
* **Sibling repositories** were not modified: CNA (untracked `startup-metrics.log` only), Bible (`4df1475c`, 86 paths) and Developer (`9f07046d`, 7 paths) have the same HEAD and status counts as at the start of the audit, except that CNA's HEAD advanced by one commit made by another session.

(Sections 6–9 — Bible conservation review, Known Issues adversarial review, evidence/terminology/count audits, preservation and QA results — are appended as the work is completed.)
