# Worklist — Apple / macOS / iOS / Metal / C API-on-macOS / CNA.NET-on-macOS claims on libcna.com (CNA `b0e97bb1` → `c1c316b9`)

Internal audit record (not served). Research only: no page was edited, nothing was built or run.

- **Line numbers are libcna.com `HEAD` = `7f0dbaa` line numbers** (`git show HEAD:<path>`), because pages are being edited concurrently;
  every row also carries an exact text excerpt so it can be found after other edits.
- **Authorities:** `R2-apple-m4.md` (Apple/macOS/iOS/Metal; "R2 §n"), `R3-c-api-cna-net.md` (C ABI, C API on macOS, CNA.NET; "R3 §n"), CNA at `c1c316b9`
  (`file:line`), and `plans/plan_apple_m4.md` task ids (`AM4-nnn`).
- **Classes:** STALE = must change; CURRENT = still true at `c1c316b9`; OK-GENERIC = incidental (renderer lists, OS lists reached through SDL3, link labels).
  Only STALE items are tabulated with replacements; CURRENT items are listed briefly per page; OK-GENERIC are counted.
- **Policy honoured by every proposed replacement:** no retired renderer identity (the four retired in this delta or earlier ones) is named, not even as
  "removed"; 14 public renderer identities over 12 families; `CNA_PLATFORM` = `SDL3 | HEADLESS | TERMINAL` (Windows/X11/Wayland/macOS/iOS/Android/browser
  through SDL3's video drivers, removal never described); C ABI 0.46.0. Where an Apple sentence also carried a policy violation, the replacement fixes both
  (tagged [policy-a]/[policy-b]/[policy-c]). Two places need an owner/lead wording decision: how (or whether) to describe ABI 0.45.0
  (Part 2, docs/c-api.html:140) and link labels pointing at known-issue pages that will be retired (Part 4).
- **Evidence wording to keep consistent** (see R2 §1-§3, §7, §8): "tested on a physical Mac mini M4 (Apple M4, 16 GB, macOS 27.0.1, Xcode 27, Apple clang 21)";
  "console locked — on-screen presentation not observed"; METAL "SUPPORTED, not primary-production"; "iOS Simulator pixel probe (iPhone 17 profile), exact in
  8 of 8 launches; device build final-linked, never run"; "C API built and tested locally on macOS; no CI job builds it"; "CNA.NET osx-arm64: local evidence,
  not a shipping claim"; repository `libcna/cna-dotnet` (formerly `cna-cs`).

## Structure

1. **Part 1 — key pages** (22 pages: platforms, rendering backends, tutorial 109, building, features, index, roadmap, verification, FAQ, deep dives on Apple
   platforms / GPU evidence tiers / cross-platform contract, …). Surveyed per regex hit; counts reconcile per page.
2. **Part 2 — C API and CNA.NET pages** (docs/c-api, the two C API deep dives, C API internals, tutorial 129, docs/cna-net, migrating-to-cna-net, tutorials 170/171,
   C# binding internals) plus every `cna-cs` → `cna-dotnet` rename elsewhere.
3. **Part 3 — cross-site C ABI 0.44.0 → 0.46.0** (mechanical, with rules A–F; may overlap single rows of Parts 1 and 5, which are tagged [policy-c]/[R3] there).
4. **Part 4 — known issues** (generated pages: edit `audit/data/bible/issues/issues-source.json`, then `python3 scripts/known_issues.py build`).
5. **Part 5 — long tail** (198 further pages; pages with only CURRENT/OK-GENERIC hits are in a compact table there).

## STALE counts by file

Counts are STALE rows (Parts 1, 2, 5) or STALE lines (Part 3). A few items are counted in two parts (Part 3 vs a [policy-c] row of Part 1/5).
Known-issue pages are not in this table: **Part 4 lists 15 issue entries to change** (6 retire as fixed: CNA-GAP-013, CNA-GAP-028, CNA-BUG-199, CNA-VGAP-019,
CNA-BUG-190, CNA-BUG-012 after re-verification; 6 narrow: CNA-VGAP-024, CNA-VGAP-008, CNA-BUG-094, CNA-VGAP-025, CNA-VGAP-021, CNA-GAP-009; 3 number updates:
CNA-BUG-056, CNA-GAP-062, CNA-BUG-058), plus title policy fixes on CNA-BUG-133/134.

| File | STALE total | Part 1 (key pages) | Part 2 (C API / CNA.NET) | Part 3 (ABI 0.44.0 lines) | Part 5 (long tail) |
|---|---:|---:|---:|---:|---:|
| docs/tutorials/109-metal-macos.html | 53 | 53 |  |  |  |
| docs/platforms.html | 28 | 28 |  |  |  |
| docs/c-api.html | 26 |  | 26 |  |  |
| features.html | 25 | 20 |  | 5 |  |
| docs/rendering-backends.html | 24 | 23 |  | 1 |  |
| roadmap.html | 15 | 12 | 1 | 2 |  |
| deep-dives/platforms/android-and-apple-platforms.html | 14 | 14 |  |  |  |
| deep-dives/reference/c-api-evidence-and-gates.html | 14 |  | 14 |  |  |
| docs/building.html | 11 | 9 |  | 2 |  |
| docs/roadmap.html | 11 | 9 |  | 2 |  |
| docs/migrating-to-cna-net.html | 10 |  | 10 |  |  |
| deep-dives/renderers/native-gpu-evidence-tiers.html | 9 | 9 |  |  |  |
| docs/3d-rendering.html | 9 |  |  |  | 9 |
| docs/cna-net.html | 9 |  | 9 |  |  |
| docs/verification.html | 9 | 7 |  | 2 |  |
| docs/faq.html | 8 | 5 | 1 | 2 |  |
| docs/tutorials/72-backend-selection.html | 8 |  |  |  | 8 |
| docs/tutorials/80-cross-platform.html | 8 |  |  |  | 8 |
| deep-dives/platforms/cross-platform-contract.html | 7 | 7 |  |  |  |
| development/architecture/bindings.html | 7 |  | 1 | 6 |  |
| development/internals/bindings/c-api-internals.html | 7 |  | 7 |  |  |
| development/internals/bindings/csharp.html | 7 |  | 7 |  |  |
| development/takeover/uncertainty.html | 7 |  | 1 | 3 | 3 |
| docs/render-targets.html | 7 |  |  |  | 7 |
| showcase.html | 7 | 6 | 1 |  |  |
| architecture.html | 6 | 4 |  | 2 |  |
| development/handbook/update-the-c-api.html | 6 |  | 1 | 5 |  |
| development/internals/bindings/java.html | 6 |  |  | 6 |  |
| development/workflows.html | 6 |  | 1 | 2 | 3 |
| docs/runtime-renderer-selection.html | 6 |  |  | 2 | 4 |
| docs/tutorials/129-c-api-first-program.html | 6 |  | 6 |  |  |
| index.html | 6 | 2 | 1 | 3 |  |
| development/internals/bindings/python.html | 5 |  |  | 5 |  |
| development/testing/architecture.html | 5 |  |  | 2 | 3 |
| docs/effects.html | 5 |  |  |  | 5 |
| docs/native-platforms.html | 5 | 5 |  |  |  |
| docs/tutorials/170-run-xna-csharp-game-on-cna-net.html | 5 |  | 5 |  |  |
| docs/tutorials/171-cna-net-template.html | 5 |  | 5 |  |  |
| docs/tutorials/62-mrt.html | 5 |  |  |  | 5 |
| about.html | 4 | 2 |  | 2 |  |
| development/handbook/make-a-release.html | 4 |  |  | 2 | 2 |
| development/repository/index.html | 4 |  |  | 2 | 2 |
| docs/getting-started.html | 4 | 3 | 1 |  |  |
| docs/tutorials/114-pbr-materials.html | 4 |  |  |  | 4 |
| deep-dives/build/configuring-cna.html | 3 |  |  |  | 3 |
| deep-dives/graphics/shader-routes-four-answers.html | 3 |  |  |  | 3 |
| deep-dives/graphics/state-objects.html | 3 |  |  |  | 3 |
| deep-dives/reference/glossary.html | 3 |  |  | 1 | 2 |
| deep-dives/reference/native-c-api.html | 3 |  | 3 |  |  |
| development/debugging.html | 3 |  |  | 1 | 2 |
| development/handbook/change-map.html | 3 |  | 1 | 1 | 1 |
| development/internals/graphics/selection.html | 3 |  |  |  | 3 |
| development/reference/cmake-options.html | 3 |  |  |  | 3 |
| docs/releases.html | 3 |  |  | 3 |  |
| docs/tutorials/02-setup.html | 3 |  |  |  | 3 |
| docs/tutorials/151-one-shader-several-renderers.html | 3 |  |  |  | 3 |
| docs/tutorials/61-occlusion-query.html | 3 |  |  |  | 3 |
| docs/tutorials/65-msaa.html | 3 |  |  |  | 3 |
| docs/tutorials/67-deferred-rendering.html | 3 |  |  |  | 3 |
| docs/xna-compatibility.html | 3 |  |  |  | 3 |
| contribute.html | 2 |  |  |  | 2 |
| deep-dives/foundations/cna-and-xna.html | 2 |  |  | 2 |  |
| deep-dives/foundations/compatibility-and-evidence.html | 2 |  |  |  | 2 |
| deep-dives/reference/gltf-evidence-matrix.html | 2 |  |  |  | 2 |
| deep-dives/reference/index.html | 2 |  |  | 2 |  |
| deep-dives/reference/verification-tiers.html | 2 | 2 |  |  |  |
| deep-dives/renderers/presentation-and-backbuffer-readback.html | 2 |  |  |  | 2 |
| deep-dives/renderers/sdl-gpu-resources-and-frame-recovery.html | 2 |  |  |  | 2 |
| deep-dives/sharp-runtime/parity-and-verification.html | 2 |  |  |  | 2 |
| development/build/index.html | 2 |  |  |  | 2 |
| development/internals/graphics/backends.html | 2 |  |  |  | 2 |
| development/internals/graphics/sdl-gpu.html | 2 |  |  |  | 2 |
| development/internals/modules/gamer-services.html | 2 |  |  |  | 2 |
| development/internals/modules/storage.html | 2 |  |  | 1 | 1 |
| development/reference/public-headers.html | 2 |  |  | 2 |  |
| development/reference/test-targets.html | 2 |  |  | 1 | 1 |
| development/repository/module-graph.html | 2 |  |  |  | 2 |
| development/repository/source-ownership.html | 2 |  |  | 1 | 1 |
| development/takeover/inherited.html | 2 |  |  | 1 | 1 |
| development/takeover/investigation.html | 2 |  | 1 | 1 |  |
| docs/cnaext-extensions.html | 2 |  |  | 1 | 1 |
| docs/cnb-format.html | 2 |  |  | 1 | 1 |
| docs/shader-effects.html | 2 |  |  |  | 2 |
| docs/tutorials/100-shipping.html | 2 |  |  |  | 2 |
| docs/tutorials/146-cnb-packs.html | 2 |  |  | 1 | 1 |
| docs/tutorials/152-graphics-profiles.html | 2 |  |  |  | 2 |
| docs/tutorials/168-operate-gamer-services-server.html | 2 |  |  |  | 2 |
| docs/tutorials/52-custom-shaders.html | 2 |  |  |  | 2 |
| docs/tutorials/60-instancing.html | 2 |  |  |  | 2 |
| docs/tutorials/64-cubemaps.html | 2 |  |  |  | 2 |
| docs/tutorials/66-bloom.html | 2 |  |  |  | 2 |
| documentation.html | 2 |  |  | 2 |  |
| deep-dives/build/third-party-dependencies.html | 1 |  |  |  | 1 |
| deep-dives/foundations/ecosystem.html | 1 |  | 1 |  |  |
| deep-dives/models/gltf-conformance.html | 1 |  |  |  | 1 |
| deep-dives/models/gltf-import.html | 1 |  |  |  | 1 |
| deep-dives/platforms/index.html | 1 | 1 |  |  |  |
| deep-dives/practice/project-records-and-evidence.html | 1 |  |  | 1 |  |
| deep-dives/reference/ecosystem-quick-reference.html | 1 |  | 1 |  |  |
| deep-dives/renderers/render-targets-clears-and-viewports.html | 1 |  |  |  | 1 |
| deep-dives/renderers/renderer-contract.html | 1 |  |  |  | 1 |
| deep-dives/renderers/sdl-renderer-2d-contract.html | 1 |  |  |  | 1 |
| deep-dives/services/avatars.html | 1 |  |  |  | 1 |
| deep-dives/services/gamer-services-contract.html | 1 |  |  |  | 1 |
| deep-dives/services/network-sessions.html | 1 |  |  |  | 1 |
| development/architecture/platform.html | 1 |  |  |  | 1 |
| development/handbook/change-build-configuration.html | 1 |  |  |  | 1 |
| development/handbook/change-public-xna-behavior.html | 1 |  | 1 |  |  |
| development/handbook/update-libcna-com.html | 1 |  |  | 1 |  |
| development/internals/graphics/draw-call.html | 1 |  |  |  | 1 |
| development/internals/platforms/sdl3.html | 1 |  |  |  | 1 |
| development/invariants.html | 1 |  |  |  | 1 |
| development/reference/modules.html | 1 |  |  |  | 1 |
| development/takeover/blast-radius.html | 1 |  |  | 1 |  |
| development/takeover/index.html | 1 |  |  | 1 |  |
| development/takeover/mental-model.html | 1 |  |  | 1 |  |
| development/takeover/validation.html | 1 |  |  |  | 1 |
| development/takeover/worked-changes.html | 1 |  |  | 1 |  |
| docs/gamer-services.html | 1 |  |  |  | 1 |
| docs/graphics-state.html | 1 |  |  |  | 1 |
| docs/migration-from-monogame.html | 1 |  |  |  | 1 |
| docs/tutorials/01-introduction.html | 1 |  |  |  | 1 |
| docs/tutorials/101-renderer-capabilities.html | 1 |  |  |  | 1 |
| docs/tutorials/116-post-process-effects.html | 1 |  |  |  | 1 |
| docs/tutorials/117-devices-layer.html | 1 |  |  |  | 1 |
| docs/tutorials/121-video-playback.html | 1 |  |  |  | 1 |
| docs/tutorials/123-achievements.html | 1 |  |  |  | 1 |
| docs/tutorials/126-multi-renderer-build.html | 1 |  |  |  | 1 |
| docs/tutorials/128-compiled-xna-effects.html | 1 |  |  |  | 1 |
| docs/tutorials/131-sdl-gpu.html | 1 |  |  |  | 1 |
| docs/tutorials/132-webgpu.html | 1 |  |  |  | 1 |
| docs/tutorials/133-renderer-capability-profile.html | 1 |  |  | 1 |  |
| docs/tutorials/162-gamer-services-setup.html | 1 |  |  |  | 1 |
| docs/tutorials/163-guide-system-ui.html | 1 |  |  |  | 1 |
| docs/tutorials/164-gamer-services-server.html | 1 |  |  |  | 1 |
| docs/tutorials/165-friends-presence.html | 1 |  |  |  | 1 |
| docs/tutorials/166-online-sessions.html | 1 |  |  |  | 1 |
| docs/tutorials/167-avatars.html | 1 |  |  |  | 1 |
| docs/tutorials/24-post-processing.html | 1 |  |  |  | 1 |
| docs/tutorials/49-touch-input.html | 1 |  |  |  | 1 |
| docs/tutorials/53-effect-parameter.html | 1 |  |  |  | 1 |
| docs/tutorials/58-normal-mapping.html | 1 |  |  |  | 1 |
| docs/tutorials/59-shadow-mapping.html | 1 |  |  |  | 1 |
| docs/tutorials/63-stencil-buffer.html | 1 |  |  |  | 1 |
| docs/tutorials/68-terrain.html | 1 |  |  |  | 1 |
| docs/tutorials/69-water.html | 1 |  |  |  | 1 |
| docs/tutorials/75-lod.html | 1 |  |  |  | 1 |
| docs/tutorials/79-debugging.html | 1 |  |  |  | 1 |
| docs/tutorials/85-vulkan-backend.html | 1 |  |  |  | 1 |
| docs/tutorials/87-custom-backend.html | 1 |  |  |  | 1 |
| docs/tutorials/88-device-layer.html | 1 |  |  |  | 1 |
| docs/tutorials/97-networking.html | 1 |  |  |  | 1 |
| docs/video-playback.html | 1 |  |  |  | 1 |
| docs/vs-alternatives.html | 1 |  |  |  | 1 |
| **Total (public pages)** | **611** | **221** | **106** | **87** | **197** |

---

# Part 1 — Key pages (Apple claims)

> Worklist A — Apple / macOS / iOS / Metal (+ C API and CNA.NET on macOS) refresh, b0e97bb1 → c1c316b9

Scope: 22 pages, read at libcna.com `HEAD` = `7f0dbaa` (`git show HEAD:<path>`); **all line numbers are HEAD line numbers**.
Authority: `audit/data/facts/c1c316b9/R2-apple-m4.md` (cited "R2 §n") and `R3-c-api-cna-net.md` ("R3 §n"); spot checks in the CNA clone at `c1c316b9` cited as `file:line`.

Counting rule: one classification per **source line that matches the Apple regex** (case-insensitive
`macos|mac os|\bios\b|iphone|ipad|\bmetal\b|apple|xcode|\bmac\b|mac mini|cocoa|uikit|osx|darwin|mach-o|dylib|\bm4\b`),
plus explicitly added items (marked "+extra") for C-API/CNA.NET-on-macOS statements or meta/JSON-LD/title-attr lines that carry an Apple
claim without matching the regex. A line holding both a current and a stale claim is counted once, as STALE.
Counts per page therefore add up to (regex hit lines + extras).

Facts that recur in the replacements (so the lead can keep wording consistent across pages):
- Host: physical **Mac mini M4** (Apple M4, 16 GB), macOS 27.0.1, Xcode 27, Apple clang 21; `CNA_PLATFORM=SDL3` (SDL's Cocoa/UIKit video drivers). (R2 §1)
- Phase 4 full trees on the M4, console **locked** (on-screen presentation not observed), 0 failures, skips by name: METAL 11,015/11,015; SOFTWARE 11,084/11,084;
  OPENGL33 11,916/11,916 (compiled effects ON); SDL_GPU 10,962/10,962; WEBGPU 10,968/10,968; FNA3D 10,875/10,875; SDL_RENDERER 10,940/10,940. (R2 §2.1, AM4-208)
- METAL: `ctest -L Metal` 261/261 under validation layers (101 shared pixel fixtures, 146 oracles, 14 native), Release 261/261; native MRT, MSAA (2x/4x on M4),
  occlusion queries, instancing, multi-stream, float/packed/DXT, cube/volume, SpriteBatch-scoped MSL custom effects; compiled XNA effects opt-in
  `CNA_METAL_COMPILED_EFFECTS` (default OFF); verdict **SUPPORTED, not primary-production**. (R2 §2.4, AM4-159)
- iOS: METAL + SDL_RENDERER allowed; `cna_ios_pixel_probe` exact on frame 1 + 10 frames in 8 of 8 launches (iOS 27 Simulator, iPhone 17 profile, AM4-120);
  device build final-linked, **not run** (no device/signing). `CNA_ENABLE_NET=OFF` required. (R2 §3)
- Hosted CI: `macos-26` runners; **no green post-campaign hosted run recorded**; hosted Metal GPU = "Apple Paravirtual device" (no shader validation). (R2 §2.16)
- C API on macOS: Mach-O `libcna_c_api.dylib` (exactly 3,210 `_cna_*` exports) + static archive, 119/119 C API tests in SOFTWARE and SDL_RENDERER trees, installed-consumer test,
  **no CI job builds it on macOS**. C ABI **0.46.0** (experimental). (R3 §1-2)
- CNA.NET on macOS: osx-arm64 local evidence on the M4 (suites, package acceptance, template, 84 samples smoke-run on SOFTWARE and METAL); not a shipping claim
  (no CI leg, signing, notarization); repo renamed `cna-dotnet`. (R3 §3)

---

## 1. deep-dives/platforms/android-and-apple-platforms.html

### deep-dives/platforms/android-and-apple-platforms.html
Counts: STALE 14 · CURRENT 6 · OK-GENERIC 9  (29 regex hit lines)

Section note (L171-177, `#macos` and `#ios`): both sections describe the pre-campaign state (macOS 14 workflows that "cannot configure",
the historical 136/143 feature-branch run as the only Metal execution, readback refused / MSAA disabled, iOS = one-frame smoke). They need a
rewrite around the Mac mini M4 qualification (R2 §2.1, §2.4), the iOS Simulator probe (R2 §3) and the current workflows (R2 §2.16). Row-level
replacements below are written so that L172+L173 and L176+L177 can be pasted as-is. CNA-BUG-199 (stale sharp-runtime pins) is fixed at
c1c316b9 by AM4-234 (both Apple workflows now pick the sibling branch via `scripts/ci/sibling_branch.sh`), so its link should go from this page and
the known-issue page itself needs a resolved note (outside this worklist).

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 7 (meta description) | `...how assets and saves are found on a device, and what the macOS and iOS workflows check.` | Understated: the page's Apple evidence is now the Mac mini M4 qualification and the iOS Simulator probe, not just workflows (R2 §2.1, §3; AM4-208, AM4-120). | `How CNA's Android application and NDK code are structured, how Game handles mobile lifecycle events, how assets and saves are found on a device, and what the Mac mini M4 qualification, the iOS Simulator probe and the Apple workflows show.` |
| 13 (og:description) | same as L7 | same | same as L7 |
| 19 (JSON-LD) | `"description":"...and what the macOS and iOS workflows check."` (also `"dateModified":"2026-10-04"`) | same as L7 | `"description":"How CNA's Android application and NDK code are structured, how Game handles mobile lifecycle events, how assets and saves are found on a device, and what the Mac mini M4 qualification, the iOS Simulator probe and the Apple workflows show."` (bump `dateModified`) |
| 123 | `<a href="#macos">macOS: two declared routes</a>` | TOC follows the rewritten h2 (L171). | `<li><a href="#macos">macOS: the Mac mini M4 qualification and the workflows</a></li>` |
| 124 | `<a href="#ios">iOS: final link and one simulator frame</a>` | "one simulator frame" is stale: Simulator pixel probe 8/8 launches (R2 §3, AM4-120); R2 §6 row "iOS has only a one-frame smoke". | `<li><a href="#ios">iOS: a Simulator pixel probe and a device build that is not run</a></li>` |
| 131 (evidence callout) | `...the Apple CMake and workflows at b0e97bb1 ... Nothing was built, run on an emulator or device, or launched on macOS/iOS; the Android emulator results are CNA's own records...` | Must name the Apple records the page now relies on (plan_apple_m4.md, apple-platforms.md) and say they are CNA's records, like the Android ones. Snapshot SHA handled globally by lead. | `<p><strong>Evidence basis:</strong> source-verified at the pinned commit; tests exist (not executed for this page). Claims on this page were checked by reading the CNA source at commit <code>c1c316b9</code>; unless a sentence says otherwise, nothing here was built or executed. Checked by reading the Android demo project, the devices, platform, content, storage and runtime sources, the Apple CMake and workflows, and CNA's Apple records (<code>docs/apple-platforms.md</code>, <code>docs/metal-renderer.md</code>, <code>plans/plan_apple_m4.md</code>) at c1c316b9, and Sharp Runtime next @ 41b918c9. Nothing was built, run on an emulator or device, or launched on macOS/iOS for this page; the Android emulator results and the Mac mini M4 and iOS Simulator results are CNA's own records, not re-run here.</p>` |
| 133 | `...how content and saves are found on a device, what the Apple workflows are configured to check, and which historical results...` | Understated (R2 §2.1, §3). | `...how content and saves are found on a device, what CNA's own qualification on a physical Mac mini M4 and in the iOS Simulator measured, what the Apple workflows are configured to check, and which historical results are records of their own revision rather than evidence for this one.` (rest of the paragraph, incl. the four links, unchanged) |
| 136 | `<code>METAL</code> is macOS-only; and iOS allows only <code>SDL_RENDERER</code> unless <code>CNA_APPLE_ALLOW_UNVALIDATED_RENDERER=ON</code>` | METAL targets macOS **and iOS/iPadOS** since AM4-037; iOS allow-list = SDL_RENDERER + METAL (`cmake/ApplePlatform.cmake:247-248`; R2 §3, §6). | `...(Android's <code>CMAKE_SYSTEM_NAME</code> is <code>Android</code>, not <code>Linux</code>, so it does not inherit Linux's <code>OPENGLES3</code> default); <code>METAL</code> targets macOS and iOS/iPadOS (on iOS it draws into a <code>CAMetalLayer</code>-backed view in SDL's <code>UIWindow</code>) and CMake rejects it everywhere else; and iOS allows <code>SDL_RENDERER</code> and <code>METAL</code> unless <code>CNA_APPLE_ALLOW_UNVALIDATED_RENDERER=ON</code> is set for an experiment (<a class="src-link" href="…/cmake/ApplePlatform.cmake"><code>ApplePlatform.cmake</code></a>). The same file refuses any other Darwin target: ...` (tvOS/watchOS/visionOS sentence unchanged; still true, `ApplePlatform.cmake:44`) |
| 171 | `<h2 id="macos">macOS: two declared routes</h2>` | Section is now about measured runs (R2 §2.1). | `<h2 id="macos">macOS: the Mac mini M4 qualification and the workflows</h2>` |
| 172 | `...<code>AppKit</code>, <code>Metal</code>, <code>QuartzCore</code> and <code>Foundation</code> are linked ... That is a sound portability seam, but source isolation is not native validation. ... only <code>Metal_Smoke</code> and <code>Metal_Capabilities</code> require a <code>METAL</code> build` | View framework is AppKit on macOS, UIKit on iOS (`modules/renderers/metal/CMakeLists.txt:13-19`, AM4-037); "source isolation is not native validation" now reads as if no native validation exists (R2 §6); a METAL tree now registers many native Metal tests (`ctest -L Metal` 261, AM4-159), not two. The `Metal_PortableHelpers` caveat is still true (`modules/renderers/metal/examples/CMakeLists.txt:38`). | `<p><code>METAL</code> keeps its Objective-C++ out of every other configuration: the <code>.mm</code> sources join the renderer archive, and <code>Metal</code>, <code>QuartzCore</code>, <code>Foundation</code> and the view framework (<code>AppKit</code> on macOS, <code>UIKit</code> on iOS) are linked only when <code>METAL</code> is the configured renderer (<a class="src-link" href="…/modules/renderers/metal/CMakeLists.txt"><code>Metal CMake</code></a>). The <code>Metal</code> CTest prefix needs care: the Metal policy suites are host-portable and are registered as <code>Metal_PortableHelpers</code> in every test-enabled configuration, so <code>ctest -R '^Metal'</code> on a Linux <code>HEADLESS</code> tree passes without executing any Objective-C++, Apple framework, shader compiler or GPU command; the native tests (<code>Metal_Smoke</code>, <code>Metal_Capabilities</code> and the shared pixel fixtures and oracles under the <code>Metal</code> label) exist only in a <code>METAL</code> build (<a class="src-link" href="…/modules/renderers/metal/examples/CMakeLists.txt"><code>Metal examples CMake</code></a>). A quoted Metal result must therefore carry the renderer identity of the build that produced it.</p>` |
| 173 (whole paragraph) | `Two workflows are configured for macOS 14, and both pin a sharp-runtime revision ... neither can configure ... run 29814126178 ... macos-14 with Xcode 15.4 and passed 136 of 143 ... refuses backbuffer readback ... and disables MSAA` | Every claim superseded: workflows on `macos-26` (AM4-255) and branch-chosen sharp-runtime (AM4-234, fixes CNA-BUG-199); readback native (AM4-025), MSAA native (AM4-141); the 136/143 run is history whose causes were fixed (AM4-025, AM4-028); macOS is now measured on a physical M4 (R2 §2.1, §2.4, §2.16, §6). | Replace by two paragraphs: `<p>CNA's own qualification ran on a physical Mac mini M4 (Apple M4, 16 GB, macOS 27.0.1, Xcode 27, Apple clang 21) in October 2026, recorded task by task in <code>plans/plan_apple_m4.md</code> and summarised in <a class="src-link" href="…/docs/apple-platforms.md"><code>docs/apple-platforms.md</code></a>. At its close-out every renderer tree that applies to macOS ran its full test suite with no failing case: <code>METAL</code> 11,015/11,015, <code>SOFTWARE</code> 11,084/11,084, <code>OPENGL33</code> 11,916/11,916 with compiled effects on, <code>SDL_GPU</code> on SDL's Metal driver 10,962/10,962, <code>WEBGPU</code> on wgpu-native's Metal backend 10,968/10,968, <code>FNA3D</code> on its Metal driver 10,875/10,875 and <code>SDL_RENDERER</code> 10,940/10,940; the remaining cases skip by name (a capability is absent, another renderer is active, a facility is Linux-only). Those runs were made with the console session locked, so macOS reported every window occluded and on-screen presentation was not observed. For <code>METAL</code> the campaign replaced the earlier refusals with native paths (backbuffer readback, multiple render targets, MSAA, occlusion queries, instancing and multi-stream input, float, packed and DXT formats, cube and volume textures, SpriteBatch-scoped MSL custom effects), and <code>ctest -L Metal</code> passes 261/261 under the Metal validation layers in Debug and Release. CNA's verdict is supported, not primary-production: compiled XNA effects need <code>CNA_METAL_COMPILED_EFFECTS=ON</code> (off by default), custom effects are SpriteBatch-only, <code>PresentInterval.Two</code> presents as <code>One</code>, no soak run has bounded the caches and no Intel Mac was run (<a class="src-link" href="…/docs/metal-renderer.md"><code>docs/metal-renderer.md</code></a>). The earlier feature-branch run on <code>macos-14</code> that saw only clear colours is history for its revision; its two causes, disabled readback and a transposed world-view-projection matrix, were fixed in this campaign.</p><p>Two workflows run on GitHub's <code>macos-26</code> runners and check out the sharp-runtime branch CNA's own sibling script chooses. <a class="src-link" href="…/.github/workflows/metal-macos-ci.yml"><code>metal-macos-ci.yml</code></a> configures <code>METAL</code> and runs the Metal test prefix plus a renderer-definition control (its push path filter still names a few files that no longer exist, so it effectively triggers on pull requests and the paths that remain); the hosted GPU is an "Apple Paravirtual device" that cannot run Metal shader validation, so there the tests run with API validation only and one process at a time. <a class="src-link" href="…/.github/workflows/apple-ci.yml"><code>apple-ci.yml</code></a> builds <code>CnaTests</code> on <code>SDL_RENDERER</code> and runs the target-platform, game-window, mobile-lifecycle, storage and desktop-OS suites directly rather than through CTest; it then builds a self-contained <code>cna_macos_smoke.app</code>, lints its <code>Info.plist</code>, uses <code>otool -L</code> to reject any dependency that still points at the build machine (the SDL prebuilt root, Homebrew or <code>/usr/local</code>) in the executable or the embedded frameworks, and launches it until it prints <code>CNA_APPLE_SMOKE_OK</code>. No green hosted run of either workflow is recorded after the campaign's last CI change, so the numbers above are the Mac mini M4's, not CI's. The deployment floors (macOS 13.3, iOS 16.3) are on <a href="../../docs/platforms.html#macos">Platforms: macOS</a>; a binary linked against Homebrew's FFmpeg starts only on the macOS that FFmpeg was built for unless video is configured off.</p>` |
| 175 | `<h2 id="ios">iOS: final link and one simulator frame</h2>` | R2 §3, §6 (AM4-120). | `<h2 id="ios">iOS: a Simulator pixel probe and a device build that is not run</h2>` |
| 177 (whole paragraph) | `The <code>apple-ci.yml</code> iOS matrix builds for an arm64 device and an arm64 simulator ... requires the one-frame marker ... older pinned sharp-runtime revision ... stops at configure time (CNA-BUG-199)` | Matrix is 4 legs incl. METAL device/simulator, METAL simulator leg runs `cna_ios_pixel_probe` (R2 §2.16, §3); sharp-runtime pin fixed (AM4-234); Simulator pixel evidence exists (AM4-120); still no device. | `<p>The <code>apple-ci.yml</code> iOS matrix has four legs, <code>SDL_RENDERER</code> and <code>METAL</code> each for an arm64 device and an arm64 simulator, with tests, examples and networking off (<code>CNA_ENABLE_NET=OFF</code> is required, because the iOS SDK ships no libcurl). It checks the archive's <code>LC_BUILD_VERSION</code> platform, verifies that the final bundle exports <code>SDL_main</code> and carries no build-machine dynamic dependency, and for the simulator boots a device, ad-hoc signs, installs, launches with the console attached and requires the one-frame marker within a bounded interval; the <code>METAL</code> simulator leg also runs <a class="src-link" href="…/tests/apple/apple_pixel_probe.cpp"><code>cna_ios_pixel_probe</code></a>, which reads back a clear colour, a SpriteBatch quad and a BasicEffect triangle. No green hosted run of the matrix is recorded after the campaign. CNA's own iOS evidence comes from the Mac mini M4 (iOS 27 Simulator, iPhone 17 profile): the probe reads back exact pixels on the first frame and on the ten frames after it in 8 of 8 launches, and the smoke app passes. Reaching that needed an SDL fix that CNA carries as a patch for iOS builds: SDL's UIKit view-frame computation swapped a portrait window's bounds before UIKit rotated it to the landscape-only orientation set, so the game drew into a 1346x0 view. The device build is final-linked (Mach-O arm64, platform 2, minimum iOS 16.3, system frameworks only) and not run: no physical iPhone or iPad, signing identity or Apple account was available, so there are no device pixels, touch, audio, storage, background/resume or performance observations.</p>` |
| 180 | `...retained artifacts from the Apple and Metal workflows; and a result from a physical iOS device.` | Rung list must reflect the new boundary: on-screen presentation, soak, Intel Mac and a green hosted run are the open macOS rungs (R2 §7 items 1-3, 6, 7). | `<p>Each of these would move one route up exactly one rung, and should say which rung it proves: an archived Android graphics build with an emulator frame and its logs; an emulator test that drives the lifecycle transitions and checks state and graphics-resource reconstruction; content loaded through <code>ContentManager</code> inside an APK and inside an Apple bundle; a green hosted run of the Apple and Metal workflows with retained artifacts; on-screen presentation and <code>PresentInterval</code> pacing observed on an unlocked Mac, and a Metal soak run; a run on an Intel Mac; and a result from a physical iOS device. tvOS would need a designed host, not an inferred one. The platform-wide status table is on <a href="../../docs/platforms.html#os-status">Platforms: status by operating system</a>.</p>` |

CURRENT (keep): L137 iOS UIKit entry point via Entrypoint.hpp; L152 iOS background GPU-work termination; L158 macOS CI filter includes lifecycle test; L164 bundle content is the app's job (optionally "the Apple smoke and pixel-probe applications load no content"); L176 ios.cmake, static SDL, orientation adapter, smoke app; L188 ApplePlatform.cmake + apple-ci.yml reading item (optionally add `docs/apple-platforms.md`: "the Mac mini M4 qualification matrix").
OK-GENERIC: L6 title, L8 keywords, L11 og:url, L12 og:title, L16 canonical, L89 sidebar link, L109 breadcrumb, L114 h1, L194 related-pages links (Tutorial 109 / iOS and tvOS). (L18-19 JSON-LD counted as STALE above.)

---

## 2. docs/platforms.html

### docs/platforms.html
Counts: STALE 28 · CURRENT 6 · OK-GENERIC 13  (43 regex hit lines + 4 extras: L449, L454, L456, L502)

Section notes:
- **Platform matrix, macOS and iOS rows (L388-405)** and **status by OS, macOS and iOS rows (L444-457)**: rewrite from "configured, pinned sharp-runtime, not verified" to
  macOS = runs on real hardware (one physical Mac mini M4; full suites, console locked) + hosted workflows configured on `macos-26`, no green post-campaign run;
  iOS = Simulator runs with a METAL pixel probe + device build final-linked, not run. Row-level cells below.
- **Renderer availability (L498-507)** and **defaults (L519)**: METAL is gated to macOS **and iOS** and is on the iOS allow-list next to SDL_RENDERER (`cmake/RendererSelection.cmake:140-143`, `cmake/ApplePlatform.cmake:247-248`).
  The L507 counts assume the lead's renderer pass removes the retired identities from rows L498, L499, L501 (at c1c316b9 the OS gates are: DIRECTX9/DIRECTX11 → Windows, METAL → Darwin+iOS, WEBGL2 → Emscripten; `RendererSelection.cmake:122-161`).
- **CI caveat callout (L583)**: the whole "seven jobs pin a stale sharp-runtime" callout is obsolete — at c1c316b9 every workflow that checks out sharp-runtime goes through `scripts/ci/sibling_branch.sh` or `clone_siblings.sh` (AM4-234; checked: apple-ci, metal-macos-ci, emscripten-multi-renderer-ci, devices-tests, content-pipeline-windows-ci, d3d-windows-ci all reference them). All "(sharp-runtime pin caveat)" asides on this page (L360, L386, L392, L404, L447, L454, L593, L595) should go; L386/L593 are web/Linux and not in this worklist's count.
- L243, L290, L360 also carry policy-(b) content (WIN32/X11/WAYLAND platforms, "native platform", Win32 module under Wine); the replacements below for L243/L290 fix it. For L360 only the Apple sentence is given; the Win32-module/native-Wayland sentences in the same paragraph belong to the platform pass (at c1c316b9 `platform-ci.yml` has no MinGW/Wine job; only `c-api-compat-matrix.yml` and `d3d-windows-ci.yml` mention mingw/wine).

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 243 | `<code>WIN32</code> only on Windows targets; <code>TERMINAL</code> only off Windows; <code>X11</code>/<code>WAYLAND</code> only where their dev packages exist (and not on Windows, Emscripten, Android, iOS; Wayland also not on Apple)` | Policy (b): CNA_PLATFORM is `SDL3 \| HEADLESS \| TERMINAL` at c1c316b9 (`cmake/PlatformSelection.cmake:24-32`); the Apple mention only exists to qualify the retired direct platforms. | `<li><strong>Platform gates:</strong> <code>TERMINAL</code> only off Windows (it is built on termios); <code>SDL3</code> and <code>HEADLESS</code> on every target, with Windows, X11, Wayland, macOS, iOS, Android and the browser reached through SDL3's video drivers; <code>ALSA</code> only on Linux.</li>` |
| 290 | `<code>-DCNA_ENABLE_SDL=OFF</code> with a native platform, ... CI checks <code>ldd</code>, <code>readelf</code> ... Windows and macOS have no SDL-free audio` | Policy (b) ("native platform"); the macOS audio statement itself is still true. CI job `sdl-free` = HEADLESS + HEADLESS + ALSA and checks with `readelf` (`.github/workflows/platform-ci.yml:315-373`). | `<p><code>-DCNA_ENABLE_SDL=OFF</code> with the <code>HEADLESS</code> or <code>TERMINAL</code> platform, <code>NULL</code> or <code>ALSA</code> audio, and a non-SDL renderer produces a binary with no SDL in it &mdash; CI proves with <code>readelf</code> and the build tree that no SDL was found, built or linked. Windows and macOS have no SDL-free audio, so a silent <code>NULL</code> build is the SDL-free option there.</p>` |
| 360 | `macOS and iOS have build workflows that trigger automatically (subject to the pinned-sibling caveat under <a href="#ci">CI</a>).` | Pin caveat fixed (AM4-234); macOS has run on real hardware (R2 §2.1, AM4-208); iOS has Simulator pixel evidence (AM4-120). | `macOS has run on real hardware (every applicable renderer's full test suite on one physical Mac mini M4) and has build workflows that trigger automatically; iOS has run only in the Simulator, and its device build final-links but has not been run.` (rest of the paragraph: policy pass, see note) |
| 372 | `Every renderer that is not Windows-only (5), macOS-only (1) or Emscripten-only (5) &mdash; 13 of the 18 identities.` | METAL is Apple-only (macOS + iOS), not macOS-only (AM4-037); counts are pre-policy (a): 14 identities, gates DX9/DX11 → Windows, METAL → Darwin/iOS, WEBGL2 → Emscripten (`RendererSelection.cmake:122-161`). | `<td>Every renderer that is not Windows-only (2), Apple-only (1) or browser-only (1) &mdash; 10 of the 14 identities. Default: <code>OPENGLES3</code>.</td>` |
| 390 | `<td><code>METAL</code> (macOS-only), plus the portable renderers.</td>` | METAL also on iOS (AM4-037); portable renderers now each run in full on the M4 (R2 §2.1). | `<td><code>METAL</code> (native; macOS and iOS), plus the portable renderers; <code>SDL_RENDERER</code>, <code>SOFTWARE</code>, <code>OPENGL33</code>, <code>SDL_GPU</code>, <code>WEBGPU</code> and <code>FNA3D</code> were each run in full on a Mac mini M4. Default: <code>SDL_RENDERER</code>.</td>` |
| 391 | `Build workflows configured on macOS runners; not verified passing at this snapshot` | Stale per R2 §6 row 1: 7 full trees, 0 failures on a physical M4 (AM4-208). "Runs on real hardware" = "someone ran it on the actual platform" (L354). | `<td><span class="status-badge status-done">Runs on real hardware</span> (one physical Mac mini M4, Apple silicon; full test suites, console locked, so on-screen presentation was not observed)</td>` |
| 392 | `Workflows exist &mdash; Apple and Metal on macOS runners &mdash; but they pin an older sharp-runtime` | Pin fixed (AM4-234); runners are `macos-26` (AM4-255); no green post-campaign run recorded (R2 §2.16). | `<td>Yes &mdash; Apple and Metal workflows on <code>macos-26</code> runners (portable suites and an <code>.app</code> launch on <code>SDL_RENDERER</code>; the <code>^Metal</code> tests on a paravirtual GPU); no green run recorded after the Mac mini M4 campaign</td>` |
| 402 | `<code>SDL_RENDERER</code> is the only validated iOS renderer; tvOS has no validated path.` | iOS allow-list = SDL_RENDERER + METAL (`ApplePlatform.cmake:247-248`); R2 §6 "Only SDL_RENDERER is allowed on iOS" stale. | `<td><code>SDL_RENDERER</code> and the native <code>METAL</code> renderer are the two allow-listed iOS renderers; tvOS has no validated path.</td>` |
| 403 | `iOS device final-link and simulator one-frame smoke, as configured` | Simulator pixel probe 8/8 launches (AM4-120); "Runs under Wine or an emulator" is the matching level (L353). | `<td><span class="status-badge status-partial">Runs in the iOS Simulator (a <code>METAL</code> pixel probe); device build final-linked, not run</span></td>` |
| 404 | `Narrow iOS build/simulator workflows exist (same sharp-runtime pin caveat); no physical-device or pixel claim` | Matrix has 4 legs incl. METAL; METAL simulator leg runs the pixel probe; pin fixed (R2 §2.16, §3). "no ... pixel claim" now wrong for the Simulator (R2 §8). | `<td>A four-leg iOS workflow (<code>SDL_RENDERER</code> and <code>METAL</code>, device and simulator; the <code>METAL</code> simulator leg runs the pixel probe); no green run recorded after the campaign; no physical-device claim</td>` |
| 446 | `CMake also offers <code>HEADLESS</code> and <code>TERMINAL</code> and, when its libraries are found, native <code>X11</code>; none is exercised on macOS.` | Policy (b): no X11 platform at c1c316b9 (`PlatformSelection.cmake:24-32`). | `<td><code>SDL3</code> (default; the only one CI configures; SDL's Cocoa video driver, CNA has no Cocoa backend of its own). CMake also offers <code>HEADLESS</code> and <code>TERMINAL</code>; no workflow selects either on macOS.</td>` |
| 447 | `<span class="status-badge status-partial">CI workflow, configured</span> (macos-14) configure and build of <code>CnaTests</code> on <code>SDL_RENDERER</code> ... Pins an older sharp-runtime` | macos-14 → macos-26 (AM4-255); pin fixed (AM4-234); M4 full-suite evidence missing (AM4-208); hosted Metal GPU is paravirtual (AM4-279). | `<td><span class="status-badge status-partial">Local</span> every applicable renderer's full test suite on a physical Mac mini M4 with no failing case (<code>METAL</code>, <code>SOFTWARE</code>, <code>OPENGL33</code>, <code>SDL_GPU</code>, <code>WEBGPU</code>, <code>FNA3D</code>, <code>SDL_RENDERER</code>; 10,875&ndash;11,916 tests each, console locked). <span class="status-badge status-partial">CI workflow, configured</span> (<code>macos-26</code>) <code>CnaTests</code> on <code>SDL_RENDERER</code>, portable suites, a self-contained <code>.app</code> bundle launch; <code>METAL</code> build and <code>^Metal</code> tests on a paravirtual GPU; no green run recorded after the campaign. Deployment floor 13.3.</td>` |
| 448 | `The <code>METAL</code> contract is narrower than &ldquo;it builds&rdquo;` | Verdict now SUPPORTED, not primary-production (AM4-159). | `<td><code>METAL</code>: supported, not primary-production (compiled effects opt-in, custom effects SpriteBatch-only)</td>` |
| 449 (+extra) | `<td>Anything outside those lanes.</td>` (macOS "Not proven") | The open items are now specific (R2 §7 items 2, 3, 6; Vulkan/MoltenVK out of scope). | `<td>Intel Macs; on-screen presentation and <code>PresentInterval</code> pacing; a Metal soak run; Vulkan through MoltenVK (out of scope).</td>` |
| 454 (+extra) | `device final-link of a smoke app and a simulator install + one-frame launch; <code>SDL_RENDERER</code> only; deployment floor 16.3. Same sharp-runtime pin caveat.` | METAL allowed; Simulator pixel probe; pin fixed; NET off required (R2 §3; AM4-037, AM4-105, AM4-120, AM4-234). | `<td><span class="status-badge status-partial">Local</span> iOS 27 Simulator (iPhone 17 profile) on the Mac mini M4: <code>METAL</code> pixel probe exact in 8 of 8 launches, smoke app OK; device <code>.app</code> final-linked, not run. <span class="status-badge status-partial">CI workflow, configured</span> device final-link and simulator launch for <code>SDL_RENDERER</code> and <code>METAL</code>; no green run recorded after the campaign. Deployment floor 16.3; <code>CNA_ENABLE_NET=OFF</code> required.</td>` |
| 456 (+extra) | `<td>Physical device, pixels, input, audio, storage; tvOS.</td>` | "pixels" now exist in the Simulator; device-side items remain (R2 §7 item 1). | `<td>Physical device (pixels, touch, audio, storage, background/resume, performance); tvOS.</td>` |
| 500 | `<code>METAL</code> (1, macOS-only)</th>...<td>Refused (an experiment-only override exists)</td>` | METAL gated to Darwin **and iOS**, on the iOS allow-list (`RendererSelection.cmake:140-143`; `ApplePlatform.cmake:247-248`). | `<tr><th scope="row"><code>METAL</code> (1, Apple-only)</th><td>Refused</td><td>Refused</td><td>Gated to here</td><td>Gated to here; on the iOS allow-list</td><td>Refused</td><td>Refused</td></tr>` |
| 502 (+extra) | SDL_RENDERER row, iOS cell: `<td>The only allow-listed renderer</td>` | Allow-list has two entries (`ApplePlatform.cmake:247-248`). | `<td>Allow-listed (with <code>METAL</code>)</td>` |
| 507 | `That is 3 + 3 + 1 platform-gated identities and 11 that are not gated by operating system, for the 18 in total. The iOS allow-list can be overridden...` | Counts follow METAL row and policy (a) (14 identities); iOS allow-list content. | `<p>That is 2 + 1 + 1 platform-gated identities (<code>DIRECTX9</code> and <code>DIRECTX11</code> to Windows, <code>METAL</code> to macOS and iOS, <code>WEBGL2</code> to the browser) and 10 that are not gated by operating system, for the 14 in total. iOS adds its own allow-list (<code>SDL_RENDERER</code> and <code>METAL</code>), which <code>CNA_APPLE_ALLOW_UNVALIDATED_RENDERER=ON</code> can override for experiments only; that is not a support claim. <code>TERMINAL</code> further restricts the choice to <code>SOFTWARE</code>, <code>HEADLESS</code> and <code>STUB</code>. Which native window services a renderer needs is on <a href="native-platforms.html#renderers">Native Platforms</a>.</p>` |
| 519 | `<td><code>SDL_RENDERER</code> (the only allowed)</td>` | Two allowed (AM4-037). | `<tr><th scope="row">iOS</th><td><code>SDL3</code></td><td><code>SDL3</code></td><td><code>SDL_RENDERER</code> (<code>METAL</code> is the other allow-listed renderer)</td><td>Off</td></tr>` |
| 564 | `It is macOS-only, and a workflow is configured to <strong>build it on a real <code>macos-14</code> runner on every push and pull request</strong>.` | METAL not macOS-only (AM4-037); runner macos-26 (AM4-255); M4 qualification missing (AM4-208); no green post-campaign run (R2 §2.16). | `<p>macOS carries the <code>METAL</code> renderer, which drives Apple Metal directly and uses SDL3 only for the window, to which it adds its own <code>CAMetalLayer</code>-backed view. CNA's own qualification ran on a physical Mac mini M4 (Apple M4, 16 GB, macOS 27.0.1, Xcode 27): every renderer that applies to macOS &mdash; <code>METAL</code>, <code>SOFTWARE</code>, <code>OPENGL33</code>, <code>SDL_GPU</code> and <code>FNA3D</code> on their Metal drivers, <code>WEBGPU</code> on wgpu-native's Metal backend, and <code>SDL_RENDERER</code> &mdash; passed its full test suite with no failing case (10,875 to 11,916 tests per renderer, the rest skipping by name). Two workflows run on GitHub's <code>macos-26</code> runners: <code>metal-macos-ci.yml</code> builds <code>METAL</code> and runs the <code>^Metal</code> tests, and <code>apple-ci.yml</code> builds <code>CnaTests</code> on <code>SDL_RENDERER</code>, runs the portable suites, verifies and launches a self-contained <code>.app</code> bundle, and covers iOS. No green hosted run of either is recorded after the campaign, so the full-suite numbers are the Mac mini's, not CI's.</p>` |
| 565 | `Two caveats: <code>METAL</code> throws on custom <code>ShaderEffect</code> shaders, and the Metal job builds and runs the <code>^Metal</code> tests rather than the full suite. ... and native <code>X11</code> whenever libX11 ...` | Custom effects now SpriteBatch-scoped MSL (AM4-077); compiled effects opt-in (AM4-144); locked console / no Intel (R2 §7); FFmpeg floor (AM4-130); relay needs Homebrew curl (AM4-044); policy (b) X11. | `<p>Caveats: the Mac mini runs were made with the console session locked, so on-screen presentation and <code>PresentInterval</code> pacing were not observed, and no Intel Mac was run. <code>METAL</code> compiles XNA effects only with <code>CNA_METAL_COMPILED_EFFECTS=ON</code> (off by default) and accepts custom <code>ShaderEffect</code>s only as SpriteBatch-scoped MSL (a 3D draw with one throws). The hosted Metal job runs the <code>^Metal</code> tests, not the full suite, on a paravirtual GPU without shader validation. The macOS deployment floor is 13.3 (a lower <code>CNA_MACOS_DEPLOYMENT_TARGET</code> is a configure error, because CNA needs Apple's floating-point <code>std::to_chars</code>). FFmpeg is optional on macOS (<code>CNA_ENABLE_VIDEO=AUTO</code> uses it when found; CI installs it with Homebrew), so <a href="video-playback.html">video</a> is available there only in builds that found it; Homebrew's FFmpeg is built for the host's macOS, so a binary linked against it does not start on an older one whatever the deployment target says. Online play needs a libcurl with WebSocket support, such as Homebrew's: the SDK's libcurl has none, and the relay transport then refuses by name. <code>SDL3</code> is the default and the only platform implementation any CI job configures on macOS (through SDL's Cocoa video driver); CMake also offers <code>HEADLESS</code> and <code>TERMINAL</code> there, and no macOS lane selects them.</p>` |
| 576 | `...allows only <code>SDL_RENDERER</code> by default. The Apple workflow is configured to final-link a device application and launch a simulator smoke application for one frame. That establishes ... not ... pixel correctness.` | METAL allowed; Simulator pixel probe (AM4-037, AM4-120); NET off required (AM4-105); R2 §8 "iOS has no pixel evidence" is wrong. | `<p>iOS support is <strong>experimental</strong>. The snapshot ships an iOS toolchain file (<code>cmake/toolchains/ios.cmake</code>, with <code>CNA_IOS_SIMULATOR</code> for the simulator SDK) and allows <code>SDL_RENDERER</code> and the native <code>METAL</code> renderer; networking must be configured off (<code>CNA_ENABLE_NET=OFF</code>), because the iOS SDK ships no libcurl, and FFmpeg video is unavailable. On the Mac mini M4, in the iOS 27 Simulator with an iPhone 17 profile, a pixel probe on <code>METAL</code> read back exact pixels on its first frame and the ten after it in 8 of 8 launches, and the one-frame smoke app passes; the device build final-links and was not run. That establishes configuration, link, Simulator startup and Simulator pixels for <code>METAL</code> &mdash; not physical-device behavior, touch, audio, storage or performance. The deployment floor is iOS 16.3. <code>CNA_APPLE_ALLOW_UNVALIDATED_RENDERER=ON</code> merely permits experiments outside the allow-list; it is not a support claim. tvOS has no validated path.</p>` |
| 583 (callout) | `Seven jobs in six workflows check CNA out against a <code>sharp-runtime</code> revision that predates ... <code>apple-ci</code> (its macOS and iOS jobs) and <code>metal-macos-ci</code> pin <code>f23ded28</code> ... (including native X11 ...)` | All pins replaced by `sibling_branch.sh`/`clone_siblings.sh` (AM4-234; R2 §6 row "Five CI workflows pin stale sharp-runtime commits"); policy (b) "native X11". | `<p><strong>Configured is not the same as passing.</strong> Every workflow now checks its sibling repositories out through CNA's own scripts (<code>scripts/ci/clone_siblings.sh</code> or <code>scripts/ci/sibling_branch.sh</code>), which pick the sharp-runtime branch that matches the branch being built, so the stale sharp-runtime pins of the previous snapshot are gone. A workflow file is still not a result: no green hosted run of the Apple or Metal workflow is recorded after the Mac mini M4 campaign's last CI change, and the Windows Direct3D and content-pipeline lanes run only on manual dispatch. Treat a workflow as <em>configured to</em> do what is described here unless a run is cited.</p>` |
| 595 | `<td>macOS/Metal plus iOS device final-link and simulator smoke lanes (sharp-runtime pin caveat).</td>` | macos-26, METAL iOS legs + pixel probe, pin fixed (R2 §2.16). | `<tr><td><code>apple-ci.yml</code> and <code>metal-macos-ci.yml</code></td><td><span class="status-badge status-done">Push / PR</span></td><td>macOS (<code>macos-26</code>)</td><td>macOS <code>SDL_RENDERER</code> portable suites and <code>.app</code> launch; <code>METAL</code> build and <code>^Metal</code> tests on a paravirtual GPU; iOS device final-link and simulator smoke for <code>SDL_RENDERER</code> and <code>METAL</code>, plus the <code>METAL</code> Simulator pixel probe. No green run recorded after the Mac mini M4 campaign.</td></tr>` |
| 606 | `The iOS device lane final-links; the simulator lane launches one smoke frame.` | METAL simulator lane runs the pixel probe (apple-ci.yml:383-390). | `<li>The iOS device lanes final-link; the simulator lanes launch the smoke app, and the <code>METAL</code> simulator lane also runs the pixel probe. None establishes physical-device or full-game correctness.</li>` |
| 625 | `...and what the macOS and iOS workflows check.` (deep-dive description) | Mirrors the deep dive's new description (page 1 L7). | `...how assets and saves are found on a device, and what the Mac mini M4 qualification, the iOS Simulator probe and the Apple workflows show.</li>` |
| 647 | `CNA-VGAP-008: Android and iOS have no device evidence at this snapshot: no Android workflow, one iOS simulator frame, ... iOS evidence is a device final-link plus a one-frame simulator launch` | "one iOS simulator frame" stale (AM4-120). The VGAP-008 page itself needs the same update (outside this list). | `<li><a href="../known-issues/verification-gaps/cna-vgap-008.html">CNA-VGAP-008: Android and iOS have no device evidence at this snapshot: no Android workflow, iOS evidence from the Simulator only, and lifecycle and packaged-content loading untested on a device</a> &mdash; Android has no preset or workflow, iOS evidence is a device final-link plus Simulator runs (a <code>METAL</code> pixel probe exact in 8 of 8 launches), lifecycle is tested only with scripted host events, and no test loads packaged content on a device.</li>` |

CURRENT (keep): L217 SDL3 default on macOS/iOS, static on iOS (the "most complete backend" wording is for the platform pass); L335 managedEntrypoint on iOS; L453 iOS platform implementations; L518 macOS defaults; L617 FFmpeg decoding Linux+macOS only, never on iOS; L642 CNA-BUG-192 (metal-macos-ci push filter still names `cmake/BackendLibraries.cmake`, `cmake/Examples.cmake`, `cmake/Tests/MetalTests.cmake`, all missing at c1c316b9, and still omits `modules/renderers/metal/CMakeLists.txt` / `examples/CMakeLists.txt` → still valid).
OK-GENERIC: L147, L149 TOC; L175 TargetPlatform enum; L233 NULL audio on Windows/macOS; L389, L401, L445, L452 row labels; L495 table header; L563, L575 h2; L579 "Apple/Metal" in the workflow list (the "18 workflow files" count is not Apple); L626 "Apple routes" in a link description.

---

## 3. docs/tutorials/109-metal-macos.html

### docs/tutorials/109-metal-macos.html
Counts: STALE 53 · CURRENT 12 · OK-GENERIC 11  (54 regex hit lines + 22 extras: L98, L106, L129-130, L182, L186, L188, L189, L190, L191, L193, L194, L195, L196, L210, L236, L237, L238, L239, L240, L245, L258, L262)

Section note: the whole tutorial is written around the pre-campaign contract (METAL macOS-only, readback/MSAA/MRT/occlusion/custom effects/
multi-stream/instancing/formats refused, no Apple evidence). At c1c316b9 every one of those is native (R2 §2.4; `docs/metal-renderer.md:107-126`;
`modules/renderers/metal/include/CNA/Internal/Renderers/Metal/MetalPolicy.hpp:165-184`), so sections `#platform-gate`, `#ci`, `#capabilities`,
`#shader-effect`, `#deterministic`, `#why-narrow`, `#what-works` and the code comments in `#portable` need rewriting. Keep the ids. Capability facts
verified in source at c1c316b9:
- `MetalSupportsCapability` returns true for ThreeD, DepthStencilBuffer, MRT (AM4-097), Anisotropic, WireFrame, OcclusionQuery (AM4-038), CustomEffects (AM4-077),
  Texture3D, MultiStreamVertexInput, Instancing (AM4-143), StencilBuffer, AdditiveBlending; MSAA is answered per device (`MetalRenderer.mm:6464-6469`, true when the
  device supports any of 2/4/8 samples).
- The six newer members are derived in `GraphicsDevice::SupportsCapability` (`modules/graphics/src/Xna/GraphicsDevice.cpp:3453-3480`): CompiledEffects → `SupportsCompiledEffects()`,
  declared only `#if defined(CNA_METAL_COMPILED_EFFECTS)` (`MetalRenderer.hpp:700-716`, `MetalRenderer.mm:6372`); Float/HalfFloat RTs → render-target format
  classification (true: AM4-142); HalfFloatTextureLinearFiltering → true (`MetalRenderer.mm:5268-5271`); ComputeShaders, IndirectDraw → false (no override).
  Result: **16 of 19 true in a default build, 17 with `CNA_METAL_COMPILED_EFFECTS=ON`, ComputeShaders/IndirectDraw false** (MRT, Texture3D and float targets under HiDef).
- The renderer no longer uses `SDL_Metal_CreateView`/`SDL_Metal_GetLayer`: it creates its own layer-backed `CNAMetalView` and adds it to the native window's content view
  (`MetalRenderer.mm:4869-4876`); window flags `SDL_WINDOW_METAL`/`SDL_WINDOW_HIGH_PIXEL_DENSITY` still come from the SDL3 platform (`Sdl3Platform.cpp:433-439`). MRR (no ARC) still true.
- CMake message: `"CNA: METAL renderer targets macOS and iOS only."` (`cmake/RendererSelection.cmake:140-143`). `CNA_METAL_COMPILED_EFFECTS` fetches MojoShader + SPIRV-Cross (`RendererSelection.cmake:342-355`).
- Workflows naming each renderer at c1c316b9: METAL → apple-ci, metal-macos-ci; WEBGPU → emscripten-multi-renderer-ci; SDL_GPU, FNA3D, OPENGL33, DIRECTX9 → none.

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 7 (meta description) | `CNA's native Metal renderer: macOS-only by a hard CMake gate, SDL supplies only the window and CAMetalLayer, and its capability surface is deliberately narrow.` | METAL also on iOS (AM4-037); surface widened (AM4-025..159); SDL no longer supplies the layer (`MetalRenderer.mm:4869-4876`). | `CNA's native Metal renderer on macOS (and iOS): SDL supplies the window, the renderer adds its own CAMetalLayer view, and since the Mac mini M4 campaign it renders MRT, MSAA, instancing, readback and SpriteBatch-scoped MSL effects. What works, what is opt-in, and what is still unproven.` |
| 12 (og:description) | same as L7 | same | same as L7 |
| 96 | `...and why CMake refuses anywhere but macOS.` | R2 §6 "METAL is macOS-only" stale. | `<li>How to build CNA's native Metal renderer, and why CMake refuses it anywhere but macOS and iOS.</li>` |
| 98 (+extra) | `The renderer's current capability surface, which is narrower than you may expect, and why.` | Surface no longer narrow (R2 §2.4). | `<li>The renderer's current capability contract: what is native, what is opt-in, and what still refuses.</li>` |
| 99 | `What its automatic macOS CI job does, and what it does not yet prove.` | Evidence now comes from the M4, CI is a separate narrower matter (R2 §2.16). | `<li>What CNA's own runs on a physical Mac mini M4 prove, what the hosted macOS CI job does, and what neither proves yet.</li>` |
| 106 (+extra) | `It is also the renderer where CNA is most visibly conservative ... Several capabilities ... are reported <code>false</code> and refuse at runtime, because the evidence ... has not been re-established` | Evidence re-established and capabilities re-enabled (AM4-025, 038, 077, 097, 141..148). | `<p>It is also a renderer whose contract was rebuilt against evidence. Capabilities it once reported <code>false</code> &mdash; readback, MSAA, multiple render targets, instancing, custom effects &mdash; were re-enabled one at a time in CNA's Mac mini M4 campaign, each with native tests under Metal's validation layers. What remains is a short list of deliberate limits, which this tutorial states next to what works.</p>` |
| 108 | `<h2 id="platform-gate">macOS only, enforced by a hard error</h2>` | AM4-037. | `<h2 id="platform-gate">macOS and iOS only, enforced by a hard error</h2>` |
| 112 | `Configuring <code>METAL</code> anywhere other than macOS fails immediately:` | `RendererSelection.cmake:140-143`. | `<p>Configuring <code>METAL</code> anywhere other than macOS or iOS fails immediately:</p>` |
| 113 | `CNA: METAL renderer is currently supported only on macOS; iOS and tvOS remain unvalidated.` | Message changed (`RendererSelection.cmake:143`). | `<p><code>CNA: METAL renderer targets macOS and iOS only.</code></p>` |
| 118 | `In this snapshot the iOS path is experimental and limited to <code>SDL_RENDERER</code> ... any other renderer (<code>METAL</code> included) is a configure error on iOS ... CNA also sets no explicit macOS deployment target` | iOS allow-list = SDL_RENDERER + METAL (`ApplePlatform.cmake:247-248`); Simulator pixel probe 8/8 (AM4-120); device build-only; deployment floors 13.3/16.3 are explicit (`apple-platforms.md:65`, `:132`); LOD bias needs 26 (AM4-099). | `<p>The wording matters. <strong>On iOS the renderer is experimental</strong>: the iOS allow-list contains <code>SDL_RENDERER</code> and <code>METAL</code>, the Metal renderer draws into its own <code>CAMetalLayer</code>-backed UIKit view, and CNA's iOS evidence is the Simulator only &mdash; a pixel probe exact on its first frame and the ten after it in 8 of 8 launches (iOS 27 Simulator, iPhone 17 profile) &mdash; with a device build that final-links but has never run on a physical iPhone or iPad. tvOS remains unsupported. The macOS deployment floor is 13.3 (<code>CNA_MACOS_DEPLOYMENT_TARGET</code>) and the iOS floor 16.3; sampler LOD bias additionally needs macOS or iOS 26.</p>` |
| 129-130 (+extra) | `<td>The window itself, plus <code>SDL_Metal_CreateView()</code> and <code>SDL_Metal_GetLayer()</code> to obtain a <code>CAMetalLayer</code>.</td><td>Device and command-queue creation, ...</td>` | The renderer adds its own layer-backed view to the native window (`MetalRenderer.mm:4869-4876`; `metal-renderer.md:5-10`). | `<td>The window itself (<code>SDL_WINDOW_METAL</code>, high pixel density) and its native handle &mdash; <code>NSWindow*</code> on macOS, <code>UIWindow*</code> on iOS.</td><td>A <code>CAMetalLayer</code>-backed view of its own, added to that window; device and command-queue creation, every render pass and encoder, all resource allocation, the drawable, and presentation.</td>` |
| 136 | `<code>METAL</code> runs on the SDL3 platform, which is the only platform implementation CNA offers on macOS.` | HEADLESS/TERMINAL are also offered on macOS (`PlatformSelection.cmake:24-32`); SDL3 is the only *graphical* one, via Cocoa/UIKit drivers (R2 §1). | `...Other renderers' window flags are untouched by this. <code>METAL</code> runs on the <code>SDL3</code> platform, CNA's only graphical platform implementation on Apple systems (SDL's Cocoa video driver on macOS, its UIKit driver on iOS).</p>` (first two sentences unchanged) |
| 155 | `Nothing is fetched at configure time &mdash; Metal ships with the OS. ... and the CI job installs it.` | `CNA_METAL_COMPILED_EFFECTS=ON` fetches MojoShader + SPIRV-Cross (`RendererSelection.cmake:342-355`, AM4-144); Homebrew FFmpeg floor (AM4-130). | `<p>A default build fetches nothing at configure time &mdash; Metal ships with the OS. <code>-DCNA_METAL_COMPILED_EFFECTS=ON</code> adds compiled XNA effects (MojoShader's SPIR-V output translated to MSL by SPIRV-Cross), which are fetched dependencies and therefore off by default. Like every CNA build you still need the <code>sharp-runtime</code> sibling checkout beside <code>cna/</code> (its <code>next</code> branch). FFmpeg is optional (<code>CNA_ENABLE_VIDEO=AUTO</code> uses it when found; <code>brew install ffmpeg</code> enables video playback), and the CI job installs it; Homebrew's FFmpeg is built for the macOS it was installed on, so a binary linked against it does not start on an older macOS whatever the deployment target says.</p>` (optionally add `  -DCNA_METAL_COMPILED_EFFECTS=ON \` as a commented line to the L144-149 snippet) |
| 159 | `Several of CNA's 18 renderers have no continuous integration at all &mdash; no workflow names <code>WEBGPU</code>, <code>SDL_GPU</code>, <code>FNA3D</code>, <code>DIRECTX9</code> or <code>OPENGLES2</code> ... running on a <code>macos-14</code> runner.` | macos-14 → macos-26 (AM4-255); policy (a): retired identity named, 14 identities; WEBGPU is now named by emscripten-multi-renderer-ci (checked at c1c316b9). Path-filter sentence still true. | `<p>Several of CNA's 14 renderers have no continuous integration at all &mdash; no workflow names <code>SDL_GPU</code>, <code>FNA3D</code>, <code>OPENGL33</code> or <code>DIRECTX9</code>, and the native-Windows Direct3D lane is manual-dispatch only. <code>METAL</code> is one of the few with a dedicated, <strong>automatically triggered</strong> workflow &mdash; <code>metal-macos-ci.yml</code>, running on GitHub's <code>macos-26</code> runner. It fires on pull requests, on pushes to <code>next</code>, <code>develop</code> or <code>main</code> that touch the files its path filter lists, and on manual dispatch. That filter is kept by hand: at this snapshot it still names three files that no longer exist and omits the Metal module's own <code>CMakeLists.txt</code> files, so a push that changes only those does not trigger it.</p>` |
| 161 | `...builds with three parallel jobs, and runs the supported Metal contract tests (<code>ctest -R '^Metal'</code>) <strong>with Metal's shader validation and debug layer enabled</strong>.` | Hosted GPU is an "Apple Paravirtual device": shader validation off and `--parallel 1` there (AM4-279, AM4-283, AM4-306; `metal-macos-ci.yml` "Choose the Metal validation layers"); no green post-campaign run (R2 §2.16). | `<p>The job checks out CNA and the <code>sharp-runtime</code> sibling (the branch CNA's own sibling script chooses), asks Metal which GPU it has, configures with <code>-DCNA_GRAPHICS_RENDERER=METAL</code>, builds, and runs the Metal tests (<code>ctest -R '^Metal'</code>) with Metal's API validation layer. GitHub's hosted macOS runner exposes an &ldquo;Apple Paravirtual device&rdquo; rather than a real Apple GPU, and that device reports false texture-usage errors under Metal's shader validation, so there the job turns shader validation off and runs one test process at a time; on Apple hardware both validation layers stay on. A separate step re-runs the renderer compile-definition control so the build cannot drift into claiming to be a different renderer. No green run of this workflow is recorded after the campaign's last change to it.</p>` |
| 165 (callout) | `...CNA's own Metal page says the historical successful compile does not count as compile or runtime evidence for the <em>adapted</em> Objective-C++ source, and treats a fresh macOS run ... as an external validation boundary.` | Fresh native run exists (AM4-025..159); verdict SUPPORTED, not primary-production (AM4-159; `metal-renderer.md:71-74`). | `<p><strong>&ldquo;Supported&rdquo; now has evidence behind it, and a stated limit.</strong> CNA built and ran the adapted renderer on a physical Mac mini M4 (macOS 27, Xcode 27) under <code>MTL_DEBUG_LAYER</code> and <code>MTL_SHADER_VALIDATION</code>: <code>ctest -L Metal</code> passes 261/261 (101 shared pixel fixtures, 146 renderer-neutral oracles, 14 native tests) in Debug and in Release, and the full test suite in a <code>METAL</code> tree passes 11,015/11,015 with 114 named skips. CNA's verdict is <em>supported, not primary-production</em>: compiled effects are off in a default build, on-screen presentation and <code>PresentInterval</code> pacing were never observed (the console stayed locked, so every window was occluded), no physical iOS device ran it, and no soak run has bounded its caches.</p>` |
| 170 (callout) | `<strong>Real macOS hardware in CI is a genuine advantage here.</strong> The Metal renderer builds and runs on an Apple runner ... Wine/DXVK paths are manual` | Overstatement: the hosted GPU is a paravirtual device, not real Apple hardware (AM4-279); the real-hardware evidence is the local M4 (R2 §8 "CI verifies Metal pixels on every push"). Drops the Wine/DXVK aside. | `<p><strong>The hosted CI job is a regression guard, not the evidence.</strong> The numbers above come from CNA's own runs on Apple hardware; the hosted job compiles the renderer and runs its Metal tests on a paravirtual GPU that cannot run shader validation, and only when the relevant files change. Read a green hosted run as &ldquo;it still builds and its contract tests pass on that device&rdquo;, and the Mac mini M4 results as the pixel evidence &mdash; see <a href="../verification.html">Verification</a>.</p>` |
| 175 | `Metal's switch (<code>MetalSupportsCapability</code>) still has named answers for only the 13 members that preceded compiled effects; the six newer members ... reach the function's final <code>false</code>.` | The six newer members are derived by GraphicsDevice, and four of them are true on Metal (`GraphicsDevice.cpp:3453-3480`; AM4-142, AM4-144). | `<p><code>GraphicsCapability</code> has 19 members. Metal answers the original thirteen in its own switch (<code>MetalSupportsCapability</code>, with <code>MultiSampleAntiAliasing</code> decided per device); the six newer members are derived by <code>GraphicsDevice</code> from narrower renderer queries &mdash; compiled-effect support, the render-target formats the renderer really creates, half-float filtering, compute and indirect draws. There is <strong>no permissive true default</strong> here. This table is the renderer's contract in this snapshot:</p>` |
| 182 (+extra) | `<td>Native combined depth/stencil attachments.</td>` | AM4-151: per-format planes, Depth16 native, D3D9 DepthBias (`metal-renderer.md:114`). | `<tr><td><code>DepthStencilBuffer</code></td><td>true</td><td>A target has the planes its <code>DepthFormat</code> names, the backbuffer included; <code>Depth16</code> is stored natively; <code>DepthBias</code> follows Direct3D 9's normalized offset.</td></tr>` |
| 186 (+extra) | `<td>Colour-format native 3D textures.</td>` | AM4-147. | `<tr><td><code>Texture3D</code></td><td>true</td><td>Native volume textures in every uncompressed format (HiDef; DXT stays out of volumes, as in XNA).</td></tr>` |
| 188 (+extra) | `MultiSampleAntiAliasing` **false**, `Every requested sample count is clamped to zero.` | AM4-141. | `<tr><td><code>MultiSampleAntiAliasing</code></td><td>true where the GPU multisamples</td><td>Backbuffer, <code>RenderTarget2D</code>, <code>RenderTargetCube</code> and MRT; a request rounds down to a count the GPU accepts (2x and 4x on an M4, not 8x).</td></tr>` |
| 189 (+extra) | `MultipleRenderTargets` **false**, `More than one descriptor is rejected...` | AM4-097, AM4-146. | `<tr><td><code>MultipleRenderTargets</code></td><td>true</td><td>Up to eight <code>RenderTarget2D</code> or cube-face members (HiDef); stock effects write the first, compiled effects write the others too.</td></tr>` |
| 190 (+extra) | `OcclusionQuery` **false**, `Creation throws.` | AM4-038. | `<tr><td><code>OcclusionQuery</code></td><td>true</td><td>Counted natively; one query open at a time (a second <code>Begin</code> is refused).</td></tr>` |
| 191 (+extra) | `CustomEffects` **false**, `Effect creation and non-null <code>SpriteBatch</code> custom effects both throw.` | AM4-077. | `<tr><td><code>CustomEffects</code></td><td>true</td><td>SpriteBatch-scoped MSL; a 3D draw with a custom effect throws (see below).</td></tr>` |
| 192 | `CompiledEffects` **false**, `...Metal has no compiled Effect Framework runtime.` | AM4-144: opt-in runtime exists. | `<tr><td><code>CompiledEffects</code></td><td>true with <code>CNA_METAL_COMPILED_EFFECTS=ON</code>, else <strong>false</strong></td><td>XNA Effect Framework bytecode through MojoShader's SPIR-V profile and SPIRV-Cross to MSL, compiled by Metal at run time; off in a default build. Vertex textures and what the SPIR-V profile cannot express refuse by name.</td></tr>` |
| 193 (+extra) | `MultiStreamVertexInput` **false**, `More than one per-vertex stream is rejected.` | AM4-143. | `<tr><td><code>MultiStreamVertexInput</code></td><td>true</td><td>Up to sixteen vertex streams, each at its own buffer index and offset.</td></tr>` |
| 194 (+extra) | `Instancing` **false**, `Instance streams and instance counts other than one are rejected.` | AM4-143, AM4-154. | `<tr><td><code>Instancing</code></td><td>true</td><td><code>DrawInstancedPrimitives</code> with every stock effect, plus base-instance draws.</td></tr>` |
| 195 (+extra) | `FloatRenderTargets, HalfFloatRenderTargets, HalfFloatTextureLinearFiltering` **false**, `...render targets accept only <code>SurfaceFormat::Color</code>.` | AM4-142; derived answers true (`GraphicsDevice.cpp:3466-3473`, `MetalRenderer.mm:5216-5221`, `:5268-5271`). | `<tr><td><code>FloatRenderTargets</code>, <code>HalfFloatRenderTargets</code>, <code>HalfFloatTextureLinearFiltering</code></td><td>true</td><td>Derived from the formats the renderer really creates: float, half-float, wide and packed render-target and texture formats are native (HiDef); the packed 16-bit formats exist only on Apple-family GPUs.</td></tr>` |
| 196 (+extra) | `<td>Unnamed in the switch; the renderer has no compute or indirect-draw path.</td>` | Mechanism wording (derived, `GraphicsDevice.cpp:3474-3479`). | `<tr><td><code>ComputeShaders</code>, <code>IndirectDraw</code></td><td><strong>false</strong></td><td>Derived; the renderer has no compute or indirect-draw path.</td></tr>` |
| 201 | `Seven of the nineteen are <code>true</code> and <strong>twelve are <code>false</code></strong> ... <code>SurfaceFormat::Color</code> is the only surface format <code>METAL</code> accepts.` | 16/19 true in a default build (see note); formats AM4-142/147/148. | `<p>Sixteen of the nineteen are <code>true</code> in a default build (seventeen with <code>CNA_METAL_COMPILED_EFFECTS=ON</code>, and <code>MultiSampleAntiAliasing</code> only on a GPU that multisamples); <code>ComputeShaders</code> and <code>IndirectDraw</code> are <code>false</code>. As <a href="101-renderer-capabilities.html">Tutorial 101</a> explains, an authored or fail-closed <code>false</code> is the most trustworthy answer this API gives. Take these at face value and branch on them. Query a specific surface format rather than assuming one: the backbuffer is always BGRA8 (reported as <code>Color</code>), the packed 16-bit formats exist only on Apple-family GPUs (an Intel Mac GPU refuses them by name), and DXT is held as BC on every Mac and decoded to RGBA8 on GPUs without BC, such as an iPhone's.</p>` |
| 203 | `<h2 id="shader-effect">ShaderEffect throws on Metal</h2>` | AM4-077. | `<h2 id="shader-effect">ShaderEffect on Metal: SpriteBatch-scoped MSL</h2>` |
| 207 (callout) | `Constructing a <code>ShaderEffect</code> under <code>METAL</code> raises <code>System::NotSupportedException</code>: ... &ldquo;Metal custom effects are disabled until ...&rdquo;` | AM4-077; `docs/metal-shader-effect-contract.md` "Current status". | `<p><strong>On <code>METAL</code>, a <code>ShaderEffect</code> is a pair of Metal Shading Language sources for <code>SpriteBatch</code>.</strong> <code>ShaderEffect(device, vertexSource, fragmentSource)</code> compiles each source as its own runtime Metal library; a source that does not compile gives an effect whose <code>IsEffectValid()</code> is false and whose <code>GetCompileErrorEXT()</code> carries the Metal compiler's message &mdash; construction does not throw. <code>SpriteBatch.Begin(..., effect)</code> draws the batch through it; an ordinary 3D draw with a custom effect throws <code>System::NotSupportedException</code>, as on Direct3D 11 and Vulkan.</p>` |
| 210 (+extra) | `The refusal is complete and consistent rather than partial ... dormant MSL scaffolding ... must not be re-enabled by flipping a capability bit.` | The scaffolding is the enabled facility now (AM4-077). | `<p>The interface is fixed-slot, because MSL has no named loose uniforms: the sprite vertices and the clip-space mapping arrive in vertex buffers 0 and 1, <code>SetUniformMat4</code>, <code>SetUniformVec4</code> and <code>SetUniformFloat</code> fill buffers 2, 3 and 4 in both stages (the <code>name</code> argument is ignored), and the sprite's texture and sampler are slot 0. With several render targets bound only the first receives the effect's output. The full binding table is in CNA's <code>docs/metal-shader-effect-contract.md</code>.</p>` |
| 212 | `So on Metal you are on the stock-effect path. Guard the branch rather than catching the exception:` | AM4-077. | `<p>Write the effect in the dialect the device reports (<code>GetShaderDialectEXT()</code> is MSL on Metal), and keep a stock-effect path for 3D:</p>` |
| 226 (code) | `// Metal lands here: BasicEffect and friends, which are fully supported.` | Custom effects true on Metal now; 3D custom shaders need compiled effects (AM4-144). | `    // 3D on Metal: BasicEffect and friends, or a compiled XNA effect in a build with CNA_METAL_COMPILED_EFFECTS=ON.` (and above L224 add `    // On METAL, kVertexSrc/kFragmentSrc are MSL sources and the effect is for SpriteBatch.`) |
| 235 | `<strong>Back-buffer readback throws.</strong> ... on Metal you cannot. Use <code>SOFTWARE</code> for image-level assertions` | AM4-025 (`metal-renderer.md:130-133`). | `<li><strong>Back-buffer readback works in the game's backbuffer coordinates.</strong> <code>GetBackBufferData()</code> reads each requested pixel through the logical viewport (Retina scale and letterbox offset included) after the pending pass completes; it throws while a render target is bound, and a frame with no drawable reads zero. Image-level tests can run on <code>METAL</code> itself; <a href="107-cpu-renderers.html">Tutorial 107</a>'s <code>SOFTWARE</code> renderer stays the deterministic reference.</li>` |
| 236 (+extra) | `<strong>MSAA reports zero and allocates single-sample attachments</strong>` | AM4-141. | `<li><strong>MSAA is real where the GPU supports it</strong>: a request rounds down to a sample count the device accepts (2x or 4x on an M4), on the back buffer, render targets, cube faces and MRT, resolved at every encoder boundary. See <a href="65-msaa.html">Tutorial 65</a> for the portable pattern.</li>` |
| 237 (+extra) | `...<strong>or exactly one</strong> normalised 2D or cube-face descriptor. An MRT set throws.` | AM4-097. | `<li><strong>Render-target binding accepts zero descriptors</strong> (restore the back buffer), <strong>one</strong> normalised 2D or cube-face descriptor, or an MRT set of up to eight. Array slices are rejected. See <a href="62-mrt.html">Tutorial 62</a>.</li>` |
| 238 (+extra) | `multi-stream input and instancing throw <code>System::NotSupportedException</code>.` | AM4-143. | `<li><strong>Malformed stream metadata throws <code>std::invalid_argument</code></strong>; multi-stream input (up to sixteen streams) and instancing are native, and a per-instance stream, or one of several per-vertex streams, needs a <code>VertexDeclaration</code>.</li>` |
| 239 (+extra) | `<code>TextureCube</code>, <code>Texture3D</code> and render targets accept only <code>SurfaceFormat::Color</code>` | AM4-142, AM4-147, AM4-148. | `<li><strong>Surface formats are native, not coerced</strong>: float, half-float, wide and packed formats for textures and render targets, DXT1/3/5 for <code>Texture2D</code> and <code>TextureCube</code>, and every uncompressed format for cube and volume textures; a format a target cannot store throws by name rather than silently becoming <code>Color</code>.</li>` |
| 240 (+extra) | `Non-default per-target colour-write masks, multisample coverage masks, sampler maximum mip level and sampler LOD bias all throw` | AM4-079/146, AM4-141, AM4-034, AM4-099/296. | `<li><strong>Colour-write masks (target 0, and targets 1 to 3 under compiled effects), multisample masks, sampler maximum mip level and LOD bias are applied</strong>, with stated limits: LOD bias needs macOS or iOS 26 (SDK and OS) and is refused on a device measured to ignore it; a partial multisample mask is refused for a SpriteBatch custom effect; <code>PresentInterval.Two</code> presents as <code>One</code>.</li>` |
| 245 (+extra) | `<h2 id="why-narrow">Why the surface is this narrow</h2>` | Section now tells how it was widened. | `<h2 id="why-narrow">How the surface was widened</h2>` |
| 249 | `An earlier macOS CI run did build the historical Metal renderer successfully ... did not prove the rendering paths those booleans advertised.` | Keep as history but add the root causes found on the M4 (AM4-025, AM4-028; `metal-renderer.md:50-59`). | `<p>An earlier hosted CI run built the historical Metal renderer on <code>macos-14</code> with Metal validation enabled and exercised its test set. Seven checks could not demonstrate their result: six read back only the frame's clear colour after real draws &mdash; among them the two PBR golden tests and the custom-effect, MRT, MSAA and user-primitives tests &mdash; and a seventh applied a sample count of four but produced an edge that was still binary. CNA's later run on a physical Mac mini M4 found the two causes: readback itself had been disabled, and every 3D vertex was clipped by a transposed world-view-projection matrix. Both were fixed first.</p>` |
| 251 | `...Those are fixed in the source. What does not yet exist is a fresh macOS run proving the <em>adapted</em> renderer's pixels.` | Fresh run exists (R2 §2.4; AM4-159). | `<p>The renderer had been adapted to CNA's current graphics interfaces in between, and a source audit during that adaptation found and fixed a substantial list of real defects: a cached drawable held without an owned reference, a partially constructed renderer with no rollback, a doubly retained device, draws that selected pipelines by vertex stride alone, unchecked cube and volume transfers, viewport and scissor state lost when an encoder was recreated, render-target uploads that silently did nothing, and swapped channels on BGRA targets. On the Mac mini M4 each capability that had been switched off was then re-enabled only together with native tests run under Metal's validation layers: readback, occlusion queries, SpriteBatch custom effects, MRT, MSAA, every XNA surface format, instancing and multi-stream input, compiled effects, cube and volume textures and DXT.</p>` |
| 255 (callout) | `So the capabilities without that evidence were switched off rather than left advertised. ... Enabling <code>CustomEffects</code> again is defined as one coherent change ...` | Done (AM4-077 etc.); remaining limits R2 §2.4. | `<p><strong>A capability bit is a promise to callers.</strong> That is why the bits came back one at a time, each with its own evidence, rather than by flipping a switch. It is also why the remaining limits are stated rather than hidden: compiled effects need <code>CNA_METAL_COMPILED_EFFECTS=ON</code>, custom effects are SpriteBatch-only, the backbuffer is always BGRA8, a multisampled <code>RenderTarget2D</code> loses a <code>SetData</code> under <code>PreserveContents</code>, and no Intel Mac has run the renderer.</p>` |
| 258 (+extra) | `Read the <code>false</code>s on this page as &ldquo;not yet demonstrated on the current source&rdquo;` | Only two falses remain; reframe. | `<p>Read the remaining <code>false</code>s and refusals as &ldquo;not provided&rdquo; or &ldquo;not yet demonstrated&rdquo;, not as &ldquo;impossible&rdquo;. The distinction is exactly the one <a href="../verification.html">CNA's verification page</a> makes throughout.</p>` |
| 262 (+extra) | `Ordinary 3D draws consume the current vertex-stream metadata with one valid per-vertex stream; pipeline selection uses the effect's own flags and canonical stride rather than guessing from stride alone;` | Declaration-driven vertex input, multi-stream (AM4-035, AM4-143). | `<p>Inside that contract the renderer is a real one. Ordinary 3D draws build their Metal vertex descriptor from the bound vertex declaration, so meaning rather than stride decides how bytes are read; pipeline selection uses the effect's own flags; fog uses the FNA-compatible four-component fog-vector contract.` (rest of the paragraph from "Requested viewport and scissor state ..." unchanged) |
| 266 | `<strong>forward rendering with the stock effects, one render target at a time, no MSAA, no instancing, and no pixel readback.</strong> ... A deferred renderer, a hardware-instanced crowd or a custom post-processing chain does not &mdash; not on Metal, today.` | All refuted (AM4-025, 097, 141, 143); MRT outputs beyond the first need compiled effects (`metal-renderer.md:116`, `metal-shader-effect-contract.md`). | `<p>Practically, that means: <strong>forward rendering with the stock effects, MSAA, instancing, float render targets and pixel readback all work</strong>. Multiple render targets work too, but only a compiled XNA effect writes more than the first, so a deferred renderer needs <code>CNA_METAL_COMPILED_EFFECTS=ON</code>. Custom <code>ShaderEffect</code> code is SpriteBatch-only MSL: a post-processing pass drawn through <code>SpriteBatch</code> fits, a custom 3D shader does not.</p>` |
| 270 | `(a macOS-only renderer cannot share a binary with Windows-only or Emscripten-only ones)` | METAL is Apple-only (AM4-037). | `...but renderer/platform gates still apply (an Apple-only renderer cannot share a binary with Windows-only or Emscripten-only ones) and the selected renderer latches before device creation. ...` (rest unchanged) |
| 286 (code) | `return plan;   // On METAL: all three false, and all three answers are authored.` | MRT/MSAA/Instancing true (AM4-097, 141, 143). | `    return plan;   // On METAL: all three true (MSAA only on a GPU that multisamples), and all three answers are authored.` |
| 289 | `...keep your image-level regression tests on a CPU renderer rather than on the platform renderer, so a Metal build failing to read back pixels never becomes a gap in your coverage.` | Readback works (AM4-025). | `...so a bug report from a Mac user tells you immediately which renderer produced it. And keep a CPU renderer in your image-level regression tests next to the platform renderer: <code>SOFTWARE</code> is deterministic across machines, while <code>METAL</code> readback tells you what the GPU actually drew.</p>` (first sentence incl. the alpha.1 parenthesis unchanged) |
| 294 | `<a href="107-cpu-renderers.html">Tutorial 107: CPU-Only Renderers</a> &mdash; where to run the pixel tests Metal cannot` | AM4-025. | `<li><a href="107-cpu-renderers.html">Tutorial 107: CPU-Only Renderers</a> &mdash; the deterministic reference for image-level tests</li>` |
| 305 | `...and what the macOS and iOS workflows check.` (deep-dive description) | Mirrors page 1 L7. | `...how assets and saves are found on a device, and what the Mac mini M4 qualification, the iOS Simulator probe and the Apple workflows show.</li>` |

CURRENT (keep): L104 direct MTLDevice/queue/encoder/layer renderer; L138 MSL embedded, `newLibraryWithSource:`; L140 manual retain/release (optionally add "and per-frame autorelease pools", AM4-102); L144, L145, L149, L151, L153 build/test snippet (`MTL_SHADER_VALIDATION=1 MTL_DEBUG_LAYER=1 ctest -R '^Metal'` still the documented local command); L181 ThreeD "Built-in fixed-layout Metal pipelines only" (same wording as `metal-renderer.md:113`; optionally add "plus compiled effects when enabled"); L185 WireFrame row; L243 nil-drawable skip (METAL-277, still in `metal-renderer.md:101`); L264 transfer validation, 256-byte staging rows.
OK-GENERIC: L6 title; L10 og:url; L11 og:title; L15 canonical; L21 JSON-LD headline; L22 JSON-LD url (no JSON-LD description on this page; bump `dateModified` L24); L89 h1; L101 "macOS chapter"; L120 h2; L126 table header; L268 h2.

---

## 4. docs/rendering-backends.html

### docs/rendering-backends.html
Counts: STALE 23 · CURRENT 11 · OK-GENERIC 3  (33 regex hit lines + 4 extras: insert after L520, L625, L626, L628)

Section notes:
- METAL appears in eight tables/paragraphs that all encode the pre-campaign contract (partition "macOS only", "conservative", Color-only formats, no custom/compiled
  effects, capability rows mostly F). Source facts at c1c316b9 are the same as in §3's note (capability switch `MetalPolicy.hpp:165-184`, derived members
  `GraphicsDevice.cpp:3453-3480`, formats `MetalPolicy.hpp:427-444` = all 20 classic formats, packed16 only with `MTLGPUFamilyApple1`, 7 extension formats defer).
- Capability matrix (L561, L589): new METAL rows are 3D T, DS T, AA **c** (device: `supportedSampleCountMask != 0`), RT T, An T, Wf T, Oq T, Cx T, T3 T, MS T, In T, St T, Ad T;
  CE **c** (build option), F32 T, F16 T, HF T, Cs F, Id F. Optionally add to "Reading the conditions" (L594, not a hit): "<code>METAL</code>: AA is true when the
  device accepts a 2x, 4x or 8x sample count (every Metal GPU does 4x); CE is the <code>CNA_METAL_COMPILED_EFFECTS</code> build."
- Partition table (L229-232): only the METAL row is in this worklist; after the renderer pass the "Everything else" count becomes 10 (14 − DIRECTX9/DIRECTX11 − METAL − WEBGL2).
- L699 also lists a multi-renderer set `OPENGL33;VULKAN;SOFTWARE;HEADLESS` that came from the SDL-free X11 job (b0e97bb1 `platform-ci.yml:573-580`); no workflow names OPENGL33 at c1c316b9, so the replacement drops it.
  Similarly L701 (not a hit) "WEBGPU ... Named by no workflow" is now wrong for WEBGPU (named by `emscripten-multi-renderer-ci.yml`), and SDL_GPU, FNA3D, OPENGL33, DIRECTX9 are the unnamed ones — renderer pass.
- Several flagged lines also contain retired identities (L337, L501, L624, L626, L628, L640, L661, L699, L736); the replacements remove them (policy (a)).

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 221 | `Windows-only, Emscripten-only and macOS-only identities cannot cross platform partitions` | METAL is Apple-only (AM4-037; `RendererSelection.cmake:140-143`). | `<li>Windows-only, Emscripten-only and Apple-only identities cannot cross platform partitions: one toolchain cannot target both.</li>` |
| 231 | `<tr><td>macOS only (1)</td><td><code>METAL</code></td><td>Refused on other systems and on iOS/tvOS</td></tr>` | METAL accepted on iOS and on the iOS allow-list (R2 §3; `ApplePlatform.cmake:247-248`). | `<tr><td>Apple only (1)</td><td><code>METAL</code></td><td>Refused on every system other than macOS and iOS (tvOS, watchOS and visionOS are refused by the Apple platform gate)</td></tr>` |
| 287 | `<td><code>METAL</code></td><td>42</td><td>Metal</td><td>2D + 3D (conservative)</td><td>Supported</td><td>macOS only</td>` | "conservative" and "macOS only" stale (R2 §2.4, §6). | `<tr><td><code>METAL</code></td><td>42</td><td>Metal</td><td>2D + 3D</td><td>Supported</td><td>macOS and iOS</td></tr>` |
| 332 | `2D + 3D but the most conservative 3D renderer: <strong>no</strong> MSAA, MRT, occlusion, instancing, multi-stream, custom effects, compute or float targets; only <code>SurfaceFormat::Color</code> ... <strong>macOS only</strong>; iOS and tvOS refused ... AppKit, Metal, QuartzCore and Foundation frameworks` | R2 §2.4 feature table (AM4-025..148); iOS (AM4-037); renderer adds its own view (`MetalRenderer.mm:4869-4876`); UIKit on iOS (`modules/renderers/metal/CMakeLists.txt:13-19`). | `<tr><td><code>METAL</code></td><td>Apple Metal directly; SDL3 supplies the window, the renderer adds its own <code>CAMetalLayer</code>-backed view; declared <em>Supported</em></td><td>2D + 3D; MSAA (device-probed), MRT, occlusion queries, instancing, multi-stream, float and half-float targets, DXT, SpriteBatch-scoped MSL custom effects; compiled XNA effects with <code>CNA_METAL_COMPILED_EFFECTS=ON</code> (off by default); <strong>no</strong> compute or indirect draw</td><td>macOS and iOS (iOS: Simulator evidence only); every other system refused</td><td>Objective-C++; Metal, QuartzCore, Foundation, and AppKit (macOS) or UIKit (iOS); SDL3; MojoShader and SPIRV-Cross for compiled effects</td></tr>` |
| 337 | `The "modern graphics" work landed on <code>VULKAN</code>, <code>SDL_GPU</code>, <code>WEBGPU</code> and the Direct3D 11 and 12 renderers: float and half-float render targets, ...` | METAL now has float/half-float targets (AM4-142); policy (a) (Direct3D 12). | `<p>The "modern graphics" work landed on <code>VULKAN</code>, <code>SDL_GPU</code>, <code>WEBGPU</code> and the Direct3D 11 renderer: float and half-float render targets, shadow and image-based-lighting sampling, and renderer-internal compute, indirect-draw and GPU-timer support that the capability queries report (see <a href="#modern-features">Modern features by renderer</a>). <code>METAL</code> gained float and half-float render targets in CNA's Mac mini M4 campaign but has no compute or indirect-draw path. <code>VULKAN</code> is covered by <a href="tutorials/85-vulkan-backend.html">Tutorial 85</a>, <code>SDL_GPU</code> by <a href="tutorials/131-sdl-gpu.html">Tutorial 131</a>, <code>WEBGPU</code> by <a href="tutorials/132-webgpu.html">Tutorial 132</a> and <code>METAL</code> by <a href="tutorials/109-metal-macos.html">Tutorial 109</a>.</p>` |
| 338 | `<code>METAL</code> is declared <em>Supported</em>, but CNA's own Metal page says the adapted native <code>.mm</code> source has no fresh macOS compile-and-run result ... 136 of 143 ... disables the unproven backbuffer readback and MSAA ... iOS path is restricted to <code>SDL_RENDERER</code> and proves final linking plus a one-frame simulator launch` | R2 §6 rows 1-3, 5-7; AM4-025, 028, 037, 120, 141, 159; R2 §2.16. | `<p><code>METAL</code> is declared <em>Supported</em>, and since CNA's Mac mini M4 campaign that declaration has native evidence behind it: on a physical Mac mini M4 (macOS 27, Xcode 27) <code>ctest -L Metal</code> passes 261/261 under Metal's API and shader validation layers (101 shared pixel fixtures, 146 renderer-neutral oracles, 14 native tests), the same in a Release tree, and the full test suite of a <code>METAL</code> tree passes 11,015/11,015 with 114 named skips. The historical <code>macos-14</code> run that saw only the clear colour had two causes, disabled readback and a transposed world-view-projection matrix, both fixed. CNA's verdict is supported, not primary-production: compiled effects are off in a default build, on-screen presentation was never observed (the console was locked), no physical iOS device ran it and no soak run bounded its caches. The automatic lane, <code>metal-macos-ci.yml</code>, builds it and runs <code>ctest -R '^Metal'</code> on a hosted paravirtual GPU without shader validation; no green run of it is recorded after the campaign. On iOS, <code>SDL_RENDERER</code> and <code>METAL</code> are allowed; <code>METAL</code>'s iOS evidence is a Simulator pixel probe exact in 8 of 8 launches, and the device build final-links without being run. tvOS remains unsupported.</p>` |
| 349 | `...and the only renderer allowed on iOS; declared <em>Production</em>` | iOS allow-list has METAL too (`ApplePlatform.cmake:247-248`). | `<tr><td><code>SDL_RENDERER</code></td><td>SDL3's built-in accelerated 2D renderer &mdash; the default on Windows, macOS, iOS, Android and other non-Linux hosts, and one of the two renderers allowed on iOS; declared <em>Production</em></td>` (rest of row unchanged) |
| 458 | `<strong>Terminal</strong> accepts only the four CPU/no-pixel renderers. <strong>iOS</strong> allows only <code>SDL_RENDERER</code>` | iOS: SDL_RENDERER + METAL; TERMINAL list is three (`RendererSelection.cmake:109`). | `<li><strong>Terminal</strong> accepts only the three CPU/no-pixel renderers (<code>SOFTWARE</code>, <code>HEADLESS</code>, <code>STUB</code>). <strong>iOS</strong> allows <code>SDL_RENDERER</code> and <code>METAL</code>; anything else is a <code>FATAL_ERROR</code> unless the unsupported override <code>-DCNA_APPLE_ALLOW_UNVALIDATED_RENDERER=ON</code> is given.</li>` |
| 478 | `<tr><td>AppKit, Metal, QuartzCore, Foundation</td><td><code>METAL</code> (Objective-C++)</td><td>macOS SDK</td></tr>` | View framework is UIKit on iOS (`modules/renderers/metal/CMakeLists.txt:13-19`). | `<tr><td>Metal, QuartzCore, Foundation, and AppKit (macOS) or UIKit (iOS)</td><td><code>METAL</code> (Objective-C++)</td><td>macOS or iOS SDK</td></tr>` |
| 501 | `<tr><td><code>SOFTWARE</code>, <code>METAL</code>, <code>FNA3D</code>, <code>STUB</code>, and both 2D-only renderers</td><td>No (<code>CustomEffects</code> false)</td>` | METAL CustomEffects true, SpriteBatch-scoped MSL (AM4-077; `metal-shader-effect-contract.md`); policy (a): only one 2D-only renderer remains. | Two rows: `<tr><td><code>METAL</code></td><td>Yes, for <code>SpriteBatch</code> only (a 3D draw with a custom effect throws)</td><td>MSL source, compiled at run time</td><td>Not declared (the query is about the GLSL CNAEXT writes)</td></tr><tr><td><code>SOFTWARE</code>, <code>FNA3D</code>, <code>STUB</code> and the 2D-only <code>SDL_RENDERER</code></td><td>No (<code>CustomEffects</code> false)</td><td>&mdash;</td><td>&mdash;</td></tr>` |
| after 520 (+extra) | compiled-effects gate table has no Metal row | `CNA_METAL_COMPILED_EFFECTS` (AM4-144; `RendererSelection.cmake:342-355`). | insert `<tr><td>Metal (<code>METAL</code>)</td><td><code>-DCNA_METAL_COMPILED_EFFECTS=ON</code>; MojoShader's SPIR-V output translated to MSL by SPIRV-Cross</td></tr>` (L521's Direct3D row and L508's "17 of the 18" are renderer-pass items; the opt-in family count stays eight: EasyGL, Vulkan, WebGPU, SDL_GPU, Software, Direct3D 9, Direct3D 11, Metal — eight `option(CNA_*_COMPILED_EFFECTS` at c1c316b9) |
| 525 | `There is no compiled-effect implementation on <code>METAL</code>, <code>HEADLESS</code>, <code>STUB</code>, <code>SDL_RENDERER</code> or <code>CANVAS</code>.` | AM4-144; policy (a) (CANVAS). | `<p>There is no compiled-effect implementation on <code>HEADLESS</code>, <code>STUB</code> or <code>SDL_RENDERER</code>. Each opt-in family has its own compiled-effect test file; FNA-executed reflection, state and pixel fixtures (<code>tests/fixtures/compiled-effects/</code>) are replayed by several of them with a &plusmn;3 channel tolerance on 8&times;8 flat-input pixels &mdash; compiled effects only, not sprites or 3D scenes. <code>METAL</code>'s opt-in path was measured on a Mac mini M4: 43 Metal tests and 1,237 effect and SpriteBatch tests in a tree built with the option.</p>` |
| 561 | `<code>METAL</code></th><td>T</td><td>T</td><td>F</td><td>F</td><td>T</td><td>T</td><td>F</td><td>F</td><td>T</td><td>F</td><td>F</td><td>T</td><td>T</td>` | AM4-038, 077, 097, 141, 143; `MetalPolicy.hpp:165-184`, `MetalRenderer.mm:6464-6469`. | `<tr><th scope="row"><code>METAL</code></th><td>T</td><td>T</td><td>c</td><td>T</td><td>T</td><td>T</td><td>T</td><td>T</td><td>T</td><td>T</td><td>T</td><td>T</td><td>T</td></tr>` |
| 589 | `<code>METAL</code></th><td>F</td><td>F</td><td>F</td><td>F</td><td>F</td><td>F</td>` | CE opt-in (AM4-144), F32/F16/HF true (AM4-142; `GraphicsDevice.cpp:3466-3473`, `MetalRenderer.mm:5268-5271`). | `<tr><th scope="row"><code>METAL</code></th><td>c</td><td>T</td><td>T</td><td>T</td><td>F</td><td>F</td></tr>` |
| 624 | `...<code>DIRECTX9/11/12</code> (native HLSL); <code>METAL</code> carries shaders too, but see the caveat below` | Metal PBR now has native tests (`modules/renderers/metal/examples/CMakeLists.txt:112-128`: `Metal_PbrVertexColour`, `Metal_PbrDualUvSpecular`; PBR oracles `:401-402`); "both specular textures sampled" (AM4-085); policy (a). | `<tr><td>PBR / skinned-PBR drawing (<code>PbrEffect</code>, <code>SkinnedPbrEffect</code>)</td><td>GL family, <code>VULKAN</code>, <code>SDL_GPU</code>, <code>WEBGPU</code>, <code>DIRECTX9/11</code> (native HLSL), <code>METAL</code> (MSL)</td><td>Golden and hand-derived tests per family (<code>easygl_*pbreffect_golden</code>, <code>vulkan_pbreffect_*</code>, <code>sdlgpu_*pbreffect_test</code>, <code>webgpu_*pbr3d_test</code>; on <code>METAL</code> the shared PBR oracles plus <code>Metal_PbrVertexColour</code> and <code>Metal_PbrDualUvSpecular</code>, run on a Mac mini M4)</td></tr>` |
| 625 (+extra) | Skinned mesh drawing: `EasyGL, <code>VULKAN</code>, <code>SDL_GPU</code>, <code>WEBGPU</code>, <code>SOFTWARE</code>, <code>DIRECTX9</code>` | METAL omitted; skinned normal fixed and tested (AM4-145, `Metal_SkinnedEffect_WorldNormal`). | `<td>EasyGL, <code>VULKAN</code>, <code>SDL_GPU</code>, <code>WEBGPU</code>, <code>SOFTWARE</code>, <code>DIRECTX9</code>, <code>METAL</code></td>` (evidence cell: append "; <code>Metal_SkinnedEffect_WorldNormal</code>") |
| 626 (+extra) | Instancing: `EasyGL (non-ES2), <code>VULKAN</code>, <code>WEBGPU</code>, <code>SDL_GPU</code>, <code>DIRECTX9/11/12</code>, ... Base-instance: <code>VULKAN</code>, <code>SDL_GPU</code> (device level)` | METAL instancing + base instance (AM4-143, AM4-154; `MetalRenderer.hpp:281`); policy (a) (ES2 generation, DX12 retired). | `<td>Instancing: EasyGL, <code>VULKAN</code>, <code>WEBGPU</code>, <code>SDL_GPU</code>, <code>DIRECTX9/11</code>, <code>METAL</code>, <code>SOFTWARE</code>, <code>HEADLESS</code>; <code>FNA3D</code> conditional. Base-instance: <code>VULKAN</code>, <code>SDL_GPU</code>, <code>METAL</code> (device level)</td>` |
| 628 (+extra) | Float / half-float render targets: `<code>VULKAN</code>, <code>SDL_GPU</code>, <code>WEBGPU</code>, <code>DIRECTX11</code>, <code>DIRECTX12</code>, EasyGL (non-ES2), <code>SOFTWARE</code>` | METAL (AM4-142); policy (a). | `<td><code>VULKAN</code>, <code>SDL_GPU</code>, <code>WEBGPU</code>, <code>DIRECTX11</code>, <code>METAL</code>, EasyGL, <code>SOFTWARE</code></td>` |
| 640 | `<strong>Color-only (no classifier):</strong> <code>METAL</code>, <code>HEADLESS</code>, <code>STUB</code>, <code>SDL_RENDERER</code>, <code>CANVAS</code>;` | Metal has classifiers now (`MetalRenderer.mm:5216-5228`, `MetalPolicy.hpp:427-444`; AM4-142, 147, 148); policy (a) (CANVAS). | `<li><strong>Color-only (no classifier):</strong> <code>HEADLESS</code>, <code>STUB</code>, <code>SDL_RENDERER</code>; <code>DIRECTX9</code> and <code>FNA3D</code> as well, for textures and render targets alike (see the last bullet).</li><li><code>METAL</code>: the 20 classic formats &mdash; float, half-float, wide and packed (the packed 16-bit formats only on Apple-family GPUs; an Intel Mac GPU refuses them by name) and DXT1/3/5, held as BC on every Mac and decoded to RGBA8 on a GPU without BC; cube and volume textures in every uncompressed format; render targets in the float, half-float, wide and packed formats; the 7 extension formats defer, so they are refused. The backbuffer stays BGRA8, reported as <code>Color</code>.</li>` |
| 661 | `Categories: <em>Native</em> (<code>OPENGLES2/3</code>, ... <code>DIRECTX9/11/12</code>, <code>METAL</code>) ... the Windows and Metal lanes in particular are exercised mostly under Wine or a build-only lane.` | Metal lane no longer build-only: M4 full suites; hosted job runs `^Metal` tests (R2 §2.1, §2.16); policy (a) names; Windows Direct3D lanes are manual (`d3d-windows-ci.yml` `workflow_dispatch` only). | `<p>Categories: <em>Native</em> (<code>OPENGLES3</code>, <code>OPENGL33</code>, <code>VULKAN</code>, <code>DIRECTX9/11</code>, <code>METAL</code>), <em>TranslationLayer</em> (<code>SDL_RENDERER</code>, <code>WEBGPU</code>, <code>SDL_GPU</code>, <code>FNA3D</code>), <em>Software</em> (<code>SOFTWARE</code>), <em>Web</em> (<code>WEBGL2</code>) and <em>Diagnostic</em> (<code>HEADLESS</code>, <code>STUB</code>). Automatic fallback uses these two declarations to order the candidates (mature GPU renderers first, CPU renderers ten places later, <code>STUB</code> last). Read "Production" with the <a href="#verification">verification</a> section beside it: it is a declaration. The Windows Direct3D lanes in particular run only on manual dispatch, and <code>METAL</code>'s evidence is CNA's own runs on a Mac mini M4, with a hosted job that runs only its Metal tests.</p>` |
| 699 | `<code>SDL_RENDERER</code> on macOS/iOS; <code>METAL</code> build plus <code>ctest -R '^Metal'</code>, and multi-renderer builds (<code>HEADLESS;SOFTWARE;STUB</code>, <code>OPENGL33;VULKAN;SOFTWARE;HEADLESS</code>, and the Emscripten bundle <code>WEBGL2;WEBGL1;CANVAS</code>)` | iOS METAL legs + pixel probe (`apple-ci.yml:228-235`, `:383-390`); hosted Metal GPU paravirtual (AM4-279); policy (a): Emscripten bundle is `WEBGL2;WEBGPU` (`emscripten-multi-renderer-ci.yml:132`); the OPENGL33 set no longer exists (see note). | `<tr><td><code>OPENGLES3</code> (the full default suite under Xvfb); <code>VULKAN</code>, <code>SOFTWARE</code>, <code>HEADLESS</code> and <code>STUB</code> (glTF conformance and platform jobs); <code>SDL_RENDERER</code> on macOS and iOS; <code>METAL</code> on iOS (device final-link, Simulator launch and pixel probe) and on macOS (build plus <code>ctest -R '^Metal'</code> on a paravirtual GPU); multi-renderer builds (<code>HEADLESS;SOFTWARE;STUB</code>, and the Emscripten bundle <code>WEBGL2;WEBGPU</code>)</td><td><span class="status-badge status-done">Automatic on push and pull request</span></td></tr>` |
| 716 | `...it is the only renderer allowed on iOS, and its 3D entry points throw deterministically` | `ApplePlatform.cmake:247-248`. | `<p><strong>For 2D-only games wanting maximum portability:</strong> <code>SDL_RENDERER</code>. It needs nothing beyond the vendored SDL3, it is one of the two renderers allowed on iOS (with <code>METAL</code>), and its 3D entry points throw deterministically (or warn-and-stub, if you ask) instead of quietly drawing nothing.</p>` |
| 736 | `Custom <code>ShaderEffect</code> shaders are not accepted by <code>SOFTWARE</code>, <code>METAL</code>, <code>FNA3D</code> or either 2D-only renderer ... <code>METAL</code> is the most conservative 3D renderer and has no fresh macOS run evidence in CNA's own docs. <code>OPENGLES2</code> and <code>WEBGL1</code> drop ...` | AM4-077, AM4-144, AM4-159; policy (a) (two retired identities; one 2D-only renderer left). | `<p><strong>Know what you are opting into.</strong> Custom <code>ShaderEffect</code> shaders are not accepted by <code>SOFTWARE</code>, <code>FNA3D</code> or the 2D-only <code>SDL_RENDERER</code> (<code>FNA3D</code> supports the separate compiled Effect Framework path instead), and <code>METAL</code> accepts them only as SpriteBatch-scoped MSL. <code>METAL</code> runs compiled XNA effects only in a build with <code>CNA_METAL_COMPILED_EFFECTS=ON</code>, and its evidence is CNA's own runs on one Mac mini M4, with on-screen presentation not observed. CI does not exhaustively exercise every identity and driver combination.</p>` |

CURRENT (keep): L171 SDL_RENDERER default on macOS/iOS (same paragraph's identity counts/retired names are for the renderer pass); L182 Windows/macOS default to a 2D-only renderer (optionally make the example list per-OS: on macOS `METAL`, `OPENGL33`, `SDL_GPU`, `WEBGPU`, `FNA3D` — each run in full on the M4; VULKAN/MoltenVK is out of scope on Apple, R2 §2.8); L330 WEBGPU native on macOS through wgpu-native (optionally: "full suite run on a Mac mini M4 on its Metal backend"); L331 SDL_GPU shadercross default ON on Apple; L425 SDL_GPU custom ShaderEffect unavailable on Apple (matches AM4-175, `modules/renderers/sdl-gpu/CMakeLists.txt:53-63`); L475 SDL_shadercross default ON on Apple (optionally add "SPIRV-Cross also for <code>METAL</code> with <code>CNA_METAL_COMPILED_EFFECTS=ON</code>"); L530 METAL switch has no default arm (true: `MetalPolicy.hpp:167-183`; DIRECTX12 in the same sentence is a renderer-pass item); L629 compute false on METAL; L656 METAL declared Supported (row also lists retired identities — renderer pass); L712 macOS 3D game must choose a renderer; L776 CNA-BUG-094 (SDL_GPU still answers compute/SPIR-V true whenever a device exists, `SdlGpuRenderer.cpp:2865-2872`, `:3070-3078` → still valid).
OK-GENERIC: L321 "VULKAN, METAL drive explicit APIs directly"; L692 "CI exists across Linux, macOS and Emscripten jobs" (18 workflow files is still 18 at c1c316b9); L756 deep-dive link description.

---

## 5. docs/building.html

### docs/building.html
Counts: STALE 9 · CURRENT 24 · OK-GENERIC 7  (38 regex hit lines + 2 extras: L347, insert after L474)

Notes: the Apple presets are unchanged at c1c316b9 (`CMakePresets.json`: `macos` Release SDL_RENDERER tests+examples; `ios`/`ios-simulator` SDL_RENDERER with tests, examples and NET off; still 17 visible configure + 17 build presets), so L369-371 stay. `CNA_BUILD_APPLE_SMOKE_APP` now also builds the pixel probe (`cmake/AppleSmoke.cmake:25-35`). The hosted macOS runners install `ccache ffmpeg nlohmann-json` with Homebrew (`metal-macos-ci.yml`, AM4-247: gamer services need nlohmann-json, which the hosted image lacks) — worth a line in the prerequisites if the page lists macOS packages (it does not at HEAD; optional).

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 160 | `CI's workflows use GCC 14 on Linux, AppleClang on <code>macos-14</code>, ... (whether each lane currently passes is a separate question; see the caveat on <a href="platforms.html#ci">Platforms</a>)` | Runners are `macos-26` (Xcode 26) (AM4-255; workflow comments); the M4 toolchain is the measured one (R2 §1). | `<td>Not checked by CMake</td><td>CI's workflows use GCC 14 on Linux, AppleClang (Xcode 26) on <code>macos-26</code>, MSVC on <code>windows-latest</code>, mingw-w64 GCC, and Emscripten 6.0.3 (whether each lane currently passes is a separate question; see <a href="platforms.html#ci">Platforms</a>). CNA's own macOS qualification on a Mac mini M4 used Xcode 27 and Apple clang 21. The always-built content-pipeline module uses <code>&lt;format&gt;</code>, so a compiler older than roughly libstdc++ 13 / MSVC 2022 / a current libc++ cannot be assumed to work. Clang on Linux and clang-cl are not exercised by any build workflow.</td>` |
| 344 | `<code>METAL</code> is macOS-only, ... On iOS only <code>SDL_RENDERER</code> is allowed. ... lists all 18 identities` | METAL macOS + iOS (`RendererSelection.cmake:140-143`); iOS allow-list SDL_RENDERER + METAL (`ApplePlatform.cmake:247-248`); policy (a) in the same paragraph (DIRECTX12, WEBGL1, CANVAS, OPENGLES2, 18). | `<p>Several renderers are hard-gated and refuse to configure off their platform: <code>DIRECTX9</code> and <code>DIRECTX11</code> are Windows-only, <code>METAL</code> is limited to macOS and iOS, <code>WEBGL2</code> is Emscripten-only, and <code>OPENGLES3</code> / <code>OPENGL33</code> cannot be selected under Emscripten. On iOS only <code>SDL_RENDERER</code> and <code>METAL</code> are allowed. <a href="rendering-backends.html">Graphics Renderers</a> lists all 14 identities with their scope, platform gate and dependency.</p>` |
| 347 (+extra) | `...through eight options ...: <code>CNA_EASYGL_COMPILED_EFFECTS</code>, ..., <code>CNA_DIRECTX12_COMPILED_EFFECTS</code> and <code>CNA_SDL_GPU_COMPILED_EFFECTS</code>. ... With the options on, 13 of the 18 identities (in 9 families) support them. ... (unsupported on 17 of the 18 identities)` | `CNA_METAL_COMPILED_EFFECTS` added (AM4-144; eight `option(CNA_*_COMPILED_EFFECTS` at c1c316b9); policy (a) (DIRECTX12; 14 identities; EasyGL has three). | `<p>Compiled Effect Framework (<code>.fxb</code>) bytecode support is opt-in per renderer family, through eight options that all default to <code>OFF</code>: <code>CNA_EASYGL_COMPILED_EFFECTS</code>, <code>CNA_VULKAN_COMPILED_EFFECTS</code>, <code>CNA_WEBGPU_COMPILED_EFFECTS</code>, <code>CNA_SOFTWARE_COMPILED_EFFECTS</code>, <code>CNA_DIRECTX9_COMPILED_EFFECTS</code>, <code>CNA_DIRECTX11_COMPILED_EFFECTS</code>, <code>CNA_SDL_GPU_COMPILED_EFFECTS</code> and <code>CNA_METAL_COMPILED_EFFECTS</code>. <code>FNA3D</code> always supports compiled effects and has no option; <code>CNA_EASYGL_COMPILED_EFFECTS</code> enables all three GL identities at once. With the options on, 11 of the 14 identities (in 9 families) support them. Any of them (and <code>FNA3D</code>) fetches FNA3D with its MojoShader patch series at configure time; the Metal option also fetches SPIRV-Cross. A default configure reports compiled effects as supported on <code>FNA3D</code> only (unsupported on 13 of the 14 identities). See <a href="shader-effects.html">Shader Effects</a> and <a href="effects.html">Effects System</a>.</p>` |
| 434 (code) | `# iOS device / simulator (Apple floor 16.3; SDL_RENDERER only)` | METAL allowed on iOS (AM4-037). | `# iOS device / simulator (Apple floor 16.3; the presets use SDL_RENDERER, METAL is also allowed)` |
| 437 | `iOS is experimental: the Apple workflow is configured to final-link a device smoke app and to install and launch a simulator smoke app for one frame ... Other renderers need <code>-DCNA_APPLE_ALLOW_UNVALIDATED_RENDERER=ON</code>` | iOS METAL + pixel probe (AM4-037, AM4-120); NET off required (AM4-105); macOS M4 qualification missing (AM4-208). | `<p>On macOS every renderer that applies there (<code>METAL</code>, <code>OPENGL33</code>, <code>SDL_GPU</code>, <code>WEBGPU</code>, <code>FNA3D</code>, <code>SOFTWARE</code> and <code>SDL_RENDERER</code>) has passed its full test suite on a physical Mac mini M4; select one with <code>-DCNA_GRAPHICS_RENDERER=&lt;name&gt;</code>. iOS is experimental. The presets build <code>SDL_RENDERER</code>; add <code>-DCNA_GRAPHICS_RENDERER=METAL</code> for the native Metal renderer, and keep networking off (<code>CNA_ENABLE_NET=OFF</code>, as the presets do), because the iOS SDK ships no libcurl. The Apple workflow is configured to final-link device apps and to install and launch a simulator smoke app for both renderers, plus a pixel probe on <code>METAL</code> (<code>CNA_BUILD_APPLE_SMOKE_APP</code>, on by default for iOS); CNA's own Simulator run on the Mac mini M4 (iOS 27, iPhone 17 profile) read back exact pixels in 8 of 8 launches, and no physical device has run either renderer. Renderers outside <code>SDL_RENDERER</code> and <code>METAL</code> need <code>-DCNA_APPLE_ALLOW_UNVALIDATED_RENDERER=ON</code>, which is an experiment switch, not a support claim.</p>` |
| after 474 (+extra) | options table has no `CNA_METAL_COMPILED_EFFECTS` row | AM4-144; `RendererSelection.cmake:347-355`. | insert `<tr><td><code>CNA_METAL_COMPILED_EFFECTS</code></td><td><code>ON</code>, <code>OFF</code></td><td><code>OFF</code></td><td>The same for <code>METAL</code>: MojoShader's SPIR-V output translated to MSL by SPIRV-Cross (both fetched) and compiled by Metal at run time.</td></tr>` (L473's three-Direct3D row is a renderer-pass item) |
| 494 | `<td>Build the minimal Apple final-link/simulator smoke application.</td>` | The option also builds the pixel probe (`cmake/AppleSmoke.cmake:25-35`, AM4-037). | `<td>Build the minimal Apple smoke application (<code>cna_ios_smoke</code> / <code>cna_macos_smoke</code>) and the pixel probe (<code>cna_ios_pixel_probe</code> / <code>cna_macos_pixel_probe</code>), which reads back what one frame drew.</td>` |
| 495 | `iOS experiment escape hatch for identities outside the sole validated <code>SDL_RENDERER</code> allow-list` | Allow-list = SDL_RENDERER + METAL. | `<td>iOS experiment escape hatch for identities outside the allow-list (<code>SDL_RENDERER</code> and <code>METAL</code>); unsupported configurations are expected to fail.</td>` |
| 518 | `CI's workflows cover focused subsets across Linux, macOS and a headless browser (some of those lanes pin an older sharp-runtime; see <a href="platforms.html#ci">Platforms</a>).` | Pins gone (AM4-234; all workflows use `sibling_branch.sh`/`clone_siblings.sh` at c1c316b9). | `<p>CI's workflows cover focused subsets across Linux, macOS and a headless browser (a configured workflow is not a passing one; see <a href="platforms.html#ci">Platforms</a>).` (rest of the paragraph unchanged) |

CURRENT (keep): L148 FFmpeg on Linux/macOS; L161 macOS/iOS floors 13.3/16.3 (optionally append: "A binary linked against Homebrew's FFmpeg starts only on the macOS that FFmpeg was built for; build with <code>CNA_ENABLE_VIDEO=OFF</code> or an FFmpeg built for the floor to keep 13.3" — AM4-130); L170 FFmpeg optional on Linux/macOS; L175 no FFmpeg on iOS; L231 SDL prebuilt keys (`-simulator`, `-min<version>`), static on iOS; L257 house3d demo not built for Metal (`modules/graphics/examples/CMakeLists.txt:140-144`; same row lists retired GL identities — renderer pass); L270 static link on macOS (optionally note the C API's own `libcna_c_api.dylib`, R3 §2); L274 inspector refused on iOS; L369-371 Apple presets; L430 macOS floor comment; L452, L464 option rows (video/inspector on iOS); L475 shadercross ON on Apple; L487-493 Apple option rows (defaults verified: `CNA_APPLE_BUNDLE_VERSION` = PROJECT_VERSION 0.1.0); L588, L591 FFmpeg troubleshooting.
OK-GENERIC: L350 preset names; L429 h3 "macOS and iOS"; L431, L432, L435, L436 preset commands; L605 deep-dive "Apple routes" link text.

---

## 6. features.html

### features.html
Counts: STALE 20 · CURRENT 10 · OK-GENERIC 3  (28 regex hit lines + 5 extras: L110, L807, L808, L809, L810)

Section notes:
- METAL card (L710-716), renderer table row (L526), capability row (L561), compiled-effects gate (L583), platform-gate row (L602) and the "macOS / iOS" card (L772)
  all describe the pre-campaign renderer. New capability row (19 columns, same order as the header at L542): `Y Y c Y Y Y Y Y Y Y Y Y Y c Y Y Y – –` (see §3 note for sources).
- Not counted here (no Apple term, global passes): meta/og/JSON-LD description (L7, L12, L24) and the snapshot paragraph L80 still say "C ABI 0.44.0", "18 renderer identities",
  "native X11, Wayland and Win32 platforms" and "compiled effects on 13 identities". With METAL's option and the retirements the last figure becomes **11 of 14 identities** (EasyGL ×3, VULKAN, WEBGPU, SOFTWARE, DIRECTX9, DIRECTX11, SDL_GPU, METAL, FNA3D); the ABI is 0.46.0 (R3 §1).
- L744 (CURRENT for its Apple sentence) and L838 (OK-GENERIC for "Apple/Metal") carry policy-(b) content (SDL-free X11 lanes, Win32 harness under Wine, native Wayland) for the platform pass.

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 110 (+extra) | `seven renderer families (<code>SDL_GPU</code>, <code>VULKAN</code>, <code>WEBGPU</code>, <code>DIRECTX11</code>, <code>DIRECTX12</code>, the EasyGL family and <code>SOFTWARE</code>) classify Texture2D and render-target formats themselves` | METAL now classifies formats (`MetalRenderer.mm:5216-5228`; AM4-142/147/148); policy (a). | `...seven renderer families (<code>SDL_GPU</code>, <code>VULKAN</code>, <code>WEBGPU</code>, <code>DIRECTX11</code>, <code>METAL</code>, the EasyGL family and <code>SOFTWARE</code>) classify Texture2D and render-target formats themselves, while the rest defer to the framework's <code>SurfaceFormat::Color</code>-only rule, under which any other format throws. ...` (rest unchanged) |
| 236 | `...on seven families (11 identities: <code>DIRECTX9/11/12</code>, the five EasyGL identities, <code>SDL_GPU</code>, <code>VULKAN</code>, <code>WEBGPU</code>); factor-only on <code>METAL</code>;` | Metal samples both specular textures and TEXCOORD_1 (AM4-085; R2 §6 "factors only" stale); policy (a). | `<p style="margin-top:0.5rem;"><strong>Where it draws:</strong> full metallic-roughness PBR with specular-texture sampling on seven families (9 identities: <code>DIRECTX9/11</code>, the three EasyGL identities, <code>SDL_GPU</code>, <code>VULKAN</code>, <code>WEBGPU</code>, <code>METAL</code>); a reduced CPU cross-check on <code>SOFTWARE</code>; <code>FNA3D</code> refuses PBR draws by name.` (rest unchanged; Metal still has no shadow sampling/IBL, so the next sentence stays true) |
| 274 | `...so real video playback is native Linux/macOS only, and the optional split was not run on macOS by its author.` | macOS trees on the M4 were built with Homebrew FFmpeg (AM4-004, AM4-130); the floor caveat is the real limit (R2 §2.10, §2.14). | `...FFmpeg is never built on Windows, Emscripten, Android or iOS, so real video playback is native Linux/macOS only. CNA's Mac mini M4 runs linked Homebrew's FFmpeg; a binary linked against it starts only on the macOS that FFmpeg was built for, so build with <code>CNA_ENABLE_VIDEO=OFF</code>, or against an FFmpeg built for the 13.3 floor, to keep that floor. Unrecognised video pixel formats render magenta rather than raising an error. See <a href="docs/video-playback.html">Video playback</a>.</p>` |
| 289 | `...<strong>Direct3D 11/12</strong> and <code>FNA3D</code>; ... It is not available on <code>OPENGLES2</code>/<code>WEBGL1</code>, <code>METAL</code> or the 2D-only renderers.` | Metal MSAA (AM4-141); policy (a). | `<p>Enabled via <code>GraphicsDeviceManager</code>: set <code>PreferMultiSampling = true</code> and <code>MultiSampleCount</code> on <code>PresentationParameters</code> before device creation. Support is decided per device: MSAA is reported (probed where the API requires it) on the EasyGL identities, <strong>Vulkan</strong>, <strong>WebGPU</strong>, <strong>SDL_GPU</strong>, <strong>Direct3D 11</strong>, <strong>Metal</strong> (2x and 4x on an Apple M4) and <code>FNA3D</code>; <strong>Software</strong> implements 4x MSAA on the CPU. It is not available on the 2D-only <code>SDL_RENDERER</code>.</p>` |
| 296 | `...They are not available on <code>OPENGLES2</code>/<code>WEBGL1</code>, <code>SDL_GPU</code> or <code>METAL</code>, and the two 2D-only renderers (SDL_Renderer and Canvas)` | Metal occlusion queries (AM4-038); FNA3D's Metal driver and WebGPU-on-Metal limits (R2 §2.5, §2.7); policy (a). | `<p>Hardware occlusion queries are reported by the EasyGL identities, <strong>Vulkan</strong>, <strong>WebGPU</strong>, <strong>Direct3D 9/11</strong>, <strong>Metal</strong> (one query open at a time) and <code>FNA3D</code>, by <code>SOFTWARE</code> as a CPU implementation, and by <code>HEADLESS</code> without rasterizing. They are not available on <code>SDL_GPU</code> or on <code>FNA3D</code>'s Metal driver on Apple, WebGPU on Apple's Metal backend counts them only as a boolean, and the 2D-only SDL_Renderer has no GPU query API at all. Under the default <code>Reach</code> profile an <code>OcclusionQuery</code> throws unless <code>HiDef</code> is requested.</p>` |
| 526 | `<td>2D + 3D (conservative)</td><td>macOS-only; no MSAA, MRT, occlusion, instancing or float targets, Color format only; automatic macOS CI builds it, but fresh macOS run validation is an open external boundary.</td>` | R2 §2.4, §6 (AM4-037, 038, 097, 141..148, 159). | `<tr><td><code>METAL</code></td><td>Supported (declared)</td><td>2D + 3D</td><td>macOS and iOS; MSAA, MRT, occlusion, instancing, float targets and DXT native, SpriteBatch-scoped MSL custom effects, compiled effects opt-in; full test suite passed on a physical Mac mini M4 (on-screen presentation not observed); iOS evidence is the Simulator.</td></tr>` |
| 532 | `...the default on Windows, macOS, iOS and Android, and the only renderer allowed on iOS.` | iOS allow-list has METAL too. | `<tr><td><code>SDL_RENDERER</code></td><td>Production (declared), within 2D scope</td><td>2D only</td><td>Portable SDL path with deliberate 3D rejection; the default on Windows, macOS, iOS and Android, and one of the two renderers allowed on iOS (with <code>METAL</code>).</td></tr>` |
| 561 | METAL row `Y Y – – Y Y – – Y – – Y Y – – – – – –` | See note. | `<tr><td><code>METAL</code></td><td>Y</td><td>Y</td><td>c</td><td>Y</td><td>Y</td><td>Y</td><td>Y</td><td>Y</td><td>Y</td><td>Y</td><td>Y</td><td>Y</td><td>Y</td><td>c</td><td>Y</td><td>Y</td><td>Y</td><td>&ndash;</td><td>&ndash;</td></tr>` |
| 583 | `<tr><td><code>METAL</code>, <code>HEADLESS</code>, <code>STUB</code>, <code>SDL_RENDERER</code>, <code>CANVAS</code></td><td>Never</td><td>No implementation</td></tr>` | AM4-144; policy (a). | `<tr><td>Metal (<code>METAL</code>)</td><td>With the option</td><td><code>CNA_METAL_COMPILED_EFFECTS</code>; MojoShader's SPIR-V output translated to MSL by SPIRV-Cross</td></tr><tr><td><code>HEADLESS</code>, <code>STUB</code>, <code>SDL_RENDERER</code></td><td>Never</td><td>No implementation</td></tr>` |
| 602 | `<td><code>METAL</code></td><td>macOS only (iOS and tvOS refuse it)</td><td>SDL3 is the macOS platform</td><td>Objective-C++; AppKit, Metal, QuartzCore, Foundation</td>` | AM4-037; UIKit on iOS; compiled-effect deps (AM4-144). | `<tr><td><code>METAL</code></td><td>macOS and iOS (tvOS and the other Darwin targets refuse it)</td><td><strong>Yes</strong> (SDL3 supplies the window)</td><td>Objective-C++; Metal, QuartzCore, Foundation, and AppKit (macOS) or UIKit (iOS); MojoShader and SPIRV-Cross with compiled effects</td></tr>` |
| 612 | `One combination rule is enforced: Windows-only, Emscripten-only and macOS-only identities cannot mix.` | Apple-only. | `...One combination rule is enforced: Windows-only, Emscripten-only and Apple-only identities cannot mix. ...` (rest unchanged) |
| 620 | `It is the default on Windows, macOS, iOS, Android and other non-Linux hosts and the only renderer allowed on iOS.` | iOS allow-list has METAL too. | `...It is the default on Windows, macOS, iOS, Android and other non-Linux hosts and one of the two renderers allowed on iOS (with <code>METAL</code>). ...` (rest unchanged) |
| 712 | `<span class="status-badge status-partial">Supported (declared) &mdash; macOS only</span>` | AM4-037. | `<span class="status-badge status-partial">Supported (declared) &mdash; macOS and iOS</span>` |
| 714 | `A native Apple Metal renderer; SDL3 supplies only the window and <code>CAMetalLayer</code>. It is macOS-only (iOS and tvOS refuse it) and the most conservative 3D renderer: no MSAA, MRT, ... and factor-only PBR.` | R2 §2.4, §6; AM4-085; own view (`MetalRenderer.mm:4869-4876`). | `<p>A native Apple Metal renderer; SDL3 supplies the window and the renderer adds its own <code>CAMetalLayer</code>-backed view. It runs on macOS and, experimentally, on iOS (tvOS and the other Darwin targets refuse it). Since CNA's Mac mini M4 campaign it implements MSAA, multiple render targets, occlusion queries, instancing and multi-stream input, float, packed and DXT formats, cube and volume textures, full PBR with specular textures, and SpriteBatch-scoped MSL custom effects; compiled XNA effects need <code>-DCNA_METAL_COMPILED_EFFECTS=ON</code>, and it has no compute or indirect-draw path. Selected with <code>-DCNA_GRAPHICS_RENDERER=METAL</code>.</p>` |
| 715 | `<strong>Evidence boundary:</strong> automatic macOS CI builds it and runs the <code>Metal</code> tests, but CNA's own Metal page treats a fresh compile-and-run of the adapted native source as an open external validation boundary.` | AM4-156, AM4-159, AM4-208; hosted GPU paravirtual (AM4-279); R2 §2.16. | `<p style="margin-top:0.5rem;"><strong>Evidence boundary:</strong> on a physical Mac mini M4 its full test suite passes (11,015 tests) and its Metal tests pass 261/261 under Metal's validation layers, in Debug and Release. CNA calls it supported, not primary-production, because compiled effects are off by default, on-screen presentation was never observed (the console was locked), no physical iOS device ran it and no soak run has bounded its caches. The automatic macOS CI job builds it and runs its Metal tests on a paravirtual GPU; no green run is recorded after the campaign.</p>` |
| 772 | `macOS/Metal has automatic CI (deployment floor macOS 13.3). iOS is experimental and restricted to <code>SDL_RENDERER</code> (floor iOS 16.3): CI final-links a device app and launches a one-frame simulator smoke path, without a physical-device or pixel-correctness claim.` | R2 §2.1, §3, §6, §7 items 1, 6. | `<p>macOS is tested on real hardware: every renderer that applies there passed its full test suite on a physical Mac mini M4 (Apple silicon, macOS 27; no Intel Mac was run), and automatic workflows build it on GitHub's <code>macos-26</code> runners (deployment floor macOS 13.3). iOS is experimental, with <code>SDL_RENDERER</code> and <code>METAL</code> allowed (floor iOS 16.3): a <code>METAL</code> pixel probe reads back exact pixels in the iOS Simulator (8 of 8 launches, iPhone 17 profile), while the device build is final-linked and has not run on a physical iPhone or iPad. tvOS is unsupported.</p>` |
| 807 (+extra) | `<span class="status-badge status-partial">Experimental &mdash; ABI 0.44.0</span>` | Policy (c); R3 §1. | `<span class="status-badge status-partial">Experimental &mdash; ABI 0.46.0</span>` |
| 808 (+extra) | `<h3>C API (C ABI 0.44.0)</h3>` | Policy (c). | `<h3>C API (C ABI 0.46.0)</h3>` |
| 809 (+extra) | `The version is 0.44.0 (alpha.1: 0.7.0) ... a <code>hello_cna</code> example is exercised by a local consumer test on Linux.` | ABI 0.46.0; installed-consumer test on macOS, shared and static (AM4-210, 211, 213; R3 §2). | `...The version is 0.46.0 (alpha.1: 0.7.0) and remains an experimental <code>0.x</code> ABI; renderer identity values are stable and unused ones stay reserved. A recorded baseline (197 struct layouts, 3,210 exports) is enforced by header-only gates, and a <code>find_package(CNA CONFIG)</code> package with <code>CNA::CApi</code> and a <code>hello_cna</code> example is exercised by a local consumer test on Linux and, on a physical Mac mini M4, by an installed-package test that builds and runs <code>hello_cna</code> against the shared <code>libcna_c_api.dylib</code> and against the static archive.</p>` (first sentence unchanged) |
| 810 (+extra) | `...7,030 implemented, 15 partial, 656 planned and 441 not applicable ... because of those 656. No CNA CI job builds the C library; the CNA.NET project builds and uses it on Linux from source identical to this snapshot.` | Coverage at c1c316b9: 7,053 / 15 / 631 / 443, gate "631 unmapped" (R3 §1); macOS local evidence 119/119 (R3 §2); CNA.NET osx-arm64 local (R3 §3). "source identical to this snapshot" is not established for c1c316b9 (CNA.NET admitted 0.46.0 at CNA `a3da0a5bb`). | `<p style="margin-top:0.5rem;"><strong>Status:</strong> CNA's semantic inventory lists 8,142 public C++ symbols &mdash; 7,053 implemented, 15 partial, 631 planned and 443 not applicable &mdash; and its own release gate reads &ldquo;Not ready&rdquo; because of those 631. No CNA CI job builds the C library. It has been built and tested on a physical Mac mini M4, where every C API test passes (119/119, <code>SOFTWARE</code> and <code>SDL_RENDERER</code> configurations), and CNA.NET builds and uses it on Linux and, as local evidence without a CI leg, on macOS (osx-arm64). The C# binding <a href="docs/cna-net.html">CNA.NET</a> is the maintained consumer and admits exactly this ABI version; the Common Lisp, Go, Java, Python, Ruby, Rust, Swift and TypeScript bindings are archived and not maintained. See the <a href="docs/c-api.html">C API page</a>.</p>` |

CURRENT (keep): L147 SDL sensors on iOS; L416 no SDL-free audio on macOS; L476 SDL3 default/only CI platform on macOS/iOS; L525 SDL_GPU on Metal devices via shadercross (optionally "full suite run on a Mac mini M4 on SDL's Metal driver; no occlusion queries, LOD bias ignored"); L598 WEBGPU native on macOS; L599 shadercross ON on Apple; L691 SDL_GPU translated for Metal devices, ShaderEffect unavailable on Apple (AM4-175); L744 "macOS also has an automatic CI job of its own for METAL" (optionally add "and a full local qualification on a Mac mini M4"); L802 inspector refused on iOS; L821 "current AppleClang" in CI.
OK-GENERIC: L713 h3 "Metal Renderer"; L771 h3 "macOS / iOS"; L838 "Apple/Metal" in the workflow summary and its "build/link/simulator evidence must not be upgraded into a physical-device ... claim" (still a correct caution).

---

## 7. deep-dives/renderers/native-gpu-evidence-tiers.html

### deep-dives/renderers/native-gpu-evidence-tiers.html
Counts: STALE 9 · CURRENT 2 · OK-GENERIC 6  (16 regex hit lines + 1 extra: L163)

Section notes:
- Both tables (L148-156 "Four identities", L169-177 "What each identity's evidence actually covers") need new METAL rows, and the SDL_GPU and WEBGPU evidence rows must gain their macOS
  results (SDL_GPU on SDL's Metal driver 10,962/10,962; WEBGPU on wgpu-native's Metal backend 10,968/10,968; both M4-LOCKED, R2 §2.5-2.6).
- The two refusal messages quoted at L182 no longer exist in `MetalRenderer.mm` at c1c316b9 (0 matches); current named refusals include
  `"Metal SamplerState.MipMapLevelOfDetailBias: this Metal device ignores MTLSamplerDescriptor.lodBias (measured), so a non-zero bias is refused."` (`MetalRenderer.mm:3092-3093`)
  and `"Metal RenderTarget2D array slices are not supported."` (`:5335`).
- CNA-BUG-099 (linked at L173) is a Linux/RADV record of 25-26 failing classic `^SdlGpu` CTests; at c1c316b9 the SDL_GPU full tree on the M4 (Metal driver) has no failing case and AM4-092/181/183/184 fixed SDL_GPU tests and renderer paths. The known-issue page should be re-checked (it may still hold on Linux; do not claim it fixed there).
- Optional new "defect shapes" bullets (L200-210, not counted): *a skip counted as a pass* — before AM4-088 the WebGPU GPU tests on macOS returned the skip code (no X11/Wayland socket) and ctest counted 148 skips as passes; *a disabled check hiding a second bug* — Metal's clear-only readback had two causes, readback switched off and a transposed world-view-projection matrix (AM4-025, AM4-028).
- L144 "Four of CNA's 18 renderer identities" → 14 is a renderer-pass item (counted OK-GENERIC here).

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 154 | `<td><code>METAL</code></td><td>Supported; native</td><td>Metal directly (macOS only)</td>...<td>none: creation throws</td><td>yes / refused</td><td>refused: creation throws</td>` | iOS (AM4-037); custom MSL SpriteBatch effects (AM4-077); MRT up to 8 (AM4-097); occlusion queries (AM4-038). | `<tr><td><code>METAL</code></td><td>Supported; native</td><td>Metal directly (macOS and iOS)</td><td>MSL embedded as a string, compiled with <code>newLibraryWithSource:</code> at run time</td><td>MSL source pairs, for SpriteBatch only (a 3D draw with a custom effect throws)</td><td>yes / up to 8</td><td>real; one query open at a time, counts summed across encoders</td><td><code>BGRA8Unorm</code> layer</td></tr>` |
| 162 | `...so a member they do not name is false (<code>METAL</code> names thirteen of the nineteen)` | Renderer-level statement still true, but at device level METAL's float/half-float members are derived true and CompiledEffects is build-dependent (`GraphicsDevice.cpp:3453-3480`); readers take it as "Metal answers six members false". | `...<code>VULKAN</code>, <code>SDL_GPU</code> and <code>METAL</code> answer from switches without a <code>default:</code> arm, so a member they do not name is false at the renderer level (<code>METAL</code> names the thirteen original members and decides <code>MultiSampleAntiAliasing</code> per device), while <code>WEBGPU</code> overrides the members it probes and lets the rest fall through to the shared default.</li>` |
| 163 (+extra) | `On <code>SDL_GPU</code> the renderer's own switch answers compute, indirect draw and the float render-target members false, while <code>GraphicsDevice</code> derives them ... and answers true.` | Same holds for METAL's float/half-float members (AM4-142; `MetalRenderer.mm:5216-5221`, `:5268-5271`). | `<li><strong>A device-level answer versus a renderer-level answer.</strong> On <code>SDL_GPU</code> the renderer's own switch answers compute, indirect draw and the float render-target members false, while <code>GraphicsDevice</code> derives them from dedicated queries and format probes and answers true; <code>METAL</code> is the same for the float and half-float members. The device-level answer is the public one; a caller holding the renderer interface directly sees different values.</li>` |
| 173 | SDL_GPU evidence row: `...SDL_gpu's Vulkan driver on Linux; a cross-compiled Direct3D 12 probe ... Not established: Native Direct3D 12 presentation; any Metal run; a green classic suite (... CNA-BUG-099)` | SDL_GPU on SDL's Metal driver: full tree 10,962/10,962 on the M4 (AM4-208; R2 §2.6, §6 "SDL_GPU's Metal driver route has no native execution evidence" stale). | `<tr><td><code>SDL_GPU</code></td><td>Pixel, lifecycle and modern-resource tests in its own directory, fatal on validation output, plus the parity corpus</td><td>SDL_gpu's Vulkan driver on Linux; SDL's Metal driver on a physical Mac mini M4 (the full test suite of an <code>SDL_GPU</code> tree, 10,962 tests with no failure, console locked); a cross-compiled Direct3D 12 probe run under Wine with vkd3d-proton</td><td>No workflow selects it</td><td>Native Direct3D 12 presentation; a green classic suite on Linux (CNA's last Linux record lists 26 failing classic <code>SdlGpu_*</code> tests, <a href="../../known-issues/bugs/cna-bug-099.html">CNA-BUG-099</a>); sampler LOD bias on Metal, which SDL's Metal backend ignores</td></tr>` |
| 174 | WEBGPU evidence row: `Native on Linux x86_64; ... No workflow selects it ... Not established: The other pinned native packages (Windows, macOS, Linux aarch64)` | macOS arm64 wgpu-native package ran the full suite (10,968/10,968; AM4-088..131; R2 §2.5); the "148/148" figure must not be used (R2 §8). Also (not Apple) the Emscripten workflow now builds a `WEBGL2;WEBGPU` bundle (`emscripten-multi-renderer-ci.yml:121-164`, build + bundle assertion only). | `<tr><td><code>WEBGPU</code></td><td>A WebGPU-labelled test set, a native smoke test, pure-CMake checksum and present-mode mapping tests, plus the parity corpus</td><td>Native on Linux x86_64 and on a physical Mac mini M4 (wgpu-native on its Metal backend: the full test suite, 10,968 tests with no failure, rendered offscreen with the console locked); browser pages driven in headless Chrome by CNA's scripts</td><td>Built, not run, in the Emscripten bundle workflow (<code>WEBGL2;WEBGPU</code>); no workflow runs its tests</td><td>The other pinned native packages (Windows, Linux aarch64); on-screen presentation on macOS; cross-browser behaviour</td></tr>` |
| 175 | METAL evidence row: `<code>Metal_PortableHelpers</code>, <code>Metal_Smoke</code> (clear and present) and <code>Metal_Capabilities</code> ... macOS, in CI ... Representative 3D draw pixels; its readback is refused, so pixel tests cannot run` | R2 §2.4 (AM4-026, 149..159), §2.16 (AM4-255, 279, 306); readback native (AM4-025). | `<tr><td><code>METAL</code></td><td>Native smoke, capability, MRT, MSAA, depth-bias, packed-format, skinned-normal and presentation tests, plus 101 shared pixel fixtures and 146 renderer-neutral oracles run through <code>METAL</code> (<code>ctest -L Metal</code>, 261 tests), all under <code>MTL_DEBUG_LAYER</code> and <code>MTL_SHADER_VALIDATION</code>; <code>Metal_PortableHelpers</code> also runs in every other configuration</td><td>A physical Mac mini M4 (macOS 27): <code>ctest -L Metal</code> 261/261 in Debug and Release and the full test suite 11,015/11,015, console locked; the iOS 27 Simulator (pixel probe); GitHub's hosted paravirtual GPU</td><td><code>metal-macos-ci.yml</code> builds on a <code>macos-26</code> runner and runs <code>ctest -R '^Metal'</code> with the API validation layer (shader validation off and one test at a time on the paravirtual device); no green run recorded after the campaign</td><td>On-screen presentation and <code>PresentInterval</code> pacing; a physical iOS device; an Intel Mac; a soak run; compiled effects in a default build</td></tr>` |
| 179 | `...its device path executes on a real Mac in CI, while much of its feature surface is deliberately outside the claimed evidence boundary (Tutorial 109: why the surface is this narrow)` | Overstatement ("real Mac in CI" — hosted GPU is paravirtual, AM4-279) and understatement (feature surface now evidenced, AM4-159). | `<p>The <code>METAL</code> row changed the most in this snapshot: CNA's Mac mini M4 campaign re-enabled each capability that had been refused (readback, MSAA, multiple render targets, occlusion queries, instancing, custom effects, every surface format) together with native tests under Metal's validation layers, so its pixel evidence now comes from real Apple hardware rather than from CI. What it still lacks is in the last column (<a href="../../docs/tutorials/109-metal-macos.html#why-narrow">Tutorial 109: how the surface was widened</a>).</p>` |
| 182 | `<code>METAL</code> shows the safer pattern: enumerate the unsupported surface, throw at the boundary, and widen it only when a platform-specific observation proves the new path. Its refusals name their reason, for example "Metal backbuffer readback is disabled because ..." and "Metal OcclusionQuery is disabled until ..."` | Both quoted refusals removed (AM4-025, AM4-038); the pattern itself played out (AM4-025..159). | `<p>Because the shared capability default is permissive, a renderer can overclaim by doing nothing. <code>METAL</code> shows the safer pattern: it enumerated the unsupported surface, threw at the boundary, and widened it only when a platform-specific observation proved the new path &mdash; readback, occlusion queries, MSAA and the rest were each re-enabled on a Mac mini M4 together with native tests. Its remaining refusals still name their reason, for example <code>"Metal SamplerState.MipMapLevelOfDetailBias: this Metal device ignores MTLSamplerDescriptor.lodBias (measured), so a non-zero bias is refused."</code> and <code>"Metal RenderTarget2D array slices are not supported."</code> in <a class="src-link" href="…/modules/renderers/metal/src/MetalRenderer.mm"><code>MetalRenderer.mm</code></a>. Callers get an early diagnostic instead of a later blank frame.</p>` |
| 197 | `<code>METAL</code>: the only macOS evidence is the CI lane above; CNA's own Metal page treats a fresh macOS run of the adapted Objective-C++ source as an external validation boundary.` | R2 §2.4, §2.16; AM4-279, AM4-289, AM4-306; R2 §7 item 6. | `<li><code>METAL</code>: record the machine and whether the console was unlocked. CNA's macOS evidence comes from one physical Mac mini M4 (Apple GPU, validation layers on, console locked so every window was occluded) and from the iOS Simulator. GitHub's hosted runner exposes an &ldquo;Apple Paravirtual device&rdquo; that cannot run Metal shader validation and needed its GPU tests serialised, so a hosted result is evidence for that device only. An Intel or AMD Mac GPU differs again: it has no packed 16-bit formats and needs managed-storage synchronisation, which CNA implements but no Intel Mac has run.</li>` |

CURRENT (keep): L152 SDL_GPU row (SDL picks Metal; shadercross translation for Metal); L194 "A Vulkan result says nothing about Direct3D 12 or Metal" (optionally add "SDL_GPU's Metal driver now has its own result, from the Mac mini M4").
OK-GENERIC: L7 meta description, L8 keywords, L13 og:description, L19 JSON-LD (lists the four identities; bump `dateModified`); L144 lede (identity count is a renderer-pass item); L192 Vulkan-vs-Metal principle.

---

## 8. deep-dives/platforms/cross-platform-contract.html

### deep-dives/platforms/cross-platform-contract.html
Counts: STALE 7 · CURRENT 3 · OK-GENERIC 4  (14 regex hit lines)

Section notes:
- Three of the STALE lines (L194, L203, L224) are hits only because a policy-(b) sentence mentions Apple in passing; their Apple content is correct, but the lines must change, so replacements are given.
- CNA-internal naming to be aware of (do not copy): `cmake/RendererCombinations.cmake:25` still calls METAL's combination partition `CNA_RENDERER_MACOS_ONLY` and reports it as "macOS" (`:50-51`), although `RendererSelection.cmake:140-143` admits METAL on iOS too. The site should say "Apple-only" (macOS and iOS); the partition rule (no mixing with Windows-only or browser-only identities) is unaffected.
- The evidence table (L241-251) has a Web row (L247) with retired identities — renderer pass.

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 179 | `host-exclusive values on the wrong host: <code>WIN32</code> off Windows, <code>TERMINAL</code> on Windows, <code>X11</code>/<code>WAYLAND</code> without their development packages, <code>ALSA</code> off Linux, and the OS partitions of the renderer set (three Windows-only identities, three Emscripten-only ones, macOS-only <code>METAL</code>; ...)` | METAL is macOS + iOS (AM4-037); partitions at c1c316b9: DIRECTX9/DIRECTX11, WEBGL2, METAL (`RendererCombinations.cmake:20-25`); policy (b): no WIN32/X11/WAYLAND values (`PlatformSelection.cmake:24-32`). | `<li>host-exclusive values on the wrong host: <code>TERMINAL</code> on Windows, <code>ALSA</code> off Linux, and the OS partitions of the renderer set (two Windows-only identities, one Emscripten-only one, and <code>METAL</code>, which is limited to macOS and iOS; <a class="src-link" href="…/cmake/RendererCombinations.cmake"><code>RendererCombinations.cmake</code></a>);</li>` |
| 194 | `...on iOS, UIKit owns the process and must start before the game's entry point runs. ... Under <code>HEADLESS</code>, <code>TERMINAL</code> and <code>WIN32</code> the header is empty ...; <code>WIN32</code> deliberately imposes no <code>WinMain</code>, so a console or test host keeps its own <code>main()</code>.` | Apple content current; policy (b) (WIN32). `Entrypoint.hpp` at c1c316b9 names only HEADLESS and TERMINAL as entry-point-free. | Keep the paragraph up to "...gets the rename (<a …><code>PlatformSelection.cmake</code></a>)." then: `Under <code>HEADLESS</code> and <code>TERMINAL</code> the header is empty, and those implementations report the <code>managedEntrypoint</code> capability as false, so a console or test host keeps its own <code>main()</code>.</p>` |
| 201 | `...the only implementation any CI job configures on macOS, iOS, Android and the web (CMake also offers HEADLESS and TERMINAL there, and X11 on macOS); mobile entry-point glue` | Policy (b): no X11 platform (`PlatformSelection.cmake:24-32`); SDL3 reaches macOS through Cocoa, iOS through UIKit (R2 §1). | `<tr><td><code>SDL3</code> (default)</td><td>always</td><td>SDL3 window, event, input and system-service adaptation, reaching Windows, X11, Wayland, macOS (Cocoa), iOS (UIKit), Android and the browser through SDL's video drivers; the only implementation any CI job configures on macOS, iOS, Android and the web (CMake also offers <code>HEADLESS</code> and <code>TERMINAL</code> there); mobile entry-point glue</td></tr>` |
| 203 | `<tr><td><code>WAYLAND</code></td><td>non-Windows, non-Apple, non-mobile, non-web targets ...` | Policy (b): no WAYLAND platform value at c1c316b9 (Apple mention incidental). | Delete the row (Wayland is reached through SDL3's Wayland video driver; platform pass). |
| 224 | `...And Windows and macOS have no SDL-free audio value, so a fully SDL-free <code>WIN32</code> build is silent (<code>NULL</code>).` | Apple claim current; policy (b) (WIN32). | `...And Windows and macOS have no SDL-free audio value, so a fully SDL-free build there is silent (<code>NULL</code>). What each value does to the sound route is on the <a href="../../docs/audio.html">audio guide</a> and <a href="../../docs/tutorials/137-alsa-audio.html">Tutorial 137</a>.</p>` (earlier sentences unchanged) |
| 248 | `<tr><td>macOS and iOS</td><td>workflows that build and launch an <code>.app</code>, build <code>METAL</code>, final-link an iOS device bundle and launch one simulator frame</td><td>physical iOS devices, Retina and frame-pacing observations</td></tr>` | Workflows now on macos-26 with iOS METAL legs and the pixel probe; hosted Metal GPU is paravirtual (R2 §2.16, §3); local M4 evidence beyond CI (AM4-208, AM4-120); open items R2 §7 items 1, 2, 6, 7. | `<tr><td>macOS and iOS</td><td>workflows on <code>macos-26</code> runners that build and launch an <code>.app</code>, build <code>METAL</code> and run its Metal tests on a paravirtual GPU, final-link iOS device bundles for <code>SDL_RENDERER</code> and <code>METAL</code>, and launch the simulator smoke app plus, for <code>METAL</code>, a pixel probe; beyond CI, CNA's own full test suites on a physical Mac mini M4</td><td>a green hosted run after the campaign; physical iOS devices; on-screen presentation and frame pacing (the Mac mini runs had a locked console); Intel Macs</td></tr>` |
| 252 (callout) | `The Emscripten, Apple and Metal workflows (like the content-pipeline Windows workflow) pin August 2026 sharp-runtime revisions ... stops at configure time with 'Unknown Sharp Runtime component' (CNA-BUG-199)` | Pins replaced by `scripts/ci/sibling_branch.sh` (AM4-234; checked in all four workflows at c1c316b9); R2 §6. | `<div class="callout callout--warn"><span class="callout-icon">&#9888;</span><p>The Web, macOS and iOS cells state what those workflows are configured to do, not runs that passed: every workflow now checks out the sharp-runtime branch that CNA's sibling script chooses, but no green hosted run of the Apple or Metal workflow is recorded after the Mac mini M4 campaign. The macOS and iOS evidence that did execute is CNA's own: full test suites on a physical Mac mini M4 and a pixel probe in the iOS Simulator (see <a href="android-and-apple-platforms.html">Android and Apple</a>); the per-workflow detail is on the <a href="../../docs/platforms.html#ci">platforms guide</a>. Nothing on this page was built or run.</p></div>` |

CURRENT (keep): L139 target-OS row (`CNA_TARGET_APPLE/IOS/MACOS`); L210 iOS and Android are target OSes served by SDL3; L227 TargetPlatform/`getCurrentPlatformName()`/`DesktopOS::MacOSX`.
OK-GENERIC: L89 sidebar link; L215 `RendererWindowKind::Metal`; L249 Android row link to "Android and Apple"; L268 related-pages link.

---

## 9. docs/verification.html

### docs/verification.html
Counts: STALE 7 · CURRENT 2 · OK-GENERIC 2  (8 regex hit lines + 3 extras: L421, L523, L553)

Notes: not counted (policy (c), no Apple term) but on this page: L522 "ABI **0.44.0**" and "7,030 implemented, 15 partial, 656 planned, 441 not applicable" → 0.46.0 and 7,053 / 15 / 631 / 443 (R3 §1); L731 deep-dive description "C ABI 0.44.0 ... 656 unmapped" → 0.46.0 / 631. L556 (ES2-generation profiles) is a renderer-pass item.

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 299 | `<td><code>METAL</code></td><td>An automatic macOS-14 build plus the supported Metal contract tests</td><td>Fresh native macOS compile-and-run validation of the adapted source, which CNA's own Metal page treats as an external gate</td>` | AM4-025..159 (261/261, 101 pixel fixtures, 146 oracles), AM4-208, AM4-120; macos-26 (AM4-255); R2 §7. | `<tr><td><code>METAL</code></td><td>On a physical Mac mini M4, <code>ctest -L Metal</code> 261/261 under Metal's validation layers (101 shared pixel fixtures, 146 renderer-neutral oracles, 14 native tests) in Debug and Release, and the full test suite of a <code>METAL</code> tree; an iOS Simulator pixel probe; an automatic <code>macos-26</code> build that runs the Metal tests on a paravirtual GPU</td><td>On-screen presentation; a physical iOS device; an Intel Mac; a green hosted run after the campaign</td></tr>` |
| 418 | `...links <code>WEBGL2;WEBGL1;CANVAS</code> ... by a static reading it (and the Apple, Metal and Devices workflows) stops at configure at this snapshot because they pin an old sharp-runtime revision (CNA-BUG-199).` | Pins gone (AM4-234); policy (a): bundle is `WEBGL2;WEBGPU` (`emscripten-multi-renderer-ci.yml:121-164`). | `<tr><td>Emscripten and browser</td><td><code>emscripten-multi-renderer-ci.yml</code> links <code>WEBGL2;WEBGPU</code> into one WebAssembly bundle and asserts that both renderers and the JavaScript selection surface are in it</td><td>The lane is designed to establish configure/build/link, not browser behaviour.</td></tr>` |
| 420 | `<code>apple-ci.yml</code>: Apple CMake layer check, a macOS-14 build with portable tests, an iOS device final link and an iOS simulator launch of one frame; <code>metal-macos-ci.yml</code>: native Metal contract tests</td><td>No physical-iOS-device or pixel-correctness claim.` | macos-26; iOS METAL legs + pixel probe; paravirtual GPU; no green post-campaign run (R2 §2.16, §3). "no pixel-correctness claim" is now wrong for the Simulator (R2 §8). | `<tr><td>Apple</td><td><code>apple-ci.yml</code> on <code>macos-26</code>: Apple CMake layer check, a macOS build with portable tests and an <code>.app</code> launch, iOS device final links and simulator launches for <code>SDL_RENDERER</code> and <code>METAL</code>, with a pixel probe on <code>METAL</code>; <code>metal-macos-ci.yml</code>: the Metal tests on GitHub's paravirtual GPU (API validation only)</td><td>No green hosted run is recorded after the Mac mini M4 campaign, and no physical-iOS-device claim is made. CNA's own full-suite runs on a physical Mac mini M4 are local evidence, not CI.</td></tr>` |
| 421 (+extra) | `...The release gate itself reports "Not ready" (656 public symbols unmapped). Whether the library builds at this snapshot was not verified here.` | 631 unmapped (R3 §1); CNA's own record now shows the library built and its tests passing on macOS (AM4-209..214, R3 §2). | `<td>All five are build-free header and inventory checks: no workflow builds the C library. The release gate itself reports "Not ready" (631 public symbols unmapped). CNA's own records show the library built on a physical Mac mini M4 with every C API test passing (119/119, <code>SOFTWARE</code> and <code>SDL_RENDERER</code> configurations); that was not re-run here.</td>` |
| 523 (+extra) | `...No CNA CI job builds the library; CNA.NET builds and uses it on Linux.` | CNA.NET osx-arm64 local evidence (AM4-215..231; R3 §3). | `<td>Maps CNA's own C++ declarations to C ABI rows. "Implemented" means a mapped route, not a behaviour test, and the figures are not comparable with alpha.1's (ABI 0.7.0). No CNA CI job builds the library; CNA.NET builds and uses it on Linux and, as local evidence on a Mac mini M4, on macOS (osx-arm64).</td>` |
| 553 (+extra) | `...eight opt-in build options that default to OFF (EasyGL, Vulkan, WebGPU, Software, <code>DIRECTX9</code>, <code>DIRECTX11</code>, <code>DIRECTX12</code>, <code>SDL_GPU</code>). A default configure therefore reports <code>CompiledEffects</code> false on 17 of the 18 identities.` | `CNA_METAL_COMPILED_EFFECTS` (AM4-144); policy (a). | `<li><strong>Compiled effects are renderer-qualified.</strong> XNA/FNA D3D9 Effect Framework bytecode runs on nine renderer families: <code>FNA3D</code> always, and eight opt-in build options that default to OFF (EasyGL, Vulkan, WebGPU, Software, <code>DIRECTX9</code>, <code>DIRECTX11</code>, <code>SDL_GPU</code>, <code>METAL</code>). A default configure therefore reports <code>CompiledEffects</code> false on 13 of the 14 identities. ...` (rest unchanged) |
| 557 | `<strong><code>METAL</code> is the most conservative 3D renderer.</strong> It reports no MSAA, MRT, ... and only <code>SurfaceFormat.Color</code>. ... the only automatic evidence is the macOS-14 build and its contract tests.` | R2 §2.4, §6, §7 (AM4-159). | `<li><strong><code>METAL</code> is supported, not primary-production.</strong> Since CNA's Mac mini M4 campaign it implements MSAA, multiple render targets, occlusion queries, instancing, multi-stream input, float, packed and DXT formats and SpriteBatch-scoped MSL custom effects, with native pixel tests under Metal's validation layers on that machine. What remains: compiled XNA effects need <code>CNA_METAL_COMPILED_EFFECTS=ON</code>; custom effects cannot draw 3D; there is no compute or indirect draw; <code>PresentInterval.Two</code> presents as <code>One</code>; and on-screen presentation, a physical iOS device, an Intel Mac and a soak run are unmeasured.</li>` |

CURRENT (keep): L566 FFmpeg never built on iOS; L599 FFmpeg optional on Linux and macOS.
OK-GENERIC: L717 preset list (`macos`, `ios`, `ios-simulator` still exist, 17 visible at c1c316b9); L735 deep-dive link description.

---

## 10. roadmap.html

### roadmap.html
Counts: STALE 12 · CURRENT 1 · OK-GENERIC 0  (10 regex hit lines + 3 extras: L203, L266, L286)

Section notes: the "Metal" timeline item (L245-249) should be rewritten from "a narrow 3D contract" to "supported on a physical Mac, not yet primary-production"; the "Compiled effects" (L280), "surface-format coverage" (L286), "Gamer Services beyond Linux" (L298), "Media" (L304) and "CNA.NET on Windows, macOS and iOS" (L321-322) items each carry an Apple statement that the campaign changed. L254 (CI) also has policy-(b) content and job counts that changed with `platform-ci.yml` (no Win32/X11 jobs at c1c316b9) — recount in the platform pass. Not counted: meta description (L7/L12) only names the snapshot.

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 143 | `PBR draws are implemented on the GL family, Vulkan, SDL_GPU, WebGPU and Direct3D 9/11/12 (Metal factor-only, Software as a reduced CPU cross-check); FNA3D refuses them.` | Metal samples both specular textures (AM4-085); policy (a). | `...PBR draws are implemented on the GL family, Vulkan, SDL_GPU, WebGPU, Direct3D 9/11 and Metal (Software as a reduced CPU cross-check); FNA3D refuses them.</p>` |
| 203 (+extra) | `...it pairs with exactly C ABI 0.44.0, ... Qualified on Linux x86_64, in headless Chromium and on the x86_64 Android emulator.` | ABI 0.46.0 admitted (AM4-217); osx-arm64 local evidence (AM4-215..231; R3 §3). | `...Its public metadata matches the selected XNA 4.0 runtime profile, it pairs with exactly C ABI 0.46.0, and a <code>dotnet new</code> template creates games with desktop, browser and Android heads. Qualified on Linux x86_64, in headless Chromium and on the x86_64 Android emulator; on a physical Mac mini M4 (osx-arm64) it builds, passes its managed suites and package acceptance, and smoke-runs its 84 samples on <code>SOFTWARE</code> and <code>METAL</code>, as local evidence without a CI leg, signing or notarization. See <a href="docs/cna-net.html">C# with CNA.NET</a>.</p>` |
| 247 | `<h3>Metal — a narrow 3D contract and no compiled effects <span class="status-badge status-wip">Partial</span></h3>` | AM4-141..159. | `<h3>Metal — supported on a physical Mac, not yet primary-production <span class="status-badge status-wip">Partial</span></h3>` |
| 248 | `Metal is the most conservative 3D renderer: no MSAA, MRT, ... factor-only PBR, and no compiled-effect support. CNA declares it Supported, but its own Metal page records no fresh macOS compile-and-run result ... macOS-only, and refused on iOS.` | R2 §2.4, §3, §6, §7; AM4-037, 085, 144, 159. | `<p>Since CNA's Mac mini M4 campaign Metal implements MSAA, multiple render targets, occlusion queries, instancing and multi-stream input, float, packed and DXT formats, cube and volume textures, full PBR and SpriteBatch-scoped MSL custom effects, with compiled XNA effects behind <code>CNA_METAL_COMPILED_EFFECTS</code> (off by default); it runs on macOS and, with Simulator evidence only, on iOS. On a physical Mac mini M4 its full test suite and its 261 Metal tests under the validation layers pass. CNA declares it Supported but not primary-production: compiled effects are off by default, on-screen presentation was never observed, no physical iOS device has run it and no soak run has bounded its caches; the hosted macOS lane runs only the Metal tests, on a paravirtual GPU.</p>` |
| 254 | `...covering Linux, Apple, Emscripten, the native X11 platform and a Wine-executed Win32 harness, ... By static reading, several lanes check out <code>sharp-runtime</code> at pinned commits that predate components CNA now requires ... across 18 identities, graphics drivers, physical iOS devices` | Pins gone (AM4-234); macos-26 and no post-campaign green run (R2 §2.16); policy (a)/(b). | Replace "covering Linux, Apple, Emscripten, the native X11 platform and a Wine-executed Win32 harness, multi-renderer selection and five build-free C API gates" with `covering Linux, Apple (macOS and iOS, on <code>macos-26</code> runners), Emscripten, the <code>SDL3</code>, <code>HEADLESS</code> and <code>TERMINAL</code> platform implementations, multi-renderer selection and five build-free C API gates`; replace the "By static reading, several lanes check out ... (the causes were not investigated for this page)." sentence with `Every lane now checks out the sharp-runtime branch that CNA's sibling script chooses; no green hosted run of the Apple or Metal workflow is recorded after the Mac mini M4 campaign, whose own full-suite runs are local evidence rather than CI.`; "18 identities" → "14 identities". (File/job counts: recount in the platform pass.) |
| 266 (+extra) | `The C ABI is at 0.44.0 ... 656 public C++ symbols are still unmapped (8,142 inventoried: 7,030 implemented, 15 partial, 656 planned, 441 not applicable). No CNA CI job builds the library; the CNA.NET project builds and uses it on Linux from source identical to this snapshot. ... CNA.NET pairs with exactly 0.44.0` | Policy (c); R3 §1 figures; macOS build and tests (AM4-209..214); CNA.NET osx-arm64 (R3 §3); "source identical to this snapshot" not established for c1c316b9. | `<p>The C ABI is at 0.46.0 (alpha.1: 0.7.0) with 60 headers, 3,210 routes and 197 recorded struct layouts. Its committed release report records one unmet criterion: 631 public C++ symbols are still unmapped (8,142 inventoried: 7,053 implemented, 15 partial, 631 planned, 443 not applicable). No CNA CI job builds the library; it has been built and tested on a physical Mac mini M4 (a Mach-O <code>libcna_c_api.dylib</code> exporting exactly the 3,210 routes, a static archive and an installed-package test), and CNA.NET builds and uses it on Linux and, as local evidence, on macOS. ABI 0.x is experimental and several minor steps since alpha.1 were incompatible. The C# binding CNA.NET pairs with exactly 0.46.0; the Common Lisp, Go, Java, Python, Ruby, Rust, Swift and TypeScript bindings are <a href="docs/c-api.html#archived-bindings">archived</a> and will not follow new ABI versions. See <a href="docs/c-api.html">Experimental Native C API</a>.</p>` |
| 280 | `...on 13 of the 18 identities: FNA3D always, and thirteen more behind default-OFF build options. What remains open is Metal (no compiled-effect implementation; it needs a macOS build to develop), the 2D-only and no-pixel renderers` | Metal compiled effects exist, opt-in (AM4-144); policy (a) counts (11 of 14; see §6 note). | `<p>XNA/FNA D3D9 Effect Framework binaries now load through <code>Effect</code> and XNB <code>EffectReader</code> on 11 of the 14 identities: FNA3D always, and ten more behind default-OFF build options, <code>METAL</code>'s among them since the Mac mini M4 campaign. What remains open is the 2D-only and no-pixel renderers, and the default configure, which reports the capability on FNA3D only. HLSL <code>.fx</code> source, DXBC and MGFX remain unsupported at run time; <code>.fx</code> sources compile only at build time through an external legacy <code>fxc</code>, which was not exercised on macOS.</p>` |
| 286 (+extra) | `seven renderer families (SDL_GPU, Vulkan, WebGPU, Direct3D 11 and 12, EasyGL and Software) classify formats themselves` | Metal classifies (AM4-142/147/148); policy (a). | `...seven renderer families (SDL_GPU, Vulkan, WebGPU, Direct3D 11, Metal, EasyGL and Software) classify formats themselves, ...` (rest unchanged) |
| 298 | `The service client, relay and server are qualified on Linux only. Windows (...), macOS, a real wide-area network, ... are open` | M4: server suite 46/46 (9 skip) with Homebrew-curl client harnesses, loopback only; system libcurl refuses the relay by name (AM4-044, AM4-071, AM4-123, AM4-178; R2 §2.13, §5); networking cases on the Metal tree (AM4-200). | `<p>The service client, relay and server are qualified on Linux. On a physical Mac mini M4 the server's suite passes (46 tests, nine skipped) against CNA's client harnesses built with Homebrew's curl, on loopback only; with the SDK's libcurl, which has no WebSocket support, the relay transport refuses by name. Windows (credential storage is sealed with DPAPI but has run only under Wine), a real wide-area network, browser builds (where the service, relay and voice are absent) and avatar pixels on Direct3D and Metal are open, and no public server instance is operated. Offline leaderboards drop stream columns, and online sessions refuse guests.</p>` |
| 304 | `...which is built only on Linux and macOS (the optional split was not run on macOS by its author), so elsewhere it throws` | macOS trees built with Homebrew FFmpeg on the M4 (AM4-004, AM4-130). | `...the <code>Video</code> types exist in every build, but file-backed decoding needs the optional FFmpeg backend, which is built only on Linux and macOS, so elsewhere it throws <code>NotSupportedException</code>; on macOS a binary linked against Homebrew's FFmpeg starts only on the macOS that FFmpeg was built for. ...` (rest unchanged) |
| 321 | `<h3>CNA.NET on Windows, macOS and iOS <span class="status-badge status-planned">Future qualification</span></h3>` | macOS now has local evidence (R3 §3). | `<h3>CNA.NET on Windows and iOS, and on macOS beyond local evidence <span class="status-badge status-planned">Future qualification</span></h3>` |
| 322 | `...Windows and macOS have documented build steps but nothing has been run on them; iOS is planned through static linking.` | AM4-215..231 (osx-arm64 local); R2 §7 item 16; R3 §3.3. | `<p>CNA.NET&rsquo;s runtime qualification covers Linux x86_64, headless Chromium and the x86_64 Android emulator and, as local evidence on a physical Mac mini M4, macOS on Apple silicon (osx-arm64): its managed suites, package acceptance, the template and a smoke run of all 84 samples on <code>SOFTWARE</code> and <code>METAL</code>, without a CI leg, signing or notarization (its <code>SDL_RENDERER</code> integration suite is still open there). Windows has documented build steps but nothing has been run on it; iOS is planned through static linking. Interactive browsers, hardware GPUs in the browser, physical Android devices and a macOS CI leg are the next evidence to collect.</p>` |

CURRENT (keep): L113 SDL_GPU reaches Metal devices through shadercross, on by default on Apple (optionally add "and its full test suite passed on SDL's Metal driver on a Mac mini M4").

---

## 11. docs/roadmap.html

### docs/roadmap.html
Counts: STALE 9 · CURRENT 4 · OK-GENERIC 1  (12 regex hit lines + 2 extras: L180, L260)

Notes: not counted (policy (c)/(a), no Apple term): L179 "C ABI at 0.44.0" → 0.46.0; L225 "no CI workflow names WEBGPU (or OPENGLES2, ...)" (WEBGPU is named by the Emscripten bundle workflow at c1c316b9; OPENGLES2 is retired); L293 "468 unmapped symbols" (inconsistent with the page's own 656; c1c316b9 figure is 631, R3 §1). L250 (OK-GENERIC for "Apple") carries policy-(b) content (native X11 with no SDL, Wine-run Win32 harness) and job counts for the platform pass. L265 "macOS runtime validation is pending" for Diagnostics/Inspector stays true: `plan_apple_m4.md` records no Diagnostics or Inspector run.

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 180 (+extra) | `C# through CNA.NET ... (beta; qualified on Linux, in headless Chromium and on the x86_64 Android emulator)` | osx-arm64 local evidence (AM4-215..231; R3 §3). | `<li><strong>C# through CNA.NET</strong>: the C# binding over the C ABI exposes the <code>Microsoft.Xna.Framework</code> API and runs original XNA 4.0 C# source on CNA (beta; qualified on Linux, in headless Chromium and on the x86_64 Android emulator, with local osx-arm64 evidence from a physical Mac mini M4 and no macOS CI leg). See <a href="cna-net.html">C# with CNA.NET</a>.</li>` |
| 205 | `...eight opt-in build options cover the EasyGL family, Vulkan, WebGPU, Software, DirectX 9/11/12 and SDL_GPU. A default configure still reports the capability false on 17 of the 18 identities. Open: Metal has no compiled-effect implementation, and the 2D-only renderers cannot run them.` | AM4-144 (opt-in Metal route); policy (a). | `<td>Compiled D3D9 Effect Framework binaries (<code>.fxb</code>) now execute on nine implementation families (eleven identities): FNA3D is always on, and eight opt-in build options cover the EasyGL family, Vulkan, WebGPU, Software, DirectX 9/11, SDL_GPU and Metal. A default configure still reports the capability false on 13 of the 14 identities. Open: the 2D-only <code>SDL_RENDERER</code> cannot run them. HLSL <code>.fx</code> source is not accepted at run time; at build time <code>cna-content</code> compiles it through an external fxc-compatible compiler, a route CNA's own notes say has not been checked against a genuine Microsoft <code>fxc</code>. MGFX and raw DXBC remain unsupported inputs.</td>` |
| 210 | `...EasyGL, SDL_GPU, DirectX 11/12, WebGPU and Software cover subsets. Renderers without a format classifier (Metal, Headless, Stub, SDL_Renderer and Canvas) accept <code>Color</code> only` | Metal classifies formats (AM4-142/147/148; `MetalRenderer.mm:5216-5228`); policy (a). | `<td>Vulkan maps all 27 <code>SurfaceFormat</code> members against device format properties; EasyGL, SDL_GPU, DirectX 11, WebGPU, Metal and Software cover subsets. Renderers without a format classifier (Headless, Stub and SDL_Renderer) accept <code>Color</code> only, and anything else throws. A truthful per-renderer contract and configuration tests remain.</td>` |
| 228 | `<td><strong>Metal validation on macOS</strong></td>` | The validation happened (AM4-159); what remains is narrower. | `<td><strong>Metal beyond the Mac mini M4 runs</strong></td>` |
| 229 | `<td><span class="status-badge status-wip">Needs a Mac</span></td>` | AM4-159 verdict SUPPORTED, not primary-production. | `<td><span class="status-badge status-partial">Supported, not primary-production</span></td>` |
| 230 | `Declared Supported, but CNA's own Metal page says the adapted native source has no fresh macOS compile-and-run result. It is the most conservative 3D renderer (no MSAA, MRT, ...; <code>Color</code> surface format only)` | R2 §2.4, §6, §7. | `<td>Declared Supported, and since CNA's Mac mini M4 campaign measured on real hardware: MSAA, multiple render targets, occlusion queries, instancing, float, packed and DXT formats and SpriteBatch-scoped MSL custom effects are native, the full test suite and 261 Metal tests under the validation layers pass on that machine, and compiled XNA effects work behind <code>CNA_METAL_COMPILED_EFFECTS</code> (off by default). Open: on-screen presentation and <code>PresentInterval</code> pacing (the runs had a locked console), a physical iOS device, an Intel Mac, a soak run, compute and indirect draw, and a green hosted CI run.</td>` |
| 235 | `...exist and are qualified on Linux only. Open: Windows and macOS, a real wide-area network, ...` | M4 server suite 46/46 with Homebrew-curl harnesses, loopback; SDK libcurl refuses relay (AM4-044, 071, 123, 178; R2 §2.13, §5). | `<td>Local profiles, the Guide, avatars and the optional CNA Gamer Services server (accounts, social features, leaderboards, relayed PlayerMatch and Ranked sessions) exist and are qualified on Linux. On a physical Mac mini M4 the server's suite passes against CNA's client harnesses built with Homebrew's curl, on loopback only; with the SDK's libcurl, which has no WebSocket support, the relay transport refuses by name. Open: Windows, a real wide-area network, browser builds (where the service, relay and voice are absent), avatar pixels on Direct3D and Metal, offline leaderboard stream columns and online guests; achievements and scores are client claims without anti-cheat, and no public server instance is operated. See <a href="gamer-services.html">Gamer Services &amp; Avatars</a>.</td>` |
| 260 (+extra) | `656 public C++ symbols are still unmapped ... (441 more ...). No CNA CI job builds the C library, the consumer test and package machinery are verified on Linux only, ... CNA.NET pairs with exactly ABI 0.44.0` | R3 §1 (631/443, ABI 0.46.0); macOS installed-consumer and package checks (AM4-210..213). | `<td>631 public C++ symbols are still unmapped in the generated inventory (443 more are recorded as having no C form); that is the one unmet criterion the committed report records. No CNA CI job builds the C library; the consumer test and package machinery are verified on Linux and, by CNA's own run on a physical Mac mini M4, on macOS (a Mach-O <code>libcna_c_api.dylib</code> and a static archive, installed and consumed); ABI 1.0 is a separate future decision. The C# binding CNA.NET pairs with exactly ABI 0.46.0; the Common Lisp, Go, Java, Python, Ruby, Rust, Swift and TypeScript bindings are <a href="c-api.html#archived-bindings">archived</a> and will not follow new ABI versions. See <a href="c-api.html">Experimental C API</a>.</td>` |
| 290 | `Closing the named renderer gaps &mdash; Metal validation on a Mac, automatic coverage for ...` | Validation done (AM4-159); remaining Metal gaps R2 §7. | `<li>Closing the named renderer gaps &mdash; Metal's on-screen presentation, soak and physical-iOS evidence, automatic coverage for the Direct3D, WebGPU and SDL_GPU renderers, and per-renderer surface-format contracts.</li>` |

CURRENT (keep): L151 SDL_GPU reaches Metal through shadercross, on by default on Apple; L154 SDL_Renderer default on macOS/iOS; L240 FFmpeg never built for iOS; L265 Diagnostics/Inspector macOS runtime validation pending.
OK-GENERIC: L250 "Linux, Apple, Emscripten" in the CI inventory (policy-(b) parenthetical for the platform pass).

---

## 12. docs/faq.html

### docs/faq.html
Counts: STALE 5 · CURRENT 3 · OK-GENERIC 3  (10 regex hit lines + 1 extra: L150)

Notes: not counted, no Apple term: L162 (`cna-cs` repo name → W-NET rename worklist), L184 "pairs with exactly ... (0.44.0)" (policy (c) → 0.46.0). L250 (OK-GENERIC here) has policy-(a) content ("18 ... 14 families", "a browser canvas"); suggested wording for the renderer pass: `The 14 public renderer identities live in 12 implementation families, and the breadth is a statement about the abstraction rather than a promise that all 14 are equally complete. If a single <code>IGraphicsRenderer</code> interface can be satisfied by Direct3D 9, WebGPU, a CPU rasterizer, browser WebGL and Metal, then the interface is genuinely doing its job.` L304 (OK-GENERIC) has the Wine-executed Win32 lane (policy (b)).

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 150 (+extra) | `Its experimental native C ABI (version 0.44.0) is not built by CNA&rsquo;s CI ...; the C# binding CNA.NET builds and uses it on Linux.` | Policy (c); CNA.NET osx-arm64 local evidence (R3 §3). | `...Its experimental native C ABI (version 0.46.0) is not built by CNA&rsquo;s CI and its own release gate reports &ldquo;Not ready&rdquo;; the C# binding CNA.NET builds and uses it on Linux and, as local evidence on a physical Mac mini M4, on macOS.</p>` (snapshot sentence before it: global pass) |
| 234 | `Three renderers are Windows-only ... <code>METAL</code> is macOS-only. <code>WEBGL1</code>, <code>WEBGL2</code> and <code>CANVAS</code> are Emscripten-only. ... outside the 18 supported identities` | METAL macOS + iOS (AM4-037); policy (a). | `<li><strong>Platform gates are hard errors.</strong> Two renderers are Windows-only &mdash; <code>DIRECTX9</code> and <code>DIRECTX11</code>. <code>METAL</code> is limited to macOS and iOS. <code>WEBGL2</code> is Emscripten-only. Configuring the wrong one stops CMake with a <code>FATAL_ERROR</code>, and a name outside the 14 supported identities is a configure-time error too.</li>` |
| 273 | `Yes. macOS has the <code>METAL</code> renderer and, unusually for this project, <strong>real automatic CI</strong> &mdash; a <code>macos-14</code> runner ... (The optional-video split itself was not run on macOS by its author.)` | M4 qualification (AM4-208); macos-26 (AM4-255); no green post-campaign run (R2 §2.16); FFmpeg floor (AM4-130); relay needs Homebrew curl (AM4-044); METAL verdict (AM4-159). | `<p>Yes. CNA's own qualification on a physical Mac mini M4 (Apple silicon, macOS 27) ran the full test suite of every renderer that applies to macOS &mdash; <code>METAL</code>, <code>OPENGL33</code>, <code>SDL_GPU</code>, <code>WEBGPU</code>, <code>FNA3D</code>, <code>SOFTWARE</code> and <code>SDL_RENDERER</code> &mdash; with no failing case, although on-screen presentation was not observed (the console was locked) and no Intel Mac was run. macOS also has automatic CI: a <code>macos-26</code> runner builds and tests the <code>SDL_RENDERER</code> configuration and launches a self-contained app bundle, and a separate workflow builds <code>METAL</code> and runs its tests; no green hosted run is recorded after the campaign. The native <code>METAL</code> renderer is supported but not primary-production, and compiles XNA effects only with <code>CNA_METAL_COMPILED_EFFECTS=ON</code>. FFmpeg is an <em>optional</em> dependency on macOS: with <code>CNA_ENABLE_VIDEO=AUTO</code> (the default) video decoding is enabled when the <code>libavcodec</code>/<code>libavformat</code>/<code>libavutil</code>/<code>libswresample</code> development packages are found (for example through Homebrew), and otherwise <code>Video</code> playback throws <code>NotSupportedException</code> at run time; a binary linked against Homebrew's FFmpeg starts only on the macOS that FFmpeg was built for. Online play needs a libcurl with WebSocket support, such as Homebrew's curl: with the SDK's libcurl the relay transport refuses by name.</p>` |
| 274 | `This snapshot also has a <strong>narrow experimental iOS path</strong>, restricted to <code>SDL_RENDERER</code>. CI final-links a device application and launches a one-frame simulator smoke test; it does not establish physical-device, pixel, ...` | METAL allowed (AM4-037); Simulator pixel probe 8/8 (AM4-120); NET off (AM4-105); R2 §8 (no "iOS has no pixel evidence"). | `<p>This snapshot also has an <strong>experimental iOS path</strong> with two allowed renderers, <code>SDL_RENDERER</code> and the native <code>METAL</code>. CI final-links device applications and launches simulator smoke tests, and in CNA's own iOS Simulator runs (iPhone 17 profile) a <code>METAL</code> pixel probe read back exact pixels in 8 of 8 launches. No physical iPhone or iPad has run it, so device pixels, input, audio, storage and performance are not established, and networking must be configured off. tvOS remains unsupported.</p>` |
| 410 | `Where <code>ShaderEffect</code> source actually executes: the five GL-profile renderers (GLSL), <code>WEBGPU</code> (WGSL), and <code>DIRECTX11</code> and <code>DIRECTX12</code> (HLSL); ... <code>FNA3D</code> and the two 2D-only renderers report no custom-effect capability, and <code>METAL</code> throws.` | Metal SpriteBatch-scoped MSL (AM4-077; `metal-shader-effect-contract.md`: `ExecutesShaderEffectSourceEXT()` stays false on Metal); policy (a). | `<p>Where <code>ShaderEffect</code> source actually executes: the three GL-profile renderers (GLSL), <code>WEBGPU</code> (WGSL), <code>DIRECTX11</code> (HLSL) and <code>METAL</code> (MSL, for <code>SpriteBatch</code> only); <code>DIRECTX9</code> also compiles HLSL. <code>VULKAN</code> takes SPIR-V words rather than GLSL text, and <code>SDL_GPU</code> supports the path only in builds that found <code>libshaderc</code> (GLSL) or with SPIR-V. <code>HEADLESS</code> records them without drawing. <strong><code>SOFTWARE</code> accepts the source and silently never executes it</strong>, which is the failure mode most likely to waste your afternoon. <code>FNA3D</code> and the 2D-only <code>SDL_RENDERER</code> report no custom-effect capability. Query <code>GraphicsDevice::ExecutesShaderEffectSourceEXT()</code> and the <code>RendererCapabilityProfile</code> rather than guessing (on <code>METAL</code> the first stays false, because it concerns the GLSL that CNAEXT writes; <code>GetShaderDialectEXT()</code> reports MSL there). See <a href="shader-effects.html">Shader Effects</a>.</p>` |

CURRENT (keep): L349 FFmpeg optional on Linux and macOS; L420 save root `~/Library/Application Support` on macOS (matches `apple-platforms.md:295-299`); L454 sensors probed on desktop macOS.
OK-GENERIC: L250 Metal in the abstraction sentence (see note); L269 question "Can I use CNA on macOS?"; L304 "Apple" in the CI inventory.

---

## 13. index.html

### index.html
Counts: STALE 2 · CURRENT 0 · OK-GENERIC 3  (4 regex hit lines + 1 extra: L135 title attr)

Notes: not counted (no Apple term; global passes): meta/og description L7/L13 and JSON-LD L37 ("18 renderer identities"), L108 "C ABI (0.44.0, opt-in build)", L146 snapshot paragraph (0.44.0, native X11/Wayland/Win32), L415 CNA.NET card ("admits exactly C ABI 0.44.0", `cna-cs-*` repos → W-NET). L180 and L264 (OK-GENERIC for Metal) list retired identities — renderer pass. L39 JSON-LD `operatingSystem` "Linux, Windows, macOS, iOS, Android, WebAssembly" stays.

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 135 (+extra, title attr) | `title="cna-cs-samples @ 1e6d763 (2026-10-04): 83 Microsoft XNA 4.0 sample projects (84 programs) built from byte-identical upstream C# source run on CNA.NET on Linux, in headless Chromium and on the x86_64 Android emulator. Recorded in the CNA.NET campaign ledgers, not CI."` | The 84 programs were also smoke-run on macOS osx-arm64 on SOFTWARE and METAL (AM4-228; R3 §3.2, §4: smoke-run, not pixel-verified); repo renamed `cna-dotnet-samples` (R3 §3.1). | `title="cna-dotnet-samples @ 1e6d763 (2026-10-04): 83 Microsoft XNA 4.0 sample projects (84 programs) built from byte-identical upstream C# source run on CNA.NET on Linux, in headless Chromium and on the x86_64 Android emulator; on a physical Mac mini M4 (osx-arm64) all 84 start, load content and keep running on the SOFTWARE and METAL renderers (a smoke run, not a pixel check). Recorded in the CNA.NET campaign ledgers, not CI."` |
| 192 | `...macOS has a native Metal workflow lane (configured, not verified as passing). ... iOS is experimental and narrowly scoped to <code>SDL_RENDERER</code>: CI final-links a device app and launches a simulator smoke frame, but does not establish physical-device or pixel correctness.` | R2 §2.1, §3, §6 (AM4-208, AM4-037, AM4-120); same paragraph has policy (a) (Direct3D 12, WebGL 1, Canvas) and (b) (native X11/Wayland, Win32 backend). | `<p>Linux is the primary development host (SDL3 on X11 or Wayland); Windows has Direct3D 9 and 11 renderers whose Windows CI lanes are manual; the browser is a real CNA platform through Emscripten, with WebGL 2 and experimental WebGPU identities &mdash; see the 90 <a href="https://samples.libcna.com/" target="_blank" rel="noopener">playable sample builds</a>; macOS was qualified on a physical Mac mini M4, where every renderer that applies there, the native Metal one included, passed its full test suite (on-screen presentation was not observed, and no green hosted CI run is recorded since). Android has NDK/source integration without an automatic gate; real games and samples have been run on the Android emulator. iOS is experimental, with <code>SDL_RENDERER</code> and <code>METAL</code> allowed: in the iOS Simulator a <code>METAL</code> pixel probe reads back exact pixels, while the device build is final-linked and has not run on a physical iPhone or iPad.</p>` |

OK-GENERIC: L39 JSON-LD operatingSystem; L180 renderer list naming Metal; L264 renderer list naming Metal.

---

## 14. architecture.html

### architecture.html
Counts: STALE 4 · CURRENT 4 · OK-GENERIC 3  (11 regex hit lines)

Notes: L112 (diagram, OK-GENERIC for METAL) and the bullets L213-218 carry policy-(a)/(b) content (retired identities in the diagram; native X11/Wayland/Win32 windows, GLX/WGL) — renderer/platform passes.

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 219 | `<strong>Native surface creation</strong> — used by the WEBGPU renderer and the Direct3D and Metal families (Win32/Metal/X11/Wayland surfaces built from the platform's native window handle, ...)` | The Metal family now also takes a `UIWindow*` on iOS (AM4-037; `metal-renderer.md:5-10`); the handles come from SDL3, not direct platforms (policy (b)). | `<li><strong>Native surface creation</strong> — used by the WEBGPU renderer and the Direct3D and Metal families (surfaces built from the native window handle the platform reports: a Win32, X11 or Wayland window, an <code>NSWindow</code> on macOS or a <code>UIWindow</code> on iOS; no separate compatibility library needed)</li>` |
| 299 | `identities from different platform partitions &mdash; Windows-only, Emscripten-only, macOS-only &mdash; cannot mix` | METAL is Apple-only (macOS + iOS). | `<p>A multi-renderer build is checked at configure time: identities from different platform partitions &mdash; Windows-only, Emscripten-only, Apple-only &mdash; cannot mix, because one toolchain cannot target both. See <a href="docs/runtime-renderer-selection.html">Runtime renderer selection</a>.</p>` |
| 387 | `<td>Anywhere SDL3 runs (default elsewhere; the only renderer on iOS)</td>` | iOS allow-list has METAL too. | `<td>Anywhere SDL3 runs (default elsewhere; one of the two renderers allowed on iOS)</td>` |
| 395 | `<tr><td><code>METAL</code></td><td>Native macOS</td><td>2D + 3D</td><td>macOS only</td></tr>` | AM4-037. | `<tr><td><code>METAL</code></td><td>Native Apple GPU access on macOS and, experimentally, iOS</td><td>2D + 3D</td><td>macOS and iOS</td></tr>` |

CURRENT (keep): L168 target OS list incl. macOS and iOS; L324 Inspector refused on iOS (and the C ABI needing `CNA_ENABLE_NET=ON` — `CMakeLists.txt:187-192` — while iOS needs `CNA_ENABLE_NET=OFF`, so the C ABI cannot be configured for iOS today); L389 SDL_GPU Metal devices via shadercross; L390 WEBGPU on macOS through wgpu-native.
OK-GENERIC: L112 diagram cell "METAL · WEBGPU"; L275 window kind "Metal"; L520 source tree `metal/`.

---

## 15. about.html

### about.html
Counts: STALE 2 · CURRENT 2 · OK-GENERIC 2  (6 regex hit lines)

Notes: L75 (OK-GENERIC for "Apple/Metal") and L101 (OK-GENERIC for "Metal" in the renderer list) carry policy-(a)/(b) content (18 identities, native X11, Win32-platform workflow; Direct3D 12, WebGL/Canvas) for the global passes.

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 93 | `This snapshot contains Linux, Windows, macOS, Emscripten and Android build paths &mdash; served by the SDL3 platform layer and by native X11, Wayland and Win32 layers &mdash; plus narrow experimental iOS SDL_RENDERER final-link and simulator-smoke evidence.` | macOS full-suite runs on the M4 (AM4-208); iOS METAL + Simulator pixel probe (AM4-037, AM4-120); policy (b). | `<li><strong>Portability:</strong> host integration, audio, graphics rendering and target OS are separate axes. This snapshot contains Linux, Windows, macOS, Emscripten and Android build paths, all served by the SDL3 platform layer (with headless and terminal implementations beside it); macOS has been run in full on a physical Mac mini M4, and iOS is experimental, with Simulator pixel evidence for the native Metal renderer and a device build that is final-linked but not run. See <a href="docs/platforms.html">Platforms</a> and <a href="docs/native-platforms.html">Native Platforms</a> for what is tested where.</li>` |
| 132 | `macOS/Metal has automatic CI (a build plus the Metal tests, a narrower contract than "it builds"), while iOS is experimental and limited to SDL_RENDERER final-link plus a one-frame simulator smoke path; tvOS is unsupported. Native Wayland and Android have no CI lane ...` | R2 §2.1, §2.16, §3, §6, §7; policy (b) (native Wayland). | `<li>CNA's platform claims are scoped: macOS was qualified on a physical Mac mini M4, where every renderer that applies there passed its full test suite (on-screen presentation not observed, no Intel Mac run), and its automatic CI builds and tests the platform layer and runs the Metal tests on a paravirtual GPU, with no green run recorded since; iOS is experimental, with <code>SDL_RENDERER</code> and <code>METAL</code> allowed and Simulator-only evidence; tvOS is unsupported. Android has no CI lane in this snapshot, and the Windows Direct3D lanes are manual.</li>` |

CURRENT (keep): L158 "current AppleClang" in CI; L164 FFmpeg on Linux and macOS, never iOS.
OK-GENERIC: L75 "Apple/Metal" in the workflow summary; L101 "Metal" in the renderer list.

---

## 16. showcase.html

### showcase.html
Counts: STALE 6 · CURRENT 0 · OK-GENERIC 3  (6 regex hit lines + 3 extras: L334, L394, L399)

Section note (Platform Validation table, macOS and iOS rows L391-402): the rows still say "configured lanes ... pin an older sharp-runtime" and "allow-listed to SDL_RENDERER only". New content: macOS = every applicable renderer run in full on one Mac mini M4, sample ports measured per renderer (cna-samples Release multi-renderer matrix: METAL/OPENGL33/WEBGPU 91/91, SDL_GPU/FNA3D 90/91 — LensFlare needs occlusion queries; 248/248 cna-examples demos render on Metal; R2 §5, M4-LOCKED/M4-LOCAL); iOS = METAL + SDL_RENDERER, Simulator pixel probe, device build not run. The Web row (L383) also has a sharp-runtime pin caveat that is now obsolete (AM4-234) — not counted here (no Apple term).

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 334 (+extra) | `83 sample projects (84 programs) build and run on Linux, single-threaded in headless Chromium and on the x86_64 Android emulator;` | AM4-228: all 84 smoke-run on osx-arm64 on SOFTWARE and METAL (start, load content, run to a 15 s alarm; not a pixel check) (R3 §3.2, §4). Repo name `cna-cs-samples` → W-NET. | `...83 sample projects (84 programs) build and run on Linux, single-threaded in headless Chromium and on the x86_64 Android emulator, and on a physical Mac mini M4 (osx-arm64) all 84 start, load their content and keep running on the <code>SOFTWARE</code> and <code>METAL</code> renderers (a smoke run, not a pixel comparison); 83 of the 91 C++ ports therefore also exist as unchanged C#, and 26 programs were compared pixel for pixel with their C++ port and match.</p>` |
| 393 | `<td><code>SDL_RENDERER</code>, <code>METAL</code></td>` | All seven applicable renderers ran in full on the M4 (AM4-208). | `<td><code>METAL</code>, <code>OPENGL33</code>, <code>SDL_GPU</code>, <code>WEBGPU</code>, <code>FNA3D</code>, <code>SOFTWARE</code>, <code>SDL_RENDERER</code></td>` |
| 394 (+extra) | `<td><span class="status-badge status-partial">Partial</span></td>` (macOS) | "Partial" understates a full local qualification; keep a non-"Validated" badge because there is one machine, no observed presentation and no green CI. | `<td><span class="status-badge status-partial">Tested on one Mac</span></td>` |
| 395 | `macOS 13.3 and later: an automatic macOS workflow builds ... Those workflows pin an older sharp-runtime revision ..., so read them as configured lanes, not as evidence of a passing build; Metal's contract is the narrowest of the 3D renderers.` | AM4-208, AM4-169/182 (cna-samples), cna-examples 248/248, AM4-234, AM4-255, AM4-159; R2 §5. | `<td>macOS 13.3 and later. CNA's own qualification ran every renderer listed here through its full test suite on a physical Mac mini M4 (Apple silicon, macOS 27) with no failing case; the console was locked, so on-screen presentation was not observed, and no Intel Mac was run. The C++ sample ports pass CNA's automated renderer matrix on <code>METAL</code>, <code>OPENGL33</code> and <code>WEBGPU</code> (91 of 91) and on <code>SDL_GPU</code> and <code>FNA3D</code> (90 of 91; LensFlare needs occlusion queries), and 248 cna-examples demos render on Metal. Automatic workflows on <code>macos-26</code> build the portable suites, launch a self-contained app bundle and run the Metal tests on a paravirtual GPU; no green run is recorded after the campaign. The native Metal renderer is supported but not primary-production (compiled effects are opt-in).</td>` |
| 399 (+extra) | `<td><code>SDL_RENDERER</code></td>` (iOS renderers) | METAL allowed on iOS (AM4-037). | `<td><code>SDL_RENDERER</code>, <code>METAL</code></td>` |
| 401 | `iOS 16.3 and later, allow-listed to <code>SDL_RENDERER</code> only. CI final-links a device app and launches a one-frame simulator smoke app; there is no physical-device, pixel, input or audio evidence.` | AM4-037, AM4-105, AM4-120; R2 §8. | `<td>iOS 16.3 and later, allow-listed to <code>SDL_RENDERER</code> and <code>METAL</code>. In CNA's own iOS Simulator runs (iOS 27, iPhone 17 profile) a <code>METAL</code> pixel probe read back exact pixels in 8 of 8 launches; the device app is final-linked and has never run on a physical iPhone or iPad, so there is no device pixel, input or audio evidence. Networking must be configured off.</td>` |

OK-GENERIC: L106 "Apple/Metal" in the workflow note; L392 row label "macOS"; L398 row label "iOS".

---

## 17. docs/native-platforms.html

### docs/native-platforms.html
Counts: STALE 5 · CURRENT 3 · OK-GENERIC 0  (8 regex hit lines)

Section note: the whole page documents the X11/WAYLAND/WIN32 platform implementations, which do not exist at c1c316b9 (`CNA_PLATFORM` = `SDL3 | HEADLESS | TERMINAL`, `cmake/PlatformSelection.cmake:24-32`), so it needs the platform pass (rewrite or retarget). Four of its five STALE Apple hits are policy-(b) lines whose Apple mention is incidental. Apple facts worth carrying into whatever replaces it: SDL3 is the only platform any CI job configures on macOS and iOS (through SDL's Cocoa and UIKit drivers; CNA has no Cocoa/AppKit/UIKit backend, R2 §1); `managedEntrypoint` is true on SDL3 for iOS and Android; there is no SDL-free audio on macOS; METAL is gated to macOS and iOS.

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 137 | `The <code>next</code> branch adds <strong>three native platform backends</strong> ... <code>X11</code> ..., <code>WAYLAND</code> ... and <code>WIN32</code> ... SDL3 is still the default, and the only platform CI configures, on macOS, iOS, Android and the web` | Policy (b); Apple part current. | `<p><strong>Platform implementations in this snapshot.</strong> <code>CNA_PLATFORM</code> selects <code>SDL3</code> (the default and the only graphical implementation), <code>HEADLESS</code> or <code>TERMINAL</code> (POSIX-only). Windows, X11, Wayland, macOS (Cocoa), iOS (UIKit), Android and the browser are all reached through SDL3's video drivers, and SDL3 is the only platform any CI job configures on macOS, iOS, Android and the web. The other axes (<a href="platforms.html#four-axes">target OS, renderer, audio</a>) stay independent.</p>` |
| 147 | X11 row: `...the target is not Windows, Emscripten, Android or iOS` | Policy (b) (no X11 platform value). | Delete the row (platform pass). |
| 148 | WAYLAND row: `...not Windows, Emscripten, Android or Apple` | Policy (b). | Delete the row (platform pass). |
| 371 | `<code>METAL</code>, <code>WEBGL1</code>, <code>WEBGL2</code>, <code>CANVAS</code> ... Platform-gated to macOS or Emscripten; not offered on these targets.` | METAL is macOS + iOS (AM4-037); policy (a); the table's X11/Wayland/Win32 columns are policy (b). | If the table survives the platform pass: `<tr><th scope="row"><code>METAL</code>, <code>WEBGL2</code></th><td colspan="3">Platform-gated to macOS and iOS (<code>METAL</code>) or to Emscripten (<code>WEBGL2</code>).</td></tr>`; otherwise drop with the table. |
| 491 | `...native Wayland is not offered on macOS, iOS, Android or the web, and native X11 is not offered on iOS, Android or the web (on macOS it is offered whenever libX11, libXext and <code>XKBlib.h</code> are found; not exercised).` | Policy (b): no native X11 on macOS (or anywhere). | Delete the bullet (platform pass). |

CURRENT (keep, for the rewrite): L165 SDL3 the default and only CI-configured platform on macOS/iOS; L309 `managedEntrypoint` "Yes (Android and iOS main)"; L489 no SDL-free audio on Windows or macOS.

---

## 18. deep-dives/reference/verification-tiers.html

### deep-dives/reference/verification-tiers.html
Counts: STALE 2 · CURRENT 4 · OK-GENERIC 0  (6 regex hit lines)

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 245 | `...one <code>WEBGL2</code>, <code>WEBGL1</code> and <code>CANVAS</code> bundle links (but it, <code>devices-tests.yml</code> and the Apple and Metal workflows pin a sharp-runtime revision that lacks a component ... CNA-BUG-199)` | Pins replaced (AM4-234; all four workflows use `sibling_branch.sh` at c1c316b9); policy (a): bundle is `WEBGL2;WEBGPU`. | `<li><strong>Browsers and runtime selection.</strong> No workflow runs a renderer in a real browser. The Emscripten multi-renderer job is designed to prove that one <code>WEBGL2</code> and <code>WEBGPU</code> bundle links and carries both renderers and the JavaScript selection surface, and the native multi-renderer job proves descriptor generation and early runtime selection for a CPU and diagnostic set; neither proves every renderer's pixels.</li>` |
| 247 | `The macOS workflows build and run portable suites and the native Metal contract tests with <code>MTL_DEBUG_LAYER</code> and <code>MTL_SHADER_VALIDATION</code> set; they do not imply iOS or tvOS devices or every GPU.` | Hosted GPU is paravirtual: shader validation off, `--parallel 1` (AM4-279, AM4-283, AM4-306); M4 local tier and Simulator tier missing (R2 §2.1, §3). | `<li><strong>Apple and Windows.</strong> The macOS workflows build and run portable suites and the native Metal tests on <code>macos-26</code> runners, whose GPU is an &ldquo;Apple Paravirtual device&rdquo;: there the Metal tests run with <code>MTL_DEBUG_LAYER</code> only, because that device cannot run shader validation, and no green run is recorded after the Mac mini M4 campaign. CNA's own runs on a physical Mac mini M4 (full test suites, Metal tests under both validation layers, console locked) and in the iOS Simulator are a separate, local tier; none of these implies an iOS or tvOS device, an Intel Mac or every GPU. The Direct3D workflow is manual. Native MSVC, MinGW under Wine with DXVK, WARP, and a physical interactive Windows machine remain different evidence tiers (see <a href="../renderers/direct3d-evidence-and-wine.html#evidence-ladder">Direct3D: what each tier proves</a>).</li>` |

CURRENT (keep): L226 iOS simulator launch vs signed physical-device build (optionally add "and, for <code>METAL</code>, a Simulator pixel probe"); L233 `apple-ci.yml` has 3 jobs (still `apple-cmake-check`, `macos-build`, `ios` matrix at c1c316b9; the `platform-ci.yml` count is a platform-pass item); L252 Inspector macOS runtime validation pending (no Inspector run in `plan_apple_m4.md`); L257 Metal's validation variables as a family-specific GPU validation.

---

## 19. deep-dives/platforms/index.html

### deep-dives/platforms/index.html
Counts: STALE 1 · CURRENT 0 · OK-GENERIC 5  (6 regex hit lines)

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 123 | `...how assets and saves are found on a device, and what the macOS and iOS workflows check.</li>` | Mirrors the deep dive's new description (§1 L7). | `<li><a href="android-and-apple-platforms.html"><strong>Android and Apple targets: structure, lifecycle, assets and evidence</strong></a> &mdash; How CNA&#x27;s Android application and NDK code are structured, how Game handles mobile lifecycle events, how assets and saves are found on a device, and what the Mac mini M4 qualification, the iOS Simulator probe and the Apple workflows show.</li>` |

OK-GENERIC: L7 meta description, L13 og:description, L19 JSON-LD description ("Android and Apple platforms"), L89 sidebar link, L117 lede.

---

## 20. docs/getting-started.html

### docs/getting-started.html
Counts: STALE 3 · CURRENT 0 · OK-GENERIC 2  (5 regex hit lines)

Notes: two prerequisites the campaign established for any macOS build are missing from the macOS list: Xcode 15.4 (the old `macos-14` default) is too old, because its libc++ lacks `std::jthread`/`std::stop_token`, which gamer services use (AM4-255, workflow comment); and `nlohmann_json` 3.11+ is a hard `find_package(... REQUIRED)` for the networking/Gamer Services build (`cmake/HeaderOnlyJson.cmake`; AM4-247: Homebrew `nlohmann-json`). The replacements for L173-174 add them. Not counted: L157 and L168 (retired identities, "Windows-only renderers (5)") and L370 "the six platform implementations" — renderer/platform passes.

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 173 | `CMake 3.20 or newer and a current Xcode / AppleClang (CI uses <code>macos-14</code>); deployment floor macOS 13.3` | Runners moved to `macos-26` because macos-14's Xcode 15.4 cannot build CNA (AM4-255); M4 toolchain Xcode 27 (R2 §1). | `<li>CMake 3.20 or newer and a current Xcode / AppleClang: CI uses <code>macos-26</code> (Xcode 26), CNA's own Mac mini M4 qualification used Xcode 27, and Xcode 15.4 is too old (its libc++ lacks <code>std::jthread</code>, which the Gamer Services code uses); deployment floor macOS 13.3</li>` |
| 174 | `...<code>SDL_RENDERER</code> is the default renderer (<code>METAL</code> is macOS-only)` | METAL macOS + iOS (AM4-037); M4 qualification (AM4-208); nlohmann-json (AM4-247); relay needs Homebrew curl (AM4-044). | `<li><code>../sharp-runtime</code> sibling (<code>next</code> branch); SDL3 from the vendored submodules; <code>SDL_RENDERER</code> is the default renderer, and <code>METAL</code> (CNA's native Metal renderer, macOS and iOS), <code>OPENGL33</code>, <code>SDL_GPU</code>, <code>WEBGPU</code>, <code>FNA3D</code> and <code>SOFTWARE</code> have each passed their full test suite on a physical Mac mini M4</li><li><code>nlohmann-json</code> 3.11 or newer (for example <code>brew install nlohmann-json</code>) for the networking and Gamer Services modules; online play additionally needs a libcurl with WebSocket support, such as Homebrew's <code>curl</code>, because the SDK's libcurl has none and the relay transport then refuses by name</li>` |
| 183 | `CI's workflows use GCC 14, AppleClang (macos-14), MSVC (windows-latest), mingw-w64 GCC and Emscripten 6.0.3` | `macos-26` (AM4-255). | `<tr><td>Compiler</td><td>A C++23 compiler. CI's workflows use GCC 14, AppleClang (Xcode 26 on <code>macos-26</code>), MSVC (windows-latest), mingw-w64 GCC and Emscripten 6.0.3; the CMake files enforce no compiler version</td></tr>` |

OK-GENERIC: L171 h3 "macOS"; L370 "Linux, Windows, macOS, Android, iOS, web" link description (its "six platform implementations" is a platform-pass item).

---

## 21. tutorials.html

### tutorials.html
Counts: STALE 0 · CURRENT 0 · OK-GENERIC 4  (4 regex hit lines)

Nothing to change for Apple: L327 JSON-LD ListItem "Metal on macOS", L1224/L1226 the Tutorial 109 card and title, L458 "⌘+F on macOS". The tutorial keeps its title (it remains the macOS chapter; iOS is covered inside it per §3). No description text for Tutorial 109 appears on this page.

---

## 22. documentation.html

### documentation.html
Counts: STALE 0 · CURRENT 1 · OK-GENERIC 2  (3 regex hit lines)

CURRENT (keep): L276 optional FFmpeg backend on Linux and macOS.
OK-GENERIC: L90 "Linux, Windows, macOS and Emscripten" build instructions; L116 renderer list naming Metal (its "18 selectable renderers", Direct3D 12 and Canvas are renderer-pass items).

---

## Summary

| Page | STALE | CURRENT | OK-GENERIC | regex hit lines + extras |
|---|---:|---:|---:|---|
| deep-dives/platforms/android-and-apple-platforms.html | 14 | 6 | 9 | 29 + 0 |
| docs/platforms.html | 28 | 6 | 13 | 43 + 4 |
| docs/tutorials/109-metal-macos.html | 53 | 12 | 11 | 54 + 22 |
| docs/rendering-backends.html | 23 | 11 | 3 | 33 + 4 |
| docs/building.html | 9 | 24 | 7 | 38 + 2 |
| features.html | 20 | 10 | 3 | 28 + 5 |
| deep-dives/renderers/native-gpu-evidence-tiers.html | 9 | 2 | 6 | 16 + 1 |
| deep-dives/platforms/cross-platform-contract.html | 7 | 3 | 4 | 14 + 0 |
| docs/verification.html | 7 | 2 | 2 | 8 + 3 |
| roadmap.html | 12 | 1 | 0 | 10 + 3 |
| docs/roadmap.html | 9 | 4 | 1 | 12 + 2 |
| docs/faq.html | 5 | 3 | 3 | 10 + 1 |
| index.html | 2 | 0 | 3 | 4 + 1 |
| architecture.html | 4 | 4 | 3 | 11 + 0 |
| about.html | 2 | 2 | 2 | 6 + 0 |
| showcase.html | 6 | 0 | 3 | 6 + 3 |
| docs/native-platforms.html | 5 | 3 | 0 | 8 + 0 |
| deep-dives/reference/verification-tiers.html | 2 | 4 | 0 | 6 + 0 |
| deep-dives/platforms/index.html | 1 | 0 | 5 | 6 + 0 |
| docs/getting-started.html | 3 | 0 | 2 | 5 + 0 |
| tutorials.html | 0 | 0 | 4 | 4 + 0 |
| documentation.html | 0 | 1 | 2 | 3 + 0 |
| **Total** | **221** | **98** | **86** | **354 + 51 = 405** |

Cross-page items found while surveying (outside the 22 pages; for the lead):
- `known-issues/bugs/cna-bug-199.html` (stale sharp-runtime pins) is fixed at c1c316b9 by AM4-234 — every workflow uses `scripts/ci/sibling_branch.sh` or `clone_siblings.sh`.
- `known-issues/verification-gaps/cna-vgap-008.html` ("one iOS simulator frame") needs the Simulator pixel-probe evidence (AM4-120).
- `known-issues/bugs/cna-bug-099.html` (Linux/RADV `^SdlGpu` failures) should be re-checked against the SDL_GPU full tree on the M4 (Metal driver, no failure) and AM4-092/181/183/184; do not assume it is fixed on Linux.
- `known-issues/bugs/cna-bug-192.html` (metal-macos-ci push filter) is still valid at c1c316b9.
- CNA-internal inconsistencies not to copy: `cmake/RendererCombinations.cmake:25,50-51` labels METAL's partition "macOS"; `docs/metal-renderer.md:83` still says MSAA capability false; `docs/apple-platforms.md:9-10, 171, 314` and `README.md` keep pre-campaign wording (R2 §2.16, §3).

---

# Part 2 — C API and CNA.NET pages (C API on macOS, ABI 0.46.0, the cna-dotnet rename)

Facts: `R3-c-api-cna-net.md`. Encoded 0.46.0 = **`0x00002E00`** (11776); 0.44.0 was `0x00002C00` (11264). Gate numbers at TARGET: **631** unmapped
("planned"), **7,053** implemented, 15 partial, **443** not applicable, **451** excluded headers; **1,463** integer constants; 3,210 exports; 197 structs; 295 scalars; 60 headers.
Snapshot identifiers (`b0e97bb1`, "4 October 2026") on these pages are assumed to be swapped globally by the lead; rows below only mention them where the sentence
must change anyway.

## docs/c-api.html
Counts: STALE 27 · CURRENT 6 · OK-GENERIC 3 (Apple-term hits: 4; the rest are ABI/gate/rename items on the same page)

| Line | Current text (excerpt) | Why stale | Proposed replacement |
|---|---|---|---|
| 9 (JSON-LD description) | "Source-level guide to the experimental CNA C ABI 0.44.0 at snapshot b0e97bb1 …" | ABI is 0.46.0 (`abi.h:37`); C API now built/tested on macOS (R3 §2) | "Guide to the experimental CNA C ABI 0.46.0 at snapshot c1c316b9: build and package design (Linux/ELF and macOS/Mach-O), ABI policy, release gate status, threading rules, and the maintained (C, C#) and archived (…) language bindings." |
| 62 (doc-meta) | "declared C ABI 0.44.0 · source present, gated, not built by any CNA CI workflow" | 0.46.0; CNA's own records now include local builds on Linux and on a physical Mac mini M4 | "declared C ABI 0.46.0 · built and tested locally (Linux; macOS on a physical Mac mini M4), not built by any CNA CI workflow" |
| 64 (warn callout) | "…built and used <code>libcna_c_api</code> on Linux from a CNA commit whose source is identical to this snapshot. … with 656 public C++ symbols still unmapped." | 656 → 631 (`RELEASE_GATE.md`); add the macOS M4 evidence (AM4-209..213) | "…No CNA CI workflow builds the C library. Run evidence comes from CNA's own local records: the <a href="cna-net.html">CNA.NET</a> campaign built and used <code>libcna_c_api</code> on Linux, and CNA's Apple campaign built the shared and static library on a physical Mac mini M4 and ran every C API test there (119/119 in the SOFTWARE and SDL_RENDERER configurations). CNA's own release gate for the C ABI says <strong>“Not ready”</strong>, with 631 public C++ symbols still unmapped. Unless a sentence says otherwise, what follows was read from source, not built by us." |
| 69 | "<code>0.44.0</code> (encoded <code>0x00002C00</code>)" | `abi.h` 0.46.0 | "<code>0.46.0</code> (encoded <code>0x00002E00</code>)" |
| 72 | "197 struct layouts, 295 scalar types, 1,466 integer constants, …, 3,210 exports" | baseline at TARGET has 1,463 integer constants (`abi_baseline.json`) | "197 struct layouts, 295 scalar types, 1,463 integer constants, 14 string constants, 141 colour constants, 3,210 exports (<code>tools/c-api/abi_baseline.json</code>; checked against the built Mach-O library on arm64 macOS by AM4-212)" |
| 74 | "the unmet one is 656 unmapped public symbols" | 631 | "…the unmet one is 631 unmapped public symbols (not re-run for this page)" |
| 89 | "…Windows and macOS shared-library builds have not been run." | macOS shared + static built and tested on a physical Mac mini M4 (AM4-209..213; `apple-platforms.md:218`) | "…Android (NDK) and Emscripten builds of the library are used by CNA.NET's Android-emulator and headless-Chromium hosts. On macOS (Apple silicon) CNA's own campaign built the library as a Mach-O dylib and static archive on a physical Mac mini M4 and ran every C API test (119/119, SOFTWARE and SDL_RENDERER configurations), including the installed-package consumer; no CI job does this. Windows shared-library builds have not been run." |
| 97 | "Optional static archive, default ON on Linux-like hosts with Python 3: … (except GCC's STB_GNU_UNIQUE symbols)" | Darwin now builds it with `ld -r -all_load` + `nmedit -s` (`modules/c-api/CMakeLists.txt:358-362`, AM4-213) | "Optional static archive, default ON on Linux and macOS hosts with Python 3: the whole closure is partially linked into one relocatable object (<code>ld -r</code>; ld64's <code>ld -r -all_load</code> on macOS), every non-<code>cna_*</code> symbol is localized (<code>objcopy</code>; <code>nmedit -s</code> on macOS), and the build fails if any survives (except GCC's <code>STB_GNU_UNIQUE</code> symbols on ELF). …" (keep the rest) |
| 98 | "…the SDL3 libraries CNA builds (installed beside the library; INSTALL_RPATH is $ORIGIN, so no LD_LIBRARY_PATH is needed)…" | macOS: `@loader_path`, `libSDL3*.dylib` installed, Mach-O versions (AM4-210) | "…the SDL3 libraries CNA builds (installed beside the library; its run path is <code>$ORIGIN</code> on Linux and <code>@loader_path</code> on macOS, so neither <code>LD_LIBRARY_PATH</code> nor a <code>DYLD_*</code> variable is needed), …" ; add: "On macOS the library is <code>libcna_c_api.dylib</code> with install name <code>@rpath/libcna_c_api.dylib</code> and Mach-O compatibility/current version taken from the ABI (0.46.0)." |
| 115 (info callout) | "<strong>Linux/ELF first.</strong> … It is a local CTest registration (Linux/ELF only), not a CI job. The package machinery, RPATH, version script and consumer test are ELF/Linux only; Windows and macOS shared-library builds are not verified." | AM4-209..213: exported-symbols list, `@loader_path`, consumer test registered on Darwin | "<strong>Linux/ELF and macOS/Mach-O.</strong> The consumer test <code>CApi_InstalledConsumer</code> installs the <code>CNACApi</code> component into a staging prefix, configures the <code>hello_cna</code> example as a standalone project against it, builds it shared and static, and runs both with no <code>LD_LIBRARY_PATH</code> or <code>DYLD_*</code> variable. It is a local CTest registration on Linux and macOS, not a CI job; on macOS it also checks the installed dylib's <code>LC_RPATH @loader_path</code>. The export set is enforced by a version script on ELF and by ld64's exported-symbols list on macOS (exactly the 3,210 <code>cna_*</code> names). Windows shared-library builds are not verified." |
| 120 | "Native C ABI · 0.7.0 · 0.44.0" | 0.46.0 | "<code>0.46.0</code>" |
| 140 (version-history row "0.40.0 – 0.44.0") | ends at 0.44.0 | CURRENT as history, but the table needs the two newer minors | Add a row: "<code>0.45.0</code> – <code>0.46.0</code> \| 0.45.0 narrowed the renderer-identity constants to the 14 public identities (integer values of withdrawn identities stay reserved; no route, structure or export changed; source-breaking only for a binding that named a withdrawn constant). 0.46.0 adds <code>CNA_NATIVE_WINDOW_SYSTEM_UIKIT</code> (9): on iOS/iPadOS <code>cna_game_window_get_native_window_ext</code> reports the <code>UIWindow*</code>; additive." — **policy check for the lead:** the 0.45.0 sentence describes a withdrawal without naming identities; if even that is unwanted, write only the 0.46.0 half and "0.45.0: renderer-identity constant set reduced to the public 14 (values reserved)". |
| 167 | "(0.44)" rule note | CURRENT (historical rule) | — |
| 189 | "Tutorial 129 walks through a complete first program against ABI 0.44.0" | 0.46.0 | "…against ABI 0.46.0…" |
| 192 | "8,142 symbols: 7,030 implemented in C, 15 approved partial…, 656 …, 441 …" | COVERAGE.md at TARGET | "…8,142 symbols: 7,053 implemented in C, 15 approved partial, 631 planned, 443 not applicable…" |
| 194 | "The 656 planned rows are the live backlog" | 631 | "The 631 planned rows are the live backlog…" |
| 202 | "CApi_InstalledConsumer · Local CTest, Linux/ELF, timeout 900 s" | registered on Darwin (AM4-211) | "Local CTest, Linux/ELF and macOS/Mach-O, timeout 900 s" |
| 205 | "The CNA.NET campaign's final regression run on Linux x86_64 (CSX-153, 4 October 2026) records the native C API test set passing…" | add the macOS record | append: "CNA's Apple campaign (October 2026, physical Mac mini M4, arm64) records every C API test passing on macOS too — 119/119 in the SOFTWARE and SDL_RENDERER configurations, the exported symbols equal to the 3,210 declared routes, and the installed package consumed shared and static. We did not reproduce either run; …" |
| 210 | "CNA.NET at revision <code>860f92c</code> admits exactly 0.44.0, the version this snapshot exports" | cna-dotnet admitted 0.46.0 after a review of 0.44.0→0.46.0 (AM4-217, cna-dotnet `8219a6c`, as recorded by CNA's plan) | "…CNA.NET admits exactly 0.46.0, the version this snapshot exports: its maintainers moved from 0.44.0 to 0.46.0 after a recorded compatibility review (1,419 consumed exports, no prototype or layout change; 0.45.0 was never admitted). The archived bindings admit older generations only." |
| 214 | "C: CNA's own … <code>b0e97bb1</code>, 2026-10-04 … 0.44.0" | snapshot/ABI | "…<code>c1c316b9</code>, 2026-10-09 … 0.46.0 …" |
| 215 | "<a href="https://github.com/libcna/cna-cs">cna-cs</a> (C#/.NET, "CNA.NET") <code>860f92c</code>, 2026-10-04 … exactly 0.44.0" | repo renamed to `libcna/cna-dotnet` (`8947b91`); admits 0.46.0 (AM4-217) | "<a href="https://github.com/libcna/cna-dotnet">cna-dotnet</a> (C#/.NET, "CNA.NET"), admission change recorded at <code>8219a6c</code> (October 2026) · beta, source-first; no published packages · exactly 0.46.0 · …" (do not invent a later head SHA) |
| 231 | "none of the eight admits ABI 0.44.0 as qualified. … <code>cna_get_abi_version()</code> (encoded <code>0x00002C00</code> for 0.44.0) … the ELF symbol-version node <code>CNA_C_API_0.1</code>" | 0.46.0 / 0x00002E00; Mach-O marker | "…none of the eight admits ABI 0.46.0 as qualified. … (encoded <code>0x00002E00</code> for 0.46.0), the <code>CNA_ABI_VERSION</code> macro, the CMake package version, the ELF symbol-version node <code>CNA_C_API_0.1</code> (Linux) and the dylib's Mach-O compatibility version (macOS), …" |
| 234 (limitations list) | "No CNA CI job builds the C library. Run evidence comes from the CNA.NET campaign (Linux x86_64, plus Android-emulator and headless-Chromium hosts)…" / "656 … 441" / "declared ABI 0.44.0" / "Package machinery, RPATH, the version script and the consumer test are Linux/ELF-only; Windows, macOS and iOS shared-library consumption is not verified." | AM4-209..214; gate numbers | items → "No CNA CI job builds the C library. Run evidence comes from local records: the CNA.NET campaign (Linux x86_64, plus Android-emulator and headless-Chromium hosts) and CNA's Apple campaign on a physical Mac mini M4 — not from CNA's CI and not from us." / "…631 public C++ symbols are still unmapped, and 443 more are recorded as having no C form…" / "The declared ABI 0.46.0 is experimental and pre-1.0…" / "Package machinery, run path, export control and the consumer test exist for Linux/ELF and macOS/Mach-O (macOS measured locally on Apple silicon only); Windows and iOS shared-library consumption is not verified, and the C ABI is not exercised on iOS." |
| 235 | "Tutorial 129: Your first C program against ABI 0.44.0" | 0.46.0 | "…against ABI 0.46.0" |
| 241 (related card) | "How far the evidence for CNA's C ABI 0.44.0 reaches, … the 656 unmapped symbols" | card text = target page description; update with that page | "How far the evidence for CNA's C ABI 0.46.0 reaches, … the 631 unmapped symbols…" |
| 243 (related card) | "What CNA's C ABI 0.44.0 version checks admit…" | same | "…C ABI 0.46.0…" |
| 254, 261 (known-issue cards) | CNA-BUG-056 "…abi.h declares 0.44.0"; CNA-GAP-062 "656 …" | generated from `issues-source.json` (see Part 4) | regenerate after Part 4 edits |
| 89/64 CURRENT | Linux CNA.NET evidence sentences | still true | keep |

## deep-dives/reference/c-api-evidence-and-gates.html
Counts: STALE 16 · CURRENT 4 · OK-GENERIC 1

| Line | Current text (excerpt) | Why stale | Proposed replacement |
|---|---|---|---|
| 7/13/19 (meta, og, JSON-LD description) | "How far the evidence for CNA's C ABI 0.44.0 reaches, … the 656 unmapped symbols…" | 0.46.0; 631 | "How far the evidence for CNA's C ABI 0.46.0 reaches, what each release-gate criterion really checks, what the gate reports for the 631 unmapped symbols, and how the coverage inventory classifies modules." |
| 137 | "656 public C++ symbols in runtime scope have no C mapping" | 631 | "…631 public C++ symbols…" |
| 147 | "Links and exports · Not verified at this commit · The baseline's "runtime": 11264 field (0.44.0) can only come from a built library…" | AM4-212 measured the exports of the built dylib at TARGET-era source: "declared and exported agree exactly: 3210 routes", baseline current on arm64 macOS; runtime field now 11776 | "Links and exports · Measured locally on macOS · The baseline's <code>"runtime": 11776</code> field (0.46.0) comes from a built library. CNA's Apple campaign ran <code>check_declared_exports.py</code> and <code>generate_abi_baseline.py --check</code> against the built Mach-O library on a physical Mac mini M4: declared and exported agree exactly (3,210 routes) and the recorded layouts hold on arm64 macOS. Not run by CI." |
| 149 | "Integration tested · Declared locally only · CApi_InstalledConsumer … on Linux/ELF, where a developer enables the option." | registered on Darwin; passed on the M4 (AM4-211/213) | "…CApi_InstalledConsumer installs the package and builds and runs hello_cna shared and static, on Linux/ELF and on macOS (passed locally on a physical Mac mini M4), where a developer enables the option." |
| 150 | "CNA.NET (libcna/cna-cs), the maintained C# binding, admits exactly ABI 0.44.0 … six refuse a 0.44.0 library…" | rename; 0.46.0 (AM4-217) | "CNA.NET (libcna/cna-dotnet), the maintained C# binding, admits exactly ABI 0.46.0 after a recorded 0.44.0→0.46.0 compatibility review, and records local evidence on Linux and on osx-arm64. … six refuse a 0.46.0 library by an exact-version rule…" |
| 202 | "The install rules name libSDL3*.so* and set INSTALL_RPATH "$ORIGIN"…" | release gate now also requires the dylib pattern and `@loader_path` (AM4-210) | "The install rules name <code>libSDL3*.so*</code> and set <code>INSTALL_RPATH "$ORIGIN"</code> on Linux, and <code>libSDL3*.dylib</code> with <code>@loader_path</code> on macOS; the consumer script passes no <code>-rpath-link</code>, <code>LD_LIBRARY_PATH</code> or <code>DYLD_*</code> variable" |
| 209 | "The committed RELEASE_GATE.md names "CNA C ABI 0.44.0, experimental"" | 0.46.0 | "…names "CNA C ABI 0.46.0, experimental"…" |
| 212 | "656 public symbols in runtime scope have no C mapping" | 631 | "631 …" |
| 213 | "15 partially mapped symbols in 9 groups, 441 unmapped in 86 groups" | 443 | "…15 partially mapped symbols in 9 groups, 443 unmapped in 86 groups…" |
| 215 | "…They are registered in ModuleProbes.cmake in every native tests build that finds Python…" | CURRENT, but since AM4-160 the three generator gates exit 77 (CTest skip) unless the Doxygen series matches the pinned 1.9.x (`CNA_C_API_DOXYGEN`) | append: "Since October 2026 the coverage, limitations and release-gate CTests measure only with the Doxygen series their pins were recorded with (1.9.x); with another Doxygen they report Skipped, naming the version, and a direct invocation still fails." |
| 247 (totals row) | "Total (469 headers) 8,142 7,030 15 656 441" | COVERAGE.md | "8,142 · 7,053 · 15 · 631 · 443" (per-module rows above it must be re-read from `docs/c-api/COVERAGE.md` at TARGET) |
| 250 | "471 further headers are excluded … (renderers 137, content pipeline 107, platform 28, design 16, … 15, phone 9, inspector 3, diagnostics 2, and 154 Internal/Detail paths…)" | COVERAGE.md at TARGET | "451 further headers are excluded by the scope rules (renderers 115, content pipeline 107, platform 29, design 16, the build-time import and pipeline subtrees of content 15, phone 9, inspector 3, diagnostics 2, and 155 Internal/Detail paths of runtime modules)…" |
| 253, 266 | "The 656 planned rows…" / "7,486 of them (7,030 …, 15 …, 441 …)" | 631; 7,511 = 7,053+15+443 | "The 631 planned rows…" / "…partitions only 7,511 of them (7,053 fully mapped, 15 partially mapped, 443 with no C form)…" — verify CNA-BUG-058 still applies (LIMITATIONS still omits planned rows: not re-checked here) |
| 270 | "Say "ABI 0.44.0, experimental, source-level, not build-verified" for the library" | 0.46.0; CNA's own records now include local builds (Linux, macOS M4) | "Say "ABI 0.46.0, experimental; built and tested in CNA's own local runs (Linux; macOS on Apple silicon), not by CI" for the library; say that no CI workflow builds it…" |
| 271 / 272 | quote templates with 7,030/656/441 | numbers | "(469 headers, 8,142 symbols: 7,053 implemented, 15 partial, 631 planned, 443 not applicable)" / "Not ready, one criterion unmet: 631 public symbols are still unmapped" |

## deep-dives/reference/native-c-api.html
Counts: STALE 6 · CURRENT 6 (historical rule notes 0.42.0/0.44.0, example version pairs)

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 7/13/19 (meta/JSON-LD) | "What CNA's C ABI 0.44.0 version checks admit…" | 0.46.0 | "What CNA's C ABI 0.46.0 version checks admit…" |
| 136 | "…experimental native C API (ABI 0.44.0)…" | 0.46.0 | "(ABI 0.46.0)" |
| 141 | "(0.44.0 is 0x00002C00) … four later ones (0.40.0, 0.42.0, 0.43.0 and 0.44.0) changed which…" | current version/encoding; history incomplete | "(0.46.0 is <code>0x00002E00</code>) … four later ones (0.40.0, 0.42.0, 0.43.0 and 0.44.0) changed which calls succeed; 0.45.0 reduced the renderer-identity constants to the 14 public identities (source-breaking only for a binding that named a withdrawn one) and 0.46.0 added one native-window-system value (<code>CNA_NATIVE_WINDOW_SYSTEM_UIKIT</code>)" — same policy check as docs/c-api.html:140 |
| 143, 153, 210, 214 | example pairs "Headers 0.36.0, library 0.44.0" etc.; "(0.44.0)" rule notes | CURRENT (illustrative/historical); optionally shift the example to 0.46.0 | — |

## development/internals/bindings/c-api-internals.html
Counts: STALE 8 · CURRENT 3

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 7/13/19 (meta/JSON-LD) | "How CNA's experimental C ABI 0.44.0 is implemented…" | 0.46.0 | "…C ABI 0.46.0…" |
| 147 | "…CNA's own release gate for ABI 0.44.0 reads "Not ready"." | 0.46.0 | "…for ABI 0.46.0…" |
| 150 | "(0.44.0: CNA_ABI_VERSION_MAJOR 0, _MINOR 44, _PATCH 0…" | `abi.h:34-40` | "(0.46.0: <code>CNA_ABI_VERSION_MAJOR 0</code>, <code>_MINOR 46</code>, <code>_PATCH 0</code>…" |
| 155 | "On ELF only (UNIX AND NOT APPLE AND NOT EMSCRIPTEN) the link adds --exclude-libs,ALL and the version script CnaCApiExports.map: cna_* global, everything else local. INSTALL_RPATH "$ORIGIN"." | Apple branch added (`modules/c-api/CMakeLists.txt:103-115`, AM4-209/210) | "On ELF (<code>UNIX AND NOT APPLE AND NOT EMSCRIPTEN</code>) the link adds <code>--exclude-libs,ALL</code> and the version script <code>CnaCApiExports.map</code>; on Apple it passes ld64 <code>-exported_symbols_list cmake/CnaCApiExports.darwin.txt</code> (<code>_cna_*</code>). Either way <code>cna_*</code> is global and everything else local. Run path: <code>$ORIGIN</code> on ELF, <code>@loader_path</code> on macOS, where the dylib also gets install name <code>@rpath/libcna_c_api.dylib</code> and Mach-O versions from the ABI." |
| 285 | "CApi_InstalledConsumer … Local CTest, Linux/ELF only" | AM4-211 | "Local CTest, Linux/ELF and macOS (asserts <code>LC_RPATH @loader_path</code> there)" |
| 292 | "It does not establish that the library builds at b0e97bb1 … TARGET exports 0.44.0. The maintained C# binding admits exactly 0.44.0, an admission inferred from headers…" | 0.46.0; cna-dotnet admission AM4-217 based on a baseline diff and the macOS dylib passing its runtime contract | "…TARGET exports 0.46.0. The maintained C# binding admits exactly 0.46.0 since its maintainers reviewed the 0.44.0→0.46.0 difference (no prototype, layout or string change; five reviewed integer-constant differences) and ran its ABI fixtures against the built macOS library; the archived bindings stopped at 0.21–0.23 (Common Lisp) and 0.35.0 (the other seven)…" |
| 229 | "(0.44.0)" rule note | CURRENT | — |
| 312/313/322 (related cards) | 0.44.0 / 656 / BUG-056 | follow the target pages | regenerate with those pages |

## docs/tutorials/129-c-api-first-program.html
Counts: STALE 7 · CURRENT 2

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 7/12/18 (meta/JSON-LD) | "Install CNA's experimental C ABI 0.44.0 package…" | 0.46.0 | "…C ABI 0.46.0 package…" |
| 55 (breadcrumb meta) | "CNA snapshot b0e97bb1 · C ABI 0.44.0" | 0.46.0 | "· C ABI 0.46.0" |
| 59 | "Read this first — the C library is source-level, not build-verified. … (ABI 0.44.0, pre-1.0) … no CI workflow builds the C library and the authors of this tutorial did not build it." | CNA's own records now show the library built and its tests passing locally (Linux; macOS M4: AM4-209..213) | "<strong>Read this first.</strong> The C API is experimental (ABI 0.46.0, pre-1.0) and belongs to the unreleased development snapshot <code>c1c316b9</code>, not to a release. No CI workflow builds the C library; CNA's own local records show it built and its tests passing on Linux and, as a Mach-O dylib and static archive, on a physical Mac mini M4. The authors of this tutorial did not build it. …" (keep the rest after re-checking the "earlier snapshot" compile claim) |
| 79 | "The component contains the shared library libcna_c_api.so, …, whose RPATH is $ORIGIN, so you need no LD_LIBRARY_PATH…" | macOS packaging (AM4-210) | "…the shared library (<code>libcna_c_api.so</code> on Linux, <code>libcna_c_api.dylib</code> on macOS), …, the SDL3 libraries CNA built (installed beside the library, whose run path is <code>$ORIGIN</code> / <code>@loader_path</code>, so you need no <code>LD_LIBRARY_PATH</code> or <code>DYLD_*</code> variable)… On macOS create and run the game on the main thread when the renderer needs a window." |
| 272 | "CNA C ABI 0.44.0" (summary/footer) | 0.46.0 | "CNA C ABI 0.46.0" |
| 293 | "…8,142 symbols — 7,030 implemented, 15 partial, 656 planned, 441 not applicable. … the unmet one is the 656 public symbols…" | COVERAGE/RELEASE_GATE at TARGET | "…7,053 implemented, 15 partial, 631 planned, 443 not applicable … the unmet one is the 631 public symbols…" |
| 197-210 (code) | `if (runtime_abi != CNA_ABI_VERSION)` | CURRENT: the program compares against the header macro, no hard-coded version | — |

## docs/cna-net.html
Counts: STALE 11 · CURRENT 3 (Linux, browser, Android rows) · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 135 | "<a href="https://github.com/libcna/cna-cs">CNA.NET</a> (repository <code>libcna/cna-cs</code>)" | repository renamed (`8947b91`, 2026-10-06) | "<a href="https://github.com/libcna/cna-dotnet">CNA.NET</a> (repository <code>libcna/cna-dotnet</code>)" |
| 147 (diagram) | "libcna_c_api (cna_* functions, ABI 0.44.0)" | 0.46.0 | "libcna_c_api (cna_* functions, ABI 0.46.0)" |
| 171 | "CNA.NET is beta and source-first (revision 860f92c, 4 October 2026). … currently 0.44.0 — the version CNA exports at this documentation snapshot…" | AM4-217: admits 0.46.0; revision pin | "CNA.NET is <strong>beta and source-first</strong>. There are no published NuGet packages or prebuilt native libraries yet; you build CNA's C ABI and CNA.NET from source. Each CNA.NET revision admits exactly one reviewed C ABI version, currently <strong>0.46.0</strong> (admitted at <code>8219a6c</code> after a recorded review of the 0.44.0→0.46.0 difference) — the version CNA exports at this documentation snapshot, so the two are a matched pair. A different CNA build is refused when the library loads, with a diagnostic naming both versions." |
| 179 (platform row) | "Windows, macOS · Build steps are documented; only compile-time ABI header checks ran in CI · everything at run time — future qualification work" | AM4-215..231: osx-arm64 measured locally | split into two rows: **macOS (Apple silicon, osx-arm64)** · "Local measurements on a physical Mac mini M4 (October 2026, .NET SDK 8.0.425): Debug and Release builds; managed suites (Framework 652 + 3 skipped, XnaCompat 319, BrowserCompat 5, Integration 261/261 on SOFTWARE, GamerServices/Avatar/Net 24); ABI verification with 0 mismatches; package acceptance with <code>runtimes/osx-arm64/native</code> (60 and 600 frames with no environment); the template; all 84 sample programs started and ran to a 15-second alarm on SOFTWARE and on METAL; a main-thread C# game with exact pixel readback on METAL" · "CI runtime leg, signing and notarization; Intel Macs (only an osx-x64 ABI-header check runs in CI); the SDL_RENDERER integration suite (239 of 261 pass); per-sample pixel checks" — and **Windows** · "Build steps are documented; only compile-time ABI header checks ran in CI" · "everything at run time — future qualification work" |
| 180 | "iOS · — · planned (static linking), not started" | CURRENT (nothing in the campaign) | keep |
| 184 (after table) | "These are local measurements recorded in CNA.NET's campaign ledgers (CSX-001 to CSX-155, closed on 4 October 2026)…" | macOS evidence is recorded in CNA's `plans/plan_apple_m4.md` (AM4-215..231) | "These are local measurements recorded in CNA.NET's campaign ledgers (CSX-001 to CSX-155, closed on 4 October 2026) and, for macOS, in CNA's Apple campaign record (AM4-215 to AM4-231, October 2026), not continuous-integration results; nothing was re-run for this page. …" |
| 187 | "cna-cs-samples is not a port…" | renamed `cna-dotnet-samples` | "<code>cna-dotnet-samples</code> is not a port…" (link `https://github.com/libcna/cna-dotnet-samples`) |
| 190 | "All 84 build in Debug and Release and run on Linux; all 84 run single-threaded in headless Chromium; all 84 draw on the x86_64 Android emulator." | add macOS (AM4-228) | append: "On a physical Mac mini M4 the solution builds (122 projects) and all 84 start, load their content and keep running to a 15-second alarm on SOFTWARE and on METAL (smoke runs, not pixel comparisons)." |
| 197, 204, 206 | "cna-cs-samples …" / "cna-cs-template: dotnet new install it…" | rename | "cna-dotnet-samples" / "cna-dotnet-template: <code>dotnet new install</code> it, then <code>dotnet new cna-game</code>…" |
| 214 | "…the native staging scripts are Linux-only (WSL 2 on Windows)." | browser/Android staging scripts: not changed by the campaign as far as recorded; desktop `build-native-cna.sh`/`run-sample.sh` (samples) run on Darwin since AM4-228 | CURRENT for browser/Android staging; optionally add "the desktop sample scripts also run on macOS" |

## docs/migrating-to-cna-net.html
Counts: STALE 19 · CURRENT 3

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 136 | "(docs/migrating-xna-games.md in libcna/cna-cs, revision 860f92c)… Linux x86_64 is the platform on which they were qualified." | rename; macOS osx-arm64 now measured locally (AM4-229) | "(docs/migrating-xna-games.md in libcna/cna-dotnet) … Linux x86_64 is the platform on which they were qualified; CNA's Apple campaign also measured the desktop route on osx-arm64 (local evidence, not a shipping claim)." |
| 144 | "The C ABI … currently 0.44.0" | 0.46.0 | "currently 0.46.0" |
| 156 | "A cna-cs checkout next to it." | rename | "A <code>cna-dotnet</code> checkout next to it." |
| 160 | "The configuration CNA.NET qualifies on Linux: the OpenGL ES 3 renderer…" | CURRENT for Linux; macOS uses SOFTWARE or METAL (OPENGLES3 n/a on macOS) | append: "On macOS the measured configurations are SOFTWARE and METAL, each with its compiled-effects option on (<code>CNA_SOFTWARE_COMPILED_EFFECTS</code> / <code>CNA_METAL_COMPILED_EFFECTS</code>)." |
| 168 | "CNA.NET at 860f92c admits exactly 0.44.0 … Windows build steps exist in the upstream guide, but nothing has been run on Windows yet…" | 0.46.0; Windows part CURRENT | "CNA.NET admits exactly 0.46.0, the version of this documentation snapshot. Windows build steps exist in the upstream guide, but nothing has been run on Windows yet, so treat them as a source-build exercise…" |
| 171, 211, 225, 226, 232, 233 | `cd cna-cs`, `CNA_CS_ROOT=/path/to/cna-cs …`, `# in cna-cs` | rename (`8947b91`: `CNA_CS_ROOT` → `CNA_DOTNET_ROOT`) | `cd cna-dotnet`; `CNA_DOTNET_ROOT=/path/to/cna-dotnet …`; `# in cna-dotnet` |
| 177 | "Point your projects at the checkout with CNA_CS_ROOT" | rename | "…with <code>CNA_DOTNET_ROOT</code> (an environment variable or MSBuild property <code>CnaDotnetRoot</code>)." |
| 194, 197 | `$(CnaCsRoot)/src/…` | rename | `$(CnaDotnetRoot)/src/…` |
| 203 | "(cna-cs-samples has a Linux/Wine script)" | rename | "(cna-dotnet-samples has a Linux/Wine script)" |
| 219 (snippet) | template engine switch text | CURRENT | — |
| 223 | "The staging script is Linux-only:" (browser) | CURRENT (not changed by the campaign as recorded) | — |
| 239 | "set CNA_CS_ROOT and CNA_NATIVE_LIBRARY" | rename | "set <code>CNA_DOTNET_ROOT</code> and <code>CNA_NATIVE_LIBRARY</code>" |
| — | (no macOS section) | macOS osx-arm64 is now measured | optional new short section: "macOS (Apple silicon)": build CNA's C API with SOFTWARE or METAL (+ compiled-effects option), point <code>CNA_NATIVE_LIBRARY</code> at <code>libcna_c_api.dylib</code>; METAL needs SDL's <code>cocoa</code> driver and the game on the main thread; local evidence only (no CI, signing or notarization). |

## docs/tutorials/170-run-xna-csharp-game-on-cna-net.html
Counts: STALE 10 · CURRENT 2

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 60 | "…each CNA.NET revision admits exactly one C ABI version (0.44.0 at this snapshot)." | 0.46.0 | "(0.46.0 at this snapshot)" |
| 63, 97, 110, 118 | "cna-cs-samples …" | rename | "cna-dotnet-samples …" |
| 66 | "# CNA's C ABI, in the configuration CNA.NET qualifies on Linux" | CURRENT; add macOS note | add comment line: "# macOS (Apple silicon): use SOFTWARE or METAL with its compiled-effects option instead of OPENGLES3" |
| 72, 74 | `dotnet build cna-cs/CNA.sln -c Release`; `export CNA_CS_ROOT="$PWD/cna-cs"` | rename | `dotnet build cna-dotnet/CNA.sln -c Release`; `export CNA_DOTNET_ROOT="$PWD/cna-dotnet"` (solution file name `CNA.sln` not re-verified post-rename) |
| 92, 95 | `$(CnaCsRoot)` | rename | `$(CnaDotnetRoot)` |
| 118 | "…run on Linux (on private X displays), single-threaded in headless Chromium, and on the x86_64 Android emulator…" | add macOS smoke (AM4-228) | "…run on Linux (on private X displays), single-threaded in headless Chromium and on the x86_64 Android emulator; on a physical Mac mini M4 all 84 start and run to a 15-second alarm on SOFTWARE and METAL (smoke runs)…" |

## docs/tutorials/171-cna-net-template.html
Counts: STALE 9 · CURRENT 2

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 7/12/18 (meta/JSON-LD) | "Install cna-cs-template, create a C# game with dotnet new cna-game…" | rename | "Install cna-dotnet-template, create a C# game with dotnet new cna-game…" |
| 60 | "Commands follow cna-cs-template's README (revision 008c3b1)…" | rename; template verified on macOS (AM4-226, AM4-230) | "Commands follow cna-dotnet-template's README and were not re-run for this page. CNA's Apple campaign verified the template on a physical Mac mini M4 (development and package modes; a fresh <code>dotnet new cna-game</code> reports METAL and draws 60 and 600 frames on the METAL library)." (drop the old SHA or keep it as "pre-rename revision 008c3b1") |
| 64, 66 | "cna-cs-template" / "cna-cs-samples" | rename | "cna-dotnet-template" / "cna-dotnet-samples" |
| 70, 76 | `dotnet new install /path/to/cna-cs-template`; `export CNA_CS_ROOT=/path/to/cna-cs` | rename | `dotnet new install /path/to/cna-dotnet-template`; `export CNA_DOTNET_ROOT=/path/to/cna-dotnet` |
| (body) | engine-diagnostics output | AM4-230 fixed generated games losing `#if ENGINE_CNA` (renderer reported as "Display 0") | if the page shows sample output of the diagnostics, make sure it shows the renderer name (e.g. "METAL"/"OPENGLES3") |

## development/internals/bindings/csharp.html
Counts: STALE 14 · CURRENT 8 (design facts read at 860f92c)

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 7/8/13/19 (meta/JSON-LD) | "How the maintained CNA.NET binding (cna-cs at 860f92c) loads, admits and calls CNA's C ABI: layers, the exact-0.44.0 admission matrix…" | rename; 0.46.0 | "How the maintained CNA.NET binding (cna-dotnet) loads, admits and calls CNA's C ABI: layers, the exact-version admission matrix (0.46.0)…" |
| 139, 246 | "Reading order at cna-cs commit 860f92c" | rename; the page's facts were read at 860f92c (pre-rename) | "Reading order (as read at the pre-rename commit 860f92c of what is now libcna/cna-dotnet)" |
| 144, 146 | "Binding facts were read at libcna/cna-cs 860f92c… which admits C ABI 0.44." / "CNA.NET (libcna/cna-cs) is the maintained…" | rename; admission moved | "Binding facts were read at 860f92c (2026-10-04) of the repository now named libcna/cna-dotnet; that revision admitted C ABI 0.44.0. CNA's Apple campaign records the move to 0.46.0 at cna-dotnet 8219a6c (AM4-217)…" / "CNA.NET (libcna/cna-dotnet)…" |
| 148 | "At the audited commit the binding admits exactly one native generation, C ABI 0.44.0, and CNA snapshot b0e97bb1 declares 0.44.0…" | TARGET declares 0.46.0; binding moved | "At the audited commit (860f92c) the binding admitted exactly C ABI 0.44.0. CNA snapshot c1c316b9 declares 0.46.0, and CNA.NET's maintainers admitted 0.46.0 (and never 0.45.0) after reviewing the difference: 1,419 consumed exports, 0 absent, 0 changed prototypes, no struct, scalar or string change, five reviewed integer constants (AM4-217). So the pair matches again — by review, not by a run of this page." |
| 174 | resolver file names incl. `libcna_c_api.dylib` | CURRENT; AM4-221 added Mach-O loader diagnostics ("the wrong architecture or binary format") | optional: add "On macOS dyld's "incompatible architecture" / "not a mach-o file" are reported as a wrong-architecture library (cna-dotnet bdbd49f)." |
| 178 | "ConsumerVersion = 0.44.0 … (policyVersion cna-cs-native-abi/1, consumerAbi 0.44.0, acceptedVersions = [0.44.0]…" | moved to 0.46.0 (AM4-217); policy identifier after the rename not established | "…(<code>ConsumerVersion</code> = 0.46.0 since 8219a6c; at 860f92c it was 0.44.0) … <code>eng/cna-native-abi-policy.json</code> (at 860f92c: <code>policyVersion cna-cs-native-abi/1</code>, <code>consumerAbi 0.44.0</code>)…" — do not invent the post-rename identifier |
| 182 | "What the snapshot's 0.44.0 surface looks like from this binding" (heading) | 0.46.0 | "What the snapshot's 0.46.0 surface looks like from this binding" (body: 0.46.0 adds only `CNA_NATIVE_WINDOW_SYSTEM_UIKIT`; the 1,419 consumed exports are unchanged) |
| 243 | "Linux x86_64 is the primary qualified platform…" platform classes | add osx-arm64 local evidence (AM4-229) | append: "osx-arm64 now has local evidence measured on a physical Mac mini M4 (builds, managed suites, ABI verification, package acceptance, template, 84 samples smoke-run on SOFTWARE and METAL), recorded by the binding as "local evidence, not a shipping claim (no CI leg, signing or notarization)"; osx-x64 has only a CI ABI-header check (moved to the macos-15-intel image)." |
| 253 | "docs/migrating-xna-games.md and docs/final-compatibility-audit.md: the build steps per platform…" | CURRENT | — |

## Other pages: CNA.NET rename (`cna-cs` → `cna-dotnet`) outside the pages above
Each row is STALE (rename `8947b91`); replace the repository/template/samples names and links (`https://github.com/libcna/cna-cs*` → `https://github.com/libcna/cna-dotnet*`). Where the same sentence says "admits exactly 0.44.0", use the ABI rows of Part 3.

| File:line | Excerpt | Replacement |
|---|---|---|
| deep-dives/foundations/ecosystem.html:189 | "the language bindings (cna-cs, the C# binding CNA.NET, is maintained and admits exactly C ABI 0.44.0…" | "(cna-dotnet, the C# binding CNA.NET, is maintained and admits exactly C ABI 0.46.0…" |
| deep-dives/reference/ecosystem-quick-reference.html:198 | "CNA.NET (cna-cs) … admits exactly C ABI 0.44.0, the version CNA exports at this snapshot" | "CNA.NET (cna-dotnet) … admits exactly C ABI 0.46.0, the version CNA exports at this snapshot" |
| development/architecture/bindings.html:8, 173 | "libcna/cna-cs (860f92c) · Exactly 0.44.0" | "libcna/cna-dotnet (0.46.0 admitted at 8219a6c) · Exactly 0.46.0" |
| development/handbook/change-map.html:217 | "(CNA.NET, libcna/cna-cs) … admits exactly one ABI (0.44.0 at cna-cs 860f92c)" | "(CNA.NET, libcna/cna-dotnet) … admits exactly one ABI (0.46.0)" |
| development/handbook/change-public-xna-behavior.html:232 | "pins its own exact ABI (0.44.0 at cna-cs 860f92c)" | "pins its own exact ABI (0.46.0 in cna-dotnet)" |
| development/handbook/update-the-c-api.html:286 | "CNA.NET (cna-cs) … admits exactly one reviewed ABI point, 0.44.0 at its revision 860f92c" | "CNA.NET (cna-dotnet) … admits exactly one reviewed ABI point, 0.46.0 (moved from 0.44.0 by a recorded review; 0.45.0 never admitted)" |
| development/takeover/investigation.html:188 | "the C# binding's policy at cna-cs 860f92c eng/cna-native-abi-policy.json admits only exact reviewed entries (consumer ABI 0.44.0)" | "…at cna-dotnet … (consumer ABI 0.46.0; 0.44.0 at the pre-rename 860f92c)" |
| development/takeover/uncertainty.html:165 | "(CNA.NET, libcna/cna-cs) … admits exactly ABI 0.44.0" | "(CNA.NET, libcna/cna-dotnet) … admits exactly ABI 0.46.0" |
| development/workflows.html:166 | "(CNA.NET, libcna/cna-cs) … (0.44.0 at 860f92c)" | "(CNA.NET, libcna/cna-dotnet) … (0.46.0)" |
| docs/faq.html:162 | "separate, pre-alpha language-binding projects (including a C# one, cna-cs) target its experimental C ABI, but each is pinned to an older ABI version than…" | already inconsistent with faq:184 (CNA.NET is beta and matched); "including a C# one, cna-cs" → "the C# binding CNA.NET (cna-dotnet) is maintained and matches the current ABI; the other bindings are archived and pinned to older ABI versions" |
| docs/getting-started.html:143 | "cna-cs-samples holds the original Microsoft samples…" | "cna-dotnet-samples holds…" |
| index.html:135 (title tooltip: "cna-cs-samples @ 1e6d763 … on Linux, in headless Chromium and on the x86_64 Android emulator"), 415, 417 | "cna-cs-template (a dotnet new template…)", "cna-cs on GitHub ↗", href to libcna/cna-cs | "cna-dotnet-template …", "cna-dotnet on GitHub ↗", `https://github.com/libcna/cna-dotnet` |
| roadmap.html:209 | "(cna-cs-samples 1e6d763)" | "(cna-dotnet-samples, pre-rename revision 1e6d763)" |
| showcase.html:145, 334 | "cna-cs-samples — the same Microsoft samples as unchanged original C#…" | "cna-dotnet-samples — …" (+ link) |

# Part 3 — Cross-site C ABI version (0.44.0 → 0.46.0) outside Parts 1-2

Rules: **A** = "CNA's ABI is 0.44.0 at this snapshot" → STALE, write 0.46.0. **B** = "CNA.NET admits exactly 0.44.0 (at 860f92c / cna-cs)" → STALE, write
"CNA.NET (cna-dotnet) admits exactly 0.46.0". **C** = encoded `0x00002C00` / `11264` → `0x00002E00` / `11776`. **D** = historical
rule/version notes ("0.40.0–0.44.0", "the commit that set 0.44.0 (ed885a8ae)", "(0.44.0)" after a rule, example version pairs) → CURRENT; where a
version-history list *ends* at 0.44.0, append 0.45.0/0.46.0 (policy check as in docs/c-api.html:140). **E** = archived bindings "refuse TARGET's 0.44.0" →
STALE number only: "refuse TARGET's 0.46.0". **F** = related-card/meta descriptions copied from another page → change with that page.

| File:line | Rule | Excerpt (short) |
|---|---|---|
| about.html:70 | A | "experimental native C ABI, now at 0.44.0, on which the C# binding CNA.NET runs…" |
| about.html:122 | A | "An experimental C ABI: version 0.44.0 (alpha.1: 0.7.0), 60 headers and 3,210 routes" |
| architecture.html:240 | A | "c-api · Experimental C ABI 0.44.0 adapter over the C++ aggregate" |
| architecture.html:517 | A | "c-api/ ← experimental C ABI 0.44.0" |
| deep-dives/foundations/cna-and-xna.html:203, 208 | A | "The experimental C ABI (0.44.0) versions independently"; "the C ABI version (0.44.0)" |
| deep-dives/practice/project-records-and-evidence.html:177 | A | "(0.44.0 at this snapshot)" |
| deep-dives/reference/c-api-evidence-and-gates.html:148 | D | "the commit messages of the 0.40.0 to 0.44.0 changes … report local runs of 119 of 119" — CURRENT; may add "and AM4-213 (macOS): 119/119" |
| deep-dives/reference/glossary.html:142 | A | "The version of CNA's experimental native C interface: 0.44.0 at this snapshot" |
| deep-dives/reference/index.html:130, 131 | F | card descriptions (native-c-api, c-api-evidence-and-gates) |
| development/architecture/bindings.html:19 | A+B | JSON-LD "The experimental C ABI (0.44.0) … which admits exactly ABI 0.44.0" |
| development/architecture/bindings.html:146 | A | "whose ABI version at this snapshot is 0.44.0" |
| development/architecture/bindings.html:153 | A+D | "CNA_ABI_VERSION (0.44.0, in abi.h) … Of the fifteen minors from 0.30.0 to 0.44.0…" → "(0.46.0, in abi.h) … Of the seventeen minors from 0.30.0 to 0.46.0, …" and add the 0.45.0 (source-breaking for named withdrawn constants) / 0.46.0 (additive) classification |
| development/architecture/bindings.html:190 | A+B | "This snapshot exports 0.44.0. The maintained C# binding admits exactly 0.44.0; its own records measure it against an earlier CNA commit…" → "This snapshot exports 0.46.0. The maintained C# binding admits exactly 0.46.0 after a recorded review; its macOS records were measured against a CNA commit (a3da0a5bb) on this branch, and its Linux records against an earlier commit…" |
| development/architecture/bindings.html:197 | D | rule-only steps list "(0.40.0, 0.42.0 to 0.44.0)" — CURRENT; add "0.46.0 is additive" |
| development/architecture/bindings.html:207, 209 | F | card descriptions |
| development/debugging.html:262 | A+C+B | "This snapshot exports ABI 0.44.0 (…encoded 0x00002C00…), which is exactly the version the maintained binding (CNA.NET…)" → 0.46.0 / 0x00002E00 |
| development/handbook/change-map.html:217 | A+B | "(0.44.0 at this snapshot) … (0.44.0 at cna-cs 860f92c)" |
| development/handbook/make-a-release.html:176, 229 | A | "Native C ABI version 0.44.0, experimental"; "(0.44.0 at TARGET)" |
| development/handbook/update-libcna-com.html:216 | A | "C ABI (0.44.0), headers (60), routes (3,210)" |
| development/handbook/update-the-c-api.html:8 | F/A | meta |
| development/handbook/update-the-c-api.html:162 | D | "the commit that set ABI 0.44.0 (ed885a8ae, 34 commits before this snapshot…)" → CURRENT as history but "34 commits before this snapshot" is now wrong (`git rev-list --count ed885a8ae..c1c316b9` = 388; or drop the count); add the AM4-213 macOS record "^CApi 119/119 (SOFTWARE and SDL_RENDERER trees)" |
| development/handbook/update-the-c-api.html:199 | C | "(0.44.0 is 0x00002C00)" |
| development/handbook/update-the-c-api.html:218 | D | history list ends at 0.44.0 → append 0.45.0/0.46.0 |
| development/handbook/update-the-c-api.html:230 | D | "ABI_VERSIONING.md records every step from 0.30.0 to 0.44.0, but [Unreleased] has no entry for most of them" → "…to 0.46.0 …; CHANGELOG has an entry for 0.45.0 but none for 0.46.0" |
| development/handbook/update-the-c-api.html:314, 315, 325 | F | cards (incl. CNA-BUG-056) |
| development/internals/bindings/java.html:19, 131, 146, 148, 150, 171 | E | "refuses TARGET's 0.44.0", "TARGET exports 0.44.0", "TARGET snapshot b0e97bb1 declares 0.44.0", "Between ABI 0.21 and TARGET's 0.44.0…", "pointing CNA_ROOT at a 0.44…" → 0.46.0 (and add 0.45.0/0.46.0 to the "minor steps" sentence at 150) |
| development/internals/bindings/python.html:131, 146, 150, 234, 240 | E | "refuses TARGET's 0.44.0", "(ABI 0.44.0) library", "exports ABI 0.44.0 (abi.h: CNA_ABI_VERSION_MINOR is 44)", "0.36.0 to 0.44.0 came after the final revision: five add routes and four change rules only", "(0.44.0 at TARGET)" → 0.46.0 / MINOR is 46 / "0.36.0 to 0.46.0 …: five add routes, four change rules only, one (0.45.0) withdraws renderer-identity constants and one (0.46.0) adds a native-window-system value" |
| development/internals/modules/storage.html:227 | A | "(…ABI 0.44.0; source-level, not build-verified here)" → "ABI 0.46.0; built and tested in CNA's own local runs (Linux; macOS on Apple silicon), not here" |
| development/reference/public-headers.html:162, 176 | A, F | "(modules/c-api/include/CNA/C, ABI 0.44.0)" |
| development/reference/test-targets.html:142 | F | card |
| development/repository/index.html:224, 241 | A | "The experimental C ABI (0.44.0; …)"; "(ABI 0.44.0, experimental)" |
| development/repository/source-ownership.html:362 | A | "CNA_ABI_VERSION in abi.h (0.44.0, experimental)" |
| development/takeover/blast-radius.html:169 | B | "admits exactly the ABI version it was built for, 0.44.0 at its recorded revision, which is also what this snapshot exports" → "0.46.0 since its recorded review, which is also what this snapshot exports" |
| development/takeover/index.html:195 | A+B | "(0.44.0 at this snapshot) … CNA.NET, which admits exact…" |
| development/takeover/inherited.html:155 | A (+ policy) | "14 physical renderer-family directories serving 18 public renderer identities, an experimental C ABI (0.44.0, 60 public headers)" → "12 renderer-family directories serving 14 public renderer identities, an experimental C ABI (0.46.0, 60 public headers)" — the 18/14 numbers are also stale (RRC-018) |
| development/takeover/investigation.html:188 | A+B | "(0.44.0 at this snapshot) … (consumer ABI 0.44.0)" |
| development/takeover/mental-model.html:194 | B | "CNA.NET admits exactly ABI 0.44.0, the version this snapshot exports" |
| development/takeover/threading.html:270, 274 | D | "That document still states only the baseline; the headers of ABI 0.39.0 to 0.44.0 promise more…" — CURRENT (0.45.0/0.46.0 add no threading rule). Optional addition: `CALLBACKS_AND_THREADING.md` now also states Apple's main-thread rule for windowed renderers (AM4-074, AM4-214). |
| development/takeover/uncertainty.html:164, 165, 179 | A, B, A | "The C ABI is 0.44.0 (abi.h)…"; "admits exactly ABI 0.44.0"; "at this snapshot (ABI 0.44.0) the maximum is 43, FNA3D" → 0.46.0 (maximum still 43) |
| development/takeover/worked-changes.html:199 | A+B | "At this snapshot CNA exports ABI 0.44.0 and the C# binding admits exactly that version" |
| development/testing/architecture.html:344, 377 | F | cards |
| development/workflows.html:165, 166 | A, B | "The ABI is 0.44.0 at this snapshot"; "(0.44.0 at 860f92c)" |
| docs/building.html:453 | A | "CNA_BUILD_C_API … (ABI 0.44.0; …)" |
| docs/building.html:541 | A+B | "The C ABI version is 0.44.0 (experimental; alpha.1 was 0.7.0) … CNA.NET at revision 860f92c admits exactly 0.44.0." |
| docs/cnaext-extensions.html:300 | A | "(0.44.0 at this snapshot)" |
| docs/cnb-format.html:515 | A | "The experimental C ABI (version 0.44.0 at this snapshot…)" |
| docs/faq.html:150 | A | "Its experimental native C ABI (version 0.44.0) is not built by CNA's CI…" → "(version 0.46.0) is not built by CNA's CI (CNA's own local runs build it on Linux and macOS)…" |
| docs/faq.html:184 | B | "CNA.NET is beta and pairs with exactly the ABI version this snapshot exports (0.44.0)" → "(0.46.0)" |
| docs/releases.html:213 | A | "0.44.0: 60 headers, 3,210 routes; not built by CNA's CI, built and used on Linux by th…" → "0.46.0: 60 headers, 3,210 routes; not built by CNA's CI; built and used locally on Linux (CNA.NET) and on a physical Mac mini M4 (macOS)" |
| docs/releases.html:214 | B | "The C# binding CNA.NET (beta) over C ABI 0.44.0" |
| docs/releases.html:240 | A | "0.44.0 at snapshot b0e97bb1" → "0.46.0 at snapshot c1c316b9" |
| docs/rendering-backends.html:612 | A | "(ABI 0.44.0)" |
| docs/roadmap.html:179, 260 | A, B | "The experimental C ABI at 0.44.0"; "pairs with exactly ABI 0.44.0" |
| docs/runtime-renderer-selection.html:141, 156 | A, F | "The experimental C API (ABI 0.44.0)…" |
| docs/tutorials/133-renderer-capability-profile.html:444 | A+B | "CNA's C ABI is 0.44.0 … (CNA.NET, which admits exactly ABI 0.44.0)" |
| docs/tutorials/146-cnb-packs.html:429 | A | "(0.44.0 at this snapshot) declares 272 cna_cnb_* routes" (route count not re-checked) |
| docs/verification.html:522 | A + gate numbers | "7,030 implemented, 15 partial, 656 planned, 441 not applicable. ABI 0.44.0" → "7,053 implemented, 15 partial, 631 planned, 443 not applicable. ABI 0.46.0" |
| docs/verification.html:731 | F | card |
| documentation.html:96, 128 | A | "(0.44.0)"; "ABI 0.44.0 (alpha.1: 0.7.0) source surface: 60 headers, 3,210 routes" |
| features.html:24 (meta/JSON-LD), 80, 807, 808, 809 | A | "experimental C ABI 0.44.0" ×5 |
| index.html:108, 146 | A | "(0.44.0, opt-in build)"; "now at 0.44.0" |
| index.html:415 | B + rename | "revision 860f92c admits exactly C ABI 0.44.0, the version this snapshot exports. Companion repositories: cna-cs-template…" → "CNA.NET admits exactly C ABI 0.46.0, the version this snapshot exports, and has local osx-arm64 evidence besides Linux, browser and Android. Companion repositories: cna-dotnet-template…" |
| roadmap.html:203, 266 | B, A+B | "pairs with exactly C ABI 0.44.0"; "The C ABI is at 0.44.0 … pairs with exactly 0.44.0" |
| known-issues/** (bug-055, bug-056, bug-057, gap-062, vgap-053, bugs/index) | — | generated; see Part 4 |

# Part 4 — Known issues (generated; edit `audit/data/bible/issues/issues-source.json`, then `scripts/known_issues.py build`)

The generator publishes only issues that exist at TARGET ("the index has no `fixed` status"); a fixed issue must move to `dispositions.json` and its page disappears.
Status below is verified against CNA `c1c316b9` where a citation is given; "not re-checked" means only the Apple aspect was examined.

| Issue | Apple-related claim | Status at c1c316b9 | Recommended action |
|---|---|---|---|
| **CNA-GAP-013** | METAL refuses MRT, custom effects, occlusion queries, instancing, multi-stream input, back-buffer readback, sampler LOD/MaxMipLevel, partial colour-write masks, MultiSampleMask; MSAA applied as none | **FIXED** (AM4-025, 034, 038, 077, 079, 097, 135, 141, 143; `metal-renderer.md:111-126`) | Retire (disposition: fixed in the delta). If the owner wants a residual Metal-limits issue, open a new one from R2 §2.4 "Limitations still recorded" (PresentInterval.Two, BGRA8 backbuffer, LOD bias < 26, MSAA RT2D PreserveContents SetData, SpriteBatch-only MSL, compiled effects opt-in). |
| **CNA-GAP-028** | METAL samples neither KHR_materials_specular texture | **FIXED** (AM4-085: `Metal_PbrDualUvSpecular` 8/8; GLTF-344 closed) | Retire. |
| **CNA-VGAP-024** | METAL CI proves construction/clear/capabilities only; macos-14; 3 registered Metal tests | **STALE**: `metal-macos-ci.yml` runs on macos-26 and `ctest -R '^Metal'` now covers 518 tests incl. the shared pixel fixtures and oracles (AM4-255, AM4-279, AM4-289); full 3D pixel evidence exists locally on a physical Mac mini M4 (`-L Metal` 261/261, full tree 11,015/11,015) | Rewrite (narrow) or retire. Narrowed version: "Metal's hosted CI runs the 518 `^Metal` tests on GitHub's paravirtual GPU without shader validation, one process at a time; no green hosted run after the last CI change is recorded, and the full-tree and validation-layer evidence is local (physical Mac mini M4)." |
| **CNA-VGAP-008** | iOS evidence = device final-link + one-frame simulator launch | **STALE for iOS**: METAL on iOS (AM4-037); `cna_ios_pixel_probe` exact on frame 1 + 10 frames in 8 of 8 iPhone 17 Simulator launches (AM4-120); CI iOS matrix has METAL device/simulator legs with the probe; still no physical device | Narrow the iOS half: "iOS evidence is Simulator-only: a smoke app and a pixel probe (clear, SpriteBatch quad, BasicEffect triangle) exact in 8 of 8 launches on an iPhone 17 Simulator profile; device builds are final-linked but no physical iPhone/iPad has run CNA." Android half: not re-checked. |
| **CNA-BUG-199** | apple-ci and metal-macos-ci pin sharp-runtime f23ded28 | **FIXED** (AM4-234; workflows check out the branch from `scripts/ci/sibling_branch.sh`) | Retire. |
| **CNA-VGAP-019** | ModuleLinkClosure_* skip under Ninja (incl. "macos" presets context) | **FIXED** (AM4-167: 28/28 measured on the M4 Ninja tree) | Retire (note: CI still may not run them; re-check before writing a successor). |
| **CNA-BUG-190** | renderers/CMakeLists enters common/d3d and Metal only when default matches; title names a retired identity | **FIXED** in the delta by `71a0e7313` (RRC-027, "enter common/d3d and build the Metal renderer on membership, not the default") | Retire (also removes a retired-renderer name from public pages). |
| **CNA-BUG-012** | capability test default arm mis-describes METAL/SDL_GPU; SDL_GPU occlusion limitation test message | **Appears FIXED**: SDL_GPU row added (AM4-175), the SDL_GPU stale tests aligned with the public refusal (AM4-070; `sdlgpu_occlusionquery_limitation_test.cpp` changed by `bb9250261`); METAL now reports MRT/occlusion/custom effects true | Re-verify the two named tests at TARGET, then retire or narrow (the text also names a retired GL identity). |
| **CNA-BUG-094** | SDL_GPU claims SPIR-V intake for compute and ShaderEffect on Metal/D3D12 drivers | **NARROWED**: ShaderEffect SPIR-V now goes through the routed shader path (AM4-068, `8a5e6e220`); `SupportsComputeShadersEXT()` still returns `device_ != nullptr` and compute still creates `SDL_GPU_SHADERFORMAT_SPIRV` (`SdlGpuModern.cpp:561`) | Narrow to the compute half. |
| **CNA-VGAP-025** | no CI selects WEBGPU or SDL_GPU; SDL_GPU Metal route has no execution evidence | **PARTLY STALE**: SDL_GPU on SDL's Metal driver ran its full tree locally on the M4 (10,962/10,962; AM4-208); WEBGPU on macOS 10,968/10,968 locally; `emscripten-multi-renderer-ci.yml` now builds a WEBGL2+WEBGPU bundle (CI) | Narrow: "No CI workflow runs the SDL_GPU or native WEBGPU test suites; their macOS evidence (SDL's Metal driver; wgpu-native's Metal backend) is a local Mac mini M4 campaign." |
| **CNA-VGAP-021** | no SpriteFont/DrawString pixel test for DIRECTX9, METAL, CANVAS or FNA3D | **STALE for METAL** (`modules/renderers/metal/examples/CMakeLists.txt:242` `sprite_font_test`, `:429-434` spritefont oracles; AM4-150) | Narrow to DIRECTX9 and FNA3D (not re-checked) and drop the retired identity from the title. |
| **CNA-GAP-009** | sub-pixel SpriteBatch only on EasyGL and SOFTWARE; METAL truncates | **STALE for METAL** (AM4-136: float Draw overload; `spritebatch_subpixel_contract_test` passes) | Narrow: remove METAL (and the retired identity) from the list; others not re-checked. |
| **CNA-BUG-192** | metal-macos-ci push path filter names 3 missing CMake files and omits the Metal test registration files | **CURRENT** (`cmake/BackendLibraries.cmake`, `cmake/Examples.cmake`, `cmake/Tests/MetalTests.cmake` are absent at TARGET; the paths list was not changed by AM4-234/247/255/279/283/306) | Keep; update "macos-14" wording if present (now macos-26). |
| **CNA-BUG-133** | METAL (and the D3D renderers) never RegisterForWindow | **CURRENT** for METAL (no `RegisterForWindow` under `modules/renderers/metal` at TARGET) | Keep; drop the retired identity from the title ("DIRECTX9, DIRECTX11 and METAL…"). Same for CNA-BUG-134's text. |
| **CNA-BUG-181** | nativeFileDialog true on iOS/web | **CURRENT** (`Sdl3Platform.cpp:342`) | Keep. |
| **CNA-BUG-113** | "METAL suppresses the draw" for an empty scissor | CURRENT as a Metal statement (AM4-026 records the empty scissor drawing nothing, XNA's outcome) | Keep (Vulkan/SDL_GPU part not re-checked). |
| **CNA-VGAP-027** | no workflow runs SDL_Renderer_* tests (apple-ci runs CnaTests directly) | **CURRENT** for CI; note local M4 runs (AM4-030: 77/80 → later full SDL_RENDERER tree 10,940/10,940) | Keep; optionally add the local macOS evidence sentence. |
| **CNA-VGAP-039**, **CNA-GAP-068**, **CNA-VGAP-059** | iOS exclusions (process-spawning tests, FFmpeg, spawning tests) | **CURRENT** (`apple-platforms.md:155-162`) | Keep. |
| **CNA-BUG-163** | macOS `SO_NOSIGPIPE` not examined | CURRENT (not touched by the campaign; AM4-264 is a different SIGPIPE issue in `RunHostProcess`) | Keep. |
| **CNA-BUG-186** | "Homebrew on macOS" FFmpeg lanes | CURRENT (AM4-004 adapts the WMA encoder to FFmpeg 8; the 5.1 minimum issue is unrelated) | Keep; optionally note AM4-130 (Homebrew FFmpeg raises the deployment floor). |
| **CNA-BUG-041**, **CNA-BUG-047**, **CNA-BUG-134**, **CNA-BUG-275**, **CNA-GAP-032**, **CNA-GAP-069**, **CNA-PLAT-014** | incidental macOS/iOS/METAL mentions | OK-GENERIC for Apple (BUG-041 and BUG-134 also need the direct-platform / retired-identity policy pass, outside this worklist) | — |
| **CNA-BUG-056**, **CNA-GAP-062**, **CNA-BUG-058**, **CNA-VGAP-053** | C API (not Apple) | BUG-056: CURRENT but "abi.h declares 0.44.0" → 0.46.0 (`FEATURE_MATRIX.md` still says 0.1.0); GAP-062 / BUG-058: 656 → 631; VGAP-053: CURRENT (no workflow sets `CNA_BUILD_C_API`) | Update numbers in source. |


---

# Part 5 — Long tail (198 pages)

> Worklist B — Apple / macOS / iOS / Metal refresh of 198 pages (CNA b0e97bb1 → c1c316b9)

Research only; nothing was built or run. Line numbers are **HEAD (7f0dbaa) line numbers** (`git show HEAD:<path>`).
Authorities: `audit/data/facts/c1c316b9/R2-apple-m4.md` (cited R2 §n), `R3-c-api-cna-net.md` (R3 §n), and CNA at `c1c316b9`
(cited `file:line`). Every CNA claim below was re-checked with `git show c1c316b9:<path>` where a file is named.

Conventions
- **STALE** = must change. A row tagged **[policy-c]** or **[R3]** is a C ABI / CNA.NET occurrence that sits on one of *my* pages (not an
  Apple claim) — listed so nothing is missed; dedupe with the C-API/CNA.NET sweep. **[policy-a]/[policy-b]** in the "why" column means
  the same sentence also carries a retired renderer / direct-platform claim, and the replacement fixes it.
- "Partition" items: CMake's partition list is still *named* `CNA_RENDERER_MACOS_ONLY` with label "macOS"
  (`cmake/RendererCombinations.cmake:25,50-51`), but the host gate now admits METAL on macOS **and iOS/iPadOS**
  (`cmake/RendererSelection.cmake:136-144`, "CNA: METAL renderer targets macOS and iOS only."). These are minor STALE items.
- Replacements keep the evidence type explicit: **local physical Mac mini M4** (not CI), **iOS Simulator (iPhone 17 profile)**, **build-only**
  device, **CI configured, no green post-campaign run recorded**.

### Reusable verified facts (paste-consistent wording)

| Topic | Wording to reuse | Source |
|---|---|---|
| Host | a physical Mac mini M4 (Apple M4, 16 GB, macOS 27.0.1, Xcode 27, Apple clang 21) | R2 §1 |
| macOS full trees | every renderer tree passed in full on the Mac mini M4 with the console locked (on-screen presentation not observed): METAL 11,015, SOFTWARE 11,084, OPENGL33 11,916, SDL_GPU 10,962, WEBGPU 10,968, FNA3D 10,875, SDL_RENDERER 10,940 — 0 failures, skips by name | R2 §2.1, AM4-208, `docs/apple-platforms.md:201-215` |
| METAL verdict | SUPPORTED, explicitly *not* primary-production (compiled effects off by default, on-screen presentation never observed, no physical iOS device, no soak run) | R2 §2.4, AM4-159, `docs/metal-renderer.md:71-74` |
| METAL features | readback (AM4-025), occlusion queries — one open at a time, counting mode (AM4-038), SpriteBatch-scoped MSL custom effects (AM4-077), ColorWriteChannels (AM4-079/146), MRT up to 8 RT2D or RTCube-face members (AM4-097), MSAA on backbuffer/RT2D/RTCube/MRT, rounded to a supported count — the M4 does 2x/4x, not 8x (AM4-141), every uncompressed XNA surface format for Texture2D, float/half/wide render targets (AM4-142), instancing + multi-stream + base-instance (AM4-143/154), compiled XNA effects opt-in `CNA_METAL_COMPILED_EFFECTS` default OFF (AM4-144), cube and volume textures in every uncompressed format (AM4-147), DXT1/3/5 Texture2D/TextureCube (BC on every Mac, decoded RGBA8 fallback where the GPU has no BC; AM4-148), both `KHR_materials_specular` maps (AM4-085) and vertex-colour PBR (AM4-084), backbuffer depth format honoured (AM4-151) | R2 §2.4; `docs/metal-renderer.md:113-178` |
| METAL limits | custom effects are SpriteBatch-scoped MSL only (a 3D draw with one throws); backbuffer always BGRA8; `PresentInterval.Two` presents as `One`; LOD bias needs macOS/iOS 26 SDK+OS and is refused on a device measured to ignore it; packed 16-bit formats only on Apple-family GPUs; no compute/indirect draws/array slices; no DXT volume textures; no Intel Mac run | R2 §2.4, §7 |
| METAL targets | macOS and, since AM4-037, iOS/iPadOS (UIKit view path); CMake refuses it elsewhere | `docs/metal-renderer.md:12-14`; `cmake/RendererSelection.cmake:136-144` |
| iOS | allow-list `SDL_RENDERER` and `METAL` (`cmake/ApplePlatform.cmake:246-249`); `cna_ios_pixel_probe` exact on frame 1 and the 10 frames after it in 8 of 8 launches on the iOS 27 Simulator (iPhone 17 profile) (AM4-120); device `.app` final-linked, never run (no physical device, no signing identity); `-DCNA_ENABLE_NET=OFF` required (no libcurl in the iOS SDK) | R2 §3 |
| Apple CI | `apple-ci.yml` and `metal-macos-ci.yml` run on `macos-26` (Xcode 26) since AM4-255, check out sharp-runtime's matching branch instead of a pinned commit (AM4-234); `apple-ci` iOS matrix has 4 legs (SDL_RENDERER and METAL × device/simulator; the METAL simulator leg runs the pixel probe); the hosted Metal GPU is an "Apple Paravirtual device"; **no green run after the campaign's last CI change is recorded** | R2 §2.16; `.github/workflows/*.yml` at c1c316b9 |
| SDL_GPU on Apple | SDL's Metal driver; full tree 10,962/10,962 (295 skips), cna-samples 90/91 (LensFlare refused: no occlusion queries); no occlusion queries; `mip_lod_bias` ignored; GLSL/SPIR-V `ShaderEffect` capability off on Apple | R2 §2.6 |
| WEBGPU on Apple | wgpu-native v29.0.1.1 on its Metal backend; full tree 10,968/10,968 (279 skips), cna-samples 91/91; partial `MultiSampleMask` refused and occlusion counted as a boolean on Metal adapters. Pre-AM4-088 "WebGPU on macOS" numbers were skips, never GPU runs | R2 §2.5 |
| FNA3D on Apple | CNA's registered FNA3D tests on Apple pin FNA3D's Metal driver (its SDL_GPU driver on Metal); full tree 10,875/10,875; no occlusion queries on that driver; float render targets not promoted; legacy macOS GL is a GL 2.1 compatibility context | R2 §2.7, AM4-051 |
| Compiled effects default | 9 implementation families: FNA3D always + 8 default-OFF options (`CNA_EASYGL_`, `_SDL_GPU_`, `_VULKAN_`, `_WEBGPU_`, `_DIRECTX9_`, `_DIRECTX11_`, `_SOFTWARE_`, `_METAL_COMPILED_EFFECTS`); 11 of the 14 identities can run them; a default configure reports `CompiledEffects` true on FNA3D only | `git grep option(CNA_*_COMPILED_EFFECTS` at c1c316b9 |
| macOS online play | Apple's SDK libcurl 8.7.1 has no WebSocket support → the relay is refused by name (`RELAY_SECURE_WEBSOCKET_UNAVAILABLE`); Homebrew curl works | R2 §2.13, AM4-044/123 |
| macOS FFmpeg floor | Homebrew FFmpeg is built for the host macOS, so a `CNA_ENABLE_VIDEO=AUTO` binary linked against it does not start below that macOS whatever the 13.3 deployment target says; keep the floor with `CNA_ENABLE_VIDEO=OFF` or an FFmpeg built for it | R2 §2.10/§2.14, AM4-130, `docs/apple-platforms.md:73-77` |
| C ABI | 0.46.0 (experimental), encoded `0x00002E00`; C API on macOS: 119/119 in SOFTWARE and SDL_RENDERER trees, Mach-O dylib exporting exactly 3,210 `_cna_*`, static archive on macOS too; **no CI job builds it on macOS** | R3 §1-§2 |

---

## Pages with STALE items (most STALE first)

### docs/3d-rendering.html
Counts: STALE 9 · CURRENT 1 · OK-GENERIC 1

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 214 | `Direct3D 12 or Metal devices through SDL_shadercross, which the build files turn on by default on Windows and Apple (not verified on those platforms).` | SDL_GPU on SDL's Metal driver passed CNA's full tree on the M4 (R2 §2.6, AM4-208; `apple-platforms.md:207`). Default ON on Apple is still true (`cmake/RendererSelection.cmake:366-370`). | `Direct3D 12 or Metal devices through SDL_shadercross, which the build files turn on by default on Windows and Apple (on macOS, SDL's Metal driver passed CNA's full test tree on a physical Mac mini M4 &mdash; 10,962 tests, 295 named skips, local evidence, no CI lane; the Windows route has no native run).` |
| 233 | `<span class="status-badge status-partial">Declared supported; macOS only</span>` | METAL also targets iOS/iPadOS (AM4-037, `metal-renderer.md:12-14`); verdict SUPPORTED, not primary-production (AM4-159). | `<span class="status-badge status-partial">Supported on macOS and iOS; not primary-production</span>` |
| 234 | `The most conservative 3D renderer: no MSAA, multiple render targets, occlusion queries, instancing, multi-stream input, custom effects, compute or float targets; only <code>SurfaceFormat::Color</code> textures; factor-only PBR.` (+ "external validation boundary") | Every listed refusal except compute was implemented in AM4 Phase 3 (R2 §2.4, §6 rows 2-4: AM4-025/038/077/085/097/141..148); the "fresh macOS compile-and-run" boundary is superseded by the M4 run (AM4-156/159). | `Native Metal on macOS and iOS/iPadOS: MSAA (2x/4x on an M4), up to eight render targets, occlusion queries, instancing and multi-stream input, every uncompressed XNA surface format with float and half-float render targets, DXT, cube and volume textures, and full PBR including both <code>KHR_materials_specular</code> maps. Custom effects are SpriteBatch-scoped MSL only; compiled XNA effects need <code>-DCNA_METAL_COMPILED_EFFECTS=ON</code> (default <code>OFF</code>); no compute or indirect draws. Evidence: CNA's full test tree (11,015 tests) and <code>ctest -L Metal</code> 261/261 under Metal's validation layers on a physical Mac mini M4 with a locked console; on-screen presentation, a physical iOS device and a soak run are unmeasured, so CNA rates it supported, not primary-production.` |
| 303 | `<tr><td><code>FNA3D</code>, <code>DIRECTX9</code>, <code>METAL</code>, <code>HEADLESS</code>, <code>STUB</code> and the two 2D-only renderers</td><td><code>Color</code> only.</td></tr>` | METAL Texture2D stores every uncompressed format + DXT (AM4-142/148; `metal-renderer.md:155-173`); it classifies RT formats (`MetalRenderer::ClassifyRenderTargetFormatEXT`, `MetalRenderer.mm:5216`). [policy-a] "two 2D-only renderers" → only SDL_RENDERER is left. | `<tr><td><code>METAL</code></td><td>Every uncompressed format natively (float, half, <code>Rgba1010102</code>, 16-bit-norm, signed-normalized, <code>Alpha8</code>; the packed 16-bit formats only on Apple-family GPUs) and DXT1/3/5 (BC on every Mac, decoded to RGBA8 where the GPU has no BC). Render targets: <code>Color</code>, <code>Rgba1010102</code>, <code>Rg32</code>, <code>Rgba64</code> and the float and half-float formats.</td></tr><tr><td><code>FNA3D</code>, <code>DIRECTX9</code>, <code>HEADLESS</code>, <code>STUB</code> and the 2D-only <code>SDL_RENDERER</code></td><td><code>Color</code> only.</td></tr>` |
| 479 | `Not <code>OPENGLES2</code>, <code>WEBGL1</code>, <code>METAL</code>, <code>STUB</code> or the 2D-only renderers.` | METAL reports Instancing (AM4-143; `MetalPolicy.hpp:165-183`). [policy-a] OPENGLES2/WEBGL1/DIRECTX12 retired. | `Renderers that report <code>Instancing</code>: <code>OPENGLES3</code>, <code>WEBGL2</code>, <code>OPENGL33</code>, <code>VULKAN</code>, <code>WEBGPU</code>, <code>SDL_GPU</code>, <code>DIRECTX9</code>, <code>DIRECTX11</code>, <code>SOFTWARE</code>, <code>METAL</code>, and <code>FNA3D</code> (from its driver, and not with stock effects). Not <code>STUB</code> or the 2D-only <code>SDL_RENDERER</code>.` |
| 750 | `<code>METAL</code> supports volume storage but only in <code>Color</code>.` | AM4-147: cube and volume textures in every uncompressed format; DXT cube yes, DXT volume no (`metal-renderer.md:174-178`). [policy-a] same sentence lists `DIRECTX12`. | `a float LUT is constructible on <code>DIRECTX11</code>, the EasyGL identities, <code>VULKAN</code>, <code>METAL</code> and <code>SOFTWARE</code> under HiDef. <code>WEBGPU</code> supports both cube and volume storage, and <code>METAL</code> stores cube and volume textures in every uncompressed format (DXT for cubes but not for volumes, as in XNA).` |
| 787 | `It is <strong>not available</strong> on <code>OPENGLES2</code>, <code>WEBGL1</code>, <code>METAL</code> or <code>STUB</code>` | AM4-143/154. [policy-a] | `Instancing is reported by <strong>EasyGL</strong> (<code>OPENGLES3</code>, <code>WEBGL2</code>, <code>OPENGL33</code>), by <code>VULKAN</code>, <code>WEBGPU</code>, <code>SDL_GPU</code>, <code>DIRECTX9</code>, <code>DIRECTX11</code>, <code>SOFTWARE</code> and <code>METAL</code> (multi-stream and base-instance draws included), and by <code>FNA3D</code> when its selected driver has it. It is <strong>not available</strong> on <code>STUB</code>, and the 2D-only <code>SDL_RENDERER</code> has no instancing path at all.` (rest of the paragraph unchanged) |
| 791 | `They are not available on <code>METAL</code>, <code>OPENGLES2</code>, <code>WEBGL1</code> or the other 2D-only renderers.` | MRT up to 8 RT2D/RTCube-face members (AM4-097; `metal-renderer.md:116`). Cube face inside MRT works on Metal. [policy-a] | `... <code>FNA3D</code>, <code>SOFTWARE</code> (4 CPU targets) and <code>METAL</code> (up to 8 targets). They are not available on <code>STUB</code> or the 2D-only <code>SDL_RENDERER</code>. ... a cube face inside a multi-target set works on EasyGL, <code>VULKAN</code>, <code>SOFTWARE</code>, <code>FNA3D</code> and <code>METAL</code> but is refused on <code>WEBGPU</code>, <code>SDL_GPU</code> and the Direct3D renderers.` (also drop `DIRECTX12` earlier in the sentence) |
| 807 | `They are absent on <code>SDL_GPU</code>, <code>METAL</code>, <code>OPENGLES2</code>, <code>WEBGL1</code> and the 2D-only renderers.` | METAL occlusion queries (AM4-038; counting visibility mode, `MetalRenderer.mm:3859`); WebGPU on a Metal adapter is boolean (AM4-091); FNA3D's Metal driver has none (AM4-182). [policy-a] | `Queries are then available on the EasyGL identities (a real count on <code>OPENGL33</code>; only a 0-or-1 result on <code>OPENGLES3</code> and <code>WEBGL2</code>), <code>VULKAN</code> (an exact count needs the precise-occlusion feature), <code>WEBGPU</code> (a 0-or-1 result on a Metal adapter), <code>DIRECTX9</code>, <code>DIRECTX11</code>, <code>FNA3D</code> (not with its Metal driver), <code>SOFTWARE</code> and <code>METAL</code> (a real count, one query open at a time). They are absent on <code>SDL_GPU</code> and the 2D-only <code>SDL_RENDERER</code>.` |

CURRENT: 940 (METAL reports WireFrame). OK-GENERIC: 232 (row label).
Section note (non-Apple lines changed by the same campaign): the `SDL_GPU` and `WEBGPU` rows of the Texture2D format table (L301-302) are stale too — AM4-184 made SDL_GPU store Single/Vector2/Vector4/HalfSingle/HalfVector2/HalfVector4/HdrBlendable/Alpha8/Rg32/Rgba64/Rgba1010102 Texture2D, and AM4-187 made WebGPU store HdrBlendable/HalfVector4 Texture2D (both renderer-level, not Apple-only).

### docs/tutorials/80-cross-platform.html
Counts: STALE 8 · CURRENT 7 · OK-GENERIC 7

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 106 | `macOS-only: <code>METAL</code>. On iOS only <code>SDL_RENDERER</code> is on the allow-list.` | METAL targets macOS and iOS (AM4-037); iOS allow-list is SDL_RENDERER + METAL (`cmake/ApplePlatform.cmake:246-249`). [policy-a] sentence lists DIRECTX12/WEBGL1/CANVAS and "18 renderer identities". | `CNA has 14 renderer identities in total ... Windows-only renderers: <code>DIRECTX9</code>, <code>DIRECTX11</code> (two). Emscripten-only: <code>WEBGL2</code>. Apple-only: <code>METAL</code> (macOS and iOS/iPadOS). On iOS, <code>SDL_RENDERER</code> and <code>METAL</code> are on the allow-list.` |
| 122 | `Every renderer except the seven gated to Windows, Emscripten or macOS is Linux-configurable. Platform layers: <code>SDL3</code> (default), native <code>X11</code>, native <code>WAYLAND</code>, <code>TERMINAL</code>, <code>HEADLESS</code>.` | METAL gate is Apple (macOS + iOS); count changes with retirement. [policy-a][policy-b] | `Every renderer except the four gated to Windows, Emscripten or Apple targets is Linux-configurable. Platform implementations: <code>SDL3</code> (default; X11 and Wayland are reached through SDL's video drivers), <code>TERMINAL</code>, <code>HEADLESS</code>.` |
| 133 | `<td>Supported, build workflows configured</td>` | Full renderer trees now run on a physical Mac mini M4 (R2 §2.1, AM4-208). | `<td>Supported; full test trees run on a physical Mac mini M4 (local)</td>` |
| 134 | `<code>apple-ci</code> is configured to build the <code>SDL_RENDERER</code> configuration on <code>macos-14</code> automatically ... Both pin an older sharp-runtime revision, so we cannot say they currently pass` | Runners moved to `macos-26` (AM4-255); pins replaced by branch selection (AM4-234); no green post-campaign run recorded (R2 §2.16); M4 evidence is the real macOS evidence. | `On a physical Mac mini M4 (macOS 27, Xcode 27) all seven renderer trees CNA qualified on macOS &mdash; <code>METAL</code>, <code>SOFTWARE</code>, <code>OPENGL33</code>, <code>SDL_GPU</code>, <code>WEBGPU</code>, <code>FNA3D</code>, <code>SDL_RENDERER</code> &mdash; passed CNA's full test suite with no failures (local evidence, console locked, so on-screen presentation was not observed; no Intel Mac was run). In CI, <code>apple-ci</code> builds <code>SDL_RENDERER</code> on <code>macos-26</code>, runs the portable suites and launches a self-contained <code>.app</code> bundle, and <code>metal-macos-ci</code> builds <code>METAL</code> and runs its tests on the hosted runner's paravirtual GPU; both now check out sharp-runtime's matching branch, but no green run after the latest CI changes is recorded (see <a href="../platforms.html#ci">Platform Support</a>). Deployment floor macOS 13.3. Only the <code>SDL3</code> platform layer is available.` |
| 150 | `<td><code>SDL_RENDERER</code> (the only one allowed)</td>` | iOS allow-list SDL_RENDERER + METAL (R2 §3). | `<td><code>SDL_RENDERER</code> or <code>METAL</code> (the allow-list)</td>` |
| 152 | `The Apple workflow is configured to final-link a device app and to install and launch a one-frame simulator smoke app (same sharp-runtime pin caveat); that says nothing about physical devices, input, audio or pixels.` | Simulator pixel evidence exists for METAL (AM4-120); CI has 4 iOS legs; still no device; networking must be off (AM4-105). | `<code>cmake/toolchains/ios.cmake</code> and the <code>ios</code> and <code>ios-simulator</code> presets exist (they turn networking off: the iOS SDK has no libcurl). With <code>METAL</code>, <code>cna_ios_pixel_probe</code> read back exact pixels on frame 1 and the 10 frames after it in 8 of 8 launches on the iOS 27 Simulator (iPhone 17 profile); device apps are final-linked but have never run on a physical iPhone or iPad, so device pixels, touch, audio, storage and performance are unmeasured. The Apple workflow is configured for SDL_RENDERER and METAL device and simulator legs; no green run after the campaign is recorded. Deployment floor iOS 16.3. tvOS is unsupported.` |
| 195 | `# macOS native (SDL_RENDERER; METAL is the macOS-only native renderer)` | METAL also iOS. | `# macOS native (SDL_RENDERER; METAL is CNA's native Apple renderer)` |
| 199 | `# iOS (macOS host with Xcode): device and simulator presets, SDL_RENDERER only` | METAL allowed on iOS. | `# iOS (macOS host with Xcode): device and simulator presets (SDL_RENDERER, networking off);` + new line `# add -DCNA_GRAPHICS_RENDERER=METAL for the native Metal renderer` |

CURRENT: 131 (row label), 132 (macOS renderers), 151 ("Experimental" — CNA still labels iOS experimental), 161 (no FFmpeg on iOS), 197 (`-DCNA_GRAPHICS_RENDERER=METAL`), 230 (`#elif defined(__APPLE__)` save path), 290 (no SDL-free audio on macOS — Apple part current; same sentence names an SDL-free `WIN32` build [policy-b], fix in the platform sweep).
OK-GENERIC: 7, 12, 22 (meta/og/JSON-LD descriptions list macOS generically — optional: add "and iOS (experimental)"), 149 (row label), 196, 200, 201 (preset commands).

### docs/tutorials/72-backend-selection.html
Counts: STALE 8 · CURRENT 3 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 155 | `The most conservative 3D renderer: <code>SurfaceFormat::Color</code> only, no MSAA, MRT, occlusion, instancing, custom effects or compute.` … `<td>macOS only</td>` | R2 §2.4/§6; AM4-037. | `<tr><td><strong>METAL</strong></td><td>Native Apple Metal; SDL3 supplies only the window, CNA attaches its own <code>CAMetalLayer</code> view. MSAA, up to eight render targets, occlusion queries, instancing, every uncompressed surface format and DXT; custom effects are SpriteBatch-scoped MSL only, compiled XNA effects need <code>-DCNA_METAL_COMPILED_EFFECTS=ON</code>, no compute. Rated supported, not primary-production (full test tree passed on a physical Mac mini M4). See <a href="109-metal-macos.html">Tutorial 109</a>.</td><td>macOS; iOS/iPadOS (Simulator-tested)</td></tr>` |
| 159 | `<code>METAL</code> is macOS-only. The only automatic macOS lane is a <code>metal-macos-ci.yml</code> workflow ... iOS is restricted to <code>SDL_RENDERER</code> (final-link and one-frame simulator smoke coverage only)` | R2 §2.16, §3. | `<code>METAL</code> builds for macOS and iOS/iPadOS. Its evidence is a local campaign on a physical Mac mini M4 (CNA's full test tree, 11,015 tests, no failures) plus an iOS Simulator pixel probe; <code>metal-macos-ci.yml</code> builds it and runs the <code>Metal*</code> tests on a hosted paravirtual GPU, with no green run after the latest CI changes recorded. iOS allows <code>SDL_RENDERER</code> and <code>METAL</code>; no physical iPhone or iPad has run either, and tvOS remains unsupported.` |
| 216 | `The default outside Linux and Emscripten and the only renderer allowed on iOS.` | iOS allows SDL_RENDERER and METAL. | `The default outside Linux and Emscripten, and one of the two renderers allowed on iOS (with <code>METAL</code>).` |
| 242 | `<li><strong><code>METAL</code> throws.</strong> You find out immediately.</li>` | Metal accepts MSL ShaderEffects (construction does not throw; invalid source → invalid effect); a 3D draw with a custom effect throws (`docs/metal-shader-effect-contract.md:5-19`, AM4-077). | `<li><strong><code>METAL</code> takes Metal Shading Language for SpriteBatch effects only.</strong> An uncompilable source gives an invalid effect with the compiler message; a 3D draw with a custom effect throws <code>NotSupportedException</code>.</li>` |
| 268 | `<td><code>METAL</code> (conservative capability set) &mdash; or the default <code>SDL_RENDERER</code> for 2D</td>` | "Conservative" no longer accurate (R2 §2.4). | `<td><code>METAL</code> (native; turn on <code>CNA_METAL_COMPILED_EFFECTS</code> for compiled XNA effects) &mdash; or the default <code>SDL_RENDERER</code> for 2D; <code>OPENGL33</code>, <code>SDL_GPU</code>, <code>WEBGPU</code> and <code>FNA3D</code> also passed CNA's full tests on a Mac mini M4</td>` |
| 274 | `Not <code>FNA3D</code>, <code>SOFTWARE</code> (silently ignored) or the 2D-only set; <code>METAL</code> throws` | AM4-077. [policy-a] "2D-only set" → SDL_RENDERER. | `Not <code>FNA3D</code>, <code>SOFTWARE</code> (silently ignored) or <code>SDL_RENDERER</code>; <code>METAL</code> runs custom MSL in SpriteBatch only and throws on a 3D custom-effect draw` |
| 317 | `CMake rejects identities from different platform partitions (Windows-only, Emscripten-only, macOS-only)` | Partition now covers iOS too (see Conventions). | `CMake rejects identities from different platform partitions (Windows-only, Emscripten-only, Apple-only)` |
| 320 | `<code>SDL_RENDERER</code> on macOS and iOS, <code>METAL</code> on macOS` | `apple-ci.yml` iOS matrix has METAL device/simulator legs (AM4-037; workflow L218-236). [policy-a] the same paragraph names `WEBGL1`, `CANVAS`, `OPENGLES2`, "18 identities" and says no workflow names `WEBGPU` — the Emscripten bundle is now `WEBGL2;WEBGPU` (`emscripten-multi-renderer-ci.yml:131-132`). | Apple fragment: `<code>SDL_RENDERER</code> on macOS, <code>SDL_RENDERER</code> and <code>METAL</code> for iOS device and simulator, <code>METAL</code> on macOS` (no green post-campaign Apple run is recorded). Rest of the paragraph: fix in the renderer-retirement sweep. |

CURRENT: 120 (defaults on macOS/iOS = SDL_RENDERER), 154 (WEBGPU native hosts include macOS — optionally add "full test tree passed on a Mac mini M4 through wgpu-native's Metal backend"), 251 (METAL switch has no permissive default arm — true, `MetalPolicy.hpp:165-183`).

### docs/render-targets.html
Counts: STALE 7 · CURRENT 1 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 140 | `<code>RenderTargetCube</code> has real storage on the same 3D renderers (Color only on <code>METAL</code>). Multiple render targets (MRT) are real on 12 identities` | AM4-142/147 (formats), AM4-097 (MRT). [policy-a] the sentence lists "five EasyGL identities", `DIRECTX9/11/12`; MRT count becomes 11 of 14. | `<code>RenderTarget2D</code> is implemented on every 3D renderer &mdash; the three EasyGL identities, <code>VULKAN</code>, <code>WEBGPU</code>, <code>SDL_GPU</code>, <code>DIRECTX9/11</code>, <code>FNA3D</code>, <code>SOFTWARE</code> and <code>METAL</code> &mdash; and in a Color-only, depth-less form on the 2D-only <code>SDL_RENDERER</code>. <code>RenderTargetCube</code> has real storage on the same 3D renderers. Multiple render targets (MRT) are real on 11 identities, but ...` |
| 321 | `<td><code>METAL</code> (macOS-only)</td>` | AM4-037. | `<td><code>METAL</code> (macOS, iOS)</td>` |
| 324 | `Real 2D and cube targets (Color only); no MRT (a set larger than one throws), no MSAA` | AM4-097/141/142. | `<span class="status-badge status-partial">Real 2D and cube targets in Color and the float, half and wide formats; MRT up to 8 targets; MSAA (2x/4x on an M4); a multisampled cube refuses <code>SetData</code></span>` |
| 353 | `<code>FNA3D</code>, <code>DIRECTX9</code>, <code>METAL</code>, <code>HEADLESS</code> and the 2D-only renderers are in that group for render targets.` | Metal classifies RT formats (`MetalRenderer.mm:5216`): Color, Rgba1010102, Rg32, Rgba64, Single, Vector2, Vector4, HalfSingle, HalfVector2, HalfVector4, HdrBlendable (`metal-renderer.md:170-173`). [policy-a] same sentence names OPENGLES2/WEBGL1. | add `METAL` to the classifying list (`... <code>SOFTWARE</code> (all seven float/half formats) and <code>METAL</code> (<code>Rgba1010102</code>, <code>Rg32</code>, <code>Rgba64</code> and every float and half format)`) and end with: `<code>FNA3D</code>, <code>DIRECTX9</code>, <code>HEADLESS</code> and the 2D-only <code>SDL_RENDERER</code> are in that group for render targets.` |
| 401 | `It is unavailable on <code>METAL</code>, <code>STUB</code>, the 2D-only renderers and the ES2 generation (<code>OPENGLES2</code>, <code>WEBGL1</code>).` | AM4-097. [policy-a] | `MRT is real on 11 identities: the EasyGL identities (<code>OPENGLES3</code>, <code>OPENGL33</code>, <code>WEBGL2</code>), <code>VULKAN</code> (when the device allows more than one colour attachment), <code>WEBGPU</code>, <code>SDL_GPU</code>, <code>DIRECTX9</code>, <code>DIRECTX11</code>, <code>FNA3D</code>, <code>SOFTWARE</code> and <code>METAL</code> (up to 8). It is unavailable on <code>STUB</code> and the 2D-only <code>SDL_RENDERER</code>.` |
| 426 | `real on the ES3-generation EasyGL identities, VULKAN, WEBGPU, SDL_GPU, DIRECTX9/11/12, FNA3D and SOFTWARE; unavailable on METAL, the 2D-only renderers and the ES2 generation.` | AM4-097. [policy-a] | `<strong>MRT support:</strong> HiDef profile required; real on the EasyGL identities, VULKAN, WEBGPU, SDL_GPU, DIRECTX9/11, FNA3D, SOFTWARE and METAL; unavailable on STUB and SDL_RENDERER.` |
| 430 | `(<code>Color</code> only on <code>METAL</code>)` … `and <code>METAL</code> refuses any multi-target set.` | AM4-097 (cube faces may be MRT members), AM4-142/147. [policy-a] DIRECTX12. | `Cube targets have real storage on every 3D renderer with render targets, and are limited to ... A cube <em>face</em> can be one member of a multi-target set on the EasyGL identities, <code>VULKAN</code>, <code>SOFTWARE</code>, <code>FNA3D</code> and <code>METAL</code>; <code>DIRECTX9/11</code>, <code>SDL_GPU</code>, <code>WEBGPU</code> and <code>HEADLESS</code> refuse it.` |

CURRENT: 322 (`Metal texture` storage cell).
Section note: L321-325 row should also state MSAA resolve per encoder boundary and that a multisampled RenderTargetCube refuses `SetData` (AM4-147) if the row lists limits.

### docs/effects.html
Counts: STALE 5 · CURRENT 1 · OK-GENERIC 2

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 347 | `<code>METAL</code> is factor-only (no specular textures, and it refuses vertex-colour PBR draws)` | AM4-084 (vertex-colour PBR accepted), AM4-085 (both specular maps sampled); inventory test lists metal under "sampling" (`modules/content/tests/CNA/Internal/GltfImport/GltfRendererPbrFallbackPolicyTests.cpp:1224-1225`). [policy-a] same sentence: DIRECTX12, "five EasyGL identities", "11 identities". | `PBR support is broad but not universal: <code>DIRECTX9</code>, <code>DIRECTX11</code>, the three EasyGL identities, <code>SDL_GPU</code>, <code>VULKAN</code>, <code>WEBGPU</code> and <code>METAL</code> (9 identities, seven implementation families) implement the full model, both <code>KHR_materials_specular</code> maps and vertex-colour PBR included; <code>SOFTWARE</code> draws a reduced CPU cross-check (base colour multiplied by diffuse); <code>FNA3D</code> refuses PBR draws by name.` |
| 411 | `<tr><td><code>METAL</code></td><td>Not supported: <code>CompiledEffects</code> is false.</td></tr>` | AM4-144: opt-in `CNA_METAL_COMPILED_EFFECTS`, default OFF (`cmake/RendererSelection.cmake:342-355`). | `<tr><td><code>METAL</code></td><td><code>-DCNA_METAL_COMPILED_EFFECTS=ON</code> (default <code>OFF</code>): MojoShader's SPIR-V output translated to MSL in process by SPIRV-Cross (both fetched at configure time). Measured on a physical Mac mini M4: 43 Metal tests and 1,237 effect and SpriteBatch tests.</td></tr>` |
| 483 | `<span class="status-badge status-partial">Stock effects, factor-only PBR</span>` | AM4-085/084/077/144. | `<span class="status-badge status-partial">Stock effects, full PBR; SpriteBatch MSL effects; compiled effects opt-in</span>` |
| 484 | `macOS-only. No <code>ShaderEffect</code> and no compiled effects; cannot be built or tested on Linux CI.` | AM4-037/077/144; evidence now local M4 (AM4-156/159). | `macOS and iOS/iPadOS. A <code>ShaderEffect</code> takes Metal Shading Language and runs only in <code>SpriteBatch</code> (a 3D draw with one throws); compiled XNA effects need <code>-DCNA_METAL_COMPILED_EFFECTS=ON</code>. It cannot be built on Linux; its evidence is a local run on a physical Mac mini M4 (CNA's full test tree and <code>ctest -L Metal</code> 261/261 under Metal's validation layers).` |
| 604 | `<code>FNA3D</code>, <code>METAL</code> and <code>SOFTWARE</code> report <code>CustomEffects</code> false` | Metal reports CustomEffects true (`MetalPolicy.hpp:177`; `metal-shader-effect-contract.md:8`). [policy-a] the paragraph also names OPENGLES2/WEBGL1/DIRECTX12/CANVAS. | `... HLSL on <code>DIRECTX9/11</code>, and Metal Shading Language on <code>METAL</code> (SpriteBatch effects only). <code>FNA3D</code> and <code>SOFTWARE</code> report <code>CustomEffects</code> false; ...` |

CURRENT: 459 (SDL_GPU: shadercross default on Windows and Apple). OK-GENERIC: 376 ("Metal source" as a non-Effect format), 482 (row label).
Section note: the compiled-effects table (L403-413) also lists `OPENGLES2`, `WEBGL1`, `DIRECTX12` [policy-a]; after the fix it should read FNA3D always + 8 options, 11 of 14 identities.

### docs/tutorials/62-mrt.html
Counts: STALE 5 · CURRENT 0 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 105 | `So do <code>METAL</code> (any multi-target set throws <code>NotSupportedException</code>) and <code>STUB</code>` | AM4-097: up to 8 RT2D or RTCube-face members (`metal-renderer.md:116`). [policy-a] sentence starts with OPENGLES2/WEBGL1. | `<code>STUB</code> has no MRT, and the 2D-only <code>SDL_RENDERER</code> throws on 3D calls, including <code>SetRenderTargets</code> with more than one binding. <code>METAL</code> binds up to eight targets.` |
| 141 | `<tr><th scope="row"><code>METAL</code>, <code>STUB</code></th><td>No</td><td>&mdash;</td></tr>` | AM4-097. | `<tr><th scope="row"><code>METAL</code></th><td>Yes, up to 8 (the stock effects write the first target only)</td><td>Implemented</td></tr>` + `<tr><th scope="row"><code>STUB</code></th><td>No</td><td>&mdash;</td></tr>` |
| 149 | `and <code>METAL</code> refuses any multi-target set. It is implemented on the EasyGL family (...), <code>VULKAN</code>, <code>DIRECTX11</code>, <code>DIRECTX12</code>, <code>SOFTWARE</code> and <code>FNA3D</code>` | AM4-097 (cube faces are allowed members). [policy-a] DIRECTX12. | `It is refused with <code>NotSupportedException</code> on <code>DIRECTX9</code>, <code>SDL_GPU</code> and <code>WEBGPU</code> (and with a <code>runtime_error</code> on <code>HEADLESS</code>). It is implemented on the EasyGL family (<code>OPENGLES3</code>, <code>OPENGL33</code>, <code>WEBGL2</code>), <code>VULKAN</code>, <code>DIRECTX11</code>, <code>SOFTWARE</code>, <code>FNA3D</code> and <code>METAL</code>` |
| 189 | `while <code>FNA3D</code>, <code>DIRECTX9</code>, <code>METAL</code> and <code>HEADLESS</code> are Color-only.` | AM4-142 (RT formats). [policy-a] DIRECTX12 earlier in sentence. | `... <code>SDL_GPU</code>, <code>WEBGPU</code> and <code>SOFTWARE</code> probe them and <code>METAL</code> accepts every float, half and wide render-target format, while <code>FNA3D</code>, <code>DIRECTX9</code> and <code>HEADLESS</code> are Color-only.` |
| 305 | `// HiDef is necessary but not sufficient: OPENGLES2, WEBGL1, METAL,` / `// STUB and the 2D-only renderers have no MRT at all.` | AM4-097. [policy-a] | `// HiDef is necessary but not sufficient: STUB and the 2D-only` / `// SDL_RENDERER have no MRT at all.` |

### docs/tutorials/114-pbr-materials.html
Counts: STALE 4 · CURRENT 0 · OK-GENERIC 2

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 311 | `Seven renderer implementation families implement the universal PBR draw parameters, plus <code>METAL</code> with two documented gaps` | Both gaps closed: AM4-084 (vertex colour), AM4-085 (specular maps). [policy-a] "all 18 public identities". | `Seven renderer implementation families implement the universal PBR draw parameters (<code>METAL</code> among them since CNA's Apple campaign), plus a reduced CPU cross-check and one renderer that refuses. This table lists all 14 public identities; ...` |
| 318 | `<tr><td><span class="status-badge status-partial">Specular maps partial</span></td><td><code>METAL</code></td><td>Consumes the IOR and specular factors but not the two optional <code>KHR_materials_specular</code> maps.</td><td>No.</td></tr>` | AM4-085 (`Metal_PbrDualUvSpecular` 8/8). | delete the row and add `<code>METAL</code>` to the "Full PBR" row (L317); keep its last-column answer "No" for METAL (no shadow/IBL sampling in the Metal source). |
| 319 | `Refuses the coloured stride-60/80 PBR draw instead of accepting it with wrong colour semantics.` | AM4-084 (`Metal_PbrVertexColour` 5/5). | delete the row. |
| 327 | `(eight directories: the seven full families and METAL; SOFTWARE is added separately)` | Metal is a full family now. [policy-a] the D3D12 family is retired. | `(seven directories, all full families now that METAL samples both maps; SOFTWARE is added separately)` |

OK-GENERIC: 154, 209 ("metal" as a material).
Section note: L317's Full-PBR row lists DIRECTX12/OPENGLES2/WEBGL1 [policy-a]; corrected row: `DIRECTX9`, `DIRECTX11`, `OPENGLES3`, `OPENGL33`, `WEBGL2`, `SDL_GPU`, `VULKAN`, `WEBGPU`, `METAL` (seven families, nine identities), last column "Honoured on ... ; not on METAL".

### docs/runtime-renderer-selection.html
Counts: STALE 4 (2 [policy-c]) · CURRENT 1 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 141 | `The experimental C API (ABI <code>0.44.0</code>) exposes the same selection surface` | [policy-c] R3 §1. | `The experimental C API (ABI <code>0.46.0</code>) exposes the same selection surface` |
| 145 | `<li>Windows-only, Emscripten-only and macOS-only identities cannot cross target-toolchain partitions.</li>` | METAL partition covers iOS too (Conventions). | `<li>Windows-only, Emscripten-only and Apple-only (<code>METAL</code>) identities cannot cross target-toolchain partitions.</li>` |
| 156 | link label `What CNA&#x27;s C ABI 0.44.0 version checks admit` | [policy-c] | `What CNA&#x27;s C ABI 0.46.0 version checks admit` |
| 169 | link label `CNA-BUG-190: ... enters common/d3d and the Metal renderer target only when the default identity matches` | Fixed at c1c316b9 by RRC-027 `71a0e7313` "enter common/d3d and build the Metal renderer on membership, not the default" (`modules/renderers/CMakeLists.txt:137-148`). Not in R2/R3. | Mirror the known-issues owner's decision for CNA-BUG-190 (mark fixed/remove the link). |

CURRENT: 123 (METAL needs its own window kind).

### docs/xna-compatibility.html
Counts: STALE 3 · CURRENT 6 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 352 | `<strong>Qualification is Linux-only</strong> (...); Windows, macOS, a real wide-area network and avatar pixels on Direct3D and Metal are not qualified` | macOS networking/Guide/server suites ran on the M4 (R2 §2.11-2.13, §5: AM4-043 ENet 81/81 + TwoProcessLoopback 8/8, AM4-086/090 Guide UI 130/130 on Metal, AM4-200 304 networking cases, cna-gamer-services-server 46/46 with 9 skips, `apple-platforms.md:223`). Loopback only; SDK libcurl refuses the relay. Note: CNA's own `docs/gamer-services-known-limitations.md:80,581-583` still says "no macOS host exists" (CNA-internal staleness). | `<li><strong>Qualification is mainly Linux</strong> (CNA&rsquo;s recorded runs: 649 GamerServices and 524 Net tests passed). On macOS the networking, Guide and server suites passed locally on a physical Mac mini M4 over loopback, and online play there needs a libcurl with WebSocket support such as Homebrew&rsquo;s (Apple&rsquo;s system libcurl 8.7.1 is refused by name); Windows, a real wide-area network and avatar pixels on Direct3D and Metal are not qualified, and browser builds have no service, relay or voice.</li>` |
| 404 | `seven (eleven identities: DirectX 9/11/12, the five EasyGL identities, SDL_GPU, Vulkan and WebGPU) sample the specular texture maps as well, Metal is factor-only` | AM4-085; inventory `GltfRendererPbrFallbackPolicyTests.cpp:1224-1225`. [policy-a] | `<code>PbrEffect</code> and <code>SkinnedPbrEffect</code> are real glTF 2.0 metallic-roughness implementations. Seven implementation families (nine identities: DirectX 9/11, the three EasyGL identities, SDL_GPU, Vulkan, WebGPU and Metal) implement the model, specular texture maps included, and the Software renderer is a separate reduced CPU cross-check. FNA3D refuses PBR draws by name.` |
| 489 | `<strong>iOS support is narrow and experimental</strong> &mdash; CI final-links an SDL_RENDERER device application and launches a one-frame simulator smoke test.` | R2 §3 (AM4-037/105/120). | `<li><strong>iOS support is narrow and experimental</strong> &mdash; <code>SDL_RENDERER</code> and <code>METAL</code> are allowed; with <code>METAL</code> a pixel probe read back exact frames in 8 of 8 launches on the iOS 27 Simulator (iPhone 17 profile), and device apps are final-linked but have never run on a physical iPhone or iPad, so device pixels, input, audio, storage and performance are unmeasured. Networking must be configured off (<code>-DCNA_ENABLE_NET=OFF</code>). tvOS remains unsupported.</li>` |

CURRENT: 260, 340 (×2) (FFmpeg on Linux/macOS, never on iOS), 280, 369 (sensors on macOS desktop), 483 (no video on iOS).

### docs/tutorials/61-occlusion-query.html
Counts: STALE 3 · CURRENT 0 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 105 | `(<code>SDL_GPU</code> and <code>METAL</code> throw from the factory itself). <code>OPENGLES2</code> and <code>WEBGL1</code> <strong>lose occlusion queries entirely</strong>; so do <code>SDL_GPU</code> ..., <code>METAL</code> and <code>STUB</code>` | AM4-038 (counting slots per encoder, one query open at a time); FNA3D's Metal driver has none (AM4-182). [policy-a] | `... or when the renderer&rsquo;s factory returns nothing (<code>SDL_GPU</code> throws from the factory itself). <code>SDL_GPU</code> (its vendored SDL_gpu has no query API) and <code>STUB</code> have no occlusion queries, nor does <code>FNA3D</code> on its Metal driver, and the 2D-only <code>SDL_RENDERER</code> throws on 3D calls. <code>METAL</code> counts samples, with one query open at a time (a second <code>Begin</code> is refused).` |
| 138 | `<tr><th scope="row"><code>SDL_GPU</code>, <code>METAL</code>, <code>STUB</code></th><td>No (the constructor throws)</td><td>&mdash;</td></tr>` | AM4-038; `MetalRenderer.mm:3859` (`MTLVisibilityResultModeCounting`). | `<tr><th scope="row"><code>METAL</code></th><td>Yes (one query open at a time)</td><td>A real tally (Metal&rsquo;s counting visibility mode)</td></tr><tr><th scope="row"><code>SDL_GPU</code>, <code>STUB</code></th><td>No (the constructor throws)</td><td>&mdash;</td></tr>` |
| 274 | `// HiDef is not enough on its own: OPENGLES2, WEBGL1, SDL_GPU, METAL` / `// and STUB have no queries.` | AM4-038. [policy-a] | `// HiDef is not enough on its own: SDL_GPU, STUB and FNA3D's Metal` / `// driver have no queries. Fall back to "always visible".` |

Section note: the `WEBGPU` row ("Exact", non-Apple line) should add "a 0-or-1 flag on a Metal adapter (wgpu-native's Metal backend)" (AM4-091); the `FNA3D` row should add "not on its Metal driver" (AM4-182).

### docs/tutorials/67-deferred-rendering.html
Counts: STALE 3 · CURRENT 0 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 106 | `<code>OPENGLES2</code> and <code>WEBGL1</code> lose MRT entirely, so do <code>METAL</code> and <code>STUB</code>` | AM4-097 (MRT), AM4-077 (custom effects SpriteBatch-only), AM4-146 (compiled pixel shaders write MRT attachments 1..3). [policy-a] | `<code>STUB</code> has no MRT, and the 2D-only <code>SDL_RENDERER</code> has no 3D pipeline at all. <code>METAL</code> has MRT (up to eight targets) but runs a custom <code>ShaderEffect</code> only in <code>SpriteBatch</code>, so this G-buffer pass cannot be written as one there; a compiled XNA effect can fill the extra targets when <code>CNA_METAL_COMPILED_EFFECTS=ON</code>.` |
| 138 | `<tr><th scope="row"><code>OPENGLES2</code>, <code>WEBGL1</code>, <code>METAL</code>, <code>STUB</code></th><td>No</td><td>&mdash;</td><td>Not available</td></tr>` | as above. [policy-a] | `<tr><th scope="row"><code>METAL</code></th><td>Yes, up to 8</td><td>Metal Shading Language, <code>SpriteBatch</code> effects only</td><td>Not available (a 3D draw with a custom effect throws)</td></tr><tr><th scope="row"><code>STUB</code></th><td>No</td><td>&mdash;</td><td>Not available</td></tr>` |
| 152 | `<code>Color</code> only on <code>FNA3D</code>, <code>DIRECTX9</code>, <code>METAL</code> and <code>HEADLESS</code>` | AM4-142. [policy-a] `DIRECTX11/12` in the same parenthesis. | `(probed on the GL family, <code>VULKAN</code>, <code>DIRECTX11</code>, <code>SDL_GPU</code>, <code>WEBGPU</code> and <code>SOFTWARE</code>, accepted by <code>METAL</code>; <code>Color</code> only on <code>FNA3D</code>, <code>DIRECTX9</code> and <code>HEADLESS</code>)` |

### docs/tutorials/65-msaa.html
Counts: STALE 3 · CURRENT 0 · OK-GENERIC 1

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 100 | `<code>OPENGLES2</code>, <code>WEBGL1</code> and <code>METAL</code> have none ... covers all 18 identities` | AM4-141 (`metal-renderer.md:115`). [policy-a] | `Renderer support differs sharply: <code>OPENGLES3</code>, <code>VULKAN</code> and <code>METAL</code> implement MSAA, <code>STUB</code> has none, and <code>SDL_RENDERER</code> accepts the flag and ignores it; the table under <a href="#renderer-support">Renderer Support</a> covers all 14 identities.` |
| 208 | `<tr><th scope="row"><code>METAL</code>, <code>STUB</code></th><td>No (one sample per pixel)</td><td>Clamped to none</td><td>No</td></tr>` | AM4-141: per-device answer (`MetalRenderer.mm:6464-6469`), rounding via `supportsTextureSampleCount:`, `GetAppliedMultiSampleCountEXT` override (`MetalRenderer.hpp:93-111`). | `<tr><th scope="row"><code>METAL</code></th><td>Yes, where the device multisamples (every Metal GPU does at 4x)</td><td>Rounded down to a count the device accepts (an M4: 2 or 4, not 8); also for <code>RenderTarget2D</code>, <code>RenderTargetCube</code> and MRT</td><td>Yes</td></tr><tr><th scope="row"><code>STUB</code></th><td>No (one sample per pixel)</td><td>Clamped to none</td><td>No</td></tr>` |
| 317 | `<code>FNA3D</code>, <code>SOFTWARE</code> and <code>METAL</code> report <code>CustomEffects</code> false.` | AM4-077. | `... and <code>FNA3D</code> and <code>SOFTWARE</code> report <code>CustomEffects</code> false; on <code>METAL</code> the pass must be written in Metal Shading Language and drawn through <code>SpriteBatch</code>, the only place Metal runs a custom effect.` |

OK-GENERIC: 168 (Apple M-series GPU performance advice).

### docs/tutorials/151-one-shader-several-renderers.html
Counts: STALE 3 · CURRENT 0 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 68 | `<code>FNA3D</code>, <code>METAL</code>, <code>SOFTWARE</code>, <code>STUB</code>, the two 2D-only renderers, and <code>SDL_GPU</code> builds without libshaderc. Ask <em>before</em> constructing: <code>METAL</code> throws from the constructor.` | Metal: CustomEffects true; construction never throws (`metal-shader-effect-contract.md:5-19`). [policy-a] "two 2D-only renderers". | `<code>FNA3D</code>, <code>SOFTWARE</code>, <code>STUB</code>, the 2D-only <code>SDL_RENDERER</code>, and <code>SDL_GPU</code> builds without libshaderc. <code>METAL</code> answers true but runs a custom effect only in <code>SpriteBatch</code>, written in Metal Shading Language; a 3D draw with one throws.` |
| 190 | `//    METAL throws from the ShaderEffect constructor.` | as above; note `ExecutesShaderEffectSourceEXT()` stays false on Metal (`metal-shader-effect-contract.md:17-18`), so step 2 of this sample returns None there anyway. | `//    (METAL answers true but runs MSL only, and only in SpriteBatch.)` and add `METAL` to the step-2 comment: `//    ignore), on VULKAN (takes SPIR-V words), on DIRECTX9, on FNA3D and on METAL.` |
| 296 | `<tr><td><code>FNA3D</code>, <code>METAL</code>, <code>SOFTWARE</code>, <code>HEADLESS</code>, <code>STUB</code></td><td>fallback</td><td>not possible with source (...)</td></tr>` | AM4-077/144. | `<tr><td><code>METAL</code></td><td>fallback</td><td>an MSL variant for <code>SpriteBatch</code> draws only; or compiled effect bytecode with <code>CNA_METAL_COMPILED_EFFECTS=ON</code> (<a href="128-compiled-xna-effects.html">Tutorial 128</a>)</td></tr><tr><td><code>FNA3D</code>, <code>SOFTWARE</code>, <code>HEADLESS</code>, <code>STUB</code></td><td>fallback</td><td>not possible with source (FNA3D can run compiled effect bytecode instead: <a href="128-compiled-xna-effects.html">Tutorial 128</a>)</td></tr>` |

### deep-dives/graphics/shader-routes-four-answers.html
Counts: STALE 3 · CURRENT 1 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 200 | `<tr><td><code>METAL</code></td><td>none: construction throws <code>NotSupportedException</code></td><td>none; 3D custom-effect draws are also refused until adapted macOS evidence exists</td></tr>` | AM4-077; `metal-shader-effect-contract.md:5-28`. | `<tr><td><code>METAL</code></td><td>Metal Shading Language, one stage function per string, each compiled as its own runtime <code>MTLLibrary</code>; an uncompilable source gives an invalid effect carrying the Metal compiler&rsquo;s message</td><td><code>SpriteBatch</code> only (<code>Metal_SpriteBatch_CustomEffect</code>, 10/10 on a Mac mini M4); a 3D draw with a custom effect throws <code>NotSupportedException</code>, as on Direct3D 11 and Vulkan</td></tr>` |
| 230 | `A renderer may still throw from its own factory (Metal does), so this is not a promise that every setup failure becomes a boolean.` | Metal construction no longer throws; it throws from the draw when a valid effect's pipeline cannot be built (`metal-shader-effect-contract.md:46-49`). | `A renderer may still throw later &mdash; Metal throws from the draw when a valid effect&rsquo;s pipeline cannot be built, or when a 3D draw uses a custom effect &mdash; so this is not a promise that every setup failure becomes a boolean.` |
| 300 | `METAL cannot be built on Linux and its refusals are read from source.` | Behaviour changed and is now measured on the M4. | `METAL cannot be built on Linux; its behaviour here is read from source and from CNA&rsquo;s recorded Mac mini M4 runs.` |

CURRENT: 194 (SDL_GPU GLSL via libshaderc never on Apple). Section note: L186 lists the compiled-effects options; at c1c316b9 the eight are EasyGL, Vulkan, SDL_GPU, WebGPU, Software, DirectX 9, DirectX 11 **and Metal** (`CNA_METAL_COMPILED_EFFECTS`), with `CNA_DIRECTX12_COMPILED_EFFECTS` gone [policy-a].

### deep-dives/graphics/state-objects.html
Counts: STALE 3 · CURRENT 3 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 195 | `(a Direct3D 9 render-state failure, or Metal refusing an unsupported write mask)` | AM4-079: ColorWriteChannels are honoured, so a write mask is no longer refused; a sampler-state refusal that remains is a non-zero LOD bias Metal cannot apply (AM4-034/099/296). | `(a Direct3D 9 render-state failure, or Metal refusing a sampler LOD bias it cannot apply)` |
| 205 | `Metal throws <code>NotSupportedException</code> for anything but all-channel writes and the default sample mask;` | AM4-079/146/141. [policy-a] the next clause describes Canvas. | `Metal honours render target 0&rsquo;s <code>ColorWriteChannels</code> (and <code>ColorWriteChannels1..3</code> for the attachments a compiled pixel shader writes) and applies a partial <code>MultiSampleMask</code> on a multisampled target through the stock fragment&rsquo;s sample mask, refusing it only for a custom MSL effect;` (drop the Canvas clause) |
| 277 | `Metal throws <code>NotSupportedException</code> for non-default values.` | AM4-034 (MaxMipLevel → `lodMinClamp`, bias → `lodBias`), AM4-099 (SDK gate), AM4-296 (device probe). [policy-a] same cell: "EasyGL's ES 2.0 and WebGL 1 profiles". | `Metal maps <code>MaxMipLevel</code> to the sampler&rsquo;s <code>lodMinClamp</code> and the bias to <code>lodBias</code>, which needs the macOS/iOS 26 SDK and OS; below that, or on a device measured to ignore the bias, a non-zero bias throws <code>NotSupportedException</code>.` |

CURRENT: 209, 245 (Metal stencil reference / scissor), 279 (anisotropy clamp 1–16).

### development/workflows.html
Counts: STALE 3 (2 [policy-c]/[R3]) · CURRENT 2 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 165 | `The ABI is 0.44.0 at this snapshot and experimental.` | [policy-c] R3 §1. | `The ABI is 0.46.0 at this snapshot and experimental.` |
| 166 | `The C# binding (CNA.NET, <code>libcna/cna-cs</code>) is a separate repository that admits exactly one ABI version (0.44.0 at <code>860f92c</code>)` | [R3] rename to cna-dotnet (R3 §3.1); cna-dotnet admitted 0.46.0, never 0.45.0 (AM4-217, R3 §3.2 — sibling SHA not verified locally, so cite none). | `The C# binding (CNA.NET, <code>libcna/cna-dotnet</code>) is a separate repository that admits exactly one ABI version (0.46.0; its compatibility review skipped 0.45.0);` |
| 262 | `The Apple, Emscripten, devices and content-pipeline workflows instead check out sharp-runtime at a fixed commit, and static reading of those files suggests that some pin a revision older than the snapshot needs` | AM4-234: all five now run `scripts/ci/sibling_branch.sh` (`apple-ci.yml:100-111`, `metal-macos-ci.yml:50-58`, `emscripten-multi-renderer-ci.yml:56-67`, `devices-tests.yml:99-103`, `content-pipeline-windows-ci.yml:39-45`). | `The Apple, Emscripten, devices and content-pipeline workflows check out sharp-runtime themselves, but through <code>scripts/ci/sibling_branch.sh</code>, which picks the same branch <code>clone_siblings.sh</code> would instead of the fixed commits they used to pin.` |

CURRENT: 256 (apple-ci/metal-macos-ci triggers — optional: "macOS and iOS (SDL_RENDERER and METAL) builds with portable suites and an iOS Simulator pixel probe"), 270 (CNA-BUG-192 link — the Metal workflow's push filter still names the three removed files at c1c316b9, `metal-macos-ci.yml:5-24`).

### development/reference/cmake-options.html
Counts: STALE 3 · CURRENT 10 · OK-GENERIC ~36 (src-link paths `cmake/ApplePlatform.cmake`/`AppleSmoke.cmake` and option names on L135; L144 link label)

All on the single table line 135.

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 135 | `<td><code>CNA_RENDERER_METAL</code></td><td>option</td><td><code>OFF</code></td><td>Enable native Apple Metal graphics renderer (macOS only)</td>` | The docstring is quoted verbatim and is **still "(macOS only)" in CNA at c1c316b9** (`cmake/RendererSelection.cmake:35`) — a CNA-internal stale docstring; the gate admits macOS and iOS (`RendererSelection.cmake:136-144`). | Keep the verbatim docstring if the table is generated, but add after it: `<br><small>The docstring predates iOS support: the configure gate accepts <code>METAL</code> for macOS and iOS/iPadOS.</small>` (or a sentence above the table). |
| 135 | `<td><code>CNA_APPLE_IOS_RENDERERS</code></td><td>cache internal</td><td><code>SDL_RENDERER</code></td>` | `cmake/ApplePlatform.cmake:246-249` sets `"SDL_RENDERER" "METAL"` (AM4-037). | `<td><code>CNA_APPLE_IOS_RENDERERS</code></td><td>cache internal</td><td><code>SDL_RENDERER;METAL</code></td>` |
| 135 | (missing row) | New option `CNA_METAL_COMPILED_EFFECTS` (`cmake/RendererSelection.cmake:347-348`, AM4-144). | insert after `CNA_MAX_VENDORED_BUILD_JOBS`: `<tr><td><code>CNA_METAL_COMPILED_EFFECTS</code></td><td>option</td><td><code>OFF</code></td><td>Build Metal support for compiled XNA Effect bytecode (plans/plan_apple_m4.md AM4-144)</td><td><a class="src-link" href="https://github.com/libcna/cna/blob/c1c316b9c7a846ce8002809c151fcd1af14942c9/cmake/RendererSelection.cmake"><code>cmake/RendererSelection.cmake</code></a></td></tr>` |

CURRENT: `CMAKE_OSX_DEPLOYMENT_TARGET`, `CNA_APPLE_ALLOW_UNVALIDATED_RENDERER`, `CNA_APPLE_BUNDLE_IDENTIFIER_PREFIX`, `CNA_APPLE_BUNDLE_MACOS_EXECUTABLES`, `CNA_APPLE_BUNDLE_VERSION`, `CNA_APPLE_DEVELOPMENT_TEAM`, `CNA_BUILD_APPLE_SMOKE_APP` (docstring unchanged; it now also builds `cna_*_pixel_probe`, `cmake/AppleSmoke.cmake:24-36`), `CNA_IOS_DEPLOYMENT_TARGET` 16.3, `CNA_IOS_SIMULATOR`, `CNA_MACOS_DEPLOYMENT_TARGET` 13.3.
Section note: the table must be regenerated at c1c316b9 anyway — it still lists `CNA_RENDERER_CANVAS/DIRECTX12/OPENGLES2/WEBGL1` and `CNA_DIRECTX12_COMPILED_EFFECTS` [policy-a]; the delta also adds `CNA_C_API_DOXYGEN` (FILEPATH, AM4-160; pins Doxygen 1.9.x for the C API coverage gates).

### development/testing/architecture.html
Counts: STALE 3 (2 [policy-c]) · CURRENT 3 · OK-GENERIC 3

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 279 | `A host-portable Apple CMake check; a macOS build with <code>SDL_RENDERER</code> and portable suites; an iOS device final link and a simulator launch of one frame; native Metal contract tests.` / `No physical-device or pixel-correctness claim.` | iOS matrix now has METAL device/simulator legs and the METAL simulator leg runs `cna_ios_pixel_probe` (`apple-ci.yml:218-236,288`); runners `macos-26`; no green post-campaign run recorded (R2 §2.16). Path-filter sentence is still true (`metal-macos-ci.yml:5-24`). | `<td>A host-portable Apple CMake check; a <code>macos-26</code> build with <code>SDL_RENDERER</code>, portable suites and a launched <code>.app</code> bundle; iOS device final links and Simulator launches for <code>SDL_RENDERER</code> and <code>METAL</code>, the <code>METAL</code> Simulator leg reading pixels back (<code>cna_ios_pixel_probe</code>); the native Metal tests (<code>ctest -R '^Metal'</code>) on the hosted runner&rsquo;s paravirtual GPU.</td><td>No physical-device claim, and no green run after the latest CI changes is recorded; CNA&rsquo;s macOS runtime evidence is its local Mac mini M4 qualification, not these jobs. The Metal workflow&rsquo;s push path filter still names three CMake files ...</td>` (rest unchanged) |
| 344 | link label `How far the evidence for CNA&#x27;s C ABI 0.44.0 reaches, ... for the 656 unmapped symbols` | [policy-c] R3 §1: 0.46.0; RELEASE_GATE "631 public symbols are still unmapped". | `How far the evidence for CNA&#x27;s C ABI 0.46.0 reaches, what each release-gate criterion really checks, what the gate reports for the 631 unmapped symbols, ...` |
| 377 | link label `What CNA&#x27;s C ABI 0.44.0 version checks admit` | [policy-c] | `What CNA&#x27;s C ABI 0.46.0 version checks admit` (60 headers is still right at c1c316b9) |

CURRENT: 165 (multi-process tests excluded on iOS), 173 (Apple sources outside CnaTests), 431 (CNA-BUG-192 link — still true). OK-GENERIC: 342, 350, 365 (link labels naming Apple/METAL generically).

### deep-dives/build/configuring-cna.html
Counts: STALE 3 · CURRENT 3 · OK-GENERIC 6

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 138 | `AppleClang on macOS 14` | Workflows run on `macos-26` (Xcode 26); macos-14's Xcode 15.4 lacks `std::jthread`/`std::stop_token`, so it no longer builds CNA with gamer services (`metal-macos-ci.yml:38-40`, AM4-255). | `AppleClang from Xcode 26 on <code>macos-26</code>` |
| 152 | `<td><code>SDL_RENDERER</code> (the only allowed one)</td><td>static</td><td>no tests; a smoke app is final-linked</td>` | iOS allow-list SDL_RENDERER + METAL; pixel probe (AM4-037/120; `cmake/AppleSmoke.cmake:24-36`). | `<td><code>SDL_RENDERER</code> (<code>METAL</code> is the other allowed one)</td><td>static</td><td>no <code>CnaTests</code>; a smoke app and a pixel probe are final-linked, and the Simulator runs the probe for <code>METAL</code></td>` |
| 175 | `macOS builds natively with the default <code>SDL_RENDERER</code> or the macOS-only <code>METAL</code>; iOS ... is restricted to <code>SDL_RENDERER</code> unless <code>CNA_APPLE_ALLOW_UNVALIDATED_RENDERER=ON</code>` | R2 §2.1, §3; iOS needs `CNA_ENABLE_NET=OFF` (AM4-105). | `macOS builds natively with the default <code>SDL_RENDERER</code> or with <code>METAL</code>, <code>OPENGL33</code>, <code>SDL_GPU</code>, <code>WEBGPU</code>, <code>FNA3D</code> or <code>SOFTWARE</code>, each of which passed CNA&rsquo;s full test suite on a physical Mac mini M4 (Vulkan through MoltenVK is not covered); iOS goes through <code>ios.cmake</code> with <code>CNA_IOS_SIMULATOR</code> choosing the SDK, is restricted to <code>SDL_RENDERER</code> and <code>METAL</code> unless <code>CNA_APPLE_ALLOW_UNVALIDATED_RENDERER=ON</code>, needs <code>-DCNA_ENABLE_NET=OFF</code> (the iOS SDK has no libcurl), links SDL statically (...), and builds the smoke application and pixel probe instead of tests.` (rest unchanged) |

CURRENT: 139 (static archives on macOS/iOS), 142 (`ios.cmake` toolchain), 151 (macOS route row). OK-GENERIC: 7, 13, 19 (meta/og/JSON-LD "Apple routes"), 124 (TOC), 134 (lede), 174 (heading).

### docs/tutorials/02-setup.html
Counts: STALE 3 · CURRENT 3 · OK-GENERIC 2

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 118 | `macOS with AppleClang on <code>macos-14</code>` | AM4-255 (`macos-26`). | `macOS with AppleClang (Xcode 26) on <code>macos-26</code>` |
| 172 | `Install Xcode or the Command Line Tools (AppleClang; CI uses <code>macos-14</code>), then <code>brew install cmake ninja ccache</code> ... <code>METAL</code> is the macOS-only native renderer.` | macos-26 (AM4-255); nlohmann-json needed while networking is on (AM4-247, `cmake/HeaderOnlyJson.cmake:30`); Homebrew FFmpeg floor (AM4-130); METAL also iOS; other renderers measured on M4. | `Install Xcode or the Command Line Tools (AppleClang; CI uses Xcode 26 on <code>macos-26</code> &mdash; the older Xcode 15.4 libc++ lacks <code>std::jthread</code>, which gamer services use), then <code>brew install cmake ninja ccache nlohmann-json</code> (nlohmann-json 3.11 or newer is required while networking is on; add <code>ffmpeg</code> for video, but Homebrew&rsquo;s FFmpeg is built for your own macOS version, so a binary linked against it will not start on an older one). The deployment target defaults to macOS 13.3 and cannot be lowered. The default renderer on macOS is <code>SDL_RENDERER</code> (2D only); <code>METAL</code> is CNA&rsquo;s native Apple renderer, and <code>OPENGL33</code>, <code>SDL_GPU</code>, <code>WEBGPU</code>, <code>FNA3D</code> and <code>SOFTWARE</code> also passed CNA&rsquo;s full test suite on a physical Mac mini M4. The bundled preset is <code>cmake --preset macos</code>.` |
| 213 | `CNA&rsquo;s CI workflows pin specific sharp-runtime revisions for the Emscripten and Apple jobs (through <code>-DCNA_SHARP_RUNTIME_ROOT=&hellip;</code>), which is what to fall back on if a newer sharp-runtime ever breaks configure.` | AM4-234: workflows now pick a sharp-runtime branch via `scripts/ci/sibling_branch.sh` (workflow lines cited under development/workflows.html L262). The `git checkout b0e97bb1…` in the same paragraph is handled by the global pin move. | `CNA&rsquo;s CI workflows no longer pin sharp-runtime: the Emscripten and Apple jobs check out the branch <code>scripts/ci/sibling_branch.sh</code> chooses (the pushed, source or target branch, then <code>next</code>), so there is no recorded fallback revision to copy if a newer sharp-runtime ever breaks configure.` |

CURRENT: 124 (macOS 13.3 floor; iOS experimental), 132 (FFmpeg never built for iOS), 295 (`macos`, `ios` presets). OK-GENERIC: 171 (heading), 358 (`--parallel` on macOS).

### development/internals/graphics/selection.html
Counts: STALE 3 · CURRENT 4 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 184 | `the three Direct3D identities require a Windows target; <code>METAL</code> requires macOS; the browser identities require Emscripten; the three native GL-profile identities refuse Emscripten` | Gate: "METAL renderer targets macOS and iOS only" (`RendererSelection.cmake:136-144`). [policy-a] counts after retirement: DIRECTX9/DIRECTX11, WEBGL2, OPENGLES3/OPENGL33. | `the two Direct3D identities require a Windows target; <code>METAL</code> requires macOS or iOS; <code>WEBGL2</code> requires Emscripten; the two native GL-profile identities refuse Emscripten` |
| 277 | `the platform partition (Windows-only, Emscripten-only and macOS-only identities cannot share a binary)` | see Conventions (partition list still named MACOS_ONLY in CMake). | `the platform partition (Windows-only, Emscripten-only and Apple-only identities cannot share a binary; CMake names the Apple partition "macOS")` |
| 304 | link label `CNA-BUG-190: modules/renderers/CMakeLists.txt enters common/d3d and the Metal renderer target only when the default identity matches ...` | Fixed by RRC-027 `71a0e7313` (`modules/renderers/CMakeLists.txt:137-148`). Not in R2/R3. | Mirror the known-issues owner's decision for CNA-BUG-190 (fixed at c1c316b9). |

CURRENT: 172 (Apple gate in the macro), 187 (`modules/renderers/metal` entered unconditionally — still true, `modules/renderers/CMakeLists.txt:137-148`), 241 (`Metal` window kind), 243 (only Metal sets `wantsHighDpi`).

### development/takeover/uncertainty.html
Counts: STALE 3 (all [policy-c]/[R3]) · CURRENT 2 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 164 | `The C ABI is 0.44.0 (<a ...><code>abi.h</code></a>), 60 public headers, 3,210 exported routes` | [policy-c] R3 §1 (60 headers and 3,210 routes unchanged). Optional: add the macOS C API run (R3 §2: 119/119 in SOFTWARE and SDL_RENDERER trees, local; no CI job builds it on macOS). | `The C ABI is 0.46.0 (<a ...><code>abi.h</code></a>), 60 public headers, 3,210 exported routes` |
| 165 | `The maintained C# binding (CNA.NET, <code>libcna/cna-cs</code>) is a separate project that admits exactly ABI 0.44.0, the version this snapshot exports. ... each refuses 0.44.0 or was never qualified against it.` | [R3] §3.1 rename; §3.2 AM4-217 admits 0.46.0. | `The maintained C# binding (CNA.NET, <code>libcna/cna-dotnet</code>) is a separate project that admits exactly ABI 0.46.0, the version this snapshot exports. ... none was qualified against 0.46.0.` |
| 179 | `at this snapshot (ABI 0.44.0) the maximum is 43, <code>FNA3D</code>, set by 0.33.0` | [policy-c] R3 §1 (maximum stays 43, next new value 52). | `at this snapshot (ABI 0.46.0) the maximum is 43, <code>FNA3D</code>, set by 0.33.0` |

CURRENT: 163 (18 workflow files incl. Apple cells — count still 18 at c1c316b9; the same cell's "Win32 cross-build under Wine" is [policy-b]), 174 (teardown test excluded on iOS; same sentence names native X11/Wayland/Win32 [policy-b]).

### docs/tutorials/100-shipping.html
Counts: STALE 2 · CURRENT 3 · OK-GENERIC 2

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 124-125 | `<td>Linux and macOS builds</td>` / `... the shipped binary links FFmpeg runtime libraries, so bundle them (AppImage handles this) and account for their licences.` | Understated: on macOS a Homebrew FFmpeg raises the minimum macOS of the shipped binary (AM4-130, `docs/apple-platforms.md:73-77`). | append to the L125 cell: ` On macOS, Homebrew&rsquo;s FFmpeg is built for the macOS it was installed on, so a binary linked against it will not start on an older macOS whatever <code>CNA_MACOS_DEPLOYMENT_TARGET</code> (13.3) says; ship with <code>-DCNA_ENABLE_VIDEO=OFF</code> or an FFmpeg built for your floor.` |
| 135 | `<strong>iOS support is narrow and experimental</strong>: the Apple workflow is configured to final-link an SDL_RENDERER device app and launch a one-frame simulator smoke path, but does not establish physical-device or pixel correctness; ... on EasyGL-family, Vulkan, WebGPU, Software, DirectX 9/11/12 and SDL_GPU builds` | R2 §3 (AM4-037/120); compiled effects now also on METAL (AM4-144). [policy-a] DirectX 12. | `<strong>iOS support is narrow and experimental</strong>: <code>SDL_RENDERER</code> and <code>METAL</code> build for device and Simulator, and with <code>METAL</code> a pixel probe read back exact frames on the iOS 27 Simulator, but no physical iPhone or iPad has run CNA, so device pixels, touch, audio and performance are unmeasured, and there is no <code>.ipa</code> or App Store packaging; tvOS is unsupported. <strong>Compiled effects are renderer-qualified</strong>: XNA/FNA D3D9 Effect Framework bytecode works on FNA3D and, when the matching <code>*_COMPILED_EFFECTS</code> option is switched on, on EasyGL-family, Vulkan, WebGPU, Software, DirectX 9/11, SDL_GPU and Metal builds (a default configure enables it on FNA3D only).` |

CURRENT: 119 (no video on iOS), 164 (SDL shared on macOS), 324 (CI matrix "not exhaustive ... physical iOS hardware" — Apple part current; the paragraph's "18 identities", native X11/Win32 lanes are [policy-a]/[policy-b]). OK-GENERIC: 22 (JSON-LD "no video off Linux/macOS" — still right), 306 (`elseif(APPLE)` CPack sample).
Section note: no Apple-signing/notarization caveat exists on this page; optional addition: "CNA has no signing or notarization step for macOS bundles; `CNA_APPLE_BUNDLE_MACOS_EXECUTABLES=ON` produces `.app` bundles you sign after the dependency fixup (`docs/apple-platforms.md:89-91`)".

### docs/shader-effects.html
Counts: STALE 2 · CURRENT 3 · OK-GENERIC 1

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 483 | `<td>None: throws <code>NotSupportedException</code></td>` | AM4-077; `metal-shader-effect-contract.md:5-19`. | `<td>Metal Shading Language, one stage function per string, for <code>SpriteBatch</code> only (a 3D draw with a custom effect throws <code>NotSupportedException</code>); an uncompilable source leaves the effect invalid with the Metal compiler&rsquo;s message</td>` |
| 484 | `<td><span class="status-badge status-wip">unavailable</span></td>` | as above. | `<td><span class="status-badge status-partial">executes in SpriteBatch</span> (<code>ExecutesShaderEffectSourceEXT()</code> stays false: it concerns the GLSL the engine writes)</td>` |

CURRENT: 448 (SDL_GPU GLSL never on Apple), 504 (shipped sample shaders have no MSL variant, so "not on METAL" is still right), 515 (`ExecutesShaderEffectSourceEXT` false on METAL). OK-GENERIC: 482 (row label).

### docs/tutorials/152-graphics-profiles.html
Counts: STALE 2 · CURRENT 0 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 135 | `<tr><th scope="row"><code>METAL</code></th><td>no</td><td>no</td><td>no</td><td>yes</td></tr>` | Columns: MRT, OcclusionQuery, float/half RTs, Texture3D. AM4-097/038/142; FloatRenderTargets/HalfFloatRenderTargets are derived from Vector4/HdrBlendable RT support (`GraphicsDevice.cpp:3466-3469`). | `<tr><th scope="row"><code>METAL</code></th><td>yes (up to 8)</td><td>yes; a real count, one query open at a time</td><td>yes</td><td>yes</td></tr>` |
| 142 | `(the ES2-generation GL identities, <code>METAL</code>)` | METAL now has the HiDef features. [policy-a] the ES2 identities are retired. | `A game that stays inside Reach can therefore run on renderers that have none of the right-hand features (<code>STUB</code>, and the 2D-only <code>SDL_RENDERER</code> for 2D games); a game that asks for HiDef and uses MRT will not.` |

### docs/tutorials/64-cubemaps.html
Counts: STALE 2 · CURRENT 0 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 176 | `<code>FNA3D</code>, <code>SOFTWARE</code> and <code>METAL</code> cannot run a custom shader at all` | Metal runs custom MSL only in SpriteBatch, so a custom cube-map shader for 3D is still unavailable — reason changed (AM4-077). [policy-a] same sentence: OPENGLES2/WEBGL1/DIRECTX12. | `<code>FNA3D</code> and <code>SOFTWARE</code> cannot run a custom shader at all, and <code>METAL</code> runs one only in <code>SpriteBatch</code>; for them use the stock <code>EnvironmentMapEffect</code> (<a href="56-environment-map.html">Tutorial 56</a>) where the renderer supports it.` |
| 420 | `<tr><th scope="row"><code>METAL</code></th><td>Yes, <code>Color</code> only</td><td>No</td></tr>` | AM4-147 (every uncompressed format for cubes), AM4-148 (DXT cube: BC on every Mac, decoded RGBA8 fallback). | `<tr><th scope="row"><code>METAL</code></th><td>Yes, every uncompressed format</td><td>Blocks kept compressed where the GPU has BC (every Mac); decoded to RGBA8 beside the kept blocks where it has none (an iPhone GPU)</td></tr>` |

### docs/tutorials/52-custom-shaders.html
Counts: STALE 2 · CURRENT 1 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 342 | `<li><strong><code>METAL</code> throws</strong> (<code>NotSupportedException</code>). You find out at the call site, which is the behaviour you want.</li>` | AM4-077: construction never throws; MSL SpriteBatch effects; 3D draw throws. | `<li><strong><code>METAL</code> takes Metal Shading Language, for <code>SpriteBatch</code> only.</strong> An uncompilable source gives an invalid effect with the compiler&rsquo;s message; a 3D draw with a custom effect throws <code>NotSupportedException</code> at the call site.</li>` |
| 368 | `<code>METAL</code> throws, <code>FNA3D</code> returns an invalid effect` | as above. | `... HLSL compiled at run time on the Direct3D renderers, and Metal Shading Language on <code>METAL</code> (SpriteBatch only; a 3D draw with one throws). <code>FNA3D</code> returns an invalid effect, and <code>SOFTWARE</code> and <code>HEADLESS</code> accept it and never execute it.` |

CURRENT: 332 (SDL_GPU GLSL never on Apple).

### docs/tutorials/66-bloom.html
Counts: STALE 2 · CURRENT 0 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 105 | `<code>FNA3D</code>, <code>SOFTWARE</code> and <code>METAL</code> report <code>CustomEffects</code> false, so the hand-written route is unavailable on them.` | Metal: CustomEffects true for SpriteBatch MSL — bloom's passes are SpriteBatch draws, so an MSL port is possible; note `SetUniformFloatArray`/`Vec2Array` are not implemented on Metal (`metal-shader-effect-contract.md:44-45`). [policy-a] CANVAS earlier in paragraph. | `<code>FNA3D</code> and <code>SOFTWARE</code> report <code>CustomEffects</code> false, so the hand-written route is unavailable on them; on <code>METAL</code> it needs an MSL port of each pass, drawn through <code>SpriteBatch</code>, and the blur weights cannot use the array setters, which Metal does not implement.` |
| 126 | `<tr><th scope="row"><code>FNA3D</code>, <code>SOFTWARE</code>, <code>METAL</code></th><td>Not available: <code>CustomEffects</code> is false</td><td><code>SOFTWARE</code> has float targets but cannot run the shaders; the others have none</td></tr>` | Metal float targets (AM4-142) and SpriteBatch MSL (AM4-077). | `<tr><th scope="row"><code>METAL</code></th><td>Needs an MSL port, drawn through <code>SpriteBatch</code> (no array uniform setters)</td><td>Yes (<code>HdrBlendable</code> and the float and half formats)</td></tr><tr><th scope="row"><code>FNA3D</code>, <code>SOFTWARE</code></th><td>Not available: <code>CustomEffects</code> is false</td><td><code>SOFTWARE</code> has float targets but cannot run the shaders; <code>FNA3D</code> has none</td></tr>` |

### development/internals/modules/gamer-services.html
Counts: STALE 2 · CURRENT 1 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 154 | `Windows and macOS clients, real wide-area networks, Guide sounds heard by a person and avatar pixels on DirectX, Metal, OPENGLES2, FNA3D and SDL_RENDERER remain unverified.` | macOS client/server suites ran on the M4 (R2 §2.11-2.13, §5; AM4-043/086/090/200; `apple-platforms.md:223`). [policy-a] OPENGLES2. | `CNA also records a local macOS run on a physical Mac mini M4 (networking, Guide and companion-server suites over loopback; online play there needs a libcurl with WebSocket support). Windows clients, real wide-area networks, Guide sounds heard by a person and avatar pixels on DirectX, Metal, FNA3D and SDL_RENDERER remain unverified.` |
| 273 | `how the Guide behaves on Windows and macOS windowing platforms ... CNA's own records state them as unqualified.` | Guide/gamer-services UI tests 130/130 on Metal on the M4 (AM4-086/090); CNA's `gamer-services-known-limitations.md:80,581-583` still says no macOS host (CNA-internal staleness — the plan is the newer record). | `how the Guide behaves on Windows windowing platforms (on macOS CNA records its Guide and gamer-services UI suite passing on a Mac mini M4, 130/130 on METAL, not a person&rsquo;s session), and whether its sounds and voice are heard through real devices were not verified here.` |

CURRENT: 260 (a green local suite does not establish Windows/macOS client behaviour — still a fair general caveat).

### development/internals/graphics/sdl-gpu.html
Counts: STALE 2 · CURRENT 7 · OK-GENERIC 1

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 155 | `Driver-specific live validation remains open: no workflow selects SDL_GPU, Direct3D 12 evidence is a Wine/vkd3d-proton route, and Metal has none recorded here.` | SDL_GPU on SDL's Metal driver: full tree 10,962/10,962 on the M4 (R2 §2.6). | `Driver-specific live validation is uneven: no workflow selects SDL_GPU, Direct3D 12 evidence is a Wine/vkd3d-proton route, and the Metal driver's evidence is CNA's local Mac mini M4 qualification (full test tree, 10,962 tests, 295 named skips; no occlusion queries, <code>mip_lod_bias</code> ignored).` |
| 332 | link label `CNA-VGAP-025: No CI workflow selects WEBGPU or SDL_GPU; ... SDL_GPU&#x27;s Direct3D 12 and Metal driver routes have no native execution evidence` | Metal route now has local native evidence (R2 §6 row "SDL_GPU's Metal driver route…"); and the Emscripten workflow builds `WEBGL2;WEBGPU` (`emscripten-multi-renderer-ci.yml:131-132`). | Mirror the known-issues owner's rewrite of CNA-VGAP-025 (Metal route: local M4 evidence, still no CI job selects SDL_GPU). |

CURRENT: 166 (driver diagram), 172 (`CNA_SDL_GPU_SHADERCROSS` ON on Windows and Apple — `RendererSelection.cmake:366-370`), 174 (no shaderc on APPLE), 175 (`cocoa`/`uikit` test video driver), 220 (SPIR-V intake/compute answer true for any device — still in source, `SdlGpuRenderer.cpp:2865-2871`), 269, 327 (CNA-BUG-094 link — still true). OK-GENERIC: 315 (link label).

### development/internals/graphics/backends.html
Counts: STALE 2 · CURRENT 3 · OK-GENERIC 1

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 178 | `<td>macOS only; Objective-C++ and Apple frameworks; SDL3 supplies the window and <code>CAMetalLayer</code></td>` | AM4-037 (iOS/UIKit); the renderer adds its own `CAMetalLayer`-backed view to the SDL window (`metal-renderer.md:5-10`). | `<td>macOS and iOS/iPadOS; Objective-C++ and Apple frameworks; SDL3 supplies the window (<code>NSWindow</code> or <code>UIWindow</code>) and the renderer attaches its own <code>CAMetalLayer</code>-backed view</td>` |
| 228 | `<strong>A Metal test that nothing builds.</strong> <code>metal_spritebatch_customeffect_test.cpp</code> is referenced by no CMake file. It asserts a custom-effect path that <code>MetalRenderer::CreateEffectRenderer</code> refuses at this snapshot` | Registered as `cna_test_metal_spritebatch_customeffect` (`modules/renderers/metal/examples/CMakeLists.txt:85`); passes 10/10 under validation layers (AM4-077). | Delete the bullet, or replace with: `<li><strong>Metal tests run only on Apple hosts.</strong> The Metal family's tests (for example <code>metal_spritebatch_customeffect_test.cpp</code>, registered as <code>Metal_SpriteBatch_CustomEffect</code>) need a Mac; their recorded results are CNA's local Mac mini M4 runs and the hosted <code>metal-macos-ci</code> job.</li>` |

CURRENT: 166 (SDL_GPU shadercross default ON on Apple), 177 (wgpu-native for macOS), 245 (page-scope caveat; same sentence says "18 identities" [policy-a]). OK-GENERIC: 270 (link label).

### development/build/index.html
Counts: STALE 2 · CURRENT 2 · OK-GENERIC 1

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 228 | `(the Windows-only Direct3D identities, the browser-only <code>WEBGL1</code>, <code>WEBGL2</code> and <code>CANVAS</code>, the macOS-only <code>METAL</code>)` | Partition (Conventions). [policy-a] WEBGL1/CANVAS. | `(the Windows-only Direct3D identities, the browser-only <code>WEBGL2</code>, the Apple-only <code>METAL</code>)` |
| 230 | `Windows-only, macOS-only or browser-only renderers off their target` | Partition/gate. | `Windows-only, Apple-only or browser-only renderers off their target` |

CURRENT: 176 (`cmake-build-ios-sim`), 191 (Apple presets: Release `SDL_RENDERER`, iOS presets with networking off — matches `CMakePresets.json` at c1c316b9). OK-GENERIC: 299 (link label).

### contribute.html
Counts: STALE 2 · CURRENT 2 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 218 | `nine renderer families: FNA3D always, and eight opt-in build options (EasyGL, Vulkan, WebGPU, Software, DIRECTX9, DIRECTX11, DIRECTX12, SDL_GPU), so a default configure reports <code>CompiledEffects</code> as unsupported on 17 of 18 identities ... (for example Metal and Canvas)` | Metal has the opt-in now (AM4-144). [policy-a] DIRECTX12, Canvas, 18 identities. | `... CNA/FNA D3D9 Effect Framework bytecode on nine renderer families: FNA3D always, and eight opt-in build options (EasyGL, Vulkan, WebGPU, Software, DIRECTX9, DIRECTX11, SDL_GPU, Metal), so a default configure reports <code>CompiledEffects</code> as unsupported on 13 of 14 identities (it is true on FNA3D only). The open work is to add real sample runtime evidence on more of those renderers, or build an explicit conversion strategy for different inputs such as DXBC and MGFX.` |
| 266 | `CNA has automatic macOS/Metal coverage (a macOS-14 build plus the supported Metal contract tests) and experimental iOS final-link plus simulator-smoke coverage. CNA's own Metal page treats fresh native macOS compile-and-run validation of the adapted source as an external gate. Useful contributions include that validation, ... beyond its <code>SDL_RENDERER</code>-only boundary.` | R2 §2.1, §2.4, §2.16, §3, §7. | `CNA&rsquo;s macOS evidence is a local campaign on a physical Mac mini M4, where all seven renderer trees CNA qualified there (<code>METAL</code>, <code>SOFTWARE</code>, <code>OPENGL33</code>, <code>SDL_GPU</code>, <code>WEBGPU</code>, <code>FNA3D</code>, <code>SDL_RENDERER</code>) passed the full test suite; its CI configures <code>macos-26</code> Apple and Metal jobs (no green run after the latest changes is recorded) and iOS device and Simulator builds for <code>SDL_RENDERER</code> and <code>METAL</code>, with a Simulator pixel probe. Useful contributions: a run on a physical iPhone or iPad, an Intel Mac run, on-screen presentation and <code>PresentInterval</code> pacing observed on an unlocked Mac, a soak run of the Metal renderer, and a green hosted macOS CI run.` |

CURRENT: 254 (18 workflow files incl. Apple — Apple part fine; "Wine-executed Win32 lane" [policy-b]), 312 (CI exercises AppleClang).

### deep-dives/renderers/presentation-and-backbuffer-readback.html
Counts: STALE 2 · CURRENT 4 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 202 | `and Metal always reports <code>Depth24Stencil8</code>.` | AM4-151: backbuffer takes `PresentationParameters.DepthStencilFormat` at creation and on Reset; Depth16 native (`MetalRenderer.hpp:120-133`; `metal-renderer.md:114`). [policy-a] DirectX 12, Canvas in the paragraph. | `..., SDL_GPU, Software and Vulkan report what they allocated, and Metal reports the requested <code>DepthFormat</code>, which its backbuffer now honours (<code>None</code> has no planes, <code>Depth16</code> is stored as 16-bit).` |
| 223 | `<tr><td>Explicit refusal</td><td><code>HEADLESS</code>, <code>METAL</code>, <code>STUB</code></td><td>... Metal throws because a historical macOS run returned clear-colour-only data; Stub inherits the throwing default</td></tr>` | AM4-025: readback in logical backbuffer coordinates (Retina/letterbox), throws while a render target is bound (`metal-renderer.md:130-134`). | Move METAL to the reading families: `<tr><td>Explicit refusal</td><td><code>HEADLESS</code>, <code>STUB</code></td><td>Headless throws ... ; Stub inherits the throwing default</td></tr>` and add to the implementing rows: `<code>METAL</code> reads the drawable through the logical viewport (Retina scale and letterbox included) after completing the pending pass; it throws while a render target is bound.` |

CURRENT: 144, 229 (page-scope "macOS families were not run" — true for this page's own method), 173, 194 (`PresentInterval.Two` behaves as One on Metal — still recorded, AM4-139).

### development/repository/module-graph.html
Counts: STALE 2 · CURRENT 4 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 230 | `Two helpers are entered from conditions that test the <em>default</em> identity rather than list membership: <code>common/d3d</code> (default DIRECTX11 or DIRECTX12) and the Metal family target (default METAL).` | Fixed by RRC-027 `71a0e7313`: "enter common/d3d and build the Metal renderer on membership, not the default" (`modules/renderers/CMakeLists.txt:137-151`). Not in R2/R3. | `Two helpers are entered on list membership: <code>common/d3d</code> whenever <code>DIRECTX11</code> is selected, and the Metal family target whenever <code>METAL</code> is selected (the header-interface target is always defined).` (drop the rest of the bullet) |
| 264 | link label `CNA-BUG-190: ...` | as above. | Mirror the known-issues owner's decision for CNA-BUG-190 (fixed). |

CURRENT: 176 (Inspector configure error on iOS), 203 (×2: `metal` family; `cna_renderer_metal_headers` always defined), 226 (FFmpeg never on iOS).

### development/repository/index.html
Counts: STALE 2 (both [policy-c]) · CURRENT 4 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 224 | `The experimental C ABI (0.44.0; public headers held to a C99 consumer floor` | [policy-c] | `The experimental C ABI (0.46.0; public headers held to a C99 consumer floor` |
| 241 | `60 plain-C headers with their own version (ABI 0.44.0, experimental)` | [policy-c] | `60 plain-C headers with their own version (ABI 0.46.0, experimental)` |

CURRENT: 157 (`ApplePlatform`, iOS toolchain), 158 (`apple/` smoke app — it now also holds `apple_pixel_probe.cpp`; optional "Apple smoke application and pixel probe"), 162 (26 jobs over Linux, macOS, iOS ... — job count not re-verified; "MinGW under Wine" ok), 192 (Metal header interface).

### deep-dives/reference/glossary.html
Counts: STALE 2 (1 [policy-c]) · CURRENT 1 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 142 | `The version of CNA's experimental native C interface: 0.44.0 at this snapshot. ... (no CI job builds it)` | [policy-c] R3 §1; R3 §2: built and tested locally on macOS, still no CI job builds it on macOS. | `The version of CNA's experimental native C interface: 0.46.0 at this snapshot. It moves independently of the product version and is not a statement that the C library builds in CI.` |
| 206 | `<dd>The macOS-only native renderer and the most conservative 3D one.</dd>` | AM4-037; Phase 3 (R2 §2.4). | `<dd>CNA&rsquo;s native Apple renderer for macOS and iOS/iPadOS, rated supported but not primary-production.</dd>` |

CURRENT: 210 (SDL_GPU GLSL never on Apple).

### deep-dives/foundations/compatibility-and-evidence.html
Counts: STALE 2 · CURRENT 0 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 157 | `<td>Native Linux, a Wine prefix, headless Chromium, a macOS-14 runner, an iOS simulator</td>` | Runners `macos-26`; physical Mac mini M4 is now an execution host (R2 §1, AM4-255). | `<td>Native Linux, a Wine prefix, headless Chromium, a <code>macos-26</code> runner, a physical Mac mini M4, an iOS Simulator</td>` |
| 195 | `(<code>METAL</code> is the most conservative)` | R2 §2.4. [policy-a] same row: "five EasyGL profiles", `DIRECTX12`. | `<td>The three EasyGL profiles, <code>VULKAN</code>, <code>WEBGPU</code>, <code>DIRECTX9</code>, <code>DIRECTX11</code>, <code>SDL_GPU</code>, <code>METAL</code></td><td>3D, state and effect surface with family-specific format, shader and profile limits (<code>METAL</code> runs custom effects only in SpriteBatch)</td>` |

### docs/tutorials/168-operate-gamer-services-server.html
Counts: STALE 2 · CURRENT 0 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 63 | `Linux is the tested host; Windows and macOS builds are unvalidated.` | cna-gamer-services-server built on the M4 (Homebrew Boost 1.92/curl) and passed 46/46, 9 skip (AM4-071/178; `apple-platforms.md:223`). | `Linux is the tested host; a macOS build also passed its suite locally on a Mac mini M4 (46 tests, 9 skipped for Linux-only network namespaces and unrouted loopback aliases) with Homebrew&rsquo;s Boost and curl; Windows builds are unvalidated.` |
| 149 | `Not qualified: Windows and macOS server hosts and clients (...)` | as above, plus macOS clients via CNA harnesses (loopback only). | `<li>Not qualified: Windows server hosts and clients (the database lock and the Windows credential store were exercised under Wine only), macOS beyond one local Mac mini M4 run over loopback, a real wide-area network with NAT, voice on physical audio devices, and avatar pixels on Direct3D and Metal.</li>` |

### deep-dives/renderers/sdl-gpu-resources-and-frame-recovery.html
Counts: STALE 2 · CURRENT 0 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 144 | `Direct3D 12 evidence is a Wine and vkd3d-proton probe, and no Metal run is recorded.` | R2 §2.6 (AM4-208). | `Direct3D 12 evidence is a Wine and vkd3d-proton probe, and the Metal driver's is CNA's local Mac mini M4 qualification (full test tree, 10,962 tests).` |
| 226 | `a Direct3D 12 probe run under Wine with vkd3d-proton, and no Metal run recorded.` | as above (also check the target page `native-gpu-evidence-tiers.html#tiers`, outside my list). | `a Direct3D 12 probe run under Wine with vkd3d-proton, and a local Metal-driver run of CNA's full test tree on a physical Mac mini M4 (no CI job selects SDL_GPU).` |

### deep-dives/reference/gltf-evidence-matrix.html
Counts: STALE 2 · CURRENT 0 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 158 | `its two maps sampled by seven renderer families, not by <code>METAL</code>` | AM4-085; inventory test lists 7 sampling families incl. metal (`GltfRendererPbrFallbackPolicyTests.cpp:1224-1225`). | `its two maps sampled by every PBR renderer family (seven, <code>METAL</code> included)` |
| 184 | `CNA's plan records the broader <code>GLTF ROBUST</code> milestone at 9 of 12 rows: <code>KHR_materials_specular</code> texture sampling (only <code>METAL</code> among the current PBR renderers lacks it), native point and spot lighting, and a fourth renderer ... remain open.` | `plans/plan_gltf.md:140`: GLTF-344 "2026-10-08: METAL closed by AM4-085"; the GLTF-459 tally line (`:142`) still says 9 of 12 (not re-assessed). | `CNA's plan still records the broader <code>GLTF ROBUST</code> milestone at 9 of 12 rows, assessed before the last <code>KHR_materials_specular</code> blocker closed: <code>METAL</code> began sampling both maps on 2026-10-08. Native point and spot lighting and a fourth renderer on the bounded external retake matrix remain open.` |

### development/handbook/make-a-release.html
Counts: STALE 2 (both [policy-c]) · CURRENT 2 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 176 | `<td>Native C ABI version</td><td><code>0.44.0</code>, experimental</td>` | [policy-c] | `<td>Native C ABI version</td><td><code>0.46.0</code>, experimental</td>` |
| 229 | `compares against the C ABI (0.44.0 at TARGET)` | [policy-c]; R3 §2 AM4-210: on macOS the dylib's Mach-O compatibility/current versions also come from the ABI version. | `compares against the C ABI (0.46.0 at TARGET; on macOS the dylib&rsquo;s Mach-O compatibility and current versions are derived from it too)` |

CURRENT: 180, 237 (`CNA_APPLE_BUNDLE_VERSION` numeric components).

### development/debugging.html
Counts: STALE 2 (1 [policy-c]/[R3]) · CURRENT 1 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 257 | `The <code>CApi_Exports</code> check is ELF-only.` | AM4-209: `CApi_Exports` registered on Apple via `cmake/CheckMachOExports.cmake` (`modules/c-api/CMakeLists.txt:537-546`). | `The <code>CApi_Exports</code> check reads ELF on Linux and Mach-O on macOS (<code>nm -gU</code>); there is no Windows variant.` |
| 262 | `This snapshot exports ABI 0.44.0 (<code>cna_get_abi_version()</code>, encoded <code>0x00002C00</code> ...), which is exactly the version the maintained C# binding (CNA.NET at <code>860f92c</code>) admits; ... most of them refuse a 0.44.0 library` | [policy-c]/[R3]: 0.46.0 encodes as 46×256 = `0x00002E00` (`abi.h:34-44`); CNA.NET admits 0.46.0 (AM4-217). | `This snapshot exports ABI 0.46.0 (<code>cna_get_abi_version()</code>, encoded <code>0x00002E00</code>, ...), which is exactly the version the maintained C# binding (CNA.NET, <code>libcna/cna-dotnet</code>) admits; the eight archived bindings stopped at 0.21&ndash;0.23 or 0.35.0 and none was qualified against 0.46.0 ...` |

CURRENT: 282 (Inspector not built for iOS).

### deep-dives/sharp-runtime/parity-and-verification.html
Counts: STALE 2 (conditional on the page's sharp-runtime snapshot) · CURRENT 2 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 191 | `<tr><td><code>NetworkInterface</code> enumeration, <code>FileSystemWatcher</code></td><td>Linux (inotify for the watcher)</td><td>throw elsewhere</td></tr>` | Accurate for the page's pinned sharp-runtime `41b918c9` (pre-campaign), but CNA's campaign records a Darwin `NetworkInterface` and a **kqueue** `FileSystemWatcher` (not FSEvents) in later sharp-runtime (last commit of the series `62952ef5`, as recorded by `plan_apple_m4.md`; not present locally) and hardening (AM4-101/127) (R2 §5; `apple-platforms.md:203`). | If the page stays pinned to `41b918c9`: keep the row and add after the table: `<p>Later sharp-runtime revisions, recorded by CNA&rsquo;s Apple campaign, add Darwin backends for both: a kqueue <code>FileSystemWatcher</code> (not FSEvents) and <code>NetworkInterface</code> enumeration.</p>` If re-pinned to a post-campaign sharp-runtime: `<td>Linux (inotify) and macOS (kqueue for the watcher)</td><td>throw elsewhere</td>` |
| 193 | `... with no tests cross-built or run, and no macOS job, only fixes driven by downstream Xcode builds.` | CNA records sharp-runtime's standalone suite on the M4: 18,084 run / 18,059 passed / 0 failed / 25 skipped at `62952ef5` (independent rerun 2026-10-08) and 18,127/18,127 (25 skips) at the Phase 4 head (R2 §5, AM4-208, `apple-platforms.md:203`). Still no sharp-runtime macOS CI job is recorded. | append: `CNA&rsquo;s Apple campaign later ran sharp-runtime&rsquo;s own suite natively on a Mac mini M4 (18,127 tests passing, 25 skipped, at the head of that campaign) &mdash; a local run, not a sharp-runtime CI job.` |

CURRENT: 188 (AppDomain base directory on macOS), 239 (sharp-runtime's own workflow supplies no macOS execution — still no macOS CI recorded).

### docs/tutorials/60-instancing.html
Counts: STALE 2 · CURRENT 0 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 105 | `<code>OPENGLES2</code> and <code>WEBGL1</code> &mdash; the two lower GL profile identities &mdash; <strong>have no instancing at all</strong>, and neither do <code>METAL</code> or <code>STUB</code>` | AM4-143 (instancing with every stock effect, multi-stream), AM4-154 (base instance). [policy-a] | `<code>STUB</code> <strong>has no instancing at all</strong>, and the 2D-only <code>SDL_RENDERER</code> throws on 3D calls entirely.` |
| 139 | `<tr><th scope="row"><code>METAL</code>, <code>STUB</code></th><td>No</td><td>No</td></tr>` | Columns: stock instancing / custom-effect instancing. Metal: stock yes (AM4-143); custom effects SpriteBatch-only, so no custom instanced 3D draw. | `<tr><th scope="row"><code>METAL</code></th><td>Yes (stock effects, multi-stream and base-instance draws)</td><td>No: custom effects run only in <code>SpriteBatch</code></td></tr><tr><th scope="row"><code>STUB</code></th><td>No</td><td>No</td></tr>` |

### docs/tutorials/101-renderer-capabilities.html
Counts: STALE 1 · CURRENT 0 · OK-GENERIC 1

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 219 | `<tr><td><code>METAL</code></td><td>Thirteen named switch arms; the six newer members reach the final <code>false</code>. Seven answers are true and twelve are false of the nineteen, with no permissive true fallback.</td></tr>` | `MetalPolicy.hpp:165-183` (12 arms true, MSAA arm false but overridden per device, `MetalRenderer.mm:6464-6469`); device-derived answers `GraphicsDevice.cpp:3453-3477`: CompiledEffects via `SupportsCompiledEffects()` (built only with `CNA_METAL_COMPILED_EFFECTS`), Float/HalfFloat RT via Vector4/HdrBlendable RT classification (HiDef), half-float linear filtering true (`MetalRenderer.mm:5268-5271`), compute/indirect not overridden (false). | `<tr><td><code>METAL</code></td><td>Thirteen named switch arms with no permissive fallback: twelve answer true and <code>MultiSampleAntiAliasing</code> is answered per device (true wherever the GPU multisamples). The six newer members reach the switch&rsquo;s final <code>false</code>, but the device derives them: compiled effects are true only with <code>CNA_METAL_COMPILED_EFFECTS=ON</code>, the float and half-float render-target answers are true under HiDef, half-float linear filtering is true, and compute and indirect draws are false.</td></tr>` |

OK-GENERIC: 386 (link label).

### docs/tutorials/128-compiled-xna-effects.html
Counts: STALE 1 · CURRENT 1 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 69 | `<tr><td>Every other family (<code>METAL</code>, <code>HEADLESS</code>, <code>STUB</code>, <code>SDL_RENDERER</code>, <code>CANVAS</code>)</td><td><code>CompiledEffects</code> capability is false and cannot be enabled</td></tr>` | AM4-144 (`cmake/RendererSelection.cmake:342-355`). [policy-a] CANVAS. | `<tr><td><code>METAL</code></td><td><code>-DCNA_METAL_COMPILED_EFFECTS=ON</code> (MojoShader&rsquo;s SPIR-V output translated to MSL in process by SPIRV-Cross; measured on a physical Mac mini M4)</td></tr><tr><td>Every other family (<code>HEADLESS</code>, <code>STUB</code>, <code>SDL_RENDERER</code>)</td><td><code>CompiledEffects</code> capability is false and cannot be enabled</td></tr>` |

CURRENT: 115 (`.fx` compiled by the external fxc through wine on Linux or macOS — `.fx` compilation itself was not exercised on macOS, AM4-048).
Section note: L60 (non-Apple line) must become "Compiled effects work on 11 of the 14 renderer identities, spread over 9 implementation families. FNA3D always supports them; the other eight families need a default-OFF CMake option." and L64/L67 drop OPENGLES2/WEBGL1/DIRECTX12 [policy-a].

### docs/tutorials/87-custom-backend.html
Counts: STALE 1 · CURRENT 3 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 360 | `If your renderer cannot execute a custom <code>ShaderEffect</code>, <strong>throw</strong>, as <code>METAL</code> does (and report <code>CustomEffects</code> false).` | Metal no longer throws on construction and reports CustomEffects true (AM4-077). | `If your renderer cannot execute a custom <code>ShaderEffect</code>, report <code>CustomEffects</code> false and return no effect renderer, as <code>FNA3D</code> does, so the effect is visibly invalid; if it can execute one only in some draws, refuse the others by name, as <code>METAL</code> does for a 3D draw with a custom effect.` |

CURRENT: 260 (METAL switch with no permissive default), 313 (`Metal` window kind), 316 (Metal asks for a high-density backing).

### docs/tutorials/79-debugging.html
Counts: STALE 1 · CURRENT 0 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 133-135 | `<code>DIRECTX9/11/12</code>, <code>WEBGPU</code>, <code>SOFTWARE</code> and <code>FNA3D</code> do; <code>SDL_RENDERER</code>, <code>OPENGLES2</code>, <code>WEBGL1</code>, <code>SDL_GPU</code>, <code>METAL</code> and the 2D-only renderers refuse construction.` | AM4-038; FNA3D Metal driver has none (AM4-182). [policy-a] | `<code>DIRECTX9/11</code>, <code>WEBGPU</code>, <code>SOFTWARE</code>, <code>METAL</code> and <code>FNA3D</code> (not on its Metal driver) do; <code>SDL_GPU</code> and the 2D-only <code>SDL_RENDERER</code> refuse construction.` |

### docs/tutorials/75-lod.html
Counts: STALE 1 · CURRENT 0 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 244 | `They are absent on <code>SDL_GPU</code>, <code>METAL</code>, the ES2-generation GL identities (<code>OPENGLES2</code>, <code>WEBGL1</code>), <code>STUB</code> and both 2D-only renderers.` | AM4-038, AM4-182. [policy-a] | `They are absent on <code>SDL_GPU</code>, <code>STUB</code>, <code>FNA3D</code>&rsquo;s Metal driver and the 2D-only <code>SDL_RENDERER</code>.` |

### docs/tutorials/116-post-process-effects.html
Counts: STALE 1 · CURRENT 0 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 198 | `<code>METAL</code> and <code>FNA3D</code> report false;` | AM4-077 (`metal-shader-effect-contract.md:8-10`). | `<code>FNA3D</code> reports false; <code>METAL</code> reports true but compiles only Metal Shading Language, and runs it only in <code>SpriteBatch</code> draws;` |

### docs/tutorials/63-stencil-buffer.html
Counts: STALE 1 · CURRENT 1 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 245 | `<code>FNA3D</code>, <code>SOFTWARE</code> and <code>METAL</code> report <code>CustomEffects</code> false` | AM4-077. [policy-a] DIRECTX12 in the list; the same line later says "13 of the 18 iden…" for compiled effects → 11 of 14. | `... and <code>DIRECTX11</code> with HLSL; <code>FNA3D</code> and <code>SOFTWARE</code> report <code>CustomEffects</code> false, and <code>METAL</code> runs custom effects only in <code>SpriteBatch</code>, not in this 3D outline pass)` |

CURRENT: 132 (METAL has a stencil buffer).

### docs/tutorials/59-shadow-mapping.html
Counts: STALE 1 · CURRENT 0 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 271 | `<tr><th scope="row"><code>FNA3D</code>, <code>SOFTWARE</code>, <code>METAL</code></th><td>None: <code>CustomEffects</code> is false</td><td>Not available</td><td>No</td></tr>` | AM4-077 (Metal shadow/IBL sampling still absent — "No" stays). | `<tr><th scope="row"><code>METAL</code></th><td>Metal Shading Language, <code>SpriteBatch</code> effects only</td><td>Not available (a 3D draw with a custom effect throws)</td><td>No</td></tr><tr><th scope="row"><code>FNA3D</code>, <code>SOFTWARE</code></th><td>None: <code>CustomEffects</code> is false</td><td>Not available</td><td>No</td></tr>` |

### docs/tutorials/69-water.html
Counts: STALE 1 · CURRENT 0 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 124 | `<tr><th scope="row"><code>FNA3D</code>, <code>SOFTWARE</code>, <code>METAL</code></th><td>Not available: <code>CustomEffects</code> is false</td></tr>` | AM4-077. | `<tr><th scope="row"><code>METAL</code></th><td>Not available: Metal runs custom effects (MSL) only in <code>SpriteBatch</code>, and a 3D draw with one throws</td></tr><tr><th scope="row"><code>FNA3D</code>, <code>SOFTWARE</code></th><td>Not available: <code>CustomEffects</code> is false</td></tr>` |

### docs/tutorials/68-terrain.html
Counts: STALE 1 · CURRENT 0 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 320 | `<code>FNA3D</code>, <code>SOFTWARE</code> and <code>METAL</code> report <code>CustomEffects</code> false and stay on the <code>BasicEffect</code> path below.` | AM4-077. [policy-a] DIRECTX12 earlier in sentence. | `<code>FNA3D</code> and <code>SOFTWARE</code> report <code>CustomEffects</code> false, and <code>METAL</code> runs custom effects only in <code>SpriteBatch</code>; all three stay on the <code>BasicEffect</code> path below.` |

### docs/tutorials/24-post-processing.html
Counts: STALE 1 · CURRENT 0 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 120 | `<code>FNA3D</code>, <code>METAL</code> and <code>SOFTWARE</code> cannot run a source <code>ShaderEffect</code> at all.` | AM4-077: a full-screen post-process pass is a SpriteBatch draw, which Metal runs in MSL. [policy-a] OPENGLES2/WEBGL1/DIRECTX12 in same sentence. | `... <code>WEBGPU</code> wants WGSL, <code>DIRECTX9/11</code> want HLSL and <code>METAL</code> wants Metal Shading Language (it runs custom effects only through <code>SpriteBatch</code>, which is how this full-screen pass is drawn); <code>FNA3D</code> and <code>SOFTWARE</code> cannot run a source <code>ShaderEffect</code> at all.` |

### docs/tutorials/53-effect-parameter.html
Counts: STALE 1 · CURRENT 0 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 111 | `<code>METAL</code> throws on a custom shader, <code>FNA3D</code> hands back an invalid effect` | AM4-077; Metal's setters fill fixed slots and ignore the name (`metal-shader-effect-contract.md:40-44`). [policy-a] DIRECTX12. | `<code>METAL</code> compiles Metal Shading Language and runs it only in <code>SpriteBatch</code> (its uniform setters fill fixed slots and ignore the name), <code>FNA3D</code> hands back an invalid effect, and <code>SOFTWARE</code> and <code>HEADLESS</code> accept it and <strong>never execute it</strong>.` |

### docs/tutorials/58-normal-mapping.html
Counts: STALE 1 · CURRENT 1 · OK-GENERIC 1

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 122 | `only renderers that classify DXT formats (<code>DIRECTX11/12</code>, ... EasyGL) accept it; <code>FNA3D</code>, <code>DIRECTX9</code> and <code>METAL</code> take <code>Color</code> only.` | AM4-148 (DXT1/3/5 Texture2D: BC on every Mac, decoded fallback). [policy-a] DIRECTX12. | `only renderers that classify DXT formats (<code>DIRECTX11</code>, <code>VULKAN</code>, <code>SDL_GPU</code>, <code>WEBGPU</code> with BC support, <code>SOFTWARE</code>, EasyGL and <code>METAL</code>, which keeps the blocks compressed on every Mac) accept it; <code>FNA3D</code> and <code>DIRECTX9</code> take <code>Color</code> only.` |

CURRENT: 105 (normal maps via PBR on METAL). OK-GENERIC: 111 ("scratches in metal").

### docs/graphics-state.html
Counts: STALE 1 · CURRENT 1 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 386 | `false on <code>METAL</code>, the ES2 generation and the 2D-only renderers.` | AM4-141 (per-device answer). [policy-a] DIRECTX12, ES2 generation. | `<code>GraphicsCapability::MultiSampleAntiAliasing</code> is probed per device on EasyGL, <code>VULKAN</code>, <code>SDL_GPU</code>, <code>WEBGPU</code> (4x only), <code>DIRECTX11</code>, <code>FNA3D</code> and <code>METAL</code>; true on <code>SOFTWARE</code> (4x only) and <code>DIRECTX9</code> (inherited); false on the 2D-only <code>SDL_RENDERER</code>.` |

CURRENT: 306 (StencilBuffer true on METAL; same sentence has "five EasyGL identities", `DIRECTX9/11/12` [policy-a]).

### docs/video-playback.html
Counts: STALE 1 · CURRENT 6 · OK-GENERIC 1

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 338 | `<span class="status-badge status-partial">Decodes</span> with the backend (the optional split was not run on macOS by its author)` | Understated: Homebrew FFmpeg raises the binary's minimum macOS (AM4-130, `apple-platforms.md:73-77`). The "optional split not run on macOS" remark is still CNA's record (`docs/video-backend.md:55`). | `<span class="status-badge status-partial">Decodes</span> with the backend (the optional split was not run on macOS by its author); a Homebrew FFmpeg is built for the macOS it was installed on, so the binary will not start on an older macOS unless you link an FFmpeg built for your deployment floor` |

CURRENT: 141 ("per CNA's notes, macOS"; FFmpeg never on iOS), 151, 171, 173, 336, 337. OK-GENERIC: 357 ("the platform video player on iOS" as alternative).

### docs/tutorials/121-video-playback.html
Counts: STALE 1 · CURRENT 4 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 124 | `<td>same; the optional split itself has not been exercised on macOS by CNA&rsquo;s author</td>` | as docs/video-playback.html L338 (AM4-130). | `<td>same; the optional split itself has not been exercised on macOS by CNA&rsquo;s author, and a Homebrew FFmpeg raises the binary&rsquo;s minimum macOS to the version it was built on</td>` |

CURRENT: 112, 113, 126, 307.

### docs/tutorials/131-sdl-gpu.html
Counts: STALE 1 · CURRENT 5 · OK-GENERIC 3

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 269 | `Treat Windows and Apple as "built to work", not as CI-verified.` | R2 §2.6 (AM4-208, `apple-platforms.md:207`). | `On macOS, SDL&rsquo;s Metal driver passed CNA&rsquo;s full test tree on a physical Mac mini M4 (10,962 tests, 295 named skips; 90 of 91 cna-samples, LensFlare refused because SDL&rsquo;s GPU API has no occlusion queries) &mdash; local evidence, still not CI-verified. Treat Windows as "built to work".` |

CURRENT: 83 (Apple → SDL's Metal driver), 97, 262 (Apple row: shadercross ON), 266, 278 (ShaderEffect never available on Apple). OK-GENERIC: 68, 277, 343.

### docs/vs-alternatives.html
Counts: STALE 1 · CURRENT 1 · OK-GENERIC 5

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 199 | `narrow experimental iOS SDL_RENDERER final-link and simulator-smoke evidence. Seven platform implementations (SDL3, native X11, Wayland and Win32 with no SDL, Headless, Terminal) are independently selectable.` | R2 §2.1, §3. [policy-b] | `<td>Linux, Windows, macOS, Emscripten and Android source/build paths, with macOS measured on a physical Mac mini M4; experimental iOS (<code>SDL_RENDERER</code> and <code>METAL</code>, Simulator pixel evidence, no physical-device run). Three platform implementations (SDL3, Headless, Terminal) are independently selectable; Windows, X11, Wayland, macOS, iOS, Android and the browser are reached through SDL3.</td>` |

CURRENT: 255 (Apple workflows exist). OK-GENERIC: 186, 187, 200, 201, 236 (MonoGame/FNA columns).

### development/internals/platforms/sdl3.html
Counts: STALE 1 · CURRENT 4 · OK-GENERIC 1

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 236 | `<tr><td><code>cocoa</code></td><td><code>Cocoa</code></td><td><code>window</code></td></tr>` (table has no `uikit` row) | AM4-037: `NativeWindowSystem::UIKit` (`NativeWindowSystem.hpp:57`), SDL driver `uikit` mapped in `Sdl3Window.cpp:102`; C ABI `CNA_NATIVE_WINDOW_SYSTEM_UIKIT`=9 (R3 §1). | keep the cocoa row and insert after it: `<tr><td><code>uikit</code></td><td><code>UIKit</code></td><td><code>window</code> = <code>UIWindow*</code></td></tr>` |

CURRENT: 184 (METAL declares a Metal window), 209 (`cocoa` global mouse state), 251 (`tray` on macOS), 236 (cocoa row itself). OK-GENERIC: 286 (link label).

### development/architecture/platform.html
Counts: STALE 1 · CURRENT 0 · OK-GENERIC 1

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 168 | `which of Win32, X11, Wayland, Cocoa, Android, Web, Headless or Terminal its pointers belong to` | AM4-037 added `UIKit` (`NativeWindowSystem.hpp:57`). These name SDL video-driver handle kinds, not CNA platforms. | `which of Win32, X11, Wayland, Cocoa, UIKit, Android, Web, Headless or Terminal its pointers belong to` |

OK-GENERIC: 227 (link label).

### docs/tutorials/85-vulkan-backend.html
Counts: STALE 1 · CURRENT 0 · OK-GENERIC 4

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 151 | `<code>METAL</code> is the macOS-gated renderer and has its own macOS CI lane. CNA does not verify a MoltenVK path.` | AM4-037; evidence mostly local M4 (R2 §2.4, §2.16); MoltenVK out of scope (R2 §1, `apple-platforms.md:214`). | `<li><strong>Apple targets are served by <code>METAL</code>, not by Vulkan.</strong> <code>METAL</code> is CNA&rsquo;s native renderer for macOS and iOS, measured on a physical Mac mini M4 and built by a hosted <code>metal-macos-ci</code> job. Vulkan through MoltenVK is out of scope on Apple and not tested.</li>` |

OK-GENERIC: 7, 12 (meta/og "limits on macOS and Android"), 101, 107 (lists METAL among modern-GPU renderers; same sentence "18 renderer identities" [policy-a]).

### docs/tutorials/01-introduction.html
Counts: STALE 1 · CURRENT 3 · OK-GENERIC 1

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 148 | `Three renderers (<code>DIRECTX9</code>, <code>DIRECTX11</code> and <code>DIRECTX12</code>) are Windows-only and <code>METAL</code> is macOS-only.` | AM4-037. [policy-a] DIRECTX12 (and the preceding OPENGLES2/WEBGL1 sentence); the next sentence's "native Win32 platform module" is [policy-b]. | `Two renderers (<code>DIRECTX9</code> and <code>DIRECTX11</code>) are Windows-only and <code>METAL</code> is Apple-only (macOS and iOS).` |

CURRENT: 113 ("iOS is experimental"; same paragraph's "native X11, Wayland and Win32 backends" is [policy-b]), 166, 224 (no FFmpeg on iOS). OK-GENERIC: 167 (Metal in the MonoGame column).

### docs/tutorials/88-device-layer.html
Counts: STALE 1 · CURRENT 3 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 207 | `Read anything about iOS as descriptive of the code, not as a supported target: <strong>CNA does not support iOS or tvOS at any level</strong> &mdash; there is no toolchain file, and the <code>METAL</code> renderer&rsquo;s own configure gate states that both remain unvalidated.` | Wrong already at b0e97bb1 (`cmake/toolchains/ios.cmake` existed); at c1c316b9 METAL targets iOS (gate L136-144) and iOS has Simulator evidence (R2 §3, §8 "iOS is only configured" must not be said). | `Read anything about iOS as descriptive of the code: CNA&rsquo;s iOS support is experimental (a toolchain file, Simulator runs with <code>SDL_RENDERER</code> and <code>METAL</code>, no physical-device run), and tvOS is not supported.` |

CURRENT: 173 (no native file dialog on iOS), 214 (SDL3 dialog backends: none for iOS), 222 (FileDialog false on iOS).

### docs/tutorials/117-devices-layer.html
Counts: STALE 1 · CURRENT 3 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 213 | `we did not run the layer on Android, iOS or the browser, and <strong>CNA does not support iOS or tvOS at any level</strong> &mdash; there is no toolchain file, and the <code>METAL</code> renderer&rsquo;s own configure gate states that both remain unvalidated.` | as 88-device-layer L207. | `we did not run the layer on Android, iOS or the browser; CNA&rsquo;s iOS support is experimental (a toolchain file and Simulator runs, no physical-device run), and tvOS is not supported.` |

CURRENT: 185, 204, 215.

### docs/tutorials/132-webgpu.html
Counts: STALE 1 · CURRENT 4 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 64 | `<strong>Experimental, and measured on one native platform.</strong> ... CNA's own renderer notes describe the native route as run on Linux x86_64; the pinned Windows, macOS and Linux aarch64 wgpu-native packages are hash-pinned but their build, link and run verification is recorded there as still open. ... <strong>no GitHub workflow selects <code>WEBGPU</code></strong>, natively or under Emscripten.` | macOS aarch64: full tree 10,968/10,968 through wgpu-native v29.0.1.1's Metal backend on the M4 (R2 §2.5, AM4-088/131/208). Pre-AM4-088 macOS "WebGPU" passes were skips (R2 §8). Non-Apple: the Emscripten workflow now builds `WEBGL2;WEBGPU` (`emscripten-multi-renderer-ci.yml:131-132`, build only). | `<strong>Experimental, and measured on two native platforms.</strong> CNA declares <code>WEBGPU</code> <em>Experimental</em> (a declaration, not a measurement). The native route has run on Linux x86_64 and, in CNA&rsquo;s Apple campaign, on macOS arm64: the full test tree passed through wgpu-native&rsquo;s Metal backend on a physical Mac mini M4 (10,968 tests, 279 named skips; a partial <code>MultiSampleMask</code> is refused there and occlusion is a 0-or-1 flag). The pinned Windows and Linux aarch64 packages are hash-pinned but their build, link and run verification is still open. The browser route has been driven in headless Chrome by CNA&rsquo;s own scripts, and the Emscripten workflow builds a <code>WEBGL2;WEBGPU</code> bundle, but no workflow runs <code>WEBGPU</code>.` |

CURRENT: 74, 75, 84, 118 (macOS host/asset rows).

### docs/migration-from-monogame.html
Counts: STALE 1 · CURRENT 1 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 509 | `<strong>Apple targets are scoped</strong> &mdash; macOS/Metal has automatic CI. iOS is experimental and limited to SDL_RENDERER final-link plus a one-frame simulator smoke path; tvOS is unsupported.` | R2 §2.1, §2.4, §2.16, §3. | `<li><strong>Apple targets are scoped</strong> &mdash; macOS was measured on a physical Mac mini M4 (all seven renderer trees CNA qualified there passed its full test suite; <code>METAL</code> is rated supported, not primary-production), and hosted macOS CI is configured with no green run after its latest changes recorded. iOS is experimental: <code>SDL_RENDERER</code> and <code>METAL</code>, Simulator pixel evidence, no physical-device run; tvOS is unsupported.</li>` |

CURRENT: 507 (video decodes on Linux and macOS with FFmpeg).

### deep-dives/build/third-party-dependencies.html
Counts: STALE 1 · CURRENT 5 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 202 | `(and a static <code>CNA::CApiStatic</code> archive on non-Apple Unix builds when Python 3 is available)` | AM4-213: macOS builds it too via `ld -r -all_load` + `nmedit -s` (`modules/c-api/CMakeLists.txt:358-362`); on macOS the `CNACApi` component installs the SDL dylibs with `@loader_path` (AM4-210). | `(and a static <code>CNA::CApiStatic</code> archive on Unix builds, macOS included, when Python 3 is available)` |

CURRENT: 144, 171 (FFmpeg probe skipped on iOS), 189 (wgpu-native v29.0.1.1 for macOS — `cmake/ThirdPartyWebGPU.cmake:12`), 192, 194.

### docs/tutorials/164-gamer-services-server.html
Counts: STALE 1 · CURRENT 1 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 163 | `Not qualified: Windows and macOS clients and server hosts, a real wide-area network with NAT, ...` | R2 §2.11-2.13, §5 (cna-gamer-services-server 46/46 on the M4; client harnesses; AM4-043/200). | `<li>Not qualified: Windows clients and server hosts, macOS beyond one local Mac mini M4 run over loopback (online play there needs a libcurl with WebSocket support), a real wide-area network with NAT, voice on physical audio devices, and avatar pixels on Direct3D and Metal. Public-Internet deployment has not been independently qualified.</li>` |

CURRENT: 136 (credentials in owner-only files on macOS; Keychain not used — `docs/gamer-services-server.md:181`).

### docs/gamer-services.html
Counts: STALE 1 · CURRENT 2 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 183 | `<li>Not qualified: Windows and macOS, a real wide-area network with NAT, voice on physical audio devices, and avatar pixels on Direct3D and Metal.</li>` | as above. | `<li>Not qualified: Windows; macOS beyond one local Mac mini M4 run over loopback (where online play needs a libcurl with WebSocket support); a real wide-area network with NAT, voice on physical audio devices, and avatar pixels on Direct3D and Metal.</li>` |

CURRENT: 156 (0600 files on macOS), 178 (avatar rendering not measured on Metal; same sentence names "OpenGL ES 2" [policy-a]).

### docs/tutorials/162-gamer-services-setup.html · 163-guide-system-ui.html · 165-friends-presence.html · 166-online-sessions.html · 167-avatars.html
Counts (each page): STALE 1 · CURRENT 0 (167: CURRENT 1) · OK-GENERIC 0

| Page:Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 162:199 | `Not qualified: Windows and macOS (the Windows paths above are read from the source, not run), ...` | R2 §2.11-2.13, §5. | `<li>Not qualified: Windows (the Windows paths above are read from the source, not run); macOS beyond one local Mac mini M4 run over loopback; a real wide-area network with NAT, voice on physical audio devices, and avatar pixels on Direct3D and Metal.</li>` |
| 163:161 | `Not qualified: Windows and macOS (Guide input there was not exercised), ...` | Guide/gamer-services UI tests 130/130 on METAL on the M4, Guide input fixes (AM4-086/090). | `<li>Not qualified: Windows (Guide input there was not exercised); macOS beyond CNA&rsquo;s local Mac mini M4 run, where the Guide and gamer-services UI suite passed (130 of 130 on <code>METAL</code>); a real wide-area network with NAT, voice on physical audio devices, and avatar pixels on Direct3D and Metal.</li>` |
| 165:153 | `Not qualified: Windows and macOS, a real wide-area network with NAT, ...` | as 162. | `<li>Not qualified: Windows; macOS beyond one local Mac mini M4 run over loopback; a real wide-area network with NAT, voice on physical audio devices, and avatar pixels on Direct3D and Metal. Public-Internet deployment of the server has not been independently qualified.</li>` |
| 166:179 | `Not qualified: Windows and macOS, a real wide-area network with NAT (latency, loss and failover are unmeasured), ...` | as 162; the SDK libcurl refuses the relay (AM4-044/123). | `<li>Not qualified: Windows; macOS beyond one local Mac mini M4 run over loopback (the relay needs a libcurl with WebSocket support; Apple&rsquo;s system libcurl 8.7.1 is refused by name); a real wide-area network with NAT (latency, loss and failover are unmeasured), voice on physical audio devices (tested in software only), and avatar pixels on Direct3D and Metal.</li>` |
| 167:172 | `Not qualified: Windows and macOS, a real wide-area network with NAT, ...` | as 162. | `<li>Not qualified: Windows; macOS beyond one local Mac mini M4 run over loopback; a real wide-area network with NAT, voice on physical audio devices, and avatar pixels on Direct3D and Metal.</li>` |

167 CURRENT: 170 (avatar pixels not measured on Metal; same item names "OpenGL ES 2" [policy-a]).

### docs/tutorials/97-networking.html
Counts: STALE 1 · CURRENT 0 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 495 | `Windows and macOS, a real wide-area network with NAT, and voice on physical audio devices have not been qualified.` | AM4-043 (SystemLink discovery on macOS: `TwoProcessLoopbackTest` 8/8, ENet 81/81, one machine), AM4-200 (304 networking cases on the Metal tree). | `Windows, a real wide-area network with NAT, and voice on physical audio devices have not been qualified; on macOS CNA records one local Mac mini M4 run (the networking suites, the two-process loopback test included, after fixes to SystemLink discovery for macOS), not a multi-machine qualification.` |

### docs/tutorials/123-achievements.html
Counts: STALE 1 · CURRENT 1 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 315 | `<strong>Qualification is Linux-only.</strong> ... Windows and macOS have not been qualified` | R2 §2.11, §5. | `<li><strong>Qualification is mainly Linux.</strong> CNA records its final audit run of this work on Linux (2 October 2026): the GamerServices suite 649 passed and the Net suite 524 passed, with no failures. Windows has not been qualified and macOS only by one local Mac mini M4 run over loopback, and no public server instance exists &mdash; a server-backed game runs against a server you operate.</li>` |

CURRENT: 286 (macOS storage path).

### deep-dives/services/network-sessions.html
Counts: STALE 1 · CURRENT 1 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 202 | `nothing establishes play across the public Internet, on Windows or macOS, or in a browser.` | R2 §2.12-2.13, §5. | `CNA also records its networking suites and the server&rsquo;s harness-driven tests passing over loopback on one Mac mini M4, where the relay needs a libcurl with WebSocket support; nothing establishes play across the public Internet, between machines, on Windows, or in a browser.` |

CURRENT: 316 (process-spawning tests compiled out on iOS).

### deep-dives/services/gamer-services-contract.html
Counts: STALE 1 · CURRENT 2 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 253 | `the online client paths, credential stores or Guide input on Windows or macOS (not run there; the Windows credential store was exercised under Wine only)` | R2 §2.11 (Guide UI 130/130 on Metal), §5 (server harnesses on the M4). CNA's own `gamer-services-known-limitations.md:581-583` still says no macOS host (stale inside CNA). | `the online client paths, credential stores or Guide input on Windows (not run there; the Windows credential store was exercised under Wine only), or on macOS beyond one local Mac mini M4 run over loopback` |

CURRENT: 169 (macOS keeps 0600 files, no Keychain), 250 (harness cases compiled out on iOS).

### deep-dives/services/avatars.html
Counts: STALE 1 · CURRENT 0 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 310 | `Not measured: OpenGL ES 2, the DirectX and Metal renderers (no Windows or macOS host), FNA3D and SDL_RENDERER` | A macOS host existed in the campaign but the avatar review was not repeated on Metal; CNA's `gamer-services-known-limitations.md:662` still gives "no Windows or macOS host". [policy-a] OpenGL ES 2. | `Not measured: the DirectX renderers (no Windows host), Metal (CNA&rsquo;s Mac mini M4 campaign did not repeat this review), FNA3D and SDL_RENDERER (which cannot draw the 3D avatar at all).` |

### deep-dives/renderers/renderer-contract.html
Counts: STALE 1 · CURRENT 1 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 219 | `Metal and the 2D-only families keep the throwing default` | Metal implements `DrawInstancedPrimitivesEx` (`MetalRenderer.hpp:681`; AM4-143/154). [policy-a] DirectX 12, "ES 2.0 generation". | `By the source search, the instanced route is implemented by DirectX 9, DirectX 11, EasyGL, FNA3D, Metal, SDL_GPU, Software, Vulkan and WebGPU; the 2D-only family keeps the throwing default, and Headless records the call without rasterising, so it proves routing, not instancing.` |

CURRENT: 261 (Metal overrides `SetStringMarkerEXT` — `MetalRenderer.mm:6457-6462`).

### deep-dives/renderers/sdl-renderer-2d-contract.html
Counts: STALE 1 · CURRENT 1 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 148 | `It is also the default renderer everywhere except Linux and the web, and the only renderer allowed on iOS` | iOS allow-list SDL_RENDERER + METAL. | `It is also the default renderer everywhere except Linux and the web, and one of the two renderers allowed on iOS (with <code>METAL</code>)` |

CURRENT: 265 (the Apple workflow builds on macOS and iOS and runs selected suites from `CnaTests`).

### deep-dives/renderers/render-targets-clears-and-viewports.html
Counts: STALE 1 · CURRENT 3 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 149 | `Two shapes are refused by some families only, at the renderer: a cube face inside a multi-target set (DirectX 9, 11 and 12, SDL_GPU, WebGPU and Headless refuse it; ...) and any multi-target set at all on Metal.` | AM4-097 (Metal MRT incl. cube-face members). [policy-a] DirectX 12. | `<p>One shape is refused by some families only, at the renderer: a cube face inside a multi-target set (DirectX 9 and 11, SDL_GPU, WebGPU and Headless refuse it; see <a href="../../docs/render-targets.html#rendertargetcube">RenderTargetCube</a>).</p>` |

CURRENT: 143, 200 (page-scope "macOS families not observed"), 190 (METAL overrides both hooks).

### deep-dives/models/gltf-import.html
Counts: STALE 1 · CURRENT 0 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 241 | `its two texture maps are sampled by seven renderer families (DirectX 9, 11 and 12, EasyGL, SDL_GPU, Vulkan and WebGPU, per <code>SpecularTextureInventoryClassifiesEveryPbrRenderer</code>) and not by <code>METAL</code>, which is factor-only.` | AM4-085; `GltfRendererPbrFallbackPolicyTests.cpp:1224-1225` (directx9, directx11, easygl, sdl-gpu, vulkan, webgpu, metal). [policy-a] DirectX 12. | `its two texture maps are sampled by all seven PBR renderer families (DirectX 9 and 11, EasyGL, SDL_GPU, Vulkan, WebGPU and Metal, per <code>SpecularTextureInventoryClassifiesEveryPbrRenderer</code>).` (re-check the following "registry's own prose lists six" remark at c1c316b9) |

### deep-dives/models/gltf-conformance.html
Counts: STALE 1 · CURRENT 0 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 217 | `<li><code>KHR_materials_specular</code> texture sampling on every PBR renderer — among the current renderers only <code>METAL</code> still samples neither map (per the renderer inventory test);</li>` | Closed 2026-10-08 (`plans/plan_gltf.md:140`, GLTF-344 via AM4-085); the GLTF-459 tally (`:142`) was not re-assessed. | Remove the item from the open list, or: `<li><code>KHR_materials_specular</code> texture sampling &mdash; now on every PBR renderer (<code>METAL</code> since 2026-10-08), although the plan&rsquo;s milestone tally still lists the row as open;</li>` |

### development/takeover/validation.html
Counts: STALE 1 · CURRENT 4 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 179 | `runtime evidence comes from the Apple CI job (the simulator preset's description says it launches the app for one framework frame) and CNA's recorded notes (<a ...><code>apple-platforms.md</code></a>).` | R2 §2.1, §3, §2.16. The preset description is unchanged at c1c316b9 (`CMakePresets.json` `ios-simulator`). | `runtime evidence comes from CNA&rsquo;s recorded Mac mini M4 qualification and iOS Simulator pixel probe (<a ...><code>apple-platforms.md</code></a>) and from the Apple CI jobs (configured; no green run after their latest changes recorded); the simulator preset&rsquo;s description still speaks of one framework frame.` |

CURRENT: 158 (page claims no Apple result itself), 188, 218, 222.

### development/handbook/change-build-configuration.html
Counts: STALE 1 · CURRENT 3 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 225 | `Windows-only (<code>DIRECTX9</code>, <code>DIRECTX11</code>, <code>DIRECTX12</code>), Emscripten-only (<code>WEBGL1</code>, <code>WEBGL2</code>, <code>CANVAS</code>) and macOS-only (<code>METAL</code>) partitions` | Partition (Conventions). [policy-a] | `Windows-only (<code>DIRECTX9</code>, <code>DIRECTX11</code>), Emscripten-only (<code>WEBGL2</code>) and Apple-only (<code>METAL</code>) partitions, because one toolchain targets one of them at a time. Three EasyGL identities <em>can</em> coexist ...` |

CURRENT: 244 (macos/ios presets have no build preset), 275 (Apple sysroot before SDL sub-builds), 293 (link label).

### docs/tutorials/126-multi-renderer-build.html
Counts: STALE 1 · CURRENT 1 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 75 | `Windows-only (<code>DIRECTX9</code>, <code>DIRECTX11</code>, <code>DIRECTX12</code>), Emscripten-only (<code>WEBGL1</code>, <code>WEBGL2</code>, <code>CANVAS</code>) and macOS-only (<code>METAL</code>)` | Partition. [policy-a] | `Windows-only (<code>DIRECTX9</code>, <code>DIRECTX11</code>), Emscripten-only (<code>WEBGL2</code>) and Apple-only (<code>METAL</code>)` |

CURRENT: 142 (Metal window kind).

### development/invariants.html
Counts: STALE 1 · CURRENT 1 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 185 | `states the platform partitions (Windows-only, Emscripten-only and macOS-only identities)` | Partition. | `states the platform partitions (Windows-only, Emscripten-only and Apple-only identities)` |

CURRENT: 197 (only METAL sets `wantsHighDpi`).

### docs/tutorials/49-touch-input.html
Counts: STALE 1 · CURRENT 0 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 106 | `iOS support in this snapshot is a narrow <code>SDL_RENDERER</code> build/link and one-frame simulator smoke path, not broad device validation; tvOS remains unsupported.` | R2 §3; real iOS touch never exercised (`apple-platforms.md` "Touch input"). [policy-b] the same paragraph names `WIN32` and native Wayland touch implementations. | `iOS support in this snapshot is experimental: <code>SDL_RENDERER</code> and <code>METAL</code> builds run on the iOS Simulator, and no physical device has run CNA, so touch on a real iOS screen has never been exercised; tvOS remains unsupported.` |

### development/internals/graphics/draw-call.html
Counts: STALE 1 · CURRENT 1 · OK-GENERIC 3

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 306 | link label `CNA-GAP-013: METAL refuses a large part of the graphics API until it has macOS evidence: MRT, custom effects, occlusion queries, instancing, multi-stream input, back-buffer readback and several sampler/blend states` | All implemented in AM4 Phase 3 (R2 §2.4, §6). | Mirror the known-issues owner's decision for CNA-GAP-013 (closed at c1c316b9; remaining Metal limits are in R2 §2.4). |

CURRENT: 245 (Metal draw path "not traced"). OK-GENERIC: 168, 217, 218 (Vulkan submit/present lines).

### development/reference/modules.html
Counts: STALE 1 · CURRENT 0 · OK-GENERIC 0

| Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| 143 | `<td><code>metal</code></td><td>implementation family</td><td>25</td><td>2</td><td>26</td>` | Counted at c1c316b9: `modules/renderers/metal/include` 28 files, `src` 3 (`MetalCompiledEffect.cpp` added, AM4-144), `tests` 29 (b0e97bb1: 25/2/26). | `<td><code>metal</code></td><td>implementation family</td><td>28</td><td>3</td><td>29</td>` (the whole table is a generated census and should be regenerated at c1c316b9) |

### [policy-c]/[R3]-only pages (each STALE 1)

| Page:Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| development/reference/test-targets.html:142 | link label `C ABI 0.44.0 reaches, ... for the 656 unmapped symbols` | [policy-c] R3 §1 (631 unmapped). | `C ABI 0.46.0 reaches, ... for the 631 unmapped symbols` |
| docs/tutorials/146-cnb-packs.html:429 | `The experimental C ABI (0.44.0 at this snapshot) declares` | [policy-c] | `The experimental C ABI (0.46.0 at this snapshot) declares` |
| docs/cnaext-extensions.html:300 | `follow the C ABI&rsquo;s own versioning (0.44.0 at this snapshot)` | [policy-c] | `(0.46.0 at this snapshot)` |
| docs/cnb-format.html:515 | `The experimental C ABI (version <strong>0.44.0</strong> at this snapshot;` | [policy-c] | `(version <strong>0.46.0</strong> at this snapshot;` |
| development/takeover/inherited.html:155 | `an experimental C ABI (0.44.0, 60 public headers)` | [policy-c]; same sentence "14 physical renderer-family directories serving 18 public renderer identities" [policy-a] → 12 families, 14 identities. | `an experimental C ABI (0.46.0, 60 public headers)` |
| development/repository/source-ownership.html:362 | `<code>abi.h</code></a> (0.44.0, experimental)` | [policy-c] | `(0.46.0, experimental)` |
| development/internals/modules/storage.html:227 | `default <code>OFF</code>; ABI 0.44.0; source-level` | [policy-c] | `default <code>OFF</code>; ABI 0.46.0; source-level` |
| development/handbook/change-map.html:217 | `(CNA.NET, <code>libcna/cna-cs</code>)` … `(0.44.0 at this snapshot) ... admits exactly one ABI (0.44.0 at cna-cs <code>860f92c</code>)` | [policy-c]/[R3] §3.1-3.2. "No CNA workflow builds the C library" is still true (no `cmake --build` in any `c-api-*.yml` at c1c316b9). | `(CNA.NET, <code>libcna/cna-dotnet</code>)` … `(0.46.0 at this snapshot) and the C# binding is independently versioned and admits exactly one ABI (0.46.0).` |

Other Apple hits on these pages: cnb-format 267 CURRENT (CRC32 always on Apple silicon); 146-cnb-packs 198 OK-GENERIC (`std::ios`); inherited 158 CURRENT (Metal header interface); source-ownership 235 CURRENT (shadercross default on Apple); storage 185 CURRENT (Apple `Library/Application Support`); change-map 209 CURRENT (FFmpeg never on iOS); test-targets 135 CURRENT (generated target list; regenerate at c1c316b9 — new Metal targets such as `cna_test_metal_spritebatch_customeffect`), 144 OK-GENERIC.


---

## Campaign-driven items on non-Apple lines (found incidentally; NOT counted in the totals)

These lines carry no Apple term, so they are outside the regex survey, but the AM4 campaign made them stale (R2 §6 rows "Five CI workflows pin stale sharp-runtime commits" and "ModuleLinkClosure_* gates skip under Ninja"). Listed so the lead can route them.

| Page:Line | Current text | Why stale | Proposed replacement |
|---|---|---|---|
| docs/tutorials/80-cross-platform.html:146 | `it pins an older sharp-runtime revision, so we cannot say it currently passes` | AM4-234: every workflow that checks out sharp-runtime now uses `scripts/ci/sibling_branch.sh` (no SHA pin left at c1c316b9 — `apple-ci.yml:100-111`, `metal-macos-ci.yml:50-60`, `emscripten-multi-renderer-ci.yml:56-67`, `devices-tests.yml:99-109`, `content-pipeline-windows-ci.yml:39-49`). [policy-a] same cell lists `WEBGL1;CANVAS`; the bundle is `WEBGL2;WEBGPU` (`emscripten-multi-renderer-ci.yml:131-132`). | `A build/link workflow covers a <code>WEBGL2;WEBGPU</code> bundle and checks out sharp-runtime&rsquo;s matching branch; no green run after its latest changes is recorded.` |
| development/testing/architecture.html:433 · development/testing/index.html:276 | link label `CNA-BUG-199: Five CI workflows pin August 2026 sharp-runtime commits ...` | Fixed by AM4-234 (see above). | Mirror the known-issues owner's decision for CNA-BUG-199 (fixed). |
| deep-dives/platforms/web-build-and-main-loop.html:192 | `the web workflow (<code>emscripten-multi-renderer-ci.yml</code>) pins a sharp-runtime revision that predates the components this snapshot requests, so by a static reading it cannot configure at TARGET` | AM4-234; Emscripten CI fixes AM4-273..300 (R2 §5 cna-template row; plan Phase 7). | `the web workflow (<code>emscripten-multi-renderer-ci.yml</code>) now checks out sharp-runtime&rsquo;s matching branch; no green run after its latest changes is recorded.` |
| deep-dives/build/third-party-dependencies.html:142 | `(six CI workflows check out a pinned older sharp-runtime commit)` | AM4-234 (six workflows, all branch-selected now). | `(six CI workflows check out the matching sharp-runtime branch through <code>scripts/ci/sibling_branch.sh</code>)` |
| deep-dives/build/third-party-dependencies.html:180 | `while several workflows pin older commits that predate the components listed above` | AM4-234. | `while the six workflows that check sharp-runtime out themselves pick the same branch through <code>scripts/ci/sibling_branch.sh</code> instead of the older commits they used to pin` |
| deep-dives/build/tools-and-scripts.html:194 | `(some CI lanes pin an older sharp-runtime)` | AM4-234. | `(CI lanes check out sharp-runtime&rsquo;s matching branch, so record which commit that was)` |
| development/testing/architecture.html:251 | `<td>Executables plus <code>scripts/check_module_link_closure.py</code>; skipped under Ninja</td>` | AM4-167: the checker falls back to `ninja -t commands -s <target>` in a single-config Ninja tree; it still skips in a multi-config tree. 28/28 measured on macOS. | `<td>Executables plus <code>scripts/check_module_link_closure.py</code>; evaluated under Makefiles and single-config Ninja, skipped in multi-config trees</td>` |
| development/testing/architecture.html:446 · development/repository/index.html:374 · development/reference/test-targets.html:168 | link label `CNA-VGAP-019: ModuleLinkClosure_* link-closure gates report CTest SKIP in every Ninja tree ...` | AM4-167. | Mirror the known-issues owner's decision for CNA-VGAP-019 (fixed for single-config Ninja). |
| deep-dives/build/dependency-boundaries.html:219 | `The Makefiles generators write that file; Ninja does not. When the file is missing the script prints <code>SKIP: ... not found (non-Makefiles generator?)</code> and exits 77` | AM4-167. | `The Makefiles generators write that file; in a single-config Ninja tree the script asks <code>ninja -t commands -s &lt;target&gt;</code> for the same link command instead. Only where neither exists (a multi-config generator) does it print a skip and exit 77, ...` |
| deep-dives/build/dependency-boundaries.html:220 | `configures with <code>-G Ninja</code>, where every closure gate reports skipped ... By reading, no workflow evaluates a link-closure contract` | AM4-167; `general-tests-ci.yml:146` uses single-config Ninja, so its unfiltered `ctest` now evaluates the closure gates it registers. | `configures with <code>-G Ninja</code>, where the closure gates now run, although its <code>OPENGLES3</code> configuration registers neither the HEADLESS nor the Vulkan closure.` (re-check the rest of the paragraph) |
| deep-dives/build/dependency-boundaries.html:255 | `In a Ninja tree the same test reports skipped instead.` | AM4-167. | `In a multi-config tree the same test reports skipped instead.` |
| development/internals/modules/storage.html:167 | `the closure check also needs Python 3 and a Makefiles generator, because it reads <code>link.txt</code>: under Ninja it reports SKIPPED with exit 77, and every CI job either uses Ninja or filters these tests out` | AM4-167. | `the closure check also needs Python 3 and a single-config generator (Makefiles, or Ninja through <code>ninja -t commands</code>); it reports SKIPPED with exit 77 only in a multi-config tree` (and drop "no CI job currently enforces it" only after confirming `general-tests-ci` registers this probe) |

---

## Pages with only CURRENT / OK-GENERIC occurrences

| Page | CURRENT | OK-GENERIC | Note |
|---|---|---|---|
| development/build/architecture.html | 9 | 1 | Apple sysroot/SDL keys, static link on macOS, shadercross default on Apple, Metal header interface; 336 link label |
| docs/sensors.html | 6 | 0 | Accelerometer/Gyroscope on macOS desktop and iOS policy |
| deep-dives/build/module-architecture.html | 4 | 1 | 153 iOS PUBLIC entry point ([policy-b] "Xlib, Wayland, Win32" in same sentence), 214 metal entered always, 267/270 Metal workflow path filter still stale in CNA (`metal-macos-ci.yml:5-24`); 204 OK-GENERIC |
| deep-dives/framework/window-and-device-manager.html | 5 | 0 | iOS orientation swap, launch parameters empty on macOS/iOS |
| deep-dives/renderers/sdl-gpu-pipeline-state-and-draw-order.html | 5 | 0 | "Metal behaviour is not established by it" refers to the Linux push-uniform measurement — still true; optional: link the M4 SDL_GPU run |
| development/internals/platforms/index.html | 3 | 2 | 156 SDL3 PUBLIC on iOS and 188 `ApplePlatform.cmake` current; 157-158 X11/Wayland rows and 165's X11-on-macOS remark are [policy-b] (native X11/Wayland platforms), Apple mention only an exclusion |
| docs/audio.html | 4 | 1 | SDL3 audio on macOS/iOS, no SDL-free audio on macOS; 386 `std::ios` (OK-GENERIC) |
| docs/input.html | 5 | 0 | `cocoa` global mouse; sensors on iOS; 684 CNA-BUG-133 link still true for METAL (no `RegisterForWindow` in `modules/renderers/metal` at c1c316b9) |
| deep-dives/platforms/web-build-and-main-loop.html | 2 | 2 | METAL refused by host gate; Apple storage path; 89/246 nav links |
| deep-dives/platforms/windows-cross-compiling-and-wine.html | 3 | 1 | `ios.cmake` toolchain, SDL static on iOS, Apple deployment-target SDL key; 89 nav link |
| development/internals/modules/devices.html | 3 | 1 | iOS sensor policy; 276 link label |
| development/internals/modules/inspector.html | 4 | 0 | as docs/inspector.html |
| development/internals/modules/video-ffmpeg.html | 4 | 0 | Apple workflows `brew install ffmpeg` (macOS jobs, `apple-ci.yml:117`, `metal-macos-ci.yml`); iOS exclusion |
| docs/inspector.html | 4 | 0 | macOS runtime validation still pending in CNA `docs/inspector.md:284,338` at c1c316b9 |
| docs/tutorials/124-web-gotchas.html | 4 | 0 | METAL refused for web builds; no video on iOS ([policy-a] 202/215 name OPENGLES2/three browser renderers) |
| docs/tutorials/141-save-data-portably.html | 3 | 1 | macOS `~/Library/Application Support`; 299 shell comment OK-GENERIC |
| docs/tutorials/150-build-time-fx-compilation.html | 4 | 0 | fxc through wine on macOS; no Metal shader output (true — the compiler emits D3D9 bytecode). Optional: `.fx` compilation was not exercised on macOS (AM4-048) |
| docs/tutorials/19-save-load.html | 2 | 2 | 107/155 macOS save path; 7/12 meta description (macOS listed generically) |
| docs/tutorials/50-accelerometer.html | 4 | 0 | iOS/desktop sensor policy |
| deep-dives/services/sensors-and-vibration.html | 3 | 0 | iOS sensor policy |
| development/internals/modules/devices-ext.html | 3 | 0 | file-dialog iOS policy, macOS pixel density, CNA-BUG-181 link |
| docs/tutorials/138-sdl-free-build.html | 3 | 0 | no SDL-free path on macOS/iOS |
| docs/tutorials/56-environment-map.html | 0 | 3 | "metal" as a material |
| deep-dives/build/dependency-boundaries.html | 2 | 0 | Apple presets use the platform default generator; macOS lanes filter CTest; stale Metal path filter (still stale in CNA) |
| deep-dives/graphics/compiled-effects-semantics.html | 2 | 0 | "Metal text" is not an Effect container; SDL_GPU shadercross default on Apple. Optional: the CMake-option table on this page should gain `CNA_METAL_COMPILED_EFFECTS` if it lists options (not an Apple-hit line) |
| deep-dives/graphics/surface-formats.html | 2 | 0 | Metal does not override `GetMaxTextureDimension` (still true at c1c316b9) |
| deep-dives/graphics/texture-data-transfer.html | 2 | 0 | Metal mip-definedness override and cube/volume readback |
| deep-dives/models/cnj-toolchain.html | 2 | 0 | converter tests excluded on iOS |
| deep-dives/services/host-devices.html | 2 | 0 | file dialog/tray iOS |
| deep-dives/services/input-model.html | 2 | 0 | `cocoa`; METAL never calls `RegisterForWindow` (still true) |
| development/architecture/graphics.html | 1 | 1 | Metal window kind/high-DPI; 231 link label |
| development/handbook/fix-a-renderer-bug.html | 1 | 1 | SDL_GPU "a Vulkan result does not establish Direct3D 12 or Metal"; 314 link label |
| development/internals/input/events.html | 2 | 0 | `cocoa` global mouse; CNA-BUG-133 link (still true for METAL) |
| development/internals/modules/core.html | 2 | 0 | `CNA_TARGET_APPLE/IOS/MACOS` macros |
| development/internals/modules/net.html | 2 | 0 | process-spawning tests filtered on iOS; VGAP-039 link |
| docs/content-pipeline.html | 1 | 1 | 511 media decoder unavailable on iOS; 560 `ios` XNB platform id |
| docs/tutorials/03-first-window.html | 2 | 0 | SDL shared on macOS, static on iOS; no FFmpeg on iOS |
| docs/tutorials/103-direct3d-windows.html | 2 | 0 | D3D refused on macOS; iOS accepts none ([policy-b] WIN32 platform in 114) |
| docs/tutorials/127-platform-audio-selection.html | 2 | 0 | macOS audio = SDL3 or NULL ([policy-b] SDL-free WIN32 in 126) |
| docs/tutorials/82-android.html | 1 | 1 | sensors on macOS desktop; 250 link label |
| docs/tutorials/89-sharp-runtime.html | 1 | 1 | 319 `FileSystemWatcher` listed generically (CURRENT); 257 `std::ios` (OK-GENERIC) |
| deep-dives/build/index.html | 0 | 1 | link label |
| deep-dives/build/tools-and-scripts.html | 1 | 0 | the Apple workflow runs `CnaTests` with a filter |
| deep-dives/framework/game-time-and-timestep.html | 1 | 0 | Metal treats any nonzero interval as display sync (PresentInterval.Two = One, AM4-139) |
| deep-dives/graphics/capability-model-and-evidence.html | 1 | 0 | METAL switch without a default arm |
| deep-dives/graphics/graphicsdevice-contract.html | 1 | 0 | `SetStringMarkerEXT` on METAL |
| deep-dives/graphics/stock-effects-semantics.html | 1 | 0 | METAL reads `preferPerPixelLighting` |
| deep-dives/index.html | 0 | 1 | "Android and Apple platforms" section label |
| deep-dives/practice/migrating-an-xna-game.html | 1 | 0 | no FFmpeg on iOS |
| deep-dives/renderers/index.html | 0 | 1 | link label |
| deep-dives/renderers/vulkan-deferred-state-and-descriptors.html | 1 | 0 | METAL suppresses an empty-scissor draw (METAL-279, still in `metal-renderer.md`) |
| deep-dives/services/media-contract.html | 1 | 0 | no FFmpeg on iOS |
| deep-dives/sharp-runtime/components-and-consumption.html | 1 | 0 | `System.Diagnostics.Process` does not compile against the iOS SDK |
| deep-dives/verification/test-populations-and-gates.html | 1 | 0 | METAL only for Apple |
| development/architecture/runtime.html | 0 | 1 | link label |
| development/handbook/add-a-regression-test.html | 1 | 0 | Apple smoke app registered as its own executable |
| development/handbook/investigate-a-sample-failure.html | 1 | 0 | Apple storage root |
| development/handbook/modify-contentmanager.html | 1 | 0 | tool-spawning tests excluded on iOS |
| development/handbook/modify-the-content-pipeline.html | 1 | 0 | tool-spawning tests excluded on iOS |
| development/index.html | 1 | 0 | Metal has no dedicated internals page (still true) |
| development/internals/audio/engine.html | 1 | 0 | mixer tests excluded on iOS |
| development/internals/content/runtime.html | 1 | 0 | tool-spawning tests excluded on iOS |
| development/internals/graphics/device.html | 1 | 0 | Metal overrides `GetDefaultViewportRect` ([policy-a] Canvas in same list) |
| development/internals/graphics/vulkan.html | 0 | 1 | link label |
| development/internals/runtime/frame.html | 1 | 0 | iOS background lifecycle |
| development/internals/runtime/module.html | 1 | 0 | orientations on iOS |
| development/internals/runtime/startup.html | 1 | 0 | iOS orientation swap |
| development/reference/selection-axes.html | 0 | 1 | METAL ordinal 42 |
| development/takeover/case-study-storage.html | 1 | 0 | Apple storage root |
| development/testing/index.html | 1 | 0 | "A green Linux unit job does not validate ... the Metal backend" |
| docs/content-manager.html | 1 | 0 | no FFmpeg on iOS |
| docs/content-pipeline-xnb.html | 0 | 1 | `ios` XNB platform id |
| docs/storage.html | 1 | 0 | macOS storage root |
| docs/tools.html | 0 | 1 | `ios` XNB platform id |
| docs/tutorials/108-fna3d.html | 1 | 0 | 152 `Metal` alias of `FNA3D_FORCE_DRIVER=SDLGPU`. Section note: the driver-order paragraph (L144, non-Apple line) could add "CNA&rsquo;s registered FNA3D tests on Apple pin FNA3D&rsquo;s Metal driver; macOS&rsquo;s legacy OpenGL is a GL 2.1 compatibility context" (AM4-051) and the M4 result (10,875 tests; no occlusion queries on that driver) |
| docs/tutorials/122-media-library.html | 1 | 0 | no decoder on iOS |
| docs/tutorials/125-pixel-testing.html | 1 | 0 | 18 workflow files incl. Apple ("none builds the C library" still true; "18 identities" [policy-a] elsewhere on page) |
| docs/tutorials/136-native-wayland-build.html | 0 | 1 | "not offered on Apple targets" — the whole page is [policy-b] (native Wayland platform) |
| docs/tutorials/137-alsa-audio.html | 1 | 0 | no SDL-free audio on macOS |
| docs/tutorials/139-terminal-platform.html | 1 | 0 | TERMINAL on macOS (POSIX) |
| docs/tutorials/147-xnb-interop.html | 0 | 1 | `ios` XNB platform id |
| docs/tutorials/148-custom-content-type.html | 0 | 1 | `std::ios` |
| docs/tutorials/156-inspector-live.html | 1 | 0 | Inspector on macOS/POSIX desktop, refused on iOS |
| docs/tutorials/20-build-run.html | 1 | 0 | no video on iOS |
| docs/tutorials/30-gamepad.html | 1 | 0 | gamepads on macOS via SDL3 ([policy-b] native X11/WAYLAND in same paragraph) |
| docs/tutorials/35-model-loading.html | 1 | 0 | SDL_RENDERER default on macOS ([policy-a] CANVAS in same sentence) |
| docs/tutorials/36-model-texturing.html | 0 | 1 | "painted metal" comment |
| docs/tutorials/37-multiple-lights.html | 0 | 1 | "metal" as a material |
| docs/tutorials/45-content-manager.html | 1 | 0 | no FFmpeg on iOS |
| docs/tutorials/57-skinned-effect.html | 1 | 0 | METAL draws SkinnedEffect; optional: Metal now has its own skinned tests (`Metal_SkinnedEffect_WorldNormal`, AM4-145) |
| docs/tutorials/70-procedural-geometry.html | 1 | 0 | METAL draws 3D |
| docs/tutorials/81-emscripten.html | 1 | 0 | no video on iOS |
| docs/tutorials/83-migrate-monogame.html | 1 | 0 | FFmpeg on Linux and macOS only |
| docs/tutorials/84-migrate-xna.html | 0 | 1 | code comment listing macOS |


---

## Summary — pages with STALE > 0

| Page | STALE | Note |
|---|---|---|
| docs/3d-rendering.html | 9 |  |
| docs/tutorials/72-backend-selection.html | 8 |  |
| docs/tutorials/80-cross-platform.html | 8 |  |
| docs/render-targets.html | 7 |  |
| docs/effects.html | 5 |  |
| docs/tutorials/62-mrt.html | 5 |  |
| docs/runtime-renderer-selection.html | 4 | 2 [policy-c] |
| docs/tutorials/114-pbr-materials.html | 4 |  |
| deep-dives/build/configuring-cna.html | 3 |  |
| deep-dives/graphics/shader-routes-four-answers.html | 3 |  |
| deep-dives/graphics/state-objects.html | 3 |  |
| development/internals/graphics/selection.html | 3 |  |
| development/reference/cmake-options.html | 3 |  |
| development/takeover/uncertainty.html | 3 | all [policy-c]/[R3] |
| development/testing/architecture.html | 3 | 2 [policy-c] |
| development/workflows.html | 3 | 2 [policy-c]/[R3] |
| docs/tutorials/02-setup.html | 3 |  |
| docs/tutorials/151-one-shader-several-renderers.html | 3 |  |
| docs/tutorials/61-occlusion-query.html | 3 |  |
| docs/tutorials/65-msaa.html | 3 |  |
| docs/tutorials/67-deferred-rendering.html | 3 |  |
| docs/xna-compatibility.html | 3 |  |
| contribute.html | 2 |  |
| deep-dives/foundations/compatibility-and-evidence.html | 2 |  |
| deep-dives/reference/glossary.html | 2 | 1 [policy-c] |
| deep-dives/reference/gltf-evidence-matrix.html | 2 |  |
| deep-dives/renderers/presentation-and-backbuffer-readback.html | 2 |  |
| deep-dives/renderers/sdl-gpu-resources-and-frame-recovery.html | 2 |  |
| deep-dives/sharp-runtime/parity-and-verification.html | 2 | conditional on the page's sharp-runtime snapshot |
| development/build/index.html | 2 |  |
| development/debugging.html | 2 | 1 [policy-c]/[R3] |
| development/handbook/make-a-release.html | 2 | both [policy-c] |
| development/internals/graphics/backends.html | 2 |  |
| development/internals/graphics/sdl-gpu.html | 2 |  |
| development/internals/modules/gamer-services.html | 2 |  |
| development/repository/index.html | 2 | both [policy-c] |
| development/repository/module-graph.html | 2 |  |
| docs/shader-effects.html | 2 |  |
| docs/tutorials/100-shipping.html | 2 |  |
| docs/tutorials/152-graphics-profiles.html | 2 |  |
| docs/tutorials/168-operate-gamer-services-server.html | 2 |  |
| docs/tutorials/52-custom-shaders.html | 2 |  |
| docs/tutorials/60-instancing.html | 2 |  |
| docs/tutorials/64-cubemaps.html | 2 |  |
| docs/tutorials/66-bloom.html | 2 |  |
| deep-dives/build/third-party-dependencies.html | 1 |  |
| deep-dives/models/gltf-conformance.html | 1 |  |
| deep-dives/models/gltf-import.html | 1 |  |
| deep-dives/renderers/render-targets-clears-and-viewports.html | 1 |  |
| deep-dives/renderers/renderer-contract.html | 1 |  |
| deep-dives/renderers/sdl-renderer-2d-contract.html | 1 |  |
| deep-dives/services/avatars.html | 1 |  |
| deep-dives/services/gamer-services-contract.html | 1 |  |
| deep-dives/services/network-sessions.html | 1 |  |
| development/architecture/platform.html | 1 |  |
| development/handbook/change-build-configuration.html | 1 |  |
| development/handbook/change-map.html | 1 | [policy-c]/[R3] only |
| development/internals/graphics/draw-call.html | 1 |  |
| development/internals/modules/storage.html | 1 | [policy-c]/[R3] only |
| development/internals/platforms/sdl3.html | 1 |  |
| development/invariants.html | 1 |  |
| development/reference/modules.html | 1 |  |
| development/reference/test-targets.html | 1 | [policy-c]/[R3] only |
| development/repository/source-ownership.html | 1 | [policy-c]/[R3] only |
| development/takeover/inherited.html | 1 | [policy-c]/[R3] only |
| development/takeover/validation.html | 1 |  |
| docs/cnaext-extensions.html | 1 | [policy-c]/[R3] only |
| docs/cnb-format.html | 1 | [policy-c]/[R3] only |
| docs/gamer-services.html | 1 |  |
| docs/graphics-state.html | 1 |  |
| docs/migration-from-monogame.html | 1 |  |
| docs/tutorials/01-introduction.html | 1 |  |
| docs/tutorials/101-renderer-capabilities.html | 1 |  |
| docs/tutorials/116-post-process-effects.html | 1 |  |
| docs/tutorials/117-devices-layer.html | 1 |  |
| docs/tutorials/121-video-playback.html | 1 |  |
| docs/tutorials/123-achievements.html | 1 |  |
| docs/tutorials/126-multi-renderer-build.html | 1 |  |
| docs/tutorials/128-compiled-xna-effects.html | 1 |  |
| docs/tutorials/131-sdl-gpu.html | 1 |  |
| docs/tutorials/132-webgpu.html | 1 |  |
| docs/tutorials/146-cnb-packs.html | 1 | [policy-c]/[R3] only |
| docs/tutorials/162-gamer-services-setup.html | 1 |  |
| docs/tutorials/163-guide-system-ui.html | 1 |  |
| docs/tutorials/164-gamer-services-server.html | 1 |  |
| docs/tutorials/165-friends-presence.html | 1 |  |
| docs/tutorials/166-online-sessions.html | 1 |  |
| docs/tutorials/167-avatars.html | 1 |  |
| docs/tutorials/24-post-processing.html | 1 |  |
| docs/tutorials/49-touch-input.html | 1 |  |
| docs/tutorials/53-effect-parameter.html | 1 |  |
| docs/tutorials/58-normal-mapping.html | 1 |  |
| docs/tutorials/59-shadow-mapping.html | 1 |  |
| docs/tutorials/63-stencil-buffer.html | 1 |  |
| docs/tutorials/68-terrain.html | 1 |  |
| docs/tutorials/69-water.html | 1 |  |
| docs/tutorials/75-lod.html | 1 |  |
| docs/tutorials/79-debugging.html | 1 |  |
| docs/tutorials/85-vulkan-backend.html | 1 |  |
| docs/tutorials/87-custom-backend.html | 1 |  |
| docs/tutorials/88-device-layer.html | 1 |  |
| docs/tutorials/97-networking.html | 1 |  |
| docs/video-playback.html | 1 |  |
| docs/vs-alternatives.html | 1 |  |
| **Total** | **197** | 104 pages; of which [policy-c]/[R3] (C ABI 0.44.0 / cna-cs on my pages, not Apple claims): 23; Apple/Metal/iOS STALE: 174 |

## Applied

Phase B, 2026-10-09, by the Apple/C API/CNA.NET agent. Only pages that this agent owned were edited. No generator was run, and nothing was built.

### Files edited (53)

- **Apple/Metal:**
  - docs/tutorials/109-metal-macos.html (body rewritten; old ids kept; new `#m4-evidence`)
  - deep-dives/platforms/android-and-apple-platforms.html
  - deep-dives/renderers/native-gpu-evidence-tiers.html
- **C API:**
  - docs/c-api.html
  - deep-dives/reference/c-api-evidence-and-gates.html
  - deep-dives/reference/native-c-api.html
  - development/internals/bindings/c-api-internals.html, csharp.html, java.html, python.html
  - development/handbook/update-the-c-api.html
  - docs/tutorials/129-c-api-first-program.html
- **CNA.NET (cna-cs to cna-dotnet; ABI 0.46.0; osx-arm64 evidence):**
  - docs/cna-net.html
  - docs/migrating-to-cna-net.html
  - tutorials 170 and 171
- **sharp-runtime:**
  - deep-dives/sharp-runtime/components-and-consumption.html, parity-and-verification.html, object-model-and-core-types.html, streams-text-and-tasks.html
  - These stay on next @ 41b918c9, marked "not re-read". parity-and-verification adds the 62952ef5 M4 suite: 18,084 run, 18,059 passed, 0 failed, 25 skipped. The 18,127 figure is not cited.
- **Graphics (retired renderers removed; 14 identities and 12 families; EasyGL = 3 profiles; compiled effects on 11 of 14; Metal capabilities per AM4-038/077/097/141..148):**
  - docs/3d-rendering.html, render-targets.html, effects.html, shader-effects.html, graphics-state.html
  - tutorials 52, 59–69, 72, 85, 87, 101, 102 (rewritten, three GL profiles plus `#macos`), 103 (rewritten: "Direct3D 9 and 11 on Windows"), 105 (rewritten: "Browser Renderers: WebGL 2 and WebGPU"; its CNA-BUG-199 issue block was removed), 126, 128, 131, 132, 133, 150, 151, 152.

### Decisions followed

- **ABI 0.46.0** (0x00002E00): the page names the 14 current renderer constants and `CNA_NATIVE_WINDOW_SYSTEM_UIKIT`, and says that older bindings must be regenerated or re-reviewed. CNA.NET admitted 0.46.0 at 8219a6c. The withdrawn constants and 0.45.0 are not narrated.
- **METAL:** described as supported, not primary-production (AM4-159), with its limits:
  - compiled effects opt-in;
  - custom effects SpriteBatch-only MSL;
  - `PresentInterval.Two` presents as One;
  - console locked;
  - no Intel Mac.

  New code fact found while editing: METAL does not override `ExecutesShaderEffectSourceEXT()`, so it reads false, as on DIRECTX9. Tutorials 151 and 52 say so.
- **iOS pixel probe:** both results are given, always as "iOS Simulator (iPhone 17 profile)". The device build is final-linked and never run.
- **Clone lines:** CNA `-b apple/m4-stabilization`; sharp-runtime and meta-gl on the same-named branch; easy-gl on develop.

### Not done (outside ownership)

- **Generated deep-link and known-issue blocks** still name retired renderers or old ABI facts:
  - DIRECTX12 cards on 52, 103, render-targets, shader-effects and graphics-state;
  - the "five GL profiles" card on 102;
  - the CANVAS card on 105;
  - "C ABI 0.44.0" and "18 public renderer identities" cards on c-api, c-api-internals and update-the-c-api.
- **Global renderers sidebar:** "DIRECTX11/12 resources" and "Canvas 2D renderer" (e.g. native-gpu-evidence-tiers lines 88 and 91).
- **tutorials.html cards** still show the old titles for 103 ("Direct3D 11 and 12 on Windows") and 105 ("Browser Renderers: WebGL, Canvas and WebGPU").
- **Known issues:** not edited. CNA-VGAP-008's title still says "one iOS simulator frame", although R5 marked it EDIT. CNA-BUG-056's title should be checked against ABI 0.46.0.
