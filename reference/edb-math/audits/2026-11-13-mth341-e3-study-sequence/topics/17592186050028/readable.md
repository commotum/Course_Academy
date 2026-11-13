# 17592186050028 The Rank of a Matrix

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186121058 — Introduction

The dimension of the column space of a matrix $A$ is called the **rank of $A$**. It's usually denoted by $\textrm{rank}(A)$. So, 

$$
\textrm{rank}(A) = \textrm{dim}(\textrm{Col}(A)).
$$

For example, to find the rank of 


$$
A=\begin{bmatrix}3 & 2 & 5 \\ 0 & 1 & 0 \\ 6 & 4 & 10\end{bmatrix},
$$


we write $A$ in row echelon form, as follows:

$$
\begin{aligned}A & =\begin{bmatrix}3 & 2 & 5 \\ 0 & 1 & 0 \\ 6 & 4 & 10\end{bmatrix} & {R}_{3} & :={R}_{3}+(-2){R}_{1} \\  & ∼\begin{bmatrix}3 & 2 & 5 \\ 0 & 1 & 0 \\ 0 & 0 & 0\end{bmatrix}.\end{aligned}
$$

From the reduced matrix above, we see that there are $2$ pivot columns, namely, the $1$st and the $2$nd. This implies that the first and the second columns of $A$ form a basis of $\textrm{Col}(A)$ and, therefore, the dimension of $\textrm{Col}(A)$ is equal to $2.$



### example 17592186119661 — Determining the Rank of a Matrix Given the Number of Pivot Columns

Let $A$ be a $4 \times 7$ matrix that has $3$ **non-pivot** columns. Find $\textrm{rank}(A).$

We know that $\textrm{rank}(A)$ is the number of pivot columns in $A$. 

Since $A$ has $7$ columns and $3$ of them are non-pivots, then the number of pivot columns in $A$ is 

$$
7-3=4.
$$

Therefore, $\textrm{rank}(A)=4$.

### tutorial 17592186121068 — An Alternative Definition of the Rank

Note that the number of pivot columns always coincides with the number of non-zero rows in the corresponding row echelon form matrix.
So, technically, 

$\textrm{rank}(A)$ is the number of *pivot columns* in the corresponding row echelon form matrix of $A$.

Or, equivalently,

$\textrm{rank}(A)$ is the number of *non-zero rows* in the corresponding row echelon form matrix of $A$.



### example 17592186119662 — Identifying the Matrix With a Given Rank by Inspection

Which of the following matrices have a rank of $4?$



$$
A = \begin{bmatrix}1 & -2 & 0 & -1 \\ 0 & 2 & 7 & 1 \\ 0 & 0 & 3 & 0 \\ 0 & 0 & 0 & 0\end{bmatrix}, \quad B = \begin{bmatrix}1 & 0 & 1 & 6 \\ 0 & 4 & 2 & -3 \\ 0 & 0 & 1 & -1\end{bmatrix}, \quad C = \begin{bmatrix}1 & 0 & 1 & 1 & 6 \\ 0 & 4 & 2 & 2 & -3 \\ 0 & 0 & 1 & 0 & -1 \\ 0 & 0 & 0 & 0 & 1\end{bmatrix}
$$



First, notice that a matrix of rank $4$ must have at least $4$ columns and at least $4$ rows. 
So, we disregard the matrix $B$ since it has only $3$ rows. 

Also, the matrix must have $4$ pivot columns. As we can see, the matrix $A$ has only $3$ pivot columns, while the matrix $C$ has exactly $4$ pivot columns. So, $\textrm{rank}(A)=3$ and $\textrm{rank}(C)=4.$

Therefore, the correct answer is "$C$ only".

### example 17592186119663 — Finding the Rank of a Matrix Using Row Reduction

If 

$$
A=\begin{bmatrix}2 & 3 & 0 \\ 0 & -1 & 5 \\ -4 & 0 & 5\end{bmatrix}
$$

, find $\textrm{rank}(A).$

To find the rank of $A,$ we first reduce it to row echelon form, as follows:

$$
\begin{aligned}A & =\begin{bmatrix}2 & 3 & 0 \\ 0 & -1 & 5 \\ -4 & 0 & 5\end{bmatrix} & {R}_{3} & :={R}_{3}+2{R}_{1} \\  & ∼\begin{bmatrix}2 & 3 & 0 \\ 0 & -1 & 5 \\ 0 & 6 & 5\end{bmatrix} & {R}_{3} & :={R}_{3}+6{R}_{2} \\  & ∼\begin{bmatrix}2 & 3 & 0 \\ 0 & -1 & 5 \\ 0 & 0 & 35\end{bmatrix}\end{aligned}
$$

