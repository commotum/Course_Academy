# Template extraction

## 1. Describe the originals

The source task is to calculate an indefinite integral `n/(ax+b)^m`, with integer m greater than one. Easy sources have (n,a,b,m): q-113511=(1,5,-1,6); q-113512=(1,2,3,7); q-12018=(6,2,-3,4); q-72429=(-15,5,-7,4); q-113509=(1,1,-2,3). Moderate originals are q-12019=(3,-3,1,3), q-72431=(4,-1,8,5), q-113517=(1,-5,9,3). q-12499=(1,1,-3,8) is unrated/incomplete. These original level labels are retained; a signed numerator alone does not establish a universal difficulty boundary.

Some prompts say “Calculate the integral”; others consist only of the displayed integral followed by equals. Rewriting as a negative power precedes u substitution, du/dx and dx. The main aligned solution substitutes the whole affine expression, extracts constant factors, applies the power rule, substitutes back and rewrites the reciprocal. Source profiles differ in redundant factor-extraction, coefficient collection and u-reciprocal stages, so their exact ordered rows remain distinct. The final aligned block differentiates the primitive using the chain rule and recovers the supplied integrand.

`templates.json` describes each original exactly: source parameter tuple and affine spelling; full prompt and solution masks; every answer’s full source value, source identity, full-expression mask, and correct designation. `source-cases.json` includes every practice record, including unrated and independent records. `bank-recipes.json` records each option as an exact coefficient times the affine factor to a negative integer power, plus C. Coefficients/exponents are observed patterns; misconception intent is unresolved, so these profiles only vary the full affine intercept. All four distractors are mapped per complete original, with no pooled bank selection.

## 2. Shared mathematical pattern

Choose u=ax+b, convert dx=du/a, then integrate u^(-m) with the power rule. The primitive is n/[a(1-m)] times (ax+b)^(1-m), plus C, on each connected interval excluding x=-b/a. Learners select one complete primitive from five field-owned radio choices. No logarithm case, nonlinear substitution, sum of integrals, bounds, initial condition or new operator is introduced.

## 3. Components and complete banks

Original profiles retain their original n,a,m and intercept sign. The variable full factor `@@L@@` replaces the complete affine component in prompt, each choice, u definition, integration rows, chain-rule operands and derivative check. It never replaces isolated digits throughout arbitrary prose. The masks are served by the normal public generator at original and changed parameters; they are not copied raw question records returned as source replay.

The normal authored bank consists of five complete recipes, in recipe order before independent shuffling: correct primitive; negative of correct primitive; omit the division by a; use m+1 in place of m-1 with corresponding negative denominator; multiply by a instead of dividing by a. The last yields a² times the correct primitive. Each whole bank must have five distinct derivatives, so equivalence modulo C is rejected. These are explicitly authored bank profiles, not recovered original misconception diagnoses.

q-12499 raw values and duplicate pairs are recorded in `source-errors.json` and `legacy-raw-reference.json`. Its correct missing designation is derived from differentiation, not claimed recovered. Normal repair retains the original correct primitive, its sign reversal and the original last wrong exponent choice. The two ambiguous copies become omission of the power-rule divisor and the opposite sign of the wrong-exponent primitive. All five then differ modulo constants. No source record is modified.

## 4. Stable backbone and slots

Observed profiles: n,a,m, field layout, five-option complete bank, shared prose and ordered solution rows fixed; b varies over integers 1..12 or -12..-1 retaining the observed sign. This is intentionally narrow because the complete distractor formulas do not establish how all numeric constants should vary. Source anchors are retained exactly, apart from documented differential insertion and canonical presentation normalization.

Authored defaults use the same backbone at all levels. All have b in {-12,..,-1,1,..,12}, m in {3,..,7}. Easy has n in {1,2,3}, a in {2,3,4,5}. Moderate has n in {1,2,3,4}, a in {-2,-3,-4,-5}; a negative slope requires the sign in dx. Hard has n in {-2,-3,-4,-5}, a in {-2,-3,-4,-5,-6,-7}, gcd(n,a)=1, preserving a nontrivial rational signed scaling. Every allowed value within one level has the same six integration rows and five derivative-check rows; changing values does not create a within-level progression. Explicit inputs obey the same bounds.

These are conservative equal-method definitions, not observed MA difficulty rules. The lesson route follows `activity/first-step` then `step/next`: introduction 65053, positive integer exponent KP64203 (65054), this negative integer exponent KP64204 (65055), fractional exponent KP64205 (65056), general formula (65057). The prior topics are the sum rule and chain rule. The next linear-rational and exponential-substitution KPs are excluded. The final general formula explicitly permits integer n other than -1; the authored policy stays with negative integers away from that branch and uses the source’s reciprocal format.

Meaningful task identity is the actual rational integrand, normalized as n/a^m and b/a with exponent m. Profiles, banks, C, seed and choice shuffles never inflate capacity. Presentation identity includes normalized full prompt, full solution and complete bank. The finite domain is deduplicated before selecting a batch; overflow is rejected. `capacity.json` reports actual capacities, not requested seed counts.
