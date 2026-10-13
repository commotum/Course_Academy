# Potential reconstruction generator

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186133879/validate.py
.venv/bin/python generate/scratch/17592186133879.py --difficulty all --seed 7 --count 2
.venv/bin/python generate/scratch/17592186133879.py --difficulty hard --template radial_log --profile observed_homogeneous --format json
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and `generate_easy`, `generate_moderate`, `generate_hard`. Explicit parameters are validated and never silently resampled. Parameters require all template keys plus integer `s`. Observed profiles fix the source relative coefficients/path and vary homogeneous scale `s∈{1,2,3}`. Authored generation varies independent relative coefficients and endpoint-bearing path parameters with `s=1` by default.

14 potential/path templates: two authored easy, six observed moderate, six observed hard. Normal output uses an authored complete bank of five operations; whole-instance collisions are rejected. Complete source banks remain available through explicit observed profiles. Original wrong-operation intent is underdetermined and is not claimed as recovered. The two documented source endpoint typos are repaired in generated solutions. `source-cases.json` retains originals with every field/answer; `review.md` and `review.json` show original replays and two authored examples per template. No plots or DB operations; work stops at step 7.

The validator independently reads displayed TeX, reconstructs a potential from the printed field, differentiates the displayed potential, evaluates the printed path/endpoints, verifies every printed numeric final row and every choice, compares complete source banks/designations/prose/stage counts, enforces workload bounds and identities, and submits every correct/wrong radio option to the real native grader with memory-only fixtures.
