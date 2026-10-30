# Parametric graph readability repair

Published to math at **T11766** on 2026-10-30; fresh readback and grading verified at **T11768**.

Topic **17592186048293 — Graphing Curves Defined Parametrically**; KP **17592186087721 — Graphing a Curve Defined Parametrically**.

## Result

- Registered generator **parametric-graphs-3** uses one-unit grid lines, larger numerical labels every two units on compact banks or five on wider banks, and labels outside the plotting area so they cannot cover the curve.
- Every option in a bank has the same bounds, numerical aspect, dimensions and styling. Bounds/grid depend on the complete bank, independently of its correct role. Answer curves have no table-point dots, coordinate labels or parameter labels. The worked graph marks the calculated table points.
- Banks are resampled when their unit grid or the distinction between candidates becomes too small at a conservative 240px image width. All 16 imported mathematical families remain supported; some oversized parameter variants are rejected rather than making visual estimation part of the difficulty.
- **16 unused generated questions retired**; **15 new unused questions added**, five per band.
- Used questions **17592186535273** and **17592186697897** remain unchanged, including their existing images and saved responses. The 16 imported practice questions, canonical example, observed level coverage and all old field/answer identities and ownership links are preserved.
- The publication check rejects old renderer versions, inconsistent grid plans, mismatched plot bytes/keys and choice-point overlays. The plot-generation instructions and author/reviewer prompts now require coordinate readability and distinguish unmarked choices from marked solution plots.

Current immutable reference:

`generators/4f/4fde422f2d9b6e0a75ffb58938000e8e0516aa1218d19d731d85a7bc103b1e03/generator.py`

The local `generate/scratch/17592186087721.py` delegates to this same repaired package. The learning service was reloaded to use the new publication check.

## Verification

- Source study: [review and evidence](../../audits/2026-10-30-parametric-plot-readability/README.md).
- Exact reported checkpoints (7,−8), (2,−4), (−1,−2), (−2,−2), (−1,−4) reproduced under the new grid in `reported-reproduction/`; the used database question was not rewritten.
- All 15 replacement tables, displayed formulas, bank uniqueness, keys and readability plans checked. Mathematical fingerprints are distinct across the new pool and do not repeat either retained used curve.
- Readable parameter settings verified for all 16 imported families; wide quadratic, reciprocal, root/cubic and ellipse cases rendered separately.
- **114 actual PNGs** checked for visible grid lines at every integer coordinate, independently of their metadata. Minimum detected line coverage is 0.8357. See `pixel-verification.json`.
- All **75 answer plots** visually inspected in five bank contact sheets. All 15 questions passed desktop UI rendering; widest easy plus moderate/hard representatives passed a 390px phone viewport and were visually inspected. Their choice images measure 262px including borders, exceeding the conservative 240px content-width check after borders. See `render-desktop/` and `render-phone/`.
- **20 regression tests passed**: `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest tests.test_parametric_plot_policy tests.test_matrix_product_prompt_policy`.
- Immutable package CLI checked in every band. Installed package, local entry files and published image bytes verified.
- Exact preview, durable request, committed receipt and readback verified. Concurrent basis changes caused confirmed rejections; requests were archived and preparation refreshed. No unknown request outcome was bypassed.
- **75 live grading checks passed**, testing all five image choices for every new question. No learner attempts were created. Fresh availability is five unused questions per band; see `completion.json`.

## Publication evidence

`verification.json` lists the exact retired and new entity IDs. `publication/requests/` retains the stable requests, receipts and source-aware datom verification. `completion.json` records live grading and preservation checks. `generator-verification.json` records source-family coverage and readability measurements. `candidate-pool.json` is the exact authored pool; `publication/preparation.json` records its normalized delivery identities.
