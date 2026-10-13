# Template extraction

## 1. Specific observed instances

Every raw original is preserved in source.json; bank/source masks below preserve full notation, order, and punctuation.

## 2. Generalized pattern

Parameterize the printed circle/ellipse with x=a cos t,y=b sin t on the printed CCW arc; compute tangent derivatives; substitute both coefficients and differentials; distribute, collect and simplify. Easy stops with the equivalent definite integral. Moderate includes antiderivative and ordered endpoint evaluation. Preserve each distinct source row mask rather than making all source solutions one generic template.

## 3. Components and complete observed banks

The global parameter c multiplies the entire one-form. Every source integral-stage node and full answer component is multiplied by the same c, using linearity. Parametrization, tangent derivatives, coordinates, axes and t-limit equations remain unscaled. At c=1 the multiplier is the empty rendering identity. This is a truly parameterized expression recipe, not a literal-return branch or correct-answer lookup. Numerical source distractor intentions remain unresolved. Each entire source bank stays together; it is not used as a default authored error bank.

### q-124597

Which of the following is equivalent to ${\int }_{C}{y}^{2}\,dx-{x}^{2}\,dy,$ where $C$ is part of the circle ${x}^{2}+{y}^{2}=1$ traversed in the counterclockwise direction from the point $A(1,0)$ to the point $B(0,1).$

Shape: axes (1,1); quarter-angle limits (0,1); P=y**2, Q=-x**2.

Source complete bank (each value is one indivisible component; c scaling is the replay operation):

1. Incorrect: ${\int }_{0}^{\pi /2}{sin}^{2}⁡t\operatorname{cos}⁡t+{cos}^{2}⁡t\operatorname{sin}⁡t\,\text{d}t$ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

2. Incorrect: ${\int }_{0}^{\pi /2}{sin}^{2}⁡t\operatorname{cos}⁡t\,\text{d}t$ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

3. Incorrect: $-{\int }_{0}^{\pi /2}{sin}^{3}⁡t\,\text{d}t$ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

4. Incorrect: ${\int }_{0}^{\pi /2}\frac{1}{2}\operatorname{sin}⁡2t\,\text{d}t$ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

5. Correct: $-{\int }_{0}^{\pi /2}{sin}^{3}⁡t+{cos}^{3}⁡t\,\text{d}t$ — parameterized recipe `c × complete component`; assessed tangent substitution.

Ordered source integral arithmetic masks:

1. `${\int }_{0}^{\pi /2}{y}^{2}\,\frac{dx}{\text{d}t}\,\text{d}t-{x}^{2}\,\frac{dy}{\text{d}t}\,\text{d}t $`

2. `${\int }_{0}^{\pi /2}({y}^{2}\,\frac{dx}{\text{d}t}-{x}^{2}\,\frac{dy}{\text{d}t})\,\text{d}t $`

3. `${\int }_{0}^{\pi /2}(\operatorname{sin}⁡t)^{2}\cdot (-\operatorname{sin}⁡t)-(\operatorname{cos}⁡t)^{2}\cdot \operatorname{cos}⁡t\,\text{d}t $`

4. `${\int }_{0}^{\pi /2}-{sin}^{3}⁡t-{cos}^{3}⁡t\,\text{d}t $`

5. `$-{\int }_{0}^{\pi /2}{sin}^{3}⁡t+{cos}^{3}⁡t\,\text{d}t$`

Full shared prose and path/differential masks (unaltered by c):

```text

Since $C$ is a circle of radius $1$ centered at the origin, it can be parametrized as follows:

$$
\begin{aligned}r(t) & =x(t)\,i+y(t)\,j=\operatorname{cos}⁡t\,i+\operatorname{sin}⁡t\,j,\,t\in [0,\frac{\pi }{2}]\end{aligned}
$$

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=-\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j.\end{aligned}
$$

Therefore, we can write our line integral as follows:

$$
<ORDERED INTEGRAL ROWS>\end{aligned}
$$

```

### q-81192

Evaluate ${\int }_{C}\frac{y\,dy-x\,dx}{{x}^{2}+{y}^{2}},$ where $C$ is part of the circle ${x}^{2}+{y}^{2}=1$ traversed in the counterclockwise direction from the point $(1,0)$ to the point $(0,1).$

Shape: axes (1,1); quarter-angle limits (0,1); P=-x/(x**2 + y**2), Q=y/(x**2 + y**2).

Source complete bank (each value is one indivisible component; c scaling is the replay operation):

1. Incorrect: $\frac{2}{3}$ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

2. Incorrect: $\frac{1}{4}$ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

3. Incorrect: $2$ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

4. Correct: $1$ — parameterized recipe `c × complete component`; assessed tangent substitution.

5. Incorrect: $\frac{1}{2}1$ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

