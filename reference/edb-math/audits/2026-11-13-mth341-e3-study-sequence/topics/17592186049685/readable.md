# 17592186049685 Finding Determinants Using Row and Column Operations

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186121046 — Introduction

One way to simplify a determinant calculation is to create a row (or column) containing all zeros except for one entry. Then, we can use a Laplace expansion across that row (or column) to compute the determinant.

Let's demonstrate this method on the matrix $A$ below.

$$
A=
	{\left[ \begin{array}{ccc}2 & 1 & {\color{black}1} \\ 1 & 2 & {\color{black}3} \\ 8 & 14 & 17\end{array} \right]}
$$

Notice that we can make entries to the right of $a_{21}=1$ equal to zero using elementary *column* operations.

Since adding a multiple of one column to another column in a matrix does not change the value of its determinant, we obtain

$$
\begin{aligned} & \hspace{0.222em}\hspace{0.167em}\phantom{=}\begin{vmatrix}{\color{blue}{2}} & 1 & 1 \\ {\color{blue}{1}} & {\color{red}{2}} & {\color{red}{3}} \\ {\color{blue}{8}} & 14 & 17\end{vmatrix} &  & \hspace{2em}\begin{aligned}{C}_{2}: &={C}_{2}+(-2){C}_{1} \\ {C}_{3}: &={C}_{3}+(-3){C}_{1}\end{aligned} \\  & =\begin{vmatrix}{\color{blue}{2}} & -3 & -5 \\ {\color{blue}{1}} & {\color{red}{0}} & {\color{red}{0}} \\ {\color{blue}{8}} & -2 & -7\end{vmatrix}.\end{aligned}
$$

Expanding the result along the $2$nd row, we get

$$
\begin{aligned} & \hspace{0.222em}\hspace{0.167em}\phantom{=}\begin{vmatrix}{\color{blue}{2}} & -3 & -5 \\ {\color{blue}{1}} & {\color{red}{0}} & {\color{red}{0}} \\ {\color{blue}{8}} & -2 & -7\end{vmatrix} \\  & ={\color{blue}{1}}\cdot (-1)^{2+1}\begin{vmatrix}-3 & -5 \\ -2 & -7\end{vmatrix} \\  & =-(21-10) \\  & =-11.\end{aligned}
$$



### example 17592186119690 — Reducing a 4x4 Determinant to a 3x3 Determinant Using Row Operations

$$
\begin{vmatrix}{\color{blue}{1}} & 2 & 3 & 1 \\ {\color{red}{2}} & -1 & 5 & -7 \\ {\color{red}{4}} & -2 & 4 & -5 \\ {\color{red}{-3}} & 3 & -3 & -4\end{vmatrix}
$$

Consider the above $4\times 4$ determinant. Find a $3\times 3$ determinant that has the same value.

*Hint: Use elementary row operations to make the entries below $a_{11}$ equal to zero.*

Let's make entries below $a_{11}=1$ equal to zero using elementary row operations.

Since adding a multiple of one row (or column) to another row (or column) in a matrix does not change the value of its determinant, we obtain

$$
\begin{aligned} & \,\,\begin{vmatrix}1 & 2 & 3 & 1 \\ 2 & -1 & 5 & -7 \\ 4 & -2 & 4 & -5 \\ -3 & 3 & -3 & -4\end{vmatrix} &  & \,\begin{aligned}{R}_{2}:={R}_{2}+(-2){R}_{1} \\ {R}_{3}:={R}_{3}+(-4){R}_{1} \\ {R}_{4}:={R}_{4}+3{R}_{1}\end{aligned} \\  & =\begin{vmatrix}1 & 2 & 3 & 1 \\ 0 & -5 & -1 & -9 \\ 0 & -10 & -8 & -9 \\ 0 & 9 & 6 & -1\end{vmatrix}.\end{aligned}
$$

Expanding the result along the $1$st column, we get

$$
\begin{aligned} & \,\,\begin{vmatrix}1 & 2 & 3 & 1 \\ 0 & -5 & -1 & -9 \\ 0 & -10 & -8 & -9 \\ 0 & 9 & 6 & -1\end{vmatrix} \\  & =1\cdot (-1)^{1+1}\begin{vmatrix}-5 & -1 & -9 \\ -10 & -8 & -9 \\ 9 & 6 & -1\end{vmatrix} \\  & =\begin{vmatrix}-5 & -1 & -9 \\ -10 & -8 & -9 \\ 9 & 6 & -1\end{vmatrix}.\end{aligned}
$$

