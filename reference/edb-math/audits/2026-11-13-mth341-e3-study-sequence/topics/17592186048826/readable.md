# 17592186048826 Solving Systems of Equations by Substitution

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186075033 — Introduction

Suppose that we want to solve, *without* using graphs, the following system of linear equations:

$$\begin{cases}{\color{blue}x+y=4} \\ {\color{red}x-2=y}\hspace{0.167em}\end{cases}.$$

In order to solve the system without a graph, we will need to combine the equations into a single equation that can be solved using algebraic manipulation.

One way to combine the equations is called the **substitution method.** To use the substitution method, we substitute for one variable in terms of the other.

For instance, notice that we can make $y$ the subject of the second equation:

$$
\color{red}y=x - 2
$$

Substituting this expression for $y$ into the first equation, we get an equation that we can solve for $x\mathbin{:}$

$$\begin{aligned}{\color{blue}x+y} & ={\color{blue}4} \\ {\color{blue}x}+{\color{red}(x-2)} & ={\color{blue}4} \\ 2x-2 & =4 \\ 2x & =6 \\ x & =3\end{aligned}$$

So, the solution must have $x=3.$ But we also need to figure out what $y$ is. We can do this by substituting $x=3$ back into the second equation:

$$\begin{aligned}{\color{red}y} & ={\color{red}x-2} \\ y & =3-2 \\ y & =1\end{aligned}$$

Therefore, the solution to the system of equations is $x = 3$ and $y = 1$, which can be written as $\left(3, 1\right).$

**Note:** Whenever we isolate the variable in one equation, we have to substitute it into the *other* equation. We cannot substitute a variable into the same equation it came from, because this will not give us any more information about the variable.



### example 17592186073445 — Solving a System of Linear Equations Using Substitution

Solve the following system of equations:

$$
\left\{\begin{aligned}x-y &=4 \\ x+2y &=16\end{aligned}\right.
$$

We will isolate a variable in one of the equations and then substitute it into the other equation. It doesn't matter which equation we pick first, so we choose the easiest one. In this case, the first equation looks like the easiest.

Using the first equation, we can isolate $x$ by adding $y$ to both sides of the equation:

$$
\begin{aligned}x-y & =4 \\ x & =4+y\end{aligned}
$$

Then, we replace $x$ with $4+y$ in the second equation and solve for $y\mathbin{:}$

$$
\begin{aligned}
	x+2y &=16 \\
	(4+y) + 2y &=16\\
	4+3y &=16\\
	3y &=12\\
	y &=4
\end{aligned}
$$

If we now substitute $y=4$ into $x=4+y$, then we can find the value of $x\mathbin{:}$

$$
\begin{aligned}
	x &= 4 + y \\
	   &= 4 + (4) \\
	   &=8
\end{aligned}
$$

Therefore, the solution to the system of equations is $x = 8$ and $y = 4$, which can be written as $(8, 4).$

### example 17592186073446 — Solving a Challenging System of Linear Equations Using Substitution

Solve the following system of equations:

$$
\left\{\begin{aligned}2u+9v-6 &=0 \\ 2u+6v-8 &=0\end{aligned}\right.
$$

Sometimes, it's handy to assign a number to each equation in a system, so that we can refer to them more easily:


$$\qquad\:\:\:
\begin{cases}{\color{red}2u+9v-6=0}\hspace{2em}{\color{red}(1)} \\ {\color{blue}2u+6v-8=0}\hspace{2em}{\color{blue}(2)}\end{cases}.$$



We will isolate a variable in one of the equations and then substitute it into the other equation. Using equation $\color{blue}(2)$, we can solve for $u$ as follows:

$$
\begin{aligned}
	2u+6v-8 &= 0 \\
2u+6v &= 8 \\
2u &= 8 - 6v \\
u &= \dfrac{8-6v}{2} \\
u &= 4 - 3v
\end{aligned}
$$

Then, we substitute $u=4-3v$ into equation $\color{red}(1)$ and solve for $v\mathbin{:}$

$$
\begin{aligned}
	2u+9v-6 &= 0 \\
	2(4-3v)+9v-6 &= 0 \\
	8-6v+9v-6 &= 0 \\
2+3v &= 0 \\
3v &= -2 \\
v &= -\dfrac{2}{3}
\end{aligned}
$$

If we now substitute $v=-\dfrac{2}{3}$ into equation $\color{red}(1)$, then we can find the value of $u\mathbin{:}$

$$
\begin{aligned}
	2u+9v-6 &= 0 \\
	2u+9\left(-\dfrac{2}{3}\right) -6 &= 0 \\
	2u-6-6 &= 0 \\
	2u-12 &= 0 \\
	2u &= 12 \\
	u &= 6
\end{aligned}
$$

Therefore, the solution to the system of equations is $u=6$ and $v=-\dfrac{2}{3}$, which can be written as $\left(6,-\dfrac{2}{3}\right).$

## Representative practice (first three per skill; full bank in practice.json)

### Solving a System of Linear Equations Using Substitution (33 captured questions)

Question 17592186074030 — None

Consider the following system of equations:
$$
\displaystyle \left\{\begin{aligned}x + 5y &=13 \\ y &=x + 5\end{aligned}\right.
$$
Find the solution $(x, y)$ to this system using the method of substitution.

The solution is
$($ {{field-1}} $,$ {{field-2}} $)$

Solution: Substitute $y=x+5$ into the first equation: $$x+5(x+5)=13\implies6x=-12\implies x=-2.$$ Then $y=-2+5=3$. Both original equations hold, so the ordered solution is $(-2,3)$.

Answer field-1: -2

Answer field-2: 3

Question 17592186074172 — None

Given the system of equations below, what is the value of $a - b$?

$$
\displaystyle \left\{\begin{aligned}3a + 2b &=4 \\ - 4a + b &=2\end{aligned}\right.
$$

Solution: The second equation gives $b=2+4a$. Substitute into the first equation: $3a+2(2+4a)=4$, so $11a=0$. Thus $a=0$, $b=2$, and $a-b=-2$.

Answer selection: -2

Question 17592186074185 — question.difficulty/moderate

Given the system of equations below, what is the value of $p-q?$

$$
\left\{\begin{aligned}3p &=15 \\ p+2q &=9.\end{aligned}\right.
$$

Solution: We will isolate a variable in one of the equations and then substitute it into the other equation. It doesn't matter which equation we pick first, so we choose the easiest one. In this case, the first equation looks like the easiest.

Using the first equation, we can isolate $p$ by dividing both sides of the equation by $3:$

$$
\begin{aligned}3p & =15 \\ p & =5\end{aligned}
$$

If we now substitute $p=5$ into $p+2q=9,$ then we can find the value of $q:$

$$
\begin{aligned}p+2q & =9 \\ (5)+2q & =9 \\ 2q & =4 \\ q & =2\end{aligned}
$$

Therefore, the solution to the system of equations is $p=5,\,q=2.$ So,

$$
p-q=5-2=3.
$$

Answer selection: 3

### Solving a Challenging System of Linear Equations Using Substitution (24 captured questions)

Question 17592186073997 — None

Using the method of substitution, find the solution of
$$
\displaystyle \left\{\begin{aligned}-3p + q &=-9 \\ 5p + 4q &=32\end{aligned}\right.
$$.

Solution: The first equation gives $q=3p-9$. Substitute into the second equation: $$5p+4(3p-9)=32\implies17p=68\implies p=4.$$ Hence $q=3(4)-9=3$. Substitution into both original equations gives $-9$ and $32$, as required.

Answer selection: p = 4, q = 3

Question 17592186073998 — None

Using the method of substitution, find the solution of

$$
\displaystyle \left\{\begin{aligned}-7a + 2b &=18 \\ \phantom{-}6a + 6b &=0\end{aligned}\right.
$$

Solution: The second equation gives $b=-a$. Substitute into the first equation: $$-7a+2(-a)=18\implies-9a=18\implies a=-2.$$ Then $b=2$. Indeed, $-7(-2)+2(2)=18$ and $6(-2)+6(2)=0$.

Answer selection: a =-2, b = 2

Question 17592186074047 — None

Given the system of equations below, what is the value of $p - q$?

$$
\displaystyle \left\{\begin{aligned}5q + 55 &=0 \\ 2p + 3q + 3 &=0\end{aligned}\right.
$$

Solution: From $5q+55=0$, we obtain $q=-11$. Substituting into the second equation gives $2p-33+3=0$, so $p=15$. Therefore $p-q=15-(-11)=26$.

Answer selection: 26
