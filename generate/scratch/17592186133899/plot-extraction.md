# Plot extraction and reusable specification

Database `math`, basis1356, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. Source/topic/lesson wrappers copied without changes. Canonical example e-9557 is contextual evidence, not a practice question.

## 1. Individual inspection

All21 original practice rasters were independently viewed at original resolution, composited on white for inspection under `/tmp/33999-source`. Originals remain unchanged and are linked from the frozen record. White inspection makes early transparent C1 labels visible. Axis arrows indicate coordinate axes; problem boundary curves have no traversal arrows.

| Source | Outer | Hole shape, placement and labels | Positive-solution boundary colors |
|---|---|---|---|
| q-126558 | circle C1 | C2 circular NE; C3 circular SW; both tangent to coordinate axes; radius one quarter outer radius | missing solution in source; authored all-orange completion |
| q-126654 | circle C1 | C2 circular E; C3 circular W; centers on horizontal axis, radius one quarter outer radius | C1: orange (already positive), C2: pink (reversed), C3: pink (reversed) |
| q-126862 | circle C1 | C2 square W; C3 square E; centers on horizontal axis, side one half outer radius | C1: orange (already positive), C2: orange (already positive), C3: orange (already positive) |
| q-126863 | circle C1 | C2 circular NW; C3 circular SE; both tangent to coordinate axes; radius one quarter outer radius | C1: orange (already positive), C2: orange (already positive), C3: orange (already positive) |
| q-126865 | square C1 | C2 square S; C3 square N; centered on vertical axis, side one quarter outer side | C1: orange (already positive), C2: orange (already positive), C3: pink (reversed) |
| q-126867 | circle C1 | C2 circular NE; C3 circular SW; larger tangent holes with radius one third outer radius | C1: pink (reversed), C2: pink (reversed), C3: pink (reversed) |
| q-126870 | circle C1 | C2 square NW, its bottom edge on horizontal axis; C3 square SE, its top edge on horizontal axis | C1: pink (reversed), C2: orange (already positive), C3: pink (reversed) |
| q-126868 | circle C1 | C2 square SW, its right edge on vertical axis; C3 square NE, its left edge on vertical axis | C1: pink (reversed), C2: orange (already positive), C3: orange (already positive) |
| q-126864 | square C1 | C2 circular W; C3 circular E; centers on horizontal axis, diameters one quarter outer side | C1: orange (already positive), C2: pink (reversed), C3: orange (already positive) |
| q-126855 | square C1 | C2 square W; C3 square E; centers on horizontal axis, side one quarter outer side | C1: orange (already positive), C2: orange (already positive), C3: orange (already positive) |
| q-126861 | circle C1 | C2 square SW, its top edge on horizontal axis; C3 square NE, its bottom edge on horizontal axis | C1: orange (already positive), C2: orange (already positive), C3: orange (already positive) |

## 2. Shared visual purpose

A light-blue planar region lies inside C1 and outside two white holes C2/C3. The position and curve labels identify the three boundary components. Every supplied circulation is textual; no circulation scalar is embedded in the figure. A positive-orientation solution figure uses outer CCW and both holes CW, regardless of stated question orientations. Pink boundaries show traversals that must reverse relative to the question; orange means already positive.

## 3. Components

White/transparent background; black x/y axes with arrowheads and italic labels; orange outer and hole edges in problem; D inside the shaded region; C1 adjacent to the outer top/right edge; C2/C3 adjacent to their individual holes. Solution adds small black directional arrows to each boundary, and selectively recolors reversed curves pink. Region shading and holes remain identical. Source labels and hole placements are retained individually; no generic replacement diagram is used for modern families.

## 4. Reusable specification

Circulation values vary while geometry, traversal statements and orientation corrections remain fixed for a selected family/diagram, so all21 source assets are reused unchanged. Parameter values never appear in these rasters. Hard adds no geometry demand and reuses each corresponding solution’s source color cue. Only the missing legacy solution is newly rendered in Matplotlib: circular C1 radius1 centered at origin; circular C2 radius1/4 centered(1/4,1/4); circular C3 radius1/4 centered(−1/4,−1/4). Axes, labels, region shading and tangencies match the inspected original. It adds outer CCW/inner CW arrows and keeps all three edges orange. No SVG creation or image model is used.

Rendered `plots/legacy-positive.png` was viewed at original resolution: C1, C2, C3, D and axis labels are visible; each arrow direction follows positive traversal; hole tangencies and placements match the source. Sidecar records exact recipe and actual Matplotlib version. Writes use unique temporary files and atomic replacement; a cache hit requires PNG and JSON sidecar. No geometry-changing variants are supported, hence no parameter-dependent rendering is needed.
