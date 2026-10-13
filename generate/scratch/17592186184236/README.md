# Local tangent stretch/vertical-shift draft

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186184236/validate.py
.venv/bin/python generate/scratch/17592186184236.py --difficulty all --seed 42 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186184236.py --difficulty easy --profile raw-q-65547 --format json
```

Public API: generate_easy, generate_moderate, generate_hard and generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None). Parameters are strings or exact rational numbers keyed B,D; optional source_mask selects an observed prose mask. Templates sum/difference. Fields are five-choice math radio. Normal complete profiles period-sign/omitted-sign; explicit raw-q-* profiles preserve original banks and omissions and are evidence-only. repair-q-* profiles separately label source-format/inferred repairs; only repair-q-65448 is eligible, while opaque banks remain ineligible.

Frozen source lineage/basis is preserved in source.json. Review originals, six changed source banks, explicit repairs and two generated examples for every level in review.md/review.json. source-cases.json replays every source via the public API. validation.json separates exact source fidelity, independently parsed mathematics, geometric checks and real native ID grading; native grading alone cannot prove bank correctness. Read classification.md, template-extraction.md and plot-extraction.md for scope, missing-level rationale and historical distractor interpretation limits.

No EDB reads/writes, shared edits, registration, engine modifications or commits. This draft stops at step 7 for parent QA.
