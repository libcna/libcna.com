# R8 — Bible absorption ledger reconciled with the c6dec91f site, CNA B=c1c316b9 → T=c6dec91f

INTERNAL AUDIT RECORD (not served). Concept texts and notes quoted here name retired renderer identities; the public pages do not.

Scope: the ledger records `audit/data/bible/records/*.json` only. No HTML page, script, generated block or other data file was
edited; nothing was committed; `regenerate_site.sh`, `apply_expansions.py fold`, `bible_ledger.py render` and
`adversarial_audit.py counts --write` were not run. CNA was read through Git objects only (`git log/show/grep/cat-file` at T).
The site had already been regenerated, so every cited section was read in its final c6dec91f form.

## 1. Before and after

| Check | Before | After |
|---|---|---|
| `python3 scripts/adversarial_audit.py anchors` | 338 errors: 310 tokens absent from the destination page, 18 destination anchors gone, 10 destination pages gone (retired Known Issues); 0 semantic-claim errors | **0 errors**; 6,004 destinations, 4,866 concepts fully anchored; 44 tokens outside the cited anchor (the same 44 concepts as before, none of them touched here); 140 tokenless current concepts (baseline 141) |
| `python3 scripts/bible_ledger.py check` | 340 errors, 39/119 units audited: 274 tokens not in the page text, 38 SUPERSEDED concepts without `tokens` or `no_tokens_reason`, 18 fragments missing, 10 pages missing | **0 errors, 119/119 units audited** (also with `--final`) |

No error of the kind "the cited section carries a claim the semantic checks reject" occurred, before or after: the regenerated
generated blocks (deep-links, issue-links, sidebars, dev-layers, pagers) carry no rejected claim inside any cited section.

## 2. What was done, per action (338 failing concepts, each decided individually against the current section)

| Action | Concepts | Meaning |
|---|---:|---|
| tokens | 86 | the page still states the concept in new words: `tokens` replaced by exact phrases of the current section |
| tokens + anchor | 5 | as above, and the destination moved: WPB3-rc-034 (renderer-contract `#missing-vertex-inputs` → internals/graphics/backends `#lagging-contract-comments`, where the "inheriting silence is the trap" rule now lives), WP05-ch12-117 (resources `#vulkan-target` → `#deferred-target`), WPB7-d6d-005 and WPB7-d6d-016 (releases `#delta` → `#delta-alpha1`), WPB7-edit-016 (glossary `#term-easygl-profiles` added beside its two anchors) |
| superseded | 133 | the fact changed at c6dec91f: disposition `SUPERSEDED`, `tokens: []`, `replacement_tokens` = the superseding phrase(s) of the cited section, note "Phase 6 (c6dec91f): <why>. Was <disposition> [at …] with tokens […]" |
| rt | 26 | concepts already `SUPERSEDED` whose superseding statement was itself rewritten: `replacement_tokens` re-pointed, note "Phase 6 (c6dec91f): <why>. Was SUPERSEDED … with replacement tokens […]" |
| removed-renderer | 75 | subject is VULKAN, DIRECTX11, METAL or SDL_RENDERER (including the 2D-only-family contract): `REMOVED FUNCTIONALITY`, no destinations/tokens, the established Phase 6 note ("…RRC-031..036; cmake/RendererIdentities.cmake lists it in CNA_RENDERER_RETIRED_IDENTITIES), and <its page became a tombstone \| the rewritten destination no longer describes it \| its section (#id) was removed …>, so the site states nothing current about it. Was …") |
| removed-modern | 1 | WP17-ch59-051 (the EasyGL GPU-timer 32-bit limit): retired modern GPU layer (MRT-001..012, C ABI 0.47.0; `plans/plan_modern_retirement.md`) |
| fixed | 10 | aux-cnabugs entries whose Known Issue was retired as PROVEN FIXED (R5) and whose page no longer exists: `FIXED BUG` (the disposition aux-cnabugs already uses for fixed entries), note naming the fixing commit and test: CNA-BUG-001 (0b03b7b21), -002 and -003 (5ab1c7729), -004 (9a5e5d896), -021 (39ef8ea2f), -026 (2a245b91f), -027 (eef23e6f8), CNA-GAP-048 (21b4cd64c, 169470ee7), CNA-BUG-049 (a83673fc5), CNA-BUG-061 (056398edf, 96c6e77be) |
| obsolete | 2 | documents gone at T: NEXT.md (WP20-ch78-002; bb6607d34 cut it and renamed it handoff.md) and AUDIT.md (WP20-ch78-004; fa70df1ae deleted it) |

