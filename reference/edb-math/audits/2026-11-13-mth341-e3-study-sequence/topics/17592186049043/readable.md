# 17592186049043 Calculating the Inverse of a 3x3 Matrix Using the Cofactor Method

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186060933 — Introduction

We can calculate the inverse of a $3\times 3$ matrix $A$ using the following five-step algorithm.

**Step 1:** Find the determinant $\det(A)$ of the matrix.

**Step 2:** Form the **matrix $M$ of the minors** of $A,$ where each entry $a_{ij}$ of $A$ is replaced by its minor $M_{ij}\mathbin{:}$
   $$
M = {\left[ \begin{array}{ccc}{M}_{11} & {M}_{12} & {M}_{13} \\ {M}_{21} & {M}_{22} & {M}_{23} \\ {M}_{31} & {M}_{32} & {M}_{33}\end{array} \right]}
$$

**Step 3:** Create the **matrix $C$ of cofactors** by changing the sign of some entries of the matrix of the minors according to the **rule of alternating signs**:
   

$$
\begin{bmatrix}+ & - & + \\ - & + & - \\ + & - & +\end{bmatrix}
$$

For each entry of $M$, we change the sign if the corresponding sign in the pattern is "$-$". Otherwise, if the corresponding sign in the pattern is "$+$", then we don't change the entry.

So, the matrix of cofactors is given by

$$
C = {\left[ \begin{array}{ccc}{M}_{11} & - {M}_{12} & {M}_{13} \\ - {M}_{21} & {M}_{22} & - {M}_{23} \\ {M}_{31} & - {M}_{32} & {M}_{33}\end{array} \right]}.
$$

**Step 4:** Write down the transpose of the matrix of cofactors, $C^T.$

$$
C^T = {\left[ \begin{array}{ccc}{M}_{11} & - {M}_{21} & {M}_{31} \\ - {M}_{12} & {M}_{22} & - {M}_{32} \\ {M}_{13} & - {M}_{23} & {M}_{33}\end{array} \right]}.
$$

**Step 5:** Use the formula for the inverse of a $3\times 3$ matrix:
   

$$
A^{-1} = \dfrac{1}{\det ( A)}C^{T}
$$

In other words, we divide each entry of the transpose of the matrix of cofactors by the determinant of the original matrix (which we computed in step 1).

Let's see this in practice, in the next example.



### example 17592186059563 — Calculating the Inverse of a 3x3 Matrix Using the Matrix of Cofactors

Find the inverse of $A={\left[ \begin{array}{ccc}0 & 1 & 2 \\ 1 & 0 & 3 \\ 4 & - 3 & 8\end{array} \right]}.$

Let's follow the standard five-step procedure.

**Step 1:** Find the determinant of $A.$

$$
\begin{aligned}\det (A)=\begin{vmatrix}0 & 1 & 2 \\ 1 & 0 & 3 \\ 4 & -3 & 8\end{vmatrix} & =0\begin{vmatrix}0 & 3 \\ -3 & 8\end{vmatrix}-1\begin{vmatrix}1 & 3 \\ 4 & 8\end{vmatrix}+2\begin{vmatrix}1 & 0 \\ 4 & -3\end{vmatrix} \\  & =0-(8-12)+2(-3-0) \\  & =-2\end{aligned}
$$

**Step 2:** Form the matrix of the minors of $A.$
To make this matrix, we replace each entry of $A$ by its minor.

$$
\begin{aligned}M & =\begin{bmatrix}\begin{vmatrix}0 & 3 \\ -3 & 8\end{vmatrix} & \begin{vmatrix}1 & 3 \\ 4 & 8\end{vmatrix} & \begin{vmatrix}1 & 0 \\ 4 & -3\end{vmatrix} \\ \begin{vmatrix}1 & 2 \\ -3 & 8\end{vmatrix} & \begin{vmatrix}0 & 2 \\ 4 & 8\end{vmatrix} & \begin{vmatrix}0 & 1 \\ 4 & -3\end{vmatrix} \\ \begin{vmatrix}1 & 2 \\ 0 & 3\end{vmatrix} & \begin{vmatrix}0 & 2 \\ 1 & 3\end{vmatrix} & \begin{vmatrix}0 & 1 \\ 1 & 0\end{vmatrix}\end{bmatrix} \\  & =\begin{bmatrix}9 & -4 & -3 \\ 14 & -8 & -4 \\ 3 & -2 & -1\end{bmatrix}\end{aligned}
$$

