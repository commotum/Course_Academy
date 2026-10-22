# Current state — 2026-10-22, author-91

Preserved the repaired generator, source banks, runtime files, manifest,
instructional account, evidence bundle, staged runner patch and strict regressions.
No files outside this workspace were changed. No publication or database writes.

Read feedback and retained history before validation. The latest finding requires
an evidence-only correction and unchanged runtime. Existing source analysis and
instructional constraints remain applicable; no runtime change is justified.

Commands run from this workspace with
`/home/jake/Developer/Course_Academy/.venv/bin/python -B`:

- `checks/check_current_handoff.py` — exit 1. Exact latest failure reproduced:
  installed runner rejects a byte-identical package before retained regressions
  or sampling. Evidence: `evidence/current-handoff-regression.json`.
- `checks/check_evidence_contract.py` — exit 1 only at that handoff gate.
  Actual review validator accepts the complete 83-file bundle and two relocated
  roots. Wrong-root and missing-provenance controls correctly fail. Twelve source
  captures, three affected generated inventory records and all six unchanged
  runtime/manifest hashes are reconfirmed. Evidence:
  `evidence/author91-evidence-check.log`,
  `evidence/evidence-contract-validation.json`.
- `checks/check_batch_selection.py` — exit 0. Five records survive shared delivery
  filtering with no duplicates. Shortcut scores 1/5 raw and delivered; historical
  5/5 failure is retained as a strict negative control. Ten profiles pass controlled
  role checks. Native grader: 5 acceptances and 20 rejections, all expected.
  Evidence: `evidence/author91-batch-check.log`,
  `evidence/batch-selection-regression.json`,
  `evidence/delivery-batch-repair/delivery.json`,
  `evidence/batch-repair-native-report.json`.
- `checks/check_render_binding.py` — exit 0. Ten complete source banks replay
  with 50 choices; two retained actual-UI records match fresh delivered endpoints.
  Visually inspected `evidence/author8-render/question-001.png`: readable prompt,
  five choices and full elimination solution. Evidence:
  `evidence/current-render-binding.json`.

Confirmed the installed cause at repo_root/scripts/generator_pipeline.py:723:
equal package, source and engine hashes trigger rejection before tests. Installed
SHA-256 is 6b5e606725c2b82f87212da3c0ec39da0231db0722cd440ef1d21e141d01deb2,
matching runner-fix/patch.json's base. Staged patch bytes match their recorded hash.
Applying it requires an external write, forbidden in this job. Changing working
runtime merely to evade this gate would not repair evidence paths and contradicts
the retained report-only instruction. Strict failing checks were not weakened.
Broad unrelated tests were not repeated.

Next unfinished step: runner owner resolves evidence-only routing outside this
workspace, then runs retained checks and fresh independent review. Proposed fix:
`runner-fix/evidence-only-rejection.patch`. Corrected bundle and relative installation
map: `evidence/contract-correction`, `evidence/contract-installation.json`.
Neither installation nor fresh independent approval is claimed.
