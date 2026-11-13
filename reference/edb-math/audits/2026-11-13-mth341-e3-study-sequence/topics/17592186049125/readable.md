# 17592186049125 Introduction to the Inverse of a Matrix

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186088893 — Introduction

Given the scalar $a,$ the **multiplicative inverse** of $a$ is defined as the scalar $a^{-1}$ such that

$$
a \cdot a^{-1} = a^{-1} \cdot a = 1.
$$

For example, the multiplicative inverse of $2$ is the number $2^{-1} = \dfrac{1}{2}$ because 

$$
\dfrac{1}{2}\cdot 2 =  2\cdot \dfrac{1}{2} = 1.
$$

Similarly, given a square $n \times n$ matrix $A,$ the **inverse** of $A$ is defined as the $n \times n$ matrix $A^{-1}$ such that

$$
A \cdot A^{-1} = A^{-1} \cdot A = I_n,
$$

where $I_n$ is the $n\times n$ identity matrix.

For example, suppose we're given the following $2\times 2$ matrix:

<div class="matrix-operands matrix-operands-stacked">
<div>$A=\begin{bmatrix}-1 & -1 \\ 1 & 2\end{bmatrix}$</div>
</div>

The inverse of the above matrix is given by

$$
A^{-1} =
	\begin{bmatrix}-2 & -1 \\ 1 & 1\end{bmatrix}.
$$

To verify that the above matrix is in fact the inverse of $A,$ first observe that if we multiply $A$ by the above matrix $A^{-1},$ then we get the identity matrix $I_2\mathbin{:}$

$$
\begin{aligned}\underbrace{\begin{bmatrix}-1 & -1 \\ 1 & 2\end{bmatrix}}_{A}\underbrace{\begin{bmatrix}-2 & -1 \\ 1 & 1\end{bmatrix}}_{{A}^{-1}} & =\begin{bmatrix}-1\cdot (-2)+(-1)\cdot 1 & -1\cdot (-1)+(-1)\cdot 1 \\ 1\cdot (-2)+2\cdot 1 & 1\cdot (-1)+2\cdot 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}\,✓\end{aligned}
$$

Likewise, if we multiply $A^{-1}$ by $A,$ then we also get the identity matrix $I_2\mathbin{:}$

$$
\begin{aligned}\begin{bmatrix}-2 & -1 \\ 1 & 1\end{bmatrix}\underbrace{\begin{bmatrix}-1 & -1 \\ 1 & 2\end{bmatrix}}_{A} & ={I}_{2}\,✓\end{aligned}
$$

We do not yet know how to find the inverse of a matrix. However, we can verify that one matrix is the inverse of the other by carrying out the same procedure as we did here.



### example 17592186087506 — Determining the Inverse of a 2x2 Matrix

Using the method of direct verification, determine whether the matrix $B$ is the inverse of $A,$ where

<div class="matrix-operands matrix-operands-stacked">
<div>$A=\begin{bmatrix}1 & 0 \\ -1 & 1\end{bmatrix}$</div>
<div>$B=\begin{bmatrix}1 & 0 \\ 1 & 1\end{bmatrix}$</div>
</div>

We must check whether $AB = BA = I_2.$

Computing $AB,$ we get

$$
\begin{aligned}AB & =\begin{bmatrix}1 & 0 \\ -1 & 1\end{bmatrix}\begin{bmatrix}1 & 0 \\ 1 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $BA,$ we get

$$
\begin{aligned}BA & =\begin{bmatrix}1 & 0 \\ 1 & 1\end{bmatrix}\begin{bmatrix}1 & 0 \\ -1 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Therefore, $B = A^{-1}.$

### example 17592186087507 — Determining the Inverse of a Larger Matrix

Using the method of direct verification, determine whether the matrix $B$ is the inverse of $A,$ where

<div class="matrix-operands matrix-operands-stacked">
<div>$A =\begin{bmatrix}1 & 1 & 1 \\ 0 & 1 & 1 \\ 0 & 0 & 1\end{bmatrix}$</div>
<div>$B=\begin{bmatrix}1 & -1 & 0 \\ 0 & 1 & -1 \\ 0 & 0 & 1\end{bmatrix}$</div>
</div>

First, we  check whether $AB = BA = I_3.$

Computing $AB,$ we get

$$
\begin{aligned}AB & =\begin{bmatrix}1 & 1 & 1 \\ 0 & 1 & 1 \\ 0 & 0 & 1\end{bmatrix}\begin{bmatrix}1 & -1 & 0 \\ 0 & 1 & -1 \\ 0 & 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