Judgement rules applied:
* A concept naming a retired renderer only as one item of a list, or as one of two co-equal clauses whose other clause still holds
  for a survivor, was kept current (tokens on the survivor's wording), not retired: e.g. WP10-ch28-069 and -107 (DIRECTX9 half),
  WP08-ch19-049 (WEBGPU/SDL_GPU "2 behaves as 1"), WP06-ch16-098, WP02-ch11-041 (DIRECTX9's Windows SDK), WP14-ch44-059.
  Where the survivor's half itself changed it became SUPERSEDED (WP10-ch28-047, DIRECTX9 now applies the presentation rules).
* A concept that cites a count or value which changed at T (17 capabilities, 10/8 identities, five compiled-effect options, test and
  file counts, exception types moved from `std::*` to `System::*`, defaults SDL_GPU/OPENGLES3) is SUPERSEDED. Concepts whose text was
  already historical and whose token only tracked the current value (WPB3-rc-041, WPB4-ggc-035, WP14-ch48-005) got new tokens instead.
* Defects fixed at T (math containment and ray clipping, Plane::Transform, ContentManager disposal, ResetElapsedTime, component
  disposal and events, storage disposal/sharing, sensors' Dispose(bool), discovery bounds, network simulation side, mixer teardown)
  are SUPERSEDED by the page's current statement; the retired Known Issue ids are named in the notes.
* Every token and replacement token was copied from the current section; `adversarial_audit.check_concept` passes for all 338.

## 3. `no_tokens_reason` on SUPERSEDED concepts (165)

`bible_ledger.py check` requires `tokens` or a `no_tokens_reason` for every SUPERSEDED concept, and knows nothing of
`replacement_tokens` (which `adversarial_audit.py anchors` checks inside the cited section). The 38 SUPERSEDED-with-replacement-tokens
concepts left by Phase 5 and the earlier Phase 6 pass already failed that check before this work. Every SUPERSEDED concept with empty
`tokens`, non-empty `replacement_tokens` and no `no_tokens_reason` (165: 152 superseded at c6dec91f, 13 left from c1c316b9) now carries
`no_tokens_reason`: "SUPERSEDED at <pin>: the destination states the current fact instead of this concept's claim, so the old tokens were
retired; the superseding statement is anchored by replacement_tokens, which scripts/adversarial_audit.py anchors checks inside the cited
section". Seven concepts that already had the b0e97bb1 reason keep it. The field changes nothing in `adversarial_audit.py`.

**Coordinator follow-up (replaces this section's approach).** `no_tokens_reason` is meant for concepts that cannot be
anchored lexically, and these can: their `replacement_tokens` are phrases on the page. The coordinator therefore removed
the 165 added fields again and changed `scripts/bible_ledger.py` instead: for a SUPERSEDED concept without `tokens`, the
`replacement_tokens` are the tokens it checks against the destination page (so an empty or off-page replacement still
fails). `scripts/test_validators.py` has three fixtures for it (as recorded: passes; no tokens at all: fails; a replacement
token not on the page: fails). `bible_ledger.py check` still gives 0 errors, 119/119 units. The `ntr` column below
records what this pass did, not the final records.

## 4. Per unit

Columns as in section 2; `ntr` = `no_tokens_reason` added.

| Unit | tokens | tokens+anchor | superseded | rt | removed-renderer | removed-modern | fixed | obsolete | ntr |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| appendix-a-core-graphics-quick-reference | 2 |  | 1 |  |  |  |  |  | 1 |
| appendix-c-glossary | 1 |  |  |  | 3 |  |  |  | 1 |
| appendix-d-repo-map |  |  | 1 | 1 |  |  |  |  | 2 |
| appendix-f-ecosystem-quick-reference |  |  | 1 |  |  |  |  |  | 1 |
| appendix-g-verification-tiers |  |  |  |  |  |  |  |  | 1 |
| appendix-h-gltf-evidence-matrix |  |  | 1 |  |  |  |  |  | 1 |
| appendix-i-native-c-api |  |  | 1 | 2 |  |  |  |  | 3 |
| aux-audit | 2 |  | 2 |  |  |  |  |  | 2 |
| aux-audit-3d-gltf-cnj | 3 |  |  |  |  |  |  |  |  |
| aux-audit-alpha1-delta | 2 |  |  |  |  |  |  |  |  |
| aux-audit-architecture-build | 2 |  | 2 | 1 |  |  |  |  | 2 |
| aux-audit-content-xnb-cnj | 2 |  | 4 |  |  |  |  |  | 4 |
| aux-audit-d6e9ff05-delta | 1 | 2 | 1 | 1 |  |  |  |  | 1 |
| aux-audit-framework-core-math |  |  | 8 |  |  |  |  |  | 8 |
| aux-audit-graphics-core-effects | 4 |  | 2 | 1 |  |  |  |  | 3 |
| aux-audit-input-audio-net-services | 1 |  | 1 |  |  |  |  |  | 1 |
| aux-audit-platforms | 1 |  |  | 1 | 1 |  |  |  | 2 |
| aux-audit-renderer-catalog | 2 | 1 |  |  | 6 |  |  |  |  |
| aux-audit-renderer-draw-path-matrix |  |  | 5 |  | 1 |  |  |  | 5 |
| aux-audit-sibling-libraries |  |  |  | 1 |  |  |  |  |  |
| aux-audit-testing-verification | 4 |  |  | 4 |  |  |  |  |  |
| aux-cnabugs |  |  |  |  |  |  | 10 |  |  |
| aux-editorial-audit |  | 1 |  |  |  |  |  |  |  |
| aux-next | 1 |  |  |  |  |  |  |  |  |
| aux-plan |  |  | 1 |  |  |  |  |  | 1 |
| aux-readme | 1 |  |  |  |  |  |  |  |  |
| ch01-cna-and-xna | 1 |  |  |  |  |  |  |  |  |
| ch02-ecosystem-vocabulary |  |  | 1 |  |  |  |  |  | 1 |
| ch04-configuring-building |  |  | 3 | 1 |  |  |  |  | 4 |
| ch05-first-game | 1 |  |  |  |  |  |  |  |  |
| ch06-game-lifecycle |  |  | 6 |  | 1 |  |  |  | 6 |
| ch07-math-conventions |  |  | 12 |  |  |  |  |  | 12 |
| ch08-geometry-color-layout | 2 |  | 10 |  |  |  |  |  | 10 |
| ch09-module-monorepo | 1 |  | 1 |  | 3 |  |  |  | 1 |
| ch10-boundaries-enforcement | 1 |  | 1 |  |  |  |  |  | 1 |
| ch11-dependencies-tools | 4 |  | 2 |  | 1 |  |  |  | 2 |
| ch12-graphicsdevice |  | 1 | 3 |  |  |  |  |  | 3 |
| ch13-spritebatch | 1 |  | 2 |  | 2 |  |  |  | 2 |
| ch14-textures-rendertargets | 6 |  | 3 | 1 | 9 |  |  |  | 4 |
| ch15-stock-effects | 1 |  |  |  | 1 |  |  |  |  |
| ch16-state-objects | 3 |  | 1 | 3 | 2 |  |  |  | 4 |
| ch17-shaders-four-answers |  |  | 2 | 2 | 4 |  |  |  | 4 |
| ch18-vertex-streams-capabilities | 1 |  | 2 |  |  |  |  |  | 2 |
| ch19-renderer-contract | 5 |  | 2 |  | 5 |  |  |  | 2 |
| ch20-selection-identity | 1 |  | 2 | 2 |  |  |  |  | 5 |
| ch21-opengl-fixed-profiles |  |  |  |  |  |  |  |  | 1 |
| ch22-opengl-programmable | 1 |  |  |  | 1 |  |  |  |  |
| ch23-native-modern-gpu | 1 |  |  |  | 4 |  |  |  |  |
| ch24-abstraction-layers-one | 1 |  | 1 |  |  |  |  |  | 1 |
| ch25-abstraction-layers-two |  |  | 1 |  |  |  |  |  | 1 |
| ch26-directx-time-machine |  |  |  |  | 4 |  |  |  |  |
| ch28-modern-direct3d | 2 |  | 4 | 1 | 20 |  |  |  | 5 |
| ch30-vector-rasterizers |  |  |  |  | 2 |  |  |  |  |
| ch33-contentmanager-resolution |  |  | 4 |  |  |  |  |  | 4 |
| ch35-xnb-type-readers | 1 |  | 6 |  |  |  |  |  | 6 |
| ch38-models-meshes | 1 |  | 5 |  |  |  |  |  | 5 |
| ch39-gltf-import-core |  |  | 2 |  |  |  |  |  | 2 |
| ch40-gpu-packing |  |  | 1 |  |  |  |  |  | 1 |
| ch41-skinning-animation |  |  | 1 |  |  |  |  |  | 1 |
| ch42-cnj-model-toolchain |  |  | 1 |  |  |  |  |  | 1 |
| ch43-gltf-conformance |  |  | 1 |  |  |  |  |  | 1 |
| ch44-input-system | 4 |  | 1 |  | 1 |  |  |  | 1 |
| ch45-audio-system |  |  | 3 |  |  |  |  |  | 4 |
| ch46-media-system | 3 |  |  |  |  |  |  |  | 1 |
| ch47-sensors |  |  | 2 |  |  |  |  |  | 2 |
| ch48-host-devices | 1 |  | 1 |  |  |  |  |  | 1 |
| ch50-storage | 4 |  | 4 |  |  |  |  |  | 4 |
| ch51-networking | 1 |  | 2 |  |  |  |  |  | 2 |
| ch59-easygl-metagl | 1 |  | 1 |  |  | 1 |  |  | 3 |
| ch61-cross-platform-contract | 1 |  |  |  |  |  |  |  | 1 |
| ch62-windows-cross-compiling | 1 |  |  | 1 |  |  |  |  | 1 |
| ch63-wine-engagement | 2 |  |  |  |  |  |  |  |  |
| ch67-android-macos |  |  |  |  | 3 |  |  |  |  |
| ch69-counting-discipline |  |  |  | 1 |  |  |  |  | 1 |
| ch70-oracles |  |  | 2 |  |  |  |  |  | 2 |
| ch71-hostile-environments | 1 |  |  | 1 |  |  |  |  | 2 |
| ch72-discipline-as-test |  |  | 1 |  |  |  |  |  | 1 |
| ch73-ci-reality |  |  | 2 | 1 |  |  |  |  | 4 |
| ch77-samples-and-examples | 1 |  |  |  |  |  |  |  |  |
| ch78-project-practice |  |  | 2 |  |  |  |  | 2 | 2 |
| legacy-sdlgpu | 2 |  | 1 |  | 1 |  |  |  | 2 |
| **total** | 86 | 5 | 133 | 26 | 75 | 1 | 10 | 2 | 165 |

## 5. Remaining errors and open items

* `adversarial_audit.py anchors` and `bible_ledger.py check` (with and without `--final`): no remaining error.
* Not a ledger matter, reported for the coordinator:
  * `python3 scripts/adversarial_audit.py counts` reports the generated block in `audit/phase3-adversarial-audit.md` as stale. That
    block is computed from `data/known-issues.json`, `dispositions.json` and `audit/data/adversarial/`, not from the ledger records, so
    the Known Issues regeneration (R5) changed it; it needs `counts --write` at integration.
  * `audit/bible-absorption-phase3.md` and `audit/bible-absorption-phase3-concepts.md` are rendered from the records
    (`bible_ledger.py render`) and still show the pre-c6dec91f dispositions and removed anchors (R2 §8); re-render at integration.
  * `scripts/cnabugs_record.py` rebuilds `aux-cnabugs.json` from `dispositions.json` and `data/known-issues.json`. It looks up each
    surviving candidate's `published_as` entry, so for the ten entries retired at T it would fail (KeyError) or, if adapted, overwrite
    the FIXED BUG concepts and their Phase 6 notes; do not rerun it without carrying the retirements over.
* Hand-written page text noticed while reading cited sections (not edited; not a ledger error):
  * `development/internals/content/runtime.html:215` lists "the unlocked XNB reader registry" among the things concurrent loading must
    audit; at T the registry is guarded by a `std::shared_mutex` (`modules/content/src/Xna/ContentTypeReaderManager.cpp:30-33`), as
    `deep-dives/content/xnb-container-and-object-graph.html#registration` and R4 §3 say.
  * `development/internals/modules/storage.html:254` says the suite does not establish "glob matching with a non-empty pattern", while
    `docs/storage.html#wildcard-patterns` (line 468) says the tests match plain prefixes and suffixes; `StorageDeviceTests.cpp:525-528` at
    T does call `GetFileNames("*.bin")` and `GetDirectoryNames("directory-*")`. The internals sentence should probably narrow to the
    matcher's `?` and case edge cases.

## 6. Method and reproducibility

The failing concepts were collected with `adversarial_audit.check_concept` (the function `anchors` runs), each shown with the old
context of its tokens (HEAD page) and the current section, and decided by hand; the decisions were applied in one pass that writes
`json.dumps(record, indent=1, ensure_ascii=False)` plus the record's own trailing newline (ch08-geometry-color-layout.json keeps
its missing final newline). Only `concepts` changed; ids, order and the record headers are untouched, and outside the 338 decided
concepts the only change is the added `no_tokens_reason` on 13 c1c316b9 concepts. Commits cited in notes were checked to be
ancestors of c6dec91f.
