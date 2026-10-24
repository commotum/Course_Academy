# TeX boundary and source-layout repair

Committed to `math` in 12 guarded batches, **T6150–T6161**, source `:agent/codex`.
All 3,423 changed values were verified at T6161. The final scan covered 158,564
prose fields and found zero remaining instances of the diagnosed boundary defects.

The repair covers **2,391 entities**: 1,972 question problems, 1,356 worked
solutions, 94 tutorials, and one multistep context (field counts overlap entities).
No answer values, correct-answer links, identities, field types, curriculum links,
learner history, or generator registrations were changed by these transactions.
The unrelated work occurring during the investigation was preserved.

## Root causes and scope

The reported question, `17592186233932` / `q-342405`, contained raw standalone
`align*` and `eqnarray` environments. Its original Math Academy HTML capture
reproduced the database solution exactly. The historical importer normalized
MathML, but passed these ordinary text nodes through. The Markdown renderer only
protected explicitly delimited math: Markdown split the environment into
paragraphs and consumed a backslash from its row breaks. Direct MathJax rendering
worked, proving the failure was at the Markdown boundary. See the
[original diagnosis](../../audits/2026-10-23-solution-latex-17592186233932/README.md).

The database-wide search also found related source/formatting failures:

- A row separator such as `\\[5pt]` could be mistaken for a `\[` display opener.
- Unescaped currency signs became duplicate/unpaired math delimiters; `[math]`
  markers sometimes survived inside formulas or replaced currency glyphs.
- Empty source formulas and table cells, duplicate display wrappers, and
  mathematical prose indented by HTML extraction caused parsing shifts or code
  blocks that MathJax intentionally skips.
- Unescaped percentage labels and numeric percentages silently commented out
  equations; literal number signs and split set-builder braces also broke TeX.
- Four canonical arithmetic examples contained lossy matrix/absolute-value
  conversions of digit-column layouts. Six affected fields were recovered from
  the original column declarations or complete source MathML. Supplied digit
  columns/carries were checked against integer arithmetic where applicable;
  complete MathML was used where readable-text projections lost phantom cells.

The repair preserves existing mathematical expressions. Seven fields require
explicit source-backed layout treatment: the six arithmetic fields and one
question whose captured empty formula represented an unknown radio-answer word.
That unknown is shown as `?`, and its unclosed TeX grouping is balanced.
Other fields preserve their non-formatting tokens exactly.

## Prevention

- `ui/math-protection.js` protects complete, nested standalone environments before
  Markdown parsing. The player imports it in `ui/learning.js`.
- The dependency-free shared formatter normalizes explicit legacy boundary,
  currency, percentage, spacing and indentation encodings before interpreting
  environments. It validates boundaries and rejects unresolved source layouts.
- Generator publication normalizes prompts, solutions, text choices and feedback
  before content identity/deduplication, and validates the result. This covers
  old immutable packages through their shared publication path; no approved
  package bytes were edited in place.
- The current capture/import save boundary and historical HTML importer use the
  shared normalization. All three MathML extractors escape literal currency,
  percentage/number signs, and set braces at their applicable glyph boundaries.
- The generator author and reviewer prompts, template authoring instructions,
  and actual-UI preview checks now require all intended equations and rows to
  appear. The preview detects raw TeX and math trapped in code blocks, rather
  than relying only on MathJax error counts.
- The old arithmetic source language has a checked column-table recovery path;
  unsupported source placeholders/layouts fail validation instead of being
  guessed as matrices.

New inventory jobs launch a fresh `generator_pipeline.py` subprocess, so new
jobs load the updated publication code and prompt files. This was checked in
`inventory_jobs.py`; no active cohort service required a restart. Existing
running build jobs and their durable state were preserved.

## Evidence and replay

- [preparation.json](preparation.json), [fields.json](fields.json), and
  [batches.json](batches.json): exact original/repaired values and CAS payload hashes.
- [preview-verification.json](preview-verification.json): all 12 speculative
  previews verified the exact proposed datoms.
- Each batch folder retains its `transaction.edn`, stable `commit-intent.json`,
  durable `receipt.edn`, and readbacks. Retry an uncertain submission only with
  that exact original request key/payload.
- [verification.json](verification.json): all commits and exact final-basis reads.
- [global-verification.json](global-verification.json): full post-commit scan,
  exact repaired values, and unchanged non-content metadata on repaired entities.
- [render-verification.json](render-verification.json): all 3,423 complete fields
  rendered; zero final MathJax errors, raw-TeX leaks, math in code, or lost
  existing inline controls. The original renderer reported 280 math errors and
  358 raw-TeX text fragments on these fields. Representative screenshots in
  `review/` include the reported question and recovered arithmetic layouts.
- [fidelity-verification.json](fidelity-verification.json): 3,416 fields retain
  identical non-formatting tokens; seven source-backed layout exceptions.
- [process-verification.json](process-verification.json): all six profiles of an
  actual registered legacy generator, shared publication/identity preparation,
  and both historical/current importer routes; answer banks remain unchanged.
- Source MathML/column declarations for the arithmetic examples are retained
  beside the recovery script and their original topic/example identities.

Regression checks passed: 11 boundary/source-layout tests, 25 existing math-format
checks, 105 generator publication/delivery/pipeline/package/assignment checks,
16 three-importer glyph/brace/hat checks, and three JavaScript protection tests.

The full native snapshots are `.local/edb/tex-boundary-current.jsonl` (T6134)
and `.local/edb/tex-boundary-after.jsonl` (T6161). Initial inventories examined all
prose fields; refinement reused the complete candidate set and existing full-scan
results. Historical intermediate candidates are retained for audit, but only
`fields.json`, `batches.json`, and the committed payloads define the final repair.
