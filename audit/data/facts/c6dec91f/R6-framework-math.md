# R6 — Framework-math Deep Dives, CNA B=c1c316b9 → T=c6dec91f

INTERNAL AUDIT RECORD (not served).

Scope: the framework-math Deep Dives (`deep-dives/framework/{bounding-volumes-and-intersections,vector-matrix-numerics,
math-value-types-and-layout,curve-evaluation,rectangle-point-and-color,math-coordinate-conventions,index}.html`), the math
statements of `deep-dives/foundations/language-conventions.html`, and a sweep of the other Deep Dives for statements that the
B..T math repairs invalidated.

## 1. Method

* CNA was read, never built or run: `git log/diff/show/grep` at B and T in `/rv/data/development/github.com/libcna/cna`, and the
  extracted tree `~/.cache/libcna-com/cna-target`, whose `modules/math` blobs were checked hash-for-hash against
  `git ls-tree -r c6dec91f modules/math` before use (0 differences). `modules/math` is identical at B and at `v0.1.0`
  (`git diff c1c316b9 v0.1.0 -- modules/math` is empty; B is 22 commits before the tag), and every math commit of B..T is after
  the tag (`git merge-base --is-ancestor`), so "since the 0.1.0 release" is exact for each change described.
* Commits read (all after v0.1.0): 9a5e5d896, 900d0db3b, 1ad0a3916, 5ab1c7729, e1377c437, bd46b6ffe, 0e7be08e0, e4ddea6e0, 0b03b7b21,
  5a44d2c50, 9786d4c93, eef23e6f8, bf209dcbe, 705ea2324, df9234202, 2a245b91f, d753d0997, 62e3f9c56 (tests only), cd211420e,
  a83673fc5. R5 §3/§4 rows CNA-BUG-001..004, 026, 027, 063..067, 069..072, 074, 251, 252, 259 were used as a map; every statement
  written was checked in the T source.
* XNA 4.0: decompiled sources in `/rv/data/development/github.com/libcna/xna4-decomp` (Ray, BoundingBox, BoundingSphere,
  BoundingFrustum, MathHelper, Vector3, Curve, CurveKeyCollection, Model) and an IL listing of the genuine
  `Microsoft.Xna.Framework.dll` 4.0.0.0 (monodis, written to the session scratchpad, used for the `GetHashCode` bodies of Plane,
  Ray, BoundingBox, BoundingSphere and for `BoundingSphereReader.Read`).
* sharp-runtime: `next` checkout at 4e146b90 (not pinned by CNA; exception headers last changed 2026-09-28): `ArgumentOutOfRangeException
  : ArgumentException : SystemException : Exception : std::exception`; `IndexOutOfRangeException : SystemException`;
  `NotFiniteNumberException : ArithmeticException`.
