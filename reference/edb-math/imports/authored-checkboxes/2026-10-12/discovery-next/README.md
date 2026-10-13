# Next-tier radio → checkbox preparation

**Committed and verified.** Three `gpt-6.1-sol` agents at high reasoning reviewed the held statements, text cases, and image cases; follow-up reviews tested ordered answers and mathematical qualifications. Of 1,696 keyed, rated candidates, **1,695 questions across 311 KPs** were converted. One remains radio. This tier has no canonical examples and no captured learner presentations or saved responses.

The nine guarded conversion transactions created **5,178 checkbox fields and 10,356 owned Boolean answers**, with source **`:agent/gpt-6.1-sol-high`**. The field enum is `:answer-field/type :answer-field.type/checkbox`. All stored answer keys are preserved semantically. Detaching the old fields retains all **10,170 original field/answer entities** and their history. Every one of the 8,475 old choices, including wrong choices, has an explicit equivalent subset mapping.

Read [plan.json](plan.json) for exact counts and eight substantive prompt diffs, [prepared-questions.csv](prepared-questions.csv) for the question/KP list, [kp-topic-membership.json](kp-topic-membership.json) for topic links, and [resolutions.json](resolutions.json) for per-question decisions, evidence, mappings and status.

## How the cases were resolved

| Review class | Questions | Resolution |
|---|---:|---|
| Ordinary text lists, named matrices and sets | 1,297 | Recover the finite selectable objects from the source; decode all combination options against that universe. |
| Text structure/source exceptions | 48 | Resolve inline Roman systems, derivative annotations, repeated or missing labels, inline integrals, and source-solution conflicts individually. |
| Previously held mathematical statements | 33 | Independent proofs resolve derivative tests, region types, path limits, level curves, linear maps, Big O and related predicates. |
| Image-related questions | 317 | Inspect all 45 image-only universes and representative reference diagrams for the remaining 272 text-based questions; preserve original asset references and recover diagram labels. |
| Ordered completion | 1 | Retain radio: a subset cannot express placement order. |

Existing database keys supply the correct selections. No study-vault key replaces a database key. No image-valued answer-option bank occurs in this tier, so the first-captured-answer-filename convention was unnecessary. Diagram ordering and unordered Pull output were not used to infer keys. Image evidence and hashes are recorded in [image review](reviews/image-cases.json).

“All” and “None” are interpreted against the actual predicate. For example, q-94462 asks which forms are **not** positive/negative definite: “None of the given forms are positive or negative definite” means selecting all three, not selecting nothing. Empty subsets remain supported, with explicit guidance when applicable. Objects absent from an old combination bank are recovered from the statement/diagram, rather than silently dropped.

The retained question is **q-48430 / `17592186329885`**, completing the intermediate value theorem in left-to-right blank order. `I, II` and `II, I` are distinct responses; checkbox conversion would collapse them. Its entities were excluded from every transaction and read back unchanged.

## Eight necessary prompt qualifications

These changes are included through problem-string CAS, in addition to consistent labels/bullets and “Select all that apply.” They clarify mathematical intent; they are not merely formatting edits. Equations, listed cases and stored keys remain unchanged.

| Questions | Clarification and reason |
|---|---|
| q-141209, q-141212, q-141218 | Specify **finite bounds and an unbounded integrand** for second-kind improper integrals. Infinite-bound integrals with poles otherwise allow competing classification conventions. |
| q-42028, q-72574 | Ask whether the **coefficient matrix** is in row echelon form. Including the constants column changes the truth vector, while the source key/solution tests the coefficient matrix. q-72575 already contains the required clarification and needs no further edit. |
| q-71391 | Ask for the complete conic equation after clearing the denominator, in the entire xy-plane. The rational function's actual level curves omit domain-excluded points, while the source key classifies the complete conics. |
| q-38300, q-38305 | Explicitly require a **linear transformation**. Being onto a line alone does not justify matrix nullity or rank-nullity arguments. |

The [semantic qualification review](reviews/semantic-qualifications.md) and [independent semantic audit](reviews/independent-semantic-audit.json) record proofs, counterexamples and before/after reasoning.

## Exact conversion transactions

The conversions were committed **one batch at a time**: capture the current database, read that group's questions and incoming learner uses, prepare its guarded request, preview it with native validators, submit those exact bytes, and validate the receipt before preparing the next group. Actual conversion bases span **1774 → 1834**; external writes between groups are allowed. The separate correction transaction finished at **1835**. Ten database transactions were submitted by this migration.

The [execution plan](execution-plan.json), [commit receipts](commit-receipt.json), and [final readback verification](verification.json) are authoritative. Historical cohort preparations in `plan.json` and archived speculative chains do not override committed receipts.

