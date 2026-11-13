# 17592186049009 Finding a Basis of the Column Space of a Matrix

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186153352 — Introduction

Remember that the column space of a matrix is the span of its columns. For example, for the matrix

$$
A={\left[ \begin{array}{ccc}1 & 2 & - 1 \\ 3 & 2 & 5\end{array} \right]},
$$

the column space is

$$
\textrm{Col}(A) = \text{Span} \Bigg\{ 
		\underbrace{ {\left[ \begin{array}{c}1 \\ 3\end{array} \right]}}_{\color{black}\mathbf{a}_1}, 
		\underbrace{ {\left[ \begin{array}{c}2 \\ 2\end{array} \right]}}_{\color{black}\mathbf{a}_2},
		\underbrace{ {\left[ \begin{array}{c}- 1 \\ 5\end{array} \right]}}_{\color{black}\mathbf{a}_3}
	\Bigg\}.
$$

So, to find a basis of $\textrm{Col}(A),$ we can apply the usual procedure of converting the matrix $A$ to row echelon form and then picking the pivot columns from the original matrix $A.$



### example 17592186151943 — Finding a Basis of the Column Space of a Matrix

Consider the matrix $A={\left[ \begin{array}{ccc}1 & 2 & - 1 \\ 3 & 2 & 5\end{array} \right]}.$ Find a basis $\mathcal B$ of $\textrm{Col}(A).$

In order to find a basis of $\textrm{Col}(A),$ we need reduce the matrix $A$ to row echelon form:

$$
\begin{aligned}A & =\begin{bmatrix}1 & 2 & -1 \\ 3 & 2 & 5\end{bmatrix} & {R}_{2} & :={R}_{2}+(-3){R}_{1} \\  & ∼\begin{bmatrix}1 & 2 & -1 \\ 0 & -4 & 8\end{bmatrix}\end{aligned}
$$

The pivot columns correspond to linearly independent vectors, while the non-pivot columns correspond to linearly dependent vectors that can be removed. Here, the $1$st and $2$nd columns are pivot columns, while the $3$rd column is a non-pivot column.

Remember that we need to pick the pivot columns from the *original matrix*, not from the reduced one. 

The $1$st and $2$nd columns from the original matrix are $\mathbf{a}_1$ and $\mathbf{a}_2.$ So, a basis of $\textrm{Col}(A)$ is $\{ \mathbf{a}_1, \mathbf{a}_2 \},$ that is to say, 

$$
\mathcal{B} = \Bigg\{ 
		\underbrace{ {\left[ \begin{array}{c}1 \\ 3\end{array} \right]}}_{\color{black}\mathbf{a}_1}, 
		\underbrace{ {\left[ \begin{array}{c}2 \\ 2\end{array} \right]}}_{\color{black}\mathbf{a}_2} 
	\Bigg\}.
$$

### tutorial 17592186153353 — Finding a Particular Linear Combination of Vectors

In the previous example, we computed a basis of $\textrm{Col}(A),$ where 

$$
A={\left[ \begin{array}{ccc}1 & 2 & - 1 \\ 3 & 2 & 5\end{array} \right]}.
$$

The basis that we found previously was

$$
\mathcal{B} = \Bigg\{ 
		\underbrace{ {\left[ \begin{array}{c}1 \\ 3\end{array} \right]}}_{\color{black}\mathbf{a}_1}, 
		\underbrace{ {\left[ \begin{array}{c}2 \\ 2\end{array} \right]}}_{\color{black}\mathbf{a}_2} 
	\Bigg\}.
$$

Therefore, we can write

$$
\textrm{Col}(A) = \textrm{Span}\,\mathcal B
= \textrm{Span}\{\mathbf a_1, \mathbf a_2\}

= 
\textrm{Span} \Bigg\{ 
		{\left[ \begin{array}{c}1 \\ 3\end{array} \right]}, 
		{\left[ \begin{array}{c}2 \\ 2\end{array} \right]}
	\Bigg\}.
$$

The vector $\mathbf{a}_3$ was not included in the basis because the $3$rd column of $A$ was not a pivot column. This means that $\mathbf{a}_3$ can be written as a linear combination of $\mathbf{a}_1$ and $\mathbf{a}_2.$

