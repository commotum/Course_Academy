# Current state — 2026-10-22, author-210

Read feedback, both retained findings, latest history event, existing instructional
account, checks, and previous state. Preserved the runtime and completed repairs.

Reproduced the latest failure first:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/check_current_handoff.py`
Exit 1: actual installed runner calls only `repair`; it rejects the unchanged
package before retained checks or sampling. The rule is at external
`scripts/generator_pipeline.py:723`.

Affected validation and a retained regression sample were rerun:
- `checks/check_evidence_contract.py`: exit 1. Corrected bundle validation,
  relocation, missing-provenance and wrong-root negative controls pass. Current
  source binding (12 captures), records, and three affected stored generated
  records pass. The strict installed-runner check remains failing.
- `checks/check_batch_selection.py`: exit 0. Exact seed 4258185931, supported
  family/rank coverage, preserved finite catalogs, independent mathematics,
  actual delivery filters and 25 native grader responses pass. The reported
  shortcut gets 1/5 on both raw and delivered records; its historical 5/5
  counterexample remains a required failing control.

Commands, exit codes and logs: `evidence/current-author-verification.json`.
Unchanged source/CLI/render evidence from preceding passes remains available;
no unrelated broad tests or new renders were repeated. All registered strict
checks remain intact in `repair-regressions.json`.

No runtime, manifest, external runner, engine, database, images, publication or
other jobs changed. No approval or evidence installation is claimed.

Next unfinished action belongs to the runner: permit evidence-only correction
without demanding changed runtime bytes and install the complete staged bundle
at the runner-selected evidence root. The existing staged, uninstalled proposal
is `runner-fix/evidence-only-rejection.patch`; the bundle and installation map
are `evidence/contract-correction/` and `evidence/contract-installation.json`.
Both external writes are outside this session's authorized workspace. Keep the
strict failure until the installed runner changes; then rerun affected checks
and fresh independent review. Runtime byte churn would evade the gate without
repairing the finding and is not justified.
