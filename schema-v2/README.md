# Schema organization

`data` holds curriculum entities, course groups and outcomes, and skill relationships. `content` holds reusable activity definitions, instructional material, problems, and answer representations. `learner` holds learner identity, current state, task history, and item performance. `engine` holds FIRe policy settings and fixed earned-XP rule documentation. Generic activities and steps replace the type-specific content schemas; the runtime still needs migration to that shared model.

Each folder has its own numbering; content starts at 0 for the generic activity definition. Single-file groups use `group-name`; groups with multiple files use `group-item-name`. Within a folder, the first number groups related schemas and the second gives their reading order. Numbers do not connect groups across folders; EDB references define the relationships. This is a navigation aid rather than a required transaction order. Install schema definitions before seed transaction data.

```text
data/
  1-course-group.edn
  1-2-course-groups.edn       # seed transaction data
  2-1-course.edn
  2-2-course-outcome.edn
  2-3-courses.edn         # Math Academy course seed data
  3-unit.edn
  3-2-units.edn          # seed data
  3-3-course-units.edn   # membership links
  4-module.edn
  4-2-modules.edn        # seed data
  4-3-unit-modules.edn   # membership links
  5-1-topic.edn
  5-2-encompassing.edn
  5-3-topics.edn         # seed data
  5-4-module-topics.edn  # membership links
  5-5-prerequisites.edn  # topic graph links
  6-knowledge-point.edn

content/
  0-activity.edn
  1-step.edn
  2-tutorial.edn
  4-question.edn
  5-answer-field.edn
  6-answer.edn
  7-multistep.edn
  8-assigned-problem.edn

learner/
  1-1-learner.edn
  1-2-learner-performance.edn
  1-3-learner-progress.edn
  2-1-learner-task.edn
  2-2-learner-task-item.edn

engine/
  1-fire-policy.edn
  2-question-weights.edn
  3-xp-weights.edn           # fixed earned-XP rule identities and formulas
  3-default-fire-policy.edn   # seed transaction data
```

The [course transactions](data/2-3-courses.edn) import all 32 identities from `MA/DATA/Courses.csv` and their descriptions, overviews, and outcomes from `MA/DATA/Course-Maps`. [Course-unit links](data/3-3-course-units.edn) complete their required membership. The [course-group transactions](data/1-2-course-groups.edn) organize courses into nine catalog groups and retain course navigation links. University includes both Math Academy and Oregon State courses. Group membership does not change topic prerequisites or learner progress. Course level is no longer part of the model; group titles supply catalog labels.

The live migration renamed `sequence/*` attributes in place to `course-group/*`; EDB retains the old names as aliases. All current `course/level` values were retracted. EDB cannot remove an installed attribute, so its unused definition remains marked retired in the database and is omitted from these fresh-install schema files.

The PostgreSQL-backed EDB database `course-academy-v2` uses the revised content model. It was built from the current reconciled records in `course-academy` at basis 143, preserving corrected content and answer keys. The original database and its backup remain intact. The initial import contained 315 units, 1,122 modules, 2,971 named MA topics plus four prerequisite-only placeholders, 9,636 knowledge points, 6,016 tutorials, 9,636 worked examples, 19,646 practice questions, and 2,964 lesson activities. Worked examples and ordinary questions share `question/id`. A question is a worked example when a `knowledge-point/canonical-example` reference targets it; those targets are excluded from every KP practice pool. Optional `question/math-academy-id` prefixes identify imported source records and do not determine their current role. Seven catalog topics have no captured lesson.

In the initial imported catalog, 10,978 of 22,840 answer fields have canonical correct answers, covering all fields of 10,742 practice questions. The remaining 8,904 practice questions retain at least one missing answer; migration does not invent missing content. There are 95,445 field-owned answer entities after merging 45 exact duplicates within their respective fields, with an explicit UUID replacement map. Recovered feedback is attached to 100 answers. Current content and relationships were transferred; the source transaction history stays in the original database. No learner attempt records were present in that source snapshot.

[build_content_migration.py](../scripts/build_content_migration.py) prepares the transfer from the native offline export, and [verify_content_migration.py](../scripts/verify_content_migration.py) compares every resulting domain fact by stable identity. The local backup, batches, duplicate map, and verification report live under ignored `.local/edb/content-migration/` and `.local/edb/backups/`. The raw-capture [seed generator](../scripts/generate_ma_lesson_seed.py) remains available for initial imports; regenerating raw seed data does not reproduce the later reconciliations.


On 2026-10-04, the active database retired `question/is-example` in one atomic transaction at basis 416. Its 30,452 current boolean facts were retracted and the attribute was removed from `question/validate`; the installed definition remains marked retired because EDB cannot uninstall attributes. Fresh schemas and importers omit it. The database contains 9,637 canonical examples and 20,815 ordinary questions, including all 1,170 questions added since the earlier active export. Verification found all 840,524 other domain facts unchanged, including answer keys, curriculum relationships, and learner records. See the [migration record](../reference/canonical-example-migration.md).

