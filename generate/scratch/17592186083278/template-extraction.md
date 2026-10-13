# Four-stage template extraction

## 1. Describe each source before generalizing

The complete raw prompt, optional solution, field key/type, exact values, correct-ref presence and captured difficulty are in source.json. source-cases.json supplies every original parameter/profile replay, including unrated q-21206. q-20853 is linear/quadratic, q-21206 linear/cubic; q-122726 odd fifth-power/linear. q-21072 has a closed half-circle interval and two horizontal endpoint parameters; q-21081 uses a right-open full period and two interior vertical parameters. q-350359 uses a monic quadratic x with half coefficients and a cubic y whose derivative factors into primitive (3t+2)(t+4); q-350368 and q-357255 have e^t times swapped sin/cos and exact diagonal angles, two ascending blank fragments. The source retains both the product-rule derivatives and a six-row trig solve chain, followed by explicit substitution and evaluated companion derivatives. Answers request parameters t, not coordinate points.

## 2. Generalized shared skill

Compute x'(t),y'(t). For a horizontal regular tangent solve y'=0 and check x'!=0; for a vertical regular tangent solve x'=0 and check y'!=0. Report the COMPLETE finite parameter set in the stated interval, retaining endpoints exactly as included/excluded. Every nonzero companion derivative check is necessary. Stationary parameterizations require further geometry and are excluded from this generator rather than silently designated H/V.

## 3. Components and complete banks

The table below enumerates EVERY source choice at the original parameter settings. Observed profiles are expression recipes, not literal-payload replay or arbitrary polynomial interpolation. The raw source includes exact type/value spelling and correct designation; the raw profile regenerates those values. Historical scalar formulas reproduce the bank but their original error intent remains unknown. No such bank is a normal default solely because its numeric values can be matched.

### q-20853 / line_quadratic

Field 0 key=selection type=:answer-field.type/radio; correct=t=0

| Exact source value | Type | Parameterized component mapping |
|---|---|---|
| `t=0` | :answer.type/math | Complete bank recipe below; independently compared at original parameters |
| `t=-2` | :answer.type/math | Complete bank recipe below; independently compared at original parameters |
| `t=1` | :answer.type/math | Complete bank recipe below; independently compared at original parameters |
| `t=3` | :answer.type/math | Complete bank recipe below; independently compared at original parameters |
| `t=-1` | :answer.type/math | Complete bank recipe below; independently compared at original parameters |

### q-21206 / line_cubic

Field 0 key=selection type=:answer-field.type/radio; correct=ABSENT

| Exact source value | Type | Parameterized component mapping |
|---|---|---|
| `t = 0` | :answer.type/math | Complete bank recipe below; independently compared at original parameters |
| `t = 1` | :answer.type/math | Complete bank recipe below; independently compared at original parameters |
| `t =-3` | :answer.type/math | Complete bank recipe below; independently compared at original parameters |
| `t =-1` | :answer.type/math | Complete bank recipe below; independently compared at original parameters |
| `t = 3` | :answer.type/math | Complete bank recipe below; independently compared at original parameters |

### q-21072 / circle_horizontal

Field 0 key=selection type=:answer-field.type/radio; correct=$t=0$ and $t=\pi $

| Exact source value | Type | Parameterized component mapping |
|---|---|---|
| `$t=0$ and $t=\frac{\pi }{2}$` | :answer.type/text | Complete bank recipe below; independently compared at original parameters |
| `$t=\frac{\pi }{4}$ and $t=\frac{\pi }{2}$` | :answer.type/text | Complete bank recipe below; independently compared at original parameters |
| `$t=0$ and $t=\pi $` | :answer.type/text | Complete bank recipe below; independently compared at original parameters |
| `$t=\frac{\pi }{4}$ and $t=\pi $` | :answer.type/text | Complete bank recipe below; independently compared at original parameters |
| `$t=\frac{\pi }{2}$ and $t=\pi $` | :answer.type/text | Complete bank recipe below; independently compared at original parameters |

### q-350359 / polynomial_two

Field 0 key=field-1 type=:answer-field.type/blank; correct=-4

| Exact source value | Type | Parameterized component mapping |
|---|---|---|
| `-4` | :answer.type/math | Complete bank recipe below; independently compared at original parameters |

