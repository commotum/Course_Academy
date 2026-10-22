# Current state — pass 292

Preserved completed runtime repairs, manifest, all five executable finding checks,
and the verified replacement proposal. No runtime change, database write or publication.

Latest failure reproduced first:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/batch_regressions.py --finding inventory`
Exit 1: five stored historical banks; possible-history shortcut witness 64/64.

Retained recheck:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/recheck_status.py --output evidence/repair-292`
Exit 1 solely for finding 591f580cadb749294588. Four current-generator regressions,
17 complete source banks plus canonical replay, delivery 14/14, native grading
(7 accepted, 28 rejected), exact dependencies, and relocation pass. Staged mapping
and protected hashes verify. Reinspected retained UI screenshot.
Commands and results: evidence/repair-292/{commands.json,results.json,outcome.md}.
Visually reinspected evidence/repair-3/render/question-002.png: readable system,
choices, augmented matrices and elimination. Protected hashes are unchanged.

Next unfinished action belongs to the separate inventory-remediation workflow:
resolve the five records in affected-inventory.json using the staged proposal,
then recapture inventory and rerun the strict regression. That action is prohibited
in this author task. Keep the failure explicit; do not modify the runtime or repeat
unchanged-input author passes to conceal an immutable stored-pool defect.
The selector reads stored snapshots and does not call this entrypoint to rebuild
their banks; another unchanged-input author pass cannot resolve this finding.
