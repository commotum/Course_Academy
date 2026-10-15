### easy_integer

Calculate $3G+3L$, where
$G=\begin{bmatrix}0 & 4 \\ 4 & 4\end{bmatrix}$
and
$L=\begin{bmatrix}4 & 3 \\ 2 & 2\end{bmatrix}.$

selection: $\begin{bmatrix}12 & 9 \\ 6 & 6\end{bmatrix}$, $\begin{bmatrix}12 & 13 \\ 10 & 10\end{bmatrix}$, $\begin{bmatrix}12 & 21 \\ 18 & 18\end{bmatrix}$, $\begin{bmatrix}-12 & 3 \\ 6 & 6\end{bmatrix}$, $\begin{bmatrix}4 & 15 \\ 14 & 14\end{bmatrix}$

We multiply each entry of $G$ by $3$ and each entry of $L$ by $3,$ and then add the resulting matrices, as follows:

$$
\begin{aligned}3G+3L & =3\begin{bmatrix}0 & 4 \\ 4 & 4\end{bmatrix}+3\begin{bmatrix}4 & 3 \\ 2 & 2\end{bmatrix} \\  & =\begin{bmatrix}3\cdot 0 & 3\cdot 4 \\ 3\cdot 4 & 3\cdot 4\end{bmatrix}+\begin{bmatrix}3\cdot 4 & 3\cdot 3 \\ 3\cdot 2 & 3\cdot 2\end{bmatrix} \\  & =\begin{bmatrix}0 & 12 \\ 12 & 12\end{bmatrix}+\begin{bmatrix}12 & 9 \\ 6 & 6\end{bmatrix} \\  & =\begin{bmatrix}0+12 & 12+9 \\ 12+6 & 12+6\end{bmatrix} \\  & =\begin{bmatrix}12 & 21 \\ 18 & 18\end{bmatrix}\end{aligned}
$$

### symmetric_plus

Calculate $2N + 6L$, where
$N = \begin{bmatrix}3 & 2 \\ 5 & 2\end{bmatrix}$
and
$L = \begin{bmatrix}3 & 0 \\ -1 & -1\end{bmatrix}$.

selection: $\begin{bmatrix}9 & 4 \\ 9 & 3\end{bmatrix}$, $\begin{bmatrix}24 & 4 \\ 4 & -2\end{bmatrix}$, $\begin{bmatrix}18 & 0 \\ -6 & -6\end{bmatrix}$, $\begin{bmatrix}21 & 2 \\ -1 & -4\end{bmatrix}$, $\begin{bmatrix}-12 & 4 \\ 16 & 10\end{bmatrix}$

We multiply each entry of $N$ by $2$ and each entry of $L$ by $6,$ and then add the resulting matrices, as follows:

$$
\begin{aligned}2N+6L & =2\begin{bmatrix}3 & 2 \\ 5 & 2\end{bmatrix}+6\begin{bmatrix}3 & 0 \\ -1 & -1\end{bmatrix} \\  & =\begin{bmatrix}2\cdot 3 & 2\cdot 2 \\ 2\cdot 5 & 2\cdot 2\end{bmatrix}+\begin{bmatrix}6\cdot 3 & 6\cdot 0 \\ 6\cdot (-1) & 6\cdot (-1)\end{bmatrix} \\  & =\begin{bmatrix}6 & 4 \\ 10 & 4\end{bmatrix}+\begin{bmatrix}18 & 0 \\ -6 & -6\end{bmatrix} \\  & =\begin{bmatrix}6+18 & 4+0 \\ 10+(-6) & 4+(-6)\end{bmatrix} \\  & =\begin{bmatrix}24 & 4 \\ 4 & -2\end{bmatrix}\end{aligned}
$$

### opaque_subtract

Calculate $2N - 6L$, where
$N = \begin{bmatrix}3 & 2 \\ 5 & 2\end{bmatrix}$
and
$L = \begin{bmatrix}3 & 0 \\ -1 & -1\end{bmatrix}$.

selection: $\begin{bmatrix}3 & 4 \\ 11 & 5\end{bmatrix}$, $\begin{bmatrix}-12 & 4 \\ 16 & 10\end{bmatrix}$, $\begin{bmatrix}-18 & 0 \\ 6 & 6\end{bmatrix}$, $\begin{bmatrix}-15 & 2 \\ 11 & 8\end{bmatrix}$, $\begin{bmatrix}24 & 4 \\ 4 & -2\end{bmatrix}$

We multiply each entry of $N$ by $2$ and each entry of $L$ by $6,$ and then subtract the resulting matrices, as follows:

