# libcna.com update plan — 2026-07-02

Source of truth: `/rv/data/development/github.com/openeggbert/cna` (real project state, verified directly:
`NEXT.md`, `known_bugs.md`, `AUDIT.md`, `GRAPHICS_TASKS.md`, `git log`, header count, test count).

Goal: bring every factual claim on libcna.com in line with the real current state of CNA, close
disclosure/consistency gaps, and raise overall site quality to a genuinely top-notch (špičkové) level.
Never fabricate URLs/links/IDs — leave those as explicit TODOs if the real value isn't known.

## Ground truth (verified 2026-07-02)

- Unit tests (`CnaTests`, GoogleTest): **1,813 / 1,813 pass**, 0 known failures. (Site currently says 374, 1 pre-existing failure.)
- Public headers: **280**. (Site currently says 271.)
- Separate from the unit suite: EasyGL integration tests (~63 executables) have 2 known pre-existing
  failures (`easygl_device_dispose_order_test`, one pixel-readback test tied to the Vulkan
  SpriteBatch bug below); Vulkan integration tests 11/13 historically pass; Bgfx is smoke-tested only
  (no pixel readback API). These are backend integration tests, not part of the "374/1813" unit stat —
  the site currently conflates the two.
- Known bug (confirmed, undisclosed on site): multiple `SpriteBatch::Begin()/End()` pairs in one frame
  silently drop all but the last batch. Confirmed on Vulkan. Workaround: one Begin/End per frame.
- Backend maturity roughly matches what architecture.html's table already says (EasyGL/SDL_RENDERER
  stable, Vulkan ~93%, Bgfx ~82%, WebGPU not started/not in CMake at all) — good, don't need to
  re-derive this, just fix the couple of stale labels noted below.
- `cna-samples` is a real, separate repo. Cross-checked directly against `PLAN.md`'s status table and
  the actual `samples/` directory: **31 of 83** targeted XNA 4.0 samples are confirmed ✅ Done
  (Platformer, CatapultWars, GameStateManagement, Pathfinding, ParticleSample, Audio3D, GesturesSample,
  etc.); 5 more directories exist on disk (Spacewar, BloomSample, ColorReplacement, ReachGraphicsDemo,
  Yacht) but are marked Deferred/Todo — excluded from any "done" count to avoid overclaiming.
- `cna_audio`/`cna_devices`/`cna_graphics`/`cna_input`/`cna_net` are NOT separate products — they're
  worktree branches of the same `cna` repo. Site correctly does not present them as separate libraries;
  keep it that way.
- A second, separate minimal site already exists at `cna.openeggbert.com` — relationship to libcna.com
  is undecided; needs a decision from Robert, not something to silently paper over.

## P0 — Accuracy fixes (do first)

- [x] 1. Sitewide stat refresh: `374` → `1,813` (prose) / `1813` (code/terminal-output blocks),
      `271` → `280`. Done via targeted phrase-level Python replace across all 18 affected files;
      verified zero stray matches remain (confirmed docs/tutorials/70-procedural-geometry.html's `374`
      substring was a false positive inside an unrelated magic number and was correctly left alone).
- [x] 2. Removed/corrected the "1 pre-existing failure" claim tied to the *unit* test count — now
      reads "0 known failures" / "no known pre-existing failures" wherever it appeared.
- [x] 3. Reconciled all "~95% of XNA 4.0 implemented" / "~95% API surface implemented" claims down to
      `~85%` for consistency. This was bigger than initially scoped: beyond `docs/roadmap.html`'s
      heading, the exact same stale footer sentence was baked into **87 tutorial pages (14 through
      100)** plus `docs/platforms.html`'s footer — found via a second, broader sweep after the initial
      374/271 fix, since these didn't contain either of those numbers. Fixed via a targeted batch
      replace; verified zero "~95% API surface implemented" instances remain. Also corrected
      `docs/roadmap.html`'s stale "Vulkan: full 3D textured/lit pipeline is the remaining gap" framing
      (leftover from before Vulkan reached ~93%) in three places on that page.
- [x] 4. Fixed `showcase.html`'s false CI claims — reworded to "manual smoke test" / "no automated CI"
      framing (3 spots: intro paragraph, CI-role callout, platform table row).
- [x] 5. Disclosed the known Vulkan SpriteBatch multi-Begin/End bug in `features.html`'s Vulkan card
      and `roadmap.html` (also mentioned the separate `easygl_device_dispose_order_test` integration
      failure there for completeness).
- [x] 6. Fixed `architecture.html` stale Vulkan labels (ASCII diagram + directory-tree comment) to
      match the page's own ~93% framing.
- [x] 7. Removed the dead TODO comment in `index.html` above the GitHub link.

## P1 — Sitewide technical/SEO quality

- [x] 8. Added `<link rel="canonical">` to all 140 pages (root + docs + tutorials), derived
      deterministically from file path; verified exactly one canonical tag per file afterward.
- [x] 9. Fixed `index.html` `og:url` from `/index.html` to the bare domain `https://libcna.com/`.

## P2 — Content depth (real, verifiable additions)

- [x] 10. Expanded the existing (but thin, 2-card) "Sample Applications — cna-samples" section on
       `showcase.html` with an accurate count (31 confirmed ports, verified against the real
       `cna-samples/PLAN.md` status table and cross-checked against the actual `samples/` directory
       listing — deliberately excluded 5 directories that exist but are marked Deferred/Todo in PLAN.md
       to avoid overclaiming) and 4 new representative cards spanning full games, AI/pathfinding,
       audio, and touch gestures.
- [x] 11. Refreshed `roadmap.html`'s "What's new" timeline with the recent Texture2D FNA-conformance
       work and the cna-samples milestone. Also fixed `docs/roadmap.html`'s stale Vulkan "remaining
       gap" framing (see item 3).

## P3 — Needs a decision from Robert (do not guess)

- [ ] 12. Asked about the relationship between libcna.com and the pre-existing `cna.openeggbert.com`
       site (redirect it, retire it, or keep both intentionally distinct) — no response received:
       left as-is, not touched. Re-ask or revisit later.
- [ ] 13. TODO placeholders that need real-world values (not fabricatable): `videos.html` YouTube video
       IDs + channel link, `contact.html` Android/Play Store link + author contact + cna-demo repo
       link, `demos.html` APK download links. Leave as visible TODO badges until real links are
       supplied.

## Also fixed along the way

- [x] 14. `search-index.json` carried the same stale "374-test suite" phrasing in 3 description fields
       (getting-started/migrate-xna/unit-testing tutorial entries) — fixed to 1,813; verified JSON
       still parses.
- [x] 15. Post-edit validation: re-swept the entire repo for `374`/`271`/stale-percentage patterns
       (zero remaining outside the one legitimate magic-number false positive), verified the
       `architecture.html` ASCII diagram box stayed character-aligned after the Vulkan label edit, and
       ran an HTML tag-balance check on the most heavily edited pages (all clean).

## Out of scope but flagged once

- Security: all `cna`/`cna_*` sibling repos have a GitHub personal access token embedded in plaintext
  in their `.git/config` remote URL. Not a website task — recommend rotating/removing it separately.

## Execution order

P0 (1→7) first since these are direct factual corrections a visitor could catch and lose trust over,
then P1 (8→9, mechanical), then P2 (10→11, additive), then ask about P3 (12) once, leave P3-13 alone
unless Robert supplies real links.
