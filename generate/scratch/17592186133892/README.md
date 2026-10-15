# Line integrals with respect to y — KP 17592186133892

Run using the repository Python environment:

```
.venv/bin/python generate/scratch/17592186133892.py --difficulty easy --count 5 --seed 2722 --format json
.venv/bin/python generate/scratch/17592186133892/validate.py
.venv/bin/python generate/scratch/17592186133892/replenish.py
```

The public script generates 32 bounded, mathematically distinct easy tasks using eight usable source banks and four geometry scales. Moderate and hard are explicitly unsupported; see capabilities.json. Two defective original banks are retained as evidence and never sampled. Source-bank fidelity, calculus, whole integral option inequivalence, actual radio grading, reproducibility, domain coverage and diagrams are validated separately.

The replenishment entry point captures current native inventory and the source pool, counts only fresh validated tasks, then acquires the application's api.lock through preview, exact-request submission and exact-basis readback. At the captured inventory there are enough source questions, so it commits generator registration only. It refuses to insert future newly needed questions until content-addressed asset preparation is added to that scoped entry point; the public generator remains callable by the application's documented generation/preparation workflow. Any prior durable request is recovered identically before new work. Requests, receipts, readbacks and result are retained under reference/replenishment.
