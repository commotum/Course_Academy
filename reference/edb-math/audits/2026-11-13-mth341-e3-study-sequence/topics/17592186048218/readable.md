# 17592186048218 The Dimension of a Span

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186121056 — Introduction

There is something interesting about the bases of a vector space, summarized in the theorem below:

If the vector space $V$ has a basis with $n$ vectors, then any basis of $V$ has exactly $n$ vectors.

The number $n$ of vectors in any basis of $V$ is called the **dimension of the space** $V$ and is denoted $\textrm{dim}(V).$

For example, consider the linear span below:
$$
H = \textrm{Span}\bigg\{
		\underbrace{ {\left[ \begin{array}{c}3 \\ - 1\end{array} \right]}}_{\mathbf{v}_1}, 
		\underbrace{ {\left[ \begin{array}{c}- 3 \\ 1\end{array} \right]}}_{\mathbf{v}_2}, 
		\underbrace{ {\left[ \begin{array}{c}- 6 \\ 5\end{array} \right]}}_{\mathbf{v}_3}
	\bigg\}
$$

We know that, in order to find a basis of the span, we start by creating a matrix whose columns are made up of our vectors, and then we reduce the matrix to row echelon form:

$$
\begin{aligned} & \begin{bmatrix}3 & -3 & -6 \\ -1 & 1 & 5\end{bmatrix} & {R}_{2} & :={R}_{2}+\frac{1}{3}{R}_{1} \\  & ∼\begin{bmatrix}3 & -3 & -6 \\ 0 & 0 & 3\end{bmatrix}\end{aligned}
$$

We see that the matrix above has two pivot columns: the $1$st and the $3$rd columns. This tells us that
$\mathcal{B}=\{ \mathbf{v}_1,\mathbf{v}_3 \}$ is a basis of $H.$

Since $\mathcal{B}$ consists of two vectors, *any basis* of $H$ will also have *exactly* two vectors. So, we have $\textrm{dim}(H)=2.$



### tutorial 17592186121069 — Finite and Infinite-Dimensional Vector Spaces

As defined earlier, the dimension of a vector space $V$ is the number of vectors in any basis of $V$.

However, note that the definition above is only applicable if a vector space has at least one basis with a finite number of elements.

- If a vector space has a basis with a finite number of vectors, then it is called **finite-dimensional**.

- Otherwise, if there is no finite basis, the vector space is called **infinite-dimensional**.

In linear algebra, we mostly consider finite-dimensional vector spaces.



### example 17592186119659 — Finding the Dimension of a Span by Inspection

Determine the dimension of
$$
\textrm{Span}
		\left\{ 
			{\left[ \begin{array}{c}1 \\ 0 \\ 0\end{array} \right]}, 
			{\left[ \begin{array}{c}1 \\ 1 \\ 0\end{array} \right]}, 
			{\left[ \begin{array}{c}1 \\ 1 \\ 0\end{array} \right]} 
		\right\}.
$$

We start by creating a matrix whose columns are made up of our vectors, and then we reduce the matrix to row echelon form:

$$
\begin{aligned}\begin{bmatrix}1 & 1 & 1 \\ 0 & 1 & 1 \\ 0 & 0 & 0\end{bmatrix}\end{aligned}
$$

In this case, our matrix is already in a row echelon form. We see that the matrix above has two pivot columns: the $1$st and the $2$nd columns. This tells us that $\mathcal{B}=\{ \mathbf{v}_1,\mathbf{v}_2 \}$ forms a basis for our span.

Since $\mathcal{B}$ consists of two vectors, any basis of our span will also have *exactly* two vectors. Therefore, the dimension of the span is $2\mathbin{:}$

$$
\textrm{dim} \left( \textrm{Span}
		\left\{ 
			{\left[ \begin{array}{c}1 \\ 0 \\ 0\end{array} \right]}, 
			{\left[ \begin{array}{c}1 \\ 1 \\ 0\end{array} \right]}, 
			{\left[ \begin{array}{c}1 \\ 1 \\ 0\end{array} \right]} 
		\right\} \right) = 2.
$$

