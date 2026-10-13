# Orthogonal vector-sum normalization

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186096815/validate.py
.venv/bin/python generate/scratch/17592186096815.py --difficulty all --seed 42 --count 2 --format json
```

The API exposes easy/moderate/hard and public raw/inferred evidence profiles. Explicit replay calls are recorded in `source-cases.json`. Two unrated sources replay complete banks, with absent correct refs/solutions/ratings retained in raw profiles. Inferred evidence profiles supply a supported correct ref only; the opaque banks remain ineligible for learning. Authored method banks provide all three levels. No database writes, plots, new component-form branch, or source-difficulty claims.

`validate.py` checks printed directions, magnitudes, every bank value, every solution stage, source fidelity/omissions, scope guards, content/task identities, formatting, and native grading. Raw records cannot be graded until the missing correct designation is supplied; the report separates original omissions from authored inferred fixtures. `review.md` and `review.json` contain originals, changed-parameter evidence profiles, and at least two authored records per level.
