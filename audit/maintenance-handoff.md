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
- Other tools still default to `/rv/tmp/libcna-v2/...` (`check_cpp_blocks.py`, `check_dev_claims.py`, `dev_pack.py`; all but
  `check_dev_claims.py` honour `CNA_TARGET_TREE`). They are authoring-time helpers, outside `validate_all.sh`.
- Low-contrast warnings on inherited Phase-1/2 elements remain known presentation debt; deliberately not touched.

## Owner decision pending (do not decide in code or public prose)

Whether libcna.com should publicly disclose AI assistance in producing the documentation. No public wording either way has been added.
