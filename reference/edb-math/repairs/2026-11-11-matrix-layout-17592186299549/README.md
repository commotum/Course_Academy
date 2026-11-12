# Standard-matrix answer layout repair

The imported answer grids used Markdown tables with shifted cells, or old HTML
tables whose empty edge cells no longer drew matrix brackets. This affected 27
questions in *The Standard Matrix of a Linear Transformation* (lesson entity
17592186124744), including 17592186299549 and 17592186299554.

Replaced those layouts with the existing bracketed matrix controls. Square
matrices retain their row-major answer fields. Transformation outputs and vector
images retain one field per row. Mapping arrows remain arrows; no extra equals
sign is introduced. Question IDs, field IDs, answer keys, worked solutions and
learner history are preserved.

Audited all 58 unique questions and canonical examples across the lesson's four
knowledge points, including their solutions. All are imported Math Academy
questions. None of these knowledge points has a published generator.

The shared import formatter now also recognizes transformation mapping labels
before column-vector grids, in both Markdown and source HTML. Previously it
recognized only equality labels. Regression tests cover 2D and 3D mappings,
multiple arrow spellings, field order, idempotence and real-table preservation.

Verification:

- [Live final audit](final-audit.json): 27 repairs, no old table layouts left,
  read back at database basis 14348.
- [Initial commit](initial-publication/verification.json) and
  [remaining 26 repairs](lesson-publication/verification.json): guarded CAS,
  native validation, exact receipt verification, full parent readback and
  historical reads. Only the reviewed question/problem values changed.
- [UI rendering](lesson-render/rendering.json): all 27 repaired questions in
  active and completed states at 390 and 1280 pixels, 108 passing presentations.
  Representative screenshots were visually inspected, including both requested
  questions, 3D vectors, and source HTML variants.
- [DOM field-position checks](layout-verification.json): all 108 presentations
  preserve matrix cell positions and field identities; active inputs are empty
  and editable.
- [Independent math](math-verification.json) and
  [native grading](lesson-native-report.json): exact coefficient extraction or
  matrix multiplication for every repaired question; 170 accepted and 85 rejected
  controls, none unresolved.
- [Formatter tests](formatter-tests.log): all 52 passed. The separate Python
  source-table browser suite could not start because this environment lacks the
  Python Playwright package. The actual UI renders used the installed Node
  Playwright runtime successfully.

Scope: this was an audit and repair of matrix/table layouts. Five older imported
questions independently lack correct-answer links and worked solutions; their IDs
are recorded in [the lesson audit](lesson-audit.json). Those pre-existing content
completion issues were not changed by this formatting repair.