Now, what if we want to find the exact linear combination of $\mathbf{a}_1$ and $\mathbf{a}_2$ that yields $\mathbf{a}_3?$ That is to say, we want to find $x_1, x_2 \in \mathbb{R}$ such that 

$$
{\color{black}x_1} \underbrace{ {\left[ \begin{array}{c}1 \\ 3\end{array} \right]}}_{\mathbf{a}_1} + {\color{black}x_2} \underbrace{ {\left[ \begin{array}{c}2 \\ 2\end{array} \right]}}_{\mathbf{a}_2} = \underbrace{ {\left[ \begin{array}{c}- 1 \\ 5\end{array} \right]}}_{\mathbf{a}_3}.
$$

This is equivalent to a system with the augmented matrix
$$
\left[
	{\begin{array}{cc|c}1 & 2 & - 1 \\ 3 & 2 & 5\end{array}}
	\right].
$$

If we reduced this matrix to the *reduced* row echelon form, we get

$$
\left[
	{\begin{array}{cc|c}\bbox[3pt,lightgray]{ {\color{blue}1}} & 0 & {\color{red}3} \\ 0 & \bbox[3pt,lightgray]{ {\color{blue}1}} & {\color{red}- 2}\end{array}}
	\right].
$$

Finally, the third column of the *reduced* matrix tells us that $x_1=3$ and $x_2=-2,$ meaning that
$$
\underbrace{ {\left[ \begin{array}{c}- 1 \\ 5\end{array} \right]}}_{\mathbf{a}_3} = {\color{red}3}\cdot \underbrace{ {\left[ \begin{array}{c}1 \\ 3\end{array} \right]}}_{\mathbf{a}_1} + ({\color{red}-2})\cdot \underbrace{ {\left[ \begin{array}{c}2 \\ 2\end{array} \right]}}_{\mathbf{a}_2}.
$$

In general, if the $n$th column of the reduced matrix is a non-pivot column, then the entries in that column tell us the coefficients needed to express $\mathbf{a}_n$ as a linear combination of the pivot columns of the original matrix. 

**Watch out!** The matrix must be written in *reduced* row echelon form (with $1$'s for pivots and $0$'s above and below the pivots), not just in a row echelon form.



### example 17592186151944 — Determining Whether a Given Set Is a Basis of the Column Space of a Matrix With Two Rows

The matrix $A$ is given below. Let $\mathbf{a}_1$, $\mathbf{a}_2$, and $\mathbf{a}_3$ be the respective columns of $A.$ Determine if $\mathcal{B}={ { {\mathbf{a}}_{1} , {\mathbf{a}}_{2}}}$ is a basis of $\textrm{Col}(A).$ 
If that is the case, find $x_1 \cdot x_2$, where $\mathbf{a}_3=x_1\mathbf{a}_1+x_2\mathbf{a}_2.$

$$
A= 
{\left[ \begin{array}{ccc}1 & 2 & 9 \\ 3 & 1 & 17\end{array} \right]}
$$

First, we reduce the matrix $A$ to reduced row echelon form (RREF):

