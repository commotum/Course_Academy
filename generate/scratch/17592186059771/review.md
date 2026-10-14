# Original and generated review

Basis 2366. Source records are preserved. Moderate one-row addition; five matrix choices; no plots.

## q-10248

### Original

Consider the matrix $M,$ given by

$$
M=\begin{bmatrix}-1 & 2 & 4 \\ 8 & 3 & 1 \\ 3 & -1 & 9\end{bmatrix}.
$$

What matrix results from carrying out the row operation ${R}_{3}:={R}_{3}+3{R}_{1}$ on $M?$

The operation ${R}_{3}:={R}_{3}+3{R}_{1}$ means that we need to add $3$ times the first row to the third row.

Applying this row operation, we obtain the following:

$$
\begin{aligned}M & =\begin{bmatrix}-1 & 2 & 4 \\ 8 & 3 & 1 \\ 3 & -1 & 9\end{bmatrix}\,{R}_{3}:={R}_{3}+3\cdot {R}_{1} \\  & ∼\begin{bmatrix}1 & -2 & -4 \\ 8 & 3 & 1 \\ 3+(3)(-1) & -1+(3)(2) & 9+(3)(4)\end{bmatrix} \\  & ∼\begin{bmatrix}-1 & 2 & 4 \\ 8 & 3 & 1 \\ 0 & 5 & 21\end{bmatrix}\end{aligned}
$$

### Parameterized source replay

Consider the matrix $M,$ given by

$$
M=\begin{bmatrix}-1 & 2 & 4 \\ 8 & 3 & 1 \\ 3 & -1 & 9\end{bmatrix}.
$$

What matrix results from carrying out the row operation ${R}_{3}:={R}_{3}+3{R}_{1}$ on $M?$

$\begin{bmatrix}3 & -1 & 9 \\ 8 & 3 & 1 \\ -1 & 2 & 4\end{bmatrix}$

$\begin{bmatrix}-1 & 2 & 4 \\ 8 & 3 & 1 \\ 3 & -1 & 9\end{bmatrix}$

$\begin{bmatrix}-1 & 2 & 4 \\ 8 & 3 & 1 \\ 0 & 5 & 21\end{bmatrix}$ [correct]

$\begin{bmatrix}-1 & 2 & 4 \\ 8 & 3 & 1 \\ 0 & -1 & 9\end{bmatrix}$

$\begin{bmatrix}-3 & 1 & -9 \\ 8 & 3 & 1 \\ -1 & 2 & 4\end{bmatrix}$

The operation ${R}_{3}:={R}_{3}+3{R}_{1}$ means that we need to add $3$ times the first row to the third row.

Applying this row operation, we obtain the following:

$$
\begin{aligned}M & =\begin{bmatrix}-1 & 2 & 4 \\ 8 & 3 & 1 \\ 3 & -1 & 9\end{bmatrix}\,{R}_{3}:={R}_{3}+3{R}_{1} \\  & \sim\begin{bmatrix}-1 & 2 & 4 \\ 8 & 3 & 1 \\ 3+(3)(-1) & -1+(3)(2) & 9+(3)(4)\end{bmatrix} \\  & \sim\begin{bmatrix}-1 & 2 & 4 \\ 8 & 3 & 1 \\ 0 & 5 & 21\end{bmatrix}\end{aligned}
$$

## q-20239

### Original

Consider the matrix $X,$ given by

$$
X=\begin{bmatrix}1 & 2 & 1 \\ 3 & -1 & 1 \\ 2 & 3 & 2\end{bmatrix}.
$$

What matrix results from carrying out the row operation ${R}_{2}:={R}_{2}-3{R}_{1}$ on $X?$

The operation ${R}_{2}:={R}_{2}-3{R}_{1}$ means that we need to add $-3$ times the first row to the second row. 

Applying this row operation, we obtain the following:

