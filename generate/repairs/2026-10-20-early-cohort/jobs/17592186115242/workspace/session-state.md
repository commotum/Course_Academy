# Current state

Author-544 milestone, 2026-10-22. Runtime repairs preserved.

Latest failure reproduced first: job Python `-B checks/batch_regressions.py --finding inventory` exits 1 for five historical stored banks and the retained 64/64 possible-history shortcut witness.

Job Python `-B checks/recheck_status.py --output evidence/author-544` exits 1 solely for finding 591f580cadb749294588. Four generator regressions pass: 17 complete source banks, zero roots, construction, batch delivery and counterfactual checks; 14 delivered records. Native grading: 7 accepted, 28 rejected. Dependencies, relocation, protected hashes and five staged replacement mappings verify. All captured generated inventory tested. Reused unchanged renderer output and visually inspected question-002.png.

Status: unsupported. No runtime, engine, database, source, publication or other-job edits. Strict historical failure retained. The separate inventory-remediation workflow must apply reviewed replacements outside this author task, then capture the pool again. Repeating unchanged author passes cannot repair stored records. Do not mutate inventory captures or weaken tests to make them pass.

Evidence: evidence/author-544/commands.json, results.json, outcome.md; repair-regressions.json; affected-inventory.json; evidence/generated-records.json; evidence/repair-3/inventory-repair-proposal.json.
