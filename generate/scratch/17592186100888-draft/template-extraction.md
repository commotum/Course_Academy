# Four-stage extraction and supported variable slots

## 1. Individual source descriptions

Exact original text/records are retained in `source.json`. `masks.json` contains extracted complete-component masks and all component spellings at original parameters.

- q-140631: y'=4y/x, x≠0; f=x⁴; asserted5x⁵. Actual derivative4x³; I false, II/III true. Preserve derivative-parenthesis spelling, three derivative rows, three substitution rows, punctuation and the final “II and III only” sentence.
- q-141078: y'=2y; f=e²ˣ; asserted2e²ˣ. All statements true. Two derivative rows and only two substitution rows; no redundant substituted-ky row is added.
- q-141080: y'=2y; f=(1/2)sin2x; asserted2cos2x. Four derivative rows include (1/2)·2cos2x before cos2x. Three substitution rows compare cos2x with sin2x. All statements false.
- q-141081: y'=y cos2x; f=cos2x; asserted−2sin2x. I true; II/III false. Two derivative rows and three substitution rows; retain source final `{cos}^{2}` spelling rather than claiming an escape repair.
- q-141082: y'=1/eʸ; f=lnx; asserted1/x. All statements true on x>0. Two derivative rows and three substitution rows, including exp(lnx) before1/x. Raw source omits an explicit positive interval.
- q-141084: y'=y/x², x≠0; f=−1/x²; asserted−2/x³. Actual derivative2/x³; substituted RHS−1/x⁴. All false. Three derivative rows and three substitution rows.
- q-141086: y'=−3y; f=3e⁻ˣ; asserted3e⁻ˣ. Actual derivative−3e⁻ˣ and substituted RHS−9e⁻ˣ. All false. Three derivative rows and three substitution rows.
- q-141088: y'=4x/e^(y/2); f=4lnx; asserted1/(4x). I false; II/III true on x>0. Three derivative rows and six substitution rows: formal ODE, substituted divided exponent,2lnx,ln(x²),x² denominator, final4/x.
- q-141089: y'=2y/x, x≠0; f=−3x²; asserted−5x. I false; II/III true. Four derivative rows retain−3·2x, then−6x, then inequality. Three substitution rows.

All current prompts explicitly say “Select all that apply” and label the three statements **I**, **II**, **III**. Every statement has its own Boolean checkbox field. The source solutions still conclude with the combined statement-set wording; this accurately describes the checked subset and is preserved.

Five captured independent moderate records use (a,n)=(-2,3),(-3,4),(-4,2),(-5,2),(-3,3). They have the same signed-power mask and corrected interval opening, with Boolean field order/option order varying in Pull. Their exact records are preserved separately. Their independent origin is not promoted to recovered MA difficulty evidence.

## 2. Backbone and purpose

One supplied function f(x), one first-order ODE already isolated as y'=R(x,y), one asserted derivative, and three fixed semantic statement roles: I derivative assertion; II substitution identity; III being a solution. Compute the actual derivative, test the assertion, substitute y=f into the actual printed RHS, and decide II and III together on a valid interval. The three checkbox keys and Boolean answer banks are the current answer-field backbone. The learner never finds an unknown solution.

Each family retains its own operative prose and ordered derivative/substitution stages. Every instance has one concrete worked solution independent of the learner's selection. The only normal prose correction changes the overbroad equation-domain phrase to the function's valid interval. Natural logarithm intervals are also made explicit in normal prompts. No extra solution method, response type, helper variable or stage is introduced for variety.

## 3. Components and complete Boolean banks

Complete-component slots: F proposed function, D actual derivative, C asserted wrong derivative where distinct, R ODE RHS, S substituted RHS, E evaluated RHS, P unevaluated coefficient/chain product, H/J/K successive exponential/log stages. `extract.py` uses a longest-first single-pass replacement of whole mathematical components. Slots never blindly replace a short letter or coefficient throughout prose. Formal derivative inputs, prose substitution functions/derivatives, and final function definitions share the same whole-function slot.

