# Our FIRe implementation: checks against learner history

The available history informs and exercises our FIRe implementation. This report
checks source identities and outcomes, separates observations from assumptions,
and compares the consequences of concrete policy choices through reproducible
replays. The live follow-up adds direct evidence about remediation, question
reuse, and topic/example identity.

The purpose is to build and evaluate our own engine. Exact agreement with Math
Academy's hidden retention values is not required. The history has no numeric
FIRe state transitions or due timestamps; that bounds what retrospective
comparisons can establish, without blocking our implementation. Its chosen
parameters can be tuned against future observations of actual retention.

The implementation in `engine/fire/history.py` joins records by exact task ID,
checks agreement, preserves unknown outcomes, and runs explicitly labelled
alternative assumptions through `FireEngine`. It never converts earned XP,
Completed status, prerequisite edges, or inferred profile labels into FIRe truth.

**Later evidence:** the authorized [live-account inspection](fire-live-account-analysis.md)
adds 162 question-ID/topic/example-linked occurrences across nine tasks and a
current graph/menu snapshot. Counts and missing-identity statements in the
original-snapshot sections below describe the retained 217-row CSV and reduced
34-task JSON. The new source is separate and must be deduplicated by task and
occurrence before combining it with those observations. It still supplies no
numeric FIRe state transitions or due timestamps.

## Sources and exact joins

| Source | Recovered evidence | Limit |
| --- | --- | --- |
| `reference/progress.csv` | 217 tasks, 2025-02-27 11:13 through 2026-09-24 17:05; 186 lesson/review rows have catalog topic IDs covering 129 topics | Completion times have minute resolution and no verified time zone; no task-level FIRe pass/fail or state |
| `reference/mathacademy-xp-observations.json` | 34 tasks, 308 ordered question outcomes, displayed difficulty and elapsed seconds | Reduced observations omit question IDs, topic/KP links and individual answer timestamps |
| `reference/mathacademy-activity-schema.md` | Prior completed-page inspection, selectors, field provenance and known discrepancies | Describes fields the full UI can expose; does not retroactively fill the reduced JSON |
| `/home/jake/Developer/study/vault/252/progress.csv` | Byte-identical to current reference CSV | Not an additional independent observation |
| `/home/jake/Developer/study/vault/252/progress-notes.md` | Explains catalog reconciliation and inferred course enrollment | Its text documents an earlier 212-task snapshot |
| `/home/jake/Developer/study/vault/252/knowledge_profile.csv` | 693 topic rows with explicit evidence labels | A locally assembled mixed-evidence snapshot, not a timestamped FIRe state export |
| `/home/jake/Developer/MA/DATA/Topics.csv` | 2,971 topic IDs/names; all 186 history topic/name pairs match exactly | Identity validation gives neither practice scope nor encompassing weight |
| `/home/jake/Developer/MA/DATA/Prerequisites.csv` and `Lesson-Data/Questions.csv` | Prerequisite and content question/KP identifiers | Prerequisites do not establish encompassing; retained answer occurrences have no question IDs to join to the content table |

The generated audit records SHA-256 hashes. The current progress hash is
`f78317d629e6b95d17a9f76718eae28b45c78069bb6ee11e10d2e8c114547b49`.
The XP metadata still describes **214 rows** and a different hash. All **34 task
joins nevertheless agree** on date, activity type, title, award, base and URL.
The three additional CSV rows have no new question observations. A snapshot hash
discrepancy is reported; the importer neither discards valid exact joins nor
pretends the original snapshot remained unchanged.

The CSV contains 133 lessons, 53 reviews, 13 assessments, 10 multisteps, six
diagnostics and two supplemental diagnostics. Course attributions are contextual
where inferred by the original reconciliation; they are not used to filter the
cross-course history replay. Task IDs remain strings, and sorted completion
timestamps provide chronology without inventing UTC instants. There are no
minute-resolution timestamp ties in this snapshot.

