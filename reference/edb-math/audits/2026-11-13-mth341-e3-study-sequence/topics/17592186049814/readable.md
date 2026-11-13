# 17592186049814 Vectors in N-Dimensional Euclidean Space

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186121032 — Introduction

The **real coordinate space** (of dimension $n$) is the set of all possible column vectors of height $n,$ whose components are real numbers. Symbolically, we represent the real coordinate space of dimension $n$ as $\mathbb{R}^n.$

For example, the following vectors are in $\mathbb{R}, \mathbb{R}^2,$ $\mathbb{R}^3,$ and $\mathbb{R}^5,$ respectively: 

$$
6,\qquad 
	{\left[ \begin{array}{c}\sqrt{4} \\ 0\end{array} \right]},
	\qquad
	{\left[ \begin{array}{c}- 1 \\ 8 \\ - 1\end{array} \right]},
	\qquad
	{\left[ \begin{array}{c}5 \\ - 2 \\ 0 \\ 2 \\ - 7\end{array} \right]}.
$$

We've already encountered several operations on vectors in $\mathbb{R}^2$ or $\mathbb{R}^3,$ namely, vector addition and subtraction, scalar multiplication, and the dot product. All of these operations work the same way in $\mathbb{R}^n.$



### example 17592186119612 — Calculating a Multiple of a Vector

Let $\mathbf{a}={\left[ \begin{array}{c}- 4 \\ 6 \\ 3 \\ 0\end{array} \right]}.$ Find $\dfrac{1}{2} \mathbf{a}.$

Multiplying each component of $\mathbf{a}$ by $\dfrac{1}{2},$ we get

$$
\begin{aligned}\frac{1}{2}\mathbf{a} & =\frac{1}{2}\begin{bmatrix}-4 \\ 6 \\ 3 \\ 0\end{bmatrix} \\  & =\begin{bmatrix}\frac{1}{2}\cdot (-4) \\ \frac{1}{2}\cdot 6 \\ \frac{1}{2}\cdot 3 \\ \frac{1}{2}\cdot 0\end{bmatrix} \\  & =\begin{bmatrix}-2 \\ 3 \\ \frac{3}{2} \\ 0\end{bmatrix}.\end{aligned}
$$

### tutorial 17592186121062 — Adding Two Vectors

To add two vectors in $\mathbb{R}^n,$ we just need to add their corresponding components. To illustrate, consider the vectors $\mathbf{a},\mathbf{b} \in \mathbb{R}^4,$ given by

$$
\mathbf{a}={\left[ \begin{array}{c}5 \\ 1 \\ - 3 \\ 6\end{array} \right]}, \quad \quad \mathbf{b}={\left[ \begin{array}{c}- 5 \\ 3 \\ 1 \\ 0\end{array} \right]}.
$$

To compute $\mathbf{a} + \mathbf{b},$ all we have to do is to add each component of the vector $\mathbf{a}$ with the corresponding component of $\mathbf{b}.$ Doing this, we get

$$
\begin{aligned}{\color{red}\mathbf{a}}+{\color{blue}\mathbf{b}} & =\begin{bmatrix}{\color{red}5} \\ {\color{red}1} \\ {\color{red}-3} \\ {\color{red}6}\end{bmatrix}+\begin{bmatrix}{\color{blue}-5} \\ {\color{blue}3} \\ {\color{blue}1} \\ {\color{blue}0}\end{bmatrix} \\  & =\begin{bmatrix}{\color{red}5}+({\color{blue}-5}) \\ {\color{red}1}+{\color{blue}3} \\ {\color{red}-3}+{\color{blue}1} \\ {\color{red}6}+{\color{blue}0}\end{bmatrix} \\  & =\begin{bmatrix}0 \\ 4 \\ -2 \\ 6\end{bmatrix}.\end{aligned}
$$

We can only compute the sum, difference, or dot product of two vectors if both vectors have the same number of components. For example, we can't find the following sum, so we say it's *undefined*:
$$
{\left[ \begin{array}{c}1 \\ 2 \\ 3\end{array} \right]} +  {\left[ \begin{array}{c}- 1 \\ 5\end{array} \right]} = {\color{red}\times} \:(\textrm{undefined})
$$



### example 17592186119613 — Adding Multiples of Vectors

Let $\mathbf{a}={\left[ \begin{array}{c}- 3 \\ 6 \\ 12 \\ - 9 \\ 3\end{array} \right]}$ and $\mathbf{b}={\left[ \begin{array}{c}- 4 \\ - 6 \\ 2 \\ - 8 \\ 10\end{array} \right]}.$ Find $$
\displaystyle \dfrac{1}{3}\mathbf{a}+\dfrac{1}{2}\mathbf{b}.
$$

