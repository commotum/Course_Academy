# Template extraction

## 1. Specific source descriptions

Each plot has an origin vertex and one integer on-curve coordinate (no equation given). All responses are the slope expression dy/dx, not a tangent equation or slope at the marked point. Observed blanks request a y-only fragment after an existing dy/dx= prefix. Historical radio prompts do not restrict the variable explicitly. Number forms are exact integer coordinates and rational p, c and derivative coefficients. Source explanations retain the standard/general direction wording, point substitution, numeric square, p isolation, resulting curve, formal differentiation, chain factor and final isolation.

- q-127372: unrated, radio `selection`, marked (1,2), p=1, c=4, derivative coefficient c/2=2; 5 values. Correct reference and solution absent; raw also omits difficulty.
- q-127374: unrated, radio `selection`, marked (-2,2), p=-1/2, c=-2, derivative coefficient c/2=-1; 5 values. Correct reference and solution absent; raw also omits difficulty.
- q-127510: :question.difficulty/moderate, radio `selection`, marked (3,6), p=3, c=12, derivative coefficient c/2=6; 5 values. Correct reference and eight-stage/block structure captured.
- q-127515: :question.difficulty/hard, radio `selection`, marked (-1,2), p=-1, c=-4, derivative coefficient c/2=-2; 5 values. Correct reference and eight-stage/block structure captured.
- q-127520: :question.difficulty/hard, radio `selection`, marked (-8,4), p=-1/2, c=-2, derivative coefficient c/2=-1; 5 values. Correct reference and eight-stage/block structure captured.
- q-312780: :question.difficulty/moderate, blank `field-1`, marked (5,7), p=49/20, c=49/5, derivative coefficient c/2=49/10; 1 values. Correct reference and eight-stage/block structure captured.
- q-342215: :question.difficulty/hard, blank `field-1`, marked (-3,-1), p=-1/12, c=-1/3, derivative coefficient c/2=-1/6; 1 values. Correct reference and eight-stage/block structure captured.
- q-342218: :question.difficulty/hard, blank `field-1`, marked (-6,6), p=-3/2, c=-6, derivative coefficient c/2=-3; 1 values. Correct reference and eight-stage/block structure captured.
- q-342354: :question.difficulty/moderate, blank `field-1`, marked (8,-8), p=2, c=8, derivative coefficient c/2=4; 1 values. Correct reference and eight-stage/block structure captured.
- q-342355: :question.difficulty/moderate, blank `field-1`, marked (6,-2), p=1/6, c=2/3, derivative coefficient c/2=1/3; 1 values. Correct reference and eight-stage/block structure captured.

## 2. Shared pattern

Read vertex O and marked point (a,b). Substitute b²=4pa, evaluate b² and 4a, solve p=b²/(4a), form y²=cx with c=b²/a. Apply d/dx to both sides, retain the y-chain factor 2y dy/dx=c and isolate c/(2y), valid for y≠0. Left/right opening is the sign of a. The marked point recovers the curve and is never a final tangent-point evaluation.

## 3. Complete component and answer mapping

All five complete historical radio banks are mapped below in their captured order. Recipes reproduce every original scalar/expression at original coordinates, but their intent is underdetermined. In particular the historical point-ratio and altered-p recipes cannot establish a recovered learner error. These public raw/completed profiles remain evidence-only. A scalar numerical fit is not used as the default bank.

The symbols c=b²/a, p=c/4 and m=c/(2y) are computed from the complete prompt geometry. The authored bank is [m, −m, c/y, 2y/c, c/2]: correct derivative, sign error, omit factor 2, invert derivative, omit factor y. Every option follows the actual implicit differentiation method. No feedback is added to learner choices.

### q-127372 / selection

| Captured value | Parameterized operation | Captured designation |
|---|---|---|
| $-\frac{y}{2}$ | -2y/c | missing designation (inferred only in completed record) |
| $-\frac{2}{y}$ | -m | missing designation (inferred only in completed record) |
| $\frac{2}{y}$ | m | missing designation (inferred only in completed record) |
| $-\frac{4}{y}$ | -c/y | missing designation (inferred only in completed record) |
| $4y$ | cy | missing designation (inferred only in completed record) |
### q-127374 / selection

| Captured value | Parameterized operation | Captured designation |
|---|---|---|
| $\frac{y}{2}$ | -y/c | missing designation (inferred only in completed record) |
| $\frac{1}{y}$ | -m | missing designation (inferred only in completed record) |
| $-\frac{1}{y}$ | m | missing designation (inferred only in completed record) |
| $-\frac{2}{y}$ | c/y | missing designation (inferred only in completed record) |
| $-\frac{1}{2y}$ | c/(4y) | missing designation (inferred only in completed record) |
### q-127510 / selection

| Captured value | Parameterized operation | Captured designation |
|---|---|---|
| $-\frac{1}{2y}$ | -a/(by) | incorrect |
| $\frac{6}{y}$ | m | correct |
| $-\frac{1}{6y}$ | -2/(cy) | incorrect |
| $\frac{2}{y}$ | b/(ay) | incorrect |
| $\frac{3}{2y}$ | p/(2y) | incorrect |
### q-127515 / selection

