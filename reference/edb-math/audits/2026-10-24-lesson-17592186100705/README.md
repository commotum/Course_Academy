# Lesson import audit: Calculating Definite Integrals Using Substitution

Read-only EDB audit of topic **1159**, entity **17592186048332**, at **T6239**. The reported entity **17592186100705** is canonical example **e-456**, “Calculating a Definite Integral of a Rational Function Using Substitution.”

## Main finding: change-of-limits tables lost their structure

The original source uses a 2-by-3 MathML table with centered cells, a solid outer frame, vertical separators and a horizontal row separator. For the reported example, the source cells are:

| $x$ | $-1$ | $2$ |
| --- | --- | --- |
| $u$ | $1$ | $10$ |

The stored TeX is `\begin{aligned}x & -1 & 2 \\ u & 1 & 10\end{aligned}`. MathJax consequently uses `right left right` column alignment, with no frame, column lines or row lines. The first two cells run together: `u` and `1` look like `u1`; `x` and `-1` look like an expression. This is valid TeX describing the wrong kind of layout, so syntax and MathJax-error checks do not catch it.

Source-confirmed instructional records:

| Entity | Role | Source |
| --- | --- | --- |
| 17592186102027 | Introduction tutorial 840 | `1159.html`, step 1618 |
| 17592186100704 | Canonical example e-455 | `1159.html`, step 1619 |
| 17592186100705 | Canonical example e-456 | `1159.html`, step 1623 |

All three lost their source table structure. **29 additional practice worked solutions** in the same lesson contain the identical two-row `x`/`u` table pattern encoded as `aligned`, for **32 affected table occurrences**. Their entity IDs and exact stored strings are in `fields.json`. The 29 practice matches are identified by stored structure; this audit did not recover a separate original HTML table for every practice question.

The [current reported example](17592186100705-before.png) and [source-faithful local preview](17592186100705-after.png) show the difference. The preview replaces only that table with `\begin{array}{|c|c|c|}\hline x & -1 & 2 \\ \hline u & 1 & 10 \\ \hline\end{array}`. `source-table-proof.json` retains the original MathML, exact cells, attributes and proposed TeX for all three instructional records. No values or calculus steps are changed.

## Root cause and import history

`scripts/import_historical_question_content.py:95` maps every `mtable` to `aligned`, ignoring frame, row/column rules, alignment and source row spacing. `capture/scripts/browser/extract.js:278` has the same blanket conversion. Both reproduce the faulty table from the original source with no reported extraction error.

In contrast, `scripts/question_capture/dom.js:325` already preserves ruled centered tables as TeX arrays. Running both DOM extraction paths against the same three source tables confirms the disagreement; see `importer-reproduction.json`. The remaining paths need the same structural handling rather than a UI setting change.

Retained history shows the canonical examples changed from earlier `bmatrix` representations to `aligned` at **T78**, and the tutorial at **T127**. The initial `bmatrix` versions retained an enclosing bracket, but also failed to reproduce the original table grid. Later integral-display and Markdown-emphasis repairs preserved the preexisting table defect. See `table-history-summary.json` and `history.jsonl`.

## Other components

- The lesson route is intact and correctly ordered: introduction, KP 17592186100874, KP 17592186100877. Both canonical example links and the first KP's source prerequisite links (topics 283 and 443) match the archive.
- The original prose, the important warning about the order of limits, derivatives, powers, fractions, evaluation bounds and log expressions are present in the instructional records. There are no source image components in these three records to lose.
- Source custom row spacing is discarded too. For example, source derivations specify 0.8em row gaps, while their current parsed MathJax tables report uniform 0.5em gaps after the application's global spacing adjustment. This makes the derivations denser even when the formulas render correctly.
- The full prose audit covers **66 fields across 35 entities**: the introduction, two canonical examples, and all 32 linked practice questions. There are zero MathJax errors, raw-TeX leaks or browser errors in the tested renderer. The test fixture used a desktop viewport; it is not a claim about every mobile layout.
- Independent exact integration confirms the three instructional results: $1/6$, $-15/8$, and $\log(10)/3$. This was a formatting/completeness audit, not an independent mathematical grading audit of every practice item.

## Separate completeness issue

Three practice records have neither a worked solution nor a correct-answer link:

| Entity | Source question |
| --- | --- |
| 17592186101449 | q-49527 |
| 17592186101118 | q-12912 |
| 17592186101119 | q-12917 |

The archived lesson Markdown explicitly marks all three `MA_ANSWER_MISSING`; these were incomplete source captures, not a current rendering failure. They should be handled separately from a table-formatting repair. See `missing-solution-details.json`.

## Next repair scope

Preserve source tables as actual gridded arrays; preserve equation alignment for derivations. Reuse the border-preserving extraction logic across the legacy Python importer and current capture browser extractor, and validate structural fidelity as well as absence of rendering errors. Any database repair should replace only source-confirmed table spans, retaining mathematical values, content identities, answer-field links and learner history. The three missing practice keys/solutions require their own reviewed completion.

**No database or application-code changes were made.** Only audit evidence and local previews were written.
