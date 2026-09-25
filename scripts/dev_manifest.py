#!/usr/bin/env python3
"""Structure of the Development area (Phase 2): groups, pages, and their Developer sources.

This module is data only. It is the single description of

  * which pages exist under development/ and in which order the local sidebar lists them
    (consumed by site_dev.py),
  * which developer.libcna.com page each one absorbs, if any (consumed by
    check_developer_absorption.py, which cross-checks the absorption ledger).

A page is a dict:  path (site-relative), title, label (short sidebar text), dev (developer.libcna.com
source file or None for a page that has no single Developer counterpart), kind
("migrated" | "new" | "generated" | "hub").
"""

from __future__ import annotations

DEV_ROOT = "development"


def P(path: str, title: str, label: str, dev: str | None = None, kind: str = "migrated") -> dict:
    return {"path": path, "title": title, "label": label, "dev": dev, "kind": kind}


# --------------------------------------------------------------------------------------
# Groups, in sidebar order. `landing` is the group's first page. `crumbs` are the breadcrumb
# segments between "Development" and the page itself (label, site-relative path).
# --------------------------------------------------------------------------------------
GROUPS: list[dict] = [
    {
        "key": "home", "label": "Development home", "crumbs": [],
        "pages": [
            P("development/index.html", "Development", "Development home", "index.html", "hub"),
            P("development/getting-started.html", "Getting started as a maintainer", "Getting started",
              "getting-started/index.html"),
        ],
    },
    {
        "key": "handbook", "label": "Maintainer Handbook",
        "crumbs": [("Maintainer Handbook", "development/handbook/index.html")],
        "pages": [
            P("development/handbook/index.html", "Maintainer Handbook", "Handbook home", None, "hub"),
            P("development/handbook/change-map.html", "I want to change… (change map)", "Change map",
              "change-map/index.html"),
            P("development/handbook/fix-a-renderer-bug.html", "I need to fix a renderer bug", "Fix a renderer bug",
              None, "new"),
            P("development/handbook/change-public-xna-behavior.html", "I need to change public XNA behavior",
              "Change public XNA behavior", None, "new"),
            P("development/handbook/modify-a-platform-backend.html", "I need to modify a platform backend",
              "Modify a platform backend", None, "new"),
            P("development/handbook/add-a-regression-test.html", "I need to add a regression test",
              "Add a regression test", None, "new"),
            P("development/handbook/modify-contentmanager.html", "I need to modify ContentManager",
              "Modify ContentManager", None, "new"),
            P("development/handbook/modify-the-content-pipeline.html", "I need to modify the Content Pipeline",
              "Modify the Content Pipeline", None, "new"),
            P("development/handbook/update-the-c-api.html", "I need to update the C API", "Update the C API",
              None, "new"),
            P("development/handbook/debug-shutdown-and-lifetime.html",
              "I need to debug shutdown and lifetime behavior", "Debug shutdown / lifetime", None, "new"),
            P("development/handbook/investigate-a-sample-failure.html", "I need to investigate a sample failure",
              "Investigate a sample failure", None, "new"),
            P("development/handbook/change-build-configuration.html", "I need to change build configuration",
              "Change build configuration", None, "new"),
            P("development/handbook/make-a-release.html", "I need to make a release", "Make a release",
              None, "new"),
            P("development/handbook/update-libcna-com.html", "I need to update libcna.com after CNA changes",
              "Update libcna.com", None, "new"),
            P("development/handbook/conventions.html", "Conventions", "Conventions", "conventions/index.html"),
        ],
    },
    {
        "key": "takeover", "label": "Human Takeover",
        "crumbs": [("Human Takeover", "development/takeover/index.html")],
        "pages": [
            P("development/takeover/index.html", "Take engineering ownership of CNA", "Takeover home",
              "takeover/index.html", "hub"),
            P("development/takeover/inherited.html", "What a human maintainer inherits", "What you inherited",
              "takeover/inherited.html"),
            P("development/takeover/mental-model.html", "The canonical mental model", "Mental model",
              "takeover/mental-model.html"),
            P("development/takeover/own-a-subsystem.html", "Choose one subsystem and own it", "Own a subsystem",
              None, "new"),
            P("development/takeover/curriculum.html", "First 10, 50 and 100 hours with CNA",
              "First 10 / 50 / 100 hours", "takeover/curriculum.html"),
            P("development/takeover/investigation.html", "How to understand code you did not write",
              "Investigate unknown code", "takeover/investigation.html"),
            P("development/takeover/worked-changes.html", "Worked human changes", "Worked changes",
              "takeover/worked-changes.html"),
            P("development/takeover/case-study-components.html", "Case study: Game component lifetime",
              "Case study: components", "takeover/case-study-components.html"),
            P("development/takeover/case-study-storage.html", "Case study: storage containment",
              "Case study: storage", "takeover/case-study-storage.html"),
            P("development/takeover/review-ai-generated-code.html",
              "Review large AI-generated areas without trusting them", "Review AI-era code", None, "new"),
            P("development/takeover/ownership.html", "Ownership and lifetime master map", "Ownership map",
              "takeover/ownership.html"),
            P("development/takeover/threading.html", "Thread and callback map", "Threads & callbacks",
              "takeover/threading.html"),
            P("development/takeover/blast-radius.html", "Blast radius and readiness", "Blast radius",
              "takeover/blast-radius.html"),
            P("development/takeover/validation.html", "What to test after changing X", "What must I test?",
              "takeover/validation.html"),
            P("development/takeover/xna-oracle.html", "Using the XNA oracle as evidence", "XNA oracle", None, "new"),
            P("development/takeover/uncertainty.html", "Known uncertainty and history", "Uncertainty & history",
              "takeover/uncertainty.html"),
        ],
    },
    {
        "key": "repository", "label": "Repository & Ownership",
        "crumbs": [("Repository & Ownership", "development/repository/index.html")],
        "pages": [
            P("development/repository/index.html", "Repository map", "Repository map", "repository/index.html",
              "hub"),
            P("development/repository/source-ownership.html", "Source ownership: which part of CNA owns this?",
              "Source ownership", None, "new"),
            P("development/repository/module-graph.html", "Physical module dependency map", "Module graph",
              "architecture/module-graph.html"),
        ],
    },
    {
        "key": "build", "label": "Build System",
        "crumbs": [("Build System", "development/build/index.html")],
        "pages": [
            P("development/build/index.html", "Build system", "Build system home", "build/index.html", "hub"),
            P("development/build/architecture.html", "CMake architecture", "CMake architecture",
              "build/architecture.html"),
        ],
    },
    {
        "key": "testing", "label": "Testing",
        "crumbs": [("Testing", "development/testing/index.html")],
        "pages": [
            P("development/testing/index.html", "Testing handbook", "Testing home", "testing/index.html", "hub"),
            P("development/testing/architecture.html", "Test architecture and change recipes",
              "Test architecture", "testing/architecture.html"),
        ],
    },
    {
        "key": "debugging", "label": "Debugging", "crumbs": [],
        "pages": [P("development/debugging.html", "Debugging cookbook", "Debugging cookbook",
                    "debugging/index.html")],
    },
    {
        "key": "workflows", "label": "Workflows", "crumbs": [],
        "pages": [P("development/workflows.html", "Working on CNA", "Working on CNA", "workflows/index.html")],
    },
    {
        "key": "invariants", "label": "Invariants", "crumbs": [],
        "pages": [P("development/invariants.html", "Architectural invariants", "Architectural invariants",
                    "invariants/index.html")],
    },
    {
        "key": "architecture", "label": "Architecture Maps",
        "crumbs": [("Architecture Maps", "development/architecture/overview.html")],
        "pages": [
            P("development/architecture/overview.html", "Architecture overview", "Overview",
              "architecture/overview.html", "hub"),
            P("development/architecture/runtime.html", "Runtime lifecycle", "Runtime lifecycle",
              "architecture/runtime.html"),
            P("development/architecture/platform.html", "Platform architecture", "Platform layer",
              "architecture/platform.html"),
            P("development/architecture/graphics.html", "Graphics architecture", "Graphics",
              "architecture/graphics.html"),
            P("development/architecture/content.html", "Content architecture", "Content",
              "architecture/content.html"),
            P("development/architecture/audio-input.html", "Audio and input architecture", "Audio & input",
              "architecture/audio-input.html"),
            P("development/architecture/bindings.html", "C API and bindings architecture", "C API & bindings",
              "architecture/bindings.html"),
        ],
    },
    {
        "key": "internals", "label": "Internals overview",
        "crumbs": [("Internals", "development/internals/index.html")],
        "pages": [P("development/internals/index.html", "Internals", "Internals home", None, "hub")],
    },
    {
        "key": "runtime", "label": "Runtime internals",
        "crumbs": [("Internals", "development/internals/index.html"),
                   ("Runtime", "development/internals/runtime/module.html")],
        "pages": [
            P("development/internals/runtime/module.html", "Runtime module internals", "Runtime module",
              "runtime/module.html", "hub"),
            P("development/internals/runtime/startup.html", "Startup source trace", "Startup trace",
              "runtime/startup.html"),
            P("development/internals/runtime/frame.html", "One frame source trace", "One frame trace",
              "runtime/frame.html"),
            P("development/internals/runtime/shutdown.html", "Ownership and shutdown", "Shutdown trace",
              "runtime/shutdown.html"),
        ],
    },
    {
        "key": "graphics", "label": "Graphics internals",
        "crumbs": [("Internals", "development/internals/index.html"),
                   ("Graphics", "development/internals/graphics/selection.html")],
        "pages": [
            P("development/internals/graphics/selection.html", "Renderer selection internals",
              "Renderer selection", "graphics/selection.html", "hub"),
            P("development/internals/graphics/device.html", "GraphicsDevice internals",
              "GraphicsDevice & contract", "graphics/device.html"),
            P("development/internals/graphics/draw-call.html", "Indexed draw trace", "Indexed draw trace",
              "graphics/draw-call.html"),
            P("development/internals/graphics/resources.html", "Textures and render targets",
              "Textures & render targets", "graphics/resources.html"),
            P("development/internals/graphics/backends.html", "Graphics backends", "Renderer family map",
              "graphics/backends.html"),
            P("development/internals/graphics/easygl.html", "EasyGL renderer internals", "EasyGL",
              "graphics/easygl.html"),
            P("development/internals/graphics/vulkan.html", "Vulkan renderer internals", "Vulkan",
              "graphics/vulkan.html"),
            P("development/internals/graphics/opengl4.html", "OpenGL4 renderer internals", "OpenGL4",
              None, "new"),
            P("development/internals/graphics/sdl-gpu.html", "SDL_gpu renderer internals", "SDL_gpu",
              "graphics/sdl-gpu.html"),
            P("development/internals/graphics/software.html", "Software renderer internals", "Software",
              "graphics/software.html"),
            P("development/internals/graphics/headless.html", "Headless renderer internals", "Headless",
              "graphics/headless.html"),
            P("development/internals/graphics/stub.html", "Stub renderer internals", "Stub",
              "graphics/stub.html"),
        ],
    },
    {
        "key": "platforms", "label": "Platform internals",
        "crumbs": [("Internals", "development/internals/index.html"),
                   ("Platforms", "development/internals/platforms/index.html")],
        "pages": [
            P("development/internals/platforms/index.html", "Platform backends", "Platform backends",
              "platforms/index.html", "hub"),
            P("development/internals/platforms/sdl3.html", "SDL3 platform internals", "SDL3",
              "platforms/sdl3.html"),
            P("development/internals/platforms/sdl2.html", "SDL2 platform internals", "SDL2",
              "platforms/sdl2.html"),
            P("development/internals/platforms/x11.html", "X11 platform internals", "X11", "platforms/x11.html"),
            P("development/internals/platforms/wayland.html", "Wayland platform internals", "Wayland",
              "platforms/wayland.html"),
            P("development/internals/platforms/win32.html", "Win32 platform internals", "Win32",
              "platforms/win32.html"),
            P("development/internals/platforms/headless.html", "Headless platform internals", "Headless",
              "platforms/headless.html"),
            P("development/internals/platforms/terminal.html", "Terminal platform internals", "Terminal",
              "platforms/terminal.html"),
        ],
    },
    {
        "key": "audio", "label": "Audio internals",
        "crumbs": [("Internals", "development/internals/index.html"),
                   ("Audio", "development/internals/audio/engine.html")],
        "pages": [P("development/internals/audio/engine.html", "Audio engine internals",
                    "Mixer, voices & devices", "audio/engine.html")],
    },
    {
        "key": "content", "label": "Content internals",
        "crumbs": [("Internals", "development/internals/index.html"),
                   ("Content", "development/internals/content/runtime.html")],
        "pages": [
            P("development/internals/content/runtime.html", "Content runtime internals",
              "ContentManager & formats", "content/runtime.html", "hub"),
            P("development/internals/content/pipeline.html", "Content pipeline internals",
              "Build-time pipeline", "content/pipeline.html"),
        ],
    },
    {
        "key": "input", "label": "Input internals",
        "crumbs": [("Internals", "development/internals/index.html"),
                   ("Input", "development/internals/input/events.html")],
        "pages": [P("development/internals/input/events.html", "Input internals", "Events & snapshots",
                    "input/events.html")],
    },
    {
        "key": "modules", "label": "Module internals",
        "crumbs": [("Internals", "development/internals/index.html"),
                   ("Modules", "development/internals/modules/core.html")],
        "pages": [
            P("development/internals/modules/core.html", "Core module internals", "Core", "modules/core.html",
              "hub"),
            P("development/internals/modules/math.html", "Math module internals", "Math", "modules/math.html"),
            P("development/internals/modules/design.html", "Design converter internals", "Design converters",
              "modules/design.html"),
            P("development/internals/modules/storage.html", "Storage internals", "Storage",
              "modules/storage.html"),
            P("development/internals/modules/media.html", "Media internals", "Media", "modules/media.html"),
            P("development/internals/modules/video-ffmpeg.html", "FFmpeg video boundary", "FFmpeg video",
              "modules/video-ffmpeg.html"),
            P("development/internals/modules/devices.html", "Devices and sensor lifetime", "Devices & sensors",
              "modules/devices.html"),
            P("development/internals/modules/devices-ext.html", "Device extensions and host services",
              "Device host services", "modules/devices-ext.html"),
            P("development/internals/modules/diagnostics.html", "Diagnostics and profiler internals",
              "Diagnostics", "modules/diagnostics.html"),
            P("development/internals/modules/inspector.html", "Inspector transport internals", "Inspector",
              "modules/inspector.html"),
            P("development/internals/modules/phone.html", "Phone compatibility internals", "Phone",
              "modules/phone.html"),
            P("development/internals/modules/gamer-services.html", "Gamer services internals",
              "Gamer services", "modules/gamer-services.html"),
            P("development/internals/modules/graphics-ext.html", "Graphics extension pipeline internals",
              "Graphics extensions", "modules/graphics-ext.html"),
            P("development/internals/modules/net.html", "Network session internals", "Network sessions",
              "modules/net.html"),
        ],
    },
    {
        "key": "bindings", "label": "C API & bindings internals",
        "crumbs": [("Internals", "development/internals/index.html"),
                   ("C API & bindings", "development/internals/bindings/c-api-internals.html")],
        "pages": [
            P("development/internals/bindings/c-api-internals.html", "C API internals", "C ABI ownership & errors",
              "bindings/c-api-internals.html", "hub"),
            P("development/internals/bindings/csharp.html", "C# binding internals", "C# binding",
              "bindings/csharp.html"),
            P("development/internals/bindings/java.html", "Java binding internals", "Java binding",
              "bindings/java.html"),
            P("development/internals/bindings/python.html", "Python binding internals", "Python binding",
              "bindings/python.html"),
        ],
    },
    {
        "key": "reference", "label": "Generated References",
        "crumbs": [("Generated References", "development/reference/index.html")],
        "pages": [
            P("development/reference/index.html", "Generated references", "Reference index",
              "reference/index.html", "hub"),
            P("development/reference/modules.html", "Module index", "Modules", "reference/modules.html",
              "generated"),
            P("development/reference/cmake-options.html", "CMake option index", "CMake options",
              "reference/cmake-options.html", "generated"),
            P("development/reference/test-targets.html", "Test target index", "Test targets",
              "reference/test-targets.html", "generated"),
            P("development/reference/public-headers.html", "Public header index", "Public headers",
              "reference/public-headers.html", "generated"),
            P("development/reference/selection-axes.html", "Selection axes index", "Selection axes", None,
              "generated"),
        ],
    },
    {
        "key": "maintenance", "label": "Maintenance & Releases", "crumbs": [],
        "pages": [P("development/maintenance.html", "Maintaining these pages", "Maintenance & pin policy",
                    "maintenance/index.html")],
    },
]

