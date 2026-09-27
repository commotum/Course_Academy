# FIRe data model and acquisition plan

For the simpler application integration proposal, start with [How the learning engine plugs into our schema](fire-schema-integration.md). The contract below describes the standalone Python prototype; its policy, calibration, and receipt entities are not all required in the final application model.

This is the data contract for [our FIRe implementation](../engine/fire/core.py). It records the state and evidence our engine needs, drawing on the published mechanisms and observed behavior. The [learner and progress schemas](../schema-v2/learner/) and remaining [FIRe schemas](../schema-v2/fire/) add retention and performance data without changing the existing course, topic, lesson, KP, question, or answer models. The separate [implementation explanation](fire-reconstruction.md) owns the executable equations and policy choices.

The smallest useful system needs an explicit encompassing graph, an initial learner-topic profile, actual graded work, and a specified policy. A prerequisite graph plus completed-task XP is insufficient. It is possible to run an honest direct-review baseline before any encompassing weights have been established.

The subsequent [live-account inspection](fire-live-account-analysis.md) supplies
162 question occurrences with source identities and outcomes. It confirms why
occurrence identity must remain separate from question identity: two question
IDs repeat across diagnostics. All captured topic fragments identify example
content, not lesson placement IDs. It also distinguishes quiz completion-time
labels from individual answer timing. The optional ordered observation payload
can preserve these fields; they do not justify inventing a retention-quality
value, diagnostic admission/reset state, or an unambiguous event timestamp.

## What the sources establish

The author describes positive repetition credit flowing from advanced topics to encompassed component topics, failures propagating in the reverse direction, fractional coverage, discounting early repetitions, and a learning speed calibrated for each learner-topic pair. The published algebra is:

```text
r' = max(0, r + speed × decay^failed × rawDelta)
m' = max(0, m + rawDelta) × 2^(-days / interval)
```

The publication does not supply the complete functions for interval growth, early discount, failure severity, ability-to-speed conversion, graph path aggregation, or operational timestamp ordering. Those are explicit local choices in the implementation. The literal recurrence and the operational decay-before-add interpretation must remain distinguishable. See the [saved primary article](<Optimized, Individualized Spaced Repetition in Hierarchical Knowledge Structures Introducing Spaced Repetition Compression and Fractional Implicit Repetition (FIRe)/Optimized, Individualized Spaced Repetition in Hierarchical Knowledge Structures Introducing Spaced Repetition Compression and Fractional Implicit Repetition (FIRe).md:187>).

| Meaning | Public support | Local representation or choice |
| --- | --- | --- |
| Encompassing differs from prerequisite | A prerequisite may receive no practice credit | Dedicated directed edges; never automatically assign prerequisite weights |
| Partial coverage | Explicit expert weights describe fractions of component practice | Finite weights in `[0,1]`; zero is an explicit value |
| Multilayer propagation | Credit and penalties extend through several levels | Maximum-product aggregation and direct-pair override are reconstruction choices |
| Weak learner-topic implicit credit | Incoming implicit positive credit is discarded when learning speed is below one | Explicit configurable gate, evaluated separately from ability evidence |
| Ability | Recent answers matter; both global and topic estimates are described | Separate assessment/practice estimates and evidence masses |
| Assessment versus practice accuracy | The author describes maintaining the two averages and averaging them together | Arithmetic mean is our reading of that description; the precise recency kernel, alpha, and priors are chosen locally |
| Topic difficulty | Aggregate assessment accuracy among qualifying students | Direct assessment counts and an explicit cohort rule; no E/M/H substitution |
| Initial learning | Topics are taught through mastery learning before retention tracking | Explicit `learned` admission; failed initial work can still update ability |

