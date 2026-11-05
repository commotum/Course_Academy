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
Any unresolved outcome produces a failed report and nonzero exit, even when expected;
record it as a limitation and resolve it before acceptance. An accepted review needs
substantive accepted and rejected coverage.
`field_index` defaults to zero. The tool rejects empty coverage, fails on an unexpected outcome and saves
checked responses with input/record fingerprints and runtime identity. Keep the
recognized report intact so review can bind its checks to actual final records. Test plausible wrong responses and independently
chosen valid equivalents. Exact value equivalence does not satisfy an explicit
"simplest form" instruction when the submitted fraction is unreduced. The harness
source is `generate/runs/current/check-engine.rs` if a specific interface gap needs
inspection; do not replace it with a homemade grader.

## Actual UI rendering

```sh
python3 <repo_root>/generate/pipeline/render_preview.py \
  --input <records.json> --output <evidence_root/render> \
  --asset-root <generated_asset_directory> --math-root <math_root> \
  --state both --viewport 1280x1000
```

Input is an array of complete generated records, not counterfactual/report objects.
For localized `accepted.json`, use `--asset-root <delivery_output/assets>`.
`--state active|completed|both` selects unanswered questions, completed solutions,
or both (default). Repeat `--viewport WIDTHxHEIGHT` for a relevant narrow layout.
Use `--indices` with comma-separated zero-based indices for representative coverage;
`--limit` is an optional explicit cap; without selection/capping all supplied records are rendered. Omitted inputs are recorded. Supply a bounded representative input or indices rather than an entire inventory. Select materially
different task/support/response layouts rather than relying on the first records.

Inspect screenshots, open dropdown content and `rendering.json`; the helper uses
the actual unmodified UI, installed browser, MathJax and image decoding. Successful
DOM/typesetting checks do not establish readability, correct cells or absence of
answer-revealing prompt/choice annotations. Active and completed states support
different claims. Keep recognized reports and record fingerprints intact; cite
reports for actual final raw or delivered records. Rendering cannot certify math
or grading.

## Shared repository repairs

For a shared repository repair, stage a unified diff against the current files under your own workspace without first applying it to the shared tree. Run the argv in `shared_repair_command` from context with `--patch <workspace/repair.patch>` and one or more `--check-json '["executable","argument",...]'` options. The helper serializes the shared edit and its regression commands and reverses your patch if a check fails. It also restores the previous native grader binary; list any other rebuilt output with repeated `--artifact <repo-relative-path>` options so those files are restored on failure too. Resolve any patch conflict yourself by reading the current files, updating the patch, and retrying the relevant checks. Keep ownership of the repair; do not create another handoff. This coordination is only for shared code such as the renderer or engine. Edit your own KP package and evidence directly.

For engine changes, reproduce a valid-response rejection or wrong-response
acceptance in the native grader, repair the actual rule and retain acceptance and
rejection regressions. Rebuild the harness used here before rerunning. Never
special-case a question, bypass grading or restart live services. Apply equivalent
failure-preserving checks to renderer, delivery or packaging rules.

## Evidence and report validation

Save full inputs, recognized tool reports and reproducible commands under the
workspace/evidence root; print summaries and failures. Accepted review evidence
must identify final records actually tested. Native grading needs nonempty positive
and negative coverage. Each final band cites its matching delivery report plus
recognized grader and render reports for raw or delivered records. Representative
checks are allowed; the verifier still accounts for all material families and
limitations. Report status and file existence alone do not establish those claims.

Keep the initial `source-analysis.json` unchanged. Conceptual amendments belong in
`source-analysis-amendments.json`, using the reviewer prompt’s schema and linking
the initial hash to the final substantive account. `solution-paths.json` needs a
conversion negative control only for cases with a necessary conversion; unrelated
CAS/trig examples are not required for direct answers.

After finalizing and inspecting the actual candidate, validate the report:

```sh
python3 <repo_root>/scripts/generator_review.py \
  --result <evidence_root>/final-result.json --evidence-root <evidence_root>
```

Correct evidence/report errors in the same verifier session. Reuse unaffected
checks and expand samples only for a demonstrated gap. Do not relabel an unresolved
valid response or unexamined applicable stage as passed to satisfy the contract.

## Retained findings and supersession

Ordinary author repair maps findings to executable checks in
`workspace/repair-regressions.json`:

```json
{"findings":[{"id":"retained-finding-id","script":"checks/regression.py","args":[]}]}
```

Each script exits nonzero when the demonstrated defect persists in current visible
records, and zero only after checking the intended behavior. A script may cover
several findings. Retain old counterexamples; use independent mathematical or
structural witnesses rather than copied expected results.

If the verifier proves a retained requirement mistaken or superseded, it may write
`evidence_root/finding-dispositions.json` (otherwise no such file is needed):

```json
{
  "format": "course-academy-finding-dispositions-v1",
  "findings": [{
    "id": "retained-finding-id",
    "disposition": "superseded",
    "reason": "Concrete source/instructional reason the old rule is inappropriate",
    "source_refs": ["specific source identity or passage"],
    "evidence_paths": ["supersession-evidence.json"],
    "counterexample_path": "valid-case-excluded-by-old-rule.json"
  }]
}
```

Paths name nonempty evidence-root-relative files. Preserve the original history
and a valid counterexample the old rule would exclude. Finalization validates
known finding IDs and evidence, binds this file and skips only the superseded
executable obligation. An accepted review cites `finding-dispositions.json` in
`checks.scope.evidence_paths`. This does not waive an unresolved actual defect or
replace the conceptual source-account amendment when the interpretation changed.
