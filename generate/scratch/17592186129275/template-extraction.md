# Template extraction

Database math at basis1356. Four extraction stages are explicit below. Raw evidence stays in source.json. Exact mathematical operations are recorded for ALL45 choices; interpretations of compound wrong operations remain hypotheses.

## 1. Specific source descriptions


### difference — 17592186129513

If $D = {(x, y): (x - 3)^{2} + y^{2} \le 9}$, then $∬_(D)(x^{2} - y^{2})dA =$

The source radius is 3, axis x, center sign 1, part full. It has one radio field selection and five math-valued complete-integral choices. No source solution or correct ref exists. The authoritative lesson widget confirms five choices; mathematical derivation supplies a supported correct index 4 and a shared-form authored worked solution.

### xsqrt — 17592186129628

If $D = {(x, y): (x - 1)^{2} + y^{2} \le 1, y \ge 0}$, then $∬_(D)x\sqrt{x^{2} + y^{2}}dA =$

The source radius is 1, axis x, center sign 1, part upper. It has one radio field selection and five math-valued complete-integral choices. No source solution or correct ref exists. The authoritative lesson widget confirms five choices; mathematical derivation supplies a supported correct index 4 and a shared-form authored worked solution.

### linear — 17592186278369

If $D={(x,y)\,:\,{x}^{2}+(y-1)^{2}\le 1},$ then ${∬}_{D}x\,\text{d}A=$

The source radius is 1, axis y, center sign 1, part full. It has one radio field selection and five math-valued complete-integral choices. Seven shared solution sections: change of variables, region sketch/notice, coordinate equations, six circle-substitution/factoring rows, radial range/figure, angular range/figure, polar region and final substitution/reduction. The exact prose and row sequences are retained in solution_mask.

### x2y — 17592186278370

If $D=\{(x,y)\,:\,(x-2)^{2}+{y}^{2}\le 4\},$ then ${∬}_{D}{x}^{2}y\,\text{d}A=$

The source radius is 2, axis x, center sign 1, part full. It has one radio field selection and five math-valued complete-integral choices. Seven shared solution sections: change of variables, region sketch/notice, coordinate equations, six circle-substitution/factoring rows, radial range/figure, angular range/figure, polar region and final substitution/reduction. The exact prose and row sequences are retained in solution_mask.

### expdiff — 17592186278371

If $D=\{(x,y)\,:\,(x-4)^{2}+{y}^{2}\le 16,\,y\le 0\},$ then ${∬}_{D}{e}^{{x}^{2}-{y}^{2}}\,\text{d}A=$

The source radius is 4, axis x, center sign 1, part lower. It has one radio field selection and five math-valued complete-integral choices. Seven shared solution sections: change of variables, region sketch/notice, coordinate equations, six circle-substitution/factoring rows, radial range/figure, angular range/figure, polar region and final substitution/reduction. The exact prose and row sequences are retained in solution_mask.

### sqrt — 17592186351514

If $D={(x,y)\,:\,{x}^{2}+(y-2)^{2}\le 4,\,x\ge 0},$ then ${∬}_{D}\sqrt{{x}^{2}+{y}^{2}}\,\text{d}A=$

The source radius is 2, axis y, center sign 1, part right. It has one radio field selection and five math-valued complete-integral choices. Seven shared solution sections: change of variables, region sketch/notice, coordinate equations, six circle-substitution/factoring rows, radial range/figure, angular range/figure, polar region and final substitution/reduction. The exact prose and row sequences are retained in solution_mask.

### xy2 — 17592186394504

If $D={(x,y)\,:\,(x+\frac{1}{2})^{2}+{y}^{2}\le \frac{1}{4},\,y\le 0},$ then ${∬}_{D}x{y}^{2}\,\text{d}A=$

The source radius is 1/2, axis x, center sign -1, part lower. It has one radio field selection and five math-valued complete-integral choices. Seven shared solution sections: change of variables, region sketch/notice, coordinate equations, six circle-substitution/factoring rows, radial range/figure, angular range/figure, polar region and final substitution/reduction. The exact prose and row sequences are retained in solution_mask.

### radial2 — 17592186394545

If $D={(x,y)\,:\,{x}^{2}+{(y-\frac{1}{2})}^{2}\le \frac{1}{4},\,x\le 0},$ then ${∬}_{D}({x}^{2}+{y}^{2})\,\text{d}A=$

