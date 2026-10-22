# Current state — 2026-10-22, author-138

Preserved completed generator repairs, manifest, regression registrations and
staged evidence bundle. No runtime, engine, database, publication or other-job
changes. Read feedback and all repair-history findings/events before validation.
The latest installed-runner failure was reproduced first.

Fresh commands use `/home/jake/Developer/Course_Academy/.venv/bin/python -B`:

- `checks/check_current_handoff.py`: exit 1. Installed sample-stage gate rejects
  the unchanged package before retained regressions or sampling.
- `checks/check_evidence_contract.py`: exit 1 overall. Corrected bundle validates
  with relocation, wrong-root and missing-provenance controls; current-record,
  original-source and three generated inventory records remain bound. The strict
  installed-runner check still fails. The 83-file bundle remains staged.
- `checks/check_batch_selection.py`: exit 0. Exact seed 4258185931 shortcut
  scores 1/5 raw and delivered; five accepted records, zero duplicates. Ten
  profiles, independent matrix checks and 25 native responses pass (5 accepted,
  20 rejected).
- `checks/check_cli_contract.py`: exit 0. Runtime-only relocation, deterministic
  easy/moderate CLI, counts 0/1/5 and explicit finite-limit failure pass.
- `checks/check_render_binding.py`: exit 0. Ten complete source banks (50
  choices) replay exactly. Two retained actual-UI inputs equal current delivered
  endpoints. Visually reinspected `evidence/author8-render/question-001.png`:
  readable matrices and complete elimination stages, no apparent clipping or
  exposed TeX. No new render needed for unchanged records/runtime.

Commands, results, distinct fidelity/correctness/grading/variation claims and
limits: `evidence/author138-verification.json`. Source evidence and the existing
instructional account remain applicable; no pedagogical or runtime change is
justified by finding 9b8cb52352b8ca3e790e, which explicitly requests an evidence-only
correction preserving the package.

Remaining blocker: installed `scripts/generator_pipeline.py:722` rejects the
unchanged runtime despite that evidence-only finding. Confirmed package hash:
`38c685ce1e5bd4f89ac79b6ab3d31a4a81f2b77c9f4bb6f0abcab5c20640f626`.
`runner-fix/evidence-only-rejection.patch` is uninstalled. Changing runtime bytes
to evade the gate would not repair the finding. Strict failing checks remain.

Next required step is outside the authorized workspace: the runner owner must
resolve that gate, install the corrected evidence bundle at its matching root,
rerun strict regressions and obtain fresh independent review. Repeating this
unchanged author pass cannot resolve an external runner rejection. Handoff is
unsupported; source-supported generator coverage remains preserved.
