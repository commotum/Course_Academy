# Derivative fraction layouts: topic-wide repair

Completed 2026-11-01. Text repairs committed to math at **T12062**; fresh readback, served styles and grading verified at **T12064**.

Topic **17592186049248 — Calculating dy/dx Using dx/dy**; its only KP is **17592186119939**. All nine practice questions are imported. There is no registered question generator for this topic.

## Repairs

- **17592186315109 / q-341608:** restored `dy/dx = y³ / [field-1]` as an interactive fraction with the input in the denominator. Corrected the worked rewrite `−2y⁻¹ + 5y²` to `−2y⁻² + 5y²`. The denominator key remains `4+10y⁴`.
- **17592186233915 / q-341626:** restored `dy/dx = [field-1] / (2√y + [field-2])`. The numerator key remains y and the missing denominator term remains 15y⁵.
- Audited the other seven practice questions and canonical example for the same formatting defect. No further matching fraction tables were found. Two preexisting incomplete imports were reviewed as display-only fixtures without inventing missing source answer keys; this repair does not claim to complete those records.

Only **three text attributes** changed. Every question, field and answer identity, correct link, bank member, topic/KP membership, canonical example and learner response is preserved. No questions were retired or replaced for this imported-content presentation repair.

## Failure mechanism and prevention

The stored prompts contain two-row, three-column Markdown tables: dy above dx, an equals sign in the top middle cell, and a numerator above a denominator control. This is mathematical fraction layout encoded as ordinary table data. Markdown supplies a header row and grid borders; it cannot infer the two missing fraction bars or vertical equation alignment.

The legacy HTML-to-Markdown path in `capture/scripts/database/text.py` classified a rectangular HTML table as a data table and serialized only cell contents, losing the mathematical meaning of borders/alignment. A structural fixture reproduces this failure mechanism. The exact historical source HTML for these two questions was not recovered; the diagnosis is based on the captured question markup, mathematical response contract and converter reproduction, rather than a claim about the original website's styling.

The repair adds:

- A narrow, idempotent recognizer in `scripts/question_capture/math_format.py` for unambiguous dy/dx fraction tables containing answer controls. It handles Markdown and HTML forms and leaves ordinary data tables, larger tables and code examples unchanged.
- A canonical HTML fraction with separate numerator/denominator containers. Existing real input markers remain outside MathJax and retain their roles.
- Capture/import normalization and legacy-converter preservation of this fraction structure.
- The same normalization at generator publication, covering future content even when an older bundled formatter is used by a generator.
- `ui/fraction-answers.css`, shared by learning, activity history, topic and course views, and its explicit static-file allowlist entry.
- Immutable-basis mathematical-correction provenance for q-341608. The actual importer was checked to retain the verified exponent correction instead of restoring the original typo. Evidence: `correction-protection.json` and `reference/mathacademy/mathematical-corrections/2026-11-01-q-341608/`.

## Verification

- Symbolic differentiation independently confirms both reconstructed fraction answers and their existing field keys.
- Seven new fraction-layout regressions passed, including numerator/denominator field placement, the legacy converter, ordinary-table preservation, code preservation, idempotence and generator delivery.
- Sixty-seven existing formatter, boundary and mathematical-correction tests passed.
- All ten question/example records passed the actual desktop renderer. Both repaired fractions passed completed and active-input phone renders at 390px. Screenshots were visually inspected; DOM checks confirm numerator/denominator ordering, visible fraction bars and mounted real controls.
- Exact guarded preview, durable request, source-aware receipt and full KP readback verify that only the planned text changed. The canonical example and other questions are unchanged.
- Ten live grading checks passed: canonical and algebraically equivalent answers are accepted; swapped fields, a full fraction entered into the denominator-only field, wrong powers and zero alternatives are rejected. Verification created no learner attempts.
- The running service serves the shared fraction stylesheet and all three importing stylesheets successfully.

Evidence: `audit.json`, `proposals.json`, `verification.json`, `completion.json`, `render-desktop/`, `render-phone/`, `render-phone-active/` and the archived exact request in `publication/requests/`.
