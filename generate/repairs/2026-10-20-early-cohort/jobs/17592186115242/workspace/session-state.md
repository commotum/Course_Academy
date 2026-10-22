# Current state

Author-384 reproduced the latest strict inventory failure first and preserved all completed runtime repairs. Current evidence: `evidence/author-384/commands.json`, `results.json`, `outcome.md`.

Ran job Python with `-B checks/batch_regressions.py --finding inventory`: exit 1, five affected captured records, 64/64 possible-history shortcut successes. Then `-B checks/recheck_status.py --output evidence/author-384`: exit 1 solely for that inventory finding. Four current-generator regressions pass; 17 source banks, zero roots, counterfactuals, conditional variation, shared delivery (14 records), native grading (7 accepted/28 rejected), pinned dependencies and relocated deterministic execution pass. Protected input/runtime/manifest hashes and staged replacement mapping verified unchanged. Reused unchanged UI rendering and visually inspected question-002.png.

Affected identities: `affected-inventory.json`; complete historical records: `evidence/generated-records.json`; verified staged proposal: `evidence/repair-3/inventory-repair-proposal.json`. Affected evidence paths resolve relative to supplied author-384 evidence_root. All non-source inventory records tested.

Unfinished: finding 591f580cadb749294588 requires separate stored-inventory remediation and fresh capture. This job prohibits database changes. Keep the strict failure and existing source coverage. Runtime edits cannot change stored-pool eligibility. Resume dependent work when captured inventory or authorization changes, or new concrete generator feedback arrives. Status unsupported; nothing published.
