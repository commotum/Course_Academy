# No-solution equation generator

The script supports easy only, with three observed checkbox layouts and no plots. The two legacy source questions remain unrated. Moderate/hard capability exceptions are recorded in `capabilities.json`.

```sh
.venv/bin/python generate/scratch/17592186204089/validate.py
python3 generate/scratch/17592186204089.py --difficulty easy --count 5 --seed 811 --format json
.venv/bin/python generate/scratch/17592186204089/replenish.py
```

The CLI uses the existing repository virtual environment if the caller lacks SymPy. It emits the instance list expected by the inventory worker. `review.md` contains exact originals and fixed worked variants. `validation.json` separates full source-bank coverage, independent algebra, distinctness and actual engine grading.

Replenishment uses the existing database integration and contributor `:application/ca-engine`. It acquires the application `api.lock`, captures fresh native inventory, checks source stability, excludes already shown/reserved and canonical questions, and commits only any genuine shortage. A generator-only registration is sufficient when the existing fresh easy bank meets the quota. Exact EDN, durable request, basis guard, speculative preview, receipt and exact-basis verification are retained under `reference/replenishment/`. Source questions, answer identities and learner history are never changed.