$$
\begin{aligned}2N-6L & =2\begin{bmatrix}3 & 2 \\ 5 & 2\end{bmatrix}-6\begin{bmatrix}3 & 0 \\ -1 & -1\end{bmatrix} \\  & =\begin{bmatrix}2\cdot 3 & 2\cdot 2 \\ 2\cdot 5 & 2\cdot 2\end{bmatrix}-\begin{bmatrix}6\cdot 3 & 6\cdot 0 \\ 6\cdot (-1) & 6\cdot (-1)\end{bmatrix} \\  & =\begin{bmatrix}6 & 4 \\ 10 & 4\end{bmatrix}-\begin{bmatrix}18 & 0 \\ -6 & -6\end{bmatrix} \\  & =\begin{bmatrix}6-18 & 4-0 \\ 10-(-6) & 4-(-6)\end{bmatrix} \\  & =\begin{bmatrix}-12 & 4 \\ 16 & 10\end{bmatrix}\end{aligned}
$$

### subtract_square

Calculate $2N-6L$, where
$N=\begin{bmatrix}3 & 2 \\ 5 & 2\end{bmatrix}$
and
$L=\begin{bmatrix}3 & 0 \\ -1 & -1\end{bmatrix}.$

selection: $\begin{bmatrix}3 & 4 \\ 11 & 5\end{bmatrix}$, $\begin{bmatrix}-12 & 4 \\ 16 & 10\end{bmatrix}$, $\begin{bmatrix}-18 & 0 \\ 6 & 6\end{bmatrix}$, $\begin{bmatrix}-15 & 2 \\ 11 & 8\end{bmatrix}$, $\begin{bmatrix}24 & 4 \\ 4 & -2\end{bmatrix}$

We multiply each entry of $N$ by $2$ and each entry of $L$ by $6,$ and then subtract the resulting matrices, as follows:

$$
\begin{aligned}2N-6L & =2\begin{bmatrix}3 & 2 \\ 5 & 2\end{bmatrix}-6\begin{bmatrix}3 & 0 \\ -1 & -1\end{bmatrix} \\  & =\begin{bmatrix}2\cdot 3 & 2\cdot 2 \\ 2\cdot 5 & 2\cdot 2\end{bmatrix}-\begin{bmatrix}6\cdot 3 & 6\cdot 0 \\ 6\cdot (-1) & 6\cdot (-1)\end{bmatrix} \\  & =\begin{bmatrix}6 & 4 \\ 10 & 4\end{bmatrix}-\begin{bmatrix}18 & 0 \\ -6 & -6\end{bmatrix} \\  & =\begin{bmatrix}6-18 & 4-0 \\ 10-(-6) & 4-(-6)\end{bmatrix} \\  & =\begin{bmatrix}-12 & 4 \\ 16 & 10\end{bmatrix}\end{aligned}
$$

### half_plus

Calculate $2N+\frac{1}{2}L$, where
$N=\begin{bmatrix}2 & 3 \\ 2 & 5\end{bmatrix}$
and
$L=\begin{bmatrix}2 & 6 \\ 0 & -2\end{bmatrix}.$

selection: $\begin{bmatrix}5 & 9 \\ 4 & 9\end{bmatrix}$, $\begin{bmatrix}1 & 3 \\ 0 & -1\end{bmatrix}$, $\begin{bmatrix}6 & 12 \\ 4 & 8\end{bmatrix}$, $\begin{bmatrix}3 & 3 \\ 4 & 11\end{bmatrix}$, $\begin{bmatrix}3 & 6 \\ 2 & 4\end{bmatrix}$

We multiply each entry of $N$ by $2$ and each entry of $L$ by $\frac{1}{2},$ and then add the resulting matrices, as follows:

$$
\begin{aligned}2N+\frac{1}{2}L & =2\begin{bmatrix}2 & 3 \\ 2 & 5\end{bmatrix}+\frac{1}{2}\begin{bmatrix}2 & 6 \\ 0 & -2\end{bmatrix} \\  & =\begin{bmatrix}2\cdot 2 & 2\cdot 3 \\ 2\cdot 2 & 2\cdot 5\end{bmatrix}+\begin{bmatrix}\frac{1}{2}\cdot 2 & \frac{1}{2}\cdot 6 \\ \frac{1}{2}\cdot 0 & \frac{1}{2}\cdot (-2)\end{bmatrix} \\  & =\begin{bmatrix}4 & 6 \\ 4 & 10\end{bmatrix}+\begin{bmatrix}1 & 3 \\ 0 & -1\end{bmatrix} \\  & =\begin{bmatrix}4+1 & 6+3 \\ 4+0 & 10+(-1)\end{bmatrix} \\  & =\begin{bmatrix}5 & 9 \\ 4 & 9\end{bmatrix}\end{aligned}
$$

