# Current state — author-336

Read feedback and both retained findings plus all 336 history events. Preserved
the runtime, manifest, source analysis, staged runner correction and strict checks.
Reproduced the latest failure first with:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/check_current_handoff.py`
It exits 1: the installed runner rejects the byte-identical package before
regressions or sampling. The gate is at `scripts/generator_pipeline.py:723`.

Ran each registered regression once, then the retained UI binding check. Exact
commands, exit codes, logs and unchanged runtime hashes are in
`evidence/current-author-verification.json`:
- `checks/check_all.py`: exit 0. Relocated CLI, source replay, independent math,
  native grading, delivery filtering and captured-inventory checks pass.
- `checks/check_batch_selection.py`: exit 0. The reported seed, current/delivered
  shortcut probes, controlled candidate changes and native grading pass.
- `checks/check_evidence_contract.py`: exit 1. Corrected bundle validation and
  wrong-root/missing-provenance negative controls pass; installed handoff fails.
- `checks/check_render_binding.py`: exit 0. Ten complete source banks and two
  current delivered records remain bound to retained actual-UI renderings.
  Visually inspected `evidence/author8-render/question-001.png`; matrices,
  controls and elimination steps are readable. No new rendering was needed.

No new mathematical or instructional defect was demonstrated. The retained
evidence-only finding explicitly requires preserving the package. Changing its
bytes solely to escape the gate would not fix the reported defect.

Unfinished: the runner owner must review/apply
`runner-fix/evidence-only-rejection.patch` to `scripts/generator_pipeline.py`,
rerun the strict handoff, and arrange fresh independent review. The patch target
and supplied author evidence destination are outside authorized workspace writes.
The correction remains uninstalled and its strict regression remains failing.
No publication, database, engine, other-job or external-runner writes occurred.
