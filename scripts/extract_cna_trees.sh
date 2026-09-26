#!/usr/bin/env bash
# Extract read-only copies of two CNA revisions for the validators that read files (not git objects):
#   cna-target  the commit in cnahead      (retired-renderer scan, snippet checks)
#   cna-base    the v0.1.0-alpha.1 baseline (retired identities are BASE minus TARGET)
# Uses `git archive`: nothing in the CNA clone is checked out, modified or cleaned.
#
#   ./scripts/extract_cna_trees.sh [DEST]     # DEST default: ${XDG_CACHE_HOME:-~/.cache}/libcna-com
#
# The validators find DEST by default; otherwise export CNA_BASE_TREE / CNA_TARGET_TREE. CNA clone: ../cna or $CNA_REPO.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CNA_REPO="${CNA_REPO:-$ROOT/../cna}"
DEST="${1:-${XDG_CACHE_HOME:-$HOME/.cache}/libcna-com}"
BASE=1bb2145d99ed572dd4eb15009c34e2e5f410fcf0   # tag v0.1.0-alpha.1, the documented baseline (audit/009d40f5-phase1-delta.md)
TARGET="$(tr -d '[:space:]' < "$ROOT/cnahead")"
for pair in "cna-base:$BASE" "cna-target:$TARGET"; do
  name="${pair%%:*}"; rev="${pair#*:}"
  git -C "$CNA_REPO" cat-file -e "$rev^{commit}" 2>/dev/null || { echo "commit $rev not found in $CNA_REPO (set CNA_REPO)" >&2; exit 1; }
  rm -rf "$DEST/$name.tmp" && mkdir -p "$DEST/$name.tmp"
  git -C "$CNA_REPO" archive "$rev" | tar -x -C "$DEST/$name.tmp"
  echo "$rev" > "$DEST/$name.tmp/.extracted-from"
  rm -rf "$DEST/$name" && mv "$DEST/$name.tmp" "$DEST/$name"
  echo "$name -> $DEST/$name ($rev)"
done
