# Current state: author 1037

Preserved the repaired candidate. Latest failure reproduced first:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/batch_regressions.py --finding inventory`
Exit 1: five historical records affected; 64/64 possible-history shortcut.

Validation milestone:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/recheck_status.py --output evidence/author-1037`
Exit 1 only for finding 591f580cadb749294588. Four generator regressions pass;
17 complete source banks, zero roots, and counterfactual/shortcut contrasts after
shared delivery (14 records). Native grading: 7 accepted, 28 rejected. Exact
dependencies, relocation, protected hashes and staged replacement mapping pass.
Retained UI screenshot visually inspected. Evidence paths resolve from author-1037.
No runtime, engine, source, inventory, publication or database changes.

Next unfinished step: separate inventory remediation, prohibited by this task,
then fresh inventory capture and the same strict regression. Retain the failure;
do not rewrite generator repairs against unchanged stored records.
Evidence: evidence/author-1037/commands.json, results.json and disposition.md.
