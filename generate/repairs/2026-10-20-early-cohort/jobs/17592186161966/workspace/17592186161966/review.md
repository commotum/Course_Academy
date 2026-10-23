## q-42563 original

$$
A=\begin{bmatrix}5 & 0 & 2 & 7 \\ 1 & -7 & -4 & -6 \\ -1 & 3 & 1 & 2 \\ 2 & 7 & 2 & 3\end{bmatrix},\,B=\begin{bmatrix}7 & -6 & 2 & 3 \\ -3 & 5 & -4 & 2 \\ 0 & 0 & 1 & 0 \\ 4 & 1 & 2 & -1\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations 

I. ${C}_{1}:={C}_{1}+{C}_{3}$
II. ${C}_{2}:=…$
III. ${C}_{4}:=…$

each of the form ${C}_{i}:={C}_{i}+k{C}_{3},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

To transform $A$ into $B,$ we need to make entries to the left and to the right of ${a}_{33}=1$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{aligned}A & =\begin{bmatrix}5 & 0 & 2 & 7 \\ 1 & -7 & -4 & -6 \\ -1 & 3 & 1 & 2 \\ 2 & 7 & 2 & 3\end{bmatrix} &  & \,\begin{aligned}{C}_{1}: &={C}_{1}+{C}_{3}\end{aligned} \\  & ∼\begin{bmatrix}7 & 0 & 2 & 7 \\ -3 & -7 & -4 & -6 \\ 0 & 3 & 1 & 2 \\ 4 & 7 & 2 & 3\end{bmatrix} &  & \,\begin{aligned}{C}_{2}: &={C}_{2}-3{C}_{3}\end{aligned} \\  & ∼\begin{bmatrix}7 & -6 & 2 & 7 \\ -3 & 5 & -4 & -6 \\ 0 & 0 & 1 & 2 \\ 4 & 1 & 2 & 3\end{bmatrix} &  & \,\begin{aligned}{C}_{4}: &={C}_{4}-2{C}_{3}\end{aligned} \\  & ∼\begin{bmatrix}7 & -6 & 2 & 3 \\ -3 & 5 & -4 & 2 \\ 0 & 0 & 1 & 0 \\ 4 & 1 & 2 & -1\end{bmatrix} \\  & =B\end{aligned}
$$

Therefore, the corresponding elementary column operations are

$\,$ ${C}_{2}:={C}_{2}-3{C}_{3}\,$ and $\,{C}_{4}:={C}_{4}-2{C}_{3}.$

Replay

$$
A=\begin{bmatrix}5 & 0 & 2 & 7 \\ 1 & -7 & -4 & -6 \\ -1 & 3 & 1 & 2 \\ 2 & 7 & 2 & 3\end{bmatrix},\,B=\begin{bmatrix}7 & -6 & 2 & 3 \\ -3 & 5 & -4 & 2 \\ 0 & 0 & 1 & 0 \\ 4 & 1 & 2 & -1\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations

- $C_{1}:=C_{1}+C_{3}$
- $C_{2}:=\ldots$
- $C_{4}:=\ldots$

each of the form $C_i:=C_i+kC_{3},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

$C_{2}:=C_{2}+2C_{3}$ and $C_{4}:=C_{4}-C_{3}$
$C_{2}:=C_{2}+3C_{3}$ and $C_{4}:=C_{4}-2C_{3}$
$C_{2}:=C_{2}+3C_{3}$ and $C_{4}:=C_{4}+2C_{3}$
$C_{2}:=C_{2}-C_{3}$ and $C_{4}:=C_{4}-2C_{3}$
$C_{2}:=C_{2}-3C_{3}$ and $C_{4}:=C_{4}-2C_{3}$

To transform $A$ into $B,$ we need to make entries in row 3 other than $a_{33}=1$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{bmatrix}5 & 0 & 2 & 7 \\ 1 & -7 & -4 & -6 \\ -1 & 3 & 1 & 2 \\ 2 & 7 & 2 & 3\end{bmatrix}
\xrightarrow{C_{1}:=C_{1}+C_{3}}\begin{bmatrix}7 & 0 & 2 & 7 \\ -3 & -7 & -4 & -6 \\ 0 & 3 & 1 & 2 \\ 4 & 7 & 2 & 3\end{bmatrix}
\xrightarrow{C_{2}:=C_{2}-3C_{3}}\begin{bmatrix}7 & -6 & 2 & 7 \\ -3 & 5 & -4 & -6 \\ 0 & 0 & 1 & 2 \\ 4 & 1 & 2 & 3\end{bmatrix}
\xrightarrow{C_{4}:=C_{4}-2C_{3}}\begin{bmatrix}7 & -6 & 2 & 3 \\ -3 & 5 & -4 & 2 \\ 0 & 0 & 1 & 0 \\ 4 & 1 & 2 & -1\end{bmatrix}=B
$$

Therefore, the corresponding elementary column operations are

$C_{2}:=C_{2}-3C_{3}$ and $C_{4}:=C_{4}-2C_{3}$.

## q-130619 original

$$
A=\begin{bmatrix}5 & 0 & 0 & 7 \\ -8 & 2 & 4 & 8 \\ 5 & -1 & 3 & -2 \\ 2 & 0 & 4 & 1\end{bmatrix},\,B=\begin{bmatrix}5 & 0 & 0 & 7 \\ 2 & 2 & 10 & 4 \\ 0 & -1 & 0 & 0 \\ 2 & 0 & 4 & 1\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations 

- ${C}_{1}:={C}_{1}+5{C}_{2}$
- ${C}_{3}:=…$
- ${C}_{4}:=…$

each of the form ${C}_{i}:={C}_{i}+k{C}_{2},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

To transform $A$ into $B,$ we need to make entries to the left and to the right of ${a}_{32}=-1$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{aligned}A & =\begin{bmatrix}5 & 0 & 0 & 7 \\ -8 & 2 & 4 & 8 \\ 5 & -1 & 3 & -2 \\ 2 & 0 & 4 & 1\end{bmatrix} &  & \,\begin{aligned}{C}_{1}: &={C}_{1}+5{C}_{2}\end{aligned} \\  & ∼\begin{bmatrix}5 & 0 & 0 & 7 \\ 2 & 2 & 4 & 8 \\ 0 & -1 & 3 & -2 \\ 2 & 0 & 4 & 1\end{bmatrix} &  & \,\begin{aligned}{C}_{3}: &={C}_{3}+3{C}_{2}\end{aligned} \\  & ∼\begin{bmatrix}5 & 0 & 0 & 7 \\ 2 & 2 & 10 & 8 \\ 0 & -1 & 0 & -2 \\ 2 & 0 & 4 & 1\end{bmatrix} &  & \,\begin{aligned}{C}_{4}: &={C}_{4}-2{C}_{2}\end{aligned} \\  & ∼\begin{bmatrix}5 & 0 & 0 & 7 \\ 2 & 2 & 10 & 4 \\ 0 & -1 & 0 & 0 \\ 2 & 0 & 4 & 1\end{bmatrix} \\  & =B.\end{aligned}
$$

Therefore, the corresponding elementary column operations are

$\,$ ${C}_{3}:={C}_{3}+3{C}_{2}\,$ and $\,{C}_{4}:={C}_{4}-2{C}_{2}.$

Replay

$$
A=\begin{bmatrix}5 & 0 & 0 & 7 \\ -8 & 2 & 4 & 8 \\ 5 & -1 & 3 & -2 \\ 2 & 0 & 4 & 1\end{bmatrix},\,B=\begin{bmatrix}5 & 0 & 0 & 7 \\ 2 & 2 & 10 & 4 \\ 0 & -1 & 0 & 0 \\ 2 & 0 & 4 & 1\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations

- $C_{1}:=C_{1}+5C_{2}$
- $C_{3}:=\ldots$
- $C_{4}:=\ldots$

each of the form $C_i:=C_i+kC_{2},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

$C_{3}:=C_{3}+3C_{2}$ and $C_{4}:=C_{4}+2C_{2}$
$C_{3}:=C_{3}+3C_{2}$ and $C_{4}:=C_{4}-2C_{2}$
$C_{3}:=C_{3}+2C_{2}$ and $C_{4}:=C_{4}-3C_{2}$
$C_{3}:=C_{3}-3C_{2}$ and $C_{4}:=C_{4}+2C_{2}$
$C_{3}:=C_{3}-3C_{2}$ and $C_{4}:=C_{4}-2C_{2}$

To transform $A$ into $B,$ we need to make entries in row 3 other than $a_{32}=-1$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{bmatrix}5 & 0 & 0 & 7 \\ -8 & 2 & 4 & 8 \\ 5 & -1 & 3 & -2 \\ 2 & 0 & 4 & 1\end{bmatrix}
\xrightarrow{C_{1}:=C_{1}+5C_{2}}\begin{bmatrix}5 & 0 & 0 & 7 \\ 2 & 2 & 4 & 8 \\ 0 & -1 & 3 & -2 \\ 2 & 0 & 4 & 1\end{bmatrix}
\xrightarrow{C_{3}:=C_{3}+3C_{2}}\begin{bmatrix}5 & 0 & 0 & 7 \\ 2 & 2 & 10 & 8 \\ 0 & -1 & 0 & -2 \\ 2 & 0 & 4 & 1\end{bmatrix}
\xrightarrow{C_{4}:=C_{4}-2C_{2}}\begin{bmatrix}5 & 0 & 0 & 7 \\ 2 & 2 & 10 & 4 \\ 0 & -1 & 0 & 0 \\ 2 & 0 & 4 & 1\end{bmatrix}=B
$$

Therefore, the corresponding elementary column operations are

$C_{3}:=C_{3}+3C_{2}$ and $C_{4}:=C_{4}-2C_{2}$.

## q-130627 original

$$
A=\begin{bmatrix}7 & 5 & 6 & -9 \\ 6 & 4 & 2 & -6 \\ -7 & 2 & -3 & 6 \\ 5 & 6 & 1 & 8\end{bmatrix},\,B=\begin{bmatrix}-11 & -7 & 6 & 9 \\ 0 & 0 & 2 & 0 \\ 2 & 8 & -3 & -3 \\ 2 & 4 & 1 & 11\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations 

- ${C}_{1}:={C}_{1}-3{C}_{3}$
- ${C}_{2}:=…$
- ${C}_{4}:=…$

each of the form ${C}_{i}:={C}_{i}+k{C}_{3},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

To transform $A$ into $B,$ we need to make entries to the left and to the right of ${a}_{23}=2$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{aligned}A & =\begin{bmatrix}7 & 5 & 6 & -9 \\ 6 & 4 & 2 & -6 \\ -7 & 2 & -3 & 6 \\ 5 & 6 & 1 & 8\end{bmatrix} &  & \,\begin{aligned}{C}_{1}: &={C}_{1}-3{C}_{3}\end{aligned} \\  & ∼\begin{bmatrix}-11 & 5 & 6 & -9 \\ 0 & 4 & 2 & -6 \\ 2 & 2 & -3 & 6 \\ 2 & 6 & 1 & 8\end{bmatrix} &  & \,\begin{aligned}{C}_{2}: &={C}_{2}-2{C}_{3}\end{aligned} \\  & ∼\begin{bmatrix}-11 & -7 & 6 & -9 \\ 0 & 0 & 2 & -6 \\ 2 & 8 & -3 & 6 \\ 2 & 4 & 1 & 8\end{bmatrix} &  & \,\begin{aligned}{C}_{4}: &={C}_{4}+3{C}_{3}\end{aligned} \\  & ∼\begin{bmatrix}-11 & -7 & 6 & 9 \\ 0 & 0 & 2 & 0 \\ 2 & 8 & -3 & -3 \\ 2 & 4 & 1 & 11\end{bmatrix} \\  & =B.\end{aligned}
$$

Therefore, the corresponding elementary column operations are

$\,$ ${C}_{2}:={C}_{2}-2{C}_{3}\,$ and $\,{C}_{4}:={C}_{4}+3{C}_{3}.$

Replay

$$
A=\begin{bmatrix}7 & 5 & 6 & -9 \\ 6 & 4 & 2 & -6 \\ -7 & 2 & -3 & 6 \\ 5 & 6 & 1 & 8\end{bmatrix},\,B=\begin{bmatrix}-11 & -7 & 6 & 9 \\ 0 & 0 & 2 & 0 \\ 2 & 8 & -3 & -3 \\ 2 & 4 & 1 & 11\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations

- $C_{1}:=C_{1}-3C_{3}$
- $C_{2}:=\ldots$
- $C_{4}:=\ldots$

each of the form $C_i:=C_i+kC_{3},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

$C_{2}:=C_{2}-3C_{3}$ and $C_{4}:=C_{4}+2C_{3}$
$C_{2}:=C_{2}+2C_{3}$ and $C_{4}:=C_{4}+3C_{3}$
$C_{2}:=C_{2}+2C_{3}$ and $C_{4}:=C_{4}-3C_{3}$
$C_{2}:=C_{2}-2C_{3}$ and $C_{4}:=C_{4}+3C_{3}$
$C_{2}:=C_{2}-2C_{3}$ and $C_{4}:=C_{4}-3C_{3}$

To transform $A$ into $B,$ we need to make entries in row 2 other than $a_{23}=2$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{bmatrix}7 & 5 & 6 & -9 \\ 6 & 4 & 2 & -6 \\ -7 & 2 & -3 & 6 \\ 5 & 6 & 1 & 8\end{bmatrix}
\xrightarrow{C_{1}:=C_{1}-3C_{3}}\begin{bmatrix}-11 & 5 & 6 & -9 \\ 0 & 4 & 2 & -6 \\ 2 & 2 & -3 & 6 \\ 2 & 6 & 1 & 8\end{bmatrix}
\xrightarrow{C_{2}:=C_{2}-2C_{3}}\begin{bmatrix}-11 & -7 & 6 & -9 \\ 0 & 0 & 2 & -6 \\ 2 & 8 & -3 & 6 \\ 2 & 4 & 1 & 8\end{bmatrix}
\xrightarrow{C_{4}:=C_{4}+3C_{3}}\begin{bmatrix}-11 & -7 & 6 & 9 \\ 0 & 0 & 2 & 0 \\ 2 & 8 & -3 & -3 \\ 2 & 4 & 1 & 11\end{bmatrix}=B
$$

Therefore, the corresponding elementary column operations are

$C_{2}:=C_{2}-2C_{3}$ and $C_{4}:=C_{4}+3C_{3}$.

## q-42929 original

$$
A=\begin{bmatrix}-1 & 2 & 2 & 3 \\ 1 & 3 & 1 & -2 \\ 3 & 1 & 4 & -2 \\ 4 & -2 & -3 & -4\end{bmatrix},\,B=\begin{bmatrix}-3 & -4 & 2 & 7 \\ 0 & 0 & 1 & 0 \\ -1 & -11 & 4 & 6 \\ 7 & 7 & -3 & -10\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations 

- ${C}_{1}:=…$
- ${C}_{2}:=…$
- ${C}_{4}:={C}_{4}+2{C}_{3}$

each of the form ${C}_{i}:={C}_{i}+k{C}_{3},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

To transform $A$ into $B,$ we need to make entries to the left and to the right of ${a}_{23}=1$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{aligned}A & =\begin{bmatrix}-1 & 2 & 2 & 3 \\ 1 & 3 & 1 & -2 \\ 3 & 1 & 4 & -2 \\ 4 & -2 & -3 & -4\end{bmatrix} &  & \,\begin{aligned}{C}_{1}: &={C}_{1}-{C}_{3}\end{aligned} \\  & ∼\begin{bmatrix}-3 & 2 & 2 & 3 \\ 0 & 3 & 1 & -2 \\ -1 & 1 & 4 & -2 \\ 7 & -2 & -3 & -4\end{bmatrix} &  & \,\begin{aligned}{C}_{2}: &={C}_{2}-3{C}_{3}\end{aligned} \\  & ∼\begin{bmatrix}-3 & -4 & 2 & 3 \\ 0 & 0 & 1 & -2 \\ -1 & -11 & 4 & -2 \\ 7 & 7 & -3 & -4\end{bmatrix} &  & \,\begin{aligned}{C}_{4}: &={C}_{4}+2{C}_{3}\end{aligned} \\  & ∼\begin{bmatrix}-3 & -4 & 2 & 7 \\ 0 & 0 & 1 & 0 \\ -1 & -11 & 4 & 6 \\ 7 & 7 & -3 & -10\end{bmatrix} \\  & =B.\end{aligned}
$$

Therefore, the corresponding elementary column operations are

$\,$ ${C}_{1}:={C}_{1}-{C}_{3}\,$ and $\,{C}_{2}:={C}_{2}-3{C}_{3}.$

Replay

$$
A=\begin{bmatrix}-1 & 2 & 2 & 3 \\ 1 & 3 & 1 & -2 \\ 3 & 1 & 4 & -2 \\ 4 & -2 & -3 & -4\end{bmatrix},\,B=\begin{bmatrix}-3 & -4 & 2 & 7 \\ 0 & 0 & 1 & 0 \\ -1 & -11 & 4 & 6 \\ 7 & 7 & -3 & -10\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations

- $C_{1}:=\ldots$
- $C_{2}:=\ldots$
- $C_{4}:=C_{4}+2C_{3}$

each of the form $C_i:=C_i+kC_{3},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

$C_{1}:=C_{1}-C_{3}$ and $C_{2}:=C_{2}-C_{3}$
$C_{1}:=C_{1}-C_{3}$ and $C_{2}:=C_{2}-3C_{3}$
$C_{1}:=C_{1}-3C_{3}$ and $C_{2}:=C_{2}-C_{3}$
$C_{1}:=C_{1}-C_{3}$ and $C_{2}:=C_{2}+3C_{3}$
$C_{1}:=C_{1}+C_{3}$ and $C_{2}:=C_{2}-3C_{3}$

To transform $A$ into $B,$ we need to make entries in row 2 other than $a_{23}=1$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{bmatrix}-1 & 2 & 2 & 3 \\ 1 & 3 & 1 & -2 \\ 3 & 1 & 4 & -2 \\ 4 & -2 & -3 & -4\end{bmatrix}
\xrightarrow{C_{1}:=C_{1}-C_{3}}\begin{bmatrix}-3 & 2 & 2 & 3 \\ 0 & 3 & 1 & -2 \\ -1 & 1 & 4 & -2 \\ 7 & -2 & -3 & -4\end{bmatrix}
\xrightarrow{C_{2}:=C_{2}-3C_{3}}\begin{bmatrix}-3 & -4 & 2 & 3 \\ 0 & 0 & 1 & -2 \\ -1 & -11 & 4 & -2 \\ 7 & 7 & -3 & -4\end{bmatrix}
\xrightarrow{C_{4}:=C_{4}+2C_{3}}\begin{bmatrix}-3 & -4 & 2 & 7 \\ 0 & 0 & 1 & 0 \\ -1 & -11 & 4 & 6 \\ 7 & 7 & -3 & -10\end{bmatrix}=B
$$

Therefore, the corresponding elementary column operations are

$C_{1}:=C_{1}-C_{3}$ and $C_{2}:=C_{2}-3C_{3}$.

## q-91210 original

$$
A=\begin{bmatrix}1 & 4 & 7 & 7 \\ -7 & -4 & 2 & -1 \\ 4 & 1 & 3 & 2 \\ 1 & 5 & 1 & 8\end{bmatrix},\,B=\begin{bmatrix}-15 & 4 & -5 & -1 \\ 9 & -4 & 14 & 7 \\ 0 & 1 & 0 & 0 \\ -19 & 5 & -14 & -2\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations 

- ${C}_{1}:=…$
- ${C}_{3}:={C}_{3}-3{C}_{2}$
- ${C}_{4}:=…$

each of the form ${C}_{i}:={C}_{i}+k{C}_{2},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

To transform $A$ into $B,$ we need to make entries to the left and to the right of ${a}_{32}=1$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{aligned}A & =\begin{bmatrix}1 & 4 & 7 & 7 \\ 7 & -4 & 2 & -1 \\ 4 & 1 & 3 & 2 \\ 1 & 5 & 1 & 8\end{bmatrix} &  & \,\begin{aligned}{C}_{1}: &={C}_{1}-4{C}_{2}\end{aligned} \\  & ∼\begin{bmatrix}-15 & 4 & 7 & 7 \\ 9 & -4 & 2 & -1 \\ 0 & 1 & 3 & 2 \\ -19 & 5 & 1 & 8\end{bmatrix} &  & \,\begin{aligned}{C}_{3}: &={C}_{3}-3{C}_{2}\end{aligned} \\  & ∼\begin{bmatrix}-15 & 4 & -5 & 7 \\ 9 & -4 & 14 & -1 \\ 0 & 1 & 0 & 2 \\ -19 & 5 & -14 & 8\end{bmatrix} &  & \,\begin{aligned}{C}_{4}: &={C}_{4}-2{C}_{2}\end{aligned} \\  & ∼\begin{bmatrix}-15 & 4 & -5 & -1 \\ 9 & -4 & 14 & 7 \\ 0 & 1 & 0 & 0 \\ -19 & 5 & -14 & -2\end{bmatrix} \\  & =B.\end{aligned}
$$

Therefore, the corresponding elementary column operations are

$\,$ ${C}_{1}:={C}_{1}-4{C}_{2}\,$ and $\,{C}_{4}:={C}_{4}-2{C}_{2}.$

Replay

$$
A=\begin{bmatrix}1 & 4 & 7 & 7 \\ -7 & -4 & 2 & -1 \\ 4 & 1 & 3 & 2 \\ 1 & 5 & 1 & 8\end{bmatrix},\,B=\begin{bmatrix}-15 & 4 & -5 & -1 \\ 9 & -4 & 14 & 7 \\ 0 & 1 & 0 & 0 \\ -19 & 5 & -14 & -2\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations

- $C_{1}:=\ldots$
- $C_{3}:=C_{3}-3C_{2}$
- $C_{4}:=\ldots$

each of the form $C_i:=C_i+kC_{2},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

$C_{1}:=C_{1}-4C_{2}$ and $C_{4}:=C_{4}-2C_{2}$
$C_{1}:=C_{1}-2C_{2}$ and $C_{4}:=C_{4}-4C_{2}$
$C_{1}:=C_{1}+4C_{2}$ and $C_{4}:=C_{4}+2C_{2}$
$C_{1}:=C_{1}+2C_{2}$ and $C_{4}:=C_{4}+4C_{2}$
$C_{1}:=C_{1}-4C_{2}$ and $C_{4}:=C_{4}+2C_{2}$

To transform $A$ into $B,$ we need to make entries in row 3 other than $a_{32}=1$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{bmatrix}1 & 4 & 7 & 7 \\ -7 & -4 & 2 & -1 \\ 4 & 1 & 3 & 2 \\ 1 & 5 & 1 & 8\end{bmatrix}
\xrightarrow{C_{1}:=C_{1}-4C_{2}}\begin{bmatrix}-15 & 4 & 7 & 7 \\ 9 & -4 & 2 & -1 \\ 0 & 1 & 3 & 2 \\ -19 & 5 & 1 & 8\end{bmatrix}
\xrightarrow{C_{3}:=C_{3}-3C_{2}}\begin{bmatrix}-15 & 4 & -5 & 7 \\ 9 & -4 & 14 & -1 \\ 0 & 1 & 0 & 2 \\ -19 & 5 & -14 & 8\end{bmatrix}
\xrightarrow{C_{4}:=C_{4}-2C_{2}}\begin{bmatrix}-15 & 4 & -5 & -1 \\ 9 & -4 & 14 & 7 \\ 0 & 1 & 0 & 0 \\ -19 & 5 & -14 & -2\end{bmatrix}=B
$$

Therefore, the corresponding elementary column operations are

$C_{1}:=C_{1}-4C_{2}$ and $C_{4}:=C_{4}-2C_{2}$.

## q-91211 original

$$
A=\begin{bmatrix}1 & 1 & 6 & 1 \\ 8 & 1 & 2 & 5 \\ 0 & 9 & -5 & 4 \\ 4 & 5 & 3 & 1\end{bmatrix},\,B=\begin{bmatrix}-3 & -4 & 3 & 1 \\ -12 & -24 & -13 & 5 \\ -16 & -11 & -17 & 4 \\ 0 & 0 & 0 & 1\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations 

