# Second post-refresh remediation — libcna.com at CNA `c1c316b9`

Narrow correction pass after a second independent adversarial review of `f412fa0` (verdict: do not push yet). The pin
is unchanged: `cnahead` = `c1c316b9c7a846ce8002809c151fcd1af14942c9`. Nothing in CNA, cna-gamer-services-server or any
sibling repository was modified, built or run; CNA was read from its Git objects. Not served (`_config.yml` excludes
`audit/`).

## 1. Facts reproduced at `c1c316b9` before editing

| Fact | Source (Git objects at `c1c316b9`) | Value |
|---|---|---|
| Platform implementations | `cmake/PlatformSelection.cmake`: `SDL3 HEADLESS` always, `TERMINAL` only `if(NOT WIN32)`; `_cna_platforms_retired WIN32 X11 WAYLAND` | 3 |
| EasyGL identities | `cmake/RendererRegistry.cmake` `_map`: `OPENGLES3`, `OPENGL33`, `WEBGL2` → `EasyGL` | 3 |
| EasyGL adapter hooks | `EasyGLRendererDescriptor.cpp` `AdapterQueriesFor`: `OPENGL33` returns `{}`; `OPENGLES3`, `WEBGL2` get the Color-only render-target query | 2 of 3 |
| Compiled effects | `option(CNA_<F>_COMPILED_EFFECTS … OFF)` for EASYGL VULKAN WEBGPU SOFTWARE DIRECTX11 DIRECTX9 METAL SDL_GPU; FNA3D answers `true` with no option | 11 identities / 9 families; never: 3 (SDL_RENDERER, HEADLESS, STUB); default configuration refuses: 13 |
| Texture2D format classifiers | families defining `ClassifySurfaceFormatEXT`: directx11 easygl fna3d metal sdl-gpu software vulkan webgpu | 8 families / 10 identities; outside: 4 (DIRECTX9, SDL_RENDERER, HEADLESS, STUB → `Texture::ValidateFormat`, Color only) |
| Render-target classifiers | families defining `ClassifyRenderTargetFormatEXT` (the eight above minus fna3d) | 7 families / 9 identities; outside: 5 |
| Files named `*_test.cpp` | `git ls-tree -r --name-only`, not `third_party/`, `(^\|/)examples/.*_test\.cpp$` (none outside `examples/`) | 781 (125 framework + 656 renderer) |
| `.cpp` under `examples/` | same, `(^\|/)examples/.*\.cpp$`: 878 under `modules/`, plus `examples/xvfb_screenshot_demo.cpp` | 879 |
| Test files with a counted macro | `git grep -lE '^\s*(TEST\|TEST_F\|TEST_P\|TYPED_TEST\|TYPED_TEST_P)\s*\(' -- '*.cpp' ':!third_party'` | 781, all under `tests/`; overlap with the `*_test.cpp` set: 0 |
| ThreeD reported / pixels produced | `StubRenderer::SupportsCapability` returns false; SDL_RENDERER reports no ThreeD; HEADLESS validates only | 12 / 12 (11 rasterise 3D) |
| PBR map sampling | `GltfRendererPbrFallbackPolicyTests.cpp` `sampling`: directx9 directx11 easygl sdl-gpu vulkan webgpu metal | 7 families / 9 identities |
| C API matrix | `docs/c-api/COMPATIBILITY.md`: HEADLESS, SDL_RENDERER, SOFTWARE (×2) | 3 identities; 11 outside |
| Text input on desktop | `Sdl3TextInput::Start` → `SDL_StartTextInput`; `WM_CHAR` appears only in `plans/plan_win32.md` | — |

## 2. Public claims corrected

* Generated selection axes (`scripts/generate_dev_reference.py`, not only the page): the sentence calling Win32, X11 and
  Wayland host-conditional implementations is replaced by the registry's shape (SDL3 and HEADLESS on every host, only
  TERMINAL host-conditional; Windows a host and X11/Wayland display environments reached through SDL's video drivers;
  the retired values refused by name). The generator refuses to write the page if that shape changes, and the dead
  notes for WIN32/X11/WAYLAND/SDL2 are gone. The module index's "EasyGL serves five" is now counted from the registry.
