# 17592186048505 Finding Determinants Using Laplace Expansions

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186121018 — Introduction

Sometimes there are lots of calculations involved in finding the determinant of a matrix using a cofactor expansion across the first row. 

Fortunately, however, we don't always have to use the first row! We can use *any* row we like. A cofactor expansion across any general row is known as a **Laplace expansion**.

Across the row $i,$ the Laplace expansion of an $n\!\times\! n$ matrix $A$ is given by the formula

$$\begin{aligned}\det(A) & ={\sum }_{j=1}^{n}{\color{red}{a}_{ij}}{\color{black}{C}_{ij}} \\  & ={\color{red}{a}_{i1}}{\color{black}{C}_{i1}}+{\color{red}{a}_{i2}}{\color{black}{C}_{i2}}+⋯+{\color{red}{a}_{in}}{\color{black}{C}_{in}},\end{aligned}$$

where ${\color{blue}C_{ij}}$ is the cofactor of the entry $\color{red}a_{ij}$ in $A.$ Remember the cofactor of the entry $\color{red}a_{ij}$ is 

$${\color{black}C_{ij}}=(-1)^{i+j}{\color{black}M_{ij}},$$

where ${\color{black}M_{ij}}$ is the minor of the entry.

For example, consider the following matrix:

<div class="matrix-operands matrix-operands-stacked">
<div>$B=\begin{bmatrix}-1 & 2 & 1 & 1 \\ 0 & -1 & 1 & 1 \\ 0 & 2 & 0 & 0 \\ 0 & 1 & 0 & -3\end{bmatrix}$</div>
</div>

To compute the determinant of the matrix above, it is most convenient to use a Laplace expansion along the row with the most zeros. So, let's use Laplace expansion across the third row ($i=3$) as follows:

$$
{\begin{array}{rl}\displaystyle \det \left[ \begin{array}{cccc}-1 & 2 & 1 & 1 \\ 0 & -1 & 1 & 1 \\ {\color{red}0} & {\color{red}2} & {\color{red}0} & {\color{red}0} \\ 0 & 1 & 0 & -3\end{array} \right] & \displaystyle  = \sum _{j = 1}^{n} {\color{red}{a}_{3 j}} {\color{black}{C}_{3 j}} \\ \displaystyle  & \displaystyle  = {\color{red}0} \cdot  {\color{black}{C}_{31}} + {\color{red}2} \cdot  {\color{blue}{C}_{32}} + {\color{red}0} \cdot  {\color{black}{C}_{33}} + {\color{red}0} \cdot  {\color{black}{C}_{34}} \\ \displaystyle  & \displaystyle  = {\color{red}2} \cdot  {\color{blue}( - 1 {)}^{3 + 2}} \cdot  {\color{blue}\enclose{left right}{\begin{array}{ccc}\displaystyle - 1 & \displaystyle 1 & \displaystyle 1 \\ \displaystyle 0 & \displaystyle 1 & \displaystyle 1 \\ \displaystyle 0 & \displaystyle 0 & \displaystyle - 3\end{array}}} \\ \displaystyle  & \displaystyle  = - 2 \cdot  \enclose{left right}{\begin{array}{ccc}\displaystyle - 1 & \displaystyle 1 & \displaystyle 1 \\ \displaystyle 0 & \displaystyle 1 & \displaystyle 1 \\ \displaystyle 0 & \displaystyle 0 & \displaystyle - 3\end{array}}\end{array}}
$$

So, we reduced a $4 \times 4$ determinant to a $3 \times 3$ determinant.



### example 17592186119657 — Applying a Laplace Expansion Across a Row

Using a cofactor expansion along the $4$th row, write the following determinant as a combination of $3 \times 3$ determinants:

$$
\left|
	{\begin{array}{cccc}10 & 2 & - 2 & - 1 \\ 1 & - 2 & 7 & 9 \\ - 2 & 1 & - 2 & 3 \\ - 6 & 0 & 0 & 1\end{array}}
\right|.
$$

Using a Laplace expansion along the $4$th row, we have

