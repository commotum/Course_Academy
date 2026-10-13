# Four-stage template extraction
## 1. Specific source descriptions
The capture is math at basis 1356. All source candidates are explicit functions y=f(x); the independent variable is x and derivative is dy/dx. Five text subset choices belong to one radio field. Signs and constant shifts are retained, and domains are the common real ODE/function domain (x≠0 for powers, positive x for logarithms, excluding trig poles).
- **q-141096**: RHS `$-2y$`; candidates $-2{e}^{-2x}$, $-2{e}^{x}$, $2{e}^{-x}+1$. Ordered substitution rows per candidate: [3, 4, 4]. Exact prompt and full worked solution remain in `source.json` and `review.md`.
- **q-79335**: RHS `$\frac{2y}{x}-2,$`; candidates $2x$, ${x}^{2}$, ${x}^{3}$. Ordered substitution rows per candidate: [5, 5, 5]. Exact prompt and full worked solution remain in `source.json` and `review.md`.
- **q-141091**: RHS `$2y\operatorname{cot}⁡2x$`; candidates $\operatorname{sin}⁡2x$, $\operatorname{sin}⁡2x+1$, $-3\operatorname{sin}⁡2x$. Ordered substitution rows per candidate: [3, 4, 3]. Exact prompt and full worked solution remain in `source.json` and `review.md`.
- **q-141092**: RHS `$-y\operatorname{tan}⁡x$`; candidates $\operatorname{cos}⁡x$, $3\operatorname{cos}⁡x$, $-2\operatorname{cos}⁡x$. Ordered substitution rows per candidate: [3, 3, 3]. Exact prompt and full worked solution remain in `source.json` and `review.md`.
- **q-141093**: RHS `$\frac{2}{{e}^{y/2}}$`; candidates $\operatorname{ln}⁡x$, $2\operatorname{ln}⁡x$, $-\operatorname{ln}⁡x$. Ordered substitution rows per candidate: [5, 4, 6]. Exact prompt and full worked solution remain in `source.json` and `review.md`.
- **q-141098**: RHS `$\frac{4y}{x},$`; candidates $4x$, $2{x}^{2}$, ${x}^{3}$. Ordered substitution rows per candidate: [3, 4, 4]. Exact prompt and full worked solution remain in `source.json` and `review.md`.
- **q-141099**: RHS `$-\frac{2y}{x},$`; candidates $-\frac{1}{x}$, $-\frac{1}{{x}^{2}}$, $\frac{4}{{x}^{2}}$. Ordered substitution rows per candidate: [4, 3, 3]. Exact prompt and full worked solution remain in `source.json` and `review.md`.
- **q-141101**: RHS `$\frac{5y}{x},$`; candidates ${x}^{5}$, ${x}^{10}$, $5{x}^{4}$. Ordered substitution rows per candidate: [3, 4, 4]. Exact prompt and full worked solution remain in `source.json` and `review.md`.
- **q-141103**: RHS `$\frac{1}{{e}^{3y}}$`; candidates $\operatorname{ln}⁡x$, $-\operatorname{ln}⁡x$, $-2\operatorname{ln}⁡x$. Ordered substitution rows per candidate: [5, 7, 7]. Exact prompt and full worked solution remain in `source.json` and `review.md`.
- **q-79330**: RHS `$4y$`; candidates ${e}^{-4x}$, ${e}^{4x}$, $4{e}^{x}$. Ordered substitution rows per candidate: [3, 2, 4]. Exact prompt and full worked solution remain in `source.json` and `review.md`.
- **q-79333**: RHS `$-\frac{y}{x},$`; candidates $\frac{7}{x}$, $-\frac{1}{x}$, $\frac{2}{x}$. Ordered substitution rows per candidate: [3, 3, 3]. Exact prompt and full worked solution remain in `source.json` and `review.md`.

## 2. Generalized pattern and purpose
Differentiate all three proposed functions; substitute each derivative and complete candidate into the displayed first-order equation; test equality as an identity over the common stated domain. Return the complete subset, including None and all three. Do not find a general solution or an integration constant. Source banks express logical response patterns rather than erroneous derivative values: each recipe is the fixed subset of proposition indices. There is no inferred numerical distractor intent.

