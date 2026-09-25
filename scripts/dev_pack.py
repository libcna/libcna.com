#!/usr/bin/env python3
"""Verification pack for one developer.libcna.com page (read-only helper for the Phase-2 absorption).

    dev_pack.py platforms/wayland.html          # markdown pack on stdout
    dev_pack.py --words                          # (re)build the TARGET identifier index and exit

What it mechanically establishes, so an author can spend their time on the claims that need judgement:

  * every CNA source path the Developer page cites: does it exist at TARGET, and did it change between
    the Developer pin and TARGET (with numstat, rename detection, and the exact `git diff` command);
  * every `<code>` token whose identifier parts do not occur anywhere in the TARGET source tree
    (a strong signal of a renamed, removed or invented symbol; third_party/vendor are not in the index);
  * commits cited by the page and whether they are reachable from TARGET;
  * the page text with each cited path shown inline, and the heading list.

The Developer working tree, the CNA repository and the extracted TARGET snapshot are only read.
"""

from __future__ import annotations

import html
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEV = Path(os.environ.get("DEVELOPER_REPO", ROOT.parent / "developer.libcna.com"))
CNA = Path(os.environ.get("CNA_REPO", ROOT.parent / "cna"))
SNAP = Path(os.environ.get("CNA_TARGET_TREE", "/rv/tmp/libcna-v2/cna-target"))
WORDS = SNAP.parent / "target-words.txt"
TARGET = (ROOT / "cnahead").read_text().strip()
DEV_PIN = (DEV / "cnahead").read_text().strip()

TEXT_SUFFIX = {".hpp", ".h", ".cpp", ".c", ".cc", ".mm", ".m", ".inl", ".cmake", ".txt", ".md", ".json", ".py",
               ".sh", ".yml", ".yaml", ".glsl", ".vert", ".frag", ".comp", ".hlsl", ".fx", ".in", ".cs", ".java",
               ".swift", ".rs", ".ts", ".js", ".html", ".css", ".plist", ".toml", ".cfg", ".supp", ".patch", ""}
IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(CNA), *args], check=True, capture_output=True, text=True).stdout


def build_words() -> set[str]:
    words: set[str] = set()
    for dirpath, _, files in os.walk(SNAP):
        for name in files:
            p = Path(dirpath) / name
            if p.suffix.lower() not in TEXT_SUFFIX:
                continue
            try:
                if p.stat().st_size > 6_000_000:
                    continue
                words.update(IDENT.findall(p.read_text(encoding="utf-8", errors="ignore")))
            except OSError:
                continue
    # file and directory names also count as words
    for dirpath, dirs, files in os.walk(SNAP):
        for name in list(dirs) + files:
            words.update(IDENT.findall(name))
    return words


def load_words() -> set[str]:
    if not WORDS.exists():
        w = build_words()
        WORDS.write_text("\n".join(sorted(w)), encoding="utf-8")
        return w
    return set(WORDS.read_text(encoding="utf-8").split("\n"))


def delta() -> tuple[dict[str, str], dict[str, str], dict[str, tuple[int, int]]]:
    status: dict[str, str] = {}
    renames: dict[str, str] = {}
    for line in git("diff", "--name-status", "-M", DEV_PIN, TARGET).splitlines():
        parts = line.split("\t")
        if parts[0].startswith("R"):
            status[parts[1]] = "R"
            renames[parts[1]] = parts[2]
            status[parts[2]] = "R-new"
        else:
            status[parts[1]] = parts[0]
    numstat: dict[str, tuple[int, int]] = {}
    for line in git("diff", "--numstat", DEV_PIN, TARGET).splitlines():
        a, d, path = line.split("\t", 2)
        numstat[path] = (int(a) if a.isdigit() else 0, int(d) if d.isdigit() else 0)
    return status, renames, numstat


def page_text(raw: str) -> str:
    m = re.search(r"<article.*?</article>", raw, re.S)
    b = m.group(0) if m else raw
    b = re.sub(r"<pre[^>]*>(.*?)</pre>",
               lambda m: "\n```\n" + html.unescape(re.sub(r"<[^>]+>", "", m.group(1))) + "\n```\n", b, flags=re.S)
    def heading(m: re.Match) -> str:
        ident = re.search(r'id="([^"]+)"', m.group(2))
        suffix = "  {#" + ident.group(1) + "}" if ident else ""
        return "\n" + "#" * int(m.group(1)) + " " + re.sub(r"<[^>]+>", "", m.group(3)) + suffix + "\n"

    b = re.sub(r"<h([1-4])([^>]*)>(.*?)</h\1>", heading, b, flags=re.S)

    def link(m: re.Match) -> str:
        label = re.sub(r"<[^>]+>", "", m.group(2))
        href = m.group(1)
        mm = re.match(r"https://github\.com/libcna/cna/(?:blob|tree)/[0-9a-f]{40}/(.*)", href)
        if mm:
            return f"{label} [@{mm.group(1)}]"
        if href.startswith("http"):
            return f"{label} [{href}]"
        return f"{label} [->{href}]"

    b = re.sub(r'<a [^>]*href="([^"]*)"[^>]*>(.*?)</a>', link, b, flags=re.S)
    b = re.sub(r"</(p|li|tr|div|ul|table|section)>", "\n", b)
    b = re.sub(r"<[^>]+>", "", b)
    return html.unescape(re.sub(r"\n{3,}", "\n\n", b)).strip()


