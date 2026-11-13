# 17592186050906 The Invertible Matrix Theorem in Terms of 2x2 Systems of Equations

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186116491 — Introduction

Consider a system of two linear equations with two variables 

$$\left\{\begin{aligned}{\color{red}{a}_{11}}x+{\color{red}{a}_{12}}y &={\color{blue}{b}_{1}} \\ {\color{red}{a}_{21}}x+{\color{red}{a}_{22}}y &={\color{blue}{b}_{2}},\end{aligned}\right.$$

and let
$$A = 
\begin{bmatrix}{\color{red}{a}_{11}} & {\color{red}{a}_{12}} \\ {\color{red}{a}_{21}} & {\color{red}{a}_{22}}\end{bmatrix},
\quad
\mathbf{x} = 
\begin{bmatrix}x \\ y\end{bmatrix},
\quad
\mathbf{b} =
\begin{bmatrix}{\color{blue}{b}_{1}} \\ {\color{blue}{b}_{2}}\end{bmatrix}.$$

Recall that we can write the system as $A \mathbf{x} = \mathbf{b}.$ The **invertible matrix theorem** says the following statements are equivalent:

1\. $A$ is invertible (that is, $A^{-1}$ exists).

2\. The system $A\mathbf{x}=\mathbf{b}$ has exactly one solution for any $2 \times 1$ column vector $\mathbf{b}$ (we call such systems consistent independent).

3\. The system $A\mathbf{x}=\mathbf{0}$ has the unique solution $$\mathbf{x}=\begin{bmatrix}x \\ y\end{bmatrix}=\begin{bmatrix}0 \\ 0\end{bmatrix}.$$

4\. The lines ${\color{red}{a_{11}}}x+{\color{red}{a_{12}}}y={\color{blue}{b_1}}$ and ${\color{red}{a_{21}}}x+{\color{red}{a_{22}}}y={\color{blue}{b_2}}$ intersect at one point.

5\. The  determinant of $A$ is nonzero (that is, $\det(A) \neq 0$).



### example 17592186115065 — Identifying a True Statement Concerning a 2x2 System of Equations

Consider a system of two linear equations in two variables, represented by the matrix equation $A\mathbf{x}=\mathbf{b}$ in the usual way. Given that the system has exactly one solution, which of the following statements are true?

I. $\det(A) =0$

II. The system $A\mathbf{x}=\begin{bmatrix}2 \\ 2\end{bmatrix}$ has exactly one solution

III. $A^{-1}$ does not exist

Recall that given $A={\left[ \begin{array}{cc}{a}_{11} & {a}_{12} \\ {a}_{21} & {a}_{22}\end{array} \right]}$, then according to the invertible matrix theorem the following statements are equivalent:    

1\. $A$ is invertible.

2\. The system $A\mathbf{x}=\mathbf{b}$ has exactly one solution for any $2 \times 1$ column vector $\mathbf{b}.$

3\. The system $A\mathbf{x}=\mathbf{0}$ has the unique zero solution.

4\. The lines $a_{11}x+a_{12}y=b_1$ and $a_{21}x+a_{22}y=b_2$ intersect at exactly one point.

5\. $\det(A) \neq 0.$

Also, we are told that the second part of the invertible matrix theorem is true. So, all the other parts of the theorem are true too. Therefore, according to the theorem:

- Statement I is false by the fifth part of the invertible matrix theorem.

- Statement II is true by the second part of the invertible matrix theorem.

- Statement III is false by the first part of the invertible matrix theorem.

Therefore, only statement II is true.

### example 17592186115066 — Identifying a True Statement Given a 2x2 Matrix

Let $A={\left[ \begin{array}{cc}1 & - 2 \\ - 2 & k\end{array} \right]}$ and $\mathbf{b}=\begin{bmatrix}1 \\ -3\end{bmatrix},$ where $k\neq 4$ is a constant. Which of the following statements are true?

- $\det(A) = 0$

- $A\mathbf{x}=\mathbf{b}$ has no solutions

- The lines $x-2y=1$ and $-2x+ky=-3$ intersect at exactly one point

Recall that given $A={\left[ \begin{array}{cc}{a}_{11} & {a}_{12} \\ {a}_{21} & {a}_{22}\end{array} \right]}$, then according to the invertible matrix theorem the following statements are equivalent:    

- $A$ is invertible.

- The system $A\mathbf{x}=\mathbf{b}$ has exactly one solution for any $2 \times 1$ column vector $\mathbf{b}.$

- The system $A\mathbf{x}=\mathbf{0}$ has the unique zero solution.

- The lines $a_{11}x+a_{12}y=b_1$ and $a_{21}x+a_{22}y=b_2$ intersect at exactly one point.

- $\det(A) \neq 0.$

With that in mind, let's now check our statements.

- Statement I is false. We have 

$$
\begin{aligned}\det(A) & =\det\begin{bmatrix}1 & -2 \\ -2 & k\end{bmatrix} \\  & =1\cdot k-(-2)\cdot (-2) \\  & =k-4,\end{aligned}
$$

where $k - 4 \neq 0$ if $k \neq 4.$ 

So, since the fifth part in the invertible matrix theorem is true, all the other parts of the theorem are true too. Therefore, according to the theorem:

- Statement II is false. According to the second part of the invertible matrix theorem, there must be exactly one solution to $A\mathbf{x}=\mathbf{b}.$

- Statement III is true by the fourth part of the invertible matrix theorem.

Therefore, only statement III is true.

### example 17592186115067 — Completing a True Statement

Which of the following completes the statement so that it is true:

*If a $2\times2$-matrix $A$ is invertible, then $\underline{\phantom{xxxxxx}}$ .* 

I. $A\mathbf{x}=\mathbf{0}$ has infinitely many solutions

II. $A\mathbf{x}=\mathbf{0}$ has exactly one solution

III. $\det(A) = 0$

Recall that given $A={\left[ \begin{array}{cc}{a}_{11} & {a}_{12} \\ {a}_{21} & {a}_{22}\end{array} \right]}$, then according to the invertible matrix theorem the following statements are equivalent:    

1\. $A$ is invertible.

2\. The system $A\mathbf{x}=\mathbf{b}$ has exactly one solution for any $2 \times 1$ column vector $\mathbf{b}.$

3\. The system $A\mathbf{x}=\mathbf{0}$ has the unique zero solution.

4\. The lines $a_{11}x+a_{12}y=b_1$ and $a_{21}x+a_{22}y=b_2$ intersect at exactly one point.

5\. $\det(A) \neq 0.$

With that in mind, let's now check our statements.

Notice that since the first part of the invertible matrix theorem is true ($A$ is invertible), all the other parts of the theorem are true too. Therefore, according to the theorem, only option II gives us a true statement:

- *If $A$ is invertible, then $A\mathbf{x}=\mathbf{0}$ has exactly one solution.* $\quad \color{green}\checkmark$

## Representative practice (first three per skill; full bank in practice.json)

### Identifying a True Statement Concerning a 2x2 System of Equations (14 captured questions)

Question 17592186115744 — question.difficulty/moderate

Consider the system of linear equations given by

$$
\left\{\begin{aligned}3x+\sqrt{7}y &=0.3 \\ -2\sqrt{0.1}x+3y &=\sqrt{7}.\end{aligned}\right.
$$

Given that the system has exactly one solution, which of the following statements are true?

Select all that apply.

Solution: Recall that given $A=\begin{bmatrix}{a}_{11} & {a}_{12} \\ {a}_{21} & {a}_{22}\end{bmatrix}$, then according to the invertible matrix theorem the following statements are equivalent:    

1\. $A$ is invertible.

2\. The system $A\mathbf{x}=\mathbf{b}$ has exactly one solution for any $2\times 1$ column vector $\mathbf{b}.$

3\. The system $A\mathbf{x}=\mathbf{0}$ has the unique zero solution.

4\. The lines ${a}_{11}x+{a}_{12}y={b}_{1}$ and ${a}_{21}x+{a}_{22}y={b}_{2}$ intersect at exactly one point.

5\. $\det(A)\ne 0.$

Also, we are told that the second part of the invertible matrix theorem is true. So, all the other parts of the theorem are true too. Therefore, according to the theorem:

- Statement “The lines $3x+\sqrt{7}y=0.3$ and $-2\sqrt{0.1}x+3y=\sqrt{7}$ intersect exactly at one point” is true by the fourth part of the invertible matrix theorem.

- Statement “The determinant of the coefficient matrix is equal to $0$” is false. According to the fifth part of the invertible matrix theorem, the determinant cannot be $0.$

- Statement “The coefficient matrix is invertible” is true by the first part of the invertible matrix theorem.

Therefore, only statements “The lines $3x+\sqrt{7}y=0.3$ and $-2\sqrt{0.1}x+3y=\sqrt{7}$ intersect exactly at one point” and “The coefficient matrix is invertible” are true.

Answer The coefficient matrix is invertible: true

Answer The determinant of the coefficient matrix is equal to $0$: false

Answer The lines $3x+\sqrt{7}y=0.3$ and $-2\sqrt{0.1}x+3y=\sqrt{7}$ intersect exactly at one point: true

Question 17592186115811 — question.difficulty/easy

Consider a system of two linear equations in two variables, represented by the matrix equation $A\mathbf{x}=\mathbf{b}$ in the usual way. Given that the system has exactly one solution, which of the following statements are true?

Select all that apply.

Solution: Recall that given $A=\begin{bmatrix}{a}_{11} & {a}_{12} \\ {a}_{21} & {a}_{22}\end{bmatrix}$, then according to the invertible matrix theorem the following statements are equivalent:    

- $A$ is invertible.

- The system $A\mathbf{x}=\mathbf{b}$ has exactly one solution for any $2\times 1$ column vector $\mathbf{b}.$

- The system $A\mathbf{x}=\mathbf{0}$ has the unique zero solution.

- The lines ${a}_{11}x+{a}_{12}y={b}_{1}$ and ${a}_{21}x+{a}_{22}y={b}_{2}$ intersect at exactly one point.

- $\det(A)\ne 0.$

Also, we are told that the second part of the invertible matrix theorem is true. So, all the other parts of the theorem are true too. Therefore, according to the theorem:

- Statement “$A$ is invertible” is true by the first part of the invertible matrix theorem.

- Statement $\det(A)\ne 0$ is true by the fifth part of the invertible matrix theorem.

- Statement “$A\mathbf{x}=\mathbf{0}$ has an infinite number of solutions” is false by the third part of the invertible matrix theorem.

Therefore, only statements “$A$ is invertible” and $\det(A)\ne 0$ are true.

Answer $A$ is invertible: true

Answer $Ax=0$ has an infinite number of solutions: false

Answer $\det(A)\ne 0$: true

Answer None of the above: false

Question 17592186262850 — question.difficulty/moderate

Consider the system of linear equations given by

$$
\left\{\begin{aligned}x+2y &=-11 \\ y+7x &=4.\end{aligned}\right.
$$

Given that the system has exactly one solution, which of the following statements are true?

Select all that apply.

Solution: Recall that given $A=\begin{bmatrix}{a}_{11} & {a}_{12} \\ {a}_{21} & {a}_{22}\end{bmatrix}$, then according to the invertible matrix theorem the following statements are equivalent:    

- $A$ is invertible.

- The system $A\mathbf{x}=\mathbf{b}$ has exactly one solution for any $2\times 1$ column vector $\mathbf{b}.$

- The system $A\mathbf{x}=\mathbf{0}$ has the unique zero solution.

- The lines ${a}_{11}x+{a}_{12}y={b}_{1}$ and ${a}_{21}x+{a}_{22}y={b}_{2}$ intersect at exactly one point.

- $\det(A)\ne 0.$

Also, we are told that the second part of the invertible matrix theorem is true. So, all the other parts of the theorem are true too. Therefore, according to the theorem:

- Statement “The coefficient matrix is not invertible” is false by the first part of the invertible matrix theorem.

- Statement “The determinant of the coefficient matrix is not zero” is true. According to the fifth part of the invertible matrix theorem, the determinant cannot be $0.$

- Statement “The lines $x+2y=-11$ and $y+7x=4$ intersect at infinitely many  points” is false by the fourth part of the invertible matrix theorem.

Therefore, only statement “The determinant of the coefficient matrix is not zero” is true.

Answer The coefficient matrix is not invertible: false

Answer The determinant of the coefficient matrix is not zero: true

Answer The lines $x+2y=-11$ and $y+7x=4$ intersect at infinitely many  points: false

### Identifying a True Statement Given a 2x2 Matrix (16 captured questions)

Question 17592186115743 — question.difficulty/easy

Let 
$$
\displaystyle A=\begin{bmatrix}1 & 1 \\ 1 & -1\end{bmatrix}.
$$ 
Which of the following statements are true?

Select all that apply.

Solution: Recall that given $A=\begin{bmatrix}{a}_{11} & {a}_{12} \\ {a}_{21} & {a}_{22}\end{bmatrix}$, then according to the invertible matrix theorem the following statements are equivalent:    

- $A$ is invertible.

- The system $A\mathbf{x}=\mathbf{b}$ has exactly one solution for any $2\times 1$ column vector $\mathbf{b}.$

- The system $A\mathbf{x}=\mathbf{0}$ has the unique zero solution.

- The lines ${a}_{11}x+{a}_{12}y={b}_{1}$ and ${a}_{21}x+{a}_{22}y={b}_{2}$ intersect at exactly one point.

- $\det(A)\ne 0.$

With that in mind, let's now check our statements.

- Statement $\det(A)=0$ is false. We have 

$$
\begin{aligned}\det(A) & =\det\begin{bmatrix}1 & 1 \\ 1 & -1\end{bmatrix} \\  & =1\cdot (-1)-1\cdot 1 \\  & =-2\ne 0.\end{aligned}
$$

Now, since the fifth part of the invertible matrix theorem is true, all the other parts of the theorem are true too. Therefore, according to the theorem:

- Statement “$A\mathbf{x}=\mathbf{b}$ has exactly one solution for any $2\times 1$ column vector $b$” is true by the second part of the invertible matrix theorem.

- Statement “${A}^{-1}$ does **not** exist” is false. According to the first part of the invertible matrix theorem, the inverse ${A}^{-1}$ must exist.

Finally, only statement “$A\mathbf{x}=\mathbf{b}$ has exactly one solution for any $2\times 1$ column vector $b$” is true.

Answer $Ax=b$ has exactly one solution for any $2\times 1$ column vector $b$: true

Answer $\det(A)=0$: false

Answer ${A}^{-1}$ does **not** exist: false

Question 17592186115884 — question.difficulty/moderate

Let $A=\begin{bmatrix}6 & 2 \\ -3 & k\end{bmatrix}$ and $\mathbf{b}=\begin{bmatrix}1 \\ -2\end{bmatrix},$ where $k$ is a constant such that $k\ne -1.$ Which of the following statements are true?

Select all that apply.

Solution: Recall that given $A=\begin{bmatrix}{a}_{11} & {a}_{12} \\ {a}_{21} & {a}_{22}\end{bmatrix}$, then according to the invertible matrix theorem the following statements are equivalent:    

1\. $A$ is invertible.

2\. The system $A\mathbf{x}=\mathbf{b}$ has exactly one solution for any $2\times 1$ column vector $\mathbf{b}.$

3\. The system $A\mathbf{x}=\mathbf{0}$ has the unique zero solution.

4\. The lines ${a}_{11}x+{a}_{12}y={b}_{1}$ and ${a}_{21}x+{a}_{22}y={b}_{2}$ intersect at exactly one point.

5\. $\det(A)\ne 0.$

With that in mind, let's now check our statements.

- Statement $\det(A)\ne 0$ is true. We have 

$$
\begin{aligned}\det(A) & =\det\begin{bmatrix}6 & 2 \\ -3 & k\end{bmatrix} \\  & =6\cdot k-2\cdot (-3) \\  & =6k+6.\end{aligned}
$$

Notice that $6k+6\ne 0$ if $k\ne -1.$

Now, since the fifth part of the invertible matrix theorem is true, all the other parts of the theorem are true too. Therefore, according to the theorem:

- Statement “$A\mathbf{x}=\mathbf{0}$ has no solutions” is false. According to the third part of the invertible matrix theorem, there must be a unique zero solution to $A\mathbf{x}=\mathbf{0}.$

- Statement “The lines $6x+2y=1$ and $-3x+ky=-2$ intersect at infinitely many points” is false. According to the fourth part of the invertible matrix theorem, the lines must intersect at exactly one point.

Finally, only statement $\det(A)\ne 0$ is true.

Answer $Ax=0$ has no solutions: false

Answer $\det(A)\ne 0$: true

Answer The lines $6x+2y=1$ and $-3x+ky=-2$ intersect at infinitely many points: false

Question 17592186262854 — question.difficulty/moderate

Let $A=\begin{bmatrix}1 & 3 \\ -1 & k\end{bmatrix}$ and $\mathbf{b}=\begin{bmatrix}-1 \\ 1\end{bmatrix},$ where $k$ is a constant such that $k\ne -3.$ Which of the following statements are true?

Select all that apply.

Solution: Recall that given $A=\begin{bmatrix}{a}_{11} & {a}_{12} \\ {a}_{21} & {a}_{22}\end{bmatrix}$, then according to the invertible matrix theorem the following statements are equivalent:    

- $A$ is invertible.

- The system $A\mathbf{x}=\mathbf{b}$ has exactly one solution for any $2\times 1$ column vector $\mathbf{b}.$

- The system $A\mathbf{x}=\mathbf{0}$ has the unique zero solution.

- The lines ${a}_{11}x+{a}_{12}y={b}_{1}$ and ${a}_{21}x+{a}_{22}y={b}_{2}$ intersect at exactly one point.

- $\det(A)\ne 0.$

With that in mind, let's now check our statements.

- Statement $\det(A)\ne 0$ is true. We have 

$$
\begin{aligned}\det(A) & =\det\begin{bmatrix}1 & 3 \\ -1 & k\end{bmatrix} \\  & =1\cdot k-(-1)\cdot 3 \\  & =k+3.\end{aligned}
$$

Notice that $k+3\ne 0$ if $k\ne -3.$

Now, since the fifth part of the invertible matrix theorem is true, all the other parts of the theorem are true too. Therefore, according to the theorem:

- Statement “$A\mathbf{x}=\mathbf{0}$ has no solutions” is false. According to the third part of the invertible matrix theorem, the unique solution to  $A\mathbf{x}=\mathbf{0}$ is the trivial one (zero).

- Statement “The lines $x+3y=-1$ and $-x+ky=1$  intersect at exactly one point” is true by the fourth part of the invertible matrix theorem.

Finally, only statements $\det(A)\ne 0$ and “The lines $x+3y=-1$ and $-x+ky=1$  intersect at exactly one point” are true.

Answer $Ax=0$ has no solutions: false

Answer $\det(A)\ne 0$: true

Answer The lines $x+3y=-1$ and $-x+ky=1$  intersect at exactly one point.: true

### Completing a True Statement (16 captured questions)

Question 17592186115734 — question.difficulty/hard

Consider the lines $2x+y=2$ and $x+ky=5$, where $k$ is a constant. Complete the following statement so that it is true:

*If the lines intersect at one point, then $\underline{\phantom{xxxxxx}}\,.$*

Solution: Recall that given $A=\begin{bmatrix}{a}_{11} & {a}_{12} \\ {a}_{21} & {a}_{22}\end{bmatrix}$, then according to the invertible matrix theorem the following statements are equivalent:    

- $A$ is invertible.

- The system $A\mathbf{x}=\mathbf{b}$ has exactly one solution for any $2\times 1$ column vector $\mathbf{b}.$

- The system $A\mathbf{x}=\mathbf{0}$ has the unique zero solution.

- The lines ${a}_{11}x+{a}_{12}y={b}_{1}$ and ${a}_{21}x+{a}_{22}y={b}_{2}$ intersect at exactly one point.

- $\det(A)\ne 0.$

With that in mind, let's now check our statements.

According to the invertible matrix theorem, if the lines $2x+y=2$ and $x+ky=5$ intersect at one point, then

$$
A=\begin{bmatrix}2 & 1 \\ 1 & k\end{bmatrix}
$$

is invertible and $\det(A)\ne 0.$ 
Additionally, the unique solution to $A\mathbf{x}=\mathbf{0}$ is $⟨0,0⟩$ and

$$
\begin{bmatrix}2 & 1 \\ 1 & k\end{bmatrix}\begin{bmatrix}x \\ y\end{bmatrix}=\begin{bmatrix}2 \\ 5\end{bmatrix}
$$

has exactly one solution, which is the intersection point of the lines.

Therefore, the true statement is as follows:

*If the lines intersect at one point, then $\begin{bmatrix}2 & 1 \\ 1 & k\end{bmatrix}$ is invertible.*

Answer selection: $\begin{bmatrix}2 & 1 \\ 1 & k\end{bmatrix}$ is invertible

Question 17592186115749 — question.difficulty/moderate

Which of the following completes the statement so that it is true:

*If a $2\times 2$-matrix $A$ is invertible, then $\underline{\phantom{xxxxxx}}$ .* 

Select all that apply.

Solution: Recall that given $A=\begin{bmatrix}{a}_{11} & {a}_{12} \\ {a}_{21} & {a}_{22}\end{bmatrix}$, then according to the invertible matrix theorem the following statements are equivalent:    

- $A$ is invertible.

- The system $A\mathbf{x}=\mathbf{b}$ has exactly one solution for any $2\times 1$ column vector $\mathbf{b}.$

- The system $A\mathbf{x}=\mathbf{0}$ has the unique zero solution.

- The lines ${a}_{11}x+{a}_{12}y={b}_{1}$ and ${a}_{21}x+{a}_{22}y={b}_{2}$ intersect at exactly one point.

- $\det(A)\ne 0.$

With that in mind, let's now check our statements.

Now, since the first part of the invertible matrix theorem is true ($A$ is invertible), all the other parts of the theorem are true too. Therefore, according to the theorem, only options “$A\mathbf{x}=\mathbf{0}$ has exactly one solution” and $\det(A)\ne 0$ give us true statements:

- *If $A$ is invertible, then $A\mathbf{x}=\mathbf{0}$ has exactly one solution.* $\hspace{1em}{\color{green}✓}$

- *If $A$ is invertible, then $\det(A)\ne 0.$* $\hspace{1em}{\color{green}✓}$

Answer $Ax=0$ has exactly one solution: true

Answer $Ax=0$ has infinitely many solutions: false

Answer $\det(A)\ne 0$: true

Answer None of the above: false

Question 17592186262879 — question.difficulty/moderate

Which of the following completes the statement so that it is true:

*If the system $\begin{bmatrix}a & b \\ c & d\end{bmatrix}\mathbf{x}=\mathbf{0}$ has the unique zero solution, then $\underline{\phantom{xxxxxx}}$ .* 

Select all that apply.

Solution: Recall that given $A=\begin{bmatrix}{a}_{11} & {a}_{12} \\ {a}_{21} & {a}_{22}\end{bmatrix}$, then according to the invertible matrix theorem the following statements are equivalent:    

- $A$ is invertible.

- The system $A\mathbf{x}=\mathbf{b}$ has exactly one solution for any $2\times 1$ column vector $\mathbf{b}.$

- The system $A\mathbf{x}=\mathbf{0}$ has the unique zero solution.

- The lines ${a}_{11}x+{a}_{12}y={b}_{1}$ and ${a}_{21}x+{a}_{22}y={b}_{2}$ intersect at exactly one point.

- $\det(A)\ne 0.$

With that in mind, let's now check our statements.

Now, since the third part of the invertible matrix theorem is true, all the other parts of the theorem are true too. Therefore, according to the theorem, only option $\det\begin{bmatrix}a & b \\ c & d\end{bmatrix}\ne 0$ gives us a true statement:  

*If the system $\begin{bmatrix}a & b \\ c & d\end{bmatrix}\mathbf{x}=\mathbf{0}$ has the unique zero solution, then, $\det\begin{bmatrix}a & b \\ c & d\end{bmatrix}\ne 0$ .* $\hspace{1em}{\color{green}✓}$

Answer $\det\begin{bmatrix}a & b \\ c & d\end{bmatrix}\ne 0$: true

Answer ${\begin{bmatrix}a & b \\ c & d\end{bmatrix}}^{-1}$ does not exist: false

Answer The lines $ax+by=0$ and $cx+dy=0$ intersect at infinitely many points: false
