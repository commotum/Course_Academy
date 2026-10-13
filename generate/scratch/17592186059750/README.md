# Determinant unknown generator

Local, read-only-source generator for KP17592186059750. All 15 sources, all three levels and all observed field layouts are covered. Source wrapper retains math basis1356 provenance. Source profiles contain complete observed banks; normal radio banks use authored operations. q-11651/q-19801 correct values are mathematically inferred and their difficulty labels are explicitly authored placements; q-127614 has an explicitly authored blank and placeholder. These repairs are not counted as observed refs/fields.

```sh
.venv/bin/python generate/scratch/17592186059750.py --difficulty all --count 2 --seed 41 --format json
.venv/bin/python generate/scratch/17592186059750/build_docs.py
.venv/bin/python generate/scratch/17592186059750/validate.py
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and individual `generate_easy`, `generate_moderate`, `generate_hard`. Template keys are source-layout IDs listed in classification.md. Parameters require exactly `c` (integer component list) and `root` (nonzero integer). Original cases and profiles are in source-cases.json. Original profile example: `observed:q-127609`; normal radio profile: `authored:operations`. Defaults sample only complete eligible banks and reject collisions. Blank profile is `none`, except the field repair defaults to `authored:blank_repair`.

Validation parses actual printed matrices, every product/distribution/cancellation row, every equation stage, all displayed choice values, all original banks/correct refs/prose/stage sequence, restrictions, identity and formatting. Native grader uses the shared memory-only application harness and checks all choices plus unreduced equivalent and wrong blank entries. Grader report, honest fidelity denominators, original/variant review and final artifact hashes are separate evidence. No EDB, engine, shared files or assets are modified.

Opaque observed scalar recipes retain unknown intent; numerical replay alone is not evidence of a recovered misconception. The authored operation banks are the ordinary learner-generation defaults. Hard remains quadratic cancellation to linear, not arbitrary harder quadratic solving.
