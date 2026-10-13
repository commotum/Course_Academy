# Triple integral change-of-variables setup

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
