# 17592186048181 The Null Space of a Matrix

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186121039 — Introduction

The **null space** of a matrix $A$ is the set of all the solutions of the equation $A\mathbf{x}= \mathbf{0},$ and is denoted by $\textrm{Null}(A).$ 

To illustrate, let's consider the following matrix:

$$
A={\left[ \begin{array}{cc}2 & 6 \\ 1 & 3\end{array} \right]}
$$

The null space consists of all the solutions of $A\mathbf{x}=\mathbf{0}.$ For example, the vectors ${\left[ \begin{array}{c}- 3 \\ 1\end{array} \right]},$ ${\left[ \begin{array}{c}6 \\ - 2\end{array} \right]},$ and $\begin{bmatrix}-9 \\ 3\end{bmatrix}$ all satisfy the equation $A\mathbf{x}=\mathbf{0},$ so they are all elements of the null space:

$$
{\left[ \begin{array}{c}- 3 \\ 1\end{array} \right]}, {\left[ \begin{array}{c}6 \\ - 2\end{array} \right]}, {\left[ \begin{array}{c}- 9 \\ 3\end{array} \right]} \in \textrm{Null}(A)
$$



### example 17592186119623 — Identifying Whether a Vector Lies in the Null Space of a Given Matrix

The matrix $A$ and vectors $\mathbf{b}_1$, $\mathbf{b}_2$, $\mathbf{b}_3$ are given below. Which of the vectors lie in $\textrm{Null}(A)?$

$$
A={\left[ \begin{array}{cc}3 & - 6 \\ - 5 & 10 \\ - 8 & 16\end{array} \right]}, \quad
\mathbf{b}_1={\left[ \begin{array}{c}3 \\ 6\end{array} \right]}, \quad
\mathbf{b}_2={\left[ \begin{array}{c}6 \\ 3\end{array} \right]}, \quad
\mathbf{b}_3={\left[ \begin{array}{c}1 \\ 3\end{array} \right]}
$$

A vector $\mathbf{b}$ lies in $\textrm{Null}(A)$ if $A\mathbf{b}=\mathbf{0}.$ So, we need to compute the product of $A$ and each of the given vectors and check whether it is equal to $\mathbf{0}\mathbin{:}$

$$
\begin{aligned}A{\mathbf{b}}_{1} & =\begin{bmatrix}3 & -6 \\ -5 & 10 \\ -8 & 16\end{bmatrix}\begin{bmatrix}3 \\ 6\end{bmatrix}=\begin{bmatrix}-27 \\ 45 \\ 72\end{bmatrix}\ne \mathbf{0}\hspace{1em}{\color{red}\times } \\ A{\mathbf{b}}_{2} & =\begin{bmatrix}3 & -6 \\ -5 & 10 \\ -8 & 16\end{bmatrix}\begin{bmatrix}6 \\ 3\end{bmatrix}=\begin{bmatrix}0 \\ 0 \\ 0\end{bmatrix}=\mathbf{0}\hspace{1em}{\color{green}✓} \\ A{\mathbf{b}}_{3} & =\begin{bmatrix}3 & -6 \\ -5 & 10 \\ -8 & 16\end{bmatrix}\begin{bmatrix}1 \\ 3\end{bmatrix}=\begin{bmatrix}-15 \\ 25 \\ 40\end{bmatrix}\ne \mathbf{0}\hspace{1em}{\color{red}\times }\end{aligned}
$$

Therefore, only $\mathbf{b}_2$ lies in $\textrm{Null}(A).$

### example 17592186119624 — Solve a Variable in a Vector Lying in the Null Space of a Given Matrix

Consider the matrix $A={\left[ \begin{array}{ccc}3 & 2 & - 4 \\ - 3 & 3 & - 1 \\ 6 & - 6 & 2\end{array} \right]}$ and the vector $\mathbf{b}={\left[ \begin{array}{c}2 \\ k \\ 3\end{array} \right]}.$ Find the value of $k$ such that $\mathbf{b}\in\textrm{Null}(A).$

