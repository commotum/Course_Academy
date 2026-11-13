# 17592186049548 Inverses of 2x2 Matrices

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186088895 — Introduction

Given a $2 \times 2$ matrix

<div class="matrix-operands matrix-operands-stacked">
<div>$A =\begin{bmatrix}a & b \\ c & d\end{bmatrix}$</div>
</div>

the **inverse** of $A$ can be found using the following formula:

$$
\begin{aligned}{A}^{-1} & =\frac{1}{\det (A)}\begin{bmatrix}d & -b \\ -c & a\end{bmatrix}.\end{aligned}
$$



### example 17592186087508 — Calculating the Inverse of a 2x2 Matrix

Calculate $A^{-1},$ where

$$
A = \begin{bmatrix}{\color{blue}{1}} & 0 \\ -2 & {\color{red}{1}}\end{bmatrix}.
$$

Given a $2 \times 2$ matrix

<div class="matrix-operands matrix-operands-stacked">
<div>$A =\begin{bmatrix}a & b \\ c & d\end{bmatrix}$</div>
</div>

the inverse of $A$ can be found using the following formula:

$$
\begin{aligned}{A}^{-1} & =\frac{1}{\det (A)}\begin{bmatrix}d & -b \\ -c & a\end{bmatrix}.\end{aligned}
$$

First, we compute the determinant:

$$
\det(A) = 1 \cdot 1 - 0 \cdot (-2) = 1
$$

Using the formula, then, the inverse is given by

$$
\begin{aligned}{A}^{-1} & =\frac{1}{\det (A)}\begin{bmatrix}d & -b \\ -c & a\end{bmatrix}. \\  & =\frac{1}{1}\begin{bmatrix}1 & -0 \\ -(-2) & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 2 & 1\end{bmatrix}.\end{aligned}
$$

We can verify the result as follows:

$$
\begin{aligned}A{A}^{-1} & =\begin{bmatrix}1 & 0 \\ -2 & 1\end{bmatrix}\begin{bmatrix}1 & 0 \\ 2 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}\,✓ \\ {A}^{-1}A & =\begin{bmatrix}1 & 0 \\ 2 & 1\end{bmatrix}\begin{bmatrix}1 & 0 \\ -2 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}\,✓\end{aligned}
$$

### tutorial 17592186088896 — Invertible and Singular Matrices

Remember that the inverse of a $2\times 2$ matrix <div class="matrix-operands matrix-operands-stacked">
<div>$A=\begin{bmatrix}a & b \\ c & d\end{bmatrix}$</div>
</div> is given by

$$
A^{-1} = \dfrac{1}{\det(A)}
\begin{bmatrix}d & -b \\ -c & a\end{bmatrix}.
$$

If $\det(A)=0,$ then $A^{-1}$ doesn't exist since we can't divide by zero. In fact, we have the following statement:

> $A^{-1}$ exists if and only if $\det(A) \neq 0.$

A matrix that has an inverse is called **invertible**. Otherwise, the matrix doesn't have an inverse and is called **non-invertible**. A square matrix that is non-invertible is called **singular**.



### example 17592186087509 — Identifying Singular Matrices

Which of the matrices below are singular?

<div class="matrix-operands matrix-operands-stacked">
<div>$A =\begin{bmatrix}1 & 1 \\ 1 & 1\end{bmatrix}$</div>
<div>$B =\begin{bmatrix}1 & -2 \\ 1 & 2 \\ -2 & 0\end{bmatrix}$</div>
<div>$C =\begin{bmatrix}3 & -3 \\ 3 & 3\end{bmatrix}$</div>
</div>

- For the matrix $A$, we have

$$
\det({A})=1 \cdot 1 - 1 \cdot 1 = 0.
$$

Because $\det(A)=0,$ we conclude that $A$ is not invertible. Since $A$ is a square matrix that is not invertible, we also say that $A$ is singular.

- The matrix $B$ is a $3 \times 2$ matrix. So, it is not invertible. Since the matrix is not square, we can't say that it's singular.

- For the matrix $C$, we have

$$
\det({C})=3 \cdot 3 - (-3) \cdot 3 = 18.
$$

