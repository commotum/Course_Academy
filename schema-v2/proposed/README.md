# Proposed activity schemas

These drafts extend the existing content model with review, assessment, multistep, and diagnostic definitions, plus the records needed to capture a learner's actual work. The common attempt record is [data/6-3-learner-activity.edn](../data/6-3-learner-activity.edn), and its individual presentations use [content/4-task.edn](../content/4-task.edn). The existing [lesson schema](../content/2-1-lesson.edn) already supplies the sixth content definition; it is not duplicated here.

The design follows EDB's [one-direction relationships, enum identities, unique domain IDs, and history guidance](/home/jake/Developer/EDB/docs/02_core_concepts/05_best_practices.md). These are proposed local models, not recovered Math Academy table definitions. No content migration or live account changes were performed.

## Reading order

| File | Meaning |
| --- | --- |
| [review.edn](review.edn) | A topic to review, optionally targeting particular KPs. The engine selects questions from the existing banks. |
| [assessment.edn](assessment.edn) | A named assessment scope with optional configured time limit and expected workload. |
| [multistep.edn](multistep.edn) | Shared scenario, target topics, and ordered question placements. |
| [multistep-step.edn](multistep-step.edn) | One question's place in that dependent sequence. |
| [diagnostic.edn](diagnostic.edn) | A placement exam for a course and its foundations. |
| [supplemental-diagnostic.edn](supplemental-diagnostic.edn) | A distinct diagnostic definition addressing gaps in placement evidence after graph/curriculum changes. |
| [activity-group.edn](activity-group.edn) | Optional lesson KP grouping within an activity. |
| [content/4-task.edn](../content/4-task.edn) | One presentation of a question, tutorial, or example, with its own order and measurements. |
| [submission.edn](submission.edn) | One recorded response submission for a question presentation. |
| [submitted-answer.edn](submitted-answer.edn) | A response to one canonical answer field, using a stable selected-answer ref or entered value. |

File order is a reading aid. Install all schema definitions, including the existing data/content files, before creating domain records. `examples/` contains data, not schema.

## The two main levels

```text
learner/activity                         ordinary history membership
  └─ activity                           one attempted lesson/review/quiz/etc.
       ├─ content ───────────────────→ reusable activity definition
       ├─ groups                       owned optional KP groups
       └─ tasks                        owned ordered presentations
            ├─ content ─────────────→ reusable question/tutorial/example
            ├─ group ───────────────→ group within the same activity
            └─ submissions             owned recorded tries
                 └─ fields             owned submitted values
                      ├─ field ──────→ canonical answer-field
                      └─ selected-answer → canonical answer, when applicable
```

Activity and task are the main measurement levels. Here, a task is one learner-specific presentation of a question, tutorial, or example; placing its schema in `content` does not make it a shared definition. Math Academy’s historical `taskId` identifies the whole activity and remains `activity/math-academy-id`. Submission and submitted-answer add detail only when actual responses are available or the application needs to record retries and multiple blanks. They do not create another activity or change the canonical answer key.

The application derives an activity's category from the identity attribute on its `activity/content` target: `lesson/id`, `review/id`, `assessment/id`, `multistep/id`, `diagnostic/id`, or `supplemental-diagnostic/id`. It can expose that derived category in application state for display and routing without storing a duplicate `activity/type`. A known category with an unrecovered definition can use an identity-only content placeholder. A summary with no known content category can omit the ref and remains unclassified.

Every activity has one learner through `learner/activity`; use reverse lookup rather than storing `activity/learner`. Ordinary history membership currently preserves activity entities rather than cascading learner deletion. The writer must preserve the owner association while history is retained. Each activity owns its groups and tasks; each task owns its submissions. Shared curricular content, canonical answer fields, and selected answer choices are ordinary refs. Deleting activity details must not delete those shared entities.

The activity does not duplicate its content's intended topic scope or course. Task topic refs preserve the specific observed evidence, including cases where the full content definition is unavailable. A course that motivated a recommendation is scheduling context, not something uniquely implied by shared content.

A question occurrence has its own UUID. Reusing question 37713 in another activity or presentation does not overwrite its earlier result. The question still belongs to its established KP bank; using it in an assessment does not create another bank membership.

## Current learner queue

[learner-queue.edn](../data/6-4-learner-queue.edn) defines entries owned through `learner/queue`. Each entry requires an ID, content ref, index, selection source (`recommended` or `self-selected`), and a human-readable reason. Course context and addition time are optional. Sort the unordered reference collection by `queue/index`; keep indexes positive and distinct within a learner's queue.

