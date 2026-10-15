# Two-variable vector chain rule generator

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186124469/validate.py
.venv/bin/python generate/scratch/17592186124469.py --difficulty all --seed 31 --count 2 --format markdown
```

The API exposes `generate_easy`, `generate_moderate`, `generate_hard`, and `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)`. Use the profiles in `source-cases.json` for complete original replay (`observed`, and `raw_observed` for q-95056); normal defaults use the separately authored operation bank. Records are local review JSON with field-owned UUIDs, colon-key inner schema and plain-key outer knowledge point. No database writes.

Six source banks and five full source solutions are preserved. q-95056 lacks source difficulty/correct designation/solution; an easy label, mathematical designation and complete solution are separately authored. Moderate and hard are missing-source extensions within the same two-variable symbolic derivative scope; see classification for mandatory workload bounds. Plots: none. Validation reads actual printed functions, coordinate arguments, every evaluated vector/scalar stage and every displayed option independently, then invokes the real native radio grader for every owned choice. There are no blank fields in this KP.

`raw_observed` is public parameterized evidence for q-95056: it preserves absent difficulty, solution and correct designation and marks the record evidence-only/ineligible for practice. A separate `observed` completion preserves its bank while adding the independently derived designation and authored solution/easy level. The raw evidence cannot grade as a practice fixture because its original designation is absent.

Observed expression-pattern replay and raw omission profiles carry `evidence_only: true` and `eligible_for_learning: false`; authored method banks are eligible for practice.

## Inventory replenishment

The frozen generator is now used through this KP's `replenish.py`, which prepares only current shortages and commits through the configured EDB integration. Run `.venv/bin/python generate/scratch/17592186124469/replenish.py`, then the same command with `--commit`. The commit phase obtains the application's `api.lock`, rechecks current inventory and basis, previews native specs, saves the exact request, submits under a basis guard, and retains its receipt and readback. Existing registration identity is reused; `capabilities.json` records the UUID and repository-relative script path. No source questions or learner facts are changed.

See [the refreshed classification](reference/current-classification.md) for twelve current source questions, the distinction between classified sources and supported generator families, and the conservatively excluded radical-product source solution. The old basis-1356 snapshot and its exact source-replay evidence remain intact. `reference/replenishment/` retains current reads, distinct generated instances, all native grading checks, preparation, exact EDN, request, preview, receipt, and verification.