Ordered source integral arithmetic masks:

1. `${\int }_{0}^{\pi /2}\frac{y\cdot {y}^{′}\,\text{d}t-x\cdot {x}^{′}\,\text{d}t}{{x}^{2}+{y}^{2}} $`

2. `${\int }_{0}^{\pi /2}\frac{y\cdot {y}^{′}-x\cdot {x}^{′}}{{x}^{2}+{y}^{2}}\,\text{d}t $`

3. `${\int }_{0}^{\pi /2}\frac{\operatorname{sin}⁡t\cdot \operatorname{cos}⁡t-\operatorname{cos}⁡t\cdot (-\operatorname{sin}⁡t)}{{cos}^{2}⁡t+{sin}^{2}⁡t}\,\text{d}t $`

4. `${\int }_{0}^{\pi /2}\operatorname{sin}⁡t\operatorname{cos}⁡t+\operatorname{sin}⁡t\operatorname{cos}⁡t\,\text{d}t $`

5. `${\int }_{0}^{\pi /2}2\operatorname{sin}⁡t\operatorname{cos}⁡t\,\text{d}t $`

6. `${\int }_{0}^{\pi /2}\operatorname{sin}⁡2t\,\text{d}t $`

7. `${[-\frac{1}{2}\operatorname{cos}⁡2t]}_{0}^{\pi /2} $`

8. `$-\frac{1}{2}[\operatorname{cos}⁡(\pi )-\operatorname{cos}⁡(0)] $`

9. `$-\frac{1}{2}[-1-1] $`

10. `$1$`

Full shared prose and path/differential masks (unaltered by c):

```text

Since $C$ is a circle of radius $1$ centered at the origin, it can be parametrized as follows:

$$
\begin{aligned}r(t) & =x(t)\,i+y(t)\,j=\operatorname{cos}⁡t\,i+\operatorname{sin}⁡t\,j,\,t\in [0,\frac{\pi }{2}]\end{aligned}
$$

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=-\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
<ORDERED INTEGRAL ROWS>\end{aligned}
$$

```

### q-124656

Which of the following is equivalent to ${\int }_{C}{x}^{2}y\,dx+x\,dy,$ where $C$ is part of the circle ${x}^{2}+{y}^{2}=4$ traversed in the counterclockwise direction from the point $A(2,0)$ to the point $B(-2,0).$

Shape: axes (2,2); quarter-angle limits (0,2); P=x**2*y, Q=x.

Source complete bank (each value is one indivisible component; c scaling is the replay operation):

1. Incorrect: $2{\int }_{0}^{\pi }{cos}^{2}⁡t(1-2{sin}^{2}⁡t)\,\text{d}t$ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

2. Incorrect: $8{\int }_{0}^{\pi }{cos}^{2}⁡t{sin}^{2}⁡t\,\text{d}t$ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

3. Incorrect: $8{\int }_{0}^{\pi }{cos}^{2}⁡t(1-2{cos}^{2}⁡t)\,\text{d}t$ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

4. Incorrect: $4{\int }_{0}^{\pi }{sin}^{2}⁡t(1-4{cos}^{2}⁡t)\,\text{d}t$ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

5. Correct: $4{\int }_{0}^{\pi }{cos}^{2}⁡t(1-4{sin}^{2}⁡t)\,\text{d}t$ — parameterized recipe `c × complete component`; assessed tangent substitution.

Ordered source integral arithmetic masks:

1. `${\int }_{0}^{\pi }{x}^{2}y\,\frac{dx}{\text{d}t}\,\text{d}t+x\,\frac{dy}{\text{d}t}\,\text{d}t $`

2. `${\int }_{0}^{\pi }({x}^{2}y\,\frac{dx}{\text{d}t}+x\,\frac{dy}{\text{d}t})\,\text{d}t $`

3. `${\int }_{0}^{\pi }(2\operatorname{cos}⁡t)^{2}\cdot (2\operatorname{sin}⁡t)\cdot (-2\operatorname{sin}⁡t)+(2\operatorname{cos}⁡t)\cdot 2\operatorname{cos}⁡t\,\text{d}t $`

4. `${\int }_{0}^{\pi }-16{sin}^{2}⁡t{cos}^{2}⁡t+4{cos}^{2}⁡t\,\text{d}t $`

5. `$4{\int }_{0}^{\pi }{cos}^{2}⁡t(1-4{sin}^{2}⁡t)\,\text{d}t$`

Full shared prose and path/differential masks (unaltered by c):

