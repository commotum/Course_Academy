# 17592186049392 Solving Systems of Equations Using Inverse Matrices

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186093403 — Introduction

We know that we can write a system of three linear equations in three variables in the form $A\mathbf{x}=\mathbf{b},$ where

- $A$ is the $3\times 3$ coefficient matrix,

- $\mathbf{x}$ is the column vector of variables, and

- $\mathbf{b}$ is the column vector of constants.

If the $3\times 3$ matrix $A$ is invertible, then we can find a solution to the system $A\mathbf{x} = \mathbf{b}$ by "pre-multiplying" both sides of the equation by $A^{-1}{:}$

$$
\begin{aligned}A\mathbf{x} & =\mathbf{b} \\ {A}^{-1}A\mathbf{x} & ={A}^{-1}\mathbf{b} \\ {I}_{3}\mathbf{x} & ={A}^{-1}\mathbf{b} \\ \mathbf{x} & ={A}^{-1}\mathbf{b}\end{aligned}
$$

So, to find the solution of $A\mathbf{x}=\mathbf{b},$ we simply calculate $\mathbf{x}= A^{-1}\mathbf{b}.$

Let's see how this works for a particular system in the next example.



### example 17592186092025 — Solving a 3x3 System of Equations Given the Inverse of the Coefficient Matrix

Consider the following system of linear equations:

$$
\left\{\begin{aligned}-2x+5y-2z &=-2 \\ -3y+z &=-2 \\ 3x-7y+3z &=3\end{aligned}\right.
$$

The system above has the matrix representation $A \mathbf{x} = \mathbf{b}.$ Given that $\mathbf x = \langle x,y,z\rangle$ is unique, what is the value of $x+y+z?$ 

*Hint: The inverse of the coefficient matrix is given by*


$$
\qquad A^{-1}= \begin{bmatrix}-2 & -1 & -1 \\ 3 & 0 & 2 \\ 9 & 1 & 6\end{bmatrix}.
$$



First, let's write our system in matrix form as follows:

$$
\begin{aligned}Ax & =b \\ \begin{bmatrix}-2 & 5 & -2 \\ 0 & -3 & 1 \\ 3 & -7 & 3\end{bmatrix}\begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}-2 \\ -2 \\ 3\end{bmatrix}\end{aligned}
$$

Recall that the solution to $A\mathbf{x}=\mathbf{b}$ is given by $\mathbf{x}= A^{-1}\mathbf{b}.$

Therefore, we obtain

$$
\begin{aligned}x & ={A}^{-1}b \\  & =\begin{bmatrix}-2 & -1 & -1 \\ 3 & 0 & 2 \\ 9 & 1 & 6\end{bmatrix}\begin{bmatrix}-2 \\ -2 \\ 3\end{bmatrix} \\  & =\begin{bmatrix}3 \\ 0 \\ -2\end{bmatrix}.\end{aligned}
$$

So, the solution is $x=3, y=0, z=-2.$

Finally, $x+y+z=3+0+(-2)=1.$

### example 17592186092026 — Solving a 3x3 System of Equations By Calculating the Inverse of the Coefficient Matrix

Solve the following system of linear equations using matrices:

