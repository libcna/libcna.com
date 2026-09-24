# Phase 1 — presentation baseline (libcna.com be35902)

Source revision: `be359024e3012653fa1e4963eb3ef86d9c16a5b7`

Generated mechanically by `scripts/inventory_presentation.py` + `scripts/inventory_report.py`. Machine-readable data: `audit/data/phase1-baseline-inventory.json`. This document is the Phase-1 preservation contract: every significant item below must still be present, updated, or explicitly dispositioned in `audit/phase1-presentation-comparison.md`.

## Totals (all HTML pages)

- HTML pages: **174**
- headings: **2113**
- ctas: **79**
- links: **2542**
- cards: **681**
- images: **52**
- videos: **13**
- stats: **8**
- tables: **297**
- blocks: **52**
- primary CTAs (`btn-primary`): **22**

## Presentation-protected pages

| Page | Headings | Blocks | CTAs (primary) | Links | Cards | Images | Videos | Stats | Tables | Words |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `index.html` | 39 | 8 | 33 (3) | 19 | 37 | 0 | 0 | 8 | 0 | 2201 |
| `demos.html` | 38 | 8 | 21 (14) | 6 | 36 | 0 | 0 | 0 | 0 | 1321 |
| `showcase.html` | 21 | 6 | 2 (2) | 7 | 22 | 4 | 0 | 0 | 1 | 1687 |
| `videos.html` | 14 | 2 | 0 (0) | 0 | 11 | 0 | 13 | 0 | 0 | 325 |
| `features.html` | 57 | 2 | 0 (0) | 2 | 2 | 0 | 0 | 0 | 1 | 3818 |
| `about.html` | 10 | 2 | 0 (0) | 10 | 3 | 0 | 0 | 0 | 0 | 1734 |
| `documentation.html` | 37 | 2 | 4 (0) | 33 | 36 | 0 | 0 | 0 | 0 | 718 |
| `tutorials.html` | 8 | 10 | 0 (0) | 137 | 1 | 0 | 0 | 0 | 0 | 1342 |
| `architecture.html` | 20 | 2 | 0 (0) | 3 | 5 | 1 | 0 | 0 | 1 | 1687 |
| `roadmap.html` | 29 | 2 | 0 (0) | 3 | 2 | 0 | 0 | 0 | 0 | 1605 |
| `network.html` | 12 | 4 | 8 (2) | 0 | 9 | 0 | 0 | 0 | 0 | 133 |
| `contact.html` | 19 | 2 | 10 (0) | 0 | 0 | 0 | 0 | 0 | 0 | 336 |

## `index.html`

**Title:** CNA - C++ Reimplementation of the XNA 4.0 API

### Headings / sections

- h1 CNA
-   h2 XNA 4.0 for the modern C++ era
-     h3 XNA-Compatible API
-     h3 Independent platform layer
-     h3 Pluggable Renderers
-     h3 Native C++23
-     h3 Cross-Platform
-     h3 Real .xnb Content Pipeline
-     h3 PBR & Skeletal Animation
-     h3 Built on sharp-runtime
-     h3 Verified Against Real XNA
-   h2 Why CNA?
-     h3 No managed runtime
-     h3 Familiar API
-     h3 Pluggable renderers
-   h2 Familiar XNA-style game loop
-   h2 Get running in 5 minutes
-   h2 Related projects & references
-     h3 Microsoft XNA 4.0 Documentation
-     h3 FNA
-     h3 MonoGame
-     h3 sharp-runtime
-     h3 easy-gl & meta-gl
-     h3 free-direct & free-api
-     h3 FreeDirect game consumers
-     h3 Easy3D
-     h3 CNA glTF Viewer
-     h3 CNA.NET
-     h3 Galaxy Eggbert
-     h3 Mobile Eggbert
-     h3 MeshCraft
-     h3 CNA Editor
-     h3 cna-samples
-     h3 cna-extended
-     h3 cna-craft
-     h3 cna-examples
-     h3 cna-template
-     h3 xna4-spec
-     h3 OpenEggbert ecosystem map

### Major blocks

| Kind | id | Heading | Words | Cards | CTAs | Images |
|---|---|---|---:|---:|---:|---:|
| section |  | CNA | 127 | 0 | 6 | 0 |
| section |  |  | 30 | 0 | 0 | 0 |
| section |  |  | 167 | 0 | 0 | 0 |
| section |  | XNA 4.0 for the modern C++ era | 444 | 9 | 0 | 0 |
| section |  | Why CNA? | 111 | 3 | 0 | 0 |
| section |  | Familiar XNA-style game loop | 91 | 0 | 1 | 0 |
| section |  | Get running in 5 minutes | 108 | 0 | 2 | 0 |
| section |  | Related projects & references | 1123 | 21 | 24 | 0 |

### Statistics

| Value | Label | Hover title |
|---|---|---|
| 0.1.0 | alpha.1 release |  |
| 50 | Renderer identities |  |
| 46 | Implementation families |  |
| 4 | Platform implementations |  |
| 3 | Audio platform choices | SDL3, SDL2 and Null device selections; only SDL3 enables the alpha.1 XNA playback/mixer p… |
| 8,263 | Static test definitions | Across 568 CNA-owned C++ test sources (539 contain macros); vendored third_party sources … |
| 63 / 86 | XNA samples ported |  |
| 21 | CI workflow files | Workflow files, not passing lanes; the intended full-suite job and two Input rows have a … |

### CTAs / buttons

| Label | href | Role | target | Kind | Context |
|---|---|---|---|---|---|
| 📄 View Documentation | `documentation.html` | primary |  | internal | hero: CNA |
| Release notes | `docs/releases.html` | outline |  | internal | hero: CNA |
| 🔗 View GitHub Repository | `https://github.com/libcna/cna` | secondary | _blank | github-repo | hero: CNA |
| ► Try Web Builds | `demos.html` | outline |  | internal | hero: CNA |
| 📖 Book (PDF) | `https://book.libcna.com/CNA_Bible.pdf` | outline | _blank | external-deep | hero: CNA |
| 📖 Book (HTML) | `https://bible.libcna.com` | outline | _blank | external-root | hero: CNA |
| Get Started → | `docs/getting-started.html` | primary |  | internal | section: Familiar XNA-style game loop |
| Full Getting Started Guide → | `docs/getting-started.html` | primary |  | internal | section: Get running in 5 minutes |
| All Build Options → | `docs/building.html` | secondary |  | internal | section: Get running in 5 minutes |
| Microsoft Learn ↗ | `https://learn.microsoft.com/en-us/previous-versions/windows/xna/bb200104(v=xnagamestudio.…` | secondary | _blank | external-deep | card: Microsoft XNA 4.0 Documentation |
| FNA Docs ↗ | `https://fna-xna.github.io/docs/` | secondary | _blank | external-deep | card: FNA |
| MonoGame Docs ↗ | `https://docs.monogame.net/articles/index.html` | secondary | _blank | external-deep | card: MonoGame |
| sharp-runtime on GitHub ↗ | `https://github.com/libcna/sharp-runtime` | secondary | _blank | github-repo | card: sharp-runtime |
| easy-gl ↗ | `https://github.com/libcna/easy-gl` | secondary | _blank | github-repo | card: easy-gl & meta-gl |
| meta-gl ↗ | `https://github.com/libcna/meta-gl` | secondary | _blank | github-repo | card: easy-gl & meta-gl |
| free-direct ↗ | `https://github.com/openeggbert/free-direct` | secondary | _blank | github-repo | card: free-direct & free-api |
| free-api ↗ | `https://github.com/openeggbert/free-api` | secondary | _blank | github-repo | card: free-direct & free-api |
| planetblupi ↗ | `https://github.com/openeggbert/planetblupi` | secondary | _blank | github-repo | card: FreeDirect game consumers |
| free-eggbert ↗ | `https://github.com/openeggbert/free-eggbert` | secondary | _blank | github-repo | card: FreeDirect game consumers |
| easy-3d on GitHub ↗ | `https://github.com/libcna/easy-3d` | secondary | _blank | github-repo | card: Easy3D |
| cna-gltf-viewer on GitHub ↗ | `https://github.com/libcna/cna-gltf-viewer` | secondary | _blank | github-repo | card: CNA glTF Viewer |
| cna-cs on GitHub ↗ | `https://github.com/libcna/cna-cs` | secondary | _blank | github-repo | card: CNA.NET |
| galaxy-eggbert on GitHub ↗ | `https://github.com/openeggbert/galaxy-eggbert` | secondary | _blank | github-repo | card: Galaxy Eggbert |
| mobile-eggbert on GitHub ↗ | `https://github.com/openeggbert/mobile-eggbert` | secondary | _blank | github-repo | card: Mobile Eggbert |
| mesh-craft on GitHub ↗ | `https://github.com/libcna/mesh-craft` | secondary | _blank | github-repo | card: MeshCraft |
| cna-editor on GitHub ↗ | `https://github.com/libcna/cna-editor` | secondary | _blank | github-repo | card: CNA Editor |
| cna-samples on GitHub ↗ | `https://github.com/libcna/cna-samples` | secondary | _blank | github-repo | card: cna-samples |
| cna-extended on GitHub ↗ | `https://github.com/libcna/cna-extended` | secondary | _blank | github-repo | card: cna-extended |
| cna-craft on GitHub ↗ | `https://github.com/libcna/cna-craft` | secondary | _blank | github-repo | card: cna-craft |
| cna-examples on GitHub ↗ | `https://github.com/libcna/cna-examples` | secondary | _blank | github-repo | card: cna-examples |
| cna-template on GitHub ↗ | `https://github.com/libcna/cna-template` | secondary | _blank | github-repo | card: cna-template |
| xna4-spec on GitHub ↗ | `https://github.com/libcna/xna4-spec` | secondary | _blank | github-repo | card: xna4-spec |
| openeggbert on GitHub ↗ | `https://github.com/openeggbert/openeggbert` | secondary | _blank | github-repo | card: OpenEggbert ecosystem map |

