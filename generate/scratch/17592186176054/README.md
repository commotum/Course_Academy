# Cosecant-periodicity draft generator

Verify from repository root:

```sh
.venv/bin/python generate/scratch/17592186176054/validate.py
.venv/bin/python generate/scratch/17592186176054.py --difficulty all --seed 42 --count 2 --format json
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and `generate_easy`, `generate_moderate`, `generate_hard`. Default field is radio; `operations` is the normal authored bank. Explicit source-shaped evidence uses `profile="raw:q-103820"` (all seven cases and parameter sets are in `source-cases.json`). Raw profiles are always evidence-only, preserve original omissions/references/order at original inputs, and use nested captured enum objects; `native_record` in the validator adapts these to in-memory grading enums without changing public raw evidence. Explicit invalid parameters raise `ValueError`.

All seven original banks and records replay exactly. Normal solutions preserve all five existing original chains exactly at source parameters, with changed-parameter structural and mathematical checks. Two unrated originals lack correct refs and solutions; their easy designation, normal correct ref and shared worked solution are explicitly authored. Historical bank intent remains unresolved; complete raw banks are excluded from normal learning. Hard has no observed source: its authored two-reduction/rational-combination workload stays in the same periodicity skill. No plots, engine edits, shared edits, registration or database writes. Work stops after step 7.

`validation.json` reports complete fidelity, independent displayed math, finite domains, identity/deduplication checks, actual runtime versions and real application grading. `review.md`/`review.json` include every original, normal original-parameter variant, changed evidence-bank variants and changed normal family examples, plus two hard examples. Private typed blank fixtures test unsimplified equivalent substitution expressions without changing the radio learner shape.
