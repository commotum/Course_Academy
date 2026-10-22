# Current state — 2026-10-22, author-107

Latest feedback, both retained findings, history and previous state read first.
No runtime or regression changes. The installed runner still rejects the package
before regressions or sampling because its digest is unchanged, although the
latest independent finding requests evidence-only correction and preservation
of package bytes. Reproduced first with job Python:
`-B checks/check_current_handoff.py` (exit 1).

Targeted checks with job Python:
- `-B checks/check_evidence_contract.py > evidence/current-evidence-check.log 2>&1`:
  exit 1 at installed handoff. Corrected 83-file bundle, relocation, historical
  missing-provenance/wrong-root controls, current-record and three stored-record
  bindings pass. The strict failure remains registered.
- `-B checks/check_batch_selection.py > evidence/current-batch-check.log 2>&1`:
  exit 0. Retained seed 4258185931 shortcut is 1/5 raw and delivered; five records
  survive shared delivery. Ten profiles preserve target contrasts. Independent
  mathematics and native grading pass (5 accepted, 20 rejected).
- `-B checks/check_render_binding.py`: exit 0. Ten complete source banks and fifty
  choices replay; two retained actual-UI records match current delivered endpoints.
  Reinspected evidence/author8-render/question-001.png: readable matrices, radio
  controls and full solution with no clipping or raw TeX. No fresh rendering run.
- `-B checks/check_cli_contract.py > evidence/current-cli-check.log 2>&1`:
  exit 0. Runtime-only relocation, requested counts, deterministic output and
  explicit finite-limit rejection pass.

Commands and unchanged runtime hashes: evidence/current-verification.json.
Current strict failure: evidence/current-handoff-regression.json.

Unfinished: external runner integration in scripts/generator_pipeline.py:723–728.
The existing staged correction is runner-fix/evidence-only-rejection.patch; it
is not installed. Applying it requires a prohibited write outside this workspace.
The runner owner should review/apply it, run retained regressions and sampling,
then obtain fresh independent review. This route does not require installing the
historical accepted report. The separately staged historical evidence bundle is
evidence/contract-correction with map evidence/contract-installation.json; it is
not fresh approval and has not been installed outside the workspace.

No source-supported generator defect is demonstrated by the unchanged-byte gate.
Do not alter runtime solely to evade it or weaken the failing check. Repeated
authoring cannot repair the external file under the current write boundary.
No publication, database, engine, external-file writes or service calls performed.
