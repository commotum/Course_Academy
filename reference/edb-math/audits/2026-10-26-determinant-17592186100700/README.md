# Missed determinant matrix layout: example 17592186100700

This canonical example is Math Academy e-4437, in topic 1169, **The Geometric Interpretation of the 2x2 Determinant**, step 16239. Current-state investigation is pinned to T8446.

The determinant was encoded as ordinary bars around a nested `aligned` environment. That environment is for equations, so the entries crowd together and the bars do not stretch around the two rows. The source instead has a centered two-column MathML table with 1em column spacing and determinant fences. All four entries remain present; the determinant is -9 and the area is 9.

Retained history supplies unusually direct evidence: the original T44 value used `vmatrix`, but a second Math Academy source assertion at T78 replaced it with `|\begin{aligned}…\end{aligned}|`. The T5664 image-to-formula repair changed the first matrix illustration to TeX and retained the malformed determinant below it. It did not introduce that malformed determinant. Full retained datoms are in `history.json`.

The earlier T8044 database-wide sweep repaired a different defect: lost outer TeX around partial descendant MathML in mixed SVG titles. The T8127 determinant matrix-spacing repair covered only topic 152. This example is in topic 1169 and was outside that spacing repair. The prior conversational description should have explicitly distinguished these scopes. This investigation does not establish that all database-wide matrix layout defects have been repaired.

## Repair

The exact CAS transaction changes only this example's worked solution: the inner determinant becomes `vmatrix`, and the source's determinant operator becomes `\det`. The outer aligned derivation, first labeled matrix, all ordered cells, arithmetic, final area, images, identities, links, and learner history are preserved. No answer or learner entity is transacted.

Actual application Markdown and MathJax rendering passes with zero errors and was visually inspected (`after.png`). Native EDB speculative validation and the exact committed receipt/readback are retained in `native-preview.json`, `receipt.edn`, and `verification.json`; the latter records the resulting transaction basis. The existing complete-formula normalization added during the T8127 repair already prevents the nested fenced-table layout on future imports; this example is retained old content.

Committed repair: **T8451**, with exact readback and content-only receipt verification.
