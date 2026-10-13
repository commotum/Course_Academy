# Template extraction — four stages

Immutable math basis1356 / captured lineage. The source IDs below are provenance, not fabricated generated MA identifiers.

## 1. Specific source descriptions

### q-36383

Three polynomial terms: positive quadratic 3x², positive mixed cubic 2xy² and negative linear −y. Signed integer point (−1,1); partials 6x+2y² and 4xy−1 evaluate to (−4,−5). No difficulty, correct ref or worked solution is captured.

### q-37517

Composite cos(x²) and negative cubic −3y³, with familiar exact argument x²=π at (√π,2). The chain derivative −2x sin(x²) evaluates to zero; −9y² evaluates to −36. No difficulty, correct ref or worked solution is captured.

### q-130096

Logarithm ln(x²+y²+1), positive domain everywhere, point (−1,0). Both chain/quotient partials use the same denominator; the gradient is (−1,0). Six gradient rows and three tangent rows.

### q-130104

Three-term quadratic x²−4xy+5y², two negative point coordinates (−1,−1). Partials 2x−4y and 10y−4x evaluate to (2,−6). Six gradient rows and three tangent rows.

### q-72371

Two-term product x²y²+xy, positive point (1,2); held-coordinate derivatives 2xy²+y and 2yx²+x evaluate to (10,5). Six gradient rows and three tangent rows; source uses spaced gradient glyph and colon opening.

### q-130094

Three terms xy²−x+y at (1,−1), allowing component cancellation. Partials y²−1 and 2xy+1 evaluate to (0,−1). Six gradient rows and three tangent rows, with reduced basis row 0i−j.

### q-72377

Mixed cubic 2xy², bilinear xy and linear 2x at (1,1). Partials 2y²+y+2 and 4xy+x give equal components (5,5). Six gradient rows and three tangent rows; source uses spaced gradient glyph and colon opening.

## 2. Shared pattern and instructional purpose

Given an explicit scalar f(x,y) and P, differentiate both coordinates while holding the other fixed, evaluate both partials at P, then express the whole tangent equation using the nonzero gradient as its normal. Each observed source asks for a complete dot-product equation, not either equation side, a slope, tangent vector or normal line. The source families have fixed variable/function notation and one selection field of five choices. Distinct polynomial/log/trig components and source solution sentence/row differences have separate masks.

## 3. Complete components, original choices and bank profiles

Every bank below is a single indivisible observed profile `raw:q-ID`. In each row (v₁,v₂) is the exact historical covector, with the exact displayed whole equation retained. The only asserted parameterization is a geometric coordinate pullback: for positive integers r,s≤3, replace f by f(r x,s y), P by (p/r,q/s), and every historical normal by (r v₁,s v₂). This proves how the complete mathematical objects transform without claiming a recovered wrong-operation intention. Unclear historical errors are **opaque evidence**, including completed profiles. No arbitrary scalar fitting, answer perturbation, or mixture of partial banks is used.

### q-36383 — cross_cubic

Prompt: Given the function $f(x, y) = 3x^{2} + 2xy^{2} - y$, find the equation of the tangent line to the level curve that passes through the point where $(x, y) = (-1, 1)$.

Field key `selection`, type `:answer-field.type/radio`, five math answers. Parameters: f₀=`3*x**2+2*x*y**2-y`, P₀=`[-1, 1]`, original r=s=1.

|Original full displayed option|Original designation|Pullback normal recipe|Interpretation|
|---|---|---|---|
|$⟨2,-1⟩ \cdot ⟨x + 1, y - 1⟩ = 0$|key absent|`(r*(2), s*(-1))` at `(p₀/r,q₀/s)`|opaque historical operation|
|$⟨5, 3⟩ \cdot ⟨x + 1, y - 1⟩ = 0$|key absent|`(r*(5), s*(3))` at `(p₀/r,q₀/s)`|opaque historical operation|
|$⟨5, 4⟩ \cdot ⟨x + 1, y - 1⟩ = 0$|key absent|`(r*(5), s*(4))` at `(p₀/r,q₀/s)`|opaque historical operation|
|$⟨ - 4,-5⟩ \cdot ⟨x + 1, y - 1⟩ = 0$|key absent|`(r*(- 4), s*(-5))` at `(p₀/r,q₀/s)`|opaque historical operation|
|$⟨6, 2⟩ \cdot ⟨x + 1, y - 1⟩ = 0$|key absent|`(r*(6), s*(2))` at `(p₀/r,q₀/s)`|opaque historical operation|

