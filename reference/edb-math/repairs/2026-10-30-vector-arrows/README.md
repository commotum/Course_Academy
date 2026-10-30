# Vector-arrow recovery repair

Committed to `math` at basis **11863**, source `:agent/codex`: **31 malformed arrows in six fields**, including the three occurrences in tutorial **17592186097837**. Exact committed readback matches the six compare-and-swap replacements; no malformed arrow remains in those fields. The transaction changed only these content values and transaction metadata.

## Cause

The original tutorial capture at `reference/mathacademy/question-capture/13931259/tutorial-2910.html` contains correct MathJax SVG arrows. A long arrow is one semantic `mo` containing an arrow glyph (`data-c="2192"`) plus a clipped, stretched minus glyph (`data-c="2212"`) that extends its shaft.

The `2026-10-22-math-images/reconstruct.py` recovery joined both glyphs into `→−`. Its downstream MathML converter consequently emitted `\overset{\to -}{...}`. The SVG fingerprint validator also flattened those glyphs, so it incorrectly accepted two separate operators as equivalent to the original single arrow. Formulas recovered through original-TeX matching used `\overrightarrow` and stayed correct, explaining the mixed appearance.

Retained history and the earlier receipt identify the introducing transaction as **13194139538976**, basis **5664**, committed **2026-10-23 05:42:21.440 UTC**. This was the later formula-image recovery, not the initial import; the initial stored formulas were image references. Original capture and prior repair records remain unchanged.

## Repair and validation

- Reconstruction now recognizes the observed two-piece SVG arrow and retains its stretching semantics. The downstream converter emits `\overrightarrow`.
- Fingerprinting now treats that construction as one arrow, rejecting the malformed arrow-plus-minus expression.
- All **22 affected original formula assets** reconstruct correctly and match their corrected rendered structure; all 22 malformed versions fail that comparison.
- Three regression tests cover the actual saved arrow, separate arrow/minus tokens, and legitimate subtraction inside an arrow's base.
- All six repaired fields pass the application's strict MathJax rendering checks.
- `apply.py` persists the request key and exact transaction, previews the CAS forms, submits once, and verifies values at the receipt's exact basis. `verification.json` records the result.

The six fields were traced from the complete earlier repair manifest and confirmed against fresh EDB reads. This is a source-bounded repair, not a claim that every possible arrow notation across the whole database was audited; broader string-search attempts exceeded query limits.

Run the regression tests with `.venv/bin/python tests/test_svg_vector_arrows.py`. The browser verification uses the existing MA Playwright environment and `validate.py`. Converter changes are saved in the local repository.
