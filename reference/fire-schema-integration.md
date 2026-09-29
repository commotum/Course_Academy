# How the learning engine plugs into our schema

The current implementation is Python application code: [FIRe](../engine/fire/core.py) updates numerical state, [activity helpers](../engine/activities.py) evaluate practice and XP, and [the completion runtime](../engine/runtime.py) connects task items to those updates. [The adapter](../engine/schema.py) reads an EDB entity snapshot and prepares one guarded transaction. EDN defines stored facts and validation contracts; it does not execute the learning algorithm.

```text
shared content → learner task → ordered task items and responses
                                    ↓ complete_item
                      updated progress + global performance
                                    ↓
                         one EDB transaction plan
```

| Stored facts | Role |
| --- | --- |
| Topics, KPs, questions, answers | Shared content. Resolve an answered question's topic through its KP bank and topic relationships; task items do not copy those refs. Lessons own ordered tutorial/KP placements; KPs link examples and question pools. |
| Prerequisites and encompassings | Prerequisites constrain learning readiness. Separately weighted encompassing relationships determine FIRe practice transfer. |
| Learner tasks and items | Attempt status, actual presentations, submitted responses, result, order, timing, and supplied performance magnitude. XP belongs to the task and is separate from correctness. |
| Progress and performance | One learner-owned progress record per topic, shared across courses, plus the learner's global accuracy summary. Progress stores learned status, repetitions, anchored memory, interval, accuracy channels, and policy ref. |
| Policy and difficulty | [Engine policy](../schema-v2/engine/1-fire-policy.edn) stores typed parameters. Optional `topic/difficulty` is expected assessment accuracy in `[0,1]`; question E/M/H labels have a different meaning. |

Each submitted answer updates accuracy once. Lesson and review completion supplies one aggregate retention unit, scaled by supplied performance. Assessment and multistep answers divide that magnitude by the number of questions for the same topic in the definition. Diagnostic answers instead accumulate signed prerequisite-graph balances; positive final balances initialize previously unlearned topics. Explicit skips do not count as submitted-answer accuracy; the local diagnostic default treats them as negative placement evidence.

The runtime checks authored membership and stopping rules. Its local readiness rule requires a lesson's prerequisites to be learned and not currently due. Required, recommended, and self-selected work use the same completion rules. The broader queue scheduler, remediation assignment, and assessment assembly are separate work; the completion adapter does not implement them.

An application timer can call `expire_task` for a configured assessment or diagnostic limit. It closes the task using recorded evidence, without inventing skipped answers for unpresented questions or guessing partial-exam XP.

The transaction plan saves item completion, responses, affected progress, global performance, and applicable task outcome/XP together. The writer must submit its exact request key and database-basis guard; an item completion compare-and-swap prevents applying the same item twice. Retry the original plan after an uncertain submission. A new item identity is new evidence, so transport retry protection does not deduplicate a semantically duplicated task.

Policy parameters can change under a stable `policy/id`. EDB history and historical database views recover earlier values; existing progress retains its stored interval until the engine recomputes it. Editing a policy does not automatically reschedule every topic. Python `Event` objects and debug receipts remain runtime tools, with no separate event or update-receipt entities in schema-v2.

**Implementation boundary:** the Python adapter and completion runtime are implemented and verified by the Python suite and a native EDB transaction round trip. They return transaction plans; they do not connect to a database. Rust currently supplies EDB validation predicates and checks. A production UI, durable writer, and Rust numerical engine are not implemented. See [the data contract](fire-data-model.md) for ownership and [the reconstruction](fire-reconstruction.md) for evidence and local choices.
