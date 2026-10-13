# Perpendicular slope-intercept generator

Local steps 3–7 only. Script: `../17592186110599.py`. Uses `.venv` SymPy, exact rationals, deterministic sampling, one radio field with five full-equation choices; no database writes or engine changes.

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python generate/scratch/17592186110599/validate.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python generate/scratch/17592186110599.py --difficulty all --seed 20 --count 2 --format markdown
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` plus `generate_easy`, `generate_moderate`, `generate_hard`. Explicit parameters require `m`, `b`, five `intercepts`; exact integers/rational strings only. Supported templates are `compact`, `spaced`; profile/template and level mismatches fail. Authored default banks are used for ordinary generation. CLI supports difficulty, seed, count, format, template, profile.

`source.json` preserves raw basis-1356 evidence; `source-cases.json` replays all seven questions. `original-widgets.json` and copied section images support the two missing designations/solutions. Derived values for those two are not observed designation matches. q-72524 has two malformed quadratic distractors: strict raw replay is an explicitly evidence-only profile; normal banks remain lines, and `repaired-q-72524` applies the minimal correction.

`classification.md` and `template-extraction.md` distinguish observed profiles, interpretation limits, missing-label assignments, authored hard scope, and finite substantive variety. `review.md` includes every original, source replay, two changed-parameter variants of every observed profile, at least two authored examples of each level, and the minimal repair. `review.json` holds their records. `validation.json` reports complete-bank/notation/prompt/solution/designation fidelity separately from mathematical correctness, scope quarantine, identities, and real `learning::grade_field` checks (`engine-input.json`, `engine-report.json`). No plots are required.
