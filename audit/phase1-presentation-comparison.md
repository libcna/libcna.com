# Phase 1 — whole-site presentation comparison

`LIBCNA_PRESENTATION_BASE` (`be359024e3012653fa1e4963eb3ef86d9c16a5b7`, the deployed site) against the Phase-1 working tree,
produced by `python3 scripts/compare_presentation.py --report audit/phase1-presentation-comparison.md`. Every baseline
heading, anchor id, CTA (label/href/prominence), significant link, card, image, video, statistic, table and major block was
extracted mechanically into `audit/data/phase1-baseline-inventory.json` *before any edit* and is compared with the current site.
An item counts as preserved when a current item with the same href / src / video id / id anchor / (fuzzy) title exists; a
difference that is not a loss (an updated statistic value, a retitled heading whose id survives) is listed as a note; every other
difference must be justified in `audit/data/phase1-dispositions.json` (rendered as the table below) or it fails the run.

## Result

| | Baseline | Outcome |
|---|---:|---|
| HTML pages | 174 | 171 kept, **3 removed** (tutorials whose whole subject is retired renderers), **33 new** pages (8 reference pages, 25 tutorials) → 204 |
| Pages that grew by ≥ 20 % (visible words) | – | 134 (no page shrank by ≥ 10 %) |
| Headed major blocks (`section`, `demo-platform`, hero, page header) | 48 | 34 grew by ≥ 20 %, 13 updated in place at similar size, 1 renamed (dispositioned) |
| Headings compared (h1–h3, plus h4 outside tutorials) | 2,090 | **2,059 preserved** (title or anchor matched), 31 dispositioned |
| CTAs / buttons | 79 | 73 keep their exact href; 6 changed, all dispositioned (dead link replaced, or retired-renderer subject replaced in place) |
| **Primary CTAs (`btn-primary`)** | **22** | **22 preserved** — same href, still primary; **0 downgraded** |
| Cards / callouts (by title) | 669 | 627 preserved, 42 dispositioned (false or obsolete lead sentence corrected in place, or retired-renderer card replaced in place) |
| Images | 52 | **52 kept** (the architecture diagram was redrawn at the same path because its old content was false) |
| Videos / embeds | 13 | 10 kept; 3 empty `TODO_VIDEO_ID` placeholders replaced by 5 real videos |
| Homepage Quick Stats | 8 | 8 kept and updated + 2 added (10) |
| Tables | 292 | preserved by header/purpose; 1 dispositioned |
| **Unexplained losses** | | **0** |

Owner-designated content: homepage Quick Stats (present, 10 stats), Showcase "Verification against the real XNA runtime" (present, 804 words,
8 cards, 4 oracle images), Demos → Speedy Blupi (present, 254 words, 3 items) with the primary blue `Play in Browser` → `https://speedyblupi.com/SpeedyBlupi2013/`
(live: HTTP 200, `text/html`, checked 2026-09-24). Enforced by `python3 scripts/validate_presentation.py`.

- baseline pages compared: 174
- unexplained losses: **0**
- dispositioned differences: **98**
- notes (updates/adjustments that are not losses): 30

## Dispositioned differences