* Counts: `git grep -hE '^\s*(TEST|TEST_F|TEST_P|TYPED_TEST|TYPED_TEST_P)\s*\(' c6dec91f -- 'modules/math/tests/*.cpp'` = 957 (B: 874,
  the page said 873); 42 files (B 27); `EXPECT_FLOAT_EQ` 586 (B 586); `EXPECT_NEAR`/`ASSERT_NEAR` lines with literal 1e-5 / 1e-6 / 1e-4:
  79 / 65 / 8 (method reproduces B's 75 / 64 / 4). `std::bit_cast` in `modules/*` minus tests and examples: 61 lines, 57 outside
  comments at T (59 / 55 at B; the page's earlier "58" was not reproducible).
* No commit, push, `regenerate_site.sh`, `apply_expansions.py fold`, `build_site_indexes.py`; no generated region edited.

## 2. Pages re-verified at T (callout → "source-verified at the pinned commit … c6dec91f")

### deep-dives/framework/bounding-volumes-and-intersections.html (body rewritten from the lede to Evidence)

| Statement at B (removed or rewritten) | At T (evidence) |
|---|---|
| Plane::Transform(plane, matrix) wrong (aliased Transpose symmetrises); worked cases (y=1 + translation → tilted; y=2 rotated → wrong side); workaround code block | Correct (0b03b7b21; `Matrix::Transpose` builds the result from all 16 source fields, Matrix.cpp). Worked case replaced by the pinned one: `Plane(Up,-2)` + `CreateTranslation(0,5,0)` → `Plane(Up,-7)` in value, output and aliased forms (`MatrixTransposeCompatibilityTest.PlaneTransformRetainsTranslatedNonzeroOffset`). Workaround block removed; history sentence kept for readers of the old page. New: matrix overload does not renormalise. |
| Plane::Normalize not described | XNA arithmetic + near-unit shortcut `|len²−1| < 2^-23` (Plane.cpp); CreateReflection/CreateShadow normalise via it (e4ddea6e0). |
| "Plane::IntersectsPoint … All four agree with XNA" | `IntersectsPoint` is a private helper (Plane.hpp `private:`, friend BoundingFrustum); XNA has none; sphere and box classifications agree. |
| Ray–box: 2^-24 threshold, division, zero-direction inside → empty | XNA's clipping: interval [0, FLT_MAX], `|d| < 1e-6`, reciprocal, stationary inside → 0 (e1377c437, Ray.cpp; XNA decomp BoundingBox.Intersects(Ray)). |
| Ray–frustum: origin-only, `NotImplementedException`, worked example XNA 11 / CNA no hit | Full six-plane clipping with XNA's constants (9a5e5d896, BoundingFrustum.cpp; XNA decomp identical). Old example replaced by the pinned camera case: `CreateLookAt((0,0,5),0,Up)*CreateOrthographic(2,2,1,5)`, ray (0,0,7) along −Z → 3 (`BoundingFrustumTest.IntersectsRayUsesTransformedAndCameraFrustumPlanes`); 22-case table (`IntersectsRayClipsEveryPlaneWithXnaBoundaryRules`, recorded by CNA as passing on genuine XNA). |
| Box/Sphere `Contains(BoundingFrustum)` never Disjoint; sphere workaround code | XNA rule: Disjoint via GJK, then corners (5ab1c7729, BoundingBox.cpp/BoundingSphere.cpp); workaround removed. |
| Sphere `Contains(Vector3)` surface → Intersects | Strict; value form wide, output form stores float first (BoundingSphere.cpp, header doc; `SpherePointOverloadsRetainTheirMeasuredStorageBoundary`). |
| Sphere `Contains(BoundingSphere)` squared, larger sphere → Contains | Signed radii vs distance in double (`SphereContainmentUsesSignedRadiusDifference`). |
| — | New: sphere `Intersects(sphere)` strict, external tangency false; `Contains(BoundingBox)` Disjoint-first with inclusive corners; constructor refuses negative radius (e1377c437). |
| Sphere `CreateFromPoints` empty → `std::invalid_argument` | `System::ArgumentException`. |
| Frustum `Contains(Vector3)` exact-zero → Intersects, no tolerance | All six planes, wide distance, Disjoint only > 1e-5, never Intersects. |
| Frustum `Intersects` box/sphere = plane rule (conservative) | GJK (`Gjk.hpp`, `ConvexIntersects`); `FrustumSeparationOracleTests` + `FrustumIntersectionRequiresActualConvexSeparation`. |
| Frustum `Contains(BoundingFrustum)` `this == &frustum` shortcut | Geometric (GJK + corners), no pointer identity. |
| Frustum `GetCorners(vector&)` → `std::out_of_range` | `System::ArgumentOutOfRangeException`. |
| Containment matrix: 8 "no"/"almost" rows | Only `BoundingFrustum::Intersects(Plane)` (CNA-BUG-071) and `Ray::Intersects(BoundingSphere)` (CNA-BUG-069) remain "almost". |

Kept and re-checked unchanged at T: plane conventions, box corner order (still no test asserts it), box inclusive touching, box–sphere
double accumulation, CreateFromBoundingBox last-bit note, Transform radius formula, frustum plane extraction and corner formula,
`PlaneIntersectionType.hpp` swapped Doxygen (CNA-BUG-025). Picking-loop snippet: now labelled "syntax-checked against the headers at
c1c316b9; the declarations it uses are unchanged at TARGET" (no math header used there changed B..T; only BoundingFrustum.hpp and
BoundingSphere.hpp changed, in Doxygen). Links added to surviving entries CNA-BUG-025, 069, 071. Meta description unchanged.

### deep-dives/framework/vector-matrix-numerics.html

* Operation-groups table: arithmetic row (Clamp/Min/Max now XNA's), measurement row (wide Dot/Cross/magnitudes; Vector2/4
  LengthSquared/DistanceSquared single), transforms row (range errors now `System::ArgumentException` /
  `System::IndexOutOfRangeException`, empty ranges, 9786d4c93).
* Same-name table: Clamp vector row (min wins now, eef23e6f8), Max/Min row (scalar NaN in either operand → NaN; vector ternary,
  second operand on tie/NaN; XNA decomp `Math.Max` and Vector3.Max). Paragraph rewritten; Known Issues sentence on Clamp/NaN removed
  (CNA-BUG-027 retired); CNA-BUG-068 linked for division.
* Angles/epsilons: "Decompose uses file-local FLT_EPSILON" removed (that helper is now unused; Decompose uses 1e-4); ray–box 1e-6,
  ray–plane/frustum 1e-5 listed; link text "the two epsilons" → "other numeric details".
* Degenerate table: perspective row (`System::ArgumentOutOfRangeException`, π refused via `MathHelper::Pi`, angle checked first,
  output untouched, NaN fov passes, aspect 0 → infinite M11; 2a245b91f, `MatrixPerspectiveCompatibilityTests`), Decompose row
  rewritten for XNA's algorithm (705ea2324; worked values from `MatrixDecomposeCompatibilityTests`: (−2,3,4)·R·T → (2,3,−4);
  1e-5 refused, 1e-4 accepted; shear 0.2 refused, 0.1 accepted; zero axis and NaN/inf input → true + NaN rotation; 4th column
  ignored). CheckForNaNs → `System::NotFiniteNumberException`.
