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