### example 17592186119691 — Reducing a 4x4 Determinant to a 3x3 Determinant Using Column Operations

$$
\begin{vmatrix}2 & 3 & 2 & 2 \\ {\color{red}{-1}} & {\color{red}{2}} & {\color{blue}{1}} & {\color{red}{-3}} \\ 2 & -2 & -2 & 4 \\ -4 & -4 & 3 & 2\end{vmatrix}
$$

Consider the above $4\times 4$ determinant. Find a $3\times 3$ determinant that has the same value.

*Hint: Use elementary column operations to make the entries to the left and to the right of $a_{23}$ equal to zero.*

Let's make entries to the left and to the right of $a_{23}=1$ equal to zero using elementary column operations.

Since adding a multiple of one row (or column) to another row (or column) in a matrix does not change the value of its determinant, we obtain

$$
\begin{aligned} & \,\,\begin{vmatrix}2 & 3 & 2 & 2 \\ -1 & 2 & 1 & -3 \\ 2 & -2 & -2 & 4 \\ -4 & -4 & 3 & 2\end{vmatrix} &  & \,\begin{aligned}{C}_{1}:={C}_{1}+{C}_{3} \\ {C}_{2}:={C}_{2}+(-2){C}_{3} \\ {C}_{4}:={C}_{4}+3{C}_{3}\end{aligned} \\  & =\begin{vmatrix}4 & -1 & 2 & 8 \\ 0 & 0 & 1 & 0 \\ 0 & 2 & -2 & -2 \\ -1 & -10 & 3 & 11\end{vmatrix}.\end{aligned}
$$

Expanding the result along the $2$nd row, we get

$$
\begin{aligned} & \,\,\begin{vmatrix}4 & -1 & 2 & 8 \\ 0 & 0 & 1 & 0 \\ 0 & 2 & -2 & -2 \\ -1 & -10 & 3 & 11\end{vmatrix} \\  & =1\cdot (-1)^{2+3}\begin{vmatrix}4 & -1 & 8 \\ 0 & 2 & -2 \\ -1 & -10 & 11\end{vmatrix} \\  & =-\begin{vmatrix}4 & -1 & 8 \\ 0 & 2 & -2 \\ -1 & -10 & 11\end{vmatrix}.\end{aligned}
$$

### example 17592186119687 — Computing 4x4 Determinants Using Row and Column Operations

Calculate the value of 
$$
\,
{\left| \begin{array}{cccc}1 & - 1 & 3 & 2 \\ 2 & - 4 & - 2 & 6 \\ 1 & - 2 & - 3 & 3 \\ - 3 & 3 & 4 & 2\end{array} \right|}.
$$

*Hint: Use elementary column operations to make the entries to the right of $a_{31}$ equal to zero. You should be able to reduce the given $4 \times 4$ determinant to a $3 \times 3$ determinant.*

Using elementary column operations, let's make entries to the right of $a_{31}=1$ equal to zero.

Since adding a multiple of one row (or column) to another row (or column) in a matrix does not change the value of its determinant, we obtain

$$
\begin{aligned} & \,\,\begin{vmatrix}1 & -1 & 3 & 2 \\ 2 & -4 & -2 & 6 \\ 1 & -2 & -3 & 3 \\ -3 & 3 & 4 & 2\end{vmatrix} &  & \,\begin{aligned}{C}_{2}:={C}_{2}+2{C}_{1} \\ {C}_{3}:={C}_{3}+3{C}_{1} \\ {C}_{4}:={C}_{4}+(-3){C}_{1}\end{aligned} \\  & =\begin{vmatrix}1 & 1 & 6 & -1 \\ 2 & 0 & 4 & 0 \\ 1 & 0 & 0 & 0 \\ -3 & -3 & -5 & 11\end{vmatrix}.\end{aligned}
$$

Expanding the result along the $3$rd row, we get

