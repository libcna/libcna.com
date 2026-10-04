# R5 — cna-cs-samples: original XNA 4.0 C# run through CNA.NET (research facts)

Research date 2026-10-04. Read-only. All counts re-derived from committed content unless marked.
Abbreviations: CSS = `cna-cs-samples`, CCS = `cna-cs` (CNA.NET), CSM = `cna-samples` (C++ campaign),
CNA@T = `cna` read via git objects at `b0e97bb1bb876f9b3edd6f4ff1ef3067908ae8ac`.
Classes: **SRC** source fact · **BUILD** build fact · **RUN** runtime-qualified fact · **PLAT** platform-qualified fact · **COMPAT** compatibility/comparison result · **PLAN** future plan/not done.

## 0. Executive summary (15 lines)

1. CSS `samples/` holds **84 runnable Microsoft XNA GS 4.0 sample executables** (83 plan rows ✅, 1 row 🛑 Yacht) — `grep -vc '^#' samples/manifest.tsv` → 84; `grep -c '| ✅ |$' plan.md` → 83; `grep -c '| 🛑 |$' plan.md` → 1.
2. All 84 keep upstream sources **byte-identical** — `scripts/check-verbatim.sh` (diff -r vs `/rv/tmp/XNAGameStudio/Samples`, excl. Content/bin/obj) → `checked 84 sample(s), 0 failure(s)` (run 2026-10-04).
3. Every shipped `.xnb` is byte-identical to the C++ campaign's — `scripts/check-content.sh` → `2138 identical, 0 drifted, 0 sourced elsewhere`; plus 1358/1358 sha256 lines recorded in 77 `missing.md` files re-verified (loop in §2.3).
4. Desktop (Linux, private Xvfb, Mesa GLES 3.2 / OPENGLES3): **84/84 build Debug+Release and run** (requalify 2026-10-02, rerun on ABI 0.44.0 2026-10-03) — CCS `CAMPAIGN.md:486,898`; CNA@T `handoff.md:432`.
5. **26 of 84 pixel-equal to their C++ port** in the 2026-10-02 requalification (CNA@T `handoff.md:432-433`; artifact dir `/rv/tmp/cs-samples/requal-20261002d` no longer on disk).
6. Browser: **84/84 single-threaded** rows run in **headless** Chromium + SwiftShader WebGL2 (CCS `CAMPAIGN.md:95,633`); threaded bundles: 16-row gallery subset (CCS `CAMPAIGN.md:585`) + CSX-150 rerun of 2 programs. Interactive browser / GPU / audio **not qualified**.
7. Android: **84/84 build, run, draw on the x86_64 emulator**, 78 end on one Back (CCS `CAMPAIGN.md:102`); no physical device / ARM / audio.
8. Windows / macOS / iOS: **nothing run** (CNA@T `handoff.md:490-493`; CCS `docs/final-compatibility-audit.md:92-94`).
9. CSS `games/`: **85 main-table rows + 10 CSX-151 candidates = 95 investigated projects** (awk count, §1.2; README line 5-6 states the same), plus ~60 named blocked projects.
10. `games/manifest.tsv` (owner walk-through, 2026-10-03): **198 "run" entries → 193 played-ok, 1 runs-blank, 2 throw by design, 2 not run** (`grep -v '^#' games/manifest.tsv | awk -F'\t' '$1=="run"{split($11,a," ");print a[1]}' | sort | uniq -c`); CSX-151 later added 2 more running programs.
11. Of the games corpus, **8 rows are Microsoft-origin** (6 from the XNA GS sample archive: SAMPLE-075/097/100/103/106/152; 2 Microsoft GitHub WP titles); **≈188+2 third-party programs** ran (§1.3).
12. Overlap with C++: CSM plan has **91 ✅** (`git -C ../cna-samples show HEAD:plan.md` + awk); **83 of those 91 also run as original C#** (84 executables) — `comm -12` of the two id lists (§4).
13. The 8 C++-✅ rows without a running C# row: 004 (non-port), 071 Yacht (C# 🛑), and 085/086/087/094/101/107 completed in C++ on 2026-10-03, after the C# eligibility snapshot (no C# row yet).
14. Racing Game Kit (CSX-149): unchanged C#, zero-warning build, attract → menus → Advanced-track race on Linux at 1024x768; structural (not pixel) match to C++ port; real-XNA oracle impossible under Wine (GFWL). Browser threaded = attract only (~0.65 fps); Android emulator = attract.
15. **No C#/.NET build is publicly hosted**: `git -C ../samples.libcna.com ls-files | grep -ciE '_framework|dotnet\.|\.dll$|blazor'` → 0 (site hosts 90 C++ `*_cna_samples.wasm`).

