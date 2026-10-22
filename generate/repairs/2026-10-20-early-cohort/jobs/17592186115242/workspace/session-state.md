# Author 618 verification, 2026-10-22

Preserved the current package and all completed repairs. Reproduced the latest
failure first with `checks/batch_regressions.py --finding inventory`: exit 1,
five affected captured records, 64/64 successes in the retained possible-history
shortcut witness. All five generated inventory records were tested; none remain
untested. Original source records were not marked generated.

Ran `checks/recheck_status.py --output evidence/author-618`: exit 1 solely for
591f580cadb749294588. The other four retained regressions pass; all 17 complete
practice banks and the canonical system replay. Three finite batches retain
contrasts before/after shared delivery (14 accepted). Native grading accepts
7 correct and rejects 28 wrong submissions. Exact dependencies and relocation
pass. Reinspected retained actual-UI question-002.png: equations, all five
choices, matrices and worked solution remain legible.

No runtime implementation change is justified by the remaining finding. Its
requested_change explicitly requires the separate inventory-remediation workflow.
`engine/rust/question_selection.rs:125` selects supplied stored entity candidates;
it does not invoke this generator to replace their banks. A workspace-only edit
cannot repair those captured selectable records. The task prohibits database
changes and engine repair. Five proposed replacements and their exact old/new
mapping remain verified and unapplied. The strict failing regression is retained.
Source, inventory, manifest and runtime hashes match the protected baseline.

Status: unsupported for the full delivered-distribution requirement. The source
skill and current generator are supported; the limitation is the prohibited
inventory remediation. Do not repeat an author-only loop against this unchanged
capture expecting a generator edit to resolve the stored-pool failure. Next step
belongs to the separate inventory-remediation workflow, followed by fresh capture
and the retained strict regression. No publication or database changes performed.

Evidence: evidence/author-618/commands.json, results.json, grader-report.json, outcome.md.
