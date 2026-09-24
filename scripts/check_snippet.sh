#!/usr/bin/env bash
# Syntax-only compile check of a C++ snippet against the pinned CNA TARGET headers.
# Writes nothing (g++ -fsyntax-only); does not configure or build CNA.
#
#   scripts/check_snippet.sh snippet.cpp [extra g++ args...]
#
# Environment overrides:
#   CNA_TARGET_TREE   read-only TARGET worktree   (default /rv/tmp/libcna-v2/cna-target)
#   SHARP_RUNTIME     sharp-runtime checkout (branch `next`)  (default ../sharp-runtime next to this repo)
#   CNA_RENDERER      renderer macro suffix, one of the 25 identities (default HEADLESS)
#
# Limits: generated headers (e.g. CNA/Version.hpp) are not available, so snippets that
# include them cannot be checked; that is reported by g++ and is not a snippet error.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
T="${CNA_TARGET_TREE:-/rv/tmp/libcna-v2/cna-target}"
S="${SHARP_RUNTIME:-$here/../sharp-runtime}"
R="${CNA_RENDERER:-HEADLESS}"
[ -d "$T/modules" ] || { echo "TARGET tree not found: $T" >&2; exit 2; }
inc=()
for d in "$T"/modules/*/include "$T"/modules/renderers/*/include "$S"/modules/*/include "$S"/include; do
  [ -d "$d" ] && inc+=("-I$d")
done
src="$1"; shift
exec g++ -std=c++23 -fsyntax-only -Wall "${inc[@]}" "-DCNA_RENDERER_${R}" -DSOUND_ENABLED "$@" "$src"
