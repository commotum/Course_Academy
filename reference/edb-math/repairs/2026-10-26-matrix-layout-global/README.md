# Database-wide fenced matrix layout repair

Completed using the EDB skill on 2026-10-26. **T8500** changes **4,716 fields across 4,031 entities**, correcting **13,181 fenced table layouts**. The affected content and choices belong to **179 lessons / 2,078 question entities**; one additional multistep context lacks a current lesson ownership path. This is the full-database follow-up to example 17592186100700, not another lesson-only repair.

## Cause and scope

The historical MathML renderer emitted a generic unruled `mtable` as `aligned`. Inside brackets or determinant bars, that loses matrix column spacing and leaves literal fences too short. Nesting the table inside an outer aligned derivation does not make its inner matrix an equation alignment. All entries can remain present, and MathJax can report zero syntax errors, while the layout is still wrong.

The earlier database-wide T8044 repair addressed a different source-loss defect involving mixed SVG titles. T8127 repaired matrix layout only in topic 152. The current scan starts from a fresh full native snapshot at **T8481**, examining **2,932,721 current facts / 1,465,086 string values** across all attributes, including bare mathematical answer values. It therefore includes other lessons, tutorials, examples, practice prompts, worked solutions, answer banks, and older generated pool content. Read-only full exports remain under `.local/edb/matrix-layout-2026-10-26/`.

## Exact changes

| Attribute | Fields |
| --- | ---: |
| `question/worked-solution` | 1,976 |
| `question/problem` | 759 |
| `tutorial/content` | 40 |
| `answer/value` | 1,940 |
| `multistep/context` | 1 |

Explicit fenced `aligned` and `matrix` environments become `bmatrix`, `pmatrix`, or `vmatrix`. Changes occur only inside protected math spans or explicitly typed mathematical answers. The review covers 33 table shapes, including row/column vectors, symbolic matrices, column-vector illustrations with intentionally empty cells, determinants, and matrices nested in derivations. The complex review retains source context for unusual forms, including a nonsquare determinant distractor; this formatting pass preserves that distractor's entries rather than correcting its intended mathematical invalidity.

Every converted grid is independently parsed before and after: every entry remains in its original ordered position. One malformed alignment had an entirely empty surplus trailing column in one row; normalization removes that empty alignment padding without removing a mathematical entry. Arithmetic, numerical answer content, signs, variables, row order, source images, prompt field markers, entity IDs, answer types, choice IDs, correct-answer links and learner history remain intact. Answer **display strings** change where they contain the defect; their mathematical entries and selection outcomes do not.

## Verification

- All **4,716 before/after fields** passed the actual player's Markdown/MathJax rendering, with **zero final math errors or page errors**, unchanged image references and unchanged formula counts. Math answers use the same delimiter-wrapping rule as the player's answer renderer.
- Representative before/after screenshots were visually inspected. Actual DOM measurements show column gaps increasing from 1.54px to 30.92px on the representative 2x2 determinant, and from 6.01px to 26.92px on the representative 2x2 matrix. [Visual comparison](matrix-layout-before-after.png), [geometry](visual-verification.json).
- Native speculative EDB validation verified every proposed value and preserved validity for all **396 affected answer fields**. All are selection fields with existing correct links.
- The application's native grader ran every choice before and after: **792 accepted / 3,136 rejected / zero unresolved**, totaling **3,928 checks**. No database writes were used for grading.
- The exact committed receipt contains **9,433 datoms**: precisely the 4,716 reviewed old/new content pairs plus the transaction timestamp, attributed to `:agent/codex`. Exact readback at T8500 passed in bounded batches. The initial single large readback query exceeded the CLI's query capacity after a successful commit; verification recovered the saved receipt and read the committed values without resubmitting.
- A fresh **T8502** full snapshot scanned **2,932,901 facts / 1,465,157 strings**, verified all 4,716 repaired values, and found **zero remaining matches for the reviewed fenced-matrix defect**. [Postscan](postscan.json).

An independent broader fence/context detector reviewed 49 residual contexts: 25 already-correct `matrix` environments using named scalable brackets; 19 wrapped scalar continuations; two math-boundary false positives; and three asymmetric sign-chart tables. These are not fenced matrix defects and were preserved. The sign charts are separate table-layout candidates, not claimed repaired here. The 111 answer-field keys containing old TeX are identity keys, not display content, and remain unchanged. This pass does not certify all mathematics, missing question content, or unrelated limit/table notation.

## Prevention

The capture and historical-import paths already normalize complete formulas after their fences have been recovered, and a new historical regression verifies a nested determinant while retaining its outer aligned derivation. Generated packages have their shared formatter, but the common publication adapter previously checked math boundaries without checking matrix layout. Added `validate_matrix_layouts` to that publication boundary for prompts, worked solutions, bare mathematical answers, formulas inside text answers, and answer feedback. It rejects fenced equation alignments that need real matrix environments, without rewriting candidate identities or converting legitimate wrapped scalars. This covers the common stable-identity/publication path rather than relying on individual generator prompts.

Validation: **29 shared formatter tests**, **39 publisher tests**, and **4 historical-import layout regressions** pass. The newly added publisher cases cover nested determinants, math/text answer labels, correct matrix notation, and wrapped scalar continuations. Updated capture/generator instructions document this requirement. The one initial new historical assertion differed only in whitespace; its expected spelling was corrected and all four historical tests rerun successfully.

Evidence: [preparation](preparation.json), [ordered cell checks](grid-verification.json), [reviewed complex cases](complex-review.json), [reviewed residuals](residual-reviewed.json), [transaction](transaction.edn), [native preview](native-preview.json), [render verification](render-verification.json), [native grading](native-grading.json), [committed verification](verification.json), [postscan](postscan.json).
