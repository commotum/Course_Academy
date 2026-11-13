# 17592186048462 Row and Column Operations on Determinants

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186121020 — Introduction

Remember the following three standard elementary row operations: 

  I. Swapping two rows

  II. Multiplying a row by a non-zero number

  III. Adding a multiple of one row to another row

Of these three elementary row operations, only III (adding a multiple of one row to another row) *preserves* the determinant. The other two operations, switching two rows or multiplying a row by a non-zero number, *change* the determinant.

To demonstrate, let's consider the matrix $A = {\left[ \begin{array}{cc}1 & 2 \\ 3 & 4\end{array} \right]}.$ Taking the determinant, we have
$$
\left| {\begin{array}{cc}1 & 2 \\ 3 & 4\end{array}} \right| = 1 \cdot 4 - 2 \cdot 3 = -2.
$$

If we swap the two rows, we get a different determinant:

$$
\begin{aligned}\begin{vmatrix}3 & 4 \\ 1 & 2\end{vmatrix} & =3\cdot 2-1\cdot 4 \\  & =2 \\  & \ne -2\hspace{1em}{\color{red}\times }\end{aligned}
$$

Likewise, if we multiply top row by ${\color{red}2},$ then we get a different determinant:

$$
\begin{aligned}\begin{vmatrix}{\color{red}2}\cdot 1 & {\color{red}2}\cdot 2 \\ 3 & 4\end{vmatrix} & =\begin{vmatrix}2 & 4 \\ 3 & 4\end{vmatrix} \\  & =2\cdot 4-3\cdot 4 \\  & =-4 \\  & \ne -2\hspace{1em}{\color{red}\times }\end{aligned}
$$

However, if we add twice the top row to the bottom row, then we get the same determinant:

$$
\begin{aligned}\begin{vmatrix}1 & 2 \\ 3+{\color{red}2}\cdot 1 & 4+{\color{red}2}\cdot 2\end{vmatrix} & =\begin{vmatrix}1 & 2 \\ 5 & 8\end{vmatrix} \\  & =1\cdot 8-2\cdot 5 \\  & =-2\hspace{1em}{\color{green}✓}\end{aligned}
$$



### tutorial 17592186121044 — Switching Two Rows Changes the Sign of the Determinant

As we saw, swapping two rows does not preserve the determinant. However, the only difference is the sign of the determinant changes. 

$$
\begin{aligned}\begin{vmatrix}{\color{red}1} & {\color{red}2} \\ {\color{blue}3} & {\color{blue}4}\end{vmatrix} & =1\cdot 4-2\cdot 3=-2 \\ \begin{vmatrix}{\color{blue}3} & {\color{blue}4} \\ {\color{red}1} & {\color{red}2}\end{vmatrix} & =3\cdot 2-1\cdot 4=2\end{aligned}
$$

So, in the above example, we have

$$
\begin{aligned}\begin{vmatrix}{\color{red}1} & {\color{red}2} \\ {\color{blue}3} & {\color{blue}4}\end{vmatrix} & =-\begin{vmatrix}{\color{blue}3} & {\color{blue}4} \\ {\color{red}1} & {\color{red}2}\end{vmatrix}.\end{aligned}
$$

In general, swapping any two rows of a matrix changes the sign of the determinant to the opposite one. That is to say, 

$$
\begin{aligned}\det \begin{bmatrix}⋮ & ⋮ & … & ⋮ \\ {\color{red}◻} & {\color{red}◻} & … & {\color{red}◻} \\ ⋮ & ⋮ & … & ⋮ \\ {\color{blue}△} & {\color{blue}△} & … & {\color{blue}△} \\ ⋮ & ⋮ & … & ⋮\end{bmatrix}=-\det \begin{bmatrix}⋮ & ⋮ & … & ⋮ \\ {\color{blue}△} & {\color{blue}△} & … & {\color{blue}△} \\ ⋮ & ⋮ & … & ⋮ \\ {\color{red}◻} & {\color{red}◻} & … & {\color{red}◻} \\ ⋮ & ⋮ & … & ⋮\end{bmatrix}.\end{aligned}
$$



### example 17592186119589 — Calculating a Determinant After Switching Two Rows

