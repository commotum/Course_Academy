# Current source classification and bounded generation scope

Read at math basis **2691**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`.
The complete current Pull, source comparison and image hashes are retained under
`reference/replenishment/initial/` and `reference/replenishment/source-diff.json`.
This supplements the immutable basis-1356 classification and source replay; it
does not replace or rewrite that evidence.

There are now twelve source practice questions: ten moderate and two unrated.
The fieldless q-72754 capture has been replaced upstream by a complete moderate
five-choice radio source. Its second included angle is now **36.4 degrees**;
its correct answer is **90**. All other nine previously captured prompts,
solutions, fields and values are unchanged. Added Pull `:db/id` values inside
difficulty refs are representation differences, not reclassification.

| Source | Structure and supplied data | Field and complete bank | Solution stages | Plot rating |
|---|---|---|---|---|
| q-72754, current | General quadrilateral; AB=6, AD=8 at A=85°; DC=14, BC=16 at C=36.4°; infer BD | Radio: 85, **90**, 61, 78, 24 | 1/2·6·8·sin85° → 24·sin85° → 23.9087; 1/2·14·16·sin36.4° → 112·sin36.4° → 66.4629; add → 90.3716 → 90 | Heavy; changed prompt and solution rasters |
| q-54340 | Parallelogram; AB=10, AD=6 at A=38°; infer BD | Radio: 41, 45, 39, **37**, 35 | ABD: 1/2·10·6·sin38° → 30·sin38° → 18.470; double → 36.940 → 37 | Heavy |
| q-54338 | Parallelogram; DC=21, CB=12 at C=66°; infer BD | Radio: 245, 222, 205, 192, **230** | CBD: 1/2·21·12·sin66° → 126·sin66° → 115.107; double → 230.214 → 230 | Heavy |

All three prompt rasters were visually inspected. q-54340 shows a blue sector
at A, light blue parallelogram fill and the marked lengths at AB/AD. q-54338
shows the blue sector at C and lengths at DC/CB. Their solution rasters add BD.
The corrected q-72754 diagram shows the A/C angles and four lengths in the table.
All current referenced raster bytes are hashed and present locally.

The two added parallelograms share the sine-area-and-doubling method but have
BD solution masks with triangle ABD or CBD. Eligible marked vertices and their
incident sides are mathematical target slots; they are not new operations.
A future extension can parameterize the included-angle vertex, both incident
edge labels, the complementary diagonal and the triangle names together.
Version 5 retains its validated AC parallelogram masks; **BD parallelogram
masks are classified, not claimed implemented**. The new profiles have opaque
numerical distractors: each listed value is retained exactly, with no inferred
historical misconception recipe. Their whole banks and the current q-72754
bank are evidence only, outside the frozen raw-replay API. No unmatched source
option is silently reported as reproduced.

The current twelve questions therefore comprise the previous eight backbone
families, the now-complete BD general radio mask formerly fieldless, and two
BD parallelogram solution-mask variants. Observed practice remains moderate;
easy and hard retain the explicitly authored, same-method scopes documented
in the original classification. No source rating is altered by this job.

Normal generation uses the previously validated complete method-derived banks,
not any opaque observed bank. It executes all three declared difficulties with
existing masks, independent mathematical/diagram checks, actual current
learner grading and mathematical deduplication. Unsupported source profiles
are explicit in `capabilities.json`; this is a template coverage bound, not a
claim that a difficulty is filled. Current inventory is rechecked under the
application lock before planning and after exact-basis receipt verification.
