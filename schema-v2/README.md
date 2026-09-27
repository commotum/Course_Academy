# Schema organization

`data` holds curriculum entities, course maps and outcomes, and skill relationships. `content` holds reusable lesson definitions, instructional material, problems, and answer representations. `learner` holds learner identity, current state, the queue, task history, and topic-specific task performance. `fire` holds engine policy settings and application receipts; `proposed` holds draft schemas awaiting review, including activity definitions, task groups, and responses.

Keep proposed schemas in `proposed` until Jake has personally reviewed them and explicitly requests their move. A schema's subject does not authorize moving it into `data`, `content`, or `learner`.

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
  4-3-topic-difficulty.edn
  5-knowledge-point.edn

content/
  1-1-lesson.edn
  1-2-lesson-step.edn
  1-3-tutorial.edn
  1-4-example.edn
  2-1-question.edn
  2-2-answer-field.edn
  2-3-answer.edn

learner/
  1-1-learner.edn
  1-2-learner-performance.edn
  1-3-learner-progress.edn
  1-4-learner-queue.edn
  2-1-learner-task.edn
  2-2-learner-task-item.edn
  2-3-learner-task-performance.edn

fire/
  1-policy.edn
  07-application.edn

proposed/
  review.edn
  assessment.edn
  multistep.edn
  multistep-step.edn
  diagnostic.edn
  supplemental-diagnostic.edn
  task-group.edn
  submission.edn
  submitted-answer.edn
```

Course maps, their entries, and course outcomes sit beside the course schema in `data`. Membership stays on courses, units, and modules; the map supplies ordering. Topics and knowledge points define skills, while lessons, tutorials, examples, and questions provide teaching material. Encompassing records describe weighted topic relationships.

A **learner task** is one learner's attempt at a lesson, review, assessment, multistep activity, diagnostic, or supplemental diagnostic. [2-1-learner-task.edn](learner/2-1-learner-task.edn) records its status, outcome, XP, and timing using `learner-task/*` attributes. Its `learner-task/activity` ref points to the shared activity definition, which contains no learner results. `learner/activity` is the learner's activity history: a collection of learner-task records, not shared activity definitions.

A task owns its presented questions, tutorials, and examples through `learner-task/items`, defined in [2-2-learner-task-item.edn](learner/2-2-learner-task-item.edn). Each item records its own timing, result, and submissions and references shared instructional content. The application derives both the activity category and item content kind from their targets; neither needs a duplicate type attribute.

`lesson-step` remains authored lesson structure: an ordered tutorial or knowledge-point placement. `multistep-step` remains an authored question placement. A task item can point to either through optional `task-item/source-step`; it records what happened during an attempt without changing the authored sequence. Draft shared activity definitions, task groups, submissions, and submitted answers remain in [proposed](proposed/README.md) pending personal review and an explicit move request.

The learner's `learner/knowledge-profile` owns current `progress` records, one per topic. The reverse reference `learner/_knowledge-profile` identifies a record's learner. `learner/queue` owns up-next entries defined in [1-4-learner-queue.edn](learner/1-4-learner-queue.edn); each records an activity ref, order, selection mode (`required`, `recommended`, or `self-selected`), and reason, with optional course context and addition time. All three learner collections are optional and unordered in EDB; queue order comes from `queue/index`. Optional entries can be dismissed; required work remains an obligation until the application policy's completion condition is met. Launching a task does not itself satisfy that requirement: the controller must carry or recompute it, requeuing when needed. Task history is retained separately; the queue is not a permanent scheduling-decision log. See [progress validation](../engine/edb/README.md) for the Rust predicates and write requirements.

`learner/performance` optionally owns one global accuracy summary, defined in [1-2-learner-performance.edn](learner/1-2-learner-performance.edn). Its four `performance/*` attributes hold assessment/practice accuracy and evidence mass across topics; per-topic estimates remain on `progress`. The summary is found through the learner ref and needs no separate domain ID. Ensure `performance/validate` on the child when writing its values; `learner/validate` remains the minimal learner spec. Single ownership and numeric ranges remain application contracts.

[Learner task performance](learner/2-3-learner-task-performance.edn) holds one graded topic result prepared for FIRe. Several answers can support one result, and a task covering several topics can produce several results. This is distinct from the overall learner performance summary and from the application receipt recording resulting progress changes. The file retains the `fire-event/*` namespace and existing engine `Event` contract, including learner-scoped event identity. This reorganization does not add a task ownership ref or change the engine behavior.

Courses, units, modules, topics, and knowledge points have an `identity-validate` spec for ID-only placeholders and an existing `validate` spec for their required data. This supports loading one hierarchical level at a time, then filling in and linking the records through their stable IDs. Full validation checks each entity's own required attributes; referenced content must also be validated before it is served for study.

These five placeholder specs cover the current curriculum-loading workflow. We can add the same option to lessons, questions, examples, or tutorials when staged content generation needs it.

`4-3-topic-difficulty.edn` defines additional attributes on the existing topic, not a child entity. Unknown difficulty can be omitted. Explicit estimates require a method; assessment-derived values additionally require integer counts and a cohort. Ensure `topic/difficulty-validate` on evidence writes. `topic/validate` also checks difficulty if present, while identity-only placeholders remain supported.

`fire/1-policy.edn` defines complete named configurations with UUID identity, typed settings, and ref-based enums. Ensure `policy/validate`; create a new policy identity when changing a configuration already in use. Policy immutability is a writer contract. Applications record `fire-application/basis-t` instead of a calibration-set reference to identify the database value used to read topic difficulty and other inputs. Keep history for those inputs. See [native validation and engine mapping](../engine/edb/README.md).

## Proposed activity models

[proposed/README.md](proposed/README.md) explains the six activity families, task history, ordered task items, submitted answers, and source-to-schema mappings. The reusable lesson already lives in `content`; new review, assessment, multistep, and diagnostic definitions remain under `proposed` for review. Intended topic scope comes from the referenced activity; observed topic evidence is recorded on task items. Selection mode and motivating course belong to queue entries. Draft required-attribute specs are executable, while their documented controller/domain checks remain to be implemented. The example retake data is separate from the schema and does not constitute a migration.