$$
\begin{aligned}X & =\begin{bmatrix}1 & 2 & 1 \\ 3 & -1 & 1 \\ 2 & 3 & 2\end{bmatrix}\,{R}_{2}:={R}_{2}+(-3)\cdot {R}_{1} \\  & ∼\begin{bmatrix}1 & 2 & 1 \\ 3+(-3)(1) & -1+(-3)(2) & 1+(-3)(1) \\ 2 & 3 & 2\end{bmatrix} \\  & ∼\begin{bmatrix}1 & 2 & 1 \\ 0 & -7 & -2 \\ 2 & 3 & 2\end{bmatrix}\end{aligned}
$$

### Parameterized source replay

Consider the matrix $X,$ given by

$$
X=\begin{bmatrix}1 & 2 & 1 \\ 3 & -1 & 1 \\ 2 & 3 & 2\end{bmatrix}.
$$

What matrix results from carrying out the row operation ${R}_{2}:={R}_{2}-3{R}_{1}$ on $X?$

$\begin{bmatrix}1 & 2 & 1 \\ 3 & -1 & 1 \\ -1 & -3 & -1\end{bmatrix}$

$\begin{bmatrix}0 & -7 & -2 \\ 1 & 2 & 1 \\ 2 & 3 & 2\end{bmatrix}$

$\begin{bmatrix}1 & 2 & 1 \\ 0 & -7 & -2 \\ 2 & 3 & 2\end{bmatrix}$ [correct]

$\begin{bmatrix}1 & -1 & 1 \\ 3 & -10 & 1 \\ 2 & -3 & 2\end{bmatrix}$

$\begin{bmatrix}-1 & -3 & -1 \\ 1 & 2 & 1 \\ 3 & -1 & 1\end{bmatrix}$

The operation ${R}_{2}:={R}_{2}-3{R}_{1}$ means that we need to add $-3$ times the first row to the second row.

Applying this row operation, we obtain the following:

$$
\begin{aligned}X & =\begin{bmatrix}1 & 2 & 1 \\ 3 & -1 & 1 \\ 2 & 3 & 2\end{bmatrix}\,{R}_{2}:={R}_{2}-3{R}_{1} \\  & \sim\begin{bmatrix}1 & 2 & 1 \\ 3+(-3)(1) & -1+(-3)(2) & 1+(-3)(1) \\ 2 & 3 & 2\end{bmatrix} \\  & \sim\begin{bmatrix}1 & 2 & 1 \\ 0 & -7 & -2 \\ 2 & 3 & 2\end{bmatrix}\end{aligned}
$$

## Variant q-10248

{"matrix": [[-1, 7, 6], [-1, 0, 6], [2, 9, -3]], "target": 2, "source": 1, "k": 2, "name": "M"}

Consider the matrix $M,$ given by

$$
M=\begin{bmatrix}-1 & 7 & 6 \\ -1 & 0 & 6 \\ 2 & 9 & -3\end{bmatrix}.
$$

What matrix results from carrying out the row operation ${R}_{3}:={R}_{3}+2{R}_{2}$ on $M?$

$\begin{bmatrix}-1 & 7 & 6 \\ 2 & 9 & -3 \\ -1 & 0 & 6\end{bmatrix}$

$\begin{bmatrix}-1 & 7 & 6 \\ -1 & 0 & 6 \\ 0 & 9 & 9\end{bmatrix}$ [correct]

$\begin{bmatrix}-1 & 7 & 6 \\ -2 & -9 & 3 \\ -1 & 0 & 6\end{bmatrix}$

$\begin{bmatrix}-1 & 7 & 6 \\ -1 & 0 & 6 \\ 2 & 9 & -3\end{bmatrix}$

$\begin{bmatrix}-1 & 7 & 6 \\ -1 & 0 & 6 \\ 0 & 9 & -3\end{bmatrix}$

The operation ${R}_{3}:={R}_{3}+2{R}_{2}$ means that we need to add $2$ times the second row to the third row.

