# Parametric coordinate ranges

Generator: `../17592186087722.py`. Requires the project `.venv` and existing shared native grader. The additive inventory worker `replenish.py` registers the validated script and saves exact requests, receipts, and readback under `reference/replenishment/`. It holds the application's `api.lock` from the fresh inventory read through durable submission and verification.

```sh
.venv/bin/python generate/scratch/17592186087722/validate.py
.venv/bin/python generate/scratch/17592186087722.py --difficulty all --seed 21 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186087722.py --difficulty moderate --template q-16199 --profile observed:q-16199 --format json
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and the three level wrappers. Observed recipes accept `sx,sy` positive integers 1..6. Source cases use unit scales; source profiles transport complete source banks. Authored endpoint banks are the normal radio default. Explicit invalid inputs fail without replacement.

See classification.md for authored level scope, template-extraction.md for complete prompt/field/bank/solution extraction, and review.md/review.json for all original replays, variants of every observed bank, and all three levels. validation.json separates observed matches from missing-field/designation repairs; engine-validation.json reports real application grading.

Remaining evidence limits: q-16203/q-16205 lack observed correct refs/rating/solution, and q-73604's original assessment widget is absent locally. Their supported authored fields/designations are clearly marked. Opaque source distractor bounds are preserved as complete coordinate-transport profiles and carry no claim of recovered error intentions.

`capabilities.json` records the supported levels, bounded parameters, and source exceptions. Original source questions remain unchanged; incomplete and unrated sources do not contribute to usable inventory. `registration.json` retains the stable generator UUID and repository-relative script path. Replenishment deduplicates the simplified assessed coordinate expressions and their common admissible parameter domain against the whole existing bank and canonical example, independently of seeds, UUIDs, and choice order.
