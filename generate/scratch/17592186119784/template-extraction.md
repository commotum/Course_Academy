# Template extraction — basis 1356

The four stages below separate observed source masks from authored extension. `template-extraction.json` carries every bank value/subset recipe and source ID; `review.md` displays each whole original and changed-parameter variant. No distractor diagnoses have been invented.

## 1. Describe each source before generalizing

### q-42091

Observed level: :question.difficulty/moderate. Matrix [[4, 0, 0], [2, 1, 0], [0, 5, 3]]; signed integer entries, square dimension 3. Prompt uses unlabelled bullets; semantic statement positions are I/II/III. Complete statement expressions: I: $A$ is upper triangular; II: $A$ is lower triangular; III: ${A}^{T}$ is upper triangular.

One field: key `selection`, type `:answer-field.type/radio`, five text answers. Solution starts “Let's analyze each statement in turn.”, has three ordered statement/proof/matrix stages, and ends with the whole true subset. Each repeated A/B/C/D stage is a complete parameter slot.

### q-42115

Observed level: absent (unrated). Matrix [[-3, 1, 0], [-1, 1, 0], [0, 0, 5]]; signed integer entries, square dimension 3. Prompt uses numbered 1/2/3; semantic statement positions are I/II/III. Complete statement expressions: I: $A$ is upper triangular; II: $A^{T} + A$ is upper triangular; III: $A$ is lower triangular.

One field: key `selection`, type `:answer-field.type/radio`, five text answers. No correct ref, solution or difficulty attribute is present.

### q-126477

Observed level: :question.difficulty/hard. Matrix [[2, 0, 0, 0], [0, -3, -1, 1], [0, 0, 4, 5], [0, 0, 0, 2]]; signed integer entries, square dimension 4. Prompt uses unlabelled bullets; semantic statement positions are I/II/III. Complete statement expressions: I: $B$ is upper triangular; II: $B$ is lower triangular; III: $B-{B}^{T}$ is upper triangular.

One field: key `selection`, type `:answer-field.type/radio`, five text answers. Solution starts “Let's analyze each statement in turn.”, has three ordered statement/proof/matrix stages, and ends with the whole true subset. Each repeated A/B/C/D stage is a complete parameter slot.

### q-126479

Observed level: :question.difficulty/moderate. Matrix [[5, 0, 0], [0, -2, 0], [0, 0, -5]]; signed integer entries, square dimension 3. Prompt uses unlabelled bullets; semantic statement positions are I/II/III. Complete statement expressions: I: $C$ is upper triangular; II: $C$ is lower triangular; III: ${C}^{T}$ is upper triangular.

One field: key `selection`, type `:answer-field.type/radio`, five text answers. Solution starts “Let's analyze each statement in turn.”, has three ordered statement/proof/matrix stages, and ends with the whole true subset. Each repeated A/B/C/D stage is a complete parameter slot.

### q-126484

Observed level: :question.difficulty/moderate. Matrix [[3, 0, 0], [0, -2, 0], [0, 4, 5]]; signed integer entries, square dimension 3. Prompt uses unlabelled bullets; semantic statement positions are I/II/III. Complete statement expressions: I: $B$ is upper triangular; II: $B$ is lower triangular; III: ${B}^{T}$ is lower triangular.

One field: key `selection`, type `:answer-field.type/radio`, five text answers. Solution starts “Let's analyze each statement in turn.”, has three ordered statement/proof/matrix stages, and ends with the whole true subset. Each repeated A/B/C/D stage is a complete parameter slot.

### q-13771

Observed level: :question.difficulty/hard. Matrix [[8, 0, 0], [0, 1, 0], [0, 0, 3]]; signed integer entries, square dimension 3. Prompt uses Roman paragraphs; semantic statement positions are I/II/III. Complete statement expressions: I: $A$ is upper triangular; II: $A$ is lower triangular; III: ${A}^{T}+A$ is lower triangular.

One field: key `selection`, type `:answer-field.type/radio`, five text answers. Solution starts “Let's analyze each statement in turn.”, has three ordered statement/proof/matrix stages, and ends with the whole true subset. Each repeated A/B/C/D stage is a complete parameter slot.

### q-42116

