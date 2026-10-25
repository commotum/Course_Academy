# Source HTML table fidelity repair

Committed to `math` as `:agent/codex` in **17 CAS batches, T7046–T7062**. All 2,509 field values were read back exactly at T7062. Receipts contain only the intended old/new content datoms and transaction timestamps. Entity identities, ownership and correct-answer links, grades, progress, and learner history were not changed.

The repair covers **3,044 replacement locations on 2,248 entities**: 2,959 Markdown tables, 29 existing HTML root tables (including nested tables), and 56 tables previously collapsed into prose. The repaired fields contain 3,300 rendered source tables including their nested children. All 3,004 originally source-confirmed table occurrences are covered, together with all 18 formerly ambiguous repeated layouts and the newly discovered collapsed tables. Containing root repairs account for overlapping nested occurrences; counts are not added twice. See [coverage-verification.json](coverage-verification.json).

The affected attributes are 1,353 question problems, 547 worked solutions, 403 tutorials, and 206 answer labels. Changed answer labels belong exclusively to 43 selection fields graded by answer ID. No canonical blank or free-response answer value changed. The reported example **17592186068570** now has the source's centered limits table, ordinary data cells, visible grid, and shaded variable column.

## Cause and durable correction

Several import paths converted source HTML tables into Markdown. This invented a header row, lost cell alignment and shading, discarded merged cells, and flattened nested tables or tables inside list items. Generic prose-table CSS then overrode parts of the structure that survived as HTML.

The browser capture paths, historical importer, and tutorial importer now preserve source HTML tables using a shared contract. It retains actual `td`/`th` roles, spans, nested tables, captions, explicit alignment, grid rules, selected border and emphasis properties, and validated source colors as data attributes. Table text retains mathematics, assets and field markers. Unsupported spans or layout CSS produce an extraction gap rather than a guessed grid. A regression covers literal dollar signs: Markdown's removal of `\$` must not create a new math delimiter in raw table HTML.

Study, Assignments and Activity use the same decorator and scoped CSS. Source colors are adjusted for readable contrast in both themes after sanitization; arbitrary source styles remain forbidden. Wide tables scroll within their content area, and receive a keyboard-accessible region only while overflow exists. The study app was reloaded and its UI module and `/home` both returned HTTP 200. The writer remained active. Import cache fingerprints include the new Python helper, and capture and generator authoring documentation describe the corrected source-table contract.

## Evidence and validation

Repairs were bound to an archived source identity, content attribute, and exact normalized current cell grid, using a fresh **T7027** snapshot. Repeated identical grids with changing highlights were resolved by occurrence order only when all source occurrences were present. Nested layouts were reconstructed from current leaf content. Current cell values were retained rather than replaced from the archive. CAS preconditions protected against concurrent edits. Current data unrelated to the reviewed spans was retained.

- All **2,509** final fields passed the production sanitizer and MathJax checks, with no new errors or changed image references.
- **2,508** fields had identical rendered math-token sequences. In **17592186148070**, the sole extra item is the literal dollar sign in the `Price ($)` header, now processed as an escaped dollar. All nine mathematical expressions are unchanged; [literal-dollar-review.json](literal-dollar-review.json) records both sequences.
- **66 layout cases** passed across 11 representative tables, two themes and widths 1100, 768 and 390. Checks covered source cell roles and spans, readable shaded cells, stable editable field IDs, and absence of page overflow or vertical table scrolling.
- All 17 exact payloads passed native EDB previews. The actual grading engine checked every choice before and after: **8 accepted, 32 rejected, 390 unresolved** outcomes preserved. The unresolved checks belong to **39 preexisting fields without correct-answer links**; no keys were invented during this presentation repair.
- Six new importer regressions, 16 existing MathML tests, 69 relevant activity/math/matrix/saved-source tests, 47 cache/activity tests, and two shared-renderer browser tests passed. Matrix and assessment browser regressions passed as well.

Three preexisting MathJax errors elsewhere in the affected fields were unchanged. Source-unmatched tables from the broader audit are not asserted to be defective or repaired; the changes here are the complete source-confirmed set. The archived source is required to establish intended presentation for additional mismatches.

See [verification.json](verification.json) for committed bases and exact-write verification, [render-verification.json](render-verification.json), [layout-verification.json](layout-verification.json), [grading-verification.json](grading-verification.json), and [importer-verification.json](importer-verification.json). Each `batch-*` directory retains its exact payload, native preview, stable request identity, durable receipt and final readback. `apply.py` is recovery-safe: an existing request is reconciled using its original key, never resubmitted as new intent.
