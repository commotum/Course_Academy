# Current repair result

Preserved completed generator repairs and all runtime bytes. Targeted batch,
delivery, native-grading, relocated CLI, source replay and render-binding checks
pass. The corrected evidence bundle validates at its actual root and at relocated
roots; wrong-root and missing-provenance controls fail as expected.

The registered evidence regression still exits 1: the installed runner rejects
unchanged runtime before sampling, while finding 9b8cb52352b8ca3e790e requires
preserving it. Its staged correction targets `scripts/generator_pipeline.py`,
outside the authorized workspace. It has not been applied.

The fresh-review route described in `runner-fix/README.md` does not require
installing a historical acceptance as new approval. Corrected evidence already
exists at `evidence/contract-correction`; the immediate blocker is runner routing.

Commands and results: `evidence/current-author-verification.json`.
Strict failure: `evidence/current-handoff-regression.json`.
External correction: `runner-fix/evidence-only-rejection.patch`.

Status: unsupported due to the unresolved handoff, not absent source support.
No publication, database changes or writes outside this workspace were performed.
