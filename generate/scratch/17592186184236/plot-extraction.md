# Four-stage plot extraction and specification

## 1. Individually observed plots

All seven original KP assets were individually viewed at original 353×298 or 353×299 resolution. The tutorial's 353×298 plot was separately inspected as curriculum evidence. Original prompt/choice/solution inventory: 7 prompt graphs (6 practice + canonical), 0 choice PNGs, 0 worked-solution PNGs. Each plot's tick calibration, actual branch pixels, dashed asymptotes, intercept label and axes arrows are recorded in source-geometry.json. Source q-143638 has particularly narrow asymptote spacing; it is fit with its own coordinate scale, never copied from another asset.

## 2. Shared purpose

A single central increasing branch determines B through asymptote separation and D through its y-axis intercept. The function is tan(Bx)+D: vertical scale 1 and phase 0. The graph is not an arbitrary shift of a sibling curve. Horizontal pixel scale varies per original while vertical scale remains independently calibrated by the intercept label.

## 3. Components

White background, black arrowed axes, positive x arrow right and positive y arrow up, two gray dashed asymptotes at ±π/(2B), one blue monotone tangent branch between them, exact π-fraction x labels, and a signed or fractional intercept label. No source branch arrows or worked-solution stage arrows exist. Source-only originals reuse their exact hash-verified asset when every meaningful parameter agrees.

## 4. Parameterized Matplotlib specification

Matplotlib (Agg), 728×637 PNG; primary renderer currently uses Python3.13.5 and Matplotlib3.11.2, with an existing read-only Python3.10/cached-wheel fallback when necessary. Sidecars report actual Python/Matplotlib/NumPy versions and dependency paths. Render input derives only from the supplied instance. Unique input files and atomic PNG/sidecar writes prevent concurrent parameter contamination; cache hits require both files. No direct SVG, image model, or white text masking boxes.

The displayed branch uses y=tan(Bx)+D, with exact asymptote endpoints converted numerically only for drawing. Windowed branch endpoints are computed with arctan so the branch never connects across an asymptote. Bounds include zero, the intercept and sufficient visible tails. Easy labels the two asymptotes directly and labels D. Moderate has two horizontal subdivisions, labels ±H/2, and uses half-unit vertical grid lines. Hard has three subdivisions, labels ±2H/3 and uses quarter-unit vertical grid lines. Dashed asymptotes are distinguished from thin grid lines. A small ordinary point marks y(0). Numeric y labels sit in the left margin and calibrated x labels below the graph so branch pixels remain visible. The grid caption states the actual vertical scale.

Renderer asserts every text bounding box stays inside the image, no two boxes overlap, and each box clears actual blue branch pixels by at least 2.5 pixels. It verifies blue pixels at five independently computed curve points, gray dashed asymptote pixels, and nonempty monotone branch geometry. The independent validator reads the actual displayed x-label fractions, reads D from blue raster intercept pixels calibrated by displayed y labels, and checks all displayed equations. Original raster fitting permits at most a 1.5-pixel stroke-center span allowance and checks fitted D, full branch residuals, positive monotonicity and actual intercept-label clearances; those tolerances are explicitly separate from generated geometry.

Rendered examples at each level were individually viewed at full resolution; original styles and authored calibration changes are labeled in review.md. Assets are retained for parent QA; no active caches are pruned.
