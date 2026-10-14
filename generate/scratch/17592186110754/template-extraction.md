# Extracted coordinate templates

Source-specific parameters and full raw records are retained in source.json. All originals are described in classification.md. Every original choice has a field-owned mapping to a generated mathematical value in source-replay.json. No source identity is reused for authored questions.

## Backbone and slots

A point A lies on the unit circle in the first quadrant. One positive coordinate is supplied and the other is requested. Apply x²+y²=1; substitute and square the supplied coordinate; subtract its square from one; take the square root; show both algebraic signs and choose the positive branch. One selection radio, five options; each option is numeric or an equation assigning the requested coordinate according to the chosen complete bank profile. No new response fields, operations or solution stages.

Fixed: point label A, first quadrant, unit radius, Pythagorean identity, positive branch, five choices and selection field. The first-quadrant restriction determines the sign; unit radius determines the constant one. A stays fixed because renaming it adds no mathematical variation.

Variable: known axis x or y, numerator radicand n, positive integer denominator d, and one complete source bank profile. The supplied value is sqrt(n)/d, square n/d², missing-coordinate square (d²-n)/d² and answer sqrt(d²-n)/d. Axis changes update prompt, substituted side, unknown variable throughout all rows, final answer and equation-valued banks together. Numeric templates preserve value-only answers.

Observed domains: rational supplied values for q-23274, q-65027, q-23216 and q-65031 (n a perfect square); nonsquare integer radicands for q-124608, q-124611 and q-124613. Preserve these profile conditions. Normal sampling conservatively bounds 3≤d≤8, 1≤n≤min(12,d²−1), with positive real, finite, distinct choices and exactly one correct answer. The original n=49,d=8 remains available for replay but is outside the narrower normal numerator range. This keeps arithmetic workload small; it is a sampling policy, not a claim about all possible unit-circle problems.

Select a complete profile before its eligible parameters. Resample/reject complete banks on collision or nonreal values; never fill from a pool of unrelated distractors. Seeds order selection only. Novelty uses the unordered pair {n/d²,1−n/d²}; coordinate swapping, equivalent reduced input fractions, different profiles, new UUIDs or choice order alone cannot create new mathematical tasks.

## Complete bank recipes

Write m=d²−n and c=sqrt(m)/d. Each row reproduces the complete source bank in source order. Equation profiles prefix each value with the requested variable and '='; numerical profiles do not. All offsets below are literal observed expression patterns generalized conservatively. Their original psychological explanations are unresolved, and are not asserted in learner content.

| Profile | Five recipes | Correct |
|---|---|---|
| q-23274 | c; sqrt(d−1)/d; −sqrt(m+2d)/d; −c; sqrt(m+2d)/d | first |
| q-65027 | sqrt(m+2sqrt(n))/d; sqrt(m)/d²; m/d; m/d²; c | fifth |
| q-124608 | −sqrt(d²+n)/d²; c; sqrt(m−n)/d; −sqrt(m−1)/d²; sqrt(d²+n)/d | second |
| q-124611 | sqrt(m−1)/d; sqrt(m)/d²; c; sqrt(m−1)/d²; sqrt(n+1)/d | third |
| q-124613 | sqrt(m−2)/d; −sqrt(n−2)/d; −sqrt(m+2)/d; c; sqrt(m)/d² | fourth |
| q-23216 | sqrt(n+1)/(d−1); m/(2d²); (d−sqrt(n))/d; c; d/(d+sqrt(n)) | fourth |
| q-65031 | sqrt(m)/d²; m/d²; c; sqrt(n−1)/d; m/d | third |

Source replay compares the complete mathematical value and equation variable, not just option ordering. Five source designations are verified; the missing two are mathematically authored for new output only. No incorrect source key was found. Two original worked solutions are absent; new output derives the shared canonical solution sequence without changing those source records.

## Prompt and worked solution

Preserve the source's unit-circle statement, supplied-coordinate statement and requested-coordinate question. Worked solutions retain the opening Pythagorean statement; substitution introduction; seven aligned algebraic rows; first-quadrant positive-branch justification; and concrete final assignment. Values and axis references are parameterized together. LaTeX whitespace, fraction simplification, source punctuation and aligned layout are normalized; exact literal solution-byte replay is not claimed. No distractor feedback is introduced. Side-by-side source/parameter replay, axis changes with fixed numbers and fresh instances appear in review.md.
