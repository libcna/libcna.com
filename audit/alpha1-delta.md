# CNA v0.1.0-alpha.1 delta ledger

Audit date: 2026-08-20 (Europe/Prague)

This ledger fixes the source boundary for the libcna.com alpha.1 synchronization. The Git range is used to discover changes; final claims are checked against the immutable tag worktree.

## Source boundary

- BASE: `ae0be4b5211957efaef60f2f23627ae5a9ddda23`
- Tag: `v0.1.0-alpha.1`
- Resolved tag commit: `1bb2145d99ed572dd4eb15009c34e2e5f410fcf0`
- Tag date: 2026-08-20 19:06:23 +0200 (commit date 19:04:19 +0200)
- Exact range: `ae0be4b5211957efaef60f2f23627ae5a9ddda23..1bb2145d99ed572dd4eb15009c34e2e5f410fcf0`
- Ancestry: BASE is an ancestor of the tag.
- CNA HEAD at audit start: `1bb2145d99ed572dd4eb15009c34e2e5f410fcf0`; it is not ahead of the tag.
- Range inventory: 1,445 commits and 6,803 changed paths.

## Canonical facts and website impact

| Topic | BASE state | v0.1.0-alpha.1 state | Evidence at tag | Website impact |
| --- | --- | --- | --- | --- |
| Release identity | No tagged CNA release in the audited site baseline | Product version `0.1.0-alpha.1`; Git tag has the `v` prefix; pre-1.0 prerelease | root `CMakeLists.txt`, `cmake/Version.cmake`, `cmake/templates/Version.hpp.in`, annotated tag object | Put release identity in the homepage and add a release/versioning page; distinguish product version from the Git tag and C ABI version |
| Version API | No generated public version header | Generated `CNA/Version.hpp`; `CNA_VERSION_*` macros and constexpr `CNA::getVersion*()` / `isPreReleaseVersion()` | generated-header template and CMake configuration | Document build-time and runtime version inspection |
| Renderer terminology | Public build selection used `CNA_GRAPHICS_BACKEND`; 39 public identities used older names including `OPENGLES`, `D3D*`, `DX*`, and `ASCII` | Public terminology is renderer; `CNA_GRAPHICS_RENDERER`; DirectX names normalized; ASCII is no longer a renderer identity | BASE/tag `RendererSelection.cmake`, public enum, generated registry | Remove old backend-selection commands and use current identities in prose and examples |
| Renderer inventory | 39 public identities | 50 public identities, implemented by 46 families; no aliases; EasyGL owns five identities | `check_renderer_identities.py`, `check_runtime_renderer_discipline.py`, enum, registry generator and descriptors | Replace the site's 46/42 snapshot everywhere, including metadata and tutorials |
| Runtime renderer selection | One renderer per build | Single-renderer remains default; opt-in `CNA_GRAPHICS_RENDERERS` links a valid set and chooses before device creation through `GraphicsRendererSelection` | `RendererDefaultSelection.cmake`, `RendererCombinations.cmake`, public selection headers/source, generated registry, tests | Rewrite architecture/build/renderer/FAQ material and add a focused guide/tutorial |
| Selection and fallback | Compile-time default was the only identity | Precedence is API, environment, compile-time default. Unknown/uncompiled choices throw. Fallback is explicit opt-in, records failures, and selection latches after first device | `GraphicsRendererSelection`, renderer-selection tests, runtime selection guide corroborated by source | Document hard-failure default, fallback history, window-kind boundary and active-vs-default reporting |
| Renderer combinations | Not applicable | Four configure-time rule families reject PortableGL + real GL, GDI + Software, cross-OS partitions, and Glide + any other renderer | `cmake/RendererCombinations.cmake`, combination gate/tests | Publish the actionable rules without implying arbitrary combinations work |
| Platform architecture | Website described SDL3 as inseparable | `CNA_PLATFORM` independently selects SDL3 (default), SDL2, Headless, or POSIX Terminal; reserved identifiers fail | `PlatformSelection.cmake`, `CNA::Platform::IPlatform`, factory/services, conformance tests | Rewrite platform documentation and separate target OS, host integration, renderer and audio axes |
| Audio architecture | Audio implicitly followed SDL3 | `CNA_AUDIO_PLATFORM` independently selects SDL3 (default), SDL2 or Null at the low-level device boundary; only SDL3 defines `SOUND_ENABLED` and links the SDL3_mixer XNA playback/decoding engine. OpenAL/WASAPI/ALSA are reserved and rejected | `AudioPlatformSelection.cmake`, `modules/CMakeLists.txt`, audio module source filtering, device factories and tests | Document the independent axis without claiming feature parity; qualify SDL2/Null as device/configuration surfaces rather than equivalent production mixers |
| SDL2 constraint | No independent SDL2 mode | SDL2 is a real SDL 2.30 implementation. Pairing SDL2 platform and audio refuses SDL3-direct renderers (`SDL_RENDERER`, `SDL_GPU`, `FNA3D`, `FREEDIRECT`) | selection/build checks and platform combination tests | Add the incompatibility to build/platform guidance |
| Compiled Effect Framework bytecode | Site said all compiled `.fx`/EffectReader use was unsupported | D3D9 Effect Framework `.fxb`, including XNA wrapping and XNB Effect payloads, is implemented. HLSL `.fx` source and MGFX remain unsupported | `Effect` bytecode constructor/runtime, `EffectContentTypeReader`, tests, renderer capability implementations | Replace blanket warnings with format- and renderer-qualified truth; update all affected tutorials |
| Compiled-effects renderer boundary | None | FNA3D always; EasyGL, SDL_GPU and Vulkan only with their `*_COMPILED_EFFECTS=ON` options (all default off); every other renderer reports false | renderer CMake files, capability implementations and effect runtime factories | Publish a precise support table and avoid universal claims |
| Capability surface | 13 members before the compiled-effects work | `GraphicsCapability` has 14 members. The base returns false for multi-stream input, routes compiled effects through a false-by-default opt-in, delegates stencil, and returns true for the rest; four renderer families inherit it unchanged | public enum and `IGraphicsRenderer::SupportsCapability`, renderer overrides | Correct enum counts and the permissive-default warning across renderer tutorials |
| Deliberately 2D-only identities | 11 identities in the older site snapshot | 13 identities: `SDL_RENDERER`, `DIRECT2D`, `CANVAS`, `HTML_DOM`, `SKIA`, `BLEND2D`, `FREEDIRECT`, `DIRECTX1`, `GDI`, `SVG_DOM`, `OPENVG`, `NANOVG` and `PIXIJS` | final capability implementations and deterministic 3D-refusal paths | Add NanoVG/PixiJS to every repeated 3D tutorial boundary and update the site-wide count |
| Native C API | Absent | Experimental C API source behind `CNA_BUILD_C_API=ON`; declared ABI `0.7.0`; intended C17 implementation/C99 consumer and shared/static package rules. The final target is compile-blocked because its 49-entry renderer map is asserted against 50 canonical C++ identities; NanoVG is missing. With networking disabled it fails earlier on an unconditional GamerServices include | root/module CMake, `CNA/C/abi.h`, `CnaCApiCoreExt.cpp`, C renderer header, canonical renderer registry, isolated Headless/Null-audio GCC 14.2 builds with networking on and off | Add a dedicated C API page and diagnostic tutorial; distinguish the broad checked-in contract from the absence of a consumable alpha.1 library |
| C API measured surface | Absent | 59 C headers; 2,861 declared routes; route-name gate reports 2,861/2,861; generated inventory records 6,317 implemented, 15 partial, 380 N/A out of 6,712 public-symbol rows | headers, route test gate, `docs/c-api/COVERAGE.md` | State scope with qualified, reproducible counts; keep product and ABI versions separate |
| Public API movement | Monolithic include layout and older public names | Source reorganized into modules; new renderer selection, platform, target-platform, fallback, glTF/CNAEXT and version APIs; old `GraphicsBackendType`, `Platform` enum and `Entrypoint.hpp` removed/renamed | public-header range diff (790 path changes: 135 additions, 26 deletions, 629 moves/renames) | Sweep symbols and code samples; avoid presenting internal module paths as install paths |
| glTF import | Runtime path was documented as first-group-only, dropping rigid animation and factor-only PBR, refusing non-triangle modes and ignoring required extensions | Direct loading combines all mesh groups in one `Model`; `SkinsEXT` maps every skin; unskinned rigid clips use `ModelAnimationsEXT`; factor-only and vertex-coloured PBR are preserved; all seven primitive modes are supported/conversion-mapped; required extensions are registry-gated; both direct and CNJ paths expose `GltfImportReportEXT` | final `GltfImportCore`, `ContentManager`, public Model/animation headers, source-owned extension/layout/PBR/topology tests | Rewrite model loading, FAQ, compatibility, verification and tutorials 35/110/111/112/114; retain the unit-scale and mixed skin/rigid `Tag` boundary |
| glTF PBR renderer scope | Older site described narrower map-driven selection and incomplete WebGPU skinning | Material-model-driven PBR; seven map slots; two packed UV channels with per-map transforms; 16 full PBR families consume universal parameters, Software is a reduced CPU check; 14/16 full families sample both optional specular maps, Metal/Wicked are factor-only and refuse coloured PBR rather than draw it incorrectly | `GltfRendererPbrFallbackPolicyTests.cpp`, vertex-layout table, PBR headers and renderer implementations | Replace blanket/fallback claims with family- and feature-qualified coverage |
| Tests | Site published one stale universal count | Tag contains 568 test source files and 8,263 static GoogleTest definition macros; instantiated and CTest counts depend on options/renderer/platform | tag source inventory and CMake registration | Replace universal executable/CTest totals with scoped source facts and explain configuration variance |
| CI | Site described a much narrower matrix | 21 workflow files cover multi-renderer, Emscripten, platform, Apple/Metal, declared C API and focused renderer/subsystem gates; Windows renderer workflows are manual. The intended unfiltered job and two Input rows use invalid `EASYGL`; the C API final target has its independent count assertion failure | `.github/workflows/`, final renderer identity validator and C API implementation at tag | Rewrite verification/CI claims; distinguish declared, working, broken, automatic, manual, build-only and runtime lanes |
| Post-tag contamination | Potential because live trees can move | CNA HEAD equals the resolved tag; `v0.1.0-alpha.1..HEAD` contains zero commits at audit start | Git object resolution and rev-list | Still perform a final changed-claim sweep against the tag before completion |

