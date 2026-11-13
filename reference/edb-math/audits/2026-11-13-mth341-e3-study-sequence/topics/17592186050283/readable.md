# 17592186050283 Triangular Matrices

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186121017 — Introduction

Recall that a matrix is square if the number of rows equals the number of columns. There are other types of square matrices with special names.

- An **upper triangular** matrix is a square matrix in which all entries *below* the diagonal are zeros. For example, the following matrices are all upper triangular matrices:

$$
\begin{bmatrix}1 & -3 \\ {\color{blue}{0}} & 2\end{bmatrix},
	\qquad
	\begin{bmatrix}1 & 2 & 3 \\ {\color{blue}{0}} & 4 & 5 \\ {\color{blue}{0}} & {\color{blue}{0}} & 6\end{bmatrix},
	\qquad
	\begin{bmatrix}2 & 0 & 1 & 0 \\ {\color{blue}{0}} & 1 & 0 & 1 \\ {\color{blue}{0}} & {\color{blue}{0}} & -2 & -1 \\ {\color{blue}{0}} & {\color{blue}{0}} & {\color{blue}{0}} & 2\end{bmatrix}.
$$

$$
\begin{bmatrix}1 & 2 & 3 \\ {\color{blue}0} & 4 & 5 \\ {\color{blue}0} & {\color{blue}0} & 6\end{bmatrix}
$$

$$
\begin{bmatrix}2 & 0 & 1 & 0 \\ {\color{blue}0} & 1 & 0 & 1 \\ {\color{blue}0} & {\color{blue}0} & -2 & -1 \\ {\color{blue}0} & {\color{blue}0} & {\color{blue}0} & 2\end{bmatrix}
$$

Note that we can have any number (including $0$) on the diagonal and above.

- A **lower triangular** matrix is a square matrix in which all entries *above* the diagonal are zeros. For example, the following matrices are all lower triangular matrices:

$$
\begin{bmatrix}1 & {\color{blue}{0}} \\ 3 & 1\end{bmatrix},
	\qquad
	\begin{bmatrix}1 & {\color{blue}{0}} & {\color{blue}{0}} \\ 3 & 1 & {\color{blue}{0}} \\ -4 & -4 & 1\end{bmatrix},
	\qquad
	\begin{bmatrix}-2 & {\color{blue}{0}} & {\color{blue}{0}} & {\color{blue}{0}} \\ 4 & 0 & {\color{blue}{0}} & {\color{blue}{0}} \\ 7 & -1 & 1 & {\color{blue}{0}} \\ -1 & 2 & 0 & 3\end{bmatrix}.
$$

$$
\begin{bmatrix}1 & {\color{blue}0} & {\color{blue}0} \\ 3 & 1 & {\color{blue}0} \\ -4 & -4 & 1\end{bmatrix}
$$

$$
\begin{bmatrix}-2 & {\color{blue}0} & {\color{blue}0} & {\color{blue}0} \\ 4 & 0 & {\color{blue}0} & {\color{blue}0} \\ 7 & -1 & 1 & {\color{blue}0} \\ -1 & 2 & 0 & 3\end{bmatrix}
$$

Again, note that we can have any number (including $0$) on the diagonal and below.



### example 17592186119585 — Describing a Triangular Matrix

How can we best describe the following matrix? 

$$
A = \begin{bmatrix}-2 & 0 & 0 \\ 6 & -1 & 0 \\ 0 & 0 & 0\end{bmatrix}
$$

Notice that $A$ is a matrix for which all entries above the diagonal are $0$'s:

$$
A = \begin{bmatrix}-2 & {\color{blue}0} & {\color{blue}0} \\ 6 & -1 & {\color{blue}0} \\ 0 & 0 & 0\end{bmatrix}
$$

Therefore, it is a lower triangular matrix.

It is not an upper triangular matrix or a diagonal matrix since there is a non-zero element below the diagonal: $a_{21}=6 \neq 0.$

### example 17592186119586 — Identifying a Triangular Matrix

Which of the following matrices are lower triangular matrices?

$$
A = \begin{bmatrix}0 & 0 & 0 \\ 0 & 0 & 1 \\ 0 & 0 & 0\end{bmatrix}
$$

$$
B = \begin{bmatrix}0 & 0 & 0 \\ 0 & 0 & 0 \\ 1 & 0 & 0\end{bmatrix}
$$

$$
C = \begin{bmatrix}1 & 0 & 1 \\ 0 & 0 & 0 \\ 1 & 0 & 1\end{bmatrix}
$$

The matrix $B$ is a lower triangular matrix since all the entries above the main diagonal are zeros.

The matrices $A$ and $C$ are *not* lower triangular matrices since they each have a non-zero element above the main diagonal:

$$
\begin{aligned}{a}_{23} & =1\ne 0 \\ {c}_{13} & =1\ne 0\end{aligned}
$$

### example 17592186119598 — Identifying Correct Statements About a Matrix

Consider the matrix 

