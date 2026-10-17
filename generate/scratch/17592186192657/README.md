# Second-variable full system solve

Run the complete QA with:

```sh
.venv/bin/python generate/scratch/17592186192657/validate.py
.venv/bin/python generate/scratch/17592186192657.py --difficulty all --count 2 --format json
```

Public API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and easy/moderate/hard entrypoints. Templates: `radio_hint`, `pair_blank`. Normal banks: `signed_substitution`, `distribution_division` (moderate/hard only). Raw evidence profiles: `source_radio`, `source_blank`; require explicit original or changed parameters, preserve exact missing attributes, and are ineligible for learning. CLI also accepts JSON `--parameters` for public raw replay. `source-cases.json` gives both original parameter/profile calls.

All difficulty bands are authored integer-only workload distinctions anchored to the canonical full-solve sequence, linked lesson route and sibling KP. Exactly one row scaling, addition and back-substitution; no additional mathematical branch. Primitive-row guards keep genuine nonunit division workload. Full source banks and raw formatting anomalies remain evidence; normal presentations repair malformed TeX and infer complete fields/solutions. No observed correct refs or worked solutions exist for the two practice questions, so zero original designations/solutions are falsely counted as matched.

`validation.json` separates exact raw bank/prompt/presence fidelity from independent actual-display mathematics and real engine grading. All source-shaped normal families and eligible profiles are covered. `review.md` and `review.json` contain raw originals, changed raw evidence and at least two authored variants for every level/layout/bank. No database operations, shared engine edits or plots.

## Current system display repair (2026-10-16)

The registered generator now constructs systems with the shared `system_tex` helper: separate equation rows, explicit equation-label columns, and a single operation bar where applicable. Whole-equation multiplication stays grouped. The change preserves sampling, difficulty, mathematical task fingerprints, complete answer banks, and correct keys. Original source snapshots and raw replay prompts remain historical evidence.

Run the current presentation regression and native grading checks from the repository root:

```sh
.venv/bin/python reference/mathacademy/repairs/2026-10-16-system-equations-display/generators/verify.py
```

That harness compares retained pre-repair generators with current output across every supported template and difficulty, invokes the historical mathematical validators on the baseline, checks arithmetic and answer equivalence, and grades current output with the native engine. It avoids the historical validators' semicolon-only display parsers. Current render evidence is in `reference/mathacademy/repairs/2026-10-16-system-equations-display/generators/`.
