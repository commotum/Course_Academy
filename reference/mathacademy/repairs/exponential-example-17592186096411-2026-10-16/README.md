# Aligned derivative example

The canonical example for knowledge point 17592186096611 is question 17592186096411 (e-3625). Its original solution used a legacy eqalign block with single backslashes instead of double-backslash row breaks. Replaced it with a balanced aligned environment and four explicit rows: differentiate the expression, apply linearity and constant multiples, differentiate each term, simplify.

The derivative remains 4e^x + 12x^3 - 2x. Native preview passed. A compare-and-swap repair changed only question/worked-solution; exact committed readback preserved all other example attributes. DOM checks using the actual renderer confirmed four aligned rows, no math errors or raw delimiters, and no card overflow at 893, 375, and 320 pixels. No image inspection or screenshots were used.
