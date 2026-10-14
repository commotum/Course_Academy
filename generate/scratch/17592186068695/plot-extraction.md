# Plot extraction and specification

## 1. Individual original assets

All32 originals were read at their actual resolution,31 at353×298 and the canonical at360×304. RGBA originals were composited on white, without resizing, in source-plots/. These inspection copies are separate evidence; raw observed replay preserves original relative paths. All graphs have black coordinate axes with arrowheads, red function strokes, no area fill or curve traversal arrows. Open points are white-filled red rings, and closed points are solid red dots. The axes do not specify y-unit values except the canonical reciprocal. Numeric y-coordinates therefore cannot be inferred for the others. Unlabelled extrema/endpoint ordinates are not asserted as exact source values.

The asset prefix resolves to its exact reference in source-plots/refs.json. Each row records the individual boundary/point roles, including incorrect options and unrelated branches. A joined corner without a circle remains included in the curve.

|Prefix|Role and independently inspected geometry|
|---|---|
|4020dd89|q48039 wrong: dashed vertical asymptote at-2; left tends downward, right upward. Wavy right branch disconnected across pole; no marked point.|
|4a009c92|q48039 wrong: left wavy branch ends open at-2; lower right branch begins at filled-2, so a jump.|
|56576892|q48039 wrong: descending line has an open hole at-2 and a separate lower filled point at-2.|
|f4a28f88|q48039 correct: joined closed peak at-2; unrelated lower filled point at1 and upper open circle on curve at1.|
|29ff22e9|q48039 wrong: dashed pole at-2, both sides descend without any marked value.|
|0a31db89|q48081 wrong: inverted V has open peak at2; lower filled singleton at2.|
|8c2cca8f|q48081 wrong: dashed pole2, left downward/right upward, horizontal tails above x-axis.|
|fdd6b61f|q48081 correct: connected descending bowl rises to a sharp closed peak at2 then falls, with no open or separate value at2.|
|56a689e2|q48081 wrong: dashed pole2, both sides upward, left wavy branch; no point on pole.|
|4ad2a8ae|q48081 wrong: wavy left branch open at2, lower right branch filled at2.|
|42e1d990|q69782 wrong: rising branch becomes horizontal, ends open at5; lower horizontal right branch starts filled at5.|
|d124370f|q69782 correct: left constant ends filled at2; higher parabola begins open at2, then has a closed unmarked minimum at5.|
|17fc3c79|q69782 wrong: dashed pole5; left tends negative infinity and right positive infinity.|
|76a1b2ca|q69782 wrong: rising line open at5; separate lower filled point at5.|
|135973e3|q69782 wrong: dashed pole5; both sides descend to negative infinity; no marked value.|
|c6f0914f|q48082 correct: smoothly joined graph around0; at2, open point on lower curve and separate upper filled singleton.|
|c2f85d1a|q48082 wrong: opposite infinite branches at0 and an isolated filled origin. Finite function value does not repair the asymptote. No dashed guide; y-axis occupies pole.|
|14349b3d|q48082 wrong: wavy left branch open at0; lower wavy right branch starts filled at0.|
|3073f651|q48082 wrong: V with open vertex at0 and filled origin below vertex.|
|c95d9944|q48082 wrong: left constant ends filled at0; right branch tends positive infinity as x approaches0 from right. No dashed guide; y-axis marks pole.|
|d9cf9a5c|q102106 prompt: closed peak-1, smooth join0, lower open hole1 with upper filled1, branch continuous at2, dashed pole4 with left upward/right downward. Queried ticks-1,2,4.|
|95967eb8|q102106 solution: same points and pole asd9, blue neighborhoods at-1 and2; blue does not close hole1 or bridge pole4.|
|43544a1b|q78133 prompt: left constant ends open-7; lower curved branch starts filled-7, rises to closed peak-4, lower open hole-1 with isolated filled point on x-axis-1. Ticks-7,-4,-1.|
|d1d91b2d|q102115 prompt: lower left line ends filled-1; higher right branch open-1. At1 branches meet at a lower open hole, with upper filled singleton. Right branch continuous at3. Ticks-1,1,3.|
|57415045|q102115 solution: same open/filled roles asd1; right neighborhood at3 blue.|
|3c0dc4b8|q78131 prompt: dashed negative-infinity pole-2 on both sides, joined closed peak0 with right decreasing branch continuous at2. Ticks-2,2 and origin as0.|
|890e7eaf|q78132 prompt: left constant joins curve near-2 without a circle; low curved branch ends open1; upper descending straight branch starts filled1 and crosses x-axis at3. Ticks-2,1,3.|
|7c96c401|q78132 solution: same open/filled1 as890; blue neighborhoods at-2 and3.|
|63e7a219|q48039 solution: same open/filled1 asf4; blue closed neighborhood around peak-2.|
|d8720531|q69782 solution: same open upper/filled lower at2 asd124; blue neighborhood around parabola minimum5.|
|90c2fbe9|q48082 solution anomaly: compared toc6, upper marker at2 is OPEN and lower marker on curve is FILLED. It visually shows a continuous curve at2 with an unrelated isolated upper open annotation; source prose says discontinuity at2. Blue neighborhood surrounds0. Raw preserved separately; normal rendered solution repairs to correct-option geometry.|
|e395863c|canonical e3567: reciprocal branches at0, left negative/right positive infinite; axes arrows and unit ticks(-2,-1,1,2), y ticks1,2,3,-1,-2,-3; no filled point at0.|