Because $\det(C) \neq 0,$ we conclude that $C$ is invertible.

Therefore, only $A$ is singular.

### example 17592186087510 — Solving for a Variable in a Singular Matrix

If 
$$
\displaystyle A =
 \begin{bmatrix}1-k & 2 \\ 2 & 1-k\end{bmatrix}
$$
 is a singular matrix, calculate the value(s) of $k.$

The matrix $A$ is singular if and only if $\det(A)=0.$ Calculating the determinant, we get

$$
\begin{aligned}\det (A) & =(1-k)(1-k)-4 \\  & ={k}^{2}-2k-3.\end{aligned}
$$

Now, we set the determinant equal to $0$ and solve for $k\mathbin{:}$

$$
\begin{aligned}{k}^{2}-2k-3 & =0 \\ (k-3)(k+1) & =0 \\ k & =3,-1\end{aligned}
$$

Therefore, the values of $k$ are $k=3$ and $k=-1.$

### tutorial 17592186088897 — Verifying the Formula

Given a matrix $A = 
	\begin{bmatrix}a & b \\ c & d\end{bmatrix},$
we have been using the following formula to compute the inverse:

$$
A^{-1} = \dfrac{1}{ad-bc}
	\begin{bmatrix}d & -b \\ -c & a\end{bmatrix}
$$

To check that this formula is correct for a general matrix $A$, we need to verify that

$$
AA^{-1} = A^{-1}A = I_2.
$$

First, we compute $A^{-1}A\mathbin{:}$

$$
\begin{aligned}{A}^{-1}\cdot A & =\frac{1}{ad-bc}\begin{bmatrix}d & -b \\ -c & a\end{bmatrix}\cdot \begin{bmatrix}a & b \\ c & d\end{bmatrix} \\  & =\frac{1}{ad-bc}\begin{bmatrix}ad-bc & 0 \\ 0 & -bc+ad\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}\,{\color{green}✓}\end{aligned}
$$

Then, we compute $A A^{-1}\mathbin{:}$

$$
\begin{aligned}A\cdot {A}^{-1} & =\begin{bmatrix}a & b \\ c & d\end{bmatrix}\cdot \frac{1}{ad-bc}\begin{bmatrix}d & -b \\ -c & a\end{bmatrix} \\  & =\frac{1}{ad-bc}\begin{bmatrix}a & b \\ c & d\end{bmatrix}\cdot \begin{bmatrix}d & -b \\ -c & a\end{bmatrix} \\  & =\frac{1}{ad-bc}\begin{bmatrix}ad-bc & 0 \\ 0 & -bc+ad\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}\,{\color{green}✓}\end{aligned}
$$

So, we have verified that

$$
AA^{-1} = A^{-1}A = I_2,
$$

and we can be sure that the given formula is the correct formula for $A^{-1}.$



## Representative practice (first three per skill; full bank in practice.json)

### Calculating the Inverse of a 2x2 Matrix (23 captured questions)

Question 17592186087992 — None

Calculate $A^{-1}$, where
$$
\displaystyle A = \begin{bmatrix}7 & 2 \\ 4 & 1\end{bmatrix}.
$$

Solution: Given a $2\times2$ matrix, use the formula

$$
\begin{bmatrix}a&b\\c&d\end{bmatrix}^{-1}=\frac{1}{ad-bc}\begin{bmatrix}d&-b\\-c&a\end{bmatrix}.
$$

First, compute the determinant:

$$
\det(A)=(7)(1)-(2)(4)=-1.
$$

Since the determinant is nonzero, the inverse exists. Thus,

$$
A^{-1}=\frac{1}{-1}\begin{bmatrix}1 & -2 \\ -4 & 7\end{bmatrix}=\begin{bmatrix}-1 & 2 \\ 4 & -7\end{bmatrix}.
$$

Multiplying in either order gives the identity matrix, which verifies the result.

Answer selection: \begin{bmatrix}-1 & 2 \\ 4 & -7\end{bmatrix}

Question 17592186088369 — None

Calculate $Z^{-1}$ where
$$
\displaystyle Z = \begin{bmatrix}9 & -1 \\ 2 & 1\end{bmatrix}.
$$

