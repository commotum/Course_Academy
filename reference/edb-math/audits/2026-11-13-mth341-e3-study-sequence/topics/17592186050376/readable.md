# 17592186050376 The Characteristic Equation of a Matrix

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186125785 — Introduction

We can find the eigenvalues of a $3\times 3$ matrix in much the same way as for $2\!\times\! 2$ matrices. 

Remember, $\lambda$ is an eigenvalue of $A$ if $A\mathbf{v} = \lambda\mathbf{v}$ for some non-zero vector $\mathbf{v}$. This implies that the equation

$$(A-\lambda I)\mathbf{v}=\mathbf{0}$$

has a non-trivial solution, which means that the matrix $A-\lambda I$ is singular, and consequently
$\det(A-\lambda I)=0.$
Therefore, if we want to find the eigenvalues of a $n\!\times\! n$ matrix $A,$ we have to find the solutions of the characteristic equation

$$
\det(A-\lambda I)=0.
$$

Let's go through this process in the case of the matrix $A,$ given by

$$
A=
{\left[ \begin{array}{ccc}- 2 & 0 & 0 \\ 0 & - 8 & 0 \\ 0 & 0 & 5\end{array} \right]}.
$$

First, we write down the matrix $A-\lambda I{:}$



$$
\begin{aligned}A-\lambda I & =\begin{bmatrix}-2 & 0 & 0 \\ 0 & -8 & 0 \\ 0 & 0 & 5\end{bmatrix}-\begin{bmatrix}\lambda  & 0 & 0 \\ 0 & \lambda  & 0 \\ 0 & 0 & \lambda \end{bmatrix} \\  & =\begin{bmatrix}-2-\lambda  & 0 & 0 \\ 0 & -8-\lambda  & 0 \\ 0 & 0 & 5-\lambda \end{bmatrix}\end{aligned}
$$

Now, we set and solve the characteristic equation $\,\det(A-\lambda I)=0.$ Using the fact that the determinant of a triangular (or diagonal) matrix is given by the product of the elements on the main diagonal, we get the following:

$$
\begin{aligned}\det(A-\lambda I) & =0 \\ \begin{vmatrix}-2-\lambda  & 0 & 0 \\ 0 & -8-\lambda  & 0 \\ 0 & 0 & 5-\lambda \end{vmatrix} & =0 \\ (-2-\lambda )(-8-\lambda )(5-\lambda ) & =0 \\ (\lambda +2)(\lambda +8)(\lambda -5) & =0\end{aligned}
$$

So, the eigenvalues of the matrix $A$ are $\lambda=-2,$ $\lambda=-8,$ and $\lambda=5.$



### example 17592186124331 — Calculating the Eigenvalues of a 3x3 Matrix Containing a Block of Zeros

Determine all real eigenvalues $\lambda$ of the matrix 
$$
A=
{\left[ \begin{array}{ccc}- 9 & 4 & 8 \\ 0 & 9 & - 7 \\ 0 & 0 & 6\end{array} \right]}.
$$

First, we find the matrix $\, A-\lambda I \mathbin{:}$
$$
\displaystyle A - \lambda I = 
{\left[ \begin{array}{ccc}- 9 - \lambda  & 4 & 8 \\ 0 & 9 - \lambda  & - 7 \\ 0 & 0 & 6 - \lambda \end{array} \right]}
$$

The characteristic equation is $\det(A-\lambda I) = 0.$ 

Since the determinant of a triangular (or diagonal) matrix is given by the product of the entries on the main diagonal, we obtain the following: 

$$
\begin{aligned}\det(A-\lambda I) & =0 \\ \begin{vmatrix}-9-\lambda  & 4 & 8 \\ 0 & 9-\lambda  & -7 \\ 0 & 0 & 6-\lambda \end{vmatrix} & =0 \\ (-9-\lambda )(9-\lambda )(6-\lambda ) & =0 \\ (\lambda +9)(\lambda -9)(\lambda -6) & =0\end{aligned}
$$

Therefore, the eigenvalues are $\lambda_1=-9,$ $\lambda_2=9,$ and $\lambda_3=6.$ 

