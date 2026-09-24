# Fact sheet 08 - external ecosystem (bindings, samples, demos, showcase projects, link liveness)

Phase 1 research, read-only. Collected 2026-09-24 (UTC evening). Nothing was built, compiled or run
(no cmake/make/compiler; no browser run). All repository content below was read with `git show HEAD:...`,
`git grep ... HEAD`, `git ls-tree` (committed content), never from working-tree state. Network facts
come from `curl` (HEAD, falling back to GET on non-2xx, 15 s timeout, 0.3 s spacing) and the public
GitHub/YouTube endpoints.

Immutable reference points used throughout:

| Item | Value |
|---|---|
| Website baseline (read-only) | libcna.com `be359024e3012653fa1e4963eb3ef86d9c16a5b7` |
| CNA TARGET | `009d40f5dd085c4e674d3479675fac84b12b3e0a` (2026-09-24 17:08 +0200), = tip of GitHub `libcna/cna` branch **`next`** (confirmed: `compare next...TARGET` = identical) |
| CNA BASE | tag `v0.1.0-alpha.1` -> commit `1bb2145d99ed572dd4eb15009c34e2e5f410fcf0` (2026-08-20). `git log v0.1.0-alpha.1..TARGET` = 2,877 commits |
| C ABI at TARGET | **0.29.0** (`modules/c-api/include/CNA/C/abi.h`: MAJOR 0, MINOR 29, PATCH 0; `docs/c-api/ABI_VERSIONING.md` "The ABI is `0.29.0`") |
| C ABI at BASE | **0.7.0** (same header at `/rv/tmp/libcna-v2/cna-base`) |
| ABI policy | ABI `0.x` is experimental: an incompatible change requires a minor increment (`ABI_VERSIONING.md`: "ABI `0.x` is experimental: an incompatible change requires a minor-version increment, release notes and a regenerated ABI baseline"). Between 0.21.0 and 0.29.0 the minor moved 8 times (0.22 ... 0.29). Per the doc, 0.22-0.27 are additive (0.22 restored 10 renderer identities, 0.23 added a route, 0.24/0.25/0.26/0.27 added one identity each) while two are incompatible: **0.28.0 retired 25 renderer identities** (ceiling 51 -> 46) and **0.29.0 deleted `cna_sprite_batch_draw_mesh_ext` and `CNA_SpriteMeshEXT`**. |
| GitHub default branch of `libcna/cna` | `develop` = `1bb2145d9` (the alpha.1 commit). So every website link of the form `.../blob/master/...`, `.../tree/develop/...` shows **alpha.1**, not TARGET. TARGET is reachable only via `.../tree/next` or a SHA permalink (both verified 200). `libcna/cna` has **no GitHub Release objects** (`releases` API = `[]`); only tags `v0.1.0-alpha.1` and `audit-2026-07-complete`. |
| GitHub default branch of `libcna/sharp-runtime` | `main` (`54578590b`); the branch the ecosystem builds against is `next` (`41b918c97ed47288f87a0af176fe23942af24cdd`, 2026-09-20 23:49 +0200), so `git clone` of the default branch does not give the dependency the samples/apps use. |

Pin convention: "HEAD" means the local clone's checked-out HEAD, and where it equals the GitHub default-branch
head this is stated ("= remote"). Where the local clone differs from the public default branch the GitHub value
is given as well, because that is what a website visitor sees. 12-character SHAs are unambiguous prefixes.

---

## Link liveness table

Extraction: every `https?://` string in `index, demos, showcase, videos, features, about, documentation,
tutorials, architecture, roadmap, network, contact, contribute, docs/roadmap, docs/vs-alternatives,
docs/releases` (.html) = 406 occurrences = **234 distinct URLs** (145 are libcna.com self-links, 48 github.com,
13 demos.libcna.com, 4 youtube.com, remainder third-party). Excluded (not live URLs): placeholders
`https://www.youtube.com/embed/TODO_VIDEO_ID_1`, `https://www.youtube.com/embed/VIDEO_ID_HERE`,
`https://www.youtube.com/watch?v=VIDEO_ID_HERE` (videos.html comments/TODO markup) and the schema.org
template `https://libcna.com/search.html?q={search_term_string}`.

Result: **230 answer 200** (11 of them after a redirect, listed below), **4 are dead (404)**, 0 timeouts.

**Dead links (all four are GitHub 404s, HEAD and GET):**

1. `https://github.com/libcna/cna-craft` (index, about, showcase). No repo of that name exists in `libcna` or `openeggbert`.
   The source is a git subtree inside the public repo `libcna/cna-lab`: `https://github.com/libcna/cna-lab/tree/develop/cna-craft` = 200 (78 files at cna-lab HEAD).
2. `https://github.com/libcna/cna-editor` (index). Same: `https://github.com/libcna/cna-lab/tree/develop/cna-editor` = 200 (214 files).
3. `https://github.com/libcna/easy-3d` (index). The repo lives at `https://github.com/openeggbert/easy-3d` = 200 (public, `develop`, pushed 2026-07-18).
4. `https://github.com/libcna/cna/tree/master/include/Microsoft/Xna/Framework/` (documentation.html). There is no `master` branch on `libcna/cna` (branches: develop, main, next, opengl4-modern-graphics, work) and no top-level `include/` since the module split.
   Working replacements: `https://github.com/libcna/cna/tree/009d40f5dd085c4e674d3479675fac84b12b3e0a/modules/core/include/Microsoft/Xna/Framework` (TARGET, 200) or `.../tree/v0.1.0-alpha.1/modules/core/include/Microsoft/Xna/Framework` (200).

**Redirects that resolve (11 rows flagged `redirect` in the table; all end 200):** `discord.gg/vrnc4n6DaE` -> `discord.com/invite/...`;
`github.com/libcna/cna/blob/master/{LICENSE,NOTICE.md,THIRD_PARTY_NOTICES.md}` -> `.../blob/develop/...` (GitHub redirects these to `develop`); `.git` clone-URL forms of cna, easy-gl, meta-gl, sharp-runtime, free-direct -> repo page; `opensource.org/licenses/MS-PL` -> `/license/MS-PL`;
`wiki.libsdl.org/SDL3/` -> `/SDL3/FrontPage`. Legacy `github.com/openeggbert/<repo>` URLs for transferred repos (cna, cna-samples, sharp-runtime, cna-cs)
also redirect to `libcna/<repo>` (200), which matters because most binding/sample READMEs still link `openeggbert/cna`.

Note on one row: `learn.microsoft.com/.../bb200104(v=xnagamestudio.41)` first showed 404 because my extraction regex dropped the closing `)`;
the real URL (with the parenthesis) returns 200. The same URL with `.aspx` appended is a 404 and is not used on the site.

**Special targets (all 200):** `https://speedyblupi.com/SpeedyBlupi2013/` (analysed in the Speedy Blupi section), `https://demos.libcna.com/` and all 12 demo pages linked from
demos.html, `https://samples.libcna.com/`, `https://blog.libcna.com/` (title "CNA's Blog - Blog for CNA - Reimplementation of XNA 4.0"),
`https://www.youtube.com/@libcna` (title "LibCNA - YouTube", channel id `UCPzn-tQBEVFwqGWQaB1SLRw`), `easygl.libcna.com`, `metagl.libcna.com`, `meshcraft.libcna.com`,
`bible.libcna.com` and `book.libcna.com` (status only checked, content deliberately not read). Also all 38 `.wasm/.js/.data` artifacts behind the 14 demos.libcna.com
demos and 44 of 44 samples.libcna.com gallery/bundle pages answer 200.

**YouTube (oEmbed + watch page):**

| Video ID (videos.html) | Site caption | Real title (oEmbed) | Channel | Uploaded | Length | Real description (abridged) |
|---|---|---|---|---|---|---|
| `YzhewIB2X9c` | "House 3D Demo - CNA ... rendering a 3D house model using the EasyGL (OpenGL) renderer" | "CNA (reimplementation of XNA 4.0) now partially supports 3D" | **Open Eggbert** (`@OpenEggbert-e7t`), not @libcna | 2026-05-03 | 48 s | "I am working on the CNA C++ library ... Today the basic support for 3D was added." No mention of a house or EasyGL. |
| `TScL1L-dbHE` | "Speedy Blupi on CNA ... Classic Speedy Blupi game running on CNA" | "Speedy Blupi for Windows Phone was ported to C++" | **Open Eggbert** | 2026-04-25 | 101 s | "originally written in C# ... Now it is rewritten to the C++ programming language. The C++ version of the game is working without any issues. The sound is working too, but not was recorded. Currently supported platforms: Linux - But Windows, Android and web will be added very soon ... SDL 3 library is used internally." CNA is **not named** in the video's title or description. |
| `tIMj20Ts2dg` | "CNA 2D Demo - SpriteBatch ... rotating sprites that move and scale dynamically" | "CNA (C++ reimplementation of XNA 4.0) now supports 2D" | **Open Eggbert** | 2026-04-11 | 13 s | "This is demo of CNA ... built on top of SDL 3 ... Speedy Blupi rewritten from C# to C++ already starts, but fails ... CNA can handle even 5000 Blupi images." Nothing about rotating/scaling sprites. |

All three exist (oEmbed HTTP 200). They are about 5 months old, from a different channel than the one the nav links to, and predate alpha.1 (2026-08-20) by 3.5-4.5 months.
The channel the site links, `https://www.youtube.com/@libcna`, exists and currently has **5 videos, all September 2026**: `asNrr1IR1MQ` "CNA Car Simulator" (2026-09-15, 6:08),
`AtfnlksbRCg` "Living Room Simulator - a CNA 3D demo" (2026-09-14, 3:35), `bvENJr9gwgw` "CNA Car Simulator #2 - Helicopter was added" (2026-09-19, 4:16),
`h4OPWa_GVsU` "Wolf CNA" (2026-09-19, 1:00), `hWiBU46D6h8` "CNA Street - a city street built with CNA" (2026-09-22, 2:39). videos.html still carries a "TODO: YouTube channel link" banner although the nav already links `@libcna` (200).

### Full table (every distinct URL; `pages` codes: idx=index, demos, show=showcase, vid=videos, feat=features, about, doc=documentation, tut=tutorials, arch=architecture, road=roadmap, net=network, cont=contact, contr=contribute, d/road=docs/roadmap, d/vs=docs/vs-alternatives, d/rel=docs/releases)

