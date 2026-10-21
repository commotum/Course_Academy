# Current repair state — pass 64

Read feedback, all retained finding descriptions and prior history/state before
running tests. Preserved the existing generator, instructional account, runtime
manifest and staged replacement proposal. No new construction defect is reported.

First executed regression:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/batch_regressions.py --finding inventory`
Exit 1: five fully reproduced historical records still match captured inventory
and retain the sign-extremum shortcut. The possible new-seen-history witness
has 64/64 successes, conditional on that history rather than all learner histories.

Retained verification:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/recheck_status.py --output evidence/repair-64`
Exit 1 solely for finding 591f580cadb749294588. All four current-generator
regressions pass: bank shortcut, fractional bare-k source replay, zero roots,
and finite-batch contrasts. Seventeen source banks replay. Shared delivery
retains 14/14 records and contrasts. Relevant/irrelevant counterfactuals pass;
native grading accepts 7 correct choices and rejects 28 wrong choices. Relocation,
exact dependencies, protected hashes and all five replacement mappings pass.
See evidence/repair-64/commands.json and results.json.

Inspected retained actual-UI screenshot evidence/repair-3/render/question-002.png
and the source classification diagram. The screenshot is readable without
clipping. Reused rendering because runtime hashes remain unchanged; see
visual-inspection.json in this pass's evidence directory.

Unfinished step: separate inventory remediation must review/apply
`evidence/repair-3/inventory-repair-proposal.json`, recapture inventory, then rerun
the strict inventory regression. All five generated inventory records were
tested; none remain untested. affected-inventory.json points to complete records
through ../workspace/evidence/generated-records.json relative to author-64.
Original source questions are not marked generated.

The selector reads stored candidate IDs and difficulties directly
(engine/rust/question_selection.rs:125–195), without invoking this package.
Workspace generator edits cannot change those stored banks. Database changes,
publication and engine edits are prohibited by this task. Preserved the strict
failing check; status remains unsupported. Further identical generator passes
cannot resolve the stored-inventory finding without the separate workflow.
