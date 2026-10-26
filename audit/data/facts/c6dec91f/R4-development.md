# R4 — Development area, CNA B=c1c316b9 → T=c6dec91f

INTERNAL AUDIT RECORD (not served).

Scope: the hand-written pages under `development/` (91 pages). Not edited: the five generated
references (`development/reference/{modules,cmake-options,test-targets,public-headers,selection-axes}.html`),
`development/maintenance.html` and `development/handbook/update-libcna-com.html` (coordinator), the four
tombstones (`internals/graphics/vulkan.html`, `internals/platforms/{wayland,win32,x11}.html`), and every
generated region (sidebar, breadcrumb, `dev-layers`, `dev-pager`, `<!--p3:deep-links-->`, `<!--p3:issue-links-->`).

## 1. Method

* CNA read, never built: `git show/grep/log` at B and T in `/rv/data/development/github.com/libcna/cna`, and the
  extracted T tree `~/.cache/libcna-com/cna-target` (checked against Git: same `abi.h` bytes, 374/374 files under
  `modules/c-api`). Sibling and binding repositories read from their local clones: sharp-runtime (`next` 4e146b90,
  `v0.1.0` = c20373ba = its `main`/`develop`), easy-gl (`develop` = `v0.1.1` f4d6afa), meta-gl (`develop` = `v0.4.1`
  dd3b300), cna-dotnet (`860f92c`, `f1f88e1`, head 90b11a2 on 2026-10-25), cna-cemetery (`6661173`).
* Executed against CNA, all read-only: one `tools/count_webgpu_plan_status.sh` (an awk count over
  `plans/plan_webgpu.md`: 202 rows, 201 done, 1 partial) and one `git fetch --dry-run` in the CNA clone (prints, writes
  nothing). Nothing configured, built or run; no file in the CNA repository changed.
* Counts recomputed at T: C ABI 0.50.0 (encoded 0x00003200); `abi_baseline.json` 196 structs, 296 scalars, 1,476
  integer constants, 3,212 exports; 60 public C headers, 59 `.cpp`, 56 spec TOMLs, 56 generated `.inc`; 94
  `*Smoke.c`; COVERAGE.md 466 headers / 8,125 symbols / 7,032 implemented / 15 partial / 625 planned / 453 n/a / 406
  excluded; release gate "Not ready", 1 of 10 criteria unmet; 15 `CApi*` Python gates; 6 `c-api-*` workflows, none
  builds the library; 18 workflows, 16 on push+PR; PlatformCapabilities 31 flags (SDL3: 28 unconditional + 3
  conditional); graphics-ext 9 TUs, 11 public headers, 6 test files, 73 test macros; GraphicsRendererType 10
  enumerators (OpenGLES3=0 … Fna3d=9); maturity 3 Production / 5 Supported / 2 Experimental; category 3 Native / 3
  TranslationLayer / 1 Software / 1 Web / 2 Diagnostic. Java manifest name census re-run (method reproduces B's
  1,933 of 3,210): 1,923 of 2,774 still declared in 3,212 routes, 851 not. cna-dotnet imports 1,419 routes at
  860f92c, f1f88e1 and head; all 1,419 are declared at T.
* No commit, push, `regenerate_site.sh`, `apply_expansions.py fold`; no generated region edited.

## 2. Pages re-verified at T (24; callout "source-verified at the pinned commit … `c6dec91f`", doc-meta c6dec91f)

architecture/graphics, build/architecture, build/index, getting-started, handbook/change-build-configuration,
handbook/fix-a-renderer-bug, handbook/make-a-release, handbook/update-the-c-api, index,
internals/graphics/{backends,device,draw-call,resources,sdl-gpu,selection}, repository/{index,module-graph},
takeover/{blast-radius,inherited,own-a-subsystem,review-ai-generated-code,uncertainty,worked-changes},
testing/architecture.

What was checked on the pages rewritten in the last part of the pass (the earlier ones: renderer set, families,
defaults, descriptors, SDL_GPU capability gaps and CI, device events and leases, CI table, groups and gates, commit
statistics, recomputed per-module numbers — see the page bodies):