```text

Since $C$ is a circle of radius $2$ centered at the origin, it can be parametrized as follows:

$$
\begin{aligned}r(t) & =x(t)\,i+y(t)\,j=2\operatorname{cos}⁡t\,i+2\operatorname{sin}⁡t\,j,\,t\in [0,\pi ]\end{aligned}
$$

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=-2\operatorname{sin}⁡t\,i+2\operatorname{cos}⁡t\,j.\end{aligned}
$$

Therefore, we can write our line integral as follows:

$$
<ORDERED INTEGRAL ROWS>\end{aligned}
$$

```

### q-124657

Which of the following is equivalent to ${\int }_{C}\frac{2}{y}\,dx+y{e}^{x}\,dy,$ where $C$ is part of the ellipse $4{x}^{2}+{y}^{2}=4$ traversed in the counterclockwise direction from the point $A(1,0)$ to the point $B(0,2).$

Shape: axes (1,2); quarter-angle limits (0,1); P=2/y, Q=y*exp(x).

Source complete bank (each value is one indivisible component; c scaling is the replay operation):

1. Incorrect: ${\int }_{0}^{\pi /2}\operatorname{cos}⁡t\,{e}^{\operatorname{cos}⁡t}-\operatorname{sin}⁡t\,\text{d}t$ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

2. Correct: ${\int }_{0}^{\pi /2}4\operatorname{sin}⁡t\operatorname{cos}⁡t\,{e}^{\operatorname{cos}⁡t}-1\,\text{d}t$ — parameterized recipe `c × complete component`; assessed tangent substitution.

3. Incorrect: ${\int }_{0}^{\pi /2}2\operatorname{sin}⁡t\operatorname{cos}⁡t\,{e}^{\operatorname{cos}⁡t}+1\,\text{d}t$ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

4. Incorrect: ${\int }_{0}^{3\pi /2}\operatorname{sin}⁡t\,{e}^{\operatorname{cos}⁡t}+2\operatorname{cos}⁡t\,\text{d}t$ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

5. Incorrect: ${\int }_{\pi /2}^{\pi }\operatorname{sin}⁡t\operatorname{cos}⁡t\,{e}^{\operatorname{cos}⁡t}-2\,\text{d}t$ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

Ordered source integral arithmetic masks:

1. `${\int }_{0}^{\pi /2}\frac{2}{y}\,\frac{dx}{\text{d}t}\,\text{d}t+y{e}^{x}\,\frac{dy}{\text{d}t}\,\text{d}t $`

2. `${\int }_{0}^{\pi /2}(\frac{2}{y}\,\frac{dx}{\text{d}t}+y{e}^{x}\,\frac{dy}{\text{d}t})\,\text{d}t $`

3. `${\int }_{0}^{\pi /2}\frac{2}{2\operatorname{sin}⁡t}\cdot (-\operatorname{sin}⁡t)+(2\operatorname{sin}⁡t\,{e}^{\operatorname{cos}⁡t})\cdot 2\operatorname{cos}⁡t\,\text{d}t $`

4. `${\int }_{0}^{\pi /2}4\operatorname{sin}⁡t\operatorname{cos}⁡t\,{e}^{\operatorname{cos}⁡t}-1\,\text{d}t$`

Full shared prose and path/differential masks (unaltered by c):

```text

Since $C$ is an ellipse centered at $O$ with horizontal and vertical semiaxes of $1$ and $2,$ respectively, it can be parametrized as follows:

$$
\begin{aligned}r(t) & =x(t)\,i+y(t)\,j=\operatorname{cos}⁡t\,i+2\operatorname{sin}⁡t\,j,\,t\in [0,\frac{\pi }{2}]\end{aligned}
$$

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=-\operatorname{sin}⁡t\,i+2\operatorname{cos}⁡t\,j.\end{aligned}
$$

Therefore, we can write our line integral as follows:

$$
<ORDERED INTEGRAL ROWS>\end{aligned}
$$

```

### q-124661

Evaluate ${\int }_{C}(x-y)\,dx+(x+y)\,dy,$ where $C$ is part of the ellipse $9{x}^{2}+4{y}^{2}=36$ traversed in the counterclockwise direction from the point $(0,3)$ to the point $(-2,0).$

Shape: axes (2,3); quarter-angle limits (1,2); P=x - y, Q=x + y.

Source complete bank (each value is one indivisible component; c scaling is the replay operation):

1. Incorrect: $6\pi $ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

2. Correct: $\frac{6\pi -5}{2}$ — parameterized recipe `c × complete component`; assessed tangent substitution.

3. Incorrect: $\frac{5\pi +1}{4}$ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

4. Incorrect: $\frac{12\pi -5}{4}$ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

5. Incorrect: $3\pi $ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

Ordered source integral arithmetic masks:

1. `${\int }_{\pi /2}^{\pi }(x-y)\,\frac{dx}{\text{d}t}\,\text{d}t+(x+y)\,\frac{dy}{\text{d}t}\,\text{d}t $`

