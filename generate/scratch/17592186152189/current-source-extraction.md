# Source additions at math basis 2658

Lineage: `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source-current.json` captures all 18 practice questions and the canonical example in one Pull. The 15 questions in the original basis-1356 capture remain unchanged, ignoring entity IDs and derived reverse links. Original evidence remains in `source.json`, `specs.json`, `classification.md`, `template-extraction.md` and `raster-geometry.json`.

Current practice classification: seven moderate graph-reading radio questions, ten hard rightmost-start CCW questions (six radio sources including one duplicate historical layout, and four two-expression blanks), and one unrated radio question. The hard radio source count is six total, including the duplicate layout, and the hard blank source count is four. The unrated source and incomplete duplicate field remain excluded from inventory. Easy is an authored direct-substitution family, supported by the canonical translated ellipse formula and the predecessor center/radius workload; it adds no new operation. Moderate plots remain heavy; hard plots moderate; easy has none.

The three additions preserve existing mathematical backbones and introduce two distinct complete radio bank profiles and one blank presentation mask. Source presentation masks are separate from the three mathematical families; individual formatting masks do not imply a new instructional template. All added parameters stay inside the original integer radius/center domain.

## Specific additions and reusable slots

- `q-79288` (17592186541062), moderate: graph-only prompt, ellipse center (4,-2), horizontal radius 7, vertical radius 4; one five-choice `selection` radio field. Its original 360×304 transparent PNG has axes through approximately (79,118) and 22.5 pixels/unit. The visible ellipse has extrema x=-3,11 and y=-6,2. Signed axis labels and center guides independently agree with the prose and correct bank entry.
- `q-106396` (17592186541144), moderate: same graph-only question structure and response contract; center (-2,3), horizontal radius 3, vertical radius 6. Original graph axes approximately (169,224), 17.6 pixels/unit, extrema x=-5,1 and y=-3,9. Signed labels and guides agree. It has its own complete bank profile.
- `q-327167` (17592186541086), hard: supplies center (-3,4), horizontal radius 2, vertical radius 6, and requires one CCW traversal starting at A(-1,4). Original graph axes approximately (213,238), 16.8 pixels/unit. Extrema x=-5,-1 and y=-2,10; rightmost A and upper-right upward-left arrow agree with the stated start and direction. Two blanks retain supplied `x=`/`y=` notation, exact expression fragments, and newlines around placeholders. No distractors exist.

The visual measurements above are approximate independent readings from the original signed ticks; the retained original bytes and exact mathematical values are authoritative. White compositing was used only for inspection; original asset bytes were preserved. No new plot topology is introduced. Variable slots remain positive distinct integer radii a,b in 1..8 and integer h,k in -6..6 with nonorigin center; rightmost start A(h+a,k) and arrow/solution references depend on the same slots. Numerical variation preserves the method and workload.

## Complete choice-to-operation mapping

The exact original values and their field ownership are retained in `source-current.json`. The following order matches that capture; every recipe is applied as the complete pair `(x,y)` with trigonometric functions shown. No choice is pooled into another profile.

| Source | Index | x recipe | y recipe | Designation |
|---|---:|---|---|---|
| q-79288 | 0 | b cos(theta)+h | a sin(theta)+k | incorrect |
| q-79288 | 1 | b cos(theta)-k | a sin(theta)-h | incorrect |
| q-79288 | 2 | a cos(theta)+k | b sin(theta)+h | incorrect |
| q-79288 | 3 | a cos(theta)+h | b sin(theta)+k | correct |
| q-79288 | 4 | a² cos(theta)-h | b² sin(theta)-k | incorrect |
| q-106396 | 0 | b² cos(theta)+h | a² sin(theta)+k | incorrect |
| q-106396 | 1 | a cos(theta)-h | b sin(theta)-k | incorrect |
| q-106396 | 2 | b cos(theta)-h | a sin(theta)-k | incorrect |
| q-106396 | 3 | b cos(theta)+h | a sin(theta)+k | incorrect |
| q-106396 | 4 | a cos(theta)+h | b sin(theta)+k | correct |
| q-327167 | field-1 | a cos(theta)+h | — | canonical x fragment |
| q-327167 | field-2 | — | b sin(theta)+k | canonical y fragment |

These recipes preserve observed compound operations. Their psychological interpretation is unproven; they are not named as misconceptions in learner text. `specs-current-additions.json` preserves the exact function spellings, spaces, masks, complete banks, correct indices and parameter constraints. `update_current_sources.py` rebuilds only those supplemental specs from the retained current capture. Source replay preserves all supplied notation and ordered solution stages: general formula, optional orientation statement, concrete center/radii, final parametric equations with domain. Changed-parameter replay uses (a,b,h,k)=(7,2,-5,3) for each complete added profile.

## Normal sampling and grading

Normal easy/moderate retain the reviewed authored-locus bank. Normal hard retains the reviewed authored-orientation bank; these authored complete banks are distinct from historical profiles and are explicitly identified in generation metadata. Each selected complete bank must have exactly one mathematically valid answer and no equivalent options. Replenishment uses hard radio to avoid relying on unresolved phase-shift blank equivalences. Canonical and factored blank expressions are still tested with the current learner grader; documented unresolved identities are not counted as accepted.

Stable generator UUID is saved in `generator-id.json` and reused on registration. Extending replay coverage changes the script hash and adds a supplemental input; normal question payloads and mathematical identity policy are unchanged. The current frozen inputs and exact native library hashes are recorded in `reference/replenishment/validation.json` and `current-native-build.json`. Inventory deduplication is stricter than generator UUID identity: a tuple (a,b,h,k) is used only once across all difficulties and layouts during replenishment, and original/canonical tuples are protected. Seed, bank, notation, response layout, UUID or option order alone cannot create another inventory question.
