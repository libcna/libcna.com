# Post-refresh remediation — libcna.com at CNA `c1c316b9`

Narrow correction pass after an independent adversarial review of the Phase 5 refresh (`45b9b7a`, `c522acb`,
`835d161`). The pin is unchanged: `cnahead` = `c1c316b9c7a846ce8002809c151fcd1af14942c9`. Nothing in CNA,
cna-gamer-services-server or any sibling repository was modified, built or run; CNA was read from its Git objects.
Not served (`_config.yml` excludes `audit/`).

## 1. Facts reproduced at `c1c316b9` before editing

| Fact | Command (Git objects at `c1c316b9`) | Value |
|---|---|---|
| CNA-owned C++ test sources | `git ls-tree -r --name-only`, `*.cpp`, not `third_party/`, a `test`/`tests` path segment | 813 |
| Files with a counted macro / definitions | `git grep -cE '^\s*(TEST\|TEST_F\|TEST_P\|TYPED_TEST\|TYPED_TEST_P)\s*\(' -- '*.cpp' ':!third_party'` | 781 / 11,380 |
| Public identities / families / GL profiles | `cmake/RendererIdentities.cmake`; `modules/renderers/*/src`; `cmake/RendererRegistry.cmake` (EasyGL rows) | 14 / 12 / 3 |
| Platform implementations | `cmake/PlatformSelection.cmake` (`_cna_platforms_available`; WIN32 X11 WAYLAND in `_cna_platforms_retired`) | 3 |
| `deviceEventCallback` callers | DirectX9, DirectX11, Vulkan, WebGPU renderers | 4 families |
| `cna_register_parity_fixtures()` callers | directx11, easygl, sdl-gpu, webgpu `examples/CMakeLists.txt` | 4 families |
| `UpdatePresentationFormatEXT` overrides | DirectX9, DirectX11, EasyGL, FNA3D, Metal, SDL_GPU, Software | 7 families |
| `ClassifySurfaceFormatEXT` overrides | directx11, easygl, fna3d, metal, sdl-gpu, software, vulkan, webgpu | 8 families |
| `PresentationParameters::HeadlessEXT` | header documentation names SDL GPU only; D3D11 and EasyGL throw | — |
| Windows link set of the renderers | `d3d11 dxgi d3dcompiler` (DIRECTX11), `d3d9 d3dcompiler` (DIRECTX9); no d3d12/d2d1/gdi32 | — |
| `platform-ci.yml` | SDL3 window suites under a private Xvfb and a private headless Weston; a skip fails the step | — |
| SDL_GPU on Apple | `docs/apple-platforms.md`: full tree 10,962/10,962, 295 skip, SDL's Metal driver, physical Mac mini M4 (console locked) | — |

## 2. Public claims corrected

* Test inventory: "821" files with a counted macro → 781 (`contribute`, `about`, `docs/building`, `features`, tutorial 84);
  "852 files" → 813 (`deep-dives/foundations/compatibility-and-evidence`).
* Renderer counts: "14 families" → 12 (`contribute`, module graph, worked changes, quick reference "21" → 12,
  `documentation` "21" → 12, "(1 of 14)" → 12); "18-identity, 14-family registry" → 14 / 12; 18-row / 18-member /
  18-entry identity tables → 14; "one of 18 selectable" → 14; update-libcna-com fact table (14 / 12 / 1; 11 in 9;
  platforms 3); "five" EasyGL identities / GL profiles → three (ecosystem, build architecture, change map, backends,
  network, verification ×2, renderer guide TOC); "seven"/"two" 2D-only → one (`SDL_RENDERER`); "17"/"23" identities
  → 12 (features 3D card, SpriteBatch); compiled effects "13 more" → 10 more (tutorials 21, 58, 65, 66, 67, 69,
  108, migration guide, comparison page "(14 of 25)" → "(11 of 14)"), "14 of the 14" → "11 of the 14"; parity
  fixtures "five renderer families" → four (glossary); format classification "seven" → eight (roadmap; FNA3D
  missing); audio "four" implementations → three.
