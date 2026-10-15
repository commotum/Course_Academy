# Reconstructing a potential from its planar gradient

Validated easy generator: `generate/scratch/17592186124569.py`. Run from the repository root:

```bash
.venv/bin/python generate/scratch/17592186124569.py --level easy --seed 7 --count 5 --output /tmp/potential-questions.json
.venv/bin/python generate/scratch/17592186124569/validate.py
.venv/bin/python generate/scratch/17592186124569/replenish.py --prepare
.venv/bin/python generate/scratch/17592186124569/replenish.py --commit
```

Python/SymPy generate exact questions. JSON includes field-owned stable UUIDs, complete equations or the exact blank fragment, concrete worked solution, source template/profile, scale, seed, domain, dependency version and generator version. Local review Markdown compares unchanged source parameters with changed signs/scales. The validator reads the rendered field, all answer values, and all six solution stages, exhausts the 96 distinct tasks, replays all 12 supported source banks, and exercises the real application grader. It keeps the two excluded source profiles and unsupported levels visible.

Replenishment rechecks the native inventory and this KP's complete bank at one basis, excludes historical presentations and reservations, mathematically validates current usable sources, and prepares only a shortage at easy. An already sufficient pool needs registration only. All EDB writes are additive through the existing integration and configured application contributor. The application api.lock is held from the final inventory read through exact-basis receipt/readback. Exact requests, receipts, contributor checks and verification are retained under reference/replenishment. No source question or learner state is modified.
