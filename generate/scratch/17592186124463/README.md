# Level-surface normal-vector generator

Run from repository root:

```sh
.venv/bin/python generate/scratch/17592186124463/validate.py
.venv/bin/python generate/scratch/17592186124463.py --difficulty all --seed 42 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186124463.py --difficulty easy --profile raw_q-37570 --format json
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and easy/moderate/hard entrypoints. Use `source-cases.json` for exact raw replay. Raw profiles are evidence-only and preserve legacy omissions; normal profiles are complete, eligible method-derived banks. Normal easy defaults cover all 12 source function families. Moderate/hard are explicitly authored bounded workloads within the same skill. `review.md` includes all originals and two generated variants for every observed family plus every level. `validate.py` independently reads the displayed function, point, formal operators, partials, substitutions, reduced/concluding vectors and banks before native UUID grading. No typed answer field is claimed. No database writes, registration, engine edits or post-step-7 work.
