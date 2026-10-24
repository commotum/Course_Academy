# Shared blank sizing — applied

Question **17592186662826 / q-214693** asks for the solution to `2 < x+5 < 7` with three separate inputs: a lower bound, a comparison operator, and an upper bound. The expected response is `-3 < x < 2`. Its stored field order and inline markers are intact; the display issue was shared UI sizing. No database records were changed.

## Cause

Ordinary inline MathLive blanks had an **8ch minimum width**, regardless of whether they held one operator or a longer expression. Only `.matrix-answer` cells had the previous content-fitting rule. Text blanks used a separate JavaScript width calculation with an 8ch minimum and **30ch maximum**. Standalone math blanks occupied the entire available row. These inconsistent rules made the reported inequality unnecessarily wide and limited longer text answers.

## Behavior now

- **Value blanks:** inline entries start at a compact **3.5ch minimum**. Their actual rendered content determines any larger width.
- **Statement/equation blanks:** standalone entries start at **16ch**, with room for a complete response; they also grow and shrink with content.
- These are layout defaults, not guesses based on the correct answer. Existing types, input names, IDs, values, response collection, grading, and keyboard behavior are retained.
- MathLive controls use intrinsic `max-content` sizing, so fractions and exact expressions also gain the height they need. Native text controls use `field-sizing: content`, with a native `size` fallback when that property is unavailable. The old 30ch ceiling is removed.
- Controls respect the available page width. Very long expressions remain editable through the editor's own horizontal scrolling rather than stretching the page. Existing editable matrix cells retain their 4.5ch/3ch responsive minima and the matrix's horizontal overflow behavior.

Changes are in `ui/question-fields.js` and `ui/learning.css`. The running app serves both updated files with cache revalidation; reload the quiz to pick them up. The shared control/mounting functions are used by lessons, quizzes and assignments.

## Verification

The new `tests/blank-sizing-browser.py` exercises the real Markdown renderer, shared blank controls, MathLive, stylesheet and app theme at **1100, 768, 390 and 320px**. It verifies:

- all three reported short values fit in compact controls;
- empty controls retain a usable minimum rather than collapsing to the caret;
- typed polynomials grow and shrink when cleared;
- restored exact fractions and read-only responses size correctly;
- text answers grow beyond 30 characters and shrink after deletion, including with native `size` fallback;
- very long expressions stay within the page;
- no browser errors or learner/API writes.

The existing `tests/math-input-browser.py` typing/Enter/incomplete-answer/disabled checks, `node --test tests/question-fields.test.mjs`, and `tests/matrix-overflow-browser.cjs` also passed. The matrix fixture needed its missing current-renderer `protectMath` import restored; its production layout assertions remain unchanged. Matrix checks cover responsive geometry, checkbox/radio math, growing vector entries and saved values.

Evidence: [reported question on desktop](after/inequality-1100.png), [reported question on phone](after/inequality-390.png), [exact solution input](after/exact-solution.png), [measured geometry](after/verification.json), [served asset hashes](served-assets.json), [original stored record](question.json). Original UI source snapshots are retained as `before-learning.css` and `before-question-fields.js`.
