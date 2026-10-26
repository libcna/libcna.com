# R2 — Deep Dives, CNA B=c1c316b9 → T=c6dec91f

INTERNAL AUDIT RECORD (not served). This file names retired renderer identities; the public pages must not.

Scope: `deep-dives/**` (117 HTML pages; 4 future tombstones excluded from rewriting:
`renderers/{direct3d11-and-12-resources,sdl-renderer-2d-contract,vulkan-deferred-state-and-descriptors,vulkan-presentation-and-readback}.html`).
CNA was read only through Git objects (`git show/log/diff/grep/ls-tree` at B and T) and the extracted tree
`~/.cache/libcna-com/cna-target` (stamp = T). Nothing in CNA was built or run. No commit, push, `regenerate_site.sh`,
`build_site_indexes.py`, `apply_expansions.py fold` or `site_deep.py hubs` was run. Generated regions (sidebar,
breadcrumb, pager, `p3:deep-links`/`p3:issue-links`, `<!--issue:KEY-->` text) were not edited; hub `deep-list` items were
hand-synced to the page meta descriptions exactly as `site_deep.py hub_body()` would render them.

Facts used are those of `00-editorial-guide.md` and `R1-renderers-platforms-numbers.md`, plus the T evidence named per page.

## 1. Pages re-verified at T (callout → "checked by reading the CNA source at commit c6dec91f")

