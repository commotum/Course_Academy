# Parametric table generator

Local script: `../17592186087717.py`. No database writes, registration or engine edits. All easy/moderate/hard methods are available through the shared API and CLI. Normal output uses independently sampled affine/quadratic/cubic functions; source templates accept exact `parameters={"k":1}` and their original complete profile.

```sh
.venv/bin/python generate/scratch/17592186087717.py --difficulty all --seed 42 --count 2 --format json
.venv/bin/python generate/scratch/17592186087717.py --difficulty easy --template q-69922 --profile observed-scalar-replay --seed 42
.venv/bin/python generate/scratch/17592186087717/validate.py
```

The validator checks every original, two parameterized variants per source, 30 normal instances per level, eligible source-shaped authored banks, explicit boundary failures, identity, displayed-expression readback, prose/stage fidelity and native grading. Native checks include canonical, genuinely unreduced equivalent blank entries and incorrect answers. `validation.json` reports exact counts separately from repairs and missing designations. `review.md`/`review.json` include every raw original and generated variants. Opaque source bank intentions and two absent original widgets remain acknowledged evidence limits; they are not hidden fidelity matches.
