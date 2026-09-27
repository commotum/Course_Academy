# Schema organization

`data` holds curriculum entities, skill relationships, and learner records. `content` holds course maps, instructional material, problems, and answer representations. `fire` holds typed engine policy settings and the remaining performance/application prototypes.

Each folder has its own numbering, starting at 1. Single-file groups use `group-name`; groups with multiple files use `group-item-name`. Within a folder, the first number groups related schemas and the second gives their reading order. Numbers do not connect groups across folders; EDB references define the relationships. This is a navigation aid rather than a required transaction order. Install all schema definitions before creating application data.

```text
data/
  1-course.edn
  2-unit.edn
  3-module.edn
  4-1-topic.edn
  4-2-encompassing.edn
  4-3-topic-difficulty.edn
  5-knowledge-point.edn
  6-1-learner.edn
  6-2-learner-progress.edn
  6-3-learner-activity.edn

content/
  1-1-course-map.edn
  1-2-course-map-entry.edn
  1-3-course-outcome.edn
  2-1-lesson.edn
  2-2-lesson-step.edn
  2-3-tutorial.edn
  2-4-example.edn
  3-1-question.edn
  3-2-answer-field.edn
  3-3-answer.edn

fire/
  1-policy.edn
  06-performance.edn
  07-application.edn
```

Course maps and entries belong in `content` as authored arrangements of the curriculum. Membership stays on courses, units, and modules in `data`. Course outcomes are authored explanatory content. Topics and knowledge points define skills, while their lessons, tutorials, examples, and questions provide the teaching material. Encompassing records describe weighted topic relationships. The learner schema belongs in `data` and uses the `learner/*` namespace for identity, global accuracy, knowledge profile, and activity history.

The learner's `learner/knowledge-profile` owns current `progress` records, one per topic. The reverse reference `learner/_knowledge-profile` identifies a record's learner. `learner/activity` references activity history; its shared attempt record is defined in `6-3-learner-activity.edn`. Activity definitions and child-record drafts are in [proposed](proposed/README.md). Both collections are optional and unordered. See [progress validation](../engine/edb/README.md) for the Rust predicates and write requirements.

Courses, units, modules, topics, and knowledge points have an `identity-validate` spec for ID-only placeholders and an existing `validate` spec for their required data. This supports loading one hierarchical level at a time, then filling in and linking the records through their stable IDs. Full validation checks each entity's own required attributes; referenced content must also be validated before it is served for study.

These five placeholder specs cover the current curriculum-loading workflow. We can add the same option to lessons, questions, examples, or tutorials when staged content generation needs it.

`4-3-topic-difficulty.edn` defines additional attributes on the existing topic, not a child entity. Unknown difficulty can be omitted. Explicit estimates require a method; assessment-derived values additionally require integer counts and a cohort. Ensure `topic/difficulty-validate` on evidence writes. `topic/validate` also checks difficulty if present, while identity-only placeholders remain supported.

`fire/1-policy.edn` defines complete named configurations with UUID identity, typed settings, and ref-based enums. Ensure `policy/validate`; create a new policy identity when changing a configuration already in use. Policy immutability is a writer contract. Applications record `fire-application/basis-t` instead of a calibration-set reference to identify the database value used to read topic difficulty and other inputs. Keep history for those inputs. See [native validation and engine mapping](../engine/edb/README.md).

## Proposed activity models

[proposed/README.md](proposed/README.md) explains the six activity families, shared attempt history, ordered content occurrences, submitted answers, and source-to-schema mappings. The reusable lesson already lives in `content`; new review, assessment, multistep, and diagnostic definitions remain under `proposed` for review. `data/6-3-learner-activity.edn` now contains the common record type. Draft required-attribute specs are executable, while their documented controller/domain checks remain to be implemented. The example retake data is separate from the schema and does not constitute a migration.
