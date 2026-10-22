# Current state — 2026-10-22, author-40

Read feedback, both retained findings, history event summaries, and prior state.
First reproduced latest failure with job Python -B checks/check_current_handoff.py:
exit 1. Installed scripts/generator_pipeline.py:723–727 rejects identical package,
source and engine identities before retained regressions or sampling, including
when the independent finding requests only evidence correction.

Targeted commands, exits, logs and unchanged runtime hashes:
evidence/current-verification.json.

- checks/check_evidence_contract.py: exit 1. Bundle validation, relocation,
  missing-provenance and wrong-root controls pass; installed handoff still fails.
- checks/check_batch_selection.py: exit 0. Exact reported seed shortcut 1/5 raw
  and delivered; actual shared delivery accepts 5/5, ten profiles checked and
  25 native acceptance/rejection submissions pass.
- checks/check_cli_contract.py: exit 0. Relocated CLI/count/determinism and finite
  limits pass.
- checks/check_render_binding.py: exit 0. Ten complete source banks replay;
  retained actual-UI records equal current delivered endpoints. Visually inspected
  evidence/author8-render/question-001.png: readable matrices, five choices and
  complete elimination stages, without clipping or raw TeX.
- checks/check_runner_handoff.py: exit 0. Existing proposed external patch
  applies to a disposable checkout and passes 23 offline cases. It remains
  uninstalled; this result does not resolve the failing installed-runner check.

No runtime or manifest changes, source changes, publication, database, engine,
runner or other-job writes. Preserve completed repairs, instructional account and
repair-regressions.json. Corrected evidence at evidence/contract-correction is
historical review evidence, not fresh independent approval.

Unfinished external action: repair the runner's evidence-only rejection rule
(existing reviewable proposal: runner-fix/evidence-only-rejection.patch), then
rerun strict installed-runner regression and fresh independent review. Proposal
remains uninstalled. Workspace-only authorization prevents the runner change.
Do not alter generator bytes merely to evade the identity gate, weaken the
failing check, or repeat unrelated sampling. Status remains unsupported because
handoff is unresolved; the source-supported easy skill is preserved.
