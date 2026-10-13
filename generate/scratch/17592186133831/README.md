# Frozen setup-only generator

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186133831/variety.py
.venv/bin/python generate/scratch/17592186133831/validate.py
.venv/bin/python generate/scratch/17592186133831.py --difficulty all --seed 4 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186133831.py --difficulty easy --template shifted_circle --profile observed_shifted_circle --format json
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and all three named difficulty entrypoints. Only the observed radio field layout is supported. Explicit inputs never silently resample. Normal complete-bank collisions raise `ValueError`; random generation rejects the whole instance. Unexpected parser/CAS failures propagate.

Five source easy families are public under `observed_*` profiles with genuine field-scale and upper-endpoint parameters. Raw evidence is always ineligible. The authored defaults cover all five families with method-derived banks. Moderate and hard are missing-level authored extensions grounded in the polynomial canonical example and observed spiral respectively. No learner question asks for evaluation or changes the vector line-integral method.

`source.json` is immutable captured evidence. `source-cases.json`, `bank-map.json`, `review.json` and `review.md` contain exhaustive raw replays and clearly labeled authored variants. `validation.json` separates source fidelity, known raw anomalies, normal mathematics and native grading. The real engine checks all five radio UUID submissions per reviewed record. The sources provide no typed blank interface; equivalent free mathematical entries are not supported submissions for these radio fields, so no blank-equivalence claims are made. Grader acceptance does not establish mathematical uniqueness; the independent parser and exact algebra tests do that.

No assessment plots are present, so step 7 requires no renderer. Python and SymPy versions and the native engine hash are recorded. No database calls, shared-file changes, registration or commits are performed. Frozen for parent QA after step 7.
