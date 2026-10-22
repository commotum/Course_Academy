# Current state — pass 287

Preserved the candidate runtime, manifest, source coverage, staged replacements,
and all five strict executable regression declarations. No runtime change was
justified by the unchanged feedback; no database or publication action occurred.

First reproduction:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/batch_regressions.py --finding inventory`
Exit 1: five historical banks, 64/64 possible-history shortcut successes.
See evidence/repair-287/initial-reproduction.json.

Validation:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/recheck_status.py --output evidence/repair-287`
Exit 1 only for finding 591f580cadb749294588. Four current-generator regressions,
17 complete source banks and canonical replay, delivery 14/14, native grading
(7 correct accepted, 28 wrong rejected), exact pins and relocation pass.
Protected hashes and staged replacement mapping verify. Reinspected retained
actual-UI screenshot; no new render is needed for unchanged runtime.

Next unfinished step: separate authorized inventory remediation of the five
stored questions and fresh inventory capture. This task prohibits that database
operation. Keep the strict historical regression; do not replace inventory with
the unapplied proposal or weaken the check. No further generator-only repair is
evidenced. Evidence: evidence/repair-287/{commands.json,results.json,outcome.md}.
