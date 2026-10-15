# Original and generated pivot-column questions

## q-35457

Original:

Determine the number of pivot columns of the matrix $B,$ given by

$$
B=\begin{bmatrix}3 & 0 & 0 & 0 & 0 \\ 0 & 0 & 2 & 0 & -3 \\ 0 & 0 & 10 & 3 & -9 \\ 0 & 0 & 0 & 1 & 2\end{bmatrix}.
$$

First, we need to convert $B$ to row echelon form:

$$
\begin{aligned}B & =\begin{bmatrix}3 & 0 & 0 & 0 & 0 \\ 0 & 0 & 2 & 0 & -3 \\ 0 & 0 & 10 & 3 & -9 \\ 0 & 0 & 0 & 1 & 2\end{bmatrix} & {R}_{3} & :={R}_{3}+(-5){R}_{2} \\  & ∼\begin{bmatrix}3 & 0 & 0 & 0 & 0 \\ 0 & 0 & 2 & 0 & -3 \\ 0 & 0 & 0 & 3 & 6 \\ 0 & 0 & 0 & 1 & 2\end{bmatrix} & {R}_{4} & :={R}_{4}+(-\frac{1}{3}){R}_{3} \\  & ∼\begin{bmatrix}3 & 0 & 0 & 0 & 0 \\ 0 & 0 & 2 & 0 & -3 \\ 0 & 0 & 0 & 3 & 6 \\ 0 & 0 & 0 & 0 & 0\end{bmatrix}\end{aligned}
$$

Looking at the row echelon form, we see that $A$ has $3$ pivots, and therefore the number of pivot columns is $3.$

Variant:

Determine the number of pivot columns of the matrix $B,$ given by

$$
B=\begin{bmatrix}12 & 0 & 0 & 0 & 0 \\ 0 & 0 & -8 & 0 & -6 \\ 0 & 0 & 20 & 3 & 9 \\ 0 & 0 & 0 & 2 & -4\end{bmatrix}.
$$

First, we need to convert $B$ to row echelon form:

$$
\begin{aligned}B & =\begin{bmatrix}12 & 0 & 0 & 0 & 0 \\ 0 & 0 & -8 & 0 & -6 \\ 0 & 0 & 20 & 3 & 9 \\ 0 & 0 & 0 & 2 & -4\end{bmatrix} & {R}_{3} & :={R}_{3}+(\frac{5}{2}){R}_{2} \\  & ∼\begin{bmatrix}12 & 0 & 0 & 0 & 0 \\ 0 & 0 & -8 & 0 & -6 \\ 0 & 0 & 0 & 3 & -6 \\ 0 & 0 & 0 & 2 & -4\end{bmatrix} & {R}_{4} & :={R}_{4}+(- \frac{2}{3}){R}_{3} \\  & ∼\begin{bmatrix}12 & 0 & 0 & 0 & 0 \\ 0 & 0 & -8 & 0 & -6 \\ 0 & 0 & 0 & 3 & -6 \\ 0 & 0 & 0 & 0 & 0\end{bmatrix}\end{aligned}
$$

Looking at the row echelon form, we see that $B$ has $3$ pivots, and therefore the number of pivot columns is $3.$

## q-130957

Original:

Determine the number of pivot columns of the matrix $B,$ given by

$$
B=\begin{bmatrix}1 & 0 & 0 & -1 & 0 \\ 3 & 0 & 2 & -1 & 1 \\ 0 & 0 & -4 & 0 & 0\end{bmatrix}.
$$

First, we need to convert $B$ to row echelon form:

$$
\begin{aligned}B & =\begin{bmatrix}1 & 0 & 0 & -1 & 0 \\ 3 & 0 & 2 & -1 & 1 \\ 0 & 0 & -4 & 0 & 0\end{bmatrix} & {R}_{2} & :={R}_{2}+(-3){R}_{1} \\  & ∼\begin{bmatrix}1 & 0 & 0 & -1 & 0 \\ 0 & 0 & 2 & 2 & 1 \\ 0 & 0 & -4 & 0 & 0\end{bmatrix} & {R}_{3} & :={R}_{3}+2{R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 0 & -1 & 0 \\ 0 & 0 & 2 & 2 & 1 \\ 0 & 0 & 0 & 4 & 2\end{bmatrix}\end{aligned}
$$

Looking at the row echelon form, we see that $A$ has $3$ pivots, and therefore the number of pivot columns is $3.$

Variant:

Determine the number of pivot columns of the matrix $B,$ given by

$$
B=\begin{bmatrix}4 & 0 & 0 & -4 & 0 \\ -12 & 0 & -4 & 4 & -2 \\ 0 & 0 & -4 & 0 & 0\end{bmatrix}.
$$

First, we need to convert $B$ to row echelon form:

$$
\begin{aligned}B & =\begin{bmatrix}4 & 0 & 0 & -4 & 0 \\ -12 & 0 & -4 & 4 & -2 \\ 0 & 0 & -4 & 0 & 0\end{bmatrix} & {R}_{2} & :={R}_{2}+(3){R}_{1} \\  & ∼\begin{bmatrix}4 & 0 & 0 & -4 & 0 \\ 0 & 0 & -4 & -8 & -2 \\ 0 & 0 & -4 & 0 & 0\end{bmatrix} & {R}_{3} & :={R}_{3}+(-1){R}_{2} \\  & ∼\begin{bmatrix}4 & 0 & 0 & -4 & 0 \\ 0 & 0 & -4 & -8 & -2 \\ 0 & 0 & 0 & 8 & 2\end{bmatrix}\end{aligned}
$$

Looking at the row echelon form, we see that $B$ has $3$ pivots, and therefore the number of pivot columns is $3.$

## q-130958

Original:

Determine the number of pivot columns of the matrix $D,$ given by

$$
D=\begin{bmatrix}0 & 1 & 0 & 0 & 1 & 2 \\ 0 & 0 & -3 & 7 & 0 & 1 \\ 0 & 2 & 0 & 0 & -2 & 0\end{bmatrix}.
$$

First, we need to convert $D$ to row echelon form:

$$
\begin{aligned}D & =\begin{bmatrix}0 & 1 & 0 & 0 & 1 & 2 \\ 0 & 0 & -3 & 7 & 0 & 1 \\ 0 & 2 & 0 & 0 & -2 & 0\end{bmatrix} & {R}_{3} & :={R}_{3}+(-2){R}_{1} \\  & ∼\begin{bmatrix}0 & 1 & 0 & 0 & 1 & 2 \\ 0 & 0 & -3 & 7 & 0 & 1 \\ 0 & 0 & 0 & 0 & -4 & -4\end{bmatrix}\end{aligned}
$$

Looking at the row echelon form, we see that $D$ has $3$ pivots, and therefore the number of pivot columns is $3.$

Variant:

Determine the number of pivot columns of the matrix $D,$ given by

$$
D=\begin{bmatrix}0 & 4 & 0 & 0 & 2 & -4 \\ 0 & 0 & 6 & -28 & 0 & 2 \\ 0 & 4 & 0 & 0 & -2 & 0\end{bmatrix}.
$$

First, we need to convert $D$ to row echelon form:

$$
\begin{aligned}D & =\begin{bmatrix}0 & 4 & 0 & 0 & 2 & -4 \\ 0 & 0 & 6 & -28 & 0 & 2 \\ 0 & 4 & 0 & 0 & -2 & 0\end{bmatrix} & {R}_{3} & :={R}_{3}+(-1){R}_{1} \\  & ∼\begin{bmatrix}0 & 4 & 0 & 0 & 2 & -4 \\ 0 & 0 & 6 & -28 & 0 & 2 \\ 0 & 0 & 0 & 0 & -4 & 4\end{bmatrix}\end{aligned}
$$

Looking at the row echelon form, we see that $D$ has $3$ pivots, and therefore the number of pivot columns is $3.$

## q-130959

Original:

Determine the number of pivot columns of the matrix $C,$ given by

$$
C=\begin{bmatrix}-2 & 1 & 3 & 1 & 0 \\ 2 & 0 & -3 & 0 & -1 \\ 0 & 1 & 0 & 4 & 0\end{bmatrix}.
$$

First, we need to convert $C$ to row echelon form:

$$
\begin{aligned}C & =\begin{bmatrix}-2 & 1 & 3 & 1 & 0 \\ 2 & 0 & -3 & 0 & -1 \\ 0 & 1 & 0 & 4 & 0\end{bmatrix} & {R}_{2} & :={R}_{2}+{R}_{1} \\  & ∼\begin{bmatrix}-2 & 1 & 3 & 1 & 0 \\ 0 & 1 & 0 & 1 & -1 \\ 0 & 1 & 0 & 4 & 0\end{bmatrix} & {R}_{3} & :={R}_{3}-{R}_{2} \\  & ∼\begin{bmatrix}-2 & 1 & 3 & 1 & 0 \\ 0 & 1 & 0 & 1 & -1 \\ 0 & 0 & 0 & 3 & 1\end{bmatrix}\end{aligned}
$$

Looking at the row echelon form, we see that $C$ has $3$ pivots, and therefore the number of pivot columns is $3.$

Variant:

Determine the number of pivot columns of the matrix $C,$ given by

$$
C=\begin{bmatrix}-8 & 4 & 6 & 4 & 0 \\ -8 & 0 & 6 & 0 & 2 \\ 0 & 2 & 0 & 8 & 0\end{bmatrix}.
$$

First, we need to convert $C$ to row echelon form:

$$
\begin{aligned}C & =\begin{bmatrix}-8 & 4 & 6 & 4 & 0 \\ -8 & 0 & 6 & 0 & 2 \\ 0 & 2 & 0 & 8 & 0\end{bmatrix} & {R}_{2} & :={R}_{2}+(-1){R}_{1} \\  & ∼\begin{bmatrix}-8 & 4 & 6 & 4 & 0 \\ 0 & -4 & 0 & -4 & 2 \\ 0 & 2 & 0 & 8 & 0\end{bmatrix} & {R}_{3} & :={R}_{3}+(\frac{1}{2}){R}_{2} \\  & ∼\begin{bmatrix}-8 & 4 & 6 & 4 & 0 \\ 0 & -4 & 0 & -4 & 2 \\ 0 & 0 & 0 & 6 & 1\end{bmatrix}\end{aligned}
$$

Looking at the row echelon form, we see that $C$ has $3$ pivots, and therefore the number of pivot columns is $3.$

## q-130962

Original:

Determine the number of pivot columns of the matrix $Q,$ given by

$$
Q=\begin{bmatrix}0 & 2 & -3 & 0 & -1 & 0 \\ 0 & 2 & -1 & 0 & 0 & 2 \\ 0 & 0 & 0 & 0 & 3 & 1 \\ 0 & 0 & 0 & 0 & -6 & 0\end{bmatrix}.
$$

First, we need to convert $Q$ to row echelon form:

$$
\begin{aligned}Q & =\begin{bmatrix}0 & 2 & -3 & 0 & -1 & 0 \\ 0 & 2 & -1 & 0 & 0 & 2 \\ 0 & 0 & 0 & 0 & 3 & 1 \\ 0 & 0 & 0 & 0 & -6 & 0\end{bmatrix} & {R}_{2} & :={R}_{2}-{R}_{1} \\  & ∼\begin{bmatrix}0 & 2 & -3 & 0 & -1 & 0 \\ 0 & 0 & 2 & 0 & 1 & 2 \\ 0 & 0 & 0 & 0 & 3 & 1 \\ 0 & 0 & 0 & 0 & -6 & 0\end{bmatrix} & {R}_{4} & :={R}_{4}+2{R}_{3} \\  & ∼\begin{bmatrix}0 & 2 & -3 & 0 & -1 & 0 \\ 0 & 0 & 2 & 0 & 1 & 2 \\ 0 & 0 & 0 & 0 & 3 & 1 \\ 0 & 0 & 0 & 0 & 0 & 2\end{bmatrix}\end{aligned}
$$

Looking at the row echelon form, we see that $Q$ has $4$ pivots, and therefore the number of pivot columns is $4.$

Variant:

Determine the number of pivot columns of the matrix $Q,$ given by

$$
Q=\begin{bmatrix}0 & 4 & -12 & 0 & 2 & 0 \\ 0 & -4 & 4 & 0 & 0 & 4 \\ 0 & 0 & 0 & 0 & -3 & -1 \\ 0 & 0 & 0 & 0 & 12 & 0\end{bmatrix}.
$$

First, we need to convert $Q$ to row echelon form:

$$
\begin{aligned}Q & =\begin{bmatrix}0 & 4 & -12 & 0 & 2 & 0 \\ 0 & -4 & 4 & 0 & 0 & 4 \\ 0 & 0 & 0 & 0 & -3 & -1 \\ 0 & 0 & 0 & 0 & 12 & 0\end{bmatrix} & {R}_{2} & :={R}_{2}+(1){R}_{1} \\  & ∼\begin{bmatrix}0 & 4 & -12 & 0 & 2 & 0 \\ 0 & 0 & -8 & 0 & 2 & 4 \\ 0 & 0 & 0 & 0 & -3 & -1 \\ 0 & 0 & 0 & 0 & 12 & 0\end{bmatrix} & {R}_{4} & :={R}_{4}+(4){R}_{3} \\  & ∼\begin{bmatrix}0 & 4 & -12 & 0 & 2 & 0 \\ 0 & 0 & -8 & 0 & 2 & 4 \\ 0 & 0 & 0 & 0 & -3 & -1 \\ 0 & 0 & 0 & 0 & 0 & -4\end{bmatrix}\end{aligned}
$$

Looking at the row echelon form, we see that $Q$ has $4$ pivots, and therefore the number of pivot columns is $4.$

## q-130963

Original:

Determine the number of pivot columns of the matrix $B,$ given by

$$
B=\begin{bmatrix}3 & -1 & 5 & 0 & 7 & 1 \\ 0 & 1 & 0 & -1 & 1 & 0 \\ 0 & -4 & 0 & 0 & -1 & 2 \\ 0 & 0 & 0 & 4 & 0 & 7\end{bmatrix}.
$$

First, we need to convert $B$ to row echelon form:

$$
\begin{aligned}B & =\begin{bmatrix}3 & -1 & 5 & 0 & 7 & 1 \\ 0 & 1 & 0 & -1 & 1 & 0 \\ 0 & -4 & 0 & 0 & -1 & 2 \\ 0 & 0 & 0 & 4 & 0 & 7\end{bmatrix} & {R}_{3} & :={R}_{3}+4{R}_{2} \\  & ∼\begin{bmatrix}3 & -1 & 5 & 0 & 7 & 1 \\ 0 & 1 & 0 & -1 & 1 & 0 \\ 0 & 0 & 0 & -4 & 3 & 2 \\ 0 & 0 & 0 & 4 & 0 & 7\end{bmatrix} & {R}_{4} & :={R}_{4}+{R}_{3} \\  & ∼\begin{bmatrix}3 & -1 & 5 & 0 & 7 & 1 \\ 0 & 1 & 0 & -1 & 1 & 0 \\ 0 & 0 & 0 & -4 & 3 & 2 \\ 0 & 0 & 0 & 0 & 3 & 9\end{bmatrix}\end{aligned}
$$

Looking at the row echelon form, we see that $A$ has $4$ pivots, and therefore the number of pivot columns is $4.$

Variant:

Determine the number of pivot columns of the matrix $B,$ given by

$$
B=\begin{bmatrix}12 & -2 & 20 & 0 & -14 & -2 \\ 0 & -2 & 0 & 2 & 2 & 0 \\ 0 & -4 & 0 & 0 & 1 & -2 \\ 0 & 0 & 0 & 8 & 0 & -14\end{bmatrix}.
$$

First, we need to convert $B$ to row echelon form:

$$
\begin{aligned}B & =\begin{bmatrix}12 & -2 & 20 & 0 & -14 & -2 \\ 0 & -2 & 0 & 2 & 2 & 0 \\ 0 & -4 & 0 & 0 & 1 & -2 \\ 0 & 0 & 0 & 8 & 0 & -14\end{bmatrix} & {R}_{3} & :={R}_{3}+(-2){R}_{2} \\  & ∼\begin{bmatrix}12 & -2 & 20 & 0 & -14 & -2 \\ 0 & -2 & 0 & 2 & 2 & 0 \\ 0 & 0 & 0 & -4 & -3 & -2 \\ 0 & 0 & 0 & 8 & 0 & -14\end{bmatrix} & {R}_{4} & :={R}_{4}+(2){R}_{3} \\  & ∼\begin{bmatrix}12 & -2 & 20 & 0 & -14 & -2 \\ 0 & -2 & 0 & 2 & 2 & 0 \\ 0 & 0 & 0 & -4 & -3 & -2 \\ 0 & 0 & 0 & 0 & -6 & -18\end{bmatrix}\end{aligned}
$$

Looking at the row echelon form, we see that $B$ has $4$ pivots, and therefore the number of pivot columns is $4.$

## q-35452

Original:

Determine the number of pivot columns of the matrix $D,$ given by

$$
D=\begin{bmatrix}1 & 0 & 0 & 4 & -7 & 5 \\ 0 & 0 & 2 & 3 & 1 & 0 \\ 5 & 0 & 0 & 20 & -35 & 24\end{bmatrix}.
$$

First, we need to convert $D$ to row echelon form:

$$
\begin{aligned}D & =\begin{bmatrix}1 & 0 & 0 & 4 & -7 & 5 \\ 0 & 0 & 2 & 3 & 1 & 0 \\ 5 & 0 & 0 & 20 & -35 & 24\end{bmatrix} & {R}_{3} & :={R}_{3}+(-5){R}_{1} \\  & ∼\begin{bmatrix}1 & 0 & 0 & 4 & -7 & 5 \\ 0 & 0 & 2 & 3 & 1 & 0 \\ 0 & 0 & 0 & 0 & 0 & -1\end{bmatrix}\end{aligned}
$$

Looking at the row echelon form, we see that $D$ has $3$ pivots, and therefore the number of pivot columns is $3.$

Variant:

Determine the number of pivot columns of the matrix $D,$ given by

$$
D=\begin{bmatrix}4 & 0 & 0 & 16 & -14 & -10 \\ 0 & 0 & -4 & -12 & -2 & 0 \\ 10 & 0 & 0 & 40 & -35 & -24\end{bmatrix}.
$$

First, we need to convert $D$ to row echelon form:

$$
\begin{aligned}D & =\begin{bmatrix}4 & 0 & 0 & 16 & -14 & -10 \\ 0 & 0 & -4 & -12 & -2 & 0 \\ 10 & 0 & 0 & 40 & -35 & -24\end{bmatrix} & {R}_{3} & :={R}_{3}+(- \frac{5}{2}){R}_{1} \\  & ∼\begin{bmatrix}4 & 0 & 0 & 16 & -14 & -10 \\ 0 & 0 & -4 & -12 & -2 & 0 \\ 0 & 0 & 0 & 0 & 0 & 1\end{bmatrix}\end{aligned}
$$

Looking at the row echelon form, we see that $D$ has $3$ pivots, and therefore the number of pivot columns is $3.$

## q-35453

Original:

Determine the number of pivot columns of the matrix $B,$ given by

$$
B=\begin{bmatrix}-2 & 0 & 0 & 0 & 0 \\ 0 & 1 & 4 & -2 & 0 \\ 0 & -3 & -6 & 4 & 2 \\ 0 & 0 & -3 & 1 & -1\end{bmatrix}.
$$

First, we need to convert $B$ to row echelon form:

$$
\begin{aligned}B & =\begin{bmatrix}-2 & 0 & 0 & 0 & 0 \\ 0 & 1 & 4 & -2 & 0 \\ 0 & -3 & -6 & 4 & 2 \\ 0 & 0 & -3 & 1 & -1\end{bmatrix} & {R}_{3} & :={R}_{3}+3{R}_{2} \\  & ∼\begin{bmatrix}-2 & 0 & 0 & 0 & 0 \\ 0 & 1 & 4 & -2 & 0 \\ 0 & 0 & 6 & -2 & 2 \\ 0 & 0 & -3 & 1 & -1\end{bmatrix} & {R}_{4} & :={R}_{4}+\frac{1}{2}{R}_{3} \\  & ∼\begin{bmatrix}-2 & 0 & 0 & 0 & 0 \\ 0 & 1 & 4 & -2 & 0 \\ 0 & 0 & 6 & -2 & 2 \\ 0 & 0 & 0 & 0 & 0\end{bmatrix}\end{aligned}
$$

Looking at the row echelon form, we see that $B$ has $3$ pivots, and therefore the number of pivot columns is $3.$

Variant:

Determine the number of pivot columns of the matrix $B,$ given by

$$
B=\begin{bmatrix}-8 & 0 & 0 & 0 & 0 \\ 0 & -2 & -16 & 4 & 0 \\ 0 & -3 & -12 & 4 & -2 \\ 0 & 0 & -12 & 2 & 2\end{bmatrix}.
$$

First, we need to convert $B$ to row echelon form:

$$
\begin{aligned}B & =\begin{bmatrix}-8 & 0 & 0 & 0 & 0 \\ 0 & -2 & -16 & 4 & 0 \\ 0 & -3 & -12 & 4 & -2 \\ 0 & 0 & -12 & 2 & 2\end{bmatrix} & {R}_{3} & :={R}_{3}+(- \frac{3}{2}){R}_{2} \\  & ∼\begin{bmatrix}-8 & 0 & 0 & 0 & 0 \\ 0 & -2 & -16 & 4 & 0 \\ 0 & 0 & 12 & -2 & -2 \\ 0 & 0 & -12 & 2 & 2\end{bmatrix} & {R}_{4} & :={R}_{4}+(1){R}_{3} \\  & ∼\begin{bmatrix}-8 & 0 & 0 & 0 & 0 \\ 0 & -2 & -16 & 4 & 0 \\ 0 & 0 & 12 & -2 & -2 \\ 0 & 0 & 0 & 0 & 0\end{bmatrix}\end{aligned}
$$

Looking at the row echelon form, we see that $B$ has $3$ pivots, and therefore the number of pivot columns is $3.$

## q-73625

Original:

Determine the number of pivot columns of the matrix $D,$ given by

$$
D=\begin{bmatrix}0 & -2 & 1 & 0 & 0 \\ 0 & 2 & 1 & -1 & 2 \\ 0 & -4 & 2 & 8 & 1\end{bmatrix}.
$$

First, we need to convert $D$ to row echelon form:

$$
\begin{aligned}D & =\begin{bmatrix}0 & -2 & 1 & 0 & 0 \\ 0 & 2 & 1 & -1 & 2 \\ 0 & -4 & 2 & 8 & 1\end{bmatrix} & {R}_{2} & :={R}_{2}+{R}_{1} \\  & ∼\begin{bmatrix}0 & -2 & 1 & 0 & 0 \\ 0 & 0 & 2 & -1 & 2 \\ 0 & -4 & 2 & 8 & 1\end{bmatrix} & {R}_{3} & :={R}_{3}+(-2){R}_{1} \\  & ∼\begin{bmatrix}0 & -2 & 1 & 0 & 0 \\ 0 & 0 & 2 & -1 & 2 \\ 0 & 0 & 0 & 8 & 1\end{bmatrix}\end{aligned}
$$

Looking at the row echelon form, we see that $D$ has $3$ pivots, and therefore the number of pivot columns is $3.$

Variant:

Determine the number of pivot columns of the matrix $D,$ given by

$$
D=\begin{bmatrix}0 & -8 & 2 & 0 & 0 \\ 0 & -8 & -2 & 4 & -4 \\ 0 & -8 & 2 & 16 & 1\end{bmatrix}.
$$

First, we need to convert $D$ to row echelon form:

$$
\begin{aligned}D & =\begin{bmatrix}0 & -8 & 2 & 0 & 0 \\ 0 & -8 & -2 & 4 & -4 \\ 0 & -8 & 2 & 16 & 1\end{bmatrix} & {R}_{2} & :={R}_{2}+(-1){R}_{1} \\  & ∼\begin{bmatrix}0 & -8 & 2 & 0 & 0 \\ 0 & 0 & -4 & 4 & -4 \\ 0 & -8 & 2 & 16 & 1\end{bmatrix} & {R}_{3} & :={R}_{3}+(-1){R}_{1} \\  & ∼\begin{bmatrix}0 & -8 & 2 & 0 & 0 \\ 0 & 0 & -4 & 4 & -4 \\ 0 & 0 & 0 & 16 & 1\end{bmatrix}\end{aligned}
$$

Looking at the row echelon form, we see that $D$ has $3$ pivots, and therefore the number of pivot columns is $3.$

## q-73628

Original:

Determine the number of pivot columns of the matrix $B,$ given by

$$
B=\begin{bmatrix}-2 & 0 & 1 & -1 & -2 \\ 0 & 1 & 1 & 4 & -5 \\ 4 & 0 & 3 & -6 & 1 \\ 0 & 0 & 0 & 7 & 0\end{bmatrix}.
$$

First, we need to convert $B$ to row echelon form:

$$
\begin{aligned}B & =\begin{bmatrix}-2 & 0 & 1 & -1 & -2 \\ 0 & 1 & 1 & 4 & -5 \\ 4 & 0 & 3 & -6 & 1 \\ 0 & 0 & 0 & 7 & 0\end{bmatrix} & {R}_{3} & :={R}_{3}+2{R}_{1} \\  & ∼\begin{bmatrix}-2 & 0 & 1 & -1 & -2 \\ 0 & 1 & 1 & 4 & -5 \\ 0 & 0 & 5 & -8 & -3 \\ 0 & 0 & 0 & 7 & 0\end{bmatrix}\end{aligned}
$$

Looking at the row echelon form, we see that $B$ has $4$ pivots, and therefore the number of pivot columns is $4.$

Variant:

Determine the number of pivot columns of the matrix $B,$ given by

$$
B=\begin{bmatrix}-8 & 0 & 4 & -2 & 4 \\ 0 & -2 & -4 & -8 & -10 \\ 8 & 0 & 6 & -6 & -1 \\ 0 & 0 & 0 & 14 & 0\end{bmatrix}.
$$

First, we need to convert $B$ to row echelon form:

$$
\begin{aligned}B & =\begin{bmatrix}-8 & 0 & 4 & -2 & 4 \\ 0 & -2 & -4 & -8 & -10 \\ 8 & 0 & 6 & -6 & -1 \\ 0 & 0 & 0 & 14 & 0\end{bmatrix} & {R}_{3} & :={R}_{3}+(1){R}_{1} \\  & ∼\begin{bmatrix}-8 & 0 & 4 & -2 & 4 \\ 0 & -2 & -4 & -8 & -10 \\ 0 & 0 & 10 & -8 & 3 \\ 0 & 0 & 0 & 14 & 0\end{bmatrix}\end{aligned}
$$

Looking at the row echelon form, we see that $B$ has $4$ pivots, and therefore the number of pivot columns is $4.$

## q-73630

Original:

Determine the number of pivot columns of the matrix $C,$ given by

$$
C=\begin{bmatrix}1 & 2 & -1 & 1 & 4 \\ 0 & 0 & 8 & 0 & -2 \\ 0 & 0 & -4 & 1 & 0 \\ 0 & 0 & 0 & 0 & -1\end{bmatrix}.
$$

First, we need to convert $C$ to row echelon form:

$$
\begin{aligned}C & =\begin{bmatrix}1 & 2 & -1 & 1 & 4 \\ 0 & 0 & 8 & 0 & -2 \\ 0 & 0 & -4 & 1 & 0 \\ 0 & 0 & 0 & 0 & -1\end{bmatrix} & {R}_{3} & :={R}_{3}+\frac{1}{2}{R}_{2} \\  & ∼\begin{bmatrix}1 & 2 & -1 & 1 & 4 \\ 0 & 0 & 8 & 0 & -2 \\ 0 & 0 & 0 & 1 & -1 \\ 0 & 0 & 0 & 0 & -1\end{bmatrix}\end{aligned}
$$

Looking at the row echelon form, we see that $C$ has $4$ pivots, and therefore the number of pivot columns is $4.$

Variant:

Determine the number of pivot columns of the matrix $C,$ given by

$$
C=\begin{bmatrix}4 & 4 & -4 & 2 & -8 \\ 0 & 0 & -32 & 0 & -4 \\ 0 & 0 & -8 & 1 & 0 \\ 0 & 0 & 0 & 0 & 2\end{bmatrix}.
$$

First, we need to convert $C$ to row echelon form:

$$
\begin{aligned}C & =\begin{bmatrix}4 & 4 & -4 & 2 & -8 \\ 0 & 0 & -32 & 0 & -4 \\ 0 & 0 & -8 & 1 & 0 \\ 0 & 0 & 0 & 0 & 2\end{bmatrix} & {R}_{3} & :={R}_{3}+(- \frac{1}{4}){R}_{2} \\  & ∼\begin{bmatrix}4 & 4 & -4 & 2 & -8 \\ 0 & 0 & -32 & 0 & -4 \\ 0 & 0 & 0 & 1 & 1 \\ 0 & 0 & 0 & 0 & 2\end{bmatrix}\end{aligned}
$$

Looking at the row echelon form, we see that $C$ has $4$ pivots, and therefore the number of pivot columns is $4.$

## q-73633

Original:

Determine the number of pivot columns of the matrix $P,$ given by

$$
P=\begin{bmatrix}0 & 3 & 2 & -1 & 0 \\ 0 & 0 & 6 & 1 & 3 \\ 0 & -6 & -4 & 9 & 1 \\ 0 & 0 & 0 & 0 & 0\end{bmatrix}.
$$

First, we need to convert $P$ to row echelon form:

$$
\begin{aligned}P & =\begin{bmatrix}0 & 3 & 2 & -1 & 0 \\ 0 & 0 & 6 & 1 & 3 \\ 0 & -6 & -4 & 9 & 1 \\ 0 & 0 & 0 & 0 & 0\end{bmatrix} & {R}_{3} & :={R}_{3}+2{R}_{1} \\  & ∼\begin{bmatrix}0 & 3 & 2 & -1 & 0 \\ 0 & 0 & 6 & 1 & 3 \\ 0 & 0 & 0 & 7 & 1 \\ 0 & 0 & 0 & 0 & 0\end{bmatrix}\end{aligned}
$$

Looking at the row echelon form, we see that $P$ has $3$ pivots, and therefore the number of pivot columns is $3.$

Variant:

Determine the number of pivot columns of the matrix $P,$ given by

$$
P=\begin{bmatrix}0 & 6 & 8 & -2 & 0 \\ 0 & 0 & -24 & -2 & 6 \\ 0 & -6 & -8 & 9 & -1 \\ 0 & 0 & 0 & 0 & 0\end{bmatrix}.
$$

First, we need to convert $P$ to row echelon form:

$$
\begin{aligned}P & =\begin{bmatrix}0 & 6 & 8 & -2 & 0 \\ 0 & 0 & -24 & -2 & 6 \\ 0 & -6 & -8 & 9 & -1 \\ 0 & 0 & 0 & 0 & 0\end{bmatrix} & {R}_{3} & :={R}_{3}+(1){R}_{1} \\  & ∼\begin{bmatrix}0 & 6 & 8 & -2 & 0 \\ 0 & 0 & -24 & -2 & 6 \\ 0 & 0 & 0 & 7 & -1 \\ 0 & 0 & 0 & 0 & 0\end{bmatrix}\end{aligned}
$$

Looking at the row echelon form, we see that $P$ has $3$ pivots, and therefore the number of pivot columns is $3.$

## q-73635

Original:

Determine the number of pivot columns of the matrix $Q,$ given by

$$
Q=\begin{bmatrix}-2 & 1 & 1 & 0 & 3 \\ 0 & 2 & -1 & 1 & 4 \\ 0 & 0 & 0 & 8 & -12 \\ 0 & 0 & 0 & -2 & 1 \\ 0 & 0 & 0 & 0 & 0\end{bmatrix}.
$$

First, we need to convert $Q$ to row echelon form:

$$
\begin{aligned}Q & =\begin{bmatrix}-2 & 1 & 1 & 0 & 3 \\ 0 & 2 & -1 & 1 & 4 \\ 0 & 0 & 0 & 8 & -12 \\ 0 & 0 & 0 & -2 & 1 \\ 0 & 0 & 0 & 0 & 0\end{bmatrix} & {R}_{4} & :={R}_{4}+\frac{1}{4}{R}_{3} \\  & ∼\begin{bmatrix}-2 & 1 & 1 & 0 & 3 \\ 0 & 2 & -1 & 1 & 4 \\ 0 & 0 & 0 & 8 & -12 \\ 0 & 0 & 0 & 0 & -2 \\ 0 & 0 & 0 & 0 & 0\end{bmatrix}\end{aligned}
$$

Looking at the row echelon form, we see that $Q$ has $4$ pivots, and therefore the number of pivot columns is $4.$

Variant:

Determine the number of pivot columns of the matrix $Q,$ given by

$$
Q=\begin{bmatrix}-4 & 4 & 2 & 0 & -6 \\ 0 & -8 & 2 & 2 & 8 \\ 0 & 0 & 0 & -8 & 12 \\ 0 & 0 & 0 & 4 & -2 \\ 0 & 0 & 0 & 0 & 0\end{bmatrix}.
$$

First, we need to convert $Q$ to row echelon form:

$$
\begin{aligned}Q & =\begin{bmatrix}-4 & 4 & 2 & 0 & -6 \\ 0 & -8 & 2 & 2 & 8 \\ 0 & 0 & 0 & -8 & 12 \\ 0 & 0 & 0 & 4 & -2 \\ 0 & 0 & 0 & 0 & 0\end{bmatrix} & {R}_{4} & :={R}_{4}+(\frac{1}{2}){R}_{3} \\  & ∼\begin{bmatrix}-4 & 4 & 2 & 0 & -6 \\ 0 & -8 & 2 & 2 & 8 \\ 0 & 0 & 0 & -8 & 12 \\ 0 & 0 & 0 & 0 & 4 \\ 0 & 0 & 0 & 0 & 0\end{bmatrix}\end{aligned}
$$

Looking at the row echelon form, we see that $Q$ has $4$ pivots, and therefore the number of pivot columns is $4.$

## q-130964

Original:

Determine the number of pivot columns of the matrix $D,$ given by

$$
D=\begin{bmatrix}-3 & -2 & 0 & 0 & 1 \\ 0 & 0 & -1 & 3 & 0 \\ 0 & 0 & 0 & 0 & 1 \\ 3 & 2 & 0 & 0 & -1 \\ 0 & 0 & 2 & -6 & 0\end{bmatrix}.
$$

First, we need to convert $D$ to row echelon form:

$$
\begin{aligned}D & =\begin{bmatrix}-3 & -2 & 0 & 0 & 1 \\ 0 & 0 & -1 & 3 & 0 \\ 0 & 0 & 0 & 0 & 1 \\ 3 & 2 & 0 & 0 & -1 \\ 0 & 0 & 2 & -6 & 0\end{bmatrix} & {R}_{4} & :={R}_{4}+{R}_{1} \\  & ∼\begin{bmatrix}-3 & -2 & 0 & 0 & 1 \\ 0 & 0 & -1 & 3 & 0 \\ 0 & 0 & 0 & 0 & 1 \\ 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 2 & -6 & 0\end{bmatrix} & {R}_{5} & :={R}_{5}+2{R}_{2} \\  & ∼\begin{bmatrix}-3 & -2 & 0 & 0 & 1 \\ 0 & 0 & -1 & 3 & 0 \\ 0 & 0 & 0 & 0 & 1 \\ 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0\end{bmatrix}\end{aligned}
$$

Looking at the row echelon form, we see that $D$ has $3$ pivots, and therefore the number of pivot columns is $3.$

Variant:

Determine the number of pivot columns of the matrix $D,$ given by

$$
D=\begin{bmatrix}-6 & -8 & 0 & 0 & -2 \\ 0 & 0 & 2 & 6 & 0 \\ 0 & 0 & 0 & 0 & -1 \\ 6 & 8 & 0 & 0 & 2 \\ 0 & 0 & 4 & 12 & 0\end{bmatrix}.
$$

First, we need to convert $D$ to row echelon form:

$$
\begin{aligned}D & =\begin{bmatrix}-6 & -8 & 0 & 0 & -2 \\ 0 & 0 & 2 & 6 & 0 \\ 0 & 0 & 0 & 0 & -1 \\ 6 & 8 & 0 & 0 & 2 \\ 0 & 0 & 4 & 12 & 0\end{bmatrix} & {R}_{4} & :={R}_{4}+(1){R}_{1} \\  & ∼\begin{bmatrix}-6 & -8 & 0 & 0 & -2 \\ 0 & 0 & 2 & 6 & 0 \\ 0 & 0 & 0 & 0 & -1 \\ 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 4 & 12 & 0\end{bmatrix} & {R}_{5} & :={R}_{5}+(-2){R}_{2} \\  & ∼\begin{bmatrix}-6 & -8 & 0 & 0 & -2 \\ 0 & 0 & 2 & 6 & 0 \\ 0 & 0 & 0 & 0 & -1 \\ 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0\end{bmatrix}\end{aligned}
$$

Looking at the row echelon form, we see that $D$ has $3$ pivots, and therefore the number of pivot columns is $3.$

## q-35394

Original:

Determine the number of pivot columns of the matrix $C,$ given by

$$
C=\begin{bmatrix}1 & -2 & -1 & 4 & -5 \\ 0 & -3 & 0 & 6 & 3 \\ 0 & 0 & 0 & 4 & 0 \\ 0 & -1 & 0 & 2 & 3\end{bmatrix}.
$$

First, we need to convert $C$ to row echelon form:

$$
\begin{aligned}C & =\begin{bmatrix}1 & -2 & -1 & 4 & -5 \\ 0 & -3 & 0 & 6 & 3 \\ 0 & 0 & 0 & 4 & 0 \\ 0 & -1 & 0 & 2 & 3\end{bmatrix} & {R}_{4} & :={R}_{4}+(-\frac{1}{3}){R}_{2} \\  & ∼\begin{bmatrix}1 & -2 & -1 & 4 & -5 \\ 0 & -3 & 0 & 6 & 3 \\ 0 & 0 & 0 & 4 & 0 \\ 0 & 0 & 0 & 0 & 2\end{bmatrix}\end{aligned}
$$

Looking at the row echelon form, we see that $C$ has $4$ pivots, and therefore the number of pivot columns is $4.$

Variant:

Determine the number of pivot columns of the matrix $C,$ given by

$$
C=\begin{bmatrix}4 & -4 & -4 & 8 & 10 \\ 0 & 6 & 0 & -12 & 6 \\ 0 & 0 & 0 & 4 & 0 \\ 0 & -2 & 0 & 4 & -6\end{bmatrix}.
$$

First, we need to convert $C$ to row echelon form:

$$
\begin{aligned}C & =\begin{bmatrix}4 & -4 & -4 & 8 & 10 \\ 0 & 6 & 0 & -12 & 6 \\ 0 & 0 & 0 & 4 & 0 \\ 0 & -2 & 0 & 4 & -6\end{bmatrix} & {R}_{4} & :={R}_{4}+(\frac{1}{3}){R}_{2} \\  & ∼\begin{bmatrix}4 & -4 & -4 & 8 & 10 \\ 0 & 6 & 0 & -12 & 6 \\ 0 & 0 & 0 & 4 & 0 \\ 0 & 0 & 0 & 0 & -4\end{bmatrix}\end{aligned}
$$

Looking at the row echelon form, we see that $C$ has $4$ pivots, and therefore the number of pivot columns is $4.$

## q-130961

Original:

Determine the number of pivot columns of the matrix $P,$ given by

$$
P=\begin{bmatrix}-1 & 0 & 2 & 7 & -1 \\ 0 & 3 & 0 & 1 & 2 \\ 0 & -6 & 0 & 0 & 1 \\ 0 & 0 & 0 & -2 & 0\end{bmatrix}.
$$

First, we need to convert $P$ to row echelon form:

$$
\begin{aligned}P & =\begin{bmatrix}-1 & 0 & 2 & 7 & -1 \\ 0 & 3 & 0 & 1 & 2 \\ 0 & -6 & 0 & 0 & 1 \\ 0 & 0 & 0 & -2 & 0\end{bmatrix} & {R}_{3} & :={R}_{3}+2{R}_{2} \\  & ∼\begin{bmatrix}-1 & 0 & 2 & 7 & -1 \\ 0 & 3 & 0 & 1 & 2 \\ 0 & 0 & 0 & 2 & 5 \\ 0 & 0 & 0 & -2 & 0\end{bmatrix} & {R}_{4} & :={R}_{4}+{R}_{3} \\  & ∼\begin{bmatrix}-1 & 0 & 2 & 7 & -1 \\ 0 & 3 & 0 & 1 & 2 \\ 0 & 0 & 0 & 2 & 5 \\ 0 & 0 & 0 & 0 & 5\end{bmatrix}\end{aligned}
$$

Looking at the row echelon form, we see that $P$ has $4$ pivots, and therefore the number of pivot columns is $4.$

Variant:

Determine the number of pivot columns of the matrix $P,$ given by

$$
P=\begin{bmatrix}-4 & 0 & 8 & 14 & 2 \\ 0 & -6 & 0 & -2 & 4 \\ 0 & -6 & 0 & 0 & -1 \\ 0 & 0 & 0 & -4 & 0\end{bmatrix}.
$$

First, we need to convert $P$ to row echelon form:

$$
\begin{aligned}P & =\begin{bmatrix}-4 & 0 & 8 & 14 & 2 \\ 0 & -6 & 0 & -2 & 4 \\ 0 & -6 & 0 & 0 & -1 \\ 0 & 0 & 0 & -4 & 0\end{bmatrix} & {R}_{3} & :={R}_{3}+(-1){R}_{2} \\  & ∼\begin{bmatrix}-4 & 0 & 8 & 14 & 2 \\ 0 & -6 & 0 & -2 & 4 \\ 0 & 0 & 0 & 2 & -5 \\ 0 & 0 & 0 & -4 & 0\end{bmatrix} & {R}_{4} & :={R}_{4}+(2){R}_{3} \\  & ∼\begin{bmatrix}-4 & 0 & 8 & 14 & 2 \\ 0 & -6 & 0 & -2 & 4 \\ 0 & 0 & 0 & 2 & -5 \\ 0 & 0 & 0 & 0 & -10\end{bmatrix}\end{aligned}
$$

Looking at the row echelon form, we see that $P$ has $4$ pivots, and therefore the number of pivot columns is $4.$
