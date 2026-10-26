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

The second independent review (of f412fa0) found claims that still passed: the generated selection-axes sentence calling
Win32, X11 and Wayland host-conditional "implementations" (hardcoded in scripts/generate_dev_reference.py), "EasyGL serves
five", compiled effects "refused on the 11 identities without a compiled-effect runtime", "the other thirteen identities
accept only SurfaceFormat::Color", "879 *_test.cpp files", "631 public C++ symbols still unmapped", "the two EasyGL profiles
other than OPENGL33, OPENGLES3 and WEBGL2", and renderer shapes the semantic pass did not read ("DirectX 12 is one of the
renderer families", a bare D3D12 cell under a renderer heading, a list whose renderer context is the previous sentence).
Those sentences, verbatim where the page had them, are the *_SECOND_REVIEW fixtures below, each beside allowed
counterparts; the ledger fixtures cover the hardened written-review escape.

The third independent review (of 0077b63) found stale registry classification and compiled-effect arithmetic that still
passed: "18 enumerators from SdlRenderer (0) to Fna3d (17)", "the three Direct3D identities" (the retired DIRECTX12 kept by a
count), "eight Production, seven Supported", "the remaining eight are Native", "ten renderers: FNA3D always, nine opt-in",
"FNA3D always, nine families behind default-OFF options", "nine opt-in configurations", "the 14 capable renderer identities",
"Unbound-texture expectations cover seven renderers" (8 identities, 7 families), and the probes "Five public backends share
EasyGL", "The remaining thirteen accept Color only", "DirectX 12 belongs to the renderer family set" and "879 test files named
*_test.cpp". They are the *_THIRD_REVIEW fixtures, with the corrected sentences and other valid counterparts beside them and
the shapes this remediation's own probes found.

The final review (of 56a5ff4) found two registry counts still at 18: "the public renderer identities are a curated set of 18"
and "18 CNA_RENDERER_<X> switches" in the configure diagram of development/internals/graphics/selection.html. They end
METRIC_REJECT_THIRD_REVIEW; the corrected sentences and the same counts attributed to b0e97bb1 end METRIC_ALLOW_THIRD_REVIEW.

    test_validators.py        # exit 0 when every fixture behaves; validate_all.sh runs it first