If $\mathbf{b} \in \textrm{Null}(A),$ then we must have $A\mathbf{b} = \mathbf{0}.$ Substituting the given information, we get

$$
\begin{aligned}A\mathbf{b} & =\mathbf{0} \\ \begin{bmatrix}3 & 2 & -4 \\ -3 & 3 & -1 \\ 6 & -6 & 2\end{bmatrix}\begin{bmatrix}2 \\ k \\ 3\end{bmatrix} & =\begin{bmatrix}0 \\ 0 \\ 0\end{bmatrix} \\ \begin{bmatrix}6+2k-12 \\ -6+3k-3 \\ 12-6k+6\end{bmatrix} & =\begin{bmatrix}0 \\ 0 \\ 0\end{bmatrix}.\end{aligned}
$$

This corresponds to the system

$$
\left\{\begin{aligned}2k-6 &=0 \\ 3k-9 &=0 \\ -6k+18 &=0\end{aligned}\right.
$$

and for each of these equations, we obtain $k=3.$

### tutorial 17592186121063 — Writing the Null Space using Set-Builder Notation

Let's again consider the following matrix:

$$
A={\left[ \begin{array}{cc}2 & 6 \\ 1 & 3\end{array} \right]}
$$

To find an expression for the null space using set-builder notation, we need to find all the solutions of $A\mathbf{x}=\mathbf{0}.$ Let's start by considering the augmented matrix $[A\,|\, \mathbf{0}]$ and finding its reduced row echelon form as follows:

$$
\begin{aligned}{}[A\,|\,0] & =\left[\begin{array}{cc|c}2 & 6 & 0 \\ 1 & 3 & 0\end{array}\right] & {R}_{1} & :=\frac{1}{2}{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & 3 & 0 \\ 1 & 3 & 0\end{array}\right] & {R}_{2} & :={R}_{2}+(-1){R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & 3 & 0 \\ 0 & 0 & 0\end{array}\right]\end{aligned}
$$

Note that the reduced matrix above has one pivot column (the $1$st column). The second column is not a pivot column.

Now, we convert the reduced matrix back into a system, as follows:

$$
\left\{\begin{aligned}{\color{blue}{x}_{1}}+3{\color{red}{x}_{2}} &=0 \\ 0 &=0\end{aligned}\right.
$$

Here, $\color{blue}x_1$ is a basic variable (it corresponds to the pivot column), while $\color{red}x_2$ is a free variable (it corresponds to the non-pivot column). Because there is a free variable, the system $A\mathbf{x}=\mathbf{0}$ has infinitely many solutions. 

From the first equation we get ${\color{blue}x_1}=-3{\color{red}x_2},$ so the set of all the solutions of $A\mathbf{x}=\mathbf{0}$ is
$$
\textrm{Null}(A) = 
	\left\{  {\left[ \begin{array}{c}- 3 {\color{red}{x}_{2}} \\ {\color{red}{x}_{2}}\end{array} \right]} \: : \: {\color{red}x_2} \in\mathbb{R} \right\}.
$$

**Note:** It is not necessary to consider the full augmented matrix $[A \,|\, \mathbf{0}]$ since the last column won't be changed during the process of reduction. Really, we just need to find the reduced row echelon form of the matrix $A$ and then set up the corresponding system.



### example 17592186119625 — Finding the Null Space of a Given Matrix

Consider the matrix $A={\left[ \begin{array}{cc}4 & - 12 \\ 3 & - 8\end{array} \right]}.$ Find $\textrm{Null}(A).$

We need to solve the equation $A\mathbf{x}=\mathbf{0}.$ First, we find the row echelon form of $A$ as follows:

$$
\begin{aligned}A & =\begin{bmatrix}4 & -12 \\ 3 & -8\end{bmatrix} & {R}_{1} & :=\frac{1}{4}{R}_{1} \\  & ∼\begin{bmatrix}1 & -3 \\ 3 & -8\end{bmatrix} & {R}_{2} & :={R}_{2}+(-3){R}_{1} \\  & ∼\begin{bmatrix}1 & -3 \\ 0 & 1\end{bmatrix}\end{aligned}
$$

This corresponds to the following system:

$$
\left\{\begin{aligned}{x}_{1}-3{x}_{2} &=0 \\ {x}_{2} &=0\end{aligned}\right.
$$

The second equation tells us that $x_2=0.$ Substituting this into the first equation, we get 

$$
\begin{aligned}{x}_{1}-3{x}_{2} & =0 \\ {x}_{1}-3(0) & =0 \\ {x}_{1} & =0.\end{aligned}
$$

So, we conclude that $\mathbf{x} = {\left[ \begin{array}{c}0 \\ 0\end{array} \right]}$ is the only solution to this system.

Therefore, $\textrm{Null}(A) = \left\{ \mathbf{0} \right\}.$

## Representative practice (first three per skill; full bank in practice.json)

### Identifying Whether a Vector Lies in the Null Space of a Given Matrix (12 captured questions)

Question 17592186120323 — question.difficulty/easy

The matrix $A$ and vectors ${\mathbf{b}}_{1}$, ${\mathbf{b}}_{2}$, ${\mathbf{b}}_{3}$ are given below. Which of the vectors lie in $\operatorname{Null}(A)$?

$$
A=\begin{bmatrix}2 & -4 \\ 1 & 5\end{bmatrix},\hspace{1em}{\mathbf{b}}_{1}=\begin{bmatrix}2 \\ -3\end{bmatrix},\hspace{1em}{\mathbf{b}}_{2}=\begin{bmatrix}5 \\ -1\end{bmatrix},\hspace{1em}{\mathbf{b}}_{3}=\begin{bmatrix}-3 \\ 1\end{bmatrix}
$$

Solution: A vector $\mathbf b$ lies in $\operatorname{Null}(A)$ exactly when $A\mathbf b=\mathbf0$. Compute each product:

$$
A\mathbf b_1=\begin{bmatrix}16\\-13\end{bmatrix},\qquad A\mathbf b_2=\begin{bmatrix}14\\0\end{bmatrix},\qquad A\mathbf b_3=\begin{bmatrix}-10\\2\end{bmatrix}.
$$

None of these is the zero vector, so none of the three vectors lies in $\operatorname{Null}(A)$.

Answer selection: None

Question 17592186120334 — None

The matrix $A$ and vectors ${\mathbf{b}}_{1}$, ${\mathbf{b}}_{2}$, ${\mathbf{b}}_{3}$ are given below. Which of the vectors lie in $\operatorname{Null}(A)$?

$$
A=\begin{bmatrix}2 & 4 \\ 4 & 8 \\ 1 & 2\end{bmatrix},\hspace{1em}{\mathbf{b}}_{1}=\begin{bmatrix}-8 \\ 4\end{bmatrix},\hspace{1em}{\mathbf{b}}_{2}=\begin{bmatrix}4 \\ -2\end{bmatrix},\hspace{1em}{\mathbf{b}}_{3}=\begin{bmatrix}-4 \\ 3\end{bmatrix}
$$

Solution: A vector $\mathbf b$ lies in $\operatorname{Null}(A)$ exactly when $A\mathbf b=\mathbf0$. Compute each product:

$$
A\mathbf b_1=\begin{bmatrix}0\\0\\0\end{bmatrix},\qquad A\mathbf b_2=\begin{bmatrix}0\\0\\0\end{bmatrix},\qquad A\mathbf b_3=\begin{bmatrix}4\\8\\2\end{bmatrix}.
$$

Therefore, $\mathbf b_1$ and $\mathbf b_2$ only lie in $\operatorname{Null}(A)$.

Answer selection: $b_{1}$ and $b_{2}$ only

Question 17592186247201 — question.difficulty/easy

The matrix $A$ and vectors ${\mathbf{b}}_{1}$, ${\mathbf{b}}_{2}$, ${\mathbf{b}}_{3}$ are given below. Which of the vectors lie in $\text{Null}(A)?$

$$
A=\begin{bmatrix}2 & -1 \\ -4 & 2 \\ 6 & -3\end{bmatrix},\hspace{1em}{\mathbf{b}}_{1}=\begin{bmatrix}3 \\ 6\end{bmatrix},\hspace{1em}{\mathbf{b}}_{2}=\begin{bmatrix}-1 \\ 3\end{bmatrix},\hspace{1em}{\mathbf{b}}_{3}=\begin{bmatrix}2 \\ 4\end{bmatrix}
$$

Solution: A vector $\mathbf{b}$ lies in $\text{Null}(A)$ if $A\mathbf{b}=\mathbf{0}.$ So, we need to compute the product of $A$ and each of the given vectors and check whether it is equal to $\mathbf{0}:$

$$
\begin{aligned}A{\mathbf{b}}_{1} & =\begin{bmatrix}2 & -1 \\ -4 & 2 \\ 6 & -3\end{bmatrix}\begin{bmatrix}3 \\ 6\end{bmatrix}=\begin{bmatrix}0 \\ 0 \\ 0\end{bmatrix}=\mathbf{0}\hspace{1em}{\color{green}✓} \\ A{\mathbf{b}}_{2} & =\begin{bmatrix}2 & -1 \\ -4 & 2 \\ 6 & -3\end{bmatrix}\begin{bmatrix}-1 \\ 3\end{bmatrix}=\begin{bmatrix}-5 \\ 10 \\ -15\end{bmatrix}\ne \mathbf{0}\hspace{1em}{\color{red}\times } \\ A{\mathbf{b}}_{3} & =\begin{bmatrix}2 & -1 \\ -4 & 2 \\ 6 & -3\end{bmatrix}\begin{bmatrix}2 \\ 4\end{bmatrix}=\begin{bmatrix}0 \\ 0 \\ 0\end{bmatrix}=\mathbf{0}\hspace{1em}{\color{green}✓}\end{aligned}
$$

Therefore, only ${\mathbf{b}}_{1}$ and ${\mathbf{b}}_{3}$ lie in $\text{Null}(A).$

Answer selection: ${b}_{1}$ and ${b}_{3}$ only

### Solve a Variable in a Vector Lying in the Null Space of a Given Matrix (16 captured questions)

Question 17592186120333 — question.difficulty/easy

Consider the matrix $A=\begin{bmatrix}3 & -1 \\ -12 & 4 \\ 9 & -3\end{bmatrix}$ and the vector $\mathbf{b}=\begin{bmatrix}k \\ -6\end{bmatrix}.$ Find the value of $k$ such that $\mathbf{b}\in \text{Null}(A).$

Solution: If $\mathbf{b}\in \text{Null}(A),$ then we must have $A\mathbf{b}=\mathbf{0}.$ Substituting the given information, we get

$$
\begin{aligned}A\mathbf{b} & =\mathbf{0} \\ \begin{bmatrix}3 & -1 \\ -12 & 4 \\ 9 & -3\end{bmatrix}\begin{bmatrix}k \\ -6\end{bmatrix} & =\begin{bmatrix}0 \\ 0 \\ 0\end{bmatrix} \\ \begin{bmatrix}3k+6 \\ -12k-24 \\ 9k+18\end{bmatrix} & =\begin{bmatrix}0 \\ 0 \\ 0\end{bmatrix}.\end{aligned}
$$

This corresponds to the system

$$
\left\{\begin{aligned}3k+6 &=0 \\ -12k-24 &=0 \\ 9k+18 &=0\end{aligned}\right.
$$

and for each of these equations, we obtain $k=-2.$

Answer selection: -2

Question 17592186120368 — question.difficulty/easy

Consider the matrix $A=\begin{bmatrix}0 & 3 & -15 \\ -1 & 1 & -3\end{bmatrix}$ and the vector $\mathbf{b}=\begin{bmatrix}2 \\ k \\ 1\end{bmatrix}.$ Find the value of $k$ such that $\mathbf{b}\in \text{Null}(A).$

Solution: If $\mathbf{b}\in \text{Null}(A),$ then we must have $A\mathbf{b}=\mathbf{0}.$ Substituting the given information, we get

$$
\begin{aligned}A\mathbf{b} & =\mathbf{0} \\ \begin{bmatrix}0 & 3 & -15 \\ -1 & 1 & -3\end{bmatrix}\begin{bmatrix}2 \\ k \\ 1\end{bmatrix} & =\begin{bmatrix}0 \\ 0\end{bmatrix} \\ \begin{bmatrix}3k-15 \\ -2+k-3\end{bmatrix} & =\begin{bmatrix}0 \\ 0\end{bmatrix}.\end{aligned}
$$

This corresponds to the system

$$
\left\{\begin{aligned}3k-15 &=0 \\ k-5 &=0\end{aligned}\right.
$$

and for each of these equations, we obtain $k=5.$

Answer selection: 5

Question 17592186247206 — question.difficulty/easy

Consider the matrix $A=\begin{bmatrix}3 & -1 & -2 \\ -12 & 4 & 8\end{bmatrix}$ and the vector $\mathbf{b}=\begin{bmatrix}2 \\ 2k \\ 5\end{bmatrix}.$ Find the value of $k$ such that $\mathbf{b}\in \text{Null}(A).$

Solution: If $\mathbf{b}\in \text{Null}(A),$ then we must have $A\mathbf{b}=\mathbf{0}.$ Substituting the given information, we get

$$
\begin{aligned}A\mathbf{b} & =\mathbf{0} \\ \begin{bmatrix}3 & -1 & -2 \\ -12 & 4 & 8\end{bmatrix}\begin{bmatrix}2 \\ 2k \\ 5\end{bmatrix} & =\begin{bmatrix}0 \\ 0\end{bmatrix} \\ \begin{bmatrix}-2k-4 \\ 8k+16\end{bmatrix} & =\begin{bmatrix}0 \\ 0\end{bmatrix}.\end{aligned}
$$

This corresponds to the system

$$
\left\{\begin{aligned}-2k-4 &=0 \\ 8k+16 &=0\end{aligned}\right.
$$

and for each of these equations, we obtain $k=-2.$

Answer selection: -2

### Finding the Null Space of a Given Matrix (13 captured questions)

Question 17592186120324 — question.difficulty/moderate

Consider the matrix $A=\begin{bmatrix}3 & 6 \\ 6 & 12\end{bmatrix}.$ Find $\text{Null}(A).$

Solution: We need to solve the equation $A\mathbf{x}=\mathbf{0}.$ First, we find the row echelon form of $A$ as follows:

$$
\begin{aligned}A & =\begin{bmatrix}3 & 6 \\ 6 & 12\end{bmatrix} & {R}_{1} & :=\frac{1}{3}{R}_{1} \\  & ∼\begin{bmatrix}1 & 2 \\ 6 & 12\end{bmatrix} & {R}_{2} & :={R}_{2}+(-6){R}_{1} \\  & ∼\begin{bmatrix}1 & 2 \\ 0 & 0\end{bmatrix}\end{aligned}
$$

This corresponds to the following system:

$$
\left\{\begin{aligned}{x}_{1}+2{x}_{2} &=0 \\ 0 &=0\end{aligned}\right.
$$

The basic variables are the variables whose coefficients are pivots. In this case, the basic variable is ${x}_{1}$, and we have one free variable, ${x}_{2}.$ That means we need to find ${x}_{1}$ in terms of ${x}_{2}.$

From the first equation we get ${x}_{1}=-2{x}_{2},$ so the set of all the solutions of $A\mathbf{x}=\mathbf{0}$ is

$$
\text{Null}(A)=\left\{\begin{bmatrix}-2{x}_{2} \\ {x}_{2}\end{bmatrix}\hspace{0.222em}:\hspace{0.222em}{x}_{2}\in \mathbb{R}\right\}.
$$

Answer selection: \left\{\begin{bmatrix}-2{x}_{2} \\ {x}_{2}\end{bmatrix}\,:\,{x}_{2}\in R\right\}

Question 17592186120369 — question.difficulty/hard

Consider the matrix $A=\begin{bmatrix}-1 & 3 & -2 \\ 5 & -15 & 10 \\ 2 & -6 & 4\end{bmatrix}.$ Find $\text{Null}(A).$

Solution: We need to solve the equation $A\mathbf{x}=\mathbf{0}.$ First, we find the row echelon form of $A$ as follows:

$$
\begin{aligned}A & =\begin{bmatrix}-1 & 3 & -2 \\ 5 & -15 & 10 \\ 2 & -6 & 4\end{bmatrix} & {R}_{1} & :=(-1){R}_{1} \\  & ∼\begin{bmatrix}1 & -3 & 2 \\ 5 & -15 & 10 \\ 2 & -6 & 4\end{bmatrix} & {R}_{2} & :={R}_{2}+(-5){R}_{1} \\  & ∼\begin{bmatrix}1 & -3 & 2 \\ 0 & 0 & 0 \\ 2 & -6 & 4\end{bmatrix} & {R}_{3} & :={R}_{3}+(-2){R}_{1} \\  & ∼\begin{bmatrix}1 & -3 & 2 \\ 0 & 0 & 0 \\ 0 & 0 & 0\end{bmatrix}\end{aligned}
$$

This corresponds to the following system:

$$
\left\{\begin{aligned}{x}_{1}-3{x}_{2}+2{x}_{3} &=0 \\ 0 &=0 \\ 0 &=0\end{aligned}\right.
$$

The basic variables are the variables whose coefficients are pivots. In this case, the basic variable is ${x}_{1}$, and we have two free variables, ${x}_{2}$ and ${x}_{3}.$ That means we need to find ${x}_{1}$ in terms of ${x}_{2}$  and ${x}_{3}.$

From the first equation we get ${x}_{1}=3{x}_{2}-2{x}_{3},$ so the set of all the solutions of $A\mathbf{x}=\mathbf{0}$ is

$$
\text{Null}(A)=\left\{\begin{bmatrix}3{x}_{2}-2{x}_{3} \\ {x}_{2} \\ {x}_{3}\end{bmatrix}\hspace{0.222em}:\hspace{0.222em}{x}_{2},{x}_{3}\in \mathbb{R}\right\}.
$$

Answer selection: \left\{\begin{bmatrix}3{x}_{2}-2{x}_{3} \\ {x}_{2} \\ {x}_{3}\end{bmatrix}\,:\,{x}_{2},{x}_{3}\in R\right\}

Question 17592186247217 — question.difficulty/moderate

Consider the matrix $A=\begin{bmatrix}5 & 15 \\ 2 & 3\end{bmatrix}.$ Find $\text{Null}(A).$

Solution: We need to solve the equation $A\mathbf{x}=\mathbf{0}.$ First, we find the row echelon form of $A$ as follows:

$$
\begin{aligned}A & =\begin{bmatrix}5 & 15 \\ 2 & 3\end{bmatrix} & {R}_{1} & :=\frac{1}{5}{R}_{1} \\  & ∼\begin{bmatrix}1 & 3 \\ 2 & 3\end{bmatrix} & {R}_{2} & :={R}_{2}-2{R}_{1} \\  & ∼\begin{bmatrix}1 & 3 \\ 0 & -3\end{bmatrix}\end{aligned}
$$

This corresponds to the following system:

$$
\left\{\begin{aligned}{x}_{1}+3{x}_{2} &=0 \\ -3{x}_{2} &=0\end{aligned}\right.
$$

The second equation tells us that ${x}_{2}=0.$ Substituting this into the first equation, we get 

$$
{x}_{1}+3(0)=0\,⟹\,{x}_{1}=0.
$$

So, we conclude that $\mathbf{x}=\begin{bmatrix}0 \\ 0\end{bmatrix}$ is the only solution to this system.

Therefore, $\text{Null}(A)=\{\mathbf{0}\}.$

Answer selection: \left\{0\right\}