Solution: Given a $2\times2$ matrix, use the formula

$$
\begin{bmatrix}a&b\\c&d\end{bmatrix}^{-1}=\frac{1}{ad-bc}\begin{bmatrix}d&-b\\-c&a\end{bmatrix}.
$$

First, compute the determinant:

$$
\det(Z)=(9)(1)-(-1)(2)=11.
$$

Since the determinant is nonzero, the inverse exists. Thus,

$$
Z^{-1}=\frac{1}{11}\begin{bmatrix}1 & 1 \\ -2 & 9\end{bmatrix}=\begin{bmatrix}\frac{1}{11} & \frac{1}{11} \\ - \frac{2}{11} & \frac{9}{11}\end{bmatrix}.
$$

Multiplying in either order gives the identity matrix, which verifies the result.

Answer selection: \frac{1}{11}\begin{bmatrix}1 & 1 \\ -2 & 9\end{bmatrix}

Question 17592186262820 — question.difficulty/moderate

Calculate ${B}^{-1}$, where 
$$
\displaystyle B=\begin{bmatrix}2 & 1 \\ 1 & 0\end{bmatrix}.
$$

Solution: Given a $2\times 2$ matrix

$$
B=\begin{bmatrix}a & b \\ c & d\end{bmatrix},
$$

the inverse of $B$ can be found using the following formula:

$$
\begin{aligned}{B}^{-1} & =\frac{1}{\det (B)}\begin{bmatrix}d & -b \\ -c & a\end{bmatrix}.\end{aligned}
$$

First, we compute the determinant:

$$
\det (B)=2\cdot 0-1\cdot 1=-1
$$

Using the formula, then, the inverse is given by

$$
\begin{aligned}{B}^{-1} & =\frac{1}{\det (B)}\begin{bmatrix}d & -b \\ -c & a\end{bmatrix} \\  & =\frac{1}{(-1)}\begin{bmatrix}0 & -1 \\ -1 & 2\end{bmatrix} \\  & =\begin{bmatrix}0 & 1 \\ 1 & -2\end{bmatrix}.\end{aligned}
$$

We can verify the result as follows:

$$
\begin{aligned}B{B}^{-1} & =\begin{bmatrix}2 & 1 \\ 1 & 0\end{bmatrix}\begin{bmatrix}0 & 1 \\ 1 & -2\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}\,{\color{green}✓} \\ {B}^{-1}B & =\begin{bmatrix}0 & 1 \\ 1 & -2\end{bmatrix}\begin{bmatrix}2 & 1 \\ 1 & 0\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}\,{\color{green}✓}\end{aligned}
$$

Answer selection: \begin{bmatrix}0 & 1 \\ 1 & -2\end{bmatrix}

### Identifying Singular Matrices (32 captured questions)

Question 17592186087989 — question.difficulty/easy

Which of the matrices below are singular?

Select all that apply.

Solution: - For the matrix $A$, we have

$$
\det (A)=0\cdot 0-1\cdot 1=-1.
$$

Because $\det (A)\ne 0,$ we conclude that $A$ is invertible.

- The matrix $B$ is a $3\times 1$ matrix. So, it is not invertible. Since the matrix is not square, we can't say that it's singular.

- For the matrix $C$, we have

$$
\det (C)=1\cdot 0-0\cdot 1=0.
$$

Because $\det (C)=0,$ we conclude that $C$ is not invertible. Since $C$ is a square matrix that is not invertible, we also say that $C$ is singular.

Therefore, only $C$ is singular.

Answer $A=\begin{bmatrix}0 & 1 \\ 1 & 0\end{bmatrix}$: false

Answer $B=\begin{bmatrix}1 \\ 1 \\ -2\end{bmatrix}$: false

Answer $C=\begin{bmatrix}1 & 0 \\ 0 & 0\end{bmatrix}$: true

Question 17592186087993 — question.difficulty/easy

Which of the matrices below does **not** have an inverse?

Select all that apply.

Solution: - The matrix $A$ is a $2\times 3$ matrix. So, it is not invertible.

- For the matrix $B$, we have

