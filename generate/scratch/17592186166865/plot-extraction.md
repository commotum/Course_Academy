# Plot extraction and specification

## 1. Original diagrams

All seven actual original rasters were inspected in `originals.png` (white composite contact sheet) and their individual files. q-127359/q-127493 show blue circles centered at the origin with ±radius labels at four axial extrema. q-127360/q-127497/q-127499/q-127500/q-127502 show a blue circle, an orange center marker, exact center-coordinate text below, a horizontal dashed radius to the right, and a thin brace above with a radius label. q-127499 is tangent to both coordinate axes. q-127500 is tangent to the x-axis and lies entirely left of the y-axis. q-127502 is centered on the y-axis below the origin. Black coordinate axes have arrowheads toward positive x and y, italic axis names, and no grid. Plot placement is first in the prompt; choices and solution contain no additional plots.

## 2. Shared mathematical purpose

The plot supplies the circle's center and radius. Equal coordinate scale and exact labels must make the recovered equation agree with the visible circle. The apparent ellipse introduced by unequal aspect would be mathematically misleading.

## 3. Components

Each instance has a white background, black axes through (0,0), equal-scale blue circle `(h+r cos t,k+r sin t)`, and bounds including both circle and axes origin. Origin-centered variants label axial extrema ±r. Shifted variants mark (h,k), show a dashed radius from (h,k) to (h+r,k), label that exact radius above its brace and the center below. Signed and fractional values use conventional mathematical labels. Center labels are explicitly supplied, so hard does not claim unlabeled scale interpolation.

## 4. Renderer

Matplotlib Agg, cached read-only Python 3.10 dependency fallback, 5.4×5 inch figure, dpi140. Full parameter strings enter a unique temporary input file; final PNG and JSON sidecar writes are atomic, and cache hits require both files. Sidecars contain the exact parameters, axes transform, extents, labels, bounds, and actual dependency provenance. No direct SVG, image model, installation, or active cache pruning is used. Each call uses its own render-input directory, including simultaneous identical and different parameter requests.

Original replay uses the exact original image reference only at the independently read original geometry; changed parameters always render their own circle. The recreated original circle is still checked independently through its own PNG. Validation reads blue pixel extents back through the recorded axes transform with a four-pixel stroke/antialias allowance; checks equal x/y coordinate scales, exact labeled center/radius, axis origin, positive radius, extents and source records. This checks actual curves, not merely metadata. Visual QA covers original plots, origin extrema, changed signs and fractional centers with no clipped labels.
