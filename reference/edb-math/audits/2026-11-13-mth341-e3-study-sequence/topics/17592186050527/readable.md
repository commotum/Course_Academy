# 17592186050527 Creating Rows or Columns Containing Zeros Using Gaussian Elimination

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186163214 — Introduction

When studying linear algebra, it is common to use elementary row operations to reduce a matrix $A$ to another matrix $B$ such that $B$ contains many zeros. 

To illustrate, let's consider the matrix $A,$ given by

$$
A =
	\begin{bmatrix}{\color{blue}{1}} & {\color{blue}{1}} & {\color{blue}{-4}} \\ 3 & 2 & -2 \\ -5 & -3 & 6\end{bmatrix}.
$$

Consider the entry $a_{11}$ located in the top left-hand corner. We can reduce *all* of the entries *below* it using elementary row operations.

First, we subtract $3$ times the first row from the second row.

$$
\begin{aligned}A= & \begin{bmatrix}1 & 1 & -4 \\ 3 & 2 & -2 \\ -5 & -3 & 6\end{bmatrix} &  & \,\begin{aligned}{R}_{2}: &={R}_{2}-3{R}_{1}\end{aligned} \\ ∼ & \begin{bmatrix}1 & 1 & -4 \\ 0 & -1 & 10 \\ -5 & -3 & 6\end{bmatrix}\end{aligned}
$$

Then, we add $5$ times the first row to the third row.

$$
\begin{aligned} & \begin{bmatrix}1 & 1 & -4 \\ 0 & -1 & 10 \\ -5 & -3 & 6\end{bmatrix} &  & \,\begin{aligned}{R}_{3}: &={R}_{3}+5{R}_{1}\end{aligned} \\ ∼ & \begin{bmatrix}1 & 1 & -4 \\ 0 & -1 & 10 \\ 0 & 2 & -14\end{bmatrix}\end{aligned}
$$

And we're done! We have successfully performed elementary row operations to reduce all of the entries below $a_{11}$ to zero.



### example 17592186161759 — Using Row Operations to Create a Column of Zeros in a 3x3 Matrix



$$
A=\begin{bmatrix}\bbox[lightgray,2pt]{{\color{blue}1}} & {\color{blue}4} & {\color{blue}-7} \\ 2 & 2 & -8 \\ -3 & -2 & 1\end{bmatrix}
$$

$$
B=\begin{bmatrix}\bbox[lightgray,2pt]{{\color{blue}1}} & {\color{blue}4} & {\color{blue}-7} \\ {\color{red}0} & -6 & 6 \\ {\color{red}0} & 10 & -20\end{bmatrix}
$$

By applying elementary row operations of the form $R_i:=R_i+kR_1,$ the matrix $A$ can be transformed into the matrix $B.$ What are the elementary row operations?

To transform $A$ into $B,$ we need to make the entries below $a_{11}={\color{blue}\bbox[lightgray,2pt]{1}}$ equal to ${\color{red}0}.$

To do this, we can apply the following elementary row operations:

$$
\begin{aligned}A & =\begin{bmatrix}1 & 4 & -7 \\ 2 & 2 & -8 \\ -3 & -2 & 1\end{bmatrix} &  & \,\begin{aligned}{R}_{2}: &={R}_{2}-2{R}_{1}\end{aligned} \\  & ∼\begin{bmatrix}1 & 4 & -7 \\ 0 & -6 & 6 \\ -3 & -2 & 1\end{bmatrix} &  & \,\begin{aligned}{R}_{3}: &={R}_{3}+3{R}_{1}\end{aligned} \\  & ∼\begin{bmatrix}1 & 4 & -7 \\ 0 & -6 & 6 \\ 0 & 10 & -20\end{bmatrix} \\  & =B\end{aligned}
$$

Therefore, the elementary row operations are

$\qquad$ $R_2:=R_2-2R_1\quad$ and $\quad R_3:=R_3+3R_1.$

### example 17592186161757 — Using Row Operations to Create a Column of Zeros in a 4x4 Matrix



$$
A=\begin{bmatrix}-1 & 2 & 1 & 5 \\ {\color{blue}1} & \bbox[lightgray,2pt]{{\color{blue}1}} & {\color{blue}2} & {\color{blue}-1} \\ -1 & 3 & 1 & 1 \\ 0 & -2 & 1 & 5\end{bmatrix}
$$

$$
B=\begin{bmatrix}-3 & {\color{red}0} & -3 & 7 \\ {\color{blue}1} & \bbox[lightgray,2pt]{{\color{blue}1}} & {\color{blue}2} & {\color{blue}-1} \\ -4 & {\color{red}0} & -5 & 4 \\ 2 & {\color{red}0} & 5 & 3\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary row operations 

