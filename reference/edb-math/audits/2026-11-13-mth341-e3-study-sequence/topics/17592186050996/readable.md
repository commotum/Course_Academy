# 17592186050996 The Dimension of the Null Space of a Matrix

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186125778 — Introduction

We already learned that the rank of a matrix $A$ is the number of pivot columns in $A.$ Now, can we obtain any information from the *non-pivot* columns?

The answer is yes! The non-pivot columns help to find the dimension of the null space of a matrix $A,$ and here's how.

Consider the matrix 
$$
A = {\left[ \begin{array}{ccc}{\color{blue}3} & {\color{red}5} & {\color{blue}1} \\ {\color{blue}0} & {\color{red}0} & {\color{blue}2} \\ {\color{blue}0} & {\color{red}0} & {\color{blue}0}\end{array} \right]}.
$$

The matrix $A$ is already in row echelon form, where the $1$st and the $3$rd columns are pivot columns, while the $2$nd one is a *non-pivot* column. Now, to get the null space of $A,$ we need to find the solution of the system

$$
{\left\{  \begin{array}{l}3 {\color{blue}{x}_{1}} + 5 {\color{red}{x}_{2}} + {\color{blue}{x}_{3}} = 0 \\ 2 {\color{blue}{x}_{3}} = 0 \\ 0 = 0\end{array} \right. }
\qquad \Longrightarrow \qquad
{\left\{  \begin{array}{l}{\color{blue}{x}_{1}} = - {\displaystyle \frac{5}{3}} {\color{red}{x}_{2}} \\ {\color{blue}{x}_{3}} = 0\end{array} \right. }
$$

where $\color{blue}x_1$ and ${\color{blue}x_3}$ are basic variables and $\color{red}x_2$ is a free variable. Hence, we obtain that 

$$
\mathcal{B}=\left\{ {\left[ \begin{array}{c}- {\displaystyle \frac{5}{3}} \\ 1 \\ 0\end{array} \right]}\right\}
$$

is a basis of $\textrm{Null}(A)$ and, therefore, $\textrm{dim(Null}(A))={\color{red}1}$.

In other words,

$\textrm{dim(Null}(A))$ is equal to the number of *non-pivot* columns in the corresponding row echelon form of $A$

or, equivalently,

$\textrm{dim(Null}(A))$  is the number of *free variables* in the corresponding homogeneous system with the coefficient matrix $A.$



### example 17592186124317 — Determining the Dimension of the Null Space of a Matrix Given the Number of Non-Pivot Columns

If $A$ is a $9 \times 11$ matrix that has $9$ pivot columns, then what is $\textrm{dim(Null}(A))?$

We know that $\textrm{dim(Null}(A))$ is the number of non-pivot columns in $A$. 

Since $A$ has $11$ columns and $9$ of them are pivots, then the number of non-pivot columns in $A$ is 

$$
11-9=2.
$$

Therefore, $\textrm{dim(Null}(A))=2$.

### example 17592186124318 — Identifying the Dimension of the Null Space of Matrices Using Inspection

Which of the following statements are true?

I. If $A={\left[ \begin{array}{ccc}1 & 3 & 4 \\ 0 & 0 & 1 \\ 0 & 0 & 0\end{array} \right]}$ then $\textrm{dim(Null}(A))=2$

II. If $B={\left[ \begin{array}{ccc}2 & 0 & 4 \\ 0 & 0 & 0 \\ 0 & 0 & 0\end{array} \right]}$ then $\textrm{dim(Null}(B))=0$

III. If $C={\left[ \begin{array}{ccc}2 & 6 & 7 \\ 0 & 4 & 2 \\ 0 & 0 & 0\end{array} \right]}$ then $\textrm{dim(Null}(C))=1$

The dimension of the null space of a matrix is the number of non-pivot columns in the matrix. 

Also, all of the given matrices are in row echelon form.

With that in mind, let's consider each of the statements.

- Statement I is false. The matrix $A$ has $2$ pivot columns and $1$ non-pivot column (namely, the $2$nd column). So, 

$$
\textrm{dim(Null}(A))=1.
$$

- Statement II is false. The matrix $B$ has $1$ pivot column and $2$ non-pivot columns (namely, the $2$nd and $3$rd columns). So, 

$$
\textrm{dim(Null}(B))=2.
$$

- Statement III is true. The matrix $C$ has $2$ pivot columns and $1$ non-pivot column (namely, the $3$nd column). So, 

$$
\textrm{dim(Null}(C))=1.
$$

Therefore, only statement III is true.

### tutorial 17592186125779 — The Nullity of a Matrix

The dimension of the null space of a matrix $A$ is often called the **nullity** of $A$. We will also use the following notation:

$$
\textrm{nullity}(A) = \textrm{dim}(\textrm{Null}(A)).
$$



### example 17592186124319 — Finding the Nullity of a Matrix Using Row Reduction

Given $$
\displaystyle A={\left[ \begin{array}{cccc}2 & 1 & 3 & - 2 \\ 0 & - 3 & - 2 & - 1 \\ - 6 & 0 & - 7 & 4 \\ 0 & 9 & 6 & 3\end{array} \right]},\;
$$ what is $\textrm{nullity}(A)?$

To find $\textrm{dim}(\textrm{Null}(A))$, we reduce $A$ to row echelon form, as follows:

$$
\begin{aligned}A & =\begin{bmatrix}2 & 1 & 3 & -2 \\ 0 & -3 & -2 & -1 \\ -6 & 0 & -7 & 4 \\ 0 & 9 & 6 & 3\end{bmatrix} & {R}_{3} & :={R}_{3}+3{R}_{1} \\  & ∼\begin{bmatrix}2 & 1 & 3 & -2 \\ 0 & -3 & -2 & -1 \\ 0 & 3 & 2 & -2 \\ 0 & 9 & 6 & 3\end{bmatrix} & {R}_{3} & :={R}_{3}+{R}_{2} \\  & ∼\begin{bmatrix}2 & 1 & 3 & -2 \\ 0 & -3 & -2 & -1 \\ 0 & 0 & 0 & -3 \\ 0 & 9 & 6 & 3\end{bmatrix} & {R}_{4} & :={R}_{4}+3{R}_{2} \\  & ∼\begin{bmatrix}2 & 1 & 3 & -2 \\ 0 & -3 & -2 & -1 \\ 0 & 0 & 0 & -3 \\ 0 & 0 & 0 & 0\end{bmatrix}\end{aligned}
$$

The reduced matrix has $3$ pivot columns and $1$ non-pivot column (namely, the $3$rd column). 

Therefore,

$$
\textrm{nullity}(A) = \textrm{dim}(\textrm{Null}(A)) = 1.
$$

## Representative practice (first three per skill; full bank in practice.json)

### Determining the Dimension of the Null Space of a Matrix Given the Number of Non-Pivot Columns (12 captured questions)

Question 17592186124867 — question.difficulty/moderate

Let $R$ be a $8\times 12$ matrix that has $8$ pivot columns. What is the dimension of the null space of $R?$

Solution: We know that $\text{dim(Null}(R))$ is the number of non-pivot columns in $R.$ 

Since $R$ has $12$ columns and $8$ of them are pivots, then the number of non-pivot columns in $R$ is 

$$
12-8=4.
$$

Therefore, $\text{dim(Null}(R))=4.$

Answer selection: 4

Question 17592186125225 — question.difficulty/easy

If $A$ is a $5\times 8$ matrix that has $3$ **non-pivot** columns, then $\text{dim(Null}(A))=$

Solution: We know that $\text{dim(Null}(A))$ is the number of non-pivot columns in $A.$

Since we are told that $A$ has $3$ non-pivot columns, we have 

$$
\text{dim(Null}(A))=3.
$$

Answer selection: 3

Question 17592186271983 — question.difficulty/easy

If $B$ is a $7\times 12$ matrix that has $4$ **non-pivot** columns, then $\text{dim(Null}(B))=$

Solution: We know that $\text{dim(Null}(B))$ is the number of non-pivot columns in $B.$

Since we are told that $B$ has $4$ non-pivot columns, we have 

$$
\text{dim(Null}(B))=4.
$$

Answer selection: 4

### Identifying the Dimension of the Null Space of Matrices Using Inspection (12 captured questions)

Question 17592186124868 — question.difficulty/easy

Which of the following statements are true?

Select all that apply.

Solution: The dimension of the null space of a matrix is the number of non-pivot columns in the matrix. 

Also, all of the given matrices are in row echelon form.

With that in mind, let's consider each of the statements.

- Statement “If $A=\begin{bmatrix}1 & 1 \\ 0 & 3\end{bmatrix}$ then $\text{dim(Null}(A))=0.$” is true. The matrix $A$ has $2$ pivot columns and no non-pivot columns. So, 

$$
\text{dim(Null}(A))=0.
$$

- Statement “If $B=\begin{bmatrix}2 & 0 & 4 \\ 0 & 1 & 2 \\ 0 & 0 & 0\end{bmatrix}$ then $\text{dim(Null}(B))=2.$” is false. The matrix $B$ has $2$ pivot column and $1$ non-pivot column (namely, the $3$rd column). So, 

$$
\text{dim(Null}(B))=1.
$$

- Statement “If $C=\begin{bmatrix}5 & 4 & 0 \\ 0 & 0 & 1 \\ 0 & 0 & 0\end{bmatrix}$ then $\text{dim(Null}(C))=1.$” is true. The matrix $C$ has $2$ pivot columns and $1$ non-pivot column (namely, the $2$nd column). So, 

$$
\text{dim(Null}(C))=1.
$$

Therefore, the correct answer is “If $A=\begin{bmatrix}1 & 1 \\ 0 & 3\end{bmatrix}$ then $\text{dim(Null}(A))=0.$”; “If $C=\begin{bmatrix}5 & 4 & 0 \\ 0 & 0 & 1 \\ 0 & 0 & 0\end{bmatrix}$ then $\text{dim(Null}(C))=1.$” only.

Answer If $A=\begin{bmatrix}1 & 1 \\ 0 & 3\end{bmatrix}$ then $\text{dim(Null}(A))=0.$: true

Answer If $B=\begin{bmatrix}2 & 0 & 4 \\ 0 & 1 & 2 \\ 0 & 0 & 0\end{bmatrix}$ then $\text{dim(Null}(B))=2.$: false

Answer If $C=\begin{bmatrix}5 & 4 & 0 \\ 0 & 0 & 1 \\ 0 & 0 & 0\end{bmatrix}$ then $\text{dim(Null}(C))=1.$: true

Answer None of the above: false

Question 17592186124877 — question.difficulty/easy

Consider the matrices given below. Find $\text{dim(Null}(A))+\text{dim(Null}(B))+\text{dim(Null}(C)).$

$$
A=\begin{bmatrix}1 & -1 & 5 \\ 0 & 0 & -7 \\ 0 & 0 & 0\end{bmatrix},\,B=\begin{bmatrix}2 & -4 & 7 & 2 \\ 0 & 0 & 5 & 3 \\ 0 & 0 & 0 & 0\end{bmatrix},\,C=\begin{bmatrix}1 & 0 & -4 & 3 \\ 0 & 2 & 1 & 0 \\ 0 & 0 & -7 & 9 \\ 0 & 0 & 0 & 2\end{bmatrix}
$$

Solution: The dimension of the null space of a matrix is the number of non-pivot columns in the matrix. 

Also, all of the given matrices are in row echelon form.

With that in mind, let's consider each of the statements.

- The matrix $A$ has $2$ pivot columns and $1$ non-pivot column (namely, the $2$nd column). So, 

$$
\text{dim(Null}(A))=1.
$$

- The matrix $B$ has $2$ pivot columns and $2$ non-pivot columns (namely, the $2$nd and $4$th columns). So, 

$$
\text{dim(Null}(B))=2.
$$

- The matrix $C$ has $4$ pivot columns and no non-pivot columns. So, 

$$
\text{dim(Null}(C))=0.
$$

Therefore,

$$
\text{dim(Null}(A))+\text{dim(Null}(B))+\text{dim(Null}(C))=1+2+0=3.
$$

Answer selection: 3

Question 17592186271986 — question.difficulty/easy

Which of the following statements are true?

Select all that apply.

Solution: The dimension of the null space of a matrix is the number of non-pivot columns in the matrix. 

Also, all of the given matrices are in row echelon form.

With that in mind, let's consider each of the statements.

- Statement “If $A=\begin{bmatrix}1 & 2 \\ 0 & 1\end{bmatrix}$ then $\text{dim(Null}(A))=2.$” is false. The matrix $A$ has $2$ pivot columns and no non-pivot columns. So, 

$$
\text{dim(Null}(A))=0.
$$

- Statement “If $B=\begin{bmatrix}1 & 0 & -2 \\ 0 & 1 & -2 \\ 0 & 0 & \,0\end{bmatrix}$ then $\text{dim(Null}(B))=1.$” is true. The matrix $B$ has $2$ pivot columns and $1$ non-pivot column (namely, the $3$rd column). So, 

$$
\text{dim(Null}(B))=1.
$$

- Statement “If $C=\begin{bmatrix}5 & 4 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix}$ then $\text{dim(Null}(C))=0.$” is true. The matrix $C$ has $3$ pivot columns and no non-pivot columns. So, 

$$
\text{dim(Null}(C))=0.
$$

Therefore, the correct answer is “If $B=\begin{bmatrix}1 & 0 & -2 \\ 0 & 1 & -2 \\ 0 & 0 & \,0\end{bmatrix}$ then $\text{dim(Null}(B))=1.$”; “If $C=\begin{bmatrix}5 & 4 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix}$ then $\text{dim(Null}(C))=0.$” only.

