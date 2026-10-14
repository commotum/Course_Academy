# Four-stage plot extraction

## 1. Individual original plots

source-native-bank.png shows all 15 original answer images at their native 359/360 by 304 pixels; source-native-solutions.png shows the two complete practice solutions and canonical. Every practice answer has four blue circular points at x=0,1,2,3, a thin red infinite straight line clipped at the image boundary, black zero axes with positive-direction arrowheads, italic x,y labels and gray unit lattice. No endpoint circles are placed at the clipping boundary: boundary intersections are line extent, not finite endpoints. Practice solution plots first omit the line, then use the correct answer line. Canonical points are red, a visual difference recorded separately from practice sources.

The axes are not invariant among choices: q-54397 option 4 shifts its horizontal zero axis down; q-71695 uses multiple origins/ranges/grid sizes. Every choice is calibrated independently using long black horizontal and vertical strokes and median gray-grid spacing. Blue connected-component centroids then recover four coordinates. The fitted complete line is checked against every source recipe; red stroke residuals are bounded with antialias allowance. The q-71695 second option has ordinate 1 at x=0, then -1,-3,-5, independently establishing y=-2x+1. source-choice-mapping.json records individual dimensions, origins, x/y spacings, marker pixels/coordinates and red residuals for every original.

## 2. Generalized visual role

A complete bank of Cartesian lines asks whether all four computed coordinates lie on the plotted line. The points and unit scale carry the mathematics; visual styling supports readable identification. Solution plots show the exact same points before/after connecting them.

## 3. Components and dependencies

Fixed: white background, square Cartesian frame, gray grid, black zero axes and positive arrows, x/y labels, blue markers and red line for practice style. Variable: full equation for each choice, its four points, bank-wide bounds, grid increment, and clipping intersections. All five alternatives share bounds/scale within a generated bank; no correct-only plotting hint. Source refs remain unchanged for raw replay only. Mathematical recreation is Matplotlib PNG, never direct SVG or image models.

## 4. Reusable plot specification

Use exact rational line coefficients until rendering. Bounds are [-L,L] on both axes, L=max(6,1+ceiling(largest absolute ordinate from all 20 bank points)); all points are strictly inside. Unit lattice for easy/moderate, half-unit lattice for hard. Require lattice spacing at least five native pixels; reject the entire illegible bank. The current bounded family gives x separation at least seven pixels. Axis arrows/labels are placed at the frame's positive extrema, all native tick labels are visible, and markers are drawn above the red stroke. Native 576x576 output uses equal unit scaling and a 9-point tick font; sparse numbered ticks accompany the finer grid.

For normal plots renderer provenance includes actual Python/SymPy/Matplotlib/NumPy versions, script SHA, exact equation, four inputs/outputs, bounds, increment, pixel transform, PNG SHA and dimensions. Matplotlib receives per-call arguments directly; there is no shared render-input file. Every PNG uses a fresh unique temporary pathname and atomic replace; sidecar writes are independently atomic. A cache hit requires PNG and sidecar. Concurrent tests run four distinct processes on two identical and two different instances, checking identity and reading all output pixel markers. They retain all assets for active parent QA.

Generated pixel QA independently segments blue markers and compares native coordinates to the rendered transform; original QA does not use that transform or original equation metadata to determine calibration. Extreme signed and fractional banks are reviewed in review-bank-*.png. Raster equality is not claimed between source and recreation; geometric/math fidelity is reported separately from literal source-reference fidelity and radio grading.
