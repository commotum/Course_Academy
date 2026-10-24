# Worked-solution LaTeX diagnosis: 17592186233932

Read-only investigation at math basis T6112. No database or application code was changed.

Question `q-342405` asks for the slope of `sec(pi*x^2)` at `x=1/2`, under
“Differentiating a Reciprocal Trigonometric Function Using the Chain Rule.”
Its solution's earliest retained assertion is T74, source `:org/Math-Academy`.
There are no retained subsequent changes to that solution. The current problem
is therefore independent of the recent image, display-integral and answer-marker repairs.

## Root cause

The original history capture contains raw TeX inside HTML paragraphs, rather
than rendered MathML. In particular it has standalone `align*` and `eqnarray`
environments, a nested `eqalign` macro, and `\\[5pt]` row breaks. The saved
capture is `reference/mathacademy/progress-history-2026-10-04/12230045.json`;
its question ID is `question-342405`.

The historical importer, `scripts/import_historical_question_content.py`,
normalizes rendered MathML into delimited Markdown math, but passes ordinary
text nodes through unchanged. Replaying its `Renderer.text()` on this exact
captured solution reproduces the current DB value byte for byte. It reports
zero extraction errors and recognizes zero formula nodes in this source.
The content-only import preparation preserves that result.

`ui/learning.js:279` protects `$...$`, `$$...$$`, `\(...\)` and `\[...\]`
from Markdown parsing. It does not protect standalone TeX environments.
Consequently:

1. Blank lines inside the bare `align*` environment become separate HTML
   paragraphs. MathJax never recognizes that complete equation block, so its
   commands remain visible as text.
2. Markdown consumes one of the two backslashes in `\\[5pt]`. The evaluation
   environment is still recognized, but its row breaks are destroyed. Its
   calculation collapses onto one long line with stray backslash/spacing text.

This is a content-normalization/Markdown-boundary defect. The same original
TeX passed directly to the configured MathJax instance renders both blocks
correctly. It does not require a missing MathJax extension to render.

## Reproduction and validation gap

[renderer-reproduction.json](renderer-reproduction.json) records the exact
pre-MathJax HTML, parsed math items and visible output for three variants:

- Stored Markdown: 3 recognized display blocks; raw `align*` text and damaged
  evaluation rows.
- Original text passed straight to MathJax: all 4 display blocks render.
- An in-memory normalization to `$$`-delimited `aligned` blocks: all 4 display
  blocks render through the actual player renderer.

All three report zero MathJax `merror` nodes. Error-node checks alone miss both
unrecognized raw TeX and damaged row breaks. The stored and corrected screenshots
were visually inspected: [stored.png](stored.png), [candidate.png](candidate.png).

The candidate changes formatting wrappers only. Equations and the answer
`pi*sqrt(2)` are unchanged. It is saved for review in
[candidate-worked-solution.md](candidate-worked-solution.md), not transacted.

A durable repair should normalize affected raw environments at import, repair
stored occurrences, protect supported bare environments at the Markdown boundary,
and detect raw TeX leaks or lost equation rows in rendering checks.