- ${C}_{1}:={C}_{1}-4{C}_{4}$
- ${C}_{2}:=…$
- ${C}_{3}:=…$

each of the form ${C}_{i}:={C}_{i}+k{C}_{4},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

To transform $A$ into $B,$ we need to make entries to the left of ${a}_{44}=1$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{aligned}A & =\begin{bmatrix}1 & 1 & 6 & 1 \\ 8 & 1 & 2 & 5 \\ 0 & 9 & -5 & 4 \\ 4 & 5 & 3 & 1\end{bmatrix} &  & \,\begin{aligned}{C}_{1}: &={C}_{1}-4{C}_{4}\end{aligned} \\  & ∼\begin{bmatrix}-3 & 1 & 6 & 1 \\ -12 & 1 & 2 & 5 \\ -16 & 9 & -5 & 4 \\ 0 & 5 & 3 & 1\end{bmatrix} &  & \,\begin{aligned}{C}_{2}: &={C}_{2}-5{C}_{4}\end{aligned} \\  & ∼\begin{bmatrix}-3 & -4 & 6 & 1 \\ -12 & -24 & 2 & 5 \\ -16 & -11 & -5 & 4 \\ 0 & 0 & 3 & 1\end{bmatrix} &  & \,\begin{aligned}{C}_{3}: &={C}_{3}-3{C}_{4}\end{aligned} \\  & ∼\begin{bmatrix}-3 & -4 & 3 & 1 \\ -12 & -24 & -13 & 5 \\ -16 & -11 & -17 & 4 \\ 0 & 0 & 0 & 1\end{bmatrix} \\  & =B.\end{aligned}
$$

Therefore, the corresponding elementary column operations are

$\,$ ${C}_{2}:={C}_{2}-5{C}_{4}\,$ and $\,{C}_{3}:={C}_{3}-3{C}_{4}.$

Replay

$$
A=\begin{bmatrix}1 & 1 & 6 & 1 \\ 8 & 1 & 2 & 5 \\ 0 & 9 & -5 & 4 \\ 4 & 5 & 3 & 1\end{bmatrix},\,B=\begin{bmatrix}-3 & -4 & 3 & 1 \\ -12 & -24 & -13 & 5 \\ -16 & -11 & -17 & 4 \\ 0 & 0 & 0 & 1\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations

- $C_{1}:=C_{1}-4C_{4}$
- $C_{2}:=\ldots$
- $C_{3}:=\ldots$

each of the form $C_i:=C_i+kC_{4},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

$C_{2}:=C_{2}+3C_{4}$ and $C_{3}:=C_{3}+5C_{4}$
$C_{2}:=C_{2}+5C_{4}$ and $C_{3}:=C_{3}+3C_{4}$
$C_{2}:=C_{2}-5C_{4}$ and $C_{3}:=C_{3}-3C_{4}$
$C_{2}:=C_{2}-3C_{4}$ and $C_{3}:=C_{3}-5C_{4}$
$C_{2}:=C_{2}-5C_{4}$ and $C_{3}:=C_{3}+3C_{4}$

To transform $A$ into $B,$ we need to make entries in row 4 other than $a_{44}=1$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{bmatrix}1 & 1 & 6 & 1 \\ 8 & 1 & 2 & 5 \\ 0 & 9 & -5 & 4 \\ 4 & 5 & 3 & 1\end{bmatrix}
\xrightarrow{C_{1}:=C_{1}-4C_{4}}\begin{bmatrix}-3 & 1 & 6 & 1 \\ -12 & 1 & 2 & 5 \\ -16 & 9 & -5 & 4 \\ 0 & 5 & 3 & 1\end{bmatrix}
\xrightarrow{C_{2}:=C_{2}-5C_{4}}\begin{bmatrix}-3 & -4 & 6 & 1 \\ -12 & -24 & 2 & 5 \\ -16 & -11 & -5 & 4 \\ 0 & 0 & 3 & 1\end{bmatrix}
\xrightarrow{C_{3}:=C_{3}-3C_{4}}\begin{bmatrix}-3 & -4 & 3 & 1 \\ -12 & -24 & -13 & 5 \\ -16 & -11 & -17 & 4 \\ 0 & 0 & 0 & 1\end{bmatrix}=B
$$

Therefore, the corresponding elementary column operations are

$C_{2}:=C_{2}-5C_{4}$ and $C_{3}:=C_{3}-3C_{4}$.

## q-91214 original

$$
A=\begin{bmatrix}1 & 1 & 0 & 2 \\ 1 & 7 & 3 & 9 \\ 2 & 3 & 0 & 1 \\ 2 & 1 & 1 & 7\end{bmatrix},\,B=\begin{bmatrix}1 & 1 & 0 & 2 \\ -5 & 4 & 3 & -12 \\ 2 & 3 & 0 & 1 \\ 0 & 0 & 1 & 0\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations 

- ${C}_{1}:=…$
- ${C}_{2}:={C}_{2}-{C}_{3}$
- ${C}_{4}:=…$

each of the form ${C}_{i}:={C}_{i}+k{C}_{3},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

To transform $A$ into $B,$ we need to make entries to the left and to the right of ${a}_{43}=1$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{aligned}A & =\begin{bmatrix}1 & 1 & 0 & 2 \\ 1 & 7 & 3 & 9 \\ 2 & 3 & 0 & 1 \\ 2 & 1 & 1 & 7\end{bmatrix} &  & \,\begin{aligned}{C}_{1}: &={C}_{1}-2{C}_{3}\end{aligned} \\  & ∼\begin{bmatrix}1 & 1 & 0 & 2 \\ -5 & 7 & 3 & 9 \\ 2 & 3 & 0 & 1 \\ 0 & 1 & 1 & 7\end{bmatrix} &  & \,\begin{aligned}{C}_{2}: &={C}_{2}-{C}_{3}\end{aligned} \\  & ∼\begin{bmatrix}1 & 1 & 0 & 2 \\ -5 & 4 & 3 & 9 \\ 2 & 3 & 0 & 1 \\ 0 & 0 & 1 & 7\end{bmatrix} &  & \,\begin{aligned}{C}_{4}: &={C}_{4}-7{C}_{3}\end{aligned} \\  & ∼\begin{bmatrix}1 & 1 & 0 & 2 \\ -5 & 4 & 3 & -12 \\ 2 & 3 & 0 & 1 \\ 0 & 0 & 1 & 0\end{bmatrix} \\  & =B.\end{aligned}
$$

Therefore, the corresponding elementary column operations are

$\,$ ${C}_{1}:={C}_{1}-2{C}_{3}\,$ and $\,{C}_{4}:={C}_{4}-7{C}_{3}.$

Replay

$$
A=\begin{bmatrix}1 & 1 & 0 & 2 \\ 1 & 7 & 3 & 9 \\ 2 & 3 & 0 & 1 \\ 2 & 1 & 1 & 7\end{bmatrix},\,B=\begin{bmatrix}1 & 1 & 0 & 2 \\ -5 & 4 & 3 & -12 \\ 2 & 3 & 0 & 1 \\ 0 & 0 & 1 & 0\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations

- $C_{1}:=\ldots$
- $C_{2}:=C_{2}-C_{3}$
- $C_{4}:=\ldots$

each of the form $C_i:=C_i+kC_{3},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

$C_{1}:=C_{1}-2C_{3}$ and $C_{4}:=C_{4}-7C_{3}$
$C_{1}:=C_{1}-2C_{3}$ and $C_{4}:=C_{4}-C_{3}$
$C_{1}:=C_{1}-7C_{3}$ and $C_{4}:=C_{4}-2C_{3}$
$C_{1}:=C_{1}-2C_{3}$ and $C_{4}:=C_{4}+7C_{3}$
$C_{1}:=C_{1}+2C_{3}$ and $C_{4}:=C_{4}+7C_{3}$

To transform $A$ into $B,$ we need to make entries in row 4 other than $a_{43}=1$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{bmatrix}1 & 1 & 0 & 2 \\ 1 & 7 & 3 & 9 \\ 2 & 3 & 0 & 1 \\ 2 & 1 & 1 & 7\end{bmatrix}
\xrightarrow{C_{1}:=C_{1}-2C_{3}}\begin{bmatrix}1 & 1 & 0 & 2 \\ -5 & 7 & 3 & 9 \\ 2 & 3 & 0 & 1 \\ 0 & 1 & 1 & 7\end{bmatrix}
\xrightarrow{C_{2}:=C_{2}-C_{3}}\begin{bmatrix}1 & 1 & 0 & 2 \\ -5 & 4 & 3 & 9 \\ 2 & 3 & 0 & 1 \\ 0 & 0 & 1 & 7\end{bmatrix}
\xrightarrow{C_{4}:=C_{4}-7C_{3}}\begin{bmatrix}1 & 1 & 0 & 2 \\ -5 & 4 & 3 & -12 \\ 2 & 3 & 0 & 1 \\ 0 & 0 & 1 & 0\end{bmatrix}=B
$$

Therefore, the corresponding elementary column operations are

$C_{1}:=C_{1}-2C_{3}$ and $C_{4}:=C_{4}-7C_{3}$.

## q-130624 original

$$
A=\begin{bmatrix}-4 & 4 & -2 & 8 \\ -6 & 9 & -3 & 7 \\ 4 & 2 & 1 & -8 \\ 5 & 4 & 3 & 3\end{bmatrix},\,B=\begin{bmatrix}0 & 0 & -2 & 0 \\ 0 & 3 & -3 & -5 \\ 2 & 4 & 1 & -4 \\ -1 & 10 & 3 & 15\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations 

I. ${C}_{1}:=…$
II. ${C}_{2}:={C}_{2}+2{C}_{3}$
III. ${C}_{4}:=…$

each of the form ${C}_{i}:={C}_{i}+k{C}_{3},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

To transform $A$ into $B,$ we need to make entries to the left and to the right of ${a}_{13}=-2$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{aligned}A & =\begin{bmatrix}-4 & 4 & -2 & 8 \\ -6 & 9 & -3 & 7 \\ 4 & 2 & 1 & -8 \\ 5 & 4 & 3 & 3\end{bmatrix} &  & \,\begin{aligned}{C}_{1}: &={C}_{1}-2{C}_{3}\end{aligned} \\  & ∼\begin{bmatrix}0 & 4 & -2 & 8 \\ 0 & 9 & -3 & 7 \\ 2 & 2 & 1 & -8 \\ -1 & 4 & 3 & 3\end{bmatrix} &  & \,\begin{aligned}{C}_{2}: &={C}_{2}+2{C}_{3}\end{aligned} \\  & ∼\begin{bmatrix}0 & 0 & -2 & 8 \\ 0 & 3 & -3 & 7 \\ 2 & 4 & 1 & -8 \\ -1 & 10 & 3 & 3\end{bmatrix} &  & \,\begin{aligned}{C}_{4}: &={C}_{4}+4{C}_{3}\end{aligned} \\  & ∼\begin{bmatrix}0 & 0 & -2 & 0 \\ 0 & 3 & -3 & -5 \\ 2 & 4 & 1 & -4 \\ -1 & 10 & 3 & 15\end{bmatrix} \\  & =B.\end{aligned}
$$

Therefore, the corresponding elementary column operations are

$\,$ ${C}_{1}:={C}_{1}-2{C}_{3}\,$ and $\,{C}_{4}:={C}_{4}+4{C}_{3}.$

Replay

$$
A=\begin{bmatrix}-4 & 4 & -2 & 8 \\ -6 & 9 & -3 & 7 \\ 4 & 2 & 1 & -8 \\ 5 & 4 & 3 & 3\end{bmatrix},\,B=\begin{bmatrix}0 & 0 & -2 & 0 \\ 0 & 3 & -3 & -5 \\ 2 & 4 & 1 & -4 \\ -1 & 10 & 3 & 15\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations

- $C_{1}:=\ldots$
- $C_{2}:=C_{2}+2C_{3}$
- $C_{4}:=\ldots$

each of the form $C_i:=C_i+kC_{3},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

$C_{1}:=C_{1}-4C_{3}$ and $C_{4}:=C_{4}+2C_{3}$
$C_{1}:=C_{1}+2C_{3}$ and $C_{4}:=C_{4}-4C_{3}$
$C_{1}:=C_{1}+2C_{3}$ and $C_{4}:=C_{4}+4C_{3}$
$C_{1}:=C_{1}-2C_{3}$ and $C_{4}:=C_{4}-4C_{3}$
$C_{1}:=C_{1}-2C_{3}$ and $C_{4}:=C_{4}+4C_{3}$

