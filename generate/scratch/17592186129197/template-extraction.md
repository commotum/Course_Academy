# Four-stage template extraction

Source wrapper: math/basis1356/lineage01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. Eight complete field-owned banks across seven practice questions; source-specific decoded strings remain in source.json and review.md.

## 1. Specific observed instances

### q-38374

Unit shear u=x−y,v=y; unshifted upward parabola to horizontal cap. Five rational/integer/radical scalars; correct/solution/difficulty all absent.

Using the change of variables

$u = x - y, v = y$,
calculate the area of the finite region $D$ bounded by the curve $(x - y)^{2} - y = 0$ and the line $y = 1$.

### q-82874

Sum/difference map determinant−2; quartic vs y=0 becomes v=u⁴ and v=u, intersections0,1; primitive u²/2−u⁵/5 and external1/2. Source factorization error explicitly retained as raw.

Using the change of variables 

$$
u=x+y,\,v=x-y,
$$

calculate the area of the finite region $D$ bounded by the curve $(x+y)^{4}-x+y=0$ and  the line $y=0.$

### q-160885

u=y+2x,v=y−2x; determinant4; two unit lower lines and y²−4x²=4 become u=v=1 and uv=4. Three vertices, logarithmic primitive4lnu−u, external1/4.

Using the change of variables 

$$
u=y+2x,\,v=y-2x,
$$

calculate the area of the finite region $D$ bounded by the lines $y+2x=1,$ $y-2x=1$ and the curve ${y}^{2}-4{x}^{2}=4.$

### q-82878

u=x−y,v=y+1; determinant1; downward v=3−u², bottomv=1, endpoints±√2. Explicit four evaluated endpoint components in source; incorrect inverse prose retained as raw.

Using the change of variables 

$$
u=x-y,\,v=y+1,
$$

calculate the area of the finite region $D$ bounded by the curve $(x-y)^{2}+y=2$ and the line $y=0.$

### q-83943

u=x−2y,v=y; determinant1; lower v=u²+2, topv=3, endpoints±1; width1−u², primitiveu−u³/3, collected2−2/3.

Using the change of variables 

$$
u=x-2y,\,v=y,
$$

calculate the area of the finite region $D$ bounded by the curve $y-(x-2y)^{2}=2$ and the line $y=3.$

### q-83947

u=y+3x,v=x; determinant−1; lower v=u²−3, topv=1, endpoints±2; absolute inverse Jacobian1; width4−u², primitive4u−u³/3, collected16−16/3. Source plot axis misalignment recorded.

Using the change of variables 

$$
u=y+3x,\,v=x,
$$

calculate the area of the finite region $D$ bounded by the curve $(y+3x)^{2}-x=3$ and the line $x=1.$

### q-160710

u=x−y,v=x+y; determinant2; u=v=1 and uv=2. Three vertices, primitive2lnu−u, external1/2; original substitution order v line thenu line is retained in raw evidence.

Using the change of variables 

$$
u=x-y,\,v=x+y,
$$

calculate the area of the finite region $D$ bounded by the lines $x+y=1,$ $x-y=1$ and the curve ${x}^{2}-{y}^{2}=2.$

## 2. Generalized backbone

A supplied invertible linear/affine change of variables maps a bounded curved region to a type-I region. Return one scalar area in a five-choice radio field. Four fixed stages: transform every defining boundary/find intersections/type-I domain and diagram; determinant of the inverse map from actual partial derivatives; reciprocal forward determinant/noncritical-point statement; absolute-Jacobian iterated integral, inner primitive, bound subtraction, width collection where present, outer primitive, endpoint arithmetic, final area. Every instance has a single worked solution independent of which wrong option is selected.

## 3. Complete component/bank mapping

Raw bank expressions below are a conservative **similarity replay** parameterization, not an inferred explanation of opaque historical mistakes. The original xy coordinate variables are divided by integer s∈[1,4] in the supplied map and region equations. The uv region remains fixed, determinant scales by1/s², forward Jacobian and every full area calculation RHS scale bys². Thus every captured numerical option z is reproduced by the exact recipe s²z. At s=1 prompt/solution/values/omissions reproduce exactly. Changed raw solutions preserve the source’s defects and are evidence-only; no learner-facing diagnosis is invented.

### Complete profile raw:q-38374

Field `selection`, radio/math,5 choices. Observed anchor map/domain parameters: `{'a': 1, 'h': 1, 'k': 0}`.

| Original complete value | Parameterized replay operation | Original designation |

|---|---|---|

| $\frac{2}{3}$ | $s^2\left(\frac{2}{3}\right)$ | designation absent |

| $1$ | $s^2\left(1\right)$ | designation absent |

| $2$ | $s^2\left(2\right)$ | designation absent |

| $\frac{4}{3}$ | $s^2\left(\frac{4}{3}\right)$ | designation absent |

