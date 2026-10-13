# Template extraction

## 1. Specific observations

Every prompt supplies A in polar notation together with A's Cartesian coordinates, and B's radius/angle in terms of that information. All radii are positive. The familiar angles use multiples of pi/6, pi/4 or pi/3. Source coordinate radicals are sqrt(2), sqrt(3), sqrt(5), sqrt(10); axis points and rational target radii also occur. No angle identity, diagram reading, arbitrary inverse-trigonometric evaluation or unknown-angle system is requested.

q-40803: A=(sqrt(10),sqrt(10)), A angle pi/4; B=(2r,pi/3); correct (2sqrt(5),2sqrt(15)). No key/solution/rating.
q-40806: A=(sqrt(2),-sqrt(2)), radius 2; B=(1,theta-pi/4); correct (0,-1). No key/solution/rating.
q-120455: A=(-3,sqrt(3)), angle 5pi/6; B radius r², angle 11pi/6; radius sqrt(12) retained, R=12, answer (6sqrt(3),-6).
q-120468: A=(-sqrt(3),-1), radius2; reference pi/6 and third quadrant give 7pi/6; add pi/3, R=4; axis answer (0,-4).
q-276803: A=(sqrt(3),1), angle pi/6; R=r/3=2/3; answer (-sqrt(3)/3,1/3), two scalar blanks.
q-276807: A=(2sqrt(3),2), angle pi/6; R=2r=8; answer (-4sqrt(3),-4), two scalar blanks.
q-276838: A=(5,0); reference angle0, axis; add pi/6, R=5; answer (5sqrt(3)/2,5/2), two scalar blanks.
q-40804: A=(-sqrt(5),sqrt(5)), angle3pi/4; radius sqrt(10) retained, R=r²=10, B angle4pi/3; answer(-5,-5sqrt(3)).
q-40826: A=(-1,-1), radius sqrt(2), third-quadrant angle5pi/4; add pi, R=8, retain9pi/4 then reducepi/4; answer(4sqrt(2),4sqrt(2)).
q-86619: A=(3sqrt(2),3sqrt(2)), anglepi/4; squared-component sum18+18 then36 then radius6; R=r/2=3, B angle5pi/6; answer(-3sqrt(3)/2,3/2).

## 2. Shared pattern and purpose

Recover the missing polar component from A, evaluate the supplied relationship for B, and apply x=R cos(theta_B), y=R sin(theta_B). Each solution retains the source's common conversion sentences, coordinate formula, separate x and y calculations and final Cartesian conclusion. This is the assessed point-information skill; changing the nature of the missing component changes family, not a within-family progression.

## 3. Component and choice mapping

source-cases.json maps every practice ID to template, exact parameters and complete raw profile. masks.json contains every original prompt/solution mathematical component and every original answer value, grouped by original owned field. build_masks.py records each scoped substitution's degree: A-coordinate coefficients scale by s, squared radicands by s²; B-coordinate/radius coefficients scale by s except square-radius families, where they scale by s². Angles and known radial factors stay fixed. Whole source banks use homogeneous whole-value scaling by the B scale. This operation exactly reconstructs all original values at s=1 and permits changed-parameter evidence, but does not recover historical distractor intentions. All seven historical radio banks are opaque evidence-only, including inferred-key completions. There is no promoted polynomial fit or answer lookup.

Each source bank remains indivisible. Source option count is five; every option and present designation is compared one-to-one, and every mathematical value is independently parsed. Missing correct designations are derived from printed data for completed evidence but excluded from matched-original-key counts. Raw attribute absence is checked independently.

Normal radio defaults select one complete method-derived bank before parameters. Radius bank: correct; exchange cos/sin assignments; omit radial scale or square; reverse x sign; reverse y sign. Angle-offset bank: correct; omit offset; reverse offset direction; reverse target ray; exchange coordinate assignments. For a pi offset the reverse direction/exchange operations collide with the correct diagonal point; its separately specified complete bank uses correct, target radius with original angle (omit offset), A radius with target angle (use the wrong point's radius), reverse x sign, and reverse y sign. Entire bank collisions reject the instance. No wrong diagnosis appears in learner text.

## 4. Reusable masks, bounds and authored scope

Moderate source-shaped instances use positive integer s=1..8; hard instances use s=1..16. The hard extension changes only known radii/coordinate coefficients (A components at most 16sqrt(3), B radii at most 128); the familiar reference-angle ratio, quadrant, one offset and exact trig workload remain fixed. A's two Cartesian components and supplied explicit A/B radii change together; square-radius B values scale by s². The source arithmetic operation count and ordered stages remain fixed. Blank field order/shape remain source-specific. Normal masks also parameterize the final prose conclusion and every intermediate polar tuple. Missing solutions use full radius/reference-angle, relationship substitution and separate coordinate formula/substitution/trig-factor/reduction stages.

Easy is an authored level: A=(a,0), A=(r,0), B=(cr,b), a=1..12, c=2..5, b in {pi/6,pi/3,2pi/3,5pi/6,7pi/6,4pi/3,5pi/3,11pi/6}. Every easy task recovers radius from an axis point, applies one nonunit positive scale and evaluates two familiar nonzero trig values. Radio and coordinate-blank layouts are presentation peers and deduplicate to the same task.

Moderate retains observed radius inference with nonaxis coordinates and one supplied multiply/divide/square operation, plus the separately observed axis-angle-offset template. Source labels are retained; they are not claims of a uniform historical cognitive rubric. Within each template workload is constant. q-40803 receives an authored moderate assignment because it has the same nonaxis radius/relation/conversion sequence. Its opaque bank remains evidence.

Hard retains reference-angle evaluation at familiar exact ratios, nonaxis quadrant selection, one supplied angle offset, then Cartesian conversion. q-40806 receives an authored hard assignment from the two rated hard peers. It needs only the familiar fourth-quadrant pi/4 angle and subtracting pi/4; no angle-sum identity or additional mathematical branch is introduced. Each hard source-shaped variation has identical stages within its family.

Curriculum anchors are frozen topic 936 and canonical e-5385. Ordered route is traversed from activity/first-step via step/next: Introduction → direct polar conversion → radius/angle description → this KP → diagram conversion. The introduction and predecessor examples establish familiar-angle sine/cosine conversion; the canonical establishes recovering A's radius and applying B's radial relationship. The next diagram KP is outside this generator. No plot or rotation-identity extension is added.
