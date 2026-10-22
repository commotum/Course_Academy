# Current state — pass 290

Preserved completed runtime repairs, manifest, all five executable finding checks,
and the verified replacement proposal. No runtime change, database write or publication.

Latest failure reproduced first:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/batch_regressions.py --finding inventory`
Exit 1: five stored historical banks; possible-history shortcut witness 64/64.

Retained recheck:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/recheck_status.py --output evidence/repair-290`
Exit 1 solely for finding 591f580cadb749294588. Four current-generator regressions,
17 complete source banks plus canonical replay, delivery 14/14, native grading
(7 accepted, 28 rejected), exact dependencies, and relocation pass. Staged mapping
and protected hashes verify. Reinspected retained UI screenshot.
Commands and results: evidence/repair-290/{commands.json,results.json,outcome.md}.

Next unfinished action belongs to the separate inventory-remediation workflow:
resolve the five records in affected-inventory.json using the staged proposal,
then recapture inventory and rerun the strict regression. That action is prohibited
in this author task. Keep the failure explicit; do not modify the runtime or repeat
unchanged-input author passes to conceal an immutable stored-pool defect.