$$
\left\{\begin{aligned}3y+x+z &=0 \\ z+4y-5 &=2 \\ 1+2x-y &=-3\end{aligned}\right.
$$

First, we organize the system so that the variables are in the correct order and every variable has a coefficient:

$$
\left\{\begin{aligned}x+3y+z &=0 \\ 0x+4y+z &=7 \\ 2x-y+0z &=-4\end{aligned}\right.
$$

Next, we  write the system in the form $A\mathbf{x} = \mathbf{b}$, where $A$ is a $3\times 3$ matrix and $\mathbf{x}$ and $\mathbf{b}$ are $3\times 1$ column vectors. We can do this as follows:



$$
\begin{bmatrix}1 & 3 & 1 \\ 0 & 4 & 1 \\ 2 & -1 & 0\end{bmatrix} \begin{bmatrix}x \\ y \\ z\end{bmatrix} = \begin{bmatrix}0 \\ 7 \\ -4\end{bmatrix}
$$



Now, the solution to $A\mathbf{x}=\mathbf{b}$ is given by $\mathbf{x}= A^{-1}\mathbf{b}.$ So, we compute $A^{-1}$ as follows:

*Step 1*: Find the determinant of $A.$

$$
\begin{aligned}\det (A)=\begin{vmatrix}1 & 3 & 1 \\ 0 & 4 & 1 \\ 2 & -1 & 0\end{vmatrix} & =1\begin{vmatrix}4 & 1 \\ -1 & 0\end{vmatrix}-3\begin{vmatrix}0 & 1 \\ 2 & 0\end{vmatrix}+1\begin{vmatrix}0 & 4 \\ 2 & -1\end{vmatrix} \\  & =(1)-3(-2)+(-8) \\  & =1+6-8 \\  & =-1\end{aligned}
$$

*Step 2*: Compute the matrix of minors.

$$
\begin{aligned}M & =\begin{bmatrix}\begin{vmatrix}4 & 1 \\ -1 & 0\end{vmatrix} & \begin{vmatrix}0 & 1 \\ 2 & 0\end{vmatrix} & \begin{vmatrix}0 & 4 \\ 2 & -1\end{vmatrix} \\ \begin{vmatrix}3 & 1 \\ -1 & 0\end{vmatrix} & \begin{vmatrix}1 & 1 \\ 2 & 0\end{vmatrix} & \begin{vmatrix}1 & 3 \\ 2 & -1\end{vmatrix} \\ \begin{vmatrix}3 & 1 \\ 4 & 1\end{vmatrix} & \begin{vmatrix}1 & 1 \\ 0 & 1\end{vmatrix} & \begin{vmatrix}1 & 3 \\ 0 & 4\end{vmatrix}\end{bmatrix} \\  & =\begin{bmatrix}1 & -2 & -8 \\ 1 & -2 & -7 \\ -1 & 1 & 4\end{bmatrix}\end{aligned}
$$

*Step 3*:  Find the matrix of cofactors.



$$
C=\begin{bmatrix}1 & 2 & -8 \\ -1 & -2 & 7 \\ -1 & -1 & 4\end{bmatrix}
$$



*Step 4*: Transpose the matrix of cofactors.



$$
C^T=\begin{bmatrix}1 & -1 & -1 \\ 2 & -2 & -1 \\ -8 & 7 & 4\end{bmatrix}
$$



*Step 5*: Apply the inverse matrix formula.



$$
A^{-1}=\dfrac{1}{\det (A)}C^T=\dfrac{1}{-1}\begin{bmatrix}1 & -1 & -1 \\ 2 & -2 & -1 \\ -8 & 7 & 4\end{bmatrix} =\begin{bmatrix}-1 & 1 & 1 \\ -2 & 2 & 1 \\ 8 & -7 & -4\end{bmatrix} .
$$



Finally, we can calculate the solution as follows:

$$
\begin{aligned}x & ={A}^{-1}b \\  & =\begin{bmatrix}-1 & 1 & 1 \\ -2 & 2 & 1 \\ 8 & -7 & -4\end{bmatrix}\begin{bmatrix}0 \\ 7 \\ -4\end{bmatrix} \\  & =\begin{bmatrix}3 \\ 10 \\ -33\end{bmatrix}\end{aligned}
$$

Therefore, the solution is $x=3,$ $y=10,$ $z=-33.$

### example 17592186092027 — Solving a Matrix Equation Using Algebraic Manipulation

Consider a matrix equation $B\,\mathbf{x} = A^{-1}\,\mathbf{d},$ where $A$ and $B$ are $10 \times 10$ non-singular matrices, while $\mathbf{x}$ and $\mathbf{d}$ are $10 \times 1$ column vectors. Solve the equation for $\mathbf{x}.$

Since $B$ is not singular, it must have an inverse $B^{−1}.$ Now, pre-multiplying both sides of the equation $B\,\mathbf{x} = A^{-1}\,\mathbf{d}$ by $B^{-1},$ we obtain

$$
\begin{aligned}B\,x & ={A}^{-1}\,d \\ {B}^{-1}B\,x & ={B}^{-1}{A}^{-1}\,d \\ {I}_{10}\,x & ={B}^{-1}{A}^{-1}\,d \\ x & ={B}^{-1}{A}^{-1}\,d.\end{aligned}
$$

## Representative practice (first three per skill; full bank in practice.json)

### Solving a 3x3 System of Equations Given the Inverse of the Coefficient Matrix (29 captured questions)

Question 17592186092817 — None

Consider the following system of linear equations:

$$
\displaystyle \left\{\begin{aligned}x - 2y + 4z &=7 \\ x - y + z &=-1 \\ y - 2z &=-5\end{aligned}\right.
$$

The system above has the matrix representation $Ax = b$. Given that $x = ⟨x, y, z⟩$ is unique, what is the value of $x + y + z$?

*Hint: The inverse of the coefficient matrix is given by*
$$
\displaystyle A^{-1} = \begin{bmatrix}1 & 0 & 2 \\ 2 & -2 & 3 \\ 1 & -1 & 1\end{bmatrix}.
$$

Solution: The constant vector is $b=\begin{bmatrix}7\\-1\\-5\end{bmatrix}$. Multiplying by the given inverse gives

$$
\begin{bmatrix}x\\y\\z\end{bmatrix}=A^{-1}b=\begin{bmatrix}1&0&2\\2&-2&3\\1&-1&1\end{bmatrix}\begin{bmatrix}7\\-1\\-5\end{bmatrix}=\begin{bmatrix}-3\\1\\3\end{bmatrix}.
$$

Therefore $x+y+z=-3+1+3=1$.

Answer selection: 1

Question 17592186092818 — question.difficulty/easy

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x-y+3z &=2 \\ x-2y-5z &=-1 \\ 2x-3y+2z &=1\end{aligned}\right.
$$

The system above has the matrix representation $Ax=b.$ Given that $x=⟨x,y,z⟩$ is unique, what is the value of $x+y+z?$ 

*Hint: The inverse of the coefficient matrix is given by*

$$
\,{A}^{-1}=-\frac{1}{4}\begin{bmatrix}-19 & -7 & 11 \\ -12 & -4 & 8 \\ 1 & 1 & -1\end{bmatrix}.
$$

Solution: First, let's write our system in matrix form as follows:

$$
\begin{aligned}Ax & =b \\ \begin{bmatrix}1 & -1 & 3 \\ 1 & -2 & -5 \\ 2 & -3 & 2\end{bmatrix}\begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}2 \\ -1 \\ 1\end{bmatrix}\end{aligned}
$$

Recall that the solution to $Ax=b$ is given by $x={A}^{-1}b.$

Therefore, we obtain

$$
\begin{aligned}x & ={A}^{-1}b \\  & =-\frac{1}{4}\begin{bmatrix}-19 & -7 & 11 \\ -12 & -4 & 8 \\ 1 & 1 & -1\end{bmatrix}\begin{bmatrix}2 \\ -1 \\ 1\end{bmatrix} \\  & =\begin{bmatrix}5 \\ 3 \\ 0\end{bmatrix}.\end{aligned}
$$

So, the solution is $x=5,y=3,z=0.$

Finally, $x+y+z=5+3+0=8.$

Answer selection: 8

Question 17592186292892 — question.difficulty/easy

Consider the following system of linear equations:

$$
\left\{\begin{aligned}2x-3y+z &=-1 \\ x-y+3z &=2 \\ -2x+y-z &=1\end{aligned}\right.
$$

The system above has the matrix representation $Ax=b.$ Given that $x=⟨x,y,z⟩$ is unique, and the inverse of the coefficient matrix is given by

$$
{A}^{-1}=\frac{1}{10}\begin{bmatrix}-2 & -2 & -8 \\ -5 & 0 & -5 \\ -1 & 4 & 1\end{bmatrix},
$$

the solution of the system of equations is 

$x=$
{{field-1}}, 
$\,y=$
{{field-2}}, 
$\,z=$
{{field-3}}.

Solution: First, let's write our system in matrix form as follows:

$$
\begin{aligned}Ax & =b \\ \begin{bmatrix}2 & -3 & 1 \\ 1 & -1 & 3 \\ -2 & 1 & -1\end{bmatrix}\begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}-1 \\ 2 \\ 1\end{bmatrix}\end{aligned}
$$

Recall that the solution to $Ax=b$ is given by $x={A}^{-1}b.$

Therefore, we obtain

$$
\begin{aligned}x & ={A}^{-1}b \\  & =\frac{1}{10}\begin{bmatrix}-2 & -2 & -8 \\ -5 & 0 & -5 \\ -1 & 4 & 1\end{bmatrix}\begin{bmatrix}-1 \\ 2 \\ 1\end{bmatrix} \\  & =\frac{1}{10}\begin{bmatrix}-10 \\ 0 \\ 10\end{bmatrix} \\  & =\begin{bmatrix}-1 \\ 0 \\ 1\end{bmatrix}.\end{aligned}
$$

So, the solution is 

$$
x=-1,\,y=0,\,z=1.
$$

Answer field-1: -1

Answer field-2: 0

Answer field-3: 1

### Solving a 3x3 System of Equations By Calculating the Inverse of the Coefficient Matrix (28 captured questions)

Question 17592186092709 — question.difficulty/hard

Solve the following system of linear equations by finding the inverse of the coefficient matrix:

$$
\left\{\begin{aligned}2x-3+z &=0 \\ 5y-1+3x &=2z+1 \\ 3z+2x-1 &=2y\end{aligned}\right.
$$

Find  $x+y+z.$

Solution: First, let's rewrite the system in the correct order:

$$
\left\{\begin{aligned}2x+z &=3 \\ 3x+5y-2z &=2 \\ 2x-2y+3z &=1\end{aligned}\right.
$$

Next, we  write the system in the form $Ax=b$, where $A$ is a $3\times 3$ matrix and $x$ and $b$ are $3\times 1$ column vectors. We can do this as follows:

$$
\begin{bmatrix}2 & 0 & 1 \\ 3 & 5 & -2 \\ 2 & -2 & 3\end{bmatrix}\begin{bmatrix}x \\ y \\ z\end{bmatrix}=\begin{bmatrix}3 \\ 2 \\ 1\end{bmatrix}.
$$

Now, the solution to $Ax=b$ is given by $x={A}^{-1}b.$ So, we compute ${A}^{-1}$ as follows:

*Step 1:*

$$
\begin{aligned}\det (A) & =\begin{vmatrix}2 & 0 & 1 \\ 3 & 5 & -2 \\ 2 & -2 & 3\end{vmatrix} \\  & =2\begin{vmatrix}5 & -2 \\ -2 & 3\end{vmatrix}-0+\begin{vmatrix}3 & 5 \\ 2 & -2\end{vmatrix} \\  & =2(15-4)+(-6-10) \\  & =22-16 \\  & =6.\end{aligned}
$$

 

*Step 2:*

$$
\begin{aligned}M & =\begin{bmatrix}\begin{vmatrix}5 & -2 \\ -2 & 3\end{vmatrix} & \begin{vmatrix}3 & -2 \\ 2 & 3\end{vmatrix} & \begin{vmatrix}3 & 5 \\ 2 & -2\end{vmatrix} \\ \begin{vmatrix}0 & 1 \\ -2 & 3\end{vmatrix} & \begin{vmatrix}2 & 1 \\ 2 & 3\end{vmatrix} & \begin{vmatrix}2 & 0 \\ 2 & -2\end{vmatrix} \\ \begin{vmatrix}0 & 1 \\ 5 & -2\end{vmatrix} & \begin{vmatrix}2 & 1 \\ 3 & -2\end{vmatrix} & \begin{vmatrix}2 & 0 \\ 3 & 5\end{vmatrix}\end{bmatrix} \\  & =\begin{bmatrix}11 & 13 & -16 \\ 2 & 4 & -4 \\ -5 & -7 & 10\end{bmatrix}.\end{aligned}
$$

*Step 3:*

$$
C=\begin{bmatrix}11 & -13 & -16 \\ -2 & 4 & 4 \\ -5 & 7 & 10\end{bmatrix}.
$$

*Step 4:*

$$
{C}^{T}=\begin{bmatrix}11 & -2 & -5 \\ -13 & 4 & 7 \\ -16 & 4 & 10\end{bmatrix}.
$$

*Step 5:*

$$
{A}^{-1}=\frac{1}{\det (A)}{C}^{T}=\frac{1}{6}\begin{bmatrix}11 & -2 & -5 \\ -13 & 4 & 7 \\ -16 & 4 & 10\end{bmatrix}.
$$

Finally, the solution to the given system is

$$
\begin{aligned}x & ={A}^{-1}b \\  & =\frac{1}{6}\begin{bmatrix}11 & -2 & -5 \\ -13 & 4 & 7 \\ -16 & 4 & 10\end{bmatrix}\begin{bmatrix}3 \\ 2 \\ 1\end{bmatrix} \\  & =\frac{1}{6}\begin{bmatrix}24 \\ -24 \\ -30\end{bmatrix} \\  & =\begin{bmatrix}4 \\ -4 \\ -5\end{bmatrix}.\end{aligned}
$$

 

Therefore, $x+y+z=4-4-5=-5.$

Answer selection: -5

Question 17592186092937 — question.difficulty/moderate

Solve the following system of linear equations by finding the inverse of the coefficient matrix:

$$
\left\{\begin{aligned}2y+3z+x &=-1 \\ 4z+y &=1 \\ 5x+6y-3 &=-3\end{aligned}\right.
$$

Solution: We organize the system so that it’s in the correct order first:

$$
\left\{\begin{aligned}x+2y+3z &=-1 \\ y+4z &=1 \\ 5x+6y &=0\end{aligned}\right.
$$

We wish to write this system in the form $Ax=b$, where $A$ is a $3\times 3$ matrix and $x$ and $b$ are $3\times 1$ column vectors. We can do this as follows:

$$
\begin{bmatrix}1 & 2 & 3 \\ 0 & 1 & 4 \\ 5 & 6 & 0\end{bmatrix}\begin{bmatrix}x \\ y \\ z\end{bmatrix}=\begin{bmatrix}-1 \\ 1 \\ 0\end{bmatrix}.
$$

Now, the solution to $Ax=b$ is given by $x={A}^{-1}b.$ So, we compute ${A}^{-1}$ as follows:

*Step 1:*

$$
\begin{aligned}\det (A) & =\begin{vmatrix}1 & 2 & 3 \\ 0 & 1 & 4 \\ 5 & 6 & 0\end{vmatrix} \\  & =1\begin{vmatrix}1 & 4 \\ 6 & 0\end{vmatrix}-2\begin{vmatrix}0 & 4 \\ 5 & 0\end{vmatrix}+3\begin{vmatrix}0 & 1 \\ 5 & 6\end{vmatrix} \\  & =1(-24)-2(-20)+3(-5) \\  & =1.\end{aligned}
$$

*Step 2:*

$$
\begin{aligned}M & =\begin{bmatrix}\begin{vmatrix}1 & 4 \\ 6 & 0\end{vmatrix} & \begin{vmatrix}0 & 4 \\ 5 & 0\end{vmatrix} & \begin{vmatrix}0 & 1 \\ 5 & 6\end{vmatrix} \\ \begin{vmatrix}2 & 3 \\ 6 & 0\end{vmatrix} & \begin{vmatrix}1 & 3 \\ 5 & 0\end{vmatrix} & \begin{vmatrix}1 & 2 \\ 5 & 6\end{vmatrix} \\ \begin{vmatrix}2 & 3 \\ 1 & 4\end{vmatrix} & \begin{vmatrix}1 & 3 \\ 0 & 4\end{vmatrix} & \begin{vmatrix}1 & 2 \\ 0 & 1\end{vmatrix}\end{bmatrix} \\  & =\begin{bmatrix}-24 & -20 & -5 \\ -18 & -15 & -4 \\ 5 & 4 & 1\end{bmatrix}.\end{aligned}
$$

*Step 3:*

$$
C=\begin{bmatrix}-24 & 20 & -5 \\ 18 & -15 & 4 \\ 5 & -4 & 1\end{bmatrix}.
$$

*Step 4:*

$$
{C}^{T}=\begin{bmatrix}-24 & 18 & 5 \\ 20 & -15 & -4 \\ -5 & 4 & 1\end{bmatrix}.
$$

*Step 5:*

$$
{A}^{-1}=\frac{1}{\det (A)}{C}^{T}=\frac{1}{1}\begin{bmatrix}-24 & 18 & 5 \\ 20 & -15 & -4 \\ -5 & 4 & 1\end{bmatrix}.
$$

Hence

$$
\begin{aligned}x & ={A}^{-1}b \\  & =\begin{bmatrix}-24 & 18 & 5 \\ 20 & -15 & -4 \\ -5 & 4 & 1\end{bmatrix}\begin{bmatrix}-1 \\ 1 \\ 0\end{bmatrix} \\  & =\begin{bmatrix}42 \\ -35 \\ 9\end{bmatrix}.\end{aligned}
$$

Hence the solution is $x=42,y=-35,z=9.$

Answer selection: x=42,y=-35,z=9

Question 17592186237787 — question.difficulty/moderate

Solve the following system of linear equations by finding the inverse of the coefficient matrix:

$$
\left\{\begin{aligned}z+2y+7x &=1 \\ 3y-z &=-2 \\ 4y-2z-3x &=0\end{aligned}\right.
$$

Solution: We organize the system so that it’s in the correct order first:

$$
\left\{\begin{aligned}7x+2y+z &=1 \\ 3y-z &=-2 \\ -3x+4y-2z &=0\end{aligned}\right.
$$

We wish to write this system in the form $Ax=b$, where $A$ is a $3\times 3$ matrix and $x$ and $b$ are $3\times 1$ column vectors. We can do this as follows:

$$
\begin{bmatrix}7 & 2 & 1 \\ 0 & 3 & -1 \\ -3 & 4 & -2\end{bmatrix}\begin{bmatrix}x \\ y \\ z\end{bmatrix}=\begin{bmatrix}1 \\ -2 \\ 0\end{bmatrix}.
$$

Now, the solution to $Ax=b$ is given by $x={A}^{-1}b.$ So, we compute ${A}^{-1}$ as follows:

*Step 1:*

$$
\begin{aligned}\det (A) & =\begin{vmatrix}7 & 2 & 1 \\ 0 & 3 & -1 \\ -3 & 4 & -2\end{vmatrix} \\  & =7\begin{vmatrix}3 & -1 \\ 4 & -2\end{vmatrix}-2\begin{vmatrix}0 & -1 \\ -3 & -2\end{vmatrix}+1\begin{vmatrix}0 & 3 \\ -3 & 4\end{vmatrix} \\  & =7(-6+4)-2(-3)+1(9) \\  & =-14+6+9 \\  & =1.\end{aligned}
$$

*Step 2:*

$$
\begin{aligned}M & =\begin{bmatrix}\begin{vmatrix}3 & -1 \\ 4 & -2\end{vmatrix} & \begin{vmatrix}0 & -1 \\ -3 & -2\end{vmatrix} & \begin{vmatrix}0 & 3 \\ -3 & 4\end{vmatrix} \\ \begin{vmatrix}2 & 1 \\ 4 & -2\end{vmatrix} & \begin{vmatrix}7 & 1 \\ -3 & -2\end{vmatrix} & \begin{vmatrix}7 & 2 \\ -3 & 4\end{vmatrix} \\ \begin{vmatrix}2 & 1 \\ 3 & -1\end{vmatrix} & \begin{vmatrix}7 & 1 \\ 0 & -1\end{vmatrix} & \begin{vmatrix}7 & 2 \\ 0 & 3\end{vmatrix}\end{bmatrix} \\  & =\begin{bmatrix}-2 & -3 & 9 \\ -8 & -11 & 34 \\ -5 & -7 & 21\end{bmatrix}.\end{aligned}
$$

*Step 3:*

$$
C=\begin{bmatrix}-2 & 3 & 9 \\ 8 & -11 & -34 \\ -5 & 7 & 21\end{bmatrix}.
$$

*Step 4:*

$$
{C}^{T}=\begin{bmatrix}-2 & 8 & -5 \\ 3 & -11 & 7 \\ 9 & -34 & 21\text{ }\end{bmatrix}.
$$

*Step 5:*

$$
{A}^{-1}=\frac{1}{\det (A)}{C}^{T}=\frac{1}{1}\begin{bmatrix}-2 & 8 & -5 \\ 3 & -11 & 7 \\ 9 & -34 & 21\text{ }\end{bmatrix}.
$$

Hence

$$
\begin{aligned}x & ={A}^{-1}b \\  & =\begin{bmatrix}-2 & 8 & -5 \\ 3 & -11 & 7 \\ 9 & -34 & 21\text{ }\end{bmatrix}\begin{bmatrix}1 \\ -2 \\ 0\end{bmatrix} \\  & =\begin{bmatrix}-18 \\ 25 \\ 77\end{bmatrix}.\end{aligned}
$$

Hence the solution is $x=-18,\,y=25,\,z=77.$

Answer selection: x=-18,\,y=25,\,z=77

### Solving a Matrix Equation Using Algebraic Manipulation (25 captured questions)

Question 17592186092813 — question.difficulty/moderate

Consider a system of $3$ linear equations in $3$ variables, written in matrix form as $D\,y=w.$ Here, $D$ is the non-singular coefficient matrix of the system, $y$ is the column vector containing the variables, and $w$ is the column vector containing the constants. The unique solution of the system can be found using the method shown below:

$$
\begin{aligned}D\,y & =w \\ {D}^{-1}D\,y & =w \\ {I}_{3}\,y & ={D}^{-1}\,w \\  & ={D}^{-1}\,w\end{aligned}
$$

From top to bottom and left to right, what are the missing parts of the derivation?

Solution: Since $D$ is not singular, it must have an inverse ${D}^{-1}.$ Now, pre-multiplying both sides of the equation $D\,y=w$ by ${D}^{-1},$ we obtain the following:

$$
\begin{aligned}D\,y & =w \\ {D}^{-1}D\,y & ={D}^{-1}w \\ {I}_{3}\,y & ={D}^{-1}\,w \\ y & ={D}^{-1}\,w\end{aligned}
$$

Therefore, the missing parts are ${D}^{-1}$ and $y.$

Answer selection: ${D}^{-1}$ and $y$

Question 17592186092819 — question.difficulty/hard

Consider a matrix equation ${A}^{-1}\,x={B}^{-1}\,d,$ where $A$ and $B$ are $5\times 5$ non-singular matrices, while $x$ and $d$ are $5\times 1$ column vectors. Solve the equation for $x.$

Solution: Pre-multiplying both sides of the equation ${A}^{-1}\,x={B}^{-1}\,d$ by $A,$ we obtain

$$
\begin{aligned}{A}^{-1}\,x & ={B}^{-1}\,d \\ A{A}^{-1}\,x & =A{B}^{-1}\,d \\ {I}_{5}\,x & =A{B}^{-1}\,d \\ x & =A{B}^{-1}\,d.\end{aligned}
$$

Answer selection: x=A{B}^{-1}\,d

Question 17592186299656 — question.difficulty/moderate

Consider a system of $3$ linear equations in $3$ variables, written in matrix form as $A\,x=b.$ Here, $A$ is the non-singular coefficient matrix of the system, $x$ is the column vector containing the variables, and $b$ is the column vector containing the constants. What are the missing parts of the derivation method shown below to find the unique solution of the system?

$$
A\,x={{field-1}}
$$

$$
{{field-2}}\,x={A}^{-1}\,b
$$

$$
{I}_{3}\,x={A}^{-1}\,{{field-3}}
$$

$$
{{field-4}}={A}^{-1}\,b
$$

Solution: Since $A$ is not singular, it must have an inverse ${A}^{-1}.$ Now, pre-multiplying both sides of the equation $A\,x=b$ by ${A}^{-1},$ we obtain the following:

$$
\begin{aligned}A\,x & =b \\ {A}^{-1}A\,x & ={A}^{-1}\,b \\ {I}_{3}\,x & ={A}^{-1}\,b \\ x & ={A}^{-1}\,b\end{aligned}
$$

Answer field-1: b

Answer field-2: {A}^{-1}A

Answer field-3: b

Answer field-4: x
