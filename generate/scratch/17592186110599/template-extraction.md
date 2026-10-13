# Template extraction

Provenance: unchanged basis-1356 `source.json`; source replay cases in `source-cases.json`; missing-field widget evidence in `original-widgets.json` and copied screenshots. All calculations use exact rationals.

## Stage 1: specific originals, without generalizing

| Source | Target slope/intercept | Original option intercepts in capture order | Specific number/layout features | Observed solution |
|---|---|---|---|---|
| q-72453 | 3, 2 | 6,6,6,6,6 | integer coefficient; spaced full equations | absent |
| q-72525 | 1/2, -3 | 4,-1/3,1/3,1,3 | `x/2` presentation; fractional option intercepts; spaced | absent |
| q-215888 | -1, 5 | -5,1,-1,3,5 | implicit ±1 coefficient; two 1/2 slopes | product `(-1)·1=-1` |
| q-215890 | 1, 1/2 | -2,9,1,1,-1/2 | implicit ±1 coefficient; ±2 slopes | product `1·(-1)=-1` |
| q-72524 | -1/2, 7 | 0,-3,5,-1,19 | target `-x/2`; two malformed quadratic distractors | product `-1/2·2=-1` |
| q-72527 | -4, 1 | -6,-1,-1/4,6,-1 | reciprocal coefficient; one horizontal option | product `-4·1/4=-1` |
| q-72528 | -5, -2 | 1/2,-8,4,2,1/2 | reciprocal coefficient; one horizontal option | product `-5·1/5=-1` |

All practice fields have key `selection`, type `:answer-field.type/radio`, five choices of `:answer.type/math`, and full-equation answer fragments. Five have observed correct refs. No source contains images/plot references in prompt, options, or solution. The topic introduction has a contextual graph; the assessed practice equations do not require reproducing that graph.

## Stage 2: shared pattern

Read m from an already explicit slope-intercept equation. Identify the sole displayed line whose coefficient is -1/m; confirm m(-1/m)=-1. Intercepts do not affect the perpendicular relationship. Response is a selected complete equation, not a slope entry, equation construction, or an unknown-parameter calculation.

## Stage 3: every original option mapped to a component recipe

Let x be the variable, m the given slope, b its intercept, and c1..c5 independently supplied option intercepts. A recipe `r` below renders the complete equation `y=r*x+ci`; `horizontal` renders `y=ci`; `quadratic_m` renders the raw evidence equation `y=m*x*x+ci`. These full-equation recipes reproduce every displayed value, rather than fitting numerical answer values. Option intercepts are explicit components because their historical misconception intent is underdetermined; no arbitrary fitted dependence on m or b is asserted.

| Profile/source | Field | Slot | Exact original choice | Coefficient/object recipe | Original correctness |
|---|---|---:|---|---|---|
| q-72453 | selection | 1 | `y = 3x + 6` | m | absent ref |
| q-72453 | selection | 2 | `y =-x + 6` | -1 | absent ref |
| q-72453 | selection | 3 | `y =-3x + 6` | -m | absent ref |
| q-72453 | selection | 4 | `y = \frac{1}{3}x + 6` | 1/m | absent ref |
| q-72453 | selection | 5 | `y =-\frac{1}{3}x + 6` | -1/m | derived correct |
| q-72525 | selection | 1 | `y = 2x + 4` | 1/m | absent ref |
| q-72525 | selection | 2 | `y =-\frac{x}{2} - \frac{1}{3}` | -m | absent ref |
| q-72525 | selection | 3 | `y = \frac{x}{2} + \frac{1}{3}` | m | absent ref |
| q-72525 | selection | 4 | `y = x + 1` | 1 | absent ref |
| q-72525 | selection | 5 | `y =-2x + 3` | -1/m | derived correct |
| q-215888 | selection | 1 | `y=-x-5` | m | wrong |
| q-215888 | selection | 2 | `y=\frac{1}{2}x+1` | -m/2 | wrong |
| q-215888 | selection | 3 | `y=\frac{1}{2}x-1` | -m/2 | wrong |
| q-215888 | selection | 4 | `y=x+3` | -1/m | correct |
| q-215888 | selection | 5 | `y=-x+5` | m | wrong |
| q-215890 | selection | 1 | `y=x-2` | m | wrong |
| q-215890 | selection | 2 | `y=-x+9` | -1/m | correct |
| q-215890 | selection | 3 | `y=2x+1` | 2m | wrong |
| q-215890 | selection | 4 | `y=-2x+1` | -2m | wrong |
| q-215890 | selection | 5 | `y=x-\frac{1}{2}` | m | wrong |
| q-72524 | selection | 1 | `y=x` | 1 | wrong |
| q-72524 | selection | 2 | `y=-2x-3` | 1/m | wrong |
| q-72524 | selection | 3 | `y=-\frac{x}{2}x+5` | quadratic_m | malformed nonline |
| q-72524 | selection | 4 | `y=-\frac{x}{2}x-1` | quadratic_m | malformed nonline |
| q-72524 | selection | 5 | `y=2x+19` | -1/m | correct |
| q-72527 | selection | 1 | `y=\frac{1}{4}x-6` | -1/m | correct |
| q-72527 | selection | 2 | `y=-4x-1` | m | wrong |
| q-72527 | selection | 3 | `y=-\frac{1}{4}` | horizontal | wrong |
| q-72527 | selection | 4 | `y=-\frac{1}{4}x+6` | 1/m | wrong |
| q-72527 | selection | 5 | `y=4x-1` | -m | wrong |
| q-72528 | selection | 1 | `y=-5x+\frac{1}{2}` | m | wrong |
| q-72528 | selection | 2 | `y=\frac{1}{5}x-8` | -1/m | correct |
| q-72528 | selection | 3 | `y=-\frac{1}{5}x+4` | 1/m | wrong |
| q-72528 | selection | 4 | `y=5x+2` | -m | wrong |
| q-72528 | selection | 5 | `y=\frac{1}{2}` | horizontal | wrong |

