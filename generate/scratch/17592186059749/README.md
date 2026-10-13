# Noninteger 2×2 determinants

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186059749/validate.py
.venv/bin/python generate/scratch/17592186059749.py --difficulty all --seed 42 --count 2 --format json
```

API: generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None), plus generate_easy/moderate/hard. Source replay inputs are in source-cases.json. Observed full banks are opt-in profiles; default radios use separately authored determinant operations. Explicit invalid workloads and whole-bank collisions fail without resampling. Random sampling rejects the whole invalid instance.

Review source provenance, exact prose/stage fidelity and full-bank mathematical fidelity separately in validation.json/review.md. q-1088's missing key, level and solution are inferred/authored separately. Hard is an authored four-fraction numerical arithmetic workload. Mathematical fingerprints exclude banks; content identities include actual display, fixed solution and complete bank. No EDB writes, registration, grading-engine edits, plot models or dependencies were installed.