## 1. Repository state and inventory

### 1.1 Repo heads (recorded 2026-10-04)

| Repo | Branch | HEAD (full) | Commit date | Dirty |
|---|---|---|---|---|
| cna-cs-samples | develop (= origin/develop) | `1e6d7631ae520ae087a461ebf9d268b1babe7587` | 2026-10-04T13:20:39+02:00 | clean (0) |
| cna-cs | develop (= origin/develop) | `860f92cca30f0862f6eabf7970269ce49af90536` | 2026-10-04T13:20:39+02:00 | clean (0) |
| cna-samples | develop | `10e3c35b5fa6fcdf6680a79ffd29cee4adbdb798` | 2026-10-04T19:32:32+02:00 | dirty: `M tools/run_renderer_matrix.py`, `?? matrix-results/` (not used; facts from `git show HEAD:`) |
| cna | samples (working tree NOT used) | read at T = `b0e97bb1bb876f9b3edd6f4ff1ef3067908ae8ac` (2026-10-04T13:20:39+02:00, "docs: point release links at libcna") | — | working tree dirty (2 M, 1 ??) — ignored |
| samples.libcna.com | main (= origin/main) | `b3939de558fdb0a41f0aaa6599b7051b2680a6f7` | 2026-10-03T21:06:05+02:00 | clean |
| demos.libcna.com | — | `fa6d0bcf9d8890778851786811f7c350bcc9820d` | 2026-09-30 | — |

Command: `for r in cna-cs-samples cna-cs cna-samples cna; do git -C $r rev-parse --abbrev-ref HEAD; git -C $r log -1 --format='%H %cI %s'; git -C $r status --porcelain; done`.

### 1.2 What is in CSS (SRC)

| Item | Count | Command / evidence |
|---|---:|---|
| Tracked files | 4103 (samples 3777, games 288, scripts 24) | `git ls-files \| awk -F/ '{print $1}' \| sort \| uniq -c` |
| `samples/` directories | 85 (84 runnable + `Yacht` record-only) | `git ls-files samples \| awk -F/ 'NF>2{print $2}' \| sort -u \| wc -l` |
| `samples/manifest.tsv` rows | 84 | `grep -vc '^#' samples/manifest.tsv` |
| plan.md rows (CSSAMPLE-nnn) | 84 rows: 83 ✅, 1 🛑 (CSSAMPLE-071 Yacht) | `grep -c '\| ✅ \|$' plan.md`; plan.md:57-64; plan.md:303 |
| Executables behind ✅ rows | 84 (CSSAMPLE-020 has two: TransformedCollision, TransformedCollisionTest) | plan.md:31-32, 254 |
| Glue `.csproj` at `samples/<X>/` | 98 = 84 product + 14 library projects | `git ls-files samples \| awk -F/ 'NF==3 && /\.csproj$/' \| wc -l` |
| Products by profile | 28 HiDef, 56 Reach | grep `<XnaProfile>` over the 84 product csproj |
| Phone-only titles via generated host (`<CnaPhoneGame>`) | 13 (Bounce, PathDrawing, RimLighting, CatapultWars, Graphics3D, DynamicMenu, MarbleMaze, AccelerometerSample, SoundAndMusic, UISample, NinjAcademy, HoneycombRush, SoccerPitch); 12 of the glue projects reference CNA.PhoneCompat | `grep -l CnaPhoneGame samples/*/*.csproj`; mechanism samples/Directory.Build.targets:46-87 |
| `missing.md` files | 85 (84 runnable + Yacht) | `git ls-files 'samples/*/missing.md' \| wc -l` |
| `games/` main README table | **85 rows** | `awk '/^\| Game \|/{t=1;next} /^\|---/{next} /^$/{t=0} t&&/^\|/' games/README.md \| wc -l` |
| `games/` CSX-151 table | **10 rows** (2 run, 8 stopped for non-XNA reasons) | games/README.md:26-53 |
| `games/` blocked list ("Tried and not running here") | 48 bullets naming 60 bold entries (some entries are a sub-part, e.g. Asteria's full game, The Lost Levels' game project) | games/README.md:235-374 |
| `games/manifest.tsv` (2026-10-03) | 311 rows: 198 `run`, 94 `checkout`, 19 `content` | `grep -v '^#' games/manifest.tsv \| cut -f1 \| sort \| uniq -c` |
| `games/` glue `.csproj` | 272 (not in `CnaCsSamples.sln`; sln has 122 projects, 97 under samples) | `git ls-files games \| grep -c '\.csproj$'`; `grep -c '^Project(' CnaCsSamples.sln` |

