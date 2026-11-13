# 17592186048853 Solving 2x2 Singular Systems of Equations Using Gaussian Elimination

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186107080 — Introduction

Let's consider a system of linear equations where the corresponding coefficient matrix is singular. For example, consider the following system and its associated augmented matrix:


$$
\left\{\begin{aligned}x-2y &=-5 \\ -3x+6y &=15\end{aligned}\right. \qquad M = \left[ \begin{array}{cc|c}1 & -2 & -5 \\ -3 & 6 & 15\end{array} \right]
$$



To solve the system, we can reduce $M$ to row echelon form using Gaussian elimination, as usual. We have

$$
\begin{aligned}M & ∼\left[\begin{array}{cc|c}1 & -2 & -5 \\ -3 & 6 & 15\end{array}\right] & {R}_{2} & :={R}_{2}+3{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -2 & -5 \\ 0 & 0 & 0\end{array}\right].\end{aligned}
$$

The corresponding system is now


$$
\left\{\begin{aligned}x-2y &=-5 \\ 0x+0y &=0.\end{aligned}\right.
$$



Since any pair of numbers $x,y$ is a solution of the final equation $0x+0y = 0,$ we can remove this equation from the system. So, our system now consists of a single equation

$$
x - 2y = -5.
$$

Finally, we describe the **general solution** of our system.

- The first variable in our equation, $x,$ is called a **basic variable**.

- The second variable in our equation, $y,$ is called a **free variable**.

Solving for the basic variable $(x)$ in terms of the free variable $(y),$ we get $x = -5+2y.$ So the general solution of the system is


$$
\left\{\begin{aligned}x &=-5+2y \\ y &=y\end{aligned}\right.
$$


where the free variable $y$ is any number.

In vector form, this solution is written as

$$
\begin{aligned}\begin{bmatrix}x \\ y\end{bmatrix}=\begin{bmatrix}-5+2y \\ y\end{bmatrix}=\begin{bmatrix}-5 \\ 0\end{bmatrix}+y\begin{bmatrix}2 \\ 1\end{bmatrix},\,y\in (-\infty ,\infty ).\end{aligned}
$$

Notice that this is the equation of a straight line on a plane. Any point on this line satisfies our system of equations.

If we want to find some **particular solution** of the system, we simply choose some particular value of $y$ and find the corresponding value of $x$ on the line. For example, if we choose $y=0,$ then the corresponding value is $x=-5$ and the particular solution is $x=-5,$ $y=0.$



### example 17592186105602 — Reducing an Augmented Matrix for a Singular 2x2 System to REF and Solving the Resulting System

Consider the augmented matrix $M$ given by 


$$
M= \left[\begin{array}{cc|c}1 & -3 & 1 \\ 4 & -12 & 4\end{array}\right].
$$



Use the standard method of Gaussian elimination to reduce $M$ to row echelon form, and then find the general solution of the linear system represented by the matrix.

Reducing $M$ to echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{cc|c}1 & -3 & 1 \\ 4 & -12 & 4\end{array}\right] & {R}_{2} & :={R}_{2}+(-4){R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -3 & 1 \\ 0 & 0 & 0\end{array}\right].\end{aligned}
$$

The corresponding system is now



$$
\left\{\begin{aligned}x-3y &=1 \\ 0x+0y &=0.\end{aligned}\right.
$$



Since any pair of numbers $x,y$ is a solution of the final equation $0x+0y = 0,$ we can remove this equation from the system. So, our system now consists of a single equation

$$
x - 3y = 1.
$$

The first variable $(x)$ is the basic variable, and the second variable $(y)$ is the free variable. Solving for the basic variable $(x)$ in terms of the free variable $(y),$ we get $x=1+3y,$ and the general solution is



$$
\left\{\begin{aligned}x &=1+3y \\ y &=y\end{aligned}\right.
$$



where $y$ is an arbitrary number. 

In vector form, the general solution can be written as

$$
\begin{aligned}\begin{bmatrix}x \\ y\end{bmatrix}=\begin{bmatrix}1+3y \\ y\end{bmatrix}=⟨1+3y,\,y⟩,\,y\in (-\infty ,\infty ).\end{aligned}
$$

### tutorial 17592186107097 — Singular Systems with No Solution

Sometimes, a system of equations might not have any solutions. For example, consider the following augmented matrix:

$$
\begin{aligned}M=\left[\begin{array}{cc|c}1 & -2 & 3 \\ 0 & 0 & 10\end{array}\right]\end{aligned}
$$

The corresponding system is


$$
\left\{\begin{aligned}x-2y &=3 \\ 0x+0y &=10.\end{aligned}\right.
$$



The final equation, $0x+0y=10,$ has no solution. It simplifies to $0=10,$ which is a false statement.

So, there is no pair $x,y$ that satisfies both equations in the system. Consequently, the overall system has no solution.



### example 17592186105603 — Solving a Singular 2x2 System of Equations Using Gaussian Elimination

Consider the system of linear equations


$$
\left\{\begin{aligned}2x+5y &=4 \\ 4x+10y &=0.\end{aligned}\right.
$$


Use the standard method of Gaussian elimination to reduce the augmented matrix $M$ of the system to row echelon form, and then find the general solution of the linear system.

First, we set up the augmented matrix for the system:



$$
M = \left[\begin{array}{cc|c}2 & 5 & 4 \\ 4 & 10 & 0\end{array}\right]
$$



Reducing $M$ to row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{cc|c}2 & 5 & 4 \\ 4 & 10 & 0\end{array}\right] & {R}_{1} & :=\frac{1}{2}{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & \frac{5}{2} & 2 \\ 4 & 10 & 0\end{array}\right] & {R}_{2} & :={R}_{2}+(-4){R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & \frac{5}{2} & 2 \\ 0 & 0 & -8\end{array}\right].\end{aligned}
$$

The corresponding system is now


$$
\left\{\begin{aligned}x+\frac{5}{2}y &=2 \\ 0x+0y &=-8.\end{aligned}\right.
$$



However, the final equation $0x+0y=-8$ has no solution. It simplifies to $0=-8,$ which is a false statement.

So, there is no pair $x,y$ that satisfies both equations in the system. Consequently, the overall system has no solution.

### tutorial 17592186107081 — The Number of Solutions of a 2x2 System

Given a $2 \times 2$ system of linear equations, we have the following possibilities for the number of solutions:

- The system has exactly *one solution* if and only if the respective coefficient matrix is non-singular (meaning that the determinant is not zero). Such systems are called **consistent independent**.

- The system has *infinitely many solutions* if the second row in the standard echelon form contains only $0$'s. These systems are called **consistent dependent**.

- The system has *no solution* if the second row in the standard echelon form contains only $0$'s on the left-hand side and a non-zero element on the right-hand side. These are called **inconsistent** systems.

![](images/16/1692fbea298339ff839cf2f14986d51af45d1ec72b2b7d0de179336bdef40c0e.png)

**Note:** A system of linear equations of the form 


$$
\left\{\begin{aligned}ax+by &=0 \\ cx+dy &=0,\end{aligned}\right.
$$


where we have only $0$'s on the right-hand side, is called **homogeneous**. A homogeneous system always has at least one solution, namely, the solution $x=0$ and $y=0.$ Or, in vector form, $\langle 0,0 \rangle.$



## Representative practice (first three per skill; full bank in practice.json)

### Reducing an Augmented Matrix for a Singular 2x2 System to REF and Solving the Resulting System (29 captured questions)

Question 17592186106312 — question.difficulty/moderate

Consider the augmented matrix $M$ given by 

$$
M=\left[\begin{array}{cc|c}1 & -1 & 3 \\ -3 & 3 & -9\end{array}\right].
$$

Use the standard method of Gaussian elimination to reduce $M$ to row echelon form, and then find the general solution of the linear system represented by the matrix.

Solution: Reducing $M$ to echelon form, we have

$$
\begin{aligned}M & =\left[\begin{array}{cc|c}1 & -1 & 3 \\ -3 & 3 & -9\end{array}\right] & {R}_{2} & :={R}_{2}+3{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -1 & 3 \\ 0 & 0 & 0\end{array}\right].\end{aligned}
$$

The corresponding system is now

$$
\left\{\begin{aligned}x-y &=3 \\ 0x+0y &=0.\end{aligned}\right.
$$

Since any pair of numbers $x,y$ is a solution of the final equation $0x+0y=0,$ we can remove this equation from the system. So, our system now consists of a single equation

$$
x-y=3.
$$

The first variable $(x)$ is the basic variable, and the second variable $(y)$ is the free variable. Solving for the basic variable $(x)$ in terms of the free variable $(y),$ we get $x=3+y,$ and the general solution is

$$
\left\{\begin{aligned}x &=3+y \\ y &=y\end{aligned}\right.
$$

where $y$ is an arbitrary number. 

In vector form, the general solution can be written as

$$
\begin{aligned}\begin{bmatrix}x \\ y\end{bmatrix}=\begin{bmatrix}3+y \\ y\end{bmatrix},\,y\in (-\infty ,\infty ).\end{aligned}
$$

Answer selection: \begin{bmatrix}x \\ y\end{bmatrix}=\begin{bmatrix}3+y \\ y\end{bmatrix},\,y\in (-\infty ,\infty )

Question 17592186106313 — question.difficulty/easy

Consider the augmented matrix $M$ given by 

$$
M=\left[\begin{array}{cc|c}1 & -2 & 1 \\ 0 & 0 & 0\end{array}\right].
$$

Find the general solution of the linear system represented by the matrix.

Solution: The system corresponding to $M$ is 

$$
\left\{\begin{aligned}x-2y &=1 \\ 0x+0y &=0.\end{aligned}\right.
$$

Since any pair of numbers $x,y$ is a solution of the final equation $0x+0y=0,$ we can remove this equation from the system. So, our system now consists of a single equation

$$
x-2y=1.
$$

The first variable $(x)$ is the basic variable, and the second variable $(y)$ is the free variable. Solving for the basic variable $(x)$ in terms of the free variable $(y),$ we get $x=1+2y,$ and the general solution is

$$
\left\{\begin{aligned}x &=1+2y \\ y &=y\end{aligned}\right.
$$

where $y$ is an arbitrary number. 

In vector form, the general solution can be written as

$$
\begin{aligned}\begin{bmatrix}x \\ y\end{bmatrix}=\begin{bmatrix}1+2y \\ y\end{bmatrix}=⟨1+2y,\,y⟩,\,y\in (-\infty ,\infty ).\end{aligned}
$$

Answer selection: ⟨1+2y,\,y⟩,\,y\in (-\infty ,\infty )

Question 17592186266011 — question.difficulty/moderate

Consider the augmented matrix $M$ given by 

$$
M=\left[\begin{array}{cc|c}3 & 9 & -3 \\ 2 & 6 & -2\end{array}\right].
$$

Use the standard method of Gaussian elimination to reduce $M$ to row echelon form, and then find the general solution of the linear system represented by the matrix.

Solution: Reducing $M$ to echelon form, we have

$$
\begin{aligned}M & =\left[\begin{array}{cc|c}3 & 9 & -3 \\ 2 & 6 & -2\end{array}\right] & {R}_{1} & :=\frac{1}{3}{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & 3 & -1 \\ 2 & 6 & -2\end{array}\right] & {R}_{2} & :={R}_{2}+(-2){R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & 3 & -1 \\ 0 & 0 & 0\end{array}\right].\end{aligned}
$$

The corresponding system is now

$$
\left\{\begin{aligned}x+3y &=-1 \\ 0x+0y &=0.\end{aligned}\right.
$$

Since any pair of numbers $x,y$ is a solution of the final equation $0x+0y=0,$ we can remove this equation from the system. So, our system now consists of a single equation

$$
x+3y=-1.
$$

The first variable $(x)$ is the basic variable, and the second variable $(y)$ is the free variable. Solving for the basic variable $(x)$ in terms of the free variable $(y),$ we get $x=-3y-1,$ and the general solution is

$$
\left\{\begin{aligned}x &=-3y-1 \\ y &=y\end{aligned}\right.
$$

where $y$ is an arbitrary number. 

In vector form, the general solution can be written as

$$
\begin{aligned}\begin{bmatrix}x \\ y\end{bmatrix}=\begin{bmatrix}-3y-1 \\ y\end{bmatrix},\,y\in (-\infty ,\infty ).\end{aligned}
$$

Answer selection: \begin{aligned}\begin{bmatrix}x \\ y\end{bmatrix}=\begin{bmatrix}-3y-1 \\ y\end{bmatrix},\,y\in (-\infty ,\infty )\end{aligned}

### Solving a Singular 2x2 System of Equations Using Gaussian Elimination (30 captured questions)

Question 17592186106314 — question.difficulty/easy

Consider the system of linear equations

$$
\left\{\begin{aligned}x-6y &=2 \\ -4x+24y &=-10.\end{aligned}\right.
$$

Use the standard method of Gaussian elimination to reduce the augmented matrix $M$ of the system to row echelon form, and then find the general solution of the linear system.

Solution: First, we set up the augmented matrix for the system:

$$
M=\left[\begin{array}{cc|c}1 & -6 & 2 \\ -4 & 24 & -10\end{array}\right]
$$

Reducing $M$ to row echelon form, we have

$$
\begin{aligned}M & =\left[\begin{array}{cc|c}1 & -6 & 2 \\ -4 & 24 & -10\end{array}\right] & {R}_{2} & :={R}_{2}+4{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -6 & 2 \\ 0 & 0 & -2\end{array}\right].\end{aligned}
$$

The corresponding system is now

$$
\left\{\begin{aligned}x-6y &=2 \\ 0x+0y &=-2.\end{aligned}\right.
$$

However, the final equation $0x+0y=-2$ has no solution. It simplifies to $0=-2,$ which is a false statement.

So, there is no pair $x,y$ that satisfies both equations in the system. Consequently, the overall system has no solution.

Answer selection: No solution

Question 17592186106316 — question.difficulty/moderate

Consider the system of linear equations

$$
\left\{\begin{aligned}7x+14y &=21 \\ 3x+6y &=9.\end{aligned}\right.
$$

Use the standard method of Gaussian elimination to reduce the augmented matrix $M$ of the system to row echelon form, and then find the general solution of the linear system.

Solution: First, we set up the augmented matrix for the system:

$$
M=\left[\begin{array}{cc|c}7 & 14 & 21 \\ 3 & 6 & 9\end{array}\right]
$$

Reducing $M$ to row echelon form, we have

$$
\begin{aligned}M & =\left[\begin{array}{cc|c}7 & 14 & 21 \\ 3 & 6 & 9\end{array}\right] & {R}_{1} & :=\frac{1}{7}{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & 2 & 3 \\ 3 & 6 & 9\end{array}\right] & {R}_{2} & :={R}_{2}-3{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & 2 & 3 \\ 0 & 0 & 0\end{array}\right].\end{aligned}
$$

The corresponding system is now

$$
\left\{\begin{aligned}x+2y &=3 \\ 0x+0y &=0.\end{aligned}\right.
$$

Since any pair of numbers $x,y$ is a solution of the final equation $0x+0y=0,$ we can remove this equation from the system. So, our system now consists of a single equation

$$
x+2y=3.
$$

The first variable $(x)$ is the basic variable, and the second variable $(y)$ is the free variable. Solving for the basic variable $(x)$ in terms of the free variable $(y),$ we get $x=3-2y,$ and the general solution is

$$
\left\{\begin{aligned}x &=3-2y \\ y &=y\end{aligned}\right.
$$

where $y$ is an arbitrary number. 

In vector form, the general solution can be written as

$$
\begin{aligned}\begin{bmatrix}x \\ y\end{bmatrix}=\begin{bmatrix}3-2y \\ y\end{bmatrix},\,y\in (-\infty ,\infty ).\end{aligned}
$$

Answer selection: \begin{bmatrix}x \\ y\end{bmatrix}=\begin{bmatrix}3-2y \\ y\end{bmatrix},\,y\in (-\infty ,\infty )

Question 17592186266012 — question.difficulty/easy

Consider the system of linear equations

$$
\left\{\begin{aligned}x-2y &=-1 \\ -4x+8y &=7.\end{aligned}\right.
$$

Use the standard method of Gaussian elimination to reduce the augmented matrix $M$ of the system to row echelon form, and then find the general solution of the linear system.

Solution: First, we set up the augmented matrix for the system:

$$
M=\left[\begin{array}{cc|c}1 & -2 & -1 \\ -4 & 8 & 7\end{array}\right]
$$

Reducing $M$ to row echelon form, we have

$$
\begin{aligned}M & =\left[\begin{array}{cc|c}1 & -2 & -1 \\ -4 & 8 & 7\end{array}\right] & {R}_{2} & :={R}_{2}+4{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -2 & -1 \\ 0 & 0 & 3\end{array}\right].\end{aligned}
$$

The corresponding system is now

$$
\left\{\begin{aligned}x-2y &=-1 \\ 0x+0y &=3.\end{aligned}\right.
$$

However, the final equation $0x+0y=3$ has no solution. It simplifies to $0=3,$ which is a false statement.

So, there is no pair $x,y$ that satisfies both equations in the system. Consequently, the overall system has no solution.

Answer selection: No solution