Captured solution absent. Completed-only solution authoring uses the common six-row partial/gradient structure and three-row tangent structure, deriving all displayed expressions from the actual f and P.

### q-37517 — trig_cubic

Prompt: Given the function $f(x, y) = \cos (x^{2}) - 3y^{3}$, find the equation of the tangent line to the level curve that passes through the point where $(x, y) = (\sqrt{π}, 2)$.

Field key `selection`, type `:answer-field.type/radio`, five math answers. Parameters: f₀=`cos(x**2)-3*y**3`, P₀=`['sqrt(pi)', 2]`, original r=s=1.

|Original full displayed option|Original designation|Pullback normal recipe|Interpretation|
|---|---|---|---|
|$⟨0, 1⟩ \cdot ⟨x - \sqrt{π}, y - 2⟩ = 0$|key absent|`(r*(0), s*(1))` at `(p₀/r,q₀/s)`|opaque historical operation|
|$⟨6, 9⟩ \cdot ⟨x - \sqrt{π}, y - 2⟩ = 0$|key absent|`(r*(6), s*(9))` at `(p₀/r,q₀/s)`|opaque historical operation|
|$⟨36, 0⟩ \cdot ⟨x - \sqrt{π}, y - 2⟩ = 0$|key absent|`(r*(36), s*(0))` at `(p₀/r,q₀/s)`|opaque historical operation|
|$⟨0, 12⟩ \cdot ⟨x - \sqrt{π}, y - 2⟩ = 0$|key absent|`(r*(0), s*(12))` at `(p₀/r,q₀/s)`|opaque historical operation|
|$⟨0,-36⟩ \cdot ⟨x - \sqrt{π}, y - 2⟩ = 0$|key absent|`(r*(0), s*(-36))` at `(p₀/r,q₀/s)`|opaque historical operation|

Captured solution absent. Completed-only solution authoring uses the common six-row partial/gradient structure and three-row tangent structure, deriving all displayed expressions from the actual f and P.

### q-130096 — log_quadratic

Prompt: Given the function $f(x,y)=\operatorname{ln}⁡({x}^{2}+{y}^{2}+1),$ find the equation of the tangent line to the level curve that passes through the point where $(x,y)=(-1,0).$

Field key `selection`, type `:answer-field.type/radio`, five math answers. Parameters: f₀=`log(x**2+y**2+1)`, P₀=`[-1, 0]`, original r=s=1.

|Original full displayed option|Original designation|Pullback normal recipe|Interpretation|
|---|---|---|---|
|$⟨2,0⟩\cdot ⟨x+1,\,y⟩=0$|wrong according to captured key|`(r*(2), s*(0))` at `(p₀/r,q₀/s)`|opaque historical operation|
|$⟨-1,1⟩\cdot ⟨x+1,\,y⟩=0$|wrong according to captured key|`(r*(-1), s*(1))` at `(p₀/r,q₀/s)`|opaque historical operation|
|$⟨1,-1⟩\cdot ⟨x+1,\,y⟩=0$|wrong according to captured key|`(r*(1), s*(-1))` at `(p₀/r,q₀/s)`|opaque historical operation|
|$⟨-1,0⟩\cdot ⟨x+1,\,y⟩=0$|correct|`(r*(-1), s*(0))` at `(p₀/r,q₀/s)`|opaque historical operation|
|$⟨0,-2⟩\cdot ⟨x+1,\,y⟩=0$|wrong according to captured key|`(r*(0), s*(-2))` at `(p₀/r,q₀/s)`|opaque historical operation|

Ordered solution components:

- `F`: $\operatorname{ln}⁡({x}^{2}+{y}^{2}+1)$
- `DX`: $\frac{2x}{{x}^{2}+{y}^{2}+1}$
- `DY`: $\frac{2y}{{x}^{2}+{y}^{2}+1}$
- `EX`: $\frac{2(-1)}{(-1)^{2}+{0}^{2}+1}$
- `EY`: $\frac{2(0)}{(-1)^{2}+{0}^{2}+1}$
- `BASIS`: $(-1)i+0\,j$
- `GRAD`: $⟨-1,0⟩$
- `P`: $(-1,0)$
- `DISP_RAW`: $⟨x-(-1),\,y-0⟩$
- `DISP`: $⟨x+1,\,y⟩$

