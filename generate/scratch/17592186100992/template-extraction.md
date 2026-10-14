# Moderate template extraction

Source: q-13536, math basis 2277, immutable lineage retained in reference/source.json. All source practice content, every field-owned choice, and unresolved deferred routes are recorded in source-components.json.

At the source parameters A=[[6,7],[4,5]], B=[[3,2],[2,3]], C=[[5,1],[6,8]], the prompt asks Find $(A+B)-C-(B-C)$, if, followed by one display block listing A, B and C in that order. A is the surviving matrix; B and C each cancel. All entries are nonnegative one-digit integers; the matrices are 2x2. The solution first distributes subtraction, then displays canceled terms, then identifies A, and finally displays A's numerical entries. The answer shape is a whole 2x2 matrix radio choice. The two raw fields have identical keys and complete mathematical banks, but only the newer field has a correct ref. The generated layout is an explicitly supported correction with one complete field, not a replay of the broken duplicate layout.

The fixed backbone is distribution and cancellation of two matrix pairs, leaving the first supplied matrix. Keep the expression, three matrices, symbolic roles, 2x2 shape, five-option field, and ordered solution stages fixed. Changing the surviving role, adding coefficients, adding matrix multiplication, or requiring entrywise arithmetic would change the assessed method. Matrix letters stay A/B/C to preserve the exact source notation; letter changes would be cosmetic, so they are not counted as tasks. No target-position slot exists: the requested object is the whole surviving matrix.

Slots: each of the four entries of A, B and C is an integer. Observed values are preserved for exact replay. The normal sampling policy is 0 through 9 independently, a conservative same-method generalization of the observed one-digit nonnegative entries. A's entries feed the prompt, correct answer, altered-A distractor and final solution. B and C feed the prompt and their own distractors; symbolic cancellation stays fixed. Reject the whole instance if A, B, C, zero or the altered-A option collide. Do not drop options or mix profiles to repair a collision.

The complete bank profile is:

| Recipe | Original complete value | Correct? |
|---|---|---|
| B | [[3,2],[2,3]] | no |
| A | [[6,7],[4,5]] | yes |
| 2x2 zero | [[0,0],[0,0]] | no |
| [[A00-1,A01],[A01,A11]] | [[5,7],[7,5]] | no |
| C | [[5,1],[6,8]] | no |

The fourth option's psychological interpretation is unresolved. Its complete observed expression is retained; it is never presented as a named error to learners. Both raw source banks must reproduce all five options, ignoring choice order, including four distractors each. The intact field's correct designation must match A. The legacy field's missing ref is recorded, not silently treated as verified grading.

The prompt and concrete worked solution are parameterized directly from source text. Original parameters reproduce both strings exactly. Field-owned UUIDs derive from full prompt parameters and profile; question identities are independent of seed and choice order. A separate mathematical task fingerprint uses only the fixed expression and A. Changes to canceled matrices or option order therefore cannot replenish the inventory by themselves. Compare against source and current generated tasks before adding any questions.

Validation uses exact SymPy matrices, an independent parser of the rendered prompt and options, independent evaluation of (A+B)-C-(B-C), full bank replay, per-slot coverage of 0..9, fixed-role checks, changed-A cases holding B/C constant, solution and key corruption checks, and the existing application grade_field entry point. Radio submissions are tested against every owned answer, not by scalar algebra alone. Review source and variants side by side in review.md before database preparation.

Easy and hard are outside this version. The easy bank profiles and blank grading require their own extraction and validation before implementation. This bounded implementation exception keeps their shortages explicit.
