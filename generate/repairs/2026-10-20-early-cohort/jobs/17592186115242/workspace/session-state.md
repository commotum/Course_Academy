# Current state

Author-535 verification milestone, 2026-10-22.

Preserved all existing runtime repairs. Reproduced latest failure first:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/batch_regressions.py --finding inventory`
exits 1: five historical banks affected; retained possible-history witness
has 64/64 shortcut successes.

`-B checks/recheck_status.py --output evidence/author-535` exits 1 solely
for 591f580cadb749294588. All four generator regressions pass: source replay,
zero roots, construction and finite-batch counterfactual/shortcut checks,
shared delivery (14 records), native grading (7 accepted/28 rejected), exact
dependencies and relocation. All five staged replacement mappings and
protected input/runtime hashes verify. Captured generated inventory is fully
tested. Reused unchanged actual-UI rendering; visually inspected question-002.
No runtime, engine, database, source, publication or other-job edits.

Status: unsupported because the required captured-pool regression fails.
Historical banks are selected from stored inventory independently of this
package. The retained review requires separate inventory remediation, while
this author task explicitly prohibits database changes. Five complete reviewed
proposal records remain staged and unapplied; the strict check is preserved.

Evidence: `evidence/author-535/commands.json`, `results.json`, `outcome.md`;
`affected-inventory.json`, `evidence/generated-records.json`,
`evidence/repair-3/inventory-repair-proposal.json`.

Next unfinished step: separately authorized remediation of the five generated
identities, fresh inventory capture, then strict pool recheck. Do not repeat
unchanged author passes, weaken the regression, or substitute hypothetical
replacements for captured records. No additional runtime defect is demonstrated.
