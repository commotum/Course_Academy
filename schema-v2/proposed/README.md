# Pending content schemas

These two drafts still need review and finalization. Keep them here until Jake explicitly requests moving them into another schema folder.

| File | Remaining model |
| --- | --- |
| [multistep.edn](multistep.edn) | A shared scenario with an ordered sequence of questions. |
| [multistep-step.edn](multistep-step.edn) | One authored question placement in that sequence. |

[Lessons](../content/1-1-lesson.edn), [reviews](../content/3-review.edn), [assessments](../content/4-assessment.edn), and [diagnostics](../content/5-1-diagnostic.edn) with their [probes](../content/5-2-diagnostic-probe.edn) already have content schemas. Learner attempts and results use [learner-task](../learner/2-1-learner-task.edn) and [task-item](../learner/2-2-learner-task-item.edn). Entered answers use [learner-response](../learner/2-4-learner-response.edn); selections reference existing answer entities directly through `task-item/responses`.

The retained drafts describe content and scope. Question selection, stopping rules, grading, XP, and scheduling belong in application code. Their exact boundaries and required attributes remain to be finalized.
