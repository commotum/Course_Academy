# Current state — 2026-10-22, author-273

Read feedback and all retained history (273 events, two named findings).
Reproduced latest failure first: `python -B checks/check_current_handoff.py`
exits 1. Installed `scripts/generator_pipeline.py:723-727` rejects the unchanged
candidate before retained regressions or sampling. The remaining independent
finding requests evidence-only correction and preservation of runtime files.

Fresh checks (job Python, `-B`):

- `checks/check_evidence_contract.py`: exit 1 solely at installed runner handoff.
  Actual validator accepts the corrected bundle at two relocated roots; real
  missing-provenance and wrong-root negative controls fail as required.
  Twelve source and three historical generated-inventory bindings reconfirmed.
- `checks/check_batch_selection.py`: exit 0. Exact seed 4258185931 passes raw
  and after shared delivery: five accepted, shortcut succeeds only 1/5.
  Ten profiles checked; native grader accepts five correct and rejects 20 wrong.
- `checks/check_render_binding.py`: exit 0. Ten complete source banks replay;
  two retained actual-UI records match current delivery. Inspected unchanged
  question-001 screenshot; readable matrices, controls and elimination steps.

Commands, results and runtime hashes: `evidence/author273-verification.json`.
Runtime and manifest match the previous attempt exactly. All registered strict
regressions remain intact. Unaffected checks and staged patch verification were
retained rather than repeated. No runtime implementation change was justified.

The remaining action is installation/review of
`runner-fix/evidence-only-rejection.patch` by the runner owner, followed by strict
regressions and fresh independent review. That patch targets
`scripts/generator_pipeline.py`, outside the authorized workspace. It remains
uninstalled. No engine, runner, database, publication, or other-job edits occurred.
The handoff is unsupported under the supplied write scope; Gaussian elimination
source support and the preserved generator are not the unresolved limitation.
