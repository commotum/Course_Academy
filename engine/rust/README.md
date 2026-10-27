# FIRe engine in Rust

`course-academy-engine` is the library; `fire` is the command-line binary. Both
implement FIRe and activity completion, including
lesson KPs that advance on two consecutive correct answers, fail the lesson on
two consecutive incorrect answers or skips, and advance after five questions
when neither streak occurs; three correct answers in a row for reviews; accepted earned-XP rules,
and completed diagnostic retries replacing the original placement evidence.
The study app uses `learning` for the current generic activity/step schema,
lesson eligibility, response grading, lesson XP, and per-answer FIRe updates.
`retrieval` connects reviews and timed assessments to the same generic
activity/step definitions and learner-task/item history. Their durable EDB
integration is in `scripts/learning_api.rs`; the Study UI uses the same player.

The profile's Focused mode switch controls focused study. When
enabled, the Study feed offers lessons, reviews, and assessments only from topics
directly in `learner/targets`, including every topic in a saved quiz or retake.
Queue-only topics and prerequisites are excluded from the feed. Explicit Study
now and Review Topic selections, including starting and resuming those activities,
remain available for any topic under their normal content and lifecycle rules.
Assessment age, XP, fresh
question, and minimum-new-topic rules still apply. The targets graph initially
fits the overview at prerequisite depth zero; disabling the switch restores
the normal depth-two default. Changes apply immediately and are saved per
learner in the local server's preferences, without a database attribute.
`engine/rust/study_mode.rs` supplies the default before a preference is saved.
The app applies the preference to its immutable capture. Database-free fixtures can
exercise either policy through the capture's transient `focused_mode` field.

In engine mode, opening Study and finishing a task refresh the recommendations.
Due reviews require explicitly learned FIRe state and five fresh gradable
questions; the existing three-correct streak stops a review after at most five
presentations. A bounded pool of 16 due topics is ranked by FIRe review coverage,
and up to three new review definitions are prepared per refresh. Obsolete
unstarted tasks are locked; started and paused work remains resumable in both
modes. Self-directed mode combines explicit queued lessons with targets and their
unfinished prerequisites. Target preparation stops at historically studied topics;
their prerequisite ancestry also counts as covered, including when another studied
branch establishes that knowledge. Evidence includes learned progress, positive
legacy repetitions, and completed lessons or reviews. This planning inference does
not write mastery or remove due reviews. Queue and Study-now requests retain their
manual overrides. New target preparation requires its prerequisite frontier to be
known and the same five fresh usable questions per KP as queued lessons. Ordinary
spaced reviews and activity-history assessments remain available across courses
in both modes.

Assessments become available after 120 finalized practice XP since the
last ordinary assessment completion or expiry and become required at 150 XP.
Creation also requires at least five distinct never-assessed topics, each
explicitly learned, with recorded successful learning at least 48 hours ago and
a fresh rated standalone question. Learned topics qualify at every graph layer;
the layer-30 floor limits ordinary practice recommendations, not quizzes or
required follow-up practice for assessment misses. Every new ordinary assessment includes at
least five such topics; the remaining slots may sample previously assessed
topics. If fewer than five are available, XP continues accumulating and study
remains available even above 150 XP. The status reports the new-topic count and
the waiting reason. Never-started quizzes are rechecked before offering or
starting them; started routes and retakes retain their existing rules.
There is no mandatory prior retrieval event. This provisional topic-age floor applies
only to ordinary assessments; reviews do not restart the learning-age clock,
and assessment-miss reviews have no age delay. Assessment selection considers
the learner's whole learned activity history without a course restriction or
course preference, in either study mode. Newly prepared assessments omit a
course association, and existing pending assessments survive course switches.
Migrated terminal outcomes count toward cadence, mastery, and remediation even
without a local start event. `learner-task/finished-at` preserves an original
completion/failure date from migration evidence; otherwise the terminal status
transaction supplies the latest known completion bound. Saved progress and XP
are read rather than applied again. Assessments select one fresh question
per topic, favor previously unassessed topics, and freeze the route at start.
The 15-minute wall-clock limit continues while paused. Answers are graded and
recorded immediately, but correctness, feedback, and solutions are hidden by
the task API until completion. Explicit skips create remediation; expiry does
not fabricate wrong-answer evidence for unanswered or unpresented questions.
Failed ordinary reviews lower repetition progress and retain their accuracy
penalties, while completed review re-exposure refreshes current memory just
above the due threshold. The next ordinary review follows memory decay instead
of an activity counter. Failed remediation reviews still lead to their linked
lessons; observed assessment misses still lead to immediate required reviews,
including topics outside the current course.

