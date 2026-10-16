# Matrix capture repair

The extractor previously serialized every MathML table as `aligned`, left matrix
fences as literal characters, and discarded `mathcolor`, `mathbackground`, and
table rules. It also serialized a hat accent as `\overset{^}{...}`, which MathJax
cannot parse. `scripts/question_capture/dom.js` now preserves matrix environments,
scoped colors and highlights, augmented-matrix dividers, table rules, one-sided
system braces, and hat accents. It removes only empty surplus cells from ragged
matrices; a ragged matrix containing extra nonempty entries requires review.

The following requested topics were repaired in the requested order and committed:

| Topic ID | Topic | Text fields repaired | Commit basis |
| --- | --- | ---: | ---: |
| 17592186050765 | Systems of Equations as Augmented Matrices | 191 | 2127 |
| 17592186049120 | Elementary Row Operations | 178 | 2128 |
| 17592186048980 | Row Echelon Form | 89 | 2129 |
| 17592186049422 | Solving 2x2 Systems of Equations Using Gaussian Elimination | 138 | 2130 |

All 596 committed fields were read back at basis 2130 and matched the verified
content exactly. Receipts, retained CAS requests, and readback evidence are in
`requested-topics/`. Eighteen focused capture regressions passed. Browser validation
used the application's actual Markdown renderer and vendored MathJax: 679 reviewed
fields, including all 596 repaired topic fields and corpus samples, rendered 1,549
tables with no MathJax errors or page errors. The static fixture cannot serve the
app's image endpoint; those fixture-only image requests do not validate images.

The database-wide investigation found the same matrix-layout corruption throughout
the corpus. The broader patch uses guarded text replacements, including nested
cofactor matrices. The user explicitly approved the broader repair, which is now
**committed and verified: 22,513 fields across 18,034 entities**, in 30 batches.
The complete readback at final basis **2186** matched every intended value.
An intervening content update affected 36 fields; their newer content was retained
while applying the formatting repair. All 36 refreshed fields rendered 280 tables
without MathJax errors. Receipts, reconciliation evidence, approval, and readback
are retained in `pending-database-wide/` (the original preparation folder name).

The patch preserves numeric content except for one independently verified
missing zero in q-140306 (entity 17592186272048). That solution solves the homogeneous
eigenvector equation `(A + 2I)x = 0`; its first augmented matrix omitted the second
row's right-hand-side zero. Its stated row operation and subsequent zero row also
establish the omitted value. The original record is retained in
`missing-cell-evidence.edn`. No answer keys or learner records are changed.

`source-reextraction.json` retains old/new formula conversions from the four original
saved lesson HTML files. The database-wide transactions retain complete old and new
strings, request keys, and sources for review and recovery. The committed manifest
is `pending-database-wide/commit-intent.json`; `verification.json` in that folder
confirms the complete readback.