- $R_1 := \ldots$

- $R_3:=R_3-3R_2$

- $R_4:= \ldots$

each of the form $R_i:=R_i+kR_2,$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary row operations?

To transform $A$ into $B,$ we need to make entries above and below $a_{22}={\color{blue}\bbox[lightgray,2pt]{1}}$ equal to ${\color{red}0}.$

To do this, we can apply the following elementary row operations:

$$
\begin{aligned}A & =\begin{bmatrix}-1 & 2 & 1 & 5 \\ 1 & 1 & 2 & -1 \\ -1 & 3 & 1 & 1 \\ 0 & -2 & 1 & 5\end{bmatrix} &  & \,\begin{aligned}{R}_{1}: &={R}_{1}-2{R}_{2}\end{aligned} \\  & ∼\begin{bmatrix}-3 & 0 & -3 & 7 \\ 1 & 1 & 2 & -1 \\ -1 & 3 & 1 & 1 \\ 0 & -2 & 1 & 5\end{bmatrix} &  & \,\begin{aligned}{R}_{3}: &={R}_{3}-3{R}_{2}\end{aligned} \\  & ∼\begin{bmatrix}-3 & 0 & -3 & 7 \\ 1 & 1 & 2 & -1 \\ -4 & 0 & -5 & 4 \\ 0 & -2 & 1 & 5\end{bmatrix} &  & \,\begin{aligned}{R}_{4}: &={R}_{4}+2{R}_{2}\end{aligned} \\  & ∼\begin{bmatrix}-3 & 0 & -3 & 7 \\ 1 & 1 & 2 & -1 \\ -4 & 0 & -5 & 4 \\ 2 & 0 & 5 & 3\end{bmatrix} \\  & =B\end{aligned}
$$

Therefore, the missing elementary row operations are

$\qquad$ $R_1 := R_1 - 2R_2\quad$ and $\quad R_4:=R_4+2R_2.$

### tutorial 17592186163179 — Column Operations

We can do the same trick using the **elementary column operations** instead of row operations.

There are three types of elementary *column* operations, which are entirely analogous to the corresponding row operations:

- Switching any two columns: 

$$
C_i \leftrightarrow C_j
$$

- Multiplying (each element of) a column by a non-zero number: 

$$
C_i := k C_i,\qquad k \neq 0
$$

- Adding a multiple of one column to another column: 

$$
C_j := C_j+k C_i,\qquad j \neq i
$$

**Watch out!** 

- Unlike elementary row operations, elementary *column* operations change the solutions of a system of linear equations. This is because column operations alter the coefficients associated with each variable across the system, changing the equations.

- The exception is swapping two columns - this doesn't alter the solutions *provided that* we swap the corresponding variables in the solution vector. For example, if we swap the first and second columns, we must treat the second variable as the first and vice versa. The solution set remains unchanged because the relationships between the variables and their coefficients are preserved.



### example 17592186161760 — Using Column Operations to Create a Row of Zeros in a 3x3 Matrix



$$
A=\begin{bmatrix}-6 & -5 & \bbox[lightgray,2pt]{{\color{blue}1}} \\ 8 & 3 & {\color{blue}-4} \\ 9 & 7 & {\color{blue}-2}\end{bmatrix}
$$

$$
B=\begin{bmatrix}{\color{red}0} & {\color{red}0} & \bbox[lightgray,2pt]{{\color{blue}1}} \\ -16 & -17 & {\color{blue}-4} \\ -3 & -3 & {\color{blue}-2}\end{bmatrix}
$$

By applying elementary column operations of the form $C_i:=C_i+kC_3,$ the matrix $A$ can be transformed into the matrix $B.$ What are the elementary column operations?

To transform $A$ into $B,$ we need to make entries to the left of $a_{13}={\color{blue}\bbox[lightgray,2pt]{1}}$ equal to ${\color{red}0}.$

To do this, we can apply the following elementary column operations:

$$
\begin{aligned}A & =\begin{bmatrix}-6 & -5 & 1 \\ 8 & 3 & -4 \\ 9 & 7 & -2\end{bmatrix} &  & \,\begin{aligned}{C}_{1}: &={C}_{1}+6{C}_{3}\end{aligned} \\  & ∼\begin{bmatrix}0 & -5 & 1 \\ -16 & 3 & -4 \\ -3 & 7 & -2\end{bmatrix} &  & \,\begin{aligned}{C}_{2}: &={C}_{2}+5{C}_{3}\end{aligned} \\  & ∼\begin{bmatrix}0 & 0 & 1 \\ -16 & -17 & -4 \\ -3 & -3 & -2\end{bmatrix} \\  & =B\end{aligned}
$$

