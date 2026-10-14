# Tangent periodicity scratch generator

Frozen math basis 1356; no database writes. Generator: `../17592186176050.py`.

```sh
.venv/bin/python generate/scratch/17592186176050/validate.py
.venv/bin/python generate/scratch/17592186176050.py --difficulty all --seed 19 --count 2 --format json
.venv/bin/python generate/scratch/17592186176050.py --difficulty moderate --profile source_q-103307 --count 1
```

Public API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and `generate_easy`, `generate_moderate`, `generate_hard`. Parameters require exactly `v,a,b,n`; scalars may be exact SymPy-compatible strings. Only radio fields are supported. Explicit source profiles are parameterized evidence-only replays and preserve omitted source attributes. Normal output is completed, with separately labeled authored banks and levels.

`validate.py` reads actual prompt/answer/solution strings through an independent scalar and tangent-period parser, compares every source bank and source attribute presence, checks every displayed equality and required arithmetic stage, exercises rejected mutations, and runs the real native grader. `validation.json` separates fidelity, authored sampling and native grading. Raw originals missing correct refs remain ungraded evidence; no missing designation is reported as matched. `review.md`/`review.json` include every source bank and at least two normal variants per family and difficulty. `classification.md`, `template-extraction.md` and `variety.json` document scope and finite task counts.

