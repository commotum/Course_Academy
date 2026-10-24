# Mathematical blank answers classified as text

The audit captured `math` at **T6164** and examined all **18,849 blank fields**.
Of those, 16,179 had a math-typed correct answer, 48 had a text-typed correct
answer, and 2,622 had no correct-answer link. Missing links were counted but are
outside this classification repair.

All 48 text-correct fields were reviewed individually using their prompt,
worked solution, field key and response role. Five additional mathematical
expressions were confirmed across four questions. The other 43 remain text:
prose/domain descriptions, qualitative sign judgments, DNE, diagram/curve labels,
label lists, literal comparison tokens, and prose comparison words. The two
candidate descriptions “All points with y=0.” and “All points with x=0.” were
specifically retained as prose despite their equation fragments.

## Confirmed type-only corrections

| Question | Field | Correct answer entity | Preserved answer value |
| --- | --- | --- | --- |
| 17592186233773 / q-310182 | 17592186232537 | 17592186232538 | `$-4\pi$` |
| 17592186233933 / q-342412 | 17592186232882 | 17592186232883 | `$-\pi\sqrt{3}$` |
| 17592186233933 / q-342412 | 17592186232884 | 17592186232885 | `$\pi\sqrt{3}+2$` |
| 17592186233934 / q-342413 | 17592186232886 | 17592186232887 | `$-6\sin^2{(x)}\cos{(x)}$` |
| 17592186233935 / q-342427 | 17592186232888 | 17592186232889 | `$-7\cos^{6}{(x)}\sin{(x)}$` |

The [transaction](transaction.edn) contains only five CAS forms on `:answer/type`,
from `:answer.type/text` to `:answer.type/math`. No answer value—including its
existing dollar delimiters—is rewritten. Entity IDs, field types, field links,
answer banks, correct-answer pointers, question content and learner state are
preserved. Reverse-reference checks confirm each changed answer belongs only
to its intended blank field.

The already-fixed example `17592186233932` / `q-342405`, correct answer
`17592186232881`, remains math and is excluded from the transaction.

## Cause and evidence

All five source textboxes contain raw dollar-delimited TeX and **zero rendered
MathML elements**. The historical importer chose math only when it found one
`<math>` descendant; otherwise it used text. That DOM-shape heuristic explains
why these formulas were misclassified. The exact source boxes, source file paths
and value matches are retained in [source-type-evidence.json](source-type-evidence.json).

[Individual review](individual-review.json) records a disposition and contextual
reason for every one of the 48 text-correct fields. The audit's candidates are
signals for review, not automatic classification rules.

## Verification

- [Native grading](grading-report.json): all five bare MathLive expressions are
  accepted against the preserved dollar-delimited keys; five wrong-sign or
  wrong-constant variants are rejected, with no unresolved results.
- [Actual UI check](ui-verification.json): all five controls change from `INPUT`
  to `MATH-FIELD`; real keyboard entry produces `\pi` and `\sqrt{}`.
- [Preview](preview-verification.json): exactly five answer-type retractions and
  five math-type assertions, plus transaction metadata.
- [Commit verification](verification.json): exact readback at the receipt's
  db-after; complete question/field/answer trees differ only by the five types.
  All 48 reviewed answer records plus the already-fixed example are checked,
  including all 43 retained text types and every stored value/identity.

The stable request and durable receipt are retained in `commit-intent.json` and
`receipt.edn`. Recover an uncertain submission with the same key and exact EDN;
never generate a new request key merely to retry it. The native initial snapshot
is `.local/edb/blank-answer-type-current.jsonl`.