Applying this row operation, we obtain the following:

$$
\begin{aligned}M & =\begin{bmatrix}-1 & 7 & 6 \\ -1 & 0 & 6 \\ 2 & 9 & -3\end{bmatrix}\,{R}_{3}:={R}_{3}+2{R}_{2} \\  & \sim\begin{bmatrix}-1 & 7 & 6 \\ -1 & 0 & 6 \\ 2+(2)(-1) & 9+(2)(0) & -3+(2)(6)\end{bmatrix} \\  & \sim\begin{bmatrix}-1 & 7 & 6 \\ -1 & 0 & 6 \\ 0 & 9 & 9\end{bmatrix}\end{aligned}
$$

## Variant q-10248

{"matrix": [[-1, 6, 5], [6, 3, -3], [4, 6, -9]], "target": 2, "source": 0, "k": 4, "name": "M"}

Consider the matrix $M,$ given by

$$
M=\begin{bmatrix}-1 & 6 & 5 \\ 6 & 3 & -3 \\ 4 & 6 & -9\end{bmatrix}.
$$

What matrix results from carrying out the row operation ${R}_{3}:={R}_{3}+4{R}_{1}$ on $M?$

$\begin{bmatrix}-1 & 6 & 5 \\ 6 & 3 & -3 \\ 4 & 6 & -9\end{bmatrix}$

$\begin{bmatrix}-1 & 6 & 5 \\ 6 & 3 & -3 \\ 0 & 30 & 11\end{bmatrix}$ [correct]

$\begin{bmatrix}4 & 6 & -9 \\ 6 & 3 & -3 \\ -1 & 6 & 5\end{bmatrix}$

$\begin{bmatrix}-1 & 6 & 5 \\ 6 & 3 & -3 \\ 0 & 6 & -9\end{bmatrix}$

$\begin{bmatrix}-4 & -6 & 9 \\ 6 & 3 & -3 \\ -1 & 6 & 5\end{bmatrix}$

The operation ${R}_{3}:={R}_{3}+4{R}_{1}$ means that we need to add $4$ times the first row to the third row.

Applying this row operation, we obtain the following:

$$
\begin{aligned}M & =\begin{bmatrix}-1 & 6 & 5 \\ 6 & 3 & -3 \\ 4 & 6 & -9\end{bmatrix}\,{R}_{3}:={R}_{3}+4{R}_{1} \\  & \sim\begin{bmatrix}-1 & 6 & 5 \\ 6 & 3 & -3 \\ 4+(4)(-1) & 6+(4)(6) & -9+(4)(5)\end{bmatrix} \\  & \sim\begin{bmatrix}-1 & 6 & 5 \\ 6 & 3 & -3 \\ 0 & 30 & 11\end{bmatrix}\end{aligned}
$$

## Variant q-10248

{"matrix": [[-1, -4, 0], [-1, -3, -8], [2, -4, 4]], "target": 2, "source": 0, "k": 2, "name": "M"}

Consider the matrix $M,$ given by

$$
M=\begin{bmatrix}-1 & -4 & 0 \\ -1 & -3 & -8 \\ 2 & -4 & 4\end{bmatrix}.
$$

What matrix results from carrying out the row operation ${R}_{3}:={R}_{3}+2{R}_{1}$ on $M?$

$\begin{bmatrix}-1 & -4 & 0 \\ -1 & -3 & -8 \\ 0 & -12 & 4\end{bmatrix}$ [correct]

$\begin{bmatrix}-1 & -4 & 0 \\ -1 & -3 & -8 \\ 2 & -4 & 4\end{bmatrix}$

$\begin{bmatrix}-1 & -4 & 0 \\ -1 & -3 & -8 \\ 0 & -4 & 4\end{bmatrix}$

$\begin{bmatrix}2 & -4 & 4 \\ -1 & -3 & -8 \\ -1 & -4 & 0\end{bmatrix}$

