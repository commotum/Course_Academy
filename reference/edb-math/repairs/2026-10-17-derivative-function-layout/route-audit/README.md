# Multipart route audit

Read-only audit of database `math`, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`, basis **3424**. The complete result is in `3424/summary.json`; raw fixed-basis queries and results are retained beside it.

- 121 multipart parents contain 665 descendants, traversing multipart steps and assigned-problem wrappers.
- 516 descendant questions belong to 327 KP practice pools (516 memberships).
- 76 ordinary lesson/review/assessment tasks are open: 43 locked, 26 unlocked, 7 paused, none started.
- No started or paused task has a future fixed multipart question in its route. Existing presentations of the three flagged derivative questions remain historical learner items.
- One never-started, locked review task (`17592186569173`, activity `17592186569158`, “Review: Introduction to Matrices”) reserves multipart question `17592186235398`. The new retrieval freshness policy must reject this old definition before new presentation. No active-route migration is required.

`audit.py 3424 --memberships` reproduces the full audit, reusing captured results. Omitting `--memberships` skips the optional global membership count. Initial broad membership queries timed out; the successful result uses bounded reverse-Pull batches.

No database facts were changed by this audit.
