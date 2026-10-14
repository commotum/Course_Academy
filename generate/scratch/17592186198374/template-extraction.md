# Template extraction: four stages

Frozen math basis1356; preserved raw record is source.json. All public raw profiles parameterize a coherent external integrand scale c, simultaneously scaling every integral-stage RHS and every complete bank value. This is an evidence parameterization of historical displayed patterns, **not** an inference of original distractor intention. Normal defaults use different explicitly authored complete method banks.
## 1. Specific descriptions

### q-160433 — rational

Original prompt:

Use a change of variables to evaluate the double integral 

$$
{∬}_{D}\frac{(x+y)^{2}}{2x+y}\,dxdy,
$$

where $D$ is the quadrilateral region with vertices $(0,1),$ $(1,0),$ $(-1,3),$ and $(0,2).$

Original level: {':db/ident': ':question.difficulty/hard'}. Transform inferred from integrand: $u=x + y, v=2 x + y$. Forward inverse formulas: $x=- u + v, y=2 u - v$. Determinant inverse/forward: $-1$, $-1$. Bounds: `[1, 2, 1, 2]`. Exact integral: $\frac{7 \ln{\left(2 \right)}}{3}$.

Worked-solution sequence: common T map/formula introduction; Step1 integrand and inferred u/v; inverse-map definition; Step2 four individually substituted vertices followed by rectangle and plot; Step3 symbolic derivative matrix then numeric matrix then determinant; Step4 reciprocal determinant/noncritical-point prose; Step5 transformed integrand/symbolic absolute Jacobian, numeric absolute Jacobian, nested integral, separated product, primitive brackets, endpoint differences and final scalar. Rational includes a separate unit-Jacobian removal row and reverses separated factor order; its primitive row omits an equals sign. No missing existing source stage is inferred.

### q-160896 — shifted_polynomial

Original prompt:

Use a change of variables to evaluate the double integral

$∬_(D)(2x - 1)(x + y)^{2}dxdy$,

where $D$ is the quadrilateral region with vertices $(1, 0)$, $(2,-1)$, $(2, 2)$, and $(1, 3)$.

Original level: absent. Transform inferred from integrand: $u=2 x - 1, v=x + y$. Forward inverse formulas: $x=\frac{u}{2} + \frac{1}{2}, y=- \frac{u}{2} + v - \frac{1}{2}$. Determinant inverse/forward: $2$, $\frac{1}{2}$. Bounds: `[1, 3, 1, 4]`. Exact integral: $42$.

No worked solution or correct ref exists. Independent derivation: u=2x−1,v=x+y, |J|=1/2, rectangle [1,3]×[1,4], (1/2)·[(u²/2)]₁³·[(v³/3)]₁⁴=42. Completion is authored, not matched to missing evidence.

### q-160901 — sine

Original prompt:

Use a change of variables to evaluate the double integral 

$$
{∬}_{D}x\operatorname{sin}⁡(\pi (x+y))\,dxdy,
$$

where $D$ is the quadrilateral region with vertices $(0,0),$ $(1,-1),$ $(1,0),$ and $(0,1).$

Original level: {':db/ident': ':question.difficulty/hard'}. Transform inferred from integrand: $u=x, v=x + y$. Forward inverse formulas: $x=u, y=- u + v$. Determinant inverse/forward: $1$, $1$. Bounds: `[0, 1, 0, 1]`. Exact integral: $\frac{1}{\pi}$.

Worked-solution sequence: common T map/formula introduction; Step1 integrand and inferred u/v; inverse-map definition; Step2 four individually substituted vertices followed by rectangle and plot; Step3 symbolic derivative matrix then numeric matrix then determinant; Step4 reciprocal determinant/noncritical-point prose; Step5 transformed integrand/symbolic absolute Jacobian, numeric absolute Jacobian, nested integral, separated product, primitive brackets, endpoint differences and final scalar. No missing existing source stage is inferred.

### q-160904 — exponential

Original prompt:

Use a change of variables to evaluate the double integral 

$$
{∬}_{D}(\frac{x}{2}+y){e}^{x+3y}\,dxdy,
$$

where $D$ is the quadrilateral region with vertices $(8,-3),$  $(10,-4),$ $(16,-6),$ and $(14,-5).$

Original level: {':db/ident': ':question.difficulty/hard'}. Transform inferred from integrand: $u=\frac{x}{2} + y, v=x + 3 y$. Forward inverse formulas: $x=6 u - 2 v, y=- 2 u + v$. Determinant inverse/forward: $\frac{1}{2}$, $2$. Bounds: `[1, 2, -2, -1]`. Exact integral: $- \frac{3 - 3 e}{e^{2}}$.