* **make-a-release**: version decl (`project(CNA VERSION 0.1.0)`, `CNA_VERSION_PRERELEASE ""`), `docs/releasing.md`
  (current as of 0.1.0; sibling-release step; `cmake-build-multi` + private runner), `DependencyVersions.cmake`
  (0.1.0 / 0.1.1 / 0.4.1, `CNA_CHECK_DEPENDENCY_VERSIONS`), CHANGELOG (`[Unreleased]` Changed/Removed/Fixed,
  `[0.1.0] — 2026-10-10` with Dependencies…Verification, link defs under libcna/cna), tags (`v0.1.0` annotated
  "CNA 0.1.0" on 10a4ef1cb, contained in next/develop/main; T 812 commits after on `next`), Doxyfile and README 0.1.0,
  `CNA_APPLE_BUNDLE_VERSION`, both installed `CNA` packages take their version from `abi.h` (`InstallCxx.cmake`,
  `modules/c-api/CMakeLists.txt`), no workflow runs on tags, `NEXT.md` gone (handoff.md since 2026-10-11).
* **update-the-c-api**: generated route boundaries (`GENERATED_ROUTES.md`, spec → `src/generated/*.inc`, helpers,
  `CApiGeneratedRoutesCurrent`, `CApiRouteGeneratorTests`, `CApi_GeneratedRoutesSmoke`); counts above; ABI history
  0.47.0–0.50.0; MAXIMUM 43 / next 52; 10-row identity table; CNA.NET 0.47.0; slot retirement on generation
  exhaustion; atexit teardown; route-test coverage counts generated test.
* **index / getting-started**: 23 modules, 10/8, 3 platforms, 3 audio; presets (unchanged), siblings and
  `sibling_branch.sh`, SDL3_image gone, Python-gated configure audits, CLAUDE.md `--parallel 8`, `handoff.md`.

## 3. Pages delta-edited only (48; callout keeps its c1c316b9 evidence, now "at the stated evidence commit"; doc-meta c6dec91f; most carry a "re-read at c6dec91f" note naming what was rechecked)

architecture/{bindings,content,overview,platform,runtime}, debugging, handbook/{add-a-regression-test,change-map,
change-public-xna-behavior,conventions,debug-shutdown-and-lifetime,investigate-a-sample-failure,
modify-a-platform-backend,modify-contentmanager}, internals/bindings/{c-api-internals,csharp,java,python},
internals/content/runtime, internals/graphics/{easygl,headless,stub}, internals/index,
internals/modules/{core,gamer-services,graphics-ext,math,net,phone,storage},
internals/platforms/{headless,index,sdl3,terminal}, internals/runtime/{module,startup}, invariants,
reference/index, repository/source-ownership, takeover/{curriculum,index,investigation,mental-model,threading,
validation,xna-oracle}, testing/index, workflows.

Main T facts applied: renderer retirement (no Vulkan surface service, render intent OpenGl/None, `wantsHighDpi`
removed, SDL allowlist sdl-gpu+fna3d, defaults, CanBeginDrawEXT/context-loss families DirectX9/EasyGL/WebGPU);
ABI 0.50.0 and CNA.NET 0.47.0 (f1f88e1); generated C routes; exception arms (+UnauthorizedAccessException → IO);
content readers declared at construction and installed by `Load<T>()` (`detail::BuiltinContent`,
`DeclareBuiltinXnbReaders`, `RegisterBuiltinLoaders`/`RegisterAllBuiltInXnbReaders` install all; XNB registry now
behind a shared mutex; provisional game registrations give way to built-ins); `Matrix::Decompose` follows XNA
(705ea2324; marker `NEW-AUDIT-11` and the cna-bug-259 link removed from internals/modules/math.html);
`CNA/Misc.hpp` retired (CheckRetiredRuntimeFacade.cmake); `CNA_SHARED_LIBRARY` needs CMake ≥ 3.30;
Xml.Serialization on every platform; post_process package without HLSL; avatar review record (item 33);
SDL3 capability set and lazy camera start; ledgers (handoff.md, member-coverage report); CI table.

## 4. Pages with only evidence-wording, doc-meta and dateModified changes (19)

architecture/audio-input, handbook/index, handbook/modify-the-content-pipeline, internals/audio/engine,
internals/content/pipeline, internals/graphics/software, internals/input/events,
internals/modules/{design,devices-ext,devices,diagnostics,inspector,media,video-ffmpeg},
internals/runtime/{frame,shutdown}, takeover/{case-study-components,case-study-storage,ownership}.
They were scanned for renderer, ABI, count and record patterns; nothing T-stale was found in their bodies.

## 5. Ids and links

* Ids renamed or removed (all in the earlier part of the pass): backends `untoured-2d` removed; sdl-gpu `modern` →
  `capabilities`; draw-call `vulkan` → `sdl-gpu`, `vulkan-submit` → `sdl-gpu-submit`; resources `vulkan-target` →
  `deferred-target`. No id changed in the later pages (make-a-release, update-the-c-api and math keep theirs).
