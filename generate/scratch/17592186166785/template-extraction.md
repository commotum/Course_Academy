# Extracted templates

## q-95534

Original: indefinite integral of sech squared with argument 2x/5. Positive rational scale 2/5, no shift, real x, one `selection` radio field, five math options each ending in + C. No original key or practice solution exists. The complete source bank is retained in source.json and all five choices are individually mapped in source-choice-mapping.json.

General pattern: integrate sech²(ax) by substituting u=ax, dx=du/a, and using integral sech²u du=tanh u. Correct fragment is tanh(ax)/a + C. Preserve the five-choice layout. At original a=2/5 the recipes in source order are:

1. a*tanh(ax)^2 + C.
2. -csch(ax)^2/a + C.
3. a*tanh(ax)*sech(ax) + C.
4. tanh(ax)/a + C (derived correct).
5. -5*tanh(x/a) + C.

The constant 5 in option 5 is retained as observed, not silently changed to a presumed inverse-scale mistake. Its intent is unresolved; complete expression replay is verified. Proposed sampling keeps denominator 5 fixed, numerator n=1..12. Every scale is positive and every task has domain real x. Coefficients are rendered exactly; denominators and arguments stay tied to the same n. This is a bounded extension of the single observed positive rational coefficient; negative or shifted variants are not claimed.

## q-95535

Original: definite integral from 1 to 2 of sech(5x)tanh(5x). Positive integer scale a=5, no shift. Same single radio field and five math options, no integration constant. Neither key nor solution exists. Complete recipes in source order:

1. (sech(a)-sech(2))/a.
2. a*(sech(2)-sech(a)).
3. (tanh(2)-tanh(a))/a.
4. tanh(2a)^2/a.
5. (sech(a)-sech(2a))/a (derived correct).

General pattern: u=ax, transformed endpoints a and 2a, primitive -sech(u), final result (sech(a)-sech(2a))/a. Both bounds and the negative primitive are shown in one fixed authored worked solution. The source's unusual literal 2 in options 1–3 is preserved; author mistake intentions are unresolved. Proposed a=3..14 is a bounded positive integer extension. a=2 is excluded because options 1 and 3 both become zero. All accepted banks are separately verified to contain five different values and exactly one correct answer.

## Fidelity, presentation, and limits

Each original question maps to its own complete profile; profiles are never pooled. All 10 original values replay exactly at their source parameters, including 8 distractors. The missing keys and solutions are authored and checked independently, so exact source-solution wording fidelity cannot be claimed. Canonical solution has malformed command spellings; originals remain untouched. Source prompts/choices have omitted command slashes (sech/csch and intsech); exact replay keeps this evidence, while genuinely new parameter variants add valid command slashes and macro definitions. Full prompt/field/choice originals and side-by-side variants appear in review.json/review.md. Source tasks are excluded from commits regardless of new UUID or authored key. Fingerprints encode mathematical integrand/scale/bounds, excluding seed, UUID, wording and option order. No new plots or unchanged image assets are needed (plot rating none), so stages 5 and 7 have no assets to extract or generate.
