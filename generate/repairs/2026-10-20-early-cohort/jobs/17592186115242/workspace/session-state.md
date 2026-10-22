# Current state

Author-353 read latest feedback, all five retained findings, and history through
attempt 352. Preserved completed runtime repairs and strict regression checks.
Source, inventory, manifest and runtime files match retained protected hashes.

First test: job Python -B checks/batch_regressions.py --finding inventory
Exit 1: five historical stored banks retain the sign-extremum shortcut;
64/64 successes in the retained possible-history witness. All five generated
inventory entries were reproduced; none is untested.

Verification: job Python -B checks/recheck_status.py --output evidence/author-353
Exit 1 solely for finding 591f580cadb749294588. Four current-generator findings
pass: 17 practice source banks plus canonical replay, zero roots, shortcuts,
14 delivered records, controlled counterfactuals, native grading (7 accepted,
28 rejected), dependency pins and relocated five-record seeded output.
Five staged replacements and mappings remain verified and unapplied. Both
retained actual-UI screenshots visually inspected without observed layout defects.

Evidence: evidence/author-353/commands.json, results.json, outcome.md.
No runtime, database, engine, publication or image changes were made.

Next unfinished action: separate inventory remediation requested by finding
591f580cadb749294588, then fresh capture and strict recheck. Existing concrete
proposal: evidence/repair-3/inventory-repair-proposal.json. Database changes are
explicitly prohibited in this author job. Preserve strict failure and do not
substitute the proposed pool for captured inventory. An unchanged author retry
cannot alter stored banks.
