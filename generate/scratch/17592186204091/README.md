# Parameter equation generator

Supports easy/direct and moderate/scaled cancellation with one numeric blank. `validation.json` records exact replay of the five complete source banks, independent checks of rendered mathematics and each algebra step, parameter boundaries, conservative distinctness, and actual learner grading. `review.md` places exact source replays beside changed-parameter examples. The incomplete legacy source and hard level are explicit exceptions in `capabilities.json`.

```sh
.venv/bin/python generate/scratch/17592186204091/validate.py
python3 generate/scratch/17592186204091.py --difficulty easy --count 5 --seed 811 --format json
python3 generate/scratch/17592186204091.py --difficulty moderate --count 5 --seed 811 --format json
.venv/bin/python generate/scratch/17592186204091/replenish.py
```

Each level has 18 distinct roots; seed, variable naming, changed unequal constants and choice identities cannot inflate that count. Replenishment rechecks native inventory and conservative available task counts while holding `.local/learning/requests/math/api.lock` through submission and exact-basis readback. It uses existing EDB integration, deployed validation specs and configured contributor `:application/ca-engine`. Registration retains an existing generator UUID; only this KP's missing supported content is added. Requests, previews, basis guards, receipts, datom scope checks, unchanged source verification, repeat preparation and post-commit inventory live in `reference/replenishment/`. No source or learner history is changed.
