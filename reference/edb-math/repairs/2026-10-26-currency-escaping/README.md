# Database-wide literal currency repair

Completed after the [compound-interest lesson repair](../2026-10-26-compound-interest-17592186060946/README.md), as requested. The broad repair committed at **T8186**.

## Cause and scope

The legacy source-to-Markdown wrapper accepted bare source TeX containing a literal dollar glyph, then added `$…$` around it without escaping that glyph. For example, `$3.37` became **`$$3.37$`**, which starts a display delimiter and lacks a matching closure. The same failure affected negative amounts, amounts in parentheses, and currency embedded in equations. Many of these malformed values produce no MathJax syntax error because the lexer never identifies a complete formula.

The introduction reported by the user had already received a currency repair at T6150. Earlier broad content normalization left these remaining **text answer values** behind. A fresh T8170 scan of **1,457,507 current string values** identified 1,007 nested-currency answer labels. Review of the other delimiter findings added 59 related variants. No topic filter was used.

## Committed repair

**1,066 answer values**, containing **1,077 literal-dollar escapes**, were repaired across **217 current question records and 90 lessons**:

| Encoding | Answer values |
| --- | ---: |
| Nested currency delimiters, such as `$$3.37$` | 1007 |
| Negative currency, such as `$- $72.25$` | 48 |
| Currency inside `V(4)` equations | 5 |
| Parenthesized currency, such as `$$(-2500)$` | 6 |

Every mutation **only inserts a backslash immediately before an existing dollar sign**. Removing those inserted escapes recovers the exact old string. All digits, signs, punctuation, unit wording, answer types, question/answer/field identities, correct-choice links and history references are unchanged. Sixteen answer entities have no current field owner; their exact stored currency representation was repaired as well. Some additional retained fields are detached from current questions.

Original archived MathML explicitly confirms the currency glyphs for reviewed variants, including the negative balance, expected-profit, residual and monetary-function examples. The numerical forms and source relationships remain recorded in [reviewed-repairs.json](reviewed-repairs.json) and [currency-variants-review.json](currency-variants-review.json). The single reviewed pattern is a data repair; the shared UI correctly renders properly escaped currency and was not changed.

## Verification

- All **1,066 repaired labels** passed actual player rendering with zero final MathJax/page errors. Every inserted dollar escape belongs to a complete typeset formula; valid inline/display math was preserved.
- Native speculative EDB validation verified every proposed string and **219 field-validity checks**, preserving each field's previous validity/missing-key status.
- For the **90 affected questions with complete existing keys**, actual application grading ran before and after repair: **180 accepted and 720 rejected submissions**, zero unresolved results and zero database writes. Another **127 current questions** already lack fields/keys; those unrelated completion gaps were preserved rather than inventing answers during an escaping repair.
- Exact receipt/readback confirms **2,133 datoms**: one old-value retraction and new-value assertion for each answer plus the transaction timestamp, all attributed to `:agent/codex`. No other attributes changed.
- A fresh **T8186** database export scanned **2,917,492 facts / 1,457,676 string values**, verified all 1,066 repaired answers, and found **zero remaining confirmed currency patterns**. [Postscan](postscan.json).

The review excluded 30 other unmatched-dollar strings: unrelated partial mathematical options, detached legacy fragments, or bare literal markers. They are retained in [excluded-other-defects.json](excluded-other-defects.json), not silently treated as currency or claimed repaired. This pass does not certify every mathematical expression or incomplete question in the database.

## Prevention

Patched `/home/jake/Developer/MA/PIPELINE/Math-Academy/3-Capture/1-Source/5-MD/md.py`: inline and display wrappers now escape literal dollar glyphs in their **bare source TeX** before adding delimiters. The helper respects existing escapes, counts odd/even backslashes, and recovers the two explicit legacy currency markers. This boundary knows it is handling one formula; it does not guess whether arbitrary authored Markdown dollars are money.

The upstream suite passes **22 tests**, including new currency, negative-currency, monetary-equation, display-math, existing-escape and legacy-marker regressions. Added a local UI math-protection regression verifying that correctly escaped currency inside formulas does not close the math span. That suite passes. Existing capture and publication validation already rejects malformed currency boundaries; the lesson's current generators were verified and left unchanged. [Prevention hashes/evidence](prevention.json).

Evidence: [preparation](preparation.json), [transaction](transaction.edn), [commit verification](verification.json), [native preview](native-preview.json), [rendering checks](render-verification.json), [grading results](native-grading.json), [source-bound repairs](reviewed-repairs.json), and [postscan](postscan.json). Full read-only exports remain under `.local/edb/currency-escaping-2026-10-26/`.
