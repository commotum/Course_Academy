# Legacy matrix and equation-image repair

Reported example: `17592186059576` / `e-4683`, Finding the Coefficient Matrix of a System of Linear Equations, in topic `17592186050765` / MA 148.

The two systems of equations were PNGs. Their archived SVG titles mix literal TeX wrappers with complete MathML; capture previously treated every such mixed title as an image. The final matrix used a literal `\matrix{...}` title with one backslash before a physical row newline. MathJax consequently displayed one row. The earlier aligned-matrix sweep did not select this legacy syntax.

The correct systems are `x-2y=1, 2y=-1` and `x-2y=1, 0x+2y=-1`. The coefficient matrix has rows `(1,-2)` and `(0,2)`.

## Saved repairs

- Basis **2301**: 18 fields on 13 entities. Corrected all 16 discovered legacy-matrix fields and recovered the equation screenshots in examples `e-4683` and `e-4684` from their saved source.
- Basis **2302**: four additional fields on two entities. Recovered equations and augmented matrices in the remaining lesson examples, `e-4685` and `e-4686`.
- Total: **22 fields on 15 entities**. All ten equation screenshots across the four examples became TeX. The original image files remain available to historical content.

Both commits use source `:application/ca-engine`, CAS preconditions, retained transaction hashes and stable request keys. `verification.json` and `lesson-equations/verification.json` confirm exact readback at each commit's db-after basis. Do not regenerate a committed request to recover an uncertain outcome; use its retained intent and key.

The discovery queries cover tutorial content, question problems and solutions, answer values and feedback, and multistep context. Answer values, feedback and multistep context had no occurrences of this macro. This audit targets legacy `\matrix` syntax, rather than claiming that every conceivable TeX defect is absent database-wide.

## Capture change

`scripts/question_capture/dom.js` now recovers the observed redundant `\eqalign`, system-brace and bracketed-table wrappers when they contain one complete MathML expression. It preserves the augmented column divider. Unknown or ambiguous mixed formulas still become images. Legacy matrix titles become matrix environments with valid row separators; a trailing separator does not create an empty vector row.

The four complete archived example nodes are regression fixtures. Capture processes load `dom.js` when importing `browser.py`, so subsequent launches load the new extractor.

## Verification

- The broader capture regression suite passed **125 tests**. The final matrix suite passed **16 tests**, including all four saved examples and ambiguous-title fallback.
- Every saved repair was rendered through the Markdown renderer from `ui/learning.js`, `ui/mathjax-config.js` and vendored MathJax: 18 fields with 79 matrix/system layouts, plus four fields with six layouts. Row and column counts match the intended TeX structures, with no MathJax errors.
- A fresh complete lesson Pull at basis 2302 includes **50 questions and 331 content fields**. All 331 fields render, covering **286 matrix/system layouts**, with no MathJax errors. No image references or legacy matrix macros remain in that lesson snapshot.
- `coefficient-matrix.png` was visually checked: the coefficient matrix is a 2×2 square matrix. `lesson-rendering.json` and `lesson-audit.json` retain the full lesson checks.

The app needs a page refresh to fetch the corrected content; no app restart is needed.