Answer If $A=\begin{bmatrix}1 & 2 \\ 0 & 1\end{bmatrix}$ then $\text{dim(Null}(A))=2.$: false

Answer If $B=\begin{bmatrix}1 & 0 & -2 \\ 0 & 1 & -2 \\ 0 & 0 & \,0\end{bmatrix}$ then $\text{dim(Null}(B))=1.$: true

Answer If $C=\begin{bmatrix}5 & 4 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix}$ then $\text{dim(Null}(C))=0.$: true

### Finding the Nullity of a Matrix Using Row Reduction (12 captured questions)

Question 17592186124871 — question.difficulty/moderate

Given $$
\displaystyle D=\begin{bmatrix}2 & 1 & 2 & 3 & 1 \\ 0 & 4 & -2 & 1 & -2 \\ 8 & 0 & 10 & 9 & 7 \\ 0 & 8 & -4 & 2 & -4\end{bmatrix},\,
$$ what is $\text{dim}(\text{Null}(D))?$

Solution: To find $\text{dim}(\text{Null}(D))$, we reduce $D$ to row echelon form, as follows:

$$
\begin{aligned}D & =\begin{bmatrix}2 & 1 & 2 & 3 & 1 \\ 0 & 4 & -2 & 1 & -2 \\ 8 & 0 & 10 & 9 & 7 \\ 0 & 8 & -4 & 2 & -4\end{bmatrix} & {R}_{3} & :={R}_{3}+(-4){R}_{1} \\  & ∼\begin{bmatrix}2 & 1 & 2 & 3 & 1 \\ 0 & 4 & -2 & 1 & -2 \\ 0 & -4 & 2 & -3 & 3 \\ 0 & 8 & -4 & 2 & -4\end{bmatrix} & {R}_{3} & :={R}_{3}+{R}_{2} \\  & ∼\begin{bmatrix}2 & 1 & 2 & 3 & 1 \\ 0 & 4 & -2 & 1 & -2 \\ 0 & 0 & 0 & -2 & 1 \\ 0 & 8 & -4 & 2 & -4\end{bmatrix} & {R}_{4} & :={R}_{4}+(-2){R}_{2} \\  & ∼\begin{bmatrix}2 & 1 & 2 & 3 & 1 \\ 0 & 4 & -2 & 1 & -2 \\ 0 & 0 & 0 & -2 & 1 \\ 0 & 0 & 0 & 0 & 0\end{bmatrix}.\end{aligned}
$$

