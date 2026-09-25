#!/usr/bin/env python3
"""Structure of the Deep Dives and Known Issues areas (Phase 3).

Data only.  Two areas share one page generator (site_deep.py):

  deep-dives/    long-form conceptual and semantic knowledge, absorbed from the CNA Bible after re-verification at TARGET
  known-issues/  current defects, functional gaps, platform limitations and verification gaps at TARGET

The GROUPS below are the fixed taxonomy (each group has a generated hub at <area>/<key>/index.html).  The individual pages are
NOT listed here: every work package declares its own pages in audit/data/deep-pages/<work-package>.json, so parallel authors never
edit a shared file.  A page record is

    {"path": "deep-dives/graphics/spritebatch-sorting.html", "title": "...", "label": "short sidebar text",
     "group": "graphics", "order": 40, "bible_units": ["ch13-spritebatch"]}

`order` sorts pages inside their group (ties break on title).  Group hubs and the area hub are generated, not authored.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES_DIR = ROOT / "audit" / "data" / "deep-pages"

# --------------------------------------------------------------------------------------
# Groups.  intro = one paragraph shown on the generated group hub and on the area hub card.
# --------------------------------------------------------------------------------------
DEEP_GROUPS: list[dict] = [
    {"key": "foundations", "label": "Foundations & compatibility",
     "intro": "What CNA is, how it relates to XNA and to the sibling projects, the vocabulary the rest of the site relies on, the CNAEXT extension policy, "
              "and the difference between representing an XNA API, matching its behaviour and proving that it matches."},
    {"key": "framework", "label": "Framework core",
     "intro": "The XNA-shaped core: Game and its lifecycle, services and components, the value types and their exact numeric semantics, geometry, colour and layout."},
    {"key": "build", "label": "Architecture & build",
     "intro": "How the source tree is partitioned into physical modules, which dependencies may point where and how that is enforced, and how configuration, "
              "dependencies and tools turn into a build."},
    {"key": "graphics", "label": "The graphics machine",
     "intro": "The renderer-independent graphics layer: GraphicsDevice, SpriteBatch, textures and render targets, state objects, stock effects, shaders, "
              "vertex streams and the capability model."},
    {"key": "renderers", "label": "Renderers",
     "intro": "The renderer contract, identity and selection, and the families that implement it: OpenGL profiles, modern GPU APIs, Direct3D, "
              "software and portable 2D, browser renderers and the diagnostic renderers."},
    {"key": "content", "label": "Content",
     "intro": "How content reaches a running game: ContentManager resolution, the XNB container and its type readers, CNB and CNJ, the build-time Content Pipeline "
              "and how hostile or malformed content is handled."},
    {"key": "models", "label": "Models, glTF & 3D",
     "intro": "Model and mesh runtime types, glTF import, GPU vertex packing, skinning and animation, the CNJ model toolchain and glTF conformance evidence."},
    {"key": "services", "label": "Input, audio, media & services",
     "intro": "Input, audio, media and video, sensors, host devices, gamer services, storage, networking and avatars: contracts, lifecycles, platform "
              "differences and limits."},
    {"key": "sharp-runtime", "label": "sharp-runtime",
     "intro": "The foundation library CNA is built on: its object model, namespaces, component consumption, parity philosophy and how it is verified."},
    {"key": "siblings", "label": "Sibling libraries",
     "intro": "EasyGL, MetaGL, FreeDirect and FreeAPI: what each owns, how CNA consumes it and where the boundaries are."},
    {"key": "platforms", "label": "Cross-platform engineering",
     "intro": "The cross-platform contract, Windows cross-compiling and Wine, the web build and its main loop, renderer evidence on the web, Android and Apple platforms."},
    {"key": "verification", "label": "Diagnostics & verification",
     "intro": "Diagnostics and the Inspector, the test architecture, counting discipline, oracles, hostile environments, continuous integration and how evidence is graded."},
    {"key": "practice", "label": "Porting & project practice",
     "intro": "Migration and porting practice, case studies, spec auditing, samples and examples, project conventions and the road ahead."},
    {"key": "reference", "label": "Reference matrices",
     "intro": "Quick references and matrices: core graphics, feature matrix, glossary, repository map, CNAEXT catalogue, ecosystem, verification tiers, glTF evidence and the native C API."},
]

ISSUE_GROUPS: list[dict] = [
    {"key": "bugs", "label": "Current bugs",
     "intro": "Defects that exist at the TARGET snapshot: behaviour that violates an intended or documented contract. Each one is source-pinned, has a stable CNA-BUG identifier and states what evidence exists."},
    {"key": "gaps", "label": "Functional gaps",
     "intro": "Functionality that is intentionally or currently incomplete or unsupported at TARGET. A gap is not a bug: nothing violates a contract; the contract is narrower than one might expect."},
    {"key": "limitations", "label": "Platform limitations",
     "intro": "Behaviour that differs or is unavailable because of a host, platform or toolchain constraint."},
    {"key": "verification-gaps", "label": "Verification gaps",
     "intro": "Implementations that exist but whose behaviour is not supported by enough evidence: absent tests, unexecuted lanes, unreviewed oracles."},
]

AREAS: dict[str, dict] = {
    "deep-dives": {"root": "deep-dives", "title": "Deep Dives", "hub": "deep-dives/index.html", "groups": DEEP_GROUPS,
                   "part_of": "CNA Deep Dives"},
    "known-issues": {"root": "known-issues", "title": "Known Issues", "hub": "known-issues/index.html", "groups": ISSUE_GROUPS,
                     "part_of": "CNA Known Issues"},
}

SEE_ALSO_LAYERS = ["guide", "architecture", "internals", "maintainer", "tests", "reference", "deep", "issues"]


def group_landing(area: str, key: str) -> str:
    return f"{AREAS[area]['root']}/{key}/index.html"


def area_of(path: str) -> str | None:
    for name, a in AREAS.items():
        if path == a["hub"] or path.startswith(a["root"] + "/"):
            return name
    return None


def load_pages() -> list[dict]:
    """All authored page records, from audit/data/deep-pages/*.json (each: {"pages": [...]})."""
    out: list[dict] = []
    if PAGES_DIR.is_dir():
        for f in sorted(PAGES_DIR.glob("*.json")):
            doc = json.loads(f.read_text(encoding="utf-8"))
            for p in doc.get("pages", []):
                p = dict(p)
                p["_file"] = f.name
                out.append(p)
    return out


def all_pages() -> list[dict]:
    """Authored pages plus the generated hubs, each with `area` and `group` keys resolved."""
    pages: list[dict] = []
    for name, a in AREAS.items():
        pages.append({"path": a["hub"], "title": a["title"], "label": f"{a['title']} home", "area": name, "group": None,
                      "order": -1, "kind": "hub"})
        for g in a["groups"]:
            pages.append({"path": group_landing(name, g["key"]), "title": g["label"], "label": g["label"], "area": name,
                          "group": g["key"], "order": -1, "kind": "hub"})
    try:
        import known_issues as _KI
        issue_pages = _KI.issue_pages()
    except Exception:  # noqa: BLE001  (no index yet)
        issue_pages = []
    for p in load_pages() + issue_pages:
        p = dict(p)
        area = area_of(p["path"])
        p["area"] = area
        p.setdefault("kind", "new")
        p.setdefault("label", p["title"])
        p.setdefault("order", 100)
        pages.append(p)
    return pages


def problems() -> list[str]:
    """Manifest consistency: duplicate paths, unknown groups, pages outside their group directory."""
    errs: list[str] = []
    seen: dict[str, str] = {}
    for p in all_pages():
        if p["path"] in seen and p.get("kind") != "hub":
            errs.append(f"duplicate page {p['path']} ({seen[p['path']]} and {p.get('_file')})")
        seen[p["path"]] = p.get("_file", "generated")
        if p.get("kind") == "hub":
            continue
        area = p.get("area")
        if area is None:
            errs.append(f"{p['path']} is not under any area root")
            continue
        keys = {g["key"] for g in AREAS[area]["groups"]}
        if p.get("group") not in keys:
            errs.append(f"{p['path']}: unknown group {p.get('group')!r} for area {area}")
        elif not p["path"].startswith(f"{AREAS[area]['root']}/{p['group']}/"):
            errs.append(f"{p['path']}: must live under {AREAS[area]['root']}/{p['group']}/")
        if p["path"].endswith("/index.html"):
            errs.append(f"{p['path']}: index.html is reserved for generated hubs")
    return errs


def page_index() -> dict[str, tuple[dict, dict]]:
    """path -> (group dict, page dict) in the shape site_dev.page_index() uses (group needs 'key' and 'label')."""
    idx: dict[str, tuple[dict, dict]] = {}
    for p in all_pages():
        area = p["area"]
        if p["group"]:
            g = next(x for x in AREAS[area]["groups"] if x["key"] == p["group"])
        else:
            g = {"key": "home", "label": AREAS[area]["title"] + " home"}
        idx[p["path"]] = (g, p)
    return idx


def group_pages(area: str, key: str) -> list[dict]:
    """Authored pages of one group, in display order (hub excluded)."""
    ps = [p for p in all_pages() if p["area"] == area and p["group"] == key and p.get("kind") != "hub"]
    return sorted(ps, key=lambda p: (p.get("order", 100), p["title"]))


if __name__ == "__main__":
    import sys
    if "--list" in sys.argv:
        for name, a in AREAS.items():
            print(f"[{name}]")
            for g in a["groups"]:
                ps = group_pages(name, g["key"])
                print(f"  {g['key']:18s} {len(ps):3d} pages  {g['label']}")
                for p in ps:
                    print(f"      {p['path']}  \"{p['title']}\"")
    errs = problems()
    for e in errs:
        print("PROBLEM", e)
    sys.exit(1 if errs else 0)
