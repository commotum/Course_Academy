# Plot extraction/specification (steps 5 and 7)

## 1. Specific plots

All10 original PNGs were composited on white and inspected in `source-plots.png`; original references are retained in source records. q-77065 shows a cubic bend, q-77066 a fractional-power arc from the origin, q-127573 an exponential spiral, q-127585 a symmetric cubic bend with crossing continuations, q-127602 a nested-power bowl, q-77068 a positive-t log/quadratic bend, q-77070 an involute loop, q-77219 a positive-t rational/cubic arc below the x-axis, q-77220 an involute loop with incorrect source geometry/endpoints, and q-77072 a translated cusp-shaped cubic/quadratic arc. Source diagrams have black arrowheaded axes, axis labelsx,y, a red contextual continuation, a blue assessed interval, blue endpoint dots and blue exact parameter labels. They have no tick scales, grids, guides, curve-direction arrows or response plots.

## 2. Shared visual pattern

One planar coordinate diagram accompanies each arc-length calculation, distinguishing the requested interval from the surrounding curve. Endpoint order corresponds to the displayed parameter interval. Numeric coordinates are determined by the curve, not diagram guesswork. Plot rating ismoderate: every variant needs a changed curve/endpoint image, though it does not supply an otherwise missing mathematical value.

## 3. Components

White background; blackx/y axes with arrowheads; equal unit scales by default; independent axis scales for readable reciprocal-cubic diagrams, as recorded in sidecars; red continuation; thick blue assessed curve; blue endpoint dots and exacttlabels. Context ranges respect real-domain constraints (t≥0 for fractional powers,t>0 for log/reciprocal functions). Polynomial continuations include both signs where the source does; involutes include the surrounding loop. Hard families reuse the same layout. Coordinates are computed from the exact question in the primary SymPy runtime; the renderer accepts those coordinate arrays and does not resample anything.

## 4. Reusable renderer and verification

`render_plots` writes a unique temporary JSON input and calls `render.py`, which uses Matplotlib only. The primaryPython3.13environment lacks Matplotlib, so the already-cachedPython3.10/Matplotlib wheels are loaded read-only; no install/network operation occurs. Each asset's JSON sidecar records Python, Matplotlib, resolved dependency paths, exact curve/domain, sampled coordinates, styles and computed bounds. Bounds include curve features and axes with margins. Axis arrows, labels and endpoint offsets are retained; there are no invented traversal arrows. Output names derive from stable content identity. Renderer PNG and sidecar writes use unique temporaries plus atomic replacement. Concurrent identical/different parameter tests pass and leave no temporary inputs.

Generated plots are inspected in `generated-plots.png`. The scalar prompt/answer/worked-solution validation independently reparses printed coordinates and checks endpoint positions against each sidecar. The source's q-77220 geometric inconsistency is repaired by plotting its actual printed curve. Source plots are not reused for changed parameters. No image model, direct SVG generation or shared environment change occurs.