Note: games/README.md:5-7 itself says "85 external application/project rows plus the ten deliberately bounded final candidates below: 95 documented project investigations". CNA@T `handoff.md:87` and its §14 say "84 rows" (stale by one). Use **85 + 10 = 95**.

### 1.3 Microsoft vs third-party (SRC)

| Group | Projects/rows | Executables | Evidence |
|---|---:|---:|---|
| Microsoft XNA GS 4.0 sample collection, `samples/` | 83 rows ✅ (+ Yacht 🛑) | 84 | plan.md:235-320 |
| Microsoft XNA GS 4.0 sample collection, in `games/` | 6 rows: Racing Game Kit (SAMPLE-152), Network Prediction (100), Peer to Peer (103), Network Game State Management (075), Memory Madness lab (097), Saving Embedded Images (106) | 6 | games/README.md:81-86; manifest rows |
| Other Microsoft-published XNA titles in `games/` | 2: Moto Trial Racer (`microsoft/moto-trial-racer-wp`), Solitaire (`microsoft/solitaire-wp`) | 2 | games/README.md:63-64 |
| **Total distinct XNA GS sample-archive SAMPLE ids running as C# (Linux)** | **89** (83 + 6) of the 153 upstream directories in the CSM universe | 90 | union of the above |
| Third-party (GitHub, books, courses, engines) in `games/` | 77 main-table rows + 2 CSX-151 = **79 rows** | **190 executed** (188 from manifest + Babsang + Ronald): 185+2 played-ok, 1 runs but blank (Petzold XnaWebBitmap, network fetch), 2 throw `AccelerometerFailedException` by design (Apress Ch4 Accelerometer, Pong Demo06) | manifest: 198 run − 8 Microsoft − 1 dependency (FlightSim/Particle3DSample, Microsoft code) − 1 not run (Rabbit Apocalypse, winmm.dll) = 188 |

Largest third-party collections (programs, from manifest `run` rows per readme-row): Petzold *Programming Windows Phone 7* 48 (+ PhreeCell = 49), Apress *Windows Phone 7 Game Development* 19, *2D Graphics Programming for Games* 14, Windows Phone Pong demos 8, petriw XNA Shader Programming 7, willcraftia TestXna 7, Red Badger XPF 4, *XNA 4.0 Game Development by Example* 4, *Windows Phone 7 Recipes* 3, ExEn 3, AlexMeuer course 3, Xen starter kits 2, Asteria demos 2; single-program rows: 72 (incl. cocos2d-x-for-XNA tests, Project Mercury, Racing etc.). Command: `grep -v '^#' games/manifest.tsv | awk -F'\t' '$1=="run"{print $2}' | sort | uniq -c | sort -rn`.

Manifest input modes: 109 desktop, 88 phone (mouse = finger, Escape = Back), 1 desktop + WinForms compat (Racing). (`awk -F'\t' '$1=="run"{print $7}' | sort | uniq -c`)

## 2. Compile / run / verbatim / comparison

### 2.1 Microsoft samples in `samples/`

