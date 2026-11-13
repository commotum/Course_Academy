# 17592186050105 Elementary Trigonometric Equations Containing Tangent

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186093388 — Introduction

Suppose we want to find all of the solutions to the equation

$$
\tan x = \sqrt{3}, \qquad\text{{0}^{∘}\le x<{360}^{∘}.}
$$

We can immediately calculate a solution, called the **principal value**, as follows:

$$
x = \arctan\left(\sqrt{3}\right) = 60^\circ
$$

Since $60^\circ$ lies inside the required domain, our first solution is $x_1=60^\circ.$

The tangent function has a period of $180^\circ.$ So, to generate more solutions, we add (or subtract) integer multiples of $180^\circ$ to the principal value.

Therefore, our second solution $x_2$ inside the range $0^\circ \leq x < 360^\circ$ can be calculated as

$$
\begin{aligned}{x}_{2} & ={x}_{1}+{180}^{∘} \\  & ={60}^{∘}+{180}^{∘} \\  & ={240}^{∘}.\end{aligned}
$$

We can stop generating solutions here because adding or subtracting further integer multiples of $180^\circ$ to the principal value will give us solutions that lie outside the domain $0^\circ \leq x < 360^\circ.$

So, the solutions are $x=60^\circ, 240^\circ.$



### example 17592186091987 — Solving a Trigonometric Equation Involving Tangent with Special Angles

Find the solutions to the equation $3\tan x + 3\sqrt{3}=0$ for $0^\circ \leq x < 360^\circ.$

First, we rearrange the equation and isolate $\tan x \mathbin{:}$

$$
\begin{aligned}3\operatorname{tan}⁡x+3\sqrt{3} & =0 \\ 3\operatorname{tan}⁡x & =-3\sqrt{3} \\ \operatorname{tan}⁡x & =-\frac{3\sqrt{3}}{3} \\ \operatorname{tan}⁡x & =-\sqrt{3}.\end{aligned}
$$

Next, we find the principal value:

$$
\begin{aligned}x=\operatorname{arctan}⁡(-\sqrt{3})=-{60}^{∘}\end{aligned}
$$

Since $-60^\circ$ lies outside the given domain, it is not a solution. However, to generate more solutions, we add integer multiples of $180^\circ$ as follows:

$$
\begin{aligned}{x}_{1} & =x+{180}^{∘}=-{60}^{∘}+{180}^{∘}={120}^{∘}\end{aligned}
$$

$$
\begin{aligned}{x}_{2} & =x+{360}^{∘}=-{60}^{∘}+{360}^{∘}={300}^{∘}\end{aligned}
$$

So, the solutions are $x=120^\circ, 300^\circ.$

### example 17592186091986 — Solving a Trigonometric Equation Involving Tangent with Non-Special Angles

Calculate, in degrees to the nearest integer, the solutions to the equation $\tan x=4$ for $0 \leq x <       360^\circ.$

First, we find the principal value:

$$
\begin{aligned}x=\operatorname{arctan}⁡(4)=75.963\,75..{.}^{∘}≈{75.964}^{∘}\end{aligned}
$$

Since $75.964^\circ$ lies inside the given domain, our first solution is $x_1 = 75.964^\circ.$

To generate more solutions, we add integer multiples of $180^\circ$ as follows:

$$
x_2 = 180^\circ + 75.964^\circ \approx 255.964^\circ
$$

So, the solutions (rounded to the nearest integer) are $x=76^\circ, 256^\circ.$

### tutorial 17592186093389 — Solving a Trigonometric Equation Involving Tangent Under a Modified Domain

Suppose we want to find all of the solutions to the equation

$$
\tan x = 1, \qquad\text{-{180}^{∘}<x\le {180}^{∘}.}
$$

Notice that this time, we are looking for solutions in the domain $-180^\circ < x \leq 180^\circ.$

First, we find the principal value:

$$
\begin{aligned}x=\operatorname{arctan}(1)={45}^{∘}\end{aligned}
$$

Since $45^\circ$ lies inside the given domain, our first solution is $x_1 =45^\circ.$

To generate more solutions, we subtract integer multiples of $180^\circ,$ as follows:

$$
\begin{aligned}{x}_{2} & ={x}_{1}-{180}^{∘} \\  & ={45}^{∘}-{180}^{∘} \\  & =-{135}^{∘}\end{aligned}
$$

So, the solutions are $x=-135^\circ, 45^\circ.$



### example 17592186091988 — Solving a Trigonometric Equation Involving Tangent Under a Modified Domain

Solve the equation $3 \tan x - \sqrt{3} = 0$ for $-180^\circ < x \leq 180^\circ.$

First, we rearrange the equation, isolating $\tan x \mathbin{:}$

$$
\begin{aligned}3\operatorname{tan}⁡x-\sqrt{3} & =0 \\ 3\operatorname{tan}⁡x & =\sqrt{3} \\ \operatorname{tan}⁡x & =\frac{\sqrt{3}}{3}\end{aligned}
$$

Now, we find the principal value:

$$
\begin{aligned}x=\operatorname{arctan}⁡\left(\frac{\sqrt{3}}{3}\right)={30}^{∘}\end{aligned}
$$

Since $30^\circ$ lies inside the given domain, our first solution is $x_1 =30^\circ.$

To generate more solutions, we subtract integer multiples of $180^\circ$ as follows:

$$
\begin{aligned}{x}_{2} & ={x}_{1}-{180}^{∘} \\  & ={30}^{∘}-{180}^{∘} \\  & =-{150}^{∘}\end{aligned}
$$

So, the solutions are $x=-150^\circ, 30^\circ.$

### example 17592186091989 — Finding the Points of Intersection of a Horizontal Line and a Tangent Curve

The graph below shows a section of the curve $y=\tan{x}$ on the interval $$
\displaystyle -\dfrac \pi 2 <     x <     \dfrac {\pi} 2
$$ and the line $y=1.$ The line and the curve intersect at the point $A,$ as shown. What is the $x$-coordinate of the point $A?$

![](images/a2/a2ec73bfe4e1cb20debf73264b3a120a1d939552cc803211e0567d63cf6d5fdb.png)

The $y$-values of both functions are the same at the intersection point. Equating the two functions gives

$$
\tan x=1, \qquad -\dfrac \pi 2 <     x <     \dfrac {\pi} 2 .
$$

 First, we find the principal value:

$$
\begin{aligned}x=\operatorname{arctan}⁡(1)=\frac{\pi }{4}\end{aligned}
$$

Since $\dfrac{\pi}{4}$ lies inside the required domain, and there is only one point of intersection, we conclude that the $x$-coordinate of the intersection point $A$ is $x= \dfrac{\pi}{4}.$

## Representative practice (first three per skill; full bank in practice.json)

### Solving a Trigonometric Equation Involving Tangent with Special Angles (7 captured questions)

Question 17592186092622 — None

Given that $x_{1}$ and $x_{2}$ are the solutions of the equation $\sqrt{3}\tan x - \sqrt{3} = 0$ for $0^{∘} \le x < 360^{∘}$, what is the numerical value of $x_{1} \cdot x_{2}$?

> A calculator is required to answer this question.

Solution: 

Question 17592186092876 — None

Given that $x_{1}$ and $x_{2}$ are the solutions of the equation $\tan x = \frac{\sqrt{3}}{3}$ for $0 \le x < 2π$, what is the value of $x_{1} \cdot x_{2}$?

> A calculator is required to answer this question.

Solution: 

Question 17592186256517 — question.difficulty/moderate

Solve the equation $7\operatorname{tan}⁡x+2\sqrt{3}=-5\sqrt{3}$ for $0\le x<2\pi .$

Solution: First, we rearrange the equation and isolate $\operatorname{tan}⁡x:$

$$
\begin{aligned}7\operatorname{tan}⁡x+2\sqrt{3} & =-5\sqrt{3} \\ 7\operatorname{tan}⁡x & =-7\sqrt{3} \\ \operatorname{tan}⁡x & =-\sqrt{3}\end{aligned}
$$

Next, we find the principal value:

$$
\begin{aligned}x=\operatorname{arctan}⁡(-\sqrt{3})=-\frac{\pi }{3}\end{aligned}
$$

Since $-\frac{\pi }{3}$ lies outside the given domain, it is not a solution.

To generate more solutions, we add integer multiples of $\pi .$ Hence,

