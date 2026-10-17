# Rendering investigation

Read-only investigation at database basis **3407**. No question, UI source, generator, or database changes were applied. The `proposed` render is an in-memory fixture only.

## Question 17592186235429 / Math Academy q-167324

The stored prompt contains the derivative followed by blank lines and **40 leading spaces** before `{{field-1}}`. It does not contain an HTML `span`.

The frontend creates that span in `ui/question-fields.js` (`inlinePrompt`, around line 122), replacing the answer placeholder with `<span class="field-location" data-field-key="field-1"></span>`. The indentation survives. `ui/learning.js` then passes the text through `marked.parse` (around line 285). Markdown interprets the indented line as a code block and escapes the span as literal text. DOMPurify preserves the valid `pre/code` block; it does not cause the defect. `mountInlineFields` cannot find the escaped marker and puts the answer editor in the fallback field list below the question.

The real renderer confirms one visible code block containing the literal span, zero inline answer slots, and one fallback editor. Joining the existing derivative and `{{field-1}}` on one line produces one inline editor, no fallback editor, and no visible HTML. This is a minimal stored-format repair, preserving the question, answer field, key, choices, and grading.

## Canonical example 17592186096417 / Math Academy e-3634

The problem is simply “Differentiate $x\cos x.$” The excessive width is in its worked solution. Inside `\eqalign{...}`, each of the three intended line endings is a **single backslash followed by a newline**, rather than the TeX row separator `\\`.

MathJax accepts the expression without an error but treats it as one table row. It renders an approximately **817 px** equation in a **698 px** desktop content box; at a 375 px viewport the box is 290 px wide. The CSS intentionally gives oversized display equations horizontal scrolling, so the malformed source becomes the long side-by-side equation the user saw.

Changing only those three row separators to `\\` in the in-memory fixture produces four aligned steps, approximately **286 px** wide. It fits at both measured viewport widths (893 px and 375 px), with no horizontal scroll and no MathJax errors. The mathematics is unchanged.

## Evidence

- `capture-3407/snapshot.json`: exact captured question records.
- `rendering-probe.cjs`: replay using the actual `learning.js` Markdown and field-control functions, shared `question-fields.js`, Marked, DOMPurify, MathJax configuration, and application CSS. Serves local files only and does not submit answers.
- `rendering-report.json`: current/proposed DOM and geometry checks at both viewport widths; browser error list is empty.
- `rendering-current.png`: visually inspected reproduction of both defects.
- `rendering-proposed.png`: visually inspected minimal formatting corrections.

The screenshots deliberately show the captured leaf questions and their worked solutions, not the parent multistep function bank. Parent context and question provenance are being investigated separately.