Observed level: :question.difficulty/hard. Matrix [[7, 0, 0], [-2, 0, 0], [0, 1, 1]]; signed integer entries, square dimension 3. Prompt uses unlabelled bullets; semantic statement positions are I/II/III. Complete statement expressions: I: $A$ is lower triangular; II: ${A}^{T}-A$ is lower triangular; III: $A$ is upper triangular.

One field: key `selection`, type `:answer-field.type/radio`, five text answers. Solution starts “Let's analyze each statement in turn.”, has three ordered statement/proof/matrix stages, and ends with the whole true subset. Each repeated A/B/C/D stage is a complete parameter slot.

### q-68754

Observed level: :question.difficulty/hard. Matrix [[0, -2, -7], [2, -1, 8], [7, -8, 1]]; signed integer entries, square dimension 3. Prompt uses unlabelled bullets; semantic statement positions are I/II/III. Complete statement expressions: I: $A$ is upper triangular; II: $A$ is lower triangular; III: $A+{A}^{T}$ is upper triangular.

One field: key `selection`, type `:answer-field.type/radio`, five text answers. Solution starts “Let's analyze each statement in turn.”, has three ordered statement/proof/matrix stages, and ends with the whole true subset. Each repeated A/B/C/D stage is a complete parameter slot.

### q-74318

Observed level: :question.difficulty/moderate. Matrix [[2, 0, 1, 0], [0, 4, 0, 4], [0, 0, 2, 1], [0, 0, 0, 3]]; signed integer entries, square dimension 4. Prompt uses unlabelled bullets; semantic statement positions are I/II/III. Complete statement expressions: I: $C$ is upper triangular; II: $C$ is lower triangular; III: ${C}^{T}$ is upper triangular.

One field: key `selection`, type `:answer-field.type/radio`, five text answers. Solution starts “Let's analyze each statement in turn.”, has three ordered statement/proof/matrix stages, and ends with the whole true subset. Each repeated A/B/C/D stage is a complete parameter slot.

### q-74319

Observed level: :question.difficulty/moderate. Matrix [[3, 0, 0], [0, 2, 0], [1, 0, 1]]; signed integer entries, square dimension 3. Prompt uses Roman paragraphs; semantic statement positions are I/II/III. Complete statement expressions: I: $D$ is upper triangular; II: $D$ is lower triangular; III: ${D}^{T}$ is upper triangular.

One field: key `selection`, type `:answer-field.type/radio`, five text answers. Solution starts “Let's analyze each statement in turn.”, has three ordered statement/proof/matrix stages, and ends with the whole true subset. Each repeated A/B/C/D stage is a complete parameter slot.

## 2. Generalize the mathematical patterns

Moderate: inspect the appropriate full off-diagonal region for three assertions about a square matrix and its transpose. Hard: inspect three assertions including one transpose sum/difference, computing the complete transformed matrix before testing its region. Answer one complete subset of statement labels through the observed RADIO field. The mathematical response is the truth subset, not the numerical equality of any matrix or an individual boolean field. Signs and nonzero magnitudes are arbitrary within the workload bound; sum-cancellation relations must remain intact.

Easy, authored: inspect upper/lower/diagonal assertions about one fixed 3×3 matrix. This keeps three truth decisions and the same subset response while removing transpose computation. The prerequisite hierarchy supplies “diagonal” as both triangular regions zero. This is a declared new easy template, not a recovered source or a replacement for the sibling whole-matrix selection KP.

## 3. Map every component and every complete observed bank

Each profile is the source ID. Its five recipes are exact selected-label subsets. No numeric error intention is inferred: these choices encode alternative truth combinations. For every permitted matrix class the correct subset is independently recomputed and must be present once. Choice count and type are fixed. The captured per-choice UUID and DB provenance remain in source.json; local generated identities are owned by their field and determined by content. The semantic answer attributes retain key presence and exact values.

### Complete profile q-42091

| Source answer ID | Source text | Parameterized recipe | Captured designation |

| --- | --- | --- | --- |

| 09889ed6-d2de-5fbb-bdd2-918d22217e2f | III only | select fixed labels {III} after reading the three actual statements | incorrect |

| 53c62c9a-fbb1-59ec-9d4f-11753c880606 | II and III only | select fixed labels {II, III} after reading the three actual statements | correct |

