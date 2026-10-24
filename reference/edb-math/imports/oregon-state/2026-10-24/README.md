# F26 assignment import: PRQ-9 and GD-4

Committed to EDB database `math` at **T6229**. The vault was read without modification.

Compared all 43 assignment Markdown files under `/home/jake/Developer/study/vault/F26/{255,256,341}` with database activity identities and the learner's assignment links. Forty-one were already imported; these two were missing:

| Assignment | Problems / questions | Deadline, Pacific |
| --- | ---: | --- |
| MTH 341 GD-4: determinants of matrix sums | 1 | October 23, 2026, 11:59 p.m. PDT |
| MTH 341 PRQ-9: §§4.10.1–4.10.2 | 5 | October 23, 2026, 11:59 p.m. PDT |

The explicit source times are preserved as `2026-10-24T06:59:00Z`. Stable assignment identities derive from course and assignment code, preserving the existing import naming convention across file renames. Source references, the unnumbered reading definition, the original GD response, authored answer references, and worked feedback are retained. Four free-response fields remain free responses; one legitimate prose blank (“trivial solution”) stays text, and the zero-vector question is radio. No source difficulty, runtime estimate or full-task Math Academy equivalence is invented. The lesson matches supply component coverage, as qualified in the vault.

## Targets and coverage

Resolved the seven mapped coverage topics and four explicit prerequisite topics against their local lessons' verified `lesson-id` metadata and existing EDB topics. They total **10 unique topics**. Five were already targets; the transaction adds:

- Linear Independence in Abstract Vector Spaces (1908)
- Linear Span of Vectors in N-Dimensional Euclidean Space (1852)
- Basic Properties of Determinants (1771)
- Linear Dependence and Independence (1861)
- Linear Combinations of Vectors and Their Properties (1105)

All 10 explicitly linked coverage/prerequisite topics are now under `:learner/targets`. The authoritative reverse `topic/next` graph was also audited: expanding every prerequisite ancestor reaches 594 topics. The import defaults to the recommended explicit assignment links after the optional scope question received no reply during independent work. Those 594 ancestors were not all added as explicit learner targets. The existing curriculum graph is unchanged.

The learner now has **43 assignments and 169 targets**, up from 41 and 164. Assignment coverage is attached to each assigned problem using the existing importer convention; original topic/prerequisite distinctions and lesson paths are recorded in `source-audit.json`.

## Transaction and verification

[transaction.edn](transaction.edn) is one additive transaction attributed to the existing `:course-academy.source/editor` contributor. It creates 37 content entities and adds two learner assignment links plus five target links. The request was guarded against T6228, rechecked all candidate identity absences and preserved learner sets, and committed at T6229.

Request key: `f26-prq9-gd4-64d14a9cb636c3c167690db2-b6228`.

Payload SHA256: `64d14a9cb636c3c167690db2819d947e12a55c5654e106e23073e22e7d332f17`.

Native schema and answer-field validation passed. Exact db-after readback verified all 37 entities and 137 authored attributes, every requested target, both assignment links, and every original assignment and target. The receipt has no retractions; the only existing entity changed was the learner, through the two additive link attributes. Tasks, responses, grades, knowledge profiles, XP and engine settings were not changed.

All six questions rendered through the unmodified player with no JavaScript errors, MathJax errors, raw TeX leaks or missing assets. Screenshots of the determinant response and span definition were inspected. The native application at T6231 successfully listed all 43 assignments and displayed both complete new assignment previews. Replaying the transaction speculatively at T6231 produced only transaction metadata and **zero material changes**.

See `receipt.edn`, `verification.json`, `native-preview-verification.json`, `native-read-verification.json`, `replay-verification.json`, and `render/rendering.json`.
