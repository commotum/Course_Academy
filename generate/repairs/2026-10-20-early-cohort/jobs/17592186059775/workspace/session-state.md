# Current state — 2026-10-22, author-122

Read feedback, both retained findings, all 122 history events, and the previous
state before work. Reproduced the latest failure first:
`python -B checks/check_current_handoff.py` exits 1. The installed runner rejects
the identical package before regressions or sampling. Its gate at
scripts/generator_pipeline.py:722–728 conflicts with finding
9b8cb52352b8ca3e790e's explicit evidence-only correction and runtime preservation.
No new generator defect was demonstrated; no runtime or manifest edit was made.

Fresh commands and exits are in `evidence/current-verification.json`.
- check_batch_selection.py: exit 0; cue 1/5 raw and delivered, all five accepted,
  ten profiles and 25 native responses pass.
- check_all.py: exit 0; retained CLI, source/math, delivery/native and inventory
  regressions pass. Full fresh output: evidence/author122-retained.log.
- check_evidence_contract.py: exit 1 only at the strict installed handoff;
  relocated bundle validation, wrong-root and missing-provenance negative
  controls, current generator bindings and three affected inventory records pass.
- check_render_binding.py: exit 0; ten full source banks/50 choices and two
  retained actual-UI records match current delivered endpoints. Visually inspected
  evidence/author8-render/question-001.png: readable matrices, controls and
  worked elimination, without visible overlap or clipping.

All runtime hashes match author-121 and exact installed dependency versions.
Strict regressions remain unchanged and registered. The staged runner patch
runner-fix/evidence-only-rejection.patch is not installed. The remaining action
requires editing scripts/generator_pipeline.py outside the authorized workspace;
after that, rerun strict checks and fresh independent review. The corrected
historical evidence bundle and relocation manifest remain available at
evidence/contract-correction and evidence/contract-installation.json. They do not
constitute fresh approval. No publication, database, engine, service, or external
file mutations occurred. Do not change runtime bytes to evade the runner gate.
