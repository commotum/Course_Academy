## q-13536 original parameter replay, duplicate incomplete field excluded

Find $(A+B)-C-(B-C)$, if

$$
A=\begin{bmatrix}6 & 7 \\ 4 & 5\end{bmatrix},\,B=\begin{bmatrix}3 & 2 \\ 2 & 3\end{bmatrix},\,C=\begin{bmatrix}5 & 1 \\ 6 & 8\end{bmatrix}.
$$

- $\begin{bmatrix}0 & 0 \\ 0 & 0\end{bmatrix}$
- $\begin{bmatrix}3 & 2 \\ 2 & 3\end{bmatrix}$
- $\begin{bmatrix}5 & 7 \\ 7 & 5\end{bmatrix}$
- $\begin{bmatrix}6 & 7 \\ 4 & 5\end{bmatrix}$ (correct)
- $\begin{bmatrix}5 & 1 \\ 6 & 8\end{bmatrix}$

First, we simplify the expression by distributing the subtraction over the matrices in the parentheses:

$$
\begin{aligned}(A+B)-C-(B-C) & =A+B-C-B+C \\  & =A+\cancel{B}-\cancel{C}-\cancel{B}+\cancel{C} \\  & =A\end{aligned}
$$

We are left with a single matrix. So, the result is 

$$
\begin{aligned}A & =\begin{bmatrix}6 & 7 \\ 4 & 5\end{bmatrix}\end{aligned}
$$

---

## Same method with changed A, all canceled matrices held constant

Find $(A+B)-C-(B-C)$, if

$$
A=\begin{bmatrix}9 & 7 \\ 4 & 5\end{bmatrix},\,B=\begin{bmatrix}3 & 2 \\ 2 & 3\end{bmatrix},\,C=\begin{bmatrix}5 & 1 \\ 6 & 8\end{bmatrix}.
$$

- $\begin{bmatrix}8 & 7 \\ 7 & 5\end{bmatrix}$
- $\begin{bmatrix}3 & 2 \\ 2 & 3\end{bmatrix}$
- $\begin{bmatrix}0 & 0 \\ 0 & 0\end{bmatrix}$
- $\begin{bmatrix}5 & 1 \\ 6 & 8\end{bmatrix}$
- $\begin{bmatrix}9 & 7 \\ 4 & 5\end{bmatrix}$ (correct)

First, we simplify the expression by distributing the subtraction over the matrices in the parentheses:

$$
\begin{aligned}(A+B)-C-(B-C) & =A+B-C-B+C \\  & =A+\cancel{B}-\cancel{C}-\cancel{B}+\cancel{C} \\  & =A\end{aligned}
$$

We are left with a single matrix. So, the result is 

$$
\begin{aligned}A & =\begin{bmatrix}9 & 7 \\ 4 & 5\end{bmatrix}\end{aligned}
$$

---

## Both canceled matrices sampled within the declared numeric slots

Find $(A+B)-C-(B-C)$, if

$$
A=\begin{bmatrix}3 & 4 \\ 1 & 6\end{bmatrix},\,B=\begin{bmatrix}7 & 2 \\ 1 & 1\end{bmatrix},\,C=\begin{bmatrix}0 & 6 \\ 8 & 4\end{bmatrix}.
$$

- $\begin{bmatrix}3 & 4 \\ 1 & 6\end{bmatrix}$ (correct)
- $\begin{bmatrix}7 & 2 \\ 1 & 1\end{bmatrix}$
- $\begin{bmatrix}0 & 0 \\ 0 & 0\end{bmatrix}$
- $\begin{bmatrix}2 & 4 \\ 4 & 6\end{bmatrix}$
- $\begin{bmatrix}0 & 6 \\ 8 & 4\end{bmatrix}$

First, we simplify the expression by distributing the subtraction over the matrices in the parentheses:

$$
\begin{aligned}(A+B)-C-(B-C) & =A+B-C-B+C \\  & =A+\cancel{B}-\cancel{C}-\cancel{B}+\cancel{C} \\  & =A\end{aligned}
$$

We are left with a single matrix. So, the result is 

$$
\begin{aligned}A & =\begin{bmatrix}3 & 4 \\ 1 & 6\end{bmatrix}\end{aligned}
$$