# Classification

Snapshot: math, basis 1356, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. All nine captured practice questions are included; all are rated and have one complete five-choice math radio field with key `selection`. There are no practice plots, missing fields, legacy duplicates, or missing correct designations.

| Level | Observed templates | Source questions | Field shape | Plot rating |
|---|---:|---:|---|---|
| easy | 4 | 4 | one five-choice radio | none |
| moderate | 5 | 5 | one five-choice radio | none |
| hard | 0; 1 authored | 0 | authored matching radio | none |

## Observed template/profile inventory

- `sparse_trig` / `sparse_trig-observed`: q-39666, easy, parameters `{"a": 4, "b": 3, "c": 2, "d": 1}`. One separate observed bank; four wrong choices and one correct determinant.
- `sparse_exp` / `sparse_exp-observed`: q-161793, easy, parameters `{"a": 1, "b": 1, "c": 1, "d": 3}`. One separate observed bank; four wrong choices and one correct determinant.
- `sparse_square` / `sparse_square-observed`: q-161794, easy, parameters `{"a": 1, "b": 1, "c": 1, "d": 3, "e": 1}`. One separate observed bank; four wrong choices and one correct determinant.
- `log_product` / `log_product-observed`: q-161796, easy, parameters `{"a": 1, "b": 1, "c": 2, "d": 1}`. One separate observed bank; four wrong choices and one correct determinant.
- `rotation` / `rotation-observed`: q-39299, moderate, parameters `{"a": 1, "b": 1, "c": 1}`. One separate observed bank; four wrong choices and one correct determinant.
- `polynomial_column` / `polynomial_column-observed`: q-161792, moderate, parameters `{"a": 1, "b": 1, "c": 1, "d": 1, "e": 1}`. One separate observed bank; four wrong choices and one correct determinant.
- `polynomial_mixed` / `polynomial_mixed-observed`: q-39710, moderate, parameters `{"a": 1, "b": 1, "c": 1, "d": 1, "k": 2}`. One separate observed bank; four wrong choices and one correct determinant.
- `linear_offdiag` / `linear_offdiag-observed`: q-39294, moderate, parameters `{"a": 1, "b": 1, "c": 1, "d": 1, "e": 1, "f": 1}`. One separate observed bank; four wrong choices and one correct determinant.
- `symbolic_diagonal` / `symbolic_diagonal-observed`: q-39664, moderate, parameters `{"a": 1, "b": 1, "c": 1}`. One separate observed bank; four wrong choices and one correct determinant.

## Curriculum and authored scope

The activity route is reconstructed from `activity/first-step` and `step/next` in curriculum-route.json: Introduction → Intuition Behind the Jacobian → this direct-computation KP → The Critical Points of a Transformation → critical-point KP → inverse-transformation KP. Pull collection order is not used. The canonical direct example e-11579 derives a constant 3×3 Jacobian by two first-row cofactors. Key prerequisites are The Jacobian (1999), Finding Determinants Using Laplace Expansions (1770), and Basic Properties of Determinants (1771).

Easy and moderate preserve all observed labels even where a diagonal symbolic moderate case has fewer arithmetic steps than an easy nonlinear case. No inferred ordering between these observed families is claimed. Variations within each family keep its nonzero pattern, operators, degree, coefficient number form, chosen row/column and exact teaching-stage count. All coefficients are nonzero signed integers of magnitude 1–4; the mixed-polynomial offset is -4..4 and is excluded from mathematical task identity. Method profiles additionally guard the nonunit pivot coefficients that distinguish their complete error operations. Explicit calls enforce the same bounds.

Hard is an authored design claim. The Introduction already displays x=u sin(v) cos(w), y=u sin(v) sin(w), z=u cos(v), nine first partials, two cofactor minors, a w-identity, and then a v-identity. The hard template scales these three displayed components independently by signed integers of magnitude 1–4. Every hard instance has the same nine derivatives and the same two identity reductions; no inverse, zero-locus, critical-point, volume, or integral response is requested. The 8³=512 derivative matrices are distinct; signs/scales affect actual derivative/cofactor calculations. A fixed radial degree 1 and angular arguments v,w prevent unrelated chain-rule/arbitrary-algebra escalation.

## Source fidelity and repair policy

Complete source answer banks replay publicly through the normal API. Raw strings remain immutable in source.json. No source mathematical repair was needed. Mathematics is rendered with normalized LaTeX, including grouped negative multiplicative factors; raw prompt/solution typography counts are separate from complete mathematical/prose/stage fidelity. The logarithm source naturally has domain uvw>0; this is recorded outside learner content without changing its prompt. Fixed symbols a,b,c,theta are treated as independent real constants when comparing symbolic answers.

Scalar or compound wrong expressions do not reveal a unique causal mistake. Profiles flagged evidence-only in PROFILES preserve those complete parameterized expression patterns but are not sampled as normal learner banks. All observed replay profiles are evidence-only, including the rotation and symbolic-diagonal banks, which also have separate method profiles. Answer count is always five, and the entire instance is rejected on any symbolic equivalence collision.

Hard uses only first partial derivatives of supplied component functions, product/chain rules and the same sine/cosine identities already displayed in the Introduction. Spherical coordinate interpretation, conversion, and geometric properties are not assessed or requested.

The actual source SVG formula glyph sequence was read and decoded (formula-inspection.json): [x,y,z] = T([u,v,w]) = [u sin(v) cos(w), u sin(v) sin(w), u cos(v)]. Its original asset hash is retained. This is a rendered formula, not a geometric assessment diagram.
