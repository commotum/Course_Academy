# 17592186050426 Linear Dependence and Independence

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186121122 — Introduction

We say that two vectors $\mathbf{v}_1$ and $\mathbf{v}_2$ are **linearly independent** if the only solution to the equation

$$
x_1 \mathbf{v}_1 + x_2 \mathbf{v}_2 = \mathbf{0}
$$

is $x_1 = x_2 = 0.$ Otherwise, if there exists any solution other than $x_1 = x_2 = 0,$ then we say that the two vectors $\mathbf{v}_1$ and $\mathbf{v}_2$ are **linearly dependent**.

To illustrate, let's consider two sets of vectors in $\mathbb{R}^2\mathbin{:}$

$$
{\color{blue}
\textrm{I.}\:\: \Bigg\{ \underbrace{ {\left[ \begin{array}{c}1 \\ 0\end{array} \right]}}_{\mathbf{a}_1}, \underbrace{ {\left[ \begin{array}{c}0 \\ 1\end{array} \right]}}_{\mathbf{a}_2} \Bigg\}
}
{\color{red}
\qquad\qquad
\textrm{II.}\:\: \Bigg\{ \underbrace{ {\left[ \begin{array}{c}1 \\ 1\end{array} \right]}}_{\mathbf{b}_1}, \underbrace{ {\left[ \begin{array}{c}- 2 \\ - 2\end{array} \right]}}_{\mathbf{b}_2} \Bigg\}
}
$$

- For the first set ${\color{blue}(\textrm{I})},$ we have

$$
\begin{aligned}{x}_{1}{\color{blue}{\mathbf{a}}_{1}}+{x}_{2}{\color{blue}{\mathbf{a}}_{2}} & =\mathbf{0} \\ {x}_{1}{\color{blue}\begin{bmatrix}1 \\ 0\end{bmatrix}}+{x}_{2}{\color{blue}\begin{bmatrix}0 \\ 1\end{bmatrix}} & =\mathbf{0}.\end{aligned}
$$

The above equation is true only if $x_1=x_2=0.$ So, the set $\color{blue}(\textrm{I})$ is *linearly independent*.

- On the other hand, for the second set ${\color{red}(\textrm{II})},$ we have

$$
\begin{aligned}{x}_{1}{\color{red}{\mathbf{b}}_{1}}+{x}_{2}{\color{red}{\mathbf{b}}_{2}} & =\mathbf{0} \\ {x}_{1}{\color{red}\begin{bmatrix}1 \\ 1\end{bmatrix}}+{x}_{2}{\color{red}\begin{bmatrix}-2 \\ -2\end{bmatrix}} & =\mathbf{0}.\end{aligned}
$$

The above equation has solutions other than $x_1=x_2=0.$ For example, $x_1=2$ and $x_2=1$ gives
$$
2 \cdot {\color{red}{\left[ \begin{array}{c}1 \\ 1\end{array} \right]}} + 1 \cdot {\color{red}{\left[ \begin{array}{c}- 2 \\ - 2\end{array} \right]}} = \mathbf{0}.
$$
Therefore, the set $\color{red}(\textrm{II})$ is *not* linearly independent. Rather, it is *linearly dependent*.

**Note:** You may notice that the vectors in the set $\color{red}(\textrm{II})$ were parallel (i.e. multiples of one another), while the vectors in set $\color{blue}(\textrm{I})$ were not. This trend holds in general, for all sets of two vectors:

- a set of two vectors is *linearly dependent* if and only if the two vectors are parallel, while

- a set of two vectors is *linearly independent* if and only if the two vectors are not parallel.



### tutorial 17592186121123 — Sets of Two Vectors Containing the Zero Vector

Any set of two vectors that contains the zero vector $\mathbf{0}$ must be linearly dependent. To see this, consider the set $\left\{ \mathbf{v}, \mathbf{0} \right\}.$ We can realize that this set is linearly dependent using either of the following two methods.

**Method 1**

Notice that 

$$
0 \cdot \mathbf{v} + 1 \cdot \mathbf{0} = \mathbf{0}.
$$

Therefore, the equation

$$
x_1 \mathbf{v} + x_2 \cdot \mathbf{0} = \mathbf{0}
$$

has a solution $x_1=0$ and $x_2=1,$ which is different from $x_1=x_2=0.$ So, the set is linearly dependent.

**Method 2**

Alternatively, recall that a set of two vectors is linearly dependent if and only if the two vectors are parallel. That is, the two vectors are multiples of each other.

The zero vector $\mathbf{0}$ is parallel to every other vector because it is a multiple of any other vector. For any vector $\mathbf{v},$ we have

$$
\mathbf{0} = 0 \cdot \mathbf{v} \qquad \Longrightarrow \qquad \mathbf{0} \parallel \mathbf{v}.
$$

So, because $\mathbf{0}$ is parallel to $\mathbf{v},$ the set $\left\{ \mathbf{v}, \mathbf{0} \right\}$ is linearly dependent.



### example 17592186119497 — Finding a Vector That Makes a Set Linearly Dependent

The set $\{ \mathbf{a_1},\mathbf{a_2} \}$ is linearly dependent. Which of the following vectors could be $\mathbf{a}_2$ if
$$
\mathbf{a_1} = {\left[ \begin{array}{c}12 \\ 3 \\ 21\end{array} \right]}?
$$

$$
{\left[ \begin{array}{c}4 \\ 1 \\ 7\end{array} \right]}, \qquad {\left[ \begin{array}{c}4 \\ 1 \\ 2\end{array} \right]}, \qquad {\left[ \begin{array}{c}4 \\ 1 \\ 1\end{array} \right]}
$$

We say that two vectors $\mathbf{v}_1$ and $\mathbf{v}_2$ are *linearly independent* if the only solution to the equation

$$
x_1 \mathbf{v}_1 + x_2 \mathbf{v}_2 = \mathbf{0}
$$

is $x_1 = x_2 = \mathbf{0}.$ Otherwise, the vectors are *linearly dependent*.

