# 17592186048297 Multiplying Square Matrices

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186060930 — Introduction

If we want to multiply one square matrix by another (which has the same dimensions), we multiply each row in the first matrix by each column in the second. 

For example, suppose we want to multiply two matrices 
$$
\displaystyle A = \left\lbrack
    \begin{matrix}
        1 & 6  \\
        4 & 3
    \end{matrix}
    \right\rbrack
$$
and
$$
\displaystyle B = \left\lbrack
    \begin{matrix}
        -3 & 0  \\
        2 & -5
    \end{matrix}
    \right\rbrack.
$$

The matrices $A$ and $B$ are both $2 \times 2$ matrices, and their product will be another $2 \times 2$ matrix $C,$ as follows:

$$
\begin{aligned}
	\underbrace{
    \left\lbrack
    \begin{matrix}
        1 & 6  \\
        4 & 3
    \end{matrix}
    \right\rbrack}_{A}

	\underbrace{
    \left\lbrack
    \begin{matrix}
        -3 & 0  \\
        2 & -5
    \end{matrix}
    \right\rbrack}_{B}

	&= 
	\underbrace{
    \left\lbrack
    \begin{matrix}
        \ast & \ast   \\
        \ast & \ast 
    \end{matrix}
    \right\rbrack
	}_{C}
\end{aligned}
$$

