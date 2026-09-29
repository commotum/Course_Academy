# Schema organization

`data` holds curriculum entities, course maps and outcomes, and skill relationships. `content` holds reusable activity definitions, instructional material, problems, and answer representations. `learner` holds learner identity, current state, the queue, task history, and item performance. `engine` holds FIRe policy settings. There are 30 current EDN schemas.

Each folder has its own numbering, starting at 1. Single-file groups use `group-name`; groups with multiple files use `group-item-name`. Within a folder, the first number groups related schemas and the second gives their reading order. Numbers do not connect groups across folders; EDB references define the relationships. This is a navigation aid rather than a required transaction order. Install all schema definitions before creating application data.

```text
data/
  1-1-course.edn
  1-2-course-map.edn
  1-3-course-map-entry.edn
  1-4-course-outcome.edn
  2-unit.edn
  3-module.edn
  4-1-topic.edn
  4-2-encompassing.edn
  5-knowledge-point.edn

content/
  1-1-lesson.edn
  1-2-lesson-step.edn
  1-3-tutorial.edn
  1-4-example.edn
  2-1-question.edn
  2-2-answer-field.edn
  2-3-answer.edn
  3-review.edn
  4-assessment.edn
  5-1-diagnostic.edn
  5-2-diagnostic-probe.edn
  6-1-multistep.edn
  6-2-multistep-step.edn

learner/
  1-1-learner.edn
  1-2-learner-performance.edn
  1-3-learner-progress.edn
  1-4-learner-queue.edn
  2-1-learner-task.edn
  2-2-learner-task-item.edn
  2-4-learner-response.edn

engine/
  1-fire-policy.edn
```

Course maps, their entries, and course outcomes sit beside the course schema in `data`. Membership stays on courses, units, and modules; the map supplies ordering. Topics and knowledge points define skills, while lessons, tutorials, examples, and questions provide teaching material. Encompassing records describe weighted topic relationships.

A **learner task** is one learner's attempt at a lesson, review, assessment, multistep activity, or diagnostic. Initial and supplemental diagnosis use the same diagnostic schema. [2-1-learner-task.edn](learner/2-1-learner-task.edn) records its status, outcome, XP, and timing using `learner-task/*` attributes. Its `learner-task/activity` ref points to the shared activity definition, which contains no learner results. `learner/activity` is the learner's activity history: a collection of learner-task records, not shared activity definitions.

A task owns its presentation records through `learner-task/items`, defined in [2-2-learner-task-item.edn](learner/2-2-learner-task-item.edn). Each item records its own timing, result, and responses and references shared instructional content. Responses point directly to selected answer entities or to [learner-response](learner/2-4-learner-response.edn) records for entered values. The application derives both the activity category and item content kind from their targets; neither needs a duplicate type attribute.

`lesson-step` remains authored lesson structure: an ordered tutorial or knowledge-point placement. A [multistep](content/6-1-multistep.edn) owns [multistep-step](content/6-2-multistep-step.edn) question placements within a scenario. Both use step indexes for authored order. Task items record actual presentations during a learner's attempt.

[Diagnostics](content/5-1-diagnostic.edn) own [probes](content/5-2-diagnostic-probe.edn) and reference a starting probe. Each probe references a question and optional next probes for correct, incorrect, skipped, or accepted silly-mistake retry outcomes. Probe topics and assessment topic coverage are derived through question-bank and knowledge-point membership. Missing ordinary branches end that path; a missing retry branch means no retry is offered. Application code offers one available alternate after a submitted incorrect answer, without a timing gate. Actual presentations remain learner task items.

The learner's `learner/knowledge-profile` owns current `progress` records, one per topic. The reverse reference `learner/_knowledge-profile` identifies a record's learner. `learner/queue` owns up-next entries defined in [1-4-learner-queue.edn](learner/1-4-learner-queue.edn); each records an activity ref, order, selection mode (`required`, `recommended`, or `self-selected`), and reason, with optional course context and addition time. All three learner collections are optional and unordered in EDB; queue order comes from `queue/index`. Optional entries can be dismissed; required work remains an obligation until the application policy's completion condition is met. Launching a task does not itself satisfy that requirement: the controller must carry or recompute it, requeuing when needed. Task history is retained separately; the queue is not a permanent scheduling-decision log. See [progress validation](../engine/edb/README.md) for the Rust predicates and write requirements.

