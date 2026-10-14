# Template extraction — four stages

Source provenance: math basis2275; complete wrappers in source.json/topic.json/lesson.json.

## q-8739 — quadratic_product

### 1. Specific source

Which of the following is a first-order homogeneous ordinary differential equation?

The complete original worked solution is retained in source.json and repeated in the review. Fields and all observed bank components follow.

Field 0: `fc06f993-8bb8-5bba-9060-505b57e636e2`, key `selection`; correct reference **absent**.

- $\frac{dy}{dx} = \frac{x^{2}y}{x^{2} + y^{2}}$ — observed option; RHS recipe `sx**2*sy*x**2*y/(sx**2*x**2 + sy**2*y**2)`.
- $\frac{dy}{dx} = \frac{2xy}{x^{2} + y^{2}}$ — observed option; RHS recipe `2*sx*sy*x*y/(sx**2*x**2 + sy**2*y**2)`.
- $\frac{dy}{dx} = \frac{x^{2}y^{2}}{x^{2} + y^{2}}$ — observed option; RHS recipe `sx**2*sy**2*x**2*y**2/(sx**2*x**2 + sy**2*y**2)`.
- $\frac{dy}{dx} = \frac{xy^{2}}{x^{2} + y^{2}}$ — observed option; RHS recipe `sx*sy**2*x*y**2/(sx**2*x**2 + sy**2*y**2)`.
- $\frac{dy}{dx} = \frac{xy}{x + y}$ — observed option; RHS recipe `sx*sy*x*y/(sx*x + sy*y)`.

Field 1: `f23bfdfe-607b-5b9b-8499-14f49fb7f966`, key `selection`; correct reference present.

- $\frac{\text{d}y}{\text{d}x}=\frac{x{y}^{2}}{{x}^{2}+{y}^{2}}$ — observed option; RHS recipe `sx*sy**2*x*y**2/(sx**2*x**2 + sy**2*y**2)`.
- $\frac{\text{d}y}{\text{d}x}=\frac{xy}{x+y}$ — observed option; RHS recipe `sx*sy*x*y/(sx*x + sy*y)`.
- $\frac{\text{d}y}{\text{d}x}=\frac{{x}^{2}{y}^{2}}{{x}^{2}+{y}^{2}}$ — observed option; RHS recipe `sx**2*sy**2*x**2*y**2/(sx**2*x**2 + sy**2*y**2)`.
- $\frac{\text{d}y}{\text{d}x}=\frac{2xy}{{x}^{2}+{y}^{2}}$ — keyed correct; RHS recipe `2*sx*sy*x*y/(sx**2*x**2 + sy**2*y**2)`.
- $\frac{\text{d}y}{\text{d}x}=\frac{{x}^{2}y}{{x}^{2}+{y}^{2}}$ — observed option; RHS recipe `sx**2*sy*x**2*y/(sx**2*x**2 + sy**2*y**2)`.

### 2. Shared pattern

Select one homogeneous first-order ODE from five whole-equation options. Check numerator/denominator degrees then the f(tx,ty)=f(x,y) scaling definition; family-specific counterexample retained for offset quotient.

### 3. Components and operative stages

Stage 1: `f(tx,ty) & =\frac{2(tx)(ty)}{(tx)^{2}+(ty)^{2}}`.
Stage 2: `& =\frac{{t}^{2}\cdot 2xy}{{t}^{2}{x}^{2}+{t}^{2}{y}^{2}}`.
Stage 3: `& =\text{ }\frac{{t}^{2}\cdot 2xy}{{t}^{2}({x}^{2}+{y}^{2})}`.
Stage 4: `& =\frac{2xy}{{x}^{2}+{y}^{2}}`.
Stage 5: `& =f(x,y)`.

### 4. Reusable mask and slots

Every RHS coordinate occurrence is a complete token slot. Simultaneous factor substitution protects derivative notation, function argument labels, and complete TeX commands; adjacent xy receives both factors. The source family’s operative chain and prose remain present under changed factors. Coefficient factor1 renders the original token, through the same recipe.