## 3. Component, answer-bank and ordered-stage mapping
Each original choice is represented by its actual text and its exact bit mask (I=1, II=2, III=4). This preserves the complete response criterion. The source correct designation is independently recomputed from all three functions, not looked up.
### q-141096 / bank q-141096
| Source field | Exact choice text | Recipe / semantic subset | Source designation |
|---|---|---|---|
| selection | II only | bit mask 2 | incorrect |
| selection | III only | bit mask 4 | incorrect |
| selection | I, II, and III | bit mask 7 | incorrect |
| selection | I only | bit mask 1 | correct |
| selection | None | bit mask 0 | incorrect |

Candidate component slots and exact derivatives:

- `$y=-2{e}^{-2x}$`; computed derivative `$4 e^{- 2 x}$`.
- `$y=-2{e}^{x}$`; computed derivative `$- 2 e^{x}$`.
- `$y=2{e}^{-x}+1$`; computed derivative `$- 2 e^{- x}$`.

Complete original ordered mathematical component rows (retained with original relation tokens):

Candidate 1:

```tex
\frac{\text{d}y}{\text{d}x} & =-2y \\ 4{e}^{-2x} & \overset{?}{=}-2(-2{e}^{-2x}) \\ 4{e}^{-2x} & =4{e}^{-2x}.\,✓
```

Candidate 2:

```tex
\frac{\text{d}y}{\text{d}x} & =-2y \\ -2{e}^{x} & \overset{?}{=}-2(-2{e}^{x}) \\ -2{e}^{x} & \overset{?}{=}4{e}^{x} \\ 0 & \ne 6{e}^{x}.\,\times 
```

Candidate 3:

```tex
\frac{\text{d}y}{\text{d}x} & =-2y \\ -2{e}^{-x} & \overset{?}{=}-2(2{e}^{-x}+1) \\ -2{e}^{-x} & \overset{?}{=}-4{e}^{-x}-2 \\ 2{e}^{-x} & \ne -2.\,\times 
```

### q-79335 / bank q-79335
| Source field | Exact choice text | Recipe / semantic subset | Source designation |
|---|---|---|---|
| selection | II only | bit mask 2 | incorrect |
| selection | I and III only | bit mask 5 | incorrect |
| selection | I and II only | bit mask 3 | incorrect |
| selection | I only | bit mask 1 | correct |
| selection | II and III only | bit mask 6 | incorrect |

Candidate component slots and exact derivatives:

- `$y=2x$`; computed derivative `$2$`.
- `$y={x}^{2}$`; computed derivative `$2 x$`.
- `$y={x}^{3}$`; computed derivative `$3 x^{2}$`.

Complete original ordered mathematical component rows (retained with original relation tokens):

Candidate 1:

```tex
\frac{\text{d}y}{\text{d}x} & =\frac{2y}{x}-2 \\ 2 & \overset{?}{=}\frac{2\cdot 2x}{x}-2 \\ 2 & \overset{?}{=}\frac{4x}{x}-2 \\ 2 & \overset{?}{=}4-2 \\ 2 & =2.\,✓
```

Candidate 2:

```tex
\frac{\text{d}y}{\text{d}x} & =\frac{2y}{x}-2 \\ 2x & \overset{?}{=}\frac{2\cdot {x}^{2}}{x}-2 \\ 2x & \overset{?}{=}\frac{2{x}^{2}}{x}-2 \\ 2x & \overset{?}{=}2x-2 \\ 0 & \ne -2.\,\times 
```

Candidate 3:

```tex
\frac{\text{d}y}{\text{d}x} & =\frac{2y}{x}-2 \\ 3{x}^{2} & \overset{?}{=}\frac{2\cdot {x}^{3}}{x}-2 \\ 3{x}^{2} & \overset{?}{=}\frac{2{x}^{3}}{x}-2 \\ 3{x}^{2} & \overset{?}{=}2{x}^{2}-2 \\ {x}^{2} & \ne -2\,\times 
```

### q-141091 / bank q-141091
| Source field | Exact choice text | Recipe / semantic subset | Source designation |
|---|---|---|---|
| selection | I and III only | bit mask 5 | correct |
| selection | III only | bit mask 4 | incorrect |
| selection | II only | bit mask 2 | incorrect |
| selection | I only | bit mask 1 | incorrect |
| selection | I and II only | bit mask 3 | incorrect |

