# 17592186049875 Further Properties of Determinants

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186121022 — Introduction

In this topic, we will consider a few more properties of determinants. Let's start with the following important property. 

*The determinant of the product of two square matrices is equal to the product of the determinants.*

Symbolically, if $M$ and $N$ are both square matrices, then

$$
\det  ( M \cdot  N ) = \det  ( M ) \cdot  \det  ( N ) .
$$

For instance, suppose that we want to find the determinant of the matrix $A$ that is defined as follows:
$$
A = 
	{\left[ \begin{array}{ccc}1 & 0 & 0 \\ - 2 & - 3 & 0 \\ 2 & 0 & 2\end{array} \right]}
	{\left[ \begin{array}{ccc}3 & - 10 & \sqrt{2} \\ 0 & 5 & 2 \sqrt{3} \\ 0 & 0 & - 1\end{array} \right]}
$$

To easily compute $\det(A)$, we first compute the determinants of the two matrices and then multiply the results. Also, notice that both matrices in our product are triangular, so their determinants are given by the product of the diagonal entries:

$$
\begin{aligned}\det(A) & =\det\begin{bmatrix}1 & 0 & 0 \\ -2 & -3 & 0 \\ 2 & 0 & 2\end{bmatrix}\cdot \det\begin{bmatrix}3 & -10 & \sqrt{2} \\ 0 & 5 & 2\sqrt{3} \\ 0 & 0 & -1\end{bmatrix} \\  & =\underbrace{\begin{vmatrix}{\color{red}{1}} & {\color{blue}{0}} & {\color{blue}{0}} \\ -2 & {\color{red}{-3}} & {\color{blue}{0}} \\ 2 & 0 & {\color{red}{2}}\end{vmatrix}}_{\text{lower triangular}}\cdot \underbrace{\begin{vmatrix}{\color{red}{3}} & -10 & \sqrt{2} \\ {\color{blue}{0}} & {\color{red}{5}} & 2\sqrt{3} \\ {\color{blue}{0}} & {\color{blue}{0}} & {\color{red}{-1}}\end{vmatrix}}_{\text{upper triangular}} \\  & =({\color{red}{1}}\cdot ({\color{red}{-3}})\cdot {\color{red}{2}})\cdot ({\color{red}{3}}\cdot {\color{red}{5}}\cdot ({\color{red}{-1}})) \\  & =(-6)\cdot (-15) \\  & =90\end{aligned}
$$



### example 17592186119592 — Calculating the Determinant of a Product

Given that $$
\displaystyle A=	{\left[ \begin{array}{ccc}1 & 2 & 11 \\ 0 & - \sqrt{3} & 3 \\ 0 & 0 & 3 \sqrt{3}\end{array} \right]}
	{\left[ \begin{array}{ccc}- 2 & 1 & - \sqrt{11} \\ 0 & 5 & - 1 \\ 0 & 4 & - 1\end{array} \right]},
$$ find $\det(A).$

Given two $n\times n$ matrices $M$ and $N,$ we have

$$
\det  ( M N ) = \det  ( M ) \cdot  \det  ( N ) .
$$

In our case, this gives

$$
\begin{array}{cc}\det  ( A ) &  = \det  \left[ \begin{array}{ccc}1 & 2 & 11 \\ 0 & - \sqrt{3} & 3 \\ 0 & 0 & 3 \sqrt{3}\end{array} \right] \cdot  \det  \left[ \begin{array}{ccc}- 2 & 1 & - \sqrt{11} \\ 0 & 5 & - 1 \\ 0 & 4 & - 1\end{array} \right] .\end{array}
$$

We can compute the required determinants as follows:

- For the first determinant, we notice that it's upper triangular. Therefore, the determinant is simply the product of the diagonal entries.

- For the second determinant, we can compute it using a Laplace expansion down the $1$st column.

Therefore, we obtain 

$$
\begin{array}{cc}\det  ( A ) &  = \left| \begin{array}{ccc}{\color{red}1} & 2 & 11 \\ 0 & {\color{red}- \sqrt{3}} & 3 \\ 0 & 0 & {\color{red}3 \sqrt{3}}\end{array} \right| \cdot  \left| \begin{array}{ccc}{\color{blue}- 2} & 1 & - \sqrt{11} \\ {\color{blue}0} & 5 & - 1 \\ {\color{blue}0} & 4 & - 1\end{array} \right| \\  &  = ( {\color{red}1} \cdot  ( {\color{red}- \sqrt{3}} ) \cdot  {\color{red}3 \sqrt{3}} ) \cdot  ( - 2 \left( - 1 {)}^{1 + 1} \left| \begin{array}{cc}5 & - 1 \\ 4 & - 1\end{array} \right| \right) \\  &  = ( - 9 ) \cdot  ( ( - 2 ) \cdot  ( - 5 + 4 ) ) \\  &  = ( - 9 ) \cdot  2 \\  &  = - 18.\end{array}
$$

