# 17592186049044 The Determinant of a 2x2 Matrix

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186060931 — Introduction

The **determinant** of a general $2 \times 2$ matrix
$$
\displaystyle A = \begin{bmatrix}{\color{blue}{a}} & {\color{red}{b}} \\ {\color{red}{c}} & {\color{blue}{d}}\end{bmatrix}
$$
is denoted $\text {det} ({A})$ and computed as

$$
\displaystyle \text {det} ({A}) = \begin{vmatrix}{\color{blue}{a}} & {\color{red}{b}} \\ {\color{red}{c}} & {\color{blue}{d}}\end{vmatrix} =  {\color{blue}ad} - {\color{red}bc}.
$$

For example, given the matrix
$$
\displaystyle A=
	\begin{bmatrix}{\color{blue}{2}} & {\color{red}{1}} \\ {\color{red}{5}} & {\color{blue}{3}}\end{bmatrix},
$$ 
the determinant is

$$
\det(A) = {\color{blue}{2}} \cdot {\color{blue}{3}} - {\color{red}{1}} \cdot {\color{red}{5}} = 1.
$$

To remember how to compute the determinant of a $2 \times 2$ matrix, you can imagine taking the product of the diagonal of the matrix, and then subtracting the product of the off-diagonal terms, as follows:

![](images/25/2594f99e0f02241dc6d01f85c82923103df1d6fb4dda5ca03d438637f5178a28.png)

Later, we will see that the determinant is related to the "volume" spanned by the row vectors or column vectors in a matrix. We will also see that the determinant can tell us about many other properties of a matrix. 

However, in this lesson, we will just focus on computing the determinant.



### example 17592186059557 — Calculating the Determinant of a 2x2 Matrix With Integer Entries

Calculate $\det(A),$ if <div class="matrix-operands matrix-operands-stacked">
<div>$A=\begin{bmatrix}3 & 2 \\ 5 & 6\end{bmatrix}$</div>
</div>

For a $2 \times 2$ matrix, the determinant is given by the formula

$$
\begin{vmatrix}a & b \\ c & d\end{vmatrix} = ad - bc.
$$

Using the formula, we have:

$$
\begin{aligned}\det (A) & =\begin{vmatrix}3 & 2 \\ 5 & 6\end{vmatrix} \\  & =3\cdot 6-2\cdot 5 \\  & =18-10 \\  & =8\end{aligned}
$$

### example 17592186059558 — Calculating the Determinant of a 2x2 Matrix With Non-Integer Entries

Calculate $\det(A),$ if <div class="matrix-operands matrix-operands-stacked">
<div>$A=\begin{bmatrix}\sqrt{2} & -2 \\ 0 & \sqrt{3}\end{bmatrix}$</div>
</div>

For a $2 \times 2$ matrix, the determinant is given by the formula

$$
\begin{vmatrix}a & b \\ c & d\end{vmatrix} = ad - bc.
$$

Using the formula, we have:

$$
\begin{aligned}\det (A) & =\begin{vmatrix}\sqrt{2} & -2 \\ 0 & \sqrt{3}\end{vmatrix} \\  & =\sqrt{2}\cdot \sqrt{3}-(-2)\cdot 0 \\  & =\sqrt{6}\end{aligned}
$$

### example 17592186059559 — Solving for an Unknown in an Expression Involving the Determinant of a 2x2 Matrix

If
$$
\displaystyle {A} = 
    \left\lbrack
    \begin{matrix}
        2 & -1  \\
        -3 & k
    \end{matrix}
    \right\rbrack
$$
and
$\det({A}) = 5$, what is the value of $k?$

For a $2 \times 2$ matrix, the determinant is given by the formula

$$
\begin{vmatrix}a & b \\ c & d\end{vmatrix} = ad - bc.
$$

Using the formula, we have:

$$
\begin{aligned}\det (A) & =\begin{vmatrix}2 & -1 \\ -3 & k\end{vmatrix} \\  & =2\cdot k-(-1)\cdot (-3) \\  & =2k-3\end{aligned}
$$

Since $\det(A)=5,$ we obtain:

$$
\begin{aligned}\det (A) & =5 \\ 2k-3 & =5 \\ 2k & =8 \\ k & =4\end{aligned}
$$

## Representative practice (first three per skill; full bank in practice.json)

### Calculating the Determinant of a 2x2 Matrix With Integer Entries (26 captured questions)

Question 17592186059980 — question.difficulty/easy

Calculate $\text{det}(A)$, if
$$
\displaystyle A=\begin{bmatrix}1 & 2 \\ 3 & 0\end{bmatrix}.
$$

Solution: For a $2\times 2$ matrix, the determinant is given by the formula

$$
\begin{vmatrix}a & b \\ c & d\end{vmatrix}=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(A) & =\begin{vmatrix}1 & 2 \\ 3 & 0\end{vmatrix} \\  & =1\cdot 0-2\cdot 3 \\  & =0-6 \\  & =-6\end{aligned}
$$

Answer selection: -6

Question 17592186060000 — None

What is $\begin{vmatrix}2 & -4 \\ -2 & 7\end{vmatrix}$?

Solution: For a $2\times 2$ matrix, the determinant is given by the formula

$$
\begin{vmatrix}a & b \\ c & d\end{vmatrix}=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}
\begin{vmatrix}2 & -4 \\ -2 & 7\end{vmatrix}
&=2\cdot7-(-4)\cdot(-2) \\
&=14-8 \\
&=6.
\end{aligned}
$$

