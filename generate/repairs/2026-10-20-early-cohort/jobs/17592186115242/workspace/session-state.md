# Current state — pass 299

Preserved completed runtime repairs, manifest, all five strict finding checks,
and the unapplied replacement proposal. No runtime, engine, database, source,
publication or image changes.

First test: job Python `-B checks/batch_regressions.py --finding inventory`.
Exit 1: five historical banks; possible-history shortcut witness 64/64.

Verification: job Python `-B checks/recheck_status.py --output evidence/repair-299`.
Exit 1 solely for finding 591f580cadb749294588. Four generator regressions,
17 complete source banks and canonical replay, delivery 14/14, native grading
(7 accepted, 28 rejected), exact dependencies, relocation and replacement
bindings pass. Commands/results/outcome: evidence/repair-299/.

Visually reinspected retained actual-UI question-002.png. Bound runtime,
source and inventory hashes remain unchanged, so retained rendering applies.

Next unfinished step requires the separate inventory-remediation workflow named
by the finding: remediate five stored generated records, capture fresh inventory,
then rerun the strict regression. This task prohibits database changes. Selector
reads stored entities independently of generator output. Do not weaken the
regression or substitute hypothetical replacements for captured inventory.
Repeated unchanged author retries cannot resolve this external-state condition.
