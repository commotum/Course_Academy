# Classification

Captured database **math**, basis **1356**, lineage **01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1**. The complete wrapper is `source.json`; topic and route wrappers are `topic.json` and `lesson.json`.

| Source | Observed rating | Template | Field | Complete bank | Plot |
|---|---|---|---|---|---|
| q-160365 / 17592186129504 | absent | linear_legacy | radio, 5 scalars | observed-linear-legacy | none in source; generated solution rectangle |
| q-160379 / 17592186129506 | absent | quotient | radio, 5 logarithmic scalars | observed-quotient | none in source; generated solution rectangle |
| q-160870 / 17592186371899 | easy | linear | radio, 5 rational scalars | observed-linear | light, solution rectangle |
| q-160891 / 17592186371913 | moderate | reciprocal | radio, 5 logarithmic scalars | observed-reciprocal | light, solution rectangle |

The unrated originals lack worked solutions and correct designations. Public observed profiles preserve all three omissions. Normal completions explicitly author easy for the linear legacy family and moderate for the quadratic quotient family; these are not recovered ratings. Both full source banks also occur in `/home/jake/Developer/MA/DATA/Lessons/1998/Source/1998.json`, question widgets 160365 and 160379. Those widgets provide five choices and no captured correct key.

The actual response demand is **area**, not only a rectangle. The canonical example supplies a quadratic quotient/product transformation and uses four stages: boundary mapping, inverse-map determinant, reciprocal determinant, area integration. The linked lesson route runs Introduction → Change of Variables Formula → A Worked Example → this KP → Transformations Not Given → Type I Region. The given-map sibling boundary excludes discovering a transformation or integrating over a nonrectangular transformed region. Prerequisites in the KP are Inverse Function Theorem, Double Integrals Over Rectangular Domains, Properties of Double Integrals.

Authored hard: `u=c/(xy), v=d x^3 y`, nonunit integer `c,d` in 2..4. It retains the same four stages, while both derivative rows carry coefficients and the determinant/cancellation has a nonunit cubic power. Moderate fixes unit coefficients and exponent two; hard cannot accept that workload via explicit parameters. No original is rated hard. Equal-level choices of coefficients and rectangle bounds are unordered variations.

Source errors are retained in evidence: q-160870's first-quadrant phrase contradicts its full-parallelogram solution; q-160891 changes the positive Jacobian to negative inside an absolute value and reverses differential order in its double integral. Set braces in both source solutions are literal TeX grouping braces rather than visible delimiters. Normal output applies the smallest presentation/math repairs; raw profiles are explicitly ineligible.
