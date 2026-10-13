# Template extraction — reciprocal antiderivatives

## 1. Specific source descriptions

q-29987 gives `f(x)=x^{-2/3}`, `F′(x)=f(x)`, asks for F(x), and has five math-valued radio choices. No rating, key or solution is captured. q-29989 uses the same old spaced prompt structure but writes `1/x^{3/5}`, with a different complete bank; it also lacks rating/key/solution.

q-71100 (easy) gives `{x}^{-1/7}` in a newer named-function prompt. Its source solution first integrates F′=f in a three-row aligned block, then uses n=-1/7 in five ordered rows: F integral; negative-power integrand; unsimplified `(n+1)` power-rule quotient; evaluated exponent/divisor; collected coefficient-times-power plus C. Fields are absent.

q-113705 (moderate) gives `1/{x}^{4/3}`. It has the same three-row named-function opening, a reciprocal-to-negative-power note, then six ordered rows: integral of f; negative-power integral; unsimplified rule; evaluated quotient; negative-power product; reciprocal final form. Fields are absent.

q-29633 (moderate) directly asks the antiderivative of `1/{x}^{4}`. The note converts to x^-4, followed by four rows: reciprocal integral equals negative-power integral; unsimplified power rule; negative quotient over 3; final reciprocal. No named-function opening or answer fields.

q-29662 (moderate) asks the integral of `1/sqrt({x}^{5})`. A three-member equality chain converts reciprocal square root to reciprocal rational power and negative rational power. Four aligned rows show converted integral, unsimplified rule, coefficient-times-negative-power and final reciprocal. The source first left integral omits dx. Fields absent.

All variables are x; F is a primitive and f is its derivative. Every integral has one unit power, no sums/multiples/initial conditions. Exact arithmetic and arbitrary +C are essential. A positive real connected domain x>0 supports every displayed rational/root identity without branch ambiguity. The formula excludes n=-1.

## 2. Generalized pattern

For primitive positive integers p,q with p/q≠1, write the unit reciprocal integrand as x^n with n=-p/q. Then integrate to x^(n+1)/(n+1)+C and, where n+1<0, restore reciprocal notation. Easy already prints the negative power; moderate rewrites a reciprocal power or reciprocal square root; authored hard rewrites a reciprocal higher root. Preserve each source prompt and arithmetic stage sequence through complete masks.

## 3. Component and complete-bank mapping

Let `n=-p/q`, `m=n+1`. Every source choice has type `:answer.type/math`, field key `selection`, field type `:answer-field.type/radio`; all choices include +C. Source choices below are listed in EDB capture order. Their source answer IDs and database IDs are preserved in `source.json`.

| Profile | Original exact choice | Parameterized coefficient a | Exponent e | Interpretation status |
|---|---|---|---|---|
| q-29987 | x^{2/3}+C | 1 | -n | omit coefficient/reverse input exponent; inferred |
| q-29987 | 5x^{-1/3}+C | p+q | -m | opaque expression-shape generalization; intent unknown |
| q-29987 | -(1/3)x^{5/3}+C | -m | 1-n | opaque compound coefficient/exponent; intent unknown |
| q-29987 | 3x^{1/3}+C | 1/m | m | independently derived correct family |
| q-29987 | (1/3)x^{-1/3}+C | m | -m | multiply by result exponent and reverse it; inferred |
| q-29989 | -(3/5)x^{3/2}+C | n | p/(q-p) | opaque compound input/result-part operation; intent unknown |
| q-29989 | -x^{2/5}+C | -1 | m | negate unit coefficient; inferred |
| q-29989 | (2/5)x^{5/2}+C | m | 1/m | multiply by result power/invert exponent; inferred |
| q-29989 | (2/5)x^{2/5}+C | m | m | multiply instead of divide by result exponent; inferred |
| q-29989 | (5/2)x^{2/5}+C | 1/m | m | independently derived correct family |

Both observed banks are complete five-choice profiles. No recipe pooling or first-valid option replacement occurs. Formulas reproduce all ten original exact rendered values; p/q reduction, source counts, and designations are separately checked. The source has **zero observed keys**, so correctness does not imply designation fidelity. Neither old radio has a worked solution; its completed solution is explicitly authored from the newer shared opening and power-rule sequence.

Source components are stored in `source-cases.json` and the six template definitions. Each prompt's reciprocal/root/negative power is a complete slot. Each solution row is built structurally: input exponent n, unsimplified n+1 in numerator/divisor, evaluated m, coefficient 1/m, and reciprocal form. Do not let eager simplification erase the unsimplified row. The named-function three-row block and instructional sentences are shared constants. Absent keys are omitted in raw mode. q-29662's omitted first differential is conditional only on raw replay, not inherited by normal records.

## 4. Reusable templates, constraints and extensions

The script's `prompt`, `integrand`, `solution`, `bank`, `domain` and `validate_parameters` functions implement full component masks and exact rational arithmetic. Original parameters: `(2,3)`, `(3,5)`, `(1,7)`, `(4,3)`, `(4,1)`, `(5,2)` for the corresponding sources. Every raw case passes through `generate(level, template=..., parameters=..., profile=raw_...)`; no source JSON is returned by a special branch or used as an answer lookup table.

Default banks are **authored**, selected whole before sampling. Five recipes are: correct `x^m/m`; input exponent as coefficient `n*x^m`; omit increment `x^n/m`; differentiate instead `n*x^(n-1)`; reverse sign `-x^m/m`, always plus C. Each full instance rejects any pair with equal derivatives or a nonunique correct derivative; wrong recipes cannot drift into unrelated random perturbations. Complete bank derivations are independently recomputed from the **printed integrand**, not generator metadata. This profile's operations are author metadata, with no learner-facing distractor diagnosis.

Bounds apply equally to explicit parameters and samplers. See classification for all ranges and rationale. Easy has three representations/layouts but all share the same exponent workload. Moderate families retain their observed workload; hard uses higher reciprocal roots and exactly one rule application. Every allowed parameter list is finite and exhaustively checked. Distinct meaningful tasks per level are reported by reduced exponent; representation changes and source profile changes do not inflate those counts.

Raw fields/difficulty/solutions/correct refs preserve attribute presence. The raw radios are not passed to native grading without separately authored completion, because their missing original keys cannot make a valid grading fixture. Four fieldless raw records similarly have no original grading target. Completed records preserve original radio answer type/layout/count or explicitly author a five-option radio where absent. All field-owned answer UUIDs are deterministic; permutation and seeds do not affect content identity. Changes in complete displayed banks do.

No mathematical source error was found. q-29662's differential is the single supported presentation repair. The generator stops at step 7 with local artifacts only.

Normal learner prompts explicitly add `Assume $x>0$.` so every root/reciprocal rewrite and primitive uses the declared positive connected real domain. Raw replay preserves the original prompt exactly. Markdown/review previews label difficulty and source/generated origin and mark generated correct choices with ✓; raw missing keys remain explicitly unmarked.
