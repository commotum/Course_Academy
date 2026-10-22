# Current state — pass 272

Preserved runtime and all five declared regressions. Read feedback, retained
findings, latest history event, instructional account and source context.
No additional generator construction failure was demonstrated.

First check: supplied Python with
`-B checks/batch_regressions.py --finding inventory`.
Exit 1: five historical banks remain affected; possible-history witness 64/64.

Then ran supplied Python with
`-B checks/recheck_status.py --output evidence/repair-272`.
Exit 1 solely for finding 591f580cadb749294588. Four generator regressions pass:
17 complete source banks plus canonical replay, zero roots, fractional bare-k,
shortcut and counterfactual checks, 14/14 delivered records, native grading
(7 accepted, 28 rejected), relocation and exact dependency pins. Existing
replacement mapping and protected runtime/input hashes verify. None of the
generated inventory remains untested. Reinspected retained actual-UI screenshot.

Evidence: evidence/repair-272/{commands,results}.json and outcome.md.
Status unsupported. Unfinished action: separate inventory remediation using
evidence/repair-3/inventory-repair-proposal.json, then fresh capture and strict
recheck. This task prohibits those database changes. Repeating generator edits
against unchanged stored records cannot resolve that action; retain its failure.
No runtime, engine, database, publication, image, source or other-job changes.
