# Template extraction

## 1. Specific source descriptions

The classification table identifies every original template and field layout. Full source strings, complete owned banks and omissions are retained in `source.json`; generated source comparisons are in `source-replay.json`, and source replay inputs are in `source-cases.json`. The five full solutions share the formal `ax+b=cx+d` equation, the `a=c` and `b=d` condition, the stated equation, coefficient equality, isolated first parameter, constant equality, optional second-parameter isolation, and final parameter sum. q-288623 and q-288627 omit the redundant second isolation. Inline q-287978 and q-287985 supply no solution or difficulty.

## 2. Generalized mathematical pattern

For `(a u+b)x+(d v+e)=c x+f`, independently match `a u+b=c` and `d v+e=f`. Solve `u=(c-b)/a`, `v=(f-e)/d`, then return `u+v`. Parameter multipliers are nonzero; all objects are exact rationals and x and the parameters are real. No unknown appears in both matches.

## 3. Complete component and bank maps

Write U=(c-b)/a, V=(f-e)/d, T=U+V. In the table, displayed source values align one-to-one with the parameterized expressions in the listed order. Choice order itself is shuffled and not an identity input.

| Explicit evidence profile | Parameters [a,b,c,d,e,f] | Source bank | Parameterized complete bank |
|---|---|---|---|
| raw:q-287978 | [1,-3,4,1,0,1] | 7,3,9,8,4 | U,-b,U+2V,T,c |
| raw:q-287985 | [1,-5,2,2,0,6] | absent | absent |
| raw:q-288583 | [2,0,6,-1,1,4] | 0 | T |
| raw:q-288584 | [-1,3,1,2,0,6] | 5 | T |
| raw:q-288622 | [1,2,7,5,0,15] | 15,8,5,6,7 | f,T,U,2V,c |
| raw:q-288623 | [2,0,9,1,0,6] | 18,9/2,17/2,24,21/2 | ac,U,U+f-a,fa²,T |
| raw:q-288627 | [1/2,0,4,1,0,20] | 24,28,14,20,30 | c+f,T,T/2,f,3f/2 |

Every expression numerically reproduces its displayed value. Wrong-operation **intent is underdetermined**, particularly q-288623's `U+f-a` and `fa²`, and q-288627's `T/2` and `3f/2`. These are transparent source-compatible numeric patterns, not recovered learner mistake claims. All `raw:` profiles are explicitly requested, marked `eligible_for_normal_practice=false`, and never default sampled. Changed-parameter raw-bank previews remain evidence-only. The raw API preserves missing solutions, difficulties, choices and correct references. No captured payload is returned as a literal question branch or answer lookup table.

Normal radio profiles use whole authored method banks:

- `method-sum`: T, U, V, c+f, U−V. Errors omit one parameter match, add supplied targets without matching, or subtract instead of adding.
- `method-components` (hard only, both nonzero offsets): T, c/a+V, U+f/d, a(c−b)+V, U+d(f−e). Errors omit the coefficient offset, omit the constant offset, or multiply instead of divide at either match.
- `blank`: T only.

Select the complete profile before sampling. Compute T and every specified wrong operation. If any values collide, reject the **whole instance**, including explicit inputs; no pooled distractors or replacements. The worked solution does not depend on the chosen error/profile.

## 4. Reusable masks, constraints and identity

`components` constructs complete coefficient/constant slots, conditionally parenthesizing shifted factors and negative terms. The `render` routine replaces the whole equation slot and whole displayed solution blocks, preserving all fixed sentences, mathematical stage ordering and row omissions. Shared solution sentences are reused for missing originals and hard authorship. Normal field overrides are explicit presentation extensions; radio and blank are the only supported source response types.

Easy bounds: 0<c≤12, 0<f≤60, 0<U≤15, 0<V≤24; offset magnitude 1..8 and scale 1..6. Shift templates retain a=1 and integral roots; the fractional-scale template retains nonintegral U; divided coefficients have reduced numerator 1 and denominator 2..4. Moderate bounds: integral parameters, offsets ≤8, targets magnitude ≤72, integral U in 1..12 and |V| in 1..12; either a positive nonunit coefficient and negative constant parameter, or a negative-unit shifted coefficient and positive scaled constant. Hard bounds: integer primitive triples, nonunit multipliers of magnitude 2..6, nonzero offsets of magnitude 1..8, nonzero targets of magnitude 1..24, roots of nonzero magnitude ≤12, at least one nonintegral root. All normal profiles and field overrides use the identical level guard on explicit inputs and samples.

Raw evidence uses broader explicit bounded rational objects (coefficient magnitude ≤120, denominators ≤8, roots magnitude ≤30) and never contributes normal novelty or scope claims. The samplers are finite; batch generation deduplicates mathematical tasks and reports exhaustion rather than inventing unlimited capacity. Validation's distinct counts are witnessed sample counts, not an exhaustive catalog.

The mathematical fingerprint includes the full pair of normalized equalities `(b/a,c/a,e/d,f/d)`, retaining offset and target arithmetic, not just final roots. Variable-letter aliases, bank, layout, seed and profile are excluded. Common nonzero equation scaling is canonicalized. Content identity includes version, actual prompt, actual fixed solution, field keys/types, the complete sorted bank and correct designation; missing attributes remain explicit in that identity. Seed and option permutation never change IDs. Profiles with genuinely different displayed banks produce different content identities.
