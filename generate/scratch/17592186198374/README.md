# Inferred integrand transformation generator

`../17592186198374.py` generates easy, moderate and hard local review records. Frozen basis1356; no database writes or registrations. All five observed hard families are served by normal default sampling. Easy and moderate are explicitly authored scope extensions anchored to the canonical example/unrated question and owning lesson route.

Run from repository root:

```bash
.venv/bin/python generate/scratch/17592186198374/validate.py
.venv/bin/python generate/scratch/17592186198374/supplemental_validate.py
.venv/bin/python generate/scratch/17592186198374.py --difficulty all --seed 10 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186198374.py --difficulty hard --template rational --profile raw:q-160433 --format json
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and separately documented `generate_easy`, `generate_moderate`, `generate_hard`. Normal profile `method`; explicit raw profiles `raw:q-...` accept `{'scale':1..3}` only, replay through the same public API and are always evidence-only/ineligible. Raw replay retains attribute omissions, duplicate legacy fields and all historical scalar choices; opaque intent is not presented as recovered recipes. Unit scale matches all existing source prompt/solution strings and all 35 option values. Missing source correct refs are never counted as matched.

Normal exact inputs use `matrix=[a,b,c,d]`, `shift=[h,k]`, `bounds=[u0,u1,v0,v1]`, optional `scale=1..3`. Explicit inputs are guarded and never silently resampled. Matplotlib assets/sidecars stay in this folder. Choices are whole preselected operation profiles, reject the entire instance if ambiguous, and shuffle deterministically. One fixed solution retains the five source steps and prose, adds explicit affine inverse formulas and evaluated signed components at both primitive endpoints. source-cases.json, review.md/review.json and validation.json separate original evidence fidelity, authored normal mathematics and real native grading.

Original PNGs are copied at their preserved relative references under images/ so the raw-source review renders locally. Full-row mathematics can hide compensating primitive errors; supplemental_validate.py deliberately constructs that case and requires the per-factor primitive checks to reject it.