First, we multiply each component of $\mathbf{a}$ by $\dfrac{1}{3}$ and each component of $\mathbf{b}$ by $\dfrac{1}{2}.$ Then, we add the vectors:

$$
\begin{aligned}\frac{1}{3}\mathbf{a}+\frac{1}{2}\mathbf{b} & =\frac{1}{3}\cdot \begin{bmatrix}-3 \\ 6 \\ 12 \\ -9 \\ 3\end{bmatrix}+\frac{1}{2}\cdot \begin{bmatrix}-4 \\ -6 \\ 2 \\ -8 \\ 10\end{bmatrix} \\  & =\begin{bmatrix}-1 \\ 2 \\ 4 \\ -3 \\ 1\end{bmatrix}+\begin{bmatrix}-2 \\ -3 \\ 1 \\ -4 \\ 5\end{bmatrix} \\  & =\begin{bmatrix}-1-2 \\ 2-3 \\ 4+1 \\ -3-4 \\ 1+5\end{bmatrix} \\  & =\begin{bmatrix}-3 \\ -1 \\ 5 \\ -7 \\ 6\end{bmatrix}\end{aligned}
$$

### tutorial 17592186121033 — General Rules

In general, if we have two vectors $\mathbf{u},\mathbf{v}\in\mathbb{R}^n$ and a scalar $\lambda\in\mathbb{R},$ then our vector operations are defined as follows:

1\. The **sum/difference** of the two vectors is defined as
  $$
\mathbf{u} \pm \mathbf{v} = {\left[ \begin{array}{c}{u}_{1} \\ {u}_{2} \\ \vdots  \\ {u}_{n}\end{array} \right]} \pm {\left[ \begin{array}{c}{v}_{1} \\ {v}_{2} \\ \vdots  \\ {v}_{n}\end{array} \right]} = {\left[ \begin{array}{c}{u}_{1} \pm  {v}_{1} \\ {u}_{2} \pm  {v}_{2} \\ \vdots  \\ {u}_{n} \pm  {v}_{n}\end{array} \right]}.
$$

2\. **Scalar multiplication** of a vector is defined as
  $$
\quad \lambda \mathbf{u} =\lambda \cdot {\left[ \begin{array}{c}{u}_{1} \\ {u}_{2} \\ \vdots  \\ {u}_{n}\end{array} \right]} = {\left[ \begin{array}{c}\lambda  \cdot  {u}_{1} \\ \lambda  \cdot  {u}_{2} \\ \vdots  \\ \lambda  \cdot  {u}_{n}\end{array} \right]}.
$$

3\. The **dot product** of two vectors is defined as

  $$
\quad \mathbf{u}\cdot\mathbf{v} = \underbrace{u_1 \cdot v_1 + u_2 \cdot v_2 + \cdots + u_n \cdot v_n}_{\Large{n} \,\textrm{-terms}} = \sum_{i=1}^n u_i v_i.
$$



### example 17592186119614 — Calculating the Dot Product of Two Vectors

If $\mathbf{u} = {\left[ \begin{array}{c}- 1 \\ 4 \\ 3 \\ - 5\end{array} \right]}$ and $\mathbf{v} = {\left[ \begin{array}{c}- 2 \\ 3 \\ - 4 \\ 6\end{array} \right]},$ then what is $\mathbf{u} \cdot \mathbf{v}?$

To compute the dot product, we add up the products of corresponding components:

$$
\begin{aligned}\mathbf{u}\cdot \mathbf{v} & ={u}_{1}\cdot {v}_{1}+{u}_{2}\cdot {v}_{2}+{u}_{3}\cdot {v}_{3}+{u}_{4}\cdot {v}_{4} \\  & =(-1)\cdot (-2)+4\cdot 3+3\cdot (-4)+(-5)\cdot 6 \\  & =2+12-12-30 \\  & =-28\end{aligned}
$$

### example 17592186119615 — Finding the Value of an Unknown Quantity in an Expression Involving the Dot Product

Let be $\mathbf{a}={\left[ \begin{array}{c}10 \\ x \\ 0 \\ 5\end{array} \right]}$ and $\mathbf{b}={\left[ \begin{array}{c}x \\ x \\ 8 \\ 5\end{array} \right]}.$ If $\mathbf{a}\cdot \mathbf{b}=0,$ find the value of $x.$

