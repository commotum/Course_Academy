# Scalar recovery templates

The five supported templates supply two matrices related by kA=B and request the scalar k. The learner scales A entry by entry, equates it to B, chooses corresponding nonzero entries, and solves one linear equation. Source questions, fields, exact banks, original parameters and concrete solutions are preserved in source.json and source-questions.md. Canonical e-4381 corroborates reciprocal scaling, but is never practice inventory.

| Source | Supplied A | Scalar | Target in source | Field | Bank profile |
|---|---|---|---|---|---|
| q-981 | [-1,-3,8] | 7 | leftmost | radio selection, five equations | k-3, k, k-1, k-4, k-2 |
| q-69670 | [-9,4;0,8] | -7 | top-left | radio selection, five equations | k+5, 0, k, k+4, k+1 |
| q-320536 | [11,12;-4,-8] | 3 | bottom-left | blank field-1, scalar only | no distractors |
| q-320551 | [1,0,0;0,4,-3;2,-2,5] | 5 | third-row leftmost | blank field-1, scalar only | no distractors |
| q-320563 | [24,-12,6] | 1/3 | rightmost | blank field-1, scalar only | no distractors |

Keep row radio and square radio separate, and each blank shape/number form separate. No profile pooling. choice-recipes.json assigns every original option and its exact offset or fixed zero recipe; the interpretation of these authored numerical offsets as particular student mistakes is unresolved. Both complete banks replay exactly as mathematical equations, ignoring whitespace and order. Every sampled bank must contain five distinct equations, exactly one of which solves all matrix entries.

Fixed backbone: original dimensions, matrix letter, original zero positions and entry signs, source prompt and blank/radio contract, complete profile, and ordered solution wording. Keeping dimensions, zero/sign patterns, and integer versus reciprocal scalar form preserves each source workload. Source labels remain fixed because letter changes provide no mathematical novelty. There are no plots: matrices are notation.

Variable slots: each nonzero coefficient keeps its source sign and independently varies in magnitude 1..12. Positive integer scalars vary 2..9 for square blanks, 5..9 for q-981 (ensures its four offset distractors remain positive and distinct); negative scalars vary -9..-6 for q-69670 (avoids its fixed zero colliding with offsets). The reciprocal row blank uses k=1/d with d=2..6 and coefficients d times independently sampled signed integers 1..12. Original defaults remain replayable even outside sampling bounds. These are conservative same-method numeric generalizations, not an observed source parameter distribution.

A solution target can be any nonzero cell, with identical numeric data held fixed during target tests. Replacing the target preserves its role: choose corresponding nonzero entries and solve the same scalar equation. The source target phrase is retained at its original location; other positions use explicit row/column references. The inline entries, final equation, matrices and key all derive from one instance. A target-only change never establishes novelty. No new matrix operations, response formats, equation stages or higher difficulty bands are introduced.

Source error: q-320536's first two solution matrices contain +4 and +4k where the supplied matrix, scaled matrix and final equation require -4 and -4k. Correct those two displayed signs in generated content only. Replay checks use this explicit correction. q-11442 is unrated with no key or solution. q-139431 depends on absent matrix P; neither is accepted as a standalone template. Source identities and learner history remain untouched.

Identity is UUIDv5 over generator identity and complete authored content, with field-owned answer UUIDs. Novelty is checked separately using source and scaled matrices normalized by the first nonzero source entry: uniform scaling, target position, seed, label and choice order do not create fresh inventory. A different scalar or genuinely different matrix ratios changes mathematical content.
