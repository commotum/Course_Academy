# Standard-form parallel-line generator

Local review artifact only; no database writes, registration or engine changes.

```sh
.venv/bin/python generate/scratch/17592186087687/validate.py
.venv/bin/python generate/scratch/17592186087687.py --difficulty all --count 2
.venv/bin/python generate/scratch/17592186087687.py --difficulty moderate --profile q-110094 --format json
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None,
profile=None)` and `generate_easy`, `generate_moderate`, `generate_hard`.
Explicit source cases are in source-cases.json. q-* profiles preserve raw omissions;
completed:q-* records are inferred evidence. Normal defaults use separately authored
complete method banks and canonical-example solution stages. All level classifications
are authored: source practice has no labels, keys or solutions. See classification.md,
template-extraction.md, review.md and validation.json for bounds and exact counts.
No plots are assessed; no plot renderer is required.

Verified catalog sizes: 22 easy, 24 moderate, 36 hard reduced-slope tasks.
Validation parses 1,068 normal signed/profile/boundary instances, 96 raw opaque
profile boundary instances, all source cases and generated reviews; native grading
accepts 1,071 correct selections and rejects 4,284 wrong selections, with zero
unresolved checks. The pre-existing reference/ and replenishment artifacts are
historical and are not outputs or entrypoints of this frozen step 3–7 rebuild.
