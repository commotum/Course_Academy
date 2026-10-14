# Determining the Dimension of the Product of Two Matrices

`../17592186100871.py` provides deterministic supported moderate/hard generators with 27/12 distinct bounded tasks. Easy remains explicitly unsupported in this package. Only changed operand dimensions create new tasks. Sources and learner history are preserved.

```
.venv/bin/python generate/scratch/17592186100871/validate.py
.venv/bin/python generate/scratch/17592186100871.py --difficulty hard --count 2 --seed 23 --format json
.venv/bin/python generate/scratch/17592186100871/replenish.py
```

API: generate(level, seed=0, template=None, parameters=None, profile=None, replay=False), plus moderate/hard wrappers. `replay=True` retains exact source prompts and solutions with the documented q-22067 solution correction and marks records evidence-only. Normal CLI output is a JSON array compatible with inventory_jobs.py. System Python reexecutes in the repository virtual environment when SymPy is absent. Parameters have exactly r,k,c and obey the complete profile domain.

Validation separates source-bank fidelity, exact mathematics, formatting and actual engine grading. Full source evidence, side-by-side variants and slot coverage remain local. `replenish.py` uses configured application contributor and EDB transport, holds api.lock over inventory/basis recheck through receipt/readback, previews installed native specs, retains exact basis-guarded requests, and verifies additive datoms, all source records, field ownership, generator registration, native grading and no-op repeat preparation. Outcome and shortages are recorded without calling unsupported bands filled.
