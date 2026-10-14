# Already-isolated perfect square: negative linear term

Script: `../17592186068874.py`. Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186068874/validate.py
.venv/bin/python generate/scratch/17592186068874.py --difficulty all --seed 4 --count 2 --format json
.venv/bin/python generate/scratch/17592186068874.py --difficulty moderate --profile raw_q-140283 --format markdown
```

`generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and easy/moderate/hard entrypoints accept exact integer parameters `a,b,c,variable`. Field type selectors choose eligible families before sampling. Raw profiles preserve individually absent source ratings, solutions, banks and keys; every raw record is evidence-only and ineligible for learning. Normal completions and level extensions are authored, using method-based banks. Opaque adjacent offsets stay outside defaults.

Easy uses monic isolated identities with a=2..9. Moderate uses a=10..15 (observed a=11). Hard uses coprime a=2..9 and b=2..5 in `(b²v²−2abv+a²)±c`, an authored application of the prerequisite perfect-square identity to a nonunit variable factor (the inspected prerequisite itself has no nonunit-leading example). Outer constants have nonzero integer magnitude 1..12. All three retain the negative linear term and already-isolated parentheses. No insertion of a squared constant, add-to-both-sides operation, or equation solving occurs.

The validator compares full source fields/presence, exact prompt and complete worked-solution strings, all complete expression options, every printed arithmetic row and required operative stage, identity/alias behavior, all field types/families/banks, explicit parameter bounds, default coverage, and native grading. It tests sign, stage-removal and C0 mutations. Source key omissions are counted separately from inferred completions. Native engine executable hash/runtime versions are recorded. Artifacts are local review JSON, not transaction data. No DB writes, registration, commits or shared edits.
