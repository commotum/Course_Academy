# Direct polar-to-Cartesian generator

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186092217/validate.py
.venv/bin/python generate/scratch/17592186092217.py --difficulty all --seed 42 --count 2 --format json
```

Public API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and `generate_easy`, `generate_moderate`, `generate_hard`. Parameters are exact strings `radius`, `angle`, `unit`; for radians, `angle` is the coefficient of pi, e.g. `7/6`. Explicit inputs receive the same workload/unit/angle/bank guards as samplers. Raw replay requires explicit parameters and a matching `raw-q-...` profile; the complete `source-cases.json` gives every invocation. Raw profiles are ineligible evidence, including two omitted-correct/rating/solution records. Authored normal banks and missing-level bounds are identified in metadata and extraction. CLI normal output never selects opaque evidence.

`source.json` is the unchanged basis-1356 wrapper; `recipes.json` contains complete prompt/solution component masks and field layouts, no answer lookup table. `prepare.py` documents reproducible extraction. `review.md` / `review.json` show all seven originals and two variants per supported family at every offered level. `validation.json`, `engine-input.json`, and `engine-report.json` separate exact fidelity, mathematics, scope, formatting, identity, and real native grading. `plot-extraction.md` records why steps 5 and 7 require no plots.

No database operations, shared edits, registration, or engine changes. Freeze hashes are in validation.json. Parent independent QA is still required.

## Inventory replenishment

`replenish.py` reuses this validated generator and the configured application EDB integration. Run `.venv/bin/python generate/scratch/17592186092217/replenish.py` from the repository root. Unlike the generator and validator above, this helper submits additive content transactions. It acquires `.local/learning/requests/math/api.lock`, rechecks inventory, validates current gradable source questions and new tasks with the current native grader, registers or reuses the generator UUID, previews native validation specs, retains the exact request with a basis guard, and verifies receipt/readback before releasing the lock. Existing sources, canonical example and learner history are preserved.

`capabilities.json` records supported workloads and bounded domains. Two incomplete legacy questions remain excluded rather than acquiring invented captured answers. Replenishment evidence lives in `reference/replenishment/basis-*/`, including complete EDN requests, receipts, generated JSON, native grading, and exact-basis verification. The original basis-1356 source wrapper is retained unchanged; current source evidence must still match before submission. `reference/native-build.json` identifies the current release grader used for the replenishment fixtures.
