# Four extraction stages

## 1. Specific source descriptions

q-122271: y²=8x; 24x/y; (0,0) to (9/8,3). Solves for x, chooses y=t, computes derivative t/4 and speed √(t²+16)/4, substitutes scalar 3t, uses u=t²+16, bounds 16 and25. Primitive operations 3/8·(2/3), individually evaluated 125 and64, then61/4. Five rational quarters with numerators53,47,67,51,61.

q-122579: x=√y;4xy; (0,0) to(√2,2), increasing-y arrows. Radio rationals144/5,121/15,125/3,213/5,149/15. No level, designation or solution. Independent substitution: integrand2t√(4t+1); u=4t+1; primitive u^(5/2)/20-u^(3/2)/12; evaluate at9 and1 to149/15. Raw bad integral notation is retained only as evidence; normal renders canonical integral notation and uses regular positive lower y.

q-122574: x=y²;12x/y; (1,1) to(6,√6). Derivative2t; speed√(4t²+1); scalar12t; u=4t²+1; bounds5 and25. Primitive stages12·1/8,3/2·2/3, √25³-√5³,125-5√5,5(25-√5). All five supplied options retain their complete scalar values.

q-122593: x=2/y;xy⁶; (2,1) to(1,2). Derivative-2/t²; speed√(t⁴+4)/t²; scalar2t⁵; u=t⁴+4; bounds5,20. Primitive operations2·1/4,1/2·2/3, cube roots evaluated separately40√5 and5√5, then35√5/3. The other four displayed values do not reveal defensible error operations.

q-149727: x=2y-4;1/(y-x); (0,2) to(2,3). Derivative2; speed√5; scalar1/(4-t); u=4-t gives reversed2→1 bounds. Source explicitly moves the negative sign into reversed bounds before the ln primitive, then ln2-ln1,ln2-0,√5ln2. The complete five-option bank is preserved.

q-149745: x=e^(y/2);6x⁶e^-2y; (1,0) to(√2,ln2). Derivative e^(t/2)/2; speed√(e^t+4)/2; scalar6e^t; u=e^t+4;5→6. Primitive3·2/3; endpoint powers6^(3/2),5^(3/2); individual6√6 and5√5; expanded12√6-10√5. All five options are whole differences, not compared by separate terms.

## 2. Generalized description

Represent r(t)=⟨x(t),t⟩ using y endpoint bounds; differentiate both coordinates; compute √((dx/dt)²+1); compose f with the curve; multiply scalar and arc-length factor; evaluate the resulting definite integral with a power primitive or one elementary u-substitution. Response is the exact final scalar in one five-choice radio. The single worked solution is independent of selected choice.

## 3. Component/bank mapping

Every original source/field/choice identity and value remains in `source.json`; `bank-map.json` explicitly associates every owned answer ID and field ID with its parameter recipe and verified exact value; `source-cases.json` associates each with its public parameter/profile recipe. The renderer preserves every source sentence and every present source row, using complete coordinate/bounds/primitive-expression slots. Fixed curve/integrand coefficients in opaque raw profiles remain fixed; endpoints vary. Choice values are independently read back and compared one-to-one with SymPy. Changed endpoints exercise all six profiles.

Let U and V denote the upper/lower substitution values, A=U^(3/2), B=V^(3/2). Raw opaque profiles are explicitly **evidence-only**, including their extrapolations. Their numerical reproduction does not recover the author's intended errors.

| Profile | Complete ordered value recipes (order subsequently shuffled) | Interpretation limit |
|---|---|---|
| source:q-122271 | (A-B-8)/4,(A-B-14)/4,(A-B+6)/4,(A-B-10)/4,(A-B)/4 | observed numerator offsets; opaque, not misconceptions |
| source:q-122574 | U-√V,b²-√V,(V+1)²-√(V+1),(V+1)((V+1)²-√(V+1)), exact integral | source scalar motifs; wrong operations unresolved |
| source:q-122593 | (U+1)√(k+1)/V,(U-8)√V/(V+2),(U+3V)/(U-8),(V+k)²/(3V), exact integral | fixed visible numeric motifs; opaque constants unresolved |
| source:q-149727 | √2ln5,(a+b-1)√2, exact integral,2√5,2ln2 | speed/log patterns visible; fixed wrong endpoint motifs opaque |
| source:q-149745 | V√U-U√V,√U-√V,exact integral,U√(U/2)-2√V,2√U-V√V | endpoint power motifs; no claimed intended misconception |
| source:q-122579 | 144/5,121/15,125/3,213/5,149/15 multiplied by the current integral divided by149/15 | proportional replay only, scalar bank underdetermined and never eligible |

The q-122579 proportional profile is an explicitly limited parameterized evidence extrapolation, not a source sampler or a promoted error recipe. Its original record remains ungraded. No mathematical repairs to present source designations are needed.

Method-derived default banks are separate. For power/substitution families, the five complete operations are: correct primitive endpoint difference; integrate f(r(t)) omitting speed; add primitive endpoint values; omit the lower primitive value; integrate u rather than √u while keeping the substitution Jacobian. The square-root family applies the wrong-power operation to both distributed components. Straight-line easy substitutes a cubic primitive for its linear integrand. The logarithmic-line bank instead uses: correct; omit speed; integrate with speed squared; omit the lower logarithm; treat the reciprocal primitive as linear. Every value comes from the actual displayed method. Whole instances are rejected for any collision or invalid/nonpositive choice; no first-valid option replacement occurs.

## 4. Reusable template and domains

All raw prompt math, fixed prose and stage sequences remain captured masks. Complete components are replaced simultaneously by longest-mask matching to prevent replacing numbers inside unrelated factors, function labels or already-inserted expressions. Changing endpoints updates the coordinate tuples, parameter domain in prose, every integral limit, primitive substitution and individually evaluated endpoint values. Missing source fields are not filled in raw replay.

Normal completed records use the same common source sentences with an explicit formal derivative/component block, actual coordinate-substitution stage, formal line-integral operator, substituted product, collected integrand, substitution/Jacobian operation, primitive power operations, and separate substituted/evaluated endpoint components. The square-root family expands both u powers. Logs render as ln. All answers are delimiter-free math strings; normal prompts use full integral notation.

Normal positive integer c is 1…12. Easy: integer bounds1…6 and k1…3 (offset incidental to assessed cy task). Moderate parabola: k1,a1,b²∈{2,6,12,20}, giving upper u∈{9,25,49,81}; reciprocal k1…3,a1,b2 or3; logarithmic line k4…8,a1,integer2≤b≤k-2; canonical log-curve k1,a1,b²∈{3,8,15,24}, giving square upper u. Hard implicit parabola k∈{4,6,8}, positive radical y endpoints chosen so lower/upper u are perfect squares L²,U² with k/2<L<U≤8; exponential k2,a0,b=ln(n),n2…6; square-root k1…4,a1,b2…5. Coefficients sampled from{1,2,3,4,6,8,10,12}; all explicit calls enforce the corresponding workload/domain guards. Raw profiles hold original c and k and validate increasing finite bounds/actual curve domain separately. The direct-parabola opaque factoring profile additionally retains a=1 and upper u a square divisible by25, so its final common-factor operation remains present.

No plots assess a new demand. Mathematical fingerprints describe f, x(y), and bounds, excluding banks and profile aliases. Content identity incorporates actual difficulty, prompt, solution and the full displayed bank. Seed and option order do not affect identity. All normal families are selected before sampling and are served by default generation.