| a3d8acf6-f67c-5e6c-8b18-c9f678f10367 | I only | select fixed labels {I} after reading the three actual statements | incorrect |

| b97c66bc-77e9-5cd7-a655-cec51dd0fe8b | II only | select fixed labels {II} after reading the three actual statements | incorrect |

| c954a2d8-e51e-5a97-b015-2719a69133fc | I and III only | select fixed labels {I, III} after reading the three actual statements | incorrect |

Prompt slot: complete matrix body inside its original aligned/bmatrix environment. Fixed parts: matrix label, expression order and spelling, statement predicates, prompt prose, field key/type and complete five-answer bank. Solution slots: three complete computed matrix bodies in statement order (`identity`, `transpose`, `sum`, `transpose-minus`, or `minus-transpose` as listed in JSON). Fixed solution prose and transformed-expression labels remain shared. See the exact source stage text and its generated changed-parameter counterpart in review.md.

### Complete profile q-42115

| Source answer ID | Source text | Parameterized recipe | Captured designation |

| --- | --- | --- | --- |

| d079b31f-7956-5842-ae4d-4c8d5f7fd66a | III only | select fixed labels {III} after reading the three actual statements | missing key |

| f87e294e-b53d-5a2d-b4f7-424740def6dd | II only | select fixed labels {II} after reading the three actual statements | missing key |

| 63749c01-ff67-552d-a7aa-7aad33f51dbd | I and III only | select fixed labels {I, III} after reading the three actual statements | missing key |

| 67bea13b-8464-5256-a5c0-dbeb4526aa1b | I only | select fixed labels {I} after reading the three actual statements | missing key |

| 733d62f5-d316-5a16-ac69-e6a364d9dfa8 | None | select fixed labels {empty set} after reading the three actual statements | missing key |

Prompt slot: complete matrix body inside its original aligned/bmatrix environment. Fixed parts: matrix label, expression order and spelling, statement predicates, prompt prose, field key/type and complete five-answer bank. Solution slots: three complete computed matrix bodies in statement order (`identity`, `transpose`, `sum`, `transpose-minus`, or `minus-transpose` as listed in JSON). Fixed solution prose and transformed-expression labels remain shared. This source lacks a solution; raw replay omits it. Normal hard presentation authors the common opening, three claim/proof/matrix stages, and conclusion, deriving II only.

### Complete profile q-126477

| Source answer ID | Source text | Parameterized recipe | Captured designation |

| --- | --- | --- | --- |

| 16278a61-9875-59c1-81b4-263defc4ef28 | II only | select fixed labels {II} after reading the three actual statements | incorrect |

| 69c2515c-723d-5e1e-a869-bd9b085f59b4 | I only | select fixed labels {I} after reading the three actual statements | correct |

| 6fd7d5f2-90a4-5eca-9042-d301cd904bcb | I and II only | select fixed labels {I, II} after reading the three actual statements | incorrect |

| 92cd9da2-ef9d-596f-bc10-92a5c4144358 | III only | select fixed labels {III} after reading the three actual statements | incorrect |

| ba29aa7e-88bb-5b6f-97ad-3007774ded44 | I and III only | select fixed labels {I, III} after reading the three actual statements | incorrect |

Prompt slot: complete matrix body inside its original aligned/bmatrix environment. Fixed parts: matrix label, expression order and spelling, statement predicates, prompt prose, field key/type and complete five-answer bank. Solution slots: three complete computed matrix bodies in statement order (`identity`, `transpose`, `sum`, `transpose-minus`, or `minus-transpose` as listed in JSON). Fixed solution prose and transformed-expression labels remain shared. See the exact source stage text and its generated changed-parameter counterpart in review.md.

### Complete profile q-126479

| Source answer ID | Source text | Parameterized recipe | Captured designation |

| --- | --- | --- | --- |

| 0f1d2a35-75de-531a-afc6-ee0466ce76a5 | I only | select fixed labels {I} after reading the three actual statements | incorrect |

| 93cc1d25-eaa9-5fa8-a0c2-363186e0bfc2 | III only | select fixed labels {III} after reading the three actual statements | incorrect |