`learner/performance` optionally owns one global accuracy summary, defined in [1-2-learner-performance.edn](learner/1-2-learner-performance.edn). Its four `performance/*` attributes hold assessment/practice accuracy and evidence mass across topics; per-topic estimates remain on `progress`. The summary is found through the learner ref and needs no separate domain ID. Ensure `performance/validate` on the child when writing its values; `learner/validate` remains the minimal learner spec. Single ownership and numeric ranges remain application contracts.

[Task items](learner/2-2-learner-task-item.edn) hold responses, results, elapsed time, optional `task-item/completed-at`, and optional `task-item/performance`. Completion time identifies when practice occurred, separately from its duration and engine processing time. Whole-task outcome and XP remain on the task. The Python [completion handler](../engine/runtime.py) converts this evidence into separate accuracy and retention updates; the [schema adapter](../engine/schema.py) prepares their atomic EDB write.

Courses, units, modules, topics, and knowledge points have an `identity-validate` spec for ID-only placeholders and an existing `validate` spec for their required data. This supports loading one hierarchical level at a time, then filling in and linking the records through their stable IDs. Full validation checks each entity's own required attributes; referenced content must also be validated before it is served for study.

These five placeholder specs cover the current curriculum-loading workflow. We can add the same option to lessons, questions, examples, or tutorials when staged content generation needs it.

`data/4-1-topic.edn` includes optional `topic/difficulty`, a finite assessment-accuracy estimate in [0,1]. Ensure `topic/difficulty-validate` on difficulty-only updates. `topic/validate` also checks difficulty if present, while identity-only placeholders remain supported.

[1-fire-policy.edn](engine/1-fire-policy.edn) defines FIRe parameters under a stable `policy/id`. Ensure `policy/validate` when editing them. EDB history preserves earlier values: inspect past progress and its referenced policy in the same historical database value with `as_of`. Editing a policy leaves stored `progress/interval-days` unchanged until the engine recomputes it; it does not automatically reschedule every topic.

The completion handler prepares one transaction containing the item result, responses, affected progress, overall performance, and any task completion/XP. EDB transaction history records these changes without a separate engine-update entity. Submission must use the returned exact-basis guard and request key; retain the original plan for retries. The Python adapter exists; wiring its callbacks to a production UI and durable EDB writer remains application work. See [native validation and engine mapping](../engine/edb/README.md).

## Activity models

Lesson, review, assessment, diagnostic, and multistep schemas live in `content`. Intended topic scope comes from the referenced activity; question ownership supplies the topic for observed answers. Selection mode and motivating course belong to queue entries. The completion handler implements activity progression and engine-boundary checks. Required-attribute specs remain opt-in; the adapter is not a general validator for every curriculum-editing operation or a complete queue scheduler.

## Remaining work

`knowledge-point/question-generator` still needs its representation and generator interface finalized; a repository-relative Python file path is the current recommendation. The [scheduling](../reference/scheduling-proposal.md), [XP](../reference/xp-proposal.md), and [answer-grading](../reference/answer-grading-proposal.md) proposals give concrete application rules for review. A completed diagnostic retry replaces the original answer for frontier placement; both presentations remain in history and submitted-answer accuracy.

`learner/course` records the course selected in the UI. Broader concurrent study scope is deferred; initial population will include a Custom/Self-Directed course alongside the Math Academy courses. Queue scheduling and the production UI/EDB connection remain implementation work. Preventing repeat questions uses the existing learner activity history; serving must atomically select and reserve an unseen question before displaying it. Cross-task no-repeat enforcement is not yet implemented and needs no duplicate `question/seen-by` attribute.
