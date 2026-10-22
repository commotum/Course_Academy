# Current state — 2026-10-22, author-88

Preserved the repaired runtime, complete source banks, manifest, instructional
account, staged evidence correction, and strict regression registrations.
No runtime, engine, runner, publication, database, or other-job files changed.

Read feedback and repair history first. The retained independent finding
9b8cb52352b8ca3e790e requests evidence-only correction and preservation of
package bytes. Earlier generator repairs remain completed.

Commands run from this workspace using
`/home/jake/Developer/Course_Academy/.venv/bin/python -B`:

- `checks/check_current_handoff.py`: exit 1. Reproduced the exact latest
  rejection before regressions or sampling: candidate is byte-identical to the
  rejected package. Evidence: `evidence/current-handoff-regression.json`.
- `checks/check_evidence_contract.py`: exit 1 solely at the same installed-runner
  gate. The real review validator accepts the corrected bundle at its own root
  and two relocated roots; wrong-root and missing-provenance controls fail as
  required. Twelve source captures and three affected generated inventory
  records remain bound; all six runtime/manifest hashes remain unchanged.
  Evidence: `evidence/evidence-contract-validation.json`.
- `checks/check_batch_selection.py`: exit 0. All five records survive the shared
  delivery filter; retained shortcut scores 1/5 both raw and delivered. Ten
  profiles retain decision-role variation and semantic coverage. Native grader:
  5 accepted, 20 rejected. Evidence: `evidence/batch-selection-regression.json`,
  `evidence/delivery-batch-repair/delivery.json`, and
  `evidence/batch-repair-native-report.json`.
- `checks/check_render_binding.py`: exit 0. Ten complete source banks replay
  (50 choices), and the two previously rendered UI records equal the current
  delivered endpoints. Re-inspected `evidence/author8-render/question-001.png`:
  prompt, five matrix choices and elimination solution are readable.

Confirmed the installed cause directly at
`repo_root/scripts/generator_pipeline.py:723–727`: identical package, source,
and engine hashes trigger rejection before `check_repair_regressions()`.
The proposed scoped runner correction remains
`runner-fix/evidence-only-rejection.patch`; it is not installed. Editing that
external runner or installing reports at the supplied external evidence root
violates the workspace-only boundary. Altering generator bytes to evade the
gate would not repair the evidence finding and would contradict its instruction.

Next unfinished action requires the runner owner: resolve evidence-only routing
and install the staged bundle using `evidence/contract-installation.json`, then
run the retained checks and fresh independent review. No further generator,
rendering, or unrelated mathematical changes are justified by the current
finding. Strict failing checks remain intact; no ready claim is made.

Author-88 rechecked whether the current workspace-relative handoff could resolve
the finding without external writes. The bundle is already self-contained and
valid at relocated roots; this does not install it or alter the installed gate.
Preserved that distinction and all failing acceptance criteria. Used the
process-audit skill to stop redundant generator work after the exact external
blocker and the small retained regression sample were confirmed. No new runtime
or instructional changes were made.

Author-88 also reran `checks/check_cli_contract.py` (exit 0): relocated runtime
returns exactly 0, 1 and 5 requested records; moderate five-record support remains;
the 64-instance easy limit is explicit. Source and render binding passed again
(10 complete banks / 50 choices, 2 unchanged UI endpoints), and the first bound
screenshot was visually inspected. The evidence regression reconfirmed all 83
staged installation files, 12 source captures and 3 affected inventory records.
The original 5/5 historical shortcut remains a failing negative control; the
current batch scores 1/5 before and after shared delivery filtering. No additional
rendering or unrelated mathematical investigation is needed for an unchanged
runtime. Current results are in the existing named reports; no duplicate report
bundle was created. The runner gate still fails and no ready claim is made.