| bda955fa-4906-51a8-bbac-2912e8022dc8 | I, II, and III | select fixed labels {I, II, III} after reading the three actual statements | correct |

| d6a897df-4aa3-5e4b-aa2a-0e82a6043069 | II and III only | select fixed labels {II, III} after reading the three actual statements | incorrect |

| ff35400f-1bd2-549b-b182-cb1f0a9054d3 | I and III only | select fixed labels {I, III} after reading the three actual statements | incorrect |

Prompt slot: complete matrix body inside its original aligned/bmatrix environment. Fixed parts: matrix label, expression order and spelling, statement predicates, prompt prose, field key/type and complete five-answer bank. Solution slots: three complete computed matrix bodies in statement order (`identity`, `transpose`, `sum`, `transpose-minus`, or `minus-transpose` as listed in JSON). Fixed solution prose and transformed-expression labels remain shared. See the exact source stage text and its generated changed-parameter counterpart in review.md.

### Complete profile q-126484

| Source answer ID | Source text | Parameterized recipe | Captured designation |

| --- | --- | --- | --- |

| 0af9aa7f-a7bf-5d4a-a8bd-bb821d3e7b58 | I and II only | select fixed labels {I, II} after reading the three actual statements | incorrect |

| 28d8ac93-4b75-5896-9a82-f0496d3ca6e0 | I only | select fixed labels {I} after reading the three actual statements | incorrect |

| 2de84256-eda7-51b0-9e39-5ddd3f1fe62c | III only | select fixed labels {III} after reading the three actual statements | incorrect |

| 8938a01a-ae24-581d-82c9-76cbbf2080d2 | I and III only | select fixed labels {I, III} after reading the three actual statements | incorrect |

| a0565217-a3d6-5235-85e3-63961a7fa4d1 | II only | select fixed labels {II} after reading the three actual statements | correct |

Prompt slot: complete matrix body inside its original aligned/bmatrix environment. Fixed parts: matrix label, expression order and spelling, statement predicates, prompt prose, field key/type and complete five-answer bank. Solution slots: three complete computed matrix bodies in statement order (`identity`, `transpose`, `sum`, `transpose-minus`, or `minus-transpose` as listed in JSON). Fixed solution prose and transformed-expression labels remain shared. See the exact source stage text and its generated changed-parameter counterpart in review.md.

### Complete profile q-13771

| Source answer ID | Source text | Parameterized recipe | Captured designation |

| --- | --- | --- | --- |

| 12389f18-052b-519d-9a2a-b2d04cff0ce4 | II and III only | select fixed labels {II, III} after reading the three actual statements | incorrect |

| 522bdf1e-83a7-5e64-a119-0ea3f50e57df | I, II, and III | select fixed labels {I, II, III} after reading the three actual statements | correct |

| 86da3a70-ff02-5856-bfe6-bfd52e0aa79a | I and II only | select fixed labels {I, II} after reading the three actual statements | incorrect |

| 8a4628c9-3834-5295-8683-2196b83efb01 | I only | select fixed labels {I} after reading the three actual statements | incorrect |

| 9368856a-1f6b-5077-95c9-62f7f1fdb0de | I and III only | select fixed labels {I, III} after reading the three actual statements | incorrect |

Prompt slot: complete matrix body inside its original aligned/bmatrix environment. Fixed parts: matrix label, expression order and spelling, statement predicates, prompt prose, field key/type and complete five-answer bank. Solution slots: three complete computed matrix bodies in statement order (`identity`, `transpose`, `sum`, `transpose-minus`, or `minus-transpose` as listed in JSON). Fixed solution prose and transformed-expression labels remain shared. See the exact source stage text and its generated changed-parameter counterpart in review.md.

### Complete profile q-42116

| Source answer ID | Source text | Parameterized recipe | Captured designation |

| --- | --- | --- | --- |

| 017114c3-a1a2-5d5e-aec5-f7291e21000d | None | select fixed labels {empty set} after reading the three actual statements | incorrect |

| 23edc6a5-133c-5266-b6f2-96c0c94a31f8 | II only | select fixed labels {II} after reading the three actual statements | incorrect |

| 65328dfd-ddc6-512e-aa6e-ec778103ab31 | I and II only | select fixed labels {I, II} after reading the three actual statements | incorrect |

