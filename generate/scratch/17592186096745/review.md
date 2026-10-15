## Source q-131632 and exact replay

Consider the following system of linear equations:

$$
\left\{\begin{aligned}-2x-5y+2z &=-7 \\ x+3y-z &=5 \\ x+3y-z &=5\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form.

$$\begin{bmatrix}1 & 0 & -1 & -4 \\ 0 & 1 & 1 & 3 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & -1 & -4 \\ 0 & 1 & 0 & 3 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & -1 & 4 \\ 0 & 1 & 1 & -1 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & -1 & -4 \\ 0 & 1 & 0 & -3 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & -1 & 14 \\ 0 & 1 & 0 & -3 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

The augmented matrix for this system is

$$
M=\begin{bmatrix}-2 & -5 & 2 & -7 \\ 1 & 3 & -1 & 5 \\ 1 & 3 & -1 & 5\end{bmatrix}.
$$

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}-2 & -5 & 2 & -7 \\ 1 & 3 & -1 & 5 \\ 1 & 3 & -1 & 5\end{bmatrix} & {R}_{1} & ↔{R}_{2} \\  & ∼\begin{bmatrix}1 & 3 & -1 & 5 \\ -2 & -5 & 2 & -7 \\ 1 & 3 & -1 & 5\end{bmatrix} & {R}_{2} & :={R}_{2}+2{R}_{1} \\  & ∼\begin{bmatrix}1 & 3 & -1 & 5 \\ 0 & 1 & 0 & 3 \\ 1 & 3 & -1 & 5\end{bmatrix} & {R}_{3} & :={R}_{3}-{R}_{1} \\  & ∼\begin{bmatrix}1 & 3 & -1 & 5 \\ 0 & 1 & 0 & 3 \\ 0 & 0 & 0 & 0\end{bmatrix}.\end{aligned}
$$

