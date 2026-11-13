# 17592186049881 The Four Fundamental Subspaces of a Matrix

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186135110 — Introduction

When considering an $m \times n$ matrix $A$ as a linear transformation

$$
\mathbb{R}^n \xrightarrow{\quad A \quad} \mathbb{R}^m,
$$

there are **four fundamental subspaces** that naturally occur. The first two are as follows:

- The **column space** of $A,$ denoted $\text{Col}(A),$ is a subspace of $\mathbb{R}^m.$ This is the set of all linear combinations of the columns of $A.$

- The **null space** of $A,$ denoted $\text{Null}(A),$ is a subspace of $\mathbb{R}^n.$ This is the set of all vectors in $\mathbb{R}^n$ that, when pre-multiplied by $A,$ result in the zero-vector $\mathbf{0}.$

Now, notice that the transpose $A^T$ is an $n \times m$ matrix and can be considered as the transformation 

$$
\mathbb{R}^m \xrightarrow{\quad A^T \quad} \mathbb{R}^n.
$$

So, we have similar subspaces for the transpose $A^T{:}$

- The column space of $A^T,$ denoted $\text{Col}(A^T),$ is a subspace of $\mathbb{R}^n.$ We call this the **row space** of $A$ since the span of the columns of $A^T$ is equivalent to the span of the rows of $A.$

- The null space of $A^T,$ denoted $\text{Null}(A^T),$ is a subspace of $\mathbb{R}^m.$ We call this the **left null space** of $A$ since it is equivalent to the set of all vectors $\mathbf y\in\mathbb R^m$ such that $\mathbf y^T A = \mathbf{0}.$

Let's discuss how these spaces relate to each other:

- We have two subspaces in $\mathbb{R}^n$ that are orthogonal complements of each other:

$$
\text{Col}(A^T) = \text{Null}(A)^\perp
$$

- We have two subspaces in $\mathbb{R}^m$ that are orthogonal complements of each other:

$$
\text{Col}(A) = \text{Null}(A^T)^\perp
$$

The four fundamental subspaces of a matrix $A$ can be schematically visualized, as shown below.

![](images/ce/ced4191955b6886491bf612c62344d2faf6e7fe8d49884446de0eb86851d22e8.png)

To see why $\text{Col}(A)$ is the orthogonal complement of $\text{Null}(A^T),$ note the following:

- When calculating the product $A^T \mathbf x,$ we multiply each row of $A^T$ by $\mathbf x.$

- Suppose that $\mathbf x\in \text{Null}(A^T).$ Then, by definition, $A^T \mathbf x = \mathbf 0.$

- Thus, $\mathbf x$ must be orthogonal to each row of $A^T.$ Equivalently, this means that $\mathbf x$ is orthogonal to each *column* of $A.$

- Hence, $\text{Null}(A^T)$ is orthogonal to $\text{Col}(A).$

We can deduce that $\text{Null}(A)$ is the orthogonal complement of $\text{Col}(A^T)$ by similar reasoning.



### example 17592186133701 — Identifying an Orthogonal Fundamental Subspaces of a Matrix

Which of the following subspaces must be orthogonal to $\text{Col}(A^T)$ for every matrix $A?$

I. $\text{Null}(A)$

II. $\text{Col}(A)$

III. $\text{Null}(A^T)$

Recall that $\text{Col}(A^T)$ is the row space of $A,$ and consists of all linear combinations of the rows of $A.$

If a vector is orthogonal to every linear combination of the rows of $A,$ it must be orthogonal to each row of $A.$
But notice that when pre-multiplying a vector by $A,$ we multiply each row of $A$ by that vector.
So, $\text{Col}(A^T)$ must be orthogonal to the null space of $A,$ which is $\text{Null}(A).$

Therefore, the correct answer is "I only."

**Note:** In general, the four fundamental subspaces of a matrix $A$ can be schematically visualized, as shown below.

![](images/de/de22dd5b352e1d5be48f4b6ed3b2a4657ae623c1bd288d3464559758ea334af7.png)

### tutorial 17592186135111 — Images Under the Action of a Matrix and Its Transpose

Given an $m \times n$ matrix $A,$ what is the image of $\mathbb{R}^n$ under $A?$