For each of the9 profiles, `masks.json.bank` maps **every** key I/II/III to the exact source option values `false` and `true`; all27 complete banks are present. `source.json` also retains original choice UUIDs, text types, correct values, and absent feedback. The parameterized recipe for each Boolean option is the literal truth category it names. The correct value is derived from the actual function/ODE relation; the alternative value is its negation. Banks are complete before sampling and need no scalar fitting, perturbation or first-valid substitution. Feedback is absent in both raw and normal output, matching all originals.

The moderate asserted−5x underdetermines historical error intent. The continuation (a−n)x^(n−1) is an explicitly authored plausible operation matching that source value: subtract the exponent from the signed coefficient instead of multiplying. It is **not recovered historical distractor intent**. Its claim must remain unequal to the actual derivative; (-2,2) is rejected as a whole instance. The independent inventory uses the same previously authored continuation and does not remove this uncertainty.

## 4. Reusable masks, slot bounds and calculations

`source-cases.json` supplies every MA original's template, exact parameters, observed level and public raw profile. All raw learner strings replay byte-exact through `generate`; raw records explicitly carry evidence_only=true/eligible_for_learning=false. Unprefixed profiles use the same source banks and the supported normal wording repair. `authored` and `boolean_statements` are normal Boolean-contract aliases; they create no new mathematical tasks or content identities.

| Template | Variable slots and bounds | Dependent components; fixed demand |
|---|---|---|
| power_easy | n=2..5 | f, derivative, asserted(n+1)x^(n+1), ny/x and substitution; one power derivative |
| exp_true | k=1..4 | e^(kx), claimed/actual chain derivative and ky; source omission of redundant row |
| sin_none | k=2..4, amplitude1/k | function, chain product and ODE multiplier; reciprocal-times-inner derivative |
| cos_i | k=1..4 | trig input, chain coefficient, cosine product/square; one trig chain derivative |
| log_all | h=−4..4 | ln(x+h), reciprocal derivative, substituted exponential and interval x+h>0 |
| inverse_none | n=2..5 | signed reciprocal function, derivative exponent and RHS denominator exponent |
| exp_none | a=2..5,k=1..4,b=1..5,b≠k | exponential amplitude/input, claimed omission, derivative and distinct ODE multiplier |
| log_scaled | m=1..4, outer scale2m | f, reciprocal claim, divided exponent and numerator; all six source substitution rows remain |
| power_moderate | a=−9..−2,n=2..5,a−n≠an | f, explicit a·n product, collected derivative, authored claim and ny/x; |an|≤45 |
| affine_log — authored hard | |a|=2..4,b=2..4,|c|=1..4; true/false derivative assertion and ODE identity | a ln(bx+c), chain product, divided exponential, bx+c>0 |

Moderate extends the registered coefficient range−5..−2 conservatively to−9..−2. It remains one signed nonunit coefficient-times-exponent calculation, bounded by45, with identical stages and n≤5. The original and all prior15 registered tasks remain supported; the extension gives31 meaningful tasks. The wider bound is authored, not additional observed difficulty evidence. Sampling and explicit calls use the same guards.

Hard retains the previously reviewed authored affine logarithm: f=a ln(bx+c), asserted derivative ab/(bx+c) or b/[a(bx+c)], ODE RHS ±ab exp(−y/a). Nonunit outer/inner scales and nonzero offset are mandatory, separating this workload from the easy shifted-log and moderate power families. Its four truth states have the same differentiation/substitution workload. Actual prerequisite/context support is logarithmic differentiation and exponential chain substitution; the assigned hard label remains a design claim with no rated hard original. It does not introduce solving, initial values, product rules, or the sibling multiple-function task.

Finite semantic capacity:96 easy,31 moderate,576 hard. Every bounded parameter combination is independently read from its displayed function/ODE, every permitted slot value is covered, and profile/field-enum/seed aliases preserve content identity. Mathematical fingerprints exclude bank profiles and order and use the actual f, asserted derivative, ODE RHS and valid domain. Content identities include version, actual difficulty, full prompt, fixed solution, and complete Boolean field contracts. Structural row checks reject a collapsed coefficient product even when its scalar equality remains true; mutation tests also reject stale final-function prose, incorrect formal derivative input, wrong Boolean truth and C0 corruption.

No plots occur. There is no renderer, asset cache, image model or dependency installation. Exact Python/SymPy versions and fresh native engine library/source/binary hashes are recorded. The registered numeric baseline and its full existing evidence/path set remain unchanged.
