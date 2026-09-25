# Phase-3 site errata — Phase-1/Phase-2 statements found wrong while absorbing the Bible

Collected from work-package reports; each item is re-verified against TARGET before the page is corrected (one pass, by the orchestrator).
Status: `open` until the page is fixed and the fix is recorded here.

| # | Page#anchor | Statement | TARGET fact and evidence | Reported by | Status |
|---|---|---|---|---|---|
| 1 | `docs/xna-compatibility.html#microsoftxnaframeworkgamerservices` | the 19-bone avatar rig is "verified by pixel-readback tests" | the pixel-readback tests use a synthetic one-bone quad, not the 19-bone rig | WP15 | open |
| 2 | `docs/tutorials/97-*.html` (SendDataOptions table) | gives XNA's delivery guarantees | in CNA `Reliable` is also ordered and `InOrder` can drop packets (see `deep-dives/services/network-sessions.html#guarantees`) | WP15 | open |
| 3 | `about.html` | FNA is "built on SDL2" | the FNA reference the Bible cites (`b3551247`) defaults to SDL3 — re-verify against the FNA revision CNA compares with before changing | WP01 | open |
| 4 | `docs/faq.html` (sensors answer) | the whole device layer needs `CNA_DEVICES=ON` | `modules/CMakeLists.txt` always adds the `devices` module (verify: which parts `CNA_DEVICES` gates) | WP01 | open |
| 5 | `docs/tutorials/15-background-music.html` | "after the compiled .xnb and .cnb tiers it tries .mp3, .ogg…" | a loose `.cnj` step precedes the media-native extensions (CNA-BUG-008) | B3 | open |
| 6 | `development/repository/source-ownership.html#third-party` | "Licences are in THIRD_PARTY_NOTICES.md" | the file omits vendored cgltf, stb, ENet, dr_libs (CNA-BUG-045) | B3 | open |
| 7 | `development/debugging.html`, `development/internals/modules/devices.html`, `development/takeover/validation.html` | present the TimeSpan/TSan race as a current baseline | the cited race was fixed in sharp-runtime `9c2cb0ae` (2026-07-07, before TARGET) — re-verify which sharp-runtime revision TARGET consumes | B2 | open |
| 8 | `development/internals/graphics/resources.html#registry`, `development/internals/runtime/shutdown.html#tree` | copies of state objects become aliases | only copy *assignment* (and `VertexDeclaration`'s copy constructor) aliases; see CNA-BUG-029 | B2 | open |
| 9 | `development/internals/bindings/c-api-internals.html#destroy-order` | repeats the `cna_game_destroy` comment | the comment in CNA is wrong (new B2 finding) | B2 | open |
| 10 | `docs/math-types.html#bounding-types` | "XNA 4.0's own implementation is reported to have the same limitation"; the ray case is "the only functional gap" | XNA 4.0 IL fully implements `BoundingFrustum.Intersects(Ray)`; CNA has further defects (B1: CNA-BUG-002/003) | B1 | open |
| 11 | `docs/xna-compatibility.html` (Vector3 length/distance) | reproduces "XNA's 32-bit x87 accumulation" | `modules/math/src/Vector3.cpp` sums in `float`; also the "one named hole" narrowing (boundary origins only) needs re-checking | B1 | open |
| 12 | `development/internals/modules/math.html#curves` | Curve Step parity "not established" | established: CNA's Curve tangent/Step/loop code follows FNA and diverges from XNA 4.0 IL | B1 | open |
| 13 | `docs/tutorials/04-game-lifecycle.html#constructor` | the graphics device does not exist in the constructor | it does exist in the `Game` constructor path (WP03; verify exact statement) | WP03 | open |
| 14 | `docs/getting-started.html` | calls `Present()` inside `Draw` (double present each frame) and skips base `Update`/`Draw` | fix the sample to the real lifecycle | WP03 | open |
| 15 | `docs/tutorials/47-*.html` (FPS counter) | FPS counter | counts `Update` calls, so it reports the update rate, not the frame rate | WP03 | open |
| 16 | `docs/game-loop.html` | the first `Update` has zero elapsed time | true only for a fixed time step | WP03 | open |
| 17 | `docs/render-targets.html#rendertargetusage` | `PlatformContents` is "equivalent to `DiscardContents`" | `PlatformContents` preserves (`RenderTargetUsagePreservesContentsEXT`); the Discard bind clears to black, depth 1, stencil 0 (`GraphicsDevice::SetRenderTargets`) | WP09 | open |
| 18 | `docs/tutorials/61-*.html` (Vulkan occlusion queries) | Vulkan uses `VK_QUERY_RESULT_WITH_AVAILABILITY_BIT` | `IsComplete` uses the 64-bit flag and `VK_NOT_READY` | WP09 | open |
| 19 | `docs/effects.html#spriteeffect` | SpriteBatch uses `SpriteEffect` and it sets up the projection | SpriteBatch never creates it; `SpriteEffect::OnApply()` exits at its first statement (CNA-BUG-006) | B5 | open |
| 20 | `development/internals/modules/graphics-ext.html#frame-chain` | three tests "assert parts of this order" | they assert pass counts only | B5 | open |
| 21 | `development/internals/graphics/backends.html#opengl4-and-easygl` | the OPENGL4 + EasyGL pair is "permitted by configure rules rather than evidenced" | `plans/plan_opengl4_modern_graphics.md` (GL4-0006) records a build and run of `OPENGL4;OPENGLES3;OPENGL33` — re-verify and narrow | B5 | open |
| 22 | `development/internals/graphics/device.html#resources` | WebGPU reports device loss and reset | it does so only through the debug simulation hooks; a real loss is only logged (new B5 finding) | B5 | open |
| 23 | `development/internals/modules/storage.html#boundary` | "The closure is enforced" | every CI job skips or filters out the module-link-closure gates (B6: verification gap NEW-B6-01) | B6 | open |
| 24 | `features.html`, `docs/sensors.html`, `development/testing/architecture.html#ci` | the devices workflow runs the CNA::Devices suites | it misses 7 suites; `CNA_DEVICES_GTEST_FILTER` still names renamed dialog suites (B6: CNA-BUG-035). `features.html` is protected: fix the sentence only, additively | B6 | open |
| 25 | `development/testing/index.html#recipes` | "deadlock … tracked separately" | diagnosed and fixed (VULKAN-154/157, pinned by `Sdl3XErrorHandlerTests`) | B6 | open |
| 26 | `development/internals/modules/media.html#scan` | the scan "indexes only the extensions the bundled mixer can actually play: … .opus" | `SDLMIXER_OPUS=OFF` in `cmake/ThirdPartySDL.cmake`; the ALSA mixer refuses Opus by name (`DecodeMixerAudio`) (B4: CNA-BUG-052) | B4 | open |
| 27 | `docs/tutorials/111-cnj-pipeline.html#sourcefile` | example `"sourceFile": "Textures/hero.png"` inside `Textures/hero.cnj` | `sourceFile` resolves from the `.cnj`'s own folder (`CnjSourceFile.hpp` `ResolveCnjSourceFileSafely`) | WP12 | open |
| 28 | `docs/content-manager.html#json-descriptor-formats` | Effect `vertex`/`fragment` are "relative to the descriptor" | they are content-root-relative (`ContentManager.cpp` `ReadCustomGlslEffect` → `ResolveRootRelativeSidecarPath`) | WP12 | open |
| 29 | `docs/tutorials/147-xnb-interop.html#container` | both decoders are "bounds-checked against the declared size" | LZX is compared with the declared size only at the end (`XnbDecompression.cpp`) | WP12 | open |
| 30 | `docs/tutorials/44-bounding-volumes.html` | `BoundingFrustum.Intersects(Ray)` is partial "exactly as in XNA" | XNA 4.0 implements it fully (XNA IL); CNA throws only for an origin exactly on a plane | WP04 | open |
| 31 | `docs/math-types.html#core-types` (Rectangle row) | `Contains(x, y)` has "integer and float overloads" | no float overload exists (`Rectangle.hpp`) | WP04 | open |
| 32 | `docs/math-types.html` (MathHelper) | "Mirrors … exactly"; `WithinEpsilon`, `MachineEpsilonFloat` … are "the remaining XNA constants" | those, plus `Clamp(int)` and `ClosestMSAAPower`, are FNA-internal helpers, not XNA API | WP04 | open |
| 33 | `docs/math-types.html` (Point) | lists `+ - * /` | those operators are not XNA API and carry no CNAEXT marker | WP04 | open |
| 34 | `docs/spritebatch.html#overview` | SpriteBatch "submits them to the GPU as a single batched draw" | `SpriteBatch.cpp` (`flushBatch`): one renderer call per sprite, then one native draw per texture run on GPU families; one call per sprite on SDL_RENDERER | WP05 | open |
| 35 | `docs/tutorials/21-spritebatch.html` (flush section) | describes GPU-renderer vertex batching as if every renderer did it | only the GPU families batch per texture run | WP05 | open |
| 36 | `development/repository/index.html#validators` | include reachability is a check that keeps the module map true | at TARGET the script uses an out-of-date module graph and nothing runs it (WP02) | WP02 | open |
| 37 | `docs/tutorials/109-metal-macos.html#ci` | the Metal workflow fires on pushes that touch the renderer's files | the path filter lists 3 files that no longer exist and omits the Metal CMake files | WP02 | open |
| 38 | `docs/input.html#touchpanel` | `TouchCollection.IsReadOnly` is a "known contract bug" | TARGET tests treat it as deliberate FNA parity (WP14) | WP14 | open |
| 39 | `docs/tutorials/120-xact.html#caveat-reverb` | band-pass filters are implemented | they cannot be reached from parsed XACT content (WP14) | WP14 | open |