**Step 3:** Create the matrix of cofactors by changing the sign of some of the entries of $M$ according to the rule of alternating signs.

$$
C={\left[ \begin{array}{ccc}9 & - ( - 4 ) & - 3 \\ - ( 14 ) & - 8 & - ( - 4 ) \\ 3 & - ( - 2 ) & - 1\end{array} \right]}
={\left[ \begin{array}{ccc}9 & 4 & - 3 \\ - 14 & - 8 & 4 \\ 3 & 2 & - 1\end{array} \right]}
$$

**Step 4:** Write down the transpose of the matrix of cofactors.

$$
C^{T}={\left[ \begin{array}{ccc}9 & - 14 & 3 \\ 4 & - 8 & 2 \\ - 3 & 4 & - 1\end{array} \right]}
$$

**Step 5:** Use the formula for the inverse of a $3\times 3$ matrix.

$$
\begin{aligned}{A}^{-1} & =\frac{1}{\det (A)}{C}^{T} \\  & =\frac{1}{-2}\begin{bmatrix}9 & -14 & 3 \\ 4 & -8 & 2 \\ -3 & 4 & -1\end{bmatrix} \\  & =-\frac{1}{2}\begin{bmatrix}9 & -14 & 3 \\ 4 & -8 & 2 \\ -3 & 4 & -1\end{bmatrix} \\  & =\begin{bmatrix}-\frac{9}{2} & 7 & -\frac{3}{2} \\ -2 & 4 & -1 \\ \frac{3}{2} & -2 & \frac{1}{2}\end{bmatrix}\end{aligned}
$$

### tutorial 17592186060934 — Calculating Individual Entries of the Matrix of Cofactors

We make the matrix $C$ of cofactors by changing the sign of alternate entries of the matrix $M$ of the minors. So, each entry $c_{ij}$ of $C$ equals

$$
c_{ij} = (-1)^{i+j} M_{ij},
$$

where $M_{ij}$ is the minor of the entry $a_{ij}$ in the matrix $A.$

With this and the formula for the inverse, we can write the formula for each entry $a'_{ij}$ of the inverse matrix $A^{-1}$ as follows:

$$
a'_{ij} = \dfrac{1}{\det(A)}c^t_{ij}
        = \dfrac{1}{\det(A)} c_{ji}
$$

Here, we used the fact that the entry $c^t_{ij}$ of $C^T$ is equal to the entry $c_{ji}$ of $C$ by the definition of the transpose.



### example 17592186059565 — Calculating an Element of the Inverse of a 3x3 Matrix

Determine the entry $a'_{23}$ in the inverse of the matrix $A={\left[ \begin{array}{ccc}- 2 & 3 & - 3 \\ 0 & 1 & 0 \\ 1 & - 1 & 2\end{array} \right]}.$

First, we need to find the determinant of $A\mathbin{:}$

$$
\begin{aligned}\det (A)=\begin{vmatrix}-2 & 3 & -3 \\ 0 & 1 & 0 \\ 1 & -1 & 2\end{vmatrix} & =-2\begin{vmatrix}1 & 0 \\ -1 & 2\end{vmatrix}-3\begin{vmatrix}0 & 0 \\ 1 & 2\end{vmatrix}+(-3)\begin{vmatrix}0 & 1 \\ 1 & -1\end{vmatrix} \\  & =-2(2-0)-3(0-0)-3(0-1) \\  & =-1\end{aligned}
$$

Since we want the entry $a'_{23}$ in $A^{-1},$ we need to know the value of $c_{32}$ in the matrix of cofactors. For this, we use the formula to get

