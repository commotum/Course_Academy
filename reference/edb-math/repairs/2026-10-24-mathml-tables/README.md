# MathML table import repair — committed

The `math` database repair committed in **11 batches, T6318–T6328**, attributed to `:agent/codex`. It repairs **4,768 table occurrences in 2,001 fields across 1,885 existing entities**. All 32 affected tables in topic 1159, including example **17592186100705**, are repaired.

| Attribute | Changed fields |
| --- | ---: |
| `tutorial/content` | 30 |
| `question/worked-solution` | 1,501 |
| `question/problem` | 155 |
| `answer/value` (radio choices) | 315 |

## Cause and selection

The historical Python importer and the older browser extractor converted every MathML `mtable` into TeX `aligned`, dropping explicit frames, row/column rules, and column alignment. This made change-of-limits tables look like concatenated expressions and erased augmented-matrix and block-matrix partitions. The current DOM extractor preserved centered ruled tables but lost rules on noncentered tables. Valid TeX and a clean MathJax render were insufficient to detect the semantic layout loss.

The audit scanned **535,403 stored content/answer fields** at T6244, including aligned equations, matrices, and arrays. Source evidence came from archived lesson HTML, historical capture states, question-choice snapshots, and the newer hashed observation/lesson captures. Matching is bound to the original question/tutorial identity, field, question/step container, and repeated-table occurrence order. This matters because the same numerical matrix may legitimately appear with different partitions, or without a partition, in adjacent steps and choices. Source attributes restore layout; **current mathematical cell text is retained**. Ordinary unruled matrices and equation derivations remain unchanged.

The single ambiguous source layout was reviewed individually. For **q-129050**, losing an augmented-matrix separator made source choices B and D identical, and import deduplication collapsed them. Existing answer **17592186261594** is retained as B with its separator restored; the omitted incorrect D is restored as a new answer with UUID `8351dfc7-9bd0-5029-9d05-12e3bc502845`. The correct answer remains **17592186260624**. All preexisting entity IDs, field links, correct-answer links, and learner response IDs are preserved. Existing choice grading uses entity identity and is unchanged. Complete choice-bank counts were checked for 91 older and 55 newer captured questions; this was the only confirmed collapse.

## Verification

- Exact existing-value CAS guards on every changed field; no preflight conflicts at T6317.
- Native EDB speculative validation of all final payloads, including answer/field invariants.
- Surgical span compiler verifies mathematical cell bytes and permits only empty-cell padding needed to retain ragged source tables.
- Actual player Markdown/answer rendering and MathJax verified for all **2,001 fields**, including equal mathematical token sequences, unchanged images, and no new render errors or raw-TeX leaks.
- **659 native grading checks** across **66 radio fields**, before and after; restored D is rejected as intended.
- Every batch has a persisted original payload, SHA-256, stable request key, committed receipt, and exact readback at its `db_after`. Final readback at **T6328** matches all prepared values.
- Receipt datoms were checked against the exact intended changes: content CAS pairs, one restored answer and its choice link, and transaction metadata. No learner/history records changed.
- The temporal gap after the original scan was reviewed: four additional current answer values appeared by T6317, all ordinary scalar/text values without table environments. The final coverage check verifies all repaired table spans and closes this gap.

## Prevention

Updated `scripts/import_historical_question_content.py`, `capture/scripts/browser/extract.js`, and `scripts/question_capture/dom.js` to retain explicit table rules and left/center/right alignment as TeX arrays. They preserve ragged cells, distinguish actual inter-column rules from ineffective extra attributes, and reject unsupported rule styles rather than silently inventing a layout. The Python path shares `mathml_ruled_table` in `scripts/question_capture/math_format.py`. Generator author/reviewer instructions now explicitly require preserving data-table and augmented/block-matrix structure.

**48 math-format/matrix-capture regressions passed**, plus four source-MathML fixtures verified across all three converters. The six candidate generator scripts reviewed contained legitimate aligned derivations, with no confirmed table defect requiring a script edit. The observed running Python/Node application processes were EDB services and the graph explorer; no capture/import/generator worker required restarting.

This repair concerns lost explicit table structure. Custom equation row spacing and the three separately documented incomplete practice questions in topic 1159 are outside this repair.

## Evidence

- [Commit and readback verification](verification.json), [coverage verification](coverage-verification.json)
- [Prepared batches](batches.json), [field values](fields.json), [source-backed span changes](table-edits.json)
- [Rendered-field verification](render-verification.json), [native grading](grading-verification.json), [converter checks](importer-verification.json)
- [Reported example after repair](17592186100705-after.png), [restored matrix separator](17592186261594-after.png)
- [Original lesson audit](../../audits/2026-10-24-lesson-17592186100705/README.md)

The intermediate `archive-*`, `direct-matches`, `ambiguous-layouts`, and `retained-arrays` files record earlier candidate exploration. The committed scope is defined by `fields.json`, `table-edits.json`, `batches.json`, their final payload hashes, and committed receipts.