### tutorial 17592186121023 — The Determinant of an Inverse Matrix

Another useful property of determinants is that, for any invertible matrix $A,$ we have

$$
\det(A^{-1}) = \dfrac{1}{\det(A)}.
$$

To understand why the above property is true, remember that $A \cdot A^{-1} = I$ for any invertible matrix $A.$ So, we have

$$
\begin{aligned}A\cdot {A}^{-1} & =I \\ \det (A\cdot {A}^{-1}) & =\det (I) \\ \det (A)\cdot \det ({A}^{-1}) & =1 \\ \det ({A}^{-1}) & =\frac{1}{\det (A)}.\end{aligned}
$$

**Important:** We can only apply the formula $\det(A^{-1}) = \dfrac{1}{\det(A)}$ if $A$ is invertible, meaning that $\det(A) \neq 0.$



### example 17592186119593 — Calculating the Determinant of the Inverse of a Matrix

Find $|A^{-1}|,$ if  $A=	{\left[ \begin{array}{ccc}2 & 14 & - 1 \\ 7 & - 6 & - 6 \\ 0 & - 3 & 0\end{array} \right]}.$

Given an invertible $n\times n$ matrix $A,$ we have

$$
|A^{-1}| = \dfrac{1}{|A|}.
$$

First, we find $|A|$ using a Laplace expansion across the $3$rd row:

$$
\begin{aligned}|A| & =\begin{vmatrix}2 & 14 & -1 \\ 7 & -6 & -6 \\ {\color{blue}{0}} & {\color{blue}{-3}} & {\color{blue}{0}}\end{vmatrix} \\  & =-3(-1)^{3+2}\begin{vmatrix}2 & -1 \\ 7 & -6\end{vmatrix} \\  & =3\cdot (-12+7) \\  & =-15\end{aligned}
$$

 

Therefore, we obtain 

$$
\det(A^{-1}) =  \dfrac{1}{|A|} = -\dfrac{1}{15}.
$$

### tutorial 17592186121024 — The Linearity of the Determinant

One final important property of the determinant is that it is **linear in each row and column**. For rows, for example, this means 

$$
\begin{aligned} & \det\begin{bmatrix}⋮ & ⋮ & … & ⋮ \\ {{\color{red}{◻}}}_{1}+{{\color{blue}{△}}}_{1} & {{\color{red}{◻}}}_{2}+{{\color{blue}{△}}}_{2} & … & {{\color{red}{◻}}}_{n}+{{\color{blue}{△}}}_{n} \\ ⋮ & ⋮ & … & ⋮\end{bmatrix} \\  & \hspace{2em}\hspace{2em}=\det\begin{bmatrix}⋮ & ⋮ & … & ⋮ \\ {{\color{red}{◻}}}_{1} & {{\color{red}{◻}}}_{2} & … & {{\color{red}{◻}}}_{n} \\ ⋮ & ⋮ & … & ⋮\end{bmatrix}+\det\begin{bmatrix}⋮ & ⋮ & … & ⋮ \\ {{\color{blue}{△}}}_{1} & {{\color{blue}{△}}}_{2} & … & {{\color{blue}{△}}}_{n} \\ ⋮ & ⋮ & … & ⋮\end{bmatrix}.\end{aligned}
$$

For instance, it's easy to check that

$$
\begin{aligned}\overbrace{\det \begin{bmatrix}1 & 2 \\ 3 & 4\end{bmatrix}}^{-2} & =\det \begin{bmatrix}1 & 2 \\ {\color{red}{0}}+{\color{blue}{3}} & {\color{red}{4}}+{\color{blue}{0}}\end{bmatrix} \\  & =\underbrace{\det \begin{bmatrix}1 & 2 \\ {\color{red}{0}} & {\color{red}{4}}\end{bmatrix}}_{4}+\underbrace{\det \begin{bmatrix}1 & 2 \\ {\color{blue}{3}} & {\color{blue}{0}}\end{bmatrix}}_{-6}.\end{aligned}
$$

