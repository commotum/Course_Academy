# Template extraction

Snapshot math / basis1356 / lineage01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. All original fields and banks are mapped below; source capture is immutable. The generator loads source prose skeletons and replaces mathematical slots from polynomial calculations. It never returns a source payload or uses a numerical answer lookup.

## 1. Specific source descriptions

### q-666 — affine_constant_radio

Find $\frac{\text{d}f}{\text{d}x}$ when $f(x)=(4+6x{)}^{3}.$

Original parameters `{"a": 6, "b": 4, "n": 3}`; family `affine_constant`; original difficulty :question.difficulty/easy.
One :answer-field.type/radio field `selection`; 5 supplied values. Variable x; polynomial P=6 x + 4; integer outer power 3. Real domain; no excluded inputs.

### q-11410 — affine_variable_radio

Find $\frac{\text{d}f}{\text{d}x}$ when $f(x)={(5x+10)}^{6}.$

Original parameters `{"a": 5, "b": 10, "n": 6}`; family `affine_variable`; original difficulty :question.difficulty/easy.
One :answer-field.type/radio field `selection`; 5 supplied values. Variable x; polynomial P=5 x + 10; integer outer power 6. Real domain; no excluded inputs.

### q-340690 — affine_blank

Find $\frac{\text{d}f}{\text{d}x}$ when $f(x)=(1-7x)^{4}.$

$\frac{\text{d}f}{\text{d}x}=$
{{field-1}}

Original parameters `{"a": -7, "b": 1, "n": 4}`; family `affine_constant`; original difficulty :question.difficulty/easy.
One :answer-field.type/blank field `field-1`; 1 supplied values. Variable x; polynomial P=1 - 7 x; integer outer power 4. Real domain; no excluded inputs.

### q-132974 — quadratic_derivative

$\frac{\text{d}}{\text{d}t}[(2{t}^{2}+3)^{2}]=\,$

                            
                                    
                            
                                        {{field-1}}

Original parameters `{"a": 2, "b": 3, "n": 2}`; family `quadratic`; original difficulty :question.difficulty/moderate.
One :answer-field.type/blank field `field-1`; 1 supplied values. Variable t; polynomial P=2 t^{2} + 3; integer outer power 2. Real domain; no excluded inputs.

### q-342630 — quadratic_slope

Given that $f(x)={({x}^{2}+2x+1)}^{2},$ the slope at the point $(0,1)$ is{{field-1}}.

Original parameters `{"a": 1, "b": 2, "c": 1, "n": 2, "z": 0}`; family `quadratic_full`; original difficulty :question.difficulty/moderate.
One :answer-field.type/blank field `field-1`; 1 supplied values. Variable x; polynomial P=x^{2} + 2 x + 1; integer outer power 2. Real domain; no excluded inputs.

### q-342663 — affine_slope

Given that $f(x)={(3x+1)}^{4},$ the slope at the point $(-1,16)$ is{{field-1}}.

Original parameters `{"a": 3, "b": 1, "n": 4, "z": -1}`; family `affine_variable`; original difficulty :question.difficulty/moderate.
One :answer-field.type/blank field `field-1`; 1 supplied values. Variable x; polynomial P=3 x + 1; integer outer power 4. Real domain; no excluded inputs.

### q-48625 — quartic_radio

Find $\frac{df}{dx}$ when $f(x) = (x^{4} + 3x)^{2}$.

Original parameters `{"a": 1, "b": 3, "n": 2}`; family `quartic`; original difficulty **unrated**.
One :answer-field.type/radio field `selection`; 5 supplied values. Variable x; polynomial P=x^{4} + 3 x; integer outer power 2. Real domain; no excluded inputs.

### q-342910 — tangent_blank

Given that $f(x)=(3-2x{)}^{3},$ the equation of the tangent at the point $(2,-1)$ is

$y=$
{{field-1}}.

Original parameters `{"a": -2, "b": 3, "n": 3, "z": 2}`; family `affine_constant`; original difficulty :question.difficulty/hard.
One :answer-field.type/blank field `field-1`; 1 supplied values. Variable x; polynomial P=3 - 2 x; integer outer power 3. Real domain; no excluded inputs.

