# Source templates and complete bank recipes

## q-95532

Observed a=4, b=−3. Real x; arbitrary integration constant C. Prompt: What is the integral of sinh(ax+b)? The source bank, in its field selection, consists of:

1. cosh(ax−b)/(−b)+C: simultaneous sign change of shift and scale 1/(−b). Observed 1/3 cosh(4x+3)+C. Interpretation of the combined mistake is unresolved; retain the expression.
2. (2/a) cosh(ax+b)+C: twice the correct scale. Observed 1/2 cosh(4x−3)+C.
3. −cosh(ax+b)/a+C: sign reversal. Observed −1/4 cosh(4x−3)+C.
4. cosh(ax+b)/a+C: independently verified correct by differentiation. Observed 1/4 cosh(4x−3)+C.
5. cosh(ax+b)+C: omitted scale. Observed cosh(4x−3)+C.

All five choices use the source's math answer type and selection radio field. No source solution exists. Authored fixed solution sequence: u=ax+b; du=a dx; substitute dx=du/a; integrate sinh u; back substitute. Preserve prompt punctuation and bank notation. Frozen domain a=3..8 and b=−5..−1 covers source signs and parameters; b=0 and positive b are unsupported by this profile. Only a and b vary, and the reciprocal scale and every argument follow them. Integral identity is based on the visible integrand and response shape, not seed or choices.

## q-95533

Observed n=3; integrand cosh((2x−1)/n), bounds 1/2 and 1. Let r=(n−1)/n. Five observed complete bank recipes:

1. r sinh(exp(n−1)+1), observed 2/3 sinh(e²+1).
2. (n/2) sinh(1/n), observed 3/2 sinh(1/3), independently verified correct.
3. r sinh(n/(n−1)), observed 2/3 sinh(3/2).
4. −r sinh(exp(n−1)−1), observed −2/3 sinh(e²−1).
5. (1/n) sinh(1/n), observed 1/3 sinh(1/3).

The mathematical objects exactly reproduce every source value. Except for option 2, these parameter dependencies are inferred expression patterns from one bank; their psychological mistake interpretations are unresolved. They are bounded authored generalizations, not claims about further observed banks. No pooled/mixed profile. n=3..10 is the frozen extension, while numerator, shift and bounds remain fixed. Neither n=1 nor n=2 is supported. All choices are proven distinct by high precision bounds and the correct option by exact integration.

Authored solution: u=(2x−1)/n; du=2 dx/n; lower bound 0, upper 1/n; integrate cosh u as sinh u; subtract endpoints. No source worked wording or rating is available, so fidelity is limited to exact source prompt and complete answer bank. These added solutions and correct refs never revise the source records.

## Plot extraction and generation

None. The prompts, bank and solutions contain only text and mathematical notation. No image asset publishing or plot generator is required.
