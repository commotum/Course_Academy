# Template extraction

## 1. Describe every original specifically

Original prompts and all five present full worked solutions are in source.json and are publicly reconstructed at original parameters. q-6862 has no worked-solution attribute, difficulty attribute, or correct designation. source-widget-q6862.json confirms the original widget is a five-choice whole-equation multiple-choice layout, with the same values up to ordering, but it also contains no correct key or worked solution. The unique tangent equation is independently derived as y+1=−5/4(x−3); this is a mathematical inference, not a recovered designation.

### q-6857 / 17592186083912

Template `polynomial_radio`, raw profile `observed_17592186083912`. Parameters `{"a": 2, "b": 3, "c": 3, "d": -5, "u": 1}`. Difficulty: `:question.difficulty/moderate`.

A curve is defined by the parametric equations

$$
x=2{t}^{3}-3t,\,y=3{t}^{2}-5,\,-\infty <t<\infty .
$$

Calculate the equation of the tangent to the curve at the point where $t=1.$

| Field | Type | Original answer value | Original correct? | Parameterized complete object |
|---|---|---|---|---|
| selection | :answer-field.type/radio | $y=\frac{24}{11}\,x+\frac{2}{11}$ | no | profile recipe 1: `raw_component_affine_recipe_0`; complete object `Add(Mul(Integer(-1), Rational(24, 11), Symbol('x', real=True)), Symbol('y', real=True), Rational(-2, 11))` (stage 3 formula order) |
| selection | :answer-field.type/radio | $y+2=(x+1)$ | no | profile recipe 2: `raw_component_affine_recipe_1`; complete object `Add(Mul(Integer(-1), Symbol('x', real=True)), Symbol('y', real=True), Integer(1))` (stage 3 formula order) |
| selection | :answer-field.type/radio | $y+2=2(x+1)$ | yes | profile recipe 3: `raw_component_affine_recipe_2`; complete object `Add(Mul(Integer(-1), Integer(2), Symbol('x', real=True)), Symbol('y', real=True))` (stage 3 formula order) |
| selection | :answer-field.type/radio | $y+2=2(x+2)$ | no | profile recipe 4: `raw_component_affine_recipe_3`; complete object `Add(Mul(Integer(-1), Integer(2), Symbol('x', real=True)), Symbol('y', real=True), Integer(-2))` (stage 3 formula order) |
| selection | :answer-field.type/radio | $y+2=(x+2)$ | no | profile recipe 5: `raw_component_affine_recipe_4`; complete object `Add(Mul(Integer(-1), Symbol('x', real=True)), Symbol('y', real=True))` (stage 3 formula order) |

Computed bank objects at original parameters (ordered by the fixed profile, not shuffled display):

```json
[
  "Add(Mul(Integer(-1), Rational(24, 11), Symbol('x', real=True)), Symbol('y', real=True), Rational(-2, 11))",
  "Add(Mul(Integer(-1), Symbol('x', real=True)), Symbol('y', real=True), Integer(1))",
  "Add(Mul(Integer(-1), Integer(2), Symbol('x', real=True)), Symbol('y', real=True))",
  "Add(Mul(Integer(-1), Integer(2), Symbol('x', real=True)), Symbol('y', real=True), Integer(-2))",
  "Add(Mul(Integer(-1), Symbol('x', real=True)), Symbol('y', real=True))"
]
```

### q-6862 / 17592186083913

Template `quintic_radio`, raw profile `observed_17592186083913`. Parameters `{"a": 1, "b": 2, "c": 1, "u": -1}`. Difficulty: `ABSENT`.

A curve is defined by the parametric equations
$x = t^{2} - 2t, y = t^{5}, - ∞ < t < ∞$.

Calculate the equation of the tangent to the curve at the point where $t =-1$.

> A scientific calculator is required to answer this question.

| Field | Type | Original answer value | Original correct? | Parameterized complete object |
|---|---|---|---|---|
| selection | :answer-field.type/radio | $y - 1 =-\frac{3}{4}(x - 3)$ | absent | profile recipe 1: `raw_component_affine_recipe_0`; complete object `Add(Mul(Rational(3, 4), Symbol('x', real=True)), Symbol('y', real=True), Rational(-13, 4))` (stage 3 formula order) |
| selection | :answer-field.type/radio | $y + 1 =-\frac{5}{4}(x + 3)$ | absent | profile recipe 2: `raw_component_affine_recipe_1`; complete object `Add(Mul(Rational(5, 4), Symbol('x', real=True)), Symbol('y', real=True), Rational(19, 4))` (stage 3 formula order) |
| selection | :answer-field.type/radio | $y + 1 =-\frac{5}{4}(x - 3)$ | absent | profile recipe 3: `raw_component_affine_recipe_2`; complete object `Add(Mul(Rational(5, 4), Symbol('x', real=True)), Symbol('y', real=True), Rational(-11, 4))` (stage 3 formula order) |
| selection | :answer-field.type/radio | $y - 1 =-\frac{5}{2}(x - 3)$ | absent | profile recipe 4: `raw_component_affine_recipe_3`; complete object `Add(Mul(Rational(5, 2), Symbol('x', real=True)), Symbol('y', real=True), Rational(-17, 2))` (stage 3 formula order) |
| selection | :answer-field.type/radio | $y + 1 = \frac{5}{4}(x - 3)$ | absent | profile recipe 5: `raw_component_affine_recipe_4`; complete object `Add(Mul(Integer(-1), Rational(5, 4), Symbol('x', real=True)), Symbol('y', real=True), Rational(19, 4))` (stage 3 formula order) |

