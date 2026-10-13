# Definite rational integral generator

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186068923.py --difficulty moderate --count 5 --seed 1978 --format json
.venv/bin/python generate/scratch/17592186068923/validate.py
.venv/bin/python generate/scratch/17592186068923/replenish.py
```

Moderate and hard are supported, with 30 and 40 finite mathematical tasks respectively. Easy is unsupported and its reserve remains explicit. Complete source evidence, per-choice extraction, full replay, exhaustive symbolic and actual learner grading checks, side-by-side review and exact commit requests/receipts are scoped to this KP. Replenishment is additive, checks current inventory under api.lock and retains it through submission and exact-basis readback. Source questions and history are preserved; application/ca-engine owns generated facts. No content is committed when current supported reserves already meet their rolling minima.
