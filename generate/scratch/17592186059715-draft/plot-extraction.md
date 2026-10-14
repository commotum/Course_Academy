# Four-stage plot extraction and native inspection

## 1. Every original plot

All five originals were opened individually at full native360×304 pixels. Source PNG hashes and local copies are in `source-plot-manifest.json`; matching paths/hashes establish provenance only. The following independent pixel/geometry observations establish endpoint/direction extraction.

| Source | Origin pixel | x/y unit pixels | First endpoint pixel/coordinate | Second endpoint pixel/coordinate | Directed arrows |
|---|---|---|---|---|---|
| q-18051 | (186,180) | approximately34/34 | (50,146), A(-4,1) | (287,180), B(3,0) | blue O→A and O→B; no AB arrow |
| q-18052 | (160,183) | approximately39.3/39 | (81,104), P(-2,2) | (278,66), Q(3,3) | blue O→P/O→Q; orange P→Q, head at Q |
| q-125118 | (160,163) | approximately39/39 | (199,85), P(1,2) | (82,124), Q(-2,1) | blue O→P/O→Q; orange P→Q, head at Q |
| q-18049 | (118,183) | approximately41/41 | (77,60), C(-1,3) | (159,266), D(1,-2) | blue O→C/O→D; no CD arrow |
| q-18055 | (141,233) | approximately56/46.7 | (197,186.5), P(1,1) | (253,93), Q(2,3) | none; blue point markers only |

The first four have black horizontal x and vertical y arrows, black O near intersection, orange unit i and j arrows from O to (1,0)/(0,1) with orange labels; blue position-vector letter labels a/b, p/q or c/d. Their endpoint coordinates are printed in black, and their arrow tips coincide with marked labeled endpoints. Axes have no numeric ticks or grid. Their black axis arrows terminate at right/top. Displacement arrows occur only in the two PQ position plots listed above. There are no right-angle markers, Pythagorean right triangles, projection guides or unrecorded extra points.

q-18055 has gray Cartesian grid and black axes, x ticks-2,-1,1,2,3, y ticks-1,1,2,3,4; point P at x1/y1 and Q at x2/y3, labels black P/Q near blue circles. The blue-marker coordinates were independently read using actual origin and tick spacing, not generation metadata or the solution. The source has unequal pixel scale along x/y, so pixel lengths alone cannot be used as norms. Its coordinates are still unambiguous. Generated plots use equal coordinate units to make Euclidean geometry meaningful.

## 2. Shared visual pattern

Two point locations on Cartesian axes support end-minus-start displacement. Coordinate families illustrate position vectors from O and sometimes the directed displacement. The graph-reading family supplies essential position information and must be regenerated for every changed endpoint pair.

## 3. Components

Fixed: white background, black x/y axes with right/up arrows and labeled origin; blue endpoint markers; coordinate-family blue O→endpoint arrows and orange unit-basis arrows; family-specific orange directed first→second arrow; graph-family gray grid/visible signed integer scales. No invented triangles or projection arrows. Variable: endpoint coordinates/position-vector lengths, label positions, arrow tips, axis bounds and tick demands. No mathematical point can resample independently.

Source graph coordinates, all position-vector tail/tip pairs, displacement direction, unit vectors, color roles and absence of guides are independently transcribed above. Render-specific sidecars record actual axes transforms/PNG hashes. Original source raster copies are reused only for exact anchor evidence; changed evidence and every normal instance are generated from the endpoint tuples.

## 4. Matplotlib specification and QA

Private720×600 PNGs, equal generated axis scale; bounds contain origin and endpoints with two coordinate units of margin. Vector letters use perpendicular display offsets and origin-label quadrant avoids the incident rays. Endpoint labels use display offsets and white backing to separate arrows/grid. Coordinate-family tuples remain readable; graph-family P/Q labels omit numeric coordinates so the learner reads ticks. Authored hard uses tick2 (odd integer positions between ticks), moderate graph tick1. Unit basis arrows have true unit lengths independent of sampled endpoint size. PNG and JSON sidecars use per-call unique temporary filenames and atomic replacement; cache requires both files. Fresh independent-process identical/different render tests check marker positions and content hashes.

Validator independently extracts blue marker centers from actual generated graph PNGs and calibrates coordinates with rendered axis transformation, then verifies black origin intersection/equal units. The original q-18055 uses separately measured source pixels/units; no source geometry proof depends on matching an asset hash. Native visual review of changed sign/quadrant/boundary instances remains a separate check from field-ID grading.