Answer selection: 6

Question 17592186244112 — question.difficulty/moderate

Calculate $\text{det}(X)$, if
$$
\displaystyle X=\begin{bmatrix}10 & -3 \\ 1 & 4\end{bmatrix}.
$$

Solution: For a $2\times 2$ matrix, the determinant is given by the formula

$$
\begin{vmatrix}a & b \\ c & d\end{vmatrix}=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(X) & =\begin{vmatrix}10 & -3 \\ 1 & 4\end{vmatrix} \\  & =10\cdot 4-(-3)\cdot 1 \\  & =40-(-3) \\  & =43\end{aligned}
$$

Answer selection: 43

### Calculating the Determinant of a 2x2 Matrix With Non-Integer Entries (26 captured questions)

Question 17592186059981 — None

What is $\begin{vmatrix}\sqrt{2} & 5 \\ 1 & 3\end{vmatrix}$?

Solution: For a $2\times 2$ matrix, the determinant is given by the formula

$$
\begin{vmatrix}a & b \\ c & d\end{vmatrix}=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}
\begin{vmatrix}\sqrt{2} & 5 \\ 1 & 3\end{vmatrix}
&=\sqrt{2}\cdot3-5\cdot1 \\
&=3\sqrt{2}-5.
\end{aligned}
$$

Answer selection: 3\sqrt{2} - 5

Question 17592186059982 — question.difficulty/easy

Calculate $\det (Z)$, if
 $$
\displaystyle Z=\begin{bmatrix}\sqrt{x} & y \\ {y}^{2} & \sqrt{x}\end{bmatrix}.
$$

Solution: For a $2\times 2$ matrix, the determinant is given by the formula

$$
\begin{vmatrix}a & b \\ c & d\end{vmatrix}=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(Z) & =\begin{vmatrix}\sqrt{x} & y \\ {y}^{2} & \sqrt{x}\end{vmatrix} \\  & =\sqrt{x}\cdot \sqrt{x}-y\cdot {y}^{2} \\  & =x-{y}^{3}\end{aligned}
$$

Answer selection: x-{y}^{3}

Question 17592186244117 — question.difficulty/easy

$$
\displaystyle \begin{vmatrix}2x & {y}^{2} \\ z & -3\end{vmatrix}=
$$

Solution: For a $2\times 2$ matrix, the determinant is given by the formula

$$
\begin{vmatrix}a & b \\ c & d\end{vmatrix}=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\begin{vmatrix}2x & {y}^{2} \\ z & -3\end{vmatrix} & =2x\cdot (-3)-{y}^{2}\cdot z \\  & =-6x-{y}^{2}z\end{aligned}
$$

Answer selection: -6x-{y}^{2}z

### Solving for an Unknown in an Expression Involving the Determinant of a 2x2 Matrix (27 captured questions)

Question 17592186060001 — None

If
$$
\displaystyle C = \begin{bmatrix}2 & 3 \\ 5 & k\end{bmatrix}
$$
and
$\det (C) = 3$, what is the value of $k$?

Solution: For a $2\times 2$ matrix, the determinant is given by the formula

$$
\begin{vmatrix}a & b \\ c & d\end{vmatrix}=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}
\det(C)&=\begin{vmatrix}2 & 3 \\ 5 & k\end{vmatrix} \\
&=2\cdot k-3\cdot5 \\
&=2k-15.
\end{aligned}
$$

Since $\det(C)=3$, we obtain:

$$
\begin{aligned}
2k-15&=3 \\
2k&=18 \\
k&=9.
\end{aligned}
$$

Answer selection: k = 9

Question 17592186060195 — None

If
$$
\displaystyle A = \begin{bmatrix}1 + t & 2t \\ -3 & 1 - t\end{bmatrix}
$$
and $\det (A) = 10$, what is the value of $t$?

Solution: For a $2\times 2$ matrix, the determinant is given by the formula

$$
\begin{vmatrix}a & b \\ c & d\end{vmatrix}=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}
\det(A)&=\begin{vmatrix}1+t & 2t \\ -3 & 1-t\end{vmatrix} \\
&=(1+t)(1-t)-(2t)(-3) \\
&=1-t^2+6t.
\end{aligned}
$$

Since $\det(A)=10$, we obtain:

$$
\begin{aligned}
1-t^2+6t&=10 \\
t^2-6t+9&=0 \\
(t-3)^2&=0 \\
t&=3.
\end{aligned}
$$

Answer selection: 3

Question 17592186233379 — question.difficulty/moderate

If
$$
\displaystyle D=\begin{bmatrix}2x & 6 \\ 2x & x-2\end{bmatrix}
$$
and $\det (D)=-32$, what is the value of $x?$

$x=$ {{field-1}}

Solution: For a $2\times 2$ matrix, the determinant is given by the formula

$$
\begin{vmatrix}a & b \\ c & d\end{vmatrix}=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\det (D) & =\begin{vmatrix}2x & 6 \\ 2x & x-2\end{vmatrix} \\  & =2x\cdot (x-2)-6\cdot 2x \\  & =2{x}^{2}-16x\end{aligned}
$$

Since $\det (D)=-32$, we obtain:

$$
\begin{aligned}\det (D) & =-32 \\ 2{x}^{2}-16x & =-32 \\ 2{x}^{2}-16x+32 & =0 \\ {x}^{2}-8x+16 & =0 \\ (x-4)^{2} & =0 \\ x & =4\end{aligned}
$$

Answer field-1: 4
