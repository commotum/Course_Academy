# Second-variable full system solve

Run the complete QA with:

```sh
.venv/bin/python generate/scratch/17592186192657/validate.py
.venv/bin/python generate/scratch/17592186192657.py --difficulty all --count 2 --format json
```

Public API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and easy/moderate/hard entrypoints. Templates: `radio_hint`, `pair_blank`. Normal banks: `signed_substitution`, `distribution_division` (moderate/hard only). Raw evidence profiles: `source_radio`, `source_blank`; require explicit original or changed parameters, preserve exact missing attributes, and are ineligible for learning. CLI also accepts JSON `--parameters` for public raw replay. `source-cases.json` gives both original parameter/profile calls.

All difficulty bands are authored integer-only workload distinctions anchored to the canonical full-solve sequence, linked lesson route and sibling KP. Exactly one row scaling, addition and back-substitution; no additional mathematical branch. Primitive-row guards keep genuine nonunit division workload. Full source banks and raw formatting anomalies remain evidence; normal presentations repair malformed TeX and infer complete fields/solutions. No observed correct refs or worked solutions exist for the two practice questions, so zero original designations/solutions are falsely counted as matched.

`validation.json` separates exact raw bank/prompt/presence fidelity from independent actual-display mathematics and real engine grading. All source-shaped normal families and eligible profiles are covered. `review.md` and `review.json` contain raw originals, changed raw evidence and at least two authored variants for every level/layout/bank. No database operations, shared engine edits or plots.
