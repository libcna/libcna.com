# Phase-3 site errata — Phase-1/Phase-2 statements found wrong while absorbing the Bible

Collected from work-package reports; each item is re-verified against TARGET before the page is corrected (one pass, by the orchestrator).
Status: `open` until the page is fixed and the fix is recorded here.

| # | Page#anchor | Statement | TARGET fact and evidence | Reported by | Status |
|---|---|---|---|---|---|
| 1 | `docs/xna-compatibility.html#microsoftxnaframeworkgamerservices` | the 19-bone avatar rig is "verified by pixel-readback tests" | the pixel-readback tests use a synthetic one-bone quad, not the 19-bone rig | WP15 | open |
| 2 | `docs/tutorials/97-*.html` (SendDataOptions table) | gives XNA's delivery guarantees | in CNA `Reliable` is also ordered and `InOrder` can drop packets (see `deep-dives/services/network-sessions.html#guarantees`) | WP15 | open |
