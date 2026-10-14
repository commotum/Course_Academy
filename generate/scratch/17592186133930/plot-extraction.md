# Plot extraction

## 1. Specific source inspection

All six original PNGs were composited on white and inspected in `source-plots.png`; source paths are retained in exact public replay. Every diagram shows a closed pale-blue solid, three positive x/y/z arrows and hidden dashed coordinate segments. Solid/hidden lines indicate visibility, not exclusion of boundary faces.

| Source | Original asset prefix | Solid and independently read labels |
|---|---|---|
| q162411 | d0/d0f6f5 | Cylinder axis z; height2, radial x1 and y1; both circular caps included |
| q162569 | 58/581ac4 | Cylinder axis x; height3, radial y2 and z2; both circular caps included |
| q162570 | 98/9861e9 | Cylinder axis y; height2, radial x3 and z3; both circular caps included |
| q162572 | aa/aac270 | Box first octant: x1,y2,z3; all six faces included |
| q162571 | 07/07b46a | Box first octant: x1,y2,z1; all six faces included |
| q162573 | 6d/6dc4f6 | Box first octant: x4,y2,z2; all six faces included |

The cylinder axes differ. Rotating all cylinders onto z would lose an observed geometric cue, although flux is invariant here. The generator retains each axis. The source q162411 legacy widget anomaly is unrelated to its diagram.

## 2. Generalized pattern

A closed cylinder or rectangular solid is drawn in a consistent oblique projection. It supplies the dimensions needed by a geometric volume formula; the vector field is in the accompanying prose.

## 3. Components

White background; projected x vector(-.72,-.58), y vector(1,-.10), z vector(0,1); pale-blue solid caps/faces; thin blue outline; dashed internal coordinate segments; black positive arrows, axis names and dimension labels. Cylinder base is at axial coordinate0 and opposite cap at h, radial coordinates span[-r,r]. Boxes span[0,a]×[0,b]×[0,c]. The shape and every label derive from the exact geometry of the generated question. Bounds include all vertices/circular rings and arrow tips plus a margin. Projection is illustrative rather than a coordinate grid.

## 4. Reusable specification

`plot(geometry)` uses Matplotlib patches, sampled circular rings and the fixed oblique axis vectors; PNG and JSON sidecar are written atomically through per-call unique temporary files. Sidecars include exact geometry, renderer version, meaningful dimensions and plot bounds. Parameter changes redraw the diagram and update prose height/radius or diagram edge labels together. No direct SVG or image model is used. Raw profiles keep the original asset path and fixed geometry; normal profiles always use the generated asset. Renderer fidelity is geometric/semantic rather than pixel-exact styling. Numerical labels are offset from the marked endpoints and positive arrow labels.

`variant-plots.png` shows the six generated easy-family diagrams at seed11. Visual QA checked the changed radial/axial labels and all six box faces; interior axis segments remain dashed and positive arrows start at the boundary. Fresh concurrent renderer calls for identical and different geometries are tested in separate private `render-concurrency-*` directories, with no cache deletion.
