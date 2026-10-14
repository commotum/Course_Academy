# Four-stage plot extraction and specification

## 1. Original native observations

All four original PNGs were visually inspected at their full 360x304 native size, with transparencies on the tool's white background. Exact copies and hashes are retained in original-plots/ and provenance.json. Source-geometry.json gives independently transcribed labels and approximate pixel coordinates; it does not infer unlabeled coordinate values.

q-213914: black arrowed axes; blue steep rising l1 and red shallow falling l2. Red marker lies on y axis and has label2. Both lines meet at this marker, consistent with given y=3x+2. Thus required l2 passes through (0,2), giving y=-x/3+2. Unit-style small ticks have no other numeric labels. No right-angle symbol appears.

q-44604: blue shallow rising l1 passes through origin. Red steep falling l2 has a marker at the intersection of dashed guides labelled -4 on x axis and10 on y axis. The geometry supplies (-4,10), so y=-2x+2. The lines cross just right of the y axis. The source supplies no independently labelled red intercept: its value2 is derived rather than guessed from pixels. No right-angle marker.

q-237193: blue steep falling l1, red shallow rising l2; a red marker linked by dashed guides to x=4 and y=2. They cross left of the y axis. Source line equation supplies -4, not a pixel measurement. m=1/4 and b=1. No right-angle marker.

q-44337: blue rising l1, red falling l2, marker on y axis labelled6; source equation y=2x-1 supplies slope2. The crossing is to the right of the y axis. Derived l2 is y=-x/2+6. Tiny unlabeled ticks are not independent coordinates. No right-angle marker.

These source plots are schematic and may use unequal scaling; the labelled values and supplied equations establish coordinates. No unlabelled intercept or crossing coordinate is read as an exact value. Source marker and crossing signs agree with the recovered mathematical lines.

## 2. Generalized visual pattern

The diagram identifies l1 and l2 in a Cartesian plane, provides the required intercept or point, and shows their crossing. The equation in the prose supplies the known slope. Easy graphs use a marked y-intercept; moderate graphs use a non-axis marked point with two labelled dashed guides. Source colours, names and informational roles remain fixed.

## 3. Components and dependencies

Black x/y axes with positive arrowheads, blue l1: y=ax+c, red l2: y=(-1/a)x+b, red marked point (u,v); labels l1/l2 and x/y. Non-axis layouts contain dashed projection guides to the labelled u and v coordinates. Intercept layouts mark (0,b) with a y label. No right-angle symbol is added because none is present in the sources. No extra numeric ticks allow a shortcut to replace the supplied slope operation. All source plot roles are prompt-only; there are no plot choices or solution plots.

## 4. Renderer specification

Matplotlib Agg with Figure/Canvas (no pyplot global figures). Native PNG576x504, white background, equal coordinate units so generated perpendicular geometry is actually perpendicular. Bounds include origin, both y-intercepts, labelled point and derived line crossing, with2.5-unit margins. Equal x/y extents keep the angle legible; a labelled point is never clipped. Line labels are placed on visible interior line points away from their crossing. Labels retain the exact signed coordinates; guide orientation changes with signs.

Every renderer receives exact instance values before numerical conversion. Sidecars store actual bounds, renderer version, exact equations/point, axes transform, label bounding boxes and native size. Validator reads the actual PNG pixels to verify the red marker, multiple blue/red line points, expected transform and visible label boxes; it rejects clipping or fewer than7 native pixels per unit. The review includes signed intercepts, positive/negative slopes and all point quadrants. All eight normal graph examples were inspected at full native size; label placement was improved from four to39 interior candidates to prevent fallback labels sitting on the crossing.

Anchor evidence profiles reuse exact copied original assets while preserving their original Markdown path for byte fidelity. Changed parameters use the same mathematical renderer as defaults. Render outputs use parameter-derived names, unique tempfile names and atomic os.replace for PNG and JSON; cache reuse requires both. Four fresh concurrent renders cover identical and different parameter sets, exact sidecar/input correspondence and absence of private tempfile leakage. No image model, direct SVG, external plotting service or shared cache mutation.
