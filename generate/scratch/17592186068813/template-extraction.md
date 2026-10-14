# Four-stage template extraction

## 1. Specific observations

q-16506 supplies 1/(2x), uses a 1/2 contraction and banks negative base, negative half, base, double and half graphs. q-97952 supplies 2/x and banks negative base, half, base, negative double and double. q-113324 supplies 5/x and banks ±5/x, 1/x, 10/x and (1/5)/x; its base solution raster differs in coordinate scale from the 1/x distractor. q-99064 supplies 3/(2x) and banks ±(1/2)/x, 3/x and ±(3/2)/x; its older-widget correct ref is missing, and its later duplicate widget has the correct ref. q-113328 supplies 5/(3x) and banks 1/x, (3/5)/x, -(5/3)/x, -(3/5)/x and (5/3)/x. All five raw sources are rated; four have one radio selection field and q-99064 has two duplicate selection fields, each with five image choices; all answer types are image. All source prompts, complete prose, punctuation, two graph placements and attribute-presence contracts are reproduced through parameterized public raw profiles.

## 2. Shared pattern

Select the graph of a positive multiple of the reciprocal function. Determine the vertical scale n/d, keep x fixed and multiply reciprocal ordinates by n/d. Axes remain the two asymptotes. The fixed worked solution has exactly one base-curve stage and one scale-factor stage, with no response-dependent diagnosis.

## 3. Complete components and banks

Write a=n/d. Lists below preserve source choice order; detailed raster references and per-image coordinate calibration are in plot-spec.json, and source.json retains UUIDs and all raw attributes.

| Source/public profile | n,d | Full ordered coefficient bank | Correct source designation |
|---|---|---|---|
| raw_q-16506 | 1,2 | -1, -a, 1, 1/a, a | last |
| raw_q-99064 | 3,2 | -1/d, 1/d, n, a, -a | absent; +a independently inferred |
| raw_q-113328 | 5,3 | 1, 1/a, -a, -1/a, a | last |
| raw_q-97952 | 2,1 | -1, 1/a, 1, -a, a | last |
| raw_q-113324 | 5,1 | a, -a, 1, 2a, 1/a | first |

These recipes recover every plotted mathematical object. Mistake intent is inferred, not recovered code: sign reflection, scale omission, inverted scale, numerator-only scale and denominator-only scale are defensible operations in the assessed method. The original 10/x can be represented by doubling the scale; the source does not establish why it was chosen, so doubling is documented as an observed expression pattern. Exact anchor raster reuse preserves differing per-option scales and decimal/fraction coordinate spellings. No lookup branch returns source payload; the same prompt/solution mask and algebraic recipes run at original and changed inputs, with anchor asset reuse only when complete geometry matches.

Normal eligible profiles are selected whole before parameters. integer_reversal uses the q-97952 complete bank and unit_numerator_reversal uses the q-16506 complete bank. The q-113324 doubling pattern remains in its public observed replay profile; it is not promoted to the default integer bank because the source does not establish the doubled-scale error intent. rational_denominator and rational_reversal use the two corresponding observed moderate complete banks. Hard authored nonunit_point_reversal banks [a,-a,1/a,1,n]; nonunit_point_denominator banks [a,-a,1/d,n,-1/a]. Hard errors use reflected stretch, unchanged curve, ratio reversal and omitted numerator/denominator, all at the same nonunit reference points. No post-sampling option replacement or first-valid recipe pool occurs.

## 4. Backbone and slots

Prompt mask: `Which of the following is the graph of $y=\frac{n}{dx}?$`, omitting d when d=1.

Whole solution mask: `To plot $y=EXPRESSION,$ we apply the following steps:`; base bullet `Take the curve $y=\frac{1}{x}.$`; base image; stretch bullet `Stretch the result by a scale factor of $SCALE$ parallel to the $y$-axis to get the graph of $y=EXPRESSION.$`; correct graph image. EXPRESSION is a complete fraction component and SCALE is its exact n/d. Parameterization replaces every occurrence, including the conclusion and both images. No feedback is introduced.

Easy integer n=2–12,d=1 or n=1,d=2–12. Moderate primitive n=2–24,d=2–5, 1/3≤n/d≤4. Hard primitive n=2–24,d=6–12, same ratio bounds, marked x=±2 rather than ±1. Explicit inputs obey these bounds, coprimality and whole-bank inequality. Numeric n,d affect the actual assessed stretch; aliases and seeds do not. Canonical task fingerprints use reduced n/d and the assessed marked abscissa, excluding profile/bank, paths, seed, order and difficulty-label aliases. Content identity includes actual complete prompt, solution, bank, difficulty and correct-ref presence.

Slot coverage is exhausted mathematically: 22 easy, 32 moderate and 85 hard meaningful tasks. All default eligible banks appear in deterministic seed coverage. Five original correct designations match; one older-widget omission remains absent in raw evidence, while normal output uses the later complete widget.

Parent review: `raw_q-113324` is evidence-only and ineligible for learning because its doubled-scale distractor intent is opaque; the complete literal bank and correct designation remain preserved. Normal integer defaults use the defensible q-97952 reversal bank.

Parent source-field audit correction: frozen q-99064 contains two identical selection banks, an older widget without a correct designation and a later widget with the +3/2 designation. Raw replay preserves both widgets and their different designation presence; normal generation uses one complete authoritative widget. Total raw fidelity is six banks, 30 options, five existing designations, and one absent designation across five questions. Earlier first-widget-only counts were incomplete.
