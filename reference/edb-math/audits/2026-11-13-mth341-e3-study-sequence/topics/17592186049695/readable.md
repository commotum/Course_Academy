# 17592186049695 Solving Quadratic Equations With Complex Roots

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186088886 — Introduction

Suppose that we want to solve the quadratic equation

$$
x^2 -2x +2=0.
$$

This quadratic is written in standard form with $a=1,$ $b=-2,$ and $c=2.$ However, its discriminant is negative:

$$
\begin{aligned}{b}^{2}-4ac & =(-2)^{2}-4(1)(2) \\  & =4-8 \\  & =-4 \\  & <0\end{aligned}
$$

This means that the quadratic equation has no real solutions. However, if we allow complex solutions, we may solve the equation as follows:

$$
\begin{aligned}x & =\frac{-b\pm \sqrt{{b}^{2}-4ac}}{2a} \\  & =\frac{-(-2)\pm \sqrt{(-2)^{2}-4(1)(2)}}{2\cdot 1} \\  & =\frac{2\pm \sqrt{-4}}{2} \\  & =\frac{2\pm 2\text{i}}{2} \\  & =1\pm \text{i}\end{aligned}
$$

Therefore, the equation $x^2 -2x +2=0$ has two solutions, $x=1+\textrm{i}$ and $x=1-\textrm{i}.$



### example 17592186087498 — Solving a Quadratic Equation With Complex Roots Using the Quadratic Formula

Solve the equation $\, x^2-4x+5=0.$

We can find the roots of a quadratic equation using the quadratic formula:

$$
x = \frac{-b\pm\sqrt{b^2-4ac}}{2a}
$$

In this case, the coefficients are $a=1, b=-4,$ and $c=5.$ Substituting these values into the quadratic formula, we get

$$
\begin{aligned}x & =\frac{-(-4)\pm \sqrt{(-4)^{2}-4(1)(5)}}{2(1)} \\  & =\frac{4\pm \sqrt{16-20}}{2} \\  & =\frac{4\pm \sqrt{-4}}{2} \\  & =\frac{4\pm 2\,\text{i}}{2} \\  & =2\pm \text{i}.\end{aligned}
$$

Therefore, the equation has two solutions, $x=2+\textrm{i}$ and $x=2-\textrm{i}.$

### example 17592186087632 — Rearranging and Solving a Quadratic Equation With Complex Roots

Find the solutions of the equation $4x^2= 4x-13 .$

First, we write the equation in standard form by bringing all of the terms to the left-hand side. This gives the equation

$$
4x^2 - 4x + 13=0.
$$

We can find the roots of a quadratic equation using the quadratic formula:

$$
x = \frac{-b\pm\sqrt{b^2-4ac}}{2a}
$$

In this case, the coefficients are  $a=4, b=-4,$ and $c=13.$ Substituting these values into the quadratic formula, we get

$$
\begin{aligned}x & =\frac{-(-4)\pm \sqrt{(-4)^{2}-4(4)(13)}}{2(4)} \\  & =\frac{4\pm \sqrt{16-208}}{8} \\  & =\frac{4\pm \sqrt{-192}}{8} \\  & =\frac{4\pm 8\sqrt{-3}}{8} \\  & =\frac{4\pm 8\sqrt{3}\,\text{i}}{8} \\  & =\frac{1}{2}\pm \sqrt{3}\,\text{i}\end{aligned}
$$

Therefore, the equation has two solutions, $x=\dfrac{1}{2}+ \sqrt{3} \, \textrm{i}$ and $x=\dfrac{1}{2}- \sqrt{3} \, \textrm{i}.$

### tutorial 17592186088887 — Solving a Quadratic Equation With Complex Roots by Completing the Square

We can also solve a quadratic equation with complex solutions using the square root method.

To demonstrate, let's find the solutions of the equation $(x-2)^2=-16.$

The left-hand side is a perfect square. Therefore, we can solve the equation as follows:

$$
\begin{aligned}(x-2)^{2} & =-16 \\ x-2 & =\pm \sqrt{-16} \\ x-2 & =\pm 4\text{i} \\ x & =2\pm 4\text{i}\end{aligned}
$$

Sometimes, we need to complete the square first before applying the square root method. Let's see how.



### example 17592186087499 — Solving a Quadratic Equation With Complex Roots by Completing the Square

The equation $x^2+8x+80=0$ can be written in the form $(x+p)^2=q.$ Find $p+q,$ and solve the equation.

We first move the constant to the right-hand side:

$$
\begin{aligned}{x}^{2}+8x+80 & =0 \\ {x}^{2}+8x & =-80\end{aligned}
$$

Next, we complete the square on the left-hand side:

$$
\begin{aligned}{x}^{2}+8x & =-80 \\ {x}^{2}+2\cdot 4x+{4}^{2}-{4}^{2} & =-80 \\ (x+4)^{2}-16 & =-80 \\ (x+4)^{2} & =-64\end{aligned}
$$

Therefore, $p=4,$ $q=-64,$ and $p+q = -60.$

Finally, we solve the equation using the square root method:

$$
\begin{aligned}(x+4)^{2} & =-64 \\ x+4 & =\pm \sqrt{-64} \\ x+4 & =\pm 8\,\text{i} \\ x & =-4\pm 8\,\text{i}\end{aligned}
$$

