# Template extraction

Scope is supported by frozen topic17592186050789 and lesson17592186050789 (basis2275). The introduction differentiates sin(2x); canonicale-732 differentiates2sin(3x-1). Sibling KPs separately cover reciprocal trig, trig powers and trig-of-trig, and are excluded.

The backbone is one outer sin/cos/tan applied directly to a polynomial in x. The source stages express a composite, differentiate outer and inner operands independently, multiply the chain factors, simplify, substitute the inner argument, and then evaluate a slope / apply point-slope form only where that source asks for it. q-31163 additionally preserves its source split into g+h and differentiation of the cubic. All these shared operative sentences are preserved as source components; only complete mathematical components and factor operands are masked simultaneously. There is no anchor-specific literal-return path.

Original parameter slots and field contracts:

## q-1943

Captured prompt: Calculate $\frac{df}{dx}$ for $f(x) = \cos (x^{2})$.

Original parameters: `{"a": 1}`. Served level: moderate. All allowed parameters and exact mathematical objects are implemented in parameters_for/model. Raw omissions are preserved; details in classification.json.

Complete original bank, in captured order:

- `x\sin (2x)`
- `-x\sin (x^{2})`
- `-2x\sin (x^{2})`
- `x^{2}\sin (2x)`
- `x^{2}\cos (x^{2})`

## q-1946

Captured prompt: Find $f^{′}(x)$ for $f(x) = \tan (2x + 2)$.

Original parameters: `{"a": 2, "b": 2}`. Served level: easy. All allowed parameters and exact mathematical objects are implemented in parameters_for/model. Raw omissions are preserved; details in classification.json.

Complete original bank, in captured order:

- `2\csc^{2} (2x + 2)`
- `2\cot (2x + 2)`
- `2\sec^{2} (2x + 2)`
- `2\sec (2x + 2)`
- `\sec^{2} (2x + 2)`

## q-310182

Captured prompt: Find the slope $m$ of $y =\sin \left(\pi \left(x^{2} + 2x - 2\right)\right)$ at $x = 1.$

$m=$
{{field-1}}

Original parameters: `{"a": 1, "b": 2}`. Served level: hard. All allowed parameters and exact mathematical objects are implemented in parameters_for/model. Raw omissions are preserved; details in classification.json.

Complete original bank, in captured order:

- `$-4\pi$`

## q-31241

Captured prompt: Find the slope of $y=\operatorname{sin}({x}^{2}+2x-1)$ at $x=0.$

Original parameters: `{"b": 2, "c": -1}`. Served level: hard. All allowed parameters and exact mathematical objects are implemented in parameters_for/model. Raw omissions are preserved; details in classification.json.

## q-48508

Captured prompt: Find the equation of the tangent to the curve $y = \cos (5x-2 )$ at the point $\left(\dfrac 2 5,1\right).$

Original parameters: `{"a": 5}`. Served level: hard. All allowed parameters and exact mathematical objects are implemented in parameters_for/model. Raw omissions are preserved; details in classification.json.

## q-48636

Captured prompt: Find the equation of the tangent to the curve $f(x) = \cos{\left(x^3\right)}$ at the point $\left(0,1\right).$

Original parameters: `{"a": 1}`. Served level: hard. All allowed parameters and exact mathematical objects are implemented in parameters_for/model. Raw omissions are preserved; details in classification.json.

## q-310179

Captured prompt: Given that $y=\operatorname{tan}⁡(3{x}^{4}-5)$, find $\frac{\text{d}y}{\text{d}x}.$

$\frac{\text{d}y}{\text{d}x}=$
{{field-1}}

Original parameters: `{"a": 3, "b": -5}`. Served level: moderate. All allowed parameters and exact mathematical objects are implemented in parameters_for/model. Raw omissions are preserved; details in classification.json.

Complete original bank, in captured order:

- `12{x}^{3}{sec}^{2}(3{x}^{4}-5)`

## q-310180

Captured prompt: Find the slope $m$ of the tangent to the curve $y=\operatorname{sin}⁡(3x)$ at $x=\frac{\pi }{6}.$

$m=$
{{field-1}}

Original parameters: `{"a": 3}`. Served level: moderate. All allowed parameters and exact mathematical objects are implemented in parameters_for/model. Raw omissions are preserved; details in classification.json.

Complete original bank, in captured order:

- `0`

## q-31153

Captured prompt: Find the slope of the tangent to the curve $y=\operatorname{sin}⁡(3x+5)$ at the point where $x=2.$

Original parameters: `{"b": 5}`. Served level: moderate. All allowed parameters and exact mathematical objects are implemented in parameters_for/model. Raw omissions are preserved; details in classification.json.

Complete original bank, in captured order:

- `3\operatorname{cos}⁡11`
- `-3\operatorname{cos}⁡11`
- `5\operatorname{cos}⁡2`
- `5\operatorname{cos}⁡11`
- `-5\operatorname{cos}⁡11`

## q-31163

Captured prompt: Calculate $\frac{\text{d}y}{\text{d}x}$ for $y=\operatorname{cos}⁡(11-2x)-6{x}^{3}.$

Original parameters: `{"b": 11}`. Served level: moderate. All allowed parameters and exact mathematical objects are implemented in parameters_for/model. Raw omissions are preserved; details in classification.json.

