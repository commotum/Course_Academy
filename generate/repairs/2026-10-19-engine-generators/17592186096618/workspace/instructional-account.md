# Instructional account

## Source and operation

Source: ../source/source.json, math basis 3950, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. All 17 practice records, the canonical example e-3635, lesson tutorial 2622, lesson step 12329, and supplied exponential/logarithmic prerequisite examples were inspected. No diagrams occur; plot rating none.

Before selecting values, the learner must identify two factors, differentiate each factor using the power, exponential, logarithm or elementary trigonometric rule, retain the other factor in each term, then add u'v and uv'. A blank asks for the indicated missing term, not the entire derivative. Radio asks for the whole derivative. Tutorial 2622 explicitly gives `(uv)' = u'v + uv'` and says algebraically multiplying first can be impossible or tedious. Canonical e-3635 identifies `u=x^2`, `v=ln x`, substitutes their derivatives, simplifies, and factors. These passages justify two factors and exactly two product-rule contributions. No tangent evaluation, quotient rule, nested nonlinear chain rule, or arbitrary polynomial expansion is introduced.

Observed difficulty is easy for 15 questions; q-1933 and q-47966 have no difficulty, solution, or explicit correct reference. Their answers and solutions can be reconstructed unambiguously by the same product rule; source replay preserves their absent difficulty. Normal practice assigns their same-method variants easy. Default easy; moderate and hard unsupported because the source supplies no calibration for them. The draft's binomial/trinomial moderate/hard additions are removed from supported generation.

## Extracted families and banks

Each line describes one prompt/solution backbone. Blank left/right masks are eligible roles within a common factor family, not inherently different skills. All blanks retain one field named field-1; radio retains one selection field and five choices. Source wording is retained, with canonical TeX repairs and parameterized component references. Solutions identify u and v, show the differentiated-factor products, substitute derivatives, and simplify; radio factoring stages remain where observed.

- q-1933: `c log_b(x) ln(x)`, whole derivative. Observed five recipes: correct `c log_b(x)/x + c ln(x)/(x ln b)`; omit ln b in second term; omit log in first term; omit c in second term; omit ln x in second term. c=5,b=3.
- q-47966: `x^n log_b(x)`, n=-3,b=2. Correct `x^(n-1)(n log_b(x)+1/ln b)`; omit log-base scale; multiply derivatives; `x^n(-n log_b(x)-1/ln b)` (compound sign and exponent error); add derivatives.
- q-11841: `x b^x`, b=3. Correct `(1+x ln b)b^x`; omit x and first term, omit x only, omit second term, omit first term.
- q-1916: `c x^n e^x`, c=1,n=2. Correct `c(x+n)x^(n-1)e^x`; fail to reduce power; omit exponential from either contribution; use n-1 instead of n in factored coefficient.
- q-1934: `cos(x) log_b(x)`, b=10 shown as common log. Correct `cos(x)/(x ln b)-sin(x)log_b(x)`; omit x, omit base scale, wrong trig sign, omit log and base scale.
- q-47954: `sqrt(x)e^x`. Correct `(e^x+2xe^x)/(2sqrt(x))`; original other values `1+e^x/(2sqrt(x))`, `x+2e^x/sqrt(x)`, `(1+2e^x)/(2sqrt(x))`, `(e^x+xe^x)/sqrt(x)`. These are observed compound expression patterns; no single misconception is claimed. Extension replaces e^x by e^(kx) with k=1..3, preserving power/exponential derivative workload already present in q-319909.
- q-319421 and q-311231: `b^x sin(x)` / `b^x cos(x)`, left missing, b=5/3. q-319425: `b^x tan(x)`, right missing, b=4. Allowed target is either product-rule contribution. Right cosine contribution is negative and is requested as the positive magnitude after a printed minus sign.
- q-319909/q-319903: `c x^n e^(kx)`, right missing at (1,2,2)/(5,2,1). q-319902: same family left missing at (1,3,1). Source includes one equivalent answer alias on q-319902.
- q-320814/q-320815/q-320816: `b^(kx) log_d(x)`, left/right/left missing, (3,3,1)/(4,4,1)/(5,7,-1). These sources establish equal and unequal bases and positive/negative scale. Either target may vary at fixed factors; base equality is not frozen to a target. q-320816 has an equivalent answer alias.
- q-320820: `tan(x) log(x)` left missing, hint explicitly fixes base 10. Either term may be missing; the base remains 10 to preserve the hint and common-log interpretation.
- q-320824: `(x^n+h)ln(x)`, right missing at n=2,h=3. Either contribution may be missing; n=2..4,h=0..5 are same-method slots; h=0 is explicitly established by canonical e-3635. The nonzero constant matters in uv' but not u'v. The source's extra answer `2x ln x+x+3/x` is the full derivative, contradicting its fragment prompt. Keep this value in immutable evidence but exclude it from generated choices; correct reference `(x^2+3)/x` agrees with the solution.