### q-130104 — quadratic

Prompt: Given the function $f(x,y)={x}^{2}-4xy+5{y}^{2}$ find the equation of the tangent line to the level curve that passes through the point where $(x,y)=(-1,-1).$

Field key `selection`, type `:answer-field.type/radio`, five math answers. Parameters: f₀=`x**2-4*x*y+5*y**2`, P₀=`[-1, -1]`, original r=s=1.

|Original full displayed option|Original designation|Pullback normal recipe|Interpretation|
|---|---|---|---|
|$⟨2,0⟩\cdot ⟨x+1,\,y+1⟩=0$|wrong according to captured key|`(r*(2), s*(0))` at `(p₀/r,q₀/s)`|opaque historical operation|
|$⟨0,-1⟩\cdot ⟨x+1,\,y+1⟩=0$|wrong according to captured key|`(r*(0), s*(-1))` at `(p₀/r,q₀/s)`|opaque historical operation|
|$⟨-2,4⟩\cdot ⟨x+1,\,y+1⟩=0$|wrong according to captured key|`(r*(-2), s*(4))` at `(p₀/r,q₀/s)`|opaque historical operation|
|$⟨3,1⟩\cdot ⟨x+1,\,y+1⟩=0$|wrong according to captured key|`(r*(3), s*(1))` at `(p₀/r,q₀/s)`|opaque historical operation|
|$⟨2,-6⟩\cdot ⟨x+1,\,y+1⟩=0$|correct|`(r*(2), s*(-6))` at `(p₀/r,q₀/s)`|opaque historical operation|

Ordered solution components:

- `F`: ${x}^{2}-4xy+5{y}^{2}$
- `DX`: $(2x-4y)$
- `DY`: $(10y-4x)$
- `EX`: $(2(-1)-4(-1))$
- `EY`: $(10(-1)-4(-1))$
- `BASIS`: $2\,i-6\,j$
- `GRAD`: $⟨2,-6⟩$
- `P`: $(-1,-1)$
- `DISP_RAW`: $⟨x-(-1),\,y-(-1)⟩$
- `DISP`: $⟨x+1,\,y+1⟩$

### q-72371 — product

Prompt: Given the function $f(x,y)={x}^{2}{y}^{2}+xy$, find the equation of the tangent line to the level curve that passes through the point where $(x,y)=(1,2).$

Field key `selection`, type `:answer-field.type/radio`, five math answers. Parameters: f₀=`x**2*y**2+x*y`, P₀=`[1, 2]`, original r=s=1.

|Original full displayed option|Original designation|Pullback normal recipe|Interpretation|
|---|---|---|---|
|$⟨8,5⟩\cdot ⟨x-1,\,y-2⟩=0$|wrong according to captured key|`(r*(8), s*(5))` at `(p₀/r,q₀/s)`|opaque historical operation|
|$⟨5,10⟩\cdot ⟨x-1,\,y-2⟩=0$|wrong according to captured key|`(r*(5), s*(10))` at `(p₀/r,q₀/s)`|opaque historical operation|
|$⟨-10,15⟩\cdot ⟨x-1,\,y-2⟩=0$|wrong according to captured key|`(r*(-10), s*(15))` at `(p₀/r,q₀/s)`|opaque historical operation|
|$⟨15,10⟩\cdot ⟨x-1,\,y-2⟩=0$|wrong according to captured key|`(r*(15), s*(10))` at `(p₀/r,q₀/s)`|opaque historical operation|
|$⟨10,5⟩\cdot ⟨x-1,\,y-2⟩=0$|correct|`(r*(10), s*(5))` at `(p₀/r,q₀/s)`|opaque historical operation|

Ordered solution components:

- `F`: ${x}^{2}{y}^{2}+xy$
- `DX`: $(2x{y}^{2}+y)$
- `DY`: $(2y{x}^{2}+x)$
- `EX`: $(2(1)(2)^{2}+(2))$
- `EY`: $(2(2)(1)^{2}+(1))$
- `BASIS`: $10\,i+5\,j$
- `GRAD`: $⟨10,5⟩$
- `P`: $(1,2)$
- `DISP_RAW`: $⟨x-1,\,y-2⟩$
- `DISP`: $⟨x-1,\,y-2⟩$

