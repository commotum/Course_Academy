# 17592186049832 Solving Quadratic Equations with Leading Coefficients by Factoring

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186111830 — Introduction

Suppose that we want to solve the quadratic equation

$$
2x^2-3x+1=0
$$

To do this, we need to factor the trinomial on the left-hand side. We'll need to find two numbers such that

- their product is equal to the product of the quadratic coefficient and the constant (which is $2 \times 1 = 2$), and
- their sum is equal to the linear coefficient (which is $-3$).

These two numbers are $-1$ and $-2$. So, we can factor the left-hand side as follows:

$$
\begin{aligned}
2x^{2} - 3x + 1 &= 0 \\
2x^{2}\underbrace{-1x - 2x}_{-3x} + 1 &= 0 \\
(2x^{2} - x) + (-2x + 1) &= 0 \\
x(2x - 1) - 1(2x - 1) &= 0 \\
(x - 1)(2x - 1) &= 0
\end{aligned}
$$

Applying the zero product rule, we have

$$
x-1=0 \qquad\text{or}\qquad 2x-1=0
$$

which in turn gives

$$
x=1 \qquad\text{or}\qquad x=\dfrac{1}{2}
$$

Therefore, the solutions are

$$
x=\dfrac{1}{2},1
$$



### example 17592186110329 — Solving When the Terms Have No Common Factor

Solve the equation $-2x^2 +9x -4=0$.

First, we multiply by $-1$ so that the leading coefficient becomes positive.

$$
\begin{aligned}
-2x^{2} + 9x - 4 &= 0 \\
(-1) \cdot (-2x^{2} + 9x - 4) &= (-1) \cdot 0 \\
2x^{2} - 9x + 4 &= 0
\end{aligned}
$$

To factor the left-hand side, we need two numbers that multiply to

$$
2 \cdot 4 = 8
$$

and add to $-9$. These two numbers are $-1$ and $-8$, so we can factor the left-hand side as follows:

$$
\begin{aligned} 2x^2 -9x +4 &=0 \\ 2x^2 -1x - 8x +4 &=0 \\ (2x^2 -1x) + (-8x +4) &= 0 \\ x(2x-1) -4(2x-1) &= 0 \\ (2x-1)(x-4) &=0 \end{aligned}
$$

Applying the zero product rule, we have

$$
2x-1=0 \qquad\text{or}\qquad x-4=0
$$

which in turn gives

$$
x=\dfrac{1}{2} \qquad\text{or}\qquad x=4
$$

Therefore, the solutions are

$$
x=\dfrac{1}{2},4
$$

### example 17592186110330 — Solving When the Terms Have a Common Factor

Solve the equation $45x^2 +24 x -36 =0$.

First, notice that $45$, $24$ and $36$ have a common factor of $3$. So, we can divide by $3$ to simplify our equation:

$$
\begin{aligned}
\frac{45x^{2} + 24x - 36}{3} &= \frac{0}{3} \\
\frac{45}{3}x^{2} + \frac{24}{3}x - \frac{36}{3} &= \frac{0}{3} \\
15x^{2} + 8x - 12 &= 0
\end{aligned}
$$

To factor the left-hand side, we need two numbers that multiply to

$$
15 \cdot (-12)=-180
$$

and sum to $8$. These two numbers are $-10$ and $18$, so we can factor the left-hand side as follows:

$$
\begin{aligned} 15x^2 +8 x -12 &=0 \\ 15x^2 -10x +18 x -12 &=0 \\ (15x^2 -10x) + (18 x -12) &= 0 \\ 5x(3x-2) + 6(3x-2) &= 0 \\ (5x+6)(3x-2) &=0 \end{aligned}
$$

Applying the zero product rule, we have

$$
5x+6=0 \qquad\text{or}\qquad 3x-2=0
$$

which in turn gives

$$
x=-\dfrac{6}{5} \qquad\text{or}\qquad x=\dfrac{2}{3}
$$

Therefore, the solutions are

$$
x=-\dfrac{6}{5}, \dfrac{2}{3}
$$

### example 17592186110333 — Solving When the Right-Hand Side is Not Zero

Solve the equation $7x^2-x+1=6x-3x^2$.

First, we bring all terms to the left-hand side:

$$
\begin{aligned} 7x^2-x+1&=6x-3x^2 \\ 7x^2-x+1 -6x+3x^2&=0 \\ (7x^2+3x^2) + (-x-6x) +1 &=0 \\ 10x^2-7x+1 &=0 \end{aligned}
$$

To factor the left-hand side, we need two numbers that multiply to

