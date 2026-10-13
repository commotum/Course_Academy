# Three-variable gradient generator

Local draft, math basis 1356. Stops after steps 3–7; no database writes or registration.

Verify: `.venv/bin/python generate/scratch/17592186124444/validate.py`

Preview: `.venv/bin/python generate/scratch/17592186124444.py --difficulty all --seed 42 --count 2 --format json`

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` plus `generate_easy`, `generate_moderate`, `generate_hard`. Radio only; preserve observed selection field. Public historical replay uses `profile="observed_raw"` with source-cases.json parameters. Those records are evidence_only and ineligible for learning. Normal defaults sample all ten moderate families; opaque historical banks receive complete authored method banks. Easy and hard are clearly authored workload bands.

source.json is unchanged capture evidence. classification.md and template-extraction.md give full banks, all solution strings, curriculum anchors, bounds and source errors. review.md / review.json display originals and two generated examples for every template and every difficulty. validation.json separates raw fidelity, mathematical display checks and actual native grader results. Three raw source solutions have erroneous generic gradient component labels; corrected eligible output preserves remaining prose/stages. No plots or assets.

Additional independent checks: `.venv/bin/python generate/scratch/17592186124444/bank-operations.py` checks every authored whole bank against operations derived from actual displayed functions; `.venv/bin/python generate/scratch/17592186124444/operation-structure.py` enforces per-row operator masks and equal-math missing-operation mutations. Both are also invoked by validate.py. variety.json enumerates meaningful same-method tasks after excluding incidental periodic/point aliases. environment.json records Python 3.13.5, SymPy 1.14.0 and installed Matplotlib 3.11.2; no renderer is used.