Therefore, the elementary column operations are

$\qquad$ $C_1:=C_1+6C_3\quad$ and $\quad C_2:=C_2+5C_3.$

### example 17592186161758 — Using Column Operations to Create a Row of Zeros in a 4x4 Matrix



$$
A=\begin{bmatrix}7 & {\color{blue}-3} & -1 & -6 \\ 7 & {\color{blue}-2} & -2 & -4 \\ -5 & \bbox[lightgray,2pt]{{\color{blue}1}} & 4 & 2 \\ -8 & {\color{blue}-3} & -6 & -4\end{bmatrix}
$$

$$
B=\begin{bmatrix}-8 & {\color{blue}-3} & 11 & 0 \\ -3 & {\color{blue}-2} & 6 & 0 \\ {\color{red}0} & \bbox[lightgray,2pt]{{\color{blue}1}} & {\color{red}0} & {\color{red}0} \\ -23 & {\color{blue}-3} & 6 & 2\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations 

- $C_1:=\ldots$

- $C_3:= C_3 - 4C_2$

- $C_4:= \ldots$

each of the form $C_i:=C_i+kC_2,$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

To transform $A$ into $B,$ we need to make entries to the left and to the right of $a_{32}={\color{blue}\bbox[lightgray,2pt]{1}}$ equal to ${\color{red}0}.$

To do this, we can apply the following elementary column operations:

$$
\begin{aligned}A & =\begin{bmatrix}7 & -3 & -1 & -6 \\ 7 & -2 & -2 & -4 \\ -5 & 1 & 4 & 2 \\ -8 & -3 & -6 & -4\end{bmatrix} &  & \,\begin{aligned}{C}_{1}: &={C}_{1}+5{C}_{2}\end{aligned} \\  & ∼\begin{bmatrix}-8 & -3 & -1 & -6 \\ -3 & -2 & -2 & -4 \\ 0 & 1 & 4 & 2 \\ -23 & -3 & -6 & -4\end{bmatrix} &  & \,\begin{aligned}{C}_{3}: &={C}_{3}-4{C}_{2}\end{aligned} \\  & ∼\begin{bmatrix}-8 & -3 & 11 & -6 \\ -3 & -2 & 6 & -4 \\ 0 & 1 & 0 & 2 \\ -23 & -3 & 6 & -4\end{bmatrix} &  & \,\begin{aligned}{C}_{4}: &={C}_{4}-2{C}_{2}\end{aligned} \\  & ∼\begin{bmatrix}-8 & -3 & 11 & 0 \\ -3 & -2 & 6 & 0 \\ 0 & 1 & 0 & 0 \\ -23 & -3 & 6 & 2\end{bmatrix} \\  & =B\end{aligned}
$$

Therefore, the corresponding elementary column operations are

$\qquad$ $C_1:=C_1+5C_2\quad$ and $\quad C_4:=C_4-2C_2.$

## Representative practice (first three per skill; full bank in practice.json)

### Using Row Operations to Create a Column of Zeros in a 3x3 Matrix (15 captured questions)

Question 17592186162553 — question.difficulty/easy

$$
A=\begin{bmatrix}-3 & 2 & -1 \\ 1 & 2 & 1 \\ 0 & 1 & 2\end{bmatrix}
$$

$$
B=\begin{bmatrix}-3 & 0 & -5 \\ 1 & 0 & -3 \\ 0 & 1 & 2\end{bmatrix}
$$

By applying elementary row operations of the form ${R}_{i}:={R}_{i}+k{R}_{3},$ the matrix $A$ can be transformed into the matrix $B.$ What are the elementary row operations?

Solution: To transform $A$ into $B,$ we need to make the entries above ${a}_{32}=1$ equal to $0.$

To do this, we can apply the following elementary row operations:

$$
\begin{aligned}A & =\begin{bmatrix}-3 & 2 & -1 \\ 1 & 2 & 1 \\ 0 & 1 & 2\end{bmatrix} &  & \,\begin{aligned}{R}_{1}: &={R}_{1}-2{R}_{3}\end{aligned} \\  & ∼\begin{bmatrix}-3 & 0 & -5 \\ 1 & 2 & 1 \\ 0 & 1 & 2\end{bmatrix} &  & \,\begin{aligned}{R}_{2}: &={R}_{2}-2{R}_{3}\end{aligned} \\  & ∼\begin{bmatrix}-3 & 0 & -5 \\ 1 & 0 & -3 \\ 0 & 1 & 2\end{bmatrix} \\  & =B\end{aligned}
$$

Therefore, the elementary row operations are

$\,$ ${R}_{1}:={R}_{1}-2{R}_{3}\,$ and $\,{R}_{2}:={R}_{2}-2{R}_{3}.$