$$\begin{aligned}\begin{vmatrix}10 & 2 & -2 & -1 \\ 1 & -2 & 7 & 9 \\ -2 & 1 & -2 & 3 \\ -6 & 0 & 0 & 1\end{vmatrix} & ={\color{red}(-6)}\cdot {\color{blue}{C}_{41}}+{\color{red}0}\cdot {\color{black}{C}_{42}}+{\color{red}0}\cdot {\color{black}{C}_{43}}+{\color{red}1}\cdot {\color{blue}{C}_{44}} \\  & ={\color{red}(-6)}\cdot {\color{blue}(-1)^{4+1}\cdot \begin{vmatrix}2 & -2 & -1 \\ -2 & 7 & 9 \\ 1 & -2 & 3\end{vmatrix}}+{\color{red}1}\cdot {\color{blue}(-1)^{4+4}\cdot \begin{vmatrix}10 & 2 & -2 \\ 1 & -2 & 7 \\ -2 & 1 & -2\end{vmatrix}} \\  & =6\cdot \begin{vmatrix}2 & -2 & -1 \\ -2 & 7 & 9 \\ 1 & -2 & 3\end{vmatrix}+\begin{vmatrix}10 & 2 & -2 \\ 1 & -2 & 7 \\ -2 & 1 & -2\end{vmatrix}.\end{aligned}$$

Therefore,

$$
\left|
	{\begin{array}{cccc}10 & 2 & - 2 & - 1 \\ 1 & - 2 & 7 & 9 \\ - 2 & 1 & - 2 & 3 \\ - 6 & 0 & 0 & 1\end{array}}
\right| 
=
	6 \cdot
	\left|
	{\begin{array}{ccc}2 & - 2 & - 1 \\ - 2 & 7 & 9 \\ 1 & - 2 & 3\end{array}}
	\right|
	+
	\left|
	{\begin{array}{ccc}10 & 2 & - 2 \\ 1 & - 2 & 7 \\ - 2 & 1 & - 2\end{array}}
	\right|.
$$

### example 17592186119587 — Calculating a Determinant Using a Laplace Expansion Across a Row

Calculate
$$
\left|
	{\begin{array}{cccc}1 & - 1 & 0 & 2 \\ 0 & 1 & - 4 & 2 \\ 0 & - 2 & 3 & 1 \\ 0 & 0 & 0 & - 1\end{array}}
\right|.
$$

The $4$th row of the matrix contains three zeros, more than any other row. So using a Laplace expansion along the $4$th row, we have

$$\begin{aligned}\begin{vmatrix}1 & -1 & 0 & 2 \\ 0 & 1 & -4 & 2 \\ 0 & -2 & 3 & 1 \\ {\color{red}0} & {\color{red}0} & {\color{red}0} & {\color{red}-1}\end{vmatrix} & ={\color{red}0}\cdot {\color{black}{C}_{41}}+{\color{red}0}\cdot {\color{black}{C}_{42}}+{\color{red}0}\cdot {\color{black}{C}_{43}}+{\color{red}(-1)}\cdot {\color{blue}{C}_{44}} \\  & ={\color{red}(-1)}\cdot {\color{blue}(-1)^{4+4}\cdot \begin{vmatrix}1 & -1 & 0 \\ 0 & 1 & -4 \\ 0 & -2 & 3\end{vmatrix}} \\  & =-\begin{vmatrix}1 & -1 & 0 \\ 0 & 1 & -4 \\ 0 & -2 & 3\end{vmatrix}.\end{aligned}$$

Now, computing the $3 \times 3$ determinant by applying a Laplace expansion along the $1$st row, we obtain:

$$
\begin{aligned}\begin{vmatrix}1 & -1 & 0 \\ 0 & 1 & -4 \\ 0 & -2 & 3\end{vmatrix} & =1\cdot \begin{vmatrix}1 & -4 \\ -2 & 3\end{vmatrix}-(-1)\cdot \begin{vmatrix}0 & -4 \\ 0 & 3\end{vmatrix}+0\cdot \begin{vmatrix}0 & 1 \\ 0 & -2\end{vmatrix} \\  & =\begin{vmatrix}1 & -4 \\ -2 & 3\end{vmatrix}+\begin{vmatrix}0 & -4 \\ 0 & 3\end{vmatrix} \\  & =(3-8)+(0-0) \\  & =-5\end{aligned}
$$