Note that this property also holds for columns:

$$
\begin{aligned}\det \begin{bmatrix}⋯ & {{\color{red}{◻}}}_{1}+{{\color{blue}{△}}}_{1} & ⋯ \\ ⋯ & {{\color{red}{◻}}}_{2}+{{\color{blue}{△}}}_{2} & ⋯ \\ ⋮ & ⋮ & ⋮ \\ ⋯ & {{\color{red}{◻}}}_{n}+{{\color{blue}{△}}}_{n} & ⋯\end{bmatrix}=\det \begin{bmatrix}⋯ & {{\color{red}{◻}}}_{1} & ⋯ \\ ⋯ & {{\color{red}{◻}}}_{2} & ⋯ \\ ⋮ & ⋮ & ⋮ \\ ⋯ & {{\color{red}{◻}}}_{n} & ⋯\end{bmatrix}+\det \begin{bmatrix}⋯ & {{\color{blue}{△}}}_{1} & ⋯ \\ ⋯ & {{\color{blue}{△}}}_{2} & ⋯ \\ ⋮ & ⋮ & ⋮ \\ ⋯ & {{\color{blue}{△}}}_{n} & ⋯\end{bmatrix}\end{aligned}
$$

For example, we have that

$$
\begin{aligned}\overbrace{\det \begin{bmatrix}1 & 2 \\ 3 & 4\end{bmatrix}}^{-2} & =\det \begin{bmatrix}{\color{red}{1}}+{\color{blue}{0}} & 2 \\ {\color{red}{0}}+{\color{blue}{3}} & 4\end{bmatrix} \\  & =\underbrace{\det \begin{bmatrix}{\color{red}{1}} & 2 \\ {\color{red}{0}} & 4\end{bmatrix}}_{4}+\underbrace{\det \begin{bmatrix}{\color{blue}{0}} & 2 \\ {\color{blue}{3}} & 4\end{bmatrix}}_{-6}.\end{aligned}
$$



### example 17592186119594 — Calculating a Determinant Using the Linearity of the Determinant

Given that 
$$
{\left| \begin{array}{ccc}a & b & c \\ 1 & 2 & 3 \\ 1 & 1 & 2\end{array} \right|}
	= -10,
$$
find 
$$
{\left| \begin{array}{ccc}a & b & c + 1 \\ 1 & 2 & 3 \\ 1 & 1 & 2\end{array} \right|}.
$$

We "factor out" the given determinant from the determinant we would like to find:

$$
\begin{aligned}\begin{vmatrix}a & b & c+1 \\ 1 & 2 & 3 \\ 1 & 1 & 2\end{vmatrix} & =\begin{vmatrix}{\color{red}{a}}+{\color{blue}{0}} & {\color{red}{b}}+{\color{blue}{0}} & {\color{red}{c}}+{\color{blue}{1}} \\ 1 & 2 & 3 \\ 1 & 1 & 2\end{vmatrix}\end{aligned}
$$

Now, using the linearity property of determinants and expanding the second determinant across the $1$st row, we obtain

$$
\begin{aligned}\begin{vmatrix}{\color{red}{a}}+{\color{blue}{0}} & {\color{red}{b}}+{\color{blue}{0}} & {\color{red}{c}}+{\color{blue}{1}} \\ 1 & 2 & 3 \\ 1 & 1 & 2\end{vmatrix} & =\underbrace{\begin{vmatrix}{\color{red}{a}} & {\color{red}{b}} & {\color{red}{c}} \\ 1 & 2 & 3 \\ 1 & 1 & 2\end{vmatrix}}_{-10}+\begin{vmatrix}{\color{blue}{0}} & {\color{blue}{0}} & {\color{blue}{1}} \\ 1 & 2 & 3 \\ 1 & 1 & 2\end{vmatrix} \\  & =-10+1(-1)^{1+3}\begin{vmatrix}1 & 2 \\ 1 & 1\end{vmatrix} \\  & =-10-1 \\  & =-11.\end{aligned}
$$

## Representative practice (first three per skill; full bank in practice.json)

### Calculating the Determinant of a Product (16 captured questions)

Question 17592186120449 — question.difficulty/moderate

