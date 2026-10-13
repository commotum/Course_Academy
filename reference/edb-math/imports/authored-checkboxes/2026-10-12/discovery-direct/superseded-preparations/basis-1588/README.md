# Prepared checkbox conversion transactions

Prepared and sequentially previewed at math basis 1588 with source `:agent/gpt-6.1-sol-high`. No durable transaction has been submitted.

780 practice questions across 146 KPs become 2,417 statement checkbox fields, with 4,834 question-owned Boolean answers. The actual enum value is `:answer-field.type/checkbox` on attribute `:answer-field/type`.

Each question retains its mathematical statement text, stored correct subset, worked solution, rating, and KP/topic membership. List prefixes become bold Roman labels, and the prompt gains “Select all that apply.” The prior radio field and choice entities are detached from the question and retained unchanged. There are no learner presentations or saved responses for this batch at the captured basis. Full choice mappings are retained for review.

The four transactions are atomic individually, not as a group. Apply them in order. Each request retains the exact EDN file, SHA-256 hash, explicit agent source, stable request key, and expected basis. Confirm the preceding receipt before submitting the next batch; preview tempids are never used as durable IDs.

If unrelated activity advances the live basis before the first submission or between batches, the basis guard rejects stale work. Refresh only unsubmitted work, keeping any submitted request intact until its outcome is known. After an unknown outcome, reconcile the exact same original request and key.

## Transaction files

| Batch | Questions | Checkbox fields | Expected basis | EDN | Retained request |
|---|---:|---:|---:|---|---|
| 1 | 195 | 608 | 1588 | [batch-01/transaction.edn](batch-01/transaction.edn) | [batch-01/prepared-request.json](batch-01/prepared-request.json) |
| 2 | 195 | 609 | 1589 | [batch-02/transaction.edn](batch-02/transaction.edn) | [batch-02/prepared-request.json](batch-02/prepared-request.json) |
| 3 | 195 | 599 | 1590 | [batch-03/transaction.edn](batch-03/transaction.edn) | [batch-03/prepared-request.json](batch-03/prepared-request.json) |
| 4 | 195 | 601 | 1591 | [batch-04/transaction.edn](batch-04/transaction.edn) | [batch-04/prepared-request.json](batch-04/prepared-request.json) |

## Validation

All four native EDB speculative previews passed on one held immutable database value, with each speculative successor used for the next batch. Entity specs and checkbox predicates were checked with the deployed EDB library and application callbacks. Every emitted datom, key, Boolean bank, question link, prompt, and source was verified; only expected retractions occurred.

Native grading also checks all 780 canonical responses, every single-checkbox flip, incomplete responses, and all 3,900 original choice mappings through the current application engine. This verifies grading representation and source-key preservation; it does not independently re-solve every mathematical question.

Three source-format changes since discovery were reviewed: q-37355 acquired explicit Roman labels; two set-notation prompts acquired escaped outer braces for correct rendering. Their mathematics and stored keys are unchanged. Exact current source text is retained in snapshot.edn and used for CAS.

Evidence: plan.json, snapshot.edn, capture.json, preview.json, batch-*/preview.edn, batch-*/preview.json, engine-report.json, native-build.json, held-preview-build.json, and evidence/.

`prepare.py all` captures one native immutable database value, refreshes scoped reads, prepares the batches, and runs sequential noncommitting previews. It has no commit command. `check_native.py` runs offline grading checks. Preserve a completed preparation before refreshing it.
