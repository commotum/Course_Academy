The existing runtime repairs are preserved. The latest failure was reproduced
first with `checks/batch_regressions.py --finding inventory` (exit 1): five
captured stored records and 64/64 shortcut successes in the retained possible
learner-history scenario. This is a demonstrated possible history, not a claim
about every learner.

`checks/recheck_status.py --output evidence/author-577` exits 1 solely for
finding 591f580cadb749294588. All four generator findings pass; 17 complete
source banks replay; 14 delivered records retain tested contrasts; native
checks accept 7 correct choices and reject 28 incorrect choices. Protected
runtime/source/inventory/manifest hashes and the five staged replacements
verify. No generator change is supported by a new counterexample in this pass.
The retained actual UI screenshot `evidence/repair-3/render/question-002.png`
was visually inspected: equations, choices, augmented matrices and solution
are legible without clipping. Its renderer was not rerun because the protected
runtime and replacement records are unchanged.

The remaining repair is the separate inventory-remediation action explicitly
requested by finding 591f580cadb749294588. Its one-to-one proposal is already in
`evidence/repair-3/inventory-repair-proposal.json`. Applying it or retiring the
old records changes database content, which the user expressly prohibits in
this author job. Workspace generator edits cannot alter those stored banks.
No database, engine, publication, image or other-job changes were made. The
strict regression remains failing; no proposed pool was substituted for the
captured inventory. Status is unsupported until separate remediation and a
fresh inventory capture establish the required selectable-pool result.
