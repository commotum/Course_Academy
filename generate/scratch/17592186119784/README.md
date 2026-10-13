# Matrix statement generator

`../17592186119784.py` provides `generate_easy`, `generate_moderate`, `generate_hard` and `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)`. Local review data only; no EDB reads, writes, registration, engine changes or plots. Every question retains a single five-choice RADIO field.

```sh
.venv/bin/python generate/scratch/17592186119784.py --difficulty all --seed 19 --count 2 --format json
.venv/bin/python generate/scratch/17592186119784/validate.py
```

Profiles: `source-bank` for completed normal source variants; `source-replay` for parameterized faithful evidence, including raw attribute omissions and source prose errors; `authored-property-bank` for authored easy. Use source IDs as template names, or `direct-properties` for easy. Raw q-42115 uses a hard API routing argument while omitting its absent `:question/difficulty`; normal q-42115's hard/solution/correct reference are explicitly inferred.

Validation passed: 10 complete source banks / 50 choices, 9/9 present keys, 9/9 present solutions, exact omission parity for q-42115; 220 finite structural tasks (64 easy, 78 moderate, 78 hard), 468 signed boundary records, 239 native fixtures / 1,195 RADIO checks. The raw missing-key q-42115 cannot be graded as a fully specified source fixture; its normal inferred version is graded. Two source solution referent errors are preserved in raw evidence and corrected in normal records. Structural counts exclude numerical and presentation aliases.

Read `classification.md`, `template-extraction.md`, `source-cases.json`, `review.md`, and `validation.json`. `review.json` contains labeled raw originals and generated examples. The renderer-free plot evidence is in `plot-extraction.md`.

The earlier `replenish.py`, `capture_source.py`, `check-current-engine`, `current-engine-build.json`, and `reference/` are historical artifacts from the previous checkbox draft and are not used or endorsed by this RADIO generator. Current grading uses the shared `generate/runs/current/check-engine`; validation records its actual binary hash. Parent independent QA remains pending.
