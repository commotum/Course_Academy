# 6. Database Commit

Python commits the validated transactions from Database Preparation. This stage uses no agent judgment about content or entity identities.

1. Connect to the existing writer for `/media/jake/SSD/EDB/math`. If a prior submission exists, recover its outcome and finish verification before starting a new one.
2. Preview the prepared EDN against the database version (basis) used during preparation. Check the proposed additions, retractions, and source attribution. A changed basis or validation failure returns to Database Preparation for reconciliation and a fresh preview.
3. Save the complete request before submitting, including the exact EDN, database target, source, UUIDs, expected basis, and unique request key.
4. Commit batches in dependency order, with one source per transaction. Use a basis guard so concurrent writes cannot silently invalidate the prepared changes.
5. If the response is missing or unclear, recover the receipt or retry the identical request with the same key. Establish its outcome before changing the transaction or creating a replacement request.
6. Read back the affected entities at the receipt's committed database version. Verify content, relationships, and sources; check the receipt for unexpected changes, including learner or engine facts. Confirm that preparing the same capture against that version produces no further content changes. If verification fails, recover the receipt and retry the read. Route a confirmed mismatch to Preparation for reconciliation; retain the confirmed commit and never treat it as uncommitted or blindly resubmit it.
7. Save the transaction, preview, receipt, and verification with the capture under `reference/`. Mark the import complete only after verification. Report success or durably saved pending work to the capture loop; only that loop selects the next activity.

Python classifies commit outcomes and routes rejected plans back to Database Preparation. Source-content gaps return to Activity Capture's agent through Preparation for a decision now. An interrupted commit or verification resumes from its saved state; it never causes the Math Academy activity to be repeated.

Keep completed captures, agent decisions, original images, and pending database work durably under `reference/` before selecting another activity. Retry temporary writer or connection failures with backoff while capture proceeds.

Process pending captures in their saved order through one database worker; establish any unknown commit outcome before later writes, and reprepare against the current basis when required. Pending persistence is distinct from completed question judgments; it is never reported as a successful import. Recovery runs automatically without asking Jake or exiting the capture loop. If durable storage itself is unavailable, retain the current state and retry saving before advancing.
