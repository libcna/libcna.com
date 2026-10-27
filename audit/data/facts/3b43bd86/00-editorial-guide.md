# Phase 7 editorial guide — moving libcna.com from CNA `c6dec91f` to `3b43bd86`

INTERNAL (not served). Every person or agent editing pages in this phase follows this file. The facts live in
`R1-facts-and-changes.md` (same directory) and `data/current-facts.json`; this file says how to write them. The Phase 6
guide (`audit/data/facts/c6dec91f/00-editorial-guide.md`) still applies wherever this file does not override it — in
particular its retired-renderer rule (section 2), the retired modern GPU layer (section 3) and its mechanics (section 6).

## 1. What the snapshot is now

* `cnahead` = `3b43bd8687ed46523d873f9bec4b32bd8481dcb5` (CNA `next`, 27 October 2026). Short form `3b43bd86`.
* It is **948 commits after the 0.1.0 release** (`v0.1.0`, 2026-10-10); the version string is still `0.1.0`, the C ABI is
  still **0.50.0**. Never write 0.1.1, never write ABI 0.51.0. Say "a development snapshot after the 0.1.0 release".
* The previous pin `c6dec91f` (2026-10-24) is 136 commits earlier; every one of those commits is first-parent (no merges).
* This is an **incremental** update. Do not rewrite a correct page. Change a sentence only when the source at `3b43bd86`
  says something different, or when the sentence links a file that no longer exists.
* Already done mechanically by the coordinator: `cnahead`, `data/current-facts.json`, and every hand-written CNA source
  link on non-Known-Issues pages whose path still exists at `3b43bd86` was re-pinned (5,645 links). Nine links still point at
  `c6dec91f` because their file is gone (R1 §9 maps each to its successor). The footer sentence is regenerated from
  `cnahead` by `site_nav.py sync`; do not edit footers.

## 2. Evidence callouts (the rule for this phase)

444 pages carry `source-verified at the pinned commit … checked by reading the CNA source at commit <code>c6dec91f</code>`;
19 Development pages carry `at the stated evidence commit … <code>c1c316b9</code>`.

* A page may move its callout to `3b43bd86` (keep the wording "source-verified at the pinned commit", change only the SHA)
  **only after** its claims were checked against the interval: every CNA file it cites and every topic the interval touched
  (R1) was compared with `git diff c6dec91f 3b43bd86 -- <file>`, and any affected sentence corrected. A file that is
  byte-identical between the two revisions cannot invalidate a claim that rests only on it; a change that only rewords a
  comment (most `.cmake`/`.cpp` edits that dropped `plans/plan_vulkan_parity.md` references) does not either.
* A page you could not finish keeps `c6dec91f` and must then say **"at the stated evidence commit"** instead of "at the
  pinned commit" (`check_facts.py` fails the mismatch). Never move a SHA you did not review.
* The 19 `c1c316b9` pages keep their label unless you re-verify the page in full; if a sentence on one is now wrong
  because of the interval, fix the sentence and leave the label honest.
* Other inline mentions of `c6dec91f` on a page (meta descriptions "at snapshot c6dec91f", "Everything here targets CNA
  snapshot c6dec91f", doc-meta lines "CNA snapshot c6dec91f · source links pinned to c6dec91f") follow the page's callout:
  a page whose callout moves gets `3b43bd86` there too; statements about what was *done* at `c6dec91f` (syntax-checked at,
  measured at, re-verified at) stay as history and must read as history.
* Worklist with the CNA files each page cites that changed in the interval, and the interval topics found on it:
  `audit/data/facts/3b43bd86/worklist.json` (`status` "carry" = nothing cited changed and no topic hit; the coordinator moves
  those mechanically; "review" = read before moving).

## 3. The changes that matter for pages (details and evidence in R1)

1. **FNA3D and MojoShader are CNA's forks** `libcna/FNA3D` and `libcna/mojoshader` (upstream FNA-XNA/FNA3D and
   icculus/mojoshader). FNA3D pin `10f650b9d0f6bb0e6f3f9378833fbd807dfe8cde` on the fork's `cna` branch; its MojoShader
   submodule is `03b686fe1a33863a61fa153d6d33c3b6eafa514d` on the MojoShader fork's `cna` branch. CNA **no longer patches
   them at configure time**: the former 133 MojoShader and 4 FNA3D patch files (137 files under `cmake/patches/`) are commits
   on the forks. Never write that the forks are the official/upstream projects; never tell a reader to (re)apply patch files;
   never say the forks are ABI-compatible with upstream shared libraries (they are linked statically only). Do not claim that
   the move to forks fixed anything by itself: the patches became commits; the 2026-10-26 audit fixes are separate.