Raw source records are retained in evidence/source-questions.json. Replay compares every original choice separately, with one documented erroneous alias exclusion. Exact source labels and complete valid banks, including equivalent blank aliases, are replayed.

## Decision variation before incidental values

Normal sampling first chooses a family, then for blank families independently chooses missing side (left or right). For base/log families it next chooses sign case k=-1 or k=1; only then bases b,d=2..10, allowing equal and unequal, are sampled. Power/exponential uses c=1..6,n=2..4,k=1..3. Negative power/log uses n=-4..-1,b=2..10. Log/log uses c=2..6 (c=1 would collapse two observed choices), b=2..10. Trig/base uses b=2..10. The power/exp radio keeps k=1 because its observed factoring stages use e^x; coefficient and exponent still affect the correct arithmetic. Linear/base keeps a linear factor c*x because raising its degree changes this factoring workload. Its coefficient c=1..6 is a conservative constant-multiple extension; the base has nine values. The same constant-multiple extension c=1..6 is used for cosine/log and radical/exp without adding derivative stages. Radical/exp keeps sqrt(x) because changing root order changes the derivative rule and simplification. All other restrictions keep atomic factors, small coefficients and comparable algebra.

Radio observed banks are retained for explicit replay requests (`replay=True`). Default practice uses an authored two-contribution coefficient bank. The exact coefficients (a,b) multiply the fixed derivative-term bases, and five pairs include the true (a,b), a left-only error, a right-only error, a coherent error in both, and a fifth pair in a third column attached to either row. Direction, third-column placement, and attached row are selected before numerical values. The true pair occupies any corner of the shared two-by-two rectangle; the extra pair attaches independently, so proximity to it does not determine the key. In particular, each correct individual coefficient also appears in a wrong choice; the true relationship between the two coefficients also appears in wrong choices. This removes the original unique syntax and the first draft's single-coefficient-copying shortcut. Scalar wrappers retain zero and unit terms visually, so the number of printed summands does not reveal correctness. Options are shuffled only after all mathematical values exist. All default options have the same two-term structure and source choice count; the mathematical task remains the full derivative.

For log/log, the two terms are equal as functions, so two-coordinate distractors would collide. Its default bank varies the combined scalar in five consecutive integers with the true coefficient 2c at any rank. This doubling is a legitimate product-rule simplification: `(ln x)^2/ln b` has two equal differentiated-factor contributions. It requires doubling the supplied coefficient, not copying an incidental label, position or layout. The solution continues to show both product-rule contributions. No claim is made that repeated success on this finite recognizable family establishes the entire knowledge point. Likewise the linear family has the valid derivative pair (c,c): recognizing that relation is part of differentiating c*x and b^x, while multiple distractors preserve the equal-pair relation. Default banks are explicitly authored extensions; observed banks remain complete replay artifacts and are not sampled in practice.

For blanks, either left or right contribution is eligible. Known-term copying must fail; target swaps at otherwise identical data change the requested answer, printed known term and grader expectations. Cosine right masks print subtraction and request its positive magnitude. In polynomial/log left masks, changing h is irrelevant to the answer but changes the supplied factor and known term. Other numerical slots are relevant mathematical evidence, not semantic counts by seeds or IDs.