The reduced matrix has $3$ pivot columns and $2$ non-pivot columns (namely, the $3$rd and $5$th columns). 

Therefore,

$$
\text{dim}(\text{Null}(D))=2.
$$

Answer selection: 2

Question 17592186124876 — question.difficulty/easy

If $D=\begin{bmatrix}1 & -2 & 0 \\ 5 & -7 & 9 \\ -3 & 6 & -1\end{bmatrix},\,$ then $\text{nullity}(D)=$

Solution: Recall that by definition, $\text{nullity}(D)=\text{dim}(\text{Null}(D)).$

To find $\text{dim}(\text{Null}(D))$, we reduce $D$ to row echelon form, as follows:

$$
\begin{aligned}D & =\begin{bmatrix}1 & -2 & 0 \\ 5 & -7 & 9 \\ -3 & 6 & -1\end{bmatrix} & {R}_{2} & :={R}_{2}+(-5){R}_{1} \\  & ∼\begin{bmatrix}1 & -2 & 0 \\ 0 & 3 & 9 \\ -3 & 6 & -1\end{bmatrix} & {R}_{3} & :={R}_{3}+3{R}_{1} \\  & ∼\begin{bmatrix}1 & -2 & 0 \\ 0 & 3 & 9 \\ 0 & 0 & -1\end{bmatrix}\end{aligned}
$$

