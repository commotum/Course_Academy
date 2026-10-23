> Historical source extraction. Runtime sampling and identity rules were revised on 2026-10-22; see ../instructional-account.md. The complete bank recipes and source corrections below remain the replay specification.

# Two column additions in a 3x3 matrix

Each source is described without generalization in source.json (verbatim prompt, fields, bank, solution and IDs) and source-components.json (exact matrices, selected row/pivot, both multipliers, every option's full operation object and recipe). All sources supply A and B and ask for both operations that retain a supplied pivot column. The correct pair is in ascending target-column order. No operation is supplied separately. Five choices contain pairs, one radio field `selection`, two successive intermediate transformations, and a final sentence state the same pair.

Fixed backbone: dimension 3x3; two nonzero column additions using a single unchanged column; one target row becomes zero outside its nonzero pivot; both matrices supplied; the common pivot column is identified in the prompt; determine the two multipliers; show the first column update, then the second, then name both operations. Integer matrices and integer coefficients preserve the source method and easy workload. Do not introduce swaps, scaling, extra operations, blanks or new difficulty labels.

Variable slots: row r in {0,1,2}, pivot column p in {0,1,2}, input matrix A and nonzero coefficients k for the other columns. B is computed exactly from A. Row and column are roles, not fixed positions: the sources already exercise all three pivot columns and all three rows. Nonzero pivot and nonzero target row entries ensure each requested operation is nontrivial. Reject cases with a second eligible target row. Sampling uses integer background entries [-9,9], nonzero pivot chosen from {-5,-3,-2,-1,1,2,3,5}, and nonzero coefficients [-6,6]. Set target-row entries to -k*A[r,p]. This is a conservative same-method policy; original source values including coefficient -9 and entry -16 remain available for replay and are not rewritten.

Compute A[:,c]+k_c*A[:,p] for each target column, ordered ascending, to derive B, every stage, correct answer and all references. Direction language changes to left, right or both according to pivot position. Solution pivot coordinates and value change with r,p. All nine row/pivot combinations and every bank profile are tested. A changed-pivot example holds A and target row constant, derives the new B, prompt, key, target columns and stages; a stale-solution negative control must fail.

Each recipe acts on the correct coefficient pair (a,b). Let u(z)=sign(z). All pairs retain the selected target/pivot column roles. Profile order below is retained for source replay; bank comparisons ignore presentation order.

| Profile | Complete coefficient bank |
|---|---|
| q-42917 | (-b,a), (a,-u(b)), (a,-b), (a,b), (b,a) |
| q-91189 | (u(a),b), (-a,b), (a,b), (a,-b), (-b,-a) |
| q-130609 | (a,b), (b,a), (-a,b), (a,-b), (-a,-b) |
| q-130610 | (a,b), (-a,b), (-b,-a), (a,-b), (-a,-b) |
| q-130611 | (b,a), (a,b), (-a,b), (a,-b), (-a,-b) |
| q-91186 | (3a,b/3), (a,b), (-a,b), (a,-b), (b,a) |
| q-91187 | (a,-b), (3a,b/3), (a,b), (-a,b), (b,a) |
| q-91192 | (a,-b), (a,b), (b,a), (-a,b), (3a,b) |
| q-91188 | (a,-b), (1-a,-a), (-a,b), (b,a), (a,b) |

These expressions reproduce every original option. The psychological interpretation of compound recipes (3a,b/3), (1-a,-a) is unresolved; preserve the observed algebraic pattern without inventing feedback. Source replay precedes generalization. Normal sampling rejects nonintegral coefficients, zero coefficients, duplicate pairs, or a bank with anything other than one correct pair. Profiles with b/3 require divisible b. Choose the whole profile before sampling; never mix banks or truncate a pooled recipe list.

Known source errors: q-42917 has two `selection` fields, the legacy one without a correct key. Replay both complete banks but generate a single complete field. q-91187 correctly computes C2:=C2-C1 and C3:=C3-9C1 in the stages/key, then incorrectly concludes C1:=C1-C2. Generated conclusions use the verified stage operations. Preserve the original content; exclude the erroneous original from usable inventory.

Question identity includes matrix task and bank profile; field/answer UUIDs belong to the generated question and field. Task deduplication uses exact A,B matrices independently of seed, question UUID, whitespace and choice order; different profiles for the same task do not count as distinct inventory. Source and canonical tasks are excluded from fresh generation.
