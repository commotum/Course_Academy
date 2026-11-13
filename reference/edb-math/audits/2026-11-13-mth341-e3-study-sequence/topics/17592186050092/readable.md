# 17592186050092 The Determinant of an NxN Matrix

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186121025 — Introduction

The minor of the entry $a_{ij}$ in a $n\times n$ matrix is the determinant that we get when the rows and columns containing $a_{ij}$ are removed.

For example, suppose that we wish to find the minor of $a_{32}$ in the following matrix:

<div class="matrix-operands matrix-operands-stacked">
<div>$A=\begin{bmatrix}2 & 3 & 2 & 3 \\ 4 & 2 & 5 & 12 \\ 1 & -2 & 0 & -5 \\ -5 & 1 & 3 & 0\end{bmatrix}$</div>
</div>

To get the minor of $a_{\color{red}{3}\color{blue}{2}}$, we remove the $\color{red}3$rd row and $\color{blue}2$nd column:

$$
\begin{bmatrix}2 & {\color{lightgray}∗} & 2 & 3 \\ 4 & {\color{lightgray}∗} & 5 & 12 \\ {\color{lightgray}∗} & {\color{lightgray}-2} & {\color{lightgray}∗} & {\color{lightgray}∗} \\ -5 & {\color{gray}∗} & 3 & 0\end{bmatrix}
$$

So, the minor of $a_{32}$, denoted $M_{32}$, is 

$$
M_{32}=
\begin{vmatrix}2 & 2 & 3 \\ 4 & 5 & 12 \\ -5 & 3 & 0\end{vmatrix}.
$$

We can now calculate the value of $M_{32}$ by evaluating the determinant using previously discussed methods.



### example 17592186119595 — Calculating a Minor in a NxN Matrix

What is the minor of $a_{13}$ in 
$$
A=
{\left[ \begin{array}{cccc}0 & 0 & 2 & 3 \\ 5 & 1 & 2 & 0 \\ 1 & 6 & 0 & - 1 \\ - 6 & 3 & 1 & 0\end{array} \right]}?
$$

To get the minor of $a_{13}$, we remove the $1$st row and $3$rd column:

$$
A=
{\left[ \begin{array}{cccc}{\color{lightgray}∗} & {\color{lightgray}∗} & {\color{lightgray}2} & {\color{lightgray}∗} \\ 5 & 1 & {\color{lightgray}∗} & 0 \\ 1 & 6 & {\color{lightgray}∗} & - 1 \\ - 6 & 3 & {\color{lightgray}∗} & 0\end{array} \right]}
$$

So, the minor is 

$$
M_{13}=
{\left| \begin{array}{ccc}5 & 1 & 0 \\ 1 & 6 & - 1 \\ - 6 & 3 & 0\end{array} \right|}.
$$

### tutorial 17592186121060 — Calculating a Cofactor of a NxN Matrix

In general, for any $n\times n$ matrix $A,$ the **cofactor** $C_{ij}$ of the entry $\color{red}a_{ij}$ is

$$
{\color{blue}C_{ij}}=(-1)^{i+j}{\color{blue}M_{ij}}.
$$

Cofactors are a useful tool in helping us to compute determinants of larger matrices. Before we learn how, let's get some practice at computing cofactors.



### example 17592186119596 — Calculating a Cofactor in a NxN Matrix

Find the cofactor of $d_{23}$ in 
$$
D=
{\left[ \begin{array}{cccc}0 & 2 & 3 & - 6 \\ 7 & - 3 & - 2 & - 1 \\ 6 & 0 & 8 & 9 \\ 5 & 4 & 0 & 0\end{array} \right]}
.
$$

First, to get the minor of $d_{23}$, we remove the $2$nd row and $3$rd column:

$$
D=
{\left[ \begin{array}{cccc}0 & 2 & {\color{lightgray}∗} & - 6 \\ {\color{lightgray}∗} & {\color{lightgray}∗} & {\color{lightgray}- 2} & {\color{lightgray}∗} \\ 6 & 0 & {\color{lightgray}∗} & 9 \\ 5 & 4 & {\color{lightgray}∗} & 0\end{array} \right]}
$$

