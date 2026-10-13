# Function-of-y scalar line integral evaluation

Scratch generator at math basis1356; no database writes, registrations or commits.

```sh
.venv/bin/python generate/scratch/17592186179718/validate.py
.venv/bin/python generate/scratch/17592186179718.py --difficulty all --seed 4 --count 2 --format json
.venv/bin/python generate/scratch/17592186179718.py --difficulty hard --template implicit_parabola --profile source:q-122271 --format markdown
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and individual `generate_easy`, `generate_moderate`, `generate_hard` entrypoints. Parameters are exact strings a,b,c,k; invalid explicit inputs fail rather than resample. Normal profile `method` serves every supported family. Source profiles are public, parameterized, opaque evidence replay and always ineligible. All six raw source banks/prompt strings and five present source solution sequences are checked; omitted raw difficulty/solution/designation attributes remain omitted. The unrated sqrt source's verified149/15 is not an observed designation.

Normal zero-endpoint defects are avoided by positive lower y in implicit-parabola and square-root families. Easy is authored straight-line evaluation; canonical log curves extend moderate; unrated sqrt is assigned authored hard. See extraction for workload bounds and complete bank definitions. `validation.json` separates raw fidelity, exact mathematics and native radio grading. `review.md` includes originals plus two normal examples of every family and endpoint variants of every observed profile. Plots are rendered by private Matplotlib code; source originals were visually inspected. Root independent QA follows this draft freeze.