$$
\begin{aligned} & \,\,\begin{vmatrix}1 & 1 & 6 & -1 \\ 2 & 0 & 4 & 0 \\ 1 & 0 & 0 & 0 \\ -3 & -3 & -5 & 11\end{vmatrix} \\  & =1\cdot (-1)^{3+1}\begin{vmatrix}1 & 6 & -1 \\ 0 & 4 & 0 \\ -3 & -5 & 11\end{vmatrix} \\  & =\begin{vmatrix}1 & 6 & -1 \\ 0 & 4 & 0 \\ -3 & -5 & 11\end{vmatrix} \\  & =4\cdot (-1)^{2+2}\begin{vmatrix}1 & -1 \\ -3 & 11\end{vmatrix} \\  & =4(11-3) \\  & =32.\end{aligned}
$$

## Representative practice (first three per skill; full bank in practice.json)

### Reducing a 4x4 Determinant to a 3x3 Determinant Using Row Operations (14 captured questions)

Question 17592186120434 — None

$$
\displaystyle \begin{vmatrix}1 & -2 & -7 & 10 \\ -9 & -1 & -6 & 9 \\ -7 & 2 & 3 & -11 \\ 2 & 1 & 4 & -7\end{vmatrix}
$$

Consider the above $4 \cdot 4$ determinant. Which of the following $3 \cdot 3$ determinants has the same value?

*Hint: Use elementary row operations to make the entries above $a_{42}$ equal to zero.*

Solution: Apply $R_1:=R_1+2R_4$, $R_2:=R_2+R_4$, and $R_3:=R_3-2R_4$. Adding a multiple of one row to another does not change the determinant, so it becomes

$$
\begin{vmatrix}5&0&1&-4\\-7&0&-2&2\\-11&0&-5&3\\2&1&4&-7\end{vmatrix}.
$$

Expanding down column $2$, the only nonzero entry is $a_{42}=1$. Its cofactor sign is $(-1)^{4+2}=1$. Therefore the original determinant equals

$$
\begin{vmatrix}5&1&-4\\-7&-2&2\\-11&-5&3\end{vmatrix}.
$$

Answer selection: \begin{vmatrix}5 & 1 & -4 \\ -7 & -2 & 2 \\ -11 & -5 & 3\end{vmatrix}

Question 17592186120546 — question.difficulty/easy

$$
\begin{vmatrix}2 & -2 & -3 & {\color{blue}{3}} \\ -3 & -4 & -2 & {\color{red}{12}} \\ -7 & 2 & 3 & {\color{red}{-6}} \\ 1 & 3 & -2 & {\color{red}{-3}}\end{vmatrix}
$$

Consider the above $4\times 4$ determinant. Which of the following $3\times 3$ determinants has the same value?

*Hint: Use elementary row operations to make the entries below ${a}_{14}$ equal to zero.*

Solution: Let's make entries below ${a}_{14}=3$ equal to zero using elementary row operations.

Since adding a multiple of one row (or column) to another row (column) in a matrix does not change the value of its determinant, we obtain

$$
\begin{aligned} & \,\,\begin{vmatrix}2 & -2 & -3 & 3 \\ -3 & -4 & -2 & 12 \\ -7 & 2 & 3 & -6 \\ 1 & 3 & -2 & -3\end{vmatrix} &  & \,\begin{aligned}{R}_{2}:={R}_{2}+(-4){R}_{1} \\ {R}_{3}:={R}_{3}+2{R}_{1} \\ {R}_{4}:={R}_{4}+{R}_{1}\end{aligned} \\  & =\begin{vmatrix}2 & -2 & -3 & 3 \\ -11 & 4 & 10 & 0 \\ -3 & -2 & -3 & 0 \\ 3 & 1 & -5 & 0\end{vmatrix}.\end{aligned}
$$

Expanding the result along the $4$th column, we get

$$
\begin{aligned} & \,\,\begin{vmatrix}2 & -2 & -3 & 3 \\ -11 & 4 & 10 & 0 \\ -3 & -2 & -3 & 0 \\ 3 & 1 & -5 & 0\end{vmatrix} \\  & =3\cdot (-1)^{1+4}\begin{vmatrix}-11 & 4 & 10 \\ -3 & -2 & -3 \\ 3 & 1 & -5\end{vmatrix} \\  & =-3\begin{vmatrix}-11 & 4 & 10 \\ -3 & -2 & -3 \\ 3 & 1 & -5\end{vmatrix}.\end{aligned}
$$

