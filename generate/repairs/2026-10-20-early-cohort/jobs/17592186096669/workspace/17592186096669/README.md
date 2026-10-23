# Back substitution generator

KP 17592186096669. Run `python3 generate/scratch/17592186096669.py --difficulty easy --count 5 --seed 42 --format json`. The script uses the existing `.venv` when the worker Python lacks SymPy. Run `.venv/bin/python generate/scratch/17592186096669/validate.py` for exact source-bank replay, the complete bounded domain, rendered arithmetic checks and native learner grading. Validation output is frozen with the generator and source evidence.

Version 1 supports Easy only. Its conservative domain scales all RHSs and each complete observed answer bank by one positive integer in 1..9; all 99 mathematical systems are validated. Source banks are never pooled. Moderate and Hard are unsupported by this package. See classification.md and template-extraction.md for the restriction and source anomaly. Exceeding the remaining domain is a finite capability exception.

`.venv/bin/python generate/scratch/17592186096669/replenish.py` reuses the application's EDB integration and contributor. It captures fresh inventory under `.local/learning/requests/math/api.lock`, excludes shown/reserved and mathematically repeated questions, registers or reuses the generator UUID, previews native ensures, saves exact basis-guarded requests and recovers receipts before dependent work. The lock is retained through submission/readback. Evidence lives under reference/replenishment/.

This classify job found nine fresh validated Easy questions, already above the target of five. Only the generator registration was committed; all generated previews remain local. The incomplete unrated q-20451, every source question, canonical example, other KPs and learner history are preserved.
