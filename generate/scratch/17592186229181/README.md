# Equal-flow dilution generator

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186229181/validate.py
.venv/bin/python generate/scratch/17592186229181.py --difficulty all --seed 42 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186229181.py --difficulty moderate --profile raw_17592186377242 --format json
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and documented easy/moderate/hard entrypoints. Normal templates are `expression`, `amount`, `amount_unit_conversion`; normal complete bank is `method_bank`. Seven `source_<db-id>` templates and `raw_<db-id>` profiles preserve all source evidence and are ineligible for learning. Normal parameters are V, r, c (normalized kg/L), q0, context, plus time for moderate/hard; raw parameters are positive integer mass_scale in 1–4 and flow_scale in 1–3. Explicit invalid/ambiguous instances fail without resampling.

`source.json` and `source-cases.json` preserve provenance and replay routes. `masks.json` is the extraction product. `extract.py` rebuilds only those masks/cases from the private frozen source. `classification.md` and `template-extraction.md` document scope, bank limitations and omissions. `review.md`/`review.json` label originals and variants. `validate.py` checks original bytes/presence/banks/designations, printed numerical stages, exact model/distractor mathematics, identities, parameter guards, public JSON serialization, CLI labeling and the real native grader. Native reports are `engine-input.json`/`engine.json`; `validation.json` keeps denominators separate.

The missing hard level is authored feed-unit conversion followed by the same constant-volume IVP and rounded amount. Numerical source banks and two easy banks have opaque wrong-answer coefficients; defaults use a separately authored complete operation bank. This script has no plots, database client, writes, registrations, or engine changes. Frozen at step 7 for parent QA.
