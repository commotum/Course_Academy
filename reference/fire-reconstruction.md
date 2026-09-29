# Our FIRe implementation: design, evidence, and validation

Research snapshot: September 26, 2026. Schema integration updated September 28, 2026.

We now have a working implementation of Fractional Implicit Repetition in
[engine/fire](../engine/fire/). It implements the disclosed structure, including
fractional multihop practice credit, reverse failure propagation, individualized
learning speed, early-repetition discounts, overdue failure penalties, and
review compression. Where the sources leave numerical functions unspecified,
we have chosen explicit, configurable policies for our engine.

**The objective is a solid implementation of our own, using the available
evidence.** Recovering Math Academy's exact parameters or reproducing its
numerical schedules is not an acceptance criterion. Unknown private values are
design choices to resolve and evaluate, not blockers to this implementation.

The current application layer adds [schema hydration and transaction planning](../engine/schema.py),
[activity helpers](../engine/activities.py), and [automatic item completion](../engine/runtime.py).
The full Python suite passes (124 tests), and the native EDB check passes an actual
entity capture → item completion → generated transaction round trip. Run `python3 -m unittest discover -s tests -v` for the current Python suite.
Historical sensitivity scenarios check identities, observed behavior, and the
consequences of alternative policies; they do not establish learning efficacy.

The adapter returns an atomic EDB transaction plan. A durable database writer,
production UI, Rust numerical engine, and complete scheduler remain outside this
implementation. Building those does not require MA's private learner-state values.

## What was investigated

The [source evidence review](fire-source-evidence.md) identifies the local book
chapters, original FIRe article and diagrams, official product descriptions,
author-hosted podcast transcripts, and newer spaced-repetition roadmap. Searches
also targeted public code, patents, named model variables, timing conventions,
path aggregation, and subsequent implementation announcements. It distinguishes
published rules from interpretation and records what the searches did not find.

The [history analysis](fire-history-analysis.md) examines the actual progress CSV,
question observations, locally inferred knowledge profile, catalog identities,
and supplementary captures. The [data model](fire-data-model.md) maps executable
state to the current EDN definitions and application boundary.

An authorized [live-account follow-up](fire-live-account-analysis.md) subsequently
recovered 162 question occurrences with exact topic/example links across nine
tasks, a current graph-color snapshot, and the offered menu. It verifies the
quiz-error/review-topic correspondence and repeated diagnostic question IDs.
The 217-row/308-answer analysis below refers to the original saved snapshot;
the live observations are retained separately. Numeric FIRe state and due times
remain unavailable.

## The recovered structure

1. **Prerequisite and encompassing relationships have different meanings.** A
   prerequisite supports learning readiness; an encompassing weight describes
   actual practice of a component skill. A prerequisite can have zero practice
   coverage. Equivalent skills can be encompassed without a prerequisite path.
2. **Success and failure flow in different directions.** Successful advanced
   work gives credit to encompassed components. Failure on a component supplies
   negative evidence to advanced topics that encompass it. Both can span several
   layers, with fractional attenuation.
3. **Each learner-topic pair has its own retention state.** The sources disclose
   fractional repetition position, a decaying memory quantity, an interval, and
   a learning speed. A completed task is not itself a unit of mastery.
4. **The target's timing matters.** An advanced topic might have been practiced
   recently while a component is due; the component still needs its own early
   discount calculation. The implementation does not discount everything by the
   source topic's memory before propagating it.
5. **Slow topics require explicit review.** Incoming positive implicit credit is
   disabled when the receiving learner-topic speed is below one. This does not
   disable its direct reviews or discard failure evidence.
6. **Ability and difficulty calibrate speed.** Recent answer accuracy informs
   topic ability; correct answers propagate downward and incorrect answers
   upward. Topic difficulty comes from qualifying assessment performance across
   students, independently of the question's easy/moderate/hard label.
7. **Assessment evidence has its own channel.** A newer author interview describes
   maintaining assessment and non-assessment accuracy separately, then averaging
   them. The implementation preserves this distinction locally and globally.
8. **Compression chooses work that supplies several needed repetitions.** A new
   lesson may review already learned components. If no suitable encompassing
   task is available, a component still needs its direct review.

