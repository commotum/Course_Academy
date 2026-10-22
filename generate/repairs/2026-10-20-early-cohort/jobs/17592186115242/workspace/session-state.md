# Current state

Existing generator repairs and the unapplied five-record replacement proposal
are preserved. Latest evidence: evidence/repair-331/commands.json, results.json,
grader-report.json and outcome.md.

First command: job Python -B checks/batch_regressions.py --finding inventory
(exit 1: five historical banks; 64/64 possible-history shortcut successes).
Then: job Python -B checks/recheck_status.py --output evidence/repair-331
(exit 1). All four current-generator finding regressions pass. Source replay,
shared delivery (14/14), counterfactual checks, native grading (7 accepted,
28 rejected), exact dependencies, relocation and proposal bindings pass.
Retained actual-UI screenshots question-001.png and question-002.png were
visually inspected again. Runtime and presentation are unchanged. All five
generated inventory records are audited; original source questions are excluded
from affected IDs. Evidence paths resolve relative to author-331.

The selector reads stored candidate entities independently of this generator.
Finding 591f580cadb749294588 explicitly requires separate inventory remediation;
this job prohibits database changes. No workspace runtime change can update or
retire those stored banks. The strict check remains failing, not waived.

Next unfinished action: independently review and apply the separate inventory
remediation proposal at evidence/repair-3/inventory-repair-proposal.json, then
recapture inventory and rerun the strict regression. That action is outside this
job's authorized scope. Current status: unsupported for the stored pool. No
runtime, database, source, engine, publication or image changes in this pass.

Do not repeat another unchanged full audit on continuation. First inspect whether
inventory changed or new concrete generator feedback exists; otherwise the same
outside-scope action remains unfinished. This does not waive the strict check.
