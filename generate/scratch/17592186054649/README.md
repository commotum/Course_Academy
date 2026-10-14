# Subtracting Matrices generator

Registered script: `generate/scratch/17592186054649.py`. Generator UUID: `aff755f8-ae78-5cc7-8a60-ab39066d5b21`. Supports easy only; moderate/hard capability exceptions are in `capabilities.json`.

Run from the repository root:

```sh
python3 generate/scratch/17592186054649.py --difficulty easy --count 5 --seed 2073 --format json
.venv/bin/python generate/scratch/17592186054649/validate.py
.venv/bin/python generate/scratch/17592186054649/replenish.py
```

The script uses the existing repository virtual environment for SymPy if the system interpreter lacks it. JSON output uses the application question/field/answer representation. Every generated question still requires live inventory deduplication, validation and preparation before persistence. The commit runner serializes with the application lock and recovers exact saved receipts before new intent.

Seven templates, four complete radio profiles and three blank layouts are documented in `template-extraction.md`. All 38 original answer values (16 distractors) replay exactly; all available prompts, keys and worked solutions replay exactly. Missing source key/solution/rating evidence is explicitly authored for new output, with originals untouched. Actual native grading passed 3,892 validation checks plus 92 final preview checks.

At basis 2201 the locked inventory had five fresh easy questions. Only generator registration was needed: three explicit domain assertions and the automatic transaction instant. Commit basis 2202 verified generator registration, all seven unchanged source practice questions, unchanged canonical example and zero learner/engine changes. Exact request, preview, receipt, readback and frozen package are under `reference/replenishment/basis-2201/`. Moderate/hard each retain an explicit unfilled reserve of five; two unrated originals remain excluded from inventory.
