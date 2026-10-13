# Complex-root vertical asymptotes generator

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186087844.py --difficulty all --count 2
.venv/bin/python generate/scratch/17592186087844.py --difficulty moderate --template q-113525 --profile original --format json
.venv/bin/python generate/scratch/17592186087844/validate.py
```

Public API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and separate easy/moderate/hard entrypoints. Templates are source Math Academy IDs listed in `SPECS`. Profiles: `original` (raw, preserving missing fields and source metadata), `supported-observed` (observed banks with teaching repair and supported missing-field completions), and default `authored` (same source solution structure with complete authored banks). Explicit invalid parameters fail, never change silently. Source-case replay goes through the public API.

Scope: negative-discriminant denominator factors, with quadratics at easy, GCF/grouping at moderate, cubes at hard. All numerator/denominator pairs are coprime; no hole cancellation or complex-number root arithmetic. No plots, transactions, shared edits or nested agents. Native grading uses the existing memory-only `check-engine`; printed expression checks are independent of generator metadata. `validation.json` separates fidelity, repairs, supported completions, mathematics and actual native checks.

The task fingerprint uses the monic denominator and, for the four observed factorable-numerator families, the monic numerator. Scalar prefactors, irrelevant linear shifts and answer-bank/profile differences are excluded; actual prompt/solution/bank determine presentation identity. Raw originals and opaque observed radio banks are explicitly evidence-only and ineligible for learning. Exhaustive eligible task counts are 98 easy, 444 moderate and 36 hard. No unlimited diversity claim is made: bounded integer samplers are finite and documented in `template-extraction.md`.
