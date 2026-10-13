# Four-stage template extraction

## 1. Specific source descriptions

q-28850 is a 345×29 number line with labelled integers -3 through 3. A red finite segment runs from open -1 to filled 2. Its field has five full `x ∈ interval` values: `(-1, 2)`, `[- 1, 2]`, `(- ∞, 2]`, `(-1, 2]`, `[- 1, 2)`. It has no rating, key or solution.

q-31762 is a 296×29 number line with labelled integers 1 through 6. A red finite segment runs from open 1 to open 4. Its five values are `[1, 4)`, `(1, 4)`, `(-1, 4)`, `[1, 4]`, `(1, 4]`. It has no rating, key or solution. This is a both-open source anomaly, not another intended half-open family.

Both prompts contain an image, blank line and identical question sentence. Neither has a placeholder; radio fields do not need one. Original captures and authoritative widget text are preserved. Adjacent decoded backslash runs in the canonical solution are measured in decoded-source-bytes.json; all are single. No TeX escape repair is claimed from JSON serialization.

## 2. Shared mathematical pattern

Read two ordered finite endpoint coordinates from a number line, read whether each endpoint is filled or open, and select the corresponding complete interval. For this KP, normal questions require exactly one filled endpoint. Use a bracket for inclusion and parenthesis for exclusion. Source q-31762 violates the exactly-one condition and stays raw evidence only.

## 3. Complete component and bank maps

Let a and b be the left and right endpoint values, with a < b. The field is `selection`, radio, five math-valued choices. Every profile chooses its complete operation list before sampling.

| Source/profile | Original value | Parameterized recipe | Independent source semantic result |
|---|---|---|---|
| q-28850 / raw_q28850 | x ∈ (-1, 2) | (a,b), both excluded | (-1,2) |
| same | x ∈ [- 1, 2] | [a,b], both included | [-1,2] |
| same | x ∈ (- ∞, 2] | (-∞,b], replace finite left boundary with ray | (-∞,2] |
| same | x ∈ (-1, 2] | (a,b], left excluded, right included | (-1,2], actual original truth |
| same | x ∈ [- 1, 2) | [a,b), left included, right excluded | [-1,2) |
| q-31762 / raw_q31762 | x ∈ [1, 4) | [a,b) | [1,4) |
| same | x ∈ (1, 4) | (a,b) | (1,4), actual original truth |
| same | x ∈ (-1, 4) | (-a,b), negate left coordinate and exclude both | (-1,4) |
| same | x ∈ [1, 4] | [a,b] | [1,4] |
| same | x ∈ (1, 4] | (a,b] | (1,4] |

Every original choice is mapped; five-to-five matching uses both exact decoded value strings and complete SymPy interval sets. The source has no correct designation to match: designation denominator 0, missing 2. It has no solution to match: solution denominator 0, missing 2. Missing fields stay absent in raw output.

Observed recipe interpretations are limited: four closures are explicit structural alternatives, left ray is an observed alternative, and sign-negated a matches the other bank. These are concrete transformations, not inferred learner diagnoses. No option feedback is invented. Negated-left banks require a ≠ 0 and -a < b, otherwise the WHOLE bank fails. All banks reject semantic duplication. No first-valid distractor pool is used.

Normal defaults use an explicitly authored bank: the same four endpoint closures plus the correct half-open orientation with left endpoint displaced by one tick. This bank assesses a reading error and remains bounded. Separate normal observed-bank profiles preserve the complete ray or negate bank under changed eligible parameters. Profile aliases never affect mathematical identity; actual displayed content affects content identity.

## 4. Reusable template and constraints

Fixed prompt/layout: `![](plot)` followed by the exact source question sentence. Variable components: a, b, left inclusion, tick increment, label increment, derived plot bounds. The right inclusion is the opposite of the left in every normal question; raw_q31762 alone fixes both endpoints open and is marked evidence_only.

Source raw profiles require explicit bounded integer parameters, fully labelled unit ticks and open left endpoint. Their original plot paths are reused only at exactly the source geometry; changed parameters invoke Matplotlib. Raw output preserves absence of difficulty, correct ref and worked solution. It does not become learner eligible merely because its truth can be inferred.

Normal repairs author the rating, derive a key from the displayed interval sets and use the complete canonical shared opening plus inequality and interval stages. q-28850 geometry stays unchanged in a fresh renderer; q-31762 changes only its left closure. Canonical math blocks are constructed from complete endpoint/operator slots, avoiding blind substitutions through prose or TeX commands. The normal solution is fixed independently of the selected wrong choice.

Easy catalog: integer -4 ≤ a < b ≤ 4, gap at most 4, unit ticks and unit labels, both half-open orientations. Moderate: integer -6 ≤ a < 0, a+2 ≤ b ≤ 6, gap at most 6, unit ticks, alternate labels; a or b must be odd. Hard: half-integers -4 ≤ a < 0, a+1 ≤ b ≤ 4, gap at most 4, half-unit ticks, whole labels; at least one endpoint must be a noninteger half. These guards also apply to explicit calls. Eligible complete bank counts are recorded in validation.json.

Mathematical fingerprint: exact a/b, the two inclusion states, assessed tick and label increments. Complete bank, solution, actual prompt and version determine content identity. Choice shuffling and seeds do not change identity for fixed displayed content. No database IDs or transaction records are emitted.

## Additional source profiles at basis 2110

q-154795 has a=-3, b=2, two open markers, unit ticks with integer labels -4 through 4, a five-choice selection field, and correct value x\\in (-3,2). Every bank member is exactly one of (a,b), [a,b], (a,b], [a,b), or (-infinity,b). The last is an open-left unbounded region with open right endpoint, unlike q-28850's closed-right ray. The whole bank is replayed in current_validate.py; this both-open family is evidence only and excluded from this KP's supported generated workload. Its solution first states parentheses/brackets without color, then -3<x<2, then x in (-3,2).

q-31779 has a=2, b=4, closed-left/open-right markers, fully labelled unit ticks 1 through 6, a five-choice selection field, and correct value x\\in [2,4). Its complete bank contains all four closure combinations and [a,infinity). Each source member is mapped to the corresponding closure recipe; the unbounded distractor has fixed positive-infinity right endpoint and fixed closed left endpoint. The bank is parameterized as observed_right_ray, chosen before option construction. Replaying a=2,b=4 matches all five complete mathematical sets; source-specific TeX formatting is also replayed exactly by the evidence validator. Normal variants use the existing Unicode interval value style. Both sources retain their original prompt shells and their two-stage inequality→interval solution order; newly generated solutions use the existing canonical colored opening and authored exact substitutions, not an exact match claim for the newer uncolored prose. No source facts are repaired.
