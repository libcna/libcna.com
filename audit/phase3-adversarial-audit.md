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

## 5. Findings (append-only; status is updated in place)

| ID | Area | Finding | Status |
|---|---|---|---|
| AF-001 | Known Issues pages | The generator (`scripts/known_issues.py page_fragment`) marks **every** page `test-present` because `tests_current` is never empty; 105 entries' own `tests_current` text says "None"/"No test…". The page callout renders “tests exist (not executed for this page)” next to a text that says none exist. | open |
| AF-002 | Known Issues evidence | `confidence: reproduced` is applied to entries whose text says CNA's *own* recorded run was used and "not executed for this entry" (CNA-BUG-099, -175, -203). | open |
| AF-003 | Known Issues duplicates | Mechanical pre-pass: CNA-BUG-215 / -219 / -226 (same `IsLatched()` defect, identical sources), -185 / -188, and several weaker pairs. | open |
| AF-004 | Ledger precision | 93 of 5,494 ledger concepts (1.7 %) cite a destination *anchor* whose section does not contain the concept's own tokens (they are elsewhere on the same page). Page-level: 0 misses. | open |
| AF-005 | Source graph | `NEXT-ARCHIVE-2026-07-26.md`, `PLAN-ARCHIVE-2026-07-26.md` never dispositioned. | open |

(Sections 6–9 — Bible conservation review, Known Issues adversarial review, evidence/terminology/count audits, preservation and QA results — are appended as the work is completed.)