### example 17592186119660 — Finding the Dimension of a Span Using Row Reduction

Determine the dimension of
$$
\textrm{Span}
		\left\{ 
			{\left[ \begin{array}{c}2 \\ - 6 \\ 4\end{array} \right]}, 
			{\left[ \begin{array}{c}- 1 \\ 3 \\ - 2\end{array} \right]}, 
			{\left[ \begin{array}{c}5 \\ - 15 \\ 10\end{array} \right]} 
		\right\}.
$$

We start by creating a matrix whose columns are made up of our vectors, and then we reduce the matrix to row echelon form:

$$
\begin{aligned} & \begin{bmatrix}2 & -1 & 5 \\ -6 & 3 & -15 \\ 4 & -2 & 10\end{bmatrix} & {R}_{2} & :={R}_{2}+3{R}_{1} \\  & ∼\begin{bmatrix}2 & -1 & 5 \\ 0 & 0 & 0 \\ 4 & -2 & 10\end{bmatrix} & {R}_{3} & :={R}_{3}+(-2){R}_{1} \\  & ∼\begin{bmatrix}2 & -1 & 5 \\ 0 & 0 & 0 \\ 0 & 0 & 0\end{bmatrix}\end{aligned}
$$

We see that the matrix above has one pivot columns: the $1$st column. This tells us that $\mathcal{B}=\{ \mathbf{v}_1 \}$ forms a basis for our span.

Since $\mathcal{B}$ consists of one vector, any basis of our span will also have *exactly* one vector. Therefore, the dimension of the span is $1\mathbin{:}$

$$
\textrm{dim} \left( \textrm{Span}
		\left\{ 
			{\left[ \begin{array}{c}2 \\ - 6 \\ 4\end{array} \right]}, 
			{\left[ \begin{array}{c}- 1 \\ 3 \\ - 2\end{array} \right]}, 
			{\left[ \begin{array}{c}5 \\ - 15 \\ 10\end{array} \right]} 
		\right\} \right) = 1.
$$

### tutorial 17592186121057 — Geometric Intuition for Finite-Dimensional Vector Spaces

We can build some geometric intuition for finite-dimensional vector spaces. To illustrate, let's find the dimensions of $\{\mathbf{0}\},$ $\mathbb{R},$ $\mathbb{R}^2,$ and $\mathbb{R}^3.$

First, note that $\{\mathbf{0}\}$ can be written as $\mathbb{R}^0,$ and $\mathbb{R}$ can be written as $\mathbb{R}^1.$ We have the following standard bases:

$$
\mathbb{R}^0:
	\big\{
		\textrm{no basis}
	\big\},
	\qquad
	\mathbb{R}^1:
	\big\{
		\underbrace{ {\left[ \begin{array}{c}1\end{array} \right]}}_{\color{blue}\mathbf{i}}
	\big\},
	\qquad
	\mathbb{R}^2:
	\Bigg\{
		\underbrace{ {\left[ \begin{array}{c}1 \\ 0\end{array} \right]}}_{\color{blue}\mathbf{i}}, 
		\underbrace{ {\left[ \begin{array}{c}0 \\ 1\end{array} \right]}}_{\color{blue}\mathbf{j}}
	\Bigg\},
	\qquad
	\mathbb{R}^3:
	\Bigg\{
		\underbrace{ {\left[ \begin{array}{c}1 \\ 0 \\ 0\end{array} \right]}}_{\color{blue}\mathbf{i}}, 
		\underbrace{ {\left[ \begin{array}{c}0 \\ 1 \\ 0\end{array} \right]}}_{\color{blue}\mathbf{j}}, 
		\underbrace{ {\left[ \begin{array}{c}0 \\ 0 \\ 1\end{array} \right]}}_{\color{blue}\mathbf{k}}
	\Bigg\}.
$$

Consequently, we have the following dimensions:

$$
\begin{aligned}\text{dim}({\mathbb{R}}^{0}) &=0,\hspace{1em}\text{dim}({\mathbb{R}}^{1})=1,\hspace{1em}\text{dim}({\mathbb{R}}^{2})=2,\hspace{1em}\text{dim}({\mathbb{R}}^{3})=3.\end{aligned}
$$

