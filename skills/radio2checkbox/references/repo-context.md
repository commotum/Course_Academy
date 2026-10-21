# Repo context and checkpoints

Paths below are relative to the Course_Academy repo root and include historical migration checkpoints and later repair runs. Inspect current code/configuration and receipts before reusing them; this reference is not a live database status report.

## Integration

- `scripts/question_capture/database.py`: existing `Database` wrapper, query/Pull evidence files, basis reads, durable request/replay handling. Inspect `_commit` before adapting it.
- `scripts/question_capture/edn.py`: EDN encoding/decoding; `core.py`: `stable_id` identities.
- `capture/scripts/database/preview.py`: installed-library native preview helper and validator registry integration.
- `engine/edb/answer_fields.rs`, `configuration.rs`, `progress.rs`: native validation callbacks; inspect current engine grading entry points for response checks.
- Historical math writer configuration used `.local/edb/capture-runtime/math-edb`, database `math`, and `/tmp/edb-math/writer.sock`. Reuse actual existing configuration, verifying lineage and endpoint; do not print environment credentials. The deployed library must match the running writer, not merely an arbitrary local EDB build.

Use the [EDB sources reference](../../edb/references/sources.md) for authoritative docs and version-specific interfaces. Inspect live schema enum/spec/contributor entities instead of inventing domain attributes or numeric IDs.

## Candidate inventories and prior decisions

| Location | Purpose and caveat |
| --- | --- |
| `generate/scripts/find_candidates.py` | Original narrower KP finder; inspect the script's actual scope |
| `generate/runs/checkbox-audit-2026-10-12/` | Earlier finder audit and question evidence |
| `generate/reports/checkbox-discovery-2026-10-12/` | Repo-wide inventory, source snapshots, readiness and strict-cohort reports |
| `reference/edb-math/imports/authored-checkboxes/2026-10-11/topic-3215/` | Initial topic migration, None removal and prompt consistency |
| `reference/edb-math/imports/authored-checkboxes/2026-10-12/finder-easy/` | 220-question conversion; logical forms, learner subset mapping and native verification examples |
| `reference/edb-math/imports/authored-checkboxes/2026-10-12/finder-remaining/` | `resolutions.json`, `resolve.py`, `read_snapshot.py`, `prepare.py`, `commit.py`; missing-key proofs, source evidence, retain-radio decisions; 89 conversions and one retained-radio key repair |
| `reference/edb-math/imports/authored-checkboxes/2026-10-12/discovery-direct/` | Confirmed 780-question migration, held native preview chain, four batch receipts, grading and final readback |
| `reference/edb-math/imports/authored-checkboxes/2026-10-12/discovery-next/` | Next keyed/rated tier: 1,695 conversions across 311 KPs in nine independently captured/previewed groups, plus 14 separate solution corrections; retain ordered radio q-48430 (`17592186329885`). Inspect `commit-receipt.json`, `verification.json`, `execution-plan.json` and status to establish confirmed completion. |
| `reference/edb-math/repairs/2026-10-17-triangular-checkbox-layout/` | Confirmed repair at **3479 → 3480**; see `verification.json` and retained receipts. Repaired 16 existing checkbox layouts and converted four radios; scope includes three canonical examples, seven raster images, four restored tutorial matrices, and two generators. One unseen all-false generated question was withdrawn. `content-plan.json` retains complete source-object mappings, including `17592186262617` and `17592186120421`. `images/responsive/verification.json` records the final narrow-screen rendering checks. |

In the repo-wide discovery directory, start with `report.json`, `readiness-summary.json`, `canonical-membership.json`, and `direct-candidates.json`. `sources/<kp-eid>.json` and stored query/input/result files supply evidence. `scan.py`, `screen.py`, `review_direct.py`, and `filter_direct.py` illustrate selection and screening, but some scripts assume fixed historical bases/counts. Read before adapting; do not run as generic current-state tools.