{"easy": "sx,sy integers1..9, at least one is1", "moderate": "sx,sy integers1..9 except offset family1..3", "hard": "only cubic_quotient/quadratic_difference, sx and sy integers2..9"}

## q-14319 — cubic_quotient

### 1. Specific source

Which of the following is a first-order homogeneous ordinary differential equation?

The complete original worked solution is retained in source.json and repeated in the review. Fields and all observed bank components follow.

Field 0: `6eb6e88a-8ce7-5065-891e-2b9f914a957e`, key `selection`; correct reference present.

- $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}x-{x}^{2}}{{y}^{2}+{x}^{2}}$ — observed option; RHS recipe `(-sx**2*x**2 + sx*sy**2*x*y**2)/(sx**2*x**2 + sy**2*y**2)`.
- $\frac{\text{d}y}{\text{d}x}=\frac{{x}^{3}-3{x}^{2}y+x{y}^{2}}{{y}^{3}+{x}^{3}}$ — keyed correct; RHS recipe `(sx**3*x**3 - 3*sx**2*sy*x**2*y + sx*sy**2*x*y**2)/(sx**3*x**3 + sy**3*y**3)`.
- $\frac{\text{d}y}{\text{d}x}=\frac{{x}^{3}-3xy+xy}{{y}^{2}-{x}^{2}}$ — observed option; RHS recipe `(sx**3*x**3 - 2*sx*sy*x*y)/(-sx**2*x**2 + sy**2*y**2)`.
- $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{3}-{x}^{2}y+{x}^{3}}{{y}^{3}+1}$ — observed option; RHS recipe `(sx**3*x**3 - sx**2*sy*x**2*y + sy**3*y**3)/(sy**3*y**3 + 1)`.
- $\frac{\text{d}y}{\text{d}x}=\frac{{x}^{2}-x{y}^{2}+{y}^{2}}{1+{x}^{2}}$ — observed option; RHS recipe `(sx**2*x**2 - sx*sy**2*x*y**2 + sy**2*y**2)/(sx**2*x**2 + 1)`.

### 2. Shared pattern

Select one homogeneous first-order ODE from five whole-equation options. Check numerator/denominator degrees then the f(tx,ty)=f(x,y) scaling definition; family-specific counterexample retained for offset quotient.

### 3. Components and operative stages

Stage 1: `f(tx,ty) & =\frac{(tx)^{3}-3(tx)^{2}(ty)+(tx)(ty)^{2}}{(ty)^{3}+(tx)^{3}}`.
Stage 2: `& =\frac{{t}^{3}({x}^{3})-{t}^{3}(3{x}^{2}y)+{t}^{3}(x{y}^{2})}{{t}^{3}{y}^{3}+{t}^{3}{x}^{3}}`.
Stage 3: `& =\frac{{t}^{3}({x}^{3}-3{x}^{2}y+x{y}^{2})}{{t}^{3}({y}^{3}+{x}^{3})}`.
Stage 4: `& =\frac{{x}^{3}-3{x}^{2}y+x{y}^{2}}{{y}^{3}+{x}^{3}}`.
Stage 5: `& =f(x,y)`.

### 4. Reusable mask and slots

Every RHS coordinate occurrence is a complete token slot. Simultaneous factor substitution protects derivative notation, function argument labels, and complete TeX commands; adjacent xy receives both factors. The source family’s operative chain and prose remain present under changed factors. Coefficient factor1 renders the original token, through the same recipe.

{"easy": "sx,sy integers1..9, at least one is1", "moderate": "sx,sy integers1..9 except offset family1..3", "hard": "only cubic_quotient/quadratic_difference, sx and sy integers2..9"}

## q-8369 — quadratic_difference

### 1. Specific source

Which of the following is a first-order homogeneous ordinary differential equation?

The complete original worked solution is retained in source.json and repeated in the review. Fields and all observed bank components follow.

