# Template extraction

Captured at EDB basis 2637, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. All ten original practice records and the canonical example are retained in source.json. Eight complete sources are rated easy; two legacy sources lack their key, rating and solution and are excluded.

The shared assessment is selecting the arc-length integral of a supplied polynomial parametric curve on a supplied interval. Six Markdown/value families differ in their derivative structures, factorization stage or illustration. Each of the eight source questions retains its own complete five-choice bank. Classification groups and profile membership are in classification.json. No bank pooling is used.

The fixed backbone is the supplied x(t), y(t), one radio field named selection, five integral expressions, the formula L = integral sqrt((dx/dt)^2+(dy/dt)^2), the two explicit differentiation stages and substitution/simplification in the original worked solution. The factored t in q-15174 requires nonnegative t. Every original choice, with field, answer identity, exact text, radicand, outside factor and replay result, is mapped in choice-recipes.json. Psychological interpretations are unresolved; no inferred mistakes replace observed expressions.

Only the two endpoint roles vary. The lower and upper bound must change together in the prompt, every answer and every explicit solution integral. Curves, coefficients, translations, powers, operators, choice order and answer shapes are fixed. Coefficients remain fixed as a conservative policy because their source distractor derivations are not evidenced. Bounds are a conservative same-method generalization: they alter the mathematical integral without adding differentiation or integration stages; the question still asks for an expression, not its evaluation. No seed-only, identity-only or option-order variants count. Canonical IDs never enter generated content.

Normal sampling uses integral bounds a in 2..8, b in a+1..a+4 on four nonplot source profiles; q-85724 instead uses negative intervals a in -8..-3 with a < b <= -1. Every domain cell is filtered by exact polynomial root isolation: all five integrands must be real and their squared integrands strictly pairwise ordered throughout the interval. This proves unique definite integral values, not merely distinct text. All 126 admitted cells are independently validated, rather than relying on random sampling. The endpoint domain is deliberately bounded and is not a claim of mathematical exhaustion.

Some original distractors are nonreal on part of their original intervals (exact rational witnesses in source-issues.json). Original replay preserves those banks for fidelity evidence; generated intervals avoid these defects. Original questions and learner history are never repaired or rewritten here.

## Source-specific components

### q-123005

x=t**3 - 8, y=t**4 + 5*t; original interval [-2, 3].

Which of the following gives the length of the curve defined by the parametric equations
$x={t}^{3}-8,\,y={t}^{4}+5t$
from $t=-2$ to $t=3$ ?

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}({t}^{3}-8)=3{t}^{2}\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}({t}^{4}+5t)=4{t}^{3}+5\,.\end{aligned}
$$

We substitute these derivatives in the formula for arc length, and we get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{-2}^{3}\sqrt{{(3{t}^{2})}^{2}+{(4{t}^{3}+5)}^{2}}\,\text{d}t \\  & ={\int }_{-2}^{3}\sqrt{9{t}^{4}+16{t}^{6}+40{t}^{3}+25}\,\text{d}t \\  & ={\int }_{-2}^{3}\sqrt{16{t}^{6}+9{t}^{4}+40{t}^{3}+25}\,\text{d}t\,.\end{aligned}
$$

### q-123019

x=3*t**2, y=5*t; original interval [0, 1].

![](images/0a/0a58808ee9b20e201d1ea8a31683f742e02f739127640de2fea87ce4757e7901.png)

Which of the following gives the length of the curve defined by the parametric equations
$x=3{t}^{2},\,y=5t$
from $t=0$ to $t=1$ (shown above)?

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(3{t}^{2})=6t\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5t)=5.\end{aligned}
$$

We substitute these derivatives in the formula for arc length, and we get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{1}\sqrt{(6t)^{2}+(5)^{2}}\,\text{d}t \\  & ={\int }_{0}^{1}\sqrt{36{t}^{2}+25}\,\text{d}t\,.\end{aligned}
$$

### q-123025

x=3*t**3 + 5, y=t**2 - 5*t; original interval [-1, 2].

Which of the following gives the length of the curve defined by the parametric equations
$x=3{t}^{3}+5,\,y={t}^{2}-5t$
from $t=-1$ to $t=2$ ?

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(3{t}^{3}+5)=9{t}^{2}\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}({t}^{2}-5t)=2t-5.\end{aligned}
$$