Answer selection: -3\begin{vmatrix}-11 & 4 & 10 \\ -3 & -2 & -3 \\ 3 & 1 & -5\end{vmatrix}

Question 17592186266066 — question.difficulty/easy

$$
\begin{vmatrix}-1 & -3 & 4 & {\color{red}{-6}} \\ 8 & -3 & 5 & {\color{red}{3}} \\ -2 & 4 & -1 & {\color{blue}{3}} \\ -5 & -2 & 1 & {\color{red}{-6}}\end{vmatrix}
$$

Consider the above $4\times 4$ determinant. Which of the following $3\times 3$ determinants has the same value?

*Hint: Use elementary row operations to make the entries above and below ${a}_{34}$ equal to zero.*

Solution: Let's make entries above and below ${a}_{34}=3$ equal to zero using elementary row operations.

Since adding a multiple of one row (or column) to another row (column) in a matrix does not change the value of its determinant, we obtain

$$
\begin{aligned} & \,\,\begin{vmatrix}-1 & -3 & 4 & -6 \\ 8 & -3 & 5 & 3 \\ -2 & 4 & -1 & 3 \\ -5 & -2 & 1 & -6\end{vmatrix} &  & \,\begin{aligned}{R}_{1}:={R}_{1}+2{R}_{3} \\ {R}_{2}:={R}_{2}-{R}_{3} \\ {R}_{4}:={R}_{4}+2{R}_{3}\end{aligned} \\  & =\begin{vmatrix}-5 & 5 & 2 & 0 \\ 10 & -7 & 6 & 0 \\ -2 & 4 & -1 & 3 \\ -9 & 6 & -1 & 0\end{vmatrix}.\end{aligned}
$$

Expanding the result along the $4$th column, we get

$$
\begin{aligned} & \,\,\begin{vmatrix}-5 & 5 & 2 & 0 \\ 10 & -7 & 6 & 0 \\ -2 & 4 & -1 & 3 \\ -9 & 6 & -1 & 0\end{vmatrix} \\  & =3\cdot (-1)^{3+4}\begin{vmatrix}-5 & 5 & 2 \\ 10 & -7 & 6 \\ -9 & 6 & -1\end{vmatrix} \\  & =-3\begin{vmatrix}-5 & 5 & 2 \\ 10 & -7 & 6 \\ -9 & 6 & -1\end{vmatrix}.\end{aligned}
$$

Answer selection: -3\begin{vmatrix}-5 & 5 & 2 \\ 10 & -7 & 6 \\ -9 & 6 & -1\end{vmatrix}

### Reducing a 4x4 Determinant to a 3x3 Determinant Using Column Operations (16 captured questions)

Question 17592186120545 — question.difficulty/easy

$$
\begin{vmatrix}1 & -2 & -7 & 10 \\ -9 & -1 & -6 & 9 \\ {\color{red}{-2}} & {\color{blue}{2}} & {\color{red}{2}} & {\color{red}{-6}} \\ 2 & 1 & 4 & -7\end{vmatrix}
$$

Consider the above $4\times 4$ determinant. Which of the following $3\times 3$ determinants has the same value?

*Hint: Use elementary column operations to make the entries to the left and to the right of ${a}_{32}$ equal to zero.*

Solution: Let's make entries to the left and to the right of ${a}_{32}=2$ equal to zero using elementary column operations.

Since adding a multiple of one row (or column) to another row (column) in a matrix does not change the value of its determinant, we obtain

$$
\begin{aligned} & \,\,\begin{vmatrix}1 & -2 & -7 & 10 \\ -9 & -1 & -6 & 9 \\ -2 & 2 & 2 & -6 \\ 2 & 1 & 4 & -7\end{vmatrix} &  & \,\begin{aligned}{C}_{1}:={C}_{1}+{C}_{2} \\ {C}_{3}:={C}_{3}+(-1){C}_{2} \\ {C}_{4}:={C}_{4}+3{C}_{2}\end{aligned} \\  & =\begin{vmatrix}-1 & -2 & -5 & 4 \\ -10 & -1 & -5 & 6 \\ 0 & 2 & 0 & 0 \\ 3 & 1 & 3 & -4\end{vmatrix}.\end{aligned}
$$

Expanding the result along the $3$rd row, we get

