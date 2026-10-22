# Current state — 2026-10-22, author-56

Read feedback, repair history, prior state and required generator/validation docs.
Preserved runtime, package manifest, completed repairs and strict regressions.
No new source or generator defect is demonstrated; no runtime edit is warranted.

Latest failure reproduced first:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/check_current_handoff.py`
exits 1. Installed `scripts/generator_pipeline.py` rejects the byte-identical
candidate before retained regressions or sampling. Finding 9b8cb52352b8ca3e790e
requires an evidence-only correction while preserving runtime.

Affected checks rerun:
- `checks/check_evidence_contract.py`: bundle validates at its actual root and two
  relocated roots; missing-provenance and wrong-root controls reject. Overall exit
  1 preserves the actual runner failure.
- `checks/check_batch_selection.py`: exit 0; ten source profiles retain all target
  ranks; five records survive shared delivery; shortcut scores 1/5 raw/delivered;
  25 native grades pass (5 accepted, 20 rejected).
Commands/results: `evidence/author56-verification.json`. Unchanged source replay,
CLI and inspected UI evidence remain available; these were not rerun unnecessarily.
The staged runner patch also passes all 23 offline control-flow cases in
`checks/check_runner_handoff.py`; it remains uninstalled. Its passing proposal
check does not resolve the strict installed-runner failure.

Unfinished action is external: apply the reviewable runner correction at
`runner-fix/evidence-only-rejection.patch` to `scripts/generator_pipeline.py`, then
run the strict handoff and retained regressions before fresh independent review.
The proposed patch is NOT installed. Its target is outside authorized writes.
The evidence bundle is `evidence/contract-correction`, with relative-root mapping
in `evidence/contract-installation.json`. No publication or database writes.

Further author-only retries with identical authorization cannot install this fix.
Do not change generator bytes merely to evade the runner hash gate, weaken its
strict failing regression, or present historical review acceptance as new approval.
