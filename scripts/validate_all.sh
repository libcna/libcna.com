#!/usr/bin/env bash
# Run every site validator. check_retired_renderers.py and the source-link/ledger checks need the pinned CNA
# material (see audit/b0e97bb1-phase4-delta.md and audit/developer-absorption-phase2.md): the CNA clone next to this
# repository (../cna or $CNA_REPO), whose Git objects are read and never modified.
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
# reads the CNA Git objects (../cna or $CNA_REPO) or, when given, the extracted trees; it fails rather than skips
run python3 scripts/check_retired_renderers.py
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
run python3 scripts/compare_presentation.py --phase4 --quiet
if [ "${PHASE3_FINAL:-0}" = "1" ]; then
  run python3 scripts/bible_ledger.py check --final
fi
# independent adversarial-audit gates: Bible graph, ledger anchors, issue json/pages/hubs/duplicates, generated ledger counts, applied page fixes
run python3 scripts/adversarial_audit.py all
run python3 scripts/apply_page_fixes.py check
run git diff --check
echo "overall: $([ $rc -eq 0 ] && echo PASS || echo FAIL)"
exit $rc
