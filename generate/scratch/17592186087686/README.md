# Parallel slope-intercept generator

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186087686/validate.py
.venv/bin/python generate/scratch/17592186087686.py --difficulty all --count 2 --seed 12
.venv/bin/python generate/scratch/17592186087686.py --difficulty easy --profile raw_scalar_radio --format json
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and `generate_easy`, `generate_moderate`, `generate_hard`. Parameters are exactly `slope,b,k` as exact rational/integer strings. Templates: coefficient_blank, coefficient_radio, line_choice. Completed source profiles pair with raw profiles in source-cases.json. Raw profiles preserve unrated/missing solution/key/bank attributes and are evidence-only. Historical scalar profiles remain evidence-only even when completed; normal defaults use separately authored method banks.

Scope is reading/comparing visible x-coefficients in slope-intercept equations. Direct missing-coefficient responses equal the given slope immediately. No standard-form isolation, equation-solving parameter branch, points, or perpendicular tasks. All normal levels are authored integer / unit-fraction / reduced nonunit-rational number-form tiers; none is an observed rating. Coincident lines and ambiguous complete banks reject as whole instances.

`source.json` retains exact snapshot evidence. `classification.md`, `template-extraction.md`, `plot-extraction.md`, `source-cases.json`, `review.md`/`review.json`, `validation.json` and native `engine-input.json`/`engine-report.json` document coverage, completions, variants, full-bank checks and limitations. Runtime: Python3.13.5, SymPy1.14.0. No renderer or database writes.