$$
\begin{aligned}{x}_{1} & =\pi +x=\pi +\left(-\frac{\pi }{3}\right)=\frac{2\pi }{3}, \\ {x}_{2} & =2\pi +x=2\pi +\left(-\frac{\pi }{3}\right)=\frac{5\pi }{3}.\end{aligned}
$$

So, the solutions are $x=\frac{2\pi }{3},\frac{5\pi }{3}.$

Answer selection: x=\frac{2\pi }{3},\frac{5\pi }{3}

### Solving a Trigonometric Equation Involving Tangent with Non-Special Angles (12 captured questions)

Question 17592186092877 — None

Given that $x_{1}$ and $x_{2}$ are the solutions to the equation $\tan x =-2$ for $0 \le x < 2π$, what is the value of $x_{1} \cdot x_{2}$, rounded to the nearest integer?

> A scientific calculator is required to answer this question.

Solution: 

Question 17592186092878 — None

Given that $x_{1}$ and $x_{2}$ are the solutions to the equation $\tan x = \frac{1}{5}$ for $0 \le x < 2π$, what is the value of $x_{1} \cdot x_{2}$, rounded to one decimal place?

> A scientific calculator is required to answer this question.

Solution: 

Question 17592186256518 — question.difficulty/easy

Solve the equation $\operatorname{tan}⁡x=8$ for ${0}^{∘}\le x<{360}^{∘},$ rounded to the nearest integer.

Solution: First, we find the principal value:

$$
\begin{aligned}x=\operatorname{arctan}⁡(8)=82.874\,983{…}^{∘}≈{82.87}^{∘}\end{aligned}
$$

Since ${82.87}^{∘}$ lies inside the given domain, our first solution is ${x}_{1}={82.87}^{∘}.$

To generate more solutions, we add integer multiples of ${180}^{∘}.$ Hence,

$$
\begin{aligned}{x}_{2}={180}^{∘}+{82.87}^{∘}={262.87}^{∘}.\end{aligned}
$$

So, the solutions are

$$
x={83}^{∘},{263}^{∘}
$$

rounded to the nearest integer.

Answer selection: x={83}^{∘},{263}^{∘}

### Solving a Trigonometric Equation Involving Tangent Under a Modified Domain (11 captured questions)

Question 17592186092623 — None

Given that $x_{1}$ and $x_{2}$ are the solutions of the equation $3\sqrt{3}\tan x + 3\sqrt{3} = 0$ for $-180^{∘} < x \le 180^{∘}$, what is the numerical value of $x_{1} \cdot x_{2}$?

> A scientific calculator is required to answer this question.

Solution: 

Question 17592186092879 — question.difficulty/easy

Given that ${x}_{1}$ and ${x}_{2}$ are the solutions of the equation $\operatorname{tan}⁡x=-\sqrt{3}$ for $-\pi <x\le \pi ,$ what is the value of ${x}_{1}\cdot {x}_{2}?$

Solution: First, we find the principal value:

$$
\begin{aligned}x=\operatorname{arctan}⁡(-\sqrt{3})=-\frac{\pi }{3}\end{aligned}
$$

Since $-\frac{\pi }{3}$ lies inside the given domain, our first solution is ${x}_{1}=-\frac{\pi }{3}.$

To generate more solutions, we add integer multiples of $\pi .$ Hence,

$$
\begin{aligned}{x}_{2}=\pi +{x}_{1}=\pi -\frac{\pi }{3}=\frac{2\pi }{3}.\end{aligned}
$$

So, the solutions are $x=-\frac{\pi }{3},\frac{2\pi }{3}.$

Finally,

$$
{x}_{1}\cdot {x}_{2}=-\frac{\pi }{3}\cdot \frac{2\pi }{3}=-\frac{2{\pi }^{2}}{9}.
$$

Answer selection: -\frac{2{\pi }^{2}}{9}

Question 17592186256538 — question.difficulty/moderate

Given that ${x}_{1}$ and ${x}_{2}$ are the solutions of the equation $3\sqrt{3}\operatorname{tan}⁡x+1=4$  for $-{180}^{∘}<x\le {180}^{∘},$ what is the numerical value of ${x}_{1}\cdot {x}_{2}?$