| $\sqrt{2}$ | $s^2\left(\sqrt{2}\right)$ | designation absent |

### Complete profile raw:q-82874 — field0 (older widget)

Field `selection`, radio/math,5 choices. Observed anchor map/domain parameters: `{'a': 1, 'h': 1, 'k': 0}`.

| Original complete value | Parameterized replay operation | Original designation |

|---|---|---|

| $\frac{1}{3}$ | $s^2\left(\frac{1}{3}\right)$ | designation absent |

| $\frac{1}{2}$ | $s^2\left(\frac{1}{2}\right)$ | designation absent |

| $\frac{1}{10}$ | $s^2\left(\frac{1}{10}\right)$ | designation absent |

| $\frac{3}{20}$ | $s^2\left(\frac{3}{20}\right)$ | designation absent |

| $\frac{2}{3}$ | $s^2\left(\frac{2}{3}\right)$ | designation absent |

### Complete profile raw:q-160885

Field `selection`, radio/math,5 choices. Observed anchor map/domain parameters: `{'a': 2, 'h': 4, 'k': 1}`.

| Original complete value | Parameterized replay operation | Original designation |

|---|---|---|

| $\operatorname{ln}⁡4-\frac{3}{2}$ | $s^2\left(\operatorname{ln}⁡4-\frac{3}{2}\right)$ | wrong |

| $\operatorname{ln}⁡4-\frac{3}{4}$ | $s^2\left(\operatorname{ln}⁡4-\frac{3}{4}\right)$ | correct |

| $2\operatorname{ln}⁡4-3$ | $s^2\left(2\operatorname{ln}⁡4-3\right)$ | wrong |

| $4\operatorname{ln}⁡4-\frac{3}{4}$ | $s^2\left(4\operatorname{ln}⁡4-\frac{3}{4}\right)$ | wrong |

| $2\operatorname{ln}⁡4-\frac{3}{2}$ | $s^2\left(2\operatorname{ln}⁡4-\frac{3}{2}\right)$ | wrong |

### Complete profile raw:q-82878

Field `selection`, radio/math,5 choices. Observed anchor map/domain parameters: `{'a': 1, 'h': 2, 'k': 1}`.

| Original complete value | Parameterized replay operation | Original designation |

|---|---|---|

| $\frac{2}{3}$ | $s^2\left(\frac{2}{3}\right)$ | wrong |

| $\frac{8\sqrt{2}}{3}$ | $s^2\left(\frac{8\sqrt{2}}{3}\right)$ | correct |

| $\frac{8}{3}$ | $s^2\left(\frac{8}{3}\right)$ | wrong |

| $\frac{2\sqrt{2}}{3}$ | $s^2\left(\frac{2\sqrt{2}}{3}\right)$ | wrong |

| $\frac{\sqrt{2}}{3}$ | $s^2\left(\frac{\sqrt{2}}{3}\right)$ | wrong |

### Complete profile raw:q-83943

Field `selection`, radio/math,5 choices. Observed anchor map/domain parameters: `{'a': 2, 'h': 1, 'k': 2}`.

| Original complete value | Parameterized replay operation | Original designation |

|---|---|---|

| $\frac{2}{3}$ | $s^2\left(\frac{2}{3}\right)$ | wrong |

| $10$ | $s^2\left(10\right)$ | wrong |

| $2$ | $s^2\left(2\right)$ | wrong |

| $\frac{4}{3}$ | $s^2\left(\frac{4}{3}\right)$ | correct |

| $\frac{1}{3}$ | $s^2\left(\frac{1}{3}\right)$ | wrong |

### Complete profile raw:q-83947

Field `selection`, radio/math,5 choices. Observed anchor map/domain parameters: `{'a': 3, 'h': 4, 'k': -3}`.

| Original complete value | Parameterized replay operation | Original designation |

|---|---|---|

| $-\frac{32}{3}$ | $s^2\left(-\frac{32}{3}\right)$ | wrong |

| $\frac{16}{3}$ | $s^2\left(\frac{16}{3}\right)$ | wrong |

| $\frac{32}{3}$ | $s^2\left(\frac{32}{3}\right)$ | correct |

| $-\frac{16}{3}$ | $s^2\left(-\frac{16}{3}\right)$ | wrong |

| $\frac{47}{3}$ | $s^2\left(\frac{47}{3}\right)$ | wrong |

### Complete profile raw:q-160710

Field `selection`, radio/math,5 choices. Observed anchor map/domain parameters: `{'a': 1, 'h': 2, 'k': 1}`.

| Original complete value | Parameterized replay operation | Original designation |

|---|---|---|

| $\operatorname{ln}⁡2-1$ | $s^2\left(\operatorname{ln}⁡2-1\right)$ | wrong |

