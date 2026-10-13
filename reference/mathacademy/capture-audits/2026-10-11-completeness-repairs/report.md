# Capture completeness repairs — 2026-10-11

The original audit remains preserved in `../2026-10-11-completeness/`. This report records the first repair pass. Historical source reviews subsequently resumed with the user's explicit authorization; see `../2026-10-11-backlog-repairs/report.md` and the current durable results in this directory for later repairs.

## Applied and verified

- Re-extracted all authored problem bodies, including proof stages and sibling table sections, without duplicating nested content or mixing solutions into prompts. Added authored field-position checks and trusted enclosing-history grades for completed proofs.
- Restored all 35 truncated prompts in the original seven affected captures. Reprocessed those captures plus foundations quiz 14116310 through the normal database preview, commit, and readback workflow. All eight verified with zero omissions; all 35 question IDs are present and match the restored database prompts and field counts. The four previously absent proof questions are now imported.
- Fixed the quiz's answer attribution and recovered its missing blank controls from original source evidence. The repaired questions pass authoritative source-answer validation.
- Added authoritative answer validation before capture handoff, a bounded focused evidence review, and durable supported/unavailable findings. Missing source evidence does not stop activity progress or become a guessed answer.
- Persist accepted preparation answer repairs into raw capture records after verified import or no-change reconciliation. Preserve originals and exact source hashes; do not alter an unresolved request or preview-only capture.
- Recovered 48 displayed course percentages directly from saved Learn HTML and 46 before/after topic-color and band comparisons. Two earliest captures have no saved baseline; their comparisons remain unavailable. Original times, XP, account ledgers, and retake state remain intact.
- Applied 59 already completed, quotation-checked legacy answer attributions to 17 archived packages, with immutable originals. This is a local provenance repair, not a claim of new database verification or completion of the entire legacy audit.
- The monitor now shows pending imports separately from terminal captures with omissions. A verified transaction does not mean unsupported omitted questions were imported.

Evidence: `verified-repairs.json`, `restored-question-readback.json`, `progress-recovery.json`, and `legacy-provenance/applied-reviews.json`. Original packages, solver decisions, source HTML, and database receipts remain under each capture's `repairs/` directory.

## Historical work remaining at the end of the first pass

- Prepared saved-source candidates for 35 further completed archives, covering 483 question records. 83 candidates already pass source-field validation, but the packages still require final source review and verified reprocessing. Candidates do not overwrite the finished packages or database facts. See `later-source-candidates.json` and each package's `repairs/source-candidates-v1/`.
- Of 3,440 unique legacy questions flagged by strict provenance validation, 59 received applied supported findings. The other 3,381 remain unresolved by this repair run. The initial 64-question review had five unavailable findings; it did not complete the broader audit. This is missing confirmation of source attribution, not evidence that all those mathematical answers are wrong.
- Automatic approval initially rejected continuing historical source reviews because the workflow sends archived problem text, worked solutions, and diagrams to the existing separate Codex capture solver. The first pass stopped there. The user later explicitly authorized those historical repairs, and the narrowed reviews resumed. `legacy-provenance/solver-payload-review.json` records the restricted payload and destination; it excludes learner attempts, credentials, profile files, and full checkpoints.
- Seven missing factorial question IDs cannot be safely restored from the old manual transaction: it inferred answer-control types and choices that were absent from the saved source. A fresh, read-only history capture also exposed no answer controls. The gap is recorded under `../../factorials-13831129/repairs/current-lineage-reconciliation/`; no guessed choices were replayed.
- The original audit's 23 capture-only diagnostic records and 29 intentionally uncommitted manual records remain outside normal database import. Recovery honors capture-only status.

## Validation and operation

The final full regression run passed 355 test executions, including nine duplicate executions caused by a temporary imported test class. The final discovery contains 346 distinct tests. After removing that duplicate discovery, all seven focused recovery tests passed again. `git diff --check -- capture` passed.

All four runners checkpoint-stopped cleanly and restarted with the fixes. The saved post-restart status shows all four running with no reported errors. Pending imports and terminal omissions still exist; these historical repair results do not declare the entire backlog complete. See `runners-after-fixes.json` for the observed counts and times.

Reviewed and updated activity capture, post-activity processing, preparation, and commit documentation. `capture/principles.md` is unchanged. The 500 ms minimum browser latency and existing activity-specific timing policies remain in place. Database Commit still owns writes; no completed Math Academy activity was replayed for these repairs.