Note that pre-multiplying a vector $\mathbf{x} \in \mathbb{R}^n$ by $A$ gives a linear combination of the columns of $A{:}$
$$
\underbrace{ {\left[ \begin{array}{cccc}| & | & \cdots  & | \\ {a}_{1} & {a}_{2} & \cdots  & {a}_{n} \\ | & | & \cdots  & |\end{array} \right]}}_{\large A}
\cdot
\underbrace{ {\left[ \begin{array}{c}{x}_{1} \\ \vdots  \\ {x}_{n}\end{array} \right]}}_{\large \mathbf{x}}
=
x_1
{\left[ \begin{array}{c}| \\ {a}_{1} \\ |\end{array} \right]}
+
x_2
{\left[ \begin{array}{c}| \\ {a}_{2} \\ |\end{array} \right]}
+\cdots+
x_n
{\left[ \begin{array}{c}| \\ {a}_{n} \\ |\end{array} \right]}
$$

Therefore, by definition, the image of $\mathbb{R}^n$ under the action of $A$ is $\text{Col}(A),$ the column space of $A.$

![](images/db/dbefb436195af5ffa8841f4119054426db50ac2987138a5912991cf42321e0dc.png)

Similarly, pre-multiplying a vector $\mathbf{x} \in \mathbb{R}^m$ by $A^T$ gives a linear combination of the columns of $A^T{:}$
$$
\underbrace{ {\left[ \begin{array}{cccc}| & | & \cdots  & | \\ {a}_{1}^{T} & {a}_{2}^{T} & \cdots  & {a}_{m}^{T} \\ | & | & \cdots  & |\end{array} \right]}}_{\large A^T}
\cdot
\underbrace{ {\left[ \begin{array}{c}{x}_{1} \\ \vdots  \\ {x}_{m}\end{array} \right]}}_{\large \mathbf{x}}
=
x_1
{\left[ \begin{array}{c}| \\ {a}_{1}^{T} \\ |\end{array} \right]}
+
x_2
{\left[ \begin{array}{c}| \\ {a}_{2}^{T} \\ |\end{array} \right]}
+\cdots+
x_m
{\left[ \begin{array}{c}| \\ {a}_{m}^{T} \\ |\end{array} \right]}
$$

Therefore, the image of $\mathbb{R}^m$ under the action of $A^T$ must be $\text{Col}(A^T).$ This is also the row space of $A,$ since a linear combination of the columns of $A^T$ is equivalent to a linear combination of the rows of $A.$

![](images/c8/c82ab88289fc2d35ce354933937d908c54a9839bfa0fd126187a9723c58eeb27.png)

We can use similar reasoning to find the image of the four fundamental subspaces under the appropriate matrix.



### example 17592186133704 — Identifying the Images of the Four Fundamental Subspaces of the Matrix Under Its Action

Let $A$ be a $m \times n$ matrix. What is the image of $\text{Col}(A^T)$ under the action of $A?$

Pre-multiplying a vector $\mathbf{x} \in \mathbb{R}^n$ by $A$ gives a linear combination of the columns of $A{:}$

$$
\underbrace{ {\left[ \begin{array}{cccc}| & | & \cdots  & | \\ {a}_{1} & {a}_{2} & \cdots  & {a}_{n} \\ | & | & \cdots  & |\end{array} \right]}}_{\large A}
\cdot
\underbrace{ {\left[ \begin{array}{c}{x}_{1} \\ \vdots  \\ {x}_{n}\end{array} \right]}}_{\large \mathbf{x}}
=
x_1
{\left[ \begin{array}{c}| \\ {a}_{1} \\ |\end{array} \right]}
+
x_2
{\left[ \begin{array}{c}| \\ {a}_{2} \\ |\end{array} \right]}
+\cdots+
x_n
{\left[ \begin{array}{c}| \\ {a}_{n} \\ |\end{array} \right]}
$$

Therefore, the image of $\mathbb{R}^n$ under the action of $A$ must be $\text{Col}(A),$ the column space of $A.$

Furthermore, since $\text{Null}(A)$ is mapped to the zero vector $\mathbf{0}$ by the definition of the null subspace, the image of its orthogonal complement $\text{Col}(A^T)$ must be $\text{Col}(A).$

This can be schematically visualized, as shown below.

![](images/8b/8b08bdf79d53f312cabd665bcd4669795bd8851dfb33d5e5db6178bd80b24398.png)

### tutorial 17592186135112 — Dimensions of the Four Fundamental Subspaces

Consider an $m \times n$ matrix $A$ with rank $r.$ The dimensions of the four fundamental subspaces of $A$ are as follows:

- $\text{dim}(\text{Col}(A)) = r.$ Since the column space is the span of the columns of $A,$ its dimension is the number of linearly independent columns which, by Gaussian elimination, is $\text{rank}(A)=r.$

- $\text{dim}(\text{Col}(A^T)) = r.$ It can be shown that the dimension of the row space of $A$ also equals $r.$ Therefore, $\text{rank}(A^T)=\text{rank}(A)=r.$

- $\text{dim}(\text{Null}(A)) = n-r.$ Since $\text{Null}(A)$ is the orthogonal complement of $\text{Col}(A^T)$ in $\mathbb{R}^n,$ we have that

$$
\text{dim}(\text{Null}(A)) = \underbrace{\text{dim}(\mathbb{R}^n)}_{n} - \underbrace{\text{dim}(\text{Col}(A^T))}_{r} = n-r.
$$

- $\text{dim}(\text{Null}(A^T)) = m-r.$ Since $\text{Null}(A^T)$ is the orthogonal complement of $\text{Col}(A)$ in $\mathbb{R}^m,$ we have that

$$
\text{dim}(\text{Null}(A^T)) = \underbrace{\text{dim}(\mathbb{R}^m)}_{m} - \underbrace{\text{dim}(\text{Col}(A))}_{r} = m-r.
$$

Let's add these dimensions to the diagram below.

![](images/1c/1c550b87048bba6a7c362f00f09faca74ca9b056a93698436d0994c120971356.png)



### example 17592186133703 — Finding the Dimensions of the Four Fundamental Subspaces of a Matrix

Consider a $8 \times 6$ matrix $A.$ If $\text{dim}(\text{Null}(A)) = 3,$ then find $\text{dim}(\text{Col}(A^T)).$

The four fundamental subspaces of a matrix $A$ can be schematically visualized, as shown below.

![](images/88/889b83fadd26b377c4dd34143c9b16541630c04e90de3d9b005e7147ead75ad5.png)

In our case, we are given that $m=8,$ $n=6,$ and $n-r=3.$ 

Substituting $n=6$ into $n-r=3,$ we can find the rank of $A{:}$

$$
6 - r = 3 
\qquad\Longrightarrow\qquad
r = 3
$$

Therefore, we obtain

$$
\begin{aligned}\text{dim}(\text{Col}({A}^{T})) & =r=3.\end{aligned}
$$

### tutorial 17592186135113 — The Big Picture of the Four Fundamental Subspaces

Let's review what we have learned in this lesson.

If we consider an $m \times n$ matrix $A$ of rank $r$ as a transformation from $\mathbb{R}^n$ to $\mathbb{R}^m,$ then there are four fundamental subspaces of $A{:}$

- $\text{Col}(A)$ and $\text{Null}(A^T)$ are subspaces in $\mathbb{R}^m$ with dimensions $r$ and $m-r,$ respectively.

- $\text{Col}(A^T)$ and $\text{Null}(A)$ are subspaces in $\mathbb{R}^n$ with dimensions $r$ and $n-r,$ respectively.

Furthermore,

- $\text{Col}(A)$ and $\text{Null}(A^T)$ are orthogonal complements in $\mathbb{R}^m,$ and

- $\text{Null}(A)$ and $\text{Col}(A^T)$ are orthogonal complements in $\mathbb{R}^n.$

Finally, we have that

- the image of $\text{Col}(A^T)$ under the action of $A$ is $\text{Col}(A),$ and

- the image of $\text{Col}(A)$ under the action of $A^T$ is $\text{Col}(A^T).$

These facts about the four fundamental subspaces of a matrix $A$ can be schematically visualized, as shown below.

![](images/37/37f633d0bca1a599f7d1658c051f802da5d607d420beeb4bddbef5cd98c366ef.png)



## Representative practice (first three per skill; full bank in practice.json)

### Identifying an Orthogonal Fundamental Subspaces of a Matrix (12 captured questions)

Question 17592186134071 — question.difficulty/easy

Which of the following subspaces must be orthogonal to $\text{Null}(A)$ for every matrix $A?$

Select all that apply.

Solution: Recall that $\text{Null}(A)$ contains all vectors that, when pre-multiplied by $A,$ result in the zero-vector $0.$ 

When pre-multiplying a vector by $A,$ we actually multiply each row of $A$ by that vector. So, $\text{Null}(A)$ must be orthogonal to the row space of $A,$ which is $\text{Col}({A}^{T}).$