A set containing *only two* vectors is linearly *dependent* if and only if the two vectors are parallel.

From the given options, the correct answer is
$$
\mathbf{a}_2 = {\left[ \begin{array}{c}4 \\ 1 \\ 7\end{array} \right]}.
$$
To see why, notice that 
$$
{\left[ \begin{array}{c}4 \\ 1 \\ 7\end{array} \right]}= \dfrac 1 3 {\left[ \begin{array}{c}12 \\ 3 \\ 21\end{array} \right]} = \dfrac 1 3\mathbf{a}_1.
$$
In other words, the vectors $\mathbf{a}_1$ and $\mathbf{a}_2$ are parallel.

To see why this means that $\mathbf{a}_1$ and $\mathbf{a}_2$ are linearly dependent, notice that

$$
\begin{aligned}\frac{1}{3}{\mathbf{a}}_{1}-{\mathbf{a}}_{2} & =\mathbf{0}.\end{aligned}
$$

So, the equation

$$
x_1 \mathbf{a}_1  +x_2  \mathbf{a}_2 = \mathbf{0}
$$

has the solution $x_1=\dfrac 1 3$ and $x_2=-1,$ which is different from $x_1=x_2=\mathbf{0}.$ Therefore, the set is linearly dependent.

### tutorial 17592186121124 — Linear Dependence and Independence for a General Set of Vectors

So far, we've discussed linear dependence and linear independence for sets of two vectors. However, these concepts can be extended to sets of any number of vectors.

A set of $n$ vectors $\left\{ \mathbf{v}_1, \mathbf{v}_2, \ldots, \mathbf{v}_n \right\}$ is called **linearly independent** if the only solution to the equation

$$
x_1 \mathbf{v}_1 + x_2 \mathbf{v}_2 + \ldots + x_n \mathbf{v}_n = \mathbf{0}
$$

is $x_1=x_2=\ldots=x_n=0.$ Otherwise, if there exists any solution other than $x_1 = x_2 = \ldots = x_n = 0,$ then we say that the set $\left\{ \mathbf{v}_1, \mathbf{v}_2, \ldots, \mathbf{v}_n \right\}$ is **linearly dependent**.

Similar to sets containing two vectors, a general set of $n$ vectors is dependent if *any* two vectors in the set are parallel.

**But be careful!** When working with sets containing more than two vectors, having a linearly dependent set is possible even if *none* of the vectors are parallel! 

For example, consider the following set of vectors: 

$$
\left\{
	{\left[ \begin{array}{c}1 \\ 0\end{array} \right]},
	{\left[ \begin{array}{c}0 \\ 1\end{array} \right]},
	{\left[ \begin{array}{c}1 \\ 1\end{array} \right]}
	\right\}
$$

None of the vectors in this set are parallel. However, we have

$$
{\left[ \begin{array}{c}1 \\ 0\end{array} \right]} + {\left[ \begin{array}{c}0 \\ 1\end{array} \right]} - {\left[ \begin{array}{c}1 \\ 1\end{array} \right]} = {\left[ \begin{array}{c}0 \\ 0\end{array} \right]}.
$$

So, the equation

$$
x_1 \cdot {\left[ \begin{array}{c}1 \\ 0\end{array} \right]} + x_2 \cdot {\left[ \begin{array}{c}0 \\ 1\end{array} \right]}+ x_3 \cdot {\left[ \begin{array}{c}1 \\ 1\end{array} \right]} = {\left[ \begin{array}{c}0 \\ 0\end{array} \right]}
$$

has a solution $x_1 = 1,$ $x_2 = 1,$ and $x_3 = -1,$ which is different from $x_1 = x_2 = x_3 = 0.$ Therefore, we conclude that the vectors are linearly dependent.



### tutorial 17592186121125 — General Sets of Vectors Containing the Zero Vector

As with sets containing only two vectors, any set of vectors that contains the zero vector $\mathbf{0}$ must be linearly dependent. 

To see this, consider the set 

$$
\left\{ \mathbf{v}_1, \mathbf{v}_2, \ldots, \mathbf{v}_{n-1}, \mathbf{0} \right\}.
$$

 

Notice that 

$$
0 \cdot \mathbf{v}_1 + 0 \cdot \mathbf{v}_2 + \ldots + 0 \cdot \mathbf{v}_{n-1} + 1 \cdot \mathbf{0} = \mathbf{0}.
$$

So, the equation

$$
x_1 \mathbf{v}_1 + x_2 \mathbf{v}_2 + \ldots + x_{n-1} \mathbf{v}_{n-1} + x_n \cdot \mathbf{0} = \mathbf{0}
$$

has the solution $x_1=x_2=\ldots = x_{n-1}=0$ and $x_n=1,$ which is different from $x_1=x_2=\ldots = x_n=0.$ Therefore, the set is linearly dependent.



### example 17592186119498 — Identifying Linearly Independent Sets by Inspection

Consider the following vectors:

$$
\mathbf{a}_1 = {\left[ \begin{array}{c}4 \\ - 1 \\ 0\end{array} \right]}, \qquad
\mathbf{a}_2 = {\left[ \begin{array}{c}0 \\ 1 \\ 0\end{array} \right]},\qquad
\mathbf{a}_3 = {\left[ \begin{array}{c}2 \\ - 1 \\ 7\end{array} \right]}.
$$

Which of the following statements are true?

I. $\mathbf{a}_1 - \mathbf{a}_2 -2 \mathbf{a}_3 = \mathbf{0}.$

II. $x_1\mathbf{a}_1 + x_2\mathbf{a}_2 + x_3\mathbf{a}_3  = \mathbf{0}$ only if $x_1=x_2=x_3 = \mathbf{0}.$

III. The set $\{\mathbf{a}_1, \mathbf{a}_2, \mathbf{a}_3\}$ is linearly independent.

We say that three vectors $\mathbf{v}_1, \mathbf{v}_2$ and $\mathbf{v}_3$ are *linearly independent* if the only solution to the equation

