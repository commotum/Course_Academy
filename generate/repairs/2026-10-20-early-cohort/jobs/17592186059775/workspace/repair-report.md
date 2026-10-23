# Current repair result — author-272

Completed generator repairs are preserved. Fresh evidence validation, delivered
shortcut probes, native grading, relocated CLI and source/render bindings pass.
The strict evidence regression still fails at the installed runner gate.

The root cause remains `scripts/generator_pipeline.py:723-727`: unchanged runtime
bytes trigger rejection before evidence corrections or retained checks are
examined. The staged `runner-fix/evidence-only-rejection.patch` addresses that
rule but requires writes outside the authorized workspace. It remains uninstalled.
No acceptance criteria or runtime bytes were changed to bypass the failure.

Fresh commands and results: `evidence/author272-verification.json`.
Failure: `evidence/current-handoff-regression.json`.
Corrected evidence root: `evidence/contract-correction`.
Retained affected inventory: `evidence/contract-correction/affected-inventory.json`.

The runner owner must resolve the external handoff failure before fresh
independent review. No publication or database changes occurred.
