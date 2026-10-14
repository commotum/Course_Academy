# Inventory classification refresh, 2026-10-14

Current capture at math basis 2289, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`, is retained in `reference/initial/kp.edn`. The 14 frozen practice questions and canonical example are unchanged. Three new moderate sources bring the current count to 17: nine moderate and eight hard. Easy remains unobserved and explicitly authored, with the supplied quadratic-level workload justified in `classification.md`. Every field is radio; q-37515 retains its two captured fields and missing legacy correct ref. No new source question, choice, or solution contains a plot; every family is rated **none**.

`reference/preflight/source-validation.json` and the commit package's `source-validation.json` retain exact new banks, independently decoded level functions, evaluated gradients, and solution-stage checks. The frozen generator's 15 complete banks (75 values) and all 14 prompt/solution replays still pass. Those fidelity counts apply to the frozen families; they are not inflated to claim generated replay of the new families.

## New family: q-71406, logarithm plus monomial product

The surface is `ln(x+y+z)=ln(2)-xyz`, point `(1,0,1)`. The selected level function is `ln(x+y+z)+xyz`, constant `ln(2)`, in the domain `x+y+z>0`. Its gradient at the point is `(1/2,3/2,1/2)`. The question expects a complete vector equation in one five-choice radio field, without a parameter-range suffix.

Its solution rearranges the surface, introduces the level function, writes the formal three-partial gradient, differentiates the logarithm and product, substitutes the point, reduces to fractional components, and constructs the normal line. The logarithmic denominator and product rule are structural. The original full choices, interpreted as `(basepoint; direction)`, are:

- `(1/2,3/2,1/2); (1,0,1)`
- `(1,0,1); (1,1,1)`
- `(1,0,1); (1/2,0,1/2)`
- `(1/2,3/2,1/2); (1/2,0,1/2)`
- `(1,0,1); (1/2,3/2,1/2)` — correct.

These are retained as one complete opaque source profile. A reusable geometric evidence recipe transforms every basepoint by `h+s*B` and every direction by `s*D`; this reproduces each complete mathematical value at `h=0,s=(1,1,1)`. The historical distractor intent is unresolved. They are not silently merged with v1's method-derived banks.

## New family: q-131125, quadratic saddle with linear z term

The surface is `x^2-y^2=4-4z`, point `(0,2,2)`. The selected level function is `x^2-y^2+4z`, constant `4`, over real coordinates. Its gradient is `(2x,-2y,4)` and evaluated direction `(0,-4,4)`. One five-choice radio field expects the complete vector line without an `r=` prefix and with the parameter range.

The solution rearranges to a level function, computes formal and symbolic partials, substitutes, removes the zero x component, collects the direction, and constructs the vector line. All stages and the answer's zero-coordinate behavior are structural. Original `(basepoint; direction)` choices are:

- `(0,2,2); (2,4,4)`
- `(0,-4,-4); (0,2,2)`
- `(0,2,2); (2,-4,4)`
- `(0,2,2); (0,-4,4)` — correct.
- `(0,-4,-4); (2,2,0)`

This is another complete opaque profile with the same basepoint/direction isometry evidence recipe. It differs from the frozen saddle family in response contract and solution masks; changed numbers alone are not the distinguishing feature.

## New family: q-37231, logarithmic sphere with parametric response

The surface is `ln(x^2+y^2+z^2)=1`, point `(0,0,sqrt(e))`. Its level-function domain excludes the origin. The gradient is `2(x,y,z)/(x^2+y^2+z^2)` and the evaluated normal direction is `(0,0,2/sqrt(e))`.

One five-choice radio field contains complete triples of parametric equations. It is a separate answer shape from a vector line and from symmetric equations. The worked solution introduces the supplied level function, computes formal and symbolic partials, substitutes and reduces, supplies three point-plus-partial formulas, then concludes with the three concrete equations. Exact source triples are preserved in the database capture and validation evidence. Decoded `(basepoint; direction)` values are:

- `(0,0,0); (1,1,2/sqrt(e))`
- `(0,0,sqrt(e)); (-1,0,1/sqrt(e))`
- `(0,0,sqrt(e)); (1,0,1/sqrt(e))`
- `(0,0,sqrt(e)); (0,0,2/sqrt(e))` — correct.
- `(0,0,sqrt(e)); (0,1,2*sqrt(e))`

The complete source bank has exactly one geometrically valid choice. The inventory validator independently parses the parametric triples, derives basepoints and directions, checks all displayed derivative stages and the three construction formulas, and tests every selected answer with the real learner grader. Whitespace before square-root tokens is normalized locally in this evidence parser to avoid the frozen TeX parser misreading adjacent `t` and `sqrt` as free symbols.

## Bounded generator scope and replenishment

The frozen `normal-surface-v1` generator is reused unchanged. It generates its original six moderate/eight hard families and the authored easy family. The three newly captured families are classified and checked as existing inventory but are outside this version's generated-family domain; in particular it does not generate parametric triples. This is a family capability boundary, not a claim that the moderate difficulty is unsupported or filled by another response type. Their source records and history remain intact. A future request for one of these specific families must extend extraction, complete-bank replay and changed-instance validation before generation.

Translations are bounded by `[-2,2]^3` for easy and `[-3,3]^3` for observed families, with eight reflections. These are finite sampling domains (at most 1,000 easy isometry inputs and 2,744 per observed family), with mathematical aliases excluded. The package does not promise unlimited variants or coefficient/evaluation-point variation. No finite limit is reached for this job.

The native initial reader reports easy 0, moderate 9, hard 7. The stricter mathematical/gradable count excludes q-131124's false worked equality and q-37515's incomplete field, without editing either source. Historical exposure and active reservations are excluded at the same captured basis. Only the actual missing reserve is generated. Seed, identity, bank profile and choice order do not enter task distinctness. The deduplication key canonicalizes the printed surface relation, actual point and response criterion and includes all source/canonical tasks before selecting new questions.

The scoped `replenish.py` uses the existing native inventory reader, EDB Database integration, deployed native preview specs and configured `:application/ca-engine` contributor. Its complete request, exact EDN, preview, receipt and exact-basis verification are retained under `reference/replenishment/`. It holds the application's `api.lock` from the fresh inventory/basis check through submission and readback, and uses the durable basis guard. Registration uses `question-generator/id`, `question-generator/script`, and the existing KP reference, preserving an already registered identity when present.
