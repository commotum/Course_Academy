# Current repair state — pass 217

Read feedback and all five retained findings. Reproduced the latest failure first:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/batch_regressions.py --finding inventory`
Exit 1: five captured historical generated banks retain the sign-extremum
shortcut; the possible-history witness succeeds 64/64 times. All non-source
inventory records were tested. Complete records: evidence/generated-records.json.
Affected identities: affected-inventory.json.

Ran:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/recheck_status.py --output evidence/repair-217`
Exit 1 only for historical inventory. Four current-generator regressions pass,
including 17 complete source-bank replays and 14 delivery-filtered records with
counterfactual and within-template shortcut checks. Native grading accepts 7
correct responses and rejects 28 wrong responses. Dependency pins, relocation,
input/runtime hashes and the five staged replacement mappings verify.
Reinspected retained actual-UI screenshot
`evidence/repair-3/render/question-001.png`: readable with no observed clipping.

No new runtime defect or source change was demonstrated. Preserved the repaired
generator, all source families, complete banks and strict failing regression.
No database, engine, source, other job or publication changes were made.
Instructional scope remains as recorded in evidence/repair-216/instructional-scope.md.
The existing instructional account and extraction remain applicable.

Finding 591f580cadb749294588 explicitly requests a separate inventory-remediation
workflow followed by recapture. The selector consumes stored candidate entities
independently of this Python package (engine/rust/question_selection.rs:125).
Workspace edits cannot change their existing banks. Five complete replacements
are staged in evidence/repair-3/inventory-repair-proposal.json, unapplied.
Applying them requires database changes prohibited by this task.

Next unfinished step: the external inventory-remediation workflow and fresh
capture. Do not repeat unchanged repair cycles, weaken the strict regression,
or substitute proposed records for captured inventory. Resume this repair only
with changed evidence or scope. Status remains unsupported for the stored pool.
Current commands and results: evidence/repair-217/.
History contains 217 events; all five retained findings remain covered by
executable checks. No new runtime defect or changed source evidence was found.