So, the minor is 

$$
M_{23}=
	\left|
	{\begin{array}{ccc}0 & 2 & - 6 \\ 6 & 0 & 9 \\ 5 & 4 & 0\end{array}}
	\right|.
$$

Now, the cofactor of $d_{23}$ is

$$
\begin{aligned}{C}_{23} & =(-1)^{2+3}{M}_{23} \\  & =-{M}_{23} \\  & =-\begin{vmatrix}0 & 2 & -6 \\ 6 & 0 & 9 \\ 5 & 4 & 0\end{vmatrix}.\end{aligned}
$$

### tutorial 17592186121059 — Calculating Determinants Using Cofactors

One way to find the determinant of a $3\!\times\! 3$ matrix $A$ is to take the alternating sum of the entries of the top row of the matrix, multiplied by their respective minors, as follows:

$$
\det(A) = {\color{red}a_{11}}{\color{blue}M_{11}} - {\color{red}a_{12}}{\color{blue}M_{12}} + {\color{red}a_{13}}{\color{blue}M_{13}}
$$

Remember that we had to change the sign of the second product. When we multiply a minor of an entry by the respective sign in the formula like this, we get the cofactor of the entry. The cofactors in the above formula were ${\color{blue}M_{11}},$ $-{\color{blue}M_{12}},$ and ${\color{blue}M_{13}}.$

Using this idea, we can write the formula for the determinant of a $3\!\times\! 3$ matrix $A$ in terms of cofactors, as follows:

$$
\det(A) = {\color{red}a_{11}}{\color{blue}C_{11}} + {\color{red}a_{12}}{\color{blue}C_{12}} + {\color{red}a_{13}}{\color{blue}C_{13}}
$$

This is called the **cofactor expansion** of the determinant across the first row.

In fact, we can use a similar method of multiplying the entries of the top row of the matrix by their respective cofactors to find the determinant for any $n\!\times\! n$ matrix $A$ when $n \ge 3$. The formula is

$$
\begin{aligned}\det (A) & ={\sum }_{j=1}^{n}{a}_{1j}{C}_{1j} \\  & ={a}_{11}{C}_{11}+{a}_{12}{C}_{12}+⋯+{a}_{1n}{C}_{1n}.\end{aligned}
$$

Let's see how to use this formula in the next example.



### example 17592186119597 — Calculating the Determinant of a NxN Matrix Using Cofactor Expansion

Calculate the determinant of the matrix
$$
A=
\left[
	{\begin{array}{cccc}0 & 0 & 2 & 0 \\ 5 & 1 & 2 & 0 \\ 1 & 6 & 0 & - 1 \\ - 6 & 3 & 1 & 0\end{array}}
\right].
$$

We use the cofactor expansion along the first row:

$$
\begin{aligned}\det (A) & ={a}_{11}{C}_{11}+{a}_{12}{C}_{12}+{a}_{13}{C}_{13}+{a}_{14}{C}_{14} \\  & =0\cdot {C}_{11}+0\cdot {C}_{12}+2\cdot {C}_{13}+0\cdot {C}_{14} \\  & =2{C}_{13} \\  & =2\cdot \begin{vmatrix}∗ & ∗ & 2 & ∗ \\ 5 & 1 & ∗ & 0 \\ 1 & 6 & ∗ & -1 \\ -6 & 3 & ∗ & 0\end{vmatrix} \\  & =2(-1)^{1+3}\begin{vmatrix}5 & 1 & 0 \\ 1 & 6 & -1 \\ -6 & 3 & 0\end{vmatrix} \\  & =2\left(5\begin{vmatrix}6 & -1 \\ 3 & 0\end{vmatrix}-1\begin{vmatrix}1 & -1 \\ -6 & 0\end{vmatrix}+0\begin{vmatrix}1 & 6 \\ -6 & 3\end{vmatrix}\right) \\  & =2(5(6\cdot 0+1\cdot 3)-(1\cdot 0-(-1)\cdot (-6))+0(1\cdot 3-6\cdot (-6))) \\  & =2(15+6+0) \\  & =2\cdot 21 \\  & =42\end{aligned}
$$

