# Four-stage extraction

## 1. Describe each source

All sources ask to evaluate d/dt[f(r(t))] at a specified t. The gradient is supplied as an i,j vector; the curve also has two components. They contain no plots. Exact scalar options are radio5. Their fixed prose and six display blocks occur in this order: formal chain rule; supplied gradient; substitution/composition; formal component derivative and evaluated velocity; formal dot product, explicit vectors, scalar products and simplification; evaluation at the requested point. Source-specific intermediate row counts are preserved, not padded to a common generic count.

| Source | Point | Gradient | Curve | Composition / velocity / dot / evaluation RHS row counts |
|---|---|---|---|---|
| q-36215 | 1 | (2x/(x²+3y),3/(x²+3y)) | (t,t²) | 4 / 2 / 6 / 1 (contains two equals) |
| q-94872 | pi/2 | (sin y,x cos y) | (t/2,t) | 1 / 2 / 4 / 3 |
| q-167497 | pi | (2xy cos(x²),sin(x²)) | (sqrt t,t/2) | 1 / 2 / 4 / 3 |
| q-167498 | -1 | (2x exp(x²+y),exp(x²+y)) | (sin t,t+cos²t) | 2 / 2 / 5 / 1 (contains two equals) |
| q-37106 | 1 | (1/x,1/y) | (2t²+2,arctan t) | 1 / 2 / 5 / 3 |
| q-37109 | 0 | (y(ln x+1),x ln x) | (exp(2t),sin(2t)) | 2 / 2 / 4 / 1 (contains two equals) |
| q-94873 | 1 | (2x,2y) | (exp(-t),exp(t)) | 1 / 2 / 4 / 2 |
| q-94878 | pi/8 | (-y sin(xy),-x sin(xy)) | (2sqrt t,-2sqrt t) | 2 / 2 / 5 / 3 |

## 2. Shared mathematical pattern

Substitute both path components into the supplied gradient, differentiate both path components, form their dot product, simplify, then evaluate. All components, operators and point-substitution stages remain visible. Source replay uses extracted complete mathematical RHS masks, not a stored question-return branch or a correct-answer lookup. Coherent parameters c and k scale the given gradient by c and replace the curve argument t by kt, with evaluation point q/k. Thus composition scales by c, velocity by k and the full derivative and numeric options by ck. Unit coefficients are suppressed by the same renderer to match source notation exactly.

## 3. Complete source banks and component mapping

Every listed value belongs to the single source `selection` field. Source values are parsed independently and compared one-to-one with the generated bank, ignoring choice order, while correct designation is checked separately. Asterisks identify the captured correct option.

| Explicit profile | Complete scalar patterns, before common ck factor |
|---|---|
| observed_q-36215 | 1/2; 6; 1; **2***; 4 |
| observed_q-94872 | 2-pi; 0; pi/4; **1/2***; -1 |
| observed_q-167497 | -2pi; 1/2; pi; **-pi/2***; -1 |
| observed_q-167498 | **1***; 2/e; 2e; e; 1/2 |
| observed_q-37106 | 1; **(pi+2)/pi***; (pi+1)/pi; pi/(pi+2); pi/(pi+1) |
| observed_q-37109 | 3; 4; 2; 1; **0*** |
| observed_q-94873 | 2-3exp(-1); 3e+exp(-1); **2exp(2)-2exp(-2)***; 4exp(2); -4exp(-1) |
| observed_q-94878 | **-4***; 0; 2; -sqrt(pi)/2; sqrt(pi)/4 |

These are explicit numerical-pattern replay formulas, not recovered authoring mistakes. Their common scaling is justified for coherent function scaling and time dilation; their original distractor intent is unresolved. They are never automatically selected for default learner generation. Correct values are computed from actual gradients and curves; no correct-answer table exists.

