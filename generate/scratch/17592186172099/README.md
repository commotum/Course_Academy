# Flux inventory generator

Run from the repository with `.venv/bin/python generate/scratch/17592186172099.py --difficulty moderate --seed 1 --count 2 --format json`. Explicit template/scale preview: `--template q-126817 --scale 7`. Validated supported difficulties are moderate and hard. Easy is unsupported; see capabilities.json.

`validate.py` checks source banks, printed mathematics, independent boundary flux, deterministic replay and declared slot coverage. `engine-input.json`/`engine-report.json` exercise the application's actual `learning::grade_field`. `replenish.py` rechecks current native inventory and exact KP membership, excludes seen/reserved questions including history, validates current questions, deduplicates by mathematics, and prepares only needed additive content. It registers the stable generator UUID, holds the application's api.lock from fresh basis through submission and exact-basis readback, and saves exact request/receipts under reference/replenishment. Source evidence and canonical examples are never changed.

See classification.md, template-extraction.md, plot-extraction.md, bank-mapping.json, review.json, validation.json and freeze.json for the evidence and bounded capability exception. Math parser is a scoped copy of the existing fail-closed elementary parser; no shared application code is changed.
