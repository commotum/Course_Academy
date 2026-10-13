# Plot extraction and specification

Four practice diagrams were inspected at full raster resolution. All use black horizontal x/vertical y axes, no numeric tick grid, blue assessed curve only, filled endpoints with exact coordinate labels, and blue arrowheads for traversal in increasing y.

q-122579 rises rightwards from the origin to(√2,2), convex upward in the xy plane. q-122574 rises rightwards from(1,1) to(6,√6), concave downward as y=√x. q-122593 traverses leftwards/upwards from(2,1) to(1,2), with three arrows, not the reversed order. q-149727 traverses rightwards/upwards from(0,2) to(2,3). The source diagrams show only the assessed section; no context-curve continuation is inferred. Geometry recipes are verified against both marked endpoints and all arrow directions. The diagrams carry no scale-reading workload.

Private renderer `render_plot.py` uses Matplotlib with 121 samples of the exact printed x(y), equal-coordinate aspect, bounds derived from both endpoints/curve extents and the origin, three increasing-y direction arrows, blue endpoint markers, and exact labels. Plots are rated light and appear for normal instances of those same four families. Reuse of captured original images is allowed only when raw endpoint geometry is unchanged; changed raw endpoint variants receive fresh parameter-dependent plots. No answer/solution plots exist.

Cached Python3.10/Matplotlib wheels are read only; no environment installation occurs. Each PNG has a JSON sidecar containing sampled coordinates, exact curve/bounds, labels, actual Python/Matplotlib versions and dependency paths. Input filenames are unique and PNG/sidecar replacement is atomic. Cache hits require both assets. Render files stay under this KP's `plots/`; no images are pruned during review.

Visual QA inspected generated parabola, reciprocal, square-root and signed-coordinate line instances. Endpoint labels are clear of axis crossings and curve arrows after the adaptive first-label placement. Raw source raster preservation and fresh geometry render checks are separate.
