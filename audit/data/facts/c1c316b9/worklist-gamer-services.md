# Worklist — Gamer Services / server / networking-service claims on libcna.com (move to CNA c1c316b9)

Internal audit record, not served. Facts and citations: `R4-gamer-services-server.md` (same directory;
"R4 §n" below). Survey of all public `*.html` outside `audit/` and `scripts/` in the working tree on
2026-10-09 (`git grep`; line numbers are working-tree lines; `docs/roadmap.html` and
`development/reference/cmake-options.html` already carry uncommitted lead edits, so re-check their lines).

**Classes.** **STALE** = wrong or materially incomplete at C / server `4ab12fd`+apple branch; change it.
**CURRENT** = accurate, keep. **OK** = summary or incidental mention that is not wrong (optional
refresh noted). Snapshot labels ("CNA snapshot b0e97bb1"), pinned `blob/b0e97bb1…` links and footers are
the lead's mechanical re-pin and are not listed. Generated regions (`development/reference/*.html`,
`known-issues/**`, `search-index.json`, `sitemap.xml`) are not hand-edited; regenerate after page edits.

**Style for all replacements:** sober, dated, scoped ("recorded", "loopback", "one Apple M4"); a skip is
never a pass; never name retired renderers; no Xbox LIVE compatibility; link to
<https://github.com/libcna/cna-gamer-services-server> for operational depth instead of copying the README.

## Shared replacement blocks (used by several items)

