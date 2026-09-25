# Phase-3 guide for the auxiliary Bible documents (residue scan) — packages WPB1…WPB7

Read `audit/data/phase3-editorial-guide.md` §1–§10 first (boundaries, dispositions, record schema, lean rules; the "issues" and "figures" parts of §6 apply as written). This file only changes the *method*.

## What these units are
The `aux-*` units are the Bible's research and planning documents (`bible.libcna.com/audit/*.md`, `AUDIT.md`, `EDITORIAL-AUDIT.md`, `PLAN.md`, `NEXT.md`, `PROGRESS.md`, `README.md`, `CLAUDE.md`). The manuscript chapters — already absorbed into libcna.com by the chapter packages — were written *from* the subsystem audits, so most of their current content is already on the site (`deep-dives/**`, `docs/**`, `development/**`). The job is a **residue scan**: find what is still current at TARGET, useful, and *not yet* on the site — and record everything else with an honest disposition. The units' headings are the `##` sections in `units.json` (`aux-cnabugs` is NOT yours; the Known Issues pipeline records it).

## Method (per unit)
1. Read the unit once (large files: read section by section with `sed -n`; do not re-read).
2. For each `##` heading extract its distinct claims (identifiers, numbers, file:line evidence, test names, measured results with their hosts, "why" reasoning). Aim for **6–12 concepts per 10 KB of source** — one per claim *cluster* that would be a separate fact on a page, not one per sentence. Every `##` heading needs a concept or an `empty_sections` entry.
3. Decide each concept with `python3 scripts/site_grep.py <identifier|phrase>` (site-wide; `--area deep-dives|docs|development`), reading the hit's context:
   * already on the site at sufficient depth → `PRESERVED` / `DUPLICATE` (destination page#anchor + `tokens`; `target.result: "confirmed"` with evidence "already stated on <page>, which was checked at TARGET" is acceptable *only after you skimmed that page's statement and it matches what you know of TARGET*);
   * current, useful, absent → verify at TARGET (source/tests, `git show 009d40f5…:path`; the Bible pin d6e9ff05 is 55 commits older; alpha.1-era text is often stale) then publish: a short **expansion** onto an existing page (`docs/**`, `development/**` or `deep-dives/**`; ≤ ~400 words; guide §5.4) or, when a group of residue concepts forms a coherent topic (>400 words), a new page in the matching deep-dive group (declare it in `audit/data/deep-pages/<WPB>.json`, `order` base `9000 + 10·k`). Disposition `EXPANDED` / `NEW PAGE`;
   * stale, alpha.1-only, retired renderers, process/methodology of the book, campaign chronology → `HISTORICAL ONLY` / `OBSOLETE` / `REMOVED FUNCTIONALITY` / `TARGET CONTRADICTED` / `FIXED BUG` with a note carrying the evidence (never name a retired renderer identity, guide §4).
4. Record issue candidates you meet that are *not already* in `audit/data/bible/issues/candidates-B*.json`, `verified-B*.json` or `WP*.json` (grep by identifier first) in `audit/data/bible/issues/<WPB>.json` (guide §7).
5. Write one record per unit (`audit/data/bible/records/<unit-id>.json`, e.g. `aux-audit-graphics-core-effects.json`), validate `bible_ledger.py check --units <ids>` → 0 errors.

Budget: the residue is expected to be small. Do not read sources beyond what a residue concept needs; do not spawn helpers; report ≤ 200 words (units, concept counts by disposition, pages/expansions added, notable finds, site errors noticed with page#anchor + evidence).
