# Phase 3 — completion record (2026-09-26)

Boundary: `PHASE2_BASE` `2c4970c131eac9b69a9bbfb3c30eee080cbc1469` · CNA TARGET / `cnahead` `009d40f5dd085c4e674d3479675fac84b12b3e0a` (exact, one newline) · Bible HEAD `4df1475c00ec241f126bca20b065eb465917adaa` (branch `develop`, 86 modified/untracked paths, **working tree read**;
its own `cnahead` = `d6e9ff05…`, 55 commits before TARGET) · Developer HEAD `9f07046d…` · CNA, Developer and Bible repositories were never written (`git status` counts identical before and after; CNA has only its pre-existing untracked `startup-metrics.log`).
Post-TARGET audit: CNA HEAD `5229c992ebc795b63a2c1d6469a6190ada0e5fb9`, **11** commits after TARGET (7 when the phase started; CNA kept moving), touching renderer, input, platform and graphics-ext paths; none of it was incorporated.
Nothing was pushed. Phase 4 was not started.

## Conservation ledger (`audit/bible-absorption-phase3.md`, `-concepts.md`, `bible-depth-audit-phase3.md`)
* Bible source units audited **119/119**, pending **0**: 98 canonical LaTeX units (front matter, chapters, appendices, nested fragments) + 21 auxiliary evidence/planning documents; plus 20 figure sources and 5 raster images, recorded inside their including chapters (25 records).
* Technical concepts classified **6,019**: NEW PAGE 3,493 · PRESERVED 1,695 · HISTORICAL ONLY 345 · SUPERSEDED 145 · FIXED BUG 121 · EXPANDED 77 · TARGET CONTRADICTED 54 · REMOVED FUNCTIONALITY 43 · DUPLICATE 27 · OBSOLETE 18 · MOVED 1 · **MISSING 0**.
  TARGET verification results: confirmed 4,064 · corrected 1,235 · contradicted 93 · unverifiable-hedged 46 · not-applicable/obsolete/unrecorded 599.
  "Initially missing" was not counted as a separate state (packages fixed gaps before recording); the NEW PAGE + EXPANDED concepts (3,570) are the ones that were absent or too shallow on the trusted site.
* Depth audit: 20 units of ≥ 2,500 Bible words; deep-dive words ≥ 0.8 × Bible words for every one (0 flagged).
* Code examples: 149 recreated (syntax-checked against TARGET headers where practical, otherwise read-checked and labelled), 17 already present, 22 superseded, 7 rejected, 4 not ported, 3 obsolete. Figures: 20 redrawn as captioned text diagrams, 5 Bible screenshots superseded.

## Site growth
HTML pages 308 → 782 (+474: 119 in `deep-dives/` incl. 15 generated hubs, 355 in `known-issues/` incl. 5 hubs). 76 of the 308 existing pages grew ≥ 10 %; 232 are within ±10 %; **0 shrank by more than 10 %**.
Presentation preservation against PHASE2_BASE: 0 unexplained losses (CTAs, images, videos, headings, cards, stats); one note: `architecture.html` "Key C++23 features…" retitled (id kept) as a documented factual correction (also a Phase-1 disposition).
Header: one new global entry ("Deep Dives"); link spacing tightened (font 0.925→0.91 rem, padding 0.37→0.33 rem, cap +100 px) so the header keeps the baseline two rows at 1400 px. Known Issues is linked from the Deep Dives hub, the Documentation hub, the homepage, the verification page and every footer, not from the header.

## Known Issues (`data/known-issues.json`, `known-issues/`)
Candidates reviewed **566**: Bible ledger 62 ids + 4 documentation items, Phase-2 Development findings 222, chapter/auxiliary-package findings 278. Dispositions: STILL EXISTS 430 · PARTIALLY FIXED 15 · PROVEN FIXED 23 · OBSOLETE 5 · NOT A BUG 91 · INSUFFICIENT EVIDENCE 2 (fixed / obsolete / not-a-bug items are **not** published anywhere).
Published after merging cross-package duplicates (40 folded): **350 entries** — 218 bugs · 62 functional gaps · 15 platform limitations · 55 verification gaps; 336 open, 14 narrowed. 31 Bible stable ids survive; 187 further bug ids were allocated above 062 (origin: 134 from Phase-2 candidates, 177 from chapter/auxiliary-package findings, 5 new findings, 3 other, incl. 6 CNA documentation-drift items). Severity: 2 high, 47 medium, 163 low bugs.
Adversarial second review of all 49 high/medium bugs by independent reviewers: 39 confirmed, 10 corrected (text/severity), 0 refuted. The other 301 entries had one verification pass (by reading; 8 bugs carry `reproduced` evidence from focused runs of CNA's own gate/test scripts or tiny probes).
Evidence boundary: nothing was built as a whole; executed items are named per entry.

## Existing-site corrections (`audit/phase3-site-errata.md`)
76 statements on Phase-1/2 pages found wrong at TARGET while absorbing the Bible: 75 fixed, 1 hedged (FAQ: CNA's expansion is not defined in the repository).

## Validation (`scripts/validate_all.sh`, `PHASE3_FINAL=1`): overall PASS
validate_site, validate_presentation, compare_presentation (Phase 1 / Phase 2 / Phase 3), check_facts (0 problems), check_source_links, site_dev, developer_ledger, check_retired_renderers (0), site_deep, check_deep_page --all (0 errors), apply_expansions, backlinks, known_issues validate, bible_ledger --final (119/119, 0 errors, 0 warnings), git diff --check.
Browser QA (headless Chrome): 468 new pages at 1400 dark and 390 light (after CSS fixes: 0 overflow / console / image flags) + 30 protected and representative pages in 1400/390 × dark/light; remaining flags are pre-existing low-contrast labels reproduced identically on the PHASE2_BASE pages.
