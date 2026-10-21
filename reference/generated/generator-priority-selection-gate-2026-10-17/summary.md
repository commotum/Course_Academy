# Direct-selection completion gate: relevance-v4

Historical snapshot. [Relevance-v5](../generator-refill-scope-2026-10-17/summary.md)
supersedes the refill restriction below: approved automatic refills now run across
topics; the selection gate continues to restrict agent build and review work.

The live generator pipeline now excludes prerequisite, downstream, and other unselected work until every KP in the current queue or targets has a usable hashed generator package and at least five available easy, five moderate, and five hard questions. This applies to both build and refill workers. A rejected or failed attempt does not satisfy the gate.

Discovery reads only direct-selection inventories first. It expands to broader inventory only if that first snapshot is complete, and checks the gate again on the broader snapshot. Changed selections or consumed stock can close it again. Saved outside drafts are withdrawn with their workspaces and cycles retained. Pending publication reconciliation is the only exception.

Within admitted work, the relevance-first topic ordering remains: actual immediate demand, direct queue/targets, prerequisite preparation, other current work, and speculative preparation. Topic layer and support cannot cross these boundaries.

Live verification at basis 3480: **202 selected topics, 633 distinct KPs, zero unselected runnable jobs**. The selection gate is closed. 602 KPs lack a usable hashed package and 441 lack the full difficulty-band reserve; these sets overlap.

All 16 arithmetic-prerequisite jobs listed previously are withdrawn. The old unrelated job for KP17592186152211 was paused at its validation stage after confirming no publication request existed. Its draft, evidence, attempt3, and cycle1 remain intact. The selected build for KP17592186129110 (The Power of Product Rule for Exponents) is running and survived deployment.

The updated service returned HTTP200. Verification covered both worker lanes using saved queue metadata under a shared lock; it did not run a broad database query. Two bounded title/membership queries read only the next14 KPs and their five topics, confirming that every listed topic is directly selected.

Validation: **101 focused tests passed** (17native finder,46Python finder,38worker). These cover the admission gate, missing generators, legacy packages, missing difficulty bands, deduplicated/shared KPs, selected-first discovery, snapshot races, both lanes, draft preservation, and exact publication recovery.

## Current leading build jobs

**The Power of Product Rule for Exponents** (`17592186049861`)

- 1. Applying the Power of Product Rule (`17592186129110`)
- 2. Applying the Power of Product Rule to Expressions with Fractions (`17592186129111`)
- 3. Applying the Power of Product Rule to Expressions with Negative Numbers (`17592186129112`)

**The Power of Quotient Rule for Exponents** (`17592186048683`)

- 4. Applying the Power of Quotient Rule (`17592186105742`)
- 5. Evaluating Powers of Negative Fractions Using the Power of Quotient Rule (`17592186105744`)

**Powers of Negative One** (`17592186049823`)

- 6. Raising an Integer to the Power of Negative One (`17592186078574`)
- 7. Raising a Fraction to the Power of Negative One (`17592186078576`)
- 8. Raising a Negative Integer to the Power of Negative One (`17592186078575`)

**Negative Exponents** (`17592186050495`)

- 9. Raising an Integer to a Negative Power (`17592186176090`)
- 10. Raising a Fraction to a Negative Power (`17592186176091`)
- 11. Expressing a Fraction as a Power With a Negative Exponent (`17592186176092`)

**The Product Rule for Radicals** (`17592186049923`)

- 12. Writing a Product of Two Square Roots as a Single Square Root (`17592186124482`)
- 13. The Product Rule With Cube Roots (`17592186124483`)
- 14. Separating a Square Root Into a Product of Two Square Roots (`17592186124481`)

The first job is already running. Queue positions may change as selected work completes or the learner changes selections.

[Queue evidence](queue-snapshot.json) · [Bounded title and membership evidence](next-titles.json) · [Deployment](deployment.json) · [Paused draft](paused-unselected-job.json) · [Current policy](../../../generate/scripts/README.md)