The queue is current up-next state. Launching or dismissing an entry removes it from that queue; activity history remains separate. The current activity schema has no selection attribute or queue-entry reference, so a completed activity does not preserve why it was selected. A permanent scheduling-decision history would need its own retained record later. These schemas do not implement the scheduler, launch transitions, or queue relationship checks.

## Evidence used

The current [progress.csv](../../reference/progress.csv) has **217 rows**, all marked Completed, with unique task IDs in this snapshot:

| Type | Rows | Main topic IDs in CSV | Displayed XP baseline |
| --- | ---: | --- | --- |
| Lesson | 133 | Present | Present |
| Review | 53 | Present | Present |
| Assessment | 13 | Absent | Present |
| Multistep | 10 | Absent | Present |
| Diagnostic | 6 | Absent | Absent |
| Supplemental Diagnostic | 2 | Absent | Absent |

Some earlier reports describe a 214-row snapshot. The read-only [XP analysis script](../../reference/analyze-mathacademy-xp.py), rerun against the current file, reports 217 CSV rows and 34 reduced task observations containing 308 questions. All 34 observed IDs occur in the CSV. Its candidate assessment formula fits 12 observed assessments; its multistep formula fits six observations. The formulas are hypotheses and are not schema constraints.

The additional [saved live capture](../../reference/fire-live-observations-2026-09-26.json) includes the exact requested task, **13682227**, with **eight correct question occurrences** and **18/15 XP**. No new live browsing was necessary. The user's supplied prompt provides the expression for question 37713; the saved capture supplies its question/topic/example IDs, E label, 1:43 elapsed time, and displayed time.

Primary local sources reviewed:

- [Activity schema and HTML interpretation](../../reference/mathacademy-activity-schema.md): nesting, timing, answers, and missing-data distinctions.
- [XP analysis](../../reference/mathacademy-xp-analysis.md) and [analysis code](../../reference/analyze-mathacademy-xp.py): signed XP, baseline/bonus distinctions, adaptive sequences, and limits of inferred formulas.
- [Engine analysis](../../reference/mathacademy_engine_analysis.md): six families, placement, remediation, scheduling, and separation of task completion from knowledge state.
- [Architecture analysis](../../reference/mathacademy_schema_architecture.md): definitions versus attempts, question occurrences versus submissions, and corrected source identity mappings.
- [Progress attribution notes](../../reference/progress-notes.md): inferred course contexts and timestamp ambiguities.

The older activity-schema table calls a topic-link fragment a KP ID. The later source audit establishes that these fragments identify **example content**. The drafts preserve that through `task/example`; `knowledge-point` is populated only after a verified local mapping. `#4962` is neither lesson-step ID nor automatically our KP ID.

## Mapping the requested example

[examples/quiz-4-retake.edn](examples/quiz-4-retake.edn) is executable example data for the saved eight-question task.

| Observed value | Stored as |
| --- | --- |
| `taskId=13682227` | `activity/math-academy-id` |
| Assessment | `activity/content` points to a placeholder with `assessment/id`; derive the category from that target |
| Quiz 4 (Retake) | `activity/title` and `activity/retake true` |
| Completed | `activity/status :activity.status/completed` |
| 18/15 XP | `activity/xp-earned 18`, `activity/xp-base 15` |
| CSV `2026-09-24 17:05` | `activity/completed-local`; no invented UTC instant |
| `question-37713` | Reference to a question with `question/math-academy-id 37713` |
| `/topics/660#4962` | References to topic 660 and example 4962 |
| E | `task/difficulty :question.difficulty/easy` |
| Elapsed: 1:43 | `task/elapsed-seconds 103.0` |
| Correct | `task/result :task.result/correct` |
| Thu, Sep 24th @ 5:05 PM | `task/source-time`, without inventing a submission instant |

The example creates local identity placeholders for incompletely captured content, including an assessment placeholder scoped to this captured task. Its UUID is a local illustrative identity, not a recovered assessment ID or proof of which other attempts share its definition. It does not claim the assessment scope, question formats, choices, grading keys, KP identities, or instructional definitions are recovered. These placeholders cannot be served until the corresponding complete content specs are satisfied. The example also omits an overall pass/fail outcome: eight correct results and a completed header are observations, not an exposed controller decision.

## Timing and XP