Computed bank objects at original parameters (ordered by the fixed profile, not shuffled display):

```json
[
  "Add(Mul(Rational(3, 4), Symbol('x', real=True)), Symbol('y', real=True), Rational(-13, 4))",
  "Add(Mul(Rational(5, 4), Symbol('x', real=True)), Symbol('y', real=True), Rational(19, 4))",
  "Add(Mul(Rational(5, 4), Symbol('x', real=True)), Symbol('y', real=True), Rational(-11, 4))",
  "Add(Mul(Rational(5, 2), Symbol('x', real=True)), Symbol('y', real=True), Rational(-17, 2))",
  "Add(Mul(Integer(-1), Rational(5, 4), Symbol('x', real=True)), Symbol('y', real=True), Rational(19, 4))"
]
```

### q-122698 / 17592186256700

Template `exponential_y_intercept`, raw profile `observed_17592186256700`. Parameters `{"a": 3, "h": 1, "w": 1}`. Difficulty: `:question.difficulty/hard`.

A curve is defined by the parametric equations

$$
x={e}^{3t}+1,\,y={e}^{t}\operatorname{sin}⁡(\pi t),\,-\infty <t<\infty .
$$

Let $C$ be the point that corresponds to $t=0$ on the curve. Determine the point at which the tangent to the curve at $C$ crosses the $y$-axis.

| Field | Type | Original answer value | Original correct? | Parameterized complete object |
|---|---|---|---|---|
| selection | :answer-field.type/radio | $(0,\frac{\pi }{3})$ | no | profile recipe 1: `raw_component_affine_recipe_0`; complete object `['Integer(0)', 'Mul(Rational(1, 3), pi)']` (stage 3 formula order) |
| selection | :answer-field.type/radio | $(0,\frac{\pi }{2})$ | no | profile recipe 2: `raw_component_affine_recipe_1`; complete object `['Integer(0)', 'Mul(Rational(1, 2), pi)']` (stage 3 formula order) |
| selection | :answer-field.type/radio | $(0,-\pi )$ | no | profile recipe 3: `raw_component_affine_recipe_2`; complete object `['Integer(0)', 'Mul(Integer(-1), pi)']` (stage 3 formula order) |
| selection | :answer-field.type/radio | $(0,-\frac{2\pi }{3})$ | yes | profile recipe 4: `raw_component_affine_recipe_3`; complete object `['Integer(0)', 'Mul(Integer(-1), Rational(2, 3), pi)']` (stage 3 formula order) |
| selection | :answer-field.type/radio | $(0,-\frac{\pi }{6})$ | no | profile recipe 5: `raw_component_affine_recipe_4`; complete object `['Integer(0)', 'Mul(Integer(-1), Rational(1, 6), pi)']` (stage 3 formula order) |

Computed bank objects at original parameters (ordered by the fixed profile, not shuffled display):

```json
[
  [
    "Integer(0)",
    "Mul(Rational(1, 3), pi)"
  ],
  [
    "Integer(0)",
    "Mul(Rational(1, 2), pi)"
  ],
  [
    "Integer(0)",
    "Mul(Integer(-1), pi)"
  ],
  [
    "Integer(0)",
    "Mul(Integer(-1), Rational(2, 3), pi)"
  ],
  [
    "Integer(0)",
    "Mul(Integer(-1), Rational(1, 6), pi)"
  ]
]
```

### q-15564 / 17592186275337

Template `trig_x_intercept`, raw profile `observed_17592186275337`. Parameters `{"a": 1, "b": 1, "c": 1, "h": "1/3", "k": 1}`. Difficulty: `:question.difficulty/hard`.

A curve is defined by the parametric equations

$$
x=\operatorname{sin}⁡t+\operatorname{cos}⁡t+\frac{1}{3},\,y=\operatorname{cos}⁡t+1,\,-\infty <t<\infty .
$$

