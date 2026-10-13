# Plot extraction and specification

## 1. Specific originals

Every original, including e-6150, is a 360 × 304 coordinate diagram with black
ungraduated axes, arrowheads pointing right/up, black x/y labels, a thin red
circle and small red marks at C and X. C and X labels contain exact ordered
coordinates. No radius segment, diameter, grid or tick marks is drawn. The
circle position and scale differ by source. q-117096 places X on the x-axis;
q-117099 places X on the y-axis; e-6150 places C on the x-axis. These are
meaningful label/axis coincidences, not permission to infer a new skill.

All eight originals were inspected at full resolution. `original-geometry.json`
fits each image's own red-circle bounds and black-axis origin and verifies C
and X against the recovered coordinates; center discrepancy is below 1.18
pixels, within the 2-pixel stroke/antialias allowance. Both marked coordinates
have red pixels in a 4-pixel window. Coordinates in labels were visually checked.
The exact asset hashes remain attached to public source replay.

## 2. General visual pattern

Illustrate the circle determined by center C and on-circle X on an equal-scale
Cartesian plane. The question assesses distance computation and equation
construction; coordinates are given explicitly, so diagram scale-reading is
not assessed.

## 3. Components and dependencies

The circle is centered at (h,k), with r = √((u−h)²+(v−k)²). C is marked at
(h,k), X at (u,v). Black axes cross at (0,0), with right/up arrows. Both labels
are computed from these exact coordinates; only plotting uses numeric values.
White background, red curve and dots, black labels and no ticks are fixed.
Source assets occur only in the prompt; no plotted choices or solution images
exist. Thus bank recipes change equations rather than drawing choice circles.

## 4. Reusable renderer

`render_plots` returns the prompt reference and geometry/provenance sidecar.
Source replay reuses its original raster only when all four coordinates match
the same source; every changed instance renders through Matplotlib. Bounds
include the full circle and the origin, padded by max(0.9, 0.26r). Equal aspect
keeps circles circular. C prefers offsets and alignment away from the axes;
its complete measured text box must stay inside the circle without covering
the center mark. Centered text alignment is available for smaller circles.
X prefers the source's
radial outward placement. Its actual Matplotlib text box is measured against
both coordinate axes, the circle boundary and the center mark; other quadrants
and bounded offsets are tried only if needed for a clear label. An interior
label is allowed when its complete box stays inside the circle and clear of C
and its label. The two coordinate labels cannot overlap.
This avoids both long labels crossing axes and short labels crossing a nearby
arc. The selected text box, transforms and clearance checks are recorded and
independently rechecked by the validator.
Axis labels are offset at the arrow tips. Radius is not a displayed given.

Renderer dependency versions and paths, dimensions, bounds, scale, coordinates,
labels, sampling count, PNG hash and roles are recorded with each generated
record. The renderer uses actual installed Matplotlib when available and a
read-only cached Python 3.10 dependency fallback otherwise; nothing is installed
by this KP. Generator metadata records the actual Python version independently.

All render-input files are unique. PNG and JSON sidecars are atomic writes;
cache hits require both files and matching coordinates. Fresh concurrent calls
for identical and different geometries are validated. Assets are retained during
parent QA. The plot rating stays **moderate** because a changed diagram appears
in every instance. No direct SVG or image models are used.
