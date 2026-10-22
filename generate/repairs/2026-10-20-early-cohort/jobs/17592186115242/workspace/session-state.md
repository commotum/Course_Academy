# Current repair state — pass 178

Preserved the repaired runtime, source families, strict regression declarations,
and staged inventory replacement proposal. No runtime changes were justified
by the unchanged finding; no database or publication changes were performed.

First test:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/batch_regressions.py --finding inventory`
Exit 1: all five historical v2 records still expose the sign-extremum shortcut.
The 64/64 selection result is a possible-history witness, not observed usage.

Retained checks:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/recheck_status.py --output evidence/repair-178`
Exit 1 overall. Four current-generator regressions pass; 17 complete source
banks replay. Three delivery batches preserve the checked contrasts across 14
records. Native grading accepts 7 correct and rejects 28 wrong responses.
Relocation, exact dependency versions, protected hashes, and the five replacement
mappings pass. Retained actual-UI screenshot question-002 was visually inspected.
All five generated inventory records are reproduced; none remain untested.
Affected-inventory evidence paths resolve relative to author-178.

Remaining: finding 591f580cadb749294588 requires separate inventory remediation
and a fresh capture. The stored banks cannot be changed by a workspace generator
edit. Keep the strict regression failing until that external state changes.
Proposal: evidence/repair-3/inventory-repair-proposal.json (unapplied).
Current evidence: evidence/repair-178/commands.json, results.json,
grader-report.json, scope-resolution.json. Status: unsupported.
