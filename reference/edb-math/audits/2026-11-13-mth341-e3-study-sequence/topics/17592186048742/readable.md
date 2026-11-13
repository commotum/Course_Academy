# 17592186048742 Reduced Row Echelon Form

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186097843 — Introduction

Consider a system of linear equations and its respective augmented matrix $M\mathbin{:}$


$$
\left\{\begin{aligned}x+y+z &=2 \\ y+z &=-1 \\ -2z &=2\end{aligned}\right. \qquad M = \left[ \begin{array}{ccc|c}1 & 1 & 1 & 2 \\ 0 & 1 & 1 & -1 \\ 0 & 0 & -2 & 2\end{array} \right]
$$



The matrix $M$ is already in row echelon form, but we can transform it even further into the **reduced row echelon form** (RREF) using the standard **Gauss-Jordan** method. 

The algorithm is similar to the algorithm of converting a matrix to row echelon form, except that we need to make *all* the pivot entries equal to $1$ and *all* the entries below *and above* a pivot (in a pivot column) equal to $0.$

In our case, we convert $M$ to reduced row echelon form as follows:

$$
\begin{aligned}M & =\left[\begin{array}{ccc|c}1 & 1 & 1 & 2 \\ 0 & 1 & 1 & -1 \\ 0 & 0 & -2 & 2\end{array}\right] & {R}_{3} & :=-\frac{1}{2}{R}_{3} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & 1 & 2 \\ 0 & 1 & 1 & -1 \\ 0 & 0 & 1 & -1\end{array}\right] & {R}_{2} & :={R}_{2}+(-1){R}_{3} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & 1 & 2 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & -1\end{array}\right] & {R}_{1} & :={R}_{1}+(-1){R}_{3} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & 0 & 3 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & -1\end{array}\right] & {R}_{1} & :={R}_{1}+(-1){R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & 0 & 0 & 3 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & -1\end{array}\right]\end{aligned}
$$

The final matrix is in reduced row echelon form:

- all the pivot entries are equal to $1$ (here we have $\color{red}1$'s on the main diagonal), and

- all the entries below and above a pivot are equal to ${\color{blue}0}.$



### tutorial 17592186097844 — General Algorithm (RREF)

For a $3\times 3$ system with $3$ pivots, the Gauss-Jordan method can be described as follows:

1\. First, reduce the matrix to row echelon form using the standard Gaussian elimination method (also making all pivot entries equal to $1$). 
  

$$
\left[ \begin{array}{ccc|c}{\color{red}1} & \ast & \ast & \ast \\ {\color{blue}0} & {\color{red}1} & \ast & \ast \\ {\color{blue}0} & {\color{blue}0} & {\color{red}1} & \ast \end{array} \right]
$$



2\. We use the third row and necessary row operations to make the entries above $a_{33}$ equal to $0.$ Namely, 

  - if $a_{23} \neq 0$, then we use the row operation $R_2:=R_2 + (-a_{23})R_3$, and

  - if $a_{13} \neq 0$, then we use the row operation $R_1:=R_1 + (-a_{13})R_3$.

3\. We use the second row and necessary row operations to make the entries above $a_{22}$ equal to $0$. Namely, 

  - if $a_{12} \neq 0$, then we use the row operation $R_1:=R_1 + (-a_{12})R_2$.

Carrying out the above algorithm will convert the matrix to reduced row echelon form.



$$
\left[ \begin{array}{ccc|c}{\color{red}1} & {\color{blue}0} & {\color{blue}0} & \ast \\ {\color{blue}0} & {\color{red}1} & {\color{blue}0} & \ast \\ {\color{blue}0} & {\color{blue}0} & {\color{red}1} & \ast \end{array} \right]
$$



**Note:** Unlike the row echelon form, the *reduced* row echelon form of a matrix is unique.



### example 17592186096461 — Finding the Reduced Row Echelon Form of a 3x3 System That Is Already in Row Echelon Form

Consider the following system of linear equations:


$$
\left\{\begin{aligned}x-y+z &=-3 \\ y+2z &=-7 \\ z &=-4\end{aligned}\right.
$$



Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

The augmented matrix for this system is


$$
M= \left[\begin{array}{ccc|c}1 & -1 & 1 & -3 \\ 0 & 1 & 2 & -7 \\ 0 & 0 & 1 & -4\end{array}\right].
$$



Transforming $M$ into reduced row echelon form, we have

$$
\begin{aligned}M & =\left[\begin{array}{ccc|c}1 & -1 & 1 & -3 \\ 0 & 1 & 2 & -7 \\ 0 & 0 & 1 & -4\end{array}\right] & {R}_{2} & :={R}_{2}+(-2){R}_{3} \\  & ∼\left[\begin{array}{ccc|c}1 & -1 & 1 & -3 \\ 0 & 1 & 0 & 1 \\ 0 & 0 & 1 & -4\end{array}\right] & {R}_{1} & :={R}_{1}+(-1){R}_{3} \\  & ∼\left[\begin{array}{ccc|c}1 & -1 & 0 & 1 \\ 0 & 1 & 0 & 1 \\ 0 & 0 & 1 & -4\end{array}\right] & {R}_{1} & :={R}_{1}+{R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & 0 & 0 & 2 \\ 0 & 1 & 0 & 1 \\ 0 & 0 & 1 & -4\end{array}\right].\end{aligned}
$$

The corresponding system is now


$$
\left\{\begin{aligned}x &=2 \\ y &=1 \\ z &=-4.\end{aligned}\right.
$$



So, we have the solution $x=2,$ $y=1,$ and $z=-4.$ Or, in vector form, $\langle 2,1,-4 \rangle.$

### example 17592186096462 — Finding the Reduced Row Echelon Form of a 3x3 System That Is Not in Row Echelon Form

Consider the following system of linear equations:


$$
\left\{\begin{aligned}x+y-z &=1 \\ 2x+y+3z &=4 \\ 5x+4y+z &=7\end{aligned}\right.
$$


Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

The augmented matrix for this system is


$$
M= \left[ \begin{array}{ccc|c}1 & 1 & -1 & 1 \\ 2 & 1 & 3 & 4 \\ 5 & 4 & 1 & 7\end{array} \right].
$$



Transforming $M$ into reduced row echelon form, we have

$$
\begin{aligned}M & =\left[\begin{array}{ccc|c}1 & 1 & -1 & 1 \\ 2 & 1 & 3 & 4 \\ 5 & 4 & 1 & 7\end{array}\right] & {R}_{2} & :={R}_{2}-2{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & -1 & 1 \\ 0 & -1 & 5 & 2 \\ 5 & 4 & 1 & 7\end{array}\right] & {R}_{3} & :={R}_{3}-5{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & -1 & 1 \\ 0 & -1 & 5 & 2 \\ 0 & -1 & 6 & 2\end{array}\right] & {R}_{2} & :=-{R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & -1 & 1 \\ 0 & 1 & -5 & -2 \\ 0 & -1 & 6 & 2\end{array}\right] & {R}_{3} & :={R}_{3}+{R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & -1 & 1 \\ 0 & 1 & -5 & -2 \\ 0 & 0 & 1 & 0\end{array}\right] & {R}_{2} & :={R}_{2}+5{R}_{3} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & -1 & 1 \\ 0 & 1 & 0 & -2 \\ 0 & 0 & 1 & 0\end{array}\right] & {R}_{1} & :={R}_{1}+{R}_{3} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & 0 & 1 \\ 0 & 1 & 0 & -2 \\ 0 & 0 & 1 & 0\end{array}\right] & {R}_{1} & :={R}_{1}+(-1){R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & 0 & 0 & 3 \\ 0 & 1 & 0 & -2 \\ 0 & 0 & 1 & 0\end{array}\right].\end{aligned}
$$

The corresponding system is now


$$
\left\{\begin{aligned}x &=3 \\ y &=-2 \\ z &=0.\end{aligned}\right.
$$



So, we have the solution $x=3,$ $y=-2,$ and $z=0.$ Or, in vector form, $\langle 3,-2,0 \rangle.$

### tutorial 17592186097869 — Using the Gauss-Jordan Method on a 3x3 System With Two Pivots

When a $3\times3$ system of equations has two pivot columns instead of three, we can still reduce its augmented matrix to reduced row echelon form. The process is similar to what we did before. 

1\. First, reduce the matrix to row echelon form using the standard Gaussian elimination method (also making all pivot entries equal to $1$). 
   

$$
\left[ \begin{array}{ccc|c}{\color{red}1} & \ast & \ast & \ast \\ {\color{blue}0} & {\color{red}1} & \ast & \ast \\ {\color{blue}0} & {\color{blue}0} & {\color{blue}0} & \ast \end{array} \right]
$$



2\. We use the second row and necessary row operations to make the entries above $a_{22}$ equal to $0$. Namely, 

  - if $a_{12} \neq 0$, then we use the row operation $R_1:=R_1 + (-a_{12})R_2$.

Carrying out the above algorithm will convert the matrix to reduced row echelon form.



$$
\left[ \begin{array}{ccc|c}{\color{red}1} & {\color{blue}0} & \ast & \ast \\ {\color{blue}0} & {\color{red}1} & \ast & \ast \\ {\color{blue}0} & {\color{blue}0} & {\color{blue}0} & \ast \end{array} \right]
$$





### example 17592186096546 — Finding the Reduced Row Echelon Form of a Singular 3x3 System With Two Pivots

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x-2y &=2 \\ x-4z &=6 \\ -3x+6y &=-6\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

The augmented matrix for this system is


$$
M= \left[ \begin{array}{ccc|c}1 & -2 & 0 & 2 \\ 1 & 0 & -4 & 6 \\ -3 & 6 & 0 & -6\end{array} \right].
$$



Transforming $M$ into reduced row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{ccc|c}1 & -2 & 0 & 2 \\ 1 & 0 & -4 & 6 \\ -3 & 6 & 0 & -6\end{array}\right] & {R}_{2} & :={R}_{2}+(-1){R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -2 & 0 & 2 \\ 0 & 2 & -4 & 4 \\ -3 & 6 & 0 & -6\end{array}\right] & {R}_{3} & :={R}_{3}+3{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -2 & 0 & 2 \\ 0 & 2 & -4 & 4 \\ 0 & 0 & 0 & 0\end{array}\right] & {R}_{2} & :=\frac{1}{2}{R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & -2 & 0 & 2 \\ 0 & 1 & -2 & 2 \\ 0 & 0 & 0 & 0\end{array}\right].\end{aligned}
$$

In the row echelon form above, we have only two pivots (in the $1$st and $2$nd columns). To transform the matrix to reduced row echelon form, we need to create zeros above the pivots only. This gives,

$$
\begin{aligned}M & ∼\left[\begin{array}{ccc|c}1 & -2 & 0 & 2 \\ 0 & 1 & -2 & 2 \\ 0 & 0 & 0 & 0\end{array}\right] & {R}_{1} & :={R}_{1}+2{R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & 0 & -4 & 6 \\ 0 & 1 & -2 & 2 \\ 0 & 0 & 0 & 0\end{array}\right].\end{aligned}
$$

The corresponding system is now


$$
\left\{\begin{aligned}x-4z &=6 \\ y-2z &=2 \\ 0 &=0.\end{aligned}\right.
$$



Since any numbers $x,y,z$ form a solution of the final equation, we can remove this equation from the system. 

The basic variables are the variables whose coefficients are pivots. In this case, the basic variables are $x$ and $y,$ and we have one free variable, $z.$ That means we need to find $x$ and $y$ in terms of $z.$ 

Therefore, the general solution is

$$
\left\{\begin{aligned}x &=4z+6 \\ y &=2z+2 \\ z &=z,\end{aligned}\right.
$$

where $z$ (the free variable) is an arbitrary number.

In vector form, the solution can be written as

$$
\begin{aligned}\begin{bmatrix}x \\ y \\ z\end{bmatrix}=\begin{bmatrix}4z+6 \\ 2z+2 \\ z\end{bmatrix},\,z\in (-\infty ,\infty ).\end{aligned}
$$

### tutorial 17592186097870 — Using the Gauss-Jordan Method on a 3x3 System With One Pivot

It's also possible to write the augmented matrix for a $3\times 3$ system of linear equations with only one pivot in reduced row echelon form. 

Let's see an example of how this works.



### example 17592186096547 — Finding the Reduced Row Echelon Form of a Singular 3x3 System With One Pivot

Consider the following system of linear equations:

$$
\left\{\begin{aligned}2x-6y+2z &=8 \\ -6x+18y-6z &=-24 \\ 4x-12y+4z &=16\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form.

The augmented matrix for this system is


$$
M= \left[ \begin{array}{ccc|c}2 & -6 & 2 & 8 \\ -6 & 18 & -6 & -24 \\ 4 & -12 & 4 & 16\end{array} \right].
$$



Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{ccc|c}2 & -6 & 2 & 8 \\ -6 & 18 & -6 & -24 \\ 4 & -12 & 4 & 16\end{array}\right] & {R}_{1} & :=\frac{1}{2}{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -3 & 1 & 4 \\ -6 & 18 & -6 & -24 \\ 4 & -12 & 4 & 16\end{array}\right] & {R}_{2} & :={R}_{2}+6{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -3 & 1 & 4 \\ 0 & 0 & 0 & 0 \\ 4 & -12 & 4 & 16\end{array}\right] & {R}_{3} & :={R}_{3}+(-4){R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -3 & 1 & 4 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0\end{array}\right].\end{aligned}
$$

Therefore,


$$
M\sim \left[\begin{array}{ccc|c}1 & -3 & 1 & 4 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0\end{array}\right].
$$



## Representative practice (first three per skill; full bank in practice.json)

### Finding the Reduced Row Echelon Form of a 3x3 System That Is Already in Row Echelon Form (36 captured questions)

Question 17592186097184 — None

Consider the following system of linear equations:
$$
\displaystyle \left\{\begin{aligned}x + z &=4 \\ y - z &=-4 \\ z &=1\end{aligned}\right.
$$
Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

Solution: 

Question 17592186097185 — question.difficulty/easy

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x+2y+z &=14 \\ y+z &=8 \\ z &=4\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form.

Solution: The augmented matrix for this system is

$$
M=\left[\begin{array}{ccc|c}1 & 2 & 1 & 14 \\ 0 & 1 & 1 & 8 \\ 0 & 0 & 1 & 4\end{array}\right].
$$

Notice that the matrix $M$ is already in row echelon form.

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{ccc|c}1 & 2 & 1 & 14 \\ 0 & 1 & 1 & 8 \\ 0 & 0 & 1 & 4\end{array}\right] & {R}_{2} & :={R}_{2}+(-1){R}_{3} \\  & ∼\left[\begin{array}{ccc|c}1 & 2 & 1 & 14 \\ 0 & 1 & 0 & 4 \\ 0 & 0 & 1 & 4\end{array}\right] & {R}_{1} & :={R}_{1}+(-1){R}_{3} \\  & ∼\left[\begin{array}{ccc|c}1 & 2 & 0 & 10 \\ 0 & 1 & 0 & 4 \\ 0 & 0 & 1 & 4\end{array}\right] & {R}_{1} & :={R}_{1}+(-2){R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & 0 & 0 & 2 \\ 0 & 1 & 0 & 4 \\ 0 & 0 & 1 & 4\end{array}\right].\end{aligned}
$$

Answer selection: M∼\left[\begin{array}{ccc|c}1 & 0 & 0 & 2 \\ 0 & 1 & 0 & 4 \\ 0 & 0 & 1 & 4\end{array}\right]

Question 17592186288001 — question.difficulty/easy

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x+3y+4z &=-6 \\ y+z &=-1 \\ z &=-2\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

Solution: The augmented matrix for this system is

$$
M=\left[\begin{array}{ccc|c}1 & 3 & 4 & -6 \\ 0 & 1 & 1 & -1 \\ 0 & 0 & 1 & -2\end{array}\right].
$$

Notice that the matrix $M$ is already in row echelon form.

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{ccc|c}1 & 3 & 4 & -6 \\ 0 & 1 & 1 & -1 \\ 0 & 0 & 1 & -2\end{array}\right] & {R}_{2} & :={R}_{2}+(-1){R}_{3} \\  & ∼\left[\begin{array}{ccc|c}1 & 3 & 4 & -6 \\ 0 & 1 & 0 & 1 \\ 0 & 0 & 1 & -2\end{array}\right] & {R}_{1} & :={R}_{1}+(-4){R}_{3} \\  & ∼\left[\begin{array}{ccc|c}1 & 3 & 0 & 2 \\ 0 & 1 & 0 & 1 \\ 0 & 0 & 1 & -2\end{array}\right] & {R}_{1} & :={R}_{1}+(-3){R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & 0 & 0 & -1 \\ 0 & 1 & 0 & 1 \\ 0 & 0 & 1 & -2\end{array}\right].\end{aligned}
$$

The corresponding system is now

$$
\left\{\begin{aligned}x &=-1 \\ y &=1 \\ z &=-2.\end{aligned}\right.
$$

So, we have the solution $x=-1$, $y=1$, and $z=-2.$ In vector form $⟨-1,1,-2⟩.$

Answer selection: ⟨-1,1,-2⟩

### Finding the Reduced Row Echelon Form of a 3x3 System That Is Not in Row Echelon Form (31 captured questions)

Question 17592186097173 — question.difficulty/moderate

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x-y+z &=1 \\ 2x-y+z &=3 \\ -x+y &=-3\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form.

Solution: The augmented matrix for this system is

$$
M=\left[\begin{array}{ccc|c}1 & -1 & 1 & 1 \\ 2 & -1 & 1 & 3 \\ -1 & 1 & 0 & -3\end{array}\right].
$$

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{ccc|c}1 & -1 & 1 & 1 \\ 2 & -1 & 1 & 3 \\ -1 & 1 & 0 & -3\end{array}\right] & {R}_{2} & :={R}_{2}-2{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -1 & 1 & 1 \\ 0 & 1 & -1 & 1 \\ -1 & 1 & 0 & -3\end{array}\right] & {R}_{3} & :={R}_{3}+{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -1 & 1 & 1 \\ 0 & 1 & -1 & 1 \\ 0 & 0 & 1 & -2\end{array}\right] & {R}_{2} & :={R}_{2}+{R}_{3} \\  & ∼\left[\begin{array}{ccc|c}1 & -1 & 1 & 1 \\ 0 & 1 & 0 & -1 \\ 0 & 0 & 1 & -2\end{array}\right] & {R}_{1} & :={R}_{1}-{R}_{3} \\  & ∼\left[\begin{array}{ccc|c}1 & -1 & 0 & 3 \\ 0 & 1 & 0 & -1 \\ 0 & 0 & 1 & -2\end{array}\right] & {R}_{1} & :={R}_{1}+{R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & 0 & 0 & 2 \\ 0 & 1 & 0 & -1 \\ 0 & 0 & 1 & -2\end{array}\right]\end{aligned}
$$

Answer selection: M∼\left[\begin{array}{ccc|c}1 & 0 & 0 & 2 \\ 0 & 1 & 0 & -1 \\ 0 & 0 & 1 & -2\end{array}\right]

Question 17592186097174 — question.difficulty/moderate

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x+y+z &=2 \\ x+2y+z &=0 \\ x+y+2z &=3\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

Solution: The augmented matrix for this system is

$$
M=\left[\begin{array}{ccc|c}1 & 1 & 1 & 2 \\ 1 & 2 & 1 & 0 \\ 1 & 1 & 2 & 3\end{array}\right].
$$

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{ccc|c}1 & 1 & 1 & 2 \\ 1 & 2 & 1 & 0 \\ 1 & 1 & 2 & 3\end{array}\right] & {R}_{2} & :={R}_{2}-{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & 1 & 2 \\ 0 & 1 & 0 & -2 \\ 1 & 1 & 2 & 3\end{array}\right] & {R}_{3} & :={R}_{3}-{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & 1 & 2 \\ 0 & 1 & 0 & -2 \\ 0 & 0 & 1 & 1\end{array}\right] & {R}_{1} & :={R}_{1}-{R}_{3} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & 0 & 1 \\ 0 & 1 & 0 & -2 \\ 0 & 0 & 1 & 1\end{array}\right] & {R}_{1} & :={R}_{1}-{R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & 0 & 0 & 3 \\ 0 & 1 & 0 & -2 \\ 0 & 0 & 1 & 1\end{array}\right].\end{aligned}
$$

The corresponding system is now

$$
\left\{\begin{aligned}x &=3 \\ y &=-2 \\ z &=1.\end{aligned}\right.
$$

So, we have the solution $x=3$, $y=-2$, and $z=1.$ Or, in vector form, $⟨3,-2,1⟩.$

Answer selection: ⟨3,-2,1⟩

Question 17592186241159 — question.difficulty/moderate

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x+z &=2 \\ 2y+z &=0 \\ -x+2y+z &=0\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

Solution: The augmented matrix for this system is

$$
M=\left[\begin{array}{ccc|c}1 & 0 & 1 & 2 \\ 0 & 2 & 1 & 0 \\ -1 & 2 & 1 & 0\end{array}\right].
$$

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{ccc|c}1 & 0 & 1 & 2 \\ 0 & 2 & 1 & 0 \\ -1 & 2 & 1 & 0\end{array}\right] & {R}_{3} & :={R}_{3}+{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 0 & 1 & 2 \\ 0 & 2 & 1 & 0 \\ 0 & 2 & 2 & 2\end{array}\right] & {R}_{2} & :=\frac{1}{2}{R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & 0 & 1 & 2 \\ 0 & 1 & \frac{1}{2} & 0 \\ 0 & 2 & 2 & 2\end{array}\right] & {R}_{3} & :={R}_{3}+(-2){R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & 0 & 1 & 2 \\ 0 & 1 & \frac{1}{2} & 0 \\ 0 & 0 & 1 & 2\end{array}\right] & {R}_{2} & :={R}_{2}+\left(-\frac{1}{2}\right){R}_{3} \\  & ∼\left[\begin{array}{ccc|c}1 & 0 & 1 & 2 \\ 0 & 1 & 0 & -1 \\ 0 & 0 & 1 & 2\end{array}\right] & {R}_{1} & :={R}_{1}+(-1){R}_{3} \\  & ∼\left[\begin{array}{ccc|c}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & -1 \\ 0 & 0 & 1 & 2\end{array}\right].\end{aligned}
$$

The corresponding system is now  

$$
\left\{\begin{aligned}x &=0 \\ y &=-1 \\ z &=2.\end{aligned}\right.
$$

So, we have the solution $x=0$, $y=-1$, and $z=2.$ Or, in vector form $⟨0,-1,2⟩.$

Answer selection: ⟨0,-1,2⟩

### Finding the Reduced Row Echelon Form of a Singular 3x3 System With Two Pivots (43 captured questions)

Question 17592186097353 — question.difficulty/hard

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x-2y+z &=1 \\ 2x-y-z &=-1 \\ -2x+4y-2z &=-2\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form.

Solution: The augmented matrix for this system is

$$
M=\left[\begin{array}{ccc|c}1 & -2 & 1 & 1 \\ 2 & -1 & -1 & -1 \\ -2 & 4 & -2 & -2\end{array}\right].
$$

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{ccc|c}1 & -2 & 1 & 1 \\ 2 & -1 & -1 & -1 \\ -2 & 4 & -2 & -2\end{array}\right] & {R}_{2} & :={R}_{2}-2{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -2 & 1 & 1 \\ 0 & 3 & -3 & -3 \\ -2 & 4 & -2 & -2\end{array}\right] & {R}_{3} & :={R}_{3}+2{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -2 & 1 & 1 \\ 0 & 3 & -3 & -3 \\ 0 & 0 & 0 & 0\end{array}\right] & {R}_{2} & :=\frac{1}{3}{R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & -2 & 1 & 1 \\ 0 & 1 & -1 & -1 \\ 0 & 0 & 0 & 0\end{array}\right].\end{aligned}
$$

In the row echelon form above, we have only two pivots (in the $1$st and $2$nd columns). To transform the matrix to reduced row echelon form, we need to create zeros above the pivots only. This gives,

$$
\begin{aligned}M & ∼\left[\begin{array}{ccc|c}1 & -2 & 1 & 1 \\ 0 & 1 & -1 & -1 \\ 0 & 0 & 0 & 0\end{array}\right] & {R}_{1} & :={R}_{1}+2{R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & 0 & -1 & -1 \\ 0 & 1 & -1 & -1 \\ 0 & 0 & 0 & 0\end{array}\right].\end{aligned}
$$

Answer selection: \left[\begin{array}{ccc|c}1 & 0 & -1 & -1 \\ 0 & 1 & -1 & -1 \\ 0 & 0 & 0 & 0\end{array}\right]

Question 17592186097354 — question.difficulty/hard

Consider the following system of linear equations:

$$
\left\{\begin{aligned}2x-y+z &=1 \\ x-y+z &=-1 \\ 2y-2z &=6\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

Solution: The augmented matrix for this system is

$$
M=\left[\begin{array}{ccc|c}2 & -1 & 1 & 1 \\ 1 & -1 & 1 & -1 \\ 0 & 2 & -2 & 6\end{array}\right].
$$

Transforming $M$ into reduced row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{ccc|c}2 & -1 & 1 & 1 \\ 1 & -1 & 1 & -1 \\ 0 & 2 & -2 & 6\end{array}\right] & {R}_{1} & ↔{R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & -1 & 1 & -1 \\ 2 & -1 & 1 & 1 \\ 0 & 2 & -2 & 6\end{array}\right] & {R}_{2} & :={R}_{2}-2{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -1 & 1 & -1 \\ 0 & 1 & -1 & 3 \\ 0 & 2 & -2 & 6\end{array}\right] & {R}_{3} & :={R}_{3}-2{R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & -1 & 1 & -1 \\ 0 & 1 & -1 & 3 \\ 0 & 0 & 0 & 0\end{array}\right].\end{aligned}
$$

In the row echelon form above, we have only two pivots (in the $1$st and $2$nd columns). To transform the matrix to reduced row echelon form, we need to create zeros above the pivots only. This gives,

$$
\begin{aligned}M & ∼\left[\begin{array}{ccc|c}1 & -1 & 1 & -1 \\ 0 & 1 & -1 & 3 \\ 0 & 0 & 0 & 0\end{array}\right] & {R}_{1} & :={R}_{1}+{R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & 0 & 0 & 2 \\ 0 & 1 & -1 & 3 \\ 0 & 0 & 0 & 0\end{array}\right].\end{aligned}
$$

The corresponding system is now

$$
\left\{\begin{aligned}x &=2 \\ y-z &=3 \\ 0 &=0.\end{aligned}\right.
$$

Since any numbers $x,y,z$ form a solution of the final equation, we can remove this equation from the system. 

The basic variables are the variables whose coefficients are pivots. In this case, the basic variables are $x$ and $y,$ and we have one free variable, $z.$ That means we need to find $x$ and $y$ in terms of $z.$ 

Therefore, the general solution is

$$
\left\{\begin{aligned}x &=2 \\ y &=3+z \\ z &=z,\end{aligned}\right.
$$

where $z$ (the free variable) is an arbitrary number.

In vector form, the solution can be written as

$$
\begin{aligned}\begin{bmatrix}x \\ y \\ z\end{bmatrix}=\begin{bmatrix}2 \\ 3+z \\ z\end{bmatrix},\,z\in (-\infty ,\infty ).\end{aligned}
$$

Answer selection: \begin{bmatrix}2 \\ 3+z \\ z\end{bmatrix},\,z\in (-\infty ,\infty )

Question 17592186266105 — question.difficulty/hard

Consider the following system of linear equations:

$$
\left\{\begin{aligned}-2x-5y+2z &=-7 \\ x+3y-z &=5 \\ x+3y-z &=5\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form.

Solution: The augmented matrix for this system is

$$
M=\left[\begin{array}{ccc|c}-2 & -5 & 2 & -7 \\ 1 & 3 & -1 & 5 \\ 1 & 3 & -1 & 5\end{array}\right].
$$

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{ccc|c}-2 & -5 & 2 & -7 \\ 1 & 3 & -1 & 5 \\ 1 & 3 & -1 & 5\end{array}\right] & {R}_{1} & ↔{R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & 3 & -1 & 5 \\ -2 & -5 & 2 & -7 \\ 1 & 3 & -1 & 5\end{array}\right] & {R}_{2} & :={R}_{2}+2{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 3 & -1 & 5 \\ 0 & 1 & 0 & 3 \\ 1 & 3 & -1 & 5\end{array}\right] & {R}_{3} & :={R}_{3}-{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 3 & -1 & 5 \\ 0 & 1 & 0 & 3 \\ 0 & 0 & 0 & 0\end{array}\right].\end{aligned}
$$

In the row echelon form above, we have only two pivots (in the $1$st and $2$nd columns). To transform the matrix to reduced row echelon form, we need to create zeros above the pivots only. This gives,

$$
\begin{aligned}M & ∼\left[\begin{array}{ccc|c}1 & 3 & -1 & 5 \\ 0 & 1 & 0 & 3 \\ 0 & 0 & 0 & 0\end{array}\right] & {R}_{1} & :={R}_{1}-3{R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & 0 & -1 & -4 \\ 0 & 1 & 0 & 3 \\ 0 & 0 & 0 & 0\end{array}\right].\end{aligned}
$$

Answer selection: \left[\begin{array}{ccc|c}1 & 0 & -1 & -4 \\ 0 & 1 & 0 & 3 \\ 0 & 0 & 0 & 0\end{array}\right]

### Finding the Reduced Row Echelon Form of a Singular 3x3 System With One Pivot (34 captured questions)

Question 17592186097355 — None

Consider the following system of linear equations:
$$
\displaystyle \left\{\begin{aligned}3x - 6y - 3z &=-3 \\ x - 2y - z &=-1 \\ - 6x + 12y + 6z &=6\end{aligned}\right.
$$
Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

Solution: 

Question 17592186097356 — question.difficulty/easy

Consider the following system of linear equations:

$$
\left\{\begin{aligned}-x-y-3z &=1 \\ 2x+2y+6z &=-2 \\ -2x-2y-6z &=2\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form.

Solution: The augmented matrix for this system is

$$
M=\left[\begin{array}{ccc|c}-1 & -1 & -3 & 1 \\ 2 & 2 & 6 & -2 \\ -2 & -2 & -6 & 2\end{array}\right].
$$

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{ccc|c}-1 & -1 & -3 & 1 \\ 2 & 2 & 6 & -2 \\ -2 & -2 & -6 & 2\end{array}\right] & {R}_{1} & :=-{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & 3 & -1 \\ 2 & 2 & 6 & -2 \\ -2 & -2 & -6 & 2\end{array}\right] & {R}_{2} & :={R}_{2}-2{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & 3 & -1 \\ 0 & 0 & 0 & 0 \\ -2 & -2 & -6 & 2\end{array}\right] & {R}_{3} & :={R}_{3}+2{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & 3 & -1 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0\end{array}\right].\end{aligned}
$$

Answer selection: \left[\begin{array}{ccc|c}1 & 1 & 3 & -1 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0\end{array}\right]

Question 17592186266107 — question.difficulty/moderate

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x+y+3z &=7 \\ 5x+5y+15z &=35 \\ -x-y-3z &=-7\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

Solution: The augmented matrix for this system is

$$
M=\left[\begin{array}{ccc|c}1 & 1 & 3 & 7 \\ 5 & 5 & 15 & 35 \\ -1 & -1 & -3 & -7\end{array}\right].
$$

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{ccc|c}1 & 1 & 3 & 7 \\ 5 & 5 & 15 & 35 \\ -1 & -1 & -3 & -7\end{array}\right] & {R}_{2} & :={R}_{2}-5{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & 3 & 7 \\ 0 & 0 & 0 & 0 \\ -1 & -1 & -3 & -7\end{array}\right] & {R}_{3} & :={R}_{3}+{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & 3 & 7 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0\end{array}\right].\end{aligned}
$$

The corresponding system is now

$$
\left\{\begin{aligned}x+y+3z &=7 \\ 0x+0y+0z &=0 \\ 0x+0y+0z &=0.\end{aligned}\right.
$$

Since any numbers $x,y,z$ form a solution of the final two equations, we can remove these equations from the system. 

The basic variables are the variables whose coefficients are pivots. In this case, the basic variable is $x$, and we have two free variables, $y,$ and $z.$ That means we need to find $x$ in terms of $y$ and $z.$ 

Therefore, the general solution is

$$
\left\{\begin{aligned}x &=7-y-3z \\ y &=y \\ z &=z,\end{aligned}\right.
$$

where $y$ and $z$ (the free variables) are arbitrary numbers.

In vector form, the solution can be written as

$$
\begin{aligned}\begin{bmatrix}x \\ y \\ z\end{bmatrix}=\begin{bmatrix}7-y-3z \\ y \\ z\end{bmatrix},\,y,z\in (-\infty ,\infty ).\end{aligned}
$$

Answer selection: \begin{bmatrix}7-y-3z \\ y \\ z\end{bmatrix},\,y,z\in (-\infty ,\infty )
