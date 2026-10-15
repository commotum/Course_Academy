# Cartesian surface-integral setup generator

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186105889/validate.py
.venv/bin/python generate/scratch/17592186105889.py --difficulty all --seed 42 --count 2 --format json
.venv/bin/python generate/scratch/17592186105889.py --difficulty easy --profile raw:q-161323 --count 1
```

The API exposes `generate`, `generate_easy`, `generate_moderate` and `generate_hard`. All responses are five-choice radio integrand fragments. Explicit parameters use exact scalar strings and four ordered integer bounds; validation rejects unsupported shapes and out-of-workload values without resampling. Raw profiles preserve historical strings and missing attributes through reusable masks and scalar-scaled expression recipes; they are ineligible for learner defaults. Every raw profile holds its surface fixed and varies the coefficient of f and the rectangle. Default families vary surface and scalar coefficients.

`classification.md`, `template-extraction.md`, `plot-spec.md`, `source-cases.json`, `review.md`/`review.json` and `validation.json` provide steps 3–7 evidence. `engine-report.json` uses the unchanged native learning grader with in-memory fixtures. No registration, database reads/writes, engine changes or image generation occurs. Raw bank fidelity, mathematical correctness and native grading are distinct measures. Moderate/hard are documented authored scope claims, not observed source labels. The unrated original has no historical correct designation; its authored completion infers the correct integrand independently.

## Inventory replenishment

Registered generator `40acf4e9-694c-5e02-a520-e7496771b14c` at verified math basis 2514 through `:application/ca-engine`. `replenish.py` retains exact EDN requests, preview, receipt, and readback in `reference/replenishment/basis-2513/`. It added one easy, five moderate, and five hard tasks, yielding five fresh mathematically validated tasks per band. Four unusable historical sources remain unchanged and excluded from validated counts. `capabilities.json` records the finite catalog and supported levels. The adapter holds `api.lock` from current-basis reads through submission and verification, reuses a saved exact request on recovery, and uses the current application grader fixture in `reference/`.
