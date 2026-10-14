# Four extraction stages

## 1. Source-specific descriptions

All eleven practice records have three-component vectors and request a scalar. q-20063 and q-128091 supply a and b×c as signed integer vectors, one zero coordinate in a, five numeric radio choices, and three dot-solution rows. q-275347 supplies a paired negative sqrt3 in the first coordinate, one zero, a scalar blank, explicit cdot products and a separate evaluated-components row. q-317302 supplies paired positive sqrt7 first coordinates and uses grouped juxtaposed products. q-317303 has signed paired sqrt8 first coordinates and thin component spacing. q-317304 has paired sqrt11 third coordinates, zero first coordinate, and thin spacing. All four radical blanks have four dot rows.

q-275348 supplies three integer vectors with zeros, expects a scalar blank, uses five cross-product rows and four dot rows. Its second j-minor product is commuted in the displayed distributed row; the parameterized mask preserves this exact operation ordering. q-73457, q-73458 and q-73459 supply three signed integer vectors, five scalar radio options, five cross rows and three dot rows. q-73457's final scalar is0; this is ordinary cancellation, not a geometry branch. q-20065 is unrated, missing worked solution and correct ref, and says b·c inside its outer dot expression.

## 2. Generalized assessed pattern

Easy substitutes a and the supplied cross vector into a three-component dot product. Moderate first computes b×c by its three signed components and then substitutes that vector into the same dot product. Source cross-product determinant notation is retained only for the cross-product phase: no direct determinant with rows a,b,c is introduced. One fixed worked solution is computed before option shuffling, regardless of the chosen error.

## 3. Component and complete-bank mapping

`source-cases.json` gives every original vector and family/profile. The code's SPECS table exposes identical mathematical parameters. Prompt vector tuples, each cross determinant/minor operand, each signed distributed component, collected basis vector, cross tuple, dot operand pair, component product and final scalar are complete slots, rendered by arithmetic operation masks rather than substring number replacement. Square roots remain source-spelled (including sqrt8), while mathematical identities canonicalize equivalent values.

All six historical numeric radio banks are opaque. Below, `T` is the parameterized intended triple scalar; every displayed value uses the listed residual. This is numerical empirical replay, not an inferred mistake recipe. These complete profiles, including the corrected opaque bank, are evidence-only and excluded from normal sampling.

| Profile | Source anchor T | Source bank | Complete parameterized residuals |
|---|---:|---|---|
| source:q-20063 |14|14,20,18,12,16|0,+6,+4,-2,+2|
| source:q-128091 |-5|-7,14,-12,2,-5|-2,+19,-7,+7,0|
| source:q-20065 |16 inferred|20,10,24,12,16|+4,-6,+8,-4,0|
| source:q-73457 |0|16,3,-21,-9,0|+16,+3,-21,-9,0|
| source:q-73458 |-11|-14,32,-11,-15,28|-3,+43,0,-4,+39|
| source:q-73459 |7|9,8,7,5,6|+2,+1,0,-2,-1|

The five blank banks each consist only of their computed scalar, with no invented feedback. All 35 original answer values replay exactly. Twenty observed wrong choices and ten present correct designations match; q-20065's five bank values match without claiming a missing original designation was observed. Its inferred four wrong choices are counted separately.

Normal authored dot radio profile: T; add rather than multiply every input pair; use a as both operands; use the supplied cross vector as both operands; reverse the supplied cross-vector components. Normal authored cross radio profile: T; lose the j cofactor minus; omit the second term of each cross component; omit the first dot component; omit the third dot component. Each bank is a single fixed five-operation profile and rejects the whole instance if any complete scalar values coincide. No first-valid recipe pool, unrelated perturbation, or distractor-specific solution prose is used.

## 4. Reusable masks, scope, constraints and anomalies

The masks retain source sentence wording, aligned stage count and sequence, cdot versus paired-product notation, thin spacing, source minors, and evaluated-component rows. At original inputs all eleven prompts and ten available solutions are byte exact. Under changed signed inputs every displayed operation is independently checked from printed vectors; each cross product's component factors and each dot product's factors are checked before scalar equality. Explicit and sampled inputs share workload guards.

Easy integer a-coordinates have magnitude≤5 and supplied cross coordinates≤10. Radical families have exactly one paired equal nonsquare radicand from2..15 and ordinary integer remaining coordinates, using those same ceilings. Scalar magnitude≤100. Moderate has integer coordinates magnitude≤4 and scalar magnitude≤200. Hard has the documented dense nonzero magnitude≤5 workload and scalar magnitude≤375. Source forms include signed values, zeros, familiar square-root products and cancellation. Three hundred independently checked default seeds per level establish substantial task variety without counting option order, seed, source bank/profile aliases or radical spelling as new mathematics. Default sampling covers every eligible observed family, while opaque historical banks remain evidence-only.

q-20065 raw evidence preserves the ill-typed `a·(b·c)` prompt and all missing attrs. The original MA1286 lesson screenshot `/home/jake/Developer/MA/DATA/Lessons/1286/Source/Sections/03-question-20065.png` was inspected at original1460×974 resolution and clearly shows `a·(b×c)` with the same five choices. The private `completed:q-20065` profile makes that supported single-symbol repair, authors a moderate rating and the canonical cross-then-dot solution, and supplies inferred correct16. Its opaque bank remains evidence-only. Completion is authored, not a recovered solution or observed rating. The intended cross vector(-3,-5,2) and dot scalar16 are independently derived.

The canonical example e-4347 has `0·2` in its final k-minor subtraction where the determinant's inputs call for `0·1`; the zero makes the value unchanged. It is context evidence rather than a practice template; normal cross masks use the actual printed b,c inputs and do not copy this operand typo.

Decoded captures contain ordinary single TeX command backslashes; JSON transport escaping is not a formatting defect. No math images occur. Steps5 and7 therefore require no plotting specification or renderer. No database writes or registration follow step7.
