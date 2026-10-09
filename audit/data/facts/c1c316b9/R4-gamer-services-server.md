# R4 — Gamer Services and cna-gamer-services-server (facts for the move to CNA c1c316b9)

Internal audit record, not served. Research only: nothing was built, run or edited outside this file
and `worklist-gamer-services.md`.

**Pins.** CNA **C = `c1c316b9c7a846ce8002809c151fcd1af14942c9`** (branch `apple/m4-stabilization`,
2026-10-09), read via Git objects only; previous site pin **B = `b0e97bb1bb876f9b3edd6f4ff1ef3067908ae8ac`**
(2026-10-04). Previous fact sheet for this area: `audit/data/facts/b0e97bb1/R8-gamer-services.md`
(server then at `9bd5173`).

**Citation prefixes.**
`SA:` = archive `~/Downloads/cna-gamer-services-server-apple-m4-stabilization.zip`, path inside
`cna-gamer-services-server-apple-m4-stabilization/` ·
`SN:` = archive `~/Downloads/cna-gamer-services-server-next.zip`, path inside
`cna-gamer-services-server-next/` ·
`SG:` = local clone `/rv/data/development/github.com/libcna/cna-gamer-services-server` (read-only) ·
`C:` = CNA at C (`git -C …/cna show c1c316b9:<path>`) ·
`W:` = libcna.com working tree.
Where `SA:` is cited for a file that is identical in `SN:` and `SG:@4ab12fd`, the same line numbers hold
in all three (see §1).

---

## Executive summary

1. **Two archives, neither has `.git`.** The *next* archive is content-identical to the local clone's
   commit `4ab12fd` (develop = next, 2026-10-07). The *apple/m4-stabilization* archive (zip
   2026-10-09 17:26, files 2026-10-08 22:37) is the **newest state**: `4ab12fd` plus four changed
   files that are exactly the macOS portability work CNA records as AM4-071 and AM4-178. No Git SHA can
   be proven for it (§1).
2. README.md, HANDOFF.md, protocol/, docs/, tools/ (except loadlab.py) and migrations/ are
   **identical** in both archives; protocol and migrations are unchanged since `9bd5173`, and CNA at C
   vendors byte-identical protocol headers and golden vectors (§1.4).
3. The server is CNA-owned, MIT, C++23, **"not Xbox LIVE compatible"** (SA:README.md:10-12;
   SA:protocol/v1.md:3). `hello` advertises **37 capabilities**; the dispatcher has **59 public
   operations**; schema **23** (§2-3). Every contract item the owner listed is verified (§3).
4. **Linux handoff qualification, 2026-10-07** (SA:HANDOFF.md:94-98): 46 configured tests, **29
   applicable passed in 48.86 s, 17 CNA-harness tests skipped (exit 77), 0 failed**; ASan/UBSan
   **19/19**; focused TSan **3/3**; Release benchmark smoke completed (178 req/s steady, 187 req/s login;
   SA:docs/ai-final-infrastructure-campaign.md:158-160). All owner-expected numbers match (§4).
5. **That run had no CNA processes at all** (all 17 harness tests skipped). The latest Linux run *with*
   CNA's harnesses is still CNA's GS-AUDIT-P4 run of 2026-10-02 at server `9bd5173`: 40 registered,
   **33 passed, 7 skipped, 0 failed** (C:audit/gamer-services/evidence/phase4/server-final.log) (§4.2).
6. **Conformance** (independent black-box): **20 smoke cases** + **1** deliberate ~61 s wall-clock
   relay-ticket-expiry case (default profile 21/21 in 70.0 s), guard over **all 59** dispatcher
   operations (verified by counting both sets) (§4.3).
7. **macOS (AM4-071 → AM4-178 → AM4-208)**, Apple M4, Homebrew Boost **1.92**, CNA harnesses linked
   against Homebrew **curl 8.22**: first **37/46 pass, 7 skip, 2 fail**; after AM4-178 the 2
   (127.x loopback) cases skip with exit 77; final recorded state **37 passed, 9 skipped, 0 failed**
   (CNA writes it "46/46, 9 skip"). Against Apple's system **libcurl 8.7.1** (no WebSockets) **10**
   CNA-driven tests fail (§5).
8. **The server's own docs were not updated for macOS**: SA:README.md:47-48, SA:HANDOFF.md:215-216,
   SA:docs/ai-final-infrastructure-campaign.md:172 still say macOS untested/unvalidated; CNA's
   `docs/gamer-services-known-limitations.md` #28 (C) also still says "Windows and macOS clients and
   server hosts not run". The macOS evidence exists only in CNA's plan and `docs/apple-platforms.md` (§10).
9. **Operator/maintainer infrastructure is new since 9bd5173** (all in `4ab12fd`): CMake presets,
   `tools/qualify.sh` tiers, conformance, six-worker loadlab, scratch-only chaos, authenticated
   CSRF-protected admin web UI, systemd/container/Compose/nginx-L4 templates, verified online
   backup/restore, loopback `/healthz` `/readyz` `/metrics`, JSON logs, `--help`/`--version`, a
   34-chapter offline handbook with 17 labs (§6).
10. **CNA-side user-visible delta B→C** in gamer-services/net: relay refused by name
    (`RELAY_SECURE_WEBSOCKET_UNAVAILABLE`) when libcurl lacks ws/wss (AM4-044/123); SystemLink
    discovery fixed on macOS (AM4-043); online host-migration data hold (AM4-200); Guide input priming
    fixes (AM4-086/090); avatar robustness (AM4-008, MSR-021, AM4-046); voice never probed in cross
    builds (MSR-030) (§7).
11. Site impact (details in `worklist-gamer-services.md`): every "Evidence and qualification" block in
    tutorials 162-168, `docs/gamer-services.html`, the two roadmaps, `docs/xna-compatibility.html`,
    tutorials 97/123 and the services deep dives/internals still carry the 40/33/7 server numbers and/or
    "macOS not qualified"; tutorial 168 and the server section of `docs/gamer-services.html` describe the
    pre-handoff build/backup/monitoring/deployment story; four pages still contain claims from before
    the online service existed.

---

## 1. Source identity

### 1.1 Archives (untrusted data, extracted into separate scratch directories; nothing executed)

