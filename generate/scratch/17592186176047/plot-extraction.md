# Plot extraction and unchanged-asset specification

## 1. Specific originals inspected

All three actual PNG rasters were opened at native resolution using `view_image`:

- `images/88/88378ece5b1721cdc533d07d69c004901539c7f8fda9a5a3e5c5648ed32905c5.png`: 360×304. White background; blue unit cosine; black axes with positive-direction arrowheads; horizontal labels from −2π to 2π in π/2 increments; vertical labels −1 and 1. A maximum at (0,1), minima at (±π,−1), zeros at ±π/2 and ±3π/2, and peaks at ±2π are visible. Curve continues beyond the outer labels. No restricted interval/endpoints is asserted.
- `images/9c/9c77bec4ebb04668fbff5176418ed9c09143a8660879fdf523a158c5f109006c.png`: 361×304. Same cosine geometry, ticks/labels/arrowheads. Dotted horizontal guides at y=−1 and y=1 emphasize extrema. Used in q-27009.
- `images/96/96bd60d23237f836b77a26c5c0461a5c2a474554f0a14266b53fc5e7d999f1b7.png`: 431×364. White background; blue unit sine through the origin; extrema at π/2 and −π/2; axis ticks −2π to 2π; vertical labels ±1; positive-direction axis arrowheads. This establishes that q-167631’s raster is sine, not an unseen cosine-graph normalization.

These describe actual raster geometry, not conclusions guessed from filenames or copied Markdown image hashes.

## 2. Shared instructional role

The solution recalls a fixed trigonometric graph before checking range, output, intercept, zero and extrema claims. Images are explanatory; no source answer is an image. General-family statements are about the entire real domain, not only the drawn window.

## 3. Components

Fixed objects: untransformed unit curve; origin-centered axes; angle labels at π/2 increments; output labels ±1; directional axis arrows; blue curve and white background. Conditional component: dotted extrema guides in q-27009. Function selection: sine only for explicitly raw mislink replay, cosine for all normal output. No parameters vary curve amplitudes, phase, argument scale, domain restrictions or assessed grid increments.

## 4. Reusable specification and verification

The mathematically meaningful geometry is unchanged when statement parameters vary. Therefore **unchanged assets may be reused**, and the doc-3 plot rating is **none** (no newly generated plots required). No Matplotlib/TikZ renderer is necessary, and no direct SVG or image model is used. The raw replay profiles preserve exact original image references for full source worked-solution fidelity. Copies with SHA-256 provenance are supplied under `assets/` for local normal/review rendering. Normal q-167631 replaces the sine image with the standard cosine image. Changed local claims never point outside the visible familiar-angle bounds; general-family corrections use the plotted repeating structure plus the preceding Introduction.

`plot-provenance.json` records source hashes, dimensions, copied paths and inspected geometry. No extracted curve approximation is passed into a changed-parameter generator, so there is no unverified coordinate scale, arrow reconstruction or inferred fractional endpoint. Asset identity checks in `validate.py` detect missing or altered files. The generated review uses the inspected rasters; original fidelity and supported cosine repair are counted separately.
