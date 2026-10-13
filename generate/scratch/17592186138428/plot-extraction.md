# Four-stage plot extraction and reusable specification

## 1. Inspected originals

All original EDB PNGs were inspected, plus authoritative lesson 2225's question widget screenshots. Practice images are 360×310, white/transparent background, gray unit-square grid, black x/y axes through zero with right/up arrowheads, nonzero signed integer tick labels, orange first line and blue second line. Lines carry their actual equation labels. q-171700's window is approximately [-3.5,7.5]×[-4.5,4.5], intersection (3,-2). q-238014 uses approximately [-2.5,7.5]×[-4.5,4.5], intersection (3,0). Neither prompt marks or labels the answer coordinate.

Canonical prompt uses x+2y=8 (orange) and 2x-y=6 (blue), intersection (4,2). Its solution plot adds a black intersection point and dashed horizontal/vertical coordinate guides. The solution prose states the coordinate. No source practice solution image was supplied.

## 2. Generalized purpose

Two labeled lines on equal Cartesian unit scales let the learner read one unique intersection. Prompt graph contains the assessed data, so every changed system needs a new graph. Solution graph preserves the same lines/grid/bounds and adds canonical point/guide cues.

## 3. Components and provenance

Local immutable image copies: source-images/q-171700.png, q-238014.png, e-13129-prompt.png and e-13129-solution.png. Original paths and SHA hashes are in plot-source-comparison.json. The plot inputs are primitive coefficients [a,b,c], exact intersection, exact equation-label text and bounds. Color order links rows to lines. Every point sample obeys ax+by=c; labels must identify that same equation. Hard figures number major ticks by 2 and retain unit minor grid lines, following the canonical plot's demonstrated scale convention. Both hard coordinates are odd and require reading an intermediate grid value. Arrows, unit ticks and equal aspect preserve readable signed coordinates.

## 4. Reusable specification

Private render.py uses pinned cached Python 3.10 and Matplotlib 3.10.9, not an image model or SVG. Its 620×540 PNGs increase readability while preserving instructional geometry. Source replay preserves recovered windows and numbered unit ticks. Hard authorship uses numbered even ticks plus the same unit grid. Other windows include the axes and at least three units around each coordinate. Lines run across the whole window and are clipped at its bounds. Prompt has no intersection marker or coordinate label; solution adds black marker, dashed axis guides and an explicitly authored coordinate label. Zero-length guides at axis intersections are harmless; other coordinates still determine the labeled point.

Equation text is placed away from the intersection and axes; distinct top/bottom anchors avoid collisions in steep-line variants. Source replay has recovered equation placements. White label backgrounds and larger raster size are incidental readability changes, not pixel-exact reproduction. Colors remain orange/blue. Matplotlib computes all samples from the actual shared coefficient rows; it never resamples.

Each image has an atomic JSON sidecar with plot inputs, samples, label coordinates, dimensions, role and renderer provenance. Cache hit requires both PNG and sidecar. Calls use unique input files and atomic final writes, including identical concurrent jobs. No normal cache pruning occurs. Fresh identical/different concurrent calls are tested in a new private directory. Inspect and compare actual PNGs as well as sidecar mathematics; pixel-exact source identity is neither asserted nor counted.