The reduced matrix has $3$ pivot columns and no non-pivot columns. 

Therefore,

$$
\text{nullity}(D)=\text{dim}(\text{Null}(D))=0.
$$

Answer selection: 0

Question 17592186271988 — question.difficulty/easy

If $W=\begin{bmatrix}1 & -4 & 2 & 3 \\ -3 & 12 & 4 & 9 \\ 5 & -20 & 10 & 8\end{bmatrix},\,$ then $\text{nullity}(W)=$

Solution: Recall that by definition, $\text{nullity}(W)=\text{dim}(\text{Null}(W)).$

To find $\text{dim}(\text{Null}(W))$, we reduce $W$ to row echelon form, as follows: 

$$
\begin{aligned}W & =\begin{bmatrix}1 & -4 & 2 & 3 \\ -3 & 12 & 4 & 9 \\ 5 & -20 & 10 & 8\end{bmatrix} & {R}_{2} & :={R}_{2}+3{R}_{1} \\  & ∼\begin{bmatrix}1 & -4 & 2 & 3 \\ 0 & 0 & 10 & 18 \\ 5 & -20 & 10 & 8\end{bmatrix} & {R}_{3} & :={R}_{3}+(-5){R}_{1} \\  & ∼\begin{bmatrix}1 & -4 & 2 & 3 \\ 0 & 0 & 10 & 18 \\ 0 & 0 & 0 & -7\end{bmatrix}\end{aligned}
$$

The reduced matrix has $3$ pivot columns and  $1$
 non-pivot column (the $2$nd). 

Therefore,

$$
\text{nullity}(W)=\text{dim}(\text{Null}(W))=1.
$$

Answer selection: 1
