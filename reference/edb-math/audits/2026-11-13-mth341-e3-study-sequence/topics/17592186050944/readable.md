# 17592186050944 Solving 2x2 Systems of Equations Using Inverse Matrices

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186093402 — Introduction

If the $2\times 2$ matrix $A$ is invertible, then we can find a solution to the system 

$$A\mathbf{x} = \mathbf{b}$$

by "pre-multiplying" both sides of the equation by $A^{-1}\mathbin{:}$

$$\begin{aligned}A\mathbf{x} & =\mathbf{b} \\ {A}^{-1}A\mathbf{x} & ={A}^{-1}\mathbf{b} \\ {I}_{2}\mathbf{x} & ={A}^{-1}\mathbf{b} \\ \mathbf{x} & ={A}^{-1}\mathbf{b}\end{aligned}$$

So, to find the solution of $A\mathbf{x} = \mathbf{b},$ we simply calculate $\mathbf{x}=A^{-1}\mathbf{b}.$

For instance, to find the solution to the system of equations

$$
\begin{bmatrix}1 & 1 \\ 0 & 1\end{bmatrix}
\begin{bmatrix}x \\ y\end{bmatrix}
	=
	\begin{bmatrix}5 \\ 2\end{bmatrix},
$$

 we first calculate the inverse of the coefficient matrix $A = \begin{bmatrix}1 & 1 \\ 0 & 1\end{bmatrix}.$
This gives

$$
A^{-1} =\begin{bmatrix}1 & -1 \\ 0 & 1\end{bmatrix}.
$$

Then, the solution to this system is

$$\begin{aligned}\mathbf{x} & ={A}^{-1}\mathbf{b} \\  & =\begin{bmatrix}1 & -1 \\ 0 & 1\end{bmatrix}\begin{bmatrix}5 \\ 2\end{bmatrix} \\  & =\begin{bmatrix}3 \\ 2\end{bmatrix}.\end{aligned}$$

So the solution is $x=3$ and $y=2.$



### example 17592186092023 — Solving a 2x2 System of Equations Using an Inverse Matrix

Find a solution to the system of linear equations

