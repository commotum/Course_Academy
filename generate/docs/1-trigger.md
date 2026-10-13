# 1. Trigger

Automatically call [Inventory](2-inventory.md) for a topic when:

- It is added to `:learner/queue`.
- It is added to `:learner/targets`.
- Its learner task enters `:learner-task.status/unlocked`.
- A review of it becomes due or is assigned, including remedial reviews.
- It is selected for an upcoming assessment.

Retakes use the same activity triggers and inventory requirements. Topic selection and eligibility must happen before filtering by question supply; an empty bank must still trigger inventory.

Use **event hooks** from the scheduler and committed database changes. Follow the most efficient [$edb](../../skills/edb/SKILL.md) practices: read relevant changes from the transaction log, retain the processing position across restarts, and batch checks for affected topics. Time-based review triggers come from the scheduler.

1. Pass the affected topics and activity types to Inventory.
2. If inventory is sufficient, no generation is needed. Otherwise, queue background generation for the shortages, reusing existing jobs for overlapping pools.
3. After generated questions are validated and committed, recheck inventory and continue any pending activity preparation automatically.

Recheck availability before starting an unstarted activity. Preserve already started or paused work; existing required-work rules still apply while generation runs.

`generate/scripts/find_candidates.py` returns a flat, ranked `knowledge_points`
list alongside the topic groups. Sort by earliest linked assignment deadline
(overdue first; undated last), then activity state (needed now, queued,
target-related, other unlocked), descending engine priority, and lowest total
available question count (`available_total`). Sum easy, moderate, and hard counts
at the applicable activity scope; a zero in one band does not get separate priority.
Targets and their supporting prerequisites inherit the earliest relevant deadline.
Remaining ties use the oldest known queue/target assertion or activity offer,
then stable entity IDs. Each KP reports its rank, deadline, priority, and counts.

Informational urgency labels remain P0 for an exhausted pool, P1 for an exhausted supported band, P2 below
the 3-easy/2-moderate/1-hard buffer, P3 below five per supported band, and P4 when
stocked; these labels do not determine ranking. Unclassified pools need classification. Lessons count per KP; reviews
and assessments count the topic pool. The five-question preparation minimums
remain in [Inventory](2-inventory.md). The script only reads and ranks candidates.
