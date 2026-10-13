# Trigonometric substitution generator

Run from repository root:

```sh
.venv/bin/python generate/scratch/17592186068917.py --difficulty moderate --count 3 --seed 1941 --format json
.venv/bin/python generate/scratch/17592186068917/validate.py
.venv/bin/python generate/scratch/17592186068917/replenish.py
```

The package supports moderate and hard via a bounded positive amplitude policy. Easy remains unsupported. Source evidence, per-choice extraction, exact replay, actual grading, review and retained database requests are local to this KP. The replenisher rechecks inventory under api.lock, preserves source and history, uses application/ca-engine attribution and a basis guard, and verifies exact commit readback before reporting success. Repeated seeds never count as new content. Exhaustion of the finite domain must leave the shortage explicit.
