# Source extraction and bounded hard generator

Exact source components are in source.json/source.edn; source-components.json enumerates every original choice and field without discarding incomplete records. Source statements, equations, solutions, choices and original IDs are retained unchanged there.

q-31288 asks for f'(pi/6) with f(x)=-6cot(x). The coefficient is a negative integer, the argument is x, the angle is the positive special angle pi/6, and the function is defined at that angle. The solution first factors the coefficient, uses (cot x)'=-csc^2 x, cancels two negatives, substitutes pi/6, uses csc(pi/6)=2, squares 2, and multiplies to obtain 24. It contains no graph or diagram.

The reusable calculation is f(x)=-n cot(x), f'(x)=n csc^2 x, f'(pi/6)=4n, on the real domain sin(x)!=0. Keep the angle, variable, derivative target, all source prose and the solution sequence fixed. Only the coefficient and its dependent intermediate/final values vary. Observed n=6; proposed bounded extension n=1..24, integral and positive. No sign, angle, composition, product-rule or chain-rule extension is used. Differentiation plus special-angle evaluation preserves the source's hard task and workload.

The live hard source has no field. The retained historical import-ready record adds `Answer: {{answer}}` with one math-valued blank and canonical answer 24, derived from the worked calculation, not a learner response. The generator replays that locally reviewed response adaptation and explicitly records that it cannot recover the original bank. It invents no distractors. This is an authored response completion, not a claim of original bank fidelity. Numeric blank correctness and equivalent/incorrect entries are exercised with the actual learner grader.

Source rendering repairs in generated content only: `{csc}` becomes `\csc` and duplicated nested `aligned` environments become one. The source records stay unchanged. Source sentences and equation steps remain in order. The fixed worked solution does not depend on the learner's response.

## Other source families and choice profiles (deferred)

These formulas describe every observed choice, in source order. They are extraction evidence, not supported sampler implementations. No mixed profiles are used.

- q-105309: input a^x-cot(x), observed a=5. Bank: a^x-csc^2 x; a^x ln(a)-csc x; a^x ln(a)+csc x; a^x ln(a)+csc^2 x (correct); a^x ln(a)-csc^2 x. Solution differentiates each term separately. Radio has five math choices.
- q-1913: input -a x^p cot(x), observed a=2,p=4. Bank: x^p csc^2 x+ap x^(p-1)cot(x); a x^p cot^2 x-ap x^(p-1)csc(x); a x^p csc^2 x-ap x^(p-1)cot(x) (correct); a x^2 csc(x)-ap x^(p-1)cot(x); a x^p csc^2 x+ap x^(p-1)tan(x). The fourth option's exponent 2 is observed; its general mistake is unresolved. Do not infer a p/2 recipe from one source. Product rule, then simplification. Radio has five math choices.
- q-17639: input a tan(x)-b x^p-c cot(x), observed a=23,b=5,p=5,c=1. Bank: c sec^2 x-bp x^(p-1)+a csc^2 x; bp sec^2 x-a x^(p-1)+c csc^2 x; c sec^2 x-bp x^(p-1)+c sec^2 x; a sec^2 x-bp x^(p-1)+c csc^2 x; c sec^2 x-a x^(p-1)+c csc^2 x. Fourth is mathematically correct, but stored correct reference and worked solution are absent. No difficulty inferred.
- q-31279: input a x-cot(x), observed a=2. Bank: csc^2 x; a-csc^2 x; -a-csc x; a+csc x; a+csc^2 x. Fifth is mathematically correct; stored correct reference and solution are absent. No difficulty inferred.
- q-340595: e^x-3cot(x), full derivative blank e^x+3csc^2(x); separate-term derivative solution. No choices to synthesize.
- q-340597: ln(x)cot(x), x>0 and sin(x)!=0. Blank is cot(x)/x, followed by fixed -ln(x)csc^2(x). Product-rule solution. Preserve this fragment shape.
- q-340598: x cot(x), sin(x)!=0. Blank is x csc^2(x), subtracted from fixed cot(x). Product-rule solution.
- q-340599: ln(x)/cot(x), x>0, sin(x)!=0, cos(x)!=0. Blank is x ln(x), the multiplier of csc^2 in the numerator. Table fraction with numerator cot(x)+csc^2(x) times the blank and denominator x cot^2(x). Quotient rule, nested fraction simplification, then common denominator.
- q-340603: x/cot(x), sin(x)!=0 and cos(x)!=0. Blank is x csc^2(x), added to cot(x) above cot^2(x). Quotient rule then simplification.
- q-31355: cot(x)/x^2, x!=0 and sin(x)!=0; quotient-rule solution (-x csc^2 x-2cot(x))/x^3. Response layout absent; do not invent a radio bank.

Full source bank fidelity is not claimed for deferred families. Their exact banks are retained, including unresolved fourth-option generalization for q-1913 and missing key/solution evidence for unrated questions. New source evidence can extend this version after independent extraction and validation.