| URL | status | final URL (if different) | note |
|---|---|---|---|
| https://bible.libcna.com | 200 | - | [pages: idx] |
| https://bible.libcna.com/ | 200 | - | [pages: net] |
| https://[retired].github.io/[retired]/ | 200 | - | [pages: cont] |
| https://blog.libcna.com/ | 200 | - | [pages: about,arch,cont,contr,d/rel,d/road,d/vs,demos,doc,feat,idx,net,road,show,tut,vid] |
| https://book.libcna.com/ | 200 | - | [pages: net] |
| https://book.libcna.com/CNA_Bible.pdf | 200 | - | [pages: idx,net] |
| https://demos.libcna.com/ | 200 | - | [pages: demos,net] |
| https://demos.libcna.com/black-pine/black-pine.html | 200 | - | [pages: demos] |
| https://demos.libcna.com/cna-craft/CnaCraft.html | 200 | - | [pages: demos] |
| https://demos.libcna.com/cna_demo_2d/cna_demo_2d.html | 200 | - | [pages: demos,show] |
| https://demos.libcna.com/cna_demo_house_3d/cna_house3d_demo.html | 200 | - | [pages: demos,show] |
| https://demos.libcna.com/cna-examples/cna_examples.html | 200 | - | [pages: demos] |
| https://demos.libcna.com/iron-gang/play.html | 200 | - | [pages: demos] |
| https://demos.libcna.com/lines-cna/winlinez_cna.html | 200 | - | [pages: demos] |
| https://demos.libcna.com/mario-cna/copper-boots.html | 200 | - | [pages: demos] |
| https://demos.libcna.com/mesh-craft/MeshCraft.html | 200 | - | [pages: demos] |
| https://demos.libcna.com/people-cna/People.html | 200 | - | [pages: demos] |
| https://demos.libcna.com/tamagotchi-cna/TamagotchiCna.html | 200 | - | [pages: demos] |
| https://demos.libcna.com/wolf-cna/wolf-cna.html | 200 | - | [pages: demos] |
| https://discord.gg/vrnc4n6DaE | 200 | https://discord.com/invite/vrnc4n6DaE | redirect [pages: about,arch,cont,contr,d/rel,d/road,d/vs,demos,doc,feat,idx,net,road,show,tut,vid] |
| https://docs.monogame.net/articles/index.html | 200 | - | [pages: about,doc,idx] |
| https://easygl.libcna.com/ | 200 | - | [pages: net] |
| https://fna-xna.github.io/ | 200 | - | [pages: cont] |
| https://fna-xna.github.io/docs/ | 200 | - | [pages: about,doc,idx] |
| https://github.com/FNA-XNA/FNA | 200 | - | [pages: about,contr,idx] |
| https://github.com/libcna | 200 | - | [pages: cont,d/rel] |
| https://github.com/libcna/cna | 200 | - | [pages: about,arch,cont,contr,d/rel,d/road,d/vs,demos,doc,feat,idx,net,road,show,tut,vid] |
| https://github.com/libcna/cna/blob/master/LICENSE | 200 | https://github.com/libcna/cna/blob/develop/LICENSE | redirect [pages: about,arch,cont,contr,d/road,d/vs,demos,doc,feat,idx,net,road,show,tut,vid] |
| https://github.com/libcna/cna/blob/master/NOTICE.md | 200 | https://github.com/libcna/cna/blob/develop/NOTICE.md | redirect [pages: contr] |
| https://github.com/libcna/cna/blob/master/THIRD_PARTY_NOTICES.md | 200 | https://github.com/libcna/cna/blob/develop/THIRD_PARTY_NOTICES.md | redirect [pages: contr] |
| https://github.com/libcna/cna/blob/v0.1.0-alpha.1/CHANGELOG.md | 200 | - | [pages: d/rel] |
| https://github.com/libcna/cna/blob/v0.1.0-alpha.1/LICENSE | 200 | - | [pages: about] |
| https://github.com/libcna/cna/blob/v0.1.0-alpha.1/NOTICE.md | 200 | - | [pages: about] |
| https://github.com/libcna/cna/blob/v0.1.0-alpha.1/THIRD_PARTY_NOTICES.md | 200 | - | [pages: about,idx] |
| https://github.com/libcna/cna-craft | 404 | - | DEAD (HEAD and GET both 404) [pages: about,idx,show] |
| https://github.com/libcna/cna-cs | 200 | - | [pages: idx] |
| https://github.com/libcna/cna/discussions | 200 | - | [pages: cont] |
| https://github.com/libcna/cna-editor | 404 | - | DEAD (HEAD and GET both 404) [pages: idx] |
| https://github.com/libcna/cna-examples | 200 | - | [pages: demos,idx] |
| https://github.com/libcna/cna-extended | 200 | - | [pages: idx,show] |
| https://github.com/libcna/cna.git | 200 | https://github.com/libcna/cna | redirect [pages: contr,idx] |
| https://github.com/libcna/cna-gltf-viewer | 200 | - | [pages: idx] |
| https://github.com/libcna/cna/issues | 200 | - | [pages: cont] |
| https://github.com/libcna/cna-java | 200 | - | [pages: idx] |
| https://github.com/libcna/cna/pulls | 200 | - | [pages: cont] |
| https://github.com/libcna/cna-python | 200 | - | [pages: idx] |
| https://github.com/libcna/cna/releases | 200 | - | [pages: demos] |
| https://github.com/libcna/cna-rust | 200 | - | [pages: idx] |
| https://github.com/libcna/cna-samples | 200 | - | [pages: about,demos,idx,show] |
| https://github.com/libcna/cna-swift | 200 | - | [pages: idx] |
| https://github.com/libcna/cna-template | 200 | - | [pages: idx] |
| https://github.com/libcna/cna/tree/master/include/Microsoft/Xna/Framework/ | 404 | https://github.com/libcna/cna/tree/develop/include/Microsoft/Xna/Framework | DEAD (HEAD and GET both 404) [pages: doc] |
| https://github.com/libcna/cna/tree/v0.1.0-alpha.1 | 200 | - | [pages: d/rel] |
| https://github.com/libcna/cna-ts | 200 | - | [pages: idx] |
| https://github.com/libcna/easy-3d | 404 | - | DEAD (HEAD and GET both 404) [pages: idx] |
| https://github.com/libcna/easy-gl | 200 | - | [pages: idx] |
| https://github.com/libcna/easy-gl.git | 200 | https://github.com/libcna/easy-gl | redirect [pages: contr,idx] |
| https://github.com/libcna/mesh-craft | 200 | - | [pages: idx] |
| https://github.com/libcna/meta-gl | 200 | - | [pages: idx] |
| https://github.com/libcna/meta-gl.git | 200 | https://github.com/libcna/meta-gl | redirect [pages: idx] |
| https://github.com/libcna/sharp-runtime | 200 | - | [pages: idx] |
| https://github.com/libcna/sharp-runtime.git | 200 | https://github.com/libcna/sharp-runtime | redirect [pages: contr,idx] |
| https://github.com/libcna/xna4-spec | 200 | - | [pages: idx] |
| https://github.com/openeggbert | 200 | - | [pages: idx] |
| https://github.com/openeggbert/free-api | 200 | - | [pages: idx] |
| https://github.com/openeggbert/free-direct | 200 | - | [pages: idx] |
| https://github.com/openeggbert/free-direct.git | 200 | https://github.com/openeggbert/free-direct | redirect [pages: contr] |
| https://github.com/openeggbert/free-eggbert | 200 | - | [pages: idx] |
| https://github.com/openeggbert/galaxy-eggbert | 200 | - | [pages: idx] |
| https://github.com/openeggbert/mobile-eggbert | 200 | - | [pages: idx] |
| https://github.com/openeggbert/openeggbert | 200 | - | [pages: idx] |
| https://github.com/openeggbert/planetblupi | 200 | - | [pages: idx] |
| https://learn.microsoft.com/en-us/previous-versions/windows/xna/bb200104(v=xnagamestudio.41) | 200 | - | extraction artefact: regex cut the closing parenthesis; full URL re-checked = 200 (the same URL with .aspx is 404, not used on site) [pages: doc,idx] |
| https://libcna.com/ | 200 | - | [pages: idx] |
| https://libcna.com/about.html | 200 | - | [pages: about] |
| https://libcna.com/architecture.html | 200 | - | [pages: arch] |
| https://libcna.com/contact.html | 200 | - | [pages: cont] |
| https://libcna.com/contribute.html | 200 | - | [pages: contr] |
| https://libcna.com/demos.html | 200 | - | [pages: demos] |
| https://libcna.com/docs/releases.html | 200 | - | [pages: d/rel] |
| https://libcna.com/docs/roadmap.html | 200 | - | [pages: d/road] |
| https://libcna.com/docs/tutorials/01-introduction.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/02-setup.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/03-first-window.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/04-game-lifecycle.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/05-game-loop.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/06-first-shape.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/07-colors.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/08-textures.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/09-spritefont.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/100-shipping.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/101-renderer-capabilities.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/102-opengl-family.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/103-direct3d-windows.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/104-directx-ladder.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/105-browser-renderers.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/106-vector-renderers.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/107-cpu-renderers.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/108-fna3d.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/109-metal-macos.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/10-keyboard.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/110-gltf-models.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/111-cnj-pipeline.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/112-gltf-animation.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/113-morph-targets.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/114-pbr-materials.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/115-cnaext-overview.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/116-post-process-effects.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/117-devices-layer.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/118-dynamic-audio.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/119-3d-audio.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/11-mouse.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/120-xact.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/121-video-playback.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/122-media-library.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/123-achievements.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/124-web-gotchas.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/125-pixel-testing.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/126-multi-renderer-build.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/127-platform-audio-selection.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/128-compiled-xna-effects.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/129-c-api-first-program.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/12-moving-sprites.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/13-sprite-sheets.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/14-sound-effects.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/15-background-music.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/16-collision-detection.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/17-camera-2d.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/18-game-states.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/19-save-load.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/20-build-run.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/21-spritebatch.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/22-blend-modes.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/23-render-targets.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/24-post-processing.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/25-sprite-sort-mode.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/26-tilemaps.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/27-parallax.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/28-particles-2d.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/29-ui-elements.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/30-gamepad.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/31-first-3d-triangle.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/32-basiceffect.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/33-matrices.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/34-camera-3d.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/35-model-loading.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/36-model-texturing.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/37-multiple-lights.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/38-vertex-buffers.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/39-depth-buffer.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/40-primitive-types.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/41-math-vectors.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/42-matrix-ops.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/43-quaternions.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/44-bounding-volumes.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/45-content-manager.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/46-content-reader.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/47-game-component.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/48-timestep.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/49-touch-input.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/50-accelerometer.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/51-custom-vertex.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/52-custom-shaders.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/53-effect-parameter.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/54-alpha-test.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/55-dual-texture.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/56-environment-map.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/57-skinned-effect.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/58-normal-mapping.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/59-shadow-mapping.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/60-instancing.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/61-occlusion-query.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/62-mrt.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/63-stencil-buffer.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/64-cubemaps.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/65-msaa.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/66-bloom.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/67-deferred-rendering.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/68-terrain.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/69-water.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/70-procedural-geometry.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/71-memory-management.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/72-backend-selection.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/73-profiling.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/74-frustum-culling.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/75-lod.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/76-spatial-partitioning.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/77-async-loading.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/78-multithreading.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/79-debugging.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/80-cross-platform.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/81-emscripten.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/82-android.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/83-migrate-monogame.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/84-migrate-xna.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/85-vulkan-backend.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/86-[retired]-backend.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/87-custom-backend.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/88-device-layer.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/89-sharp-runtime.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/90-easy-gl.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/91-platformer.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/92-top-down-rpg.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/93-fps-game.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/94-puzzle-game.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/95-speedy-blupi.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/96-physics.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/97-networking.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/98-localization.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/tutorials/99-unit-testing.html | 200 | - | [pages: tut] |
| https://libcna.com/docs/vs-alternatives.html | 200 | - | [pages: d/vs] |
| https://libcna.com/documentation.html | 200 | - | [pages: doc] |
| https://libcna.com/features.html | 200 | - | [pages: feat] |
| https://libcna.com/network.html | 200 | - | [pages: net] |
| https://libcna.com/roadmap.html | 200 | - | [pages: road] |
| https://libcna.com/showcase.html | 200 | - | [pages: show] |
| https://libcna.com/tutorials.html | 200 | - | [pages: tut] |
| https://libcna.com/videos.html | 200 | - | [pages: vid] |
| https://libsdl.org/ | 200 | - | [pages: cont] |
| https://meshcraft.libcna.com/ | 200 | - | [pages: net] |
| https://metagl.libcna.com/ | 200 | - | [pages: net] |
| https://monogame.net/ | 200 | - | [pages: cont] |
| https://opensource.org/licenses/MS-PL | 200 | https://opensource.org/license/MS-PL | redirect [pages: idx] |
| https://plausible.io | 200 | - | [pages: idx] |
| https://plausible.io/js/plausible.js | 200 | - | [pages: idx] |
| https://samples.libcna.com/ | 200 | - | [pages: demos,idx,net] |
| https://schema.org | 200 | - | [pages: d/rel,idx,tut] |
| https://speedyblupi.com/SpeedyBlupi2013/ | 200 | - | [pages: demos] |
| https://wiki.libsdl.org/SDL3/ | 200 | https://wiki.libsdl.org/SDL3/FrontPage | redirect [pages: doc] |
| https://www.doxygen.nl/ | 200 | - | [pages: doc] |
| https://www.youtube.com/embed/tIMj20Ts2dg | 200 | - | [pages: vid] |
| https://www.youtube.com/embed/TScL1L-dbHE | 200 | - | [pages: vid] |
| https://www.youtube.com/embed/YzhewIB2X9c | 200 | - | [pages: vid] |
| https://www.youtube.com/@libcna | 200 | - | [pages: about,arch,cont,contr,d/rel,d/road,d/vs,demos,doc,feat,idx,net,road,show,tut,vid] |