Likewise, computing $BA,$ we get

$$
\begin{aligned}BA & =\begin{bmatrix}1 & -1 & 0 \\ 0 & 1 & -1 \\ 0 & 0 & 1\end{bmatrix}\begin{bmatrix}1 & 1 & 1 \\ 0 & 1 & 1 \\ 0 & 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

Therefore, $B = A^{-1}.$

### tutorial 17592186088894 — Not Every Matrix Has an Inverse

The number $0$ does not have an inverse for multiplication over the real numbers, because there's no such number $a$ that $a \cdot 0 = 1.$ Instead, for every $a$ we have $a \cdot 0 = 0.$

Similarly, not every matrix has an inverse.

- If a matrix is not square, an inverse does not exist.

- Some square matrices do not have an inverse. If a square matrix does not have an inverse, then it is said to be **singular**. An example of a singular matrix is the zero matrix

$$
\begin{bmatrix}0 & 0 \\ 0 & 0\end{bmatrix}
$$

We will soon learn how to calculate the inverse of a square matrix, and we'll also soon learn how to determine when a square matrix does not have an inverse.



## Representative practice (first three per skill; full bank in practice.json)

### Determining the Inverse of a 2x2 Matrix (30 captured questions)

Question 17592186087986 — question.difficulty/easy

Consider the matrices

$$
B=\begin{bmatrix}1 & 2 \\ 1 & 1\end{bmatrix},\,C=\begin{bmatrix}1 & 2 \\ 0 & 1\end{bmatrix},\,D=\begin{bmatrix}-1 & 2 \\ 1 & -1\end{bmatrix}.
$$

Which of the following statements are true?

Select all that apply.

Solution: - First, we check whether $BC=CB={I}_{2}.$ Computing $BC$, we get

$$
\begin{aligned}BC & =\begin{bmatrix}1 & 2 \\ 1 & 1\end{bmatrix}\begin{bmatrix}1 & 2 \\ 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}∗ & 4 \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement $BC=CB={I}_{2}$ is false.

- Now, we check whether $BD=DB={I}_{2}.$ Computing $BD$, we get

$$
\begin{aligned}BD & =\begin{bmatrix}1 & 2 \\ 1 & 1\end{bmatrix}\begin{bmatrix}-1 & 2 \\ 1 & -1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $DB$, we get

$$
\begin{aligned}DB & =\begin{bmatrix}-1 & 2 \\ 1 & -1\end{bmatrix}\begin{bmatrix}1 & 2 \\ 1 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement $BD=DB={I}_{2}$ is true. As a result, $D={B}^{-1}$ and statement $D={B}^{-1}$ is true too.

Therefore, the correct answer is $BD=DB={I}_{2}$; $D={B}^{-1}$ only.

Answer $BC=CB={I}_{2}$: false

Answer $BD=DB={I}_{2}$: true

Answer $D={B}^{-1}$: true

Answer None of the above: false

Question 17592186088366 — None

Consider the matrices
$$
\displaystyle A = \begin{bmatrix}1 & 0 \\ 1 & 1\end{bmatrix}, B = \begin{bmatrix}-1 & 1 \\ -1 & -1\end{bmatrix}, C = \begin{bmatrix}1 & 0 \\ -1 & 1\end{bmatrix}.
$$

Which of the following statements are true?

1. $AB = BA = I_{2}$
2. $AC = CA = I_{2}$
3. $B = A^{-1}$

Solution: Multiplying $A$ and $C$ in both orders gives

$$
AC=CA=\begin{bmatrix}1&0\\0&1\end{bmatrix}=I_2.
$$

Thus $C=A^{-1}$. Since $B\ne C$, statement III is false. Also

$$
AB=\begin{bmatrix}-1&1\\-2&0\end{bmatrix}\ne I_2,
$$

so statement I is false. Only statement II is true.

Answer selection: II only

Question 17592186237917 — question.difficulty/easy

Consider the matrices

$$
A=\begin{bmatrix}1 & 1 \\ -1 & 2\end{bmatrix},\,B=\begin{bmatrix}\frac{2}{3} & -\frac{1}{3} \\ \frac{1}{3} & \frac{1}{3}\end{bmatrix},\,C=\begin{bmatrix}2 & -1 \\ 1 & 1\end{bmatrix}.
$$

Which of the following statements are true?

Select all that apply.

