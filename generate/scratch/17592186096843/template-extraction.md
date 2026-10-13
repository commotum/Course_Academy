# Template extraction: KP 17592186096843

Captured basis 1999, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. All source facts are preserved in source.json and reference/source.edn.

The moderate templates differentiate a fixed power of an affine expression, as a full radio choice or full blank. Hard templates require an inner derivative fragment of a polynomial square, a full affine radical derivative, or a numerator fragment of a reciprocal quartic radical. Keep these answer shapes separate. All use the original fixed two-stage chain-rule solution. No plots or assets occur.

Sampling is intentionally narrow: only the affine shift b or specified polynomial c varies. Slopes, exponents and observed complete distractor coefficients stay fixed. In particular the unexplained 20 and 9 in q-107293 are preserved fixed patterns, not assigned an invented learner misconception. No mixed banks are used. Seed and choice order do not define a new mathematical task.

Source wording uses f(g(x)) loosely as outer-function notation and q-342891 uses dy/dx in the response line while its prompt names f. These notational imprecisions are retained for fidelity; the generator and independent verification use the unambiguous displayed f(x).

## q-107293 (moderate, affine-power-radio)

Original parameters: {"b": 4}. Proposed values: [{"b": -9}, {"b": -8}, {"b": -7}, {"b": -6}, {"b": -5}, {"b": -4}, {"b": -3}, {"b": -2}, {"b": -1}, {"b": 0}, {"b": 1}, {"b": 2}, {"b": 3}, {"b": 4}, {"b": 5}, {"b": 6}, {"b": 7}, {"b": 8}, {"b": 9}].

Given that $f(x)={(3x+4)}^{5},$ find ${f}^{′}(x).$

Field selection (:answer-field.type/radio).

- 5(3x+4{)}^{4} → 5(3x+b)^4: omit inner slope
- 3(3x+4{)}^{5} → 3(3x+b)^5: inner slope times unchanged outer power
- 20(3x+4{)}^{4} → 20(3x+b)^4: observed fixed coefficient 20; mechanism unresolved
- 9(3x+4{)}^{4} → 9(3x+b)^4: observed fixed coefficient 9; mechanism unresolved
- 15(3x+4{)}^{4} → 15(3x+b)^4: chain rule (correct)

Original fixed solution:

Let $g(x)=3x+4$ and $f(g(x))=g(x{)}^{5}.$ 

Differentiating, we have

$$
\begin{aligned}{f}^{′}(g(x)) & =({g}^{5}{)}^{′}=5{g}^{4}, \\ {g}^{′}(x) & =(3x+4{)}^{′}=3.\end{aligned}
$$

Then, using the chain rule, 

$$
\begin{aligned}{f}^{′}(x) & ={f}^{′}(g(x))\cdot {g}^{′}(x) \\  & =5{g}^{4}\cdot 3 \\  & =15(3x+4{)}^{4}.\end{aligned}
$$

## q-342804 (moderate, affine-power-blank)

Original parameters: {"b": 3}. Proposed values: [{"b": -9}, {"b": -8}, {"b": -7}, {"b": -6}, {"b": -5}, {"b": -4}, {"b": -3}, {"b": -2}, {"b": -1}, {"b": 0}, {"b": 1}, {"b": 2}, {"b": 3}, {"b": 4}, {"b": 5}, {"b": 6}, {"b": 7}, {"b": 8}, {"b": 9}].

Given that $f(x)={(4x+3)}^{5},$ find ${f}^{′}(x).$

${f}^{′}(x)=$
{{field-1}}

Field field-1 (:answer-field.type/blank).

- 20(4x+3)^{4} → 20(4x+b)^4: full derivative (correct)

Original fixed solution:

Let $g(x)=4x+3$ and $f(g(x))=g(x{)}^{5}.$ 

Differentiating, we have

$$
\begin{aligned}{f}^{′}(g(x)) & =({g}^{5}{)}^{′}=5{g}^{4}, \\ {g}^{′}(x) & =(4x+3{)}^{′}=4.\end{aligned}
$$

Then, using the chain rule, 

$$
\begin{aligned}{f}^{′}(x) & ={f}^{′}(g(x))\cdot {g}^{′}(x) \\  & =5{g}^{4}\cdot (4) \\  & =20(4x+3{)}^{4}.\end{aligned}
$$

## q-71954 (moderate, affine-power-radio)