## Representative practice (first three per skill; full bank in practice.json)

### Calculating a Minor in a NxN Matrix (13 captured questions)

Question 17592186120509 — question.difficulty/easy

What is the minor of ${x}_{33}$ in 
$$
\displaystyle X=\begin{bmatrix}-2 & 0 & 1 & 0 \\ -1 & 3 & 1 & 3 \\ 2 & 1 & -1 & 5 \\ 1 & 4 & 1 & -2\end{bmatrix}?
$$

Solution: To get the minor of ${x}_{33}$, we remove the $3$rd row and $3$rd column:

$$
X=\begin{bmatrix}-2 & 0 & {\color{gray}∗} & 0 \\ -1 & 3 & {\color{gray}∗} & 3 \\ {\color{gray}∗} & {\color{gray}∗} & \bbox[lightgray, 2pt]{-1} & {\color{gray}∗} \\ 1 & 4 & {\color{gray}∗} & -2\end{bmatrix}
$$

So, the minor is 

$$
{M}_{33}=\begin{vmatrix}-2 & 0 & 0 \\ -1 & 3 & 3 \\ 1 & 4 & -2\end{vmatrix}.
$$

Answer selection: \begin{vmatrix}-2 & 0 & 0 \\ -1 & 3 & 3 \\ 1 & 4 & -2\end{vmatrix}

Question 17592186120510 — question.difficulty/easy

Find the minor of ${q}_{23}$ in 
$$
\displaystyle Q=\begin{bmatrix}1 & 2 & -1 & 1 \\ -2 & 9 & 1 & 0 \\ -1 & 1 & -1 & 0 \\ 4 & 5 & 8 & 0\end{bmatrix}.
$$

Solution: To get the minor of  ${q}_{23}$, we remove the $2$nd row and $3$rd column:

$$
Q=\begin{bmatrix}1 & 2 & {\color{gray}∗} & 1 \\ {\color{gray}∗} & {\color{gray}∗} & \bbox[lightgray, 2pt]{1} & {\color{gray}∗} \\ -1 & 1 & {\color{gray}∗} & 0 \\ 4 & 5 & {\color{gray}∗} & 0\end{bmatrix}
$$

So, the minor is 

$$
{M}_{23}=\begin{vmatrix}1 & 2 & 1 \\ -1 & 1 & 0 \\ 4 & 5 & 0\end{vmatrix}.
$$

Answer selection: \begin{vmatrix}1 & 2 & 1 \\ -1 & 1 & 0 \\ 4 & 5 & 0\end{vmatrix}

Question 17592186265949 — question.difficulty/easy

What is the minor of ${x}_{12}$ in 
$$
\displaystyle X=\begin{bmatrix}5 & 0 & 1 & -2 \\ 3 & 3 & 11 & 7 \\ \sqrt{2} & 1 & -8 & 8 \\ -6 & 4 & 1 & -2\end{bmatrix}?
$$

Solution: To get the minor of ${x}_{12}$, we remove the $1$st row and $2$nd column:

$$
X=\begin{bmatrix}{\color{gray}∗} & \bbox[lightgray, 2pt]{0} & {\color{gray}∗} & {\color{gray}∗} \\ 3 & {\color{gray}∗} & 11 & 7 \\ \sqrt{2} & {\color{gray}∗} & -8 & 8 \\ -6 & {\color{gray}∗} & 1 & -2\end{bmatrix}
$$

So, the minor is 

$$
{M}_{12}=\begin{vmatrix}3 & 11 & 7 \\ \sqrt{2} & -8 & 8 \\ -6 & 1 & -2\end{vmatrix}.
$$

