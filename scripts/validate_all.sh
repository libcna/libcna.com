#!/usr/bin/env bash
# Run every site validator. check_retired_renderers.py and the source-link/ledger checks need the pinned CNA
# material (see audit/c1c316b9-phase5-delta.md and audit/developer-absorption-phase2.md): the CNA clone next to this
# repository (../cna or $CNA_REPO), whose Git objects are read and never modified.
#
# Two stages read repositories outside this one and are optional: the developer.libcna.com conservation ledger
# (../developer.libcna.com or $DEVELOPER_REPO) and the Bible inclusion graph (../bible.libcna.com or $BIBLE_REPO).
# When one is absent the stage is skipped, the run can still succeed, and the final status says so:
#   overall: PASS                                          every stage ran and passed
#   overall: PASS WITH OPTIONAL EXTERNAL CHECKS SKIPPED    everything that ran passed; the listed stages did not run
#   overall: FAIL                                          a stage failed
# With --require-external (or VALIDATE_REQUIRE_EXTERNAL=1) a skipped optional stage fails the run instead.
set -u
cd "$(dirname "$0")/.."
export PYTHONDONTWRITEBYTECODE=1
require_external="${VALIDATE_REQUIRE_EXTERNAL:-0}"
[ "${1:-}" = "--require-external" ] && require_external=1
rc=0
skipped=()
run() { echo "== $*"; "$@" || rc=1; }
skip() { echo "== SKIPPED (optional external stage): $1"; skipped+=("$1"); }
# the validators' own regression fixtures first: if a semantic check has gone blind, nothing below can be trusted
run python3 scripts/test_validators.py
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
  skip "developer_ledger.py check (developer.libcna.com working tree not present at ${DEVELOPER_REPO:-../developer.libcna.com})"
fi
python3 -c "import html5lib" 2>/dev/null || skip "strict HTML5 parse in validate_site.py (html5lib not installed)"
# reads the CNA Git objects (../cna or $CNA_REPO) or, when given, the extracted trees; it fails rather than skips
run python3 scripts/check_retired_renderers.py
# the retired CNA platform backends are derived from cmake/PlatformSelection.cmake at cnahead in the same CNA clone
run python3 scripts/check_retired_platforms.py
run python3 scripts/site_deep.py check
# retired URLs kept as noindex transition pages: exact content, never linked, never indexed
run python3 scripts/tombstones.py check
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
run python3 scripts/compare_presentation.py --phase5 --quiet
run python3 scripts/compare_presentation.py --phase6 --quiet
run python3 scripts/compare_presentation.py --phase7 --quiet
if [ "${PHASE3_FINAL:-0}" = "1" ]; then
  run python3 scripts/bible_ledger.py check --final
fi
# independent adversarial-audit gates: Bible graph, ledger anchors (tokens, SUPERSEDED replacements, semantic content of
# every cited section), issue json/pages/hubs/duplicates, generated ledger counts, applied page fixes
[ -f "${BIBLE_REPO:-../bible.libcna.com}/latex/book/main.tex" ] \
  || skip "adversarial_audit.py graph (Bible repository not present at ${BIBLE_REPO:-../bible.libcna.com})"
run python3 scripts/adversarial_audit.py all
run python3 scripts/apply_page_fixes.py check
run git diff --check
echo
if [ ${#skipped[@]} -gt 0 ]; then
  echo "optional external checks NOT run (${#skipped[@]}):"
  for s in "${skipped[@]}"; do echo "  - $s"; done
  [ "$require_external" = 1 ] && { echo "  (--require-external: a skipped stage fails the run)"; rc=1; }
fi
if [ $rc -ne 0 ]; then
  echo "overall: FAIL"
elif [ ${#skipped[@]} -gt 0 ]; then
  echo "overall: PASS WITH OPTIONAL EXTERNAL CHECKS SKIPPED"
else
  echo "overall: PASS"
fi
exit $rc
