# Phase-3 site errata — Phase-1/Phase-2 statements found wrong while absorbing the Bible

Collected from work-package reports; each item is re-verified against TARGET before the page is corrected (one pass, by the orchestrator).
Status: `open` until the page is fixed and the fix is recorded here.

| # | Page#anchor | Statement | TARGET fact and evidence | Reported by | Status |
|---|---|---|---|---|---|
| 1 | `docs/xna-compatibility.html#microsoftxnaframeworkgamerservices` | the 19-bone avatar rig is "verified by pixel-readback tests" | the pixel-readback tests use a synthetic one-bone quad, not the 19-bone rig | WP15 | open |
| 2 | `docs/tutorials/97-*.html` (SendDataOptions table) | gives XNA's delivery guarantees | in CNA `Reliable` is also ordered and `InOrder` can drop packets (see `deep-dives/services/network-sessions.html#guarantees`) | WP15 | open |
| 3 | `about.html` | FNA is "built on SDL2" | the FNA reference the Bible cites (`b3551247`) defaults to SDL3 — re-verify against the FNA revision CNA compares with before changing | WP01 | open |
| 4 | `docs/faq.html` (sensors answer) | the whole device layer needs `CNA_DEVICES=ON` | `modules/CMakeLists.txt` always adds the `devices` module (verify: which parts `CNA_DEVICES` gates) | WP01 | open |
| 5 | `docs/tutorials/15-background-music.html` | "after the compiled .xnb and .cnb tiers it tries .mp3, .ogg…" | a loose `.cnj` step precedes the media-native extensions (CNA-BUG-008) | B3 | open |
| 6 | `development/repository/source-ownership.html#third-party` | "Licences are in THIRD_PARTY_NOTICES.md" | the file omits vendored cgltf, stb, ENet, dr_libs (CNA-BUG-045) | B3 | open |
