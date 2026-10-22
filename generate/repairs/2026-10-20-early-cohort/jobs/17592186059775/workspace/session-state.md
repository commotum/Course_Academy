# Current state — 2026-10-22, author-151

Read feedback and all retained history findings/events; preserved runtime package,
manifest, instructional account, evidence bundle and strict regression registrations.

Latest failure reproduced first with the job Python:
`python -B checks/check_current_handoff.py` exits 1. The installed runner's
`scripts/generator_pipeline.py:723` identity gate rejects the evidence-only
correction before retained regressions or sampling. No generator defect is newly
reported. Changing working runtime bytes to evade that gate is not a repair.

Affected checks rerun with exact commands, exit codes and logs in
`evidence/author151-verification.json`:
- Evidence bundle validation, relocation and negative controls pass; its registered
  check exits 1 because the installed handoff still fails.
- Batch selection passes: raw/delivered shortcut 1/5, five delivered records,
  ten profiles and 25 native acceptance/rejection responses.
- Relocated CLI/count/determinism/finite-limit checks pass.
- Ten complete source banks (50 choices) replay; two retained actual-UI endpoints
  bind to current delivery. Re-inspected question-002.png; readable.
- All six runtime/manifest hashes remain unchanged.

Unfinished: the runner owner must correct the evidence-only identity gate and
route the staged evidence. `runner-fix/evidence-only-rejection.patch` remains
uninstalled. Strict failure is retained. The necessary runner edit and evidence
installation are outside the authorized workspace. No engine, database,
publication, service, other-job or external runner writes were made.
Later inventory and live learner histories remain untested. No broad unchanged
suite, new render, or offline patch test was repeated.