| Captured value | Parameterized operation | Captured designation |
|---|---|---|
| $-\frac{2}{y}$ | m | correct |
| $-\frac{1}{y}$ | c/(4y) | incorrect |
| $\frac{1}{2y}$ | -2/(cy) | incorrect |
| $\frac{2}{y}$ | -m | incorrect |
| $\frac{4}{y}$ | -c/y | incorrect |
### q-127520 / selection

| Captured value | Parameterized operation | Captured designation |
|---|---|---|
| $-\frac{2}{y}$ | c/y | incorrect |
| $-\frac{1}{y}$ | m | correct |
| $\frac{1}{4y}$ | -1/(2cy) | incorrect |
| $-\frac{1}{2y}$ | c/(4y) | incorrect |
| $\frac{4}{y}$ | -2c/y | incorrect |
### q-312780 / field-1

| Captured value | Parameterized operation | Captured designation |
|---|---|---|
| $\frac{49}{10y}$ | m | correct |
### q-342215 / field-1

| Captured value | Parameterized operation | Captured designation |
|---|---|---|
| $-\frac{1}{6y}$ | m | correct |
### q-342218 / field-1

| Captured value | Parameterized operation | Captured designation |
|---|---|---|
| $-\frac{3}{y}$ | m | correct |
### q-342354 / field-1

| Captured value | Parameterized operation | Captured designation |
|---|---|---|
| $\frac{4}{y}$ | m | correct |
### q-342355 / field-1

| Captured value | Parameterized operation | Captured designation |
|---|---|---|
| $\frac{1}{3y}$ | m | correct |

## 4. Reusable template and constraints

Fixed Markdown uses an image followed by the source derivative request. Direction, coordinate label, coefficient values, exact fractions, bank and plot geometry vary together. Blank prompts retain the field-1 placeholder and derivative prefix; radio fields retain key selection and five choices. The observed moderate/hard worked template has four display blocks, in order: standard equation; three substitution/square/p rows; resulting equation; three formal-derivative/chain-factor/isolation rows. This is eight mathematical teaching rows plus the equation/formal setup blocks, not interchangeable simplified copies. Parenthetical/braced source square spelling is conditional, as are standard/general wording and raw attribute omissions. No solution depends on the selected wrong option.

All profile modes obey the finite domains: integers 1≤|a|,|b|≤8, right a>0 for moderate and left a<0 for hard; authored easy a>0 and c integral. Each source bank is chosen before parameter construction. Any pairwise equivalence or ambiguity rejects the entire sampled instance; explicit inputs fail instead of resampling. No unrestricted real values, radicals, large denominators or profile bypasses. This bounds b²≤64, |4a|≤32 and the reduced p denominator≤32. The source already shows b=±8 and p=49/20, so this retains familiar source-sized arithmetic.

Source replay masks retain full prose/stage sequence, including q-342218's braced square. q-127510's `(3,6)` vertex sentence is raw-only erroneous evidence; completed output changes it to `(0,0)`. Raw q-127372/q-127374 retain absent difficulty, solution and correct refs. Completed missing attributes are explicitly authored/inferred. All decoded source fraction backslashes are single bytes; no backslash repair is needed.

Meaningful task enumeration deduplicates by the assessment demand (supplied equation or graph reconstruction) and the entire locus coefficient c; marker sign, another marked point on the same curve, symbol spelling, profile aliases and layout never inflate counts. The finite domains contain 17 easy, 56 moderate and 56 hard slope tasks. These are independent same-method instances, with no progression or added branch within a level. Easy is separated by supplying the equation and omitting graph/p reconstruction. The observed moderate/hard labels and their arithmetic overlap remain untouched.

## Authored easy equation template

Easy retains the origin/marked-point raster but states `The parabola shown above has equation`, followed by the complete y²=cx equation and the derivative request. The supplied equation is a complete component, not a short-string replacement in prose. `equation_radio` keeps five choices; `equation_blank` keeps the y-only answer fragment and field-1 placeholder. The solution repeats the supplied equation, then uses the source's shared `Finally, to calculate ... we use implicit differentiation` sentence and exactly the formal d/dx inputs, chain factor and isolation rows. No b²=4pa or p-solving appears. Every easy instance has the same three differentiation rows and integer c, so the level has no internal progression. This narrows the reasoning demand using a stage present in the canonical example and the Implicit Differentiation prerequisite, without adding a new method. The full 17 coefficient family is preserved; the validator reads the actual supplied equation independently and checks every easy coefficient in both layouts, marker-sign aliases and cross-level task distinction.

Generation metadata now records the actual calling Python version and SymPy version. Generated plots include their sidecar's actual renderer Python, Matplotlib and NumPy versions, loaded module paths and all read-only cached dependency paths. Original raster renderer dependencies remain explicitly unknown; no historical runtime is invented. These additions are outside question content and do not alter moderate/hard source replay.

## Current-source supplement at basis 2656

q-127503: moderate, point_radio, selection, marked (2,-3), p=9/8, c=9/2, derivative 9/(4y). The source uses five answers: -9y/2 = -cy; -3/(4y) = b/(2ay); 3y/4 = -by/(2a); 9/(2y) = c/y; 9/(4y) = c/(2y), designated correct. The complete bank is a separate evidence-only profile. Point-ratio recipes have unresolved intent. All solution stages and blank/radio contracts remain as above. Current q-127374 now includes difficulty, solution and correct designation; its current replay is separate from historical raw evidence. See classification-current.md and source-current.json.
