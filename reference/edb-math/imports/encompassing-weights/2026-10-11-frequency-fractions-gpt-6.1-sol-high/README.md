# Committed encompassing weights

**Committed and verified in `math` at basis 1308**, following the user's instruction to transact the weights and use **`:agent/gpt-6.1-sol-high`** as the source. The existing contributor entity `17592186045436` was reused.

The [transaction](transaction.edn) added **1,730 relationships across 533 source topics**, using the approved original frequency estimates rounded to 1/5, 1/4, 1/3, 2/5, 1/2, 3/5, 2/3, 3/4, 4/5, or 1. Every relationship's source, target, fraction, numerical weight, selected account, and observation counts matched the previously approved proposal. Account evidence remains separate, including single-observation estimates.

Pinned reads and the passing native preview used basis **1307**. The durable transaction advanced **1307 → 1308**, asserting **6,920 domain facts and one timestamp**, with no retractions. Every assertion is attributed to the requested source. No engine parameters or learner facts changed.

[Commit verification](commit-verification.json) confirms exact agreement with the validated preview and reads every domain assertion and its source back at committed basis 1308. [Receipt](receipt.edn), [exact request](request.json), and [receipt envelope](receipt-request.json) preserve the committed outcome and stable request key. [Selected relationships](selected-relationships.json) retain all account evidence; [coverage audit](coverage-override-audit.json) records the explicit-edge effects.

`commit.py` prepared the fresh snapshot, checked that the approved weights were unchanged, previewed, and submitted the saved request using its basis guard. Its recovery path reuses the original request and saved receipt; do not create another request to repeat this import. The first read-back pass encountered UUID serialization in existing topic facts; verification was corrected and completed from the retained receipt without a second submission.

The earlier [Codex request](../2026-10-11-frequency-fractions-r2/README.md) remains preserved and unsubmitted. The committed source is the model contributor requested by the user. See the [methodology report](../../../../../encompassing-report.md).
