# Current state — 2026-10-22, author-98

Preserved all runtime files and completed repairs. Read feedback, retained
findings, prior handoff and runner control flow. No external, engine, database
or publication edits.

Exact latest failure: job Python `-B checks/check_current_handoff.py` exits 1.
Installed `scripts/generator_pipeline.py:723` rejects the identical package
before regressions or sampling. Retained finding 9b8cb52352b8ca3e790e requests
an evidence-only correction and explicitly forbids package changes.

Affected checks actually run:
- `checks/check_evidence_contract.py`: exit 1 at installed handoff. The bundle
  itself validates at two relocated roots; wrong-root and missing-provenance
  negative controls reject. Twelve source captures and three affected inventory
  records bind to retained evidence.
- `checks/check_batch_selection.py`: exit 0. Exact seed 4258185931 yields 1/5
  shortcut hits both raw and after shared delivery; all five survive. Native
  grader accepts 5 correct and rejects 20 wrong selections. Retained profile
  and controlled contrast checks pass.
- `checks/check_render_binding.py`: exit 0. Ten complete source banks (50 choices)
  replay; two retained actual-UI records equal current delivered endpoints.
  Reinspected question-001.png: readable matrices and solution, no clipping.

Commands, results and unchanged runtime hashes: evidence/author98-verification.json.
Strict failing evidence/handoff regressions remain registered and unchanged.

Unfinished: runner-owned evidence-only routing and installation outside this
workspace. Existing proposal: runner-fix/evidence-only-rejection.patch; complete
bundle: evidence/contract-correction; install inventory:
evidence/contract-installation.json. Neither was installed. The easy question
family remains supported; unsupported describes the unresolved handoff contract.
Do not repeat unchanged author retries or alter runtime bytes to evade the gate.
