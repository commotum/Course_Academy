# Plot extraction and specification

## 1. Native inspection

All twelve practice prompt assets and canonical e-3569 were viewed individually at their native 360×304 pixels, without interpolation. There are no plotted options or solution plots. All plots have white background, black actual coordinate axes with arrowheads, red curves, and open/filled red markers where specified. A missing numeric tick does not establish a missing axis or zero. Calibration is per plot (`specs.json`: origin pixel x/y and independent unit scales).

|Plot|Independently transcribed geometry and assessed coordinate|
|---|---|
|e-3569|Origin (73,163), x unit48, y unit40. At x=2 filled (2,2), open (2,1); left bowl minimum (0,-2), right cap near (3,2). Tails leave lower crop. Canonical I true only.|
|q-48042|Origin (170,243), units40/40. Vertical dashed asymptote x=2; left tail descends below crop toward -infinity; filled right endpoint (2,3), oscillating right branch, no open marker. Left branch approximately approaches ordinate3 far left; exact formula unknown.|
|q-48064|Origin (73,194), units48/32. Filled (2,1), open (2,-2); left curved maximum near (0,5), right minimum near (3,-3). Assessed x=2; unequal finite one-sided limits. No captured designation/solution/rating.|
|q-48063|Origin (90,243), units40/40. Open (2,3), isolated filled (2,1). Smooth decreasing curve through the hole; left local flattening, right tail crosses x axis near5.5. Asked left-sided existence at2, not two-sided existence.|
|q-104049|Origin (85,203), units56/40. Unmarked continuous join (2,2), left concave curve rises to join, straight right branch crosses x axis near4; no marker or asymptote. Exact left formula unknown.|
|q-104051|Origin (65,243), units42/40. Filled (5,2), open (5,4). Left branch gently increases from near ordinate1; right decays from4 toward near1. This is a jump, not a vertical asymptote.|
|q-104052|Origin (170,203), units40/40. Open (0,3), no filled point at0. Two straight arms descend from the missing vertex; no x ticks other than axis. Both limits3; exact straight-arm slope is a raster geometric estimate.|
|q-104124|Origin (266,243), units48/40. Unmarked continuous corner (-2,5), descending straight arm to unmarked (0,0), then rising straight arm. Left curved branch flattening around x=-4 before reaching -2. Asked x=-2.|
|q-48040|Origin (170,243), units40/40. Open (-1,2) on descending line; filled (-1,1) on parabola with unmarked vertex (0,0). Asked x=-1, right-sided value1, left-sided value2.|
|q-48062|Origin (170,163), units51/50. Smooth increasing curve flattened around x=0, open (1,1), no filled point. Tails leave crop below left and above right. Formula unknown.|
|q-48065|Origin (110,243), units40/40. Unmarked continuous vertices (1,-1), (2,1), and smooth bowl minimum (3,0). Target2 has value1, although it is a corner. No open circles.|
|q-48067|Origin (70,243), units64/40. V vertex is (2,0), continuous and unmarked. Target is x=1, on left arm, where value1. Target is not the vertex.|
|q-48068|Origin (170,243), units48/40. Filled (-1,1), open (1,1), outer upward curved arms; middle cap peaks around (0,1.5), unlabelled ordinate uncertain. One-sided claims ask +1, continuity asks -1. No asymptote.|

## 2. Generalized pattern

One curve-bearing prompt, actual zero axes, scale ticks, and local topology sufficient to evaluate three claims. Filled versus open markers, asymptotic tails, and the exact asked coordinate carry assessed information. Unqueried curve formulas and unlabelled extrema are not recoverable from these rasters and are not asserted as algebra.

## 3. Components and bounds

`specs.json` retains each calibration, labelled local limits/value, markers, and asymptotes. For changed easy coordinates, red stroke pixels are mapped through the independently calibrated transform, horizontally translated, and rendered as red Matplotlib samples. Marker footprints are removed and markers are rendered from the independently transcribed inclusion predicates. Axes/ticks are constructed at the actual x=0/y=0, not translated from the original axes. Bounds include both axes and the original cropped curve extent; original unmarked tails remain cropped without invented curve direction arrows. A source negative-power coordinate typography is retained in exact raw replay.

## 4. Reusable implementation

Matplotlib alone writes 720×608 PNGs and JSON geometry/axes-transform sidecars atomically with unique temporary names. Cache use requires both artifacts. Native-source anchors reuse exact copied source assets. Changed curves preserve raster silhouette and endpoint topology; this is conservative trace parameterization, explicitly not symbolic formula recovery. No source SVG, model image generation, or global renderer modification is used.

Authored fractional plots use numeric samples of two local finite parabolic arms or ±1/|x-a| asymptotic arms, with separately marked value at a; formulas are internal geometric construction, never given to the learner or used as an algebraic-limit exercise. The second hard coordinate is a±1 and either an ordinary curve point or a white open circle on that branch. Moderate ticks show half units. Hard ticks retain quarter-unit grid/ticks, but label integers and assessed quarter coordinates to preserve legibility. Bounds contain all markers with margin and both actual zero axes. One-sided infinity is sign-correct and branches reach beyond the plotting window.

Automated QA reads actual saved marker center pixels under each saved transform: filled centers must be red; open centers must be white. Source trace geometry is anchored by independently transcribed calibration and inclusion facts. Review images were read at full generated pixel size. A first rendering had literal TeX fraction tick text and crowded hard labels; version2 adds MathText tick labels and reduces hard label density. Cached version1 assets remain private evidence and are not referenced by final review.
