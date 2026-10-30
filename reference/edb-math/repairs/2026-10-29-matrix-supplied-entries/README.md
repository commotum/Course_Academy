# Restore numerical entries in partial matrix answers

Committed to math at **T11640**, from T11639, on 2026-10-29.

Topic **17592186050122 — Properties of Matrix Multiplication**; KP **17592186115226 — Calculating a Matrix Product Using the Distributive Law**.

The generated question 17592186717716 and eight other generated questions used asterisks for unrequested matrix cells. All 21 imported practice questions and the canonical example were reviewed in `../../audits/2026-10-29-matrix-asterisk-17592186717716/`: none uses this convention. Nine imports use partial matrices with actual numerical values in the remaining cells.

## Repair

- The generator now always supplies the actual remaining matrix entries and says “Fill in the missing entries.” It retains the existing numerical sampling, requested cells, difficulty profiles and worked calculations.
- Nine existing questions were repaired in place by changing only `question/problem`: 17592186717716, 17592186717720, 17592186717722, 17592186717738, 17592186717746, 17592186717755, 17592186717759, 17592186717763 and 17592186717772. Their question, field and answer identities, keys, solutions, difficulties and saved responses remain intact. No questions were added or retired for this presentation change.
- A scoped check in `generate/matrix_product_prompt_policy.py` rejects asterisk cells for this KP at both generation and publication. Author and reviewer prompts now require preserving the source's numerical partial-matrix layout.
- The learning service was reloaded to use the publication check. The local generator entrypoint now delegates to the same repaired package used in production.

Registered immutable generator:

`generators/7f/7f6768bd62ac2dfa9f9bf58768e1a75709f20df2e706449a9c13154946cbef59/generator.py`

## Verification

- All nine repaired grids: requested and supplied entries independently calculated as the two printed matrix products and their sum/difference; final worked matrices also checked.
- 22 fresh samples covering every profile in all three bands: every grid cell checked; same seeds retain the prior operands, targets, solution calculations and correct values.
- Published package CLI: five fresh samples per band verified, including package closure and local/package byte agreement.
- Eleven policy regression tests passed: `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest tests.test_matrix_product_prompt_policy`.
- Nine desktop UI renders and two narrow-screen renders passed the normal math/DOM checks. Reported question and a hard question visually inspected on desktop; reported question also inspected at 390px width.
- Exact speculative transaction and committed receipt verified. Readback preserves all 21 imports, the canonical example, pool membership, every field/answer and learner facts; only the nine planned prompts and generator registration change.
- 18 live read-only grading checks passed: a full correct response and a response with one wrong entry for each repaired question. Verification created no learner attempts.

Evidence: `generator-verification.json`, `render/rendering.json`, `render-phone/rendering.json`, `verification.json`, `completion.json` and the archived exact request under `publication/requests/`.