The reduced matrix above has $3$ pivot columns (or, alternatively, it has exactly $3$ non-zero rows).

Therefore, $\textrm{rank}(A)=3.$

## Representative practice (first three per skill; full bank in practice.json)

### Determining the Rank of a Matrix Given the Number of Pivot Columns (18 captured questions)

Question 17592186120363 — question.difficulty/moderate

If $A$ is a $6\times 11$ matrix that has $8$ **non-pivot** columns, then $\text{rank}(A)=$

Solution: We know that $\text{rank}(A)$ is the number of pivot columns in $A.$ 

Since $A$ has $11$ columns and $8$ of them are non-pivots, then the number of pivot columns in $A$ is 

$$
11-8=3.
$$

Therefore, $\text{rank}(A)=3.$

Answer selection: 3

Question 17592186120366 — question.difficulty/easy

Let $P$ be a $5\times7$ matrix that has $5$ **pivot** columns. What is the rank of the matrix?

Solution: The rank of a matrix is the number of its pivot columns. Since $P$ has $5$ pivot columns,

$$
\operatorname{rank}(P)=5.
$$

Answer selection: 5

Question 17592186271973 — question.difficulty/easy

Let $T$ be a $8\times 8$ matrix that has $7$ **pivot** columns. What is the rank of the matrix?

Solution: We know that $\text{rank}(T)$ is the number of pivot columns in $T.$ 

Since we are told that $T$ has $7$ pivot columns, we have 

$$
\text{rank}(T)=7.
$$

Answer selection: 7

### Identifying the Matrix With a Given Rank by Inspection (17 captured questions)

Question 17592186120364 — question.difficulty/easy

Which of the following matrices has a rank of $4$?

Solution: A matrix with rank $4$ must have at least four rows and four columns. This excludes $A$, $C$, and $E$, which have fewer than four rows or columns.

The remaining matrices are in row echelon form. Matrix $D$ has three nonzero rows, hence three pivot columns, so its rank is $3$. Matrix $B$ has four nonzero rows with pivots in columns $1$, $2$, $3$, and $4$, so its rank is $4$.

Therefore, the correct matrix is $B$.

Answer selection: B = \begin{bmatrix}1 & 0 & 2 & 0 & 0 \\ 0 & -1 & 3 & 1 & 2 \\ 0 & 0 & 1 & 1 & 0 \\ 0 & 0 & 0 & 2 & 1\end{bmatrix}

Question 17592186120384 — question.difficulty/easy

Which of the following matrices have a rank of $4$?

$$
\displaystyle A = \begin{bmatrix}1 & 0 & 2 & 0 \\ 0 & 1 & 3 & 0\end{bmatrix}, B = \begin{bmatrix}1 & 3 & 5 & 0 & 6 \\ 0 & 0 & 3 & 7 & 5 \\ 0 & 0 & 1 & 4 & 2 \\ 0 & 0 & 0 & 2 & 3 \\ 0 & 0 & 0 & 0 & 3\end{bmatrix}, C = \begin{bmatrix}1 & 0 & 1 & 6 \\ 0 & 0 & 2 & -3 \\ 0 & 0 & 1 & -1 \\ 0 & 0 & 0 & -1\end{bmatrix}
$$

Solution: The rank is the number of pivot columns in row echelon form.

Matrix $A$ has only two rows, so its rank is at most $2$.

For $B$, apply $R_2:=R_2-3R_3$ to obtain a row with entries $0,0,0,-5,-1$. This row, together with the rows whose last two entries are $2,3$ and $0,3$, spans a two-dimensional space in columns $4$ and $5$. Along with the pivots in columns $1$ and $3$, this gives four pivot columns. Thus $\operatorname{rank}(B)=4$.

For $C$, the second column is zero. The first, third, and fourth columns are independent: a $3\times3$ minor using rows $1$, $2$, and $4$ has determinant $-2$. Hence $\operatorname{rank}(C)=3$.

Therefore, $B$ only has rank $4$.

Answer selection: $B$ only

Question 17592186271978 — question.difficulty/easy

Which of the following matrices has a rank of $4?$

Solution: First, notice that a matrix of rank $4$ must have at least $4$ columns and at least $4$ rows. 
So, we disregard the following matrices:

- $A$ since it has only $2$ rows.

- $B$ since it has only $3$  rows.

- $D$ since it has only $3$ columns.

Also, the matrix must have $4$ pivot columns. As we can see, the matrix $C$ has exactly $4$ pivot columns, while the matrix $E$ has only $3$ pivot columns. So, $\text{rank}(C)=4$ and $\text{rank}(E)=3.$

Therefore, the correct answer is the matrix $C.$