An additional local search covered filenames and HTML/JSON/JSONL/source-code
contents under `/home/jake/Developer/study` and `/home/jake/Developer/MA`, including
the MA capture pipeline, for sampled task IDs, task-result container IDs and
the `questionKP`/`timeElpased` selectors. No completed-task HTML/JSON export was
found in those searched trees. The pipeline's documented output is topic-content
capture, which cannot supply learner results by itself. This is a scoped search
finding, not a claim about every file on the computer or live browser state.

Four manually saved screenshots for supplemental task **9319474** were found in
`/home/jake/Desktop/MA-Manual-Caps/Supplementary Diagnostic` and inspected. They
preserve an introductory page and three question screens with outcomes Correct,
**Skipped Question**, Correct. Thus that specific missing-answer result has
additional explicit skipped-state evidence. The screenshots show no numeric
topic/KP links. Similar catalog prompts were rejected as identity joins: the
first screenshot transforms by translation then reflection, whereas catalog
question 45397 scales then reflects; the tetrahedron screenshot's three
statements differ from catalog tutorial step 35199. Neither a shared phrase nor
a topic family establishes an exact occurrence identity. No additional question
topic IDs enter the replay from these images.

## What outcomes and time are actually available

Of the 308 question results, **205 are correct and 103 incorrect**. Only **11
observed tasks, containing 70 questions**, have a known main task topic: five
lessons and six reviews across eight topics. The remaining 23 sampled tasks
contain 238 questions whose topic identities were not retained. They cannot be
assigned to topics by quiz title, course, question order, or content inventory.
Even for the 70 retained questions, the question-level topic link itself is
unknown: replay assigns the task topic under an explicit scope assumption.

Six sampled tasks have every answer correct; only two have a task topic ID:
lesson **13512234 / topic 893** and review **13124977 / topic 1042**. Correctness
and a passing FIRe event are not identical observed fields. All other task-level
pass/fail flags remain null, including the 183 tasks without retained questions.

The supplied history directly falsifies these shortcuts:

| Shortcut | Counterexamples |
| --- | ---: |
| Completed implies all questions correct | 28 of the 34 inspected tasks |
| Positive XP implies all questions correct | 24 inspected tasks |
| Earned/base XP is a bounded correctness proportion | 137 CSV rows exceed the base or have negative awards |

For example, zero-XP review **13409092** has outcomes
`correct, correct, incorrect, correct, incorrect`. Its XP must not erase the
three successful answers or establish a task-level failure rule. Full-base
review **13675888** includes an incorrect answer. These examples do not establish
that either review passed or failed Math Academy's internal threshold.

Displayed elapsed durations sum to **34,106 seconds**, of which 8,609 belong to
the 11 tasks with a main topic ID. This is not total study time: 183 task durations
are absent, pauses may be counted, and the reduced observations omit answer
timestamps. The importer preserves both local completion time and displayed
duration rather than subtracting question durations to invent start times.
Diagnostic **4748206** has the pre-existing feed/question-date discrepancy
documented in the schema report; its completion chronology is not clean timing
ground truth.

There are **57 successive same-topic completion pairs**. Their calendar gaps
are reproducible descriptive observations, but are not due intervals: the first
activity may not be a successful spaced repetition, implicit practice could
occur between them, and the later review could be delayed, remedial or chosen
by the learner. No assignment time or scheduler due time is supplied.

## The profile is useful context, not a validation target

The 693 unique profile topics have these explicit statuses:

| Status | Count | Interpretation |
| --- | ---: | --- |
| `inferred-mastered` | 376 | Evidence explicitly says prerequisite of a completed/checkmarked topic; local ancestry inference |
| `completed` | 64 | Activity history; nine also reference a queue checkmark |
| `unresolved` | 250 | No mastery evidence recorded |
| `checked-prerequisite` | 3 | Queue checkmark evidence |