Explicit profiles preserve the complete source bank, count, spacing, x-in-fraction versus coefficient-in-fraction notation, and all independently supplied intercepts. The sign/reciprocal operations suggest familiar coefficient mistakes, but historical misconception intent is not recoverable solely from these values. The unit profiles' half/double slopes in particular are retained structural recipes, not promoted to universal source-derived error models. No learner-facing distractor diagnosis is added.

## Stage 4: reusable templates and authored extensions

Prompt slots are complete line components, not string replacements:

- Compact: `Which of the following lines is perpendicular to ${target-line}?$`
- Spaced: `Which of the following lines is perpendicular to ${target-line}$?`

Fixed solution sentences reproduce the observed criterion, identification of each slope, multiplication introduction, and conclusion. Variable slots contain a complete target equation, complete correct equation, m, -1/m, and the unreduced two-factor product. Only the observed ±1 negative factor is parenthesized; no mathematical stage is collapsed or inserted. At source parameters all five observed solutions match exactly, including sentence wording, blank-line sequence, and product notation. Both missing solutions use an explicitly authored reconstruction of these stages and are excluded from the exact-solution denominator.

Normal defaults use the complete authored bank `[m,-m,1/m,-1/m,0]`, independently displaying five intercepts. These wrong coefficients correspond to retaining the original slope, changing its sign only, reversing it without changing sign, and dropping the x term to obtain a horizontal line of slope zero. They derive from the assessed coefficient/negative-reciprocal method. The whole bank is chosen before any member is calculated. Non-unit m guarantees one perpendicular coefficient; full-equation collisions and multiple correct objects reject the entire instance. There is no first-valid distractor pooling or arbitrary numerical perturbation. The minimal q-72524 repair is an independent profile, never reported as a raw source match.

Normal slope domains: easy ±n for n=2..12; moderate ±1/n for n=2..12; hard ±p/q with coprime p,q=2..9. Hard has no observed difficulty label: its fixed one-rational-coefficient workload is supported by canonical -2/5 and the prerequisite, with the explicit same-KP boundaries explained in classification.md. Intercepts are bounded exact rationals for observed replay and bounded integers for authored defaults; neither changes the assessed mathematical task. Explicit input guards enforce these same slope bounds, including negative magnitudes.

Content identity includes generator version, level, template, profile, canonical parameters, displayed prompt, complete fixed solution, and sorted full answer bank. Option order and seed are excluded. The mathematical task identity is reduced target slope alone; intercept and bank changes never inflate the count. Field and answer UUIDs are owned by the content-specific question/field. All source cases pass through `generate` and the same arithmetic/slot rendering used for changed parameters.

Plot specification: none. Step 5 and step 7 need no renderer or assets because this KP's source assessment contains no plots.