| Page | Kind | Item | Disposition | Reason |
|---|---|---|---|---|
| `about.html` | link | CNA Craft -> https://github.com/libcna/cna-craft | dead link replaced | github.com/libcna/cna-craft is HTTP 404; the source lives as a subtree of libcna/cna-lab. Same link label, working destination. |
| `contact.html` | heading | bgfx | removed-functionality (replaced in place) | The card described the dependency library of a retired renderer. Replaced in the same slot by an FNA3D card; sharp-runtime and easy-gl/meta-gl cards were added. |
| `contact.html` | cta | bgfx docs ↗ -> https://bkaradzic.github.io/bgfx/ | removed-functionality (replaced in place) | Documentation link for the retired renderer's dependency; the card now links FNA3D documentation (github.com/FNA-XNA/FNA3D, HTTP 200). |
| `contribute.html` | heading | bgfx 32-bit index buffers | removed-functionality | Task card about a renderer that CNA retired; its subject no longer exists. Replaced by current task cards (cube-face MRT, parity-fixture registration, oracle re-measurement). |
| `contribute.html` | heading | bgfx D3D and Metal shader variants | removed-functionality | Task card about a renderer that CNA retired; subject no longer exists. |
| `contribute.html` | heading | DIRECTX12 scissor, viewport, stencil and blend factor | false claim removed | The card claimed DIRECTX12 lacked these four states; at TARGET all four are implemented (OMSetStencilRef, OMSetBlendFactor, RSSetScissorRects, RSSetViewports in DirectX12Renderer.cpp). |
| `contribute.html` | heading | Draw-offset handling | false claim removed | The card claimed DIRECTX11 ignored draw offsets; at TARGET it passes startIndex and baseVertex to DrawIndexed (REMED-GFX-020). |
| `contribute.html` | link | NOTICE.md -> https://github.com/libcna/cna/blob/master/NOTICE.md | destination updated | github.com/libcna/cna/blob/master/... does not exist (master branch absent; GitHub redirects to alpha.1 develop). Link now pins the documented snapshot commit. |
| `contribute.html` | link | THIRD_PARTY_NOTICES.md -> https://github.com/libcna/cna/blob/master/THIRD_PARTY_NOTICES.md | destination updated | github.com/libcna/cna/blob/master/... does not exist (master branch absent; GitHub redirects to alpha.1 develop). Link now pins the documented snapshot commit. |
| `contribute.html` | card | bgfx 32-bit index buffers | removed-functionality | Task card about a renderer that CNA retired; its subject no longer exists. Replaced by current task cards (cube-face MRT, parity-fixture registration, oracle re-measurement). |
| `contribute.html` | card | bgfx D3D and Metal shader variants | removed-functionality | Task card about a renderer that CNA retired; subject no longer exists. |
| `contribute.html` | card | DIRECTX12 scissor, viewport, stencil and blend factor | false claim removed | The card claimed DIRECTX12 lacked these four states; at TARGET all four are implemented (OMSetStencilRef, OMSetBlendFactor, RSSetScissorRects, RSSetViewports in DirectX12Renderer.cpp). |
| `contribute.html` | card | Draw-offset handling | false claim removed | The card claimed DIRECTX11 ignored draw offsets; at TARGET it passes startIndex and baseVertex to DrawIndexed (REMED-GFX-020). |
| `demos.html` | heading | Input — 50 demos | updated in place | Counts refreshed: cna-examples README at ea33c9a29 lists Input at 52 screens; item retitled 'Input — 52 screens' with richer text. |
| `demos.html` | heading | Audio — 10 demos | updated in place | Counts refreshed: Audio is 12 screens at ea33c9a29; item retitled and expanded (XACT added). |
| `demos.html` | heading | Not yet written | false claim replaced | 'Devices, Net, Media, 2D and 3D Graphics are empty' is false at ea33c9a29: all 13 areas are populated (249 screens). Replaced by 'Graphics — 83 screens' and 'Framework, Math, Content, Media, Devices, Net and more' items. |
| `demos.html` | card | Why 23 samples do not build. | false claim corrected | '23 samples do not build because of .fx' is false at cna-samples 4da98a0 (all named shader samples are complete). The callout is preserved in place with the corrected story and pinned facts. |
| `demos.html` | card | Early — two of seven areas are populated. | false claim corrected | 'Early — two of seven areas populated, no tests' is false at ea33c9a29; replaced in place by a corrected callout 'Broad, with a catalogue checker'. |
| `demos.html` | card | Input — 50 demos | updated in place | Counts refreshed: cna-examples README at ea33c9a29 lists Input at 52 screens; item retitled 'Input — 52 screens' with richer text. |
| `demos.html` | card | Audio — 10 demos | updated in place | Counts refreshed: Audio is 12 screens at ea33c9a29; item retitled and expanded (XACT added). |
| `demos.html` | card | Not yet written | false claim replaced | 'Devices, Net, Media, 2D and 3D Graphics are empty' is false at ea33c9a29: all 13 areas are populated (249 screens). Replaced by 'Graphics — 83 screens' and 'Framework, Math, Content, Media, Devices, Net and more' items. |
| `docs/building.html` | heading | SKIA: missing CNA_SKIA_ROOT | removed-functionality | Troubleshooting entry for a renderer that CNA has retired (its option and dependency no longer exist); other troubleshooting entries are kept. |
| `docs/content-pipeline-xnb.html` | heading | XNB Content Pipeline | retitled (URL and anchors kept) | CNA now has a real build-time Content Pipeline that writes XNB and CNB (docs/content-pipeline.html); this page's subject is XNB loading and interoperability, so the h1 is 'XNB Loading & Interoperability'. The page keeps its URL, every anchor and its depth. |
| `docs/faq.html` | link | LICENSE file -> https://github.com/libcna/cna/blob/master/LICENSE | destination updated | github.com/libcna/cna/blob/master/... does not exist (no master branch); every LICENSE link now pins the documented snapshot commit. |
| `docs/migration-from-monogame.html` | card | Alpha.1 status: | updated in place | The status callout described the alpha.1 tag; it now describes the documented development snapshot in the same slot. |
| `docs/packed-vector.html` | card | These are vertex formats, not texture formats, in practice. | updated in place | Statement refined: packed/float formats are mainly vertex formats but texture use is doubly gated (profile gate and per-renderer classification), which is what the current callout explains. |
| `docs/rendering-backends.html` | card | DIRECTX3 is not the old DX3 . | removed-functionality | The callout warned that a look-alike renderer identity exists; that identity is retired and refused at configure time, so the warning is obsolete. Replaced in place by a 'Case matters in CMake, not at run time' callout. The old-name -> FREEDIRECT translation row is kept. |
| `docs/sensors.html` | heading | AccelerometerState members | false claim corrected | No AccelerometerState/GetState exists at TARGET; sensors are instance classes. The section is replaced in place by 'AccelerometerReading members' documenting the real type. |
| `docs/storage.html` | card | Implementation status: 100% functionally complete. | unsupported claim narrowed | '100% functionally complete' is unsupported (StorageDevice::DeviceChanged is never raised, web has no persistence); the callout keeps its slot with the verified status. |
| `docs/tutorials/02-setup.html` | card | FFmpeg is a hard requirement on Linux and macOS. | false or obsolete claim corrected in place | false at the snapshot: FFmpeg is optional (CNA_ENABLE_VIDEO); video throws NotSupportedException at run time without a backend. The callout keeps its slot and is now 'FFmpeg is optional.' with the corrected content. |
| `docs/tutorials/104-directx-ladder.html` | page | docs/tutorials/104-directx-ladder.html | page removed (removed functionality) | The tutorial's purpose depends entirely on functionality that no longer exists: its entire subject is a group of legacy-API renderers that CNA has retired; its only surviving content (the GDI row and the WarnAndStub snippet) is carried by tutorial 101. The 'Renderers in Depth' section keeps tutorials 101-103, 105 and 107-109 and gains 130-133 for the current renderers. |
| `docs/tutorials/106-vector-renderers.html` | page | docs/tutorials/106-vector-renderers.html | page removed (removed functionality) | The tutorial's purpose depends entirely on functionality that no longer exists: its entire subject is three vector/2D-rasterizer renderers that CNA has retired. The 'Renderers in Depth' section keeps tutorials 101-103, 105 and 107-109 and gains 130-133 for the current renderers. |
| `docs/tutorials/112-gltf-animation.html` | card | Mixed skin and extra rigid tracks remain an alpha boundary. | reworded in place | The alpha.1-era wording no longer fits the snapshot; The callout keeps its slot and is now 'Mixed skin and extra rigid tracks remain a boundary at this snapshot.' with the corrected content. |
| `docs/tutorials/114-pbr-materials.html` | card | There is no image-based lighting. | false or obsolete claim corrected in place | false at the snapshot: image-based lighting (ImageBasedLightEXT) and shadow receiving exist in the CNAEXT engine layer. The callout keeps its slot and is now 'Factor-only PBR was fixed in alpha.1, and still holds.' with the corrected content. |
| `docs/tutorials/114-pbr-materials.html` | card | Factor-only PBR is fixed in alpha.1. | reworded in place | The alpha.1-era wording no longer fits the snapshot; The callout keeps its slot and is now 'Factor-only PBR was fixed in alpha.1, and still holds.' with the corrected content. |
| `docs/tutorials/116-post-process-effects.html` | card | These run only where custom ShaderEffect s run. | reworded in place | The alpha.1-era wording no longer fits the snapshot; The callout keeps its slot and is now 'These run only where the renderer takes one of their shader variants.' with the corrected content. |
| `docs/tutorials/117-devices-layer.html` | card | The CI job that covers this layer is dormant on ordinary development pushes. | false or obsolete claim corrected in place | no longer true: the devices workflow now triggers on next/develop/main pushes. The callout keeps its slot and is now 'What you’ll learn' with the corrected content. |
| `docs/tutorials/119-3d-audio.html` | card | that instance is 3D for the rest of its life | false or obsolete claim corrected in place | false at the snapshot: Apply3D now follows a pan-versus-3D mode rule, documented in the replacement callout. The callout keeps its slot and is now 'Exactly one listener is heard.' with the corrected content. |
| `docs/tutorials/121-video-playback.html` | card | Two hard platform facts. | false or obsolete claim corrected in place | the FFmpeg restrictions changed (optional backend, run-time NotSupportedException); callout keeps its slot. The callout keeps its slot and is now 'Two facts decide it.' with the corrected content. |
| `docs/tutorials/122-media-library.html` | card | The music scan indexes .ogg , .oga , .mp3 and .wav . | reworded in place | The alpha.1-era wording no longer fits the snapshot; The callout keeps its slot and is now 'The music scan indexes .ogg , .oga , .mp3 , .wav , .flac and .opus — a' with the corrected content. |
| `docs/tutorials/124-web-gotchas.html` | card | On Emscripten, allocate your Game subclass with new . A stack-allocated one is silently co | false or obsolete claim corrected in place | obsolete: Game::Run() now blocks through Asyncify, so a stack-allocated Game is fine on Emscripten. The callout keeps its slot and is now 'In this snapshot a stack-allocated Game is fine on Emscripten — if you' with the corrected content. |
| `docs/tutorials/129-c-api-first-program.html` | heading | Tutorial 129: Inspect the Experimental C API Boundary | retitled (premise gone) | The tutorial's premise -- inspecting why the alpha.1 C library could not compile -- no longer holds in source; it is rewritten as 'Your First C Program Against the Experimental C API' (ABI 0.29.0). URL, ids and the honest 'not build-verified' callouts are kept. |
| `docs/tutorials/28-particles-2d.html` | heading | Blending with AdditiveBlend | reworded in place | The alpha.1-era wording no longer fits the snapshot; The heading keeps its slot and is now 'Blending with BlendState::Additive' with the corrected content. |
| `docs/tutorials/35-model-loading.html` | card | Alpha.1 glTF boundaries are explicit. | reworded in place | The alpha.1-era wording no longer fits the snapshot; The callout keeps its slot and is now 'The glTF boundaries are explicit (re-verified at this snapshot).' with the corrected content. |
| `docs/tutorials/43-quaternions.html` | heading | ToMatrix — convert for rendering | reworded in place | The alpha.1-era wording no longer fits the snapshot; The heading keeps its slot and is now 'CreateFromQuaternion — convert for rendering' with the corrected content. |
| `docs/tutorials/45-content-manager.html` | card | CNA is an XNB loader , not a content pipeline. | false or obsolete claim corrected in place | false at the snapshot: CNA also has a build-time Content Pipeline that writes XNB and CNB. The callout keeps its slot and is now 'CNA is both an XNB/CNB loader and, at build time, a content pipeline.' with the corrected content. |
| `docs/tutorials/45-content-manager.html` | card | The readers are not registered automatically. | false or obsolete claim corrected in place | only true for a standalone ContentManager: a Game registers the built-in readers. The callout keeps its slot and is now 'A Game registers the built-in XNB readers for you.' with the corrected content. |
| `docs/tutorials/48-timestep.html` | heading | Physics simulation with fixed step, rendering with interpolation | reworded in place | The alpha.1-era wording no longer fits the snapshot; The heading keeps its slot and is now 'Physics on the fixed step' with the corrected content. |
| `docs/tutorials/49-touch-input.html` | heading | TouchLocation struct | reworded in place | The alpha.1-era wording no longer fits the snapshot; The heading keeps its slot and is now 'TouchLocationState enum' with the corrected content. |
| `docs/tutorials/49-touch-input.html` | heading | GestureSample fields | reworded in place | The alpha.1-era wording no longer fits the snapshot; The heading keeps its slot and is now 'GestureSample members' with the corrected content. |
| `docs/tutorials/50-accelerometer.html` | card | Two things must be true before any of this compiles or runs. | reworded in place | The alpha.1-era wording no longer fits the snapshot; The callout keeps its slot and is now 'Two things to keep straight.' with the corrected content. |
| `docs/tutorials/51-custom-vertex.html` | heading | VertexElement struct | reworded in place | The alpha.1-era wording no longer fits the snapshot; The heading keeps its slot and is now 'VertexElement' with the corrected content. |
| `docs/tutorials/51-custom-vertex.html` | heading | VertexPositionNormalTextureTangent struct + declaration | reworded in place | The alpha.1-era wording no longer fits the snapshot; The heading keeps its slot and is now 'A tangent-space vertex: struct + declaration' with the corrected content. |
| `docs/tutorials/52-custom-shaders.html` | card | Call order matters. | reworded in place | The alpha.1-era wording no longer fits the snapshot; The callout keeps its slot and is now 'ShaderEffect is CNAEXT.' with the corrected content. |
| `docs/tutorials/52-custom-shaders.html` | card | BGFX and SOFTWARE accept a ShaderEffect and silently ignore the source you supplied. | false or obsolete claim corrected in place | names a retired renderer; the surviving statement (SOFTWARE and HEADLESS accept but never execute a ShaderEffect source) keeps the slot. The callout keeps its slot and is now 'SOFTWARE and HEADLESS accept a ShaderEffect and never execute the sour' with the corrected content. |
| `docs/tutorials/53-effect-parameter.html` | card | Call order matters. | reworded in place | The alpha.1-era wording no longer fits the snapshot; The callout keeps its slot and is now 'Call Apply() first.' with the corrected content. |
| `docs/tutorials/58-normal-mapping.html` | card | custom GLSL shader | reworded in place | The alpha.1-era wording no longer fits the snapshot; The callout keeps its slot and is now 'What you’ll learn' with the corrected content. |
| `docs/tutorials/63-stencil-buffer.html` | card | This portable outline example uses ShaderEffect . | reworded in place | The alpha.1-era wording no longer fits the snapshot; The callout keeps its slot and is now 'This outline example uses ShaderEffect , but the stencil technique doe' with the corrected content. |
| `docs/tutorials/71-memory-management.html` | heading | Move semantics | reworded in place | The alpha.1-era wording no longer fits the snapshot; The heading keeps its slot and is now 'Move semantics and copies' with the corrected content. |
| `docs/tutorials/78-multithreading.html` | heading | Audio thread: SDL3_mixer is thread-safe | reworded in place | The alpha.1-era wording no longer fits the snapshot; The heading keeps its slot and is now 'What is thread-safe in CNA?' with the corrected content. |
| `docs/tutorials/81-emscripten.html` | heading | emscripten_set_main_loop() | reworded in place | The alpha.1-era wording no longer fits the snapshot; The heading keeps its slot and is now 'The browser main loop' with the corrected content. |
| `docs/tutorials/81-emscripten.html` | heading | Async file loading (Asyncify) | reworded in place | The alpha.1-era wording no longer fits the snapshot; The heading keeps its slot and is now 'Asset loading: preloading and Asyncify' with the corrected content. |
| `docs/tutorials/83-migrate-monogame.html` | card | Readers are not auto-registered. | false or obsolete claim corrected in place | only true for a standalone ContentManager: a Game registers the built-in readers. The callout keeps its slot and is now 'Reader registration.' with the corrected content. |
| `docs/tutorials/84-migrate-xna.html` | heading | Read-side XNB support | reworded in place | The alpha.1-era wording no longer fits the snapshot; The heading keeps its slot and is now 'XNB support and the content pipeline' with the corrected content. |
| `docs/tutorials/86-bgfx-backend.html` | page | docs/tutorials/86-bgfx-backend.html | page removed (removed functionality) | The tutorial's purpose depends entirely on functionality that no longer exists: its entire subject is a renderer that CNA has retired. The 'Renderers in Depth' section keeps tutorials 101-103, 105 and 107-109 and gains 130-133 for the current renderers. |
| `docs/tutorials/88-device-layer.html` | table | File dialogs are asynchronous Capability Desktop Android iOS Web/Emscripten | reworded in place | The alpha.1-era wording no longer fits the snapshot; The table keeps its slot and is now 'Cancel and error look identical.' with the corrected content. |
| `docs/tutorials/89-sharp-runtime.html` | card | Iterator invalidation is C++'s, not C#'s. | reworded in place | The alpha.1-era wording no longer fits the snapshot; The callout keeps its slot and is now 'There is no doublecs and no boolcs .' with the corrected content. |
| `docs/tutorials/95-speedy-blupi.html` | heading | Original MonoGame codebase | reworded in place | The alpha.1-era wording no longer fits the snapshot; The heading keeps its slot and is now 'What the game code used' with the corrected content. |
| `docs/video-playback.html` | card | Video is effectively native Linux/macOS only today. | false claim corrected | FFmpeg is now optional (CNA_ENABLE_VIDEO); Video/VideoPlayer types link on every target and throw NotSupportedException at run time without a backend. Callout replaced in place. |
| `docs/video-playback.html` | card | Platform restriction — FFmpeg is NOT available on: | false claim corrected | The 'fails to link' restriction is obsolete: video units link everywhere; FFmpeg is simply never built for Windows/Emscripten/Android/iOS. Callout replaced in place. |
| `docs/vs-alternatives.html` | card | Current documented release: 0.1.0-alpha.1. | updated in place | The comparison page documented a release; the callout now names the documented snapshot 009d40f5 (version string still 0.1.0-alpha.1). |
| `docs/xna-compatibility.html` | link | cna-craft -> https://github.com/libcna/cna-craft | dead link replaced | github.com/libcna/cna-craft is HTTP 404; source lives as a subtree of libcna/cna-lab. |
| `docs/xna-compatibility.html` | card | "Content pipeline" is the wrong phrase for what CNA has. | false claim corrected in place | The callout said CNA has no content pipeline. At the snapshot CNA has a build-time Content Pipeline (cna-content, importers/processors, XNB and CNB writers). The callout keeps its slot as a 'Correction to alpha.1' callout. |
| `documentation.html` | link | include/Microsoft/Xna/Framework/ on GitHub -> https://github.com/libcna/cna/tree/master/in | dead link replaced | HTTP 404: CNA has no master branch and no top-level include/ since the module split. Replaced by the snapshot SHA permalink to modules/core/include/Microsoft/Xna/Framework plus a modules/ link; text says headers are split across modules. |
| `features.html` | heading | bgfx Renderer | removed-functionality (replaced in place) | The card described a renderer that CNA has retired. It is replaced in the same position by the 'OpenGL 4 Renderer' card (and the maturity-table row by the OPENGL4 row); further cards were added for Metal, FNA3D, Direct2D, GDI, HTML_DOM, SVG_DOM, PortableGL and Stub, so the renderer presentation is richer, not smaller. |
| `index.html` | heading | Get running in 5 minutes | renamed (unsupported claim) | The 5-minute promise is unsupported: the first configure builds SDL3, SDL3_image and SDL3_mixer from source; renamed 'Get running from source'. The quickstart block itself is preserved and updated. |
| `index.html` | cta | easy-3d on GitHub ↗ -> https://github.com/libcna/easy-3d | dead link replaced | github.com/libcna/easy-3d is HTTP 404; the repository lives at github.com/openeggbert/easy-3d. Same button, working destination. |
| `index.html` | cta | cna-gltf-viewer on GitHub ↗ -> https://github.com/libcna/cna-gltf-viewer | destination improved | The repository default branch (main) holds only an empty 'initialize project' commit; the working viewer is on develop. Button kept with the deeper, useful destination. |
| `index.html` | cta | cna-editor on GitHub ↗ -> https://github.com/libcna/cna-editor | dead link replaced | github.com/libcna/cna-editor is HTTP 404; the source lives as a subtree of libcna/cna-lab. Button kept, pointing at the cna-lab subtree. |
| `index.html` | cta | cna-extended on GitHub ↗ -> https://github.com/libcna/cna-extended | destination improved | The default branch (master) shows a July 2026 bootstrap README; the real project is on develop. Button kept with the deeper, useful destination. |
| `index.html` | cta | cna-craft on GitHub ↗ -> https://github.com/libcna/cna-craft | dead link replaced | github.com/libcna/cna-craft is HTTP 404; the source lives as a subtree of libcna/cna-lab. Button kept, pointing at the cna-lab subtree. |
| `index.html` | link | CNA Craft -> https://github.com/libcna/cna-craft | dead link replaced | Same dead repository link inside the 'Verified Against Real XNA' card; now points at the cna-lab subtree. |
| `index.html` | link | THIRD_PARTY_NOTICES.md -> https://github.com/libcna/cna/blob/v0.1.0-alpha.1/THIRD_PARTY_NO | destination updated | Link followed the alpha.1 tag; it now follows the documented snapshot (pinned SHA permalink), which is what this page describes. |
| `index.html` | card | First tagged release. | updated in place | The status callout was rewritten as 'Development snapshot, not a release.' because 009d40f5 is a post-alpha.1 snapshot, not a tagged release. Same position, same style, richer content. |
| `index.html` | stat | 0.1.0 alpha.1 release | relabelled | The stat still shows the version string 0.1.0, relabelled 'alpha.1 version string' because the documented commit is not a release; a companion stat reports the 2,877 commits since the tag. |
| `index.html` | block | Get running in 5 minutes | renamed (unsupported claim) | Same section, renamed; content updated and expanded (108 words -> longer). |
| `roadmap.html` | heading | bgfx — no D3D or Metal shader blobs Partial | removed-functionality (replaced in place) | Roadmap item about a retired renderer's shader blobs. The same slot and status badge now carry 'Metal - a narrow 3D contract and no compiled effects', a current renderer gap. |
| `showcase.html` | link | cna-craft -> https://github.com/libcna/cna-craft | dead link replaced | github.com/libcna/cna-craft is HTTP 404; the source lives as a subtree of libcna/cna-lab; link kept with the working destination. |
| `showcase.html` | link | cna-extended -> https://github.com/libcna/cna-extended | destination improved | Default branch shows an obsolete July bootstrap README; link now points at tree/develop where the real project lives. |
| `videos.html` | heading | Development Update #1 | placeholder replaced by real video | The card was an empty placeholder (TODO_VIDEO_ID, no video existed). The 'Progress & Development' section keeps its place and now holds five real, embeddable videos from the LibCNA channel (verified via YouTube oEmbed). |
| `videos.html` | heading | Development Update #2 | placeholder replaced by real video | The card was an empty placeholder (TODO_VIDEO_ID, no video existed). The 'Progress & Development' section keeps its place and now holds five real, embeddable videos from the LibCNA channel (verified via YouTube oEmbed). |
| `videos.html` | heading | Development Update #3 | placeholder replaced by real video | The card was an empty placeholder (TODO_VIDEO_ID, no video existed). The 'Progress & Development' section keeps its place and now holds five real, embeddable videos from the LibCNA channel (verified via YouTube oEmbed). |
| `videos.html` | card | Development Update #1 | placeholder replaced by real video | The card was an empty placeholder (TODO_VIDEO_ID, no video existed). The 'Progress & Development' section keeps its place and now holds five real, embeddable videos from the LibCNA channel (verified via YouTube oEmbed). |
| `videos.html` | card | Development Update #2 | placeholder replaced by real video | The card was an empty placeholder (TODO_VIDEO_ID, no video existed). The 'Progress & Development' section keeps its place and now holds five real, embeddable videos from the LibCNA channel (verified via YouTube oEmbed). |
| `videos.html` | card | Development Update #3 | placeholder replaced by real video | The card was an empty placeholder (TODO_VIDEO_ID, no video existed). The 'Progress & Development' section keeps its place and now holds five real, embeddable videos from the LibCNA channel (verified via YouTube oEmbed). |
| `videos.html` | video | Development Update #1 | placeholder replaced by real video | The card was an empty placeholder (TODO_VIDEO_ID, no video existed). The 'Progress & Development' section keeps its place and now holds five real, embeddable videos from the LibCNA channel (verified via YouTube oEmbed). |
| `videos.html` | video | Development Update #2 | placeholder replaced by real video | The card was an empty placeholder (TODO_VIDEO_ID, no video existed). The 'Progress & Development' section keeps its place and now holds five real, embeddable videos from the LibCNA channel (verified via YouTube oEmbed). |
| `videos.html` | video | Development Update #3 | placeholder replaced by real video | The card was an empty placeholder (TODO_VIDEO_ID, no video existed). The 'Progress & Development' section keeps its place and now holds five real, embeddable videos from the LibCNA channel (verified via YouTube oEmbed). |

