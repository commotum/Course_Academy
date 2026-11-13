# 17592186049058 Solving 3x3 Systems of Equations Using Gaussian Elimination

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186097841 — Introduction

Consider a system of linear equations and its respective augmented matrix $M\mathbin{:}$


$$
\left\{\begin{aligned}x-y+z &=6 \\ y-3z &=-13 \\ -x-y-z &=-4\end{aligned}\right. \qquad M = \left[ \begin{array}{ccc|c}1 & -1 & 1 & 6 \\ 0 & 1 & -3 & -13 \\ -1 & -1 & -1 & -4\end{array} \right]
$$



We can reduce $M$ to row echelon form using the standard Gaussian elimination algorithm. The algorithm that we use is very similar to the case of $2 \times 2$ systems. 

Our goal is to create a descending "staircase" of $1$'s with $0$'s below, and we achieve this using elementary row operations. So, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{ccc|c}1 & -1 & 1 & 6 \\ 0 & 1 & -3 & -13 \\ -1 & -1 & -1 & -4\end{array}\right] & {R}_{3} & :={R}_{3}+{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -1 & 1 & 6 \\ 0 & 1 & -3 & -13 \\ 0 & -2 & 0 & 2\end{array}\right] & {R}_{3} & :={R}_{3}+2{R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & -1 & 1 & 6 \\ 0 & 1 & -3 & -13 \\ 0 & 0 & -6 & -24\end{array}\right] & {R}_{3} & :=-\frac{1}{6}{R}_{3} \\  & ∼\left[\begin{array}{ccc|c}{\color{red}1} & -1 & 1 & 6 \\ {\color{blue}0} & {\color{red}1} & -3 & -13 \\ {\color{blue}0} & {\color{blue}0} & {\color{red}1} & 4\end{array}\right].\end{aligned}
$$

The matrix is now in row echelon form, and we can apply back substitution to solve the original system of equations.

**Note:** The row echelon form of a matrix is *not* unique.  In the previous example, after the second row operation we arrived at



$$
\left[ \begin{array}{ccc|c}{\color{red}1} & -1 & 1 & 6 \\ {\color{blue}0} & {\color{red}1} & -3 & -13 \\ {\color{blue}0} & {\color{blue}0} & {\color{red}-6} & -24\end{array}\right].
$$



This augmented matrix is already in row echelon form! However, it is always useful to do an extra step and obtain $1$'s along the main diagonal, like we did previously:



$$
\left[ \begin{array}{ccc|c}{\color{red}1} & -1 & 1 & 6 \\ {\color{blue}0} & {\color{red}1} & -3 & -13 \\ {\color{blue}0} & {\color{blue}0} & {\color{red}1} & 4\end{array}\right]
$$



Having $1$'s along the main diagonal makes the final back substitution process a little easier.



### tutorial 17592186097842 — General Algorithm

The **standard Gaussian elimination** for a $3 \times 3$ system can be described as follows:

1. If $a_{11} \neq 0$ and $a_{11} \neq 1,$ then we use the row operation $R_1:=R_1/a_{11}.$

2. We use first row and the necessary row operations to make the remaining entries of the first column below $a_{11}$ equal to $0.$ Namely,

   - if $a_{21} \neq 0,$ then we use the row operation $R_2:=R_2 + (-a_{21})R_1;$
   - if $a_{31} \neq 0,$ then we use the row operation $R_3:=R_3 + (-a_{31})R_1.$

3. If $a_{22} \neq 1,$ then we use the row operation $R_2:=R_2/a_{22}.$

4. We use the second row and the necessary row operation to make the entry below $a_{22}$ equal to $0.$ Namely,

   - if $a_{32} \neq 0,$ then we use the row operation $R_3:=R_3 + (-a_{32})R_2.$

5. If $a_{33} \neq 1,$ then we use the row operation $R_3:=R_3/a_{33}.$

6. In some exceptional cases, such as when the element on the diagonal is equal to $0,$ we first need to exchange rows. Then proceed using the same steps as above.

Carrying out the above algorithm will convert the matrix to row echelon form.



### example 17592186096459 — Solving a 3x3 System of Equations Using Standard Gaussian Elimination

Consider the system of linear equations



