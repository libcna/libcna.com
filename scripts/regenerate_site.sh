#!/usr/bin/env bash
# Regenerate every generated part of libcna.com, in dependency order. Idempotent: on a current checkout it changes nothing.
#
#   ./scripts/regenerate_site.sh           # regenerate in place, then run ./scripts/validate_all.sh
#   ./scripts/regenerate_site.sh --check   # regenerate in a throwaway copy of HEAD's tree and report drift; your tree is untouched
#
# Needs only Python 3 and git. The reference inventories are read from the CNA git objects at the commit in cnahead
# (CNA clone: ../cna, or set CNA_REPO): page source-link tokens are expanded and validated against that tree. The clone is only read.
#
# Order matters (see development/maintenance.html, "Regenerate"):
#   1. known_issues.py merge, build
#                                 merge: audit/data/bible/issues/{verified-*,merge-map,patches,patches-adversarial}.json ->
#                                 issues-source.json + dispositions.json. Visible CNA-BUG/GAP/PLAT/VGAP numbers are ALLOCATED here,
#                                 in order, so a reclassification can shift them; dispositions.json records stable key -> current id.
#                                 build: data/known-issues.json + known-issues/** pages and hubs from issues-source.json.
#   2. site_deep.py hubs, sync    Deep Dives / Known Issues hubs, sidebars, breadcrumbs, pagers
#   3. generate_dev_reference.py  five reference pages. It REWRITES those pages whole, which drops their backlink blocks,
#                                 so it must run before step 6.
#   4. site_dev.py sync, site_nav.py sync   Development and docs sidebars / breadcrumbs / pagers
#   5. (not run) apply_expansions.py apply -- deliberately NOT part of the routine: re-applying an expansion rewrites its block
#                                 from audit/data/bible/expansions/ and would revert later apply_page_fixes.py edits.
#                                 validate_all.sh runs "apply_expansions.py check" and "apply_page_fixes.py check" instead.
#   6. backlinks.py apply         "Deep dives on this topic" / "Known issues in this area" blocks on docs/ and development/ pages
#   7. issue_refs.py apply        hand-written <!--issue:KEY--> references -> current visible id and link. After steps 1 and 6.
#   8. build_site_indexes.py      search-index.json + sitemap.xml. LAST, because it reads the finished pages' metadata.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export PYTHONDONTWRITEBYTECODE=1

MODE=apply
case "${1:-}" in
  "") ;;
  --check) MODE=check ;;
  *) echo "usage: $0 [--check]" >&2; exit 2 ;;
esac

if [ "$MODE" = check ]; then
  # Work on a temporary worktree of HEAD (committed state) so the maintainer's tree is never modified.
  # Uncommitted edits are therefore not seen: commit (or stash) first.
  command -v git >/dev/null || { echo "git is required" >&2; exit 1; }
  if [ -n "$(git status --porcelain --untracked-files=no)" ]; then
    echo "note: --check inspects the committed HEAD only; uncommitted changes are not included." >&2
  fi
  export CNA_REPO="${CNA_REPO:-$ROOT/../cna}"
  TMP="$(mktemp -d "${TMPDIR:-/tmp}/libcna-regenerate.XXXXXX")"
  cleanup() { git -C "$ROOT" worktree remove --force "$TMP/wt" >/dev/null 2>&1 || true; rm -rf "$TMP"; }
  trap cleanup EXIT
  git worktree add --detach -q "$TMP/wt" HEAD
  "$TMP/wt/scripts/regenerate_site.sh"
  if [ -n "$(git -C "$TMP/wt" status --porcelain)" ]; then
    echo "DRIFT: regeneration changes committed files:" >&2
    git -C "$TMP/wt" status --short >&2
    exit 1
  fi
  echo "check: regeneration leaves the committed tree unchanged"
  exit 0
fi

# Prerequisites: fail early and clearly.
for f in cnahead audit/data/bible/issues/issues-source.json audit/data/bible/issues/dispositions.json \
         scripts/known_issues.py scripts/site_deep.py scripts/generate_dev_reference.py scripts/site_dev.py \
         scripts/site_nav.py scripts/backlinks.py scripts/issue_refs.py scripts/build_site_indexes.py; do
  [ -f "$f" ] || { echo "missing required file: $f (run from a complete checkout)" >&2; exit 1; }
done
command -v python3 >/dev/null || { echo "python3 is required" >&2; exit 1; }
export CNA_REPO="${CNA_REPO:-$ROOT/../cna}"
TARGET="$(tr -d '[:space:]' < cnahead)"
git -C "$CNA_REPO" cat-file -e "$TARGET^{commit}" 2>/dev/null || {
  echo "CNA commit $TARGET (cnahead) not found in '$CNA_REPO'. Clone CNA next to this repository or set CNA_REPO." >&2; exit 1; }

run() { echo "== $*"; "$@"; }

run python3 scripts/known_issues.py merge
run python3 scripts/known_issues.py build
run python3 scripts/site_deep.py hubs
run python3 scripts/site_deep.py sync

run python3 scripts/generate_dev_reference.py

run python3 scripts/site_dev.py sync
run python3 scripts/site_nav.py sync
run python3 scripts/backlinks.py apply
run python3 scripts/issue_refs.py apply
run python3 scripts/build_site_indexes.py

echo "regenerate: done. Now run ./scripts/validate_all.sh, review 'git diff --stat', and commit source and generated files together."
