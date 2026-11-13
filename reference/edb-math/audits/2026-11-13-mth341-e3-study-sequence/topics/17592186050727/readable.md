# 17592186050727 The Transpose of a Matrix

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186060928 — Introduction

To take the **transpose of a matrix**, we interchange each of its columns with the corresponding row. That is, row $1$ becomes column $1,$ row $2$ becomes column $2,$ and so on. A superscript ${}^{T}$ is used to denote the transpose operation.

For example, the transpose of the $2 \times 3$ matrix ${X}$ is the following $3 \times 2$ matrix $X^T\mathbin{:}$

$$
{X} = 
    		\begin{bmatrix}
        		{\color{red}7} & {\color{red}2} & {\color{red}-4}  \\
        		{\color{blue}-3} & {\color{blue}1} & {\color{blue}0}
    		\end{bmatrix}

        \qquad\implies\qquad

	{X}^T = 
    		\begin{bmatrix}
        		{\color{red}7} & {\color{blue}-3}  \\
        		{\color{red}2} & {\color{blue}1}  \\
        		{\color{red}-4} & {\color{blue}0}
    		\end{bmatrix}
$$

The first row of $X$ becomes the first column of $X^T,$ and the second row of $X$ becomes the second column of $X^T.$

Note that transposing a matrix swaps its dimensions. In general, we have the following property:

> *When a matrix is transposed, its dimensions switch from $m \times n$ to $n \times m.$*

Also, notice that the transpose of a column vector is a row vector:

$$
{A} = 
    		\begin{bmatrix}
        		5  \\
        		4  \\
                        2 
    		\end{bmatrix}

       \qquad \implies\qquad

	{A}^T = 
    		\begin{bmatrix}
        		5 & 4 & 2
    		\end{bmatrix}
$$

Similarly, the transpose of a row vector is a column vector:

$$
{B} = 
    		\begin{bmatrix}
        		8 & -10 & 0 & 6
    		\end{bmatrix}

        \qquad\implies\qquad

	{B}^T = 
    		\begin{bmatrix}
        		8  \\
                        -10  \\
                        0  \\
                        6
    		\end{bmatrix}
$$



### example 17592186059552 — Finding the Transpose of a Matrix

Find $C^T,$ if 

<div class="matrix-operands matrix-operands-stacked">
<div>$C =\begin{bmatrix}-1 & 1 \\ 0 & 2 \\ -2 & -3\end{bmatrix}$</div>
</div>

To find the transpose, we interchange the rows and columns:


$$
C^T =
	\begin{bmatrix}-1 & 0 & -2 \\ 1 & 2 & -3\end{bmatrix}
$$

### example 17592186059553 — Finding the Transpose of a Row Vector or Column Vector

If
    

$$
{A} = 
    \begin{bmatrix}
        5 & -1 & 0  \end{bmatrix},
$$

then what is ${A^T} ?$

To find the transpose, we interchange the rows and columns. 

Here, there is just a single row, so it becomes a single column:

$$
{A}^T = 
    		\begin{bmatrix}
    5  \\
    -1  \\
    0  \end{bmatrix}
$$

### example 17592186059554 — Determining the Dimensions of the Transpose of a Matrix

Consider the matrix
    

$$
{B} = 
    \begin{bmatrix}
        1 & 2 & 4 & 2 \\
        4 & 4 & 1 & 1 \\
        3 & -3 & 0 & -1
    \end{bmatrix}.
$$

What are the dimensions of ${B}^T?$

When a matrix is transposed, its dimensions switch from $N \times M$ to $M \times N.$

So, since $B$ is a $3 \times 4$ matrix, the transpose ${B}^T$ is a $4\times3$ matrix.

### tutorial 17592186060929 — Properties of the Transpose of a Matrix

Remember that transposing a matrix swaps the rows and columns. So, if $B=A^T,$ then $b_{ij}=a_{ji}$ for all values of $i$ and $j.$ 

Geometrically, when a matrix is transposed, the diagonal elements (those with $i=j$) remain the same while all other elements are reflected across the diagonal.  For example,

$$
{A} = 
    		\begin{bmatrix}
        		\color{red}{3} & \color{blue}{7}  \\
        		1 & \color{red}{6}
    		\end{bmatrix}

      \qquad  \implies\qquad

	{A}^T = 
    		\begin{bmatrix}
        		\color{red}{3} & 1  \\
        		\color{blue}{7} & \color{red}{6} 
    		\end{bmatrix}.
$$

Also,  transposing a matrix twice results in the original matrix. More precisely, for any matrix $A,$ we have

$$
\left( A^T\right)^T = A.
$$

This happens because, in the first transpose, we swap the rows of $A$ for the columns, and then in the second transpose, we swap them back again. For example,

$$
{A} = 
    		\begin{bmatrix}
        		\color{red}{3} & \color{blue}{7}  \\
        		1 & \color{red}{6}
    		\end{bmatrix}

      \quad  \implies\quad

	{A}^T = 
    		\begin{bmatrix}
        		\color{red}{3} & 1  \\
        		\color{blue}{7} & \color{red}{6} 
    		\end{bmatrix}

      \quad  \implies\quad

	\left( {A}^T\right)^T = 
    		\begin{bmatrix}
        		\color{red}{3} & \color{blue}{7}  \\
        		1 & \color{red}{6} 
    		\end{bmatrix} =A.
$$

Finally, for any numbers $c_1,c_2$ and any $m \times n$ matrices $A,B$ we have the following rule:

$$
(c_1 A \pm c_2 B)^T = c_1 A^T \pm c_2 B^T
$$



## Representative practice (first three per skill; full bank in practice.json)

### Finding the Transpose of a Matrix (34 captured questions)

Question 17592186059967 — question.difficulty/easy

If
    

<div class="matrix-operands matrix-operands-stacked">
<div>$Y=\begin{bmatrix}-2 & 9 & 7 \\ 1 & 6 & 0 \\ -8 & 2 & 1\end{bmatrix}$</div>
</div>

then ${Y}^{T}=$

Solution: To find the transpose, we interchange the rows and columns:

$$
{Y}^{T}=\begin{bmatrix}-2 & 1 & -8 \\ 9 & 6 & 2 \\ 7 & 0 & 1\end{bmatrix}
$$

Answer selection: \begin{bmatrix}-2 & 1 & -8 \\ 9 & 6 & 2 \\ 7 & 0 & 1\end{bmatrix}

Question 17592186059993 — None

Find $A^{T}$, given that

<div class="matrix-operands matrix-operands-stacked">
<div>$A =\begin{bmatrix}5 & 4 \\ 3 & 2\end{bmatrix}$</div>
</div>

.

Solution: To find the transpose, we interchange the rows and columns.

$$
A^T=\begin{bmatrix}5 & 3 \\ 4 & 2\end{bmatrix}
$$

Answer selection: \begin{bmatrix}5 & 3 \\ 4 & 2\end{bmatrix}

Question 17592186240846 — question.difficulty/easy

Find ${Y}^{T}$, given that 
    

<div class="matrix-operands matrix-operands-stacked">
<div>$Y=\begin{bmatrix}-20 & 0 & 15 \\ 9 & 6 & 0.5\end{bmatrix}$</div>
</div>

Solution: To find the transpose, we interchange the rows and columns:

$$
{Y}^{T}=\begin{bmatrix}-20 & 9 \\ 0 & 6 \\ 15 & 0.5\end{bmatrix}
$$

Answer selection: \begin{bmatrix}-20 & 9 \\ 0 & 6 \\ 15 & 0.5\end{bmatrix}

### Finding the Transpose of a Row Vector or Column Vector (37 captured questions)

Question 17592186059966 — question.difficulty/easy

Find ${Z}^{T}$ given that 

<div class="matrix-operands matrix-operands-stacked">
<div>$Z=\begin{bmatrix}-4 & 4 & 5 & 1\end{bmatrix}$</div>
</div>

Solution: To find the transpose, we interchange the rows and columns. 

Here, there is just a single row, so it becomes a single column:

$$
{Z}^{T}=\begin{bmatrix}-4 \\ 4 \\ 5 \\ 1\end{bmatrix}
$$

Answer selection: \begin{bmatrix}-4 \\ 4 \\ 5 \\ 1\end{bmatrix}

Question 17592186059968 — None

If

<div class="matrix-operands matrix-operands-stacked">
<div>$G =\begin{bmatrix}-4 \\ 15 \\ -1 \\ 8\end{bmatrix}$</div>
</div>

,
then $G^{T} =$

Solution: To find the transpose, we interchange the rows and columns.

$$
G^T=\begin{bmatrix}-4 & 15 & -1 & 8\end{bmatrix}
$$

Answer selection: \begin{bmatrix}-4 & 15 & -1 & 8\end{bmatrix}

Question 17592186250296 — question.difficulty/easy

Find ${F}^{T}$ given that 
    

<div class="matrix-operands matrix-operands-stacked">
<div>$F=\begin{bmatrix}3 \\ 3 \\ 2 \\ 1\end{bmatrix}$</div>
</div>

Solution: To find the transpose, we interchange the rows and columns. 

Here, there is just a single column, so it becomes a single row:

$$
{F}^{T}=\begin{bmatrix}3 & 3 & 2 & 1\end{bmatrix}
$$

Answer selection: \begin{bmatrix}3 & 3 & 2 & 1\end{bmatrix}

### Determining the Dimensions of the Transpose of a Matrix (36 captured questions)

Question 17592186059994 — None

Consider the matrix

<div class="matrix-operands matrix-operands-stacked">
<div>$B =\begin{bmatrix}2 & 3 \\ 2 & 3 \\ 3 & 2\end{bmatrix}$</div>
</div>

.
What are the dimensions of $B^{T}$?

Solution: The original matrix has $3$ rows and $2$ columns. Transposing interchanges them, so its transpose has dimensions $2\times 3$.

Answer selection: 2 \cdot 3

Question 17592186059996 — None

Consider the matrix

<div class="matrix-operands matrix-operands-stacked">
<div>$C =\begin{bmatrix}5 & 3 \\ 4 & 3 \\ 3 & -2 \\ 4 & 1\end{bmatrix}$</div>
</div>

.
What are the dimensions of $C^{T}$?

Solution: The original matrix has $4$ rows and $2$ columns. Transposing interchanges them, so its transpose has dimensions $2\times 4$.

Answer selection: 2 \cdot 4

Question 17592186250292 — question.difficulty/easy

Consider the matrix
    

<div class="matrix-operands matrix-operands-stacked">
<div>$C=\begin{bmatrix}1 & 3 \\ 2 & 4\end{bmatrix}$</div>
</div>

What are the dimensions of ${C}^{T}?$

Solution: When a matrix is transposed, its dimensions switch from $m\times n$ to $n\times m.$

So, since $C$ is a $2\times 2$ matrix, the transpose ${C}^{T}$ is a $2\times 2$ matrix too.

Answer selection: 2\times 2
