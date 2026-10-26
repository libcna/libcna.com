# R3 — Tutorials, CNA B=c1c316b9 → T=c6dec91f

INTERNAL AUDIT RECORD (not served). This file names retired renderer identities; the public pages must not.

Scope: `docs/tutorials/*.html` (157 pages) and the hand-written parts of `tutorials.html` (card titles and
descriptions, section intros, the Tutorial 85 card and JSON-LD item). Tutorial 85 (`85-vulkan-backend.html`) is the
coordinator's tombstone and was not edited. CNA was read only through Git objects at B and T
(`git show/grep/log/ls-tree`); nothing in CNA was built or run, and nothing was built anywhere. No commit, push,
`regenerate_site.sh`, `apply_expansions.py fold` or `update_tutorial_hub.py` was run. Generated regions
(`p3:deep-links`, `p3:issue-links`, sidebar, `docs-pagination` pagers, hub counts and JSON-LD numbering) were not
edited. Facts used are those of `00-editorial-guide.md` and `R1-renderers-platforms-numbers.md`, plus the T evidence
named per page. `dateModified` was set to 2026-10-25 on every page whose content changed (not on `tutorials.html`).

## 1. Pages re-verified at T (renderer, build, branch and number claims checked against CNA at c6dec91f)

Tutorials carry no "at the pinned commit" dev-evidence callouts. Where a page has its own snapshot note it now names
c6dec91f (or, for partly re-checked pages, keeps c1c316b9 and says which part was re-checked at c6dec91f; see §3).

