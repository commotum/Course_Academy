# Current state: author 927

Completed runtime repairs preserved; no runtime changes. Latest feedback and all five retained findings read. Exact latest failure reproduced first.

Commands (job Python `/home/jake/Developer/Course_Academy/.venv/bin/python`):
- `-B checks/batch_regressions.py --finding inventory`: exit 1, five affected historical banks, 64/64 possible-history shortcut successes.
- `-B checks/recheck_status.py --output evidence/author-927`: exit 1 solely for 591f580cadb749294588. Four current-generator findings pass; 17 practice banks and canonical case replay; 14 delivered records retain contrasts; native grader accepts 7 correct and rejects 28 incorrect choices. Counterfactuals, relocation, dependencies, protected hashes and staged mappings pass.

Evidence: evidence/author-927/initial-reproduction.json, commands.json, results.json, disposition.md. Existing actual-UI screenshot visually inspected. No database writes or publication.

Next required step: separate inventory remediation using `evidence/repair-3/inventory-repair-proposal.json`, then fresh inventory capture and strict recheck. Both database changes and publication are prohibited in this task. Preserve failing acceptance test and completed repairs; repeating generator edits cannot change stored banks.
