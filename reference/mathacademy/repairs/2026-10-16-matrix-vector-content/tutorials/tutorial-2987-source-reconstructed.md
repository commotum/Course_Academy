To multiply a matrix by a column vector, we multiply each row in the matrix by the column vector using the dot product.

For example, suppose we would like to multiply $A= \begin{bmatrix}1 & 3 \\ 6 & 7\end{bmatrix}$ and $\mathbf{x}= \begin{bmatrix}-3 \\ 4\end{bmatrix}.$

First, we write the multiplication as follows:

$$ \underbrace{ \begin{bmatrix}1 & 3 \\ 6 & 7\end{bmatrix}}_{A} \underbrace{ \begin{bmatrix}-3 \\ 4\end{bmatrix}}_{\mathbf{x}} = \underbrace{ \begin{bmatrix}∗ \\ ∗\end{bmatrix}}_{\mathbf{y}} $$

The result of the multiplication is another column vector $\mathbf{y}$ with the same dimensions as $\mathbf{x}$. Now, we calculate the entries of the product (shown as $\ast$'s in the equation above).

To find $y_1,$ the $1$st component of $\mathbf{y}$, we calculate the dot product of the $1$st row of $A$ and the vector $\mathbf{x}\mathbin{:}$

$$ \begin{bmatrix}{\color{blue}1} & {\color{blue}3} \\ 6 & 7\end{bmatrix} \begin{bmatrix}\bbox[lightgray, 2pt]{-3} \\ \bbox[lightgray, 2pt]{4}\end{bmatrix} = \begin{bmatrix}{\color{blue}1}\cdot (\bbox[lightgray, 2pt]{-3})+{\color{blue}3}\cdot \bbox[lightgray, 2pt]{4} \\ ∗\end{bmatrix} =\begin{bmatrix}9 \\ ∗\end{bmatrix} $$

To find $y_2,$ the $2$nd component of $\mathbf{y},$ we calculate the dot product of the $2$nd row of $A$ and the vector $\mathbf{x}\mathbin{:}$

$$ \begin{bmatrix}1 & 3 \\ {\color{blue}6} & {\color{blue}7}\end{bmatrix} \begin{bmatrix}\bbox[lightgray, 2pt]{-3} \\ \bbox[lightgray, 2pt]{4}\end{bmatrix} = \begin{bmatrix}9 \\ {\color{blue}6}\cdot (\bbox[lightgray, 2pt]{-3})+{\color{blue}7}\cdot \bbox[lightgray, 2pt]{4}\end{bmatrix} =\begin{bmatrix}9 \\ 10\end{bmatrix} $$

Therefore,

$$ A\mathbf{x}=\begin{bmatrix}9 \\ 10\end{bmatrix}. $$
