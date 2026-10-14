# Plot extraction and reusable specification

##1. Specific observed plots

All25 answer plots and all15 hard solution plots were viewed at original360×304 resolution, compositing alpha on white without scaling. Private q-ID.png sheets place each complete answer bank in captured choice order. q-ID-solution.png sheets retain the three solution stages. Canonical e-9466-solution.png was also inspected.

Disk bank axes are centered, with black arrowed x/y axes, blue boundaries, pale-blue interiors, radius labels on both axes. Solid means included and dashed means excluded. Hollow origin markers indicate removed origin; removed diameter endpoints are hollow when lying on an otherwise included circular boundary. Source q-122518 choices0 and2 have the same excluded diameter and therefore the same domain despite the extra origin marker in choice0. q-122677 options include upper/lower halfdisks and full disks; the correct boundary is solid arc, dashed diameter and hollow arc-diameter endpoints. q-122554 correct disk excludes both the outer circle and the y=x diameter. q-122671 correct disk includes outer circle but excludes origin.

Rectangle source layouts use their own scale, so coordinates were read from each plot's own axis positions and labels, never inherited from another plot. q-122710 choice0 is the closed upper-half rectangle; choice1 has x-open sides, included lower y=0 edge and excluded upper y=1 edge;2 is closed full rectangle;3 is the full rectangle with x-closed/y-open edges;4 is correct x-open/y-closed full rectangle. Source choice0 uses a wider drawing than the remaining rectangles; coordinate labels identify its ±1 sides, not a new numerical halfwidth. Endpoint circles in the mixed-boundary correct plot indicate all four corners excluded. Source solution strips show x-open vertical strip and y-closed horizontal strip. The denominator/log graph component plots are unbounded-plane/halfplane pictures cropped by the viewport; the frame is not an assessed boundary.

##2. Generalized pattern

Each hard instance plots two component domains and their intersection; the five answer choices use the complete source-shaped geometric bank, with one documented method-bank repair. The task assesses topology/inequality boundary inclusion and intersection, not parameterization or traversal.

##3. Components and parameter links

Shared background is white with equal-aspect coordinate axes and arrowheads. A disk has exact squared radius r2, closure bit, optional origin puncture, optional diagonal y=m x removal, or upper/lower halfplane selection. Radius labels derive from exact sqrt(r2). A halfdisk line intersects the circle at (±r/sqrt(1+m²),±mr/sqrt(1+m²)); excluded endpoints are marked hollow. Rectangles have halfwidth a, halfheight b, independent x/y closure, an independently included lower edge for choice1, and optional lower y bound0. Component strip dimensions and final rectangle dimensions use the same a/b. All graph-bank profiles and their exact source paths are mapped in template-extraction.md.

##4. Reusable rendering specification

render_graph takes one complete immutable geometry object; Matplotlib generates PNG only. Domain predicates compute the fill; plotted boundaries/markers independently describe inclusion. Equal axes, radius-dependent limits1.65r (at least2), source-sized3.6×3.04in canvas at150dpi, readable signed exact labels, no clipping. Complete source images are reused only at their exact historical parameter anchors. Parameter-dependent variants render every answer and solution plot. Each content-addressed PNG has a geometry/constraint/render-version/hash sidecar. Unique temporary PNG and JSON paths are atomically renamed; cache hits require both. No shared render-input file, no SVG output, no image model. Boundary and endpoint styles are visible in the review. Plot task fingerprints include radius, line/point exclusion, halfplane side or rectangle closures; they omit plot filenames and ordering.

The historical banks have no unlabelled endpoint-coordinate uncertainty relevant to these categorical domains. Fine stroke widths and incidental axis lengths differ between the sources and recreated plots and do not determine set membership. Graphical fidelity means full source-anchor image paths and inspected geometric operations; Matplotlib variants are not claimed pixel-identical source reproductions.

Final geometry regression: q-122710 choice1 preserves the included y=0 edge and excluded y=b edge under changed widths/heights. Original raster was rechecked at full resolution; its bottom blue stroke is solid, top and sides dashed. Renderer and independent displayed-bank predicates encode lower-edge inclusion separately.

Parent version4 corrects source choice3 from incorrectly open-in-both-directions to x-closed/y-open. Both lower-edge inclusion and vertical-side closure have independent transcription mutation regressions; source paths remain byte-exact and older assets remain intact.
