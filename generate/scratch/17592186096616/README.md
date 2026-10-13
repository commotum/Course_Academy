# Logarithmic tangent-slope inventory package

The script is `generate/scratch/17592186096616.py`. Its stable generator UUID is derived from the existing KP UUID. The package supports easy questions only; moderate and hard retain explicit nominal shortages and a bounded capability exception in `capabilities.json`.

```bash
.venv/bin/python generate/scratch/17592186096616.py --difficulty easy --count 5 --seed 23 --format json
.venv/bin/python generate/scratch/17592186096616/validate.py
.venv/bin/python generate/scratch/17592186096616/replenish.py
```

Validation independently reads displayed functions, answer banks and each worked-solution row; replays every complete original bank; tests seed/identity behavior, domain boundaries and unsupported bands; and invokes the real application grader. Formula notation is standardized. Literal source content and all source anomalies are retained with explicit repair descriptions. Native grading requires canonical/equivalent accepted entries and wrong entries rejected, with zero unresolved checks. No plots are needed.

`replenish.py` reuses the project's EDB integration and deployed preview predicates. Under the application's `api.lock`, it captures inventory/basis, rechecks source evidence, counts distinct validated unseen/unreserved easy tasks, validates supplied/local records, checks global UUID collisions, and prepares only the shortage. It preserves every existing question and canonical example. It registers the generator through the installed UUID/script attributes and existing KP ref, with the configured application contributor. It retains exact EDN and a durable basis-guarded request before submission, verifies the actual receipt and all scoped content at its exact commit basis, checks that no learner or unrelated content datoms changed, and rechecks inventory while holding the lock.

A confirmed receipt is recovered before new intent. A no-op is recorded without another transaction. Successful registration can add zero questions when existing easy inventory already meets the five-task reserve. Higher bands are never marked filled.

The job outcome is written to the requested `.result` file; `reference/replenishment/basis-*/` retains the complete preparation, preview, request, receipt, grading checks, source snapshots and verified readback. The generator's mathematical capacity is bounded by its declared sampling policy; exact exhaustive capacity is not claimed.