| Batch | Questions | Confirmed bases | Files |
|---|---:|---|---|
| 1 | 195 | 1774 → 1775 | [EDN](batch-01/transaction.edn) / [receipt](batch-01/commit-receipt.json) |
| 2 | 195 | 1775 → 1776 | [EDN](batch-02/transaction.edn) / [receipt](batch-02/commit-receipt.json) |
| 3 | 195 | 1825 → 1826 | [EDN](batch-03/transaction.edn) / [receipt](batch-03/commit-receipt.json) |
| 4 | 195 | 1826 → 1827 | [EDN](batch-04/transaction.edn) / [receipt](batch-04/commit-receipt.json) |
| 5 | 195 | 1827 → 1828 | [EDN](batch-05/transaction.edn) / [receipt](batch-05/commit-receipt.json) |
| 6 | 195 | 1828 → 1829 | [EDN](batch-06/transaction.edn) / [receipt](batch-06/commit-receipt.json) |
| 7 | 195 | 1829 → 1830 | [EDN](batch-07/transaction.edn) / [receipt](batch-07/commit-receipt.json) |
| 8 | 195 | 1832 → 1833 | [EDN](batch-08/transaction.edn) / [receipt](batch-08/commit-receipt.json) |
| 9 | 135 | 1833 → 1834 | [EDN](batch-09/transaction.edn) / [receipt](batch-09/commit-receipt.json) |
Each complete question conversion is atomic. The prepared requests retain exact EDN hashes, stable UUIDs, source, lineage, request keys and required basis guards. [Preview results](preview.json) verify native validators, exact assertions/retractions, tempids and every datom's provenance. Prospective identities were checked absent at the captured basis.

## Verification

The current native grading engine passed **36,246 field checks** (19,327 accepted; 16,919 rejected), plus whole-question checks for all 1,695 canonical responses, 5,178 single-checkbox flips, 1,695 incomplete responses, and all **8,475 mapped original choices**. See [engine report](engine-report.json), [native build](native-build.json), and [fixture-to-final-plan verification](engine-fixture-verification.json).

These checks establish representation and grading preservation. They do not independently recalculate every question's mathematics. Mathematical proofs are recorded for the held/exception cases, 300 matrix atoms, and the semantic ambiguities; ordinary cases rely on the existing key and source evidence. No unresolved migration decision remains in this tier.

## Separate worked-solution corrections

A separately submitted and verified transaction corrected **14 definite errors**, without changing any answer key, field, prompt, rating, membership or learner state. Its [plan](optional-solution-repairs/plan.json) includes complete before/after strings, and its [EDN](optional-solution-repairs/transaction.edn), [exact request](optional-solution-repairs/prepared-request.json), and [native preview](optional-solution-repairs/preview.json) were retained alongside its confirmed commit receipt. These corrections address established content errors.

| MA question | Database ID | Correction |
|---|---:|---|
| q-2459 | 17592186064639 | Replace the out-of-universe label VI with IV. Source statement order, exact derivative proof and final answer all establish IV. |
| q-71892 | 17592186129841 | In the type-II description replace the middle y in -sqrt(1-y)<=y<=sqrt(1-y) with x. The horizontal interval is for x. |
| q-2469 | 17592186290566 | Replace the out-of-universe label VI with IV. Source statement order, exact derivative proof and final answer all establish IV. |
| q-2471 | 17592186290567 | Replace the out-of-universe label VI with IV. Source statement order, exact derivative proof and final answer all establish IV. |
| q-334851 | 17592186308693 | Remove the stray +1 in the restated function, change statement II verdict to false, and replace incorrect signed/two-sided infinity claims with absolute-ratio unboundedness. Existing prompt and key are correct. |
| q-335020 | 17592186308716 | Change statement III's introductory verdict from true to false. Its displayed divergent ratio and conclusion already prove not O(1), agreeing with the existing I-only key. |
| q-71402 | 17592186373132 | From 3y=-9x+c+4, the intercept is (c+4)/3, not /9; likewise the c=0 intercept is 4/3. Shapes and existing II-only key are unchanged. |
| q-128139 | 17592186400331 | For invertible A, det(A)≠0 and Ax=b has exactly one solution x=A⁻¹b; Ax=0 has the unique zero solution, not infinitely many. Therefore current cases I and II apply, agreeing with the database key. The source solution conclusion is a copied/stale I,III conclusion. |
| q-330333 | 17592186412805 | The body rejects I/II and proves III. Change the final answer from I and III only to III only, matching the independently verified existing database key. |
| q-125395 | 17592186180023 | Correct the two path-direction references to match the prompt and pictured paths. |
| q-159485 | 17592186278226 | Correct the point name in the explanation of statement III. |
| q-120187 | 17592186362976 | Correct the numerator and finite limit for offered equation III; express the infinite behavior of equation I as slope magnitude. |
| q-120290 | 17592186382964 | Correct the sign of the zero-slope horizontal line for equation III. |
| q-169184 | 17592186426975 | Correct the point name in the coordinate conclusion. |

The correction transaction was freshly captured and previewed after all nine conversions were confirmed, then committed at **1834 → 1835**. A separate explanatory domain note for q-71391 is recorded as optional evidence and is not included among these definite repairs.

## Completion and continuation

[status.json](status.json) records verified completion. The nine batch directories and `optional-solution-repairs/` retain original EDN, exact requests, submission intents, native previews, committed reports and receipts. All 1,695 converted questions and 14 corrected solutions were read back at the final confirmed basis. All 10,170 original field/answer entities and the ordered-completion radio were unchanged. The initial historical snapshot and each batch's independent historical snapshot were reproduced.

Concurrent label and TeX-brace repairs found during refresh were preserved; [fresh-source-overlays.json](fresh-source-overlays.json) records these differences and equivalence checks. No stored key was changed or replaced. Question IDs confirmed here must be excluded from the next audit. Never rebuild or resubmit this cohort under new request keys; recover an existing uncertain request exactly. Candidates outside this keyed/rated tier were not re-audited. Generator source snapshots for the affected KPs may need refreshing separately.