| Page | What changed | CNA evidence at T |
|---|---|---|
| 72-backend-selection | Body rewritten: 10 identities/8 families; groups GL family, modern GPU (SDL_GPU, WEBGPU), translation layers (WEBGPU, SDL_GPU, FNA3D), Windows (DIRECTX9 + SDL_GPU default), browser, CPU-only; "2D games run on every renderer" (id `raster-2d`), CPU-only (id `cpu-only`), "Which renderers produce no picture" (id `two-d-only`); custom shaders (DIRECTX9 SpriteBatch-only); compiled effects 8 identities/6 families, 5 options; 17 capabilities, profile 31 features/8 limits; cube-in-MRT gap (`mrt-cube-gap`); decision table; CMake examples; defines; CI paragraph. All ids kept. New meta description. In-text link to Tutorial 85 removed. | `cmake/RendererIdentityDefault.cmake`, `cmake/RendererSelection.cmake`, `GraphicsRenderer{Category,Maturity}.hpp`, `GraphicsCapability.hpp`, `RendererCapabilityProfile.hpp`, renderer `SupportsCapability` bodies, `CMakeLists.txt` options |
| 103-direct3d-windows | Full rewrite, title "Tutorial 103: Direct3D 9 and SDL_GPU on Windows" (title, og, JSON-LD, h1, hub card). Ids `gate`, `crosscompile`, `translation`, `guards`, `proves`, `capabilities`, `d3d9` (inbound from 107 and a deep dive), `next` kept. Capability table DIRECTX9 vs SDL_GPU. | `modules/renderers/directx9/**`, `scripts/run-wine-dxvk9.sh`, `scripts/run-wine-vkd3d{,-headless}.sh`, `.github/workflows/d3d-windows-ci.yml`, `cmake/Tests/UnitTests.cmake` |
| 109-metal-macos | Full rewrite, title "Tutorial 109: macOS on Apple Silicon" (SDL_GPU default on SDL's Metal driver, OPENGL33, WEBGPU, FNA3D, SOFTWARE). Ids `platform-gate`, `sdl-boundary`, `building`, `capabilities`, `shader-effect`, `ci`, `m4-evidence`, `deterministic`, `why-narrow`, `what-works`, `portable`, `next` kept. M4 campaign kept as dated history for surviving renderers ("before this snapshot; not repeated"). Source links to `apple-ci.yml`, `plans/plan_apple_m4.md`, `docs/apple-platforms.md` at T; links to the B-only `metal-macos-ci.yml` and `metal-shader-effect-contract.md` removed. | `cmake/ApplePlatform.cmake`, `cmake/RendererIdentityDefault.cmake`, `.github/workflows/apple-ci.yml`, `docs/apple-platforms.md`, `plans/plan_apple_m4.md` |
| 01-introduction | Snapshot paragraph (next, 0.1.0, c6dec91f), renderer table (10 identities, SDL_GPU default on Windows/macOS/iOS), test counts 898/11,898, branch rules | `CMakeLists.txt`, `cmake/Version.cmake`, `git ls-tree` counts |
| 02-setup | Clone block (`-b next` for cna and sharp-runtime; easy-gl `v0.1.1`, meta-gl `v0.4.1`), 4 submodules, CMake ≥3.30 for shared builds, apt list incl. `libcurl4-openssl-dev nlohmann-json3-dev`, macOS/Windows defaults, SOFTWARE/SDL_GPU section replacing the 2D-renderer one, options table, installed C++ SDK, test counts, meta description | `.gitmodules`, `cmake/DependencyVersions.cmake`, `general-tests-ci.yml` apt list, `CMakeLists.txt` |
| 03, 20, 80, 82 | Branch/sibling layout, defaults (Windows SDL_GPU, Android OPENGLES3, macOS SDL_GPU), install note, troubleshooting rows | same as 02; `cmake/RendererIdentityDefault.cmake` |
| 52, 53, 57–70 (and 31, 37, 39, 40, 55) | Custom-shader language table (SDL_GPU SPIR-V/libshaderc, WGSL, GLSL; DIRECTX9 HLSL SpriteBatch-only), skinned/shadow/instancing/occlusion/MRT/stencil/cube/MSAA/bloom/deferred/terrain/water/procedural tables to the surviving identities; shadow sampling on all six pixel families; IBL not on DIRECTX9; occlusion queries absent on SDL_GPU and on FNA3D's SDL_GPU driver; cube face in MRT refused by DIRECTX9/SDL_GPU/WEBGPU; MultiSampleMask ignored; base-instance only SDL_GPU; ComputeShaders capability removed from text | renderer sources under `modules/renderers/*/src`, `GraphicsCapability.hpp`, `IGraphicsRenderer.hpp` |
| 87, 90, 101, 102, 105, 107, 108 | Custom-backend contract, easy-gl (release tag, compute check only in easy-gl), capability tables (17), GL family, browser renderers, CPU renderers, FNA3D (drivers, occlusion only on its OpenGL/D3D11 drivers, instancing via compiled effect) | as above plus `modules/renderers/fna3d/**` |
| 114, 116 | PBR shading table (all six pixel families via `ShadesPbrEffectEXT`), post-process effects | `IGraphicsRenderer.hpp`, PBR effect renderers, `modules/graphics-ext/**` |
| 125, 126, 128, 129 | Readback counts (375 files/540 call sites), 2 glTF golden sets; multi-renderer build; compiled XNA effects (8 identities/6 families, 5 options); C ABI 0.50.0, 60 headers, 3,212 routes, gate 625 planned | `rg` over T tree via `git grep`, `GltfFixtureCorpusTests.cpp`, `modules/c-api/include/CNA/C/abi.h`, `docs/c-api/*.md` |
| 131, 132, 133 | SDL_GPU (drivers, qualification Linux + Wine D3D12, ShaderEffect availability, formats), WebGPU (Supported since 17 Oct 2026, WGSL, rgba16float, Chrome flags), capability profile (31/8, schema 3, `CNA_RENDERER_FEATURE_PBR_EFFECT_SHADING` C example, `GBufferTargetCount` example) | `modules/renderers/sdl-gpu/**`, `modules/renderers/webgpu/**`, `RendererCapabilityProfile.hpp`, `modules/c-api/include/CNA/C/renderer_profile.h` |
| 135, 136, 137, 138, 139 | Native X11/Wayland/ALSA/SDL-free/terminal builds: renderer choices and requirements, branch rules | `cmake/SdlAvailability.cmake`, `platform-ci.yml` |
| 150, 151, 152, 160 | Build-time .fx (renderer list re-checked at T), one shader several renderers, GraphicsProfile renderer table (re-checked at T), parity fixtures (32, three families EasyGL/SDL_GPU/WEBGPU) | `parity/ParityFixtures.cmake`, renderer sources |
| 170, 171 | CNA.NET admits exactly ABI 0.47.0; CI pins CNA next `fbd8e64a3`; macOS SOFTWARE | `cna-dotnet` CI files (read only) |
| 162, 166, 42 (stale issue markers) | 42: Decompose now follows XNA 4.0 (marker NEW-AUDIT-11 and CNA-BUG-259 link removed). 162: offline leaderboards keep stream columns (NEW-PIN-04 removed); hand-written CNA-BUG-154 warning replaced by a note that `DeleteContainer` removes only that container's folder. 166: `SendDataOptions` is a flags enum, Chat alone unreliable (NEW-PIN-03 removed). | `Matrix.cpp`, GamerServices leaderboard/storage sources, `SendDataOptions.hpp` |
| 167 | Avatar-pixel evidence restated from CNA's limitations document at T (521-frame review, 15 Oct 2026, eight renderer/driver combinations incl. DIRECTX9 and SDL_GPU D3D12 under Wine; worst 0.09/255; not measured: SDL_GPU Metal, native Windows drivers) | `docs/gamer-services-known-limitations.md` §33 at T |
| 168 | Server's Apple portability fixes are now merged (in server `v0.1.0` and `develop`); branch name removed | `cna-gamer-services-server` git: f74f42e, 2869b20 contained in `v0.1.0`, `develop`, `main` |

## 2. Pages delta-edited (only the stated sentences changed)

- 21, 24, 25 — Immediate SpriteBatch: EasyGL, SOFTWARE, FNA3D and DIRECTX9 (since 3b6a2eaf3) submit per Draw; SDL_GPU and WEBGPU still batch ordinary stock sprites (CNA-BUG-278).
- 31–40, 51–58, 68, 70, 74, 75, 93 — prerequisite sentence → "Requires a 3D-capable renderer such as OPENGLES3 or SDL_GPU …; STUB …" (32, 33, 34, 35, 36, 38, 51, 54, 56, 74, 93 changed only this sentence).
- 45, 83, 84, 147, 148 — XNB readers: declared only by `Game`'s constructor (`Game.cpp:446`); `Load<T>` installs per type without a Game; registry queries without a Game need `RegisterAllBuiltInXnbReaders()` first. 84 also: five compiled-effects options (EasyGL, WebGPU, Software, DirectX 9, SDL_GPU) and parity families EasyGL/WebGPU/SDL_GPU.
- 49, 71, 73, 75, 79, 89, 95, 96, 99, 100, 124, 140, 141, 145, 146, 155, 156, 157, 161, 163, 164, 165 — renderer lists, branch names (`next`), numbers and wording. 73: "GPU validation layers" (meta, list, RenderDoc sentence). 145: CMake comment branch `next`. 161: oracle tools changed only in comments and renderer names. 157: only `cna_tool_gltf_to_cnj` source changed. 163–165 (and 162, 166, 168): "avatar pixels on native Windows drivers and on SDL_GPU's Metal driver".
- 77 — code comment "no graphics-API calls" (API names removed).
- 115 — "10 renderer identities"; post-process shader package has GLSL ES, desktop GLSL, SPIR-V and WGSL variants (no HLSL at T: `modules/graphics-ext/src/PostProcessShaderPackages.cpp`).
- 127 — "outside the 10 public identities".
- `tutorials.html` — Tutorial 85 card and JSON-LD ListItem removed; 103 and 109 renamed in cards and JSON-LD; renderers section intro "10 renderer identities … and the Windows and macOS paths".

## 3. Pages that keep c1c316b9 as their evidence commit (not re-verified as a whole)

133 (fragments changed for T not re-compiled), 140, 141, 145, 146, 147, 148, 150 (renderer list re-checked at T),
152 (renderer table re-checked at T), 155, 156, 157, 160, 161, 162 (two notes re-checked at T, stated), 163, 164,
165, 166 (`SendDataOptions` note re-checked at T, stated), 167.

## 4. Pages untouched

04–19, 22, 23, 26–30, 41, 43, 44, 46, 47, 48, 50, 76, 78, 81, 88, 91, 92, 94, 97, 98, 110–113, 117–123 (scanned for
retired names, stale numbers, branch names and alpha-era claims; remaining `alpha.1` mentions are history).
85 is the coordinator's tombstone.

## 5. Ids removed or renamed

None. 72's headings were retitled (`raster-2d`, `cpu-only`, `two-d-only` kept); 103 and 109 kept every id listed in §1.

## 6. p3 regions edited

None.

## 7. Links removed

- `tutorials.html`: Tutorial 85 card and its JSON-LD ListItem.
- 131 and 72: in-text links to Tutorial 85.
- 109: source links to `.github/workflows/metal-macos-ci.yml` and `docs/metal-shader-effect-contract.md` (B only).
- 42, 162, 166: `<!--issue:-->` markers and their links (NEW-AUDIT-11 → CNA-BUG-259; NEW-PIN-04 → CNA-GAP-073;
  NEW-PIN-03 → CNA-GAP-072); 162's hand-written CNA-BUG-154 link. No hand-written link to `cna-gap-010.html` existed.

## 8. Generated regions still naming retired renderers or linking tombstones / retired issues (left for regeneration)

- `p3:deep-links`: 101:379 (native-gpu-evidence-tiers description "What VULKAN, SDL_GPU, WEBGPU and METAL…"),
  103:263–265 (direct3d-evidence-and-wine, direct3d-presentation-and-state descriptions; direct3d11-and-12-resources
  tombstone), 125:366 and 72:305 (sdl-renderer-2d-contract tombstone), 52:374 (old title of
  direct3d-shadereffect-contract), 61:346 (vulkan-deferred-state-and-descriptors tombstone).
- Pagers: 84:349–351 (next → 85, "The Vulkan Renderer: Setup and Quirks"), 87:379–381 (prev → 85).
- `p3:issue-links` to retired issues (broken local links): 122 → cna-bug-137, 42 → cna-bug-259, 77 → cna-bug-119.
- Hub numbers: "157 tutorials available", `numberOfItems: 157`, the section header "19 tutorials" (now 18 cards) and
  JSON-LD positions (gap at 85) need `update_tutorial_hub.py`.
- `sitemap.xml` and `search-index.json` still list the tombstone `docs/tutorials/85-vulkan-backend.html`.

## 9. Claims not verifiable here

- SDL_GPU on native Windows drivers and on SDL's Metal driver: no recorded run at T (apple-ci `macos-sdlgpu` gating
  leg had not run; `d3d-windows-ci` is manual). Pages say "not re-qualified".