Field 1 key=field-2 type=:answer-field.type/blank; correct=-\frac{2}{3}

| Exact source value | Type | Parameterized component mapping |
|---|---|---|
| `-\frac{2}{3}` | :answer.type/math | Complete bank recipe below; independently compared at original parameters |

### q-350368 / spiral_cos

Field 0 key=field-1 type=:answer-field.type/blank; correct=\frac{3\pi }{4}

| Exact source value | Type | Parameterized component mapping |
|---|---|---|
| `\frac{3\pi }{4}` | :answer.type/math | Complete bank recipe below; independently compared at original parameters |

Field 1 key=field-2 type=:answer-field.type/blank; correct=\frac{7\pi }{4}

| Exact source value | Type | Parameterized component mapping |
|---|---|---|
| `\frac{7\pi }{4}` | :answer.type/math | Complete bank recipe below; independently compared at original parameters |

### q-357255 / spiral_sin

Field 0 key=field-2 type=:answer-field.type/blank; correct=\frac{5\pi }{4}

| Exact source value | Type | Parameterized component mapping |
|---|---|---|
| `\frac{5\pi }{4}` | :answer.type/math | Complete bank recipe below; independently compared at original parameters |

Field 1 key=field-1 type=:answer-field.type/blank; correct=\frac{\pi }{4}

| Exact source value | Type | Parameterized component mapping |
|---|---|---|
| `\frac{\pi }{4}` | :answer.type/math | Complete bank recipe below; independently compared at original parameters |

### q-21081 / circle_vertical

Field 0 key=selection type=:answer-field.type/radio; correct=ABSENT

| Exact source value | Type | Parameterized component mapping |
|---|---|---|
| `$t = \frac{π}{2}$ only` | :answer.type/text | Complete bank recipe below; independently compared at original parameters |
| `$t = \frac{π}{2}$ and $t = \frac{3π}{2}$` | :answer.type/text | Complete bank recipe below; independently compared at original parameters |
| `$t = \frac{3π}{2}$ only` | :answer.type/text | Complete bank recipe below; independently compared at original parameters |
| `$t = \frac{π}{4}$ and $t = \frac{3π}{4}$` | :answer.type/text | Complete bank recipe below; independently compared at original parameters |
| `$t = \frac{π}{4}$ only` | :answer.type/text | Complete bank recipe below; independently compared at original parameters |

Field 1 key=selection type=:answer-field.type/radio; correct=$t=\frac{\pi }{2}$ and $t=\frac{3\pi }{2}$

| Exact source value | Type | Parameterized component mapping |
|---|---|---|
| `$t=\frac{3\pi }{2}$ only` | :answer.type/text | Complete bank recipe below; independently compared at original parameters |
| `$t=\frac{\pi }{2}$ and $t=\frac{3\pi }{2}$` | :answer.type/text | Complete bank recipe below; independently compared at original parameters |
| `$t=\frac{\pi }{4}$ only` | :answer.type/text | Complete bank recipe below; independently compared at original parameters |
| `$t=\frac{\pi }{4}$ and $t=\frac{3\pi }{4}$` | :answer.type/text | Complete bank recipe below; independently compared at original parameters |
| `$t=\frac{\pi }{2}$ only` | :answer.type/text | Complete bank recipe below; independently compared at original parameters |

### q-122726 / power_line

Field 0 key=selection type=:answer-field.type/radio; correct=t=0

| Exact source value | Type | Parameterized component mapping |
|---|---|---|
| `t=20` | :answer.type/math | Complete bank recipe below; independently compared at original parameters |
| `t=4` | :answer.type/math | Complete bank recipe below; independently compared at original parameters |
| `t=9` | :answer.type/math | Complete bank recipe below; independently compared at original parameters |
| `t=-1` | :answer.type/math | Complete bank recipe below; independently compared at original parameters |
| `t=0` | :answer.type/math | Complete bank recipe below; independently compared at original parameters |

Observed whole-bank recipes in operation order:

- line_quadratic: {s}, {-a}, {h}, {a+h}, {-h}; anchor a2,b4,h1,s0. Scalar distractor intent opaque.
- line_cubic: {s}, {s-h}, {s+3h}, {s+h}, {s-3h}; anchor a1,b1,h-1,k-2,s0. Offset pattern is evidence, not recovered intent. Missing correct ref remains absent in raw.
- power_line: {an}, {a}, {b}, {-1}, {s}; anchor a4,b9,n5,s0. Coefficient/exponent numbers observed; intention unknown.
- circle_horizontal, L=mπ: {L,L+π/2}, {L+π/4,L+π/2}, {L,L+π}, {L+π/4,L+π}, {L+π/2,L+π}. Whole sets are distinct; correct complete set is the third.
- circle_vertical, L=mπ: {L+3π/2}, {L+π/2,L+3π/2}, {L+π/4}, {L+π/4,L+3π/4}, {L+π/2}. Current source uses this order; legacy uses indices4,1,0,3,2 and Unicodeπ with spaced equal signs. Both are preserved.
- polynomial_two: blanks sorted {r,u/3}. Cubic y=t³-(3r+u)t²/2+ru t; dy=(3t-u)(t-r). x=t²+ct+d; check 2r+c and 2u/3+c nonzero.
- spiral_cos: x=a e^t cos(t+φ),y=b e^t sin(t+φ), φ=jπ/2. Solve sin(t+φ)+cos(t+φ)=0, divide by cos after noting it cannot be zero at a solution, tan=-1. Intersect all π-spaced diagonal-angle roots with [0,2π].
- spiral_sin: x=a e^t sin(t+φ),y=b e^t cos(t+φ). Solve cos-sin=0 -> sin=cos -> ratio=1 -> tan=1 -> all eligible roots. The field-key mapping enforces ascending answers even where capture order is field2 first.

Normal complete method banks are separately authored:

- line_quadratic: {s}, {-h}, {h}, {b}, {2b}. Wrong component root x=0, wrong sign of that linear root, confusing original y coefficient with a root, confusing differentiated coefficient with a root. Coefficient/root confusion is a method-derived error hypothesis, not a recovered source author intention.
- line_cubic: {s}, {-h}, {-3b}, {h}, {3b}. Wrong component root and its reversed sign; signed differentiated coefficient 3b confused with a root. The same derivative is used for both coefficient sign errors.
- power_line: {s}, {s+1}, {s-1}, {n-1}, {n}. Solve the isolated factor incorrectly as ±1 instead of0; confuse the derived exponent n-1 or original exponent n with the parameter root. The entire five-option bank is rejected on any collision.
- Trig banks retain the full observed omission/quarter-angle/set-confusion profiles. Blank families preserve exact fragment shapes and have no invented distractors.

## 4. Reusable masks, calculations and constraints

source_render fills complete equation, derivative, solving-chain, companion-substitution and conclusion components into the original source prose/Markdown skeleton. It does not return the literal original question at an anchor: all original values are recomputed through the same recipe. All seven source worked solutions replay byte-exact at anchors. The source q-21206 has no solution and raw retains that absence; normal reconstructs the common formal slope, rule, component derivatives, target solve/factor/root rows, regularity check and conclusion.

For every spiral phase, the product-rule block, exponential cancellation, trig rearrangement, sine/cosine quotient, tan equation and complete interval root list are preserved as separate operations. For the polynomial family, expanded derivative=0 -> primitive factor product=0 -> sorted roots, followed by substituted signed 2(root)+c and its evaluated value, is preserved. q-20853/q-122726 use single zero solve rows and prose nonzero check. Trig sources use complete two-row evaluation blocks. All final prose t values are fresh slots.

Raw preserves original Do not round wording; normal uses Give exact answers because the native grader otherwise rejects equivalent exact entries. No actual rounding requirements are removed. Raw attribute absence is part of evidence: no difficulty/solution/correct ref is fabricated. Normal duplicate-field repair uses authoritative widget evidence. Identity includes complete prompt, fixed solution, difficulty, field layout/bank and correct-ref presence; shuffling changes no content identity. Task fingerprint separately removes irrelevant translations/nonzero component scales.

Strict nonzero-scale, primitive rational-root, familiar-angle, ascending-order, finite-domain, regularity and level workload guards are documented in classification.md and enforced on explicit calls. Each whole bank is selected as a complete profile before sampling; collisions reject the entire instance. No first-valid distractor pool, mixed historical bank or answer lookup table exists.

No source geometry appears. Plot extraction/generation steps are inapplicable; plot-extraction.md records the none rating. No renderer, image model or SVG has been used.
