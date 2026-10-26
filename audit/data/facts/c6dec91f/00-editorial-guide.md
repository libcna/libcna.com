# Phase 6 editorial guide — moving libcna.com from CNA `c1c316b9` to `c6dec91f`

INTERNAL (not served). Every person or agent editing pages in this phase follows this file. The facts live in
`R1-renderers-platforms-numbers.md` (same directory) and `data/current-facts.json`; this file says how to write them.

## 1. What the snapshot is now

* `cnahead` = `c6dec91fbf3ef5440f60e5329e4a4758b2d80c22` (CNA `next`, 24 October 2026). Short form `c6dec91f`.
* CNA released **0.1.0** on 10 October 2026 (tag `v0.1.0`). The snapshot is **812 commits after that release**; its version
  string is still `0.1.0`. Say "a development snapshot after the 0.1.0 release" — never "post-alpha.1", never "the 0.1.0
  release" for the snapshot itself, never "0.1.0-alpha.1 is the current version". alpha.1 (2026-08-20) is history.
* The footer sentence, the "CNA snapshot c6dec91f" meta lines and every CNA source link whose path still exists were
  re-pinned mechanically already. 360 links in 109 files still point at `c1c316b9` because their path is gone at `c6dec91f`;
  each must be replaced by a current path that supports the sentence, or the sentence/link removed if its subject is gone.
  In `development/` a link not pinned to `cnahead` fails `scripts/check_source_links.py`.

## 2. Renderers (the largest change)

Current set: **10 public identities over 8 implementation families** — `OPENGLES3`, `OPENGL33`, `WEBGL2` (EasyGL, one
family), `WEBGPU`, `HEADLESS`, `SOFTWARE`, `STUB`, `DIRECTX9`, `SDL_GPU`, `FNA3D`. Maturity: Production 3 (OPENGLES3, OPENGL33,
DIRECTX9), Supported 5 (WEBGL2, WEBGPU, HEADLESS, STUB, SDL_GPU), Experimental 2 (SOFTWARE, FNA3D). Category: Native 3, TranslationLayer 3
(WEBGPU, SDL_GPU, FNA3D), Software 1, Web 1 (WEBGL2), Diagnostic 2 (HEADLESS, STUB). Defaults: Emscripten `WEBGL2`; Windows, macOS
and iOS `SDL_GPU`; everything else (Linux, Android, BSDs) `OPENGLES3`. No identity is 2D-only any more.

**Retired since the last pin (2026-10-13/14):** the Vulkan renderer, the Direct3D 11 renderer, the Metal renderer and the SDL
2D renderer (identity spellings are in R1 §1; do not write them on public pages). Phase 5's policy continues: **a retired
renderer leaves no public trace** — not in prose, lists, tables, metadata, diagrams, code samples, CMake lines, link text,
nor as a "removed"/"retired" notice. Do not narrate the removal. The validators enforce this:
`python3 scripts/check_retired_renderers.py` (≈35 s, whole site).

How to rewrite a sentence that named one:
* A list of renderers: drop the retired names and fix the grammar and any count ("EasyGL, WebGPU and SDL_GPU").
* A behaviour stated per renderer: keep it for the surviving renderers only; if only retired renderers had it, delete the
  sentence (or state the current fact for the survivors after checking the source at `c6dec91f`).
* Guidance that sent readers to a retired renderer: send them to the current path. Vulkan-class GPU access →
  `SDL_GPU` (SDL selects its Vulkan, Direct3D 12 or Metal **GPU driver**); Windows → `DIRECTX9` or `SDL_GPU` (SDL's Direct3D 12
  driver); macOS/iOS → `SDL_GPU` (SDL's Metal driver; the default there but **not re-qualified on Apple hardware** at this
  snapshot) or `SOFTWARE`; 2D-only → any surviving renderer (SpriteBatch works on all of them).
