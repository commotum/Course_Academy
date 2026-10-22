# Current repair state — pass 199

Read latest feedback and all five retained findings. First executed test:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/batch_regressions.py --finding inventory`
Exit 1: all five historical banks retain the sign-extremum shortcut; 64/64
successes describe a possible learner-history witness, not observed usage.

Validation:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/recheck_status.py --output evidence/repair-199`
Exit 1 solely for 591f580cadb749294588. Four generator regressions pass;
17 complete source banks replay; 14 records survive shared delivery with
conditional contrasts; native grading accepts 7 correct and rejects 28 wrong
responses. Relocation, dependencies, protected hashes and staged replacement
mapping pass. All five generated inventory records were reproduced; none are
untested. Commands and results: evidence/repair-199.

Reinspected unchanged actual-UI screenshot
`evidence/repair-3/render/question-002.png`: prompt, choices, matrices,
(k-12)y=3 and k=12 conclusion are legible and consistent. Retained prior
rendering because runtime and records have not changed.

Next required state change: separate reviewed inventory remediation using
`evidence/repair-3/inventory-repair-proposal.json`, then a fresh inventory
capture. Native selection reads stored entity IDs independently of this
entrypoint (question_selection.rs:125-197). Database changes, publication and
engine edits are prohibited here. Preserve the strict failing regression and
unsupported status; no additional runtime defect is demonstrated.