**Note:** The eigenvalues of a triangular (or diagonal) matrix are always the entries on the main diagonal.

### tutorial 17592186125786 — The Algebraic Multiplicity of an Eigenvalue

The **algebraic multiplicity** of an eigenvalue $\lambda$ is the number of times it is a solution of the characteristic equation. 

For example, consider a $6\times 6$ matrix $A$ with the following characteristic equation:

$$(\lambda-{\color{red}4})(\lambda-{\color{red}4})(\lambda-1)(\lambda+8)^{\color{blue}3} =0$$

The eigenvalue $\lambda={\color{red}4}$ is a double root. Therefore, it has algebraic multiplicity $2.$ 

By the same reasoning, we say that 

- $\lambda=1$ has algebraic multiplicity $1,$ and

- $\lambda=-8$ has algebraic multiplicity $\color{blue}3$.



### example 17592186124380 — Calculating the Eigenvalues of a 4x4 Matrix Containing a Block of Zeros

$$
P=
{\left[ \begin{array}{cccc}3 & 0 & - 8 & - 2 \\ 0 & - 1 & 3 & 5 \\ 0 & 0 & 4 & 0 \\ 0 & 7 & - 3 & 1\end{array} \right]}.
$$

Consider the matrix $P$ given above. Which of the following statements are true?

I. $\lambda=4$ is an eigenvalue of $P$

II. $\lambda=-1$ is an eigenvalue of $P$

III. The eigenvalue $\lambda=6$ has algebraic multiplicity $2$

First, we find the matrix $\, P-\lambda I \mathbin{:}$
$$
\displaystyle P - \lambda I = 
{\left[ \begin{array}{cccc}3 - \lambda  & 0 & - 8 & - 2 \\ 0 & - 1 - \lambda  & 3 & 5 \\ 0 & 0 & 4 - \lambda  & 0 \\ 0 & 7 & - 3 & 1 - \lambda \end{array} \right]}
$$

The characteristic equation is $\det(P-\lambda I) = 0.$ 

Notice that we can expand the $4 \times 4$ determinant across the $1$st column, as follows:

$$
\begin{aligned}\det(P-\lambda I) & =0 \\ \begin{vmatrix}3-\lambda  & 0 & -8 & -2 \\ 0 & -1-\lambda  & 3 & 5 \\ 0 & 0 & 4-\lambda  & 0 \\ 0 & 7 & -3 & 1-\lambda \end{vmatrix} & =0 \\ (3-\lambda )\begin{vmatrix}-1-\lambda  & 3 & 5 \\ 0 & 4-\lambda  & 0 \\ 7 & -3 & 1-\lambda \end{vmatrix} & =0\end{aligned}
$$

Now, expanding the $3 \times 3$ determinant across the $2$nd row, we obtain the following:

$$
\begin{aligned}(3-\lambda )\cdot (4-\lambda )\begin{vmatrix}-1-\lambda  & 5 \\ 7 & 1-\lambda \end{vmatrix} & =0 \\ (3-\lambda )(4-\lambda )((-1-\lambda )(1-\lambda )-35) & =0 \\ (3-\lambda )(4-\lambda )({\lambda }^{2}-36) & =0 \\ (\lambda -3)(\lambda -4)(\lambda -6)(\lambda +6) & =0\end{aligned}
$$

So, the eigenvalues of $P$ are $\lambda=3,$ $\lambda=4,$ $\lambda=6,$ and $\lambda=-6$ (all with algebraic multiplicity $1$).

Therefore, the correct answer is "I only."

### example 17592186124332 — Finding the Eigenvalues of a General 3x3 Matrix

Determine all real eigenvalues $\lambda$ of the matrix 
$$
A=
{\left[ \begin{array}{ccc}1 & - 1 & - 2 \\ - 1 & 1 & - 2 \\ - 2 & - 2 & - 7\end{array} \right]}.
$$

First, we find the matrix $A-\lambda I{:}$
$$
\displaystyle A - \lambda I = 
{\left[ \begin{array}{ccc}1 - \lambda  & - 1 & - 2 \\ - 1 & 1 - \lambda  & - 2 \\ - 2 & - 2 & - 7 - \lambda \end{array} \right]}
$$

