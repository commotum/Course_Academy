# Related Completing the Square lessons: committed repair

**Committed and verified in math, basis 3573 → 3574.** The user authorized
preparation and submission without another confirmation. The transaction was
submitted once; the durable receipt reports `:edb/replayed false`.

The repair contains **147 guarded text updates across 137 entities**:
99 worked solutions, 13 question prompts, four tutorials, and 31 answer values.
It fixes the findings from the [ten-lesson audit](../../audits/2026-10-17-completing-square-related/audit.md):

- 63 misplaced underbraces.
- Five broken legacy equation blocks in four canonical examples.
- 14 equation chains with trailing equals signs.
- 43 unformatted function names across 38 attributes.
- Broken bold in the circle tutorial and three missing prompt/equation breaks.
- Seven slash-form fractions in the hyperbolic material.
- Two confirmed sign typos in integration solutions.

The modified instructional text also received bounded punctuation and
closing-parenthesis cleanup. The 31 answer changes add operator markup only;
removing that markup reproduces the exact old strings. None of those answers
had historical response references, and their existing fields had no correct
answers. Their identities, bank memberships, and missing-key state are preserved.
All existing keys, learner history, difficulty, curriculum links, and lesson
routes are unchanged. The 33 missing solutions and 36 questions with missing
keys remain separate work. No question generators were modified.

## Review and evidence

- [Transaction](transaction.edn), [readable diff](changes.diff), and
  [structured edits](changes.json).
- [Plan](plan.json), [saved request](request.json), and exact
  `commit-intent.json` with the authorized transaction bytes.
- [Durable receipt](receipt.edn) and [committed verification](commit-verification.json).
- [Validation summary](validation.json), [native preview](preview.edn), and
  [preview verification](preview-verification.json).
- Rendered repairs: [integration examples](sample-0.png),
  [inverse reciprocal hyperbolic examples](sample-1.png),
  [odd-linear-term tutorials](sample-2.png), and
  [circle and hyperbolic tutorials](sample-3.png).

Preparation used a fresh snapshot at basis 3573 and the existing `:agent/codex`
contributor. All replacements use compare-and-swap forms, with a whole-basis
guard on the saved submission. No schema or contributor records were added.

The native preview and durable receipt contain exactly the planned scalar
retractions/assertions plus transaction time. Full readback at basis 3574
matches the preview for all 306 questions, 12 tutorials, ten activities, and
31 knowledge points, including nested answer banks and captured response refs.

All 318 content items passed desktop/mobile checks in editable and answered
states: 1,272 item renders, with no browser exceptions, MathJax error nodes,
or outer card overflow. Representative fixes were visually checked; legacy
blocks now have multiple rows and show no literal row-spacing commands.
Exact algebra verifies all 28 adjacent equalities in the reorganized rational
equation chains and both sign corrections. This is not a complete independent
audit of all answer keys or integral domains.

`prepare.py` reproduces the transaction from pinned evidence without submission.
`verify.py` checks the saved preview; `verify.py --commit` verifies the durable
receipt and committed readback. Preserve the saved request key, source, basis,
and transaction bytes for any receipt recovery. No further submission is needed.

SHA-256: `8264f91840e31aa3808dd9135855faee760f446afcefaa10c3a24c1c66f2eeab`.
