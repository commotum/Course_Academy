# Author 662 result

Latest failure reproduced first with the job Python:
`-B checks/batch_regressions.py --finding inventory`.
Exit 1: five reproduced historical questions, 64/64 sign-extremum successes
in the retained possible-history witness. Stored prompts, solutions, complete
banks, keys, IDs and generation metadata match archival replay. All generated
inventory questions were tested; original source questions were not relabeled.

Then ran `-B checks/recheck_status.py --output evidence/author-662`.
Exit 1 solely for finding 591f580cadb749294588. The four generator regressions
pass, including 17 complete source banks and canonical replay, zero-root and
fractional cases, three finite batches (14 accepted records), and relevant and
irrelevant counterfactuals. Native grading accepts seven correct submissions
and rejects 28 incorrect submissions. Relocation and dependency checks pass.
The staged five-record replacement mapping and protected hashes are verified.
Commands and outputs are in commands.json; results are in results.json.

Reinspected the retained actual-UI screenshot
`evidence/repair-3/render/question-001.png`: prompt, choices, matrices,
elimination and contradiction are legible and consistent. No runtime change
requires a new rendering.

The existing instructional account remains applicable: eliminate x, solve the
remaining coefficient for k, and distinguish contradiction from redundancy
(canonical f2c7cfd3-da43-5208-bd0e-21692357fabe; tutorial
e0c85152-daea-5a87-a3ba-81870558c7a2). No outstanding generator construction
failure is demonstrated. Runtime repairs and all strict regression contracts
are preserved.

The remaining finding explicitly requires the separate inventory-remediation
workflow. Its reviewed-input proposal is
`evidence/repair-3/inventory-repair-proposal.json`; it has not been applied.
A workspace generator edit cannot alter those stored banks or their selector
eligibility. Database changes are explicitly prohibited, so the retained pool
test remains failing and the result is unsupported. No publication, engine,
database, source-capture or runtime changes were made. Another identical author
retry cannot resolve this state; apply separately authorized remediation and
recapture inventory before rerunning the strict pool check.
