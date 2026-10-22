# Author 662 — 2026-10-22

Existing runtime repairs and all five strict regression contracts preserved.
Read feedback, five retained findings and latest history event. Latest failure
reproduced first with `checks/batch_regressions.py --finding inventory`: exit 1,
five historical records, 64/64 shortcut successes in the possible-history witness.

Ran job Python with `-B checks/recheck_status.py --output evidence/author-662`.
Exit 1 solely for finding 591f580cadb749294588. Four current-generator regressions
pass; 17 source banks plus canonical replay, 14 delivered records, seven native
acceptances and 28 rejections, relocation and protected hashes pass. Existing
replacement mapping verified, not applied. Retained UI screenshot visually
reinspected. No runtime, source, database, engine or publication changes.

Next unresolved action belongs to separate inventory remediation using
`evidence/repair-3/inventory-repair-proposal.json`, followed by fresh capture and
strict stored-pool validation. Workspace-only changes cannot change those stored
banks. Do not waive the test or repeat unchanged author investigations.
Fresh commands, results and outcome: evidence/author-662/.