## Source contradictions found

- `CHANGELOG.md` says 49 renderer identities, while the final enum, CMake identity list and generated runtime registry contain 50; NanoVG is the additional final identity.
- `docs/runtime-renderer-selection.md` correctly says 46 families / 50 identities but also says “all 45 factories” in the same table. The descriptor gate reports 46 families.
- `CHANGELOG.md` presents compiled Effect Framework bytecode as FNA3D-only. Tag implementation also supports opt-in EasyGL, SDL_GPU and Vulkan configurations.
- `docs/fx-compiled-effects.md` has an early support table that omits Vulkan, while its later tag-era section and Vulkan implementation include the opt-in path.
- `docs/c-api/ABI_VERSIONING.md` mentions ABI 0.4.0, but the public `CNA/C/abi.h` and C++ ABI assertions define 0.7.0.
- `docs/c-api/FEATURE_MATRIX.md` and the generated release-gate heading still label the C ABI 0.1.0, while the public ABI header defines 0.7.0. The website follows the header for the binary contract.
- `.github/workflows/c-api-release-gate.yml` says the gate is “NOT READY”, while the checked-in generated `docs/c-api/RELEASE_GATE.md` says “Ready. Every criterion below is met.” Final source settles the dispute: `CnaCApiCoreExt.cpp` has 49 C renderer rows against 50 canonical identities and its own `static_assert` must fail. The website documents source presence but no usable alpha.1 C library.
- Several historical CNA coverage documents still say that ContentManager is not XNB-based or that EffectReader is missing; tag implementation and tests contain registered XNB readers and a real EffectReader.
- `scripts/check_renderer_identities.py` retains prose comments about 49 identities even though its parsed final tag result is 50.
- `general-tests-ci.yml` and two `input-ci.yml` rows still configure `CNA_GRAPHICS_RENDERER=EASYGL`, but final tag CMake accepts only the five EasyGL profile identities and has no `EASYGL` alias. The intended unfiltered suite and those two Input rows therefore fail before building.
- The generated C API inventory check reports two explicit rules matching no symbols in the detached tag worktree, despite the checked-in release-gate report being marked ready; the checked-in inventory numbers are therefore reported as a tag snapshot, not as a freshly regenerated success.
- The public C renderer enum and `RendererIdentities` mapping omit NanoVG even though the C++ public enum, generated registry and build selection expose it. The implementation's deliberate canonical-count assertion makes this a release-blocking compile defect, not merely missing runtime coverage.
- `CNA_BUILD_C_API=ON` does not require `CNA_ENABLE_NET=ON` at configure time, but the C API unconditionally includes `GameUpdateRequiredException.hpp`; a networking-disabled build therefore fails before it reaches the renderer-map assertion.
- Several final glTF implementation comments still describe the superseded map-presence and `!colored` PBR selection rule even though the executable assignment is material-model-driven and the source-owned defect/layout tests require factor-only and coloured PBR. The website follows the code and tests.
- A final `ContentManager.cpp` comment still refers to loading the “first group”, while the same final function iterates every group and the runtime model tests require the combined model plus complete `SkinsEXT` mapping.
- Tag-era glTF prose/generated summaries disagree on 15 versus 16 full PBR families and on four versus two pending specular-texture families. The source-owned renderer partition at the tag enumerates 16 full families, with 14 sampling both specular maps and Metal/Wicked factor-only; Software is explicitly a seventeenth reduced CPU cross-check.
- `NEXT.md`, `docs/direct2d-renderer.md`, the Direct2D test name and `plan_binding.md` still describe 13 graphics capabilities. The final public enum has 14 because `CompiledEffects` was appended; the website follows the enum and executable switches, including the false fall-through where a renderer did not add a named arm.
- `plan_platform.md` records successful Null-device memory-mixer/XACT slices during implementation, which can read like high-level Null playback support. Final `modules/CMakeLists.txt`, `docs/platform-sdl2.md` and the media/content source guards define `SOUND_ENABLED` only for SDL3; the website therefore presents SDL2/Null as low-level device selections, not feature-equivalent playback engines.

