# Private chain-rule draft

The registered generator and its evidence remain unchanged. This separate draft uses the frozen math database read at basis 2275. No database, engine or registration changes are included.

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python generate/scratch/17592186096742-draft.py --difficulty all --count 1 --format json
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python generate/scratch/17592186096742-draft/validate.py
```

The API is `generate(level, seed=0, template=None, parameters=None, profile=None, field_type=None)`. `observed_raw` replays original source evidence, including absent grades, solutions, keys and fields, and is ineligible for learning. Source cases are listed in source-cases.json. `source-bank` and `source-blank` preserve the corresponding response contracts. The normal `q-28655` template requires explicit `source-compatibility` and original base 5.

All normal parameter combinations were independently read from their rendered math and tested through the actual native grader. The eligible capacity is 60 easy, 117 moderate and 97 hard tasks, including the one fixed compatibility task. Easy source grades were absent; their easy ratings are tentative authored assignments.

The radical-numerator blank serves shifts 1 through 24 only. The wider raw shift range demonstrates the native grading gap outside these bounds. raw-exclusion-grading.json preserves the unresolved ordinary wrong entry, while native-grading.json has no unresolved served checks. The fieldless MA question is raw-only. Raw base variants of the exponential/log source are evidence, not extra serving capacity; this narrower sampling choice makes no general claim about constant-answer practice.

Source fidelity, interpreted bank recipes, sampling limits, source errors and step-by-step review are recorded separately in source-components.json, classification.md, template-extraction.md, source-replay.json and review.md. Captured non-MA inventory records remain exact and separate from authored previews. registered-baseline.json records the original entire path set and byte hashes; freeze.json records the draft and its dependencies for parent review.
