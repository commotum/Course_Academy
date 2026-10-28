# Matrix answer layout: q-275522

Question `17592186292861` had a malformed imported answer layout. The original capture uses a two-row label cell (`rowspan="2"`), four editable matrix entries, and narrow border cells to draw brackets. Flattening this into Markdown discarded the row span and border roles. The lower answer row shifted one column left and the brackets became a five-column spreadsheet grid.

Replaced only `question/problem`'s answer table with the existing `matrix_answer()` presentation: external label, square brackets and a borderless 2×2 entry grid. Field keys remain row-major:

| Position | Field | Correct answer |
|---|---|---:|
| Top left | field-1 / 17592186292450 | −2 |
| Top right | field-2 / 17592186292436 | 3 |
| Bottom left | field-3 / 17592186292070 | 2 |
| Bottom right | field-4 / 17592186292329 | 0 |

Committed at **T8992**, using exact CAS and explicit Codex provenance. Native preview, receipt validation and exact readback passed. All field/answer IDs, correct-answer links, values, solution and learner history are unchanged. See [verification.json](verification.json).

Actual MathLive rendering verifies column alignment, one control for each original field ID, visible borders, completion with the original answers, and a narrow-screen layout without page overflow. No learner responses were recorded. Compare [before](before.png) and [after](after.png); details are in [interactive-verification.json](interactive-verification.json).

The current source-backed HTML table importer already retains row and column spans. Its browser leaf renderer, however, omitted live MathQuill wrapper nodes, so those editors could be lost inside preserved tables. Fixed the shared helper and both embedded copies to preserve those widget boundaries. A regression using the actual archived question checks every field and source row position in both browser extractors. All seven source-table tests and 33 formatting tests pass.

The external legacy Markdown converter now rejects merged cells instead of silently flattening them; structural HTML conversion is required. All 28 external Markdown tests pass. Source: `reference/mathacademy/question-capture-workers/linear/14043295/q-275522-before.json`.
