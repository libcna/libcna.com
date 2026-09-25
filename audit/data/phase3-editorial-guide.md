# Phase-3 editorial guide — absorbing the CNA Bible into libcna.com

Authoritative for every agent working on Phase 3. Read it completely. It builds on, and does not repeal, the Phase-1 guide
(`audit/data/facts/00-editorial-guide.md` §2–§5: snapshot framing, canonical numbers, retired-renderer rule, truthfulness rules) and the
Phase-2 guide (`audit/data/phase2-editorial-guide.md` §3–§5: verification method, quality bar, fragment format). Where they disagree, this one wins.

## 0. The job in one paragraph

libcna.com (Phases 1+2, accepted, 308 pages) documents CNA snapshot **`009d40f5dd085c4e674d3479675fac84b12b3e0a`** (TARGET). The **CNA Bible**
(`/rv/data/development/github.com/libcna/bible.libcna.com`, a LaTeX book, read-only) is a deep reservoir of technical knowledge written against an
**older** CNA commit (`d6e9ff05…`, 55 commits before TARGET) — and many of its chapters are *older still* (alpha.1 text that was never re-synchronised).
Your job: for every Bible source unit assigned to you, **absorb all useful CURRENT knowledge into libcna.com without losing, weakening or
contradicting the trusted pages that already exist**, after re-verifying each claim against TARGET.

```
Bible unit  ->  candidate concepts  ->  verify at TARGET  ->  compare with what libcna.com already says  ->  disposition
                                                                    PRESERVED / EXPANDED / ... / NEW PAGE / MISSING->fix
```

The Bible is **not** an authority. Where it disagrees with TARGET, TARGET wins; write the TARGET-correct statement (or nothing). The site is a
**knowledge graph, not a converted book**: never mirror the book's chapter shape, never write "Chapter 12", never say "the Bible".

Default operation: `trusted page + unique current Bible knowledge = deeper trusted page`, or `unique deep topic -> new page`. Never `trusted page -> replaced`.
Scale is not a constraint: if conservation needs many pages, write many pages. Page count is not a target either: no shallow pages, no padding.

## 1. Hard boundaries

* **Read-only sources:** the Bible working tree (`/rv/data/development/github.com/libcna/bible.libcna.com` — **the working tree, including uncommitted and
  untracked files**, not Git HEAD, not `docs/` HTML, not the PDF); the CNA repository (`/rv/data/development/github.com/libcna/cna`, Git objects only:
  never check out, reset, clean, fetch, build or write there — its HEAD is *past* TARGET, ignore it); the extracted TARGET tree
  **`/rv/tmp/libcna-v2/cna-target`** (`third_party/` and `vendor/` are not extracted: use `git -C /rv/data/development/github.com/libcna/cna show 009d40f5dd085c4e674d3479675fac84b12b3e0a:<path>`).
* **Never document post-TARGET facts.** Never `git grep` without naming the TARGET revision. `git -C …/cna diff d6e9ff05 009d40f5 -- <path>` shows
  what changed after the Bible's pin (`d6e9ff05`); a changed path is a **mandatory re-verification target**, and an *unchanged* path only proves the file is
  identical — the Bible's claim about it may still have been wrong or alpha.1-stale.
* **Do not read or use:** the archived failed first "unified documentation" attempt, other libcna.com branches/worktrees, `developer.libcna.com`
  (Phase 2 already absorbed it; use the *libcna.com* Development pages instead).
* **No builds** (no cmake/make/compiler runs except `g++ -fsyntax-only` on a snippet whose include set works without generated headers), **nothing under `/tmp`
  except the scratchpad given in your brief, no `git add/commit/push/stash/reset`.** Rule 3 of the repository build rules applies to you.
* **Write only** the files named in §2 for your work package. Do not edit any other repository file: not protected pages, not the CSS, not another package's
  page, not scripts (if you believe a script or another page needs a change, say so in your report).
* Voice: neutral third person, present tense for TARGET facts. Never "I verified"; write "checked by reading … at 009d40f5; not executed". No references to "the book",
  "the Bible", "chapter N", "this edition", "the audit", the Bible's file names or its pin `d6e9ff05`, "Developer", "Phase N".

