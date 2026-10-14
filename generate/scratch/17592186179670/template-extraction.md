# Four extraction stages

## 1. Specific originals

- q-39954: 2xy, (1,2)->(2,1), opposite displacement signs; full product (-2t²+2t+4), speed sqrt(2), value 13sqrt(2)/3. Five-option bank; key/solution/rating absent.
- q-76565: 2x-3y, (1,0)->(-1,0); y=0, speed2, pulled 2-4t, primitive2t-2t², value0. Five-option bank; key/solution/rating absent. The unused -3y is retained for fidelity and excluded from meaningful-task identity.
- q-123363: x+sqrt(2y), vertical (2,0)->(2,2); x=2,y=2t, speed2, pull2+2sqrt(t); factor4 integral(1+sqrt(t)); primitive t+2t^(3/2)/3; endpoint4(1+2/3)-0; value20/3.
- q-123366: e^(3x+y), origin->(-1,4); origin-specific five-row parameterization, x=-t,y=4t, speed sqrt(17); e^[3(-t)+4t] -> e^t; reverse chain primitive e^t; sqrt(17)(e-1).
- q-76564: xy, (1,2)->(4,7); x=1+3t,y=2+5t, speed sqrt(34); product ->15t²+11t+2; primitive5t³+(11/2)t²+2t; endpoint5+11/2+2;25sqrt(34)/2.
- q-76605: sec²(pi(y-x)/8), (1,1)->(2,4); x=1+t,y=1+3t, sqrt(10); innerpi[((1+3t)-(1+t))]/8 ->pi t/4; u substitution, du=(pi/4)dt; limits0,pi/4; tangent evaluation1-0;4sqrt(10)/pi.
- q-76650: (4x+2)e^(xy), (0,1)->(2,3); x=2t,y=1+2t,2sqrt2; (4(2t)+2)e^[2t(1+2t)] ->(8t+2)e^(2t+4t²); u=2t+4t²,du=(2+8t)dt; limits0,6; exponent endpoints e^6-e^0;2sqrt2(e^6-1). Raw LHS missing-factor anomaly documented separately.

## 2. Generalized backbone

All tasks evaluate a scalar arc-length integral along one nonzero Cartesian segment. The same instance controls r=a+t(b-a), 0<=t<=1, x=a_x+dx*t, y=a_y+dy*t, speed sqrt(dx²+dy²), full f(r(t)) including every implicit xy product, primitive, both signed endpoints and final scalar. One fixed worked solution is independent of selected error. Stable prose is the source formula/endpoint-vector/parameterization/derivative-norm/substitution/evaluation sequence. Distinct families preserve their operative expansion, common factor, origin simplification or substitution stages.

Raw evidence uses a source prose/operand mask with explicit mathematical formulas and original notation hints per operand. It is not an original-question return branch. `build_templates.py` extracts operand masks; `source-templates.json` is the public recipe data. Changing parameters computes every masked operand. The original raw Euler-e spellings remain intact. Raw evidence is ineligible for learner sampling because original omission/anomaly/opaque distractor intent must not be advertised as recovered correctness. Normal authored method banks use visible multiplication in scalar values.

## 3. Components and complete banks

The complete empirical mapping is `bank-mapping.json`: every original option, exact source spelling, derived original value, formula and interpretation limit. All 35 choices participate; no subset mixing, fitted-bank substitution or omitted source. Unrated-source correct answers are inferred by the displayed mathematics and cannot count as matched source designations.

Source scalar distractors generally underdetermine their original authoring operations. Their parameterized algebraic forms are empirical evidence only, with explicitly fitted offsets/scales where needed. No learner-facing diagnoses are invented. Separately authored default complete banks specify method mistakes in `generation.recipes`; a collision of any two wrong choices, or wrong/correct equality, rejects the entire instance. Correct answer is derived before the selected five-option bank. Eligibility is whole-bank; individual options are never replaced by first-valid pool members.

