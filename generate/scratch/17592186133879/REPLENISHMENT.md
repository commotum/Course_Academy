# Inventory replenishment

The frozen generator and its source evidence remain unchanged. `replenish.py`
adds stages 8 and 9 using the application's existing EDB integration and native
question pool and grader. Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186133879/replenish.py
```

The wrapper verifies frozen artifact hashes and the existing parent review,
acquires `.local/learning/requests/math/api.lock`, and rechecks the database
lineage, basis, source evidence, learner history, reservations and inventory.
It retains the lock through preparation, preview, basis-guarded submission and
exact-basis readback. Saved requests are recovered with their original key and
EDN before new intent is prepared. It uses `:application/ca-engine` attribution
and the installed question, field, answer and knowledge-point validation specs.

All three difficulty bands are supported by the frozen package. Easy is the
documented authored extension; moderate and hard use the extracted families.
Mathematical distinctness uses the simplified vector field and ordered endpoints,
independent of seed, identity, choice order and bank. Zero-result banks are
rejected whole. A bounded refill attempt leaves an explicit capability exception
and shortage if it cannot produce the requested reserve.

Source q-104747 and q-104764 contain the endpoint typos documented in
`template-extraction.md`. They remain unchanged in the database and are excluded
from validated inventory counts. Generated solutions use the corrected endpoints.
Canonical examples, previously shown and reserved questions are also excluded.

For job `2ab563fc`, basis 2514 had 0 easy, 6 moderate and 4 hard validated
questions available. Six distinct instances (5 easy, 1 hard) passed displayed
mathematics checks and all 30 native grading checks. The additive commit at basis
2515 registered generator `2a6bb8ac-5c52-5872-bb16-3a7edda9efd7` at
`generate/scratch/17592186133879.py`. Exact readback verified 5 easy, 6 moderate
and 5 hard available, with no remaining shortage. All 12 original questions,
the canonical example and learner history were preserved.

Requests, preview, receipt, generated JSON/Markdown, validation, inventory reads
and verification are retained under
`reference/generated/17592186133879/job-2ab563fc/basis-2514/`.
