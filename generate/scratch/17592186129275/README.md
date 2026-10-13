# Off-center disk polar setups

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186129275.py --difficulty all --seed 42 --count 2 --format json
.venv/bin/python generate/scratch/17592186129275/validate.py
.venv/bin/python generate/scratch/17592186129275/check-concurrency.py
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and easy/moderate/hard wrappers. Explicit parameters are exactly `{"a":"3/2"}` (radius). Templates and scope are in classification.md; source replays and exact observed parameters are in source-cases.json. Default profile `setup` clarifies the requested actual-region/transformed-density criterion. Profile `observed` preserves the original wording with documented TeX presentation repairs. All45 source choice values are raw-exact; the two old widgets lack keys/solutions, and their derived keys/solutions and level assignments are explicitly authored.

Easy: four authored axis-oriented full disks with constant integrand, integer radius1–5. Moderate/hard: source families, integer/half-integer radius1/2–5. The finite meaningful task domain is20easy +30moderate +60hard =110. These are setup exercises, not scalar integral evaluation; the observed moderate banks include scalar-zero coincidences. Some source distractor intent, particularly compound xy2 bounds, is underdetermined; the exact visible operations are preserved without claiming original authoring recipes.

`validate.py` reads the actual displayed prompt/choices/solution mathematics independently, checks every circle expansion/factoring row and transformed-integrand stage, all complete source banks and shared solutions, supported radius domain, identity/shuffling and native radio grading. Fresh concurrent renderer checks are separate. Review originals and26 generated examples are in review.md/review.json. Rasters and their exact inputs/runtime provenance are in plots/; source and generated contact sheets document visual inspection. See validation.json and engine-report.json for exact counts. freeze.json pins script/evidence/asset/native-helper hashes after verification.

All records are local review JSON. No registration, transactions, engine changes, or database writes occur.
