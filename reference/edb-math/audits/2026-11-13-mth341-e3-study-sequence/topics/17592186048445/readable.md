# 17592186048445 Gaussian Elimination For NxM Systems of Equations

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186116493 — Introduction

We can use Gaussian elimination to find the general solutions of systems with any number of equations and variables. For instance, consider the system of linear equations

$$
\left\{\begin{aligned}x-y+z &=1, \\ y+3z &=0.\end{aligned}\right.
$$

This system has the augmented matrix


$$
M=\left[\begin{array}{ccc|c}1 & -1 & 1 & 1 \\ 0 & 1 & 3 & 0\end{array}\right].
$$



Using the standard Gauss-Jordan method, we can reduce this matrix to reduced row echelon form as follows:

$$
\begin{aligned}M & =\left[\begin{array}{ccc|c}1 & -1 & 1 & 1 \\ 0 & 1 & 3 & 0\end{array}\right]\, & {R}_{1} & :={R}_{1}+{R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & 0 & 4 & 1 \\ 0 & 1 & 3 & 0\end{array}\right]\end{aligned}
$$

The corresponding system is now

$$
\left\{\begin{aligned}x+4z &=1 \\ y+3z &=0.\end{aligned}\right.
$$

We see that the basic variables are $x$ and $y,$ and we have one free variable $z.$ From the second equation, we get $y=-3z,$ and from the first equation, we obtain $x=1-4z.$ Therefore, the general solution is

$$
\left\{\begin{aligned}x &=1-4z, \\ y &=-3z, \\ z &=z.\end{aligned}\right.
$$

In vector form, the solution can be written as

$$
\begin{aligned}\begin{bmatrix}x \\ y \\ z\end{bmatrix}=\begin{bmatrix}1-4z \\ -3z \\ z\end{bmatrix}=\begin{bmatrix}1 \\ 0 \\ 0\end{bmatrix}+z\begin{bmatrix}-4 \\ -3 \\ 1\end{bmatrix},\,z\in (-\infty ,\infty ).\end{aligned}
$$



### example 17592186115070 — Solving a Consistent System of Equations Using Gauss-Jordan Elimination

Consider the system of linear equations


$$
\left\{\begin{aligned}x+5y+z &=2 \\ x+5y+2z &=5.\end{aligned}\right.
$$


Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

The augmented matrix for this system is


$$
M= \left[ \begin{array}{ccc|c}1 & 5 & 1 & 2 \\ 1 & 5 & 2 & 5\end{array} \right].
$$



Using the standard Gauss-Jordan method, we can reduce this matrix to reduced row echelon form as follows:

$$
\begin{aligned}M & ∼\left[\begin{array}{ccc|c}1 & 5 & 1 & 2 \\ 1 & 5 & 2 & 5\end{array}\right] & {R}_{2} & :={R}_{2}+(-1){R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 5 & 1 & 2 \\ 0 & 0 & 1 & 3\end{array}\right] & {R}_{1} & :={R}_{1}+(-1){R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & 5 & 0 & -1 \\ 0 & 0 & 1 & 3\end{array}\right]\end{aligned}
$$

The corresponding system is now


$$
\left\{\begin{aligned}x+5y &=-1 \\ z &=3.\end{aligned}\right.
$$



The basic variables are the variables whose coefficients are pivots. In this case, the basic variables are $x$ and $z,$ and we have one free variable, $y.$ That means we need to find $x$ and $z$ in terms of $y.$ 

Therefore, the general solution is

$$
\left\{\begin{aligned}x &=-1-5y \\ y &=y \\ z &=3,\end{aligned}\right.
$$

where $y$ (the free variable) is an arbitrary number.

In vector form, the solution can be written as

$$
\begin{aligned}\begin{bmatrix}x \\ y \\ z\end{bmatrix}=\begin{bmatrix}-1-5y \\ y \\ 3\end{bmatrix},\,y\in (-\infty ,\infty ).\end{aligned}
$$

### tutorial 17592186116494 — Consistent and Inconsistent Systems of Linear Equations

Recall that a system of linear equations is called **consistent** if it has at least one solution. Otherwise, if there are no solutions, the system is called **inconsistent**. 

For a consistent system, 

- the system is called **consistent independent** if the solution is unique, while

- the system is called **consistent dependent** if there are infinitely many solutions.

![](images/f5/f5b808eac6e1d865b13b68ce2a4f7d317560ae3965928e478531fcd2148c2c6b.png)



### example 17592186115124 — Classifying a System as Consistent Dependent, Consistent Independent, or Inconsistent

Given the system


$$
\left\{\begin{aligned}2x-3y &=4 \\ -4x+6y &=-8,\end{aligned}\right.
$$


which of the following statements are true?

- The system is consistent dependent

- The system has no solution

- The system is consistent independent

To classify the system, we first need to find its solution. The augmented matrix for this system is


$$
M= \left[ \begin{array}{cc|c}2 & -3 & 4 \\ -4 & 6 & -8\end{array} \right].
$$



Using Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =\left[\begin{array}{cc|c}2 & -3 & 4 \\ -4 & 6 & -8\end{array}\right] & {R}_{2} & :={R}_{2}+2{R}_{1} \\  & ∼\left[\begin{array}{cc|c}2 & -3 & 4 \\ 0 & 0 & 0\end{array}\right]\end{aligned}
$$

The system is now


$$
\left\{\begin{aligned}2x-3y &=4 \\ 0x+0y &=0.\end{aligned}\right.
$$



Since any numbers $x$ and $y$ form a solution of the final equation $0x+0y=0,$ we can remove this equation from the system. So, our system now consists of just a single equation:

$$
2x -3y= 4
$$

The basic variable is $x,$ and we have a free variable $y.$ That means we need to find $x$ in terms of $y.$ 

Therefore, since there are infinitely many solutions, we conclude that the system is *consistent dependent*.

As a result, only statement I is true.

### example 17592186115071 — Determining the Value of a Constant for Which a Given Linear System Is Consistent or Inconsistent

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
\left\{\begin{aligned}2x-2y &=1, \\ 4x+ky &=-3\end{aligned}\right.
$$

The augmented matrix for this system is



$$
M= \left[ \begin{array}{cc|c}2 & -2 & 1 \\ 4 & k & -3\end{array} \right].
$$



Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =\left[\begin{array}{cc|c}2 & -2 & 1 \\ 4 & k & -3\end{array}\right] & {R}_{2} & :={R}_{2}-2{R}_{1} \\  & ∼\left[\begin{array}{cc|c}2 & -2 & 1 \\ 0 & k+4 & -5\end{array}\right]\end{aligned}
$$

The corresponding system is now 



$$
\left\{\begin{aligned}2x-2y &=1 \\ (k+4)y &=-5.\end{aligned}\right.
$$



The system is inconsistent if it has no solutions. For the system to have no solutions, one of the equations above must be false.

If $k=-4,$ then the second equation is $0=-5,$ which is false, and the system will have no solution.

Therefore, our system is inconsistent when $k=-4.$

## Representative practice (first three per skill; full bank in practice.json)

### Solving a Consistent System of Equations Using Gauss-Jordan Elimination (45 captured questions)

Question 17592186115751 — None

Consider the system of linear equations
$$
\displaystyle \left\{\begin{aligned}x + y + 2z &=19 \\ 3x + y + 2z &=31\end{aligned}\right.
$$.
Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

Solution: The augmented matrix is

$$
M=\left[\begin{array}{ccc|c}1&1&2&19\\3&1&2&31\end{array}\right].
$$

Apply $R_2:=R_2-3R_1$, then $R_2:=-\frac12R_2$, and finally $R_1:=R_1-R_2$. The reduced row echelon form is

$$
M\sim\left[\begin{array}{ccc|c}1&0&0&6\\0&1&2&13\end{array}\right].
$$

Hence $x=6$ and $y=13-2z$, with $z$ free. The solution is

$$
\begin{bmatrix}6\\13-2z\\z\end{bmatrix},\qquad z\in(-\infty,\infty).
$$

Answer selection: \begin{bmatrix}6 \\ 13 - 2z \\ z\end{bmatrix}, z ∈ (- ∞, ∞)

Question 17592186115830 — question.difficulty/easy

Consider the system of linear equations

$$
\left\{\begin{aligned}x+3z &=-2 \\ x+y &=0.\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

Solution: The augmented matrix for this system is

$$
M=\left[\begin{array}{ccc|c}1 & 0 & 3 & -2 \\ 1 & 1 & 0 & 0\end{array}\right].
$$

Using the standard method of Gaussian elimination, we can reduce this matrix to reduced row echelon form as follows:

$$
\begin{aligned}M & =\left[\begin{array}{ccc|c}1 & 0 & 3 & -2 \\ 1 & 1 & 0 & 0\end{array}\right] & {R}_{2} & :={R}_{2}+(-1){R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 0 & 3 & -2 \\ 0 & 1 & -3 & 2\end{array}\right]\end{aligned}
$$

The corresponding system is now  

$$
\left\{\begin{aligned}x+3z &=-2 \\ y-3z &=2.\end{aligned}\right.
$$

The basic variables are the variables whose coefficients are pivots. In this case, the basic variables are $x$ and $y,$ and we have one free variable, $z.$ That means we need to find $x$ and $y$ in terms of $z.$ 

Therefore, the general solution is

$$
\left\{\begin{aligned}x &=-2-3z \\ y &=2+3z \\ z &=z,\end{aligned}\right.
$$

where $z$ (the free variable) is an arbitrary number.

In vector form, the latter can be written as

$$
\begin{aligned}\begin{bmatrix}x \\ y \\ z\end{bmatrix}=\begin{bmatrix}-2-3z \\ 2+3z \\ z\end{bmatrix},\,z\in (-\infty ,\infty ).\end{aligned}
$$

Answer selection: \begin{bmatrix}-2-3z \\ 2+3z \\ z\end{bmatrix},\,z\in (-\infty ,\infty )

Question 17592186266111 — question.difficulty/easy

Consider the system of linear equations

$$
\left\{\begin{aligned}{x}_{1}-{x}_{2}+2{x}_{3} &=2 \\ {x}_{1}-3{x}_{3} &=1.\end{aligned}\right.
$$

 
Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

Solution: The augmented matrix for this system is

$$
M=\left[\begin{array}{ccc|c}1 & -1 & 2 & 2 \\ 1 & 0 & -3 & 1\end{array}\right].
$$

Using the standard Gauss-Jordan method, we can reduce this matrix to reduced row echelon form as follows:

$$
\begin{aligned}M & =\left[\begin{array}{ccc|c}1 & -1 & 2 & 2 \\ 1 & 0 & -3 & 1\end{array}\right] & {R}_{2} & :={R}_{2}-{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -1 & 2 & 2 \\ 0 & 1 & -5 & -1\end{array}\right] & {R}_{1} & :={R}_{1}+{R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & 0 & -3 & 1 \\ 0 & 1 & -5 & -1\end{array}\right]\end{aligned}
$$

 

The corresponding system is now  

$$
\left\{\begin{aligned}{x}_{1}-3{x}_{3} &=1 \\ {x}_{2}-5{x}_{3} &=-1.\end{aligned}\right.
$$

The basic variables are the variables whose coefficients are pivots. In this case, the basic variables are ${x}_{1}$ and ${x}_{2},$ and we have one free variable, ${x}_{3}.$ That means we need to find ${x}_{1}$ and ${x}_{2}$ in terms of ${x}_{3}.$ 

Therefore, the general solution is

$$
\left\{\begin{aligned}{x}_{1} &=3{x}_{3}+1 \\ {x}_{2} &=5{x}_{3}-1 \\ {x}_{3} &={x}_{3},\end{aligned}\right.
$$

where ${x}_{3}$ (the free variable) is an arbitrary number.

In vector form, the solution can be written as

$$
\begin{aligned}\begin{bmatrix}{x}_{1} \\ {x}_{2} \\ {x}_{3}\end{bmatrix}=\begin{bmatrix}3{x}_{3}+1 \\ 5{x}_{3}-1 \\ {x}_{3}\end{bmatrix},\,{x}_{3}\in (-\infty ,\infty ).\end{aligned}
$$

Answer selection: \begin{bmatrix}3{x}_{3}+1 \\ 5{x}_{3}-1 \\ {x}_{3}\end{bmatrix},\,{x}_{3}\in (-\infty ,\infty )

### Classifying a System as Consistent Dependent, Consistent Independent, or Inconsistent (32 captured questions)

Question 17592186115752 — question.difficulty/moderate

Consider the following system of equations.

$$
\left\{\begin{aligned}-x+2y &=6 \\ 2x-3y &=13 \\ 5x-y &=45\end{aligned}\right.
$$

Which of the following statements are true?

Select all that apply.

Solution: To classify the system, we first need to find its solution. The augmented matrix for this system is

$$
M=\left[\begin{array}{cc|c}-1 & 2 & 6 \\ 2 & -3 & 13 \\ 5 & -1 & 45\end{array}\right].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =\left[\begin{array}{cc|c}-1 & 2 & 6 \\ 2 & -3 & 13 \\ 5 & -1 & 45\end{array}\right] & {R}_{2} & :={R}_{2}+2{R}_{1} \\  & ∼\left[\begin{array}{cc|c}-1 & 2 & 6 \\ 0 & 1 & 25 \\ 5 & -1 & 45\end{array}\right] & {R}_{3} & :={R}_{3}+5{R}_{1} \\  & ∼\left[\begin{array}{cc|c}-1 & 2 & 6 \\ 0 & 1 & 25 \\ 0 & 9 & 75\end{array}\right] & {R}_{3} & :={R}_{3}+(-9){R}_{2} \\  & ∼\left[\begin{array}{cc|c}1 & -2 & -6 \\ 0 & 1 & 25 \\ 0 & 0 & -150\end{array}\right]\end{aligned}
$$

The final row corresponds to the equation $0x+0y=-150,$ and this has no solution. Therefore, our system has no solution, and we conclude that the system is inconsistent.

As a result, only statement “The system is inconsistent” is true.

Answer None of the above: false

Answer The system has a unique solution: false

Answer The system is consistent dependent: false

Answer The system is inconsistent: true

Question 17592186115832 — question.difficulty/moderate

Consider the following system of equations.

$$
\left\{\begin{aligned}x-3y+z &=0 \\ -4x+6y &=2\end{aligned}\right.
$$

Which of the following statements are true?

Select all that apply.

Solution: To classify the system, we first need to find its solution. The augmented matrix for this system is

$$
M=\left[\begin{array}{ccc|c}1 & -3 & 1 & 0 \\ -4 & 6 & 0 & 2\end{array}\right].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =\left[\begin{array}{ccc|c}1 & -3 & 1 & 0 \\ -4 & 6 & 0 & 2\end{array}\right] & {R}_{2} & :={R}_{2}+4{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -3 & 1 & 0 \\ 0 & -6 & 4 & 2\end{array}\right]\end{aligned}
$$

The basic variables are the variables whose coefficients are pivots. In this case, the basic variables are $x$ and $y,$ and we have one free variable, $z.$ That means we can to find $x$ and $y$ in terms of $z.$ 

Therefore, since there are infinitely many solutions, we conclude that the system is *consistent dependent*. 

As a result, only statement “The system is consistent dependent” is true.

Answer None of the above: false

Answer The system has no solution: false

Answer The system is consistent dependent: true

Answer The system is consistent independent: false

Question 17592186266113 — question.difficulty/moderate

Consider the following system of equations.

$$
\left\{\begin{aligned}x+4y &=-1 \\ 2x+8y &=-2 \\ -3x-12y &=3\end{aligned}\right.
$$

Which of the following statements are true?

Select all that apply.

Solution: To classify the system, we first need to find its solution. The augmented matrix for this system is

$$
M=\left[\begin{array}{cc|c}1 & 4 & -1 \\ 2 & 8 & -2 \\ -3 & -12 & 3\end{array}\right].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =\left[\begin{array}{cc|c}1 & 4 & -1 \\ 2 & 8 & -2 \\ -3 & -12 & 3\end{array}\right] & {R}_{2} & :={R}_{2}-2{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & 4 & -1 \\ 0 & 0 & 0 \\ -3 & -12 & 3\end{array}\right] & {R}_{3} & :={R}_{3}+3{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & 4 & -1 \\ 0 & 0 & 0 \\ 0 & 0 & 0\end{array}\right]\end{aligned}
$$

The basic variables are the variables whose coefficients are pivots. In this case, the basic variable is $x,$ and we have one free variable, $y.$ That means we can find $x$ in terms of $y.$ 

Therefore, since there are infinitely many solutions, we conclude that the system is *consistent dependent*. 

As a result, only statement “The system is consistent dependent” is true.

Answer None of the above: false

Answer The system has a unique solution: false

Answer The system is consistent dependent: true

Answer The system is inconsistent: false

### Determining the Value of a Constant for Which a Given Linear System Is Consistent or Inconsistent (27 captured questions)

Question 17592186115753 — question.difficulty/hard

Determine the value of $k$ for which the following system of linear equations is consistent dependent:

$$
\left\{\begin{aligned}3x+4y &=12 \\ x+ky &=4\end{aligned}\right.
$$

Solution: The augmented matrix for this system is

$$
M=\left[\begin{array}{cc|c}3 & 4 & 12 \\ 1 & k & 4\end{array}\right].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =\left[\begin{array}{cc|c}3 & 4 & 12 \\ 1 & k & 4\end{array}\right] & {R}_{1} & ↔{R}_{2} \\  & ∼\left[\begin{array}{cc|c}1 & k & 4 \\ 3 & 4 & 12\end{array}\right] & {R}_{2} & :={R}_{2}+(-3){R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & k & 4 \\ 0 & 4-3k & 0\end{array}\right]\end{aligned}
$$

The corresponding system is now 

$$
\left\{\begin{aligned}x+ky &=4 \\ (4-3k)y &=0.\end{aligned}\right.
$$

The system is consistent dependent if it has infinitely many solutions. For the system to have infinitely many solutions, it must have at least one free variable.

If $k=\frac{4}{3},$ then the second equation is $0=0,$ which is true for any value of $y$, and we can remove this equation from the system. As a result, the system will contain only one equation, $x+ky=4.$ 

Then, the basic variable will be $x,$ and we will have a free variable $y.$ That means the system will have infinitely many solutions.

Therefore, our system is consistent dependent when $k=\frac{4}{3}.$

Answer selection: k=\frac{4}{3}

Question 17592186115831 — question.difficulty/moderate

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
\left\{\begin{aligned}2x+3y &=1 \\ 6x+(k+3)y &=-5\end{aligned}\right.
$$

Solution: The augmented matrix for this system is

$$
M=\left[\begin{array}{cc|c}2 & 3 & 1 \\ 6 & k+3 & -5\end{array}\right].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =\left[\begin{array}{cc|c}2 & 3 & 1 \\ 6 & k+3 & -5\end{array}\right] & {R}_{2} & :={R}_{2}+(-3){R}_{1} \\  & ∼\left[\begin{array}{cc|c}2 & 3 & 1 \\ 0 & k-6 & -8\end{array}\right]\end{aligned}
$$

The corresponding system is now 

$$
\left\{\begin{aligned}2x+3y &=1 \\ (k-6)y &=-8.\end{aligned}\right.
$$

The system is inconsistent if it has no solutions. For the system to have no solutions, one of the equations above must be false.

If $k=6,$ then the second equation is $0=-8,$ which is false, and the system will have no solution.

Therefore, our system is inconsistent when $k=6.$

Answer selection: k=6

Question 17592186266116 — question.difficulty/moderate

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
\left\{\begin{aligned}-3x+2y &=1 \\ 6x+(k+9)y &=5\end{aligned}\right.
$$

Solution: The augmented matrix for this system is

$$
M=\left[\begin{array}{cc|c}-3 & 2 & 1 \\ 6 & k+9 & 5\end{array}\right].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =\left[\begin{array}{cc|c}-3 & 2 & 1 \\ 6 & k+9 & 5\end{array}\right] & {R}_{2} & :={R}_{2}+2{R}_{1} \\  & ∼\left[\begin{array}{cc|c}-3 & 2 & 1 \\ 0 & k+13 & 7\end{array}\right]\end{aligned}
$$

The corresponding system is now 

$$
\left\{\begin{aligned}-3x+2y &=1 \\ (k+13)y &=7.\end{aligned}\right.
$$

The system is inconsistent if it has no solutions. For the system to have no solutions, one of the equations above must be false.

If $k=-13,$ then the second equation is $0=7,$ which is false, and the system will have no solution.

Therefore, our system is inconsistent when $k=-13.$

Answer selection: k=-13