Therefore,

$$
\left|
	{\begin{array}{cccc}1 & -1 & 0 & 2 \\ 0 & 1 & -4 & 2 \\ 0 & -2 & 3 & 1 \\ 0 & 0 & 0 & -1\end{array}}
\right|
= - (-5) = 5.
$$

### tutorial 17592186121019 — Laplace Expansion Across a Column

We can also use the Laplace expansion across any *column* to find the determinant. Across the column $j,$ the Laplace expansion is given by the formula

$$\begin{aligned}\det(A) & ={\sum }_{i=1}^{n}{\color{red}{a}_{ij}}{\color{blue}{C}_{ij}} \\  & ={\color{red}{a}_{1j}}{\color{blue}{C}_{1j}}+{\color{red}{a}_{2j}}{\color{blue}{C}_{2j}}+⋯+{\color{red}{a}_{nj}}{\color{blue}{C}_{nj}},\end{aligned}$$

where $\color{blue}C_{ij}$ is the cofactor of the entry ${\color{red}a_{ij}}.$

In other words, the Laplace expansion across a row or column is the sum of the entries in the row or column multiplied by their respective cofactors.

To find the determinant of a matrix, we can choose to use the Laplace expansion across any row or column, so choose the row or column that has the most zeros, to cut down on the calculations!



### example 17592186119588 — Calculating a Determinant Using a Laplace Expansion Across a Column

Using a cofactor expansion along the $2$nd column, write the following determinant as a combination of $3 \times 3$ determinants:

$$
\left|
	{\begin{array}{cccc}1 & 0 & - 3 & - 2 \\ 2 & 3 & - 1 & 5 \\ 1 & 0 & 8 & 9 \\ 2 & 0 & 3 & - 1\end{array}}
\right|.
$$

Using a Laplace expansion along the $2$nd column, we have

$$\begin{aligned}\begin{vmatrix}1 & {\color{red}0} & -3 & -2 \\ 2 & {\color{red}3} & -1 & 5 \\ 1 & {\color{red}0} & 8 & 9 \\ 2 & {\color{red}0} & 3 & -1\end{vmatrix} & ={\color{red}0}\cdot {\color{black}{C}_{12}}+{\color{red}3}\cdot {\color{blue}{C}_{22}}+{\color{red}0}\cdot {\color{black}{C}_{32}}+{\color{red}0}\cdot {\color{black}{C}_{42}} \\  & ={\color{red}3}\cdot {\color{blue}(-1)^{2+2}\cdot \begin{vmatrix}1 & -3 & -2 \\ 1 & 8 & 9 \\ 2 & 3 & -1\end{vmatrix}} \\  & =3\cdot \begin{vmatrix}1 & -3 & -2 \\ 1 & 8 & 9 \\ 2 & 3 & -1\end{vmatrix}.\end{aligned}$$

Therefore,

$$
\left|
	{\begin{array}{cccc}1 & 0 & -3 & -2 \\ 2 & 3 & -1 & 5 \\ 1 & 0 & 8 & 9 \\ 2 & 0 & 3 & -1\end{array}}
\right|
=
	3 \cdot
	\left|
	{\begin{array}{ccc}1 & - 3 & - 2 \\ 1 & 8 & 9 \\ 2 & 3 & - 1\end{array}}
	\right|
$$

## Representative practice (first three per skill; full bank in practice.json)

### Applying a Laplace Expansion Across a Row (13 captured questions)

Question 17592186120402 — None

What is $\begin{vmatrix}3 & 2 & -1 & 2 \\ 5 & 0 & 0 & 0 \\ 4 & 1 & -2 & 3 \\ -7 & 1 & -1 & 1\end{vmatrix}$?

Solution: Let $A$ denote the given matrix. Expand along the second row. Terms with a zero entry vanish. The cofactor signs are $(-1)^{i+j}$.

$$
\det(A)=5(-1)^{2+1}\begin{vmatrix}2 & -1 & 2 \\ 1 & -2 & 3 \\ 1 & -1 & 1\end{vmatrix}.
$$

Evaluating the smaller determinants gives

$$
\det(A)=-10.
$$