Candidate component slots and exact derivatives:

- `$y=\operatorname{sin}⁡2x$`; computed derivative `$2 \cos{\left(2 x \right)}$`.
- `$y=\operatorname{sin}⁡2x+1$`; computed derivative `$2 \cos{\left(2 x \right)}$`.
- `$y=-3\operatorname{sin}⁡2x$`; computed derivative `$- 6 \cos{\left(2 x \right)}$`.

Complete original ordered mathematical component rows (retained with original relation tokens):

Candidate 1:

```tex
\frac{\text{d}y}{\text{d}x} & =2y\operatorname{cot}⁡2x \\ 2\operatorname{cos}⁡2x & \overset{?}{=}2\operatorname{sin}⁡2x\cdot \operatorname{cot}⁡2x \\ 2\operatorname{cos}⁡2x & =2\operatorname{cos}⁡2x.\,✓
```

Candidate 2:

```tex
\frac{\text{d}y}{\text{d}x} & =2y\operatorname{cot}⁡2x \\ 2\operatorname{cos}⁡2x & \overset{?}{=}2(\operatorname{sin}⁡2x+1)\operatorname{cot}⁡2x \\ 2\operatorname{cos}⁡2x & \overset{?}{=}2\operatorname{cos}⁡2x+2\operatorname{cot}⁡2x \\ 0 & =2\operatorname{cot}⁡2x.\,\times 
```

Candidate 3:

```tex
\frac{\text{d}y}{\text{d}x} & =2y\operatorname{cot}⁡2x \\ -6\operatorname{cos}⁡2x & \overset{?}{=}2(-3\operatorname{sin}⁡2x)\cdot \operatorname{cot}⁡2x \\ -6\operatorname{cos}⁡2x & =-6\operatorname{cos}⁡2x.\,✓
```

### q-141092 / bank q-141092
| Source field | Exact choice text | Recipe / semantic subset | Source designation |
|---|---|---|---|
| selection | III only | bit mask 4 | incorrect |
| selection | I only | bit mask 1 | incorrect |
| selection | I and II only | bit mask 3 | incorrect |
| selection | I, II, and III | bit mask 7 | correct |
| selection | II only | bit mask 2 | incorrect |

Candidate component slots and exact derivatives:

- `$y=\operatorname{cos}⁡x$`; computed derivative `$- \sin{\left(x \right)}$`.
- `$y=3\operatorname{cos}⁡x$`; computed derivative `$- 3 \sin{\left(x \right)}$`.
- `$y=-2\operatorname{cos}⁡x$`; computed derivative `$2 \sin{\left(x \right)}$`.

Complete original ordered mathematical component rows (retained with original relation tokens):

Candidate 1:

```tex
\frac{\text{d}y}{\text{d}x} & =-y\operatorname{tan}⁡x \\ -\operatorname{sin}⁡x & \overset{?}{=}-\operatorname{cos}⁡x\cdot \operatorname{tan}⁡x \\ -\operatorname{sin}⁡x & =-\operatorname{sin}⁡x.\,✓
```

Candidate 2:

```tex
\frac{\text{d}y}{\text{d}x} & =-y\operatorname{tan}⁡x \\ -3\operatorname{sin}⁡x & \overset{?}{=}-3\operatorname{cos}⁡x\cdot \operatorname{tan}⁡x \\ -3\operatorname{sin}⁡x & =-3\operatorname{sin}⁡x.\,✓
```

Candidate 3:

```tex
\frac{\text{d}y}{\text{d}x} & =-y\operatorname{tan}⁡x \\ 2\operatorname{sin}⁡x & \overset{?}{=}-(-2\operatorname{cos}⁡x)\cdot \operatorname{tan}⁡x \\ 2\operatorname{sin}⁡x & =2\operatorname{sin}⁡x.\,✓
```

### q-141093 / bank q-141093
| Source field | Exact choice text | Recipe / semantic subset | Source designation |
|---|---|---|---|
| selection | I and III only | bit mask 5 | incorrect |
| selection | III only | bit mask 4 | incorrect |
| selection | II and III only | bit mask 6 | incorrect |
| selection | II only | bit mask 2 | correct |
| selection | I only | bit mask 1 | incorrect |