Now, let's build some geometric intuition. We can represent the standard bases in the following diagram:

![](images/16/169b5597d89fa32fd09772593cc2a9a330ee12881281dea4e3e43dc6165b9ebd.png)

So, the sequence $\mathbb{R}^0,$ $\mathbb{R}^1,$ $\mathbb{R}^2,$ $\mathbb{R}^3,$ $\ldots$ can be visualized as follows:

![](images/37/379823eca26d43337744a8f4a3872e67ac537a6c193d55e39b5d6761f258f6f5.png)

Notice the following:

- The basis for $\mathbb{R}^0$ is represented geometrically as a $0$-dimensional point.

- The basis for $\mathbb{R}^1$ is represented geometrically as a $1$-dimensional line segment.

- The basis for $\mathbb{R}^2$ is represented geometrically as a $2$-dimensional square.

- The basis for $\mathbb{R}^3$ is represented geometrically as a $3$-dimensional cube.

Unfortunately, we can't visualize dimensions greater than $3,$ but we know that $\mathbb{R}^n$ has the following standard basis consisting of $n$ vectors:

$$
\left\{ {\left[ \begin{array}{c}1 \\ 0 \\ 0 \\ \vdots  \\ 0\end{array} \right]}, {\left[ \begin{array}{c}0 \\ 1 \\ 0 \\ \vdots  \\ 0\end{array} \right]}, \cdots, {\left[ \begin{array}{c}0 \\ 0 \\ \vdots  \\ 0 \\ 1\end{array} \right]} \right\}
$$

Therefore, 

$$
\textrm{dim}(\mathbb{R}^n) = n.
$$



## Representative practice (first three per skill; full bank in practice.json)

### Finding the Dimension of a Span by Inspection (17 captured questions)

Question 17592186120529 — question.difficulty/easy

$$
\displaystyle \text{dim}\left(\text{Span}\left\{\begin{bmatrix}2 \\ 0 \\ 0\end{bmatrix},\begin{bmatrix}0 \\ 1 \\ 0\end{bmatrix},\begin{bmatrix}0 \\ 0 \\ 0\end{bmatrix}\right\}\right)=
$$

Solution: We start by creating a matrix whose columns are made up of our vectors, and then we reduce the matrix to row echelon form:

$$
\begin{aligned}\begin{bmatrix}2 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 0\end{bmatrix}\end{aligned}
$$

In this case, our matrix is already in a row echelon form.

The pivot columns correspond to basis vectors, while the non-pivot columns correspond to linearly dependent vectors that can be removed. Here, the reduced matrix has $2$ pivot columns (or alternatively, $2$ non-zero rows). 

Therefore,
$$
\displaystyle \text{dim}\left(\text{Span}\left\{\begin{bmatrix}2 \\ 0 \\ 0\end{bmatrix},\begin{bmatrix}0 \\ 1 \\ 0\end{bmatrix},\begin{bmatrix}0 \\ 0 \\ 0\end{bmatrix}\right\}\right)=2.
$$

Answer selection: 2

Question 17592186120530 — question.difficulty/moderate

Let ${v}_{1},{v}_{2},{v}_{3}$ be linearly independent vectors, and suppose that the vector $w$ can be written as a linear combination of ${v}_{1},{v}_{2},{v}_{3}.$ Which of the following statements are true?

I. ${v}_{1},{v}_{2},{v}_{3}$ form a basis of $\text{Span}\{{v}_{1},{v}_{2},{v}_{3}\}$

II. $\text{dim}(\text{Span}\{{v}_{1},{v}_{2},{v}_{3}\})=3$

III. $\text{dim}(\text{Span}\{{v}_{1},{v}_{2},{v}_{3},w\})=4$

Solution: Recall that a basis of a vector space $V$ is a set of linearly independent vectors that span $V.$ The dimension of $V$ is the number of vectors in any basis of $V$ (if such a basis exists). 

With that in mind, let's consider each of the statements.

