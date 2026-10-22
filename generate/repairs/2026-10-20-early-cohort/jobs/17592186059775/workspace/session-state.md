# Current state — 2026-10-22, author-69

Feedback and repair history read first. Latest failure reproduced before other
checks with the job Python and `-B checks/check_current_handoff.py`: exit 1.
Installed `scripts/generator_pipeline.py` rejects the unchanged package at its
sample gate, before regressions or sampling. Finding 9b8cb52352b8ca3e790e asks
for evidence-only correction and runtime preservation. No new generator defect
is demonstrated. Do not change runtime bytes solely to evade this gate.

Affected checks freshly executed (job Python, `-B`):
- checks/check_evidence_contract.py: exit 1. Real bundle validation, relocation,
  negative controls, current record/source binding and three affected stored
  generated records pass; installed runner handoff alone fails.
- checks/check_batch_selection.py: exit 0. Exact seed 4258185931 scores 1/5
  for the retained pivot/rank shortcut before and after shared delivery;
  ten profiles pass controlled-role checks. Native grader: 5 accepted,
  20 rejected, no unexpected results.
- checks/check_runner_handoff.py: exit 0. Proposed external patch passes 23
  offline cases. This does not repair installed runner control flow.
- checks/check_cli_contract.py: exit 0. Runtime-only relocation, requested
  counts, determinism and explicit finite-limit failure pass.
- checks/check_render_binding.py: exit 0. Ten complete source banks replay;
  two retained UI inputs match fresh delivered records. Visually reinspected
  evidence/author8-render/question-001.png: readable, no clipping observed.

Exact commands, result paths, versions and unchanged runtime hashes are in
`evidence/current-verification.json`. Existing strict regressions remain intact.
No runtime, engine, external runner, publication, database or other-job edits.
No unrelated bulk retesting or redundant rendering was performed.

Unfinished: runner owner must apply the staged correction at
`runner-fix/evidence-only-rejection.patch` to scripts/generator_pipeline.py,
which is outside this workspace. Then rerun the actual handoff and retained
regressions before fresh independent review. The corrected report bundle is
validated at evidence/contract-correction; its installation is runner-owned.
The proposed patch remains uninstalled. Status: unsupported for this boundary,
not for the easy Gaussian-elimination skill.
