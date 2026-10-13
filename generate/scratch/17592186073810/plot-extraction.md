# Coordinate sketch specification

The six solution sketches were visually inspected in source-plots.png (canonical plus five complete practices). Each contains white background, gray square coordinate grid, black x/y axes, blue vertical or horizontal infinite line labeled with its equation, red given point labeled with its coordinates, blue foot of the perpendicular on the line, black dashed shortest-distance segment, and a brace labeling the distance in units. Source asset references and roles are retained exactly in source.json. All sketches belong to the worked solution, never the prompt or answers. They visually explain why one coordinate difference suffices; new parameter values require a new sketch, rating moderate.

q-74034: horizontal y=2, red (5,-1), blue (5,2), vertical 3-unit dashed distance.
q-114323: vertical x=2, red (4,3), blue (2,3), horizontal 2-unit distance.
q-74202: vertical x=4, red (-1,-4), blue (4,-4), horizontal 5-unit distance.
q-74206: horizontal y=5, red (2,-3), blue (2,5), vertical 8-unit distance.
q-74207: horizontal y=-2, red (-3,3), blue (-3,-2), vertical 5-unit distance.
Canonical e-12548: vertical x=5, point (3,2), foot (5,2), 2 units; reused solely as evidence.

New sketches use Matplotlib with equal coordinate aspect, grid, black axes, blue line/foot, red point, dashed connection, coordinate/equation labels and distance label beside the segment. Bounds include the origin, point and foot with 3k padding. Their data all come from the same exact integer instance; no renderer resampling. The brace is simplified to a direct distance label, axis arrows and sparse original ticks are normalized; these are disclosed visual-fidelity changes, preserving geometry and meaning. Exact source images are reused unchanged at k=1. Assets are SHA-256 addressed, with sidecar geometry/bounds for validation. No mathematical raster is used as an answer value.