"""

from __future__ import annotations

import re
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


def stale_problems(html: str) -> list[str]:
    from bs4 import BeautifulSoup
    body = re.sub(r"\s+", " ", BeautifulSoup(html, "html.parser").get_text(" "))
    return [f"stale {what}: {needle}" for needle, what, _ctx in CF.stale_needle_findings(body)]


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
RENDERER_REJECT_SECOND_REVIEW = [
    "<p>DirectX 12 is one of the renderer families.</p>",
    "<p>DirectX12 is one of CNA's renderers.</p>",
    "<p>D3D12 is a renderer family on Windows.</p>",
    # a bare D3D12 cell: under a Family header, and in a header-less table under a renderer heading
    "<table><tr><th>Family</th><th>Window</th></tr><tr><td>EasyGL</td><td>OpenGL</td></tr><tr><td>D3D12</td><td>HWND</td></tr></table>",
    "<h3>Renderer families</h3><table><tr><td>EasyGL</td></tr><tr><td>D3D12</td></tr></table>",
    "<h2>The renderer families</h2><table><tr><th>Name</th><th>Notes</th></tr><tr><td>Vulkan</td><td>native</td></tr><tr><td>D3D12</td><td>Windows</td></tr></table>",
    # heading + following list, a <br> inventory, a newline inventory
    "<h3>Renderer families</h3><ul><li>EasyGL</li><li>Vulkan</li><li>Direct3D 12</li></ul>",
    "<p>Renderer families:<br>EasyGL<br>Vulkan<br>Direct3D 12</p>",
    "<p>Renderers:\nEasyGL\nVulkan\nDirect3D 12</p>",
    # the renderer context is the preceding sentence
    "<p>CNA has twelve renderer families. Direct3D 11 and Direct3D 12 are among them.</p>",
    "<p>CNA has twelve renderer families. They include Direct3D 11 and Direct3D 12.</p>",
    # found by this remediation's own adversarial probes
    "<p>CNA renders through Direct3D 12 on Windows.</p>",
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
    "<p>SDL_GPU is a renderer. Direct3D 12 is one of the drivers SDL's GPU API chooses from.</p>",
    "<p>SDL_GPU is CNA's renderer for SDL3's GPU API. Direct3D 12 is the driver SDL picks on Windows.</p>",
    "<h3>SDL_GPU drivers</h3><ul><li>Vulkan</li><li>Metal</li><li>Direct3D 12</li></ul>",
    "<h2>SDL_GPU drivers</h2><table><tr><th>Name</th></tr><tr><td>Vulkan</td></tr><tr><td>D3D12</td></tr></table>",
    "<p>Direct3D 12 is the API SDL_gpu reaches on Windows.</p>",
    "<p>Output matching a Direct3D 12 debug-layer ERROR line from SDL's Direct3D 12 driver fails every test in the directory.</p>",
    "<p>CNA renders through SDL_gpu, which picks Direct3D 12 on Windows.</p>",
    "<p>Direct3D 12 belongs to SDL's GPU driver set, not to CNA's renderer families.</p>",
    "<p>Direct3D 12 is among the drivers SDL_gpu picks from.</p>",
]
RENDERER_REJECT_THIRD_REVIEW = [
    "<p>DirectX 12 belongs to the renderer family set.</p>",
    "<p>DirectX 12 is a CNA renderer family.</p>",
    "<p>Direct3D 12 is part of CNA's renderers.</p>",
    "<p>DirectX 12 is among the renderer identities.</p>",
    "<p>The DirectX 12 renderer identity is selectable.</p>",
    # found by this remediation's own adversarial probes
    "<p>DirectX 12 counts among CNA's renderer families.</p>",
    "<p>DirectX 12 still ships as a CNA renderer.</p>",
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
PLATFORM_REJECT_SECOND_REVIEW = [
    # development/reference/selection-axes.html at f412fa0, written by scripts/generate_dev_reference.py
    '<h2 id="platforms">Platform implementations (<code>CNA_PLATFORM</code>)</h2><p>From <a class="src-link" href="cmake/PlatformSelection.cmake">'
    '<code>cmake/PlatformSelection.cmake</code></a>. <code>SDL12</code> and <code>EMSCRIPTEN</code> are reserved identifiers that are refused rather '
    'than aliased. Some implementations are host-conditional (Terminal is POSIX-only, Win32 Windows-only, X11 and Wayland need their development '
    'packages) and are refused with an explanation rather than replaced by SDL3.</p>',
    "<p>CNA ships a Win32 implementation.</p>",
    "<p>The X11 implementation reads XInput2 itself.</p>",
    "<p>The Wayland implementation negotiates fractional scaling.</p>",
    "<p>The implementations include SDL3, Win32, X11 and Wayland.</p>",
    "<p>Our platform implementations are SDL3, X11 and Headless.</p>",
    "<p>X11 remains a native implementation.</p>",
    "<p>It falls back to the native X11 implementation.</p>",
    "<p>The Wayland platform layer handles scaling.</p>",
    "<p>The Win32 platform implementation owns its message loop.</p>",
    # an unrelated mention of Windows or of SDL's drivers elsewhere in the sentence does not excuse the name
    "<p>Win32 is a host-conditional implementation offered only on Windows.</p>",
    "<p>X11 is a platform implementation of its own, unlike SDL3, which goes through SDL's video drivers.</p>",
    # development/takeover/curriculum.html at f412fa0 (found by this remediation's manual search; the noun is in the sentence before)
    '<li><strong>Compare implementations of one contract.</strong> For the platform, compare <a href="sdl3.html">SDL3</a> with '
    '<a href="sdl3.html">Win32</a> or <a href="sdl3.html">X11</a>, and contrast <a href="headless.html">Headless</a>.</li>',
    # docs/input.html at f412fa0: the retired Win32 backend's event mapper described as current
    "<p>Text input is a mode, not a no-op on desktop: on Win32, for example, the event mapper consumes every WM_CHAR without raising a "
    "TextInput event until the window's mode has been enabled by StartTextInput(), and the mapper's own source comment says a game that never "
    "called it sees the same on every other backend.</p>",
    # platform implementation table rows (by heading, by header, by neighbouring current implementations)
    '<h2>Platform implementations (<code>CNA_PLATFORM</code>)</h2><table><tr><th>Value</th><th>Role</th></tr><tr><td><code>SDL3</code></td>'
    '<td>default</td></tr><tr><td><code>X11</code></td><td>windowing on Linux</td></tr></table>',
    "<table><tr><th>Platform implementation</th><th>Notes</th></tr><tr><td>Win32</td><td>message loop</td></tr></table>",
    "<table><tr><th>Value</th><th>Role</th></tr><tr><td>HEADLESS</td><td>no window</td></tr><tr><td>WIN32</td><td>windowing</td></tr></table>",
    # source diagrams whose tokens are separated by tags and newlines
    "<pre>platform/\n  src/\n    <span>Sdl3/</span>\n    <span>X11/</span>\n    <span>Headless/</span></pre>",
    "<pre>modules/platform/src/<b>Sdl3</b>\n<b>Wayland</b>\n<b>Terminal</b></pre>",
    # found by this remediation's own adversarial probes: one name per list item
    "<p>CNA_PLATFORM accepts:</p><ul><li>SDL3</li><li>X11</li><li>Headless</li></ul>",
    "<p>Platforms: SDL3 &middot; X11 &middot; Headless &middot; Terminal</p>",
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
    # the generated replacement paragraph and the SDL3 row (scripts/generate_dev_reference.py)
    "<p><code>SDL3</code> and <code>HEADLESS</code> are offered on every host. Only <code>TERMINAL</code> is host-conditional: it is built on termios, so on "
    "a Windows host it is reserved and refused with an explanation rather than replaced by SDL3. Windows is a host environment, not an implementation, and "
    "X11 and Wayland are display environments: <code>SDL3</code> reaches all three through SDL&rsquo;s own video drivers, so whatever is host- or "
    "driver-specific lives inside SDL, while <code>HEADLESS</code> opens no window at all. The values <code>WIN32</code>, <code>X11</code> and "
    "<code>WAYLAND</code> are refused by name, with a message that says to configure SDL3.</p>",
    "<table><tr><th>Value</th><th>Role</th></tr><tr><td><code>SDL3</code></td><td>default, on every host; CNA's one windowing implementation: SDL's own "
    "video drivers reach Windows, X11, Wayland, macOS, iOS, Android and the browser</td></tr></table>",
    "<p>A GPU backend must not assume that the tag hides an X11 or Wayland surface; there is none.</p>",
    "<p>a platform-implementation matrix (SDL3 on X11 and on Wayland, an SDL-free headless build, terminal and headless)</p>",
    "<p>X11 is not a CNA platform implementation; SDL3 reaches it.</p>",
    "<p>The SDL X11 driver and the SDL Wayland driver both hand over a native handle (HWND, the X11 native handle or the Wayland native handle).</p>",
    "<table><tr><th>NativeWindowSystem</th></tr><tr><td>Win32</td></tr><tr><td>X11</td></tr><tr><td>Cocoa</td></tr><tr><td>Headless</td></tr></table>",
    "<li><strong>Compare implementations of one contract.</strong> For the platform, compare SDL3 with Terminal, and contrast Headless.</li>",
    "<p>Text input is a mode: CNA's SDL3 platform turns SDL's text input on only from StartTextInput(), so a game that never calls it receives no "
    "TextInput events on Windows, X11 or Wayland alike.</p>",
    "<p>On Linux a windowed build also wants the X11, GL, Vulkan, ALSA and D-Bus development packages so the vendored SDL3 (and the native backends) get real drivers.</p>",
    "<p>The exception lists the video drivers compiled into that SDL build, which separates \u201cthis session is not running X11/Wayland\u201d from "
    "\u201cthis SDL was configured without that backend\u201d.</p>",
    "<p>modules/CMakeLists.txt sets the FFmpeg flag OFF for MINGW OR WIN32 OR EMSCRIPTEN, and the build then compiles the no-video backend.</p>",
    "<table><tr><th>Value</th><th>Status</th></tr><tr><td>SDL3</td><td>available</td></tr><tr><td>X11</td><td>retired: use SDL3</td></tr></table>",
    "<p>NativeWindowSystem names the window system:</p><ul><li>Win32</li><li>X11</li><li>Wayland</li><li>Headless</li></ul>",
    "<p>The retired values:</p><ul><li>WIN32</li><li>X11</li><li>WAYLAND</li></ul><p>The current ones:</p><ul><li>SDL3</li><li>HEADLESS</li></ul>",
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
METRIC_REJECT_SECOND_REVIEW = [
    # development/repository/source-ownership.html and development/reference/modules.html at f412fa0
    "<td>One family can serve several public identities: EasyGL serves five, and every other family serves one.</td>",
    "<p>A directory that owns a src/ is an implementation family; one family can serve several public identities (EasyGL serves five).</p>",
    "<p>EasyGL serves five identities.</p>",
    "<p>EasyGL owns five renderer identities.</p>",
    "<p>Five identities are served by EasyGL.</p>",
    "<p>The GL family has five EasyGL profiles.</p>",
    "<li>then one small descriptor such as StubRendererDescriptor.cpp and the five-identity EasyGLRendererDescriptor.cpp.</li>",
    # development/internals/graphics/selection.html at f412fa0: the subset and its exclusions do not add up
    "<td>Implemented by Vulkan (MSAA clamp only) and the two EasyGL profiles other than <code>OPENGL33</code>, <code>OPENGLES3</code> and "
    "<code>WEBGL2</code> (render-target format: <code>Color</code> only).</td>",
    # deep-dives/practice/xna-api-surface-auditing.html at f412fa0, and the same inversion in other words
    "<li><code>Effect(GraphicsDevice&amp;, bytes)</code> is represented perfectly and still refused on the 11 identities without a compiled-effect runtime.</li>",
    "<p>Compiled effects are refused on 11 identities.</p>",
    "<p>Eleven renderer identities cannot consume compiled effects.</p>",
    "<p>The 13 identities without a compiled-effect runtime throw NotSupportedException.</p>",
    # about.html, docs/tutorials/108, 128 and 151, docs/content-pipeline-xnb.html at f412fa0
    "<li>XNA Effect Framework bytecode is a separate compatibility path on qualified renderer builds (13 of the 14 identities).</li>",
    "<p>(In this snapshot thirteen other identities (nine implementation families) can also execute compiled XNA effects that you supply.)</p>",
    "<p>Load XNA/FNA D3D9 Effect Framework bytecode and XNB Effect assets in CNA on the 14 renderer identities that support them.</p>",
    "<li>Tutorial 128 &mdash; the compiled-effect path, which is portable across 14 renderer identities instead.</li>",
    "<p>That succeeds only when the renderer reports CompiledEffects (FNA3D always provides it; nine other renderer families offer it through opt-in build options).</p>",
    # docs/migration-from-monogame.html at f412fa0
    "<li>on top of that, eight renderer families promote the broader public texture formats and the other thirteen identities accept only "
    "<code>SurfaceFormat::Color</code>. Verify the active renderer.</li>",
    "<p>Nine renderer families classify the broader texture formats; the other five identities accept only SurfaceFormat::Color.</p>",
    # development/repository/source-ownership.html at f412fa0: a count of every examples/ .cpp under the *_test.cpp name
    "<td>Demos and standalone pixel or contract programs (879 <code>*_test.cpp</code> files), registered by the owning module's own CMake.</td>",
    "<p>The examples hold 879 standalone pixel programs.</p>",
    "<p>The tree has 813 files named *_test.cpp.</p>",
    # development/handbook/investigate-a-sample-failure.html and docs/tutorials/87-custom-backend.html at f412fa0
    "<td>Standalone <code>*_test.cpp</code> programs registered beside each module (879 across the tree)</td>",
    "<p>The default is Defer, and that rule is SurfaceFormat::Color only. That is why seven shipped renderers are Color-only without writing a line of format code.</p>",
    "<p>The tree has 781 test source files.</p>",
    "<p>879 test files with a GoogleTest macro.</p>",
    # docs/tutorials/87-custom-backend.html at f412fa0 (one identity, SDL_RENDERER, is 2D-only)
    "<p>You override what your API can genuinely do. Seven shipped renderers are 2D-only, and two produce no pixels at all.</p>",
    # complements larger than the whole
    "<li>A green single-renderer run describes the selected family, not the other 20 families.</li>",
    "<p>The other 15 renderer identities share the same C surface but are not in the matrix at all.</p>",
    "<td>No oracle-corpus number recorded. Unbound-texture expectations cover seven renderers; parity fixtures cover five families.</td>",
    # docs/c-api.html and docs/roadmap.html at f412fa0
    "<p>CNA&rsquo;s own release gate for the C ABI says &ldquo;Not ready&rdquo;, with 631 public C++ symbols still unmapped.</p>",
    "<td>631 public C++ symbols are still unmapped in the generated inventory.</td>",
    "<p>631 missing C ABI exports keep the release gate at Not ready.</p>",
    # found by this remediation's own adversarial probes
    "<p>EasyGL is shared by five identities.</p>",
    "<p>Compiled effects are unavailable on eleven identities.</p>",
    "<p>Six identities without a classifier accept only SurfaceFormat::Color.</p>",
    "<p>EasyGL: five identities, one implementation.</p>",
    "<p>Compiled effects work everywhere except on 11 identities.</p>",
]
METRIC_ALLOW = [
    "<p>Since alpha.1 the set has been deliberately curated from 50 identities over 46 implementation families to 14 over 12.</p>",
    "<p>The previous snapshot, b0e97bb1, had 18 public identities over 14 implementation families and 852 C++ test source files.</p>",
    "<p>Storage has 14 statically discoverable GoogleTest-family definitions (alpha.1: five).</p>",
    '<p>Quote the gate as committed: "Not ready, one criterion unmet: 631 public symbols are still unmapped".</p>',
    "<p>631 planned public C++ declarations do not yet have C mappings.</p>",
    "<table><tr><th>Area</th><th>Alpha.1</th><th>Snapshot</th></tr><tr><td>Renderers</td><td>50 public identities over 46 implementation families</td><td>14 over 12</td></tr></table>",
    "<td>One family can serve several public identities: EasyGL serves three (OPENGLES3, OPENGL33 and WEBGL2), and every other family serves one.</td>",
    "<p>All three GL identities are one implementation: agreement between two EasyGL profiles does not independently confirm code they share.</p>",
    "<td>Vulkan (MSAA clamp only) and two of the three EasyGL identities, OPENGLES3 and WEBGL2 (render-target format: Color only).</td>",
    "<td>One EasyGL identity on one host, not all renderer families.</td>",
    "<p>The EasyGL family (3) serves OPENGLES3, OPENGL33 and WEBGL2.</p>",
    "<li><code>Effect(GraphicsDevice&amp;, bytes)</code> is still refused wherever the active renderer has no compiled-effect runtime. The two identities that "
    "cannot have one (HEADLESS and STUB) always refuse it; in a default configuration 9 of the 10 identities refuse it, all but FNA3D, "
    "because every compiled-effect build option defaults to OFF. Only the first set is a renderer limit: the other seven identities can run compiled "
    "effects once their option is turned on.</li>",
    "<li>six renderer families (eight of the 10 identities) classify the broader public texture formats themselves, while the other two identities "
    "(HEADLESS and STUB) have no classifier and accept only <code>SurfaceFormat::Color</code> for a public Texture2D.</li>",
    "<p>That is why two shipped renderers are Color-only for textures, and four for render targets.</p>",
    "<td>Demos and standalone pixel or contract programs: 694 <code>.cpp</code> files in all (693 under modules/&lt;name&gt;/examples/ plus the loose "
    "demo), 598 of them named <code>*_test.cpp</code>. That 598 is a different set from the 855 test files with a GoogleTest macro.</td>",
    "<p>No shipped renderer is 2D-only, and two produce no pixels at all (HEADLESS and STUB).</p>",
    "<p>CNA&rsquo;s own release gate says &ldquo;Not ready&rdquo;, because 631 in-scope public C++ declarations still lack C mappings.</p>",
    "<td>625 planned public C++ declarations remain without C mappings; 3,212 C routes are declared and exported.</td>",
    '<div class="callout callout--note dev-evidence"><p><strong>Evidence basis:</strong> source-verified at the stated evidence commit. Claims on this page were '
    'checked by reading the CNA source at commit <code>b0e97bb1</code>; nothing was built.</p></div>',    '<p>The source tree has 898 C++ test files and 11,898 statically discoverable GoogleTest-family definitions (855 files contain at least one; alpha.1 had 568 and 8,263).</p>',
    '<li>The 10-identity, 8-family registry in cmake/RendererIdentities.cmake is strong structural evidence.</li>',
    '<p>Compiled-effect support is 8 of the 10 identities in 6 implementation families.</p>',
    '<p>A default configure reports CompiledEffects false on 9 of the 10 identities.</p>',
    '<p>Storage has 70 statically discoverable GoogleTest-family definitions (alpha.1: five).</p>',
    "<p>one renderer's oracle result says nothing about the other 9 identities</p>",
    '<p>Named refusals: compiled effects on 2 of the 10 identities.</p>',
    '<p>Eight of the 10 identities run compiled effects (HEADLESS and STUB do not).</p>',
    '<p>FNA3D always, and 7 more renderer identities behind default-OFF CNA_*_COMPILED_EFFECTS options.</p>',
    '<p>A default configure reports compiled effects as supported on FNA3D only (unsupported on 9 of 10 identities).</p>',
    '<p>A default configure reports the CompiledEffects capability true on FNA3D only; the other 9 identities report false.</p>',
    '<p>FNA3D always provides it; five other renderer families offer it through opt-in build options.</p>',
    '<p>Compiled effects run on six renderer families (8 identities); the EasyGL option covers its three identities.</p>',
    '<p>10 public renderer identities in 8 implementation families, capabilities, compiled effects and verification.</p>',
    '<p>Four families classify render-target formats themselves; the other four identities accept only Color for render targets.</p>',
    '<td>Standalone <code>*_test.cpp</code> programs registered beside each module (598 across the tree)</td>',
    '<p>The source tree has 898 C++ test source files; 855 files contain at least one counted macro, and 598 standalone pixel programs sit under examples/.</p>',
    '<p>A green single-renderer run describes the selected family, not the other 7 families.</p>',
    '<p>The other 7 renderer identities share the same C surface but are not in the matrix at all.</p>',
    '<p>32 parity fixtures are registered for three renderer families; parity fixtures cover three families.</p>',
    '<p>The previous snapshot, c1c316b9, had 14 public identities over 12 implementation families and 813 C++ test files.</p>',
    '<p>The 0.1.0 release still had 14 renderer identities and C ABI 0.46.0; both changed afterwards.</p>',
    '<table><tr><th>Area</th><th>0.1.0 release</th><th>This snapshot</th></tr><tr><td>Renderers</td><td>14 public identities over 12 families</td><td>10 public identities over 8 families</td></tr></table>',
    '<table><tr><th>Area</th><th>Alpha.1</th><th>0.1.0</th></tr><tr><td>Renderers</td><td>50 public identities over 46 implementation families</td><td>A curated set of 14 identities over 12 families</td></tr></table>',
    '<div class="callout callout--note dev-evidence"><p><strong>Evidence basis:</strong> source-verified at the stated evidence commit. Claims on this page were checked by reading the CNA source at commit <code>c1c316b9</code>; nothing was built.</p></div>',

]

# development/internals/graphics/selection.html at 56a5ff4, verbatim up to the stale line: the .cmake names above it excused the count as a quotation
SELECTION_DIAGRAM = ('<pre class="diagram">CMakeLists.txt\n'
                     '  → cmake/RendererIdentities.cmake        refuse any name outside the 14 public identities\n'
                     '                                          (all three routes), before SDL or any dependency\n'
                     '  → cmake/PlatformSelection.cmake, AudioPlatformSelection.cmake\n'
                     '  → cmake/SdlAvailability.cmake\n'
                     '      → RendererIdentityDefault.cmake     per-host default, needed to decide whether SDL is needed\n'
                     '  → cmake/RendererSelection.cmake\n'
                     '      → RendererIdentityDefault.cmake / RendererIdentities.cmake   (re-included, no-op)\n'
                     '      → CNA_GRAPHICS_RENDERER cache value + {n} CNA_RENDERER_&lt;X&gt; switches (exactly one may be ON)\n'
                     '      → RendererDefaultSelection.cmake    set + default first + dedupe → CNA_RENDERER_IDENTITIES</pre>')

METRIC_REJECT_THIRD_REVIEW = [
    # development/internals/modules/core.html at 0077b63: the 18-identity enum, its ordinals and its classification arithmetic
    "<p><code>GraphicsRendererType</code> is dense: 18 enumerators from <code>SdlRenderer</code> (0) to <code>Fna3d</code> (17).</p>",
    "<p>GraphicsRendererType ends at ordinal 17.</p>",
    "<p>Maturity: <code>SDL_RENDERER</code>, the three non-web EasyGL profiles, <code>VULKAN</code> and the three Direct3D identities are <code>Production</code>; "
    "<code>WEBGPU</code>, <code>SOFTWARE</code> and <code>FNA3D</code> are <code>Experimental</code>; the rest are <code>Supported</code>.</p>",
    "<p>Category: <code>HEADLESS</code> and <code>STUB</code> are <code>Diagnostic</code>, <code>SOFTWARE</code> is <code>Software</code>, the three browser-only "
    "identities are <code>Web</code>, four identities (<code>SDL_RENDERER</code>, <code>WEBGPU</code>, <code>SDL_GPU</code> and <code>FNA3D</code>) are "
    "<code>TranslationLayer</code>, and the remaining eight are <code>Native</code>.</p>",
    # docs/faq.html at 0077b63: the maturity split of the 18-identity registry
    "<p>CNA itself declares a maturity for each of the 14 identities in code (eight <em>Production</em>, seven <em>Supported</em>, three <em>Experimental</em>).</p>",
    "<p>CNA's categories: eight Native identities, four TranslationLayer, one Software, three Web and two Diagnostic.</p>",
    # development/internals/graphics/selection.html and deep-dives/models/vertex-packing-and-strides.html at 0077b63: the retired
    # DIRECTX12 kept alive by a count
    "<p><code>CNA_PLATFORM=TERMINAL</code> admits only <code>SOFTWARE</code>, <code>HEADLESS</code> and <code>STUB</code>; the three Direct3D identities require a "
    "Windows target; <code>METAL</code> requires macOS; the browser identities require Emscripten; the three native GL-profile identities refuse Emscripten.</p>",
    "<p>The canonical table exists because seven rasterizing renderers (Vulkan, Software, WebGPU, SDL_GPU and the three Direct3D renderers) do not translate a "
    "<code>VertexDeclaration</code>.</p>",
    # compiled effects: docs/verification.html, docs/tutorials/87, deep-dives/reference/graphics-quick-reference.html,
    # deep-dives/graphics/shader-routes-four-answers.html and docs/tutorials/52 and 53 at 0077b63
    "<td>Already-compiled XNA/FNA effects can be retained when the active renderer exposes <code>CompiledEffects</code> (ten renderers: <code>FNA3D</code> always, nine opt-in).</td>",
    "<p>A second, separate route exists for XNA-authored effects: <code>SupportsCompiledEffects()</code> and <code>CreateCompiledEffect(&hellip;)</code> let a renderer "
    "execute compiled Direct3D 9 Effect Framework bytecode. Ten renderers implement it &mdash; <code>FNA3D</code> always, nine behind opt-in "
    "<code>CNA_*_COMPILED_EFFECTS</code> build options &mdash; and it is a large piece of work.</p>",
    "<td>the byte constructor works where <code>CompiledEffects</code> is true: FNA3D always, nine families behind default-OFF options; it is not a source compiler</td>",
    "<li>A game that loads compiled XNA/FNA Effect Framework bytecode needs FNA3D or one of the nine opt-in configurations (route three).</li>",
    "<li>The separate <code>Effect(device, effectCode)</code> compatibility path accepts XNA/FNA Effect Framework bytecode only on the 14 capable renderer identities.</li>",
    "<li><strong>Compiled XNA effects</strong> (<code>Effect(device, bytes)</code> or an XNB <code>Effect</code>, on the 14 capable renderer identities) reflect a complete graph.</li>",
    "<p>Ten renderers support compiled effects through nine opt-in configurations.</p>",
    "<p>FNA3D plus nine optioned families support compiled effects.</p>",
    "<p>There are nine opt-in compiled-effect families.</p>",
    # development/takeover/xna-oracle.html at 0077b63: the 8-identity unbound-texture gate counted as seven renderers
    "<td>No oracle-corpus number recorded. Unbound-texture expectations cover seven renderers; parity fixtures cover four families.</td>",
    # the natural complement and inverse forms the third review found passing
    "<p>Five public backends share EasyGL.</p>",
    "<p>Eleven renderers cannot consume compiled effects.</p>",
    "<p>The remaining thirteen accept Color only.</p>",
    "<p>879 test files named *_test.cpp.</p>",
    # development/build/index.html at 0077b63, found by this remediation's final sweep
    "<td>A renderer name outside the 18, through <code>CNA_GRAPHICS_RENDERER</code> or a member of <code>CNA_GRAPHICS_RENDERERS</code></td>",
    # found by this remediation's own adversarial probes
    "<p>GraphicsRendererType ordinals run from 0 to 17.</p>",
    "<p>CNA's GraphicsRendererType enumerates 18 identities.</p>",
    "<p>Production: eight identities.</p>",
    "<p>CNA classifies four identities as TranslationLayer.</p>",
    "<p>Besides FNA3D, eleven identities need an opt-in option for compiled effects.</p>",
    "<p>The unbound-texture test skips on the other eight identities.</p>",
    "<p>SurfaceFormat::Color is the only texture format on eleven renderers.</p>",
    # the final review of 56a5ff4: development/handbook/conventions.html and the selection.html diagram
    "<td>The public renderer identities are a curated set of 18, with fixed C ABI values that are never reassigned; a name outside the set is refused at configure time.</td>",
    SELECTION_DIAGRAM.format(n=18),
]
METRIC_ALLOW_THIRD_REVIEW = [
    # the corrected sentences of the pages above
    "<p><code>GraphicsRendererType</code> is dense: 10 enumerators from <code>OpenGLES3</code> (0) to <code>Fna3d</code> (9).</p>",
    "<p>GraphicsRendererType ends at ordinal 9; OpenGLES3 is therefore ordinal 0 in C++ but 3 in C.</p>",
    "<p>Maturity: three identities are <code>Production</code> (the two non-web EasyGL profiles <code>OPENGLES3</code> and <code>OPENGL33</code>, "
    "and the one Direct3D identity, <code>DIRECTX9</code>); two are <code>Experimental</code> (<code>SOFTWARE</code> and <code>FNA3D</code>); "
    "the remaining five are <code>Supported</code> (<code>WEBGL2</code>, <code>WEBGPU</code>, <code>HEADLESS</code>, <code>STUB</code> and "
    "<code>SDL_GPU</code>); <code>Historical</code> and <code>Deprecated</code> are unused.</p>",
    "<p>Category: <code>HEADLESS</code> and <code>STUB</code> are <code>Diagnostic</code>, <code>SOFTWARE</code> is <code>Software</code>, the one browser-only identity, "
    "<code>WEBGL2</code>, is <code>Web</code>, three identities (<code>WEBGPU</code>, <code>SDL_GPU</code> and <code>FNA3D</code>) are "
    "<code>TranslationLayer</code>, and the remaining three (<code>OPENGLES3</code>, <code>OPENGL33</code> and <code>DIRECTX9</code>) are <code>Native</code>.</p>",
    "<p>CNA itself declares a maturity for each of the 10 identities in code (three <em>Production</em>, five <em>Supported</em>, two <em>Experimental</em>).</p>",
    "<p>the one Direct3D identity (<code>DIRECTX9</code>) requires a Windows target; the browser-only <code>WEBGL2</code> requires Emscripten; "
    "the two native GL-profile identities (<code>OPENGLES3</code> and <code>OPENGL33</code>) refuse Emscripten.</p>",
    "<p>four rasterizing renderers (Software, WebGPU, SDL_GPU and the one Direct3D renderer, DIRECTX9) do not translate a VertexDeclaration.</p>",
    "<p>Only one Direct3D renderer, DIRECTX9, runs Microsoft's recompiled stock effects; two native GL-profile identities accept them too.</p>",
    "<td>Already-compiled XNA/FNA effects can be retained when the active renderer exposes <code>CompiledEffects</code> (8 renderer identities in six implementation "
    "families: <code>FNA3D</code> always, the other seven identities only with their family's opt-in option, five options in all).</td>",
    "<p>Eight renderer identities in six implementation families implement it &mdash; <code>FNA3D</code> always, the other seven identities in five families behind "
    "opt-in <code>CNA_*_COMPILED_EFFECTS</code> build options &mdash; and it is a large piece of work.</p>",
    "<td>the byte constructor works where <code>CompiledEffects</code> is true: FNA3D always, five more families (seven identities) behind default-OFF options</td>",
    "<li>A game that loads compiled XNA/FNA Effect Framework bytecode needs FNA3D or a build of one of the other seven capable identities with its family's opt-in "
    "option on (five options, route three).</li>",
    "<li>The separate <code>Effect(device, effectCode)</code> compatibility path accepts XNA/FNA Effect Framework bytecode only on the 8 capable renderer identities.</li>",
    "<p>Eight renderer identities across six implementation families can support compiled effects.</p>",
    "<p>Seven capable identities are provided by five optioned implementation families, plus FNA3D.</p>",
    "<p>Nine identities refuse compiled effects in the default configuration.</p>",
    "<p>Two identities can never support compiled effects.</p>",
    "<p>Two renderers cannot consume compiled effects.</p>",
    "<p>-DCNA_EASYGL_COMPILED_EFFECTS=ON (default OFF); one option enables all three identities.</p>",
    "<td>No oracle-corpus number recorded. Unbound-texture expectations cover five renderer identities across four implementation families; parity fixtures cover three families.</td>",
    "<p>The unbound-texture gate spans four implementation families.</p>",
    "<p>Three public backends share EasyGL.</p>",
    "<p>EasyGL is shared by three identities.</p>",
    "<p>Six renderer families classify the broader texture formats. The remaining two accept Color only.</p>",
    "<p>The remaining two accept Color only.</p>",
    "<p>Four families classify render-target formats themselves; the remaining four accept only Color for render targets.</p>",
    "<p>598 test files named *_test.cpp sit under examples/; 694 .cpp files sit under examples/ directories.</p>",
    "<p>The compiled-effect path is optioned on five families (seven identities).</p>",
    "<p>The unbound-texture test skips on the other five identities.</p>",
    "<p>SurfaceFormat::Color is the only texture format on two renderers.</p>",
    "<p>Two identities, HEADLESS and STUB, are Diagnostic; of the three Native identities, two are EasyGL profiles.</p>",
    "<p>The one Direct3D identity, DIRECTX9, needs Windows.</p>",
    "<td>A renderer name outside the 10, through <code>CNA_GRAPHICS_RENDERER</code> or a member of <code>CNA_GRAPHICS_RENDERERS</code></td>",
    # the corrected final-review sentences, and the old count attributed to the snapshot that had it
    "<td>The public renderer identities are a curated set of 10, with fixed C ABI values that are never reassigned; a name outside the set is refused at configure time.</td>",
    SELECTION_DIAGRAM.format(n=10),
    "<p>At c1c316b9 the public renderer identities were a curated set of 14; at c6dec91f they are 10.</p>",
    "<p>At b0e97bb1, RendererSelection.cmake read 18 CNA_RENDERER_&lt;X&gt; switches, one per public identity of that snapshot.</p>",
]

# Phase 6 (c1c316b9 -> c6dec91f): the sentences that were current at c1c316b9 must now fail, and VULKAN, DIRECTX11, METAL
# and SDL_RENDERER joined the retired renderers, so naming them as CNA renderers fails while the API names of SDL's, FNA3D's
# and wgpu-native's own drivers still pass.
METRIC_REJECT_PHASE6 = [
    '<p>The source tree has 813 C++ test files and 11,380 statically discoverable GoogleTest-family definitions (781 files contain at least one; alpha.1 had 568 and 8,263).</p>',
    '<li>The 14-identity, 12-family registry in cmake/RendererIdentities.cmake is strong structural evidence.</li>',
    '<p>Compiled-effect support is 11 of the 14 identities in 9 implementation families.</p>',
    '<p>A default configure reports CompiledEffects false on 13 of the 14 identities.</p>',
    "<p>one renderer's oracle result says nothing about the other 13 identities</p>",
    '<p>Named refusals: compiled effects on 3 of the 14 identities, 3D calls on the 2D-only renderer.</p>',
    '<p>Eleven of the 14 identities run compiled effects (SDL_RENDERER, HEADLESS and STUB do not).</p>',
    '<p>FNA3D always, and 10 more renderer identities behind default-OFF CNA_*_COMPILED_EFFECTS options.</p>',
    '<p>A default configure reports compiled effects as supported on FNA3D only (unsupported on 13 of 14 identities).</p>',
    '<p>A default configure reports the CompiledEffects capability true on FNA3D only; the other 13 identities report false.</p>',
    '<p>FNA3D always provides it; eight other renderer families offer it through opt-in build options.</p>',
    '<p>Compiled effects run on nine renderer families (11 identities); the EasyGL option covers its three identities.</p>',
    '<p>14 public renderer identities in 12 implementation families, capabilities, compiled effects and verification.</p>',
    '<p>Seven families classify render-target formats themselves; the other five identities accept only Color for render targets.</p>',
    '<td>Standalone <code>*_test.cpp</code> programs registered beside each module (781 across the tree)</td>',
    '<p>The source tree has 813 C++ test source files; 781 files contain at least one counted macro, and 781 standalone pixel programs sit under examples/.</p>',
    '<p>A green single-renderer run describes the selected family, not the other 11 families.</p>',
    '<p>The other 11 renderer identities share the same C surface but are not in the matrix at all.</p>',
    '<p>32 parity fixtures are registered for four renderer families; parity fixtures cover four families.</p>',
    "<p>CNA exposes 14 renderer identities across 12 implementation families.</p>",
    "<p>Its experimental C ABI is at ABI 0.46.0.</p>",
    "<p>The snapshot has 18 workflow files (24 jobs).</p>",
]
RENDERER_REJECT_PHASE6 = [
    "<p>CNA's Vulkan renderer takes SPIR-V words rather than GLSL text.</p>",
    "<p>The Metal backend shades PBR on macOS and iOS.</p>",
    "<p>Custom HLSL runs on the Direct3D 11 renderer.</p>",
    "<p>Renderers that report instancing: EasyGL, SDL_GPU, Vulkan and WebGPU.</p>",
    "<p>The 2D-only SDL_RENDERER clips to any non-empty scissor rectangle.</p>",
    "<table><tr><th>Renderer</th><th>Notes</th></tr><tr><td><code>SDL_GPU</code></td><td>modern path</td></tr><tr><td><code>VULKAN</code></td><td>native</td></tr></table>",
    "<pre><code>cmake -S . -B build -DCNA_GRAPHICS_RENDERER=METAL</code></pre>",
    "<p>Compiled effects need -DCNA_DIRECTX11_COMPILED_EFFECTS=ON on that renderer.</p>",
]
RENDERER_ALLOW_PHASE6 = [
    "<p>SDL_GPU runs on SDL&rsquo;s Vulkan, Direct3D 12 or Metal GPU driver.</p>",
    "<p>FNA3D chooses its SDL_GPU, Direct3D 11 or OpenGL driver at run time.</p>",
    "<p>On macOS WEBGPU, whose wgpu-native library drives Metal there, is another choice.</p>",
    "<p>On Linux SDL_GPU needs a Vulkan loader and driver ICD at run time.</p>",
    "<p>The default on Windows is SDL_GPU, on SDL&rsquo;s Direct3D 12 GPU driver.</p>",
]

# the ledger gate: a concept whose token survives must still fail when its cited section carries a rejected claim
STALE_SECTION_HTML = ("<h2 id='device-loss'>Device loss</h2><p><code>createRenderer()</code> hands every family a <code>deviceEventCallback</code>. "
                      "At this snapshot five families call it: DirectX 9, DirectX 11 and DirectX 12 report loss and reset.</p>")
CURRENT_SECTION_HTML = ("<h2 id='device-loss'>Device loss</h2><p><code>createRenderer()</code> hands every family a <code>deviceEventCallback</code>. "
                        "At this snapshot three families call it: DirectX 9 reports loss and reset.</p>")


def ledger_result(section_html: str, concept: dict) -> list[str]:
    tree = AA.Tree()
    tree.feed(section_html)
    sec = AA._norm(AA.section_text(tree.ids["device-loss"]))

    def section_fn(page: str, frag: str) -> str | None:
        return sec if frag in ("", "device-loss") else None

    def claims_fn(page: str) -> list[tuple[str, str]]:
        out = [(f"retired renderer: {w}", core) for w, _x, core in RR.semantic_findings(section_html, RETIRED_R)]
        return out + CF.page_claim_findings(page, section_html, VALUES)

    errs, _a, _r = AA.check_concept("fixture", concept, section_fn, claims_fn)
    return errs


def late_reclassification_problems() -> list[str]:
    """The c6dec91f re-verification reclassified a functional gap into a bug class that already held entries the audit had
    added; allocated in the ordinary order it would have renumbered every added bug.  scripts/known_issues.py therefore takes
    "late": true reclassifications after "added".  The fixture runs apply_adversarial on a three-entry patch held in memory
    and checks the ids: the ordinary reclassification first, then the added entry, then the late one (no id moves)."""
    import known_issues as K

    class _Patch:                                      # stands in for ISS / "patches-adversarial.json"; nothing is read or written
        def __truediv__(self, _name):
            return self

        def exists(self):
            return True
    adv = {"reclassified": {"CNA-GAP-001": {"class": "bug", "late": True}, "CNA-PLAT-001": {"class": "bug"}},
           "added": [{"id": "NEW-T-01", "class": "bug", "cand_ids": []}]}
    issues = [{"id": "CNA-GAP-001", "class": "functional-gap", "severity": "n/a"},
              {"id": "CNA-PLAT-001", "class": "platform-limitation", "severity": "n/a"}]
    counters = {"bug": 10, "functional-gap": 1, "platform-limitation": 1, "verification-gap": 0}
    saved = K.ISS, K.load
    K.ISS, K.load = _Patch(), (lambda _path: adv)
    try:
        _issues, _disp, trail, rc = K.apply_adversarial(issues, [], counters)
    finally:
        K.ISS, K.load = saved
    got = {**trail.get("reclassified", {}), **trail.get("added", {})}
    want = {"CNA-PLAT-001": "CNA-BUG-011", "NEW-T-01": "CNA-BUG-012", "CNA-GAP-001": "CNA-BUG-013"}
    return [] if rc == 0 and got == want else [f"late reclassification allocated {got} (rc {rc}), expected {want}"]


def superseded_replacement_problems(variant: str) -> list[str]:
    """bible_ledger.py: a SUPERSEDED concept whose old wording left the page is anchored by replacement_tokens (the
    superseding statement), checked against the destination page like tokens.  The fixture takes a real recorded concept
    of that shape and checks it as recorded ("as-is"), without any token ("none": still an error) and with a replacement
    token that is not on the page ("absent": still an error).  Only that concept's errors count."""
    import copy
    import bible_ledger as BL
    units = {u["id"]: u for u in BL.record_units(BL.load_units())}
    for uid, rec in BL.load_records().items():
        for i, c in enumerate(rec.get("concepts") or []):
            if (c.get("disposition") == "SUPERSEDED" and c.get("replacement_tokens") and not c.get("tokens")
                    and not c.get("no_tokens_reason") and c.get("destinations") and uid in units):
                rec = copy.deepcopy(rec)
                c = rec["concepts"][i]
                if variant == "none":
                    c["replacement_tokens"] = []
                elif variant == "absent":
                    c["replacement_tokens"] = ["a phrase no page of this site carries 7f3e"]
                errs, _w = BL.check_record(uid, rec, units[uid], False)
                return [e for e in errs if e.startswith(f"{uid}/{c.get('id')}:")]
    return ["no SUPERSEDED concept anchored by replacement_tokens found in the records"] if variant == "as-is" else []


