# Triple integral change-of-variables setup

Current inventory version: `triple-setup-2`. Run `revalidate.py` for current
source classification and mathematical/native grading checks, then `replenish.py`
for locked, basis-guarded preparation, submission and exact readback. Current
evidence lives in `reference/replenishment/`; the earlier documents below retain
their basis-1356 historical scope. `validation-freeze.json` identifies version 2.

Supported levels are easy (exp/log/cos2/sin) and moderate (product/sqrt). Current
q-38941 rates the square-root family moderate, superseding its earlier authored
hard assignment. Hard emits no learner content and retains an explicit five-item
shortage. The seven newly captured banks have been classified; they are not
claimed as newly implemented generator profiles. Source records are preserved.

Frozen draft `triple-setup-1`, math basis1356. No database access, registration or writes.

Run validation:

```sh
.venv/bin/python generate/scratch/17592186198397/validate.py
```

Preview:

```sh
.venv/bin/python generate/scratch/17592186198397.py --difficulty all --count 2 --seed 42 --format markdown
.venv/bin/python generate/scratch/17592186198397.py --difficulty easy --template q-161880 --profile raw --format json
```

APIs: generate_easy, generate_moderate, generate_hard, and generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None). All fields are five-choice radio. Explicit parameters obey the same level guards as normal sampling. Raw evidence requires captured fixed height and common amplitude scale in[1,4]; integer/rational common amplitudes are supported. `source-cases.json` replays originals through this API. Normal profile is `method`; raw profiles preserve historical errors and omission of absent attributes.

The validator reconstructs mathematics from displayed TeX with a strict private parser, solves displayed coordinates independently, checks all9 partials and three cofactor minors, both determinant stages, reciprocal determinant, transformed integrand and final bounds. It rejects equal complete definite-integral values in whole-integral banks, even when displayed structures differ. Native grading uses the real learning::grade_field helper. Raw records lacking correct designations cannot enter that helper and remain documented omissions.

`review.md` and `review.json` contain all5 originals, changed-amplitude evidence versions, and two generated examples per supported family/level. See classification.md and template-extraction.md for source repairs and authored scope. This draft deliberately retains raw errors as ineligible evidence. Normal questions use supported repairs; no native grading limitations were found for the generated radio shape.
