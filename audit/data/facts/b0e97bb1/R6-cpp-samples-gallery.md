# R6 — C++ XNA sample campaign (cna-samples), samples.libcna.com gallery, libcna.com coverage

## Executive summary (read this first)

1. **91 complete is correct**: `cna-samples` `plan.md` has 153 `SAMPLE-nnn` rows; status column = 91 ✅, 49 🗑, 8 ⏸, 3 ⛔, 1 🟡, 1 ↗ (source fact, recounted).
2. **CORRECTION to the brief: Racing Game is NOT one of the 91.** SAMPLE-152 Racing is ↗ ("separate plan"), not ✅. The 91 ✅ include SAMPLE-004 StockEffects (tool only), SAMPLE-062 NetRumble and SAMPLE-091 ClientServer (native-only by owner scope). None of the three has a browser build.
3. The gallery *also* says "91", but it counts something different: 91 gallery entries = 90 playable bundles + 1 informational Racing page. The two 91s are a coincidence. Do not merge them into "Racing is the 91st port".
4. The 90 playable bundles come from 88 ✅ rows (SAMPLE-020 ships 2 programs, so 89 bundles) plus SAMPLE-104 Performance Utility, a 🟡 partial release with browser networking missing.
5. Since the libcna.com pin (4da98a0, 87 ✅): six rows became ✅ (085, 086, 087, 094, 101, 107). Two rows were downgraded: 068 ✅→⛔ and 104 ✅→🟡. All 49 🛑 rows and 14 ⛔ rows were re-decided: 49 🗑, 3 ⛔, 8 ⏸.
6. The gallery grew from 40 bundles (736b8aa, 2026-09-20) to 90 bundles + Racing page (b3939de, 2026-10-03).
7. Relevant XNA 4.0 C# programs still incomplete: **8**. They are 096, 097, 100, 103, 106, 143 (⏸), 104 (🟡) and 152 Racing (↗). So 153 = 91 + 8 + 54 non-targets.
8. The 54 non-targets are: 13 XNA ≤3.x, 11 asset/art packs, 7 platform/retired-service, 7 pure Silverlight, 4 WinForms tools, 4 duplicates/training kits, 3 VB.NET, 2 Silverlight/XNA Phone hybrids, 2 C++ and 1 third-party asset archive.
9. Racing C++ port status:
   - Implementation is complete. Linux OPENGL33 is feature-complete and was requalified on 2026-10-03.
   - Web: a local Chrome smoke test passed on 2026-10-03. An earlier local full race with persistence passed on 2026-09-04.
   - Android: the build exists and has emulator integration. One physical Redmi device ran a debug race on 2026-09-03. Android qualification is still open.
   - Windows: not qualified.
10. Racing is not hosted because `REDISTRIBUTION_STATUS=BLOCKED_MISSING_CANONICAL_LICENSE`: the snapshot has no licence grant and keeps an "All rights reserved" notice.
11. A Racing YouTube video exists: `https://www.youtube.com/watch?v=bTThYkZJzYw`, "Racing Game on CNA and in web browser", channel @libcna. It is linked from the gallery's RacingGame.html. libcna.com has **no** Racing link and **no** Racing screenshot. The screenshot is in the gallery at `assets/img/racing-game.png`.
12. The gallery has **no per-build qualification record** (no manifest, log or flag). It has only a general banner, "native and web builds are validated". Per-build browser evidence lives in cna-samples `plan.md` rows and `missing.md`, almost always system Chrome. Firefox appears for about 6 rows. Safari never appears.
13. There is no C# (CNA.NET) gallery in samples.libcna.com. It links out to `libcna/cna-cs-samples`, which has no hosted site.
14. Every libcna.com sample claim is pinned to 4da98a0 / 87 / 40, about 20 places in total. Two are not just stale but wrong: (a) "complete = native + real-browser run" (false for 3 ✅ rows); (b) showcase lists "the client-server networking sample" as browser-verified (it is native-only).
15. A tooling trap: `scripts/check_facts.py:107` hard-requires the literal `87 / 153` on index.html. The editorial guide `audit/data/facts/00-editorial-guide.md:69` and `data/current-facts.json` must change together with it.

---

## 0. Repositories read (all read-only; status facts from committed objects)

