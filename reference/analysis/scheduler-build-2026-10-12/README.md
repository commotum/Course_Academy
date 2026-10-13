# Scheduler build — October 12, 2026

Implemented and deployed the ten approved categories in [scheduler-report.md](../../../scheduler-report.md). No scheduler policy decision remains open. This is a single-user implementation; diagnostics and the adaptive difficulty controller remain deferred.

## Behavior

- Global ordinary assessments: first successful learning at least 48 hours earlier, offered at 120 signed practice XP and required at 150 when feasible. Only ordinary assessments reset the cycle. Infeasible pools preserve XP, permit study and expose their reason.
- Assessment selection: one question per topic without replacement; never-tested/prior-tested weight 4:1, multiplied by `0.05 + 0.95 * (1 - coverage)^2`. At least one easy, moderate and hard question; additional draws read database weights and fit provisional 1/2/3-minute estimates into 15 minutes. The actual deadline is independent wall time.
- Editable assessment drafts and free navigation; one atomic Submit/expiry grades all reserved questions. Unanswered slots receive zero score and remediation without fictional incorrect-answer events. Feedback remains hidden until finalization.
- Wrong and unanswered topics require origin-linked reviews. Failed remediation reviews require full lessons. Failed required lessons retain their obligations during a break of five other successful practice activities; ready obligations gate unrelated queue entries and API starts/resumes.
- One optional retake below 75%, after repairs, without an XP/age delay or another cadence reset. Retakes preserve all original topics/KPs, exclude every original question including unvisited ones, and use budget/minimum-band lookahead with database remedial weights.
- Optional ordinary reviews are global and follow the existing direct/fractional FIRe updates. All five recommendations may be reviews. After three finished ordinary review attempts since an actual ordinary lesson offer, include an eligible optional lesson.
- First failed ordinary lessons return automatically after five other successful practice activities. Two consecutive failures at the same KP without progress assign its existing key-prerequisite reviews; failing those requires prerequisite lessons. Those repairs block the original path; assessment-origin repairs retain the global gate.
- Captured-basis inventory counts rolling fresh validated stock: five per supported band per lesson KP, or per review/assessment topic. Original-KP retake alternatives are protected. Durable jobs merge queue/target/unlock/review/assessment triggers, recover interrupted attempts before starting new work, prioritize shortages and proximity, and execute a registered generator or launch its creator. Unsupported and finite-limit outcomes remain explicit and stop repeated generation.

## Implementation

History-derived lifecycle and gates are in `engine/rust/scheduling.rs`; budget-aware sampling is in `engine/rust/assessment_sampling.rs`; batched discovery/counts are in `engine/rust/inventory.rs`. Existing `retrieval.rs`, `learning.rs` and `timing.rs` integrate these with FIRe, activity supply, signed XP and deadlines.

`scripts/learning_api.rs` implements durable drafts, navigation, batch grading, origin links, immediate expiry preparation and actual queue-offer timestamps. `ui/learning.js` provides the assessment controls. `scripts/serve_graph_explorer.py` runs captured-state scheduler refreshes and `scripts/inventory_jobs.py` stores deduplicated restart-safe generator jobs. Generator commits must use the application's existing `api.lock`, exact-basis requests and verified receipts.

The build preserves existing authored questions and learner history. Durable fixtures use separate temporary content and learners; their current entities are removed afterward. [Cleanup readback](fixture-cleanup-verification.edn) found no remaining scheduler-fixture or integration learners. Historical facts remain in EDB as intended.

## Schema and policy

Four new attributes were committed using the existing `:application/ca-engine` contributor:

| Attribute | Type/cardinality | Purpose |
|---|---|---|
| `:learner-task/active-item` | ref/one | Current assessment presentation |
| `:learner-task/offered-at` | instant/one | Actual ordinary lesson offer, without a separate review counter |
| `:question-generator/id` | UUID/one, unique identity | Stable generator registration |
| `:question-generator/script` | string/one | Validated repository-relative generator script |

The exact [request](schema-request.json), [logical forms](schema-transaction.edn), [preview](schema-preview.txt), [receipt](schema-receipt.txt) and [basis-1694 readback](schema-verification.edn) are retained. Database lineage is `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`; the request compared basis 1693 and committed at 1694. Local schema definitions and the SSD schema mirror include these attributes.

[Policy readback](policy-verification.edn) confirms the existing 0.5 retention threshold, 1-day base half-life, ordinary assessment 50/40/10 and remedial 45/40/15 weights. No new global question-duration attributes or stored XP/break counters were added. Prepared and started routes remain frozen when weights change.

## Verification

| Check | Result | Record |
|---|---|---|
| `cargo test --offline --quiet` | 113 passed | [Engine tests](engine-tests.txt) |
| Native learning API tests | 52 passed; 3 separately ignored | [Native tests](native-tests.txt) |
| `node --test tests/*.test.mjs` | 15 passed | [UI tests](ui-tests.txt) |
| Inventory job unit tests | 6 passed | [Inventory tests](inventory-tests.txt) |
| `bash tests/check_rust_edb.sh` | 25 current schemas and native validation/history checks passed | [Schema checks](schema-tests.txt) |
| `python3 scripts/check_learning_api.py` | Durable lesson and scheduler journeys passed | [Durable tests](durable-tests.txt) |
| Final durable scheduler rerun | Passed, including unchanged draft saves through reconnect | [Final durable journey](durable-scheduler-final.txt) |
| Python compile / JavaScript syntax / targeted whitespace checks | Passed | Checked during build |

Native fixtures cover the exact 48-hour admission boundary without prior retrieval, actual-offer resets after three ordinary reviews, signed awards, ordinary and retake minimum difficulty floors despite extreme database weights, mode/course changes, paused expiry, hidden draft grading, missed/unvisited remediation, failed repair escalation, five-success breaks, prerequisite path gates, fresh fixed-KP retakes and no retake chains. Durable tests use exact-basis transactions and replay commits to verify idempotence and contributor attribution.

The live database requires monotonic transaction instants. Its scheduler fixture therefore uses an explicitly admitted assessment route; isolated fixtures verify historical admission and age behavior. The third ignored test is the separate, environment-dependent delivery migration preview, outside this scheduler build.

## Deployment and limits

`course-academy.service` was restarted with the final tested build and verified active. The checks above total 188 passing tests, in addition to the schema harness. [Endpoint verification](deployment-verification.json) confirms successful home/inventory reads, five current resumable lessons, preserved recording mode and captured inventory lineage. Browser verification through the existing local Course Academy tab confirmed the same five-activity queue and its fresh-question preparation notice. No real learner assessment or lesson was started for verification.

At deployment the inventory identified 520 jobs from the current learner state. The creator worker was observed running after resolving its executable independently of the service manager's restricted PATH. Jobs remain pending until a subsequent database inventory verifies stock; launching a creator is not treated as successful replenishment. Previously rejected missing-executable jobs reopen when the executable becomes available.

The scheduler build is complete. Question authoring continues through the background pipeline; supported-band classification, finite-template limits and real stock shortages remain visible content dependencies. Retention timing and solving-time estimates are provisional and can be calibrated later. The automated application runs continue to prepare and refresh eligible work as verified stock arrives.
