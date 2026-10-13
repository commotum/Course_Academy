# Plot extraction: unit-circle reciprocal ratios

The [plot-extraction protocol](../../../docs/5-plot-extraction.md) applies because diagrams carry the first-quadrant branch restriction. Eleven practice image occurrences and the canonical-example image were inspected at their original 410×412 resolution through a labelled contact sheet. All required practice assets exist and were copied locally; [manifest](../plot-assets.json) records their roles and source hashes.

Specific sets: `q-124750`, `q-124743`, `q-65062`, `q-65064`, and `q-85234` each contain a prompt image and annotated solution image. Their known coordinates are respectively y=1/5, x=1/3, y=√3/3, x=√15/5, and y=√2/3. `q-65066` has only its prompt image, at y=3/5; it has no stored worked solution. Canonical `e-3484` has a prompt image for x=2√6/7.

Each figure has a white background, a light gray square grid, black x/y axes with arrowheads, a blue unit circle centered at the origin, labels at ±1, a black radius to a point P in the first quadrant, and an ochre angle sector θ measured counterclockwise from positive x. Prompt figures label P; solution figures label P(cos θ, sin θ). The actual coordinates and angle change across originals. Fractions are stated in the prompt, not read approximately from the picture.

Reusable specification: equal axis scales; a unit circle; axes through zero; first-quadrant point `(x,y)` satisfying x²+y²=1; segment from `(0,0)` to `(x,y)`; angle `atan2(y,x)`; a small filled sector at the origin; nonoverlapping labels. The solution version changes the point label and retains identical coordinates. Grid density, blue/ochre hues, and line widths are stylistic; the circle radius, point location, angle direction, and quadrant are mathematical constraints.

For given x=g, set point `(g,sqrt(1-g²))`; for given y=g, set `(sqrt(1-g²),g)`. Generate both images from the same parameters used in the prompt, answers, and solution. Reuse a source image unchanged only when those parameters and annotations also remain unchanged. Otherwise new figures are required. Plot rating is **moderate**, because recurring paired figures support interpretation and branch selection, even though constructing a unit circle is technically simple.

The authored x=5/13 probe has a new prompt and solution pair with P=(5/13,12/13). These reproduce the mathematical relationships and broadly similar visual components, rather than claiming pixel-level source fidelity. Its explicit first-quadrant sentence also preserves the branch restriction if viewed without the image.
