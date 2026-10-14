# Triangle area generator

Run from repository root:

```sh
.venv/bin/python generate/scratch/17592186105903/validate.py
.venv/bin/python generate/scratch/17592186105903.py --difficulty all --count 2 --format json
.venv/bin/python generate/scratch/17592186105903.py --difficulty easy --template radio_A --profile raw_q-18021
```

API entrypoints: generate_easy, generate_moderate, generate_hard and generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None). source-cases.json supplies all six public raw replay cases. Profiles raw_q-* are ineligible evidence; normal blanks and method_sine radio banks are eligible. Changed source parameters pass through the same masks/recipes, rather than literal source-return branches.

Only general-triangle area via half side product times sine is assessed. Missing moderate/hard levels are authored: decimal-side products; then an isosceles included-angle sum with hundredth sides. Read classification.md and template-extraction.md for bounds, evidence limitations and source precision/prose repairs. Raw q-18023 preserves absent rating/solution/correct designation. Normal completion infers11.12 independently.

Validation separates exact source fidelity, independently read displayed mathematics/complete banks/stages, geometry, identity, invalid boundaries, default family coverage and native engine grading. Native rounding blanks accept canonical precision and reject numerically equivalent extra trailing-zero precision; those equivalent-form rejections are explicitly tested and documented. The generator only creates local records. `replenish.py` performs the documented database preparation and commit stages through the existing application integration. It holds the application api.lock across inventory recheck, basis-guarded submission and exact-basis readback; durable requests and receipts are retained under `reference/replenishment/`. No engine or scheduler edits are needed.


## Verified replenishment

The 2026-10-14 run rechecked current source evidence at basis 2482. All six prompts, solutions, fields, banks and existing difficulty facts matched the original capture. Two sources had gained `question/requires-calculator=true`; this additive metadata is recorded in `reference/replenishment/basis-2482/source-refresh.json`. Normal generated instances now explicitly require a calculator. Raw evidence replay retains the original captured shape.

The additive commit at basis 2483 registered the script UUID and repository-relative path and added two easy, five moderate and five hard questions. Available mathematically checked, gradable, unseen, unreserved inventory is 5/5/5. Moderate and hard retain the authored policies and evidence limits documented in classification.md. The two known erroneous sources and the unrated incomplete source are preserved and excluded from validated inventory. The original canonical example is preserved.

`reference/replenishment/basis-2482/` retains the exact EDN, explicit application contributor, request key, lineage, basis guard, speculative preview, verified durable receipt, source comparison, published asset hashes, native grading reports and exact-basis verification. A repeated preparation would add no content.