Solution: - First, we check whether $AB=BA={I}_{2}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}1 & 1 \\ -1 & 2\end{bmatrix}\begin{bmatrix}\frac{2}{3} & -\frac{1}{3} \\ \frac{1}{3} & \frac{1}{3}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $BA$, we get

$$
\begin{aligned}BA & =\begin{bmatrix}\frac{2}{3} & -\frac{1}{3} \\ \frac{1}{3} & \frac{1}{3}\end{bmatrix}\begin{bmatrix}1 & 1 \\ -1 & 2\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement $AB=BA={I}_{2}$ is true.

- Now, we check whether $AC=CA={I}_{2}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}1 & 1 \\ -1 & 2\end{bmatrix}\begin{bmatrix}2 & -1 \\ 1 & 1\end{bmatrix} \\  & =\begin{bmatrix}3 & ∗ \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement $AC=CA={I}_{2}$ is false. As a result, $C\ne {A}^{-1}$ and statement $C={A}^{-1}$ is false too.

Therefore, the correct answer is $AB=BA={I}_{2}$ only.

Answer $AB=BA={I}_{2}$: true

Answer $AC=CA={I}_{2}$: false

Answer $C={A}^{-1}$: false

Answer None of the above: false

### Determining the Inverse of a Larger Matrix (33 captured questions)

Question 17592186087987 — question.difficulty/moderate

Consider the matrices

$$
C=\begin{bmatrix}1 & 2 & 1 \\ 0 & 1 & 1 \\ 1 & 2 & 0\end{bmatrix},\,D=\begin{bmatrix}2 & -2 & -1 \\ -1 & 1 & 1 \\ 1 & 0 & -1\end{bmatrix},\,E=\begin{bmatrix}2 & -2 & -1 \\ 1 & 1 & 1 \\ 1 & 0 & -1\end{bmatrix}.
$$

Which of the following statements are true?

Select all that apply.

Solution: - First, we check whether $CD=DC={I}_{3}.$ Computing $CD$, we get

$$
\begin{aligned}CD & =\begin{bmatrix}1 & 2 & 1 \\ 0 & 1 & 1 \\ 1 & 2 & 0\end{bmatrix}\begin{bmatrix}2 & -2 & -1 \\ -1 & 1 & 1 \\ 1 & 0 & -1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

Likewise, computing $DC$, we get

$$
\begin{aligned}DC & =\begin{bmatrix}2 & -2 & -1 \\ -1 & 1 & 1 \\ 1 & 0 & -1\end{bmatrix}\begin{bmatrix}1 & 2 & 1 \\ 0 & 1 & 1 \\ 1 & 2 & 0\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

So, statement $CD=DC={I}_{3}$ is true.

- Now, we check whether $CE=EC={I}_{3}.$ Computing $CE$, we get

$$
\begin{aligned}CE & =\begin{bmatrix}1 & 2 & 1 \\ 0 & 1 & 1 \\ 1 & 2 & 0\end{bmatrix}\begin{bmatrix}2 & -2 & -1 \\ 1 & 1 & 1 \\ 1 & 0 & -1\end{bmatrix} \\  & =\begin{bmatrix}5 & ∗ & ∗ \\ ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗\end{bmatrix} \\  & \ne {I}_{3}.\,\times \end{aligned}
$$

So, statement $CE=EC={I}_{3}$ is false. As a result, $E\ne {C}^{-1}$ and statement $E={C}^{-1}$ is false too.

Therefore, the correct answer is $CD=DC={I}_{3}$ only.

Answer $CD=DC={I}_{3}$: true

Answer $CE=EC={I}_{3}$: false

Answer $E={C}^{-1}$: false

Answer None of the above: false

Question 17592186088367 — question.difficulty/hard

Consider the matrices

$$
A=\begin{bmatrix}3 & 2 & 0 & 0 \\ 4 & 3 & 0 & 0 \\ 0 & 0 & 6 & 5 \\ 0 & 0 & 7 & 6\end{bmatrix},\,B=\begin{bmatrix}3 & -2 & 0 & 0 \\ -4 & 3 & 0 & 0 \\ 0 & 0 & 6 & -5 \\ 0 & 0 & -7 & 6\end{bmatrix},\,C=\begin{bmatrix}-3 & 2 & 0 & 0 \\ 4 & -3 & 0 & 0 \\ 0 & 0 & -6 & 5 \\ 0 & 0 & 7 & -6\end{bmatrix}.
$$

Which of the following statements are true?

Select all that apply.

