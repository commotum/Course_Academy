# Scalar factor generator

Run `.venv/bin/python generate/scratch/17592186096701/validate.py` to replay all 14 original banks and validate supported variants with the native learner grader.

Preview: `.venv/bin/python generate/scratch/17592186096701.py --difficulty all --seed 40 --count 2 --format json`.

The stable generator UUID is recorded in `capabilities.json`. Supported difficulties are easy and moderate, using the existing known-unit/known-multiple path and coefficient-matching method. Radio and scalar blank fields are supported. The fourteen named source profiles preserve original prompts, ordered solutions, complete banks and original parameter replay. Normal banks are explicitly authored complete operation profiles; bank/profile/seed/order changes never establish distinct mathematical questions.

Hard is unsupported for this version: the former fractional-known proposal added coordinate and arithmetic stages absent from the source backbone. Its prior code and validation evidence remain in `historical-positive-scalar-1/`. The nominal five-question hard reserve remains unfilled and must not be counted as supplied. New source evidence can reopen classification.

The generator renders Matplotlib PNGs into its own package without writing the database. `replenish.py` rechecks inventory, registers the validated generator with the configured application contributor, retains requests/receipts, and holds the application's `api.lock` through guarded submission and exact-basis readback.