Suppose $A$ is a $3 \times 3$ matrix and $\det (A) = -16.$ The matrix $B$ is obtained from $A$ by applying the elementary row operation $R_1 \leftrightarrow R_2$ (switching the first and the second rows). What is the value of $\det(B)?$

Since swapping any two rows changes the sign of the determinant to the opposite sign, we have

$$
\begin{aligned}\det (B) & =-\det (A) \\  & =-(-16) \\  & =16.\end{aligned}
$$

### tutorial 17592186121045 — Multiplying a Row By a Number Scales the Determinant By That Number

As we have seen, multiplying a row by a number does not preserve the determinant. However, it does affect the determinant in a predictable way: multiplying a row by a number scales the determinant by that number as well.

$$
\begin{aligned}\begin{vmatrix}1 & 2 \\ 3 & 4\end{vmatrix} & =1\cdot 4-2\cdot 3=-2 \\ \begin{vmatrix}{\color{red}2}\cdot 1 & {\color{red}2}\cdot 2 \\ 3 & 4\end{vmatrix}=\begin{vmatrix}2 & 4 \\ 3 & 4\end{vmatrix} & =2\cdot 4-3\cdot 4=-4\end{aligned}
$$

So, in the above example, we have
$$
\left| {\begin{array}{cc}{\color{red}2} \cdot  1 & {\color{red}2} \cdot  2 \\ 3 & 4\end{array}} \right| = {\color{red}2} \cdot \left| {\begin{array}{cc}1 & 2 \\ 3 & 4\end{array}} \right|.
$$

In general, multiplying a row of a matrix by a number multiplies the determinant by that number. That is to say, we can factor out the common multiplier from the row of the determinant:

$$
\begin{aligned}\det \begin{bmatrix}⋮ & ⋮ & … & ⋮ \\ {\color{red}k}△ & {\color{red}k}△ & … & {\color{red}k}△ \\ ⋮ & ⋮ & … & ⋮\end{bmatrix}={\color{red}k}\cdot \det \begin{bmatrix}⋮ & ⋮ & … & ⋮ \\ △ & △ & … & △ \\ ⋮ & ⋮ & … & ⋮\end{bmatrix}\end{aligned}
$$



### example 17592186119590 — Calculating a Determinant After Multiplying a Row by a Number

Suppose $A$ is a $6 \times 6$ matrix and $\det(A) = 32.$ The matrix $B$ is obtained from $A$ by applying the elementary row operation $R_3:= \dfrac{1}{8} R_3$. What is the value of $\det(B)?$

The row operation applied to $A$ consists of multiplying a row by the number $\dfrac{1}{8}.$

When we do this, the determinant is multiplied by the same number. So, we have

$$
\begin{aligned}\det (B) & =\frac{1}{8}\det (A) \\  & =\frac{1}{8}\cdot 32 \\  & =4.\end{aligned}
$$

### tutorial 17592186121061 — Multiplying a Matrix By a Scalar

Let's check what happens if we multiply the entire matrix (not only one row) by a number. For example,

$$
\begin{aligned}\begin{vmatrix}1 & 2 \\ 3 & 4\end{vmatrix} & =1\cdot 4-2\cdot 3=-2 \\ \begin{vmatrix}{\color{red}3}\cdot 1 & {\color{red}3}\cdot 2 \\ {\color{red}3}\cdot 3 & {\color{red}3}\cdot 4\end{vmatrix}=\begin{vmatrix}3 & 6 \\ 9 & 12\end{vmatrix} & =3\cdot 12-6\cdot 9=-18\end{aligned}
$$

So, in the above example, we have

$$
\left| {\begin{array}{cc}{\color{red}3} \cdot  1 & {\color{red}3} \cdot  2 \\ {\color{red}3} \cdot  3 & {\color{red}3} \cdot  4\end{array}} \right| = {\color{red}3}^2 \cdot \left| {\begin{array}{cc}1 & 2 \\ 3 & 4\end{array}} \right|.
$$

The above is equivalent to multiplying both rows of the matrix by $3$. Multiplying the first row scales the determinant by $3$, and then multiplying the second row scales it by $3$ once more.

In general, multiplying an entire $n \times n$ matrix by a number multiplies the determinant by that number to the power of $n$. That is to say, we can factor out the common multiplier from the entire matrix, as follows:

$$
\begin{aligned}\det (k\cdot A) &={k}^{n}\cdot \det (A),\end{aligned}
$$

where $A$ is an $n \times n$ matrix.



### example 17592186119666 — Calculating a Determinant After Multiplying a Matrix by a Scalar

Suppose $A$ is a $4\times4$ matrix and $\det(A)=5.$ What is the value of $\det(2A)?$

Multiplying a $n\times n$ matrix by a scalar $k$ is equivalent to multiplying each row by $k,$ and this occurs $n$ times. This leads to the result

$$
\begin{aligned}\det (k\cdot A)={k}^{n}\cdot \det (A).\end{aligned}
$$

In our case, we have $k=2$ and $n=4.$ Therefore,

$$
\begin{aligned}\det (2A) & ={2}^{4}\cdot \det (A) \\  & =16\cdot 5 \\  & =80.\end{aligned}
$$

### example 17592186119591 — Calculating a Determinant After Applying Several Elementary Operations

Suppose $A$ is an $8 \times 8$ matrix and $\det(A) = 5.$ The matrix $B$ is obtained from $A$ by applying the elementary row operations $R_4 \leftrightarrow R_5,$ $R_6:= 4 R_6,$ and $R_8: = R_8 - \dfrac{1}{2} R_7.$ What is the value of $\det(B)?$

First, let's figure out what each operation does to the determinant.

- The operation $R_4 \leftrightarrow R_5$ involves swapping two rows, so it changes the sign of the determinant to the opposite one.

- The operation $R_6:= 4 R_6$ involves multiplying a row by $4,$ so the determinant is multiplied by $4$ as well.

- The operation $R_8:= R_8 - \dfrac{1}{2} R_7$ involves adding a multiple of one row to another row,  so it does not change the determinant.

Therefore, we have to change the sign of the determinant to the opposite one and multiply by $4$ as well. Consequently, we get

$$
\begin{aligned}\det (B) & =4\cdot (-\det (A)) \\  & =-4\det (A) \\  & =-4\cdot 5 \\  & =-20.\end{aligned}
$$

### example 17592186119665 — Identifying a Row Operation Given the Connection Between Two Determinants

Given that $\det(X)=\det(Y),$ which elementary row operations transforms matrix $X$ to matrix $Y,$ where

$$
X=
{\left[ \begin{array}{ccc}2 & - 1 & 2 \\ 3 & 0 & - 1 \\ - 1 & 1 & 1\end{array} \right]},
\quad
Y=
{\left[ \begin{array}{ccc}2 & - 1 & 2 \\ 0 & 3 & 2 \\ - 1 & 1 & 1\end{array} \right]}?
$$

Since $\det(X)=\det(Y)$, the row operation applied to $X$ must be to add or subtract a multiple of one row to another row. In other words, it is of the form 

$$
R_j := R_j + (k)R_i, \quad i \neq j.
$$

By considering the given row operations that are of the above form, we notice that

$$
\begin{aligned}\det (X) & =\begin{vmatrix}2 & -1 & 2 \\ 3 & 0 & -1 \\ -1 & 1 & 1\end{vmatrix} & {R}_{2} & :={R}_{2}+3{R}_{3} \\  & =\begin{vmatrix}2 & -1 & 2 \\ 0 & 3 & 2 \\ -1 & 1 & 1\end{vmatrix} \\  & =\det (Y).\end{aligned}
$$

Therefore, the required row operation is

$$
R_2:= R_2 + 3R_3.
$$

### tutorial 17592186121021 — Column Operations on Determinants

Since $\det(A^T)=\det(A),$ the corresponding elementary column operations on determinants have the same properties as the elementary row ones.

- Swapping two columns changes the sign of the determinant.

- Multiplying a column by a number scales the determinant by that number.

- Adding a multiple of one column to another column does not change the determinant.



## Representative practice (first three per skill; full bank in practice.json)

### Calculating a Determinant After Switching Two Rows (12 captured questions)

Question 17592186120452 — question.difficulty/easy

Suppose $A$ is a $5\times 5$ matrix and $\det (A)=-28.$ The matrix $B$ is obtained from $A$ by applying the elementary row operation ${R}_{5}↔{R}_{3}$ (switching the third and the fifth rows). What is the value of $\det (B)?$

