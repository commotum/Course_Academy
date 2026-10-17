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