| Page | What changed | CNA evidence at T |
|---|---|---|
| renderers/native-gpu-evidence-tiers | Rewritten for the two modern native identities (SDL_GPU, WEBGPU); tables, refusal examples, driver-axis and defect shapes rewritten; links to tombstoned Vulkan pages → presentation-and-backbuffer-readback; internals vulkan link removed | `modules/renderers/sdl-gpu/**`, `modules/renderers/webgpu/**`, `.github/workflows/{platform-ci,apple-ci,d3d-windows-ci,gltf-renderer-stride-ci}.yml`, `handoff.md` §5 |
| renderers/direct3d-evidence-and-wine | Full rewrite: DIRECTX9 + SDL_GPU on SDL's Direct3D 12 driver under vkd3d-proton; sections `discriminating-fixtures`, `debug-layers` removed (no inbound site links); p3 `wpb6-posix-setenv-gate` rewritten | `scripts/run-wine-dxvk9.sh`, `scripts/run-wine-vkd3d{,-headless}.sh`, `cmake/Tests/UnitTests.cmake`, `modules/renderers/directx9/examples/CMakeLists.txt`, `d3d-windows-ci.yml`, `scripts/check_no_posix_setenv.py` |
| renderers/direct3d-presentation-and-state | Full rewrite DIRECTX9-only; section `flip-model` removed | `modules/renderers/directx9/src/{DirectX9Renderer,D3D9RenderTargets}.cpp` |
| renderers/direct3d-shadereffect-contract | Full rewrite (title "Custom HLSL ShaderEffect on DIRECTX9" in `<title>`, og, JSON-LD, h1); sections `d3d11-vs-d3d12`, `history` removed; new `other-renderers`; new SM3 example (not compiled) | `modules/renderers/directx9/src/D3D9EffectDraw.cpp`, `D3D9CompiledEffect.cpp`, effect renderer sources |
| renderers/direct3d9-xna-fidelity | Effect-reach table, fifth pixel-lighting shader, failed-Reset → device lost (d0cea7036), marker/recovery paragraph, RT storage/format bullets | `modules/renderers/directx9/src/**` |
| renderers/presentation-and-backbuffer-readback, webgpu-renderer-semantics, sdl-gpu-pipeline-state-and-draw-order, sdl-gpu-resources-and-frame-recovery, renderer-contract, render-targets-clears-and-viewports, easygl-gl-profiles, index | Retired families removed; SDL_GPU/WEBGPU facts (occlusion, Immediate caveat, zero-area scissor, WEBGPU Supported); renderer-contract p3 `wpb3-missing-vertex-inputs` rewritten around `GraphicsDevice::RequireStockEffectInputs`; WebGPU callout now says CI configures WEBGPU (platform matrix, glTF stride workflow, Emscripten bundle) | renderer sources, `IGraphicsRenderer.hpp`, `GraphicsDevice.cpp`, `deferred_scissor_capture_test.cpp`, workflows |
| graphics/state-objects, render-target-semantics, spritebatch-sorting-and-batching (id `sdl-renderer` removed), compiled-effects-semantics, shader-routes-four-answers, capability-model-and-evidence | Counts (17 capabilities, 8 identities/6 families compiled effects, 5 options), retired rows removed | `CNA/GraphicsCapability.hpp`, `CMakeLists.txt` options, renderer `SupportsCapability` bodies |
| build/configuring-cna, third-party-dependencies, dependency-boundaries | Defaults table, version banner 0.1.0, CMake ≥3.30 for shared builds, SDL_image gone, sibling version checks (DependencyVersions.cmake: compatible = same minor, ≥ stated patch), C++ SDK (CNA_INSTALL_CXX), link-footprint gates (new h3 `footprint`) | `CMakeLists.txt`, `cmake/{DependencyVersions,ThirdPartySDL,SharedRuntimePolicy,RendererIdentityDefault}.cmake`, `cmake/Tests/LinkFootprint.cmake`, `.gitmodules` |
| verification/oracles-and-engagement (p3 `wpb6-pixel-harness-contract`), test-populations-and-gates | Test numbers 898/855/11,898; 625 planned; registration counts per family | `git ls-tree`/`git grep` at T, `cmake/UnitTests.cmake`, renderer example CMake |
| reference/c-api-evidence-and-gates | C ABI 0.50.0, 60 headers, 3,212 routes, generated routes, gate 625 planned, CNA.NET 0.47.0 | `modules/c-api/include/CNA/C/abi.h`, `docs/c-api/{RELEASE_GATE,COVERAGE,LIMITATIONS,GENERATED_ROUTES}.md`, `tools/c-api/abi_baseline.json` |
| reference/glossary (p3 `wpb7-name-cna`, `wpb7-backend-vocabulary`) | Terms `term-directx11`, `term-metal`, `term-sdl-renderer`, `term-vulkan` removed; alpha.1 → prerelease history, snapshot term (next, 812 commits after v0.1.0), C ABI 0.50.0, 10 identities/8 families, defaults, SDL_GPU/WEBGPU status, GraphicsRendererCategory/Maturity (+ getters), 17 capabilities, profile 31 features/8 limits, parity fixtures on 3 families, PBR shading on all 6 pixel families, lazy XNB reader install, VertexDeclaration binds lazily | `CNA/GraphicsRenderer{Category,Maturity}.hpp`, `RendererCapabilityProfile.hpp`, `IGraphicsRenderer.hpp` (`ShadesPbrEffectEXT`), `ContentManager.hpp`, `ContentTypeReaderManager.cpp`, `VertexDeclaration.cpp`, `parity/ParityFixtures.cmake` |
| reference/graphics-quick-reference | 8 families; indirect draw family removed; compiled effects five more families/seven identities | `GraphicsDevice.hpp`, `SkinnedEffect.hpp` |
| reference/gltf-evidence-matrix | Specular maps sampled by all six PBR families; L7 golden sets now OPENGLES3 + SOFTWARE; GLTF ROBUST row 12 restated per plan; link to `docs/gltf-limitations.md` | `GltfRendererPbrFallbackPolicyTests.cpp`, `GltfFixtureCorpusTests.cpp` (2 golden policies), `plans/plan_gltf.md` §27.2, `docs/gltf-limitations.md` |
| reference/verification-tiers | 18 files/25 jobs; 6 C-ABI workflows (header compile only); 625; general job fails on any failure (no expected-failure list); sibling_branch.sh; platform matrix OPENGLES3/SDL_GPU/WEBGPU/SOFTWARE; Apple jobs (SOFTWARE build, SDL_GPU Metal smoke, iOS SOFTWARE + non-gating SDL_GPU); D3D workflow DIRECTX9 + SDL_GPU D3D12 legs; GPU validation (SDL_GPU debug mode in Debug, WebGPU error scopes); goldens; backlog table now explicitly "re-verified at c1c316b9" | `.github/workflows/*.yml` (parsed), `scripts/ci/sibling_branch.sh`, `SdlGpuRenderer.cpp` (debugModeEnabled), `WebGPURenderer*.cpp` (PushErrorScope), `examples/golden`, `CrossFamilyPrograms.cmake` |
| reference/cnaext-catalog | Compute work-group limits and indirect draws removed; BaseInstance only SDL_GPU; graphics-ext 73 tests, post_process without HLSL; CNAEXT marker recount (method reproduces B exactly: 1,840/321 and 2,280/343) → T 1,861 in 323, 2,274 in 340 `.hpp`, 2,306 in 345 | `git cat-file` over `modules/*/include` at B and T; `modules/graphics-ext/**`; all 180 identifiers on the page grepped at T |
| platforms/windows-cross-compiling-and-wine | DIRECTX9-only cross route (command example, emulator, prefixes incl. spike prefix, allow-WineD3D switch), SDL3_image gone, d3d-windows-ci legs, retired-renderer rows/paragraph (Windows 11 laptop baseline) removed | `cmake/Tests/UnitTests.cmake:1261`, `cmake/Harnesses.cmake:210`, `scripts/run-wine-dxvk9.sh`, `modules/renderers/directx9/examples/CMakeLists.txt`, `cmake/ThirdPartySDL.cmake` |
| platforms/cross-platform-contract | Vulkan-surface bridge gone (`IPlatformVulkanSurface` deleted), 31 platform capability flags, SDL-linking renderers SDL_GPU/FNA3D, OS partitions DIRECTX9/WEBGL2, RendererWindowKind None/Plain/OpenGL, automatic fallback order (HEADLESS then STUB last), evidence table rows | `IPlatform.hpp`, `PlatformCapabilities.hpp`, `SdlAvailability.cmake`, `RendererCombinations.cmake`, `GraphicsRendererDescriptor.hpp`, `GraphicsRendererSelection.hpp`, workflows |
| platforms/android-and-apple-platforms | Defaults (SDL_GPU on Apple, OPENGLES3 on Android), iOS allow-list SOFTWARE/SDL_GPU, macOS section rewritten (SDL_GPU on Metal, shadercross, M4 campaign survivors only, apple-ci jobs), iOS matrix rewritten, UIKit SDL patch named; old links to retired Metal files removed; Tutorial 109 link text | `cmake/{ApplePlatform,RendererIdentityDefault}.cmake`, `apple-ci.yml`, `docs/apple-platforms.md`, `cmake/patches/sdl-cbe3fbe9-0005-uikit-scene-window-frame.patch`, `StorageDevice.cpp` |
| foundations/compatibility-and-evidence (p3 `wpb7-claim-scopes`) | Renderer classes 4 (2D row removed), defaults, 17 capabilities, profile 31/8, MRT cube refusal DIRECTX9+SDL_GPU, ThreeD false only on STUB, 10 identities, 898/11,898, CNAEXT recount, README now fixed (only "0/31" remains) | `HeadlessRenderer.cpp`, `StubRenderer.hpp`, `DirectX9Renderer.cpp:1600`, `SdlGpuRenderer.cpp:5040`, `README.md` |
| foundations/ecosystem | Diagram (sharp-runtime branch next, snapshot c6dec91f), sibling version checks, clone URL now libcna, cna-examples renderer clause dropped, CNA.NET 0.47.0 | `CMakeLists.txt:278-296`, `cmake/RendererSelection.cmake:155-170`, `DependencyVersions.cmake` |
| foundations/cna-and-xna | CNA.NET 0.47.0 (not 0.50.0), 10/8, compiled effects 8/10 with five options, DIRECTX9 + SDL_GPU D3D12 row, version identity (0.1.0, empty prerelease, tag v0.1.0), README goals wording, test counts, lazy XNB readers | `CMakeLists.txt:3,12`, `cmake/Version.cmake`, `README.md` §2, `Game.cpp:446` |
| practice/project-records-and-evidence | Records table rewritten (handoff.md replaces NEXT.md; AUDIT.md, remediation archive and integration/ no longer in tree, named as Git history); plans 63/69; RRC-051 example replaces REMED-GFX-188; 625; descriptor gate exception now only directx9; version paragraph 0.1.0/0.50.0; handoff paragraph | `handoff.md`, `AGENTS.md`, `docs/c-api/RELEASE_GATE.md`, `cmake/RendererDescriptorGate.cmake`, `tools/count_webgpu_plan_status.sh`, `git log` deletions (bb6607d34, de310727c, fa70df1ae) |

