# Current state — 2026-10-22, author-289

Read feedback and all retained findings/history; reused completed source analysis.
Reproduced the latest failure first with job Python:
`-B checks/check_current_handoff.py` exits 1. Actual installed runner
`scripts/generator_pipeline.py:723-727` rejects the unchanged runtime before
retained regressions or sampling. Its evidence-only finding requires preservation
of runtime; no new generator defect is demonstrated.

Fresh verification: `evidence/author289-verification.json` records exact commands,
exit codes, timings, logs and unchanged runtime hashes.

- `checks/check_all.py` passes (CLI relocation/count contract, source replay,
  independent mathematics, native grading, shared delivery, stored inventory).
- `checks/check_batch_selection.py` passes, including seed 4258185931 before/after
  delivery and controlled within-family answer-role changes. Original cue: 1/5.
- `checks/check_evidence_contract.py` validates the real bundle, relocation and
  negative controls, then exits 1 because strict installed handoff still fails.
- `checks/check_render_binding.py` passes: ten complete source banks and actual-UI
  records bind to current runtime. Inspected question-001.png: readable throughout.
- Runtime, engine, runner, database, publication and other jobs were not edited.

## Next unfinished step

Apply/review `runner-fix/evidence-only-rejection.patch` in the runner repository,
then rerun strict regressions and fresh independent review. This requires editing
`scripts/generator_pipeline.py` outside the user-authorized workspace. The patch
remains uninstalled and the retained check remains failing. Repeated authoring or
changing valid generator bytes cannot repair this external design rule.
Corrected self-contained evidence root: `evidence/contract-correction`.
