# Template extraction

## 1. Specific descriptions

q-334916 uses a constant unit P, constant Q=1, negative initial y(0), inline rather than display ODE, no captured solution or designations. q-335808 uses rational P=x/2, Q=x, positive y(0), inline ODE, no captured solution/designations. q-335810 begins outside standard form and divides by x; logarithmic IF calculation has six rows, integration three, initial substitution three; the empty display after the product rule is preserved in replay. q-335811 has P=2/x, cosine forcing, familiar π evaluation, zero integration constant; IF six rows, integration three, initial three. q-335812 has P=1/x, sine forcing, π/2 evaluation, explicit x>0, four IF rows, three integration rows, three initial rows, and a three-row final rearrangement. q-335806 cancels exponentials before integrating 2x; IF three rows, integration three, initial three. q-335829 integrates a coefficient times an exponential primitive before simplifying; IF three, integration four, initial three. q-339145 integrates using u=x²/12, retaining both u-antiderivative and back-substitution; IF three, integration five, initial three.

All answers are complete functions y(x), not general-solution families or scalar initial constants. IF answers are functions of x. Neither source layout asks for intermediate fields. Complete choices and raw malformed escapes remain in source.json and raw-original sections of review.md.

## 2. Shared pattern

Write y′+P(x)y=Q(x), compute nonzero I satisfying I′=PI, rewrite (Iy)′=IQ, integrate to Iy=F+C, apply y(t)=h to obtain C=hI(t)−F(t), and return the entire function y=(F+C)/I. Correctness requires both the displayed ODE and initial condition. Comparing IF candidates allows nonzero constant multiples; comparing particular solutions uses complete algebraic functions. General rows are checked as a family under reparameterizing C.

## 3. Components and whole-bank mapping

Let h denote the displayed initial value; c the derived integration constant. e(v)=exp(v), s=k sin(x). Mathematical expressions below map in source choice order, by field key. Every expression is a parameterized recipe; when its error intent cannot be identified, it remains evidence-only. Explicit profile `observed` is never selected by default.

| Source | IF field in original order | Full solution bank in original order |
|---|---|---|
| 334916 | x; e(x); x³; 1/x | 1+c e(x); 1+c e(−x); h e(x); e(−x)+c; h e(−x), c=h−1 |
| 335808 | 1/x; e(4x); e(x²/4); x³ | e(2x²); 2x+h; 2x²+h; 2+c e(−x²/4); 2+c e(x²), c=h−2 |
| 335810 | 2x; e(2x); e(x); x² | (h+1)x²−c/x²; x²+c/x²; x+c/x²; (h+1)x−c/x², c=h−1 |
| 335811 | e(x²); e(2x); x²; 2x | x²s; s/x; s/x²; s/x²; xs, h=0 |
| 335812 | 1/x; e(x); x; ln(x) | (2c+3cos(x))/(2x); (2c+4cos(x))/(2x); (2c−cos(x))/(2x); (c−cos(x))/x; (c−cos(x))/x, c=hπ/2 |
| 335806 | e(x); x; e(−x); x² | (x+h)e(x); (x²+h)e(x); h e(−x); (x+h)e(−x); (x²+h)e(−x) |
| 335829 | e(2x); 4x; e(4x); e(8x) | 2+c e(−4x); 1+(h−1)e(−4x); 4+(h−4)e(4x); h e(4x); h e(−4x), c=h−2 |
| 339145 | e(12x); 1/x; x⁶; e(x²/12) | 6+c e(x²); 6x+h; e(6x²); 6x²+h; 6+c e(−x²/12), c=h−6 |

Changing 2 to 3 in 335810's wrong leading coefficient, changing trigonometric scales 3/4 in 335812, and the unrelated exponents in 335808/339145 do not establish the original author's error mechanism. These are explicit expression-pattern hypotheses with fixed captured coefficients, kept only in observed replay profiles. No polynomial fits to source scalar answers are promoted to default recipes.

Source solution masks operate on complete initial-condition and particular-constant components, with coefficient matrices otherwise fixed. 335811 varies forcing amplitude k while retaining h=0 and the omitted zero-constant steps. Other observed presentations vary h; their P/Q remain fixed. Replacing initial-point π/2 is prohibited: only initial value and solved C components are slots. Unrated sources use a separately authored solution sequence.

## 4. Reusable template, constraints, and authored scope

Observed mask parameters: integer h from −8..8, except 335811 h=0 and amplitude k=1..5. All other source coefficients remain fixed. Complete banks are selected before sampling; invalid instances reject the entire bank. The ambiguous original banks are an explicit exception only in evidence profile, never normal practice. Wrong-choice arithmetic has no invented learner-facing diagnosis.

Authored easy: y′+y=b with b=1..6 and integer nonzero h=−6..6; h≠b. This applies the full KP method using a unit integrating factor exponent and a direct exponential primitive, with a three-row initial-condition calculation. It is anchored in the constant-coefficient practice sources, canonical example's final initial-condition step, and the prerequisite exponential substitution lesson. Easy is a design claim: no practice source has an easy label.

Authored moderate: peer variants of the observed divide-by-x power template, cancelling exponential template, and cancelling cosine/sine templates. b, a, or k=1..6 and h=−6..6, nonzero. Familiar evaluation points 1, π, π/2 stay fixed. No integration by parts, arbitrary-angle evaluation, noninteger powers, or new differential-equation method is added. These are equal-level alternatives, not a progression.

