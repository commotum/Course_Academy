# Template extraction — four stages

## 1. Specific original objects

q-2382: ∫z exp(z²) dz, ratio1/2, easy monomial derivative, five options. Substitution introduction includes a trailing space before its paragraph break. Its nested aligned environments are literal source syntax. Its final answer displays the exponential in a fraction numerator; its integration row has an explicit dot.

q-73662: ∫(4x−1) exp(2x²−x) dx, exact derivative. Unlike the other solutions, it omits redundant multiplier/constant-out and u-primitive rows, finishing directly in the original variable. Its bank includes x-dependent factor and polynomial-addition errors.

q-73664: ∫6x² exp(5−2x³) dx, ratio−1. The substituted differential is explicitly grouped (−du), followed by constant extraction and primitive/back-substitution.

q-73798: ∫3x² exp(3x³+1) dx, ratio1/3. Five scalar bank coefficients retain different derivative coefficient/power multipliers.

q-113847: ∫8x³ exp(4−x⁴) dx, ratio−2. The substituted multiplier is grouped (−2), then extracted. The bank contains multiplier reciprocals and sign reversals.

q-13737: “What is” ∫4x² exp(x³+2) dx; no difficulty, correct reference, or solution. Five scalar options are present. Its correct1.333… coefficient is independently derived as4/3.

q-73663: “What is” ∫5x exp(1−5x²) dx; no difficulty, correct reference, or solution. Five scalar options are present. Its correct coefficient is independently derived as−1/2.

Every complete original record is retained in source-cases.json, including raw keys, UUIDs, exact prompt, answer values, correct-reference presence, difficulty presence, and solution presence.

## 2. Shared pattern and response

Given p(v)e^{g(v)} with p proportional to g′, identify u=g(v), compute du, determine the scalar ratio, reorder the integral, substitute, extract a nonunit scalar, integrate e^u, and back-substitute. Select one complete antiderivative family +C from exactly five math radio options. Unit-ratio exact derivative retains its shorter observed solution sequence. The target remains an indefinite natural exponential product; variation changes complete polynomial components, never isolated prose tokens.

## 3. Complete option-component mapping

Let E=e^{g(v)}, n the exponent power, a its leading coefficient, c the outside monomial coefficient, r=c/(an). For exact-derivative family r=1 and p=g′. Order below is captured source order, not normal shuffled option order. Expressions are whole answer values, all followed by +C; the recipe identifier in generation matches the listed operation. The exact source strings are included in source-cases.json; actual rendered strings are independently parsed by validate.py.

| Source | Complete five-choice recipe bank at all parameters | Original coefficients/expressions | Correct position |
|---|---|---|---|
| q-2382 | rE; anE; E; r e^v; −rE | E/2;2E;E;e^z/2;−E/2 | 1 |
| q-73662 | avE;E;E+av²;anE;gE | 2xE;E;E+2x²;4E;(2x²−x)E | 2 |
| q-73664 | E/(an);−E/n;rE;cE;−E/a | −E/6;−E/3;−E;6E;E/2 | 3 |
| q-73798 | E/(an);E/(a²n);rE;E;aE | E/9;E/27;E/3;E;3E | 3 |
| q-113847 | rE;E/r;E;−rE;−E/r | −2E;−E/2;E;2E;E/2 | 1 |
| q-13737 | rE;E/c;E/r;cE;E/n | 4E/3;E/4;3E/4;4E;E/3 | inferred1, designation absent |
| q-73663 | cE;E/abs(an);nE;rE;E/a | 5E;E/10;2E;−E/2;−E/5 | inferred4, designation absent |

Historical scalar recipes are mathematical pattern recovery, not recovered author intent. The reciprocal/outside and isolated-power values in the two unrated banks especially underdetermine the mistake. Public observed/raw profiles retain each COMPLETE bank, apply these explicit parameterized operations, and reject the whole instance on any equivalence. Raw profiles and both legacy observed profiles are evidence-only; completed opaque banks remain ineligible for normal learning. Normal legacy family defaults use the complete separately authored bank [rE,−rE,cE,anE,r e^v]: correct multiplier, reversed sign, omitted derivative division, multiplied instead of divided derivative coefficient, dropped exponent power. This bank is chosen before parameters; no individual option is replaced after a collision.

## 4. Backbone, slots, bounds and dependent masks

All mathematical components derive from the same exact instance. Common slots: variable x/z/t (cosmetic, excluded from task fingerprint); integer shift b∈[−5,5]; fixed familiar power n. a,c and optional linear term l vary according to the family below. Every occurrence in prompt, u-definition, differential relation, aligned rows, final answer and all options is recomputed. The exponential coefficient is interpreted as Euler e in the independent parser.

| Family | Permitted slots and invariant workload |
|---|---|
| quadratic_monomial | n=2, a=1..4 positive, c=1, l=0. Familiar quadratic derivative and one small positive reciprocal. Canonical z is an alias. |
| quadratic_exact | n=2, a=1..5 positive, l∈{−5..−1,1..5}, c=1. p=g′ exactly, two visible terms and unit ratio; shorter source solution. |
| cubic_positive | n=3, a=2..5, c=3, l=0. Scaled familiar cubic and reciprocal inner coefficient. |
| cubic_negative | n=3, a=−5..−2, c=−3a, l=0. Scaled familiar cubic and sign reversal, r=−1. |
| quartic_negative | n=4, a=−3..−1, c=5..16, l=0, 1<abs(r)≤4. Negative quartic derivative and negative nonunit ratio. Reduced ratio excludes unit and reciprocal-unit cases. |
| legacy_cubic | n=3,a=1,c∈{2,4,5,6,7,8},l=0. Familiar cubic, nonunit ratio; authored moderate completion. |
| legacy_quadratic | n=2,a=−5..−2,c=2..8,l=0. Signed scaled quadratic and small ratio; authored moderate completion. |

Explicit inputs obey exactly the same guards as sampling. A complete bank is selected before sampling; any option-pair derivative equivalence modulo C rejects the entire instance, including incorrect/incorrect pairs. All expressions are entire real-variable functions, so no branch or singularity is introduced. Negative exponents retain source constant-before-power order. Negative grouped multiplier and the −du special case preserve their distinct source layout. c=1 omits only the coefficient token; ratio1 in exact derivative omits redundant solution stages rather than injecting generic extra rows.

Presentation repair: normal q-2382 removes outer duplicate aligned only. Source bytes remain in source.json, original records, and public raw replay. No mathematical source repair was needed. The two absent keys/solutions receive independently verified authored completions only outside raw replay; a missing designation is never counted as a matched designation. All source profiles reproduce original complete bank, prompt, and available solution at anchor values via the same algebraic recipes as changed values. No source-return branch exists.

Task fingerprint is canonical integrand after variable alias normalization, without seed, profile, answer bank, or option order. Identity uses version, actual difficulty presence/value, actual prompt, fixed solution presence/value, complete displayed bank, and correct-designation presence. Answer UUIDs are field-owned and derived from displayed values. An arbitrary seed or shuffled order cannot change identity. Different displays do change identity.

Variation count is meaningful assessed integrands, not bank or notation aliases. Bounded positive monomial, two-term exact derivative, scaled signed cubics and quartic families admit hundreds of independent integrands. validate.py measures default-family coverage and task counts across90 seeds per level. Review includes original raw replay, completed/normalized original, and two changed-parameter examples for every family (therefore at least two per difficulty).