Let $C$ be the point that corresponds to $t=\frac{\pi }{2}$ on the curve. Determine the point at which the tangent to the curve at $C$ crosses the $x$-axis.

| Field | Type | Original answer value | Original correct? | Parameterized complete object |
|---|---|---|---|---|
| selection | :answer-field.type/radio | $(\frac{2}{9},\,0)$ | no | profile recipe 1: `raw_component_affine_recipe_0`; complete object `['Rational(2, 9)', 'Integer(0)']` (stage 3 formula order) |
| selection | :answer-field.type/radio | $(\frac{1}{3},\,0)$ | yes | profile recipe 2: `raw_component_affine_recipe_1`; complete object `['Rational(1, 3)', 'Integer(0)']` (stage 3 formula order) |
| selection | :answer-field.type/radio | $(\frac{2}{7},\,0)$ | no | profile recipe 3: `raw_component_affine_recipe_2`; complete object `['Rational(2, 7)', 'Integer(0)']` (stage 3 formula order) |
| selection | :answer-field.type/radio | $(\frac{2}{5},\,0)$ | no | profile recipe 4: `raw_component_affine_recipe_3`; complete object `['Rational(2, 5)', 'Integer(0)']` (stage 3 formula order) |
| selection | :answer-field.type/radio | $(\frac{1}{4},\,0)$ | no | profile recipe 5: `raw_component_affine_recipe_4`; complete object `['Rational(1, 4)', 'Integer(0)']` (stage 3 formula order) |

Computed bank objects at original parameters (ordered by the fixed profile, not shuffled display):

```json
[
  [
    "Rational(2, 9)",
    "Integer(0)"
  ],
  [
    "Rational(1, 3)",
    "Integer(0)"
  ],
  [
    "Rational(2, 7)",
    "Integer(0)"
  ],
  [
    "Rational(2, 5)",
    "Integer(0)"
  ],
  [
    "Rational(1, 4)",
    "Integer(0)"
  ]
]
```

### q-348109 / 17592186319229

Template `polynomial_blank`, raw profile `observed_17592186319229`. Parameters `{"a": 1, "b": 4, "c": 2, "d": 1, "u": 2}`. Difficulty: `:question.difficulty/moderate`.

A curve is defined by the parametric equations

$$
x={t}^{3}-4t,\,y=2{t}^{2}+1,\,-\infty <t<\infty .
$$

Find the Cartesian equation of the tangent to the curve at the point where $t=2.$

The Cartesian equation of the tangent line is $y=$
{{field-1}}.

| Field | Type | Original answer value | Original correct? | Parameterized complete object |
|---|---|---|---|---|
| field-1 | :answer-field.type/blank | $x+9$ | yes | profile recipe 1: `correct`; complete object `Add(Symbol('x', real=True), Integer(9))` (stage 3 formula order) |

Computed bank objects at original parameters (ordered by the fixed profile, not shuffled display):

```json
[
  "Add(Symbol('x', real=True), Integer(9))"
]
```

### q-348115 / 17592186319230

Template `log_y_intercept`, raw profile `observed_17592186319230`. Parameters `{"k": 2, "n": 1}`. Difficulty: `:question.difficulty/hard`.

A curve is defined by the parametric equations

$$
x=t(\operatorname{ln}⁡t+2),\,y=\operatorname{ln}⁡t,\,t\in (0,\infty ).
$$

Let $C$ be the point that corresponds to $t=e$ on the curve. Determine the coordinates of the point at which the tangent to the curve at $C$ crosses the $y$-axis. Do not round the answers.

The tangent to the curve at $C$ crosses the $y$-axis at $(${{field-1}},
{{field-2}}$).$

| Field | Type | Original answer value | Original correct? | Parameterized complete object |
|---|---|---|---|---|
| field-2 | :answer-field.type/blank | $\frac{1}{4}$ | yes | profile recipe 1: `correct_y`; complete object `Rational(1, 4)` (stage 3 formula order) |
| field-1 | :answer-field.type/blank | $0$ | yes | profile recipe 2: `correct_x`; complete object `Integer(0)` (stage 3 formula order) |

Computed bank objects at original parameters (ordered by the fixed profile, not shuffled display):

```json
[
  "Rational(1, 4)",
  "Integer(0)"
]
```

## 2. Generalize the shared pattern

Substitute the given parameter into x(t), y(t); differentiate both coordinates; use y′/x′ at that parameter; insert the point and slope in point-slope form. Whole-line radios retain whole equations; RHS blanks retain only the missing expression. Hard intercept questions additionally set x=0 or y=0 and rearrange. Trigonometric arguments are radians; exponential problems stay at t=0, trigonometric ones at π/2, and log ones at eⁿ so the exact arithmetic remains familiar.

## 3. Map all components and complete profiles