| | `cna-gamer-services-server-next.zip` | `cna-gamer-services-server-apple-m4-stabilization.zip` |
|---|---|---|
| Zip mtime | 2026-10-07 21:19 | 2026-10-09 17:26 |
| Zip SHA-256 | `a227b0921880c88f3b57ae6cf2c62617e64c5188a77a9fc68293508f0d93ae5f` | `a3abd4706c873ca605b6fff0963af4e061709b0decc61e247eb02dbf47c684c4` |
| Entries / bytes | 212 files, 1,189,221 B | 212 files, 1,190,963 B |
| File mtimes | 2026-10-07 21:10:19 (= commit time of `4ab12fd`) | 2026-10-08 22:37:46 |
| `.git` present | **No** (no `.git` at any depth) | **No** |
| Honest identity | **content-identical to `4ab12fd`** of the local clone: `git archive 4ab12fd` vs extracted tree, `diff -rq` = no differences (content only; file modes not compared) | **no verifiable commit**. = `4ab12fd` + 4 changed files (below). CNA plan AM4-178 (C:plans/plan_apple_m4.md:166) names server commit **`f74f42e`** on branch `apple/m4-stabilization`; a read-only `git ls-remote origin` on 2026-10-09 reports `refs/heads/apple/m4-stabilization` = `f74f42e9c3e4ddbd4eee522c15b7eaac330159a5`, but that object is **not** in the local clone, so archive = `f74f42e` is *consistent but unverified*. Refer to it as "the `apple/m4-stabilization` archive of 2026-10-09". |

**Current/newest:** the apple archive. It is a strict superset of next/4ab12fd (no file added or
removed; same 212 paths).

### 1.2 apple vs next (`diff -rq`, then `diff -u`)

| File | Change | CNA record |
|---|---|---|
| `CMakeLists.txt:80,248` | `service_benchmark_smoke` and `service_loadlab_smoke` gain `SKIP_RETURN_CODE 77` | AM4-178 |
| `tests/service_benchmark.py` | `prlimit --nofile=48:48` (util-linux, Linux-only) replaced by `resource.setrlimit` in `preexec_fn`; new `distinct_loopback_sources_available()` probe binds 127.0.0.2 and returns 77 with a printed reason when it fails; `raise SystemExit(main())` | AM4-071 (prlimit), AM4-178 (probe) |
| `tests/ServiceTests.cpp:288` | `for(int batch=0;tokens.size()<33;++batch)` → `while(tokens.size()<33)` (unused variable; the "one Clang-only `-Werror` diagnostic") | AM4-071 |
| `tools/cna-gamer-services-loadlab/loadlab.py` | `import socket`; the same 127.0.0.2 probe → exit 77 | AM4-178 |

HANDOFF.md, README.md, protocol/, docs/, migrations/ are identical — the apple branch did **not** update
any document for macOS.

### 1.3 Local clone (read-only)

`SG:` branches: `develop` = `next` = `origin/develop` = `origin/next` = **`4ab12fd593b9db036e8b5228fbaa32146b9de4cb`**
(2026-10-07 21:10:19 +0200, "feat: prepare gamer services for human ownership"; tree
`6ec78a5a9077c627daec132aa990eb696ad76abb`); `main` = `origin/main` = `9bd5173` (2026-10-02). No
`apple/m4-stabilization` ref is fetched locally. `9bd5173..4ab12fd` is a single commit: 80 files,
+7,754/−47; in `src/`+`include/` only 9 files (+289/−29: Listener diagnostics, Main options/logging,
Service counters, EventListener hello, Admission); **no change** in `protocol/` or `migrations/`.

### 1.4 Compatibility with CNA at C

- Protocol unchanged since `9bd5173`; HANDOFF.md:3-4 "The public control/relay v1 contracts remain
  compatible; no CNA source change … is required."
- CNA at C vendors byte-identical copies (`cmp`): `modules/gamer-services/src/Internal/Protocol/CnaService/{Protocol,RelayProtocol}.hpp`
  = SA:protocol/include/CnaService/…; `modules/gamer-services/tests/fixtures/service-protocol-v1.json`
  = SA:protocol/golden/v1.json; `modules/net/tests/fixtures/relay-protocol-v1.json` = SA:protocol/golden/relay-v1.json.
  Drift test `GamerServices_ProtocolDrift` (C:cmake/Harnesses.cmake:564-566) runs when
  `CNA_GAMER_SERVICES_SERVER_ROOT` (default `${CMAKE_SOURCE_DIR}/../../cna-gamer-services-server`) has `protocol/v1.md`.
- The one server-side behaviour change relevant to clients: the event WebSocket hello now accepts
  exactly `v`, `id`, `game`, `token` (SA:HANDOFF.md:18-19; campaign:76-79). CNA's client sends exactly
  those four (C:modules/gamer-services/src/Internal/GamerServicesBackend.cpp, `connectEvents`, `Json hello{{"v",1},{"id","events"},{"game",…},{"token",…}}`).

---

## 2. What the server is

- "An independent C++23 service for CNA" providing "accounts and Guide sign-in, gamer profiles and
  pictures, friends and presence, achievements, leaderboards with Ranked arbitration, messages and player
  reviews, parties, avatars, the online session directory with invitations and host migration, an event
  channel that pushes change hints, and the relay that carries online NetworkSession traffic" (SA:README.md:3-8).
- **"It is not Xbox LIVE compatible."** "Protocol, accounts, assets and binaries are CNA's own; no Xbox
  LIVE wire format, service binary or proprietary asset is used or reproduced" (SA:README.md:10-12);
  "There is no Xbox LIVE wire, account, binary or service compatibility. XNA objects never cross this
  protocol" (SA:protocol/v1.md:3). XNA/Xbox-like only in workflow (XNA names mapped: `GameUpdateRequiredException`,
  `GamerPrivileges`, `PartySize`, `FriendGamer.HasVoice`, …).
- MIT (SA:LICENCE; README:11-12). Project version **0.1.0** (SA:CMakeLists.txt:3; `--version` prints
  `cna-gamer-services-server 0.1.0`, SA:src/Main.cpp:37 + CMakeLists.txt:63).
- System dependencies: OpenSSL ≥3, Boost ≥1.74 (headers, Beast), SQLite ≥3.38, nlohmann/json ≥3.11
  (SA:README.md:53-54); `ccache` required by the maintained presets (README:65; HANDOFF:26).
  Tests: Python `websockets` pinned in `tests/requirements.txt`; optional `slirp4netns` executed, never
  linked (README:310-325).
- One process, one SQLite database (WAL), in-memory relay and event hubs; a second process on the same
  database refuses `DATABASE_IN_USE` (OS lock on `<database>.lock`: `flock` on Linux and macOS, unshared
  open on Windows) (SA:README.md:160-170). Two Asio network threads, four service workers, two separate
  sign-in (scrypt) workers (SA:docs/ai-final-infrastructure-campaign.md:30-32).
- Endpoints, one TLS port: control `POST /cna/v1`; files `GET /cna/v1/files/<sha256>`; events WSS
  `/cna/v1/events`; relay WSS `/cna/relay/v1` (SA:README.md:28,35-36; SA:protocol/relay-v1.md:11-13;
  SA:tools/cna-gamer-services-deploy/README.md:21-23 "There is no separate relay/event port").
