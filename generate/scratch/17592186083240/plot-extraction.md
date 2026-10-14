# Plot extraction and specification

All seven practice graphics are supplementary prompt illustrations. There are no plotted choices or solutions. The canonical unit-circle image is also inspected context. Source paths are preserved in source.json and public observed replay. Original images were opened from /media/jake/SSD/EDB/math and composited on white into source-plots-inspected.png for visual inspection. No original graph contains a P marker or traversal arrows; the assessed supplied t is textual. Axis arrows label x and y; the blue curve and light grid are shared styling.

## Stage 1: individual source geometry

| Source / family | Original graph geometry and source scale | Verified features |
|---|---|---|
| 17592186290260 / quadratic | Two positive-x branches meeting near (−1/3,−8/9); x grid 5, y grid 5, displayed x roughly −7..38 and y −10..25 | x=3t²−2t has vertical-tangent turning at t=1/3; y=t²−1 has minimum at t=0. Both coordinate sign changes agree with curve. |
| 17592186321110 / expneg_poly | Decreasing positive curve from (4,0), x/y grid 2; chart roughly [0,10]² | t≥0 gives x=4exp(−t) decreasing toward zero while y=t²+6t rises; no arrow or endpoint glyph. |
| 17592186321111 / trig_double | Horizontal ellipse with intercepts (±5,0),(0,±√3), unit grid and ticks spaced 2 | x=5sin(2t), y=√3cos(2t); t∈[0,2π) traverses ellipse twice but image records locus only. |
| 17592186335950 / quartic | Two rightward branches with upper flat turn near (−1,0), leftmost x about −1.47; unit grid | x=t⁴+t−1,y=t³; t=−1 gives (−1,−1), t=0 gives (−1,0). The shallow hook is consistent with x′=4t³+1. |
| 17592186335963 / quintic | Sideways S-shaped curve, crossing y=1 at x=0, signed unit grid | x=t⁵−2t,y=1−t³; t=−1 gives (1,2), t=0 gives (0,1), t=1 gives (−1,0). Local extrema in x are at ±(2/5)^(1/4). |
| 17592186395776 / line_quad | Full upward parabola with vertex (2,0), unit grid; visible arms beyond x=0 and x=4 | x=2(t+1),y=4t² with printed −1≤t<1 actually restricts x to [0,4). Source raster contains extra arms beyond the supplied interval. Normal variants repair this displayed-segment error. |
| 17592186401853 / texp_poly | First-quadrant increasing concave-down locus from (0,0), x ticks 50/100 and y horizontal guide 20 | x=2t exp(t),y=t²+2t,t≥0; t=3 gives (6e³,15), agreeing with visible upper right curve. |

Canonical e-595 shows a unit circle centered at the origin, x/y ±1 tick labels and no P marker or traversal arrow; its formula has x=cos t,y=sin t.

## Stage 2: generalized visual pattern

A blue parameterized curve is drawn against labeled coordinate axes and light grid. Its job is identifying the parametric locus given in the following formula. It is not a reading-scale task. Normal variants have the same locus under positive x/y coordinate scaling. The restricted source segment has inclusion markers added for the repaired interpretation.

## Stage 3: component mapping

The rendered x/y arrays are computed from the same actual expressions used in the question. Sampling windows preserve each source illustration's meaningful features: quadratic t=−3..4; expneg_poly 0..2; trig_double 0..2π; quartic/quintic −1.6..1.6; line_quad −1..1; texp_poly 0..3. Positive r,s scales alter the coordinates and axis ranges, not these parameter windows or turning parameters. Coordinate-scaled plots retain signs and zero sets; labels/ticks come from actual transformed data. For unbounded curves, the illustration is a finite viewing window without an endpoint claim. Ellipse equal axes display geometry; the wide quadratic/exponential graphs use independent axes scales as in their source charts. No unrelated arrows or marked evaluation point is added.

## Stage 4: renderer contract

Matplotlib Agg, 1200 samples, 5×4 inch PNG at 120 dpi. Source curve is dark blue with fine gray grid and x/y axes. Output cache key includes render version, template, exact x/y expressions and parameter window. Unique private temporary PNG and JSON files are atomically renamed; fresh writes and concurrent identical/different parameter instances are checked. Source replay keeps exact original assets; normal generation regenerates each changed pair. PNG sidecars record exact expressions, parameter window, sample count and actual runtime versions. Outputs and sidecars remain under this KP folder. No direct SVG or image models.