2. **SDL** moved from `cbe3fbe9` to `86296ac8` (upstream main, 2026-05-15) and now carries **five** CNA patches, each only on
   the platforms that need it (two Emscripten, one iOS, one Android, one Vulkan-backend). The two Vulkan patches CNA carried on
   `cbe3fbe9` are upstream in `86296ac8`. macOS builds SDL exactly as upstream ships it. SDL_shadercross keeps **one**
   build-integration patch, applied only to the build tree's own clone or a staged copy, never to a developer's checkout.
3. **ENet** is upstream master `5a9c537fd464b3c6d3c55e1d3bd47588faf71b42` (ENet 1.3.18 plus later fixes), **vendored
   unmodified** in `third_party/enet` (a committed directory, **not a submodule** — it never was one). The former
   `CNA_PATCHES.md` and the patched 1.3.17 base are gone.
4. **Configure now verifies sources**: `CNA_VENDORED_SOURCE_CHECK=ON|WARN|OFF` (default ON) refuses a stale
   `third_party/SDL`/`SDL_mixer` submodule (e.g. `git pull` without `git submodule update`); a FetchContent-populated FNA3D
   checkout that drifts from the pin is refused unless `CNA_FNA3D_ALLOW_SOURCE_DRIFT=ON`; a `FETCHCONTENT_SOURCE_DIR_FNA3D`
   checkout is only reported. An old tree whose `_deps/fna3d-src` still holds the former patches stops: delete `_deps/fna3d-*`.
5. **Avatar catalog v3 revision 5** (was revision 4) and it is now the **Git submodule** `modules/gamer-services/assets/avatars`
   = `https://github.com/libcna/cna-avatar-assets` (commit `4617a1e7503f`). Configuring with Gamer Services on **fails** until
   the submodule is initialized (`git submodule update --init`); a source archive (GitHub ZIP, `git archive`) has no submodules
   and cannot build avatars; `CNA_ENABLE_GAMER_SERVICES=OFF` does not need the catalog. Revision 5 is byte-identical to the
   in-tree catalog it replaced; no runtime or serialization format changed with the move. Never say avatar assets or avatar
   features were removed.