* Precision section rewritten as a list (bd46b6ffe, 0e7be08e0, df9234202, 5ab1c7729, e4ddea6e0).
* Tests section recounted (§1) and rewritten; FrustumSeparationOracleTests added; compatibility files listed; what is now pinned.
* p3 region **`wpb1-math-static-constants`** touched: only the provenance clause of its code sample ("syntax-checked against the
  headers at c1c316b9, whose declarations used here are unchanged at TARGET"); its facts (constinit Vector2 constants, 11/6
  constants, 141 colours, function-local identity) re-verified unchanged at T. Same provenance wording for the MoveToward sample.

### deep-dives/framework/math-value-types-and-layout.html

* `#two-spellings`: every output-reference form read is alias-safe at T; Transpose (0b03b7b21) and Rectangle::Union (5a44d2c50)
  fixed since 0.1.0; Decompose's scale-wins aliasing (XNA's) noted.
* `#equality` hashes rewritten: vector/matrix/quaternion/point/rectangle/colour/curve-key hashes are XNA's integers (bf209dcbe,
  5a44d2c50, a83673fc5); Plane, Ray, BoundingBox, BoundingSphere still differ (XNA IL adds; CNA XOR / boost mix / std::hash);
  CurveKey `size_t` zero-extension noted. Text: single outer braces (e1377c437), negative zero prints 0 (`DisplayFloat`), CNA-BUG-073
  linked.
* `#exception-families` rewritten (heading text "Argument errors: the System exception types"; id kept; TOC entry updated):
  table of System types at T; hierarchy from sharp-runtime; C ABI barrier (`CnaCApiDetail.hpp`: `System::ArgumentException` →
  `CNA_RESULT_INVALID_ARGUMENT`, argument category; `CnaCApiVectors.cpp` validates unsigned ranges itself).
* Meta description (meta, og, JSON-LD) changed: "…hash and ToString differences, and the split argument exceptions." →
  "…hash and ToString rules, and the System argument exceptions." **The generated copies of the old description are now stale**
  (hub list in `deep-dives/framework/index.html`, related-deep-dive lists in `docs/math-types.html`, `docs/packed-vector.html`,
  `docs/tutorials/51-custom-vertex.html`, `development/architecture/graphics.html`,
  `development/handbook/change-public-xna-behavior.html`, `development/testing/architecture.html`,
  `development/internals/modules/math.html`, and `search-index.json`); they were not hand-edited.
* Graphics-side claims re-checked at T: Texture3D/TextureCube comments and `colorsToRgba`, `VertexPositionColorTests.cpp` comment,
  `GetBackBufferDataCore` Color path, `BuiltInVertexStreams.hpp` (unchanged B..T), 17 packed-vector types (+ HalfTypeHelper),
  14-type `ObjectEqualityContractTests`, CNAEXT compound assignments, C ABI `CNA_Matrix`/`CNA_Color`.

### deep-dives/framework/curve-evaluation.html