Original curve aesthetics are source evidence, not algebraic expressions. Curve paths alone cannot prove endpoint inclusion. The distinction is carried by separately transcribed marker predicates above and by source prose where points have unlabelled coordinates. Source solution anomaly90 is not merged into its correct-option graph recipe.

## 2. Generalized visual pattern

Cartesian graph with disconnected branches as applicable, open-circle exclusions, separately filled singleton values, optional vertical asymptote guides and source solution neighborhood highlighting. Easy graphs must show5 independently valid mathematical functions in one complete bank. Moderate/hard use one graph with three queried positions. The graph carries the decisive information; plot rating is heavy at every level.

## 3. Components and derived data

The script's G dictionary contains exact bounded piecewise-linear/rational surrogate realizations. Each segment has an exact open interval and symbolic expression; shared joined knots receive the function value. External ends at the viewport are clipped, not displayed as finite domain endpoints. Open branch ends, interior holes, filled values, and singular positions are separate components. Raw denominators are inspected recursively before simplifying expressions, preserving exclusions even for cancelled x/x. Plot sidecars contain exact transformed segments, intervals, raw excluded points, holes, poles, values, bounds, queried coordinates, tick values, renderer version and highlighting role.

Source y-scale is not recoverable; the surrogate ordinates are **authored schematic units**. They are used consistently in plotting and symbolic QA. They preserve source topology/sign/asymptote roles and the assessment, without pretending the unknown original smooth curve is uniquely identified. All original mathematical x positions are grounded in the named ticks or source prose. Whole graph banks are compared as complete functions/domain/value objects, not only by whether their local continuity predicates coincide.

## 4. Reusable rendering specification

Use Matplotlib only. Apply exact affine coordinate parameters to branch formulas, interval boundaries, point locations, contextual positions and all prompt/solution x-components. The renderer never resamples. Derive viewport from each original family's own extent, transformed with the same scale/shift; vertical bounds transform with ordinate offset. Never connect across a hole/jump/pole. Draw finite open ends independently of filled singleton values, and clip rational asymptotes outside the viewport. Red strokes, white open-ring centers, red filled values, grey dashed asymptote guide where source has one; omit dashed guide where source uses the y-axis as its pole. Black axis arrowheads are context, not curve traversal arrows. Source-derived optional blue marks show only the continuous queried neighborhoods.

Easy/moderate label queried integer coordinates. Authored hard labels only unit-spaced integer ticks and draws matching faint grid lines; its queried positions lie halfway between labels and require coordinate-scale reading. Half-integer targets are not labeled for the learner in the hard plot. Every relevant marker is unchanged in inclusion status under coordinate transformations. No mathematical area is filled.

Atomic writes use unique temporary PNG/JSON names. A cache hit requires both final PNG and matching sidecar. Old evidence assets are retained during QA; no active-reader cache pruning. The original exact asset is reused only for identity-coordinate observed replay. The normal q48082 solution uses the same repaired function as its correct answer; raw anomalous90 remains exact evidence with its own predicate interpretation.