## 2. Your inputs, outputs and tools

Your brief names: your **work package id** (`WPnn`), your **Bible units** (ids from `audit/data/bible/units.json`), the **auxiliary audit files** to mine,
the **deep-dive groups/paths** you may use, your **concept-id prefix**, and your **scratchpad directory** `S` (fragments live under `S/deep-src/`).

| Path | Who writes it | What |
|---|---|---|
| `audit/data/bible/records/<unit-id>.json` | you (your units only) | the ledger record, §6 |
| `audit/data/deep-pages/WPnn.json` | you | `{"pages":[{path,title,label,group,order,bible_units}]}` for the new pages you author |
| `S/deep-src/<page path minus .html>.body.html` + `.meta.json` | you | page fragments, §5 (built into `deep-dives/**` by the generator) |
| `audit/data/bible/expansions/WPnn/<key>.json` + `.html` | you | additive expansions of *existing* `docs/**` / `development/**` pages, §5.4 |
| `audit/data/bible/issues/WPnn.json` | you | bug / gap / limitation candidates you found, §7 (**not** published by you) |

```bash
cd /rv/data/development/github.com/libcna/libcna.com
python3 scripts/bible_inventory.py --list                          # the unit list (already generated: audit/data/bible/units.json)
python3 scripts/site_grep.py TOKEN [TOKEN..]                       # where does the site already say this? (page + nearest anchor); --context 200 to read it
python3 scripts/site_grep.py --page development/internals/runtime/frame.html --context 250 TOKEN
python3 scripts/site_deep.py build --src S/deep-src <page>...      # write pages from fragments (needs your audit/data/deep-pages/WPnn.json first)
python3 scripts/check_deep_page.py <page>...                       # per-page validator: must print "ok"
python3 scripts/apply_expansions.py apply --only <key>...          # insert your expansions into the target pages
python3 scripts/bible_ledger.py check --units <unit-id>...         # validate your records: must print 0 errors for your units
python3 scripts/check_retired_renderers.py                         # whole-site retired-renderer scan
git -C /rv/data/development/github.com/libcna/cna diff d6e9ff05 009d40f5 -- <path>
```

Do **not** run `site_deep.py sync|hubs`, `bible_ledger.py render`, `build_site_indexes.py` or `patch_global_nav.py`: the orchestrator runs them once per wave (they touch every
page and would race with other agents).

## 3. Method for each Bible unit

1. **Read the whole unit** (the .tex file, and the figure files it `\input`s). Read `units.json` for its heading list — **every heading must end up accounted for** (§6).
   Note `git_state`: `clean` means alpha.1-era text that the `d6e9ff05` synchronisation never touched (expect stale facts: 50 renderer identities, ABI 0.7.0, 14 capabilities,
   "no X exists" statements later falsified, …); `M`/`??` means updated for `d6e9ff05`, which is itself older than TARGET. Also read the matching subsystem audit(s) in
   `bible.libcna.com/audit/*.md`, `NEXT.md`/`PLAN.md`/`AUDIT.md` passages that touch your units (they explain *why* claims were made and contain evidence the chapters compress).
2. **Extract concepts** — one concept per distinct technical statement cluster (a rule, semantic, invariant, algorithm, format, lifecycle step, ownership rule, compatibility nuance,
   platform difference, limitation, worked example, test strategy, evidence caveat, maintainer implication). A paragraph usually holds 1–3; a table holds one per row-group. Dense
   chapters have dozens. **A 5,000-word chapter recorded as 8 concepts is under-extracted and will be rejected by the ledger checker** (< 6 concepts per 1,000 Bible words warns).
   Conceptual richness beats count, but do not skip: quirks, edge cases and "why" sentences are exactly what the site lacks.
