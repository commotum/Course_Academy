# Derivative units generator

```sh
.venv/bin/python generate/scratch/17592186064271/validate.py
.venv/bin/python generate/scratch/17592186064271.py --difficulty all --count 2 --seed 24 --format json
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and the three level entrypoints. Unit-interpretation only; no differentiation or numeric conversions. JSON is local review data. No DB operations. Plot rating none.

`source-cases.json` provides all nine original replay calls. Farmer's raw_observed profile is invalid evidence with no correct ref, since none of the source options has the requested units; repaired normal output changes one option. Website observed profile reproduces the source's visitors/visits teaching inconsistency; normal output says visits throughout. Do not deliver either raw teaching/evidence replay as a learner question. Two absent fields and two absent correct refs are explicitly derived/authored repairs. Their source provenance, omissions and fidelity denominators are separate in classification.md and validation.json.

`templates.json` contains extracted unit-slot masks and complete bank recipes, not copied question-return branches. Random and explicit calls share these recipes. Explicit inputs outside the documented domains raise ValueError. Option order is seeded; content identity excludes option order and depends on the actual prompt, solution and complete bank. Mathematical identity excludes bank/presentation profiles.

Validator reads the actual prompt, choices and every displayed unit-quotient stage independently. Exact named-unit scales distinguish kilograms from grams and hours/minute from minutes/hour. The separate real native grader tests every option using owned radio IDs; this does not replace mathematical/fidelity checks. All work stops after step 7 and is frozen for independent parent review.