* Lede: CNA now follows XNA's segment, step and loop rules; two differences remain.
* Key collection: exact-position in-place replacement and aliasing-safe reinsertion (d753d0997; `ReplacementMayAliasAnotherElement`);
  index errors `System::ArgumentOutOfRangeException`, CopyTo too small `System::ArgumentException`.
* Evaluate: t in double, 1e-10 guard (as XNA). `#step` rewritten: Step uses t (worked values 5 and second key's value recomputed
  from T code; `StepUsesNormalizedSegmentPosition`). Loops table: post-loop Linear uses last.TangentOut (matches XNA); example
  replaced by the pinned one (keys (0,0,TO 2), (1,1,TO 3) → Evaluate(2)=4, Evaluate(1.25)=1.75; `EvaluatePostLoopLinear`).
* `#degenerate` rewritten: duplicate/tiny segments select first key ((1,3),(1,4),(2,5) → 3; `DuplicateAndTinySegmentsMatchXnaSelection`);
  all-keys-one-position cyclic UB kept (CNA-BUG-065, linked); NaN position now NaN (Smooth) / last value (Step), not 0
  (`NaNPositionMatchesXnaForEmptySingleSmoothAndStep`). Smooth tangents unchanged (CNA-BUG-028 linked).
* Example curve values recomputed from T code: unchanged (t = 0.5 exactly in double). Evidence counts: CurveTests 31,
  CurveKeyCollectionTests 25, CurveKeyTests 18.

### deep-dives/framework/rectangle-point-and-color.html

* Rectangle `Union` aliasing note; hash now XNA's wrapped field sum; Point hash X + Y (5a44d2c50); CNA-BUG-075 linked for Point
  operators.
* Color `Multiply` and `Lerp` rewritten for XNA's 16.16 fixed point (1ad0a3916). Worked values derived by hand from Color.cpp:
  `Multiply(Color(100,100,100,100), 1.1f)` = 109 per channel (1.1f·65536 = 72089.6015625 → 72089; 100·72089 >> 16 = 109); Lerp
  black↔white at 0.5 = 127 both ways (floor shift); NaN Lerp keeps the first colour (`NaNLerpKeepsEveryFirstColorChannelIncludingAlpha`
  — the B text "NaN yields 0 in every channel" was wrong for T).
* Re-checked unchanged: half-open rectangle rules, IsEmpty, Center, overflow UB, 141/140/139 colours, float-constructor rounding and
  its 28-case oracle (oracle file unchanged), FromNonPremultiplied, BlendState/SpriteBatch defaults (BlendState.cpp unchanged).

## 3. Pages edited for the delta but not re-verified (callout keeps c1c316b9, "at the stated evidence commit")

* `deep-dives/foundations/language-conventions.html` — p3 region **`wpb1-cpp-dialect-error-model`** touched: the
  `std::bit_cast` clause ("58 places … none in the math sources") → "57 non-comment uses in the production module sources at
  c6dec91f, two of them in the math module's wrapped integer hashes of Point and Rectangle; its float hashes still type-pun through
  std::memcpy" (sentence carries its own commit). Its other math statement (Decompose reports by Boolean) holds at T.
* `deep-dives/content/xnb-type-readers.html` (sweep) — "None checks … non-negative sizes or radii" was invalidated by e1377c437:
  `ContentReader::ReadBoundingSphere` (used by the BoundingSphere reader and `XnbModelGraphReader.hpp` mesh spheres) builds the
  sphere through the constructor, which now throws `System::ArgumentException` for a negative radius; XNA's
  `BoundingSphereReader.Read` (IL) and `Model` mesh reading (decomp) assign the fields without a check. Sentence rewritten with
  "at c6dec91f".

## 4. Pages checked, no change

* `math-coordinate-conventions.html`: its precision statements hold at T (Vector3::Transform wide, Vector4::Transform single;
  CreateRotationZ single-precision sin/cos; Cross sign convention). The page also carries renderer claims not re-read here, so its
  callout stays c1c316b9 / "stated evidence commit".
* `index.html`: hand-written lede still true; callout already names c6dec91f.
* Sweep hits that hold at T: `practice/xna-api-surface-auditing.html` (Ray hash XOR vs XNA add; no frustum output form),
  `reference/verification-tiers.html` (hash overflow "since fixed"), `reference/graphics-quick-reference.html`,
  `graphics/shader-routes-four-answers.html` (CreatePerspectiveFieldOfView call only).

## 5. Ids and regions

