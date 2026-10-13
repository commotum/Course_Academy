# Cartesian flux setup generator

Scratch-only, steps 3–7; no database writes. Use:

```sh
.venv/bin/python generate/scratch/17592186198389.py --difficulty all --seed 42 --count 2 --format json
.venv/bin/python generate/scratch/17592186198389.py --difficulty easy --template q-161359 --profile q-161359 --count 2
.venv/bin/python generate/scratch/17592186198389/validate.py
```

API: generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None), plus generate_easy/moderate/hard with the same optional arguments. JSON uses existing leading-colon attributes, enum strings, field-owned UUIDs and lookup refs; it is review data, not transaction data. Source profiles preserve all original banks; normal banks are authored operations. Moderate/hard are authored bounded concrete setup variants. See classification.md for level workload bounds, extraction for source repairs and expression-pattern intent limits, validation.json for separate fidelity/correctness/grading counts, and review.md/review.json for originals and variants.
