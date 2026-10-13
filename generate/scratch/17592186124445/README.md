# Finding the Points Where a Gradient Vanishes

Local steps 3–7 draft only. All eight practice sources replay publicly with exact prompt, complete solution and complete five-choice bank strings. Raw profiles preserve known source errors and are evidence-only. Normal output minimally corrects those errors and uses complete method banks where historical error intent is opaque. No database writes or registration.

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186124445/validate.py
.venv/bin/python generate/scratch/17592186124445.py --difficulty all --count 2 --seed 7 --format markdown
.venv/bin/python generate/scratch/17592186124445.py --difficulty moderate --template quadratic --profile raw_quadratic --format json
```

The API offers `generate_easy`, `generate_moderate`, `generate_hard`, and `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)`. Exact source inputs are in `source-cases.json`. `method_<template>` are normal profiles; `raw_<template>` are parameterized public evidence profiles. Only radio is supported because every captured practice field is radio. Invalid explicit parameters fail; sampling rejects the entire colliding bank. Seeds shuffle options deterministically but do not alter content identities for fixed parameters.

`review.md` shows every exact source with full bank/solution and two normal variants for every family, including authored easy. `validation.json` separates source fidelity, exact mathematics, finite meaningful task counts and native radio grading. Native checks invoke the real application grading fixture, without database transactions. No plots are assessed or generated; no image renderer is required. Actual Python and SymPy versions and native executable hash are recorded.