$$
\left\{\begin{aligned}x-y+z &=1 \\ y+z &=-2 \\ -x+2y+z &=-1.\end{aligned}\right.
$$



Use the standard method of Gaussian elimination to reduce the augmented matrix $M$ of the system to row echelon form, and then solve the linear system.

Reducing $M$ to row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{ccc|c}1 & -1 & 1 & 1 \\ 0 & 1 & 1 & -2 \\ -1 & 2 & 1 & -1\end{array}\right] & {R}_{3} & :={R}_{3}+{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -1 & 1 & 1 \\ 0 & 1 & 1 & -2 \\ 0 & 1 & 2 & 0\end{array}\right] & {R}_{3} & :={R}_{3}+(-1){R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & -1 & 1 & 1 \\ 0 & 1 & 1 & -2 \\ 0 & 0 & 1 & 2\end{array}\right].\end{aligned}
$$

The system is now


$$
\left\{\begin{aligned}x-y+z &=1 \\ y+z &=-2 \\ z &=2,\end{aligned}\right.
$$



and we can apply back substitution. The final equation $z=2$ tells us the value of $z.$ Substituting this value into the second equation, we get

$$
\begin{aligned}y+(2) &=-2\,⟹\,y=-4.\end{aligned}
$$

Finally, substituting both $y=-4$ and $z=2$ into the first equation, we get

$$
\begin{aligned}x-(-4)+(2) &=1\,⟹\,x=-5.\end{aligned}
$$

Therefore, the solution is $x=-5,$ $y=-4,$ and $z=2.$ Or, in vector form, $\langle -5,-4,2 \rangle.$

### example 17592186096460 — Solving a 3x3 System of Equations Using Standard Gaussian Elimination with Row Exchanges

Consider the system of linear equations


$$
\left\{\begin{aligned}x+y+z &=-2 \\ x+y+2z &=-1 \\ x+2y+z &=1.\end{aligned}\right.
$$



Use the standard method of Gaussian elimination to reduce the augmented matrix $M$ of the system to row echelon form, and then solve the linear system.

The augmented matrix for this system is



$$
M= \left[\begin{array}{ccc|c}1 & 1 & 1 & -2 \\ 1 & 1 & 2 & -1 \\ 1 & 2 & 1 & 1\end{array}\right].
$$



Reducing $M$ to row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{ccc|c}1 & 1 & 1 & -2 \\ 1 & 1 & 2 & -1 \\ 1 & 2 & 1 & 1\end{array}\right] & {R}_{2} & :={R}_{2}+(-1){R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & 1 & -2 \\ 0 & 0 & 1 & 1 \\ 1 & 2 & 1 & 1\end{array}\right] & {R}_{3} & :={R}_{3}+(-1){R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & 1 & -2 \\ 0 & 0 & 1 & 1 \\ 0 & 1 & 0 & 3\end{array}\right].\end{aligned}
$$

Note that we get $a_{22}=0.$ Therefore, we swap the $2$nd and $3$rd rows:

$$
\begin{aligned} & ∼\left[\begin{array}{ccc|c}1 & 1 & 1 & -2 \\ 0 & 0 & 1 & 1 \\ 0 & 1 & 0 & 3\end{array}\right] & {R}_{2} & ↔{R}_{3} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & 1 & -2 \\ 0 & 1 & 0 & 3 \\ 0 & 0 & 1 & 1\end{array}\right]\end{aligned}
$$

The system is now


$$
\left\{\begin{aligned}x+y+z &=-2 \\ y &=3 \\ z &=1,\end{aligned}\right.
$$



and we can apply back substitution. The third equation $z=1$ tells us the value of $z,$ and the second equation $y=3$ tells us the value of $y.$ Substituting these values into the first equation, we get

$$
\begin{aligned}x+(3)+(1) &=-2\,⟹\,x=-6.\end{aligned}
$$

Therefore, the solution is $x=-6,$ $y=3,$ and $z=1.$ Or, in vector form, $\langle -6,3,1 \rangle.$

## Representative practice (first three per skill; full bank in practice.json)

### Solving a 3x3 System of Equations Using Standard Gaussian Elimination (40 captured questions)

Question 17592186096937 — question.difficulty/moderate

Consider the augmented matrix $M$ given by 

$$
M=\left[\begin{array}{ccc|c}1 & 1 & 2 & 19 \\ 0 & 1 & 2 & 13 \\ 1 & 3 & 2 & 25\end{array}\right].
$$

Use the standard method of Gaussian elimination to reduce the augmented matrix $M$ of the system to row echelon form, and then solve the linear system.

Solution: Reducing $M$ to row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{ccc|c}1 & 1 & 2 & 19 \\ 0 & 1 & 2 & 13 \\ 1 & 3 & 2 & 25\end{array}\right] & {R}_{3} & :={R}_{3}-{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & 2 & 19 \\ 0 & 1 & 2 & 13 \\ 0 & 2 & 0 & 6\end{array}\right] & {R}_{3} & :={R}_{3}-2{R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & 2 & 19 \\ 0 & 1 & 2 & 13 \\ 0 & 0 & -4 & -20\end{array}\right] & {R}_{3} & :=-\frac{1}{4}{R}_{3} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & 2 & 19 \\ 0 & 1 & 2 & 13 \\ 0 & 0 & 1 & 5\end{array}\right].\end{aligned}
$$

