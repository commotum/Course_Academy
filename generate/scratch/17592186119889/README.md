# Surface-area integrand generator

This package covers KP 17592186119889 only. `../17592186119889.py` implements seven observed moderate/hard templates and their complete five-option radio banks. All 48 declared coefficient combinations pass independent printed-math validation. Seed and bank order do not add tasks. The finite domain contains 24 distinct moderate integrands and 23 hard integrands; deduplication may reduce these further against live inventory. Easy remains an explicit unsupported capability with five questions unfilled. See `classification.md`, `template-extraction.md`, `plot-extraction.md` and `capabilities.json`.

Run from the repository root:

```sh
python3 generate/scratch/17592186119889.py --difficulty moderate --count 5 --seed 771 --format json
.venv/bin/python generate/scratch/17592186119889/validate.py
.venv/bin/python generate/scratch/17592186119889/replenish.py
.venv/bin/python generate/scratch/17592186119889/replenish.py --commit
```

The CLI falls back to the repository Python environment for SymPy. JSON previews include the fields, answers, source evidence and reproducibility metadata. `--template` and JSON `--parameters` permit exact replay; a request beyond the finite mathematical domain fails explicitly. No generated question carries a Math Academy content ID.

Validation parses the actual displayed surface, partial-derivative inputs and outputs, every determinant/minor cell and cofactor sign, cross-product vectors, every norm equality, final integral and answer bank. It checks all source banks algebraically (35/35 complete values, 7/7 complete banks), tests every declared slot value and seed/order invariance, and runs every choice through `course_academy_engine::learning::grade_field`. `reference/validation` retains the results and original/replay/variant review. All 55 checked instances produce 55 accepted and 220 rejected grader checks, with zero unresolved. The three publication candidates also receive separate validation. Source anomalies and conservative recipe interpretations are explicit in extraction.

Publication rechecks the native inventory before generation and under the application's `api.lock`. It excludes all historical presentations and current reservations through existing EDB queries and the application pool, deduplicates against all existing mathematical integrands including exhausted questions, resolves the configured `:application/ca-engine` contributor, retains exact typed EDN and request identity before submission, previews native entity validation, submits with the captured basis guard, and holds the lock through exact-basis readback. It verifies the additive datoms and original source records and leaves learner history unchanged. Registration uses the installed generator UUID and repository-relative script attributes; an existing identity is reused. No new plot assets are needed.

`reference/replenishment/basis-*/` retains preparation, preview, exact durable request, receipt, readback, inventory and verification. Recovery checks saved requests before starting new intent. The job result records supported shortages and the unsupported easy shortage separately.