Given that $$
\displaystyle A=\begin{bmatrix}5 & 0 & 0 \\ -1 & -1 & 0 \\ 10 & 3 & 2\end{bmatrix}\begin{bmatrix}3 & 9 & 0 \\ 0 & 2 & 1 \\ 0 & 0 & -2\end{bmatrix},
$$ find $\det (A).$

Solution: Given two $n\times n$ matrices $M$ and $N,$ we have

$$
\det (MN)=\det (M)\cdot \det (N).
$$

In our case, this gives

$$
\det (A)=\det \begin{bmatrix}5 & 0 & 0 \\ -1 & -1 & 0 \\ 10 & 3 & 2\end{bmatrix}\cdot \det \begin{bmatrix}3 & 9 & 0 \\ 0 & 2 & 1 \\ 0 & 0 & -2\end{bmatrix}.
$$

Notice that both matrices are triangular. Therefore, we obtain

$$
\begin{aligned}\det (A) & =(5\cdot (-1)\cdot 2)\cdot (3\cdot 2\cdot (-2)) \\  & =(-10)\cdot (-12) \\  & =120.\end{aligned}
$$

Answer selection: 120

Question 17592186120450 — None

Given that $$
\displaystyle A = \begin{bmatrix}\sqrt{3} & -4 \\ -1 & 5\sqrt{3}\end{bmatrix}\begin{bmatrix}7 & 2 \\ 5 & 3\end{bmatrix},
$$ find $\det (A)$.

Solution: The determinant of a product equals the product of the determinants:

$$
\begin{aligned}\det(A)&=\begin{vmatrix}\sqrt3&-4\\-1&5\sqrt3\end{vmatrix}\begin{vmatrix}7&2\\5&3\end{vmatrix}\\&=(15-4)(21-10)\\&=11\cdot11\\&=121.\end{aligned}
$$

Answer selection: 121

Question 17592186265916 — question.difficulty/moderate

Given that $$
\displaystyle Q=\begin{bmatrix}4 & 0 & 0 \\ 7 & 5 & 0 \\ -4 & 9 & -1\end{bmatrix}\begin{bmatrix}3 & 5 & 6 \\ 0 & -2 & -8 \\ 0 & 0 & 2\end{bmatrix},
$$ find $\det (Q).$

Solution: Given two $n\times n$ matrices $M$ and $N,$ we have

$$
\det (MN)=\det (M)\cdot \det (N).
$$

In our case, this gives

$$
\det (Q)=\det \begin{bmatrix}4 & 0 & 0 \\ 7 & 5 & 0 \\ -4 & 9 & -1\end{bmatrix}\cdot \det \begin{bmatrix}3 & 5 & 6 \\ 0 & -2 & -8 \\ 0 & 0 & 2\end{bmatrix}.
$$

Notice that both matrices are triangular. Therefore, we obtain

$$
\begin{aligned}\det (Q) & =(4\cdot 5\cdot (-1))\cdot (3\cdot (-2)\cdot 2) \\  & =(-20)\cdot (-12) \\  & =240.\end{aligned}
$$

Answer selection: 240

### Calculating the Determinant of the Inverse of a Matrix (17 captured questions)

Question 17592186120436 — question.difficulty/hard

Find $|{A}^{-1}|,$ if $A=\begin{bmatrix}-5 & -1 & 4 \\ 4 & 1 & -2 \\ -6 & -2 & 3\end{bmatrix}.$

Solution: Given an invertible $n\times n$ matrix $A,$ we have

$$
|{A}^{-1}|=\frac{1}{|A|}.
$$

First, we find $|A|$ using a Laplace expansion across the $2$nd column:

$$
\begin{aligned}|A| & =\begin{vmatrix}-5 & -1 & 4 \\ 4 & 1 & -2 \\ -6 & -2 & 3\end{vmatrix} \\  & =-1(-1)^{1+2}\begin{vmatrix}4 & -2 \\ -6 & 3\end{vmatrix}+1(-1)^{2+2}\begin{vmatrix}-5 & 4 \\ -6 & 3\end{vmatrix}-2(-1)^{3+2}\begin{vmatrix}-5 & 4 \\ 4 & -2\end{vmatrix} \\  & =(12-12)+(-15+24)+2(10-16) \\  & =0+9-12 \\  & =-3\end{aligned}
$$

Therefore, we obtain 

$$
|{A}^{-1}|=\frac{1}{|A|}=-\frac{1}{3}.
$$

Answer selection: -\frac{1}{3}

Question 17592186120451 — question.difficulty/easy