The runtime policy's `failed_review_refresh_fraction` defaults to `0.01` and
requires no new EDB attributes. It restores 1% of the log-memory headroom between
the review threshold and normal restored memory. The resulting delay is
`updated_interval * 0.01 * log2(restored_memory / threshold)`: with the seeded
defaults, 0/1/2/3 remaining repetitions yield about 14/29/58/115 minutes.
The existing failure severity and learning speed determine the repetition
penalty and resulting interval. This is an initial approximation of captured
return behavior, not a recovered private parameter. Queue priority can postpone
the visible offer further. Only the directly reviewed learned topic gets this
refresh; propagated penalties, answer-only events, failed lessons, and assessment
misses do not. Accuracy-only question updates cannot refresh retention. Zero
disables the refresh for comparative numerical replays; JSON engine snapshots
include the parameter and policy fingerprint, and existing stored EDB policies
use the runtime default. Historical states are not rewritten on load.

Assessment assembly provisionally budgets one/two/three minutes for an
easy/moderate/hard question, aiming for the longest feasible duration up to
15 minutes after maximizing difficulty-band coverage. Question count varies.
Difficulty distributions come from the active policy's owned question-weight
records. First-time topics use the initial assessment distribution (currently
50/40/10 easy/moderate/hard). Previously assessed topics multiply those weights
by 0.4/1.25/3.0, giving 20/50/30 with the current policy. This is one fixed
repeat preference, not an escalation on every subsequent assessment.

Within a feasible difficulty band, ordinary quizzes choose a KP before choosing
a fresh question uniformly from that KP. KP weights rise linearly from 1 to 2
over the learner's latest successfully completed lesson's authored KP sequence.
One-KP lessons have weight 1. Membership collections and entity IDs do not define
sequence; missing or malformed legacy lesson routes receive neutral KP weights.
Unavailable KPs/bands are omitted and the remaining weights are normalized, so
later KPs remain a preference and large question banks do not dominate selection.
Budget and band-coverage constraints can change a particular quiz's proportions.

Retakes preserve the original topics and KPs and explicitly use the assessment
remedial distribution (currently 45/40/15); ordinary repeat/KP preferences do not
alter retakes. A missing assessment record is a configuration error. New
selections use synchronized database values; already assembled routes remain fixed.
Review XP uses a provisional 4.5-minute estimate.
These estimates affect selection and base XP, not measured FIRe performance.
All served questions and frozen active retrieval pools are excluded from other
practice draws. Preparing an unstarted definition records no presentation or
clock; stale unstarted definitions are replaced when Study is refreshed.

The type-specific `runtime` remains for existing replay/diagnostic tooling; the
live lesson, review and assessment paths use shared activity and step records.

Target-based planning reads its target set only from `learner/targets`. Linked
assignments provide deadline context for topics already in that set. Completing
or failing an assignment leaves targets and their priority weights unchanged;
explicitly removing a target takes effect even while its assignment stays linked.

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
Base XP is computed by `base_xp` from content and the expected difficulty distribution. No individual difficulty labels are required. Topic workload multipliers default to 1.0; expected seconds are stored on activities and base XP is frozen on attempts at start. See [the selected formula](../../reference/xp-docs/expected-distribution-base-xp.md).

```bash
cargo test
cargo run -- demo
cargo run -- replay engine/rust/fixtures/example-input.json
cargo run -- history --output /tmp/history.json --replay-output /tmp/replay.json
cargo run -- live-history --output /tmp/live-history.json
cargo run -- graph-snapshots --ma-root ../MA --without-git --output /tmp/graphs.json
```

The library separates these responsibilities:

- `core` and `calibration`: weighted graph propagation, retention, accuracy,
  prerequisite-weighted initial accuracy forecasts, ranking, and JSON snapshot/restore.
- `activities`: exact rational XP calculations, practice stopping rules, and
  diagnostic placement balances.
- `schema`: hydrate an `EntitySnapshot` into a `LoadedRuntime` and construct
  guarded EDN transaction plans.
- `runtime`: `complete_item`, `transition_item`, and `expire_task` validate activity progression and
  prepare the corresponding state changes for the older activity-specific
  schemas without changing the loaded input.
- `learning`: the current generic lesson delivery and grading path used by the
  study app, including finite question banks and partial imported progress.
- `symbolic`: bounded exact symbolic equivalence for entered answers. It handles
  polynomials, rational expressions, supported radicals and powers, common
  function identities, complex coefficients, and explicit special tokens.
  Unsupported comparisons return an error before learner results are saved.
  See [the checker documentation and verification](../../reference/symbolic-grader-2026-10-05/README.md).
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

Numerical FIRe snapshots use format 1 with two-channel `ability` state.
Receipt fingerprints cover the event and update mode; retries must match both.
EDB UUIDs, progress identities, and request keys use deterministic encodings.

To check the native EDB boundary, run:

```bash
bash tests/check_rust_edb.sh
```

The command uses the sibling EDB release library, or `EDB_ROOT`, for the native
schema/predicate harness. Its obsolete activity fixture currently prevents a
complete run; see [the validation notes](../edb/README.md).