- **Elapsed seconds:** measured wall-clock time, potentially including pauses. Activity elapsed time covers the whole attempt; task elapsed time covers a presentation. The sum of displayed question times is a separate derived quantity and does not establish total activity duration.
- **Active seconds:** explicitly measured engagement excluding tracked pauses. It cannot be reconstructed from the historical elapsed labels.
- **Expected seconds:** workload estimate used by scheduling, question selection, or calibration. E/M/H labels and earned XP do not reveal expected solve times.
- **Time limit:** the configured maximum for that attempt, separate from expected or actual time. None is assumed universally, including 900 seconds for every quiz.
- **Instants:** use `started-at`, `completed-at`, and `submitted-at` only when their meaning, date, and timezone are supported. Quiz question time labels often all equal the task completion time. Some diagnostic labels conflict with the feed date. Keep the source local/string evidence instead of assigning a guessed instant.
- **XP earned:** signed task-level award. A lesson can earn -1; 18/15 is valid. The denominator is base XP, not maximum possible XP. Missing diagnostic baselines remain absent. No per-question XP is invented.

Question count, correct count, accuracy, XP totals, and current streaks can be calculated from the recorded data. `activity/results-complete` distinguishes a complete question-result set from a partial capture; compute whole-activity accuracy only when completeness and all outcomes are established. Completed status alone does not establish that the imported results are complete. Avoid independently mutable duplicates. Adaptive stopping, failure caps, bonuses, and retake eligibility belong to application code. A three-question review does not establish that five questions were planned or that all three were correct; the observed `mEE` review is a counterexample to that simple inference.

## Responses and instruction

For a selection, record a stable `selected-answer` reference instead of a displayed letter. For a blank, record the actual entered value and its canonical `answer-field`. Several fields can receive one overall question grade; per-field grades remain absent unless explicitly available.

A final result can be Correct while the submitted response is unavailable in the capture. Literal No answer is distinct from unavailable and does not explain whether time expired or the learner intentionally skipped. The inline result-page blank can show a correct answer rather than what the learner submitted; use the actual student-answer region or runtime submission data.

When a displayed response such as `-4, 2` cannot reliably be mapped to fields, store it in `submission/response`. Do not invent two individually graded field records. Record multiple submissions only when observed by the application or source; the first recovered record does not establish the total number of previous attempts.

Lesson results can preserve KP group order and titles without a recovered KP identity. Question indexes remain activity-wide. Tutorial/example task types allow our application to measure instructional work as well; those presentation logs are a local extension, not something the completed CSV supplies.

## Engine use and validation boundary

The controller uses the definition's scope to select content. Self-selected and recommended queue entries lead to the same activity/task record structure and completion rules. It records graded work, updates activity XP once, and sends appropriately grouped evidence to learner progress. An assessment spanning several topics can create several topic-level updates; a question occurrence must not automatically award a full repetition. Diagnostic placement has its own inference semantics and is not merely another review.

Core `activity/validate` accepts historical summaries with missing details, including an absent content ref. `activity/ready-validate` additionally requires a content ref, but a ref alone does not establish that its target is ready to serve. Before local delivery, the controller must require exactly one supported content category on that target and validate the complete definition. Task specs similarly distinguish a recoverable observation from a presentation with resolved content. Full question/example/tutorial validation still happens before serving content.

These drafts use native **required-attribute specs**, with no dangling predicate names. Those specs do not enforce all the proposed domain rules. Queue ownership, valid content targets, allowed selection enums, and distinct positive indexes also need controller or predicate checks. The controller or future registered predicates must check enum membership; exact ownership; sibling indexes; correct target types; same-activity groups; retake/remediation ownership and cycles; nonnegative/finite timings; supported timestamp order; complete source reconciliation; exactly one entered/selected value; and that a selected answer belongs to the target field. A response needs text or field values. External task IDs must be reconciled within the learner history. Persist observations, awarded XP, and resulting engine changes atomically and idempotently.

No five-question review cap, universal timer, pass threshold, fixed XP formula, or inferred student mastery is embedded as a schema constraint. Native type/cardinality/required-field and component-lifecycle behavior is tested in [edb_activity_checks.rs](../../tests/edb_activity_checks.rs), invoked by the existing [schema harness](../../tests/validate_fire_schema.rs). The harness installs `proposed` explicitly and checks the real retake fixture, refs to all six content categories, signed/above-base XP, unknown durations, repeated question presentations and submissions, and deletion of activity details without deleting shared question content. It does not claim the runtime category resolver, future domain predicates, or activity controller are implemented.