Answer selection: C=\begin{bmatrix}-2 & 0 & 0 & 0 & 0 \\ 2 & -1 & 0 & 0 & 0 \\ 1 & 3 & 3 & 0 & 0 \\ 2 & 2 & 1 & 3 & 0\end{bmatrix}

### Finding the Rank of a Matrix Using Row Reduction (12 captured questions)

Question 17592186120385 — question.difficulty/hard

If 
$$
\displaystyle A=\begin{bmatrix}-2 & 1 & 3 & -2 \\ 6 & -2 & -7 & 5 \\ 0 & 2 & 4 & -3 \\ 0 & -3 & -6 & 3\end{bmatrix},
$$ find $\text{rank}(A).$

Solution: To find the rank of $A,$ we first reduce it to row echelon form, as follows:

$$
\begin{aligned}A & =\begin{bmatrix}-2 & 1 & 3 & -2 \\ 6 & -2 & -7 & 5 \\ 0 & 2 & 4 & -3 \\ 0 & -3 & -6 & 3\end{bmatrix} & {R}_{2} & :={R}_{2}+3{R}_{1} \\  & ∼\begin{bmatrix}-2 & 1 & 3 & -2 \\ 0 & 1 & 2 & -1 \\ 0 & 2 & 4 & -3 \\ 0 & -3 & -6 & 3\end{bmatrix} & {R}_{3} & :={R}_{3}+(-2){R}_{2} \\  & ∼\begin{bmatrix}-2 & 1 & 3 & -2 \\ 0 & 1 & 2 & -1 \\ 0 & 0 & 0 & -1 \\ 0 & -3 & -6 & 3\end{bmatrix} & {R}_{4} & :={R}_{4}+3{R}_{2} \\  & ∼\begin{bmatrix}-2 & 1 & 3 & -2 \\ 0 & 1 & 2 & -1 \\ 0 & 0 & 0 & -1 \\ 0 & 0 & 0 & 0\end{bmatrix}\end{aligned}
$$

The reduced matrix has $3$ pivot columns (or alternatively, it has exactly $3$ non-zero rows).

Therefore, $\text{rank}(A)=3.$

Answer selection: 3

Question 17592186120386 — question.difficulty/easy

If 
$H=\begin{bmatrix}-4 & 6 \\ 0 & -1 \\ 2 & -3\end{bmatrix}$, then $\text{rank}(H)=$

Solution: To find the rank of $H,$ we first reduce it to row echelon form, as follows:

$$
\begin{aligned}H & =\begin{bmatrix}-4 & 6 \\ 0 & -1 \\ 2 & -3\end{bmatrix} & {R}_{3} & :={R}_{3}+\frac{1}{2}{R}_{1} \\  & ∼\begin{bmatrix}-4 & 6 \\ 0 & -1 \\ 0 & 0\end{bmatrix}\end{aligned}
$$

The reduced matrix has $2$ pivot columns (or alternatively, it has exactly $2$ non-zero rows).

Therefore, $\text{rank}(H)=2.$

Answer selection: 2

Question 17592186319238 — question.difficulty/hard

If 
$$
\displaystyle E=\begin{bmatrix}-1 & 6 & 5 & 3 \\ 0 & -2 & -2 & -1 \\ 3 & 2 & 5 & 1 \\ 0 & -4 & -4 & -2\end{bmatrix},
$$ find $\text{rank}(E).$

Solution: To find the rank of $E,$ we first reduce it to row echelon form, as follows:

$$
\begin{aligned}E & =\begin{bmatrix}-1 & 6 & 5 & 3 \\ 0 & -2 & -2 & -1 \\ 3 & 2 & 5 & 1 \\ 0 & -4 & -4 & -2\end{bmatrix} & {R}_{3} & :={R}_{3}+3{R}_{1} \\  & ∼\begin{bmatrix}-1 & 6 & 5 & 3 \\ 0 & -2 & -2 & -1 \\ 0 & 20 & 20 & 10 \\ 0 & -4 & -4 & -2\end{bmatrix} & {R}_{3} & :={R}_{3}+10{R}_{2} \\  & ∼\begin{bmatrix}-1 & 6 & 5 & 3 \\ 0 & -2 & -2 & -1 \\ 0 & 0 & 0 & 0 \\ 0 & -4 & -4 & -2\end{bmatrix} & {R}_{4} & :={R}_{4}+(-2){R}_{2} \\  & ∼\begin{bmatrix}-1 & 6 & 5 & 3 \\ 0 & -2 & -2 & -1 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0\end{bmatrix}\end{aligned}
$$

The reduced matrix has $2$ pivot columns (or alternatively, it has exactly $2$ non-zero rows).

Therefore, $\text{rank}(E)=2.$

Answer selection: 2
