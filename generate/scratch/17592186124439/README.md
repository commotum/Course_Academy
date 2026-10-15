# Tangent-vector generator

Validated generator for KP17592186124439. The frozen source evidence is from math basis 1356; current-source compatibility and replenishment were verified at basis 2692, with commit readback at basis 2693. The generator itself has no database side effects; `replenish.py` uses the existing integration for additive, application-attributed commits under `api.lock`.

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

## Inventory replenishment — 2026-10-15

Reused this package and generator version `tangent-vector-1`. No supplied `.generated` handoff existed. Current source questions were read at one basis, and `reference/replenishment/basis-2692/live-source-comparison.json` verifies that the only differences from the frozen source were repaired system braces and equation alignment. Original content and learner history were preserved. Two historical stale prose references remain excluded from usable counts, without editing them.

Rebuilt `reference/native/check-engine` against the deployed application engine library; build inputs and hashes are in `reference/native/build.json`. All 15 complete source banks replayed exactly against frozen evidence; the current grader accepted 285 correct selections and rejected 1140 incorrect selections with none unresolved. The ten submitted instances separately passed 10 correct and 40 incorrect selection checks.

The additive commit at **2692 → 2693** added **5 easy and 5 moderate** questions; independently validated fresh task counts are **5 easy, 5 moderate, 13 hard**. All supported-band shortages are zero. No capability exception was needed. The existing bounded domains remain 32 easy, 192 moderate and 127 hard method tasks; exhaustion must remain explicit on future requests.

Generator UUID: `1517b8a7-b8eb-5039-9dec-9ce81c5652e6`. Registered script: `generate/scratch/17592186124439.py`. Registration uses `question-generator/id`, `question-generator/script`, and the existing KP reference.

Exact EDN, durable request, native preview, confirmed receipt, source-aware datom checks, exact-basis readback, post-commit inventory and outcome are retained in `reference/replenishment/basis-2692/`. Repeated preparation produces no content changes. `replenish.py` first recovers a saved request under its original key before considering fresh intent.