Solution: Since swapping any two rows changes the sign of the determinant to the opposite sign, we have

$$
\begin{aligned}\det (B) & =-\det (A) \\  & =-(-28) \\  & =28.\end{aligned}
$$

Answer selection: 28

Question 17592186120454 — question.difficulty/easy

Suppose $X$ is a $4\times 4$ matrix and $\det (X)=105.$ The matrix $Y$ is obtained from $X$ by applying the elementary row operation ${R}_{3}↔{R}_{1}$ (switching the first and the third rows). What is the value of $\det (Y)?$

Solution: Since swapping any two rows changes the sign of the determinant to the opposite sign, we have

$$
\begin{aligned}\det (Y) & =-\det (X) \\  & =-(105) \\  & =-105.\end{aligned}
$$

Answer selection: -105

Question 17592186265957 — question.difficulty/easy

Suppose $A$ is a $5\times 5$ matrix and $\det (A)=-15.$ The matrix $B$ is obtained from $A$ by applying the elementary row operation ${R}_{1}↔{R}_{5}$ (switching the first and the fifth rows). What is the value of $\det (B)?$

Solution: Since swapping any two rows changes the sign of the determinant to the opposite sign, we have

$$
\begin{aligned}\det (B) & =-\det (A) \\  & =-(-15) \\  & =15.\end{aligned}
$$

Answer selection: 15

### Calculating a Determinant After Multiplying a Row by a Number (15 captured questions)

Question 17592186120453 — question.difficulty/easy

Suppose $A$ is a $6\times 6$ matrix and $\det (A)=35.$ The matrix $B$ is obtained from $A$ by applying the elementary row operation ${R}_{1}:=-\frac{3}{5}{R}_{1}.$ What is the value of $\det (B)?$

Solution: The row operation applied to $A$ consists of multiplying a row by the number $-\frac{3}{5}.$

When we do this, the determinant is multiplied by the same number. So, we have

$$
\begin{aligned}\det (B) & =-\frac{3}{5}\det (A) \\  & =-\frac{3}{5}\cdot 35 \\  & =-21.\end{aligned}
$$

Answer selection: -21

Question 17592186120455 — question.difficulty/easy

Suppose $C$ is a $7\times 7$ matrix and $\det (C)=-126.$ The matrix $D$ is obtained from $C$ by applying the elementary row operation ${R}_{5}:=\frac{8}{21}{R}_{5}.$ What is the value of $\det (D)?$

Solution: The row operation applied to $C$ consists of multiplying a row by the number $\frac{8}{21}.$

When we do this, the determinant is multiplied by the same number. So, we have

$$
\begin{aligned}\det (D) & =\frac{8}{21}\det (C) \\  & =\frac{8}{21}\cdot (-126) \\  & =-48.\end{aligned}
$$

Answer selection: -48

Question 17592186265963 — question.difficulty/easy

Suppose $A$ is a $4\times 4$ matrix and $\det (A)=-63.$ The matrix $B$ is obtained from $A$ by applying the elementary row operation ${R}_{3}:=\frac{2}{9}{R}_{3}.$ What is the value of $\det (B)?$

Solution: The row operation applied to $A$ consists of multiplying a row by the number $\frac{2}{9}.$

When we do this, the determinant is multiplied by the same number. So, we have

$$
\begin{aligned}\det (B) & =\frac{2}{9}\det (A) \\  & =\frac{2}{9}\cdot (-63) \\  & =-14.\end{aligned}
$$

Answer selection: -14

### Calculating a Determinant After Multiplying a Matrix by a Scalar (17 captured questions)

Question 17592186120512 — question.difficulty/easy

Suppose $A$ is a $3\times3$ matrix and $\det (A) = 4$. What is the value of $\det (5A)$?

Solution: Multiplying an $n\times n$ matrix by a scalar $k$ multiplies each of its $n$ rows by $k$. Consequently,

$$
\det(kA)=k^n\det(A).
$$

Here $k=5$, $n=3$, and $\det(A)=4$, so

$$
\det(5A)=5^3\cdot4=125\cdot4=500.
$$

Answer selection: 500

Question 17592186120513 — question.difficulty/easy

