# Inventory replenishment

Completed for KP 17592186087768 at math lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`.
The original frozen generator and its evidence remain byte-for-byte unchanged.
The original README describes its earlier steps 3–7 freeze; this record covers
subsequent database preparation and commit.

At basis 2643 the native pool had 0 easy, 6 moderate, and 0 hard available
questions. The existing six moderate sources passed independent mathematical
and actual learner grading checks. The seventh source, q-72616, remains
unrated and incomplete, is preserved, and is excluded from inventory.

Five easy and five hard instances from the frozen generator were validated,
visually reviewed, and published through the existing content-addressed image
store. Each has a different exact circle equation from every source, canonical
example, and other selected question. The easy and hard assignments are the
explicit same-method authored extensions in classification.md; they do not
claim source-observed difficulty labels. Their parameter scopes are in
capabilities.json. No source or learner records were revised.

Generator UUID: `78cff98a-9f06-5652-9413-1df86fa11866`.
Script: `generate/scratch/17592186087768.py`.
The UUID and script were registered through the existing generator reference.

`replenish.py prepare` uses the existing database integration, the native
inventory/pool reader, and the actual learner grader. `replenish.py commit`
acquires the application's `api.lock`, recovers saved requests before new
intent, rechecks the inventory and basis, previews with deployed native
validation specs, persists the exact request, submits with a basis guard,
and verifies exact readback before releasing the lock.

The verified commit advanced basis 2643 → 2644 and left available inventory
at **5 easy, 6 moderate, 5 hard**, with no remaining job for this KP.
All seven original questions and the canonical example are unchanged.
Receipt datoms contain only additions for this KP's generated content and
registration, attributed to `:application/ca-engine`; no learner facts changed.
Repeated preparation produces no additional content changes.

Evidence: `reference/replenishment/basis-2643/` contains the original records,
counts, generated records, assets, visual review, native grading, preview,
exact EDN/request key, verified receipt, readback, and outcome. The required
job `.result` contains the same outcome and links to these artifacts.
