# Four-stage template extraction

## 1. Specific originals

q-54286 supplies `y = 2x - 4`; q-59678 supplies `y = 1/2 x - 2`. Each has five image choices and no captured solution, grade or correct reference. Their original widget in `/home/jake/Developer/MA/DATA/Lessons/95/Source/95.json` confirms the five-choice layout and lacks those fields. No unavailable solution is invented in evidence replay. Independently reading each graph identifies the equation-matching option; normal completion is explicitly authored.

q-102054 supplies `y=-2x`, easy, and computes x=0 then x=1. Each chain retains the symbolic expression, substituted expression and evaluated result. Its actual chosen points are (0,0) and (1,−2). Shared opening prose says any two distinct points will do. Its final sentence repeats the equation and its final red line has two blue markers.

q-109055 supplies `y=2−1/2 x`, easy, and computes x=0 then x=8. Each chain retains expression, substitution, evaluated product and subtraction, collected value. Its actual points are (0,2), (8,−2). It uses the same shared prose, then a red line with two blue markers. Its constant-first order is retained.

## 2. Shared purpose

Given an explicit linear equation, calculate two distinct points by substitution and select the matching complete line graph. The learner response is one field-owned radio image choice; one concrete solution is independent of the selected wrong answer. Omitted source feedback remains omitted.

## 3. Components and every original option

Pairs denote the complete line `y=a x+c`. The first pair is not necessarily correct. Each row maps the original source field's stored option order; `contract.json` includes exact paths, and `source-plot-inspection.json` independently calibrates every image occurrence with its own origin and grid scale. Equality compares complete equations up to nonzero rescaling, not separate equation sides.

| Profile | Original ordered whole lines | Correct position | Parameterized whole bank |
|---|---|---|---|
| q-54286 | (2,−4), (−2,4), (2,4), (1/2,−2), (−1/2,2) | 0, inferred only | (m,b), (−m,−b), (m,−b), (m/4,b/2), (−m/4,−b/2) |
| q-59678 | (−1/2,4), (1/2,−2), (−1,2), (1,0), (2,−4) | 1, inferred only | (−m,−2b), (m,b), (−2m,−b), (2m,0), (4m,2b) |
| q-102054 | (2,−2), (−2,2), (−1,0), (−2,0), (2,0) | 3, captured | (−m,m), (m,−m), (m/2,0), (m,0), (−m,0) |
| q-109055 | (1/2,−2), (−1/2,4), (−1/2,2), (1/2,0), (−1/2,0) | 2, captured | (−m,−b), (m,2b), (m,b), (−m,0), (m,0) |

Original intent behind compound transformations such as simultaneous coefficient/intercept scaling is opaque; an exact geometric reconstruction does not recover author psychology. All historical complete profiles remain public evidence-only. Normal banks are independently authored from substitution errors: negate coefficient, negate shift, negate both, combine coefficient and shift before multiplication; homogeneous profiles omit/negate/halve/double/reciprocate the coefficient. The unit-slope homogeneous profile uses zero from omitted multiplication instead of a colliding reciprocal. A complete eligible profile is chosen first, then its parameter domain; the whole bank is rejected if any two full lines coincide.

## 4. Reusable backbone and slots

Fixed roles: given equation; five plotted complete lines; first chosen x=0; second chosen x≠0; ordered equation/substitution/product-plus-shift/result stages for each point (three rows when no shift); explicit first/second point tuples; draw the line; final equation and graph. No table or supplied-point unknown-line task is introduced.

Variable numerical slots m, b, x2 are exact rationals. Easy allows signed integer coefficient magnitude ≤4 or unit numerator over 2–4, integer shift magnitude ≤4, and x2 equal to signed one/two denominator multiples; point magnitude ≤14. Moderate retains denominator 2–4 with reduced numerator magnitude 2–5 and nonzero integer shift ≤4. Hard retains those coefficient bounds with shift of denominator exactly 2, magnitude ≤4. All actual x2 values remain signed denominator multiples; first-point and second-point y denominators are asserted from the displayed calculation. Layout may retain coefficient-first or constant-first masks with the same meaning; it does not create a new mathematical task.

Every dependent prompt, substitution, reduced product, tuple, final equation and graph is constructed from the same slots. No blind string replacement drives changed-parameter generation. Exact original parameters use original raster assets only after the independent whole-line reconstruction; the original source chains are reproduced through these parameterized masks, not returned verbatim as a solution branch. Normal output always uses Matplotlib.

Content identity depends on actual prompt, concrete solution, complete unordered displayed bank and level. Mathematical fingerprints include the supplied equation, fixed two-forward-substitution point roles and actual reading grid/difficulty; exclude the freely chosen solution-only second x, layout aliases, axis bounds, profile names and choice order. Distinct graph-selection task counts deduplicate that solution slot as well as layout aliases. Fixed parameters plus reordered choices or seed changes retain identity. Changed second point cases verify all references independently.