$$
\begin{aligned}{c}_{32} & =(-1)^{3+2}{M}_{32} \\  & =(-1)^{5}\begin{vmatrix}-2 & -3 \\ 0 & 0\end{vmatrix} \\  & =-1\cdot (0) \\  & =0.\end{aligned}
$$

Then, since $A^{-1}=\dfrac{1}{\det (A)}C^{T},$ we have

$$
a'_{23} = \dfrac{1}{-1}c_{32} = -1\cdot 0 = 0.
$$

### example 17592186059564 — Calculating the Cofactor Method To Solve for an Unknown Quantity

The entry $a'_{31}$ in the inverse of the matrix
$$
A={\left[ \begin{array}{ccc}3 & 2 & - 2 \\ - 2 & k & 0 \\ - 1 & - 3 & 3\end{array} \right]}
$$ 
equals $1$. Find the value of $k$.

First, we need to find the determinant of $A\mathbin{:}$

$$
\begin{aligned}\det (A)=\begin{vmatrix}3 & 2 & -2 \\ -2 & k & 0 \\ -1 & -3 & 3\end{vmatrix} & =3\begin{vmatrix}k & 0 \\ -3 & 3\end{vmatrix}-2\begin{vmatrix}-2 & 0 \\ -1 & 3\end{vmatrix}+(-2)\begin{vmatrix}-2 & k \\ -1 & -3\end{vmatrix} \\  & =3(3k-0)-2(-6-0)-2(6+k) \\  & =9k+12-12-2k \\  & =7k.\end{aligned}
$$

Since we want the entry $a'_{31}$ in $A^{-1},$ we need to know the value of $c_{13}$ in the matrix of cofactors. For this, we use the formula to get

$$
\begin{aligned}{c}_{13} & =(-1)^{1+3}\begin{vmatrix}-2 & k \\ -1 & -3\end{vmatrix} \\  & =\begin{vmatrix}-2 & k \\ -1 & -3\end{vmatrix} \\  & =6+k.\end{aligned}
$$

Then, since $A^{-1}=\dfrac{1}{\det (A)}C^{T},$ we have

$$
\begin{aligned}{a}_{31}^{′} & =\frac{1}{\text{det}(A)}{c}_{13} \\  & =\frac{1}{7k}\cdot (6+k) \\  & =\frac{6+k}{7k}.\end{aligned}
$$

Finally, since we are told that $a'_{31}=1$, we have

$$
\begin{aligned}\frac{6+k}{7k} & =1 \\ 6+k & =7k \\ 6 & =6k \\ k & =1.\end{aligned}
$$

## Representative practice (first three per skill; full bank in practice.json)

### Calculating the Inverse of a 3x3 Matrix Using the Matrix of Cofactors (14 captured questions)

Question 17592186060448 — None

Find the inverse of the matrix $A = \begin{bmatrix}7 & 2 & 1 \\ 0 & 3 & -1 \\ -3 & 4 & -2\end{bmatrix}$.

Solution: Let's follow the standard five-step procedure.

**Step 1:** Find the determinant of $A$.

$$
\det(A)=(7)(-2)+(2)(3)+(1)(9)=1.
$$

**Step 2:** Form the matrix of minors. Delete row $i$ and column $j$ to obtain $M_{ij}$. For example,

$$
M_{11}=\begin{vmatrix}3 & -1 \\ 4 & -2\end{vmatrix}=-2.
$$

Computing the remaining minors gives

$$
M=\begin{bmatrix}-2 & -3 & 9 \\ -8 & -11 & 34 \\ -5 & -7 & 21\end{bmatrix}.
$$

**Step 3:** Apply the alternating signs $(-1)^{i+j}$ to form the cofactor matrix.

$$
C=\begin{bmatrix}-2 & 3 & 9 \\ 8 & -11 & -34 \\ -5 & 7 & 21\end{bmatrix}.
$$

**Step 4:** Transpose the matrix of cofactors.

$$
C^T=\begin{bmatrix}-2 & 8 & -5 \\ 3 & -11 & 7 \\ 9 & -34 & 21\end{bmatrix}.
$$