2. `${\int }_{\pi /2}^{\pi }((x-y)\,\frac{dx}{\text{d}t}+(x+y)\,\frac{dy}{\text{d}t})\,\text{d}t $`

3. `${\int }_{\pi /2}^{\pi }(2\operatorname{cos}⁡t-3\operatorname{sin}⁡t)\cdot (-2\operatorname{sin}⁡t)+(2\operatorname{cos}⁡t+3\operatorname{sin}⁡t)\cdot 3\operatorname{cos}⁡t\,\text{d}t $`

4. `${\int }_{\pi /2}^{\pi }(-4\operatorname{cos}⁡t\operatorname{sin}⁡t+6{sin}^{2}⁡t+6{cos}^{2}⁡t+9\operatorname{cos}⁡t\operatorname{sin}⁡t)\,\text{d}t $`

5. `${\int }_{\pi /2}^{\pi }5\operatorname{sin}⁡t\operatorname{cos}⁡t+6\,\text{d}t $`

6. `${\int }_{\pi /2}^{\pi }\frac{5}{2}\operatorname{sin}⁡2t+6\,\text{d}t $`

7. `${[-\frac{5}{4}\operatorname{cos}⁡2t+6t]}_{\pi /2}^{\pi } $`

8. `$[(-\frac{5}{4}\operatorname{cos}⁡(2\pi )+6\pi )-(-\frac{5}{4}\operatorname{cos}⁡(\pi )+3\pi )] $`

9. `$(-\frac{5}{4}+6\pi )-(\frac{5}{4}+3\pi ) $`

10. `$3\pi -\frac{5}{2} $`

11. `$\frac{6\pi -5}{2}$`

Full shared prose and path/differential masks (unaltered by c):

```text

Since $C$ is an ellipse centered at $O$ with horizontal and vertical semiaxes of $2$ and $3,$ respectively, it can be parametrized as follows:

$$
\begin{aligned}r(t) & =x(t)\,i+y(t)\,j=2\operatorname{cos}⁡t\,i+3\operatorname{sin}⁡t\,j,\,t\in [\frac{\pi }{2},\pi ]\end{aligned}
$$

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & ={x}^{′}(t)\,i+{y}^{′}(t)\,j=-2\operatorname{sin}⁡t\,i+3\operatorname{cos}⁡t\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
<ORDERED INTEGRAL ROWS>\end{aligned}
$$

```

### q-124665

Evaluate ${\int }_{C}dx+\frac{2}{x}\,dy,$ where $C$ is part of the ellipse $9{x}^{2}+{y}^{2}=9$ traversed in the counterclockwise direction from the point $(-1,0)$ to the point $(0,-3).$

Shape: axes (1,3); quarter-angle limits (2,3); P=1, Q=2/x.

Source complete bank (each value is one indivisible component; c scaling is the replay operation):

1. Incorrect: $2\pi -1$ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

2. Incorrect: $3\pi -4$ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

3. Incorrect: $4\pi $ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

4. Correct: $3\pi +1$ — parameterized recipe `c × complete component`; assessed tangent substitution.

5. Incorrect: $\frac{3\pi +1}{2}$ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

Ordered source integral arithmetic masks:

1. `${\int }_{\pi }^{3\pi /2}\frac{dx}{\text{d}t}\,\text{d}t+\frac{2}{x}\,\frac{dy}{\text{d}t}\,\text{d}t $`

2. `${\int }_{\pi }^{3\pi /2}(\frac{dx}{\text{d}t}+\frac{2}{x}\,\frac{dy}{\text{d}t})\text{d}t $`

3. `${\int }_{\pi }^{3\pi /2}(-\operatorname{sin}⁡t)+\frac{2}{\operatorname{cos}⁡t}\cdot 3\operatorname{cos}⁡t\,\text{d}t $`

4. `${\int }_{\pi }^{3\pi /2}-\operatorname{sin}⁡t+6\,\text{d}t $`

5. `$[\operatorname{cos}⁡t+6t]_{\pi }^{3\pi /2} $`

6. `$(\operatorname{cos}⁡(\frac{3\pi }{2})+9\pi )-(\operatorname{cos}⁡\pi +6\pi ) $`

7. `$(0+9\pi )-(-1+6\pi ) $`

8. `$3\pi +1$`

Full shared prose and path/differential masks (unaltered by c):

```text

Since $C$ is an ellipse centered at $O$ with horizontal and vertical semiaxes of $1$ and $3,$ respectively, it can be parametrized as follows:

$$
\begin{aligned}r(t) & =x(t)\,i+y(t)\,j=\operatorname{cos}⁡t\,i+3\operatorname{sin}⁡t\,j,\,t\in [\pi ,\frac{3\pi }{2}]\end{aligned}
$$

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=-\operatorname{sin}⁡t\,i+3\operatorname{cos}⁡t\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
<ORDERED INTEGRAL ROWS>\end{aligned}
$$

```