| $\operatorname{ln}⁡2-\frac{1}{2}$ | $s^2\left(\operatorname{ln}⁡2-\frac{1}{2}\right)$ | correct |

| $2\operatorname{ln}⁡2-2$ | $s^2\left(2\operatorname{ln}⁡2-2\right)$ | wrong |

| $\operatorname{ln}⁡2-3$ | $s^2\left(\operatorname{ln}⁡2-3\right)$ | wrong |

| $2\operatorname{ln}⁡2-\frac{3}{2}$ | $s^2\left(2\operatorname{ln}⁡2-\frac{3}{2}\right)$ | wrong |

### Complete profile raw:q-82874 — field1 (later widget)

A second captured radio field with the same selection key owns a separate five-value bank and original correct ref3/20. Raw replay preserves this field simultaneously with field0. Normal output uses one authoritative widget, matching the single widget in the owning MA capture.

| Original complete value | Parameterized replay operation | Original designation |

|---|---|---|

| $\frac{1}{10}$ | $s^2\left(\frac{1}{10}\right)$ | wrong |

| $\frac{3}{20}$ | $s^2\left(\frac{3}{20}\right)$ | correct |

| $\frac{2}{3}$ | $s^2\left(\frac{2}{3}\right)$ | wrong |

| $\frac{1}{2}$ | $s^2\left(\frac{1}{2}\right)$ | wrong |

| $\frac{1}{3}$ | $s^2\left(\frac{1}{3}\right)$ | wrong |

### Authored complete method banks

Let J be the absolute reciprocal determinant. For parabolas L=2h√h and E=2(√h)³/3 are separately integrated constant and quadratic terms; for quartic L=h²/2,E=h²/5; for hyperbola L=h ln(hi/lo),E=k(hi−lo). Entire selected bank before parameter sampling: `[J(L−E),J(L+E),−J(L−E),JL,JE]` for polynomial families; hyperbola’s last member is `−JE`, retaining the actual linear primitive component. Wrong choices respectively reverse the sign between terms, omit the area absolute sign, omit the second contribution or omit the first contribution. All complete scalar pairs are checked for equivalence, and any collision rejects the whole instance. No recipes are cherry-picked after sampling.

## 4. Reusable slots and constraints

All normal families vary integer shear/scale coefficient a∈[1,8]. Easy has h∈{1,4,9,16,25,36},k=0, u=x−ay,v=y. Moderate has a∈[2,8], same h,k=0,u=ax−2y,v=x+y. Hard up/vertical vary nonzero signed shift |k|≤5 and h∈{1,2,3,4,5,6,7,8,9,10,12,16}; down has k∈[1,4] and h∈{2,3,5,6,7,8,10,12}; quartic has h∈[1,3],k=0, curve coefficient1/h³ gives integer endpointsh, while original liney=0 transforms tov=u; hyperbolas k∈[1,3],h∈[2,12] with h>k².

Dependent objects are displayed xy equations, every substitution/prose operand, intersections, uv bounds, determinant entries/values, primitive terms at both endpoints, all five bank values and graph. No variable renaming, arbitrary operator change, rectangular-region mapping, choosing transformation or new nonlinear Jacobian is introduced. Source raw profiles keep their original field contract and omissions. Normal missing attributes are explicitly authored. Negative shift clauses and nonsquare down endpoints are difficulty guards, enforced on explicit parameters too.

Finite sampler catalog sizes (before cosmetic option order): easy48,moderate42,up960,vertical960,down256,quartic24,each hyperbola176. These are meaningful displayed maps/bounds rather than UUID/seed counts. The authored arithmetic ceiling uses familiar squares through36 and coefficients through8: endpoints are at most6 and only the existing determinant, reciprocal, quadratic primitive and two endpoint-power evaluations are required. This conservative broader domain follows the two stated integration/transformation prerequisites; it does not introduce a new operation or stage. Hard quartic keeps endpoints at most3 and familiar cube denominators1,8,27, so its existing degree-five evaluation stays at most243. The inverse y=(u−v)/(2a) substitution into y=0 remains operative; changing the line would have made that source stage redundant, so the line is fixed and the quartic coefficient is the conservative variable slot. Same determinant-one shears change the actual xy region but leave the area invariant; metadata retains their supplied map as part of the assessed transformation object.

Normal presentation retains shared source introductory/four-step sentences and the ordered mathematical operations. Safe TeX notation/grouping and correct source mathematics are explicit normalization; endpoint detail is an addition where a source collected endpoints into one row. Normal method banks are authored extensions, never counted as recovered historical banks. Raw and normal solution denominators are reported separately.

Full frozen-field fidelity totals are8/8 banks,40/40 values and6/6 existing correct refs. Missing refs are retained on q-38374 field0 and q-82874 field0. Field key/type, every answer type/feedback presence and attribute omissions are compared per widget; the old first-field-only validator has been replaced and a removed-second-widget regression must fail.
