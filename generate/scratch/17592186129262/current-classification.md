# Current classification and extraction addendum — basis 2700

Database math, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. All nine current practice records were read in one Pull, retaining all fields, bank choices, correct values, solutions and plot references in reference/replenishment/initial/kp.edn. The basis1356 source remains immutable replay evidence.

| Band | Current source templates | Field contract | New-plot rating |
|---|---|---|---|
|Unrated, authored easy support|xy,y/x (q-160373)|one radio, five scalar choices; source incomplete|light authored rectangle|
|Moderate|5x-3y,4x-2y (q-160864); 3x-y,x-3y (q-160852); 4x-3y,3x-2y (q-160857); 2x-y,x-2y (q-160846); 3x-2y,2x-3y (q-160853)|one radio, five scalar choices each|light rectangle|
|Hard|x²y,xy (q-160654); xy,x/y² (q-161869); exp(x)y,2y (q-160638)|one radio, five logarithmic scalar choices each|light rectangle|

This is one easy-support mask, five moderate masks, three hard masks. The six historical supported masks retain their parameterized prompt/solution components and complete source banks. Current q-160864 now has its authoritative single field and complete correct designation. Source banks and the five-stage method remain the same. The old malformed duplicate field survives only as frozen replay evidence.

New q-160846 supplies y=2x-1, y=2x-3, x=2y+1, x=2y+4. It asks for scalar area 2 after choosing u=2x-y,v=x-2y, rectangle [1,3]×[1,4], determinant -3, inverse -1/3, then 1/3·2·3. Its exact bank is [1/3,3,1/2,2,4]. At a=1,b=3,c=1,d=4, complete expression recipes in this observed order are [1/|J|,h,1/w,A,wh-A]. Distractor intent of 1/w and wh-A is unresolved; these literal-expression profiles are evidence only.

New q-160853 supplies 2y=3x-2, 2y=3x-7, 2x=3y+1, 2x=3y+4. It chooses u=3x-2y,v=2x-3y, maps [2,7]×[1,4], computes J=-5 and inverse -1/5, then A=3. Its exact bank [1/3,3,1/2,2,5] is reproduced by [1/h,A,1/a,a,w] at these parameters; opaque distractor intentions remain unresolved. This is a separate mask from changing only a rectangle bound.

New q-160638 supplies y=5/e^x,y=12/e^x,2y-1=0,2y-5=0 in the first quadrant. Choosing u=e^xy,v=2y maps [5,12]×[1,5]; J=2u, inverse 1/(2u), so A=(d-c)/2 ln(b/a)=2ln(12/5). The bank [2ln(5/12),ln(5/12),ln(12/5),2ln(12/5),2ln60] maps exactly to [-A,-L,L,A,(d-c)/2 ln(ab)]. The first four reflect sign/width factors; the final profile omits the logarithmic subtraction. Inversion x=ln(2u/v),y=v/2 requires 2a>d for an entirely first-quadrant region. Unlike the existing nonlinear masks, this introduces an exponential boundary family; it is not silently pooled with their sampler.

The three added masks have exact complete-bank source evidence and independent mathematical verification, and their valid source instances count in inventory. Parameterized generation remains explicitly bounded to the six already validated masks; no unsupported new-family sampler is claimed. All three difficulty levels are supported by those masks, with no requested count limitation. Original worked solutions use the same ordered five stages: discover transformation, substitute four boundaries and show rectangle, compute forward determinant, reciprocate, integrate absolute inverse and collect area. All changed-boundary references in generated output are validated together.

q-160373 remains excluded as unrated/incomplete. q-160654 remains excluded because its upper xy=3 boundary maps incorrectly to v=2 in the source solution; no source or learner history is edited. Its correct area 2ln2 does not excuse the faulty teaching step.

The three added source plots carry the same solution-only rectangle role: black u/v axes, colored horizontal bounds, dashed vertical guides, pale-blue fill and Delta. Their exact current source assets are retained. No new plots are needed to count these existing source questions. Generated variants use the established rectangle-v4 Matplotlib renderer and publish verified PNG bytes through images/<sha-prefix>/<sha>.png. See plot-spec.md for rendering components and geometry validation.
