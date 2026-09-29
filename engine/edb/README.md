# Progress ownership

`learner/knowledge-profile` owns progress records. Each record references a shared topic through `progress/topic`; its learner is available through the reverse reference `learner/_knowledge-profile`. Component ownership gives progress the learner's lifecycle, while deleting progress does not delete the topic.

[progress.rs](progress.rs) implements the entity predicates named in the EDN. `valid-profile?` checks that every member has an ID, a real topic, exactly this learner as owner, and a distinct topic within the profile. An empty profile is valid. `valid-progress?` checks that the record has exactly one owner and checks that owner's profile. This also catches topic changes that create duplicates.

Register these callbacks with `register_progress_predicates` in a `TxFunctions` registry supplied to `Database::with_forms`. For a durable writer, register the same checks using EDB's `NativeRegistryBuilder::entity_predicate` with cooperative cancellation; that writer integration remains to be implemented.

On progress writes, request `:db/ensure :progress/validate`. On membership changes, request `:db/ensure :learner/validate` for affected learners and `:progress/validate` for affected surviving progress records, including detached records. Create the learner link and progress in the same transaction. To remove progress, retract the component entity; to transfer it, retract the old link and assert the new link atomically. A learner deletion cascades to its progress.

Specs are opt-in: bypassing `:db/ensure` bypasses these checks. The learner's minimal validation permits ID-only progress placeholders with a topic; ensure each progress record's complete spec before using it in the engine.

Global accuracy lives on the optional component referenced by `learner/performance`, defined in [1-2-learner-performance.edn](../../schema-v2/learner/1-2-learner-performance.edn). Ensure `performance/validate` on that child when writing its four accuracy/mass values. Resolve it through the learner ref; the reverse ref is `learner/_performance`. No separate domain ID is needed. Cardinality one permits at most one summary per learner but does not prevent two learners from sharing a summary. Single ownership and numeric ranges remain application contracts; the progress predicates do not check them. Per-topic accuracy remains on `progress`.

Task history through `learner/activity` remains an ordinary reference collection; its common schema is described in [the schema organization](../../schema-v2/README.md). Task domain guards are not implemented by these progress predicates. `learner/queue` owns the current up-next entries, while each task owns individual learner presentations through `learner-task/items`, defined in `learner/2-2-learner-task-item.edn`. `learner-task/activity` points to the shared activity definition; `task-item/content` points to the presented question, tutorial, or example. Optional `task-item/source-step` links to an authored lesson or multistep placement. The schema does not store duplicate task/item type enums. Queue ownership, index uniqueness, selection enums, and content validation likewise remain application contracts; these progress predicates do not check the queue or implement scheduling.

# Policy and topic difficulty

[configuration.rs](configuration.rs) implements `course-academy.policy/valid?` and `course-academy.topic/valid-difficulty?`. Register these with `register_configuration_predicates` alongside the progress predicates. Like the progress checks, production writer deployment through EDB's native registry remains to be implemented.

Ensure `policy/validate` for complete configurations. The predicate checks supported algorithm/order enums, finite numeric ranges, and cross-setting bounds. Policies use UUID identities. Once referenced by progress or an application, the writer must keep a configuration fixed and use a new identity for changed settings. The predicate sees db-after and checks validity; it does not enforce historical immutability. EDB history remains enabled.

Ensure `topic/difficulty-validate` for every difficulty or evidence write. A starting/expert estimate needs a topic ID, difficulty in [0,1], and its method. Counts can be absent or both zero. Assessment-derived difficulty requires positive total, integer correct/total counts, a nonblank cohort definition, and agreement with correct/total within 1e-12. `topic/validate` invokes the same predicate, allowing completely unknown difficulty but rejecting partially populated estimates. Identity-only topic imports can still use `topic/identity-validate`.

The application selects eligible direct assessment answers and avoids counting an observation twice. Persist both counts and the resulting difficulty atomically; use EDB CAS or a transaction computation for concurrent read-modify-write updates. A changed cohort definition requires recomputation from the intended evidence, not relabeling old counts. The evidence cutoff `topic/assessment-through` is separate from transaction time.

The engine reads authoritative `topic/difficulty`; if absent, it uses `policy/initial-accuracy`. Read all inputs from one database value and record its logical `basis_t()` as `fire-application/basis-t` in the same database. Historical `as_of(basis_t)` reads recover earlier difficulty while that history remains retained. Preserve history on the relevant attributes. Basis T does not identify the event's occurrence time, enforce concurrency, or reproduce external code; policy/algorithm and the actual engine implementation still matter.

The Python engine remains a standalone numerical prototype; there is no completed EDB persistence adapter. The database schema maps to its existing `Policy` fields as follows. All settings are explicit on a complete policy; do not silently fill omitted persisted fields from changing program defaults.

| EDB policy attribute | Python `Policy` field |
| --- | --- |
| `name` | `name` |
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

`policy.algorithm/fire-v1` identifies the current executable formulas and graph rules. `policy/id` is a UUID, not the prototype's calculated `Policy.id` fingerprint. Prototype JSON snapshots and their difficulty-map fingerprints remain supported runtime artifacts, not EDB calibration-set entities. The future adapter must resolve enum entity IDs to their idents and preserve these explicit mappings.

Run the EDB checks from the repository root:

```bash
rustc --edition=2021 tests/validate_fire_schema.rs \
  --extern edb_core=/home/jake/Developer/EDB/target/debug/deps/libedb_core-a0676893826732bc.rlib \
  -L dependency=/home/jake/Developer/EDB/target/debug/deps \
  -o /tmp/course-academy-fire-schema-check
/tmp/course-academy-fire-schema-check
```

The library filename is specific to the installed EDB build. Tests cover policy bounds and enums, topic evidence consistency, optional initial estimates, historical difficulty lookup, and existing progress/event behavior. They do not exercise a production writer or change a persistent database.

The schema harness also installs the `learner` folder, including queue, task, and task-item schemas, as well as the shared activity definitions and task-group/response drafts under `proposed`, and exercises `tests/edb_activity_checks.rs`. Those drafts currently enforce required attributes and native types/cardinalities only; their full domain rules are documented for the future activity controller.

[Task items](../../schema-v2/learner/2-2-learner-task-item.edn) hold responses, results, elapsed time, and optional `task-item/performance`. Whole-task outcome and XP remain on the task. Application code will assemble runtime FIRe `Event` inputs from this evidence; the adapter is not yet implemented.
