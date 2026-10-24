# Missing visible percentages in question 17592186508947

Read-only audit of `math` at **T6489**. Question **q-85526**, KP **17592186115384** (“Interpreting a Decay Rate”), topic **1629** (“Interpreting Exponential Decay”). No database or application code was changed.

**The original answers include percent symbols. The database retains those symbols, but four answer values contain invalidly escaped percentage notation.** They store `$30%$` or `$70%$` instead of `$30\%$` or `$70\%$`. The UI passes embedded math in these prose answers to MathJax; the bare `%` starts a TeX comment, so only `30` or `70` renders. The answers are correctly classified as text because they are full sentences containing inline math.

| Answer entity | Intended visible answer |
| --- | --- |
| 17592186508429 | The population of ticks decreases by 30% every week — correct |
| 17592186508515 | The population of ticks decreases by 70% every week |
| 17592186508617 | The population of ticks increases by 70% every week |
| 17592186508679 | The population of ticks increases by 30% every week |
| 17592186508696 | There were 70 ticks initially — intentionally no percent sign |

The original capture `reference/mathacademy/capture/linear/14195578/observations/step-q85526-7a7c74f995b9f5aa8ae3.json` retains rendered percent glyphs and MathML `<mi mathvariant="normal">%</mi>` in all four percentage choices. Its extracted choice strings already contain the unescaped percentages. Retained database history shows each current answer string asserted at **T2151**, with no later answer-value changes. Thus the formatting error existed at ingestion; it was not introduced by the recent UI or table corrections.

The extraction cause is the MathML `mi` handler returning token text without escaping TeX special characters. `scripts/question_capture/dom.js` escapes special glyphs in `mo` and `mtext` but returns raw `mi` text. Re-extracting this original saved question with the current DOM extractor reproduces all four unescaped percentages. The historical Python renderer has the same raw-text override in its `mi` branch. This is a conversion/escaping defect, not omission of the original symbol.

The current shared `normalize_prose` corrects these strings, and `validate_prose` rejects the unescaped originals with “Unescaped percentage glyph comments out math.” Those safeguards do not retroactively repair existing answer entities. The earlier TeX-boundary database repair targeted content/prose attributes and did not modify `answer/value`; these radio-choice values therefore remained unchanged.

The actual current player `answerValue` function and MathJax were tested against all five stored choices. The stored strings render **zero percent glyphs**, with no MathJax errors. A local preview that changes only `%` to `\%` in the four affected values renders **all four percent glyphs**, preserving numbers and prose. The fifth choice remains unchanged. A repair would change only those four answer values; field/correct links, answer types, IDs and selection-based grading can remain intact.

Evidence: [stored records](question.json), [retained answer history](answer-history.json), [source comparison](source-comparison.json), [current DOM extraction](current-dom-extraction.json), [render comparison](render-comparison.json), [stored rendering](stored.png), [escaped-percent preview](escaped-percent-preview.png), [normalizer/validator behavior](normalization-verification.json).
