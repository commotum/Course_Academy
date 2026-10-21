# Shared offline validation tools

Use these interfaces before reading or rebuilding their plumbing. None opens a
database connection. Write all inputs/results below your workspace or evidence
directory. Run tools with the job context's Python executable. Save full reports
and print summaries/failures; source interpretation, mathematical checks and
pedagogical judgments remain your responsibility.

## Publication filtering

```sh
python <repo_root>/generate/pipeline/check_delivery.py \
  --input <records.json> --source <source_file> --inventory <inventory_file> \
  --difficulty <requested_difficulty> --output <evidence_root/delivery> \
  --asset-root <generated_asset_directory> --math-root <math_root>
```

Input is an array of generated records. This calls the publisher's actual shared
`prepare_records` implementation: KP identity validation, local image normalization,
question validation, stable content identities, and inventory/within-batch deduplication.
It also enforces the runner's requested difficulty. Invalid records fail; only
duplicates are skipped. It writes `accepted.json`, `delivery.json`, and any
localized images under the output's `assets/` directory. Canonical image bytes
are read from math_root; published images and database state are never changed.
The compact report names its inputs, implementation hashes, captured basis, stage
counts and limits. Compare your own decision-case and shortcut probes on input
and accepted records; the helper does not make those judgments.

This does not exercise generator rejection/resampling, database identity collisions,
or the learner's history and weighted selection. Inspect the relevant generator
branch and `question_selection_file` as needed for those checks. Do not claim the
helper covers them. Live inventory may change after capture. No need to reread
all of generator_publish.py or rewrite its deduplication loop for every job.

## Actual learner grading

`<repo_root>/generate/runs/current/check-engine INPUT.json REPORT.json` runs the
application's native `learning::grade_field` without a database. Input is an array:

```python
# record is one complete generated record; choose responses for that case.
cases = [{"label": "independent case", "record": record, "checks": [
    {"field_index": 0, "submitted": "1/2", "expected": "accepted",
     "purpose": "independently checked equivalent notation"}
]}]
```

Pass the complete generated record as `record`. For radio/select/checkbox, use
`submitted_answer_id` with an authored choice UUID instead of `submitted`.
For checkbox fields, choose the UUID whose stored value is `true` or `false`,
as the UI does. For blank responses use a string `submitted`.
Expected outcomes are `accepted`, `rejected`, or explicitly justified `unresolved`.
`field_index` defaults to zero. The tool fails on an unexpected outcome and saves
all checked responses on success. Test plausible wrong responses and independently
chosen valid equivalents. Exact value equivalence does not satisfy an explicit
"simplest form" instruction when the submitted fraction is unreduced. The harness
source is `generate/runs/current/check-engine.rs` if a specific interface gap needs
inspection; do not replace it with a homemade grader.

## Actual UI rendering

Use `generate/pipeline/render_preview.py` as specified in the job prompt. Input
must be an array of complete generated records, not a counterfactual/report object.
For localized `accepted.json`, pass `--asset-root <delivery_output/assets>`.
Inspect its screenshots and concise `rendering.json` results; reuse the installed
runtime and browser. Rendering success does not certify math or grading.
