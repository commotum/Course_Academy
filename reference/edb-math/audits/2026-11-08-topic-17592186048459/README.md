# Introduction to Linear Transformations — source audit and repair

All identified defects were repaired in the live `math` database at basis **13537** (previous basis 13536). The transaction changed 134 attributes while preserving question, answer-field, and answer identities, existing choice banks, and learner history. See [repair verification](repair/verification.json), [changes](repair/changes.json), and the [commit receipt](repair/receipt.edn).

The full audit covered both tutorials, all six lesson steps, four canonical examples, all 50 practice questions, all 103 answer fields, and 225 distinct answer entities. Raw original HTML and screenshots were used: the intermediate normalized source JSON is itself lossy for some mixed SVG/MathML expressions.

## What was repaired

- Sixteen vector response layouts, including question `17592186299639`, now use bracketed matrix input controls. These were layout tables in the original, not mathematical data tables.
- One three-component vector response was reunited on a single line.
- Three unanswered seed questions received correct-answer links and complete worked solutions. Two solutions were authored from the original givens and nearby lesson templates because no original solution capture was available; their authorship is recorded in [completion templates](repair/completion-templates.json).
- Original bold vector/operator notation was restored across the 54 examples and questions.
- An arithmetic error present in the Math Academy original was corrected: an intermediate vector in q-74776 incorrectly used −2 instead of −1. Its original givens and final answer were already correct. The independent correction record is under `reference/mathacademy/mathematical-corrections/q-74776/`.

## Root causes

The old table serializer flattened row spans, discarded CSS used to draw vector brackets, and promoted the first row to a Markdown table header. One variant kept the HTML span but lost its bracket borders. The active browser extractor already reconstructs the saved originals correctly; the old damaged records remained in the database.

The earlier TeX cleanup checked formula syntax while retaining the surrounding table structure. The existing `normalize_matrix_answer_tables` recovery routine had no production caller. It is now invoked by `normalize_prose`, with conservative recovery for the lost-border HTML variant as well. New regressions cover the reported layout, three-component HTML layout, idempotence, ambiguous repeated bindings, real data tables, and code preservation. End-to-end tests through the active import preparation also exposed paragraph collapse when a repaired matrix layout was processed again; the HTML-to-Markdown converter now preserves the surrounding Markdown paragraphs. All **51 formatter tests and 16 active import math-content tests pass**.

HTML whitespace had also become paragraph breaks inside one inline vector answer. Earlier MathML conversion discarded `mathvariant="bold"`. Both are corrected in the retained content; the active extractor already preserves that source structure and styling.

The incomplete questions came from initial unanswered seeds. The existing-record recapture path intentionally defers missing solutions and requires retained/captured prompts to normalize identically before filling answer components. A later capture therefore did not complete q-12010 because its prompt differed. This repair completes the source-verified entries explicitly rather than loosening those import safeguards.

## Verification

- 444 strict checks through the actual application renderer: passed.
- 109 correct/incorrect checks through the actual read-only application grader: passed.
- 108 desktop/mobile prompt-layout checks: passed.
- All 47 previously populated question keys independently checked against their givens: correct; all three missing keys now complete.
- Native application schema preview and committed readback: passed; only planned content attributes changed.

The broader legacy matrix-capture and complex-table test suites were also attempted. They contain existing failures unrelated to this formatter change (changed display/font output expectations and an outdated renderer fixture missing `decorateEquationGroups`, among others). They are not counted as passing checks. The actual-player verification above and the targeted formatter regressions passed.
