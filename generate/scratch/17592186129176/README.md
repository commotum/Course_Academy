# Leading-entry generator

Validated at math basis 2350. Only easy is supported; see `capabilities.json` for bounded exceptions. Normal seeded sampling supports the two-row and three-row templates and all 12 source bank profiles. The adjacent `source.json` is an immutable package dependency.

```bash
.venv/bin/python generate/scratch/17592186129176.py --difficulty easy --seed 42 --count 5 --format json
.venv/bin/python generate/scratch/17592186129176.py --template sum_3_rows --profile q-129204 --seed 7 --format markdown
.venv/bin/python generate/scratch/17592186129176/validate.py
.venv/bin/python generate/scratch/17592186129176/replenish.py
```

The generator requires Python 3 and SymPy 1.14.0 (available in the repository venv). Its scheduler-facing CLI uses the configured repository venv when invoked by a plain Python interpreter without SymPy. Unsupported band requests fail explicitly. Output carries version, seed, parameters, source profile and content-derived identities. Generated review examples are local; only a fresh inventory deficit authorizes importing new instances. `replenish.py` uses the existing EDB integration, native grader and preview, application contributor and api.lock, preserving exact requests and verified receipts.

Validation checks complete source banks, actual radio grading, 480 normal profile samples, all target subsets on a held matrix, leading-column boundaries and signs, deterministic replay, and invalid-input rejection. See `review.md` for originals and variants. Neither the missing source fields nor unsupported bands are presented as recovered content or filled inventory.