- Defaults: `--listen 127.0.0.1`, `--port 47831`; diagnostics only when `--diagnostics-port` is given,
  default diagnostics address 127.0.0.1, non-loopback refused (SA:src/Main.cpp:20-28,51-64; operations.md:21-24).
- Schema **23** (SA:include/CnaService/Store.hpp:40 `SchemaVersion = 23`; 23 migrations
  `001_initial.sql`…`023_friend_voice.sql`; README:113 "current schema (23)" — the stale "(20)" noted in
  the b0e97bb1 audit is fixed, campaign:49-50).
- No public instance is evidenced anywhere (unchanged from R8 §7). The *source repository* is public.

## 3. Contract coverage (owner's list verified)

`hello` returns 37 capabilities (SA:src/Service.cpp:194): identity, authentication, session-refresh,
heartbeat, friends, friend-requests, presence, presence-status, game-defaults, gamer-zone, achievements,
assets, leaderboard-reads, leaderboard-list, title-version, local-leaderboard-commit,
leaderboard-epoch-abort, ranked-arbitration, messages, player-reviews, avatars, avatar-catalog-packs,
files, session-directory, session-removal, host-migration, session-add-members, session-invitations,
join-friend, parties, events, relay-tickets, relay, request-outcomes, privacy, friend-voice,
policy-refresh. CNA refuses a feature whose capability is missing (README:20-21).

| Owner's item | Verified by | Capability / ops |
|---|---|---|
| Accounts / sign-in | README:25; v1.md:11,249 (`auth.login` scrypt N=32768, 1 h tokens, 30-day rotating refresh families, replay revokes family) | identity, authentication, session-refresh, heartbeat |
| Profiles / pictures | v1.md:16 (`profile.get`, `gamer.lookup`, gamer zone, reputation); README:98 (`picture` admin cmd); README:28 (hash-addressed PNG/GLB, `files`) | gamer-zone, assets, files |
| Friends and friend requests | README:26; v1.md:18,35-45 | friends, friend-requests |
| Presence | README:26; v1.md:18 (`presence.set`, `presence.status` online/away/busy) | presence, presence-status |
| Achievements | README:28; v1.md:23 (≤128 per title, idempotent award) | achievements |
| Leaderboard reads/writes | README:29; v1.md:75-141 | leaderboard-reads, leaderboard-list, local-leaderboard-commit, leaderboard-epoch-abort |
| Ranked arbitration | README:29; v1.md:143-169 (row counts when a strict majority of reporting machines sent an identical row) | ranked-arbitration |
| Messages | README:30; v1.md:171-185 (200/sender/hour, 100 stored/recipient) | messages |
| Player reviews | README:30; v1.md:16 (reputation 5×prefer/(prefer+avoid)) | player-reviews |
| Avatars and avatar catalog packs | README:31,327-344; v1.md:187-245 | avatars, avatar-catalog-packs |
| Session directory | README:32; v1.md:279-349 (≤1024 live sessions/title, 16/host) | session-directory |
| Session removal | README:32 (`RemoveFromSession`) | session-removal |
| Host migration | README:32; v1.md:351-364 | host-migration |
| Additional local gamers | README:32 (`AddLocalGamer`); v1.md:366-375 | session-add-members |
| Invitations | README:32; v1.md:377-430 (64 live incoming/recipient/title, 32 sends/hour) | session-invitations |
| Join-friend | README:32 | join-friend |
| Parties | README:33; v1.md:450-467 (account-level, ≤8 incl. invitations) | parties |
| Title versioning | README:34,92; v1.md:7 (`UPDATE_REQUIRED` → `GameUpdateRequiredException`) | title-version |
| Event WebSocket hints | README:35,38-41; v1.md:501-526 (topics invitations/messages/friends/party; hints only; ≤8 channels/account, 4096 total) | events |
| One-use relay tickets | README:36; relay-v1.md:103-131 (256-bit, ≤60 s, consumed once, SHA-256 stored) | relay-tickets |
| Authenticated WSS relay for ENet datagrams incl. NetworkSession voice | README:36,38-41; relay-v1.md:1-18 ("CNA's game data and its NetworkSession voice frames alike"; server injects source identity; no P2P, no NAT traversal) | relay |

Present but not on the owner's list: account-wide XNA `GameDefaults` (game-defaults), replay-safe
request IDs committed with their outcome (request-outcomes, schema 21), operator-set `GamerPrivileges`
and two-way block lists enforced by the service (privacy, schema 22), `FriendGamer.HasVoice`
(friend-voice, schema 23), live privilege/block refresh on `auth.ping` (policy-refresh; README:120-129).

**Not provided** (SA:README.md:43-49): Xbox LIVE compatibility; self-registration / password change over
the wire; motto and region; TrueSkill; time windows for `...Recent` boards; direct peer-to-peer; store
(Marketplace), PartnerToken, title-update delivery.

## 4. Qualification evidence

### 4.1 Linux handoff run, 2026-10-07 (server `4ab12fd`; no CNA harnesses)

Verbatim (SA:HANDOFF.md:94-98): "Final Linux loopback evidence on 2026-10-07: full qualification
configured 46 tests, passed all 29 applicable tests in 48.86 seconds, explicitly skipped 17 unavailable
CNA harness tests and failed none. Serial ASan/UBSan passed 19/19 unit/component tests; focused serial
TSan passed 3/3. The Release benchmark completed steady, login and descriptor-pressure smoke profiles."

Details (SA:docs/ai-final-infrastructure-campaign.md):
- :154-157 the single full run included conformance, all ten load smoke profiles, all nine chaos cases,
  admin-web security, diagnostics, backup/restore, protocol golden vectors and strict documentation checks.
- :146-148 ASan/UBSan serial with leak detection; LeakSanitizer could not run under the managed ptrace
  sandbox, so the authoritative run used the same binaries outside it.
- :149-150 focused TSan covered concurrency lifetime, admission and relay flow; `cppcheck`: two reviewed
  coroutine false positives, no actionable defect.
- :158-160 Release benchmark smoke: **178 req/s** steady, **187 req/s** login; descriptor pressure left
  the server alive and a later `hello` returned OK — "local comparison data, not capacity promises".
- :12 host: Debian Linux, GCC 14.2.0, CMake/Ninja, OpenSSL 3.5.7, SQLite 3.46.1, Python 3.13.5.
- :171 "CNA source and harness executables were unavailable. No CNA test is claimed as passing."
- :20-24 baseline before the campaign (at 9bd5173, same environment): 23 applicable passed, 17 skipped.
  :82-83 intermediate: 41 configured, 24 passed, 17 skipped.

**Test inventory at 4ab12fd / apple archive (46 `add_test`, SA:CMakeLists.txt:257-277):**