Original parameters: {"b": -7}. Proposed values: [{"b": -9}, {"b": -8}, {"b": -7}, {"b": -6}, {"b": -5}, {"b": -4}, {"b": -3}, {"b": -2}, {"b": -1}, {"b": 0}, {"b": 1}, {"b": 2}, {"b": 3}, {"b": 4}, {"b": 5}, {"b": 6}, {"b": 7}, {"b": 8}, {"b": 9}].

Given that $f(x)={(8x-7)}^{4},$ find ${f}^{′}(x).$

Field selection (:answer-field.type/radio).

- 32(16x-7{)}^{3} → 32(16x+b)^3: double inner x coefficient
- 16(8x-7{)}^{3} → 16(8x+b)^3: half outer coefficient
- 16(16x-7{)}^{3} → 16(16x+b)^3: half outer coefficient and double inner x coefficient
- 8(8x-7{)}^{3} → 8(8x+b)^3: quarter outer coefficient
- 32(8x-7{)}^{3} → 32(8x+b)^3: chain rule (correct)

Original fixed solution:

Let $g(x)=8x-7$ and $f(g(x))=g(x{)}^{4}.$ 

Differentiating, we have

$$
\begin{aligned}{f}^{′}(g(x)) & =({g}^{4}{)}^{′}=4{g}^{3}, \\ {g}^{′}(x) & =(8x-7{)}^{′}=8.\end{aligned}
$$

Then, using the chain rule, 

$$
\begin{aligned}{f}^{′}(x) & ={f}^{′}(g(x))\cdot {g}^{′}(x) \\  & =4{g}^{3}\cdot (8) \\  & =32(8x-7{)}^{3}.\end{aligned}
$$

## q-71956 (moderate, affine-power-radio)

Original parameters: {"b": 2}. Proposed values: [{"b": 1}, {"b": 2}, {"b": 3}, {"b": 4}, {"b": 5}, {"b": 6}, {"b": 7}, {"b": 8}, {"b": 9}].

Given that $f(x)={(2-5x)}^{3},$ find ${f}^{′}(x).$

Field selection (:answer-field.type/radio).

- -15(2+5x{)}^{2} → -15(b+5x)^2: reverse inner sign
- -15(2-5x{)}^{3} → -15(b-5x)^3: leave outer exponent unchanged
- 15(2+5x{)}^{2} → 15(b+5x)^2: reverse inner and outer signs
- 15(2-5x{)}^{2} → 15(b-5x)^2: reverse outer sign
- -15(2-5x{)}^{2} → -15(b-5x)^2: chain rule (correct)

Original fixed solution:

Let $g(x)=2-5x$ and $f(g(x))=g(x{)}^{3}.$ 

Differentiating, we have

$$
\begin{aligned}{f}^{′}(g(x)) & =({g}^{3}{)}^{′}=3{g}^{2}, \\ {g}^{′}(x) & =(2-5x{)}^{′}=-5.\end{aligned}
$$

Then, using the chain rule, 

$$
\begin{aligned}{f}^{′}(x) & ={f}^{′}(g(x))\cdot {g}^{′}(x) \\  & =3{g}^{2}\cdot (-5) \\  & =-15(2-5x{)}^{2}.\end{aligned}
$$

## q-342875 (hard, polynomial-square-inner-fragment)

Original parameters: {"c": 4}. Proposed values: [{"c": 1}, {"c": 2}, {"c": 3}, {"c": 4}, {"c": 5}, {"c": 6}, {"c": 7}, {"c": 8}, {"c": 9}, {"c": 10}, {"c": 11}, {"c": 12}].

Given that $f(x)={({x}^{5}-4{x}^{4})}^{2},$ find ${f}^{′}(x).$

${f}^{′}(x)=2({x}^{5}-4{x}^{4})($
{{field-1}}
$)$

Field field-1 (:answer-field.type/blank).

- 5{x}^{4}-16{x}^{3} → 5x^4-4cx^3: inner derivative fragment (correct)

Original fixed solution:

Let $g(x)={x}^{5}-4{x}^{4}$ and $f(g(x))=g(x)^{2}.$ 

Differentiating, we have

$$
\begin{aligned}{f}^{′}(g(x)) & =({g}^{2})^{′}=2g, \\ {g}^{′}(x) & =({x}^{5}-4{x}^{4})^{′}=5{x}^{4}-16{x}^{3}.\end{aligned}
$$

Then, using the chain rule, 

$$
\begin{aligned}{f}^{′}(x) & ={f}^{′}(g(x))\cdot {g}^{′}(x) \\  & =2g\cdot (5{x}^{4}-16{x}^{3}) \\  & =2({x}^{5}-4{x}^{4})(\,5{x}^{4}-16{x}^{3}\,).\end{aligned}
$$