## 2. Pages edited for the delta but NOT re-verified (callout keeps c1c316b9, wording "source-verified at the stated evidence commit")

renderers/easygl-state-and-resource-semantics (pass-order list); graphics/texture-data-transfer (SDL3_image sentence),
stock-effects-semantics, spritebatch-semantics, spritefont-text-layout, surface-formats (p3 `wpb2-renderer-texture-maximum`,
linear-colour section), vertex-and-index-buffers, vertex-streams-and-declarations, graphicsdevice-contract (diagram 1 of 8),
device-reset-and-lifetime; build/module-architecture (8 families, links), tools-and-scripts (p3 `wpb6-smoke-orchestrator`,
598 example programs); reference/native-c-api (versions, route table, selection bullets), ecosystem-quick-reference (CNA.NET
0.47.0, sharp-runtime version check); services/avatars (gamer-services option, retired registrations removed),
input-model (coordinate table rows), gamer-services-contract (audit record now unlinked, "read at c1c316b9");
platforms/web-build-and-main-loop (host gate sentence); practice/porting-case-studies, migrating-an-xna-game,
xna-api-surface-auditing (compiled-effect counts); models/gltf-conformance (L7 reports 2, CI matrix, ROBUST rows),
vertex-packing-and-strides (stride-table renderers from `VertexDeclarationFidelity.hpp`, CI matrix), gltf-import (6 PBR
families), model-mesh-runtime (Ensure3DSupported, model test registrations SDL_GPU + Software); framework/
window-and-device-manager (UpdatePresentationFormatEXT 5 families, DXGI sentence removed), game-time-and-timestep
(PresentInterval.Two per family; link → internals sdl-gpu), game-class-and-lifecycle (F9/F10 overrides EasyGL/DIRECTX9/
WEBGPU; AUDIT.md unlinked), first-game-walkthrough (SDL_GPU/SOFTWARE paragraph), math-coordinate-conventions
(SDL_GPU y-flip example), services-and-components; siblings/easygl-and-metagl (version checks; integration records
unlinked); sharp-runtime/components-and-consumption (next branch, version check); content/contentmanager-resolution-rules
and xnb-container-and-object-graph (lazy reader installation, `RegisterBuiltinLoaders()`).

