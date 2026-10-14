# Derivative units generator

```sh
.venv/bin/python generate/scratch/17592186064271/validate.py
.venv/bin/python generate/scratch/17592186064271.py --difficulty all --count 2 --seed 24 --format json
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and the three level entrypoints. Unit-interpretation only; no differentiation or numeric conversions. JSON is local review data. No DB operations. Plot rating none.

`source-cases.json` provides all nine original replay calls. Farmer's raw_observed profile is invalid evidence with no correct ref, since none of the source options has the requested units; repaired normal output changes one option. Website observed profile reproduces the source's visitors/visits teaching inconsistency; normal output says visits throughout. Do not deliver either raw teaching/evidence replay as a learner question. Two absent fields and two absent correct refs are explicitly derived/authored repairs. Their source provenance, omissions and fidelity denominators are separate in classification.md and validation.json.

`templates.json` contains extracted unit-slot masks and complete bank recipes, not copied question-return branches. Random and explicit calls share these recipes. Explicit inputs outside the documented domains raise ValueError. Option order is seeded; content identity excludes option order and depends on the actual prompt, solution and complete bank. Mathematical identity excludes bank/presentation profiles.

Validator reads the actual prompt, choices and every displayed unit-quotient stage independently. Exact named-unit scales distinguish kilograms from grams and hours/minute from minutes/hour. The separate real native grader tests every option using owned radio IDs; this does not replace mathematical/fidelity checks. The original draft covered steps 3–7; the verified replenishment below completes preparation and commit.

## Verified inventory replenishment

Revalidated and committed on 2026-10-14, from math basis 2249 to 2250, under
`.local/learning/requests/math/api.lock`. Contributor: `:application/ca-engine`.
Registered generator UUID `e5d9c8a9-e502-52af-b588-07dab00deac0` and script
`generate/scratch/17592186064271.py` through the existing generator attributes.

Current validated fresh inventory: easy 5, moderate 5, hard 5. The commit added
five moderate and five hard questions; moderate/hard are documented authored
workload assignments. All nine source questions, the canonical example and
learner history are unchanged. Four incomplete/unrated sources remain excluded.
Meaningful finite capacities and their limits are in `capabilities.json`.

`reference/replenishment/basis-2249/` retains the captured source read, current
inventory, independent mathematical checks, native grading, complete prepared
EDN, preview, exact durable request, committed receipt and exact-basis readback.
Verification confirms only additive scoped content facts and repeat preparation
produces no content changes. No plot assets were required.

The scoped `replenish.py` recovers retained requests before new work and rechecks
current inventory while holding the application lock. It imports the validator
without rerunning the standalone source audit. Run `validate.py` directly for
full source fidelity, finite-domain mathematics and native grading validation.
