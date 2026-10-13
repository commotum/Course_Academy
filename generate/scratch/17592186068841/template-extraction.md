# Template extraction: four stages

Capture: math basis 1356; lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. Raw source.json is unchanged. Mathematical component slots are simultaneous and confined to mathematical spans. Shared solution prose remains fixed independently of chosen option. All 14 observed question/bank profiles are covered before authored easy extensions.

Coefficient a is a single complete component per route, not a blind numeral replacement. Moderate/hard a is a positive integer 1..8 except the blank power 1..4. The original coefficients remain accepted. Varying one coefficient retains signs, power structure, exact primitives and the source arithmetic workload. These finite ranges produce meaningful assessed tasks; see validation counts. No claim of unlimited variety is made.

## Source errors and normal repairs

- q3854: log(x²)+log(x³/3)+K and log(x²)+log(x³)+K differ by a constant. The full ambiguous source bank is available through public observed profile. Normal output changes only the final wrong exponent from x³ to x², an explicitly authored distractor repair. Both log distractors remain incorrect for the ODE; native choice IDs cannot detect their duplicate families.
- q158009: after K is allowed either sign, the source retains |y+3|=K exp(-1/x). Negative K makes that row impossible. Normal output removes precisely this row; the supported y+3=K exp(-1/x) and final subtract-shift row remain. Raw evidence replay preserves it. Nonzero x is explicit in normal prompts.
- q79665 and q8304: splitting sqrt(xy) into sqrt(x)sqrt(y) is not valid for negative x,y even though the original ODE admits that real domain. Normal prompt restricts x,y>0; source mathematical checks therefore apply to its positive branch, not its unrestricted wording.
- q8303 and q79665: squaring a sqrt(y) primitive also requires its solved inner factor positive. q8304 requires 3a sqrt(x)+K positive for positive y. Normal prompts include the local-interval restrictions. Source wording and bank are retained in observed evidence.
- Radio source prompts are preserved without added placeholders. Blank source whitespace/layout and the matching {{field-1}} placeholder are retained. No source field is silently omitted.

Source correctness is conditional where domains are omitted; raw exact reproduction, equivalent values/prose/stage structure, normal correctness and native grading have separate denominators. Observed prompts and worked solutions are raw-exact 14/14 after source-style component rendering, with no literal-payload replay branch. All natural logs keep ln convention. Answer notation is normalized by SymPy; raw solution equality is reported separately.

## q-8303 / source 17592186069532

### 1. Specific source

Find the general solution to the differential equation ${y}^{′}-\sqrt{y}=2x\sqrt{y}$ for $y\ne 0.$

Observed difficulty moderate, field :answer-field.type/radio, key selection. Original component a=1. Exact forms and complete raw prose are preserved in source.json and source-cases.json. No plots.

### 2. Shared pattern

Separate as g(y)y′=f(x), with g(y)=1/sqrt(y), f(x)=2*x + 1. Evaluate both primitives and solve for y; preserve the same explicit family shape and local domain. This route is an independent value/prose template, not merged with another primitive inversion.

### 3. Components and complete choice-bank mapping

| Source option (exact captured value) | Recipe position | Value at changed component a=2 | Correct |
|---|---:|---|---|
| `y={(\frac{{x}^{2}+x+C}{2})}^{2}` | `spec(q-8303, a)[bank][0]` | `(C/2 + x**2/2 + x)**2` | True |
| `y={x}^{2}+x+C` | `spec(q-8303, a)[bank][1]` | `C + x**2 + 2*x` | False |
| `y=({x}^{2}+x)^{2}` | `spec(q-8303, a)[bank][2]` | `(x**2 + 2*x)**2` | False |
| `y=({x}^{2}+x+C)^{2}` | `spec(q-8303, a)[bank][3]` | `(C + x**2 + 2*x)**2` | False |
| `y={(\frac{{x}^{2}+x}{2})}^{2}` | `spec(q-8303, a)[bank][4]` | `(x**2/2 + x)**2` | False |

Each recipe is the explicit symbolic expression in the named spec branch. The bank is selected whole; pairwise family equivalence is checked modulo constant rescaling/shifts. Evidence shapes with obscure distractor intent remain interpreted only as parameterized expressions, not recovered error operations. Coefficient dependencies for these shapes are design choices anchored to their observed forms.

### 4. Reusable masks and constraints

Worked-solution math-block row counts: [5, 3, 1, 1]. The opening, integration, implicit-form and explicit-form prose remains unchanged in observed replay. The mask contains complete coefficient terms, collected integrands and corresponding primitive components; replacement order cannot alter already-rendered text. At a changed component, the original stage count and route remain fixed.

Local domain: `y>0,\quad x^2+a x+C>0`. Sampling/explicit guards: integer coefficient a=1..8. Public observed profiles retain the whole evidence bank. Normal output applies documented teaching/domain repairs and uses authored whole operation banks where listed below. For the blank, the entire expected answer fragment is x^(a+1), reinserted into the actual displayed -(a+1)(fragment+K)^(-1) family and independently differentiated.

Actual mathematical slot map (a=2):

```json
{
  "{x}^{2}+x": "{x}^{2}+2x",
  "2x+1": "2x+2",
  "-\\sqrt{y}": "-2\\sqrt{y}",
  "+\\sqrt{y}": "+2\\sqrt{y}"
}
```

## q-8305 / source 17592186069533

### 1. Specific source

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}-(\operatorname{cos}⁡x)y=0$ for $y\ne 0.$

Observed difficulty hard, field :answer-field.type/radio, key selection. Original component a=1. Exact forms and complete raw prose are preserved in source.json and source-cases.json. No plots.

### 2. Shared pattern

Separate as g(y)y′=f(x), with g(y)=1/y, f(x)=cos(x). Evaluate both primitives and solve for y; preserve the same explicit family shape and local domain. This route is an independent value/prose template, not merged with another primitive inversion.

