# Classification at math basis 1356

Lineage: 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. All 15 practice records and the canonical example were examined. There are 8 moderate and 7 hard sources, no easy sources, no unrated practice records and no field anomalies. Eleven sources have malformed unescaped literal system braces, repaired to visible escaped braces in generated prompts and solutions. Every source has one radio field named selection, five whole equations k=value, and one correct designation. The canonical example is context, not a sixteenth practice question.

| Level | Template | Response / work | Sources | Plots |
|---|---|---|---|---|
| easy, authored | inconsistent_easy | 2 equations, a=1, coefficient k; integer elimination and contradiction | none | none |
| moderate | inconsistent_bare | coefficient k; one integer elimination | q-32245, q-32331 | none |
| moderate | inconsistent_shift | coefficient k+v; one integer elimination | q-42059, q-131726, q-74646 | none |
| moderate | inconsistent_scaled | coefficient uk; one integer elimination | q-131727, q-74688 | none |
| moderate | inconsistent_scaled_shift | coefficient uk+v; one integer elimination | q-131728 | none |
| hard | dependent_swap | swap to unit pivot, eliminate, identify free variable | q-32246, q-131729, q-74695, q-131730 | none |
| hard | dependent_fractional | fractional elimination, shifted k, identify free variable | q-131731, q-74650 | none |
| hard | dependent_negative | negative affine parameter coefficient, eliminate, identify free variable | q-42021 | none |

The seven observed mathematical templates have fifteen complete observed bank profiles. Wording, alignment, row-operation sign style and white-space variants remain per-source presentation masks. They do not claim additional skills. No source options are pooled. All raw original prompts, solutions, fields and banks are preserved in source.json, and all replay through the normal generator interface.

## Curriculum and missing easy level

The route reconstructed from activity/first-step and step/next is:

Introduction → Solving a Consistent System of Equations Using Gauss-Jordan Elimination → Consistent and Inconsistent Systems of Linear Equations → Classifying a System as Consistent Dependent, Consistent Independent, or Inconsistent → Determining the Value of a Constant for Which a Given Linear System Is Consistent or Inconsistent

The preceding classification tutorial defines inconsistency, dependence and independence. The sibling solving KP uses general NxM elimination and free variables; this KP asks only for k, never a general solution. The later null-space/span topics are excluded. Canonical e-4712 is a two-equation inconsistent system requiring one integer row subtraction and a contradiction. Authored easy retains this exact demand with unit first pivot, bare k, |b|≤4, |d|=2 or 3, small integer constants, and a nonzero residual. This is a design claim, not an observed label. Easy questions differ in multiplier sign, y-coefficient sign and contradiction value, without a within-level progression. Moderate remains the observed inconsistent affine-k problem with integer row multiplier. Bare-k moderate requires |a|≥2, matching the observed non-unit pivots and preventing overlap with the authored easy workload; shifted/scaled families retain observed unit pivots because their k-rearrangement or division adds the observed moderate demand. Hard remains observed dependence with swap, fractional multiplier or negative affine coefficient; every hard instance has proportional constants and one free variable. All explicit parameters obey the same bounds as samplers.

## Inventory reconciliation, 2026-10-15

The live bank at basis 2698 contains 16 practice questions: nine moderate and
seven hard. The added source q-131725 belongs to `inconsistent_shift`, with
`a=2,b=-1,c=3,d=-4,u=1,v=-5,e=-1`. It uses one five-choice radio field
`selection`, requesting a complete equation `k=value`. No additional mathematical
template or plot is needed. Its singular parameter is 7 and its contradiction is
0=5. Its complete source bank is k=10, k=8, k=7 (correct), k=5, k=6.

The original basis-1356 source capture remains intact. The full current capture,
16-bank replay, supplemental variants and grading evidence are retained under
`reference/replenishment/initial/`. Presentation normalization has changed source
formatting since the old capture; current printed systems and complete answer
banks match the exact mathematical replays. Historical solution errors in
q-74695 and q-42021 are conservatively excluded from the validated reserve and
remain unchanged. The authored easy capability and its curriculum rationale
above remain applicable; absence of imported easy labels does not establish an
unsupported band.
