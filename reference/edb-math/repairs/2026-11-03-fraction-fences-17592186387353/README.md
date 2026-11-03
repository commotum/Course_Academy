# Fraction-containing expression fences

Applied to math at **T12417** on 2026-11-03. Reported question **17592186387353** is imported **q-123203**, under “Evaluating a Vector-Valued Function,” in topic **17592186050171 — Defining Vector-Valued Functions**.

The previous fraction-sizing rule recognized only a signed fraction by itself inside parentheses. It correctly sized `r(π/3)` and the squared negative fraction, but missed `(5·π/3)` and `(6·1/2)`. It did not size the surrounding vector-angle brackets. This is why otherwise similar fences had visibly different heights in the reported solution.

The shared formatter now follows balanced parentheses, square brackets and vector angles around complete fraction-containing expressions, including products and sums. It respects TeX group and alignment-cell boundaries, script/annotation scope, optional indices and explicit delimiter sizes. Small parentheses around ordinary negative numbers remain small. Unicode vector angles are given equivalent portable TeX delimiter spellings when sizing is added. Ambiguous conditional/absolute-value bars and mixed interval fences are outside this extension.

The final displayed answer remains ⟨3, 3/4⟩. The correction changes only fence sizing and equivalent angle spellings; every arithmetic symbol, coordinate, coefficient, sign, exponent, answer identity, correct link and saved response is preserved.

All **60 questions/examples across the lesson's three KPs** were checked:

- **17592186068857:** Evaluating a Vector-Valued Function.
- **17592186068858:** Finding the Magnitude of a Vector-Valued Function.
- **17592186068859:** Evaluating a Three-Component Vector-Valued Function.

**23 questions repaired, across 49 attributes:** 17 prompts, 22 worked solutions and 10 answer values. All three KPs were read back exactly at the committed basis. No generator is registered for these KPs; the shared publication path normalizes output from other generators, including packages with older formatter copies, before assigning stable identities. Source imports use the repaired shared formatter. Author/reviewer prompts now require inspection of actual fence height for mixed fraction expressions.

Validation:

- **77 focused regressions**, **48 formatter tests**, and **14 capture-preparation tests** passed.
- All 23 repaired questions passed the actual learner UI. The reported question also passed a 390px phone preview, and its repaired desktop screenshot was visually inspected.
- The reported solution's previously small parentheses measured about **28.69px** high. Their median height after repair is **51.61px**, enclosing the fraction expressions. The already-scaled parentheses retained their sizing. Actual per-glyph measurements are in `render-verification.json`.
- The 10 changed answer values retain identical import-matching identities.
- **65 live grading checks** passed, including correct complete responses and every alternative discrete choice. Two partial imports were preserved without inventing missing keys. No duplicate choices were introduced and no learner attempts were created.
- Learner activity added the valid alias `4\ln2` to an unrelated answer bank while this audit was running. It was already present before the repair transaction and was preserved. Verification uses the transaction's exact committed basis, rather than mistaking concurrent activity for a formatting regression.

[Corrected reported question](desktop/question-004.png). `capture.json` retains the original text; `proposals.json` contains the exact edits. `publication/` retains the durable request, preview, receipt and full before/after readback. `verification.json` and `completion.json` record deployment and grading. The workflow is `build.py`, `render.py`, `deploy.py` and `verify_live.py`.
