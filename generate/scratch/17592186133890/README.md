# Cartesian supplied-potential FTLI generator

Production v2 supports the twelve observed easy/moderate source families. Hard
is unsupported; its five-question nominal shortage is explicit in
capabilities.json. Earlier authored structures were review experiments and are
excluded from production. No source questions or learner records are edited.

Run `.venv/bin/python generate/scratch/17592186133890/validate.py` for exact replay
of all twelve complete source banks, independently parsed prompt/endpoint/solution
mathematics for positive and negative coefficient variants, stable identities,
and the current native application grader. The documented q-39749 zero-start
substitution repair is applied only to generated solutions. Source evidence is
retained in source.json and reference/initial/kp.edn.

Preview distinct bounded variants with:
`.venv/bin/python generate/scratch/17592186133890.py --difficulty all --seed 17 --count 2 --format json`.
The CLI samples without replacement and fails explicitly beyond the finite
coefficient domain. Seed and option order do not create new question identities.

Run `.venv/bin/python generate/scratch/17592186133890/replenish.py` to recheck
inventory and perform needed additive publication under application api.lock.
The helper recovers saved exact requests before new work, uses the configured
application contributor, previews native validation specs, commits with a basis
guard, and verifies the exact committed basis. Registration reuses an existing
UUID or the KP's stable generator identity. Requests, previews, receipts, scoped
native inventory/grading checks and outcomes stay under reference/replenishment.