Starting from the equation $\mathbf{a} \cdot \mathbf{b}=0,$ we compute the dot product in terms of $x$ and then solve for $x$ in the resulting equation:

$$
\begin{aligned}\mathbf{a}\cdot \mathbf{b} & =0 \\ 10\cdot x+x\cdot x+0\cdot 8+5\cdot 5 & =0 \\ 10x+{x}^{2}+25 & =0 \\ {x}^{2}+10x+25 & =0 \\ (x+5)^{2} & =0 \\ x & =-5\end{aligned}
$$

Therefore, we conclude that $x=-5.$

## Representative practice (first three per skill; full bank in practice.json)

### Calculating a Multiple of a Vector (13 captured questions)

Question 17592186120371 — question.difficulty/easy

Let $\mathbf{u}=\begin{bmatrix}5 \\ 6 \\ -9 \\ 0\end{bmatrix}.$ Find $-\frac{1}{3}\mathbf{u}.$

Solution: Multiplying each component of $\mathbf{u}$ by $-\frac{1}{3},$ we get

$$
\begin{aligned}-\frac{1}{3}\mathbf{u} & =-\frac{1}{3}\begin{bmatrix}5 \\ 6 \\ -9 \\ 0\end{bmatrix} \\  & =\begin{bmatrix}-\frac{1}{3}\cdot 5 \\ -\frac{1}{3}\cdot 6 \\ -\frac{1}{3}\cdot (-9) \\ -\frac{1}{3}\cdot 0\end{bmatrix} \\  & =\begin{bmatrix}-\frac{5}{3} \\ -2 \\ 3 \\ 0\end{bmatrix}.\end{aligned}
$$

Answer selection: \begin{bmatrix}-\frac{5}{3} \\ -2 \\ 3 \\ 0\end{bmatrix}

Question 17592186120375 — question.difficulty/easy

If $\mathbf{u}=\begin{bmatrix}0 \\ 1 \\ -2 \\ 6\end{bmatrix}$, then $2\mathbf{u}=$

Solution: Multiplying each component of $u$ by $2,$ we get

$$
\begin{aligned}2u & =2\begin{bmatrix}0 \\ 1 \\ -2 \\ 6\end{bmatrix} \\  & =\begin{bmatrix}2\cdot 0 \\ 2\cdot 1 \\ 2\cdot (-2) \\ 2\cdot 6\end{bmatrix} \\  & =\begin{bmatrix}0 \\ 2 \\ -4 \\ 12\end{bmatrix}.\end{aligned}
$$

Answer selection: \begin{bmatrix}0 \\ 2 \\ -4 \\ 12\end{bmatrix}

Question 17592186342108 — question.difficulty/easy

If $\mathbf{v}=\begin{bmatrix}0 \\ 2 \\ 5 \\ -1\end{bmatrix}$, then $3\mathbf{v}=$

Solution: Multiplying each component of $\mathbf{v}$ by $3,$ we get

$$
\begin{aligned}3\mathbf{v} & =3\begin{bmatrix}0 \\ 2 \\ 5 \\ -1\end{bmatrix} \\  & =\begin{bmatrix}3\cdot 0 \\ 3\cdot 2 \\ 3\cdot 5 \\ 3\cdot (-1)\end{bmatrix} \\  & =\begin{bmatrix}0 \\ 6 \\ 15 \\ -3\end{bmatrix}.\end{aligned}
$$

Answer selection: \begin{bmatrix}0 \\ 6 \\ 15 \\ -3\end{bmatrix}

### Adding Multiples of Vectors (14 captured questions)

Question 17592186120307 — question.difficulty/easy

Let $\mathbf{a}=\begin{bmatrix}-3 \\ 2 \\ 5 \\ 1 \\ -2\end{bmatrix}$ and $\mathbf{b}=\begin{bmatrix}-3 \\ -2 \\ 1 \\ 5 \\ 6\end{bmatrix}.$ Find $3\mathbf{a}+2\mathbf{b}.$

Solution: First, we multiply each component of $\mathbf{a}$ by $3$ and each component of $\mathbf{b}$ by $2.$ Then, we add the vectors:

$$
\begin{aligned}3\mathbf{a}+2\mathbf{b} & =3\cdot \begin{bmatrix}-3 \\ 2 \\ 5 \\ 1 \\ -2\end{bmatrix}+2\cdot \begin{bmatrix}-3 \\ -2 \\ 1 \\ 5 \\ 6\end{bmatrix} \\  & =\begin{bmatrix}-9 \\ 6 \\ 15 \\ 3 \\ -6\end{bmatrix}+\begin{bmatrix}-6 \\ -4 \\ 2 \\ 10 \\ 12\end{bmatrix} \\  & =\begin{bmatrix}-9-6 \\ 6-4 \\ 15+2 \\ 3+10 \\ -6+12\end{bmatrix} \\  & =\begin{bmatrix}-15 \\ 2 \\ 17 \\ 13 \\ 6\end{bmatrix}\end{aligned}
$$

Answer selection: \begin{bmatrix}-15 \\ 2 \\ 17 \\ 13 \\ 6\end{bmatrix}

Question 17592186120374 — question.difficulty/easy

Let $\mathbf{a}=\begin{bmatrix}1 \\ -1 \\ 5 \\ 6\end{bmatrix}$ and $\mathbf{b}=\begin{bmatrix}7 \\ 8 \\ -9 \\ 5 \\ 0\end{bmatrix}.$ Find $5\mathbf{a}-\mathbf{b}.$

Solution: Let's examine our vectors:

- The vector $a=\begin{bmatrix}1 \\ -1 \\ 5 \\ 6\end{bmatrix}$ has $4$ components as it lies in ${R}^{4}.$

- The vector $b=\begin{bmatrix}7 \\ 8 \\ -9 \\ 5 \\ 0\end{bmatrix}$ has $5$ components as it lies in ${R}^{5}.$

Therefore, since the number of components does not match, the operation is undefined.

Answer selection: Undefined

Question 17592186240977 — question.difficulty/easy

Let $\mathbf{a}=\begin{bmatrix}1 \\ -4 \\ 1 \\ 0\end{bmatrix}$ and $\mathbf{b}=\begin{bmatrix}6 \\ 6 \\ -2 \\ 4\end{bmatrix}.$ Find $\mathbf{a}+\frac{1}{2}\mathbf{b}.$

Solution: First, we multiply each component of $\mathbf{b}$ by $\frac{1}{2}.$ Then, we add the vectors:

$$
\begin{aligned}\mathbf{a}+\frac{1}{2}\mathbf{b} & =\begin{bmatrix}1 \\ -4 \\ 1 \\ 0\end{bmatrix}+\frac{1}{2}\cdot \begin{bmatrix}6 \\ 6 \\ -2 \\ 4\end{bmatrix} \\  & =\begin{bmatrix}1 \\ -4 \\ 1 \\ 0\end{bmatrix}+\begin{bmatrix}3 \\ 3 \\ -1 \\ 2\end{bmatrix} \\  & =\begin{bmatrix}1+3 \\ -4+3 \\ 1+(-1) \\ 0+2\end{bmatrix} \\  & =\begin{bmatrix}4 \\ -1 \\ 0 \\ 2\end{bmatrix}\end{aligned}
$$

Answer selection: \begin{bmatrix}4 \\ -1 \\ 0 \\ 2\end{bmatrix}

### Calculating the Dot Product of Two Vectors (11 captured questions)

Question 17592186120308 — question.difficulty/easy

If $\mathbf{u}=\begin{bmatrix}-4 \\ 1 \\ 2 \\ 3\end{bmatrix}$ and $\mathbf{v}=\begin{bmatrix}2 \\ -4 \\ 6 \\ -7\end{bmatrix}$, then $\mathbf{u}\cdot \mathbf{v}=$

Solution: To compute the dot product, we add up the products of corresponding components:

$$
\begin{aligned}\mathbf{u}\cdot \mathbf{v} & ={u}_{1}\cdot {v}_{1}+{u}_{2}\cdot {v}_{2}+{u}_{3}\cdot {v}_{3}+{u}_{4}\cdot {v}_{4} \\  & =(-4)\cdot 2+1\cdot (-4)+2\cdot 6+3\cdot (-7) \\  & =-8-4+12-21 \\  & =-21\end{aligned}
$$

Answer selection: -21

Question 17592186120373 — question.difficulty/moderate

Let $$
\mathbf{u}=\begin{bmatrix}1 \\ -1 \\ 1 \\ 2\end{bmatrix}
$$ and $$
\mathbf{v}=\begin{bmatrix}2 \\ -5 \\ 1 \\ 0\end{bmatrix}.
$$ What is $(2\mathbf{u})\cdot \mathbf{v}?$

Solution: First, multiplying each component of $u$ by $2$, we get

