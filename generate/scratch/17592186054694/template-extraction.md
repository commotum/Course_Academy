# Extracted templates and bank profiles

Three Markdown/solution-layout templates preserve their original prompt, table alignment and selection field. Fixed: x=0,1,2,3, empty table, graph selection, five images, one selection key. Variable: intercept b, expression y=mx+b, four substituted expressions and values, completed table, graph geometry. Original substitution/points/connected-line sentences are retained in the two complete source templates. The incomplete negative template uses q-54397's solution wording as an explicitly authored extension. No added distractor feedback. Domain x,y real; m and b integral in this package, nonzero.

Ordered complete banks below specify (slope, intercept) of each graph. These are parameterized observed-expression patterns, not established psychological explanations:

| Profile | Original parameters | Ordered bank recipes | Correct index |
|---|---|---|---:|
| q-54397 | m=1,b=-2 | (-m,0), (m,b), (-m,-b/2), (m,-b), (m,0) | 2 |
| q-59676 | m=-1,b=1 | (m,2b), (-m,-2b), (-m,-b), (2m,4b), (m,b) | 5 |
| q-71695 | m=2,b=2 | (m,-b), (-m,b), (-m/2,b), (m,b), (m/2,b) | 4 |

Every original option is mapped in source-choice-mapping.json to its field, UUID, asset, observed line, two marked points, parameterized recipe, bank profile and correct designation. Source-replay.json checks all 15 values and 12 distractors, preserving choice count and source keys when supplied. Equivalent lines are compared as complete linear polynomials. Source replay reuses the original raster assets; generated plots intentionally use a documented Matplotlib style. Two complete source solutions are reproduced exactly at original parameters. The third lacks a solution/key and retains that limitation.

Sampling bounds are a conservative extension of observed intercepts: unit_positive fixes m=1 and b in {-6,-4,-2,2,4,6}; unit_negative fixes m=-1 and b in {-3,-2,-1,1,2,3}; double_positive fixes m=2 and b in {-6,-4,-2,2,4,6}. All observed parameter tuples are included. These 18 tasks have unique (m,b); no broader slope range is claimed. Canonical (3,-2) and every existing practice (m,b) are excluded before commit. Profiles never mix. Any duplicate option or extra correct option fails generation.

Correct line is calculated first; table entries are exact m*i+b. Each distractor graph uses its own recipe and table points. Question identity is derived from the exact mathematical task (m,b), with field-owned answer UUIDs based on line values. Seed, rendering style and bank order do not establish novelty. Current-pool task fingerprints are checked independently of identity before selection.