## Coverage obligations and limits

Replay all 17 sources and every bank value; verify all 6 observed radio profiles plus all authored bank error directions/placements/attached rows, every blank family with both targets, all exponent sign/base-equality cases, and parameter endpoints. Check independently differentiated full products and missing fragments, uniqueness of radio values as functions (not at isolated x), source aliases, and rejection guards. Test actual native grading for all choices, fragment/full-answer confusion, equivalent math and wrong submissions. Render representative source-style and extension records in the actual UI, then inspect screenshots.

Counterfactuals hold numerical factors fixed while switching blank target; hold a radio candidate bank fixed while changing the correct derivative coefficient through prompt parameters where possible; change h with a left polynomial mask and require response preservation. Probe option position, shortest/longest choice, coefficient rank, first/second-coefficient copying and copy-known-term strategies per family and coefficient-role subgroup before/after actual delivery filtering. Source observed radio banks have known structural cues, so are explicitly replay-only by default. No live learner history is available: read-only selection analysis covers difficulty-first uniform selection among fresh easy records, not a guarantee for every learner's history. Source inventory filtering is measured using the shared delivery tool. Output has no assets, network calls or database writes.

## Implementation and validation notes

The actual source has 16 retained implementation identifiers for 17 questions; several identifiers represent masks of the same factor family. Coverage counts distinguish those identifiers from semantic tasks: a semantic task is the product as a mathematical function plus the requested contribution, excluding seed, option order and bank-window changes. Rejection is unnecessary within the declared sampled domain; explicit invalid coefficients, bases, and exponents fail early. Native equivalence tests document a platform limitation comparing negative-power notation with positive-power denominator notation, although both agree on x>0 and independent exact checks pass. The source negative-power records are radio questions, whose actual selected-choice grading passes; normal banks use fraction notation consistently. The required expanded-log regression exposes the grader's inability to prove ln(4)=2ln(2); this is an unresolved delivery blocker, and the current author result is unsupported. Canonical answers, canceling-scalar equivalents, source aliases, and wrong responses are tested directly.

## Review repair specification (2026-10-18)

Feedback identified an unjustified h>=1 restriction. Canonical e-3635
(6bb0eded-7277-5ab5-8c13-bfc480403b1a), repeated in lesson step 12329,
explicitly differentiates x^2 ln x by identifying u=x^2 and v=ln x,
forming 2x ln x+x^2(1/x), and simplifying to 2x ln x+x. Together with
q-320824's (x^2+3)ln x scaffold, this supports h=0..5 in (x^n+h)ln x,
n=2..4. Zero is observed, not merely a conservative extension; other small
powers remain the existing same-method extension. No nonzero shift is needed
for either product-rule stage. Normal sampling must include zero as well as
positive shifts. At h=0, omit the printed +0 and retain the two-factor
identification and derivative substitution stages. Either missing contribution
is eligible at fixed n,h; swapping targets must change the key and known term
while preserving the full solution. Changing h from zero to nonzero preserves
the left contribution and changes the right contribution. Neither choice adds
a reasoning stage or changes the easy single-math-blank response contract.
Source replay at h=3 must remain unchanged, including the exclusion of the
incorrect full-derivative alias already documented above.

The second feedback item is an expected-accept native regression for q-320815:
4^x/(2x ln 2) must grade the same as 4^x/(x ln 4). Both expressions have domain
x!=0 and agree there since ln4=2ln2. This must remain an acceptance requirement,
not an allowed unresolved outcome. Inspect native comparison only to determine
whether the package can satisfy it without changing response requirements,
source banks, or files outside this workspace. Additional blank aliases cannot
repair it if the native grader compares only the single canonical answer.
If that engine behavior prevents a faithful package-level fix, retain the
expected-accept failure and return unsupported, explicitly identifying the
external engine limitation. Do not conceal it by changing the assessed skill,
constraining learner notation, or dropping composite bases.
