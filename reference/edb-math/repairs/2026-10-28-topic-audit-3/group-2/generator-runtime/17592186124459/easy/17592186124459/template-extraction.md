# Four-stage template extraction

## 1. Specific originals

- **cosxy:** `cos x+x²y`, point (1,1), increase; i/j answers, no captured difficulty, solution or correct key. Gradient `(2-sin(1),1)`.
- **quadratic:** `x²+3xy+2y²`, point (2,1), increase; formal two held partials, polynomial partial row `(2x+3y,3x+4y)`, individually substituted row, final `(7,10)`, same vector in final prose.
- **exp:** `x ln y+y e^x-xy`, point (-1,1), increase; formal partials, three-term partial components, individually substituted terms including `-(-1)`, reduction `(e^-1-1,e^-1)`, conclusion. Wrong evaluation label `(1,1)` retained in raw.
- **trig_product:** `3x² sin y-y cos x`, point (0,1); formal partials, partial row `(y sin x+6x sin y,3x² cos y-cos x)`, substituted zero-factor terms retained, final `-j`, conclusion.
- **linear_sin:** `y²+sin(2pi x+pi z)`, point (1,1,2); formal three partials, partial row, component substitution, separate evaluation `cos(4pi)` row, reduced `(2pi,2,pi)`, conclusion.
- **mixed_sin:** `sin(pi x+y)+3z²x`, point (1,0,1); formal three partials, `(pi cos(...)+3z²,cos(...),6xz)`, component substitution, separate `cos(pi)` evaluation row, final `(-pi+3,-1,6)`, conclusion.

## 2. Shared patterns

Differentiate the actual multivariate function holding the other coordinates constant, substitute the actual point into every partial, then choose the gradient direction for increase or the opposite direction for decrease. Observed prompts ask **a direction**, so every nonzero positive parallel vector is eligible; unit norm is not required. Normal complete banks reject any extra positive-parallel answer, even with unequal component values. Authored hard explicitly asks a unit direction, so direction and norm both determine eligibility.

## 3. Original complete banks and recipes

Every bank contains five choices and is reproduced through the public `profile='source'` API. `source-cases.json` binds every original to its parameter recipe. Exact raw values and original correct refs are in source.json; choices below follow source capture order. Let G be the evaluated gradient, U,V,W the point, A,B,C function coefficients, E=exp(U), R=exp(-U), P=pi.

| Family | Full source bank recipe, in original capture order | Correct index | Interpretation |
|---|---|---|---|
|cosxy|`(-A sin U,2BUV)`, `(-2BUV,-BU²)`, G, -G, `(2BUV,BU²)`|2|omit product/power derivative, reverse orientation, omit trig contribution; first choice mixes two mistaken components|
|quadratic|`(V,-U)`, `(U,V)`, G, `(2U,V)`, `(B,-(A+2C))`|2|opaque historical vector patterns; exact numerical fit does not recover error intent|
|linear_sin|-G, `(B cos(theta),2AV,C cos(theta))`, `(-CP,-AV,CP)`, `(CP,2AV,CP)`, G|4|some omitted pi/chain factors; third pattern compound historical structure; evidence-only|
|mixed_sin|`(BW²,-AP,BUW)`, `(Gx,AP,BUW)`, `(BW²,0,Gz)`, G, `(A cos(theta)+BW²,cos(theta),Gz)`|3|omitted trig contribution/chain factors and missing z power factor; compound wrong y/z choices|
|exp|`(A ln V+BVE+CV,BE+CU)`, `(A ln V+BVR-CV,AU/V+BR-CU)`, `(Gx+2CV,Gy)`, G, `(A ln V+BVR+CV,BR+CU)`|3|sign of -xy, missing ln term in y, reversed exponential input, compounds|
|trig_product|G,-G,`(B,B)`,`(2B,-B)`,`(B,-B)`|0|axis distractor patterns under original U=0; numerical reproduction without recovered error intent|

All source profiles are conservatively **evidence-only**, even those with defensible operations, to keep raw omission/label evidence separate from completed practice. No profile returns a copied source payload: complete function/point/row slots and full parameterized bank operations render the originals and changed inputs.

Normal method banks are complete authored profiles, not replacements of individual invalid options. Compute G, then -G, then the three family-specific operations in method_bank. cosxy omits the trig term, omits product term, or substitutes the x-product derivative for the y derivative. Quadratic omits one cross term at a time or omits both power factors. linear_sin omits the x chain multiplier, y power factor, or z pi multiplier. mixed_sin omits x trig contribution, z power factor, or x pi multiplier. exp reverses cross-term sign in x, omits ln term in y, or reverses exponential input in both components. trig_product has two complete authored profiles chosen before random parameters. axis_method fixes x=0 and uses: G, -G, omission of x from the x-product derivative, swapped components, and wrongly retaining cos x when differentiating -B y cos x. nonaxis_method uses x=+/-1 and: G, -G, omission of the -B y cos x contribution to the x partial, reversal of the -B cos x sign in the y partial, and swapped components. Explicit profile/input mismatches are rejected. Sign applies to the entire bank for a decrease prompt. Each whole instance is rejected if any required direction is zero, duplicate, or additionally eligible. In direction-only banks, positive-parallel equivalence is checked for EVERY pair, including two wrong options; checking only eligibility against the correct answer misses redundant wrong directions. Explicit unit banks compare full vector values so their distinct normalization errors remain distinct. No first-valid distractor pool.

Hard bank: normalized G, opposite normalized G, unnormalized G, G divided by norm squared, and normalized vector obtained by dropping the x log-inner power factor. Guards reject collisions/extra eligible entries. Magnitude distractors are valid here because the prompt explicitly requests unit direction.

## 4. Reusable masks and calculations

Source prompts mask entire function and point components. Each distinct source solution masks entire aligned RHS rows and the final prose vector; source sentences and row sequence stay fixed. Nothing replaces isolated symbols across basis labels or unrelated prose. components constructs the formal held-partial block, symbolic component expressions, individually substituted expressions, separate trig-phase row where observed, reduced vector and conclusion. Source exp retains its legacy point slot; normal exp corrects it. Normal decrease computes G by the same source chain and states -G in the conclusion, without asking for maximum rate.

Hard adds the canonical chain operand `1/(x^a y^b z^c)` times each inner held derivative, then cancellation to `(a/x,b/y,c/z)`, substitution and reduction, followed by the lesson's unit-gradient formula, component squared-norm calculation and normalized conclusion.

Content identity includes actual prompt, fixed solution, full displayed bank, correct displayed value, level and version. It excludes seed/choice order/profile alias. Mathematical identity excludes bank/profile/layout; the oriented gradient is reduced modulo every common positive magnitude. Function/point arithmetic context has a separate parameter fingerprint and is not counted as another direction. At trig-product U=0, A, B's positive magnitude and V cannot change the axis direction, so they do not inflate mathematical tasks. Hard preserves the unit response demand. A finite source-axis task family is acknowledged rather than claimed infinite through incidental coefficient changes.

No practice source contains a plot. The lesson's theorem illustration was inspected: blue gradient, red unit direction, angle theta and dashed projection. It informs direction/orientation only and is not reused as a generated question asset. Plot extraction/generation rating none.
