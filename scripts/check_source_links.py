#!/usr/bin/env python3
"""Validate source-pinned links to the CNA repository (and to pinned binding repositories) across the site.

Policy
  * development/** (deep Architecture / Internals / Maintainer pages): every link into github.com/libcna/cna must be a
    blob/tree link pinned to TARGET (cnahead) whose path exists in the TARGET Git tree, or a commit link whose commit is
    reachable from TARGET.  A moving ref (next, develop, master, HEAD) in a deep page is an error.
  * every other page: links pinned to TARGET are validated the same way; links pinned to another 40-hex commit are
    reported; moving refs are counted (Phase-1 pages use them for user-facing "browse the repo" links).
  * links into pinned binding repositories (cna-cs, cna-java, cna-python, ...) at a 40-hex commit are validated against
    the local sibling checkout when present (path must exist at that commit).

Reads Git objects only; never writes to any repository.  Exit status 1 on any error.
"""

from __future__ import annotations

import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
CNA = ROOT.parent / "cna"
TARGET = (ROOT / "cnahead").read_text().strip()
LINK = re.compile(r'href="(https://github\.com/libcna/([A-Za-z0-9._-]+)/(blob|tree|commit)/([^/"#]+)(?:/([^"#]*))?)(#[^"]*)?"')


def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=check)


def main() -> int:
    ls = git(CNA, "ls-tree", "-r", "--name-only", TARGET).stdout.splitlines()
    files = set(ls)
    dirs = {"/".join(f.split("/")[:i]) for f in ls for i in range(1, len(f.split("/")))}
    errors: list[str] = []
    stats: Counter[str] = Counter()
    other_pins: defaultdict[str, int] = defaultdict(int)
    commit_ok: dict[str, bool] = {}
    ext_ok: dict[tuple[str, str, str], bool] = {}
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT).as_posix()
        deep = rel.startswith("development/")
        text = path.read_text(encoding="utf-8")
        seen: set[str] = set()
        for m in LINK.finditer(text):
            url, repo, kind, ref, sub = m.group(1), m.group(2), m.group(3), m.group(4), unquote(m.group(5) or "")
            if url in seen:
                continue
            seen.add(url)
            sub = sub.rstrip("/")
            pinned = re.fullmatch(r"[0-9a-f]{40}", ref) is not None
            if repo == "cna":
                if kind == "commit":
                    if ref not in commit_ok:
                        commit_ok[ref] = git(CNA, "merge-base", "--is-ancestor", ref, TARGET, check=False).returncode == 0
                    stats["cna commit links"] += 1
                    if not commit_ok[ref]:
                        errors.append(f"{rel}: commit {ref[:10]} is not an ancestor of TARGET")
                    continue
                if pinned and ref == TARGET:
                    stats["cna links pinned to TARGET (deep pages)" if deep else "cna links pinned to TARGET (other pages)"] += 1
                    if sub and sub not in files and sub not in dirs:
                        errors.append(f"{rel}: pinned path absent at TARGET: {sub}")
                elif pinned:
                    other_pins[rel] += 1
                    if deep:
                        errors.append(f"{rel}: CNA link pinned to a commit other than TARGET: {ref[:10]}/{sub}")
                else:
                    stats["cna links on a moving ref (other pages)" if not deep else "cna moving-ref links in deep pages"] += 1
                    if deep:
                        errors.append(f"{rel}: deep page links CNA at a moving ref '{ref}': {sub}")
            elif repo.startswith("cna-") and pinned and kind == "blob":
                key = (repo, ref, sub)
                if key not in ext_ok:
                    local = ROOT.parent / repo
                    if not local.exists():
                        ext_ok[key] = True
                    else:
                        ext_ok[key] = git(local, "cat-file", "-e", f"{ref}:{sub}", check=False).returncode == 0
                stats["pinned binding-repository links"] += 1
                if not ext_ok[key]:
                    errors.append(f"{rel}: {repo}@{ref[:8]} has no {sub}")
    for k, v in sorted(stats.items()):
        print(f"{k}: {v}")
    if other_pins:
        print(f"CNA links pinned to another commit on {len(other_pins)} page(s) (informational)")
    if errors:
        print(f"FAILED: {len(errors)} problem(s)")
        for e in errors[:80]:
            print(" -", e)
        return 1
    print("source links: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