Worked-solution sequence: common T map/formula introduction; Step1 integrand and inferred u/v; inverse-map definition; Step2 four individually substituted vertices followed by rectangle and plot; Step3 symbolic derivative matrix then numeric matrix then determinant; Step4 reciprocal determinant/noncritical-point prose; Step5 transformed integrand/symbolic absolute Jacobian, numeric absolute Jacobian, nested integral, separated product, primitive brackets, endpoint differences and final scalar. No missing existing source stage is inferred.

### q-160933 — exponential_square

Original prompt:

Use a change of variables to evaluate the double integral 

$$
{∬}_{D}(2x-y){e}^{(2x-y)^{2}}\,dxdy,
$$

where $D$ is the quadrilateral region with vertices $(2,3),$ $(4,7),$ $(4,6),$ and $(2,2).$

Original level: {':db/ident': ':question.difficulty/hard'}. Transform inferred from integrand: $u=x, v=2 x - y$. Forward inverse formulas: $x=u, y=2 u - v$. Determinant inverse/forward: $-1$, $-1$. Bounds: `[2, 4, 1, 2]`. Exact integral: $- e + e^{4}$.

Worked-solution sequence: common T map/formula introduction; Step1 integrand and inferred u/v; inverse-map definition; Step2 four individually substituted vertices followed by rectangle and plot; Step3 symbolic derivative matrix then numeric matrix then determinant; Step4 reciprocal determinant/noncritical-point prose; Step5 transformed integrand/symbolic absolute Jacobian, numeric absolute Jacobian, nested integral, separated product, primitive brackets, endpoint differences and final scalar. No missing existing source stage is inferred.

### q-160935 — cosine_square

Original prompt:

Use a change of variables to evaluate the double integral 

$$
{∬}_{D}({x}^{2}-{y}^{2})\operatorname{cos}⁡((x+y)^{2})\,dxdy,
$$

where $D$ is the quadrilateral region with vertices $(\frac{1}{2},-\frac{1}{2}),$ $(\frac{3}{2},-\frac{3}{2}),$ $(\frac{\pi +6}{4},\frac{\pi -6}{4}),$ and $(\frac{\pi +2}{4},\frac{\pi -2}{4}).$

Original level: {':db/ident': ':question.difficulty/hard'}. Transform inferred from integrand: $u=x - y, v=x + y$. Forward inverse formulas: $x=\frac{u}{2} + \frac{v}{2}, y=- \frac{u}{2} + \frac{v}{2}$. Determinant inverse/forward: $2$, $\frac{1}{2}$. Bounds: `[1, 3, 0, "pi/2"]`. Exact integral: $\sin{\left(\frac{\pi^{2}}{4} \right)}$.

Worked-solution sequence: common T map/formula introduction; Step1 integrand and inferred u/v; inverse-map definition; Step2 four individually substituted vertices followed by rectangle and plot; Step3 symbolic derivative matrix then numeric matrix then determinant; Step4 reciprocal determinant/noncritical-point prose; Step5 transformed integrand/symbolic absolute Jacobian, numeric absolute Jacobian, nested integral, separated product, primitive brackets, endpoint differences and final scalar. Cosine-square includes explicit difference-of-squares factorization both before choosing the transform and at the start of the final chain. No missing existing source stage is inferred.

## 2. General pattern

Infer the two affine components visible in the integrand, map the supplied four vertices through that inverse transformation to recover a rectangle, compute the reciprocal constant Jacobian and substitute the integrand. Evaluate a product of two elementary single-variable definite integrals. Preserve numerator/denominator and squared-inner-function structure. In the cosine family first factor x²−y²=(x−y)(x+y). All transforms are globally injective because their matrices have nonzero determinant; reciprocals use positive denominator bounds.

## 3. Complete component and bank mapping

Each table row is a complete displayed source value in its original owning field, with an exact symbolic interpretation and a parameterized raw scaling recipe c·value. Original-bank choice order is incidental; field membership and designation presence are not. Scalar distractor intention is unresolved unless the normal authored operations explicitly say otherwise. No arbitrary polynomial fit or unrelated numerical perturbation is used.

### q-160433

