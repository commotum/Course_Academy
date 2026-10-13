# Four extraction stages

1. Specific sources

All five originals ask for the single constant making a homogeneous linear
x-equation have infinitely many real solutions. Their first displayed equation,
last solving row, and all answer values are preserved in source.json and review.

| Source | a,b,c; parameter | Structure / number forms | Field / solution ending |
| --- | --- | --- | --- |
| q-287970 | 2,0,3; p | 2px=3x, positive integer coefficients, fractional result | 5-choice radio; p=3/2 |
| q-287971 | 1,-3,4; p | (p-3)x=4x, unit leading coefficient, negative shift | 5-choice radio; p=7 |
| q-288436 | 5,0,10; p | 5px=10x, positive integer coefficients, integer result | 5-choice radio; p=2 |
| q-288440 | -4,0,8; k | -4kx=8x, negative leading coefficient and result | 5-choice radio; k=-2 |
| q-287975 | 2,-3,5; p | (2p-3)x=5x, multiplication and negative shift | blank fragment 4; 2p=8, p=4 aligned |

2. Shared pattern

For real x and real parameter u, (au+b)x=cx is an identity exactly when au+b=c.
For a nonzero, the unique requested value is (c-b)/a. Scale and shift retain one
inverse operation; affine uses subtract then divide. Identifying the two x
coefficients and applying the identity condition remains the assessed method.
The blank supplies u= and expects a scalar, not a complete equation.

3. All components and complete source banks

Let r=(c-b)/a. Every bank listed below is selected as a unit, then instantiated
and rejected as a unit if any value is undefined/equivalent. The correct value
is derived before wrong operations. choice-mapping.json gives every original
answer UUID, exact value, designation and its generated field-owned UUID.

| Profile / source | Complete bank (correct first) | Exact observed bank |
| --- | --- | --- |
| observed_ratio / q-287970 | r; 1/r; -1/r; 1; 0 | 3/2; 2/3; -2/3; 1; 0 |
| observed_shift / q-287971 | r; c/(-b); (-b)/c; c; -b | 7; 4/3; 3/4; 4; 3 |
| observed_scale / q-288436 | r; 1; a; a/r; c | 2; 1; 5; 5/2; 10 |
| observed_signed / q-288440 | r; -r; 1/r; 0; -a | -2; 2; -1/2; 0; 4 |
| blank / q-287975 | r | 4 |

Reciprocal, wrong sign, omitted division and dividing instead of adding are
plausible mathematical mistakes. A single scalar source option cannot recover
its author's algorithm: fixed 1/0, a/r and -a are explicitly observed expression
patterns with unresolved author intent. No fitted expression is promoted into
normal generation. Complete observed profiles are available through the public
API for original and changed-parameter replay, not chosen by default. This
preserves source evidence without pretending inferred intent is verified.

Normal authored scale bank: r; 1/r (invert quotient); -r (wrong division sign);
c (omit division); ac (multiply rather than divide). Normal authored shift bank:
r; c+b (move shift with wrong sign); c/(-b) (divide by shift rather than subtract);
(-b)/c (invert that ratio); c (omit shift). Both have exactly five options and
all four explicit wrong operations, selected before parameters. No option pool,
first-valid replacement or learner-facing distractor diagnosis is emitted.

4. Reusable slots, solution stages and constraints

Fixed prompt: "Consider the equation" → displayed left/right coefficient times
x → real-constant context → given infinitely many solutions → value of parameter.
Complete slots are coefficient expressions, opposite coefficient, and parameter
name (p,k,s,q), never blind substitutions across prose. A nonzero shift makes
parentheses mandatory; signed terms are rendered with one visible sign.
Every blank has its exact matching {{field-1}} placeholder and supplied u=.

The fixed worked solution retains all original prose and four math displays:
ax=bx; a=au+b, b=c; au+b=c; the final solving block. Scale/shift keep one final
row. Moderate/hard keep the two distinct rows au=c-b, u=(c-b)/a. The same solution
is returned for every answer choice. Exact original paragraph, sentence, row
sequence and punctuation are validated at all five replays, including comma
placement inside math. There are no source-format or mathematical repairs.
All choices are delimiter-free math values, correct refs are owned lookup refs,
and choices are shuffled after recording correctness.

Normal domains (also enforced on explicit parameters):

- Easy scale: integer |a|=2..8, b=0, integer |c|=2..16; all sign combinations.
- Easy shift: a=1, integer |b|=2..8, integer |c|=2..12, nonzero result.
- Moderate: nonunit integer |a|=2..8, nonzero integer |b|=1..9, |c|=1..24;
  0<|r|<=12, reduced result denominator<=4, |c-b|<=48, and gcd(|a|,|b|,|c|)=1.
  The primitive integer triple prevents a hidden common factor from reducing
  the equation to a unit-coefficient easy shift. The observed case fits.
- Hard authored: a,b,c each noninteger reduced rationals with denominator2..5,
  numerator magnitude1..12, value magnitude<=4; b and c denominators differ;
  reduced difference denominator2..10 and numerator magnitude<=24; reduced
  result denominator2..6 and numerator magnitude1..12. This enforces the stated
  rational arithmetic workload after reduction. Variable-letter aliases and
  unreduced input fractions cannot inflate diversity.

Observed profiles add their source sign conditions (positive a,c for ratio/scale;
negative a and positive c for signed; negative b and positive c for shift). Banks
add whole-instance collision guards. Explicit parameters are rejected unchanged
on any violation. Sampling uses these exact same guards; profile selection is
never replaced after rejection. All normal finite domains are enumerated in
variant-counts.json, with mathematical task counts normalized by common nonzero
scaling (b/a,c/a). This fingerprint excludes banks, profile aliases, seed, layout,
and variable-letter aliases. Content identity separately depends on version,
actual printed prompt/solution, difficulty, domain, field layout and entire
unordered displayed bank/correct designation. Different banks change IDs;
option order, seed, profile aliases and rational parameter spelling do not.

Plots: none in any prompt, choice or solution; steps5/7 need no renderer.
No database registration or transaction is part of this package.
