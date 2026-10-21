# Consistent systems by Gauss–Jordan elimination

Script: ../17592186115241.py. Original evidence: math basis 1356. Current source refresh and inventory evidence are under `reference/replenishment/`.

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186115241.py --difficulty all --seed 23 --count 2 --format json
.venv/bin/python generate/scratch/17592186115241.py --difficulty easy --profile q-131715 --seed 23
.venv/bin/python generate/scratch/17592186115241/validate.py
```

Eight observed layout families / eleven complete radio banks, 9 observed easy plus 2 unrated assigned authored easy. Original fidelity uses scale=1 and zero offsets through the normal parameterized generator. Normal easy/moderate/hard output uses clearly authored complete operation-error banks and coefficient sampling; moderate/hard scope is explicitly authored from the NxM lesson route and RREF prerequisite. Workloads are 2, 6, 9 elementary row operations. All outputs solve consistent systems; none asks for parameter-consistency or system classification. Every level has at least two examples in review.md/review.json.

validation.json separates 55 matched source values / 11 banks, 9 available correct designations, 2 independently derived missing designations, and 9 available full solution prose/stage matches. Missing source designation/solution evidence is retained in original-widgets.json and never counted as exact matches. Printed mathematics, native radio grading, identities, bounds and option banks are validated independently. Mathematical notation and unclosed-brace presentation repairs are explicit; source.json is unchanged. Plot rating none; inspected canonical assets are mathematical typesetting.


Replenishment refresh (2026-10-15): current source capture at math basis 2701
retains the same eleven complete mathematical banks (55 values). Ten sources
now have a correct designation and an independently checked worked solution;
q-42040 was completed since the original capture. q-32234 remains unrated and
incomplete and is excluded from usable inventory. Source questions are retained
unchanged. Matrix/system formatting changes do not create new templates.

The full existing validation was rerun (407 records); the current application
grader independently passed 61 accepted and 244 rejected submissions, and all
ten complete current sources passed all 50 radio submissions. Current source
capture, bank replay and native build hashes are retained under
`reference/replenishment/initial/` and `reference/replenishment/native-build.json`.

Run `.venv/bin/python generate/scratch/17592186115241/replenish.py` to recheck
inventory and add only missing distinct tasks, or use `--prepare-only` to retain
validated local output without preview/submission. The script holds the app's
`api.lock` through fresh inventory, source and identity checks, guarded submission
and exact-basis readback. It retains exact intent/EDN/receipts, registers a stable
UUID and this repository-relative generator path, and verifies unchanged source
content and scoped additive datoms. Repeated solution spaces are rejected using
nonzero canonical RREF rows, irrespective of row mixing/scaling, redundant rows,
profile, seed, UUID or option order. `capabilities.json` records level scope.
