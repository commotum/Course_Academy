# Template extraction — 17592186100890

This follows the four-stage procedure in Step 4. Exact source records are in [source.json](source.json), with specific descriptions and component inventories in [extraction.json](extraction.json).

[Choice-bank extraction](choice-bank-extraction.md) accounts for every original distractor before generalizing, including compound scale/offset changes and altered constants. Its 14 complete bank profiles are independent of the 13 prompt/field/solution templates. The [option ledger](choice-extraction.json) maps all 76 source answer values to their formulas or canonical answer and replay results; [full-bank replay](source-bank-fidelity.json) verifies all 56 distractors and every correct designation.

## 1. Specific source descriptions

| Source | Template | Specific description |
|---|---|---|
| q-15751 | `ellipse_sin_radio` | x=2\sin t-1; y=5\cos t+4; full-period interval; radio, equation answer, 5 stored math values; integer shifts and positive scales; squared-coordinate identity; no plots or option feedback. |
| q-102680 | `ellipse_sin_radio` | x=\sin t; y=\cos t-5; full-period interval; radio, equation answer, 5 stored math values; integer shifts and positive scales; squared-coordinate identity; no plots or option feedback. |
| q-102682 | `ellipse_sin_radio` | x=5\sin t+3; y=3\cos t-2; full-period interval; radio, equation answer, 5 stored math values; integer shifts and positive scales; squared-coordinate identity; no plots or option feedback. |
| q-15657 | `ellipse_sin_radio` | x=\sin t-3; y=\cos t; full-period interval; radio, equation answer, 5 stored math values; integer shifts and positive scales; squared-coordinate identity; no plots or option feedback. |
| q-15752 | `ellipse_cos_radio` | x=2\cos t; y=3\sin t; full-period interval; radio, equation answer, 5 stored math values; integer shifts and positive scales; squared-coordinate identity; no plots or option feedback. |
| q-15679 | `ellipse_cos_radio` | x=\cos t-2; y=\sin t+3; full-period interval; radio, equation answer, 5 stored math values; integer shifts and positive scales; squared-coordinate identity; no plots or option feedback. |
| q-320946 | `ellipse_sin_blank` | x=3\sin t; y=\cos t-2; full-period interval; blank, lhs answer, 1 stored math values; integer shifts and positive scales; squared-coordinate identity; no plots or option feedback. |
| q-319828 | `ellipse_cos_blank` | x=2\cos t; y=\sin t+4; full-period interval; blank, lhs answer, 1 stored math values; integer shifts and positive scales; squared-coordinate identity; no plots or option feedback. |
| q-102677 | `tan_sec_radio` | x=2\tan t; y=\sec t; open first-quadrant interval; radio, equation answer, 5 stored math values; positive integer scales; squared-coordinate identity; no plots or option feedback. |
| q-15761 | `cot_csc_radio` | x=3\cot t; y=\csc t; open first-quadrant interval; radio, equation answer, 5 stored math values; positive integer scales; squared-coordinate identity; no plots or option feedback. |
| q-321400 | `cot_csc_blank` | x=3\cot t; y=2\csc t; open first-quadrant interval; blank, rhs answer, 1 stored math values; positive integer scales; root/quotient composition; positive branch; no plots or option feedback. |
| q-102687 | `cos_tan_radio` | x=\cos t; y=\tan t; open first-quadrant interval; radio, equation answer, 5 stored math values; positive integer scales; root/quotient composition; positive branch; no plots or option feedback. |
| q-15759 | `sin_tan_radio` | x=\sin t; y=\tan t; open first-quadrant interval; radio, equation answer, 5 stored math values; positive integer scales; root/quotient composition; positive branch; no plots or option feedback. |
| q-24378 | `sin_double_factored_radio` | x=2\sin t; y=3\cos 2t; full-period interval; radio, equation answer, 5 stored math values; integer signed scales; double-angle operator followed by quadratic polynomial; no plots or option feedback. |
| q-24576 | `sin_double_expanded_radio` | x=6\sin t; y=-5\cos 2t; full-period interval; radio, equation answer, 5 stored math values; integer signed scales; double-angle operator followed by quadratic polynomial; no plots or option feedback. |
| q-24574 | `cos_double_radio` | x=4\cos t; y=2\cos 2t; full-period interval; radio, equation answer, 5 stored math values; integer signed scales; double-angle operator followed by quadratic polynomial; no plots or option feedback. |
| q-24575 | `cos_double_radio` | x=-3\cos t; y=4\cos 2t; full-period interval; radio, equation answer, 5 stored math values; integer signed scales; double-angle operator followed by quadratic polynomial; no plots or option feedback. |
| q-321314 | `cos_double_blank` | x=5\cos t; y=-6\cos 2t; full-period interval; blank, rhs answer, 1 stored math values; integer signed scales; double-angle operator followed by quadratic polynomial; no plots or option feedback. |
| q-321315 | `cos_double_blank` | x=-4\cos t; y=3\cos 2t; full-period interval; blank, rhs answer, 1 stored math values; integer signed scales; double-angle operator followed by quadratic polynomial; no plots or option feedback. |
| q-321318 | `cos_double_blank` | x=6\cos t; y=5\cos 2t; full-period interval; blank, rhs answer, 1 stored math values; integer signed scales; double-angle operator followed by quadratic polynomial; no plots or option feedback. |

