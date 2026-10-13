# Template extraction

Each source is described individually in source.json, including exact prompt, every field and option, original solution and image. choice-recipes.json maps every original answer ID to its complete parameterized value.

Shared pattern: find the perpendicular foot on a nonhorizontal/nonvertical line and use the Euclidean distance between that foot and the given point. Moderate begins with slope-intercept form; hard adds the standard-form rearrangement. The response is one length selected from five values.

| Source/profile | A,B,C,x0,y0 in Ax+By=C | Features |
|---|---|---|
| q-114341 | [3, 2, 6, 1, -5] | integral coordinates; signed intercept and source slope preserved |
| q-114343 | [-1, 1, -2, -1, 5] | integral coordinates; signed intercept and source slope preserved |
| q-74417 | [1, 1, 2, -1, -3] | integral coordinates; signed intercept and source slope preserved |
| q-74420 | [-1, 3, -9, 5, -8] | integral coordinates; signed intercept and source slope preserved |
| q-114358 | [5, 2, 10, -5, 3] | integral coordinates; signed intercept and source slope preserved |
| q-114364 | [3, 2, -6, 2, '1/2'] | fractional y0, negative intercept |
| q-74435 | [2, 1, -2, -3, -6] | integral coordinates; signed intercept and source slope preserved |

Parameter k is an integer 1..9. Replace C,x0,y0 by k*C,k*x0,k*y0. Slopes remain fixed; perpendicular intercept, foot coordinates and distance scale by k. Every option is the whole source mathematical value multiplied by k, including opaque options such as 25. These are observed expressions with unresolved mistake interpretations, not inferred pedagogical error recipes. Bank conditions are exactly the original source profile and this bounded dilation. At k=1 replay all original choices with their correct designation; at k>=2 retain their cardinality and check distinctness. Each original option must match exactly one generated mathematical value.

Markdown retains the source instructional sentences and sequence: optional rearrangement, diagram, negative reciprocal, point-slope equation, intersecting system, solve x, substitute y, distance formula, conclusion. At k=1 the original source layout is retained. At k>1 numeric alignments are explicitly normalized into one consistent layout; intermediate simplification line counts are not claimed to be byte-for-byte source fidelity. Values are delimiter-free LaTeX; generated choice UUIDs belong to their field.

Exact calculations: m=-A/B, b=C/B, n=-1/m, c=y0-n*x0, h=(c-b)/(m-n), j=m*h+b, d=sqrt((h-x0)^2+(j-y0)^2). Independently validate d=abs(A*x0+B*y0-C)/sqrt(A^2+B^2). All geometry is over the real Euclidean plane, slopes nonzero; k>0, distance positive. No branches or inequalities are lost.

Source error q-114358: -5/2-2/5=-29/10, but the source renders +29/10 in its zero RHS equation. Its foot and distance are still correct. Generated source replay corrects that sign and retains the raw original. q-74437 has a malformed system delimiter and no answer fields; excluded rather than fabricating its bank. The two unrated incomplete banks remain unchanged.

Novelty is the normalized entire line and point, excluding equivalent equations and all current/canonical geometries. Seed, bank order and authored identity never determine novelty. Positive dilation changes the point, line intercept, computed foot and required distance. All 56 new candidates have distinct geometry and differ from the seven replay instances.