The characteristic equation is given by $\det(A-\lambda I)=0.$ 

Expanding the determinant across the $1$st row, we get the following:

$$
\begin{array}{cc}\det  ( A - \lambda  I ) &  = 0 \\ \left| \begin{array}{ccc}1 - \lambda  & - 1 & - 2 \\ - 1 & 1 - \lambda  & - 2 \\ - 2 & - 2 & - 7 - \lambda \end{array} \right| &  = 0 \\ ( 1 - \lambda  ) \left| \begin{array}{cc}1 - \lambda  & - 2 \\ - 2 & - 7 - \lambda \end{array} \right| - ( - 1 ) \left| \begin{array}{cc}- 1 & - 2 \\ - 2 & - 7 - \lambda \end{array} \right| + ( - 2 ) \left| \begin{array}{cc}- 1 & 1 - \lambda  \\ - 2 & - 2\end{array} \right| &  = 0 \\ ( - {\lambda }^{3} - 5 {\lambda }^{2} + 17 \lambda  - 11 ) + ( 3 + \lambda  ) - 2 ( 4 - 2 \lambda  ) &  = 0 \\ - {\lambda }^{3} - 5 {\lambda }^{2} + 22 \lambda  - 16 &  = 0 \\ {\lambda }^{3} + 5 {\lambda }^{2} - 22 \lambda  + 16 &  = 0\end{array}
$$

Now, we need to solve this equation. We find the first root by testing some values. According to the rational zeros theorem, a list of good first guesses consists of all divisors of $16\mathbin{:}$ 
$$
\pm1, \pm2, \pm4, \pm8, \pm 16
$$

Let's pick $\lambda=1.$ Substituting to the characteristic equation gives
$$
\begin{array}{rl}\displaystyle ( 1 {)}^{3} + 5 ( 1 {)}^{2} - 22 ( 1 ) + 16 & \displaystyle  = 0.\end{array}
$$
So, $\lambda=1$ is a root of the equation. This means we can factor $(\lambda-1)$ out of $\lambda^3 +5 \lambda^2 - 22 \lambda + 16$ using synthetic division:



<div class="source-table-scroll"><table class="source-table" data-rules="all" data-table-align="center">
<tbody><tr data-next-row="true">
<td data-cell-align="center" data-fill="#D6EAF8" data-border-top="none" data-border-right="solid" data-border-bottom="none" data-border-left="none">$1$</td>
<td data-cell-align="center" data-border-top="none" data-border-right="none" data-border-bottom="none" data-border-left="none">$1$</td>
<td data-cell-align="center" data-border-top="none" data-border-right="none" data-border-bottom="none" data-border-left="none">$5$</td>
<td data-cell-align="center" data-border-top="none" data-border-right="none" data-border-bottom="none" data-border-left="none">$-22$</td>
<td data-cell-align="center" data-border-top="none" data-border-right="none" data-border-bottom="none" data-border-left="none">$16$</td>
</tr>
<tr data-next-row="true">
<td data-cell-align="center" data-border-top="none" data-border-right="solid" data-border-bottom="none" data-border-left="none"></td>
<td data-cell-align="center" data-border-top="none" data-border-right="none" data-border-bottom="solid" data-border-left="none">$\color{lightgray}\downarrow$</td>
<td data-cell-align="center" data-border-top="none" data-border-right="none" data-border-bottom="solid" data-border-left="none">$1$</td>
<td data-cell-align="center" data-border-top="none" data-border-right="none" data-border-bottom="solid" data-border-left="none">$6$</td>
<td data-cell-align="center" data-border-top="none" data-border-right="none" data-border-bottom="solid" data-border-left="none">$-16$</td>
</tr>
<tr>
<td data-cell-align="center" data-border-top="none" data-border-right="none" data-border-bottom="none" data-border-left="none"></td>
<td data-cell-align="center" data-border-top="none" data-border-right="none" data-border-bottom="none" data-border-left="none">$1$</td>
<td data-cell-align="center" data-border-top="none" data-border-right="none" data-border-bottom="none" data-border-left="none">$6$</td>
<td data-cell-align="center" data-border-top="none" data-border-right="none" data-border-bottom="none" data-border-left="none">$-16$</td>
<td data-cell-align="center" data-fill="#EEEEEE" data-border-top="solid" data-border-right="solid" data-border-bottom="solid" data-border-left="solid">$0$</td>
</tr>
</tbody></table></div>