Readers derive roles from canonical references in the same captured database value as the questions. A partial projection must include incoming canonical references for its question targets. When interpreting past presentations, use the historical database value for their roles as well. A worked solution alone does not make a question an example, and an ordinary question needs complete, keyed answer fields before automatic grading.

Run [start_local_edb.sh](../scripts/start_local_edb.sh) to restart local PostgreSQL if needed and run the Course Academy writer with its native predicates. It stays in the foreground; leave that terminal open while transacting. Its default database is `course-academy-v2`, with endpoint `/tmp/course-academy-edb-v2/writer.sock`; `EDB_DATABASE` and `EDB_ENDPOINT` can override those defaults. The private PostgreSQL socket is under `.local/edb/run`. For read-only CLI queries, set `EDB_POSTGRES_URL="host=$PWD/.local/edb/run dbname=course_academy user=edb_peer sslmode=disable"` and pass `--database course-academy-v2`. This local setup uses the PostgreSQL 15 installation bundled with MATLAB and the sibling EDB release build; set `PG_CTL` or `EDB_ROOT` if those locations differ.

Course groups collect shared courses through `course-group/courses`; courses, units, and modules hold their members through `course/units`, `unit/modules`, and `module/topics`. These collections are unordered. `topic/next` stores the single prerequisite graph with edges pointing from a prerequisite to its direct dependents. Reverse lookup supplies a topic's prerequisites; traversal supplies transitive dependencies. The engine uses these incoming edges for readiness and diagnostic scope. `course/next`, `unit/next`, and `module/next` support navigation between collections and do not introduce additional readiness requirements. Course maps and map entries are no longer needed. Topics and knowledge points define skills, while lessons, tutorials, and questions (including worked examples) provide teaching material. Encompassing records describe weighted practice coverage, separately from prerequisites.

A **learner task** is one learner's task for a lesson, review, assessment, diagnostic, or assignment. Initial and supplemental diagnosis use the same diagnostic schema. [2-1-learner-task.edn](learner/2-1-learner-task.edn) records its status, XP, and elapsed working time using `learner-task/*` attributes. Status is one of `locked`, `unlocked`, `started`, `paused`, `completed`, or `failed`; it replaces the separate task outcome. Paused means suspended and unfinished; completed means finished under the activity's rules; failed means an explicit task-level failure. Its `learner-task/activity` ref points to the shared activity definition, which contains no learner results. `learner/activity` contains these learner-specific tasks and their attempt history, not shared activity definitions. Availability states are represented by the schema; maintaining them belongs to application scheduling.

A task owns its presentation records through `learner-task/items`, defined in [2-2-learner-task-item.edn](learner/2-2-learner-task-item.edn). Optional ordinary `task-item/next` refs link these members in presentation order; the last item has no next ref, and the first has no incoming sibling link. The runtime checks for one connected chain, rejecting cycles, merges, and links outside the task. Each item records its own status, elapsed time, and responses and references shared instructional content. Responses point directly to answer entities owned by the question field through `answer-field/choices`, including distinct values entered in blank fields. `answer-field/correct` points to one member of that collection. The referenced activity supplies activity/type; item content kind is derived from its target. Neither needs a duplicate type attribute on the learner task or item.

The shared [step schema](content/1-step.edn) replaces lesson-step and multistep-step. It references content and uses an optional next link for sibling order. An assignment can contain one multipart problem or several problems. Reusable [multistep content](content/7-multistep.edn) owns its shared context and inner generic steps; finishing its last step returns to the enclosing sequence. An [assigned problem](content/8-assigned-problem.edn) is a separate entity referenced by step/content, with its own identity, optional topic coverage, and a content ref to a question or multistep. This allows external problems to be imported before their preparation targets are mapped. Task items continue to record actual presentations during a learner attempt. The runtime still awaits migration.

Diagnostic routing now belongs to [generic steps](content/1-step.edn), through the optional `diagnostic-probe/on-*` attributes on those same entities. The separate diagnostic-probe schema has been removed. Runtime diagnostic traversal still requires migration to activity/steps and step/content. Actual presentations remain learner task items.

The learner's `learner/knowledge-profile` owns current `progress` records, one per topic. The reverse reference `learner/_knowledge-profile` identifies a record's learner. The displayed queue is derived from eligible, unfinished tasks in `learner/activity`, ordered by `learner-task/priority`; the application's priority threshold determines required work. There is no separate queue entity or learner/queue attribute. Starting required work does not satisfy it: the scheduler retains the obligation until its completion condition is met. See [progress validation](../engine/edb/README.md) for the Rust predicates and write requirements.

