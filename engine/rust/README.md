# FIRe engine in Rust

`course-academy-engine` is the library; `fire` is the command-line binary. Both
run without Python. The port preserves the existing engine's rules, including
two correct answers in a row for lesson KPs, three for reviews, accepted earned-XP rules,
and completed diagnostic retries replacing the original placement evidence.
The study app uses `learning` for the current generic activity/step schema,
lesson eligibility, response grading, lesson XP, and per-answer FIRe updates.
Its durable EDB integration is in `scripts/learning_api.rs`. Review and
assessment scheduling for that interface remains to be connected.

Earned XP uses the fixed version-one rules documented in
[3-xp-weights.edn](../../schema/engine/3-xp-weights.edn) and the
[formula report](../../reference/xp-docs/earned-xp-formula-report.md).
`activities::earned_xp` is the shared calculation for lesson, review, assessment,
and multistep awards. It takes base XP and whole-task correct/total counts, with
the final outcome required for partial-credit reviews. Question difficulty and
answer-field count do not weight accuracy. Rounding is `floor(x + 0.5)`, once
at the end; intermediate coefficients use exact rational arithmetic.

Both `runtime` completion and the study app's `learning::continuation` use these
rules. A finished failed lesson/review still receives its calculated XP, while
its mastery/status decision remains separate. Unfinished work receives no final
award. Assessment completion and expiry use every assigned question in the XP
denominator, without creating responses or FIRe evidence for unanswered work.
Diagnostics retain their separate placement rules. Explicit observed/imported
awards remain authoritative, and stored history is not recalculated.

`ActivityRules::use_fitted_xp` is retained for replay compatibility and now
defaults to `true`. Setting it to `false` suppresses automatic partial awards
in the older `runtime` API; the current study app always uses the accepted rules.
Base XP is supplied separately; these changes concern the earned/base adjustment.

```bash
cargo test
cargo run -- demo
cargo run -- replay engine/fire/fixtures/example-input.json
cargo run -- history --output /tmp/history.json --replay-output /tmp/replay.json
cargo run -- live-history --output /tmp/live-history.json
cargo run -- graph-snapshots --ma-root ../MA --without-git --output /tmp/graphs.json
```

The library separates these responsibilities:

- `core` and `calibration`: weighted graph propagation, retention, accuracy,
  difficulty estimation, ranking, and JSON snapshot/restore.
- `activities`: exact rational XP calculations, practice stopping rules, and
  diagnostic placement balances.
- `schema`: hydrate an `EntitySnapshot` into a `LoadedRuntime` and construct
  guarded EDN transaction plans.
- `runtime`: `complete_item`, `transition_item`, and `expire_task` validate activity progression and
  prepare the corresponding state changes for the older activity-specific
  schemas without changing the loaded input.
- `learning`: the current generic lesson delivery and grading path used by the
  study app, including finite question banks and partial imported progress.
- `replay`, `history`, `live_history`, and `graph_snapshots`: the existing local
  replay and evidence-analysis tools.

Call `runtime::complete_item(&loaded, item_eid, CompletionOptions::new(at))`
after grading, supplying the result, responses, and applicable
options. A question result of `None` means an explicit skip. Instruction
completion has no answer result. Use `expire_task` for an assessment or
diagnostic timer; it does not fabricate answers for unseen questions. Use
`transition_item(&loaded, item_eid, "paused" | "started", at)` to pause or resume
the current item. Item elapsed time is derived from its status history, counting
only intervals in `started`; task elapsed time is the sum of its items. Callers
do not supply elapsed durations. Assessment and diagnostic deadlines run from
the task's first start and continue during pauses. Expiry pauses any active
unanswered item and completes the task.

Submit the returned `TransactionPlan.edn` with its `request_key` and
`compare_basis_t` through EDB. Adopt the returned engine state only after a
successful commit. A conflict requires reloading and recalculating; an uncertain
submission requires retrying the original plan. The study app's writer bridge
implements these protections; the full queue scheduler remains application work.

`fire request FILE` exposes the same boundary as JSON. Requests contain `op`
(`complete_item`, `transition_item`, `expire_task`, or a numerical operation), an entity `snapshot`
with `basis_t` and EID-keyed `entities`, `learner_eid`, `policy_eid`, `target`,
and `options`. References are numeric EIDs or installed enum names. Write values
distinguish `{"$keyword":"task-item.status/correct"}`, `{"$uuid":"…"}`, and
`{"$instant":"2026-09-29T00:00:00Z"}` from ordinary strings. Captured instants
also accept integer epoch milliseconds. `fire batch` reads one request per line
and returns one `ok` or `error` result per line. Transition requests use top-level
`status` and `at` values.

Entity snapshots also include `status_history`: an array of added task and item
status assertions containing `entity`, `attribute`, `value`, logical transaction
`t`, and transaction instant `at`. For example:

```json
{"entity": 123, "attribute": "task-item/status", "value": 9001,
 "t": 42, "at": {"$instant": "2026-09-28T00:00:00Z"}}
```

Capture these from EDB history and `db/txInstant`. An omitted history is accepted
for read-only snapshots, but timing updates require the relevant recorded starts
and transitions. Every transaction plan includes an explicit `db/txInstant`
matching the time used to calculate durations.

Numerical FIRe snapshots retain the Python format and can be restored by Rust. Rust normalizes
integer/float representations in typed numerical fields, so debug fingerprints
can differ; replay protection compares the stored event evidence when reading
older receipts. EDB UUIDs, progress identities, and request keys remain stable.

To compare actual calls from the existing Python tests with Rust, run:

```bash
cargo build
PYTHONDONTWRITEBYTECODE=1 python3 tests/rust_parity.py
bash tests/check_rust_edb.sh
```

The last command uses the sibling EDB release library, or `EDB_ROOT`, to install
all current schemas and exercise Rust completion transactions through native
EDB, including their completion CAS and ownership predicates.