|Field / answer ID|Original display|Exact interpretation|Raw recipe|Original correct?|
|---|---|---|---|---|
|0 / 9c4b7867-a736-571c-ad31-eb780c69adfe|`\frac{7}{3}\ln (2)`|$\frac{7 \ln{\left(2 \right)}}{3}$|$c(\frac{7 \ln{\left(2 \right)}}{3})$; intention opaque|designation absent|
|0 / e7e6aaa2-58ff-59fb-907b-41a8a66271bc|`\frac{1}{9}\ln (2)`|$\frac{\ln{\left(2 \right)}}{9}$|$c(\frac{\ln{\left(2 \right)}}{9})$; intention opaque|designation absent|
|0 / f6058698-95f6-55c0-a7c0-70eb158629d5|`\frac{1}{3}\ln (2)`|$\frac{\ln{\left(2 \right)}}{3}$|$c(\frac{\ln{\left(2 \right)}}{3})$; intention opaque|designation absent|
|0 / fba2da32-6e0e-59e1-b78b-93358a40bc01|`2\ln (2)`|$2 \ln{\left(2 \right)}$|$c(2 \ln{\left(2 \right)})$; intention opaque|designation absent|
|0 / 36fd6d06-849b-5ef7-9d1f-0d446195d0d7|`\frac{2}{3}\ln (2)`|$\frac{2 \ln{\left(2 \right)}}{3}$|$c(\frac{2 \ln{\left(2 \right)}}{3})$; intention opaque|designation absent|
|1 / 668e96f5-c245-5783-9d06-593c4e78f8fe|`2\operatorname{ln}⁡(2)`|$2 \ln{\left(2 \right)}$|$c(2 \ln{\left(2 \right)})$; intention opaque|no|
|1 / a8e42901-d026-5c3b-99b7-1e76badd9d24|`\frac{7}{3}\operatorname{ln}⁡(2)`|$\frac{7 \ln{\left(2 \right)}}{3}$|$c(\frac{7 \ln{\left(2 \right)}}{3})$; intention opaque|yes|
|1 / eb0cffb4-d3f7-53d5-acbb-196bad09a042|`\frac{1}{3}\operatorname{ln}⁡(2)`|$\frac{\ln{\left(2 \right)}}{3}$|$c(\frac{\ln{\left(2 \right)}}{3})$; intention opaque|no|
|1 / fe02fb4f-78ab-561d-b73f-99e66adb3595|`\frac{1}{9}\operatorname{ln}⁡(2)`|$\frac{\ln{\left(2 \right)}}{9}$|$c(\frac{\ln{\left(2 \right)}}{9})$; intention opaque|no|
|1 / 909ee938-9aa9-5943-b10d-13855833836d|`\frac{2}{3}\operatorname{ln}⁡(2)`|$\frac{2 \ln{\left(2 \right)}}{3}$|$c(\frac{2 \ln{\left(2 \right)}}{3})$; intention opaque|no|

### q-160896

|Field / answer ID|Original display|Exact interpretation|Raw recipe|Original correct?|
|---|---|---|---|---|
|0 / bdb97453-dd87-51d7-8e74-71739c98b4ea|`42`|$42$|$c(42)$; intention opaque|designation absent|
|0 / fd33a36b-2892-58b1-b178-7ad6c33b02fb|`84`|$84$|$c(84)$; intention opaque|designation absent|
|0 / 1735d3c0-fabb-5e13-bc9b-d22554e2311f|`64`|$64$|$c(64)$; intention opaque|designation absent|
|0 / 6245bb7a-687f-508b-98d6-d993799bae19|`11`|$11$|$c(11)$; intention opaque|designation absent|
|0 / 7bd58517-695b-569c-bab2-38a084aebb0b|`21`|$21$|$c(21)$; intention opaque|designation absent|

### q-160901

|Field / answer ID|Original display|Exact interpretation|Raw recipe|Original correct?|
|---|---|---|---|---|
|0 / 790e8e07-7e51-507f-8184-c6e269fb8de8|`2`|$2$|$c(2)$; intention opaque|no|
|0 / e4fff2f8-8d95-5435-b189-10210d784148|`\pi `|$\pi$|$c(\pi)$; intention opaque|no|
|0 / f14b4067-73c1-5f25-863f-0a6233383ceb|`\frac{3}{2\pi }`|$\frac{3}{2 \pi}$|$c(\frac{3}{2 \pi})$; intention opaque|no|
|0 / 39736917-e30f-55c3-8963-53bb38f33eca|`1`|$1$|$c(1)$; intention opaque|no|
|0 / afb3f4bf-6797-5fe7-8bba-23659e124fb6|`\frac{1}{\pi }`|$\frac{1}{\pi}$|$c(\frac{1}{\pi})$; intention opaque|yes|

### q-160904

