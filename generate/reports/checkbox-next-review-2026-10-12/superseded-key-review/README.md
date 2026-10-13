# Next checkbox review

Evaluated at **EDB basis 1836**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. **No database writes, transaction preparation, or native preview performed.** The review covers the remaining historical strong shortlist; it is not a new database-wide discovery.

Confirmed conversion IDs were excluded using prior verified receipts and their matching per-batch requests/plans. The previously retained ordered IVT radio `17592186329885` was also excluded. Of the 1,076 remaining candidates, all 69 with an existing database key were evaluated against their complete current fields, worked solutions, memberships, incoming uses, and mathematical or image evidence.

| Outcome | Questions |
| --- | ---: |
| Suitable for checkbox conversion preserving the database key | 68 |
| Separate content repair required before conversion | 1 |
| Still awaiting missing-key investigation | 1,007 |

The evaluated group contains 55 duplicate-field questions and 14 single-field questions. The 68 conversion candidates span **64 KPs** and would require **209 checkbox fields**. One candidate, q-37456 (`17592186420504`), is unrated: its answer is established, but its missing difficulty must remain unset unless separately researched. Thus **67** candidates also satisfy the earlier keyed-and-rated requirement. There are no canonical memberships or saved learner presentations/responses in the evaluated group.

## How the cases were resolved

- **Duplicate captures:** Each of the 55 questions has one unkeyed radio field and one keyed field. Their entire banks agree as subsets, including wrong answers. q-40639 differs in math delimiter/comma placement; q-76236 differs in spacing. Ownership was checked, and every old answer ID has an explicit subset mapping. For the 54 duplicate cases suitable for conversion, detach both old fields and retain their original entities. Do not copy a correct key into an unkeyed old field merely to facilitate the migration.
- **Existing keys:** All 69 keys were checked against the actual problem, worked solution and independent calculation or diagram inspection. No study-vault keys were consulted or substituted. Source order defines selectable cases; option order does not define labels.
- **Diagrams:** Ten essential problem diagrams were inspected directly; two other illustrations are redundant with explicit formulas. All answer options are text, so the first-answer-image filename rule does not apply here. q-162747 includes all four plotted points A–D, including false point C omitted by the old bank. q-155956 includes all four statements, including IV present in the problem but not named by its individual distractors.
- **None and malformed distractors:** q-76219 has an empty correct subset; submit explicit false answers for its three fields. Add unchecked-box guidance where the old bank includes an empty selection. q-36477's wrong option “II and II only” maps literally to `{II}`. Its intended typo correction is unknown; no III is invented and neither original answer entity is edited.
- **Prompt conventions:** Three proposed clarifications preserve the intended keys: q-171334 compares conditional logical forms for arbitrary truth values; q-95915 specifies reduced/thin QR and properties that must hold for every factorization; q-53000 states the source's inclusive-kite and exclusive-trapezoid definitions. Other proposed prompt edits add labels and “Select all that apply.” as needed.

## Separate content findings

**q-94772 — `17592186184875`:** The existing key is “III only.” Statement I says a 3×2 matrix has *at most 3* distinct singular values. Having at most 2 makes that weaker bound true, not false. Statement II is false because singular values are nonnegative; III is true. Therefore the mathematically correct selection is **I and III**, which neither old bank offers. Keep this outside the key-preserving conversion group. The recommended separate repair preserves the statements and corrects the key and solution. Its proof and alternative are in [proposed-key-repair.json](proposed-key-repair.json).

Seven solution corrections are proposed independently of answer-field changes; none changes a key:

| Question | Finding and proposed correction |
| --- | --- |
| q-64207 | Copy the problem's logarithm constant −2 rather than −3 |
| q-108979 | The A+3I chain maps y, not w, to zero |
| q-95915 | Rectangular thin-QR Q has orthonormal columns; it need not be an orthogonal matrix |
| q-76236 | Include both irrational square roots; use x² ≥ 0, including zero |
| q-76250 | Replace an irrational counterexample outside domain Q with g(1)=g(−1)=−1 |
| q-77378 | 27 is an omitted codomain element, not a range element |
| q-80265 | Compare the integrals 32/105 and 8/3; nonzero values outside the region alone do not exclude cancellation |

Exact before/after strings are in [proposed-solution-repairs.json](proposed-solution-repairs.json). These are reviewable proposed repairs, not transactions.

## Evidence and continuation

- [keyed-resolutions.json](keyed-resolutions.json): all 69 decisions, independent proofs, source-order objects, keys, full old fields, mappings, memberships and proposed prompts.
- [snapshot.json](snapshot.json) and `snapshot.edn`: immutable basis-1836 facts. Query/input/result files are retained in `evidence/`; the EDN snapshot SHA is in [status.json](status.json).
- [image-evidence.json](image-evidence.json): diagram paths, hashes and inspection methods.
- [provenance.json](provenance.json): original key attribution and the verified existing contributor `:agent/gpt-6.1-sol-high` for future authored transactions.
- [next-queue.json](next-queue.json): separate evaluated conversion IDs, content-repair ID and 1,007 unevaluated IDs.
- [unkeyed-queue-summary.json](unkeyed-queue-summary.json): remaining questions span 621 KPs, with 227 problem-image cases. Every remaining question lacks a key, solution and difficulty at this basis. Historical screen flags are only hints, not resolved judgments.

Next, investigate missing keys in bounded KP/topic groups using original capture evidence, then local study material only where the DB has no key; independently verify every recovered answer. Missing difficulty is a distinct issue and should not be invented. Any later preparation must refresh unsubmitted source facts, preserve intervening corrections, and use the user's per-group capture → native preview → exact commit → receipt-verification workflow.

To reproduce offline evaluation, run `python3 generate/reports/checkbox-next-review-2026-10-12/review_keyed.py` and then `handoff.py` from the repo root. `audit_capture.py` refuses to overwrite an existing full snapshot. Read-only `read_provenance.py` uses the stored review basis.
