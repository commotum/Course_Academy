# Plot extraction and specification

All nine canonical/practice PNGs were individually viewed at original resolution. Every source picture has an orange solid meaningful boundary, pale blue region, white hole, black Cartesian axes and coordinate labels. No original has boundary-direction arrows. Positive orientation is inferred from ∂D and the lesson convention, not transcribed from nonexistent arrows.

| Record | Independent visible geometry | Boundary details |
|---|---|---|
| e-9097 | circles centered at (0,0), radii 4 and 2 | both circles solid |
| q-126515 | square outer x,y∈[−2,2]; inner x,y∈[−1,1] | all eight segments solid |
| q-126578 | concentric circles radii 2 and 1 | both circles solid |
| q-126853 | outer x∈[−3,3], y∈[−2,2]; inner [−1,1]² | all eight segments solid |
| q-126856 | concentric circles radii 3 and 1 | both circles solid |
| q-126860 | outer [−4,4]²; inner [−3,3]² | all eight segments solid |
| q-126894 | concentric circles radii 3 and 2 | both circles solid |
| q-126891 | outer radius 4; removed **upper** semicircle radius 2 | upper arc and diameter [−2,2] on x-axis solid; lower semicircle dashed gray auxiliary guide, NOT boundary |
| q-126880 | diamond vertices (−3,0),(0,−3),(3,0),(0,3); inner [−1,1]² | diamond has diagonal lengths 6 and 6, area 18; inner square area 4 |

The source tick lettering is offset outside the stroke and occasionally appears slightly inward from the outer extent. Labels and symmetry determine the integer coordinates; no unsupported fractional vertex is inferred. There is no diamond-side-length interpretation: the worked solution correctly uses diagonal-product/2.

Generalization: outer filled disk/polygon, with one or two disjoint white removed regions. Independently varying geometry requires a new plot. No plot choice banks exist. Raw anchor replay references the original immutable paths exactly; changed raw and normal output uses Matplotlib. Normal output adds positive-direction arrows and explicit orientation prose. Circle outer arrows have positive cross product; inner arrows negative. Polygon vertices are counterclockwise; hole traversal is clockwise. The semicircle arrow traverses its arc clockwise and the diameter closes the removed region; lower dashed guide remains visually distinct.

Components: exact integer dimensions, centers, radii, vertices, all boundaries, sign-aware coordinate tick labels, region D, length/radius labels, axes, direction arrows, and guide predicates. Bounds derive from the full outer extent. Equal x/y scale is enforced. For two circles, centers are (−R/2,0),(R/2,0), max(r,t)<R/2 and r+t<R; for two squares, centers (−W/4,0),(W/4,0), max(s,t)<W/2 and each square is strictly inside the rectangle. Unequal holes prevent omission-bank collisions.

Renderer: Matplotlib, SHA-addressed PNGs and JSON sidecars with exact boundaries, arrow tails/tips, actual axes transform, Python/Matplotlib versions and PNG SHA. Final files are atomically written from unique temporary files. Source rasters have no arrows and are not falsely reported as positive-arrow transcriptions. Independent QA reads PNG pixel coordinates back through its real axes transform, checking each polygon segment, several arc points, and the semicircle diameter with bounded antialias/stroke allowance. Arrow orientation is checked against an independent geometric sign test, with a reversed-inner-arrow mutation regression. Manual review of the two hard renderings and representative changed single-hole figures complements this pixel check.
