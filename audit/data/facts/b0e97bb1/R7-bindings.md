# R7 — CNA language bindings and their archive status

## Executive summary (10 lines)

1. `cna-lab/bindings/` holds 19 subtrees: 9 language directories (+8 templates) and `cna-vbnet-template`. All were subtree-added on **2026-10-03** (cna-lab@d292e40b).
2. **The exact set of 8 archived C-ABI bindings is: Common Lisp, Go, Java, Python, Ruby, Rust, Swift, TypeScript (incl. JavaScript).** Each binds the CNA C ABI directly (CFFI / cgo / JNI / ctypes / Fiddle / `-sys` crate / Swift C module / Node-API + WASM).
3. **Kotlin is not a 9th binding**: its own README says it is "**not** a native binding", only a ~386-line Kotlin/JVM ergonomic layer over CNA-Java. **VB.NET is not a binding**: its README says "There is no CNA-VB binding and none is needed" — it is a template over CNA.NET (cna-cs).
4. Corroboration: CNA@T `plans/plan_bindings_upstream.md:3-4` names exactly `cna-cs` + the same 8 (no Kotlin); `:599-602` says "The seven standalone bindings (Go, Java, Python, Ruby, Rust, Swift, TS) were requalified against ABI 0.35.0 before being archived into `cna-lab`" (Common Lisp is the 8th, frozen earlier, last commit 2026-09-08, ABI 0.21–0.23).
5. Second corroboration: cna-multi-language-3d-demo had placeholder dirs for exactly these 8 languages (common-lisp, go, java, python, ruby, rust, swift, ts) beside c/cpp/cs; removed 2026-10-04 (16bde3c); README now: "exactly three languages… No additional language ports are planned".
6. Active paths: C++ core, C ABI (CNA@T exports **0.44.0**), C# **CNA.NET** (cna-cs targets 0.44.0, 95 commits since 2026-10-01). Java and TypeScript are **archived**, not maintained — the site is wrong on this in ~35 places.
7. Maturity: 7 of 8 were requalified against ABI 0.35.0 on 2026-09-30 (Linux x86-64; HEADLESS + OPENGLES3); most report the selected XNA 4.0 runtime profile (257 types) structurally complete. Common Lisp is a "selected subset", SBCL/Linux only, ABI 0.21–0.23.
8. Why archived: no explicit "why" sentence exists in any repo. The evidence is the pre-1.0 ABI moving fast: minor 0.1 (2026-08-17) → 0.44 (2026-10-03), 34 bumps, 9 minors after the 0.35 requalification in 4 days. Several minors were incompatible (0.28, 0.29, 0.30, 0.33, 0.34). Each binding pins an exact 0.x minor (or minimum minor 35).
9. Standalone repos are gone: no sibling dirs locally, and `gh repo view libcna/cna-{java,ts,rust,python,swift,go,ruby,common-lisp,kotlin}` → "Could not resolve". `cna-lab` (public, default `develop`) is the only home. **About 57 site links to `github.com/libcna/cna-{java,python,rust,swift,ts}` are now dead.**
10. The site's pins (`ef25fbb`, `f085bbb`, `e7e0750`, `4965c69`, `510a84d`, `6661173`, `14af178`) are not the final revisions. All are still reachable in cna-lab history. The real final heads are dated 2026-09-30 (CL: 2026-09-08). The site's "42b00b84 removal" story is obsolete: cna-lab history was rebuilt on 2026-10-03, and 42b00b84 is not in the repo.

## Repositories read (branch + full HEAD)

| repo | branch | HEAD |
|---|---|---|
| cna-lab | develop (= origin/develop; GitHub default `develop`, PUBLIC) | d292e40b65dd0771497ce36200bf1b2bd8fda483 |
| cna-cs | develop | 860f92cca30f0862f6eabf7970269ce49af90536 |
| cna-c-template | develop | 024c1f7aad2092c9ec8dc4862bd201c43a4ae3cc |
| cna-multi-language-3d-demo | develop | 16bde3c20fd6e3f4539e1e6ed8a2869c65e002dd |
| cna | (checkout on `samples` @1f2ada05…) read only via objects at **T = b0e97bb1bb876f9b3edd6f4ff1ef3067908ae8ac** (2026-10-04, on `next`) | — |
| libcna.com | develop | df85d05d82abf8ffa39c5a02661eb2abb85946e3 (**HEAD blobs quoted; the working tree has concurrent uncommitted edits by another session, so line numbers may shift**) |

## 1. Per-directory inventory (cna-lab@d292e40b)

