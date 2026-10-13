# Four extraction stages

## 1. Specific originals

`source.json` preserves the full immutable wrapper, canonical example, UUIDs, difficulty enums, prompts, complete banks, correct refs, and every original worked-solution string. `source-cases.json` repeats the full original records with explicit endpoint parameters and profiles. Classification lists every original's mathematical structure. All sources use x=t, y=g(t), vector derivative, norm, scalar substitution, definite-integral setup, antiderivative and endpoint arithmetic, except q-76508, which has no supplied solution. Hard exponential/parabola/reciprocal add a separately narrated u-substitution block; circle cancels its radical before ordinary integration. Moderate polynomial evaluates three individual endpoint terms; constant integrates 1 with a pulled-out factor. These distinct sequences are not merged.

The source integrands y/x at zero have a removable singularity after restriction to the graph. Canonical y³/x² has the same issue. Circle speed diverges at the endpoint x=2, while the full scalar density has limit 8. Evaluation uses continuous extension/improper endpoint limits; these facts remain author metadata. This does not authorize a new improper-integration skill or a different path.

## 2. Generalized pattern

Evaluate a first-order scalar line integral along the explicit graph y=g(x): choose x=t, calculate √(1+g′(t)²), substitute the graph into the scalar integrand, integrate the resulting one-variable density over the stated x-interval. The assessed response is a scalar exact value. Every template preserves its own shared prose and structural stage sequence. Endpoint variation changes the actual integration/evaluation operation, not a decorative parameter.

## 3. Component and bank mapping

Each source profile is `observed_<template>`. Choice ordering below is capture order. V denotes the computed correct scalar integral, b the x upper bound, and n the source-template endpoint parameter. These formulas reproduce **every** original displayed scalar value; their wrong-operation intent is unresolved. They are explicit endpoint expression-pattern extensions and cannot be advertised as recovered error operations. No fitted polynomial or answer lookup table is used.

| Template / original parameter | Complete five-choice formulas | Correct position |
|---|---|---|
| exponential n=3 | V/2; 3V/2; −2√2; (n²+1)³ᐟ²/2; V | 5 |
| line_product b=1 | V; 2b³/3; 2b³√5; b³√5/3; 5b³√2/3 | independently derived 1 |
| circle b=2 | 3b²/32; b²√2; b²√2/4; b²/16; V | 5 |
| line_sum b=3 | V; √2/b; b√2; b²; √2/b² | 1 |
| line_polynomial b=1 | b√5/6; 3b√5; 13b√10; b√10/3; V | 5 |
| line_constant b=2 | b/4; V; b; 3b/4; b√2/2 | 2 |
| parabola n=5 | V; √n/3; n²/3; n√n/3; n³/3 | 1 |
| reciprocal n=2 | 12V; 16·2³ᐟ²; V; 24V; 16(1+1/n)³ᐟ² | 3 |

The record's original answer UUIDs/values are preserved in source-cases, allowing each table member to be linked to its original field. Choices are equivalent by complete scalar value, irrespective of TeX factorization. Every normal and replay bank must be pairwise inequivalent; the whole instance is rejected on collision. No pool of alternative wrong answers or individual option replacement exists.

Separate normal `authored_<template>` banks derive operations from the assessed density. Linear nonconstant families use omitted ds, squared metric factor, differentiation of the scalar integrand before integration, and reversed bounds. Constant family uses omitted ds, squared speed, inverted speed and using the intercept as the slope. Nonlinear families use omitted ds, squared metric factor, reversed limits and omitting ds combined with upper-endpoint rectangular integration. These are authored distractor operations, not source intent. Each bank includes the correct result and all four operations, with whole-bank rejection.

## 4. Reusable template and variation constraints

`templates.json` holds fixed prose and mathematical notation with **complete bound/endpoint-expression slots**. `build_evidence.py` documents how these are extracted. It replaces complete TeX components (bounds, endpoint powers, expanded endpoint arithmetic and final scalar), never individual x/y letters across arbitrary prose. `render_source` fills them from exact calculations. It is the same path at original and changed parameters; no literal-source question return branch exists. Source fixed coefficients/curves preserve workload, while endpoints vary. Power substitutions retain an unevaluated upper-endpoint power row and expanded difference row before final simplification. The authored easy and missing-solution product peer preserve three derivative rows, formal norm → squared-input norm → simplified speed, and primitive → unevaluated endpoint powers → evaluated endpoint powers → final arithmetic. Changing difficulty never silently changes a template.

Bounds are enforced for explicit calls as well as samplers. Nonlinear n is an integer 2..12: exponential upper ln(n), parabola upper 2√(n²−1), reciprocal upper n¹ᐟ⁴. Circle keeps radius 2, with positive rational b≤2 with denominator≤4; authored sampling uses reduced fractions with denominator 2,3,4 and 0<b<2. Linear b is exact rational in (0,8] with denominator≤2, authored sum b≥3; default moderate samples half-integers within these bounds. Easy requires m,c integers 1..6 and b integer 2..8. Endpoint denominator variation has the same elementary integration method. Sampling rejects a complete bank on collisions; explicit invalid parameters raise an error.

Task fingerprints contain the printed mathematical graph, scalar function and endpoints, excluding profiles/banks. Content identities hash version, actual prompt, actual solution and the complete sorted displayed bank. Seed and shuffle cannot change identity with fixed parameters and profile; actual bank changes do. Option UUIDs are field-owned. No plots are needed in steps 5 or 7.

## Preserved anomalies and minimal repairs

All raw errors remain unchanged in source.json/source-cases. All seven supplied source solutions write r′(u) while differentiating with respect to t: generated solutions normalize only that argument, retaining all rows/prose. q-148219 has an extra `)` in `1/(t−(t−4))` as printed; remove the unmatched parenthesis. q-76480 begins its setup with unrelated `3x⁵y²`; replace that one displayed integrand by the given `4y²/x³`. This is a mathematical teaching repair counted separately from notation normalization. No original banks require a mathematical repair or exclusion. Final answer notation may normalize equivalent factored radicals to expanded radicals.

q-76508 has no difficulty, correct reference or worked solution. Derivation: y′=2 gives √5 speed, x(y−1)=2x², integral 0..1 equals 2√5/3. The first source choice is correct by independent mathematics; **zero source designation matches are claimed for this question**. A supported radio correct ref and fixed worked solution are authored. Its original five values match as a whole bank. Exact supplied solution count is 0/7, notation-normalized count 7/7, with one additional presentation repair and one additional mathematical integrand repair; sequence/prose retention is measured separately from literal strings.
