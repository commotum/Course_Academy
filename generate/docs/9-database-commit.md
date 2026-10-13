# 9. Database Commit

Python submits the validated transactions from [Database Preparation](8-database-prep.md). Follow [$edb](../../skills/edb/SKILL.md) through the configured EDB CLI and existing writer; this stage makes no new content or identity judgments.

1. Recover any saved submission's outcome and verification before starting another, checking its database target and immutable lineage.
2. Preview the original prepared EDN with its source at the preparation basis, using the same native validation predicates as the writer; confirmed basis changes or validation failures return to Preparation.
3. Save the complete durable request before submission, including exact EDN, target, lineage, source, UUIDs, expected basis, and a unique request key.
4. Commit batches in dependency order with one explicit source per transaction and a basis guard protecting the prepared reads.
5. If the outcome is unknown, recover the receipt or retry the identical saved request with the same key before changing intent or starting dependent writes.
6. Verify affected questions, fields, answers, plot references, difficulty, knowledge-point membership, and attribution at the report's exact `db_after`; inspect datoms for unexpected learner or engine changes and confirm repeat preparation produces no content changes.
7. Save the preview, request, receipt, and verification with the generation package, then mark verified work complete and recheck [Inventory](2-inventory.md) to continue pending activity preparation.

Previews are speculative: submit the original logical forms, never preview entity IDs or a datom diff. A confirmed commit remains committed if readback fails; recover its receipt and retry verification. A confirmed mismatch returns to Preparation for reconciliation without blindly resubmitting the successful transaction.

Process durable pending batches through one database worker. Retry temporary failures with backoff, preserve saved requests across restarts, and retain requests with different or unknown lineage for reconciliation instead of silently retargeting them. After each committed batch, prepare dependent work at the appropriate current basis.

Report pending, rejected, no-change, and verified outcomes separately. Inventory counts only accepted, verified questions and remains pending while a shortage exists; database persistence does not itself mark a question as presented, reserved, or answered.