$\begin{bmatrix}-2 & 4 & -4 \\ -1 & -3 & -8 \\ -1 & -4 & 0\end{bmatrix}$

The operation ${R}_{3}:={R}_{3}+2{R}_{1}$ means that we need to add $2$ times the first row to the third row.

Applying this row operation, we obtain the following:

$$
\begin{aligned}M & =\begin{bmatrix}-1 & -4 & 0 \\ -1 & -3 & -8 \\ 2 & -4 & 4\end{bmatrix}\,{R}_{3}:={R}_{3}+2{R}_{1} \\  & \sim\begin{bmatrix}-1 & -4 & 0 \\ -1 & -3 & -8 \\ 2+(2)(-1) & -4+(2)(-4) & 4+(2)(0)\end{bmatrix} \\  & \sim\begin{bmatrix}-1 & -4 & 0 \\ -1 & -3 & -8 \\ 0 & -12 & 4\end{bmatrix}\end{aligned}
$$

## Variant q-10248

{"matrix": [[-1, 2, 4], [3, 5, 6], [3, -1, 9]], "source": 0, "target": 1, "k": 3, "name": "M"}

Consider the matrix $M,$ given by

$$
M=\begin{bmatrix}-1 & 2 & 4 \\ 3 & 5 & 6 \\ 3 & -1 & 9\end{bmatrix}.
$$

What matrix results from carrying out the row operation ${R}_{2}:={R}_{2}+3{R}_{1}$ on $M?$

$\begin{bmatrix}3 & 5 & 6 \\ -1 & 2 & 4 \\ 3 & -1 & 9\end{bmatrix}$

$\begin{bmatrix}-1 & 2 & 4 \\ 3 & 5 & 6 \\ 3 & -1 & 9\end{bmatrix}$

$\begin{bmatrix}-1 & 2 & 4 \\ 0 & 11 & 18 \\ 3 & -1 & 9\end{bmatrix}$ [correct]

$\begin{bmatrix}-1 & 2 & 4 \\ 0 & 5 & 6 \\ 3 & -1 & 9\end{bmatrix}$

$\begin{bmatrix}-3 & -5 & -6 \\ -1 & 2 & 4 \\ 3 & -1 & 9\end{bmatrix}$

The operation ${R}_{2}:={R}_{2}+3{R}_{1}$ means that we need to add $3$ times the first row to the second row.

Applying this row operation, we obtain the following:

$$
\begin{aligned}M & =\begin{bmatrix}-1 & 2 & 4 \\ 3 & 5 & 6 \\ 3 & -1 & 9\end{bmatrix}\,{R}_{2}:={R}_{2}+3{R}_{1} \\  & \sim\begin{bmatrix}-1 & 2 & 4 \\ 3+(3)(-1) & 5+(3)(2) & 6+(3)(4) \\ 3 & -1 & 9\end{bmatrix} \\  & \sim\begin{bmatrix}-1 & 2 & 4 \\ 0 & 11 & 18 \\ 3 & -1 & 9\end{bmatrix}\end{aligned}
$$

## Variant q-10248

{"matrix": [[-1, 2, 4], [3, 5, 6], [3, -1, 9]], "source": 0, "target": 2, "k": 3, "name": "M"}

Consider the matrix $M,$ given by

$$
M=\begin{bmatrix}-1 & 2 & 4 \\ 3 & 5 & 6 \\ 3 & -1 & 9\end{bmatrix}.
$$

What matrix results from carrying out the row operation ${R}_{3}:={R}_{3}+3{R}_{1}$ on $M?$

$\begin{bmatrix}3 & -1 & 9 \\ 3 & 5 & 6 \\ -1 & 2 & 4\end{bmatrix}$

$\begin{bmatrix}-1 & 2 & 4 \\ 3 & 5 & 6 \\ 3 & -1 & 9\end{bmatrix}$

