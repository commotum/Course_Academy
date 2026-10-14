# Four-stage extraction

## 1. Specific source descriptions

q-31244 asks “What is” an inline display-style integral 3e^x dx. It is unrated, has no solution or correct reference, and has five whole-primitive radio choices. q-31245 uses -2; q-113853 uses -4; q-71914 uses -5. All three are easy and use the same integral-equals prompt plus the same source factorization prose and two aligned rows. q-71900 is moderate, coefficient 1/2, otherwise identical. q-71918 is hard, coefficient pi², otherwise identical. The symbolic coefficient is a constant with respect to x.

Every choice contains +C. Source notation includes braced e, fraction positions, exponent spellings 1/2x and ln⁡x, and spaces in pi². The raw masks reproduce these actual strings. All six are distinct complete bank profiles; source-choice-map.json accounts for every original record/value/recipe. Source-cases.json supplies exact public API replay parameters.

## 2. Shared pattern and instructional backbone

Calculate the indefinite integral of c e^x using the constant multiple rule and integral e^x=e^x+C. Supply one entire antiderivative as a five-choice selection. In the aligned family the fixed solution begins “Factoring out the constant … and calculating the resulting integral, we get”, then prints the original integral, c outside the basic integral, and the final c e^x+C. Every generated instance has one solution independent of the selected wrong answer.

## 3. Component/choice mapping

Let A=c exp(x), B=exp(x)/c. Each profile contains the correct A and four simultaneous distractors:

| Profile | Original c | Complete wrong-expression bank |
|---|---|---|
| raw:q-31244 | 3 | c exp(-x), exp(cx), c exp(ln x), B |
| raw:q-31245 | -2 | c exp(-x), exp(cx), c exp(ln x), B |
| raw:q-113853 | -4 | B, -c exp(-x), -B, -A |
| raw:q-71914 | -5 | B, exp(x), -c exp(-cx), exp(cx) |
| raw:q-71900 | 1/2 | c exp(x/c), exp(x), c exp(cx), B |
| raw:q-71918 | pi² | exp(x)/D, B, D exp(x), exp(x), where D=2pi |

For symbolic extension D is obtained by incorrectly treating c=m*pi^p as m*z^p and differentiating with respect to z, then substituting pi. This recovers the source derivative/reciprocal-derivative options at pi². It is a wrong operation, never part of the worked solution.

The historical -c exp(-cx) expression has an opaque intended error. Its parameterized expression is preserved with that limitation, and raw banks are evidence-only. Normal method_omit uses the separate authored operation c exp(cx), meaning copy the given coefficient into the exponent while retaining it outside. No numerical perturbations or mixed pools are used.

Normal method_exponent and method_reciprocal_sign reproduce complete observed expression shapes; their pedagogical interpretations remain hypotheses. Normal method_rational and method_symbolic preserve their corresponding source masks. The five default complete profiles are chosen before sampling coefficients. Every pair is compared by derivatives, rejecting the entire instance on equivalence up to an integration constant. The historical banks are all mathematically unambiguous.

Easy defaults select both observed prompt layouts, integer_constant and what_integral. Completing the unrated what_integral layout with the shared solution is authored normal content; raw replay continues to omit its solution/reference/rating. Layout changes do not increase mathematical task counts. Validation checks default coverage of all four templates and all five normal profiles.

Captured source has 30 options with 5 designated correct refs and 25 values not designated correct; the unrated bank contributes one independently inferred correct value among those 25. Thus mathematical classification has 6 correct and 24 incorrect values, while captured designated distractor coverage is 20/20 plus 4 inferred wrong values. No missing designation is claimed as captured fidelity.

## 4. Reusable template and slot constraints

Fixed: variable x; exponent x in the supplied integrand; Euler base e; one constant multiple; whole-primitive five-choice radio; field key selection; ordered factor-out/basic-integral/final stages; arbitrary C. There is no final prose equation apart from the final aligned conclusion, which is checked independently.

Variable: the complete constant c and selected whole-bank profile. Every reference to c in the prompt, introductory prose, factorization stage, primitive and bank is derived from the same exact constant. Explicit inputs enforce the same bounds as sampling. Rational aliases such as 2/4 canonicalize to 1/2 before rendering/fingerprinting. Mathematical fingerprints exclude profile, notation, UUID, seed, bank and option order, using the canonical integrand and assessed response. Content identities include actual level, prompt, fixed solution, and entire displayed bank.

Authored bounds: easy c is any signed integer with 2<=|c|<=12; moderate c is a reduced positive proper fraction n/d with n<=9,d<=12; hard c=m*pi^p with integer m, 1<=|m|<=5, and p in 2..5. These extend the source integer/rational/power forms without additional integration steps. Unit coefficients are excluded because they collapse distractors and remove the constant's number-form demand. The moderate fraction must remain nonintegral; symbolic pi powers remain hard. Bounds are modest arithmetic extensions of the constant-multiple prerequisite, not recovered difficulty labels or original sampling policies.

All complete source expressions replay through generate with explicit raw profiles, not a literal source-record return. Raw what_integral preserves its missing solution even at changed coefficients. Normal solutions retain the original shared prose and both operative rows at changed coefficients. No feedback, blanks, variable constants, trigonometric/logarithmic integration, sums, general bases, e^(ax+b), plots or chain/substitution stages are introduced. A ln distractor is a historically observed wrong value, not a new integration demand.
