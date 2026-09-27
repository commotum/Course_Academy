# Our FIRe implementation: design, evidence, and validation

Research and implementation date: September 26, 2026.

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

The FIRe core, research, data requirements, EDN definitions, and available-history
analysis are complete for this implementation stage. Validation includes 67
passing tests, native EDB schema checks, 32 history sensitivity scenarios, and
the live-observation audit. The history checks identities, observed behavior,
and consequences of alternative policies; it does not establish learning efficacy.
Prospective retention measurements will guide tuning as the engine is used.

Integrating the core with EDB persistence, a populated encompassing graph, and
the broader activity-delivery application is the next product stage. It does
not require additional access to Math Academy's private learner-state values.

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
state to new EDN definitions and describes the missing inputs.

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

The engine uses pre-event ability to calculate that event's speed and then
updates accuracy from its ordered answers. Answer-level accuracy propagation is
independent of the whole task's pass/fail result: a passed review containing an
incorrect answer still sends negative *ability evidence* upward. Its retention
credit is governed by the explicitly supplied task outcome and quality.

Failed initial lessons retain accuracy evidence while `learned=false`. They
do not start retention or establish mastery. Later successful admission preserves
that evidence. Initial estimates use supplied topic neighborhoods and known
encompassing neighbors, then learner-global accuracy or a declared prior. Direct
and key prerequisites and same-module membership can inform those neighborhoods
without being treated as encompassing edges.

`DifficultyEstimate` separately accumulates actual direct assessment counts only
when both assessment context and qualifying-student status are explicitly given.
With no population data the engine uses a labeled prior. Its quality magnitude
and pass/fail decision must come from an activity-specific grading adapter; the
private MA answer-to-quality function has not been recovered.

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

# Core behavior, calibration, and history-integrity checks.
python3 -m unittest discover -s tests -v
```

The core is standard-library Python. It supports JSON snapshot/restore, atomic
in-memory event application, idempotent retries, conflicting-ID rejection, and
chronological ingestion. Receipts expose before/after state, coverage, discount,
speed, failure multiplier, gated credit, and configuration fingerprints. Global
accuracy counts a direct answer once even when it affects many topic profiles.

An additional operational audit checked that exported snapshots cannot mutate
live configuration, seeded observations cannot leak into earlier events, and
first-learning receipts preserve the preceding unlearned state. The `created`
flag distinguishes a newly initialized prior from an existing profile. Preview
IDs cannot collide with real event IDs, JSON replay preserves neighborhood and
isolated-topic inputs, and retry receipts remain equal after persistence.

`rank` accepts candidates already cleared for prerequisites and content readiness.
Its previews do not mutate learner state. Both student-selected and recommended
events call `apply`; selection source is recorded and has no effect on retention.
XP, question delivery, diagnostic admission, task grading, and the complete MA
scheduler are adjacent application responsibilities, not silently implemented by
this retention model.

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

## What we must track next

The detailed [data-model report](fire-data-model.md) and
[six EDN files](../schema-v2/fire/) provide the reviewable definitions. The main
new information is:

- Expert-supported encompassing edges, weights, and rationale, separate from
  readiness prerequisites, with known zero distinguished from unknown.
- Learner-topic repetition position, anchored memory and interval, learned
  admission, both accuracy channels and their evidence mass, and last direct work.
- Learner-global accuracy channels and declared population topic calibration.
- Actual ordered question outcomes with question/KP/topic identities, occurrence
  time, assessment context, and the task grading/quality decision.
- The exact policy, graph, calibration and prior-neighborhood inputs used for an
  update, plus replayable observation identity and application receipt.

For stronger verification, collect the served task menu and timestamps before
and after work, any legitimately exposed due/profile values, diagnostic/reset
events, and later unaided retention outcomes. These are more informative than
additional XP totals. Start authoring encompassing weights on a small active
topic neighborhood, validating them against representative problems; expand as
new topics enter study. The model can run direct reviews while that work proceeds.

The EDN schemas have native EDB smoke validation. The Python implementation uses
JSON snapshots; an atomic EDB persistence adapter has not been implemented.
Neither the captured content nor an existing learner database was migrated.
