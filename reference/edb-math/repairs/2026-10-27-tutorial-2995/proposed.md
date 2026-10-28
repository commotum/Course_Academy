Remember that the **identity matrix** $I_n$ is an $n \times n$ square matrix with $1$'s on the diagonal, and where all other elements are $0.$ For example, the $3 \times 3$ identity matrix $I_3$ is given below:

$$
I_3 = 
			\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix}
$$

The identity matrix gets its name from the fact that whenever we multiply a matrix by the corresponding identity matrix, the matrix remains unchanged.

For example, let's consider the matrix

<div class="matrix-operands matrix-operands-stacked">
<div>$A=\begin{bmatrix}-2 & 3 & 10 \\ 6 & -2 & 2 \\ 23 & 4 & 8\end{bmatrix}$</div>
</div>

Multiplying the matrix $A$ by the identity matrix $I_3,$ we find that the result is just $A$ itself:

$$
\begin{aligned}A\cdot {I}_{3} & =\begin{bmatrix}-2 & 3 & 10 \\ 6 & -2 & 2 \\ 23 & 4 & 8\end{bmatrix}\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}(-2)\cdot 1+3\cdot 0+10\cdot 0 & (-2)\cdot 0+3\cdot 1+10\cdot 0 & (-2)\cdot 0+3\cdot 0+10\cdot 1 \\ 6\cdot 1+(-2)\cdot 0+2\cdot 0 & 6\cdot 0+(-2)\cdot 1+2\cdot 0 & 6\cdot 0+(-2)\cdot 0+2\cdot 1 \\ 23\cdot 1+4\cdot 0+8\cdot 0 & 23\cdot 0+4\cdot 1+8\cdot 0 & 23\cdot 0+4\cdot 0+8\cdot 1\end{bmatrix} \\  & =\begin{bmatrix}-2 & 3 & 10 \\ 6 & -2 & 2 \\ 23 & 4 & 8\end{bmatrix} \\  & =A\end{aligned}
$$

Therefore, $A \cdot I_3 = A.$ You can check that $I_3 \cdot A = A$ using the same method.

This result holds in general: 

> For *any* square $n \times n$ matrix $A,$ we have
> 
> 
> $$
> A \cdot I_n = I_n \cdot A = A.
> $$

In other words, the $n \times n$ identity matrix $I_n$ has a similar property to the number $1,$ namely that 

$$
a\cdot 1 = 1\cdot a = a
$$

 for any real number $a.$