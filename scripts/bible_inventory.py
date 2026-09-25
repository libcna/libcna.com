#!/usr/bin/env python3
"""Mechanical enumeration of the CNA Bible's canonical source graph (Phase 3).

    bible_inventory.py            # write audit/data/bible/units.json and print a summary
    bible_inventory.py --list     # print the unit list only

The Bible repository (default ../bible.libcna.com, override with BIBLE_REPO) is READ-ONLY.  Its *working tree* is
read, not Git HEAD, because the frozen tree holds uncommitted synchronisation work that the generated HTML/PDF lack.

The graph is derived, never typed: start at latex/book/main.tex and follow every \\input{...} recursively
(chapters, front matter, appendices, nested fragments, figure sources).  Each reached file is a *unit*:

  kind = front | chapter | appendix | fragment | figure

plus the raster images the manuscript includes (\\includegraphics) as *asset* units, and the auxiliary evidence /
planning documents (cnabugs.md, audit/*.md, ...) as *aux* units.  Every unit carries its Bible git state, size, and the
list of structural headings (\\chapter/\\section/\\subsection/\\subsubsection/\\paragraph-with-title) that a ledger
record must account for.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BIBLE = Path(os.environ.get("BIBLE_REPO", ROOT.parent / "bible.libcna.com"))
BOOK = BIBLE / "latex" / "book"
OUT = ROOT / "audit" / "data" / "bible" / "units.json"

INPUT_RX = re.compile(r"\\input\{([^}]+)\}")
HEAD_RX = re.compile(r"\\(chapter|section|subsection|subsubsection)\*?(?:\[[^\]]*\])?\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}")
GFX_RX = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}")
LABEL_RX = re.compile(r"\\label\{([^}]+)\}")


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(BIBLE), *args], check=True, capture_output=True, text=True).stdout


def git_state() -> dict[str, str]:
    """path (repo-relative) -> ' M' | '??' | ...  for the whole working tree."""
    out = {}
    for line in git("status", "--short", "--untracked-files=all").splitlines():
        out[line[3:]] = line[:2].strip() or "clean"
    return out


def diff_stats() -> dict[str, tuple[int, int]]:
    out: dict[str, tuple[int, int]] = {}
    for line in git("diff", "--numstat", "HEAD").splitlines():
        a, d, p = line.split("\t", 2)
        if a.isdigit() and d.isdigit():
            out[p] = (int(a), int(d))
    return out


def strip_comments(text: str) -> str:
    return re.sub(r"(?<!\\)%.*", "", text)


def clean_title(s: str) -> str:
    s = re.sub(r"\\(?:texttt|cnaclass|cnans|repolink|emph|textbf|textit)\{([^{}]*)\}", r"\1", s)
    s = re.sub(r"\\[a-zA-Z]+\*?", "", s)
    s = s.replace("{", "").replace("}", "").replace("~", " ").replace("\\", "")
    return re.sub(r"\s+", " ", s).strip()


def prose_words(text: str) -> int:
    t = strip_comments(text)
    t = re.sub(r"\\begin\{(lstlisting|verbatim)\}.*?\\end\{\1\}", " ", t, flags=re.S)
    t = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?", " ", t)
    return len(re.findall(r"[A-Za-z][A-Za-z0-9_'’-]*", t))


def scan(rel: str, text: str) -> dict:
    body = strip_comments(text)
    heads = []
    for m in HEAD_RX.finditer(body):
        line = body.count("\n", 0, m.start()) + 1
        heads.append({"level": m.group(1), "title": clean_title(m.group(2)), "line": line})
    return {
        "headings": heads,
        "sections": sum(1 for h in heads if h["level"] == "section"),
        "subsections": sum(1 for h in heads if h["level"] in ("subsection", "subsubsection")),
        "listings": len(re.findall(r"\\begin\{(?:lstlisting|verbatim)\}|\\lstinputlisting|\\begin\{cnacpp|\\begin\{cnashell", text)),
        "tables": len(re.findall(r"\\begin\{(?:tabular|longtable|tabularx|tabulary)\}", text)),
        "figures_inline": len(re.findall(r"\\begin\{(?:figure|tikzpicture)\}", text)),
        "sourcenotes": len(re.findall(r"\\begin\{sourcenote\}", text)),
        "labels": LABEL_RX.findall(text),
        "input_children": [m for m in INPUT_RX.findall(body)],
        "graphics": GFX_RX.findall(body),
    }


def walk(rel: str, seen: list[str], parents: dict[str, str]) -> None:
    p = BOOK / rel
    if not p.exists():
        raise SystemExit(f"main.tex graph references a missing file: {rel}")
    if rel in seen:
        return
    seen.append(rel)
    text = p.read_text(encoding="utf-8")
    for child in INPUT_RX.findall(strip_comments(text)):
        if child.startswith("../common/"):
            continue
        if not child.endswith(".tex"):
            child += ".tex"
        if child not in parents:
            parents[child] = rel
        walk(child, seen, parents)


def classify(rel: str) -> str:
    if rel.startswith("front/"):
        return "front"
    if rel.startswith("figures/"):
        return "figure"
    if "/appendices/" in rel:
        return "appendix"
    if "/fragments/" in rel:
        return "fragment"
    return "chapter"


def unit_id(rel: str) -> str:
    return re.sub(r"\.tex$", "", Path(rel).name)


def main() -> int:
    list_only = "--list" in sys.argv
    main_tex = BOOK / "main.tex"
    seen: list[str] = []
    parents: dict[str, str] = {}
    walk("main.tex", seen, parents)
    seen = [s for s in seen if s != "main.tex"]

    state = git_state()
    stats = diff_stats()
    part_of: dict[str, str] = {}
    part_no = None
    part_title = ""
    order_main: list[str] = []
    for raw in strip_comments(main_tex.read_text(encoding="utf-8")).splitlines():
        m = re.match(r"\\part\{(.*)\}", raw.strip())
        if m:
            part_title = clean_title(m.group(1))
            part_no = (part_no or 0) + 1
        if raw.strip().startswith("\\appendix"):
            part_title, part_no = "Appendices", None
        if raw.strip().startswith("\\frontmatter"):
            part_title, part_no = "Front matter", None
        for c in INPUT_RX.findall(raw):
            if c.startswith("../common/"):
                continue
            c = c if c.endswith(".tex") else c + ".tex"
            part_of[c] = (f"Part {part_no}: {part_title}" if part_no else part_title)
            order_main.append(c)

    # figures are reached through chapters; keep them after the file that includes them
    units = []
    for rel in seen:
        p = BOOK / rel
        text = p.read_text(encoding="utf-8")
        info = scan(rel, text)
        repo_rel = "latex/book/" + rel
        gs = state.get(repo_rel, "clean")
        added, deleted = stats.get(repo_rel, (0, 0))
        kind = classify(rel)
        parent = parents.get(rel, "main.tex")
        chapter_title = next((h["title"] for h in info["headings"] if h["level"] == "chapter"), "")
        name = Path(rel).stem
        cn = re.match(r"ch(\d+)", name)
        units.append({
            "id": unit_id(rel),
            "kind": kind,
            "path": repo_rel,
            "part": part_of.get(rel) or part_of.get(parent) or "",
            "chapter_number": int(cn.group(1)) if cn else None,
            "title": chapter_title or name,
            "included_by": "main.tex" if parent == "main.tex" else parent,
            "order": len(units) + 1,
            "bytes": len(text.encode()),
            "lines": text.count("\n") + 1,
            "prose_words": prose_words(text),
            "git_state": gs,
            "diff_added": added,
            "diff_deleted": deleted,
            "headings": info["headings"],
            "sections": info["sections"],
            "subsections": info["subsections"],
            "listings": info["listings"],
            "tables": info["tables"],
            "figures_inline": info["figures_inline"],
            "sourcenotes": info["sourcenotes"],
            "labels": info["labels"],
            "graphics": info["graphics"],
        })

    assets = []
    seen_assets = set()
    for u in units:
        for g in u["graphics"]:
            key = g
            if key in seen_assets:
                continue
            seen_assets.add(key)
            cand = [BOOK / g] + [BOOK / (g + ext) for ext in (".png", ".pdf", ".jpg", ".svg")] + \
                   [BOOK / "images" / Path(g).name]
            found = next((c for c in cand if c.is_file()), None)
            repo_rel = ("latex/book/" + found.relative_to(BOOK).as_posix()) if found else None
            assets.append({"id": Path(g).stem, "kind": "asset", "path": repo_rel, "included_by": u["id"],
                           "bytes": found.stat().st_size if found else 0, "git_state": state.get(repo_rel or "", "clean")})
    # every image on disk that is not referenced is still reported (it may be dead weight)
    on_disk = {p.relative_to(BOOK).as_posix() for p in (BOOK / "images").glob("*")}
    referenced = {a["path"].replace("latex/book/", "") for a in assets if a["path"]}
    orphans = sorted(on_disk - referenced)

    def md_headings(path: Path, levels: tuple[str, ...]) -> list[dict]:
        out = []
        fence = False
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if line.startswith("```"):
                fence = not fence
            if fence:
                continue
            m = re.match(r"(#{2,3}) (.+?)\s*$", line)
            if m and m.group(1) in levels:
                out.append({"level": "section" if m.group(1) == "##" else "subsection",
                            "title": re.sub(r"[`*_]", "", m.group(2)).strip(), "line": n})
        return out

    aux = []
    aux_spec = [
        ("cnabugs.md", "bugs", "Current defect ledger; every active item must be re-verified at TARGET"),
        ("AUDIT.md", "audit", "Curated feature matrix and documentation-staleness log"),
        ("EDITORIAL-AUDIT.md", "audit", "Editorial audit: terminology, evidence taxonomy, claims discipline"),
        ("PLAN.md", "plan", "Expansion plan, methodology, session log"),
        ("NEXT.md", "plan", "Current-state handoff"),
        ("PROGRESS.md", "plan", "Historical progress log"),
        ("README.md", "readme", "Repository overview"),
        ("CLAUDE.md", "guide", "Authoring methodology for the manuscript"),
    ]
    for name, cat, note in aux_spec:
        p = BIBLE / name
        if p.exists():
            levels = ("##", "###") if name == "cnabugs.md" else ("##",)
            aux.append({"id": "aux-" + Path(name).stem.lower(), "kind": "aux", "category": cat, "path": name, "note": note,
                        "bytes": p.stat().st_size, "git_state": state.get(name, "clean"),
                        "headings": md_headings(p, levels)})
    for p in sorted((BIBLE / "audit").glob("*.md")):
        rel = p.relative_to(BIBLE).as_posix()
        aux.append({"id": "aux-audit-" + p.stem.lower(), "kind": "aux", "category": "subsystem-audit", "path": rel,
                    "note": "Read-only source audit that the manuscript was written from",
                    "bytes": p.stat().st_size, "git_state": state.get(rel, "clean"),
                    "headings": md_headings(p, ("##",))})

    doc = {
        "meta": {
            "bible_repo": str(BIBLE),
            "bible_head": git("rev-parse", "HEAD").strip(),
            "bible_branch": git("branch", "--show-current").strip(),
            "bible_cnahead": (BIBLE / "cnahead").read_text().strip() if (BIBLE / "cnahead").exists() else "",
            "bible_dirty_paths": len(state),
            "main_tex_inputs": len(order_main),
            "graph_files": len(seen),
            "orphan_images": orphans,
            "note": "Derived by scripts/bible_inventory.py from the Bible WORKING TREE (uncommitted work included).",
        },
        "units": units,
        "assets": assets,
        "aux": aux,
    }
    if list_only:
        for u in units:
            print(f"{u['order']:3d} {u['kind']:8s} {u['id']:44s} {u['prose_words']:6d}w {u['git_state']:>5s}  {u['part']}")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    kinds: dict[str, int] = {}
    for u in units:
        kinds[u["kind"]] = kinds.get(u["kind"], 0) + 1
    print(f"Bible HEAD {doc['meta']['bible_head'][:8]} ({doc['meta']['bible_branch']}), cnahead {doc['meta']['bible_cnahead'][:8]}, "
          f"{doc['meta']['bible_dirty_paths']} dirty paths")
    print("tex units:", len(units), kinds, "| main.tex inputs:", len(order_main), "| assets:", len(assets),
          "| orphan images:", len(orphans), "| aux:", len(aux))
    print("prose words:", sum(u["prose_words"] for u in units), "| headings:", sum(len(u["headings"]) for u in units))
    print("->", OUT.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
