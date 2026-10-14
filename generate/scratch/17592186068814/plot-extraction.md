# Plot extraction

## 1. Specific original plots

All 45 original practice option occurrences, representing 31 unique native PNGs, were viewed on white at 360×304 pixels in source-native-0.png through source-native-8.png. Every option has two blue reciprocal branches, a black horizontal x-axis and vertical y-axis with positive arrowheads, no tick grid, two blue marked points with explicit coordinate labels, and axis titles x,y. Opposite points have x=±1. Some plots use decimal ordinate labels (1.5, 2.5, 1.25, 0.75, 0.8, 0.4, 0.25, 0.5); others use stacked fractions. The 0.33 label is genuinely rounded/uncertain and is preserved as the displayed 33/100 raw coefficient rather than asserted to be exact 1/3.

## 2. Shared visual method

Each image encodes y=c/x. Sign is read from quadrants; magnitude is read from each marked coordinate pair and its own axes scale. A correct negative target has quadrants II and IV. The base and stretched graphs are each shown in ordered solution slots. No image alone is reused for changed c unless complete geometry and labels match.

## 3. Components and calibration

plot-spec.json maps every source raster independently. Native origin is approximately (169,162.5) pixels. Horizontal scale differs between images (19–56 px/unit), as does vertical scale; marker centers determine each image’s scale after coordinate-label transcription. Both left and right markers are checked, not a single silhouette. Source-raster-validation.json reports curve product residuals, sign quadrant tests and SHA256. A 15% median relative product tolerance accommodates one-pixel uncertainty on contracted curves whose marked ordinate lies only 5.75 pixels from the axis (asset34); most plots are below 6%. This raster tolerance does not permit changes to transcribed exact coefficients or point labels.

## 4. Renderer specification

Matplotlib Agg Figure/Canvas, 360×304 RGB white, solid blue curves, separately sampled negative and positive x branches, arrowed black axes, two filled markers and exact coordinate annotations. For easy/moderate, marks x=±1; authored hard x=±2. All y-coordinates derive from c/x. Bounds derive from mark magnitude and |c|/mark, preserving visible branch segments and coordinate clearance. Fraction typography remains exact for generated assets. Coordinate labels are placed away from their branch; label and axis-title boxes must fit native bounds and contain actual dark raster ink. Every supported parameter input is rendered and checked at native pixels: both branches at marks and nonunit probes, marker density, title/annotation ink, and axis clearance. All ten bank pairs are unequal under the requested full graph criterion. Parameter-dependent scale changes are communicated by coordinate labels.

Renderer cache requires both PNG and JSON sidecar. Local lock serializes Matplotlib calls, while unique temporary files and atomic replacement protect final assets. Fresh concurrent identical and distinct coefficient renders are verified. No direct SVG or image model. Sidecars record exact coefficients, marks, point coordinates, branch geometry, bounding boxes and actual runtime versions.
