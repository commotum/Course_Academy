# Progress ownership

`learner/knowledge-profile` owns progress records. Each record references a shared topic through `progress/topic`; its learner is available through the reverse reference `learner/_knowledge-profile`. Component ownership gives progress the learner's lifecycle, while deleting progress does not delete the topic.

[progress.rs](progress.rs) implements the entity predicates named in the EDN. `valid-profile?` checks that every member has an ID, a real topic, exactly this learner as owner, and a distinct topic within the profile. An empty profile is valid. `valid-progress?` checks that the record has exactly one owner, checks that owner's profile, validates finite retention/accuracy/mass values, and requires a real policy target. This also catches topic changes that create duplicates.

Register these callbacks with `register_progress_predicates` in a `TxFunctions` registry supplied to `Database::with_forms`. The durable [Course Academy transactor](transactor.rs) registers the same checks in EDB's native registry.

On progress writes, request `:db/ensure :progress/validate`. On membership changes, request `:db/ensure :learner/validate` for affected learners and `:progress/validate` for affected surviving progress records, including detached records. Create the learner link and progress in the same transaction. To remove progress, retract the component entity; to transfer it, retract the old link and assert the new link atomically. A learner deletion cascades to its progress.

Specs are opt-in: bypassing `:db/ensure` bypasses these checks. The learner's minimal validation permits ID-only progress placeholders with a topic; ensure each progress record's complete spec before using it in the engine.

Global accuracy lives on the optional component referenced by `learner/performance`, defined in [1-2-learner-performance.edn](../../schema/learner/1-2-learner-performance.edn). Ensure `performance/validate` on that child when writing its four accuracy/mass values. Resolve it through the learner ref; the reverse ref is `learner/_performance`. No separate domain ID is needed. Cardinality one permits at most one summary per learner but does not prevent two learners from sharing a summary. Single ownership and numeric ranges remain application contracts; the progress predicates do not check them. Per-topic accuracy remains on `progress`.

Task history through `learner/activity` remains an ordinary reference collection; its common schema is described in [the schema organization](../../schema/README.md). Each task owns individual learner presentations through `learner-task/items`, defined in `learner/2-2-learner-task-item.edn`. `learner-task/activity` points to the shared activity definition; `task-item/content` points to the presented question, tutorial, or example. The displayed queue is derived from eligible unfinished tasks and their priority, with no separate queue entities. Task content validation and scheduling remain application work; the progress predicates do not implement them.

# Policy and topic difficulty

[configuration.rs](configuration.rs) implements `course-academy.policy/valid?` and `course-academy.topic/valid-difficulty?`. Register these with `register_configuration_predicates` alongside the progress predicates. Like the progress checks, production writer deployment through EDB's native registry remains to be implemented.

Ensure `policy/validate` for complete configurations, defined in [1-fire-policy.edn](../../schema/engine/1-fire-policy.edn). The predicate checks the two supported retention-update orders, finite numeric ranges, and cross-setting bounds. Parameters can be edited under the same UUID `policy/id`; EDB history preserves previous values.

Ensure `topic/difficulty-validate` for a difficulty update: it requires topic identity and a positive finite workload multiplier (values above 1 are allowed). `topic/validate` invokes the same predicate while allowing absent difficulty. Identity-only imports can use `topic/identity-validate`. Difficulty methods, counts, cohorts, and cutoff attributes were removed from the schema.

Topic workload calibration uses authoritative lesson base XP divided by the unrounded expected-distribution content score. It never reads learner correctness. `progress/expected-assessment-accuracy` and `progress/expected-practice-accuracy` are optional finite probabilities in [0,1], validated when present. Initial forecasts use direct prerequisites with separate evidence-mass weighting, then same-channel learner-topic performance, then the policy prior. The retention engine uses learner accuracy alone; topic workload multipliers never enter learning speed.

To inspect a past progress state, use `as_of` at the transaction that wrote it and resolve `progress/policy` and its parameters in that same historical database value. Reading the policy's current values would not recover the settings used then. Retain the relevant history. Editing policy parameters does not rewrite stored `progress/interval-days`; the interval remains in effect until the engine explicitly recomputes it, with no automatic bulk rescheduling.