$$
x_1 \mathbf{v}_1 + x_2 \mathbf{v}_2 + x_3\mathbf{v}_3= \mathbf{0}
$$

is $x_1 = x_2 = x_3 = \mathbf{0}.$ Otherwise, the vectors are *linearly dependent*.

With that in mind, let's look at each statement in turn.

- Statement I is false. Indeed:

$$
\begin{aligned}{\mathbf{a}}_{1}-{\mathbf{a}}_{2}-2{\mathbf{a}}_{3} & =\begin{bmatrix}4 \\ -1 \\ 0\end{bmatrix}-\begin{bmatrix}0 \\ 1 \\ 0\end{bmatrix}-2\begin{bmatrix}2 \\ -1 \\ 7\end{bmatrix} \\  & =\begin{bmatrix}4 \\ -1 \\ 0\end{bmatrix}+\begin{bmatrix}0 \\ -1 \\ 0\end{bmatrix}+\begin{bmatrix}-4 \\ 2 \\ -14\end{bmatrix} \\  & =\begin{bmatrix}4+0-4 \\ -1-1+2 \\ 0+0-14\end{bmatrix} \\  & =\begin{bmatrix}0 \\ 0 \\ -14\end{bmatrix} \\  & \ne \mathbf{0}\end{aligned}
$$

- Statement II is true. The equation $x_1\mathbf{a}_1 + x_2\mathbf{a}_2 + x_3\mathbf{a}_3 = \mathbf{0}$ corresponds to the system

