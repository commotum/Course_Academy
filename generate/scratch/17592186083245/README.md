# Parametric normal-line generator

Run the independent mathematical/fidelity/native validation:

```sh
.venv/bin/python generate/scratch/17592186083245/validate.py
.venv/bin/python generate/scratch/17592186083245.py --difficulty all --seed 42 --count 2 --format json
```

The script exposes `generate_easy`, `generate_moderate`, `generate_hard` and `generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None)`. All three levels are supplied. Source replay uses the parameters/profile in `source-cases.json`, preserving actual enum values, absent fields/refs and field ordering. Raw profiles are evidence-only; authored normal banks remain separate. Native fixtures exercise every answer field and all radio choices, scalar canonical/equivalent/wrong entries. Local artifacts are review records, not database transactions.

Evidence is frozen at math basis1356. `classification.md` and `template-extraction.md` distinguish observed, authored and opaque components. Eight source questions include an unrated incomplete quartic intercept. Easy is explicitly authored from the route/prerequisites; hard supplies a supported completion for that source. The two stated prose repairs and native “round” limitation are recorded separately. Coordinate translations provide new lines/intercepts at each source family's fixed derivative workload; this is not a claim of new recovered templates. No database, registration, engine, shared environment or installation changes.