def _prism_page(*names: str, sep: str = "\n", mode: str = "defer", lang: str = "") -> str:
    tags = sep.join(f'<script src="../js/prism/{n}.min.js" {mode}></script>' for n in names)
    block = f'<pre><code class="language-{lang}">x</code></pre>' if lang else "<p>x</p>"
    return f"<html><body>{block}\n{tags}\n</body></html>"


# prism_scripts.py: a component runs after the grammar it extends (prism-cpp and prism-glsl extend prism-c)
PRISM_REJECT = [
    _prism_page("prism", "prism-cpp", "prism-glsl", "prism-json", "prism-bash", "prism-cmake"),   # the footer before the fix
    _prism_page("prism", "prism-cpp", "prism-c"),                                                 # docs/releases.html before the fix
    _prism_page("prism-c", "prism", "prism-cpp"),                                                 # a component before the core
    _prism_page("prism-c", "prism-cpp"),                                                          # components without the core
    _prism_page("prism", "prism-c", "prism-c", "prism-cpp"),                                      # loaded twice
    _prism_page("prism", "prism-glsl"),                                                           # glsl needs c as well
    _prism_page("prism", "prism-c", "prism-cpp", lang="bash"),                                    # docs/releases.html: no bash component
]
PRISM_ALLOW = [
    _prism_page("prism", "prism-c", "prism-cpp", "prism-glsl", "prism-json", "prism-bash", "prism-cmake"),
    _prism_page("prism", "prism-c", "prism-cpp", "prism-cmake", "prism-bash"),
    _prism_page("prism", "prism-bash"),
    _prism_page("prism", "prism-c", "prism-cpp", sep=""),
    _prism_page("prism", "prism-c", "prism-cpp", lang="cpp"),
    _prism_page("prism", "prism-bash", lang="text"),                                             # no component exists for it
    _prism_page("prism", "prism-bash", lang="javascript"),                                       # in the core bundle
    "<html><body><p>no code on this page</p></body></html>",
]


