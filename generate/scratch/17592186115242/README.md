# KP17592186115242 local generator

Run from repository root:

```sh
.venv/bin/python generate/scratch/17592186115242/validate.py
.venv/bin/python generate/scratch/17592186115242.py --difficulty all --seed 4 --count 2 --format markdown
```

All three difficulties; no database access or registration. Seven observed templates, fifteen five-choice radio banks, one missing-level authored easy template, and method-based authored default banks. Observed profiles replay via `generate(level, parameters=..., profile="q-...")` using source-cases.json. Opaque observed bank intent remains unresolved and is not used for normal defaults. Two source mathematical solution errors and eleven source system-brace presentation errors have explicit repairs. Exact and repaired fidelity counts are reported separately. Validation independently parses printed equations, every printed matrix and row operation, all answer values and solution statements; fidelity and native radio grading are counted separately. Review includes every original, replay and changed-profile variant, and two authored defaults of each template.

Inventory replenishment now uses `replenish.py`. Its artifacts are scoped beneath
`reference/replenishment/`; it obtains the application's api.lock, checks live
inventory and source evidence, validates distinct tasks and actual grading,
previews native specs, saves an exact basis-guarded request, and verifies the
receipt and scoped additive datoms before releasing the lock. `--prepare-only`
retains a review without submission. The supplemental `validate-current.py`
replays all 16 live source banks and preserves the original 15-source capture.
The registry reuses an existing generator UUID and otherwise uses the KP-derived
stable identity. Only easy stock is needed for the current classification job;
the moderate and hard reserves are rechecked before preparing additions.
