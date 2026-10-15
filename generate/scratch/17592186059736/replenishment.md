The existing frozen `cross-determinants-1` generator was reused for the inventory
job ending `5be30f4b…eaecfd8f`. Its source capture was unchanged at preparation
basis 2599. The complete source replay passed again, and the fixture was also
recompiled against the application's current engine: 250 accepted and 286
rejected submissions, with no unresolved grading checks.

`replenish.py` acquired the application's `api.lock`, rechecked native inventory
and current/historical learner usage, and retained the lock through preview,
submission, exact-basis readback, and final inventory. The transaction used
`:application/ca-engine`, the deployed validation specs, and a basis guard.
Its exact request and confirmed receipt are under
`reference/replenishment/basis-2599/`.

Commit basis **2600** added five moderate and five hard questions and registered
generator UUID `18db453d-7a9f-5752-a71a-93a6324522bd` at
`generate/scratch/17592186059736.py`. The new questions use four existing
tuple/basis and radio/component-blank layouts. Their ordered vector operands
are mathematically distinct from the source bank, canonical example, and each
other; seeds, identities, notation, and choice ordering do not establish novelty.
Independent parsing checks every printed determinant and solution stage.
The current native grader passed all 30 accepted and 36 rejected submissions
for the ten new instances, including equivalent and incorrect blank entries.

The verified usable reserve is **24 easy, 5 moderate, 5 hard**, with no remaining
KP inventory jobs. Moderate and hard are the frozen package's explicitly
authored arithmetic workloads, rather than observed source ratings. No new
plots or assets were needed. All 27 source questions, the canonical example,
and learner history were preserved. The incomplete duplicate field in q-1405,
unrated q-1408, and malformed solution in q-282147 remain unchanged and are
excluded from usable counts. No supplied `.generated` file existed.

The retained result, exact transaction, preview, receipt, readback, source
exclusions, native grading reports, and dependency hashes are linked from
`reference/replenishment/basis-2599/outcome.json`. Re-executing `replenish.py`
recovers this same saved request and verifies its receipt before any new intent.
