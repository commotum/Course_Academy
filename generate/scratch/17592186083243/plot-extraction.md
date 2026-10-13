# Plot extraction and reusable specification

Source snapshot: math, basis 1356. All six referenced original images were opened and visually inspected.

## Stage 1 — original plots

| Question | Reference | Curve / visible features |
|---|---|---|
| q-6730 | images/94/9434dda63c08fc1202d16ab5410fe7061050515876ffa473d8720db39079af3e.png | x=t³+t², y=t². Two branches meeting at origin, one folds near x=0; approximate x range −2..4, y range −1..5. |
| q-348303 | images/59/59f053b9a122018d78cd9c30f5a53cd67cd2ff645d02ccb6d311e6183e081102.png | x=t³+2t², y=t². Two branches at origin; left branch folds around x≈1; approximate x range −2..6, y range −2..5. |
| q-6808 | images/17/1739317bf1b1c567f74dccf5b24a1b1dde8eb101d20ceec9652f604dc6f84543.png | x=4cos t, y=3sin 2t. Two crossing loops; horizontal extent ±4, vertical extent ±3. |
| q-348304 | images/7a/7ae65c873838ede4cce89c953ff2654fa1e58e65fdc87896c8ba85bbf947be20.png | x=6cos t, y=2sin 3t. Multiple crossings; horizontal extent ±6, vertical extent ±2. |
| q-353351 | images/35/35c62ccf48c4d0a49729da04b443cb94d112e673e0c24e7784d22f48eaabf8f7.png | x=3cos t, y=4sin 2t. Two crossing loops; horizontal extent ±3, vertical extent ±4. |
| q-353350 | images/ab/abab926e465522d30b236577bf8a1654502807b864c9fed8a4cebb84efffd3a2.png | x=2sin t, y=3cos t. Ellipse with extents ±2 horizontally, ±3 vertically. |

All are blue solid curves over gray square coordinate grids, black x/y axes through zero, numerical ticks and x/y labels, white background. The originals use arrowheads on the positive axes. No point, parameter value, tangent, direction arrow or slope is marked. There are no choice or solution plots.

## Stage 2 — shared pattern

The prompt plot shows the curve's shape for orientation. The supplied parameter and formulas carry the assessed derivative/evaluation task. A curve with changed coefficients needs a new plot; changing only t₀ can reuse the unchanged curve.

## Stage 3 — components and parameter connections

Curve coordinates come from the same x(t), y(t) and coefficients as the question. Trigonometric curves sample one full [0,2π] traversal for a closed picture, consistent with the half-open parameter interval. Cubics sample both signed branches and crop to a source-like window around the origin/fold. Positive a/b scale the relevant coordinates. Harmonic frequency controls crossing structure. Axes/grid have equal numerical aspect ratio. The image precedes “For the parametric curve”; “shown above” appears only with a completed prompt image.

## Stage 4 — reusable specification and rendering

`render_plots` in the generator reuses copied source images when the entire curve matches an observed original, independently of evaluation t₀. Otherwise it calls `render.py` with that instance's family and exact coefficient parameters. New assets are deterministic `curve-<curve-fingerprint>.png`. Matplotlib uses a blue line, white canvas, gray grid, origin spines, integer ticks, x/y labels and equal aspect. Cubic view bounds contain the exact turning point (4a³/27,4a²b/9), the origin, and negative-root crossing (0,a²b); sample span extends past t=−a and explicitly includes these special parameters; harmonic and ellipse windows add one unit around exact extrema. It intentionally has no tangent or evaluation marker. Positive-axis arrowheads are a minor style difference in generated assets; no mathematical cue depends on them. Cubic figure height grows with the y/x window ratio (capped at 14 inches) so equal-unit aspect does not collapse the horizontal axis and overlap labels at extreme coordinate scales. Tick spacing uses at most about ten visible labels. Images are PNG, never directly generated SVG or image-model output.

Rating: light for the easy bank (two of eight questions plotted), moderate for moderate (all questions plotted), none for hard. Rendered sample images are linked from review.md and referenced in review.json. Dependencies use the existing Python 3.10 Matplotlib cache read-only when the primary Python 3.13 environment lacks Matplotlib; paths and versions are in render-provenance.json. Generated plots and exact source copies remain within this evidence folder.
