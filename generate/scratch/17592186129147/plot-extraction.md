# Four-stage plot extraction and specification

## 1. Native original inspection

All eight PNGs (canonical e-5818 plus seven practice banks) were opened at original native resolution, without thumbnails/contact-sheet substitution. original-assets.json lists exact refs, dimensions, hashes and copies. Each is a 2×2 panel bank with red polynomial curves, black horizontal and vertical arrow axes, root-coordinate labels, and no y ticks, scale, degree annotation or labeled ordinate point. The canonical uses roots -2,-1,2 and selects III. Its full representative bank is I: negative sign [1,2,1]; II: positive sign [1,1,1]; III: positive sign [1,2,1]; IV: negative sign [1,2,3]. All six canonical pair signatures are distinct; it introduces simple/even/simple root behavior plus positive leading sign. The complete practice mappings are in DATA, template-extraction.md and bank-proof.json; all 28 practice panels are accounted for.

Root inspection of all eight original assets at full native resolution confirms that every panel is labeled I, II, III or IV. The earlier report of missing or duplicated labels was incorrect and has been removed. Raw source profiles remain evidence-only because they replay captured examples; normal profiles generate varied, clearly labeled main graphs and local views. No source label repair is needed.

## 2. Shared visual purpose

Graph-choice selection uses precisely root locations, simple non-tangent crossing, even touching/reversal, odd multiple tangent crossing, and leading-sign end behavior. The scale is qualitative. Neither positive coefficient amplitude nor exact multiplicity among even multiples/odd multiples is recovered from the source graph. Curves are genuine polynomial representatives consistent with those visible categories.

## 3. Components and relationships

The same instance supplies ordered roots, fixed exponents, sign and factor order. Each complete bank member supplies its own exponents/sign. The whole graph, axes, tick labels, local root views, signs and solution use these factors. Background is white, curve red, axes black, no y ticks. All roots are labeled, including zero at the true origin. Zoom windows have gray frames, a black y=0 line and gray vertical x=root guide, and labels x=root. They are distinct panels under the parent sketch, preventing curve-label overlap.

## 4. Reusable Matplotlib specification

Normal figures are 1300×1040 PNGs. Each of four panels has an actual polynomial main graph, derived bounds around the roots, derivative-isolated real extrema determining vertical limits, exact root samples and a dense grid. Arrowheads near main curve exits show directions. Axis zero positions are mathematical zeros; bounds include x=0 even when every root is on one side. Roman labels sit outside the curve region. Root labels have pixel offsets and no y ticks. Derivative roots are isolated exactly to narrow rational intervals, avoiding numerical failures on repeated roots.

High-degree polynomials and uneven root gaps can make a small lobe visually vanish at the main panel scale. Every generated panel therefore has one true-function local zoom for each root. Width is 0.14 times the nearest-root distance, so another root cannot enter the window. Each local graph uses its actual f(x) values with a separate vertical range and true y=0 axis. The image explicitly states “Small boxes: local views at roots, with independent vertical scales.” This preserves the assessed method and lets simple versus tangent crossings, and touching versus crossing, be read at native pixels. It is an authored visual extension, not recovered original artwork. Normal original-parameter renders get the same zooms and label repair.

No marked scale points are present in originals or authored output. Introducing coefficient-magnitude distractors without such evidence would be ambiguous; these are rejected after qualitative signature collapse. All six pairwise comparisons include wrong–wrong pairs. Sidecars retain exact factors, expressions, extrema, main and local sample coordinates, bounds and runtime versions. Validation substitutes samples into the exact same function and checks pixels/dimensions. Plot images and sidecars are atomic writes protected by a private renderer lock, with unique temporary files. Fresh concurrent identical/different parameter renders verify instance consistency. No SVG, raster synthesis/image model, or database writes are used.

Native generated images reviewed: all 16 review records (two per complete profile), plus hard boundary cases with roots -4,0,4 and -3,0,3. The local views expose the classification even when the main graph is strongly asymmetric. The source-preserving plot-reference change does not claim exact arbitrary y coordinates for its unlabeled sketches.