The subtree-add commits are all named `Add 'bindings/<x>/' from commit '<split>'` and dated 2026-10-03 16:42 (cna-lab log: 867ddf67…62682e45). The split commit is the upstream final head. Upstream history: `git rev-list --count <split>` and `git log --reverse <split>`. Files: `git ls-tree -r HEAD bindings/<x> | wc -l`. LOC: `git grep -I -c '' HEAD -- 'bindings/<x>/*.<ext>'` summed.

| dir | language | binds to | files | src files / LOC (exts) | tests (count method) | examples / template | ABI admitted in code at final rev | upstream commits; first → final head (date) | maturity in its own words |
|---|---|---|---|---|---|---|---|---|---|
| cna-common-lisp | Common Lisp (SBCL) | **C ABI directly** via CFFI (`README.md:12-17`) | 279 | 191 / 69,939 (lisp, asd) | 85 files under tests/; 495 `define-native-test` + 37 `define-audio-device-test` + 8 `define-valueprobe-test` | 6 `examples/*.lisp`; cna-common-lisp-template (12 files) | **{0.21.0, 0.22.0, 0.23.0}** (`src/internal/abi-gate.lisp:12-17`) | 240; 2026-09-03 → **c09a7583** (2026-09-08) | "projects a **selected subset**" of XNA 4.0; qualified only on SBCL 2.5.2 Linux x86-64, HEADLESS + SOFTWARE lanes (`README.md:3,20-31`). Not part of the 0.35 requalification. |
| cna-go | Go (cgo) | **C ABI directly** (`internal/interop` is "the only cgo/native boundary", `README.md:11-21`) | 587 | 461 / 155,568 (go, c, h) | 163 `*_test.go`, 1,229 `func Test` | none in tree; cna-go-template ("Linux desktop canary", 8 files) | major 0, **minor ≥ 35** (`internal/interop/bridge.h:44-47`, `bridge.c:292-297`) | 124; 2026-08-16 → **9e46194a** (2026-09-30) | "256 of the 257 types … projected completely"; requalified 2026-09-30 vs ABI 0.35.0 on Linux amd64 HEADLESS + OPENGLES3; "This repository is being retired into `cna-lab`" (`README.md:3-7`; `NEXT.md:8-11`) |
| cna-java | Java 17 (JNI) | **C ABI directly** via a JNI adapter (`README.md:6-17`) | 774 | 708 / 109,175 (java, c, h) | 82 files in src/test, 363 `@Test` | cna-java-template ("desktop starter", 18 files) | **exact 0.35** (`NativeBindings.java` `COMPILED_ABI_VERSION = encodeVersion(0,35,0)`; `tools/native-abi/bindings.json` abiPolicy requireExactMinor=true) | 159; 2026-08-16 → **c2227a18** (2026-09-30) | "early, measured Java 17 projection"; full XNA runtime superset (331 types / 3,640 members) "structurally at zero diagnostics" (`README.md:3-40`); "final requalification against CNA C ABI 0.35.0 before this repository was archived into `cna-lab`" (`NEXT.md:3-5`, `plan.md:6-7`) |
| cna-kotlin | Kotlin/JVM | **CNA-Java, not the C ABI**: "It is **not** a native binding" (`README.md:3-20`). No JNI, no native code | 22 | 9 / 386 (kt, kts) | 4 test files ("13 focused adapter tests", README) | cna-kotlin-template (15 files) | inherits CNA-Java; README diagram says "CNA stable C ABI 0.7.0"; pinned to `org.openeggbert:cna-java:0.1.0-SNAPSHOT` | 3; 2026-08-16 → 06e7e4e2 (2026-08-23) | "functional, deliberately small Kotlin/JVM ergonomic layer"; Linux/JVM on CNA 0.7.0 HEADLESS/NULL, 60/600 frames (README "Platform truth") |
| cna-python | Python (ctypes) | **C ABI directly** (`README.md:7-13`) | 385 | 277 / 82,637 (py) | 52 files, 913 `def test_` | cna-python-template (15 files) | **exact minor 35** (`src/_cna_native/loader.py:37-44`) | 69; 2026-08-16 → **36242c73** (2026-09-30) | "pre-alpha, measured Python projection"; 257 types / 2,423 members, zero diagnostics (`README.md:3`; `NEXT.md:1-12`, requalified 0.35.0 on 2026-09-30) |
| cna-ruby | Ruby (Fiddle) | **C ABI directly** (`README.md:3`; `lib/cna/native/library.rb`) | 408 | 216 / 78,314 (rb) | 126 files, 1,736 `def test_` | cna-ruby-template ("desktop canary", 6 files) | **{0.35.0}** (`lib/cna/native/manifest.rb:215` `[0x0000_2300]`) | 136; 2026-08-16 → **25624a95** (2026-09-30) | 257/257 types, 2,915/2,915 members; suite passes HEADLESS + OPENGLES3; "This repository is being archived into `cna-lab`" (`README.md:5`; `NEXT.md:178`) |
| cna-rust | Rust (`cna-rust-sys` + safe crate) | **C ABI directly** (`crates/cna-sys`, `README.md:13-26`) | 282 | 204 / 137,989 (rs) | 47 test files, 225 `#[test]` | 0 examples; cna-rust-template (8 files) | **exact minor 35** (`crates/cna/src/native/abi.rs:1-60`) | 156; 2026-08-16 → **377af7ee** (2026-09-30, "RUST-ABI-035: the 0.35 evidence") | "early, measurable safe Rust projection"; selected profile "structurally complete" (`README.md:3-11,54-62`) |
| cna-swift | Swift 6 (Linux) | **C ABI directly** ("over the canonical CNA C ABI", `README.md:3-6`) | 515 | 359 / 77,047 (swift, c, h) | 126 files, 996 `func test` (996 pass HEADLESS + OPENGLES3 per requal doc) | cna-swift-template ("desktop canary", 6 files) | major 0, **minor ≥ 35** (`Sources/CNA/Native/NativeFunctions.swift:29-37`) | 196; 2026-08-16 → **8fc3c294** (2026-09-30) | "real Swift projection"; 257 types strict-complete; "The last pass before CNA-Swift is archived into `cna-lab`" (`docs/cna-0-35-requalification.md:3`) |
| cna-ts | TypeScript + JavaScript (Node-API + WASM) | **C ABI directly** (Node-API bridge `native/cna_node_bridge.c`; WASM `cna_c_api_wasm`) | 394 | 323 / 98,592 (ts, c, js, mjs) | 67 files, 351 `test(`/`it(` | cna-ts-template (13 files) | **exact minor 35** (`src/internal/abi.ts:12-15,46-49`) | 176; 2026-08-16 → **80514a51** (2026-09-30) | "complete XNA 4.0 runtime surface is projected and verified"; Node-API 1,040 routes + WASM 1,017 routes; 60/600 frames in headless Chromium WebGL2 (`README.md:9-24`). It absorbed the former `cna-js` on 2026-08-22: "no unique binding code was found" (`NEXT.md:3-20`) |
| cna-vbnet-template | VB.NET | **CNA.NET (cna-cs)**, not the C ABI: "There is no CNA-VB binding and none is needed" (`README.md:1-16`) | 15 | 4 / 708 (vb) | 1 compile probe (`tests/CNA.VB.CompileProbe`) | it *is* a `dotnet new cna-game-vb` template | via CNA-CS (net8.0) | 5; 2026-08-16 → 74fcfdc0 (2026-08-23) | Linux x64 OPENGLES3 under Xvfb measured; other platforms unverified (`README.md` "Measured status") |

