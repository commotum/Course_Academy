# Current repair state — pass 29

Read feedback, all five retained findings and the 29 history events. Reused the
existing candidate and instructional account. Read the required generation and
validation documents, source lesson, worked examples, all 17 complete practice
banks and solutions, and inspected the tutorial diagram.

Latest failure reproduced first:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/batch_regressions.py --finding inventory`
Exit 1: five captured generated records retain the sign-only extremum shortcut.
The possible new-seen-history witness succeeds 64/64; this is not a prediction
of every learner history. All captured generated records were tested.

Then executed once:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/recheck_status.py --output evidence/repair-29`
Exit 1 solely for finding 591f580cadb749294588. Four generator regressions pass;
17 source banks and canonical replay, independent printed math, zero roots,
controlled relevant/irrelevant changes, within-sign-group rank and position
contrasts, shared delivery (14 accepted), native grading (7 accepted and 28
rejected), exact dependency pins and relocated CLI execution pass. Runtime,
manifest, source and inventory match retained hashes. Five replacement mappings
are verified, proposed only, and unapplied. Both unchanged actual-UI screenshots
were visually reinspected; no additional render was invoked.

Read-only inspection of engine/rust/question_selection.rs:125–203 confirms it
selects stored entities and does not invoke this generator to update old banks.
The remaining failure cannot be repaired by changing workspace runtime files.
Do not weaken its regression or substitute a hypothetical replacement pool.

Evidence: evidence/repair-29/commands.json, results.json, inventory-results.json,
grader-report.json, visual-inspection.json and scope-diagnosis.json. The affected
inventory paths resolve from author-29 to complete workspace reproduction records.

Next unfinished action: separately review/apply
`evidence/repair-3/inventory-repair-proposal.json`, recapture inventory, then rerun
the strict pool check. Database changes and publication are explicitly forbidden
in this task. No runtime, engine, source, database, publication or other-job edits
were made. Status remains unsupported for the selectable-pool finding; the source
skill and current generator remain supported.