| Claim | Number | Class | Evidence |
|---|---|---|---|
| Build Debug and Release | 84/84 | BUILD | CCS@860f92c `CAMPAIGN.md:898` ("84/84 build (Debug and Release) and run", 2026-10-02, `requal-20261002`); `CAMPAIGN.md:486` (rerun on ABI 0.44.0 2026-10-03, "every build, run and exit status the 2026-10-02 baseline's"); rules.md:131 (DoD item 4) |
| Run + capture on Linux | 84/84 | RUN, platform = Linux desktop **on a private Xvfb** (rules.md:133-135; scripts/capture-sample.sh:69), renderer OPENGLES3/EasyGL on Mesa (llvmpipe) GLES 3.2 | same; plan.md:178 |
| Exit through own path | 78/84 one key; 6 need menu input (ReachGraphicsDemo, GameStateManagement, ClientServerSample, ShipGame, RolePlayingGame, NetRumble) | RUN | CCS `CAMPAIGN.md:889-892, 900` |
| Source deviations | **0** in all 84 (`missing.md` "Source deviations: None" in 84/84) | SRC | `scripts/check-verbatim.sh` → `checked 84 sample(s), 0 failure(s)` (executed 2026-10-04; diff -r, excludes Content/bin/obj: scripts/check-verbatim.sh:44) |
| Hash manifests | 77/84 `missing.md` carry sha256 lists; **1358/1358 hashes match** committed files; 7 rows (Bounce, ColorReplacement, InputSequence, ParticleSample, PathDrawing, SpriteEffects, WaypointSample) rely on diff -r only | SRC | loop: `grep -E '^[0-9a-f]{64}  ' samples/*/missing.md` then `sha256sum` per path |
| Content | 2138 `.xnb`/content files byte-identical to CSM ports' Content | SRC | `scripts/check-content.sh` → `2138 identical, 0 drifted, 0 sourced elsewhere` |
| Project-level adaptation only | `Directory.Build.props`/`.targets` (net8.0, WinExe, ImplicitUsings off, GenerateAssemblyInfo false, `.resx` LogicalName, generated phone host, `CnaWindowsPath` symlinks); 2 rows define `WINDOWS` instead of `WINDOWS_PHONE` (GesturesSample, Orientation — "Deviation" section, project file only) | SRC | samples/Directory.Build.props:13-47; samples/Directory.Build.targets:34-148 |
| Compared with C++ port | 84/84 measured by `scripts/requalify.sh`; **26 pixel-equal** (2026-10-02d run) | COMPAT | CNA@T `handoff.md:428-433`; NEXT.md:159-206 (first 30 rows: 11 at 0.00%), NEXT.md:21-84 (54 more rows; 16 entries cite "0 px", some vs the C++ *start* frame or HUD only). Non-zero diffs explained as animation phase, seeded randomness, older retained C++ binaries, C++ phone-capture window offset (NEXT.md:200-206) |
| Compared with an original XNA frame | 4 rows: AccelerometerSample **0 px**/384 000, DynamicMenu **0 px**/384 000, Graphics3D 35 px/384 000, RimLighting 0.40% | COMPAT | samples/AccelerometerSample/missing.md:7-8; samples/DynamicMenu/missing.md:5; samples/Graphics3D/missing.md:5; samples/RimLighting/missing.md:5 |
| Known XNA divergence | InverseKinematics: 2.36% is CNA's avatar, "which XNA on Windows and the older C++ binary do not draw" | COMPAT | NEXT.md:56 |

### 2.2 Games (`games/`)