$$
\begin{aligned} & \,\,\begin{vmatrix}-1 & -2 & -5 & 4 \\ -10 & -1 & -5 & 6 \\ 0 & 2 & 0 & 0 \\ 3 & 1 & 3 & -4\end{vmatrix} \\  & =2\cdot (-1)^{3+2}\begin{vmatrix}-1 & -5 & 4 \\ -10 & -5 & 6 \\ 3 & 3 & -4\end{vmatrix} \\  & =-2\begin{vmatrix}-1 & -5 & 4 \\ -10 & -5 & 6 \\ 3 & 3 & -4\end{vmatrix}.\end{aligned}
$$

Answer selection: -2\begin{vmatrix}-1 & -5 & 4 \\ -10 & -5 & 6 \\ 3 & 3 & -4\end{vmatrix}

Question 17592186120547 — question.difficulty/easy

$$
\begin{vmatrix}-2 & -4 & 2 & 1 \\ 3 & 2 & 1 & 2 \\ {\color{red}{6}} & {\color{red}{-4}} & {\color{blue}{2}} & {\color{red}{2}} \\ 2 & -3 & -2 & -3\end{vmatrix}
$$

Consider the above $4\times 4$ determinant. Which of the following $3\times 3$ determinants has the same value?

*Hint: Use elementary column operations to make the entries to the left and to the right of ${a}_{33}$ equal to zero.*

Solution: Let's make entries to the left and to the right of ${a}_{33}=2$ equal to zero using elementary column operations.

Since adding a multiple of one row (or column) to another row (column) in a matrix does not change the value of its determinant, we obtain

$$
\begin{aligned} & \,\,\begin{vmatrix}-2 & -4 & 2 & 1 \\ 3 & 2 & 1 & 2 \\ 6 & -4 & 2 & 2 \\ 2 & -3 & -2 & -3\end{vmatrix} &  & \,\begin{aligned}{C}_{1}:={C}_{1}+(-3){C}_{3} \\ {C}_{2}:={C}_{2}+2{C}_{3} \\ {C}_{4}:={C}_{4}+(-1){C}_{3}\end{aligned} \\  & =\begin{vmatrix}-8 & 0 & 2 & -1 \\ 0 & 4 & 1 & 1 \\ 0 & 0 & 2 & 0 \\ 8 & -7 & -2 & -1\end{vmatrix}.\end{aligned}
$$

Expanding the result along the $3$rd row, we get

$$
\begin{aligned} & \,\,\begin{vmatrix}-8 & 0 & 2 & -1 \\ 0 & 4 & 1 & 1 \\ 0 & 0 & 2 & 0 \\ 8 & -7 & -2 & -1\end{vmatrix} \\  & =2\cdot (-1)^{3+3}\begin{vmatrix}-8 & 0 & -1 \\ 0 & 4 & 1 \\ 8 & -7 & -1\end{vmatrix} \\  & =2\begin{vmatrix}-8 & 0 & -1 \\ 0 & 4 & 1 \\ 8 & -7 & -1\end{vmatrix}.\end{aligned}
$$

Answer selection: 2\begin{vmatrix}-8 & 0 & -1 \\ 0 & 4 & 1 \\ 8 & -7 & -1\end{vmatrix}

Question 17592186266127 — question.difficulty/easy

$$
\begin{vmatrix}{\color{red}{-6}} & {\color{red}{9}} & {\color{red}{-3}} & {\color{blue}{3}} \\ 2 & -4 & 5 & 1 \\ -3 & -5 & -3 & -3 \\ 1 & 10 & -4 & 5\end{vmatrix}
$$

Consider the above $4\times 4$ determinant. Which of the following $3\times 3$ determinants has the same value?

*Hint: Use elementary column operations to make the entries to the left of ${a}_{14}$ equal to zero.*

Solution: Let's make entries to the left of ${a}_{14}=3$ equal to zero using elementary column operations.

Since adding a multiple of one row (or column) to another row (column) in a matrix does not change the value of its determinant, we obtain

