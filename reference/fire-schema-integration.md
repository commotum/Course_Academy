# How the learning engine plugs into our schema

The current implementation is Rust application code: [FIRe](../engine/rust/core.rs) updates numerical state, [activity helpers](../engine/rust/activities.rs) evaluate practice and XP, and [the completion runtime](../engine/rust/runtime.rs) connects task items to those updates. [The adapter](../engine/rust/schema.rs) reads an EDB entity snapshot and prepares one guarded transaction. EDN defines stored facts and validation contracts; it does not execute the learning algorithm.

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
| Learner tasks and items | Attempt and item statuses, actual presentations, submitted responses, order, elapsed time, and supplied performance magnitude. Question correctness is a terminal item status. XP belongs to the task and is separate from correctness. |
| Progress and performance | One learner-owned progress record per topic, shared across courses, plus the learner's global accuracy summary. Progress stores learned status, repetitions, anchored memory, interval, accuracy channels, and policy ref. |
| Policy and difficulty | [Engine policy](../schema/engine/1-fire-policy.edn) stores typed parameters. Optional `topic/difficulty` is expected assessment accuracy in `[0,1]`; question E/M/H labels have a different meaning. |

Each submitted answer updates accuracy once. Lesson and review completion supplies one aggregate retention unit, scaled by supplied performance. Assessment and multistep answers divide that magnitude by the number of questions for the same topic in the definition. Diagnostic answers instead accumulate signed prerequisite-graph balances; positive final balances initialize previously unlearned topics. Explicit skips do not count as submitted-answer accuracy; the local diagnostic default treats them as negative placement evidence.

The runtime checks authored membership and stopping rules. Its local readiness rule requires a lesson's prerequisites to be learned and not currently due. Required, recommended, and self-selected work use the same completion rules. The broader queue scheduler, remediation assignment, and assessment assembly are separate work; the completion adapter does not implement them.

Status transaction history supplies both clocks. Item elapsed seconds sum intervals spent in `started`, excluding `paused`; task elapsed seconds sum its item durations. Calendar time comes from the same transactions and governs retention decay and exam deadlines. The application records each transition when it happens. Pausing suspends working time but does not extend an exam deadline.

An application timer can call `expire_task` for a configured assessment or diagnostic limit. It pauses any active unanswered item and closes the task using recorded evidence, without inventing answer verdicts or guessing partial-exam XP.

The transaction plan saves item status, responses, derived elapsed totals, affected progress, global performance, and applicable task status/XP together. Its explicit transaction instant matches the time used in the calculation. The writer must submit its exact request key and database-basis guard; an item-status compare-and-swap prevents applying the same item twice. Retry the original plan after an uncertain submission. A new item identity is new evidence, so transport retry protection does not deduplicate a semantically duplicated task.

Policy parameters can change under a stable `policy/id`. EDB history and historical database views recover earlier values; existing progress retains its stored interval until the engine recomputes it. Editing a policy does not automatically reschedule every topic. Runtime `Event` objects and debug receipts remain runtime tools, with no separate event or update-receipt entities in schema.

**Implementation boundary:** the Rust numerical engine, adapter, completion runtime, and audit tools are implemented. Rust tests, comparisons with the retained Python implementation, and a native EDB transaction round trip verify the port. The adapter returns transaction plans; it does not connect to a database. A production UI, durable writer, and full queue scheduler remain application work. See [the data contract](fire-data-model.md) for ownership and [the reconstruction](fire-reconstruction.md) for evidence and local choices.