### q-48666 — tangent_radio

Given that $f(x)={(5-3x)}^{4},$ find the equation of the tangent at point $(2,1).$

Original parameters `{"a": -3, "b": 5, "n": 4, "z": 2}`; family `affine_constant`; original difficulty :question.difficulty/hard.
One :answer-field.type/radio field `selection`; 5 supplied values. Variable x; polynomial P=5 - 3 x; integer outer power 4. Real domain; no excluded inputs.

## 2. Generalized family

Differentiate a real polynomial integer power F=P^n by computing nP^(n−1)P′. Easy uses an affine P. Moderate either differentiates a quadratic/two-term polynomial or evaluates the derivative at a supplied point. Hard evaluates an affine-power derivative and uses the prerequisite point-slope equation to return a tangent equation. Responses preserve full derivative, scalar slope, complete radio equation, or blank RHS as captured. Source-specific multiplication/substitution sentence sequences remain separate templates.

## 3. Component and complete-bank mapping

P denotes the displayed inner polynomial, z the supplied abscissa, y₀=P(z)^n, and m=nP(z)^(n−1)P′(z). Bank recipes are mapped by full mathematical equality; ordering is not asserted because source and local radio options may shuffle. All five values are selected as one profile.

### q-666 / observed_666

| Original answer UUID | Exact captured value | Complete parameterized recipe | Designation |
|---|---|---|---|
| `0c2e9e80-9009-5c4d-8418-53807b048413` | `18(4+6x{)}^{2}` | n a P^(n−1) | captured correct |
| `2f451149-34e3-5874-ac22-67e5f7f806cc` | `18x(4+6x{)}^{2}` | n a x P^(n−1) | incorrect |
| `ac1f9842-ca0a-55db-bcb6-06735b728dba` | `\frac{(4+6x{)}^{2}}{2}` | (n/a) P^(n−1) | incorrect |
| `b1df2cc8-3e8e-59c7-a92f-f4f573b06622` | `3(4+6x{)}^{2}` | n P^(n−1) | incorrect |
| `d848947b-033e-583b-9707-793c5c4bf6dc` | `30(4+6x{)}^{4}` | (n+2) a P^(n+1) | incorrect |

The `n/a` and `(n+2)`/raised-power patterns reproduce complete source values. Their cognitive interpretation is unresolved; this profile is explicit replay only. Retaining x and omitting P′ are operationally interpretable.

Captured solution ending:

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =3\cdot 6\cdot (4+6x{)}^{2} \\  & =18(4+6x{)}^{2}.\end{aligned}
$$

### q-11410 / observed_11410

| Original answer UUID | Exact captured value | Complete parameterized recipe | Designation |
|---|---|---|---|
| `147b8607-00ab-583f-9d29-c36db3ffb93e` | `30{(5x+10)}^{5}` | n a P^(n−1) | captured correct |
| `8b9923c0-68fb-5db2-a270-b22a0a565a94` | `30{(5x+10)}^{6}` | n a P^n | incorrect |
| `b955e3b8-b464-5b10-97ae-eea2d8b024ff` | `5{(5x+10)}^{5}` | a P^(n−1) | incorrect |
| `efb057ba-bc50-5a4b-9c8c-026e21fb0356` | `10{(5x+10)}^{5}` | b P^(n−1) | incorrect |
| `f825b128-d786-54b0-9c93-577427b75d05` | `6{(5x+10)}^{5}` | n P^(n−1) | incorrect |

The b scale is an empirical component pattern; source evidence cannot establish why the constant term was used as multiplier. This profile is explicit replay only.

Captured solution ending:

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =6{g}^{5}\cdot 5 \\  & =30(5x+10{)}^{5}.\end{aligned}
$$

### q-340690 / blank

| Original answer UUID | Exact captured value | Complete parameterized recipe | Designation |
|---|---|---|---|
| `db185f31-d898-509f-b9c4-a2881a9060fa` | `-28(1-7x)^3` | nP^(n−1)P′ (derivative) | captured correct |

