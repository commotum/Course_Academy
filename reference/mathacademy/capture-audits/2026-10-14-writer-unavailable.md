# Capture import failure — 2026-10-14

The status card's truncated `Import: Command [...] returned non-zero exit status 1` referred to shared database batch c07cea05-e22a-4a43-85d6-e6d4e3eaea11, not a failed browser answer. Captures continued while the batch was pending.

## Cause

The saved CLI error was `Unavailable / transport/remote-error`. A native exact-request probe using the deployed EDB library exposed `remote_code=service/unavailable`: the socket was still listening, but the writer no longer accepted transactions. Course Academy's writer wrapper waited only on stdin and never checked the transaction service's availability, leaving this failed writer alive indefinitely.

After adding that availability check, service logs exposed the underlying EDB background indexing error, `tree/unapplied-edit`. A later directory's sparse parent lower bound can sort before the exact lower bound of its first leaf. Merge and no-history discovery incorrectly used the first leaf's own bound, omitting edits in that gap. Both paths now inherit their parent directory's bound for the first leaf. There is no format or schema migration.

The original deployed library reproduced this failure in a two-leaf, two-directory in-memory tree. The fixed source passes a 12-case regression covering all six index orders with current and history trees. All 60 enabled EDB core unit tests passed; three environment-dependent tests remained ignored. The patch is applied to /home/jake/Developer/EDB and archived at `2026-10-14-writer-unavailable/edb-tree-gap.patch`.

## Recovery and verification

The original request `capture-03d77566-9951-44e4-8886-770330f4f7e4`, basis 2350, was retained byte-for-byte until the writer explicitly rejected it as stale. Its rejection and complete request are archived in the batch's requests directory. Only then was the same whole-activity group reprepared and previewed at the new basis.

The **200-question, 24-activity** batch committed and verified at **2353 → 2354**, request `capture-33ee5c1c-7c95-496e-8c61-533f79e42fba`: 3630 assertions, 87 retractions. The receipt verifies unchanged learner/engine facts and a no-op reimport. Eight separately protected content/historical-response omissions remain; they were not overwritten to clear the transport error. No undersized flush was used.

The writer linked to the repaired EDB library was deployed with the old binaries and build receipts preserved. Its live service then logged `INDEX_COMPLETED basis=2355 jobs=1`, confirming background indexing completed at the previous failure point.

The Course Academy wrapper now checks writer/listener availability every 250 ms, logs safe failure codes, gracefully shuts down, and exits unsuccessfully so its existing supervisor can recover it. Normal stdin shutdown remains supported. The two writer lifecycle tests passed.

Capture transaction submission now uses the native API against the deployed library, preserving the saved EDN representation, source, key and basis guard, and retaining minimal confirmed receipts if report opening fails. Safe remote error codes are exposed without arbitrary error messages or transaction values. CLI stdout/stderr are durably saved with the request hash, and status messages no longer print an entire command line. The native submission argument test, 88 focused Python tests, and a later 32-test verification of helper caching, lineage and diagnostic preservation passed.

Three ordinary capture workers were checkpoint-restarted to load the importer changes; the active Foundations diagnostic was left running. Browser answers, pacing, course enrollment, capture evidence, and the 200-question floor were preserved.

Detailed probe, deployment, batch, and restart records are under `2026-10-14-writer-unavailable/`.
