# Content and data schema review

Initially reviewed all 18 EDN files in `content` and `data` against EDB's [schema best practices](/home/jake/Developer/EDB/docs/02_core_concepts/05_best_practices.md), [schema reference](/home/jake/Developer/EDB/docs/03_schema/02_schema_reference.md), and [Pull reference](/home/jake/Developer/EDB/docs/05_query_and_pull/06_pull_reference.md).

The overall structure is sound. We already store relationships in one direction, distinguish reusable entities from owned records, use domain-specific unique identities, represent enums with ident entities and refs, and separate instructional content from learner evidence. The largest remaining improvement is to implement the relationship rules currently documented as application contracts. Required attributes alone cannot enforce those rules.

This review records the initial recommendations. Since that review, typed policy validation and topic difficulty/evidence validation have been implemented; see `data/4-3-topic-difficulty.edn`, `fire/1-policy.edn`, and `../engine/edb/configuration.rs`. Other proposed ownership/content checks remain pending.

## One direction is enough

None of the reviewed models needs an additional stored parent reference merely for navigation. These reverse references already provide it:

| Stored relationship | Reverse navigation |
| --- | --- |
| `course/units` | `course/_units` on a unit |
| `unit/modules` | `unit/_modules` on a module |
| `module/topics` | `module/_topics` on a topic |
| `topic/knowledge-points` | `topic/_knowledge-points` on a KP |
| `knowledge-point/questions` | `knowledge-point/_questions` on a question |
| `knowledge-point/example` | `knowledge-point/_example` on an example |
| `course/map` | `course/_map` on a map |
| `course/outcomes` | `course/_outcomes` on an outcome |
| `lesson/steps` | `lesson/_steps` on a step |
| `question/answer-fields` | `question/_answer-fields` on a field |
| `learner/knowledge-profile` | `learner/_knowledge-profile` on progress |
| `learner/performance` | `learner/_performance` on the global performance summary |
| `learner/queue` | `learner/_queue` on a queue entry |
| `learner/activity` | `learner/_activity` on a task |
| `learner-task/items` | `learner-task/_items` on a task item |

Reverse navigation discovers the parents; it does not, by itself, enforce how many parents are allowed. Component reverse Pull returns a single parent map, so ownership checks should use query or the VAET index to detect invalid sharing rather than relying on that result shape.

`lesson/topic` is also appropriate: the lesson references the topic it teaches. There is no reason to add a separately maintained `topic/lessons` attribute.

## Ownership should follow lifecycle

Component refs mean that deleting a parent entity also deletes its components. They are not simply a convenient way to display nested data, nor a built-in single-owner constraint.

| Relationship | Current modeling | Recommendation |
| --- | --- | --- |
| Course → units → modules → topics | Ordinary refs | Keep. Membership and sequencing are separate; deleting a course should not automatically destroy shared curriculum. |
| Topic → knowledge points | Ordinary refs | Keep for now. Restricting KP membership, if desired, is separate from deciding whether deleting a topic should delete its KPs. |
| KP → example | Ordinary ref | Keep. The example is independently identified instructional content. |
| KP → questions | Ordinary refs | Keep the lifecycle choice. Enforce the intended single-KP bank membership separately before admitting questions to the usable bank. Task-item presentations reuse a question without changing its bank membership. |
| KP → question generator | Ordinary ref | Appropriate if generators can be independently maintained or shared. The generator schema is still missing. |
| Course → map → entries → child entries | Components | Correct. These are course-specific placements of independently identified curriculum. Add single-owner and tree-consistency checks. |
| Course → outcomes | Components | Correct. Outcomes belong to a course. Add single ownership and unique indexes within that course. |
| Topic → encompassing records | Components | Correct. The relationship belongs to its source topic; its target remains an ordinary ref. Add ownership, distinct targets, and graph checks. |
| Lesson → steps | Components | Correct. A step is a placement; tutorial/KP content is independently referenced. Add ownership and unique indexes within a lesson. |
| Question → answer fields | Components | Correct. A field belongs to one question. Add ownership and unique keys within a question. |
| Answer field → choices and correct answer | Components | Correct under our current field-owned-answer model. Check owners across both attributes, treating two links from the same field as one owner. |
| Learner → progress | Components | Correct; implemented ownership predicates now cover this relationship. |
| Learner → performance | One optional component | The global accuracy summary belongs to one learner and is accessed through that learner. No separate domain ID or stored learner backref is needed. Add single-owner and numeric-range checks; cardinality one only limits each learner to one summary. |
| Learner → activity history (tasks) | Ordinary refs | `learner/activity` contains task records; each task owns its presented items. The writer must preserve its learner association while history is retained. |
| Learner → queue entries | Components | Current up-next entries belong to one learner. They reference shared content through ordinary refs. Optional entries can be dismissed; launching required work does not satisfy its obligation. The controller must carry or recompute it until its completion condition is met. Retain task history separately. Add ownership and distinct positive index checks. |
| Task → items → submissions → submitted answers | Components | These are learner-specific presentation and response records. Tasks and task items are under `learner`; task-group, submission, and submitted-answer schemas remain in `proposed` until personally reviewed and explicitly moved. The task references its shared activity definition; task items reference shared questions, tutorials, or examples. Canonical answers and optional authored source steps also remain ordinary refs. Add ownership and target checks. |

The current question-bank model expresses our intended design, not a claim that all captured MA question memberships have already been reconciled. The inventory notes reused placements; import must resolve their meaning before applying a single-bank rule.

## Similar structures can use similar validation

Keep the small child schemas. Put rules about a collection on its parent spec, and rules about a child's own values on its child spec. Use entity predicates for relationships and attribute predicates for reusable scalar restrictions. Both must have real registered implementations.

