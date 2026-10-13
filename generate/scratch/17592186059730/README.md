# Component dot product generator

Scope: KP17592186059730 only; captured math basis 1356. One scalar dot product by corresponding-component multiplication and addition. No database operations.

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186059730/validate.py
.venv/bin/python generate/scratch/17592186059730.py --difficulty all --seed 42 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186059730.py --difficulty easy --profile observed_1340 --seed 42 --format json
```

The API exposes `generate`, `generate_easy`, `generate_moderate`, and `generate_hard`; explicit parameters/profile replay follows `source-cases.json`. Original sources remain in `source.json`. All seven source complete banks replay; source-format repairs and absent correct/solution data are reported separately in `validation.json`. Moderate and hard levels and normal radio banks are authored extensions. Source scalar distractor intent remains underdetermined and observed-bank numerical reconstructions are explicit replay profiles only.

`validate.py` independently reads the actual printed vectors, checks every option and every formal/multiplication/evaluated-product/final stage, exact full source solution equality, identity, formatting, workload guards, and native engine grading. `engine-input.json` and `engine-report.json` preserve native evidence. `review.md` includes every original, every original-parameter replay, changed variants for every observed bank, and at least two authored variants per difficulty/layout. `freeze.json` records the frozen actual artifact hashes for parent QA.

The registered generator UUID is `4e729dd4-b331-5f5b-8c36-7bc58a5536ca`. System-Python CLI execution automatically uses the repository `.venv/bin/python` when SymPy is unavailable. This changes neither mathematical output nor question identities. `reference/replenishment/` retains the exact basis-guarded request, receipt, and readback for the initial replenishment.