### Cards / callouts

| Kind | Title | Words | CTAs |
|---|---|---:|---|
| callout | First tagged release. | 84 |  |
| callout | Read capabilities narrowly. | 83 |  |
| card | XNA-Compatible API | 20 |  |
| card | Independent platform layer | 47 |  |
| card | Pluggable Renderers | 49 |  |
| card | Native C++23 | 20 |  |
| card | Cross-Platform | 65 |  |
| card | Real .xnb Content Pipeline | 46 |  |
| card | PBR & Skeletal Animation | 50 |  |
| card | Built on sharp-runtime | 54 |  |
| card | Verified Against Real XNA | 61 |  |
| card | No managed runtime | 23 |  |
| card | Familiar API | 27 |  |
| card | Pluggable renderers | 40 |  |
| callout | Release boundary: | 56 |  |
| callout | CNA is partially based on FNA (C#). | 50 |  |
| card | Microsoft XNA 4.0 Documentation | 27 | Microsoft Learn ↗ |
| card | FNA | 28 | FNA Docs ↗ |
| card | MonoGame | 25 | MonoGame Docs ↗ |
| card | sharp-runtime | 34 | sharp-runtime on GitHub ↗ |
| card | easy-gl & meta-gl | 36 | easy-gl ↗; meta-gl ↗ |
| card | free-direct & free-api | 32 | free-direct ↗; free-api ↗ |
| card | FreeDirect game consumers | 49 | planetblupi ↗; free-eggbert ↗ |
| card | Easy3D | 32 | easy-3d on GitHub ↗ |
| card | CNA glTF Viewer | 35 | cna-gltf-viewer on GitHub ↗ |
| card | CNA.NET | 54 | cna-cs on GitHub ↗ |
| card | Galaxy Eggbert | 37 | galaxy-eggbert on GitHub ↗ |
| card | Mobile Eggbert | 43 | mobile-eggbert on GitHub ↗ |
| card | MeshCraft | 35 | mesh-craft on GitHub ↗ |
| card | CNA Editor | 48 | cna-editor on GitHub ↗ |
| card | cna-samples | 50 | cna-samples on GitHub ↗ |
| card | cna-extended | 91 | cna-extended on GitHub ↗ |
| card | cna-craft | 76 | cna-craft on GitHub ↗ |
| card | cna-examples | 69 | cna-examples on GitHub ↗ |
| card | cna-template | 73 | cna-template on GitHub ↗ |
| card | xna4-spec | 56 | xna4-spec on GitHub ↗ |
| card | OpenEggbert ecosystem map | 45 | openeggbert on GitHub ↗ |

### Significant external links

| Label | href | Kind |
|---|---|---|
| View on GitHub | `https://github.com/libcna/cna` | github-repo |
| blog.libcna.com | `https://blog.libcna.com/` | external-root |
| Browse published samples | `https://samples.libcna.com/` | external-root |
| C# | `https://github.com/libcna/cna-cs` | github-repo |
| Java | `https://github.com/libcna/cna-java` | github-repo |
| TypeScript | `https://github.com/libcna/cna-ts` | github-repo |
| Python | `https://github.com/libcna/cna-python` | github-repo |
| Rust | `https://github.com/libcna/cna-rust` | github-repo |
| Swift | `https://github.com/libcna/cna-swift` | github-repo |
| sharp-runtime | `https://github.com/libcna/sharp-runtime` | github-repo |
| cna-samples | `https://github.com/libcna/cna-samples` | github-repo |
| CNA Craft | `https://github.com/libcna/cna-craft` | github-repo |
| openeggbert GitHub account | `https://github.com/openeggbert` | github-org |
| FNA | `https://github.com/FNA-XNA/FNA` | github-repo |
| THIRD_PARTY_NOTICES.md | `https://github.com/libcna/cna/blob/v0.1.0-alpha.1/THIRD_PARTY_NOTICES.md` | github-deep |

## `demos.html`

**Title:** Demos - CNA

### Headings / sections

- h1 CNA Demos
-   h2 📚 cna-samples (GitHub)
-       h4 Rendering & 3D
-       h4 Gameplay & complete games
-       h4 Input & devices
-       h4 Audio
-       h4 Collision, physics & AI
-       h4 Cameras, UI & networking
-   h2 🌐 Web Builds (Emscripten / WebGL 2)
-       h4 House 3D Demo
-       h4 cna-demo (2D Sprite Demo)
-       h4 CNA Craft
-       h4 CNA Examples
-       h4 Mesh Craft
-       h4 Black Pine
-       h4 Iron Gang
-       h4 Lines CNA
-       h4 Copper Boots
-       h4 People
-       h4 Tamagotchi CNA
-       h4 Wolf CNA
-   h2 📱 Android Builds
-       h4 CNA Demo APK
-       h4 Speedy Blupi - Android Port
-   h2 🖥 Desktop Builds
-       h4 House 3D Demo - Linux
-       h4 2D Sprite Demo - Linux
-       h4 Input Demo - Linux
-       h4 Sound Demo - Linux
-       h4 Prebuilt Releases
-   h2 🏃 Speedy Blupi - Port / Demo
-       h4 Speedy Blupi - Desktop
-       h4 Speedy Blupi - Web
-       h4 Speedy Blupi - Android
-   h2 🎮 cna-examples (GitHub)
-       h4 Input — 50 demos
-       h4 Audio — 10 demos
-       h4 Not yet written

### Major blocks

| Kind | id | Heading | Words | Cards | CTAs | Images |
|---|---|---|---:|---:|---:|---:|
| page-header |  | CNA Demos | 30 | 0 | 0 | 0 |
| section |  | 📚 cna-samples (GitHub) | 1291 | 31 | 21 | 0 |
| demo-platform | cna-samples | 📚 cna-samples (GitHub) | 322 | 6 | 2 | 0 |
| demo-platform |  | 🌐 Web Builds (Emscripten / WebGL 2) | 283 | 12 | 12 | 0 |
| demo-platform |  | 📱 Android Builds | 80 | 2 | 0 | 0 |
| demo-platform |  | 🖥 Desktop Builds | 178 | 5 | 5 | 0 |
| demo-platform |  | 🏃 Speedy Blupi - Port / Demo | 131 | 3 | 1 | 0 |
| demo-platform |  | 🎮 cna-examples (GitHub) | 231 | 3 | 1 | 0 |

### CTAs / buttons

| Label | href | Role | target | Kind | Context |
|---|---|---|---|---|---|
| Browse and play CNA Samples → | `https://samples.libcna.com/` | primary | _blank | external-root | demo-platform: 📚 cna-samples (GitHub) |
| View on GitHub | `https://github.com/libcna/cna-samples` | secondary | _blank | github-repo | demo-platform: 📚 cna-samples (GitHub) |
| Play in Browser | `https://demos.libcna.com/cna_demo_house_3d/cna_house3d_demo.html` | primary | _blank | external-deep | demo-item: House 3D Demo |
| Play in Browser | `https://demos.libcna.com/cna_demo_2d/cna_demo_2d.html` | primary | _blank | external-deep | demo-item: cna-demo (2D Sprite Demo) |
| Play in Browser | `https://demos.libcna.com/cna-craft/CnaCraft.html` | primary | _blank | external-deep | demo-item: CNA Craft |
| Play in Browser | `https://demos.libcna.com/cna-examples/cna_examples.html` | primary | _blank | external-deep | demo-item: CNA Examples |
| Play in Browser | `https://demos.libcna.com/mesh-craft/MeshCraft.html` | primary | _blank | external-deep | demo-item: Mesh Craft |
| Play in Browser | `https://demos.libcna.com/black-pine/black-pine.html` | primary | _blank | external-deep | demo-item: Black Pine |
| Play in Browser | `https://demos.libcna.com/iron-gang/play.html` | primary | _blank | external-deep | demo-item: Iron Gang |
| Play in Browser | `https://demos.libcna.com/lines-cna/winlinez_cna.html` | primary | _blank | external-deep | demo-item: Lines CNA |
| Play in Browser | `https://demos.libcna.com/mario-cna/copper-boots.html` | primary | _blank | external-deep | demo-item: Copper Boots |
| Play in Browser | `https://demos.libcna.com/people-cna/People.html` | primary | _blank | external-deep | demo-item: People |
| Play in Browser | `https://demos.libcna.com/tamagotchi-cna/TamagotchiCna.html` | primary | _blank | external-deep | demo-item: Tamagotchi CNA |
| Play in Browser | `https://demos.libcna.com/wolf-cna/wolf-cna.html` | primary | _blank | external-deep | demo-item: Wolf CNA |
| Build Instructions | `docs/building.html` | secondary |  | internal | demo-item: House 3D Demo - Linux |
| Build Instructions | `docs/building.html` | secondary |  | internal | demo-item: 2D Sprite Demo - Linux |
| Build Instructions | `docs/building.html` | secondary |  | internal | demo-item: Input Demo - Linux |
| Build Instructions | `docs/building.html` | secondary |  | internal | demo-item: Sound Demo - Linux |
| GitHub Releases | `https://github.com/libcna/cna/releases` | secondary | _blank | github-deep | demo-item: Prebuilt Releases |
| Play in Browser | `https://speedyblupi.com/SpeedyBlupi2013/` | primary | _blank | external-deep | demo-item: Speedy Blupi - Web |
| View on GitHub | `https://github.com/libcna/cna-examples` | secondary | _blank | github-repo | demo-platform: 🎮 cna-examples (GitHub) |

### Cards / callouts

| Kind | Title | Words | CTAs |
|---|---|---:|---|
| callout | Twelve web builds available now: | 35 |  |
| callout | Playable sample gallery. | 15 |  |
| callout | Why 23 samples do not build. | 94 |  |
| demo-item | Rendering & 3D | 25 |  |
| demo-item | Gameplay & complete games | 26 |  |
| demo-item | Input & devices | 19 |  |
| demo-item | Audio | 16 |  |
| demo-item | Collision, physics & AI | 26 |  |
| demo-item | Cameras, UI & networking | 24 |  |
| demo-item | House 3D Demo | 33 | Play in Browser |
| demo-item | cna-demo (2D Sprite Demo) | 24 | Play in Browser |
| demo-item | CNA Craft | 19 | Play in Browser |
| demo-item | CNA Examples | 19 | Play in Browser |
| demo-item | Mesh Craft | 18 | Play in Browser |
| demo-item | Black Pine | 19 | Play in Browser |
| demo-item | Iron Gang | 18 | Play in Browser |
| demo-item | Lines CNA | 23 | Play in Browser |
| demo-item | Copper Boots | 19 | Play in Browser |
| demo-item | People | 19 | Play in Browser |
| demo-item | Tamagotchi CNA | 21 | Play in Browser |
| demo-item | Wolf CNA | 18 | Play in Browser |
| demo-item | CNA Demo APK | 25 |  |
| demo-item | Speedy Blupi - Android Port | 27 |  |
| demo-item | House 3D Demo - Linux | 44 | Build Instructions |
| demo-item | 2D Sprite Demo - Linux | 29 | Build Instructions |
| demo-item | Input Demo - Linux | 27 | Build Instructions |
| demo-item | Sound Demo - Linux | 24 | Build Instructions |
| demo-item | Prebuilt Releases | 20 | GitHub Releases |
| demo-item | Speedy Blupi - Desktop | 26 |  |
| demo-item | Speedy Blupi - Web | 32 | Play in Browser |
| demo-item | Speedy Blupi - Android | 20 |  |
| callout | Early — two of seven areas are populated. | 56 |  |
| demo-item | Input — 50 demos | 25 |  |
| demo-item | Audio — 10 demos | 41 |  |
| demo-item | Not yet written | 31 |  |
| callout | Build it yourself now: | 31 |  |

### Significant external links

| Label | href | Kind |
|---|---|---|
| demos.libcna.com | `https://demos.libcna.com/` | external-root |
| samples.libcna.com | `https://samples.libcna.com/` | external-root |

## `showcase.html`

**Title:** Showcase - CNA Demos & Real-World Usage

### Headings / sections

- h1 Showcase
-   h2 🌐 Browser Demos
-     h3 House 3D Demo
-     h3 CNA 2D Demo
-   h2 🎯 Verification against the real XNA runtime
-     h3 Pixel-exact against real XNA
-     h3 Differential testing against FNA
-     h3 Real ported games
-     h3 What the oracle corpus actually looks like
-   h2 🏃 Real-World Validation — Speedy Blupi
-     h3 What Speedy Blupi validates
-     h3 What it proves
-     h3 Platform targets
-   h2 📚 Sample Applications — cna-samples
-     h3 PrimitivesSample
-     h3 Primitives3D
-     h3 CatapultWars
-     h3 GameStateManagement
-     h3 Pathfinding & FlockingSample
-     h3 Audio3D & GesturesSample
-   h2 🖥 Platform Validation

### Major blocks

| Kind | id | Heading | Words | Cards | CTAs | Images |
|---|---|---|---:|---:|---:|---:|
| page-header |  | Showcase | 20 | 0 | 0 | 0 |
| section |  | 🌐 Browser Demos | 267 | 2 | 2 | 0 |
| section |  | 🎯 Verification against the real XNA runtime | 400 | 7 | 0 | 4 |
| section |  | 🏃 Real-World Validation — Speedy Blupi | 253 | 3 | 0 | 0 |
| section |  | 📚 Sample Applications — cna-samples | 475 | 6 | 0 | 0 |
| section |  | 🖥 Platform Validation | 272 | 0 | 0 | 0 |

### CTAs / buttons

| Label | href | Role | target | Kind | Context |
|---|---|---|---|---|---|
| ▶ Play in Browser | `https://demos.libcna.com/cna_demo_house_3d/cna_house3d_demo.html` | primary | _blank | external-deep | card: House 3D Demo |
| ▶ Play in Browser | `https://demos.libcna.com/cna_demo_2d/cna_demo_2d.html` | primary | _blank | external-deep | card: CNA 2D Demo |

### Cards / callouts

| Kind | Title | Words | CTAs |
|---|---|---:|---|
| card | House 3D Demo | 75 | ▶ Play in Browser |
| card | CNA 2D Demo | 67 | ▶ Play in Browser |
| callout | Note: | 70 |  |
| card | Pixel-exact against real XNA | 72 |  |
| card | Differential testing against FNA | 67 |  |
| card | Real ported games | 70 |  |
| card |  | 2 |  |
| card |  | 6 |  |
| card |  | 3 |  |
| card |  | 3 |  |
| callout | The honest framing: | 64 |  |
| card | What Speedy Blupi validates | 65 |  |
| card | What it proves | 81 |  |
| card | Platform targets | 66 |  |
| card | PrimitivesSample | 48 |  |
| card | Primitives3D | 51 |  |
| card | CatapultWars | 49 |  |
| card | GameStateManagement | 44 |  |
| card | Pathfinding & FlockingSample | 46 |  |
| card | Audio3D & GesturesSample | 43 |  |
| callout | Repository: | 35 |  |
| callout | Renderer note: | 69 |  |

### Images

| src | alt | clickable | caption |
|---|---|---|---|
| `img/oracle/colored3d.png` | A triangle on a cornflower-blue background with red, green … | False  | Vertex-coloured triangle. |
| `img/oracle/alphatest_quad.png` | A quad with only its left half drawn — a red block above a … | False  | Alpha test discarding half a quad. |
| `img/oracle/envmap_fresnel_quad.png` | A square shading from bright orange-brown at the top to nea… | False  | Fresnel-weighted environment reflection. |
| `img/oracle/sprite_sortmode_backtofront_quad.png` | A brown square on a black background, the topmost sprite af… | False  | Back-to-front sprite sorting. |

### Tables

| Purpose | Headers | Data rows |
|---|---|---:|
| 🖥 Platform Validation | Platform / Renderer / Status / Notes | 4 |

### Significant external links

| Label | href | Kind |
|---|---|---|
| cna-craft | `https://github.com/libcna/cna-craft` | github-repo |
| cna-extended | `https://github.com/libcna/cna-extended` | github-repo |
| cna-samples | `https://github.com/libcna/cna-samples` | github-repo |
| github.com/libcna/cna-samples | `https://github.com/libcna/cna-samples` | github-repo |

## `videos.html`

**Title:** Videos - CNA

### Headings / sections

- h1 CNA on YouTube
-   h2 Demo Videos
-     h3 House 3D Demo
-     h3 Speedy Blupi on CNA
-     h3 CNA 2D Demo
-     h3 Web Build Demo
-   h2 Progress & Development
-     h3 Development Update #1
-     h3 Development Update #2
-     h3 Development Update #3
-   h2 Architecture & Walkthroughs
-     h3 CNA Architecture Walkthrough
-     h3 Rendering Renderer Comparison
-     h3 Building CNA from Source

### Major blocks

| Kind | id | Heading | Words | Cards | CTAs | Images |
|---|---|---|---:|---:|---:|---:|
| page-header |  | CNA on YouTube | 19 | 0 | 0 | 0 |
| section |  | Demo Videos | 306 | 10 | 0 | 0 |

### Cards / callouts

| Kind | Title | Words | CTAs |
|---|---|---:|---|
| callout |  | 31 |  |
| video-card | House 3D Demo | 14 |  |
| video-card | Speedy Blupi on CNA | 21 |  |
| video-card | CNA 2D Demo | 15 |  |
| video-card | Web Build Demo | 20 |  |
| video-card | Development Update #1 | 18 |  |
| video-card | Development Update #2 | 18 |  |
| video-card | Development Update #3 | 33 |  |
| video-card | CNA Architecture Walkthrough | 24 |  |
| video-card | Rendering Renderer Comparison | 35 |  |
| video-card | Building CNA from Source | 24 |  |

### Videos / media

| id | title | thumbnail | CTA hrefs |
|---|---|---|---|
| YzhewIB2X9c | House 3D Demo |  |  |
| TScL1L-dbHE | Speedy Blupi on CNA |  |  |
| tIMj20Ts2dg | CNA 2D Demo |  |  |
|  | Web Build Demo |  |  |
|  | Development Update #1 |  |  |
|  | Development Update #2 |  |  |
|  | Development Update #3 |  |  |
|  | CNA Architecture Walkthrough |  |  |
|  | Rendering Renderer Comparison |  |  |
|  | Building CNA from Source |  |  |
| https://www.youtube.com/embed/YzhewIB2X9c | House 3D Demo - CNA |  |  |
| https://www.youtube.com/embed/TScL1L-dbHE | Speedy Blupi on CNA |  |  |
| https://www.youtube.com/embed/tIMj20Ts2dg | CNA 2D Demo - SpriteBatch |  |  |

## `features.html`

**Title:** Features - CNA

### Headings / sections

- h1 What CNA offers
-   h2 XNA 4.0 API Implementation
-     h3 Game Loop
-     h3 SpriteBatch
-     h3 Texture2D
-     h3 GraphicsDevice
-     h3 Math Types
-     h3 PackedVector Types
-     h3 Input
-     h3 Devices & Sensors
-     h3 Audio
-     h3 Content System & .xnb Pipeline
-     h3 Networking
-     h3 GamerServices & Avatar
-   h2 3D Rendering Pipeline
-     h3 3D Rendering
-     h3 Effects System
-     h3 PBR & Skeletal Animation
-     h3 Vertex & Index Buffers
-     h3 Model System
-     h3 SpriteFont
-     h3 Media & Video Playback
-     h3 Storage
-     h3 Multisample Anti-Aliasing
-     h3 OcclusionQuery
-     h3 Context-Loss Recovery
-   h2 Platform and audio implementations
-     h3 Windowing & Events
-     h3 Selectable audio integration
-     h3 SDL3_image Loading
-   h2 Pluggable Renderers
-     h3 SDL_Renderer Renderer
-     h3 EasyGL (OpenGL) Renderer
-     h3 bgfx Renderer
-     h3 Vulkan Renderer
-     h3 Direct3D 11 Renderer
-     h3 Direct3D 12 Renderer
-     h3 WebGPU Renderer
-     h3 Headless Renderer
-     h3 Software Renderer
-     h3 Direct3D 9 Renderer
-     h3 SDL_GPU Renderer
-     h3 FreeDirect (DirectDraw) Renderer
-     h3 ASCII post-process effect
-     h3 Canvas Renderer
-   h2 Cross-Platform Architecture
-     h3 Linux (x86_64)
-     h3 Windows (x86_64)
-     h3 Android
-     h3 Emscripten / Web
-     h3 macOS / iOS
-   h2 Modern C++23 Codebase
-     h3 C++23 Standard
-     h3 CMake Build System
-     h3 Test Suite
-     h3 Continuous Integration
-     h3 sharp-runtime

### Major blocks

| Kind | id | Heading | Words | Cards | CTAs | Images |
|---|---|---|---:|---:|---:|---:|
| page-header |  | What CNA offers | 27 | 0 | 0 | 0 |
| section |  | XNA 4.0 API Implementation | 3791 | 0 | 0 | 0 |

### Cards / callouts

| Kind | Title | Words | CTAs |
|---|---|---:|---|
| callout | This page describes CNA 0.1.0-alpha.1. | 94 |  |
| callout | 50 renderer identities is not 46 equally complete renderers. | 77 |  |

### Tables

| Purpose | Headers | Data rows |
|---|---|---:|
| Pluggable Renderers | Renderer / Maturity / Scope / Notes | 13 |

## `about.html`

**Title:** About CNA - C++ Reimplementation of the XNA 4.0 API

### Headings / sections

- h1 What is CNA?
-   h2 Background - the XNA programming model
-   h2 Why CNA?
-   h2 What problem does CNA solve?
-   h2 What CNA is not
-   h2 Relationship to FNA and MonoGame `#fna`
-   h2 C++ API differences — the CNAEXT marker
-   h2 Technology stack
-   h2 Real-world validation
-   h2 Licence Ms-PL License

### Major blocks

| Kind | id | Heading | Words | Cards | CTAs | Images |
|---|---|---|---:|---:|---:|---:|
| page-header |  | What is CNA? | 32 | 0 | 0 | 0 |
| section |  | Background - the XNA programming model | 1702 | 0 | 0 | 0 |

### Cards / callouts

| Kind | Title | Words | CTAs |
|---|---|---:|---|
| callout | CNA 0.1.0-alpha.1 | 90 |  |
| callout | Where the project actually stands. | 94 |  |
| callout | Attribution - based in part on FNA (C#): | 90 |  |

### Significant external links

| Label | href | Kind |
|---|---|---|
| FNA | `https://github.com/FNA-XNA/FNA` | github-repo |
| NOTICE.md | `https://github.com/libcna/cna/blob/v0.1.0-alpha.1/NOTICE.md` | github-deep |
| THIRD_PARTY_NOTICES.md | `https://github.com/libcna/cna/blob/v0.1.0-alpha.1/THIRD_PARTY_NOTICES.md` | github-deep |
| FNA | `https://fna-xna.github.io/docs/` | external-deep |
| MonoGame | `https://docs.monogame.net/articles/index.html` | external-deep |
| cna-samples | `https://github.com/libcna/cna-samples` | github-repo |
| CNA Craft | `https://github.com/libcna/cna-craft` | github-repo |
| LICENSE file | `https://github.com/libcna/cna/blob/v0.1.0-alpha.1/LICENSE` | github-deep |

## `documentation.html`

**Title:** Documentation - CNA

### Headings / sections

- h1 CNA Documentation
-     h3 Getting Started
-     h3 Building
-     h3 Releases & Versioning
-     h3 Platforms
-     h3 Graphics Renderers
-     h3 Runtime Renderer Selection
-     h3 Experimental Native C API
-     h3 XNA Compatibility
-     h3 Verification & Known Issues
-     h3 Effects System
-     h3 SpriteBatch
-     h3 Audio System
-     h3 Input System
-     h3 Math Types
-     h3 Roadmap
-     h3 FAQ
-   h2 Subsystem reference
-     h3 3D Rendering
-     h3 Graphics State
-     h3 Render Targets
-     h3 Shader Effects
-     h3 ContentManager
-     h3 XNB Content Pipeline
-     h3 Model Loading
-     h3 Game Loop & Lifecycle
-     h3 PackedVector Types
-     h3 Storage
-     h3 Video Playback
-     h3 Sensors
-     h3 CNA vs Alternatives
-     h3 Migration from MonoGame / XNA
-   h2 External references
-     h3 Microsoft XNA 4.0 API Reference
-     h3 FNA Documentation
-     h3 MonoGame Documentation
-     h3 SDL3 Documentation

### Major blocks

| Kind | id | Heading | Words | Cards | CTAs | Images |
|---|---|---|---:|---:|---:|---:|
| page-header |  | CNA Documentation | 22 | 0 | 0 | 0 |
| section |  | Getting Started | 696 | 34 | 4 | 0 |

### CTAs / buttons

| Label | href | Role | target | Kind | Context |
|---|---|---|---|---|---|
| Open ↗ | `https://learn.microsoft.com/en-us/previous-versions/windows/xna/bb200104(v=xnagamestudio.…` | secondary | _blank | external-deep | card: Microsoft XNA 4.0 API Reference |
| Open ↗ | `https://fna-xna.github.io/docs/` | secondary | _blank | external-deep | card: FNA Documentation |
| Open ↗ | `https://docs.monogame.net/articles/index.html` | secondary | _blank | external-deep | card: MonoGame Documentation |
| Open ↗ | `https://wiki.libsdl.org/SDL3/` | secondary | _blank | external-deep | card: SDL3 Documentation |

### Cards / callouts

| Kind | Title | Words | CTAs |
|---|---|---:|---|
| callout |  | 36 |  |
| callout | Doxygen API reference: | 50 |  |
| card | Getting Started | 21 |  |
| card | Building | 18 |  |
| card | Releases & Versioning | 25 |  |
| card | Platforms | 13 |  |
| card | Graphics Renderers | 45 |  |
| card | Runtime Renderer Selection | 15 |  |
| card | Experimental Native C API | 20 |  |
| card | XNA Compatibility | 21 |  |
| card | Verification & Known Issues | 31 |  |
| card | Effects System | 14 |  |
| card | SpriteBatch | 14 |  |
| card | Audio System | 15 |  |
| card | Input System | 16 |  |
| card | Math Types | 16 |  |
| card | Roadmap | 13 |  |
| card | FAQ | 16 |  |
| card | 3D Rendering | 11 |  |
| card | Graphics State | 7 |  |
| card | Render Targets | 9 |  |
| card | Shader Effects | 20 |  |
| card | ContentManager | 17 |  |
| card | XNB Content Pipeline | 18 |  |
| card | Model Loading | 14 |  |
| card | Game Loop & Lifecycle | 13 |  |
| card | PackedVector Types | 13 |  |
| card | Storage | 11 |  |
| card | Video Playback | 9 |  |
| card | Sensors | 20 |  |
| card | CNA vs Alternatives | 12 |  |
| card | Migration from MonoGame / XNA | 17 |  |
| card | Microsoft XNA 4.0 API Reference | 18 | Open ↗ |
| card | FNA Documentation | 19 | Open ↗ |
| card | MonoGame Documentation | 17 | Open ↗ |
| card | SDL3 Documentation | 20 | Open ↗ |

### Significant external links

| Label | href | Kind |
|---|---|---|
| GitHub | `https://github.com/libcna/cna` | github-repo |
| Doxygen | `https://www.doxygen.nl/` | external-root |
| include/Microsoft/Xna/Framework/ on GitHub | `https://github.com/libcna/cna/tree/master/include/Microsoft/Xna/Framework/` | github-deep |

## `tutorials.html`

**Title:** Tutorials - CNA Game Development Guides

### Headings / sections

- h1 CNA Tutorials
-   h2 Getting Started
-   h2 Core Systems
-   h2 Graphics and Architecture
-   h2 Real-World and Platform
-   h2 Renderers in Depth
-   h2 3D Content and CNA Extensions
-   h2 Audio, Media, Services and Verification

### Major blocks

| Kind | id | Heading | Words | Cards | CTAs | Images |
|---|---|---|---:|---:|---:|---:|
| page-header |  | CNA Tutorials | 68 | 0 | 0 | 0 |
| section |  |  | 22 | 0 | 0 | 0 |
| section | beginner | Getting Started | 182 | 0 | 0 | 0 |
| section | intermediate | Core Systems | 244 | 0 | 0 | 0 |
| section | advanced | Graphics and Architecture | 216 | 0 | 0 | 0 |
| section | expert | Real-World and Platform | 194 | 0 | 0 | 0 |
| section | renderers | Renderers in Depth | 114 | 0 | 0 | 0 |
| section | content-ext | 3D Content and CNA Extensions | 119 | 0 | 0 | 0 |
| section | subsystems | Audio, Media, Services and Verification | 150 | 0 | 0 | 0 |
| section |  |  | 33 | 0 | 0 | 0 |

### Cards / callouts

| Kind | Title | Words | CTAs |
|---|---|---:|---|
| callout | Want a tutorial faster? | 33 |  |

### Significant external links

| Label | href | Kind |
|---|---|---|
| GitHub | `https://github.com/libcna/cna` | github-repo |

## `architecture.html`

**Title:** Architecture - CNA

### Headings / sections

- h1 How CNA is structured
-   h2 Layer overview
-   h2 Detailed architecture diagram
-   h2 Layer descriptions
-       h4 Game / Application Code
-       h4 XNA-Compatible API Layer
-       h4 CNA Internal Layer & sharp-runtime Support
-       h4 Renderer, platform and audio implementations
-   h2 Required sibling repositories
-       h4 sharp-runtime
-       h4 easy-gl
-   h2 Which renderer should I choose?
-   h2 Key architectural decisions
-     h3 Interface/Implementation separation
-     h3 Compact default, opt-in runtime selection
-     h3 Vendored dependencies
-     h3 XNA namespace mirroring
-     h3 sharp-runtime support layer
-   h2 Key C++23 features used in CNA
-   h2 Directory structure

### Major blocks

| Kind | id | Heading | Words | Cards | CTAs | Images |
|---|---|---|---:|---:|---:|---:|
| page-header |  | How CNA is structured | 23 | 0 | 0 | 0 |
| section |  | Layer overview | 1664 | 5 | 0 | 1 |

### Cards / callouts

| Kind | Title | Words | CTAs |
|---|---|---:|---|
| card | Interface/Implementation separation | 29 |  |
| card | Compact default, opt-in runtime selection | 33 |  |
| card | Vendored dependencies | 30 |  |
| card | XNA namespace mirroring | 23 |  |
| card | sharp-runtime support layer | 32 |  |

### Images

| src | alt | clickable | caption |
|---|---|---|---|
| `mermaid-diagram.png` | CNA detailed architecture diagram | False  |  |

### Tables

| Purpose | Headers | Data rows |
|---|---|---:|
| Which renderer should I choose? | Renderer / Best for / Scope / Platform | 12 |

## `roadmap.html`

**Title:** Roadmap - CNA

### Headings / sections

- h1 Development Roadmap
-   h2 Where CNA actually is
-   h2 What is done and verified
-     h3 50 renderer identities, single or multi-renderer builds Shipped
-     h3 EasyGL renderer — the most mature path Shipped
-     h3 Direct3D 9 renderer — functional, and the pixel-exact XNA oracle target Shipped
-     h3 Vulkan renderer Shipped
-     h3 SDL_GPU renderer Shipped
-     h3 FreeDirect renderer — the best 2D fidelity in the project Shipped
-     h3 ASCII effect Migrated
-     h3 Canvas renderer (Emscripten) Configuration-specific
-     h3 The .xnb content pipeline Shipped
-     h3 PBR effects and skeletal animation Shipped
-     h3 Pixel-exact verification against the real XNA runtime Shipped
-     h3 A real Input, Audio, Net and Storage core Shipped
-   h2 Partial, and known to be partial
-     h3 DIRECTX12 — missing scissor, viewport, stencil and blend factor Partial
-     h3 WebGPU — no render targets at all Partial
-     h3 bgfx — no D3D or Metal shader blobs Partial
-     h3 Continuous integration Partial
-     h3 Truthful capability reporting Partial
-   h2 Work that remains before 1.0
-     h3 Compiled effects beyond qualified builds Partial
-     h3 Consistent surface-format coverage Renderer-dependent
-     h3 ReflectiveReader for custom XNB types Not started
-     h3 A GamerServices service renderer Not started
-     h3 Media portability and codec coverage Platform-dependent
-     h3 Deeper tests for Media, Storage and Canvas Open
-     h3 Public stable release (v1.0) Long term

### Major blocks

| Kind | id | Heading | Words | Cards | CTAs | Images |
|---|---|---|---:|---:|---:|---:|
| page-header |  | Development Roadmap | 27 | 0 | 0 | 0 |
| section |  | Where CNA actually is | 1578 | 0 | 0 | 0 |

### Cards / callouts

| Kind | Title | Words | CTAs |
|---|---|---:|---|
| callout | Honest timeline note: | 41 |  |
| callout | Contributing: | 36 |  |

### Significant external links

| Label | href | Kind |
|---|---|---|
| GitHub repository | `https://github.com/libcna/cna` | github-repo |

## `network.html`

**Title:** CNA Network - libcna.com Sites & Services

### Headings / sections

- h1 Sites & services
-   h2 Read and follow
-     h3 CNA Bible
-     h3 CNA Book
-     h3 Blog
-   h2 Try and explore
-     h3 Demos
-     h3 Samples
-   h2 Graphics projects
-     h3 EasyGL
-     h3 MeshCraft
-     h3 MetaGL

### Major blocks

| Kind | id | Heading | Words | Cards | CTAs | Images |
|---|---|---|---:|---:|---:|---:|
| page-header |  | Sites & services | 16 | 0 | 0 | 0 |
| section |  | Read and follow | 44 | 3 | 3 | 0 |
| section |  | Try and explore | 30 | 2 | 2 | 0 |
| section |  | Graphics projects | 43 | 3 | 3 | 0 |

### CTAs / buttons

| Label | href | Role | target | Kind | Context |
|---|---|---|---|---|---|
| bible.libcna.com ↗ | `https://bible.libcna.com/` | secondary | _blank | external-root | card: CNA Bible |
| book.libcna.com ↗ | `https://book.libcna.com/` | secondary | _blank | external-root | card: CNA Book |
| blog.libcna.com ↗ | `https://blog.libcna.com/` | secondary | _blank | external-root | card: Blog |
| demos.libcna.com ↗ | `https://demos.libcna.com/` | primary | _blank | external-root | card: Demos |
| samples.libcna.com ↗ | `https://samples.libcna.com/` | primary | _blank | external-root | card: Samples |
| easygl.libcna.com ↗ | `https://easygl.libcna.com/` | secondary | _blank | external-root | card: EasyGL |
| meshcraft.libcna.com ↗ | `https://meshcraft.libcna.com/` | secondary | _blank | external-root | card: MeshCraft |
| metagl.libcna.com ↗ | `https://metagl.libcna.com/` | secondary | _blank | external-root | card: MetaGL |

### Cards / callouts

| Kind | Title | Words | CTAs |
|---|---|---:|---|
| card | CNA Bible | 12 | bible.libcna.com ↗ |
| card | CNA Book | 12 | book.libcna.com ↗ |
| card | Blog | 11 | blog.libcna.com ↗ |
| card | Demos | 10 | demos.libcna.com ↗ |
| card | Samples | 12 | samples.libcna.com ↗ |
| card | EasyGL | 7 | easygl.libcna.com ↗ |
| card | MeshCraft | 7 | meshcraft.libcna.com ↗ |
| card | MetaGL | 7 | metagl.libcna.com ↗ |
| callout |  | 15 |  |

## `contact.html`

**Title:** Contact - CNA

### Headings / sections

- h1 Get in Touch
-   h2 Project
-     h3 GitHub Repository
-     h3 Report an Issue
-     h3 Contribute
-     h3 GitHub Discussions
-     h3 cna-demo
-   h2 Video & Demos
-     h3 YouTube Channel
-     h3 Web Builds
-     h3 Android Builds
-   h2 Author & Contact
-     h3 Robert Vokac
-     h3 Author Contact
-   h2 Related Open-Source Projects
-     h3 FNA
-     h3 MonoGame
-     h3 SDL3
-     h3 bgfx

### Major blocks

| Kind | id | Heading | Words | Cards | CTAs | Images |
|---|---|---|---:|---:|---:|---:|
| page-header |  | Get in Touch | 26 | 0 | 0 | 0 |
| section |  | Project | 310 | 0 | 10 | 0 |

### CTAs / buttons

| Label | href | Role | target | Kind | Context |
|---|---|---|---|---|---|
| github.com/libcna/cna ↗ | `https://github.com/libcna/cna` | secondary | _blank | github-repo | section: Project |
| Open Issues ↗ | `https://github.com/libcna/cna/issues` | secondary | _blank | github-deep | section: Project |
| Pull Requests ↗ | `https://github.com/libcna/cna/pulls` | secondary | _blank | github-deep | section: Project |
| Discussions ↗ | `https://github.com/libcna/cna/discussions` | secondary | _blank | github-deep | section: Project |
| View Web Demos | `demos.html` | secondary |  | internal | section: Project |
| github.com/libcna ↗ | `https://github.com/libcna` | secondary | _blank | github-org | section: Project |
| fna-xna.github.io ↗ | `https://fna-xna.github.io/` | secondary | _blank | external-root | section: Project |
| monogame.net ↗ | `https://monogame.net/` | secondary | _blank | external-root | section: Project |
| libsdl.org ↗ | `https://libsdl.org/` | secondary | _blank | external-root | section: Project |
| bgfx docs ↗ | `https://bkaradzic.github.io/bgfx/` | secondary | _blank | external-deep | section: Project |

## All other pages (summary)

| Page | H | CTAs (primary) | Cards | Images | Tables | Code blocks | Words |
|---|---:|---:|---:|---:|---:|---:|---:|
| `404.html` | 2 | 0 (0) | 0 | 0 | 0 | 0 | 34 |
| `contribute.html` | 23 | 1 (1) | 15 | 0 | 1 | 5 | 1499 |
| `docs/3d-rendering.html` | 30 | 0 (0) | 6 | 0 | 6 | 21 | 3272 |
| `docs/audio.html` | 13 | 0 (0) | 2 | 0 | 6 | 5 | 1508 |
| `docs/building.html` | 28 | 0 (0) | 8 | 0 | 3 | 15 | 2832 |
| `docs/c-api.html` | 9 | 0 (0) | 1 | 0 | 2 | 3 | 946 |
| `docs/content-manager.html` | 21 | 0 (0) | 3 | 0 | 3 | 10 | 2072 |
| `docs/content-pipeline-xnb.html` | 9 | 0 (0) | 2 | 0 | 3 | 2 | 1319 |
| `docs/effects.html` | 20 | 0 (0) | 5 | 1 | 8 | 10 | 2018 |
| `docs/faq.html` | 1 | 0 (0) | 0 | 0 | 0 | 0 | 3451 |
| `docs/game-loop.html` | 24 | 0 (0) | 2 | 0 | 6 | 15 | 1948 |
| `docs/getting-started.html` | 15 | 0 (0) | 1 | 0 | 1 | 7 | 916 |
| `docs/graphics-state.html` | 34 | 0 (0) | 11 | 5 | 8 | 15 | 2417 |
| `docs/input.html` | 16 | 0 (0) | 3 | 0 | 8 | 7 | 1837 |
| `docs/math-types.html` | 29 | 0 (0) | 2 | 0 | 17 | 5 | 2737 |
| `docs/migration-from-monogame.html` | 14 | 0 (0) | 3 | 0 | 7 | 8 | 2003 |
| `docs/model-loading.html` | 15 | 0 (0) | 3 | 0 | 4 | 7 | 1381 |
| `docs/packed-vector.html` | 12 | 0 (0) | 2 | 0 | 4 | 4 | 1331 |
| `docs/platforms.html` | 15 | 0 (0) | 8 | 0 | 5 | 1 | 1982 |
| `docs/releases.html` | 7 | 0 (0) | 1 | 0 | 1 | 2 | 449 |
| `docs/render-targets.html` | 15 | 0 (0) | 4 | 0 | 4 | 9 | 1800 |
| `docs/rendering-backends.html` | 21 | 0 (0) | 15 | 0 | 11 | 3 | 3786 |
| `docs/roadmap.html` | 10 | 0 (0) | 1 | 0 | 2 | 0 | 1277 |
| `docs/runtime-renderer-selection.html` | 8 | 0 (0) | 2 | 0 | 1 | 4 | 580 |
| `docs/sensors.html` | 16 | 0 (0) | 3 | 0 | 5 | 3 | 1313 |
| `docs/shader-effects.html` | 17 | 0 (0) | 4 | 0 | 2 | 11 | 1683 |
| `docs/spritebatch.html` | 15 | 0 (0) | 2 | 0 | 6 | 5 | 1292 |
| `docs/storage.html` | 17 | 0 (0) | 4 | 0 | 5 | 4 | 1354 |
| `docs/tutorials/01-introduction.html` | 16 | 0 (0) | 2 | 0 | 2 | 4 | 1747 |
| `docs/tutorials/02-setup.html` | 20 | 0 (0) | 6 | 0 | 3 | 15 | 1527 |
| `docs/tutorials/03-first-window.html` | 12 | 0 (0) | 2 | 0 | 1 | 7 | 904 |
| `docs/tutorials/04-game-lifecycle.html` | 11 | 0 (0) | 2 | 0 | 0 | 10 | 1207 |
| `docs/tutorials/05-game-loop.html` | 10 | 0 (0) | 1 | 0 | 2 | 11 | 1009 |
| `docs/tutorials/06-first-shape.html` | 8 | 0 (0) | 1 | 0 | 0 | 6 | 831 |
| `docs/tutorials/07-colors.html` | 9 | 0 (0) | 1 | 0 | 1 | 13 | 972 |
| `docs/tutorials/08-textures.html` | 15 | 0 (0) | 1 | 0 | 1 | 13 | 909 |
| `docs/tutorials/09-spritefont.html` | 16 | 0 (0) | 1 | 0 | 0 | 12 | 1112 |
| `docs/tutorials/10-keyboard.html` | 10 | 0 (0) | 1 | 0 | 2 | 6 | 1021 |
| `docs/tutorials/100-shipping.html` | 11 | 0 (0) | 3 | 0 | 1 | 10 | 1337 |
| `docs/tutorials/101-renderer-capabilities.html` | 10 | 0 (0) | 4 | 0 | 3 | 4 | 1637 |
| `docs/tutorials/102-opengl-family.html` | 9 | 0 (0) | 4 | 0 | 3 | 2 | 1351 |
| `docs/tutorials/103-direct3d-windows.html` | 10 | 0 (0) | 4 | 0 | 2 | 4 | 1240 |
| `docs/tutorials/104-directx-ladder.html` | 9 | 0 (0) | 5 | 0 | 2 | 2 | 1494 |
| `docs/tutorials/105-browser-renderers.html` | 12 | 0 (0) | 4 | 0 | 4 | 2 | 1419 |
| `docs/tutorials/106-vector-renderers.html` | 7 | 0 (0) | 4 | 0 | 3 | 3 | 1456 |
| `docs/tutorials/107-cpu-renderers.html` | 14 | 0 (0) | 6 | 0 | 4 | 8 | 3200 |
| `docs/tutorials/108-fna3d.html` | 13 | 0 (0) | 5 | 0 | 4 | 5 | 2450 |
| `docs/tutorials/109-metal-macos.html` | 12 | 0 (0) | 5 | 0 | 2 | 3 | 2263 |
| `docs/tutorials/11-mouse.html` | 13 | 0 (0) | 1 | 0 | 1 | 12 | 1112 |
| `docs/tutorials/110-gltf-models.html` | 7 | 0 (0) | 3 | 0 | 2 | 2 | 848 |
| `docs/tutorials/111-cnj-pipeline.html` | 11 | 0 (0) | 3 | 0 | 7 | 9 | 2202 |
| `docs/tutorials/112-gltf-animation.html` | 9 | 0 (0) | 3 | 0 | 3 | 8 | 1611 |
| `docs/tutorials/113-morph-targets.html` | 7 | 0 (0) | 2 | 0 | 3 | 6 | 1383 |
| `docs/tutorials/114-pbr-materials.html` | 9 | 0 (0) | 5 | 0 | 5 | 5 | 1319 |
| `docs/tutorials/115-cnaext-overview.html` | 11 | 0 (0) | 4 | 0 | 4 | 6 | 1847 |
| `docs/tutorials/116-post-process-effects.html` | 10 | 0 (0) | 5 | 0 | 3 | 6 | 2078 |
| `docs/tutorials/117-devices-layer.html` | 9 | 0 (0) | 4 | 0 | 3 | 6 | 1743 |
| `docs/tutorials/118-dynamic-audio.html` | 10 | 0 (0) | 5 | 0 | 1 | 8 | 1412 |
| `docs/tutorials/119-3d-audio.html` | 11 | 0 (0) | 5 | 0 | 2 | 5 | 1320 |
| `docs/tutorials/12-moving-sprites.html` | 11 | 0 (0) | 1 | 0 | 1 | 11 | 1186 |
| `docs/tutorials/120-xact.html` | 15 | 0 (0) | 6 | 0 | 2 | 9 | 1612 |
| `docs/tutorials/121-video-playback.html` | 11 | 0 (0) | 5 | 0 | 1 | 10 | 1284 |
| `docs/tutorials/122-media-library.html` | 12 | 0 (0) | 7 | 0 | 2 | 9 | 1566 |
| `docs/tutorials/123-achievements.html` | 14 | 0 (0) | 8 | 0 | 2 | 11 | 1733 |
| `docs/tutorials/124-web-gotchas.html` | 7 | 0 (0) | 3 | 0 | 1 | 4 | 924 |
| `docs/tutorials/125-pixel-testing.html` | 10 | 0 (0) | 6 | 0 | 3 | 7 | 2130 |
| `docs/tutorials/126-multi-renderer-build.html` | 7 | 0 (0) | 2 | 0 | 0 | 3 | 475 |
| `docs/tutorials/127-platform-audio-selection.html` | 10 | 0 (0) | 2 | 0 | 1 | 5 | 417 |
| `docs/tutorials/128-compiled-xna-effects.html` | 7 | 0 (0) | 1 | 0 | 1 | 3 | 392 |
| `docs/tutorials/129-c-api-first-program.html` | 6 | 0 (0) | 2 | 0 | 0 | 3 | 603 |
| `docs/tutorials/13-sprite-sheets.html` | 10 | 0 (0) | 1 | 0 | 0 | 8 | 1295 |
| `docs/tutorials/14-sound-effects.html` | 11 | 0 (0) | 3 | 0 | 1 | 8 | 1127 |
| `docs/tutorials/15-background-music.html` | 13 | 0 (0) | 4 | 0 | 0 | 8 | 1245 |
| `docs/tutorials/16-collision-detection.html` | 8 | 0 (0) | 1 | 0 | 0 | 7 | 1234 |
| `docs/tutorials/17-camera-2d.html` | 8 | 0 (0) | 1 | 0 | 0 | 6 | 1090 |
| `docs/tutorials/18-game-states.html` | 8 | 0 (0) | 1 | 0 | 0 | 5 | 1015 |
| `docs/tutorials/19-save-load.html` | 11 | 0 (0) | 4 | 0 | 1 | 7 | 1231 |
| `docs/tutorials/20-build-run.html` | 10 | 0 (0) | 3 | 0 | 0 | 11 | 1104 |
| `docs/tutorials/21-spritebatch.html` | 15 | 0 (0) | 5 | 4 | 1 | 9 | 1245 |
| `docs/tutorials/22-blend-modes.html` | 12 | 0 (0) | 1 | 0 | 2 | 9 | 733 |
| `docs/tutorials/23-render-targets.html` | 7 | 0 (0) | 1 | 0 | 0 | 6 | 825 |
| `docs/tutorials/24-post-processing.html` | 8 | 0 (0) | 2 | 0 | 0 | 8 | 1233 |
| `docs/tutorials/25-sprite-sort-mode.html` | 12 | 0 (0) | 4 | 3 | 1 | 8 | 1105 |
| `docs/tutorials/26-tilemaps.html` | 9 | 0 (0) | 1 | 0 | 0 | 6 | 1676 |
| `docs/tutorials/27-parallax.html` | 8 | 0 (0) | 2 | 0 | 0 | 6 | 1136 |
| `docs/tutorials/28-particles-2d.html` | 7 | 0 (0) | 2 | 0 | 0 | 7 | 1361 |
| `docs/tutorials/29-ui-elements.html` | 8 | 0 (0) | 2 | 0 | 0 | 7 | 1500 |
| `docs/tutorials/30-gamepad.html` | 11 | 0 (0) | 2 | 0 | 1 | 8 | 1210 |
| `docs/tutorials/31-first-3d-triangle.html` | 9 | 0 (0) | 3 | 1 | 1 | 6 | 1083 |
| `docs/tutorials/32-basiceffect.html` | 12 | 0 (0) | 5 | 3 | 2 | 8 | 1318 |
| `docs/tutorials/33-matrices.html` | 11 | 0 (0) | 2 | 0 | 0 | 9 | 1184 |
| `docs/tutorials/34-camera-3d.html` | 9 | 0 (0) | 2 | 0 | 0 | 7 | 1348 |
| `docs/tutorials/35-model-loading.html` | 13 | 0 (0) | 6 | 0 | 2 | 9 | 1844 |
| `docs/tutorials/36-model-texturing.html` | 9 | 0 (0) | 2 | 0 | 0 | 6 | 1158 |
| `docs/tutorials/37-multiple-lights.html` | 8 | 0 (0) | 3 | 1 | 0 | 6 | 1304 |
| `docs/tutorials/38-vertex-buffers.html` | 10 | 0 (0) | 2 | 0 | 2 | 7 | 1356 |
| `docs/tutorials/39-depth-buffer.html` | 9 | 0 (0) | 2 | 0 | 1 | 7 | 1545 |
| `docs/tutorials/40-primitive-types.html` | 9 | 0 (0) | 4 | 3 | 1 | 4 | 1042 |
| `docs/tutorials/41-math-vectors.html` | 12 | 0 (0) | 1 | 0 | 0 | 11 | 878 |
| `docs/tutorials/42-matrix-ops.html` | 11 | 0 (0) | 1 | 0 | 0 | 10 | 721 |
| `docs/tutorials/43-quaternions.html` | 12 | 0 (0) | 1 | 0 | 0 | 9 | 854 |
| `docs/tutorials/44-bounding-volumes.html` | 9 | 0 (0) | 1 | 0 | 0 | 8 | 667 |
| `docs/tutorials/45-content-manager.html` | 12 | 0 (0) | 4 | 0 | 1 | 9 | 1455 |
| `docs/tutorials/46-content-reader.html` | 9 | 0 (0) | 3 | 0 | 0 | 6 | 829 |
| `docs/tutorials/47-game-component.html` | 7 | 0 (0) | 1 | 0 | 1 | 4 | 543 |
| `docs/tutorials/48-timestep.html` | 8 | 0 (0) | 1 | 0 | 1 | 5 | 740 |
| `docs/tutorials/49-touch-input.html` | 8 | 0 (0) | 2 | 0 | 1 | 6 | 760 |
| `docs/tutorials/50-accelerometer.html` | 8 | 0 (0) | 3 | 0 | 2 | 4 | 1009 |
| `docs/tutorials/51-custom-vertex.html` | 9 | 0 (0) | 1 | 0 | 2 | 5 | 695 |
| `docs/tutorials/52-custom-shaders.html` | 14 | 0 (0) | 4 | 0 | 2 | 13 | 2182 |
| `docs/tutorials/53-effect-parameter.html` | 12 | 0 (0) | 4 | 0 | 2 | 11 | 2117 |
| `docs/tutorials/54-alpha-test.html` | 9 | 0 (0) | 9 | 8 | 1 | 3 | 1764 |
| `docs/tutorials/55-dual-texture.html` | 8 | 0 (0) | 5 | 1 | 0 | 6 | 1768 |
| `docs/tutorials/56-environment-map.html` | 10 | 0 (0) | 5 | 3 | 1 | 7 | 1362 |
| `docs/tutorials/57-skinned-effect.html` | 9 | 0 (0) | 9 | 6 | 0 | 8 | 1783 |
| `docs/tutorials/58-normal-mapping.html` | 11 | 0 (0) | 4 | 0 | 0 | 8 | 2091 |
| `docs/tutorials/59-shadow-mapping.html` | 14 | 0 (0) | 5 | 0 | 0 | 13 | 2733 |
| `docs/tutorials/60-instancing.html` | 10 | 0 (0) | 2 | 0 | 2 | 6 | 2288 |
| `docs/tutorials/61-occlusion-query.html` | 8 | 0 (0) | 2 | 0 | 0 | 6 | 1494 |
| `docs/tutorials/62-mrt.html` | 9 | 0 (0) | 6 | 0 | 1 | 7 | 2245 |
| `docs/tutorials/63-stencil-buffer.html` | 9 | 0 (0) | 3 | 0 | 3 | 3 | 1457 |
| `docs/tutorials/64-cubemaps.html` | 10 | 0 (0) | 2 | 0 | 1 | 7 | 1586 |
| `docs/tutorials/65-msaa.html` | 12 | 0 (0) | 3 | 0 | 2 | 6 | 2153 |
| `docs/tutorials/66-bloom.html` | 10 | 0 (0) | 4 | 0 | 0 | 8 | 1436 |
| `docs/tutorials/67-deferred-rendering.html` | 10 | 0 (0) | 5 | 0 | 1 | 6 | 1757 |
| `docs/tutorials/68-terrain.html` | 9 | 0 (0) | 1 | 0 | 0 | 7 | 1243 |
| `docs/tutorials/69-water.html` | 10 | 0 (0) | 3 | 0 | 0 | 10 | 1401 |
| `docs/tutorials/70-procedural-geometry.html` | 7 | 0 (0) | 1 | 0 | 0 | 5 | 1081 |
| `docs/tutorials/71-memory-management.html` | 12 | 0 (0) | 1 | 0 | 1 | 6 | 1155 |
| `docs/tutorials/72-backend-selection.html` | 18 | 0 (0) | 7 | 0 | 8 | 4 | 2475 |
| `docs/tutorials/73-profiling.html` | 9 | 0 (0) | 1 | 0 | 1 | 4 | 1064 |
| `docs/tutorials/74-frustum-culling.html` | 9 | 0 (0) | 1 | 0 | 0 | 5 | 813 |
| `docs/tutorials/75-lod.html` | 8 | 0 (0) | 1 | 0 | 0 | 6 | 986 |
| `docs/tutorials/76-spatial-partitioning.html` | 9 | 0 (0) | 1 | 0 | 1 | 4 | 1050 |
| `docs/tutorials/77-async-loading.html` | 7 | 0 (0) | 1 | 0 | 0 | 3 | 922 |
| `docs/tutorials/78-multithreading.html` | 8 | 0 (0) | 1 | 0 | 1 | 5 | 1060 |
| `docs/tutorials/79-debugging.html` | 8 | 0 (0) | 1 | 0 | 0 | 4 | 771 |
| `docs/tutorials/80-cross-platform.html` | 11 | 0 (0) | 1 | 0 | 1 | 5 | 1068 |
| `docs/tutorials/81-emscripten.html` | 10 | 0 (0) | 2 | 0 | 0 | 6 | 1041 |
| `docs/tutorials/82-android.html` | 10 | 0 (0) | 3 | 0 | 0 | 9 | 731 |
| `docs/tutorials/83-migrate-monogame.html` | 10 | 0 (0) | 3 | 0 | 2 | 2 | 1085 |
| `docs/tutorials/84-migrate-xna.html` | 9 | 0 (0) | 1 | 0 | 0 | 1 | 1180 |
| `docs/tutorials/85-vulkan-backend.html` | 9 | 0 (0) | 1 | 0 | 0 | 5 | 886 |
| `docs/tutorials/86-bgfx-backend.html` | 7 | 0 (0) | 3 | 0 | 0 | 3 | 895 |
| `docs/tutorials/87-custom-backend.html` | 10 | 0 (0) | 4 | 0 | 0 | 3 | 1673 |
| `docs/tutorials/88-device-layer.html` | 11 | 0 (0) | 3 | 0 | 2 | 8 | 1810 |
| `docs/tutorials/89-sharp-runtime.html` | 13 | 0 (0) | 5 | 0 | 2 | 13 | 1817 |
| `docs/tutorials/90-easy-gl.html` | 7 | 0 (0) | 2 | 0 | 0 | 1 | 872 |
| `docs/tutorials/91-platformer.html` | 8 | 0 (0) | 1 | 0 | 0 | 6 | 992 |
| `docs/tutorials/92-top-down-rpg.html` | 8 | 0 (0) | 1 | 0 | 0 | 7 | 1021 |
| `docs/tutorials/93-fps-game.html` | 6 | 0 (0) | 1 | 0 | 0 | 5 | 1001 |
| `docs/tutorials/94-puzzle-game.html` | 7 | 0 (0) | 1 | 0 | 0 | 6 | 1004 |
| `docs/tutorials/95-speedy-blupi.html` | 7 | 0 (0) | 2 | 0 | 0 | 1 | 824 |
| `docs/tutorials/96-physics.html` | 7 | 0 (0) | 1 | 0 | 0 | 6 | 655 |
| `docs/tutorials/97-networking.html` | 14 | 0 (0) | 6 | 0 | 3 | 10 | 2119 |
| `docs/tutorials/98-localization.html` | 9 | 0 (0) | 1 | 0 | 0 | 8 | 907 |
| `docs/tutorials/99-unit-testing.html` | 7 | 0 (0) | 3 | 0 | 0 | 8 | 946 |
| `docs/verification.html` | 16 | 0 (0) | 14 | 8 | 5 | 2 | 2954 |
| `docs/video-playback.html` | 14 | 0 (0) | 5 | 0 | 4 | 6 | 1209 |
| `docs/vs-alternatives.html` | 12 | 0 (0) | 3 | 0 | 3 | 2 | 1372 |
| `docs/xna-compatibility.html` | 20 | 0 (0) | 10 | 0 | 3 | 0 | 3524 |
| `search.html` | 1 | 0 (0) | 0 | 0 | 0 | 0 | 2 |