**Step 5:** Divide by the nonzero determinant.

$$
A^{-1}=\frac{1}{\det(A)}C^T=1\begin{bmatrix}-2 & 8 & -5 \\ 3 & -11 & 7 \\ 9 & -34 & 21\end{bmatrix}=\begin{bmatrix}-2 & 8 & -5 \\ 3 & -11 & 7 \\ 9 & -34 & 21\end{bmatrix}.
$$

Answer selection: \begin{bmatrix}-2 & 8 & -5 \\ 3 & -11 & 7 \\ 9 & -34 & 21\end{bmatrix}

Question 17592186060458 — question.difficulty/easy

Find the inverse of the matrix $A = \begin{bmatrix}1 & -1 & 3 \\ 2 & 1 & 2 \\ -2 & -2 & 1\end{bmatrix}$
given that $\det (A) = 5$.

Solution: Let's follow the standard five-step procedure.

**Step 1:** Find the determinant of $A$.

$$
\det(A)=(1)(5)+(-1)(-6)+(3)(-2)=5.
$$

**Step 2:** Form the matrix of minors. Delete row $i$ and column $j$ to obtain $M_{ij}$. For example,

$$
M_{11}=\begin{vmatrix}1 & 2 \\ -2 & 1\end{vmatrix}=5.
$$

Computing the remaining minors gives

$$
M=\begin{bmatrix}5 & 6 & -2 \\ 5 & 7 & -4 \\ -5 & -4 & 3\end{bmatrix}.
$$

**Step 3:** Apply the alternating signs $(-1)^{i+j}$ to form the cofactor matrix.

$$
C=\begin{bmatrix}5 & -6 & -2 \\ -5 & 7 & 4 \\ -5 & 4 & 3\end{bmatrix}.
$$

**Step 4:** Transpose the matrix of cofactors.

$$
C^T=\begin{bmatrix}5 & -5 & -5 \\ -6 & 7 & 4 \\ -2 & 4 & 3\end{bmatrix}.
$$

**Step 5:** Divide by the nonzero determinant.

$$
A^{-1}=\frac{1}{\det(A)}C^T=\frac{1}{5}\begin{bmatrix}5 & -5 & -5 \\ -6 & 7 & 4 \\ -2 & 4 & 3\end{bmatrix}=\begin{bmatrix}1 & -1 & -1 \\ - \frac{6}{5} & \frac{7}{5} & \frac{4}{5} \\ - \frac{2}{5} & \frac{4}{5} & \frac{3}{5}\end{bmatrix}.
$$

Answer selection: \frac{1}{5}\begin{bmatrix}5 & -5 & -5 \\ -6 & 7 & 4 \\ -2 & 4 & 3\end{bmatrix}

Question 17592186240804 — question.difficulty/easy

Find the inverse of the matrix $A=\begin{bmatrix}-1 & 0 & 0 \\ 2 & 3 & 1 \\ 0 & 2 & 1\end{bmatrix}$
given that $\det (A)=-1.$

Solution: Let's follow the standard five-step procedure.

**Step 1:** We are given the determinant of $A:$

$$
\begin{aligned}\det (A)=-1\end{aligned}
$$

**Step 2:** Form the matrix of the minors of $A.$
To make this matrix, we replace each entry of $A$ by its minor.

$$
\begin{aligned}M & =\begin{bmatrix}\begin{vmatrix}3 & 1 \\ 2 & 1\end{vmatrix} & \begin{vmatrix}2 & 1 \\ 0 & 1\end{vmatrix} & \begin{vmatrix}2 & 3 \\ 0 & 2\end{vmatrix} \\ \begin{vmatrix}0 & 0 \\ 2 & 1\end{vmatrix} & \begin{vmatrix}-1 & 0 \\ 0 & 1\end{vmatrix} & \begin{vmatrix}-1 & 0 \\ 0 & 2\end{vmatrix} \\ \begin{vmatrix}0 & 0 \\ 3 & 1\end{vmatrix} & \begin{vmatrix}-1 & 0 \\ 2 & 1\end{vmatrix} & \begin{vmatrix}-1 & 0 \\ 2 & 3\end{vmatrix}\end{bmatrix} \\  & =\begin{bmatrix}1 & 2 & 4 \\ 0 & -1 & -2 \\ 0 & -1 & -3\end{bmatrix}.\end{aligned}
$$