Templates (all under `bindings/*-template`) are starters or canaries for their binding, not bindings. Their final heads: CL 17eb9483 (2026-09-07), Go 46bc0a10, Java 14de2a75, Python 212f0737, Ruby a7ca65b6, Rust abba449b, Swift f6426612, TS 71696e83 (all 2026-09-30), Kotlin 4941eab4 (2026-08-23).

## 2. The exact set of 8 archived bindings and the reasoning

**{Common Lisp, Go, Java, Python, Ruby, Rust, Swift, TypeScript}**

- 9 language directories − **Kotlin** = 8. Kotlin is a layer over CNA-Java, by its own README ("not a native binding … CNA-Java is an API dependency"). It adds operators and extensions only: 386 LOC, 3 adapter classes. It is Java's Kotlin face, not an independent binding to the C ABI.
- **VB.NET** is excluded twice over: it is a template, and it sits on CNA.NET ("There is no CNA-VB binding and none is needed").
- **JavaScript** is not separate: `cna-js` was consolidated into `cna-ts` on 2026-08-22 (cna-ts `NEXT.md:3-20`). cna-ts calls itself "the single canonical TypeScript and JavaScript binding".
- CNA's own record at T (`plans/plan_bindings_upstream.md:3-6`): "`cna-cs`, `cna-common-lisp`, `cna-go`, `cna-java`, `cna-python`, `cna-ruby`, `cna-rust`, `cna-swift`, `cna-ts`, and their templates. Each one binds this repository's C ABI". That is cna-cs plus exactly these 8, with no Kotlin. (The line opens "Ten language bindings" but names nine. The inconsistency has been there since 323111e26, 2026-09-04. Do not quote "ten".)
- `plans/plan_bindings_upstream.md:599-602` (since c536b6807, 2026-09-30): "## Fixed in the 2026-09-30 binding retirement pass — The seven standalone bindings (Go, Java, Python, Ruby, Rust, Swift, TS) were requalified against ABI 0.35.0 before being archived into `cna-lab`". Adding Common Lisp, which is in cna-lab/bindings but was frozen on 2026-09-08 and never requalified, gives 8.
- cna-multi-language-3d-demo@`16bde3c^` had `.gitkeep` placeholders for exactly common-lisp, go, java, python, ruby, rust, swift, ts (alongside c, cpp, cs). They were removed in 16bde3c (2026-10-04, "feat(CSX-155): complete C and C# Starfield ports"). The README now says: "exactly three languages … C++ … C … C# … No additional language ports are planned here."

