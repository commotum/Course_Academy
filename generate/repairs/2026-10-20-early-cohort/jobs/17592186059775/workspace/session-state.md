# Current state — author-344

Read latest feedback, both retained findings, prior state, source evidence and
generation/validation instructions. Preserved all runtime and manifest bytes;
no publication, database writes, other-job edits, or external runner edits.

First reproduced the latest failure with the job Python:
`python -B checks/check_current_handoff.py` exits 1. Installed runner rejects
the unchanged package before regressions or sampling. Evidence finding
9b8cb52352b8ca3e790e explicitly requires preserving the runtime. Changing package
bytes to evade that gate would not repair this finding.

Fresh checks (full commands, durations and logs in
`evidence/current-author-verification.json`):

- `checks/check_all.py`: exit 0. CLI/relocation, complete source banks,
  independent math, native grading, shared delivery and captured inventory.
- `checks/check_batch_selection.py`: exit 0. Exact seed 4258185931, controlled
  answer-role variation, shared delivery and native grading.
- `checks/check_evidence_contract.py`: exit 1. Actual evidence bundle, relocation,
  missing-provenance/wrong-root controls and current-record binding pass;
  installed-runner handoff remains failing.
- `checks/check_render_binding.py`: exit 0. Ten source banks and two UI records
  match the current runtime/delivery. Reinspected
  `evidence/author8-render/question-001.png`; matrices, controls and elimination
  solution are readable. Unchanged output did not require another render.
- `checks/check_runner_handoff.py`: exit 0. The staged external correction
  applies in a disposable checkout and passes 23 control-flow cases; it is
  **not installed**. This does not resolve the strict installed-runner failure.

Both retained finding IDs remain in `repair-regressions.json`; no check was
weakened. Runtime hashes are unchanged.

Unfinished action belongs to the runner owner: review/apply
`runner-fix/evidence-only-rejection.patch` to
`/home/jake/Developer/Course_Academy/scripts/generator_pipeline.py`, then run
`checks/check_current_handoff.py` and `checks/check_evidence_contract.py` and
route through fresh independent review. The target is outside this workspace's
authorized writes. Corrected evidence is staged at `evidence/contract-correction`;
the runner chooses its destination. Historical acceptance is not fresh approval.
Repeating unchanged author validation cannot install that external correction.