$$
\left\{\begin{aligned}4{x}_{1}+2{x}_{3} &=\mathbf{0} \\ -{x}_{1}+{x}_{2}-{x}_{3} &=\mathbf{0} \\ 7{x}_{3} &=\mathbf{0}.\end{aligned}\right.
$$

Notice that we can reorder the equations in this system as follows:

$$
\left\{\begin{aligned}-{x}_{1}+{x}_{2}-{x}_{3} &=\mathbf{0} \\ 4{x}_{1}+2{x}_{3} &=\mathbf{0} \\ 7{x}_{3} &=\mathbf{0}\end{aligned}\right.
$$

Solving this system using back substitution, we find that the solution is $x_1 = x_2 = x_3 = \mathbf{0}.$

- Statement III is true. Since statement II is true, the set $\{\mathbf{a}_1, \mathbf{a}_2, \mathbf{a}_3 \}$ is linearly independent.

Therefore, the correct answer is "II and III only."

### example 17592186119499 — Identifying Linearly Independent and Dependent Sets Using Row Reduction

Consider the following vectors:

$$
\mathbf{a}_1 = {\left[ \begin{array}{c}2 \\ 4 \\ 0\end{array} \right]}, \qquad
\mathbf{a}_2 = {\left[ \begin{array}{c}- 1 \\ 4 \\ 6\end{array} \right]}, \qquad
\mathbf{a}_3 = {\left[ \begin{array}{c}2 \\ 5 \\ 1\end{array} \right]}.
$$

Assume that $x_1,x_2,$ and $x_3$ are real numbers. Which of the following statements are true?

I. The equation $x_1\mathbf{a}_1+x_2\mathbf{a}_2+x_3\mathbf{a}_3=\mathbf{0}$ has an infinite number of nonzero solutions.

II. The vectors $\mathbf{a}_1,\mathbf{a}_2,$ and $\mathbf{a}_3$ are linearly independent.

III. The vectors $\mathbf{a}_1,\mathbf{a}_2,$ and $\mathbf{a}_3$ are linearly dependent.

We say that three vectors $\mathbf{v}_1, \mathbf{v}_2,$ and $\mathbf{v}_3$ are *linearly independent* if the only solution to the equation

$$
x_1 \mathbf{v}_1 + x_2 \mathbf{v}_2 + x_3 \mathbf{v}_3 = \mathbf{0}
$$

is $x_1 = x_2 = x_3 = 0.$ Otherwise, the vectors are *linearly dependent*.

With that in mind, let's examine our statements.

The equation $x_1\mathbf{a}_1+x_2\mathbf{a}_2+x_3\mathbf{a}_3=\mathbf{0}$ corresponds to the system

$$
\left\{\begin{aligned}2{x}_{1}-{x}_{2}+2{x}_{3} &=0 \\ 4{x}_{1}+4{x}_{2}+5{x}_{3} &=0 \\ 6{x}_{2}+{x}_{3} &=0.\end{aligned}\right.
$$

To solve the system, we create its augmented matrix and reduce it using Gaussian elimination:

$$
\begin{aligned}M & =\left[\begin{array}{ccc|c}2 & -1 & 2 & 0 \\ 4 & 4 & 5 & 0 \\ 0 & 6 & 1 & 0\end{array}\right] & {R}_{2}:={R}_{2}+(-2){R}_{1} \\  & ∼\left[\begin{array}{ccc|c}2 & -1 & 2 & 0 \\ 0 & 6 & 1 & 0 \\ 0 & 6 & 1 & 0\end{array}\right] & {R}_{3}:={R}_{3}+(-1){R}_{2} \\  & ∼\left[\begin{array}{ccc|c}2 & -1 & 2 & 0 \\ 0 & 6 & 1 & 0 \\ 0 & 0 & 0 & 0\end{array}\right]\end{aligned}
$$

From the matrix above, we conclude that the basic variables are $x_1$ and $x_2,$ while $x_3$ is the free variable. 

Since there is one free variable, the equation $x_1\mathbf{a}_1+x_2\mathbf{a}_2+x_3\mathbf{a}_3=\mathbf{0}$ has an infinite number of nonzero solutions, which means that the vectors are linearly dependent. 

Therefore, statements II is false, while statements I and III are true.

## Representative practice (first three per skill; full bank in practice.json)

### Finding a Vector That Makes a Set Linearly Dependent (25 captured questions)

Question 17592186120320 — question.difficulty/easy

The set $\{{\mathbf{a}}_{\mathbf{1}},{\mathbf{a}}_{\mathbf{2}}\}$ is linearly dependent. Which of the following vectors could be ${\mathbf{a}}_{2}$ if
$$
{\mathbf{a}}_{\mathbf{1}}=\begin{bmatrix}2 \\ -3\end{bmatrix}?
$$

Solution: We say that two vectors ${\mathbf{v}}_{1}$ and ${\mathbf{v}}_{2}$ are *linearly independent* if the only solution to the equation

$$
{x}_{1}{\mathbf{v}}_{1}+{x}_{2}{\mathbf{v}}_{2}=\mathbf{0}
$$

is ${x}_{1}={x}_{2}=\mathbf{0}.$ Otherwise, the vectors are *linearly dependent*.

A set containing *only two* vectors is linearly *dependent* if and only if the two vectors are parallel.

From the given options, the correct answer is 

$$
{\mathbf{a}}_{2}=\begin{bmatrix}-8 \\ 12\end{bmatrix}.
$$

To see why, notice that 

$$
\begin{bmatrix}-8 \\ 12\end{bmatrix}=-4\begin{bmatrix}2 \\ -3\end{bmatrix}=-4{\mathbf{a}}_{1}.
$$

This way, we have

$$
\begin{aligned}4{\mathbf{a}}_{1}-4{\mathbf{a}}_{1} & =\mathbf{0} \\ 4{\mathbf{a}}_{1}+{\mathbf{a}}_{2} & =\mathbf{0}.\end{aligned}
$$

In other words, the vectors ${\mathbf{a}}_{1}$ and ${\mathbf{a}}_{2}$ are parallel.

To see why this means that ${\mathbf{a}}_{1}$ and ${\mathbf{a}}_{2}$ are linearly dependent, we notice that the equation

$$
{x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2}=\mathbf{0}
$$

has the solution ${x}_{1}=4$ and ${x}_{2}=1,$ which is different from ${x}_{1}={x}_{2}=\mathbf{0}.$ Therefore, the set is linearly dependent.

Answer selection: \begin{bmatrix}-8 \\ 12\end{bmatrix}

Question 17592186120321 — question.difficulty/moderate

The set $\{{\mathbf{a}}_{\mathbf{1}},{\mathbf{a}}_{\mathbf{2}}\}$ is linearly dependent. Which of the following vectors could be ${\mathbf{a}}_{2}$ if
$$
{\mathbf{a}}_{\mathbf{1}}=\begin{bmatrix}1 \\ -4 \\ 2\end{bmatrix}?
$$

Solution: We say that two vectors ${\mathbf{v}}_{1}$ and ${\mathbf{v}}_{2}$ are *linearly independent* if the only solution to the equation

$$
{x}_{1}{\mathbf{v}}_{1}+{x}_{2}{\mathbf{v}}_{2}=\mathbf{0}
$$

is ${x}_{1}={x}_{2}=\mathbf{0}.$ Otherwise, the vectors are *linearly dependent*.

A set containing *only two* vectors is linearly *dependent* if and only if the two vectors are parallel.

From the given options, the correct answer is 

$$
{\mathbf{a}}_{2}=\begin{bmatrix}5 \\ -20 \\ 10\end{bmatrix}.
$$

To see why, notice that 

$$
\begin{bmatrix}5 \\ -20 \\ 10\end{bmatrix}=5\begin{bmatrix}1 \\ -4 \\ 2\end{bmatrix}=5{\mathbf{a}}_{1}.
$$

This way, we have

$$
\begin{aligned}5{\mathbf{a}}_{1}-5{\mathbf{a}}_{1} & =\mathbf{0} \\ 5{\mathbf{a}}_{1}-{\mathbf{a}}_{2} & =\mathbf{0} \\ 5{\mathbf{a}}_{1}+(-1){\mathbf{a}}_{2} & =\mathbf{0}.\end{aligned}
$$

In other words, the vectors ${\mathbf{a}}_{1}$ and ${\mathbf{a}}_{2}$ are parallel.

To see why this means that ${\mathbf{a}}_{1}$ and ${\mathbf{a}}_{2}$ are linearly dependent, notice that the equation

$$
{x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2}=\mathbf{0}
$$

has the solution ${x}_{1}=5$ and ${x}_{2}=-1,$ which is different from ${x}_{1}={x}_{2}=\mathbf{0}.$ Therefore, the set is linearly dependent.

Answer selection: \begin{bmatrix}5 \\ -20 \\ 10\end{bmatrix}

Question 17592186241026 — question.difficulty/easy

The set $\{{\mathbf{a}}_{\mathbf{1}},{\mathbf{a}}_{\mathbf{2}}\}$ is linearly dependent. Which of the following vectors could be ${\mathbf{a}}_{2}$ if
$$
{\mathbf{a}}_{\mathbf{1}}=\begin{bmatrix}-1 \\ 3\end{bmatrix}?
$$

Solution: We say that two vectors ${\mathbf{v}}_{1}$ and ${\mathbf{v}}_{2}$ are *linearly independent* if the only solution to the equation

$$
{x}_{1}{\mathbf{v}}_{1}+{x}_{2}{\mathbf{v}}_{2}=\mathbf{0}
$$

is ${x}_{1}={x}_{2}=\mathbf{0}.$ Otherwise, the vectors are *linearly dependent*.

A set containing *only two* vectors is linearly *dependent* if and only if the two vectors are parallel.

From the given options, the correct answer is

$$
{\mathbf{a}}_{2}=\begin{bmatrix}2 \\ -6\end{bmatrix}.
$$

To see why, notice that 

$$
\begin{bmatrix}2 \\ -6\end{bmatrix}=(-2)\begin{bmatrix}-1 \\ 3\end{bmatrix}=-2{\mathbf{a}}_{1}.
$$

This way, we have

$$
\begin{aligned}2{\mathbf{a}}_{1}-2{\mathbf{a}}_{1} & =\mathbf{0} \\ 2{\mathbf{a}}_{1}+{\mathbf{a}}_{2} & =\mathbf{0}.\end{aligned}
$$

In other words, the vectors ${\mathbf{a}}_{1}$ and ${\mathbf{a}}_{2}$ are parallel.

To see why this means that ${\mathbf{a}}_{1}$ and ${\mathbf{a}}_{2}$ are linearly dependent, we notice that the equation

$$
{x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2}=\mathbf{0}
$$

has the solution ${x}_{1}=2$ and ${x}_{2}=1,$ which is different from ${x}_{1}={x}_{2}=\mathbf{0}.$ Therefore, the set is linearly dependent.

Answer selection: \begin{bmatrix}2 \\ -6\end{bmatrix}

### Identifying Linearly Independent Sets by Inspection (22 captured questions)

Question 17592186120147 — question.difficulty/hard

Consider the following vectors:

$$
{\mathbf{a}}_{1}=\begin{bmatrix}1 \\ -1 \\ 2\end{bmatrix},\,{\mathbf{a}}_{2}=\begin{bmatrix}3 \\ 0 \\ 0\end{bmatrix},\,{\mathbf{a}}_{3}=\begin{bmatrix}1 \\ 2 \\ 0\end{bmatrix}.
$$

Which of the following statements are true?

Select all that apply.

Solution: We say that three vectors ${\mathbf{v}}_{1},{\mathbf{v}}_{2}$ and ${\mathbf{v}}_{3}$ are *linearly independent* if the only solution to the equation

$$
{x}_{1}{\mathbf{v}}_{1}+{x}_{2}{\mathbf{v}}_{2}+{x}_{3}{\mathbf{v}}_{3}=\mathbf{0}
$$

is ${x}_{1}={x}_{2}={x}_{3}=\mathbf{0}.$ Otherwise, the vectors are *linearly dependent*.

With that in mind, let's look at each statement in turn.

- Statement $2{\mathbf{a}}_{1}-{\mathbf{a}}_{2}+{\mathbf{a}}_{3}=\mathbf{0}.$ is false. Indeed:

$$
\begin{aligned}2{\mathbf{a}}_{1}-{\mathbf{a}}_{2}+{\mathbf{a}}_{3} & =2\begin{bmatrix}1 \\ -1 \\ 2\end{bmatrix}-\begin{bmatrix}3 \\ 0 \\ 0\end{bmatrix}+\begin{bmatrix}1 \\ 2 \\ 0\end{bmatrix} \\  & =\begin{bmatrix}2 \\ -2 \\ 4\end{bmatrix}-\begin{bmatrix}3 \\ 0 \\ 0\end{bmatrix}+\begin{bmatrix}1 \\ 2 \\ 0\end{bmatrix} \\  & =\begin{bmatrix}2-3+1 \\ -2-0+2 \\ 4-0+0\end{bmatrix} \\  & =\begin{bmatrix}0 \\ 0 \\ 4\end{bmatrix} \\  & \ne \mathbf{0}\end{aligned}
$$

- Statement “${x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2}+{x}_{3}{\mathbf{a}}_{3}=\mathbf{0}$ only if ${x}_{1}={x}_{2}={x}_{3}=\mathbf{0}.$” is true. The equation ${x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2}+{x}_{3}{\mathbf{a}}_{3}=\mathbf{0}$ corresponds to the system

$$
\left\{\begin{aligned}{x}_{1}+3{x}_{2}+{x}_{3} &=\mathbf{0} \\ -{x}_{1}+2{x}_{3} &=\mathbf{0} \\ 2{x}_{1} &=\mathbf{0}.\end{aligned}\right.
$$

Solving this system using back substitution, we find that the solution is ${x}_{1}={x}_{2}={x}_{3}=\mathbf{0}.$

- Statement “The set $\{{\mathbf{a}}_{1},{\mathbf{a}}_{2},{\mathbf{a}}_{3}\}$ is linearly independent” is true. Since statement “${x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2}+{x}_{3}{\mathbf{a}}_{3}=\mathbf{0}$ only if ${x}_{1}={x}_{2}={x}_{3}=\mathbf{0}.$” is true, the set $\{{\mathbf{a}}_{1},{\mathbf{a}}_{2},{\mathbf{a}}_{3}\}$ is linearly independent.

Therefore, the correct answer is “${x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2}+{x}_{3}{\mathbf{a}}_{3}=\mathbf{0}$ only if ${x}_{1}={x}_{2}={x}_{3}=\mathbf{0}.$”; “The set $\{{\mathbf{a}}_{1},{\mathbf{a}}_{2},{\mathbf{a}}_{3}\}$ is linearly independent” only.

Answer $2{\mathbf{a}}_{1}-{\mathbf{a}}_{2}+{\mathbf{a}}_{3}=\mathbf{0}.$: false

Answer ${x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2}+{x}_{3}{\mathbf{a}}_{3}=\mathbf{0}$ only if ${x}_{1}={x}_{2}={x}_{3}=\mathbf{0}.$: true

Answer The set $\{{\mathbf{a}}_{1},{\mathbf{a}}_{2},{\mathbf{a}}_{3}\}$ is linearly independent.: true

Question 17592186120148 — question.difficulty/easy

Consider the following vectors:

$$
{\mathbf{a}}_{1}=\begin{bmatrix}2 \\ 0 \\ 3\end{bmatrix},\,{\mathbf{a}}_{2}=\begin{bmatrix}1 \\ 1 \\ 0\end{bmatrix}
$$

Which of the following statements are true?

Select all that apply.

Solution: We say that two vectors ${\mathbf{v}}_{1}$ and ${\mathbf{v}}_{2}$ are *linearly independent* if the only solution to the equation

$$
{x}_{1}{\mathbf{v}}_{1}+{x}_{2}{\mathbf{v}}_{2}=\mathbf{0}
$$

is ${x}_{1}={x}_{2}=\mathbf{0}.$ Otherwise, the vectors are *linearly dependent*.

With that in mind, let's look at each statement in turn.

- Statement ${\mathbf{a}}_{1}-2{\mathbf{a}}_{2}=\mathbf{0}.$ is false. Indeed:

$$
\begin{aligned}{\mathbf{a}}_{1}-2{\mathbf{a}}_{2} & =\begin{bmatrix}2 \\ 0 \\ 3\end{bmatrix}-2\begin{bmatrix}1 \\ 1 \\ 0\end{bmatrix} \\  & =\begin{bmatrix}2 \\ 0 \\ 3\end{bmatrix}-\begin{bmatrix}2 \\ 2 \\ 0\end{bmatrix} \\  & =\begin{bmatrix}0 \\ -2 \\ 3\end{bmatrix} \\  & \ne \mathbf{0}\end{aligned}
$$

- Statement “${x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2}=\mathbf{0}$ only if ${x}_{1}={x}_{2}=\mathbf{0}.$” is true. The equation ${x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2}=\mathbf{0}$ corresponds to the system

$$
\left\{\begin{aligned}2{x}_{1}+{x}_{2} &=\mathbf{0} \\ {x}_{2} &=\mathbf{0} \\ 3{x}_{1} &=\mathbf{0}.\end{aligned}\right.
$$

Solving this system using back substitution, we find that the solution is ${x}_{1}={x}_{2}=\mathbf{0}.$

- Statement “The set $\{{\mathbf{a}}_{1},{\mathbf{a}}_{2}\}$ is linearly independent” is true. Since statement “${x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2}=\mathbf{0}$ only if ${x}_{1}={x}_{2}=\mathbf{0}.$” is true, the set $\{{\mathbf{a}}_{1},{\mathbf{a}}_{2}\}$ is linearly independent.

Therefore, the correct answer is “${x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2}=\mathbf{0}$ only if ${x}_{1}={x}_{2}=\mathbf{0}.$”; “The set $\{{\mathbf{a}}_{1},{\mathbf{a}}_{2}\}$ is linearly independent” only.

Answer ${\mathbf{a}}_{1}-2{\mathbf{a}}_{2}=\mathbf{0}.$: false

Answer ${x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2}=\mathbf{0}$ only if ${x}_{1}={x}_{2}=\mathbf{0}.$: true

Answer The set $\{{\mathbf{a}}_{1},{\mathbf{a}}_{2}\}$ is linearly independent.: true

Question 17592186120149 — question.difficulty/moderate

Consider the following vectors:

$$
{\mathbf{a}}_{1}=\begin{bmatrix}1 \\ 2 \\ 0\end{bmatrix},\,{\mathbf{a}}_{2}=\begin{bmatrix}1 \\ 0 \\ 2\end{bmatrix},\,{\mathbf{a}}_{3}=\begin{bmatrix}1 \\ 1 \\ 1\end{bmatrix}.
$$

Which of the following statements are true?

Select all that apply.

Solution: We say that three vectors ${\mathbf{v}}_{1},{\mathbf{v}}_{2}$ and ${\mathbf{v}}_{3}$ are *linearly independent* if the only solution to the equation

$$
{x}_{1}{\mathbf{v}}_{1}+{x}_{2}{\mathbf{v}}_{2}+{x}_{3}{\mathbf{v}}_{3}=\mathbf{0}
$$

is ${x}_{1}={x}_{2}={x}_{3}=\mathbf{0}.$ Otherwise, the vectors are *linearly dependent*.

With that in mind, let's look at each statement in turn.

- Statement ${\mathbf{a}}_{1}+{\mathbf{a}}_{2}-2{\mathbf{a}}_{3}=\mathbf{0}.$ is true. Indeed:

$$
\begin{aligned}{\mathbf{a}}_{1}+{\mathbf{a}}_{2}-2{\mathbf{a}}_{3} & =\begin{bmatrix}1 \\ 2 \\ 0\end{bmatrix}+\begin{bmatrix}1 \\ 0 \\ 2\end{bmatrix}-2\begin{bmatrix}1 \\ 1 \\ 1\end{bmatrix} \\  & =\begin{bmatrix}1 \\ 2 \\ 0\end{bmatrix}+\begin{bmatrix}1 \\ 0 \\ 2\end{bmatrix}-\begin{bmatrix}2 \\ 2 \\ 2\end{bmatrix} \\  & =\begin{bmatrix}1+1-2 \\ 2+0-2 \\ 0+2-2\end{bmatrix} \\  & =\begin{bmatrix}0 \\ 0 \\ 0\end{bmatrix} \\  & =\mathbf{0}\end{aligned}
$$

- Statement “${x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2}+{x}_{3}{\mathbf{a}}_{3}=\mathbf{0}$ only if ${x}_{1}={x}_{2}={x}_{3}=\mathbf{0}.$” is false. Since statement ${\mathbf{a}}_{1}+{\mathbf{a}}_{2}-2{\mathbf{a}}_{3}=\mathbf{0}.$ is true, we have ${x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2}+{x}_{3}{\mathbf{a}}_{3}=\mathbf{0}$ for ${x}_{1}={x}_{2}=1$ and ${x}_{3}=-2.$

- Statement “The set $\{{\mathbf{a}}_{1},{\mathbf{a}}_{2},{\mathbf{a}}_{3}\}$ is linearly independent” is false. Since statement “${x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2}+{x}_{3}{\mathbf{a}}_{3}=\mathbf{0}$ only if ${x}_{1}={x}_{2}={x}_{3}=\mathbf{0}.$” is false, the set $\{{\mathbf{a}}_{1},{\mathbf{a}}_{2},{\mathbf{a}}_{3}\}$ is linearly *dependent*.

Therefore, the correct answer is ${\mathbf{a}}_{1}+{\mathbf{a}}_{2}-2{\mathbf{a}}_{3}=\mathbf{0}.$ only.

Answer ${\mathbf{a}}_{1}+{\mathbf{a}}_{2}-2{\mathbf{a}}_{3}=\mathbf{0}.$: true

Answer ${x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2}+{x}_{3}{\mathbf{a}}_{3}=\mathbf{0}$ only if ${x}_{1}={x}_{2}={x}_{3}=\mathbf{0}.$: false

Answer The set $\{{\mathbf{a}}_{1},{\mathbf{a}}_{2},{\mathbf{a}}_{3}\}$ is linearly independent.: false

### Identifying Linearly Independent and Dependent Sets Using Row Reduction (26 captured questions)

Question 17592186120300 — question.difficulty/moderate

Consider the following vectors:

$$
{\mathbf{a}}_{1}=\begin{bmatrix}1 \\ 1 \\ 0\end{bmatrix},\,{\mathbf{a}}_{2}=\begin{bmatrix}-2 \\ 1 \\ 3\end{bmatrix},\,{\mathbf{a}}_{3}=\begin{bmatrix}1 \\ 2 \\ 1\end{bmatrix}.
$$

Assume that ${x}_{1},{x}_{2},$ and ${x}_{3}$ are real numbers. Which of the following statements are true?

Select all that apply.

Solution: We say that three vectors ${\mathbf{v}}_{1},{\mathbf{v}}_{2},$ and ${\mathbf{v}}_{3}$ are *linearly independent* if the only solution to the equation

$$
{x}_{1}{\mathbf{v}}_{1}+{x}_{2}{\mathbf{v}}_{2}+{x}_{3}{\mathbf{v}}_{3}=\mathbf{0}
$$

is ${x}_{1}={x}_{2}={x}_{3}=\mathbf{0}.$ Otherwise, the vectors are *linearly dependent*.

With that in mind, let's examine our statements.

The equation ${x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2}+{x}_{3}{\mathbf{a}}_{3}=\mathbf{0}$ corresponds to the system

$$
\left\{\begin{aligned}{x}_{1}-2{x}_{2}+{x}_{3} &=\mathbf{0} \\ {x}_{1}+{x}_{2}+2{x}_{3} &=\mathbf{0} \\ 3{x}_{2}+{x}_{3} &=\mathbf{0}.\end{aligned}\right.
$$

To solve the system, we create its augmented matrix and reduce it using Gaussian elimination:

$$
\begin{aligned}M & =\left[\begin{array}{ccc|c}1 & -2 & 1 & 0 \\ 1 & 1 & 2 & 0 \\ 0 & 3 & 1 & 0\end{array}\right] & {R}_{2} & :={R}_{2}+(-1){R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -2 & 1 & 0 \\ 0 & 3 & 1 & 0 \\ 0 & 3 & 1 & 0\end{array}\right] & {R}_{3} & :={R}_{3}+(-1){R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & -2 & 1 & 0 \\ 0 & 3 & 1 & 0 \\ 0 & 0 & 0 & 0\end{array}\right]\end{aligned}
$$

From the matrix above, we conclude that the basic variables are ${x}_{1}$ and ${x}_{2}$, while ${x}_{3}$ is the free variable. 

Since there is one free variable, the equation ${x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2}+{x}_{3}{\mathbf{a}}_{3}=\mathbf{0}$ has an infinite number of nonzero solutions, which means that the vectors are linearly dependent. 

Therefore, statements “The equation ${x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2}+{x}_{3}{\mathbf{a}}_{3}=\mathbf{0}$ has only the trivial solution ${x}_{1}={x}_{2}={x}_{3}=\mathbf{0}.$” and “The vectors ${\mathbf{a}}_{1},{\mathbf{a}}_{2},$ and ${\mathbf{a}}_{3}$ are linearly independent” are false, while statement “The vectors ${\mathbf{a}}_{1},{\mathbf{a}}_{2},$ and ${\mathbf{a}}_{3}$ are linearly dependent” is true.

Answer None of the above: false

Answer The equation ${x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2}+{x}_{3}{\mathbf{a}}_{3}=\mathbf{0}$ has only the trivial solution ${x}_{1}={x}_{2}={x}_{3}=\mathbf{0}.$: false

Answer The vectors ${\mathbf{a}}_{1},{\mathbf{a}}_{2},$ and ${\mathbf{a}}_{3}$ are linearly dependent.: true

Answer The vectors ${\mathbf{a}}_{1},{\mathbf{a}}_{2},$ and ${\mathbf{a}}_{3}$ are linearly independent.: false

Question 17592186120318 — question.difficulty/moderate

Consider the following vectors:

$$
{\mathbf{a}}_{1}=\begin{bmatrix}1 \\ 2 \\ 0\end{bmatrix},\,{\mathbf{a}}_{2}=\begin{bmatrix}-2 \\ 3 \\ 7\end{bmatrix},\,{\mathbf{a}}_{3}=\begin{bmatrix}2 \\ 1 \\ -3\end{bmatrix}.
$$

Assume that ${x}_{1},{x}_{2},$ and ${x}_{3}$ are real numbers. Which of the following statements are true?

Select all that apply.

Solution: We say that three vectors ${\mathbf{v}}_{1},{\mathbf{v}}_{2},$ and ${\mathbf{v}}_{3}$ are *linearly independent* if the only solution to the equation

$$
{x}_{1}{\mathbf{v}}_{1}+{x}_{2}{\mathbf{v}}_{2}+{x}_{3}{\mathbf{v}}_{3}=\mathbf{0}
$$

is ${x}_{1}={x}_{2}={x}_{3}=\mathbf{0}.$ Otherwise, the vectors are *linearly dependent*.

With that in mind, let's examine our statements.

The equation ${x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2}+{x}_{3}{\mathbf{a}}_{3}=\mathbf{0}$ corresponds to the system 

$$
\left\{\begin{aligned}{x}_{1}-2{x}_{2}+2{x}_{3} &=\mathbf{0} \\ 2{x}_{1}+3{x}_{2}+{x}_{3} &=\mathbf{0} \\ 7{x}_{2}-3{x}_{3} &=\mathbf{0}.\end{aligned}\right.
$$

To solve the system, we create its augmented matrix and reduce it using Gaussian elimination:

$$
\begin{aligned}M & =\left[\begin{array}{ccc|c}1 & -2 & 2 & 0 \\ 2 & 3 & 1 & 0 \\ 0 & 7 & -3 & 0\end{array}\right] & {R}_{2} & :={R}_{2}+(-2){R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -2 & 2 & 0 \\ 0 & 7 & -3 & 0 \\ 0 & 7 & -3 & 0\end{array}\right] & {R}_{3} & :={R}_{3}+(-1){R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & -2 & 2 & 0 \\ 0 & 7 & -3 & 0 \\ 0 & 0 & 0 & 0\end{array}\right]\end{aligned}
$$

From the matrix above, we conclude that the basic variables are ${x}_{1}$ and ${x}_{2}$, while ${x}_{3}$ is the free variable. 

Since there is one free variable, the equation ${x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2}+{x}_{3}{\mathbf{a}}_{3}=\mathbf{0}$ has an infinite number of nonzero solutions, which means that the vectors are linearly dependent. 

Therefore, statement “The vectors ${\mathbf{a}}_{1},{\mathbf{a}}_{2},$ and ${\mathbf{a}}_{3}$ are linearly independent” is false, while statements “The equation ${x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2}+{x}_{3}{\mathbf{a}}_{3}=\mathbf{0}$  has an infinite number of nonzero solutions” and “The vectors ${\mathbf{a}}_{1},{\mathbf{a}}_{2},$ and ${\mathbf{a}}_{3}$ are linearly dependent” are true.

Answer None of the above: false

Answer The equation ${x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2}+{x}_{3}{\mathbf{a}}_{3}=\mathbf{0}$  has an infinite number of nonzero solutions.: true

Answer The vectors ${\mathbf{a}}_{1},{\mathbf{a}}_{2},$ and ${\mathbf{a}}_{3}$ are linearly dependent.: true

Answer The vectors ${\mathbf{a}}_{1},{\mathbf{a}}_{2},$ and ${\mathbf{a}}_{3}$ are linearly independent.: false

Question 17592186241031 — question.difficulty/moderate

Consider the following vectors:

$$
{\mathbf{a}}_{1}=\begin{bmatrix}1 \\ 3 \\ -4\end{bmatrix},\,{\mathbf{a}}_{2}=\begin{bmatrix}3 \\ 10 \\ -12\end{bmatrix},\,{\mathbf{a}}_{3}=\begin{bmatrix}4 \\ 8 \\ -16\end{bmatrix}.
$$

Assume that ${x}_{1},{x}_{2},$ and ${x}_{3}$ are real numbers. Which of the following statements are true?

Select all that apply.

Solution: We say that three vectors ${\mathbf{v}}_{1},{\mathbf{v}}_{2},$ and ${\mathbf{v}}_{3}$ are *linearly independent* if the only solution to the equation

$$
{x}_{1}{\mathbf{v}}_{1}+{x}_{2}{\mathbf{v}}_{2}+{x}_{3}{\mathbf{v}}_{3}=\mathbf{0}
$$

is ${x}_{1}={x}_{2}={x}_{3}=\mathbf{0}.$ Otherwise, the vectors are *linearly dependent*.

With that in mind, let's examine our statements.

The equation ${x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2}+{x}_{3}{\mathbf{a}}_{3}=\mathbf{0}$ corresponds to the system

$$
\left\{\begin{aligned}{x}_{1}+3{x}_{2}+4{x}_{3} &=\mathbf{0} \\ 3{x}_{1}+10{x}_{2}+8{x}_{3} &=\mathbf{0} \\ -4{x}_{1}-12{x}_{2}-16{x}_{3} &=\mathbf{0}.\end{aligned}\right.
$$

To solve the system, we create its augmented matrix and reduce it using Gaussian elimination:

$$
\begin{aligned}M & =\left[\begin{array}{ccc|c}1 & 3 & 4 & 0 \\ 3 & 10 & 8 & 0 \\ -4 & -12 & -16 & 0\end{array}\right] & {R}_{2} & :={R}_{2}+(-3){R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 3 & 4 & 0 \\ 0 & 1 & -4 & 0 \\ -4 & -12 & -16 & 0\end{array}\right] & {R}_{3} & :={R}_{3}+4{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 3 & 4 & 0 \\ 0 & 1 & -4 & 0 \\ 0 & 0 & 0 & 0\end{array}\right]\end{aligned}
$$

From the matrix above, we conclude that the basic variables are ${x}_{1}$ and ${x}_{2}$, while ${x}_{3}$ is the free variable. 

Since there is one free variable, the equation ${x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2}+{x}_{3}{\mathbf{a}}_{3}=\mathbf{0}$ has an infinite number of nonzero solutions, which means that the vectors are linearly dependent. 

Therefore, statements “The equation ${x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2}+{x}_{3}{\mathbf{a}}_{3}=\mathbf{0}$ has only the trivial solution ${x}_{1}={x}_{2}={x}_{3}=\mathbf{0}.$” and “The vectors ${\mathbf{a}}_{1},{\mathbf{a}}_{2},$ and ${\mathbf{a}}_{3}$ are linearly independent” are false, while statement “The vectors ${\mathbf{a}}_{1},{\mathbf{a}}_{2},$ and ${\mathbf{a}}_{3}$ are linearly dependent” is true.

Answer The equation ${x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2}+{x}_{3}{\mathbf{a}}_{3}=\mathbf{0}$ has only the trivial solution ${x}_{1}={x}_{2}={x}_{3}=\mathbf{0}.$: false

Answer The vectors ${\mathbf{a}}_{1},{\mathbf{a}}_{2},$ and ${\mathbf{a}}_{3}$ are linearly dependent.: true

Answer The vectors ${\mathbf{a}}_{1},{\mathbf{a}}_{2},$ and ${\mathbf{a}}_{3}$ are linearly independent.: false
