# Parametric arc-length integral generator

Run from the repository with `.venv/bin/python generate/scratch/17592186092375.py --difficulty easy --count 5 --seed 42 --format json`. SymPy 1.14 is required; the application uses its configured Python environment. Validate with `.venv/bin/python generate/scratch/17592186092375/validate.py`.

Easy only. There are 126 validated bounded endpoint variants across five nonplot profiles. Illustrated profiles support source replay only. Moderate and hard are unsupported; their nominal five-question reserves remain unfilled. Source evidence can reopen these restrictions. Seeds and identity changes do not add variants. Output stores stable field-owned UUIDs and complete solutions, retaining provenance separately from content.

See classification.json, template-extraction.md, choice-recipes.json, plot-extraction.json, source-replay.json, source-issues.json, slot-coverage.json, native-grading.json, validation.json and review.md. Registration and any replenishment requests/receipts/readback are retained under reference/replenishment. Original source and learner facts must remain unchanged. Current inventory is always rechecked under the application's api.lock before committing.
