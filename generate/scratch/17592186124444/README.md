# Three-variable gradient generator

Validated generator from source basis 1356, rechecked at basis 2666. Additive replenishment and generator registration were verified at math basis 2667. Ten new questions (five easy, five hard); validated fresh inventory: easy 5, moderate 7, hard 5. All eleven current source questions and learner history are preserved. Exact preview, request, receipt, and readback are in `reference/replenishment/basis-2666/`. The final native inventory has no remaining job for this KP.

Verify: `.venv/bin/python generate/scratch/17592186124444/validate.py`

Preview: `.venv/bin/python generate/scratch/17592186124444.py --difficulty all --seed 42 --count 2 --format json`

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` plus `generate_easy`, `generate_moderate`, `generate_hard`. Radio only; preserve observed selection field. Public historical replay uses `profile="observed_raw"` with source-cases.json parameters. Those records are evidence_only and ineligible for learning. Normal defaults sample all ten moderate families; opaque historical banks receive complete authored method banks. Easy and hard are clearly authored workload bands.

source.json is unchanged capture evidence. classification.md and template-extraction.md give full banks, all solution strings, curriculum anchors, bounds and source errors. review.md / review.json display originals and two generated examples for every template and every difficulty. validation.json separates raw fidelity, mathematical display checks and actual native grader results. Three raw source solutions have erroneous generic gradient component labels; corrected eligible output preserves remaining prose/stages. No plots or assets.

Additional independent checks: `.venv/bin/python generate/scratch/17592186124444/bank-operations.py` checks every authored whole bank against operations derived from actual displayed functions; `.venv/bin/python generate/scratch/17592186124444/operation-structure.py` enforces per-row operator masks and equal-math missing-operation mutations. Both are also invoked by validate.py. variety.json enumerates meaningful same-method tasks after excluding incidental periodic/point aliases. environment.json records Python 3.13.5, SymPy 1.14.0 and installed Matplotlib 3.11.2; no renderer is used.

The source recheck found an additional moderate polynomial-at-point question with malformed stored escapes and an unsupported angle-vector readback shape. It is explicitly excluded from validated inventory and this generator's ten-family fidelity claim; see `reference/source-refresh-2666.json`. Three other original questions retain known erroneous gradient labels and are also excluded from usable inventory. None were changed. Shared math-format validation now guards public generated records without changing their content or identities.
