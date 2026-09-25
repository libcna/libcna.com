#!/usr/bin/env python3
"""Headless-Chrome QA harness (Chrome DevTools Protocol over a local websocket; no extra dependencies beyond
`websocket-client`).  Serves nothing itself: point it at a running static server (python3 -m http.server).

    browser_qa.py shot  URL OUT.png [--width 1400] [--height 900] [--scheme dark|light] [--full]
    browser_qa.py check URL [URL ...] [--width 1400] [--scheme dark|light]
    browser_qa.py sweep URL_LIST_FILE [--out DIR]     # every URL x {1400 dark, 1400 light, 390 dark, 390 light}

`check` reports, per URL/viewport/scheme: horizontal overflow (document wider than the viewport, and the widest
offending elements), the number of rows the global header occupies, console errors, images that failed to load,
and the lowest text/background contrast ratio among visible body text.  `sweep` writes screenshots too.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import websocket  # websocket-client

PORT = 9333
PROFILE = Path(os.environ.get("QA_PROFILE", "/tmp/claude-1000/qa-chrome-profile"))

JS_METRICS = r"""
(() => {
  const de = document.documentElement;
  const vw = de.clientWidth;
  const over = [];
  for (const el of document.querySelectorAll('body *')) {
    const r = el.getBoundingClientRect();
    if (r.width > 0 && r.right > vw + 1 && getComputedStyle(el).position !== 'fixed') {
      // ignore anything inside an element that scrolls on its own
      let p = el.parentElement, scrolls = false;
      while (p) { const ox = getComputedStyle(p).overflowX; if (ox === 'auto' || ox === 'scroll' || ox === 'hidden') { scrolls = true; break; } p = p.parentElement; }
      if (!scrolls) over.push(el.tagName.toLowerCase() + (el.className ? '.' + String(el.className).split(' ')[0] : '') + ' right=' + Math.round(r.right));
    }
  }
  const menu = document.querySelector('.nav-menu');
  let rows = 0;
  if (menu && getComputedStyle(menu).display !== 'none') {
    const tops = new Set([...menu.children].map(c => Math.round(c.getBoundingClientRect().top)));
    rows = tops.size;
  }
  // contrast of visible text (sampled)
  function parse(c) { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(',').map(Number); return {r:p[0],g:p[1],b:p[2],a:p.length>3?p[3]:1}; }
  function lum(c) { const f = v => { v/=255; return v<=0.03928? v/12.92 : Math.pow((v+0.055)/1.055,2.4); }; return 0.2126*f(c.r)+0.7152*f(c.g)+0.0722*f(c.b); }
  function bgOf(el) { let e = el; while (e) { const c = parse(getComputedStyle(e).backgroundColor); if (c && c.a > 0.5) return c; e = e.parentElement; } return {r:255,g:255,b:255,a:1}; }
  let worst = 99, worstEl = '';
  const seen = new Set();
  for (const el of document.querySelectorAll('main p, main li, main td, main th, main h1, main h2, main h3, main a, main code, main span, main dd, main dt')) {
    if (!el.childNodes.length || ![...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) continue;
    const r = el.getBoundingClientRect(); if (r.width === 0 || r.height === 0) continue;
    if (el.closest('.toc-title, .section-label, .dev-pager span')) continue;  // shared, pre-existing muted labels
    const cs = getComputedStyle(el); if (cs.visibility === 'hidden') continue;
    const fg = parse(cs.color), bg = bgOf(el); if (!fg) continue;
    const key = cs.color + '|' + JSON.stringify(bg); if (seen.has(key)) continue; seen.add(key);
    const l1 = lum(fg), l2 = lum(bg); const ratio = (Math.max(l1,l2)+0.05)/(Math.min(l1,l2)+0.05);
    if (ratio < worst) { worst = ratio; worstEl = el.tagName.toLowerCase() + ' "' + el.textContent.trim().slice(0,30) + '" ' + cs.color; }
  }
  const broken = [...document.images].filter(i => i.complete && i.naturalWidth === 0).map(i => i.src);
  return JSON.stringify({vw, sw: de.scrollWidth, over: over.slice(0,6), navRows: rows, worstContrast: Math.round(worst*100)/100, worstEl, brokenImages: broken,
                         title: document.title, theme: de.getAttribute('data-theme') || 'auto'});
})()
"""


class Chrome:
    def __init__(self) -> None:
        PROFILE.mkdir(parents=True, exist_ok=True)
        self.proc = subprocess.Popen(
            ["google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
             f"--remote-debugging-port={PORT}", f"--user-data-dir={PROFILE}", "about:blank"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(60):
            try:
                urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=1)
                break
            except Exception:
                time.sleep(0.25)
        req = urllib.request.Request(f"http://127.0.0.1:{PORT}/json/new?about:blank", method="PUT")
        tab = json.load(urllib.request.urlopen(req, timeout=5))
        self.ws = websocket.create_connection(tab["webSocketDebuggerUrl"], timeout=30, suppress_origin=True)
        self.n = 0
        self.console: list[str] = []
        self.call("Page.enable")
        self.call("Runtime.enable")
        self.call("Log.enable")

    def call(self, method: str, **params):
        self.n += 1
        mid = self.n
        self.ws.send(json.dumps({"id": mid, "method": method, "params": params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("method") == "Runtime.consoleAPICalled" and msg["params"]["type"] in ("error", "assert"):
                self.console.append(" ".join(str(a.get("value", a.get("description", ""))) for a in msg["params"]["args"]))
            if msg.get("method") == "Log.entryAdded" and msg["params"]["entry"]["level"] == "error":
                self.console.append(msg["params"]["entry"]["text"] + " " + msg["params"]["entry"].get("url", ""))
            if msg.get("id") == mid:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error']}")
                return msg.get("result", {})

    def open(self, url: str, width: int, height: int, scheme: str) -> None:
        self.console.clear()
        mobile = width < 700
        self.call("Emulation.setDeviceMetricsOverride", width=width, height=height, deviceScaleFactor=1, mobile=mobile)
        self.call("Emulation.setEmulatedMedia", features=[{"name": "prefers-color-scheme", "value": scheme}])
        self.call("Page.navigate", url=url)
        deadline = time.time() + 30
        while time.time() < deadline:
            state = self.call("Runtime.evaluate", expression="document.readyState")["result"].get("value")
            if state == "complete":
                break
            time.sleep(0.15)
        time.sleep(0.4)

    def eval(self, js: str):
        r = self.call("Runtime.evaluate", expression=js, returnByValue=True, awaitPromise=True)
        return r["result"].get("value")

    def shot(self, out: Path, full: bool = False) -> None:
        params = {"format": "png"}
        if full:
            dims = self.eval("JSON.stringify([document.documentElement.scrollWidth, document.documentElement.scrollHeight])")
            w, h = json.loads(dims)
            params.update(captureBeyondViewport=True, clip={"x": 0, "y": 0, "width": w, "height": min(h, 6000), "scale": 1})
        data = self.call("Page.captureScreenshot", **params)["data"]
        out.write_bytes(base64.b64decode(data))

    def close(self) -> None:
        try:
            self.ws.close()
        finally:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=5)
            except Exception:
                self.proc.kill()


def report(ch: Chrome, url: str, w: int, scheme: str) -> dict:
    ch.open(url, w, 900, scheme)
    m = json.loads(ch.eval(JS_METRICS))
    m["console"] = [c for c in ch.console if "favicon" not in c][:4]
    m["url"], m["width"], m["scheme"] = url, w, scheme
    return m


def line(m: dict) -> str:
    flags = []
    if m["sw"] > m["vw"] + 1:
        flags.append(f"H-OVERFLOW {m['sw']}>{m['vw']} {m['over']}")
    if m["worstContrast"] < 4.5:
        flags.append(f"LOW-CONTRAST {m['worstContrast']} {m['worstEl']}")
    if m["brokenImages"]:
        flags.append(f"BROKEN-IMG {m['brokenImages']}")
    if m["console"]:
        flags.append(f"CONSOLE {m['console']}")
    status = "FLAG" if flags else "ok"
    return f"{status:4s} {m['width']:4d} {m['scheme']:5s} navRows={m['navRows']} contrast>={m['worstContrast']} {m['url']}" + ("\n      " + "\n      ".join(flags) if flags else "")


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("shot")
    s.add_argument("url")
    s.add_argument("out")
    s.add_argument("--width", type=int, default=1400)
    s.add_argument("--height", type=int, default=900)
    s.add_argument("--scheme", default="dark")
    s.add_argument("--full", action="store_true")
    c = sub.add_parser("check")
    c.add_argument("urls", nargs="+")
    c.add_argument("--width", type=int, action="append")
    c.add_argument("--scheme", action="append")
    w = sub.add_parser("sweep")
    w.add_argument("list_file")
    w.add_argument("--out", default="")
    w.add_argument("--full", action="store_true")
    args = ap.parse_args()
    ch = Chrome()
    rc = 0
    try:
        if args.cmd == "shot":
            ch.open(args.url, args.width, args.height, args.scheme)
            ch.shot(Path(args.out), args.full)
            print("wrote", args.out)
        elif args.cmd == "check":
            for url in args.urls:
                for wd in args.width or [1400]:
                    for sc in args.scheme or ["dark"]:
                        m = report(ch, url, wd, sc)
                        print(line(m))
                        rc |= 1 if "FLAG" in line(m)[:4] else 0
        else:
            out = Path(args.out) if args.out else None
            if out:
                out.mkdir(parents=True, exist_ok=True)
            for url in Path(args.list_file).read_text().split():
                for wd, sc in ((1400, "dark"), (1400, "light"), (390, "dark"), (390, "light")):
                    m = report(ch, url, wd, sc)
                    print(line(m))
                    rc |= 1 if line(m).startswith("FLAG") else 0
                    if out:
                        name = url.split("127.0.0.1:8765/")[-1].replace("/", "_").replace(".html", "")
                        ch.shot(out / f"{name}-{wd}-{sc}.png", args.full)
    finally:
        ch.close()
    return rc


if __name__ == "__main__":
    sys.exit(main())
