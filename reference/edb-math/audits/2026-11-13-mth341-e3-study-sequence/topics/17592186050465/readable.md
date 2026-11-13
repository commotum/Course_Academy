# 17592186050465 The Quadratic Formula

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186069948 — Introduction

The **quadratic formula** is a formula that we can use to compute the solution of a quadratic equation.

Given a quadratic equation in standard form

$$
ax^2 + bx + c = 0
$$

the formula for the solutions to this equation is

$$
x = \dfrac{-b \pm \sqrt{b^2 - 4ac}}{2a}
$$

The quadratic formula is derived using a method called *completing the square*. You'll learn more about this method and how it's used to derive the quadratic formula in future lessons.

To see how applying the quadratic formula works in practice, let's consider the equation

$$
x^2-2x-15=0
$$

The coefficients of this quadratic equation are

$$
{\color{blue}a=1}, \qquad {\color{red}b=-2}, \qquad {\color{purple}c=-15}
$$

To compute the solution, we substitute the above values into the quadratic formula:

$$
\begin{aligned}
x &= \frac{-b ± \sqrt{b^{2} - 4ac}}{2a} \\
&= (- (-2) ± \sqrt{(-2)^{2} - 4(1)(-15)})/(2(1)) \\
&= \frac{2 ± \sqrt{64}}{2} \\
&= \frac{2 ± 8}{2} \\
&= 1 ± 4
\end{aligned}
$$

Finally, we simplify the two solutions:

$$
\begin{aligned}
x &= 1 + 4 = 5 \\
x &= 1 - 4 =-3
\end{aligned}
$$

Therefore, the solutions to our quadratic equation are $x=-3$ and $x=5$.



### example 17592186068637 — Applying the Quadratic Formula Using a Framework

Solving the equation $25x^{2}-20x+4= 0$ using the quadratic formula leads to the expression below:
$$
\displaystyle x = \dfrac{20 \pm \sqrt{(-20)^2-4\cdot  25 \cdot  \boxed{ {\phantom{00}}}}} {2 \cdot 25}
$$
What number is missing from the formula, and what is the solution of the equation?

The coefficients of our quadratic equation are

$$
a=25, \quad b=-20, \quad c=4
$$

So, we substitute these values into the quadratic formula:

$$
\begin{aligned}
x &= \frac{-b ± \sqrt{b^{2} - 4ac}}{2a} \\
&= (- (-20) ± \sqrt{(-20)^{2} - 4 \cdot 25 \cdot (4)})/(2 \cdot 25) \\
&= \frac{20 ± \sqrt{20^{2} - 4 \cdot 25 \cdot \color{blue}\,4\,}}{2 \cdot 25}
\end{aligned}
$$

So, the missing number is $\boxed{ { {\color{blue}\hspace{0.167em} 4 \hspace{0.167em}}}}.$

Now, to find the solution, we simplify the above:

$$
\begin{aligned}
\frac{20 ± \sqrt{20^{2} - 4 \cdot 25 \cdot \color{blue}\,4\,}}{2 \cdot 25} &= \frac{20 ± \sqrt{400 - 400}}{50} \\
&= \frac{20 ± \sqrt{0}}{50} \\
&= \frac{20 ± 0}{50} \\
&= \frac{20}{50} \\
&= \frac{2}{5}
\end{aligned}
$$

Therefore, the solution is

$$
x= \dfrac{2}{5}
$$

### example 17592186068500 — Using the Quadratic Formula to Solve a Quadratic Equation

Solve for $x$ where $2x^2 - 3x - 5 = 0$.

The coefficients of our quadratic equation are

$$
a = 2, \quad b = -3, \quad c = -5
$$

So, we substitute these values into the quadratic formula:

$$
\begin{aligned} x &= \dfrac{-b \pm \sqrt{b^2 - 4ac}}{2a} \\[5pt] &= \dfrac{-(-3) \pm \sqrt{(-3)^2 - 4(2)(-5)}}{2(2)} \\[5pt] &= \dfrac{3 \pm \sqrt{49}}{4} \\[5pt] &= \dfrac{3 \pm 7}{4} \end{aligned}
$$

Finally, we simplify the two solutions:

$$
\begin{aligned}
x &= \frac{3 + 7}{4} = \frac{10}{4} = \frac{5}{2} \\
x &= \frac{3 - 7}{4} =-1
\end{aligned}
$$

Therefore, the solutions are $x=-1$ and

$$
x=\dfrac{5}{2}
$$

### example 17592186068501 — Simplifying and Solving a Quadratic Equation

Solve the equation $x^2 + 2x = 6$.

The first step is to put the equation into standard form:

$$
\begin{aligned}
x^{2} + 2x &= 6 \\
x^{2} + 2x - 6 &= 0
\end{aligned}
$$

The coefficients of our quadratic equation are

$$
a = 1, \quad b = 2, \quad c = -6
$$

Now, we substitute these values into the quadratic formula:

$$
\begin{aligned} x &= \dfrac{-b \pm \sqrt{b^2 - 4ac}}{2a} \\[5pt] &= \dfrac{-(2) \pm \sqrt{(2)^2 - 4(1)(-6)}}{2(1)} \\[5pt] &= \dfrac{-2 \pm \sqrt{28}}{2} \\[5pt] &= \dfrac{-2 \pm 2\sqrt{7}}{2} \\[5pt] &= -1 \pm \sqrt{7} \end{aligned}
$$

