# 17592186050178 Solving 3x3 Singular Systems of Equations Using Gaussian Elimination

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186107082 — Introduction

Let's consider a system of linear equations where the corresponding coefficient matrix is singular. For example, consider the following system and its associated augmented matrix:


$$
\left\{\begin{aligned}x-y+z &=2 \\ 2x-y-z &=-1 \\ 2y-6z &=-10\end{aligned}\right. \qquad M = \left[ \begin{array}{ccc|c}1 & -1 & 1 & 2 \\ 2 & -1 & -1 & -1 \\ 0 & 2 & -6 & -10\end{array} \right]
$$



To solve the system, we can reduce $M$ to row echelon form using Gaussian elimination, as usual. We have

$$
\begin{aligned}M & ∼\left[\begin{array}{ccc|c}1 & -1 & 1 & 2 \\ 2 & -1 & -1 & -1 \\ 0 & 2 & -6 & -10\end{array}\right] & {R}_{2} & :={R}_{2}+(-2){R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -1 & 1 & 2 \\ 0 & 1 & -3 & -5 \\ 0 & 2 & -6 & -10\end{array}\right] & {R}_{3} & :={R}_{3}+(-2){R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & -1 & 1 & 2 \\ 0 & 1 & -3 & -5 \\ 0 & 0 & 0 & 0\end{array}\right].\end{aligned}
$$

The corresponding system is now


$$
\left\{\begin{aligned}x-y+z &=2 \\ 0x+y-3z &=-5 \\ 0x+0y+0z &=0.\end{aligned}\right.
$$



Since any numbers $x,y,z$ form a solution of the final equation $0x+0y+0z = 0,$ we can remove this equation from the system. So, our system now consists of just two equations:



$$
\left\{\begin{aligned}x-y+z &=2 \\ y-3z &=-5\end{aligned}\right.
$$



The **basic variables** are the variables of our system whose coefficients are the pivots of the row echelon form matrix. Let's illustrate the pivots of $M\mathbin{:}$



$$
M= \left[ \begin{array}{ccc|c}\bbox[lightgray, 2pt]{1} & -1 & 1 & 2 \\ 0 & \bbox[lightgray, 2pt]{1} & -3 & -5 \\ 0 & 0 & 0 & 0\end{array}\right]
$$



The pivots are

- $m_{11}=1,$ which is the coefficient of $x,$ and

- $m_{22}=1,$ which is the coefficient of $y.$

Therefore, the basic variables are $x$ and $y.$

The remaining variables are called the **free variables**. We have only one free variable in our system, which is $z$.

Finally, we can describe the **general solution** by finding equations for the basic variables in terms of the free variables. In our case, this means we need to find $x$ and $y$ in terms of $z$.

To do this, we apply the back substitution. From the second equation, we obtain

$$
y - 3z = -5
	\qquad\Longrightarrow\qquad
	y = -5+3z.
$$

Substituting this into the first equation, we get

$$
\begin{aligned}x-(-5+3z)+z=2\,⟹\, & x=-3+2z.\end{aligned}
$$

Therefore, the general solution is


$$
\left\{\begin{aligned}x &=-3+2z \\ y &=-5+3z \\ z &=z\end{aligned}\right.
$$


where $z$ (the free variable) is an arbitrary number.

In vector form, the solution can be written as


$$
\begin{bmatrix}x \\ y \\ z\end{bmatrix}= \begin{bmatrix}-3+2z \\ -5+3z \\ z\end{bmatrix}= \begin{bmatrix}-3 \\ -5 \\ 0\end{bmatrix}+z \begin{bmatrix}2 \\ 3 \\ 1\end{bmatrix}, \qquad z\in(-\infty,\infty).
$$



Geometrically, this is the vector equation of a line, and any point on the line is a solution to our original system.

If we want to find some **particular solution** of the system, we simply choose some particular value of $z$ and find the corresponding values of $x$ and $y$ on the line. For example, if we choose $z=0,$ then the corresponding values are $x=-3$ and $y=-5$ and the particular solution is $x=-3,$ $y=-5,$ $z=0.$



### example 17592186105604 — Finding the General Solution of a Singular 3x3 System of Equations with Two Pivots

Consider the augmented matrix $M$ given by 


$$
M= \left[\begin{array}{ccc|c}1 & 1 & 3 & 1 \\ 1 & 1 & 1 & -1 \\ 1 & 1 & 5 & 3\end{array}\right].
$$



Use the standard method of Gaussian elimination to reduce $M$ to row echelon form, and then find the general solution of the linear system represented by the matrix.

Reducing $M$ to echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{ccc|c}1 & 1 & 3 & 1 \\ 1 & 1 & 1 & -1 \\ 1 & 1 & 5 & 3\end{array}\right] & {R}_{2} & :={R}_{2}+(-1){R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & 3 & 1 \\ 0 & 0 & -2 & -2 \\ 1 & 1 & 5 & 3\end{array}\right] & {R}_{3} & :={R}_{3}+(-1){R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & 3 & 1 \\ 0 & 0 & -2 & -2 \\ 0 & 0 & 2 & 2\end{array}\right] & {R}_{3} & :={R}_{3}+{R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & 3 & 1 \\ 0 & 0 & -2 & -2 \\ 0 & 0 & 0 & 0\end{array}\right] & {R}_{2} & :=-\frac{1}{2}{R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & 3 & 1 \\ 0 & 0 & 1 & 1 \\ 0 & 0 & 0 & 0\end{array}\right].\end{aligned}
$$

The corresponding system is now


$$
\left\{\begin{aligned}x+y+3z &=1 \\ 0x+0y+z &=1 \\ 0x+0y+0z &=0.\end{aligned}\right.
$$



Since any numbers $x,y,z$ form a solution of the final equation $0x+0y+0z = 0,$ we can remove this equation from the system. So, our system now consists of just two equations:



$$
\left\{\begin{aligned}x+y+3z &=1 \\ z &=1\end{aligned}\right.
$$



The basic variables are the variables whose coefficients are pivots. In this case, the basic variables are $x$ and $z,$ and we have one free variable, $y.$ That means we need to find $x$ and $z$ in terms of $y.$ To do this, we apply the back substitution. 

Starting with the second equation $z=1,$ we substitute into the first equation and get

$$
\begin{aligned}x+y+3(1) &=1\,⇒\,x=-2-y.\end{aligned}
$$

Therefore, the general solution is


$$
\left\{\begin{aligned}x &=-2-y \\ y &=y \\ z &=1,\end{aligned}\right.
$$


where $y$ (the free variable) is an arbitrary number.

In vector form, the solution can be written as

$$
\begin{aligned}\begin{bmatrix}x \\ y \\ z\end{bmatrix}=\begin{bmatrix}-2-y \\ y \\ 1\end{bmatrix}=\begin{bmatrix}-2 \\ 0 \\ 1\end{bmatrix}+y\begin{bmatrix}-1 \\ 1 \\ 0\end{bmatrix},\,y\in (-\infty ,\infty ).\end{aligned}
$$

### example 17592186105605 — Finding the General Solution of a Singular 3x3 System of Equations with One Pivot

Consider the augmented matrix $M$ given by 


$$
M= \left[\begin{array}{ccc|c}1 & 1 & 3 & 1 \\ -2 & -2 & -6 & -2 \\ 3 & 3 & 9 & 3\end{array}\right].
$$



Use the standard method of Gaussian elimination to reduce $M$ to row echelon form, and then find the general solution of the linear system represented by the matrix.

Reducing $M$ to echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{ccc|c}1 & 1 & 3 & 1 \\ -2 & -2 & -6 & -2 \\ 3 & 3 & 9 & 3\end{array}\right] & {R}_{2} & :={R}_{2}+2{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & 3 & 1 \\ 0 & 0 & 0 & 0 \\ 3 & 3 & 9 & 3\end{array}\right] & {R}_{3} & :={R}_{3}+(-3){R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & 3 & 1 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0\end{array}\right].\end{aligned}
$$

The corresponding system is now


$$
\left\{\begin{aligned}x+y+3z &=1 \\ 0x+0y+0z &=0 \\ 0x+0y+0z &=0.\end{aligned}\right.
$$



Since any numbers $x,y,z$ form a solution of the final two equations $0x+0y+0z = 0,$ we can remove these equations from the system. So, our system now consists of just a single equation:

$$
x + y + 3z = 1
$$

The basic variable is $x$, and we have two free variables $y$ and $z$. That means we need to find $x$ in terms of $y,z.$ Doing this, we get

$$
x = 1-y-3z.
$$

Therefore, the general solution is


$$
\left\{\begin{aligned}x &=1-y-3z \\ y &=y \\ z &=z\end{aligned}\right.
$$



where $y,z$ (the free variables) are arbitrary numbers.

In vector form, the solution can be written as

$$
\begin{aligned}\begin{bmatrix}x \\ y \\ z\end{bmatrix}=\begin{bmatrix}1-y-3z \\ y \\ z\end{bmatrix}=\begin{bmatrix}1 \\ 0 \\ 0\end{bmatrix}+y\begin{bmatrix}-1 \\ 1 \\ 0\end{bmatrix}+z\begin{bmatrix}-3 \\ 0 \\ 1\end{bmatrix},\,y,z\in (-\infty ,\infty ).\end{aligned}
$$

Geometrically, this is the equation of a plane in $\mathbb R^3$, and any point on the plane is a solution to the system.

### example 17592186105645 — Identifying a Singular 3x3 System of Equations That Has No Solution

Consider the augmented matrix $M$ given by 


$$
M= \left[\begin{array}{ccc|c}1 & -2 & -6 & 7 \\ 1 & 1 & 0 & 19 \\ 1 & -3 & -8 & 6\end{array}\right].
$$


Use the standard method of Gaussian elimination to reduce $M$ to row echelon form, and then find the general solution of the linear system represented by the matrix.

Reducing $M$ to echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{ccc|c}1 & -2 & -6 & 7 \\ 1 & 1 & 0 & 19 \\ 1 & -3 & -8 & 6\end{array}\right] & {R}_{2} & :={R}_{2}-{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -2 & -6 & 7 \\ 0 & 3 & 6 & 12 \\ 1 & -3 & -8 & 6\end{array}\right] & {R}_{3} & :={R}_{3}-{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -2 & -6 & 7 \\ 0 & 3 & 6 & 12 \\ 0 & -1 & -2 & -1\end{array}\right] & {R}_{2} & :=\frac{1}{3}{R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & -2 & -6 & 7 \\ 0 & 1 & 2 & 4 \\ 0 & -1 & -2 & -1\end{array}\right] & {R}_{3} & :={R}_{3}+{R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & -2 & -6 & 7 \\ 0 & 1 & 2 & 4 \\ 0 & 0 & 0 & 3\end{array}\right].\end{aligned}
$$

The corresponding system is now

$$
\left\{\begin{aligned}x-2y-6z &=7 \\ 0x+y+2z &=4 \\ 0x+0y+0z &=3\end{aligned}\right.
$$

Since there are no such numbers $x,y,z$ that form a solution of the final equation $0x+0y+0z = 3,$ we can conclude that our system has no solution.

## Representative practice (first three per skill; full bank in practice.json)

### Finding the General Solution of a Singular 3x3 System of Equations with Two Pivots (23 captured questions)

Question 17592186106150 — question.difficulty/easy

Consider the augmented matrix $M$ given by 

$$
M=\left[\begin{array}{ccc|c}1 & 0 & -1 & 1 \\ 0 & 1 & 3 & 2 \\ 0 & 0 & 0 & 0\end{array}\right].
$$

Find the general solution of the linear system represented by the matrix.

Solution: Notice that the matrix $M$ is already in row echelon form. The system corresponding to $M$ is 

$$
\left\{\begin{aligned}x+0y-z &=1 \\ 0x+y+3z &=2 \\ 0x+0y+0z &=0.\end{aligned}\right.
$$

Since any numbers $x,y,z$ form a solution of the final equation $0x+0y+0z=0,$ we can remove this equation from the system. So, our system now consists of just two equations:

$$
\left\{\begin{aligned}x-z &=1 \\ y+3z &=2\end{aligned}\right.
$$

The basic variables are the variables whose coefficients are pivots. In this case, the basic variables are $x$ and $y,$ and we have one free variable, $z.$ That means we need to find $x$ and $y$ in terms of $z.$ To do this, we apply the back substitution. 

From the second equation, we get

$$
y+3z=2\,⇒\,y=2-3z
$$

and from the first equation, we obtain

$$
x-z=1\,⇒\,x=1+z.
$$

Therefore, the general solution is

$$
\left\{\begin{aligned}x &=1+z \\ y &=2-3z \\ z &=z,\end{aligned}\right.
$$

where $z$ (the free variable) is an arbitrary number.

In vector form, the solution can be written as

$$
\begin{aligned}\begin{bmatrix}x \\ y \\ z\end{bmatrix}=\begin{bmatrix}1+z \\ 2-3z \\ z\end{bmatrix},\,z\in (-\infty ,\infty ).\end{aligned}
$$

Answer selection: \begin{bmatrix}1+z \\ 2-3z \\ z\end{bmatrix},\,z\in (-\infty ,\infty )

Question 17592186106290 — None

Consider the system
$$
\displaystyle \left\{\begin{aligned}-x_{1} + 2x_{3} &=2 \\ x_{2} - 3x_{3} &=1 \\ 2x_{1} - 4x_{3} &=-4\end{aligned}\right.
$$.
Use the standard method of Gaussian elimination to reduce the augmented matrix $M$ of the system to row echelon form.

Solution: The augmented matrix is

$$
M=\left[\begin{array}{ccc|c}-1&0&2&2\\0&1&-3&1\\2&0&-4&-4\end{array}\right].
$$

Apply $R_1:=-R_1$ and then $R_3:=R_3-2R_1$. This gives the row echelon form

$$
M\sim\left[\begin{array}{ccc|c}1&0&-2&-2\\0&1&-3&1\\0&0&0&0\end{array}\right].
$$

Answer selection: M ∼ \left[ \begin{array}{ccc|c}1 & 0 & - 2 & - 2 \\ 0 & 1 & - 3 & 1 \\ 0 & 0 & 0 & 0\end{array} \right]

Question 17592186266092 — question.difficulty/easy

Consider the augmented matrix $M$ given by 

$$
M=\left[\begin{array}{ccc|c}1 & 7 & -8 & 0 \\ 0 & 1 & -1 & -7 \\ 0 & 0 & 0 & 0\end{array}\right].
$$

Find the general solution of the linear system represented by the matrix.

Solution: Notice that the matrix $M$ is already in row echelon form. The system corresponding to $M$ is 

$$
\left\{\begin{aligned}x+7y-8z &=0 \\ 0x+y-z &=-7 \\ 0x+0y+0z &=0.\end{aligned}\right.
$$

Since any numbers $x,y,z$ form a solution of the final equation $0x+0y+0z=0,$ we can remove this equation from the system. So, our system now consists of just two equations:

$$
\left\{\begin{aligned}x+7y-8z &=0 \\ y-z &=-7\end{aligned}\right.
$$

The basic variables are the variables whose coefficients are pivots. In this case, the basic variables are $x$ and $y,$ and we have one free variable, $z.$ That means we need to find $x$ and $y$ in terms of $z.$ To do this, we apply the back substitution. 

From the second equation, we get

$$
y-z=-7\,⇒\,y=z-7
$$

and from the first equation, we obtain

$$
x+7(z-7)-8z=0\,⇒\,x=z+49.
$$

Therefore, the general solution is

$$
\left\{\begin{aligned}x &=z+49 \\ y &=z-7 \\ z &=z,\end{aligned}\right.
$$

where $z$ (the free variable) is an arbitrary number.

In vector form, the solution can be written as

$$
\begin{aligned}\begin{bmatrix}x \\ y \\ z\end{bmatrix}=\begin{bmatrix}z+49 \\ z-7 \\ z\end{bmatrix},\,z\in (-\infty ,\infty ).\end{aligned}
$$

Answer selection: \begin{bmatrix}z+49 \\ z-7 \\ z\end{bmatrix},\,z\in (-\infty ,\infty )

### Finding the General Solution of a Singular 3x3 System of Equations with One Pivot (31 captured questions)

Question 17592186106149 — question.difficulty/easy

Consider the augmented matrix $M$ given by 

$$
M=\left[\begin{array}{ccc|c}1 & -1 & 4 & -1 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0\end{array}\right].
$$

Find the general solution of the linear system represented by the matrix.

Solution: The system corresponding to $M$ is

$$
\left\{\begin{aligned}x-y+4z &=-1 \\ 0x+0y+0z &=0 \\ 0x+0y+0z &=0.\end{aligned}\right.
$$

Since any numbers $x,y,z$ form a solution of the final two equations $0x+0y+0z=0,$ we can remove these equations from the system. So, our system now consists of just a single equation:

$$
x-y+4z=-1
$$

The basic variables are the variables whose coefficients are pivots. In this case, the basic variable is $x$, and we have two free variables $y$ and $z.$ That means we need to find $x$ in terms of $y,z.$ Doing this, we get

$$
x=-1+y-4z.
$$

Therefore, the general solution is

$$
\left\{\begin{aligned}x &=-1+y-4z \\ y &=y \\ z &=z,\end{aligned}\right.
$$

where $y$, $z$ (free variables) are arbitrary numbers.

In vector form, the solution can be written as

$$
\begin{aligned}\begin{bmatrix}x \\ y \\ z\end{bmatrix}=\begin{bmatrix}-1+y-4z \\ y \\ z\end{bmatrix}=\begin{bmatrix}-1 \\ 0 \\ 0\end{bmatrix}+y\begin{bmatrix}1 \\ 1 \\ 0\end{bmatrix}+z\begin{bmatrix}-4 \\ 0 \\ 1\end{bmatrix},\,y,z\in (-\infty ,\infty ).\end{aligned}
$$

Answer selection: \begin{bmatrix}-1 \\ 0 \\ 0\end{bmatrix}+y\begin{bmatrix}1 \\ 1 \\ 0\end{bmatrix}+z\begin{bmatrix}-4 \\ 0 \\ 1\end{bmatrix},\,y,z\in (-\infty ,\infty )

Question 17592186106484 — question.difficulty/moderate

Consider the augmented matrix $M$ given by 

$$
M=\left[\begin{array}{ccc|c}1 & 3 & -2 & 4 \\ 4 & 12 & -8 & 16 \\ -2 & -6 & 4 & -8\end{array}\right].
$$

Use the standard method of Gaussian elimination to reduce $M$ to row echelon form, and then find the general solution of the linear system represented by the matrix.

Solution: Reducing $M$ to echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{ccc|c}1 & 3 & -2 & 4 \\ 4 & 12 & -8 & 16 \\ -2 & -6 & 4 & -8\end{array}\right] & {R}_{2} & :={R}_{2}+(-4){R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 3 & -2 & 4 \\ 0 & 0 & 0 & 0 \\ -2 & -6 & 4 & -8\end{array}\right] & {R}_{3} & :={R}_{3}+2{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 3 & -2 & 4 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0\end{array}\right].\end{aligned}
$$

The corresponding system is now

$$
\left\{\begin{aligned}x+3y-2z &=4 \\ 0x+0y+0z &=0 \\ 0x+0y+0z &=0.\end{aligned}\right.
$$

Since any numbers $x,y,z$ form a solution of the final two equations $0x+0y+0z=0,$ we can remove these equations from the system. So, our system now consists of just a single equation:

$$
x+3y-2z=4
$$

The basic variables are the variables whose coefficients are pivots. In this case, the basic variable is $x$, and we have two free variables $y$ and $z.$ That means we need to find $x$ in terms of $y,z.$ Doing this, we get

$$
x=4-3y+2z.
$$

Therefore, the general solution is

$$
\left\{\begin{aligned}x &=4-3y+2z \\ y &=y \\ z &=z\end{aligned}\right.
$$

where $y,z$ (the free variables) are arbitrary numbers.

In vector form, the solution can be written as

$$
\begin{aligned}\begin{bmatrix}x \\ y \\ z\end{bmatrix}=\begin{bmatrix}4-3y+2z \\ y \\ z\end{bmatrix},\,y,z\in (-\infty ,\infty ).\end{aligned}
$$

Answer selection: \begin{bmatrix}4-3y+2z \\ y \\ z\end{bmatrix},\,y,z\in (-\infty ,\infty )

Question 17592186266094 — question.difficulty/easy

Consider the augmented matrix $M$ given by 

$$
M=\left[\begin{array}{ccc|c}1 & 9 & 2 & 8 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0\end{array}\right].
$$

Find the general solution of the linear system represented by the matrix.

Solution: The system corresponding to $M$ is

$$
\left\{\begin{aligned}x+9y+2z &=8 \\ 0x+0y+0z &=0 \\ 0x+0y+0z &=0.\end{aligned}\right.
$$

Since any numbers $x,y,z$ form a solution of the final two equations $0x+0y+0z=0,$ we can remove these equations from the system. So, our system now consists of just a single equation:

$$
x+9y+2z=8
$$

The basic variables are the variables whose coefficients are pivots. In this case, the basic variable is $x$, and we have two free variables $y$ and $z.$ That means we need to find $x$ in terms of $y,z.$ Doing this, we get

$$
x=8-9y-2z.
$$

Therefore, the general solution is

$$
\left\{\begin{aligned}x &=8-9y-2z \\ y &=y \\ z &=z,\end{aligned}\right.
$$

where $y$, $z$ (free variables) are arbitrary numbers.

In vector form, the solution can be written as

$$
\begin{aligned}\begin{bmatrix}x \\ y \\ z\end{bmatrix}=\begin{bmatrix}8-9y-2z \\ y \\ z\end{bmatrix}=\begin{bmatrix}8 \\ 0 \\ 0\end{bmatrix}+y\begin{bmatrix}-9 \\ 1 \\ 0\end{bmatrix}+z\begin{bmatrix}-2 \\ 0 \\ 1\end{bmatrix},\,y,z\in (-\infty ,\infty ).\end{aligned}
$$

Answer selection: \begin{bmatrix}8 \\ 0 \\ 0\end{bmatrix}+y\begin{bmatrix}-9 \\ 1 \\ 0\end{bmatrix}+z\begin{bmatrix}-2 \\ 0 \\ 1\end{bmatrix},\,y,z\in (-\infty ,\infty )

### Identifying a Singular 3x3 System of Equations That Has No Solution (25 captured questions)

Question 17592186106026 — question.difficulty/moderate

Consider the augmented matrix $M$ given by 

$$
M=\left[\begin{array}{ccc|c}1 & -2 & -6 & 12 \\ 2 & 4 & 12 & -16 \\ 1 & -4 & -12 & 21\end{array}\right].
$$

Use the standard method of Gaussian elimination to reduce $M$ to row echelon form, and then find the general solution of the linear system represented by the matrix.

Solution: Reducing $M$ to echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{ccc|c}1 & -2 & -6 & 12 \\ 2 & 4 & 12 & -16 \\ 1 & -4 & -12 & 21\end{array}\right] & {R}_{2} & :={R}_{2}-2{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -2 & -6 & 12 \\ 0 & 8 & 24 & -40 \\ 1 & -4 & -12 & 21\end{array}\right] & {R}_{3} & :={R}_{3}-{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -2 & -6 & 12 \\ 0 & 8 & 24 & -40 \\ 0 & -2 & -6 & 9\end{array}\right] & {R}_{2} & :=\frac{1}{8}{R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & -2 & -6 & 12 \\ 0 & 1 & 3 & -5 \\ 0 & -2 & -6 & 9\end{array}\right] & {R}_{3} & :={R}_{3}+2{R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & -2 & -6 & 12 \\ 0 & 1 & 3 & -5 \\ 0 & 0 & 0 & -1\end{array}\right].\end{aligned}
$$

The corresponding system is now

$$
\left\{\begin{aligned}x-2y-6z &=12 \\ 0x+y+3z &=-5 \\ 0x+0y+0z &=-1\end{aligned}\right.
$$

Since there are no such numbers $x,y,z$ that form a solution of the final equation $0x+0y+0z=-1,$ we can conclude that our system has no solution.

Answer selection: No solution

Question 17592186106027 — question.difficulty/moderate

Consider the system

$$
\left\{\begin{aligned}2x+6y+8z &=12 \\ y-z &=-1 \\ 4x+4y+24z &=7.\end{aligned}\right.
$$

Use the standard method of Gaussian elimination to reduce the augmented matrix $M$ of the system to row echelon form.

Solution: The augmented matrix for the system is

$$
M=\left[\begin{array}{ccc|c}2 & 6 & 8 & 12 \\ 0 & 1 & -1 & -1 \\ 4 & 4 & 24 & 7\end{array}\right].
$$

Reducing $M$ to echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{ccc|c}2 & 6 & 8 & 12 \\ 0 & 1 & -1 & -1 \\ 4 & 4 & 24 & 7\end{array}\right] & {R}_{1} & :=\frac{1}{2}{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 3 & 4 & 6 \\ 0 & 1 & -1 & -1 \\ 4 & 4 & 24 & 7\end{array}\right] & {R}_{3} & :={R}_{3}-4{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 3 & 4 & 6 \\ 0 & 1 & -1 & -1 \\ 0 & -8 & 8 & -17\end{array}\right] & {R}_{3} & :={R}_{3}+8{R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & 3 & 4 & 6 \\ 0 & 1 & -1 & -1 \\ 0 & 0 & 0 & -25\end{array}\right].\end{aligned}
$$

Answer selection: M∼\left[\begin{array}{ccc|c}1 & 3 & 4 & 6 \\ 0 & 1 & -1 & -1 \\ 0 & 0 & 0 & -25\end{array}\right]

Question 17592186266096 — question.difficulty/easy

Consider the augmented matrix $M$ given by 

$$
M=\left[\begin{array}{ccc|c}-1 & 6 & -7 & 4 \\ 0 & 3 & 0 & 9 \\ 0 & 0 & 0 & -8\end{array}\right].
$$

Find the general solution of the linear system represented by the matrix.

Solution: The system corresponding to $M$ is

$$
\left\{\begin{aligned}-x+6y-7z &=4 \\ 0x+3y+0z &=9 \\ 0x+0y+0z &=-8\end{aligned}\right.
$$

Since there are no such numbers $x,y,z$ that form a solution of the final equation $0x+0y+0z=-8,$ we can conclude that our system has no solution.

Answer selection: No solution
