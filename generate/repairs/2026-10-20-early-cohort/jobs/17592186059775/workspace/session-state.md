# Current state — 2026-10-22, author-47

Preserved all runtime files, manifest, source families and strict regressions.
Read feedback, both retained findings, the repair history, source evidence,
existing instructional account and required generator documentation. No new
instructional or generator defect was demonstrated.

Exact latest reproduction:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/check_current_handoff.py`
exits 1. The installed `scripts/generator_pipeline.py:723` identical-package
gate calls repair before regressions or sampling. Finding 9b8cb52352b8ca3e790e
requests evidence-only correction and runtime preservation. Changing runtime
bytes to evade that gate would not repair the finding.

Fresh targeted commands and exit codes are in
`evidence/current-check-commands.json`; results and unchanged runtime hashes
are in `evidence/current-verification.json`.

- `checks/check_evidence_contract.py`: exit 1. The corrected 83-file bundle,
  two arbitrary relocations, missing-provenance and wrong-root negative controls,
  12 source captures, three affected stored generated records and current batch
  binding pass. The required installed-runner handoff fails.
- `checks/check_batch_selection.py`: exit 0. Exact seed 4258185931 shortcut
  scores 1/5 raw and delivered; all five survive actual delivery filters.
  Ten profiles and 25 native learner-grading responses pass.
- `checks/check_cli_contract.py`: exit 0. Runtime-only relocation, deterministic
  replay, requested counts and finite-limit rejection pass.
- `checks/check_render_binding.py`: exit 0. Ten complete source banks and 50
  choices replay; retained UI inputs equal current delivered endpoints.
  Reinspected `evidence/author8-render/question-002.png`: all five choices and
  row-operation stages remain readable and consistent. No render-affecting edit.
- All six manifest/runtime hashes remain unchanged. Installed dependency
  versions match the manifest. No publication, database or external file writes.

Unfinished: runner owner must correct evidence-only identical-package routing
and install the evidence correction at the runner-chosen evidence root. Both
locations are outside the authorized workspace. The complete validated bundle
is `evidence/contract-correction`; copy map `evidence/contract-installation.json`;
proposed runner patch `runner-fix/evidence-only-rejection.patch`. The unchanged
patch retains its existing 23-case offline results; those do not establish that
it is installed. Keep the current failure strict, then rerun it and retained
regressions after an external correction. Historical acceptance is not fresh
approval. Author status is unsupported because the strict handoff fails.
