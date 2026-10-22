# Author 340 verification

Status: unsupported. Completed repairs and strict regression declarations are
preserved. No runtime construction change is justified by the unchanged evidence.

Read feedback and all five retained findings through attempt 339, all supplied
source questions with complete banks and solutions, lesson definitions, the
prerequisite row-reduction example, and the existing instructional account.
Canonical f2c7cfd3-da43-5208-bd0e-21692357fabe requires elimination to
`(k+4)y=-5`; tutorial e0c85152-daea-5a87-a3ba-81870558c7a2 defines inconsistency
as no solutions and dependence as infinitely many solutions. No source change
invalidates the old counterexample.

First check: job Python -B checks/batch_regressions.py --finding inventory.
Exit 1 reproduced five defective captured banks and 64/64 shortcut successes in
the retained possible learner-history scenario. This conditional witness does
not describe every actual learner history. Every generated inventory record was
tested; original source questions remain excluded from remediation.

Then: job Python -B checks/recheck_status.py --output evidence/author-340.
Exit 1 is solely the inventory finding 591f580cadb749294588. Full command output
and individual exit codes are in commands.json; results.json records protected
input and runtime hashes and the validation summary.

- Fidelity: 17 complete practice banks and the canonical system replay pass.
- Correctness: printed-system witnesses, fractional bare-k and zero-root cases pass.
- Grading: native grader accepts 7 correct choices and rejects 28 wrong choices.
- Variation: four generator findings pass, including three small batches with
  14/14 delivery survivors, within-sign-group contrasts, relevant-evidence answer
  changes, and irrelevant-evidence answer preservation.
- Packaging: pinned dependencies, deterministic relocation, and unchanged runtime,
  manifest, source and inventory hashes pass.
- Rendering: visually inspected both retained actual-UI screenshots under
  evidence/repair-3/render and the source tutorial flowchart. Prompts, choices,
  matrix operations and solutions are readable. No presentation changed.

The five-record proposal at evidence/repair-3/inventory-repair-proposal.json
still matches this generator and the delivered replacement records, but remains
unapplied. The selector consumes stored candidate identities independently of
this entrypoint (engine/rust/question_selection.rs, select). A generator edit
cannot alter the five stored banks. Resolving this finding requires the separate
inventory-remediation workflow named in the review, then fresh inventory capture.
Database changes, publication and engine changes are prohibited in this job.
No strict test was waived; no source family or valid response was removed.