SEE_ALSO_LAYERS = ("guide", "architecture", "internals", "maintainer", "tests", "reference")


def all_pages() -> list[dict]:
    return [p for g in GROUPS for p in g["pages"]]


def page_index() -> dict[str, tuple[dict, dict]]:
    """path -> (group, page)"""
    return {p["path"]: (g, p) for g in GROUPS for p in g["pages"]}


def developer_map() -> dict[str, str]:
    """Developer source file -> libcna destination (only 1:1 migrated/hub/generated pages)."""
    return {p["dev"]: p["path"] for p in all_pages() if p["dev"]}


if __name__ == "__main__":  # quick self-check; `--list` prints the page plan
    import sys
    if "--list" in sys.argv:
        for g in GROUPS:
            print(f"[{g['key']}] {g['label']}")
            for p in g["pages"]:
                src = f"  <- developer:{p['dev']}" if p["dev"] else "  (new)"
                print(f"   {p['path']}  \"{p['title']}\"{src}")
        raise SystemExit(0)
    idx = page_index()
    assert len(idx) == len(all_pages()), "duplicate page paths in manifest"
    dev = [p["dev"] for p in all_pages() if p["dev"]]
    assert len(dev) == len(set(dev)), "a Developer source is mapped twice"
    print(f"{len(GROUPS)} groups, {len(idx)} pages, {len(dev)} mapped Developer sources")
