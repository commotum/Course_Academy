# 1. Trigger

Automatically call [Inventory](2-inventory.md) for a topic when:

- It is added to `:learner/queue`.
- It is added to `:learner/targets`.
- Its learner task enters `:learner-task.status/unlocked`.
- Its learner task is started or paused, including work outside the queue or targets.
- A review of it becomes due or is assigned, including remedial reviews.
- It is selected for an upcoming assessment.

Retakes use the same activity triggers and inventory requirements. Topic selection and eligibility must happen before filtering by question supply; an empty bank must still trigger inventory.

The running application coalesces refresh events after learner actions, scheduler
passes and generator completion. It also refreshes at startup and on the scheduler's
30-second cadence. The finder captures a consistent database snapshot and inspects
the full eligible pool, because distinct-topic assessment coverage is a global
calculation. The durable cursor records the accepted lineage and basis. This scan
runs outside the learner API lock; starting a lesson does not await generator work.

1. Pass the affected topics and activity types to Inventory.
2. If inventory is sufficient, no generation is needed. Otherwise, queue background generation for the shortages, reusing existing jobs for overlapping pools.
3. After generated questions are validated and committed, recheck inventory and continue any pending activity preparation automatically.

Recheck availability before starting an unstarted activity. Preserve already started or paused work; existing required-work rules still apply while generation runs.

The live worker uses the read-only `generate/scripts/find_candidates.py`
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
next-activity rules, distinct-topic coverage and cursor behavior. The service calls
it with `include_registered=true` so the independent refill worker also maintains
existing hashed generators outside the urgency groups. Those extra topics remain
ineligible for new generator creation. Refills run approved packages directly;
missing or stale approval sends the affected difficulty to the build worker for
review. See the [pipeline guide](../README.md) for recovery and storage details.