**Step 3:** Create the matrix of cofactors by changing the sign of some of the entries of $M$ according to the rule of alternating signs.

$$
C=\begin{bmatrix}1 & -2 & 4 \\ 0 & -1 & 2 \\ 0 & 1 & -3\end{bmatrix}.
$$

**Step 4:** Write down the transpose of the matrix of cofactors.

$$
{C}^{T}=\begin{bmatrix}1 & 0 & 0 \\ -2 & -1 & 1 \\ 4 & 2 & -3\end{bmatrix}.
$$

**Step 5:** Use the formula for the inverse of a $3\times 3$ matrix.

$$
\begin{aligned}{A}^{-1} & =\frac{1}{\det (A)}{C}^{T} \\  & =\frac{1}{(-1)}\begin{bmatrix}1 & 0 & 0 \\ -2 & -1 & 1 \\ 4 & 2 & -3\end{bmatrix} \\  & =\begin{bmatrix}-1 & 0 & 0 \\ 2 & 1 & -1 \\ -4 & -2 & 3\end{bmatrix}.\end{aligned}
$$

Answer selection: \begin{bmatrix}-1 & 0 & 0 \\ 2 & 1 & -1 \\ -4 & -2 & 3\end{bmatrix}

### Calculating an Element of the Inverse of a 3x3 Matrix (27 captured questions)

Question 17592186060153 — question.difficulty/easy

Determine the entry ${a}_{12}^{′}$ in the inverse of a matrix $A=\begin{bmatrix}1 & -2 & 4 \\ 0 & 3 & 1 \\ -1 & 0 & 2\end{bmatrix}.$

Solution: First, we need to find the determinant of $A:$

$$
\begin{aligned}\text{det}(A)=\begin{vmatrix}1 & -2 & 4 \\ 0 & 3 & 1 \\ -1 & 0 & 2\end{vmatrix} & =1\begin{vmatrix}3 & 1 \\ 0 & 2\end{vmatrix}-(-2)\begin{vmatrix}0 & 1 \\ -1 & 2\end{vmatrix}+4\begin{vmatrix}0 & 3 \\ -1 & 0\end{vmatrix} \\  & =1(6-0)+2(0+1)+4(0+3) \\  & =6+2+12 \\  & =20.\end{aligned}
$$

 

Since we want the entry ${a}_{12}^{′}$ in ${A}^{-1},$ we need to know the value of ${c}_{21}$ in the matrix of cofactors. For this, we use the formula to get

$$
\begin{aligned}{c}_{21} & =(-1)^{2+1}\begin{vmatrix}-2 & 4 \\ 0 & 2\end{vmatrix} \\  & =-\begin{vmatrix}-2 & 4 \\ 0 & 2\end{vmatrix} \\  & =-(-4-0) \\  & =4.\end{aligned}
$$

Then, since ${A}^{-1}=\frac{1}{\det (A)}{C}^{T},$ we have

$$
\begin{aligned}{a}_{12}^{′}=\frac{1}{\text{det}(A)}{c}_{21}=\frac{1}{20}\cdot 4=\frac{1}{5}.\end{aligned}
$$

Answer selection: \frac{1}{5}

Question 17592186060154 — question.difficulty/easy

Determine the entry ${a}_{33}^{′}$ in the inverse of a matrix $A$ $=\begin{bmatrix}5 & 0 & 3 \\ -2 & -3 & 2 \\ 1 & 1 & 0\end{bmatrix}.$

Solution: First, we need to find the determinant of $A:$ 

