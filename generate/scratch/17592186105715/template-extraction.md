# Reciprocal integral templates

Instructional move: pull a real constant c out of the integral of c/x, then apply the primitive ln|x| independently on the positive and negative half-lines. The real domain excludes zero; C is arbitrary independently on each connected component. Reciprocal radicals additionally rationalize 1/sqrt(n). All supported questions use exactly one five-option radio field, key selection; no blanks or added feedback.

The exact original prompt sentences and worked steps are stored as fixed strings with explicit @@n@@ or @@a@@ / @@b@@ slots in templates.json. Original values, UUIDs, field membership, keyed choices, exact recipe expressions and source IDs are accounted for individually in source-analysis.json. source.json retains the excluded banks as well. All source command escaping is decoded for newly rendered answers, and ln notation becomes \ln; prose, integral layout, sequence and field shape remain source-derived.

| Template/profile | Parameters and coefficient | Complete bank expressions (L=ln|x|) |
|---|---|---|
| q-49097 | n=9 observed; c=1/n | L+nx+C; L/n+C (correct); nL+C; ln(n+x)+C; ln(n-x)+C |
| q-29838 | n=2 observed; c=1/sqrt(n) | sqrt(n)L/n+C (correct); sqrt(n)L+C; sqrt(n)ln(|x|+C)/n; ln(sqrt(n)|x|/n+C); ln(sqrt(n)|x|)+C |
| q-71098 | a=2,b=5 observed; c=-a/b | -aL/b+C (correct); aL/b+C; bL/a+C; -bL/a+C; aL+C |
| q-72059 | n=7 observed; c=-1/sqrt(n) | -sqrt(n)L/n+C (correct); -sqrt(n)/L+C; -L/n+C; -nL/sqrt(n)+C; -ln|sqrt(n)x|+C |

The observed expression recipes are reproduced completely; pedagogical error intent remains unresolved where the original gives no feedback. A profile is selected as a whole. No pooling, shuffling or seed changes count as a new task. A mathematical task is normalized to its exact coefficient c: different numeric representations of the same c/x are one task. Stable records include the selected bank so distinct authored banks never share identity, while inventory still counts only distinct coefficients.

Sampling bounds in capabilities.json are explicit small extensions of observed values. n>=2 prevents unit-coefficient collisions; nonsquare positive radicands preserve the observed rationalization step; reduced unequal rational numerator/denominator prevents duplicate distractors. Every bounded parameter/profile case is checked rather than selectively tested. Source bank replay compares exact mathematical expressions on both real half-lines. Correctness additionally treats antiderivatives differing only by an arbitrary constant as equivalent, which exposes the excluded integer-bank duplicates.