| Claim | Number | Class | Evidence |
|---|---|---|---|
| Source handling | Game `.cs` are **not checked in**; glue compiles the game's own project's file list from an external checkout (`GameRoot`) at a recorded commit | SRC | games/README.md:18-24; e.g. games/MissileCommand/MissileCommand.csproj |
| Verbatim check | **No hash manifest for games.** Measured now: 78 git checkouts referenced by manifest are at their recorded commit (78/78 HEAD match); 77 have no tracked-file changes, 1 (Speedy Blupi, owner's repo) shows only an FNA submodule pointer change; 6 Microsoft snapshot dirs are not git repos (unverifiable). CSX-151 checkouts (Babsang `2d5ce0b63312`, Ronald `60bc554b324a`) clean | SRC (measured 2026-10-04, not at run time) | loop `git -C <checkout> status --porcelain --untracked-files=no` and `rev-parse HEAD` vs manifest col 3 |
| Recorded non-source adaptations | files a repo does not ship compiled without (Reflexio and 2DCamExample `AssemblyInfo.cs`), Windows-path symlinks (`CnaWindowsPath`), case-insensitive name resolution, Racing opt-in `CNA.WindowsFormsCompat`, Forge run 5 dirs below Assets, SKraft data copied | SRC | games/README.md:110, 133, 81, 91, 90 |
| Content substitutions (not official pipeline output) | labelled stand-ins for WMA/MP3 songs, MP3 sounds, WMV videos (Resonance, Kosmic Warz, Enceladus silent 5 s tracks, Super Mario World, Sonic 3, NeonVectorShooter, Heroes of Rock 66 sounds, Kittens & Kobolds, ExEn CatGirls, GearsVge, Playing in Traffic videos); one font substitution (Ronald the Snake: Liberation Serif for Palatino Linotype) | SRC | games/README.md:37, 67-77, 92, 95, 117, 121, 136, 141, 229-233 |
| Desktop runs (owner walk-through) | 198 entries: 193 played-ok, 1 played (blank), 2 shown (throw), 2 not | RUN, Linux desktop; display/GPU of the owner's walk-through **not recorded** | games/manifest.tsv:2-4 + status col; commit d11f26b "the walk-through complete: all 198 programs played by the owner" |
| CSX-151 additions | Project Babsang, Ronald the Snake run unchanged (Linux) | RUN | games/README.md:36-37; evidence `/rv/tmp/cs-samples/final-sweep-20261004/` (present) |
| Compared with XNA 4.0 under Wine | 7 rows / 8 programs: Speedy Blupi title 255 px (save numbers), Rookie Drivers 0.24%, XNASidescroller 8 px/480 000, Dominó Tropical 0.32% (10% fuzz), Asteria lighting 2/300 000 px, Thieves Like Us 0/384 000, willcraftia LiSPSM "matches" + TerrainDemo "draws the same" | COMPAT | games/README.md:57, 58, 65, 68, 103, 113, 130 |
| Other oracles | LilyPath vs XNA-rendered README image 2 281/129 600 px @10%; MP3Sharp audio RMS diff 20 vs signal 9 500 vs ffmpeg decode | COMPAT | games/README.md:129, 127 |
| No XNA frame obtainable | Zombie Smashers X, Virulent (XNA exe crashes under Wine), Racing (GFWL) | COMPAT (negative) | games/README.md:62, 66, 81 |

## 3. Platform evidence

| Platform | `samples/` (84 executables) | `games/` | Exact mode | Evidence | Class |
|---|---|---|---|---|---|
| Linux desktop | 84/84 build+run+capture; 26 pixel-equal to C++ | 198-entry owner walk-through (193 ok) + 2 CSX-151 | samples: private Xvfb (virtual X server), Mesa llvmpipe GLES 3.2; games: owner-run (display not recorded) | §2 | RUN/PLAT |
| Browser, single-threaded | **84/84** in one run (`browser-requal-20261002-st`, 2026-10-02); first pass 77/84, 7 fixed in CCS/CNA/generator | ≥ 53 programs named as reaching ≥ first screen (lower bound by enumeration of README paragraphs: 24/25 first two batches incl. threaded, 5 Microsoft, 4 GitHub, 18 of 2026-10-03, TerrainDemo after CSX-145, Gemstone Hunter after CSX-144). Named failures: Playing in Traffic (video), Forge sample (UDP), TiledTerrainDemo (`Rgba64` needs EXT_texture_norm16), MDTerrainDemo (.NET 11 RC1 thread-pool fault). Partial: Saving Embedded Images blocking `Guide.EndShowMessageBox`; Memory Madness round not re-run in browser | **headless** Chromium (Chrome for Testing headless shell 151.0.7922.34), SwiftShader WebGL2, .NET 11 RC1 browser-wasm, Emscripten 6.0.3 | CCS `CAMPAIGN.md:95, 627-636, 876-885`; CNA@T `handoff.md:438-477`; games/README.md:143-208 | PLAT (headless only) |
| Browser, threaded (`--threads`) | 16 representative gallery rows pass (2026-10-02); CSX-150 (2026-10-04): AimingSample held-key movement + clean Escape | Enceladus (save slots), HeliumBiker (CONNECT), Resonance (plays arena; CSX-150 rerun), Missile Command, SKraft (menu), Racing (attract only, ~0.65 fps, menus never register a press); NGSM Single Player stops on "Loading.." | headless Chromium/SwiftShader, COOP/COEP, WebGL proxied to page thread | CCS `CAMPAIGN.md:585-586, 175, 177`; games/README.md:158-179; evidence `/rv/tmp/cs-samples/final-threaded-20261004/` (present) | PLAT; "threaded requalification of the gallery" explicitly **not done** (CNA@T `handoff.md:476-477`) |
| Android | **84/84** build, run, draw (2026-10-02, CNA `ffb82bc0d`); 78 end on one Back tap; pause/resume, relaunch, touch exercised | ≥ 50 programs named (15/16 + 9/9 + 5 Microsoft + 20 of 2026-10-03 + Gemstone Hunter). Named failures: Playing in Traffic (video), NGSM Single Player stuck on Loading (Mono `Thread.Join`) | **x86_64 emulator** only (AVD Medium_Phone, API 35, `-no-window -no-audio`, `swiftshader_indirect`), NDK 29, .NET 11 android workload | CCS `CAMPAIGN.md:102, 887-892, 1130-1157`; CNA@T `handoff.md:479-488`; games/README.md:147-156, 180-188, 209-213 | PLAT (emulator only; no physical device, no ARM, audio not heard) |
| Windows | not run | not run (Wine runs are XNA-oracle runs, not CNA-on-Windows) | — | CNA@T `handoff.md:490-493`; CCS `docs/final-compatibility-audit.md:92` | PLAN |
| macOS / iOS | not run | not run | — | CCS `docs/final-compatibility-audit.md:93-94` | PLAN |

Retained artifacts caveat: the 84-row desktop/browser/Android requalification directories cited in docs (`requal-20261002d`, `browser-requal-20261002-st`, `android-requal-20261001`, `requalify-0.44`, per-row `CSSAMPLE-*` evidence) are **no longer on disk**; `/rv/tmp/cs-samples/` now holds only 18 `final-*` dirs (`ls /rv/tmp/cs-samples`). The corpus-wide platform numbers therefore rest on the committed ledgers (CCS `CAMPAIGN.md`, CNA@T `handoff.md`), not on inspectable artifacts.

## 4. Overlap with the C++ campaign

| Set | Count | Command |
|---|---:|---|
| CSM `plan.md` rows (SAMPLE-001..153) | 153 | `git -C ../cna-samples show HEAD:plan.md \| grep -cE '^\| SAMPLE-[0-9]+ \|'` |
| CSM ✅ (complete) | **91** (status mix: 91 ✅, 49 🗑, 8 ⏸, 3 ⛔, 1 ↗, 1 🟡) | `... \| awk -F'\|' '/^\| SAMPLE-[0-9]+ \|/{st=$(NF-1); gsub(/^ +\| +$/,"",st); print st}' \| sort \| uniq -c` |
| CSS ✅ rows | 83 | `grep -oE "^\| CSSAMPLE-[0-9]+ \|.*\| ✅ \|$" plan.md \| grep -oE "[0-9]+$"`-style id extraction |
| **∩ (C++ ✅ and original C# runs)** | **83 rows = 84 executables** | `comm -12 <(cpp ids) <(cs ids) \| wc -l` → 83; C#-✅-but-not-C++-✅ → 0 |
| C++ ✅ without a C# run | 8: SAMPLE-004 StockEffects (CSM calls it a "completed Content Pipeline demonstration"; excluded as non-port, plan.md:26,326), 071 Yacht (C# 🛑, samples/Yacht/missing.md:5-24), **085, 086, 087, 094, 101 (avatar samples), 107 TiltPerspective** — all completed in C++ on 2026-10-03 (CSM commits 5c7f151, 672a889, cb3891f, d4da766, df673b5, 0e8c8c9), after CSS's 2026-10-01 eligibility snapshot | in-memory re-run of `scripts/check-eligibility.sh` logic → "derived eligible 90; plan rows 84; newly eligible 085 086 087 094 101 107" |
| Microsoft samples running as C# but NOT C++ ✅ | 6: 075 (C++ ⛔), 097/100/103/106 (C++ ⏸), 152 Racing (C++ ↗ separate plan) | games/README.md:81-86 |

Evidence-safe statement: **83 of the 91 rows the C++ campaign marks complete also run as original, unmodified C# through CNA.NET (84 executables)**; counting only real game/sample ports (excluding SAMPLE-004), 83 of 90. Against the published gallery as it stands now (samples.libcna.com@b3939de, 90 playable C++ web entries), 82 have a running C# counterpart; the 2026-10-02 `gallery-inventory.md` figure "82 of 84" predates 6 new avatar/tilt entries (`comm` of site dirs vs `samples/` dirs: missing C# = AvatarAnimationBlending, AvatarMultipleAnimations, AvatarShadows, CustomAvatarAnimation, ObjectPlacementOnAvatar, PerformanceUtility, TiltPerspective; plus Yacht).

## 5. Racing Game Kit (C#)

| Aspect | Fact | Class | Evidence |
|---|---|---|---|
| Source | `/rv/tmp/XNAGameStudio/Samples/XNA-4-Racing-Game-Kit-master/...`, unchanged; "byte-identical to cna-samples SAMPLE-152" | SRC | games/README.md:81; CNA@T handoff.md §16 |
| Content | authentic XNA 4.0 build from former Win7 VM (339 `.xnb`, XACT, tracks) | SRC | games/README.md:81 |
| Fixes it required | CCS CSX-113 (dir case), CSX-114 (opt-in WinForms compat: `Form.FromHandle`, `MessageBox`), CNA FX-142 (centroid link), CSX-116 (browser threads) | SRC | games/README.md:81; CCS CAMPAIGN.md:86 |
| Linux desktop (CSX-149, 2026-10-04) | zero-warning build vs CNA.NET `55ecb16`; on CNA `16dce8d5a`/C ABI 0.44.0 ran attract → main menu → car selection → Advanced track → race (lap 1/3) at 1024x768 windowed | RUN | CCS CAMPAIGN.md:176; artifacts present: `/rv/tmp/cs-samples/final-racing-differential-20261004/cna-net/01..06*.png` (06-race.png verified visually: lap HUD, speedometer, Advanced times) |
| vs C++ port | C++ port on CNA OPENGL33 ran the same six stages; **structural, not pixel-identity** match (camera/time differ) | COMPAT | same dir `cna-cpp/`; CNA@T handoff.md §16 |
| vs real XNA | authentic `RacingGame.exe` under Wine fails: missing `XnaLiveProxy.exe`, then GFWL initialization failure (`xna-wine/run.log` ends in unhandled exception) | COMPAT (oracle unavailable) | `xna-wine/run.log`, `missing-proxy.log` |
| Input caveat | Space must be held 2-3 s (slow polling under llvmpipe) | RUN | games/README.md:81 |
| Browser | single-threaded: refuses `Thread.Start`; threaded headless Chromium: attract mode only, ~0.65 fps; menus never see a press (CSX-148 classified as platform limitation) | PLAT | games/README.md:153-167; CCS CAMPAIGN.md:175 |
| Android | x86_64 emulator: attract mode | PLAT | games/README.md:155-156 |
| Public hosting | samples.libcna.com `RacingGame.html` is informational; playable bundle withheld (no redistribution grant); page text says the C# route "has been exercised on desktop, Web and Android" | SRC | samples.libcna.com@b3939de README.md:75-78, RacingGame.html:27 |
| Audibility | not qualified | PLAN | CNA@T handoff.md §16 |

## 6. Known failures / limitations, grouped by cause

**A. Microsoft gallery (from `missing.md`, plan.md)**

| Cause | Rows | Evidence |
|---|---|---|
| Silverlight WCF client (generated proxy uses configuration-name constructors + `ServiceReferences.ClientConfig`) | Yacht (CSSAMPLE-071) 🛑 owner decision; 4 build errors, all in generated `Reference.cs` | samples/Yacht/missing.md:5-39 |
| No C++ port ⇒ not eligible | PerformanceUtility (SAMPLE-104, C++ 🟡) | gallery-inventory.md:56 |
| Behaviour not driven (no input harness at the time; single frame compared) | Aiming, Audio3D (3D audio), ChaseAndEvade, ColorReplacement, Flocking, FuzzyLogic, Gestures (all gestures), InputReporter, InputSequence, Localization (other cultures), Particle, PathDrawing, Pathfinding, PerPixelCollision, Primitives3D (other primitives), RectangleCollision, SafeArea, SnowShovel, SpriteEffects, SpriteSheet, TouchThumbsticks, TransformedCollision, Waypoint | "## Not verified" sections, 31 files |
| Hardware absent on desktop | gamepad (most rows), accelerometer (Accelerometer, Bounce), microphone (MicrophoneEcho), orientation change (Orientation) | same |
| Exit only via gamepad/phone Back | AccelerometerSample, PathDrawing, TouchThumbsticks, Orientation, Gestures, Pathfinding (later: Escape = Back for phone rows, CSX-095, NEXT.md:86-91) | same |
| Audio not heard (captures play no sound) | e.g. SnowShovel `plink.xnb` | samples/SnowShovel/missing.md |
| Documentation staleness (not runtime failures) | 21 `missing.md` still say "No browser result. No .NET route to CNA's WEBGL2 backend exists" and plan.md:183-185 lists browser builds as out of scope, although CSX-062/063 later ran 84/84 in headless Chromium; TransformedCollisionTest's missing.md says no C++ comparison although NEXT.md:197 records 0.00%; README/plan still name `../cnanext` | `grep -l 'No browser result' samples/*/missing.md \| wc -l` → 21 |

**B. Games corpus (games/README.md:235-379 and CSX-151 table)**

| Cause | Examples |
|---|---|
| Windows Forms / WPF / System.Xaml host | Minor Destruction, Diseased Toast, Mannux, DwarfCorp, EvoNet, Almirante, Kodu Game Lab, XNALara, The Lost Levels (game), Asteria full game, SeedWorld (clipboard), Engine Nine (CSX-151) |
| Win32 P/Invoke | Divine Right (Kernel32), Rabbit Apocalypse (`winmm.dll joyGetPos`), YCPU, Tactile Engine, Zelda Oracle & AutonomousCar (x86 `SetWindowLong` hook) |
| Silverlight / phone XAML | Astro Flare Rampage, Nu Pogodi!, Pixel Blast (CSX-151), Yacht |
| Missing source/content/libraries in published repo | StarWarrior, Space Conquest, infinecraft, Grey Infection, Great Paper Adventure, Expanze, Mythology, Isosurface, Quarx, SuperHorrorFactory, DrunkiBoy, Pokémon Azure (Lua), Bamboozled, Voodoo Boy, Hunted (CSX-151) |
| Commercial/Windows fonts not shipped | Second Realipony, Eva Frontier, Flux, Sleepwalker, Voxeliq, BulletXNA demos, xTile/XNAVERGE/Azmyth, TestBench1, Rugby League, Asteroids, PACMAN, Shooter, Drumkit XNA (Segoe WP) |
| Dead services / external DB | Samurai (AppHarbor server), MunchKlone (MySQL, CSX-151) |
| Not XNA 4.0 / MonoGame | Medicraft, Old School Adventure, Project Heist, Adventure Time, Squared (FNA), BitSits games/AngryTanks/Flotilla/XNA Street Fighter (3.1), Infiniminer (3.0) |
| Other | Snails (published source builds nowhere), Shading (Xbox-only shader), Design Patterns Game (21 `Game` objects; CNA runs one per process), Jxqy HD (commercial data) |
| Runtime limits in running games | Heroes of Rock stops at `PerformanceCounter` (`PlatformNotSupportedException`) after menu; GearsVge ends with `Thread.Abort` PNSE (.NET 5+); Project Mercury Demo2 overruns its own vertex array (as XNA would); XnaWebBitmap blank (web fetch); XnaTapToBrowse/XnaLocation need phone services; accelerometer samples throw/stay still without a sensor; HeliumBiker/Zombie Smashers/Playing in Traffic/Super Smash Polls wait for Wiimote/Xbox gamepad |
| Browser-specific | video (no backend), UDP (Forge), `Rgba64` without EXT_texture_norm16, .NET 11 RC1 thread-start fault (upstream, owner: don't pursue), blocking `Guide.End*` in single-threaded page, slow proxied WebGL in threaded bundles (CSX-148) |
| Android-specific | Mono `Thread.Join` ignores SynchronizationContext (NGSM loading), video refusal |

## 7. Public hosting

- **No C# / CNA.NET build is publicly hosted.** samples.libcna.com@b3939de tracks 90 `*_cna_samples.wasm` (C++ Emscripten ports) and 0 .NET runtime files (`git ls-files | grep -ciE '_framework|dotnet\.|\.dll$|blazor'` → 0); demos.libcna.com@fa6d0bc likewise 0. CSS browser bundles exist only locally under gitignored `build-consumer/browser/` (CSS .gitignore:55). CCS CSX-154 guide states no official binaries or packages exist yet (CCS CAMPAIGN.md:181).
- The C# route is only **described** publicly: samples.libcna.com README.md:66-73 and index.html:37-40 ("runs nearly all of the same samples from their original, unchanged C# source on the Web, …"), RacingGame.html:27. Note "the Web" there means headless-Chromium evidence only.
- Source is public on GitHub (`libcna/cna-cs-samples`, `develop` = origin/develop at `1e6d763`).

## 8. Evidence-safe public wording (draft)

> The CNA.NET sample collection runs Microsoft's original XNA Game Studio 4.0 C# samples on CNA without porting them: 84 sample executables build and run on Linux from upstream source that a checker verifies byte-for-byte (`check-verbatim.sh`: 84 checked, 0 differences), with all 2,138 compiled content files identical to official XNA pipeline output. Everything that adapts them lives in project files and opt-in compatibility assemblies, never in the samples' `.cs` files. In the October 2026 requalification all 84 also built and ran in headless Chromium (WebGL2 via SwiftShader) and on an x86_64 Android emulator; 26 of them rendered pixel-identical to their C++ ports. 83 of the 91 samples completed by the C++ port campaign therefore also run as unmodified C#. Beyond Microsoft's samples, 95 third-party and Microsoft XNA 4.0 projects were investigated; about 190 programs from 79 third-party projects — including Petzold's Windows Phone 7 samples, *XNA 4.0 Game Development by Example*, cocos2d-x for XNA's tests, Project Mercury and the Xen starter kits — plus the XNA 4.0 Racing Game Kit ran unchanged on the Linux desktop. Interactive browsers, GPU-accelerated browsers, physical Android devices, Windows, macOS and iOS have not been tested.

Wording guardrails: say "headless Chromium" and "Android emulator", never "browsers"/"Android devices" unqualified; say "run" for games (owner walk-through), not "pixel-verified"; Racing is "plays a race on Linux; attract mode only in the threaded browser build and on the emulator"; do not cite the "82 of 84 gallery" figure without its 2026-10-02 date (gallery now has 90 entries).
