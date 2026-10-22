# Current state — 2026-10-22, author-145

Read latest feedback and repair history (2 findings, 145 events); reproduced the
latest installed-runner rejection before validation. Preserved runtime, manifest,
instructional account, registered regressions and staged runner patch. No runtime
change is justified by the evidence-only finding.

Fresh commands, exit codes, logs and unchanged runtime hashes:
`evidence/author145-verification.json`. Commands used the pinned job Python.

- `checks/check_current_handoff.py`: exit 1; actual installed runner rejects the
  identical package before retained regressions or sampling.
- `checks/check_evidence_contract.py`: exit 1 overall. Corrected bundle validation,
  two relocations, missing-provenance/wrong-root negative controls, current-record
  binding, 12 source captures and 3 generated inventory records pass. Installed
  runner gate remains the failure.
- `checks/check_batch_selection.py`: exit 0; seed 4258185931 shortcut scores 1/5
  raw and delivered; 5 accepted, 0 duplicates; 10 profiles checked; 25 native
  responses pass (5 accepted, 20 rejected).
- `checks/check_render_binding.py`: exit 0; 10 source banks / 50 choices replay;
  two retained actual-UI endpoints match fresh delivery. Visually re-inspected
  `evidence/author8-render/question-002.png`: matrices, controls and full solution
  are readable. No new render claimed.

All six runtime/manifest file hashes remain unchanged; package digest remains
`38c685ce1e5bd4f89ac79b6ab3d31a4a81f2b77c9f4bb6f0abcab5c20640f626`.
No publication, database writes, engine changes or external runner edits.

Unresolved root cause: `scripts/generator_pipeline.py:725` demands changed runtime
bytes although finding 9b8cb52352b8ca3e790e requires an evidence-only correction
preserving the package. `runner-fix/evidence-only-rejection.patch` is uninstalled.
Its retained 23 offline cases are not fresh results or an installed fix.

Next unfinished step requires the runner owner to review/apply that correction
outside this workspace, then run retained checks, sampling and fresh independent
review. Repeating authoring cannot repair the external gate. Keep strict checks
failing until installed behavior changes; do not alter package bytes to evade it.
Status is unsupported for this handoff, not for the easy instructional family.
Live learner history and later inventory remain untested.