| d3ce84b6-e829-50fb-8784-7ae9dd928eec | I only | select fixed labels {I} after reading the three actual statements | correct |

| f204210a-2a56-5ba1-bb31-fca5ab8c400d | I and III only | select fixed labels {I, III} after reading the three actual statements | incorrect |

Prompt slot: complete matrix body inside its original aligned/bmatrix environment. Fixed parts: matrix label, expression order and spelling, statement predicates, prompt prose, field key/type and complete five-answer bank. Solution slots: three complete computed matrix bodies in statement order (`identity`, `transpose`, `sum`, `transpose-minus`, or `minus-transpose` as listed in JSON). Fixed solution prose and transformed-expression labels remain shared. See the exact source stage text and its generated changed-parameter counterpart in review.md.

### Complete profile q-68754

| Source answer ID | Source text | Parameterized recipe | Captured designation |

| --- | --- | --- | --- |

| 2b04cce7-f7e1-514a-bf46-6bdc2f41e305 | I only | select fixed labels {I} after reading the three actual statements | incorrect |

| 3a4005dd-77d3-5d4b-a72c-2cf5db39a286 | II only | select fixed labels {II} after reading the three actual statements | incorrect |

| 52569706-e3d9-5a3d-bc15-02a4fd34fdec | II and III only | select fixed labels {II, III} after reading the three actual statements | incorrect |

| 60d691ce-29b6-5220-898b-1b6a3afe6708 | I and II only | select fixed labels {I, II} after reading the three actual statements | incorrect |

| 613a72a0-7650-5c25-bf03-340b66e2443b | III only | select fixed labels {III} after reading the three actual statements | correct |

Prompt slot: complete matrix body inside its original aligned/bmatrix environment. Fixed parts: matrix label, expression order and spelling, statement predicates, prompt prose, field key/type and complete five-answer bank. Solution slots: three complete computed matrix bodies in statement order (`identity`, `transpose`, `sum`, `transpose-minus`, or `minus-transpose` as listed in JSON). Fixed solution prose and transformed-expression labels remain shared. See the exact source stage text and its generated changed-parameter counterpart in review.md.

### Complete profile q-74318

| Source answer ID | Source text | Parameterized recipe | Captured designation |

| --- | --- | --- | --- |

| 2dbca51b-7f54-5a7a-ba5f-3d88cb4bc95a | III only | select fixed labels {III} after reading the three actual statements | incorrect |

| 55b791d8-4371-5bf9-bd1e-a54e720de779 | I and III only | select fixed labels {I, III} after reading the three actual statements | incorrect |

| 7b095170-c16f-5974-ab98-b3690a252ff3 | I and II only | select fixed labels {I, II} after reading the three actual statements | incorrect |

| caef5ea6-785c-5dcb-bc6b-8144853d5c55 | II only | select fixed labels {II} after reading the three actual statements | incorrect |

| e368e4ef-99eb-518e-bdb0-6a3a39964aef | I only | select fixed labels {I} after reading the three actual statements | correct |

Prompt slot: complete matrix body inside its original aligned/bmatrix environment. Fixed parts: matrix label, expression order and spelling, statement predicates, prompt prose, field key/type and complete five-answer bank. Solution slots: three complete computed matrix bodies in statement order (`identity`, `transpose`, `sum`, `transpose-minus`, or `minus-transpose` as listed in JSON). Fixed solution prose and transformed-expression labels remain shared. See the exact source stage text and its generated changed-parameter counterpart in review.md.

### Complete profile q-74319

| Source answer ID | Source text | Parameterized recipe | Captured designation |

| --- | --- | --- | --- |

| 34777553-5006-5f5c-9727-020effdb1863 | III only | select fixed labels {III} after reading the three actual statements | incorrect |

| 3dc969e4-1f40-5c0a-b425-d47fcc951c13 | II only | select fixed labels {II} after reading the three actual statements | incorrect |

| 961268ff-d9a5-5b91-83a8-57bc579b7229 | I only | select fixed labels {I} after reading the three actual statements | incorrect |

| c1ed66f7-ff3c-5b64-aded-bf5edcca033c | I and II only | select fixed labels {I, II} after reading the three actual statements | incorrect |

