# Current state — 2026-10-22, author-94

Preserved the repaired generator, manifest, source banks and strict regression
registrations. This continuation changed verification evidence and this state
file only. No external runner, engine, database, publication or other-job writes.

Read feedback/history first and reproduced the exact latest failure with
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/check_current_handoff.py`
(exit 1). The installed runner rejects the byte-identical package before sampling
or retained regressions. Its predicate was reconfirmed at
`repo_root/scripts/generator_pipeline.py:723`. The retained evidence-only finding
requests runtime preservation; unrelated byte changes would not repair it.

Affected checks were run with the same Python and `-B`:

- `checks/check_evidence_contract.py`: exit 1 at the installed handoff. The actual
  review validator accepts the corrected 83-file bundle at two relocated roots;
  wrong-root and missing-provenance controls correctly fail. Twelve source
  captures, three affected generated inventory records and six package hashes
  match. No fresh independent approval is claimed.
- `checks/check_batch_selection.py`: exit 0. The exact reported seed produces five
  delivered records, no duplicates, and shortcut score 1/5 raw and delivered.
  Ten profiles retain controlled role variation. Native grading: five correct
  choices accepted, twenty wrong choices rejected.
- `checks/check_cli_contract.py`: exit 0. Relocated runtime, deterministic counts
  0/1/5, supported bands and explicit finite-limit rejection pass.
- `checks/check_render_binding.py`: exit 0. Ten complete source banks (50 choices)
  replay and retained actual-UI inputs equal fresh delivered endpoints. Both
  `evidence/author8-render/question-001.png` and `question-002.png` were visually
  inspected: readable matrices, five choices and complete elimination.

Commands, exits, logs and separate claims: `evidence/author94-verification.json`.
Strict failing handoff and evidence regressions remain intact. No new generator
failure was demonstrated; unrelated broad tests were not repeated.

Unfinished action: resolve the external runner's evidence-only/unchanged-package
routing, then run the retained checks and fresh independent review. The existing
proposal is `runner-fix/evidence-only-rejection.patch`; it remains uninstalled
because its target is outside the authorized workspace. Corrected historical
bundle: `evidence/contract-correction`; installation map:
`evidence/contract-installation.json`. The source supports the generator, but a
ready result cannot claim the known failing handoff is repaired.