$$
\det (B)=6\cdot 4-8\cdot 3=0.
$$

Because $\det (B)=0,$ we conclude that $B$ is not invertible.

- For the matrix $C$, we have

$$
\det (C)=(-1)\cdot 5-1\cdot 5=-10.
$$

Because $\det (C)\ne 0,$ we conclude that $C$ is invertible.

Therefore, only $A$ and $B$ do not have an inverse.

Answer $A=\begin{bmatrix}1 & 5 & 0 \\ -1 & 1 & -1\end{bmatrix}$: true

Answer $B=\begin{bmatrix}6 & 8 \\ 3 & 4\end{bmatrix}$: true

Answer $C=\begin{bmatrix}-1 & 1 \\ 5 & 5\end{bmatrix}$: false

Question 17592186253311 — question.difficulty/easy

Which of the matrices below are singular?

Select all that apply.

Solution: - For the matrix $H$, we have

$$
\det (H)=5\cdot 0-3\cdot 0=0.
$$

Because $\det (H)=0,$ we conclude that $H$ is not invertible. Since $H$ is a square matrix that is not invertible, we also say that $H$ is singular.

- For the matrix $J$, we have

$$
\det (J)=2\cdot 6-3\cdot 4=0.
$$

Because $\det (J)=0,$ we conclude that $J$ is not invertible. Since $J$ is a square matrix that is not invertible, we also say that $J$ is singular.

- The matrix $K$ is a $3\times 2$ matrix. So, it is not invertible. Since the matrix is not square, we can't say that it's singular.

Therefore, only $H$ and $J$ is singular.

Answer $H=\begin{bmatrix}5 & 0 \\ 3 & 0\end{bmatrix}$: true

Answer $J=\begin{bmatrix}2 & 4 \\ 3 & 6\end{bmatrix}$: true

Answer $K=\begin{bmatrix}1 & 4 \\ 0 & 5 \\ -3 & 0\end{bmatrix}$: false

### Solving for a Variable in a Singular Matrix (36 captured questions)

Question 17592186087990 — None

If $A = \begin{bmatrix}k & 2 \\ 2 & k\end{bmatrix}$ is a singular matrix, calculate the value(s) of $k$.

Solution: The matrix $A$ is singular if and only if its determinant is $0$. Calculating the determinant, we get

$$
\det(A)=k\cdot k-2\cdot2=k^2-4.
$$

Now, set the determinant equal to $0$ and solve for $k$:

$$
\begin{aligned}k^2-4&=0\\(k-2)(k+2)&=0\\k&=2\quad\text{or}\quad k=-2.\end{aligned}
$$

Therefore, $k=\pm2$.

Answer selection: k = ± 2

Question 17592186087991 — question.difficulty/easy

If $A=\begin{bmatrix}k & k \\ 2 & 1\end{bmatrix}$ is a singular matrix, calculate the value of $k.$

Solution: The matrix $A$ is singular if and only if $\det (A)=0.$ Calculating the determinant, we get

$$
\begin{aligned}\det (A) & =k\cdot 1-k\cdot 2 \\  & =k-2k \\  & =-k\end{aligned}
$$

Now, we set the determinant equal to $0$ and solve for $k:$

$$
\begin{aligned}-k & =0 \\ k & =0\end{aligned}
$$

Therefore, the value of $k$ is $k=0.$

Answer selection: k=0

Question 17592186253312 — question.difficulty/moderate

If $F=\begin{bmatrix}3 & t \\ t & 3\end{bmatrix}$ is a singular matrix, calculate the value(s) of $t.$

Solution: The matrix $F$ is singular if and only if $\det (F)=0.$ Calculating the determinant, we get

$$
\begin{aligned}\det (F) & =3\cdot 3-t\cdot t \\  & =9-{t}^{2}.\end{aligned}
$$

Now, we set the determinant equal to $0$ and solve for $t:$

$$
\begin{aligned}9-{t}^{2} & =0 \\ {t}^{2} & =9 \\ t & =\pm 3\end{aligned}
$$

Therefore, the values of $t$ are $t=\pm 3.$

Answer selection: t=\pm 3
