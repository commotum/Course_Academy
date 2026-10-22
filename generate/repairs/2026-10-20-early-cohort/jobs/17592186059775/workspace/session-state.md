# Current state — 2026-10-22, author-217

Preserved the completed generator repairs and all runtime bytes. Read feedback,
retained history findings and prior state first. Reproduced the exact latest
failure using `checks/check_current_handoff.py`: exit 1. Installed
`scripts/generator_pipeline.py:723` rejects identical runtime before retained
regressions or sampling. The concrete remaining independent finding is evidence-only.

Fresh verification (commands, results and logs in
`evidence/current-author-verification.json`):
- `checks/check_evidence_contract.py`: exit 1. Evidence bundle validates at its
  actual root and two relocated roots; missing-provenance/wrong-root controls
  reject as required. Twelve source captures and three stored generated records
  remain bound. Only installed runner handoff fails.
- `checks/check_batch_selection.py`: exit 0. Reported seed 4258185931 scores
  1/5 on the shortcut before and after shared delivery; all five survive.
  Ten profile contrast banks and 25 native grader responses pass.

Author-217 reconfirmed both retained findings and all 217 history events by
category. Fresh logs are `evidence/author217-check_evidence_contract.log` and
`evidence/author217-check_batch_selection.log`; commands and exit codes are in
`evidence/current-author-verification.json`. The evidence check validates 83
bundle files, 12 source captures and three affected stored records; its exit 1
still reflects the actual installed runner rejection. No check was weakened.

No runtime, engine, database, image publication or external runner changes.
Source replay and rendering evidence remain applicable to unchanged runtime;
no unrelated broad checks or interchangeable renders repeated. Strict failure
and regression registration remain intact.

Unfinished action: runner owner must repair the evidence-only identical-package
gate and install the corrected bundle at its selected evidence root. Existing
`runner-fix/evidence-only-rejection.patch` remains staged, not installed. Both
required destinations are outside the user-authorized workspace. Another retry
under identical write constraints cannot resolve that installed-runner rule;
do not change runtime bytes solely to evade it or claim ready while strict
handoff fails.