| f144d22f-284c-5b5a-bb1b-1dd2f910f9dd | II and III only | select fixed labels {II, III} after reading the three actual statements | correct |

Prompt slot: complete matrix body inside its original aligned/bmatrix environment. Fixed parts: matrix label, expression order and spelling, statement predicates, prompt prose, field key/type and complete five-answer bank. Solution slots: three complete computed matrix bodies in statement order (`identity`, `transpose`, `sum`, `transpose-minus`, or `minus-transpose` as listed in JSON). Fixed solution prose and transformed-expression labels remain shared. See the exact source stage text and its generated changed-parameter counterpart in review.md.

## 4. Extract reusable masks and guards

Observed prompt mask: source Markdown with the complete first matrix-body span replaced by `matrix(M)`. Observed solution mask: source Markdown with exactly three matrix-body spans replaced by `matrix(transform(M, op_I))`, `matrix(transform(M, op_II))`, `matrix(transform(M, op_III))`. Partial number/string substitution is never used. This preserves every source sentence, expression label, blank line and conclusion across changed parameters; masks and complete matrix stages are independently verified. Source labels and order remain literal because they do not affect mathematical variety.

Parameters are one complete square integer matrix. Every recipe fixes its source dimension. Bounds apply equally to random and explicit calls: each input entry is an integer with absolute value at most eight; booleans and extra keys are rejected. Strict upper/lower recipes require the original zero region and the same nonempty-support truth profile. Diagonal recipes require all off-diagonal entries zero. Cancellation recipes require nonempty opposite off-diagonal pairs, preserving the original sum-cancellation truth profile. A complete source bank is selected before sampling; an invalid/ambiguous instance is rejected as a whole. Raw source replay accepts changed matrices within exactly these guards, rather than returning a copied source record or a numeric lookup table.

Easy authored mask: the fixed source-style opening, LaTeX 3×3 A, question prose, and the statements upper triangular/lower triangular/diagonal. Complete bank is `{None, I only, II only, I and II only, I, II, and III}`. All 64 support masks are legal. Sampling chooses one of the four upper/lower truth classes equally before choosing its support, rather than over-weighting the 49 neither-triangular masks. Truth is computed from the displayed object; diagonal means all six off-diagonal entries zero. Solutions retain the common analysis opening, three full region proofs with the actual matrix repeated, and the derived subset conclusion. Within-level workload stays three direct property decisions; varying support never changes to another operation.

Raw omission contract: difficulty absent in q-42115 stays absent, worked solution absent stays absent, and correct ref absent stays absent. Source profiles use local enum strings and lookup refs where present; db/id and MA IDs stay in external provenance. Its raw bank matches 5/5 values but supplies zero captured designation comparisons. Completed normal q-42115 explicitly authors/infer its hard level, key and solution.

Raw-error contract: q-126477 names A incorrectly in Statement II; q-126484 names B/below incorrectly in Statement III. Evidence replay preserves exact prose. Normal variants apply minimal B and Bᵀ/above corrections, respectively; displayed matrices and original banks remain unchanged. Raw-exact solution fidelity (9/9) is reported separately from the two normal semantic repairs.

Identity/fingerprint contract: content identity includes rendered prompt, complete solution, attribute-presence/difficulty and whole bank, independent of seed and choice order. Mathematical identity includes dimension, the original off-diagonal support and assessed expression/predicate/transformed support triples, canonicalized over statement order. It excludes answer banks, aliases, matrix labels, incidental diagonal values, nonzero signs/magnitudes and unassessed transforms. Catalog deduplication therefore gives 64/78/78 rather than claiming arbitrary numeric variants are new tasks.

Plot specification: none for practice; canonical highlighted-matrix rasters were read at full resolution and recorded in plot-extraction.md. No generated image or SVG is used.

Verification separates raw full-bank/attribute/prose fidelity; independent printed matrix and truth-region mathematics; source-stage structure; finite catalog/bounds/identity; native grading. Mutation tests reject changed printed matrices, wrong intermediate truth, missing shared prose and semantically duplicate answer banks. Raw missing-key q-42115 is not claimed native graded; its completed inferred normal version is fully graded.