- Statement I is true. Indeed, $\text{Span}\{{v}_{1},{v}_{2},{v}_{3}\}$ is spanned by ${v}_{1},{v}_{2},{v}_{3}$, and we are told that ${v}_{1},{v}_{2},{v}_{3}$ are linearly independent vectors. So, ${v}_{1},{v}_{2},{v}_{3}$ is a basis of the span.

- Statement II is true. Since ${v}_{1},{v}_{2},{v}_{3}$ is a basis of the given span and this basis contains $3$ vectors, we have $\text{dim}(\text{Span}\{{v}_{1},{v}_{2},{v}_{3}\})=3.$

- Statement III is false. We are told that $w$ can be written as a linear combination of ${v}_{1},{v}_{2},{v}_{3}.$ This means that $\text{Span}\{{v}_{1},{v}_{2},{v}_{3},w\}$ is completely spanned by the vectors ${v}_{1},{v}_{2},{v}_{3}$ only. So, $\text{dim}(\text{Span}\{{v}_{1},{v}_{2},{v}_{3},w\})=3$ (not $4$).

Therefore, the correct answer is "I and II only."

Answer selection: I and II only

Question 17592186278261 — question.difficulty/moderate

Let ${v}_{1},{v}_{2},{v}_{3}$ be linearly independent vectors, and suppose that the vector $w$ can be written as a linear combination of ${v}_{1}$ and ${v}_{2}.$ Which of the following statements are true?

Select all that apply.

Solution: Recall that a basis of a vector space $V$ is a set of linearly independent vectors that span $V.$ The dimension of $V$ is the number of vectors in any basis of $V$ (if such a basis exists). 

With that in mind, let's consider each of the statements.

- Statement “${v}_{1},{v}_{2}$ form a basis of $\text{Span}{{v}_{1},{v}_{2},w}$” is true. We are told that $w$ can be written as a linear combination of ${v}_{1},{v}_{2}.$ This means that $\text{Span}{{v}_{1},{v}_{2},w}$ is completely spanned by the vectors ${v}_{1},{v}_{2}$ only. So, ${v}_{1},{v}_{2}$ form a basis of $\text{Span}{{v}_{1},{v}_{2},w}$

- Statement $\text{dim}(\text{Span}{{v}_{1},{v}_{2},{v}_{3},w})=4$ is false. We are told that $w$ can be written as a linear combination of ${v}_{1},{v}_{2},$ and we are told that ${v}_{1},{v}_{2},{v}_{3}$ are linearly independent vectors. This means that $\text{Span}{{v}_{1},{v}_{2},{v}_{3},w}$ is completely spanned by the vectors ${v}_{1},{v}_{2},{v}_{3}$ only. So, ${v}_{1},{v}_{2},{v}_{3}$ is a basis of the span. Therefore, we have $\text{dim}(\text{Span}{{v}_{1},{v}_{2},{v}_{3},w})=3$ (not $4$).

- Statement $\text{dim}(\text{Span}{{v}_{1},{v}_{2}})=3$ is false. Indeed, $\text{Span}{{v}_{1},{v}_{2}}$ is spanned by ${v}_{1},{v}_{2}$, and we are told that ${v}_{1},{v}_{2}$ are linearly independent vectors. So, ${v}_{1},{v}_{2}$ is a basis of the span. Therefore, we have $\text{dim}(\text{Span}{{v}_{1},{v}_{2}})=2$ (not $3$).

Therefore, the correct answer is “${v}_{1},{v}_{2}$ form a basis of $\text{Span}{{v}_{1},{v}_{2},w}$” only.

Answer $\text{dim}(\text{Span}\{{\mathbf{v}}_{1},{\mathbf{v}}_{2},{\mathbf{v}}_{3},\mathbf{w}\})=4$: false

Answer $\text{dim}(\text{Span}\{{\mathbf{v}}_{1},{\mathbf{v}}_{2}\})=3$: false

Answer ${\mathbf{v}}_{1},{\mathbf{v}}_{2}$ form a basis of $\text{Span}\{{\mathbf{v}}_{1},{\mathbf{v}}_{2},\mathbf{w}\}$: true