Answer selection: ${R}_{1}:={R}_{1}-2{R}_{3}\,$ and $\,{R}_{2}:={R}_{2}-2{R}_{3}$

Question 17592186162570 — question.difficulty/easy

$$
A=\begin{bmatrix}-1 & 1 & 6 \\ 2 & -5 & -3 \\ -3 & -6 & -9\end{bmatrix}
$$

$$
B=\begin{bmatrix}3 & -9 & 0 \\ 2 & -5 & -3 \\ -9 & 9 & 0\end{bmatrix}
$$

By applying elementary row operations of the form ${R}_{i}:={R}_{i}+k{R}_{2},$ the matrix $A$ can be transformed into the matrix $B.$ What are the elementary row operations?

Solution: To transform $A$ into $B,$ we need to make the entries above and below ${a}_{23}=-3$ equal to $0.$

To do this, we can apply the following elementary row operations:

$$
\begin{aligned}A & =\begin{bmatrix}-1 & 1 & 6 \\ 2 & -5 & -3 \\ -3 & -6 & -9\end{bmatrix} &  & \,\begin{aligned}{R}_{1}: &={R}_{1}+2{R}_{2}\end{aligned} \\  & ∼\begin{bmatrix}3 & -9 & 0 \\ 2 & -5 & -3 \\ -3 & -6 & -9\end{bmatrix} &  & \,\begin{aligned}{R}_{3}: &={R}_{3}-3{R}_{2}\end{aligned} \\  & ∼\begin{bmatrix}3 & -9 & 0 \\ 2 & -5 & -3 \\ -9 & 9 & 0\end{bmatrix} \\  & =B\end{aligned}
$$

Therefore, the elementary row operations are

$\,$ ${R}_{1}:={R}_{1}+2{R}_{2}\,$ and $\,{R}_{3}:={R}_{3}-3{R}_{2}.$

Answer selection: ${R}_{1}:={R}_{1}+2{R}_{2}\,$ and $\,{R}_{3}:={R}_{3}-3{R}_{2}$

Question 17592186265905 — question.difficulty/easy

$$
A=\begin{bmatrix}7 & 4 & 2 \\ -9 & -6 & -12 \\ 6 & 2 & 5\end{bmatrix}
$$

$$
B=\begin{bmatrix}-5 & 0 & -8 \\ 9 & 0 & 3 \\ 6 & 2 & 5\end{bmatrix}
$$

By applying elementary row operations of the form ${R}_{i}:={R}_{i}+k{R}_{3},$ the matrix $A$ can be transformed into the matrix $B.$ What are the elementary row operations?

Solution: To transform $A$ into $B,$ we need to make the entries above ${a}_{32}=2$ equal to $0.$

To do this, we can apply the following elementary row operations:

$$
\begin{aligned}A & =\begin{bmatrix}7 & 4 & 2 \\ -9 & -6 & -12 \\ 6 & 2 & 5\end{bmatrix} &  & \,\begin{aligned}{R}_{1}: &={R}_{1}-2{R}_{3}\end{aligned} \\  & ∼\begin{bmatrix}-5 & 0 & -8 \\ -9 & -6 & -12 \\ 6 & 2 & 5\end{bmatrix} &  & \,\begin{aligned}{R}_{2}: &={R}_{2}+3{R}_{3}\end{aligned} \\  & ∼\begin{bmatrix}-5 & 0 & -8 \\ 9 & 0 & 3 \\ 6 & 2 & 5\end{bmatrix} \\  & =B\end{aligned}
$$

Therefore, the elementary row operations are

$\,$ ${R}_{1}:={R}_{1}-2{R}_{3}\,$ and $\,{R}_{2}:={R}_{2}+3{R}_{3}.$

Answer selection: ${R}_{1}:={R}_{1}-2{R}_{3}\,$ and $\,{R}_{2}:={R}_{2}+3{R}_{3}$

### Using Row Operations to Create a Column of Zeros in a 4x4 Matrix (11 captured questions)

Question 17592186162554 — question.difficulty/moderate

$$
A=\begin{bmatrix}-2 & 3 & -4 & 5 \\ 5 & -1 & 3 & 0 \\ 0 & 4 & 7 & 2 \\ 0 & 5 & 4 & -3\end{bmatrix}
$$

$$
B=\begin{bmatrix}13 & 0 & 5 & 5 \\ 5 & -1 & 3 & 0 \\ 20 & 0 & 19 & 2 \\ 25 & 0 & 19 & -3\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary row operations 

- ${R}_{1}:=…$
- ${R}_{3}:={R}_{3}+4{R}_{2}$
- ${R}_{4}:=…$