Answer selection: \begin{vmatrix}3 & 11 & 7 \\ \sqrt{2} & -8 & 8 \\ -6 & 1 & -2\end{vmatrix}

### Calculating a Cofactor in a NxN Matrix (15 captured questions)

Question 17592186120400 — question.difficulty/easy

Find the cofactor of ${a}_{23}$ in 
$$
\displaystyle A=\begin{bmatrix}1 & -7 & 5 & 3 \\ 0 & 0 & 0 & 2 \\ 9 & 0 & 11 & -1 \\ 3 & -5 & 1 & 0\end{bmatrix}.
$$

Solution: First, to get the minor of ${a}_{23}$, we remove the $2$nd row and $3$rd column: 

$$
A=\begin{bmatrix}1 & -7 & {\color{gray}∗} & 3 \\ {\color{gray}∗} & {\color{gray}∗} & \bbox[lightgray, 2pt]{{\color{gray}0}} & {\color{gray}∗} \\ 9 & 0 & {\color{gray}∗} & -1 \\ 3 & -5 & {\color{gray}∗} & 0\end{bmatrix}
$$

So, the minor is 

$$
{M}_{23}=\begin{vmatrix}1 & -7 & 3 \\ 9 & 0 & -1 \\ 3 & -5 & 0\end{vmatrix}.
$$

Now, the cofactor of ${a}_{23}$ is

$$
\begin{aligned}{C}_{23} & =(-1)^{2+3}{M}_{23} \\  & =-{M}_{23} \\  & =-\begin{vmatrix}1 & -7 & 3 \\ 9 & 0 & -1 \\ 3 & -5 & 0\end{vmatrix}.\end{aligned}
$$

Answer selection: -\begin{vmatrix}1 & -7 & 3 \\ 9 & 0 & -1 \\ 3 & -5 & 0\end{vmatrix}

Question 17592186120505 — None

Find the cofactor of $d_{33}$ in $$
\displaystyle D = \begin{bmatrix}-1 & 2 & 3 & 4 \\ 5 & -6 & 7 & 8 \\ 9 & 1 & -2 & 3 \\ 4 & 5 & 6 & -7\end{bmatrix}.
$$

Solution: First, to get the minor of $d_{33}$, remove the $3$rd row and $3$rd column:

$$
M_{33}=\begin{vmatrix}-1 & 2 & 4 \\ 5 & -6 & 8 \\ 4 & 5 & -7\end{vmatrix}.
$$

The cofactor includes the alternating sign $(-1)^{i+j}$. Therefore,

$$
C_{33}=(-1)^{3+3}M_{33}=M_{33}=\begin{vmatrix}-1 & 2 & 4 \\ 5 & -6 & 8 \\ 4 & 5 & -7\end{vmatrix}.
$$

Answer selection: \begin{vmatrix}-1 & 2 & 4 \\ 5 & -6 & 8 \\ 4 & 5 & -7\end{vmatrix}

Question 17592186266007 — question.difficulty/moderate

Find the cofactor of ${d}_{51}$ in 
$$
\displaystyle D=\begin{bmatrix}-5 & -8 & 2 & 0 & 1 \\ 3 & 5 & 0 & 7 & 1 \\ -1 & 0 & -5 & 6 & -4 \\ 4 & 0 & 6 & 8 & 3 \\ 11 & 3 & 0 & -9 & 3\end{bmatrix}.
$$

Solution: First, to get the minor of ${d}_{51}$, we remove the $5$th row and $1$st column: 

$$
D=\begin{bmatrix}{\color{gray}∗} & -8 & 2 & 0 & 1 \\ {\color{gray}∗} & 5 & 0 & 7 & 1 \\ {\color{gray}∗} & 0 & -5 & 6 & -4 \\ {\color{gray}∗} & 0 & 6 & 8 & 3 \\ \bbox[lightgray, 2pt]{{\color{gray}11}} & {\color{gray}∗} & {\color{gray}∗} & {\color{gray}∗} & {\color{gray}∗}\end{bmatrix}
$$

