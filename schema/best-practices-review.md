# Schema and engine review — 2026-09-28

The current `schema/` contains 30 EDN files: 9 data, 13 content, 7 learner, and 1 engine schema. It replaces the deleted legacy schema; the proposed folder has also been removed. This review covers the current definitions, including the cleanup of groups, submissions, course-map children, and topic-calibration fields.

Basis: EDB [best practices](/home/jake/Developer/EDB/docs/02_core_concepts/05_best_practices.md), [schema reference](/home/jake/Developer/EDB/docs/03_schema/02_schema_reference.md), and [transaction data](/home/jake/Developer/EDB/docs/04_transactions/04_transaction_data.md), compared with the actual schemas and engine implementation.

The hierarchy is sound. The approved cleanup moved policy to `engine`, removed the separate processing record and progress pointer, added optional item completion time, and made policy settings editable with retained EDB history. The Python engine now has a current-schema adapter and item-completion controller; a production UI/writer and full scheduling application are separate work.

## Verification

The Python suite covers the numerical core, captured research observations, activity rules, current-schema loading/writeback, and automatic completion flows. Run `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'` from the repository root.

Native EDB checks install all 30 current EDNs and exercise configuration/history, progress ownership, current activity records, and guarded generated transactions. These in-memory checks do not mean a production durable writer has been deployed. See [the adapter integration instructions](../engine/edb/README.md).

## What to retain

| Schemas | Finding |
| --- | --- |
| Course, unit, module, topic, knowledge point | One-direction membership, independent shared curriculum, local identity, and optional source IDs fit EDB. Keep ID-only validation for staged loading. |
| Course map, entries, outcomes | Indexed course-specific records are appropriate. The current map is flat; there are no child-entry refs. Membership and sequence have distinct purposes and need consistency checks. |
| Topic prerequisites and encompassing | Different relationships: readiness versus implicit practice coverage. Owned encompassing records correctly obtain their source from their parent topic. |
| Lesson/step and multistep/step | Keep indexed authored placements and the distinct schemas. A lesson KP placement can generate several presentations; a multistep placement references a question. |
| Tutorial and example | A tutorial's Markdown body accommodates varied exposition. A worked example has a problem and explanation. Neither needs a graded-question wrapper. |
| Question, answer field, answer | Separate interaction, response location, and answer value are useful. Choices and correct answer are different facts, even when they reference the same answer entity. Keep field keys; application code controls option order and grading. |
| Review and assessment | Direct question collections suffice. Review/topic is an instructional target; aggregate assessment/multistep topic coverage is derived from questions. No assessment-step is currently justified. |
| Diagnostic and probe | Prepared probes and alternate retry questions are useful. Static branching is the approved current design; it should not be mistaken for the entire profile-adaptive selection algorithm. |
| Learner, performance, progress, queue | Global accuracy, per-topic knowledge, and planned work are distinct. Reverse refs supply their owners; no duplicate learner attributes are needed. |
| Learner task, item, response | Separate activity definitions from attempts and actual presentations. Selected responses point to existing answers; typed responses store field plus value. |
| Policy | Sixteen computational settings map to the numerical Policy fields. Its UUID is a stable database identity; the Python policy fingerprint is a different concept. Name and the single-value algorithm selector have been removed from the schema. |

Ref enums do not automatically restrict values to their intended enum members. Components provide cascading deletion, not exclusive ownership. EDB's one-direction guidance does not require every entity to share a generic step/type abstraction. The recommendation to avoid string-built queries does not prohibit Markdown, LaTeX, or optional debug payloads.

## Engine boundary

[engine/schema.py](../engine/schema.py) reads one captured EDB basis. It resolves the learner through ownership, resolves a question through its single knowledge-point bank and topic, loads typed policy settings and encompassing weights, and validates numeric progress/performance. It rejects ambiguous memberships and shared progress ownership instead of storing another topic or learner ref.

[engine/runtime.py](../engine/runtime.py) accepts an application-graded completion. Submitted answers update accuracy once. A completed lesson or review supplies one graded retention unit; assessment and multistep evidence is apportioned across each topic's questions. Diagnostic placement uses a separate prerequisite-graph balance, with skips retained as explicit skips. Tutorial/example completion supplies no correctness observation.

The adapter prepares the response, item completion, progress, global performance, and any task result/XP in one transaction. Submit with its exact basis guard and native request key. Retain the original plan for exact retries. Item completion CAS prevents another request from crediting an already-completed presentation; timer expiry uses task-status CAS and creates no fake skipped questions. The application still supplies grading, timers, entity snapshots, and durable submission.

Current validation is a boundary, not a replacement for every database-writing contract. [progress.rs](../engine/edb/progress.rs) now checks numeric retention/accuracy bounds and a policy target in addition to ownership. Minimal learner validation still permits import placeholders. General curriculum writers must also check field/step ownership, parent membership, enum targets and other documented invariants when they change relationships. Components alone do not enforce exclusive ownership.

## Explicit local choices

The numerical policy still controls interval growth, decay thresholds, accuracy priors/rates, speed, implicit-credit gating, and update order. Exact proprietary coefficients are not needed to implement and tune these rules.

The controller currently uses two consecutive correct answers within five for a KP and three consecutive correct within five for a review. Lesson readiness requires learned prerequisites that are not currently due. These are local delivery rules, informed by the research, not a claim that every historical MA activity followed them.

Diagnostic skips give negative placement evidence by default but add no answer-accuracy observation. Both answers of an accepted retry remain evidence; cancellation is not established by the captures. Supplied reduced positive weights are supported, with no guessed duration threshold. Initial placement does not erase established retention histories. Those choices are application configuration, separate from FIRe parameters.

Perfect lesson/review XP has observed candidate rules. Fitted assessment/multistep equations require explicit opt-in; unresolved partial lesson/review awards remain absent unless supplied by application policy. XP never stands in for correctness, retention credit, or elapsed time.

## Policy references and history

[1-fire-policy.edn](engine/1-fire-policy.edn) contains a stable UUID, sixteen settings used by the numerical engine, optional description, and validation. Neither a policy name nor a single-implementation algorithm selector is required.

Its only domain reference selects one of the two update-order enums declared in the same file. `course-academy.policy/valid?` is the Rust callback in `engine/edb/configuration.rs`, not a missing domain entity. The Python snapshot's legacy label and fingerprint are not database attributes.

Update policy under the same identity and keep history. To recover settings used for a past progress change, read the policy at that transaction's historical database value. A threshold edit changes the current due calculation; interval growth settings affect stored intervals only when recomputed. No automatic bulk rescheduling is implied.

## Remaining application work

The core and completion adapter do not yet implement the whole study application: generating fresh content, selecting study scope, populating/reordering the queue, maintaining mandatory-work obligations, estimating expected duration, assembling assessments, and deciding remediation cadence remain scheduler/content work. The numerical ranker still accepts already-eligible candidates with explicit expected durations.

The schema does not yet define the target of `knowledge-point/question-generator` or a durable selected-study-scope relationship. Add those when implementing those features; no generic event, update, calibration-count, or duplicate inverse relationship is needed for the current completion path.
