# Four-stage plot extraction and specification

## 1. Inspect originals

All seven original practice rasters and canonical e-3224 were opened at original resolution. White background, black right/up arrow axes, italic x/y labels, no ticks/grid, red circular outline and red center marker. Center has an explicit C(h,k) label below it; blue dashed radius travels from the center to the rightmost point (horizontal) or topmost point (vertical). A black overbrace/side brace marks the positive radius, printed adjacent to the brace. Every source diagram is 360×304 px and is mathematically to scale in its own coordinate transform.

| Source | Radius orientation | Center (px) | Own axes origin (px) | Pixel/unit |
|---|---|---|---|---|
| q-54187 | right | (169,163) | (134,271) | 36 |
| q-54210 | up | (178,154) | (213,242) | 17.57 |
| q-116929 | right | (169,171) | (226,129) | 14 |
| q-117077 | up | (169,175) | (128,112) | 21 |
| q-117081 | up | (169,163) | (230,163) | 12 |
| q-70896 | right | (157,170) | (132,220) | 25 |
| q-70898 | up | (169,170) | (199,125) | 14.875 |
| canonical e-3224 | right | (157,163) | (193,199) | 36 |

The seven source circle extents, center positions and radius lengths are checked against their individual transforms using a <=3 px allowance for stroke/antialiasing; actual signed center and positive radius labels were read visually. No shared transform is assumed. The source q-167932 contains no image reference, so its original geometry cannot be inspected or recovered; the generated diagram explicitly derives from independently verified solution parameters, with that limitation retained.

## 2. Shared pattern and instructional purpose

Diagram supplies center and radius directly. The assessed operation is constructing a complete circle equation from those labeled inputs, not grid reading, measuring distance or finding a diameter midpoint. Horizontal and vertical presentation variations convey the same radius and must not inflate task counts or difficulty.

## 3. Components and links

One prompt asset; no plots in answer bank or solution. Fixed background/axes/arrow styles, red locus, red dot, dashed blue marked radius, black dimension bracket, exact C-coordinate and radius labels. Variable geometry is `(h+r*cos(t),k+r*sin(t))`, endpoint `(h+r,k)` or `(h,k+r)`. Axes origin stays (0,0), bounds include both the complete circle and origin plus padding `max(1,.28*r)`. Equal aspect is required. Fraction labels retain reduced numerator/denominator and signed center values. Radius label is positive. Center label gets a white background to keep axes/radius from crossing text.

## 4. Reusable plot specification

`render_plots()` uses original hashed assets only at the exact original parameters **and original orientation**. Otherwise the private `render.py` uses Matplotlib with exact inputs serialized to a unique private temporary JSON, converting to floating coordinates only for plotting. Output/cache filenames depend on geometry and orientation. Sidecar includes exact parameters, center, radius, endpoint, bounds, equal aspect, renderer/runtime/dependency versions and cached dependency provenance. Cache hits require both PNG and sidecar. PNG and sidecar are atomically replaced from unique temporary files. No direct SVG, image models, installs, database writes or shared plot inputs.

The primary Python 3.13 virtualenv has no Matplotlib; renderer delegates to pre-existing Python 3.10 and read-only cached wheels as demonstrated in the worker instructions. Nothing is installed or downloaded. Sidecars record actual Matplotlib/NumPy versions and selected dependency paths. The primary generator uses exact SymPy values; its dependencies are recorded separately.

Generated easy/moderate/hard diagrams were visually inspected, including rational coordinate/radius labels, both radius orientations, signed quadrants and circle clipping/aspect. Native PNG extents independently confirm equal-scale red circles. Concurrent fresh render checks cover identical and different parameter sets; outputs retain matching sidecars and stable identity. Assets are preserved for active review, never pruned.
