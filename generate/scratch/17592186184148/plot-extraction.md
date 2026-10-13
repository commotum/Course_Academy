# Plot extraction and generator specification

## 1. Individual source plots

All 13 assets were opened individually at original resolution, including the canonical plot; there are no answer or solution plots. Each is a white, source 353x298-ish Cartesian viewport (actual dimensions below), black arrowed axes, a blue decreasing cotangent branch, grey dashed positive asymptote, dashed midpoint guides, and exact rational/pi tick labels. The y-axis is itself the asymptote x=0. The curve tails end at viewport borders without finite endpoint markers or curve arrows. No open/closed circles are present. The positive asymptote at T and midpoint at T/2 are the only marked x-values. There is no y-intercept. The x-intercept lies in (0,T), satisfying cot(Bx)=-D; it is visually shown but is unmarked and not assessed.

Native source fits independently locate each black axis and grey guide and test every sampled blue branch point against cot(pi*(x-x0)/(xT-x0))+D, with that image's own x/y scale. Fit uses perpendicular pixel distance so steep tails do not produce false vertical residual failures. The maximum allowed source stroke/illustrative-raster distance is 4px; actual maxima are below 2.62px. Exact ticks were read visually, not inferred from an image hash or worked answer. Source hashes and full fit data are in source-geometry.json.

| Source | Native size | T | T/2 | D | Perpendicular residual max |
|---|---|---|---|---|---|
| e-3663 | [353, 298] | 1/2 pi | 1/4 pi | -1 | 0.854 px |
| q-65549 | [353, 298] | 1/5 pi | 1/10 pi | 3/2 | 2.617 px |
| q-79188 | [353, 298] | 1/3 pi | 1/6 pi | 3 | 1.413 px |
| q-117798 | [353, 298] | 2/3 pi | 1/3 pi | 2 | 1.049 px |
| q-117800 | [353, 298] | 2/5 pi | 1/5 pi | 5/4 | 0.644 px |
| q-143665 | [354, 298] | 2/3 pi | 1/3 pi | -5 | 0.675 px |
| q-143666 | [355, 298] | 4/5 pi | 2/5 pi | 9/4 | 0.964 px |
| q-143668 | [367, 298] | 5/3 pi | 5/6 pi | -12/5 | 1.091 px |
| q-117799 | [353, 298] | 4/3 pi | 2/3 pi | -3 | 0.743 px |
| q-141999 | [353, 298] | 1/2 pi | 1/4 pi | 1 | 0.468 px |
| q-142000 | [353, 298] | 1/3 pi | 1/6 pi | 1 | 1.076 px |
| q-143669 | [353, 298] | 1/4 pi | 1/8 pi | -9/4 | 0.737 px |
| q-65550 | [355, 298] | 4/5 pi | 2/5 pi | -3 | 0.657 px |

## 2. Shared plot pattern

The graph gives the two inputs required by this KP: the horizontal period and the midpoint vertical level. Extract B=pi/T from the visible asymptote label and D from the visible horizontal-guide label. Both positive and negative shifts preserve a strictly decreasing branch. Bounds change to show both y=0 and y=D with at least three units of vertical context on each relevant side. The source's actual geometry, not incidental raster aspect ratio, is the fidelity criterion.

## 3. Components

- Axes: horizontal y=0 and vertical x=0, black strokes with directional axis arrowheads and x/y labels.
- Cotangent branch: y=cot(Bx)+D, x in (0,T), blue solid stroke; clipped unbounded tails, no finite endpoints.
- Asymptote: dashed vertical x=T across the viewport; x=0 is the black y-axis.
- Midpoint guides: horizontal segment from (0,D) to (T/2,D), vertical segment from (T/2,0) to (T/2,D).
- Tick marks: x=T/2, x=T on horizontal axis, y=D on vertical axis. Exact reduced pi/rational labels, signed y label.
- Labels: x tick text is above the x-axis when D<0, below when D>0, preventing it from colliding with the branch. It is offset to the right of guides, keeping dashed features visible. D is left of the y-axis. No text background/masks hide features.

## 4. Reusable rendering specification

render_plots(instance, output_dir) delegates only rendering to private render.py. Every coordinate and tick label comes from the same exact instance. T=pi/B, M=T/2; branch endpoints solve y=ymax,ymin, then 1800 points sample the intervening curve. Output is a 720x576 Matplotlib PNG. The primary renderer currently uses Python 3.13.5 and Matplotlib 3.11.2; the existing read-only Python 3.10/cached-wheel fallback remains available. No package install. Sidecars contain actual Python/Matplotlib versions, dependency paths, axis pixel bounds, limits, label glyphs/bounding boxes, transformed curve samples, true intercept/monotonicity/endpoint metadata and PNG SHA256.

Actual render canvas text boxes are measured. Every label must remain inside the PNG, every pair of labels must be disjoint, and every label must be more than 3 pixels from the blue curve. The generated PNG is independently decoded to locate its blue stroke and test graph-derived coordinates under the actual axes transform with a 3px antialias/stroke allowance. Native source diagrams and changed-parameter/default plots were visually checked individually or through labeled review records; native examples and extrema were additionally opened at full resolution.

Unique input and output temporary names make concurrent calls safe. Final PNG and sidecar replacements are atomic, and cache hits require both files. Validation exercises fresh simultaneous identical and different geometry calls in concurrent-plots; each sidecar's instance and identical-geometry PNG hashes must match. No image cache pruning occurs.

Original source replay retains the exact frozen image reference when complete source geometry matches; independently generated corresponding PNGs are still produced and checked. Changed parameters generate new plots. Markdown previews rebase source image paths to /media/jake/SSD/EDB/math for readable local viewing while raw JSON prompt text stays exact.