$$
10 \cdot 1=10
$$

and sum to $-7$. These two numbers are $-2$ and $-5$, so we can factor the left-hand side as follows:

$$
\begin{aligned} 10x^2-7x+1 &= 0 \\ 10x^2-2x-5x+1 &= 0 \\ (10x^2-2x) + (-5x +1) &= 0 \\ 2x(5x -1) - (5x -1) &= 0 \\ (2x-1)(5x-1)&=0 \end{aligned}
$$

Applying the zero product rule, we have

$$
2x-1=0 \qquad\text{or}\qquad 5x-1=0
$$

which in turn gives

$$
x=\dfrac{1}{2} \qquad\text{or}\qquad x=\dfrac{1}{5}
$$

Therefore, the solutions are

$$
x=\dfrac{1}{2},\dfrac{1}{5}
$$

## Representative practice (first three per skill; full bank in practice.json)

### Solving When the Terms Have No Common Factor (2 captured questions)

Question 17592186110991 — None

Solve the equation $5x^{2} + 3x - 2 = 0$.

Solution: 

Question 17592186111400 — None

Solve the equation $2x^{2} + 3x + 1 = 0$.

Solution: 

### Solving When the Terms Have a Common Factor (22 captured questions)

Question 17592186111326 — None

Solve the equation $8y^{2} - 20y + 8 = 0$.

Solution: 

Question 17592186111401 — None

Solve the equation $2z^{2} + 10z + 8 = 0$.

Solution: 

Question 17592186758185 — question.difficulty/moderate

Solve the equation $20z^{2} - 48z + 16 = 0$.

Solution: First, the coefficients have a greatest common factor of $4$. Divide both sides by $4$:

$$
\begin{aligned}
\frac{20z^{2} - 48z + 16}{4} &= \frac{0}{4} \\5z^{2} - 12z + 4 &= 0
\end{aligned}
$$

To factor the left-hand side, find two numbers whose product is $5\cdot (4) = 20$ and whose sum is $-12$. These numbers are $-2$ and $-10$. Split the middle term and group:

$$
\begin{aligned}
5z^{2} - 12z + 4 &= 0 \\5z^{2} - 2z - 10z + 4 &= 0 \\(5z^{2} - 2z) + (-10z + 4) &= 0 \\z(5z - 2) - 2(5z - 2) &= 0 \\(z - 2)(5z - 2) &= 0
\end{aligned}
$$

Applying the zero product rule gives

$$
z - 2=0\qquad\text{or}\qquad 5z - 2=0
$$

Solve each linear equation:

$$
\begin{aligned}
z &= \frac{2}{1} = 2 \\z &= \frac{2}{5} = \frac{2}{5}
\end{aligned}
$$

Therefore, the solutions are

$$
z = \frac{2}{5}, 2
$$

Answer selection: z = \frac{2}{5}, 2

### Solving When the Right-Hand Side is Not Zero (17 captured questions)

Question 17592186110992 — None

Solve the equation $5u - 9 =-2u^{2} + 8u$.

Solution: 

Question 17592186111132 — None

Solve the equation $5y = 3 - 2y^{2}$.

Solution: 

Question 17592186677881 — question.difficulty/moderate

Solve the equation $-7u+3=-6u^2+4u$.

Solution: First, bring all terms to the left-hand side and collect like terms:

$$
\begin{aligned}
-7u+3&=-6u^2+4u \\
-7u+3-(-6u^2+4u)&=0 \\
6u^2-11u+3&=0
\end{aligned}
$$

To factor, find two numbers whose product is $6\cdot(3)=18$ and whose sum is $-11$. These are $-9$ and $-2$. Split the middle term and group:

$$
\begin{aligned}
6u^2-11u+3&=0 \\
6u^2-9u-2u+3&=0 \\
(6u^2-9u)+(-2u+3)&=0 \\
3u(2u-3)-(2u-3)&=0 \\
(3u-1)(2u-3)&=0
\end{aligned}
$$

Applying the zero-product rule gives

$$
3u-1=0\qquad\text{or}\qquad 2u-3=0
$$

Solve the two linear equations:

$$
\begin{aligned}
3u&=1\qquad\text{or}\qquad 2u=3 \\
u&=\frac{1}{3}\qquad\text{or}\qquad u=\frac{3}{2} \\
u&=\frac{1}{3}\qquad\text{or}\qquad u=\frac{3}{2}
\end{aligned}
$$

Therefore, the solutions are

$$
u=\frac{1}{3}, \frac{3}{2}
$$

Answer selection: \frac{1}{3}, \frac{3}{2}