## Audit notes

Temporary detached worktrees were used for direct inspection of BASE and the tag, then removed after validation. The CNA checkout itself was not edited, reset, merged or switched. Because its clean HEAD equalled the tag, it also served read-only as source for an isolated `/tmp` C API build; no build output was written into CNA, and the build directory was removed.

## Website impact inventory

- Baseline: 168 HTML files, including 125 tutorials; 164 indexed/canonical public pages.
- Alpha.1 result: 175 HTML files, including 129 tutorials; 171 indexed/canonical public pages.
- Existing pages changed: 166. Of these, 102 received substantive release content updates; the rest received the release snapshot footer and/or metadata/HTML cleanup. Two generated Emscripten demo shells were preserved unchanged.
- New pages: `docs/releases.html`, `docs/runtime-renderer-selection.html`, `docs/c-api.html`, and tutorials 126–129.
- Existing tutorials were searched as a complete 125-page corpus; 72 received substantive release corrections and all received the release snapshot footer.
- Homepage facts now include the product release, renderer identity/family inventory, 568 test sources / 8,263 static definitions, 63/86 XNA samples ported, and 21 workflow files. The project owner confirmed that `cna-samples` has not changed since the previous audit.
- The homepage ecosystem section now distinguishes CNA-tag truth from independently moving companion repositories and links additional verified public OpenEggbert projects. Private repositories discovered locally were not published.