each of the form ${R}_{i}:={R}_{i}+k{R}_{2},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary row operations?

Solution: To transform $A$ into $B,$ we need to make entries above and below ${a}_{22}=-1$ equal to $0.$

To do this, we can apply the following elementary row operations:

$$
\begin{aligned}A & =\begin{bmatrix}-2 & 3 & -4 & 5 \\ 5 & -1 & 3 & 0 \\ 0 & 4 & 7 & 2 \\ 0 & 5 & 4 & -3\end{bmatrix} &  & \,\begin{aligned}{R}_{1}: &={R}_{1}+3{R}_{2}\end{aligned} \\  & ∼\begin{bmatrix}13 & 0 & 5 & 5 \\ 5 & -1 & 3 & 0 \\ 0 & 4 & 7 & 2 \\ 0 & 5 & 4 & -3\end{bmatrix} &  & \,\begin{aligned}{R}_{3}: &={R}_{3}+4{R}_{2}\end{aligned} \\  & ∼\begin{bmatrix}13 & 0 & 5 & 5 \\ 5 & -1 & 3 & 0 \\ 20 & 0 & 19 & 2 \\ 0 & 5 & 4 & -3\end{bmatrix} &  & \,\begin{aligned}{R}_{4}: &={R}_{4}+5{R}_{2}\end{aligned} \\  & ∼\begin{bmatrix}13 & 0 & 5 & 5 \\ 5 & -1 & 3 & 0 \\ 20 & 0 & 19 & 2 \\ 25 & 0 & 19 & -3\end{bmatrix} \\  & =B\end{aligned}
$$

Therefore, the missing elementary row operations are

$\,$ ${R}_{1}:={R}_{1}+3{R}_{2}\,$ and $\,{R}_{4}:={R}_{4}+5{R}_{2}.$

Answer selection: ${R}_{1}:={R}_{1}+3{R}_{2}\,$ and $\,{R}_{4}:={R}_{4}+5{R}_{2}$

Question 17592186162571 — question.difficulty/moderate

$$
A=\begin{bmatrix}1 & -3 & -7 & -5 \\ 1 & 10 & 7 & 2 \\ -1 & 0 & 8 & 7 \\ -2 & 1 & 0 & 9\end{bmatrix}
$$

$$
B=\begin{bmatrix}1 & -3 & -7 & -5 \\ 0 & 13 & 14 & 7 \\ 0 & -3 & 1 & 2 \\ 0 & -5 & -14 & -1\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary row operations 

- ${R}_{2}:=…$
- ${R}_{3}:={R}_{3}+{R}_{1}$
- ${R}_{4}:=…$

each of the form ${R}_{i}:={R}_{i}+k{R}_{1},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary row operations?

Solution: To transform $A$ into $B,$ we need to make entries below ${a}_{11}=1$ equal to $0.$

To do this, we can apply the following elementary row operations:

$$
\begin{aligned}A & =\begin{bmatrix}1 & -3 & -7 & -5 \\ 1 & 10 & 7 & 2 \\ -1 & 0 & 8 & 7 \\ -2 & 1 & 0 & 9\end{bmatrix} &  & \,\begin{aligned}{R}_{2}: &={R}_{2}-{R}_{1}\end{aligned} \\  & ∼\begin{bmatrix}1 & -3 & -7 & -5 \\ 0 & 13 & 14 & 7 \\ -1 & 0 & 8 & 7 \\ -2 & 1 & 0 & 9\end{bmatrix} &  & \,\begin{aligned}{R}_{3}: &={R}_{3}+{R}_{1}\end{aligned} \\  & ∼\begin{bmatrix}1 & -3 & -7 & -5 \\ 0 & 13 & 14 & 7 \\ 0 & -3 & 1 & 2 \\ -2 & 1 & 0 & 9\end{bmatrix} &  & \,\begin{aligned}{R}_{4}: &={R}_{4}+2{R}_{1}\end{aligned} \\  & ∼\begin{bmatrix}1 & -3 & -7 & -5 \\ 0 & 13 & 14 & 7 \\ 0 & -3 & 1 & 2 \\ 0 & -5 & -14 & -1\end{bmatrix} \\  & =B\end{aligned}
$$

  

Therefore, the missing elementary row operations are

$\,$ ${R}_{2}:={R}_{2}-{R}_{1}\,$ and $\,{R}_{4}:={R}_{4}+2{R}_{1}.$

Answer selection: ${R}_{2}:={R}_{2}-{R}_{1}\,$ and $\,{R}_{4}:={R}_{4}+2{R}_{1}$

Question 17592186265911 — question.difficulty/moderate

