# Source templates and complete banks

Each original question is retained verbatim in source.json, with all field-owned choices and IDs. source-components.json records every original option, its exact symbolic recipe and whether it reproduces that source value. Complete source bank replay is separate from correctness and grading evidence.

| Template / source | Original parameters and response | Complete bank recipes (unordered; correct bold) | Domain and sampling |
|---|---|---|---|
| scale-radio / q-11930 | a=8; derivative of ln(ax); selection radio | a/x, a ln(ax), 1/ln(ax), **1/x**, 1/(ax) | x>0, original only; scale variants collapse |
| power-radio / q-11932 | n=2; derivative of ln(xⁿ); selection radio | n x^(n−1) ln(xⁿ), 1/x, n/xⁿ, **n/x**, 1/xⁿ | n=2..21; x≠0 for even n, x>0 for odd n |
| polynomial-blank / q-341676 | ln(3−5x⁶); field-1 expects derivative RHS | **−30x⁵/(3−5x⁶)**; no distractors | 3−5x⁶>0; original only |
| scale-blank / q-341671 | a=9; field-1 expects derivative RHS | **1/x**; no distractors | x>0; original only, same mathematical task as scale-radio |
| slope-polynomial / q-310144 | a=5 in ln(ax²+4); x=1; field-1 expects m | **2a/(a+4)**; no distractors | all real x; a=1..20 |
| slope-affine / q-341679 | b=7 in ln(b−4x); x=−1; field-1 expects m | **−4/(b+4)**; no distractors | x<b/4; b=1..20 |
| tangent-origin / q-150014 | a=3 in ln(ax+1); x=0; selection radio | ax+1, **ax**, x, x+a, ax+ln a | x>−1/a; a=2..21 |
| tangent-shift / q-150015 | t=1 in ln(t+1−x); x=t; selection radio | x+t, x−t, **−x+t**, −x, 2x | x<t+1; t=1..20 |
| tangent-scaled / q-48654 | c=4 in c ln(2x); x=c; selection radio | 2x−c/2−ln(2c), 2x−2c+c ln(2c), x−c, **x−c+c ln(2c)**, x+c | x>0; c=2..21 |

The bank expressions are observed patterns, not claims about a learner's reasoning. In particular the scaled-tangent −c/2 expression extends the observed −2 constant and its interpretation is unresolved. This declared sparse-evidence extension is never mixed with another bank. Whole equations are compared through their y−RHS residual with fixed coefficient of y, so multiplication-equivalent equations denote the same line.

The generator computes the correct derivative, slope or tangent first. Variants retain the source composite-function, separate differentiation, chain-rule, then optional evaluation and point-slope sequence and the original instructional sentences. Source parameters replay original prompts and banks exactly; non-source notation is rendered with SymPy. Source duplicated aligned environments in numeric-slope solutions are normalized. q-11930's source calls f “g” once; preserved in replay, flagged as a wording error, not propagated to new variants.

All proposed ranges are bounded policies, not inferred source support across every integer. No new bank, field shape, feedback or image is introduced. Original-only templates are replayed and tested, but are never expanded by superficial coefficient changes.
