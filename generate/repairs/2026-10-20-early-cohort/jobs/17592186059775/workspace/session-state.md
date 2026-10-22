# Current state — 2026-10-22, author-120

Runtime, manifest, instructional account and strict regressions preserved.
Read feedback/history and previous state; reproduced latest failure first with
job Python `-B checks/check_current_handoff.py`: exit 1, unchanged-package
rejection before regressions or sampling. Responsible external rule remains
`scripts/generator_pipeline.py:722–728`. Finding 9b8cb52352b8ca3e790e explicitly
requires preserving runtime. No new generator defect demonstrated.

Targeted checks (exact commands and logs in evidence/current-verification.json):
- check_batch_selection.py: exit 0; reported cue 1/5 raw and delivered, all five
  survive shared delivery; ten profiles and 25 native grading submissions pass.
- check_evidence_contract.py: exit 1 only at installed runner handoff. Bundle,
  relocation, wrong-root/missing-provenance controls, 12 source bindings and
  three affected generated inventory records pass. 83 files remain staged.
- check_render_binding.py: exit 0; ten complete source banks/50 choices;
  retained actual-UI records match current delivered endpoints. Runtime is
  unchanged, so previous screenshot inspection remains applicable.

Unfinished external action: runner owner must review/apply
runner-fix/evidence-only-rejection.patch to scripts/generator_pipeline.py,
resolve evidence installation with evidence/contract-installation.json, then
rerun strict checks and independent review. Both destinations are outside
workspace-only authorization. The staged patch is not installed; the installed
failure remains strict. No runtime changes merely to evade the identity gate,
external edits, publication, services, or database writes were performed.
Do not repeat authoring or unrelated validation for this same external gate.