- Early-October Apple M4 campaign results (102, 109, 131, 132, 162–168, 170, 171): historical, dated, not repeated.
- SDL_shadercross translating MojoShader SPIR-V for SDL's Direct3D 12 and Metal drivers (150:74): from source only.
- Per-renderer DepthBias magnitudes (39): removed, not verified.
- Gamer-services server behaviour (164, 168): server README at `4ab12fd`; nothing run.
- Avatar review and AvatarShadows results (167): recorded runs in CNA's documentation.
- RenderDoc and Khronos validation-layer support for SDL's drivers (73, 79): third-party scope.
- Chrome flags used by CNA's WebGPU browser tests (132): read from scripts, not run.

## 10. Cross-area requests (not edited: owned by others)

1. `docs/link-size.html:169` — "A `Game` and every `ContentManager` still *declare* all 61 built-in readers": at T only
   `Game`'s constructor declares them (`modules/runtime/src/Game.cpp:446` → `DeclareBuiltinXnbReaders()`, defined in
   `modules/content/src/Xna/ContentTypeReaderManager.cpp:299`); a `ContentManager` alone does not.
2. `docs/building.html:517` — "tolerates a single known failure (its ctest step is continue-on-error, then a
   classification step …)": at T `general-tests-ci.yml` has no known-failure allowlist (comment at line 17); the step
   after ctest fails the job on any failure (lines 182–188).
