# FIRe data contract

[The integration overview](fire-schema-integration.md) explains the completion flow. This document maps the current [schema](../schema/README.md) to [the Rust adapter](../engine/rust/schema.rs); [the reconstruction](fire-reconstruction.md) explains the numerical choices. Native tests cover the Rust adapter and runtime. The separate EDB harness still has an obsolete activity fixture; see [the validation notes](../engine/edb/README.md).

The engine needs an explicit encompassing graph, learner state, graded work, and a policy. Prerequisites and task XP cannot recover practice-transfer weights or hidden retention state. Direct practice works when encompassing weights are not yet available.

| Records | Ownership and identity |
| --- | --- |
| [Policy](../schema/engine/1-fire-policy.edn) | UUID identity and typed FIRe parameters. No persisted algorithm/name selector; `Policy.name` is only a runtime label. |
| [Topic](../schema/data/5-1-topic.edn), [encompassing](../schema/data/5-2-encompassing.edn) | Shared topic identity across courses. A topic owns its encompassing records; each names a component topic and weight. Prerequisite refs are separate. |
| [Learner](../schema/learner/1-1-learner.edn) | Owns progress, optional global performance, and queue entries; references retained task history through ordinary refs. Reverse relationships identify the learner. |
| [Progress](../schema/learner/1-3-learner-progress.edn) | One record per learner/topic, with its own identity, shared topic ref, and policy ref. Ownership and uniqueness are explicitly validated. |
| [Global performance](../schema/learner/1-2-learner-performance.edn) | Optional single learner-owned component; no independent domain identity. |
| [Task](../schema/learner/2-1-learner-task.edn), [task item](../schema/learner/2-2-learner-task-item.edn) | A task references its shared activity and owns ordered presentations. Each occurrence has its own UUID, including repeated presentations of the same question. |
| [Response](../schema/learner/2-4-learner-response.edn) | Entered values identify their answer fields. Item response refs can instead select canonical answer entities; canonical answers are never rewritten as learner submissions. |

The adapter resolves question → KP bank → topic and requires one KP bank and one topic. An unresolved or ambiguous mapping is an error for live updates, not permission to invent task-item topic refs. Historical source captures may preserve external topic/example IDs independently; an external example anchor does not establish an authored lesson-step identity.

## Numerical state and time

| Runtime state | EDB attribute | Meaning |
| --- | --- | --- |
| `repetitions` | `progress/repetitions` | Nonnegative fractional repetition position |
| `memory`, `memory_at` | `progress/memory`, `progress/memory-at` | Nonnegative memory quantity and its time anchor; memory may exceed one |
| `interval_days` | `progress/interval-days` | Stored positive interval used to decay memory |
| `learned` | `progress/learned` | Admission to retention tracking, distinct from present recall |
| `last_direct_at` | `progress/last-direct-at` | Last directly observed work, separate from implicit credit |
| Accuracy channels and masses | `progress/assessment-accuracy`, `practice-accuracy`, `assessment-mass`, `practice-mass` | Separate assessment/practice estimates and effective evidence masses |

The four accuracy fields also exist under `performance/*` for learner-global evidence. Effective accuracy, learning speed, and due time are derived. Failed initial work can update accuracy while the topic remains unlearned. Global accuracy receives each directly submitted answer once, regardless of how many topic profiles it affects.

`topic/difficulty` is an optional finite expected assessment accuracy in `[0,1]`, with lower values meaning harder material. Missing values use `policy/initial-accuracy`. Current schema stores no difficulty method, calibration-count, or cohort entities. The research estimator can still analyze qualifying population observations independently. Question E/M/H and actual solving duration are not substitutes for topic difficulty.

The adapter normalizes aware instants to UTC milliseconds and converts them to fractional epoch days for FIRe. Retained status transaction history supplies both working and calendar time: item elapsed seconds total the intervals spent in `started`, excluding `paused`; task elapsed seconds sum the item durations. Calendar instants identify when practice occurred and when an exam started, independently of working duration. Pausing does not extend a timed exam's deadline. XP measures a separate reward. The loader reconstructs chronological bounds from progress anchors and recorded status transitions; it does not manufacture missing historical timestamps.

## Activity evidence

[The runtime](../engine/rust/runtime.rs) consumes an application-graded result, not an unverified answer string. It validates the presentation against the activity and updates a copy of the loaded engine before preparing a transaction.

