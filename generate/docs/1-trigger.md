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
passes and generator completion, including startup and the scheduler's 30-second
cadence. In self-directed mode the finder captures the bounded Study lesson pool,
current activity needs, and maintenance inventory together at one database basis.
New lessons use targets and queue plus two reverse `topic/next` hops, L30+, and the
same below-band-one filter as Study. Prerequisite mastery and empty banks do not
remove these topics from generation demand. Ordinary new lessons outside that
scope do not create authoring demand.

There is no direct-selection completion gate in self-directed mode. Course mode
retains the existing gate: broader authoring waits until directly selected KPs
have usable hashed generators and five fresh questions in each difficulty band.
Approved refills remain independent. The durable cursor records the accepted
lineage and basis. The scan runs outside the learner API lock; starting a lesson
does not await generator work.

1. Pass the affected topics and activity types to Inventory.
2. If inventory is sufficient, no generation is needed. Otherwise, queue background generation for the shortages, reusing existing jobs for overlapping pools.
3. After generated questions are validated and committed, recheck inventory and continue any pending activity preparation automatically.

Recheck availability before starting an unstarted activity. Preserve already started or paused work; existing required-work rules still apply while generation runs.

The live worker and read-only `generate/scripts/find_candidates.py` share the
`study-scope-v6` comparator in `scripts/generator_priority.py`. They order work by:

1. Actual shortages for active, requested, or required remedial work.
2. Other actual lesson, review, or assessment shortages.
3. Distinct-topic assessment variety, in hard/moderate/easy order within relevance.
4. Advance builds and routine replenishment.

Within each urgency class, relevance and activity purpose refine the order. New
scoped roots and prerequisite lessons all have relevance tier 1, so early missing
lesson banks are not deferred behind their directly selected descendants. Lesson
shortages precede review and assessment shortages at the same relevance tier.
Current needs outside the lesson scope retain their activity demand; immediate
priority applies only to the matching shortage, not every future band in a topic.

Lesson work orders topics by global prerequisite layer, distinct selected goals
supported, engine priority, and age before comparing individual KP deficits. A
lesson's deficient KPs stay together. Reviews use due dates instead of graph
layers. Lessons need five usable fresh questions per KP, reviews five across the
topic, and assessments one rated question across the topic. Exactly five satisfies
the lesson/review threshold. Missing per-band reserves do not block another job
or give a stocked activity shortage priority.

The flat `knowledge_points` list deduplicates build candidates and excludes usable
registered generators. Full nested topic inventories remain available for coverage
and diagnostics, including per-KP refill deficits toward five of every difficulty.
The [finder guide](../scripts/README.md) defines the ordering, simultaneous activity
demands, distinct-topic coverage and cursor behavior. The service calls
it with `include_registered=true` so the independent refill worker also maintains
existing hashed generators outside the urgency groups. Those extra topics remain
ineligible for new generator creation. Refills run approved packages directly;
missing or stale approval defers the affected difficulty to the build worker for
review at its current priority, subject to the course-mode selection gate when
applicable. See the
[pipeline guide](../README.md) for recovery and storage details.
Uncertain publication recovery precedes ordinary work to reconcile its exact saved
request. Unfinished authoring and review drafts retain their workspace and resume
at their current priority.
