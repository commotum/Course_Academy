# Writing first-order linear ODEs in standard form

Validated generator: `generate/scratch/17592186087866.py`. Observed bands: easy and hard. Moderate generation fails explicitly. The CLI uses the repository virtual environment when invoked by a system Python without SymPy.

```sh
python3 generate/scratch/17592186087866.py --difficulty hard --count 5 --seed 19 --format json
.venv/bin/python generate/scratch/17592186087866/validate.py
.venv/bin/python generate/scratch/17592186087866/replenish.py
```

Explicit source replay uses `--template SOURCE_ID --parameters JSON`. Original parameter shapes are in `source-cases.json`; the complete selected profile is the template's source ID. There are eight easy templates and one hard template. All source banks are replayed as full mathematical equations, with source field errors excluded explicitly. SymPy normalizes typography; byte-identical source notation is not claimed.

`classification.md`, `template-extraction.md/json`, `plot-extraction.md`, `review.md`, `validation.json`, and `capabilities.json` separate source observations, recipe hypotheses, mathematical validation, actual application grading and bounded exceptions. Hard has 90 distinct normalized tasks in its frozen parameter domain; easy has 526. These counts exclude seed/choice/identity/dependent-scale aliases and precede source/canonical/learner-history exclusions. Each replenishment rechecks the actual database before selecting new tasks.

`replenish.py` uses the existing EDB integration and configured application contributor. It acquires `.local/learning/requests/math/api.lock` before basis/inventory reads and holds it through preview, basis-guarded submission, exact-basis readback and post-commit inventory. Each durable request and receipt stays in `replenishment/basis-N/`. Recovery uses the original request key and exact EDN. Datom checks permit only additive content in this KP and its generator registration, preserving all originals and learner history.