### 3. Components and complete choice-bank mapping

| Source option (exact captured value) | Recipe position | Value at changed component a=2 | Correct |
|---|---:|---|---|
| `y=K{e}^{-\operatorname{cos}⁡x}` | `spec(q-8305, a)[bank][0]` | `K*exp(-2*cos(x))` | False |
| `y={e}^{-\operatorname{cos}⁡x}+K` | `spec(q-8305, a)[bank][1]` | `K + exp(-2*cos(x))` | False |
| `y={e}^{\operatorname{sin}⁡x}+K` | `spec(q-8305, a)[bank][2]` | `K + exp(2*sin(x))` | False |
| `y=K{e}^{\operatorname{cos}⁡x}` | `spec(q-8305, a)[bank][3]` | `K*exp(2*cos(x))` | False |
| `y=K{e}^{\operatorname{sin}⁡x}` | `spec(q-8305, a)[bank][4]` | `K*exp(2*sin(x))` | True |

Each recipe is the explicit symbolic expression in the named spec branch. The bank is selected whole; pairwise family equivalence is checked modulo constant rescaling/shifts. Evidence shapes with obscure distractor intent remain interpreted only as parameterized expressions, not recovered error operations. Coefficient dependencies for these shapes are design choices anchored to their observed forms.

### 4. Reusable masks and constraints

Worked-solution math-block row counts: [3, 3, 1, 4, 1]. The opening, integration, implicit-form and explicit-form prose remains unchanged in observed replay. The mask contains complete coefficient terms, collected integrands and corresponding primitive components; replacement order cannot alter already-rendered text. At a changed component, the original stage count and route remain fixed.

Local domain: `K\ne0`. Sampling/explicit guards: integer coefficient a=1..8. Public observed profiles retain the whole evidence bank. Normal output applies documented teaching/domain repairs and uses authored whole operation banks where listed below. For the blank, the entire expected answer fragment is x^(a+1), reinserted into the actual displayed -(a+1)(fragment+K)^(-1) family and independently differentiated.

Actual mathematical slot map (a=2):

```json
{
  "\\operatorname{cos}⁡x": "2\\operatorname{cos}⁡x",
  "\\operatorname{sin}⁡x": "2\\operatorname{sin}⁡x"
}
```

## q-128191 / source 17592186235351

### 1. Specific source

Find the general solution to the differential equation ${y}^{′}=x{y}^{2}.$ Assume that $y\ne 0$ and $K$ is an arbitrary constant.

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        $y=-2($ 

                                    
                                
                                    
                            
                                        {{field-1}}                
                                    
                                
                                    
                                        
                                        $+K)^{-1}$

Observed difficulty moderate, field :answer-field.type/blank, key field-1. Original component a=1. Exact forms and complete raw prose are preserved in source.json and source-cases.json. No plots.

### 2. Shared pattern

Separate as g(y)y′=f(x), with g(y)=y**(-2), f(x)=x. Evaluate both primitives and solve for y; preserve the same explicit family shape and local domain. This route is an independent value/prose template, not merged with another primitive inversion.

### 3. Components and complete choice-bank mapping

| Source option (exact captured value) | Recipe position | Value at changed component a=2 | Correct |
|---|---:|---|---|
| `{x}^{2}` | `spec(q-128191, a)[bank][0]` | `x**3` | True |

Each recipe is the explicit symbolic expression in the named spec branch. The bank is selected whole; pairwise family equivalence is checked modulo constant rescaling/shifts. Evidence shapes with obscure distractor intent remain interpreted only as parameterized expressions, not recovered error operations. Coefficient dependencies for these shapes are design choices anchored to their observed forms.

### 4. Reusable masks and constraints

Worked-solution math-block row counts: [2, 3, 6]. The opening, integration, implicit-form and explicit-form prose remains unchanged in observed replay. The mask contains complete coefficient terms, collected integrands and corresponding primitive components; replacement order cannot alter already-rendered text. At a changed component, the original stage count and route remain fixed.

Local domain: `x^{a+1}+K\ne0`. Sampling/explicit guards: integer power a=1..4. Public observed profiles retain the whole evidence bank. Normal output applies documented teaching/domain repairs and uses authored whole operation banks where listed below. For the blank, the entire expected answer fragment is x^(a+1), reinserted into the actual displayed -(a+1)(fragment+K)^(-1) family and independently differentiated.

Actual mathematical slot map (a=2):

```json
{
  "{x}^{2}+2C": "{x}^{3}+3C",
  "{x}^{2}+K": "{x}^{3}+K",
  "\\frac{{x}^{2}}{2}": "\\frac{{x}^{3}}{3}",
  "{x}^{2}": "{x}^{3}",
  "x{y}^{2}": "{x}^{2}{y}^{2}",
  "=x\\end": "={x}^{2}\\end",
  "\\int x\\,": "\\int {x}^{2}\\,",
  "\\frac{{x}^{2}+2C}{2}": "\\frac{{x}^{3}+3C}{3}",
  "-\\frac{2}{": "-\\frac{3}{",
  "-2{(": "-3{(",
  "-2($": "-3($",
  "$K=2C$": "$K=3C$"
}
```

## q-14247 / source 17592186272346

### 1. Specific source

Find the general solution to the differential equation ${y}^{′}=y+3y{x}^{2}$ for $y\ne 0.$

Observed difficulty hard, field :answer-field.type/radio, key selection. Original component a=1. Exact forms and complete raw prose are preserved in source.json and source-cases.json. No plots.

### 2. Shared pattern

Separate as g(y)y′=f(x), with g(y)=1/y, f(x)=3*x**2 + 1. Evaluate both primitives and solve for y; preserve the same explicit family shape and local domain. This route is an independent value/prose template, not merged with another primitive inversion.

### 3. Components and complete choice-bank mapping

