# Scalar function multiple rule generator

Local scratch implementation; math basis 1356; no database writes. Stop at steps 3–7.

Run verification from repository root:

```sh
.venv/bin/python generate/scratch/17592186115391/validate.py
.venv/bin/python generate/scratch/17592186115391.py --difficulty all --seed 42 --count 2 --format json
```

`generate_easy`, `generate_moderate`, `generate_hard`, and `generate` support deterministic explicit parameters. Normal generation uses `authored_easy`, `authored_moderate`, or `authored_hard` with complete derived operation banks. To replay a source use its q-ID as template and `observed_q-ID` as profile, with `parameters={'scales':[1,1,1]}`. Observed profiles preserve unresolved original distractor patterns explicitly; they are evidence profiles and never selected by normal default generation. Mathematical fingerprints separate assessed-task identity from presentation UUIDs.

See classification for difficulty claims/bounds, extraction for every component and bank recipe, review for originals/variants, and validation for exact fidelity denominators. q32501's missing difficulty, solution and correct ref are repaired by independent differentiation and not counted as observed matches.