- Lessons follow ordered tutorial/KP placements. Local stopping is two consecutive correct within five questions per KP; all topic KPs must pass before admission. Local readiness requires learned prerequisites whose memory is above the due threshold. If a bank runs out before mastery, the accepted answer is retained and delivery requests more questions without declaring the lesson finished.
- Reviews use five distinct questions from their topic and stop after three consecutive correct or five attempts. Each finished lesson/review, including failed attempts, supplies one aggregate retention unit, scaled by mean submitted performance. Every submitted answer has already updated accuracy separately.
- Assessment and multistep items update retention using `performance / questions_for_this_topic_in_definition`. This is a local allocation rule, not a recovered MA formula. Multisteps preserve authored order; assessment order is application-selected.
- Diagnostics follow prepared probe branches. An available retry is offered after a submitted wrong answer without a timing gate; the learner chooses once. A completed retry replaces the original answer for frontier placement, while both presentations remain in history and submitted-answer accuracy. Correct evidence flows to prerequisites and wrong evidence to postrequisites, once per reached topic. Supplied reduced positive weights can represent slow correct answers; no time-to-weight formula is inferred. Final positive balances initialize previously unlearned topics without overwriting established retention history.
- Explicit skips consume practice attempts and break streaks, but do not count as wrong submitted answers in accuracy. Diagnostic skip placement is an explicit configurable policy, defaulting locally to negative evidence. Unpresented questions produce no task items.

`Event` and calculation receipts are runtime structures, not EDB domain records. The split `apply_accuracy`/`apply_retention` calls prevent recounting answers when an activity closes. XP remains separate: perfect lesson/review bonuses are observed candidates, assessment/multistep fitted formulas require opt-in, and partial lesson/review or diagnostic awards require an explicit caller award or remain unknown. See [the XP analysis](mathacademy-xp-analysis.md).

## Transaction and policy history

`EntitySnapshot` accepts entity maps keyed by numeric EID at one captured basis, plus `status_history` for timing. Each history entry identifies the entity, status attribute, asserted enum value, logical transaction basis `t`, and transaction instant `at`. Capture added status datoms from EDB's history view and join their transaction entities to `db/txInstant`. This is adapter input, not a new persisted schema. The snapshot resolves references, enums, UUIDs, policy settings, ownership, difficulty, and current state. Its `edn()` helper encodes the limited native value vocabulary used by transaction plans; it is not a general EDN parser or a database connection.

`complete_item` prepares item status/responses, derived item/task durations, affected progress and performance, and applicable task completion/XP in one `TransactionPlan`. The writer submits `plan.edn` with `TransactionRequest::from_edn(plan.request_key, ...).comparing_basis(plan.compare_basis_t)` and the registered validation predicates. The plan compare-and-swaps the item's started status to its terminal status and supplies the same `db/txInstant` used in the calculation. The basis guard protects graph, policy, and learner-state inputs from concurrent changes; the item guard protects this occurrence from duplicate completion. `transition_item` prepares pause/resume transactions and elapsed totals without awarding learning credit.

For a configured assessment or diagnostic timer, `expire_task` prepares a guarded task-completion plan using existing answers. Any active unanswered item is paused and its elapsed duration recorded; an already paused item stays paused. The completed parent prevents resuming either. Expiry neither invents answer verdicts nor repeats earlier accuracy updates. A partially delivered timed exam needs an explicit XP award or leaves XP unknown; the application runs the timer itself.

Retain the exact plan for uncertain-outcome retries. After a confirmed basis conflict, reload and recompute. A fresh identity for the same real-world answer is not deduplicated merely by EDB request retries. Commit success is the boundary for accepting the returned engine state; a rejected transaction leaves the loaded engine unchanged.

Policy parameters may be edited under the existing UUID. `progress/policy` identifies the policy, while EDB history and an appropriate historical database view recover the values associated with past state. Existing progress keeps its stored interval until a relevant engine update recomputes it; a parameter edit causes no automatic mass reschedule. There is no domain application/update receipt, separate event log, or policy-immutability requirement.

## Verification boundary

Run Rust checks with `cargo test`. [Native EDB checks](../tests/validate_fire_schema.rs) and the [Rust validation notes](../engine/edb/README.md) cover the separate schema/predicate boundary. Specs apply only when explicitly ensured; writers must register the predicates. Current work verifies hydration, application transitions, numerical updates, and generated transaction plans. The production writer, UI, and complete scheduler remain outside this implementation. Captured content and existing learner databases have not been migrated.