* Graphics APIs stay nameable when they are another project's: "SDL's Vulkan, Direct3D 12 and Metal GPU drivers", "FNA3D
  selects SDL_GPU, Direct3D 11 or OpenGL internally", "wgpu-native drives Vulkan", "DXVK translates Direct3D 9 to Vulkan",
  "vkd3d-proton". Use **driver**, not "backend"/"renderer"/"family", for those (the guard flags "Vulkan backend", "Metal
  renderer", "Direct3D 11 renderer", and a retired name listed beside a current CNA renderer).
* A whole page about a retired renderer is not rewritten line by line: the coordinator replaces it with a tombstone
  (`scripts/tombstones.py`). Decided: `deep-dives/renderers/{direct3d11-and-12-resources,sdl-renderer-2d-contract,
  vulkan-deferred-state-and-descriptors,vulkan-presentation-and-readback}.html`, `development/internals/graphics/vulkan.html`,
  `docs/tutorials/85-vulkan-backend.html`. Rewritten in place (same URL, current subject): `docs/tutorials/103-direct3d-windows.html`
  (Windows: DIRECTX9 and SDL_GPU on Direct3D 12), `docs/tutorials/109-metal-macos.html` (macOS and iOS: SDL_GPU on Metal, SOFTWARE),
  the `deep-dives/renderers/direct3d-*` pages (DIRECTX9 only), `native-gpu-evidence-tiers.html`. Links *to* a tombstoned page
  must be re-pointed to the page its tombstone names (no page may link a tombstone).
* Counts: 10 identities, 8 families, 1 Direct3D identity (DIRECTX9), compiled effects 8 identities / 6 families (FNA3D always;
  five default-OFF options EASYGL [3 identities], WEBGPU, SOFTWARE, DIRECTX9, SDL_GPU → 7 identities; HEADLESS and STUB never;
  9 of 10 refuse in a default configure). `GraphicsRendererType` has 10 enumerators, ordinals 0 (`OpenGLES3`) to 9 (`Fna3d`);
  the C ABI values are sparse (3, 4, 6, 9, 11, 12, 13, 22, 31, 43; `CNA_GRAPHICS_RENDERER_MAXIMUM` 43; next new value 52) — never
  equate a C++ ordinal with a C ABI value.
* Classification API renamed (ABI 0.49.0): `CNA::GraphicsRendererCategory` / `CNA::GraphicsRendererMaturity` in
  `CNA/GraphicsRendererCategory.hpp` / `CNA/GraphicsRendererMaturity.hpp`, `get[Current]GraphicsRenderer{Category,Maturity}()`;
  C: `CNA_GraphicsRenderer*`, `cna_graphics_renderer_*`. No alias of the old `GraphicsBackend*` names exists — update code samples.
* SDL_GPU gaps to state where relevant (R1 §2): `ShaderEffect` compiled out on Windows, Apple and Emscripten; no occlusion
  queries; `BlendState.MultiSampleMask` ignored; mixed cube/2D MRT refused; validated on Linux (Vulkan) and Direct3D 12 under
  Wine only; never built for iOS. `SpriteSortMode::Immediate` is batched on SDL_GPU and WEBGPU (handoff §5.1 defect).
* WEBGPU is **Supported** (was Experimental) and runs in CI; verified on Linux x86_64 and headless Chrome only.
* Automatic fallback tries `HEADLESS` after the renderers that show a picture.

## 3. The retired modern GPU layer

Compute shaders, storage buffers/images, the texture-array facade, `GraphicsMemoryBarrier`, `GraphicsImageAccess`,
`IndirectDrawArguments`, indirect drawing and GPU timers are gone end to end (`plans/plan_modern_retirement.md`); `GraphicsCapability`
has **17** members (no `ComputeShaders`, no `IndirectDraw`). Do not present any of them as a CNA feature, capability, roadmap item
or C route. A current-state sentence such as "CNA has no compute-shader API" is fine where a reader would ask; no removal story.
Kept and still current: glTF/PBR/IBL/shadows, `ShaderEffect`, vertex/fragment `ShaderPackageEXT`, float render targets,
instancing, compiled effects, uniform blocks, base-instance drawing on SDL_GPU only.

## 4. Other changes to reflect where a page touches them (R1 §0, §4–§8)

* Link boundaries and size: a program links only the subsystems it uses (`docs/link-size-architecture.md`); options
  `CNA_ENABLE_GAMER_SERVICES` (default = `CNA_ENABLE_NET`), `CNA_OPTIMIZE_FOR_SIZE`, `CNA_CXX_RUNTIME_LINKAGE`; SDL3_image is gone;
  C++ ABI break (rebuild C++ consumers). Mobile Eggbert's measured sizes are one game's record, never a guarantee.
* XNB readers: 61 built-ins (60 without native int128), declared registered by every `Game`/`ContentManager`, installed per family
  on the first `Load<T>`; registry queries answer as before.
* C ABI **0.50.0**; 60 headers; **3,212** declared routes; routes are generated from `modules/c-api/spec/*.toml`
  (`docs/c-api/GENERATED_ROUTES.md`); release gate **not ready**, 625 planned public C++ declarations without a C mapping (never
  "unmapped symbols" bare). CNA.NET admits exactly **0.47.0**, pins a CNA `next` commit from 13 October, refuses 0.46.0 (the v0.1.0
  release) and does not consume this snapshot (0.50.0) yet.
* Apple: macOS CI builds `SOFTWARE`, runs the portable platform suites and a bundle smoke app; a gating SDL_GPU-on-Metal smoke leg
  exists but had not run at the snapshot; iOS is a `SOFTWARE` simulator smoke app (allow-list `SOFTWARE`, `SDL_GPU`; SDL_GPU never
  built for iOS). The Mac mini M4 campaign of early October is history (before the retirements) and was not repeated.
* Windows: `DIRECTX9` (via DXVK under Wine) and SDL_GPU's Direct3D 12 driver (vkd3d-proton under Wine); manual MSVC workflow;
  no current real-Windows hardware validation.
* Test numbers: 898 C++ test source files, 855 with a counted macro, 11,898 static definitions; 18 workflow files / 25 jobs
  (16 / 22 automatic). Runtime results are CNA's records (R1 §6) — say "recorded by CNA", never "passes".
* Defects: CNA's handoff §5.1 lists one defect (Immediate batching on SDL_GPU/WEBGPU); the demos repair campaign (R1 §7) has nine
  findings whose fixes are committed at the snapshot but not yet closed on a complete checkpoint — never call those "fixed".

## 5. Evidence wording

* A page whose claims you re-verified against `c6dec91f`: its `dev-evidence` callout says "source-verified at the pinned
  commit … checked by reading the CNA source at commit <code>c6dec91f</code>". Keep the page's other evidence labels honest.
* A page you did not re-verify keeps `c1c316b9` and must say "at the stated evidence commit" instead of "at the pinned commit"
  (`check_facts.py` fails the mismatch). The coordinator applies that wording to untouched pages at the end; do not do it blindly.
* "Recorded by CNA" for CNA's own test runs, measurements and campaign ledgers; "not executed here" for anything not run.
* Do not invent benchmarks, run results, dates, platform qualification or compatibility.

## 6. Mechanics

* Edit authored HTML in place; keep the visual structure, ids, classes and heading anchors. Removing a section with an `id`
  that other pages link: re-point the links (`grep -rn 'page.html#id'`) and record it.
* Do not hand-edit generated regions: `known-issues/**`, `data/known-issues.json`, `development/reference/*.html`, sidebars,
  breadcrumbs, pagers, `<!--p3:deep-links-->`/`<!--p3:issue-links-->` blocks, text inside `<!--issue:KEY-->` markers,
  `search-index.json`, `sitemap.xml`, `img/architecture-diagram.svg`.
* `<!--p3:begin …-->`/`<!--p3:end …-->` regions may be edited; the coordinator folds them back into their sources
  (`apply_expansions.py fold`) at integration. Do not run `fold`, `regenerate_site.sh`, `build_site_indexes.py` or `git commit`.
* Checks you can run on your own work: `python3 scripts/check_retired_renderers.py`, `python3 scripts/check_facts.py`
  (≈90 s; filter its output to your files), `python3 scripts/check_source_links.py`, `python3 scripts/validate_site.py`
  (structure and links), `python3 scripts/check_dev_page.py <page>` for `development/` pages.
* Record what you changed in your area's record file in this directory (page → what changed, evidence path at `c6dec91f`,
  statements removed or reclassified, uncertainties).
