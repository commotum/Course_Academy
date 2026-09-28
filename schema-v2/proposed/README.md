# Pending content schemas

These five drafts still need review and finalization. Keep them here until Jake explicitly requests moving them into another schema folder.

| File | Remaining model |
| --- | --- |
| [assessment.edn](assessment.edn) | A named assessment scope with optional timing settings. |
| [multistep.edn](multistep.edn) | A shared scenario with an ordered sequence of questions. |
| [multistep-step.edn](multistep-step.edn) | One authored question placement in that sequence. |
| [diagnostic.edn](diagnostic.edn) | A placement exam covering a course and its foundations. |
| [supplemental-diagnostic.edn](supplemental-diagnostic.edn) | Targeted diagnostic work to fill gaps in placement evidence. |

[Lessons](../content/1-1-lesson.edn) and [reviews](../content/3-review.edn) already have content schemas. Learner attempts and results use [learner-task](../learner/2-1-learner-task.edn) and [task-item](../learner/2-2-learner-task-item.edn). Entered answers use [learner-response](../learner/2-4-learner-response.edn); selections reference existing answer entities directly through `task-item/responses`.

The retained drafts describe content and scope. Question selection, stopping rules, grading, XP, and scheduling belong in application code. Their exact boundaries and required attributes remain to be finalized.
