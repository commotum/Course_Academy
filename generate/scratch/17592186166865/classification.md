# Classification

Immutable source: database `math`, basis 1356, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. KP 17592186166865 belongs to topic 17592186049506 (MA 3216). Seven practice sources: one easy, four moderate, two unrated. All seven use one radio field named `selection`, five math options, one central circle plot. Plot rating **heavy**: the equation must be recovered from the diagram in every question.

| Family | Rated sources | Raw unrated sources | Banks | Solution structure |
|---|---|---|---|---|
| Origin circle | q-127493 easy | q-127359 | 2 | circle equation; five derivative rows; q-127359 raw solution absent |
| Shifted circle | q-127497, q-127499, q-127500, q-127502 moderate | q-127360 | 5 | circle equation; five derivative rows, except q-127499 six rows with final sign rewriting; q-127360 raw solution absent |
| Fractional shifted circle | none | none | 1 authored method bank | same five derivative rows |

q-127359 is assigned easy for evidence routing, q-127360 moderate. Their public raw replay remains unrated: `:question/difficulty`, `:question/worked-solution`, and `:answer-field/correct` are omitted. The assessment attribute omissions are preserved; EDB identity attributes are converted to the established local review shape with generated UUIDs. Their inferred correct options are metadata, never counted as matched original designations.

Lesson order was reconstructed from `:activity/first-step` then `:step/next`: Introduction → Circle KP → Ellipse KP → Parabola KP. Circle prerequisites are Implicit Differentiation (57) and Equations of Circles (843). The introduction differentiates an origin circle, the canonical circle example shifts the center to (0,−1), and moderate practice uses one and two signed integer shifts. The subsequent ellipse and parabola examples delimit this KP; none is included here.

The missing hard level is authored: both center coordinates are nonintegral signed halves with magnitudes at most 7/2. It asks exactly the original response and uses the same circle equation, sum differentiation, chain factors, rearrangement, and division. Its additional workload is retaining two fractional signed shifts, not a new calculus method or evaluating at a point. Center and radius remain explicitly labeled as in original shifted plots; no grid interpolation difficulty is claimed. All hard instances have the same workload, with no internal progression.

Current-inventory reclassification (basis 2626): a later eighth practice source,
q-131253, is a moderate single-blank point-evaluation question using a graph of
f′ and asking for f″(2). It has a different backbone and response contract from
the generic radio slope questions. Its prompt supplies only (2,√5), with no
semicircle graph/equation. The solution assumes radius 3 and the upper branch;
that information is insufficiently specified in the standalone prompt. This
family is excluded from generation and independently validated available counts
until its missing instructional context is recovered. The eight source records
are preserved. See capability.json and the current source read under reference/.

The seven original circle radio records were reread at the current basis and
checked against the captured source fields; extra enum entity IDs in the wider
Pull shape are harmless. Current source replay again passed 7/7 complete banks,
35/35 options, 7/7 prompts and all 5 supplied solutions and answer keys. Unrated
missing-source attributes remain absent. The generator's existing version and
content identities are retained.