def prism_repair_problems() -> list[str]:
    """prism_scripts.py fix: the rejected pages come back clean, with the tag form, prefix and separator kept, a correct
    page is returned unchanged, a second run changes nothing, and a run split by other markup is refused, not guessed."""
    import prism_scripts as PS
    out: list[str] = []
    for page in PRISM_REJECT:
        fixed, err = PS.repair(page)
        if err or PS.problems(fixed):
            out.append(f"repair left problems ({err or PS.problems(fixed)[:1]}) for {page[30:120]!r}")
        elif PS.repair(fixed) != (fixed, None):
            out.append(f"repair is not idempotent for {page[30:120]!r}")
    want = _prism_page("prism", "prism-c", "prism-cpp", "prism-glsl", "prism-json", "prism-bash", "prism-cmake")
    if PS.repair(PRISM_REJECT[0])[0] != want:
        out.append("the footer run was not rebuilt as prism, prism-c, prism-cpp, ... in the page's own tag form")
    one_line = _prism_page("prism", "prism-cpp", sep="")
    if PS.repair(one_line)[0] != _prism_page("prism", "prism-c", "prism-cpp", sep=""):
        out.append("repair did not keep a run written on one line")
    for page in PRISM_ALLOW:
        if PS.repair(page) != (page, None):
            out.append(f"repair changed a correct page {page[30:120]!r}")
    with_bash = PS.repair(_prism_page("prism", "prism-c", "prism-cpp", lang="bash"))[0]
    if with_bash != _prism_page("prism", "prism-c", "prism-cpp", "prism-bash", lang="bash"):
        out.append("repair did not append the component a code block names")
    split = _prism_page("prism").replace("</body>", '<p>other</p>\n<script src="../js/prism/prism-cpp.min.js" defer></script>\n</body>')
    if PS.repair(split)[1] is None:
        out.append("repair rewrote a Prism run that other markup splits")
    return out


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
           ledger_result(CURRENT_SECTION_HTML, {**tokenless, "replacement_tokens": ["three families call it"]}), False)
    expect("ledger", "tokenless SUPERSEDED with a stale replacement token",
           ledger_result(CURRENT_SECTION_HTML, {**tokenless, "replacement_tokens": ["five families call it"]}), True)
    # the written-review escape: any non-empty result/reason used to pass; now it needs a classification, a reason and a checkable pointer
    why = "the device-loss statement it recorded belongs to a renderer family CNA no longer ships"
    reviews = [
        ("free-text review (passed before the second review)", {"result": "no current statement", "reason": "subject retired"}, True),
        ("review with an unknown classification", {"result": "superseded somehow", "reason": why, "evidence": "cmake/RendererIdentities.cmake"}, True),
        ("review with a token reason", {"result": "retired", "reason": "retired", "evidence": "cmake/RendererIdentities.cmake"}, True),
        ("retired review without evidence", {"result": "retired", "reason": why}, True),
        ("replaced review without a replacement anchor", {"result": "replaced", "reason": why}, True),
        ("replaced review naming a missing anchor", {"result": "replaced", "reason": why, "replacement": "fixture.html#nowhere"}, True),
        ("explicit retired review with evidence", {"result": "retired", "reason": why, "evidence": "cmake/RendererIdentities.cmake CNA_RENDERER_RETIRED_IDENTITIES"}, False),
        ("explicit replaced review naming the replacement", {"result": "replaced", "reason": why, "replacement": "fixture.html#device-loss"}, False),
    ]
    for name, review, reject in reviews:
        expect("ledger", f"tokenless SUPERSEDED, {name}", ledger_result(CURRENT_SECTION_HTML, {**tokenless, "review": review}), reject)

    groups = [(RENDERER_REJECT_SECOND_REVIEW, renderer_problems, "retired-renderer"), (PLATFORM_REJECT_SECOND_REVIEW, platform_problems, "retired-platform"),
              (METRIC_REJECT_SECOND_REVIEW, metric_problems, "metric")]
    for fixtures, fn, kind in groups:
        for f in fixtures:
            expect(f"{kind} (second review)", f, fn(f), True)
    for f in RENDERER_REJECT_THIRD_REVIEW:
        expect("retired-renderer (third review)", f, renderer_problems(f), True)
    for f in METRIC_REJECT_THIRD_REVIEW:
        expect("metric (third review)", f, metric_problems(f), True)
    for f in METRIC_ALLOW_THIRD_REVIEW:
        expect("metric (third review)", f, metric_problems(f) + renderer_problems(f), False)
    for f in METRIC_REJECT_PHASE6:
        expect("metric (phase 6)", f, metric_problems(f) + stale_problems(f), True)
    for f in RENDERER_REJECT_PHASE6:
        expect("retired-renderer (phase 6)", f, renderer_problems(f), True)
    for f in RENDERER_ALLOW_PHASE6:
        expect("retired-renderer (phase 6)", f, renderer_problems(f), False)
    # known_issues.py: a "late" reclassification takes its id after every added entry, so no added id moves
    expect("known-issues ids", "late reclassification after added entries", late_reclassification_problems(), False)
    for f in PRISM_REJECT:
        expect("prism order", f, __import__("prism_scripts").problems(f), True)
    for f in PRISM_ALLOW:
        expect("prism order", f, __import__("prism_scripts").problems(f), False)
    expect("prism order", "repair of the rejected pages", prism_repair_problems(), False)
    # bible_ledger.py: replacement_tokens anchor a SUPERSEDED concept; without them, or with one off the page, it fails
    expect("bible ledger", "SUPERSEDED concept anchored by replacement_tokens", superseded_replacement_problems("as-is"), False)
    expect("bible ledger", "SUPERSEDED concept with neither tokens nor replacement_tokens", superseded_replacement_problems("none"), True)
    expect("bible ledger", "SUPERSEDED concept whose replacement token is not on the page", superseded_replacement_problems("absent"), True)

    total = (1 + len(RENDERER_REJECT) + len(RENDERER_ALLOW) + len(PLATFORM_REJECT) + len(PLATFORM_ALLOW)
             + len(METRIC_REJECT) + len(METRIC_ALLOW) + 5 + len(reviews)
             + len(RENDERER_REJECT_SECOND_REVIEW) + len(PLATFORM_REJECT_SECOND_REVIEW) + len(METRIC_REJECT_SECOND_REVIEW)
             + len(RENDERER_REJECT_THIRD_REVIEW) + len(METRIC_REJECT_THIRD_REVIEW) + len(METRIC_ALLOW_THIRD_REVIEW)
             + len(METRIC_REJECT_PHASE6) + len(RENDERER_REJECT_PHASE6) + len(RENDERER_ALLOW_PHASE6) + 3
             + len(PRISM_REJECT) + len(PRISM_ALLOW) + 1)
    print(f"validator fixtures: {total} run; {failures} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