## 4. Reusable slots, bounds and ordered stages

All explicit input calls enforce the same bounds as sampling. Integer endpoint/displacement/coefficient slots only; t bounds fixed0,1; nonzero segment mandatory. Fields remain radio/selection/five scalar values; no feedback introduced.

- Authored easy linear: a,b in[-3,3], dx,dy in{-3,-2,2,3}, c,d in{-3,-2,1,2,3}. Pulled slope c*dx+d*dy is nonzero. Both input components vary; one linear polynomial primitive, fixed number of integration stages. Full bank: correct, omit speed, left rectangle, right rectangle, integrate only half the segment.
- Inferred easy odd linear: a in1..4, x endpoint a->-a, y=0, c in1..4, d fixed-3. Correct remains0 by cancellation. Whole method bank rejects a=1 because absolute integral and absolute endpoint collide. Raw source bank still includes a=1,c=2; unused d changes are forbidden.
- Moderate product: a,b in1..3; dx in{-2,-1,1,2,3}; dy in{-2,-1,1,2,3,4,5}; c in1..3; endpoints nonnegative. Preserve product then quadratic expansion, termwise cubic/quadratic/linear primitive and uncollected endpoint sum. Full bank: correct, omit speed, omit cross term, omit quadratic term, divide quadratic primitive by2 instead of3. Complete bank collisions reject canceled cross components.
- Moderate radical: a in1..4,b=dx=0; (k,dy) in{(1,1),(1,4),(2,2),(2,8),(3,3),(4,1),(4,4)}. k*dy perfect square; radicand nonnegative over the whole path. Source common factor a*speed is explicit before primitive of1+(sqrt(kdy)/a)sqrt(t). Full bank: correct, omit speed, endpoint rectangle, integrate sqrt(t) as t, invert power-rule multiplier. dy=1 fails whole bank because omitted speed coincides.
- Moderate exponential: origin start a=b=0; dx in±1,±2,±3; dy in±2,±3,±4; c in±1..3,d in±1..2; 1<=abs(cdx+ddy)<=4. Real exponent, nonzero slope. Preserve origin-specific parameterization, uncollected substituted exponent, collected exponent, constant speed factor, reverse-chain primitive. Full bank: correct, omit speed, omit lower endpoint, double upper parameter, add lower endpoint. Source k=1 remains valid.
- Hard secant: a=b in[-3,3], dx in{-2,-1,1,2,3}, dy in{-3,-2,-1,1,2,3,4,5}, 1<=abs(dy-dx)<=4, n=abs(dy-dx)*den with den in{3,4,6}. u starts0 and ends±pi/3,±pi/4,±pi/6; no pole anywhere along the segment. Same substitution/tangent endpoint workload, familiar exact values. Bank preserves missing/inverted chain/speed factors. Translations and sec² argument sign aliases do not inflate capacity.
- Hard matched exponential: a in{-1,0,1}, b in1..3, dx,dy in1..3; 1<=dx*b+dy*a<=10, endpoint (a+dx)(b+dy)<=18. Integrand factor m*x+n has declared m=2dy,n=dx*b-dy*a, so after substitution it equals q'(t) where q=(a+dx*t)(b+dy*t). q has genuine quadratic term; substitution is monotone and real. Source factor/inner expansion, u/du, limits, primitive and two exponent endpoints retained. Full bank: correct, omit speed, add lower endpoint, increment lower exponent, use x displacement as speed.

`capacity.json` exhausts declared finite domains using exact rational/radical tuples and algebraic transcendence arguments. Meaningful identity includes weighted pulled integrand, speed and primitive workload, excluding seed, option order, raw-profile aliases, unused coordinates/coefficients and translations that cancel. Content identity separately includes version, actual difficulty, complete displayed prompt/solution/bank. Normal default routing samples every supported source family, including unrated odd-linear cancellation, plus authored easy; variants within a level are equal-workload alternatives, not a progression.