### q-124651

Which of the following is equivalent to ${\int }_{C}{x}^{2}\,dx+xy\,dy,$ where $C$ is part of the ellipse ${x}^{2}+4{y}^{2}=4$ traversed in the counterclockwise direction from the point $A(2,0)$ to the point $B(0,1).$

Shape: axes (2,1); quarter-angle limits (0,1); P=x**2, Q=x*y.

Source complete bank (each value is one indivisible component; c scaling is the replay operation):

1. Incorrect: $6{\int }_{0}^{\pi /2}\operatorname{cos}⁡t\operatorname{sin}⁡t(\operatorname{cos}⁡t-\operatorname{sin}⁡t)\,\text{d}t$ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

2. Incorrect: $-2{\int }_{0}^{\pi /2}{cos}^{2}⁡t{sin}^{2}⁡t\,\text{d}t$ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

3. Correct: $-6{\int }_{0}^{\pi /2}{cos}^{2}⁡t\operatorname{sin}⁡t\,\text{d}t$ — parameterized recipe `c × complete component`; assessed tangent substitution.

4. Incorrect: ${\int }_{0}^{\pi /2}\operatorname{cos}⁡t\operatorname{sin}⁡t(\operatorname{cos}⁡t+\operatorname{sin}⁡t)\,\text{d}t$ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

5. Incorrect: $3{\int }_{0}^{\pi /2}\operatorname{cos}⁡t{sin}^{2}⁡t\,\text{d}t$ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

Ordered source integral arithmetic masks:

1. `${\int }_{0}^{\pi /2}{x}^{2}\,\frac{dx}{\text{d}t}\,\text{d}t+xy\,\frac{dy}{\text{d}t}\,\text{d}t $`

2. `${\int }_{0}^{\pi /2}({x}^{2}\,\frac{dx}{\text{d}t}+xy\,\frac{dy}{\text{d}t})\,\text{d}t $`

3. `${\int }_{0}^{\pi /2}(2\operatorname{cos}⁡t)^{2}\cdot (-2\operatorname{sin}⁡t)+(2\operatorname{cos}⁡t)\cdot \operatorname{sin}⁡t\cdot \operatorname{cos}⁡t\,\text{d}t $`

4. `${\int }_{0}^{\pi /2}-8{cos}^{2}⁡t\operatorname{sin}⁡t+2{cos}^{2}⁡t\operatorname{sin}⁡t\,\text{d}t $`

5. `$-6{\int }_{0}^{\pi /2}{cos}^{2}⁡t\operatorname{sin}⁡t\,\text{d}t$`

Full shared prose and path/differential masks (unaltered by c):

```text

Since $C$ is an ellipse centered at $O$ with horizontal and vertical semiaxes of $2$ and $1,$ respectively, it can be parametrized as follows:

$$
\begin{aligned}r(t) & =x(t)\,i+y(t)\,j=2\operatorname{cos}⁡t\,i+\operatorname{sin}⁡t\,j,\,t\in [0,\frac{\pi }{2}]\end{aligned}
$$

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=-2\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j.\end{aligned}
$$

Therefore, we can write our line integral as follows:

$$
<ORDERED INTEGRAL ROWS>\end{aligned}
$$

```

### q-124653

Which of the following is equivalent to ${\int }_{C}({e}^{x}+y)\,dx-x\,dy,$ where $C$ is part of the circle ${x}^{2}+{y}^{2}=3$ traversed in the counterclockwise direction from the point $A(0,\sqrt{3})$ to the point $B(-\sqrt{3},0).$

Shape: axes (sqrt(3),sqrt(3)); quarter-angle limits (1,2); P=y + exp(x), Q=-x.

Source complete bank (each value is one indivisible component; c scaling is the replay operation):

1. Incorrect: $-{\int }_{\pi /2}^{\pi }\operatorname{sin}⁡t\,{e}^{3\operatorname{cos}⁡t}+3\,\text{d}t$ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

2. Incorrect: $-{\int }_{\pi /2}^{\pi }\operatorname{sin}⁡t\,{e}^{\sqrt{3}\operatorname{cos}⁡t}+\sqrt{3}\operatorname{cos}⁡t\,\text{d}t$ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

3. Incorrect: $-3{\int }_{\pi /2}^{\pi }\operatorname{sin}⁡t\,{e}^{\sqrt{3}\operatorname{cos}⁡t}\,\text{d}t$ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

4. Incorrect: ${\int }_{\pi /2}^{\pi }\sqrt{3}\operatorname{sin}⁡t\,{e}^{3\operatorname{cos}⁡t}+1\,\text{d}t$ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

