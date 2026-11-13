# 17592186048965 The Minors of a 3x3 Matrix

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186060932 — Introduction

The **minor** of the entry $a_{ij}$ in a matrix $A$ is the determinant of the remaining entries when the row and column containing $a_{ij}$ are removed.

For instance, suppose we want to find the minor of $a_{{\color{red}1}{\color{blue}2}} = {\bbox[lightgray, 2pt]{-1}}$ (row ${\color{red}1}$, column ${\color{blue}2}$) in the matrix $A$ given by

$$
A=
\begin{bmatrix}3 & -1 & 6 \\ 5 & 2 & 7 \\ 8 & 9 & 4\end{bmatrix}.
$$

To find the minor, we exclude all entries in row $1$ and all entries in column $2\mathbin{:}$

$$
A=
\begin{bmatrix}{\color{gray}{\enclose{updiagonalstrike}{3}}} & {\color{gray}{-1}} & {\color{gray}{\enclose{updiagonalstrike}{6}}} \\ 5 & {\color{gray}{\enclose{updiagonalstrike}{2}}} & 7 \\ 8 & {\color{gray}{\enclose{updiagonalstrike}{9}}} & 4\end{bmatrix}
$$

This leaves us with the $2\times 2$ determinant given by

$$
M_{12} = \begin{vmatrix}5 & 7 \\ 8 & 4\end{vmatrix}
$$

We call it $M_{{\color{red}{1}}{\color{blue}{2}}}$ to denote the fact that it was obtained by deleting row $\color{red}1$ and column $\color{blue}2$ of the matrix $A.$

Finally, we compute the above determinant:

$$
\begin{aligned}\begin{vmatrix}5 & 7 \\ 8 & 4\end{vmatrix} & =5\cdot 4-7\cdot 8 \\  & =20-56 \\  & =-36\end{aligned}
$$



### example 17592186059560 — Calculating a Minor in a 3x3 Matrix With Integer Entries

Calculate the minor of the entry $b_{21}$ in the matrix
$$
B= 
{\left[ \begin{array}{ccc}10 & 1 & 5 \\ 3 & 6 & 8 \\ 4 & 7 & 2\end{array} \right]}.
$$

The minor of $b_{21} = 3$ (second row, first column) is the determinant of the remaining entries when the column and row containing $3$ are removed: 

$$
B= 
{\left[ \begin{array}{ccc}{\color{gray}∗} & 1 & 5 \\ \bbox[2pt,lightgray]{ {\color{gray}3}} & {\color{gray}∗} & {\color{gray}∗} \\ {\color{gray}∗} & 7 & 2\end{array} \right]}
$$

So, the minor of $b_{21}=3$ is

$$
\begin{aligned}\det \begin{bmatrix}1 & 5 \\ 7 & 2\end{bmatrix} & =\begin{vmatrix}1 & 5 \\ 7 & 2\end{vmatrix} \\  & =1\cdot 2-5\cdot 7 \\  & =2-35 \\  & =-33.\end{aligned}
$$

### example 17592186059561 — Calculating a Minor in a 3x3 Matrix With Variable Entries

What is the minor of $c_{22}$ in the matrix
$$
C=
{\left[ \begin{array}{ccc}7 x & 0 & - 3 y \\ 1 & x + 2 y & 4 \\ - y & 0 & 5\end{array} \right]}?
$$

First, we remove the second row and second column: 

$$
C=
{\left[ \begin{array}{ccc}7 x & {\color{gray}∗} & - 3 y \\ {\color{gray}∗} & \bbox[2pt,lightgray]{ {\color{gray}x + 2 y}} & {\color{gray}∗} \\ - y & {\color{gray}∗} & 5\end{array} \right]}
$$

Next, we calculate the determinant:

$$
\begin{aligned}\det \begin{bmatrix}7x & -3y \\ -y & 5\end{bmatrix} & =\begin{vmatrix}7x & -3y \\ -y & 5\end{vmatrix} \\  & =7x\cdot 5-(-3y)\cdot (-y) \\  & =35x-3{y}^{2}\end{aligned}
$$

### example 17592186059562 — Solving for an Unknown Given the Value of a Minor

Given that the minor of $a_{23}$ is $5,$ find all the possible values of $k$ in the matrix
$$
A= {\left[ \begin{array}{ccc}k & 3 & - 1 \\ - 5 & 2 & 7 \\ - 1 & 2 k & - 6\end{array} \right]}.
$$

First, we remove the second row and third column:

$$
A= {\left[ \begin{array}{ccc}k & 3 & {\color{gray}∗} \\ {\color{gray}∗} & {\color{gray}∗} & \bbox[2pt,lightgray]{ {\color{gray}7}} \\ - 1 & 2 k & {\color{gray}∗}\end{array} \right]}
$$

The minor of $a_{23}$ is

$$
\begin{aligned}\det \begin{bmatrix}k & 3 \\ -1 & 2k\end{bmatrix} & =\begin{vmatrix}k & 3 \\ -1 & 2k\end{vmatrix} \\  & =k\cdot 2k-3\cdot (-1) \\  & =2{k}^{2}+3.\end{aligned}
$$

We're told that the minor of $a_{23}$ is $5,$ so we must have:

$$
\begin{aligned}2{k}^{2}+3 & =5 \\ 2{k}^{2} & =2 \\ {k}^{2} & =1 \\ k & =\pm 1\end{aligned}
$$

Therefore, the solutions are $k=-1$ and $k=1.$

## Representative practice (first three per skill; full bank in practice.json)

### Calculating a Minor in a 3x3 Matrix With Integer Entries (30 captured questions)

Question 17592186059985 — None

Calculate the minor of the entry $a_{23}$ in the matrix
$$
\displaystyle A = \begin{bmatrix}1 & 2 & 7 \\ -6 & 0 & 4 \\ 12 & 3 & 5\end{bmatrix}.
$$

Solution: 

Question 17592186059987 — question.difficulty/easy

Calculate the minor of the entry ${y}_{13}$ in the matrix
$$
\displaystyle Y=\begin{bmatrix}15 & 8 & 9 \\ 7 & 1 & 2 \\ 0 & -1 & 2\end{bmatrix}.
$$

Solution: The minor of ${y}_{13}=9$ (first row, third column) is the determinant of the remaining entries when the column and row containing $9$ are removed: 

$$
Y=\begin{bmatrix}∗ & ∗ & 9 \\ 7 & 1 & ∗ \\ 0 & -1 & ∗\end{bmatrix}
$$

So, the minor of ${y}_{13}=9$ is

$$
\begin{aligned}\det \begin{bmatrix}7 & 1 \\ 0 & -1\end{bmatrix} & =\begin{vmatrix}7 & 1 \\ 0 & -1\end{vmatrix} \\  & =7\cdot (-1)-1\cdot 0 \\  & =-7-0 \\  & =-7.\end{aligned}
$$

Answer selection: -7

Question 17592186233380 — question.difficulty/easy

Calculate the minor of the entry ${p}_{32}$ in the matrix
$$
\displaystyle P=\begin{bmatrix}8 & 8 & 4 \\ -5 & 4 & 6 \\ 10 & 3 & 0\end{bmatrix}.
$$

Solution: The minor of ${p}_{32}=3$ (third row, second column) is the determinant of the remaining entries when the column and row containing $3$ are removed: 

$$
P=\begin{bmatrix}8 & ∗ & 4 \\ -5 & ∗ & 6 \\ ∗ & 3 & ∗\end{bmatrix}
$$

So, the minor of ${p}_{32}=3$ is

$$
\begin{aligned}\text{det}\begin{bmatrix}8 & 4 \\ -5 & 6\end{bmatrix} & =\begin{vmatrix}8 & 4 \\ -5 & 6\end{vmatrix} \\  & =8\cdot 6-4\cdot (-5) \\  & =48+20 \\  & =68.\end{aligned}
$$

Answer selection: 68

### Calculating a Minor in a 3x3 Matrix With Variable Entries (37 captured questions)

Question 17592186059988 — question.difficulty/moderate

What is the minor of ${x}_{12}$ in the matrix
$$
\displaystyle X=\begin{bmatrix}6a & -3a & c \\ -b & {b}^{2} & -2c \\ -a & 0 & b\end{bmatrix}?
$$

Solution: First, we remove the first row and second column:

$$
X=\begin{bmatrix}∗ & -3a & ∗ \\ -b & ∗ & -2c \\ -a & ∗ & b\end{bmatrix}
$$

Next, we calculate the determinant:

$$
\begin{aligned}\det \begin{bmatrix}-b & -2c \\ -a & b\end{bmatrix} & =\begin{vmatrix}-b & -2c \\ -a & b\end{vmatrix} \\  & =-b\cdot b-(-2c)\cdot (-a) \\  & =-{b}^{2}-2ac\end{aligned}
$$

Answer selection: -{b}^{2}-2ac

Question 17592186059989 — question.difficulty/moderate

What is the minor of ${d}_{32}$ in the matrix
$$
\displaystyle D=\begin{bmatrix}3s & -{r}^{2} & 2t \\ -r & 0 & r \\ 5t & 4r & 1\end{bmatrix}?
$$