| Source option (exact captured value) | Recipe position | Value at changed component a=2 | Correct |
|---|---:|---|---|
| `y=K{e}^{\sqrt{{x}^{2}+2}}` | `spec(q-14247, a)[bank][0]` | `K*exp(sqrt(x**2 + 4))` | False |
| `y=K{e}^{{x}^{2}+2x}` | `spec(q-14247, a)[bank][1]` | `K*exp(x**2 + 4*x)` | False |
| `y=K{e}^{\sqrt{{x}^{3}+x}}` | `spec(q-14247, a)[bank][2]` | `K*exp(sqrt(x**3 + 2*x))` | False |
| `y=K{e}^{{x}^{3}+x}` | `spec(q-14247, a)[bank][3]` | `K*exp(x**3 + 2*x)` | True |
| `y=K{e}^{3{x}^{2}+x}` | `spec(q-14247, a)[bank][4]` | `K*exp(3*x**2 + 2*x)` | False |

Each recipe is the explicit symbolic expression in the named spec branch. The bank is selected whole; pairwise family equivalence is checked modulo constant rescaling/shifts. Evidence shapes with obscure distractor intent remain interpreted only as parameterized expressions, not recovered error operations. Coefficient dependencies for these shapes are design choices anchored to their observed forms.

### 4. Reusable masks and constraints

Worked-solution math-block row counts: [4, 3, 1, 4, 1]. The opening, integration, implicit-form and explicit-form prose remains unchanged in observed replay. The mask contains complete coefficient terms, collected integrands and corresponding primitive components; replacement order cannot alter already-rendered text. At a changed component, the original stage count and route remain fixed.

Local domain: `K\ne0`. Sampling/explicit guards: integer coefficient a=1..8. Public observed profiles retain the whole evidence bank. Normal output applies documented teaching/domain repairs and uses authored whole operation banks where listed below. For the blank, the entire expected answer fragment is x^(a+1), reinserted into the actual displayed -(a+1)(fragment+K)^(-1) family and independently differentiated.

Actual mathematical slot map (a=2):

```json
{
  "y+3y": "2y+3y",
  "1+3{x}^{2}": "2+3{x}^{2}",
  "x+{x}^{3}": "2x+{x}^{3}",
  "{x}^{3}+x": "{x}^{3}+2x"
}
```

## q-14253 / source 17592186272353

### 1. Specific source

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}={y}^{2}+2{y}^{2}x$ for $y\ne 0.$

Observed difficulty moderate, field :answer-field.type/radio, key selection. Original component a=1. Exact forms and complete raw prose are preserved in source.json and source-cases.json. No plots.

### 2. Shared pattern

Separate as g(y)y′=f(x), with g(y)=y**(-2), f(x)=2*x + 1. Evaluate both primitives and solve for y; preserve the same explicit family shape and local domain. This route is an independent value/prose template, not merged with another primitive inversion.

### 3. Components and complete choice-bank mapping

| Source option (exact captured value) | Recipe position | Value at changed component a=2 | Correct |
|---|---:|---|---|
| `y=-\frac{1}{2x+C}` | `spec(q-14253, a)[bank][0]` | `-1/(C + 4*x)` | False |
| `y=-\frac{1}{{x}^{2}+x}+C` | `spec(q-14253, a)[bank][1]` | `C - 1/(x**2 + 2*x)` | False |
| `y=\frac{1}{2{x}^{2}+x}+C` | `spec(q-14253, a)[bank][2]` | `C + 1/(2*x**2 + 2*x)` | False |
| `y=\frac{1}{{x}^{3}+C}` | `spec(q-14253, a)[bank][3]` | `1/(C + x**3)` | False |
| `y=-\frac{1}{{x}^{2}+x+C}` | `spec(q-14253, a)[bank][4]` | `-1/(C + x**2 + 2*x)` | True |

Each recipe is the explicit symbolic expression in the named spec branch. The bank is selected whole; pairwise family equivalence is checked modulo constant rescaling/shifts. Evidence shapes with obscure distractor intent remain interpreted only as parameterized expressions, not recovered error operations. Coefficient dependencies for these shapes are design choices anchored to their observed forms.

### 4. Reusable masks and constraints

Worked-solution math-block row counts: [3, 3, 1, 1]. The opening, integration, implicit-form and explicit-form prose remains unchanged in observed replay. The mask contains complete coefficient terms, collected integrands and corresponding primitive components; replacement order cannot alter already-rendered text. At a changed component, the original stage count and route remain fixed.

Local domain: `x^2+a x+C\ne0`. Sampling/explicit guards: integer coefficient a=1..8. Public observed profiles retain the whole evidence bank. Normal output applies documented teaching/domain repairs and uses authored whole operation banks where listed below. For the blank, the entire expected answer fragment is x^(a+1), reinserted into the actual displayed -(a+1)(fragment+K)^(-1) family and independently differentiated.

Actual mathematical slot map (a=2):

```json
{
  "={y}^{2}+2": "=2{y}^{2}+2",
  "1+2x": "2+2x",
  "x+{x}^{2}": "2x+{x}^{2}",
  "{x}^{2}+x": "{x}^{2}+2x"
}
```

## q-158009 / source 17592186275405

### 1. Specific source

Find the general solution to the differential equation ${x}^{2}\,{y}^{′}-y=3$ for $y\ne -3.$

Observed difficulty hard, field :answer-field.type/radio, key selection. Original component a=3. Exact forms and complete raw prose are preserved in source.json and source-cases.json. No plots.

### 2. Shared pattern

Separate as g(y)y′=f(x), with g(y)=1/(y + 3), f(x)=x**(-2). Evaluate both primitives and solve for y; preserve the same explicit family shape and local domain. This route is an independent value/prose template, not merged with another primitive inversion.

### 3. Components and complete choice-bank mapping