$$
A=\begin{bmatrix}2 & 6 & 11 & 0 \\ 2 & -4 & -5 & 0 \\ 0 & 2 & 6 & 9 \\ 0 & 2 & 9 & 8\end{bmatrix}
$$

$$
B=\begin{bmatrix}2 & 0 & -7 & -27 \\ 2 & 0 & 7 & 18 \\ 0 & 2 & 6 & 9 \\ 0 & 0 & 3 & -1\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary row operations 

- ${R}_{1}:=…$
- ${R}_{2}:=…$
- ${R}_{4}:={R}_{4}-{R}_{3}$

each of the form ${R}_{i}:={R}_{i}+k{R}_{3},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary row operations?

Solution: To transform $A$ into $B,$ we need to make entries above and below ${a}_{32}=2$ equal to $0.$

To do this, we can apply the following elementary row operations:

$$
\begin{aligned}A & =\begin{bmatrix}2 & 6 & 11 & 0 \\ 2 & -4 & -5 & 0 \\ 0 & 2 & 6 & 9 \\ 0 & 2 & 9 & 8\end{bmatrix} &  & \,\begin{aligned}{R}_{1}: &={R}_{1}-3{R}_{3}\end{aligned} \\  & ∼\begin{bmatrix}2 & 0 & -7 & -27 \\ 2 & -4 & -5 & 0 \\ 0 & 2 & 6 & 9 \\ 0 & 2 & 9 & 8\end{bmatrix} &  & \,\begin{aligned}{R}_{2}: &={R}_{2}+2{R}_{3}\end{aligned} \\  & ∼\begin{bmatrix}2 & 0 & -7 & -27 \\ 2 & 0 & 7 & 18 \\ 0 & 2 & 6 & 9 \\ 0 & 2 & 9 & 8\end{bmatrix} &  & \,\begin{aligned}{R}_{4}: &={R}_{4}-{R}_{3}\end{aligned} \\  & ∼\begin{bmatrix}2 & 0 & -7 & -27 \\ 2 & 0 & 7 & 18 \\ 0 & 2 & 6 & 9 \\ 0 & 0 & 3 & -1\end{bmatrix} \\  & =B.\end{aligned}
$$

  

Therefore, the missing elementary row operations are

$\,$ ${R}_{1}:={R}_{1}-3{R}_{3}\,$ and $\,{R}_{2}:={R}_{2}+2{R}_{3}.$

Answer selection: ${R}_{1}:={R}_{1}-3{R}_{3}\,$ and $\,{R}_{2}:={R}_{2}+2{R}_{3}$

### Using Column Operations to Create a Row of Zeros in a 3x3 Matrix (15 captured questions)

Question 17592186162556 — question.difficulty/easy

$$
A=\begin{bmatrix}-1 & 2 & 2 \\ 1 & 3 & 1 \\ 3 & 4 & 1\end{bmatrix}
$$

$$
B=\begin{bmatrix}-7 & -6 & 2 \\ -2 & -1 & 1 \\ 0 & 0 & 1\end{bmatrix}
$$

By applying elementary column operations of the form ${C}_{i}:={C}_{i}+k{C}_{3},$ the matrix $A$ can be transformed into the matrix $B.$ What are the elementary column operations?

Solution: To transform $A$ into $B,$ we need to make entries to the left of ${a}_{33}=1$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{aligned}A & =\begin{bmatrix}-1 & 2 & 2 \\ 1 & 3 & 1 \\ 3 & 4 & 1\end{bmatrix} &  & \,\begin{aligned}{C}_{1}: &={C}_{1}-3{C}_{3}\end{aligned} \\  & ∼\begin{bmatrix}-7 & 2 & 2 \\ -2 & 3 & 1 \\ 0 & 4 & 1\end{bmatrix} &  & \,\begin{aligned}{C}_{2}: &={C}_{2}-4{C}_{3}\end{aligned} \\  & ∼\begin{bmatrix}-7 & -6 & 2 \\ -2 & -1 & 1 \\ 0 & 0 & 1\end{bmatrix} \\  & =B\end{aligned}
$$

Therefore, the elementary column operations are

$\,$ ${C}_{1}:={C}_{1}-3{C}_{3}\,$ and $\,{C}_{2}:={C}_{2}-4{C}_{3}.$

Answer selection: ${C}_{1}:={C}_{1}-3{C}_{3}\,$ and $\,{C}_{2}:={C}_{2}-4{C}_{3}$

Question 17592186162572 — question.difficulty/easy

$$
A=\begin{bmatrix}10 & 5 & -5 \\ -1 & 3 & -4 \\ 8 & 8 & 0\end{bmatrix}
$$

$$
B=\begin{bmatrix}0 & 5 & 0 \\ -7 & 3 & -1 \\ -8 & 8 & 8\end{bmatrix}
$$

