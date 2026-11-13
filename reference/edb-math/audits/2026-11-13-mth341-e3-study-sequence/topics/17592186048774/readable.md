# 17592186048774 Solving Quadratic Equations by Factoring

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186065344 — Introduction

Suppose that we want to solve the quadratic equation

$$
x^2+5x+6=0
$$

The square root method won't work here, since there is a linear term. We can't factor out the variable, either, since there is a constant term. So, what should we do?

One way to solve this is to factor the entire trinomial on the left-hand side. To do this, we need to find two numbers that

- multiply to give $6$ (the constant term) and
- add to give $5$ (the linear coefficient).

These two numbers are $2$ and $3$. So, we can factor the left-hand-side as follows:

$$
\begin{aligned}
x^{2} + 5x + 6 &= 0 \\
x^{2} + \underbrace{2x + 3x}_{5x} + 6 &= 0 \\
(x^{2} + 2x) + (3x + 6) &= 0 \\
x(x + 2) + 3(x + 2) &= 0 \\
(x + 3)(x + 2) &= 0
\end{aligned}
$$

Applying the zero product rule, we have

$$
x+3=0 \qquad\text{or}\qquad x+2=0
$$

which in turn gives

$$
x=-3 \qquad\text{or}\qquad x=-2
$$

Therefore, the solutions are $x=-3,-2$.



### example 17592186063981 — Solving by Factoring When the Leading Coefficient is Positive

Solve the equation $x^2-5x +6=0$.

We will factor the left-hand side and then apply the zero product rule.

To factor the left-hand side, we need to find two numbers that multiply to $6$ and add to $-5$. These two numbers are $-2$ and $-3$, so we can factor the left-hand side as follows:

$$
\begin{aligned} x^2 - 5x + 6 &= 0 \\[5pt] x^2 \underbrace{-3x -2x}_{\large -5x} + 6 &= 0 \\[5pt] x(x-3) - 2(x-3) &= 0 \\[5pt] (x - 2)(x -3) &= 0 \end{aligned}
$$

Applying the zero product rule, we have

$$
x-2=0 \qquad\text{or}\qquad x-3=0
$$

which in turn gives

$$
x=2 \qquad\text{or}\qquad x=3
$$

Therefore, the solutions are $x=2,3$.

### example 17592186064007 — Solving by Factoring When the Leading Coefficient is Negative

Solve the equation $-x^2+7x+18=0$.

First, we multiply by $-1$ so that the leading coefficient becomes positive.

$$
\begin{aligned}
-x^{2} + 7x + 18 &= 0 \\
(-1)(-x^{2} + 7x + 18) &= (-1) \cdot (0) \\
x^{2} - 7x - 18 &= 0
\end{aligned}
$$

To factor the equation, we need two numbers that multiply to $-18$ and add to $-7$. These two numbers are $2$ and $-9$, so we can factor the left-hand side as follows:

$$
\begin{aligned}
x^{2} - 7x - 18 &= 0 \\
x^{2} + (2x - 9x) - 18 &= 0 \\
(x^{2} + 2x) + (-9x - 18) &= 0 \\
x(x + 2) - 9(x + 2) &= 0 \\
(x - 9)(x + 2) &= 0
\end{aligned}
$$

Applying the zero product rule, we have

$$
x-9=0 \qquad\text{or}\qquad x+2=0
$$

which in turn gives

$$
x=9 \qquad\text{or}\qquad x=-2
$$

Therefore, the solutions are $x=-2,9$.

### example 17592186063982 — Solving by Factoring When the Right-Hand Side is Not Zero

Solve $-x^2-5x-14=5x-5$.

First, we bring all terms to the left side:

$$
\begin{aligned}
-x^{2} - 5x - 14 &= 5x - 5 \\
- x^{2} - 5x - 14 - 5x + 5 &= 0 \\
- x^{2} + (-5x - 5x) + (-14 + 5) &= 0 \\
- x^{2} - 10x - 9 &= 0
\end{aligned}
$$

Now, we multiply by $-1$ so that the leading coefficient becomes positive.

$$
\begin{aligned}
-x^{2} - 10x - 9 &= 0 \\
(-1)(-x^{2} - 10x - 9) &= (-1) \cdot (0) \\
x^{2} + 10x + 9 &= 0
\end{aligned}
$$

To factor the equation, we need two numbers that multiply to $9$ and add to $10$. These two numbers are $1$ and $9$, so we can factor the left-hand side as follows:

$$
\begin{aligned}
x^{2} + 10x + 9 &= 0 \\
x^{2} + (1x + 9x) + 9 &= 0 \\
(x^{2} + x) + (9x + 9) &= 0 \\
x(x + 1) + 9(x + 1) &= 0 \\
(x + 9)(x + 1) &= 0
\end{aligned}
$$

Applying the zero product rule, we have

$$
x+9=0 \qquad\text{or}\qquad x+1=0
$$

which in turn gives

$$
x=-9 \qquad\text{or}\qquad x=-1
$$

Therefore, the solutions are $x=-9,-1$.

## Representative practice (first three per skill; full bank in practice.json)

### Solving by Factoring When the Leading Coefficient is Positive (2 captured questions)

Question 17592186064627 — None

Solve the equation $x^{2} - 5x + 4 = 0$.

Solution: Move every term to the left, combine like terms, and factor:

$$
x^{2} - 5 x + 4=1 \left(x - 1\right) \left(x - 4\right)=0.
$$

The zero-product rule gives

$$
x = 1, 4.
$$

Substitution in the original equation confirms each listed root.

Answer selection: x = 1, 4

Question 17592186064961 — None

Solve $q^{2} + 10q + 21 = 0$.

Solution: Move every term to the left, combine like terms, and factor:

$$
q^{2} + 10 q + 21=1 \left(q + 3\right) \left(q + 7\right)=0.
$$

The zero-product rule gives

$$
q =-7,-3.
$$

Substitution in the original equation confirms each listed root.

Answer selection: q =-7,-3

### Solving by Factoring When the Leading Coefficient is Negative (2 captured questions)

Question 17592186064632 — None

Solve the equation $-z^{2} + 8z - 15 = 0$.

Solution: Move every term to the left, combine like terms, and factor:

$$
- z^{2} + 8 z - 15=- \left(z - 5\right) \left(z - 3\right)=0.
$$

The zero-product rule gives

$$
z = 3, 5.
$$

Substitution in the original equation confirms each listed root.

Answer selection: z = 3, 5

Question 17592186064633 — None

Solve the equation $-x^{2} - 4x + 5 = 0$.

Solution: Move every term to the left, combine like terms, and factor:

$$
- x^{2} - 4 x + 5=- \left(x - 1\right) \left(x + 5\right)=0.
$$

The zero-product rule gives

$$
x =-5, 1.
$$

Substitution in the original equation confirms each listed root.

Answer selection: x =-5, 1

### Solving by Factoring When the Right-Hand Side is Not Zero (17 captured questions)

Question 17592186064628 — None

Solve $-z^{2} + z =-2z^{2} - 4z + 14$.

Solution: Move every term to the left, combine like terms, and factor:

$$
z^{2} + 5 z - 14=1 \left(z + 7\right) \left(z - 2\right)=0.
$$

The zero-product rule gives

$$
z =-7, 2.
$$

Substitution in the original equation confirms each listed root.

Answer selection: z =-7, 2

Question 17592186064783 — None

Solve $y^{2} - 7y + 14 = 4y - 16$.

Solution: Move every term to the left, combine like terms, and factor:

$$
y^{2} - 11 y + 30=1 \left(y - 5\right) \left(y - 6\right)=0.
$$

The zero-product rule gives

$$
y = 5, 6.
$$

Substitution in the original equation confirms each listed root.

Answer selection: y = 5, 6

Question 17592186678563 — question.difficulty/moderate

Solve $-z^{2} - 3z + 15 = -2z^{2} + 4z + 9$.

Solution: First, bring all terms to the left side and collect like terms.

$$
\begin{aligned}
-z^{2} - 3z + 15 &= -2z^{2} + 4z + 9 \\
(-z^{2} - 3z + 15) - (-2z^{2} + 4z + 9) &= 0 \\
z^{2} - 7z + 6 &= 0
\end{aligned}
$$

To factor, find two numbers that multiply to $6$ and add to $-7$. They are $-1$ and $-6$. Split the linear term and factor by grouping.

$$
\begin{aligned}
z^{2} - 7z + 6 &= 0 \\
z^{2} + (-1)z + (-6)z + (6) &= 0 \\
(z^{2} + (-1)z) + ((-6)z + (6)) &= 0 \\
z(z - 1) + (-6)(z - 1) &= 0 \\
(z - 1)(z - 6) &= 0
\end{aligned}
$$

Applying the zero product rule gives

$$
\begin{aligned}
z - 1 &= 0 \qquad\text{or}\qquad z - 6 = 0 \\
z &= 1 \qquad\text{or}\qquad z = 6
\end{aligned}
$$

Therefore, the solutions are $z = 1, 6$.

Answer selection: z = 1, 6
