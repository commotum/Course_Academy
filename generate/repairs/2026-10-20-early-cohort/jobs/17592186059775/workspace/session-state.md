# Current state — 2026-10-22, author-241

Preserved the repaired generator, manifest, source banks, instructional account,
registered regressions and existing staged runner patch. No runtime change is
justified by the latest evidence-only feedback.

First reproduced the exact latest failure:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/check_current_handoff.py`
Exit 1: installed runner rejects the unchanged package before regressions or
sampling. This is still a failing acceptance check.

Fresh commands, exit codes, runtime hashes and evidence paths:
`evidence/current-author-verification.json`.
- Historical shortcut control exits 1, preserving the reported 5/5 failure.
- Registered packaging/source/math/delivery/inventory check passes.
- Registered batch-selection check passes: reported cue scores 1/5 raw and
  delivered; all ten source-profile contrast sets pass; 25 batch native responses pass.
- Registered evidence-contract check exits 1. Its corrected bundle and relocation,
  wrong-root and missing-provenance controls pass; installed runner handoff fails.
- Source/render binding passes for ten complete banks and 50 choices. Both retained
  actual-UI screenshots reinspected and readable; their inputs match fresh delivery.
- Runtime and manifest hashes unchanged. Installed Python/SymPy match manifest.
- No publication, database writes, engine edits, external writes or services.

Remaining root cause: `scripts/generator_pipeline.py:720-727` rejects unchanged
package bytes even when the independent finding is evidence-only and explicitly
requires preserving the package. The tested proposal remains staged at
`runner-fix/evidence-only-rejection.patch`, not installed. The corrected evidence
bundle is `evidence/contract-correction`; its map is
`evidence/contract-installation.json`. Applying the runner fix and installing
outside this workspace require the runner owner. Do not modify runtime bytes to
evade the gate or weaken its strict regression. Another identical author retry
cannot repair that external control flow under the workspace-only constraint.
