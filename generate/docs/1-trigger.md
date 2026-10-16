# 1. Trigger

Automatically call [Inventory](2-inventory.md) for a topic when:

- It is added to `:learner/queue`.
- It is added to `:learner/targets`.
- Its learner task enters `:learner-task.status/unlocked`.
- Its learner task is started or paused, including work outside the queue or targets.
- A review of it becomes due or is assigned, including remedial reviews.
- It is selected for an upcoming assessment.

Retakes use the same activity triggers and inventory requirements. Topic selection and eligibility must happen before filtering by question supply; an empty bank must still trigger inventory.

Use **event hooks** from the scheduler and committed database changes. Follow the most efficient [$edb](../../skills/edb/SKILL.md) practices: read relevant changes from the transaction log, retain the processing position across restarts, and batch checks for affected topics. Time-based review triggers come from the scheduler.

1. Pass the affected topics and activity types to Inventory.
2. If inventory is sufficient, no generation is needed. Otherwise, queue background generation for the shortages, reusing existing jobs for overlapping pools.
3. After generated questions are validated and committed, recheck inventory and continue any pending activity preparation automatically.

Recheck availability before starting an unstarted activity. Preserve already started or paused work; existing required-work rules still apply while generation runs.

The read-only `generate/scripts/find_candidates.py` now provides a separate
generator-build ranking. Eligibility is studied, target, queued, direct prerequisite
of a target, or direct descendant of studied/queued topics. It scores the strongest
reason as `purpose_points + 1000 × shortage + 100 × urgency_value`: lesson shortages
precede review shortages, assessment shortages, then hard/moderate/easy distinct-topic
assessment coverage, then advance preparation. Lessons need five total questions per
KP, reviews five across the topic, assessments one rated question across the topic.
Exactly five satisfies the lesson/review threshold.

The flat `knowledge_points` list deduplicates build candidates and excludes usable
registered generators. Full nested topic inventories remain available for coverage
and diagnostics, including per-KP refill deficits toward five of every difficulty.
The [finder guide](../scripts/README.md) defines the score components, exclusive
next-activity rules, distinct-topic coverage and cursor behavior. This finder does
not change the separate live inventory worker's trigger or ranking policy above.
