# Local tangent-line generator

All files belong to KP17592186124454; no database writes or shared-engine changes. Basis1356 provenance is retained in `source.json`, classification and generator metadata.

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186124454/validate.py
.venv/bin/python generate/scratch/17592186124454.py --difficulty all --seed 11 --count 2
.venv/bin/python generate/scratch/17592186124454.py --difficulty easy --profile raw:q-37517 --format json
.venv/bin/python generate/scratch/17592186124454.py --difficulty easy --profile completed:q-36383
```

Public API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and three level entrypoints. Normal parameters are `a,b,c,p,q`. Complete banks are `method:regular`, `method:product` and `method:horizontal`. Raw/completed source profiles take `r,s` in 1..3 and use the extracted complete masks plus a diagonal coordinate pullback. Raw profiles preserve omitted ratings, correct refs and solutions. Completed profiles infer missing keys/stages and retain opaque banks; both have `evidence_only=true`, `eligible_for_learning=false`.

Source fidelity is separate from correctness. All seven prompts, 35 choices and five supplied complete solutions replay exactly. Three original banks have equivalent whole-line options. The real native radio grader checks stored designation, so its source-key behavior cannot establish mathematical uniqueness. Independent checks reconstruct actual prompt functions/points and all displayed formal derivative inputs, symbolic partials, component substitutions/reductions, gradient tuples, displacements and final complete line equations. Native checks test every owned ID of completed evidence and safe review records; no blanks exist.

The authored moderate/hard scope and finite reduced-number domains are documented in `classification.md` and the script. Sampling rejects an entire selected bank on ambiguity; explicit parameters raise rather than resample. Content identity includes prompt, fixed solution, complete displayed bank and correct designation; choice order/seed are excluded. Assessed-task fingerprints exclude unused constants, option-bank aliases and common polynomial scaling. `validation.json` reports finite-domain enumeration and honest historical ambiguity/interpretation limits. `review.md` and `review.json` show all originals, inferred completions, changed raw evidence, two safe variants per observed template and at least two authored variants at each missing level.
