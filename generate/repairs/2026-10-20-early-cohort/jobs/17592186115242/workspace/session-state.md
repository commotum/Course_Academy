# Current repair state — pass 215

Read feedback and all five retained findings. Reproduced the latest failure first:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/batch_regressions.py --finding inventory`
Exit 1: all five historical generated records still have the sign-extremum
shortcut. Source and inventory are unchanged. No new generator defect was shown.

Ran:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/recheck_status.py --output evidence/repair-215`
Exit 1 only for historical inventory. Four current-generator regressions pass,
including 17 complete source-bank replays and 14 delivery-filtered records with
counterfactual/conditional shortcut checks. Native grading: 7 acceptance and
28 rejection checks pass. Dependency pins, relocation and the complete proposed
replacement mappings verify. Reinspected the retained actual-UI screenshot.

Verified the causal boundary in engine/rust/question_selection.rs:125: selection
uses stored candidate entities and difficulty, independently of this package.
No workspace generator edit can change the five captured stored banks. Preserved
all runtime repairs, source families, complete banks and strict failing tests.
No database, engine, source or publication changes were made.

Next unfinished step is the separate inventory-remediation workflow requested by
finding 591f580cadb749294588, then a fresh capture and strict recheck. The five
reviewable replacements are already staged in evidence/repair-3. This task
explicitly prohibits applying the required database changes. Do not repeat
unchanged validation passes, weaken the regression, or substitute proposed
records for captured inventory. Resume only with new evidence or authorization
for the separate workflow. Status remains unsupported for the historical pool.

Evidence: evidence/repair-215/{initial-reproduction,commands,results,grader-report}.json.
The strict inventory witness again has 64/64 shortcut successes in the retained
possible-history scenario. No new runtime defect or input change was observed.
The retained screenshot inspected this pass is
evidence/repair-3/render/question-001.png; its equations, choices and solution are
readable without clipping. The five complete proposed replacements remain staged
in evidence/repair-3/inventory-repair-proposal.json, unapplied.
