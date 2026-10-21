# Current repair state — pass 130

Read latest feedback, all five retained findings, and prior session state before
validation. First test reproduced the latest failure:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/batch_regressions.py --finding inventory`
Exit 1: all five captured historical v2 banks retain the sign-only extremum
shortcut. The possible-history witness succeeds 64/64; actual history is unknown.

Validation milestone:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/recheck_status.py --output evidence/repair-130`
Exit 1 solely for finding 591f580cadb749294588. All four current-generator
regressions pass: 17 complete practice source-bank replays plus canonical replay,
zero-root and fractional-bare cases, controlled counterfactuals, and three batches
(14 records) whose contrasts survive shared delivery filtering. Native grading
accepts 7 correct choices and rejects 28 wrong choices. Exact dependencies and
relocation pass. The staged replacements and protected runtime, manifest,
source and inventory hashes are verified. See evidence/repair-130/commands.json,
results.json and scope-resolution.json.

Reinspected retained actual UI screenshot evidence/repair-3/render/question-001.png:
system, choices, matrices, row operation and complete solution remain legible.
Runtime and presentation are unchanged, so existing rendering evidence applies.
No runtime, manifest, engine, source, publication or database changes were made.
Every strict executable regression is preserved, including the failed one.

Next unfinished step: separate inventory remediation using the verified
one-to-one proposal evidence/repair-3/inventory-repair-proposal.json, followed by
a fresh inventory capture and strict inventory regression. The retained finding
explicitly requires this separate workflow; database changes are prohibited here.
Inspected engine/rust/question_selection.rs:125-205: stored candidates are selected
without calling this generator. Another workspace runtime change cannot retire
those records. Status remains unsupported for the delivered-pool claim. Do not
repeat unchanged repair passes or substitute proposed replacements for capture.