* EasyGL: "serves five" → three (`source-ownership`), "five-identity" descriptor → three-identity, the malformed "two
  EasyGL profiles other than OPENGL33, OPENGLES3 and WEBGL2" → two of the three, OPENGLES3 and WEBGL2 (`selection`).
* Compiled effects: "refused on the 11 identities without a compiled-effect runtime" → three never, 13 in a default
  configuration (`xna-api-surface-auditing`); "(13 of the 14 identities)" → 11 (`about`); "thirteen other identities
  (nine implementation families)" → ten in eight more (tutorial 108); "the 14 renderer identities that support them"
  → 11 of the 14 (tutorial 128 description); "portable across 14 renderer identities" → 11 of the 14 (tutorial 151);
  "nine other renderer families" → eight (`content-pipeline-xnb`).
* Formats: "the other thirteen identities accept only SurfaceFormat::Color" → eight families / ten identities classify,
  the other four accept only Color for a public Texture2D (`migration-from-monogame`); "seven shipped renderers are
  Color-only" → four, FNA3D joining them for render targets (tutorial 87); `docs/roadmap` adds FNA3D to the classifiers
  and DirectX 9 to the Color-only set; `features` no longer says FNA3D classifies render-target formats.
* Test metrics: "879 `*_test.cpp` files" → 879 `.cpp` (878 + the loose demo), 781 named `*_test.cpp`, a set distinct from
  the 781 macro-bearing files (`source-ownership`); "(879 across the tree)" → 781 (`investigate-a-sample-failure`).
* Counts: "the other 20 families" → 11 (`docs/verification`); "the other 15 renderer identities" → 11
  (`c-api-evidence-and-gates`); parity fixtures "cover five families" → four (`xna-oracle`); "Seven shipped renderers
  are 2D-only" → one (tutorial 87); PBR "eight implementation families" → seven (tutorial 114, twice).
* 631: "631 public C++ symbols (are) still unmapped" → in-scope public C++ declarations that still lack C mappings
  (`docs/c-api` ×2, `docs/roadmap`, `roadmap`).
* Retired platform backends: the curriculum's "compare SDL3 with Win32 or X11" → Terminal; `docs/input`'s Win32
  `WM_CHAR` event mapper → the SDL3 text-input path.
* Not changed: the C API evidence wording the review judged defensible by scope (builds on other commits of the same
  branch with identical relevant source).

## 3. Validators

* `check_facts.py`: compiled-effect, format-classifier and `examples/` sets derived from CNA; EasyGL shorthand rules;
  named test-file metrics; complements larger than the whole; `concept_findings` judges compiled-effect and format
  counts by polarity and default-configuration wording; the C-mapping rule covers "public C++ symbols still unmapped"
  and "missing C exports". `HISTORY` no longer treats a bare "then" as an earlier revision, and a reporting verb no
  longer excuses impossible complement arithmetic.
* `check_retired_platforms.py`: "Win32/X11/Wayland implementation"; a sentence about CNA's platform implementations
  (or the sentence after one) naming a retired backend, with exemptions tied to the name's own clause or list;
  platform-implementation table cells; one-name-per-item lists; middot-separated lists.
* `check_retired_renderers.py`: role predicates ("DirectX 12 is one of the renderer families"), the previous
  sentence as context, list items and `<br>` lines under a renderer heading, header-less cells under a renderer
  heading, "CNA renders through ...".
* `adversarial_audit.py`: a tokenless SUPERSEDED concept's review needs `result` ∈ {retired, replaced,
  no-current-statement}, a reason of at least six words, and `evidence` (retired / no-current-statement) or an existing
  `replacement` anchor (replaced). No concept uses the escape; existing records are unaffected.
* `test_validators.py`: 79 → 205 fixtures (every sentence above, the probes' bypasses, allowed counterparts, eight
  review-escape cases).
* One applied page fix whose text was corrected here carries `superseded_by` this record
  (C06-ch25-abstraction-layers-two-F3-2); the ledger token of WP12-ch35-089 moved to the corrected sentence.