| Source option (exact captured value) | Recipe position | Value at changed component a=2 | Correct |
|---|---:|---|---|
| `y=K{e}^{-3/x}` | `spec(q-158009, a)[bank][0]` | `K*exp(-2/x)` | False |
| `y=K{e}^{-x}-3` | `spec(q-158009, a)[bank][1]` | `K*exp(-x) - 2` | False |
| `y=K{e}^{1/x}+3` | `spec(q-158009, a)[bank][2]` | `K*exp(1/x) + 2` | False |
| `y=K{e}^{x}+3` | `spec(q-158009, a)[bank][3]` | `K*exp(x) + 2` | False |
| `y=K{e}^{-1/x}-3` | `spec(q-158009, a)[bank][4]` | `K*exp(-1/x) - 2` | True |

Each recipe is the explicit symbolic expression in the named spec branch. The bank is selected whole; pairwise family equivalence is checked modulo constant rescaling/shifts. Evidence shapes with obscure distractor intent remain interpreted only as parameterized expressions, not recovered error operations. Coefficient dependencies for these shapes are design choices anchored to their observed forms.

### 4. Reusable masks and constraints

Worked-solution math-block row counts: [4, 3, 1, 4, 3]. The opening, integration, implicit-form and explicit-form prose remains unchanged in observed replay. The mask contains complete coefficient terms, collected integrands and corresponding primitive components; replacement order cannot alter already-rendered text. At a changed component, the original stage count and route remain fixed.

Local domain: `x\ne0,\quad K\ne0`. Sampling/explicit guards: integer coefficient a=1..8. Public observed profiles retain the whole evidence bank. Normal output applies documented teaching/domain repairs and uses authored whole operation banks where listed below. For the blank, the entire expected answer fragment is x^(a+1), reinserted into the actual displayed -(a+1)(fragment+K)^(-1) family and independently differentiated.

Actual mathematical slot map (a=2):

```json
{
  "& =3": "& =2",
  "=3$": "=2$",
  "y+3": "y+2",
  "y\\ne -3": "y\\ne -2",
  "-3.": "-2."
}
```

## q-158010 / source 17592186275406

### 1. Specific source

Find the general solution to the differential equation $\sqrt{1-{x}^{2}}\,{y}^{′}-y=0$ for $y\ne 0$ and $|x|<1.$

Observed difficulty hard, field :answer-field.type/radio, key selection. Original component a=1. Exact forms and complete raw prose are preserved in source.json and source-cases.json. No plots.

### 2. Shared pattern

Separate as g(y)y′=f(x), with g(y)=1/y, f(x)=1/sqrt(1 - x**2). Evaluate both primitives and solve for y; preserve the same explicit family shape and local domain. This route is an independent value/prose template, not merged with another primitive inversion.

### 3. Components and complete choice-bank mapping

| Source option (exact captured value) | Recipe position | Value at changed component a=2 | Correct |
|---|---:|---|---|
| `y=K{e}^{1/\sqrt{1-{x}^{2}}}` | `spec(q-158010, a)[bank][0]` | `K*exp(2/sqrt(1 - x**2))` | False |
| `y=K{e}^{\operatorname{arcsin}⁡x}` | `spec(q-158010, a)[bank][1]` | `K*exp(2*asin(x))` | True |
| `y=K{e}^{\operatorname{arctan}⁡x}` | `spec(q-158010, a)[bank][2]` | `K*exp(2*atan(x))` | False |
| `y=K{e}^{\operatorname{sin}⁡x}` | `spec(q-158010, a)[bank][3]` | `K*exp(2*sin(x))` | False |
| `y=K{e}^{\sqrt{1-{x}^{2}}}` | `spec(q-158010, a)[bank][4]` | `K*exp(2*sqrt(1 - x**2))` | False |

Each recipe is the explicit symbolic expression in the named spec branch. The bank is selected whole; pairwise family equivalence is checked modulo constant rescaling/shifts. Evidence shapes with obscure distractor intent remain interpreted only as parameterized expressions, not recovered error operations. Coefficient dependencies for these shapes are design choices anchored to their observed forms.

### 4. Reusable masks and constraints

Worked-solution math-block row counts: [4, 3, 1, 4, 1]. The opening, integration, implicit-form and explicit-form prose remains unchanged in observed replay. The mask contains complete coefficient terms, collected integrands and corresponding primitive components; replacement order cannot alter already-rendered text. At a changed component, the original stage count and route remain fixed.

Local domain: `|x|<1,\quad K\ne0`. Sampling/explicit guards: integer coefficient a=1..8. Public observed profiles retain the whole evidence bank. Normal output applies documented teaching/domain repairs and uses authored whole operation banks where listed below. For the blank, the entire expected answer fragment is x^(a+1), reinserted into the actual displayed -(a+1)(fragment+K)^(-1) family and independently differentiated.

Actual mathematical slot map (a=2):

```json
{
  "-y &": "-2y &",
  "-y=0": "-2y=0",
  "& =y": "& =2y",
  "\\frac{1}{\\sqrt{1-{x}^{2}}}": "\\frac{2}{\\sqrt{1-{x}^{2}}}",
  "\\operatorname{arcsin}⁡x": "2\\operatorname{arcsin}⁡x"
}
```

## q-3854 / source 17592186326690

### 1. Specific source

Find the general solution to the differential equation ${y}^{′}=2yx+y{x}^{2}$ for $y\ne 0.$

Observed difficulty hard, field :answer-field.type/radio, key selection. Original component a=2. Exact forms and complete raw prose are preserved in source.json and source-cases.json. No plots.

### 2. Shared pattern

Separate as g(y)y′=f(x), with g(y)=1/y, f(x)=x**2 + 2*x. Evaluate both primitives and solve for y; preserve the same explicit family shape and local domain. This route is an independent value/prose template, not merged with another primitive inversion.

### 3. Components and complete choice-bank mapping

