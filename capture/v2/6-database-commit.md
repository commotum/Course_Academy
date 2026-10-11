# 6. Database Commit

Commit the validated transactions from Database Preparation.

1. Connect to the existing writer for `/media/jake/SSD/EDB/math`. If a prior submission exists, recover its outcome and finish verification before starting a new one.
2. Preview the prepared EDN against the database version (basis) used during preparation. Check the proposed additions, retractions, and source attribution. A changed basis or validation failure returns to Database Preparation for reconciliation and a fresh preview.
3. Save the complete request before submitting, including the exact EDN, database target, source, UUIDs, expected basis, and unique request key.
4. Commit batches in dependency order, with one source per transaction. Use a basis guard so concurrent writes cannot silently invalidate the prepared changes.
5. If the response is missing or unclear, recover the receipt or retry the identical request with the same key. Establish its outcome before changing the transaction or creating a replacement request.
6. Read back the affected entities at the receipt's committed database version. Verify content, relationships, and sources; check the receipt for unexpected changes, including learner or engine facts. Confirm that preparing the same capture against that version produces no further content changes.
7. Save the transaction, preview, receipt, and verification with the capture under `reference/`. Mark the import complete only after verification, then return to Queue Processing.

Content recovery belongs to Database Preparation. An interrupted commit or verification resumes from its saved state; it never causes the Math Academy activity to be repeated.