$$
\begin{aligned}2u & =2\begin{bmatrix}1 \\ -1 \\ 1 \\ 2\end{bmatrix}=\begin{bmatrix}2 \\ -2 \\ 2 \\ 4\end{bmatrix}\,.\end{aligned}
$$

To compute the dot product, we add up the products of corresponding components:

$$
\begin{aligned}(2u)\cdot v & =2\cdot 2+(-2)\cdot (-5)+2\cdot 1+4\cdot 0 \\  & =4+10+2+0 \\  & =16\end{aligned}
$$

Answer selection: 16

Question 17592186240979 — question.difficulty/moderate

Let $\mathbf{r}=\begin{bmatrix}15 \\ 9 \\ 6 \\ -3\end{bmatrix}$ and $\mathbf{s}=\begin{bmatrix}1 \\ -7 \\ 6 \\ 2\end{bmatrix}.$ What is $\left(\frac{1}{3}\mathbf{r}\right)\cdot \mathbf{s}?$

Solution: First, multiplying each component of $\mathbf{r}$ by $\frac{1}{3}$, we get

$$
\begin{aligned}\frac{1}{3}\mathbf{r} & =\frac{1}{3}\begin{bmatrix}15 \\ 9 \\ 6 \\ -3\end{bmatrix}=\begin{bmatrix}5 \\ 3 \\ 2 \\ -1\end{bmatrix}\hspace{-0.167em}.\end{aligned}
$$

To compute the dot product, we add up the products of corresponding components:

$$
\begin{aligned}\left(\frac{1}{3}\mathbf{r}\right)\cdot \mathbf{s} & =5\cdot 1+3\cdot (-7)+2\cdot 6+(-1)\cdot 2 \\  & =5-21+12-2 \\  & =-6\end{aligned}
$$

Answer selection: -6

### Finding the Value of an Unknown Quantity in an Expression Involving the Dot Product (14 captured questions)

Question 17592186120372 — question.difficulty/moderate

Let
$\mathbf{a}=\begin{bmatrix}5 \\ 0 \\ p \\ 1\end{bmatrix}$ and $\mathbf{b}=\begin{bmatrix}p \\ -3 \\ 7 \\ -4\end{bmatrix}.$
If $\mathbf{a}\cdot \mathbf{b}=8$, find the value of $p.$

Solution: Starting from the equation $a\cdot b=8,$ we compute the dot product in terms of $p$ and then solve for $p$ in the resulting equation:

$$
\begin{aligned}a\cdot b & =8 \\ 5\cdot p+0\cdot (-3)+p\cdot 7+1\cdot (-4) & =8 \\ 5p+7p-4 & =8 \\ 12p & =12 \\ p & =1\end{aligned}
$$

Therefore, we conclude that $p=1.$

Answer selection: 1

Question 17592186120376 — None

Let $\mathbf{u}=\begin{bmatrix}\frac{4}{{x}^{2}} \\ 4 \\ x \\ 7\end{bmatrix}$ and $\mathbf{v}=\begin{bmatrix}{x}^{4} \\ 0 \\ 8 \\ -7\end{bmatrix}$.
If $\mathbf{u}\cdot \mathbf{v}=11$ and $x < 0$, find the value of $x$.

Solution: Starting from $\mathbf u\cdot\mathbf v=11$, compute the dot product and solve:

$$
\begin{aligned}\frac4{x^2}x^4+4\cdot0+8x+7(-7)&=11\\4x^2+8x-60&=0\\x^2+2x-15&=0\\(x+5)(x-3)&=0.\end{aligned}
$$

The vector requires $x\ne0$, and both roots satisfy this restriction. Since $x<0$, the required root is $x=-5$.

Answer selection: -5

Question 17592186240980 — question.difficulty/moderate

Let
$a=\begin{bmatrix}x \\ 2 \\ 1 \\ -1\end{bmatrix}$ and $b=\begin{bmatrix}3 \\ x \\ 9 \\ 7\end{bmatrix}.$
If $a\cdot b=-3$, find the value of $x.$

Solution: Starting from the equation $\mathbf{a}\cdot \mathbf{b}=-3,$ we compute the dot product in terms of $x$ and then solve for $x$ in the resulting equation:

$$
\begin{aligned}\mathbf{a}\cdot \mathbf{b} & =-3 \\ x\cdot 3+2\cdot x+1\cdot 9+(-1)\cdot 7 & =-3 \\ 3x+2x+9-7 & =-3 \\ 5x & =-5 \\ x & =-1\end{aligned}
$$

Therefore, we conclude that $x=-1.$

Answer selection: -1