## q-342883 (hard, affine-square-root-full-blank)

Original parameters: {"b": -4}. Proposed values: [{"b": -9}, {"b": -8}, {"b": -7}, {"b": -6}, {"b": -5}, {"b": -4}, {"b": -3}, {"b": -2}, {"b": -1}, {"b": 0}, {"b": 1}, {"b": 2}, {"b": 3}, {"b": 4}, {"b": 5}, {"b": 6}, {"b": 7}, {"b": 8}, {"b": 9}].

Given that $f(x)=\sqrt{5x-4},$ find ${f}^{′}(x).$

${f}^{′}(x)=$
{{field-1}}

Field field-1 (:answer-field.type/blank).

- \frac{5}{2\sqrt{5x-4}} → 5/(2 sqrt(5x+b)): full derivative (correct)

Original fixed solution:

Let $g(x)=5x-4$ and $f(g(x))=\sqrt{g(x)}.$ 

Differentiating, we have

$$
\begin{aligned}{f}^{′}(g(x)) & ={(\sqrt{g})}^{′}=\frac{1}{2\sqrt{g}}, \\ {g}^{′}(x) & =(5x-4)^{′}=5.\end{aligned}
$$

Then, using the chain rule, 

$$
\begin{aligned}{f}^{′}(x) & ={f}^{′}(g(x))\cdot {g}^{′}(x) \\  & =\frac{1}{2\sqrt{g}}\cdot 5 \\  & =\frac{5}{2\sqrt{5x-4}}.\end{aligned}
$$

## q-342891 (hard, quartic-reciprocal-root-numerator-fragment)

Original parameters: {"c": 5}. Proposed values: [{"c": 1}, {"c": 2}, {"c": 3}, {"c": 4}, {"c": 5}, {"c": 6}, {"c": 7}, {"c": 8}, {"c": 9}, {"c": 10}, {"c": 11}, {"c": 12}].

Given that $f(x)=\frac{1}{\sqrt{2{x}^{4}-{x}^{2}+5}},$ find ${f}^{′}(x).$

$\frac{\text{d}y}{\text{d}x}=\frac{1}{\sqrt{(2{x}^{4}-{x}^{2}+5{)}^{3}}}($
{{field-1}}
$)$

Field field-1 (:answer-field.type/blank).

- x-4{x}^{3} → x-4x^3: negative half inner derivative; denominator stays outside blank (correct)

Original fixed solution:

Let $g(x)=2{x}^{4}-{x}^{2}+5$ and $f(g(x))=\frac{1}{\sqrt{g(x)}}.$ 

Differentiating, we have

$$
\begin{aligned}{f}^{′}(g(x)) & ={(\frac{1}{\sqrt{g}})}^{′}=-\frac{1}{2\sqrt{{g}^{3}}}, \\ {g}^{′}(x) & =(2{x}^{4}-{x}^{2}+5{)}^{′}=8{x}^{3}-2x.\end{aligned}
$$

Then, using the chain rule, 

$$
\begin{aligned}{f}^{′}(x) & ={f}^{′}(g(x))\cdot {g}^{′}(x) \\  & =-\frac{1}{2\sqrt{{g}^{3}}}\cdot (8{x}^{3}-2x) \\  & =\frac{1}{\sqrt{(2{x}^{4}-{x}^{2}+5{)}^{3}}}(\,x-4{x}^{3}\,).\end{aligned}
$$

## Constraints, identity and validation

All parameters are integers. Affine shifts b range from -9 through 9; the constant-first negative-slope profile uses b=1 through 9. Polynomial c ranges from 1 through 12. For sqrt(5x+b), the derivative exists only on 5x+b>0. For the reciprocal radical, 2x^4-x^2+c = 2(x^2-1/4)^2+c-1/8 is strictly positive for every real x. Polynomial templates have real domain. Invalid duplicate or equivalent options cause validation failure.

Mathematical fingerprints parse the visible function and requested response shape, independent of seed, UUID and option order. They merge identical tasks across radio/blank banks. Field-owned answer identities are deterministic UUIDs. Every source bank is replayed exactly, and every finite parameter value is validated by independent displayed-expression differentiation, unique correct option checks, solution simplification and actual application grading. Generated output has no Math Academy IDs.

Replenishment rechecks native inventory and distinct validated availability under api.lock, prepares additive forms using the configured application contributor, requests native specs, previews, saves exact guarded requests, commits and verifies the full scoped readback. Only this KP and new content entities may change.