### q-130094 — cubic_linear

Prompt: Given the function $f(x,y)=x{y}^{2}-x+y,$ find the equation of the tangent line to the level curve that passes through the point where $(x,y)=(1,-1).$

Field key `selection`, type `:answer-field.type/radio`, five math answers. Parameters: f₀=`x*y**2-x+y`, P₀=`[1, -1]`, original r=s=1.

|Original full displayed option|Original designation|Pullback normal recipe|Interpretation|
|---|---|---|---|
|$⟨1,0⟩\cdot ⟨x-1,\,y+1⟩=0$|wrong according to captured key|`(r*(1), s*(0))` at `(p₀/r,q₀/s)`|opaque historical operation|
|$⟨-1,0⟩\cdot ⟨x-1,\,y+1⟩=0$|wrong according to captured key|`(r*(-1), s*(0))` at `(p₀/r,q₀/s)`|opaque historical operation|
|$⟨-1,1⟩\cdot ⟨x-1,\,y+1⟩=0$|wrong according to captured key|`(r*(-1), s*(1))` at `(p₀/r,q₀/s)`|opaque historical operation|
|$⟨1,-1⟩\cdot ⟨x-1,\,y+1⟩=0$|wrong according to captured key|`(r*(1), s*(-1))` at `(p₀/r,q₀/s)`|opaque historical operation|
|$⟨0,-1⟩\cdot ⟨x-1,\,y+1⟩=0$|correct|`(r*(0), s*(-1))` at `(p₀/r,q₀/s)`|opaque historical operation|

Ordered solution components:

- `F`: $x{y}^{2}-x+y$
- `DX`: $({y}^{2}-1)$
- `DY`: $(2xy+1)$
- `EX`: $((-1)^{2}-1)$
- `EY`: $(2(1)(-1)+1)$
- `BASIS`: $0\,i-j$
- `GRAD`: $⟨0,-1⟩$
- `P`: $(1,-1)$
- `DISP_RAW`: $⟨x-1,\,y-(-1)⟩$
- `DISP`: $⟨x-1,\,y+1⟩$

### q-72377 — cubic_xy

Prompt: Given the function $f(x,y)=2x{y}^{2}+xy+2x$, find the equation of the tangent line to the level curve that passes through the point where $(x,y)=(1,1).$

Field key `selection`, type `:answer-field.type/radio`, five math answers. Parameters: f₀=`2*x*y**2+x*y+2*x`, P₀=`[1, 1]`, original r=s=1.

|Original full displayed option|Original designation|Pullback normal recipe|Interpretation|
|---|---|---|---|
|$⟨3,2⟩\cdot ⟨x-1,\,y-1⟩=0$|wrong according to captured key|`(r*(3), s*(2))` at `(p₀/r,q₀/s)`|opaque historical operation|
|$⟨4,5⟩\cdot ⟨x-1,\,y-1⟩=0$|wrong according to captured key|`(r*(4), s*(5))` at `(p₀/r,q₀/s)`|opaque historical operation|
|$⟨-5,5⟩\cdot ⟨x-1,\,y-1⟩=0$|wrong according to captured key|`(r*(-5), s*(5))` at `(p₀/r,q₀/s)`|opaque historical operation|
|$⟨2,3⟩\cdot ⟨x-1,\,y-1⟩=0$|wrong according to captured key|`(r*(2), s*(3))` at `(p₀/r,q₀/s)`|opaque historical operation|
|$⟨5,5⟩\cdot ⟨x-1,\,y-1⟩=0$|correct|`(r*(5), s*(5))` at `(p₀/r,q₀/s)`|opaque historical operation|

Ordered solution components:

- `F`: $2x{y}^{2}+xy+2x$
- `DX`: $(2{y}^{2}+y+2)$
- `DY`: $(4xy+x)$
- `EX`: $(2(1)^{2}+(1)+2)$
- `EY`: $(4(1)(1)+(1))$
- `BASIS`: $5\,i+5\,j$
- `GRAD`: $⟨5,5⟩$
- `P`: $(1,1)$
- `DISP_RAW`: $⟨x-1,\,y-1⟩$
- `DISP`: $⟨x-1,\,y-1⟩$

## 4. Reusable Markdown/value templates and constraints