So, the minor is 

$$
{M}_{51}=\begin{vmatrix}-8 & 2 & 0 & 1 \\ 5 & 0 & 7 & 1 \\ 0 & -5 & 6 & -4 \\ 0 & 6 & 8 & 3\end{vmatrix}.
$$

Now, the cofactor of ${d}_{51}$ is

$$
\begin{aligned}{C}_{51} & =(-1)^{5+1}{M}_{51} \\  & ={M}_{51} \\  & =\begin{vmatrix}-8 & 2 & 0 & 1 \\ 5 & 0 & 7 & 1 \\ 0 & -5 & 6 & -4 \\ 0 & 6 & 8 & 3\end{vmatrix}.\end{aligned}
$$

Answer selection: \begin{vmatrix}-8 & 2 & 0 & 1 \\ 5 & 0 & 7 & 1 \\ 0 & -5 & 6 & -4 \\ 0 & 6 & 8 & 3\end{vmatrix}

### Calculating the Determinant of a NxN Matrix Using Cofactor Expansion (14 captured questions)

Question 17592186120207 — question.difficulty/moderate

Calculate the determinant of the matrix
$$
\displaystyle A=\begin{bmatrix}0 & 8 & 0 & 0 \\ -1 & 0 & 0 & 0 \\ 3 & 1 & 6 & 2 \\ 1 & 0 & -1 & 2\end{bmatrix}
$$

Solution: We use the cofactor expansion along the first row:

$$
\begin{aligned}\det (A) & ={a}_{11}{C}_{11}+{a}_{12}{C}_{12}+{a}_{13}{C}_{13}+{a}_{14}{C}_{14} \\  & =0\cdot {C}_{11}+8\cdot {C}_{12}+0\cdot {C}_{13}+0\cdot {C}_{14} \\  & =8{C}_{12} \\  & =8\cdot \begin{vmatrix}{\color{lightgray}∗} & {\color{lightgray}8} & {\color{lightgray}∗} & {\color{lightgray}∗} \\ -1 & {\color{lightgray}∗} & 0 & 0 \\ 3 & {\color{lightgray}∗} & 6 & 2 \\ 1 & {\color{lightgray}∗} & -1 & 2\end{vmatrix} \\  & =8(-1)^{1+2}\begin{vmatrix}-1 & 0 & 0 \\ 3 & 6 & 2 \\ 1 & -1 & 2\end{vmatrix} \\  & =-8\left((-1)\cdot \begin{vmatrix}6 & 2 \\ -1 & 2\end{vmatrix}-0\cdot \begin{vmatrix}3 & 2 \\ 1 & 2\end{vmatrix}+0\cdot \begin{vmatrix}3 & 6 \\ 1 & -1\end{vmatrix}\right) \\  & =8(6\cdot 2-(-1)\cdot 2)-0+0 \\  & =8\cdot 14 \\  & =112\end{aligned}
$$

Answer selection: 112

Question 17592186120401 — question.difficulty/hard

Calculate the determinant of the matrix
$$
\displaystyle A=\begin{bmatrix}-3 & 0 & 0 & 5 \\ 0 & 0 & 3 & -2 \\ 4 & -1 & 2 & -3 \\ -1 & 6 & 0 & 0\end{bmatrix}.
$$

Solution: We use the cofactor expansion along the first row:

$$
\begin{aligned}\det (A) & ={a}_{11}{C}_{11}+{a}_{12}{C}_{12}+{a}_{13}{C}_{13}+{a}_{14}{C}_{14} \\  & =(-3)\cdot {C}_{11}+0\cdot {C}_{12}+0\cdot {C}_{13}+5\cdot {C}_{14} \\  & =-3{C}_{11}+5{C}_{14} \\  & =(-3)\cdot \begin{vmatrix}{\color{lightgray}-3} & {\color{lightgray}∗} & {\color{lightgray}∗} & {\color{lightgray}∗} \\ {\color{lightgray}∗} & 0 & 3 & -2 \\ {\color{lightgray}∗} & -1 & 2 & -3 \\ {\color{lightgray}∗} & 6 & 0 & 0\end{vmatrix}+5\cdot \begin{vmatrix}{\color{lightgray}∗} & {\color{lightgray}∗} & {\color{lightgray}∗} & {\color{lightgray}5} \\ 0 & 0 & 3 & {\color{lightgray}∗} \\ 4 & -1 & 2 & {\color{lightgray}∗} \\ -1 & 6 & 0 & {\color{lightgray}∗}\end{vmatrix} \\  & =(-3)(-1)^{1+1}\begin{vmatrix}0 & 3 & -2 \\ -1 & 2 & -3 \\ 6 & 0 & 0\end{vmatrix}+5(-1)^{1+4}\begin{vmatrix}0 & 0 & 3 \\ 4 & -1 & 2 \\ -1 & 6 & 0\end{vmatrix} \\  & =-3\begin{vmatrix}0 & 3 & -2 \\ -1 & 2 & -3 \\ 6 & 0 & 0\end{vmatrix}-5\begin{vmatrix}0 & 0 & 3 \\ 4 & -1 & 2 \\ -1 & 6 & 0\end{vmatrix} \\  & =-3\left(0\cdot \begin{vmatrix}2 & -3 \\ 0 & 0\end{vmatrix}-3\cdot \begin{vmatrix}-1 & -3 \\ 6 & 0\end{vmatrix}-2\cdot \begin{vmatrix}-1 & 2 \\ 6 & 0\end{vmatrix}\right) \\  & -5\left(0\cdot \begin{vmatrix}-1 & 2 \\ 6 & 0\end{vmatrix}-0\cdot \begin{vmatrix}4 & 2 \\ -1 & 0\end{vmatrix}+3\cdot \begin{vmatrix}4 & -1 \\ -1 & 6\end{vmatrix}\right) \\  & =-3\cdot (-3\cdot (0+18)+(-2)\cdot (0-12))-5\cdot (3\cdot (24-1)) \\  & =90-345 \\  & =-255\end{aligned}
$$

Answer selection: -255

Question 17592186266045 — question.difficulty/moderate

Calculate the determinant of the matrix
$$
\displaystyle D=\begin{bmatrix}0 & 0 & 0 & 1 \\ 0 & 4 & 0 & 4 \\ 0 & 1 & 2 & 3 \\ 6 & 5 & 3 & 0\end{bmatrix}.
$$

Solution: We use the cofactor expansion along the first row:

$$
\begin{aligned}\det (D) & ={d}_{11}{C}_{11}+{d}_{12}{C}_{12}+{d}_{13}{C}_{13}+{d}_{14}{C}_{14} \\  & =0\cdot {C}_{11}+0\cdot {C}_{12}+0\cdot {C}_{13}+1\cdot {C}_{14} \\  & =1{C}_{14} \\  & =1\cdot \begin{vmatrix}{\color{lightgray}∗} & {\color{lightgray}∗} & {\color{lightgray}∗} & {\color{lightgray}1} \\ 0 & 4 & 0 & {\color{lightgray}∗} \\ 0 & 1 & 2 & {\color{lightgray}∗} \\ 6 & 5 & 3 & {\color{lightgray}∗}\end{vmatrix} \\  & =1(-1)^{1+4}\begin{vmatrix}0 & 4 & 0 \\ 0 & 1 & 2 \\ 6 & 5 & 3\end{vmatrix} \\  & =-1\left(0\cdot \begin{vmatrix}1 & 2 \\ 5 & 3\end{vmatrix}-4\cdot \begin{vmatrix}0 & 2 \\ 6 & 3\end{vmatrix}+0\cdot \begin{vmatrix}0 & 1 \\ 6 & 5\end{vmatrix}\right) \\  & =-(0-4(3\cdot 0-2\cdot 6)+0) \\  & =-48\end{aligned}
$$

Answer selection: -48
