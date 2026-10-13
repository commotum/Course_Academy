# Particular first-order solutions

Generator for knowledge point 17592186096699. The source snapshot is from math basis 1356; the inventory package rechecks it against the current immutable lineage before preparing additive content. The earlier frozen manifest records the step-7 review. `inventory-validation.json` records the current executable, dependency and grader validation; the only generator runtime change is selecting the existing project Python environment when system Python lacks SymPy.

```sh
.venv/bin/python generate/scratch/17592186096699/validate.py
.venv/bin/python generate/scratch/17592186096699/inventory_validation.py
python3 generate/scratch/17592186096699.py --difficulty moderate --count 3 --seed 7 --format json
.venv/bin/python generate/scratch/17592186096699/replenish.py --prepare-only
.venv/bin/python generate/scratch/17592186096699/replenish.py
```

Supports easy, moderate and explicitly authored hard workloads: respectively elementary, polynomial/exponential, and polynomial/exponential/trigonometric direct integration with one initial condition. Hard is an authored extension, not an observed source difficulty. Signed integer coefficients, bounded targets and elementary evaluation inputs control workload. No plots or assets are needed. The normal generator exposes blank and radio fields. Observed raw/repaired profiles are replay evidence only and cannot be committed by replenishment.

All fourteen original banks replay completely; original missing attributes and teaching errors are retained. Two incomplete sources and two sources with documented solution errors are excluded from validated inventory. New records use the authored operation bank and undergo independent checks of the displayed ODE, initial condition, answer values and solution rows. Current application grading checks canonical and equivalent blanks, wrong entries, and every owned radio selection. Mathematical task fingerprints ignore seed, choice order, function-name aliases and response shape.

Replenishment rechecks inventory under `.local/learning/requests/math/api.lock`, prepares native ensured EDN, uses the configured `:application/ca-engine` contributor and exact basis guard, and holds the lock through submission and exact-basis readback. It reuses an existing registered generator UUID or the package's stable UUID, and registers the repository-relative script. Exact requests, previews, receipts, source-preservation checks and inventory readback are retained in `reference/replenishment/`. Saved unknown submissions are recovered before new work. No source questions, learner history, scheduler or other knowledge points are modified.