So, we obtain the following factorization:
$$
\begin{aligned}
(λ - 1)(λ^{2} + 6λ - 16) &= 0 \\
(λ - 1)(λ - 2)(λ + 8) &= 0
\end{aligned}
$$

Therefore, the eigenvalues are $\lambda_1=1,$ $\lambda_2=2,$ and $\,\lambda_3=-8.$

## Representative practice (first three per skill; full bank in practice.json)

### Calculating the Eigenvalues of a 3x3 Matrix Containing a Block of Zeros (12 captured questions)

Question 17592186125012 — question.difficulty/easy

Determine all real eigenvalues $λ$ of the matrix
$$
\displaystyle A = \begin{bmatrix}3 & 0 & 0 \\ 1 & -2 & 0 \\ -2 & 3 & 4\end{bmatrix}.
$$

Solution: The eigenvalues satisfy the characteristic equation $\det(A-\lambda I)=0$. We have

$$
A-\lambda I=\begin{bmatrix}3 - \lambda & 0 & 0 \\ 1 & - \lambda - 2 & 0 \\ -2 & 3 & 4 - \lambda\end{bmatrix}.
$$

This matrix is triangular, so its determinant is the product of the diagonal entries.

$$
\det(A-\lambda I)=- \lambda^{3} + 5 \lambda^{2} + 2 \lambda - 24=- \left(\lambda - 4\right) \left(\lambda - 3\right) \left(\lambda + 2\right)=0.
$$

Therefore, the real eigenvalues are $-2, 3, 4$.

Answer selection: λ ∈ {-2, 3, 4}

Question 17592186125017 — question.difficulty/moderate

Find the characteristic equation of the matrix 
$$
\displaystyle A=\begin{bmatrix}-3 & 2 & -1 \\ 5 & 2 & 3 \\ 0 & 0 & 1\end{bmatrix}.
$$

Solution: First, we find the matrix $\,A-\lambda I:$


$$
A-\lambda I=\begin{bmatrix}-3-\lambda  & 2 & -1 \\ 5 & 2-\lambda  & 3 \\ 0 & 0 & 1-\lambda \end{bmatrix}
$$

The characteristic equation is $\det(A-\lambda I)=0.$ 

Expanding the determinant across the $3$rd row, we obtain the following:  

$$
\begin{aligned}\det(A-\lambda I) & =0 \\ \begin{vmatrix}-3-\lambda  & 2 & -1 \\ 5 & 2-\lambda  & 3 \\ 0 & 0 & 1-\lambda \end{vmatrix} & =0 \\ (1-\lambda )\begin{vmatrix}-3-\lambda  & 2 \\ 5 & 2-\lambda \end{vmatrix} & =0 \\ (1-\lambda )((-3-\lambda )(2-\lambda )-2\cdot 5) & =0 \\ (1-\lambda )({\lambda }^{2}+\lambda -16) & =0\end{aligned}
$$

Answer selection: (1-\lambda )({\lambda }^{2}+\lambda -16)=0

Question 17592186323857 — question.difficulty/moderate

Find the characteristic equation of the matrix 
$$
\displaystyle A=\begin{bmatrix}-2 & 0 & -2 \\ 1 & -1 & -1 \\ -2 & 0 & 1\end{bmatrix}.
$$

Solution: First, we find the matrix $\,A-\lambda I:$


$$
A-\lambda I=\begin{bmatrix}-2-\lambda  & 0 & -2 \\ 1 & -1-\lambda  & -1 \\ -2 & 0 & 1-\lambda \end{bmatrix}
$$

The characteristic equation is $\det(A-\lambda I)=0.$ 

Expanding the determinant across the $2$nd column, we obtain the following:  