Pages not edited apart from callout wording ("stated evidence commit") and doc-meta: content/cnj-documents,
content-robustness, xnb-type-readers; foundations/language-conventions; framework/bounding-volumes-and-intersections,
curve-evaluation, exit-and-shutdown-semantics, math-value-types-and-layout, rectangle-point-and-color,
vector-matrix-numerics; graphics/effect-object-model, resource-lifetime; models/cnj-toolchain, skinning-and-animation;
services/gamepads-and-haptics, host-devices, media-contract, network-sessions, sensors-and-vibration,
sound-effects-and-streaming, text-input-and-ime, touch-and-gestures, xact-runtime; sharp-runtime/object-model-and-core-types,
parity-and-verification, streams-text-and-tasks.

doc-meta "source links pinned to" → c6dec91f on every non-tombstone page (all remaining CNA links are pinned to T).

## 3. Links re-pointed away from the tombstones

native-gpu-evidence-tiers (Vulkan presentation/deferred-state → presentation-and-backbuffer-readback; internals vulkan
link dropped); renderers/index (4 tombstone entries removed from the hub list); game-time-and-timestep
(`internals/graphics/vulkan.html#swapchain` → `internals/graphics/sdl-gpu.html`); glossary related link text; Tutorial 109
link text (android-and-apple). No non-generated deep-dives link to a tombstone, to `internals/graphics/vulkan.html` or to
`tutorials/85-vulkan-backend.html` remains (sidebar and pager links are generated).

## 4. Ids removed / added

