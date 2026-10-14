# Plot extraction and specification

## 1. Original plots

All14 raster assets were opened individually at their full native resolution, including all eight prompt plots (seven practice and canonical e-9941) and six reference sketches in every worked solution. There are no graphical answer options; all35 practice options were inspected as text. Prompt root values: canonical−4 below-axis bounce; q1404113 decreasing non-tangent crossing; q140414−2 above-axis bounce; q141133−1 increasing flat crossing; q141137−5 decreasing flat crossing; q1411429 broad increasing flat crossing; q1411446 above-axis bounce; q141140−3 increasing non-tangent crossing. Exact dimensions/hashes appear in read-manifest.json. Source reference table shows both orientations for simple crossings, both above/below bounces for even multiple roots, and both orientations of flattened odd crossings.

Every prompt uses a red curve, black horizontal arrowed x-axis labeled x at the right, one labeled root and a small root tick, white/transparent background, no y-axis and no numeric y-scale. No endpoint is marked as included/excluded; these are cropped parts of graphs, not domain endpoints. Approximate shared prompt intercept raster location is x169,y88.5 for the taller seven practice sketches; individual source-raster checks independently measure the red curve there, both side signs40px away and tangent slope18px across. Canonical has its horizontal axis near the top with the below-axis bounce. Reference sketches have no numeric root label. No exact polynomial equation or higher exponent can be inferred from these unscaled images.

## 2. Shared visual pattern

A local polynomial-root sketch supplies exactly the non-tangency/tangency and crossing/bouncing cue required for qualitative multiplicity classification. Original assets can be reused only at their exact replay anchor. Changed roots/categories/configurations require a new plot. Heavy plot rating: the plotted local behavior is the problem's operative information.

## 3. Components

Fixed: red polynomial curve, true horizontal y=0 axis with right arrow/x label, readable root ticks, white background. Variable: exact root coordinates, local multiplicity class, vertical orientation and two/three-root context. Optional conditional component: target-local panel for moderate/hard. Every panel derives vertices from precisely the same polynomial; independent vertical scales are allowed because no y-value is assessed. Axis transforms, sample vertices, polynomial and PNG hash are recorded in atomic JSON sidecars. Positive vertical amplitude is unsupported and excluded from fingerprints.

## 4. Reusable renderer

Matplotlib only, Agg backend,150dpi; easy7.2×3.1 inches, moderate/hard7.2×5.1 inches. Source simple crossings use a monotonic cubic representative t(1−t²/12) restricted to |t|≤2 so no extra zero is shown. Other single roots use signed t² or t³ representatives. Multi-root curves use the exact product of distinct-root factors with representative orders1/2/3. These exponents create the assessed categories and are never assertions about hidden source exponents. Overview spans the visible roots plus2units at either side. Local view spans target±0.85, well inside the separation≥3 guard. Each panel includes its exact roots as vertices; red vertices are checked against independent evaluation and the actual PNG under the saved axes transform. Zero-line alignment is separately checked. The y-axis is drawn at x=0 only when0 lies in that panel, and roots/zero tick labels use exact signed rational TeX.

Atomic unique temporary PNG/sidecar files support simultaneous identical/different instances. Both cache files must exist; no image cache is pruned while QA may be reading. Matplotlib state is isolated per-process for concurrency verification. Generated easy/moderate/hard and signed/rational target panels were visually inspected; curves/tick labels are legible, arrow/x labels have reserved right-side space, and local panels preserve the original local category while avoiding global-scale flattening.

Fidelity does not claim raster reconstruction of an unknown equation: exact original PNGs are retained/reused at anchors. Changed-source representative plots faithfully preserve root position, orientation and qualitative crossing/bouncing/flatness. Source raster sign/slope checks are independent from generated SymPy checks and native radio grading.