By applying elementary column operations of the form ${C}_{i}:={C}_{i}+k{C}_{2},$ the matrix $A$ can be transformed into the matrix $B.$ What are the elementary column operations?

Solution: To transform $A$ into $B,$ we need to make entries to the left and to the right of ${a}_{12}=5$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{aligned}A & =\begin{bmatrix}10 & 5 & -5 \\ -1 & 3 & -4 \\ 8 & 8 & 0\end{bmatrix} &  & \,\begin{aligned}{C}_{1}: &={C}_{1}-2{C}_{2}\end{aligned} \\  & ∼\begin{bmatrix}0 & 5 & -5 \\ -7 & 3 & -4 \\ -8 & 8 & 0\end{bmatrix} &  & \,\begin{aligned}{C}_{3}: &={C}_{3}+{C}_{2}\end{aligned} \\  & ∼\begin{bmatrix}0 & 5 & 0 \\ -7 & 3 & -1 \\ -8 & 8 & 8\end{bmatrix} \\  & =B\end{aligned}
$$

Therefore, the elementary column operations are

$\,$ ${C}_{1}:={C}_{1}-2{C}_{2}\,$ and $\,{C}_{3}:={C}_{3}+{C}_{2}.$

Answer selection: ${C}_{1}:={C}_{1}-2{C}_{2}\,$ and $\,{C}_{3}:={C}_{3}+{C}_{2}$

Question 17592186265938 — question.difficulty/easy

$$
A=\begin{bmatrix}9 & -2 & -16 \\ -2 & 2 & 8 \\ 0 & 4 & 2\end{bmatrix}
$$

$$
B=\begin{bmatrix}9 & 7 & 20 \\ -2 & 0 & 0 \\ 0 & 4 & 2\end{bmatrix}
$$

By applying elementary column operations of the form ${C}_{i}:={C}_{i}+k{C}_{1},$ the matrix $A$ can be transformed into the matrix $B.$ What are the elementary column operations?

Solution: To transform $A$ into $B,$ we need to make entries to the right of ${a}_{21}=-2$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{aligned}A & =\begin{bmatrix}9 & -2 & -16 \\ -2 & 2 & 8 \\ 0 & 4 & 2\end{bmatrix} &  & \,\begin{aligned}{C}_{2}: &={C}_{2}+{C}_{1}\end{aligned} \\  & ∼\begin{bmatrix}9 & 7 & -16 \\ -2 & 0 & 8 \\ 0 & 4 & 2\end{bmatrix} &  & \,\begin{aligned}{C}_{3}: &={C}_{3}+4{C}_{1}\end{aligned} \\  & ∼\begin{bmatrix}9 & 7 & 20 \\ -2 & 0 & 0 \\ 0 & 4 & 2\end{bmatrix} \\  & =B\end{aligned}
$$

Therefore, the elementary column operations are

$\,$ ${C}_{2}:={C}_{2}+{C}_{1}\,$ and $\,{C}_{3}:={C}_{3}+4{C}_{1}.$

Answer selection: ${C}_{2}:={C}_{2}+{C}_{1}\,$ and $\,{C}_{3}:={C}_{3}+4{C}_{1}$

### Using Column Operations to Create a Row of Zeros in a 4x4 Matrix (18 captured questions)

Question 17592186162555 — question.difficulty/moderate

$$
A=\begin{bmatrix}5 & 0 & 2 & 7 \\ 1 & -7 & -4 & -6 \\ -1 & 3 & 1 & 2 \\ 2 & 7 & 2 & 3\end{bmatrix}
$$

$$
B=\begin{bmatrix}7 & -6 & 2 & 3 \\ -3 & 5 & -4 & 2 \\ 0 & 0 & 1 & 0 \\ 4 & 1 & 2 & -1\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations 

I. ${C}_{1}:={C}_{1}+{C}_{3}$
II. ${C}_{2}:=…$
III. ${C}_{4}:=…$

each of the form ${C}_{i}:={C}_{i}+k{C}_{3},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