$$
\begin{aligned} & \,\,\begin{vmatrix}-6 & 9 & -3 & 3 \\ 2 & -4 & 5 & 1 \\ -3 & -5 & -3 & -3 \\ 1 & 10 & -4 & 5\end{vmatrix} &  & \,\begin{aligned}{C}_{1}:={C}_{1}+2{C}_{4} \\ {C}_{2}:={C}_{2}+(-3){C}_{4} \\ {C}_{3}:={C}_{3}+{C}_{4}\end{aligned} \\  & =\begin{vmatrix}0 & 0 & 0 & 3 \\ 4 & -7 & 6 & 1 \\ -9 & 4 & -6 & -3 \\ 11 & -5 & 1 & 5\end{vmatrix}.\end{aligned}
$$

Expanding the result along the $1$st row, we get

$$
\begin{aligned} & \,\,\begin{vmatrix}0 & 0 & 0 & 3 \\ 4 & -7 & 6 & 1 \\ -9 & 4 & -6 & -3 \\ 11 & -5 & 1 & 5\end{vmatrix} \\  & =3\cdot (-1)^{1+4}\begin{vmatrix}4 & -7 & 6 \\ -9 & 4 & -6 \\ 11 & -5 & 1\end{vmatrix} \\  & =-3\begin{vmatrix}4 & -7 & 6 \\ -9 & 4 & -6 \\ 11 & -5 & 1\end{vmatrix}.\end{aligned}
$$

Answer selection: -3\begin{vmatrix}4 & -7 & 6 \\ -9 & 4 & -6 \\ 11 & -5 & 1\end{vmatrix}

### Computing 4x4 Determinants Using Row and Column Operations (14 captured questions)

Question 17592186120419 — question.difficulty/moderate

Calculate the value of 
$$
\displaystyle \,\begin{vmatrix}1 & 1 & -1 & 1 \\ 1 & 1 & 1 & 2 \\ 1 & 2 & -2 & 3 \\ -1 & -1 & -1 & 1\end{vmatrix}.
$$

*Hint: Use elementary row operations to make the entries below ${a}_{11}$ equal to zero. You should be able to reduce the given $4\times 4$ determinant to a $3\times 3$ determinant.*

Solution: Using elementary row operations, let's make entries below ${a}_{11}=1$ equal to zero.

Since adding a multiple of one row (or column) to another row (column) in a matrix does not change the value of its determinant, we obtain

$$
\begin{aligned} & \,\,\begin{vmatrix}1 & 1 & -1 & 1 \\ 1 & 1 & 1 & 2 \\ 1 & 2 & -2 & 3 \\ -1 & -1 & -1 & 1\end{vmatrix} &  & \,\begin{aligned}{R}_{2}:={R}_{2}+(-1){R}_{1} \\ {R}_{3}:={R}_{3}+(-1){R}_{1} \\ {R}_{4}:={R}_{4}+{R}_{1}\end{aligned} \\  & =\begin{vmatrix}1 & 1 & -1 & 1 \\ 0 & 0 & 2 & 1 \\ 0 & 1 & -1 & 2 \\ 0 & 0 & -2 & 2\end{vmatrix}.\end{aligned}
$$

Expanding the result along the $1$st column, we get

$$
\begin{aligned} & \,\,\begin{vmatrix}1 & 1 & -1 & 1 \\ 0 & 0 & 2 & 1 \\ 0 & 1 & -1 & 2 \\ 0 & 0 & -2 & 2\end{vmatrix} \\  & =1\cdot (-1)^{1+1}\begin{vmatrix}0 & 2 & 1 \\ 1 & -1 & 2 \\ 0 & -2 & 2\end{vmatrix} \\  & =\begin{vmatrix}0 & 2 & 1 \\ 1 & -1 & 2 \\ 0 & -2 & 2\end{vmatrix} \\  & =1\cdot (-1)^{2+1}\begin{vmatrix}2 & 1 \\ -2 & 2\end{vmatrix} \\  & =-(4-(-2)) \\  & =-6.\end{aligned}
$$

Answer selection: -6

Question 17592186120433 — question.difficulty/moderate

Calculate the value of 
$$
\displaystyle \,\begin{vmatrix}5 & -8 & 3 & -2 \\ -7 & 5 & -4 & -1 \\ 3 & -1 & 1 & 2 \\ -6 & -4 & -2 & -4\end{vmatrix}.
$$

*Hint: Use elementary column operations to make the entries to the left and to the right of ${a}_{33}$ equal to zero. You should be able to reduce the given $4\times 4$ determinant to a $3\times 3$ determinant.*

