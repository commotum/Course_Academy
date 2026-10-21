# Generator priorities deployed: relevance-v2

Historical deployment report. The later user correction requires completion of
all directly selected KP generators and question stock before prerequisite or
downstream work becomes eligible. See the
[current selection-gate report](../generator-priority-selection-gate-2026-10-17/summary.md).

The finder and durable build/refill workers now share one relevance-first comparator.
The running service accepted the new policy at EDB basis 3442. All 6,980 pending or
running build requests in the saved verification snapshot carry `relevance-v2`.

Ordering is lexicographic, so a larger numerical deficit cannot cross a relevance
or purpose boundary:

1. Required or active/requested activity needs.
2. Selected study: queue, targets, and unmet necessary prerequisites.
3. Other current activity needs.
4. Speculative preparation.

Within each tier, purpose orders lesson shortages, review shortages, assessment
shortages, hard/moderate/easy assessment coverage, then advance preparation and
routine replenishment. The old additive score remains diagnostic only.

Lesson topics sort by global prerequisite layer, distinct selected goals supported,
engine priority, waiting age, and topic ID before KP deficit and KP ID. The layer
uses the same engine function as the study queue. Support counts the distinct union
of queue and targets, including the topic itself when selected; multiple paths and
duplicate selections do not inflate it. Reviews use due dates instead of layers.

Explicit lesson demand is independent of imported mastery. A target without a
completed local lesson and an explicitly queued lesson both receive a lesson-supply
check, alongside existing review/assessment demands. Prerequisite traversal uses
the engine's current retention readiness, not historical lesson completion. An
overdue learned prerequisite receives selected review relevance; an unlearned
prerequisite receives selected lesson relevance. A ready prerequisite closes its
ancestor branch. Implicit future assessments remain speculative until a current
activity trigger establishes demand.

The six previously blocked lessons now have all 16 deficient KPs classified as
selected-study lesson shortages. The saved queue retains the earlier audit's total
deficit of 44 usable questions. Their positions at basis 3442 are:

| Topic | Display layer | Build priority positions |
| --- | ---: | ---: |
| Power Rule, 17592186049879 | L39 | 377–379 |
| Product Rule, 17592186050375 | L39 | 380–381 |
| Quotient Rule, 17592186050542 | L40 | 384–387 |
| Exponential Equations Using Logarithms, 17592186049053 | L40 | 388–390 |
| Combining the Laws of Logarithms, 17592186049195 | L41 | 392–394 |
| Equations Containing the Exponential Function, 17592186050649 | L41 | 397 |

They are ahead of speculative work, but not first overall: earlier selected-study
lesson shortages, including unmet prerequisites, precede them. The snapshot has
428 selected-study lesson-shortage build jobs. These positions reflect all current
selections, not just the original list of 53 topics. Positions can change with
selection changes, completed work, reservations, and new supply.

Unfinished drafts retain their workspace, cycle, and inputs while following their
current rank. Withdrawn demand pauses a draft without deleting it. Only pending or
uncertain publication receives a recovery override. A reason for a shared KP keeps
its own topic context; routine refills do not inherit another demand's immediate
tier. Build and refill lanes retain their shared KP locks and package approvals.

Validation passed: 137 engine tests, 15 native finder fixtures, 31 Python finder
tests, and 30 worker tests (213 total). Tests cover selected reviews outranking
speculative lessons, layer/support ordering before shortage size, independent
lesson/review demand, imported mastery and local completion, overdue prerequisites,
diamond support, shared-KP contexts, draft preservation, publication recovery, and
mixed legacy/current jobs.

The application restarted successfully and returned HTTP 200. The already-running
generator review (PID 731465) survived the restart and keeps its lane/KP locks until
completion. A temporary runtime service override preserved that work; the override
was removed and the original `KillMode=mixed` restored. Subsequent work uses the new
queue. [Deployment record](deployment.json).

Verification used saved queue files under a shared lock; it made no database reads
or queue writes. The service performed its normal background inventory refresh.
The existing learner-bound progress pull gained readiness fields; no new global
question query was added. Existing inventory validation/projection behavior for
multistep questions was outside this sorting change and remains unchanged.

[Saved queue evidence](queue-snapshot.json) · [Read-only queue inspection](inspect_queue.py)
· [Current policy guide](../../../generate/scripts/README.md)
· [Shared comparator](../../../scripts/generator_priority.py)