## 2–4. Generalization and reusable components

### ellipse_sin_radio

Isolate same-angle sine/cosine and substitute into sin²+cos²=1, with sine/x first.

Sources: q-15751, q-102680, q-102682, q-15657. Expected value: equation. Plot rating: none.

Observed parameters: `[{"a": 2, "b": 5, "h": -1, "k": 4}, {"a": 1, "b": 1, "h": 0, "k": -5}, {"a": 5, "b": 3, "h": 3, "k": -2}, {"a": 1, "b": 1, "h": -3, "k": 0}]`.

Ordered fixed prose patterns from its representative source:

- First, let's make the trigonometric functions the subject of each equation:
- Using the Pythagorean identity {{math}}, we get
- So the Cartesian equation of the given curve is {{math}}

Per-source mathematical blocks, choice values, placeholders, and conditional prose variants are retained in extraction.json. Derived scales, coefficient squares, branch signs, and final expressions come from one shared mathematical instance.

### ellipse_cos_radio

Isolate same-angle cosine/sine and substitute into sin²+cos²=1, with sine/y first.

Sources: q-15752, q-15679. Expected value: equation. Plot rating: none.

Observed parameters: `[{"a": 2, "b": 3, "h": 0, "k": 0}, {"a": 1, "b": 1, "h": -2, "k": 3}]`.

Ordered fixed prose patterns from its representative source:

- First, let's make the trigonometric functions the subject of each equation:
- Using the Pythagorean identity {{math}} we get
- So the Cartesian equation of the given curve is {{math}}

Per-source mathematical blocks, choice values, placeholders, and conditional prose variants are retained in extraction.json. Derived scales, coefficient squares, branch signs, and final expressions come from one shared mathematical instance.

### ellipse_sin_blank

Isolate same-angle sine/cosine and substitute into sin²+cos²=1, with sine/x first.

Sources: q-320946. Expected value: lhs. Plot rating: none.

Observed parameters: `[{"a": 3, "b": 1, "h": 0, "k": -2}]`.

Ordered fixed prose patterns from its representative source:

- First, let's make the trigonometric functions the subject of each equation:
- Using the Pythagorean identity {{math}}, we get

Per-source mathematical blocks, choice values, placeholders, and conditional prose variants are retained in extraction.json. Derived scales, coefficient squares, branch signs, and final expressions come from one shared mathematical instance.

### ellipse_cos_blank

Isolate same-angle cosine/sine and substitute into sin²+cos²=1, with sine/y first.

Sources: q-319828. Expected value: lhs. Plot rating: none.

Observed parameters: `[{"a": 2, "b": 1, "h": 0, "k": 4}]`.

Ordered fixed prose patterns from its representative source:

- First, let's make the trigonometric functions the subject of each equation:
- Using the Pythagorean identity {{math}}, we get

Per-source mathematical blocks, choice values, placeholders, and conditional prose variants are retained in extraction.json. Derived scales, coefficient squares, branch signs, and final expressions come from one shared mathematical instance.

### tan_sec_radio

Derive tan²+1=sec² by dividing the Pythagorean identity by cos², then substitute.

Sources: q-102677. Expected value: equation. Plot rating: none.

Observed parameters: `[{"a": 2, "b": 1}]`.

Ordered fixed prose patterns from its representative source:

- First, let's make the trigonometric functions the subject of each equation:
- Dividing the Pythagorean identity {{math}} by {{math}}, we get
- Substituting {{math}} and {{math}} into this formula, we get
- So the Cartesian equation of the given curve is {{math}}

Per-source mathematical blocks, choice values, placeholders, and conditional prose variants are retained in extraction.json. Derived scales, coefficient squares, branch signs, and final expressions come from one shared mathematical instance.

### cot_csc_radio

Radio: derive 1+cot²=csc² by division; blank: use it directly and select the positive root.

Sources: q-15761. Expected value: equation. Plot rating: none.

Observed parameters: `[{"a": 3, "b": 1}]`.

Ordered fixed prose patterns from its representative source:

- First, let's make the trigonometric functions the subject of each equation:
- Dividing the Pythagorean identity {{math}} by {{math}}, we get
- Substituting {{math}} and {{math}} into this formula, we get
- So the Cartesian equation of the given curve is {{math}}

Per-source mathematical blocks, choice values, placeholders, and conditional prose variants are retained in extraction.json. Derived scales, coefficient squares, branch signs, and final expressions come from one shared mathematical instance.

### cot_csc_blank

Radio: derive 1+cot²=csc² by division; blank: use it directly and select the positive root.

Sources: q-321400. Expected value: rhs. Plot rating: none.

Observed parameters: `[{"a": 3, "b": 2}]`.

Ordered fixed prose patterns from its representative source:

- First, let's make the trigonometric functions the subject of each equation:
- Using the Pythagorean identity {{math}}, we get
- We used here that {{math}} and {{math}} in the range {{math}}  Now, solving for {{math}}, we obtain
- So, the Cartesian equation of the given curve is  {{math}}

Per-source mathematical blocks, choice values, placeholders, and conditional prose variants are retained in extraction.json. Derived scales, coefficient squares, branch signs, and final expressions come from one shared mathematical instance.

### cos_tan_radio

Recover positive sine from cosine, then divide sine by cosine to form tangent.

Sources: q-102687. Expected value: equation. Plot rating: none.

Observed parameters: `[{"a": 1, "b": 1}]`.

Ordered fixed prose patterns from its representative source:

- First, let's make the trigonometric functions the subject of each equation:
- Using the Pythagorean identity {{math}}, we get
- We used here that {{math}} in the range {{math}}  Now, using the definition of a tangent, we obtain
- Substituting {{math}} and {{math}} into this formula, we get
- So the Cartesian equation of the given curve is {{math}}

Per-source mathematical blocks, choice values, placeholders, and conditional prose variants are retained in extraction.json. Derived scales, coefficient squares, branch signs, and final expressions come from one shared mathematical instance.

### sin_tan_radio

Recover positive cosine from sine, then divide sine by cosine to form tangent.

Sources: q-15759. Expected value: equation. Plot rating: none.

Observed parameters: `[{"a": 1, "b": 1}]`.

Ordered fixed prose patterns from its representative source:

- First, let's make the trigonometric functions the subject of each equation:
- Using the Pythagorean identity {{math}}, we get
- We used here that {{math}} in the range {{math}}  Now, using the definition of a tangent, we obtain
- Substituting {{math}} and {{math}} into this formula, we get
- So the Cartesian equation of the given curve is {{math}}

Per-source mathematical blocks, choice values, placeholders, and conditional prose variants are retained in extraction.json. Derived scales, coefficient squares, branch signs, and final expressions come from one shared mathematical instance.

### sin_double_factored_radio

Derive cos(2t)=1−2sin²(t), substitute scales, and leave positive-y-scale answer factored.

Sources: q-24378. Expected value: equation. Plot rating: none.

Observed parameters: `[{"a": 2, "b": 3}]`.

Ordered fixed prose patterns from its representative source:

- First, let's make the trigonometric functions the subject of each equation:
- Now, using double angle formula for cosine and the Pythagorean identity, we obtain
- Substituting {{math}} and {{math}} into this formula, we get
- So the Cartesian equation of the given curve is {{math}}

Per-source mathematical blocks, choice values, placeholders, and conditional prose variants are retained in extraction.json. Derived scales, coefficient squares, branch signs, and final expressions come from one shared mathematical instance.

### sin_double_expanded_radio

Use the same sine identity, but preserve the negative-y-scale constant-first expanded radio answer.