The source radius is 1/2, axis y, center sign 1, part left. It has one radio field selection and five math-valued complete-integral choices. Seven shared solution sections: change of variables, region sketch/notice, coordinate equations, six circle-substitution/factoring rows, radial range/figure, angular range/figure, polar region and final substitution/reduction. The exact prose and row sequences are retained in solution_mask.

### log — 17592186394552

If $D={(x,y)\,:\,(x-1)^{2}+{y}^{2}\le 1,\,y\le 0},$ then ${∬}_{D}\operatorname{ln}⁡({x}^{2}+{y}^{2}+1)\,\text{d}A=$

The source radius is 1, axis x, center sign 1, part lower. It has one radio field selection and five math-valued complete-integral choices. Seven shared solution sections: change of variables, region sketch/notice, coordinate equations, six circle-substitution/factoring rows, radial range/figure, angular range/figure, polar region and final substitution/reduction. The exact prose and row sequences are retained in solution_mask.

## 2. Shared mathematical pattern

For an origin-tangent disk with center (±a,0) or (0,±a), substitute x=r cosθ,y=r sinθ into the circle and factor r(r∓2a cosθ) or its sine analogue. Choose the angular interval on which the nonnegative radial upper bound describes exactly the requested full/half disk. Substitute the integrand and multiply by r. Return a whole repeated-integral setup, without evaluating it. The composite integrands retain the source sum/difference/double-angle/radical/log reductions.


## 3. Complete component maps and observed banks

Each operation below is (outer lower/π, outer upper/π, inner lower, inner upper, density). Order is capture bank order, zero-based correct indices are identified. This maps each complete choice, never just its correct value. The literal raw choice and radius-slot render mask are in templates.json.


### difference — observed profile

| Index | Correct? | Full mathematical operation | Source value |
|---|---|---|---|
| 0 | no | `['-1/2', '1/2', '0', '2*a*cos(t)', 'r**2*cos(2*t)']` | $\displaystyle \int_{- π/2}^{π/2}\displaystyle \int_{0}^{6\cos θ}r^{2}\cos 2θdrdθ$ |
| 1 | no | `['-1/2', '1/2', '0', 'a', 'r**3']` | $\displaystyle \int_{- π/2}^{π/2}\displaystyle \int_{0}^{3}r^{3}drdθ$ |
| 2 | no | `['0', '2', '0', '2*a*cos(t)', 'r**3']` | $\displaystyle \int_{0}^{2π}\displaystyle \int_{0}^{6\cos θ}r^{3}drdθ$ |
| 3 | no | `['0', '2', '0', 'a', 'r**3*cos(2*t)']` | $\displaystyle \int_{0}^{2π}\displaystyle \int_{0}^{3}r^{3}\cos 2θdrdθ$ |
| 4 | yes, derived | `['-1/2', '1/2', '0', '2*a*cos(t)', 'r**3*cos(2*t)']` | $\displaystyle \int_{- π/2}^{π/2}\displaystyle \int_{0}^{6\cos θ}r^{3}\cos 2θdrdθ$ |

### xsqrt — observed profile

| Index | Correct? | Full mathematical operation | Source value |
|---|---|---|---|
| 0 | no | `['0', '1', '0', '2*a*cos(t)', 'r**3*cos(t)']` | $\displaystyle \int_{0}^{π}\cos θ\displaystyle \int_{0}^{2\cos θ}r^{3}drdθ$ |
| 1 | no | `['0', '1', '0', '2*a*cos(t)', 'r**2*cos(t)']` | $\displaystyle \int_{0}^{π}\cos θ\displaystyle \int_{0}^{2\cos θ}r^{2}drdθ$ |
| 2 | no | `['0', '1/2', '0', 'a', 'r**2*cos(t)']` | $\displaystyle \int_{0}^{π/2}\cos θ\displaystyle \int_{0}^{1}r^{2}drdθ$ |
| 3 | no | `['0', '1/2', '0', 'a', 'r*cos(t)']` | $\displaystyle \int_{0}^{π/2}\cos θ\displaystyle \int_{0}^{1}rdrdθ$ |
| 4 | yes, derived | `['0', '1/2', '0', '2*a*cos(t)', 'r**3*cos(t)']` | $\displaystyle \int_{0}^{π/2}\cos θ\displaystyle \int_{0}^{2\cos θ}r^{3}drdθ$ |

### linear — observed profile

