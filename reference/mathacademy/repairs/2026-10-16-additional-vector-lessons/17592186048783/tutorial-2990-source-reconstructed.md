Given two matrices, it is not always possible to multiply them together. To demonstrate why, consider the following two matrices: $$ A= \begin{bmatrix}1 & 12 \\ 6 & -4\end{bmatrix}, \qquad B= \begin{bmatrix}1 & 3 \\ 2 & -2 \\ 3 & 5\end{bmatrix}. $$

Normally, to compute the product $AB,$ we multiply each row of $A$ by each column of $B.$ However, in this case, each row of $A$ has $\color{blue}2$ entries, while each column of $B$ has $\color{red}3$ entries. The number of entries do not match!

$$ AB = \begin{bmatrix}{\color{blue}1} & {\color{blue}12} \\ 6 & -4\end{bmatrix} \begin{bmatrix}{\color{red}1} & 3 \\ {\color{red}2} & -2 \\ {\color{red}3} & 5\end{bmatrix}. $$

As a result, we cannot compute the dot product, and therefore the product $AB$ is not defined.
