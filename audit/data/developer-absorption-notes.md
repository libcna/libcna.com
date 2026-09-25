## 10. Method, evidence and process notes

**Enumeration.** The units are the *files of the Developer working tree* (95: 80 authored pages, 4 generated-reference pages, 3 presentation assets, 1 process
document, 4 tooling files, 3 repository-metadata files), enumerated mechanically by `scripts/developer_ledger.py enumerate`; the seven files that are modified or
untracked in the Developer working tree (uncommitted work in `graphics/backends.html`, `graphics/headless.html`, `graphics/stub.html`, `takeover/validation.html`,
`docs/COVERAGE.md`, `assets/site.js`, `assets/search-index.js`) were read from the working tree, not from Git HEAD.

**Verification, not transcription.** Developer documents CNA `d6e9ff05`, 55 commits before TARGET; 224 files differ between the two (OpenGL4, SDL_gpu, EasyGL,
graphics tests and examples, `cmake/`). For every page `scripts/dev_pack.py` listed each cited source path (present at TARGET? changed since the pin? renamed?), every code
token unknown to a source-wide identifier index built from TARGET, cited commits and external pins; authors then re-read the source for every load-bearing claim (the
"unchanged since the pin" paths were spot-checked too: Developer contained wrong header paths, a non-existent `Game::UpdateInput`, mis-ordered device creation, and other errors
that byte-identical files could not have caught). The ledger's `target_verification.contradictions` records each correction.

**Conservation checks** (`scripts/developer_ledger.py check`, part of `scripts/validate_all.sh`): every Developer `<h2>/<h3>` is mapped to a destination section whose anchor exists
(or explicitly dropped with a reason); every CNA source path cited by a Developer page is cited by its destination or explained; the destination is not shorter than 85% of its source in
words; at most 35% of the source's `<code>` tokens may be absent from the destination. The remaining review flags (Developer-pin hashes, Developer-site tooling such as `make check`, ellipsis
placeholders) are intentional drops.

**Other mechanical gates.** `scripts/check_dev_page.py` (strict HTML5, fragments, pinned source paths exist at TARGET, no retired renderer identity, no first-person voice, no leftover Developer
vocabulary), `scripts/check_dev_claims.py` (repository paths, CMake presets, options and identifiers against TARGET), `scripts/check_source_links.py` (every CNA link on a Development page is pinned to TARGET and
exists there; binding-repository links exist at their pinned commit), `scripts/check_facts.py` (whole-registry counts on every page equal the canonical facts), `scripts/compare_presentation.py --phase2` (Phase-1 presentation
preserved, 10% shrink guard) and the retired-renderer scan.

**Evidence semantics.** Every Development page states its evidence basis. Nothing was built or run to write these pages; where a page reports a test result or a measurement it attributes it to CNA's own records.
Developer's coverage vocabulary (NOT STARTED / INVESTIGATING / DRAFTED / SOURCE VERIFIED / COMPLETE) describes Developer's own documentation audit and is never republished as CNA product status; the Development home
states which subsystems have a dedicated internals page and which do not, without implying anything about their maturity.

**Process note (model availability).** The first wave of page authors ran on Opus and was cut short when the account's weekly Opus limit was reached (resets 2026-09-27 20:00 Europe/Prague). The pages that had been
written and built by then survived on disk. All remaining work, and the audit and ledger of every page whose author had been interrupted, was done by Sonnet-class agents against TARGET with the same guide and the
same mechanical gates; the orchestrator additionally re-verified sampled claims (Wayland activation token handling, `PlatformEvent` alternatives, `Game` member order, `SetClockForTesting`, the CMake option scan) and fixed the
defects the claim checker and the authors' hand-backs exposed in sibling pages (a mis-named net test hook, three repository-map statements, the Vulkan example-block guard, the "reference implementation" wording).

**Deliberate non-actions.** Bible, the abandoned first unified-documentation attempt, the CNA repository and the Developer repository were not modified, and nothing was pushed. Bug-like findings (222 across the ledgers) are recorded in
section 7 for the later catalogue phase; they are not published as a catalogue.

## 11. Changes to protected Phase-1 pages (all additive or corrective; 0 unexplained presentation losses)

| Change | Pages | Why |
|---|---|---|
| One header entry, "Development", after "Documentation" (`scripts/patch_global_nav.py`, idempotent) | every page (204 + the new ones) | the only global-navigation change; the area's own pages are reached through hubs and a local sidebar |
| Header cap 1360→1460 px, link size/padding 0.9375/0.5 rem → 0.925/0.4 rem, two-row breakpoint 1240→1265 px (`css/style.css`) | all pages | keeps the full menu on one row where it fitted before the extra link |
| New section "Development, internals and the maintainer handbook" (six cards) | `documentation.html` | discoverability; no existing card touched |
| "Go deeper" callout linking Architecture maps, module graph, internals, selection axes | `architecture.html` | additive |
| Third secondary button "Development & Maintainer Guide" beside the two existing buttons of "Get running from source" | `index.html` | additive; no primary CTA changed |
| "Working on CNA itself?" callout | `contribute.html` | additive |
| Factual corrections found while verifying Developer's claims | see `audit/phase2-phase1-errata.md` (58 decisions on 33 pages) | Phase-1 errors, corrected in place |
| Stylesheet and script additions for the Development area (local nav, source links, evidence box, related pages, pager; mobile collapse of the local nav) | `css/style.css`, `js/main.js` | new area only |
