# Deferred study repairs — awaiting the user

**Applied on 2026-10-15 after the user's explicit instruction.**

All 181 prepared compare-and-swap field replacements were committed at basis 2615
and verified by exact readback. The retained payload and request key are unchanged.
See `authorization.json`, `receipt.edn`, and `verification.json`.

The additional question-completeness findings remain investigation-only and have
not been repaired. Their follow-up is in
`../2026-10-15-question-quality-investigation/`.

## Ready visual repair

The latest transaction contains 181 compare-and-swap field replacements on 173
entities. It replaces 41 formula images with semantic TeX, stacks independent
matrix groups, and moves inline matrices into bounded display blocks. Matrix
entries, row/column counts, augmentation rules, labels, colors, and highlights
are preserved. The shaded row-echelon schematic remains an intentional diagram.

Five containing lessons were captured at basis 2548:

- 17592186048980 — Row Echelon Form
- 17592186049120 — Elementary Row Operations
- 17592186049422 — Solving 2x2 Systems of Equations Using Gaussian Elimination
- 17592186050267 — Solving Systems of Equations Using Back Substitution
- 17592186050527 — Creating Rows or Columns Containing Zeros Using Gaussian Elimination

The complete audit covers 1,380 fields and 203 question/example records, including
tutorials, canonical examples, practice prompts, worked solutions and answers.
`fields.json` contains before/after values. `changes.json` explains each change.
`image-replacements.json` retains source hashes and MathML/transcription evidence.
All source PNG formula images were visually inspected; representative restored
formulas and stacked matrices were also inspected as rendered screenshots.

`17592186262981` currently contains TeX in both its prompt and worked solution,
with no image references, so this entry needs no image-removal transaction.

## Checks completed

- All 1,380 fields rendered through the actual lesson Markdown, sanitization,
  MathJax and CSS at 810 px and 375 px viewport widths. No exposed TeX, collapsed
  matrices, MathJax errors, or content-card overflow remained. Individual wide
  equations can still use the UI's contained horizontal scrolling on mobile.
- All 1,102 matrix occurrences match their prior content or recovered image source,
  including explicit augmentation columns and teaching highlights.
- Independent arithmetic/row-echelon checks passed for 34 supported question forms,
  respecting prompts that explicitly ask about coefficient matrices.
- `preview.edn` is an in-memory EDB preview at db-before 2550, with
  `:edb/committed false`. Its hypothetical db-after is not a committed basis.
- The transaction changes text attributes only. It contains no learner progress,
  answer keys, component links, or generator registration changes.

Rendering, preservation and sampled answer-key checks do not constitute an
exhaustive proof of every worked solution in these lessons.

## Additional quality findings

`content-quality-findings.json` records 18 existing incomplete question records:
13 have missing correct answers and missing worked solutions; five have an older
unkeyed answer field alongside a keyed field with the same field key. These need
separate completion/ownership review. They are **not** silently repaired by the
visual transaction, and no answer key has been guessed or changed.

`generator-scripts.json` inventories the 13 scripts currently built for these
lessons. No generator or shared production formatter was edited during this
preparation. Layout normalization should be carried into relevant producers when
changes are authorized so later inventory does not reintroduce horizontal groups.

## Retained application procedure (completed for the visual repair)

1. Recheck the exact transaction hash and saved rendering input hashes. Read the
   current values for all 181 guarded fields; stop to reconcile any concurrent
   changes instead of overwriting them.
2. Use the explicit application source and exact retained payload/request key in
   `commit-intent.json`. Only after the user's instruction, submit that request.
3. Retain its receipt and verify all values at the receipt's exact db-after basis.
   A lost reply must be reconciled with the same payload and request key.
4. Handle the additional incomplete/duplicate-field findings separately, with
   verified answers and preservation of existing learner history.

The earlier `transaction.draft-*.edn` is a superseded, never-submitted draft.
Only `transaction.edn` matches the active pending intent and the latest preview.