6. **Immediate SpriteBatch / texture uploads**: an upload to a texture a queued draw samples is now ordered after that draw on
   SDL_GPU (submits queued work first) and WEBGPU (writes into a fresh texture: Texture2D, TextureCube, Texture3D). XNA's
   per-call behaviour of `SpriteSortMode::Immediate` holds on SDL_GPU, WEBGPU, OPENGLES3, OPENGL33, SOFTWARE and FNA3D by
   CNA's recorded test (`spritebatch_sort_mode_semantics` leg B). CNA's handoff §5.1 lists **no open defect**. Remaining,
   external: FNA3D's SDL_GPU driver shows a `TextureCube`/`Texture3D`/mipmapped `Texture2D` changed between two draws of one
   frame in the earlier draw too (FNA3D's driver; reported, not worked around).
7. **SDL_GPU**: binds `RenderTargetCube` faces in any slot of a multi-target set (DC-R1; WEBGPU and DIRECTX9 still refuse
   cube faces in an MRT set); applies `MultiSampleMask` **all-or-none** on a multisampled target and refuses a partial mask
   with `NotSupportedException` (DC-R2; it was silently ignored before); the per-pixel lit vertex colour now multiplies
   `EmissiveColor` (XNA's formula).
8. **New `RendererFeature` values** (33 queryable features, was 31): `MultiSampleMask` (35) and `RenderTargetReadback` (36),
   C constants `CNA_RENDERER_FEATURE_MULTI_SAMPLE_MASK` / `_RENDER_TARGET_READBACK`, both `@since ABI 0.50.0` — **added at the
   same ABI version** (no bump; 1,478 integer constants, 3,212 exports unchanged).
9. **XNA integer pixel centres on multisampled targets too** (measured on XNA 4.0 through DXVK): every renderer now applies its
   63/128-pixel correction to multisampled destinations as well; lines and points keep host centres (unmeasured for XNA).
10. **`new PresentationParameters()` is XNA's default**: 0x0 back buffer, `IsFullScreen = true`. A device built directly from
    it must state a size; CNAEXT `PresentationParameters::CreateWindowedEXT(width, height)` gives a windowed back buffer.
    `GraphicsDeviceManager`, `Game` without a device service, and `GraphicsDevice()` behave as before (800x480 windowed).
11. **C API**: `cna_shader_effect_create` accepts a whole SPIR-V module byte for byte (whole 32-bit words, at least the
    five-word header, SPIR-V magic); every other view is still UTF-8 text. `effects.h` documents that WEBGPU refuses a cube
    sampler binding on its WGSL contract (`CNA_RESULT_NOT_SUPPORTED`). `cna_presentation_parameters_init` gives XNA's values.
    Release gate: 8,134 public C++ declarations, 7,033 implemented, 15 partial, **633 planned**, 453 not applicable
    (inventory of the C++ surface — never call them C routes or "unmapped symbols").
12. **Content pipeline**: `XmlSerializer<Color|Rectangle|Point>` with XNA's measured text; generated nested names unique across
    the whole build (XNA's `stub_N`), in node order, independent of worker count and incremental builds; XNA-typed
    `BuildAndLoadAsset<TextureContent, TextureContent>` answered by the XNA-shaped TextureImporter/TextureProcessor; six
    Pipeline Workshop exception/semantics divergences matched to XNA (R1 §5). Formats (XNB, CNB, CNJ) unchanged.
13. **FNA3D renderer**: double-sided PBR takes Direct3D's `VFACE` sign on every driver; a pass's bump-environment state
    (`BUMPENVMAT`, `BUMPENVLSCALE`, `BUMPENVLOFFSET`) reaches the driver; effect struct defaults follow genuine XNA 4.0.
14. **Input**: `MouseState`/`GamePadState` text follows XNA's IL (`{X:10 Y:20 Buttons:Left Wheel:120}`, `{IsConnected:True}`).
15. **Documentation moved in CNA**: see R1 §9 for every deleted `misc/`, `plans/` and root file and its current successor.

## 4. Known Issues

Only through `audit/data/bible/issues/patches-adversarial.json` and the existing pipeline (`known_issues.py`); never edit
generated pages. Every published entry must be re-checked at `3b43bd86` before the new repin step `c6dec91f → 3b43bd86`
is appended (the step is the claim that each entry was re-verified). Record in `R5-known-issues.md`.

## 5. Evidence wording (unchanged from Phase 6)

"Recorded by CNA" for CNA's own runs, measurements and campaign ledgers (handoff §0/§2 figures, the avatar acceptance, the
fork suites); "not executed here" for anything this update did not run. Linux or Wine evidence is never native Windows, macOS
or iOS qualification. Do not invent benchmarks, results, dates, hardware or compatibility.

## 6. Mechanics

* Do not hand-edit generated regions: `known-issues/**`, `data/known-issues.json`, `development/reference/*.html`, sidebars,
  breadcrumbs, pagers, `<!--p3:deep-links-->`/`<!--p3:issue-links-->` blocks, text inside `<!--issue:KEY-->` markers,
  `search-index.json`, `sitemap.xml`, `img/architecture-diagram.svg`, footers.
* `<!--p3:begin …-->`/`<!--p3:end …-->` regions may be edited; the coordinator folds them back (`apply_expansions.py fold`).
* Do not run `regenerate_site.sh`, `build_site_indexes.py`, `apply_expansions.py fold` or `git commit`.
* Checks you may run: `check_retired_renderers.py`, `check_facts.py` (filter to your files), `check_source_links.py`,
  `validate_site.py`, `check_dev_page.py <page>`, `check_deep_page.py <page>`.
* Record what you changed in your area's record in this directory (page → change, evidence path at `3b43bd86`, statements
  removed or reclassified, uncertainties, pages whose callout you moved and pages you left on `c6dec91f`).