Solution: Using elementary column operations, let's make entries to the left and to the right of ${a}_{33}=1$ equal to zero.

Since adding a multiple of one row (or column) to another row (column) in a matrix does not change the value of its determinant, we obtain

$$
\begin{aligned} & \,\,\begin{vmatrix}5 & -8 & 3 & -2 \\ -7 & 5 & -4 & -1 \\ 3 & -1 & 1 & 2 \\ -6 & -4 & -2 & -4\end{vmatrix} &  & \,\begin{aligned}{C}_{1}:={C}_{1}+(-3){C}_{3} \\ {C}_{2}:={C}_{2}+{C}_{3} \\ {C}_{4}:={C}_{4}+(-2){C}_{3}\end{aligned} \\  & =\begin{vmatrix}-4 & -5 & 3 & -8 \\ 5 & 1 & -4 & 7 \\ 0 & 0 & 1 & 0 \\ 0 & -6 & -2 & 0\end{vmatrix}.\end{aligned}
$$

Expanding the result along the $3$rd row, we get

$$
\begin{aligned} & \,\,\begin{vmatrix}-4 & -5 & 3 & -8 \\ 5 & 1 & -4 & 7 \\ 0 & 0 & 1 & 0 \\ 0 & -6 & -2 & 0\end{vmatrix} \\  & =1\cdot (-1)^{3+3}\begin{vmatrix}-4 & -5 & -8 \\ 5 & 1 & 7 \\ 0 & -6 & 0\end{vmatrix} \\  & =\begin{vmatrix}-4 & -5 & -8 \\ 5 & 1 & 7 \\ 0 & -6 & 0\end{vmatrix} \\  & =(-6)\cdot (-1)^{3+2}\begin{vmatrix}-4 & -8 \\ 5 & 7\end{vmatrix} \\  & =6(-28+40) \\  & =72.\end{aligned}
$$

Answer selection: 72

Question 17592186266142 — question.difficulty/moderate

Calculate the value of 
$$
\displaystyle \,\begin{vmatrix}-3 & 1 & 4 & 3 \\ 2 & -2 & -8 & -1 \\ -3 & 3 & 7 & 5 \\ -4 & -1 & -4 & -1\end{vmatrix}.
$$

*Hint: Use elementary row operations to make the entries below ${a}_{12}$ equal to zero. You should be able to reduce the given $4\times 4$ determinant to a $3\times 3$ determinant.*

Solution: Using elementary row operations, let's make entries below ${a}_{12}=1$ equal to zero.

Since adding a multiple of one row (or column) to another row (column) in a matrix does not change the value of its determinant, we obtain

$$
\begin{aligned} & \,\,\begin{vmatrix}-3 & 1 & 4 & 3 \\ 2 & -2 & -8 & -1 \\ -3 & 3 & 7 & 5 \\ -4 & -1 & -4 & -1\end{vmatrix} &  & \,\begin{aligned}{R}_{2}:={R}_{2}+2{R}_{1} \\ {R}_{3}:={R}_{3}+(-3){R}_{1} \\ {R}_{4}:={R}_{4}+{R}_{1}\end{aligned} \\  & =\begin{vmatrix}-3 & 1 & 4 & 3 \\ -4 & 0 & 0 & 5 \\ 6 & 0 & -5 & -4 \\ -7 & 0 & 0 & 2\end{vmatrix}.\end{aligned}
$$

Expanding the result along the $2$nd column, we get

$$
\begin{aligned} & \,\,\begin{vmatrix}-3 & 1 & 4 & 3 \\ -4 & 0 & 0 & 5 \\ 6 & 0 & -5 & -4 \\ -7 & 0 & 0 & 2\end{vmatrix} \\  & =1\cdot (-1)^{1+2}\begin{vmatrix}-4 & 0 & 5 \\ 6 & -5 & -4 \\ -7 & 0 & 2\end{vmatrix} \\  & =-\begin{vmatrix}-4 & 0 & 5 \\ 6 & -5 & -4 \\ -7 & 0 & 2\end{vmatrix} \\  & =(-1)\cdot -5\cdot (-1)^{2+2}\begin{vmatrix}-4 & 5 \\ -7 & 2\end{vmatrix} \\  & =5(-8+35) \\  & =135.\end{aligned}
$$

Answer selection: 135
