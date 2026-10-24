# Whitespace inside imported Markdown emphasis

Committed to database `math` at **T6226** using contributor `:agent/codex`.

## Cause and scope

The legacy HTML renderer in `scripts/import_historical_question_content.py` concatenated emphasis delimiters around untrimmed HTML children. Legal HTML such as `<strong> Step 1</strong>` became invalid Markdown `** Step 1**`. Its italic branch had the same defect. The original tutorial's retained history establishes that malformed replacement text appeared at T127, before the later integral-formatting repair. See the [original investigation](../../audits/2026-10-23-bold-17592186102027/README.md).

Audited the current immutable T6225 snapshot: 158,564 prose fields and 87,027 text answer values, totaling **245,591 fields**. Protected TeX and code during candidate selection, considered both asterisk and underscore delimiters, reviewed nested formatting, and checked whether the actual Markdown parser displayed the delimiters literally. False matches spanning valid emphasis, list bullets, blockquotes, adjacent bold labels, and underscore answer placeholders were retained. Existing unrelated markup defects are outside this whitespace-specific repair.

## Repair

One atomic, guarded [transaction](transaction.edn) repaired **409 emphasis spans in 389 fields belonging to 382 entities**:

| Attribute | Fields |
| --- | ---: |
| `question/problem` | 273 |
| `question/worked-solution` | 76 |
| `tutorial/content` | 40 |

For 408 spans, the edit only relocates existing whitespace from inside the delimiters to outside them. Every non-whitespace byte, including all formulas, words, Markdown delimiters, answer markers, and URLs, remains in order. One source-confirmed padded empty table header (`<b> </b>` imported as `** **`) loses its empty wrapper. `additional-source-proof.json` retains that source and the nested strong-emphasis evidence.

The requested tutorial, entity 17592186102027, now renders Step 1, Step 2 and Step 3 in bold.

Answer values and types, entity IDs, field links, correct-answer links, and learner history were not changed.

## Validation and receipt

- All 389 fields exercised through the actual player Markdown function, sanitization and MathJax: no failed checks or page errors; identical mathematical content, words, table cell counts, image references, and math-error results before and after. The player gains 407 rendered emphasis elements; overlapping nested repairs and the empty wrapper account for the difference from span count.
- EDB speculative preview verified exactly 389 content replacements and transaction metadata.
- The committed receipt verified exactly those assertions and retractions. Readback at exact db-after T6226 matches every prepared value.
- A new full database scan at T6226 found **zero remaining confirmed whitespace-emphasis errors** across all 245,591 audited fields. Valid formatting and answer placeholders remain intact.

Request key: `repair-emphasis-whitespace-2026-10-23-dd1d4b751d5d6e0918832375`.

Payload SHA256: `dd1d4b751d5d6e0918832375913d153b5a3e9e80fb08912bf80b8fbd209417db`.

See `verification.json`, `global-verification.json`, `render-verification.json`, `individual-review.json`, and `receipt.edn`.

## Prevention

Added `markdown_emphasis` to the shared content formatter. Both the legacy history importer and current capture HTML converter now move emphasis padding outside delimiters and omit empty emphasis wrappers, preserving separation between adjacent words. Added a regression covering the original bug, trailing padding, italic hints, nested emphasis and empty tags; all 26 math-format tests passed. Direct checks through both HTML importers also passed. Generator author and reviewer prompts now explicitly require unpadded emphasis and checks for visible stars.

No UI parser permissiveness was added. The source conversion now emits valid Markdown.