## Notes

- docs/audio.html: heading `Tier 1 — Implemented playback (SDL3_mixer)` retitled (id #tier-1-implemented-sdl3mixer kept)
- docs/c-api.html: heading `Tag status and scope` retitled (id #status kept)
- docs/c-api.html: heading `Intended build and package design` retitled (id #intended-build kept)
- docs/content-manager.html: heading `Two asset paths: .xnb first, loose files second` retitled (id #two-asset-paths kept)
- docs/rendering-backends.html: heading `Standalone GL renderers` retitled (id #native-gl kept)
- docs/rendering-backends.html: heading `Portable 2D renderers and vector rasterizers` retitled (id #portable-2d kept)
- docs/rendering-backends.html: heading `Windows renderers: the Direct3D ladder` retitled (id #windows-directx kept)
- docs/rendering-backends.html: heading `Portable middleware layers` retitled (id #middleware kept)
- docs/tutorials/103-direct3d-windows.html: heading `A capability warning specific to these two` retitled (id #capabilities kept)
- docs/tutorials/105-browser-renderers.html: heading `Three traps that apply to all three` retitled (id #traps kept)
- docs/tutorials/108-fna3d.html: heading `Instancing is false, and that is a shader limit too` retitled (id #instancing kept)
- docs/tutorials/114-pbr-materials.html: heading `Lit by three directional lights, not an environment` retitled (id #lighting kept)
- docs/tutorials/117-devices-layer.html: heading `The ten classes and what they sit on` retitled (id #classes kept)
- docs/tutorials/124-web-gotchas.html: heading `1. Your Game must be heap-allocated` retitled (id #game-lifetime kept)
- docs/tutorials/124-web-gotchas.html: heading `3. Video is not in the build at all` retitled (id #no-video kept)
- docs/tutorials/127-platform-audio-selection.html: heading `The three CMake selections` retitled (id #axes kept)
- docs/tutorials/129-c-api-first-program.html: heading `Confirm the tag-level blocker` retitled (id #build kept)
- docs/tutorials/129-c-api-first-program.html: heading `Understand the intended consumer project` retitled (id #consumer kept)
- docs/tutorials/129-c-api-first-program.html: heading `Read the source-owned example` retitled (id #program kept)
- docs/tutorials/129-c-api-first-program.html: heading `What to require from a later release` retitled (id #configure kept)
- docs/tutorials/72-backend-selection.html: heading `Group 3 — portable middleware and engine wrappers (8 identities)` retitled (id #middleware kept)
- docs/tutorials/72-backend-selection.html: heading `Group 6 — 2D raster and vector (6 identities)` retitled (id #raster-2d kept)
- docs/xna-compatibility.html: heading `Content: the XNB loader and its siblings` retitled (id #microsoftxnaframeworkcontent kept)
- index.html: stat `Renderer identities` 50 -> 25 (updated)
- index.html: stat `Implementation families` 46 -> 21 (updated)
- index.html: stat `Platform implementations` 4 -> 7 (updated)
- index.html: stat `Audio platform choices` 3 -> 4 (updated)
- index.html: stat `Static test definitions` 8,263 -> 12,610 (updated)
- index.html: stat `XNA samples ported` 63 / 86 -> 87 / 153 (updated)
- index.html: stat `CI workflow files` 21 -> 20 (updated)

