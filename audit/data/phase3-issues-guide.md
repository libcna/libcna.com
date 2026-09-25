# Phase-3 issues guide — verifying current bugs, gaps, limitations and verification gaps at TARGET

Binding for every agent of the Known Issues pipeline (packages `B1`…`B6`). Read `audit/data/phase3-editorial-guide.md` §1 (hard boundaries), §4 (evidence semantics, XNA nuance,
retired-renderer rule) and §5.6 (quality bar) first; they apply here unchanged. This guide replaces its §6–§8 for your package.

## 0. The question this area answers

> **What is wrong with, or missing from, CNA right now — at commit `009d40f5dd085c4e674d3479675fac84b12b3e0a`?**

Not: what was wrong at some earlier audit. The public Known Issues area (`known-issues/`) lists **only what exists at TARGET**. There is no fixed-bug museum. A candidate that turns out to be
fixed, obsolete, not a defect, or unsupported by evidence is recorded in the (non-public) disposition list of your package, never on the site.

`Candidate finding does NOT automatically mean bug.` Every candidate is re-verified from scratch against TARGET (source, headers, CMake, tests, CI; occasionally a focused execution).

## 1. Inputs

* `audit/data/bible/issues/candidates-<area>.json` — the candidates assigned to your package: Bible defect-ledger entries (`CNA-BUG-###`, with the Bible's own claim, severity, confidence and its
  TARGET-era disposition), Phase-2 Development-page findings (`P2-###`, with the page that recorded it), and candidates found by the chapter packages (`WPnn-i###`). Read each candidate's
  `text`/`bible_body` fully. The Bible's ledger text itself: `/rv/data/development/github.com/libcna/bible.libcna.com/cnabugs.md` (working tree; read-only). The Bible checked its items at
  `d6e9ff05`, 55 commits before TARGET, and its "TARGET disposition" table is a *hint*, not evidence.
* The TARGET tree `/rv/tmp/libcna-v2/cna-target` (read-only; `third_party/` and `vendor/` via `git -C /rv/data/development/github.com/libcna/cna show 009d40f5dd085c4e674d3479675fac84b12b3e0a:<path>`),
  `git -C /rv/data/development/github.com/libcna/cna diff d6e9ff05 009d40f5 -- <path>` (what changed after the Bible's pin), the site pages named in each candidate (read them: a Development page may already
  carry a hedged statement about the same behaviour), `python3 scripts/site_grep.py TOKEN`.