We substitute these derivatives in the formula for arc length, and we get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{-1}^{2}\sqrt{(9{t}^{2})^{2}+(2t-5)^{2}}\,\text{d}t \\  & ={\int }_{-1}^{2}\sqrt{81{t}^{4}+4{t}^{2}-20t+25}\,\text{d}t.\end{aligned}
$$

### q-81377

x=t - 1, y=t**2 + 2; original interval [-1, 2].

Which of the following gives the length of the curve defined by the parametric equations
$x=t-1,\,y={t}^{2}+2$
from $t=-1$ to $t=2$ ?

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(t-1)=1\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}({t}^{2}+2)=2t\,.\end{aligned}
$$

We substitute these derivatives in the formula for arc length, and we get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{-1}^{2}\sqrt{{(1)}^{2}+{(2t)}^{2}}\,\text{d}t \\  & ={\int }_{-1}^{2}\sqrt{1+4{t}^{2}}\,\text{d}t\,.\end{aligned}
$$

### q-81380

x=t**3 + 1, y=3*t; original interval [-2, 0].

![](images/12/120220c7c1a24c68c1a9282548efcf62c34fd110bd11911799a2a83409f257ab.png)

Which of the following gives the length of the curve defined by the parametric equations
$x={t}^{3}+1,\,y=3t$
from $t=-2$ to $t=0$ (shown above)?

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}({t}^{3}+1)=3{t}^{2}\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(3t)=3.\end{aligned}
$$

We substitute these derivatives in the formula for arc length, and we get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{-2}^{0}\sqrt{(3{t}^{2})^{2}+(3)^{2}}\,\text{d}t \\  & ={\int }_{-2}^{0}\sqrt{9{t}^{4}+9}\,\text{d}t \\  & =3{\int }_{-2}^{0}\sqrt{{t}^{4}+1}\,\text{d}t\,.\end{aligned}
$$

### q-85724

x=t**3 - 1, y=t**2 - t; original interval [0, 1].

Which of the following gives the length of the curve defined by the parametric equations
$x={t}^{3}-1,\,y={t}^{2}-t$
from $t=0$ to $t=1$ ?

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}({t}^{3}-1)=3{t}^{2}\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}({t}^{2}-t)=2t-1.\end{aligned}
$$

We substitute these derivatives in the formula for arc length, and we get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{1}\sqrt{(3{t}^{2})^{2}+(2t-1)^{2}}\,\text{d}t \\  & ={\int }_{0}^{1}\sqrt{9{t}^{4}+4{t}^{2}-4t+1}\,\text{d}t.\end{aligned}
$$

### q-123020

x=t**3 - 4, y=2*t; original interval [-2, 0].

![](images/ae/ae210abc4028440aa9c822510d68f0ab0b8ba4b9f5806dd299149e953ccd1b21.png)

Which of the following gives the length of the curve defined by the parametric equations
$x={t}^{3}-4,\,y=2t$
from $t=-2$ to $t=0$ (shown above)?

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}({t}^{3}-4)=3{t}^{2}\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(2t)=2.\end{aligned}
$$

We substitute these derivatives in the formula for arc length, and we get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{-2}^{0}\sqrt{(3{t}^{2})^{2}+(2)^{2}}\,\text{d}t \\  & ={\int }_{-2}^{0}\sqrt{9{t}^{4}+4}\,\text{d}t\,.\end{aligned}
$$

### q-15174

x=t**3 + t**2, y=t**3 - t**2; original interval [0, 1].

Which of the following gives the length of the curve defined by the parametric equations
$x={t}^{3}+{t}^{2},\,y={t}^{3}-{t}^{2}$
from $t=0$ to $t=1$ ?

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}({t}^{3}+{t}^{2})=3{t}^{2}+2t\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}({t}^{3}-{t}^{2})=3{t}^{2}-2t\,.\end{aligned}
$$

We substitute these derivatives in the formula for arc length, and we get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{1}\sqrt{{(3{t}^{2}+2t)}^{2}+{(3{t}^{2}-2t)}^{2}}\,\text{d}t \\  & ={\int }_{0}^{1}\sqrt{9{t}^{4}+12{t}^{3}+4{t}^{2}+9{t}^{4}-12{t}^{3}+4{t}^{2}}\,\text{d}t \\  & ={\int }_{0}^{1}\sqrt{18{t}^{4}+8{t}^{2}}\,\text{d}t \\  & ={\int }_{0}^{1}t\sqrt{18{t}^{2}+8}\,\text{d}t\,.\end{aligned}
$$