Find $\det ({A}^{-1}),$ if $A=\begin{bmatrix}2 & -1 \\ 3 & 6\end{bmatrix}.$

Solution: Given an invertible $n\times n$ matrix $A,$ we have

$$
\det ({A}^{-1})=\frac{1}{\det (A)}.
$$

First, we find $\det (A):$

$$
\begin{aligned}\det (A) & =\det \begin{bmatrix}2 & -1 \\ 3 & 6\end{bmatrix} \\  & =12+3 \\  & =15\end{aligned}
$$

Therefore, we obtain 

$$
\det ({A}^{-1})=\frac{1}{\det (A)}=\frac{1}{15}.
$$

Answer selection: \frac{1}{15}

Question 17592186265928 — question.difficulty/hard

Find $|{A}^{-1}|,$ if $A=\begin{bmatrix}3 & 2 & 5 \\ -4 & 1 & -2 \\ 1 & -1 & 3\end{bmatrix}.$

Solution: Given an invertible $n\times n$ matrix $A,$ we have

$$
|{A}^{-1}|=\frac{1}{|A|}.
$$

First, we find $|A|$ using a Laplace expansion across the $2$nd column:

$$
\begin{aligned}|A| & =\begin{vmatrix}3 & 2 & 5 \\ -4 & 1 & -2 \\ 1 & -1 & 3\end{vmatrix} \\  & =2(-1)^{1+2}\begin{vmatrix}-4 & -2 \\ 1 & 3\end{vmatrix}+1(-1)^{2+2}\begin{vmatrix}3 & 5 \\ 1 & 3\end{vmatrix}+(-1)(-1)^{3+2}\begin{vmatrix}3 & 5 \\ -4 & -2\end{vmatrix} \\  & =-2(-12+2)+(9-5)+(-6+20) \\  & =20+4+14 \\  & =38\end{aligned}
$$

Therefore, we obtain 

$$
|{A}^{-1}|=\frac{1}{|A|}=\frac{1}{38}.
$$

Answer selection: \frac{1}{38}

### Calculating a Determinant Using the Linearity of the Determinant (15 captured questions)

Question 17592186120435 — question.difficulty/moderate

Given that 
$$
\displaystyle \begin{vmatrix}a+3 & -5 \\ b & 6\end{vmatrix}=-7,
$$
find 
$$
\displaystyle \begin{vmatrix}a+2 & -5 \\ b+4 & 6\end{vmatrix}.
$$

Solution: We "factor out" the given determinant from the determinant we would like to find:

$$
\begin{aligned}\begin{vmatrix}a+2 & -5 \\ b+4 & 6\end{vmatrix} & =\begin{vmatrix}{\color{red}{(a+3)}}-{\color{blue}{1}} & -5 \\ {\color{red}{b}}+{\color{blue}{4}} & 6\end{vmatrix}\end{aligned}
$$

Now, using the linearity property of determinants, we obtain

$$
\begin{aligned}\begin{vmatrix}{\color{red}{(a+3)}}-{\color{blue}{1}} & -5 \\ {\color{red}{b}}+{\color{blue}{4}} & 6\end{vmatrix} & =\underbrace{\begin{vmatrix}{\color{red}{a+3}} & -5 \\ {\color{red}{b}} & 6\end{vmatrix}}_{-7}+\begin{vmatrix}-{\color{blue}{1}} & -5 \\ {\color{blue}{4}} & 6\end{vmatrix} \\  & =-7+(-6+20) \\  & =7.\end{aligned}
$$

Answer selection: 7

Question 17592186120457 — question.difficulty/hard

$$
\displaystyle \begin{vmatrix}107 & 215 & 99 \\ 6 & 8 & 11 \\ 107 & 215 & 100\end{vmatrix}=
$$

Solution: First, notice that the $1$st row of our determinant is almost equal to the $3$rd row. So, we can rewrite the given determinant, as follows:

$$
\begin{aligned}\begin{vmatrix}107 & 215 & 99 \\ 6 & 8 & 11 \\ 107 & 215 & 100\end{vmatrix} & =\begin{vmatrix}{\color{red}{107}} & {\color{red}{215}} & {\color{red}{99}} \\ 6 & 8 & 11 \\ {\color{red}{107}}+{\color{blue}{0}} & {\color{red}{215}}+{\color{blue}{0}} & {\color{red}{99}}+{\color{blue}{1}}\end{vmatrix}\end{aligned}
$$

Next, using the linearity property of determinants, we obtain