Use P=(p,q), D=x′(u), E=y′(u), m=E/D, B=q−mp, A=p−q/m.

* polynomial raw bank: y=(12m/11)x+m/11; y−q=(m/2)(x−p); correct y−q=m(x−p); y−q=m(x−q); y−q=(m/2)(x−q). The 12/11 and 1/11 expression has no identifiable method error from the sole source. This entire bank is evidence only.
* quintic raw bank: y+q=(3m/5)(x−p); y−q=m(x+p); y−q=m(x−p); y+q=2m(x−p); y−q=−m(x−p). Raw designation is absent. Normal inference is unique third relation; its new bank and complete solution are explicitly authored.
* exponential raw bank, ω=wπ: (0,m), (0,ω/p), (0,−ω), correct (0,B), (0,−m/p). The historical intent of ω/p and −ω is unresolved, so the whole raw profile is evidence only.
* trig raw bank: (2A/3,0), correct (A,0), (6A/7,0), (6A/5,0), (3A/4,0). These are deliberately documented component ratios reproducing the source's opaque 2/9, 1/3, 2/7, 2/5, 1/4 bank. They are not promoted to normal practice.
* polynomial RHS blank: mx+(q−mp). No bank/distractors added.
* log coordinate blanks retain captured field order field-2 then field-1; values B then 0, while the prompt's tuple remains field-1 then field-2.

Normal whole-line radio complete bank: tangent; inverted derivative ratio through P; negated slope through P; tangent with reversed point x coordinate; tangent with reversed point y coordinate. Each wrong operation comes from computing slope or inserting P into point-slope form. Normal exponential intercept bank: correct B; omit exponential chain factor in x′; reverse slope sign; return C's y coordinate; return slope as intercept. Normal trig intercept bank: correct A; wrongly set cos(π/2)=−1 in x′; reverse slope sign in axis calculation; return C's x coordinate; omit C's x coordinate. All five values are built together, and collisions reject the complete instance.

The historical source prose is shared by complete mathematical-span slots. Replacements cover introductory t, both coordinate substitution/evaluation chains, point prose, both derivatives, formal derivative ratio, every ratio simplification row, every numeric slope row, point-slope substitution, all line rearrangements, and final prose equations/tuples. No short-number replacement occurs. No source IDs/answer UUIDs are used to determine mathematical correctness.

## 4. Extract constrained reusable templates

| Family | Supported explicit/sampled parameters | Workload preserved |
|---|---|---|
| authored easy | a∈±1..±4, b∈−5..5, c∈±1..±3, d∈±1..±5, u∈{−2,−1,1,2}; x=at+b, y=ct³+dt | 3 nonzero coordinate terms, constant x′, 2-term y′; no axis step |
| moderate polynomial | a=1..3, b=1..6, c=1..4, d∈±1..±6, u∈{−2,−1,1,2}; x=at³−bt, y=ct²+d | 4 coordinate terms; 2-term x′, 1-term nonconstant y′; point-slope or RHS rearrangement |
| authored-rated quintic | a=1..3,b=1..4,c=1..3,u∈{−1,1}; x=at²−bt,y=ct⁵ | same two derivative computations and ratio; familiar fifth powers avoid arithmetic escalation |
| hard exp | a=2..5,h=1..4,w=1..3; x=e^(at)+h,y=eᵗsin(wπt),u=0 | chain derivative, product derivative, exponent cancellation, y-axis substitution; 48 curve/intersection tasks before bank exclusions |
| hard trig | a,b,c,k=1..4,h reduced nonintegral rational with numerator magnitude1..6 and denominator2..6; x=a sin t+b cos t+h,y=c cos t+k,u=π/2 | both trig derivatives, reciprocal then sign-reversed ratio, familiar evaluation, x-axis substitution |
| hard log | n=1..3,k=1..4; x=t(ln t+k),y=ln t,u=eⁿ | product derivative, common denominator ratio, exact logarithm evaluation, y-axis substitution; 12 meaningful tasks |

Each difficulty has unordered variations of its own required method, with no internal progression. Nonzero coefficients retain every advertised term. Explicit inputs obey the same bounds as sampling and are never silently altered. Every source anchor is valid for both its raw profile and completed normal family. Every raw profile is publicly parameterized and separately exercised away from its anchor; bank equality/ambiguity guards remain applicable. An absent source difficulty stays absent in raw output.

Finite-slope limits avoid introducing a new conditional tangent-classification branch. The domain is all real t for polynomial/exponential/trig sources and t>0 for log. No rounding is introduced. Normal log exact-entry wording uses “Give exact answers.” because the native engine detects every occurrence of “round” as requiring identical form; public raw replay retains “Do not round the answers.” and documents its rejection of correct equivalent submissions.
