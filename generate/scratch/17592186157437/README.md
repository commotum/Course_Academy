# Exponential equations by factoring

Local steps 3–7 generator for KP 17592186157437. No database writes or registration.

Verify:

```sh
.venv/bin/python generate/scratch/17592186157437/validate.py
.venv/bin/python generate/scratch/17592186157437.py --difficulty all --count 2 --seed 42 --format json
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and the three difficulty helpers. Field types are `radio` or `blank`. All explicit inputs obey documented bounds. `profile=q-...` replays an observed display and whole bank; default/`authored` uses a separately authored operation bank.

14 exact original prompts, 13 exact available entire worked solutions, 14 exact banks/layouts; the missing q-88412 correct designation and solution are independently derived/authored and never counted as observed matches. Hard comprises two authored rational-root layouts anchored to leading-coefficient factoring. Scalar source bank intent is underidentified; the replay formulas are preserved without asserting author intent. All levels are plot-free.

Evidence: `source.json`, `source-cases.json`, display masks, classification/extraction, source-versus-generated review, validation results and native memory-only engine fixtures/report. Validation reads actual displayed mathematical stages independently and compares every source choice and designation separately from native grading.