Answer selection: -5 \cdot\begin{vmatrix}2 & -1 & 2 \\ 1 & -2 & 3 \\ 1 & -1 & 1\end{vmatrix}

Question 17592186120403 — question.difficulty/moderate

$$
\displaystyle \begin{vmatrix}3 & 1 & 2 & -3 \\ 3 & 6 & -4 & 1 \\ 0 & -5 & -5 & 0 \\ -1 & 1 & 5 & 2\end{vmatrix}=
$$

Solution: The $3$rd row of the matrix contains two zeros, more than any other row. So using a Laplace expansion along the $3$rd row, we have

$$\begin{aligned}\begin{vmatrix}3 & 1 & 2 & -3 \\ 3 & 6 & -4 & 1 \\ {\color{red}0} & {\color{red}-5} & {\color{red}-5} & {\color{red}0} \\ -1 & 1 & 5 & 2\end{vmatrix} & ={\color{red}0}\cdot {\color{black}{C}_{31}}+{\color{red}(-5)}\cdot {\color{blue}{C}_{32}}+{\color{red}(-5)}\cdot {\color{blue}{C}_{33}}+{\color{red}0}\cdot {\color{black}{C}_{34}} \\  & ={\color{red}(-5)}\cdot {\color{blue}(-1)^{3+2}\begin{vmatrix}3 & 2 & -3 \\ 3 & -4 & 1 \\ -1 & 5 & 2\end{vmatrix}}+{\color{red}(-5)}\cdot {\color{blue}(-1)^{3+3}\cdot \begin{vmatrix}3 & 1 & -3 \\ 3 & 6 & 1 \\ -1 & 1 & 2\end{vmatrix}} \\  & =5\cdot \begin{vmatrix}3 & 2 & -3 \\ 3 & -4 & 1 \\ -1 & 5 & 2\end{vmatrix}-5\cdot \begin{vmatrix}3 & 1 & -3 \\ 3 & 6 & 1 \\ -1 & 1 & 2\end{vmatrix}.\end{aligned}$$

Answer selection: 5\cdot \begin{vmatrix}3 & 2 & -3 \\ 3 & -4 & 1 \\ -1 & 5 & 2\end{vmatrix}-5\cdot \begin{vmatrix}3 & 1 & -3 \\ 3 & 6 & 1 \\ -1 & 1 & 2\end{vmatrix}

Question 17592186265802 — question.difficulty/moderate

$$
\displaystyle \begin{vmatrix}2 & 1 & -1 & 0 \\ 1 & 3 & -3 & 1 \\ 1 & -1 & 2 & 3 \\ 0 & -2 & 1 & 0\end{vmatrix}=
$$

Solution: The $4$th row of the matrix contains two zeros, more than any other row. So using a Laplace expansion along the $4$th row, we have

$$\begin{aligned}\begin{vmatrix}2 & 1 & -1 & 0 \\ 1 & 3 & -3 & 1 \\ 1 & -1 & 2 & 3 \\ {\color{red}0} & {\color{red}-2} & {\color{red}1} & {\color{red}0}\end{vmatrix} & ={\color{red}0}\cdot {\color{black}{C}_{41}}+{\color{red}(-2)}\cdot {\color{blue}{C}_{42}}+{\color{red}1}\cdot {\color{blue}{C}_{43}}+{\color{red}0}\cdot {\color{black}{C}_{44}} \\  & ={\color{red}(-2)}\cdot {\color{blue}(-1)^{4+2}\cdot \begin{vmatrix}2 & -1 & 0 \\ 1 & -3 & 1 \\ 1 & 2 & 3\end{vmatrix}}+{\color{red}1}\cdot {\color{blue}(-1)^{4+3}\cdot \begin{vmatrix}2 & 1 & 0 \\ 1 & 3 & 1 \\ 1 & -1 & 3\end{vmatrix}} \\  & =-2\cdot \begin{vmatrix}2 & -1 & 0 \\ 1 & -3 & 1 \\ 1 & 2 & 3\end{vmatrix}-\begin{vmatrix}2 & 1 & 0 \\ 1 & 3 & 1 \\ 1 & -1 & 3\end{vmatrix}\end{aligned}$$

