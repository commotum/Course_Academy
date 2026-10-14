# Homogeneous ODE substitution generator

Run `./.venv/bin/python generate/scratch/17592186087886.py --difficulty easy --count 5 --seed 1 --format json`. All batches are without replacement in the bounded 42-task domain; a named `--template` has six tasks. Larger counts and unsupported levels are rejected.

Run `./.venv/bin/python generate/scratch/17592186087886/validate.py` for full source-bank replay, independent displayed-equation and worked-stage checks, all parameter boundaries and actual learner grading. `review.md` supplies side-by-side originals and variants. No new plots or assets are required.

Run `./.venv/bin/python generate/scratch/17592186087886/replenish.py` to recover retained exact requests, recheck the native inventory and current/historical learner usage under the application `api.lock`, add only shortages, preview with deployed validation predicates, commit with an explicit application contributor and basis guard, and verify at the receipt's exact basis. Evidence is retained in `reference/replenishment/`. Existing source questions and learner facts are preserved.
