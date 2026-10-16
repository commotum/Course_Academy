# Quadrant slope sign generator

Steps 3–7 complete locally at math basis 1356. No database writes, registration, engine edits or commits.

```bash
.venv/bin/python generate/scratch/17592186172039.py --difficulty all --seed 43 --count 2 --format json
.venv/bin/python generate/scratch/17592186172039/build_evidence.py
.venv/bin/python generate/scratch/17592186172039/validate.py
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and `generate_easy`, `generate_moderate`, `generate_hard`. Exact explicit parameter keys are c,a,b,quadrants,claims. Profiles and template names are documented in the classification/extraction files. No explicit invalid instance is silently changed. The CLI supports difficulty/seed/count/format/template/profile.

Eight complete banks and all 40 displayed options replay through parameterized recipes. Seven correct refs and seven available solutions match exactly. q97483's missing designation is independently derived; its hard level and solution are authored additions, with original evidence retained. Easy cx, hard coordinate-swapped parity and the normal complement/toggle sign-error bank are authored extensions. All 320 canonical meaningful tasks are exhaustively checked; cosmetic coefficient changes and reordered statements are excluded from task counts.

`validation.json` reports fidelity separately from mathematics and native grading. `engine-input.json` and `engine-report.json` capture genuine application `learning::grade_field` checks using only in-memory fixtures: 46 correct selections accepted, 184 wrong selections rejected, 0 unresolved. Four source diagrams and six authored Matplotlib diagrams were inspected; rendering dependency/concurrency evidence is included. `review.md`/`review.json` contain originals, all profile/layout replays and two changed variants per source, plus at least two authored defaults per level. Learner content should never expose correct refs or generation metadata before submission.
