# Current repair result — author-238

The repaired Gaussian-elimination generator is preserved. No new runtime defect
is demonstrated by the latest feedback. End-to-end handoff remains unsupported:
the installed runner rejects the unchanged package before evaluating corrected
evidence, running regressions or sampling.

The exact failure was reproduced first with:

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/check_current_handoff.py
```

It exits 1 with calls `["repair"]` and “Candidate is byte-identical to the rejected
package.” `scripts/generator_pipeline.py:720-727` applies its package-change gate
to an evidence-only finding that explicitly requires preserving package bytes.
Returning unsupported also requeues authoring because the easy band is supported.
This is a runner routing failure; another generator rewrite cannot resolve its rule.

## Verified current state

- Ten complete source banks / 50 choices replay, including the recorded source ambiguity.
- The exact historical shortcut is retained as a failing negative control (5/5).
  Current raw and delivery-normalized batches score 1/5; all five ranks and positions
  occur, with complete contrast sets checked for all ten source profiles.
- Shared delivery accepts all five records. Native grading passes 25 acceptance/rejection checks.
- Relocated CLI exact counts, deterministic replay, supported bands and finite-limit rejection pass.
- Two retained actual-UI screenshots match fresh delivered endpoints and were visually inspected.
- The corrected 83-file evidence bundle passes the real review validator, relocation,
  missing-provenance and wrong-root controls. Its registered regression remains
  nonzero because the installed runner handoff is still failing.
- All runtime files and manifest remain byte-identical; dependency versions match.

Commands, exit codes, log paths, hashes and separate claims:
[evidence/author238-verification.json](evidence/author238-verification.json).
Retained finding registrations: [repair-regressions.json](repair-regressions.json).
Completed instructional analysis, historical controls and earlier broad validation
remain in the workspace; unrelated broad checks were not repeated.

## Unfinished action outside the permitted workspace

The runner owner must repair the evidence-only routing gate and install the
corrected evidence at the runner-selected root, then run the strict regression
and fresh independent review. The existing proposal at
[runner-fix/evidence-only-rejection.patch](runner-fix/evidence-only-rejection.patch)
is staged, previously tested offline, and **not installed**. The corrected bundle
is `evidence/contract-correction`, with its file map in
`evidence/contract-installation.json`. Copied historical review results are not
new independent approval.

The user permits writes only in this workspace. The required installed-runner
edit and external evidence installation are outside that boundary. No database,
publication, engine, runner or other-job content was changed. This report
supersedes earlier readiness statements in historical handoff notes.