Solution: - First, we check whether $AB=BA={I}_{4}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}3 & 2 & 0 & 0 \\ 4 & 3 & 0 & 0 \\ 0 & 0 & 6 & 5 \\ 0 & 0 & 7 & 6\end{bmatrix}\begin{bmatrix}3 & -2 & 0 & 0 \\ -4 & 3 & 0 & 0 \\ 0 & 0 & 6 & -5 \\ 0 & 0 & -7 & 6\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1\end{bmatrix} \\  & ={I}_{4}.\,✓\end{aligned}
$$

Likewise, computing $BA$, we get

$$
\begin{aligned}BA & =\begin{bmatrix}3 & -2 & 0 & 0 \\ -4 & 3 & 0 & 0 \\ 0 & 0 & 6 & -5 \\ 0 & 0 & -7 & 6\end{bmatrix}\begin{bmatrix}3 & 2 & 0 & 0 \\ 4 & 3 & 0 & 0 \\ 0 & 0 & 6 & 5 \\ 0 & 0 & 7 & 6\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1\end{bmatrix} \\  & ={I}_{4}.\,✓\end{aligned}
$$

So, statement $AB=BA={I}_{4}$ is true. As a result, $B={A}^{-1}$ and statement $B={A}^{-1}$ is true too.

- Now, we check whether $AC=CA={I}_{4}.$ Computing $AC$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}3 & 2 & 0 & 0 \\ 4 & 3 & 0 & 0 \\ 0 & 0 & 6 & 5 \\ 0 & 0 & 7 & 6\end{bmatrix}\begin{bmatrix}-3 & 2 & 0 & 0 \\ 4 & -3 & 0 & 0 \\ 0 & 0 & -6 & 5 \\ 0 & 0 & 7 & -6\end{bmatrix} \\  & =\begin{bmatrix}-1 & ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗ & ∗\end{bmatrix} \\  & \ne {I}_{4}.\,\times \end{aligned}
$$

So, statement $AC=CA={I}_{4}$ is false.

Therefore, the correct answer is $AB=BA={I}_{4}$; $B={A}^{-1}$ only.

Answer $AB=BA={I}_{4}$: true

Answer $AC=CA={I}_{4}$: false

Answer $B={A}^{-1}$: true

Answer None of the above: false

Question 17592186253256 — question.difficulty/moderate

Consider the matrices

$$
A=\begin{bmatrix}-1 & 3 & 2 \\ 2 & 1 & -2 \\ 0 & 1 & 1\end{bmatrix},\,B=\begin{bmatrix}-3 & 1 & 8 \\ 2 & 1 & -2 \\ -2 & -1 & 7\end{bmatrix},\,C=\frac{1}{5}\begin{bmatrix}-3 & 1 & 8 \\ 2 & 1 & -2 \\ -2 & -1 & 7\end{bmatrix}
$$

Which of the following statements are true?

Select all that apply.

Solution: - First, we check whether $AB=BA={I}_{3}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}-1 & 3 & 2 \\ 2 & 1 & -2 \\ 0 & 1 & 1\end{bmatrix}\begin{bmatrix}-3 & 1 & 8 \\ 2 & 1 & -2 \\ -2 & -1 & 7\end{bmatrix} \\  & =\begin{bmatrix}5 & ∗ & ∗ \\ ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗\end{bmatrix} \\  & \ne {I}_{3}.\,\times \end{aligned}
$$

So, statement $AB=BA={I}_{3}$ is false. As a result, $B\ne {A}^{-1}$ and statement $B={A}^{-1}$ is false too.

- Now, we check whether $AC=CA={I}_{3}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\frac{1}{5}\begin{bmatrix}-1 & 3 & 2 \\ 2 & 1 & -2 \\ 0 & 1 & 1\end{bmatrix}\begin{bmatrix}-3 & 1 & 8 \\ 2 & 1 & -2 \\ -2 & -1 & 7\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

Likewise, computing $CA$, we get

$$
\begin{aligned}CA & =\frac{1}{5}\begin{bmatrix}-3 & 1 & 8 \\ 2 & 1 & -2 \\ -2 & -1 & 7\end{bmatrix}\begin{bmatrix}-1 & 3 & 2 \\ 2 & 1 & -2 \\ 0 & 1 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

So, statement $AC=CA={I}_{3}$ is true. 
Therefore, the correct answer is $AC=CA={I}_{3}$ only.

Answer $AB=BA={I}_{3}$: false

Answer $AC=CA={I}_{3}$: true

Answer $B={A}^{-1}$: false
