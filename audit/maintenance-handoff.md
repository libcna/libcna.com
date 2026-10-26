# Human-maintenance hardening — internal notes

Internal record (not published; `audit/` is excluded by `_config.yml`). The maintainer workflow itself lives in
`development/maintenance.html` (section "Routine maintenance without any agent tooling") and `scripts/regenerate_site.sh`.

## What this pass changed

- `scripts/regenerate_site.sh` (+ `--check`): one ordered entry point. Order found by experiment in a clean worktree:
  `generate_dev_reference.py` rewrites its pages whole and drops their backlink blocks, so it must precede `backlinks.py apply`;
  `issue_refs.py apply` follows `known_issues.py merge/build`; `build_site_indexes.py` is last.
- Idempotence measured on the committed tree: two consecutive runs leave a clean worktree.
- Hidden dependencies removed from the validated path: hard-coded `/rv/tmp/libcna-v2/cna-{base,target}` (now `CNA_BASE_TREE` /
  `CNA_TARGET_TREE` or `~/.cache/libcna-com`, created by `scripts/extract_cna_trees.sh`); the `/tmp/claude-1000` Chrome profile in
  `browser_qa.py`; `developer_ledger.py check` now skips when the retired developer.libcna.com tree is absent.

## Findings kept for later (not fixed here)

- **`apply_expansions.py apply` is not safe to re-run.** It re-applied two blocks and reverted later `apply_page_fixes.py` edits
  (`deep-dives/models/gltf-import.html`, `deep-dives/foundations/language-conventions.html`). The expansion sources under
  `audit/data/bible/expansions/` are stale relative to those pages. It is therefore excluded from regeneration; `check` passes.
  Future work: fold the page fixes back into the expansion sources, then include `apply` in the routine.
  *Phase 4 (2026-10-04):* every expansion source was folded back from its page region (token links reconstructed, the
  rendered source verified equal to the page region for all 34 expansions), so `apply` is now a no-op on the content of the
  blocks. It still stamps `dateModified`, and it is still not part of `regenerate_site.sh`.
  *Phase 5 (2026-10-09):* the pin move to `c1c316b9` edited 23 of those regions in place (retired renderers and platform
  backends, new numbers), which made the sources stale again — re-applying them would have restored retired content. Two
  guards now exist: `apply_expansions.py check` fails on any drift between a source and its page region, and
  `apply_expansions.py fold` writes edited regions back into their sources (CNA source links pinned to `cnahead` are turned
  back into `{{src:}}` / `{{tree:}}` tokens; the round trip is verified). After a deliberate page edit inside a
  `p3:begin`/`p3:end` region, run `fold`, then `check`.
  *Phase 6 (2026-10-25):* the pin move to `c6dec91f` edited 29 regions in place and folded them back (`fold`, then
  `check`: expansions ok).
- *Phase 5:* the footer and doc-meta snapshot sentence is no longer hard-coded: `scripts/site_nav.py` derives it from
  `cnahead` and `data/current-facts.json`, so the next pin move updates it through `site_nav.py sync` (and the Known
  Issues/Deep Dives hub generators that import it).
- *Phase 5:* two retirement guards now run in `validate_all.sh`: `check_retired_renderers.py` (identity spellings plus the
  prose aliases of retired identities) and `check_retired_platforms.py` (the retired `CNA_PLATFORM` backends, derived from
  `cmake/PlatformSelection.cmake`; SDL's `x11`/`wayland`/`windows` drivers and native handles stay legal).
- ~~Other tools still default to `/rv/tmp/libcna-v2/...`~~ *Phase 6:* `check_cpp_blocks.py`, `check_dev_claims.py` and
  `dev_pack.py` now default to `~/.cache/libcna-com/cna-target` (the tree `extract_cna_trees.sh` writes; the old default
  was an extraction of the Phase 1 pin `009d40f5`) and all honour `CNA_TARGET_TREE`. They are authoring-time helpers,
  outside `validate_all.sh`.
- *Phase 6:* every presentation comparison (`compare_presentation.py`, phases 1–6) runs in `validate_all.sh`, so an
  element removed in a later update must be dispositioned in every phase file whose baseline holds it, not only the
  newest (Phase 6 added 24 / 37 / 162 / 565 / 594 entries to phases 1–5). Likewise `apply_page_fixes.py check` needs a
  `superseded_by` on each earlier fix whose text an update rewrote.
- *Phase 6 follow-up (2026-10-26), fixed:* 682 pages loaded `prism-cpp.min.js` and `prism-glsl.min.js` without
  `prism-c.min.js`, which both extend (`docs/releases.html` loaded it after `prism-cpp`), so both threw
  `TypeError: Cannot set properties of undefined` at load and no C++ or GLSL block was highlighted; `docs/releases.html`
  also lacked `prism-bash` for its shell blocks. The footer scripts are baked into each hand-written page, and
  `site_nav.py sync` rewrites only the docs sidebars, so changing `footer_block()` alone reaches only the pages that
  generators write whole (Known Issues entries, hubs, the five reference pages, tombstones). `scripts/prism_scripts.py`
  reads each component's dependencies from its own `extend("…")` calls; `fix` inserted the missing scripts in place
  on 683 pages (same tag form, prefix and separator; idempotent), and `validate_site.py` now fails on a component
  loaded before what it extends, without the core, twice, or missing for a `language-…` block. Fixtures in
  `test_validators.py`. Checked in headless Chrome: no console error on any of the 687 pages, and every C++ (1,072),
  GLSL (49) and C (7) block highlighted.
- Low-contrast warnings on inherited Phase-1/2 elements remain known presentation debt; deliberately not touched.

## Owner decision pending (do not decide in code or public prose)

Whether libcna.com should publicly disclose AI assistance in producing the documentation. No public wording either way has been added.