Source prompt gradient, curve and evaluation are complete slots. Every display row is a complete RHS slot. Abstract r(t), the differentiation variable and basis names are protected when time is dilated. Both coordinate substitutions in prose are transformed; the final point in prose and the equation LHS is transformed too. Arithmetic stages and redundant rows remain in their source order. Raw source stays in `source.json`; `raw_observed_q-94878` also replays its complete erroneous solution through the public API. It remains evidence-only and ineligible for learning. Corrected observed profiles retain the same opaque bank eligibility limit.

Default complete authored bank profiles are explicit operation lists. Let A=Gx(r(q))*x′(q), B=Gy(r(q))*y′(q), gx=Gx(r(q)), gy=Gy(r(q)), vx=x′(q), vy=y′(q).

| Profile | Ordered whole bank |
|---|---|
| component_sign | A+B, B, A, -A+B, A-B |
| velocity_omission | A+B, gx+B, A+gy, gx+gy, vx+vy |
| dot_arithmetic | A+B, A-B, -(A+B), AB, gx+gy |
| chain_input | A+B, gradient·position, gradient·r″, gx*vy+gy*vx, gx²+gy² |

These operations are author metadata only. No learner-facing diagnoses are added. A complete profile is chosen before computing its options; a collision or undefined member rejects the whole sampled instance. Explicit invalid parameters or ineligible requested bank are rejected rather than changed.

## 4. Reusable recipes, scope and bounds

Source-layout masks support c=1..4 and k=1..3. This bounded family does not purport to reconstruct all original hidden parameters. Default templates vary actual gradient coefficients, path coefficients and evaluation point independently through `model`, `sample` and `bounds`. All are real; denominators must be nonzero; square-root paths have positive parameter. Familiar sine arguments are integer multiples of pi/2 or pi; arctan arguments are ±1. Rational-family evaluation points are ±1 or ±2; exponential point values are small integers. Logs render as ln; exponential templates retain exponential notation.

Easy authored coefficients are positive integers 1..4. Moderate curve coefficients b,d are both 2..4: logarithm simplification plus two inner derivative factors, or two nonunit signed square-root factors entering sin(xy). Hard coupled coefficients a,b,d are 2..3. Hard trigonometric points have kq equal to an odd multiple of pi/4, so both coordinates and every coupling are active. Hard exponential points are ±1 with a quadratic/linear curve; coefficients keep powers and exact exponential arguments bounded. Every explicit parameter call enforces these same constraints.

Hard is an authored workload claim. Canonical e-8282 already supplies an affine coupled gradient and trigonometric curve with identity-based reduction and final familiar-angle evaluation. `coupled_trig` adds a nonzero self-coordinate term to both coupled components, at a point where both coordinates contribute. `product_exp` combines the supplied exponential gradient from easy q-167498, the product-in-gradient composition from moderate q-94878, and linear gradient terms from q-94873, with polynomial curve components. Both hard templates have two nonzero terms in each gradient component and four substantive products before collection. Neither introduces a new differentiation theorem, new dimension or requirement to derive the gradient.

The actual activity route follows first-step/next: Introduction → 2-variable chain rule → 3-variable chain rule → this KP → derivative as a rate → contextual rate-at-point sibling → intuition. The owning topic lists prerequisites Differentiating Vector-Valued Functions, The Multivariable Chain Rule and The Gradient Vector. `route-evidence.json` records traversal. The three earlier sibling KPs are read-only scope anchors; the contextual rate sibling has a separate request and gradient-computation step and is not merged here.

The canonical task fingerprint uses symbolic supplied gradient, actual curve and point, excludes answer banks and unused parameter aliases. Content identity hashes displayed prompt, fixed solution, complete sorted bank, correct value, version and level. Shuffling cannot change identity; changing a displayed bank must change it. Numeric coefficients that define actual differentiation/substitution are substantive; unused generic parameter slots cannot inflate fingerprints. All six display blocks are validated from the actual printed math, including formal operators, every distributed/intermediate sum and point substitution.
