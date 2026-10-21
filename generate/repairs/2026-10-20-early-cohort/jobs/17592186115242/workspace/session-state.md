# Current repair state — pass 118

Preserved completed runtime repairs, all five regression declarations, and the
staged one-to-one inventory replacement proposal. No runtime, engine, source,
inventory, publication, or database changes were made.

Read feedback and retained findings first. The first executed test reproduced
latest finding 591f580cadb749294588:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/batch_regressions.py --finding inventory`
Exit 1: five captured historical banks retain the shortcut; the retained possible
new-seen history gives 64/64 shortcut successes. Actual learner history is unavailable.

Verification:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/recheck_status.py --output evidence/repair-118`
Exit 1 solely for the historical inventory finding. Four current-generator
regressions pass. All 17 practice source banks and canonical replay pass.
Three batches retain contrasts across 14 delivered records after shared filtering;
relevant and irrelevant counterfactuals pass. Native grading accepts 7 correct
and rejects 28 wrong choices. Relocation, pinned dependencies, protected hashes,
and staged replacement mappings pass. Commands and results: evidence/repair-118.
Reinspected bound actual UI screenshot evidence/repair-3/render/question-001.png:
prompt, choices, matrices, row operation and contradiction are legible, without
visible clipping or overlap. Runtime and captured inputs match retained hashes.

Unfinished: separate inventory remediation explicitly named in the retained
finding, followed by inventory recapture and strict recheck. Verified proposal:
`evidence/repair-3/inventory-repair-proposal.json`; it remains unapplied.
The native selector reads stored entities independently of this generator.
Workspace generator changes cannot change already stored answer banks.
Database changes and publication are prohibited. The strict regression remains
failing; status is unsupported for the delivered-pool claim.
