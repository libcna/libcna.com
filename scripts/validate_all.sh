#!/usr/bin/env bash
# Run every site validator. check_retired_renderers.py and the source-link/ledger checks need the pinned CNA
# material (see audit/009d40f5-phase1-delta.md and audit/developer-absorption-phase2.md); the retired-renderer scan
# is skipped when the extracted TARGET tree is absent.
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
if [ -f audit/data/developer-absorption-units.json ]; then
  run python3 scripts/developer_ledger.py check
fi
if [ -d "${CNA_TARGET_TREE:-/rv/tmp/libcna-v2/cna-target}/cmake" ]; then
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
