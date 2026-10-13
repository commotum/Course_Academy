# Identifying First-Order Linear ODEs

Scratch generator for KP 17592186087867; no database access or registration.

Run all fidelity, exact displayed-math, identity, and real engine checks:

```sh
.venv/bin/python generate/scratch/17592186087867/validate.py
.venv/bin/python generate/scratch/17592186087867.py --difficulty all --seed 42 --count 2 --format json
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and `generate_easy`, `generate_moderate`, `generate_hard`. Template/profile names are source IDs with underscores, e.g. `q_79754`. Only radio fields are supported. Parameters are integer `a,h` for the affine function `u=a*x+h`, with `0<|a|<=6`, `|h|<=8`. Explicit invalid parameters fail without resampling. Default samples `a` from ±1, ±2, ±3 and `h` from −4 through 4. Identity ignores seed and choice order; answer IDs are field-owned.

`source.json` preserves the immutable wrapper and basis. `source-cases.json` maps every original to a parameterized normal API replay. `review.md` contains all 12 originals and two generated variants of each bank. `review.json` contains the 24 generated review records. `validation.json` separates exact source fidelity from mathematical and native grading checks. `engine-input.json` and `engine-report.json` retain the actual real-engine evidence.

Authored extension: change the independent-variable functions through a common affine input. Difficulty stays attached to the observed bank's recognition demands. This does not claim to recover the original sampling code. Every complete observed bank remains eligible for default generation. Plot rating: none.

## Parent solution correction

q-79750’s original rationale says dependence on y prevents linearity, which is incomplete: a linear y term on the right can be collected. The generated sentence now specifies the nonlinear y² term. All12 source prompts,60 options and12 designations remain exact;11 supplied worked solutions remain byte-exact and one has this documented correction. Original evidence remains unchanged.