| Index | Correct? | Full mathematical operation | Source value |
|---|---|---|---|
| 0 | no | `['0', '2', '0', '2*a*cos(t)', 'r*sin(t)']` | ${\int }_{0}^{2\pi }{\int }_{0}^{2\operatorname{cos}⁡\theta }r\operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $ |
| 1 | no | `['0', '2', '0', '2*a*sin(t)', 'r**2*sin(t)']` | ${\int }_{0}^{2\pi }{\int }_{0}^{2\operatorname{sin}⁡\theta }{r}^{2}\operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $ |
| 2 | no | `['0', '1', '0', '2*a*sin(t)', 'r*cos(t)']` | ${\int }_{0}^{\pi }{\int }_{0}^{2\operatorname{sin}⁡\theta }r\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta $ |
| 3 | yes, observed | `['0', '1', '0', '2*a*sin(t)', 'r**2*cos(t)']` | ${\int }_{0}^{\pi }{\int }_{0}^{2\operatorname{sin}⁡\theta }{r}^{2}\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta $ |
| 4 | no | `['0', '1', '0', '2*a*cos(t)', 'r**2*cos(t)']` | ${\int }_{0}^{\pi }{\int }_{0}^{2\operatorname{cos}⁡\theta }{r}^{2}\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta $ |

### x2y — observed profile