Complete original bank, in captured order:

- `-2\operatorname{sin}⁡(11-2x)-9{x}^{2}`
- `-\operatorname{cos}⁡(11-2x)-9{x}^{2}`
- `\operatorname{sin}⁡(11-2x)-18{x}^{2}`
- `2\operatorname{cos}⁡(11-2x)-18{x}^{2}`
- `2\operatorname{sin}⁡(11-2x)-18{x}^{2}`

## q-51026

Captured prompt: Find the equation of the tangent to the curve $y=2\operatorname{cos}⁡(x-1)$ at the point $(1+\pi ,-2).$

Original parameters: `{"A": 2}`. Served level: hard. All allowed parameters and exact mathematical objects are implemented in parameters_for/model. Raw omissions are preserved; details in classification.json.

Complete original bank, in captured order:

- `y=x-\pi -3`
- `y=x+\pi -2`
- `y=-2`
- `y=-2x+2\pi `
- `y=0`

## Full-bank recipes

Each bank is selected as a complete profile before constructing choices; an equivalent pair rejects the complete instance. Normal values never use a first-valid distractor pool. bank-recipes.json maps every original value to a served value at the source parameters; source.json preserves exact wording/types and source-cases.json replays all original fields, values and correct/missing designations.

- q-1943, u=a*x^2: x*sin(2*a*x), -x*sin(u), -2*a*x*sin(u), a*x^2*sin(2*a*x), a*x^2*cos(u). These retain the observed expression patterns (two compound input/output confusions); their precise pedagogical interpretation is not claimed beyond the explicit expressions.
- q-1946, u=a*x+b: a*csc(u)^2, a*cot(u), a*sec(u)^2, a*sec(u), sec(u)^2. Correct index2. Other reciprocal trig appears only as source distractors, never as a new differentiation target.
- q-31153, u=3*x+b at2: 3*cos(6+b), -3*cos(6+b), b*cos(2), b*cos(6+b), -b*cos(6+b). The offset is the actual inner-intercept slot. b=3 collides and is rejected.
- q-31163, u=b-2*x and h=-6*x^3: -2*sin(u)-9*x^2, -cos(u)-9*x^2, sin(u)-18*x^2, 2*cos(u)-18*x^2, 2*sin(u)-18*x^2. Nine is half the magnitude18 of the cubic derivative; these complete source recipes remain fixed except the phase slot.
- q-51026, A*cos(x-1) at(1+pi,-A): equations with RHS x-pi-(A+1), x+pi-A, -A, -A*x+A*pi,0. The first RHS follows an erroneous slope1 in point-slope form at the actual point; other RHS patterns are retained explicitly without inventing a single unproved error interpretation. Full equation objects have fixed left sidey and are compared by their full RHS.

Single-answer blanks contain the derivative/slope dictated by the printed function. Missing fields q-31241, q-48508 and q-48636 are authored completions, separate from observed omission. Tangent completions supply y= in the prompt and expect the RHS; this is necessary because the native blank-expression grader does not parse an equation. Source q-51026 remains a radio of complete equations. q-1943/q-1946 use authored ordered solutions grounded in the canonical common chain-rule stages and infer the unique mathematically correct source option. Raw source types/dollar wrappers are retained only in evidence; normal blank values are bare math TeX.

## Conservative parameter slots and default workload

Easy A=2..9, a=2..12, b=-12..12 excluding0 in A*sin(a*x+b):2112 function tasks with one inner derivative and one product of constants, then inner substitution. b=0 is excluded so every task retains the affine argument; no sign/alias/permutation counts are used.

Moderate a=1..24,b=-20..20 subject to|a+b|<=16 in tan(a*x^4+b):582 tasks. Every variant differentiates exactly one quartic monomial plus an additive shift and applies one chain rule. The shift changes the outer argument and pole set, so it is mathematically operative. This numeric bound permits the native grader's common-domain witness atx=1; it applies to every explicit learner-eligible source-bank call too. It is a grader-supported sampling restriction, not a mathematical limitation. The original a3,b-5 remains included.

Hard a,b=1..24 in sin(pi*(a*x^2+b*x-2)) atx=1:576 tasks. Every variant differentiates the two nonconstant quadratic terms, multiplies the outer derivative, substitutesx=1, evaluates cos(integer*pi), and gives a nonzero exact multiple ofpi. The fixed-2 has no diversity contribution. Varying a,b changes the inner derivative operand and function, not merely an unused constant. No numerical approximation or new operation is needed.

Explicit compatibility ranges are narrower than arbitrary mathematics: q-31241 c=-16..-1, b=1..24 to keep scalar cos(c) inside native argument bounds; q-1946 a2..12,b1..12; the remaining single-slot templates use1..40, excluding q-31153 b3. Horizontal tangent compatibility variants may have an unchanged final answer; they are excluded from the stated default meaningful counts.

Domain: all realx for sine/cosine; tan families exclude every zero of cos(u). Correctness/equivalence checks preserve poles. All served blank probes use actual native grader canonical/equivalent/wrong responses; same-domain wrong tan responses are used because a constant wrong response can have unresolved domain comparison. Larger tan arguments and |c|>16 are explicitly excluded from normal parameter bounds.
