# Plot extraction and generator specification

All eleven unique relevant PNGs were inspected at original resolution: canonical plus eleven practices, with one shared annulus image. Visual extraction confirms geometry independently of asset paths.

| Source | Visual geometry and cues |
|---|---|
|e-9558|outer [-2,1]×[-1,2]; hole [-1,0]×[0,1]; D label|
|q-126566|annulus inner radius 1, outer radius 2; D label|
|q-126645|outer [-4, 4, -3, 3]; hole [0, 2, -1, 2]; D label|
|q-169207|annulus inner radius 1, outer radius 2; R label and vector arrows (3xy²,−y³)|
|q-126935|annulus inner radius 1, outer radius 3; D label|
|q-126937|annulus inner radius 2, outer radius 4; D label|
|q-126941|outer [-2, 2, -1, 2]; hole [0, 1, 0, 1]; D label|
|q-126945|outer [-2, 2, -1, 2]; hole [-1, 1, 0, 1]; D label|
|q-126939|annulus inner radius 1, outer radius 4; D label|
|q-126938|annulus inner radius 1, outer radius 3; D label|
|q-126942|outer [0, 3, -1, 2]; hole [1, 2, 0, 1]; D label|
|q-126946|outer [-1, 2, -2, 2]; hole [0, 1, 0, 1]; D label|

Every original has white background, equal Cartesian scale, black coordinate axes through zero, orange **solid** outer and inner boundaries, pale blue fill and a white hole. The rectangle’s four outer and four inner edges are all solid. Annuli label both signs of inner/outer x intercepts; rectangle tick labels specify bounds of outer/hole edges. Region labels are blue and italic. No source shows boundary orientation arrows. q-169207’s blue vector arrows are contextual field direction arrows.

For each normal variant, Matplotlib draws circles or rectangles from exact instance parameters, deriving axis bounds and ticks from geometric extrema plus padding. Labels and plot fill derive from the same domain. In q-169207 the quiver direction is derived from (3cxy²,−cy³), so negative amplitude reverses it. Quiver vectors are normalized to show direction; magnitude is not assessed by this plot. No answer or solution plots occur.

Moderate rating: recurring plots carry all bounds. Raw evidence uses original asset references at original amplitude/geometry. Changed-amplitude raw evidence rebuilds its original geometry from the extracted parameters; contextual arrows reflect the changed amplitude sign. Normal plots recreate changed geometry and contextual vector signs. No images are generated with models or direct SVG. PNG names include all plot parameters and renderer version. Cache hits require PNG plus JSON sidecar; fresh writes use unique temporary files and atomic replacement. Concurrent identical and different-parameter fresh calls are checked in a private directory. A renderer lock serializes Matplotlib drawing because its global text/layout state is not thread safe; atomic unique-file writes retain deterministic assets. No active review asset cache is pruned.

Renderer runtime: Python 3.13.5, Matplotlib 3.11.2.
