# Four-stage extraction

## 1. Specific originals

- **q-167609:** f=x+y, r=⟨t,1+t⟩, [0,1]; derivative (1,1), speed √2; substituted field 2t+1; factor √2; primitive t²+t; endpoint sum gives 2√2. Five scalar choices: 2√2, 4, 2, √2, √2/2.
- **q-76434:** f=1/(y-x), r=⟨t,t-4⟩, [0,4]; same derivative and speed; denominator is -4; factor -√2/4 and primitive t; result -√2. Complete bank: 2√2, -√2, -√2/2, √2/4, √2/2.
- **q-167621:** f=2x²-16, radius4 circle, [0,π/4]; derivative (-4sin t,4cos t), speed4; 16(2cos²t-1)=16cos2t; coefficient64; primitive (1/2)sin2t; endpoint sinπ/2-sin0; result32. Complete bank: 22√2,16,64,32,16√2.
- **q-76433:** f=y², radius2 circle, [0,π/4]; speed2; f(r)=4sin²t; coefficient8; half-angle (1-cos2t)/2, factor4; primitive t-sin2t/2; resultπ-2. Complete bank: 2π-1,π-2,(2π-1)/4,(π+2)/4,(π+1)/4.
- **q-76447:** f=x³-2y³, r=(4t²,3t²), [0,1]; derivative(8t,6t); speed√(100t²)=10|t|=10t; field64t⁶-54t⁶=10t⁶; integrand100t⁷; primitive100t⁸/8; result12.5. Complete bank: 12.5,7.5,8,10,15.
- **q-40258:** f=3x, r=⟨4t^(3/2)/3,t²/2-t⟩, [0,1]; derivative(2√t,t-1); squared speed4t+(t-1)²=(t+1)²; speed t+1; field4t^(3/2); primitive8t^(7/2)/7+8t^(5/2)/5; unique answer96/35. Complete bank: 96/35,24/5,104/35,62/7,54/7. No original difficulty, correct key, or solution.
- **q-41160:** f=x²+y², r=3(cos t+t sin t,sin t-t cos t), [0,2π]; derivative3t(cos t,sin t), speed3t; field9(1+t²); primitive27t²/2+27t⁴/4; unique answer54π²(1+2π²). Complete bank: 54(1+π⁴),54π²(1+2π²),27(1+2π²),18π²(1+2π²),54(1+π²). No original difficulty, correct key, or solution.

## 2. Shared pattern

Evaluate ∫C f ds on the supplied parameterization using f(r(t))‖r′(t)‖. Preserve formal definition, coordinate derivative operators, derivative vector, squared-speed expansion and reduction, coordinate substitution, family-specific algebra/trig identity, integral setup, factorization/expansion, primitive, each component at both endpoints, and final arithmetic. One fixed solution accompanies the entire bank. All observed responses are complete scalars in a single radio field keyed selection.

## 3. Components and complete banks

`bank-map.json` records every original option, exact symbolic value, original correct/absence, field ownership/profile, and the parameterized expression pattern c times the whole observed scalar. All seven banks are exposed as `raw_<family>` through the normal public API. This homogeneous scalar-field scaling is mathematical parameterization: the printed entire original f is scaled by c and every scalar calculation/option scales by c. It is not evidence that historical wrong answers came from a recovered error operation. Their intent remains opaque; raw and completed historical banks are ineligible for learning. No source choice is silently dropped or replaced. At c=1 the original prompt, full worked solution, bank spellings, source rating/absence, and key presence/absence replay exactly; under c changes all scalar stages scale, while derivative/speed and shared formula stay fixed.

Normal banks are separately authored complete profiles chosen before sampling. Every member comes from the actual method:

| Family | Four incorrect operations |
|---|---|
| sum | omit speed; integrate field×speed²; omit y offset; omit x coordinate |
| reciprocal | omit speed; field×speed²; reverse y-x; multiply by offset instead of reciprocal |
| circle_cos | omit speed; field×speed²; omit inner chain factor of sin2t; omit field constant subtraction |
| circle_sin | omit speed; field×speed²; reverse half-angle sign; omit inner chain factor in the sine primitive |
| cubic | omit speed; field×speed²; omit y coefficient k; add y term rather than subtract |
| fractional | omit speed; field×speed²; omit constant term of speed s(t+1); divide primitive terms by old powers instead of successor powers |
| mixed_fractional | omit speed; field×speed²; omit y field term; omit x field term |
| involute | omit speed; field×speed²; omit d; omit t² term of radius² |

The actual speed-squared integral is calculated, including nonconstant speed. No final-answer perturbation pool is used. A collision rejects the entire instance: for example radius1 duplicates omitted speed with correct; radius2 in the cosine bank duplicates omitted inner chain factor with speed-squared, and k=1 duplicates omission of k with correct. Explicit calls reject such inputs instead of changing profiles or resampling parameters. The sampler keeps its family/profile fixed while resampling whole instances.

## 4. Reusable templates, constraints, and fidelity repairs

Raw scalar scaling c∈{-3,-2,-1,1,2,3} preserves complete source objects and attribute presence. Raw solutions keep captured math errors as evidence. It is not a lookup-return branch: complete integrand masks, scalar substitution/integral stages, and every option are rendered from c. Scalar source banks may be opaque even when every value reproduces.

Normal domains are public, bounded, and shared by explicit calls and samplers: easy slope a∈±1..±4, nonzero offset b∈±1..±6, c∈±1..±3, lower∈{-2,-1,0,1}, positive interval length∈{1,2,3,4}; circles radius1..6, c∈±1..±3, orientation±1 and five familiar-angle intervals; cubic signed (4,3)/(3,4), c∈±1..±3, k1..3, [0,1]; fractional scale1..5, c∈±1..±3 and four small nonnegative integer intervals; hard mixed adds nonzero d∈±1..±3; hard involute A1..5, c,d∈±1..±3 and five familiar integer/π intervals, excluding cA²+d=0. Circle angles are multiples of π/4 with no novel trig evaluations. The affine denominator is the nonzero offset everywhere. Fractional curves require t≥0; cubic/involute allow isolated stationary endpoints with positive speed in the interval. Normal exact outputs use numbers/fractions/radicals/π, with no new decimal rounding demand.

Known source errors, kept in raw public replay and corrected in normal solutions:

1. q-167609 and q-76434 derivative-vector row is labeled r(t), though it contains coordinate derivatives; normal labels r′(t).
2. q-76434 prints 1/[t-(4-t)]=-1/4. The left expression is 1/(2t-4), not the constant from the printed curve. Correct substitution is 1/[(t-4)-t]=-1/4; the source final answer is correct.
3. q-76447 final integral LHS omits coefficient2 on y³. Its endpoint row uses plus for lower endpoint; zero hides that error at original parameters. Its prose says t>0 despite including0. Normal retains the printed field coefficient, subtracts each lower endpoint component and states t≥0.
4. q-40258 and q-41160 missing keys are independently inferred above; authored completion solutions/levels are separate, and raw omission fidelity is retained. No missing designation is counted as a matched source designation.

Normal solutions add explicit substitution/evaluation of every primitive component at both endpoints. They retain each rated family's source operative identity and factor/primitive masks; source spacing and CAS notation are normalized in normal output, not claimed as verbatim fidelity. Endpoint rows are constructed before simplification and validated componentwise. `validate.py` includes an equal-math, same-row-count half-angle-removal mutation that must fail structural validation.

Mathematical fingerprint records actual curve/traversal, field, integrand and bounds, independent of seed, option order, bank profiles and raw parameter spelling. Parameterization is assessed, so orientation is meaningful here even where square-valued fields yield equal scalar integrals. Content identity separately includes actual prompt, fixed solution, complete displayed bank, field layout and actual rating/absence. Finite counts are in `variety.json`; no unlimited variety is claimed.