All 64 completed timestamps match a history event, but nine topics have later
events in the current history. The latest profile completion is **2026-08-10
13:19**, preceding the newest history by more than six weeks. Seventy-nine
profile topics overlap the history: 64 completed, 14 unresolved and one
inferred-mastered. This mixture and timing prevent comparing final replay state
against profile labels as if they were contemporaneous independent observations.
No repetition count, current memory, calibrated interval, due date, or FIRe
state version is present. The 376 ancestry inferences are not imported as
encompassing edges or repetition credit.

## Saved graph colors provide conditional display constraints

An additional local artifact audit recovered **31 saved course graph HTML
files**, with **6,627 topic-node occurrences covering 2,590 unique topic IDs**.
Every one of the history's 129 topic IDs occurs in those graphs. The parser and
full per-course observations are in `engine/fire/graph_snapshots.py` and
`engine/fire/fixtures/graph-snapshot-observations.json`.

These files preserve `#graph` SVG node IDs, ellipse fill attributes and zero
stroke widths. Their seven-color palette matches the legacy public
`knowledge-graph.js` renderer inspected on 2026-09-26. Conditional on the same
renderer having produced the April captures, the recoverable display categories
are:

| Legacy `topic.repetition` display category | Node occurrences |
| --- | ---: |
| Numeric switch case 1 | 105 |
| Numeric switch case 2 | 36 |
| Numeric switch case 3 | 127 |
| Numeric switch case 4 | 66 |
| Numeric switch case 5 | 71 |
| Truthy default, not numeric 1–5 | 1,359 |
| Gray, no numeric repetition constraint | 4,863 |

**Dark blue does not prove six or more repetitions.** The JavaScript default
also accepts fractions, strings and other truthy values that fail its numeric
cases. Gray is not a verified zero state. The server's mapping from this display
field to FIRe's continuous `repNum` is missing, as is the exact April renderer
version. The newer `student-knowledge-graph.js` uses `topic.stability` and an HSL
formula instead; applying that newer inverse to these legacy palette values
would mix two renderers. The two downloaded scripts' hashes are recorded, with
the code evidence explained in `reference/fire-source-evidence.md`.

The ingestion log has **32 graph completion records on 2026-04-09 UTC**, from
02:06:37 through 18:53:36. Fourth Grade Math was captured twice; using each
current path's latest completion gives 31 records beginning at 02:09:49 UTC.
Mathematical Foundations II's logged operation spans 03:09:57–03:10:04 UTC and
Calculus I's 03:10:50–03:10:58 UTC. Both files were last changed in Git commit
`c4b819b01251c8efa941af0593a038ca9c0da273`, dated 2026-04-08 20:19:53 −07:00
(03:19:53 UTC); all 31 graph files match their current Git HEAD contents.
These are file and capture-log provenance, not authenticated state timestamps.
No learner ID is retained in the graph records or relevant log entries.

The capture script explicitly switches the active course, opens `/learn`,
clicks the course-percent graph control and saves `#graph.outerHTML`. Colors
conflict across course captures for **217 topic IDs**, including four history
topics: **347, 355, 361 and 459**. For example, topic 347 is numeric case 2 in
Algebra I and Integrated Math I, but uses dark default in their other captured
course contexts. The artifacts cannot distinguish course-specific display
context, state changes, rendering differences or capture effects. The audit
preserves every occurrence and does not merge these into one learner state.

There are 60 activity-history rows before April 8 (47 topic-bearing events on
36 topics), and 157 after April 9; none fall on April 8 or 9. All 36 earlier
topics occur in the graph snapshots. That gives temporal overlap without
requiring a time-zone assumption at the capture boundary, but no same-topic
before/after numeric state transitions. The saved graph colors therefore add
**conditional display observations, zero verified numeric FIRe states and zero
verified FIRe transitions**. They are not used to seed or grade the 32 replay
scenarios.

## Actual engine replay and sensitivity results

`run_history_scenarios` executes **32 scenarios** using the retained answers.
Each stores its full policy, graph fingerprint, per-event hash and update
receipt, final topic states, and model due values when a sampled review occurs.
The output also hashes the core, calibration and history implementation files.
These are executable reconstruction results, not claims about hidden MA state.

