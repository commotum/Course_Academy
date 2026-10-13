# Plot extraction: four stages

## 1. Actual source plots

All nine actual PNGs (canonical plus eight practice) were viewed at **original resolution**, each 360×304. Every one has white background, black x/y coordinate axes with arrows toward positive x and positive y, lowercase x/y axis labels, a blue increasing exponential, and a black dashed horizontal asymptote labeled `y=c`. There are NO plotted curve arrows, NO endpoint dots, NO marked/coordinate-labeled intercepts, and NO grid or tick marks. The curve's finite screen endpoints are clipping/window boundaries, not mathematical endpoints. Each left tail approaches the dashed line from above, and each y-intercept is one unit above it. Asymptote labels are exact source evidence. Pixel curve shape and unmarked intercept scale do not independently establish additional exact coordinates.

| Source | base supplied in prompt | exact dashed label | axis crossing relative to asymptote |
|---|---:|---:|---|
| e-1220 | 3 | 2 | asymptote above x-axis |
| q-26807 | 17 | -4 | below |
| q-7228 | 2 | 1 | above |
| q-170593 | 13/6 | -3/2 | below |
| q-26804 | 25 | 10 | above |
| q-99774 | 7 | -5 | below |
| q-99775 | 12 | -3 | below |
| q-7230 | 3 | -2 | below |
| q-7232 | 2 | -3 | below |

No fractional endpoint uncertainty affects the assessed datum: -3/2 is explicitly printed. Original unmarked intercept positions are illustrative; no claim of recovering a hidden per-pixel exact unit scale is made. In particular, the large-base/positive-shift source uses a different visible axis origin/vertical window. Replays retain actual originals; changed-parameter diagrams use exact y=b^x+c rather than assuming identical original raster coordinates.

## 2. Shared pattern

Graph-reading of a supplied-base exponential and its horizontal limiting value. Label position/color are incidental; relation of curve to dashed line and sign/coordinate level are essential. New plots are necessary when c changes. Heavy rating: plots carry the assessment in every question, even though construction is simple.

## 3. Components

Source asset inventory (`plot-source-inventory.json`) lists every image path, dimensions and SHA256. Prompt placement precedes the question prose; there are no answer-choice or solution plots. Black axes, positive-axis arrowheads, blue growth curve, exact dashed y=c, no curve endpoint/arrow marker. In authored hard, a light horizontal calibration grid and labeled alternate signed fractional ticks are the only added instructional data; c itself is not labeled. The full hard axis increment is mathematical task data, not cosmetic scaling.

## 4. Reusable specification

Matplotlib, white 756×588 PNG (5.4×4.2 inches, 140 dpi). Bound y by min(-2,c-2) and max(3,c+4); x spans -4 through max(1.5, log_b(ymax-c)). This makes origin, asymptote and intercept visible for all permitted signed levels. Plot exactly b^x+c at 1200 abscissae; truncate upward just inside the plot window. Axes are black 1.4pt, curve blue 1.8pt, asymptote black dashed 1pt. Source-like easy/moderate label y=c at the right of the line. Hard grid spacing equals its exact rational step; alternate signed tick values are labeled, with the c label suppressed universally. Both axes have positive-direction arrows; no endpoints/curve arrows/intercept dots are added.

Cache key includes complete exact geometry, renderer specification and generator version. Cache requires PNG AND sidecar. Each call uses unique temporary input; final PNG and sidecar writes use independent unique temporaries and atomic replace. Actual Python, NumPy and Matplotlib versions/dependency cache paths are saved. Validation checks exact geometry under the final axes transform and actual label/tick values, plus original-resolution visual review. Fresh identical/different concurrent renders are exercised in a private unique directory, with no cache pruning.