Candidate component slots and exact derivatives:

- `$y=\operatorname{ln}⁡x$`; computed derivative `$\frac{1}{x}$`.
- `$y=2\operatorname{ln}⁡x$`; computed derivative `$\frac{2}{x}$`.
- `$y=-\operatorname{ln}⁡x$`; computed derivative `$- \frac{1}{x}$`.

Complete original ordered mathematical component rows (retained with original relation tokens):

Candidate 1:

```tex
\frac{\text{d}y}{\text{d}x} & =\frac{2}{{e}^{y/2}} \\ \frac{1}{x} & \overset{?}{=}\frac{2}{{e}^{(\operatorname{ln}⁡x)/2}} \\ \frac{1}{x} & \overset{?}{=}\frac{2}{{e}^{\operatorname{ln}⁡\sqrt{x}}} \\ \frac{1}{x} & =\frac{2}{\sqrt{x}} \\ 1 & =2\sqrt{x}.\,\times 
```

Candidate 2:

```tex
\frac{\text{d}y}{\text{d}x} & =\frac{2}{{e}^{y/2}} \\ \frac{2}{x} & \overset{?}{=}\frac{2}{{e}^{(2\operatorname{ln}⁡x)/2}} \\ \frac{2}{x} & \overset{?}{=}\frac{2}{{e}^{\operatorname{ln}⁡x}} \\ \frac{2}{x} & =\frac{2}{x}.\,✓
```

Candidate 3:

```tex
\frac{\text{d}y}{\text{d}x} & =\frac{2}{{e}^{y/2}} \\ -\frac{1}{x} & \overset{?}{=}\frac{2}{{e}^{(-\operatorname{ln}⁡x)/2}} \\ -\frac{1}{x} & \overset{?}{=}\frac{2}{{e}^{\operatorname{ln}⁡({x}^{-1/2})}} \\ -\frac{1}{x} & \overset{?}{=}\frac{2}{{x}^{-1/2}} \\ -\frac{1}{x} & =2\sqrt{x} \\ -1 & =2x\sqrt{x}.\,\times 
```

### q-141098 / bank q-141098
| Source field | Exact choice text | Recipe / semantic subset | Source designation |
|---|---|---|---|
| selection | III only | bit mask 4 | incorrect |
| selection | I and II only | bit mask 3 | incorrect |
| selection | None | bit mask 0 | correct |
| selection | I only | bit mask 1 | incorrect |
| selection | II and III only | bit mask 6 | incorrect |

Candidate component slots and exact derivatives:

- `$y=4x$`; computed derivative `$4$`.
- `$y=2{x}^{2}$`; computed derivative `$4 x$`.
- `$y={x}^{3}$`; computed derivative `$3 x^{2}$`.

Complete original ordered mathematical component rows (retained with original relation tokens):

Candidate 1:

```tex
\frac{\text{d}y}{\text{d}x} & =\frac{4y}{x} \\ 4 & \overset{?}{=}\frac{4(4x)}{x} \\ 4 & \ne 16.\,\times 
```

Candidate 2:

```tex
\frac{\text{d}y}{\text{d}x} & =\frac{4y}{x} \\ 4x & \overset{?}{=}\frac{4(2{x}^{2})}{x} \\ 4x & \overset{?}{=}8x \\ -4x & \ne 0.\,\times 
```

Candidate 3:

```tex
\frac{\text{d}y}{\text{d}x} & =\frac{4y}{x} \\ 3{x}^{2} & \overset{?}{=}\frac{4({x}^{3})}{x} \\ 3{x}^{2} & \ne 4{x}^{2} \\ 0 & \ne {x}^{2}.\,\times 
```

### q-141099 / bank q-141099
| Source field | Exact choice text | Recipe / semantic subset | Source designation |
|---|---|---|---|
| selection | I and II only | bit mask 3 | incorrect |
| selection | II and III only | bit mask 6 | correct |
| selection | II only | bit mask 2 | incorrect |
| selection | I only | bit mask 1 | incorrect |
| selection | III only | bit mask 4 | incorrect |

Candidate component slots and exact derivatives:

- `$y=-\frac{1}{x}$`; computed derivative `$\frac{1}{x^{2}}$`.
- `$y=-\frac{1}{{x}^{2}}$`; computed derivative `$\frac{2}{x^{3}}$`.
- `$y=\frac{4}{{x}^{2}}$`; computed derivative `$- \frac{8}{x^{3}}$`.

Complete original ordered mathematical component rows (retained with original relation tokens):

Candidate 1:

```tex
\frac{\text{d}y}{\text{d}x} & =-\frac{2y}{x} \\ \frac{1}{{x}^{2}} & \overset{?}{=}-\frac{2(-\frac{1}{x})}{x} \\ \frac{1}{{x}^{2}} & \overset{?}{=}\frac{2}{{x}^{2}} \\ 0 & \ne \frac{1}{{x}^{2}}.\,\times 
```

Candidate 2:

```tex
\frac{\text{d}y}{\text{d}x} & =-\frac{2y}{x} \\ \frac{2}{{x}^{3}} & \overset{?}{=}-\frac{2(-\frac{1}{{x}^{2}})}{x} \\ \frac{2}{{x}^{3}} & =\frac{2}{{x}^{3}}.\,✓
```

Candidate 3:

```tex
\frac{\text{d}y}{\text{d}x} & =-\frac{2y}{x} \\ -\frac{8}{{x}^{3}} & \overset{?}{=}-\frac{2(\frac{4}{{x}^{2}})}{x} \\ -\frac{8}{{x}^{3}} & =-\frac{8}{{x}^{3}}.\,✓
```

### q-141101 / bank q-141101
| Source field | Exact choice text | Recipe / semantic subset | Source designation |
|---|---|---|---|
| selection | II only | bit mask 2 | incorrect |
| selection | III only | bit mask 4 | incorrect |
| selection | I only | bit mask 1 | correct |
| selection | None | bit mask 0 | incorrect |
| selection | II and III only | bit mask 6 | incorrect |

Candidate component slots and exact derivatives:

- `$y={x}^{5}$`; computed derivative `$5 x^{4}$`.
- `$y={x}^{10}$`; computed derivative `$10 x^{9}$`.
- `$y=5{x}^{4}$`; computed derivative `$20 x^{3}$`.

Complete original ordered mathematical component rows (retained with original relation tokens):

Candidate 1:

```tex
\frac{\text{d}y}{\text{d}x} & =\frac{5y}{x} \\ 5{x}^{4} & \overset{?}{=}\frac{5({x}^{5})}{x} \\ 5{x}^{4} & =5{x}^{4}.\,✓
```

Candidate 2:

```tex
\frac{\text{d}y}{\text{d}x} & =\frac{5y}{x} \\ 10{x}^{9} & \overset{?}{=}\frac{5({x}^{10})}{x} \\ 10{x}^{9} & \overset{?}{=}5{x}^{9} \\ 5{x}^{9} & \ne 0.\,\times 
```

Candidate 3:

```tex
\frac{\text{d}y}{\text{d}x} & =\frac{5y}{x} \\ 20{x}^{3} & \overset{?}{=}\frac{5(5{x}^{4})}{x} \\ 20{x}^{3} & \overset{?}{=}25{x}^{3} \\ 0 & \ne 5{x}^{3}.\,\times 
```

### q-141103 / bank q-141103
| Source field | Exact choice text | Recipe / semantic subset | Source designation |
|---|---|---|---|
| selection | I and II only | bit mask 3 | incorrect |
| selection | III only | bit mask 4 | incorrect |
| selection | I and III only | bit mask 5 | incorrect |
| selection | None | bit mask 0 | correct |
| selection | II only | bit mask 2 | incorrect |

Candidate component slots and exact derivatives:

- `$y=\operatorname{ln}⁡x$`; computed derivative `$\frac{1}{x}$`.
- `$y=-\operatorname{ln}⁡x$`; computed derivative `$- \frac{1}{x}$`.
- `$y=-2\operatorname{ln}⁡x$`; computed derivative `$- \frac{2}{x}$`.

Complete original ordered mathematical component rows (retained with original relation tokens):

Candidate 1:

```tex
\frac{\text{d}y}{\text{d}x} & =\frac{1}{{e}^{3y}} \\ \frac{1}{x} & \overset{?}{=}\frac{1}{{e}^{3\operatorname{ln}⁡x}} \\ \frac{1}{x} & \overset{?}{=}\frac{1}{{e}^{\operatorname{ln}⁡({x}^{3})}} \\ \frac{1}{x} & =\frac{1}{{x}^{3}} \\ {x}^{2} & =1.\,\times 
```

