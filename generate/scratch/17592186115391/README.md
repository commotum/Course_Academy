# Scalar function multiple rule generator

Generator source capture: math basis 1356. The generator itself performs no database writes. `replenish.py` follows stages 8–9 through the application integration, serializes with `api.lock`, checks current inventory and identities, saves exact requests, uses a basis guard, and verifies additive requested-KP datoms at the receipt basis. Re-run it with `.venv/bin/python generate/scratch/17592186115391/replenish.py`; an existing saved request is recovered before new intent.

Run verification from repository root:

```sh
.venv/bin/python generate/scratch/17592186115391/validate.py
.venv/bin/python generate/scratch/17592186115391.py --difficulty all --seed 42 --count 2 --format json
```

`generate_easy`, `generate_moderate`, `generate_hard`, and `generate` support deterministic explicit parameters. Normal generation uses `authored_easy`, `authored_moderate`, or `authored_hard` with complete derived operation banks. To replay a source use its q-ID as template and `observed_q-ID` as profile, with `parameters={'scales':[1,1,1]}`. Observed profiles preserve unresolved original distractor patterns explicitly; they are evidence profiles and never selected by normal default generation. Mathematical fingerprints separate assessed-task identity from presentation UUIDs.

See classification for difficulty claims/bounds, extraction for every component and bank recipe, review for originals/variants, and validation for exact fidelity denominators. q32501's missing difficulty, solution and correct ref are repaired by independent differentiation and not counted as observed matches.