### negative_plus

Calculate $-N+6L$, where
$N=\begin{bmatrix}3 & 2 \\ 5 & 2\end{bmatrix}$
and
$L=\begin{bmatrix}3 & 0 \\ -1 & -1\end{bmatrix}.$

selection: $\begin{bmatrix}0 & -2 \\ -6 & -3\end{bmatrix}$, $\begin{bmatrix}15 & -2 \\ -11 & -8\end{bmatrix}$, $\begin{bmatrix}18 & 0 \\ -6 & -6\end{bmatrix}$, $\begin{bmatrix}21 & 2 \\ -1 & -4\end{bmatrix}$, $\begin{bmatrix}-21 & -2 \\ 1 & 4\end{bmatrix}$

We multiply each entry of $N$ by $-1$ and each entry of $L$ by $6,$ and then add the resulting matrices, as follows:

$$
\begin{aligned}-N+6L & =(-1)\begin{bmatrix}3 & 2 \\ 5 & 2\end{bmatrix}+6\begin{bmatrix}3 & 0 \\ -1 & -1\end{bmatrix} \\  & =\begin{bmatrix}(-1)\cdot 3 & (-1)\cdot 2 \\ (-1)\cdot 5 & (-1)\cdot 2\end{bmatrix}+\begin{bmatrix}6\cdot 3 & 6\cdot 0 \\ 6\cdot (-1) & 6\cdot (-1)\end{bmatrix} \\  & =\begin{bmatrix}-3 & -2 \\ -5 & -2\end{bmatrix}+\begin{bmatrix}18 & 0 \\ -6 & -6\end{bmatrix} \\  & =\begin{bmatrix}-3+18 & -2+0 \\ -5+(-6) & -2+(-6)\end{bmatrix} \\  & =\begin{bmatrix}15 & -2 \\ -11 & -8\end{bmatrix}\end{aligned}
$$

### row_blank

Calculate $2N-\frac{1}{2}L$, where
$N=\begin{bmatrix}2 & 3 & 2 & 5\end{bmatrix}$
and
$L=\begin{bmatrix}2 & 6 & 0 & -2\end{bmatrix}.$

| $2N-\frac{1}{2}L=\,\,$ |  | {{field-1}} | {{field-2}} | {{field-3}} | {{field-4}} |  |
| --- | --- | --- | --- | --- | --- | --- |

field-1: $3$

field-2: $3$

field-3: $4$

field-4: $11$

We multiply each entry of $N$ by $2$ and each entry of $L$ by $\frac{1}{2},$ and then subtract the resulting matrices, as follows:

$$
\begin{aligned}2N-\frac{1}{2}L & =2\begin{bmatrix}2 & 3 & 2 & 5\end{bmatrix}-\frac{1}{2}\begin{bmatrix}2 & 6 & 0 & -2\end{bmatrix} \\  & =\begin{bmatrix}2\cdot 2 & 2\cdot 3 & 2\cdot 2 & 2\cdot 5\end{bmatrix}-\begin{bmatrix}\frac{1}{2}\cdot 2 & \frac{1}{2}\cdot 6 & \frac{1}{2}\cdot 0 & \frac{1}{2}\cdot (-2)\end{bmatrix} \\  & =\begin{bmatrix}4 & 6 & 4 & 10\end{bmatrix}-\begin{bmatrix}1 & 3 & 0 & -1\end{bmatrix} \\  & =\begin{bmatrix}4-1 & 6-3 & 4-0 & 10-(-1)\end{bmatrix} \\  & =\begin{bmatrix}3 & 3 & 4 & 11\end{bmatrix}\end{aligned}
$$

### partial_blank

Calculate $\frac{1}{3}N+2L$, where
$N=\begin{bmatrix}6 & 9 & 6 \\ 15 & 6 & 18\end{bmatrix}$
and
$L=\begin{bmatrix}\frac{1}{2} & - \frac{1}{2} & - \frac{1}{2} \\ - \frac{3}{2} & 3 & - \frac{1}{2}\end{bmatrix}.$

| $\frac{1}{3}N+2L=\,\,$ |  | {{field-1}} | {{field-2}} | $1$ |  |
| --- | --- | --- | --- | --- | --- |
|  |  | {{field-3}} | {{field-4}} | $5$ |  |

