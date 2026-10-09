#!/usr/bin/env python3
"""Regression fixtures for the semantic site validators.

The independent review of the c1c316b9 refresh found stale claims that every validator passed: a retired renderer
inside a longer list or a table row, retired platform backends in a compact source tree and in a "native sibling" link,
a CI statement contradicting the workflows, test-file counts from the previous snapshot, and a ledger token that kept a
section "anchored" while the renderer list beside it was false. Each REJECT fixture below is one of those sentences
(verbatim where the page had it) or the same shape, and must be rejected; each ALLOW fixture is a legitimate current
sentence of the same vocabulary (SDL's Direct3D 12 driver, SDL's Wayland video driver, a Windows host, native handles,
Weston and Xvfb, a number attributed to alpha.1) and must pass. The retired sets and CI facts are derived from the CNA
clone exactly as the validators derive them (../cna or $CNA_REPO), so the fixtures exercise the real configuration.

    test_validators.py        # exit 0 when every fixture behaves; validate_all.sh runs it first
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import adversarial_audit as AA  # noqa: E402
import check_facts as CF  # noqa: E402
import check_retired_platforms as RP  # noqa: E402
import check_retired_renderers as RR  # noqa: E402

RETIRED_R = RR.derive()
RETIRED_P = RP.retired_platforms()
CI = RP.ci_window_systems()
VALUES = CF.metric_values()
SHA_SHORT = (Path(__file__).resolve().parent.parent / "cnahead").read_text(encoding="utf-8").strip()[:8]


def renderer_problems(html: str) -> list[str]:
    return [why for why, _x, _c in RR.semantic_findings(html, RETIRED_R)] + [line for _n, line in RR.line_hits(html, RETIRED_R)]


def platform_problems(html: str) -> list[str]:
    out = [why for why, _x, _c in RP.semantic_findings(html, RETIRED_P, CI)]
    for line in html.splitlines():
        out += [why for rx, why in RP.patterns(RETIRED_P) if rx.search(line)]
    return out


def metric_problems(html: str) -> list[str]:
    return [msg for msg, _c in CF.page_claim_findings("docs/fixture.html", html, VALUES)] + CF.evidence_heading_findings(html, SHA_SHORT)


RENDERER_REJECT = [
    # development/internals/graphics/device.html at 835d161
    "<p>At this snapshot five families call it: DirectX 9, DirectX 11 and DirectX 12 report loss and reset; WebGPU reports them only from its debug simulation hooks.</p>",
    # development/handbook/add-a-regression-test.html at 835d161
    "<table><tr><th>Need</th><th>Mechanism</th></tr><tr><td>The same behaviour on several renderers</td><td>Every renderer that calls "
    "<code>cna_register_parity_fixtures()</code> registers <code>&lt;Prefix&gt;_Parity_&lt;name&gt;</code> automatically (EasyGL, WebGPU, SDL_GPU, DirectX 11 and DirectX 12)</td></tr></table>",
    # deep-dives/framework/window-and-device-manager.html at 835d161
    "<li>That hook is a no-op in the renderer interface; at this snapshot the DirectX 9, DirectX 11, DirectX 12, SDL GPU, EasyGL, FNA3D and Software families override it.</li>",
    # development/internals/platforms/headless.html at 835d161
    "<td>No window; only renderers that can run without a swap chain accept it (the property's documentation names the Direct3D 12 and SDL GPU renderers, and says Direct3D 11 and EasyGL throw from their constructors).</td>",
    # deep-dives/graphics/vertex-and-index-buffers.html at 835d161: a standalone table row
    "<table><thead><tr><th>Family</th><th><code>Discard</code></th></tr></thead><tbody><tr><td>EasyGL</td><td>Orphans the buffer</td></tr>"
    "<tr><td>Direct3D 12</td><td>All three options take the same path: a fresh allocation from a per-frame upload ring plus a copy</td></tr></tbody></table>",
    "<p>Renderers: DirectX11, DirectX12, Vulkan</p>",
    "<p>Renderers: DirectX 11, DirectX 12, Vulkan</p>",
    "<p>CNA renderers include Direct3D 12.</p>",
    "<p>The Windows renderers, including Direct3D 12, present through DXGI.</p>",
    "<p>The accepted renderer names are DIRECTX9, DIRECTX11 and Direct3D 12.</p>",
    "<p>CNA supports Direct3D 12 on Windows.</p>",
    "<p>The parity fixtures are registered for EasyGL, SDL_GPU, WebGPU, Direct3D 11 and Direct3D 12.</p>",
    "<p>The GL family: OpenGL ES 2, OPENGLES3, OPENGL33 and WebGL 1 share one EasyGL implementation.</p>",
    "<p>The browser renderers are WEBGL2, WEBGPU and the Canvas renderer.</p>",
]
RENDERER_ALLOW = [
    "<p>SDL_GPU uses SDL's Direct3D 12 driver on Windows.</p>",
    "<p>SDL_GPU can use SDL&rsquo;s Direct3D 12 driver.</p>",
    "<p>SDL_gpu dispatches internally to its Vulkan, Metal or Direct3D 12 driver, depending on the platform.</p>",
    "<p>SDL's Metal and Direct3D 12 drivers are code paths with narrower evidence than the Vulkan driver.</p>",
    "<p>CNA does not talk to Vulkan, Metal or the Direct3D 12 API here; SDL picks the native driver.</p>",
    "<p>WEBGPU does not pick the native GPU API itself: a Vulkan, Metal or Direct3D 12 device is chosen by wgpu-native.</p>",
    "<p>The 4,608-byte row is 256-byte aligned, which avoids Direct3D 12's slow unaligned texture-upload path.</p>",
    "<p>( SDL_GPU can also reach Direct3D 12 on Windows, as one of the drivers SDL's GPU API chooses from.)</p>",
    "<table><thead><tr><th>Host</th><th>SDL_gpu driver</th></tr></thead><tbody><tr><td>Linux</td><td>Vulkan</td></tr><tr><td>Windows</td><td>Direct3D 12</td></tr></tbody></table>",
    "<p>A browser build draws into an HTML canvas element.</p>",
    "<p>meta-gl exposes the GLES 2.0 entry points and WebGL 1/2 flags of the context.</p>",
]

PLATFORM_REJECT = [
    # architecture.html at 835d161: compact source tree
    "<pre>│   ├── platform/                     ← IPlatform; src/ Sdl3 X11 Wayland Win32 Terminal Headless</pre>",
    # development/internals/platforms/sdl3.html at 835d161
    '<dd><a href="index.html">Platform backends overview</a> &middot; <a href="sdl3.html">X11 (native sibling)</a> &middot; <a href="sdl3.html">Win32 (native sibling)</a></dd>',
    "<p>The Win32 native sibling owns its own message loop.</p>",
    # showcase.html at 835d161 (platform-ci.yml at cnahead runs SDL3 under a private headless Weston)
    "<p>the Windows Direct3D lanes remain manual and no workflow builds the C API library, runs a Wayland session or runs the XNA oracle corpus.</p>",
    # about.html at 835d161
    "<li><code>CNA_PLATFORM</code> now offers six implementations (<code>SDL3</code>, <code>X11</code>, <code>WAYLAND</code>, <code>WIN32</code>, <code>HEADLESS</code>, <code>TERMINAL</code>)</li>",
    # deep-dives/build/module-architecture.html at 835d161
    "<td>The module that links the native windowing and host libraries for the platform implementations (SDL3, Xlib, Wayland, Win32).</td>",
    "<p>the same policy applies under SDL3, X11, Wayland, Win32, HEADLESS and TERMINAL.</p>",
    "<p>CNA's Wayland backend reads the compositor's scale.</p>",
    "<p>This snapshot has an automatic Wine-executed Win32 lane.</p>",
    "<p>See modules/platform/src/X11 for the event pump.</p>",
    "<p>Configure with -DCNA_PLATFORM=WAYLAND.</p>",
]
PLATFORM_ALLOW = [
    "<p>SDL3 can run through the Wayland video driver.</p>",
    "<p>SDL's x11 driver on a private Xvfb and its wayland driver on a private headless Weston.</p>",
    "<p>Build on a Windows host with MSVC.</p>",
    "<p>The renderer receives the HWND, or Display* + XID, or wl_display* + wl_surface* (native window handles).</p>",
    "<p>SDL's Wayland backend ignores the request.</p>",
    "<p>Every CNA window, on Windows, X11, Wayland, macOS, iOS, Android and the web, is an SDL3 window.</p>",
    "<p>The retired WIN32, X11 and WAYLAND values say to use SDL3.</p>",
    "<p>A NativeWindowHandle names which of Win32, X11, Wayland, Cocoa, UIKit, Android, Web, Headless or Terminal its pointers belong to.</p>",
    "<p>no workflow builds the C API library, and the platform workflow covers X11 and Wayland only through SDL3 on a private Xvfb and a private headless Weston.</p>",
]

METRIC_REJECT = [
    # docs/building.html, features.html, about.html, contribute.html at 835d161
    "<p>This snapshot contains <strong>813 C++ test source files</strong> (821 of which contain a counted macro) and 11,380 statically declared definitions, counted by the same method as alpha.1's 568.</p>",
    "<p>This snapshot contains 813 C++ test source files (821 with a counted test macro) and 11,380 static GoogleTest-family definitions.</p>",
    "<p>821 files contain counted macros.</p>",
    # deep-dives/foundations/compatibility-and-evidence.html at 835d161
    "<p>The site's test figures (852 files, 11,380 GoogleTest-family definitions) are source counts.</p>",
    "<p>This snapshot contains 852 C++ test source files.</p>",
    "<li>The 18-identity, 14-family registry in cmake/RendererIdentities.cmake is strong structural evidence.</li>",
    "<li>The 18-identity, 12-family registry in cmake/RendererIdentities.cmake is strong structural evidence.</li>",
    "<p>CNA exposes 14 public identities over 14 renderer implementation families.</p>",
    "<p>renderers/ holds 14 implementation-family directories.</p>",
    "<p>Of the files, 821 of 813 test files contain a counted macro.</p>",
    "<p>Five identities share EasyGL, so the mapping is not one-to-one.</p>",
    "<p>the two 2D-only renderers refuse earlier</p>",
    "<p>FNA3D always, thirteen more identities behind default-OFF CNA_*_COMPILED_EFFECTS options.</p>",
    "<p>32 parity fixtures are registered for five renderer families.</p>",
    '<p>Not ready: the release gate reports 631 unmapped symbols.</p>',
    '<div class="callout callout--note dev-evidence"><p><strong>Evidence basis:</strong> source-verified at the pinned commit. Claims on this page were '
    'checked by reading the CNA source at commit <code>b0e97bb1</code>; nothing was built.</p></div>',
]
METRIC_ALLOW = [
    "<p>The source tree has 813 C++ test files and 11,380 statically discoverable GoogleTest-family definitions (781 files contain at least one; alpha.1 had 568 and 8,263).</p>",
    "<p>Since alpha.1 the set has been deliberately curated from 50 identities over 46 implementation families to 14 over 12.</p>",
    "<p>The previous snapshot, b0e97bb1, had 18 public identities over 14 implementation families and 852 C++ test source files.</p>",
    "<li>The 14-identity, 12-family registry in cmake/RendererIdentities.cmake is strong structural evidence.</li>",
    "<p>Compiled-effect support is 11 of the 14 identities in 9 implementation families.</p>",
    "<p>A default configure reports CompiledEffects false on 13 of the 14 identities.</p>",
    "<p>Storage has 14 statically discoverable GoogleTest-family definitions (alpha.1: five).</p>",
    "<p>one renderer's oracle result says nothing about the other 13 identities</p>",
    '<p>Quote the gate as committed: "Not ready, one criterion unmet: 631 public symbols are still unmapped".</p>',
    "<p>631 planned public C++ declarations do not yet have C mappings.</p>",
    "<table><tr><th>Area</th><th>Alpha.1</th><th>Snapshot</th></tr><tr><td>Renderers</td><td>50 public identities over 46 implementation families</td><td>14 over 12</td></tr></table>",
    '<div class="callout callout--note dev-evidence"><p><strong>Evidence basis:</strong> source-verified at the stated evidence commit. Claims on this page were '
    'checked by reading the CNA source at commit <code>b0e97bb1</code>; nothing was built.</p></div>',
]

# the ledger gate: a concept whose token survives must still fail when its cited section carries a rejected claim
STALE_SECTION_HTML = ("<h2 id='device-loss'>Device loss</h2><p><code>createRenderer()</code> hands every family a <code>deviceEventCallback</code>. "
                      "At this snapshot five families call it: DirectX 9, DirectX 11 and DirectX 12 report loss and reset.</p>")
CURRENT_SECTION_HTML = ("<h2 id='device-loss'>Device loss</h2><p><code>createRenderer()</code> hands every family a <code>deviceEventCallback</code>. "
                        "At this snapshot four families call it: DirectX 9 and DirectX 11 report loss and reset.</p>")


def ledger_result(section_html: str, concept: dict) -> list[str]:
    tree = AA.Tree()
    tree.feed(section_html)
    sec = AA._norm(AA.section_text(tree.ids["device-loss"]))

    def section_fn(page: str, frag: str) -> str:
        return sec

    def claims_fn(page: str) -> list[tuple[str, str]]:
        out = [(f"retired renderer: {w}", core) for w, _x, core in RR.semantic_findings(section_html, RETIRED_R)]
        return out + CF.page_claim_findings(page, section_html, VALUES)

    errs, _a, _r = AA.check_concept("fixture", concept, section_fn, claims_fn)
    return errs


def main() -> int:
    failures = 0

    def expect(kind: str, fixture: str, problems: list[str], reject: bool) -> None:
        nonlocal failures
        ok = bool(problems) == reject
        if not ok:
            failures += 1
            print(f"FAIL {kind} {'should be rejected' if reject else 'should pass'}: {fixture[:150]}"
                  + (f"\n     got: {problems[:2]}" if problems else ""))

    for f in RENDERER_REJECT:
        expect("retired-renderer", f, renderer_problems(f), True)
    for f in RENDERER_ALLOW:
        expect("retired-renderer", f, renderer_problems(f), False)
    for f in PLATFORM_REJECT:
        expect("retired-platform", f, platform_problems(f), True)
    for f in PLATFORM_ALLOW:
        expect("retired-platform", f, platform_problems(f), False)
    for f in METRIC_REJECT:
        expect("metric", f, metric_problems(f), True)
    for f in METRIC_ALLOW:
        expect("metric", f, metric_problems(f), False)

    token_concept = {"id": "fixture", "disposition": "NEW PAGE", "destinations": ["fixture.html#device-loss"], "tokens": ["deviceEventCallback"]}
    expect("ledger", "token deviceEventCallback beside a retired renderer list", ledger_result(STALE_SECTION_HTML, token_concept), True)
    expect("ledger", "token deviceEventCallback beside the current list", ledger_result(CURRENT_SECTION_HTML, token_concept), False)
    tokenless = {"id": "fixture", "disposition": "SUPERSEDED", "destinations": ["fixture.html#device-loss"], "tokens": []}
    expect("ledger", "tokenless SUPERSEDED without replacement or review", ledger_result(CURRENT_SECTION_HTML, tokenless), True)
    expect("ledger", "tokenless SUPERSEDED with replacement tokens",
           ledger_result(CURRENT_SECTION_HTML, {**tokenless, "replacement_tokens": ["four families call it"]}), False)
    expect("ledger", "tokenless SUPERSEDED with a stale replacement token",
           ledger_result(CURRENT_SECTION_HTML, {**tokenless, "replacement_tokens": ["five families call it"]}), True)
    expect("ledger", "tokenless SUPERSEDED with an explicit review",
           ledger_result(CURRENT_SECTION_HTML, {**tokenless, "review": {"result": "no current statement", "reason": "subject retired"}}), False)

    total = (len(RENDERER_REJECT) + len(RENDERER_ALLOW) + len(PLATFORM_REJECT) + len(PLATFORM_ALLOW)
             + len(METRIC_REJECT) + len(METRIC_ALLOW) + 6)
    print(f"validator fixtures: {total} run; {failures} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
