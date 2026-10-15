# Plot extraction and reuse

Nine source plots were inspected in `reference/source-plots.png`: the canonical
segment (0,0)→(3,3); the incomplete record's counterclockwise long circular arc;
the lower-right ellipse arc; left ellipse half; segment (-1,1)→(2,2); upper ellipse
half; upper-left circular quarter; lower circular half; segment (-2,3)→(0,0).
Each has black coordinate axes and endpoint values, a blue path, directed arrows
and a C label. These features determine path position and orientation; no figure
encodes a scalar-function magnitude.

The generalized plot specification is the source's oriented path with fixed
coordinates, scale, endpoints, arrows and labels. c is a scalar on f only, so
all geometry is invariant. Existing assets are reused unchanged. `assets.json`
records placement, source references, SHA-256 and successful verification against
the content-addressed math store. The new-rendering plot rating is **none**.