Suppose $B$ is a $2\times 2$ matrix and $\det (B)=-2.$ What is the value of $\det (3B)?$

Solution: Multiplying a $n\times n$ matrix by a scalar $k$ is equivalent to multiplying each row by $k,$ and this occurs $n$ times. This leads to the result

$$
\begin{aligned}\det (k\cdot B)={k}^{n}\cdot \det (B).\end{aligned}
$$

In our case, we have $k=3$ and $n=2.$ Therefore,

$$
\begin{aligned}\det (3B) & ={3}^{2}\cdot \det (B) \\  & =9\cdot (-2) \\  & =-18.\end{aligned}
$$

Answer selection: -18

Question 17592186265965 — question.difficulty/easy

Suppose $B$ is a $5\times 5$ matrix and $\det (B)=-3.$ What is the value of $\det (-2B)?$

Solution: Multiplying a $n\times n$ matrix by a scalar $k$ is equivalent to multiplying each row by $k,$ and this occurs $n$ times. This leads to the result

$$
\begin{aligned}\det (k\cdot B)={k}^{n}\cdot \det (B).\end{aligned}
$$

In our case, we have $k=-2$ and $n=5.$ Therefore,

$$
\begin{aligned}\det (-2B) & =(-2)^{5}\cdot \det (B) \\  & =-32\cdot (-3) \\  & =96.\end{aligned}
$$

Answer selection: 96

### Calculating a Determinant After Applying Several Elementary Operations (17 captured questions)

Question 17592186120431 — question.difficulty/moderate

Suppose $A$ is a $4\times 4$ matrix and $\det (A)=12.$ The matrix $B$ is obtained from $A$ by applying the elementary row operations ${R}_{2}↔{R}_{3}$ and ${R}_{1}:={R}_{1}+2{R}_{3}.$ What is the value of $\det (B)?$

Solution: First, let's figure out what each operation does to the determinant.

- The operation ${R}_{2}↔{R}_{3}$ involves swapping two rows, so it changes the sign of the determinant to the opposite one.

- The operation ${R}_{1}:={R}_{1}+2{R}_{3}$ involves adding a multiple of one row to another row,  so it does not change the determinant.

Therefore, we only have to change the sign of the determinant to the opposite one. Consequently, we get

$$
\begin{aligned}\det (B) & =-\det (A) \\  & =-(12) \\  & =-12.\end{aligned}
$$

Answer selection: -12

Question 17592186120432 — question.difficulty/moderate

Suppose $U$ is a $4\times 4$ matrix and $\det (U)=10.$ The matrix $V$ is obtained from $U$ by applying the elementary row operations ${R}_{2}:={R}_{2}+6{R}_{4}$ and ${R}_{3}:=\frac{1}{2}{R}_{3}.$ What is the value of $\det (V)?$

Solution: First, let's figure out what each operation does to the determinant.

- The operation ${R}_{2}:={R}_{2}+6{R}_{4}$ involves adding a multiple of one row to another row,  so it does not change the determinant.

- The operation ${R}_{3}:=\frac{1}{2}{R}_{3}$ involves multiplying a row by $\frac{1}{2},$ so the determinant is multiplied by $\frac{1}{2}$ as well.

Therefore, we only have to multiply the determinant by $\frac{1}{2}.$ Consequently, we get

$$
\begin{aligned}\det (V) & =\frac{1}{2}\det (U) \\  & =\frac{1}{2}\cdot 10 \\  & =5.\end{aligned}
$$

Answer selection: 5

Question 17592186265971 — question.difficulty/moderate

Suppose $X$ is a $6\times 6$ matrix and $\det (X)=28.$ The matrix $Y$ is obtained from $X$ by applying the elementary row operations ${R}_{1}:=\frac{3}{4}{R}_{1}$ and ${R}_{6}:={R}_{6}+(-7){R}_{2}.$ What is the value of $\det (Y)?$

Solution: First, let's figure out what each operation does to the determinant.

- The operation ${R}_{6}:={R}_{6}+(-7){R}_{2}$ involves adding a multiple of one row to another row,  so it does not change the determinant.

- The operation ${R}_{1}:=\frac{3}{4}{R}_{1}$ involves multiplying a row by $\frac{3}{4},$ so the determinant is multiplied by $\frac{3}{4}$ as well.

