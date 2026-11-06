Establish the learner task from target source evidence only. You are the existing {{role}} agent in its source-account phase; this is not generator or exemplar review.

Context:
{{context}}

Read generate/principles.md and the supplied target source_file, including the target lesson, eligible original examples, diagrams and prerequisite context. Do not inspect donor references, local examples, author accounts, generator implementation, prior reviews or repair feedback. The runner has not admitted those artifacts to this phase. Do not query or mutate the database.

Write evidence_root/source-analysis.json with exactly these substantive fields: skill (nonempty string), reasoning_steps, invariants, permitted_variations, source_refs (nonempty arrays of substantive strings). Describe the learner's required decisions and recall before feedback, supplied information and response endpoint; distinguish guided practice from independent choice. Cite exact target source IDs/passages. Record genuine uncertainty in the account rather than borrowing a different task. The same reasoning may remain across all three difficulty levels.

Return {"status":"ready","account_file":"source-analysis.json"} only after the account exists and is complete. The runner freezes this original before exposing references or examples. Later conceptual corrections require explicit source-backed amendments; never rewrite the checkpoint. For a demonstrated external blocker return status blocked with the same account_file value and retain concrete evidence. Repair fixable capture/tool errors within your authorization; do not silently substitute a different task.
