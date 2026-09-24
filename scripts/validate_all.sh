#!/usr/bin/env bash
# Run every site validator. check_retired_renderers.py needs the pinned CNA worktrees
# (see audit/009d40f5-phase1-delta.md); it is skipped when they are absent.
set -u
cd "$(dirname "$0")/.."
export PYTHONDONTWRITEBYTECODE=1
rc=0
run() { echo "== $*"; "$@" || rc=1; }
run python3 scripts/validate_site.py
run python3 scripts/validate_presentation.py
run python3 scripts/compare_presentation.py --quiet
run python3 scripts/check_facts.py
if [ -d "${CNA_TARGET_TREE:-/rv/tmp/libcna-v2/cna-target}/cmake" ]; then
  run python3 scripts/check_retired_renderers.py
else
  echo "== check_retired_renderers.py skipped (CNA worktrees not present)"
fi
run git diff --check
echo "overall: $([ $rc -eq 0 ] && echo PASS || echo FAIL)"
exit $rc
