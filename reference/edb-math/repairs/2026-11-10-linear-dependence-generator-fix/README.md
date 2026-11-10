# Empty checkbox selections and generator repair

Completed the follow-up to the [lesson conversion](../2026-11-10-linear-dependence-checkboxes/README.md).

- **Empty subsets are supported** in fresh practice and generated-question publication. Every unchecked field submits its owned false answer. Missing fields and an absent response map remain incomplete.
- **Question `17592186707100` is converted** to three full-statement checkboxes. All three statements are false; leaving all boxes unchecked is the correct answer. Its original fields/answers and historical snapshot remain readable.
- **Both generators are replaced and registered**, with verified easy, moderate and hard capabilities. Fresh output contains three full-statement checkboxes and no extra None field. Original mathematical constructions, row-reduction explanations, source replay and old immutable packages are preserved.
- A package-bound refill checker examines every delivered survivor, rejecting combination radios, bare labels, extra None options, missing empty-subset guidance and malformed Boolean banks.

No extra practice inventory was published. Registration-only repair receipts now have an explicit approval representation with zero new questions and no claimed published difficulty. The independent all-band samples are recorded separately from publication.

## Confirmed database changes

| Change | Before → after | Receipt |
| --- | --- | --- |
| Remaining question conversion | 13829 → 13830 | [Question receipt](conversion/receipt.edn) |
| Inspection generator registration | 13844 → 13845 | [Verified publication](installed/17592186119924/publication.json) |
| Row-reduction generator registration | 13845 → 13846 | [Verified publication](installed/17592186119925/publication.json) |

Contributor: `:agent/codex`. Final readback at **basis 13846** verified both immutable package hashes, their current registrations and all three approved refill bands. Learner history is unchanged. The running study service was rebuilt and reloaded.

New packages:

- KP `17592186119924`: `generators/45/45d614162b5d1a3bfa8dba46ae90f5cd53dbf2cd5f8f07df5b1bc8fe919132f3/generate.py`
- KP `17592186119925`: `generators/0f/0f76a6e72337762ce664605943fb6376f4fe3fbe83f6a5d5e10373abfcaf5867/generator.py`

## Verification

- Independent `gpt-6.1-sol` high reviewer read the imported source before the revised code. **720 generated records**, including **76 empty subsets**, passed exact displayed-vector/statement checks, deterministic identity checks and row-operation arithmetic. **31 source replays** preserve their original response structures and mathematical content.
- **180 additional generated records**, 30 per KP/band, passed current native practice eligibility, both Boolean answers per field, canonical responses, every single-checkbox flip, incomplete-response rejection and all eight possible whole-question selections.
- All **180 actual publication survivors** passed the real isolated refill checker and native grading against current inventory. All six batches reproduce after relocation outside the repository. No database writes were used to test delivery.
- The reviewer found an initial overly broad caption guard. The tightened complete-statement grammars passed a second review and rejected **11 injected regressions**. The rejected report is retained alongside its accepted replacement.
- Actual player checks cover **48 generated question/viewport cases**, plus the remaining question at three widths, including correct empty selections, encoded false responses and saved-answer feedback. No MathJax errors or outer card overflow. Genuinely wide mathematics retains existing responsive scrolling.
- All eight responses to the committed remaining question passed the live read-only grading API after the final service reload.
- Regression suites passed: one targeted Rust whole-question test, 43 publication tests, 12 approval tests and 13 refill tests.

## Evidence

- [Final verification](final-verification.json) and [current status](status.json)
- [Independent source-first review](review/report.md) and [accepted refill review](review/refill-review-final.json)
- [Actual survivor and relocation verification](preflight-verification.json)
- [Native whole-question checks](engine-report.json) and [player checks](player-verification.json)
- [Remaining question ledger](conversion/case-ledger.json) and [readback](conversion/verification.json)
- [Installed packages and approvals](installation-verification.json)

The engine restriction was removed from `engine/rust/learning.rs` and the publication restriction from `scripts/generator_publish.py`. Generator guidance now documents complete statement labels and valid empty subsets. The optional nonempty sampler remains available for families that intentionally restrict their generated cases.