| Repo | Branch | Commit used | Date | Notes |
|---|---|---|---|---|
| cna-samples | develop | HEAD `10e3c35b5fa6fcdf6680a79ffd29cee4adbdb798` | 2026-10-04 19:32:32 +0200 | 4 commits ahead of `origin/develop` `5db32e6a2631f216e85082b1c390321548924aa2` (2026-10-03 23:07:21). Those commits only touch the renderer matrix. `git diff --stat origin/develop HEAD -- plan.md NEXT.md plan_racing.md ignored.md missing.md README.md` is empty. `plan.md` was last changed in `3d76f01509e86ce49612683fb8d32f70cbe26c90` (2026-10-03 23:00:32, "samples: apply SAMPLE-088 through SAMPLE-153 review"). The working tree has 2 uncommitted items (`M tools/run_renderer_matrix.py`, `?? matrix-results/`); neither is used here. **Recommended new pin: `5db32e6a` (pushed).** |
| samples.libcna.com | main | `b3939de558fdb0a41f0aaa6599b7051b2680a6f7` | 2026-10-03 21:06:05 +0200 | = `origin/main`; clean. 120 commits. CNAME `samples.libcna.com`. |
| libcna.com | develop | `df85d05d82abf8ffa39c5a02661eb2abb85946e3` | 2026-10-02 12:32:12 +0200 | Untracked `audit/data/phase4-baseline-inventory.json` only. Read via `git show HEAD:`/`git grep HEAD`. |
| cna | (git objects only) | T = `b0e97bb1bb876f9b3edd6f4ff1ef3067908ae8ac` | 2026-10-04 13:20:39 +0200 | The checkout is on branch `samples` @ `1f2ada05` (dirty) and was not used. |
| cna-cs-samples (context only) | develop | `1e6d7631ae520ae087a461ebf9d268b1babe7587` | 2026-10-04 13:20:39 | Checked only for "is there a C# gallery". |
| Old pin | — | cna-samples `4da98a0fc24520d8ff9f9b462f8f78d47fc23fbe` (2026-09-20 21:10:12); gallery `736b8aa3199e07cb8ce4d174c7290d6db2c8c4aa` (2026-09-20 20:53:36) | | |

---

## TOPIC A — the C++ XNA sample port campaign (cna-samples)

### A1. Audit universe and the 91 (source fact)

**What "153" is.** `plan.md:10-13` (cna-samples@5db32e6/HEAD) says: "A direct inventory on 2026-08-22 found **153 directories after excluding `.idea`**. All 153 have an individual row below."

It is the count of physical directories in Microsoft's local XNA Game Studio sample archive snapshot (`/rv/tmp/XNAGameStudio/Samples`), plus the community Racing Game Kit directory. It is **not** "153 XNA 4.0 games". It includes XNA 2.0/3.x archives, Silverlight apps, WinForms tools, VB duplicates, art packs and documentation (see A3).

**Method (exact commands, run 2026-10-04):**

```bash
cd cna-samples
git show HEAD:plan.md | /usr/bin/grep -c '^| SAMPLE-'                      # 153 rows
for s in ✅ 🟡 ↗ ⏸ ⛔ 🗑; do printf '%s %s\n' "$s" "$(git show HEAD:plan.md | /usr/bin/grep -c "| $s |\$")"; done
# ✅ 91 | 🟡 1 | ↗ 1 | ⏸ 8 | ⛔ 3 | 🗑 49   (sum 153)
# cross-check with awk on the last column:
git show HEAD:plan.md | /usr/bin/grep -E '^\| *SAMPLE-[0-9]{3} *\|' | awk -F'|' '{s=$(NF-1); gsub(/^ +| +$/,"",s); print s}' | sort | uniq -c
# unique IDs: ... | awk -F'|' '{print $2}' | sort -u | wc -l  -> 153
```

This matches the plan's own tables:
- `plan.md:189-206` "Progress at a glance": ✅ 91, ⛔ 3, 🗑 49, ↗ 1, 🟡 1, ⏸ 8, total 153.
- `NEXT.md:27-37` "Final sample inventory", same numbers. It also says (`NEXT.md:12-14`): "Every physical upstream entry from SAMPLE-001 through SAMPLE-153 has an owner-reviewed disposition."

**The definition of ✅** is at `plan.md:121-150` (Definition of done) and `plan.md:186` (legend):
- the gates are classification, original evidence, complete translation, zero workarounds, native OPENGLES3 verification, real-browser WEBGL2 verification, and documentation;
- the legend reads: "fidelity is either verified or has a specific owner-approved, documented exception".

**Rows that are ✅ by an owner-approved scoped exception** (important for wording):

| Row | Name | Exception | Evidence |
|---|---|---|---|
| SAMPLE-004 | StockEffects | Content-Pipeline-only: a `CompileEffect` CLI tool, "intentionally creates neither a native game demo nor a web target" | plan.md:907 |
| SAMPLE-062 | NetRumble | "Native-only OPENGLES3/System-Link port … No WEBGL2 target or gallery card exists under the owner's SAMPLE-062-only exception" | plan.md:975 |
| SAMPLE-091 | ClientServerSample | "NATIVE-ONLY SCOPE ACCEPTED by the owner on 2026-09-09"; a WEBGL2 bundle builds but browser multiplayer is not provided | plan.md:1009 |
| SAMPLE-041 | LensFlare | complete "only under its expressly owner-approved, documented visual limitation, not a claim of flare parity" (occlusion-query gap on ES3/WebGL2) | plan.md:196, 949 |
| SAMPLE-061 | MarbleMaze | only the final `EX2_Polishing/End` endpoint; seven tutorial stages out of scope (SAMPLES-DEC-011) | plan.md:310, 974 |
| SAMPLE-085/086/087/094/101 | Avatar samples | use CNA's **own original avatar artwork/presets**, not Microsoft's Xbox avatars (owner decision 2026-10-03) | plan.md:315 (DEC-004 resolution); rows |

**Racing is not in the 91.** `plan.md:1078`: `| SAMPLE-152 | XNA-4-Racing-Game-Kit-master | absent | Governed only by plan_racing.md … | ↗ |`.

