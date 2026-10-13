# Template extraction

## 1. Specific originals

`source.json` retains every original attribute and the basis wrapper. `review.md` prints every original prompt, five-answer bank, designation and full worked solution beside an observed-profile replay and changed-coefficient examples. `bank-mapping.json` maps **every** answer UUID/value, with correct flag and computed expression recipe; no choice is dropped. `source-cases.json` gives all 12 original parameters and bank profiles.

All vector components are exact, with real x,y,z; no units or precision instructions occur. Bounds are rectangles or one-variable triangles. q-161541 requires strictly positive x,y for derivative simplifications. q-161539's domain has |xy|≤1<π/2, so tangent is nonsingular. Exponential surfaces are positive, making reciprocal components defined. Flux can be negative; negative choices are valid signed-flux values.

Specific expressions and bounds are the `BASE` dictionary. `source-stage-audit.py` reads and independently checks every original numeric final integration row, in addition to the generated-stage checks. `STAGES` preserves the source final row sequence and repeated/omitted simplification stages. q-160888/q-161447 include an extra simplified integrand row. q-161536 has only eight final rows and no explicit outer-bound arithmetic row; q-161541 factors its outer integral and also omits that row. Other families retain their corresponding ten- or nine-row sequences.

Two source errors:

* q-161481 has −π≤x≤0 and −x≤y≤0. The geometric set has no interior. Its five options and marked π−π³/6 agree with the **formal integral with reversed y limits**. The observed-profile replay is quarantined and clearly marked outside learner metadata; default presentation swaps y bounds, recomputing flux −π+π³/6 at original coefficients. It does not introduce a new triangle or retain the invalid geometric claim as normal output.
* q-161552's first substitution vector uses `2xz`, contradicting the prompt's `2x(y+z)`. The next substitution row and all later stages/final result use the prompt correctly. Regeneration repairs only that mathematical error; raw source remains available. The corrected substitution does not count as an exact original mathematical stage match.

## 2. Shared pattern

Differentiate z=g(x,y), substitute z into all three field components, compute F·(−g_x,−g_y,1), then evaluate the double integral with stated bounds. Answer is an exact scalar flux. This is evaluation of Cartesian graph flux, not scalar surface area, integrand-only setup, general parametric flux, divergence theorem or Stokes' theorem.

## 3. Components and complete banks

For each observed family, fixed parts are expression structure, graph and bound shape, source prose and stage sequence. Variable parts are the independent field weights p,q,r. The normal banks use complete operations on A=∬(−Pg_x), B=∬(−Qg_y), C=∬R: correct A+B+C, reverse orientation, flip one signed normal contribution, omit a component. For the zero y-normal families, the eligible complete bank instead uses correct, opposite, R-only, P-only and Q-only (the last two omit the normal factor). For q-161553, the vertical contribution integrates to zero on the unit square, so its eligible complete bank instead uses correct, opposite, omit-P, R-only, and P-only; weights with duplicate contributions reject the whole instance. Every bank has exactly five distinct scalars and exactly one correct answer; whole-instance rejection handles collisions. No first-valid distractor pool exists.

Before marking intent unresolved, extraction tests all 64 coefficient combinations from {−1,0,1,2}³ on A,B,C against every source option; matching candidate sequences appear in `bank-mapping.json`. Scalar coincidences remain ambiguous. Unmatched options stay as explicit observed symbolic shapes, not guessed offsets or fitted polynomials. Uniformly scaled observed profiles multiply each complete expression by the same field weight; this is a faithful value-shape replay policy, **not** a claim to recover author error code. These profiles require p=q=r. They are never chosen by default. Default operation banks are separately labeled authored extensions and tested independently.

## 4. Reusable template and bounds

The renderer splits each source worked solution at complete display-math blocks, preserving every prose segment and block location. Each block is regenerated from the actual symbolic field, graph and integration stages. Prompt substitution replaces complete vector/graph/domain slots; no short expression is globally replaced across prose. Standard LaTeX replaces source Unicode operators, underbrace notation and inconsistent differential typography. Equation labels and factor placement are normalized while preserving mathematical stages and row counts. There is one worked solution regardless of selected option.

Moderate/hard signed weights satisfy 1≤|p|,|q|,|r|≤3, including explicit API calls. The graph and domains are fixed per observed family, preserving degree, cancellation structure, singularity control, exact trig bounds, and integration workload. Independent signed weights create meaningful combinations of component flux and cancellation, not a claim to add more templates. Six possibilities per weight yield up to 216 mathematical field instances per family; collision rejection can narrow the eligible bank. This is a stated authored sampling policy, not recovered original code.

Missing easy is an authored bounded simplification anchored to the same route: g=ax+by+c, F=⟨uy,vx,z+w⟩ over [0,X]×[0,Y]. a,b,u,v are nonzero integers of |value|≤2; |c|,|w|≤2; X,Y∈{1,2}. The substituted integrand is linear, so students perform the same derivative/substitution/dot-product/two-integrations method with no mixed powers, nonlinear chain rules or variable bounds. This has equal-level variations, not a progression. The canonical and observed problems demonstrate all these prerequisites; easy reduces algebra while still assessing the full flux evaluation.

Mathematical fingerprints use the exact field, graph, domain and orientation independently of option order/profile. Content identity includes version, displayed prompt, full fixed solution and complete bank. Owned UUIDs use deterministic UUID5. All records remain local JSON review data; steps stop at 7 and no EDB writes occur.