To transform $A$ into $B,$ we need to make entries in row 1 other than $a_{13}=-2$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{bmatrix}-4 & 4 & -2 & 8 \\ -6 & 9 & -3 & 7 \\ 4 & 2 & 1 & -8 \\ 5 & 4 & 3 & 3\end{bmatrix}
\xrightarrow{C_{1}:=C_{1}-2C_{3}}\begin{bmatrix}0 & 4 & -2 & 8 \\ 0 & 9 & -3 & 7 \\ 2 & 2 & 1 & -8 \\ -1 & 4 & 3 & 3\end{bmatrix}
\xrightarrow{C_{2}:=C_{2}+2C_{3}}\begin{bmatrix}0 & 0 & -2 & 8 \\ 0 & 3 & -3 & 7 \\ 2 & 4 & 1 & -8 \\ -1 & 10 & 3 & 3\end{bmatrix}
\xrightarrow{C_{4}:=C_{4}+4C_{3}}\begin{bmatrix}0 & 0 & -2 & 0 \\ 0 & 3 & -3 & -5 \\ 2 & 4 & 1 & -4 \\ -1 & 10 & 3 & 15\end{bmatrix}=B
$$

Therefore, the corresponding elementary column operations are

$C_{1}:=C_{1}-2C_{3}$ and $C_{4}:=C_{4}+4C_{3}$.

## q-42562 original

$$
A=\begin{bmatrix}2 & 8 & 6 & -2 \\ 1 & 4 & 5 & -3 \\ -2 & -5 & -3 & 8 \\ -1 & -1 & -4 & 1\end{bmatrix},\,B=\begin{bmatrix}2 & 0 & -4 & 4 \\ 1 & 0 & 0 & 0 \\ -2 & 3 & 7 & 2 \\ -1 & 3 & 1 & -2\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations 

I. ${C}_{2}:=…$
II. ${C}_{3}:={C}_{3}-5{C}_{1}$
III. ${C}_{4}:=…$

each of the form ${C}_{i}:={C}_{i}+k{C}_{1},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

To transform $A$ into $B,$ we need to make entries to the right of ${a}_{21}=1$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{aligned}A & =\begin{bmatrix}2 & 8 & 6 & -2 \\ 1 & 4 & 5 & -3 \\ -2 & -5 & -3 & 8 \\ -1 & -1 & -4 & 1\end{bmatrix} &  & \,\begin{aligned}{C}_{2}: &={C}_{2}-4{C}_{1}\end{aligned} \\  & ∼\begin{bmatrix}2 & 0 & 6 & -2 \\ 1 & 0 & 5 & -3 \\ -2 & 3 & -3 & 8 \\ -1 & 3 & -4 & 1\end{bmatrix} &  & \,\begin{aligned}{C}_{3}: &={C}_{3}-5{C}_{1}\end{aligned} \\  & ∼\begin{bmatrix}2 & 0 & -4 & -2 \\ 1 & 0 & 0 & -3 \\ -2 & 3 & 7 & 8 \\ -1 & 3 & 1 & 1\end{bmatrix} &  & \,\begin{aligned}{C}_{4}: &={C}_{4}+3{C}_{1}\end{aligned} \\  & ∼\begin{bmatrix}2 & 0 & -4 & 4 \\ 1 & 0 & 0 & 0 \\ -2 & 3 & 7 & 2 \\ -1 & 3 & 1 & -2\end{bmatrix} \\  & =B.\end{aligned}
$$

Therefore, the corresponding elementary column operations are

$\,$ ${C}_{2}:={C}_{2}-4{C}_{1}\,$ and $\,{C}_{4}:={C}_{4}+3{C}_{1}.$

Replay

$$
A=\begin{bmatrix}2 & 8 & 6 & -2 \\ 1 & 4 & 5 & -3 \\ -2 & -5 & -3 & 8 \\ -1 & -1 & -4 & 1\end{bmatrix},\,B=\begin{bmatrix}2 & 0 & -4 & 4 \\ 1 & 0 & 0 & 0 \\ -2 & 3 & 7 & 2 \\ -1 & 3 & 1 & -2\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations

- $C_{2}:=\ldots$
- $C_{3}:=C_{3}-5C_{1}$
- $C_{4}:=\ldots$

each of the form $C_i:=C_i+kC_{1},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

$C_{2}:=C_{2}-4C_{1}$ and $C_{4}:=C_{4}+3C_{1}$
$C_{2}:=C_{2}-3C_{1}$ and $C_{4}:=C_{4}+4C_{1}$
$C_{2}:=C_{2}-2C_{1}$ and $C_{4}:=C_{4}+3C_{1}$
$C_{2}:=C_{2}+4C_{1}$ and $C_{4}:=C_{4}+3C_{1}$
$C_{2}:=C_{2}-4C_{1}$ and $C_{4}:=C_{4}-3C_{1}$

To transform $A$ into $B,$ we need to make entries in row 2 other than $a_{21}=1$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{bmatrix}2 & 8 & 6 & -2 \\ 1 & 4 & 5 & -3 \\ -2 & -5 & -3 & 8 \\ -1 & -1 & -4 & 1\end{bmatrix}
\xrightarrow{C_{2}:=C_{2}-4C_{1}}\begin{bmatrix}2 & 0 & 6 & -2 \\ 1 & 0 & 5 & -3 \\ -2 & 3 & -3 & 8 \\ -1 & 3 & -4 & 1\end{bmatrix}
\xrightarrow{C_{3}:=C_{3}-5C_{1}}\begin{bmatrix}2 & 0 & -4 & -2 \\ 1 & 0 & 0 & -3 \\ -2 & 3 & 7 & 8 \\ -1 & 3 & 1 & 1\end{bmatrix}
\xrightarrow{C_{4}:=C_{4}+3C_{1}}\begin{bmatrix}2 & 0 & -4 & 4 \\ 1 & 0 & 0 & 0 \\ -2 & 3 & 7 & 2 \\ -1 & 3 & 1 & -2\end{bmatrix}=B
$$

Therefore, the corresponding elementary column operations are

$C_{2}:=C_{2}-4C_{1}$ and $C_{4}:=C_{4}+3C_{1}$.

## q-91212 original

$$
A=\begin{bmatrix}2 & 1 & 2 & 3 \\ 0 & 8 & 0 & 4 \\ 6 & 9 & 1 & 3 \\ -6 & -1 & 1 & -6\end{bmatrix},\,B=\begin{bmatrix}0 & 1 & 0 & 0 \\ -16 & 8 & -16 & -20 \\ -12 & 9 & -17 & -24 \\ -4 & -1 & 3 & -3\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations 

I. ${C}_{1}:=…$
II. ${C}_{3}:=…$
III. ${C}_{4}:={C}_{4}-3{C}_{2}$

each of the form ${C}_{i}:={C}_{i}+k{C}_{2},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

To transform $A$ into $B,$ we need to make entries to the left and to the right of ${a}_{12}=1$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{aligned}A & =\begin{bmatrix}2 & 1 & 2 & 3 \\ 0 & 8 & 0 & 4 \\ 6 & 9 & 1 & 3 \\ -6 & -1 & 1 & -6\end{bmatrix} &  & \,\begin{aligned}{C}_{1}: &={C}_{1}-2{C}_{2}\end{aligned} \\  & ∼\begin{bmatrix}0 & 1 & 2 & 3 \\ -16 & 8 & 0 & 4 \\ -12 & 9 & 1 & 3 \\ -4 & -1 & 1 & -6\end{bmatrix} &  & \,\begin{aligned}{C}_{3}: &={C}_{3}-2{C}_{2}\end{aligned} \\  & ∼\begin{bmatrix}0 & 1 & 0 & 3 \\ -16 & 8 & -16 & 4 \\ -12 & 9 & -17 & 3 \\ -4 & -1 & 3 & -6\end{bmatrix} &  & \,\begin{aligned}{C}_{4}: &={C}_{4}-3{C}_{2}\end{aligned} \\  & ∼\begin{bmatrix}0 & 1 & 0 & 0 \\ -16 & 8 & -16 & -20 \\ -12 & 9 & -17 & -24 \\ -4 & -1 & 3 & -3\end{bmatrix} \\  & =B.\end{aligned}
$$

Therefore, the corresponding elementary column operations are

$\,$ ${C}_{1}:={C}_{1}-2{C}_{2}\,$ and $\,{C}_{3}:={C}_{3}-2{C}_{2}.$

Replay

$$
A=\begin{bmatrix}2 & 1 & 2 & 3 \\ 0 & 8 & 0 & 4 \\ 6 & 9 & 1 & 3 \\ -6 & -1 & 1 & -6\end{bmatrix},\,B=\begin{bmatrix}0 & 1 & 0 & 0 \\ -16 & 8 & -16 & -20 \\ -12 & 9 & -17 & -24 \\ -4 & -1 & 3 & -3\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations

- $C_{1}:=\ldots$
- $C_{3}:=\ldots$
- $C_{4}:=C_{4}-3C_{2}$

each of the form $C_i:=C_i+kC_{2},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

$C_{1}:=C_{1}-C_{2}$ and $C_{3}:=C_{3}-C_{2}$
$C_{1}:=C_{1}-2C_{2}$ and $C_{3}:=C_{3}-3C_{2}$
$C_{1}:=C_{1}-2C_{2}$ and $C_{3}:=C_{3}-2C_{2}$
$C_{1}:=C_{1}+2C_{2}$ and $C_{3}:=C_{3}+2C_{2}$
$C_{1}:=C_{1}+C_{2}$ and $C_{3}:=C_{3}+C_{2}$

To transform $A$ into $B,$ we need to make entries in row 1 other than $a_{12}=1$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{bmatrix}2 & 1 & 2 & 3 \\ 0 & 8 & 0 & 4 \\ 6 & 9 & 1 & 3 \\ -6 & -1 & 1 & -6\end{bmatrix}
\xrightarrow{C_{1}:=C_{1}-2C_{2}}\begin{bmatrix}0 & 1 & 2 & 3 \\ -16 & 8 & 0 & 4 \\ -12 & 9 & 1 & 3 \\ -4 & -1 & 1 & -6\end{bmatrix}
\xrightarrow{C_{3}:=C_{3}-2C_{2}}\begin{bmatrix}0 & 1 & 0 & 3 \\ -16 & 8 & -16 & 4 \\ -12 & 9 & -17 & 3 \\ -4 & -1 & 3 & -6\end{bmatrix}
\xrightarrow{C_{4}:=C_{4}-3C_{2}}\begin{bmatrix}0 & 1 & 0 & 0 \\ -16 & 8 & -16 & -20 \\ -12 & 9 & -17 & -24 \\ -4 & -1 & 3 & -3\end{bmatrix}=B
$$

Therefore, the corresponding elementary column operations are

$C_{1}:=C_{1}-2C_{2}$ and $C_{3}:=C_{3}-2C_{2}$.

## Changed given-column with matrix held constant

$$
A=\begin{bmatrix}5 & 0 & 2 & 7 \\ 1 & -7 & -4 & -6 \\ -1 & 3 & 1 & 2 \\ 2 & 7 & 2 & 3\end{bmatrix},\,B=\begin{bmatrix}7 & -6 & 2 & 3 \\ -3 & 5 & -4 & 2 \\ 0 & 0 & 1 & 0 \\ 4 & 1 & 2 & -1\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations

- $C_{1}:=C_{1}+C_{3}$
- $C_{2}:=\ldots$
- $C_{4}:=\ldots$

each of the form $C_i:=C_i+kC_{3},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

$C_{2}:=C_{2}+2C_{3}$ and $C_{4}:=C_{4}-C_{3}$
$C_{2}:=C_{2}+3C_{3}$ and $C_{4}:=C_{4}-2C_{3}$
$C_{2}:=C_{2}+3C_{3}$ and $C_{4}:=C_{4}+2C_{3}$
$C_{2}:=C_{2}-C_{3}$ and $C_{4}:=C_{4}-2C_{3}$
$C_{2}:=C_{2}-3C_{3}$ and $C_{4}:=C_{4}-2C_{3}$