$\begin{bmatrix}-1 & 2 & 4 \\ 3 & 5 & 6 \\ 0 & 5 & 21\end{bmatrix}$ [correct]

$\begin{bmatrix}-1 & 2 & 4 \\ 3 & 5 & 6 \\ 0 & -1 & 9\end{bmatrix}$

$\begin{bmatrix}-3 & 1 & -9 \\ 3 & 5 & 6 \\ -1 & 2 & 4\end{bmatrix}$

The operation ${R}_{3}:={R}_{3}+3{R}_{1}$ means that we need to add $3$ times the first row to the third row.

Applying this row operation, we obtain the following:

$$
\begin{aligned}M & =\begin{bmatrix}-1 & 2 & 4 \\ 3 & 5 & 6 \\ 3 & -1 & 9\end{bmatrix}\,{R}_{3}:={R}_{3}+3{R}_{1} \\  & \sim\begin{bmatrix}-1 & 2 & 4 \\ 3 & 5 & 6 \\ 3+(3)(-1) & -1+(3)(2) & 9+(3)(4)\end{bmatrix} \\  & \sim\begin{bmatrix}-1 & 2 & 4 \\ 3 & 5 & 6 \\ 0 & 5 & 21\end{bmatrix}\end{aligned}
$$

## Variant q-20239

{"matrix": [[-1, 7, 6], [1, 0, 6], [2, 9, -3]], "target": 2, "source": 1, "k": -2, "name": "X"}

Consider the matrix $X,$ given by

$$
X=\begin{bmatrix}-1 & 7 & 6 \\ 1 & 0 & 6 \\ 2 & 9 & -3\end{bmatrix}.
$$

What matrix results from carrying out the row operation ${R}_{3}:={R}_{3}-2{R}_{2}$ on $X?$

$\begin{bmatrix}-1 & -2 & -6 \\ 1 & 0 & 6 \\ 2 & 9 & -3\end{bmatrix}$

$\begin{bmatrix}-1 & 7 & 6 \\ 1 & 0 & 6 \\ 0 & 9 & -15\end{bmatrix}$ [correct]

$\begin{bmatrix}2 & 9 & -3 \\ -1 & -2 & -6 \\ 1 & 0 & 6\end{bmatrix}$

$\begin{bmatrix}-1 & 7 & 6 \\ 0 & 9 & -15 \\ 1 & 0 & 6\end{bmatrix}$

$\begin{bmatrix}-1 & 9 & 6 \\ 1 & -2 & 6 \\ 2 & 5 & -3\end{bmatrix}$

The operation ${R}_{3}:={R}_{3}-2{R}_{2}$ means that we need to add $-2$ times the second row to the third row.

Applying this row operation, we obtain the following:

$$
\begin{aligned}X & =\begin{bmatrix}-1 & 7 & 6 \\ 1 & 0 & 6 \\ 2 & 9 & -3\end{bmatrix}\,{R}_{3}:={R}_{3}-2{R}_{2} \\  & \sim\begin{bmatrix}-1 & 7 & 6 \\ 1 & 0 & 6 \\ 2+(-2)(1) & 9+(-2)(0) & -3+(-2)(6)\end{bmatrix} \\  & \sim\begin{bmatrix}-1 & 7 & 6 \\ 1 & 0 & 6 \\ 0 & 9 & -15\end{bmatrix}\end{aligned}
$$

## Variant q-20239

{"matrix": [[1, 6, 5], [6, 3, -3], [4, 6, -9]], "target": 2, "source": 0, "k": -4, "name": "X"}

Consider the matrix $X,$ given by

$$
X=\begin{bmatrix}1 & 6 & 5 \\ 6 & 3 & -3 \\ 4 & 6 & -9\end{bmatrix}.
$$

What matrix results from carrying out the row operation ${R}_{3}:={R}_{3}-4{R}_{1}$ on $X?$