| Group (CTest label) | Count | Members |
|---|---|---|
| `unit` | 19 | service_unit, ranked_migration, privacy, database_lock, atomicity, directory, arbitration, avatars, avatar_validation, social, invitations, relay_protocol, relay_authorization, relay_flow, picture_privacy, numeric_persistence, admission, progress_trust, concurrency_lifetime |
| `integration` (local, no CNA) | 10 | tls_e2e, benchmark_smoke, relay_wss, backup_restore, cache_authorization, diagnostics, conformance_smoke, loadlab_smoke, chaos_smoke, admin_web |
| `cna-harness` (need CNA programs; exit 77 without) | 17 | cna_directory, cna_relay, cna_relay_nat, cna_owned_enet, cna_owned_enet_nat, cna_session, cna_session_nat, cna_invite, cna_invite_nat, cna_avatars, cna_session_restart, cna_session_restart_nat, cna_session_migration, cna_session_host_crash, cna_session_add_gamer, cna_session_host_crash_loopback, cna_session_add_gamer_loopback |

19 + 10 = 29 applicable without CNA. `9bd5173` had 40; `4ab12fd` added admin_web, backup_restore,
chaos_smoke, conformance_smoke, diagnostics, loadlab_smoke (`diff` of the two `add_test` lists).
Of the 17 harness tests, 7 need Linux user+network namespaces and `slirp4netns` (the five `_nat`, plus
`host_crash` and `add_gamer`); their `_loopback` twins do not.

### 4.2 Latest Linux run *with* CNA processes (CNA GS-AUDIT-P4, 2026-10-02, server `9bd5173`)

C:audit/gamer-services/evidence/phase4/server-final.log:85 "100% tests passed, 0 tests failed out of
40", 204.18 s; skipped exactly `service_cna_relay_nat`, `_owned_enet_nat`, `_session_nat`, `_invite_nat`,
`_session_restart_nat`, `_session_host_crash`, `_session_add_gamer`. **`service_cna_session_host_crash_loopback`
and `service_cna_session_add_gamer_loopback` passed** — so the site's phrase "the skipped seven are the
NAT-isolated variants, the host-crash test and the AddLocalGamer test" (W:docs/tutorials/166-online-sessions.html:177)
is imprecise: the namespace-isolated host-crash and AddLocalGamer variants skipped; their loopback
variants passed. CNA-side suites in the same audit: GamerServices **649** passed, Net **524** passed,
0 failed, 0 skipped (C:audit/gamer-services/gamer-services-handoff-phase4.md:73-74; audit.md:7) — still
the latest dated Linux totals for those suites in CNA's records at C.

### 4.3 Conformance (`tools/cna-gamer-services-conformance/`)

- Black-box: real TLS/WSS listener, fixtures provisioned only through the admin CLI, no SQLite access,
  no CNA (SA:tools/cna-gamer-services-conformance/README.md:3-5; HANDOFF:107-111).
- Default profile **21 cases** incl. a deliberate ~61 s wait proving wall-clock relay-ticket expiry;
  `--smoke` = **20 cases** (skips only that wait; CTest `service_conformance_smoke`) (README:25-28;
  conformance.py:811-838 — 20 entries in `cases`, `relay ticket wall-clock expiry` inserted only when
  `include_slow`). Expanded run 21/21 in 70.0 s (campaign:75).
- Coverage guard: `PUBLIC_OPERATIONS` (conformance.py:38-47) has **59** operations; the dispatcher set
  `operations{…}` (SA:src/Service.cpp:192) has **59**; `tools/cna-gamer-services-docs/check.py:122-134`
  fails on drift either way.
- Scope (README:65-75): every operation exercised, "not a claim that every boundary permutation is";
  relay datagrams are small opaque probes, "not an ENet compatibility claim"; loopback, not LAN/NAT/
  remote/proxy/failover.

### 4.4 Chaos, loadlab, benchmark

- **Chaos** (`tools/cna-gamer-services-chaos/`): 9 cases (chaos.py:375-385): SIGTERM durable restart,
  SIGKILL active-session reconnect, disconnect during mutation, broken/expired/replayed relay tickets,
  database busy timeout, controlled database-full (child-only file-size limit), hostile/truncated
  transport, single database owner, corrupted database copy. Accepts a build dir, never a database path.
  "SIGKILL is a process crash. It does not simulate an OS crash, torn storage write, controller-cache
  loss or physical power loss" (README:33-37).
- **Loadlab** (`tools/cna-gamer-services-loadlab/`): `MAX_WORKERS = 6` (loadlab.py:33); 10 scenarios
  (loadlab.py:35-38): ordinary, signin-storm, refresh-storm, session-churn, directory-pressure,
  reconnect-storm, host-migration, events, relay (`small`, `large`, `voice`, `burst`, `idle`,
  `asymmetric` shapes, ≤31 players/session), soak; JSON + optional HTML report; ≤50,000 latency samples.
  "Results are loopback saturation evidence … do not interpret them as public-Internet latency. No
  universal pass/fail performance threshold is embedded" (README:41-44).
- **Committed benchmark** (README:220-253; `benchmarks/2026-09-30-824decd.json`): Release, GCC 14.2,
  Ryzen 7 PRO 7840U, Debian 13, loopback, 64 players, load avg 5-9: steady **1,210 req/s** (p50 48 ms,
  p99 118 ms); sign-in storm 1,013 req/s (p99 411 ms); 160 idle connections from one address 1,161 req/s;
  request-ID table at 90,000 1,335 req/s; descriptors exhausted → keeps serving. "one shared machine's
  figures at one moment". An idle player ≈ 2 requests/minute.

## 5. macOS evidence (AM4-071, AM4-178, AM4-208, AM4-044/123)

All from CNA at C; nothing re-run here. The server's own documents do **not** record any of it (§10).

