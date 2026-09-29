# Progress ownership

`learner/knowledge-profile` owns progress records. Each record references a shared topic through `progress/topic`; its learner is available through the reverse reference `learner/_knowledge-profile`. Component ownership gives progress the learner's lifecycle, while deleting progress does not delete the topic.

[progress.rs](progress.rs) implements the entity predicates named in the EDN. `valid-profile?` checks that every member has an ID, a real topic, exactly this learner as owner, and a distinct topic within the profile. An empty profile is valid. `valid-progress?` checks that the record has exactly one owner, checks that owner's profile, validates finite retention/accuracy/mass values, and requires a real policy target. This also catches topic changes that create duplicates.

Register these callbacks with `register_progress_predicates` in a `TxFunctions` registry supplied to `Database::with_forms`. For a durable writer, register the same checks using EDB's `NativeRegistryBuilder::entity_predicate` with cooperative cancellation; that writer integration remains to be implemented.

On progress writes, request `:db/ensure :progress/validate`. On membership changes, request `:db/ensure :learner/validate` for affected learners and `:progress/validate` for affected surviving progress records, including detached records. Create the learner link and progress in the same transaction. To remove progress, retract the component entity; to transfer it, retract the old link and assert the new link atomically. A learner deletion cascades to its progress.

Specs are opt-in: bypassing `:db/ensure` bypasses these checks. The learner's minimal validation permits ID-only progress placeholders with a topic; ensure each progress record's complete spec before using it in the engine.

Global accuracy lives on the optional component referenced by `learner/performance`, defined in [1-2-learner-performance.edn](../../schema/learner/1-2-learner-performance.edn). Ensure `performance/validate` on that child when writing its four accuracy/mass values. Resolve it through the learner ref; the reverse ref is `learner/_performance`. No separate domain ID is needed. Cardinality one permits at most one summary per learner but does not prevent two learners from sharing a summary. Single ownership and numeric ranges remain application contracts; the progress predicates do not check them. Per-topic accuracy remains on `progress`.

Task history through `learner/activity` remains an ordinary reference collection; its common schema is described in [the schema organization](../../schema/README.md). Task domain guards are not implemented by these progress predicates. `learner/queue` owns the current up-next entries, while each task owns individual learner presentations through `learner-task/items`, defined in `learner/2-2-learner-task-item.edn`. `learner-task/activity` points to the shared activity definition; `task-item/content` points to the presented question, tutorial, or example. The schema does not store duplicate task/item type enums. Queue ownership, index uniqueness, selection enums, and content validation likewise remain application contracts; these progress predicates do not check the queue or implement scheduling.

# Policy and topic difficulty

[configuration.rs](configuration.rs) implements `course-academy.policy/valid?` and `course-academy.topic/valid-difficulty?`. Register these with `register_configuration_predicates` alongside the progress predicates. Like the progress checks, production writer deployment through EDB's native registry remains to be implemented.

Ensure `policy/validate` for complete configurations, defined in [1-fire-policy.edn](../../schema/engine/1-fire-policy.edn). The predicate checks the two supported retention-update orders, finite numeric ranges, and cross-setting bounds. Parameters can be edited under the same UUID `policy/id`; EDB history preserves previous values.

Ensure `topic/difficulty-validate` for a difficulty update: it requires topic identity and a finite value in [0,1]. `topic/validate` invokes the same predicate while allowing absent difficulty. Identity-only imports can use `topic/identity-validate`. Difficulty methods, counts, cohorts, and cutoff attributes were removed from the schema.

A future difficulty estimator must select eligible direct assessment evidence and avoid duplicate counting. Only its resulting topic difficulty is currently modeled. Use EDB CAS or a basis guard for read-compute-write updates; the estimator and durable writer are not implemented.

The engine reads authoritative `topic/difficulty`; if absent, it uses `policy/initial-accuracy`. To inspect a past progress state, use `as_of` at the transaction that wrote it and resolve `progress/policy` and its parameters in that same historical database value. Reading the policy's current values would not recover the settings used then. Retain the relevant history. Editing policy parameters does not rewrite stored `progress/interval-days`; the interval remains in effect until the engine explicitly recomputes it, with no automatic bulk rescheduling.

The intended item-completion operation grades the response and atomically writes the item result, responses, affected progress, and global performance. Compute against the transaction's authoritative input state, or guard an external calculation against a changed basis. EDB transaction history connects completion with its state changes without a separate engine-update record. Exact request retries use EDB's retry mechanism, while a one-time completion guard prevents fresh requests from crediting the same item again. The Python adapter prepares this transaction; wiring it to the production durable writer remains application work. Schema validation alone does not run the engine.

The Python [schema adapter](../schema.py) loads a captured entity projection and prepares native EDN writes. The [completion handler](../runtime.py) runs after application grading and distinguishes answer accuracy from grouped retention credit. The database schema maps to its existing `Policy` fields as follows. All settings are explicit on a complete policy; do not silently fill omitted persisted fields from changing program defaults.

| EDB policy attribute | Python `Policy` field |
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

`policy/id` is a UUID, not the prototype's calculated `Policy.id` fingerprint. Python `Policy.name` is only a prototype label, not a database input; there is no stored algorithm selector. The adapter resolves the retention-update enum refs with these explicit mappings.

Run the Python checks and the native EDB boundary check from the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'
rustc --edition=2021 tests/validate_fire_schema.rs \
  --extern edb_core=/home/jake/Developer/EDB/target/release/deps/libedb_core-2824b6ab39ee5756.rlib \
  -L dependency=/home/jake/Developer/EDB/target/release/deps \
  -o /tmp/course-academy-current-schema-check
PYTHONDONTWRITEBYTECODE=1 /tmp/course-academy-current-schema-check
```

The library filename is specific to the installed EDB build. The native harness installs all 30 current EDNs, captures actual EDB entity values for Python, and applies the resulting transaction EDN back through EDB. It checks policy history, numeric/ownership guards, item completion CAS, and protection of canonical answer choices during task deletion.

The plan's `compare_basis_t` must be submitted through `TransactionRequest::comparing_basis`, together with its stable `request_key`. Item CAS alone cannot detect a concurrently changed graph, policy, or another task's progress update. Retain the original plan for an uncertain submission or exact retry. The in-memory harness checks emitted transactions and native request construction; it does not exercise a deployed durable transactor's retry/basis-conflict path.

The application calls `engine.runtime.complete_item` automatically after grading, or `expire_task` from its timer. These functions return a transaction plan and speculative updated engine. Only adopt that state after a successful commit; reload and recompute after a confirmed conflicting write. No additional domain event or processing record is required. Grading, snapshot acquisition, production writer registration, UI callbacks and the full queue scheduler remain application integration work.

[Task items](../../schema/learner/2-2-learner-task-item.edn) hold responses, results, elapsed time, optional `task-item/completed-at`, and optional `task-item/performance`. Completion time identifies when practice occurred, separately from its duration and the engine transaction's commit time. Whole-task outcome and XP remain on the task. The completion handler uses these facts directly; no separate persisted event or update record is needed.
