# Current template extraction

Source snapshot: math basis 2134. Exact original content, fields, choices and identities are retained in `source.json`; original tails and parameters are in `source-cases.json`. Previous radio-bank extraction is retained under `reference/prior-radio-v2/`.

q-19215 places its diagram before the prompt. Its statements are `b =-2e`, `c =-d`, `b = 2e`. Its three checkbox banks each contain the two text values false and true. Correct values are I=true, II=true, III=false. The fixed solution reads the grid displacements b=(-4,-2), e=(2,1), c=(2,5), d=(-2,-5), then confirms the first two equalities and rejects the third. Its difficulty is absent.

q-20404 has the same layout but the distinct statements `a =-c`, `c =-\frac{1}{2}a`, `b = d`. Correct values are I=false, II=true, III=false. Its fixed solution reads a=(6,4), c=(-3,-2), b=(-3,-5), d=(3,5), then confirms the reciprocal relation and rejects the other two. Its difficulty is absent. This is a different statement/value mask, not merely new numbers in the first mask.

The shared purpose is to compare direction and relative magnitude in three complete vector equalities, selecting precisely the true statements. Translation does not change a vector. Negative scaling reverses direction; exact equality also requires the stated magnitude ratio.

| Mask | Computed arrows | Complete statements |
|---|---|---|
| opposite_multiple | e=u, b=sk·u, c=v, d=t·v, unused a=k·u | b=-k·e; c=-d; b=k·e |
| reciprocal_multiple | a=k·u, c=s·u, b=v, d=t·v, unused e=(-4,0) | a=-c; c=-(1/k)·a; b=d |

u and v are nonzero, nonparallel direction families, k is positive, and s,t are ±1. Each source choice is mapped to its own field: I/false and I/true refer to the truth of statement I; II/false and II/true to II; III/false and III/true to III. For each field the true-valued choice is correct exactly when the complete vector equality holds; otherwise false is correct. Thus every source value and incorrect choice has an exact parameterized semantic recipe. No opaque psychological distractor explanation is inferred. There is one complete boolean bank profile per field layout, shared by both masks.

Fixed parts are image-first placement, the question sentence, select-all instruction, Roman bullet labels, field keys, checkbox type, false/true text banks, and source whitespace around equalities. Variable components are signed scalar expressions, exact displacements, diagram tails/tips, image references, and truth values. Rational arithmetic computes vectors and correct values before plotting. No choice is pooled across fields, and every answer UUID belongs to its field.

The source-a and source-b profiles replay their bounded original geometry, prompt, complete answer banks, correct designation and compact worked solution exactly while preserving absent difficulty. They are evidence-only. The checkbox-completed profile generates supported variants with an authored level and a fixed three-bullet solution followed by a true-subset conclusion. This longer explanation follows the canonical example's direction/magnitude sequence; it is a labeled solution-layout extension of the current compact source solutions. One fixed solution is determined by each instance; it never depends on seed or option order.

Sampler bounds are in classification and the script: easy unit/sign relations, moderate doubling/halving, and hard exact 3:2 or 2:3 comparisons. Explicit parameter calls enforce the same level bounds. Zero arrows and the repeated easy reciprocal demand are rejected. Every changed geometry uses the same renderer; source assets are reused only for identical verified geometry. Plot specification is in `plot-extraction.md`.

Source-bank fidelity, independent printed-equation/PNG correctness, and actual engine grading are separate evidence. `source-replay.json` reports complete current banks and correct designations. `reference/current-validation/` checks both masks, every level, signed boundary cases, and checked/unchecked field-owned answer-ID submissions. No source error or unresolved bank comparison remains. Original database IDs and Math Academy IDs are evidence only and are omitted from new generated questions.
