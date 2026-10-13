# Canonical raster and widget extraction

## 1. Specific source assets

Canonical e-4395 uses the copied full-resolution raster canonical-e4395.png. It displays three labeled 3×3 bracketed arrays in one horizontal row, black on white, A/B/C separated by commas. There are no axes, curves, scales, colored highlights or plotted geometry. At original resolution the entire bank is legible:

- A = [[0,0,0],[0,0,1],[0,0,0]], not lower triangular: a23=1.
- B = [[0,0,0],[0,0,0],[1,0,0]], lower triangular: all entries above the diagonal vanish.
- C = [[1,0,1],[0,0,0],[1,0,1]], not lower triangular: c13=1.

The authoritative original MA q-42090 screenshot was also inspected at full resolution. Its five labeled text choices form a single multiple-choice widget; one complete prompt bank has A 4×4, B/C 3×3. The normalized JSON confirms question_format multiple-choice and choice_count 5. It contains no duplicate response demand. Copies and exact original paths/dimensions/SHA256 values are in plot-provenance.json; the extracted normalized widget is authoritative-widget.json.

## 2. Shared representation

The raster encodes a native mathematical array bank. It does not require a geometric diagram or parametric renderer. Every practice question already uses TeX matrix arrays. The canonical example anchors the same whole-subset zero-support method as the moderate sources.

## 3. Components

Full matrices, labels, square dimensions, integer entries, row/column indices, diagonal positions and the requested lower/upper criterion are mathematical components. Brackets, row spacing and commas are presentation. Every original canonical entry, including the otherwise incidental diagonals, was read; both wrong matrices and their witness positions were inspected rather than only correct B. The zero B diagonal is allowed by the introduction.

## 4. Reusable specification

Use native TeX `[\begin{aligned}...\end{aligned}]` blocks for all complete matrices. The generator's actual matrix instance drives prompt, radio math options and repeated solution blocks; the corresponding exact nonzero entry drives every witness equality. No source asset is reused for changed parameters. Plot rating is none, and step7 needs no Matplotlib/TikZ implementation. These PNGs are retained read-only evidence, not generated question plots. No SVG or image model is used.