$\begin{bmatrix}0 & -18 & -29 \\ 6 & 3 & -3 \\ 1 & 6 & 5\end{bmatrix}$

$\begin{bmatrix}1 & 6 & 5 \\ 6 & 3 & -3 \\ 0 & -18 & -29\end{bmatrix}$ [correct]

$\begin{bmatrix}1 & 6 & 5 \\ -1 & -4 & -5 \\ 4 & 6 & -9\end{bmatrix}$

$\begin{bmatrix}1 & 2 & 5 \\ 6 & -21 & -3 \\ 4 & -10 & -9\end{bmatrix}$

$\begin{bmatrix}-1 & -4 & -5 \\ 4 & 6 & -9 \\ 1 & 6 & 5\end{bmatrix}$

The operation ${R}_{3}:={R}_{3}-4{R}_{1}$ means that we need to add $-4$ times the first row to the third row.

Applying this row operation, we obtain the following:

$$
\begin{aligned}X & =\begin{bmatrix}1 & 6 & 5 \\ 6 & 3 & -3 \\ 4 & 6 & -9\end{bmatrix}\,{R}_{3}:={R}_{3}-4{R}_{1} \\  & \sim\begin{bmatrix}1 & 6 & 5 \\ 6 & 3 & -3 \\ 4+(-4)(1) & 6+(-4)(6) & -9+(-4)(5)\end{bmatrix} \\  & \sim\begin{bmatrix}1 & 6 & 5 \\ 6 & 3 & -3 \\ 0 & -18 & -29\end{bmatrix}\end{aligned}
$$

## Variant q-20239

{"matrix": [[1, -4, 0], [-1, -3, -8], [2, -4, 4]], "target": 2, "source": 0, "k": -2, "name": "X"}

Consider the matrix $X,$ given by

$$
X=\begin{bmatrix}1 & -4 & 0 \\ -1 & -3 & -8 \\ 2 & -4 & 4\end{bmatrix}.
$$

What matrix results from carrying out the row operation ${R}_{3}:={R}_{3}-2{R}_{1}$ on $X?$

$\begin{bmatrix}1 & -4 & 0 \\ -1 & -3 & -8 \\ 0 & 4 & 4\end{bmatrix}$ [correct]

$\begin{bmatrix}0 & 4 & 4 \\ -1 & -3 & -8 \\ 1 & -4 & 0\end{bmatrix}$

$\begin{bmatrix}1 & -6 & 0 \\ -1 & -1 & -8 \\ 2 & -8 & 4\end{bmatrix}$

$\begin{bmatrix}1 & -4 & 0 \\ -1 & -2 & 0 \\ 2 & -4 & 4\end{bmatrix}$

$\begin{bmatrix}-1 & -2 & 0 \\ 2 & -4 & 4 \\ 1 & -4 & 0\end{bmatrix}$

The operation ${R}_{3}:={R}_{3}-2{R}_{1}$ means that we need to add $-2$ times the first row to the third row.

Applying this row operation, we obtain the following:

$$
\begin{aligned}X & =\begin{bmatrix}1 & -4 & 0 \\ -1 & -3 & -8 \\ 2 & -4 & 4\end{bmatrix}\,{R}_{3}:={R}_{3}-2{R}_{1} \\  & \sim\begin{bmatrix}1 & -4 & 0 \\ -1 & -3 & -8 \\ 2+(-2)(1) & -4+(-2)(-4) & 4+(-2)(0)\end{bmatrix} \\  & \sim\begin{bmatrix}1 & -4 & 0 \\ -1 & -3 & -8 \\ 0 & 4 & 4\end{bmatrix}\end{aligned}
$$

## Variant q-20239

{"matrix": [[1, 2, 1], [3, -1, 1], [3, 3, 2]], "source": 0, "target": 1, "k": -3, "name": "X"}

Consider the matrix $X,$ given by

