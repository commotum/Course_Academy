# Current state — author-340

Read feedback and both retained findings in repair-history.json; reused the existing instructional account, source analysis, candidate and executable regressions. Inspected all 12 supplied source questions, the lesson, canonical example and prerequisite context. No runtime, manifest, engine, runner, publication, database or other-job changes.

Exact latest failure reproduced first:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/check_current_handoff.py`
Exit 1: installed `scripts/generator_pipeline.py:723` rejects the unchanged package before regressions and sampling. The retained evidence-only finding explicitly requires runtime preservation.

Ran the registered regressions once and checked retained UI binding:
- `checks/check_all.py`: exit 0 (CLI/relocation, source banks, independent math, native grading, shared delivery and captured inventory).
- `checks/check_batch_selection.py`: exit 0 (historical seed 4258185931, controlled target roles, delivery and native grading).
- `checks/check_evidence_contract.py`: exit 1. Evidence bundle, relocation and negative controls pass; installed runner handoff fails.
- `checks/check_render_binding.py`: exit 0. Reinspected `evidence/author8-render/question-001.png`; readable matrices, controls and elimination steps. No new render was needed for unchanged records.

Commands, results, logs and unchanged runtime hashes: `evidence/current-author-verification.json`.

Unfinished: the external runner must resolve its evidence-only/unchanged-package gate and route this preserved candidate to fresh independent review. Existing proposal: `runner-fix/evidence-only-rejection.patch`. The corrected evidence bundle remains at `evidence/contract-correction`, with root-relative reports and three reproduced affected stored generated records. Neither the runner correction nor installation at the runner-owned evidence root is writable within this task. Strict failing regression remains registered. Do not alter generator bytes simply to evade the gate; do not treat a staged patch or historical accepted report as current approval.