| Record | What it says (verbatim fragments) |
|---|---|
| **AM4-071** (C:plans/plan_apple_m4.md:87) | "cna-gamer-services-server on macOS (its branch `apple/m4-stabilization`, after the owner lifted the hands-off; `develop` fast-forwarded to `4ab12fd` first): **Boost 1.92 installed from Homebrew**; **one Clang-only `-Werror` diagnostic** in its tests and the **Linux-only `prlimit(1)`** in its benchmark fixed there. With the pinned `websockets` in a venv under the build root and CNA's harnesses from a macOS build linked against **Homebrew curl 8.22**: **37/46 pass, 7 skip** (the `_nat`/host-crash/add-gamer variants need Linux user and network namespaces and slirp4netns), **2 fail** only because they bind many `127.x.y.z` source addresses and macOS configures only `127.0.0.1` on `lo0` (aliases need `sudo ifconfig`). Against macOS's **system libcurl 8.7.1**, which has no WebSocket support, the relay and event channel refuse by name (AM4-044) and **10 CNA-driven tests fail** -- which curl CNA should use on macOS is an owner decision." Status Done. |
| **AM4-178** (plan:166) | server branch `apple/m4-stabilization`, **`f74f42e`**, classified APPLE LIMIT: `service_benchmark_smoke` and `service_loadlab_smoke` probe 127.0.0.2 and "where it is not routed, says why and exits 77, which CTest reports as a skip". "Evidence: both report `Skipped` through CTest on the M4 with the reason printed; the server suite's other **27 tests pass, 17 skip** on harness/NAT prerequisites" (that run without harnesses: 27 + 2 + 17 = 46). |
| **AM4-208** (plan:210) and C:docs/apple-platforms.md:223 | Phase 4 close-out at CNA `fdd33d2c6`: "cna-gamer-services-server **46/46** (with CNA's client harnesses from a Homebrew-curl tree, **9 environment skips**)"; table row: "PASS WITH KNOWN LIMITATION | 46/46, 9 skip, with CNA's client harnesses from a tree linking Homebrew curl | 7 skip (Linux network namespaces), 2 skip where 127/8 is not routed (`AM4-178`). A CNA build that links the SDK's libcurl 8.7.1 has no WebSocket support and refuses the relay transport by name (`AM4-123`), so the harness-driven tests need one that found Homebrew curl". |
| **AM4-044** (plan:60; commit `14f74e81f`) | Apple's system libcurl 8.7.1: `curl_url_set(SCHEME,"ws")` without `CURLU_NON_SUPPORT_SCHEME` turned a valid configuration into `RELAY_CONFIGURATION`; now the intended `RELAY_SECURE_WEBSOCKET_UNAVAILABLE`. "**Owner decision:** with the system libcurl the relay cannot work on macOS; Homebrew curl 8.22 has ws/wss." |
| **AM4-123** (plan:132; commit `a1c0c4d91`) | rule is the pure function `relayTransportRefusalFor(version, protocols, tls)`; accepted: 8.11 and 7.86.0 with ws+wss+TLS; refused: 7.85, Apple 8.7.1's protocol list, ws without wss, no TLS backend, no protocol list. `RelayTransportTest` 5/5. |
| C:docs/c-api/CONSUMING.md:167-168 | "The SDK's own libcurl works for TLS but has no WebSocket support, and a build that found it refuses the online relay transport by name." |