$$
\begin{aligned}A & =\begin{bmatrix}1 & 2 & 9 \\ 3 & 1 & 17\end{bmatrix} & {R}_{2} & :={R}_{2}+(-3){R}_{1} \\  & ∼\begin{bmatrix}1 & 2 & 9 \\ 0 & -5 & -10\end{bmatrix} & {R}_{2} & :=\left(-\frac{1}{5}\right){R}_{2} \\  & ∼\begin{bmatrix}1 & 2 & 9 \\ 0 & 1 & 2\end{bmatrix} & {R}_{1} & :={R}_{1}+(-2){R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 5 \\ 0 & 1 & 2\end{bmatrix}\end{aligned}
$$

From the matrix above, we see that the pivot columns are the $1$st and $2$nd columns. So, a basis of $\textrm{Col}(A)$ is $\{\mathbf{a}_1,\mathbf{a}_2 \},$ that is to say,

$$
\mathcal{B}=\left\{ {\left[ \begin{array}{c}1 \\ 3\end{array} \right]}, {\left[ \begin{array}{c}2 \\ 1\end{array} \right]}\right\}.
$$

Now, since the $3$rd column of the reduced matrix is a non-pivot column, then the entries in that column tell us the coefficients needed to express $\mathbf{a}_3$ as a linear combination of all the other columns in the original matrix. So, we have

$$
\underbrace{ {\left[ \begin{array}{c}9 \\ 17\end{array} \right]}}_{\mathbf{a}_3} = \underbrace{(5)}_{x_1}\cdot \underbrace{ {\left[ \begin{array}{c}1 \\ 3\end{array} \right]}}_{\mathbf{a}_1} + \underbrace{(2)}_{x_2}\cdot \underbrace{ {\left[ \begin{array}{c}2 \\ 1\end{array} \right]}}_{\mathbf{a}_2}.
$$

This gives us $x_1 \cdot x_2 = 5 \cdot 2=10.$

### example 17592186151945 — Determining Whether a Given Set Is a Basis of the Column Space of a Matrix For a Larger Matrix

The matrix $A$ is given below. Let $\mathbf{a}_1$, $\mathbf{a}_2$,  $\mathbf{a}_3$, and $\mathbf{a}_4$ be the respective columns of $A.$ Determine if $\mathcal{B}={ { {\mathbf{a}}_{1} , {\mathbf{a}}_{2}}}$ is a basis of $\textrm{Col}(A).$ If that is the case, find $x_1 \cdot x_2$, where $\mathbf{a}_4=x_1\mathbf{a}_1+x_2\mathbf{a}_2.$

$$
A= 
{\left[ \begin{array}{cccc}2 & 0 & - 4 & 4 \\ 0 & 1 & - 6 & - 3 \\ 1 & 2 & - 14 & - 4\end{array} \right]}
$$

First, we reduce the matrix $A$ to reduced row echelon form (RREF):

$$
\begin{aligned}A & =\begin{bmatrix}2 & 0 & -4 & 4 \\ 0 & 1 & -6 & -3 \\ 1 & 2 & -14 & -4\end{bmatrix} & {R}_{1} & :=\frac{1}{2}{R}_{1} \\  & ∼\begin{bmatrix}1 & 0 & -2 & 2 \\ 0 & 1 & -6 & -3 \\ 1 & 2 & -14 & -4\end{bmatrix} & {R}_{3} & :={R}_{3}+(-1){R}_{1} \\  & ∼\begin{bmatrix}1 & 0 & -2 & 2 \\ 0 & 1 & -6 & -3 \\ 0 & 2 & -12 & -6\end{bmatrix} & {R}_{3} & :={R}_{3}+(-2){R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & -2 & 2 \\ 0 & 1 & -6 & -3 \\ 0 & 0 & 0 & 0\end{bmatrix}\end{aligned}
$$

From the matrix above, we see that the pivot columns are the $1$st and $2$nd columns. So, a basis of $\textrm{Col}(A)$ is $\{\mathbf{a}_1,\mathbf{a}_2 \},$ that is to say,
$$
\mathcal{B}=\left\{ {\left[ \begin{array}{c}2 \\ 0 \\ 1\end{array} \right]}, {\left[ \begin{array}{c}0 \\ 1 \\ 2\end{array} \right]}\right\}.
$$

Now, since the $4$th column of the reduced matrix is a non-pivot column, then the entries in that column tell us the coefficients needed to express $\mathbf{a}_4$ as a linear combination of all the other columns in the original matrix. So, we have

$$
\underbrace{ {\left[ \begin{array}{c}4 \\ - 3 \\ - 4\end{array} \right]}}_{\mathbf{a}_4} = \underbrace{\left(2\right)}_{x_1}\cdot \underbrace{ {\left[ \begin{array}{c}2 \\ 0 \\ 1\end{array} \right]}}_{\mathbf{a}_1} + \underbrace{(-3)}_{x_2}\cdot \underbrace{ {\left[ \begin{array}{c}0 \\ 1 \\ 2\end{array} \right]}}_{\mathbf{a}_2}.
$$

This gives us $x_1 \cdot x_2 = 2 \cdot (-3) = -6.$

## Representative practice (first three per skill; full bank in practice.json)

### Finding a Basis of the Column Space of a Matrix (17 captured questions)

Question 17592186152581 — None

Consider the matrix
$A = \begin{bmatrix}2 & -6 & 0 \\ 1 & -1 & 1 \\ 3 & 1 & 5\end{bmatrix}$. Find a basis $\mathcal{B}$ of $\operatorname{Col}(A)$.

Solution: To find a basis of the column space, reduce $A$ and select the corresponding pivot columns of the original matrix. Its reduced row echelon form is

$$
\begin{bmatrix}1&0&\frac32\\0&1&\frac12\\0&0&0\end{bmatrix}.
$$

The pivot columns are columns 1 and 2. Therefore,

$$
\mathcal B=\left\{\begin{bmatrix}2\\1\\3\end{bmatrix},\begin{bmatrix}-6\\-1\\1\end{bmatrix}\right\}
$$

is a basis of $\operatorname{Col}(A)$. The third column equals $\frac32$ times the first plus $\frac12$ times the second.

Answer selection: B = \left\{\begin{bmatrix}2 \\ 1 \\ 3\end{bmatrix}, \begin{bmatrix}-6 \\ -1 \\ 1\end{bmatrix}\right\}

Question 17592186152583 — question.difficulty/easy

Given the matrix
$A = \begin{bmatrix}0 & 0 & 0 \\ 0 & 0 & 3 \\ 1 & 0 & 2\end{bmatrix}$. Find a basis $\mathcal{B}$ of $\operatorname{Col}(A)$.

Solution: Swap rows 1 and 3, divide row 2 by 3, and subtract twice row 2 from row 1. This gives the reduced row echelon form

$$
\begin{bmatrix}1&0&0\\0&0&1\\0&0&0\end{bmatrix}.
$$

Columns 1 and 3 are pivot columns. Select those columns from the original matrix:

$$
\mathcal B=\left\{\begin{bmatrix}0\\0\\1\end{bmatrix},\begin{bmatrix}0\\3\\2\end{bmatrix}\right\}.
$$

These independent vectors span the column space. A basis cannot include the zero second column.

Answer selection: B = \left\{\begin{bmatrix}0 \\ 0 \\ 1\end{bmatrix}, \begin{bmatrix}0 \\ 3 \\ 2\end{bmatrix}\right\}

Question 17592186247215 — question.difficulty/easy

Given the matrix 
$G=\begin{bmatrix}0 & 0 & -5 \\ 5 & 2 & 0 \\ 0 & 0 & 0\end{bmatrix}.$ Find a basis $\mathcal{B}$ of $\text{Col}(G).$

Solution: In order to find a basis of $\text{Col}(G),$ we reduce the matrix $G$ to row echelon form:

$$
\begin{aligned}G & =\begin{bmatrix}0 & 0 & -5 \\ 5 & 2 & 0 \\ 0 & 0 & 0\end{bmatrix} & {R}_{1} & ↔{R}_{2} \\  & ∼\begin{bmatrix}5 & 2 & 0 \\ 0 & 0 & -5 \\ 0 & 0 & 0\end{bmatrix}\end{aligned}
$$

The pivot columns correspond to linearly independent vectors, while the non-pivot columns correspond to linearly dependent vectors that can be removed. Here, the $1$st and $3$rd columns are pivot columns, while the $2$nd column is a non-pivot column.

Remember that we need to pick the pivot columns from the *original matrix*, not from the reduced one. 

The $1$st and $3$rd columns from the original matrix are ${\mathbf{g}}_{1}$ and ${\mathbf{g}}_{3}.$ So, a basis of $\text{Col}(G)$ is $\{{\mathbf{g}}_{1},{\mathbf{g}}_{3}\},$ that is to say, 

$$
\mathcal{B}=\left\{\begin{bmatrix}0 \\ 5 \\ 0\end{bmatrix},\begin{bmatrix}-5 \\ 0 \\ 0\end{bmatrix}\right\}.
$$

Answer selection: B=\left\{\begin{bmatrix}0 \\ 5 \\ 0\end{bmatrix},\begin{bmatrix}-5 \\ 0 \\ 0\end{bmatrix}\right\}

### Determining Whether a Given Set Is a Basis of the Column Space of a Matrix With Two Rows (17 captured questions)

Question 17592186152579 — question.difficulty/moderate

The matrix $A$ is given below. Let ${\mathbf{a}}_{1}$, ${\mathbf{a}}_{2}$, and ${\mathbf{a}}_{3}$ be the respective columns of $A.$ Determine if $\mathcal{B}=\left\{{\mathbf{a}}_{1},{\mathbf{a}}_{2}\right\}$ is a basis of $\text{Col}(A).$ If that is the case, find ${x}_{1}\cdot {x}_{2}$, where ${\mathbf{a}}_{3}={x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2}.$ 

$$
A=\begin{bmatrix}1 & 0 & -1 \\ 0 & -2 & -6\end{bmatrix}
$$

Solution: First, we reduce the matrix $A$ to reduced row echelon form (RREF):

$$
\begin{aligned}A & =\begin{bmatrix}1 & 0 & -1 \\ 0 & -2 & -6\end{bmatrix} & {R}_{2} & :=-\frac{1}{2}{R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & -1 \\ 0 & 1 & 3\end{bmatrix}\end{aligned}
$$

From the matrix above, we see that the pivot columns are the $1$st and $2$nd columns. So, a basis of $\text{Col}(A)$ is $\{{a}_{1},{a}_{2}\},$ that is to say,

$$
B=\left\{\begin{bmatrix}1 \\ 0\end{bmatrix},\begin{bmatrix}0 \\ -2\end{bmatrix}\right\}.
$$

Now, since the $3$rd column of the reduced matrix is a non-pivot column, then the entries in that column tell us the coefficients needed to express ${a}_{3}$ as a linear combination of all the other columns in the original matrix. So, we have

$$
\underbrace{\begin{bmatrix}-1 \\ -6\end{bmatrix}}_{{a}_{3}}=\underbrace{(-1)}_{{x}_{1}}\cdot \underbrace{\begin{bmatrix}1 \\ 0\end{bmatrix}}_{{a}_{1}}+\underbrace{(3)}_{{x}_{2}}\cdot \underbrace{\begin{bmatrix}0 \\ -2\end{bmatrix}}_{{a}_{2}}.
$$

This gives us ${x}_{1}\cdot {x}_{2}=(-1)\cdot 3=-3.$

Answer selection: -3

Question 17592186152580 — question.difficulty/moderate

The matrix $A$ is given below. Let ${\mathbf{a}}_{1}$, ${\mathbf{a}}_{2}$, and ${\mathbf{a}}_{3}$ are the respective columns of $A.$ Determine if $\mathcal{B}=\left\{{\mathbf{a}}_{1},{\mathbf{a}}_{3}\right\}$ is a basis of $\text{Col}(A).$ 
If that is the case, find ${x}_{1}\cdot {x}_{3}$, where ${\mathbf{a}}_{2}={x}_{1}{\mathbf{a}}_{1}+{x}_{3}{\mathbf{a}}_{3}.$ 

$$
A=\begin{bmatrix}1 & 3 & 4 \\ -2 & -6 & 5\end{bmatrix}
$$

Solution: First, we reduce the matrix $A$ to reduced row echelon form (RREF):

$$
\begin{aligned}A & =\begin{bmatrix}1 & 3 & 4 \\ -2 & -6 & 5\end{bmatrix} & {R}_{2} & :={R}_{2}+2{R}_{1} \\  & ∼\begin{bmatrix}1 & 3 & 4 \\ 0 & 0 & 13\end{bmatrix} & {R}_{2} & :=\frac{1}{13}{R}_{2} \\  & ∼\begin{bmatrix}1 & 3 & 4 \\ 0 & 0 & 1\end{bmatrix} & {R}_{1} & :={R}_{1}+(-4){R}_{2} \\  & ∼\begin{bmatrix}1 & 3 & 0 \\ 0 & 0 & 1\end{bmatrix}\end{aligned}
$$

From the matrix above, we see that the pivot columns are the $1$st and $3$rd columns. So, a basis of $\text{Col}(A)$ is $\{{a}_{1},{a}_{3}\},$ that is to say,

$$
B=\left\{\begin{bmatrix}1 \\ -2\end{bmatrix},\begin{bmatrix}4 \\ 5\end{bmatrix}\right\}.
$$

Now, since the $2$nd column of the reduced matrix is a non-pivot column, then the entries in that column tell us the coefficients needed to express ${a}_{2}$ as a linear combination of all the other columns in the original matrix. So, we have

$$
\underbrace{\begin{bmatrix}3 \\ -6\end{bmatrix}}_{{a}_{2}}=\underbrace{(3)}_{{x}_{1}}\cdot \underbrace{\begin{bmatrix}1 \\ -2\end{bmatrix}}_{{a}_{1}}+\underbrace{(0)}_{{x}_{3}}\cdot \underbrace{\begin{bmatrix}4 \\ 5\end{bmatrix}}_{{a}_{3}}.
$$

This gives us ${x}_{1}\cdot {x}_{3}=3\cdot 0=0.$

Answer selection: 0

Question 17592186247221 — question.difficulty/moderate

The matrix $D$ is given below. Let ${\mathbf{d}}_{1}$, ${\mathbf{d}}_{2}$, and ${\mathbf{d}}_{3}$ be the respective columns of $D.$ Determine if $\mathcal{B}=\left\{{\mathbf{d}}_{1},{\mathbf{d}}_{3}\right\}$ is a basis of $\text{Col}(D).$ 
If that is the case, find ${x}_{1}\cdot {x}_{3}$, where ${\mathbf{d}}_{2}={x}_{1}{\mathbf{d}}_{1}+{x}_{3}{\mathbf{d}}_{3}.$ 

$$
D=\begin{bmatrix}1 & -6 & 2 \\ -4 & 24 & 8\end{bmatrix}
$$

Solution: First, we reduce the matrix $A$ to reduced row echelon form (RREF):

$$
\begin{aligned}D & =\begin{bmatrix}1 & -6 & 2 \\ -4 & 24 & 8\end{bmatrix} & {R}_{2} & :={R}_{2}+4{R}_{1} \\  & ∼\begin{bmatrix}1 & -6 & 2 \\ 0 & 0 & 16\end{bmatrix} & {R}_{2} & :=\frac{1}{16}{R}_{2} \\  & ∼\begin{bmatrix}1 & -6 & 2 \\ 0 & 0 & 1\end{bmatrix} & {R}_{1} & :={R}_{1}+(-2){R}_{2} \\  & ∼\begin{bmatrix}1 & -6 & 0 \\ 0 & 0 & 1\end{bmatrix}\end{aligned}
$$

From the matrix above, we see that the pivot columns are the $1$st and $3$rd columns. So, a basis of $\text{Col}(D)$ is $\{{\mathbf{d}}_{1},{\mathbf{d}}_{3}\},$ that is to say,

$$
\mathcal{B}=\left\{\begin{bmatrix}1 \\ -4\end{bmatrix},\begin{bmatrix}2 \\ 8\end{bmatrix}\right\}.
$$

Now, since the $2$nd column of the reduced matrix is a non-pivot column, then the entries in that column tell us the coefficients needed to express ${\mathbf{d}}_{2}$ as a linear combination of all the other columns in the original matrix. So, we have

$$
\underbrace{\begin{bmatrix}-6 \\ 24\end{bmatrix}}_{{\mathbf{d}}_{2}}=\underbrace{(-6)}_{{x}_{1}}\cdot \underbrace{\begin{bmatrix}1 \\ -4\end{bmatrix}}_{{\mathbf{d}}_{1}}+\underbrace{(0)}_{{x}_{3}}\cdot \underbrace{\begin{bmatrix}2 \\ 8\end{bmatrix}}_{{\mathbf{d}}_{3}}.
$$

This gives us ${x}_{1}\cdot {x}_{3}=-6\cdot 0=0.$

Answer selection: 0

### Determining Whether a Given Set Is a Basis of the Column Space of a Matrix For a Larger Matrix (17 captured questions)

Question 17592186152582 — question.difficulty/hard

The matrix $A$ is given below. Let ${\mathbf{a}}_{1}$, ${\mathbf{a}}_{2}$,  ${\mathbf{a}}_{3}$ and ${\mathbf{a}}_{4}$ be the respective columns of $A.$
Determine if $\mathcal{B}=\left\{{\mathbf{a}}_{1},{\mathbf{a}}_{2}\right\}$ is a basis of $\text{Col}(A).$ 
If that is the case, find ${x}_{1}\cdot {x}_{2}$, where ${\mathbf{a}}_{4}={x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2}.$ 

$$
A=\begin{bmatrix}1 & 2 & -1 & 0 \\ 0 & 4 & -4 & 4 \\ 3 & 5 & -2 & -1\end{bmatrix}
$$

Solution: First, we reduce the matrix $A$ to reduced row echelon form (RREF):

$$
\begin{aligned}A & =\begin{bmatrix}1 & 2 & -1 & 0 \\ 0 & 4 & -4 & 4 \\ 3 & 5 & -2 & -1\end{bmatrix} & {R}_{3} & :={R}_{3}+(-3){R}_{1} \\  & ∼\begin{bmatrix}1 & 2 & -1 & 0 \\ 0 & 4 & -4 & 4 \\ 0 & -1 & 1 & -1\end{bmatrix} & {R}_{2} & :=\frac{1}{4}{R}_{2} \\  & ∼\begin{bmatrix}1 & 2 & -1 & 0 \\ 0 & 1 & -1 & 1 \\ 0 & -1 & 1 & -1\end{bmatrix} & {R}_{3} & :={R}_{3}+{R}_{2} \\  & ∼\begin{bmatrix}1 & 2 & -1 & 0 \\ 0 & 1 & -1 & 1 \\ 0 & 0 & 0 & 0\end{bmatrix} & {R}_{1} & :={R}_{1}+(-2){R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 1 & -2 \\ 0 & 1 & -1 & 1 \\ 0 & 0 & 0 & 0\end{bmatrix}\end{aligned}
$$

From the matrix above, we see that the pivot columns are the $1$st and $2$nd columns. So, a basis of $\text{Col}(A)$ is $\{{\mathbf{a}}_{1},{\mathbf{a}}_{2}\},$ that is to say,

$$
\mathcal{B}=\left\{\begin{bmatrix}1 \\ 0 \\ 3\end{bmatrix},\begin{bmatrix}2 \\ 4 \\ 5\end{bmatrix}\right\}.
$$

Now, since the $4$th column of the reduced matrix is a non-pivot column, then the entries in that column tell us the coefficients needed to express ${\mathbf{a}}_{4}$ as a linear combination of all the other columns in the original matrix. So, we have

$$
\underbrace{\begin{bmatrix}0 \\ 4 \\ -1\end{bmatrix}}_{{\mathbf{a}}_{4}}=\underbrace{(-2)}_{{x}_{1}}\cdot \underbrace{\begin{bmatrix}1 \\ 0 \\ 3\end{bmatrix}}_{{\mathbf{a}}_{1}}+\underbrace{(1)}_{{x}_{2}}\cdot \underbrace{\begin{bmatrix}2 \\ 4 \\ 5\end{bmatrix}}_{{\mathbf{a}}_{2}}.
$$

This gives us ${x}_{1}\cdot {x}_{2}=(-2)\cdot 1=-2.$

Answer selection: -2

Question 17592186152721 — question.difficulty/hard

The matrix $A$ is given below. Let ${\mathbf{a}}_{1}$, ${\mathbf{a}}_{2}$, ${\mathbf{a}}_{3}$ and ${\mathbf{a}}_{4}$ be the respective columns of $A$.
Determine if $\mathcal{B}=\left\{{\mathbf{a}}_{1},{\mathbf{a}}_{2}\right\}$ is a basis of $\operatorname{Col}(A)$.
If that is the case, find $x_{1} \cdot x_{2}$, where ${\mathbf{a}}_{4}={x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2}$.

$$
\displaystyle A = \begin{bmatrix}1 & 0 & 2 & 1 \\ 0 & 5 & 10 & 5 \\ 1 & 0 & 2 & 2\end{bmatrix}
$$

Solution: The first two columns are $\mathbf a_1=(1,0,1)^T$ and $\mathbf a_2=(0,5,0)^T$. Every linear combination has equal first and third components. However, $\mathbf a_4=(1,5,2)^T$ does not have equal first and third components, so it is outside their span.

Thus $\{\mathbf a_1,\mathbf a_2\}$ does not span $\operatorname{Col}(A)$ and is not a basis. The conditional request for $x_1x_2$ does not apply.

Answer selection: ${a_{1}, a_{2}}$ is not a basis of $Col(A)$

Question 17592186247227 — question.difficulty/hard

The matrix $C$ is given below. Let ${\mathbf{c}}_{1}$, ${\mathbf{c}}_{2}$,  ${\mathbf{c}}_{3}$, and ${\mathbf{c}}_{4}$ be the respective columns of $C.$ Determine if $\mathcal{B}=\left\{{\mathbf{c}}_{1},{\mathbf{c}}_{2}\right\}$ is a basis of $\text{Col}(C).$ If that is the case, find ${x}_{1}\cdot {x}_{2}$, where ${\mathbf{c}}_{4}={x}_{1}{\mathbf{c}}_{1}+{x}_{2}{\mathbf{c}}_{2}.$

$$
C=\begin{bmatrix}1 & 0 & 1 & 4 \\ 1 & -4 & -3 & -8 \\ 3 & -4 & -1 & 0\end{bmatrix}
$$

Solution: First, we reduce the matrix $C$ to reduced row echelon form (RREF):

$$
\begin{aligned}C & =\begin{bmatrix}1 & 0 & 1 & 4 \\ 1 & -4 & -3 & -8 \\ 3 & -4 & -1 & 0\end{bmatrix} & {R}_{2} & :={R}_{2}+(-1){R}_{1} \\  & ∼\begin{bmatrix}1 & 0 & 1 & 4 \\ 0 & -4 & -4 & -12 \\ 3 & -4 & -1 & 0\end{bmatrix} & {R}_{3} & :={R}_{3}+(-3){R}_{1} \\  & ∼\begin{bmatrix}1 & 0 & 1 & 4 \\ 0 & -4 & -4 & -12 \\ 0 & -4 & -4 & -12\end{bmatrix} & {R}_{2} & :=\left(-\frac{1}{4}\right){R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 1 & 4 \\ 0 & 1 & 1 & 3 \\ 0 & -4 & -4 & -12\end{bmatrix} & {R}_{3} & :={R}_{3}+4{R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 1 & 4 \\ 0 & 1 & 1 & 3 \\ 0 & 0 & 0 & 0\end{bmatrix}\end{aligned}
$$

From the matrix above, we see that the pivot columns are the $1$st and $2$nd columns. So, a basis of $\text{Col}(C)$ is $\{{\mathbf{c}}_{1},{\mathbf{c}}_{2}\},$ that is to say,

$$
\mathcal{B}=\left\{\begin{bmatrix}1 \\ 1 \\ 3\end{bmatrix},\begin{bmatrix}0 \\ -4 \\ -4\end{bmatrix}\right\}.
$$

Now, since the $4$th column of the reduced matrix is a non-pivot column, then the entries in that column tell us the coefficients needed to express ${\mathbf{c}}_{4}$ as a linear combination of all the other columns in the original matrix. So, we have

$$
\underbrace{\begin{bmatrix}4 \\ -8 \\ 0\end{bmatrix}}_{{\mathbf{c}}_{4}}=\underbrace{(4)}_{{x}_{1}}\cdot \underbrace{\begin{bmatrix}1 \\ 1 \\ 3\end{bmatrix}}_{{\mathbf{c}}_{1}}+\underbrace{(3)}_{{x}_{2}}\cdot \underbrace{\begin{bmatrix}0 \\ -4 \\ -4\end{bmatrix}}_{{\mathbf{c}}_{2}}.
$$

This gives us ${x}_{1}\cdot {x}_{2}=4\cdot 3=12.$

Answer selection: 12
