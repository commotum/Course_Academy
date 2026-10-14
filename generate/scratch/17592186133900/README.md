# Advanced Green’s theorem generator

Draft at math basis 1356. No registration, engine edits or database writes.

```sh
.venv/bin/python generate/scratch/17592186133900.py --difficulty all --seed 7 --count 2 --format json
.venv/bin/python generate/scratch/17592186133900/validate.py
```

API: generate_easy / generate_moderate / generate_hard and generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None).

Every source has a public `raw:<source-id>` profile with `parameters={"amplitude":1}` (integer amplitude up to |3|). It preserves original duplicate fields, missing designation presence and source errors; evidence only. Normal profiles are radial, angular, blank and outer_minus_hole. Invalid explicit parameters or complete-bank collisions raise ValueError. All levels supported; easy is authored supplied-curl scope. See extraction for full original banks, corrections, operative solution masks, arithmetic bounds and identity rules. Native source fixtures omit only a legacy field without any correct designation; raw replay preserves it. Steps 8–9 are intentionally unperformed.