The system is now

$$
\left\{\begin{aligned}x+y+2z &=19 \\ y+2z &=13 \\ z &=5,\end{aligned}\right.
$$

and we can apply back substitution. The final equation $z=5$ tells us the value of $z.$ Substituting this value into the second equation, we get

$$
y+2(5)=13\,⟹\,y=13-10=3.
$$

Finally, substituting both $y=3$ and $z=5$ into the first equation, we get

$$
x+(3)+2(5)=19\,⟹\,x=6.
$$

Therefore, the solution is $x=6,y=3$, and $z=5.$ Or, in vector form, $⟨6,3,5⟩.$

Answer selection: ⟨6,3,5⟩

Question 17592186097183 — question.difficulty/easy

Consider the system of linear equations

$$
\left\{\begin{aligned}x+2y+6z &=5 \\ y-10z &=-11 \\ 4x+8y+13z &=9\end{aligned}\right.
$$

Use the standard method of Gaussian elimination to reduce the augmented matrix $M$ of the system to row echelon form.

Solution: The augmented matrix for this system is

$$
M=\left[\begin{array}{ccc|c}1 & 2 & 6 & 5 \\ 0 & 1 & -10 & -11 \\ 4 & 8 & 13 & 9\end{array}\right].
$$

Reducing $M$ to row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{ccc|c}1 & 2 & 6 & 5 \\ 0 & 1 & -10 & -11 \\ 4 & 8 & 13 & 9\end{array}\right] & {R}_{3} & :={R}_{3}-4{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 2 & 6 & 5 \\ 0 & 1 & -10 & -11 \\ 0 & 0 & -11 & -11\end{array}\right] & {R}_{3} & :=-\frac{1}{11}{R}_{3} \\  & ∼\left[\begin{array}{ccc|c}1 & 2 & 6 & 5 \\ 0 & 1 & -10 & -11 \\ 0 & 0 & 1 & 1\end{array}\right].\end{aligned}
$$

Answer selection: M∼\left[\begin{array}{ccc|c}1 & 2 & 6 & 5 \\ 0 & 1 & -10 & -11 \\ 0 & 0 & 1 & 1\end{array}\right]

Question 17592186266014 — question.difficulty/moderate

Consider the augmented matrix $M$ given by 

$$
M=\left[\begin{array}{ccc|c}3 & -6 & 3 & -9 \\ -2 & 5 & -4 & 4 \\ 0 & 3 & -5 & 2\end{array}\right].
$$

Use the standard method of Gaussian elimination to reduce the augmented matrix $M$ of the system to row echelon form, and then solve the linear system.

Solution: Reducing $M$ to row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{ccc|c}3 & -6 & 3 & -9 \\ -2 & 5 & -4 & 4 \\ 0 & 3 & -5 & 2\end{array}\right] & {R}_{1} & :=\frac{1}{3}{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -2 & 1 & -3 \\ -2 & 5 & -4 & 4 \\ 0 & 3 & -5 & 2\end{array}\right] & {R}_{2} & :={R}_{2}+2{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -2 & 1 & -3 \\ 0 & 1 & -2 & -2 \\ 0 & 3 & -5 & 2\end{array}\right] & {R}_{3} & :={R}_{3}-3{R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & -2 & 1 & -3 \\ 0 & 1 & -2 & -2 \\ 0 & 0 & 1 & 8\end{array}\right].\end{aligned}
$$

The system is now

