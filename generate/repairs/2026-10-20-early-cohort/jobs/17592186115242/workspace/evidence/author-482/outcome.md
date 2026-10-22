Preserved the repaired generator and every strict regression. Reproduced the latest
inventory failure first, then ran checks/recheck_status.py --output
evidence/author-482. Exact commands, exit codes, and outputs are in commands.json.

Source fidelity: 17 complete source banks replay. Correctness: independent
printed-math checks pass, including zero roots and bare-k fractional elimination.
Grading: 7 correct selections accepted and 28 incorrect selections rejected by
the native engine. Variation: three CLI batches retain the tested sign-group,
rank and position contrasts after shared delivery (14 accepted records), with
relevant and irrelevant counterfactual checks. Relocation passes. Reused unchanged
actual-UI render evidence and visually inspected
../repair-3/render/question-001.png; math and full solution are legible, unclipped.

The only failing finding is 591f580cadb749294588. All five historical generated
records still permit the sign-only extremum shortcut; the possible learner-history
witness succeeds 64/64. No generated inventory records remain untested. The source,
inventory, runtime and manifest match retained protected hashes, so the old
counterexample still applies. The native selector reads stored candidate identities
and difficulty, not this generator; see engine/rust/question_selection.rs:125.
A further generator change cannot repair already stored answer banks.

Five verified replacements remain staged and unapplied in
../repair-3/inventory-repair-proposal.json. The finding explicitly calls for a
separate inventory-remediation workflow; this job explicitly prohibits database
changes. Keep the historical regression failing until that workflow repairs the
stored pool and supplies a fresh capture. No runtime, engine, database, publication,
source or other-job edits were made. Status: unsupported for this unresolved
historical-pool requirement; the source-supported generator is preserved.