$$
\begin{aligned}\text{det}A=\begin{vmatrix}5 & 0 & 3 \\ -2 & -3 & 2 \\ 1 & 1 & 0\end{vmatrix} & =5\begin{vmatrix}-3 & 2 \\ 1 & 0\end{vmatrix}-0\begin{vmatrix}-2 & 2 \\ 1 & 0\end{vmatrix}+3\begin{vmatrix}-2 & -3 \\ 1 & 1\end{vmatrix} \\  & =5(0-2)+0+3(-2+3) \\  & =-10+0+3 \\  & =-7.\end{aligned}
$$

 

Since we want the entry ${a}_{33}^{′}$ in ${A}^{-1},$ we need to know the value of ${c}_{33}$ in the matrix of cofactors. For this, we use the formula to get

$$
\begin{aligned}{c}_{33} & =(-1)^{3+3}\begin{vmatrix}5 & 0 \\ -2 & -3\end{vmatrix} \\  & =\begin{vmatrix}5 & 0 \\ -2 & -3\end{vmatrix} \\  & =-15-0 \\  & =-15.\end{aligned}
$$

Then, since ${A}^{-1}=\frac{1}{\det (A)}{C}^{T},$ we have

$$
\begin{aligned}{a}_{33}^{′}=\frac{1}{\text{det}(A)}{c}_{33}=\frac{1}{-7}\cdot (-15)=\frac{15}{7}.\end{aligned}
$$

Answer selection: \frac{15}{7}

Question 17592186240871 — question.difficulty/easy

Determine the entry ${a}_{23}^{′}$ in the inverse of a matrix $A$ $=\begin{bmatrix}3 & 0 & 1 \\ 1 & 1 & 0 \\ 0 & -1 & 1\end{bmatrix}.$

Solution: First, we need to find the determinant of $A:$ 

$$
\begin{aligned}\text{det}A=\begin{vmatrix}3 & 0 & 1 \\ 1 & 1 & 0 \\ 0 & -1 & 1\end{vmatrix} & =3\begin{vmatrix}1 & 0 \\ -1 & 1\end{vmatrix}-0\begin{vmatrix}1 & 0 \\ 0 & 1\end{vmatrix}+1\begin{vmatrix}1 & 1 \\ 0 & -1\end{vmatrix} \\  & =3(1-0)-0+(-1-0) \\  & =3+0-1 \\  & =2.\end{aligned}
$$

 

Since we want the entry ${a}_{23}^{′}$ in ${A}^{-1},$ we need to know the value of ${c}_{32}$ in the matrix of cofactors. For this, we use the formula to get

$$
\begin{aligned}{c}_{32} & =(-1)^{3+2}\begin{vmatrix}3 & 1 \\ 1 & 0\end{vmatrix} \\  & =-\begin{vmatrix}3 & 1 \\ 1 & 0\end{vmatrix} \\  & =-(0-1) \\  & =1.\end{aligned}
$$

Then, since ${A}^{-1}=\frac{1}{\det (A)}{C}^{T},$ we have

$$
\begin{aligned}{a}_{23}^{′}=\frac{1}{\text{det}(A)}{c}_{32}=\frac{1}{2}\cdot 1=\frac{1}{2}.\end{aligned}
$$

Answer selection: \frac{1}{2}

### Calculating the Cofactor Method To Solve for an Unknown Quantity (27 captured questions)

Question 17592186060450 — question.difficulty/hard

The entry ${a}_{12}^{′}$ in the inverse of the matrix
$$
\displaystyle A=\begin{bmatrix}1 & 2 & 3 \\ 0 & 1 & 4 \\ k & 6 & 0\end{bmatrix}
$$
equals $18.$ Find the value of $k.$

Solution: First, we need to find the determinant of $A:$

$$
\begin{aligned}\det (A)=\begin{vmatrix}1 & 2 & 3 \\ 0 & 1 & 4 \\ k & 6 & 0\end{vmatrix} & =1\begin{vmatrix}1 & 4 \\ 6 & 0\end{vmatrix}-2\begin{vmatrix}0 & 4 \\ k & 0\end{vmatrix}+3\begin{vmatrix}0 & 1 \\ k & 6\end{vmatrix} \\  & =1(0-24)-2(0-4k)+3(0-k) \\  & =8k-3k-24 \\  & =5k-24.\end{aligned}
$$

