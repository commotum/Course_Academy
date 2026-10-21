# Original-import source restoration — October 17, 2026

**Committed and verified at database basis 3519 (from basis 3518).** The guarded transaction, native preview, and exact saved-state readback passed. See [verification.json](verification.json), [transaction](attempt-1/transaction.edn), and [receipt](attempt-1/receipt.edn).

The batch resolves all **2,861 distinct fields** in the [October 16 import-loss investigation](../2026-10-16-import-root-cause/README.md): **2,859 fields were repaired**, and **two answer values remain unchanged** because their loss witnesses belong to different original choices. Repairs cover **607 EDB topics and 616 archived source lessons**. The full audit touched 617 source lessons; one supplied only the two false positives.

| Repaired content | Fields |
| --- | ---: |
| Question prompts | 1,251 |
| Existing worked solutions | 478 |
| Tutorial content | 210 |
| Answer values | 920 |
| Total | 2,859 |

The [integrated plan](integrated-changes.json) contains **3,709 localized replacements** across 2,815 entities. Each replacement is bound to its original source position, retained HTML/MathML, and content hashes. This restores missing formula operands, labels, equation rows, matrix structure, accents, cancellation, percentages, invisible placeholders, and instructional colors. Repeated surviving fragments are mapped independently. Existing prose, diagrams, answer controls, and images outside those spans are preserved. Eighty-six reviewed layout adjustments give complex expressions display space or stack equivalent representations without changing their mathematics.

Reconciliation used [database basis 3482](snapshot-3482/summary.json): 2,860 entire fields still matched the earlier audit, and one changed tutorial received a contextual repair preserving its intervening edit. The committed transaction changes content only. Answer identities, correct-answer links, difficulty, and learner state are preserved; the snapshot found no saved task items using the affected question/tutorial content.

[Native grading checks](grading/verification.json) passed before and after for nine keyed fields whose choices changed, with no new duplicate choices. **233 preexisting unkeyed legacy fields remain unkeyed**; this restoration does not supply missing answer keys. Source/restoration checks and render evidence are recorded in the [review directory](review/), including [static verification](review/static-verification.json) and [source fidelity](review/final-source-fidelity.json). The [final review](review/verification.json) passed for 3,683 restored formulas and 4,430 full-content before/after viewport comparisons, with no introduced rendering errors, changed answer controls, or overflow regressions. Forty-four unrelated preexisting content cases still have rendering errors, recorded separately in that report. The [native transaction preview](attempt-1/preview-verification.json), commit, and exact readback all passed.

- [Per-field case ledger](case-ledger.json): every audited field, its decision, source references, hashes, and transaction status.
- [Primary proposals and verification](primary/verification.json), [primary source-position bindings](primary/bound.json), and [layout overrides](primary/layout-overrides.json).
- [Secondary decisions](secondary/decisions.json), [secondary summary](secondary/summary.json), and [strict source converter](secondary/convert_source.py).
- [Reviewed manual restorations](manual/changes.json) and [two adjacent confidence-interval repairs](primary/adjacent-interval-changes.json).
- [Fresh reconciliation](snapshot-3482/reconciliation.json) and [final transaction verification](verification.json).

Wide radio-choice formulas now scroll within their choice labels at natural size. [Live CSS verification](review/live-css-verification.json) confirms the running app serves the reviewed stylesheet; the existing matrix-overflow browser regression suite passed.