| Source option (exact captured value) | Recipe position | Value at changed component a=2 | Correct |
|---|---:|---|---|
| `y={e}^{{x}^{2}}+{e}^{{x}^{3}}+K` | `spec(q-3854, a)[bank][0]` | `K + exp(x**2) + exp(x**3)` | False |
| `y=K{e}^{{x}^{2}+{x}^{3}/3}` | `spec(q-3854, a)[bank][1]` | `K*exp(x**3/3 + x**2)` | True |
| `y={x}^{2}+\frac{{x}^{3}}{3}+K` | `spec(q-3854, a)[bank][2]` | `K + x**3/3 + x**2` | False |
| `y=\operatorname{ln}⁡{x}^{2}+\operatorname{ln}⁡\frac{{x}^{3}}{3}+K` | `spec(q-3854, a)[bank][3]` | `K + log(x**2) + log(x**3/3)` | False |
| `y=\operatorname{ln}⁡{x}^{2}+\operatorname{ln}⁡{x}^{3}+K` | `spec(q-3854, a)[bank][4]` | `K + log(x**2) + log(x**3)` | False |

Each recipe is the explicit symbolic expression in the named spec branch. The bank is selected whole; pairwise family equivalence is checked modulo constant rescaling/shifts. Evidence shapes with obscure distractor intent remain interpreted only as parameterized expressions, not recovered error operations. Coefficient dependencies for these shapes are design choices anchored to their observed forms.

### 4. Reusable masks and constraints

Worked-solution math-block row counts: [4, 3, 1, 4, 1]. The opening, integration, implicit-form and explicit-form prose remains unchanged in observed replay. The mask contains complete coefficient terms, collected integrands and corresponding primitive components; replacement order cannot alter already-rendered text. At a changed component, the original stage count and route remain fixed.

Local domain: `K\ne0`. Sampling/explicit guards: integer coefficient a=1..8. Public observed profiles retain the whole evidence bank. Normal output applies documented teaching/domain repairs and uses authored whole operation banks where listed below. For the blank, the entire expected answer fragment is x^(a+1), reinserted into the actual displayed -(a+1)(fragment+K)^(-1) family and independently differentiated.

Actual mathematical slot map (a=2):

```json
{
  "2yx": "2yx",
  "2x+{x}^{2}": "2x+{x}^{2}",
  "{x}^{2}+\\frac{{x}^{3}}{3}": "{x}^{2}+\\frac{{x}^{3}}{3}",
  "{x}^{2}+{x}^{3}/3": "{x}^{2}+{x}^{3}/3"
}
```

## q-79660 / source 17592186348250

### 1. Specific source

Find the general solution to the differential equation $(xy)^{2}\,\frac{\text{d}y}{\text{d}x}=1$ for $x\ne 0.$

Observed difficulty moderate, field :answer-field.type/radio, key selection. Original component a=1. Exact forms and complete raw prose are preserved in source.json and source-cases.json. No plots.

### 2. Shared pattern

Separate as g(y)y′=f(x), with g(y)=y**2, f(x)=x**(-2). Evaluate both primitives and solve for y; preserve the same explicit family shape and local domain. This route is an independent value/prose template, not merged with another primitive inversion.

### 3. Components and complete choice-bank mapping

| Source option (exact captured value) | Recipe position | Value at changed component a=2 | Correct |
|---|---:|---|---|
| `y=\sqrt[3]{\frac{K}{x}+1}` | `spec(q-79660, a)[bank][0]` | `(2*K/x + 1)**(1/3)` | False |
| `y=\sqrt[3]{K-\frac{1}{x}}` | `spec(q-79660, a)[bank][1]` | `(K - 2/x)**(1/3)` | False |
| `y=\sqrt{K+\frac{1}{x}}` | `spec(q-79660, a)[bank][2]` | `sqrt(K + 2/x)` | False |
| `y=\sqrt{K-\frac{2}{x}}` | `spec(q-79660, a)[bank][3]` | `sqrt(K - 4/x)` | False |
| `y=\sqrt[3]{K-\frac{3}{x}}` | `spec(q-79660, a)[bank][4]` | `(K - 6/x)**(1/3)` | True |

Each recipe is the explicit symbolic expression in the named spec branch. The bank is selected whole; pairwise family equivalence is checked modulo constant rescaling/shifts. Evidence shapes with obscure distractor intent remain interpreted only as parameterized expressions, not recovered error operations. Coefficient dependencies for these shapes are design choices anchored to their observed forms.

### 4. Reusable masks and constraints

Worked-solution math-block row counts: [3, 3, 1, 4]. The opening, integration, implicit-form and explicit-form prose remains unchanged in observed replay. The mask contains complete coefficient terms, collected integrands and corresponding primitive components; replacement order cannot alter already-rendered text. At a changed component, the original stage count and route remain fixed.

Local domain: `x\ne0,\quad K-3a/x\ne0`. Sampling/explicit guards: integer coefficient a=1..8. Public observed profiles retain the whole evidence bank. Normal output applies documented teaching/domain repairs and uses authored whole operation banks where listed below. For the blank, the entire expected answer fragment is x^(a+1), reinserted into the actual displayed -(a+1)(fragment+K)^(-1) family and independently differentiated.

Actual mathematical slot map (a=2):

```json
{
  "& =1": "& =2",
  "=1$": "=2$",
  "\\frac{1}{{x}^{2}}": "\\frac{2}{{x}^{2}}",
  "\\frac{1}{x}": "\\frac{2}{x}",
  "\\frac{3}{x}": "\\frac{6}{x}"
}
```

## q-79663 / source 17592186348251

### 1. Specific source

Find the general solution to the differential equation ${y}^{′}-2xy=3{x}^{2}y$ for $y\ne 0.$

Observed difficulty hard, field :answer-field.type/radio, key selection. Original component a=2. Exact forms and complete raw prose are preserved in source.json and source-cases.json. No plots.

### 2. Shared pattern

Separate as g(y)y′=f(x), with g(y)=1/y, f(x)=3*x**2 + 2*x. Evaluate both primitives and solve for y; preserve the same explicit family shape and local domain. This route is an independent value/prose template, not merged with another primitive inversion.

