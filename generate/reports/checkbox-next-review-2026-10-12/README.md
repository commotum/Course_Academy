# Next checkbox review

Evaluated at **EDB basis 1836**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. **The evaluated group is now committed and verified.** Conversions committed at basis 1854, followed by seven separate solution corrections at basis 1855. Each group was freshly captured, natively previewed, committed and verified before the next. Source: `:agent/gpt-6.1-sol-high`. The review covers the remaining historical strong shortlist; it is not a new database-wide discovery.

Confirmed conversion IDs were excluded using prior verified receipts and their matching per-batch requests/plans. The previously retained ordered IVT radio `17592186329885` was also excluded. Of the 1,076 remaining candidates, all 69 with an existing database key were evaluated against their complete current fields, worked solutions, memberships, incoming uses, and mathematical or image evidence.

| Outcome | Questions |
| --- | ---: |
| Suitable for checkbox conversion preserving the database key | 69 |
| Proposed answer-key replacements | 0 |
| Still awaiting missing-key investigation | 1,007 |

The evaluated group contains 55 duplicate-field questions and 14 single-field questions. The 69 conversion candidates span **65 KPs** and require **212 checkbox fields**. One candidate, q-37456 (`17592186420504`), is unrated: its answer is established, but its missing difficulty must remain unset unless separately researched. Thus **68** candidates also satisfy the earlier keyed-and-rated requirement. There are no canonical memberships or saved learner presentations/responses in the evaluated group.

## How the cases were resolved

- **Duplicate captures:** Each of the 55 questions has one unkeyed radio field and one keyed field. Their entire banks agree as subsets, including wrong answers. q-40639 differs in math delimiter/comma placement; q-76236 differs in spacing. Ownership was checked, and every old answer ID has an explicit subset mapping. For all 55 duplicate cases suitable for conversion, detach both old fields and retain their original entities. Do not copy a correct key into an unkeyed old field merely to facilitate the migration.
- **Existing keys:** All 69 keys were checked against the actual problem, worked solution and independent calculation or diagram inspection. No study-vault keys were consulted or substituted. Source order defines selectable cases; option order does not define labels.
- **Diagrams:** Ten essential problem diagrams were inspected directly; two other illustrations are redundant with explicit formulas. All answer options are text, so the first-answer-image filename rule does not apply here. q-162747 includes all four plotted points A–D, including false point C omitted by the old bank. q-155956 includes all four statements, including IV present in the problem but not named by its individual distractors.
- **None and malformed distractors:** q-76219 has an empty correct subset; submit explicit false answers for its three fields. Add unchecked-box guidance where the old bank includes an empty selection. q-36477's wrong option “II and II only” maps literally to `{II}`. Its intended typo correction is unknown; no III is invented and neither original answer entity is edited.
- **Prompt conventions:** Four proposed clarifications preserve the intended keys: q-171334 compares conditional logical forms for arbitrary truth values; q-95915 specifies reduced/thin QR and properties that must hold for every factorization; q-53000 states the source's inclusive-kite and exclusive-trapezoid definitions. q-94772 makes the source-intended maximum-possible-count reading explicit in statement I while preserving its III-only key. Other proposed prompt edits add labels and “Select all that apply.” as needed.

## Separate content findings

**q-94772 — `17592186184875`:** Preserve the Math Academy **III-only** key as requested. The earlier key-repair proposal is withdrawn. Statement I is clarified to “The maximum possible number of distinct singular values of a $3\times 2$ matrix $A$ is $3$.” Its stored solution and key are otherwise preserved. The reviewed interpretation is recorded in [review-overrides.json](review-overrides.json).

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

Exact before/after strings are in [proposed-solution-repairs.json](proposed-solution-repairs.json). All seven corrections were committed separately at basis 1855; existing keys are preserved.

## Evidence and continuation

- [keyed-resolutions.json](keyed-resolutions.json): all 69 decisions, independent proofs, source-order objects, keys, full old fields, mappings, memberships and proposed prompts.
- [snapshot.json](snapshot.json) and `snapshot.edn`: immutable basis-1836 facts. Query/input/result files are retained in `evidence/`; the EDN snapshot SHA is in [status.json](status.json).
- [image-evidence.json](image-evidence.json): diagram paths, hashes and inspection methods.
- [provenance.json](provenance.json): original key attribution and the verified existing contributor `:agent/gpt-6.1-sol-high` for future authored transactions.
- [next-queue.json](next-queue.json): separate evaluated conversion IDs, no outstanding key-repair IDs and 1,007 unevaluated IDs.
- [unkeyed-queue-summary.json](unkeyed-queue-summary.json): remaining questions span 621 KPs, with 227 problem-image cases. Every remaining question lacks a key, solution and difficulty at this basis. Historical screen flags are only hints, not resolved judgments.

Next, investigate missing keys in bounded KP/topic groups using original capture evidence, then local study material only where the DB has no key; independently verify every recovered answer. Missing difficulty is a distinct issue and should not be invented. Any later preparation must refresh unsubmitted source facts, preserve intervening corrections, and use the user's per-group capture → native preview → exact commit → receipt-verification workflow.

To reproduce offline evaluation, run `python3 generate/reports/checkbox-next-review-2026-10-12/review_keyed.py` and then `handoff.py` from the repo root. `audit_capture.py` refuses to overwrite an existing full snapshot. Read-only `read_provenance.py` uses the stored review basis.

Committed package: [discovery-keyed-incomplete](/home/jake/Developer/Course_Academy/reference/edb-math/imports/authored-checkboxes/2026-10-12/discovery-keyed-incomplete/README.md). All 69 reviewed questions are included, with existing keys preserved, and seven separate solution corrections. Both groups are confirmed and verified; see the package receipt. A concurrent removal of q-40639’s obsolete unkeyed duplicate was preserved. Historical counts above describe the original audit.