These rules come from the local technical chapters and [original FIRe
article](https://www.justinmath.com/individualized-spaced-repetition-in-hierarchical-knowledge-structures/).
The separate accuracy channels are described in the [January 2026 author
interview](https://www.justinmath.com/math-academy-podcast-6-part-3/).

The author's [September 2024 interview](https://www.justinmath.com/scraping-bits-podcast-107/)
also clarifies that a strong review may receive more than one repetition and a
weak pass less than one. Accordingly, `Event.quality` is a positive magnitude,
not a probability limited to one. XP is never used as repetition credit.

## Published equations and an unresolved timing ambiguity

The public algebra is implemented literally by `public_recurrence`:

```text
r' = max(0, r + speed × decay^failed × rawDelta)
m' = max(0, m + rawDelta) × 2^(-days / interval)
```

The definitions do not specify the operational timestamps around that memory
assignment. If `m` is stored immediately after the preceding event, the literal
expression also decays the newly received credit over the preceding gap.
Another natural event-time interpretation is to decay old memory first, then
add present evidence. These produce different results.

The engine exposes both conventions:

- `decay-before-add`, the default: compute current memory, add current credit,
  and anchor the result at this event's time.
- `literal-add-before-decay`: apply the displayed expression to the stored
  memory and elapsed gap, then anchor the result at this event's time.

Neither is presented as a verified production update convention. The history
experiment compares their consequences. The default's memory is an unbounded
nonnegative model quantity, not a calibrated probability; a value above one is
allowed by the disclosed algebra.

## The concrete local policy

Let `r` be repetitions, `m` current memory, `a` the learner's balanced accuracy,
`d` the topic's qualifying assessment accuracy, and `w` effective graph coverage.

| Calculation | Implemented starting choice | Evidence status |
| --- | --- | --- |
| Interval | `min(36500, 1 × 2^r)` days | Expanding schedule supported; family and constants chosen |
| Current memory | `stored_memory × 2^(-elapsed_days / stored_interval)` | Public decay form with explicit anchor convention |
| Due | `m ≤ 0.5` | Threshold chosen; the equation's base `0.5` does not prove this threshold |
| Early discount | `clamp((1 - m) / (1 - 0.5), 0, 1)` | Chosen monotone function, zero at restored memory, full at due |
| Raw credit | `sign(outcome) × quality × w × early_discount` | Factors supported; exact combination/quality function not recovered |
| Ability | Mean of assessment and practice EWMAs; each starts at `0.8` | Separate channels supported; priors and `alpha=0.2` chosen |
| Fractional accuracy evidence | EWMA step `1 - (1-alpha)^w` | Chosen composable weighting rule |
| Speed | `clamp((a/0.8)^2 / (0.8/d)^2, 0.25, 4)` | Ratio structure supported; transforms and bounds chosen |
| Failure multiplier | `min(4, 1 + max(0, log2(0.5 / max(m, epsilon))))` | Increasing overdue penalty supported; function/cap chosen |
| Path coverage | Maximum product over paths, with explicit pair overrides | Multihop attenuation supported; multiplication/merge/override semantics chosen |
| Initial qualified lesson | `r = speed × quality`, memory `1` | Speed-scaled lesson reps illustrated; initialization details chosen |
| Compression | Simulated due removals per expected minute; future due-time gain breaks ties | Objective supported; greedy optimization/cost model chosen |

An explicit zero coverage overrides an inferred source/destination weight. This
is distinct from an unknown weight. Multiple paths do not independently award
several repetitions for the same event. Weights to different component topics
are not normalized to sum to one: a problem can fully exercise several skills.
Cycles are rejected by this reconstruction. Graph traversal is computed before
the per-target slow-speed gate, so a slow intermediate topic does not block
credit to another eligible target; that transit behavior remains an assumption.

The combined research `apply` call uses pre-event ability, then updates accuracy.
The completion runtime instead calls `apply_accuracy` once per submitted answer
and `apply_retention` when the relevant graded unit closes. Retention therefore
uses the ability accumulated so far. A passed review containing an incorrect
answer still sends negative ability evidence upward, while its retention credit
uses the overall review outcome. Neither path counts an answer repeatedly just
because it affects several topic profiles.

Failed initial lessons retain accuracy evidence while `learned=false`. They
do not start retention or establish mastery. Later successful admission preserves
that evidence. Initial estimates use supplied topic neighborhoods and known
encompassing neighbors, then learner-global accuracy or a declared prior. Direct
and key prerequisites and same-module membership can inform those neighborhoods
without being treated as encompassing edges.

The research `DifficultyEstimate` helper separately analyzes qualifying direct
assessment observations. Current schema stores only optional `topic/difficulty`,
not calibration-count or cohort entities. The adapter uses that estimate or the
policy prior. Grading and positive performance magnitudes are supplied by the
application; the private MA answer-to-quality function has not been recovered.

## Current activity rules

These application rules use the current schemas and explicit local choices;
they do not claim to recover every MA activity controller.

| Activity | Implemented completion and evidence rule |
| --- | --- |
| Lesson | Follow ordered tutorials/KPs and use fresh questions from each KP bank. Two consecutive correct within five questions passes a KP; all topic KPs must pass to establish learning. Prerequisites must already be learned and not due, a conservative local readiness rule. |
| Review | Five questions from one topic, stopping at three consecutive correct or five attempts. Answer order matters in the published FAQ; this precise stopping policy is local. |
| Lesson/review retention | One aggregate unit at completion, scaled by mean supplied submitted performance. Answers have already updated accuracy individually, including failed initial work. |
| Assessment/multistep retention | Each submitted item contributes `performance / questions_for_its_topic_in_the_definition`, a local allocation policy. Multistep placements retain authored order. |
| Diagnostic | Follow the prepared probe graph; missing ordinary branches end the path. Offer an available alternate after any submitted wrong answer, without a timing gate, and require an explicit retry choice. Alternate probes do not offer another retry. |
| Placement | Accumulate signed prerequisite-graph balances separately from FIRe: correct downward, wrong upward, once per reached topic. Supplied weights may reduce slow-correct credit. Final positive balances initialize previously unlearned topics; established retention history is preserved. |
| Skip | A presented skip consumes a practice attempt and breaks its streak, but contributes no submitted-answer accuracy. The configurable local diagnostic default gives negative placement evidence. Unpresented questions create no items. |

The [diagnostic chapter](<The Math Academy Way/V-TECHNICAL-DEEP-DIVES/30-Technical-Deep-Dive-on-Diagnostic-Exams/30-Technical-Deep-Dive-on-Diagnostic-Exams.md>)
supports signed balances, directional propagation, reduced slow-correct credit,
and positive balances becoming repetitions. Exact time weighting, path
deduplication, and retry accounting remain local choices. The current accumulator
retains both wrong and alternate answers; it does not silently cancel the first.

XP is independent of mastery and retention. The [XP analysis](mathacademy-xp-analysis.md)
supports observed perfect-lesson `R(1.25B)` and perfect-review `B+2` candidates.
Assessment `max(0, R(1.2B(p−0.35)/0.65))` and multistep `R(B(2.25p−1))` are fitted
hypotheses enabled by an explicit runtime switch, where `R(x)=floor(x+1/2)`.
Partial lesson/review and diagnostic awards require a caller-supplied value or
remain unknown. The runtime does not invent missing workload baselines.

## What runs

```bash
# Published multiplication example: one review can satisfy three due topics.
python3 -m engine.fire demo

# Apply a JSON scenario, retaining state and per-topic receipts.
python3 -m engine.fire replay engine/fire/fixtures/example-input.json

# Rebuild the local history audit and execute the sensitivity scenarios.
python3 -m engine.fire.history \
  --output engine/fire/fixtures/history-observations.json \
  --replay-output engine/fire/fixtures/history-replay-results.json

# Core, activity, adapter, and history-integrity checks.
python3 -m unittest discover -s tests -v
```

The core is standard-library Python. It supports JSON snapshot/restore, atomic
in-memory event application, idempotent retries, conflicting-ID rejection, and
chronological ingestion. Receipts expose before/after state, coverage, discount,
speed, failure multiplier, gated credit, and configuration fingerprints. Global
accuracy counts a direct answer once even when it affects many topic profiles.
These are runtime/debug receipts, not domain entities in schema.

An additional operational audit checked that exported snapshots cannot mutate
live configuration, seeded observations cannot leak into earlier events, and
first-learning receipts preserve the preceding unlearned state. The `created`
flag distinguishes a newly initialized prior from an existing profile. Preview
IDs cannot collide with real event IDs, JSON replay preserves neighborhood and
isolated-topic inputs, and retry receipts remain equal after persistence.

`rank` accepts candidates already cleared for prerequisites and content readiness.
Its previews use retention-only simulation and do not create answer accuracy.
The completion runtime applies the same grading and learning rules regardless of
queue selection mode. It validates delivery against existing content definitions;
it does not assemble assessments, generate diagnostic graphs, assign remediation,
or implement a complete queue scheduler.

`EntitySnapshot` reads a captured EDB entity map at one basis; the adapter is not
a general EDN parser or database connection. `complete_item` produces an item
completion compare-and-swap plus result/response, progress, performance, and
applicable task/XP writes. The writer must submit the returned request key and
exact basis guard and retain that plan for uncertain-outcome retries. No loaded
engine state is mutated before commit. This protects the existing occurrence;
fresh identities for duplicated real-world work still require application care.
For timed assessments and diagnostics, `expire_task` closes the attempt using
existing evidence without inventing unanswered items or partial-exam XP. The
application owns the timer and submits the resulting guarded task transaction.

Policy settings can change under the same `policy/id`; historical database views
recover earlier values. Existing progress retains its stored interval until an
engine update recomputes it. There is no automatic mass reschedule and no separate
domain event or application receipt. `Policy.name` is a Python prototype label,
not a persisted engine input.

## Verification against the available history

The actual local record contains **217 activities**. The question-observation
snapshot covers **34 tasks and 308 answers**; all 34 exact task-ID joins agree
with the current progress rows. Its metadata describes an older 214-row snapshot.

Only **11 sampled lesson/review tasks, containing 70 answers**, have retained
task-topic identities usable by the replay. Treating those answers as evidence
for their task's topic is itself an explicit mapping assumption. The other
238 answers lack retained question-topic identities. They cannot be propagated
through a graph merely from their difficulty labels or task titles.

The saved [replay results](../engine/fire/fixtures/history-replay-results.json)
contain actual executions under alternative outcome granularity, initial
repetition position, interval growth, clock assumptions, and memory update
ordering. An elapsed-question-time clock is included only as a sensitivity
control: it is incomplete and is not the calendar-day clock in the source model.
The report records the conditions under which sampled reviews would have been
due and how different assumptions change the final states.

Further inspection found 31 saved course graphs with 6,627 node occurrences.
Public legacy renderer code maps five RGB colors to display repetition values
1–5. The other dark-blue color is a default branch, not a proved `6+` category.
The captures date to April 9, 2026; their learner identity is not recorded, and
the renderer was retrieved later. These are conditional, categorical snapshot
constraints. The display field's relationship to continuous FIRe `repNum` is
unknown. The [source review](fire-source-evidence.md#recovered-display-mappings)
also distinguishes a newer renderer's `stability` field from those legacy colors.
The [extracted graph observations](../engine/fire/fixtures/graph-snapshot-observations.json)
cover 2,590 distinct topics, including all 129 topic IDs in the progress history.
However, 217 topics have conflicting colors across course snapshots. Without
resolving course context, capture identity, time, and display semantics, those
colors cannot be merged into one authoritative learner-topic retention value.

There are **zero observed numeric FIRe state transitions or due timestamps**
against which to score numerical predictions. Completion times can be later than
serving times; missing intermediate work, diagnostic resets, weights, and starting
profiles can change any predicted schedule. Agreement with a review occurrence
is therefore a compatibility observation, not prediction accuracy. The local
knowledge profile also contains prerequisite-based inferences and stale entries;
it is not a dump of MA's memory or repetition values.

The test suite verifies the published algebra and directional examples, policy
boundaries, graph behavior, ability channels, event safety, persistence, and
history joins. It does **not** turn guessed numerical constants into empirically
verified MA parameters. No weights were invented from prerequisite edges, and
no XP-to-mastery substitution was made to make the replay appear complete.

## Inputs and verification boundary

The detailed [data-model report](fire-data-model.md) and
[current EDN schemas](../schema/README.md) provide the reviewable definitions.
The engine consumes:

- Expert-supported encompassing edges, weights, and rationale, separate from
  readiness prerequisites, with known zero distinguished from unknown.
- Learner-topic repetition position, anchored memory and interval, learned
  admission, both accuracy channels and their evidence mass, and last direct work.
- Learner-global accuracy channels and optional topic difficulty estimates.
- Actual ordered task items, submitted responses, result, occurrence time, and
  supplied performance. Question/KP/topic relationships come from shared content.
- Policy, graph, and state from one database basis, with task-item identities and
  EDB history supplying the durable observation and configuration context.

For stronger verification, collect the served task menu and timestamps before
and after work, any legitimately exposed due/profile values, diagnostic/reset
events, and later unaided retention outcomes. These are more informative than
additional XP totals. Start authoring encompassing weights on a small active
topic neighborhood, validating them against representative problems; expand as
new topics enter study. The model can run direct reviews while that work proceeds.

The EDN schemas have native EDB checks, and the Python adapter prepares guarded
atomic writes verified through the native in-memory EDB transaction path. The durable writer still needs to
submit those plans with registered predicates; this is separate from the core's
JSON snapshot support. Neither captured content nor an existing learner database
was migrated.