To transform $A$ into $B,$ we need to make entries in row 3 other than $a_{33}=1$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{bmatrix}5 & 0 & 2 & 7 \\ 1 & -7 & -4 & -6 \\ -1 & 3 & 1 & 2 \\ 2 & 7 & 2 & 3\end{bmatrix}
\xrightarrow{C_{1}:=C_{1}+C_{3}}\begin{bmatrix}7 & 0 & 2 & 7 \\ -3 & -7 & -4 & -6 \\ 0 & 3 & 1 & 2 \\ 4 & 7 & 2 & 3\end{bmatrix}
\xrightarrow{C_{2}:=C_{2}-3C_{3}}\begin{bmatrix}7 & -6 & 2 & 7 \\ -3 & 5 & -4 & -6 \\ 0 & 0 & 1 & 2 \\ 4 & 1 & 2 & 3\end{bmatrix}
\xrightarrow{C_{4}:=C_{4}-2C_{3}}\begin{bmatrix}7 & -6 & 2 & 3 \\ -3 & 5 & -4 & 2 \\ 0 & 0 & 1 & 0 \\ 4 & 1 & 2 & -1\end{bmatrix}=B
$$

Therefore, the corresponding elementary column operations are

$C_{2}:=C_{2}-3C_{3}$ and $C_{4}:=C_{4}-2C_{3}$.

$$
A=\begin{bmatrix}5 & 0 & 2 & 7 \\ 1 & -7 & -4 & -6 \\ -1 & 3 & 1 & 2 \\ 2 & 7 & 2 & 3\end{bmatrix},\,B=\begin{bmatrix}7 & -6 & 2 & 3 \\ -3 & 5 & -4 & 2 \\ 0 & 0 & 1 & 0 \\ 4 & 1 & 2 & -1\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations

- $C_{1}:=\ldots$
- $C_{2}:=C_{2}-3C_{3}$
- $C_{4}:=\ldots$

each of the form $C_i:=C_i+kC_{3},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

$C_{1}:=C_{1}-2C_{3}$ and $C_{4}:=C_{4}-C_{3}$
$C_{1}:=C_{1}-C_{3}$ and $C_{4}:=C_{4}-2C_{3}$
$C_{1}:=C_{1}-C_{3}$ and $C_{4}:=C_{4}+2C_{3}$
$C_{1}:=C_{1}+3C_{3}$ and $C_{4}:=C_{4}-2C_{3}$
$C_{1}:=C_{1}+C_{3}$ and $C_{4}:=C_{4}-2C_{3}$

To transform $A$ into $B,$ we need to make entries in row 3 other than $a_{33}=1$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{bmatrix}5 & 0 & 2 & 7 \\ 1 & -7 & -4 & -6 \\ -1 & 3 & 1 & 2 \\ 2 & 7 & 2 & 3\end{bmatrix}
\xrightarrow{C_{1}:=C_{1}+C_{3}}\begin{bmatrix}7 & 0 & 2 & 7 \\ -3 & -7 & -4 & -6 \\ 0 & 3 & 1 & 2 \\ 4 & 7 & 2 & 3\end{bmatrix}
\xrightarrow{C_{2}:=C_{2}-3C_{3}}\begin{bmatrix}7 & -6 & 2 & 7 \\ -3 & 5 & -4 & -6 \\ 0 & 0 & 1 & 2 \\ 4 & 1 & 2 & 3\end{bmatrix}
\xrightarrow{C_{4}:=C_{4}-2C_{3}}\begin{bmatrix}7 & -6 & 2 & 3 \\ -3 & 5 & -4 & 2 \\ 0 & 0 & 1 & 0 \\ 4 & 1 & 2 & -1\end{bmatrix}=B
$$

Therefore, the corresponding elementary column operations are

$C_{1}:=C_{1}+C_{3}$ and $C_{4}:=C_{4}-2C_{3}$.

## Changed given-column with matrix held constant

$$
A=\begin{bmatrix}5 & 0 & 0 & 7 \\ -8 & 2 & 4 & 8 \\ 5 & -1 & 3 & -2 \\ 2 & 0 & 4 & 1\end{bmatrix},\,B=\begin{bmatrix}5 & 0 & 0 & 7 \\ 2 & 2 & 10 & 4 \\ 0 & -1 & 0 & 0 \\ 2 & 0 & 4 & 1\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations

- $C_{1}:=C_{1}+5C_{2}$
- $C_{3}:=\ldots$
- $C_{4}:=\ldots$

each of the form $C_i:=C_i+kC_{2},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

$C_{3}:=C_{3}+3C_{2}$ and $C_{4}:=C_{4}+2C_{2}$
$C_{3}:=C_{3}+3C_{2}$ and $C_{4}:=C_{4}-2C_{2}$
$C_{3}:=C_{3}+2C_{2}$ and $C_{4}:=C_{4}-3C_{2}$
$C_{3}:=C_{3}-3C_{2}$ and $C_{4}:=C_{4}+2C_{2}$
$C_{3}:=C_{3}-3C_{2}$ and $C_{4}:=C_{4}-2C_{2}$

To transform $A$ into $B,$ we need to make entries in row 3 other than $a_{32}=-1$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{bmatrix}5 & 0 & 0 & 7 \\ -8 & 2 & 4 & 8 \\ 5 & -1 & 3 & -2 \\ 2 & 0 & 4 & 1\end{bmatrix}
\xrightarrow{C_{1}:=C_{1}+5C_{2}}\begin{bmatrix}5 & 0 & 0 & 7 \\ 2 & 2 & 4 & 8 \\ 0 & -1 & 3 & -2 \\ 2 & 0 & 4 & 1\end{bmatrix}
\xrightarrow{C_{3}:=C_{3}+3C_{2}}\begin{bmatrix}5 & 0 & 0 & 7 \\ 2 & 2 & 10 & 8 \\ 0 & -1 & 0 & -2 \\ 2 & 0 & 4 & 1\end{bmatrix}
\xrightarrow{C_{4}:=C_{4}-2C_{2}}\begin{bmatrix}5 & 0 & 0 & 7 \\ 2 & 2 & 10 & 4 \\ 0 & -1 & 0 & 0 \\ 2 & 0 & 4 & 1\end{bmatrix}=B
$$

Therefore, the corresponding elementary column operations are

$C_{3}:=C_{3}+3C_{2}$ and $C_{4}:=C_{4}-2C_{2}$.

$$
A=\begin{bmatrix}5 & 0 & 0 & 7 \\ -8 & 2 & 4 & 8 \\ 5 & -1 & 3 & -2 \\ 2 & 0 & 4 & 1\end{bmatrix},\,B=\begin{bmatrix}5 & 0 & 0 & 7 \\ 2 & 2 & 10 & 4 \\ 0 & -1 & 0 & 0 \\ 2 & 0 & 4 & 1\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations

- $C_{1}:=\ldots$
- $C_{3}:=C_{3}+3C_{2}$
- $C_{4}:=\ldots$

each of the form $C_i:=C_i+kC_{2},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

$C_{1}:=C_{1}+5C_{2}$ and $C_{4}:=C_{4}+2C_{2}$
$C_{1}:=C_{1}+5C_{2}$ and $C_{4}:=C_{4}-2C_{2}$
$C_{1}:=C_{1}+2C_{2}$ and $C_{4}:=C_{4}-5C_{2}$
$C_{1}:=C_{1}-5C_{2}$ and $C_{4}:=C_{4}+2C_{2}$
$C_{1}:=C_{1}-5C_{2}$ and $C_{4}:=C_{4}-2C_{2}$

To transform $A$ into $B,$ we need to make entries in row 3 other than $a_{32}=-1$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{bmatrix}5 & 0 & 0 & 7 \\ -8 & 2 & 4 & 8 \\ 5 & -1 & 3 & -2 \\ 2 & 0 & 4 & 1\end{bmatrix}
\xrightarrow{C_{1}:=C_{1}+5C_{2}}\begin{bmatrix}5 & 0 & 0 & 7 \\ 2 & 2 & 4 & 8 \\ 0 & -1 & 3 & -2 \\ 2 & 0 & 4 & 1\end{bmatrix}
\xrightarrow{C_{3}:=C_{3}+3C_{2}}\begin{bmatrix}5 & 0 & 0 & 7 \\ 2 & 2 & 10 & 8 \\ 0 & -1 & 0 & -2 \\ 2 & 0 & 4 & 1\end{bmatrix}
\xrightarrow{C_{4}:=C_{4}-2C_{2}}\begin{bmatrix}5 & 0 & 0 & 7 \\ 2 & 2 & 10 & 4 \\ 0 & -1 & 0 & 0 \\ 2 & 0 & 4 & 1\end{bmatrix}=B
$$

Therefore, the corresponding elementary column operations are

$C_{1}:=C_{1}+5C_{2}$ and $C_{4}:=C_{4}-2C_{2}$.

## Changed given-column with matrix held constant

$$
A=\begin{bmatrix}7 & 5 & 6 & -9 \\ 6 & 4 & 2 & -6 \\ -7 & 2 & -3 & 6 \\ 5 & 6 & 1 & 8\end{bmatrix},\,B=\begin{bmatrix}-11 & -7 & 6 & 9 \\ 0 & 0 & 2 & 0 \\ 2 & 8 & -3 & -3 \\ 2 & 4 & 1 & 11\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations

- $C_{1}:=C_{1}-3C_{3}$
- $C_{2}:=\ldots$
- $C_{4}:=\ldots$

each of the form $C_i:=C_i+kC_{3},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

$C_{2}:=C_{2}-3C_{3}$ and $C_{4}:=C_{4}+2C_{3}$
$C_{2}:=C_{2}+2C_{3}$ and $C_{4}:=C_{4}+3C_{3}$
$C_{2}:=C_{2}+2C_{3}$ and $C_{4}:=C_{4}-3C_{3}$
$C_{2}:=C_{2}-2C_{3}$ and $C_{4}:=C_{4}+3C_{3}$
$C_{2}:=C_{2}-2C_{3}$ and $C_{4}:=C_{4}-3C_{3}$

To transform $A$ into $B,$ we need to make entries in row 2 other than $a_{23}=2$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{bmatrix}7 & 5 & 6 & -9 \\ 6 & 4 & 2 & -6 \\ -7 & 2 & -3 & 6 \\ 5 & 6 & 1 & 8\end{bmatrix}
\xrightarrow{C_{1}:=C_{1}-3C_{3}}\begin{bmatrix}-11 & 5 & 6 & -9 \\ 0 & 4 & 2 & -6 \\ 2 & 2 & -3 & 6 \\ 2 & 6 & 1 & 8\end{bmatrix}
\xrightarrow{C_{2}:=C_{2}-2C_{3}}\begin{bmatrix}-11 & -7 & 6 & -9 \\ 0 & 0 & 2 & -6 \\ 2 & 8 & -3 & 6 \\ 2 & 4 & 1 & 8\end{bmatrix}
\xrightarrow{C_{4}:=C_{4}+3C_{3}}\begin{bmatrix}-11 & -7 & 6 & 9 \\ 0 & 0 & 2 & 0 \\ 2 & 8 & -3 & -3 \\ 2 & 4 & 1 & 11\end{bmatrix}=B
$$

Therefore, the corresponding elementary column operations are

$C_{2}:=C_{2}-2C_{3}$ and $C_{4}:=C_{4}+3C_{3}$.

$$
A=\begin{bmatrix}7 & 5 & 6 & -9 \\ 6 & 4 & 2 & -6 \\ -7 & 2 & -3 & 6 \\ 5 & 6 & 1 & 8\end{bmatrix},\,B=\begin{bmatrix}-11 & -7 & 6 & 9 \\ 0 & 0 & 2 & 0 \\ 2 & 8 & -3 & -3 \\ 2 & 4 & 1 & 11\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations

- $C_{1}:=\ldots$
- $C_{2}:=\ldots$
- $C_{4}:=C_{4}+3C_{3}$

each of the form $C_i:=C_i+kC_{3},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