$$
\left\{\begin{aligned}2x+y &=2 \\ 4x+3y &=6.\end{aligned}\right.
$$

This system can be written as

$$
{\left[ \begin{array}{cc}2 & 1 \\ 4 & 3\end{array} \right]}
{\left[ \begin{array}{c}x \\ y\end{array} \right]}=
{\left[ \begin{array}{c}2 \\ 6\end{array} \right]}.
$$

To find the solution, we need to calculate the inverse of the coefficient matrix $A = {\left[ \begin{array}{cc}2 & 1 \\ 4 & 3\end{array} \right]}.$ This gives

$$
\begin{aligned}{A}^{-1} & =\frac{1}{3\cdot 2-4\cdot 1}\begin{bmatrix}3 & -1 \\ -4 & 2\end{bmatrix} \\  & =\frac{1}{2}\begin{bmatrix}3 & -1 \\ -4 & 2\end{bmatrix}.\end{aligned}
$$

We can now find the solution to this system:

$$\begin{aligned}\mathbf{x} & ={A}^{-1}\mathbf{b} \\  & =\frac{1}{2}\begin{bmatrix}3 & -1 \\ -4 & 2\end{bmatrix}\begin{bmatrix}2 \\ 6\end{bmatrix} \\  & =\frac{1}{2}\begin{bmatrix}0 \\ 4\end{bmatrix} \\  & =\begin{bmatrix}0 \\ 2\end{bmatrix}\end{aligned}$$

So the solution is $x=0$ and $y=2.$

### example 17592186092024 — Solving a 2x2 System of Equations Using an Inverse Matrix With Reorganization

Solve the system of linear equations

$$
\left\{\begin{aligned}2x-3y &=5 \\ 6y-5x &=-8.\end{aligned}\right.
$$

First, we reorganize the equations so that they are in the right order, to get

$$
\left\{\begin{aligned}2x-3y &=5 \\ -5x+6y &=-8.\end{aligned}\right.
$$

Now, we can represent this system of equations in the form $A\mathbf{x} =\mathbf{b}\mathbin{:}$

$$
{\left[ \begin{array}{cc}2 & - 3 \\ - 5 & 6\end{array} \right]}
{\left[ \begin{array}{c}x \\ y\end{array} \right]}
={\left[ \begin{array}{c}5 \\ - 8\end{array} \right]}.
$$

To find the solution, we need to calculate the inverse of the coefficient matrix $A = {\left[ \begin{array}{cc}2 & - 3 \\ - 5 & 6\end{array} \right]}.$ This gives

$$
\begin{aligned}{A}^{-1} & =\frac{1}{6\cdot 2-3\cdot 5}\begin{bmatrix}6 & 3 \\ 5 & 2\end{bmatrix} \\  & =-\frac{1}{3}\begin{bmatrix}6 & 3 \\ 5 & 2\end{bmatrix}.\end{aligned}
$$

We can now find the solution to this system:

$$\begin{aligned}\mathbf{x} & ={A}^{-1}\mathbf{b} \\  & =-\frac{1}{3}\begin{bmatrix}6 & 3 \\ 5 & 2\end{bmatrix}\begin{bmatrix}5 \\ -8\end{bmatrix} \\  & =-\frac{1}{3}\begin{bmatrix}6 \\ 9\end{bmatrix} \\  & =\begin{bmatrix}-2 \\ -3\end{bmatrix}.\end{aligned}$$

Therefore, the solution is $x=-2$ and $y=-3.$

### tutorial 17592186093404 — Systems of Equations Where the Coefficient Matrix is Singular

Consider the system of equations

$$
\left\{\begin{aligned}2x+y &=3 \\ 6x+3y &=9.\end{aligned}\right.
$$

Can we use the matrix method of $\mathbf{x} = A^{-1}\mathbf{b}$ to find a solution to this system?

This system can be represented in the form $A\mathbf{x}=\mathbf{b}$ as

$$
\begin{bmatrix}2 & 1 \\ 6 & 3\end{bmatrix} \begin{bmatrix}x \\ y\end{bmatrix} = \begin{bmatrix}3 \\ 9\end{bmatrix}.
$$

To use this matrix method, we need to find $A^{-1}.$ However

$$
\det (A) = 2\cdot 3 - 1\cdot 6 =0.
$$

Therefore, $A$ is not invertible. So we cannot use the matrix method to find a solution to the system.

In general, if the coefficient matrix $A$ is not invertible, there is no unique solution. This means that either

- a solution may not exist, or

- there may be infinitely many solutions.



## Representative practice (first three per skill; full bank in practice.json)

### Solving a 2x2 System of Equations Using an Inverse Matrix (31 captured questions)

Question 17592186092678 — question.difficulty/easy

Which of the following represents the solution to the system of linear equations given below?

$$
\left\{\begin{aligned}x-2y &=1 \\ 2x+2y &=-1\end{aligned}\right.
$$

Solution: This system can be written as

$$
\begin{bmatrix}1 & -2 \\ 2 & 2\end{bmatrix}\begin{bmatrix}x \\ y\end{bmatrix}=\begin{bmatrix}1 \\ -1\end{bmatrix}.
$$

To find the solution, we need to calculate the inverse of the coefficient matrix 
$$
\displaystyle A=\begin{bmatrix}1 & -2 \\ 2 & 2\end{bmatrix}.
$$
This gives

$$
\begin{aligned}{A}^{-1} & =\frac{1}{1\cdot 2-(-2)\cdot 2}\begin{bmatrix}2 & 2 \\ -2 & 1\end{bmatrix} \\  & =\frac{1}{6}\begin{bmatrix}2 & 2 \\ -2 & 1\end{bmatrix}.\end{aligned}
$$

We can now represent the solution to this system, as follows:

$$\begin{aligned}\mathbf{x} & ={A}^{-1}\mathbf{b} \\  & =\frac{1}{6}\begin{bmatrix}2 & 2 \\ -2 & 1\end{bmatrix}\begin{bmatrix}1 \\ -1\end{bmatrix}\end{aligned}$$

Answer selection: x=\frac{1}{6}\begin{bmatrix}2 & 2 \\ -2 & 1\end{bmatrix}\begin{bmatrix}1 \\ -1\end{bmatrix}

Question 17592186092885 — question.difficulty/easy

Which of the following represents the solution to the system of linear equations given below?

$$
\left\{\begin{aligned}2x+y &=0 \\ 3x-6y &=2.\end{aligned}\right.
$$

Solution: This system can be written as

$$
\begin{bmatrix}2 & 1 \\ 3 & -6\end{bmatrix}\begin{bmatrix}x \\ y\end{bmatrix}=\begin{bmatrix}0 \\ 2\end{bmatrix}.
$$

To find the solution, we need to calculate the inverse of the coefficient matrix 
$$
\displaystyle A=\begin{bmatrix}2 & 1 \\ 3 & -6\end{bmatrix}.
$$
This gives

$$
\begin{aligned}{A}^{-1} & =\frac{1}{2\cdot (-6)-1\cdot 3}\begin{bmatrix}-6 & -1 \\ -3 & 2\end{bmatrix} \\  & =-\frac{1}{15}\begin{bmatrix}-6 & -1 \\ -3 & 2\end{bmatrix}.\end{aligned}
$$

We can now find the solution to this system as

$$\begin{aligned}\mathbf{x} & ={A}^{-1}\mathbf{b} \\  & =-\frac{1}{15}\begin{bmatrix}-6 & -1 \\ -3 & 2\end{bmatrix}\begin{bmatrix}0 \\ 2\end{bmatrix}.\end{aligned}$$

Answer selection: x=-\frac{1}{15}\begin{bmatrix}-6 & -1 \\ -3 & 2\end{bmatrix}\begin{bmatrix}0 \\ 2\end{bmatrix}

Question 17592186235397 — question.difficulty/easy

![](images/c1/c1d9f53c6aed4acd378f8554df5c8beaaea81e169b5284e51f87204a87b3d53d.png)

A housing complex designed by an architect is shown in the coordinate plane as the region $R$ with vertices $ABCD.$ A highway lies on the line $l$ with equation $2x+y+1=0.$ The area of the complex is $16$ hectares.

The solution of the system of linear equations

$$
\left\{\begin{aligned}2x+y+1 &=0 \\ 4x+3y-3 &=0\end{aligned}\right.
$$

gives the point where the highways meet. This solution can be written in matrix form as

$$\begin{bmatrix}x \\ y\end{bmatrix}=\frac{1}{2}\begin{bmatrix}\bbox[Gainsboro, 2pt]{a} & \bbox[Gainsboro, 2pt]{b} \\ -4 & 2\end{bmatrix}\begin{bmatrix}-1 \\ \bbox[Gainsboro, 2pt]{c}\end{bmatrix}$$

Find the values of $a,$ $b,$ and $c.$

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
$a\,=$

                                    
                                
                                    
                            
                                        {{field-1}}                
                                    
                                
                                    
                                        
                                        
$\,b\,=$

                                    
                                
                                    
                            
                                        {{field-2}}                
                                    
                                
                                    
                                        
                                        
$\,c\,=$

                                    
                                
                                    
                            
                                        {{field-3}}

Solution: This system can be written as

$$
\begin{bmatrix}2 & 1 \\ 4 & 3\end{bmatrix}\begin{bmatrix}x \\ y\end{bmatrix}=\begin{bmatrix}-1 \\ 3\end{bmatrix}.
$$

To find the solution, we need to calculate the inverse of the coefficient matrix $A=\begin{bmatrix}2 & 1 \\ 4 & 3\end{bmatrix}.$ This gives

$$
\begin{aligned}{A}^{-1} & =\frac{1}{2\cdot 3-4\cdot 1}\begin{bmatrix}3 & -1 \\ -4 & 2\end{bmatrix} \\  & =\frac{1}{2}\begin{bmatrix}3 & -1 \\ -4 & 2\end{bmatrix}.\end{aligned}
$$

Therefore, we can write the solution to this system as

$$\begin{aligned}\mathbf{x} & ={A}^{-1}\mathbf{b} \\  & =\frac{1}{2}\begin{bmatrix}\bbox[Gainsboro, 2pt]{{\color{blue}3}} & \bbox[Gainsboro, 2pt]{{\color{blue}-1}} \\ -4 & 2\end{bmatrix}\begin{bmatrix}-1 \\ \bbox[Gainsboro, 2pt]{{\color{blue}3}}\end{bmatrix}.\end{aligned}$$

Answer field-1: 3

Answer field-2: -1

Answer field-3: 3

### Solving a 2x2 System of Equations Using an Inverse Matrix With Reorganization (23 captured questions)

Question 17592186092528 — question.difficulty/moderate

Which of the following represents the solution to the system of linear equations given below?

$$
\left\{\begin{aligned}8y &=6 \\ -5x &=7-6y\end{aligned}\right.
$$

Solution: First, we reorganize the equations so that they are in the right order, to get

$$
\left\{\begin{aligned}8y &=6 \\ -5x+6y &=7\end{aligned}\right.
$$

Now, we can represent this system of equations in the form $A\mathbf{x}=\mathbf{b}:$

$$
\begin{bmatrix}0 & 8 \\ -5 & 6\end{bmatrix}\begin{bmatrix}x \\ y\end{bmatrix}=\begin{bmatrix}6 \\ 7\end{bmatrix}.
$$

To find the solution, we need to calculate the inverse of the coefficient matrix 
$$
\displaystyle A=\begin{bmatrix}0 & 8 \\ -5 & 6\end{bmatrix}
$$
This gives

$$
\begin{aligned}{A}^{-1} & =\frac{1}{6\cdot 0-(-5)\cdot 8}\begin{bmatrix}6 & -8 \\ 5 & 0\end{bmatrix} \\  & =\frac{1}{40}\begin{bmatrix}6 & -8 \\ 5 & 0\end{bmatrix}.\end{aligned}
$$

We can now represent the solution to this system, as follows:

$$\begin{aligned}\mathbf{x} & ={A}^{-1}\mathbf{b} \\  & =\frac{1}{40}\begin{bmatrix}6 & -8 \\ 5 & 0\end{bmatrix}\begin{bmatrix}6 \\ 7\end{bmatrix}\end{aligned}$$

Answer selection: x=\frac{1}{40}\begin{bmatrix}6 & -8 \\ 5 & 0\end{bmatrix}\begin{bmatrix}6 \\ 7\end{bmatrix}

Question 17592186092884 — question.difficulty/moderate

Which of the following represents the solution to the system of linear equations given below?

$$
\left\{\begin{aligned}2x &=5y \\ x &=-2\end{aligned}\right.
$$

Solution: First, we reorganize the equations so that they are in the right order, to get

$$
\left\{\begin{aligned}2x-5y &=0 \\ x &=-2.\end{aligned}\right.
$$

Now, we can represent this system of equations in the form $A\mathbf{x}=\mathbf{b}:$

$$
\begin{bmatrix}2 & -5 \\ 1 & 0\end{bmatrix}\begin{bmatrix}x \\ y\end{bmatrix}=\begin{bmatrix}0 \\ -2\end{bmatrix}.
$$

To find the solution, we need to calculate the inverse of the coefficient matrix $A=\begin{bmatrix}2 & -5 \\ 1 & 0\end{bmatrix}.$ This gives

$$
\begin{aligned}{A}^{-1} & =\frac{1}{2\cdot 0-(-5)\cdot 1}\begin{bmatrix}0 & 5 \\ -1 & 2\end{bmatrix} \\  & =\frac{1}{5}\begin{bmatrix}0 & 5 \\ -1 & 2\end{bmatrix}.\end{aligned}
$$

We can now find the solution to this system as:

$$\begin{aligned}\mathbf{x} & ={A}^{-1}\mathbf{b} \\  & =\frac{1}{5}\begin{bmatrix}0 & 5 \\ -1 & 2\end{bmatrix}\begin{bmatrix}0 \\ -2\end{bmatrix}\end{aligned}$$

Answer selection: x=\frac{1}{5}\begin{bmatrix}0 & 5 \\ -1 & 2\end{bmatrix}\begin{bmatrix}0 \\ -2\end{bmatrix}

Question 17592186237950 — question.difficulty/moderate

Which of the following represents the solution to the system of linear equations given below?

$$
\begin{aligned}\left\{\begin{aligned}4x-2y &=4 \\ 6 &=5x\end{aligned}\right.\end{aligned}
$$

Solution: First, we reorganize the equations so that they are in the right order, to get

$$
\begin{aligned}\left\{\begin{aligned}4x-2y &=4 \\ 5x &=6.\end{aligned}\right.\end{aligned}
$$

Now, we can represent this system of equations in the form $A\mathbf{x}=\mathbf{b}:$

$$
\begin{bmatrix}4 & -2 \\ 5 & 0\end{bmatrix}\begin{bmatrix}x \\ y\end{bmatrix}=\begin{bmatrix}4 \\ 6\end{bmatrix}.
$$

To find the solution, we need to calculate the inverse of the coefficient matrix $A=\begin{bmatrix}4 & -2 \\ 5 & 0\end{bmatrix}.$ This gives

$$
\begin{aligned}{A}^{-1} & =\frac{1}{4\cdot 0-5\cdot (-2)}\begin{bmatrix}0 & 2 \\ -5 & 4\end{bmatrix} \\  & =\frac{1}{10}\begin{bmatrix}0 & 2 \\ -5 & 4\end{bmatrix}.\end{aligned}
$$

We can now find the solution to this system as:

$$\begin{aligned}\mathbf{x} & ={A}^{-1}\mathbf{b} \\  & =\frac{1}{10}\begin{bmatrix}0 & 2 \\ -5 & 4\end{bmatrix}\begin{bmatrix}4 \\ 6\end{bmatrix}\end{aligned}$$

Answer selection: x=\frac{1}{10}\begin{bmatrix}0 & 2 \\ -5 & 4\end{bmatrix}\begin{bmatrix}4 \\ 6\end{bmatrix}
