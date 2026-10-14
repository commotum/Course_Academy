# Matched derivative power integration draft

Verification from repository root:

```sh
.venv/bin/python generate/scratch/17592186068722/validate.py
.venv/bin/python generate/scratch/17592186068722.py --difficulty all --seed 83 --count 2 --format json
```

Public Python API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` plus `generate_easy`, `generate_moderate`, `generate_hard`. All have radio output and five math choices. Explicit replay inputs appear in source-cases.json. The immutable source wrapper is copied unchanged; analysis basis is 2275, not the older worker snapshot.

Bounded same-method families vary a=1..5, m=2..6, b=−6..6, easy n=2..12, root n=0. These give 3575 easy and 325 each moderate/hard parameter tasks before presentation aliases. Root outputs apply on connected real intervals where the inner expression is positive. The levels retain respectively integer power, root conversion and reciprocal-root conversion. No derivative factor adjustment, logs or parts.

Default complete banks are explicitly authored from errors in the displayed operations; historical q-2189 and q-2390 banks are available through the API, flagged evidence-only and excluded from defaults. Their exact value patterns are reproduced; historical pedagogical intention is unresolved. No observed malformed TeX, mathematical source error, missing field or repair was found.

Validation compares every original full prompt, solution and bank exactly, correct refs and attribute presence. A strict private parser reads the actual learner TeX rather than generation metadata, independently checks each derivative/differential, substitution integral, power-rule row and final conclusion, then compares every pair of choices by derivatives (including two wrong answers) modulo C. Signed, zero and extreme parameters are tested for each complete bank. Display and control-character mutations must fail. The unmodified `generate/runs/current/check-engine` uses `learning::grade_field` with in-memory snapshots and no database access. Radio selection checks establish field/ID compatibility, with symbolic mathematics separately establishing option correctness. No blanks or unsupported parser entries are claimed.

Artifacts: classification.md; template-extraction.md; source.json; source-cases.json; review.md and review.json; validate.py; validation.json; engine-input.json and engine-report.json; runtime.json; hashes.json. No plots or rendering dependency. Generation writes no files; validation writes only this private evidence directory. This draft stops at step 7: no EDB writes, registration, engine edits, publication or commits.
