# Schema organization

`data` holds curriculum entities, skill relationships, and learner records. `content` holds course maps, instructional material, problems, and answer representations. The remaining `fire` files are prototype definitions awaiting review; their names and contents have been left intact.

Each folder has its own numbering, starting at 1. Single-file groups use `group-name`; groups with multiple files use `group-item-name`. Within a folder, the first number groups related schemas and the second gives their reading order. Numbers do not connect groups across folders; EDB references define the relationships. This is a navigation aid rather than a required transaction order. Install all schema definitions before creating application data.

```text
data/
  1-course.edn
  2-unit.edn
  3-module.edn
  4-1-topic.edn
  4-2-encompassing.edn
  5-knowledge-point.edn
  6-1-learner.edn
  6-2-progress.edn

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
```

Course maps and entries belong in `content` as authored arrangements of the curriculum. Membership stays on courses, units, and modules in `data`. Course outcomes are authored explanatory content. Topics and knowledge points define skills, while their lessons, tutorials, examples, and questions provide the teaching material. Encompassing records describe weighted topic relationships. The learner schema belongs in `data`; its existing `fire-learner` attribute names are unchanged.

The learner's `learner/knowledge-profile` owns current `progress` records, one per topic. The reverse reference `learner/_knowledge-profile` identifies a record's learner. `learner/activity` references activity history; the activity schema remains to be defined. Both collections are optional and unordered. See [progress validation](../engine/edb/README.md) for the Rust predicates and write requirements.

Courses, units, modules, topics, and knowledge points have an `identity-validate` spec for ID-only placeholders and an existing `validate` spec for their required data. This supports loading one hierarchical level at a time, then filling in and linking the records through their stable IDs. Full validation checks each entity's own required attributes; referenced content must also be validated before it is served for study.

These five placeholder specs cover the current curriculum-loading workflow. We can add the same option to lessons, questions, examples, or tutorials when staged content generation needs it.