$$
X=\begin{bmatrix}1 & 2 & 1 \\ 3 & -1 & 1 \\ 3 & 3 & 2\end{bmatrix}.
$$

What matrix results from carrying out the row operation ${R}_{2}:={R}_{2}-3{R}_{1}$ on $X?$

$\begin{bmatrix}1 & 2 & 1 \\ 3 & -1 & 1 \\ -1 & -3 & -1\end{bmatrix}$

$\begin{bmatrix}0 & -7 & -2 \\ 1 & 2 & 1 \\ 3 & 3 & 2\end{bmatrix}$

$\begin{bmatrix}1 & 2 & 1 \\ 0 & -7 & -2 \\ 3 & 3 & 2\end{bmatrix}$ [correct]

$\begin{bmatrix}1 & -1 & 1 \\ 3 & -10 & 1 \\ 3 & -6 & 2\end{bmatrix}$

$\begin{bmatrix}-1 & -3 & -1 \\ 1 & 2 & 1 \\ 3 & -1 & 1\end{bmatrix}$

The operation ${R}_{2}:={R}_{2}-3{R}_{1}$ means that we need to add $-3$ times the first row to the second row.

Applying this row operation, we obtain the following:

$$
\begin{aligned}X & =\begin{bmatrix}1 & 2 & 1 \\ 3 & -1 & 1 \\ 3 & 3 & 2\end{bmatrix}\,{R}_{2}:={R}_{2}-3{R}_{1} \\  & \sim\begin{bmatrix}1 & 2 & 1 \\ 3+(-3)(1) & -1+(-3)(2) & 1+(-3)(1) \\ 3 & 3 & 2\end{bmatrix} \\  & \sim\begin{bmatrix}1 & 2 & 1 \\ 0 & -7 & -2 \\ 3 & 3 & 2\end{bmatrix}\end{aligned}
$$

## Variant q-20239

{"matrix": [[1, 2, 1], [3, -1, 1], [3, 3, 2]], "source": 0, "target": 2, "k": -3, "name": "X"}

Consider the matrix $X,$ given by

$$
X=\begin{bmatrix}1 & 2 & 1 \\ 3 & -1 & 1 \\ 3 & 3 & 2\end{bmatrix}.
$$

What matrix results from carrying out the row operation ${R}_{3}:={R}_{3}-3{R}_{1}$ on $X?$

$\begin{bmatrix}1 & 2 & 1 \\ -1 & -3 & -1 \\ 3 & 3 & 2\end{bmatrix}$

$\begin{bmatrix}0 & -3 & -1 \\ 3 & -1 & 1 \\ 1 & 2 & 1\end{bmatrix}$

$\begin{bmatrix}1 & 2 & 1 \\ 3 & -1 & 1 \\ 0 & -3 & -1\end{bmatrix}$ [correct]

$\begin{bmatrix}1 & -1 & 1 \\ 3 & -10 & 1 \\ 3 & -6 & 2\end{bmatrix}$

$\begin{bmatrix}-1 & -3 & -1 \\ 3 & 3 & 2 \\ 1 & 2 & 1\end{bmatrix}$

The operation ${R}_{3}:={R}_{3}-3{R}_{1}$ means that we need to add $-3$ times the first row to the third row.

Applying this row operation, we obtain the following:

$$
\begin{aligned}X & =\begin{bmatrix}1 & 2 & 1 \\ 3 & -1 & 1 \\ 3 & 3 & 2\end{bmatrix}\,{R}_{3}:={R}_{3}-3{R}_{1} \\  & \sim\begin{bmatrix}1 & 2 & 1 \\ 3 & -1 & 1 \\ 3+(-3)(1) & 3+(-3)(2) & 2+(-3)(1)\end{bmatrix} \\  & \sim\begin{bmatrix}1 & 2 & 1 \\ 3 & -1 & 1 \\ 0 & -3 & -1\end{bmatrix}\end{aligned}
$$