$$
\left\{\begin{aligned}x-2y+z &=-3 \\ y-2z &=-2 \\ z &=8,\end{aligned}\right.
$$

and we can apply back substitution. The final equation $z=8$ tells us the value of $z.$ Substituting this value into the second equation, we get

$$
y-2(8)=-2\,⟹\,y=-2+16=14.
$$

Finally, substituting both $y=14$ and $z=8$ into the first equation, we get

$$
x-2(14)+(8)=-3\,⟹\,x=17.
$$

Therefore, the solution is $x=17,y=14$, and $z=8.$ Or, in vector form, $⟨17,14,8⟩.$

Answer selection: ⟨17,14,8⟩

### Solving a 3x3 System of Equations Using Standard Gaussian Elimination with Row Exchanges (44 captured questions)

Question 17592186097349 — question.difficulty/moderate

Consider the system of linear equations

$$
\left\{\begin{aligned}x-y+2z &=8 \\ -2x+2y-3z &=-11 \\ x+z &=9.\end{aligned}\right.
$$

Use the standard method of Gaussian elimination to reduce the augmented matrix $M$ of the system to row echelon form, and then solve the linear system.

Solution: The augmented matrix for this system is

$$
M=\left[\begin{array}{ccc|c}1 & -1 & 2 & 8 \\ -2 & 2 & -3 & -11 \\ 1 & 0 & 1 & 9\end{array}\right].
$$

Reducing $M$ to row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{ccc|c}1 & -1 & 2 & 8 \\ -2 & 2 & -3 & -11 \\ 1 & 0 & 1 & 9\end{array}\right] & {R}_{2} & :={R}_{2}+2{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -1 & 2 & 8 \\ 0 & 0 & 1 & 5 \\ 1 & 0 & 1 & 9\end{array}\right] & {R}_{3} & :={R}_{3}+(-1){R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -1 & 2 & 8 \\ 0 & 0 & 1 & 5 \\ 0 & 1 & -1 & 1\end{array}\right].\end{aligned}
$$

Note that we get ${a}_{22}=0.$ Therefore, we swap the $2$nd and $3$rd rows:

$$
\begin{aligned} & ∼\left[\begin{array}{ccc|c}1 & -1 & 2 & 8 \\ 0 & 0 & 1 & 5 \\ 0 & 1 & -1 & 1\end{array}\right] & {R}_{2} & ↔{R}_{3} \\  & ∼\left[\begin{array}{ccc|c}1 & -1 & 2 & 8 \\ 0 & 1 & -1 & 1 \\ 0 & 0 & 1 & 5\end{array}\right]\end{aligned}
$$

So, the system is now

$$
\left\{\begin{aligned}x-y+2z &=8 \\ y-z &=1 \\ z &=5,\end{aligned}\right.
$$

and we can apply back substitution. The third equation $z=5$ tells us the value of $z.$ Substituting this value into the second equation, we get

$$
\begin{aligned}y-(5) &=1\,⟹\,y=6.\end{aligned}
$$

Now, substituting $y=6$ and $z=5$ into the first equation, we get

$$
\begin{aligned}x-(6)+2(5) &=8\,⟹\,x=4.\end{aligned}
$$

Thus, the solution is $x=4$, $y=6$, and $z=5.$

Answer selection: $x=4$, $y=6$, and $z=5$

Question 17592186097350 — question.difficulty/hard

Consider the augmented matrix $M$ given by

$$
M=\left[\begin{array}{ccc|c}1 & 2 & 3 & 1 \\ 1 & 2 & 5 & 3 \\ 2 & 1 & 4 & 9\end{array}\right].
$$

Use the standard method of Gaussian elimination to reduce the augmented matrix $M$ of the system to row echelon form.

Solution: Reducing $M$ to row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{ccc|c}1 & 2 & 3 & 1 \\ 1 & 2 & 5 & 3 \\ 2 & 1 & 4 & 9\end{array}\right] & {R}_{2} & :={R}_{2}+(-1){R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 2 & 3 & 1 \\ 0 & 0 & 2 & 2 \\ 2 & 1 & 4 & 9\end{array}\right] & {R}_{3} & :={R}_{3}+(-2){R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 2 & 3 & 1 \\ 0 & 0 & 2 & 2 \\ 0 & -3 & -2 & 7\end{array}\right].\end{aligned}
$$

Note that we get ${a}_{22}=0.$ Therefore, we swap the $2$nd and $3$rd rows:

$$
\begin{aligned} & ∼\left[\begin{array}{ccc|c}1 & 2 & 3 & 1 \\ 0 & 0 & 2 & 2 \\ 0 & -3 & -2 & 7\end{array}\right] & {R}_{2} & ↔{R}_{3} \\  & ∼\left[\begin{array}{ccc|c}1 & 2 & 3 & 1 \\ 0 & -3 & -2 & 7 \\ 0 & 0 & 2 & 2\end{array}\right]\end{aligned}
$$

Finally, we multiply the $2$nd row by $-\frac{1}{3}$ and the $3$rd row by $\frac{1}{2}$ to get

$$
\begin{aligned} & ∼\left[\begin{array}{ccc|c}1 & 2 & 3 & 1 \\ 0 & -3 & -2 & 7 \\ 0 & 0 & 2 & 2\end{array}\right] & {R}_{2} & :=-\frac{1}{3}{R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & 2 & 3 & 1 \\ 0 & 1 & \frac{2}{3} & -\frac{7}{3} \\ 0 & 0 & 2 & 2\end{array}\right] & {R}_{3} & :=\frac{1}{2}{R}_{3} \\  & ∼\left[\begin{array}{ccc|c}1 & 2 & 3 & 1 \\ 0 & 1 & \frac{2}{3} & -\frac{7}{3} \\ 0 & 0 & 1 & 1\end{array}\right].\end{aligned}
$$

Answer selection: M∼\left[\begin{array}{ccc|c}1 & 2 & 3 & 1 \\ 0 & 1 & \frac{2}{3} & -\frac{7}{3} \\ 0 & 0 & 1 & 1\end{array}\right]

Question 17592186266015 — question.difficulty/hard

Consider the augmented matrix $M$ given by

$$
M=\left[\begin{array}{ccc|c}4 & -4 & -12 & 8 \\ -1 & 1 & 10 & -5 \\ 0 & 3 & -9 & -6\end{array}\right].
$$

Use the standard method of Gaussian elimination to reduce the augmented matrix $M$ of the system to row echelon form.

Solution: Reducing $M$ to row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{ccc|c}4 & -4 & -12 & 8 \\ -1 & 1 & 10 & -5 \\ 0 & 3 & -9 & -6\end{array}\right] & {R}_{1} & :=\frac{1}{4}{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -1 & -3 & 2 \\ -1 & 1 & 10 & -5 \\ 0 & 3 & -9 & -6\end{array}\right] & {R}_{2} & :={R}_{2}+{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -1 & -3 & 2 \\ 0 & 0 & 7 & -3 \\ 0 & 3 & -9 & -6\end{array}\right].\end{aligned}
$$

