# Negative linear term completion generator

Local draft only; source is math basis1356. No database or engine changes.

```sh
.venv/bin/python generate/scratch/17592186068876/validate.py
.venv/bin/python generate/scratch/17592186068876.py --difficulty all --seed 42 --count 2
.venv/bin/python generate/scratch/17592186068876.py --difficulty easy --profile source:q-141611 --format json
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and individual level entrypoints. Families: easy `direct`, `fragment`; moderate/hard `pq_plus`, `pq_minus`. Plain and enum field selectors radio/blank work. `authored_method` is normal generation; `source:<id>` exposes faithful parameterized evidence with raw omissions and is always marked evidence-only/ineligible. Explicit input is validated, never resampled. Historical opaque-bank scalar parameters are available only in evidence profiles, never defaults.

For `parameters`, supply integer `h` (positive half-coefficient), integer `c` (constant), and variable `v` in x/y/z. Easy: h1..12,c1..144, c≠h². Moderate: h1..12,c0..144,c≠h². Hard: h3..12,c−60..−1. Radio h1 causes the unsquared-correction recipe to collide and rejects the complete instance; blanks support h1. Normal binomial blanks specify positive leading variable coefficient. This avoids the raw source's sign ambiguity, while faithful raw records retain original wording.

Validation reads displayed equations/stages, checks all original choice values and optional-attribute presence separately from correctness, rejects C0 bytes and equal-but-collapsed teaching stages, checks identity semantics and native grading. Raw anomalies remain raw; inferred completed versions are separate review artifacts. Three missing designations and opaque historical distractor intention are documented limitations, not passed comparisons. Validation reports exact Python/SymPy versions and grader binary hash.
