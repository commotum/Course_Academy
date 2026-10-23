# Current state — 2026-10-22, author-283

Read feedback and repair history first (two retained findings; 283 history events).
Preserved completed runtime repairs, manifest, instructional account, corrected
evidence bundle, and strict regression criteria. No source or generator defect
was newly demonstrated. No runtime edits were justified by the evidence-only
finding 9b8cb52352b8ca3e790e, which explicitly requires runtime preservation.

Latest failure reproduced first with the job Python:
`python -B checks/check_current_handoff.py` exits 1. Actual installed
`scripts/generator_pipeline.py:723-727` rejects the unchanged package before
regressions or sampling. Read that code directly; this is an unconditional
package/source/engine identity gate, without an evidence-only exception.

Affected checks rerun with the job Python and `-B`:
- `checks/check_evidence_contract.py`: exit 1. Real evidence validation, missing
  provenance and wrong-root negative controls, and relocation pass. Strict
  installed-runner handoff still fails; no acceptance criterion was weakened.
- `checks/check_batch_selection.py`: exit 0. Exact seed, controlled target changes,
  within-family probes, actual delivery filtering, and 25 native responses pass.
  Reported cue succeeds 1/5 before and after filtering.
- `checks/check_cli_contract.py`: exit 0. Relocation, deterministic CLI and counts.
- `checks/check_render_binding.py`: exit 0. Ten complete source banks and two
  retained actual-UI records remain bound to fresh delivered endpoints.

Inspected `evidence/author8-render/question-001.png`: readable prompt, five
matrix choices, and complete worked row operations. Runtime unchanged, so no
interchangeable rerender was needed. Exact commands, results, logs, and unchanged
runtime hashes: `evidence/author283-verification.json`.

No external, engine, database, publication, or other-job edits occurred.

## Unfinished external step

The runner owner must review/install `runner-fix/evidence-only-rejection.patch`
under `scripts/generator_pipeline.py`, then run retained strict regressions,
sampling and fresh independent review. The corrected self-contained bundle is
`evidence/contract-correction`; its destination is runner-supplied. Both runner
modification and installation at the supplied author evidence root lie outside
the authorized workspace. The patch is staged, not installed.

Another identical author retry cannot resolve that external gate. Do not change
runtime bytes merely to evade it, relabel a staged patch as installed, weaken
regressions, or claim unsupported source mathematics. The current unsupported
result reports the unresolved handoff, not a lack of source-supported questions.