Captured solution ending:

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =4{g}^{3}\cdot (-7) \\  & =-28(1-7x)^{3}.\end{aligned}
$$

### q-132974 / blank

| Original answer UUID | Exact captured value | Complete parameterized recipe | Designation |
|---|---|---|---|
| `182d03f6-7007-5d30-9f41-468940bf1b5d` | `8t(2{t}^{2}+3)` | nP^(n−1)P′ (derivative) | captured correct |

Captured solution ending:

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[(2{t}^{2}+3)^{2}] & ={h}^{′}(t) \\  & ={h}^{′}(g(t))\cdot {g}^{′}(t) \\  & =2g\cdot 4t \\  & =8t(2{t}^{2}+3).\end{aligned}
$$

### q-342630 / blank

| Original answer UUID | Exact captured value | Complete parameterized recipe | Designation |
|---|---|---|---|
| `9dddace1-6902-5bd8-8d9c-4f8e9ee4c695` | `4` | m (scalar) | captured correct |

Captured solution ending:

$$
\begin{aligned}{\frac{\text{d}f}{\text{d}x}|}_{x=0} & =[2({x}^{2}+2x+1)(2x+2){]}_{x=0} \\  & =2((0{)}^{2}+2\cdot (0)+1)(2\cdot (0)+2) \\  & =2(1)(2) \\  & =4.\end{aligned}
$$

### q-342663 / blank

| Original answer UUID | Exact captured value | Complete parameterized recipe | Designation |
|---|---|---|---|
| `afdc11cd-82dd-5c6f-bcb3-29722512bae8` | `-96` | m (scalar) | captured correct |

Captured solution ending:

$$
\begin{aligned}{\frac{\text{d}f}{\text{d}x}|}_{x=-1} & =[12(3x+1{)}^{3}{]}_{x=-1} \\  & =12(3\cdot (-1)+1{)}^{3} \\  & =12(-2{)}^{3} \\  & =-96.\end{aligned}
$$

### q-48625 / observed_48625

| Original answer UUID | Exact captured value | Complete parameterized recipe | Designation |
|---|---|---|---|
| `85752216-72d1-52c5-a307-1f7593bb2baa` | `2(x^{4} + 3x)(4x^{3} + 3)` | n P^(n−1) P′ | designation absent; inferred correct |
| `bffd2b2f-d555-5e17-8756-8a754febf526` | `2(x^{4} + 3x)(4x^{3} + 3x)` | n P^(n−1)(4ax³+bx) | incorrect |
| `eef892e3-6947-592f-9345-311b595e0536` | `2(4x^{3})(x^{4} + 3x)` | n(4ax³)P^(n−1) | incorrect |
| `05327ffd-b783-558f-8116-edad45453171` | `2(4x^{3})(x^{4} + 3x)^{2}` | n(4ax³)P^n | incorrect |
| `62baa9f7-a4b9-5ff4-84f6-37fdf189f3fa` | `2(x^{4} + 3x)(4x^{3} + 3)^{2}` | n P^(n−1)(P′)^n | incorrect |

No original worked solution. Canonical chain-rule wording is supplied as an authored solution repair.

### q-342910 / blank

| Original answer UUID | Exact captured value | Complete parameterized recipe | Designation |
|---|---|---|---|
| `9e15c4f3-e0aa-5296-8996-2def04133195` | `-6x+11` | m x+y₀−m z (RHS only) | captured correct |

Captured solution ending:

$$
\begin{aligned}y-{y}_{1} & =m(x-{x}_{1}) \\ y+1 & =-6\cdot (x-2) \\ y & =-6x+12-1 \\ y & =-6x+11\end{aligned}
$$

### q-48666 / observed_48666

| Original answer UUID | Exact captured value | Complete parameterized recipe | Designation |
|---|---|---|---|
| `354142ae-6999-5699-b81d-9f16570b6115` | `y=-12x+25` | −m x+y₀+m z | incorrect |
| `6637b75c-a39e-5721-a28b-4a320ad5c971` | `y=12x-23` | m x+y₀−m z | captured correct |
| `790d805f-3881-5904-ba81-7ea14a53c052` | `y=-3x+7` | a x+y₀−a z | incorrect |
| `85aa1fa8-f1d2-5839-ba72-e02c15010a7e` | `y=-4x+9` | −n x+y₀+n z | incorrect |
| `bcf17a1f-abef-5a3c-bb11-4d68176c30e1` | `y=4x-7` | n x+y₀−n z | incorrect |