**[EV-A] dated audit bullet + handoff run** (replaces the "CNA's final audit run of this work …" bullet;
keep each page's page-specific middle sentence where marked):

```html
<li>CNA&rsquo;s final audit run of this work (2 October 2026, Linux, server commit <code>9bd5173</code> with CNA&rsquo;s client harnesses): the GamerServices suite 649 passed and the Net suite 524 passed, with no failures; the server&rsquo;s 40 registered tests: 33 passed, 7 that need Linux network namespaces skipped for lack of a test tool, none failed. [PAGE-SPECIFIC SENTENCE] The server&rsquo;s later handoff qualification (7 October 2026, Linux loopback, commit <code>4ab12fd</code>) configured 46 tests: 29 passed, the 17 that drive real CNA processes were skipped because no CNA build was available (a skip, not a pass), none failed. These are recorded runs; this site did not re-run them.</li>
```

**[EV-M] macOS bullet** (new bullet after EV-A):

```html
<li>macOS, recorded by CNA&rsquo;s Apple campaign on one Apple M4: CNA&rsquo;s test trees pass there, and the server&rsquo;s suite, with CNA&rsquo;s harnesses built against Homebrew curl, passed 37 of 46 tests with 9 skipped (seven need Linux network namespaces, two need extra 127.x loopback addresses that macOS does not configure) and none failed. Apple&rsquo;s system libcurl (8.7.1) has no WebSocket support, so a CNA build linked against it refuses the online relay (<code>RELAY_SECURE_WEBSOCKET_UNAVAILABLE</code>).</li>
```

**[EV-N] "not qualified" bullet** (replaces "Not qualified: Windows and macOS, …"):

```html
<li>Not qualified: Windows (its credential store, and the server&rsquo;s database lock, have run only under Wine), a real wide-area network with NAT, voice on physical audio devices, and avatar pixels on Direct3D and Metal.</li>
```

Citations for the three blocks: C:audit/gamer-services/evidence/phase4/server-final.log:85 and
handoff-phase4.md:73-74 (EV-A first sentence); SA:HANDOFF.md:94-98 (EV-A second); C:plans/plan_apple_m4.md
AM4-071 (:87), AM4-178 (:166), AM4-208 (:210), C:docs/apple-platforms.md:223, AM4-044/AM4-123 (:60,:132)
(EV-M); C:docs/gamer-services-known-limitations.md #28/#33, SA:README.md:164-167 (EV-N). R4 §4-§5.

---

## Counts

| File | STALE | CURRENT / OK listed |
|---|---|---|
| index.html | 1 | 0 |
| docs/gamer-services.html | 7 | 5 |
| docs/tutorials/162-gamer-services-setup.html | 2 | 0 |
| docs/tutorials/163-guide-system-ui.html | 2 | 0 |
| docs/tutorials/164-gamer-services-server.html | 6 | 2 |
| docs/tutorials/165-friends-presence.html | 2 | 0 |
| docs/tutorials/166-online-sessions.html | 4 | 1 |
| docs/tutorials/167-avatars.html | 3 | 0 |
| docs/tutorials/168-operate-gamer-services-server.html | 11 | 8 |
| docs/tutorials/97-networking.html | 3 | 2 |
| docs/tutorials/123-achievements.html | 1 | 0 |
| docs/tutorials/84-migrate-xna.html | 0 | 1 |
| docs/xna-compatibility.html | 5 | 3 |
| docs/faq.html | 1 | 2 |
| docs/roadmap.html | 2 | 1 |
| roadmap.html | 3 | 0 |
| about.html | 1 | 1 |
| features.html | 0 | 2 |
| tutorials.html | 0 | 1 |
| documentation.html | 0 | 1 |
| network.html | 0 | 1 |
| docs/migration-from-monogame.html | 1 | 0 |
| docs/building.html | 1 | 0 |
| deep-dives/services/gamer-services-contract.html | 2 | 1 |
| deep-dives/services/network-sessions.html | 7 | 0 |
| deep-dives/services/avatars.html | 1 | 0 |
| deep-dives/services/index.html | 0 | 1 |
| deep-dives/reference/{ecosystem-quick-reference,glossary}.html, deep-dives/foundations/cna-and-xna.html, deep-dives/practice/migrating-an-xna-game.html | 0 | 4 |
| development/internals/modules/gamer-services.html | 2 | 0 |
| development/internals/modules/net.html | 5 | 0 |
| development/reference/cmake-options.html | 0 | 1 |
| **Total** | **73** | |

---

## index.html

**GS-01 · index.html:240 · STALE (incomplete contract on the home page)**
- Excerpt: `…connect to the self-hosted <a …>CNA Gamer Services server</a> for accounts, friends, presence, leaderboards and relayed online sessions.`
- Why: omits achievements, messages, reviews, parties, avatars, invitations, host migration; the server
  covers the whole list (SA:README.md:3-8,23-36; R4 §3).
- Proposed: `…and can optionally connect to the self-hosted <a …>CNA Gamer Services server</a> for accounts and sign-in, friends and presence, achievements and leaderboards, messages, parties, avatars and relayed online sessions with invitations and host migration. The server is CNA&rsquo;s own and not Xbox LIVE compatible. See <a href="docs/gamer-services.html">Gamer Services &amp; Avatars</a>.`

## docs/gamer-services.html

**GS-02 · :7, :12, :18 (meta/og/JSON-LD description) · OK** — "…an optional self-hosted CNA Gamer Services
server for accounts, leaderboards and online sessions…" is a summary; optional: "for accounts, social
features, achievements, leaderboards and online sessions". Regenerate search-index.json if changed.

**GS-03 · :128 · STALE (incomplete contract)**
- Excerpt: `the same APIs connect to the self-hosted <a …>CNA Gamer Services server</a> for accounts, friends, presence, pictures, leaderboards and online sessions. It is a CNA service, not Xbox LIVE, and no public instance is operated.`
- Why: R4 §3 (SA:README.md:3-8,23-36).
- Proposed: `the same APIs connect to the self-hosted <a …>CNA Gamer Services server</a> for accounts and Guide sign-in, profiles and pictures, friends and presence, achievements, leaderboards with Ranked arbitration, messages and player reviews, parties, avatars, and online sessions (session directory, invitations, host migration and an authenticated relay that also carries voice). It is a CNA service, not Xbox LIVE compatible, and no public instance is operated.`

**GS-04 · :140 (overview row "Friends, presence, messages, pictures") · OK** — optional: server column
"Service features, plus parties and player reviews".

**GS-05 · :157 · STALE (missing user-visible transport rules; macOS/iOS)**
- Excerpt: `<strong>Platforms:</strong> the service client needs libcurl with TLS on native desktop builds. Browser builds run avatars, …`
- Why: online sessions additionally need libcurl ≥7.86 with ws **and** wss; since C a build without them
  is refused by name (`RELAY_SECURE_WEBSOCKET_UNAVAILABLE`, commit `14f74e81f`, AM4-044/123); Apple's
  system libcurl 8.7.1 has none (C:docs/c-api/CONSUMING.md:167-168); iOS needs `CNA_ENABLE_NET=OFF`
  (C:docs/apple-platforms.md:117-119). R4 §5, §7.
- Proposed: `<strong>Platforms:</strong> the service client needs libcurl 7.85 or newer with TLS on native desktop builds, and online sessions need libcurl 7.86 or newer built with WebSockets (<code>ws</code> and <code>wss</code>). Apple&rsquo;s system libcurl (8.7.1) has no WebSocket support: a macOS build linked against it refuses the online relay with <code>RELAY_SECURE_WEBSOCKET_UNAVAILABLE</code> and receives no event-channel hints, so use a WebSocket-capable libcurl such as Homebrew&rsquo;s. iOS builds are configured with <code>CNA_ENABLE_NET=OFF</code> (the iOS SDK has no libcurl), so neither <code>GamerServices</code> nor <code>Net</code> is built there. Browser builds run avatars, the Guide and local profiles, …` (rest of the sentence unchanged).

**GS-06 · :161 · CURRENT** — "(MIT, C++23 on SQLite) is one process that serves the control API, file
downloads, an event channel and the session relay on one TLS port …" (SA:README.md:160-170; deploy README:21-23).

**GS-07 · :163-164 (code block) · STALE (no longer the README's commands)**
- Excerpt: `cmake -S . -B build -G Ninja &amp;&amp; cmake --build build --parallel` / `build/cna-gamer-services-server --database service.sqlite3 --insecure-loopback   # development: http://127.0.0.1:47831`
- Why: README at `4ab12fd` documents presets with ccache and `build-agent/` (SA:README.md:56-67; HANDOFF:24-34).
- Proposed:
  ```
  # in the server repository (its presets need ccache)
  cmake --preset dev &amp;&amp; cmake --build --preset dev
  build-agent/cna-gamer-services-server --database service.sqlite3 --insecure-loopback   # development: http://127.0.0.1:47831
  ```
  (lines 166-169, the client `export`s, unchanged — CURRENT.)

**GS-08 · :170 · STALE (attribution + missing operator tooling)**
- Excerpt: `Commands are quoted from the server&rsquo;s README and CNA&rsquo;s client rules and were not run for this page; <a …>Tutorial 164</a> walks through provisioning a title and an account.`
- Why: attribution must name the revision; the handoff added the operator layer (R4 §6; SA:HANDOFF.md:6-19).
- Proposed: `Commands are quoted from the server&rsquo;s README (commit <code>4ab12fd</code>) and CNA&rsquo;s client rules and were not run for this page; <a href="tutorials/164-gamer-services-server.html">Tutorial 164</a> walks through provisioning a title and an account, and <a href="tutorials/168-operate-gamer-services-server.html">Tutorial 168</a> covers running it for others. The repository also carries the operator tooling: loopback-only health, readiness and Prometheus endpoints, JSON logs, verified online SQLite backup and a restore that refuses to overwrite, an authenticated, CSRF-protected administrator web UI that delegates every change to the admin tool, and systemd, container, Compose and nginx TCP-passthrough templates &mdash; starting points, not evidence of a production deployment. Its README and <code>HANDOFF.md</code> are the operational reference.`

**GS-09 · :173 (trust callout) · CURRENT** — client claims/no anti-cheat; per-address limits, no
server-wide handshake rate; public Internet unqualified; single process/writer (SA:README.md:172-189,212-214; security.md:49-56).

**GS-10 · :178 · STALE (public-content policy + macOS)**
- Excerpt: `it has not been measured on OpenGL ES 2, Direct3D, Metal, FNA3D or SDL_Renderer.`
- Why: names a retired renderer (policy; CNA dropped it from known-limitations #33 at C, commit
  `1cac65958`/RRC-018); AM4-082 ran the EasyGL avatar GPU test on macOS OPENGL33.
- Proposed: `Avatar rendering was reviewed on OpenGL 3.3, Vulkan, Software, SDL_GPU and WebGPU, and CNA&rsquo;s standard avatar GPU test also passes on OpenGL 3.3 under macOS; it has not been measured on Direct3D, Metal or FNA3D, and SDL_Renderer cannot draw the 3D avatar.`

**GS-11 · :182 · STALE (superseded server numbers)** — Excerpt: `the server&rsquo;s 40 registered tests: 33 passed, 7 network-isolation tests skipped for lack of a test tool, none failed. These are CNA-recorded runs, not re-run for this page.` — Why: R4 §4.1-§4.3. Proposed (this page is the overview, so the fuller form):
```html
<li>CNA&rsquo;s final audit run of this work (2 October 2026, Linux, server commit <code>9bd5173</code> with CNA&rsquo;s client harnesses): the GamerServices suite 649 passed and the Net suite 524 passed, with no failures; the server&rsquo;s 40 registered tests: 33 passed, 7 that need Linux network namespaces skipped for lack of a test tool, none failed.</li>
<li>The server&rsquo;s handoff qualification (7 October 2026, Linux loopback, commit <code>4ab12fd</code>): 46 configured tests, 29 passed, the 17 that drive real CNA processes skipped because no CNA build was available (a skip, not a pass), none failed; AddressSanitizer/UndefinedBehaviorSanitizer 19/19 and a focused ThreadSanitizer run 3/3. An independent black-box conformance suite runs 20 smoke cases plus one wall-clock relay-ticket-expiry case and exercises all 59 public operations over TLS and WebSocket.</li>
<li>macOS, recorded by CNA&rsquo;s Apple campaign on one Apple M4: CNA&rsquo;s test trees pass, including the networking and Guide tests; the server builds with Homebrew&rsquo;s Boost after small portability fixes on its <code>apple/m4-stabilization</code> branch, and with CNA&rsquo;s harnesses built against Homebrew curl 37 of its 46 tests passed, 9 were skipped (seven need Linux network namespaces, two need extra 127.x loopback addresses that macOS does not configure) and none failed. Apple&rsquo;s system libcurl (8.7.1) has no WebSocket support, so a CNA build linked against it refuses the online relay.</li>
<li>All of these are recorded runs on one machine over loopback, not re-run for this page.</li>
```

**GS-12 · :183 · STALE (macOS)** — Excerpt: `Not qualified: Windows and macOS, a real wide-area network with NAT, …` — Proposed: [EV-N].

**GS-13 · :184 (known gaps) · CURRENT.**

## docs/tutorials/162-gamer-services-setup.html

**GS-14 · :198 · STALE** — Excerpt: `the server&rsquo;s 40 registered tests: 33 passed, 7 network-isolation tests skipped for lack of a test tool, none failed. The GamerServices suite includes CNA&rsquo;s local-profile, offline-store durability and concurrency tests.` — Proposed: [EV-A] with page-specific sentence "The GamerServices suite includes CNA&rsquo;s local-profile, offline-store durability and concurrency tests." + [EV-M] variant: `<li>macOS, recorded by CNA&rsquo;s Apple campaign on one Apple M4: CNA&rsquo;s GamerServices tests were made portable to macOS and its test trees pass there; local credentials are kept in owner-only files, not the Keychain.</li>` (AM4-048, AM4-208; C:docs/gamer-services-server.md:181).

**GS-15 · :199 · STALE** — Excerpt: `Not qualified: Windows and macOS (the Windows paths above are read from the source, not run), …` — Proposed: `Not qualified: Windows (the Windows paths above are read from the source, not run), a real wide-area network with NAT, voice on physical audio devices, and avatar pixels on Direct3D and Metal.`

## docs/tutorials/163-guide-system-ui.html

**GS-16 · :159 · STALE** — server numbers (same excerpt pattern). Proposed: [EV-A] with page-specific
"The GamerServices suite contains the Guide&rsquo;s UI, input-ownership, render-state and system-Guide tests." + `<li>macOS, recorded by CNA&rsquo;s Apple campaign on one Apple M4: the Guide and gamer-services UI tests pass on Metal (130/130). Two Guide input fixes came from that work: held keys are judged by what appears on top rather than by frame time, so a Guide drawn below two frames a second still reads presses, and an identical message box opened while Enter is held does not answer itself.</li>` (AM4-086, AM4-090; commits `4f7783a95`, `8f86d0371`).

**GS-17 · :161 · STALE** — Excerpt: `Not qualified: Windows and macOS (Guide input there was not exercised), …` — Proposed: `Not qualified: Windows (Guide input there was not exercised), a real wide-area network with NAT, voice on physical audio devices, and avatar pixels on Direct3D and Metal.`

## docs/tutorials/164-gamer-services-server.html

**GS-18 · :60 · STALE (server revision)** — Excerpt: `The server commands below are quoted from its README (commit 9bd5173)` — Proposed: `…quoted from its README (commit <code>4ab12fd</code>)…` (SG: develop = next = 4ab12fd; README identical in the apple archive).

**GS-19 · :72 · CURRENT** (deps OpenSSL 3, Boost with Beast, SQLite, nlohmann/json; SA:README.md:53-54). Optional append: "and <code>ccache</code> for its build presets".

**GS-20 · :74-75 · STALE (build commands)** — Excerpt: `cmake -S . -B build -G Ninja &amp;&amp; cmake --build build --parallel` / `build/cna-gamer-services-server --database service.sqlite3 --insecure-loopback   # http://127.0.0.1:47831` — Proposed: `cmake --preset dev &amp;&amp; cmake --build --preset dev` / `build-agent/cna-gamer-services-server --database service.sqlite3 --insecure-loopback   # http://127.0.0.1:47831` (SA:README.md:56-63).

**GS-21 · :76 · CURRENT** (defaults 127.0.0.1:47831; SA:src/Main.cpp:20-21,51,61).

**GS-22 · :80-83 · STALE (paths follow GS-20)** — Excerpt: `build/cna-gamer-services-admin service.sqlite3 title my.game "My Game"` and `| build/cna-gamer-services-admin service.sqlite3 user alice Alice` — Proposed: `build-agent/cna-gamer-services-admin …` in both lines (SA:README.md:86; HANDOFF:67-70). Line 79 identifier rules CURRENT (SA:src/Protocol.cpp:9-16; Store.cpp:226-228); optional precision "8 to 256 bytes".

**GS-23 · :158 · STALE (user-visible relay refusal)** — Excerpt: `link libcurl with TLS &mdash; 7.85 or newer for the service, 7.86 with WebSocket support for the online relay.` — Proposed: `link libcurl with TLS &mdash; 7.85 or newer for the service, 7.86 or newer built with WebSockets (<code>ws</code> and <code>wss</code>) for the online relay and the event channel. A build whose libcurl lacks them &mdash; Apple&rsquo;s system libcurl 8.7.1 is one &mdash; refuses to start the relay with <code>RELAY_SECURE_WEBSOCKET_UNAVAILABLE</code>; on macOS, build against a WebSocket-capable libcurl such as Homebrew&rsquo;s. iOS builds have no networking (<code>CNA_ENABLE_NET=OFF</code>).` Optionally add a row to the error table (:146-156): `<tr><td><code>RELAY_SECURE_WEBSOCKET_UNAVAILABLE</code> when an online session starts</td><td>libcurl without WebSocket support (for example Apple&rsquo;s system libcurl)</td></tr>` — verify how the code surfaces through `NetworkSession` before adding (R4 §7; RelayWebSocket.cpp:15-25,131).

**GS-24 · :162 · STALE** — Proposed: [EV-A] with page-specific "The passing server tests include an end-to-end TLS test that signs in through the Guide with the standard XNA API." + [EV-M].

**GS-25 · :163 · STALE** — Excerpt: `Not qualified: Windows and macOS clients and server hosts, …` — Proposed: `Not qualified: Windows clients and server hosts (checked under Wine only), a real wide-area network with NAT, voice on physical audio devices, and avatar pixels on Direct3D and Metal. On macOS the evidence is the single Apple M4 run above; the server&rsquo;s own README still lists macOS as unvalidated. Public-Internet deployment has not been independently qualified.`

## docs/tutorials/165-friends-presence.html

**GS-26 · :151 · STALE** — Proposed: [EV-A] with page-specific "The passing server tests drive Guide sign-in, social flows, pictures and rich presence through the standard XNA API, and the server&rsquo;s privacy checks." + [EV-M].

**GS-27 · :153 · STALE** — Excerpt: `Not qualified: Windows and macOS, a real wide-area network with NAT, …` — Proposed: [EV-N] + keep "Public-Internet deployment of the server has not been independently qualified."

## docs/tutorials/166-online-sessions.html

**GS-28 · :156 · STALE (behaviour changed, AM4-200)** — Excerpt: `A client waits up to 30 seconds for the decision; if the session is gone or migration is off, it ends with <code>HostEndedSession</code>.` — Why: since C, data a client sends to the new host before that host has admitted it is held and delivered in order (C:modules/net/src/Internal/ServiceENetSession.cpp `pendingUpstream`; plan:201). Proposed: append after that sentence: `Data a client sends to the new host before that host has admitted it is held in order (up to 128 messages and 4&nbsp;MiB, beyond which the send fails with <code>LIMIT_EXCEEDED</code>) and delivered once the new host welcomes the client.`

**GS-29 · :161 · STALE (voice build rule, MSR-030)** — Excerpt: `browser and Android builds never carry voice.` — Why: C:modules/net/CMakeLists.txt:25-53 + cmake/HostPkgConfig.cmake: no pkg-config probe in any cross build. Proposed: `cross-compiled builds (browser, Android, iOS, or Windows built from Linux) never carry voice, because the probe asks the build host&rsquo;s pkg-config only in native builds; <code>ON</code> fails the configure there.`

**GS-30 · :177 · STALE (numbers + imprecise skip list)** — Excerpt: `the skipped seven are the NAT-isolated variants, the host-crash test and the <code>AddLocalGamer</code> test.` — Why: in that run the host-crash and AddLocalGamer **loopback** variants passed; only their namespace-isolated twins skipped (C:audit/gamer-services/evidence/phase4/server-final.log). Proposed: [EV-A] with page-specific "The passing server tests run two real CNA processes through the TLS relay for <code>PlayerMatch</code> and <code>Ranked</code>, invitations, a server restart mid-session, host migration, a host crash and an added local gamer; the seven skipped are the variants that isolate each process in its own Linux network namespace." + [EV-M] variant ending: "…On macOS the ten server tests that drive CNA processes and can run there passed (with Homebrew curl; the namespace-isolated ones need Linux), and a reliable-data loss right after an online host migration was found and fixed there."

**GS-31 · :178 · CURRENT** (NAT-isolation runs are shared-host evidence).

**GS-32 · :179 · STALE** — Excerpt: `Not qualified: Windows and macOS, a real wide-area network with NAT (latency, loss and failover are unmeasured), …` — Proposed: `Not qualified: Windows, a real wide-area network with NAT (latency, loss and failover are unmeasured), voice on physical audio devices (tested in software only), and avatar pixels on Direct3D and Metal.`

## docs/tutorials/167-avatars.html

**GS-33 · :169 · STALE** — Proposed: [EV-A] with page-specific "The GamerServices suite includes the avatar API, catalog and coordinate-space tests." + [EV-M] variant: `<li>macOS, recorded by CNA&rsquo;s Apple campaign on one Apple M4: the avatar tests pass, avatar models are built without fused multiply-add contraction so a released description assembles the same vertices on Apple silicon as on x86-64, and the standard avatar GPU test passes on OpenGL 3.3.</li>` (AM4-046 `09094e939`, AM4-082).

**GS-34 · :170 · STALE (policy)** — Excerpt: `Not measured: OpenGL ES 2, Direct3D, Metal, FNA3D and SDL_RENDERER.` — Proposed: `Not measured: Direct3D, Metal and FNA3D; SDL_RENDERER cannot draw the 3D avatar.`

**GS-35 · :172 · STALE** — Proposed: [EV-N].

(Optional, avatar behaviour at C: a `Draw` during which loading completes still draws the loading
frame and `State` becomes `Ready` for the next frame (MSR-021 `1f2ada05d`); on a renderer without 3D,
every `Draw` fails the same clean way (AM4-008 `aafdc4987`).)

## docs/tutorials/168-operate-gamer-services-server.html

**GS-36 · :60 · STALE** — Excerpt: `Every command below is quoted from or built on the server&rsquo;s README and source at commit 9bd5173; none was run for this page.` — Proposed: `…README, HANDOFF.md and source at commit <code>4ab12fd</code>; none was run for this page.`

**GS-37 · :63 · STALE (macOS)** — Excerpt: `Linux is the tested host; Windows and macOS builds are unvalidated.` — Proposed: `Linux is the qualified host. On macOS, CNA&rsquo;s Apple campaign built it with Homebrew&rsquo;s Boost on one Apple M4 and ran its suite (37 of 46 tests passed, 9 skipped for prerequisites macOS lacks (Linux network namespaces, extra loopback addresses), none failed) after small portability fixes that are on the server&rsquo;s <code>apple/m4-stabilization</code> branch, not yet on <code>develop</code>; the server&rsquo;s own README still lists macOS as unvalidated. Native Windows has not been tested (the Windows database-lock code ran under Wine only).` (Rest of :63 CURRENT.)

**GS-38 · :64 · CURRENT** (not-provided list; SA:README.md:43-49).

**GS-39 · :67-71 · STALE (build/run)** — Excerpt: `cmake -S . -B build -G Ninja &amp;&amp; cmake --build build --parallel` … `build/cna-gamer-services-server --database service.sqlite3 --listen 0.0.0.0 --port 47831 \ --cert certificate.pem --key private-key.pem` — Proposed:
```
cmake --preset dev &amp;&amp; cmake --build --preset dev     # needs ccache; at most six compile jobs
build-agent/cna-gamer-services-server --database service.sqlite3 --listen 0.0.0.0 --port 47831 \
    --cert certificate.pem --key private-key.pem --diagnostics-port 47832 --log-format json
# Development only, plain HTTP on a numeric loopback address:
build-agent/cna-gamer-services-server --database service.sqlite3 --insecure-loopback
```
and a sentence after the block: `<code>--help</code> lists every option and <code>--version</code> identifies the binary; <code>tools/qualify.sh quick</code> is the shortest supported build-and-test command.` (SA:README.md:56-67; HANDOFF:24-60.)

**GS-40 · :72 · CURRENT** (defaults; `DATABASE_IN_USE`; SIGINT/SIGTERM).

**GS-41 · :73-81 · STALE (pre-handoff deployment)** — Excerpt: `A sketch of a unit, not a file from the repository:` + `[Service] User=cna-gs …` block — Why: the repository now ships templates (R4 §6; SA:tools/cna-gamer-services-deploy/). Proposed (replace the paragraph and block):
`<p>The repository ships deployment templates in <code>tools/cna-gamer-services-deploy/</code>: a hardened systemd unit (a dedicated <code>cna-gamer-services</code> user, the database under <code>/var/lib/cna-gamer-services</code>, the certificate and key passed as systemd credentials, <code>ProtectSystem=strict</code> and <code>NoNewPrivileges</code>, diagnostics on <code>127.0.0.1:47832</code>), an unprivileged container image with a Compose file (read-only root file system, certificate and key as secrets, a health check on <code>/readyz</code>) and an nginx <code>stream</code> example that passes TCP through unchanged. They are templates: review every path, add your certificate automation and qualify your own staging host. None of them has been installed on a remote production host, the container image was not built during the server&rsquo;s own qualification, and the nginx example has not been exercised on a public network.</p>` (HANDOFF:166-172,216; campaign:124-126,165-167; deploy README:7-33.)

**GS-42 · :85-87 · CURRENT** (TLS, one port, no TLS-terminating proxy, secrets).

**GS-43 · :88 · STALE (logging)** — Excerpt: `The server&rsquo;s only regular output is one statistics line a minute on standard output, without credentials, addresses or request bodies.` — Proposed: `By default the server prints one human-readable statistics line a minute; <code>--log-format json</code> emits bounded structured events instead. Neither form contains passwords, tokens, relay tickets, request bodies or client addresses.` (operations.md:26-29; README:145-158.)

**GS-44 · :92-110 · STALE (paths) + addition** — Excerpt: `<code>build/cna-gamer-services-admin &lt;database&gt; &lt;command&gt;</code>` and every `build/cna-gamer-services-admin $DB …` line — Proposed: `build-agent/…` throughout. Append after :111: `<p>For browser administration, <code>tools/cna-gamer-services-admin-web/</code> runs a separate web UI on loopback (port 47833 by default), signed in with a password file that only its owner can read; every change is protected by a per-session CSRF token and carried out by the admin tool, <code>--read-only</code> gives an inspection-only session, and binding it to another address requires <code>--allow-remote</code> with a TLS certificate and key. Prefer an SSH tunnel.</p>` (admin-web README:8-48.) :97 "8 to 256 characters" → optional "8 to 256 bytes" (Store.cpp:227). :111 CURRENT (128 boards, 32 columns: Leaderboards.cpp:21,27,54).

**GS-45 · :115 · STALE (backup/restore)** — Excerpt: `Use SQLite&rsquo;s online backup, which is consistent under WAL, never a copy of the file while the server runs: <code>sqlite3 service.sqlite3 ".backup service-backup.sqlite3"</code>. Schedule it, and try a restore once.` — Proposed: `<strong>Backups.</strong> Use <code>tools/cna-gamer-services-deploy/backup.py</code> while the server runs: it uses SQLite&rsquo;s online backup API, checks integrity and foreign keys, and publishes a mode-0600 file atomically; it deletes nothing unless <code>--retain</code> is given. Restore with <code>restore.py</code> after stopping the server: it validates the backup and refuses to overwrite an existing database. Never copy the live database file. Keep encrypted copies in another failure domain, schedule backups and try a restore once (the repository&rsquo;s <code>docs/disaster-recovery.md</code>).` (deploy README:35-82; HANDOFF:149-164.)

**GS-46 · :116-117 · CURRENT** (durability classes; forward-only migrations; schema 23).

**GS-47 · :118 · STALE (monitoring)** — Excerpt: `The per-minute line counts responses by code, connections refused by admission, …` — Proposed: `<strong>Monitoring.</strong> With <code>--diagnostics-port 47832</code> the server opens a loopback-only HTTP listener (a non-loopback address is refused): <code>/healthz</code> for liveness, <code>/readyz</code>, ready only when SQLite has foreign keys enabled and exactly the schema this binary expects, and <code>/metrics</code> in Prometheus text format &mdash; build and schema, database and table counts, connections and admission refusals, operation and outcome counters and a fixed latency histogram, never labelled by player, address, title or session. Alert on readiness below 1, on <code>INTERNAL_ERROR</code> (storage failed: a full disk, a locked database), on refusals rising and on latency moving against your own baseline.` (operations.md:31-70; README:143-147.)

**GS-48 · :125-132 · CURRENT** (limits verified: README:136-143,172-189; v1.md:175,300,425; capacity README:233-247). Optional append to :132: `The repository&rsquo;s load lab (at most six workers; ordinary, sign-in, refresh, session-churn, directory, reconnect, host-migration, event, relay and soak profiles) produces loopback evidence for comparing revisions, not a public-Internet capacity figure.`

**GS-49 · :135-139 · CURRENT** (trust boundaries).

**GS-50 · :143 · STALE (testing)** — Excerpt: `<code>ctest --test-dir build --output-on-failure</code> runs the server&rsquo;s own suites, a TLS end-to-end test with Python clients and a relay test …` — Proposed: `<code>tools/qualify.sh quick</code> builds with ccache and runs the 19 C++ unit and component suites; <code>normal</code> runs every configured test, <code>security</code> an AddressSanitizer/UndefinedBehaviorSanitizer build, <code>performance</code> the Release benchmark smoke, and <code>full</code> adds the documentation checks. The configured set includes the TLS end-to-end and WebSocket relay tests (Python <code>websockets</code>, pinned in <code>tests/requirements.txt</code>), a black-box conformance suite, backup and restore, diagnostics, chaos, load-lab and admin-web checks. The 17 tests that drive real CNA processes need CNA&rsquo;s harness programs from a CNA build, named by <code>CNA_SERVICE_*_HARNESS</code> variables as the README lists; without them they <em>skip</em> (exit 77), which is not a pass. The NAT-isolated variants additionally need unprivileged user namespaces and a <code>slirp4netns</code> binary, which is executed, never linked, so they run on Linux only.` (qualify.sh; HANDOFF:80-92; CMakeLists.txt:257-277; README:287-325.)

**GS-51 · :147 · STALE** — Proposed: [EV-A] (page-specific: keep "(<code>slirp4netns</code>)") + new bullets: `<li>Independent conformance: <code>tools/cna-gamer-services-conformance/</code> drives the real TLS and WebSocket listener through public interfaces only &mdash; 20 smoke cases in the test suite plus one deliberate wall-clock relay-ticket-expiry case in the default profile &mdash; and checks that all 59 public operations are exercised. It is loopback evidence, not a LAN, NAT or Internet result.</li>` and `<li>Process-failure tests (<code>tools/cna-gamer-services-chaos/</code>, nine cases on scratch data) cover SIGTERM and SIGKILL recovery, ticket refusal, a locked and a full database and hostile connections; they do not prove behaviour after an operating-system crash or a power loss.</li>` + [EV-M] (server-host wording as in GS-37).

**GS-52 · :148 · CURRENT** (NAT-isolation = shared-host evidence; manual plan not executed).

**GS-53 · :149 · STALE** — Excerpt: `Not qualified: Windows and macOS server hosts and clients (the database lock and the Windows credential store were exercised under Wine only), …` — Proposed: `Not qualified: Windows server hosts and clients (the database lock and the Windows credential store were exercised under Wine only), a real wide-area network with NAT, voice on physical audio devices, and avatar pixels on Direct3D and Metal; the deployment templates have not been run on a production host.`

**GS-54 · :7/:12/:18 description · OK** — optional: "…backups and restore, health and metrics, deployment templates, limits and the service&rsquo;s trust boundaries".

## docs/tutorials/97-networking.html

**GS-55 · :143 · STALE (MSR-030)** — Excerpt: `and voice is never built for Emscripten or Android.` — Proposed: `and voice is never built in a cross-compiled build (Emscripten, Android, iOS, or Windows built from Linux).`

**GS-56 · :115, :447 · CURRENT** (SystemLink broadcast discovery on UDP 61190). Optional addition near :230-240 (discovery): `On macOS, CNA also sends the discovery query to each network interface&rsquo;s own broadcast address and listens for replies on a socket of its own, because Darwin refuses the global broadcast address; CNA records two-process SystemLink discovery on one Mac, not between two Macs.` (AM4-043 `363af6738`.)

**GS-57 · :483 · STALE (platform row)** — Excerpt: `<td>Browser and Android</td> <td>In a browser, <code>SystemLink</code> discovery is empty and the online service, relay and voice are unavailable. An Android build without libcurl has no online service either.</td>` — Proposed: row label `Browser, Android and Apple`; text `…An Android build without libcurl has no online service either. A macOS build linked against Apple&rsquo;s system libcurl (no WebSocket support) refuses the online relay with <code>RELAY_SECURE_WEBSOCKET_UNAVAILABLE</code>; iOS builds have no networking (<code>CNA_ENABLE_NET=OFF</code>).`

**GS-58 · :495 · STALE (macOS)** — Excerpt: `Windows and macOS, a real wide-area network with NAT, and voice on physical audio devices have not been qualified.` — Proposed: `…the two-process loopback test runs on POSIX hosts only. On one Apple M4, CNA&rsquo;s Apple campaign records the two-process test (8/8) and the ENet suites passing after a macOS discovery fix. Windows, a real wide-area network with NAT, and voice on physical audio devices have not been qualified. These are CNA&rsquo;s records, not re-run for this page.`

**GS-59 · :421-432 · CURRENT** (online sessions via the server; relay only; not Xbox LIVE; no public instance).

## docs/tutorials/123-achievements.html

**GS-60 · :315 · STALE** — Excerpt: `<strong>Qualification is Linux-only.</strong> … Windows and macOS have not been qualified, and no public server instance exists` — Proposed: `<strong>Qualification is Linux-first.</strong> CNA records its final audit run of this work on Linux (2 October 2026): the GamerServices suite 649 passed and the Net suite 524 passed, with no failures; CNA&rsquo;s Apple campaign records its test trees passing on one Apple M4. Windows has not been qualified, and no public server instance exists &mdash; a server-backed game runs against a server you operate.`

## docs/tutorials/84-migrate-xna.html

**GS-61 · :158-164 · CURRENT** (complete API port, not Xbox LIVE; PlayerMatch/Ranked/JoinInvited via the optional server).

## docs/xna-compatibility.html

**GS-62 · :265 (Net row) · CURRENT.**

**GS-63 · :275 (GamerServices row) · OK** — optional: "…adds accounts, friends, presence, pictures, messages, parties, server leaderboards, avatars and online sessions."

**GS-64 · :345 · CURRENT.**

**GS-65 · :352 · STALE** — Excerpt: `<strong>Qualification is Linux-only</strong> (CNA&rsquo;s recorded runs: 649 GamerServices and 524 Net tests passed); Windows, macOS, a real wide-area network and avatar pixels on Direct3D and Metal are not qualified, and browser builds have no service, relay or voice.` — Proposed: `<strong>Qualification is Linux-first</strong> (CNA&rsquo;s recorded Linux runs: 649 GamerServices and 524 Net tests passed; its Apple campaign records the test trees and the server suite passing on one Apple M4, where online play needs a WebSocket-capable libcurl rather than Apple&rsquo;s system one); Windows, a real wide-area network and avatar pixels on Direct3D and Metal are not qualified, and browser builds have no service, relay or voice.`

**GS-66 · :484 · STALE (contradicts :345)** — Excerpt: `<strong><code>GamerServices</code> has no online half</strong> &mdash; local persistence is real; sign-in, matchmaking and cloud sync do not exist. Fourteen <code>Guide::Show*</code> overlay entry points and <code>DelayNotifications</code> are documented no-ops.` — Proposed: `<strong><code>GamerServices</code> is offline unless a CNA server is configured</strong> &mdash; local profiles and local achievements and leaderboards by default; accounts, social features and online sessions need a self-hosted CNA Gamer Services server (not Xbox LIVE, no public instance, no cloud sync of local saves). Every standard <code>Guide::Show*</code> page opens.` (R4 §2-3; C:modules/gamer-services/src/Xna/Guide.cpp.)

**GS-67 · :485 · STALE (contradicts :265)** — Excerpt: `<strong>Networking is SystemLink only</strong> (plus in-process <code>Local</code>, which delivers no packets), with LAN discovery excluded on Emscripten; <code>PlayerMatch</code>, <code>Ranked</code> and <code>JoinInvited</code> throw.` — Proposed: `<strong>Online sessions need a CNA server</strong> &mdash; <code>SystemLink</code> is direct ENet on the LAN (discovery excluded on Emscripten) and <code>Local</code> delivers no packets; <code>PlayerMatch</code>, <code>Ranked</code> and <code>JoinInvited</code> go through a configured CNA Gamer Services server and its relay (no peer-to-peer path, no NAT traversal) and throw without one.`

**GS-68 · :497 · STALE** — Excerpt: `<strong>Xbox LIVE server-side services</strong> &mdash; authentication against Microsoft's servers, matchmaking and cloud-synced saves. <code>GamerServices</code> persists locally instead.` — Proposed: `…authentication against Microsoft&rsquo;s servers, Xbox LIVE matchmaking and cloud-synced saves. <code>GamerServices</code> persists locally, or uses CNA&rsquo;s own self-hosted server, which is not Xbox LIVE compatible.`

**GS-69 · :498 · STALE (false at C)** — Excerpt: `<strong>Non-SystemLink <code>NetworkSessionType</code> values</strong> (<code>PlayerMatch</code>, <code>Ranked</code>) and <code>JoinInvited</code> &mdash; they throw <code>GamerServicesNotAvailableException</code> naming the missing service, and no synthetic offline approximation is attempted.` — Proposed: delete this bullet from "Intentionally excluded" (they are implemented through the CNA server; the refusal without a server is already stated at :380 and in GS-67), or reword to: `<strong>An offline stand-in for online sessions</strong> &mdash; without a configured CNA server, <code>PlayerMatch</code>, <code>Ranked</code> and <code>JoinInvited</code> throw <code>GamerServicesNotAvailableException</code>; no synthetic offline approximation is attempted.`

## docs/faq.html

**GS-70 · :163 · CURRENT** (FNA comparison; optional: mention the optional server).

**GS-71 · :289 · CURRENT** (no LAN discovery on the web).

**GS-72 · :421 · STALE (wrong for server accounts)** — Excerpt: `the optional self-hosted CNA Gamer Services server adds accounts, server leaderboards and online sessions (it is not Xbox LIVE, and there is no cloud sync of local saves). … The <code>Begin*</code>/<code>End*</code> pairs on <code>Storage</code>, and the <code>GamerServices</code> achievement, profile and leaderboard pairs, are <strong>synchronous</strong>` — Why: for server accounts those pairs are asynchronous, completed during `GamerServicesDispatcher::Update` (W:docs/tutorials/123-achievements.html:270; W:docs/xna-compatibility.html:353). Proposed: `…adds accounts, social features, server achievements and leaderboards and online sessions (it is not Xbox LIVE, and there is no cloud sync of local saves). … The <code>Begin*</code>/<code>End*</code> pairs on <code>Storage</code>, and for local profiles the <code>GamerServices</code> achievement, profile and leaderboard pairs, are <strong>synchronous</strong>: … For a server account the same <code>GamerServices</code> pairs complete later, on the game thread during <code>GamerServicesDispatcher::Update</code>.`

## docs/roadmap.html (has uncommitted lead edits — re-check lines)

**GS-73 · :181 · OK** (summary of the optional server).

**GS-74 · :234 · STALE (badge)** — Excerpt: `<span class="status-badge status-partial">Linux-qualified</span>` (row "Gamer Services beyond Linux") — Proposed: `<span class="status-badge status-partial">Linux; macOS recorded</span>` (or keep "Partial").

**GS-75 · :235 · STALE** — Excerpt: `…exist and are qualified on Linux only. Open: Windows and macOS, a real wide-area network, …` — Proposed: `…are qualified on Linux; CNA&rsquo;s Apple campaign records the client tests and the server suite on one Apple M4 (37 of 46 server tests passed, 9 skipped for prerequisites macOS lacks (Linux network namespaces, extra loopback addresses), none failed), where online play needs a WebSocket-capable libcurl such as Homebrew&rsquo;s. Open: Windows, a real wide-area network, browser builds (where the service, relay and voice are absent), iOS (built without networking), avatar pixels on Direct3D and Metal, offline leaderboard stream columns and online guests; achievements and scores are client claims without anti-cheat, and no public server instance is operated.`

## roadmap.html

**GS-76 · :214 · STALE (badge)** — Excerpt: `<span class="status-badge status-partial">Linux-qualified</span>` — Proposed: `Linux; macOS recorded` (consistent with GS-74).

**GS-77 · :215 · STALE** — Excerpt: `Qualification is Linux-only, there is no public server instance, …` — Proposed: `Qualification is on Linux, with a CNA-recorded run on one Apple M4; there is no public server instance, and achievements and scores are client claims without anti-cheat.` Optional: add "messages, parties, avatars" to the server list in the same sentence.

**GS-78 · :297-298 · STALE** — Excerpt (h3 + p): `Gamer Services beyond Linux` / `The service client, relay and server are qualified on Linux only. Windows (credential storage is sealed with DPAPI but has run only under Wine), macOS, a real wide-area network, …` — Proposed: h3 unchanged (or "Gamer Services on more platforms"); p: `The service client, relay and server are qualified on Linux; on macOS, CNA&rsquo;s Apple campaign records them on one Apple M4, with online play needing a WebSocket-capable libcurl rather than Apple&rsquo;s system one. Open: Windows (credential storage is sealed with DPAPI but has run only under Wine; the server has not run natively), a real wide-area network, browser builds (where the service, relay and voice are absent), iOS (built without networking) and avatar pixels on Direct3D and Metal, and no public server instance is operated. Offline leaderboards drop stream columns, and online sessions refuse guests.`

## about.html

**GS-79 · :104 · STALE (contradicts :121)** — Excerpt: `(<code>PlayerMatch</code> and <code>Ranked</code> sessions, and <code>JoinInvited</code>, are refused with <code>GamerServicesNotAvailableException</code>, as they require Xbox Live.)` — Proposed: `(<code>PlayerMatch</code> and <code>Ranked</code> sessions and <code>JoinInvited</code> go through CNA&rsquo;s own self-hosted Gamer Services server, not Xbox LIVE; without a configured server they are refused with <code>GamerServicesNotAvailableException</code>.)`

**GS-80 · :121 · OK** ("optional self-hosted server for accounts and online sessions"; optional: "accounts, social features and online sessions").

## features.html

**GS-81 · :174 (Networking card) · CURRENT.** **GS-82 · :181-183 (GamerServices card) · OK** — optional:
add "player reviews, parties and avatars stored per account" to :181.

## tutorials.html · documentation.html · network.html

**GS-83 · tutorials.html:1475 and JSON-LD :341,:370-376 · OK.** **GS-84 · documentation.html:148 · OK.**
**GS-85 · network.html · OK** — the page lists `*.libcna.com` sites; it makes no Gamer Services claim.
Do not add a card that implies a hosted Gamer Services instance; if the server is mentioned at all, link
the GitHub source repository.

## docs/migration-from-monogame.html

**GS-86 · :506 · STALE (pre-service text)** — Excerpt: `<strong>GamerServices has no online service, but it is not a pure shim</strong> … What genuinely does nothing: fourteen <code>Guide::Show*</code> overlay entry points plus <code>DelayNotifications</code>, and the XNA-faithful <code>AvatarRenderer::Draw()</code>. <code>NetworkSessionType::PlayerMatch</code>, <code>Ranked</code> and <code>JoinInvited</code> throw <code>GamerServicesNotAvailableException</code>. There is no Steam, Xbox Live or HTTP integration of any kind.` — Proposed: `<strong>GamerServices is offline by default, with an optional CNA server</strong> &mdash; all 52 types are present, and unlike FNA&rsquo;s no-op shim CNA backs them with real local profiles: achievements and leaderboard entries are written as JSON under <code>&lt;StorageDevice root&gt;/GamerServices/</code> … (keep the storage sentence) … The Guide is a CNA-drawn system UI whose standard pages open, and <code>AvatarRenderer::Draw()</code> draws CNA&rsquo;s own avatars. Accounts, social features and <code>PlayerMatch</code>/<code>Ranked</code>/<code>JoinInvited</code> sessions need a self-hosted CNA Gamer Services server, configured outside game code (not Xbox LIVE; no Steam integration); without one those session types throw <code>GamerServicesNotAvailableException</code>.`

## docs/building.html

**GS-87 · :486 · STALE (MSR-030)** — Excerpt: `<code>AUTO</code> carries voice when the system has libopus; it is not vendored, so Windows, browser and Android builds carry voice only when one is provided.` — Proposed: `<code>AUTO</code> carries voice when a native build finds libopus 1.3 or newer through pkg-config; it is not vendored, and a cross-compiled build (browser, Android, iOS, Windows built from Linux) never probes for it, so it carries no voice there and <code>ON</code> fails the configure.` (C:modules/net/CMakeLists.txt:25-53; cmake/HostPkgConfig.cmake.)

## deep-dives/services/gamer-services-contract.html

**GS-88 · :141, :148, :169 · CURRENT.**

**GS-89 · :163 · STALE (incomplete)** — Excerpt: `The native service client needs libcurl with TLS; a browser build has local profiles only.` — Proposed: `The native service client needs libcurl 7.85 or newer with TLS, and online sessions and the event channel need libcurl 7.86 or newer with WebSockets; a build whose libcurl lacks them (Apple&rsquo;s system libcurl among them) refuses the relay by name. A browser build has local profiles only, and iOS builds are configured without networking.`

**GS-90 · :253 · STALE** — Excerpt: `…and the server&rsquo;s suite at 33 passed with 7 NAT-isolation cases skipped, all on Linux; … What none of this establishes: … the online client paths, credential stores or Guide input on Windows or macOS (not run there; the Windows credential store was exercised under Wine only)…` — Proposed: keep the 2026-10-02 numbers, then add: `The server&rsquo;s own handoff qualification (2026-10-07, Linux loopback, commit <code>4ab12fd</code>) passed 29 of 46 tests with the 17 CNA-driven ones skipped as unavailable and none failed; CNA&rsquo;s Apple campaign (<code>plans/plan_apple_m4.md</code> AM4-071, AM4-208) records the client tests and the server suite on one Apple M4 (37 of 46 server tests passed, 9 skipped, none failed).` and change the negative list to `…the online client paths, credential stores or Guide input on Windows (not run there; the Windows credential store was exercised under Wine only), a public Internet deployment …`. Note in the evidence callout (:139) that macOS facts come from CNA's Apple plan, which CNA's own `gamer-services-known-limitations.md` #28 has not yet absorbed.

## deep-dives/services/network-sessions.html

**GS-91 · :192 · STALE (relay refusal)** — Excerpt: `A browser build has no service transport and refuses both types, and an Android build without libcurl refuses them the same way.` — Proposed: append `A native build whose libcurl has no WebSocket support (Apple&rsquo;s system libcurl 8.7.1, or any libcurl older than 7.86) refuses the relay before any I/O with <code>RELAY_SECURE_WEBSOCKET_UNAVAILABLE</code>.` (C:modules/net/src/Internal/RelayWebSocket.cpp:15-25,131.)

**GS-92 · :197 · STALE (AM4-200)** — Excerpt: `A client waits up to 30 seconds for that decision before the session ends with <code>HostEndedSession</code>.` — Proposed: append `Until the new host has admitted a client, application data that client sends to it is held in order (at most 128 messages and 4&nbsp;MiB; more fails with <code>LIMIT_EXCEEDED</code>) and sent when the host&rsquo;s welcome arrives; a failed session discards it. (Before this fix a reliable message sent in that window could be lost.)` (ServiceENetSession.cpp `pendingUpstream`; RelayEnetPolicy.hpp:10; plan:201.)

**GS-93 · :202 · STALE** — Excerpt: `seven NAT-isolation cases were skipped in CNA&rsquo;s final recorded run, and nothing establishes play across the public Internet, on Windows or macOS, or in a browser.` — Proposed: `seven namespace-isolated cases were skipped in CNA&rsquo;s final Linux run; on one Apple M4, CNA&rsquo;s Apple campaign records the server&rsquo;s CNA-driven tests passing over loopback with a WebSocket-capable libcurl (Homebrew curl), except the namespace-isolated variants, which need Linux. Nothing establishes play across the public Internet, on Windows, or in a browser.`

**GS-94 · :231 · STALE (discovery on Apple)** — Excerpt: `A searching client sends a <code>Query</code> … by broadcast and, as a same-machine fallback, by unicast to <code>127.0.0.1</code>, then polls …` — Proposed: insert after that clause: `On Apple platforms the query is also sent to every up interface&rsquo;s own broadcast address (Darwin refuses the global broadcast address), from a socket of the search&rsquo;s own so that a host on the same Mac cannot capture the replies, while the shared port keeps answering other machines.` (C:modules/net/src/Internal/ENetDiscoveryService.cpp `SearchSocket`, `SendToEveryInterfaceBroadcast`; AM4-043.)

**GS-95 · :290 · STALE (MSR-030)** — Excerpt: `Voice needs libopus at build time (<code>CNA_ENABLE_VOICE</code>; never on Emscripten or Android)` — Proposed: `Voice needs libopus at build time (<code>CNA_ENABLE_VOICE</code>; never in a cross-compiled build such as Emscripten, Android or iOS)`.

**GS-96 · :315 · STALE (minor, dated count)** — Excerpt: `CNA&rsquo;s own audit record reports the Net suite at 524 passed, 0 failed, 0 skipped on Linux (2026-10-02).` — Proposed: append `CNA&rsquo;s Apple campaign records the two-process test (8/8) and the ENet suites (81/81) passing on one Apple M4 after a macOS discovery fix.`

**GS-97 · :316 · STALE (macOS)** — Excerpt: `It does not establish discovery between separate machines, behaviour on Windows (…), anything in a browser, …` — Proposed: keep, and change the opening to `What that establishes is SystemLink delivery between processes on the kinds of host the tests run on (Linux, and one Apple M4 in CNA&rsquo;s Apple campaign), and the online lifecycle over loopback and Linux network namespaces.`

**GS-98 · deep-dives/services/index.html · OK.**

## deep-dives/services/avatars.html

**GS-99 · :310 · STALE (policy + macOS)** — Excerpt: `Not measured: OpenGL ES 2, the DirectX and Metal renderers (no Windows or macOS host), FNA3D and SDL_RENDERER (which cannot draw the 3D avatar at all).` — Proposed: `Not measured: the Direct3D and Metal renderers and FNA3D; SDL_RENDERER cannot draw the 3D avatar at all. CNA&rsquo;s standard avatar GPU test also passes on OpenGL 3.3 under macOS (Apple campaign, AM4-082).` Optional addition elsewhere on the page: MSR-021 readiness latch, AM4-008 clean failure without 3D, AM4-046 identical assembly on arm64.

## development/internals/modules/gamer-services.html

**GS-100 · :154 (evidence callout) · STALE** — Excerpt: `the 36 test files (634 test-macro definitions) were located, none executed. CNA records its own Linux qualification (GamerServices 649 passed, Net 524 passed, the companion server 33 passed and 7 skipped, 2026-10-02); … Windows and macOS clients, real wide-area networks, Guide sounds heard by a person and avatar pixels on DirectX, Metal, OPENGLES2, FNA3D and SDL_RENDERER remain unverified.` — Proposed: `…the 36 test files (637 test-macro definitions) were located, none executed. CNA records its own Linux qualification (GamerServices 649 passed, Net 524 passed, the companion server 33 passed and 7 skipped, 2026-10-02) and its Apple campaign&rsquo;s run on one Apple M4; … Windows clients, real wide-area networks, Guide sounds heard by a person and avatar pixels on Direct3D, Metal and FNA3D remain unverified.` (Counts at C, R4 §7.)

**GS-101 · :260 · STALE** — Excerpt: `CNA&rsquo;s final qualification ran those on one Linux host, with the NAT-isolation gates skipped. … A green local suite cannot establish behaviour against a public Internet deployment or on Windows and macOS clients.` — Proposed: `CNA&rsquo;s final Linux qualification ran those on one Linux host with the namespace-isolated gates skipped, and its Apple campaign ran them on one Apple M4 with a WebSocket-capable libcurl. … A green local suite cannot establish behaviour against a public Internet deployment or on Windows clients.`

## development/internals/modules/net.html

**GS-102 · :154 (evidence callout) · STALE** — Excerpt: `the 33 test files (529 test-macro definitions)` and `CNA records its own Linux qualification of the module (524 passed, 2026-10-02) …` — Proposed: `530 test-macro definitions`; append `CNA&rsquo;s Apple campaign records the module&rsquo;s networking cases passing on one Apple M4 (304 in the Metal Debug tree) after a SystemLink discovery fix and an online host-migration fix.`

**GS-103 · :159 · STALE (MSR-030)** — Excerpt: `the pkg-config probe is not asked on Emscripten or Android, so without a provided libopus <code>NetworkGamer.HasVoice</code> stays false` — Proposed: `the pkg-config probe is not asked in any cross-compiled configuration (<code>CMAKE_CROSSCOMPILING</code>, through <code>cmake/HostPkgConfig.cmake</code>), so a cross build carries no voice and <code>ON</code> fails there`.

**GS-104 · :209 · STALE (Apple discovery)** — Excerpt: `On native builds the socket is bound to port 61190 with <code>SO_REUSEADDR</code>, broadcast and non-blocking options, so several processes on one machine can each bind it; …` — Proposed: append `On Apple platforms the socket also sets <code>SO_REUSEPORT</code> (Darwin grants port sharing only that way), and <code>FindSessions</code> sends from a temporary socket of its own to the global broadcast address, to every up interface&rsquo;s broadcast address and to loopback, draining the shared socket meanwhile; the Linux path is unchanged.` (AM4-043.)

**GS-105 · :222 · STALE (count)** — Excerpt: `<code>RelayTransportTests</code> (4)` — Proposed: `<code>RelayTransportTests</code> (5, including the libcurl capability rule on synthetic version data)` (AM4-123).

**GS-106 · :237 · STALE** — Excerpt: `CNA&rsquo;s own records add that online sessions were qualified only on one Linux host over loopback and network namespaces, …` — Proposed: `…that online sessions were qualified on one Linux host over loopback and network namespaces and, in the Apple campaign, on one Apple M4 over loopback with a WebSocket-capable libcurl, …`. Also consider a sentence in the teardown/error section that a libcurl without ws/wss now fails with `RELAY_SECURE_WEBSOCKET_UNAVAILABLE` (formerly `RELAY_CONFIGURATION`).

## development/reference/cmake-options.html

**GS-107 · :135 rows `CNA_ENABLE_NET`, `CNA_ENABLE_VOICE`, `CNA_GAMER_SERVICES_SERVER_ROOT` · CURRENT** —
descriptions/defaults identical at C (C:CMakeLists.txt:180; modules/net/CMakeLists.txt:29;
cmake/Harnesses.cmake:563). Generated page: regenerate, do not hand-edit.

## Other pages checked — CURRENT

deep-dives/reference/ecosystem-quick-reference.html:172; deep-dives/reference/glossary.html:281;
deep-dives/foundations/cna-and-xna.html:200; deep-dives/practice/migrating-an-xna-game.html:215-216;
development/build/architecture.html:317 (`CNA_ENABLE_VOICE` generic). No `title=` tooltip on any page
mentions Gamer Services or the server. `data/current-facts.json` has no Gamer Services key.
`search-index.json` mirrors the page descriptions (regenerate after GS-02/GS-54 if changed).

## Out-of-area observations (not counted; for the owning researcher)

- docs/faq.html:285 names retired browser renderers (`WEBGL1`, `CANVAS`) — public-content policy.
- docs/xna-compatibility.html:482 "Web caveats — no save persistence at all" contradicts docs/faq.html:287 (IndexedDB persistence).
- about.html:93, features.html:7/12/24, docs/building.html:341, docs/native-platforms.html: native X11/Wayland/Win32 platform layers (CNA_PLATFORM is SDL3 | HEADLESS | TERMINAL at C).
- docs/roadmap.html:230 Metal row ("no fresh macOS compile-and-run result") is contradicted by C:docs/apple-platforms.md (METAL full tree 11,015/11,015; Phase 3 verdict SUPPORTED).
- about.html:122 and docs/roadmap.html:179 give the C ABI as 0.44.0; it is 0.46.0 at C.

---

## Applied (Phase B, 2026-10-09)

Edited in place (structure, IDs, classes kept; footers, "CNA snapshot b0e97bb1" doc-meta lines, pinned
`b0e97bb1` links that still resolve at c1c316b9, and generated blocks left to the global pass). All CNA
link paths on these pages exist at c1c316b9 (checked with `git cat-file -e`); no link was added.
Checks: `hits.py` clean (only the legitimate ALSA-capture line in xna-compatibility), `vanished.py` empty,
`check_retired_renderers.py` lists none of these files, `check_deep_page.py`/`check_dev_page.py` report only
the expected "not pinned to TARGET" link errors, every page parses (html5lib).

- **docs/gamer-services.html** — GS-03 full contract in the callout; GS-05 libcurl/WebSocket rule, Apple
  system libcurl refusal, iOS `CNA_ENABLE_NET=OFF`; GS-07 preset build + `build-agent/`; GS-08 README
  `4ab12fd` attribution + operator tooling sentence + link to Tutorial 168; GS-10 retired renderer removed,
  macOS OpenGL 3.3 avatar test; GS-11/GS-12 qualification list rewritten (2 Oct Linux run with harnesses,
  7 Oct handoff run 29/46 + 17 skipped, conformance 20+1/59 ops, macOS 37/9/0 + system-libcurl note,
  loopback/one-machine caveat, Windows-only "not qualified").
- **docs/tutorials/162** — EV-A + macOS bullet (GamerServices tests portable, owner-only credential files) + Windows-only not-qualified.
- **163** — EV-A + macOS Guide bullet (Metal 130/130, held-key priming fixes) + Windows-only not-qualified.
- **164** — README `4ab12fd`; `ccache` for presets; preset build and `build-agent/` paths; password "bytes";
  libcurl ws/wss rule, `RELAY_SECURE_WEBSOCKET_UNAVAILABLE`, polling fallback, Homebrew curl, iOS; EV-A +
  EV-M; not-qualified reworded (README still says macOS unvalidated).
- **165** — EV-A + EV-M; not-qualified Windows-only.
- **166** — AM4-200 data hold in host migration; voice not in cross builds; EV-A with corrected skip list
  (loopback host-crash/AddLocalGamer passed) + macOS bullet linking to #migration; not-qualified Windows-only.
- **167** — readiness latch (MSR-021) in "Loading states"; EV-A + macOS avatar bullet (FMA contraction,
  OpenGL 3.3 test); retired renderer removed; EV-N.
- **168** — commit `4ab12fd`/HANDOFF; macOS/Windows host status; preset build/run with diagnostics + JSON
  logs, `--help`/`--version`, `qualify.sh`; systemd sketch replaced by the checked-in unit excerpt + template
  boundaries; logs; `build-agent/` admin paths (8×); new admin-web paragraph; backup.py/restore.py; loopback
  health/readiness/metrics monitoring; load-lab note; qualify.sh test tiers; evidence list (2 Oct run, 7 Oct
  handoff, conformance + chaos, macOS); not-qualified + templates. Meta/og/JSON-LD description updated.
- **97-networking** — voice not in cross builds; macOS discovery note; "Browser, Android and Apple" row
  (system-libcurl refusal, iOS no networking); qualification sentence with macOS two-process/ENet results.
- **123-achievements** — "Qualification is Linux-first" with the Apple-campaign note; Windows not qualified.
- **84-migrate-xna** — parity fixtures registered by EasyGL, WebGPU, SDL_GPU and Direct3D 11 (retired renderer removed; verified in renderer examples CMake at c1c316b9).
- **xna-compatibility** — 14 identities / 12 families (×3), compiled effects 11 of 14 in 9 families with the
  eight current options (`CNA_METAL_` added, retired option removed, "other 13"), SDL_RENDERER the one
  2D-only identity, PBR row (seven families/nine identities incl. Metal sample the maps — AM4-085), primary
  selection through SDL3 on X11/Wayland, Linux-first qualification, web caveats (IndexedDB saves with the
  legacy FS), GS-66..GS-69 pre-service bullets rewritten. Sidebar link text "Native Platforms (X11, Wayland,
  Win32)" left for the global docs-sidebar pass.
- **deep-dives/services/gamer-services-contract** — evidence callout notes the Apple-campaign source;
  libcurl/WebSocket/iOS rule; evidence paragraph adds the handoff run and macOS; Windows-only negative list.
- **deep-dives/services/network-sessions** — relay refusal by name; AM4-200 hold; macOS online evidence;
  Apple discovery behaviour; voice not in cross builds; Net macOS results; "kinds of host"; callout note.
- **deep-dives/services/avatars** — readiness latch + clean failure without vertex buffers; retired renderer
  removed and macOS evidence; demos built for the three EasyGL identities or VULKAN.
- **development/internals/modules/gamer-services** — 637 test macros; macOS run noted; retired renderer
  removed; `-ffp-contract=off` for AvatarModel.cpp; Guide priming by creation serial; recipes/qualification
  wording; avatar-render orientation sentence.
- **development/internals/modules/net** — 530 test macros; Apple-campaign networking cases; voice probe
  in cross builds; Apple discovery socket behaviour; RelayTransportTests 5; online migration data hold;
  qualification wording with the relay refusal code.

### Applied — platform/renderer cleanup on the input, media and devices pages (same pass)

- **deep-dives/services/gamepads-and-haptics** — evdev mapping-database section (inside the
  `wpb5-evdev-controller-mappings` markers) replaced by an SDL3 "Controller mappings" section (`#controller-mappings`,
  TOC updated): SDL's mapping data decides the layout, CNA ships no database, `SDL_GAMECONTROLLERCONFIG`
  corrects mappings (CNA `docs/platform-input-notes.md` "Gamepad backend & mapping"); evidence
  `Sdl3EventMapperTests`, `GamePadMappingTest`. Gamepad/haptics services SDL3-only. NOTE: the expansion
  source `audit/data/bible/expansions/WPB5/wpb5-evdev-controller-mappings.html` is now stale — re-applying it
  would restore the evdev text.
- **input-model** — relative-mode/global-pointer/focus wording for SDL3 + terminal only; renderer table
  without the retired identities, EasyGL = OPENGLES3/OPENGL33/WEBGL2.
- **host-devices** (tray via SDL3 on Windows/Linux/macOS builds), **sensors-and-vibration** (SDL3-only
  sensors, evdev clause removed), **touch-and-gestures** (SDL3 finger events), **text-input-and-ime**
  (`SDL_StartTextInput` rule), **media-contract** (SDL user folders, XDG under HEADLESS/TERMINAL).
- **development/internals/input/events** — description/meta, service table, pump diagram, keyboard/mouse
  paragraphs, `VirtualMouseWarp`, tests table (`Sdl3InputServicesTests` 41), build conditions and reading
  order rewritten for SDL3 | HEADLESS | TERMINAL.
- **development/internals/modules/devices-ext** — services table SDL3 vs HEADLESS/TERMINAL; real
  `Sdl3ServiceTest` dialog tests; Win32 dialog/CNA-BUG-182 prose removed. **media** — Win32 known-folder
  row/diagram entry removed.
- sound-effects-and-streaming, xact-runtime, index: no change needed (ALSA statements accurate).
- Links removed (paths absent at c1c316b9): Win32Platform.cpp, Win32EventMapper.cpp, Win32InputServices.cpp,
  X11Platform.cpp, Win32SystemServices.cpp, Linux/Evdev*.cpp/.hpp, LinuxEvdevMappingTests.cpp, the deleted
  site pages development/internals/platforms/{x11,wayland,win32}.html, and inline links to the removed
  cna-bug-182 page. New CNA links use c1c316b9 paths that exist.
- Remaining checker hits are only inside generated "Known issues in this area" blocks (events.html:284
  CNA-BUG-133 title naming a retired renderer; :286/:288 Wayland/Win32 titles; devices-ext.html:269 CNA-BUG-182
  title and its now-missing page) — they need the known-issues regeneration.
