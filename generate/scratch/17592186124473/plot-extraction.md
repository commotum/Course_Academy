# Plot extraction and analytic specification

## 1. Original plots

All original PNG files are copied beside this document using source ID and prompt/solution role. `asset-manifest.json` records exact dimensions and SHA-256 hashes. Source plots are blue on white with grey grids and black axes; q-36061 uses labeled coordinate tuples instead of a grid. Solution composites restrict curves, mark requested endpoints, and draw black dashed horizontal witnesses. No plotted answer choices occur.

q-36039: origin (0,0), unit grid; left line [-4,-2) from ordinate 1 to excluded 3, right line [-2,3] from 5 to 0, all other endpoints filled. q-36011 similarly has an excluded (-2,3) and filled (-2,4), followed by filled (3,2); left line continues off the visible window. The different output ranges make a two-piece restriction possibly injective despite reversal of monotonic direction.

q-36941: grid step two; outer pieces meet (-2,2) filled and (2,2) open. Middle endpoints are (-2,-2) open and (2,-2) filled; its maximum is visibly below zero but unlabelled, so its exact ordinate/formula is underidentified. Symmetric outer ranges overlap; negative middle versus positive outer ranges are separated.

q-108667: unit grid, peaks (-3,1) and (3,1), minimum (0,-1); outer descending/increasing strokes continue to clipping boundaries without arrowheads. q-108673: unit grid, local maximum (-2,3), minimum (0,1), increasing left piece includes a flat inflection near (-3,2); clipping, not endpoint circles, indicates continuation. q-36934: unit grid, minimum (-2,1), local maximum (-1,2), decreasing line through (0,1) and (1,0).

q-36002: cusp (0,0), two strictly monotone curved pieces, left output positive and right output positive; tails are clipped without drawn arrow tips. q-36008: same cusp plus peak (1,2), then line through (3,0). q-36004: grid increment two on both axes, x labels every two and y labels every four; filled endpoints at x=-6 and x=10, maximum x=0 and minimum x=4. Extreme ordinates are fractional/unlabelled; surrogate choices of -12.5, -0.5, -11.5 and -5.5 are illustrative landmarks, not recovered exact numbers. The invertibility conclusions depend on turns, not those precise heights.

q-36066: local minimum (0,1), maximum (2,3), right curved segment crosses x-axis between 3 and 4; source restriction I has output ranges [3,4) and (-1,3), which are disjoint because the right component excludes x=2. q-108791: filled endpoints (-3,-4),(5,3), corner (-2,-1), plateau y=1 from x=1 through3. q-108795: filled endpoints (-2,-2),(4,2), initial plateau y=-2 through x=0, then strictly increasing curve. q-36061: filled (-3,3),(1,-1), excluded (4,-1), domain [-3,4), sloping segment passes origin; exact point labels and absence of grid are retained in source ink.

Canonical e-3962: blue line increasing to (0,0), decreasing to (2,-2), then rising curve; requested (-3,-1] monotone, (0,4] and [-2,2) cross turns. Its solution plots use open/closed markers matching those restrictions.

## 2. Shared pattern

The graph, requested input intervals, endpoint membership and output overlap carry the assessment. No analytic formulas, asymptotes or inverse construction are inferred. Source clipping without an arrow is recorded as such; it is not transcribed as a recovered endpoint or invented arrow tip.

## 3. Components

Normal plots have finite shown domain, integer grid, labelled x/y axes, blue straight affine pieces, open/filled endpoint circles, and exact plotted joins. Source profile plots retain original raster ink at original parameters. Changed evidence plots use explicit landmark surrogates and carry honest ineligibility flags. Exact-asset replay proves raster preservation; it does not prove analytic geometry recovery.

## 4. Reusable renderer

`renderer.py` uses Matplotlib Agg in the primary environment when available, with cached read-only Python3.10 dependencies as fallback; no install, SVG or image model. The main generator calls it with its exact instance data, never another sampler. Plot bounds include every finite endpoint with margin and the origin. Curves, joins and endpoint inclusion come from the same branch objects as the exact HLT test. Ticks sit outside the plotting rectangle, preserving readable association with grid coordinates. Text bounding boxes are measured after draw and checked against actual curve paths, endpoint centres, other labels and axis-adjacent placement; no label masks cover graph features. Actual saved PNG center pixels verify filled/hollow circles, and blue pixels verify every curve midpoint. Sidecars record actual Python/Matplotlib versions, dimensions, transforms, text boxes and clearance.

Unique temporary input/PNG/sidecar files and atomic renames prevent concurrent mixing. Cache hits require both PNG and sidecar and include renderer hash. Cached assets are preserved during review.

Actual eligible rendering runtime: Python 3.13.5 and Matplotlib 3.11.2 (recorded in every reviewed sidecar). The independent read-only source-calibration helper uses cached Python 3.10.13/Pillow/numpy.
