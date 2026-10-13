# Four-stage extraction

## 1. Describe the originals

q-211986 displays `2x - y =-2` and `6x - 3y =-12`. Both are integer standard-form lines with both variable terms present. The dependent coefficient of the first is -1. Multiplying the first equation by 3 would give constant -6, different from the second's -12; the lines are parallel. The prompt names l_1/l_2, asks how many intersections, and completes a sentence with select placeholder field-1. Source choices, in captured order: “intersect at infinitely many points”, “intersect at one point”, “do not intersect”. Missing: difficulty, correct reference, worked solution.

q-237095 displays `y = 3x - 4` and `12x - 4y = 16`. The first is already isolated; substituting gives `12x - 4(3x - 4) = 16`, then `12x - 12x + 16 = 16`, then `16 = 16`. They coincide. The same prompt/field mask is used. Captured choices: “intersect at one point”, “do not intersect”, “intersect at infinitely many points”. The same three attributes are absent.

Original MA capture entries corroborate the full banks and layout but do not resolve missing keys or solutions. Canonical e-14011 instead shows x-isolation followed by grouped substitution, distribution, cancellation to a true statement, then the connection from solutions to intersections. Its original stages: system; first equation and isolated x; standalone substitution; second equation, grouped substitution, distribution, constant equality; always-true conclusion and coincidence. Completed generated solutions use the same operative stages and shared prose, choosing y as the isolated variable to match the two observed practice masks. Required moving/dividing stages are added only when the displayed first equation needs them.

## 2. Generalize the skill

Two complete linear equations determine two lines. Substitute an isolated dependent variable into the other equation and interpret the remaining equation: nonzero independent coefficient means one solution, a true constant statement means infinitely many, a false constant statement means none. Respond with one of the complete observed categories, without computing intersection coordinates or a general solution family.

## 3. Map every component

Parameters a,b,c,d,e,f specify `ax+by=c`, `dx+ey=f`. First dependent isolation gives `y=mx+h`, where `m=-a/b`, `h=c/b`. Substitution gives `dx+e(mx+h)=f`; distribution retains separately `dx`, `emx`, `eh`; collection gives `(d+em)x+eh=f`. These coefficients and constants are recomputed from the actual lines; no answer lookup table is used.

| Source/profile | a,b,c | d,e,f | infinite choice | one choice | none choice | Inferred correct |
|---|---|---|---|---|---|---|
| q-211986 / observed-211986 | 2,-1,-2 | 6,-3,-12 | intersect at infinitely many points | intersect at one point | do not intersect | none |
| q-237095 / observed-237095 | -3,1,-4 | 12,-4,16 | intersect at infinitely many points | intersect at one point | do not intersect | infinite |

All six displayed source values and answer types map exactly. These are exhaustive categorical alternatives, not numerical distractors with hidden arithmetic operations. They represent claiming each alternative line relation; no speculative error diagnosis is displayed. All options belong to the generated field with stable owned UUIDs. Original IDs/db IDs are preserved in source evidence; generated local UUIDs are intentionally new.

Fixed prompt: original “Consider the lines...” prose, line labels, count question, complete sentence and field placeholder. Variable: the two complete equations and optional paired variable names. Conditional: first equation isolated versus standard; correct category; solution statement true/false/nonzero coefficient. Raw observed profiles preserve missing attrs for every parameterization; normal categorical profile completes inferred keys and authored solutions. There is no copied-source-payload branch. Template masks render coefficients with unit suppression, signed ordered sums and the observed right-side spacing, reproducing both prompts byte for byte at their original parameters.

## 4. Extract constraints, solutions and identity

Easy: first b=1, integer nonzero slope magnitude1..5, intercept magnitude<=6; second dependent coefficient magnitude2..5 and integer slope/intercept with the same bounds. First is printed isolated. Moderate: |b|=1, same integer slope/intercept limits and second nonunit coefficient bounds; first printed standard and requires moving its nonzero independent term. For b=-1, the extra sign-isolation row is retained. Hard: primitive |a|,|b| in2..5 with gcd1, so isolation requires a genuine fractional slope. Second coefficients reduce to primitive magnitudes2..5 with scale1..5, displayed magnitudes<=25; |f|<=33, |c|<=6. Both independent/dependent terms are nonzero. All explicit calls use the same guards; no resampling invalid explicit parameters. All numbers remain exact rational/integer values.

Normal fixed solutions preserve the shared canonical opening, first-isolation conditional, “Then, we substitute”, standalone isolated equation, original second equation, grouped replacement, separately distributed terms, collection and interpretation. For one intersection, a final moved constant equation is shown and the nonzero coefficient guarantees one independent and hence one dependent value; no point is computed. Intermediate arithmetic is independently parsed from rendered rows and checked against the actual prompt. A mutation replacing distribution by collection must fail despite algebraic equality.

Geometry fingerprints convert complete `(a,b,c)` equations to primitive integer triples with normalized sign and sort the pair. They exclude scales, order, paired variable aliases, category-only labels, profile, bank and seed. Actual distinct geometric line pairs count as tasks. Content identity instead hashes version, actual difficulty/presence, prompt, fixed solution/presence, complete sorted bank and field/answer types. Option order or profile alias cannot change identity; different rendered prompts/solutions/difficulty do.

Meaningful finite default variety is counted explicitly, not infinite coefficient aliases. Easy/moderate have 130 integer-slope lines (10 slopes,13 intercepts); normal sampling covers 130 coincident tasks,780 parallel pairs and7020 different-slope/different-intercept pairs =7930 geometric tasks per level. Explicit inputs allow the additional shared-intercept crossing tasks, yielding8515 total. Hard has20 primitive slope directions and13 first constants; second crossing constants are the distinct fractions n/k, |n|<=30, k1..5. Parallel offsets use distinct nonzero fractions delta/k with |delta|1..3. Validation reports exact counts after order/sign/scale deduplication. Different levels can assess the same geometry through distinct information/isolation workloads; geometry fingerprints deliberately identify those as the same mathematical object.

No parameter-dependent plot occurs. Steps5 and7 require no rendering or plot extraction beyond this documented none classification. Raw evidence is ineligible for practice until completion because it lacks a native correct ref. Native tests cover completed records and every owned categorical option separately; no missing-source key is counted as an observed matched key.