Since we want the entry ${a}_{12}^{′}$ in ${A}^{-1},$ we need to know the value of ${c}_{21}$ in the matrix of cofactors. For this, we use the formula to get

$$
\begin{aligned}{c}_{21} & =(-1)^{2+1}\begin{vmatrix}2 & 3 \\ 6 & 0\end{vmatrix} \\  & =-\begin{vmatrix}2 & 3 \\ 6 & 0\end{vmatrix} \\  & =-(0-18) \\  & =18.\end{aligned}
$$

Then, since ${A}^{-1}=\frac{1}{\det (A)}{C}^{T},$ we have

$$
\begin{aligned}{a}_{12}^{′} & =\frac{1}{\text{det}(A)}{c}_{21} \\  & =\frac{1}{5k-24}\cdot 18 \\  & =\frac{18}{5k-24}.\end{aligned}
$$

Finally, since we are told that ${a}_{13}^{′}=18$, we have

$$
\begin{aligned}\frac{18}{5k-24} & =18 \\ \frac{1}{5k-24} & =1 \\ 1 & =5k-24 \\ 25 & =5k \\ k & =5.\end{aligned}
$$

Answer selection: 5

Question 17592186060459 — question.difficulty/moderate

The entry $a_{23}^{′}$ in the inverse of the matrix
$$
\displaystyle A = \begin{bmatrix}1 & 0 & -1 \\ 1 & 1 & 3 \\ 3 & k & 1\end{bmatrix}
$$
equals $-1$ and $\det (A) = 4 - 4k$. Find the value of $k$.

Solution: Since $A^{-1}=\dfrac{1}{\det(A)}C^T,$ the entry $a_{23}^{\prime}$ uses the cofactor $C_{32}$. Remove row $3$ and column $2$ to get

$$
C_{32}=(-1)^{3+2}\begin{vmatrix}1 & -1 \\ 1 & 3\end{vmatrix}=-4.
$$

Using the given determinant, we obtain

$$
a_{23}^{\prime}=\frac{-4}{4-4k}.
$$

The inverse exists only when $k\ne1$. Set this entry equal to $-1$ and solve:

$$
\begin{aligned}\frac{-4}{4-4k}&=-1\\-4&=-4+4k\\k&=0.\end{aligned}
$$

At $k=0,$ the determinant is $4\ne0,$ so this value is valid.

Answer selection: 0

Question 17592186240876 — question.difficulty/moderate

The entry ${a}_{12}^{′}$ in the inverse of the matrix
$$
\displaystyle A=\begin{bmatrix}0 & 0 & 1 \\ k & 1 & 1 \\ -2 & 2 & 1\end{bmatrix}
$$
equals $\frac{1}{2}$ and $\det (A)=2k+2.$ Find the value of $k.$

Solution: First, note that we are given the determinant of $A:$

$$
\det (A)=2k+2
$$

Since we want the entry ${a}_{12}^{′}$ in ${A}^{-1},$ we need to know the value of ${c}_{21}$ in the matrix of cofactors. For this, we use the formula to get

$$
\begin{aligned}{c}_{21} & =(-1)^{2+1}\begin{vmatrix}0 & 1 \\ 2 & 1\end{vmatrix} \\  & =-\begin{vmatrix}0 & 1 \\ 2 & 1\end{vmatrix} \\  & =-(0-2) \\  & =2\end{aligned}
$$

Then, since ${A}^{-1}=\frac{1}{\det (A)}{C}^{T},$ we have

$$
\begin{aligned}{a}_{12}^{′} & =\frac{1}{\text{det}(A)}{c}_{21} \\  & =\frac{1}{2k+2}\cdot 2 \\  & =\frac{1}{k+1}.\end{aligned}
$$

Finally, since we are told that ${a}_{12}^{′}=\frac{1}{2}$, we have

$$
\begin{aligned}\frac{1}{k+1} & =\frac{1}{2} \\ k+1 & =2 \\ k & =1.\end{aligned}
$$

Answer selection: 1
