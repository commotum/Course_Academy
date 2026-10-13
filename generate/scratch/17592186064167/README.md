# Finding the Antiderivative of a Monomial

Reuse of the existing source-faithful generator. Source capture is math basis
1356; replenishment evidence uses current pinned reads under `reference/`.
Only easy is supported, with a finite 0..20 exponent domain. Moderate and hard
are unsupported: the old larger-exponent labels did not establish distinct
workload. See classification.md and capabilities.json. Production replenishment
uses radio fields, deduplicates by integrand across all layouts and profiles,
and excludes every source/canonical integrand already in the KP.

```sh
.venv/bin/python generate/scratch/17592186064167/validate.py
.venv/bin/python generate/scratch/17592186064167.py --difficulty easy --seed 12 --count 2 --format json
.venv/bin/python generate/scratch/17592186064167/replenish.py
```

Raw replay preserves absent fields, solutions and correct refs and is ineligible.
The validator checks printed mathematics, complete bank replay, every finite
easy exponent and applicable profile, deterministic identities, and actual
native grading. Blank previews retain the native arbitrary-C equivalence
limitation; production commits only radio selection questions. No plots.
The replenisher preserves originals and learner history, registers one stable
UUID and script path, retains exact requests and receipts, and holds the shared
application api.lock through current inventory reads, guarded commit and readback.