| Index | Correct? | Full mathematical operation | Source value |
|---|---|---|---|
| 0 | no | `['0', '2', '0', 'a', 'r**4*cos(t)**2*sin(t)']` | ${\int }_{0}^{2\pi }{\int }_{0}^{2}{r}^{4}{cos}^{2}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $ |
| 1 | no | `['-1/2', '1/2', '0', 'a', 'r**3*cos(t)**2*sin(t)']` | ${\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{2}{r}^{3}{cos}^{2}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $ |
| 2 | yes, observed | `['-1/2', '1/2', '0', '2*a*cos(t)', 'r**4*cos(t)**2*sin(t)']` | ${\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{4\operatorname{cos}⁡\theta }{r}^{4}{cos}^{2}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $ |
| 3 | no | `['0', '2', '0', '2*a*cos(t)', 'r**4*cos(t)**2*sin(t)']` | ${\int }_{0}^{2\pi }{\int }_{0}^{4\operatorname{cos}⁡\theta }{r}^{4}{cos}^{2}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $ |
| 4 | no | `['-1/2', '1/2', '0', '2*a*cos(t)', 'r**3*cos(t)**2*sin(t)']` | ${\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{4\operatorname{cos}⁡\theta }{r}^{3}{cos}^{2}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $ |

### expdiff — observed profile

| Index | Correct? | Full mathematical operation | Source value |
|---|---|---|---|
| 0 | yes, observed | `['3/2', '2', '0', '2*a*cos(t)', 'r*exp(r**2*cos(2*t))']` | ${\int }_{3\pi /2}^{2\pi }{\int }_{0}^{8\operatorname{cos}⁡\theta }r{e}^{{r}^{2}\operatorname{cos}⁡2\theta }\,\text{d}r\,\text{d}\theta $ |
| 1 | no | `['3/2', '2', '0', 'a', 'r*exp(r**2*cos(2*t))']` | ${\int }_{3\pi /2}^{2\pi }{\int }_{0}^{4}r{e}^{{r}^{2}\operatorname{cos}⁡2\theta }\,\text{d}r\,\text{d}\theta $ |
| 2 | no | `['3/2', '2', '0', '2*a*cos(t)', 'exp(r**2)']` | ${\int }_{3\pi /2}^{2\pi }{\int }_{0}^{8\operatorname{cos}⁡\theta }{e}^{{r}^{2}}\,\text{d}r\,\text{d}\theta $ |
| 3 | no | `['0', '2', '0', '2*a*cos(t)', 'exp(r**2*cos(2*t))']` | ${\int }_{0}^{2\pi }{\int }_{0}^{8\operatorname{cos}⁡\theta }{e}^{{r}^{2}\operatorname{cos}⁡2\theta }\,\text{d}r\,\text{d}\theta $ |
| 4 | no | `['0', '2', '0', 'a', 'r*exp(r**2)']` | ${\int }_{0}^{2\pi }{\int }_{0}^{4}r{e}^{{r}^{2}}\,\text{d}r\,\text{d}\theta $ |

### sqrt — observed profile

| Index | Correct? | Full mathematical operation | Source value |
|---|---|---|---|
| 0 | no | `['0', '1/2', '0', '2*a*sin(t)', 'r']` | ${\int }_{0}^{\pi /2}{\int }_{0}^{4\operatorname{sin}⁡\theta }r\,\text{d}r\,\text{d}\theta $ |
| 1 | no | `['0', '1', '0', '2*a*sin(t)', 'r**2']` | ${\int }_{0}^{\pi }{\int }_{0}^{4\operatorname{sin}⁡\theta }{r}^{2}\,\text{d}r\,\text{d}\theta $ |
| 2 | yes, observed | `['0', '1/2', '0', '2*a*sin(t)', 'r**2']` | ${\int }_{0}^{\pi /2}{\int }_{0}^{4\operatorname{sin}⁡\theta }{r}^{2}\,\text{d}r\,\text{d}\theta $ |
| 3 | no | `['0', '1/2', '0', 'a*sin(t)', 'r**2']` | ${\int }_{0}^{\pi /2}{\int }_{0}^{2\operatorname{sin}⁡\theta }{r}^{2}\,\text{d}r\,\text{d}\theta $ |
| 4 | no | `['0', '1', '0', 'a*sin(t)', 'r**3']` | ${\int }_{0}^{\pi }{\int }_{0}^{2\operatorname{sin}⁡\theta }{r}^{3}\,\text{d}r\,\text{d}\theta $ |

### xy2 — observed profile

| Index | Correct? | Full mathematical operation | Source value |
|---|---|---|---|
| 0 | no | `['0', '1/2', '2*a', '4*a*sin(t)', 'r**4*cos(t)*sin(t)**2']` | ${\int }_{0}^{\pi /2}{\int }_{1}^{2\operatorname{sin}⁡\theta }{r}^{4}\operatorname{cos}⁡\theta {sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta $ |
| 1 | no | `['0', '1', '2*a/cos(t)', '4*a*sin(t)', 'r**3*cos(t)*sin(t)**2']` | ${\int }_{0}^{\pi }{\int }_{\operatorname{sec}⁡\theta }^{2\operatorname{sin}⁡\theta }{r}^{3}\operatorname{cos}⁡\theta {sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta $ |
| 2 | no | `['0', '1', '0', '2*a*sin(t)', 'r**4*cos(t)*sin(t)']` | ${\int }_{0}^{\pi }{\int }_{0}^{\operatorname{sin}⁡\theta }{r}^{4}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $ |
| 3 | no | `['0', '1/2', '2*a', '-2*a*cos(t)', 'r**2*cos(t)*sin(t)']` | ${\int }_{0}^{\pi /2}{\int }_{1}^{-\operatorname{cos}⁡\theta }{r}^{2}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $ |
| 4 | yes, observed | `['1', '3/2', '0', '-2*a*cos(t)', 'r**4*cos(t)*sin(t)**2']` | ${\int }_{\pi }^{3\pi /2}{\int }_{0}^{-\operatorname{cos}⁡\theta }{r}^{4}\operatorname{cos}⁡\theta {sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta $ |

### radial2 — observed profile

| Index | Correct? | Full mathematical operation | Source value |
|---|---|---|---|
| 0 | yes, observed | `['1/2', '1', '0', '2*a*sin(t)', 'r**3']` | ${\int }_{\pi /2}^{\pi }{\int }_{0}^{\operatorname{sin}⁡\theta }{r}^{3}\,\text{d}r\,\text{d}\theta $ |
| 1 | no | `['0', '1', '0', '2*a*sin(t)', 'r**2']` | ${\int }_{0}^{\pi }{\int }_{0}^{\operatorname{sin}⁡\theta }{r}^{2}\,\text{d}r\,\text{d}\theta $ |
| 2 | no | `['-1/2', '1', '0', '2*a*sin(t)', 'r**3']` | ${\int }_{-\pi /2}^{\pi }{\int }_{0}^{\operatorname{sin}⁡\theta }{r}^{3}\,\text{d}r\,\text{d}\theta $ |
| 3 | no | `['1/2', '3/2', '0', '2*a*sin(t)', 'r']` | ${\int }_{\pi /2}^{3\pi /2}{\int }_{0}^{\operatorname{sin}⁡\theta }r\,\text{d}r\,\text{d}\theta $ |
| 4 | no | `['1', '2', '0', '2*a*sin(t)', 'r**2']` | ${\int }_{\pi }^{2\pi }{\int }_{0}^{\operatorname{sin}⁡\theta }{r}^{2}\,\text{d}r\,\text{d}\theta $ |

### log — observed profile

| Index | Correct? | Full mathematical operation | Source value |
|---|---|---|---|
| 0 | no | `['-1', '0', '0', '2*a*cos(t)', '2*r*log(r+1)']` | ${\int }_{-\pi }^{0}{\int }_{0}^{2\operatorname{cos}⁡\theta }2r\operatorname{ln}⁡(r+1)\,\text{d}r\,\text{d}\theta $ |
| 1 | no | `['0', '1', '0', 'a*cos(t)', 'r**2*log(r+1)']` | ${\int }_{0}^{\pi }{\int }_{0}^{\operatorname{cos}⁡\theta }{r}^{2}\operatorname{ln}⁡(r+1)\,\text{d}r\,\text{d}\theta $ |
| 2 | yes, observed | `['-1/2', '0', '0', '2*a*cos(t)', 'r*log(r**2+1)']` | ${\int }_{-\pi /2}^{0}{\int }_{0}^{2\operatorname{cos}⁡\theta }r\operatorname{ln}⁡({r}^{2}+1)\,\text{d}r\,\text{d}\theta $ |
| 3 | no | `['0', '1/2', '0', 'a*cos(t)', 'log(r**2+1)']` | ${\int }_{0}^{\pi /2}{\int }_{0}^{\operatorname{cos}⁡\theta }\operatorname{ln}⁡({r}^{2}+1)\,\text{d}r\,\text{d}\theta $ |
| 4 | no | `['-1/2', '1/2', '0', '2*a*cos(t)', 'r*log(r**2)']` | ${\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{2\operatorname{cos}⁡\theta }r\operatorname{ln}⁡({r}^{2})\,\text{d}r\,\text{d}\theta $ |

## 4. Reusable templates, constraints and fidelity boundaries

Fixed components: complete source sentence order, same field/type/count, Cartesian integrand, center axis/sign and half-plane restriction, source angular conventions, each complete bank. Variable component: positive radius a. Whole coordinate shifts, squared radius, radial2a factors, notices, diagrams, bound coefficients and all dependent constants change together. Source arithmetic masks preserve expanded constants and unevaluated factoring rows. No arbitrary expression polynomial fit is used.

Observed radius values are1/2,1,2,3,4. Normal sampling permits integer/half-integer radius1/2–5 at moderate/hard; easy uses integer1–5. These bounds are enforced for explicit calls too. Parameters beyond these domains fail rather than silently resample. The api profile observed replays every original bank; setup adds a minimal response-criterion sentence while using the same complete observed operation bank. The four easy families have a separately authored five-choice complete bank: correct, omitted Jacobian, constant radius, full0..2π sweep, wrong radial sign. None is a recovered source bank. All masks generalize exact source values; source wrong-intent claims remain limited to visible operations (wrong power/angle/axis/shift scale/lower bound). In xy2, the compound wrong bounds secθ and1 are visible observed shapes; their intended error cannot be inferred uniquely and some choices do not define a finite scalar integral. They are structurally invalid setups, not extra valid answers.

### Source format repairs (no algebraic changes)

Raw source set notation D={(...)} and Δ={(...)} uses literal braces as TeX groups, hiding the braces. These become visible escaped\{,\}. Five source coordinate systems have an unmatched nonliteral opening { before\begin{aligned}; this becomes a visible\{. The x2y/expdiff systems already use\{. The two unrated legacy banks were checked byte by byte: each TeX command begins with one backslash. No slash normalization is needed; all45 values remain raw-exact. Original solution image refs are expanded to real captured asset paths. These presentation changes are separately counted from mathematical/bank fidelity; available complete prose/stage sequences are compared against exactly this documented normalization.

### Missing evidence and scalar coincidences

The two unrated banks lack difficulty labels, correct refs and solutions both in EDB capture and original MA widget extraction. Correct choices are independently derived; no matched observed designation is claimed for them. New solutions use the common six circle-conversion stages and final formal/substitution/reduction steps.

For linear over the upper full disk, the correct scalar is0, and the omitted-Jacobian cosθ option also integrates to0; other full-sweep options can do so too. For x2y over a full right disk, oddness in y makes the correct scalar0, and several wrong regions/densities also integrate to0. This is documented as scalar equality, not mathematical unique-value fidelity. The assessed rewriting criterion is actual D plus transformed density/Jacobian. Normal wording makes that response criterion explicit; source replays retain source wording.