**Honest summary of the macOS state (Apple M4, CNA-recorded):**
- Server built on macOS with Homebrew Boost 1.92 after one Clang-only `-Werror` fix in a test and the
  removal of the Linux-only `prlimit(1)` from the benchmark (owner expectation said "Clang-specific
  issues" — the record says **one** diagnostic).
- Final recorded result with CNA harnesses (Homebrew curl 8.22): **46 configured, 37 passed, 9 skipped,
  0 failed**. Skips: 7 need Linux user/network namespaces + slirp4netns (inherently Linux-specific);
  2 (`service_benchmark_smoke`, `service_loadlab_smoke`) need distinct 127.x source addresses that macOS
  does not route without `ifconfig lo0 alias` (exit 77 since AM4-178; before it they **failed**).
- Derived from the counts (not separately itemised by CNA): the 37 passes are the 19 unit/component
  suites (incl. `service_database_lock`, the `flock` path), the 8 other local integrations (TLS E2E, WSS
  relay, backup/restore, cache authorization, diagnostics, conformance smoke, chaos smoke, admin web) and
  10 CNA-harness tests (directory, relay, owned ENet, session, invite, avatars, restart, migration,
  host-crash loopback, AddLocalGamer loopback).
- Apple's system libcurl 8.7.1 lacks ws/wss: the CNA relay refuses with
  `RELAY_SECURE_WEBSOCKET_UNAVAILABLE`; the event channel cannot connect (CNA's events client sets
  `CURLOPT_PROTOCOLS_STR "wss"`, C:GamerServicesBackend.cpp:951, and simply retries; clients keep
  polling). AM4-071 phrases both as "refuse by name"; in code only the relay has a named refusal. All 10
  CNA-driven server tests fail against it. Note: libcurl is a **CNA client** dependency; the server
  itself does not use libcurl (Boost.Beast/OpenSSL).
- Scope: one Apple M4, loopback; no remote network; the changes live on the server branch
  `apple/m4-stabilization` (not on `develop`/`next` = `4ab12fd` as of 2026-10-09).
- Related CNA-side macOS networking evidence: SystemLink discovery fixed (AM4-043:
  `TwoProcessLoopbackTest` 8/8, ENet suites 81/81 on the M4); online host-migration fix verified 30/30
  repeats and "all **304** networking cases pass" (AM4-200, Metal Debug tree); Metal Guide/gamer-services
  UI tests **130/130** (AM4-086, AM4-090). iOS: `CNA_ENABLE_NET=OFF` is required (no libcurl in the iOS SDK;
  AM4-105; C:docs/apple-platforms.md:117-119) — GamerServices and Net are not built for iOS.

## 6. Operator/maintainer infrastructure (all new in `4ab12fd`, unchanged in the apple archive)

| Item | Facts (citations) |
|---|---|
| CMake presets | `dev` (`build-agent`, RelWithDebInfo, ccache launcher), `release` (`build-release`), `asan` (ASan+UBSan, `build-asan`), `tsan` (`build-tsan`); build presets: dev/release 6 jobs, asan/tsan 1 job (SA:CMakePresets.json:8-56; HANDOFF:36-39). CMake ≥3.25, Ninja. |
| Qualification entry point | `tools/qualify.sh quick` (dev build + 19 unit suites, `-L unit`), `normal` (all configured tests), `security` (asan preset, serial, `detect_leaks=1`), `performance` (release + `service_benchmark.py --smoke`), `full` (normal + `tools/cna-gamer-services-docs/check.py --strict`); `CTEST_PARALLEL_LEVEL=6` (1 for sanitizers); prints `ccache --show-stats` (SA:tools/qualify.sh; HANDOFF:80-92). Exit-77 harness skip "means unavailable, never pass" (HANDOFF:90-91). Internal note (not for publication): if the configured ccache dir is not writable, qualify.sh exports `CCACHE_DIR=${TMPDIR:-/tmp}/cna-gamer-services-ccache` (qualify.sh:15-29) — this contradicts the openeggbert build rules on this machine (one shared ccache, no builds under /tmp) if it ever triggers here. |
| Conformance | §4.3. |
| Loadlab | §4.4. |
| Chaos | §4.4. |
| Admin CLI | `cna-gamer-services-admin <db> <command>`: title, title-minimum-version, user, achievement, leaderboard, seed-leaderboard, asset, privilege, picture, avatar-catalog, avatar, game-defaults, inspect, inspect-online, revoke-user, expire-access, reset-earned, reset-online; secrets/JSON on stdin; never prints a credential; no arbitrary SQL (SA:README.md:84-105; HANDOFF:64-74). Identifiers 1-64 of `A-Za-z0-9._-`; gamertag same set ≤32; password 8-256 **bytes** (SA:src/Protocol.cpp:9-16; src/Store.cpp:226-228). |
| Admin web UI | `tools/cna-gamer-services-admin-web/admin_web.py`, Python stdlib, separate process; reads via fixed parameterised SQLite queries, **all mutations through the C++ admin CLI**; loopback default `http://127.0.0.1:47833/`; mode-0600 password file (rejected with group/other bits); `--read-only`; remote bind needs `--allow-remote` + `--tls-cert` + `--tls-key`; constant-time compare; ≤10 failed sign-ins/source/minute (256-source tracker); ≤16 handler threads; random in-memory sessions, 1 h idle, ≤64; HttpOnly + SameSite=Strict (+Secure under TLS); **per-session CSRF token on every mutation and logout**; CSP, no framing/caching, nosniff; destructive resets need the exact title ID typed; never shows message bodies, verifiers, tokens or relay tickets (SA:tools/cna-gamer-services-admin-web/README.md:1-52). CTest `service_admin_web` incl. a login rate-limit regression (campaign:120-123). |
| Deployment templates | `tools/cna-gamer-services-deploy/`: **systemd** unit (user/group `cna-gamer-services`, `StateDirectory` 0700, `LoadCredential=` for certificate and key, `--diagnostics-listen 127.0.0.1 --diagnostics-port 47832 --log-format json`, `NoNewPrivileges`, `ProtectSystem=strict`, `ProtectHome`, `MemoryDenyWriteExecute`, `RestrictAddressFamilies`, `LimitNOFILE=65536`, `Restart=on-failure`); **container**: multi-stage `debian:13-slim`, ccache + 6 jobs, runtime as UID/GID 65532, `EXPOSE 47831`; **Compose**: read-only root fs, tmpfs /tmp, Docker secrets for cert/key, health check `curl --fail http://127.0.0.1:47832/readyz`, nofile 65536; **nginx** `stream {}` L4 passthrough (listen 443 → 127.0.0.1:47831; TLS and both WebSocket routes pass unchanged) (SA:tools/cna-gamer-services-deploy/{systemd/cna-gamer-services.service,container/Dockerfile,container/compose.yaml,nginx-stream.conf,README.md}). Boundaries: "These are templates: adjust paths and certificate automation and qualify the actual staging host" (HANDOFF:168-172); "Container/systemd examples were not installed on a remote production host" (HANDOFF:216); "Compose YAML parsed locally; Docker itself was unavailable, so an image build is not claimed" (campaign:165-167); nginx example "syntax-reviewed but was not exercised against a remote public network" (operations.md:82-84; deploy README:17-18). |
| Health/readiness/metrics | Opt-in `--diagnostics-port`, **loopback-only plain HTTP** (non-loopback refused): `/healthz` (no user state), `/readyz` (foreign keys on and exactly the expected schema; non-mutating), `/metrics` Prometheus text: `cna_build_info{version}`, `cna_up`, `cna_ready`, `cna_uptime_seconds`, `cna_schema_version`, `cna_database_bytes`, `cna_titles`, `cna_accounts`, `cna_access_sessions`, `cna_directory_sessions`, `cna_pending_invitations`, `cna_connections{surface}`, `cna_refused_connections_total{surface}`, `cna_responses_total{outcome}`, `cna_operations_total{operation}`, `cna_request_duration_seconds` (fixed 1–250 ms buckets + Inf); labels never identify players, addresses, titles, sessions or credentials (SA:docs/operations.md:31-70; README:143-147). CTest `service_diagnostics`. |
| Structured logs | `--log-format human|json` (default human: one statistics line a minute); JSON records `timestamp`, `level`, `event` + bounded fields; never passwords, credentials, relay tickets, request bodies or client IPs (operations.md:26-29; README:145-158). `--help`, `--version` (Main.cpp:20-37). |
| Online SQLite backup/restore | `backup.py`: Python's SQLite online-backup API while serving, `integrity_check` + `foreign_key_check`, fsync, atomic publish, mode 0600, prints one JSON object, `--dry-run`, retention only with `--retain N`. `restore.py`: stop the service first; validates source and result; **refuses to overwrite** (destination must not exist); `--create-directory` (SA:tools/cna-gamer-services-deploy/README.md:35-82; HANDOFF:149-164). `service_backup_restore` proves a live backup and restored credentials/profile/defaults/achievement/friendship/message/leaderboard (campaign:99-101). Stress procedure: SA:docs/disaster-recovery.md. |
| Offline handbook | `tools/cna-gamer-services-docs/site/build.py` (stdlib renderer; no Node/CDN); **34 chapters** (`site/pages/01-…34-`), **17 labs** (pages 31-34; index page 26), SVG sequence diagrams, local search; `check.py --strict` validates links, fenced JSON, migrations/`user_version`/`SchemaVersion`, every admin command and exported metric, and builds the site (HANDOFF:16-17,187-198; docs README:9-12). "Educational; the protocol Markdown remains normative" (HANDOFF:197-198). No visual browser review was possible (HANDOFF:217-218). |
| Source documents | `docs/architecture.md`, `database.md`, `disaster-recovery.md`, `operations.md`, `protocol-implementation-map.md`, `security.md`, `ai-final-infrastructure-campaign.md`; reading order HANDOFF:174-185. |

Security model summary (SA:docs/security.md): hostile-input TLS listener; Beast header cap 8 KiB, body =
protocol maximum, 10 s first-read/handshake deadlines, 5 s keep-alive; JSON bounds before DOM insertion;
exact WebSocket/event/relay envelopes; fixed SQL with bindings; hash-addressed files only; per-address
admission (not DDoS protection); OpenSSL CSPRNG tokens/tickets stored as hashes; stable public error
codes. Residual: single machine/process; cooperative voice policy; restart for certificate renewal;
diagnostics unauthenticated but loopback-only; "Public-Internet penetration testing and third-party
security review were not performed" (security.md:49-56).

## 7. CNA-side delta B → C in `modules/gamer-services`, `modules/net`

`git log B..C -- modules/gamer-services modules/net` (19 commits). User-visible effects:

| Commit / task | Effect for a CNA user |
|---|---|
| `14f74e81f` AM4-044, `a1c0c4d91` AM4-123 | With a libcurl lacking ws **and** wss, version < 7.86.0 or no TLS backend (Apple's system libcurl 8.7.1 is one), creating the online relay now fails with **`RELAY_SECURE_WEBSOCKET_UNAVAILABLE`** before any I/O; at B the same configuration was misreported as `RELAY_CONFIGURATION` (C:modules/net/src/Internal/RelayWebSocket.cpp:15-25,66-80,131). Rule unchanged otherwise; now a tested pure function (RelayTransportTests 4 → **5** TEST macros). |
| `363af6738` AM4-043 | **SystemLink discovery on macOS works between processes** (Apple-guarded): `SO_REUSEPORT` on the shared 61190 socket; the query is also sent to every up interface's own broadcast address (Darwin refuses 255.255.255.255 with `EHOSTUNREACH`); a search sends from its own ephemeral socket so replies are not captured by a host on the same Mac. Linux path unchanged. `TwoProcessLoopbackTest` 8/8, ENet suites 81/81 on the M4 (commit msg; plan:59). Discovery between two physical Macs is not separately evidenced. |
| `fca036f19` AM4-200 | **Online host migration:** after the directory names a new host, a client's `SendData` to that host before it has admitted the client is **held in order** (≤128 messages and ≤`MaxRelayWaitingBytes` = 4 MiB, else `LIMIT_EXCEEDED`) and sent on the host's welcome; a failed session discards it. At B such a reliable message could be silently lost (C:modules/net/src/Internal/ServiceENetSession.cpp, `pendingUpstream`, `flushPendingUpstream`; RelayEnetPolicy.hpp:10). 30/30 repeats (was 8/10), 304 networking cases pass (plan:201). |
| `4f7783a95` AM4-086, `8f86d0371` AM4-090, `c3ec93942` AM4-111, `068cb0a66` AM4-180 | **Guide input:** the 0.5 s wall-clock "idle" rule is gone (on renderers drawing the Guide below 2 fps, no key or button used to register); the Guide primes held keys whenever a new dialog/screen appears on top, judged by a per-process **creation serial** (an identical second message box opened while Enter is held no longer answers itself). Metal Guide/gamer-services UI 130/130. AM4-180 is test-only. |
| `aafdc4987` AM4-008 | `AvatarRenderer` on a renderer that refuses `VertexBuffer` (2D-only) now fails every `Draw` the same clean way instead of segfaulting on the second. |
| `1f2ada05d` MSR-021 | `AvatarRenderer::Draw`: if the background load completes during that `Draw`, that frame still takes the loading path; `State` becomes `Ready` and the model is drawn from the next frame, so a game that initialises bone transforms after observing `Ready` is never handed an uninitialised pose. |
| `09094e939` AM4-046 | `AvatarModel.cpp` (and `cna_math`) built with `-ffp-contract=off` on Clang/GNU: released avatar descriptions assemble the same vertices on arm64 (Apple silicon, Linux aarch64) as on x86-64 (C:modules/gamer-services/CMakeLists.txt:6-14). |
| `04502c85e` MSR-030 | **Voice build rule:** `CNA_ENABLE_VOICE=AUTO` never asks host pkg-config in **any cross build** (`CMAKE_CROSSCOMPILING`; C:cmake/HostPkgConfig.cmake), so a cross-compiled build (Emscripten, Android, iOS, MinGW-w64 from Linux, …) carries no voice and `ON` fails the configure there; at B only Emscripten and Android were excluded (C:modules/net/CMakeLists.txt:25-53). |
| `06f7c05d4` AM4-304 | `<algorithm>` includes (MSVC C2039). Records the fact: "Gamer services and Net had never been compiled by MSVC in CI (CNA's Windows workflows configure `CNA_ENABLE_NET=OFF`)" (plan:306). |
| `5106eff1f` AM4-048, `00e1cfb20` AM4-082, `15f001301` AM4-273, `325e6a990` AM4-275 | Test portability/guards only. AM4-082: `EasyGL_AvatarRenderer_Standard` passes on macOS OPENGL33. |
| `1cac65958` RRC-018 | Example gating lists only current renderers (no user effect; do not name the retired ones publicly). |

Counts at C (for internals pages): `modules/gamer-services`: 65 `src/*.cpp`, 36 test files, **637**
test-macro definitions (B: 634; AvatarRendererTests 30→32, GamerServicesServiceTests 57→58);
`modules/net`: 39 `src/*.cpp`, 30 public headers, 33 test files, **530** macros (B: 529;
RelayTransportTests 4→5). Unchanged CMake facts: `CNA_ENABLE_NET` "Build CNA networking (GamerServices
+ Net, requires ENet)" ON (C:CMakeLists.txt:180); service libcurl ≥7.85, relay libcurl ≥7.86, both
REQUIRED on native non-Android (C:modules/gamer-services/CMakeLists.txt:31-33; modules/net/CMakeLists.txt:59-61).

CNA documents touched in the delta: `docs/gamer-services-known-limitations.md` (only OpenGL ES 2 removed
from #33 and its text), `docs/apple-platforms.md` (iOS needs `CNA_ENABLE_NET=OFF`; server row).
`docs/gamer-services-server.md` unchanged — its line 314-315 "Windows/macOS/browser provider behavior is
not yet verified" is now partly outdated by AM4-071/208.

## 8. Limitations to keep published

From SA:README.md:212-222 / HANDOFF.md:212-222, security.md:49-56, operations.md:80-85, README:43-49,
172-189, 260-278 and CNA known limitations (C:docs/gamer-services-known-limitations.md #1-#4, #16-#17,
#24-#38):
- Single process, single machine, single SQLite writer, in-memory relay/event hubs; **no horizontal
  scaling** or clustering (a second node would need shared relay routing, cross-node events and
  distributed session ownership).
- No built-in distributed-DDoS defence: per-address limits only (32 held / 600 new per minute per
  address, 256 pool, 10 sign-ins/min/address); no server-wide handshake rate; an L4 filter/firewall in
  front is required; no TLS-terminating proxy (breaks per-address limits).
- Evidence is **loopback** (and Linux network namespaces for the NAT-isolation tests): no public-Internet
  latency, loss, failover or capacity claim; loadlab and the benchmark are loopback evidence.
- Deployment templates are **templates**, not proof of a production deployment; no remote production
  install; container image not built in the campaign; nginx example not exercised on a public network.
- Chaos proves process crash recovery, not OS crash, device failure, torn writes or power loss.
- Certificate renewal needs a restart (clients and relays reconnect).
- Voice: opaque relay payload; privacy/communication policy is applied by cooperating CNA clients, with
  privileges/blocks refreshed on the ~30 s heartbeat; not server inspection or instant revocation.
- Achievements and scores are authenticated, validated **client claims**; no anti-cheat; Ranked is
  strict-majority agreement, no TrueSkill.
- Accounts are operator-provisioned; no self-registration, password reset or password change.
- Events are coalesced hints, not data; directory, presence, leaderboards and achievements are not pushed.
- Every online datagram goes through the relay over TLS/TCP (head-of-line latency); no P2P, no NAT traversal.
- Platforms: Linux is the qualified host; macOS has one CNA-recorded Apple M4 run (§5) that the server's
  own docs do not yet reflect; native Windows untested (Windows lock code under Wine only); browser builds
  have no service/relay/voice; iOS builds have no networking (`CNA_ENABLE_NET=OFF`); Android without
  libcurl refuses a configured endpoint.
- The 17 CNA-driven tests are skipped (exit 77) whenever CNA's harnesses are not configured — a skip is
  never a pass; the 2026-10-07 run is server-only evidence.
- Third-party security review / penetration testing not performed.
- No public instance is operated.

## 9. Claims that must NOT be made

- Any Xbox LIVE compatibility, interoperation with Microsoft identity/accounts/avatars, or "Xbox LIVE
  replacement"; XNA/Xbox-like **workflow only**.
- That a public/hosted CNA Gamer Services instance exists, or that libcna.com/network.html offers one.
- Any public-Internet capacity, latency, loss or failover figure; presenting 1,210 req/s or loadlab
  numbers as capacity.
- Horizontal scaling, clustering, high availability, DDoS protection.
- That the systemd/container/Compose/nginx templates prove a production deployment, that the container
  image was built, or that the nginx L4 example was exercised.
- "29/29 passed" without saying 17 harness tests were skipped as unavailable, or "46/46 passed" for
  either Linux or macOS. macOS is **37 passed, 9 skipped, 0 failed** (CNA's "46/46, 9 skip" counts
  skips as non-failures).
- That the 2026-10-07 run exercised real CNA processes (it exercised none).
- That macOS is a "qualified"/"supported production" server host, or that the server's own docs say so
  (they still say unvalidated); that online play works on macOS with Apple's system libcurl.
- Native Windows qualification of server or client.
- Anti-cheat, trustworthy competitive scores, TrueSkill.
- Server-side voice inspection or instant voice revocation.
- Self-registration, password reset, Marketplace/store, PartnerToken, title-update delivery.
- That events/push carry data, or that presence/leaderboards/achievements/directory are pushed.
- Peer-to-peer or NAT traversal.
- Power-loss/OS-crash durability from chaos results.
- That conformance covers every boundary permutation, or proves ENet compatibility (it covers every
  operation; relay probes are opaque bytes).
- That the offline handbook was visually reviewed; that a third-party security review happened.
- A Git SHA for the apple archive (none is verifiable); "the archive is commit f74f42e".
- Retired renderer names (OpenGL ES 2/OPENGLES2 etc.) in any proposed text; direct Win32/X11/Wayland
  platform layers.

## 10. Discrepancies and internal inconsistencies

Against the owner's expectations:
1. All expected numbers verified exactly (46/29/17/0; ASan/UBSan 19/19; TSan 3/3; benchmark smoke; 20
   smoke + 1 expiry; 59 operations). Extra precision: 48.86 s; benchmark smoke 178/187 req/s.
2. macOS: "Clang-specific issues fixed" — the record says **one** Clang-only `-Werror` diagnostic (in a
   test). "Substantial test set ran" = 37 of 46 passed. "relay/event functionality" with system
   libcurl: relay refused by name; event channel just fails to connect (AM4-071's "refuse by name" is
   loose for events).

Inside the server sources (do not propagate to the site):
3. SA:README.md:47-48 "Linux is the tested server host; Windows and macOS builds are unvalidated";
   SA:HANDOFF.md:215-216 "… macOS and native Windows were not tested"; campaign:172 — not updated on the
   apple branch despite AM4-071/178/208.
4. SA:tools/cna-gamer-services-docs/README.md:14 says "26 interconnected chapters"; HANDOFF:17,
   README:78 and the 34 page files say **34**.
5. SA:protocol/v1.md:21 "Privacy and block settings are not provided." contradicts its own `## Privacy`
   section (v1.md:469-499, schema 22) and README:97.
6. SA:protocol/v1.md:483 "Voice is peer-to-peer game traffic" vs relay-v1.md:15-18 "Every datagram goes
   through the relay" (wording: voice is session traffic, relayed online).

Inside CNA at C:
7. C:docs/gamer-services-known-limitations.md #28 "Windows and macOS clients and server hosts not run"
   and its text (:581-583 "no macOS host exists") vs C:docs/apple-platforms.md:223 and AM4-071/208.
8. C:docs/gamer-services-server.md:314-315 "Windows/macOS/browser provider behavior is not yet verified"
   (relay) vs AM4-071/208 (macOS relay ran with Homebrew curl).
9. C:docs/gamer-services-known-limitations.md:661-662 still says "(no Windows or macOS host)" for avatar
   renderers although AM4-082 ran the EasyGL avatar GPU test on macOS OPENGL33; Metal avatar pixels
   remain unmeasured.

## 11. Reusable canonical sentences (sober site style)

- **Server qualification (Linux).** "The server's handoff qualification (7 October 2026, Linux loopback,
  commit `4ab12fd`) configured 46 tests: 29 passed, the 17 that drive real CNA processes were skipped
  because CNA's harnesses were not available (exit code 77, not a pass), and none failed; AddressSanitizer
  and UndefinedBehaviorSanitizer runs passed 19/19 and a focused ThreadSanitizer run 3/3. The last Linux
  run with CNA's harnesses is CNA's audit run of 2 October 2026 (server `9bd5173`): 40 tests, 33 passed,
  7 network-namespace tests skipped, none failed."
- **macOS.** "On macOS (one Apple M4, recorded by CNA's Apple campaign) the server builds with Homebrew's
  Boost after small portability fixes on its `apple/m4-stabilization` branch; with CNA's harnesses built
  against Homebrew curl, 37 of its 46 tests passed and 9 were skipped (seven need Linux network
  namespaces, two need extra 127.x loopback addresses that macOS does not configure), none failed. Apple's
  system libcurl (8.7.1) has no WebSocket support, so a CNA build linked against it refuses the online
  relay (`RELAY_SECURE_WEBSOCKET_UNAVAILABLE`) and gets no event-channel hints."
- **Conformance.** "An independent black-box suite drives the real TLS/WSS listener through public
  interfaces only: 20 smoke cases plus one deliberate wall-clock relay-ticket-expiry case, with a guard
  that all 59 public operations are exercised. It is loopback evidence."
- **Operations.** "The repository also carries loopback-only health, readiness and Prometheus endpoints,
  JSON logs, verified online SQLite backup and a restore that refuses to overwrite, an authenticated,
  CSRF-protected administrator web UI that delegates changes to the admin CLI, and systemd, container,
  Compose and nginx TCP-passthrough templates. The templates are starting points, not evidence of a
  production deployment."
- **Limits.** "One process on one machine with one SQLite writer: no horizontal scaling and no built-in
  defence against distributed floods. Loopback and load-lab results are not public-Internet capacity
  figures."