At discovery basis **1534**, the audit reported 3,552 strong structural candidates across 771 KPs; 2,476 had all fields keyed and a difficulty. The strict 780-question cohort is **already committed**, not the next queue. Canonical-only examples were excluded, and the audited shortlist had no canonical membership overlap. A new audit must inspect current types and subtract confirmed migrated IDs across all receipts. These counts do not describe today's remaining work.

The last confirmed direct migration was **1688 → 1692**, four batches of 195 questions, 146 KPs, 2,417 checkbox fields and 4,834 owned Boolean answers, source `:agent/gpt-6.1-sol-high`. Its `commit-receipt.json`, `verification.json`, and `status.json` establish completion. `plan.json` was retained in its prepared form for provenance; it does not override receipts. The 4,680 original field/answer entities were retained unchanged. No learner uses existed in that cohort; later cohorts require fresh checks.

Do not rerun committed preparations under new keys or overwrite their files. The direct `prepare.py` intentionally rejects submitted preparations and has fixed cohort assumptions. `held-preview.rs` shows a single captured immutable value and sequential native speculative databases; it is not a general durable writer. `commit.py` shows persisted intent, exact submission and post-commit validation. Use these as reviewed examples, adapting only to new scope and current integration.

Historical presentation warning: the October 12 finder scripts intentionally kept selectable lists/matrices in the stem and created fields keyed only by source labels. Their verification even asserted those label-only keys. Questions `17592186262617` (finder-easy, `q-126479`) and `17592186120421` (finder-remaining, `q-42090`) demonstrate that defect. The October 16 statement-label repair covered only conformability KP `17592186100869`; it was not a repo-wide cleanup. Do not reuse those historical prompt/field transformations or label-key assertions for new work. Use the current complete-object rule and presentation lint; retain the old plans and receipts as evidence of what was actually committed.

In discovery-next, `one_at_a_time.py` and `batch-preview.rs` implement the user's preferred per-group capture → preview → commit → receipt verification workflow. Historical root `plan.json` and chain previews do not override per-batch receipts. Concurrent edits that only corrected ordered labels or literal TeX braces were reviewed and preserved; no existing key was replaced. `transport-recovery.json` records recovery of a confirmed stale-basis rejection with the deployed native API and the decoder update for canonical blob v4 / outcome v7. Unknown outcomes must still retain their complete original requests.

## Persistent case ledger

Create a new dated/run-specific audit directory rather than repurposing committed artifacts. Keep the ledger machine-readable and a short human-readable breakdown. Suggested per-question fields:

```text
question_eid, math_academy_id, kp_ids, topic_ids, canonical_memberships
captured_lineage, captured_basis, source_snapshot_path/hash
old_fields, old_choices, database_key, difficulty, worked_solution
universe: ordered objects with labels and text/image identities
choice_mapping: every old answer ID -> selected labels
key_evidence: database/capture/study, file/line/hash, independent proof
decision: convert | retain_radio | repair_key | needs_evidence
reason, metadata/feedback handling, problem_before/after
learner_uses, response_mapping, state_preservation_checks
new_uuids, batch, preview_status, request_key, intent/hash
commit_status/receipt/basis, verification, unresolved_question, next_action
```

Record unresolved facts precisely: missing capture order, missing list object, conflicting solution, malformed saved response, or a genuine choice about intended question meaning. Group common resolutions for the user's breakdown, but retain each question's proof and mapping. A resume should establish which decisions are resolved and whether the underlying database/source changed before extending the queue.

Keep run status separate from the case ledger: captured basis/lineage, selected IDs, completed IDs, unsubmitted IDs, unknown-outcome requests, batch order and expected guards, artifact paths, verification summary, and next action. Write status after meaningful progress and receipts before any post-commit processing. Preserve superseded preparations and why they were rejected.

## Generator follow-up

Generators may replay captured question fields and prompts. Inspect `generate/scratch` source captures and documented basis when asked about affected generators; update and validate them as a separate authorized task. The determinant generators `17592186059848.py` and `17592186059849.py` were refreshed against prior migrations, but that is not evidence that every generator reflects later changes. Record affected KP IDs in the migration handoff; never claim generator repair from database conversion alone.