The [primary article](https://www.justinmath.com/individualized-spaced-repetition-in-hierarchical-knowledge-structures/) explains the speed gate. The later [author interview, approximately 21:33–23:42](https://www.justinmath.com/math-academy-podcast-6-part-3/) describes the separate accuracy averages. The book's [technical chapter](</home/jake/Developer/MA/DATA/The Math Academy Way/V-TECHNICAL-DEEP-DIVES/29-Technical-Deep-Dive-on-Spaced-Repetition/29-Technical-Deep-Dive-on-Spaced-Repetition.md:112>) describes topic ability and assessment-based topic difficulty.

## Schema files and ownership

Install all content, data, learner, engine, and proposed activity schema files before transacting domain records; filename order is for navigation. These files contain attribute definitions and opt-in entity specs, not production MA weights or learner profiles.

| File | Records | Why it exists |
| --- | --- | --- |
| [1-policy.edn](../schema-v2/fire/1-policy.edn) | `policy` | Names the executable algorithm and stores complete typed settings |
| [1-1-learner.edn](../schema-v2/learner/1-1-learner.edn) | `learner` | Learner identity and refs to owned state, current queue, and task history |
| [1-3-learner-progress.edn](../schema-v2/learner/1-3-learner-progress.edn) | `progress` | One retention and accuracy profile per learner-topic pair |
| [1-2-learner-performance.edn](../schema-v2/learner/1-2-learner-performance.edn) | `performance` | One optional learner-owned global accuracy summary across topics |
| [4-3-topic-difficulty.edn](../schema-v2/data/4-3-topic-difficulty.edn) | Additional `topic` attributes | Current difficulty estimate and optional qualifying assessment evidence |
| [2-3-learner-task-performance.edn](../schema-v2/learner/2-3-learner-task-performance.edn) | `fire-event` | One graded topic-specific task performance result before propagation |
| [07-application.edn](../schema-v2/fire/07-application.edn) | `fire-application`, `fire-update` | Records how one event changed or deliberately did not change state |

Topic, KP, and question refs point to existing content entities. No new content identities, copies, or versions are introduced. Each learner owns one progress record per topic through `learner/knowledge-profile`. Entity predicates enforce ownership and topic uniqueness when the specs are ensured; no reverse learner attribute or learner/topic composite is stored. Shared knowledge carries across concurrent courses. Course membership still controls curricular scope and prerequisite eligibility outside this retention transition.

Encompassing relationships are defined in [4-2-encompassing.edn](../schema-v2/data/4-2-encompassing.edn) and owned through `topic/encompasses`. Each record contains a component topic, weight, and optional rationale; the parent topic supplies the source. There is no separate graph entity or graph reference on application receipts. Rust can assemble its runtime graph from these relationships and the existing topic records, including topics without encompassings.

Policy UUIDs identify configurations; they are independent of the Python engine's runtime fingerprints. The writer keeps a policy fixed after it is used and creates a new identity for changed settings. Current topic difficulty and its evidence live directly on the topic. An application records the exact input database basis T, allowing historical reads of those values without copying them into calibration-set entities. Read all inputs from one database value and retain their history.

## State and time

| Engine field | EDB attribute | Meaning |
| --- | --- | --- |
| `TopicState.repetitions` | `:progress/repetitions` | Nonnegative fractional repetition position, not a count of completed tasks |
| `memory` | `:progress/memory` | Model memory at its anchor; not a probability and not constrained to be at most one |
| `memory_at` | `:progress/memory-at` | Instant at which stored memory applies |
| `interval_days` | `:progress/interval-days` | Positive interval used to decay that anchored memory |
| `ability.assessment_accuracy` | `:progress/assessment-accuracy` | Assessment-channel accuracy estimate |
| `ability.practice_accuracy` | `:progress/practice-accuracy` | Non-assessment accuracy estimate |
| `ability.assessment_mass` | `:progress/assessment-mass` | Effective assessment evidence mass |
| `ability.practice_mass` | `:progress/practice-mass` | Effective non-assessment evidence mass |
| `learned` | `:progress/learned` | Admission to retention tracking, distinct from current recall |
| `last_direct_at` | `:progress/last-direct-at` | Last direct practice, unaffected by receiving only implicit credit |

The four ability fields also exist under `:performance/*` on the learner-global summary referenced by `learner/performance`. This optional cardinality-one component has no separate domain ID; look it up through its learner. Ensure `performance/validate` on writes to require all four values. Single ownership and numeric ranges remain application contracts. Global ability updates from directly observed answers once; propagating one answer to several topics must not count it several times globally. The effective accuracy is computed from the two channels rather than stored as an independently mutable third estimate. Per-topic accuracy remains on `progress`; failed initial lessons can update it while `progress/learned=false`, without silently establishing mastery.

The engine uses fractional elapsed days. The persistence adapter should map UTC instants to days from one fixed epoch, such as `unix_seconds / 86400`, and apply the same conversion to every event and state anchor. Local calendar dates and earned XP are not elapsed time. Simulated relative-day experiments remain simulations; do not invent calendar timestamps for them.

Memory at time `t` is derived from the anchored value and stored interval. Due time and learning speed are also derived from state, policy, and calibration, so they do not need separately mutable authoritative fields. The schema does not store a separate latest-event timestamp on the learner. The prototype's chronological processing checks remain in application code; incorporating older evidence may require recomputing progress in order.

`topic/difficulty` now has an explicit local scale: expected assessment accuracy in [0,1], with lower values meaning harder material. It is the authoritative engine input. Its method identifies an initial estimate, expert estimate, or assessment-derived value. Positive integer assessment counts require a nonblank cohort definition and a matching correct/total ratio; update the counts and difficulty atomically. Estimated values may omit counts or use two zero counts. When the value is absent, use `policy/initial-accuracy`. The schema does not claim this numeric scale was recovered from MA storage. It is distinct from question-level easy/moderate/hard labels or expected solve time.

## Performance and application receipts

The file `learner/2-3-learner-task-performance.edn` names the role of the record: graded topic-specific performance prepared from task evidence. Its attributes retain the `fire-event/*` namespace and existing engine contract; no task ownership link is added by the move. An event has one learner, one directly assessed topic, time, graded outcome, positive quality magnitude, activity kind, explicit assessment channel, initial-learning flag, ordered question outcomes when available, and source/context label. This mirrors `Event` in the core. Quality may exceed one; it is neither an accuracy percentage nor earned XP. A task adapter must define the grading and quality rule before emitting events.

Several questions can support one topic-level event. Conversely, an assessment spanning several topics can produce distinct topic events under an explicit aggregation rule. Do not award a full repetition per question merely because a task contained several questions. Unknown correctness is not converted into `false`; an unavailable sequence remains unavailable. When the engine falls back to the event's passed/failed outcome for ability updating, that is a declared approximation.

Ordered Boolean outcomes are stored as an EDN vector inside a string. An EDB cardinality-many Boolean attribute would keep only the set of values and lose both order and repeated outcomes. Optional question observations can preserve occurrence IDs, actual question/KP IDs, timing, prior exposure, and hint/reveal conditions for future quality calibration. Question pool membership remains in the content model; answering a question never reassigns it to another KP.

`(learner, event ID)` is the observation identity. Native composite uniqueness prevents duplicate rows, but it does not prove identical payloads or prevent an application from crediting an existing event again. The writer must compare the complete event fingerprint and make identical retries no-ops while rejecting conflicting payloads.

Each receipt links the event, event hash, policy, input database basis T, processing time, pre-event input bundle, and per-target update traces. The input bundle includes topic states, global ability, latest accepted time, and any configured ability-neighborhood inputs. Topic states alone cannot reproduce a new topic's prior. Existing direct/key prerequisites and same-module membership can inform those neighborhoods; none is automatically an encompassing edge.

The trace preserves the engine's update dictionary: direct/implicit direction, coverage, early discount, raw delta, speed, failure multiplier, gate result, state before/after, and derived due time. Unlearned targets retain their ability changes and an explicit retention-skip reason; they receive no retention credit. The schema no longer preserves immutable encompassing graph snapshots; the Python prototype's snapshots remain separate from this EDB model.

Receipt insertion, learner-global ability, chronological frontier, and learner-topic state changes must commit atomically. Configuration experiments use isolated model state. Comparing another policy is not another successful repetition by the learner.

## Real data still needed

The [inventory](ma_data_inventory.md) found 6,560 direct-prerequisite pairs and 9,167 step/key-prerequisite rows, but no production encompassing edge/weight dataset. It also found no populated topic-difficulty estimates, learner-topic retention profile, or complete historical question-ID-linked results. The related history contains completed tasks and some reduced question features; XP and completion do not fill those missing fields. Saved course graph HTML also contains categorical topic colors, but no recovered numeric FIRe values or authoritative color-to-state mapping; those colors must not be converted into repetition, memory, or speed values.

Acquire the missing inputs progressively:

1. **Start with a small, explicitly selected topic set.** Reconcile existing topic and KP identities, verified answers, and readiness. Use no encompassing edges initially if none have been justified; label this a direct-review baseline.
2. **Build a small expert-reviewed encompassing graph.** Direct/key prerequisites supply candidates. Inspect a representative set of advanced-topic problems and ask which component procedures must actually be performed. Record coverage rationale, sample size, and confidence separately from the weight. Include known zero coverage and non-ancestor cases when justified. Book-diagram values remain illustrations unless independently established for these actual topics.
3. **Initialize learner state explicitly.** Use a fresh diagnostic or reviewed placement decision, or declare a local starting prior. Existing completion history may inform a hypothesis; it cannot recover MA's hidden repetition position or memory. Keep unlearned topics outside retention credit while retaining answer-based ability evidence.
4. **Collect direct graded events prospectively.** Capture actual question/KP/topic IDs, ordered outcomes, timing, assistance, exposure, and assessment channel. Define one aggregation/quality contract, then measure later unaided recall. Keep recommendations and preview simulations from creating performance evidence.
5. **Calibrate ability and difficulty.** Start with clearly labeled priors. Update learner accuracy from observed answers; estimate topic difficulty only from qualifying direct assessment observations. Declare cohort eligibility instead of treating “serious student” as an invisible database property. One learner's data is not a population calibration.
6. **Evaluate the local choices.** Compare prediction and review burden against a direct-review baseline and later retention outcomes. Change discount, interval, propagation, and speed choices through named configurations. Fitting XP awards alone does not validate retention or implicit credit.

The prerequisite and encompassing graphs may differ in topology. Non-ancestor coverage is allowed. The current implementation rejects encompassing cycles and applies maximum-product path aggregation with explicit-pair overrides, including zero: these are concrete reconstruction rules, not recovered MA edge semantics.

## Validation and implementation boundary

The reproducible native smoke-check source is [tests/validate_fire_schema.rs](../tests/validate_fire_schema.rs).
From the repository root, using the installed EDB build:

```bash
rustc --edition=2024 tests/validate_fire_schema.rs \
  -L dependency=/home/jake/Developer/EDB/target/debug/deps \
  --extern edb_core=/home/jake/Developer/EDB/target/debug/deps/libedb_core-a0676893826732bc.rlib \
  -o /tmp/course-academy-fire-schema-validation
/tmp/course-academy-fire-schema-validation
```

The library hash is build-specific; use the matching `edb_core` artifact after
rebuilding EDB.

Native EDB checks install all current schemas and validate representative topic, policy, progress, event, and receipt records. The tests reject unsupported policy/method enums, missing settings, nonfinite numeric values, inconsistent policy bounds, fractional or inconsistent answer counts, stale difficulty ratios, missing assessment cohorts, duplicate learner-topic progress, shared progress ownership, and invalid event identities/types. They accept unknown topic difficulty and explicit initial/expert estimates. A historical read at the saved input basis retrieves the original difficulty after later evidence updates.

[Registered Rust predicates](../engine/edb/configuration.rs) enforce policy ranges and topic difficulty consistency when the specs are explicitly ensured. They do not implement mathematical correctness checks, production policy immutability, eligibility selection, duplicate assessment ingestion prevention, or the engine persistence transaction. Those are writer/application responsibilities. Deploy the predicates to the executing writer; local registry tests alone do not deploy them. The schema reference explains that [`:db/ensure`](edb-schema-reference.md#entity-specs) must be requested explicitly and does not install a permanent table-wide constraint.

The Python engine currently persists its own JSON snapshots. These EDN files define the corresponding EDB data model; they do not implement a database adapter. The EDB receipt's exact pre-event input bundle is a future adapter requirement: current engine receipts retain updated targets, global ability changes, and configuration fingerprints, while a retained pre-event snapshot carries the additional configured neighborhood and state inputs needed for replay. A current receipt alone must not be presented as a standalone replay bundle. A future adapter must preserve the mappings and atomicity described above. The operational engine tests and the native schema smoke check establish different things and should be reported separately.
