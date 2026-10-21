# Equation-chain import investigation — October 18, 2026

The current database contains **1,619 text fields across 262 lessons matching the demonstrated equation-chain or unsupported-command defects**. Another 9 fields across 5 additional lessons contain legacy `\eqalign` without one of those defect signatures; those are review candidates, not proven broken displays.

This investigation made **zero database writes**. The preceding quotient- and power-rule repairs remain separate completed transactions.

## What actually happened

There are two source-to-storage paths, and the retained history distinguishes them.

1. **Original archived lesson import.** `scripts/generate_ma_lesson_seed.py` copies lesson Markdown into `:tutorial/content` and example fields without a shared LaTeX layout normalization or rendering check. The seed for tutorial `17592186065338` already used a working `aligned` environment. Other archived Markdown, including portions of the fractional-exponent examples, already contained incomplete rows such as `expression &= \\`.
2. **A later live capture regressed working content.** EDB history shows tutorial `17592186065338` and example `17592186063922` seeded at basis **36**, then replaced at basis **1933** with raw legacy `\eqalign` and single-backslash row separators. The exact committed capture request is `capture-c89d82c7-0caa-4823-9861-2d7d5362806a`, and its manifest identifies the power-rule lesson capture at `reference/mathacademy/capture/linear/14160977` on October 13. The raw strings are present in both the saved capture manifest and that transaction's receipt; this is not inferred from a filename or the current importer alone.
3. **SVG-title path.** `capture/scripts/browser/extract.js` reads plain text from an SVG title when MathML is absent. The retained titles contain legacy `\eqalign`, single backslashes before line endings or `[5pt]`, and equality markers attached to the preceding expression. Copying that metadata does not produce portable, correctly aligned TeX.
4. **MathML path.** The browser extractor and `scripts/import_historical_question_content.py` emit `mtable` as `aligned`, `mtr` as rows, and `mtd` as cells. A source row containing `[expression, =]` becomes `expression & = \\`; the next expression remains on another row. The converter preserves presentation cells without reconstructing the equality chain. Offline replay reproduces this output on the actual retained power-rule MathML.
5. **Validation did not establish visual correctness.** Balanced braces, valid entity references, correct answer links, or exact readback do not detect an empty right-hand side. The configured MathJax `noundefined` extension can render unsupported `\require` as red text without producing an `merror` node. All eight bad witness pages passed the existing renderer's structural status check, despite red undefined-command nodes on three pages and visibly broken equality layouts.

The source metadata is evidence of what was captured, not proof that those strings were ready for direct use by our renderer. This audit does not establish why the upstream SVG title had those spellings.

## Reproduction and current prevention

[Eight retained source fragments](source-fixtures.json) cover four SVG-title formulas and four MathML formulas. The [offline reproduction](reproduction.json) runs the current browser extractor and historical Python converter against those exact fragments. It confirms the raw extraction failure and that the shared preparation formatter now repairs their complete empty-RHS chains.

The current capture preparation calls the shared formatter, and separately attributed repairs are preserved. The historical standalone seed generator still does not use that boundary. Current validation also needs stronger coverage for unsupported `\require` and mixed complete/incomplete equation rows; the recent complete-chain normalizer alone does not cover every finding in this audit.

Six detector-control tests passed. They distinguish complete aligned equations and valid continuations from broken chains, preserve legacy-only cases as review-only, detect malformed `[5pt]` separators, and verify the eight source replays.

## Scope and findings

Snapshot: database `math`, basis **4476**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. The native reader inspected all five text attributes: tutorial content, question prompts, worked solutions, answer values, and answer feedback. Counts in the native manifest are current attribute contributions; findings are deduplicated by entity and attribute.

| Signature | Fields | Interpretation |
| --- | ---: | --- |
| Complete chain with empty right-hand sides | 1,044 | Same layout defect as the repaired power-rule examples; conservative normalizer can reconstruct these chains. |
| Mixed complete/incomplete equation rows | 306 | Same dangling-equals symptom, but requires source review before repair. |
| Single-backslash legacy row separator | 222 | Newline or optional spacing was written with one backslash instead of a TeX row separator. |
| Unsupported `\require` command | 139 | Current UI does not load the `require` extension; cancellation itself is already loaded. |

Of the matched fields, 1,552 are currently attributed to Math Academy and 67 to agent/application sources. Those later contributions can also carry or recreate the same layout defect. Current attribution does not establish the exact historical conversion path for every field; the four traced power-rule entities provide direct transaction-level evidence.

These categories overlap; their counts must not be added. The audit is a targeted screen for these defects, not a certification of all LaTeX or all mathematical content. Every finding was mapped to its owning lesson. Some content can be shared across lessons.

| Lesson | Lesson entity | Matching fields | Example affected entity |
| --- | --- | ---: | --- |
| Dividing Rational Expressions | `17592186048690` | 41 | `17592186068597` |
| The Antiderivative | `17592186049481` | 39 | `17592186064038` |
| Simplifying Linear Expressions Containing Fractions | `17592186049047` | 36 | `17592186138069` |
| Further Rationalizing Denominators of Algebraic Expressions | `17592186048758` | 35 | `17592186212794` |
| Adding and Subtracting Rational Expressions | `17592186049782` | 29 | `17592186068590` |
| Collecting Like Terms in Linear Expressions | `17592186050452` | 28 | `17592186054374` |
| Solving Cubic Equations by Grouping | `17592186050551` | 27 | `17592186083042` |
| Simplifying Linear Expressions Using the Distributive Law | `17592186050575` | 27 | `17592186054378` |
| Rationalizing Denominators | `17592186048702` | 25 | `17592186105481` |
| Adding and Subtracting Radical Expressions | `17592186048138` | 23 | `17592186179463` |
| The Method of Frobenius | `17592186048177` | 23 | `17592186147232` |
| Evaluating Numerical Expressions Containing Radicals | `17592186049299` | 23 | `17592186078317` |

The full [lesson list](affected-lessons.csv) contains all 267 matched/review lessons. [Detailed findings](findings.json) retain exact current text, source attribution, detector reasons, owning questions, and lesson links. [Summary](summary.json) records scope and counts. The recently repaired power-rule lesson is absent from these remaining findings.

## Next repair boundary

Use the matching complete-chain and unsupported-command queues to prepare small, guarded repairs. Review mixed rows against the retained source before rewriting them. Keep legacy-only cases separate. Apply rendering checks for undefined-command nodes and horizontal clipping in addition to `merror` checks, then verify the committed content. No bulk changes have been applied by this investigation.