---

## Speedy Blupi

### What exists (verified)

| Item | Fact |
|---|---|
| The original game | "Speedy Blupi"/"Speedy Eggbert" is an EPSITEC SA game series. The version ported to CNA is the **2013 Windows Phone edition** (a C#/XNA 4.0 game). `openeggbert/mobile-eggbert` README: "Mobile Eggbert is a modified version of Speedy Blupi, originally developed for Windows Phone and released in 2013. The project underwent: **decompiled by the ILSpy to the C# source code; migrated from XNA 4.0 to Monogame; migrated from C# to C++; migrated from Monogame to CNA**." `mobile-eggbert/LICENSE` is MIT, "Copyright (c) 2013 Daniel Roux, (c) 2024-2026 Robert Vokac". Counter-evidence for "open-source": `openeggbert/free-eggbert` README states "The original source code for Speedy Blupi / Speedy Eggbert has **not been publicly released**". So the C# came from decompilation, not from a published source tree. |
| The CNA port repo | `https://github.com/openeggbert/mobile-eggbert` (public, 200; **not** in the `libcna` org). Local HEAD `d43c6a143833aead71db655dcb28ab2a37565094`, 2026-08-21 17:28 +0200, branch `develop`, = remote `develop`. (Working tree has 6 uncommitted entries, ignored; committed content used.) GitHub description: "C++ port of Speedy Blupi (2013 Windows Phone XNA game) on the CNA framework - desktop, Android, and web (playable at speedyblupi.com)". ~31,986 lines under `src/` + `include/` (`git grep -c ''` at HEAD). CMake target `WindowsPhoneSpeedyBlupi`; links `CNA::Runtime`, `CNA::Devices`, `CNA::GamerServices` + selected renderer + sharp-runtime `IO.IsolatedStorage`; default consumes a sibling `../cna` checkout (`-DMOBILE_EGGBERT_CNA_ROOT`). Git history shows CNA in use by 2026-04-06/07 ("Upgraded to the latest version of CNA") and 2026-04-11 ("DDebug ... replaced by CNA:Logger::Debug"). |
| Other Speedy Blupi projects | `openeggbert/speedyblupi.com` (public; playable WebAssembly builds; HEAD `f9c5555450295d04252d28dd2e77de51dce29dcb`, 2026-07-19 10:53 +0200, = remote; deployed by GitHub Pages, `last-modified` 2026-07-19 08:56 GMT); `mobile-eggbert-libgdx` (Java/LibGDX port), `mobile-eggbert-legacy` (C#/MonoGame archive), `galaxy-eggbert` (3D remake on CNA + Easy3D), `free-eggbert` (Speedy Eggbert 2 reconstruction by decompilation, Ghidra/IDA), `planetblupi` (fork of EPSITEC's Planet Blupi source, which **is** published), `speedyblupi-data`, `BlupiEdit`, `tiled-blupi`. Only `mobile-eggbert` and `galaxy-eggbert` are CNA consumers. |
| CNA TARGET's own mentions | TARGET docs call it "an independently-developed XNA-style game, not a CNA example" (`docs/webgpu-renderer.md`, WEBGPU-130: on 2026-07-12 on Linux desktop it linked `cna_renderer_webgpu`, "reached its main menu automatically (~5 seconds after launch) with pixel-correct SpriteBatch rendering", and a simulated Play click started its mission-start cutscene) and "a real, complete third-party game" that builds against `-DCNA_GRAPHICS_RENDERER=HEADLESS` and "runs 20+ seconds with zero crashes" (`docs/headless-renderer.md`). Those records are dated 2026-07-12 and refer to a `../mobile-eggbert` checkout of that day (commit `dcdb648`), not to TARGET. TARGET has no test, CI job or build gate that builds mobile-eggbert. |

### Live "Play in Browser" target: `https://speedyblupi.com/SpeedyBlupi2013/`

* HTTP 200, no redirect; `content-type: text/html; charset=utf-8`; `content-length: 21953`; `server: GitHub.com` (Pages); `last-modified: Sun, 19 Jul 2026 08:56:02 GMT`.
* First 4 KB of body: `<!doctype html>`, `<title>Emscripten-Generated Code</title>` - it is the **stock Emscripten shell page**: emscripten.org logo, spinner + status "Downloading...", progress bar, checkboxes "Resize canvas" / "Lock/hide mouse pointer", a "Fullscreen" button (`Module.requestFullscreen`), `<canvas id="canvas">`, and a debug output `<textarea>`; script tail loads `<script async src="WindowsPhoneSpeedyBlupi.js">`. It is a WebAssembly/JS build. It is not Flash, not Unity, not a canvas-only JS game.
* Companion artifacts, all 200: `WindowsPhoneSpeedyBlupi.js` (417,076 B, `application/javascript`), `WindowsPhoneSpeedyBlupi.wasm` (16,456,055 B, `application/wasm`), `WindowsPhoneSpeedyBlupi.data` (25,137,146 B). Byte sizes are identical to the files in the local `speedyblupi.com` clone at HEAD `f9c555545`, so the clone's committed binary was inspected (`strings`, read-only) instead of downloading 41 MB.
* **What the wasm is built from** (strings in the committed binary): C++ symbols in namespace `WindowsPhoneSpeedyBlupi::` (`Game1`, `Decor`, `Pixmap`, `Sound`, `Worlds`, `InputPad`, `MyResource`, `GameData` ...); embedded assert/source paths `cna/include/Microsoft/Xna/Framework/{Rectangle,Color,Graphics/Texture2D,Graphics/GraphicsDevice,Input/Touch/...}.hpp`, `cna/include/Microsoft/Devices/Sensors/...`, `cna/include/CNA/...`, `cna/src/Microsoft/Xna/Framework/...`, `cna/third_party/SDL`, `SDL_image`, `SDL_mixer`, `sharp-runtime/include/System/...`, `sharp-runtime/include/SharpRuntime/...`; classes `CNA::Internal::Backends::SdlRenderer::SdlGraphicsBackend` / `SdlSpriteBatchBackend` / `SdlRenderer::ThrowNo3D()`; `.cna_isolated_storage` + an IDBFS sync snippet (save game in IndexedDB); Emscripten `clang version 23.0.0git`; SDL string `SDL-3.5.0-HEAD-HASH-NOTFOUND`; SDL's own `opengles2` render driver + Emscripten video driver. There is **no** reference to XNA-runtime/MonoGame/FNA/Unity. Verdict: it is a genuine **CNA + sharp-runtime + SDL3 WebAssembly build of the C++ Speedy Blupi 2013 port**, using CNA's **SDL_RENDERER backend** (2D-only), not EasyGL/WebGL 2 as the surrounding demos.html copy implies.
* **Which CNA?** An early, pre-modularization layout (`cna/include/...`, `cna/src/...` rather than `modules/*`), file dates 2026-05-17, i.e. built about 3 months before alpha.1 (2026-08-20) and 4 months before TARGET. It is not an alpha.1 or TARGET build and nothing in the artifact ties it to a CNA commit. `speedyblupi.com` also holds three "experimental" variants (`SpeedyBlupi201360FPS` files dated 2026-05-17 01:40 with a 16,279,019 B wasm, plus `...120FPS`, `...144FPS`) and an obsolete C#/KNI Blazor build (`SpeedyBlupi2013CSharp`). `speedyblupi.com/index.html` describes the main one as "A fully functional web port of the Windows Phone version of Speedy Blupi 2013. The game is playable, including sound. Save-state persistence is implemented ... modern C++ version with persistence (20 FPS)".
* **Not verified by this agent:** actual in-browser execution (no browser session was used; a 41 MB load was not attempted). The evidence is static (artifact identity, headers, the project's own description).

### Desktop / Web / Android status against evidence

| Claim currently on demos.html / showcase.html | Evidence | Verdict |
|---|---|---|
| "Speedy Blupi - Desktop ... Currently in development" | mobile-eggbert README documents Linux native (`SDL_RENDERER`), Windows native + MinGW cross build, D3D11/D3D12 builds runnable under Wine/Proton; YouTube (2026-04-25) shows it running on Linux; TARGET docs record 2026-07-12 Linux runs (WEBGPU, HEADLESS). `TODO.md` at HEAD lists open issues: accelerometer shown without device, "Sound - to check", "transparency", "Fullscreen is not working correctly", "Web version: Sound is a little bit delayed", audio pitch/missing-file reports. No prebuilt binaries or GitHub Releases (releases API = `[]`). | A working desktop port exists and is buildable from source; "completed" is not supported. |
| "Speedy Blupi - Web: Browser-playable WebAssembly build of the Speedy Blupi CNA port ... web port is in progress" + "Play in Browser" | Live build exists and is a CNA wasm build (above). "In progress" contradicts the working link. | A CNA WebAssembly build exists (early CNA, SDL_RENDERER). |
| "Speedy Blupi - Android: Android APK of the Speedy Blupi CNA port. APK download coming soon" (TODO-link) and "Speedy Blupi - Android Port ... running on CNA ... milestone demo" (second TODO-link in the Android section) | mobile-eggbert has an Android Gradle/NDK project (`android/`, `ANDROID.md`, package `org.openeggbert.speedyblupi`, NDK 28.2, API 35), commits "Support for releasing apk file was added", "fix: stabilize Android tablet gameplay", "fix: preload SDL dependencies on Android 4". **No APK is published anywhere**: `mobile-eggbert` has zero GitHub Releases; no APK link on speedyblupi.com or mobileeggbert.openeggbert.com (that site's build page documents `assembleDebug` and `adb install` only). | An Android build project exists; **no downloadable APK exists**. Do not claim an Android CNA APK. |
| showcase: "Speedy Blupi is a classic open-source action game ... The port did not require changes to the game's core logic - only the platform-facing layer was adapted." | The port is a decompile -> XNA-to-MonoGame -> C#-to-C++ -> MonoGame-to-CNA translation with ~32k lines of C++ rewritten class by class ("Rewriting the class Decor to C++ #1..#7" etc. in history). "Open source" is contradicted by free-eggbert's statement and unsupported except for the MIT LICENSE file in mobile-eggbert. | Both sentences are unsupported. |
| showcase: "Linux x86_64 - EasyGL renderer" | mobile-eggbert README default for Linux is `-DCNA_GRAPHICS_RENDERER=SDL_RENDERER`; the live web build uses the SdlRenderer backend; CNA's default on Linux is `OPENGLES3` (EasyGL) only if the consumer does not override. | Not established as EasyGL. |
| showcase: "Android - SDL_RENDERER/NDK project path ... WebAssembly - Emscripten/WebGL 2 build in progress" | Android part is close to the evidence; the web part understates it (a live build exists). | Update web line. |

### Truthful wording options

demos.html, section "Speedy Blupi - Port / Demo" (intro): *"Speedy Blupi (the 2013 Windows Phone edition) has been decompiled, translated from C# to C++ and ported onto CNA by the OpenEggbert project (repository `openeggbert/mobile-eggbert`, MIT-licensed). It is an independent consumer of CNA, not part of CNA or its test suite; every result below is tied to the CNA revision it was built with, not to alpha.1 or the current development tree."*

* Web: *"Playable in the browser at speedyblupi.com (WebAssembly via Emscripten, built in May 2026 with an early CNA revision and CNA's SDL_Renderer backend; not rebuilt against alpha.1 or newer)."* Button "Play in Browser" may stay.
* Desktop: *"Builds and runs on Linux (SDL_Renderer); Windows builds are documented (native, MinGW cross-build, D3D11/D3D12 via Wine/Proton). No prebuilt binaries are published; known open issues are listed in the repository."*
* Android: *"An Android (Gradle/NDK) project exists in the repository; no APK has been published."* Remove both "APK coming soon" TODO-links or replace them with this sentence.

showcase.html Real-World Validation: replace "classic open-source action game ... did not require changes to the game's core logic" by the description above (decompiled Windows Phone XNA game, translated to C++, then ported onto CNA); keep "what it exercises" (SpriteBatch, input incl. touch/accelerometer, SoundEffect/MediaPlayer via SDL_mixer, ContentManager with loose PNG/WAV, IsolatedStorage saves) as evidence that "real-world XNA-style game code runs on CNA at the revision it was ported to", not as an alpha.1 claim.

videos.html card "Speedy Blupi on CNA" (`TScL1L-dbHE`): the video is titled **"Speedy Blupi for Windows Phone was ported to C++"**, on the *Open Eggbert* channel, 2026-04-25, 1:41, Linux only at the time; it never says "CNA". Options: retitle to the real title and caption *"Speedy Blupi for Windows Phone rewritten from C# to C++ (recorded 2026-04-25 on Linux; the port uses CNA - see mobile-eggbert). Project video from the OpenEggbert channel."*; or drop the card. Similar re-captioning for `YzhewIB2X9c` ("CNA now partially supports 3D", 2026-05-03, 48 s) and `tIMj20Ts2dg` ("CNA now supports 2D", 2026-04-11, 13 s). Consider replacing all three by the five 2026-09 videos on `@libcna` (car simulator x2, living room simulator, Wolf CNA, CNA Street), which show current projects and are on the channel the nav links to.

docs/tutorials/95-speedy-blupi.html: the page already says it is "a worked walkthrough ... not an audited case study". Remaining factual problems: "Speedy Blupi is an open-source action platformer ... The original Speedy Blupi C# MonoGame codebase" - the C# was decompiled from the 2013 XNA 4.0 Windows Phone release and passed through MonoGame only as an intermediate step; the snippets (`Load<Texture2D>("Blupi/blupi")`, `SoundEffect music("assets/music/theme.ogg")`, `List<T>`->`std::vector`) are generic patterns, not code from mobile-eggbert (whose real code uses `getContentProperty().Load<Texture2D>(iconPrefix + "text")` over loose PNG files under `Content/`, `System::IO::IsolatedStorage` for saves, `Microsoft::Devices::Sensors::Accelerometer`). Either retitle ("Porting a 2D XNA/MonoGame game to CNA: patterns") or rewrite the first two sections from the mobile-eggbert README facts above.

---

## cna-samples (pinned)

Repository: `libcna/cna-samples`, branch `develop`, HEAD **`4da98a0fc24520d8ff9f9b462f8f78d47fc23fbe`**, 2026-09-20 21:10:12 +0200, "docs(SAMPLES-INFRA-003): refresh sequential review handoff"; = remote `develop`; working tree clean. (GitHub default branch is `develop`; a `main` branch also exists, at `f47832fea`.) README build recipe uses sibling `../cna` and `../sharp-runtime` on `next`. Repo description on GitHub: "C++ ports of the official Microsoft XNA Game Studio 4.0 samples, running on the CNA framework. Web demos coming soon." README still links `github.com/openeggbert/cna` (redirects to libcna/cna).

**All counts below are tied to cna-samples `4da98a0fc`, not to CNA TARGET.** They cannot be tied to TARGET without building; the plan itself says the dependency is CNA `next`, and TARGET = tip of `next` on 2026-09-24 (4 days after this HEAD), so relation to TARGET is "same branch, about 4 days newer", unverified.

Counting methods (all reproducible with `git` against the pinned commit):

| Method | Command | Result |
|---|---|---|
| Rows in the repo's own authoritative inventory (`plan.md`: "one row per physical upstream directory") | `git show HEAD:plan.md \| grep -c '^\| SAMPLE-'` | **153** upstream directories (SAMPLE-001..153) |
| Rows marked complete | `git show HEAD:plan.md \| grep -c '\| ✅ \|$'` (plan says "recount from the table itself") | **87** |
| Owner-decision pending | `grep -c '\| 🛑 \|$'` | 49 |
| Cancelled by owner (evidence-backed non-ports) | ⛔ | 14 (SAMPLE-015 TicTacToe, 064, 075, 085-090, 093-097) |
| In progress | 🛠 | 2 (SAMPLE-107 TiltPerspective, SAMPLE-148 TiledSprites: native port + WEBGL2 bundle done, real-browser gate pending) |
| Separate plan | ↗ | 1 (SAMPLE-152 Racing Game, governed by `plan_racing.md`, deliberately last) |
| Sum | 87+49+14+2+1 | 153 (matches the plan's "Progress at a glance") |
| Directories under `samples/` | `git ls-tree -d HEAD samples/ \| wc -l` | 162 |
| ... of which contain a `CMakeLists.txt` (a build target exists) | `git ls-tree -r HEAD --name-only \| grep -E '^samples/[^/]+/CMakeLists.txt$' \| wc -l` | **101** (includes `RacingGame`, `RacingGameHarness`, 8 CatapultWarsTraining* stages, `StockEffects` CLI-only) |
| ... without `CMakeLists.txt` (placeholder/documentation-only dirs) | difference | 61 |
| Published web builds | `samples.libcna.com` HEAD `736b8aa3199e07cb8ce4d174c7290d6db2c8c4aa` (2026-09-20 20:53 +0200, "feat(SAMPLE-041): publish Lens Flare with known WebGL limitation"; = remote `main`) | **40** `<Sample>/<Sample>_cna_samples.html` bundles; live gallery says "Samples 1-12 of 39" on page 1 but "Samples 37-40 of 40" on page 4 (internal inconsistency); 44/44 pages return 200 |

There is no machine-readable status file (no JSON/CSV manifest); the only status source is the plan table (the plan's own `SAMPLES-INFRA-004` "inventory validator" is not yet built).

The 87 complete (✅) rows are SAMPLE-001..014, 016..063, 065..074, 076..084, 091, 092, 098, 099, 102 and 104 (14+48+10+9+6; the extraction is `awk` over the `| SAMPLE-nnn |` rows of `plan.md`). SAMPLE-004 StockEffects is complete as a Content-Pipeline-only CLI by owner decision, and SAMPLE-041 LensFlare only under an owner-approved documented visual limitation (occlusion-query count gap on ES3/WebGL2). In the plan's `Existing` column (state on 2026-08-22) the 87 are: 73 `port`, 9 `placeholder`, 3 `absent` (i.e. newly ported since), and 2 recorded otherwise (StockEffects; ShipGame).

**Comparison with the website's claim "63 of 86 in-scope samples are ported and build; 23 are placeholders/do not build because of `.fx`":**

* The denominator 86 does not exist in the repo any more: the plan re-inventoried all upstream directories at **153** ("Historical labels such as Done, Placeholder, Ignored ... are evidence to re-check, not current conclusions").
* The numerator is stale: 87 rows are complete under a stricter definition than "builds" (native OPENGLES3 run + real-browser WEBGL2 run + zero-workaround audit).
* **The ".fx blocks 23 samples" statement is false at this HEAD.** The shader-driven samples named on the site are all complete: BloomSample (SAMPLE-031), DistortionSample (032), NormalMappingSample (034), PerPixelLightingSample (035), ShadowMappingSample (038), SkinningSample (054, was "placeholder"), CPUSkinningSample (056), RimLighting (037), NonPhotoRealistic (033). The repo's mechanism (SAMPLES-DEC-001, SAMPLE-003/006): official XNA 4.0 Effect XNBs produced by XNA's own `BuildContent` (under Wine or an offline Win7 VM) load through CNA's compiled-effect path on OPENGLES3/WEBGL2. What is still true is the narrower statement that CNA does not compile HLSL `.fx` **source**: site tutorial 128 (written for alpha.1) says alpha.1 "accepts XNA/FNA D3D9 Effect Framework binary bytecode ... does not compile HLSL .fx source and does not accept DXBC or MonoGame MGFX", gated by `-DCNA_EASYGL_COMPILED_EFFECTS=ON` (and equivalents for SDL_GPU/Vulkan). So the site's own sentence "CNA cannot compile HLSL bytecode" also conflicts with tutorial 128 (compiled bytecode is the supported path). SAMPLES-DEC-001/-002 record custom `.fx`/content-pipeline extensibility as an owner-decision item.
* What blocks the remaining rows is not `.fx`: 49 rows wait on owner decisions (WP7/Silverlight/WinForms apps, Avatar packs and rigs, XNA 2.0 archive samples, VB duplicates, networking with no web transport, push notifications, tools), 14 are cancelled non-ports.
* Four names that demos.html lists among built samples are **not** complete at this HEAD: `TicTacToe` (SAMPLE-015, ⛔ cancelled by owner decision), `PeerToPeer` (SAMPLE-103, 🛑 pending), `NetworkPrediction` (SAMPLE-100, 🛑 pending) and `TiltPerspective` (SAMPLE-107, 🛠 browser gate pending). Note `NetRumble` (SAMPLE-062) is complete natively only: the owner decided no web port will be produced.

Suggested factual sentence (pinned): *"As of cna-samples `4da98a0` (2026-09-20) the repository inventories 153 official XNA Game Studio 4.0 sample directories; 87 are marked complete (native and in-browser verification), 40 are published playable at samples.libcna.com, 49 await owner decisions, 14 are documented non-ports, and Racing Game is tracked separately. Results are for CNA `next` at that date, not for alpha.1."* Or, more robustly, drop all counts and link the gallery and `plan.md`.

---

## Language bindings (pinned)

CNA TARGET publishes **C ABI 0.29.0** (BASE alpha.1: 0.7.0). Every binding below was last committed **before** ABI 0.28.0/0.29.0 existed (2026-09-17) and declares/qualifies **ABI 0.21.0** (cna-ruby and its template additionally 0.7.0). What CNA's `ABI_VERSIONING.md` records after 0.21.0: 0.22.0 (restored 10 renderer identities, ceiling 49 -> 50), 0.23.0 (+1 route), 0.24.0/0.26.0 (+1 renderer-feature identity each), 0.25.0 (+1 shader dialect), 0.27.0 (+1 renderer identity) are described as additive for existing consumers; **0.28.0 retired 25 renderer identities** and **0.29.0 removed `cna_sprite_batch_draw_mesh_ext`/`CNA_SpriteMeshEXT`** are the two incompatible steps. Additive does not mean "loads": bindings that require an exact minor refuse every later minor anyway. All bindings and templates read their native library from a user-supplied path (`CNA_NATIVE_LIBRARY`, sometimes `CNA_NATIVE_DIR`/`CNA_ROOT`); none bundles CNA, none is published to a package registry (cna-cs README: "NuGet/RID packages: none published"; cna-go-template: "CNA-Go is not published yet").

| Binding | HEAD (branch) | Public? | Own status statement | Expected ABI (authoritative source in code) vs README | Admission rule at load | Finds native lib via | CI evidence |
|---|---|---|---|---|---|---|---|
| **cna-cs** (CNA.NET, C#) | `e223909986a705d0026908155f59388c100cbda3`, 2026-09-03 (develop) = remote | yes | "exact public metadata for the selected XNA 4.0 Windows runtime profile; **not yet behaviorally complete or release-ready**" (257/257 types) | code: `eng/cna-native-abi-policy.json` `consumerAbi` **0.21.0**, `acceptedVersions` = [0.21.0]; README text still says 0.20.0 (stale) | **exact reviewed matrix entry** ("never accepted as a same-major range"); all imports + 3 runtime canaries must pass. 0.29.0 would be refused. | `CNA_NATIVE_LIBRARY` / `CNA_NATIVE_DIR`, then package-native lookup; fail-fast | `release-qualification` workflow pins CNA `599d14e54e07` (2026-08-31, ABI 0.21.0 on `next`). GitHub run status: last 3 runs (2026-09-02/03) **failure** (failing jobs include template-development, behavior-pure-corpus, package-consumer-managed, leak-only-verifier) |
| **cna-java** | `6661173c556bacd1ba3e636fa92d2e4ec330323d`, 2026-09-01 (develop) = remote | yes | "early, measured Java 17 projection ... JNI adapter"; "The complete XNA 4.0 runtime superset is structurally at zero diagnostics ... does not mean every runtime capability is present" | code: `COMPILED_ABI_VERSION = encodeVersion(0, 21, 0)`; README says 0.20.0 (stale) | major **and minor must equal** compiled ("requires ABI 0.21.x exactly") -> 0.29.0 refused with `UnsatisfiedLinkError` | `CNA_NATIVE_LIBRARY` env / `cna.native.library` system property | none (no `.github/`) |
| **cna-ts** | `14af178eb8c7714a32d9f9c43ec95a80720250d2`, 2026-09-02 (develop) = remote | yes | "complete XNA 4.0 runtime surface is projected and verified"; opt-in Node-API bridge + WebAssembly backend; "No native binary and no CNA library is bundled" | code: `CNA_ABI_MINOR = 21` (`src/internal/abi.ts`); README says 0.20.0 (stale) | `isSupportedAbiVersion`: under 0.x **minor must match exactly** -> 0.29.0 refused | `CNA_NATIVE_LIBRARY` absolute path | `Qualification` workflow: last 3 runs (2026-09-02) **success**; it checks out CNA headers at pinned commit `89024e0d4eef` (CNA `next` of 2026-08-31, ABI 0.21), so success says nothing about TARGET |
| **cna-python** | `f085bbb54c57bea553cff9b48898c11f3c49a77d`, 2026-09-02 (develop) = remote | yes | "**pre-alpha**, measured Python projection ... real exact-ABI runtime binding against one qualified CNA generation" | code: `SUPPORTED_ABI_MINOR = 21`; README "select a CNA `0.21.x` C ABI" (consistent) | different minor rejected -> 0.29.0 refused | `CNA_NATIVE_LIBRARY` (absolute) / `CNA_NATIVE_DIR` | none |
| **cna-rust** | `ef25fbb1ff54f0792006ae969a5027311139e10f`, 2026-09-02 (develop) = remote | yes | "early, measurable safe Rust projection ... selected XNA 4.0 Windows runtime Rust projection is structurally complete" | code: `cna-sys` `CNA_ABI_VERSION` = 0.21.0 "the exact canonical ABI version these declarations were reviewed against"; README "CNA ABI 0.21" | runtime enforcement not established by my grep. It **declares `cna_sprite_batch_draw_mesh_ext`** (7 references in `cna-sys/src/{lib,linked}.rs`, `cna/src/native/api.rs`): a direct-link build against a 0.29.0 library cannot resolve it. | `CNA_NATIVE_LIBRARY` / `CNA_NATIVE_DIR` / `CNA_ROOT` in `build.rs` | none |
| **cna-swift** | `4965c69c2088c00faf4b9a491e7701f8923d403f`, 2026-09-09 (develop) = remote | yes | "real Swift projection ... all 257 retained types strict-complete; runtime capabilities CNA cannot provide remain explicit refusals" | code: `minimumMinor = 21` ("a later minor is admitted by the published rule"); qualified only against 0.21.0 HEADLESS on Linux x86-64 | **admits minor >= 21** nominally, so it would load 0.29.0; nothing shows it was ever qualified past 0.21.0 | `CNA_NATIVE_LIBRARY` (absolute) | none (`.githooks` only); no `LICENSE` file at HEAD |
| **cna-go** | `510a84da2ca799d4a15c8319f8ccf9e43df7a32a`, 2026-09-05 (main) | **no** (github.com/libcna/cna-go = 404) | "early, measured binding foundation ... far from full XNA compatibility" | ABI 0.21.0 (README, `abi_version 5376` = 0x1500 = 0.21.0) | `cna_go_abi_admits`: major 0 and **minor >= 21** | `CNA_NATIVE_LIBRARY` absolute path, cgo `dlopen` | none |
| **cna-ruby** | `e7e0750de409d790a23efec798e560323cc3b96d`, 2026-09-04 (main) | **no** (404) | "implementing a formally measured Ruby projection ... intentionally incomplete" (strict scoreboard targets 149 of 257 types) | `ADMITTED_ABI_VERSIONS` = {0.7.0, 0.21.0} | exact set; 0.29.0 refused | `CNA_NATIVE_LIBRARY` | none; no `LICENSE` file at HEAD |

Templates (all read the same `CNA_NATIVE_LIBRARY`): `cna-c-template` `024c1f7aad2092c9ec8dc4862bd201c43a4ae3cc` (2026-08-22, public, CI "Repository checks" success 2026-08-22, `dependencies.lock` pins CNA `6bba5562d` = 2026-08-22, ABI 0.8.0); `cna-cs-template` `35e9700cb` (2026-08-31, public); `cna-java-template` local `11b8392e8` (2026-08-31) but public `develop` is `2a4778a30` (newer, differs); `cna-ts-template` `8a806d854` (2026-08-31); `cna-python-template` `fe84cd7c4` (2026-09-02, "external CNA `0.21.x` C ABI library"); `cna-rust-template` `416642b93` ("2026-08-31 headless test used CNA ABI 0.21.0"); `cna-swift-template` `402cbd09d` (2026-09-07, 0.21.0 HEADLESS); `cna-go-template` `f22f54f7e` (2026-09-01, not public); `cna-ruby-template` `42ae209b8` (2026-08-24, not public; qualified against ABI **0.7.0**). Support repos: `cna-cs-samples` `69ddcc107` (2026-09-02, public: the original C# XNA samples running through CNA.NET); `cna-multi-language-3d-demo` `29937cb2b` (2026-09-12, public): only the C++ reference is DONE, all ten other languages are "EMPTY" reserved directories.

**Compatibility verdict (what the website may truthfully state):**

* No binding is qualified against CNA TARGET's C ABI 0.29.0, and none against alpha.1's 0.7.0 except cna-ruby (which admits 0.7.0 and whose template was run against 0.7.0). Each is pinned to the 0.21.0 generation; CNA's own policy says an `0.x` minor may be an incompatible generation. Five of eight (cs, java, ts, python, ruby) refuse 0.29.0 by their exact-version rule; two (go, swift) accept any minor >= 21 nominally but have evidence only for 0.21.0, so acceptance by the loader is not a compatibility statement; cna-rust declares 0.21.0 and still declares `cna_sprite_batch_draw_mesh_ext`, which 0.29.0 no longer exports (the other seven bindings do not name that symbol in source; retired renderer constants: only cna-rust has a source file naming one of the retired/ceiling constants, `crates/cna/src/native/abi.rs`).
* "Latest binding + latest CNA" must not be described as compatible. Safe wording: *"Language bindings are separate, pre-alpha projects. Each targets one specific experimental C ABI generation (currently 0.21.x); CNA at alpha.1 exports ABI 0.7.0 and CNA's development branch exports 0.29.0, so check the binding's ABI policy before pairing versions."*
* Publicly visible today: C#, Java, TypeScript, Python, Rust, Swift (six repos in the `libcna` org) - matches index.html's list. Go and Ruby exist only as local repositories (404 on GitHub); they should not be advertised.
* Status words that are safe: cna-python "pre-alpha"; cna-cs "not yet behaviorally complete or release-ready"; cna-java/cna-rust "early"; cna-go "early, measured foundation". README claims of "structurally complete/strict 257/257 types" are metadata-shape claims (type/member signature parity with XNA assemblies), not behavior or compatibility claims, and should not be quoted as "XNA-compatible".
* Licence: cs/java/ts/python/rust/go carry Ms-PL; swift and ruby have no LICENSE file at HEAD.

The index.html sentence on CNA.NET ("The exact CNA alpha.1 C library cannot be built without correcting its missing [retired] C identity") is a claim about alpha.1 (0.7.0) vs a binding at 0.20/0.21; not re-verified here. Note [retired] was retired entirely in ABI 0.28.0.

---

## Ecosystem projects (pinned)

`GH` = public on GitHub (curl `https://github.com/<org>/<name>`: 200 = yes, 404 = no; nothing private can be confirmed from a 404 alone, a 404 means "not publicly visible"). "Builds vs CNA" is only what dependency files/CMake state; nothing was built. "Web demo" = present in `demos.libcna.com` HEAD `f6b37c525f314ff5968f6a6005d9bdac5ebc21fc` (2026-09-22 18:41 +0200, "Add CNA Street demo"; = remote `main`) or on `samples.libcna.com`/`speedyblupi.com`.

| Project | Pinned HEAD (branch) | GH | What it is (from its own README/CMake) | Builds vs CNA? evidence | Web demo | Website claim -> fresh fact |
|---|---|---|---|---|---|---|
| **cna-extended** | `5775ecc97843` (2026-08-22) (develop); public default branch is `master` = `d0172ced3` (2026-07-13, "Early bootstrap", 20-task Phase 1) | yes (`libcna/cna-extended`) | C++23 port of MonoGame.Extended on CNA + sharp-runtime; 9 module phases plus a non-upstream `World3DEXT` 3D layer. Default build is headers-only, `-DCNA_EXTENDED_LINK_CNA=ON` links CNA. | Sibling `../cnanext`/`../cna`; no `dependencies.lock` | none | "~65,000 lines, largest project in the ecosystem, 2,363 tests" (index) and "101,461 lines" (showcase) disagree with each other. Measured at `5775ecc97` (`git grep -c ''` over `*.cpp *.hpp *.h *.inl *.cc *.cxx` excluding third_party/vendor/external): **102,360 lines in 890 files**. Not the largest: cna-lab 207,977, cna-studio 178,418, cna-editor 125,580 (in cna-lab), house-simulator 123,135 (not public). Test count: the repo's own docs disagree (README "2371/2371 passing", NEXT.md "2363/2365" in one section and "2369/2369" in another; 2,214 `TEST(` macros); the number moves -> **remove test count and the "largest" superlative**. NB: the branch the website links (`master`) shows the July 13 bootstrap README, not this state; `develop` is the real one. |
| **cna-craft** | in `cna-lab` subtree `49e3cd5b0447` (2026-09-19) | no standalone repo (404); source at `libcna/cna-lab/tree/develop/cna-craft` (200) | C++ port of fogleman/Craft (MIT) onto CNA | CMake against sibling CNA (subtree, no lock) | yes: `demos.libcna.com/cna-craft/CnaCraft.html` (200) | showcase "13,766-line port" -> measured 13,799 C/C++ lines in 64 files (cna-lab HEAD); fragile -> drop the count. Fix the link. |
| **cna-editor** | in `cna-lab` | no standalone repo; `.../cna-lab/tree/develop/cna-editor` (200) | Editor, asset pipeline and tooling for CNA; "it edits, it plays, and it draws the game" via CNA's public API; glTF import; 3D viewport with gizmos (125,580 C++ lines, 185 files) | builds against "a real CNA checkout" | none | index link is dead -> point at the cna-lab subtree, or omit. Note `cna-studio` (below) is the newer, separate tool. |
| **cna-lab** | `49e3cd5b0447` (2026-09-19) | yes | Git-subtree collection of experimental CNA repos: black-pine, cna-craft, cna-editor, copper-boots, explore-2d, iron-gang, mesh-world, people-cna, tamagotchi-cna, wolf-cna | each subtree its own CMake | 7 of the 14 demos.libcna.com demos match cna-lab subtree names (black-pine, cna-craft, iron-gang, copper-boots [= `mario-cna/copper-boots.html`], people-cna, tamagotchi-cna, wolf-cna); this is name matching, not proven build provenance | not on the site; candidate card |
| **cna-examples** | `ea33c9a29eb4` (2026-09-13) (develop) = remote | yes | In-app catalog of live CNA demonstrations: Home -> Area -> Category -> Demo; verified on OPENGLES3 and SDL_RENDERER | sibling CNA; no lock file | yes: `demos.libcna.com/cna-examples/cna_examples.html` | "60 demos ... Input (50) and Audio (10) ... Devices, Net, Media and both Graphics areas ... still empty, and there are no tests yet" (index; demos.html "60 demos are registered today") -> at HEAD the repo registers **249** demo screens (`grep -c 'MakeDemo<' src/Navigation/AreaCatalog.hpp` = 249), 13 areas / 79 categories, all areas populated; it has a catalog checker and headless sweep tools (`tools/check_catalog.py`, `tools/sweep.sh`), README says 249/249 render on each of OPENGLES3 and SDL_RENDERER. Recommend removing the count or restating with the pin. |
| **cna-template** | local `c3b804bfa724` (2026-08-22) (branch `next`); public default `develop` = `4d0a2c8a790a2606d0e9a330fe7439f6b691722f` (2026-08-11) | yes | Starter project (HelloGame), presets per renderer, Android gradle project, MinGW cross-build, `dependencies.lock` | `dependencies.lock` pins CNA `7a64362efef4` (2026-08-11), sharp-runtime `f827a6c5`, easy-gl `0b46d35c`, meta-gl `571d3a62`, free-direct `934f72ff` -- all older than TARGET. GitHub Actions `CI` on `develop`: **failure** in the last 3 weekly runs (2026-09-07/14/21). At local `next` (`c3b804bfa`) 7 of 33 configure presets name renderers retired in ABI 0.28.0 ([retired], sokol, [retired], web-[retired]). | none | "140 lines ... 9 CMake presets" -> public `develop`: 31 configure / 27 build / 22 test presets; `game/` = 3 files (HelloGame.cpp 16,067 B, HelloGame.hpp, Program.cpp; 448 lines at `next`). Both numbers are stale; remove. Do not say it builds against TARGET. |
| **cna-c-template** | `024c1f7aad20` (2026-08-22) (develop) = remote | yes | Starter for CNA's C binding: game loop, texture loading, 2D and capability-gated 3D, Android glue, smoke test | `dependencies.lock` pins CNA `6bba5562d` (2026-08-22, C ABI 0.8.0); CI "Repository checks" success 2026-08-22 | none | not on site; only relevant if C ABI docs recommend it |
| **cna-gltf-viewer** | local `12a10a1b837d` (2026-08-23) (develop); public default `main` = `63d9f39ed` ("chore: initialize project", 2026-07-28) | yes | Desktop glTF 2.0 viewer through CNA (`cna_tool_gltf_to_cnj` path or `--direct` runtime loader) | sibling CNA; no lock | none | the public default branch is an empty "initialize project" commit; the real code is on `develop`. Link should specify `tree/develop`. 2,281 C++ lines (7 files). |
| **mesh-craft** | `c8d1783b5867` (2026-08-22) (develop) = remote; 3 uncommitted entries | yes | C++23 3D scene editor for `.mc3.xml` (primitives, CSG, PBR materials, keyframe animation, glTF/GLB/MCB export); graphical editor has a CNA path, CLI converters do not need CNA | optional CNA | yes: `demos.libcna.com/mesh-craft/MeshCraft.html`; also `meshcraft.libcna.com` (200) | 80,763 C++ lines in 299 files (pinned); no site number to fix |
| **easy-3d** | `e2d1cfa277a3` (2026-07-11) (develop) | **`openeggbert/easy-3d`** yes; `libcna/easy-3d` no | Small C++23 companion helper library next to CNA: cameras, texture atlas, billboard/cube batching, debug drawing | optional `EASY3D_LINK_CNA` (default OFF) builds CNA from `../cna` | none | fix index link to `openeggbert/easy-3d` |
| **galaxy-eggbert** | `28840fbfe398` (2026-08-21) (develop); 1 uncommitted entry | yes (`openeggbert`) | Faithful 3D remake of mobile-eggbert/Speedy Blupi; sole game target `GalaxyEggbertCNA` built directly on CNA with Easy3D; in-game world editor (`CURRENT.md`, last verified 2026-07-25) | `add_subdirectory(CNA_HOME=../cna)`; CI builds the CNA target from a sibling-checkout layout; Linux native + Vulkan native maintained; MinGW build confirmed but `SDL_RENDERER` is 2D-only so Wine launch stops at `CreateVertexBuffer`; Web/Emscripten verified manually, not in CI or release | yes: `speedyblupi.com/GalaxyEggbert/` (200) | linked card fine; do not claim Windows |
| **mobile-eggbert** | `d43c6a143833` (2026-08-21) (develop) = remote; 6 uncommitted entries | yes (`openeggbert`) | see Speedy Blupi section | sibling CNA; commits follow "CNA platform-API rename" up to 2026-08-21 (one day after alpha.1), README says 46 renderer identities (TARGET: 25) | yes: `speedyblupi.com/SpeedyBlupi2013/` | see above |
| **planetblupi** | `8e42e1cfd5ba` (2026-07-18) (feature/free_direct) | yes (`openeggbert`) | EPSITEC's original 1997 Planet Blupi source (README: "The original Windows/DirectX codebase has been made buildable and portable across Linux, and Web (Emscripten)"); GitHub calls it a fork used as a reference for the OpenEggbert preservation projects; playable on Linux, web build lacks MIDI music and AVI movies | not a CNA consumer; "indirect reference" only via CNA `FREEDIRECT` renderer | yes: `speedyblupi.com/PlanetBlupi/` | matches index wording ("indirect CNA references") |
| **free-eggbert** | `7ea63d18a1e9` (2026-07-10) (develop); 3 uncommitted | yes | Reconstruction of Speedy Eggbert 2 from decompiled/reverse-engineered code (Ghidra/IDA); "gameplay partially functional ... defective" | not a CNA consumer | `speedyblupi.com/SpeedyEggbert2/` (partially functional) | index wording OK ("work-in-progress reconstruction") |
| **free-direct** / **free-api** | `934f72ff0c52` (2026-07-18) / `53d7a3124110` (2026-07-18) (develop) | yes | free-direct: narrow [retired] (2D) subset on SDL3; free-api: minimal ~1998 Win32 API layer; MIT, C++20 | consumed by CNA's `FREEDIRECT` renderer (identity still present in TARGET's `graphics.h`) | via planetblupi/free-eggbert web builds | OK |
| **xna4-spec** | `fedc17aa48eb` (2026-09-13) (develop) = remote | yes | Machine-readable XML specification of the XNA 4.0 API converted from Microsoft docs, for auditing reimplementations | not a CNA consumer (spec/data) | none | OK |
| **sharp-runtime** | `41b918c97ed4` (2026-09-20) (`next`); public default `main` `54578590b` | yes | C++23 implementation of a practical subset of .NET `System.*`; "41 independently selectable CMake components ... 17,840 tests across 38 test executables - all passed, verified Linux baseline 2026-08-22" (README's own moving number) | required by CNA; TARGET has no pin file for it | none | site says "Every alpha.1 build requires this sibling checkout" - true; for TARGET clone branch `next`, not default `main`. Do not restate its test count (README date 2026-08-22, HEAD 2026-09-20). |
| **easy-gl** | `deda7a426c3c` (2026-08-22) (develop) = remote | yes | Toolkit-independent C++20 RAII wrapper over OpenGL/GLES; "small working vertical slice" | used by CNA's five EasyGL renderer identities | docs `easygl.libcna.com` (200) | OK |
| **meta-gl** | `20c8b2dc5bb8` (2026-09-03) (develop) = remote | yes | Low-level type-safe C++23 wrapper for OpenGL ES 2.0-3.2 and desktop GL 3.3+; foundation of easy-gl | same | docs `metagl.libcna.com` (200) | OK |
| **openeggbert** (ecosystem map) | `a83903dca588` (2026-08-12) (main) | yes | Umbrella README of the OpenEggbert ecosystem; its own summary "~560.5k lines of C++" | n/a | n/a | site already says its summaries are not the source of truth; keep, do not quote its numbers |
| **cna-samples** | see section above | yes | ports of XNA GS 4.0 samples | pins CNA `next` sibling | 40 on samples.libcna.com | replace 63/86 |
| **cna-city** | `267b79b9b8d5` (2026-09-04) (develop) = remote | yes | "A procedural city with 100 000 simulated inhabitants" - a technology demonstration built to stress CNA + sharp-runtime (22,081 C++ lines) | sibling `../cnanext`; no lock | none | newly public; candidate showcase card |
| **cna-street** | local `0e7a9e784c44` (2026-09-24); public `develop` = `506cef1f06d94ce86e001ce9ffdcd2efbe01ef6e` (2026-09-23 21:25 UTC) | yes | A procedurally generated European inner-city street (signalised junction, traffic, pedestrians, shadows, reflections) rendered with CNA's extended layer (36,069 C++ lines) | `dependencies.lock`: CNA `d42203805057` (2026-09-06, ABI 0.23), sharp-runtime `30ccdef3`, easy-gl `deda7a42`, meta-gl `20c8b2dc` -- all older than TARGET | yes: `demos.libcna.com/cna-street/cna-street.html` (200) + YouTube "CNA Street" (2026-09-22) | newly public; candidate card |
| **cna-car-simulator** | `04e4d1046e87` (2026-09-24) (main) = remote; 8 uncommitted | yes | Realistic passenger-car driving simulator in a fictional Czech landscape on CNA `next` + sharp-runtime `next` (41,861 C++ lines) | `CARSIM_CNA_ROOT` default `../cna` | yes: `demos.libcna.com/cna-car-simulator/cna-car-simulator.html` + 2 YouTube videos | newly public; candidate card |
| **living-room-simulator** | `2bf3f56b30a8` (2026-09-14) (main) = remote | yes | Explorable 3D living room on CNA EasyGL (OPENGLES3) + CNAEXT; "closed on 2026-09-14 with all nine milestones delivered" (16,064 C++ lines) | `dependencies.lock`: CNA `1b3151f2f1b7` (2026-09-11, ABI 0.26) | none (YouTube video 2026-09-14) | newly public |
| **cna-studio** | `0dd11d5bb11e` (2026-09-24) (branch `claude/studio-baseline-audit-51dyxr`, which is also the GitHub default branch) = remote | yes | "A lightweight visual development companion for CNA": project creation, asset management, scene editing, gizmos, build driver, crash recovery; "at version 1.0.0 the Core workflow was declared complete on 2026-09-23 and Studio entered maintenance mode" (178,418 C++ lines) | `CNA_STUDIO_CNA_ROOT` default `../cna`; "sibling checkout, not a submodule" | none | newly public; note the odd default branch name |
| **cna-multi-language-3d-demo** | `29937cb2b5fd` (2026-09-12) (develop) = remote | yes | One small third-person 3D game defined for CNA and its bindings; only the C++ reference is DONE, C/C#/Java/TypeScript/Python/Rust/Go/Swift/Ruby/Common Lisp are "EMPTY" | `add_subdirectory(CNA_SOURCE_DIR)` | none | must not be presented as multi-language proof |
| **cna-rts** | `1a450bc66dd4` (2026-09-02) (main) | **no** (404 in both orgs) | "One Million Units" RTS benchmark (up to two armies of a million soldiers) on CNA | `add_subdirectory(../cnanext)` | none | not public; do not link |
| **cna-killer** | `095c7394e24e` (2026-09-02) (develop) | **no** | Deliberately malicious fuzz-tester "game" hammering CNA's public API | `add_subdirectory(../cnanext)` | none | not public |
| **cna-benchmark** | `177e73f4d1d4` (2026-09-02) (develop) | **no** | 3DMark-style benchmark: seven fixed graphics workloads, "CNA Score" | `../cnanext` | none | not public |
| **cna-test** (dir title "CNA Lab") | `19ea6c314e51` (2026-08-28) (main) | **no** | single interactive C++23 lab application against `../cnanext` + `../sharp-runtimenext` | same | none | not public; not the same as `cna-lab` |
| **myra-cna** | `b0549a3fa1d4` (2026-08-24) (develop); 2 uncommitted | **no** | Independent C++23 port of the Myra retained-mode UI library for CNA ("incomplete but validated") | `add_subdirectory(MYRA_CNA_CNA_DIR)` | none | not public |
| **house-simulator** ("CNA House") | `f3e14e577329` (2026-09-24) (develop); 33 uncommitted | **no** | Architectural/graphics showcase: a very large American-style house in first person, weather and day/night; Linux, browser, Android | `CNAHOUSE_CNA_ROOT` default `../cnanext` | none published | not public |

Pattern to note for all "sibling checkout" consumers: they build against `../cna` (or the old name `../cnanext`) **at whatever commit is checked out**; only cna-template/cna-c-template/cna-street/living-room-simulator carry a `dependencies.lock`, and all four pins are ancestors of TARGET but predate it (2026-08-11, 08-22, 09-06, 09-11). No consumer repo records "builds at 009d40f5". Whether any of them still builds against TARGET is **unverified** (would require building).

---

## Web demos

`demos.libcna.com` (repo HEAD `f6b37c525f314ff5968f6a6005d9bdac5ebc21fc`, 2026-09-22 18:41:57 +0200, "Add CNA Street demo"; = GitHub `main`) publishes **14** WebAssembly builds (live index has 14 `card` entries; README lists 14). All 14 entry pages and their 38 `.wasm/.js/.data` artifacts answer 200.

| demos.libcna.com entry | On demos.html today? | Live |
|---|---|---|
| `cna_demo_house_3d/cna_house3d_demo.html` (3D House) | yes | 200 |
| `cna_demo_2d/cna_demo_2d.html` (2D sprite demo) | yes | 200 |
| `cna-craft/CnaCraft.html` | yes | 200 |
| `cna-examples/cna_examples.html` | yes | 200 |
| `mesh-craft/MeshCraft.html` | yes | 200 |
| `black-pine/black-pine.html` | yes | 200 |
| `iron-gang/play.html` | yes | 200 |
| `lines-cna/winlinez_cna.html` (Lines CNA) | yes | 200 |
| `mario-cna/copper-boots.html` (Copper Boots) | yes | 200 |
| `people-cna/People.html` | yes | 200 |
| `tamagotchi-cna/TamagotchiCna.html` | yes | 200 |
| `wolf-cna/wolf-cna.html` | yes | 200 |
| **`cna-car-simulator/cna-car-simulator.html`** | **no (new)** | 200 |
| **`cna-street/cna-street.html`** | **no (new)** | 200 |
| `cna-samples/` | - | empty stub (only `.gitignore`); the samples live at samples.libcna.com |

* The 12 web builds on demos.html: **none is dead**. "Twelve web builds available now" is therefore correct for that list but incomplete: 14 exist (car simulator: "Drive through the small town of Lipova with traffic, weather and a day-night cycle"; CNA Street: "builds the street in your browser, so the first start takes about a minute").
* The builds are prebuilt binaries committed to the repo; nothing ties them to alpha.1 or TARGET, and their CNA revisions are not recorded (Speedy Blupi's was shown to be a May 2026 pre-modularization build). Their liveness (HTTP 200 for page and artifacts) is verified; in-browser correct running was not exercised.
* `samples.libcna.com` (HEAD `736b8aa3199e07cb8ce4d174c7290d6db2c8c4aa`): 40 Release/WEBGL2/non-threaded sample bundles + 40 detail pages + 4 gallery pages (`index.html`, `page-2..4.html`): AimingSample, BillboardSample, BloomSample, Bounce, CameraShake, ChaseAndEvade, CollisionSample, ColorReplacement, DistortionSample, FlockingSample, FuzzyLogic, GeneratedGeometry, InputReporter, InputSequence, InstancedModel, LensFlare (published with a documented WebGL limitation), NonPhotoRealistic, NormalMappingEffect, ParticleSample, PathDrawing, Pathfinding, PerPixelCollision, PerPixelLighting, Platformer, Primitives3D, PrimitivesSample, ReachGraphicsDemo, RectangleCollision, RimLighting, SafeArea, ShadowMapping, ShapeRendering, Spacewar, SpriteEffects, SpriteSheet, TexturesAndColors, TransformedCollision, TransformedCollisionTest, VertexLighting, WaypointSample. demos.html says only "being published progressively" without a number.
* speedyblupi.com hosts a separate set of playable builds (SpeedyBlupi2013 [+60/120/144 FPS variants and the obsolete C# one], SpeedyEggbert2, PlanetBlupi, GalaxyEggbert); all 200.
* A visitor-facing caveat that applies to all: hosted GitHub Pages builds cannot set COOP/COEP headers, so threaded builds are impossible (samples README), and no repository workflow launches them continuously (already stated on showcase.html).

---

## Recommended edits

(page -> concrete change; all subject to the presentation-protection rules of the wider refresh)

* **index.html** (Related projects grid)
  * `github.com/libcna/cna-craft` -> `https://github.com/libcna/cna-lab/tree/develop/cna-craft`; `github.com/libcna/cna-editor` -> `.../cna-lab/tree/develop/cna-editor` (or drop the card; cna-studio is the current tool); `github.com/libcna/easy-3d` -> `https://github.com/openeggbert/easy-3d`.
  * cna-extended card: remove "largest project in the ecosystem", "~65,000 lines", "2,363 tests pass"; if a number is wanted: "about 100,000 lines of C++ at commit `5775ecc97`". Link `tree/develop` (the default `master` shows an obsolete July bootstrap README).
  * cna-examples card: replace "60 demos ... Input (50) and Audio (10) ... Devices, Net, Media and both Graphics areas ... still empty, and there are no tests yet" with the current fact (249 demo screens registered at `ea33c9a29`, 13 areas) or delete the count and the "empty" enumeration.
  * cna-template card: remove "140 lines" and "9 CMake presets"; add that its `dependencies.lock` pins CNA of 2026-08-11 and that it is not verified against alpha.1/TARGET.
  * "63 of 86 in-scope official XNA Game Studio 4.0 samples are ported and build. That repository has not changed since the preceding site audit." -> false at both ends: the repo changed continuously (HEAD 2026-09-20) and the counts are 153/87/40. Use the pinned sentence in the cna-samples section or drop numbers. The hero paragraph ("Existing samples are under review; remaining ports, including Racing Game, and web builds are in progress") is consistent with the plan.
  * Optional new cards (all public, all with a web demo or video): cna-car-simulator, cna-street, cna-city, living-room-simulator, cna-studio, cna-lab.
  * Language-support banner: keep "in development"; add that each binding targets one specific experimental ABI (0.21.x) and is not paired with alpha.1 (0.7.0) or the development branch (0.29.0). Do not add Go or Ruby (not public).
* **demos.html**
  * cna-samples box: replace "86 samples ... 63 are real ports that build; the remaining 23 are placeholders" and the whole ".fx bytecode" paragraph with the pinned facts above; remove `PeerToPeer`, `NetworkPrediction`, `TicTacToe`, `TiltPerspective` from the built lists (not complete at `4da98a0`).
  * "Twelve web builds" -> fourteen; add CNA Car Simulator and CNA Street entries with their live URLs; link the 40-sample gallery.
  * "60 demos are registered today" (cna-examples) -> 249 at `ea33c9a29`, or remove.
  * Speedy Blupi section: use the wording options above (web build exists; desktop builds from source; Android project exists but no APK). Remove the two "TODO: APK link" stubs.
  * Android box "NDK toolchain is configured and validated on Android hardware" and "CNA Demo APK ... TODO": nothing published; CNA TARGET has no Android workflow (already stated on showcase.html).
* **showcase.html**
  * `cna-craft` 13,766 lines and `cna-extended` 101,461 lines: drop counts or restate with pins (13,799 lines at cna-lab `49e3cd5b0`; 102,360 lines at `5775ecc97`); fix cna-craft link; the two numbers for cna-extended (65,000 on index, 101,461 here) must not both survive.
  * "63 of the 86 addressable samples build today ... The 23 that don't build ... `.fx`" -> replace (see cna-samples section); the sentence "close [the .fx gap] and most of them come along" is contradicted by the repo.
  * Speedy Blupi block: replace "classic open-source action game ... did not require changes to the game's core logic" and adjust the platform list (web build exists, SDL_Renderer; Android has a project but no APK).
* **videos.html**
  * Remove the "Video links below are placeholders ... TODO: YouTube channel link" banner and the 6+ TODO cards or fill them: the channel `@libcna` exists with 5 videos.
  * Re-caption or replace the three embeds with their real titles/dates/channel (table above). The "House 3D Demo ... EasyGL" caption is not confirmed by the video (title "now partially supports 3D"); "Speedy Blupi on CNA" is really "Speedy Blupi for Windows Phone was ported to C++"; "CNA 2D Demo - SpriteBatch ... rotating sprites" is "CNA now supports 2D" (13 s).
* **network.html**: no dead links; every outbound URL returns 200 (the `github.com/libcna/cna/blob/master/LICENSE` link redirects to `develop`). Optional: describe `samples.libcna.com` as "XNA 4.0 sample ports playable in the browser (40 at 2026-09-20)"; "MeshCraft graphics project" and "EasyGL graphics project" are terse but true.
* **documentation.html**: fix the dead `tree/master/include/Microsoft/Xna/Framework/` link (TARGET permalink or `tree/next/modules/core/include/Microsoft/Xna/Framework`).
* **about / features / roadmap / contribute / contact / architecture / tutorials / docs/roadmap / docs/vs-alternatives / docs/releases**: no dead external link except the `cna-craft` reference on **about.html** (same dead URL) and the `blob/master/...` links (they redirect to `develop` = alpha.1 content; change to `blob/next/...` or a TARGET SHA permalink if the page describes TARGET). `docs/releases.html` / index "GitHub Releases" wording: there are no GitHub Release objects, only tags.
* **docs/tutorials/95-speedy-blupi.html**: see the Speedy Blupi section (fix "open-source" and "original MonoGame codebase", or retitle as a generic porting-patterns tutorial).
* **Cross-cutting**: prefer `https://github.com/libcna/cna/tree/next` or SHA permalinks over `master`/`develop` when documenting TARGET; state on each consumer-project card "results are for that project's pinned revision, not for TARGET"; avoid all fragile counts (lines, tests, demos, samples) unless pinned with SHA and date.

---

## Open questions

1. Was `speedyblupi.com/SpeedyBlupi2013/` ever verified to run in a real browser at all recently, and can the project owner supply the CNA commit the May-2026 wasm was built from? (Static evidence only here.) Is a rebuild against alpha.1 or TARGET planned before the page claims anything about alpha.1?
2. Does the owner consider Speedy Blupi "open source"? The MIT LICENSE (c) 2013 Daniel Roux in mobile-eggbert conflicts with free-eggbert's "original source code ... not publicly released" and the ILSpy-decompilation provenance. Needs an owner decision on the permitted wording.
3. Should the website mention Go and Ruby bindings at all (local-only, 404 on GitHub) and should any binding be re-qualified against 0.29.0 before the docs describe them? (Bindings' READMEs still say 0.20.0 in cna-cs/cna-java/cna-ts while their code says 0.21.0; the READMEs are internally stale.)
4. cna-samples: the `.fx` explanation and 87-complete claim rely on cna-samples `plan.md`; the plan says ✅ requires real-browser gates that this agent did not replicate, and the repo's own `SAMPLES-INFRA-004` validator does not exist yet. Is the owner content for the site to quote the plan's counts (pinned), or should it stay number-free?
5. The five newly public projects (cna-city, cna-street, cna-car-simulator, living-room-simulator, cna-studio) plus cna-lab: does the owner want them added as showcase cards, and is `cna-studio`'s default branch (`claude/studio-baseline-audit-51dyxr`) intentional?
6. `cna-rts`, `cna-killer`, `cna-benchmark`, `cna-test`, `myra-cna`, `house-simulator` are 404 on GitHub (private or unpublished). Confirm they should stay unreferenced.
7. CNA TARGET's own GitHub Actions on `009d40f5`: all 13 workflow runs are concluded `failure` at run level (some individual jobs, e.g. the SDL_RENDERER/OPENGLES3/Vulkan Linux jobs of `input-ci`, succeeded; one failing step was "Checkout cna (with submodules)"). Not investigated here; relevant to any "CI validated" wording (belongs to the CI/tests fact sheet).
8. Public `cna-template`'s weekly CI is red (last 3 runs) and its presets include renderer identities retired in ABI 0.28.0; keep it as the "starting point" card only with a caveat, or replace with cna-c-template / a refreshed template?
9. The 12 `demos.libcna.com` builds' provenance: none records CNA revision; should each card carry a build date (repo commit dates could serve) so visitors do not read them as alpha.1 or TARGET behavior?