Candidate 2:

```tex
\frac{\text{d}y}{\text{d}x} & =\frac{1}{{e}^{3y}} \\ -\frac{1}{x} & \overset{?}{=}\frac{1}{{e}^{3(-\operatorname{ln}⁡x)}} \\ -\frac{1}{x} & \overset{?}{=}\frac{1}{{e}^{-3\operatorname{ln}⁡x}} \\ -\frac{1}{x} & \overset{?}{=}\frac{1}{{e}^{\operatorname{ln}⁡({x}^{-3})}} \\ -\frac{1}{x} & \overset{?}{=}\frac{1}{{x}^{-3}} \\ -\frac{1}{x} & ={x}^{3} \\ -1 & ={x}^{4}.\,\times 
```

Candidate 3:

```tex
\frac{\text{d}y}{\text{d}x} & =\frac{1}{{e}^{3y}} \\ -\frac{2}{x} & \overset{?}{=}\frac{1}{{e}^{3(-2\operatorname{ln}⁡x)}} \\ -\frac{2}{x} & \overset{?}{=}\frac{1}{{e}^{-6\operatorname{ln}⁡x}} \\ -\frac{2}{x} & \overset{?}{=}\frac{1}{{e}^{\operatorname{ln}⁡({x}^{-6})}} \\ -\frac{2}{x} & \overset{?}{=}\frac{1}{{x}^{-6}} \\ -\frac{2}{x} & ={x}^{6} \\ -2 & ={x}^{7}.\,\times 
```

### q-79330 / bank q-79330
| Source field | Exact choice text | Recipe / semantic subset | Source designation |
|---|---|---|---|
| selection | II only | bit mask 2 | correct |
| selection | I only | bit mask 1 | incorrect |
| selection | II and III only | bit mask 6 | incorrect |
| selection | III only | bit mask 4 | incorrect |
| selection | I and III only | bit mask 5 | incorrect |

Candidate component slots and exact derivatives:

- `$y={e}^{-4x}$`; computed derivative `$- 4 e^{- 4 x}$`.
- `$y={e}^{4x}$`; computed derivative `$4 e^{4 x}$`.
- `$y=4{e}^{x}$`; computed derivative `$4 e^{x}$`.

Complete original ordered mathematical component rows (retained with original relation tokens):

Candidate 1:

```tex
\frac{\text{d}y}{\text{d}x} & =4y \\ -4{e}^{-4x} & \overset{?}{=}4{e}^{-4x} \\ 0 & \ne 8{e}^{-4x}.\,\times 
```

Candidate 2:

```tex
\frac{\text{d}y}{\text{d}x} & =4y \\ 4{e}^{4x} & =4{e}^{4x}.\,✓
```

Candidate 3:

```tex
\frac{\text{d}y}{\text{d}x} & =4y \\ 4{e}^{x} & \overset{?}{=}4(4{e}^{x}) \\ 4{e}^{x} & \overset{?}{=}16{e}^{x} \\ 0 & \ne 12{e}^{x}.\,\times 
```

### q-79333 / bank q-79333
| Source field | Exact choice text | Recipe / semantic subset | Source designation |
|---|---|---|---|
| selection | I and II only | bit mask 3 | incorrect |
| selection | II only | bit mask 2 | incorrect |
| selection | I, II, and III | bit mask 7 | correct |
| selection | III only | bit mask 4 | incorrect |
| selection | I and III only | bit mask 5 | incorrect |

Candidate component slots and exact derivatives:

- `$y=\frac{7}{x}$`; computed derivative `$- \frac{7}{x^{2}}$`.
- `$y=-\frac{1}{x}$`; computed derivative `$\frac{1}{x^{2}}$`.
- `$y=\frac{2}{x}$`; computed derivative `$- \frac{2}{x^{2}}$`.

Complete original ordered mathematical component rows (retained with original relation tokens):

Candidate 1:

```tex
\frac{\text{d}y}{\text{d}x} & =-\frac{y}{x} \\ -\frac{7}{{x}^{2}} & \overset{?}{=}-\frac{(\frac{7}{x})}{x} \\ -\frac{7}{{x}^{2}} & =-\frac{7}{{x}^{2}}.\,✓
```

