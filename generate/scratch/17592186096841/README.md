# Polynomial-power generator draft

Run the full validation:

```sh
.venv/bin/python generate/scratch/17592186096841/validate.py
```

Preview every level:

```sh
.venv/bin/python generate/scratch/17592186096841.py --difficulty all --seed 20 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186096841.py --difficulty hard --profile observed_48666 --count 2 --format json
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and `generate_easy`, `generate_moderate`, `generate_hard`. JSON contains local records with field-owned UUID strings and lookup references; it is never an EDB transaction. Explicit invalid parameters raise an error. Whole-bank collisions reject the complete instance; random sampling retries, explicit replay never changes its inputs.

Coverage: 9/9 practice questions, 4/4 five-option radio banks, 5/5 blank layouts, 25/25 values, 16/16 distractors, 8/8 available correct designations. q-48625 lacks an original designation and solution and is unrated; its moderate assignment, correct designation, and solution are documented repairs, not recovered source labels.

All levels are observed. Easy affine differentiation, moderate polynomial differentiation/slope, and hard affine-power tangent equations use exact bounded integers. Easy symbolic powers span2–6; moderate affine slopes use power4; hard tangent powers span3–4. Sampled point questions require1≤|P(z)|≤3 and nonzero P′(z), with small signed points/coefficients. Explicit source inputs remain unchanged. No radicals, logarithms, exponentials, or unrelated composite-function branches. Original prose/placeholder layouts and equation-stage purposes are preserved while mathematical notation is normalized. Observed uncertain distractor banks are explicit profiles; default banks use differentiation operations.

Validation independently parses displayed prompts, every answer, generated chain/slope/tangent stages, and original mathematical solution stages. Native engine checks canonical/equivalent blank entries and wrong entries, and all radio selections. Stable content identity excludes seed/order; altered banks change identity. Review records and source cases live beside this README. No database writes. Parent QA is still required before approval.