Therefore, the correct answer is $\text{Col}({A}^{T})$ only.

**Note:** In general, the four fundamental subspaces of a matrix $A$ can be schematically visualized, as shown below.

![](images/de/de22dd5b352e1d5be48f4b6ed3b2a4657ae623c1bd288d3464559758ea334af7.png)

Answer $\text{Col}(A)$: false

Answer $\text{Col}({A}^{T})$: true

Answer $\text{Null}({A}^{T})$: false

Question 17592186134077 — question.difficulty/moderate

Which of the following subspaces must be orthogonal to $\text{Null}(XY)$ for all compatible matrices $X$ and $Y?$

Select all that apply.

Solution: Recall that $\text{Null}(XY)$ contains all vectors that, when pre-multiplied by $XY,$ result in the zero-vector $0.$ 

When pre-multiplying a vector by $XY,$ we actually multiply each row of $XY$ by that vector. So, $\text{Null}(XY)$ must be orthogonal to the row space of $XY,$ which is $\text{Col}((XY)^{T})=\text{Col}({Y}^{T}\,{X}^{T}).$

Therefore, the correct answer is $\text{Col}({Y}^{T}\,{X}^{T})$ only.

**Note:** In general, the four fundamental subspaces of a matrix $A$ can be schematically visualized, as shown below.

![](images/de/de22dd5b352e1d5be48f4b6ed3b2a4657ae623c1bd288d3464559758ea334af7.png)

Answer $\text{Col}(XY)$: false

Answer $\text{Col}({Y}^{T}\,{X}^{T})$: true

Answer $\text{Null}({Y}^{T}\,{X}^{T})$: false

Question 17592186362710 — question.difficulty/easy

Which of the following subspaces must be orthogonal to $\text{Null}({A}^{T})$ for every matrix $A?$

Select all that apply.

Solution: Recall that $\text{Null}({A}^{T})$ is the left null space of $A.$ This consists of vectors that, when pre-multiplied by ${A}^{T},$ result in the zero-vector $0.$

When pre-multiplying a vector by ${A}^{T},$ we actually multiply each row of ${A}^{T}$, that is, each column of $A$, by that vector. So, $\text{Null}({A}^{T})$ must be orthogonal to the column space of $A,$ which is $\text{Col}(A).$

Therefore, the correct answer is $\text{Col}(A)$ only.

**Note:** In general, the four fundamental subspaces of a matrix $A$ can be schematically visualized, as shown below.

![](images/de/de22dd5b352e1d5be48f4b6ed3b2a4657ae623c1bd288d3464559758ea334af7.png)

Answer $\text{Col}(A)$: true

Answer $\text{Col}({A}^{T})$: false

Answer $\text{Null}(A)$: false

### Identifying the Images of the Four Fundamental Subspaces of the Matrix Under Its Action (12 captured questions)

Question 17592186134072 — question.difficulty/moderate

Let $A$ be a $m\times n$ matrix. What is the image of $\text{Col}(A)$ under the action of ${A}^{T}?$

Solution: First,  notice that ${A}^{T}$ is a $n\times m$ matrix.

Now, pre-multiplying a vector $x\in {R}^{m}$ by ${A}^{T}$ gives a linear combination of the columns of ${A}^{T}:$

$$
\underbrace{\begin{bmatrix}| & | & ⋯ & | \\ {a}_{1}^{T} & {a}_{2}^{T} & ⋯ & {a}_{m}^{T} \\ | & | & ⋯ & |\end{bmatrix}}_{{A}^{T}}\cdot \underbrace{\begin{bmatrix}{x}_{1} \\ ⋮ \\ {x}_{m}\end{bmatrix}}_{x}={x}_{1}\begin{bmatrix}| \\ {a}_{1}^{T} \\ |\end{bmatrix}+{x}_{2}\begin{bmatrix}| \\ {a}_{2}^{T} \\ |\end{bmatrix}+⋯+{x}_{m}\begin{bmatrix}| \\ {a}_{m}^{T} \\ |\end{bmatrix}
$$

Therefore, the image of ${R}^{m}$ under the action of ${A}^{T}$ must be $\text{Col}({A}^{T}),$ the column space of ${A}^{T},$ or equivalently, the row space of $A.$

