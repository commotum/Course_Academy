# 17592186050825 Multiplying a Matrix by a Column Vector

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186101956 — Introduction

To multiply a matrix by a column vector, we multiply each row in the matrix by the column vector using the dot product.

For example, suppose we would like to multiply the matrix $A$ by the vector $\mathbf{x}$:

$$
\begin{aligned}
A&=
	\begin{bmatrix}1 & 3 \\ 6 & 7\end{bmatrix} \\
\mathbf{x}&=
	\begin{bmatrix}-3 \\ 4\end{bmatrix}
\end{aligned}
$$

First, we write the multiplication as follows:

$$
\underbrace{
	\begin{bmatrix}1 & 3 \\ 6 & 7\end{bmatrix}}_{A}
	\underbrace{
	\begin{bmatrix}-3 \\ 4\end{bmatrix}}_{\mathbf{x}}
	=
	\underbrace{
	\begin{bmatrix}\ast \\ \ast\end{bmatrix}}_{\mathbf{y}}
$$

The result of this multiplication is another column vector $\mathbf{y}$ with the same dimensions as $\mathbf{x}.$

Now, we calculate the entries of the product (shown as $\ast$'s in the equation above).

To find $y_1$, the first component of $\mathbf{y}$, we calculate the dot product of the first row of $A$ and the vector $\mathbf{x}$:

$$
\begin{aligned}
A\mathbf{x} &=\begin{bmatrix}{\color{#4169E1}1} & {\color{#4169E1}3} \\ 6 & 7\end{bmatrix}
\begin{bmatrix}\bbox[lightgray, 2pt]{{\color{black}-3}} \\ \bbox[lightgray, 2pt]{{\color{black}4}}\end{bmatrix} \\
&=\begin{bmatrix}{\color{#4169E1}1}\cdot (\bbox[lightgray, 2pt]{{\color{black}-3}})+{\color{#4169E1}3}\cdot \bbox[lightgray, 2pt]{{\color{black}4}} \\ \ast\end{bmatrix} \\
&=\begin{bmatrix}9 \\ \ast\end{bmatrix}
\end{aligned}
$$

To find $y_2$, the second component of $\mathbf{y}$, we calculate the dot product of the second row of $A$ and the vector $\mathbf{x}$:

$$
\begin{aligned}
A\mathbf{x} &=\begin{bmatrix}1 & 3 \\ {\color{#4169E1}6} & {\color{#4169E1}7}\end{bmatrix}
\begin{bmatrix}\bbox[lightgray, 2pt]{{\color{black}-3}} \\ \bbox[lightgray, 2pt]{{\color{black}4}}\end{bmatrix} \\
&=\begin{bmatrix}9 \\ {\color{#4169E1}6}\cdot (\bbox[lightgray, 2pt]{{\color{black}-3}})+{\color{#4169E1}7}\cdot \bbox[lightgray, 2pt]{{\color{black}4}}\end{bmatrix} \\
&=\begin{bmatrix}9 \\ 10\end{bmatrix}
\end{aligned}
$$

Therefore,

$$
A\mathbf{x}=\begin{bmatrix}9 \\ 10\end{bmatrix}.
$$



### example 17592186100688 — Multiplying a 2x2 Matrix by a Column Vector

Find $A\mathbf{x}$ if 


$$
A=\begin{bmatrix}1 & 3 \\ 7 & -2\end{bmatrix}
$$


and


$$
\mathbf{x}=\begin{bmatrix}2 \\ 5\end{bmatrix}.
$$



We multiply each row in the matrix by the column vector using the dot product. Multiplying the first row, we get

$$
\begin{aligned}\begin{bmatrix}1 & 3 \\ 7 & -2\end{bmatrix}\begin{bmatrix}2 \\ 5\end{bmatrix} & =\begin{bmatrix}1\cdot 2+3\cdot 5 \\ ∗\end{bmatrix}=\begin{bmatrix}17 \\ ∗\end{bmatrix}.\end{aligned}
$$

Multiplying the second row, we get

$$
\begin{aligned}\begin{bmatrix}1 & 3 \\ 7 & -2\end{bmatrix}\begin{bmatrix}2 \\ 5\end{bmatrix} & =\begin{bmatrix}17 \\ 7\cdot 2+(-2)\cdot 5\end{bmatrix}=\begin{bmatrix}17 \\ 4\end{bmatrix}.\end{aligned}
$$

Therefore, 


$$
A\mathbf{x}=\begin{bmatrix}17 \\ 4\end{bmatrix}.
$$



### example 17592186100689 — Multiplying a 3x3 Matrix by a Column Vector

Find $A\mathbf{x}$ if 


$$
A=\begin{bmatrix}-3 & 1 & 1 \\ 2 & 0 & 0 \\ -1 & -2 & 5\end{bmatrix}
$$


and


$$
\mathbf{x}=\begin{bmatrix}1 \\ -2 \\ 0\end{bmatrix}.
$$



We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Ax & =\begin{bmatrix}-3 & 1 & 1 \\ 2 & 0 & 0 \\ -1 & -2 & 5\end{bmatrix}\begin{bmatrix}1 \\ -2 \\ 0\end{bmatrix} \\  & =\begin{bmatrix}(-3)\cdot 1+1\cdot (-2)+1\cdot 0 \\ 2\cdot 1+0\cdot (-2)+0\cdot 0 \\ (-1)\cdot 1+(-2)\cdot (-2)+5\cdot 0\end{bmatrix} \\  & =\begin{bmatrix}-3-2+0 \\ 2+0+0 \\ -1+4+0\end{bmatrix} \\  & =\begin{bmatrix}-5 \\ 2 \\ 3\end{bmatrix}\end{aligned}
$$

### example 17592186100690 — Multiplying a Matrix With Variable Entries by a Column Vector

Find $A\mathbf{x}$ if 


$$
A=\begin{bmatrix}a & c \\ b & d\end{bmatrix}
$$


and


$$
\mathbf{x}=\begin{bmatrix}3 \\ 2\end{bmatrix}.
$$



We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Ax & =\begin{bmatrix}a & c \\ b & d\end{bmatrix}\begin{bmatrix}3 \\ 2\end{bmatrix} \\  & =\begin{bmatrix}a\cdot 3+c\cdot 2 \\ b\cdot 3+d\cdot 2\end{bmatrix} \\  & =\begin{bmatrix}3a+2c \\ 3b+2d\end{bmatrix}\end{aligned}
$$

### tutorial 17592186101957 — Alternative Rule

An alternative, yet equivalent, procedure for multiplying a matrix by a column vector involves adding scaled columns of the matrix $A$ as follows:

$$
\begin{aligned}Ax & =\begin{bmatrix}a & c \\ b & d\end{bmatrix}\begin{bmatrix}{\color{#4169E1}3} \\ {\color{#4169E1}2}\end{bmatrix} \\  & ={\color{#4169E1}3}\begin{bmatrix}a \\ b\end{bmatrix}+{\color{#4169E1}2}\begin{bmatrix}c \\ d\end{bmatrix} \\  & =\begin{bmatrix}3a \\ 3b\end{bmatrix}+\begin{bmatrix}2c \\ 2d\end{bmatrix} \\  & =\begin{bmatrix}3a+2c \\ 3b+2d\end{bmatrix}\end{aligned}
$$

If we denote

$$
\mathbf{u}_1=
	\begin{bmatrix}a \\ b\end{bmatrix},\qquad \mathbf{u}_2=
	\begin{bmatrix}c \\ d\end{bmatrix}
$$

then we can also write the multiplication as follows:

$$
A\mathbf{x}={\color{#4169E1}3}\mathbf{u}_1 + {\color{#4169E1}2} \mathbf{u}_2
$$

The expression above is a **linear combination** of the vectors $\mathbf{u}_1$ and $\mathbf{u}_2$, where the corresponding coefficients are given by the entries of the vector $\mathbf{x}$.



## Representative practice (first three per skill; full bank in practice.json)

### Multiplying a 2x2 Matrix by a Column Vector (29 captured questions)

Question 17592186101136 — question.difficulty/easy

Find $Ax$ if 
$$
\displaystyle A=\begin{bmatrix}-6 & 4 \\ 8 & -5\end{bmatrix}
$$
and
$$
\displaystyle x=\begin{bmatrix}2 \\ 4\end{bmatrix}.
$$

Solution: We multiply each row in the matrix by the column vector using the dot product. Multiplying the first row, we get

$$
\begin{aligned}\begin{bmatrix}-6 & 4 \\ 8 & -5\end{bmatrix}\begin{bmatrix}2 \\ 4\end{bmatrix} & =\begin{bmatrix}(-6)\cdot 2+4\cdot 4 \\ ∗\end{bmatrix}=\begin{bmatrix}4 \\ ∗\end{bmatrix}.\end{aligned}
$$

Multiplying the second row, we get

$$
\begin{aligned}\begin{bmatrix}-6 & 4 \\ 8 & -5\end{bmatrix}\begin{bmatrix}2 \\ 4\end{bmatrix} & =\begin{bmatrix}4 \\ 8\cdot 2+(-5)\cdot 4\end{bmatrix}=\begin{bmatrix}4 \\ -4\end{bmatrix}.\end{aligned}
$$

Therefore, 
$$
\displaystyle Ax=\begin{bmatrix}4 \\ -4\end{bmatrix}.
$$

Answer selection: \begin{bmatrix}4 \\ -4\end{bmatrix}

Question 17592186101137 — None

What is $\begin{bmatrix}3 & 2 \\ 4 & 0\end{bmatrix}\begin{bmatrix}3 \\ 6\end{bmatrix}$?

Solution: 

Question 17592186262621 — question.difficulty/easy

Find $Zx$ if 
$$
\displaystyle Z=\begin{bmatrix}1 & -4 \\ 2 & -7\end{bmatrix}
$$
and
$$
\displaystyle x=\begin{bmatrix}1 \\ -1\end{bmatrix}.
$$

Solution: We multiply each row in the matrix by the column vector using the dot product. Multiplying the first row, we get

$$
\begin{aligned}\begin{bmatrix}1 & -4 \\ 2 & -7\end{bmatrix}\begin{bmatrix}1 \\ -1\end{bmatrix} & =\begin{bmatrix}1\cdot 1+(-4)\cdot (-1) \\ ∗\end{bmatrix}=\begin{bmatrix}5 \\ ∗\end{bmatrix}.\end{aligned}
$$

Multiplying the second row, we get

$$
\begin{aligned}\begin{bmatrix}1 & -4 \\ 2 & -7\end{bmatrix}\begin{bmatrix}1 \\ -1\end{bmatrix} & =\begin{bmatrix}5 \\ 2\cdot 1+(-7)\cdot (-1)\end{bmatrix}=\begin{bmatrix}5 \\ 9\end{bmatrix}.\end{aligned}
$$

Therefore, 
$$
\displaystyle Zx=\begin{bmatrix}5 \\ 9\end{bmatrix}.
$$

Answer selection: \begin{bmatrix}5 \\ 9\end{bmatrix}

### Multiplying a 3x3 Matrix by a Column Vector (31 captured questions)

Question 17592186101134 — None

Find $Ax$ if
$$
\displaystyle A = \begin{bmatrix}3 & -4 & 6 \\ 2 & 6 & -4 \\ 4 & -8 & 3\end{bmatrix}
$$
and
$$
\displaystyle x = \begin{bmatrix}1 \\ 4 \\ 3\end{bmatrix}.
$$

Solution: 

Question 17592186101135 — None

What is $$
\displaystyle \begin{bmatrix}4 & 6 & -5 \\ -2 & 3 & 4 \\ 2 & 5 & -3\end{bmatrix}\begin{bmatrix}2 \\ 1 \\ 4\end{bmatrix}
$$?

Solution: 

Question 17592186262743 — question.difficulty/moderate

$$
\displaystyle \begin{bmatrix}6 & -4 & -6 \\ -2 & 5 & 2 \\ -1 & -4 & 1\end{bmatrix}\begin{bmatrix}2 \\ -1 \\ 2\end{bmatrix}=
$$

Solution: We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}\begin{bmatrix}6 & -4 & -6 \\ -2 & 5 & 2 \\ -1 & -4 & 1\end{bmatrix}\begin{bmatrix}2 \\ -1 \\ 2\end{bmatrix} & =\begin{bmatrix}6\cdot 2+(-4)\cdot (-1)+(-6)\cdot 2 \\ (-2)\cdot 2+5\cdot (-1)+2\cdot 2 \\ (-1)\cdot 2+(-4)\cdot (-1)+1\cdot 2\end{bmatrix} \\  & =\begin{bmatrix}12+4-12 \\ -4-5+4 \\ -2+4+2\end{bmatrix} \\  & =\begin{bmatrix}4 \\ -5 \\ 4\end{bmatrix}\end{aligned}
$$

Answer selection: \begin{bmatrix}4 \\ -5 \\ 4\end{bmatrix}

### Multiplying a Matrix With Variable Entries by a Column Vector (26 captured questions)

Question 17592186101115 — question.difficulty/hard

Find $By$ if 
$$
\displaystyle B=\begin{bmatrix}a & -a & a \\ a & -2b & b \\ 2a & -b & a\end{bmatrix}
$$
and
$$
\displaystyle y=\begin{bmatrix}1 \\ -1 \\ -1\end{bmatrix}.
$$

Solution: We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}By & =\begin{bmatrix}a & -a & a \\ a & -2b & b \\ 2a & -b & a\end{bmatrix}\begin{bmatrix}1 \\ -1 \\ -1\end{bmatrix} \\  & =\begin{bmatrix}a\cdot 1+(-a)\cdot (-1)+a\cdot (-1) \\ a\cdot 1+(-2b)\cdot (-1)+b\cdot (-1) \\ 2a\cdot 1+(-b)\cdot (-1)+a\cdot (-1)\end{bmatrix} \\  & =\begin{bmatrix}a+a-a \\ a+2b-b \\ 2a+b-a\end{bmatrix} \\  & =\begin{bmatrix}a \\ a+b \\ a+b\end{bmatrix}\end{aligned}
$$

Answer selection: \begin{bmatrix}a \\ a+b \\ a+b\end{bmatrix}

Question 17592186101133 — None

Find $Ax$ if
$$
\displaystyle A = \begin{bmatrix}a & c \\ b & d\end{bmatrix}
$$
and
$$
\displaystyle x = \begin{bmatrix}1 \\ 2\end{bmatrix}.
$$

Solution: 

Question 17592186262746 — question.difficulty/moderate

Find $Mz$ if 
$$
\displaystyle M=\begin{bmatrix}s & t \\ -t & s\end{bmatrix}
$$
and
$$
\displaystyle z=\begin{bmatrix}s \\ t\end{bmatrix}.
$$

Solution: We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Mz & =\begin{bmatrix}s & t \\ -t & s\end{bmatrix}\begin{bmatrix}s \\ t\end{bmatrix} \\  & =\begin{bmatrix}s\cdot s+t\cdot t \\ (-t)\cdot s+s\cdot t\end{bmatrix} \\  & =\begin{bmatrix}{s}^{2}+{t}^{2} \\ -st+st\end{bmatrix} \\  & =\begin{bmatrix}{s}^{2}+{t}^{2} \\ 0\end{bmatrix}\end{aligned}
$$

Answer selection: \begin{bmatrix}{s}^{2}+{t}^{2} \\ 0\end{bmatrix}
