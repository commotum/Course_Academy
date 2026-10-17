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

The live worker and read-only `generate/scripts/find_candidates.py` share the
`relevance-v2` comparator in `scripts/generator_priority.py`. They order work by
relevance first: required or active activity needs, selected study (queue, targets,
and their unmet necessary prerequisites), other current review/assessment needs,
then speculative preparation. Within each group, lesson shortages precede review
shortages, assessment shortages, hard/moderate/easy distinct-topic assessment
coverage, and advance preparation or routine replenishment. A selected review
shortage therefore precedes a speculative lesson shortage regardless of size.

Lesson work orders topics by global prerequisite layer, distinct selected goals
supported, engine priority, and age before comparing individual KP deficits.
Review work uses due dates instead of prerequisite layers. Selected lesson demand
is independent of imported mastery: targets without a completed local lesson and
explicitly queued lessons are checked even when the inferred next activity is a
review. Lessons need five usable fresh questions per KP, reviews five across the
topic, and assessments one rated question across the topic. Exactly five satisfies
the lesson/review threshold; a complete bank receives no shortage priority.

The flat `knowledge_points` list deduplicates build candidates and excludes usable
registered generators. Full nested topic inventories remain available for coverage
and diagnostics, including per-KP refill deficits toward five of every difficulty.
The [finder guide](../scripts/README.md) defines the ordering, simultaneous activity
demands, distinct-topic coverage and cursor behavior. The service calls
it with `include_registered=true` so the independent refill worker also maintains
existing hashed generators outside the urgency groups. Those extra topics remain
ineligible for new generator creation. Refills run approved packages directly;
missing or stale approval sends the affected difficulty to the build worker for
review. See the [pipeline guide](../README.md) for recovery and storage details.
Uncertain publication recovery precedes ordinary work to reconcile its exact saved
request. Unfinished authoring and review drafts retain their workspace and resume
at their current priority.