$C_{1}:=C_{1}+2C_{3}$ and $C_{2}:=C_{2}+3C_{3}$
$C_{1}:=C_{1}+3C_{3}$ and $C_{2}:=C_{2}-2C_{3}$
$C_{1}:=C_{1}+3C_{3}$ and $C_{2}:=C_{2}+2C_{3}$
$C_{1}:=C_{1}-3C_{3}$ and $C_{2}:=C_{2}-2C_{3}$
$C_{1}:=C_{1}-3C_{3}$ and $C_{2}:=C_{2}+2C_{3}$

To transform $A$ into $B,$ we need to make entries in row 2 other than $a_{23}=2$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{bmatrix}7 & 5 & 6 & -9 \\ 6 & 4 & 2 & -6 \\ -7 & 2 & -3 & 6 \\ 5 & 6 & 1 & 8\end{bmatrix}
\xrightarrow{C_{1}:=C_{1}-3C_{3}}\begin{bmatrix}-11 & 5 & 6 & -9 \\ 0 & 4 & 2 & -6 \\ 2 & 2 & -3 & 6 \\ 2 & 6 & 1 & 8\end{bmatrix}
\xrightarrow{C_{2}:=C_{2}-2C_{3}}\begin{bmatrix}-11 & -7 & 6 & -9 \\ 0 & 0 & 2 & -6 \\ 2 & 8 & -3 & 6 \\ 2 & 4 & 1 & 8\end{bmatrix}
\xrightarrow{C_{4}:=C_{4}+3C_{3}}\begin{bmatrix}-11 & -7 & 6 & 9 \\ 0 & 0 & 2 & 0 \\ 2 & 8 & -3 & -3 \\ 2 & 4 & 1 & 11\end{bmatrix}=B
$$

Therefore, the corresponding elementary column operations are

$C_{1}:=C_{1}-3C_{3}$ and $C_{2}:=C_{2}-2C_{3}$.

## Changed given-column with matrix held constant

$$
A=\begin{bmatrix}-1 & 2 & 2 & 3 \\ 1 & 3 & 1 & -2 \\ 3 & 1 & 4 & -2 \\ 4 & -2 & -3 & -4\end{bmatrix},\,B=\begin{bmatrix}-3 & -4 & 2 & 7 \\ 0 & 0 & 1 & 0 \\ -1 & -11 & 4 & 6 \\ 7 & 7 & -3 & -10\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations

- $C_{1}:=\ldots$
- $C_{2}:=\ldots$
- $C_{4}:=C_{4}+2C_{3}$

each of the form $C_i:=C_i+kC_{3},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

$C_{1}:=C_{1}-C_{3}$ and $C_{2}:=C_{2}-C_{3}$
$C_{1}:=C_{1}-C_{3}$ and $C_{2}:=C_{2}-3C_{3}$
$C_{1}:=C_{1}-3C_{3}$ and $C_{2}:=C_{2}-C_{3}$
$C_{1}:=C_{1}-C_{3}$ and $C_{2}:=C_{2}+3C_{3}$
$C_{1}:=C_{1}+C_{3}$ and $C_{2}:=C_{2}-3C_{3}$

To transform $A$ into $B,$ we need to make entries in row 2 other than $a_{23}=1$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{bmatrix}-1 & 2 & 2 & 3 \\ 1 & 3 & 1 & -2 \\ 3 & 1 & 4 & -2 \\ 4 & -2 & -3 & -4\end{bmatrix}
\xrightarrow{C_{1}:=C_{1}-C_{3}}\begin{bmatrix}-3 & 2 & 2 & 3 \\ 0 & 3 & 1 & -2 \\ -1 & 1 & 4 & -2 \\ 7 & -2 & -3 & -4\end{bmatrix}
\xrightarrow{C_{2}:=C_{2}-3C_{3}}\begin{bmatrix}-3 & -4 & 2 & 3 \\ 0 & 0 & 1 & -2 \\ -1 & -11 & 4 & -2 \\ 7 & 7 & -3 & -4\end{bmatrix}
\xrightarrow{C_{4}:=C_{4}+2C_{3}}\begin{bmatrix}-3 & -4 & 2 & 7 \\ 0 & 0 & 1 & 0 \\ -1 & -11 & 4 & 6 \\ 7 & 7 & -3 & -10\end{bmatrix}=B
$$

Therefore, the corresponding elementary column operations are

$C_{1}:=C_{1}-C_{3}$ and $C_{2}:=C_{2}-3C_{3}$.

$$
A=\begin{bmatrix}-1 & 2 & 2 & 3 \\ 1 & 3 & 1 & -2 \\ 3 & 1 & 4 & -2 \\ 4 & -2 & -3 & -4\end{bmatrix},\,B=\begin{bmatrix}-3 & -4 & 2 & 7 \\ 0 & 0 & 1 & 0 \\ -1 & -11 & 4 & 6 \\ 7 & 7 & -3 & -10\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations

- $C_{1}:=C_{1}-C_{3}$
- $C_{2}:=\ldots$
- $C_{4}:=\ldots$

each of the form $C_i:=C_i+kC_{3},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

$C_{2}:=C_{2}-3C_{3}$ and $C_{4}:=C_{4}+C_{3}$
$C_{2}:=C_{2}-3C_{3}$ and $C_{4}:=C_{4}+2C_{3}$
$C_{2}:=C_{2}+2C_{3}$ and $C_{4}:=C_{4}-3C_{3}$
$C_{2}:=C_{2}-3C_{3}$ and $C_{4}:=C_{4}-2C_{3}$
$C_{2}:=C_{2}+3C_{3}$ and $C_{4}:=C_{4}+2C_{3}$

To transform $A$ into $B,$ we need to make entries in row 2 other than $a_{23}=1$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{bmatrix}-1 & 2 & 2 & 3 \\ 1 & 3 & 1 & -2 \\ 3 & 1 & 4 & -2 \\ 4 & -2 & -3 & -4\end{bmatrix}
\xrightarrow{C_{1}:=C_{1}-C_{3}}\begin{bmatrix}-3 & 2 & 2 & 3 \\ 0 & 3 & 1 & -2 \\ -1 & 1 & 4 & -2 \\ 7 & -2 & -3 & -4\end{bmatrix}
\xrightarrow{C_{2}:=C_{2}-3C_{3}}\begin{bmatrix}-3 & -4 & 2 & 3 \\ 0 & 0 & 1 & -2 \\ -1 & -11 & 4 & -2 \\ 7 & 7 & -3 & -4\end{bmatrix}
\xrightarrow{C_{4}:=C_{4}+2C_{3}}\begin{bmatrix}-3 & -4 & 2 & 7 \\ 0 & 0 & 1 & 0 \\ -1 & -11 & 4 & 6 \\ 7 & 7 & -3 & -10\end{bmatrix}=B
$$

Therefore, the corresponding elementary column operations are

$C_{2}:=C_{2}-3C_{3}$ and $C_{4}:=C_{4}+2C_{3}$.

## Changed given-column with matrix held constant

$$
A=\begin{bmatrix}1 & 4 & 7 & 7 \\ -7 & -4 & 2 & -1 \\ 4 & 1 & 3 & 2 \\ 1 & 5 & 1 & 8\end{bmatrix},\,B=\begin{bmatrix}-15 & 4 & -5 & -1 \\ 9 & -4 & 14 & 7 \\ 0 & 1 & 0 & 0 \\ -19 & 5 & -14 & -2\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations

- $C_{1}:=\ldots$
- $C_{3}:=C_{3}-3C_{2}$
- $C_{4}:=\ldots$

each of the form $C_i:=C_i+kC_{2},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

$C_{1}:=C_{1}-4C_{2}$ and $C_{4}:=C_{4}-2C_{2}$
$C_{1}:=C_{1}-2C_{2}$ and $C_{4}:=C_{4}-4C_{2}$
$C_{1}:=C_{1}+4C_{2}$ and $C_{4}:=C_{4}+2C_{2}$
$C_{1}:=C_{1}+2C_{2}$ and $C_{4}:=C_{4}+4C_{2}$
$C_{1}:=C_{1}-4C_{2}$ and $C_{4}:=C_{4}+2C_{2}$

To transform $A$ into $B,$ we need to make entries in row 3 other than $a_{32}=1$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{bmatrix}1 & 4 & 7 & 7 \\ -7 & -4 & 2 & -1 \\ 4 & 1 & 3 & 2 \\ 1 & 5 & 1 & 8\end{bmatrix}
\xrightarrow{C_{1}:=C_{1}-4C_{2}}\begin{bmatrix}-15 & 4 & 7 & 7 \\ 9 & -4 & 2 & -1 \\ 0 & 1 & 3 & 2 \\ -19 & 5 & 1 & 8\end{bmatrix}
\xrightarrow{C_{3}:=C_{3}-3C_{2}}\begin{bmatrix}-15 & 4 & -5 & 7 \\ 9 & -4 & 14 & -1 \\ 0 & 1 & 0 & 2 \\ -19 & 5 & -14 & 8\end{bmatrix}
\xrightarrow{C_{4}:=C_{4}-2C_{2}}\begin{bmatrix}-15 & 4 & -5 & -1 \\ 9 & -4 & 14 & 7 \\ 0 & 1 & 0 & 0 \\ -19 & 5 & -14 & -2\end{bmatrix}=B
$$

Therefore, the corresponding elementary column operations are

$C_{1}:=C_{1}-4C_{2}$ and $C_{4}:=C_{4}-2C_{2}$.

$$
A=\begin{bmatrix}1 & 4 & 7 & 7 \\ -7 & -4 & 2 & -1 \\ 4 & 1 & 3 & 2 \\ 1 & 5 & 1 & 8\end{bmatrix},\,B=\begin{bmatrix}-15 & 4 & -5 & -1 \\ 9 & -4 & 14 & 7 \\ 0 & 1 & 0 & 0 \\ -19 & 5 & -14 & -2\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations

- $C_{1}:=C_{1}-4C_{2}$
- $C_{3}:=\ldots$
- $C_{4}:=\ldots$

each of the form $C_i:=C_i+kC_{2},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

$C_{3}:=C_{3}-3C_{2}$ and $C_{4}:=C_{4}-2C_{2}$
$C_{3}:=C_{3}-2C_{2}$ and $C_{4}:=C_{4}-3C_{2}$
$C_{3}:=C_{3}+3C_{2}$ and $C_{4}:=C_{4}+2C_{2}$
$C_{3}:=C_{3}+2C_{2}$ and $C_{4}:=C_{4}+3C_{2}$
$C_{3}:=C_{3}-3C_{2}$ and $C_{4}:=C_{4}+2C_{2}$

To transform $A$ into $B,$ we need to make entries in row 3 other than $a_{32}=1$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{bmatrix}1 & 4 & 7 & 7 \\ -7 & -4 & 2 & -1 \\ 4 & 1 & 3 & 2 \\ 1 & 5 & 1 & 8\end{bmatrix}
\xrightarrow{C_{1}:=C_{1}-4C_{2}}\begin{bmatrix}-15 & 4 & 7 & 7 \\ 9 & -4 & 2 & -1 \\ 0 & 1 & 3 & 2 \\ -19 & 5 & 1 & 8\end{bmatrix}
\xrightarrow{C_{3}:=C_{3}-3C_{2}}\begin{bmatrix}-15 & 4 & -5 & 7 \\ 9 & -4 & 14 & -1 \\ 0 & 1 & 0 & 2 \\ -19 & 5 & -14 & 8\end{bmatrix}
\xrightarrow{C_{4}:=C_{4}-2C_{2}}\begin{bmatrix}-15 & 4 & -5 & -1 \\ 9 & -4 & 14 & 7 \\ 0 & 1 & 0 & 0 \\ -19 & 5 & -14 & -2\end{bmatrix}=B
$$

Therefore, the corresponding elementary column operations are

$C_{3}:=C_{3}-3C_{2}$ and $C_{4}:=C_{4}-2C_{2}$.

## Changed given-column with matrix held constant

$$
A=\begin{bmatrix}1 & 1 & 6 & 1 \\ 8 & 1 & 2 & 5 \\ 0 & 9 & -5 & 4 \\ 4 & 5 & 3 & 1\end{bmatrix},\,B=\begin{bmatrix}-3 & -4 & 3 & 1 \\ -12 & -24 & -13 & 5 \\ -16 & -11 & -17 & 4 \\ 0 & 0 & 0 & 1\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations

- $C_{1}:=C_{1}-4C_{4}$
- $C_{2}:=\ldots$
- $C_{3}:=\ldots$

