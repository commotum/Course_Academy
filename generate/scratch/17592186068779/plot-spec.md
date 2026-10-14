# Plot extraction and rendering

## 1. Native observations

All answer plots are 360×304 or361×304 transparent PNGs. They show black arrowed x/y axes at true zero, no general grid, a thin blue reciprocal curve split at a vertical asymptote, two blue circular marked points with black coordinate labels, and grey dashed nonzero asymptotes. Asymptotes on zero coincide with black axes. Scale and origin differ between options; equal native dimensions do not imply equal axes calibration. For example q-113466's first plot uses x units≈28.1px while its second/third use≈37.5px. Each source was composited on white and inspected at full resolution in the ten q-N contact sheets; every distinct solution image was inspected in solutions-0/8/16.png.

## 2. Shared visual pattern

The mathematical information is asymptote position, branch signs relative to the horizontal asymptote, and two labelled points determining the scale inside the reciprocal family. Styling is incidental. Different graphs require their own parameter-dependent geometry; a correct graph cannot be reused for a distractor with different parameters.

## 3. Per-image components

plot-extraction.json records all58 unique answer/solution/canonical assets, original file hash, dimensions, black-axis origin, separately fitted x/y scales, visible bounds, ordered marked points, independently detected PNG marker centers, vertical one-sided limits and branch signs. build_evidence.py rereads source PNG pixels: the dense marker centers determine a calibration with the visible labelled point data, then it checks origin agreement and every blue curve pixel against the implicit reciprocal relation using shortest-normal pixel residual. Maximum95th percentile residual is2.095px. This is a bounded antialias/stroke allowance, not a claim that source geometry is exact at subpixels.

The inconsistent fifth q-113372 plot is explicitly flagged. Its negative/positive branches and x=-3 asymptote distinguish it from every other source option without claiming an exact recovered coefficient. A y=4/(x+3) model fits under a chosen y scale but is only a model; the displayed y labels do not match it. Its negative/positive marker ordering, printed labels, and uncertainty are retained separately.

## 4. Reusable specification

render_plot derives bounds from all meaningful feature coordinates, always including zero and the nonzero asymptote. It draws a new Matplotlib Figure for each call, true-zero black axes and arrows, signed integer tick labels, grey dashed nonzero asymptotes, and blue points at the profile's defined distances. Coordinate labels use exact fractions. Two independent densely sampled branches are masked outside bounds with NaN; no curve segment can cross the asymptote. Points lie at least one unit from the bounds. The output is480×400 at100dpi, with10pt coordinate/tick fonts, providing more native legibility than the captured plots.

Rendering uses Matplotlib3.11.2 under Python3.13.5, not SVG or image generation. Content-addressed filenames depend on geometry, labels and renderer version; sidecars record the exact parameters, bounds, points and runtime. Cache hits require both PNG and sidecar. Each render writes unique mkstemp files and atomically replaces the immutable final PNG/sidecar, avoiding shared global input files and Figures. Four same/different concurrent calls are verified against actual pixel geometry.

Generated PNG checks independently transform coordinates using the fixed figure axes rectangle, locate actual blue markers, check all blue curve pixels, and check the black axes are at true zero. Actual native images were visually checked for easy horizontal/vertical, moderate negative fractional vertical shifts, and hard fractional horizontal shifts, including signed tick labels and coordinate fraction legibility. Source graphical equivalence and formula uncertainty are reported separately from native radio-ID grading.
