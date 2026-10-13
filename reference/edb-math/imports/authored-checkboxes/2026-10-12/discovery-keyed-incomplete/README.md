# Keyed incomplete captures: committed

**Committed and verified in two independently refreshed groups.** Conversions: **1853 → 1854**; solution corrections: **1854 → 1855**. Original preparation captured basis **1846**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. Contributor: **`:agent/gpt-6.1-sol-high`**, verified against the captured database and every speculative and committed datom.

| Group | Scope | Forms | EDN bytes | Confirmed basis |
| --- | --- | ---: | ---: | --- |
| 1 | Convert 69 questions across 65 KPs | 897 | 238,068 | 1853 → 1854 |
| 2 | Seven separate worked-solution corrections | 14 | 14,408 | 1854 → 1855 |

Each group was freshly captured, natively previewed, committed, and read back before the next. Group 1 creates **212 checkbox fields and 424 owned Boolean answers**, detaches 123 attached old radio fields, and retains all **744 original field/answer entities** unchanged. All stored answer-key selections are preserved. q-37456 (`17592186420504`) remains unrated; the other 68 retain their ratings. No canonical membership or saved learner presentation/response was present in the fresh scope.

## Resolution classes

**55 duplicate captures:** Each has an unkeyed field and a keyed duplicate. Both complete banks map to the same subsets. Both old fields are detached, without modifying or deleting either bank. Before submission, q-40639’s unkeyed duplicate was already detached by a concurrent repair; that repair was preserved. The refreshed request omits its redundant retraction, while retaining and verifying both original banks unchanged. No missing key is guessed or repaired on an old field. All 620 old answer IDs across the 69 questions have explicit subset mappings in the conversion plan.

**14 single-field captures:** The current database supplies keys and worked solutions that were incomplete in the historical discovery inventory. The existing database keys remain authoritative. No study-vault key was consulted.

**Diagrams and source labels:** Ten essential problem diagrams were inspected directly. Selection preserves the actual source universe, including point C in q-162747 and statement IV in q-155956 even though some old banks omit those individual labels. q-76219's empty correct subset becomes three explicit false answers. The wrong “II and II only” option in q-36477 maps literally to `{II}`; no intended typo correction is invented.

**Four wording clarifications:** q-171334 specifies comparison of logical forms for arbitrary truth values; q-95915 specifies reduced/thin QR and universally required properties; q-53000 states the captured kite/trapezoid conventions; q-94772 makes statement I's intended maximum-possible-count reading explicit. The Math Academy **III-only key for q-94772 is preserved**, as requested. Its worked solution is preserved too, and the earlier key-repair proposal is withdrawn. Other edits label the cases and add “Select all that apply.” and unchecked-box guidance where needed.

## Separate solution corrections

Group 2 contains only worked-solution CAS forms and question validation ensures. It makes no key, field, prompt, rating, membership, or learner-state changes.

| Question | Correction |
| --- | --- |
| q-64207 | Copy −2 rather than −3 from the logarithm candidate |
| q-108979 | Replace w with y in the A+3I chain explanation |
| q-95915 | Say Q has orthonormal columns rather than calling a potentially rectangular Q an orthogonal matrix |
| q-76236 | Include both irrational roots and correct x² > 0 to x² ≥ 0 |
| q-76250 | Use rational inputs 1 and −1 for the noninjectivity counterexample |
| q-77378 | Call 27 an omitted codomain element |
| q-80265 | Prove unequal integrals by comparing 32/105 with 8/3 |

Exact before/after strings are in [batch-02/plan.json](batch-02/plan.json).

## Verification

Both native previews passed the installed schema validators. Their exact datom assertions/retractions and attribution were checked against the original logical forms. Native `db_after` readback verifies every new field identity, owned bank and correct ref, each prompt and solution, unchanged question metadata, and all detached original fields/answers after both groups.

The current engine was rebuilt before offline grading checks. Results:

- 2,319 field checks: 1,229 accepted and 1,090 rejected, with no unresolved results.
- All 69 canonical whole responses accepted.
- All 212 single-checkbox flips rejected; all 69 incomplete whole responses rejected.
- All 620 old-option subsets grade as expected against the authoritative keyed copy. Unkeyed old fields had no established native grade to compare; there were no saved responses requiring migration.

See [preview.json](preview.json), [engine-report.json](engine-report.json), and [package-integrity.json](package-integrity.json).

## Confirmed requests and receipts

- [Group 1 exact submitted transaction](execution/group-01-attempt-02/transaction.edn), [request](execution/group-01-attempt-02/prepared-request.json), and [receipt](execution/group-01-attempt-02/commit-receipt.json).
- [Group 2 exact submitted transaction](execution/group-02-attempt-01/transaction.edn), [request](execution/group-02-attempt-01/prepared-request.json), and [receipt](execution/group-02-attempt-01/commit-receipt.json).
- [Combined receipt](commit-receipt.json), [verification](verification.json), [resolutions.json](resolutions.json), and [status.json](status.json).
- [Historical and topic checks](post-commit/verification.json): all 69 original question snapshots at basis 1846 remain unchanged; all 65 KP/topic memberships are preserved. No matching generator file was found in `generate/scratch`.

The original `batch-01`/`batch-02` files and `preview.json` describe the speculative basis-1846 preparation, not the submitted requests. `package-integrity.json` remains the original preparation manifest; its original resolution ledger is preserved as `prepared-resolutions.json`. Current commit evidence is in `execution/`, `commit-receipt.json`, and `verification.json`. The first interrupted capture had no submission intent and remains archived; the second refreshed conversion capture preserved the concurrent duplicate-field repair. All existing keys and learner state are unchanged.

The separate [missing-key queue](../../../../../../generate/reports/checkbox-next-review-2026-10-12/next-queue.json) still contains 1,007 unevaluated questions. None is included in this transaction package.
