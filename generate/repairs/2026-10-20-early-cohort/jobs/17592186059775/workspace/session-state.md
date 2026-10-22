# Current state — 2026-10-22, author-35

Read feedback, retained finding requests and history, prior state, required
classification/extraction/generator/validation docs and instructional account.
First reproduction: job Python -B checks/check_current_handoff.py, exit 1.
Installed runner rejects the unchanged package before retained checks or sampling.

No runtime, manifest, regression or instructional-account changes were justified
by the evidence-only finding. Every runtime and manifest hash matches author34.
Preserved all completed generator repairs and prior source/math/rendering/inventory
evidence. No outside-workspace writes, database writes or publication occurred.

Fresh affected checks (job Python, -B):
- checks/check_evidence_contract.py: exit 1. Real evidence bundle validation,
  two relocation controls, missing-provenance/wrong-root controls, current
  raw/delivered records, 12 source captures and 3 affected generated records pass;
  strict installed-runner handoff remains failing.
- checks/check_batch_selection.py: exit 0. Exact reported seed shortcut scores
  1/5 raw and delivered; all ten profiles and 25 native responses pass.
- checks/check_cli_contract.py: exit 0. Relocated CLI counts and finite limit pass.
- checks/check_runner_handoff.py: exit 0. Existing proposed patch passes 23
  offline cases using a disposable checkout; installed runner remains unchanged.

Commands, results, logs and runtime hashes: evidence/author35-verification.json.
Regression registration: repair-regressions.json. Strict current result:
evidence/current-handoff-regression.json. No unrelated samples/renders repeated.

Status: unsupported because the installed handoff remains unresolved. The next
necessary action belongs to the runner owner: correct evidence-only routing
outside this workspace, then rerun the strict installed handoff and fresh review.
The concrete tested proposal is runner-fix/evidence-only-rejection.patch;
it remains uninstalled. Do not change runtime merely to alter its hash or
weaken the failing regression. Historical accepted evidence is not new approval.