Answer selection: -2\cdot \begin{vmatrix}2 & -1 & 0 \\ 1 & -3 & 1 \\ 1 & 2 & 3\end{vmatrix}-\begin{vmatrix}2 & 1 & 0 \\ 1 & 3 & 1 \\ 1 & -1 & 3\end{vmatrix}

### Calculating a Determinant Using a Laplace Expansion Across a Row (16 captured questions)

Question 17592186120424 — question.difficulty/hard

Calculate
$$
\displaystyle \begin{vmatrix}1 & 2 & 1 & -1 \\ 0 & -4 & -2 & 1 \\ 2 & 0 & 0 & 1 \\ -3 & 1 & 2 & 0\end{vmatrix}.
$$

Solution: The $3$rd row of the matrix contains two zeros, more than any other row. So using a Laplace expansion along the $3$rd row, we have

$$\begin{aligned}\begin{vmatrix}1 & 2 & 1 & -1 \\ 0 & -4 & -2 & 1 \\ {\color{red}2} & {\color{red}0} & {\color{red}0} & {\color{red}1} \\ -3 & 1 & 2 & 0\end{vmatrix} & ={\color{red}2}\cdot {\color{blue}{C}_{31}}+{\color{red}0}\cdot {\color{black}{C}_{32}}+{\color{red}0}\cdot {\color{black}{C}_{33}}+{\color{red}1}\cdot {\color{blue}{C}_{34}} \\  & ={\color{red}2}\cdot {\color{blue}(-1)^{3+1}\cdot \begin{vmatrix}2 & 1 & -1 \\ -4 & -2 & 1 \\ 1 & 2 & 0\end{vmatrix}}+{\color{red}1}\cdot {\color{blue}(-1)^{3+4}\cdot \begin{vmatrix}1 & 2 & 1 \\ 0 & -4 & -2 \\ -3 & 1 & 2\end{vmatrix}} \\  & =2\begin{vmatrix}2 & 1 & -1 \\ -4 & -2 & 1 \\ 1 & 2 & 0\end{vmatrix}-\begin{vmatrix}1 & 2 & 1 \\ 0 & -4 & -2 \\ -3 & 1 & 2\end{vmatrix}.\end{aligned}$$

Now, computing the first $3\times 3$ determinant by applying a Laplace expansion along the $3$rd row, we obtain:

$$\begin{aligned}\begin{vmatrix}2 & 1 & -1 \\ -4 & -2 & 1 \\ {\color{red}1} & {\color{red}2} & {\color{red}0}\end{vmatrix} & ={\color{red}1}\cdot {\color{blue}{C}_{31}}+{\color{red}2}\cdot {\color{blue}{C}_{32}}+{\color{red}0}\cdot {\color{black}{C}_{33}} \\  & ={\color{red}1}\cdot {\color{blue}(-1)^{3+1}\cdot \begin{vmatrix}1 & -1 \\ -2 & 1\end{vmatrix}}+{\color{red}2}\cdot {\color{blue}(-1)^{3+2}\cdot \begin{vmatrix}2 & -1 \\ -4 & 1\end{vmatrix}} \\  & =\begin{vmatrix}1 & -1 \\ -2 & 1\end{vmatrix}-2\begin{vmatrix}2 & -1 \\ -4 & 1\end{vmatrix} \\  & =(1-2)-2(2-4) \\  & =-1+4 \\  & =3\end{aligned}$$

Now, computing the second $3\times 3$ determinant by applying a Laplace expansion along the $2$nd row, we obtain:

$$\begin{aligned}\begin{vmatrix}1 & 2 & 1 \\ {\color{red}0} & {\color{red}-4} & {\color{red}-2} \\ -3 & 1 & 2\end{vmatrix} & ={\color{red}0}\cdot {\color{black}{C}_{21}}+{\color{red}(-4)}\cdot {\color{blue}{C}_{22}}+{\color{red}(-2)}\cdot {\color{blue}{C}_{23}} \\  & ={\color{red}(-4)}\cdot {\color{blue}(-1)^{2+2}\cdot \begin{vmatrix}1 & 1 \\ -3 & 2\end{vmatrix}}+{\color{red}(-2)}\cdot {\color{blue}(-1)^{2+3}\cdot \begin{vmatrix}1 & 2 \\ -3 & 1\end{vmatrix}} \\  & =-4\begin{vmatrix}1 & 1 \\ -3 & 2\end{vmatrix}+2\begin{vmatrix}1 & 2 \\ -3 & 1\end{vmatrix} \\  & =-4(2+3)+2(1+6) \\  & =-20+14 \\  & =-6\end{aligned}$$

