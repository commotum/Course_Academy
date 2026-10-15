Consider the following system of linear equations:

$$
\left\{\begin{aligned}x+2y+3z &=-12 \\ y-z &=0 \\ z &=12\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form.

- M∼\begin{bmatrix}1 & 0 & 0 & -24 \\ 0 & 1 & 0 & -12 \\ 0 & 0 & 1 & 12\end{bmatrix}
- M∼\begin{bmatrix}1 & 0 & 0 & -72 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 12\end{bmatrix}
* M∼\begin{bmatrix}1 & 0 & 0 & -72 \\ 0 & 1 & 0 & 12 \\ 0 & 0 & 1 & 12\end{bmatrix}
- M∼\begin{bmatrix}1 & 0 & 0 & 72 \\ 0 & 1 & 0 & 12 \\ 0 & 0 & 1 & 12\end{bmatrix}
- M∼\begin{bmatrix}1 & 0 & 0 & -24 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 12\end{bmatrix}

The augmented matrix for this system is

$$
M=\begin{bmatrix}1 & 2 & 3 & -12 \\ 0 & 1 & -1 & 0 \\ 0 & 0 & 1 & 12\end{bmatrix}.
$$

Notice that the matrix $M$ is already in row echelon form.

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & 2 & 3 & -12 \\ 0 & 1 & -1 & 0 \\ 0 & 0 & 1 & 12\end{bmatrix} & {R}_{2} & :={R}_{2}+{R}_{3} \\  & ∼\begin{bmatrix}1 & 2 & 3 & -12 \\ 0 & 1 & 0 & 12 \\ 0 & 0 & 1 & 12\end{bmatrix} & {R}_{1} & :={R}_{1}+(-3){R}_{3} \\  & ∼\begin{bmatrix}1 & 2 & 0 & -48 \\ 0 & 1 & 0 & 12 \\ 0 & 0 & 1 & 12\end{bmatrix} & {R}_{1} & :={R}_{1}+(-2){R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 0 & -72 \\ 0 & 1 & 0 & 12 \\ 0 & 0 & 1 & 12\end{bmatrix}.\end{aligned}
$$