$$
\begin{aligned}\begin{vmatrix}{\color{red}{107}} & {\color{red}{215}} & {\color{red}{99}} \\ 6 & 8 & 11 \\ {\color{red}{107}}+{\color{blue}{0}} & {\color{red}{215}}+{\color{blue}{0}} & {\color{red}{99}}+{\color{blue}{1}}\end{vmatrix} & =\begin{vmatrix}{\color{red}{107}} & {\color{red}{215}} & {\color{red}{99}} \\ 6 & 8 & 11 \\ {\color{red}{107}} & {\color{red}{215}} & {\color{red}{99}}\end{vmatrix}+\begin{vmatrix}107 & 215 & 99 \\ 6 & 8 & 11 \\ {\color{blue}{0}} & {\color{blue}{0}} & {\color{blue}{1}}\end{vmatrix}.\end{aligned}
$$

The first determinant must be zero since it has two identical rows, while the second determinant can be expanded across the $3$rd row, as follows:

$$
\begin{aligned}\begin{vmatrix}{\color{red}{107}} & {\color{red}{215}} & {\color{red}{99}} \\ 6 & 8 & 11 \\ {\color{red}{107}} & {\color{red}{215}} & {\color{red}{99}}\end{vmatrix}+\begin{vmatrix}107 & 215 & 99 \\ 6 & 8 & 11 \\ {\color{blue}{0}} & {\color{blue}{0}} & {\color{blue}{1}}\end{vmatrix} & =0+1(-1)^{3+3}\begin{vmatrix}107 & 215 \\ 6 & 8\end{vmatrix} \\  & =107\cdot 8-215\cdot 6 \\  & =-434\end{aligned}
$$

Answer selection: -434

Question 17592186265950 — question.difficulty/hard

$$
\displaystyle \begin{vmatrix}160 & 184 & 76 \\ 3 & 4 & -8 \\ 160 & 184 & 78\end{vmatrix}=
$$

Solution: First, notice that the $1$st row of our determinant is almost equal to the $3$rd row. So, we can rewrite the given determinant, as follows:

$$
\begin{aligned}\begin{vmatrix}160 & 184 & 76 \\ 3 & 4 & -8 \\ 160 & 184 & 78\end{vmatrix} & =\begin{vmatrix}{\color{red}{160}} & {\color{red}{184}} & {\color{red}{76}} \\ 3 & 4 & -8 \\ {\color{red}{160}}+{\color{blue}{0}} & {\color{red}{184}}+{\color{blue}{0}} & {\color{red}{76}}+{\color{blue}{2}}\end{vmatrix}\end{aligned}
$$

Next, using the linearity property of determinants, we obtain

$$
\begin{aligned}\begin{vmatrix}{\color{red}{160}} & {\color{red}{184}} & {\color{red}{76}} \\ 3 & 4 & -8 \\ {\color{red}{160}}+{\color{blue}{0}} & {\color{red}{184}}+{\color{blue}{0}} & {\color{red}{76}}+{\color{blue}{2}}\end{vmatrix} & =\begin{vmatrix}{\color{red}{160}} & {\color{red}{184}} & {\color{red}{76}} \\ 3 & 4 & -8 \\ {\color{red}{160}} & {\color{red}{184}} & {\color{red}{76}}\end{vmatrix}+\begin{vmatrix}160 & 184 & 76 \\ 3 & 4 & -8 \\ {\color{blue}{0}} & {\color{blue}{0}} & {\color{blue}{2}}\end{vmatrix}.\end{aligned}
$$

The first determinant must be zero since it has two identical rows, while the second determinant can be expanded across the $3$rd row, as follows:

$$
\begin{aligned}\begin{vmatrix}{\color{red}{160}} & {\color{red}{184}} & {\color{red}{76}} \\ 3 & 4 & -8 \\ {\color{red}{160}} & {\color{red}{184}} & {\color{red}{76}}\end{vmatrix}+\begin{vmatrix}160 & 184 & 76 \\ 3 & 4 & -8 \\ {\color{blue}{0}} & {\color{blue}{0}} & {\color{blue}{2}}\end{vmatrix} & =0+2(-1)^{3+3}\begin{vmatrix}160 & 184 \\ 3 & 4\end{vmatrix} \\  & =2\cdot (160\cdot 4-184\cdot 3) \\  & =2\cdot 88 \\  & =176\end{aligned}
$$

Answer selection: 176