5. Correct: $-{\int }_{\pi /2}^{\pi }\sqrt{3}\operatorname{sin}⁡t\,{e}^{\sqrt{3}\operatorname{cos}⁡t}+3\,\text{d}t$ — parameterized recipe `c × complete component`; assessed tangent substitution.

Ordered source integral arithmetic masks:

1. `${\int }_{\pi /2}^{\pi }({e}^{x}+y)\,\frac{dx}{\text{d}t}\,\text{d}t-x\,\frac{dy}{\text{d}t}\,\text{d}t $`

2. `${\int }_{\pi /2}^{\pi }(({e}^{x}+y)\,\frac{dx}{\text{d}t}-x\,\frac{dy}{\text{d}t})\,\text{d}t $`

3. `${\int }_{\pi /2}^{\pi }({e}^{\sqrt{3}\operatorname{cos}⁡t}+\sqrt{3}\operatorname{sin}⁡t)\cdot (-\sqrt{3}\operatorname{sin}⁡t)-(\sqrt{3}\operatorname{cos}⁡t)\cdot (\sqrt{3}\operatorname{cos}⁡t)\,\text{d}t $`

4. `${\int }_{\pi /2}^{\pi }-\sqrt{3}\operatorname{sin}⁡t\,{e}^{\sqrt{3}\operatorname{cos}⁡t}-3{sin}^{2}⁡t-3{cos}^{2}⁡t\,\text{d}t $`

5. `${\int }_{\pi /2}^{\pi }-\sqrt{3}\operatorname{sin}⁡t\,{e}^{\sqrt{3}\operatorname{cos}⁡t}-3\,\text{d}t $`

6. `$-{\int }_{\pi /2}^{\pi }\sqrt{3}\operatorname{sin}⁡t\,{e}^{\sqrt{3}\operatorname{cos}⁡t}+3\,\text{d}t$`

Full shared prose and path/differential masks (unaltered by c):

```text

Since $C$ is a circle of radius $\sqrt{3}$ centered at the origin, it can be parametrized as follows:

$$
\begin{aligned}r(t) & =x(t)\,i+y(t)\,j=\sqrt{3}\operatorname{cos}⁡t\,i+\sqrt{3}\operatorname{sin}⁡t\,j,\,t\in [\frac{\pi }{2},\pi ]\end{aligned}
$$

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=-\sqrt{3}\operatorname{sin}⁡t\,i+\sqrt{3}\operatorname{cos}⁡t\,j.\end{aligned}
$$

Therefore, we can write our line integral as follows:

$$
<ORDERED INTEGRAL ROWS>\end{aligned}
$$

```

### q-124655

Which of the following is equivalent to ${\int }_{C}(x-2y)\,dx+2x\,dy,$ where $C$ is part of the ellipse $9{x}^{2}+{y}^{2}=9$ traversed in the counterclockwise direction from the point $A(0,3)$ to the point $B(0,-3).$

Shape: axes (1,3); quarter-angle limits (1,3); P=x - 2*y, Q=2*x.

Source complete bank (each value is one indivisible component; c scaling is the replay operation):

1. Incorrect: ${\int }_{\pi /2}^{3\pi /2}6{sin}^{2}⁡t-\operatorname{cos}⁡t\,\text{d}t$ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

2. Incorrect: $2{\int }_{\pi /2}^{3\pi /2}\operatorname{sin}⁡t{cos}^{2}⁡t\,\text{d}t$ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

3. Correct: ${\int }_{\pi /2}^{3\pi /2}6-\operatorname{sin}⁡t\operatorname{cos}⁡t\,\text{d}t$ — parameterized recipe `c × complete component`; assessed tangent substitution.

4. Incorrect: ${\int }_{\pi /2}^{3\pi /2}3\operatorname{sin}⁡t+\operatorname{cos}⁡t\,\text{d}t$ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

5. Incorrect: ${\int }_{\pi /2}^{3\pi /2}3-{sin}^{2}⁡t\operatorname{cos}⁡t\,\text{d}t$ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

Ordered source integral arithmetic masks:

1. `${\int }_{\pi /2}^{3\pi /2}(x-2y)\,\frac{dx}{\text{d}t}\,\text{d}t+2x\,\frac{dy}{\text{d}t}\,\text{d}t $`

2. `${\int }_{\pi /2}^{3\pi /2}((x-2y)\,\frac{dx}{\text{d}t}+2x\,\frac{dy}{\text{d}t})\,\text{d}t $`

3. `${\int }_{\pi /2}^{3\pi /2}(\operatorname{cos}⁡t-2(3\operatorname{sin}⁡t))\cdot (-\operatorname{sin}⁡t)+2(\operatorname{cos}⁡t)\cdot 3\operatorname{cos}⁡t\,\text{d}t $`