* Ids removed: none (checked against HEAD for all five rewritten pages). `#exception-families` keeps its id with new heading text.
* p3 regions touched: `deep-dives/framework/vector-matrix-numerics.html` `wpb1-math-static-constants`;
  `deep-dives/foundations/language-conventions.html` `wpb1-cpp-dialect-error-model`.
* No sidebar, pager, breadcrumb, hub list, `p3:deep-links`/`p3:issue-links` or `<!--issue:KEY-->` text edited.
* Known Issues links added only to surviving entries: CNA-BUG-025, 028, 065, 068, 069, 071, 073, 075 (all present under
  `known-issues/bugs/`).

## 6. Claims not verifiable / not executed

* Nothing was compiled or run. Test results are CNA's records ("recorded by CNA"): the 22 frustum-ray cases vs genuine XNA
  (cna-demos FrustumRayOracle.cs), the frustum separation corpus, ColorFixedPointOracle (1,782 checks), the XNA-measured
  expectations in the compatibility tests.
* New code samples were not added; the three kept samples were syntax-checked at c1c316b9 by an earlier pass and use only
  declarations unchanged B..T.
* XNA's zero-time-range Curve behaviour (inverse span 0 below 1.4e-45) is carried from the earlier verification; `CalcCycle` and
  `InvTimeRange` were re-read in the decomp and are consistent.

## 7. Findings for the coordinator

1. **New CNA-vs-XNA difference (candidate Known Issue):** since e1377c437 an XNB `BoundingSphere`, or a model mesh sphere, with a
   negative radius fails to load (constructor throws `System::ArgumentException`), where XNA's readers assign the fields. Code:
   `modules/content/src/Xna/ContentReader.cpp:174-179`, `modules/content/src/Xnb/XnbModelGraphReader.hpp:70`.
2. CNA's `modules/math/tests/Microsoft/Xna/Framework/RayTests.cpp:211-214` still says the ray–frustum test is omitted because the
   function "throws NotImplementedException" (stale comment; the cases are in BoundingFrustumTests.cpp). Matrix.cpp's file-local
   `WithinEpsilon` (line 97) is now unused.
3. **Non-math effects of cd211420e** make other Deep Dives state stale `std::` exception types (not edited here; outside the math
   scope): `framework/game-class-and-lifecycle.html` (null platform → `System::ArgumentNullException`, Game.cpp:220; the
   "std::invalid_argument (null platform, null or duplicate service, null game or second manager)" list),
   `framework/services-and-components.html` (null provider `ArgumentNullException`, duplicate `ArgumentException`,
   GameServiceContainer.cpp:18/25; second manager `ArgumentException`, GraphicsDeviceManager.cpp:673),
   `framework/window-and-device-manager.html` (null game → `ArgumentNullException`, GraphicsDeviceManager.cpp:78),
   `services/touch-and-gestures.html` (TouchCollection index → `ArgumentOutOfRangeException`), `services/input-model.html`
   (`MouseCursor::FromTexture2D` → `ArgumentException` for both cases), `models/model-mesh-runtime.html` (meshParentBones,
   rootBoneIndex, material variant → `ArgumentOutOfRangeException`, Model.cpp:305-375), `models/skinning-and-animation.html`
   (AnimationPlayer → `ArgumentException`). `graphics/texture-data-transfer.html`'s crop error is still `std::invalid_argument`
   (ImageLoader.cpp:94).
4. Generated copies of the math-value-types description need regeneration (§2).
5. Outside Deep Dives, still describing fixed defects: `docs/math-types.html` (Plane.Transform row, links `#plane-transform`),
   `development/internals/modules/math.html` (`<!--issue:NEW-AUDIT-11-->`, Decompose history; `issue_refs.py check` error).

## 8. Validator results (own pages)

* `check_deep_page.py` on all nine touched/checked pages: ok.
* `check_facts.py`: no finding on deep-dives/framework, language-conventions or xnb-type-readers (124 problems elsewhere).
* `check_retired_renderers.py`: no finding on these pages.
* `check_source_links.py`: 7 failures, all in development/ (c1c316b9 links), none on these pages.
* `validate_site.py`: no finding on these pages (broken links in docs/xna-compatibility.html to retired cna-bug-259/264;
  search/sitemap coverage pending regeneration).
* `issue_refs.py check`: 1 error, `development/internals/modules/math.html` `<!--issue:NEW-AUDIT-11-->`.