Now, we calculate the entries of $C$ (shown as $\ast$'s in the equation above).

To find $c_{11},$ the entry at the intersection of the 1st row and 1st column, we calculate the dot product of the 1st row of $A$ and the 1st column of $B\mathbin{:}$

$$
\begin{aligned}
    \left\lbrack
    \begin{matrix}
        \color{blue}{1} & \color{blue}{6}  \\
        4 & 3
    \end{matrix}
    \right\rbrack

    \left\lbrack
    \begin{matrix}
        \color{red}{-3} & 0  \\
        \color{red}{2} & -5
    \end{matrix}
    \right\rbrack

	&= 
    \left\lbrack
    \begin{matrix}
        {\color{blue}{1}} \cdot ({\color{red}{-3}}) + {\color{blue}{6}} \cdot {\color{red}{2}} & \ast   \\
        \ast & \ast
    \end{matrix}
    \right\rbrack

	= \left\lbrack
    \begin{matrix}
        9 & \ast   \\
        \ast & \ast
    \end{matrix}
    \right\rbrack
\end{aligned}
$$

To find $c_{12},$ the entry at the intersection of the 1st row and 2nd column, we calculate the dot product of the 1st row of $A$ and the 2nd column of $B\mathbin{:}$

$$
\begin{aligned}
    \left\lbrack
    \begin{matrix}
        \color{blue}{1} & \color{blue}{6}  \\
        4 & 3
    \end{matrix}
    \right\rbrack

    \left\lbrack
    \begin{matrix}
        -3 & \color{red}{0}  \\
        2 & \color{red}{-5}
    \end{matrix}
    \right\rbrack

	&= 
    \left\lbrack
    \begin{matrix}
        9 & {\color{blue}{1}} \cdot {\color{red}{0}} + {\color{blue}{6}} \cdot ({\color{red}{-5}})   \\
        \ast & \ast
    \end{matrix}
    \right\rbrack

	= \left\lbrack
    \begin{matrix}
        9 & -30   \\
        \ast & \ast
    \end{matrix}
    \right\rbrack
\end{aligned}
$$

To find $c_{21},$ the entry at the intersection of the 2nd row and 1st column, we calculate the dot product of the 2nd row of $A$ and the 1st column of $B\mathbin{:}$

$$
\begin{aligned}
    \left\lbrack
    \begin{matrix}
        {1} & {6}  \\
        \color{blue}{4} & \color{blue}{3}
    \end{matrix}
    \right\rbrack

    \left\lbrack
    \begin{matrix}
        \color{red}{-3} & 0  \\
        \color{red}{2} & -5
    \end{matrix}
    \right\rbrack

	&= 
    \left\lbrack
    \begin{matrix}
        9 & -30   \\
        {\color{blue}{4}} \cdot ({\color{red}{-3}}) + {\color{blue}{3}} \cdot {\color{red}{2}} & \ast
    \end{matrix}
    \right\rbrack

	= \left\lbrack
    \begin{matrix}
        9 & -30   \\
        -6 & \ast
    \end{matrix}
    \right\rbrack
\end{aligned}
$$

To find $c_{22},$ the entry at the intersection of the 2nd row and 2nd column, we calculate the dot product of the 2nd row of $A$ and the 2nd column of $B\mathbin{:}$

$$
\begin{aligned}
    \left\lbrack
    \begin{matrix}
        {1} & {6}  \\
        \color{blue}{4} & \color{blue}{3}
    \end{matrix}
    \right\rbrack

    \left\lbrack
    \begin{matrix}
        -3 & \color{red}{0}  \\
        2 & \color{red}{-5}
    \end{matrix}
    \right\rbrack

	&= 
    \left\lbrack
    \begin{matrix}
        9 & -30   \\
        -6 & {\color{blue}{4}} \cdot {\color{red}{0}} + {\color{blue}{3}} \cdot ({\color{red}{-5}})
    \end{matrix}
    \right\rbrack

	= \left\lbrack
    \begin{matrix}
        9 & -30   \\
        -6 & -15
    \end{matrix}
    \right\rbrack
\end{aligned}
$$

Therefore, our final answer is

$$
\begin{aligned}
    \left\lbrack
    \begin{matrix}
        {1} & {6}  \\
        4 & 3
    \end{matrix}
    \right\rbrack

    \left\lbrack
    \begin{matrix}
        -3 & 0  \\
        2 & -5
    \end{matrix}
    \right\rbrack

	= \left\lbrack
    \begin{matrix}
        9 & -30   \\
        -6 & -15
    \end{matrix}
    \right\rbrack.
\end{aligned}
$$



### example 17592186059555 — Multiplying 2x2 Square Matrices

Find $AB$ and $BA,$ if 
<div class="matrix-operands matrix-operands-stacked">
<div>$A=\begin{bmatrix}1 & 0 \\ -5 & 1\end{bmatrix}$</div>
</div>
and
<div class="matrix-operands matrix-operands-stacked">
<div>$B=\begin{bmatrix}0 & 1 \\ -1 & 2\end{bmatrix}$</div>
</div>

Multiplying each row in the first matrix by each column in the second, we get

$$
\begin{aligned}AB & =\begin{bmatrix}1 & 0 \\ -5 & 1\end{bmatrix}\begin{bmatrix}0 & 1 \\ -1 & 2\end{bmatrix} \\  & =\begin{bmatrix}1\cdot 0+0\cdot (-1) & 1\cdot 1+0\cdot 2 \\ -5\cdot 0+1\cdot (-1) & -5\cdot 1+1\cdot 2\end{bmatrix} \\  & =\begin{bmatrix}0 & 1 \\ -1 & -3\end{bmatrix}\end{aligned}
$$

and

$$
\begin{aligned}BA & =\begin{bmatrix}0 & 1 \\ -1 & 2\end{bmatrix}\begin{bmatrix}1 & 0 \\ -5 & 1\end{bmatrix} \\  & =\begin{bmatrix}0\cdot 1+1\cdot (-5) & 0\cdot 0+1\cdot 1 \\ -1\cdot 1+2\cdot (-5) & -1\cdot 0+2\cdot 1\end{bmatrix} \\  & =\begin{bmatrix}-5 & 1 \\ -11 & 2\end{bmatrix}.\end{aligned}
$$

**Watch out!** Notice that 

$$
AB \neq BA.
$$

Matrix multiplication is not **commutative**, meaning that when we switch the order of multiplication, we often get a different result (like we did in this example).

### example 17592186059599 — Finding an Entry of the Product of Two Matrices

Let $Z=XY.$ What is the value of $z_{32}$, if

<div class="matrix-operands matrix-operands-stacked">
<div>$X=\begin{bmatrix}1 & 2 & 0 \\ -2 & 0 & -1 \\ 1 & 2 & 3\end{bmatrix}$</div>
<div>$Y=\begin{bmatrix}0 & -1 & -2 \\ 3 & 4 & -1 \\ 1 & -2 & 2\end{bmatrix}$</div>
</div>

Multiplying the $3$rd row in $X$ by the $2$nd column in $Y$, we get

$$
\begin{aligned}{z}_{32} & =\begin{bmatrix}1 & 2 & 3\end{bmatrix}\begin{bmatrix}-1 \\ 4 \\ -2\end{bmatrix} \\  & =1\cdot (-1)+2\cdot 4+3\cdot (-2) \\  & =-1+8-6 \\  & =1.\end{aligned}
$$

### example 17592186059556 — Multiplying 3x3 Square Matrices

Find $AB$, if 
<div class="matrix-operands matrix-operands-stacked">
<div>$A=\begin{bmatrix}-2 & 0 & 3 \\ 3 & -1 & -2 \\ -2 & 0 & -1\end{bmatrix}$</div>
</div>
and
<div class="matrix-operands matrix-operands-stacked">
<div>$B=\begin{bmatrix}0 & 3 & -2 \\ 1 & -2 & 4 \\ -3 & -1 & 2\end{bmatrix}$</div>
</div>

Multiplying each row in the first matrix by each column in the second, we get

$$
\begin{aligned}AB & =\begin{bmatrix}-2 & 0 & 3 \\ 3 & -1 & -2 \\ -2 & 0 & -1\end{bmatrix}\begin{bmatrix}0 & 3 & -2 \\ 1 & -2 & 4 \\ -3 & -1 & 2\end{bmatrix} \\  & =\begin{bmatrix}0+0-9 & -6+0-3 & 4+0+6 \\ 0-1+6 & 9+2+2 & -6-4-4 \\ 0+0+3 & -6+0+1 & 4+0-2\end{bmatrix} \\  & =\begin{bmatrix}-9 & -9 & 10 \\ 5 & 13 & -14 \\ 3 & -5 & 2\end{bmatrix}.\end{aligned}
$$

## Representative practice (first three per skill; full bank in practice.json)

### Multiplying 2x2 Square Matrices (26 captured questions)

Question 17592186059957 — None

What is $\begin{bmatrix}10 & \frac{1}{2} \\ 2 & 0\end{bmatrix}\begin{bmatrix}6 & 0 \\ 4 & 2\end{bmatrix}$?

Solution: 

Question 17592186059960 — None

If
$$
\displaystyle A = \begin{bmatrix}-1 & 0 \\ 0 & -1\end{bmatrix}
$$
and
$$
\displaystyle B = \begin{bmatrix}-4 & 2 \\ 8 & -6\end{bmatrix}
$$
then $AB =$

Solution: 

Question 17592186237930 — question.difficulty/easy

$$
\displaystyle \begin{bmatrix}-18 & 9 \\ 0 & 3\end{bmatrix}\begin{bmatrix}2 & 0 \\ 0 & 1\end{bmatrix}=
$$

Solution: Multiplying each row in the first matrix by each column in the second, we get

$$
\begin{aligned}\begin{bmatrix}-18 & 9 \\ 0 & 3\end{bmatrix}\begin{bmatrix}2 & 0 \\ 0 & 1\end{bmatrix} & =\begin{bmatrix}(-18)\cdot 2+9\cdot 0 & (-18)\cdot 0+9\cdot 1 \\ 0\cdot 2+3\cdot 0 & 0\cdot 0+3\cdot 1\end{bmatrix} \\  & =\begin{bmatrix}-36+0 & 0+9 \\ 0+0 & 0+3\end{bmatrix} \\  & =\begin{bmatrix}-36 & 9 \\ 0 & 3\end{bmatrix}.\end{aligned}
$$

Answer selection: \begin{bmatrix}-36 & 9 \\ 0 & 3\end{bmatrix}

### Finding an Entry of the Product of Two Matrices (29 captured questions)

Question 17592186060283 — None

If $P = AB$, where
$$
\displaystyle A = \begin{bmatrix}4 & -1 & 3 & 0 \\ 11 & 5 & -3 & 4 \\ 2 & -5 & 1 & 0 \\ -1 & 0 & 7 & 12\end{bmatrix}
$$
and
$$
\displaystyle B = \begin{bmatrix}1 & 3 & -5 & 4 \\ -1 & 0 & 3 & 11 \\ 5 & -1 & 2 & 6 \\ 0 & 9 & 8 & 1\end{bmatrix},
$$ then $p_{43} =$

Solution: 

Question 17592186060382 — question.difficulty/easy

Let $C=AB.$ What is the value of ${c}_{21}$, if

$$
A=\begin{bmatrix}3 & 2 \\ 5 & -1\end{bmatrix},\,B=\begin{bmatrix}1 & 2 \\ 3 & 4\end{bmatrix}?
$$

Solution: Multiplying the $2$nd row in $A$ by the $1$st column in $B$, we get

$$
\begin{aligned}{c}_{21} & =\begin{bmatrix}5 & -1\end{bmatrix}\begin{bmatrix}1 \\ 3\end{bmatrix} \\  & =5\cdot 1+(-1)\cdot 3 \\  & =5-3 \\  & =2.\end{aligned}
$$

Answer selection: 2

Question 17592186265720 — question.difficulty/easy

Let $T=UV.$ What is the value of ${t}_{21}$, if

$$
U=\begin{bmatrix}3 & 4 \\ -5 & 3\end{bmatrix},\,V=\begin{bmatrix}-2 & 2 \\ 4 & 3\end{bmatrix}?
$$

Solution: Multiplying the $2$nd row in $U$ by the $1$st column in $V$, we get

$$
\begin{aligned}{t}_{21} & =\begin{bmatrix}-5 & 3\end{bmatrix}\begin{bmatrix}-2 \\ 4\end{bmatrix} \\  & =(-5)\cdot (-2)+3\cdot 4 \\  & =10+12 \\  & =22.\end{aligned}
$$

Answer selection: 22

### Multiplying 3x3 Square Matrices (37 captured questions)

Question 17592186059999 — question.difficulty/moderate

$$
\displaystyle \begin{bmatrix}1 & 0 & 2 \\ 0 & -2 & 2 \\ 1 & 0 & 2\end{bmatrix}\begin{bmatrix}3 & 2 & 3 \\ 0 & 1 & 0 \\ 2 & 1 & 1\end{bmatrix}=
$$

Solution: Multiplying each row in the first matrix by each column in the second, we get

$$
\begin{aligned}\begin{bmatrix}1 & 0 & 2 \\ 0 & -2 & 2 \\ 1 & 0 & 2\end{bmatrix}\begin{bmatrix}3 & 2 & 3 \\ 0 & 1 & 0 \\ 2 & 1 & 1\end{bmatrix} & =\begin{bmatrix}3+0+4 & 2+0+2 & 3+0+2 \\ 0-0+4 & 0-2+2 & 0-0+2 \\ 3+0+4 & 2+0+2 & 3+0+2\end{bmatrix} \\  & =\begin{bmatrix}7 & 4 & 5 \\ 4 & 0 & 2 \\ 7 & 4 & 5\end{bmatrix}.\end{aligned}
$$

Answer selection: \begin{bmatrix}7 & 4 & 5 \\ 4 & 0 & 2 \\ 7 & 4 & 5\end{bmatrix}

Question 17592186060197 — None

Find $XY$, if
$$
\displaystyle X = \begin{bmatrix}1 & 2 & 3 \\ -2 & 3 & -1 \\ 3 & 1 & 2\end{bmatrix}
$$
and
$$
\displaystyle Y = \begin{bmatrix}3 & -2 & 1 \\ 2 & 1 & 3 \\ -1 & 3 & -2\end{bmatrix}.
$$

Solution: 

Question 17592186250463 — question.difficulty/moderate

Find $ST$,  if  $S=\begin{bmatrix}1 & 0 & 4 \\ 0 & -5 & 2 \\ 2 & 0 & 2\end{bmatrix}$ and $T=\begin{bmatrix}3 & 2 & 3 \\ 1 & -1 & 0 \\ 2 & -1 & 1\end{bmatrix}.$

Solution: Multiplying each row in the first matrix by each column in the second, we get

$$
\begin{aligned}ST & =\begin{bmatrix}1 & 0 & 4 \\ 0 & -5 & 2 \\ 2 & 0 & 2\end{bmatrix}\begin{bmatrix}3 & 2 & 3 \\ 1 & -1 & 0 \\ 2 & -1 & 1\end{bmatrix} \\  & =\begin{bmatrix}3+0+8 & 2+0-4 & 3+0+4 \\ 0-5+4 & 0+5-2 & 0-0+2 \\ 6+0+4 & 4-0-2 & 6+0+2\end{bmatrix} \\  & =\begin{bmatrix}11 & -2 & 7 \\ -1 & 3 & 2 \\ 10 & 2 & 8\end{bmatrix}.\end{aligned}
$$

Answer selection: \begin{bmatrix}11 & -2 & 7 \\ -1 & 3 & 2 \\ 10 & 2 & 8\end{bmatrix}
