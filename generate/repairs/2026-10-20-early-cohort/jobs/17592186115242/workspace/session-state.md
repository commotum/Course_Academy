# Current state — pass 295

Preserved completed runtime repairs, manifest, all five executable finding checks,
and the verified replacement proposal. No runtime, engine, database, source,
or publication change was made.

Latest failure reproduced first:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/batch_regressions.py --finding inventory`
Exit 1: five stored historical banks; possible-history shortcut witness 64/64.

Retained recheck:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/recheck_status.py --output evidence/repair-295`
Exit 1 solely for finding 591f580cadb749294588. Four current-generator regressions,
17 complete source banks plus canonical replay, delivery 14/14, native grading
(7 accepted, 28 rejected), exact dependencies, and relocation pass. Protected
hashes and staged replacement mapping verify. Visually reinspected retained
actual-UI screenshot evidence/repair-3/render/question-002.png: readable system,
choices, matrices, row operation, and contradiction.

Commands/results: evidence/repair-295/commands.json and results.json.
Scope explanation: evidence/repair-295/outcome.md.

Next unfinished step belongs to the separate inventory-remediation workflow
explicitly requested by finding 591f580cadb749294588: resolve the five records in
affected-inventory.json, recapture inventory, then rerun the strict regression.
Database changes are prohibited in this author task. The selector reads stored
candidate entities (engine/rust/question_selection.rs:125), not rebuilt banks
from this entrypoint. Keep the failure explicit; do not substitute hypothetical
replacements or repeat unchanged-input author passes to conceal the stored defect.