$$
A = \begin{bmatrix}0 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 2\end{bmatrix}
$$

Which of the following statements are true?

- $A$ is upper triangular

- $A$ is lower triangular

- $A^T-A$ is lower triangular

Let's analyze each statement in turn.

- Statement I is false, since $A$ has non-zero entries below the main diagonal:

$$
A = \begin{bmatrix}0 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & {\color{red}1} & 0 & 0 \\ 0 & 0 & {\color{red}1} & 2\end{bmatrix}
$$

- Statement II is true, since all the entries above the main diagonal are zeros:

$$
A = \begin{bmatrix}0 & {\color{blue}0} & {\color{blue}0} & {\color{blue}0} \\ 0 & 1 & {\color{blue}0} & {\color{blue}0} \\ 0 & 1 & 0 & {\color{blue}0} \\ 0 & 0 & 1 & 2\end{bmatrix}
$$

- Statement III is false, since the result of $A^T-A$ has non-zero entries above the main diagonal:

$$
A^T-A = \begin{bmatrix}0 & 0 & 0 & 0 \\ 0 & 0 & {\color{red}1} & 0 \\ 0 & -1 & 0 & {\color{red}1} \\ 0 & 0 & -1 & 0\end{bmatrix}
$$

Therefore, the correct answer is "II only".

## Representative practice (first three per skill; full bank in practice.json)

### Describing a Triangular Matrix (21 captured questions)

Question 17592186120120 — question.difficulty/easy

How can we best describe the following matrix? 

$$
A=\begin{bmatrix}7 & 0 & 0 \\ 3 & -1 & 0 \\ 0 & 5 & 0\end{bmatrix}
$$

Solution: Notice that $A$ is a matrix for which all entries above the diagonal are $0$'s:

$$
A=\begin{bmatrix}7 & 0 & 0 \\ 3 & -1 & 0 \\ 0 & 5 & 0\end{bmatrix}
$$

Therefore, it is a lower triangular matrix.

It is not an upper triangular matrix or a diagonal matrix since there is a non-zero element below the diagonal: ${a}_{21}=3\ne 0.$

Answer selection: Lower triangular matrix

Question 17592186120121 — None

How can we best describe the following matrix?

$$
\displaystyle A = \begin{bmatrix}3 & 0 & 0 \\ 6 & 8 & 0 \\ 4 & 5 & 1\end{bmatrix}
$$

Solution: 

Question 17592186262602 — question.difficulty/easy

How can we best describe the following matrix? 

$$
C=\begin{bmatrix}-1 & 0 \\ -5 & 3\end{bmatrix}
$$

Solution: Notice that $C$ is a matrix for which all entries above the diagonal are $0$'s:

$$
C=\begin{bmatrix}-1 & 0 \\ -5 & 3\end{bmatrix}
$$

Therefore, it is a lower triangular matrix.

It is not an upper triangular matrix or a diagonal matrix since there is a non-zero element below the diagonal: ${c}_{21}=-5\ne 0.$

Answer selection: Lower triangular matrix

### Identifying a Triangular Matrix (33 captured questions)

Question 17592186120421 — question.difficulty/moderate

Which of the following matrices are upper triangular matrices?

Select all that apply.

Solution: The matrix $A$ is an upper triangular matrix since all the entries below the main diagonal are zeros.

The matrices $B$ and $C$ are *not* upper triangular matrices since they each have a non-zero element below the main diagonal: 

$$
\begin{aligned}{b}_{31} & =5\ne 0 \\ {c}_{32} & =3\ne 0\end{aligned}
$$

Answer $A=\begin{bmatrix}8 & 0 & -1 & 0 \\ 0 & 0 & 0 & 7 \\ 0 & 0 & -4 & 5 \\ 0 & 0 & 0 & 1\end{bmatrix}$: true

Answer $B=\begin{bmatrix}1 & 0 & 6 \\ 0 & -1 & 3 \\ 5 & 7 & 11\end{bmatrix}$: false

Answer $C=\begin{bmatrix}2 & 0 & 1 \\ 0 & 1 & 0 \\ 0 & 3 & 0\end{bmatrix}$: false

Question 17592186120504 — question.difficulty/easy

Which of the following is an upper triangular matrix?

Solution: Notice that $C$ is a matrix for which all entries *below* the diagonal are $0$'s:

$$
C=\begin{bmatrix}3 & 0 & 0 \\ 0 & -5 & 1 \\ 0 & 0 & 2\end{bmatrix}
$$

Hence, it is an upper triangular matrix. 

By contrast, matrices $A$, $B$, $D$, and $E$ each have at least one non-zero entry below the diagonal:

$$
A=\begin{bmatrix}1 & 0 \\ 2 & 3\end{bmatrix},\,B=\begin{bmatrix}2 & 0 & 0 \\ 0 & 5 & 0 \\ 0 & 1 & -3\end{bmatrix},\,D=\begin{bmatrix}0 & 1 \\ 1 & 0\end{bmatrix},\,E=\begin{bmatrix}2 & 4 & 0 \\ 4 & 0 & 4 \\ 0 & 4 & 2\end{bmatrix}.
$$

