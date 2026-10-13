# Cartesian surface-integral setup generator

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186105889/validate.py
.venv/bin/python generate/scratch/17592186105889.py --difficulty all --seed 42 --count 2 --format json
.venv/bin/python generate/scratch/17592186105889.py --difficulty easy --profile raw:q-161323 --count 1
```

The API exposes `generate`, `generate_easy`, `generate_moderate` and `generate_hard`. All responses are five-choice radio integrand fragments. Explicit parameters use exact scalar strings and four ordered integer bounds; validation rejects unsupported shapes and out-of-workload values without resampling. Raw profiles preserve historical strings and missing attributes through reusable masks and scalar-scaled expression recipes; they are ineligible for learner defaults. Every raw profile holds its surface fixed and varies the coefficient of f and the rectangle. Default families vary surface and scalar coefficients.

`classification.md`, `template-extraction.md`, `plot-spec.md`, `source-cases.json`, `review.md`/`review.json` and `validation.json` provide steps 3–7 evidence. `engine-report.json` uses the unchanged native learning grader with in-memory fixtures. No registration, database reads/writes, engine changes or image generation occurs. Raw bank fidelity, mathematical correctness and native grading are distinct measures. Moderate/hard are documented authored scope claims, not observed source labels. The unrated original has no historical correct designation; its authored completion infers the correct integrand independently.