Furthermore, since $\text{Null}({A}^{T})$ is mapped to the zero vector $0$ by the definition of the null subspace, the image of its orthogonal complement $\text{Col}(({A}^{T})^{T})=\text{Col}(A)$ must be $\text{Col}({A}^{T}).$

This can be schematically visualized, as shown below.

![](images/8c/8ca8508d05e28e4c91b5a7f3c65826ce68b5dacd382bfb1a76f09c09d1d004bf.png)

Answer selection: \text{Col}({A}^{T})

Question 17592186134073 — question.difficulty/easy

Let $A$ be a $m\times n$ matrix. What is the image of ${R}^{n}$ under the action of $A?$

Solution: Pre-multiplying a vector $x\in {R}^{n}$ by $A$ gives a linear combination of the columns of $A:$

$$
\underbrace{\begin{bmatrix}| & | & ⋯ & | \\ {a}_{1} & {a}_{2} & ⋯ & {a}_{n} \\ | & | & ⋯ & |\end{bmatrix}}_{A}\cdot \underbrace{\begin{bmatrix}{x}_{1} \\ ⋮ \\ {x}_{n}\end{bmatrix}}_{x}={x}_{1}\begin{bmatrix}| \\ {a}_{1} \\ |\end{bmatrix}+{x}_{2}\begin{bmatrix}| \\ {a}_{2} \\ |\end{bmatrix}+⋯+{x}_{n}\begin{bmatrix}| \\ {a}_{n} \\ |\end{bmatrix}
$$

Therefore, the image of ${R}^{n}$ under the action of $A$ must be $\text{Col}(A),$ the column space of $A.$

Answer selection: \text{Col}(A)

Question 17592186362743 — question.difficulty/easy

Let $A$ be a $m\times n$ matrix. What is the image of $\text{Null}(A)$ under the action of $A?$

Solution: By definition of the null subspace, $\text{Null}(A)$ is mapped to the zero vector $0$ under the action of $A.$

Answer selection: 0

### Finding the Dimensions of the Four Fundamental Subspaces of a Matrix (12 captured questions)

Question 17592186134070 — question.difficulty/moderate

Consider a $3\times 4$ matrix $A.$ If $\text{dim}(\text{Null}({A}^{T}))=2,$ then $\text{dim}(\text{Col}(A))=$

Solution: The four fundamental subspaces of a matrix $A$ can be schematically visualized, as shown below.

![](images/88/889b83fadd26b377c4dd34143c9b16541630c04e90de3d9b005e7147ead75ad5.png)

In our case, we are given that $m=3,$ $n=4,$ and $m-r=2.$ 

Substituting $m=3$ into $m-r=2,$ we can find the rank of $A:$

$$
(3)-r=2\,⟹\,r=1
$$

Therefore, we obtain

$$
\begin{aligned}\text{dim}(\text{Col}(A)) & =r=1.\end{aligned}
$$

Answer selection: 1

Question 17592186134076 — question.difficulty/moderate

Consider a $7\times 5$ matrix $A.$ If $\text{dim}(\text{Col}(A))=4,$ then $\text{dim}(\text{Null}({A}^{T}))=$

Solution: The four fundamental subspaces of a matrix $A$ can be schematically visualized, as shown below.

![](images/88/889b83fadd26b377c4dd34143c9b16541630c04e90de3d9b005e7147ead75ad5.png)

In our case, we are given that $m=7,$ $n=5,$ and $r=4.$ 

Therefore, we obtain

$$
\begin{aligned}\text{dim}(\text{Null}({A}^{T})) & =m-r=7-4=3.\end{aligned}
$$

Answer selection: 3

Question 17592186362730 — question.difficulty/moderate

Consider a $4\times 3$ matrix $A.$ If $\text{dim}(\text{Null}(A))=1,$ then $\text{dim}(\text{Col}({A}^{T}))=$

Solution: The four fundamental subspaces of a matrix $A$ can be schematically visualized, as shown below.

![](images/88/889b83fadd26b377c4dd34143c9b16541630c04e90de3d9b005e7147ead75ad5.png)

In our case, we are given that $m=4,$ $n=3,$ and $n-r=1.$ 

Substituting $n=3$ into $n-r=1,$ we can find the rank of $A:$

$$
(3)-r=1\,⟹\,r=2
$$

Therefore, we obtain

$$
\begin{aligned}\text{dim}(\text{Col}({A}^{T})) & =r=2.\end{aligned}
$$

Answer selection: 2
