# Percentage escaping repair — committed

Committed to **`math` at T6518–T6522**, in five batches attributed to `:agent/codex`.

**930 missing visible percent symbols were restored across 905 fields on 887 existing entities.** This includes the four affected choices for question **17592186508947 / q-85526**. Existing answer/field/question IDs, answer types, correct-answer links, choice ownership, and learner history are preserved.

| Attribute | Repaired fields |
| --- | ---: |
| `answer/value` | 691 |
| `question/worked-solution` | 165 |
| `question/problem` | 43 |
| `answer-field/key` (checkbox statement labels) | 5 |
| `multistep/context` | 1 |

## Cause and scope

Math Academy sometimes represents a literal percent as MathML `<mi mathvariant="normal">%</mi>`. The current DOM extractor and historical Python renderer escaped `%` in other MathML token kinds but returned raw identifier text. The resulting `$30%$`, `30%`, `$p%$`, `$[100(1-\alpha )]%$`, or standalone `$%$` uses a TeX comment opener where a visible glyph was intended. The database retains the percent character; MathJax suppresses it and sometimes the remainder of the equation without reporting an error. Correct notation uses `\%`.

The fresh T6511 snapshot audit examined **1,372,985 domain strings**, including every current answer value, content field and statement label. It found 947 unescaped percent tokens inside math across 914 fields. Each token has a recorded decision and context in [token-review.json](token-review.json): **930 literal percentages repaired; 17 genuine comments in nine fields retained**. The comments include optional derivations, alternate formulas and macro-block comments; they remain byte-identical. Plain-text percentages, URL escapes, already escaped math, and ordinary titles are unchanged.

All mathematical answer values affected belong to radio or dropdown fields. Their grading compares selected entity IDs, not displayed strings. The five checkbox keys are visible statement labels, have no matching problem placeholders, and retain their field identities and true/false answer banks. No blank/free-response canonical values were changed. All affected question records have Math Academy source IDs; no generator script defect was identified. Generator author/reviewer prompts already require escaping literal percentage symbols.

The repair inserts only one backslash immediately before each reviewed literal percent. It does not normalize other TeX, rewrite prose, alter numbers, add missing answer keys, or recreate entities.

## Verification and commit evidence

- Actual current player rendering verified all **905 proposed field values** and exactly **930 newly visible percent glyphs**, with no new MathJax/page errors or image changes.
- Native EDB preview verified every exact proposed value and compared field validity before/after. **146 affected answer fields remain valid**. Seven already incomplete imported fields remain incomplete solely because their correct-answer links are absent; those unrelated missing keys are preserved, recorded in [preexisting-missing-correct.json](preexisting-missing-correct.json).
- **1,474 native grading checks** across 153 affected radio/select/checkbox fields, before and after: 292 accepted, 1,112 rejected, and 70 expected missing-key errors. All outcomes remain unchanged.
- All five batches use existing-value CAS, source `:agent/codex`, immutable payload hashes and persisted stable request keys. There were no preflight content conflicts at T6517.
- Every committed receipt was checked against the exact permitted datoms: old/new value CAS pairs and transaction metadata only. Exact readback passed at each transaction's `db_after` and again at **T6522**.
- A second full export at **T6522** scanned **1,373,080 current domain strings**, closing the gap from concurrent additions. All 905 repaired fields remain exact. **Zero percentage-escaping defects remain**; the only 17 unescaped mathematical percent tokens are the individually reviewed genuine comments.

## Prevention

Updated the `mi` handling in `scripts/question_capture/dom.js` and `scripts/import_historical_question_content.py` to escape literal TeX special characters. The older `capture/scripts/browser/extract.js` already handles percent identifiers correctly. All three paths were checked against `mi`, `mo` and `mtext` tokens, and both browser extractors now retain all four percent symbols from the authentic q-85526 source. Ordinary prose percentages remain unchanged and escaped percentages are not double escaped.

**60 source-extraction/math-format/boundary regression tests passed**, including the added identifier-percent regression. The current shared prose normalizer/validator already handles numeric percentage escaping; the token-conversion fix also covers standalone, spaced and symbolic percentages that the numeric guard does not recognize. No capture/import worker was observed with a stale converter loaded. Active generator pipeline jobs use the existing percentage-authoring instructions; no jobs or immutable packages were changed.

## Reviewable artifacts

- [Commit verification](verification.json), [fresh global coverage verification](coverage-verification.json)
- [Prepared batches and hashes](batches.json), [exact before/after fields](fields.json), [individual token decisions](token-review.json)
- [Native grading](grading-verification.json), [render verification](render-verification.json), [converter verification](importer-verification.json), [process checks](process-verification.json)
- [Reported question before](reported-question-before.png), [reported question after](reported-question-after.png)
- Each `batch-NN` directory retains its exact transaction, native preview proof, commit intent, receipt and database readbacks.

The original [q-85526 root-cause audit](../../audits/2026-10-24-percent-17592186508947/README.md) describes the historical bad values at T6489. Its saved source and rendering comparisons remain unchanged as evidence.
