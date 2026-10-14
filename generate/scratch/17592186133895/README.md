# Unit curl recognition scratch generator

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186133895.py --difficulty all --seed 17 --count 2
.venv/bin/python generate/scratch/17592186133895/validate.py
```

API: generate_easy, generate_moderate, generate_hard, and generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None). Replay each source with source-cases.json, its observed level, exact parameters and `profile="raw"`. Raw anchors retain all captured fields and ref omissions; they are evidence-only. Normal output uses one active radio field. Seven observed families (two easy, five moderate), one explicitly authored hard family; every component is smooth on R². No plots, database writes, engine edits or registration.

Validator reads actual displayed fields, partials, every grouped/distributed/collected curl stage and concluding selection with independent exact mathematics. It checks complete subset banks, fidelity/key-presence separately, all default families, guards, stable identities, formatting mutations and actual native engine choices. The two raw legacy fields without correct references cannot be graded; their absence is recorded and never counted as a matched designation.
