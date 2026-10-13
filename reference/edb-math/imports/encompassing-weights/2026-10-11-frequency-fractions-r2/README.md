# Prepared initial encompassing weights

**Superseded and not submitted.** The user authorized the same weights with `:agent/gpt-6.1-sol-high` as source. The [replacement transaction](../2026-10-11-frequency-fractions-gpt-6.1-sol-high/README.md) committed and was verified at basis 1308. This earlier proposal and preview are preserved below; do not submit this request.

This proposal used the original rising-activity frequency estimates, rounded to **1/5, 1/4, 1/3, 2/5, 1/2, 3/5, 2/3, 3/4, 4/5, or 1**, with **Codex (`:agent/codex`) as the proposed source**.

The [transaction](transaction.edn) adds **1,730 encompassing relationships on 533 source topics**, plus the Codex contributor identity. It retains all original positive candidates, including single-observation estimates. The evidence contains 1,789 separate account estimates; 619 selected relationships have one eligible observation. Engine parameters remain unchanged.

For each account and relationship, the estimate is rising activities divided by eligible activities. Round the exact ratio to its nearest allowed fraction, with midpoint ties upward. Where accounts overlap, choose one whole account estimate by most eligible observations, then lower weight, then account name. Counts and histories are never pooled. [Selected relationships](selected-relationships.json) retain every account's evidence; [account conflicts](account-conflicts.json) record the 34 pairs with differing account weights.

| Fraction | Prepared relationships |
|---|---:|
| 1/5 | 6 |
| 1/4 | 56 |
| 1/3 | 316 |
| 2/5 | 1 |
| 1/2 | 617 |
| 3/5 | 1 |
| 2/3 | 29 |
| 3/4 | 2 |
| 4/5 | 0 |
| 1 | 702 |

Read exports are pinned to **database `math`, basis 1260**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. The exact logical transaction, source argument, request key, connection identity, lineage, basis and evidence hashes are saved in [request.json](request.json). Fraction labels are retained in the rationale; numerical weights use the schema's double type.

The [native preview verification](preview-verification.json) confirms **6,922 domain/source assertions and one transaction timestamp**, with every assertion attributed to Codex, no retractions, and exact agreement with the prepared forms. It reports `committed: false`, `speculative: true`; the live database remained at basis 1260. Speculative entity IDs and basis 1261 are not durable or reserved. The request's saved basis guard remains part of any future submission; a newer database requires rechecking the proposal against a fresh snapshot.

The [coverage audit](coverage-override-audit.json) follows the engine's explicit-edge override rule. Fourteen prepared direct edges override higher inferred coverage through other new edges. There are no existing encompassing edges at the read basis and no effective coverage decreases relative to that database. All original candidates remain included.

The earlier [frequency-fraction request](../2026-10-11-frequency-fractions/request.json) at basis 1257 is superseded because the database advanced before its preview. Its transaction content is identical, and its exact request remains preserved. The older [0.05-rounded request](../2026-10-11/request.json) also remains superseded and unsubmitted.

Method and evidence: [encompassing report](../../../../../encompassing-report.md), [separate account estimates](../../../../mathacademy/encompassing-analysis-2026-10-11/frequency-fractions/README.md). The relevant analysis and preparation suite passed **63 tests**.

`read_snapshot.py` only exports pinned reads and refuses to replace an existing prepared bundle. `preview.py` only uses EDB's noncommitting `with` operation, checks the saved database identity and basis, and verifies every resulting assertion. Neither script submits a transaction.
