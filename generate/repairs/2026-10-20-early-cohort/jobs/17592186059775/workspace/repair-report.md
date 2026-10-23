# Current repair result — author-291

Preserved all completed generator repairs. Reproduced the latest failure first
and ran retained checks. Source replay, math, native grading, delivery, inventory
and shortcut checks pass. Corrected evidence validates with relocation and
missing-file negative controls; source/UI bindings pass. Runtime unchanged.

Strict evidence regression still exits 1: installed runner rejects the unchanged
package before sampling. Proposed external correction passes 23 offline cases,
but targets `scripts/generator_pipeline.py` outside the authorized workspace.
The patch is not installed and the failing acceptance criterion is unchanged.

Commands/results: `evidence/author291-verification.json`.
Current failure: `evidence/current-handoff-regression.json`.
Bundle: `evidence/contract-correction`.
Proposed fix: `runner-fix/evidence-only-rejection.patch`.

Fresh independent review remains required. No publication or database writes.
