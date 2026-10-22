# Current state — 2026-10-22, author-75

Feedback and repair history read first, including both retained findings and
repeated runner limitations through attempt 74. Completed runtime repairs and
strict regression registrations preserved. No new generator defect demonstrated.

Exact latest failure reproduced before other checks:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/check_current_handoff.py`
exits 1. Installed `scripts/generator_pipeline.py:723` rejects the byte-identical
package before regressions or sampling. Package hash remains
`38c685ce1e5bd4f89ac79b6ab3d31a4a81f2b77c9f4bb6f0abcab5c20640f626`.
Finding `9b8cb52352b8ca3e790e` requires evidence-only correction and runtime
preservation. Changing package bytes merely to evade the gate is not a repair.

Fresh commands, exits, logs and runtime hashes: `evidence/author75-verification.json`.

- `checks/check_evidence_contract.py`: exit 1. Actual review validator accepts
  the corrected bundle and relocated copies. Wrong-root and missing-provenance
  controls reject; 12 source captures and three stored generated records bind.
  Installed runner handoff is the remaining failure.
- `checks/check_batch_selection.py`: exit 0. Exact seed 4258185931 shortcut
  scores 1/5 both raw and delivered; all five survive actual delivery. Ten
  profiles retain controlled target banks. Native grader accepts five keys and
  rejects twenty distractors.
- `checks/check_cli_contract.py`: exit 0. Runtime relocation, exact counts,
  deterministic replay and finite-limit rejection pass.
- `checks/check_render_binding.py`: exit 0. Ten complete source banks replay;
  retained actual-UI endpoints bind to current delivered records. Reinspected
  `evidence/author8-render/question-001.png`: readable prompt, matrix options
  and full elimination solution.

No runtime, engine, external runner, database, publication or other-job edits.
No repeated broad audit or rerun of the unchanged proposed external patch.

Unfinished: the runner owner must resolve the identical-package gate and install
the corrected evidence bundle. `runner-fix/evidence-only-rejection.patch` is
already staged and remains uninstalled. Its target is outside the authorized
workspace. `evidence/contract-installation.json` inventories the complete bundle
at `evidence/contract-correction` with a runner-supplied destination contract.
Historical acceptance is not fresh approval. Strict handoff/regression failure
is retained; status remains unsupported because of this infrastructure blocker,
not because source support or the easy generator is absent.

Author-75 validation milestone: reran exact installed handoff failure first,
then evidence contract, exact batch shortcut/delivery/native grading, small
relocated CLI sample, and source/render binding. Results remain as above.
Runtime hashes equal author-74. The corrected evidence bundle validates, but
the registered strict evidence regression still exits 1 on installed handoff.
No implementation change is justified by this evidence-only finding. Do not
weaken the check or change runtime merely to evade the external package gate.
No broad audit repeated. External fix and evidence installation remain undone.
