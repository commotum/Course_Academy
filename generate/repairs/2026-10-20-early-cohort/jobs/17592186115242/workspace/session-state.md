# Current verification — author 760

Runtime, manifest, source families, staged replacements, and all five regressions
preserved. Read latest feedback and all retained findings; reused prior source
analysis rather than rebuilding the package.

First test: `/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/batch_regressions.py --finding inventory`.
Exit 1: five captured historical banks; 64/64 possible-history shortcut successes.

Then: `/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/recheck_status.py --output evidence/author-760`.
Exit 1 only for 591f580cadb749294588. Four generator regressions pass; 17 source
banks replay; 14 records retain contrasts after shared delivery; native grading
accepts 7 correct and rejects 28 wrong choices. Relocation, exact dependencies,
protected hashes and staged replacement proposal verify.

Evidence: evidence/author-760/{first-command,commands,results,grader-report}.json,
initial-reproduction.txt and disposition.md. Full inventory witness remains at
evidence/repair-2/inventory-results.json; complete records are in
evidence/generated-records.json.

Next unfinished step: separate inventory remediation and fresh capture, then the
strict inventory check. Database changes are expressly forbidden here. Do not
weaken the regression, substitute the proposal for captured inventory, or repeat
unchanged author passes. The reviewed proposal remains
`evidence/repair-3/inventory-repair-proposal.json`.