### 3. Components and complete choice-bank mapping

| Source option (exact captured value) | Recipe position | Value at changed component a=2 | Correct |
|---|---:|---|---|
| `y=K{e}^{\sqrt{{x}^{3}+{x}^{2}}}` | `spec(q-79663, a)[bank][0]` | `K*exp(sqrt(x**3 + x**2))` | False |
| `y=K{e}^{\sqrt{3{x}^{2}+2x}}` | `spec(q-79663, a)[bank][1]` | `K*exp(sqrt(3*x**2 + 2*x))` | False |
| `y=K{e}^{{x}^{3}+{x}^{2}}` | `spec(q-79663, a)[bank][2]` | `K*exp(x**3 + x**2)` | True |
| `y=K{e}^{6x+2}` | `spec(q-79663, a)[bank][3]` | `K*exp(6*x + 2)` | False |
| `y=K{e}^{3{x}^{2}+2x}` | `spec(q-79663, a)[bank][4]` | `K*exp(3*x**2 + 2*x)` | False |

Each recipe is the explicit symbolic expression in the named spec branch. The bank is selected whole; pairwise family equivalence is checked modulo constant rescaling/shifts. Evidence shapes with obscure distractor intent remain interpreted only as parameterized expressions, not recovered error operations. Coefficient dependencies for these shapes are design choices anchored to their observed forms.

### 4. Reusable masks and constraints

Worked-solution math-block row counts: [5, 3, 1, 4, 1]. The opening, integration, implicit-form and explicit-form prose remains unchanged in observed replay. The mask contains complete coefficient terms, collected integrands and corresponding primitive components; replacement order cannot alter already-rendered text. At a changed component, the original stage count and route remain fixed.

Local domain: `K\ne0`. Sampling/explicit guards: integer coefficient a=1..8. Public observed profiles retain the whole evidence bank. Normal output applies documented teaching/domain repairs and uses authored whole operation banks where listed below. For the blank, the entire expected answer fragment is x^(a+1), reinserted into the actual displayed -(a+1)(fragment+K)^(-1) family and independently differentiated.

Actual mathematical slot map (a=2):

```json
{
  "2xy": "2xy",
  "3{x}^{2}+2x": "3{x}^{2}+2x",
  "{x}^{3}+{x}^{2}": "{x}^{3}+{x}^{2}"
}
```

## q-79664 / source 17592186348252

### 1. Specific source

Find the general solution to the differential equation ${y}^{′}-{y}^{2}=6{x}^{2}{y}^{2}$ for $y\ne 0.$

Observed difficulty moderate, field :answer-field.type/radio, key selection. Original component a=1. Exact forms and complete raw prose are preserved in source.json and source-cases.json. No plots.

### 2. Shared pattern

Separate as g(y)y′=f(x), with g(y)=y**(-2), f(x)=6*x**2 + 1. Evaluate both primitives and solve for y; preserve the same explicit family shape and local domain. This route is an independent value/prose template, not merged with another primitive inversion.

### 3. Components and complete choice-bank mapping

| Source option (exact captured value) | Recipe position | Value at changed component a=2 | Correct |
|---|---:|---|---|
| `y=\frac{1}{{x}^{3}+{x}^{2}}+C` | `spec(q-79664, a)[bank][0]` | `C + 1/(x**3 + 2*x**2)` | False |
| `y=-\frac{1}{2{x}^{3}+x+C}` | `spec(q-79664, a)[bank][1]` | `-1/(C + 2*x**3 + 2*x)` | True |
| `y=\frac{1}{{x}^{2}-x}+C` | `spec(q-79664, a)[bank][2]` | `C + 1/(x**2 - 2*x)` | False |
| `y=\frac{1}{{x}^{3}+{x}^{2}+C}` | `spec(q-79664, a)[bank][3]` | `1/(C + x**3 + 2*x**2)` | False |
| `y=-\frac{C}{2{x}^{3}+x}` | `spec(q-79664, a)[bank][4]` | `-C/(2*x**3 + 2*x)` | False |

Each recipe is the explicit symbolic expression in the named spec branch. The bank is selected whole; pairwise family equivalence is checked modulo constant rescaling/shifts. Evidence shapes with obscure distractor intent remain interpreted only as parameterized expressions, not recovered error operations. Coefficient dependencies for these shapes are design choices anchored to their observed forms.

### 4. Reusable masks and constraints

Worked-solution math-block row counts: [5, 3, 1, 1]. The opening, integration, implicit-form and explicit-form prose remains unchanged in observed replay. The mask contains complete coefficient terms, collected integrands and corresponding primitive components; replacement order cannot alter already-rendered text. At a changed component, the original stage count and route remain fixed.

Local domain: `2x^3+a x+C\ne0`. Sampling/explicit guards: integer coefficient a=1..8. Public observed profiles retain the whole evidence bank. Normal output applies documented teaching/domain repairs and uses authored whole operation banks where listed below. For the blank, the entire expected answer fragment is x^(a+1), reinserted into the actual displayed -(a+1)(fragment+K)^(-1) family and independently differentiated.

Actual mathematical slot map (a=2):

```json
{
  "-{y}^{2}": "-2{y}^{2}",
  "+{y}^{2}": "+2{y}^{2}",
  "6{x}^{2}+1": "6{x}^{2}+2",
  "2{x}^{3}+x": "2{x}^{3}+2x"
}
```

## q-79665 / source 17592186348253

### 1. Specific source

Find the general solution to the differential equation $\frac{1}{\sqrt{xy}}\,{y}^{′}=1$ for $y\ne 0.$

Observed difficulty moderate, field :answer-field.type/radio, key selection. Original component a=1. Exact forms and complete raw prose are preserved in source.json and source-cases.json. No plots.

### 2. Shared pattern

Separate as g(y)y′=f(x), with g(y)=1/sqrt(y), f(x)=sqrt(x). Evaluate both primitives and solve for y; preserve the same explicit family shape and local domain. This route is an independent value/prose template, not merged with another primitive inversion.

