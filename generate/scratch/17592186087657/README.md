# Diameter endpoints circle generator

Frozen local generator: `../17592186087657.py`. Scope is constructing a full circle equation from two diameter endpoints; easy is authored, moderate/hard are source-grounded. No database registration or writes.

Verify from repository root:

```sh
.venv/bin/python generate/scratch/17592186087657/validate.py
.venv/bin/python generate/scratch/17592186087657.py --difficulty all --seed 4 --count 2 --format markdown
```

Raw source replay uses `generate(level, template=source_id, profile=source_id, parameters=...)`; source-cases.json lists every call. Missing original difficulty/solution/correct refs remain absent and evidence-only. Normal completion uses template `<level>_diameter` with an observed profile, or the default authored method bank. review.md and review.json label originals, generated level/template variants, correct options and radius-10 easy boundaries. validation.json separates complete-bank fidelity, present-key fidelity, independent printed arithmetic, raster geometry and native grading. Runtime asset dependencies and axes transforms are in plots/*.json.