The scalar slope replacements a, n, −n fit every complete observed line through the supplied point, but do not establish the original mistake mechanism. This bank is explicit replay only.

Captured solution ending:

$$
\begin{aligned}y-{y}_{1} & =m(x-{x}_{1}) \\ y-1 & =12(x-2) \\ y-1 & =12x-24 \\ y & =12x-23\end{aligned}
$$

## 4. Reusable templates, constraints, and sampling

Fixed: every source’s nonmathematical prose, original math-slot order, placeholders, source field key/type/count, polynomial integer-power chain method, and response shape. Variable: polynomial coefficients, signed constants, outer exponent, inner polynomial shape within that template, evaluation point, function ordinate, derivative, scalar slope, and tangent intercept. Conditional: sign formatting and the intermediate substitution reductions; every explicit template retains its source equation-stage sequence. Parameter metadata and recipe names remain outside learner prose. There is one worked solution per instance, independent of chosen answer.

Sampling is an authored policy: easy affine a∈{±2,…,±7}, b∈{±1,…,±6}, n∈{2,…,6}; moderate affine slope uses a∈{±1,±2,±3}, b∈{±1,…,±6}, fixed n=4 and z∈{−2,…,2}; quadratic derivative/slope uses a∈{±1,±2,±3}, n∈{2,3}, b∈{±1,…,±6}, optional c∈{±1,±2,±3}, z∈{−2,…,2}; quartic radio uses a∈{±1,±2,±3}, b∈{±1,…,±6}, n=2; hard tangent uses a∈{±1,±2,±3}, b∈{±1,…,±6}, n∈{3,4} and z∈{−2,…,2}. Explicit replay accepts nonzero a,b bounded by12, n2–6, optional c/z bounded by12. The observed a=1,b=10 and z=0 are preserved. Every normally sampled point question additionally requires 1≤|P(z)|≤3 and P′(z)≠0; reject the whole instance otherwise. These authored number-feature bounds preserve the small evaluated values in the source workload and prevent powers of large inputs. Explicit inputs remain unchanged and may have zero slope for a blank field; radio ambiguities reject the whole instance. No new point branch or progression is introduced.

Defaults choose the complete authored bank before sampling. Affine wrong operations: omit P′, keep exponent n, omit n, negate P′. Quartic: retain x when differentiating bx, omit the linear derivative, omit it while retaining exponent n, and wrongly raise P′ to power n. These use the assessed method; they are hypotheses about errors, not recovered author intent. Tangent: negate m, omit P′, omit n, or keep outer exponent n, then construct each full line through the displayed point. Default banks preserve five options and are checked for all equivalences.

All levels are present in the snapshot, so no missing-level extension is required. q-48625’s moderate assignment is authored: differentiating both terms of x⁴+bx adds inner sum/power-rule work beyond an easy affine constant derivative, comparable to the observed moderate quadratic derivative. Canonical e-181 already uses a degree-four inner polynomial. This claim is provisional rather than an observed rating. Coefficient/point peers within a level are unordered; no escalation in skill or progression is added.

Source anomaly: q-48625 missing designation/solution/difficulty. Preserve the raw record and widget evidence; infer the unique correct derivative independently. Fidelity counts 8/8 available designations with1 missing, never9/9. Its bank is5/5 matched and all four distractors are separately parsed. No other source mathematical error found.

Validation separates source bank/field fidelity, mathematical correctness, identity/format/scope, and native grading. Rendered solution prose skeletons retain exact source wording and whitespace; mathematical LaTeX is normalized rather than byte-identical. Original source stage values and generated stage values are both independently parsed. Radio full equations are compared as complete y-expression relations; tangent blank is RHS only. No added option feedback. No plots; no database preparation or transactions.