3. **Verify each concept at TARGET** by reading source, headers, CMake, tests (not only grep hits). Result per concept: `confirmed` | `corrected` (TARGET differs; you write the TARGET-correct
   statement) | `contradicted` (Bible claim is false at TARGET; do not copy) | `obsolete` (subject gone) | `not-applicable` (methodology/framing with no TARGET fact) | `unverifiable-hedged`
   (cannot be established by reading; keep hedged or drop). Record the evidence as `path (function/symbol)`.
4. **Find what libcna.com already says** with `site_grep.py` on the identifiers and distinctive phrases of each concept, then **read the hit** (a page that merely mentions a token is not
   coverage). Decide the disposition (§4). If the site already says it *and* says it at least as well → PRESERVED/DUPLICATE/EXPANDED. If the site says it thinly or not at all →
   MISSING now, and **you fix it before you finish** (new page or expansion), after which the record says NEW PAGE / EXPANDED / MOVED.
5. **Write** the pages/expansions (§5), then finish the record, build, run all checks, iterate until clean.

Work in this order to avoid late surprises: read → concept list with dispositions → pages → record → checks. Persist the record early (partial JSON with `"done": false` is fine) so a
compaction cannot lose your state.

## 4. Dispositions (per concept) — exact meanings

| Disposition | Meaning | Needs |
|---|---|---|
| `PRESERVED` | libcna.com already contains sufficient current depth for this concept (the substance, not a passing mention) | destination page[#anchor], `tokens` present in it |
| `SUPERSEDED` | libcna.com has a *different but stronger* explanation | destination, tokens, one-line why in `note` |
| `EXPANDED` | you added the Bible's unique substance to an existing page (expansion) or the existing page is already deeper | destination (the expanded page), tokens |
| `MOVED` | the knowledge belongs in a different conceptual home than the Bible gave it and is now there | destination, tokens |
| `NEW PAGE` | unique useful current material that got its own deep-dive page (or a new section of one) | destination, tokens |
| `DUPLICATE` | the substance is genuinely present elsewhere on the site (name where) | destination, tokens |
| `OBSOLETE` | subject no longer relevant to current CNA | `note` (≥20 chars: why, with evidence) |
| `HISTORICAL ONLY` | interesting history, not useful as current technical documentation (release chronology, superseded status, book narrative) | `note` |
| `FIXED BUG` | a former defect that no longer exists at TARGET — **never published as a current bug** | `note` with the positive evidence |
| `REMOVED FUNCTIONALITY` | the described functionality no longer exists at TARGET (e.g. a retired renderer's behaviour) | `note` |
| `TARGET CONTRADICTED` | the Bible states something false at TARGET; not copied | `note`, `target.result` = contradicted/corrected + evidence |
| `MISSING` | useful current knowledge absent or materially too shallow — **a work-in-progress state only; must be 0 when you finish** | `note` |

`tokens` = the exact identifiers/phrases (case-sensitive) that must appear in the destination page text; the checker greps them. They stop "vaguely related page" false DONEs. Pick tokens
that carry the concept (a symbol name, an option name, a distinctive phrase), 1–4 per concept. `no_tokens_reason` is allowed only for genuinely non-lexical concepts (a framing idea).

**Evidence is part of the knowledge.** Do not strip why-a-claim-is-believed: which test, which oracle, which host, what remains uncertain. Keep the vocabulary strict and unmixed:
*source exists / configures / builds / links / unit tested / integration tested / runtime observed / visual compared / real hardware observed / XNA oracle compared*. You did not run tests
or builds: say "not executed" where the distinction matters.

**XNA compatibility needs nuance:** representation (a type/member exists — 331/331 types, 3,627/3,627 members) ≠ strict member representation ≠ exact behaviour ≠ semantic behaviour ≠ host
substitution ≠ native/unsupported boundary ≠ oracle-compared ≠ tested. Never write a single compatibility percentage; never let representation coverage read as behavioural parity.

**Retired renderers (hard rule).** TARGET has 25 public renderer identities over 21 families (`cmake/RendererIdentities.cmake`). The Bible's older chapters describe a much larger set. **Never write a
retired identity, alias, module name or a dependency used only by a retired renderer** on any page or expansion — not even "removed: X" — and do **not** list them in ledger text either
(refer to "a retired renderer family (Bible ch.NN §…)"). Historical prose may say generically that an earlier release had a broader renderer surface curated down to 25. Concepts whose
subject is a retired renderer are `REMOVED FUNCTIONALITY` or `HISTORICAL ONLY`; the **generic lesson** they teach that still applies to a current renderer is a separate concept that
you keep (re-homed on the current renderer). Old spellings that are old names of *current* identities (`D3D9`→`DIRECTX9`, `DX3`→`FREEDIRECT`, `CNA_GRAPHICS_BACKEND`→`CNA_GRAPHICS_RENDERER`,
`EASYGL`→five GL profiles) may appear in "names that changed" tables. To learn the retired set for scrubbing only:
`python3 -c "import sys;sys.path.insert(0,'scripts');import check_retired_renderers as R;from pathlib import Path;print(sorted(R.derive(Path('/rv/tmp/libcna-v2/cna-base'),Path('/rv/tmp/libcna-v2/cna-target'))))"`.

**Bugs are not history.** If the Bible records a defect: do **not** publish it and do **not** call it fixed on a hunch. Record it as an *issue candidate* (§7) with your TARGET reading; the
Known Issues pipeline verifies it with positive evidence. Only defects that exist at TARGET ever appear publicly, and only through Known Issues. A pedagogical *worked case study* of
a fixed defect is legitimate teaching if the page says it is historical and what current code does.

## 5. Writing pages

### 5.1 Where things go (do not mirror chapters)

Each page is one CNA **concept** or one user task. One Bible chapter may feed many pages; one page may absorb several chapters. Choose the group by subject
(`foundations, framework, build, graphics, renderers, content, models, services, sharp-runtime, siblings, platforms, verification, practice, reference`;
your brief lists the ones you may use). Path: `deep-dives/<group>/<kebab-slug>.html`. Before creating a page, check with `site_grep.py` and the manifest
(`python3 scripts/deep_manifest.py --list`) that no page already covers the concept; if one does, extend by an *expansion* or add a section to **your own** page instead of a parallel page.
A page should be substantial (typically 700–3,000 words); a 150-word page is a paragraph that belongs in a bigger page. Do not split one continuous explanation into fragments to raise page count.

What a deep dive contains (and a guide/internals page does not): exact semantics (return values, ordering, edge cases, ownership, lifetime, thread/loop affinity), invariants and *why*
(including "matches XNA/FNA on purpose" rationale), platform/renderer qualifications, worked examples with real symbols, failure modes, the evidence behind the claims and what is not
proven, and where the behaviour is owned in source (source links). Keep the Bible's own worked reasoning and counter-examples — they are the value.

### 5.2 Fragment format (same as Phase 2, plus the deep-dive `layers`)

`S/deep-src/<path minus .html>.body.html` — inside of the article, **no `<h1>`**, no TOC/evidence box/related block/breadcrumb/sidebar/pager (generated). Start with `<p class="lede">…</p>`
(2–4 sentences: what the page explains and who needs it), then `<h2 id="kebab">` sections with `<h3 id>` inside. Every h2/h3 needs an id; heading levels never skip.

* Links to CNA source **only via tokens** (validated against TARGET at build time): `{{src:modules/runtime/src/Game.cpp}}`, `{{src:modules/runtime/src/Game.cpp|Game.cpp}}`,
  `{{tree:modules/platform/src|platform sources}}`. No line anchors (they rot; name the function). Every source path you mention in prose should be a token link on first use per section.
* Links to other site pages **only via** `{{page:development/internals/runtime/startup.html|label}}` / `{{page:docs/platforms.html#sdl3|label}}` (any manifest page — including the deep-dive
  pages of other work packages, which may not exist yet — is a valid target; verify a fragment you link exists on an already-built page). Never hard-code relative hrefs.
* Elements: `<div class="callout callout--info|warn|note"><span class="callout-icon">&#8505;</span><p>…</p></div>`; tables `<table><thead><tr><th scope="col">…</th></tr></thead><tbody>…</tbody></table>`
  (do not wrap; the generator does); code `<pre><code class="language-cpp|bash|cmake|json|glsl">…</code></pre>` (escape `<` and `&`); lists; `<ol class="source-list">`.
  No inline styles, scripts, raw `<img>` (see 5.3), custom classes. No `{{…}}` inside `<code>`.
* Meta `S/deep-src/<path minus .html>.meta.json`: `title` (a subject, never "Chapter …"), `description` (one sentence ≤ 220 chars), `keywords` (6–12 lowercase), `evidence`
  `{"levels": ["source-verified", "test-present", …], "note": "what remains unproven"}` (levels ⊆ source-verified, test-present, build-verified, runtime-observed, oracle-compared, hardware-observed;
  use the last four only when TARGET's own records say so and you attribute them to CNA), and `layers` — real links, each verified to exist:
  `guide` (a Phase-1 `docs/…` page), `architecture`/`internals`/`maintainer`/`tests`/`reference` (Development pages), `deep` (other deep-dive pages), `issues` (Known Issues pages, if any).
  A deep dive **must** link at least its user guide and its Development architecture/internals neighbour; that is what keeps it from being an orphan. Link the *tutorial(s)* teaching the same
  task in the body where natural (the tutorials are in `docs/tutorials/NNN-*.html`; use `site_grep.py --area tutorials`).
* Declare the page in `audit/data/deep-pages/WPnn.json` **before** building.

### 5.3 Figures and diagrams

Audit every Bible figure in your units (`\input{figures/fig-*.tex}` and the PNG screenshots). For each: PRESERVED (its semantic content is already in a current diagram), RECREATED (you drew it
anew, corrected to TARGET), SUPERSEDED, OBSOLETE (stale topology/old counts/removed renderers), MISSING. Recreate useful current diagrams as **reviewable text**:

```html
<figure class="diagram-figure" role="group" aria-labelledby="fig-frame-cap">
<pre class="diagram">…box-and-arrow text, ≤ 90 columns, no <code> inside…</pre>
<figcaption id="fig-frame-cap"><strong>Figure.</strong> A complete sentence-level description of what the diagram shows (the text alternative): nodes, direction, what to notice.</figcaption>
</figure>
```

Never import a stale topology (old module graphs, old renderer counts, retired platforms). Real screenshots in the Bible (five PNGs) are evidence for *their own* older revision: describe them as
such or leave them (disposition SUPERSEDED/OBSOLETE with a note); never present them as TARGET screenshots and never fabricate images.

### 5.4 Expansions of existing pages

For small additions that clearly belong on an existing `docs/**` or `development/**` page (a corrected sentence, a missing caveat, a compat nuance, an extra table row-group of ≤ ~400 words),
write an expansion instead of a new page: `audit/data/bible/expansions/WPnn/<key>.html` (fragment: `<h2 id>`/`<h3 id>` sections, same tokens) + `<key>.json`
`{"target": "docs/game-loop.html", "mode": "append|before_id|after_id", "id": "<existing heading id>", "note": "why here"}`, then `python3 scripts/apply_expansions.py apply --only <key>`.
Additive only: never remove or reword existing text; ids must be new on the target. **Protected root pages** (`index, demos, showcase, videos, features, about, documentation, tutorials,
architecture, roadmap, network, contact`) and all of `docs/tutorials/` may not be targeted — the orchestrator adds links there. Prefer a new deep-dive page when the addition exceeds ~400 words or is a
self-contained concept; the orchestrator adds automatic "Deep dives on this topic" backlink blocks to the pages named in each deep page's `layers.guide|architecture|internals|maintainer`.

### 5.5 Code examples

For each useful example in the Bible: verify symbols against TARGET public headers (`modules/*/include`), include paths, CMake option names, file paths, call style (the real style is
`getContentProperty().Load<T>("name")` returning by value). Syntax-check with `g++ -std=c++23 -fsyntax-only -I…` **only** when the include set works without generated headers; otherwise
read-check and say so in the record (`"verified": "read-checked"`). Record every example: PRESERVED (already on the site), RECREATED (verified and re-hosted), REJECTED (stale/not compiling — say why),
NOT PORTED (illustrative pseudocode without value). Label illustrative pseudocode as such on the page.

### 5.6 Quality bar

* Concrete CNA content only: source paths, types, functions, registries, options, tests, invariants, call flow, ownership, failure modes. No generic advice, filler or promotional prose.
* Do not summarise a detailed explanation into "CNA handles this internally". Detail may *move*; it must not disappear. A destination that carries a 5,000-word chapter's substance in 500 words is
  a red flag: write the depth, do not pad.
* Do not make claims stronger than TARGET evidence. Use TARGET's canonical numbers (`data/current-facts.json`); never copy a Bible count (50 renderer identities, ABI 0.7.0, 14 capabilities, 568 tests…).
* `alpha.1` appears only as historical context. Never write "alpha.2", "0.2", "beta".
* Never document what a *sibling repository* does at its current HEAD as TARGET behaviour; pin `repo @ sha` and attribute (sharp-runtime, EasyGL, MetaGL, FreeDirect, FreeAPI, samples, bindings are
  evidence for their own revisions).
* Do not import fixed bugs, retired renderers, or stale "known limitations" as current.

## 6. The ledger record — `audit/data/bible/records/<unit-id>.json`

One file per Bible unit (`ch06-game-lifecycle`, `front-…`, `appendix-…`, `fragment`s, and `aux-…` documents). Figure units and PNG assets are recorded inside the record of the chapter that includes
them (`figures[]`, key `unit` = `fig-…` or `asset:<id>`; the including chapter is in `units.json` → `included_by` / `assets[].included_by`).

```json
{
  "unit": "ch06-game-lifecycle",
  "author": "WP03",
  "done": true,
  "target_relevance": "current | partly-stale | stale | historical",
  "actions": ["MERGE", "EXPAND", "NEW PAGE", "DEEP DIVE", "TESTING/EVIDENCE"],
  "summary": "2–4 sentences: what the unit teaches, how stale it is against TARGET, what libcna.com already had and what it lacked.",
  "sections": [ {"heading": "The override points", "note": "optional free text"} ],
  "empty_sections": [ {"heading": "Chapter introduction", "reason": "pure signposting; no technical claim"} ],
  "concepts": [
    {"id": "WP03-ch06-001",
     "section": "The override points",
     "text": "BeginDraw() returning false skips both Draw and EndDraw for that frame; GraphicsDeviceManager uses this to suppress rendering while no device exists.",
     "kind": "semantics",
     "disposition": "PRESERVED",
     "destinations": ["development/internals/runtime/frame.html#sequence"],
     "tokens": ["BeginDraw", "EndDraw"],
     "target": {"result": "confirmed", "evidence": "modules/runtime/src/Game.cpp (Game::Tick); modules/graphics/src/GraphicsDeviceManager.cpp (BeginDraw)"},
     "note": ""}
  ],
  "figures":  [ {"unit": "fig-game-lifecycle", "disposition": "RECREATED", "destinations": ["deep-dives/framework/game-lifecycle.html#fig-lifecycle"], "note": ""} ],
  "examples": [ {"id": "WP03-ch06-ex1", "text": "minimal Game subclass with Exit() in Update", "disposition": "RECREATED", "verified": "syntax-checked | read-checked | not-verified",
                 "destinations": ["deep-dives/framework/game-lifecycle.html#ex-exit"], "note": ""} ],
  "issues": [ {"kind": "bug-candidate | functional-gap | platform-limitation | verification-gap | not-an-issue", "text": "…", "ref": "CNA-BUG-019 | new", "evidence": "path (symbol)"} ]
}
```

Rules the checker enforces (`bible_ledger.py check --units …`):

* Every Bible **heading** of your unit (`units.json` → `headings`: chapter/section/subsection/subsubsection) is a `concepts[].section` value **or** listed in `empty_sections` with a reason.
  Match the heading text as in `units.json` (case/punctuation-insensitive). For `aux-*` markdown units the headings are the `##` (and for `aux-cnabugs`, `###`) headings.
* Concept ids are globally unique: `<WPnn>-<unit-short>-<nnn>`; `text` ≥ 25 chars and self-contained (a reader must understand the concept without the Bible).
* Dispositions per §4; `destinations` must exist on disk (page and `#fragment` id); `tokens` must occur in the destination page's article text; `target.result` required except for
  OBSOLETE / HISTORICAL ONLY / REMOVED FUNCTIONALITY.
* `actions` (unit-level) ⊆ `MERGE, EXPAND, NEW PAGE, DEEP DIVE, REFERENCE, TUTORIAL, MAINTAINER, TESTING/EVIDENCE, BUG, GAP, HISTORY, SUPERSEDED, DUPLICATE, OBSOLETE, TARGET-CONTRADICTED, REMOVED FUNCTIONALITY`.
* `target_relevance`: how much of the unit is current at TARGET. `summary` ≥ 60 chars.
* Figures: PRESERVED | RECREATED | SUPERSEDED | OBSOLETE | MISSING; examples: PRESERVED | RECREATED | SUPERSEDED | REJECTED | OBSOLETE | NOT PORTED | MISSING. Anything MISSING must be gone before you finish.
* A destination that is one of *your* new pages is valid only after you have built it. Build first, record second.

`aux-*` units (subsystem audits, `AUDIT.md`, `PLAN.md`, `NEXT.md`, `cnabugs.md`, …) are research/planning documents the manuscript was written from. Extract the **current technical knowledge** they hold that the
chapters compress or omit (per-API evidence, reproducers, test names, measured numbers with their hosts, "why" reasoning); classify process/history/methodology-of-the-book content as HISTORICAL ONLY with a
note. The bug ledger `aux-cnabugs` is handled by the Known Issues pipeline, not by you, unless your brief says so.

## 7. Issue candidates (bugs, gaps, limitations, verification gaps)

While reading you will meet statements such as "this is a defect", "unimplemented", "silently ignores", "no test covers", "only works on X". Record each in `audit/data/bible/issues/WPnn.json`:

```json
{"wp": "WPnn", "items": [
  {"id": "WPnn-i001", "bible_unit": "ch06-game-lifecycle", "section": "Explicit disposal…", "kind": "bug-candidate",
   "text": "Game::Dispose() raises Disposed even when the inner call was a no-op (idempotence).", "bible_ref": "CNA-BUG-019",
   "target_reading": "still present | absent | narrowed | unclear", "evidence": "modules/runtime/src/Game.cpp (Dispose)", "confidence": "read | focused-test | none"}]}
```

`kind` per the definitions: **bug** = existing behaviour violates an intended/documented contract; **functional gap** = functionality intentionally/currently incomplete or unsupported (a documented boundary);
**platform limitation** = host/platform-specific; **verification gap** = implementation exists but evidence is insufficient; not-an-issue = documentation gap or architectural decision. Do not classify a documentation gap as a
CNA defect, nor an architectural decision as a bug. You do **not** decide "fixed" here — record what you read at TARGET. The orchestrator's Known Issues pipeline reverifies everything with positive evidence.
Where a limitation is an integral part of a concept you write, state it on your page as a plain scoped fact ("… is not supported at TARGET; see Known Issues") without an issue id.

## 8. Report (≤ 400 words, your final message)

(1) units audited (ids) and per-unit counts: Bible words → concepts → dispositions (PRESERVED / EXPANDED / NEW PAGE / …); (2) pages built (paths, word counts) and expansions applied (target pages);
(3) the most important Bible-vs-TARGET contradictions and stale claims you corrected; (4) Bible concepts you judged OBSOLETE / HISTORICAL ONLY / TARGET CONTRADICTED and why (one line each for the notable ones);
(5) issue candidates recorded (count by kind); (6) Phase-1/Phase-2 site errors you noticed (page + fact + evidence) — do not edit those pages yourself; (7) unverifiable items you hedged;
(8) tooling problems; (9) final `bible_ledger.py check --units …` and `check_deep_page.py` results. Do not paste page text or ledger JSON into the report.