Field 0: `b19317f0-552c-5bb1-aa73-1ed888b17d05`, key `selection`; correct reference present.

- $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}-{x}^{2}}{{y}^{2}+x}$ — observed option; RHS recipe `(-sx**2*x**2 + sy**2*y**2)/(sx*x + sy**2*y**2)`.
- $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}-x}{{y}^{2}+{x}^{2}}$ — observed option; RHS recipe `(-sx*x + sy**2*y**2)/(sx**2*x**2 + sy**2*y**2)`.
- $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}-{x}^{2}}{{y}^{2}+{x}^{2}}$ — keyed correct; RHS recipe `(-sx**2*x**2 + sy**2*y**2)/(sx**2*x**2 + sy**2*y**2)`.
- $\frac{\text{d}y}{\text{d}x}=\frac{y-{x}^{2}}{{y}^{2}+{x}^{2}}$ — observed option; RHS recipe `(-sx**2*x**2 + sy*y)/(sx**2*x**2 + sy**2*y**2)`.
- $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}-{x}^{2}}{y-{x}^{2}}$ — observed option; RHS recipe `(-sx**2*x**2 + sy**2*y**2)/(-sx**2*x**2 + sy*y)`.

### 2. Shared pattern

Select one homogeneous first-order ODE from five whole-equation options. Check numerator/denominator degrees then the f(tx,ty)=f(x,y) scaling definition; family-specific counterexample retained for offset quotient.

### 3. Components and operative stages

Stage 1: `f(tx,ty) & =\frac{(ty)^{2}-(tx)^{2}}{(ty)^{2}+(tx)^{2}}`.
Stage 2: `& =\frac{{t}^{2}{y}^{2}-{t}^{2}{x}^{2}}{{t}^{2}{y}^{2}+{t}^{2}{x}^{2}}`.
Stage 3: `& =\frac{{t}^{2}({y}^{2}-{x}^{2})}{{t}^{2}({y}^{2}+{x}^{2})}`.
Stage 4: `& =\frac{{y}^{2}-{x}^{2}}{{y}^{2}+{x}^{2}}`.
Stage 5: `& =f(x,y)`.

### 4. Reusable mask and slots

Every RHS coordinate occurrence is a complete token slot. Simultaneous factor substitution protects derivative notation, function argument labels, and complete TeX commands; adjacent xy receives both factors. The source family’s operative chain and prose remain present under changed factors. Coefficient factor1 renders the original token, through the same recipe.

{"easy": "sx,sy integers1..9, at least one is1", "moderate": "sx,sy integers1..9 except offset family1..3", "hard": "only cubic_quotient/quadratic_difference, sx and sy integers2..9"}

## q-8741 — linear_not

### 1. Specific source

Which of the following is NOT a first-order homogeneous ordinary differential equation?

The complete original worked solution is retained in source.json and repeated in the review. Fields and all observed bank components follow.

Field 0: `f08fe0a1-984f-586e-afda-76db1f02247e`, key `selection`; correct reference present.

- $\frac{\text{d}y}{\text{d}x}=1$ — observed option; RHS recipe `1`.
- $\frac{\text{d}y}{\text{d}x}=\operatorname{ln}⁡y-\operatorname{ln}⁡x$ — observed option; RHS recipe `-log(sx*x) + log(sy*y)`.
- $\frac{\text{d}y}{\text{d}x}=x$ — keyed correct; RHS recipe `sx*x`.
- $\frac{\text{d}y}{\text{d}x}=\operatorname{arctan}⁡(\frac{x}{y})$ — observed option; RHS recipe `atan(sx*x/(sy*y))`.
- $\frac{\text{d}y}{\text{d}x}=2$ — observed option; RHS recipe `2`.

### 2. Shared pattern

Select one nonhomogeneous first-order ODE from five whole-equation options. Check numerator/denominator degrees then the f(tx,ty)=f(x,y) scaling definition; family-specific counterexample retained for offset quotient.