Solution: First, we remove the third row and second column:

$$
D=\begin{bmatrix}3s & ∗ & 2t \\ -r & ∗ & r \\ ∗ & 4r & ∗\end{bmatrix}
$$

Next, we calculate the determinant:

$$
\begin{aligned}\det \begin{bmatrix}3s & 2t \\ -r & r\end{bmatrix} & =\begin{vmatrix}3s & 2t \\ -r & r\end{vmatrix} \\  & =3s\cdot r-2t\cdot (-r) \\  & =3rs-(-2rt) \\  & =3rs+2rt\end{aligned}
$$

Answer selection: 3rs+2rt

Question 17592186262866 — question.difficulty/moderate

What is the minor of ${a}_{12}$ in the matrix
$$
\displaystyle A=\begin{bmatrix}4 & -3d & 5b \\ b & {c}^{2} & b-d \\ b & -10c & b+d\end{bmatrix}?
$$

Solution: First, we remove the first row and second column:

$$
A=\begin{bmatrix}∗ & -3d & ∗ \\ b & ∗ & b-d \\ b & ∗ & b+d\end{bmatrix}
$$

Next, we calculate the determinant:

$$
\begin{aligned}\det \begin{bmatrix}b & b-d \\ b & b+d\end{bmatrix} & =\begin{vmatrix}b & b-d \\ b & b+d\end{vmatrix} \\  & =b\cdot (b+d)-(b-d)\cdot b \\  & ={b}^{2}+bd-{b}^{2}+db \\  & =2bd\end{aligned}
$$

Answer selection: 2bd

### Solving for an Unknown Given the Value of a Minor (33 captured questions)

Question 17592186060138 — None

Given that the minor of $a_{22}$ is $2k^{2} + 26$, find all the possible values of $k$ in the matrix
$$
\displaystyle A = \begin{bmatrix}-2 & 9 & -10 \\ 8 & -5 & 3 \\ 2k - 2 & 7 & 1\end{bmatrix}.
$$

Solution: 

Question 17592186060141 — question.difficulty/hard

Given that the minor of ${p}_{23}$ is ${t}^{2}+12$, find all the possible values of $t$ in the matrix

$$
P=\begin{bmatrix}t & -8 & 3 \\ -7 & 4 & 4 \\ -1 & 9 & 0\end{bmatrix}.
$$

Solution: First, we remove the second row and third column:

$$
P=\begin{bmatrix}t & -8 & ∗ \\ ∗ & ∗ & 4 \\ -1 & 9 & ∗\end{bmatrix}
$$

The minor of ${p}_{23}$ is

$$
\begin{aligned}\text{det}\begin{bmatrix}t & -8 \\ -1 & 9\end{bmatrix} & =\begin{vmatrix}t & -8 \\ -1 & 9\end{vmatrix} \\  & =t\cdot 9-(-8)\cdot (-1) \\  & =9t-8.\end{aligned}
$$

We're told that the minor of ${p}_{23}$ is ${t}^{2}+12$, so we must have:

$$
\begin{aligned}9t-8 & ={t}^{2}+12 \\ {t}^{2}-9t+20 & =0 \\ (t-5)(t-4) & =0\end{aligned}
$$

Therefore, the solutions are $t=4$ and $t=5.$

Answer selection: $t=4$ and $t=5$ only

Question 17592186262870 — question.difficulty/moderate

Given that the minor of ${p}_{11}$ is $4$, find all the possible values of $t$ in the matrix

$$
P=\begin{bmatrix}-5t & 18 & 6t \\ -3 & 9 & 5 \\ 19t & 1 & 3t\end{bmatrix}.
$$

Solution: First, we remove the first row and first column:

$$
P=\begin{bmatrix}5t & ∗ & ∗ \\ ∗ & 9 & 5 \\ ∗ & 1 & 3t\end{bmatrix}
$$

The minor of ${p}_{11}$ is

 

$$
\begin{aligned}\text{det}\begin{bmatrix}9 & 5 \\ 1 & 3t\end{bmatrix} & =\begin{vmatrix}9 & 5 \\ 1 & 3t\end{vmatrix} \\  & =9\cdot 3t-5\cdot 1 \\  & =27t-5.\end{aligned}
$$

We're told that the minor of ${p}_{11}$ is $4$, so we must have:

$$
\begin{aligned}27t-5 & =4 \\ 27t & =9 \\ t & =\frac{1}{3}\end{aligned}
$$

Therefore, the solution is $t=\frac{1}{3}.$

Answer selection: t=\frac{1}{3}