**What changed since the libcna.com pin 4da98a0 (87 ✅).** Method: extract `id status` from both revisions and `join` them.
- Counts at 4da98a0: ✅ 87, 🛑 49, ⛔ 14, 🛠 2, ↗ 1.
- Counts at HEAD: ✅ 91, 🗑 49, ⏸ 8, ⛔ 3, 🟡 1, ↗ 1.

| Change | Rows | Date / commit (cna-samples) |
|---|---|---|
| → ✅ (+6) | 085 AvatarAnimationBlending, 086 AvatarMultipleAnimations, 087 AvatarShadows, 094 CustomAvatarAnimation, 101 ObjectPlacementOnAvatar (all ⛔/🛑 → ✅ after the owner accepted CNA's own avatar art); 107 TiltPerspective (🛠 → ✅) | 5c7f151, 672a889, df673b5, d4da766, cb3891f, 0e8c8c9 (all 2026-10-03) |
| ✅ → ⛔ (−1) | 068 CatapultWarsTrainingKit: the owner chose not to requalify or publish its 7 exercise variants (2026-09-26) | plan.md:981; 2727124 (2026-09-28) |
| ✅ → 🟡 (−1) | 104 PerformanceUtility: owner-approved partial browser release; web networking not functional (2026-09-28) | plan.md:1022; a975326 |
| 🛑 → 🗑 / ⏸ / ⛔ | all 49 🛑 resolved; 14 ⛔ → 3 ⛔ (068, 075, 153) | 3d76f01 (2026-10-03) "apply SAMPLE-088 through SAMPLE-153 review" |
| net | 87 + 6 − 2 = **91** | |

Gallery bundle count over time:
- `git ls-tree -r --name-only <c> | grep -cE '_cna_samples\.wasm$'` gives 40 at 736b8aa (2026-09-20), 90 at b3939de (2026-10-03).
- Growth: 40→56 on 09-25, →66 on 09-26, →80 on 09-27, →84 on 09-28, →90 on 10-03.

### A2. Relevant XNA 4.0 C# programs still incomplete: **8**

These are the rows that are XNA 4.0, C#, have runnable program code, and are neither ✅ nor owner-cancelled/deleted.

| Row | Name | Status | Why it is not complete | Evidence |
|---|---|---|---|---|
| SAMPLE-096 | Invites | ⏸ (2026-10-03) | The faithful C++ translation is on develop, using CNA's replacement account/matchmaking/invite service. Before ✅ the owner must record the service difference and settle native-only vs browser scope. | plan.md row 096; NEXT.md:69 |
| SAMPLE-097 | MemoryMadnessLab | ⏸ | Two distinct WP7 lab endpoints must both be ported (estimate 40–70 h). No implementation authorized. | plan.md row 097; NEXT.md:70 |
| SAMPLE-100 | NetworkPrediction | ⏸ (2026-09-28) | Native-qualified with real accounts and a temporary TLS service. Browser account transport, discovery and relay are unqualified. Removed from the gallery. | plan.md row 100; gallery commit 9c8b55e |
| SAMPLE-103 | PeerToPeer | ⏸ | Waits for shared CNA account and browser multiplayer work. | plan.md row 103 |
| SAMPLE-104 | PerformanceUtility | 🟡 | Local profiling and console are playable on Web. Browser networking and the `remote` command do not work. **Published in the gallery as partial.** | plan.md:1022; gallery PerformanceUtility.html:18 |
| SAMPLE-106 | SavingEmbeddedImages | ⏸ | Needs 3 general CNA fixes: Guide dialogs without GamerServicesComponent, Asyncify modal `End*` frames, and `MediaLibrary.SavePicture` (6–10 h). Not ported. | plan.md row 106 |
| SAMPLE-143 | RolePlayingGame (Phone) | ⏸ | A materially distinct XNA 4 Phone generation of ✅ SAMPLE-070 (73 changed + 3 Phone-only C# files, 992 differing assets). | plan.md row 143 |
| SAMPLE-152 | Racing Game Kit | ↗ | Separate plan. Implementation is complete and Linux-qualified. Windows, physical Android and hosted Web gates are open, and the licence blocks publication (A4). | plan_racing.md:30-97; NEXT.md:44-63 |

Notes:
- **Borderline but excluded.** SAMPLE-068 CatapultWarsTrainingKit and SAMPLE-075 NGSM are XNA 4.0 C#, but the owner **cancelled** both (⛔).
  - 075's row (plan.md:988) says it was "Ported on branch `feature/gamer-services-samples` … status changes when that branch is merged". **No such branch exists in the local cna-samples** (`git branch -a --list '*gamer*'` returns nothing), so treat it as ⛔.
  - If you count these two, the figure is "8 open + 2 cancelled".
- **Excluded.** SAMPLE-112/113 (⏸) are Avatar animation asset packs with no code.
- **Safe public phrasing:** "eight", or "seven plus Racing Game". Avoid "~8" unless the reader is told that it includes Racing and a partial release.

### A3. Entries that are NOT campaign targets: **54** (49 🗑 + 3 ⛔ + 2 ⏸ asset packs)

Classification source:
- the row text at 4da98a0, because deleted rows at HEAD are reduced to `| SAMPLE-NNN | — | Name | deleted | 🗑 |` (deletion rule at NEXT.md:85-88);
- HEAD rows for ⛔ and ⏸;
- `ignored.md` (historical; it says itself it is "no longer an exclusion list", ignored.md:3-8).

One primary reason per entry:

| Reason | Count | Rows |
|---|---:|---|
| XNA 3.x or older (ARCHIVE_2_0 / 3_0 / 3_1, XNA 2 games) | 13 | 119 BasicEffectShader, 122 Catapult, 130 MaterialsAndLights, 131 Minjie, 133 Movipa, 134 MultipassLighting, 138 Pickture, 140 RedistributableTTFs (3.1 font pack), 142 RobotGame, 146 SpaceShooter (3.0), 147 SpriteBatchShader, 148 TiledSprites (3.1; a port existed, now deleted), 151 VectorRumble |
| Asset/art/resource packs (no program) | 11 | 112 AvatarAnimPack BIN (⏸), 113 AvatarAnimPack FBX (⏸), 114 AvatarAnimPack Maya, 115 AvatarAnimPack ModTool, 116 AvatarRig Max2010, 117 AvatarRig Maya2009, 118 AvatarRig Softimage, 120 ButtonImages, 123 ControllerImages, 129 LobbyChatImages, 145 SoundLab (WAV pack) |
| Platform-specific / retired service (Phone hardware/services, Xbox LIVE) | 7 | 015 TicTacToe (WP7 + WCF/MPNS), 088 BingMaps, 089 BingMapsPathFinding (retired Bing keys), 095 Geolocation (WP7 GPS), 105 PushNotifications (MPNS), 110 WP7MusicManagement, 075 NGSM (⛔; Xbox LIVE lobby, browser has no session directory) |
| Silverlight (pure, not XNA) | 7 | 124 CustomIndeterminateProgressBar, 128 LevelStarterKit, 135 NonLinearNavigationService, 139 PushRecipeWP7SL, 144 SilverlightMicrophoneSample, 149 TombstoningSample, 150 UnitConverterStarterKit |
| WinForms / design-time tools | 4 | 090 BitmapFontMaker, 093 CurveEditor, 108 WinFormsContentSample, 109 WinFormsGraphicsSample |
| Duplicates / training-kit or Phone variants of a ported game | 4 | 064 HoneycombRushTrainingKit, 068 CatapultWarsTrainingKit (⛔), 125 GSM Mango, 127 GSM Phone |
| VB.NET | 3 | 121 CardsStarterKitVB, 126 GSM Mango VB, 137 PaddleBattle VB |
| Silverlight/XNA Phone 7.1 hybrids (C#) | 2 | 132 ModelViewerDemoMango, 136 PaddleBattle |
| C++ (not C#) | 2 | 111 XnaGraphicsProfileChecker (C++/CLI WinForms D3D9), 153 XNA_XNB_Format (C++ VS2010 inspector + docs; ⛔ "non-port") |
| Other: third-party asset archive without source | 1 | 141 Riemers |
| **Total** | **54** | 91 + 8 + 54 = 153 ✓ |

Caveat: this is my grouping; the plan records an individual reason per row but no reason category. Some rows fit two buckets (e.g. 137 is VB *and* a Silverlight hybrid, 140 is XNA 3.1 *and* resource-only). Publish the buckets as "about" or name only the large ones.

### A4. Racing Game Kit (SAMPLE-152)

**Identity.** "canonical C# XNA 4.0/.NET 4 Racing Game Kit" (plan_racing.md:32-37). The historical ignored.md:99 called it a "Community game kit, not an official sample". The gallery says "Based on the XNA 4.0 Racing Game Kit for Windows".

**Is the C++ port complete?** The implementation is complete; platform qualification is partial; campaign status is ↗, not ✅.
- "All 58 original C# files / 23,486 lines map to 72 C++ units plus 61 headers / 22,620 lines … real native, Android and Web targets … not a placeholder" (plan_racing.md:39-45; samples/RacingGame/missing.md:5-10).

| Platform | Evidence class | Fact | Date | Evidence |
|---|---|---|---|---|
| Linux OPENGL33 | runtime, qualified | "Feature-complete and requalified in clean Release builds". The full Release suite passed: 753 physics records, 144/144 GPU harness, screen/menu/drivable/device-reset probes, race return, asset audit. | 2026-10-03 | plan_racing.md:92; samples/RacingGame/missing.md (2026-10-03 section); commit c81f89d "feat(SAMPLE-152): requalify Racing Game current heads" (2026-10-03 17:43) |
| Linux OPENGLES3 standalone | runtime, owner-observed | Standalone products for both renderers were "observed live by the owner with a correct-looking display". Dummy audio; audible XACT is open. | 2026-10-03 | plan_racing.md (post-qualification paragraph); commit 57b2b58 |
| Web WEBGL2 (local, threaded, COOP/COEP) | runtime, local-only | Current-head cold-profile Chrome run: content loaded in 23.973 s; 451 frames through splash→menu→car→track→race→exit; zero JS/HTTP/WebGL errors. Earlier: completed an Advanced race and reloaded highscore/replay in a new Chrome process; context loss and resize/fullscreen qualified. Open: hosted network/residency, audible XACT, browser/device matrix. | 2026-10-03; 2026-09-04 | racing_milestone12.md:12-27, 3-10; plan_racing.md:95; commit 69af676 (2026-09-04) "test(SAMPLE-152): qualify Web race persistence" |
| Android OPENGLES3 | platform-qualified partial | Both ABIs build (debug APK about 400 MB). API-35 x86_64 emulator integration. A benchmark APK was installed and launched on a physical **Redmi 24040RN64Y (API 35)** with the accelerometer registered. A debug APK race was "subjectively smooth … at … 15 FPS" with post-processing and high detail **disabled**. Open: touch-only race, ergonomics, perf/thermal, lifecycle, audible XACT, persistence, gamepad. The milestone says the correct claim is "Android implementation and emulator integration in progress," not "Android supported". | 2026-09-03 | racing_milestone11.md:46-62, 118-153 (line 152); commit 214f491 (2026-09-03 22:04) |
| Windows | not qualified | "Not qualified … Windows OPENGL33 package, rendering, XACT, storage/input and full race-return gates remain." | — | plan_racing.md:93; racing_milestone10.md:3-6 |

**CNA-side commits named in the brief** (cna@T; all are ancestors of T, checked with `git merge-base --is-ancestor`). They concern the **C# route (CNA.NET running the unchanged C# game)**, not the C++ port. Do not cite them as C++ evidence.
- `d9d599263` (2026-10-02) fix(FX-143): GLSL ES 3 volume-sampler precision. This is a general shader fix.
- `9265c6ca9` (2026-10-02) "docs: handoff updated after FX-143 and the Racing Game Kit's race".
- `28f8312f0` (2026-10-04) docs(CSX-149): "Racing Game Kit matched the C++ port structurally through a real race".
  - The C# race ran on desktop. The C++ port on OPENGL33 ran the same six stages; the comparison is structural, not pixel-identical (cna@T `handoff.md:559-584`).
  - "Browser (threaded) and Android: attract mode" only (handoff.md:582). The threaded browser runs at "~0.65 fps" (handoff.md:107).
  - Unchanged XNA under Wine is blocked by the defunct Games for Windows LIVE.

**Why it is not hosted (asset licence).**
- `racing_release_gate.md:5`: `REDISTRIBUTION_STATUS=BLOCKED_MISSING_CANONICAL_LICENSE`. "The canonical XNA 4 snapshot contains Microsoft copyright notices but no license, EULA, COPYING file or other grant that authorizes redistribution."
- The Web payload is 286.14 MiB (300,037,131 B) (racing_milestone12.md; racing_distribution.md).
- The owner chose an informational gallery entry only, with no dedicated repository (NEXT.md:58-61; racing_distribution.md:1-20).
- Gallery `RacingGame.html:20`: "The available Racing Game Kit snapshot contains no redistribution licence and retains an 'All rights reserved' notice".

**YouTube.**
- `https://www.youtube.com/watch?v=bTThYkZJzYw` appears in:
  - cna-samples `NEXT.md:60`;
  - gallery `RacingGame.html:17` ("Watch gameplay on YouTube"; added in gallery commit 0bdbd0d, 2026-10-03 "docs: add Racing Game video link").
- YouTube oEmbed metadata, fetched 2026-10-04 (external): title "Racing Game on CNA and in web browser", author "LibCNA", `https://www.youtube.com/@libcna`. The video content was not inspected, so whether it shows the C++ or the C# route is **unverified**.
- libcna.com has **no** link to it: `git grep -n bTThYkZJzYw HEAD` in libcna.com finds nothing, and `git grep -i racing HEAD -- '*.html'` finds only the "Racing Game is tracked separately" sentences.
- `libcna.com/videos.html:75` claims to show "Every video on the @libcna channel", so that page is now incomplete.

**Screenshot.**
- libcna.com `img/` contains only `architecture-diagram.svg` and `oracle/`. There is no Racing image (`git ls-tree -r --name-only HEAD | grep -i racing` returns nothing).
- The gallery has `assets/img/racing-game.png` (PNG 800×480, 416,284 B) and `assets/img/racing-game-thumb.png` (480×270), added in 4d88b4d/38a5b32 (2026-10-03).
- The image depicts original game assets. It is published in the gallery by explicit owner decision (racing_release_gate.md:20-25), so copying it into libcna.com is an owner call. Linking to the gallery page is the safe option.

**Minor inconsistencies inside the gallery** (FYI; not libcna.com):
- `README.md:77-78` says the YouTube destination "is shown as forthcoming", and the `page-8.html` Racing card says "A video is planned". `RacingGame.html` already links the video.
- `README.md:22-24,36` names 4 threaded launchers, but 5 exist (`Yacht/launch.html` too).
- The `index.html` banner "91 XNA samples were ported to CNA. Their native and web builds are validated." over-states:
  - Racing (not plan-✅; its web build is local-only);
  - PerformanceUtility (🟡).

---

## TOPIC B — samples.libcna.com gallery (@b3939de)

**Counts (exact commands, run 2026-10-04).** The gallery has 90 playable bundles, 91 cards and 91 detail pages:

```bash
cd samples.libcna.com
git ls-tree -r --name-only HEAD | /usr/bin/grep -cE '^[^/]+/[^/]+_cna_samples\.wasm$'          # 90 playable bundles
git ls-tree -d --name-only HEAD | grep -v '^assets$' | wc -l                                    # 90 bundle dirs
for p in index.html page-{2..8}.html; do git show HEAD:$p | /usr/bin/grep -c '<li class="card'; done  # 12×7 + 7 = 91 cards
git ls-tree --name-only HEAD | grep '\.html$' | grep -vcE '^(index|page-[0-9]+)\.html$'       # 91 detail pages
# detail pages with a Play link: 90; the only one without: RacingGame.html (no RacingGame/ dir)
```

**Reconciliation with plan.md:**
- I mapped ✅ rows to their `samples/<Dir>` names and ran `comm` against the gallery dirs.
- ✅ not in gallery: StockEffects (004), NetRumble (062), ClientServerSample (091).
- In gallery but not ✅: PerformanceUtility (104, 🟡).
- SAMPLE-020 contributes 2 bundles (TransformedCollision + TransformedCollisionTest).
- So 88 ✅ rows give 89 bundles, plus 1 🟡, for **90 playable**. With the Racing info card, there are **91 cards**.
- Page text: "Samples 1–12 of 91" … "85–91 of 91". The banner (index.html:30-31) reads "91 XNA samples were ported to CNA". It was changed from 90 to 91 in b3939de when Avatar Shadows was added.

**Runtime/browser qualification per build.**

| Question | Answer | Evidence |
|---|---|---|
| Manifest/JSON/qualification log in the gallery repo? | **No.** Tracked non-asset files are only `CNAME`, `README.md`, `.gitignore`, HTML, CSS, images and bundles. | `git ls-tree -r --name-only HEAD \| grep -iE 'json\|manifest\|log\|qualif\|smoke\|verify\|test'` → only `ContentManifestExtensions/*` and `FuzzyLogic/*` (name matches) |
| Per-page "verified" flag? | No. 0 pages contain "verified". Notes exist only for LensFlare (known rendering limitation, LensFlare.html:30), PerformanceUtility (🟡 partial, :18) and RacingGame (no bundle). | `git grep -l -i verified HEAD -- '*.html'` → none |
| Does a bundle record its CNA revision? | No (also stated by libcna.com development/handbook/investigate-a-sample-failure.html:168) | — |
| Where the per-build evidence lives | cna-samples `plan.md` row + `samples/<Dir>/missing.md`. 86 of 91 ✅ rows mention Chrome/browser/WEBGL2, and many say "exact gallery copy" was retested. Artifact roots `/rv/tmp/samples/SAMPLE-nnn-*/evidence/` are local and not public. | `git show HEAD:plan.md \| grep '\| ✅ \|$' \| grep -ciE 'chrome\|browser'` → 86. The only ✅ row with none of chrome/browser/webgl2 is 004. |
| Which browsers | System Google Chrome is the standard gate (NEXT.md:123). Firefox appears in rows 061, 063, 065, 067, 069, 070 (plus historical 068). **Safari: 0 mentions.** | `grep -ciE firefox/safari` on plan.md |
| Gallery-level claims | `index.html:30-38`: "Their native and web builds are validated"; "tested on the Web and Linux desktop". README:41-43: threaded bundles "tested over plain HTTP with clean Chrome profiles". | — |

Classification: per-build browser qualification is a **runtime-qualified, Chrome-on-Linux** claim recorded in cna-samples, not in the gallery. The gallery only asserts it collectively.

**Racing is NOT playable in the gallery.**
- `RacingGame.html` exists as an informational page: screenshot, source link, YouTube link, licence warning.
- There is no `RacingGame/` directory, no Play link, and no `.wasm`.
- Its card is #90 of 91, on page-8.html:76-82.

**C# (CNA.NET) gallery.**
- None in this repo. `index.html:35-41` and `README.md:65-73` link out to `github.com/libcna/cna-cs` and `github.com/libcna/cna-cs-samples`.
- `cna-cs-samples` has no CNAME or index.html (only `gallery-inventory.md`, a generated cross-reference table).
- Gallery text claims the C# route ran "nearly all of the same samples … on the Web, desktop and Android" (index.html:36-40). That is a cna-cs claim and was not verified here.

**URL structure** (CNAME = `samples.libcna.com`; GitHub Pages):

| Purpose | URL pattern | Example |
|---|---|---|
| Gallery page 1 / N | `https://samples.libcna.com/`, `/page-2.html` … `/page-8.html` | — |
| Detail page (link target for libcna.com) | `https://samples.libcna.com/<Sample>.html` | `https://samples.libcna.com/Platformer.html` |
| Direct play (non-threaded) | `/<Sample>/<Sample>_cna_samples.html` | `/Platformer/Platformer_cna_samples.html` |
| Direct play (threaded; COOP/COEP service worker) | `/<Sample>/launch.html` — MarbleMaze, HoneycombRush, NinjAcademy, CatapultWars, Yacht | `/MarbleMaze/launch.html` |
| Screenshots | `/assets/img/<kebab-name>.png`, `-thumb.png` | `/assets/img/racing-game.png` |
| Racing info page | `https://samples.libcna.com/RacingGame.html` | — |

Link to detail pages rather than direct-play URLs: detail pages carry controls and limitations, and the threaded launchers need their `launch.html`.

**Notable samples to link (all have Play buttons at b3939de):**
1. `Platformer.html`: a complete starter-kit game (3 levels, music). A good first click.
2. `RolePlayingGame.html`: the largest 2D game. Its plan row records real Chrome **and Firefox**, plus save/reload (plan.md row 070).
3. `ShipGame.html`: a full 3D game (37 units).
4. `MarbleMaze.html`: 3D physics; a threaded build via `launch.html`.
5. Optional honesty examples:
   - `LensFlare.html` (documented known limitation);
   - `PerformanceUtility.html` (🟡 partial);
   - `AvatarShadows.html` (newest, 2026-10-03; uses CNA's own avatar art).

---

## TOPIC C — libcna.com coverage (@df85d05): current claim → corrected claim

Proposed new pins:
- cna-samples `5db32e6a2631f216e85082b1c390321548924aa2` (2026-10-03, pushed; `plan.md` as of `3d76f01`);
- gallery `b3939de558fdb0a41f0aaa6599b7051b2680a6f7` (2026-10-03).

Wherever the old text says "complete = native + real-browser run", add "or an owner-approved documented scope (3 rows: one content-pipeline tool, two native-only networking samples)".

| File:line | Current claim | Corrected claim |
|---|---|---|
| index.html:103 (banner) | "plan (revision 4da98a0, 20 September 2026) marks **87 of 153** … complete; **40** … playable … Racing Game is tracked separately" | "plan (cna-samples 5db32e6, 3 October 2026) marks **91** of its 153 audited archive entries complete; **90** builds are playable at samples.libcna.com; Racing Game is a separate project (complete on Linux, not hosted)." |
| index.html:136 (stat tile + title attr) | "87 / 153 · XNA samples complete"; title "… 40 are published as browser builds" | "91 / 153 · XNA sample entries complete" (or "91 · XNA samples ported"); title "… 90 are published as browser builds …". **Must update `scripts/check_facts.py:107` (regex `87 / 153`) in the same change.** |
| index.html:217 | "cna-samples plan marks 87 of 153 … (pinned to revision 4da98a0)" | "… marks 91 of 153 … (pinned to 5db32e6)" |
| index.html:436 | "87 of 153 … complete … 40 … playable, 49 wait on owner decisions, 14 are documented non-ports and Racing Game is tracked separately. 'Complete' there means a native and an in-browser run" | "91 of 153 audited entries complete; 90 browser builds published (one marked partial); 8 XNA 4.0 C# programs remain open (including Racing); 54 entries are not port targets (older XNA, Silverlight, WinForms, VB, art packs). 'Complete' means native plus real-browser runs, except three owner-scoped rows (one tool, two native-only networking samples)." |
| showcase.html:72 | links "the samples gallery" | OK; no number. |
| showcase.html:144 | "87 of 153 … marked complete (revision 4da98a0), with native and in-browser runs" | "91 of 153 … (5db32e6); 88 of them have published browser builds" |
| showcase.html:247 | "All figures … tied to … 4da98a0 (20 September 2026)" | "… 5db32e6 (3 October 2026)" |
| showcase.html:248 | "87 of the 153 … complete — meaning a native OpenGL ES 3 run plus a real-browser WebGL 2 run … including … **the client-server networking sample** … Forty … playable" | 91 of 153. **Fix the error**: ClientServerSample (091) and NetRumble (062) are complete **native-only** by owner scope and have no browser build. "Ninety builds … playable" |
| showcase.html:249 | "49 wait on owner decisions (…), 14 are documented non-ports, and Racing Game is tracked separately" | "No row awaits a decision any more: 49 were deleted as non-targets, 3 cancelled, 8 deferred, 1 partial (Performance Utility), and Racing Game has its own plan." |
| demos.html:70 | "forty of the ported XNA samples are playable" | "ninety builds of ported XNA samples are playable (one marked partial)" |
| demos.html:76 | "153 … of which 87 … complete … 49 await owner decisions (…) 14 … non-ports … (4da98a0)" | 91 complete / 8 open / 54 non-targets at 5db32e6, with the scoped-exception note. |
| demos.html:80 | "Forty verified Release web builds (WebGL 2, non-threaded)" | "Ninety Release WebGL 2 builds, five of them threaded through a cross-origin-isolation launcher; each was run in Chrome before publication (per cna-samples records); one is a marked partial release." The old "non-threaded" is wrong: 5 bundles are threaded. |
| about.html:176 | "4da98a0 … 87 complete … 40 … 49 … 14 … 2 have complete native ports awaiting a real-browser gate and Racing Game …" | Replace with the 5db32e6 numbers; drop "2 awaiting real-browser gate" (107 is now ✅; 148 was deleted). |
| contact.html:130 | "samples gallery publishes 40 XNA sample ports (as of 20 September 2026)" | "90 playable builds plus an informational Racing Game page (as of 3 October 2026)" |
| network.html:94 | "40 published builds as of its commit 736b8aa (20 September 2026)" | "90 published builds as of b3939de (3 October 2026)" |
| deep-dives/foundations/ecosystem.html:165, 193 | pin `4da98a0`; "87 … 40 … 49 … 14 … two … pending … Racing" | Pin 5db32e6; 91/90/8/54 wording. |
| deep-dives/practice/porting-case-studies.html:147, 218 | pin 4da98a0; "87 … 49 … 14 … 2 in progress … 40 complete samples are published … (736b8aa)" | Pin 5db32e6 / b3939de; 91 ✅; "90 bundles (89 from complete rows, 1 partial)". |
| docs/xna-compatibility.html:438, 448 | pin 4da98a0; "87 … native run plus a real-browser WebGL2 run … 40 … 49 … 14 … 2 …" | Pin 5db32e6; 91 + scoped-exception note; 90 published. |
| development/handbook/investigate-a-sample-failure.html:167-168 | "87 … 49 … 14 … Racing", pin 4da98a0; gallery "40 prebuilt Release, WEBGL2, **non-threaded** bundles (GitHub Pages cannot send the COOP/COEP headers pthreads need)" @736b8aa | 91 ✅ @5db32e6; gallery "90 bundles @b3939de, 85 non-threaded and 5 threaded via a service-worker COOP/COEP launcher (`launch.html` + `coi-sw.js`)". The old reason text is outdated. |
| docs/faq.html:317 | "lists 87 of 153 directories complete and 49 awaiting owner decisions" | "91 of 153 complete; no row awaits a decision; 8 XNA 4.0 programs remain open (including Racing Game)" |
| development/handbook/update-libcna-com.html:217 | "Pinned external values (cna-samples 153/87/40, …)" | "153/91/90" |
| data/current-facts.json (external_pinned.cna_samples) | `sha 4da98a0…, date 2026-09-20, upstream_directories 153, complete 87, published_web_builds 40` | `sha 5db32e6a2631f216e85082b1c390321548924aa2, date 2026-10-03, upstream_directories 153, complete 91, partial 1, deferred 8, cancelled 3, deleted 49, separate_plan 1, published_web_builds 90, gallery_entries 91, gallery_sha b3939de558fdb0a41f0aaa6599b7051b2680a6f7`. Optional: `relevant_xna4_open 8`, `non_targets 54`. Only `language_bindings` is read by `scripts/check_facts.py`; the cna_samples keys are not machine-checked. |
| audit/data/facts/00-editorial-guide.md:69, audit/data/facts/08-ecosystem-external.md:365-394 | canonical 4da98a0 / 87 / 40 / 49 / 14 | Update the canon first. The site's process treats these as source of truth (update-libcna-com.html:217). The recount commands at 08:375-376 still work unchanged (`grep -c '| ✅ |$'` → 91). |
| videos.html:75 | "Every video on the @libcna channel" (Racing video absent) | Add a "Racing Game on CNA and in web browser" card (`bTThYkZJzYw`), or soften "every". Describe it as "the C++/C# Racing Game Kit port shown on CNA; not hosted for download" once the video content is confirmed. |
| videos.html:231 | "Web Build Demo … No video has been recorded" | Optional: point to the Racing video, which by title shows the game in a web browser. Unverified content, so keep it conditional. |
| features.html, docs/verification.html, tutorials.html | **No** cna-samples / gallery claims (grep hits are tutorial numbers 40/87/153 and CSS rgba(…153…)) | No change needed. |

Racing on libcna.com:
- There is currently no Racing page, link, screenshot or video.
- Recommended: one sentence plus a link to `https://samples.libcna.com/RacingGame.html`. That page already carries the screenshot, the source link, the video and the licence warning.

---

## Evidence-safe public wording (recommended, 7 sentences)

> CNA's C++ sample campaign audits every entry of the XNA Game Studio sample archive — 153 entries in total. That figure is the size of the audit inventory, not a count of 153 XNA 4.0 games: it also contains XNA 2.0/3.x archives, Silverlight and WinForms applications, Visual Basic duplicates, art packs and documentation. As of cna-samples `5db32e6` (3 October 2026), 91 entries are complete C++ ports, each run natively and — apart from one content-pipeline tool and two native-only networking samples — in a real browser, with no sample-side workarounds. Eight XNA 4.0 C# programs remain open (networking and Windows Phone titles, one partial release and the Racing Game Kit); the other 54 entries are not port targets. Ninety builds can be played in the browser at samples.libcna.com, one of them marked as a partial release. The Racing Game Kit is a separate, final project: its C++ port runs the complete game on Linux desktop and has passed local tests in Chrome, while Windows and Android qualification are still open, so it is not counted among the 91. Its gallery page shows a screenshot, the source and a gameplay video, but no playable build is hosted, because the available snapshot of its original content carries no redistribution licence.

If you need the brief's phrase about the licence, this exact form is defensible: "not hosted because its original content is not treated as redistributable by the CNA sample gallery".

**Do not publish** "Racing Game counted as the 91st". It contradicts `plan.md:1078` (↗) and `plan.md:196` (91 ✅ counted from the rows). If you want a gallery-based "91", say "the gallery lists 91 entries: 90 playable builds and an informational Racing Game page" (b3939de, index.html:45).

Claim classes for the wording above:

| Claim | Class |
|---|---|
| 153 audited | source (plan.md:10-13) |
| 91 complete | source plus runtime-qualified (Chrome/Linux per row) |
| exceptions | source |
| 8 open / 54 non-targets | source; my bucketing |
| 90 playable | build (bundles present); runtime-qualified per cna-samples rows |
| Racing Linux | runtime-qualified |
| Racing Chrome | runtime, local-only |
| Racing Windows/Android | future plan / open gates |
| video | external metadata only |
