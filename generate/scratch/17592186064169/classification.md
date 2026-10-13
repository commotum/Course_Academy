# Classification — KP 17592186064169

Database `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source.json` preserves the full captured wrapper/record unchanged. Six practice questions, separate from canonical e-368. No plots or assets occur, so every template's plot rating is **none**; steps 5 and 7 require no renderer.

| Source | Captured difficulty | Template | Captured response | Complete observed bank |
|---|---|---|---|---|
| q-29987 | absent | negative_named_radio | one `selection` radio; no correct ref | 5 choices, q-29987 profile |
| q-29989 | absent | reciprocal_named_radio | one `selection` radio; no correct ref | 5 choices, q-29989 profile |
| q-71100 | easy | negative_named | fields absent | none |
| q-113705 | moderate | reciprocal_named | fields absent | none |
| q-29633 | moderate | reciprocal_integer | fields absent | none |
| q-29662 | moderate | reciprocal_sqrt | fields absent | none |

Six distinct Markdown/value templates retain their notation, prompt structures and ordered solution sequences. The two old radio prompts differ in integrand representation and bank formulas; their absent solutions cannot be called an observed sequence. Normal completed records use an explicitly authored five-option radio field, grounded in the two authoritative captured multiple-choice layouts. No blank field is invented. All raw profiles preserve missing difficulty, fields, worked solution and correct references individually. Database IDs/UUIDs are source evidence, while generated question/field/answer identities belong to their generated content.

The owning MA lesson capture `/home/jake/Developer/MA/DATA/Lessons/308/Source/308.json` identifies both q-29987 and q-29989 as multiple-choice widgets with five choices. Its original widget snippets are copied into `widget-evidence.json`; neither widget exposes an answer key or worked solution. The other four question IDs do not occur in that old local lesson capture. Their newer basis-1356 EDB evidence therefore remains authoritative for prompt/solution; their assessment completions remain authored.

The two unrated radios receive an **authored easy assignment**: each integrates a unit negative rational power with result exponent between zero and one, matching the rated q-71100 route. Raw replay still omits the rating. There are no observed hard practice records.

## Curriculum and scope

Follow `activity/first-step` and `step/next`: Introduction → Power Rule for Integration → Monomial → Radical → Reciprocal → Final Notes. The sequence is recorded explicitly in `curriculum-route.json`, rather than inferred from collection order. Prerequisite topic 35 is Power Rule for Differentiation. The immediately subsequent topic 43 is Constant Multiple Rule for Indefinite Integrals, so the integrand numerator stays one. The final tutorial explicitly excludes n=-1 and defers 1/x; no logarithms appear.

Normal easy varies already-negative primitive rational exponents with 0<p<q≤9. Moderate varies unit reciprocals of integer powers 2–9, primitive rational powers p/q>1 with 2≤q≤5 and p≤9, or square roots with odd p=3,5,7,9. Hard is explicitly authored: unit reciprocals of higher roots, 3≤q≤7, q<p≤q+8, gcd(p,q)=1. The extra demand is reading the reciprocal higher-root notation, converting to a rational exponent, adding one to a negative rational exponent and restoring reciprocal form. This is one integration by the same power rule; it adds no new integration technique. It stays within the radical sibling's rational-power prerequisite but keeps that radical in the denominator, distinguishing this KP from the positive radical sibling. These are unordered alternatives at a fixed workload, not a progression.

Task fingerprints use the reduced integrand exponent, x>0 connected domain and requested antiderivative family modulo additive constants. Equivalent representations across templates share one task fingerprint. Displayed prompt/solution/bank/difficulty/layout determine content identity. Profile aliases, seed and option order do not.

## Source anomalies and supported completions

- Two radios omit difficulty, worked solution and correct reference. Their keys are independently inferred by differentiating all five displayed choices. The resulting source keys are **not counted as matched original designations**.
- Four rated records omit fields; raw replay omits the key, while normal output supplies an authored radio bank. No existing answer shape is overridden.
- q-29662 omits the differential from its first integral. Raw source replay preserves this exact notation. Normal output adds `\,\text{d}x`; this is a presentation repair, with all remaining prose and row order unchanged.
- Source bank intent is underdetermined, especially the `(p+q)` coefficient and `p/(q-p)` exponent. All ten exact choices are parameterized and preserved through public raw profiles. Those opaque profiles, even with authored correct refs/solutions, are **evidence-only, ineligible for learner sampling**. Normal defaults use a separately labeled complete authored operation bank.

Normal learner prompts explicitly add `Assume $x>0$.` so every root/reciprocal rewrite and primitive uses the declared positive connected real domain. Raw replay preserves the original prompt exactly. Markdown/review previews label difficulty and source/generated origin and mark generated correct choices with ✓; raw missing keys remain explicitly unmarked.