* DIRECTX12 as a current renderer removed: device-event callers (five → four families), parity registrations,
  presentation-format overrides (Metal instead of DirectX 12), HeadlessEXT (SDL GPU only), the vertex-buffer
  options table row (replaced by Metal beside Vulkan; Metal added to the declaration sentence), the renderer
  dependency row (d3d12/d2d1/gdi32 removed, attributed to DIRECTX9/DIRECTX11).
* Direct platform backends removed: architecture source tree and axis table, the exclusions note, `sdl3` sidebar
  ("native sibling" links → Headless / Terminal internals), `about` ("six implementations"), `docs/building` option
  table and GPU note, storage policy, tutorials 50 and 139, terminal internals, build module table ("Xlib, Wayland,
  Win32"), graphics quick reference (`IPlatformWindow` list), `contribute` ("Wine-executed Win32 lane"), showcase
  ("no workflow ... runs a Wayland session").
* "631 unmapped symbols" → planned public C++ declarations without a C mapping (`contribute`, `docs/building`,
  `docs/c-api`, `docs/roadmap`, `docs/verification`, tutorial 129, four deep dives, the C API deep dive's description
  and every card generated from it, CNA-BUG-058 title, CNA-GAP-062 text). Verbatim quotations of `RELEASE_GATE.md`
  stay, with the meaning stated beside them.
* SDL_GPU Metal contradiction: the evidence callout now records the Mac mini M4 run through SDL's Metal driver and
  says it is not evidence for the separate `METAL` renderer.
* Evidence headings: eight `deep-dives/services/*` pages read at `b0e97bb1` now say "source-verified at the stated
  evidence commit".
* Retired URLs: GitHub Pages serves this repository through Jekyll without a redirect plugin and the pages carry no
  front matter, so there is no server-side redirect. The four deleted pages
  (`deep-dives/renderers/canvas-renderer.html`, `development/internals/platforms/{x11,wayland,win32}.html`) are
  restored as noindex tombstones by `scripts/tombstones.py`, pointing to the renderer guide / SDL3 internals.

## 3. Validators

* `check_facts.py`: recomputes identities, families, GL profiles, platforms, audio, the three test figures, the C ABI
  and the route count from CNA and fails when `data/current-facts.json` disagrees; `METRIC_RULES` over every public
  page (Known Issues included); impossible-combination rule; evidence-heading rule; C-mapping wording rule.
* `check_retired_renderers.py`: semantic list / role / context / table-cell pass over visible text.
* `check_retired_platforms.py`: semantic list (incl. whitespace-separated trees), "native sibling", backend/lane,
  source directories, CI contradiction derived from `platform-ci.yml`.
* `adversarial_audit.py anchors`: a tokenless SUPERSEDED concept needs `replacement_tokens` or a `review`; every cited
  section is read by the semantic checks; tokenless current concepts are ratcheted at the 141 recorded in
  `audit/data/adversarial/tokenless-current-baseline.json`. The 49 tokenless SUPERSEDED concepts received replacement
  tokens (each verified in its cited section). Five tokens that kept a corrected statement "anchored"
  (WP02-ch09-010, WP06-ch14-174, WP07-appa-002, WP07-appa-012, WP02-appd-004) were moved to the corrected text or,
  for the retired DIRECTX12 row, the concept became REMOVED FUNCTIONALITY.
* `test_validators.py`: the reviewer's exact sentences and legitimate counterparts, run first by `validate_all.sh`.
* `validate_all.sh`: a skipped optional external stage is listed and the status reads
  `PASS WITH OPTIONAL EXTERNAL CHECKS SKIPPED`; `--require-external` makes it fail.
* `compare_presentation.py` compares a tombstone as the absent page, so the recorded "removed" dispositions govern.
* Two applied page fixes whose text was corrected here carry `superseded_by` this record
  (C02-ch09-module-monorepo-F1-1, C06-ch25-abstraction-layers-two-F3-1).