Therefore, the solutions are

$$
x = -1 + \sqrt{7}
$$

and

$$
x = -1 - \sqrt{7}
$$

### example 17592186068502 — Applying the Quadratic Formula To an Equation With No Real Solutions

What are the solutions to $3x^2 = x - 10$?

The first step is to put the equation into standard form. This gives

$$
\begin{aligned}
3x^{2} - x + 10 &= 0
\end{aligned}
$$

The coefficients are

$$
a = 3, \quad b = -1, \quad c = 10
$$

Now, we substitute these values into the quadratic formula:

$$
\begin{aligned}
x &= \frac{-b ± \sqrt{b^{2} - 4ac}}{2a} \\
&= (- (-1) ± \sqrt{(-1)^{2} - 4(3)(10)})/(2(3)) \\
&= \frac{1 ± \sqrt{1 - 120}}{6} \\
&= \frac{1 ± \sqrt{-119}}{6}
\end{aligned}
$$

From here, we can see that the equation has no real solutions because $\sqrt{-119}$ is not a real number.

## Representative practice (first three per skill; full bank in practice.json)

### Applying the Quadratic Formula Using a Framework (17 captured questions)

Question 17592186069468 — None

Solving the equation $9x^{2} + 6x + 1 = 0$ using the quadratic formula leads to the expression below:
$$
\displaystyle x = {\displaystyle \frac{- 6 \pm  \sqrt{\hspace{0.167em} \boxed{\phantom{00}}}}{2 \cdot  9}}
$$
What number is missing from the formula, and what is the solution of the equation?

Solution: 

Question 17592186069469 — None

Solving the equation $4y^{2} + 4y + 1 = 0$ using the quadratic formula leads to the expression below:
$$
\displaystyle y = {\displaystyle \frac{- \boxed{\phantom{00}} \pm  \sqrt{ {4}^{2} - 4 \cdot  4 \cdot  1}}{2 \cdot  4}}
$$
What number is missing from the formula, and what is the solution of the equation?

Solution: 

Question 17592186678521 — question.difficulty/moderate

Solving the equation $36x^2-24x+4=0$ using the quadratic formula leads to the expression below:

$$
x=\frac{24\pm\sqrt{(-24)^2-4\cdot 36\cdot \boxed{?}}}{2\cdot 36}
$$

What number is missing from the formula, and what is the solution of the equation?

Solution: The coefficients of our quadratic equation are $a=36$, $b=-24$, and $c=4$.

Substitute these values into the **quadratic formula**:

$$
\begin{aligned}
x&=\frac{-b\pm\sqrt{b^2-4ac}}{2a} \\
&=\frac{-(-24)\pm\sqrt{(-24)^2-4\cdot 36\cdot (4)}}{2\cdot 36} \\
&=\frac{24\pm\sqrt{576-576}}{72} \\
&=\frac{24\pm\sqrt{0}}{72} \\
&=\frac{24\pm 0}{72}
\end{aligned}
$$

The missing number is $4$.

Both signs give the same value:

$$
\begin{aligned}
x&=\frac{24+0}{72}=\frac{24}{72}=\frac{1}{3}
\end{aligned}
$$

Therefore, the solution is $x=\frac{1}{3}$.

Answer selection: $4$ and $x=\frac{1}{3}$

### Using the Quadratic Formula to Solve a Quadratic Equation (17 captured questions)

Question 17592186069269 — None

Solve for $x$ where $x^{2} - x - 3 = 0$.

Solution: 

Question 17592186069421 — None

Solve for $x$ where $x^{2} + 5x + 5 = 0$.

Solution: 

Question 17592186678489 — question.difficulty/moderate

Solve for $x$ where $x^{2} + 4x - 12 = 0$.

Solution: The coefficients of our quadratic equation are

$$
a = 1,\quad b = 4,\quad c = -12
$$

Substitute these values into the **quadratic formula**:

$$
\begin{aligned}
x &= \frac{-b \pm \sqrt{b^{2}-4ac}}{2a} \\
&= \frac{-(4) \pm \sqrt{(4)^{2}-4(1)(-12)}}{2(1)} \\
&= \frac{-4 \pm \sqrt{64}}{2} \\
&= \frac{-4 \pm 8}{2}
\end{aligned}
$$

Simplify the two solutions:

$$
\begin{aligned}
x &= \frac{-4+8}{2} = 2 \\
x &= \frac{-4-8}{2} = -6
\end{aligned}
$$

Therefore, the solutions are

$$
x = 2\quad\text{or}\quad x = -6
$$

Answer selection: x = 2\quad\text{or}\quad x = -6

### Simplifying and Solving a Quadratic Equation (2 captured questions)

Question 17592186069270 — None

Solve the equation $2x^{2} + 7 = 11x$.

Solution: 

Question 17592186069271 — None

Solve the equation $0.2t^{2} + 0.4 = t$.

Solution: 

### Applying the Quadratic Formula To an Equation With No Real Solutions (2 captured questions)

Question 17592186069043 — None

What are the solutions to $y^{2} - y + 2 = 0$?

Solution: 

Question 17592186069349 — None

What are the solutions to $-2t^{2} + 3t = 2$?

Solution: 