`templates.json` stores extracted full-component masks, exact component formatting, all 35 original mathematical values and the seven whole historical profiles. Prompt slots are **complete function** F and **complete point tuple** P. Worked solutions use complete F, DX, DY, EX, EY, basis reduction, gradient tuple, evaluated point and two displacement representations. All shared source sentences and ordered rows are retained byte-exact at original parameters. Changed pullback parameters use the same complete masks and row count; displayed substitution components use the derivative of the displayed transformed function at the displayed transformed point. Their arithmetic is independently parsed and checked. No prose-wide number replacement occurs.

Raw replay preserves missing :question/difficulty, :question/worked-solution and :answer-field/correct attributes. Identity/db IDs are regenerated as stable owned UUIDs; original identity attributes remain in source.json and source_id provenance. Completed-only profiles infer missing easy labels, missing solutions and missing correct refs. q-36383's independently derived gradient is (−4,−5), selecting that exact normal. q-37517's independently derived gradient is (0,−36), selecting that exact normal representation; this is not a claim that the other equivalent horizontal choices are incorrect. Completions remain evidence-only.

Source anomalies are mathematical whole-object ambiguities, not malformed TeX. q-37517 has three equivalent correct equations with normals (0,1), (0,12), (0,−36). q-130096 has two equivalent correct equations, (2,0) and (−1,0), plus a duplicate wrong pair (−1,1)/(1,−1). q-130094 has two duplicate wrong pairs (1,0)/(−1,0) and (−1,1)/(1,−1). All have the same displacement vector within each bank. Thus these banks have respectively 3,3,3 distinct lines rather than five. Raw exact fidelity does not certify learning validity. No source options are silently removed or counted as uniquely correct. The safe authored bank is a separate profile with five unequal complete line objects.

Normal parameters: signed nonzero integer a,b,c, |coefficient|≤5 for easy and ≤6 for moderate/hard. Easy integer coordinates have 1≤|p|,|q|≤2. Moderate has 1≤|p|,|q|≤3. Hard has reduced rational p,q with denominator 2 or 3 and 1≤|numerator|≤5. The reduced evaluated component numerators must be ≤200 and denominators ≤27. These are finite familiar arithmetic bounds, not a bypass through huge unreduced inputs. Trig easy fixes the familiar argument x²=π, x=√π, nonzero integer |q|≤2, cos coefficient 1, bounded signed cubic coefficient b. Log inner coefficients are positive abs(a),abs(b),abs(c), ensuring its domain; redundant parameter signs are excluded from identity/task counts. Polynomial families retain their displayed terms with nonzero coefficients; no degree or response branch changes under sampling.

The normal `method:regular` complete bank is: correct gradient at P; flip its x component; swap its components; reverse the x point coordinate; reverse the y point coordinate. Eligibility requires two nonzero components unequal up to sign, and all five complete lines distinct. The `method:product` bank is: correct gradient; omit the xy contribution to its x partial; omit the xy contribution to its y partial; swap gradient components; flip the x component. A separate bank is needed because product-family reversed-point errors are always equivalent to each other. `method:horizontal` is selected before trig sampling: correct horizontal tangent; swapped-components vertical line; gradient from incorrectly replacing sin(π) by 1; omit the y point coordinate; reverse the y point coordinate. Every error arises from an assessed differentiation, evaluation or line-construction operation. The whole selected profile is rejected on collisions; no member is replaced from a first-valid pool.

Each safe fixed solution uses the same source instructional sentences, formal gradient/partial input row, symbolic derivatives, both explicit point substitutions, reduced basis components, gradient tuple, formal tangent identity, substituted gradient/point row and final whole dot-product equation. It does not vary with the selected wrong response. Moderate and hard use the same canonical three terms and stage sequence, with the stated workload domains, and introduce no normal-line equation or neighboring tangent-vector/point-search tasks.

Parameter sampling, normal explicit parameters, historical coordinate pullbacks, and invalid-input tests all enforce their stated finite domains. Mathematical-task fingerprints normalize common polynomial scaling and omit profiles, notation and incidental/unused constants. Content identity includes complete actual displayed prompt, solution, bank and designation; shuffle/seed do not alter it. Finite-domain counts enumerate the quadratic easy family as a conservative lower bound and the entire supported canonical moderate/hard families. Source masks and historical banks do not inflate these task counts.
