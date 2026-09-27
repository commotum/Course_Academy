# Progress ownership

`learner/knowledge-profile` owns progress records. Each record references a shared topic through `progress/topic`; its learner is available through the reverse reference `learner/_knowledge-profile`. Component ownership gives progress the learner's lifecycle, while deleting progress does not delete the topic.

[progress.rs](progress.rs) implements the entity predicates named in the EDN. `valid-profile?` checks that every member has an ID, a real topic, exactly this learner as owner, and a distinct topic within the profile. An empty profile is valid. `valid-progress?` checks that the record has exactly one owner and checks that owner's profile. This also catches topic changes that create duplicates.

Register these callbacks with `register_progress_predicates` in a `TxFunctions` registry supplied to `Database::with_forms`. For a durable writer, register the same checks using EDB's `NativeRegistryBuilder::entity_predicate` with cooperative cancellation; that writer integration remains to be implemented.

On progress writes, request `:db/ensure :progress/validate`. On membership changes, request `:db/ensure :fire-learner/validate` for affected learners and `:progress/validate` for affected surviving progress records, including detached records. Create the learner link and progress in the same transaction. To remove progress, retract the component entity; to transfer it, retract the old link and assert the new link atomically. A learner deletion cascades to its progress.

Specs are opt-in: bypassing `:db/ensure` bypasses these checks. The learner's minimal validation permits ID-only progress placeholders with a topic; ensure each progress record's complete spec before using it in the engine. Global accuracy still has its separate `fire-learner/ability-validate` spec. Activity history remains an ordinary reference collection pending its own schema.
