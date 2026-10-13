# Four-stage plot extraction and specification

## 1. Specific originals

`assets.json` maps all 13 unique raw plot references to practice/canonical sources. `source-montage.png` composites transparent originals on white for inspection, preserving raw bytes under `raw-images/` and original relative references under `images/`. The canonical pair cuts x=−1,y=−1 and has signs (+,−,−,+) in left/below,left/above,right/below,right/above order. q-97538 cuts x=−1,y=2, signs (−,+,−,+). q-119797 and q-119816 share partition x=2,y=−1 but their signs are respectively (−,+,+,−) and (−,+,−,+): reuse of a partition does NOT permit reuse of its sign diagram. q-119800 cuts x=1,y=2, signs (−,+,+,−). q-97495 cuts x=−2,y=−2, signs (+,−,−,+). q-97534 cuts x=1,y=1, signs (−,−,+,+). Independently transcribed `source-plot-checks.json` is checked against actual displayed equations. q-96475 supplies no source diagrams and receives a generated pair.

Each original has x/y axes with positive-direction arrows, two thin blue zero lines x=h,y=k, labels on those lines, no numeric tick grid, and four rectangles. Partition plots have white background. Sign plots fill positive regions pale blue and negative regions pale peach, and explicitly label f(x,y)>0 or <0 in each. There are no slope segments or trajectories: these are sign-region diagrams, not sampled slope fields. Original source dimensions and bytes remain unchanged.

## 2. General shared pattern

First show the two axis-parallel zero lines defining four open rectangles, then the same geometry with signed regions and annotations, tying the sign directly to the differential equation. The diagrams carry the worked reasoning and recur in all variants: plot rating moderate.

## 3. Components

Fixed: white canvas, x/y axes and arrowheads, no ticks, blue boundary lines, pale sign colors, serif math labels, equal geometric aspect. Variable: roots h,k, factor parity/orientations, sign of f in each rectangle, bounds and region extents. Plot bounds derive as min(−3,h−2)/max(3,h+2), similarly y, ensuring both coordinate axes, zero lines, and all four regions are visible. Test points are region midpoints; printed sign text is repositioned when the midpoint falls on an axis. Boundary labels sit outside the plot at top/right to avoid text overlap for narrow rectangles or shifts ±3. This placement is an authored visual adjustment, not a mathematical or original solution-text change.

## 4. Reusable plot specification

`render_plots(instance, output_dir=None)` renders partition/signs using exact supplied parameters, no resampling. The complete geometry key contains both roots, both factor orientations, and both parities. Matching source geometry reuses the exact original relative image references only if all these match; changed geometry uses `render.py` with Matplotlib, 728×728 PNG, one fixed pair per geometry. The figure annotations derive from the same equation as the question. Answer choices are text; no choice-specific plots are required. There are no endpoints or solution trajectories to preserve.

Renderer dependency fallback uses already-cached read-only Python3.10 Matplotlib wheels; no installation or network. Sidecars record Python/Matplotlib versions, dependency paths, limits, roots, actual test points and evaluated slopes, signs, role and geometry fingerprint. Each call has a unique temporary input path; PNG/JSON writes are atomic, and cache hits require both PNGs plus matching JSON sidecars. Fresh private-output concurrency tests check two identical and one different geometry. Source reuse does not expect JSON sidecars; raw inspected source geometry has separate evidence.

Visual QA: all original assets inspected together; generated sign and partition montage covers every observed profile's changed geometry and all three authored levels. Labels, line locations, sign colors, arrowheads, clipping, overlap and readability are manually checked. Source same-root differing parity/sign-grid cases keep their correct distinct sign diagrams.
