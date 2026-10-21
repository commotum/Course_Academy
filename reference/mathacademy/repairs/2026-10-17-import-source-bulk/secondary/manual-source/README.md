# Narrow source-authored marker repairs

The three SVGs and their original title HTML retain broken `[math]` markup in
otherwise complete equations. This is an additional source formatting defect,
not evidence that the mathematical expressions are different. The manifest
binds each exact original title and original SVG to the archived source.

`convert_source.py` replaces only the failed-marker glyph sequence with the original currency dollar glyph for these
three exact source IDs and SHA-256 hashes: one marker in the conditional
probability calculation, and four markers in each percentage calculation.
All operands, equality steps, percent glyphs, cancellation, blue numerator,
and green check marks remain derived from the complete source MathML.

- `6053:step-572517:521517`: P(Paints and ≥$12) = 4/20 = (1·4)/(5·4) = 1/5,
  retaining the cancellation step.
- `6646:step-576872:91350`: $300×(100%+35%) = $300×135% = $300×1.35 = $405.
- `6663:step-576843:88652`: $240×(100%−5%) = $240×95% = $240×0.95 = $228.

A fourth source-specific guard in the converter restores literal set braces
inside `3428:step-182411:340346`. The preceding source sentence explicitly
defines A = {0.2, 0.5, 0.99}; the condition in the function is membership in
that same finite set. The old nested `[math]` text retained unescaped grouping
braces, which would disappear if replayed literally as TeX.

Independent original-SVG comparisons in `../../review/render-*-893.png`
confirm these markers represent currency dollars; simply deleting them would
lose visible source information.