def main() -> int:
    if len(sys.argv) >= 2 and sys.argv[1] == "--words":
        w = build_words()
        WORDS.write_text("\n".join(sorted(w)), encoding="utf-8")
        print(f"{len(w)} identifier words indexed -> {WORDS}")
        return 0
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    rel = sys.argv[1]
    src = DEV / rel
    raw = src.read_text(encoding="utf-8")
    words = load_words()
    files = set(git("ls-tree", "-r", "--name-only", TARGET).splitlines())
    dirs = {"/".join(f.split("/")[:i]) for f in files for i in range(1, len(f.split("/")))}
    status, renames, numstat = delta()

    cited = []
    for kind, rev, path in re.findall(r'https://github\.com/libcna/cna/(blob|tree)/([0-9a-f]{40})/([^"#]+)', raw):
        if (path, kind) not in cited:
            cited.append((path, kind))
    print(f"# Verification pack: {rel}")
    print(f"- Developer pin: `{DEV_PIN[:8]}`   TARGET: `{TARGET[:8]}`   (55-commit delta; see below)")
    dirty = subprocess.run(["git", "-C", str(DEV), "status", "--short", "--", rel], capture_output=True,
                           text=True).stdout.strip()
    print(f"- Developer working-tree state for this file: {dirty or 'clean (committed)'}")
    print(f"- Cited CNA paths: {len(cited)}")
    print()
    print("## Cited paths vs TARGET")
    print("| path | at TARGET | changed since Developer pin | +/- lines |")
    print("|---|---|---|---|")
    missing = []
    changed = []
    for path, kind in cited:
        clean = path.rstrip("/")
        present = clean in files if kind == "blob" else clean in dirs
        if kind == "tree":
            ch = [f for f in status if f.startswith(clean + "/")]
            st = f"{len(ch)} file(s) changed" if ch else "-"
            ns = ""
        else:
            st = status.get(clean, "-")
            if st == "R":
                st = f"renamed -> {renames[clean]}"
            ns = f"+{numstat[clean][0]}/-{numstat[clean][1]}" if clean in numstat else ""
        if not present:
            missing.append(clean)
        if st != "-" and not st.endswith("changed") or st.endswith("changed") and not st.startswith("0"):
            if st != "-":
                changed.append(clean)
        print(f"| `{clean}` | {'yes' if present else '**MISSING**'} | {st} | {ns} |")
    print()
    print(f"**Missing at TARGET: {len(missing)}**; **changed since Developer pin: {len(changed)}**")
    if changed:
        print("\nRe-verify every claim about these with `git -C ../cna diff "
              f"{DEV_PIN[:8]} {TARGET[:8]} -- <path>` (or read the file at TARGET):")
        for c in changed:
            print(f"- {c}")
    print()

    print("## Code tokens with identifier parts absent from the TARGET tree (candidates for stale/invented)")
    tokens = []
    for tok in re.findall(r"<code>(.*?)</code>", raw, re.S):
        t = html.unescape(re.sub(r"<[^>]+>", "", tok)).strip()
        if t and t not in tokens:
            tokens.append(t)
    absent = []
    for t in tokens:
        parts = [p for p in IDENT.findall(t) if len(p) >= 4 and not p.isdigit()]
        miss = [p for p in parts if p not in words]
        if miss:
            absent.append((t, miss))
    if absent:
        for t, miss in absent:
            print(f"- `{t}`  (unseen: {', '.join(miss)})")
    else:
        print("- none")
    print(f"\n({len(tokens)} distinct code tokens scanned; third_party/vendor are not in the index, so a token that "
          "belongs to a vendored library shows up here: check it with `git grep` before treating it as stale.)")
    print()

    commits = re.findall(r"libcna/cna/commit/([0-9a-f]{40})", raw)
    if commits:
        print("## Cited commits")
        for c in dict.fromkeys(commits):
            ok = subprocess.run(["git", "-C", str(CNA), "merge-base", "--is-ancestor", c, TARGET]).returncode == 0
            print(f"- `{c[:10]}` ancestor of TARGET: {'yes' if ok else '**NO**'}")
        print()
    ext = sorted(set(re.findall(r'https://github\.com/libcna/(cna-[a-z]+)/blob/([0-9a-f]{40})/([^"#]+)', raw)))
    if ext:
        print("## External repository pins cited (verify against the local sibling checkout at that commit)")
        for repo, rev, path in ext:
            print(f"- {repo}@{rev[:8]}: {path}")
        print()

    print("## Page text (cited CNA paths shown as [@path])")
    print(page_text(raw))
    return 0


if __name__ == "__main__":
    sys.exit(main())