Therefore,

$$
\begin{vmatrix}1 & 2 & 1 & -1 \\ 0 & -4 & -2 & 1 \\ 2 & 0 & 0 & 1 \\ -3 & 1 & 2 & 0\end{vmatrix}=2\cdot 3-(-6)=12.
$$

Answer selection: 12

Question 17592186120425 — None

Compute the following determinant using a cofactor expansion along the $2$nd row:
$$
\displaystyle \begin{vmatrix}0 & 0 & 2 & 2 \\ 0 & 1 & 0 & 0 \\ 1 & 0 & 1 & -1 \\ 2 & 1 & 0 & 0\end{vmatrix}.
$$

Solution: Let $A$ denote the given matrix. Expand along the second row. Terms with a zero entry vanish. The cofactor signs are $(-1)^{i+j}$.

$$
\det(A)=1(-1)^{2+2}\begin{vmatrix}0 & 2 & 2 \\ 1 & 1 & -1 \\ 2 & 0 & 0\end{vmatrix}.
$$

Evaluating the smaller determinants gives

$$
\det(A)=-8.
$$

Answer selection: -8

Question 17592186338749 — question.difficulty/moderate

Compute the following determinant using a cofactor expansion along the $1$st row:

$$
\begin{vmatrix}0 & 0 & 3 & 0 \\ 1 & 2 & 1 & -1 \\ 0 & 1 & 2 & 0 \\ 2 & -1 & 0 & 3\end{vmatrix}.
$$

Solution: Using cofactor expansion along the $1$st row, we have

$$\begin{aligned}\begin{vmatrix}{\color{red}0} & {\color{red}0} & {\color{red}3} & {\color{red}0} \\ 1 & 2 & 1 & -1 \\ 0 & 1 & 2 & 0 \\ 2 & -1 & 0 & 3\end{vmatrix} & ={\color{red}0}\cdot {\color{black}{C}_{11}}+{\color{red}0}\cdot {\color{black}{C}_{12}}+{\color{red}3}\cdot {\color{blue}{C}_{13}}+{\color{red}0}\cdot {\color{black}{C}_{14}} \\  & ={\color{red}3}\cdot {\color{blue}(-1)^{1+3}\cdot \begin{vmatrix}1 & 2 & -1 \\ 0 & 1 & 0 \\ 2 & -1 & 3\end{vmatrix}} \\  & =3\begin{vmatrix}1 & 2 & -1 \\ 0 & 1 & 0 \\ 2 & -1 & 3\end{vmatrix}.\end{aligned}$$

Now, computing the $3\times 3$ determinant by applying a Laplace expansion along the $2$nd row, we obtain:

$$\begin{aligned}\begin{vmatrix}1 & 2 & -1 \\ 0 & 1 & 0 \\ 2 & -1 & 3\end{vmatrix} & ={\color{red}0}\cdot {\color{black}{C}_{21}}+{\color{red}1}\cdot {\color{blue}{C}_{22}}+{\color{red}0}\cdot {\color{black}{C}_{23}} \\  & ={\color{red}1}\cdot {\color{blue}(-1)^{2+2}\cdot \begin{vmatrix}1 & -1 \\ 2 & 3\end{vmatrix}} \\  & =\begin{vmatrix}1 & -1 \\ 2 & 3\end{vmatrix} \\  & =3+2 \\  & =5\end{aligned}$$

Therefore,

$$
\begin{vmatrix}0 & 0 & 3 & 0 \\ 1 & 2 & 1 & -1 \\ 0 & 1 & 2 & 0 \\ 2 & -1 & 0 & 3\end{vmatrix}=3\cdot 5=15.
$$

Answer selection: 15

### Calculating a Determinant Using a Laplace Expansion Across a Column (17 captured questions)

Question 17592186120404 — None