|Field / answer ID|Original display|Exact interpretation|Raw recipe|Original correct?|
|---|---|---|---|---|
|0 / 052ff79b-a4d5-5349-8d70-9ce279b39433|`\frac{3(e-1)}{{e}^{2}}`|$\frac{-3 + 3 e}{e^{2}}$|$c(\frac{-3 + 3 e}{e^{2}})$; intention opaque|yes|
|0 / 9a53dd9c-e7a3-5dc4-bae1-0801e0278182|`\frac{1}{{e}^{2}}`|$e^{-2}$|$c(e^{-2})$; intention opaque|no|
|0 / 72671ebe-486b-51fc-984c-4bfe215446a7|`\frac{2e-1}{{e}^{2}}`|$\frac{-1 + 2 e}{e^{2}}$|$c(\frac{-1 + 2 e}{e^{2}})$; intention opaque|no|
|0 / bf88254b-b546-5332-a887-c187097fd6b7|`e(1-e)`|$e \left(1 - e\right)$|$c(e \left(1 - e\right))$; intention opaque|no|
|0 / 8766f1a6-856d-5e0d-ba8b-8c9e5b3b4e75|`\frac{1}{e}`|$e^{-1}$|$c(e^{-1})$; intention opaque|no|

### q-160933

|Field / answer ID|Original display|Exact interpretation|Raw recipe|Original correct?|
|---|---|---|---|---|
|0 / 57c94a92-0e8a-5442-aac8-2dac0c97e4c0|`{e}^{4}-e`|$- e + e^{4}$|$c(- e + e^{4})$; intention opaque|yes|
|0 / e62b8224-ac2c-5230-a4e3-89a27786d90f|`{e}^{3}-{e}^{2}`|$- e^{2} + e^{3}$|$c(- e^{2} + e^{3})$; intention opaque|no|
|0 / a9f5e559-02f0-5ffc-bdc6-ee1961e2eb8f|`{e}^{4}-2{e}^{2}+3`|$- 2 e^{2} + 3 + e^{4}$|$c(- 2 e^{2} + 3 + e^{4})$; intention opaque|no|
|0 / e96d4bb8-7a5d-5e91-bb81-d0ceb7569853|`4{e}^{2}`|$4 e^{2}$|$c(4 e^{2})$; intention opaque|no|
|0 / 1d73e77b-0e51-53da-a682-8364ea85c350|`{e}^{3}-2e+1`|$- 2 e + 1 + e^{3}$|$c(- 2 e + 1 + e^{3})$; intention opaque|no|

### q-160935

|Field / answer ID|Original display|Exact interpretation|Raw recipe|Original correct?|
|---|---|---|---|---|
|0 / 39df1efb-3147-55da-a745-396b77787150|`\operatorname{sin}⁡(\frac{\pi }{\sqrt{2}})`|$\sin{\left(\frac{\sqrt{2} \pi}{2} \right)}$|$c(\sin{\left(\frac{\sqrt{2} \pi}{2} \right)})$; intention opaque|no|
|0 / 4d0d118f-30ca-5b55-958e-4c7337aa1660|`\operatorname{sin}⁡(\frac{{\pi }^{2}}{4})`|$\sin{\left(\frac{\pi^{2}}{4} \right)}$|$c(\sin{\left(\frac{\pi^{2}}{4} \right)})$; intention opaque|yes|
|0 / 786531b9-92b5-5eca-b7c1-c382b290c929|`1`|$1$|$c(1)$; intention opaque|no|
|0 / 5a55e0ff-719d-5e62-b93c-61f5d304f641|`2\operatorname{sin}⁡(\frac{{\pi }^{2}}{2})`|$2 \sin{\left(\frac{\pi^{2}}{2} \right)}$|$c(2 \sin{\left(\frac{\pi^{2}}{2} \right)})$; intention opaque|no|
|0 / 988d3c2d-5618-5c22-9b72-aa00689b5dcc|`\frac{\sqrt{2}}{2}`|$\frac{\sqrt{2}}{2}$|$c(\frac{\sqrt{2}}{2})$; intention opaque|no|

## 4. Reusable masks, fixed/variable components and guards

Fixed shared prose is taken from the captured five-step sources. Normal masks include complete integrands, complete affine expressions and coordinate components, full matrices and each ordered primitive component. Numeric factors always have visible multiplication or grouped signs. Do not replace variable substrings inside TeX commands. Raw masks retain exact existing prose and chains at c=1, including every omission. Raw fields preserve absent difficulty/solution/correct refs. Normal masks repair presentation and add endpoint detail as separately disclosed additions.

Normal family table:

|Family|Integrand after substitution (without external c)|u primitive|v primitive|Fixed demand / allowable variation|
|---|---|---|---|---|
|polynomial|$u v^{2}$|$\frac{u^{2}}{2}$|$\frac{v^{3}}{3}$|easy; guards in validate_parameters and documented sections|
|shifted_polynomial|$u v^{2}$|$\frac{u^{2}}{2}$|$\frac{v^{3}}{3}$|moderate; guards in validate_parameters and documented sections|
|rational|$\frac{u^{2}}{v}$|$\frac{u^{3}}{3}$|$\ln{\left(v \right)}$|hard; guards in validate_parameters and documented sections|
|sine|$u \sin{\left(\pi v \right)}$|$\frac{u^{2}}{2}$|$- \frac{\cos{\left(\pi v \right)}}{\pi}$|hard; guards in validate_parameters and documented sections|
|exponential|$u e^{v}$|$\frac{u^{2}}{2}$|$e^{v}$|hard; guards in validate_parameters and documented sections|
|exponential_square|$v e^{v^{2}}$|$u$|$\frac{e^{v^{2}}}{2}$|hard; guards in validate_parameters and documented sections|
|cosine_square|$u v \cos{\left(v^{2} \right)}$|$\frac{u^{2}}{2}$|$\frac{\sin{\left(v^{2} \right)}}{2}$|hard; guards in validate_parameters and documented sections|

All explicit and sampled numeric parameters are finite real exact values. Coefficient/shift magnitudes≤5; bound magnitudes≤8; positive integer external scale c=1..3. Easy a∈{1,2,3}, b∈{−2,−1,1,2}, v=y, no shift, u lower≥1,v lower≥0. Moderate a∈{2,3,4}, d∈{1,2}, u=ax+h with h∈{−3,−2,−1,1,2,3}, v=x+dy, positive lower bounds. Hard rational u=x+y,v=mx+y with m=2..4 and both lower bounds positive. Hard sine u=x,v=mx+y,m=1..3, v bounds0..1 preserve familiar frequency π. Hard exponential u=x/2+y or x+y, v=x+dy,d=2..4 with nonsingular matrix. Hard exponential-square u=x,v=mx−y,m=1..3, v lower≥1. Hard cosine-square uses u=x−y,v=x+y and v upper π/2,π/3 orπ/4, retaining exactly the observed square/chain primitive. Bounds are strictly ordered integers, except the explicitly supported cosine-square v upper bounds. No degeneracy removes a required level component.

All normal profiles have five complete choices, selected as one family bank before sampling. Their named operations and complete formulas are in bank(); every option is independently re-evaluated from the actual prompt in validate.py. These are authored method operations, not claims about the original scalar distractors. Entire instance rejection, never first-valid pool replacement.

Meaningful finite sampler domains: easy has 3 leading coefficients×4 shear coefficients×4 u lower bounds×3 u widths×2 v lower bounds×3 v upper bounds×3 scales=2592 candidate tasks; moderate has 3 leading coefficients×2 shear coefficients×6 nonzero shifts×4 u lower bounds×3 u widths×2 v lower bounds×3 v upper bounds×3 scales=7776. Both banks are collision-free throughout these sampled domains. Hard serves all five families; source-sized coefficient forms and meaningful interval changes supply hundreds of candidates. A sampler uses exact whole-bank rejection for any collision. Fingerprints include actual integrand and domain vertices and family, exclude bank/order/aliases; coefficient and bound changes affect the assessed transform/evaluation. A coefficient/bank alias or seed shuffle never inflates counts.

## Source anomalies and separate corrections

q-160433 has duplicate same-key fields; original widget contains one complete bank. Captured legacy field lacks correct ref, and decoded byte checks confirm its TeX command prefixes contain a single backslash, with no double-escape anomaly (source-format-anomalies.json). It remains raw ineligible evidence. Updated captured field gives verified 7ln2/3. q-160896 lacks rating/solution/designation; no original matched designation or solution is claimed. Raw underscore-parenthesis integral notation remains exact. Completed normal question derives42 and uses the observed radio response shape; its authored profile uses method distractors.

Raw solution domain braces are unescaped TeX set braces; normal uses visible escaped braces. The rational raw primitive-product row lacks equals, retained exactly only in raw. Some raw completed primitive products end with a leftover d v after all integrals have been evaluated; normal omits this differential. These are presentation/notation repairs, not algebraic corrections. No source correct scalar is mathematically wrong. All normal outputs undergo balanced braces/delimiters and C0-byte checks. Existing raw solutions are5/5 exact, normal0/5 exact strings because of notation/endpoint/inverse additions; shared prose and actual source operation order are checked separately, never merged into exact denominators.