3. `docs/building.html:143–147` — Linux apt list lacks `libcurl4-openssl-dev` and `nlohmann-json3-dev`, which the
   default Net/Gamer Services build needs and `general-tests-ci.yml:77–78` installs.
4. Deep-dive meta descriptions that feed the tutorials' generated deep-links (native-gpu-evidence-tiers,
   direct3d-evidence-and-wine, direct3d-presentation-and-state, direct3d-shadereffect-contract title) — regenerate
   the deep-links after R2's edits.
5. CNA source (read-only, for the CNA owners): `modules/renderers/sdl-gpu/src/SdlGpuRenderer.cpp:2914`
   (`GetAdditionalLimitationsTextEXT`) says CNAEXT ShaderEffect instancing is not implemented, while the 3D
   custom-effect route expands per-instance streams (SMG-0022; error text at :10777). Tutorial 60 describes the
   working route and notes the text.
6. WEBGPU `HalfFloatTextureLinearFiltering` was already true at B; the old tutorial text was wrong (fixed in 132 and the rewritten 72).

## 11. Validator state (tutorials only) at the end of R3

- `check_retired_renderers.py`: 10 findings, all in generated regions (§8).
- `check_facts.py`: 0 tutorial problems.
- `check_source_links.py`: 0 tutorial problems (172 CNA links, all at c6dec91f).
- `validate_site.py`: 3 broken links, all in generated `p3:issue-links` (§8); sitemap/search coverage
  mismatches are site-wide.
- `check_retired_platforms.py`: 0.
- `issue_refs.py check`: 0 tutorial errors.
- `tombstones.py check`: tutorial errors only in generated deep-links (103, 125, 61, 72) and pagers (84, 87).
- `check_cpp_blocks.py`: not applicable (it checks Deep Dive and Development pages only).
