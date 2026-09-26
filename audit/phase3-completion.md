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
Published after merging cross-package duplicates (40 folded): **350 entries** — 218 bugs · 62 functional gaps · 15 platform limitations · 55 verification gaps; 336 open, 14 narrowed. 31 Bible stable ids survive; 187 further bug ids were allocated above 062 (origin: 134 from Phase-2 candidates, 177 from chapter/auxiliary-package findings, 5 new findings, 3 other, incl. 6 CNA documentation-drift items). Severity of the 218 bugs (canonical: `data/known-issues.json`): **2 high, 46 medium, 170 low**.
Adversarial second review of the 49 high/medium bugs that existed when the review ran (2 high, 47 medium) by independent reviewers: 39 confirmed, 10 corrected (text and severity; two mediums were downgraded to low), 0 refuted. The later merge added 6 documentation-drift bugs (one medium, five low), which is why the final mix is 2/46/170 rather than 2/47/163 (the figure first reported before the QA corrections and that merge). The other 301 entries had one verification pass (by reading; 9 bugs carry `reproduced` evidence from focused runs of CNA's own gate/test scripts or tiny probes, 8 `strong`, 1 `probable`, 200 verified by reading).
Evidence boundary: nothing was built as a whole; executed items are named per entry.

## Existing-site corrections (`audit/phase3-site-errata.md`)
76 statements on Phase-1/2 pages found wrong at TARGET while absorbing the Bible: 75 fixed, 1 hedged (FAQ: CNA's expansion is not defined in the repository).

## Validation (`scripts/validate_all.sh`, `PHASE3_FINAL=1`): overall PASS
validate_site, validate_presentation, compare_presentation (Phase 1 / Phase 2 / Phase 3), check_facts (0 problems), check_source_links, site_dev, developer_ledger, check_retired_renderers (0), site_deep, check_deep_page --all (0 errors), apply_expansions, backlinks, known_issues validate, bible_ledger --final (119/119, 0 errors, 0 warnings), git diff --check.
Browser QA (headless Chrome): 468 new pages at 1400 dark and 390 light (after CSS fixes: 0 overflow / console / image flags) + 30 protected and representative pages in 1400/390 × dark/light; remaining flags are pre-existing low-contrast labels reproduced identically on the PHASE2_BASE pages.

## Retired book sites (owner decision, 2026-09-26)
`book.libcna.com` and `bible.libcna.com` are being shut down. The sealed alpha.1 PDF (`CNA_Bible.pdf`, 584 pages, 2,602,878 bytes, SHA-256 `f4916143649d3e5e64bf6c4a5e2e0027ef136b8510ba338f58450c33a984870e`, byte-identical to the file served by book.libcna.com) is now kept on this site as
`historical/cna-bible-v0.1.0-alpha.1.pdf` behind a landing page that states it is historical (`historical/index.html`). The homepage hero buttons "Book (PDF)" / "Book (HTML)" were removed; the homepage footer and the network page link only the historical page/PDF, labelled historical.
The eight removed CTAs/cards/headings are recorded as owner-decision dispositions in `audit/data/phase{1,2,3}-dispositions.json` (0 unexplained losses). No other page linked the retired sites.

<!-- post-phase3-correction:begin -->
## Post-Phase-3 adversarial audit correction

The statements above are kept as Phase 3 wrote them. An independent adversarial audit (`audit/phase3-adversarial-audit.md`, TARGET `009d40f5`) re-read the result and corrected the following. The audit's generated numbers (§4.1 there) are authoritative; this table is the delta.

| Statement above | After the audit |
|---|---|
| 119/119 source units audited; 98 canonical + 21 auxiliary; 20 figures and 5 images recorded inside their chapters; MISSING 0 | Unchanged in structure. Every one of the 98 canonical units and 21 auxiliary documents now also has an *independent* review status (98: PASS 17 · PASS WITH FIXES 81; 21: PASS 8 · PASS WITH FIXES 13; none FAIL), and all 20 figures were compared with their redrawn diagrams. 254 findings were fixed on the site or in the ledger (one is an owner decision, three restored Known Issues). "MISSING 0" holds; 30 concepts the ledger had not recorded were added. |
| 6,019 concepts; NEW PAGE 3,493 · HISTORICAL ONLY 345 · SUPERSEDED 145 · FIXED BUG 121 · TARGET CONTRADICTED 54 · OBSOLETE 18 (others unchanged) | **6,049** concepts; NEW PAGE **3,530** · HISTORICAL ONLY **342** · SUPERSEDED **144** · FIXED BUG **120** · TARGET CONTRADICTED **53** · OBSOLETE **17**; eight dispositions that dropped knowledge were reversed to NEW PAGE. |
| TARGET results: confirmed 4,064 · corrected 1,235 · contradicted 93 · unverifiable-hedged 46 | confirmed **4,081** · corrected **1,251** · contradicted 93 · unverifiable-hedged 46 (1,118 recorded corrections were re-derived from source; 29 disagreed and were repaired). |
| Site growth: 308 → 782 pages (355 in `known-issues/`) | 803 pages in all; `known-issues/` has 375 (370 entries and 5 hubs). |
| **350** Known Issues: 218 bugs · 62 functional gaps · 15 platform limitations · 55 verification gaps; 336 open · 14 narrowed | **370**: 232 bugs · 70 functional gaps · 12 platform limitations · 56 verification gaps; 353 open · 17 narrowed (3 retired as not a bug, 8 folded, 8 reclassified, 31 added). |
| Severity of the 218 bugs: 2 high · 46 medium · 170 low | **2 high · 47 medium · 183 low** of 232 bugs (three medium bugs lowered, one low bug raised, five new medium bugs). |
| "Every page carries the `tests exist` label"; 9 bugs `reproduced`, 8 `strong`, 1 `probable`, 200 by reading (as reported there) | The label was false for 39 surviving entries; every entry now carries an explicit test flag (**325 of 370** touch a test). Evidence basis: verified-by-reading 325 · **reproduced 17** (ten after an executed probe; three former `reproduced` became recorded-by-CNA) · recorded-by-cna 13 · strong 13 · probable 2. |
| "Adversarial second review of the 49 high/medium bugs: 39 confirmed, 10 corrected, 0 refuted" | Stands as recorded. The audit re-read all 350 entries (344 individually, 6 folded duplicates) with the brief to refute: CONFIRMED 224 · CORRECTED 95 · NARROWED 12 · RECLASSIFIED 8 · DUPLICATE 2 · NOT A BUG 3. Both HIGH bugs (CNA-BUG-001, -137) were reproduced by execution. |
| Candidates reviewed **566** … NOT A BUG 91 · PROVEN FIXED 23 | The 121 dismissed candidates were re-read by reviewers told to prove the dismissal wrong: 105 confirmed, 16 restored or already published. The 62 Bible bug ids now reconcile as 32 bugs + 2 gaps + 2 verification gaps (36 survive), 16 proven fixed, 4 obsolete, 6 not a bug. |
| "76 statements on Phase-1/2 pages found wrong: 75 fixed, 1 hedged" | All 76 were independently re-verified: 36 CORRECT, 28 INCOMPLETE (the same stale claim survived on sibling pages), 10 NUANCE-LOST, 2 OVERSTATED; every gap was closed, and 6 further statements were corrected (errata rows 77–82) plus the auxiliary-review corrections. |
| Browser QA: 468 new pages at 1400 dark and 390 light; remaining flags "pre-existing low-contrast labels" | Final QA: 352 pages × 2 widths × 2 schemes = 1,408 renders, 0 overflow, 0 broken images, 0 console errors. Flags remain and are reported: dark-mode pager label contrast 4.12 (116), Prism's green CMake token 2.68 in code blocks (24), and 24 legitimate prose mentions of `<div>` and escaped entities. Both contrast items are identical on the `PHASE2_BASE` pages. |
<!-- post-phase3-correction:end -->
