# One independent variable chain rule

Run from the repository root:

```
.venv/bin/python generate/scratch/17592186166747/validate.py
.venv/bin/python generate/scratch/17592186166747/variety.py
.venv/bin/python generate/scratch/17592186166747.py --difficulty all --count 2 --seed 42 --format json
```

The script implements easy/moderate/hard and `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)`. Normal output uses `method_branches`; the public `observed_raw` and `observed_repaired` profiles preserve each complete original bank and are explicitly evidence-only/ineligible. Replay profile parameters are `{h: integer between -3 and 3}`; normal parameters are integer n,a,b,h,k with the per-level guards in the script. See source-cases.json for all twelve original replay calls.

Validation reads the actual prompt, every partial and component derivative, each substitution equality and each final arithmetic/product row, and all choices with an independent TeX reader and SymPy. Native owned radio selection is tested separately with the current real application check-engine. There are no blank fields, so typed-equivalent submission testing is inapplicable. Historical source missing correct/solution/difficulty, domain omissions and opaque distractor intent are explicitly recorded.

Version `one-independent-v2` normalizes learner content before computing identities and validates it with the shared math-content convention. Choice ordering uses a separate seeded random stream so an explicit parameter replay matches the sampled call. Mathematical fingerprints exclude difficulty as well as seeds and bank order, preventing the same task from being counted again at another level.

`reference/initial.json` captures current source evidence at basis 2736. The formerly incomplete q-94587 is now complete and rated easy upstream; the original basis-1356 snapshot is retained unchanged. `reference/current-source-replay.json` verifies all 12 current banks, all 60 options, all 48 distractors and all 12 worked solutions. Moderate/hard remain explicitly authored workload bands as described in `capabilities.json`.

`replenish.py` implements stages 8–9 through the existing database integration. It acquires the application `api.lock`, rechecks basis and distinct unseen/unreserved inventory, preserves source records, previews with deployed native validation predicates, and saves the exact basis-guarded request before submission. It holds the lock through exact-basis readback, source-preservation and attribution checks, native grading, and inventory recheck. It reuses an existing generator UUID and registers the repository-relative script path. Re-run it to recover a retained submission under its original key; receipts and verification live under `reference/replenishment/`.

The current native grading helper is local to this package at `reference/check-engine-current`. Its reproducible compiler command and dependency hashes are in `reference/native-build.json`. No scheduler or shared application code is changed.
