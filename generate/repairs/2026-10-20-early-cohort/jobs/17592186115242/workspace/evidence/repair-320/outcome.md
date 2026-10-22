The latest failure was reproduced before the retained generator checks:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/batch_regressions.py --finding inventory`
exits 1. All five captured historical generated records still have the
sign-only extremum shortcut. The retained possible-history witness succeeds on
64/64 draws; it does not describe all learner histories.

Full verification command:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/recheck_status.py --output evidence/repair-320`
also exits 1, preserving the inventory failure. The four current-generator
regressions pass: 17 complete source practice banks and canonical replay,
zero-root reachability, bank-role variation, and finite batch selection.
Three batches preserve their contrasts through shared delivery (14/14 records).
Controlled relevant and irrelevant changes pass. Native grading accepts 7
correct responses and rejects 28 incorrect responses. Dependency pins,
relocated execution, protected input/runtime hashes and the staged five-record
replacement mapping verify. See commands.json and results.json.

The root cause left to resolve is stored v2 content, not another current-generator
construction defect. For example, stored question
f4f00ddd-faa4-5195-9569-dbec2d0e2e6c (entity 17592186557444, seed 2712914515)
has x+2y=-5 and -2x+ky=0 with bank {-4,-2,0,2,4}; the sign cue identifies
the minimum, -4. Its complete archival replay and publication metadata are in
../generated-records.json. All five generated inventory records were tested;
original source questions remain distinguished from generated records.

`engine/rust/question_selection.rs:125` receives stored candidate entity IDs,
reads their difficulty and selects from those IDs. It does not call the Python
generator. Editing this package or publishing additional instances cannot
retire the existing five banks. The retained finding explicitly requests the
separate inventory-remediation workflow. The user's prohibition on changing
database content rules out performing that action in this author session.

Completed implementation and strict tests remain unchanged. The existing
instructional account still applies: eliminate x, solve the surviving
coefficient for k, then interpret contradiction or redundancy (canonical
f2c7cfd3-da43-5208-bd0e-21692357fabe; tutorial
e0c85152-daea-5a87-a3ba-81870558c7a2). No new construction change follows
from this stored-content finding. Existing rendering evidence is retained;
this pass makes no new rendering or visual-inspection claim.

Status: unsupported. The concrete remaining action is independent review and
separately authorized remediation using
../repair-3/inventory-repair-proposal.json, then fresh inventory capture and
the strict stored-pool regression. The proposal remains unapplied. No database,
engine, publication, image, source, runtime-package or other-job changes were
made. Further unchanged author retries cannot complete the stored-pool action.
