# Cartesian flux setup generator

The generator performs steps 3–7 without database writes. Use:

```sh
.venv/bin/python generate/scratch/17592186198389.py --difficulty all --seed 42 --count 2 --format json
.venv/bin/python generate/scratch/17592186198389.py --difficulty easy --template q-161359 --profile q-161359 --count 2
.venv/bin/python generate/scratch/17592186198389/validate.py
```

API: generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None), plus generate_easy/moderate/hard with the same optional arguments. JSON uses existing leading-colon attributes, enum strings, field-owned UUIDs and lookup refs; it is review data, not transaction data. Source profiles preserve all original banks; normal banks are authored operations. Moderate/hard are authored bounded concrete setup variants. See classification.md for level workload bounds, extraction for source repairs and expression-pattern intent limits, validation.json for separate fidelity/correctness/grading counts, and review.md/review.json for originals and variants.

`replenish.py` performs the authorized steps 8–9 using the existing EDB integration,
application contributor, basis guard and application `api.lock`. It retains the
exact request and reconciles its receipt before preparing further writes. The
registered identity is in `registration.json`; do not replace it.

Replenishment at basis 2541 committed ten distinct questions at basis 2542
(five moderate, five hard). Exact-basis readback confirmed 11 valid unseen easy,
five moderate and five hard questions, with all 12 sources and learner history
preserved. The q-161471 source solution error remains unchanged and excluded
from validated inventory. See `reference/replenishment/basis-2541/outcome.json`
and `verification.json`. The full source replay passed again, and the current
application grader accepted 67 correct choices and rejected 268 distractors;
`reference/native/full-grading.json` records that check.