$$
\begin{aligned}\det(A-\lambda I) & =0 \\ \begin{vmatrix}-2-\lambda  & 0 & -2 \\ 1 & -1-\lambda  & -1 \\ -2 & 0 & 1-\lambda \end{vmatrix} & =0 \\ (-1-\lambda )\begin{vmatrix}-2-\lambda  & -2 \\ -2 & 1-\lambda \end{vmatrix} & =0 \\ (-1-\lambda )((-2-\lambda )(1-\lambda )-(-2)(-2)) & =0 \\ (-1-\lambda )({\lambda }^{2}+\lambda -6) & =0 \\ (\lambda +1)(\lambda +3)(\lambda -2) & =0\end{aligned}
$$

Answer selection: (\lambda +1)(\lambda +3)(\lambda -2)=0

### Calculating the Eigenvalues of a 4x4 Matrix Containing a Block of Zeros (12 captured questions)

Question 17592186125011 — question.difficulty/easy

Find the characteristic equation of the matrix 
$$
\displaystyle B=\begin{bmatrix}2 & 5 & 4 & 2 \\ 0 & -1 & 5 & 1 \\ 0 & 0 & 5 & 1 \\ 0 & 0 & 0 & 1\end{bmatrix}.
$$

Solution: First, we find the matrix $\,B-\lambda I:$


$$
B-\lambda I=\begin{bmatrix}2-\lambda  & 5 & 4 & 2 \\ 0 & -1-\lambda  & 5 & 1 \\ 0 & 0 & 5-\lambda  & 1 \\ 0 & 0 & 0 & 1-\lambda \end{bmatrix}
$$

The characteristic equation is $\det(B-\lambda I)=0.$ 

Since the determinant of a triangular (or diagonal) matrix is given by the product of the entries on the main diagonal, we obtain the following: 

$$
\begin{aligned}\det(B-\lambda I) & =0 \\ \begin{vmatrix}2-\lambda  & 5 & 4 & 2 \\ 0 & -1-\lambda  & 5 & 1 \\ 0 & 0 & 5-\lambda  & 1 \\ 0 & 0 & 0 & 1-\lambda \end{vmatrix} & =0 \\ (2-\lambda )(-1-\lambda )(5-\lambda )(1-\lambda ) & =0 \\ (\lambda -2)(\lambda +1)(\lambda -5)(\lambda -1) & =0\end{aligned}
$$

Answer selection: (\lambda -2)(\lambda +1)(\lambda -5)(\lambda -1)=0

Question 17592186125062 — question.difficulty/moderate

$$
P=\begin{bmatrix}-1 & -9 & -18 & -3 \\ 0 & -10 & 0 & 0 \\ 0 & 0 & -10 & 0 \\ -18 & 18 & -36 & -4\end{bmatrix}.
$$

Consider the matrix $P$ given above. Which of the following statements are true?

Select all that apply.

Solution: First, we find the matrix $\,P-\lambda I:$


$$
P-\lambda I=\begin{bmatrix}-1-\lambda  & -9 & -18 & -3 \\ 0 & -10-\lambda  & 0 & 0 \\ 0 & 0 & -10-\lambda  & 0 \\ -18 & 18 & -36 & -4-\lambda \end{bmatrix}
$$

The characteristic equation is $\det(P-\lambda I)=0.$ 

Notice that we can expand the $4\times 4$ determinant across the $2$nd row, as follows:

$$
\begin{aligned}\det(P-\lambda I) & =0 \\ \begin{vmatrix}-1-\lambda  & -9 & -18 & -3 \\ 0 & -10-\lambda  & 0 & 0 \\ 0 & 0 & -10-\lambda  & 0 \\ -18 & 18 & -36 & -4-\lambda \end{vmatrix} & =0 \\ (-10-\lambda )\begin{vmatrix}-1-\lambda  & -18 & -3 \\ 0 & -10-\lambda  & 0 \\ -18 & -36 & -4-\lambda \end{vmatrix} & =0\end{aligned}
$$

Now, expanding the $3\times 3$ determinant across the $2$nd row, we obtain the following:

$$
\begin{aligned}(-10-\lambda )\cdot (-10-\lambda )\begin{vmatrix}-1-\lambda  & -3 \\ -18 & -4-\lambda \end{vmatrix} & =0 \\ (-10-\lambda )^{2}((-1-\lambda )(-4-\lambda )-54) & =0 \\ (\lambda +10)^{2}({\lambda }^{2}+5\lambda -50) & =0 \\ (\lambda +10)^{2}(\lambda +10)(\lambda -5) & =0 \\ (\lambda +10)^{3}(\lambda -5) & =0\end{aligned}
$$

So, the eigenvalues of $P$ are $\lambda =-10$ (with algebraic multiplicity $3$) and $\lambda =5.$

Therefore, the correct answer is “$\lambda =-10$ is an eigenvalue of $P$”; “The eigenvalue $\lambda =-10$ has algebraic multiplicity $3$” only.

Answer $\lambda =-1$ is an eigenvalue of $P$: false

Answer $\lambda =-10$ is an eigenvalue of $P$: true

Answer The eigenvalue $\lambda =-10$ has algebraic multiplicity $3$: true

Question 17592186272092 — question.difficulty/moderate

$$
P=\begin{bmatrix}5 & 2 & -6 & 8 \\ 0 & 0 & 0 & 7 \\ 0 & -3 & -4 & 9 \\ 0 & 0 & 0 & 2\end{bmatrix}.
$$

Consider the matrix $P$ given above. Which of the following statements are true?

Select all that apply.

Solution: First, we find the matrix $\,P-\lambda I:$


$$
P-\lambda I=\begin{bmatrix}5-\lambda  & 2 & -6 & 8 \\ 0 & -\lambda  & 0 & 7 \\ 0 & -3 & -4-\lambda  & 9 \\ 0 & 0 & 0 & 2-\lambda \end{bmatrix}
$$

The characteristic equation is $\det(P-\lambda I)=0.$ 

Notice that we can expand the $4\times 4$ determinant across the $1$st column, as follows:

$$
\begin{aligned}\det(P-\lambda I) & =0 \\ \begin{vmatrix}5-\lambda  & 2 & -6 & 8 \\ 0 & -\lambda  & 0 & 7 \\ 0 & -3 & -4-\lambda  & 9 \\ 0 & 0 & 0 & 2-\lambda \end{vmatrix} & =0 \\ (5-\lambda )\begin{vmatrix}-\lambda  & 0 & 7 \\ -3 & -4-\lambda  & 9 \\ 0 & 0 & 2-\lambda \end{vmatrix} & =0\end{aligned}
$$

Now, expanding the $3\times 3$ determinant across the $3$rd row, we obtain the following:

$$
\begin{aligned}(5-\lambda )\cdot (2-\lambda )\begin{vmatrix}-\lambda  & 0 \\ -3 & -4-\lambda \end{vmatrix} & =0 \\ (5-\lambda )(2-\lambda )(-\lambda )(-4-\lambda ) & =0 \\ (\lambda -5)(\lambda -2)\lambda (\lambda +4) & =0\end{aligned}
$$

So, the eigenvalues of $P$ are $\lambda =5,$ $\lambda =2,$ $\lambda =0,$ and $\lambda =-4$  (all with algebraic multiplicity $1$).

Therefore, the correct answer is “$\lambda =0$ is an eigenvalue of $P$”; “$\lambda =-4$ is an eigenvalue of $P$” only.

Answer $\lambda =-4$ is an eigenvalue of $P$: true

Answer $\lambda =0$ is an eigenvalue of $P$: true

Answer The eigenvalue $\lambda =2$ has algebraic multiplicity $2$: false

### Finding the Eigenvalues of a General 3x3 Matrix (12 captured questions)

Question 17592186125013 — question.difficulty/moderate

Find the characteristic equation of the matrix 
$$
\displaystyle A=\begin{bmatrix}0 & -2 & -3 \\ -2 & 3 & 6 \\ 2 & -2 & -5\end{bmatrix}.
$$

Solution: First, we find the matrix $\,A-\lambda I:$


$$
A-\lambda I=\begin{bmatrix}-\lambda  & -2 & -3 \\ -2 & 3-\lambda  & 6 \\ 2 & -2 & -5-\lambda \end{bmatrix}
$$

The characteristic equation is $\det(A-\lambda I)=0.$ 

Expanding the determinant across the $1$st row, we get the following:

$$
\begin{aligned}\det(A-\lambda I) & =0 \\ \begin{vmatrix}-\lambda  & -2 & -3 \\ -2 & 3-\lambda  & 6 \\ 2 & -2 & -5-\lambda \end{vmatrix} & =0 \\ -\lambda \begin{vmatrix}3-\lambda  & 6 \\ -2 & -5-\lambda \end{vmatrix}-(-2)\begin{vmatrix}-2 & 6 \\ 2 & -5-\lambda \end{vmatrix}+(-3)\begin{vmatrix}-2 & 3-\lambda  \\ 2 & -2\end{vmatrix} & =0 \\ -\lambda ({\lambda }^{2}+2\lambda -3)+2(2\lambda -2)-3(2\lambda -2) & =0 \\ (-{\lambda }^{3}-2{\lambda }^{2}+3\lambda )+(4\lambda -4)-(6\lambda -6) & =0 \\ -{\lambda }^{3}-2{\lambda }^{2}+\lambda +2 & =0 \\ {\lambda }^{3}+2{\lambda }^{2}-\lambda -2 & =0\end{aligned}
$$

Answer selection: {\lambda }^{3}+2{\lambda }^{2}-\lambda -2=0

Question 17592186125016 — question.difficulty/hard

Determine all real eigenvalues $λ$ of the matrix
$$
\displaystyle A = \begin{bmatrix}4 & 2 & 1 \\ -2 & -1 & -2 \\ 2 & 2 & 3\end{bmatrix}.
$$

Solution: The eigenvalues satisfy the characteristic equation $\det(A-\lambda I)=0$. We have

$$
A-\lambda I=\begin{bmatrix}4 - \lambda & 2 & 1 \\ -2 & - \lambda - 1 & -2 \\ 2 & 2 & 3 - \lambda\end{bmatrix}.
$$

Expanding the determinant and factoring gives

$$
\det(A-\lambda I)=- \lambda^{3} + 6 \lambda^{2} - 11 \lambda + 6=- \left(\lambda - 3\right) \left(\lambda - 2\right) \left(\lambda - 1\right)=0.
$$

Therefore, the real eigenvalues are $1, 2, 3$.

Answer selection: λ ∈ {1, 2, 3}

Question 17592186272116 — question.difficulty/moderate

Find the characteristic equation of the matrix 
$$
\displaystyle C=\begin{bmatrix}3 & -1 & -1 \\ 1 & -3 & 3 \\ 1 & 2 & -2\end{bmatrix}.
$$

Solution: First, we find the matrix $\,C-\lambda I:$


$$
C-\lambda I=\begin{bmatrix}3-\lambda  & -1 & -1 \\ 1 & -3-\lambda  & 3 \\ 1 & 2 & -2-\lambda \end{bmatrix}
$$

The characteristic equation is $\det(C-\lambda I)=0.$ 

Expanding the determinant across the $1$st row, we get the following:

$$
\begin{aligned}\det(C-\lambda I) & =0 \\ \begin{vmatrix}3-\lambda  & -1 & -1 \\ 1 & -3-\lambda  & 3 \\ 1 & 2 & -2-\lambda \end{vmatrix} & =0 \\ (3-\lambda )\begin{vmatrix}-3-\lambda  & 3 \\ 2 & -2-\lambda \end{vmatrix}-(-1)\begin{vmatrix}1 & 3 \\ 1 & -2-\lambda \end{vmatrix}+(-1)\begin{vmatrix}1 & -3-\lambda  \\ 1 & 2\end{vmatrix} & =0 \\ (3-\lambda )({\lambda }^{2}+5\lambda )+(-\lambda -5)-(5+\lambda ) & =0 \\ (-{\lambda }^{3}-2{\lambda }^{2}+15\lambda )-\lambda -5-5-\lambda  & =0 \\ -{\lambda }^{3}-2{\lambda }^{2}+13\lambda -10 & =0 \\ {\lambda }^{3}+2{\lambda }^{2}-13\lambda +10 & =0\end{aligned}
$$

Answer selection: {\lambda }^{3}+2{\lambda }^{2}-13\lambda +10=0
