# Template extraction

## 1. Describe every source before generalizing

All prompts consist of a circle raster followed by “Find … for the circle shown above.” q-127359 and q-127360 use `\frac{dy}{dx}`; the five rated questions use `\frac{\text{d}y}{\text{d}x}`. Sources contain no point-evaluation request, extra tangent construction, response feedback, or domain instruction. Correct answers are complete scalar derivative formulas without math delimiters.

| Source | Center | Radius | Number form and equation workload | Bank profile | Ordered solution |
|---|---|---|---|---|---|
| q-127359 | (0,0) | 2 | integer axial intercept labels | q-127359 | absent |
| q-127360 | (1,−1) | 3 | two unit signed shifts | q-127360 | absent |
| q-127493 | (0,0) | 4 | integer axial intercept labels; x²+y²=16 | q-127493 | equation + 5 derivative rows |
| q-127497 | (1,0) | 2 | one positive shift; (x−1)²+y²=4 | q-127497 | equation + 5 rows; numerator 1−x |
| q-127499 | (−1,1) | 1 | two signed shifts; (x+1)²+(y−1)²=1 | q-127499 | equation + 6 rows; last denominator 1−y |
| q-127500 | (−3,−2) | 2 | two negative shifts; (x+3)²+(y+2)²=4 | q-127500 | equation + 5 rows |
| q-127502 | (0,−2) | 3 | one negative shift; x²+(y+2)²=9 | q-127502 | equation + 5 rows |

Raw MA widgets q-127359 and q-127360 confirm multiple-choice layout, five options, and the same complete banks. They provide no authoritative correct designation. Independent differentiation gives −x/y and −(x−1)/(y+1), respectively; these are inferred keys. No doubled-backslash repair exists: all 35 decoded options have zero adjacent-backslash pairs, verified via byte counts. JSON escaping must not be confused with actual string bytes.

## 2. Generalized pattern

Read a circle centered at (h,k) with radius r>0. Write `(x−h)²+(y−k)²=r²`; differentiate both sides with respect to x, retaining the y chain factor. Isolate `dy/dx=−(x−h)/(y−k)`. The finite-slope formula applies on the circle away from y=k. Radius determines the actual locus and equation arithmetic but cancels from the derivative formula.

## 3. Map the complete banks and components

Let U=x−h, V=y−k, U+=x+h, V+=y+k. The following is a complete ordered source-option mapping, before normal deterministic shuffling. Each line is an algebraic parameterized expression pattern, not an inferred source-authoring algorithm. Original braces, whitespace, signs and final sign-rewritten answers are retained by each recipe's renderer. Every recipe is independently compared as a complete value at its original parameters.

| Profile | Option 1 | Option 2 | Option 3 | Option 4 | Option 5 | Correct original option |
|---|---|---|---|---|---|---|
| q-127359 | −x²/y² | −y/x | −x/y | x/y | yx² | 3 inferred |
| q-127360 | −V+/U+ | −U+/V+ | V+/U+ | −U/V | U+/V | 4 inferred |
| q-127493 | 2x/y | −rx/y | y/x | −x/y | −x²/y | 4 |
| q-127497 | (h−x)y | −U+/y | (h−x)/y | −U+y | U+/y | 3 |
| q-127499 | 2UV+ | (−h−x)/V+ | U/(k−y) | 2U/V | U(k−y) | 3 |
| q-127500 | V/U | −U/V | 2U+/V+ | V/U+ | −2V/U | 2 |
| q-127502 | y/(x−k) | −V/x | −(x−k)/(ry) | −x/V | (x−r)/V | 4 |

Sign reversal, reciprocal, failed square differentiation, and multiplication versus division are plausible interpretations of some options. The radius coefficients and unrelated-looking shift combinations in q-127493/q-127502 are underdetermined. Their parameterized observed patterns are retained only as explicit `evidence_only=true`, `eligible_for_learning=false` profiles. Source equality does not justify using opaque historical recipes as defaults.

Complete-bank comparisons use an exact expression coefficient domain that includes allowed radical coefficients appearing in options, even when the circle polynomial contains only the rational radius square. In particular q-127493 with radius √2 or √5 retains its parameterized −rx/y distractor and passes whole-bank uniqueness on the actual circle. These remain evidence-only profiles with unresolved error intent.

Normal authored output selects the complete `method` bank before sampling: correct −U/V; lost rearrangement minus U/V; reciprocal −V/U; omitted y power-rule factor −2U/V; omitted x power-rule factor −U/(2V). The complete bank is derived from printed operations. A collision under the circle relation rejects the whole instance; there is no pooled distractor replacement. No learner-facing error diagnosis is added.

Fixed prose and solution masks: “Since our circle is centered at … and has a radius of …, its equation is given by” → unsimplified center/radius equation → simplified circle equation → “Now, to calculate …, we use implicit differentiation:” → formal whole-equation derivative → distinct term derivatives → chain factors → rearrangement → division. q-127499 appends the observed sign-rewriting row; q-127497 preserves `h−x` numerator. Origin wording is conditional. Raw unrated solutions remain absent. Parameterized recipes reproduce all five ordered source solutions byte-for-byte at original values.

## 4. Reusable templates, domains and constraints

Slots are complete center coordinates, radius, affine terms, square terms, radius square, and derivative expressions. No blind short-expression replacement is used. Positive, negative, zero and half-integer shifts pass through explicit sign-aware masks. Formal derivative rows and all later rows are checked from actual displayed TeX, including their operands, chain factors and ordered structure.

Normal easy: h=k=0; r in {1,2,3,4,5,6,√2,√5}. The two familiar radicals are supported by the introduction's √5 radius and the circle-equation prerequisite. Moderate: integer h,k in [−4,4], not both zero; integer r in [1,4]. These enlarge the observed signed small-integer center forms without a new operation. Hard: h,k independently in {±1/2,±3/2,±5/2,±7/2}; r in {1,3/2,2,5/2,3,7/2,4}. Hard requires both nonzero nonintegral coordinates even for explicit inputs. No ellipse, parabola, slope evaluation, second derivative, or tangent-line branch is added.

Observed-profile replay applies the same finite easy or moderate arithmetic domains above, together with zero-shift restrictions matching the bank's structure, positive radius, and the full-bank collision guard. Origin evidence radii must belong to EASY_RADII; shifted evidence centers must be integers in [−4,4] and their radii integers in [1,4]. Arbitrary real centers, unsupported radicals, transcendental values, and large-denominator fractions are rejected before plot rendering. Source profiles preserve rated attribute presence and enforce the documented source level; normal learning uses method-bank level guards.

Meaningful finite counts: easy 8 circle loci and 1 derivative formula; moderate 80 centers ×4 radii =320 loci and 80 derivative formulas; hard 64 centers ×7 radii =448 loci and 64 derivative formulas. The locus fingerprint includes radius because the diagram and recovered equation are assessed. The derivative fingerprint excludes radius. Option shuffles, profile names and notation aliases never count as new mathematical tasks. Easy's derivative structure is inherently narrow; no fictitious new easy method is claimed.
