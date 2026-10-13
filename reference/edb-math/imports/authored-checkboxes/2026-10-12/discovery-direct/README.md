# Committed checkbox conversion

All four transactions committed successfully, from math basis 1688 to 1692, attributed to `:agent/gpt-6.1-sol-high`.

Converted **780 practice questions across 146 KPs**, creating **2,417 statement checkbox fields** and **4,834 owned Boolean answers**. The enum is `:answer-field.type/checkbox`, stored under `:answer-field/type`.

Each committed receipt passed validation against the native speculative preview, including every new field, owned Boolean bank, stored correct subset, prompt, expected retraction, and source. All mathematical content, current worked solutions and ratings were preserved. Original radio fields and choices were retained unchanged. No learner presentations or responses existed for these questions at the captured basis.

Current source rendering repairs were retained: escaped braces for sets and piecewise expressions, and explicit Roman list markers. Inspected repairs are recorded in accepted-render-repairs.json and the exact source text in snapshot.edn.

## Confirmed receipts

| Batch | Questions | Checkbox fields | Basis before → after | Receipt |
|---|---:|---:|---|---|
| 1 | 195 | 608 | 1688 → 1689 | [batch-01/commit-receipt.json](batch-01/commit-receipt.json) |
| 2 | 195 | 609 | 1689 → 1690 | [batch-02/commit-receipt.json](batch-02/commit-receipt.json) |
| 3 | 195 | 599 | 1690 → 1691 | [batch-03/commit-receipt.json](batch-03/commit-receipt.json) |
| 4 | 195 | 601 | 1691 → 1692 | [batch-04/commit-receipt.json](batch-04/commit-receipt.json) |

The exact submitted EDN and complete request remain in each batch directory as transaction.edn and commit-intent.json. commit.edn contains the full confirmed report. These are committed requests: do not rebuild them or submit them under new keys.

Final readback passed at basis 1692: all 780 questions and 2,417 checkbox fields matched, all 4,680 original field/answer entities remained unchanged, and the prior historical snapshot was reproduced. Results are recorded in [verification.json](verification.json). Evidence also includes preview.json, batch-*/commit-validation.json, native-build.json, engine-report.json, held-preview-build.json, and evidence/.

The prior basis-1588 preparation is retained under superseded-preparations/basis-1588/. Native grading validated all 780 canonical responses, 2,417 single-checkbox flips, incomplete responses, and all 3,900 original choice mappings.

prepare.py intentionally refuses to rebuild a submitted preparation. commit.py commit recovers existing confirmed receipts under the retained request keys; commit.py verify repeats the final readback at the confirmed final basis.
