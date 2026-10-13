# Classification

Database math, basis 1356, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. `source.json` is an unchanged copy of the captured wrapper. All 11 practice questions are easy; each has one radio field keyed `selection`, five delimiter-free scalar math answers and a present correct designation. No unrated, moderate or hard practice examples were captured. Canonical e-11156 is analyzed separately and does not count as practice.

| Template | Source IDs | Field/banks | Plot rating |
|---|---|---|---|
| polar | q-160380 | radio, 1 bank | none |
| exp_pair | q-160394 | radio, 1 bank | none |
| quotient | q-160383 | radio, 1 bank | none |
| exp_log | q-160402 | radio, 1 bank | none |
| square_pair | q-160427 | radio, 1 bank | none |
| complex_square | q-160428 | radio, 1 bank | none |
| mixed_linear | q-160431 | radio, 1 bank | none |
| diagonal_trig | q-160440, q-160445 | radio, 2 complete banks | none |
| coupled_trig | q-160434 | radio, 1 bank | none |
| quadratic_linear | q-160387 | radio, 1 bank | none |

All prompts state a transformation then ask for the Jacobian determinant at a column-vector point. All worked solutions introduce the definition, identify x/y, find all four partial derivatives, expand ad-bc, simplify, then substitute the specified point. The functions distinguish ten mathematical families; shared outer Markdown and solution sentences are intentionally reused. Scaling the diagonal trig outputs produces the same derivative/evaluation family but the complete scalar bank changes, so its two profiles remain separate. The generator normalizes legacy aligned column vectors to bmatrix and legacy Unicode trig syntax to standard LaTeX, preserving response shape and wording.

Canonical images have been individually viewed: transformation `(2v cos u, v sin u)`, point `(0,-1)`, general x/y transformation, and repeated point. These are standalone LaTeX bitmaps, not geometric plots. No practice question contains a plot reference.

q-160380 has a source teaching error: the simplification row says `6u(cos²v+cos²v)` although its correctly displayed distributed products yield `6u(cos²v+sin²v)`. Correct final determinant/value and all five source options are valid. Raw text is retained; the smallest mathematically supported correction is applied to generated output. Exact source worked mathematics count: 10/11; corrected: 1/11. This is separate from 11/11 full bank/designation fidelity.

# Curriculum scope and authored level claims

The actual lesson route was traced via activity/first-step and step/next: Introduction → The Jacobian Determinant → Finding the Jacobian Determinant of a Transformation (17592186129187) → this evaluation KP (17592186129263) → A Review of Affine Transformations → Intuition Behind the Jacobian → Local Area Scale Factor → Orientation Regions. Pull collection order was not used. Prerequisite topic edges include partial derivatives using differentiation rules and affine transformations. Local-area/orientation tasks are later separate KPs and are excluded from every authored level.

Easy templates preserve the observed function structures and point arithmetic. Authored moderate uses scaled exponential/log and coupled trig families with explicitly enforced nonunit inner chain factors, exact reciprocal sums or familiar evaluated trig arguments. Compared with easy q-160402/q-160434, it changes derivative coefficient bookkeeping and point arithmetic, while retaining four derivatives and a single 2x2 determinant at one point. These are deliberate bounded workload choices, not recovered ratings. Both moderate families are peer variants, not a progression. `exp(au-bv)` is evaluated with `au=bv` at same-sign integer points under sampling, with unequal coefficients2..7, avoiding large or arbitrary exponential approximations. Every evaluated trig argument has a pi coefficient denominator 1,2,3,4 or6; no 15-degree or exotic radical demands.

Authored hard evaluates `a(u+v)^m, b(u-v)^n` at small signed integer points, anchored directly to the preceding sibling canonical e-6810 `(u+v)^3,(u-v)^2`, together with this KP's point-evaluation canonical. Bounds: m/n pairs (3,2), (2,3), (3,3), scales1..3, point coordinates with absolute value≤4. It adds neither a new derivative rule nor another assessed task: four chain-rule derivatives, ad-bc, then signed integer powers. Every hard variant has comparable workload. Neither missing-level claim implies observed MA rating evidence.
