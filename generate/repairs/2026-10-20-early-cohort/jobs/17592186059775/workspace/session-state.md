# Current state — 2026-10-22, author-113

Read feedback and retained findings; preserved completed generator repairs.
Reproduced the latest failure first: job Python `-B checks/check_current_handoff.py`
exits 1. The installed runner rejects the unchanged runtime before regressions
or sampling. Finding 9b8cb52352b8ca3e790e explicitly requires evidence-only
correction and preservation of the package.

Fresh targeted verification (job Python, `-B`):

- `checks/check_evidence_contract.py`: exit 1. The 83-file staged bundle passes
  real review validation and two relocated-root checks. Missing provenance and
  wrong-root controls fail as expected. Current records, 12 source captures and
  three affected inventory records are bound. Installed runner handoff fails.
- `checks/check_batch_selection.py`: exit 0. Seed 4258185931 shortcut scores
  1/5 raw and delivered; all five survive shared delivery. Ten profiles checked;
  native grading accepts 5 correct responses and rejects 20 distractors.
- `checks/check_render_binding.py`: exit 0. Ten complete source banks replay;
  retained UI endpoints match current delivered records. Visually inspected
  evidence/author8-render/question-001.png: readable matrices, choices and all
  row operations. No runtime changes require another render.
- `checks/check_cli_contract.py`: exit 0. Runtime-only relocation, deterministic
  output, exact requested counts and explicit finite-limit rejection pass.
- The proposed patch previously passed 23 offline cases. It and the installed
  runner are unchanged, so that separate proposal test was not repeated.

Commands, exit codes, current evidence and unchanged runtime hashes are in
`evidence/current-verification.json`. Strict failing regressions remain intact.
No package, engine, external-file, publication or database changes occurred.

Unfinished: runner owner must resolve scripts/generator_pipeline.py:723–728
outside this workspace. The verified proposal is
runner-fix/evidence-only-rejection.patch. It retains regressions, sampling and
fresh independent review; historical acceptance is not new approval. The
corrected evidence bundle remains staged at evidence/contract-correction.
Do not modify generator bytes solely to evade the digest gate. Repeating this
author task under the same write boundary cannot install the external fix.