What is $\begin{vmatrix}2 & 1 & 0 & -3 \\ 2 & -2 & -5 & 4 \\ 1 & 6 & 0 & -2 \\ -1 & 1 & 1 & 2\end{vmatrix}$?

Solution: Let $A$ denote the given matrix. Expand along the third column. Terms with a zero entry vanish. The cofactor signs are $(-1)^{i+j}$.

$$
\det(A)=-5(-1)^{2+3}\begin{vmatrix}2 & 1 & -3 \\ 1 & 6 & -2 \\ -1 & 1 & 2\end{vmatrix}+1(-1)^{4+3}\begin{vmatrix}2 & 1 & -3 \\ 2 & -2 & 4 \\ 1 & 6 & -2\end{vmatrix}.
$$

Evaluating the smaller determinants gives

$$
\det(A)=109.
$$

Answer selection: 5 \cdot\begin{vmatrix}2 & 1 & -3 \\ 1 & 6 & -2 \\ -1 & 1 & 2\end{vmatrix}-\begin{vmatrix}2 & 1 & -3 \\ 2 & -2 & 4 \\ 1 & 6 & -2\end{vmatrix}

Question 17592186120423 — question.difficulty/moderate

$$
\displaystyle \begin{vmatrix}1 & 0 & -3 & 1 \\ 1 & 0 & 1 & 9 \\ -4 & 0 & 2 & -1 \\ -5 & 2 & 4 & 2\end{vmatrix}=
$$

Solution: Using a cofactor expansion along the $2$nd column, we have

$$\begin{aligned}\begin{vmatrix}1 & {\color{red}0} & -3 & 1 \\ 1 & {\color{red}0} & 1 & 9 \\ -4 & {\color{red}0} & 2 & -1 \\ -5 & {\color{red}2} & 4 & 2\end{vmatrix} & ={\color{red}0}\cdot {\color{black}{C}_{12}}+{\color{red}0}\cdot {\color{black}{C}_{22}}+{\color{red}0}\cdot {\color{black}{C}_{32}}+{\color{red}2}\cdot {\color{blue}{C}_{42}} \\  & ={\color{red}2}\cdot {\color{blue}(-1)^{4+2}\cdot \begin{vmatrix}1 & -3 & 1 \\ 1 & 1 & 9 \\ -4 & 2 & -1\end{vmatrix}} \\  & =2\cdot \begin{vmatrix}1 & -3 & 1 \\ 1 & 1 & 9 \\ -4 & 2 & -1\end{vmatrix}.\end{aligned}$$

Answer selection: 2\cdot \begin{vmatrix}1 & -3 & 1 \\ 1 & 1 & 9 \\ -4 & 2 & -1\end{vmatrix}

Question 17592186265821 — question.difficulty/moderate

$$
\displaystyle \begin{vmatrix}0 & 3 & 1 & 5 \\ -7 & 2 & -4 & 1 \\ 0 & 7 & 2 & -3 \\ 0 & 2 & -3 & -1\end{vmatrix}=
$$

Solution: Using a cofactor expansion along the $1$st column, we have

$$\begin{aligned}\begin{vmatrix}{\color{red}0} & 3 & 1 & 5 \\ {\color{red}-7} & 2 & -4 & 1 \\ {\color{red}0} & 7 & 2 & -3 \\ {\color{red}0} & 2 & -3 & -1\end{vmatrix} & ={\color{red}0}\cdot {\color{black}{C}_{11}}+{\color{red}-7}\cdot {\color{blue}{C}_{21}}+{\color{red}0}\cdot {\color{black}{C}_{31}}+{\color{red}0}\cdot {\color{black}{C}_{41}} \\  & ={\color{red}(-7)}\cdot {\color{blue}(-1)^{2+1}\cdot \begin{vmatrix}3 & 1 & 5 \\ 7 & 2 & -3 \\ 2 & -3 & -1\end{vmatrix}} \\  & =7\cdot \begin{vmatrix}3 & 1 & 5 \\ 7 & 2 & -3 \\ 2 & -3 & -1\end{vmatrix}.\end{aligned}$$

Answer selection: 7\cdot \begin{vmatrix}3 & 1 & 5 \\ 7 & 2 & -3 \\ 2 & -3 & -1\end{vmatrix}
