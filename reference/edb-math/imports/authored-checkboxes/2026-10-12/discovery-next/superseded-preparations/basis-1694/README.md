# Next-tier radio → checkbox preparation

**Prepared and speculatively verified; nothing submitted.** Three `gpt-6.1-sol` agents at high reasoning reviewed the held statements, text cases, and image cases; follow-up reviews tested ordered answers and mathematical qualifications. Of 1,696 keyed, rated candidates, **1,695 questions across 311 KPs** can be converted. One remains radio. This tier has no canonical examples and no captured learner presentations or saved responses.

The nine guarded conversion transactions create **5,178 checkbox fields and 10,356 owned Boolean answers**, with source **`:agent/gpt-6.1-sol-high`**. The field enum is `:answer-field/type :answer-field.type/checkbox`. All stored answer keys are preserved semantically. Detaching the old fields retains all **10,170 original field/answer entities** and their history. Every one of the 8,475 old choices, including wrong choices, has an explicit equivalent subset mapping.

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

The retained question is **q-48430 / `17592186329885`**, completing the intermediate value theorem in left-to-right blank order. `I, II` and `II, I` are distinct responses; checkbox conversion would collapse them. Its entities are excluded from every transaction.

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

The captured database basis is **1694**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. Sequential native previews held one immutable value and passed each speculative `db_after` into the next batch. The predicted final basis is **1703**, not a committed database basis. External writes advanced the basis from 1692 to 1693 and then 1694 during preparation. All scoped question facts were identical on each refresh. The nine guards and optional repair guard were rebuilt and natively previewed at 1694; the complete unsubmitted 1693 package is archived in `superseded-preparations/basis-1693/`.

| Batch | Questions | Required basis | Files |
|---|---:|---:|---|
| 1 | 195 | 1694 | [EDN](batch-01/transaction.edn) / [exact request](batch-01/prepared-request.json) |
| 2 | 195 | 1695 | [EDN](batch-02/transaction.edn) / [exact request](batch-02/prepared-request.json) |
| 3 | 195 | 1696 | [EDN](batch-03/transaction.edn) / [exact request](batch-03/prepared-request.json) |
| 4 | 195 | 1697 | [EDN](batch-04/transaction.edn) / [exact request](batch-04/prepared-request.json) |
| 5 | 195 | 1698 | [EDN](batch-05/transaction.edn) / [exact request](batch-05/prepared-request.json) |
| 6 | 195 | 1699 | [EDN](batch-06/transaction.edn) / [exact request](batch-06/prepared-request.json) |
| 7 | 195 | 1700 | [EDN](batch-07/transaction.edn) / [exact request](batch-07/prepared-request.json) |
| 8 | 195 | 1701 | [EDN](batch-08/transaction.edn) / [exact request](batch-08/prepared-request.json) |
| 9 | 135 | 1702 | [EDN](batch-09/transaction.edn) / [exact request](batch-09/prepared-request.json) |

Each complete question conversion is atomic. The prepared requests retain exact EDN hashes, stable UUIDs, source, lineage, request keys and required basis guards. [Preview results](preview.json) verify native validators, exact assertions/retractions, tempids and every datom's provenance. Prospective identities were checked absent at the captured basis.

## Verification

The current native grading engine passed **36,246 field checks** (19,327 accepted; 16,919 rejected), plus whole-question checks for all 1,695 canonical responses, 5,178 single-checkbox flips, 1,695 incomplete responses, and all **8,475 mapped original choices**. See [engine report](engine-report.json), [native build](native-build.json), and [fixture-to-final-plan verification](engine-fixture-verification.json).

These checks establish representation and grading preservation. They do not independently recalculate every question's mathematics. Mathematical proofs are recorded for the held/exception cases, 300 matrix atoms, and the semantic ambiguities; ordinary cases rely on the existing key and source evidence. No unresolved migration decision remains in this tier.

## Separate worked-solution corrections

A separately reviewable transaction corrects **14 definite errors**, without changing any answer key, field, prompt, rating, membership or learner state. Its [plan](optional-solution-repairs/plan.json) includes complete before/after strings, and its [EDN](optional-solution-repairs/transaction.edn), [exact request](optional-solution-repairs/prepared-request.json), and [native preview](optional-solution-repairs/preview.json) are ready. It is optional relative to the checkbox conversion, but these corrections address established content errors.

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

This correction transaction requires **all nine conversion batches to have been confirmed first**, then basis **1703**; its preview follows the entire conversion chain in memory. A separate explanatory domain note for q-71391 is recorded as optional evidence and is not included among these definite repairs.

## Resume safely

[status.json](status.json) is the durable handoff. No commit intents or receipts exist for this tier. Preparation scripts contain no durable submission command. Before authorized submission, confirm the live basis and exact request bytes. If the basis has advanced, archive and refresh only definitely unsubmitted work, then preview again. After a confirmed batch, persist its receipt and verify its exact result before continuing. Reconcile an unknown outcome using the complete original request and key; never rebuild uncertain submissions. Do not apply the optional corrections merely because an unrelated write happens to reach their predicted basis.

Candidates outside this keyed/rated tier were not re-audited. These prepared IDs must be kept separate from confirmed migrations and the next queue. Generator source snapshots for affected KPs may need refreshing after a confirmed migration.
