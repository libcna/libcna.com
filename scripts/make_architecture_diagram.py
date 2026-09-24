#!/usr/bin/env python3
"""Regenerate img/architecture-diagram.svg (and, with headless Chrome, mermaid-diagram.png).

The diagram replaces the alpha.1-era Mermaid image, which showed a retired renderer, the old
CNA_GRAPHICS_BACKEND name and an SDL-only platform layer.  Every label is a fact from the fact
sheets for CNA 009d40f5 (25 renderer identities in 21 families, 7 platform implementations, 4 audio
implementations, four independent selection axes).

    make_architecture_diagram.py [--png]
"""

from __future__ import annotations

import argparse
import html
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
W, H = 1800, 1330

out: list[str] = []
FONT = "font-family=\"Segoe UI, Helvetica, Arial, sans-serif\""


def esc(t: str) -> str:
    return html.escape(t, quote=False)


def rect(x, y, w, h, fill="#eef1f5", stroke="#7b8794", rx=6, sw=1.4, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')


def text(x, y, s, size=15, weight="normal", fill="#1f2933", anchor="middle"):
    out.append(f'<text x="{x}" y="{y}" {FONT} font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{esc(s)}</text>')


def box(x, y, w, h, lines, fill="#eef1f5", stroke="#7b8794", size=15, weight="normal", fills=None):
    rect(x, y, w, h, fill, stroke)
    if isinstance(lines, str):
        lines = [lines]
    n = len(lines)
    lh = size + 4
    y0 = y + h / 2 - (n - 1) * lh / 2 + size * 0.35
    for i, line in enumerate(lines):
        text(x + w / 2, y0 + i * lh, line, size, weight if i == 0 else "normal")
    return (x, y, w, h)


def group(x, y, w, h, title, stroke="#9aa5b1", fill="#fafbfc", color="#52606d"):
    rect(x, y, w, h, fill, stroke, rx=10, sw=1.4, dash="6 4")
    text(x + 14, y + 22, title, 14, "bold", color, "start")


def arrow(x1, y1, x2, y2, color="#52606d", dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="1.7"{d} marker-end="url(#arr)"/>')


def path_arrow(d, color="#52606d", dash=None):
    dd = f' stroke-dasharray="{dash}"' if dash else ""
    out.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.7"{dd} marker-end="url(#arr)"/>')


def bottom(b):
    return (b[0] + b[2] / 2, b[1] + b[3])


def top(b):
    return (b[0] + b[2] / 2, b[1])


def build() -> str:
    out.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
               f'aria-labelledby="t d"><title id="t">CNA architecture at snapshot 009d40f5</title>'
               f'<desc id="d">The game calls the XNA-shaped Framework API; GraphicsDevice asks the renderer selection for one of 25 renderer '
               f'identities behind IGraphicsRenderer; a platform implementation and an audio implementation, chosen independently, '
               f'sit on the target operating system.</desc>')
    out.append('<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
               '<path d="M0 0 L10 5 L0 10 z" fill="#52606d"/></marker></defs>')
    out.append(f'<rect width="{W}" height="{H}" rx="14" fill="#ffffff"/>')

    # ---- runtime flow strip -------------------------------------------------------------
    group(20, 14, 1760, 92, "Runtime flow")
    names = ["main", "Game.Run", "Initialize", "LoadContent", "Update (fixed or variable step)", "Draw", "Present"]
    xs = [60, 260, 470, 690, 930, 1290, 1500]
    ws = [140, 160, 170, 190, 300, 140, 160]
    bx = []
    for n, x, w in zip(names, xs, ws):
        bx.append(box(x, 44, w, 46, n, "#f4f6f8"))
    for a, b in zip(bx, bx[1:]):
        arrow(a[0] + a[2], 67, b[0], 67)
    path_arrow(f"M{bx[6][0] + bx[6][2] / 2} 90 C {bx[6][0] + bx[6][2] / 2} 108, {bx[4][0] + bx[4][2] / 2} 108, {bx[4][0] + bx[4][2] / 2} 90")

    # ---- framework ------------------------------------------------------------------------
    g = box(700, 140, 400, 48, ["Your game / ported application"], "#e3f2fd", "#5b9bd5", 16, "bold")
    fw = box(620, 226, 560, 52, ["Microsoft::Xna::Framework  (XNA-shaped API, C++23)", "3,627 / 3,627 documented runtime members represented"], "#e3f2fd", "#5b9bd5", 15, "bold")
    arrow(*bottom(g), *top(fw))
    subs = [
        ("Game · GameTime", ["Game, GameTime", "GameComponent"]),
        ("GraphicsDeviceManager", ["GraphicsDevice-", "Manager"]),
        ("GraphicsDevice", ["GraphicsDevice", "SpriteBatch · Texture2D", "Effects · Models"]),
        ("Input", ["Input", "Keyboard · Mouse", "GamePad · Touch"]),
        ("Audio / Media", ["Audio · Media", "XACT · Video"]),
        ("Content", ["ContentManager", ".xnb → .cnb → loose"]),
        ("Services", ["Storage · Net", "GamerServices · Devices"]),
    ]
    sx, sw_, gap = 40, 218, 18
    boxes = []
    for i, (_, lines) in enumerate(subs):
        boxes.append(box(sx + i * (sw_ + gap), 336, sw_, 74, lines, "#f4f6f8"))
    for b in boxes:
        path_arrow(f"M{fw[0] + fw[2] / 2} {fw[1] + fw[3]} C {fw[0] + fw[2] / 2} 300, {b[0] + b[2] / 2} 300, {b[0] + b[2] / 2} 336")
    sharp = box(1590, 226, 190, 52, ["sharp-runtime", "System.* (branch next)"], "#fff8e1", "#d0a52a", 15, "bold")
    arrow(fw[0] + fw[2], 252, sharp[0], 252)

    # ---- renderer selection ---------------------------------------------------------------
    gd = boxes[2]
    sel = box(500, 470, 800, 66, ["GraphicsRendererSelection + renderer registry",
                                   "SetPreferred() › env variable / Emscripten Module property › build default", "fallback is off unless enabled · the choice latches on the first device"],
              "#f3e5f5", "#9b6bb0", 14, "bold")
    path_arrow(f"M{gd[0] + gd[2] / 2} {gd[1] + gd[3]} C {gd[0] + gd[2] / 2} 440, 900 440, 900 470")
    ir = box(500, 578, 800, 66, ["IGraphicsRenderer  (pure virtual) + RendererDescriptor",
                                  "19 GraphicsCapability members · RendererCapabilityProfile: 32 features, 22 limits, per-format usage"],
             "#f3e5f5", "#9b6bb0", 14, "bold")
    arrow(900, 536, 900, 578)

    # ---- side panels: build-time selection and sprite draw flow ---------------------------------
    group(40, 460, 420, 190, "Build-time selection")
    box(60, 490, 380, 40, ["CNA_GRAPHICS_RENDERER=<one of the 25>"], "#f4f6f8", size=13)
    box(60, 538, 380, 40, ["CNA_GRAPHICS_RENDERERS=\"A;B;C\"  (compatible set)"], "#f4f6f8", size=13)
    box(60, 586, 380, 44, ["default: WEBGL2 (Emscripten) · OPENGLES3 (Linux)", "SDL_RENDERER (everything else)"], "#f4f6f8", size=13)
    group(1340, 460, 420, 190, "Sprite draw flow")
    sf = [box(1360, 486, 180, 32, "SpriteBatch.Begin", "#f4f6f8", size=13), box(1560, 486, 180, 32, "SpriteBatch.Draw", "#f4f6f8", size=13),
          box(1360, 536, 180, 32, "SpriteBatch.End", "#f4f6f8", size=13), box(1560, 536, 180, 32, "GraphicsDevice", "#f4f6f8", size=13),
          box(1360, 588, 380, 44, ["renderer draw call", "GPU, browser DOM/Canvas or CPU framebuffer"], "#f4f6f8", size=13)]
    arrow(1540, 502, 1560, 502); path_arrow("M1650 518 C 1650 530, 1450 520, 1450 536"); arrow(1540, 552, 1560, 552); path_arrow("M1650 568 C 1650 578, 1550 578, 1550 588")

    # ---- renderer groups ----------------------------------------------------------------------
    group(40, 690, 1720, 250, "25 public renderer identities in 21 implementation families  (one binary, or several with CNA_GRAPHICS_RENDERERS)")
    g1 = (60, 722, 890, 200)
    rect(*g1, fill="#e8f5e9", stroke="#5fae68", rx=8)
    text(g1[0] + 14, g1[1] + 22, "GPU renderers (14 identities, 3D + 2D)", 14, "bold", "#2e7d32", "start")
    gpu = [("OPENGLES2 · OPENGLES3 · OPENGL33", "WEBGL1 · WEBGL2   (five identities, one EasyGL family)"),
           ("OPENGL4", "desktop GL 4.1+ core"), ("VULKAN", ""), ("SDL_GPU", "SDL3 GPU API"), ("WEBGPU", "native + browser"),
           ("METAL", "macOS"), ("FNA3D", "FNA3D adapter"), ("DIRECTX9 · DIRECTX11 · DIRECTX12", "Windows")]
    cells = [(70, 752, 430, 70), (510, 752, 130, 70), (650, 752, 130, 70), (790, 752, 150, 70),
             (70, 832, 200, 70), (280, 832, 130, 70), (420, 832, 130, 70), (560, 832, 380, 70)]
    for (a, b), (x, y, w, h) in zip(gpu, cells):
        box(x, y, w, h, [a] + ([b] if b else []), "#ffffff", "#5fae68", 13, "bold")
    g2 = (970, 722, 400, 200)
    rect(*g2, fill="#fff3e0", stroke="#e0a040", rx=8)
    text(g2[0] + 14, g2[1] + 22, "2D-only renderers (7)", 14, "bold", "#b26a00", "start")
    for i, n in enumerate([["SDL_RENDERER", "FREEDIRECT"], ["DIRECT2D", "GDI"], ["CANVAS", "HTML_DOM"], ["SVG_DOM"]]):
        for j, name in enumerate(n):
            box(980 + j * 195, 752 + i * 40, 185, 34, name, "#ffffff", "#e0a040", 13, "bold")
    g3 = (1390, 722, 350, 200)
    rect(*g3, fill="#eceff1", stroke="#78909c", rx=8)
    text(g3[0] + 14, g3[1] + 22, "CPU and no-pixel (4)", 14, "bold", "#455a64", "start")
    for i, (n, sub) in enumerate([("SOFTWARE", "CPU rasterizer"), ("PORTABLEGL", "CPU OpenGL 3.x"), ("HEADLESS", "validates and traces"), ("STUB", "renders nothing")]):
        box(1400 + (i % 2) * 165, 752 + (i // 2) * 80, 155, 70, [n, sub], "#ffffff", "#78909c", 13, "bold")
    arrow(900, 644, 900, 690)

    # ---- platform / audio / OS -----------------------------------------------------------------------
    plat = box(40, 990, 820, 96, ["Platform implementation  ·  CNA_PLATFORM  (default SDL3)",
                                   "SDL3 · SDL2 · X11 · WAYLAND · WIN32 · HEADLESS · TERMINAL",
                                   "X11, Wayland and Win32 are native (no SDL); CNA_ENABLE_SDL=AUTO | ON | OFF"], "#e0f2f1", "#4db6ac", 14, "bold")
    aud = box(900, 990, 500, 96, ["Audio implementation  ·  CNA_AUDIO_PLATFORM  (default SDL3)",
                                   "SDL3 · SDL2 · ALSA · NULL",
                                   "SOUND_ENABLED (XNA playback mixer): SDL3 and ALSA"], "#e0f2f1", "#4db6ac", 14, "bold")
    ext = box(1440, 990, 320, 96, ["Optional layers (off by default)", "CNAEXT engine layer · Diagnostics", "Inspector · experimental C ABI 0.29.0"], "#f3f4f6", "#9aa5b1", 13, "bold")
    arrow(400, 940, 400, 990)
    path_arrow("M1150 936 L1150 990", "#52606d")
    os_ = box(40, 1150, 1360, 62, ["Target operating system:  Linux · Windows (MSVC, MinGW-w64) · macOS · iOS · Android · WebAssembly (Emscripten)"], "#eceff1", "#78909c", 15, "bold")
    arrow(450, 1086, 450, 1150)
    arrow(1150, 1086, 1150, 1150)

    # ---- build-time / content pipeline -------------------------------------------------------------------
    bt = box(1440, 1150, 320, 62, ["Build-time only", "cna-content → .xnb / .cnb"], "#fff8e1", "#d0a52a", 14, "bold")
    arrow(1600, 1086, 1600, 1150, "#b0bcc5", "5 4")
    text(900, 1256, "Four independent axes: target operating system · platform implementation · graphics renderer · audio implementation.", 14, "normal", "#52606d")
    text(900, 1280, "A name outside the 25 renderer identities is a CMake configure error; nothing falls back silently.", 14, "normal", "#52606d")
    text(900, 1310, "CNA snapshot 009d40f5 (24 September 2026, branch next)  ·  libcna.com", 13, "normal", "#7b8794")
    out.append("</svg>")
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--png", action="store_true", help="also render mermaid-diagram.png with headless Chrome")
    args = ap.parse_args()
    svg = build()
    target = ROOT / "img" / "architecture-diagram.svg"
    target.parent.mkdir(exist_ok=True)
    target.write_text(svg, encoding="utf-8")
    print(f"wrote {target.relative_to(ROOT)}")
    if args.png:
        chrome = shutil.which("google-chrome") or shutil.which("chromium")
        if not chrome:
            print("no Chrome available; PNG not rendered", file=sys.stderr)
            return 1
        png = ROOT / "mermaid-diagram.png"
        subprocess.run([chrome, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                        f"--window-size={W},{H}", "--force-device-scale-factor=1", f"--screenshot={png}", target.as_uri()],
                       check=True, capture_output=True)
        print("wrote mermaid-diagram.png")
    return 0


if __name__ == "__main__":
    sys.exit(main())