Solution: To transform $A$ into $B,$ we need to make entries to the left and to the right of ${a}_{33}=1$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{aligned}A & =\begin{bmatrix}5 & 0 & 2 & 7 \\ 1 & -7 & -4 & -6 \\ -1 & 3 & 1 & 2 \\ 2 & 7 & 2 & 3\end{bmatrix} &  & \,\begin{aligned}{C}_{1}: &={C}_{1}+{C}_{3}\end{aligned} \\  & ∼\begin{bmatrix}7 & 0 & 2 & 7 \\ -3 & -7 & -4 & -6 \\ 0 & 3 & 1 & 2 \\ 4 & 7 & 2 & 3\end{bmatrix} &  & \,\begin{aligned}{C}_{2}: &={C}_{2}-3{C}_{3}\end{aligned} \\  & ∼\begin{bmatrix}7 & -6 & 2 & 7 \\ -3 & 5 & -4 & -6 \\ 0 & 0 & 1 & 2 \\ 4 & 1 & 2 & 3\end{bmatrix} &  & \,\begin{aligned}{C}_{4}: &={C}_{4}-2{C}_{3}\end{aligned} \\  & ∼\begin{bmatrix}7 & -6 & 2 & 3 \\ -3 & 5 & -4 & 2 \\ 0 & 0 & 1 & 0 \\ 4 & 1 & 2 & -1\end{bmatrix} \\  & =B\end{aligned}
$$

Therefore, the corresponding elementary column operations are

$\,$ ${C}_{2}:={C}_{2}-3{C}_{3}\,$ and $\,{C}_{4}:={C}_{4}-2{C}_{3}.$

Answer selection: ${C}_{2}:={C}_{2}-3{C}_{3}\,$ and $\,{C}_{4}:={C}_{4}-2{C}_{3}$

Question 17592186162574 — None

$$
A = \begin{bmatrix}5 & 2 & -3 & -1 \\ 1 & 4 & 3 & 3 \\ 4 & -2 & -6 & -4 \\ 1 & 0 & 4 & -2\end{bmatrix}
$$

$$
B = \begin{bmatrix}0 & 0 & 0 & -1 \\ 16 & 10 & -6 & 3 \\ -16 & -10 & 6 & -4 \\ -9 & -4 & 10 & -2\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations

1. $C_{1}:=…$
2. $C_{2}:=C_{2} + 2C_{4}$
3. $C_{3}:=…$

each of the form $C_{i}:=C_{i} + kC_{4}$, the matrix $A$ can be transformed into the matrix $B$. What are the missing elementary column operations?

Solution: 

Question 17592186265942 — question.difficulty/moderate

$$
A=\begin{bmatrix}5 & 0 & 0 & 7 \\ -8 & 2 & 4 & 8 \\ 5 & -1 & 3 & -2 \\ 2 & 0 & 4 & 1\end{bmatrix}
$$

$$
B=\begin{bmatrix}5 & 0 & 0 & 7 \\ 2 & 2 & 10 & 4 \\ 0 & -1 & 0 & 0 \\ 2 & 0 & 4 & 1\end{bmatrix}
$$

Consider the matrices $A$ and $B$ above. By applying three matrix elementary column operations 

- ${C}_{1}:={C}_{1}+5{C}_{2}$
- ${C}_{3}:=…$
- ${C}_{4}:=…$

each of the form ${C}_{i}:={C}_{i}+k{C}_{2},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?

Solution: To transform $A$ into $B,$ we need to make entries to the left and to the right of ${a}_{32}=-1$ equal to $0.$

To do this, we can apply the following elementary column operations:

$$
\begin{aligned}A & =\begin{bmatrix}5 & 0 & 0 & 7 \\ -8 & 2 & 4 & 8 \\ 5 & -1 & 3 & -2 \\ 2 & 0 & 4 & 1\end{bmatrix} &  & \,\begin{aligned}{C}_{1}: &={C}_{1}+5{C}_{2}\end{aligned} \\  & ∼\begin{bmatrix}5 & 0 & 0 & 7 \\ 2 & 2 & 4 & 8 \\ 0 & -1 & 3 & -2 \\ 2 & 0 & 4 & 1\end{bmatrix} &  & \,\begin{aligned}{C}_{3}: &={C}_{3}+3{C}_{2}\end{aligned} \\  & ∼\begin{bmatrix}5 & 0 & 0 & 7 \\ 2 & 2 & 10 & 8 \\ 0 & -1 & 0 & -2 \\ 2 & 0 & 4 & 1\end{bmatrix} &  & \,\begin{aligned}{C}_{4}: &={C}_{4}-2{C}_{2}\end{aligned} \\  & ∼\begin{bmatrix}5 & 0 & 0 & 7 \\ 2 & 2 & 10 & 4 \\ 0 & -1 & 0 & 0 \\ 2 & 0 & 4 & 1\end{bmatrix} \\  & =B.\end{aligned}
$$

Therefore, the corresponding elementary column operations are

$\,$ ${C}_{3}:={C}_{3}+3{C}_{2}\,$ and $\,{C}_{4}:={C}_{4}-2{C}_{2}.$

Answer selection: ${C}_{3}:={C}_{3}+3{C}_{2}\,$ and $\,{C}_{4}:={C}_{4}-2{C}_{2}$