Therefore, we only have to multiply the determinant by $\frac{3}{4}.$ Consequently, we get

$$
\begin{aligned}\det (Y) & =\frac{3}{4}\det (X) \\  & =\frac{3}{4}\cdot 28 \\  & =21.\end{aligned}
$$

Answer selection: 21

### Identifying a Row Operation Given the Connection Between Two Determinants (16 captured questions)

Question 17592186120420 — question.difficulty/moderate

Given that $\det (A)=\det (B),$ which of the following elementary row operations transforms matrix $A$ to matrix $B,$ where

$$
A=\begin{bmatrix}1 & 2 & 4 \\ 2 & 4 & -1 \\ 3 & 2 & 1\end{bmatrix},\,B=\begin{bmatrix}1 & 2 & 4 \\ 0 & 0 & -9 \\ 3 & 2 & 1\end{bmatrix}?
$$

Solution: Since $\det (A)=\det (B)$, the row operation applied to $A$ must be to add or subtract a multiple of one row to another row. In other words, it is of the form 

$$
{R}_{j}:={R}_{j}+(k){R}_{i},\,i\ne j.
$$

By considering the given row operations that are of the above form, we notice that

$$
\begin{aligned}\det (A) & =\begin{vmatrix}1 & 2 & 4 \\ 2 & 4 & -1 \\ 3 & 2 & 1\end{vmatrix} & {R}_{2} & :={R}_{2}+(-2){R}_{1} \\  & =\begin{vmatrix}1 & 2 & 4 \\ 0 & 0 & -9 \\ 3 & 2 & 1\end{vmatrix} \\  & =\det (B).\end{aligned}
$$

Therefore, the required row operation is

$$
{R}_{2}:={R}_{2}+(-2){R}_{1}.
$$

Answer selection: {R}_{2}:={R}_{2}+(-2){R}_{1}

Question 17592186120456 — question.difficulty/easy

Consider the matrices given below. Given that $X$ and $Y$ are row equivalent matrices and $\det (X)=-8$, find $\det (Y).$

$$
X=\begin{bmatrix}1 & -1 & 0 \\ 0 & 1 & 0 \\ -6 & 3 & 5\end{bmatrix},\,Y=\begin{bmatrix}1 & -1 & 0 \\ -6 & 3 & 5 \\ 0 & 1 & 0\end{bmatrix}.
$$

Solution: Notice that $Y$ can be obtained from $X$ by swapping the $2$nd and the $3$rd rows. 

This changes the sign of the determinant to the opposite one.
Therefore, we obtain

$$
\begin{aligned}\det (Y) & =-\det (X) \\  & =-(-8) \\  & =8.\end{aligned}
$$

Answer selection: 8

Question 17592186265985 — question.difficulty/moderate

Given that $\det (A)=\det (B),$ which of the following elementary row operations transforms matrix $A$ to matrix $B,$ where

$$
A=\begin{bmatrix}1 & 5 & 3 \\ 2 & 4 & -2 \\ 2 & 8 & -2\end{bmatrix},\,B=\begin{bmatrix}1 & 5 & 3 \\ 2 & 4 & -2 \\ 0 & -2 & -8\end{bmatrix}?
$$

Solution: Since $\det (A)=\det (B)$, the row operation applied to $A$ must be to add or subtract a multiple of one row to another row. In other words, it is of the form 

$$
{R}_{j}:={R}_{j}+(k){R}_{i},\,i\ne j.
$$

By considering the given row operations that are of the above form, we notice that

$$
\begin{aligned}\det (A) & =\begin{vmatrix}1 & 5 & 3 \\ 2 & 4 & -2 \\ 2 & 8 & -2\end{vmatrix} & {R}_{3} & :={R}_{3}+(-2){R}_{1} \\  & =\begin{vmatrix}1 & 5 & 3 \\ 2 & 4 & -2 \\ 0 & -2 & -8\end{vmatrix} \\  & =\det (B).\end{aligned}
$$

Therefore, the required row operation is

$$
{R}_{3}:={R}_{3}+(-2){R}_{1}.
$$

Answer selection: {R}_{3}:={R}_{3}+(-2){R}_{1}