| Schema | Checks still needed beyond required attributes |
| --- | --- |
| Course | Unit target types; outcomes and map ownership; outcome indexes distinct within the course. Validate the map separately. |
| Unit | Module target types. Do not impose a single course owner without an explicit domain requirement. |
| Module | Topic target types. Shared topics are intentional. |
| Topic | KP target types; valid prerequisite targets; no prerequisite self-links or cycles. Encompassing targets are separate relationships, not inferred prerequisite credit. |
| Encompassing | Exactly one source owner; valid target topic; finite weight in `[0,1]`; distinct target per source; no self-link or cycle. |
| Knowledge point | Correct example/question/generator target types. The usable bank must respect the intended question membership rule. |
| Course map | Exactly one course owner; entries form the intended hierarchy and cover membership. |
| Course-map entry | Exactly one owner across map entries and parent-entry children; no shared/cyclic placement nodes; positive sibling-unique index; correct content type and membership at its depth. Topic entries have no children. |
| Course outcome | Exactly one course owner; positive index unique within that course; usable outcome text. |
| Lesson | Correct topic; valid steps; unique step indexes; KP steps belong to the taught topic. Define whether a complete lesson must cover every KP before enforcing that requirement. |
| Lesson step | Exactly one lesson owner; positive index; content is a tutorial or KP. |
| Tutorial | Usable title/body. Markdown is an appropriate representation of ordered prose, equations, tables, and images; no fixed problem/answer structure is warranted. |
| Example | Usable problem/explanation. Preserve the distinction between demonstration and machine-gradable question. |
| Question | Supported interaction and difficulty enum members; valid fields; unique field keys; one field for multiple choice; choices for selection interactions and no choices for blanks under the current model. |
| Answer field | Exactly one question owner; valid answer targets; correct answer is among choices when choices exist. |
| Answer | Supported representation enum; string content compatible with that representation; one field owner across choices/correct-answer links. Asset existence and mathematical correctness require separate application checks. |
| Learner | Profile ownership/topic uniqueness checks exist. Validate the optional performance child separately with `performance/validate`. |
| Performance | Exactly one learner owner; finite accuracy in `[0,1]` and nonnegative finite evidence masses. The child spec requires all four values; ownership and ranges remain application contracts. |
| Progress | Owner/topic uniqueness checks exist. Retention, accuracy and mass ranges and valid policy/receipt targets remain application contracts. |
| Queue | Exactly one learner owner; positive index unique within that learner’s queue; supported selection enum (`required`, `recommended`, `self-selected`); valid content and optional course refs; nonblank reason. Mandatory-work enforcement and failure/XP triggers belong to application policy. Required attributes alone do not enforce these rules. |
| Task | Exactly one learner association; valid activity target; supported status/outcome enums; owned items/groups; valid retake/remediation refs; finite nonnegative timings. |
| Task item | Exactly one task owner; positive index unique within that task; supported result enums; correct content and optional source-step targets; same-task groups; finite nonnegative timings; owned submissions. Derive content kind from the target instead of storing a type enum. |

Parent predicates do not replace complete child validation. ID-only curriculum placeholders must remain valid while content is being assembled; validate full referenced content before serving it. Avoid a predicate that recursively demands fully populated descendants on every placeholder write.

For ownership and uniqueness rules, validate affected parents on membership changes and affected surviving children on child changes, removals, or transfers. Otherwise a topic, field key, or index change can bypass a parent-only check. Deleting a component is distinct from merely retracting its parent link.

## Two answer links have different meanings

`answer-field/answer-choices` means “what may be selected.” `answer-field/correct-answer` means “what is expected.” These are not redundant forward/backward copies of one relationship. Keeping both is natural.

In a selection field, the correct answer is reached through both attributes. An ownership predicate must collect the distinct field entities across both reverse relationships. Two references from the same field are valid; references from different fields are not. For a blank, only the correct-answer link is needed. There is no need for a stored `answer/field` attribute.

## Other practices to retain

- Domain UUID identities and optional attribute-specific MA identities are appropriate. An MA course ID and topic ID can have the same number without colliding because uniqueness is per attribute. Confirm that each imported MA ID identifies the corresponding entity rather than an occurrence before using identity upserts.
- Ref-based enum members are correct. A ref value type alone does not restrict the attribute to the declared members; implement that check.
- Keep cardinality-many relationships unordered. Entry indexes preserve authored sequence; field keys bind responses to problem locations. Neither belongs on a reusable topic or answer merely to preserve one presentation's order.
- Do not add `noHistory` to progress by default. Historical state is useful while validating the engine, and it is a storage decision rather than a correctness mechanism.
- Learner identity and relationships use `learner/*`; its global accuracy summary uses `performance/*` on an owned child. Per-topic accuracy stays on `progress/*`. Naming does not change ownership semantics.
- `question-generator` still needs a schema. The task attempt schema is in `learner/2-1-learner-task.edn`, its item presentations in `learner/2-2-learner-task-item.edn`, and supporting group/response drafts under `proposed/` alongside shared activity definition drafts. The current queue is modeled in `learner/1-4-learner-queue.edn`. Their detailed domain predicates remain pending.

## Recommended next work

Start with the question → answer-field → answer chain. It is the closest match to learner → progress, and the missing invariants are concrete: one owner, distinct field keys, valid choice membership, and allowed types. Then apply the same approach to lesson steps, outcomes, and encompassing records. Course-map validation is a larger whole-tree check and should follow those smaller cases.

No extra parent attributes or generic relationship entities are needed for this work. The existing simple EDN structures can remain; the missing piece is executable validation attached to their specs and consistently requested by writers.
