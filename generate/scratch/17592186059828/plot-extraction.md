# Four-stage plot extraction/specification

## 1. Specific original geometry

All three original PNGs were inspected at original resolution on white. q-28850: 345×29; horizontal black axis at y≈6, unit ticks at x≈25,74,123,172,221,271,320, labels -3,…,3. Red segment has endpoint centers x=123 and x=271. The first center is white/open; second is red/filled. Fitting labelled anchors -3 at pixel 25 and 3 at pixel 320 gives origin 172.5 and 49.1667 pixels/unit, hence endpoints within 0.014 of -1 and 2.

q-31762: 296×29; labels 1,…,6 and similar tick spacing. Its own fit uses 1 at pixel 25 and 6 at pixel 271, giving origin -24.2 and 49.2 pixels/unit. Red-circle centers are x=25 and x=172, both white/open. Endpoints are within 0.013 of 1 and 4. Reusing the first image's origin would be wrong.

Canonical e-10787: 345×29; same -3,…,3 labels as q-28850, with independent fitted labelled anchors. Red centers at x=74 (filled) and x=271 (open) give [-2,2). There are no arrows indicating rays, no arrows on the assessed segment and no extra branches. Axis continuation beyond the segment is incidental.

Exact references are preserved in source.json; source-readback-input.json retains anchor fits. source-geometry.json reports measurements from red pixels, NOT the generator's parameter metadata or image hashes.

## 2. Shared pattern and purpose

One horizontal number line, evenly spaced ticks, finite red segment and one circular marker at each end. Marker fill indicates endpoint membership; endpoint position on the labelled scale gives its value. All this geometry is central, so plot rating is heavy.

## 3. Components

Background white; axis black; ticks black; coordinate labels black below axis; assessed segment red; filled marker red with red outline; open marker white with red outline. Normal templates vary coordinates, orientation, tick increment, label increment and appropriate padding bounds together. Scale labels belong to the actual geometry, not independent sampling. Styling and endpoint padding are incidental.

Source readback detects red marker arcs outside the horizontal shaft, reconstructs center positions and checks their actual center pixel fill. Coordinate fitting is separate for each source's labelled axis. This catches the both-open anomaly independently of the answer banks. Source semantic banks are then verified in full against these extracted coordinates.

## 4. Reusable specification and rendered QA

`geometry` derives bounds as one label increment beyond each endpoint, so signed and half-coordinate variants remain visible. Unit/half-unit ticks are exact rational parameter data, converted to float only at rendering. Labels appear every label increment. Normal right endpoint fill is the opposite of left; raw_q31762 keeps both open. The renderer uses Matplotlib only, with 1120×203 PNGs, 13pt labels and 9pt marker size, ensuring legibility.

Original assets are reused only in exact raw replay. Any changed geometry receives a freshly rendered PNG. Renderer hash and geometry determine asset name; PNG and sidecar must both exist for a cache hit. Each call has a unique temporary input and final PNG/JSON writes use os.replace. No cache pruning occurs. Four fresh concurrent renders check identical and distinct parameter sets and verify no inputs leak from the private temporary directory.

Generated raster readback checks actual endpoint arcs/center fills and black tick coordinates against the axes' pixel fit. Red endpoint circles intentionally cover black tick marks there, so detected black-tick gaps may be integral multiples of the increment. Scale correctness is also checked visually in review variants. Original and generated PNGs were visually inspected; review.json preserves every reviewed path. No SVG authoring or image model is used.

The current audit also inspects images/05/05b54d1b8e401f49861e335fd4736566441017576b30d9b56a6bdfe5e670bffb.png (q-154795) and images/e9/e91f27df78e4d7c05477917f0875add047f24fa2a2aee2ea26d6191023e80165.png (q-31779). Both are thin red segments above labelled unit number lines. The first marks two white circles at -3 and 2; the second marks a filled circle at 2 and a white circle at 4. Fits use independently visible label anchors (-4,4) at pixels (25,418), and (1,6) at pixels (25,271). Raster endpoint errors are below 0.025 coordinate units. All original references remain immutable; generated variants use the existing Matplotlib renderer with complete labels and content-addressed publication during preparation. Plot rating remains heavy.