The intended item-completion operation grades the response and atomically writes the item status, responses, elapsed totals, affected progress, and global performance. Compute against the transaction's authoritative input state, or guard an external calculation against a changed basis. EDB transaction history connects completion with its state changes without a separate engine-update record. Exact request retries use EDB's retry mechanism, while a status compare-and-swap prevents fresh requests from crediting the same item again. The Rust adapter prepares this transaction; wiring it to the production durable writer remains application work. Schema validation alone does not run the engine.

The Rust [schema adapter](../rust/schema.rs) loads captured entities and their status transaction history, then prepares native EDN writes. The [completion handler](../rust/runtime.rs) runs after application grading and distinguishes answer accuracy from grouped retention credit. The database schema maps to its existing `Policy` fields as follows. All settings are explicit on a complete policy; do not silently fill omitted persisted fields from changing program defaults.

| EDB policy attribute | Rust `Policy` field |
| --- | --- |
| `base-half-life-days` | `base_interval_days` |
| `interval-growth` | `interval_growth` |
| `maximum-half-life-days` | `maximum_interval_days` |
| `review-threshold` | `due_threshold` |
| `initial-retention` | `restored_memory` |
| `early-practice-discount-power` | `discount_power` |
| `initial-accuracy` | `prior_accuracy` |
| `accuracy-update-rate` | `accuracy_alpha` |
| `speed-exponent` | `speed_exponent` |
| `minimum-speed` | `minimum_speed` |
| `maximum-speed` | `maximum_speed` |
| `overdue-failure-slope` | `failure_overdue_slope` |
| `maximum-failure-multiplier` | `maximum_failure_multiplier` |
| `gate-slow-implicit` | `gate_slow_implicit` |
| `retention-update-order` | `memory_order`: `/decay-before-add` → `decay-before-add`; `/add-before-decay` → `literal-add-before-decay` |
| `future-horizon-days` | `future_horizon_days` |

`policy/id` is a UUID, not the prototype's calculated `Policy.id` fingerprint. Runtime `Policy.name` is only a prototype label, not a database input; there is no stored algorithm selector. The adapter resolves the retention-update enum refs with these explicit mappings.

Run the Rust checks and native EDB boundary check from the repository root:

```bash
cargo test
bash tests/check_rust_edb.sh
```

The native harness uses the sibling EDB release build (or `EDB_ROOT`). It installs current schema EDNs, excluding curriculum seed transactions, and checks policy history and numeric/ownership guards. Its activity fixture still uses the retired `assessment/*` schema and currently stops there with `schema/unknown-attribute`. Migrating that fixture and the runtime to generic `activity/*` and `step/*` is separate engine work; do not treat this harness as passing until then.

The plan's `compare_basis_t` must be submitted through `TransactionRequest::comparing_basis`, together with its stable `request_key`. Item CAS alone cannot detect a concurrently changed graph, policy, or another task's progress update. Retain the original plan for an uncertain submission or exact retry. The in-memory harness checks emitted transactions and native request construction; it does not exercise a deployed durable transactor's retry/basis-conflict path.

The application calls `runtime::complete_item` automatically after grading, or `expire_task` from its timer. These functions return a transaction plan and speculative updated engine. `transition_item` prepares pause/resume transactions without applying learning credit. Only adopt speculative state after a successful commit; reload and recompute after a confirmed conflicting write. No additional domain event or processing record is required. Grading, snapshot acquisition, production writer registration, UI callbacks and the full queue scheduler remain application integration work.

[Task items](../../schema/learner/2-2-learner-task-item.edn) hold responses, status, derived elapsed time, and optional `task-item/performance`. Join historical status assertions to their transaction's `db/txInstant`, ordered by transaction basis. Intervals spent in `started` supply working duration; the first task start and terminal transitions supply calendar timing. The adapter writes item and summed task durations together, with an explicit transaction instant matching the time used in its calculation. Retain status history and record transitions when they happen. Pausing does not extend a timed exam's deadline; timer expiry pauses any active unanswered item without inventing an answer verdict. Whole-task status and XP remain on the task.
