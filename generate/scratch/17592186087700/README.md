# Determining the Inverse of a Larger Matrix

Validated generator: `../17592186087700.py`, version 1.0.0. Reuses the frozen draft's source extraction and corrects only generated solution defects. Source questions remain untouched.

Supported levels: moderate (3×3, 204 finite tasks) and hard (4×4, 288 finite tasks). Each question retains three independent Boolean fields and direct verification by multiplication. Signed simultaneous coordinate permutations preserve the source dimensions, sparsity, arithmetic magnitudes, product stages and statement roles. These are workload-preserving classifications, not empirical calibration.

Easy is unsupported in this package. No source practice has an easy rating. The original draft's one-field shear experiment changes the source backbone; it is not published. Its five-question reserve remains explicitly unmet. New source evidence can reopen this decision.

Run `.venv/bin/python generate/scratch/17592186087700.py --difficulty hard --count 5 --seed 123 --format json`. The Python API is `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)`. The raw-source profile is evidence-only; only observed-profile records with `eligible_for_learning=true` may be published. `all` means supported levels only. The batch sampler deduplicates complete actual matrices and relation roles, and rejects requests beyond the finite capacity.

Validation: `validate.py` replays all 13 source banks (78/78 choices), checks every distinct finite task with exact arithmetic, verifies target/witness consistency, negative controls and native Boolean grading. `render.py` uses the current player's Markdown, MathJax and checkbox UI. Run it with Node 22 on PATH. No plots or image assets are needed by these questions.

`replenish.py` is scoped to this KP and job. It uses the existing EDB integration, rechecks never-shown/unreserved mathematically validated inventory, deduplicates against all existing source/generated tasks, reuses generator identity, records exact requests, and holds the application's `api.lock` through preview, basis-guarded submission and exact-basis readback. It publishes only visually reviewed candidates. It excludes three source solutions with mathematical/reference defects when counting usable inventory without modifying them. Durable transaction evidence is under `reference/replenishment/`; `validation-freeze.json` records the tested inputs.