## Validation results

- `scripts/validate_site.py`: 175 HTML files parsed; 173 authored pages pass strict HTML5 parsing. The two checked-in Emscripten-generated shells are tolerant-parse-only explicit exemptions.
- 10,083 link/resource references and 486 local fragments inspected; zero missing local targets or fragments.
- Duplicate IDs: zero.
- JSON-LD: 140 blocks parsed structurally.
- Search index: 171 entries; unique and exactly complete for intended public pages.
- Sitemap: 171 URLs; unique and exactly complete for intended public pages.
- Metadata and canonical URL coverage: complete for authored site pages.

## Final boundary and visual checks

- The stale-fact sweep found no unintended public occurrence of the former 46-renderer / 42-family inventory, the 11-identity 2D-only set, a blanket missing `EffectReader`, an unversioned release, or an SDL3-inseparable platform claim. Remaining search hits are deliberate: the `SoundEffectReader` codec exception, a migration row from `CNA_GRAPHICS_BACKEND`, and alpha.1's broken `EASYGL` workflow values.
- CNA still resolved to `1bb2145d99ed572dd4eb15009c34e2e5f410fcf0`; `v0.1.0-alpha.1..HEAD` contained zero commits and an empty diff. The CNA checkout remained clean.
- Firefox visual QA at 1280×900 covered the homepage, Graphics Renderers, Platform Support, Effects System, Building, Experimental C API, Releases & Versioning, tutorial index, tutorial 126 and Verification & Known Issues. The homepage was also inspected in forced dark theme, at 390×844 with the mobile menu open, and through a tall capture of the complete expanded Related projects grid. No visible overflow, overlap, unreadable theme contrast or broken navigation layout was found.
- `git diff --check` passed. The complete 169-file tracked diff (2,132 insertions, 1,546 deletions) and all 10 new files were reviewed; new-file trailing-whitespace and merge-marker sweeps were clean.
- Both temporary detached CNA worktrees and the isolated C API build were removed. Nothing was pushed.

## Remaining uncertainties

- No universal CNA pass count exists: no one build can compile/register every platform- and renderer-specific test. The website therefore publishes source inventory and configuration-scoped verification rules, not a synthetic pass total.
- Native Windows, Android hardware, physical iOS devices and the full GPU/oracle matrix were not executed in this Linux documentation audit. Claims for them remain explicitly limited to source, cross-build, simulator, manual or CI evidence present at the tag.
- Companion repository descriptions were checked against their public repositories on 2026-08-20, but those projects have independent branches and release cadence; the homepage marks them as references rather than alpha.1 source truth.
