# Author 731 — 2026-10-22

Preserved all runtime repairs and all five strict finding regressions.
Latest failure reproduced first:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/batch_regressions.py --finding inventory`
Exit 1: five historical banks; 64/64 possible-history shortcut successes.

Rechecked with:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/recheck_status.py --output evidence/author-731`
Exit 1 solely for finding 591f580cadb749294588. Four generator regressions pass;
17 complete source banks replay, 14 records survive shared delivery with tested
contrasts, native grading accepts 7 correct and rejects 28 wrong choices.
Package dependencies, relocation, protected runtime/source/inventory hashes and
staged replacement mapping pass. Reused unchanged rendering evidence and visually
inspected question-001.png and the original lesson flowchart.

Evidence: evidence/author-731/commands.json, results.json, inventory-results.json,
grader-report.json, instructional-review.md and disposition.json.
All affected-inventory evidence paths resolve relative to the supplied evidence
root. No runtime, engine, database, publication or source changes.

Remaining action is separate inventory remediation and fresh capture, prohibited
in this author task. Existing proposal: evidence/repair-3/inventory-repair-proposal.json.
Keep the inventory regression failing; do not report the delivered pool repaired.