* Body links to tombstones removed: `internals/graphics/vulkan.html` from graphics-ext, sdl3, internals/index (and the
  earlier pages). Body links pinned to c1c316b9 replaced: NEXT.md (getting-started → handoff.md,
  removed-renderers.md), GraphicsBackend{Maturity,Category}.hpp (core → GraphicsRenderer*), Misc.hpp and
  CheckUnimplementedRuntimeFacade.cmake (runtime/module → CheckRetiredRuntimeFacade.cmake),
  plan_win32_native_validation.md (phone → plain text, file left the tree 2026-10-11), generate_post_process_hlsl.py
  (graphics-ext, removed). `check_source_links.py`: ok (77 development failures at baseline).
* Retired known-issue link removed from a body: cna-bug-259 (math). All other retired-KI links are in issue-links.

## 6. Not verifiable from source

* Whether sharp-runtime's `v0.1.0` tag carries everything T uses (both it and `next` declare 0.1.0).
* GitHub's default branch (the clone's `origin/HEAD` says main) and whether a GitHub Release object exists.
* Completeness of `[Unreleased]` against the 812 commits.
* Wine genuine-runtime tests in the private runner: the runner's comment says they run there; the 0.1.0 Verification
  says they failed there and passed under Xvfb. Both stated.
* "61 built-in XNB readers" kept on content/runtime: a literal-name heuristic gives the same count at B and T (63
  strings), the exact canonical count was not recomputed.
* `scripts/check_dev_claims.py` not run: its SNAP path points at the dead `/rv/tmp/libcna-v2`.

## 7. Validator state after the pass (development pages of this area)

* `check_retired_renderers.py`: 64 development lines (276 at baseline), all in sidebar, pager, dev-layers,
  deep-links or issue-links; 0 in bodies or heads.
* `check_facts.py`: 20 development findings (234 at baseline): 5 on update-libcna-com.html (coordinator), 15 in
  generated deep-links/issue-links descriptions ("C ABI 0.46.0", "12 renderer families", "14 public renderer
  identities"). 0 callout-wording findings.
* `check_dev_page.py`: 28 pages ERROR, all broken links to retired known issues inside issue-links, plus one missing
  fragment `../internals/graphics/vulkan.html#validation` in testing/index.html's dev-layers.
* `tombstones.py check`: 41 development errors, all in deep-links (19), sidebar (16), dev-layers (13) or pager (5).
* `validate_site.py`: 67 broken development links, all in issue-links; search/sitemap coverage pending regeneration.
* `issue_refs.py check`: 0 errors. `check_retired_platforms.py`: 0.

## 8. Requests for other areas

* docs/verification.html:623 — "a stand-alone ContentManager … needs one explicit RegisterAllBuiltInXnbReaders()"
  is stale: at T `Load<T>()` installs its type's readers; `RegisterBuiltinLoaders()` installs everything.
* Regeneration (scripts/dev_manifest.py, site_dev.py, p3 blocks): dev-layers links to the tombstone
  `internals/graphics/vulkan.html` (architecture/graphics.html:276, internals/graphics/draw-call.html:310,
  resources.html:270, backends.html:283, takeover/worked-changes.html:215, internals/modules/graphics-ext.html:254,
  testing/index.html:283 with `#validation`); sidebars list vulkan.html (internals/graphics/*.html:96); pagers
  easygl.html:269 (next) and sdl-gpu.html:327 (prev) name "Vulkan renderer internals"; dev-layers label "Capability
  matrix (32 flags)" (architecture/platform.html:246, internals/platforms/headless.html:227, index.html:294) → 31;
  issue-links blocks list retired KIs; deep-links descriptions carry "C ABI 0.46.0" and "12 renderer families".
* development/handbook/update-libcna-com.html:211-216 (coordinator): compiled-effect identities 11/9 → 8/6, test
  files 813/781/11,380 → 898/855/11,898, "24 jobs" → 25, "C ABI (0.46.0) … routes (3,210)" → 0.50.0 / 3,212.
* CNA-side drift seen while reading (not site defects): `CnbLoaderRegistry.hpp` comment still says every
  ContentManager constructor registers the loaders; CHANGELOG `[0.1.0]` cites `NEXT.md` §5 (file gone);
  `docs/releasing.md` pushes `develop` while 0.1.0 was cut from `next`; `Matrix.cpp` keeps an unused
  `WithinEpsilon`; `check_renderer_identities.py` names a missing `docs/renderer-expansion-candidates.md`.