4. `${\int }_{\pi /2}^{3\pi /2}-\operatorname{sin}⁡t\operatorname{cos}⁡t+6{sin}^{2}⁡t+6{cos}^{2}⁡t\,\text{d}t $`

5. `${\int }_{\pi /2}^{3\pi /2}6-\operatorname{sin}⁡t\operatorname{cos}⁡t\,\text{d}t$`

Full shared prose and path/differential masks (unaltered by c):

```text

Since $C$ is an ellipse centered at $O$ with horizontal and vertical semiaxes of $1$ and $3,$ respectively, it can be parametrized as follows:

$$
\begin{aligned}r(t) & =x(t)\,i+y(t)\,j=\operatorname{cos}⁡t\,i+3\operatorname{sin}⁡t\,j,\,t\in [\frac{\pi }{2},\frac{3\pi }{2}]\end{aligned}
$$

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=-\operatorname{sin}⁡t\,i+3\operatorname{cos}⁡t\,j.\end{aligned}
$$

Therefore, we can write our line integral as follows:

$$
<ORDERED INTEGRAL ROWS>\end{aligned}
$$

```

### q-81186

Evaluate ${\int }_{C}y\,dx+x\,dy,$ where $C$ is part of the circle ${x}^{2}+{y}^{2}=4$ traversed in the counterclockwise direction from the point $A(-2,0)$ to the point $B(0,-2).$

Shape: axes (2,2); quarter-angle limits (2,3); P=y, Q=x.

Source complete bank (each value is one indivisible component; c scaling is the replay operation):

1. Correct: $0$ — parameterized recipe `c × complete component`; assessed tangent substitution.

2. Incorrect: $4$ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

3. Incorrect: $-1$ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

4. Incorrect: $2$ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

5. Incorrect: $-2$ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

Ordered source integral arithmetic masks:

1. `${\int }_{\pi }^{3\pi /2}y\,\frac{dx}{\text{d}t}\,\text{d}t+x\,\frac{dy}{\text{d}t}\,\text{d}t $`

2. `${\int }_{\pi }^{3\pi /2}(y\,\frac{dx}{\text{d}t}+x\,\frac{dy}{\text{d}t})\text{d}t $`

3. `${\int }_{\pi }^{3\pi /2}(2\operatorname{sin}⁡t\cdot (-2\operatorname{sin}⁡t)+2\operatorname{cos}⁡t\cdot 2\operatorname{cos}⁡t)\text{d}t $`

4. `${\int }_{\pi }^{3\pi /2}(-4{sin}^{2}⁡t+4{cos}^{2}⁡t)\text{d}t $`

5. `$4{\int }_{\pi }^{3\pi /2}({cos}^{2}⁡t-{sin}^{2}⁡t)\text{d}t $`

6. `$4{\int }_{\pi }^{3\pi /2}\operatorname{cos}⁡(2t)\,\text{d}t $`

7. `$2\operatorname{sin}⁡2t{|}_{\pi }^{3\pi /2} $`

8. `$2[\operatorname{sin}⁡(3\pi )-\operatorname{sin}⁡(2\pi )] $`

9. `$2(0-0) $`

10. `$0$`

Full shared prose and path/differential masks (unaltered by c):

```text

First, we need to find the parametrization of the curve $C.$ Since it's a circle if radius $2$ centered at the origin, the curve $C$ can be parametrized as follows:

$$
\begin{aligned}r(t) & =x(t)\,i+y(t)\,j=2\operatorname{cos}⁡(t)\,i+2\operatorname{sin}⁡(t)\,j,\,t\in [\pi ,\frac{3\pi }{2}].\end{aligned}
$$

So, along the curve we have that $x(t)=2\operatorname{cos}⁡t$ and $y(t)=2\operatorname{sin}⁡t.$ 

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=-2\operatorname{sin}⁡(t)\,i+2\operatorname{cos}⁡(t)\,j.\end{aligned}
$$

Therefore, we can calculate the line integral as follows:

$$
<ORDERED INTEGRAL ROWS>\end{aligned}
$$

```

### q-90895

Evaluate ${\int }_{C}y\,dx-x\,dy,$ where $C$ is part of the circle ${x}^{2}+{y}^{2}=2$ traversed in the counterclockwise direction from the point $A(\sqrt{2},0)$ to the point $B(0,\sqrt{2}).$

Shape: axes (sqrt(2),sqrt(2)); quarter-angle limits (0,1); P=y, Q=-x.

Source complete bank (each value is one indivisible component; c scaling is the replay operation):

1. Incorrect: $0$ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

2. Incorrect: $\frac{\pi }{3}$ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

3. Incorrect: $-\frac{\pi }{3}$ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

4. Correct: $-\pi $ — parameterized recipe `c × complete component`; assessed tangent substitution.