field-1: $3$

field-2: $2$

field-3: $2$

field-4: $8$

We multiply each entry of $N$ by $\frac{1}{3}$ and each entry of $L$ by $2,$ and then add the resulting matrices, as follows:

$$
\begin{aligned}\frac{1}{3}N+2L & =\frac{1}{3}\begin{bmatrix}6 & 9 & 6 \\ 15 & 6 & 18\end{bmatrix}+2\begin{bmatrix}\frac{1}{2} & - \frac{1}{2} & - \frac{1}{2} \\ - \frac{3}{2} & 3 & - \frac{1}{2}\end{bmatrix} \\  & =\begin{bmatrix}\frac{1}{3}\cdot 6 & \frac{1}{3}\cdot 9 & \frac{1}{3}\cdot 6 \\ \frac{1}{3}\cdot 15 & \frac{1}{3}\cdot 6 & \frac{1}{3}\cdot 18\end{bmatrix}+\begin{bmatrix}2\cdot \frac{1}{2} & 2\cdot (- \frac{1}{2}) & 2\cdot (- \frac{1}{2}) \\ 2\cdot (- \frac{3}{2}) & 2\cdot 3 & 2\cdot (- \frac{1}{2})\end{bmatrix} \\  & =\begin{bmatrix}2 & 3 & 2 \\ 5 & 2 & 6\end{bmatrix}+\begin{bmatrix}1 & -1 & -1 \\ -3 & 6 & -1\end{bmatrix} \\  & =\begin{bmatrix}2+1 & 3-1 & 2-1 \\ 5-3 & 2+6 & 6-1\end{bmatrix} \\  & =\begin{bmatrix}3 & 2 & 1 \\ 2 & 8 & 5\end{bmatrix}\end{aligned}
$$

### rect_radio

Calculate $\frac{1}{3}N+2L$, where
$N=\begin{bmatrix}6 & 9 & 6 \\ 15 & 6 & 18\end{bmatrix}$
and
$L=\begin{bmatrix}\frac{1}{2} & - \frac{1}{2} & - \frac{1}{2} \\ - \frac{3}{2} & 3 & - \frac{1}{2}\end{bmatrix}.$

selection: $\begin{bmatrix}1 & -1 & -1 \\ -3 & 6 & -1\end{bmatrix}$, $\begin{bmatrix}7 & 8 & 5 \\ 12 & 12 & 17\end{bmatrix}$, $\begin{bmatrix}3 & 2 & 1 \\ 2 & 8 & 5\end{bmatrix}$, $\begin{bmatrix}1 & 4 & 3 \\ 8 & -4 & 7\end{bmatrix}$, $\begin{bmatrix}\frac{5}{2} & \frac{5}{2} & \frac{3}{2} \\ \frac{7}{2} & 5 & \frac{11}{2}\end{bmatrix}$

We multiply each entry of $N$ by $\frac{1}{3}$ and each entry of $L$ by $2,$ and then add the resulting matrices, as follows:

$$
\begin{aligned}\frac{1}{3}N+2L & =\frac{1}{3}\begin{bmatrix}6 & 9 & 6 \\ 15 & 6 & 18\end{bmatrix}+2\begin{bmatrix}\frac{1}{2} & - \frac{1}{2} & - \frac{1}{2} \\ - \frac{3}{2} & 3 & - \frac{1}{2}\end{bmatrix} \\  & =\begin{bmatrix}\frac{1}{3}\cdot 6 & \frac{1}{3}\cdot 9 & \frac{1}{3}\cdot 6 \\ \frac{1}{3}\cdot 15 & \frac{1}{3}\cdot 6 & \frac{1}{3}\cdot 18\end{bmatrix}+\begin{bmatrix}2\cdot \frac{1}{2} & 2\cdot (- \frac{1}{2}) & 2\cdot (- \frac{1}{2}) \\ 2\cdot (- \frac{3}{2}) & 2\cdot 3 & 2\cdot (- \frac{1}{2})\end{bmatrix} \\  & =\begin{bmatrix}2 & 3 & 2 \\ 5 & 2 & 6\end{bmatrix}+\begin{bmatrix}1 & -1 & -1 \\ -3 & 6 & -1\end{bmatrix} \\  & =\begin{bmatrix}2+1 & 3+(-1) & 2+(-1) \\ 5+(-3) & 2+6 & 6+(-1)\end{bmatrix} \\  & =\begin{bmatrix}3 & 2 & 1 \\ 2 & 8 & 5\end{bmatrix}\end{aligned}
$$