* Never look at anything after TARGET (the CNA checkout's HEAD is past it). Never modify CNA. No `git add/commit/push`.

## 2. Classification (per candidate) — and what each outcome requires

| Classification | Meaning | Public? | Required evidence |
|---|---|---|---|
| `STILL EXISTS` | the defect/gap is present at TARGET exactly as claimed (or as you re-derived it) | yes — as bug / gap / limitation / verification gap | path + function (+ test files) you read; state what you did **not** run |
| `PARTIALLY FIXED` | part of the claim was fixed; a narrower defect survives | yes — the entry describes **only** the surviving defect; keep the original stable ID | what was fixed (path+symbol) and what survives |
| `PROVEN FIXED` | absent at TARGET | **no** | *positive* evidence: the fixing code path **and** (where one exists) the test that pins it. A deleted TODO, a commit message, a rewritten subsystem or cleaner-looking code is **not** proof. |
| `OBSOLETE` | the affected functionality/identity no longer exists at TARGET | no | evidence the path/module/identity is gone (registry, tree) |
| `NOT A BUG` | intended behaviour, an architectural decision, a documentation gap of *this website*, or an XNA-faithful quirk | no (unless it deserves a gap/limitation entry — say which) | why the contract says so |
| `INSUFFICIENT EVIDENCE` | cannot decide by reading; no safe focused run | no as a bug; possibly as a **verification gap** if the implementation exists but its evidence is thin | what you tried |

Rules: (1) **Do not silently declare fixed.** If reading is ambiguous, keep investigating (call the function's callers, read the tests, diff the history of the path), and if a small non-destructive execution
would settle it, do it (§5). (2) **Do not invent certainty**: "reads as broken" is `confidence: verified-by-reading`, not `reproduced`. (3) A defect in *CNA's own documentation, generated inventory or tooling*
(a README number that contradicts a generated audit, a checker that cannot classify a module) is a genuine CNA defect **only** when it lives in the CNA repository at TARGET; record it as a bug with
`subsystem: "Documentation & release tooling"`. A gap in *libcna.com* is never a CNA defect. (4) A **bug** is existing behaviour that violates an intended/documented contract (the contract may be XNA's, a
CNA header's Doxygen, a test's expectation, a CNA doc's statement). A **functional gap** is functionality intentionally/currently incomplete or unsupported (a documented boundary, a `NotSupportedException`
by design, a missing feature). A **platform limitation** is a host/platform/toolchain-specific limit. A **verification gap** is an implementation that exists but whose behaviour lacks evidence (no test, unexecuted
lane, unreviewed oracle, a permanently-skipped gate). Do not classify an architectural decision as a bug. A capability flag that *lies* (reports true while the implementation refuses) is a bug; a documented
refusal is a gap.

## 3. What to publish for each surviving item (STILL EXISTS / PARTIALLY FIXED)

One JSON object per item in your `issues[]` (see §6). Fields (HTML strings may use the Development page tokens `{{src:modules/x/y.cpp|label}}`, `{{tree:dir|label}}`, `{{page:development/…|label}}`; escape `<`/`&`;
no inline styles/scripts):

| Field | Content |
|---|---|
| `cand_ids` | every candidate id this entry resolves (a defect reported three times is one issue) |
| `id` | for an item with a Bible id keep it (`CNA-BUG-019`). For anything new use a temporary id `NEW-<pkg>-<nn>`; the orchestrator assigns the final stable id at merge |
| `class` | `bug` \| `functional-gap` \| `platform-limitation` \| `verification-gap` |
| `title` | precise, one line, names the symbol; describes only the surviving defect |
| `summary` | one sentence for tables |
| `subsystem` | one of: Math & geometry · Core & runtime · Graphics & renderers · Content & XNB/CNB/CNJ · Models & glTF · Input · Audio & media · Storage · Networking & gamer services · Platforms · Build & CI · Testing & evidence · Diagnostics & Inspector · C API & bindings · Documentation & release tooling |
| `status` | `open` (exactly as first recorded) \| `narrowed` (partially fixed; text describes what survives) |
| `severity` | `high` \| `medium` \| `low` — your judgement, stated as a starting point for triage; `n/a` for gaps/limitations |
| `confidence` | `reproduced` (you or CNA's own record executed it) \| `verified-by-reading` (the failure follows mechanically from code you read) \| `strong` \| `probable` |
| `public_contract` | the affected public API / contract, e.g. `CNA::Plane::Transform(const Plane&, const Matrix&)` |
| `expected` / `actual` | HTML paragraphs: the intended behaviour and the behaviour at TARGET |
| `sources` | list of `{"path": "modules/math/src/Plane.cpp", "note": "Plane::Transform — the aliased Transpose call"}`; paths must exist at TARGET (checked); functions named, no line numbers |
| `evidence` | HTML: what was read; what was executed (exact scope) or "not executed"; which documents/tests corroborate; what remains uncertain |
| `reproduction` | HTML with a `<pre><code class="language-cpp">` focused reproduction, or `null` when none is known (do not invent one) |
| `tests_current` | HTML: the current tests that touch the area (paths), and what they do *not* cover |
| `regression_test` | HTML: the missing regression test that would pin the fix, or the existing test that fails/passes it |
| `blast_radius` | HTML: exactly which callers/features are affected and which are not |
| `workaround` | HTML or `null` |
| `related` | `{"internals": [["development/…html#id", "label"]], "architecture": [...], "maintainer": [...], "guide": [...], "deep": [...]}` — links that must exist |
| `origin` | e.g. `"Bible ledger CNA-BUG-019; Phase-2 candidate P2-013"` (kept in the JSON only, not shown publicly) |

Quality bar: actionable for a future human C++ maintainer — enough to find the code, understand the contract, reproduce or decide, and write the missing test. Do not pad; do not invent.
Reproductions: illustrative snippets must be marked as such; a snippet you actually compiled/ran says so and how (§5).

## 4. Dispositions list (non-public audit trail, mandatory for **every** candidate)

```json
{"cand": "CNA-BUG-021", "source": "bible-cnabugs | phase2 | wp", "classification": "STILL EXISTS", "published_as": "CNA-BUG-021",
 "evidence": "modules/content/src/ContentManager.cpp (ContentManager::Unload) — clears loadedAssets_ without Dispose; no test in modules/content/tests asserts disposal",
 "changed_since_bible_pin": false, "executed": "none | scope", "note": ""}
```

For `PROVEN FIXED` / `OBSOLETE` / `NOT A BUG` / `INSUFFICIENT EVIDENCE` the `evidence` field carries the positive evidence (or the reasoning) — never "looks fixed". The orchestrator checks the conservation equation
`candidates = published + fixed + obsolete + not-a-bug + insufficient` with zero unexplained ids. Do **not** name retired renderer identities in any field (use "a retired renderer family"); a candidate whose subject is
a retired renderer is `OBSOLETE` (evidence: the affected identity is not in the public list of `cmake/RendererIdentities.cmake`, and the module directory is absent at TARGET).

## 5. Focused execution (optional, rare, scoped)

Reading is the default. Execute only when an ambiguity is *important* and a small, non-destructive run settles it (e.g. a numeric edge case in a pure function). Rules: never modify CNA; never build under `/tmp` or the
scratchpad; the only allowed build location is `/rv/data/development/github.com/libcna/libcna.com/build-probe/` (shared by everyone; use a file-name prefix `<pkg>-<topic>-…`, e.g. `B1-plane-transpose.cpp`; never
create another build directory; remove your probes when done); use `CCACHE_DIR=/rv/cnaccache CCACHE_BASEDIR=/rv` with `ccache g++`; **do not** configure or build CNA as a whole. Compile only the few TARGET sources you need
(`g++ -std=c++23 -I<target>/modules/…/include -I<sharp-runtime include> …`); `/rv/data/development/github.com/libcna/sharp-runtime` is available (its `next` branch is the one CNA uses; do not check anything out — read
headers as they are and say so if the revision differs). Never run several heavy jobs at once (30 GB RAM shared with ten agents). Record the exact scope of any run ("compiled Plane.cpp+Matrix.cpp against sharp-runtime @ <sha>; ran driver X; observed Y").
If a run is impractical, say so and rely on reading with the honest `confidence`.

## 6. Output files (yours only)

* `audit/data/bible/issues/verified-<pkg>.json` → `{"pkg": "B1", "dispositions": [...every candidate...], "issues": [...public entries...]}`
* You do **not** write pages. The orchestrator merges `verified-*.json`, allocates ids, writes `data/known-issues.json` and generates `known-issues/**` (detail page per issue, category hubs, overview) from it.
  Check yourself with `python3 scripts/known_issues.py check --pkg <pkg>` (validates your JSON: required fields, TARGET paths, links, classification vocabulary, conservation of your candidates).

## 7. Report (≤ 350 words, final message)

(1) candidates received (by source) and the outcome counts: STILL EXISTS / PARTIALLY FIXED / PROVEN FIXED / OBSOLETE / NOT A BUG / INSUFFICIENT EVIDENCE; (2) published items by class (bug / gap / limitation /
verification gap) with ids; (3) the most surprising outcomes (a Bible "open" that is fixed, a Bible "fixed" that survives, a Phase-2 candidate that was a stale statement); (4) new defects you found beyond the candidates
(with evidence); (5) Development/Phase-1 pages that contradict your findings (page + sentence + evidence) — do not edit them; (6) anything executed (exact scope); (7) `known_issues.py check` result.
