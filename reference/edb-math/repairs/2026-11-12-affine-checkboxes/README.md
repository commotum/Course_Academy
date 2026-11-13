# Affine-transformations checkbox migration

Committed and verified in `math` at basis **14385 → 14386**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`, contributor `:agent/codex`.

Converted all **10** subset-selection practice questions in topic `17592186049012` (Affine Transformations), owned by KP `17592186172092` (Identifying Affine Transformations). Each has three independently displayed complete transformations in T1, T2, T3 order: **30 checkbox fields**, **60 owned Boolean answers**. The prompt says “Select all that apply.” Existing mathematical keys, solutions, difficulties, memberships, and question identities are preserved.

Both saved radio attempts were mapped to their actual selected subsets. All other saved state, including grading status and timing, is unchanged. Every one of the **50** old answer choices has a verified subset mapping, including wrong answers. The **60** original field/answer entities remain unchanged, with retained historical attachments and responses.

The topic’s other **21** practice questions request single numerical values; they retain radio fields. Its three canonical worked examples have no answer fields and are unchanged. None of the three KPs has a registered generator, and the repository generator-source search found no matching source; no generator update is required.

## Evidence

- [Final transaction](attempt-2/transaction.edn), [saved exact intent](attempt-2/commit-intent.json), and [confirmed receipt](attempt-2/receipt.edn).
- [Verification](verification.json), [resumable case ledger](case-ledger.json), and [run status](status.json).
- [Native preview checks](attempt-2/preview-verification.json) cover exact datom scope and contributor attribution, original entity retention, unchanged metadata, and mapped learner state.
- [Native grading report](attempt-2/engine-report.json): 30 correct Boolean checks accepted, 30 incorrect checks rejected, 10 canonical whole responses accepted, 30 one-checkbox flips rejected, 10 incomplete responses rejected, and all 50 original-choice grades preserved.
- [Committed presentation lint](attempt-2/committed-lint.json) and [rendering verification](rendering-verification.json): all ten questions rendered at 893, 375, and 320 pixels, with three full checkbox labels, no MathJax errors, and no horizontal overflow. Representative screenshots are retained beside this file.
- Exact committed and pre-transaction historical readbacks are retained under `attempt-2/readback/evidence/`. They match the corresponding native speculative captures after tempid reconciliation.
- [Generator verification](generator-verification.json).

`attempt-1` was never submitted. It was superseded solely to use descriptive tempids that preserve the transformation display order; stable UUID identities did not change.

A pre-existing solution sentence in `q-124232` calls T1 linear after deriving T2; the existing correct key selects T2 and is mathematically correct. That separate content issue is recorded in the ledger; this migration preserves the solution.