Candidate 2:

```tex
\frac{\text{d}y}{\text{d}x} & =-\frac{y}{x} \\ \frac{1}{{x}^{2}} & \overset{?}{=}-\frac{(-\frac{1}{x})}{x} \\ \frac{1}{{x}^{2}} & =\frac{1}{{x}^{2}}.\,✓
```

Candidate 3:

```tex
\frac{\text{d}y}{\text{d}x} & =-\frac{y}{x} \\ -\frac{2}{{x}^{2}} & \overset{?}{=}-\frac{(\frac{2}{x})}{x} \\ -\frac{2}{{x}^{2}} & =-\frac{2}{{x}^{2}}.\,✓
```


## 4. Reusable masks, constraints and calculations
The fixed structure is the exact prompt prose, three proposed-function bullets,
shared opening sentences, three differentiating/substituting paragraphs, each
original aligned row sequence, each original truth judgment and the final subset
sentence. Variable slots are **complete mathematical components**, not short
text substitutions. `source_render` extracts math-delimited blocks; inline y=F
and dy/dx=G have component slots, and each aligned row has separate LHS, relation,
RHS and punctuation/tick components. Domain/prose fragments are fixed. At the
unity specialization each component renders its original spelling. This is a
mask renderer, not a literal source-record return.

The observed replay parameter is a nonzero integer dependent scale c of magnitude
at most 6. From source candidates f_i and source RHS F(x,y), it computes
`c*f_i`, `c*f_i'` and `c*F(x,y/c)`. Every nonformal comparison component is multiplied
by c, while the formal RHS substitutes y/c and multiplies by c. Ordered operations,
optional row omissions, punctuation and all fixed prose remain unchanged. This
transformation generalizes the whole equation and every displayed intermediate,
including nonlinear logarithmic substitution, without an answer lookup table.
It is explicitly a fidelity stress transformation; no source-intent recovery or
meaningful task-variety credit is claimed for c. The same public API returns raw
original evidence with c=1 and generated source-mask variants with c=2 and c=-3.
Original profile banks remain intact; the complete logical subset is calculated.

Authored defaults use separately labeled `authored_subset` banks. A complete bank
is selected together: the computed subset and four distinct other semantic subsets
among the remaining seven. Bank selection is deterministic from the mathematical
parameters and is independent of shuffle seed. All five options have distinct
response meanings; none is a partial-credit answer. This does not invent derivative
error intent or learner-facing distractor feedback. Duplicate candidate functions
reject the whole sampled instance rather than substituting individual options.

Normal worked solutions preserve the shared method prose and provide one fixed
solution checking all three candidates: original equation; full unreduced
substitution; reduction; identity/nonidentity decision. Log variants additionally
show the explicit power-of-x logarithm stage before exponent cancellation. Source
row counts and omissions remain exact only for their original masks; authored
stage sequences are clearly labeled rather than claimed as observed.

# Source notation and domain findings

The raw q-141091 second candidate writes `0=2 cot(2x)` followed by ×; q-141093 and
q-141103 write ordinary equal signs during failed comparisons and end them with ×.
The correct subset designations and all 55 source answer values are mathematically
sound. These equalities are failed *tests*, not true identities. Raw original
replay preserves their exact notation and is tagged `evidence_only=true`,
`eligible_for_learning=false`. Authored learner output uses query relations and
states that the final residual is not identically zero. It does not assert that a
nonzero residual is nonzero at every isolated x. This is a notation/teaching
repair, not a changed source bank or correct designation. Exact raw solution
reproduction and corrected normal presentation are reported separately.

Logarithmic candidates imply x>0 even though raw source prompts omit that explicit
restriction. Raw replay preserves the prompt and uses the common real domain.
Authored log prompts explicitly state x>0 and the shared opening refers to the
stated domain. Power questions explicitly exclude x=0; trig prompts explicitly
exclude the relevant sine/cosine zeros. Domain restrictions allow the indicated
nonzero-factor equation reductions. No field, key, grading layout or subset bank
repair was required. Source scalar amplitude changes are excluded from task-variety
counts when they are common dependent scaling. No figures or asset recipes exist.