Authored hard: y′+(x/d)y=b x/d with d=2..6, or y′+(x²/d)y=b x²/d with d=1..4; b=1..6, h nonzero in −6..6, h≠b. Both need the same exponential substitution u=xⁿ/(nd) and initial condition at zero. The quadratic branch reproduces the observed hard demand; the cubic branch is anchored to canonical e-21743, which explicitly uses u=x³. No nonlinear equation or harder forcing integral is introduced.

Normal bank definitions: IF [I,1/I,ln(I),I²] for exponential families; [I,1/I,e^x,P] for x² families; [I,1/I,e^x,ln(x)] for the x family. Solution bank [y,(F−c)/I,c/I,F+c,F/I+c]. In the observed zero-C cosine template only, the authored whole solution bank is [y,−y,FI,F/x,Fx]. Every required member must exist and be unequal as a complete mathematical object. The nonstandard source's observed 4-choice solution bank is retained in observed replay; the 5-choice authored bank is a labeled extension.

Lesson route is followed from activity/first-step 17592186088817 through step/next: Introduction → Method → transforming KP87877 → general-solution KP87878 → IVP KP87879 → derivation. The key prerequisite is Integrating Exponential Functions Using Substitution (3770). Topic predecessors include direct integration, first-order linear ODE introduction, and integration by parts, but no authored template requires additional integration-by-parts work. Topic successors about substitutions, mixtures, and d'Alembert equations do not define this scope.

## Source anomalies and fidelity denominators

335811 and 335812 each repeat the mathematically correct full solution, once with literal invisible-function-application notation. Thus their solution banks are ambiguous. Raw evidence profiles retain all five values and separate IDs; native ID grading accepts only the designated ID, so the equivalent duplicate is rejected by the engine. This is a source defect, not successful unambiguous practice. Normal authored banks replace the whole bank with method-based recipes, explicitly marked authored, rather than claiming a source repair recovered intent.

334916 and 335808 each lack two correct refs and a worked solution. Independently: I=e^x, y=1−4e^(−x) for the first; I=e^(x²/4), y=2−e^(−x²/4) for the second. Both are verified by differentiation and substitution into the actual displayed ODE/IC. The four values are derived; zero absent designations are counted matched. Six captured solutions are checked for full prose and stage-sequence fidelity separately from raw-exact strings and mathematical notation normalization.

Legacy double TeX escapes and literal `\u2061` are presentation-normalized in generated answer values. Raw strings stay in source.json/review.md; mathematical option matching is one-to-one including duplicate occurrences. Source solutions retain their original \operatorname{ln} convention in explicit replay; normal authored presentation uses \ln. Raw empty displays are retained only in source replay.

Content identity hashes actual prompt, fixed worked solution and complete sorted banks; parameter/source/profile metadata are excluded. Answer UUIDs are field owned. A separate mathematical-task fingerprint hashes normalized P,Q,t,h, so template aliases, options, seed, profile and option order do not inflate task counts. Choice shuffling is deterministic and cannot change identity.

## Bounded meaningful variety

The nonzero initial-value policy and nonzero solved-constant guard give these bounded authored domains before complete-bank checks: easy constant 66 tasks; moderate power 66, exponential cancellation 432, cosine 72, sine 72; hard quadratic 330 and cubic 264. Counts refer to displayed ODE and IC pairs, not option permutations or profile aliases. Each numeric parameter affects the integrating factor, primitive coefficient, or initial constant calculation. The validator samples 12 deterministic instances per authored family, requires at least eight distinct mathematical fingerprints per family, and also rejects out-of-bounds and collapsing explicit instances. No claim of unlimited variety is made.


## Current-source update at basis 2010

The preceding historical extraction remains evidence of basis 1356. Current records and current replay take precedence for generation version ivp-integrating-factors-2. q-335808 now has an observed hard label, original correct refs and its full five-stage substitution worked solution; its source prompt is displayed rather than inline. The q-335808 particular-value masks replace the entire initial-value line, derived C line and final y expression; general solution steps remain fixed. q-334916 alone remains missing both designations and a source solution.

q-335830 is a ninth Markdown/value template with P=−2, Q=e^(2x)sin(x), I=e^(−2x), F=−cos(x), initial t=0, h=4, and c=h+1. Its solution sequence is standard form → IF (three rows) → product rule (three rows) → trig primitive/general y (three rows) → initial-condition calculation (three rows) → full particular y. Two select fields require I and the complete function y. There are no plots. The domain is real x.

Its observed IF profile, in captured order, is [e^(−2x), −2x, e^(2x), 2x]. Its observed solution profile is [e^(−2x)(1+3cos(x)), 2e^(−2x)(1+cos(x)), e^(2x)(h+1−cos(x)), e^(2x)(h−1+cos(x)), h e^(2x)cos(x)]. These formulas match all nine original values at h=4 and both correct designations. The fixed 1, 2, and 3 in the first two wrong options are observed coefficient patterns; their original mistake intent is unresolved. They are retained only for whole-bank evidence replay. Changed h in −8..8 updates the prompt, C and complete final function, while a=−2 stays fixed; no negative coefficient is silently excluded by the shared positive authored sampler.

The wrong IF options −2x and 2x differ by a constant factor. This profile is redundant under integrating-factor equivalence, although neither solves I′=PI. It is excluded from normal bank selection and validated inventory. An explicit authored q-335830 bank uses the existing complete exponential IF profile and complete solution-recipe profile, checks all options, and rejects collisions. The default replenishment sampler continues to use the seven already validated authored templates.

All nine current source banks replay one-to-one, including the two duplicate correct-value occurrences and the redundant wrong IF options as evidence-only exceptions. Current q-335808 and q-335830 prose/stage sequences are checked at original and changed initial values. Current captured identities and learner records are never reused for newly authored instances.