### 3. Components and complete choice-bank mapping

| Source option (exact captured value) | Recipe position | Value at changed component a=2 | Correct |
|---|---:|---|---|
| `y={({x}^{3}+K)}^{2}` | `spec(q-79665, a)[bank][0]` | `(K + 2*x**3)**2` | False |
| `y={(\frac{1}{3}{x}^{3/2}+K)}^{2}` | `spec(q-79665, a)[bank][1]` | `(K + 2*x**(3/2)/3)**2` | True |
| `y=\frac{1}{9}\,{x}^{3/2}+K` | `spec(q-79665, a)[bank][2]` | `K + 4*x**(3/2)/9` | False |
| `y=\frac{1}{9}\,{x}^{3}+K` | `spec(q-79665, a)[bank][3]` | `K + 4*x**3/9` | False |
| `y={(3{x}^{1/2}+K)}^{2}` | `spec(q-79665, a)[bank][4]` | `(K + 6*sqrt(x))**2` | False |

Each recipe is the explicit symbolic expression in the named spec branch. The bank is selected whole; pairwise family equivalence is checked modulo constant rescaling/shifts. Evidence shapes with obscure distractor intent remain interpreted only as parameterized expressions, not recovered error operations. Coefficient dependencies for these shapes are design choices anchored to their observed forms.

### 4. Reusable masks and constraints

Worked-solution math-block row counts: [4, 4, 1, 4]. The opening, integration, implicit-form and explicit-form prose remains unchanged in observed replay. The mask contains complete coefficient terms, collected integrands and corresponding primitive components; replacement order cannot alter already-rendered text. At a changed component, the original stage count and route remain fixed.

Local domain: `x>0,\quad a x^{3/2}/3+K>0`. Sampling/explicit guards: integer coefficient a=1..8. Public observed profiles retain the whole evidence bank. Normal output applies documented teaching/domain repairs and uses authored whole operation banks where listed below. For the blank, the entire expected answer fragment is x^(a+1), reinserted into the actual displayed -(a+1)(fragment+K)^(-1) family and independently differentiated.

Actual mathematical slot map (a=2):

```json
{
  "& =1": "& =2",
  "=1$": "=2$",
  "& =\\sqrt{x}": "& =2\\sqrt{x}",
  "\\int \\sqrt{x}": "\\int 2\\sqrt{x}",
  "\\int {x}^{1/2}": "\\int 2{x}^{1/2}",
  "\\frac{2}{3}{x}^{3/2}": "\\frac{4}{3}{x}^{3/2}",
  "\\frac{1}{3}{x}^{3/2}": "\\frac{2}{3}{x}^{3/2}"
}
```

## q-79666 / source 17592186348254

### 1. Specific source

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}+\frac{\operatorname{sin}⁡x}{2y}=0$ for $y>0.$

Observed difficulty moderate, field :answer-field.type/radio, key selection. Original component a=1. Exact forms and complete raw prose are preserved in source.json and source-cases.json. No plots.

### 2. Shared pattern

Separate as g(y)y′=f(x), with g(y)=2*y, f(x)=-sin(x). Evaluate both primitives and solve for y; preserve the same explicit family shape and local domain. This route is an independent value/prose template, not merged with another primitive inversion.

### 3. Components and complete choice-bank mapping

| Source option (exact captured value) | Recipe position | Value at changed component a=2 | Correct |
|---|---:|---|---|
| `y={e}^{\operatorname{cos}⁡x+C}` | `spec(q-79666, a)[bank][0]` | `exp(C + 2*cos(x))` | False |
| `y={e}^{\operatorname{sec}⁡x+C}` | `spec(q-79666, a)[bank][1]` | `exp(C + 2*sec(x))` | False |
| `y={e}^{\sqrt{\operatorname{cos}⁡x+C}}` | `spec(q-79666, a)[bank][2]` | `exp(sqrt(C + 2*cos(x)))` | False |
| `y=\sqrt{\operatorname{sec}⁡x+C}` | `spec(q-79666, a)[bank][3]` | `sqrt(C + 2*sec(x))` | False |
| `y=\sqrt{\operatorname{cos}⁡x+C}` | `spec(q-79666, a)[bank][4]` | `sqrt(C + 2*cos(x))` | True |

Each recipe is the explicit symbolic expression in the named spec branch. The bank is selected whole; pairwise family equivalence is checked modulo constant rescaling/shifts. Evidence shapes with obscure distractor intent remain interpreted only as parameterized expressions, not recovered error operations. Coefficient dependencies for these shapes are design choices anchored to their observed forms.

### 4. Reusable masks and constraints

Worked-solution math-block row counts: [3, 3, 1, 1]. The opening, integration, implicit-form and explicit-form prose remains unchanged in observed replay. The mask contains complete coefficient terms, collected integrands and corresponding primitive components; replacement order cannot alter already-rendered text. At a changed component, the original stage count and route remain fixed.

Local domain: `a\cos x+C>0`. Sampling/explicit guards: integer coefficient a=1..8. Public observed profiles retain the whole evidence bank. Normal output applies documented teaching/domain repairs and uses authored whole operation banks where listed below. For the blank, the entire expected answer fragment is x^(a+1), reinserted into the actual displayed -(a+1)(fragment+K)^(-1) family and independently differentiated.

Actual mathematical slot map (a=2):

```json
{
  "\\operatorname{sin}⁡x": "2\\operatorname{sin}⁡x",
  "\\operatorname{cos}⁡x": "2\\operatorname{cos}⁡x"
}
```

## q-8304 / source 17592186351479

### 1. Specific source

Find the general solution to the differential equation $\sqrt{xy}\,\frac{\text{d}y}{\text{d}x}=1.$

Observed difficulty moderate, field :answer-field.type/radio, key selection. Original component a=1. Exact forms and complete raw prose are preserved in source.json and source-cases.json. No plots.