### 3. Components and operative stages

Stage 1: `f(tx,ty) & =tx=tf(x,y)\,`.

### 4. Reusable mask and slots

Every RHS coordinate occurrence is a complete token slot. Simultaneous factor substitution protects derivative notation, function argument labels, and complete TeX commands; adjacent xy receives both factors. The source family’s operative chain and prose remain present under changed factors. Coefficient factor1 renders the original token, through the same recipe.

{"easy": "sx,sy integers1..9, at least one is1", "moderate": "sx,sy integers1..9 except offset family1..3", "hard": "only cubic_quotient/quadratic_difference, sx and sy integers2..9"}

## q-14322 — constant_offset_not

### 1. Specific source

Which of the following is NOT a first-order homogeneous ordinary differential equation?

The complete original worked solution is retained in source.json and repeated in the review. Fields and all observed bank components follow.

Field 0: `a5a0fc63-6ea7-5103-a6b4-659ab0b835cf`, key `selection`; correct reference present.

- $\frac{\text{d}y}{\text{d}x}=\frac{xy}{{x}^{2}+{y}^{2}}$ — observed option; RHS recipe `sx*sy*x*y/(sx**2*x**2 + sy**2*y**2)`.
- $\frac{\text{d}y}{\text{d}x}=\operatorname{sin}⁡(\frac{x+y}{y})$ — observed option; RHS recipe `sin((sx*x + sy*y)/(sy*y))`.
- $\frac{\text{d}y}{\text{d}x}=\frac{{x}^{2}+1}{{y}^{2}+xy}$ — keyed correct; RHS recipe `(sx**2*x**2 + 1)/(sx*sy*x*y + sy**2*y**2)`.
- $\frac{\text{d}y}{\text{d}x}={e}^{\operatorname{sin}⁡(\frac{x}{y})}$ — observed option; RHS recipe `exp(sin(sx*x/(sy*y)))`.
- $\frac{\text{d}y}{\text{d}x}=\frac{4{x}^{2}y}{{x}^{3}+x{y}^{2}}$ — observed option; RHS recipe `4*sx**2*sy*x**2*y/(sx**3*x**3 + sx*sy**2*x*y**2)`.

### 2. Shared pattern

Select one nonhomogeneous first-order ODE from five whole-equation options. Check numerator/denominator degrees then the f(tx,ty)=f(x,y) scaling definition; family-specific counterexample retained for offset quotient.

### 3. Components and operative stages

Stage 1: `f(tx,ty) & =f(2\cdot 1,2\cdot 3)`.
Stage 2: `& =f(2,6)`.
Stage 3: `& =\frac{{2}^{2}+1}{{6}^{2}+2(6)}`.
Stage 4: `& =\frac{5}{48}`.
Stage 1: `f(x,y) & =f(1,2)`.
Stage 2: `& =\frac{{1}^{2}+1}{{2}^{2}+1(2)}`.
Stage 3: `& =\frac{2}{6}`.
Stage 4: `& =\frac{1}{3}.`.

### 4. Reusable mask and slots

Every RHS coordinate occurrence is a complete token slot. Simultaneous factor substitution protects derivative notation, function argument labels, and complete TeX commands; adjacent xy receives both factors. The source family’s operative chain and prose remain present under changed factors. Coefficient factor1 renders the original token, through the same recipe.

{"easy": "sx,sy integers1..9, at least one is1", "moderate": "sx,sy integers1..9 except offset family1..3", "hard": "only cubic_quotient/quadratic_difference, sx and sy integers2..9"}

## q-90597 — quadratic_not

### 1. Specific source

Which of the following is NOT a first-order homogeneous ordinary differential equation?

The complete original worked solution is retained in source.json and repeated in the review. Fields and all observed bank components follow.

Field 0: `1299ce9b-cffd-57b7-832d-bc7388915ab0`, key `selection`; correct reference present.

