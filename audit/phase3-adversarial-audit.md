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
| Published entries | **356** = 219 bugs · 66 functional gaps · 14 platform limitations · 57 verification gaps |
| Bug severity | **2 high · 46 medium · 171 low** |
| Status | 340 open · 16 narrowed |
| Evidence basis | probable 2 · recorded-by-cna 4 · reproduced 7 · strong 8 · verified-by-reading 335 |
| Entries with a test touching the area | 311 of 356 |
| Subsystems | Graphics & renderers 66 · Testing & evidence 45 · Documentation & release tooling 43 · Networking & gamer services 27 · Math & geometry 25 · Build & CI 25 · Core & runtime 21 · Audio & media 20 · Platforms 19 · Content & XNB/CNB/CNJ 16 · Models & glTF 14 · Storage 10 · Input 9 · Diagnostics & Inspector 9 · C API & bindings 7 |
| Audit operations recorded in `dispositions.json` | folded 2 · retired 2 · reclassified 6 · added 10 |
| Independent issue reviews ingested | 143 of 356 entries; CONFIRMED 105, CORRECTED 27, NARROWED 3, NOT A BUG 2, RECLASSIFIED 6 |
| Independent dismissal reviews ingested | 30 of 121; DISMISSAL CONFIRMED 25, NARROW-RESTORE 2, RESTORE-VERIFICATION-GAP 2, UNRESOLVED 1 |

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

## 6. Progress log (updated at each checkpoint; the final sections replace this one)

### 6.1 Known Issues — independent re-review (reviewers told to refute; verdicts stored in `audit/data/adversarial/issue-reviews/`)
Batches by subsystem; a verdict is a *proposal*: `audit_issue_review.py plan` applies text corrections and evidence flags automatically and lists severity changes, reclassifications, duplicates and retirements as *pending* until `decisions.json` adjudicates them.

| Batch | Scope | Reviewed | Confirmed | Corrected | Reclassified | Removed |
|---|---|---:|---:|---:|---:|---:|
| R10 | Math & geometry | 23 | 18 | 5 | 0 | 0 |
| R14 | Content & Models | 30 | 26 | 3 | 1 (CNA-BUG-127 → functional gap) | 0 |
| R01 | Graphics & renderers, part 1 (16 low + 5 high/medium bugs) | 21 | 12 | 6 (+1 narrowed) | 2 (CNA-BUG-100, -108 → functional gaps) | 0 |

Independently re-verified by the orchestrator (not delegated): **both HIGH bugs** — CNA-BUG-001 (aliased `Matrix::Transpose` in `Plane::Transform`) and CNA-BUG-137 (`MediaPlayer::Play(Song*)` clears the queue that owns the song before copying it) — confirmed by reading; CNA-BUG-121 (spot check of a contestable medium; reviewer right); two reviewer *corrections* (CNA-GAP-034 `DateTime(ticks, kind)` exists in sharp-runtime; CNA-GAP-036 `gltf_to_cnj` takes a positional `unitScale`) — both true.
Re-executed by the orchestrator: CNA-BUG-062 (`generate_coverage_inventory.py --check` and `generate_limitations.py --check` exit 2, naming `modules/design|diagnostics|inspector/include`), CNA-BUG-200 (`check_no_posix_setenv.py` exit 1, twelve lines), CNA-BUG-016 (header-only `Json.hpp` probe: 1,000 and 10,000 levels parse; 50,000 and 100,000 levels SIGSEGV with the default 8 MiB stack, g++ 14.2 -O0 and -O2; probe removed from `build-probe/`).

### 6.2 Independent recomputations that agreed with Phase 3
Bible graph (118 book files); 350 = 218 + 62 + 15 + 55 entries and 2/46/170 severities; 350 pages = 350 entries, 0 orphans; sitemap and search 781 = every page except `404.html`/`search.html`; 62 Bible bug ids = 31 survive + 3 reclassified to gap/verification gap + 16 proven fixed + 5 obsolete + 7 not a bug; 566 candidates = 566 dispositions, 345 published entries with origins + 5 new findings; presentation against `PHASE2_BASE` (all 308 pages: only the 5 hrefs and 3 headings tied to the retired book sites and the documented `architecture.html` retitle are gone; 0 lost images/videos/ids, 0 shrunk pages); Deep Dives hub page counts (14 groups, 104 pages); volatile facts recomputed from TARGET (25 renderer identities, 20 workflows, 39 top-level oracle scenes + 7 null-texture = 46 files, 61 C API headers, ABI 0.29.0, SOFTWARE "10 → 18 of 39 byte-exact"); oracle scene denominators on the site (39 / 31 / 46 / 7 / 18 of 39 / 10 of 39) trace to TARGET text; no post-TARGET identifier from CNA's 11 later commits appears on the site; every Deep Dive page has ≥ 2 in-body inbound links and ≥ 1,391 words; near-duplicate prose paragraphs between pages: 13 benign pairs; the closest Deep-Dive/Development page pair (TF-IDF 0.57, network sessions) is layered by audience and cross-linked; inline-code identifiers of the new pages that do not exist at TARGET are XNA IL names, disclosed sibling-library reads (free-direct `934f72ff`, free-api `53d7a312`) or test-name fragments; 8,767 pinned source links resolve (43 symbol-label "mismatches" were path segments).

(Sections 6–9 — Bible conservation review, Known Issues adversarial review, evidence/terminology/count audits, preservation and QA results — are appended as the work is completed.)