**The count of 8 is supported. No evidence points to a different count.** If someone wanted Kotlin counted, it would be "8 bindings + 1 Kotlin layer over the Java binding". It would not be a ninth C-ABI binding.

## 3. Policy evidence (why archived)

| evidence | what it says |
|---|---|
| CNA@T `plans/plan_bindings_upstream.md:599-602` | the "2026-09-30 binding retirement pass": the 7 were requalified against ABI 0.35.0 "before being archived into `cna-lab`" |
| cna-lab bindings/cna-go `README.md:3-7`, `NEXT.md:8-11` | "being retired into `cna-lab`" / "being archived into `cna-lab`" |
| bindings/cna-java `NEXT.md:3-5`, `plan.md:6-7` | "final requalification against CNA C ABI 0.35.0 before this repository was archived into `cna-lab`" |
| bindings/cna-ruby `README.md:5`, `NEXT.md:178` | "This repository is being archived into `cna-lab`" |
| bindings/cna-swift `docs/cna-0-35-requalification.md:3` | "The last pass before CNA-Swift is archived into `cna-lab`" |
| cna-multi-language-3d-demo README + 16bde3c | finite three-language scope (C++, C, C#); other language placeholders removed |
| CNA@T `plans/plan_binding.md:20-21,59` | non-goal: "a language-specific binding, wrapper, package, generator or sample for any language other than C" inside CNA |
| ABI churn: CNA@T `git log --first-parent -G'define CNA_ABI_VERSION_MINOR' -- modules/c-api/include/CNA/C/abi.h` | **34 minor bumps**: 0.1 on 2026-08-17 … 0.21 on 08-31 … 0.29 on 09-18, 0.30 on 09-27 (removed `engine_layer.h`), 0.35 on 09-29, then 0.36–0.44 on 10-01 to 10-03 (`abi.h:34-40` at T = 0.44.0) |
| bindings/cna-rust `crates/cna/src/native/abi.rs:9-16` | "While the canonical major is `0` the ABI is experimental, and CNA ships an incompatible change **as a minor increment** — that is exactly how `0.30.0` removed `engine_layer.h`, `0.33.0` the avatar real-rendering extension and `0.34.0` the two Guide setters … a `0.x` consumer cannot admit a higher minor without re-reviewing it" |
| bindings/cna-java `tools/native-abi/bindings.json` abiPolicy.rationale | "CNA ABI 0.x is experimental … a consumer compiled against one 0.x minor cannot assume the next one is compatible" |
| bindings/cna-java `NEXT.md` "What changed for ABI 0.35.0"; cna-python `NEXT.md:33-36` | the 0.21→0.35 requalification had to remove 841 (Java) or 849 (Python) bound routes that CNA retired. This is a concrete measure of the cost of keeping a binding current. |

**Gap, stated plainly:** no repo contains an explicit sentence saying the bindings were archived *because* keeping them current against a fast-moving pre-1.0 ABI cost too much time. No repo says they "could be revived on community interest" either. (The current site already says "available for study, experiments or a future revival" — `docs/c-api.html:201`. cna-cs `docs/final-compatibility-audit.md:45` uses "revive" in an unrelated context.) The time-cost reason and the community-interest revival condition are therefore **owner policy**. The ABI churn numbers and the per-requalification route removals above are the evidence that can stand beside it. The site should word them as the project's decision ("we archived them so effort goes to …"), not as a quotation from a repo.

## 4. Former standalone repositories

- Local: none of `cna-java, cna-ts, cna-rust, cna-python, cna-swift, cna-go, cna-ruby, cna-common-lisp, cna-kotlin, cna-vbnet-template, cna-js, _bindings` exists under `/rv/data/development/github.com/{libcna,openeggbert}/` or `/rv/data/development/` (`ls`/`-e` test, 2026-10-04).
- GitHub (`gh repo view libcna/<name> --json isArchived,url,pushedAt`, 2026-10-04): all nine → "GraphQL: Could not resolve to a Repository". `openeggbert/{cna-java,cna-ts,cna-python,cna-common-lisp}` → same. `gh api orgs/libcna/repos?type=all` lists no binding repo except `cna-cs` and `cna-lab`. → **They have been removed; cna-lab is the only public home.**
- `libcna/cna-lab`: PUBLIC, isArchived=false, default `develop`, pushedAt 2026-10-03T14:43:20Z. Its `main` is a 1-commit placeholder (fb7c41c1), not an ancestor of develop.
- The develop history was **re-initialised** on 2026-10-03 (6e198929 "Initialize CNA Lab integration history", then 29 subtree adds). The site's `42b00b84` (an earlier subtree-add-then-remove) **is not present** (`git cat-file -t 42b00b84` → missing).
- These site pins are all reachable in cna-lab@d292e40b (`git merge-base --is-ancestor`) and resolve on GitHub (`gh api repos/libcna/cna-lab/commits/<sha>` verified for f085bbb, c09a7583, 80514a51): cna-java 6661173c556bacd1ba3e636fa92d2e4ec330323d, cna-ts 14af178eb8c7714a32d9f9c43ec95a80720250d2, cna-rust ef25fbb1ff54f0792006ae969a5027311139e10f, cna-python f085bbb54c57bea553cff9b48898c11f3c49a77d, cna-ruby e7e0750de409d790a23efec798e560323cc3b96d, cna-swift 4965c69c2088c00faf4b9a491e7701f8923d403f, cna-go 510a84da2ca799d4a15c8319f8ccf9e43df7a32a. They are **not final**. Final heads:

| binding | final head (full) | date | cna-lab path |
|---|---|---|---|
| Common Lisp | c09a75830fc37d97709893d4de877903e1e9684e | 2026-09-08 | bindings/cna-common-lisp |
| Go | 9e46194a808a0d953a89d9739ec33cba5452653e | 2026-09-30 | bindings/cna-go |
| Java | c2227a187038eb4243345f76d5080d85ac922937 | 2026-09-30 | bindings/cna-java |
| Python | 36242c73c9d2eeefce9cef3521fd66b4c2b9f54e | 2026-09-30 | bindings/cna-python |
| Ruby | 25624a958515489bde60df7480a0e4f89f1e12bb | 2026-09-30 | bindings/cna-ruby |
| Rust | 377af7ee53a7302954af3675b3ff241e610b9938 | 2026-09-30 | bindings/cna-rust |
| Swift | 8fc3c294a1f378d0847c618b554066bbac004fa7 | 2026-09-30 | bindings/cna-swift |
| TypeScript | 80514a51fd9949d4ace035806c2a86a7eaa27c76 | 2026-09-30 | bindings/cna-ts |
| (Kotlin layer) | 06e7e4e2254266fdffef7523165bde9188e655e7 | 2026-08-23 | bindings/cna-kotlin |

Recommended stable link form: `https://github.com/libcna/cna-lab/tree/d292e40b65dd0771497ce36200bf1b2bd8fda483/bindings/<dir>`. Or use `…/tree/<final head>` for the binding at its own root.

**What a 0.44.0 library (CNA@T) meets:** CL refuses (0.21–0.23 only). Java, Python, Ruby, Rust and TS refuse (exact minor 35). Go and Swift would nominally admit it (minimum minor 35) but were only qualified against 0.35.0. Kotlin inherits Java. **C# (cna-cs@860f92c `eng/cna-native-abi-policy.json:4`) targets `consumerAbi` 0.44.0**, the only binding at T's ABI. Its README:5 says "The binding targets CNA C ABI 0.44.0". Last commit 2026-10-04, 95 commits since 2026-10-01.

## 5. libcna.com statements to correct (HEAD df85d05)

The site's snapshot is CNA 009d40f5 (ABI 0.29.0). These corrections concern binding **status** and **links**. If the snapshot is also moved to T, the ABI numbers change too (0.44.0; C# pin 860f92c at 0.44.0).

| file:line | current claim | corrected claim |
|---|---|---|
| data/current-facts.json:150-153 `bindings_expected_abi` | maintained cna-cs/java/ts and archived python/rust/swift/go/ruby all target 0.21.x | C# (cna-cs) is the only maintained external binding. It pins its own ABI (0.21.0 at e223909; **0.44.0 at 860f92c**). Archived final revisions admit: CL 0.21–0.23; Java/Python/Ruby/Rust/TS exact 0.35; Go/Swift ≥0.35 (qualified on 0.35.0 only) |
| data/current-facts.json:154-163 `bindings_pins` | cna-java 6661173 / cna-ts 14af178 as maintained pins; archived "final revision" ef25fbb/f085bbb/e7e0750/4965c69/510a84d | replace with the final heads in §4 (all in cna-lab), add cna-common-lisp c09a7583. Keep cna-cs as the maintained pin |
| data/current-facts.json:164-196 `language_bindings` | maintained [C, C#, Java, TypeScript]; archived [Rust, Python, Ruby, Swift, Go]; archived_repositories lists 10 repos; archive_state about 42b00b84 / repos "still public"; note "Nine bindings…four maintained…five archived" | maintained [C, C#] (+ C++ core); archived [Common Lisp, Go, Java, Python, Ruby, Rust, Swift, TypeScript]. Archive home: cna-lab `bindings/` (all 8 + 8 templates; also the Kotlin layer and VB.NET template), subtree-added 2026-10-03 at d292e40b. Standalone repos no longer exist on GitHub. Note: "C++ core, C ABI, C#; eight archived bindings" |
| index.html:108 | "CNA actively maintains C, C#, Java and TypeScript bindings." | "CNA actively maintains its C ABI and the C# binding (CNA.NET)." |
| index.html:109-111 | links C#, **Java (github.com/libcna/cna-java — dead)**, **TypeScript (github.com/libcna/cna-ts — dead)** "separate pre-alpha projects … 0.21.x" | C# link only. Drop the dead links. ABI wording per the snapshot |
| index.html:112 | archived = "Rust, Python, Ruby, Swift and Go"; "being preserved in CNA Lab" | archived = Common Lisp, Go, Java, Python, Ruby, Rust, Swift, TypeScript; "preserved in CNA Lab" (done, not "being") |
| index.html:412 | CNA.NET "pinned to ABI 0.21.x" | at the site's snapshot pin; currently targets 0.44.0 (cna-cs@860f92c) |
| index.html:454-456 (cna-lab card) | "experimental CNA projects … black-pine, tamagotchi-cna, wolf-cna" | optionally add "and the eight archived language bindings under `bindings/`" |
| docs/c-api.html:9 (meta/JSON-LD) | "maintained (C, C#, Java, TypeScript) and archived (Rust, Python, Ruby, Swift, Go)" | maintained (C, C#), archived (8 languages) |
| docs/c-api.html:187 | "nine language bindings … Four … C, C#, Java and TypeScript … actively maintained. Five … archived … ten programming languages … four maintained … five archived" | C++ core + C ABI + C# active. **Eight** additional bindings archived (list). Historical total: C, C# + 8 = 10 bindings, 11 languages with C++. Count it only if wanted; the evidence supports 10 bindings |
| docs/c-api.html:188 | "The C# / .NET, Java and TypeScript bindings, like the five archived ones" | "The C#/.NET binding, like the eight archived ones" |
| docs/c-api.html:189 | every external binding targets 0.21.x | per §4 ABI table |
| docs/c-api.html:191-197 (#maintained-bindings table) | rows cna-cs, **cna-java 6661173**, **cna-ts 14af178** | rows C and cna-cs only. Move Java and TS to the archived table |
| docs/c-api.html:200-208 (#archived-bindings) | heading "Rust, Python, Ruby, Swift and Go"; "archived in September 2026"; L202 "Go and Ruby … in CNA Lab … Rust, Python and Swift have not been moved yet … original repositories"; rows with 0.21 pins and links to github.com/libcna/cna-rust, cna-python, cna-swift (dead) | heading lists 8. All 8 are in cna-lab `bindings/` since 2026-10-03 and the originals are gone. Rows = final heads (§4) with cna-lab links. Status quotes from §1. ABI column per §4 (CL 0.21–0.23; 0.35 for the rest) |
| docs/c-api.html:213 | "maintained C#, Java and TypeScript bindings … five archived" | "maintained C# binding … eight archived" |
| docs/faq.html:181-182 | maintains "four language bindings: C, C#, Java and TypeScript"; archived "Rust, Python, Ruby, Swift and Go" | C ABI + C#; 8 archived |
| docs/faq.html:159 | "separate, pre-alpha language-binding projects (including a C# one, cna-cs)" | OK; optionally "one maintained (C#) and eight archived" |
| features.html:883 | "maintained C#, Java and TypeScript bindings … Rust, Python, Ruby, Swift and Go … archived" | C# maintained; the 8 archived |
| roadmap.html:248 | "maintained C#, Java and TypeScript … pinned to ABI 0.21.x; the Rust, Python, Ruby, Swift and Go bindings are archived" | C# maintained (own ABI pin); the 8 archived and will not follow new ABI versions |
| docs/roadmap.html:256 | same pattern | same correction |
| docs/tutorials/133-renderer-capability-profile.html:444 | "public language bindings target an older ABI (0.21.x) and most … refuse 0.29.0" | "the C# binding pins its own ABI; the archived bindings stopped at 0.21–0.35" |
| development/architecture/bindings.html:7,13,19 (meta/keywords/JSON-LD) | "maintained C#, Java and TypeScript bindings and the five archived ones, all pinned to ABI 0.21.x" | "maintained C# binding and eight archived ones" |
| development/architecture/bindings.html:146 | "Four language bindings are actively maintained: C … C#, Java and TypeScript … The Rust, Python, Ruby, Swift and Go bindings are archived … (0.21.x)" | C ABI + C# maintained; 8 archived (list) |
| development/architecture/bindings.html:168-174 | Maintained table rows C#, **Java libcna/cna-java**, **TypeScript libcna/cna-ts** | C# row only |
| development/architecture/bindings.html:177-185 | "These five" + rows Rust/Python/Ruby/Swift/Go with repo names and 0.21.x | 8 rows (add Common Lisp, Java, TypeScript), cna-lab paths, final ABI per §4 |
| development/architecture/bindings.html:188,195,196,198 | "five of the eight refuse"; "Only the maintained C#, Java and TypeScript … migrate"; "For each maintained external binding (C#, Java, TypeScript)"; "archived Rust, Python, Ruby, Swift and Go"; "C# binding, Java and archived Python pages" | only C# migrates; 8 archived not updated; "C# page, archived Java and Python pages" |
| development/internals/bindings/java.html (whole page; 21 links to github.com/libcna/cna-java) | presented as a maintained binding at 6661173 | add an "Archived — not maintained" banner (as python.html:131 has). Re-point links to cna-lab (6661173 resolves there; final head c2227a18). Last ABI 0.35.0 |
| development/internals/bindings/python.html:131,148,238 (6 links to github.com/libcna/cna-python) | "until that move is complete, the links … open f085bbb in the original libcna/cna-python repository"; "maintained bindings are C, C#, Java and TypeScript" | move complete (2026-10-03); original repo gone. Re-point links to cna-lab (f085bbb resolves there; final head 36242c73, ABI 0.35). Maintained = C, C# |
| development/internals/bindings/c-api-internals.html:104-105, 240, 260, 270, 288, 334 | "maintained external C#, Java and TypeScript bindings"; "archived Rust, Python, Ruby, Swift and Go"; nav "Java binding" | C# maintained; 8 archived; nav "Java binding (archived)" |
| development/internals/bindings/csharp.html:104-105, 237, 251 | nav/related "Java binding"; "the Java page and the archived Python page" | "Java (archived)" |
| development/internals/index.html:166 | "maintained C# and Java bindings and the archived Python binding" | "maintained C# binding and the archived Java and Python bindings" |
| development/index.html:208-209 | "maintained C# and Java bindings …"; "maintained TypeScript binding and the archived Rust, Swift, Go and Ruby" | C# maintained; Java and Python archived (toured); TS, Rust, Swift, Go, Ruby, Common Lisp archived (no page) |
| development/handbook/change-map.html:217 | "C, C#, Java or TypeScript API (the maintained bindings) … archived Rust, Python, Ruby, Swift and Go" | "C or C# API"; 8 archived |
| development/handbook/update-the-c-api.html:284 (+243, 334 nav) | "maintained external bindings (cna-cs, cna-java, cna-ts) … archived ones (cna-rust, cna-python, cna-ruby, cna-swift, cna-go)" | cna-cs maintained; the 8 archived |
| development/handbook/change-public-xna-behavior.html:232 | "The maintained bindings pin an ABI (0.21.x)" | "The maintained C# binding pins its own ABI" |
| development/handbook/debug-shutdown-and-lifetime.html:209, 222 | "(C#, Java)" queue releases at pinned revisions; cna-java@6661173 | keep as historical evidence; mark Java archived |
| development/handbook/update-libcna-com.html:217 | "bindings' ABI 0.21.x and revisions" | "C# binding's ABI pin; archived bindings' final revisions" |
| development/workflows.html:166 | "C#, Java and TypeScript bindings are separate repositories … archived Rust, Python, Ruby, Swift and Go" | C# only maintained; 8 archived |
| development/takeover/blast-radius.html:169 | "Every maintained external binding (C#, Java and TypeScript …; the five archived …)" | C#; eight archived |
| development/takeover/inherited.html:155, 167 | "(C#, Java and TypeScript maintained; Rust, Python, Ruby, Swift and Go archived)" | C# maintained; 8 archived |
| development/takeover/investigation.html:188 | "All eight external bindings, the three maintained and the five archived ones, target 0.21.x" | "Nine external bindings over time: one maintained (C#) and eight archived" |
| development/takeover/mental-model.html:194 | "maintained external C#, Java and TypeScript layers (… archived Rust, Python, Ruby, Swift and Go)" | C#; 8 archived |
| development/takeover/uncertainty.html:165 | maintained C#/Java/TS, archived 5; "TypeScript binding and the archived Rust, Swift, Go and Ruby bindings have no internals page" | C# maintained; 8 archived; no-page list = TS, Rust, Swift, Go, Ruby, Common Lisp |
| development/takeover/worked-changes.html:199 | "inspect the maintained C# and Java integrations … TypeScript binding's gates" | C# only; Java/TS archived records |
| development/takeover/ownership.html:238, threading.html:276, validation.html:204, testing/architecture.html:321, debugging.html:262 | "C# and Java binding pages", "each maintained binding's own tests", "every external binding, maintained or archived, targets a 0.21 generation" | singular maintained C# binding; Java page archived; archived bindings stopped at 0.21–0.35 |
| deep-dives/reference/ecosystem-quick-reference.html:198 | "eight external binding projects … nine bindings. Four are actively maintained: C, C# (cna-cs), Java (cna-java) and TypeScript (cna-ts). Five are archived … Rust, Python, Swift, Go and Ruby, the last two public since 2026-09-25 …" | nine external binding projects over time (C# + 8), plus C = 10. Maintained: C, C#. Archived 8 (list) in cna-lab, standalone repos removed. Drop "public since 2026-09-25" |
| deep-dives/foundations/ecosystem.html:197 | "(cna-cs, cna-java and cna-ts are maintained; cna-rust, cna-python, cna-ruby, cna-swift and cna-go are archived, … being preserved in cna-lab)" | "cna-cs is maintained; eight bindings (Common Lisp, Go, Java, Python, Ruby, Rust, Swift, TypeScript) are archived in cna-lab" |
| deep-dives/reference/c-api-evidence-and-gates.html:150 | "the maintained C#, Java and TypeScript ones and the five archived ones each target ABI 0.21.x; five of the eight refuse" | C# maintained; 8 archived; ABI per §4 |
| about.html:179 | only "CNA Craft (its source lives in the cna-lab repository)" | no binding claim; optional mention |
| network.html, tutorials.html | **no binding claims** (grep: tutorials.html:614 "Go deeper" is a false positive) | none |

Gate and tooling that encode the old policy (excluded from the claim scan, but they **must change with it**):
- `scripts/check_facts.py:56-96`: `MAINTAINED_EXTERNAL = re.compile(r"C#|\bJava\b|\bTypeScript\b")` is hard-coded. Change it to C# only, or Java/TS mentions will be treated as "maintained" and paired-sentence checks will misfire. The homepage lead string is derived from `LB["maintained"]` (it becomes "actively maintains C and C# bindings" if maintained = ["C","C#"]). `ARCHIVED_NAMES` is built from `LB["archived"]`: "Common Lisp" contains a space and "TypeScript" would map to `cna-typescript` rather than `cna-ts`, so the `cna-` alternation needs adjusting. `STALE_COUNT` flags "eight/nine bindings" or "ten languages" outside an archived or historical context.
- `scripts/build_site_indexes.py:41-42` keywords for `/docs/c-api.html` ("rust","python","ruby","swift","go"): add "java","typescript","common lisp". `search-index.json` is generated (lines 1235, 2172, 2706, 2732, 2751, 4180-4192 carry the old wording).

## 6. Evidence-safe public wording (bindings overview)

> CNA is implemented in C++, and that C++ library is the engine. Its experimental C ABI (pre-1.0; minor versions may break compatibility) is the single foundation for every other language. The C# binding, CNA.NET (`libcna/cna-cs`), is the actively developed managed path, and it tracks the current C ABI. During development CNA was also bound to eight more languages: Common Lisp, Go, Java, Python, Ruby, Rust, Swift and TypeScript/JavaScript. Most reached an advanced state. Seven were requalified on Linux against C ABI 0.35.0 at the end of September 2026, and most report the selected XNA 4.0 runtime API surface as structurally complete. The Common Lisp binding stopped earlier, at ABI 0.21–0.23, and covers a selected subset on SBCL. All eight are now archived. They are not maintained, they do not follow new ABI versions, and each loader accepts only the ABI generation it was qualified against. The C ABI changed incompatibly several times while it was below 1.0, and every change had to be carried through every binding, so the project now spends that effort on C++, the C ABI and C#. The archived bindings, with their templates and full Git history, are kept in CNA Lab (`libcna/cna-lab`, under `bindings/`), and any of them can be revived if there is community interest.

(Wording notes: "structurally complete" holds for Go at 256/257 and Rust "structurally complete"; Java/TS/Python/Ruby/Swift claim 257/257 or more. Keep "most". The time-cost and community-interest clauses are owner policy and are not quoted from a repo; see §3. Do not say "Kotlin binding": it is a Kotlin layer over CNA-Java, kept in cna-lab. VB.NET is a template over CNA.NET.)
