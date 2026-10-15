# Parametric normal-line generator

Run the independent mathematical/fidelity/native validation:

```sh
.venv/bin/python generate/scratch/17592186083245/validate.py
.venv/bin/python generate/scratch/17592186083245.py --difficulty all --seed 42 --count 2 --format json
```

The script exposes `generate_easy`, `generate_moderate`, `generate_hard` and `generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None)`. All three levels are supplied. Source replay uses the parameters/profile in `source-cases.json`, preserving actual enum values, absent fields/refs and field ordering. Raw profiles are evidence-only; authored normal banks remain separate. Native fixtures exercise every answer field and all radio choices, scalar canonical/equivalent/wrong entries. Local artifacts are review records, not database transactions.

Evidence is frozen at math basis1356. `classification.md` and `template-extraction.md` distinguish observed, authored and opaque components. Eight source questions include an unrated incomplete quartic intercept. Easy is explicitly authored from the route/prerequisites; hard supplies a supported completion for that source. The two stated prose repairs and native “round” limitation are recorded separately. Coordinate translations provide new lines/intercepts at each source family's fixed derivative workload; this is not a claim of new recovered templates. No database, registration, engine, shared environment or installation changes.

## Current inventory integration

`replenish.py --prepare` rechecks current inventory, source additions, every selected question and current learner grading. `replenish.py --commit` acquires the application `api.lock`, repeats the basis/inventory checks, previews using deployed native validation predicates, persists the exact basis-guarded request, submits, and verifies its exact committed basis. Registration uses the existing schema and stable identity recorded in `registration.json`.

See `classification-refresh.md` for the four added sources and scoped generation policy. Historical `validation.json` remains the frozen-package report. `reference/native/full-validation-report.json` is the current-engine recheck: 98 accepted, 168 rejected, zero unresolved; eight historical round-wording expectations now accept equivalent exact entries. The current native build and source/library hashes are retained in `reference/native/build.json`. Live database verification and exact requests/receipts are under `reference/replenishment/`.