each of the form $C_i:=C_i+kC_{4},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

$C_{2}:=C_{2}+3C_{4}$ and $C_{3}:=C_{3}+5C_{4}$
$C_{2}:=C_{2}+5C_{4}$ and $C_{3}:=C_{3}+3C_{4}$
$C_{2}:=C_{2}-5C_{4}$ and $C_{3}:=C_{3}-3C_{4}$
$C_{2}:=C_{2}-3C_{4}$ and $C_{3}:=C_{3}-5C_{4}$
$C_{2}:=C_{2}-5C_{4}$ and $C_{3}:=C_{3}+3C_{4}$

To transform $A$ into $B,$ we need to make entries in row 4 other than $a_{44}=1$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{bmatrix}1 & 1 & 6 & 1 \\ 8 & 1 & 2 & 5 \\ 0 & 9 & -5 & 4 \\ 4 & 5 & 3 & 1\end{bmatrix}
\xrightarrow{C_{1}:=C_{1}-4C_{4}}\begin{bmatrix}-3 & 1 & 6 & 1 \\ -12 & 1 & 2 & 5 \\ -16 & 9 & -5 & 4 \\ 0 & 5 & 3 & 1\end{bmatrix}
\xrightarrow{C_{2}:=C_{2}-5C_{4}}\begin{bmatrix}-3 & -4 & 6 & 1 \\ -12 & -24 & 2 & 5 \\ -16 & -11 & -5 & 4 \\ 0 & 0 & 3 & 1\end{bmatrix}
\xrightarrow{C_{3}:=C_{3}-3C_{4}}\begin{bmatrix}-3 & -4 & 3 & 1 \\ -12 & -24 & -13 & 5 \\ -16 & -11 & -17 & 4 \\ 0 & 0 & 0 & 1\end{bmatrix}=B
$$

Therefore, the corresponding elementary column operations are

$C_{2}:=C_{2}-5C_{4}$ and $C_{3}:=C_{3}-3C_{4}$.

$$
A=\begin{bmatrix}1 & 1 & 6 & 1 \\ 8 & 1 & 2 & 5 \\ 0 & 9 & -5 & 4 \\ 4 & 5 & 3 & 1\end{bmatrix},\,B=\begin{bmatrix}-3 & -4 & 3 & 1 \\ -12 & -24 & -13 & 5 \\ -16 & -11 & -17 & 4 \\ 0 & 0 & 0 & 1\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations

- $C_{1}:=\ldots$
- $C_{2}:=C_{2}-5C_{4}$
- $C_{3}:=\ldots$

each of the form $C_i:=C_i+kC_{4},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

$C_{1}:=C_{1}+3C_{4}$ and $C_{3}:=C_{3}+4C_{4}$
$C_{1}:=C_{1}+4C_{4}$ and $C_{3}:=C_{3}+3C_{4}$
$C_{1}:=C_{1}-4C_{4}$ and $C_{3}:=C_{3}-3C_{4}$
$C_{1}:=C_{1}-3C_{4}$ and $C_{3}:=C_{3}-4C_{4}$
$C_{1}:=C_{1}-4C_{4}$ and $C_{3}:=C_{3}+3C_{4}$

To transform $A$ into $B,$ we need to make entries in row 4 other than $a_{44}=1$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{bmatrix}1 & 1 & 6 & 1 \\ 8 & 1 & 2 & 5 \\ 0 & 9 & -5 & 4 \\ 4 & 5 & 3 & 1\end{bmatrix}
\xrightarrow{C_{1}:=C_{1}-4C_{4}}\begin{bmatrix}-3 & 1 & 6 & 1 \\ -12 & 1 & 2 & 5 \\ -16 & 9 & -5 & 4 \\ 0 & 5 & 3 & 1\end{bmatrix}
\xrightarrow{C_{2}:=C_{2}-5C_{4}}\begin{bmatrix}-3 & -4 & 6 & 1 \\ -12 & -24 & 2 & 5 \\ -16 & -11 & -5 & 4 \\ 0 & 0 & 3 & 1\end{bmatrix}
\xrightarrow{C_{3}:=C_{3}-3C_{4}}\begin{bmatrix}-3 & -4 & 3 & 1 \\ -12 & -24 & -13 & 5 \\ -16 & -11 & -17 & 4 \\ 0 & 0 & 0 & 1\end{bmatrix}=B
$$

Therefore, the corresponding elementary column operations are

$C_{1}:=C_{1}-4C_{4}$ and $C_{3}:=C_{3}-3C_{4}$.

## Changed given-column with matrix held constant

$$
A=\begin{bmatrix}1 & 1 & 0 & 2 \\ 1 & 7 & 3 & 9 \\ 2 & 3 & 0 & 1 \\ 2 & 1 & 1 & 7\end{bmatrix},\,B=\begin{bmatrix}1 & 1 & 0 & 2 \\ -5 & 4 & 3 & -12 \\ 2 & 3 & 0 & 1 \\ 0 & 0 & 1 & 0\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations

- $C_{1}:=\ldots$
- $C_{2}:=C_{2}-C_{3}$
- $C_{4}:=\ldots$

each of the form $C_i:=C_i+kC_{3},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

$C_{1}:=C_{1}-2C_{3}$ and $C_{4}:=C_{4}-7C_{3}$
$C_{1}:=C_{1}-2C_{3}$ and $C_{4}:=C_{4}-C_{3}$
$C_{1}:=C_{1}-7C_{3}$ and $C_{4}:=C_{4}-2C_{3}$
$C_{1}:=C_{1}-2C_{3}$ and $C_{4}:=C_{4}+7C_{3}$
$C_{1}:=C_{1}+2C_{3}$ and $C_{4}:=C_{4}+7C_{3}$

To transform $A$ into $B,$ we need to make entries in row 4 other than $a_{43}=1$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{bmatrix}1 & 1 & 0 & 2 \\ 1 & 7 & 3 & 9 \\ 2 & 3 & 0 & 1 \\ 2 & 1 & 1 & 7\end{bmatrix}
\xrightarrow{C_{1}:=C_{1}-2C_{3}}\begin{bmatrix}1 & 1 & 0 & 2 \\ -5 & 7 & 3 & 9 \\ 2 & 3 & 0 & 1 \\ 0 & 1 & 1 & 7\end{bmatrix}
\xrightarrow{C_{2}:=C_{2}-C_{3}}\begin{bmatrix}1 & 1 & 0 & 2 \\ -5 & 4 & 3 & 9 \\ 2 & 3 & 0 & 1 \\ 0 & 0 & 1 & 7\end{bmatrix}
\xrightarrow{C_{4}:=C_{4}-7C_{3}}\begin{bmatrix}1 & 1 & 0 & 2 \\ -5 & 4 & 3 & -12 \\ 2 & 3 & 0 & 1 \\ 0 & 0 & 1 & 0\end{bmatrix}=B
$$

Therefore, the corresponding elementary column operations are

$C_{1}:=C_{1}-2C_{3}$ and $C_{4}:=C_{4}-7C_{3}$.

$$
A=\begin{bmatrix}1 & 1 & 0 & 2 \\ 1 & 7 & 3 & 9 \\ 2 & 3 & 0 & 1 \\ 2 & 1 & 1 & 7\end{bmatrix},\,B=\begin{bmatrix}1 & 1 & 0 & 2 \\ -5 & 4 & 3 & -12 \\ 2 & 3 & 0 & 1 \\ 0 & 0 & 1 & 0\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations

- $C_{1}:=C_{1}-2C_{3}$
- $C_{2}:=\ldots$
- $C_{4}:=\ldots$

each of the form $C_i:=C_i+kC_{3},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

$C_{2}:=C_{2}-C_{3}$ and $C_{4}:=C_{4}-7C_{3}$
$C_{2}:=C_{2}-C_{3}$ and $C_{4}:=C_{4}-C_{3}$
$C_{2}:=C_{2}-7C_{3}$ and $C_{4}:=C_{4}-C_{3}$
$C_{2}:=C_{2}-C_{3}$ and $C_{4}:=C_{4}+7C_{3}$
$C_{2}:=C_{2}+C_{3}$ and $C_{4}:=C_{4}+7C_{3}$

To transform $A$ into $B,$ we need to make entries in row 4 other than $a_{43}=1$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{bmatrix}1 & 1 & 0 & 2 \\ 1 & 7 & 3 & 9 \\ 2 & 3 & 0 & 1 \\ 2 & 1 & 1 & 7\end{bmatrix}
\xrightarrow{C_{1}:=C_{1}-2C_{3}}\begin{bmatrix}1 & 1 & 0 & 2 \\ -5 & 7 & 3 & 9 \\ 2 & 3 & 0 & 1 \\ 0 & 1 & 1 & 7\end{bmatrix}
\xrightarrow{C_{2}:=C_{2}-C_{3}}\begin{bmatrix}1 & 1 & 0 & 2 \\ -5 & 4 & 3 & 9 \\ 2 & 3 & 0 & 1 \\ 0 & 0 & 1 & 7\end{bmatrix}
\xrightarrow{C_{4}:=C_{4}-7C_{3}}\begin{bmatrix}1 & 1 & 0 & 2 \\ -5 & 4 & 3 & -12 \\ 2 & 3 & 0 & 1 \\ 0 & 0 & 1 & 0\end{bmatrix}=B
$$

Therefore, the corresponding elementary column operations are

$C_{2}:=C_{2}-C_{3}$ and $C_{4}:=C_{4}-7C_{3}$.

## Changed given-column with matrix held constant

$$
A=\begin{bmatrix}-4 & 4 & -2 & 8 \\ -6 & 9 & -3 & 7 \\ 4 & 2 & 1 & -8 \\ 5 & 4 & 3 & 3\end{bmatrix},\,B=\begin{bmatrix}0 & 0 & -2 & 0 \\ 0 & 3 & -3 & -5 \\ 2 & 4 & 1 & -4 \\ -1 & 10 & 3 & 15\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations

- $C_{1}:=\ldots$
- $C_{2}:=C_{2}+2C_{3}$
- $C_{4}:=\ldots$

each of the form $C_i:=C_i+kC_{3},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

$C_{1}:=C_{1}-4C_{3}$ and $C_{4}:=C_{4}+2C_{3}$
$C_{1}:=C_{1}+2C_{3}$ and $C_{4}:=C_{4}-4C_{3}$
$C_{1}:=C_{1}+2C_{3}$ and $C_{4}:=C_{4}+4C_{3}$
$C_{1}:=C_{1}-2C_{3}$ and $C_{4}:=C_{4}-4C_{3}$
$C_{1}:=C_{1}-2C_{3}$ and $C_{4}:=C_{4}+4C_{3}$

To transform $A$ into $B,$ we need to make entries in row 1 other than $a_{13}=-2$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{bmatrix}-4 & 4 & -2 & 8 \\ -6 & 9 & -3 & 7 \\ 4 & 2 & 1 & -8 \\ 5 & 4 & 3 & 3\end{bmatrix}
\xrightarrow{C_{1}:=C_{1}-2C_{3}}\begin{bmatrix}0 & 4 & -2 & 8 \\ 0 & 9 & -3 & 7 \\ 2 & 2 & 1 & -8 \\ -1 & 4 & 3 & 3\end{bmatrix}
\xrightarrow{C_{2}:=C_{2}+2C_{3}}\begin{bmatrix}0 & 0 & -2 & 8 \\ 0 & 3 & -3 & 7 \\ 2 & 4 & 1 & -8 \\ -1 & 10 & 3 & 3\end{bmatrix}
\xrightarrow{C_{4}:=C_{4}+4C_{3}}\begin{bmatrix}0 & 0 & -2 & 0 \\ 0 & 3 & -3 & -5 \\ 2 & 4 & 1 & -4 \\ -1 & 10 & 3 & 15\end{bmatrix}=B
$$

Therefore, the corresponding elementary column operations are

$C_{1}:=C_{1}-2C_{3}$ and $C_{4}:=C_{4}+4C_{3}$.

$$
A=\begin{bmatrix}-4 & 4 & -2 & 8 \\ -6 & 9 & -3 & 7 \\ 4 & 2 & 1 & -8 \\ 5 & 4 & 3 & 3\end{bmatrix},\,B=\begin{bmatrix}0 & 0 & -2 & 0 \\ 0 & 3 & -3 & -5 \\ 2 & 4 & 1 & -4 \\ -1 & 10 & 3 & 15\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations

- $C_{1}:=C_{1}-2C_{3}$
- $C_{2}:=\ldots$
- $C_{4}:=\ldots$

each of the form $C_i:=C_i+kC_{3},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

$C_{2}:=C_{2}-4C_{3}$ and $C_{4}:=C_{4}-2C_{3}$
$C_{2}:=C_{2}-2C_{3}$ and $C_{4}:=C_{4}-4C_{3}$
$C_{2}:=C_{2}-2C_{3}$ and $C_{4}:=C_{4}+4C_{3}$
$C_{2}:=C_{2}+2C_{3}$ and $C_{4}:=C_{4}-4C_{3}$
$C_{2}:=C_{2}+2C_{3}$ and $C_{4}:=C_{4}+4C_{3}$

To transform $A$ into $B,$ we need to make entries in row 1 other than $a_{13}=-2$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{bmatrix}-4 & 4 & -2 & 8 \\ -6 & 9 & -3 & 7 \\ 4 & 2 & 1 & -8 \\ 5 & 4 & 3 & 3\end{bmatrix}
\xrightarrow{C_{1}:=C_{1}-2C_{3}}\begin{bmatrix}0 & 4 & -2 & 8 \\ 0 & 9 & -3 & 7 \\ 2 & 2 & 1 & -8 \\ -1 & 4 & 3 & 3\end{bmatrix}
\xrightarrow{C_{2}:=C_{2}+2C_{3}}\begin{bmatrix}0 & 0 & -2 & 8 \\ 0 & 3 & -3 & 7 \\ 2 & 4 & 1 & -8 \\ -1 & 10 & 3 & 3\end{bmatrix}
\xrightarrow{C_{4}:=C_{4}+4C_{3}}\begin{bmatrix}0 & 0 & -2 & 0 \\ 0 & 3 & -3 & -5 \\ 2 & 4 & 1 & -4 \\ -1 & 10 & 3 & 15\end{bmatrix}=B
$$

Therefore, the corresponding elementary column operations are

$C_{2}:=C_{2}+2C_{3}$ and $C_{4}:=C_{4}+4C_{3}$.

## Changed given-column with matrix held constant

$$
A=\begin{bmatrix}2 & 8 & 6 & -2 \\ 1 & 4 & 5 & -3 \\ -2 & -5 & -3 & 8 \\ -1 & -1 & -4 & 1\end{bmatrix},\,B=\begin{bmatrix}2 & 0 & -4 & 4 \\ 1 & 0 & 0 & 0 \\ -2 & 3 & 7 & 2 \\ -1 & 3 & 1 & -2\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations

- $C_{2}:=\ldots$
- $C_{3}:=C_{3}-5C_{1}$
- $C_{4}:=\ldots$

each of the form $C_i:=C_i+kC_{1},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

$C_{2}:=C_{2}-4C_{1}$ and $C_{4}:=C_{4}+3C_{1}$
$C_{2}:=C_{2}-3C_{1}$ and $C_{4}:=C_{4}+4C_{1}$
$C_{2}:=C_{2}-2C_{1}$ and $C_{4}:=C_{4}+3C_{1}$
$C_{2}:=C_{2}+4C_{1}$ and $C_{4}:=C_{4}+3C_{1}$
$C_{2}:=C_{2}-4C_{1}$ and $C_{4}:=C_{4}-3C_{1}$

To transform $A$ into $B,$ we need to make entries in row 2 other than $a_{21}=1$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{bmatrix}2 & 8 & 6 & -2 \\ 1 & 4 & 5 & -3 \\ -2 & -5 & -3 & 8 \\ -1 & -1 & -4 & 1\end{bmatrix}
\xrightarrow{C_{2}:=C_{2}-4C_{1}}\begin{bmatrix}2 & 0 & 6 & -2 \\ 1 & 0 & 5 & -3 \\ -2 & 3 & -3 & 8 \\ -1 & 3 & -4 & 1\end{bmatrix}
\xrightarrow{C_{3}:=C_{3}-5C_{1}}\begin{bmatrix}2 & 0 & -4 & -2 \\ 1 & 0 & 0 & -3 \\ -2 & 3 & 7 & 8 \\ -1 & 3 & 1 & 1\end{bmatrix}
\xrightarrow{C_{4}:=C_{4}+3C_{1}}\begin{bmatrix}2 & 0 & -4 & 4 \\ 1 & 0 & 0 & 0 \\ -2 & 3 & 7 & 2 \\ -1 & 3 & 1 & -2\end{bmatrix}=B
$$

Therefore, the corresponding elementary column operations are

$C_{2}:=C_{2}-4C_{1}$ and $C_{4}:=C_{4}+3C_{1}$.

$$
A=\begin{bmatrix}2 & 8 & 6 & -2 \\ 1 & 4 & 5 & -3 \\ -2 & -5 & -3 & 8 \\ -1 & -1 & -4 & 1\end{bmatrix},\,B=\begin{bmatrix}2 & 0 & -4 & 4 \\ 1 & 0 & 0 & 0 \\ -2 & 3 & 7 & 2 \\ -1 & 3 & 1 & -2\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations

- $C_{2}:=C_{2}-4C_{1}$
- $C_{3}:=\ldots$
- $C_{4}:=\ldots$

each of the form $C_i:=C_i+kC_{1},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

$C_{3}:=C_{3}-5C_{1}$ and $C_{4}:=C_{4}+3C_{1}$
$C_{3}:=C_{3}-3C_{1}$ and $C_{4}:=C_{4}+5C_{1}$
$C_{3}:=C_{3}-3C_{1}$ and $C_{4}:=C_{4}+3C_{1}$
$C_{3}:=C_{3}+5C_{1}$ and $C_{4}:=C_{4}+3C_{1}$
$C_{3}:=C_{3}-5C_{1}$ and $C_{4}:=C_{4}-3C_{1}$

To transform $A$ into $B,$ we need to make entries in row 2 other than $a_{21}=1$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{bmatrix}2 & 8 & 6 & -2 \\ 1 & 4 & 5 & -3 \\ -2 & -5 & -3 & 8 \\ -1 & -1 & -4 & 1\end{bmatrix}
\xrightarrow{C_{2}:=C_{2}-4C_{1}}\begin{bmatrix}2 & 0 & 6 & -2 \\ 1 & 0 & 5 & -3 \\ -2 & 3 & -3 & 8 \\ -1 & 3 & -4 & 1\end{bmatrix}
\xrightarrow{C_{3}:=C_{3}-5C_{1}}\begin{bmatrix}2 & 0 & -4 & -2 \\ 1 & 0 & 0 & -3 \\ -2 & 3 & 7 & 8 \\ -1 & 3 & 1 & 1\end{bmatrix}
\xrightarrow{C_{4}:=C_{4}+3C_{1}}\begin{bmatrix}2 & 0 & -4 & 4 \\ 1 & 0 & 0 & 0 \\ -2 & 3 & 7 & 2 \\ -1 & 3 & 1 & -2\end{bmatrix}=B
$$

Therefore, the corresponding elementary column operations are

$C_{3}:=C_{3}-5C_{1}$ and $C_{4}:=C_{4}+3C_{1}$.

## Changed given-column with matrix held constant

$$
A=\begin{bmatrix}2 & 1 & 2 & 3 \\ 0 & 8 & 0 & 4 \\ 6 & 9 & 1 & 3 \\ -6 & -1 & 1 & -6\end{bmatrix},\,B=\begin{bmatrix}0 & 1 & 0 & 0 \\ -16 & 8 & -16 & -20 \\ -12 & 9 & -17 & -24 \\ -4 & -1 & 3 & -3\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations

- $C_{1}:=\ldots$
- $C_{3}:=\ldots$
- $C_{4}:=C_{4}-3C_{2}$

each of the form $C_i:=C_i+kC_{2},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

$C_{1}:=C_{1}-C_{2}$ and $C_{3}:=C_{3}-C_{2}$
$C_{1}:=C_{1}-2C_{2}$ and $C_{3}:=C_{3}-3C_{2}$
$C_{1}:=C_{1}-2C_{2}$ and $C_{3}:=C_{3}-2C_{2}$
$C_{1}:=C_{1}+2C_{2}$ and $C_{3}:=C_{3}+2C_{2}$
$C_{1}:=C_{1}+C_{2}$ and $C_{3}:=C_{3}+C_{2}$

To transform $A$ into $B,$ we need to make entries in row 1 other than $a_{12}=1$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{bmatrix}2 & 1 & 2 & 3 \\ 0 & 8 & 0 & 4 \\ 6 & 9 & 1 & 3 \\ -6 & -1 & 1 & -6\end{bmatrix}
\xrightarrow{C_{1}:=C_{1}-2C_{2}}\begin{bmatrix}0 & 1 & 2 & 3 \\ -16 & 8 & 0 & 4 \\ -12 & 9 & 1 & 3 \\ -4 & -1 & 1 & -6\end{bmatrix}
\xrightarrow{C_{3}:=C_{3}-2C_{2}}\begin{bmatrix}0 & 1 & 0 & 3 \\ -16 & 8 & -16 & 4 \\ -12 & 9 & -17 & 3 \\ -4 & -1 & 3 & -6\end{bmatrix}
\xrightarrow{C_{4}:=C_{4}-3C_{2}}\begin{bmatrix}0 & 1 & 0 & 0 \\ -16 & 8 & -16 & -20 \\ -12 & 9 & -17 & -24 \\ -4 & -1 & 3 & -3\end{bmatrix}=B
$$

Therefore, the corresponding elementary column operations are

$C_{1}:=C_{1}-2C_{2}$ and $C_{3}:=C_{3}-2C_{2}$.

$$
A=\begin{bmatrix}2 & 1 & 2 & 3 \\ 0 & 8 & 0 & 4 \\ 6 & 9 & 1 & 3 \\ -6 & -1 & 1 & -6\end{bmatrix},\,B=\begin{bmatrix}0 & 1 & 0 & 0 \\ -16 & 8 & -16 & -20 \\ -12 & 9 & -17 & -24 \\ -4 & -1 & 3 & -3\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations

- $C_{1}:=C_{1}-2C_{2}$
- $C_{3}:=\ldots$
- $C_{4}:=\ldots$

each of the form $C_i:=C_i+kC_{2},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

$C_{3}:=C_{3}-C_{2}$ and $C_{4}:=C_{4}-C_{2}$
$C_{3}:=C_{3}-2C_{2}$ and $C_{4}:=C_{4}-4C_{2}$
$C_{3}:=C_{3}-2C_{2}$ and $C_{4}:=C_{4}-3C_{2}$
$C_{3}:=C_{3}+2C_{2}$ and $C_{4}:=C_{4}+3C_{2}$
$C_{3}:=C_{3}+C_{2}$ and $C_{4}:=C_{4}+C_{2}$

To transform $A$ into $B,$ we need to make entries in row 1 other than $a_{12}=1$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{bmatrix}2 & 1 & 2 & 3 \\ 0 & 8 & 0 & 4 \\ 6 & 9 & 1 & 3 \\ -6 & -1 & 1 & -6\end{bmatrix}
\xrightarrow{C_{1}:=C_{1}-2C_{2}}\begin{bmatrix}0 & 1 & 2 & 3 \\ -16 & 8 & 0 & 4 \\ -12 & 9 & 1 & 3 \\ -4 & -1 & 1 & -6\end{bmatrix}
\xrightarrow{C_{3}:=C_{3}-2C_{2}}\begin{bmatrix}0 & 1 & 0 & 3 \\ -16 & 8 & -16 & 4 \\ -12 & 9 & -17 & 3 \\ -4 & -1 & 3 & -6\end{bmatrix}
\xrightarrow{C_{4}:=C_{4}-3C_{2}}\begin{bmatrix}0 & 1 & 0 & 0 \\ -16 & 8 & -16 & -20 \\ -12 & 9 & -17 & -24 \\ -4 & -1 & 3 & -3\end{bmatrix}=B
$$

Therefore, the corresponding elementary column operations are

$C_{3}:=C_{3}-2C_{2}$ and $C_{4}:=C_{4}-3C_{2}$.
