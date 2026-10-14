# Template extraction

## 1. Specific source descriptions

`extraction.json` and `source-cases.json` contain every original parameter, witness cell, field key/type, full choice and source answer ID. Source evidence remains complete in `source.json`. q-11562 supplies H(2×2), J(3×3), L(4×4), with H12=1 and L14=1 as nonzero offdiagonal witnesses; only J is diagonal. q-68741 supplies M(4×4 identity), N(2×4 repeated identity columns), P(3×3 diagonal with a zero middle diagonal entry); only M is identity. q-68744 supplies F(4×4) with F13=1 and another obstruction, H(2×2 diagonal containing zero), M(3×3 diagonal); H and M are diagonal. Its H explanation contains a source double space, retained exactly. q-126222 supplies P(2×4 truncated identity), Q(4×2 dense), R(3×3) with R31=7 and another obstruction; none is diagonal. Its source P has an innocuous `\text{NBSP}` suffix, retained only in raw replay. q-68745 supplies S(4×4 diagonal), R(4×2 repeated identity rows), Y(3×3) with Y31=1 and another obstruction; only S is diagonal. Field order is R,S,Y, while prompt and solution order is S,R,Y. q-7829 supplies B(2×2 diagonal with one zero), C(2×3 truncated identity), D(5×5 identity), an inline matrix list, and no solution/key/grade.

## 2. Shared pattern and instructional purpose

Inspect the three displayed matrices independently. A diagonal matrix must be square with every offdiagonal entry zero. An identity must additionally have every diagonal entry one. Select every matrix meeting that predicate. The mathematical objects are sets of satisfying labeled matrices, not disjoint type categories. Checkbox fields encode each set membership independently; radio choices encode complete selected subsets.

## 3. Component and bank mapping

Every checkbox field's complete bank is exactly `false`, `true`; its correct value is the independently computed predicate of its matrix. Both choices are derived from that field's membership response domain, not from unrelated numeric operations. Field ownership is separate even when two fields have the same boolean value. All 30 checkbox choices and all 15 existing correct designations are mapped one-to-one.

The original q-7829 radio bank is exactly B-and-C-only, B-and-D-only, C-and-D-only, B-C-and-D, D-only. Each is rendered from its subset of three matrix-role slots; the five subsets are preserved together. B is the diagonal-one temptation, C the rectangular-shape temptation, D the actual identity. These descriptions name actual predicate omissions, not recovered learner intent. The complete bank has one correct subset and no pair of equal subsets, including wrong/wrong pairs. Raw replay omits the missing key. Completion independently derives D-only. All five original options are matched; the inferred key is outside fidelity denominators.

No feedback is present, so none is invented. Per-matrix classification, square-shape justification, offdiagonal witness or zeros assertion, optional nonidentity notice, and full-set conclusion form one fixed solution independent of the selected answer. For identity questions, positive identity explanations include square shape plus diagonal-one/offdiagonal-zero statements; rectangular rejection stops at shape; nonidentity diagonal rejection cites diagonal entries not all one. Original full prose, punctuation, blank-line stage order, and conclusion are replayed exactly.

## 4. Reusable backbone and slots

Each template fixes requested predicate, number of matrices/fields, response type, source field order, role order, obstruction count (one or two), and rectangular sparsity recipe. These roles preserve the original explanation route and complete bank eligibility. No new operations or assessment demands are introduced.

| Slot | Finite permitted values | Dependencies and restrictions |
| --- | --- | --- |
| Matrix shape | rows/columns 1..5 | Square roles use n×n; rectangular roles require unequal dimensions; offdiagonal roles require n≥2. Total entry count enforces the level band on explicit and sampled calls. |
| Diagonal entries | integers -3..7 | Arbitrary for diagonal criterion. Raw diagonal source roles stay nonidentity so the captured notice is true; identity-query wrong diagonal roles also stay nonidentity. Normal diagonal-query identity cases use the conditional identity notice. |
| Offdiagonal obstruction positions | all distinct offdiagonal cells | Exactly the source role's one/two nonzero cells; positive/negative nonzero values -3..7. Every referenced witness must be one of those actual nonzero cells. |
| Witness | any eligible nonzero offdiagonal cell | Subscript, printed value and explanation derive from that cell together. A changed-witness test keeps all matrix entries fixed. |
| Rectangular recipe | source-owned truncated identity, repeated identity rows/columns, or dense | Recipes depend on changed row/column counts. Values in dense roles are nonzero; rectangular rejection depends only on dimensions. |
| Source presentation profile | raw vs method | Raw q-7829 preserves inline spacing and missing attributes. Raw q-126222 preserves NBSP markup. Normal matrix formatting uses the shared UI helper. |

Profiles are selected before matrices are sampled. The entire instance is rejected if any role, shape, witness, workload or bank condition fails. There is no individual option replacement. The radio profile retains the genuine identity in role slot 3 and the two actual predicate failures in slots 1/2, so its full original bank stays valid.

Meaningful-task identity reads the actual displayed prompt and records shape plus only operative predicate inputs. Rectangular matrices contribute dimensions alone; square diagonal recognition contributes offdiagonal zero/nonzero masks; identity adds diagonal one/nonone masks. Diagonal values incidental to diagonal recognition, nonzero magnitudes, labels, profile aliases, seed and ordering cannot inflate capacity. Repeated equal-role slots are unordered. Full content identity separately contains version, actual difficulty presence/value, actual normalized prompt, entire fixed solution, full unordered field-owned bank, correct values or key omissions. Thus a changed witness changes presentation identity while keeping the same assessed task.

The finite semantic counts in `validation.json` enumerate per-role shapes and predicate masks analytically, combine repeated-role catalogs as unordered multisets, and enforce the whole-question cell band. They are per-template counts; their sum is not advertised as a deduplicated cross-template union. Dependency versions are recorded at runtime. There are no plots or raster assets; matrix TeX uses `scripts/question_capture/math_format.py::matrix_tex` and normalization/validation helpers. No SVG or image generator is involved.
