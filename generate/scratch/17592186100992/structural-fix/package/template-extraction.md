# Moderate template extraction

Source: q-13536, math basis 2277, immutable lineage retained in reference/source.json. All source practice content, every field-owned choice, and unresolved deferred routes are recorded in source-components.json.

At the source parameters A=[[6,7],[4,5]], B=[[3,2],[2,3]], C=[[5,1],[6,8]], the prompt asks Find $(A+B)-C-(B-C)$, if, followed by one display block listing A, B and C in that order. A is the surviving matrix; B and C each cancel. All entries are nonnegative one-digit integers; the matrices are 2x2. The solution first distributes subtraction, then displays canceled terms, then identifies A, and finally displays A's numerical entries. The answer shape is a whole 2x2 matrix radio choice. The two raw fields have identical keys and complete mathematical banks, but only the newer field has a correct ref. The generated layout is an explicitly supported correction with one complete field, not a replay of the broken duplicate layout.

The fixed backbone is distribution of subtraction, cancellation of two matrix pairs, and identification of one surviving matrix. Version 3 varies the expression structure and the assignments of the surviving and canceled roles. This is an explicitly supported generalization of q-13536, authorized by the user's request to fix the constant-answer shortcut. It preserves three 2x2 matrices, five signed occurrences, unit coefficients, a five-choice radio field, and the ordered solution stages. It adds no matrix multiplication or entrywise arithmetic.

The six structures, written with X as the surviving role, are `(X+Y)-Z-(Y-Z)`, `(Y-Z)-(Y-X)+Z`, `Y-(Z-X)-(Y-Z)`, `(Y+X)-(Z+Y)+Z`, `Y-(Z+Y)+(Z+X)`, and `(Z+Y)-(Z-X)-Y`. Each has all six assignments of A/B/C to X/Y/Z. Given matrices remain displayed in A/B/C order, so neither the first displayed matrix nor the first expression operand is always correct. The surviving role can be inside a subtracted group. All 36 cases are tested with the same numeric matrices.

Numeric slots remain independently sampled integers 0 through 9. The source bank recipes follow mathematical roles: Y, X, zero, the altered-X matrix, and Z. Reject the whole instance if choices collide. The altered-X recipe retains the source's unexplained distractor rule; its psychological interpretation is not claimed. Source replay explicitly selects structure 0 and roles ABC.

The complete bank profile is:

| Recipe | Original complete value | Correct? |
|---|---|---|
| B | [[3,2],[2,3]] | no |
| A | [[6,7],[4,5]] | yes |
| 2x2 zero | [[0,0],[0,0]] | no |
| [[A00-1,A01],[A01,A11]] | [[5,7],[7,5]] | no |
| C | [[5,1],[6,8]] | no |

The fourth option's psychological interpretation is unresolved. Its complete observed expression is retained; it is never presented as a named error to learners. Both raw source banks must reproduce all five options, ignoring choice order, including four distractors each. The intact field's correct designation must match A. The legacy field's missing ref is recorded, not silently treated as verified grading.

The prompt, distributed terms, cancellation marks, final surviving label, numerical answer and answer key all derive from the sampled expression. Source replay reproduces the original expression, worked solution and both complete mathematical option banks; the duplicate incomplete field remains excluded. Matrix layout uses the shared renderer.

Question identities include expression, profile, role assignment and numeric parameters. With those fixed, seed changes affect only choice order. The task fingerprint uses the expression and surviving matrix; changing only canceled matrix entries does not count as a new task.

`validate.py` independently reads the displayed expression through SymPy, checks every solution equality and cancellation, evaluates all choices, and exercises the native grader. It tests all 36 structure/role combinations with fixed matrices, 600 seeded questions, all three surviving labels within every structure, numeric bounds, source replay, identity stability, invalid choices, and deliberately corrupted keys, expressions and solutions. Current evidence is in `structural-fix/`; earlier evidence files describe version 2. Use the shared Publisher for new publication; `replenish.py` is the historical version-2 replenishment script.

Easy and hard remain outside this generator's supported scope.