So, they are not upper triangular matrices.

Answer selection: C=\begin{bmatrix}3 & 0 & 0 \\ 0 & -5 & 1 \\ 0 & 0 & 2\end{bmatrix}

Question 17592186262604 — question.difficulty/moderate

Which of the following matrices are lower triangular matrices?

Select all that apply.

Solution: The matrices $A$ and $B$ are lower triangular matrices since all the entries above the main diagonal are zeros.

The matrix $C$ is *not* a lower triangular matrix since it has a non-zero element above the main diagonal: 

$$
\begin{aligned}{c}_{12} & =-2\ne 0\end{aligned}
$$

Answer $A=\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix}$: true

Answer $B=\begin{bmatrix}5 & 0 \\ -1 & 2\end{bmatrix}$: true

Answer $C=\begin{bmatrix}1 & -2 \\ 0 & 5\end{bmatrix}$: false

### Identifying Correct Statements About a Matrix (18 captured questions)

Question 17592186120422 — question.difficulty/moderate

Consider the matrix

$$
A=\begin{bmatrix}4 & 0 & 0 \\ 2 & 1 & 0 \\ 0 & 5 & 3\end{bmatrix}
$$

Which of the following statements are true?

Select all that apply.

Solution: Let's analyze each statement in turn.

- $A$ is upper triangular: **False.** This fails because $A$ has non-zero entries below the main diagonal:

$$
A=\begin{bmatrix}4 & 0 & 0 \\ 2 & 1 & 0 \\ 0 & 5 & 3\end{bmatrix}
$$

- $A$ is lower triangular: **True.** All the entries above the main diagonal of $A$ are zeros:

$$
A=\begin{bmatrix}4 & 0 & 0 \\ 2 & 1 & 0 \\ 0 & 5 & 3\end{bmatrix}
$$

- ${A}^{T}$ is upper triangular: **True.** All the entries below the main diagonal of ${A}^{T}$ are zeros:

$$
{A}^{T}=\begin{bmatrix}4 & 2 & 0 \\ 0 & 1 & 5 \\ 0 & 0 & 3\end{bmatrix}
$$

The true statements are:

- $A$ is lower triangular.
- ${A}^{T}$ is upper triangular.

Answer $A$ is lower triangular.: true

Answer $A$ is upper triangular.: false

Answer ${A}^{T}$ is upper triangular.: true

Question 17592186120426 — None

Consider the matrix

$$
A=\begin{bmatrix}-3 & 1 & 0 \\ -1 & 1 & 0 \\ 0 & 0 & 5\end{bmatrix}
$$

Which of the following statements are true?

Select all that apply.

Solution: $A$ is neither upper nor lower triangular because $a_{12}=1$ and $a_{21}=-1$ are both nonzero. However,

$$
A^{T}+A=\begin{bmatrix}-6 & 0 & 0 \\ 0 & 2 & 0 \\ 0 & 0 & 10\end{bmatrix}
$$

is diagonal, so $A^{T}+A$ is upper triangular.

Answer $A$ is lower triangular.: false

Answer $A$ is upper triangular.: false

Answer $A^{T} + A$ is upper triangular.: true

Answer None of the above: false

Question 17592186262616 — question.difficulty/hard

Consider the matrix

$$
B=\begin{bmatrix}2 & 0 & 0 & 0 \\ 0 & -3 & -1 & 1 \\ 0 & 0 & 4 & 5 \\ 0 & 0 & 0 & 2\end{bmatrix}
$$

Which of the following statements are true?

Select all that apply.

Solution: Let's analyze each statement in turn.

- $B$ is upper triangular: **True.** This holds because all the entries below the main diagonal equal to zero:

$$
B=\begin{bmatrix}2 & 0 & 0 & 0 \\ 0 & -3 & -1 & 1 \\ 0 & 0 & 4 & 5 \\ 0 & 0 & 0 & 2\end{bmatrix}
$$

- $B$ is lower triangular: **False.** This fails because $B$ has non-zero entries above the main diagonal:

$$
B=\begin{bmatrix}2 & 0 & 0 & 0 \\ 0 & -3 & -1 & 1 \\ 0 & 0 & 4 & 5 \\ 0 & 0 & 0 & 2\end{bmatrix}
$$

- $B-{B}^{T}$ is upper triangular: **False.** This fails because the result of $B-{B}^{T}$ has non-zero entries below the main diagonal:

$$
B-{B}^{T}=\begin{bmatrix}0 & 0 & 0 & 0 \\ 0 & 0 & -1 & 1 \\ 0 & 1 & 0 & 5 \\ 0 & -1 & -5 & 0\end{bmatrix}
$$

The true statements are:

- $B$ is upper triangular.

Answer $B$ is lower triangular.: false

Answer $B$ is upper triangular.: true

Answer $B-{B}^{T}$ is upper triangular.: false