5. Incorrect: $\pi $ — parameterized recipe `c × complete component`; unresolved source intent; replay-only entire-expression scaling.

Ordered source integral arithmetic masks:

1. `${\int }_{0}^{\pi /2}y\,\frac{dx}{\text{d}t}\,\text{d}t-x\,\frac{dy}{\text{d}t}\,\text{d}t $`

2. `${\int }_{0}^{\pi /2}(y\,\frac{dx}{\text{d}t}-x\,\frac{dy}{\text{d}t})\,\text{d}t $`

3. `${\int }_{0}^{\pi /2}(\sqrt{2}\operatorname{sin}⁡t\cdot (-\sqrt{2}\operatorname{sin}⁡t)-\sqrt{2}\operatorname{cos}⁡t\cdot \sqrt{2}\operatorname{cos}⁡t)\text{d}t $`

4. `${\int }_{0}^{\pi /2}(-2{sin}^{2}⁡t-2{cos}^{2}⁡t)\text{d}t $`

5. `$-2{\int }_{0}^{\pi /2}\text{d}t $`

6. `$-2t{|}_{0}^{\pi /2} $`

7. `$-2[\frac{\pi }{2}-0] $`

8. `$-\pi $`

Full shared prose and path/differential masks (unaltered by c):

```text

First, we need to find the parametrization of the curve $C.$ Since it's a circle if radius $\sqrt{2}$ centered at the origin, the curve $C$ can be parametrized as follows:

$$
\begin{aligned}r(t) & =x(t)\,i+y(t)\,j=\sqrt{2}\operatorname{cos}⁡(t)\,i+\sqrt{2}\operatorname{sin}⁡(t)\,j,\,t\in [0,\frac{\pi }{2}].\end{aligned}
$$

So, along the curve we have that $x(t)=\sqrt{2}\operatorname{cos}⁡t$ and $y(t)=\sqrt{2}\operatorname{sin}⁡t.$ 

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=-\sqrt{2}\operatorname{sin}⁡(t)\,i+\sqrt{2}\operatorname{cos}⁡(t)\,j.\end{aligned}
$$

Therefore, we can calculate the line integral as follows:

$$
<ORDERED INTEGRAL ROWS>\end{aligned}
$$

```

## 4. Reusable template and authored extension

Fixed source components are prose, parameterization, derivative rows, curve equation, endpoints, arc bounds and the shape/order of each arithmetic node. The variable is a global signed nonzero multiplier c; it is inserted around complete mathematical components only. The original five owned answer fragments retain their exact notation at c=1, including the redundant final factor 1 in q-81192’s half-valued option. No option is replaced or pooled. All stage kinds and raw full source prose are compared one-to-one during every original/changed-c replay.

Normal authored templates use the same parametrization → derivative → symbolic integral sum → actual tangent-product substitution → distributed sum sequence, with the original shared connecting sentences. Evaluated templates retain primitive, raw endpoint substitution, evaluated per-term endpoint sums, and final collection as distinct masks. Hard adds collection and the explicitly authored double-angle power-reduction row. See classification.md for bounds, same-KP curriculum anchors and the absent-H design rationale.

The authored complete operation bank contains the correct tangent sum; omit dx contribution; omit dy contribution; reverse the dx contribution sign; replace both tangent derivatives with the coordinates. Easy renders all five complete definite integrals; moderate/hard evaluate all five on the same printed arc. Recipes are applied as a whole bank, rejecting equivalent or ambiguous instances. Neither the bank nor the fourth-angle row is claimed to be observed source code.

q-124657 and q-124665 require one-sided improper interpretation because an endpoint coefficient is undefined. Their tangent-composed integrands extend continuously. This qualification is documented separately from 11/11 raw-exact source strings and 55/55 bank values; there is no ordinary continuous-one-form claim. Any interior coefficient pole fails verification before cancellation.

## Complete mathematical value audit and repair

`q-124656` has an actual mathematical bank ambiguity: original options 4 and 5 (one-based source order) are different whole integral expressions both equal to zero. This does not pass answer-value uniqueness merely because one matches the intended substituted integrand. The explicit `observed_q-124656` profile retains it as raw evidence and carries `raw_ambiguous_bank=true`. The eligible `repaired_q-124656` profile replaces only original option 4 with `4 int_0^pi cos²t dt`, an omission of the dx contribution, evaluating to 2pi. It preserves the original designated answer, every other option, and all source sentences/arithmetic masks. Its parameterized recipe is `c * 4 int_0^pi cos²t dt`; it remains distinct from pi/2, pi, -2pi and zero for all allowed c. Complete-integral audits use exact polynomial integration and independent 70-digit quadrature for source exponential expressions. Authored E also rejects whole banks on scalar collisions; no transformed-integrand convention exempts ambiguity.