### 2. Shared pattern

Separate as g(y)y′=f(x), with g(y)=sqrt(y), f(x)=1/sqrt(x). Evaluate both primitives and solve for y; preserve the same explicit family shape and local domain. This route is an independent value/prose template, not merged with another primitive inversion.

### 3. Components and complete choice-bank mapping

| Source option (exact captured value) | Recipe position | Value at changed component a=2 | Correct |
|---|---:|---|---|
| `y=3{x}^{1/3}+K` | `spec(q-8304, a)[bank][0]` | `K + 6*x**(1/3)` | False |
| `y=3{x}^{1/2}+K` | `spec(q-8304, a)[bank][1]` | `K + 6*sqrt(x)` | False |
| `y={(3{x}^{1/2}+K)}^{2/3}` | `spec(q-8304, a)[bank][2]` | `(K + 6*sqrt(x))**(2/3)` | True |
| `y={({x}^{1/2}+K)}^{2/3}` | `spec(q-8304, a)[bank][3]` | `(K + 2*sqrt(x))**(2/3)` | False |
| `y={({x}^{2/3}+K)}^{1/2}` | `spec(q-8304, a)[bank][4]` | `sqrt(K + 2*x**(2/3))` | False |

Each recipe is the explicit symbolic expression in the named spec branch. The bank is selected whole; pairwise family equivalence is checked modulo constant rescaling/shifts. Evidence shapes with obscure distractor intent remain interpreted only as parameterized expressions, not recovered error operations. Coefficient dependencies for these shapes are design choices anchored to their observed forms.

### 4. Reusable masks and constraints

Worked-solution math-block row counts: [3, 4, 1, 4]. The opening, integration, implicit-form and explicit-form prose remains unchanged in observed replay. The mask contains complete coefficient terms, collected integrands and corresponding primitive components; replacement order cannot alter already-rendered text. At a changed component, the original stage count and route remain fixed.

Local domain: `x>0,\quad 3a\sqrt{x}+K>0`. Sampling/explicit guards: integer coefficient a=1..8. Public observed profiles retain the whole evidence bank. Normal output applies documented teaching/domain repairs and uses authored whole operation banks where listed below. For the blank, the entire expected answer fragment is x^(a+1), reinserted into the actual displayed -(a+1)(fragment+K)^(-1) family and independently differentiated.

Actual mathematical slot map (a=2):

```json
{
  "& =1": "& =2",
  "=1.$": "=2.$",
  "\\frac{1}{\\sqrt{x}}": "\\frac{2}{\\sqrt{x}}",
  "\\int {x}^{-1/2}": "\\int 2{x}^{-1/2}",
  "2{x}^{1/2}": "4{x}^{1/2}",
  "3{x}^{1/2}": "6{x}^{1/2}"
}
```

## Authored easy templates

easy_linear: y′+a x y=0; separated g(y)=1/y, f(x)=-a x; primitive ln|y|=-a x²/2+C; family y=K exp(-a x²/2), K nonzero. easy_constant replaces a x by a and the primitive by -a x. The shared canonical prose and four logarithmic/exponential conversion rows are retained. Two independent easy examples for each template appear in review.

Each authored bank is selected whole: K exp(F), K exp(-F), exp(F)+K, K exp(f), F+K. These are explicit wrong sign, additive constant, missing integration and missing exponentiation operations. All 24 allowed signed a values per template are checked; no absent source easy label is claimed as observed.

## Whole authored normal banks for uncertain evidence

The public observed profile preserves every original expression bank and the source masks remain parameterized. Its less clear dependencies are evidence-pattern extrapolations, never claimed as recovered error intent. Default profile authored is a separate complete bank for q14247, q14253, q158009, q79660, q79664, q79665 and q8304; profile repaired is an alias of the same normal presentation at those routes.

- q14247: correct exponential family; negate F; put K additively after exponentiation; use f instead of F; omit the primitive of the nonzero constant term.
- q14253/q79664: correct negative reciprocal; omit the minus sign; omit reciprocal inversion; put C outside inversion; use f instead of F.
- q158009: correct affine-y exponential; negate F; add K after exponentiating; use the wrong final y shift; use f instead of F.
- q79660: correct cube root; omit the factor three from the y primitive; square root instead of cube root; omit the cube root; negate F.
- q79665: correct square of the solved positive sqrt(y) primitive; omit division by two; omit squaring; cube instead of square; use the x integrand as primitive.
- q8304: correct power two-thirds; omit inversion; omit multiplication by three; square instead of power two-thirds; square root instead of power two-thirds.

Every complete authored bank uses the actual displayed f/F and solved shape, has five options, and rejects an entire instance for equivalent families or missing members. These recipes are metadata, not learner-facing diagnoses. Observed changed-parameter examples and separately labeled authored-bank variants appear in review.

## Blank family-versus-fragment grading

In q128191, x^n+5 can be absorbed into arbitrary K and thus gives the same complete family, but the native grader judges the displayed field fragment against x^n. Normal prompts minimally specify “Give the nonconstant polynomial term; put the integration constant in K.” Observed prompt stays raw-exact. Native checks accept x*x*... as an independent equivalent polynomial product, reject a wrong power/coefficient, and explicitly record rejection of the family-equivalent shifted fragment. This is a documented source grading limitation, not an unresolved engine failure or a mathematical failure of the whole family.

## Final verification

The full matrix passed for 156 normal finite-domain instances with 156 distinct assessed ODEs. Source replay matches every bank value (66/66), designation (14/14), prompt (14/14 raw-exact), and full worked solution (14/14 raw-exact). Changed observed-bank profiles remain evidence-only when source errors apply. Normal default correctness and grading are separate checks; 79 native accepted checks and 291 rejected checks have no unresolved outcomes. Supplementary domain validation reads the displayed cube-root option and checks its real derivative on both signs of x and y; pole and zero-radicand points are excluded, with no principal-complex-power assumption.