`learner/performance` optionally owns one global accuracy summary, defined in [1-2-learner-performance.edn](learner/1-2-learner-performance.edn). Its four `performance/*` attributes hold assessment/practice accuracy and evidence mass across topics; per-topic estimates remain on `progress`. The summary is found through the learner ref and needs no separate domain ID. Ensure `performance/validate` on the child when writing its values; `learner/validate` remains the minimal learner spec. Single ownership and numeric ranges remain application contracts.

[Task items](learner/2-2-learner-task-item.edn) use `started`, `paused`, `completed`, `skipped`, `correct`, and `incorrect` statuses. `completed` ends a tutorial or example; questions end with a correctness or skip status. Status transaction history supplies both clocks: item working time totals the intervals spent in `started`, while calendar time uses the recorded transaction instants. Task elapsed time is the sum of its item durations. Pausing stops working time but does not extend a timed exam's deadline. The application must record transitions when they happen and retain their history. The Rust [completion handler](../engine/rust/runtime.rs) converts completed evidence into accuracy and retention updates; the [schema adapter](../engine/rust/schema.rs) prepares their atomic EDB write.

Courses, units, modules, topics, and knowledge points have an `identity-validate` spec for ID-only placeholders and an existing `validate` spec for their required data. This supports loading one hierarchical level at a time, then filling in and linking the records through their stable IDs. Full validation checks each entity's own required attributes; referenced content must also be validated before it is served for study.

These five placeholder specs cover the current curriculum-loading workflow. We can add the same option to lessons, questions, or tutorials when staged content generation needs it.

`data/5-1-topic.edn` includes optional `topic/difficulty`, a positive finite lesson workload multiplier, default 1.0. It affects base XP only. Progress has optional separate expected assessment/practice accuracy forecasts initialized from direct prerequisites. Ensure `topic/difficulty-validate` on difficulty-only updates. `topic/validate` also checks difficulty if present, while identity-only placeholders remain supported.

[1-fire-policy.edn](engine/1-fire-policy.edn) defines FIRe parameters under a stable `policy/id`. Ensure `policy/validate` when editing them. EDB history preserves earlier values: inspect past progress and its referenced policy in the same historical database value with `as_of`. Editing a policy leaves stored `progress/interval-days` unchanged until the engine recomputes it; it does not automatically reschedule every topic.

[3-xp-weights.edn](engine/3-xp-weights.edn) installs documentation identities for the fixed version-one earned-XP rules. It is a valid EDB transaction containing `db/ident` and `db/doc` records, not a set of mutable coefficient attributes. Both engine implementations calculate these rules by default; the Rust study player uses the same shared calculator. Keep changes to a rule's equations, engine code, examples, and regression expectations together. Base XP and question-selection distributions remain separate from the earned/base adjustment. See the [earned-XP report](../reference/xp-docs/earned-xp-formula-report.md) for the complete formulas and denominator rules.

The completion handler prepares one transaction containing the item status, responses, item/task elapsed totals, affected progress, overall performance, and any task completion/XP. It uses the same transaction instant for timing and recorded history, and guards completion with an item-status compare-and-swap. Submission must use the returned exact-basis guard and request key; retain the original plan for retries. The Rust adapter exists; wiring its callbacks to a production UI and durable EDB writer remains application work. See [native validation and engine mapping](../engine/edb/README.md).

## Activity models

Lessons, reviews, assessments, diagnostics, and assignments use the shared activity schema and its activity/type enum. Multistep is reusable problem content; standalone multistep practice is an assignment containing one multistep problem. Intended topic scope comes from the referenced activity; question ownership supplies the topic for observed answers. Task status and priority supply queue eligibility and required-work priority. The completion handler implements activity progression and engine-boundary checks. Required-attribute specs remain opt-in; the adapter is not a general validator for every curriculum-editing operation or a complete queue scheduler.

## Remaining work

`knowledge-point/question-generator` still needs its representation and generator interface finalized; a repository-relative Python file path is the current recommendation, but the installed attribute is a ref. The [scheduling](../reference/scheduling-proposal.md), [XP](../reference/xp-proposal.md), and [answer-grading](../reference/answer-grading-proposal.md) proposals give concrete application rules for review. A completed diagnostic retry replaces the original answer for frontier placement; both presentations remain in history and submitted-answer accuracy.

`learner/course` records the course selected in the UI. Broader concurrent study scope is deferred. Queue scheduling and the production UI/EDB connection remain implementation work. Preventing repeat questions uses the existing learner activity history; serving must atomically select and reserve an unseen question before displaying it. Cross-task no-repeat enforcement is not yet implemented and needs no duplicate `question/seen-by` attribute.