Note that we get ${a}_{22}=0.$ Therefore, we swap the $2$nd and $3$rd rows:

$$
\begin{aligned} & ∼\left[\begin{array}{ccc|c}1 & -1 & -3 & 2 \\ 0 & 0 & 7 & -3 \\ 0 & 3 & -9 & -6\end{array}\right] & {R}_{2} & ↔{R}_{3} \\  & ∼\left[\begin{array}{ccc|c}1 & -1 & -3 & 2 \\ 0 & 3 & -9 & -6 \\ 0 & 0 & 7 & -3\end{array}\right]\end{aligned}
$$

Finally, we multiply the $2$nd row by $\frac{1}{3}$ and the $3$rd row by $\frac{1}{7}$ to get

$$
\begin{aligned} & ∼\left[\begin{array}{ccc|c}1 & -1 & -3 & 2 \\ 0 & 3 & -9 & -6 \\ 0 & 0 & 7 & -3\end{array}\right] & {R}_{2} & :=\frac{1}{3}{R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & -1 & -3 & 2 \\ 0 & 1 & -3 & -2 \\ 0 & 0 & 7 & -3\end{array}\right] & {R}_{3} & :=\frac{1}{7}{R}_{3} \\  & ∼\left[\begin{array}{ccc|c}1 & -1 & -3 & 2 \\ 0 & 1 & -3 & -2 \\ 0 & 0 & 1 & -\frac{3}{7}\end{array}\right].\end{aligned}
$$

Answer selection: M∼\left[\begin{array}{ccc|c}1 & -1 & -3 & 2 \\ 0 & 1 & -3 & -2 \\ 0 & 0 & 1 & -\frac{3}{7}\end{array}\right]