Sources: q-24576. Expected value: equation. Plot rating: none.

Observed parameters: `[{"a": 6, "b": -5}]`.

Ordered fixed prose patterns from its representative source:

- First, let's make the trigonometric functions the subject of each equation:
- Now, using double angle formula for cosine and the Pythagorean identity, we obtain
- Substituting {{math}} and {{math}} into this formula, we get
- So the Cartesian equation of the given curve is {{math}}

Per-source mathematical blocks, choice values, placeholders, and conditional prose variants are retained in extraction.json. Derived scales, coefficient squares, branch signs, and final expressions come from one shared mathematical instance.

### cos_double_radio

Derive cos(2t)=2cos²(t)−1; radios retain a factored answer, blanks add expansion and expect RHS only.

Sources: q-24574, q-24575. Expected value: equation. Plot rating: none.

Observed parameters: `[{"a": 4, "b": 2}, {"a": -3, "b": 4}]`.

Ordered fixed prose patterns from its representative source:

- First, let's make the trigonometric functions the subject of each equation:
- Now, using double angle formula for cosine and the Pythagorean identity, we obtain
- Substituting {{math}} and {{math}} into this formula, we get
- So the Cartesian equation of the given curve is {{math}}

Per-source mathematical blocks, choice values, placeholders, and conditional prose variants are retained in extraction.json. Derived scales, coefficient squares, branch signs, and final expressions come from one shared mathematical instance.

### cos_double_blank

Derive cos(2t)=2cos²(t)−1; radios retain a factored answer, blanks add expansion and expect RHS only.

Sources: q-321314, q-321315, q-321318. Expected value: rhs. Plot rating: none.

Observed parameters: `[{"a": 5, "b": -6}, {"a": -4, "b": 3}, {"a": 6, "b": 5}]`.

Ordered fixed prose patterns from its representative source:

- First, let's make the trigonometric functions the subject of each equation:
- Now, using the double-angle formula for cosine and the Pythagorean identity, we obtain
- Substituting {{math}} and {{math}} into this formula, we get
- So, the Cartesian equation of the given curve is {{math}}

Per-source mathematical blocks, choice values, placeholders, and conditional prose variants are retained in extraction.json. Derived scales, coefficient squares, branch signs, and final expressions come from one shared mathematical instance.

## Boundaries and corrections

Ellipse blanks keep x scaling, no x shift, a unit y scale, and a y shift. Hyperbola radio variants keep unit y scale. First-quadrant functions require the positive branch. Hard sine factored radios use positive y scales; hard sine expanded radios use negative y scales. Hard cosine radios use positive y scales and signed x scales; typed RHS variants may use signed scales.

Moderate source coefficients are all one. The generator now samples positive scales 1–4 by default, retaining unit inputs for source replay and identifying coefficient variation in author metadata. There is no separate unit-only or scaling mode. Numeric sampling bounds are draft policies within the extracted structures.

Domain and branch restrictions are retained separately from source-style worked solutions and shown as author metadata in previews. The canonical example e-5101 states x≥1 despite an open first-quadrant interval; the supported restriction is x>1 and y>0. Its original text is preserved as evidence.

Named distractor recipes are hypotheses. Some original sin/tan options are non-real on the correct domain; their shapes are preserved without invented learner feedback. All generated radio options must be distinct and demonstrably incorrect.

The signed cosine double-angle sources q-24575, q-321314, and q-321315 omit the unsimplified-square row that appears in the positive-scale sources q-24574 and q-321318. This is an optional layout component, not a different mathematical method. The draft uses the compact sequence when either scale is negative; this condition is inferred from the observed examples, not required by the mathematics.

## Approved moderate extensions — draft 4

The captured source descriptions above remain unchanged. [Moderate variations](moderate-variations.md) specifies the four-stage extraction for authored cotangent counterparts, quadrant variation, and correct-answer-derived banks. The existing sine/tangent and cosine/tangent templates share those quadrant/scale variations. Moderate fields remain radio and the solution retains the source stages and fixed sentences, adapting the function name and branch sign.

Normal moderate sampling selects the family and single-quadrant interval without an instructional sequence. Each family uses its complete authored bank. The captured banks remain available by explicit profile for original source replay; no original distractor is replaced in that fidelity check. Source references distinguish examples from method references for authored extensions.