Solution: First, we rearrange the equation and isolate $\operatorname{tan}⁡x:$

$$
\begin{aligned}3\sqrt{3}\operatorname{tan}⁡x+1 & =4 \\ 3\sqrt{3}\operatorname{tan}⁡x & =3 \\ \operatorname{tan}⁡x & =\frac{1}{\sqrt{3}} \\ \operatorname{tan}⁡x & =\frac{\sqrt{3}}{3}\end{aligned}
$$

Next, we find the principal value:

$$
\begin{aligned}x=\operatorname{arctan}⁡\left(\frac{\sqrt{3}}{3}\right)={30}^{∘}\end{aligned}
$$

Since ${30}^{∘}$ lies inside the given domain, our first solution is ${x}_{1}={30}^{∘}.$

To generate more solutions, we add integer multiples of ${180}^{∘}.$ Hence:

$$
\begin{aligned}{x}_{2}=-{180}^{∘}+{x}_{1}=-{180}^{∘}+{30}^{∘}=-{150}^{∘}\end{aligned}
$$

So, the solutions are $x=-{150}^{∘},{30}^{∘}.$

Finally, the numerical value of ${x}_{1}\cdot {x}_{2}$ is

$$
{x}_{1}\cdot {x}_{2}=-150\cdot 30=-4\,500.
$$

Answer selection: -4\,500

### Finding the Points of Intersection of a Horizontal Line and a Tangent Curve (11 captured questions)

Question 17592186092624 — question.difficulty/moderate

![](images/f0/f00d8bd6cbd1f113df7f023e161e4d79e2f4a81157d1ac9a8ab65e70b4959221.png)

The graph above shows the curve $y=\operatorname{tan}⁡x$ and the line $y=-\frac{\sqrt{3}}{3}.$  Find the $x$-coordinate of the point $B.$

Solution: The $y$-values of both functions are the same at the intersection point. Equating the two equations gives: 

$$
\operatorname{tan}⁡x=-\frac{\sqrt{3}}{3}
$$

 Now, we find the principal value:

$$
\begin{aligned}x=\operatorname{arctan}⁡\left(-\frac{\sqrt{3}}{3}\right)=-\frac{\pi }{6}\end{aligned}
$$

This value lies inside $-\pi \le x<\pi $ hence, our first solution is ${x}_{1}=-\frac{\pi }{6}.$ This is the $x$ coordinate of $A.$

To get another solution, we add $\pi $ to the principal value. Thus,

$$
{x}_{2}=\pi +x=\pi -\frac{\pi }{6}=\frac{5\pi }{6}.
$$

So, the $x$-coordinate of $B$ is $\frac{5\pi }{6}.$

Answer selection: \frac{5\pi }{6}

Question 17592186092625 — None

![](images/13/13821f3293b25e222466f449b87cc8f4319b3fab6ff4393d090b248187101592.png)

The graph above shows the curve $y = \tan x$ and the line $y =-\sqrt{3}$. Find, in radians, the $x$-coordinate of the point $A$.

Solution: 

Question 17592186256547 — question.difficulty/moderate

![](images/56/56726fc8331106df9b20aed561a2ed3b93fe12d90da85a8d1b92e610b19033f7.png)

The graph above shows the curve $y=\operatorname{tan}⁡x$ and the line $y=\sqrt{3}.$ Find the $x$-coordinate of the point $B.$

$$

$$

Solution: The $y$-values of both functions are the same at the intersection point. Equating the two equations gives: 

$$
\operatorname{tan}⁡x=\sqrt{3}
$$

Now, we find the principal value:

$$
\begin{aligned}x=\operatorname{arctan}⁡(\sqrt{3})=\frac{\pi }{3}\end{aligned}
$$

This value lies outside $-\frac{3\pi }{2}<x<-\frac{\pi }{2}.$ To get a value that's inside the required domain, we add $-\pi $  to the principal value. Thus,

$$
\begin{aligned}{x}_{1}=-\pi +x=-\pi +\frac{\pi }{3}=-\frac{2\pi }{3}.\end{aligned}
$$

So, the $x$-coordinate of $B$ is $-\frac{2\pi }{3}.$

Answer selection: -\frac{2\pi }{3}
