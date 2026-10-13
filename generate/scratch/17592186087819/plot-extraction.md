# Route plot extraction and specification

## 1. Actual captured figures

All seven PNGs in `images/` were inspected. Circles have pale pink interiors, black outlines and station-letter labels. Blue directed arrows join circles; repeated arcs mean distinct routes. Self loops begin and end at the same station circle; each arrowhead counts once. No coordinates, grid, line lengths or geometric scale are assessed.

q-138940 and q-139689 put A below B at the left, C at right, with B self loops (plus an A loop in q-139689). q-139685 has the same triangle without loops. q-139719 uses a square whose original screen corners are D,C / A,B, so labels must be read rather than assigned clockwise. q-319346 is a triangle A left, B top, C right with multiple opposite-direction arcs. q-319412 puts C above central D, A left and B right; the vertical C↔D arcs and outer C connections are genuine directed relations. q-319429 has A,B across the top and C below, loops at A/B/C, three A→C arrows and B↔C connections.

## 2. Generalized role

Each prompt contains one directed multigraph encoding the complete row-departure/column-arrival adjacency matrix. It is central to every task, so plot rating is **heavy** for every family. Answer options are scalar counts and solutions are tables; no answer or solution diagram is required.

## 3. Component mapping

- Background: white, no axes/grid.
- Station nodes: three triangular positions or four square corners; letters centered in nonoverlapping pink circles.
- Directed routes: one blue curve and one arrowhead per integer adjacency count; no edge-weight labels replacing parallel arrows.
- Direction: arrow origin and destination follow exact ordered matrix coordinates.
- Parallel and reciprocal arcs: separate curvatures, shortened to node boundaries, consistent width/color.
- Self routes: curved loops on the outward side of the node, separated by angle and loop length for counts 1..3.
- Bounds: fixed derived safe padding beyond triangle/square node coordinates includes the maximum three-loop and three-parallel-arc domain. Diagrams are not to scale.
- Labels: upright regular serif letters match the source style. Use the installed `LiberationSerif-Regular.ttf` explicitly, without a sans-serif fallback. Node letters remain above route paths in the draw stack and inside opaque circles, so incident arrows do not obscure labels.

## 4. Renderer specification and QA

`render_routes.py` uses Matplotlib `FancyArrowPatch`, `Circle` and cubic path loops. No direct SVG or image model. The primary venv lacks Matplotlib; read-only cached Python 3.10 wheels provide the already documented fallback without installation or shared-environment changes. Each sidecar records Matplotlib/Python versions and dependency paths, complete matrix, node coordinates and the independently countable list of individual directed edges.

The generator supplies its exact adjacency matrix to `render_plots`; no resampling happens inside plotting. Cache identity includes the full meaningful directed matrix, renderer version, and label-font SHA-256. Sidecars record the actual font family, file, hash, style, weight, and size. Cache hits require both PNG and sidecar. Exact source matrices reuse the captured source PNG only when their full meaningful route structure matches; changed matrices are always rendered. Parameter-dependent plots use a clear larger diagram with every original mathematical cue, without claiming pixel-identical source layout.

Each call has a unique input file and atomically publishes PNG and sidecar through unique temporary files. Validation exercises fresh concurrent identical and distinct matrices, parses all individual edge records to independently reconstruct the diagram matrix, compares that matrix with the actual displayed ordered prompt/solution tables, and confirms stable IDs. Images remain available during parent QA; no cache pruning occurs.

Visual QA viewed changed easy/moderate/hard images directly. Pink nodes and labels are legible, all three-loop arrows have separate visible heads, reciprocal and parallel arcs are countable, and four-node connections stay clear of other nodes. Source figures retain their exact original pixels for observed replay. Plot geometry is incidental, but directed route counts and node labels are essential and preserved.