In the row echelon form above, we have only two pivots (in the $1$st and $2$nd columns). To transform the matrix to reduced row echelon form, we need to create zeros above the pivots only. This gives,

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & 3 & -1 & 5 \\ 0 & 1 & 0 & 3 \\ 0 & 0 & 0 & 0\end{bmatrix} & {R}_{1} & :={R}_{1}-3{R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & -1 & -4 \\ 0 & 1 & 0 & 3 \\ 0 & 0 & 0 & 0\end{bmatrix}.\end{aligned}
$$

## Source q-74617 and exact replay

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x-y+z &=3 \\ x+2y-2z &=0 \\ -2x+2y-2z &=-6\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form.

$$\begin{bmatrix}1 & 0 & 0 & 2 \\ 0 & 1 & -1 & -1 \\ 0 & 0 & 1 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & 0 & 2 \\ 0 & 1 & 0 & -1 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & 0 & 2 \\ 0 & 1 & 1 & 1 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & 0 & 2 \\ 0 & 1 & -1 & -1 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & 0 & 2 \\ 0 & 1 & 0 & -1 \\ 0 & 0 & 1 & 0\end{bmatrix}$$

The augmented matrix for this system is

$$
M=\begin{bmatrix}1 & -1 & 1 & 3 \\ 1 & 2 & -2 & 0 \\ -2 & 2 & -2 & -6\end{bmatrix}.
$$

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & -1 & 1 & 3 \\ 1 & 2 & -2 & 0 \\ -2 & 2 & -2 & -6\end{bmatrix} & {R}_{2} & :={R}_{2}+(-1){R}_{1} \\  & ∼\begin{bmatrix}1 & -1 & 1 & 3 \\ 0 & 3 & -3 & -3 \\ -2 & 2 & -2 & -6\end{bmatrix} & {R}_{3} & :={R}_{3}+2{R}_{1} \\  & ∼\begin{bmatrix}1 & -1 & 1 & 3 \\ 0 & 3 & -3 & -3 \\ 0 & 0 & 0 & 0\end{bmatrix} & {R}_{2} & :=\frac{1}{3}{R}_{2} \\  & ∼\begin{bmatrix}1 & -1 & 1 & 3 \\ 0 & 1 & -1 & -1 \\ 0 & 0 & 0 & 0\end{bmatrix}.\end{aligned}
$$

In the row echelon form above, we have only two pivots (in the $1$st and $2$nd columns). To transform the matrix to reduced row echelon form, we need to create zeros above the pivots only. This gives,

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & -1 & 1 & 3 \\ 0 & 1 & -1 & -1 \\ 0 & 0 & 0 & 0\end{bmatrix} & {R}_{1} & :={R}_{1}+{R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 0 & 2 \\ 0 & 1 & -1 & -1 \\ 0 & 0 & 0 & 0\end{bmatrix}.\end{aligned}
$$

## Source q-74618 and exact replay

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x-3y+5z &=1 \\ -x+4y-3z &=-1 \\ 6y+12z &=0\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form.

$$\begin{bmatrix}1 & 0 & 11 & 1 \\ 0 & 1 & 2 & 0 \\ 0 & 0 & 1 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & 0 & 1 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & 1 & 1 \\ 0 & 1 & 2 & 0 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & 1 & 1 \\ 0 & 1 & 2 & 1 \\ 0 & 0 & 1 & -1\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & 11 & 1 \\ 0 & 1 & 2 & 0 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

The augmented matrix for this system is

$$
M=\begin{bmatrix}1 & -3 & 5 & 1 \\ -1 & 4 & -3 & -1 \\ 0 & 6 & 12 & 0\end{bmatrix}.
$$

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & -3 & 5 & 1 \\ -1 & 4 & -3 & -1 \\ 0 & 6 & 12 & 0\end{bmatrix} & {R}_{2} & :={R}_{2}+{R}_{1} \\  & ∼\begin{bmatrix}1 & -3 & 5 & 1 \\ 0 & 1 & 2 & 0 \\ 0 & 6 & 12 & 0\end{bmatrix} & {R}_{3} & :={R}_{3}+(-6){R}_{2} \\  & ∼\begin{bmatrix}1 & -3 & 5 & 1 \\ 0 & 1 & 2 & 0 \\ 0 & 0 & 0 & 0\end{bmatrix}.\end{aligned}
$$

In the row echelon form above, we have only two pivots (in the $1$st and $2$nd columns). To transform the matrix to reduced row echelon form, we need to create zeros above the pivots only. This gives,

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & -3 & 5 & 1 \\ 0 & 1 & 2 & 0 \\ 0 & 0 & 0 & 0\end{bmatrix} & {R}_{1} & :={R}_{1}+3{R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 11 & 1 \\ 0 & 1 & 2 & 0 \\ 0 & 0 & 0 & 0\end{bmatrix}.\end{aligned}
$$

## Source q-131636 and exact replay

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x+2y+z &=6 \\ x+y+z &=10 \\ -4x-8y-4z &=-24\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form.

$$\begin{bmatrix}1 & 0 & 1 & 2 \\ 0 & 1 & 1 & -4 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

No solution

$$\begin{bmatrix}1 & 0 & 1 & -14 \\ 0 & 1 & 0 & 4 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & 1 & 14 \\ 0 & 1 & 0 & -4 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & 1 & -2 \\ 0 & 1 & 0 & -4 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

The augmented matrix for this system is

$$
M=\begin{bmatrix}1 & 2 & 1 & 6 \\ 1 & 1 & 1 & 10 \\ -4 & -8 & -4 & -24\end{bmatrix}.
$$

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & 2 & 1 & 6 \\ 1 & 1 & 1 & 10 \\ -4 & -8 & -4 & -24\end{bmatrix} & {R}_{2} & :={R}_{2}-{R}_{1} \\  & ∼\begin{bmatrix}1 & 2 & 1 & 6 \\ 0 & -1 & 0 & 4 \\ -4 & -8 & -4 & -24\end{bmatrix} & {R}_{3} & :={R}_{3}+4{R}_{1} \\  & ∼\begin{bmatrix}1 & 2 & 1 & 6 \\ 0 & -1 & 0 & 4 \\ 0 & 0 & 0 & 0\end{bmatrix} & {R}_{2} & :=-{R}_{2} \\  & ∼\begin{bmatrix}1 & 2 & 1 & 6 \\ 0 & 1 & 0 & -4 \\ 0 & 0 & 0 & 0\end{bmatrix}.\end{aligned}
$$

In the row echelon form above, we have only two pivots (in the $1$st and $2$nd columns). To transform the matrix to reduced row echelon form, we need to create zeros above the pivots only. This gives,

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & 2 & 1 & 6 \\ 0 & 1 & 0 & -4 \\ 0 & 0 & 0 & 0\end{bmatrix} & {R}_{1} & :={R}_{1}-2{R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 1 & 14 \\ 0 & 1 & 0 & -4 \\ 0 & 0 & 0 & 0\end{bmatrix}.\end{aligned}
$$

## Source q-74621 and exact replay

Consider the following system of linear equations:

$$
\left\{\begin{aligned}4x-11y+5z &=-1 \\ x-3y+2z &=1 \\ -3x+9y-6z &=-3\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form.

$$\begin{bmatrix}1 & 0 & 11 & -14 \\ 0 & 1 & -3 & -5 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & 11 & -14 \\ 0 & 1 & 3 & -5 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & -7 & -14 \\ 0 & 1 & -3 & -5 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & -7 & -14 \\ 0 & 1 & -3 & -5 \\ 0 & 0 & 1 & -1\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & 0 & -14 \\ 0 & 1 & 0 & -5 \\ 0 & 0 & 1 & -1\end{bmatrix}$$

The augmented matrix for this system is

$$
M=\begin{bmatrix}4 & -11 & 5 & -1 \\ 1 & -3 & 2 & 1 \\ -3 & 9 & -6 & -3\end{bmatrix}.
$$

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}4 & -11 & 5 & -1 \\ 1 & -3 & 2 & 1 \\ -3 & 9 & -6 & -3\end{bmatrix} & {R}_{1} & ↔{R}_{2} \\  & ∼\begin{bmatrix}1 & -3 & 2 & 1 \\ 4 & -11 & 5 & -1 \\ -3 & 9 & -6 & -3\end{bmatrix} & {R}_{2} & :={R}_{2}+(-4){R}_{1} \\  & ∼\begin{bmatrix}1 & -3 & 2 & 1 \\ 0 & 1 & -3 & -5 \\ -3 & 9 & -6 & -3\end{bmatrix} & {R}_{3} & :={R}_{3}+3{R}_{1} \\  & ∼\begin{bmatrix}1 & -3 & 2 & 1 \\ 0 & 1 & -3 & -5 \\ 0 & 0 & 0 & 0\end{bmatrix}.\end{aligned}
$$

In the row echelon form above, we have only two pivots (in the $1$st and $2$nd columns). To transform the matrix to reduced row echelon form, we need to create zeros above the pivots only. This gives,

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & -3 & 2 & 1 \\ 0 & 1 & -3 & -5 \\ 0 & 0 & 0 & 0\end{bmatrix} & {R}_{1} & :={R}_{1}+3{R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & -7 & -14 \\ 0 & 1 & -3 & -5 \\ 0 & 0 & 0 & 0\end{bmatrix}.\end{aligned}
$$

## Changed RHS, fixed coefficients: q-131632, k=-2

Consider the following system of linear equations:

$$
\left\{\begin{aligned}-2x-5y+2z &=14 \\ x+3y-z &=-10 \\ x+3y-z &=-10\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form.

$$\begin{bmatrix}1 & 0 & -1 & 8 \\ 0 & 1 & 1 & -6 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & -1 & 8 \\ 0 & 1 & 0 & -6 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & -1 & -8 \\ 0 & 1 & 1 & 2 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & -1 & 8 \\ 0 & 1 & 0 & 6 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & -1 & -28 \\ 0 & 1 & 0 & 6 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

The augmented matrix for this system is

$$
M=\begin{bmatrix}-2 & -5 & 2 & 14 \\ 1 & 3 & -1 & -10 \\ 1 & 3 & -1 & -10\end{bmatrix}.
$$

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}-2 & -5 & 2 & 14 \\ 1 & 3 & -1 & -10 \\ 1 & 3 & -1 & -10\end{bmatrix} & {R}_{1} & ↔{R}_{2} \\  & ∼\begin{bmatrix}1 & 3 & -1 & -10 \\ -2 & -5 & 2 & 14 \\ 1 & 3 & -1 & -10\end{bmatrix} & {R}_{2} & :={R}_{2}+2{R}_{1} \\  & ∼\begin{bmatrix}1 & 3 & -1 & -10 \\ 0 & 1 & 0 & -6 \\ 1 & 3 & -1 & -10\end{bmatrix} & {R}_{3} & :={R}_{3}-{R}_{1} \\  & ∼\begin{bmatrix}1 & 3 & -1 & -10 \\ 0 & 1 & 0 & -6 \\ 0 & 0 & 0 & 0\end{bmatrix}.\end{aligned}
$$

In the row echelon form above, we have only two pivots (in the $1$st and $2$nd columns). To transform the matrix to reduced row echelon form, we need to create zeros above the pivots only. This gives,

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & 3 & -1 & -10 \\ 0 & 1 & 0 & -6 \\ 0 & 0 & 0 & 0\end{bmatrix} & {R}_{1} & :={R}_{1}-3{R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & -1 & 8 \\ 0 & 1 & 0 & -6 \\ 0 & 0 & 0 & 0\end{bmatrix}.\end{aligned}
$$

## Changed RHS, fixed coefficients: q-131632, k=3

Consider the following system of linear equations:

$$
\left\{\begin{aligned}-2x-5y+2z &=-21 \\ x+3y-z &=15 \\ x+3y-z &=15\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form.

$$\begin{bmatrix}1 & 0 & -1 & -12 \\ 0 & 1 & 1 & 9 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & -1 & -12 \\ 0 & 1 & 0 & 9 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & -1 & 12 \\ 0 & 1 & 1 & -3 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & -1 & -12 \\ 0 & 1 & 0 & -9 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & -1 & 42 \\ 0 & 1 & 0 & -9 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

The augmented matrix for this system is

$$
M=\begin{bmatrix}-2 & -5 & 2 & -21 \\ 1 & 3 & -1 & 15 \\ 1 & 3 & -1 & 15\end{bmatrix}.
$$

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}-2 & -5 & 2 & -21 \\ 1 & 3 & -1 & 15 \\ 1 & 3 & -1 & 15\end{bmatrix} & {R}_{1} & ↔{R}_{2} \\  & ∼\begin{bmatrix}1 & 3 & -1 & 15 \\ -2 & -5 & 2 & -21 \\ 1 & 3 & -1 & 15\end{bmatrix} & {R}_{2} & :={R}_{2}+2{R}_{1} \\  & ∼\begin{bmatrix}1 & 3 & -1 & 15 \\ 0 & 1 & 0 & 9 \\ 1 & 3 & -1 & 15\end{bmatrix} & {R}_{3} & :={R}_{3}-{R}_{1} \\  & ∼\begin{bmatrix}1 & 3 & -1 & 15 \\ 0 & 1 & 0 & 9 \\ 0 & 0 & 0 & 0\end{bmatrix}.\end{aligned}
$$

In the row echelon form above, we have only two pivots (in the $1$st and $2$nd columns). To transform the matrix to reduced row echelon form, we need to create zeros above the pivots only. This gives,

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & 3 & -1 & 15 \\ 0 & 1 & 0 & 9 \\ 0 & 0 & 0 & 0\end{bmatrix} & {R}_{1} & :={R}_{1}-3{R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & -1 & -12 \\ 0 & 1 & 0 & 9 \\ 0 & 0 & 0 & 0\end{bmatrix}.\end{aligned}
$$

## Changed RHS, fixed coefficients: q-74617, k=-2

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x-y+z &=-6 \\ x+2y-2z &=0 \\ -2x+2y-2z &=12\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form.

$$\begin{bmatrix}1 & 0 & 0 & -4 \\ 0 & 1 & -1 & 2 \\ 0 & 0 & 1 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & 0 & -4 \\ 0 & 1 & 0 & 2 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & 0 & -4 \\ 0 & 1 & 1 & -2 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & 0 & -4 \\ 0 & 1 & -1 & 2 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & 0 & -4 \\ 0 & 1 & 0 & 2 \\ 0 & 0 & 1 & 0\end{bmatrix}$$

The augmented matrix for this system is

$$
M=\begin{bmatrix}1 & -1 & 1 & -6 \\ 1 & 2 & -2 & 0 \\ -2 & 2 & -2 & 12\end{bmatrix}.
$$

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & -1 & 1 & -6 \\ 1 & 2 & -2 & 0 \\ -2 & 2 & -2 & 12\end{bmatrix} & {R}_{2} & :={R}_{2}+(-1){R}_{1} \\  & ∼\begin{bmatrix}1 & -1 & 1 & -6 \\ 0 & 3 & -3 & 6 \\ -2 & 2 & -2 & 12\end{bmatrix} & {R}_{3} & :={R}_{3}+2{R}_{1} \\  & ∼\begin{bmatrix}1 & -1 & 1 & -6 \\ 0 & 3 & -3 & 6 \\ 0 & 0 & 0 & 0\end{bmatrix} & {R}_{2} & :=\frac{1}{3}{R}_{2} \\  & ∼\begin{bmatrix}1 & -1 & 1 & -6 \\ 0 & 1 & -1 & 2 \\ 0 & 0 & 0 & 0\end{bmatrix}.\end{aligned}
$$

In the row echelon form above, we have only two pivots (in the $1$st and $2$nd columns). To transform the matrix to reduced row echelon form, we need to create zeros above the pivots only. This gives,

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & -1 & 1 & -6 \\ 0 & 1 & -1 & 2 \\ 0 & 0 & 0 & 0\end{bmatrix} & {R}_{1} & :={R}_{1}+{R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 0 & -4 \\ 0 & 1 & -1 & 2 \\ 0 & 0 & 0 & 0\end{bmatrix}.\end{aligned}
$$

## Changed RHS, fixed coefficients: q-74617, k=3

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x-y+z &=9 \\ x+2y-2z &=0 \\ -2x+2y-2z &=-18\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form.

$$\begin{bmatrix}1 & 0 & 0 & 6 \\ 0 & 1 & -1 & -3 \\ 0 & 0 & 1 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & 0 & 6 \\ 0 & 1 & 0 & -3 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & 0 & 6 \\ 0 & 1 & 1 & 3 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & 0 & 6 \\ 0 & 1 & -1 & -3 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & 0 & 6 \\ 0 & 1 & 0 & -3 \\ 0 & 0 & 1 & 0\end{bmatrix}$$

The augmented matrix for this system is

$$
M=\begin{bmatrix}1 & -1 & 1 & 9 \\ 1 & 2 & -2 & 0 \\ -2 & 2 & -2 & -18\end{bmatrix}.
$$

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & -1 & 1 & 9 \\ 1 & 2 & -2 & 0 \\ -2 & 2 & -2 & -18\end{bmatrix} & {R}_{2} & :={R}_{2}+(-1){R}_{1} \\  & ∼\begin{bmatrix}1 & -1 & 1 & 9 \\ 0 & 3 & -3 & -9 \\ -2 & 2 & -2 & -18\end{bmatrix} & {R}_{3} & :={R}_{3}+2{R}_{1} \\  & ∼\begin{bmatrix}1 & -1 & 1 & 9 \\ 0 & 3 & -3 & -9 \\ 0 & 0 & 0 & 0\end{bmatrix} & {R}_{2} & :=\frac{1}{3}{R}_{2} \\  & ∼\begin{bmatrix}1 & -1 & 1 & 9 \\ 0 & 1 & -1 & -3 \\ 0 & 0 & 0 & 0\end{bmatrix}.\end{aligned}
$$

In the row echelon form above, we have only two pivots (in the $1$st and $2$nd columns). To transform the matrix to reduced row echelon form, we need to create zeros above the pivots only. This gives,

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & -1 & 1 & 9 \\ 0 & 1 & -1 & -3 \\ 0 & 0 & 0 & 0\end{bmatrix} & {R}_{1} & :={R}_{1}+{R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 0 & 6 \\ 0 & 1 & -1 & -3 \\ 0 & 0 & 0 & 0\end{bmatrix}.\end{aligned}
$$

## Changed RHS, fixed coefficients: q-74618, k=-2

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x-3y+5z &=-2 \\ -x+4y-3z &=2 \\ 6y+12z &=0\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form.

$$\begin{bmatrix}1 & 0 & 11 & -2 \\ 0 & 1 & 2 & 0 \\ 0 & 0 & 1 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & 0 & -2 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & 1 & -2 \\ 0 & 1 & 2 & 0 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & 1 & -2 \\ 0 & 1 & 2 & -2 \\ 0 & 0 & 1 & 2\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & 11 & -2 \\ 0 & 1 & 2 & 0 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

The augmented matrix for this system is

$$
M=\begin{bmatrix}1 & -3 & 5 & -2 \\ -1 & 4 & -3 & 2 \\ 0 & 6 & 12 & 0\end{bmatrix}.
$$

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & -3 & 5 & -2 \\ -1 & 4 & -3 & 2 \\ 0 & 6 & 12 & 0\end{bmatrix} & {R}_{2} & :={R}_{2}+{R}_{1} \\  & ∼\begin{bmatrix}1 & -3 & 5 & -2 \\ 0 & 1 & 2 & 0 \\ 0 & 6 & 12 & 0\end{bmatrix} & {R}_{3} & :={R}_{3}+(-6){R}_{2} \\  & ∼\begin{bmatrix}1 & -3 & 5 & -2 \\ 0 & 1 & 2 & 0 \\ 0 & 0 & 0 & 0\end{bmatrix}.\end{aligned}
$$

In the row echelon form above, we have only two pivots (in the $1$st and $2$nd columns). To transform the matrix to reduced row echelon form, we need to create zeros above the pivots only. This gives,

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & -3 & 5 & -2 \\ 0 & 1 & 2 & 0 \\ 0 & 0 & 0 & 0\end{bmatrix} & {R}_{1} & :={R}_{1}+3{R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 11 & -2 \\ 0 & 1 & 2 & 0 \\ 0 & 0 & 0 & 0\end{bmatrix}.\end{aligned}
$$

## Changed RHS, fixed coefficients: q-74618, k=3

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x-3y+5z &=3 \\ -x+4y-3z &=-3 \\ 6y+12z &=0\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form.

$$\begin{bmatrix}1 & 0 & 11 & 3 \\ 0 & 1 & 2 & 0 \\ 0 & 0 & 1 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & 0 & 3 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & 1 & 3 \\ 0 & 1 & 2 & 0 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & 1 & 3 \\ 0 & 1 & 2 & 3 \\ 0 & 0 & 1 & -3\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & 11 & 3 \\ 0 & 1 & 2 & 0 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

The augmented matrix for this system is

$$
M=\begin{bmatrix}1 & -3 & 5 & 3 \\ -1 & 4 & -3 & -3 \\ 0 & 6 & 12 & 0\end{bmatrix}.
$$

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & -3 & 5 & 3 \\ -1 & 4 & -3 & -3 \\ 0 & 6 & 12 & 0\end{bmatrix} & {R}_{2} & :={R}_{2}+{R}_{1} \\  & ∼\begin{bmatrix}1 & -3 & 5 & 3 \\ 0 & 1 & 2 & 0 \\ 0 & 6 & 12 & 0\end{bmatrix} & {R}_{3} & :={R}_{3}+(-6){R}_{2} \\  & ∼\begin{bmatrix}1 & -3 & 5 & 3 \\ 0 & 1 & 2 & 0 \\ 0 & 0 & 0 & 0\end{bmatrix}.\end{aligned}
$$

In the row echelon form above, we have only two pivots (in the $1$st and $2$nd columns). To transform the matrix to reduced row echelon form, we need to create zeros above the pivots only. This gives,

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & -3 & 5 & 3 \\ 0 & 1 & 2 & 0 \\ 0 & 0 & 0 & 0\end{bmatrix} & {R}_{1} & :={R}_{1}+3{R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 11 & 3 \\ 0 & 1 & 2 & 0 \\ 0 & 0 & 0 & 0\end{bmatrix}.\end{aligned}
$$

## Changed RHS, fixed coefficients: q-131636, k=-2

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x+2y+z &=-12 \\ x+y+z &=-20 \\ -4x-8y-4z &=48\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form.

$$\begin{bmatrix}1 & 0 & 1 & -4 \\ 0 & 1 & 1 & 8 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

No solution

$$\begin{bmatrix}1 & 0 & 1 & 28 \\ 0 & 1 & 0 & -8 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & 1 & -28 \\ 0 & 1 & 0 & 8 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & 1 & 4 \\ 0 & 1 & 0 & 8 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

The augmented matrix for this system is

$$
M=\begin{bmatrix}1 & 2 & 1 & -12 \\ 1 & 1 & 1 & -20 \\ -4 & -8 & -4 & 48\end{bmatrix}.
$$

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & 2 & 1 & -12 \\ 1 & 1 & 1 & -20 \\ -4 & -8 & -4 & 48\end{bmatrix} & {R}_{2} & :={R}_{2}-{R}_{1} \\  & ∼\begin{bmatrix}1 & 2 & 1 & -12 \\ 0 & -1 & 0 & -8 \\ -4 & -8 & -4 & 48\end{bmatrix} & {R}_{3} & :={R}_{3}+4{R}_{1} \\  & ∼\begin{bmatrix}1 & 2 & 1 & -12 \\ 0 & -1 & 0 & -8 \\ 0 & 0 & 0 & 0\end{bmatrix} & {R}_{2} & :=-{R}_{2} \\  & ∼\begin{bmatrix}1 & 2 & 1 & -12 \\ 0 & 1 & 0 & 8 \\ 0 & 0 & 0 & 0\end{bmatrix}.\end{aligned}
$$

In the row echelon form above, we have only two pivots (in the $1$st and $2$nd columns). To transform the matrix to reduced row echelon form, we need to create zeros above the pivots only. This gives,

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & 2 & 1 & -12 \\ 0 & 1 & 0 & 8 \\ 0 & 0 & 0 & 0\end{bmatrix} & {R}_{1} & :={R}_{1}-2{R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 1 & -28 \\ 0 & 1 & 0 & 8 \\ 0 & 0 & 0 & 0\end{bmatrix}.\end{aligned}
$$

## Changed RHS, fixed coefficients: q-131636, k=3

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x+2y+z &=18 \\ x+y+z &=30 \\ -4x-8y-4z &=-72\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form.

$$\begin{bmatrix}1 & 0 & 1 & 6 \\ 0 & 1 & 1 & -12 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

No solution

$$\begin{bmatrix}1 & 0 & 1 & -42 \\ 0 & 1 & 0 & 12 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & 1 & 42 \\ 0 & 1 & 0 & -12 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & 1 & -6 \\ 0 & 1 & 0 & -12 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

The augmented matrix for this system is

$$
M=\begin{bmatrix}1 & 2 & 1 & 18 \\ 1 & 1 & 1 & 30 \\ -4 & -8 & -4 & -72\end{bmatrix}.
$$

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & 2 & 1 & 18 \\ 1 & 1 & 1 & 30 \\ -4 & -8 & -4 & -72\end{bmatrix} & {R}_{2} & :={R}_{2}-{R}_{1} \\  & ∼\begin{bmatrix}1 & 2 & 1 & 18 \\ 0 & -1 & 0 & 12 \\ -4 & -8 & -4 & -72\end{bmatrix} & {R}_{3} & :={R}_{3}+4{R}_{1} \\  & ∼\begin{bmatrix}1 & 2 & 1 & 18 \\ 0 & -1 & 0 & 12 \\ 0 & 0 & 0 & 0\end{bmatrix} & {R}_{2} & :=-{R}_{2} \\  & ∼\begin{bmatrix}1 & 2 & 1 & 18 \\ 0 & 1 & 0 & -12 \\ 0 & 0 & 0 & 0\end{bmatrix}.\end{aligned}
$$

In the row echelon form above, we have only two pivots (in the $1$st and $2$nd columns). To transform the matrix to reduced row echelon form, we need to create zeros above the pivots only. This gives,

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & 2 & 1 & 18 \\ 0 & 1 & 0 & -12 \\ 0 & 0 & 0 & 0\end{bmatrix} & {R}_{1} & :={R}_{1}-2{R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 1 & 42 \\ 0 & 1 & 0 & -12 \\ 0 & 0 & 0 & 0\end{bmatrix}.\end{aligned}
$$

## Changed RHS, fixed coefficients: q-74621, k=-2

Consider the following system of linear equations:

$$
\left\{\begin{aligned}4x-11y+5z &=2 \\ x-3y+2z &=-2 \\ -3x+9y-6z &=6\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form.

$$\begin{bmatrix}1 & 0 & 11 & 28 \\ 0 & 1 & -3 & 10 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & 11 & 28 \\ 0 & 1 & 3 & 10 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & -7 & 28 \\ 0 & 1 & -3 & 10 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & -7 & 28 \\ 0 & 1 & -3 & 10 \\ 0 & 0 & 1 & 2\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & 0 & 28 \\ 0 & 1 & 0 & 10 \\ 0 & 0 & 1 & 2\end{bmatrix}$$

The augmented matrix for this system is

$$
M=\begin{bmatrix}4 & -11 & 5 & 2 \\ 1 & -3 & 2 & -2 \\ -3 & 9 & -6 & 6\end{bmatrix}.
$$

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}4 & -11 & 5 & 2 \\ 1 & -3 & 2 & -2 \\ -3 & 9 & -6 & 6\end{bmatrix} & {R}_{1} & ↔{R}_{2} \\  & ∼\begin{bmatrix}1 & -3 & 2 & -2 \\ 4 & -11 & 5 & 2 \\ -3 & 9 & -6 & 6\end{bmatrix} & {R}_{2} & :={R}_{2}+(-4){R}_{1} \\  & ∼\begin{bmatrix}1 & -3 & 2 & -2 \\ 0 & 1 & -3 & 10 \\ -3 & 9 & -6 & 6\end{bmatrix} & {R}_{3} & :={R}_{3}+3{R}_{1} \\  & ∼\begin{bmatrix}1 & -3 & 2 & -2 \\ 0 & 1 & -3 & 10 \\ 0 & 0 & 0 & 0\end{bmatrix}.\end{aligned}
$$

In the row echelon form above, we have only two pivots (in the $1$st and $2$nd columns). To transform the matrix to reduced row echelon form, we need to create zeros above the pivots only. This gives,

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & -3 & 2 & -2 \\ 0 & 1 & -3 & 10 \\ 0 & 0 & 0 & 0\end{bmatrix} & {R}_{1} & :={R}_{1}+3{R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & -7 & 28 \\ 0 & 1 & -3 & 10 \\ 0 & 0 & 0 & 0\end{bmatrix}.\end{aligned}
$$

## Changed RHS, fixed coefficients: q-74621, k=3

Consider the following system of linear equations:

$$
\left\{\begin{aligned}4x-11y+5z &=-3 \\ x-3y+2z &=3 \\ -3x+9y-6z &=-9\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form.

$$\begin{bmatrix}1 & 0 & 11 & -42 \\ 0 & 1 & -3 & -15 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & 11 & -42 \\ 0 & 1 & 3 & -15 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & -7 & -42 \\ 0 & 1 & -3 & -15 \\ 0 & 0 & 0 & 0\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & -7 & -42 \\ 0 & 1 & -3 & -15 \\ 0 & 0 & 1 & -3\end{bmatrix}$$

$$\begin{bmatrix}1 & 0 & 0 & -42 \\ 0 & 1 & 0 & -15 \\ 0 & 0 & 1 & -3\end{bmatrix}$$

The augmented matrix for this system is

$$
M=\begin{bmatrix}4 & -11 & 5 & -3 \\ 1 & -3 & 2 & 3 \\ -3 & 9 & -6 & -9\end{bmatrix}.
$$

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}4 & -11 & 5 & -3 \\ 1 & -3 & 2 & 3 \\ -3 & 9 & -6 & -9\end{bmatrix} & {R}_{1} & ↔{R}_{2} \\  & ∼\begin{bmatrix}1 & -3 & 2 & 3 \\ 4 & -11 & 5 & -3 \\ -3 & 9 & -6 & -9\end{bmatrix} & {R}_{2} & :={R}_{2}+(-4){R}_{1} \\  & ∼\begin{bmatrix}1 & -3 & 2 & 3 \\ 0 & 1 & -3 & -15 \\ -3 & 9 & -6 & -9\end{bmatrix} & {R}_{3} & :={R}_{3}+3{R}_{1} \\  & ∼\begin{bmatrix}1 & -3 & 2 & 3 \\ 0 & 1 & -3 & -15 \\ 0 & 0 & 0 & 0\end{bmatrix}.\end{aligned}
$$

In the row echelon form above, we have only two pivots (in the $1$st and $2$nd columns). To transform the matrix to reduced row echelon form, we need to create zeros above the pivots only. This gives,

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & -3 & 2 & 3 \\ 0 & 1 & -3 & -15 \\ 0 & 0 & 0 & 0\end{bmatrix} & {R}_{1} & :={R}_{1}+3{R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & -7 & -42 \\ 0 & 1 & -3 & -15 \\ 0 & 0 & 0 & 0\end{bmatrix}.\end{aligned}
$$