The dimensions are explicit:

- **Outcome unit:** 70 question-level events using observed booleans, or 11
  task events using the assumed rule “all questions correct.” These yield 53
  versus two successful events. Neither is asserted to be MA's FIRe event rule.
- **Clock:** calendar days from the first history completion, or a sensitivity
  control based on cumulative sampled elapsed hours. The second converts both
  event times and its assumed one-hour base interval to the core's day unit;
  it remains an incomplete clock, not recovered exercise time.
- **Initial repetitions:** zero or four for each of the eight retained topics,
  all assumed learned at time zero with memory 1 and prior accuracy 0.8.
- **Interval growth:** 2 or 1.5. Other core policy values are recorded in each
  scenario. No values are fitted to these observations.
- **Memory timestamp convention:** the operational decay-before-add policy or
  literal add-before-decay algebra. These produce different states even with
  identical observed answers and other assumptions.

Retained lesson/review answers update the practice accuracy channel. The
assessment channel keeps its assumed 0.8 prior because no retained assessment
question has a known topic ID; the engine averages the two channels. That prior
and the EWMA coefficients are explicit reconstruction policies, not recovered
learner calibration.

The encompassing graph has **zero edges** because no production weight has
been observed. This replay tests direct evidence processing, decay, policy
execution and auditability; graph propagation and compression must be checked
with separate known-graph fixtures. Every event has assumed quality 1. Unsampled
tasks and diagnostic state changes are omitted rather than assigned outcomes.

Calendar scenarios using decay-before-add mark **five of the six sampled
reviews as due** when observed; literal add-before-decay scenarios mark five or
six. These are compatibility counts, **not predictive accuracy**:
observed due/assignment times are absent and the omitted history can change
state. The partial-clock controls mark zero through six reviews due, showing
how much this quantity depends on assumptions.

For topic **604** (limits using conjugate multiplication), final repetitions
range from **0 to about 4.363** across the 32 scenarios. For topic **1042**
(Riemann sums in sigma notation), they range from about **0.648 to 4.269**.
Holding calendar time, zero initial repetitions and interval growth 2 fixed,
question-level versus all-correct task aggregation gives approximately **1.772
versus 0** for topic 604 under decay-before-add. Switching the question-level
scenario to literal add-before-decay gives approximately **2.792**. The sparse
history has no observed state with which to adjudicate these different answers.
These ranges are sensitivity results for selected assumptions, not confidence
intervals or bounds on Math Academy's actual state.

## Reproduction and useful next evidence

Run from the repository root:

```sh
python3 -m engine.fire.history \
  --profile /home/jake/Developer/study/vault/252/knowledge_profile.csv \
  --catalog /home/jake/Developer/MA/DATA/Topics.csv \
  --output engine/fire/fixtures/history-observations.json \
  --replay-output engine/fire/fixtures/history-replay-results.json
python3 -m unittest discover -s tests -p test_fire_history.py -v
python3 -m engine.fire.graph_snapshots \
  --ma-root /home/jake/Developer/MA \
  --output engine/fire/fixtures/graph-snapshot-observations.json
python3 -m unittest discover -s tests -p test_fire_graph_snapshots.py -v
```

The external profile and catalog flags are optional; without them the audit and
replay remain reproducible from the two tracked reference inputs, with those
optional validations omitted. Source originals are read only. Tests cover
duplicate IDs, contradictory joins, unknown-state preservation, XP/outcome
separation, explicit scenario selection and real replay without invented edges.

The highest-value additional capture is complete per-question topic/KP links
and result labels for naturally occurring tasks, accompanied by task start/end
and assignment/due information where actually exposed. Repeated timestamped
knowledge-state or review-queue snapshots, diagnostic reset/merge information,
and sourced encompassing weights would allow specific recurrence or scheduling
predictions to become falsifiable. More XP rows alone cannot identify these
missing inputs.