Therefore, the equation has two solutions, $x=-4+8\,\textrm{i}$ and $x=-4-8\,\textrm{i}.$

## Representative practice (first three per skill; full bank in practice.json)

### Solving a Quadratic Equation With Complex Roots Using the Quadratic Formula (8 captured questions)

Question 17592186088048 — None

Solve the equation $4x^{2} + 16x + 18 = 0$.

Solution: 

Question 17592186088076 — None

Solve the equation $x^{2} - 6x + 13 = 0$.$x =$
{{field-1}}
$±$
{{field-2}} $\textrm{i}$

Solution: 

Question 17592186088077 — None

Solve the equation $-x^{2} + 6x - 25 = 0$.$x =$
{{field-1}}
$±$
{{field-2}} $\textrm{i}$

Solution: 

### Rearranging and Solving a Quadratic Equation With Complex Roots (10 captured questions)

Question 17592186088078 — question.difficulty/easy

Solve the equation ${x}^{2}-2x=-50.$

$x=$
{{field-1}}
$\pm $
{{field-2}}$\text{i}$

Solution: First, we write the equation in standard form by bringing all of the terms to the left-hand side. This gives the equation

$$
{x}^{2}-2x+50=0.
$$

We can find the roots of a quadratic equation using the quadratic formula:

$$
x=\frac{-b\pm \sqrt{{b}^{2}-4ac}}{2a}
$$

In this case, the coefficients are $a=1,\,b=-2,$ and $c=50.$ Substituting these values into the quadratic formula, we get

$$
\begin{aligned}x & =\frac{-(-2)\pm \sqrt{(-2)^{2}-4(1)(50)}}{2(1)} \\  & =\frac{2\pm \sqrt{4-200}}{2} \\  & =\frac{2\pm \sqrt{-196}}{2} \\  & =\frac{2\pm 14\,\text{i}}{2} \\  & =1\pm 7\,\text{i}.\end{aligned}
$$

Therefore, the equation has two solutions, $x=1+7\,\text{i}$ and $x=1-7\,\text{i}.$

Answer field-1: 1

Answer field-2: 7

Question 17592186088251 — None

Solve the equation $4 = 6x - 3x^{2}$.

Solution: 

Question 17592186233675 — question.difficulty/easy

Solve the equation $x(x+30)=-116+10x.$

$x=$
{{field-1}}
$\pm $
{{field-2}}$\text{i}$

Solution: First, we write the equation in standard form by bringing all of the terms to the left-hand side. This gives the equation

$$
\begin{aligned}x(x+30) & =-116+10x \\ {x}^{2}+30x+116-10x & =0 \\ {x}^{2}+20x+116 & =0.\end{aligned}
$$

We can find the roots of a quadratic equation using the quadratic formula:

$$
x=\frac{-b\pm \sqrt{{b}^{2}-4ac}}{2a}
$$

In this case, the coefficients are $a=1,\,b=20,$ and $c=116.$ Substituting these values into the quadratic formula, we get

$$
\begin{aligned}x & =\frac{-20\pm \sqrt{(20)^{2}-4(1)(116)}}{2(1)} \\  & =\frac{-20\pm \sqrt{400-464}}{2} \\  & =\frac{-20\pm \sqrt{-64}}{2} \\  & =\frac{-20\pm 8\,\text{i}}{2} \\  & =-10\pm 4\,\text{i}.\end{aligned}
$$

Therefore, the equation has two solutions, $x=-10+4\,\text{i}$ and $x=-10-4\,\text{i}.$

Answer field-1: -10

Answer field-2: 4

### Solving a Quadratic Equation With Complex Roots by Completing the Square (18 captured questions)

Question 17592186088079 — None

Solve the equation $(x + 4)^{2} =-100$.$x =$
{{field-1}}
$±$
{{field-2}} $\textrm{i}$

Solution: 

Question 17592186088250 — question.difficulty/moderate

The equation ${x}^{2}-8x+52=0$ can be written in the form $(x+p)^{2}=q.$ Find $p+q,$ and solve the equation.

Solution: We first move the constant to the right-hand side:

$$
\begin{aligned}{x}^{2}-8x+52 & =0 \\ {x}^{2}-8x & =-52\end{aligned}
$$

Next, we complete the square on the left-hand side:

$$
\begin{aligned}{x}^{2}-8x & =-52 \\ {x}^{2}-2\cdot 4x+{4}^{2}-{4}^{2} & =-52 \\ (x-4)^{2}-16 & =-52 \\ (x-4)^{2} & =-36\end{aligned}
$$

Therefore, $p=-4,\,q=-36,$ and $p+q=-40.$

Finally, we solve the equation using the square root method:

$$
\begin{aligned}(x-4)^{2} & =-36 \\ x-4 & =\pm \sqrt{-36} \\ x-4 & =\pm 6\,\text{i} \\ x & =4\pm 6\,\text{i}\end{aligned}
$$

Therefore, the equation has two solutions, $x=4+6\,\text{i}$ and $x=4-6\,\text{i}.$

Answer selection: p+q=-40,\,x=4\pm 6\,\text{i}

Question 17592186088258 — question.difficulty/easy

What are the solutions of the equation $(x - 2)^{2} =-36$?

Solution: 
