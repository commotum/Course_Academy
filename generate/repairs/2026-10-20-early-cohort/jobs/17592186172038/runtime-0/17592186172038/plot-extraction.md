# Plot extraction and specification

## 1. Individual source sets

All 35 choice assets are mapped one-to-one in source-raster.json, including original paths and independently measured local line orientations. Source-cases.json supplies each point triple. The seven white-composited contact sheets preserve visible labels, arrows, scale and negative-coordinate placement. q-49811 choices0/2/3 contain a vertical segment at (1,2); q-49811 option1 is horizontal there. q-80499's correct image has slightly different original bounds from its distractors; bounds are normalized across a generated instance without changing its point/slope content. q-80497's source worked plot has another asset path than its correct choice, but the same three point/slope pairs. All available source solution plots were inspected through the identical choice geometry; the canonical example plot was separately opened.

## 2. Shared representation

A Cartesian diagram evaluates `dy/dx` by the direction of three short centered line segments, with black dots marking the assessed locations. Segment length is incidental; its slope and center are exact. There are no traversal arrows on the segments. Axis arrowheads and unit grids communicate the coordinate system. Half-coordinate point labels are included in generated hard plots so their exact substituted inputs are readable.

## 3. Components

Fixed: white background, pale grid, dark axes through origin with positive arrowheads, x/y axis labels, unit tick labels, black centers, same segment lengths across all choices. Variable: exact integer/half point centers, segment slopes for each of the five complete-bank recipes, shared bounds derived from all points plus origin and margin. Vertical recipe values use dx=0. Horizontal values use dy=0. The solution asset is the exact correct-choice geometry. No independent plot sampling occurs.

## 4. Renderer

`render_plots(instance, output_dir)` receives the exact bank/points and returns choice and solution paths. Matplotlib with equal coordinate aspect constructs each plot; centers ±0.4(1,m)/sqrt(1+m²) form its endpoints. Bounds contain every segment and axis label. Cached Python3.10/Matplotlib dependencies are read-only; every PNG sidecar records actual version/dependency paths and endpoints. Unique temporary input files and atomic PNG/JSON writes prevent parallel calls mixing instances. Content-hashed filenames deduplicate identical geometries; answer banks are retained in content identity, while canonical mathematical-task fingerprints exclude bank and plot styling.

Independent source raster measurements estimate angles rather than claiming exact recoverability from antialiasing. Their ≤0.06-radian tolerance accommodates pixel strokes/tick interference and supports the rational slope interpretation alongside visual inspection and exact substitution. All 35 recovered orientation triples pass; numerical source/distractor recipes remain explicitly underdetermined.