Removed: build — none; graphics/spritebatch-sorting-and-batching `sdl-renderer`; reference/glossary `term-directx11`,
`term-metal`, `term-sdl-renderer`, `term-vulkan`; renderers/direct3d-evidence-and-wine `debug-layers`,
`discriminating-fixtures`; renderers/direct3d-presentation-and-state `flip-model`; renderers/direct3d-shadereffect-contract
`d3d11-vs-d3d12`, `history`. Added: build/dependency-boundaries `footprint`; direct3d-shadereffect-contract `other-renderers`.
Inbound links: only from the tombstone `sdl-renderer-2d-contract.html` (#sdl-renderer, ×2) and from
`audit/bible-absorption-phase3-concepts.md` rows (WP05-ch13-058/059, WP10-ch28-064..068, WP10-ch28-106, WP11-ch30-017).

## 5. p3 regions edited

tools-and-scripts `wpb6-smoke-orchestrator`; compatibility-and-evidence `wpb7-claim-scopes`; surface-formats
`wpb2-renderer-texture-maximum`; glossary `wpb7-name-cna`, `wpb7-backend-vocabulary`; direct3d-evidence-and-wine
`wpb6-posix-setenv-gate`; renderer-contract `wpb3-missing-vertex-inputs`; oracles-and-engagement
`wpb6-pixel-harness-contract`. (Other p3 diffs against HEAD are SHA re-pins only.)

## 6. Statements removed or reclassified (beyond retired-renderer removals)

* "FNA3D refuses PBR draws" → every pixel family (incl. FNA3D) reports `PbrEffectShading` (`ShadesPbrEffectEXT`).
* "Game registers the 61 XNB readers in its constructor; a stand-alone ContentManager must register them" → declared by
  Game, installed per type on first `Load<T>` (also stand-alone); `RegisterBuiltinLoaders()` for hosts.
* "No workflow selects WEBGPU" (webgpu callout) → false at T; corrected.
* README Usage-Example defect and README 3,467/3,627 figure → fixed at T (kept as dated history at c1c316b9).
* NEXT.md / AUDIT.md / remediation / integration records → no longer in tree; reclassified as Git history, unlinked.
* "CNA does not pin / checks nothing" (siblings) → pins no commit but checks declared versions since 0.1.0.
* Earlier 31-finding backlog table (verification-tiers) → explicitly dated "re-verified at c1c316b9".

## 7. Checks (deep-dives only)

* `check_retired_renderers.py`: remaining deep-dives hits are the 4 tombstones and generated sidebar/pager links
  (renderers group nav still lists the tombstone titles) on direct3d-presentation-and-state, direct3d-shadereffect-contract
  and every renderers page sidebar.
* `check_facts.py`: no deep-dives finding except the tombstones.
* `check_source_links.py`: no deep-dives error.
* `validate_site.py`: deep-dives issue only `sdl-renderer-2d-contract.html` → `spritebatch-sorting-and-batching.html#sdl-renderer`
  (tombstone-to-be).
* `check_deep_page.py --all`: deep-dives errors only on the 4 tombstones and the pager of direct3d-presentation-and-state /
  direct3d-shadereffect-contract (generated, neighbours are tombstones).
* `site_deep.py check`: OK (431 declared, 431 on disk).

## 8. Findings and uncertainties for the coordinator

* Manifest: title of `renderers/direct3d-shadereffect-contract` is now "Custom HLSL ShaderEffect on DIRECTX9" (hub list uses
  it); the renderers group intro still says "portable 2D"; sidebars/pagers list the 4 tombstones.
* Generated "related deep dives" lists elsewhere (docs/, development/, tutorials) still show old titles/descriptions of
  direct3d-*/native-gpu-evidence-tiers pages ("What VULKAN, …") — need regeneration.
* CNA-VGAP-025 title stale (CI selects WEBGPU and SDL_GPU at T); CNA-BUG-012 likely resolved (SDL_GPU occlusion limitation
  test checks both seams); CNA-BUG-113 describes retired renderers; CNA-BUG-133 (DIRECTX9 never registers for window) still
  holds at T.
* STUB answers false for every capability, including ThreeD (`StubRenderer.hpp:180`) — R1's "every surviving renderer
  answers ThreeD true" is wrong for STUB.
* Immediate SpriteBatch defect (handoff §5.1, reproduced 2026-10-17) vs commit 3b6a2eaf3 (2026-10-22) "Honor Immediate
  submission on WebGPU and D3D9" — pages keep the handoff wording; needs a decision.
* FNA3D now shades PBR — check docs/effects.html#noxna-effects and other user pages.
* `audit/bible-absorption-phase3-concepts.md` rows point at removed anchors (see §4).
* Anchors used by deep pages on pages other agents rewrite: docs/tutorials/103 and 109, docs/rendering-backends.html
  (#modern-gpu, #capability-matrix, #windows-directx, #shaders, #gl-family, #at-a-glance).
* Two pages carried c6dec91f callouts from an earlier pass without being in the re-verified list (graphics/surface-formats,
  reference/native-c-api); reverted to the c1c316b9 "stated evidence commit" form to stay conservative.
* MojoShader patch count at B was 128 by file count (site said 124); T count 133.
