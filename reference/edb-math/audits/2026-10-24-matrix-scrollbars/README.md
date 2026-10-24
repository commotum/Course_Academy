# Individual matrix scrollbars — root-cause audit

Read-only database investigation at **T6349**, with a local reproduction through the quiz Markdown renderer, stylesheet, MathJax configuration and SVG output. The shared CSS correction has now been applied and verified; no database changes were made. Original diagnostic measurements are preserved.

All three reports have the same cause: **the independently scrollable matrix operand wrapper includes the layout bounds of MathJax's visually hidden accessibility MathML**. Short matrices fit visibly, but the hidden element is one pixel taller than the wrapper, triggering a vertical scrollbar.

## Reproduction

The stored question statements all use `.matrix-operands`, emitted by `scripts/question_capture/math_format.py:572`. The shared stylesheet contains:

```css
.prose .matrix-operands > div { min-width: 0; max-width: 100%; overflow-x: auto; }
.prose .matrix-operands > div > mjx-container { display: block; }
```

In Chromium, the first rule computes to **`overflow-x: auto; overflow-y: auto`**. The block MathJax container inherits the prose's **27px line height**. MathJax also creates an absolutely positioned `<mjx-assistive-mml>` beside its SVG. That accessibility element is visually clipped, but its native MathML line box plus **1px top padding** measures **28px** and contributes to the scrollable extent. The wrapper is 27px high, so it scrolls vertically by **1px**. With ordinary native scrollbars enabled, a 15px-wide scrollbar appears beside an otherwise fitting matrix.

| Question | False scrolling reproduced |
| --- | --- |
| 17592186547255 | Both 1-by-4 operands, P and H |
| 17592186635728 | The 1-by-2 operand R; the taller 2-by-1 S fits |
| 17592186634808 | Both 1-by-2 operands, P and R; the taller 2-by-4 S fits |

Example: the first operand in 17592186547255 has `clientHeight=27`, `scrollHeight=28`, and an actual 1px vertical scroll range. Its SVG is only about 18px tall and fits horizontally. The hidden accessibility element is 28px tall. This explains why an individual matrix gets its own scrollbar even on a wide desktop.

Stored TeX and matrix dimensions are intact. The first question acquired its operand wrappers at T2857; the other two already had them when created at T4627 and T4633. These predate the table repair T6318–T6328. They belong to three KPs with different generators, confirming the common point is the shared operand layout rather than one question's mathematical content. Ownership and retained statement history are saved beside this report.

## Controlled experiments

Reproduced at viewport widths **1100, 768 and 390px**, with Chromium's native scrollbars explicitly enabled. `reproduce.py` uses the actual player Markdown function and local bundled assets.

- Removing only the hidden accessibility element **in the diagnostic browser** reduces the short wrapper's scroll height from 28px to 27px and removes the false scrolling. This is a causal isolation experiment, not the proposed fix.
- Bounding that element to 1px while retaining it also removes false overflow.
- Applying the following scoped container correction retains the accessibility DOM and makes the short SVG/hidden-MathML layout fit naturally:

  ```css
  .prose .matrix-operands > div > mjx-container { line-height: 0; }
  ```

  Short operands then measure approximately 18px, with no vertical overflow. Taller matrices remain intact. Every reported operand has zero false scroll range at all three viewport widths. A synthetic 30-column matrix still scrolls horizontally when necessary, with no vertical scroll range.
- `overflow-y: hidden` hides the bar but leaves the hidden overflow; changing the SVG alone to `display: block` actually worsens the mismatch. Those address the symptom or the wrong element.

The scoped line-height adjustment is now applied in `ui/learning.css`. Verification against the actual stylesheet, without experimental CSS overrides, confirms zero false scroll range for all 21 reported operands across the three viewport widths. All three wide-matrix cases retain necessary horizontal scrolling. The accessibility elements remain present and visually hidden. The running server serves the updated stylesheet with revalidation enabled; reloading the quiz loads the fix. See [post-fix verification](post-fix/verification.json) and the [corrected quiz rendering](post-fix/17592186634808-current.png).

## Why prior rendering checks missed it

MathJax parses the formulas successfully, so syntax/error checks pass. Playwright also launches Chromium with `--hide-scrollbars` by default. The reproduction explicitly removes that launch argument and measures `clientHeight`, `scrollHeight`, actual scroll movement and scrollbar width. Future layout checks should include those conditions rather than relying only on a clean formula render or default headless screenshots.

## Evidence

- [Current quiz layout](17592186634808-current.png), [scoped line-height experiment](17592186634808-line-height-zero.png)
- [Measured layout cases](layout-measurements.json), [exact rendered DOM and computed bounds](17592186547255-current-dom-details.json)
- [Stored records](reported-entities.json), [generator/KP ownership](question-ownership.json), [retained problem history](problem-history.json)
- [Reproduction script](reproduce.py)
