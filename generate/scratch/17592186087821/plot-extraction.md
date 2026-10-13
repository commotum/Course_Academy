# Plot extraction and specification

## 1. Individual actual rasters

All 35 choice rasters were visually inspected at native 360×304 resolution.
Their per-option paths/hashes/labelled geometry are in plot-observations.json.
All have white backgrounds, thin black axes labelled x,y with positive arrows,
blue smooth exponential curves, and labelled blue y-intercept dots. Nonzero
horizontal asymptotes are dashed black and labelled y=value. No choice has a
numbered x/y tick grid. Origin position and vertical scale vary between assets;
there is no common pixel origin or common mathematical x-unit to recover.
Moderate no-shift options and q-25292 option 5 appear to approach the x-axis. Zero is a modelling convention for these unlabelled limits, with corresponding amplitude uncertainty; the raster alone does not prove an exact zero limit. They have no
separate numeric y=0 label. The negative-amplitude legacy options approach their
asymptote from below and decrease as x increases; decay distractors approach
their asymptote on the right. Curves carry no tip/tail arrowheads or marked
finite endpoints. They are clipped at raster edges, not restricted-domain curves.

All ten present worked-solution rasters were also inspected individually at native
resolution. First graphs are orange y=b^x with a (0,1) marker. Final graphs overlay
orange original and blue shifted curves, a red vertical translation arrow, both
intercepts and the new dashed horizontal asymptote. The down-shift −0.75 overlay
points downward. Exact baseline source replay keeps these assets unchanged.

## 2. Generalized visual pattern

Choice plots communicate vertical level, intercept and growth orientation.
Solution plots communicate moving every point by the supplied shift. Heavy plots
are essential here. Original horizontal curve scale is underdetermined by the
unticked rasters, and no exact original base-to-pixel fit is claimed.

## 3. Components

Generated choices share bounds per question, preventing bounds from signalling
correctness. Mathematical components are b,A,c,exponent direction; display cues
are labels or numbered grid. Axes include positive arrows and labels; all chosen
curve data comes from that exact instance. Source replay values remain original
image references. Generated assets are local Matplotlib PNGs. Solutions retain
orange original/blue translation/red arrow and the fixed two-image stage order.
The arrow is placed at x=−3.5, clear of coordinate labels, and compares b^x to b^x+c at the same x, including negative shifts.

## 4. Reusable renderer and verification

The renderer samples A*b^(D*x)+c over −5≤x≤5. Y bounds include all bank asymptotes
and intercepts plus margins; each entire bank shares that viewport. Labels render
exact source-like rational notation; hard bank options omit those labels and use
minor grid 1/denominator(c), with numbered integer major ticks. Correct graph is
not mathematically stretched. Wrong amplitudes and reversed directions are
explicitly sourced/operation-derived distractors only. Source curves have no
arrow tips, so new curves have none. Shared solution roles add the original
orange curve and actual signed translation arrow.

Each cache key includes renderer version, all geometry, bounds and annotation
settings. Cache hits require both PNG and matching sidecar/hash. Renderer inputs
have unique temporary names; PNGs and sidecars are replaced atomically and inputs
are removed. Fresh concurrent identical/different requests are tested without
pruning active caches. Sidecars record real Python/Matplotlib/NumPy versions,
axes transforms and sample data. The private pixel checker reads the actual PNG
and independently recomputes expected curve positions from axis bounds; it
requires blue/orange pixels within a bounded 4-pixel antialias/stroke allowance.
Human visual QA checks actual generated examples' signed labels, grid spacing,
arrow direction, legibility and cropping. The cached Python 3.10 Matplotlib
fallback uses only pre-existing dependency wheels, without installing anything.

Renderer v7 places feature labels using measured Matplotlib mathtext bounding boxes. The closest valid candidate is chosen to preserve point/label association. Candidate boxes must be inside the viewport, with 4 pixel clearance from both axes, the dashed asymptote, sampled blue/orange curves and red arrow, 7 pixels from markers, and 5 pixels from other labels. Feature labels have no background boxes. The saved sidecars contain actual label bounds and placement; independent verification reconstructs every curve and checks all bounds. Hard calibrated tick-label guards remain. Near-zero intercepts of both signs, the exact origin intercept and base-domain boundaries are regression images in label-regression.json.