### Finding the Dimension of a Span Using Row Reduction (17 captured questions)

Question 17592186120365 — question.difficulty/moderate

Determine the dimension of $$
\displaystyle \text{Span}\left\{\begin{bmatrix}2 \\ -2 \\ 1\end{bmatrix},\begin{bmatrix}-2 \\ 1 \\ -1\end{bmatrix},\begin{bmatrix}2 \\ -2 \\ 3\end{bmatrix}\right\}.
$$

Solution: We start by creating a matrix whose columns are made up of our vectors, and then we reduce the matrix to row echelon form:

$$
\begin{aligned} & \begin{bmatrix}2 & -2 & 2 \\ -2 & 1 & -2 \\ 1 & -1 & 3\end{bmatrix} & {R}_{2} & :={R}_{2}+{R}_{1} \\  & ∼\begin{bmatrix}2 & -2 & 2 \\ 0 & -1 & 0 \\ 1 & -1 & 3\end{bmatrix} & {R}_{3} & :={R}_{3}+\left(-\frac{1}{2}\right){R}_{1} \\  & ∼\begin{bmatrix}2 & -2 & 2 \\ 0 & -1 & 0 \\ 0 & 0 & 2\end{bmatrix}\end{aligned}
$$

The pivot columns correspond to basis vectors, while the non-pivot columns correspond to linearly dependent vectors that can be removed. Here, the reduced matrix has $3$ pivot columns (or alternatively, it has exactly $3$ non-zero rows). 

Therefore, the dimension of the span is $3.$

Answer selection: 3

Question 17592186120367 — question.difficulty/easy

$$
\displaystyle \text{dim}\left(\text{Span}{\begin{bmatrix}3 \\ -6\end{bmatrix},\begin{bmatrix}5 \\ -10\end{bmatrix}}\right)=
$$

Solution: We start by creating a matrix whose columns are made up of our vectors, and then we reduce the matrix to row echelon form:

$$
\begin{aligned} & \begin{bmatrix}3 & 5 \\ -6 & -10\end{bmatrix} & {R}_{2} & :={R}_{2}+2{R}_{1} \\  & ∼\begin{bmatrix}3 & 5 \\ 0 & 0\end{bmatrix}\end{aligned}
$$

The pivot columns correspond to basis vectors, while the non-pivot columns correspond to linearly dependent vectors that can be removed. Here, the reduced matrix has $1$ pivot column (or alternatively, it has exactly $1$ non-zero row). 

Therefore, 
$$
\displaystyle \text{dim}\left(\text{Span}{\begin{bmatrix}3 \\ -6\end{bmatrix},\begin{bmatrix}5 \\ -10\end{bmatrix}}\right)=1.
$$

Answer selection: 1

Question 17592186319174 — question.difficulty/easy

$$
\displaystyle \text{dim}\left(\text{Span}\left\{\begin{bmatrix}1 \\ -2\end{bmatrix},\begin{bmatrix}-1 \\ 2\end{bmatrix},\begin{bmatrix}-1 \\ -2\end{bmatrix}\right\}\right)=
$$

Solution: We start by creating a matrix whose columns are made up of our vectors, and then we reduce the matrix to row echelon form:

$$
\begin{aligned} & \begin{bmatrix}1 & -1 & -1 \\ -2 & 2 & -2\end{bmatrix} & {R}_{2} & :={R}_{2}+2{R}_{1} \\  & ∼\begin{bmatrix}1 & -1 & -1 \\ 0 & 0 & -4\end{bmatrix}\end{aligned}
$$

The pivot columns correspond to basis vectors, while the non-pivot columns correspond to linearly dependent vectors that can be removed. Here, the reduced matrix has $2$ pivot columns (or alternatively, it has exactly $2$ non-zero rows). 

Therefore, 
$$
\displaystyle \text{dim}\left(\text{Span}\left\{\begin{bmatrix}1 \\ -2\end{bmatrix},\begin{bmatrix}-1 \\ 2\end{bmatrix},\begin{bmatrix}-1 \\ -2\end{bmatrix}\right\}\right)=2.
$$

Answer selection: 2
