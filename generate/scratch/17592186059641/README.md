# GCF factoring and the Pythagorean identity

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186059641/validate.py
.venv/bin/python generate/scratch/17592186059641.py --difficulty all --count 2 --format json
.venv/bin/python generate/scratch/17592186059641.py --difficulty easy --profile raw:q-119362 --format json
```

The API exposes `generate`, `generate_easy`, `generate_moderate` and `generate_hard`; explicit parameters obey the same workload and whole-bank guards as sampling. `raw:<source-id>` profiles preserve missing keys and source errors as evidence-only. `repaired:<source-id>` profiles make documented mathematical/presentation repairs or authored missing-field completion. Defaults use `authored_operations` with `one_gcf`, `gcf_residual` or `two_gcf` templates. `field_type='blank'` is an authored complete-expression layout.

No plots or database operations. The validator independently parses actual displayed trigonometric polynomials and every equation stage, checks all 598 finite authored tasks and 120 sampled outputs, compares every source choice and key-presence condition, tests explicit invalid bounds, and invokes the real native grader. `hashes.json` freezes script/evidence and grader hashes. Hard has no observed source label; source distractor intentions remain unresolved. See `classification.md`, `template-extraction.md`, `validation.json` and complete originals/variants in `review.md`.
