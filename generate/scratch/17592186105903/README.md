# Triangle area generator

Run from repository root:

```sh
.venv/bin/python generate/scratch/17592186105903/validate.py
.venv/bin/python generate/scratch/17592186105903.py --difficulty all --count 2 --format json
.venv/bin/python generate/scratch/17592186105903.py --difficulty easy --template radio_A --profile raw_q-18021
```

API entrypoints: generate_easy, generate_moderate, generate_hard and generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None). source-cases.json supplies all six public raw replay cases. Profiles raw_q-* are ineligible evidence; normal blanks and method_sine radio banks are eligible. Changed source parameters pass through the same masks/recipes, rather than literal source-return branches.

Only general-triangle area via half side product times sine is assessed. Missing moderate/hard levels are authored: decimal-side products; then an isosceles included-angle sum with hundredth sides. Read classification.md and template-extraction.md for bounds, evidence limitations and source precision/prose repairs. Raw q-18023 preserves absent rating/solution/correct designation. Normal completion infers11.12 independently.

Validation separates exact source fidelity, independently read displayed mathematics/complete banks/stages, geometry, identity, invalid boundaries, default family coverage and native engine grading. Native rounding blanks accept canonical precision and reject numerically equivalent extra trailing-zero precision; those equivalent-form rejections are explicitly tested and documented. There are no engine edits, database writes, registrations or commits. Work stops at step7.
