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
