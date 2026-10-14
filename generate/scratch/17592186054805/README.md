# Quartic factoring draft

Script: `generate/scratch/17592186054805.py`. Local JSON review records only; no database writes, registration, engine changes, shared-file changes or commits.

```sh
.venv/bin/python generate/scratch/17592186054805/validate.py
.venv/bin/python generate/scratch/17592186054805.py --difficulty all --seed 42 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186054805.py --difficulty hard --template q-328607 --count 2 --format json
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and `generate_easy`, `generate_moderate`, `generate_hard`. Parameters are exactly integer `r1,r2,a,b,c`; the polynomial is `sign*(x-r1)*(x-r2)*(a*x^2+b*x+c)`. `r1/r2` identify first/second synthetic roles. Profiles `method_q-N` are normal defaults. Profiles `observed_q-N` are publicly available **evidence-only** raw replays with missing source attributes and the documented source typo preserved. Explicit parameters are checked; invalid inputs fail rather than resample.

Bounds: nonzero integer roots of absolute value ≤6, quadratic a=1..3, b=−4..4, c=1..9, negative discriminant. Easy further requires repeated roots and a=1,b=0. Moderate/hard require distinct roots; hard preserves outside minus. Normal defaults cover every source-shaped family; radio banks are separately authored from synthetic operations, with whole-instance collision rejection.

The validator reads actual printed polynomials, tables, quotient equations, factorization rows, discriminants and conclusions. It checks source bytes, key presence, all 27 displayed source options, five available source correct designations, original solution stages and meaningful task capacity. Native engine fixtures exercise every owned radio option and equivalent Horner-form blank entries. Review originals, inferred/repaired anchors and two changed variants per family in review.md/review.json. Parent QA is required before adoption.

Known evidence limitations: q-75798/q-75803 lack source difficulty, solution and correct refs; q-76184 lacks the source field. These are independently inferred only in normal output. q-112651 prints an incorrect second denominator x−2 (actual divisor x−5). Raw retains it; normal repairs it. q-18852's final p(x) typo becomes f(x); historical underbrace groups become canonical `\underbrace`. Opaque historical radio distractor intent remains unresolved and is excluded from normal serving. No grading failures remain for supported normal records.
