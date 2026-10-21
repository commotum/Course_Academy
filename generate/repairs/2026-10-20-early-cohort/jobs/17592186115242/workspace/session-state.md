# Current repair state — pass 49

Read latest feedback and retained history, prior session state, instructional
account, source lesson/canonical example, and required generation/validation docs.
First executed test:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/batch_regressions.py --finding inventory`
Exit 1: five captured historical banks retain the sign-only extremum shortcut;
the conditional possible-history witness succeeds 64/64 times.

Validation:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/recheck_status.py --output evidence/repair-49`
Exit 1 solely for finding 591f580cadb749294588. All four current-generator
finding checks pass. Source banks, zero roots, sampler/batch shortcut checks,
14 delivered records, native grading (7 accepted/28 rejected), pinned dependencies
and seeded relocation pass. Five staged replacements and mapping verify.
Protected runtime, manifest, source and inventory hashes are unchanged.
Reinspected retained UI screenshot: readable, no clipping.

No runtime edit is supported by the unchanged failure. The next unfinished
state-changing action is the separate inventory-remediation workflow required
by the finding: review/apply staged replacements, recapture inventory, rerun
strict check. Database changes/publication are explicitly forbidden here.
Preserve all repairs and strict failing regression; do not replace captured
inventory with the hypothetical proposal or repeat unchanged repair cycles.

Evidence: evidence/repair-49/commands.json, results.json, inventory-results.json,
scope-diagnosis.json; affected-inventory.json; evidence/generated-records.json;
evidence/repair-3/inventory-repair-proposal.json. Affected evidence paths resolve
relative to author-49 as ../workspace/evidence/generated-records.json.