- $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}}{{x}^{2}+xy}$ — observed option; RHS recipe `sy**2*y**2/(sx**2*x**2 + sx*sy*x*y)`.
- $\frac{\text{d}y}{\text{d}x}=\operatorname{cos}⁡(\frac{x}{2y})$ — observed option; RHS recipe `cos(sx*x/(2*sy*y))`.
- $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}}{2}$ — keyed correct; RHS recipe `sy**2*y**2/2`.
- $\frac{\text{d}y}{\text{d}x}=\operatorname{sin}⁡(\frac{{x}^{3}}{{y}^{3}})$ — observed option; RHS recipe `sin(sx**3*x**3/(sy**3*y**3))`.
- $\frac{\text{d}y}{\text{d}x}=9$ — observed option; RHS recipe `9`.

### 2. Shared pattern

Select one nonhomogeneous first-order ODE from five whole-equation options. Check numerator/denominator degrees then the f(tx,ty)=f(x,y) scaling definition; family-specific counterexample retained for offset quotient.

### 3. Components and operative stages

Stage 1: `f(tx,ty) & =\frac{(ty)^{2}}{2}`.
Stage 2: `& ={t}^{2}\cdot \frac{{y}^{2}}{2}`.
Stage 3: `& ={t}^{2}f(x,y)\,`.

### 4. Reusable mask and slots

Every RHS coordinate occurrence is a complete token slot. Simultaneous factor substitution protects derivative notation, function argument labels, and complete TeX commands; adjacent xy receives both factors. The source family’s operative chain and prose remain present under changed factors. Coefficient factor1 renders the original token, through the same recipe.

{"easy": "sx,sy integers1..9, at least one is1", "moderate": "sx,sy integers1..9 except offset family1..3", "hard": "only cubic_quotient/quadratic_difference, sx and sy integers2..9"}

## Errors and authored bounds

Hard has no observed rating. Canonical e-2393 and introduction tutorial establish scaling recognition; preceding Homogeneous Functions and Introduction to Differential Equations are prerequisites. Route positions recognition before substitution-v and solving KPs. Hard therefore varies only the two observed easy polynomial banks with two nonunit coordinate factors, increasing coefficient bookkeeping at a fixed workload while retaining exactly the same recognition/factorization stages. No later-lesson operations or new functions.

Coefficients1..9 preserve one-digit number forms observed across the pool (including9); powers remain1/2/3 and recognition does not require expanding coefficient powers. Hard always carries two nonunit factors, easy at most one. The numerical counterexample family restricts factors1..3 and x0=1,y0=2,t=2..3; its largest displayed numerator is82 and denominator486, with the same square/add/multiply/fraction stages. Complete bank is selected before sampling; no individual option replacement or first-valid option pool exists. Every pair of whole ODEs, including incorrect pairs, is checked for algebraic equality. Four distractors sharing a classification are intentional; four equivalent equations would fail.

Canonical mathematical-task identity uses the qualifying RHS, the response criterion and the assessed coefficient bookkeeping. Complete banks and profile/seed/notation/witness aliases are excluded; they remain in content identity. Thus the moderate linear family does not count sy changes and the moderate quadratic family does not count sx changes as new tasks.

Log-difference options require x>0,y>0 and t>0. Ratio transcendental options use real variables and their displayed denominators nonzero. Every rational option retains its displayed-denominator exclusions, including cancellable denominator factors.

- q-8739: two selection fields; first has five choices and no correct reference. Normal uses the already-supported second field only. Raw retains both banks and missing key.

- q-14322: declares x1,y2,t3; evaluates f(2*1,2*3)=f(2,6)=5/48; simultaneous scaling would give f(3,6)=10/54=5/27. Normal derives t*x0,t*y0, actual function substitution, numerator/denominator and reduced fraction at every changed parameter.

- q-14322: Nonhomogeneous numerator claimed sufficient to imply function nonhomogeneous without considering cancellation. Normal explains numerator degrees2/0 and homogeneous denominator degree2; nonzero constant cannot cancel, so this family is nonhomogeneous of degree zero.

