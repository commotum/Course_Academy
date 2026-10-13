# Tangent-vector generator

Local review generator for KP17592186124439, math basis1356. Stop after guide step7; no registration, engine changes or DB writes.

```bash
.venv/bin/python generate/scratch/17592186124439.py --difficulty all --seed 42 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186124439.py --difficulty hard --template radical_x --seed 12 --format json
.venv/bin/python generate/scratch/17592186124439/build-evidence.py
.venv/bin/python generate/scratch/17592186124439/validate.py
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and `generate_easy`, `generate_moderate`, `generate_hard`. Only radio fields are supported, matching all originals. Easy template `constant` and moderate `scaled_coordinate` are authored; hard names are listed in classification.md. Hard `method` parameters are `c` (integer1..9) and `h` (integer-9..9). Authored parameters are `plane`, `a`, `x`, `y`, `z`; integer coefficient magnitude2..9, integer coordinates within±4, and moderate active coordinate magnitude≥2. Invalid explicit parameters fail without repair.

Public `source` profiles take `h` (vertical translation, -9..9), with `h=0` reproducing each exact original prompt, worked solution and bank. See source-cases.json. They are explicitly evidence-only and ineligible for learner use. The complete historical banks are opaque, have two redundant wrong-direction pairs, and source prose has two anchoring errors plus presentation anomalies. Normal `method` banks derive all five options from the tangent/normal construction and reject whole-instance direction collisions; m=0,±1 is ineligible for this bank.

Validation independently reads printed derivative, point, partial evaluation stages, point-slope rows, normals, determinant and concluding vectors. Mathematical eligibility means any nonzero vector parallel to the tangent, with no unit or orientation requirement. It checks all native radio options through the real grade_field engine:285 accepted and1140 rejected,0 unresolved. No typed-equivalent acceptance is claimed because a radio response is an answer selection.

Fidelity:15/15 prompts, raw solutions, complete banks and correct designations;75/75 values,60/60 distractors. Verified270 normal records plus15 originals,1425 choice-criterion checks and675 evaluation-stage checks. Finite meaningful task counts are32 easy,192 moderate and127 hard (height, held-coordinate aliases, seed/order and bank aliases excluded). Python3.13.5 and SymPy1.14.0. No assessed plot exists; the two lesson explanatory rasters were inspected full resolution, so no renderer/cache output applies.

Review.md has every original bank and at least two labeled variants per observed family, plus two examples each of the authored levels. Review.json contains all285 records. Classification, template-extraction, full source-bank-map, byte-audit and validation reports separate exact evidence, source errors, presentation normalization, mathematical correctness and grading.
