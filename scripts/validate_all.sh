#!/usr/bin/env bash
# Run every site validator. check_retired_renderers.py and the source-link/ledger checks need the pinned CNA
# material (see audit/009d40f5-phase1-delta.md and audit/developer-absorption-phase2.md); the retired-renderer scan
# is skipped when the extracted TARGET tree is absent. Create the trees with scripts/extract_cna_trees.sh.
set -u
cd "$(dirname "$0")/.."
export PYTHONDONTWRITEBYTECODE=1
rc=0
run() { echo "== $*"; "$@" || rc=1; }
run python3 scripts/validate_site.py
run python3 scripts/validate_presentation.py
run python3 scripts/compare_presentation.py --quiet
run python3 scripts/compare_presentation.py --phase2 --quiet
run python3 scripts/check_facts.py
run python3 scripts/check_source_links.py
run python3 scripts/site_dev.py check
# Phase-2 conservation check: compares against the retired developer.libcna.com working tree (../developer.libcna.com or
# $DEVELOPER_REPO). That tree is external to this repository, so the check is skipped when it is not present.
if [ -f audit/data/developer-absorption-units.json ] && [ -f "${DEVELOPER_REPO:-../developer.libcna.com}/cnahead" ]; then
  run python3 scripts/developer_ledger.py check
else
  echo "== developer_ledger.py skipped (developer.libcna.com working tree not present)"
fi
CNA_CACHE="${XDG_CACHE_HOME:-$HOME/.cache}/libcna-com"
if [ -d "${CNA_TARGET_TREE:-$CNA_CACHE/cna-target}/cmake" ]; then
  run python3 scripts/check_retired_renderers.py
else
  echo "== check_retired_renderers.py skipped (CNA worktrees not present)"
fi
run python3 scripts/site_deep.py check
run python3 scripts/check_deep_page.py --all
run python3 scripts/apply_expansions.py check
run python3 scripts/backlinks.py check
if [ -f data/known-issues.json ]; then
  run python3 scripts/known_issues.py validate
  # hand-written references to entries whose id the audit allocated: marked, current, and no unmarked one
  run python3 scripts/issue_refs.py check
fi
run python3 scripts/compare_presentation.py --phase3 --quiet
if [ "${PHASE3_FINAL:-0}" = "1" ]; then
  run python3 scripts/bible_ledger.py check --final
fi
# independent adversarial-audit gates: Bible graph, ledger anchors, issue json/pages/hubs/duplicates, generated ledger counts, applied page fixes
run python3 scripts/adversarial_audit.py all
run python3 scripts/apply_page_fixes.py check
run git diff --check
echo "overall: $([ $rc -eq 0 ] && echo PASS || echo FAIL)"
exit $rc
