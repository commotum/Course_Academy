# Perpendicular slope-intercept generator

Validated steps 3–9. Script: `../17592186110599.py`. Uses `.venv` SymPy, exact rationals, deterministic sampling, one radio field with five full-equation choices. Database replenishment uses the existing application integration; no engine changes.

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python generate/scratch/17592186110599/validate.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python generate/scratch/17592186110599.py --difficulty all --seed 20 --count 2 --format markdown
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` plus `generate_easy`, `generate_moderate`, `generate_hard`. Explicit parameters require `m`, `b`, five `intercepts`; exact integers/rational strings only. Supported templates are `compact`, `spaced`; profile/template and level mismatches fail. Authored default banks are used for ordinary generation. CLI supports difficulty, seed, count, format, template, profile.

`source.json` preserves raw basis-1356 evidence; `source-cases.json` replays all seven questions. `original-widgets.json` and copied section images support the two missing designations/solutions. Derived values for those two are not observed designation matches. q-72524 has two malformed quadratic distractors: strict raw replay is an explicitly evidence-only profile; normal banks remain lines, and `repaired-q-72524` applies the minimal correction.

`classification.md` and `template-extraction.md` distinguish observed profiles, interpretation limits, missing-label assignments, authored hard scope, and finite substantive variety. `review.md` includes every original, source replay, two changed-parameter variants of every observed profile, at least two authored examples of each level, and the minimal repair. `review.json` holds their records. `validation.json` reports complete-bank/notation/prompt/solution/designation fidelity separately from mathematical correctness, scope quarantine, identities, and real `learning::grade_field` checks (`engine-input.json`, `engine-report.json`). No plots are required.

The current grader is compiled into `reference/validation/check-engine`, with exact library and source hashes in `reference/validation/build.json`. `freeze.json` records the validated package hashes. `capabilities.json` documents the authored hard allocation, source exclusions, and finite normal-domain limits of 22 easy, 22 moderate, and 76 hard reduced target slopes. Intercepts and answer-bank changes never count as new mathematical tasks. The CLI returns samples; `replenish.py` enforces distinctness against the whole existing pool and canonical example before admission.

Run `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python generate/scratch/17592186110599/replenish.py` to prepare or recover this job. It acquires `.local/learning/requests/math/api.lock`, captures current inventory, validates all selected instances mathematically and through the current learner grader, previews native validation specs, and retains a basis-guarded request and verified receipt. The lock stays held through submission and exact-basis readback. Attribution is the configured `:application/ca-engine` contributor.

This job committed at basis **2233**, prepared at **2232**: one easy, five moderate, and five hard questions. Validated available inventory is **5 / 5 / 5**, with no remaining KP jobs. Generator UUID `237b012a-82d4-5f3d-9897-d77caddabc4c` is registered at `generate/scratch/17592186110599.py`. All seven original practice questions and the canonical example remain unchanged. The malformed moderate source and two incomplete unrated sources remain excluded from the validated reserve. Evidence, exact EDN, request, receipt, and readback are in `reference/replenishment/basis-2232/`.
